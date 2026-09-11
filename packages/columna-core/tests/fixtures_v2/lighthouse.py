"""
`lighthouse` — the publication-v2 conformance fixture.

DELIBERATELY NOT `firstlight`. `firstlight`'s v2 successor cannot be authored by a machine: its
target specifications, contribution structure, participation and movement law are unresolved
analytical facts requiring authoritative establishment (see `governed.migrate` and the migration
report). Inventing them to get an end-to-end demo would be the exact error the model exists to
prevent — a realization-shaped guess standing in for governed law.

So `lighthouse` is a synthetic world whose law IS established, by this fixture's author, explicitly.
Its job is to prove the machinery: that established law compiles, that the Core family comes from
law rather than from the mapping, and that every check refuses when it should.

Six rows, one per (store, day) — so the grain claim `coincident` is TRUE here and is checked rather
than assumed. Non-monotonic and asymmetric across stores, so a rolled-up answer differs from any
leaf and `min`/`max` cannot coincide with `first`/`last`.
"""
from __future__ import annotations

ROWS = [
    ("s1", "2026-08-01", 10.0),
    ("s1", "2026-08-02", 3.0),
    ("s1", "2026-08-03", 7.0),
    ("s2", "2026-08-01", 5.0),
    ("s2", "2026-08-02", 40.0),
    ("s2", "2026-08-03", 20.0),
]

MANIFOLD_ID, VERSION = "lighthouse", "1.0.0"


def _cite(law):
    return {"vocabulary": "datumwise.foundation", "version": "1", "law": law}


def publication() -> dict:
    """A v2 governed publication in which every identity-bearing responsibility is established.

    Note what is NOT established and is published as such: domain and movement. Nothing here
    declares a hierarchy, so nothing may travel, and the artifact says `unestablished` rather than
    implying additivity. That is the ruling — absence of prohibition is never permission — and it is
    visible in the resolved view rather than inferred from a missing record."""
    return {
        "publication_format_version": "2",
        "ref": {"manifold_id": MANIFOLD_ID, "version": VERSION},
        "logical": {"declarations": [
            {"kind": "anchor", "name": "sale_at", "body": {
                "components": [{"name": "store", "type": "text"},
                               {"name": "day", "type": "date"}]}},
            {"kind": "universe", "name": "sales", "body": {"basis": "events", "anchor": "sale_at"}},

            # The PRIMITIVE family. Its continuation is DECLARED, because "does this quantity
            # compose across refinement?" is an analytical choice and no formation law entails one.
            {"kind": "family", "name": "revenue", "body": {
                "family_id": "lh-revenue",
                "canonical_reference": "revenue",
                "universe": "sales",
                "constitutive_anchor": "sale_at",
                "target": "the revenue recognised at one sale point, in currency units",
                "formation": {"kind": "primitive", "contribution_structure": "coincident"},
                "participation": "every sale point carrying a recorded amount",
                "value_domain": "decimal",
                "continuation": _cite("SUM")}},

            # CONSTRUCTED families. Their continuation is ENTAILED and is not declared; their result
            # domains are entailed; their empty-fiber behaviour is entailed. Only the TARGET is
            # declared — because §11.5.1 makes COUNT the proof that a law cannot supply one.
            {"kind": "family", "name": "revenue_observations", "body": {
                "family_id": "lh-revcount",
                "canonical_reference": "count(revenue@sale_at)",
                "aliases": ["revenue_observations"],
                "universe": "sales",
                "constitutive_anchor": "sale_at",
                "target": ("count(x@I) — the number of SUPPORTED revenue observations, not the "
                           "number of participating sale points. §11.5.1 calls these distinct "
                           "targets; this family asserts the former"),
                "formation": {"kind": "construction", "law": _cite("COUNT"),
                              "operands": ["lh-revenue"]},
                "participation": "every sale point carrying a recorded amount"}},
            {"kind": "family", "name": "revenue_least", "body": {
                "family_id": "lh-revmin",
                "canonical_reference": "min(revenue@sale_at)",
                "universe": "sales",
                "constitutive_anchor": "sale_at",
                "target": "the least revenue value under the decimal value order",
                "formation": {"kind": "construction", "law": _cite("MIN"),
                              "operands": ["lh-revenue"]},
                "participation": "every sale point carrying a recorded amount"}},
            {"kind": "family", "name": "revenue_greatest", "body": {
                "family_id": "lh-revmax",
                "canonical_reference": "max(revenue@sale_at)",
                "universe": "sales",
                "constitutive_anchor": "sale_at",
                "target": "the greatest revenue value under the decimal value order",
                "formation": {"kind": "construction", "law": _cite("MAX"),
                              "operands": ["lh-revenue"]},
                "participation": "every sale point carrying a recorded amount"}},
        ]},
        "authority": {
            "published_by": "lighthouse fixture",
            "published_at": "2026-09-11T00:00:00Z",
            "ratifications": {},
            # Authority over each family's identity-bearing constitution. A DISTINCT record type
            # from the universe's `elf-1` existence-law ratification: the two attest different
            # objects, and one type would let a currency check compare incomparable fingerprints.
            "family_constitution": {
                fid: {"established_by": "lighthouse fixture",
                      "at": "2026-09-11T00:00:00Z",
                      "constitution_fingerprint": fp,
                      "fingerprint_scheme": "sigma-f-1"}
                for fid, fp in (("lh-revenue", "0" * 8), ("lh-revcount", "1" * 8),
                                ("lh-revmin", "2" * 8), ("lh-revmax", "3" * 8))},
        },
    }


def mapping(table: str = "sales_lines", connection: str = "warehouse",
            schema: str = "main") -> dict:
    """The private realization. Claims only — every field here is checked against governed law.

    `root_evaluator` does not appear, and cannot: the family a realization serves is named by
    `family_id`, and which law makes that family what it is lives in the publication."""
    def ep(column):
        return {"connection": connection, "schema": schema, "table": table, "column": column}
    return {
        "mapping_format_version": "2",
        "publication_ref": {"manifold_id": MANIFOLD_ID, "version": VERSION},
        "realizations": [
            {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "store",
             "endpoint": ep("store_id")},
            {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "day",
             "endpoint": ep("sale_date")},
            {"kind": "family", "family_id": "lh-revenue", "endpoint": ep("amount"),
             "grain": "coincident", "continuation_operator": "sum", "exactness": "exact"},
            {"kind": "family", "family_id": "lh-revcount", "endpoint": ep("amount"),
             "grain": "coincident", "formation_operator": "count", "exactness": "exact"},
            {"kind": "family", "family_id": "lh-revmin", "endpoint": ep("amount"),
             "grain": "coincident", "formation_operator": "min", "exactness": "exact"},
            {"kind": "family", "family_id": "lh-revmax", "endpoint": ep("amount"),
             "grain": "coincident", "formation_operator": "max", "exactness": "exact"},
        ],
    }
