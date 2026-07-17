########## ARM control — KP v0.3 (k=3) ##########
EVAL RUN run7-control  ·  2026-07-17T00:46:05
provider=anthropic  model=claude-opus-4-8@claude-opus-4-8  sampling={'max_tokens': 2048, 'temperature': 'provider-default'}  harness={'aperture_cap': 1000, 'loop_iteration_budget': 5, 'replicates_k': 3}
kp=v0.3  benchmark_list=v1  scorer=v0.4

SUMMARY   passed 11/33   ◆-explicitness 15/18   mean convergence (converged-only) 1.0   censored 22   loop-violations 2
──────────────────────────────────────────────────────────────────────────
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('universe', 'orders'), ('universe', 'inventory')]; checklist flooded (3 items > max 2)
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'orders'), ('universe', 'inventory')]; checklist flooded (8 items > max 2)
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'inventory')]; checklist flooded (3 items > max 2)
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 3 (CAPPED)  retries 2  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']; loop_violation: revise re-proposed a struck declaration 'count of returns / count of transactions, per store' — a settled mark stays settled unless the human reopens it
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)
       └ narrative: CONTRACT/HARNESS: ValueError: malformed target 'store->region' for kind 'hierarchy' — use a bare canonical name (edge/relate as 'frm->to'), not a description
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)
       └ narrative: CONTRACT/HARNESS: JSONDecodeError: Expecting value: line 1 column 1 (char 0)
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (2 items > max 1)
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (3 items > max 1)
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 4
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (3 items > max 1)
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (3 items > max 1)
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (3 items > max 1)
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]; checklist flooded (3 items > max 2)
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]; checklist flooded (3 items > max 2)
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]; checklist flooded (5 items > max 2)
B9 ○   FAIL   closure✓ grade✗ explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: a proposal carries the wrong INFERRED_* grade; checklist flooded (3 items > max 2)
B9 ○   FAIL   closure✓ grade✗ explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: a proposal carries the wrong INFERRED_* grade; checklist flooded (3 items > max 2)
B9 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('universe', 'budget')]; checklist flooded (5 items > max 2)
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 2 (CAPPED)  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'budget')]; checklist flooded (4 items > max 2); loop_violation: revise re-proposed a struck declaration 'measure target from budget.target, additive across store and day' — a settled mark stays settled unless the human reopens it
B10 ◆   PASS   closure✓ graden/a explicit✓ concise✗   conv 1
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 4
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 3
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]; checklist flooded (6 items > max 2)
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 4
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]
──────────────────────────────────────────────────────────────────────────
CONVERGENCE COST   per-benchmark iters above; converged-only mean + censoring in SUMMARY.
◆-CALL RECORD      each ◆ benchmark's `explicit` flag above is its surfaced/silent record.

########## ARM treatment — KP v0.5 (k=3) ##########
EVAL RUN run7-treatment  ·  2026-07-17T00:46:05
provider=anthropic  model=claude-opus-4-8@claude-opus-4-8  sampling={'max_tokens': 2048, 'temperature': 'provider-default'}  harness={'aperture_cap': 1000, 'loop_iteration_budget': 5, 'replicates_k': 3}
kp=v0.5  benchmark_list=v1  scorer=v0.4

