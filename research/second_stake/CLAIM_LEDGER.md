# Claim ledger: second_stake

`AuthorityEffect: None`.  One evidence class per row.  Receipt keys refer to
`receipts/stake.json`; node histories live in the hash-bound full receipt.

| id | statement | class | evidence | falsifier | does not follow |
|---|---|---|---|---|---|
| ST-01 | O1–O6, E1–E9, their rule bodies, and their capability counts are the first frozen finite menu. | DECLARED_POLICY | `menu`; frozen `PREDICTIONS.md` | frozen hash mismatch or runner/menu mismatch | that the grammar selects one member |
| ST-02 | E1 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E1]`; `test_generation_register_keeps_ties_and_guarded_members` | a growth edge with a new demand or changed old-pair label | behaviour above the rectangle |
| ST-03 | E2 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E2]` | a growth edge with a new demand or changed old-pair label | behaviour above the rectangle |
| ST-04 | E3 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E3]` | a growth edge with a new demand or changed old-pair label | an invariance result |
| ST-05 | E4 generates apart and same under growth, re-labels 683 old pairs, records 204 refusals, 152 fixpoints, and 151 guarded nodes in the rectangle on 2026-09-04. | FINITE_COMPUTATION | `generation[E4]`; full tree receipt | regeneration changes any count | an invariance result or an unguarded total |
| ST-06 | E5 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E5]` | a growth edge with a new demand or changed old-pair label | behaviour above the rectangle |
| ST-07 | E6 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E6]` | a growth edge with a new demand or changed old-pair label | an invariance result |
| ST-08 | E7 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E7]` | a growth edge with a new demand or changed old-pair label | behaviour above the rectangle |
| ST-09 | E8 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E8]` | a growth edge with a new demand or changed old-pair label | behaviour above the rectangle |
| ST-10 | E9 generates neither demand kind under growth and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E9]` | a growth edge with a new demand or changed old-pair label | behaviour above the rectangle |
| ST-11 | E1 labels commute in all 1,345,706 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E1]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-12 | E2 labels commute in all 1,345,706 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E2]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-13 | E3 invariance remains unresolved: 3,695 source-pair O4 values were computed and 1,345,706 transport cases priced, but target-regime labels were not exhaustively replayed. | OPEN | `invariance[E3]` | executable target replay or a Lean statement | that E3 is refuted or invariant |
| ST-14 | E4 invariance remains unresolved: 3,695 source-pair O4 values were computed and 1,345,706 transport cases priced, but target-regime labels were not exhaustively replayed. | OPEN | `invariance[E4]` | executable target replay or a Lean statement | that E4 is refuted or invariant |
| ST-15 | E5 labels commute in all 1,345,706 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E5]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-16 | E6 invariance remains unresolved: 3,695 source-pair O4 values were computed and 1,345,706 transport cases priced, but target-regime labels were not exhaustively replayed. | OPEN | `invariance[E6]` | executable target replay or a Lean statement | that E6 is refuted or invariant |
| ST-17 | E7 labels commute in all 1,345,706 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E7]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-18 | E8 labels commute in all 1,345,706 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E8]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-19 | E9 labels commute in all 1,345,706 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E9]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-20 | The two constant controls commute in all 1,345,706 checked cases each on 2026-09-04. | FINITE_COMPUTATION | `invariance[total_apart]`, `invariance[total_same]` | one unequal transported label | that every supplied control is refutable |
| ST-21 | `parity`, `residue_three`, and `chain` each fail renaming transport at the replayable witness stored in the receipt. | COUNTERMODEL | three `invariance` rows; `test_control_refutations_name_replayable_witnesses` | replayed before and after labels agree | anything about the constants |
| ST-22 | The blanket proposition `controls_refuted` is REFUTED because `total_apart` and `total_same` are invariant counterexamples.  The exact legacy label `OPEN_AT_CONTROLS_REFUTED` records an unmet workflow target, not an OPEN truth status. | REFUTED_CLAIM | `controls_refuted`; two constant `invariance` rows | every supplied control has a valid refuting renaming | that the three actual index readers survive |
| ST-23 | The declared-input count remains two; the rule class is a declaration and no uniqueness or forcing proof exists here. | DECLARED_POLICY | `input_count` | a named uniqueness or grammar proof | that no later rung can change the count |
| ST-24 | No member is both CHECKED invariant and observed to generate both demand kinds under growth within this menu and rectangle. | FINITE_COMPUTATION | `both_kind_members`; `NO_ENDOGENOUS_STAKE_IN_MENU` | a named member in `both_kind_members` | that no other rule can qualify |
| ST-25 | The refined and brute-force regime keys induce the same partition for 847 reached regimes; 0 regimes are above the guard on 2026-09-04. | FINITE_COMPUTATION | `canonical_crosscheck` | differing partitions below the guard | a theorem beyond the reached regimes |
| ST-26 | All nine non-refuted menu members are retained as inputs to challenge three. | DECLARED_POLICY | `retained_menu`, `survivors_for_challenge_three` | a recorded refutation without removal | that challenge three has started |
| ST-27 | X predicts persistence at five data and is not scored in this rung. | PREDICTION | `extrapolation_X` | challenge three's frozen five-data run | that X follows from four data |
| ST-28 | The protected estate question remains open and unchanged. | OPEN | `OB1_UNCHANGED`; `test_protected_open_stays_open` | a separately authorized result | any narrowing from this rung |
| ST-29 | Every full-receipt edge replays its stored event suffix from its parent, increments the response round exactly when applicable, and transports to the quotient child through stored datum/form bijections. | FINITE_COMPUTATION | full tree receipt; `test_full_receipt_hash_and_replay_certificates` | one failed edge certificate | completeness beyond the stored graph |
| ST-30 | PROMPT and PREDICTIONS are byte-bound to freeze commit `d4d5830e53d33e98404cb502ac2e694a871cb091`; receipt execution binds a closed census of fourteen project modules to declared origins, including the pinned package initializer and with no production filename exception. | METATHEORY | `source_verification`; pin and origin injection tests | a changed freeze blob, wrong origin, omitted source, or extra loaded project module, including a `test_`-prefixed module, passes | authority or semantic correctness |
| ST-31 | Growth-origin and accepted-response target kind unions are separately exported and happen to agree for all fourteen rows in this receipt.  The frozen P-G scores use response targets; the Challenge 2 terminal uses growth origins. | FINITE_COMPUTATION | `generation`; frozen-score/challenge-metric divergence regression | one row with `kind_populations_agree` false | that the populations agree by definition |

## Prediction record

`PREDICTIONS.md` was frozen at sha256
`efd3893006b4b59e80a10a4a1b067afe0453101987ca51cf6ae54a3cc9b6c07f`
before computation.  `predictions_scored` records 6 HIT, 9 MISS, 1
UNSCORED_DECLARED_POLICY, and 1 PENDING on 2026-09-04.  P-C1 is unscored
because the runner declares the input count and implements neither frozen
falsifier.  STATUS lists every scored row beside its computed value.
