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
AUTHORITY_JSON = REPO / "registry" / "sources" / "ask-authority.json"
DEPOSITS = Path(__file__).resolve().parent.parent / "deposits"
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


# IDENTIFIERS ARE NOT INDEXED. THE REGISTRY OWNS THEM.
#
# G7 caught this and G7 was right. The first version of this index committed the built page TEXT,
# which contains DOIs — so chunks.json became a second source of truth for 38 publication
# identifiers. If a record is superseded and the site rebuilds but the index is not regenerated,
# the agent would quote a DOI the site no longer shows. check_publications.py states the rule
# exactly: "a derived surface reads the registry; the moment it also types a DOI, it is a second
# source of truth wearing the clothes of the first."
#
# So DOIs and Zenodo record links are REDACTED out of indexed prose, and the chunk instead carries
# `currentRecordId` — a foreign key. The identifier itself is resolved from records.json at REQUEST
# time (retrieve.py), inside the running service, from the registry that ships in the image. The
# agent therefore cannot cite a stale DOI: it never sees one that did not come from the registry
# one moment ago.
#
# This is the same discipline that took the publication list off /about and the footer, applied to
# the agent. It is a better design than the one the gate rejected.
_DOI = re.compile(r"\b10\.5281/zenodo\.\d+\b", re.I)
_ZURL = re.compile(r"https?://(?:www\.)?zenodo\.org/records?/\d+", re.I)


def _redact_identifiers(text: str) -> str:
    text = _ZURL.sub("(Zenodo record — resolved from the registry)", text)
    return _DOI.sub("(DOI — resolved from the registry)", text)


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
    # FOREIGN KEYS, never facts. Resolved against records.json at request time so the identifier a
    # reader is given is the one the registry rules right now, not the one that was true at index
    # time. Same rule the site's own surfaces follow.
    currentRecordId: str | None
    readableRecordId: str | None
    # ── CORPUS LAYER (Huayin, 2026-08-25) ─────────────────────────────────────────────────────────
    # "core"           — entitled to establish "datumwise holds ...". Ask's default corpus.
    # "reference"      — available when the question calls for its jurisdiction. NOT weak, obsolete
    #   or untrusted: several reference sources are the highest authority for the thing they
    #   actually establish. Jurisdiction, not rank.
    layer: str
    jurisdiction: str | None


def _membership() -> tuple[dict[str, str], dict[str, str]]:
    """sourceId -> layer, and sourceId -> jurisdiction. Ruled in ask-authority.json.

    Reads ASK'S OWN manifest, not current-corpus.json. Those were one file until 2026-08-26, and
    that file is also read by apps/website/src/data/sources.ts to build the /research page. One
    ruling was therefore governing two different questions — what a reader is shown, and what an
    agent may assert datumwise's position from — and neither could move without moving the other.
    """
    c = json.loads(AUTHORITY_JSON.read_text())
    layer = {sid: "core" for sid in c["core"]["sourceIds"]}
    juris: dict[str, str] = {}
    for e in c["reference"]["entries"]:
        sid = e if isinstance(e, str) else e["sourceId"]
        layer[sid] = "reference"
        if isinstance(e, dict):
            juris[sid] = e.get("jurisdiction")
    for e in c.get("out", []):
        sid = e if isinstance(e, str) else e["sourceId"]
        layer[sid] = "out"
    return layer, juris


