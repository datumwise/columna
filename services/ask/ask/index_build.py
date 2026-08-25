"""Build the Ask retrieval index from the SHIPPED SITE BUILD, not from the source tree.

WHY dist/ AND NOT src/content/corpus/. This is the load-bearing decision in the whole retrieval
layer, so it gets the long comment.

`src/content/corpus/` holds 27 markdown files, and FOUR of them are superseded drafts that no page
imports: `theory_of_data_an_introduction_v1_1.md` (superseded by v2_2), `frameql_an_introduction_v2_1.md`
(superseded by v2_3), `launch_story_v6.md`, `launch_post_FINAL.md`. They sit in the directory looking
exactly as authoritative as the live ones. A retriever pointed at that directory would happily quote
the v1.1 Theory of Data introduction as datumwise's present position — which is the precise failure
Gateway 1 just spent a whole slice removing from /research. Re-introducing it inside the agent, one
week later, would be indefensible.

`dist/` is the build the reader actually gets. Pointing at it buys four properties for free:

  1. ORPHANS CANNOT BE RETRIEVED. Not by a filter that must be maintained — by construction. If no
     page imports it, it is not in the build, so it is not in the index. The superseded drafts are
     excluded by the same mechanism that keeps them off the website.
  2. THE ROUTE IS EXACT AND CHECKABLE. `dist/what-is-a-universe/index.html` IS `/what-is-a-universe`.
     A citation is not a guess about where something lives; it is the path it was read from.
  3. THE ANCHORS ARE REAL. Astro emits `<h2 id="...">` and this repo gates them — 167/167 internal
     fragments resolve, checked on every build. So a section-level citation lands on the exact
     heading, and the gate that keeps site links honest keeps Ask's links honest too.
  4. EDITION-PINNING IS INHERITED, NOT RE-DERIVED. Where a route renders a pinned deposited edition,
     the index gets that edition's bytes, because that is what the route serves. Ask cannot
     accidentally quote a different edition than the one it links to.

The cost is honest and worth stating: 23 of the 43 catalogued sources are deposit-only (on Zenodo,
not in this repo), so Ask can cite their record but cannot quote their text. The skill is told this
explicitly, and told to say so rather than to improvise. A prototype that knows the shape of its own
ignorance is worth more than one that papers over it.

STANDING COMES FROM THE CATALOG, NOT FROM THE TEXT. Each chunk is joined to registry/sources by
route, so every retrieved passage arrives carrying role, current-record version/date, edition-pinned
status, and preserved/historical status. The model is never asked to remember standing; it is handed
standing with the passage. That is the Level-2 half of the design: make the tool unable to return a
bare quotation.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DIST = REPO / "apps" / "website" / "dist"
SOURCES_JSON = REPO / "registry" / "sources" / "sources.json"
WORKS_JSON = REPO / "registry" / "publications" / "works.json"
RECORDS_JSON = REPO / "registry" / "publications" / "records.json"

# Routes that are navigation, machine surfaces, or duplicates rather than prose a reader would be
# sent to as a source. Excluding them keeps retrieval pointed at material that can actually support
# an answer.
SKIP_ROUTES = {
    "/",              # the front gate is an argument, not a citable source
    "/install",
    "/explorer",      # a live instrument; cited by route, not quoted
}
SKIP_PREFIXES = ("/_astro", "/fonts")


class _Extract(HTMLParser):
    """Pull readable prose out of built HTML, tracking the nearest heading anchor.

    Deliberately hand-rolled rather than a dependency: this repo runs a dependency cap guard, and
    the job is narrow enough that a parser plus a tag blacklist is genuinely the simpler thing.
    """

    DROP = {"script", "style", "nav", "footer", "svg", "noscript", "head"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[tuple[str, str, str]] = []  # (anchor, heading, text)
        self._depth_drop = 0
        self._anchor = ""
        self._heading = ""
        self._in_heading = 0
        self._heading_buf: list[str] = []
        self._buf: list[str] = []
        self._title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.DROP:
            self._depth_drop += 1
            return
        if tag == "title":
            self._in_title = True
            return
        if self._depth_drop:
            return
        if tag in ("h1", "h2", "h3"):
            self._flush()
            self._in_heading = 1
            self._heading_buf = []
            self._pending_anchor = a.get("id", "")
        elif tag in ("p", "li", "div", "section", "br", "td", "tr", "blockquote", "pre"):
            self._buf.append(" ")

    def handle_endtag(self, tag):
        if tag in self.DROP:
            self._depth_drop = max(0, self._depth_drop - 1)
            return
        if tag == "title":
            self._in_title = False
            return
        if self._depth_drop:
            return
        if tag in ("h1", "h2", "h3") and self._in_heading:
            self._in_heading = 0
            self._heading = re.sub(r"\s+", " ", "".join(self._heading_buf)).strip()
            self._anchor = getattr(self, "_pending_anchor", "")

    def handle_data(self, data):
        if self._in_title:
            self._title += data
            return
        if self._depth_drop:
            return
        if self._in_heading:
            self._heading_buf.append(data)
        else:
            self._buf.append(data)

    def _flush(self):
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        if text:
            self.parts.append((self._anchor, self._heading, text))
        self._buf = []

    def close(self):
        super().close()
        self._flush()


@dataclass
class Chunk:
    chunkId: str
    route: str
    anchor: str          # "" when the passage sits above the first heading
    heading: str
    title: str           # the page title, for display
    text: str
    # ── standing, joined from the source catalog ──────────────────────────────────────────────────
    sourceId: str | None
    sourceLabel: str | None
    role: str | None
    standing: str        # a composed, human-readable sentence — what the model is handed
    isHistorical: bool
    isEditionPinned: bool
    url: str             # the exact link a reader clicks to check the claim


def _load_standing() -> dict[str, dict]:
    """route -> standing facts, derived from the registries. Types no publication fact by hand.

    This mirrors `apps/website/src/data/publications.ts` and `sources.ts` EXACTLY, on purpose:

      · current record = the record whose `status` is ruled `current`, of which the checker enforces
        exactly one per work. NOT the newest by date and NOT the highest version string. The site's
        `currentRecord()` carries a long comment about why, and the reason applies identically here:
        picking a winner by date is a heuristic that will one day pick a different record than the
        registry rules, and then Ask and /research would disagree about datumwise's own position.
      · edition-differs = readable.recordId !== current.recordId, DERIVED. The catalog's
        `editionPinned` boolean is a declaration of editorial intent; `editionDiffers` is the fact.
        The page renders on the fact, so Ask retrieves on the fact.

    Two surfaces, one rule. If this ever drifts from the TypeScript, the eval set's currency traps
    fail, which is the point of having them.
    """
    cat = json.loads(SOURCES_JSON.read_text())
    sources = cat["sources"] if isinstance(cat, dict) else cat
    works = {w["workId"]: w for w in json.loads(WORKS_JSON.read_text())}
    records = json.loads(RECORDS_JSON.read_text())
    by_id = {r["recordId"]: r for r in records}

    def current_for(work_id: str) -> dict:
        found = [r for r in records if r.get("workId") == work_id and r.get("status") == "current"]
        if len(found) != 1:
            raise SystemExit(
                f"PUBLICATION REGISTRY: work {work_id!r} has {len(found)} current records, expected "
                f"exactly 1. scripts/check_publications.py will say precisely how."
            )
        return found[0]

    out: dict[str, dict] = {}
    for s in sources:
        route = s.get("route")
        if not route:
            continue
        work_id = s.get("workId")
        cur = current_for(work_id) if work_id else None
        readable = by_id.get(s["recordId"]) if s.get("recordId") else None
        pinned = bool(readable and cur and readable.get("recordId") != cur.get("recordId"))

        bits: list[str] = []
        if cur:
            v = f" v{cur['version']}" if cur.get("version") else ""
            bits.append(f"current record{v} ({cur.get('date','')})")
        if pinned and readable:
            rv = f"v{readable['version']}" if readable.get("version") else "the first edition"
            bits.append(
                f"EDITION-PINNED: this route renders the deposited {rv} "
                f"({readable.get('date','')}), which is NOT the current record"
            )
        if s.get("preservedState"):
            bits.append(
                f"PRESERVED HISTORICAL STATE as of {s['preservedState']} — not current authority"
            )
        if s.get("generatedBy"):
            bits.append(f"generated by {s['generatedBy']}")
        if "build-adjudicated" in (s.get("gates") or []):
            bits.append("build-adjudicated: the build fails if the displayed claim drifts")
        if "currency-stamp" in (s.get("gates") or []):
            bits.append("currency-stamped against the shipped package")
        if not work_id:
            bits.append("not a deposited publication — no DOI, no Zenodo record")

        label = works[work_id]["canonicalLabel"] if work_id else s.get("title")
        out[route.rstrip("/") or "/"] = {
            "sourceId": s["sourceId"],
            "sourceLabel": label,
            "role": s.get("role"),
            "standing": "; ".join(bits) if bits else "onsite source",
            "isHistorical": bool(s.get("preservedState")),
            "isEditionPinned": pinned,
        }
    return out


def _route_of(path: Path) -> str:
    rel = path.relative_to(DIST).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("/index.html")]
    return "/" + rel[: -len(".html")] if rel.endswith(".html") else "/" + rel


def build(min_chars: int = 220, max_chars: int = 2600) -> list[Chunk]:
    if not DIST.exists():
        raise SystemExit(
            f"no site build at {DIST}. Run `npm run build` in apps/website first — the index is "
            f"derived from the shipped build on purpose (see this module's docstring)."
        )
    standing = _load_standing()
    chunks: list[Chunk] = []

    for html_path in sorted(DIST.rglob("*.html")):
        route = _route_of(html_path)
        if route in SKIP_ROUTES or any(route.startswith(p) for p in SKIP_PREFIXES):
            continue
        raw = html_path.read_text(encoding="utf-8", errors="replace")
        # Redirect stubs are not sources. They are 200-with-a-meta-refresh (see #230).
        if 'http-equiv="refresh"' in raw and len(raw) < 2000:
            continue
        p = _Extract()
        p.feed(raw)
        p.close()
        title = re.sub(r"\s+", " ", p._title).strip() or route
        st = standing.get(route, {})

        for anchor, heading, text in p.parts:
            if len(text) < min_chars:
                continue
            # Long sections are split on sentence boundaries so a citation stays section-anchored
            # while the passage handed to the model stays readable.
            pieces = [text]
            if len(text) > max_chars:
                pieces, cur = [], ""
                for sent in re.split(r"(?<=[.!?])\s+", text):
                    if len(cur) + len(sent) > max_chars and cur:
                        pieces.append(cur)
                        cur = sent
                    else:
                        cur = (cur + " " + sent).strip()
                if cur:
                    pieces.append(cur)
            for i, piece in enumerate(pieces):
                if len(piece) < min_chars:
                    continue
                frag = f"#{anchor}" if anchor else ""
                chunks.append(
                    Chunk(
                        chunkId=f"{route}{frag}::{i}",
                        route=route,
                        anchor=anchor,
                        heading=heading,
                        title=title,
                        text=piece,
                        sourceId=st.get("sourceId"),
                        sourceLabel=st.get("sourceLabel"),
                        role=st.get("role"),
                        standing=st.get("standing", "onsite page (not in the source catalog)"),
                        isHistorical=bool(st.get("isHistorical")),
                        isEditionPinned=bool(st.get("isEditionPinned")),
                        url=f"https://datumwise.ai{route}{frag}",
                    )
                )
    return chunks


def main() -> None:
    chunks = build()
    out = Path(__file__).resolve().parent.parent / "index" / "chunks.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([asdict(c) for c in chunks], indent=0, ensure_ascii=False))
    routes = sorted({c.route for c in chunks})
    hist = sum(1 for c in chunks if c.isHistorical)
    pinned = sum(1 for c in chunks if c.isEditionPinned)
    catalogued = sum(1 for c in chunks if c.sourceId)
    print(f"index built: {len(chunks)} chunks across {len(routes)} routes -> {out}")
    print(f"  catalogued {catalogued} | historical {hist} | edition-pinned {pinned}")


if __name__ == "__main__":
    main()
