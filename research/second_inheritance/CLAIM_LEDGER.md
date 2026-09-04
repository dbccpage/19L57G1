# Claim ledger: second_inheritance (rung zero)

`AuthorityEffect: None`.  One class per row.  Evidence names a receipt
key in `receipts/inheritance.json`, a test in `test_inheritance.py`, or a
pinned sealed theorem.

| id | statement | class | evidence | falsifier | what does not follow |
|---|---|---|---|---|---|
| R0-01 | The sealed challenge reports regenerate byte for byte from the sealed kernel at the snapshot. | FINITE_COMPUTATION | `replay.challenges.byte_identical`; `test_sealed_challenges_regenerate_byte_identically` | a differing byte | that the reports are mathematically right; a receipt is not a payload |
| R0-02 | Both sealed closed baselines rebuild from the sealed engine under their own parameters and match their committed summaries on every field, including the full-export sha256. | FINITE_COMPUTATION | `replay.closed_baselines[]`; `test_sealed_closed_baselines_match_every_field` | a differing field | the same for the supply-enabled trees, which this rung does not cite |
| R0-03 | The sibling dual's summary receipt regenerates byte for byte from the sibling's runner. | FINITE_COMPUTATION | `replay.dual_summary.byte_identical` | a differing byte | anything about the sibling's full export, which the summary pins by hash |
| R0-04 | `standing_commitment` and `two_sided_commitment` are absent from `main` at the snapshot; their replay is OPEN. | OPEN | `replay.absent_at_snapshot`; `verify_pins.py` absent-at-snapshot check | either tree present at the snapshot | that their results are refused; they are unreplayed here, not rejected |
| R0-05 | The sealed event grammar has exactly six kinds; supply alone changes no state. | FINITE_COMPUTATION | `census.sealed_event_kinds`; `test_sealed_grammar_has_six_kinds_one_state_preserving`; sealed `supply_no_op` | a seventh kind, or a state-changing supply | that the grammar is the only possible one |
| R0-06 | The sealed engine declares exactly two policies, and the sibling dual exactly three events. | FINITE_COMPUTATION | `census.sealed_policies`, `census.dual_declared_events`; `test_sealed_engine_declares_two_policies_and_dual_three_events` | a further policy or event in the pinned source | that these are the only declared inputs of the estate; the seed names two more, OPEN here |
| R0-07 | Up to eight supplies from either sealed genesis leave the regime unchanged. | FINITE_COMPUTATION | `inertia.supplies`; sealed `supply_no_op` | a changed regime | the bound is eight; the sealed theorem is unbounded and is the real evidence |
| R0-08 | Growing to five data under the all-free stake admits no form, answers nothing, and leaves every state totally collapsed; the tree is one chain. | FINITE_COMPUTATION | `inertia.all_free_growth`; `test_all_free_growth_is_a_collapsed_chain` | a demand, a form, or a branch | the same past five data; and the general statement, which the absent sibling's `empty_commitment_generates_nothing` proves for the one-sided stake and no Lean proves here for the two-sided one |
| R0-09 | The two remaining declared inputs named by the seed are the stake and the stream; the stream's events are sealed and pinned, the stake's declaring event and the growth policy are OPEN custody at this snapshot. | OPEN | `remaining_declared_inputs` | a third remaining input found in the pinned sources | that two is the floor; that is the seed's question, not this rung's answer |

## Prediction record

`PREDICTIONS.md` was frozen at sha256
`86767fe4d8b2ed73ec516855d6d78d3310c22ca6815c835ea4b46060c026ab3a`
before the first run.  Three of three hit, all arithmetically forced
once the definitions were fixed.  Scoring is computed in
`run_inheritance.py` and stored under `predictions_scored`.