SUMMARY   passed 10/33   ◆-explicitness 15/18   mean convergence (converged-only) 1.1   censored 23   loop-violations 4
──────────────────────────────────────────────────────────────────────────
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 2 (CAPPED)  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'orders'), ('universe', 'inventory')]; checklist flooded (3 items > max 2); loop_violation: revise re-proposed a struck declaration 'amount from orders, summable at order grain' — a settled mark stays settled unless the human reopens it
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 3 (CAPPED)  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'orders'), ('universe', 'inventory')]; checklist flooded (3 items > max 2); loop_violation: revise re-proposed a struck declaration 'inventory_level = daily_inventory.level, grain (store_id, day)' — a settled mark stays settled unless the human reopens it
B1 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'orders'), ('universe', 'inventory')]; checklist flooded (8 items > max 2)
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B2 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']
B3 ◆   FAIL   closure✗ graden/a explicit✗ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('universe', 'returns')]; silent on oracle-asymmetric call(s): ['universe']
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B4 ◆   PASS   closure✓ graden/a explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B5 ○   PASS   closure✓ grade✓ explicit✓ concise✓   conv 1
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B6 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]; checklist flooded (3 items > max 1)
B7 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('edge', 'day->month')]
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]; checklist flooded (3 items > max 2)
B8 ○   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('measure', 'revenue'), ('measure', 'orders'), ('derived', 'aov')]
B9 ○   FAIL   closure✓ grade✗ explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: a proposal carries the wrong INFERRED_* grade
B9 ○   FAIL   closure✓ grade✗ explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: a proposal carries the wrong INFERRED_* grade
B9 ○   FAIL   closure✓ grade✗ explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: a proposal carries the wrong INFERRED_* grade
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 2 (CAPPED)  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'budget')]; loop_violation: revise re-proposed a struck declaration 'measure target = sum(budget.target) grain(store_id, day)' — a settled mark stays settled unless the human reopens it
B10 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 2 (CAPPED)  LOOP-VIOLATION
       └ narrative: missing/mismatched closures (normal form): [('universe', 'budget')]; loop_violation: revise re-proposed a struck declaration 'level store key store_id' — a settled mark stays settled unless the human reopens it
B10 ◆   PASS   closure✓ graden/a explicit✓ concise✗   conv 2
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✗   conv 5 (CAPPED)  retries 2
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]; checklist flooded (5 items > max 2)
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]
B11 ◆   FAIL   closure✗ graden/a explicit✓ concise✓   conv 5 (CAPPED)  retries 1
       └ narrative: missing/mismatched closures (normal form): [('relate', 'store->region')]
──────────────────────────────────────────────────────────────────────────
CONVERGENCE COST   per-benchmark iters above; converged-only mean + censoring in SUMMARY.
◆-CALL RECORD      each ◆ benchmark's `explicit` flag above is its surfaced/silent record.

====================================================================================
A/B RATES — CONTROL control vs TREATMENT treatment  (k=3, scorer v0.4)
====================================================================================
bench  kind pass          explicit(◆)     flood         loopviol     
B1     ◆    0.00→0.00     1.00→1.00       1.00→1.00     0.00→0.67  △ 
B2     ◆    1.00→1.00     1.00→1.00       0.00→0.00     0.00→0.00    
B3     ◆    0.00→0.00     0.00→0.00       1.00→1.00     0.33→0.00  △ 
B4     ◆    1.00→1.00     1.00→1.00       0.00→0.00     0.00→0.00    
B5     ○    1.00→1.00     -→-             0.00→0.00     0.00→0.00    
B6     ○    0.00→0.00     -→-             0.67→0.00  △  0.00→0.00    
B7     ○    0.00→0.00     -→-             1.00→0.33  △  0.00→0.00    
B8     ○    0.00→0.00     -→-             1.00→0.33  △  0.00→0.00    
B9     ○    0.33→0.00  △  -→-             0.67→0.00  △  0.00→0.00    
B10    ◆    0.33→0.33     1.00→1.00       1.00→0.33  △  0.33→0.67  △ 
B11    ◆    0.00→0.00     1.00→1.00       0.33→0.33     0.00→0.00    
------------------------------------------------------------------------------------
CONTROL control:   passed(mean) 3.67  ◆-explicit(mean) 5.0  flood(mean) 6.67  loop-viol(total) 2
TREATMENT treatment: passed(mean) 3.33  ◆-explicit(mean) 5.0  flood(mean) 3.33  loop-viol(total) 4

READING (ruling 4): refutation (B11) is the most at-risk ◆ under the strict prune — if its explicit_rate falls, the gate is too aggressive (prediction-2 do-not-ship). Concentration bought with recall is not a win.
