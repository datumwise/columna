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


# =================================================================================================
# R4-C0-S1 — THE ORDERED WALK (Frame-QL 1.0 §9.8/§9.19; ToD v7.1 §9.4; acceptance case E07)
# =================================================================================================
# R4-C0 above withholds the unplaced row at FRAME ASSEMBLY. Everything above this line is true of a
# frame that was never ordered. A SCAN is ordered, and it runs FIRST — inside each column's _eval,
# before the frame those columns are joined into even exists. So the scan sorted and walked a frame
# that still contained the unplaced row, and polars sorts nulls FIRST: the row with no position in
# the order became point ZERO of its partition. It seeded the cumulative state and it consumed a
# shift step. Its contribution then persisted into every SURVIVING row, all of which were served —
# while the row itself was withheld by the filter above, and the caveat said only that "a row was
# withheld". A reader was told the frame was incomplete. They were not told the numbers they could
# see were wrong.
#
#   SELECT cumsum(revenue.sum) AS c AT {store, day}
#                     BEFORE                 AFTER
#     cumsum    [ 80.0, 100.0, 130.0 ]   [ 10.0, 30.0, 60.0 ]   <- every served row was wrong
#     lag       [ 70.0,  10.0,  20.0 ]   [ None, 10.0, 20.0 ]   <- the walk spent a step on it
#
# This is not an ordering defect — the sort was correct given its input. The input was illegitimate.
# It is a PLACEMENT/CONTAINMENT defect: unestablished placement entering an ordered walk. The
# expected values below are not hand-computed; each is the engine's OWN output on the identical
# manifold with the unplaced record absent.
#
# WHAT THESE PIN, beyond the numbers:
#   · the withholding still happens and is still DISCLOSED — exclusion from the walk must not become
#     a silent drop, which ToD §9.4 forbids in the same breath as the influence it forbids;
#   · `lead`'s immunity is ASSERTED, not inherited. It is clean today only because polars sorts
#     nulls first, so a forward shift never reaches back past them. §9.22: a skip policy "cannot
#     emerge from a dataframe engine's default null behavior". If that default ever flips, this test
#     fails rather than the numbers quietly changing;
#   · the containment is scoped to the ORDER axis. An unplaced PARTITION key already formed its own
#     `.over()` group and never contaminated its siblings; a fix that over-filtered would break a
#     lawful result, which is the same mistake in the other direction as fixing the coarse total.

CML_ORDERED = """
MANIFOLD p VERSION 1
UNIVERSE sales_u = store * day BASIS events
LEVEL store = store_id BASE
LEVEL day   = day BASE
LEVEL month = month
HIERARCHY calendar { day -> month VIA cal(day, month) }
MEASURE revenue ON sales_u FROM sales AS sum(amount) FILL unknown
"""

# the same constitutional shape as ROWS_LOST_PLACEMENT, but every placed record carries a value, so
# any wrong number is the walk's doing and not Φ's.
ORDERED_LOST_PLACEMENT = [("s1", None, 70.0), ("s1", "2024-01-01", 10.0),
                          ("s1", "2024-01-02", 20.0), ("s1", "2024-01-03", 30.0)]
ORDERED_ALL_PLACED = [("s1", "2024-01-01", 10.0), ("s1", "2024-01-02", 20.0),
                      ("s1", "2024-01-03", 30.0)]
# the unplaced value BELOW every placed one, so it would win a running minimum if it were walked.
ORDERED_LOW_UNPLACED = [("s1", None, 5.0), ("s1", "2024-01-01", 10.0),
                        ("s1", "2024-01-02", 20.0), ("s1", "2024-01-03", 30.0)]
# placement lost on the PARTITION key instead of the order key.
ORDERED_LOST_PARTITION = [(None, "2024-01-01", 70.0), ("s1", "2024-01-01", 10.0),
                          ("s1", "2024-01-02", 20.0), ("s1", "2024-01-03", 30.0)]