def _current_record_for(records: list[dict], work_id: str | None) -> dict | None:
    """The record the registry currently rules as current for this work. Exactly one, or none."""
    if not work_id:
        return None
    found = [r for r in records if r.get("workId") == work_id and r.get("status") == "current"]
    if len(found) > 1:
        raise SystemExit(
            f"PUBLICATION REGISTRY: work {work_id!r} has {len(found)} current records, expected at "
            f"most 1. scripts/check_publications.py will say precisely how."
        )
    return found[0] if found else None


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
    records = json.loads(RECORDS_JSON.read_text())
    by_id = {r["recordId"]: r for r in records}
    layer_of, juris_of = _membership()

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

        # The composed sentence carries the SHAPE of the standing, never the numbers. Version, date
        # and DOI are publication facts; they are resolved from the registry at request time and
        # spliced in by retrieve.py. This is what keeps chunks.json `derived` in fact and not only
        # in name.
        bits: list[str] = []
        if cur:
            bits.append("{CURRENT}")
        if pinned and readable:
            bits.append("EDITION-PINNED: this route renders the deposited {READABLE}, which is NOT "
                        "the current record")
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

        # ONE NAMING RULE, IN ALL THREE PLACES (2026-08-26). The deposit path below already rules
        # that an explicitly titled source pinned to a non-current record keeps its own dated title,
        # and citations.py re-resolves stored labels by the same rule. A ROUTE for such a source was
        # the one place still falling back to the work's label — which, the day
        # /history/analytical-governance-v1-1 was added, would have labelled a preserved historical
        # page "Analytical Governance" and made it read as the current work.
        label = (s.get("title") if pinned and s.get("title")
                 else works[work_id]["canonicalLabel"] if work_id else s.get("title"))
        out[route.rstrip("/") or "/"] = {
            "layer": layer_of.get(s["sourceId"], "unruled"),
            "jurisdiction": juris_of.get(s["sourceId"]),
            "currentRecordId": cur["recordId"] if cur else None,
            "readableRecordId": readable["recordId"] if readable else None,
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
    skipped_uncatalogued: set[str] = set()

    for html_path in sorted(DIST.rglob("*.html")):
        route = _route_of(html_path)
        if route in SKIP_ROUTES or any(route.startswith(p) for p in SKIP_PREFIXES):
            continue
        # CATALOGUED SOURCES ONLY (Huayin, 2026-08-25). Previously every built page was indexed,
        # which is how `/what-is-a-universe` — a real page, but not a catalogued source — ended up
        # constituting answers. Rendered-site indexing is still the right protection against
        # superseded source files; it simply needs an explicit membership boundary in front of it.
        # 33% of retrieval slots in the first 26-case run came from pages that leave here.
        st_probe = standing.get(route)
        if not st_probe or st_probe.get("layer") in (None, "out", "unruled"):
            skipped_uncatalogued.add(route)
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
                        text=_redact_identifiers(piece),
                        sourceId=st.get("sourceId"),
                        sourceLabel=st.get("sourceLabel"),
                        role=st.get("role"),
                        standing=st.get("standing", "onsite page (not in the source catalog)"),
                        isHistorical=bool(st.get("isHistorical")),
                        isEditionPinned=bool(st.get("isEditionPinned")),
                        currentRecordId=st.get("currentRecordId"),
                        readableRecordId=st.get("readableRecordId"),
                        layer=st.get("layer", "unruled"),
                        jurisdiction=st.get("jurisdiction"),
                        url=f"https://datumwise.ai{route}{frag}",
                    )
                )
    return chunks


