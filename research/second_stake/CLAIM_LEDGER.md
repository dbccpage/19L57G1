# Claim ledger: second_stake

`AuthorityEffect: None`.  One evidence class per row.  Receipt keys refer to
`receipts/stake.json`; node histories live in the hash-bound full receipt.

| id | statement | class | evidence | falsifier | does not follow |
|---|---|---|---|---|---|
| ST-01 | O1–O6, E1–E9, their rule bodies, and their capability counts are the first frozen finite menu. | DECLARED_POLICY | `menu`; frozen `PREDICTIONS.md` | frozen hash mismatch or runner/menu mismatch | that the grammar selects one member |
| ST-02 | E1 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E1]`; `test_generation_register_keeps_ties_and_guarded_members` | an accepted response edge or changed old-pair label | behaviour above the rectangle |
| ST-03 | E2 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E2]` | an accepted response edge or changed old-pair label | behaviour above the rectangle |
| ST-04 | E3 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E3]` | an accepted response edge or changed old-pair label | an invariance result |
| ST-05 | E4 answers apart and same, re-labels 537 old pairs, records 105 refusals, 123 fixpoints, and 89 guarded nodes in the rectangle on 2026-09-04. | FINITE_COMPUTATION | `generation[E4]`; full tree receipt | regeneration changes any count | an invariance result or an unguarded total |
| ST-06 | E5 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E5]` | an accepted response edge or changed old-pair label | behaviour above the rectangle |
| ST-07 | E6 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E6]` | an accepted response edge or changed old-pair label | an invariance result |
| ST-08 | E7 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E7]` | an accepted response edge or changed old-pair label | behaviour above the rectangle |
| ST-09 | E8 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E8]` | an accepted response edge or changed old-pair label | behaviour above the rectangle |
| ST-10 | E9 answers neither kind and performs no re-labelling in the rectangle. | FINITE_COMPUTATION | `generation[E9]` | an accepted response edge or changed old-pair label | behaviour above the rectangle |
| ST-11 | E1 labels commute in all 4,606,028 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E1]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-12 | E2 labels commute in all 4,606,028 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E2]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-13 | E3 invariance is unresolved at source regime 153 because 241,920 bijection pairs exceed the 100,000 guard. | OPEN | `invariance[E3]` | a finished exact check or Lean statement | that E3 is refuted |
| ST-14 | E4 invariance is unresolved at source regime 153 because 241,920 bijection pairs exceed the 100,000 guard. | OPEN | `invariance[E4]` | a finished exact check or Lean statement | that E4 is refuted |
| ST-15 | E5 labels commute in all 4,606,028 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E5]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-16 | E6 invariance is unresolved at source regime 153 because 241,920 bijection pairs exceed the 100,000 guard. | OPEN | `invariance[E6]` | a finished exact check or Lean statement | that E6 is refuted |
| ST-17 | E7 labels commute in all 4,606,028 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E7]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-18 | E8 labels commute in all 4,606,028 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E8]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-19 | E9 labels commute in all 4,606,028 checked pair-renaming cases on 2026-09-04. | FINITE_COMPUTATION | `invariance[E9]` | one unequal transported label | a theorem beyond the reached regimes |
| ST-20 | The two constant controls commute in all 4,606,028 checked cases each on 2026-09-04. | FINITE_COMPUTATION | `invariance[total_apart]`, `invariance[total_same]` | one unequal transported label | that every supplied control is refutable |
| ST-21 | `parity`, `residue_three`, and `chain` each fail renaming transport at the replayable witness stored in the receipt. | COUNTERMODEL | three `invariance` rows; `test_control_refutations_name_replayable_witnesses` | replayed before and after labels agree | anything about the constants |
| ST-22 | The blanket target `controls_refuted` remains unresolved because both constant controls are invariant by definition. | OPEN | `OPEN_AT_CONTROLS_REFUTED` | a valid refuting renaming for each constant | that the three actual index readers survive |
| ST-23 | The declared-input count remains two; the rule class is a declaration and no uniqueness or forcing proof exists here. | DECLARED_POLICY | `input_count` | a named uniqueness or grammar proof | that no later rung can change the count |
| ST-24 | No member is both CHECKED invariant and observed to answer both kinds within this menu and rectangle. | FINITE_COMPUTATION | `both_kind_members`; `NO_ENDOGENOUS_STAKE_IN_MENU` | a named member in `both_kind_members` | that no other rule can qualify |
| ST-25 | The refined and brute-force regime keys induce the same partition for 842 reached regimes on 2026-09-04; three regimes are above the guard. | FINITE_COMPUTATION | `canonical_crosscheck` | differing partitions below the guard | agreement for a guarded regime |
| ST-26 | All nine non-refuted menu members are retained as inputs to challenge three. | DECLARED_POLICY | `retained_menu`, `survivors_for_challenge_three` | a recorded refutation without removal | that challenge three has started |
| ST-27 | X predicts persistence at five data and is not scored in this rung. | PREDICTION | `extrapolation_X` | challenge three's frozen five-data run | that X follows from four data |
| ST-28 | The protected estate question remains open and unchanged. | OPEN | `OB1_UNCHANGED`; `test_protected_open_stays_open` | a separately authorized result | any narrowing from this rung |

## Prediction record

`PREDICTIONS.md` was frozen at sha256
`efd3893006b4b59e80a10a4a1b067afe0453101987ca51cf6ae54a3cc9b6c07f`
before computation.  `predictions_scored` records eight HIT, eight MISS, zero
VACUOUS, and one PENDING on 2026-09-04.  STATUS lists every miss beside its
computed value.