SCAN_OPS = ("cumsum", "cummax", "cummin", "lag", "lead", "pct_change")


def _ordered_server(rows):
    con = duckdb.connect()
    con.execute("CREATE TABLE cal (day VARCHAR, month VARCHAR)")
    con.executemany("INSERT INTO cal VALUES (?, ?)",
                    [("2024-01-01", "2024-01"), ("2024-01-02", "2024-01"),
                     ("2024-01-03", "2024-01")])
    con.execute("CREATE TABLE sales(store_id VARCHAR, day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO sales VALUES (?, ?, ?)", rows)
    srv = ManifoldServer(parse_manifold(CML_ORDERED), DuckDBConnector(con))
    srv.publish()
    return srv


def _scan(srv, op, anchor="{store, day}"):
    """Run one scan and return its served column, ordered by day so the walk is legible."""
    fr, w = _ask(srv, f"SELECT {op}(revenue.sum) AS c AT {anchor}")
    if fr.data is None:
        return None, fr, w
    return fr.data.sort("day")["c"].to_list(), fr, w


@pytest.fixture
def ordered_lost_placement():
    return _ordered_server(ORDERED_LOST_PLACEMENT)


# ---- 6. the cumulative walk does not consume an unplaced contribution ----------------------------
def test_cumulative_walk_does_not_consume_an_unplaced_contribution(ordered_lost_placement):
    """§9.19: "A contribution whose required placement is unresolved cannot influence the cumulative
    walk and then be made harmless by deleting its output row afterward." It was seeding the total
    at position zero and persisting into all three served rows."""
    got, _fr, _w = _scan(ordered_lost_placement, "cumsum")
    assert got == [10.0, 30.0, 60.0], "the unplaced 70.0 was folded into the running total"


def test_positional_displacement_does_not_spend_a_step_on_an_unplaced_point(ordered_lost_placement):
    """§9.17: displacement "counts over analytical points that exist under the universe law. It does
    not count physical rows." `v.shift(n)` is purely positional, so the unplaced row at position zero
    became the first placed day's predecessor — a day that has no predecessor at all."""
    got, _fr, _w = _scan(ordered_lost_placement, "lag")
    assert got == [None, 10.0, 20.0], "lag stepped over an unplaced point instead of past it"

    got_pct, _fr, _w = _scan(ordered_lost_placement, "pct_change")
    assert got_pct == [None, 1.0, 0.5]


def test_a_running_extremum_is_not_won_by_an_unplaced_value():
    """Both directions, so neither passes by value coincidence: a HIGH unplaced value would win the
    running maximum, a LOW one the running minimum. Each was winning."""
    got_max, _fr, _w = _scan(_ordered_server(ORDERED_LOST_PLACEMENT), "cummax")
    assert got_max == [10.0, 20.0, 30.0], "the unplaced 70.0 won every running maximum"

    got_min, _fr, _w = _scan(_ordered_server(ORDERED_LOW_UNPLACED), "cummin")
    assert got_min == [10.0, 10.0, 10.0], "the unplaced 5.0 won every running minimum"


def test_forward_displacement_immunity_is_asserted_not_inherited(ordered_lost_placement):
    """`lead` is clean — but only because polars sorts nulls FIRST, so a forward shift never reaches
    back past the unplaced row. §9.22: a governed skip policy "cannot emerge from a dataframe
    engine's default null behavior". This pins the RESULT so the guarantee stops living in a default
    we do not own."""
    got, _fr, _w = _scan(ordered_lost_placement, "lead")
    assert got == [20.0, 30.0, None]


