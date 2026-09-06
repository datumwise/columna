"""R4-C0 — an unresolved anchor coordinate does not establish an analytical point.

THE CONSTITUTIONAL CASE (Huayin, 2026-09-06; reproduced in the M2 reconnaissance §2.2 before any
code was written). A transaction is known to exist. Its Revenue value survives. Its `day` placement
does not.

    AT {store}        the exact total may remain establishable
    AT {store, day}   `day=None` must NOT be served as an ordinary established day

WHAT WAS WRONG. `deliver_measure`'s physical `GROUP BY day` emitted the lost-`day` record as its own
NULL-key group, and the planner joined, sorted and served it as an ordinary row carrying real money:

    store  day         revenue
    s1     null        70.0      <- served, no disclosure of ANY kind
    s1     2024-01-01  10.0
    s1     2024-01-02  20.0
    s1     2024-01-03  null      <- value loss WAS disclosed (unknown_absence)

Value loss was disclosed; placement loss was not. The frame invented a coordinate. That is a false
analytical claim, not merely semantic debt — the daily frame asserted a day-placed 70.0 that no
evidence places on any day.

WHAT THIS PINS, and why each one exists:
  · the coarse frame is UNHARMED — 100.0, all four records, no caveat. The containment must not cost
    a lawful result that does not depend on the lost placement, so it is scoped to the anchor that
    actually claims the unresolved coordinate. A containment that "fixed" the total would be a worse
    defect than the one it replaced;
  · the finer frame does not serve the NULL coordinate as an ordinary point — CLOSED BY DEFAULT. The
    only two available acts are serve and withhold; serving is the false claim;
  · the withholding is DISCLOSED, MATERIAL, at frame level, so a caller cannot mistake the frame for
    a complete account. A silent drop trades a fabricated coordinate for a silent omission and is not
    a repair;
  · Φ still runs and still speaks: value loss keeps its own `unknown` disclosure. The containment
    withholds an unplaced ROW; it does not touch absence semantics, and the two channels must remain
    separately legible;
  · a frame with no unresolved coordinate is BYTE-IDENTICAL to before — no caveat, no dropped row,
    outcome unchanged. The containment is a no-op everywhere the defect is absent (as it was across
    the whole existing 1,052-test corpus, which never once exercised a NULL anchor key);
  · the disclosure uses only the EXISTING closed vocabulary — `data_gap`/`incomplete_data`, MATERIAL,
    on the existing frame channel. This mission was scoped not to invent a reason code, a standing
    enum or a wire field, and the pin records that it did not.

NOT DONE HERE, deliberately: the full R4 existence / placement / eligibility / support architecture.
There is still no per-point placement standing in this engine and this file must not be read as
claiming one. The withheld row is not represented anywhere as "a point whose placement is
unsupported" — it is simply not served, and the frame says so in aggregate. That is the containment,
and the honest limit of it.
"""
import duckdb
import pytest

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.disclosure import DATA_GAP
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.parser import parse_manifold

CML = """
MANIFOLD p VERSION 1
UNIVERSE sales_u = store * day BASIS events
LEVEL store = store_id BASE
LEVEL day   = day BASE
MEASURE revenue ON sales_u FROM sales AS sum(amount) FILL unknown
"""

# one record's PLACEMENT is lost (day NULL, amount survives); one record's VALUE is lost
# (day survives, amount NULL). The two failures must stay separately legible.
ROWS_LOST_PLACEMENT = """
 ('s1', NULL,              70.0),
 ('s1', DATE '2024-01-01', 10.0),
 ('s1', DATE '2024-01-02', 20.0),
 ('s1', DATE '2024-01-03', NULL)
"""
ROWS_ALL_PLACED = """
 ('s1', DATE '2024-01-01', 10.0),
 ('s1', DATE '2024-01-02', 20.0),
 ('s1', DATE '2024-01-03', 70.0)
"""


def _server(rows):
    con = duckdb.connect()
    con.execute("CREATE TABLE sales(store_id VARCHAR, day DATE, amount DOUBLE)")
    con.execute("INSERT INTO sales VALUES " + rows)
    srv = ManifoldServer(parse_manifold(CML), DuckDBConnector(con))
    srv.publish()
    return srv


def _ask(srv, q):
    fr = srv.planner.run_statement(parse_statement(q))
    return fr, wire_frame(fr)


@pytest.fixture
def lost_placement():
    return _server(ROWS_LOST_PLACEMENT)


# ---- 1. the coarse result survives, exactly ------------------------------------------------------
def test_coarse_total_survives_placement_loss(lost_placement):
    """AT {store} does not require `day`, so the lost placement costs it nothing: 100.0, all four
    records, and NOT ONE caveat. This is the half of the ruling that a careless containment breaks."""
    fr, w = _ask(lost_placement, "SELECT revenue AS revenue AT {store}")
    assert fr.data.shape == (1, 2)
    assert fr.data["revenue"][0] == 100.0            # 70 + 10 + 20 + (unrecorded)
    assert w["outcome"] == "serve"
    assert w["frame"]["disclosures"] == []
    assert w["columns"][0]["disclosures"] == []