def build_deposits(min_chars: int = 220, max_chars: int = 2600) -> list[Chunk]:
    """Chunk the EXACT deposited text of Core works that have no onsite route.

    Thirteen of the sixteen Core works are deposit-only. Without this, Ask's default
    corpus would be almost entirely unquotable while the reference layer stayed fully readable —
    and the ruling named that hazard precisely: it would push Ask back toward whatever is easiest
    to retrieve.

    Cited by DOI rather than by route, because there is no onsite page to send a reader to. The
    DOI is resolved at request time from the registry (retrieve.py), never stored here.
    """
    manifest_path = DEPOSITS / "manifest.json"
    if not manifest_path.exists():
        print("  (no deposit manifest — run `python3 -m ask.ingest_deposits`)")
        return []
    manifest = json.loads(manifest_path.read_text())
    works = {w["workId"]: w for w in json.loads(WORKS_JSON.read_text())}
    records = json.loads(RECORDS_JSON.read_text())
    cat = json.loads(SOURCES_JSON.read_text())
    sources = {s["sourceId"]: s for s in (cat["sources"] if isinstance(cat, dict) else cat)}
    layer_of, juris_of = _membership()

    out: list[Chunk] = []
    for d in manifest["deposits"]:
        text = (DEPOSITS / d["file"]).read_text(encoding="utf-8", errors="replace")
        src = sources[d["sourceId"]]
        # A DEPOSIT'S RECORD IS NOT AUTOMATICALLY THE CURRENT ONE (2026-08-26).
        #
        # This used to write `currentRecordId=d["recordId"]` — the record whose text this is — and a
        # standing sentence that opened with "{CURRENT}". That was correct only for as long as no
        # deposited work was ever superseded, and it failed silently the moment one was: Analytical
        # Governance v1.1's 27 chunks would have gone on introducing themselves as "current record
        # v1.1" while v2.0 held the current record, with v1.1's text underneath. The label would
        # have become false and nothing anywhere would have raised.
        #
        # The routed path has always done this correctly — `pinned = readable != current` in
        # _load_standing. Deposits simply never asked the question. They ask it now, the same way.
        cur = _current_record_for(records, d["workId"])
        cur_id = cur["recordId"] if cur else None
        readable_is_current = bool(cur) and cur["recordId"] == d["recordId"]
        preserved = src.get("preservedState")
        is_hist = bool(preserved) or not readable_is_current
        is_pinned = not readable_is_current and not preserved

        bits = []
        if readable_is_current:
            bits.append("{CURRENT}")
        else:
            # The numbers stay out of chunks.json — {READABLE} and {CURRENT} are both spliced from
            # the registry at request time, so a later ruling moves this sentence without a rebuild.
            bits.append("PRESERVED HISTORICAL STATE" + (f" as of {preserved}" if preserved else "")
                        + " — this is the deposited text of {READABLE}, which is NOT the current "
                          "record; the current record is {CURRENT_BARE}. It may not establish "
                          "datumwise's current position")
        bits.append("deposited text — read from the deposited record, not from a page on this site")
        dep_standing = "; ".join(bits)
        label = (src.get("title") if not readable_is_current and src.get("title")
                 else works[d["workId"]]["canonicalLabel"])
        role = src.get("role")
        # Split on markdown headings; the heading becomes the section name, as with built HTML.
        parts: list[tuple[str, str]] = []
        heading, buf = "", []
        for line in text.splitlines():
            m = re.match(r"^(#{1,3})\s+(.*)$", line)
            if m:
                if buf:
                    parts.append((heading, "\n".join(buf)))
                heading, buf = re.sub(r"[*_`]", "", m.group(2)).strip(), []
            else:
                buf.append(line)
        if buf:
            parts.append((heading, "\n".join(buf)))

        for heading, body in parts:
            body = _redact_identifiers(re.sub(r"\s+", " ", body).strip())
            if len(body) < min_chars:
                continue
            pieces = [body]
            if len(body) > max_chars:
                pieces, cur = [], ""
                for sent in re.split(r"(?<=[.!?])\s+", body):
                    if len(cur) + len(sent) > max_chars and cur:
                        pieces.append(cur); cur = sent
                    else:
                        cur = (cur + " " + sent).strip()
                if cur:
                    pieces.append(cur)
            for i, piece in enumerate(pieces):
                if len(piece) < min_chars:
                    continue
                out.append(Chunk(
                    chunkId=f"deposit:{d['recordId']}::{heading[:40]}::{i}",
                    route="", anchor="", heading=heading, title=label, text=piece,
                    sourceId=d["sourceId"], sourceLabel=label, role=role,
                    standing=dep_standing,
                    isHistorical=is_hist, isEditionPinned=is_pinned,
                    url="",  # resolved to the DOI link at request time
                    currentRecordId=cur_id, readableRecordId=d["recordId"],
                    layer=layer_of.get(d["sourceId"], "unruled"),
                    jurisdiction=juris_of.get(d["sourceId"]),
                ))
    return out


class SupersededCore(RuntimeError):
    """A Core chunk whose text is not the current record. See check_core_is_current."""


