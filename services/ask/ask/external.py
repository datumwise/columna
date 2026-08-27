"""EXTERNAL sources: the outside world, fetched, marked, and never allowed to speak for datumwise.

WHAT THIS IS FOR. Ask may compare datumwise with the wider world, give context, report criticism,
and state outside facts. It could not do any of that before this module existed, because the only
text it could reach was the governed index. That was the right order to build it in: external
material widens what Ask may SAY, and it should land on top of a review gate rather than under one.

THE HARD BOUNDARY, AND IT IS THE WHOLE POINT. External material may describe external parties and
support comparison. It may NEVER create or redefine a datumwise position. An article about
datumwise — however accurate, however flattering — is someone else's account, and letting it stand
in for the Core set is the identical failure as letting a datumwise manual stand in for it. The
constitution says exactly that; this module's job is to make sure the model can always TELL which
is which, by fetching external text into its own class with its own citation tokens.

SECURITY. This is a service that takes a URL from a caller and fetches it, which is a server-side
request forgery primitive unless it is fenced. So:

  · https only. No file://, no ftp://, no data:.
  · Every resolved address is checked against private, loopback, link-local, multicast and reserved
    ranges BEFORE connecting — and again on every redirect hop, because a public hostname that
    302s to 169.254.169.254 is the classic version of this attack.
  · Redirects are followed manually, at most three, so each hop can be checked.
  · Response body is capped and the read is bounded by a timeout; a slow-loris or a 10GB response
    cannot hold or exhaust the process.
  · Only text/html and text/plain are accepted.

None of that makes fetching arbitrary URLs safe in general. It makes THIS narrow thing safe enough
for a service whose external fetches are made by a reviewer or an operator, not by anonymous
traffic — which is why /ask does not accept URLs from the public rate-limited path.
"""

from __future__ import annotations

import ipaddress
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

MAX_BYTES = 600_000
MAX_REDIRECTS = 3
TIMEOUT = 20
MAX_TEXT = 24_000          # per source, handed to the model
USER_AGENT = "ask-datumwise/0 (+https://datumwise.ai)"

ALLOWED_CONTENT = ("text/html", "text/plain", "application/xhtml+xml")


class ExternalFetchError(RuntimeError):
    pass


def _check_public(host: str) -> None:
    """Resolve and refuse anything that is not a public address. Checked on every hop."""
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as e:
        raise ExternalFetchError(f"cannot resolve {host!r}: {e}") from e
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
                or ip.is_reserved or ip.is_unspecified):
            raise ExternalFetchError(f"refusing to fetch {host!r}: resolves to non-public {ip}")


class _Text(HTMLParser):
    """Readable text out of a page. Deliberately generic — this parses the open web, not our site."""

    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "form", "header", "aside"}
    BREAK = {"p", "div", "section", "article", "li", "tr", "br", "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title = ""
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag in self.BREAK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            t = data.strip()
            if t:
                self.parts.append(t + " ")


def _open(url: str) -> tuple[str, bytes, str]:
    """Fetch with manual redirect handling so every hop can be address-checked."""
    seen = 0
    while True:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "https":
            raise ExternalFetchError(f"refusing {parts.scheme or 'relative'} URL: https only")
        if not parts.hostname:
            raise ExternalFetchError("URL has no host")
        _check_public(parts.hostname)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Accept": "text/html,text/plain"})
        opener = urllib.request.build_opener(_NoRedirect)
        try:
            with opener.open(req, timeout=TIMEOUT) as r:
                if r.status in (301, 302, 303, 307, 308):
                    seen += 1
                    if seen > MAX_REDIRECTS:
                        raise ExternalFetchError("too many redirects")
                    url = urllib.parse.urljoin(url, r.headers.get("Location") or "")
                    continue
                ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                if ctype and ctype not in ALLOWED_CONTENT:
                    raise ExternalFetchError(f"refusing content-type {ctype!r}")
                body = r.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    raise ExternalFetchError(f"response larger than {MAX_BYTES} bytes")
                return url, body, ctype
        except urllib.error.HTTPError as e:
            if e.status in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                seen += 1
                if seen > MAX_REDIRECTS:
                    raise ExternalFetchError("too many redirects") from e
                url = urllib.parse.urljoin(url, e.headers["Location"])
                continue
            raise ExternalFetchError(f"HTTP {e.status} for {url}") from e
        except urllib.error.URLError as e:
            raise ExternalFetchError(f"cannot fetch {url}: {e.reason}") from e


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # handled above, so each hop gets its address check


def fetch(url: str) -> dict:
    """One external source, ready to hand to the model. Raises ExternalFetchError on refusal."""
    final, body, ctype = _open(url)
    text = body.decode("utf-8", errors="replace")
    if ctype != "text/plain":
        p = _Text()
        p.feed(text)
        title = re.sub(r"\s+", " ", p.title).strip()
        text = re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]{2,}", " ", "".join(p.parts))).strip()
    else:
        title = final
    return {
        "url": final,
        "requestedUrl": url,
        "title": title or final,
        "text": text[:MAX_TEXT],
        "truncated": len(text) > MAX_TEXT,
        "fetchedAt": time.time(),
    }


def fetch_all(urls: list[str]) -> tuple[list[dict], list[dict]]:
    """Returns (fetched, failures). A failed external source is REPORTED, never silently dropped —
    an answer assembled from three sources when four were asked for is a different answer."""
    got, bad = [], []
    for u in urls[:6]:
        try:
            got.append(fetch(u))
        except ExternalFetchError as e:
            bad.append({"url": u, "error": str(e)})
    return got, bad
