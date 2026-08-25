"""The Ask datumwise HTTP service. Small on purpose.

Stdlib only — no FastAPI, no uvicorn, no pydantic. The whole API is seven endpoints over JSON, and
this repo runs a dependency cap guard; a web framework would be more machinery than the product.
If the surface grows past this file's size, that is the signal to adopt one.

WHY THIS IS A SEPARATE SERVICE AND NOT VERCEL FUNCTIONS ON THE SITE. apps/website is `output: 'static'`
and ships through a heavily gated shipped-coherent pipeline (branch-coherent build, flap detector,
fragment integrity, discoverability, post-deploy edge verification). Turning it hybrid to host an
agent would put a stateful, model-calling, database-backed surface inside the pipeline that guards
datumwise's publication claims. Keeping Ask on its own deployment leaves that pipeline exactly as
verified in #229/#230, and keeps the service portable — the brief asked for both.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
import traceback
import uuid
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from . import answer as ask_answer
from . import providers, retrieve, store, verify

# The site is the only browser origin that should be able to spend our model budget. Previews are
# allowed by pattern so a PR preview works without redeploying the service.
ALLOWED_ORIGINS = re.compile(
    r"^https://(datumwise\.ai|www\.datumwise\.ai|website-[a-z0-9-]+\.vercel\.app)$"
)
ALLOW_LOCAL = os.environ.get("ASK_ALLOW_LOCAL") == "1"

MAX_QUESTION = 600

# ── RATE LIMIT ────────────────────────────────────────────────────────────────────────────────────
# /ask spends real money on every uncached call. The origin allow-list above is NOT a defence
# against that and must not be mistaken for one: CORS is enforced by browsers, so it stops a page on
# another site from spending our budget, and stops nothing else. `curl` ignores it entirely.
#
# So the actual protection is here, and it is deliberately crude: a per-IP token bucket, in memory,
# no dependency, no store. It will not survive a distributed abuser and is not meant to — it exists
# so that one script pointed at this endpoint cannot run up a bill before a human notices. If the
# lab surface attracts real traffic, this is the first thing to replace with something durable.
ASK_PER_HOUR = int(os.environ.get("ASK_RATE_PER_HOUR", "30"))
ASK_PER_DAY = int(os.environ.get("ASK_RATE_PER_DAY", "120"))
_hits: dict[str, deque] = defaultdict(deque)
_hits_lock = threading.Lock()


def _rate_ok(ip: str) -> tuple[bool, str | None]:
    now = time.time()
    with _hits_lock:
        q = _hits[ip]
        while q and now - q[0] > 86_400:
            q.popleft()
        last_hour = sum(1 for t in q if now - t <= 3_600)
        if last_hour >= ASK_PER_HOUR:
            return False, f"more than {ASK_PER_HOUR} questions in an hour from this address"
        if len(q) >= ASK_PER_DAY:
            return False, f"more than {ASK_PER_DAY} questions in a day from this address"
        q.append(now)
        # Bound the table so the dict cannot grow without limit on a long-lived process.
        if len(_hits) > 20_000:
            for k in [k for k, v in list(_hits.items()) if not v or now - v[-1] > 86_400][:5_000]:
                _hits.pop(k, None)
        return True, None


def _safe_error(e: Exception) -> str:
    """What a stranger is allowed to be told when something breaks.

    OBSERVED 2026-08-25: the OpenAI account ran out of credits and the raw provider error went
    straight to the browser — provider name, HTTP status, error code, and a billing URL for our
    organisation. None of that is the reader's business and some of it is ours alone. The full
    exception still goes to the server log via traceback.print_exc(); only this reaches the client.
    """
    text = str(e)
    if "insufficient_quota" in text or "credit_balance" in text or "429" in text:
        return ("Ask is temporarily unable to answer new questions. The answered questions below "
                "are still readable.")
    if "OPENAI_API_KEY" in text or "API_KEY" in text:
        return "Ask is not configured to answer questions right now."
    return "Ask could not answer that just now."


class Handler(BaseHTTPRequestHandler):
    server_version = "ask-datumwise/0"

    # ── plumbing ──────────────────────────────────────────────────────────────────────────────────
    def _origin_ok(self) -> str | None:
        o = self.headers.get("Origin")
        if not o:
            return "*"
        if ALLOWED_ORIGINS.match(o):
            return o
        if ALLOW_LOCAL and re.match(r"^http://(localhost|127\.0\.0\.1)(:\d+)?$", o):
            return o
        return None

    def _send(self, code: int, body: dict) -> None:
        raw = json.dumps(body).encode()
        origin = self._origin_ok() or "null"
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, fmt, *args):  # quieter, and no query strings in logs
        print(f"{self.address_string()} {fmt % args}", flush=True)

    def do_OPTIONS(self):  # noqa: N802
        self._send(204, {})

    # ── routes ────────────────────────────────────────────────────────────────────────────────────
    def do_GET(self):  # noqa: N802
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/health":
                return self._send(200, {
                    "ok": True,
                    "index": retrieve.stats(),
                    "providers": providers.available(),
                    "model": providers.DEFAULT_MODEL,
                    "registryDois": verify.registry_doi_count(),
                })
            if u.path == "/qa":
                return self._send(200, {"items": store.listing(int(q.get("limit", ["50"])[0]))})
            if u.path.startswith("/qa/"):
                qa = store.get(u.path[4:], bump_view=True)
                return self._send(200, qa) if qa else self._send(404, {"error": "no such Q&A"})
            if u.path == "/usage":
                return self._send(200, store.usage_totals())
            return self._send(404, {"error": "no such route"})
        except Exception as e:
            traceback.print_exc()
            return self._send(500, {"error": _safe_error(e)})

    def do_POST(self):  # noqa: N802
        u = urlparse(self.path)
        if not self._origin_ok():
            return self._send(403, {"error": "origin not allowed"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            if n > 64_000:
                return self._send(413, {"error": "payload too large"})
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"error": "invalid JSON"})

        try:
            if u.path == "/ask":
                question = (body.get("question") or "").strip()
                if not question:
                    return self._send(400, {"error": "question is required"})
                if len(question) > MAX_QUESTION:
                    return self._send(400, {"error": f"question must be under {MAX_QUESTION} chars"})
                # Fly puts the real client address in Fly-Client-IP; the socket peer is the proxy.
                ip = (self.headers.get("Fly-Client-IP")
                      or self.headers.get("X-Forwarded-For", "").split(",")[0].strip()
                      or self.client_address[0])
                ok, why = _rate_ok(ip)
                if not ok:
                    return self._send(429, {
                        "error": "Ask is rate-limited on this lab surface — " + why +
                                 ". The answered questions below are free to read.",
                    })
                conv = body.get("conversation") or uuid.uuid4().hex[:12]
                history = body.get("history") or None
                if history and len(history) > 12:
                    history = history[-12:]
                res = ask_answer.ask_and_record(
                    question, conversation=conv, history=history, parent_id=body.get("parentId"),
                )
                # The reader gets the answer and its receipts. Retrieval scores, token counts and the
                # raw verify payload stay server-side — implementation metadata, per the brief.
                return self._send(200, {
                    "id": res.get("id"), "conversation": conv,
                    "question": res["question"], "answer": res["answer"],
                    "sources": res["sources"], "external": res.get("external", []),
                    "corpusSettles": res.get("corpusSettles"),
                    "cached": res.get("cached", False),
                    "stars": res.get("stars"), "ratings": res.get("ratings", 0),
                    "views": res.get("views", 0),
                })
            if u.path == "/vote":
                qa_id, voter = body.get("id"), body.get("voter")
                if not qa_id or not voter or "helpful" not in body:
                    return self._send(400, {"error": "id, voter and helpful are required"})
                out = store.vote(qa_id, str(voter)[:64], bool(body["helpful"]))
                return self._send(200, out) if out else self._send(404, {"error": "no such Q&A"})
            return self._send(404, {"error": "no such route"})
        except Exception as e:
            traceback.print_exc()
            return self._send(500, {"error": _safe_error(e)})


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    print(f"ask-datumwise on :{port} | index={retrieve.stats()} | model={providers.DEFAULT_MODEL}",
          flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