def check_core_is_current(chunks: list[Chunk]) -> None:
    """NO CORE PASSAGE MAY BE A SUPERSEDED EDITION. Failure is a build defect, not a warning.

    Core is the only class entitled to establish "datumwise holds ...", so a Core passage IS the
    current position by construction. If its readable record is not the current record, then either
    the deposit needs refreshing or the source needs re-ruling — and until one of those happens the
    agent would be stating a superseded position as the current one, in the class of source a reader
    is told to trust most.

    This is the guard that would have caught the 2026-08-26 Analytical Governance supersession. AG
    v1.1 was Core and deposit-only; flipping its record to `superseded` without touching Ask would
    have left 27 Core chunks introducing v1.1's text as "current record v1.1". Nothing would have
    raised. The failure was silent precisely because every individual piece was behaving correctly.
    """
    bad = sorted({
        f"{c.sourceId} (reading {c.readableRecordId}, current is {c.currentRecordId})"
        for c in chunks
        if c.layer == "core" and c.currentRecordId and c.readableRecordId != c.currentRecordId
    })
    if bad:
        raise SupersededCore(
            f"{len(bad)} Core source(s) are not the current record: {'; '.join(bad)}. Refresh the "
            "deposit to the current edition, or rule the source out of Core. Do not leave a "
            "superseded edition entitled to establish datumwise's current position."
        )


class CoreUnreachable(RuntimeError):
    """A Core source that produced no retrievable text. See check_core_reachable."""


def check_core_reachable(chunks: list[Chunk]) -> None:
    """EVERY CORE SOURCE MUST BE RETRIEVABLE. Failure is a build defect, not a warning.

    Core is the only class entitled to establish "datumwise holds ...". A Core source that produced
    no chunks is therefore not merely absent from an answer — it silently narrows what datumwise is
    able to say about itself, and nothing downstream can tell the difference between "the Core set
    does not settle this" and "the Core source that settles it failed to index".

    The two legitimate routes in are a governed onsite representation and deposited/supplied source
    material. Thirteen of the sixteen Core works are deposit-only, so the second route is the normal
    one, not the exception — which is exactly why its failure has to be loud.
    """
    ruled = set(json.loads(AUTHORITY_JSON.read_text())["core"]["sourceIds"])
    reachable = {c.sourceId for c in chunks if c.layer == "core" and c.sourceId}
    missing = sorted(ruled - reachable)
    if missing:
        raise CoreUnreachable(
            f"{len(missing)} Core source(s) produced no retrievable text: {', '.join(missing)}. "
            "A Core source must be reachable through a governed onsite route or through deposited/"
            "supplied material. Fix the route or ingest the deposit; do not demote it to Reference "
            "to make the build pass."
        )


def main() -> None:
    chunks = build()
    deposits = build_deposits()
    chunks = chunks + deposits
    check_core_reachable(chunks)
    check_core_is_current(chunks)
    out = Path(__file__).resolve().parent.parent / "index" / "chunks.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([asdict(c) for c in chunks], indent=0, ensure_ascii=False))
    routes = sorted({c.route for c in chunks})
    hist = sum(1 for c in chunks if c.isHistorical)
    pinned = sum(1 for c in chunks if c.isEditionPinned)
    catalogued = sum(1 for c in chunks if c.sourceId)
    print(f"index built: {len(chunks)} chunks across {len(routes)} routes -> {out}")
    core_n = sum(1 for c in chunks if c.layer == "core")
    ref = sum(1 for c in chunks if c.layer == "reference")
    print(f"  catalogued {catalogued} | historical {hist} | edition-pinned {pinned}")
    print(f"  LAYERS: core {core_n} | reference {ref}")
    print("  NOTE: the index moved. Run `python3 -m ask.cache_purge` against the live database — a\n"
          "        cached answer is a promise that asking again gives the same thing, and this\n"
          "        rebuild has just voided it.")
    print(f"  from deposited text: {len(deposits)} chunks "
          f"({len({c.sourceId for c in deposits})} works)")


if __name__ == "__main__":
    main()