# ---- 2. the unsupported finer placement cannot serve as ordinary --------------------------------
def test_unresolved_day_is_not_served_as_an_ordinary_point(lost_placement):
    """AT {store, day} must not present `day=None` as an established day. Closed by default."""
    fr, _ = _ask(lost_placement, "SELECT revenue AS revenue AT {store, day}")
    assert fr.data["day"].null_count() == 0, "a NULL anchor coordinate was served as an ordinary point"
    assert fr.data.shape[0] == 3
    assert set(str(d) for d in fr.data["day"]) == {"2024-01-01", "2024-01-02", "2024-01-03"}
    # and the money that could not be placed is not silently redistributed onto a day that IS placed
    assert fr.data["revenue"].to_list() == [10.0, 20.0, None]


def test_the_withholding_is_disclosed_material_at_frame_level(lost_placement):
    """A silent drop would trade a fabricated coordinate for a silent omission. The frame says so."""
    fr, w = _ask(lost_placement, "SELECT revenue AS revenue AT {store, day}")
    frame_codes = [(d["code"], d["materiality"]) for d in w["frame"]["disclosures"]]
    assert ("incomplete_data", "material") in frame_codes
    assert w["outcome"] == "disclose"
    assert w["frame"]["rollup_severity"] == "critical"
    note = next(c for c in fr.disclosure.caveats if c.category == DATA_GAP)
    assert "WITHHELD" in note.detail and "day" in note.detail


def test_value_loss_keeps_its_own_disclosure(lost_placement):
    """Φ is untouched: the record whose VALUE was lost is still disclosed as `unknown`, separately
    from the record whose PLACEMENT was lost. One containment, not a reinterpretation of absence."""
    _, w = _ask(lost_placement, "SELECT revenue AS revenue AT {store, day}")
    assert [d["code"] for d in w["columns"][0]["disclosures"]] == ["unknown"]


# ---- 3. no-op where the defect is absent ---------------------------------------------------------
def test_fully_placed_frame_is_untouched():
    """Same shape of question, same money, every coordinate resolved: nothing withheld, nothing said."""
    fr, w = _ask(_server(ROWS_ALL_PLACED), "SELECT revenue AS revenue AT {store, day}")
    assert fr.data.shape == (3, 3)
    assert fr.data["revenue"].to_list() == [10.0, 20.0, 70.0]
    assert w["outcome"] == "serve"
    assert w["frame"]["disclosures"] == []


# ---- 4. the vocabulary stop-gate held ------------------------------------------------------------
def test_containment_introduces_no_new_wire_vocabulary(lost_placement):
    """The mission forbade inventing a reason code, standing enum or wire field. The disclosure this
    containment emits must therefore already be in the normative table, and already be wired."""
    from columna_core.disclosure_wire import CATEGORY_TABLE

    _, w = _ask(lost_placement, "SELECT revenue AS revenue AT {store, day}")
    known = {code for code, _ in CATEGORY_TABLE.values()}
    for d in w["frame"]["disclosures"]:
        assert d["code"] in known, f"{d['code']} is not in the normative CATEGORY_TABLE"
        assert d["category"] in CATEGORY_TABLE
    assert set(w["frame"].keys()) == {"anchor", "universe", "rollup_severity", "disclosures", "mechanical"}


# ---- 5. the expression path: contained, with a residue that is NOT this mission's to repair -------
# An expression aligns its operands on the anchor, and Polars does not join NULL to NULL — so a single
# unplaced carrier record becomes TWO one-sided coordinates in the alignment, each of which the
# divergence machinery reports as a support gap. Containment removes both rows, which is the point.
#
# THE RESIDUE, recorded here deliberately rather than quietly repaired: those upstream divergence
# caveats are produced inside the alignment layer (`_apply`), before frame assembly can see them, and
# their detail text ends "...these coordinates are IN the frame and carry no value" — a sentence that
# was true before the containment and is not true after it. It is a stale claim in a caveat, not a
# false number, and repairing it means editing the expression-alignment layer, which the R4-C0 scope
# does not authorize. Pinned so it is visible and cannot be discovered twice.
def test_expression_over_an_unplaced_record_is_contained_too():
    srv = _server(ROWS_LOST_PLACEMENT)
    fr, w = _ask(srv, "SELECT revenue / revenue AS ratio AT {store, day}")
    assert fr.data["day"].null_count() == 0
    assert ("incomplete_data", "material") in [(d["code"], d["materiality"]) for d in w["frame"]["disclosures"]]
    assert w["outcome"] == "disclose"


def test_all_records_unplaced_serves_an_empty_frame_not_a_silent_one():
    """The degenerate case: nothing is establishable at this anchor. An empty frame is the honest
    answer, but it must not read as `serve` — an empty frame and an empty frame WITH withheld
    evidence are different claims, and only the disclosure distinguishes them."""
    srv = _server(" ('s1', NULL, 70.0), ('s1', NULL, 30.0) ")
    fr, w = _ask(srv, "SELECT revenue AS revenue AT {store, day}")
    assert fr.data.height == 0
    assert w["outcome"] == "disclose"
    assert ("incomplete_data", "material") in [(d["code"], d["materiality"]) for d in w["frame"]["disclosures"]]
