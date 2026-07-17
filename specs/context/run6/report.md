########## ARM control — KP v0.3 (k=2) ##########
EVAL RUN run6-control  ·  2026-07-16T20:46:41
provider=anthropic  model=claude-opus-4-8@claude-opus-4-8  sampling={'max_tokens': 2048, 'temperature': 'provider-default'}  harness={'aperture_cap': 1000, 'loop_iteration_budget': 5, 'replicates_k': 2}
kp=v0.3  benchmark_list=v1  scorer=v0.4

SUMMARY   passed 7/22   ◆-explicitness 10/12   mean convergence (converged-only) 1.0   censored 15   loop-violations 0
──────────────────────────────────────────────────────────────────────────
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'inventory')]; checklist flooded (6 items > max 2)
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'inventory')]; checklist flooded (4 items > max 2)
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✗   conv 1
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)  retries 4
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)  retries 4
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B6 ○   FAIL   closure✓ grade✗ explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: a proposal carries the wrong INFERRED_* grade; checklist flooded (2 items > max 1)
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (3 items > max 1)
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (4 items > max 1)
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 4
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (4 items > max 1)
B8 ○   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)
       └ narrative: CONTRACT/HARNESS: JSONDecodeError: Expecting value: line 1 column 1 (char 0)
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]; checklist flooded (7 items > max 2)
B9 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B9 ○   FAIL   closure✓ grade✗ explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: a proposal carries the wrong INFERRED_* grade; checklist flooded (5 items > max 2)
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'catalog')]; checklist flooded (3 items > max 2)
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('universe', 'catalog'), ('universe', 'budget')]; checklist flooded (4 items > max 2)
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]; checklist flooded (3 items > max 2)
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]
──────────────────────────────────────────────────────────────────────────
CONVERGENCE COST   per-benchmark iters above; converged-only mean + censoring in SUMMARY.
◆-CALL RECORD      each ◆ benchmark's `explicit` flag above is its surfaced/silent record.

########## ARM treatment — KP v0.4 (k=2) ##########
EVAL RUN run6-treatment  ·  2026-07-16T20:46:41
provider=anthropic  model=claude-opus-4-8@claude-opus-4-8  sampling={'max_tokens': 2048, 'temperature': 'provider-default'}  harness={'aperture_cap': 1000, 'loop_iteration_budget': 5, 'replicates_k': 2}
kp=v0.4  benchmark_list=v1  scorer=v0.4

SUMMARY   passed 6/22   ◆-explicitness 8/12   mean convergence (converged-only) 1.2   censored 16   loop-violations 2
──────────────────────────────────────────────────────────────────────────
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 3 (CAPPED)  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'orders'), ('universe', 'inventory')]; checklist flooded (4 items > max 2); loop_violation: revise re-proposed a struck declaration 'level store keyed by store_id' — a settled mark stays settled unless the human reopens it
B1 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('universe', 'orders'), ('universe', 'inventory')]; silent on oracle-asymmetric call(s): ['basis']
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']
B4 ◆   FAIL   closure✓ graden/a explicit✗ concise✗   conv 5 (CAPPED)
       └ narrative: silent on oracle-asymmetric call(s): ['m-leak']
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (2 items > max 1)
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (2 items > max 1)
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]
B9 ○   FAIL   closure✓ grade✗ explicit✓ concise✓   conv 5 (CAPPED)  retries 3
       └ narrative: a proposal carries the wrong INFERRED_* grade
B9 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 2
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'catalog')]; checklist flooded (4 items > max 2)
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 3 (CAPPED)  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'catalog'), ('universe', 'budget')]; checklist flooded (4 items > max 2); loop_violation: revise re-proposed a struck declaration 'edge budget.store_id -> store.store_id' — a settled mark stays settled unless the human reopens it
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]
──────────────────────────────────────────────────────────────────────────
CONVERGENCE COST   per-benchmark iters above; converged-only mean + censoring in SUMMARY.
◆-CALL RECORD      each ◆ benchmark's `explicit` flag above is its surfaced/silent record.

====================================================================================
A/B RATES — CONTROL control vs TREATMENT treatment  (k=2, scorer v0.4)
====================================================================================
bench  kind pass          explicit(◆)     flood         loopviol     
B1     ◆    0.00→0.00     1.00→0.50  △    1.00→1.00     0.00→0.50  △ 
B2     ◆    1.00→1.00     1.00→1.00       0.50→0.00  △  0.00→0.00    
B3     ◆    0.00→0.00     0.00→0.00       1.00→1.00     0.00→0.00    
B4     ◆    1.00→0.50  △  1.00→0.50  △    0.00→0.50  △  0.00→0.00    
B5     ○    1.00→1.00     -→-             0.00→0.00     0.00→0.00    
B6     ○    0.00→0.00     -→-             1.00→0.50  △  0.00→0.00    
B7     ○    0.00→0.00     -→-             1.00→0.50  △  0.00→0.00    
B8     ○    0.00→0.00     -→-             1.00→0.00  △  0.00→0.00    
B9     ○    0.50→0.50     -→-             0.50→0.00  △  0.00→0.00    
B10    ◆    0.00→0.00     1.00→1.00       1.00→1.00     0.00→0.50  △ 
B11    ◆    0.00→0.00     1.00→1.00       0.50→0.00  △  0.00→0.00    
------------------------------------------------------------------------------------
CONTROL control:   passed(mean) 3.5  ◆-explicit(mean) 5.0  flood(mean) 7.5  loop-viol(total) 0
TREATMENT treatment: passed(mean) 3.0  ◆-explicit(mean) 4.0  flood(mean) 4.5  loop-viol(total) 2

READING (ruling 4): refutation (B11) is the most at-risk ◆ under the strict prune — if its explicit_rate falls, the gate is too aggressive (prediction-2 do-not-ship). Concentration bought with recall is not a win.