# ---- 7. exclusion from the walk is not a silent drop --------------------------------------------
def test_exclusion_from_the_walk_still_withholds_and_still_discloses(ordered_lost_placement):
    """THE ANTI-REGRESSION GUARD FOR THE FIX ITSELF. If the scan simply dropped the unplaced rows,
    R4-C0 would count zero of them, the frame would serve silently, and we would have traded a wrong
    number for a silent omission — which ToD §9.4 forbids in the same breath as the influence. The
    rows are excluded from the WALK and handed back unwalked, so the containment above still fires
    with the same count and the same text."""
    fr, w = _ask(ordered_lost_placement, "SELECT cumsum(revenue.sum) AS c AT {store, day}")
    assert fr.data["day"].null_count() == 0
    assert fr.data.shape[0] == 3
    assert w["outcome"] == "disclose"
    frame_codes = [(d["code"], d["materiality"]) for d in w["frame"]["disclosures"]]
    assert ("incomplete_data", "material") in frame_codes
    note = next(c for c in fr.disclosure.caveats if c.category == DATA_GAP)
    assert "1 row(s) WITHHELD" in note.detail and "day" in note.detail


def test_the_scan_discloses_that_it_did_not_walk_them(ordered_lost_placement):
    """The frame-level caveat says a row was withheld. On its own that is true and insufficient: it
    does not say the row was kept OUT OF THE WALK, which is the fact a reader of an ordered column
    needs. The scan's own existing TRANSPORT caveat now carries it — no new reason code, no new
    wire field, no new vocabulary."""
    _got, _fr, w = _scan(ordered_lost_placement, "cumsum")
    details = " ".join(d.get("detail", "") for d in w["columns"][0]["disclosures"])
    assert "did not enter the walk" in details


# ---- 8. the containment costs no lawful result ---------------------------------------------------
def test_a_fully_placed_ordered_frame_is_untouched():
    """The no-op half of the ruling, across every scan operator Core ships. A frame with nothing
    unplaced must be byte-identical to before: same numbers, `serve`, and not one caveat about
    placement. (Instrumented, the containment branch fired ZERO times across the pre-existing
    1,060-test corpus — the defect had no coverage at all, which is why it shipped.)"""
    srv = _ordered_server(ORDERED_ALL_PLACED)
    expected = {"cumsum": [10.0, 30.0, 60.0], "cummax": [10.0, 20.0, 30.0],
                "cummin": [10.0, 10.0, 10.0], "lag": [None, 10.0, 20.0],
                "lead": [20.0, 30.0, None], "pct_change": [None, 1.0, 0.5]}
    for op in SCAN_OPS:
        got, _fr, w = _scan(srv, op)
        assert got == expected[op], op
        # the FRAME channel is where placement containment speaks, and it must be silent here.
        # (The column channel is not: `lag`/`lead`/`pct_change` leave a boundary NULL on ANY frame —
        # the first point has no predecessor — and Φ discloses that as `unknown`. That is
        # pre-existing, correct, and nothing to do with placement; asserting `serve` across all six
        # would have pinned an unrelated Φ behaviour into this file.)
        assert w["frame"]["disclosures"] == [], op
        details = " ".join(d.get("detail", "") for d in w["columns"][0]["disclosures"])
        assert "did not enter the walk" not in details, op
    for op in ("cumsum", "cummax", "cummin"):
        assert _scan(srv, op)[2]["outcome"] == "serve", op


def test_an_unplaced_partition_key_does_not_contaminate_its_siblings():
    """Placement lost on the PARTITION key, not the order key. That row already formed its own
    `.over()` group and never touched s1's walk — so the numbers here were RIGHT before the fix, and
    the fix must keep them right. A containment that over-filtered would cost a lawful result, which
    is the same mistake as a containment that "fixed" the coarse total."""
    got, _fr, _w = _scan(_ordered_server(ORDERED_LOST_PARTITION), "cumsum")
    assert got == [10.0, 30.0, 60.0]


def test_the_coarse_ordered_frame_is_unharmed(ordered_lost_placement):
    """`AT {month}` does not require `day`, so nothing is withheld and nothing is excluded: the
    lawful coarse result still accounts for every record whose placement THAT anchor needs."""
    fr, w = _ask(ordered_lost_placement, "SELECT cumsum(revenue.sum) AS c AT {month}")
    assert fr.data["c"].to_list() == [60.0]
    assert w["outcome"] == "serve"
