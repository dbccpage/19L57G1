# Audit: Horizon

| field | value |
|---|---|
| Path | lean4/Derivation/Horizon.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 8251fc44d369e716 |
| Lines | 424 |
| Imported by root `Derivation.lean` | yes (line 28) |
| Imports | Derivation.Initiality (transitively Constitution, NoOutside, Completion, Represented, RefusalFrontier) |
| Declarations | 7 def (specViews, specReqs, specWorld, w1, w2, w3, satNoopWorld), 26 theorem (inventory lists 27 because the docstring word "with" was scanned as a name) |
| Axiom reports in `artifacts/lean_axioms.txt` | 10 lines; axioms seen: propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

A PR #12 correction module. The earlier ledger claimed "lawfulness across extension" for the generated run while the only Lean fact was quiescence at stage 3. This module repairs the gap upward: it writes down the complete record of the generated world at stage k (`specWorld k`: carrier 0..k, one singleton view column and one requirement (0, i+1) per earlier stage, no refusals, budget spent to zero, licensed) and proves by induction that `worldAt k` equals it at every stage (`worldAt_spec`). From the characterisation it proves quiescence, well-formedness and per-event acceptance of every block at every horizon, and lifts them to the driver's generated run through `driver_reproduces_tower`. A second correction pins the budget semantics shared with the Python mirror: for every descriptor and every event the family interpreter leaves the budget alone, applies the saturating `Nat` decrement, or sets it by an explicit `setBudget`; the audit's countermodel (a `gateBudget`-off descriptor at budget 0) is a no-op in Lean, decided for all 64 descriptors.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| specViews | 45 | def | `(range k).map (fun i => [i+1])` | ADMITTED (specification) |
| specReqs | 49 | def | `(range k).map (fun i => (0, i+1))` | ADMITTED |
| specWorld | 53 | def | the complete record at stage k | ADMITTED |
| w1 / w2 / w3 | 59 / 65 / 71 | def | intermediate states after setBudget, admitTok, require within block m+1 | ADMITTED |
| satNoopWorld | 402 | def | the audit countermodel world (satisfied requirement, budget 0) | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| specViews_succ | 76 | specViews (m+1) = specViews m ++ [[m+1]] | FROZEN | not in artifact | A |
| specReqs_succ | 82 | specReqs (m+1) = specReqs m ++ [(0,m+1)] | FROZEN | not in artifact | A |
| fresh_not_mem | 90 | m+1 ∉ range (m+1) | FROZEN | not in artifact | A |
| req_not_mem | 95 | (0, m+1) ∉ specReqs m | FROZEN | not in artifact | A |
| view_not_mem | 103 | [m+1] ∉ specViews m | FROZEN | not in artifact | A |
| data_len | 113 | length of range (m+1) ++ [m+1] is m+2 | FROZEN | not in artifact | A |
| sep_new_col | 118 | sepB [m+1] 0 (m+1) = true | FROZEN | not in artifact | A |
| old_cols_blind | 127 | c ∈ specViews m ⇒ sepB c 0 (m+1) = false | FROZEN | not in artifact | A |
| step_admit_fresh | 144 | t ∉ data ⇒ admitTok appends | FROZEN | not in artifact | A |
| step_require_ok | 149 | reqOkB ⇒ require appends | FROZEN | not in artifact | A |
| step_addView_ok | 155 | full addView guard ⇒ addView applies and decrements | FROZEN | not in artifact | A |
| req_guard | 165 | reqOkB (w2 m) 0 (m+1) = true | FROZEN | not in artifact | A |
| satB_w3_false | 176 | the new requirement is unsatisfied in w3 m | FROZEN | not in artifact | A |
| increase_guard | 185 | increaseB (w3 m) [m+1] = true | FROZEN | not in artifact | A |
| aug_guard | 201 | the full addView guard holds at w3 m | FROZEN | not in artifact | A |
| final_assembly | 222 | applying addView [m+1] to w3 m gives specWorld (m+1) | FROZEN | not in artifact | A |
| worldAt_spec | 236 | ∀ k, worldAt k = specWorld k | FROZEN | propext, Quot.sound | S |
| worldAt_quiescent | 261 | quiescentB (worldAt k) at every k | FROZEN | propext, Quot.sound | S |
| worldAt_wf | 275 | WF (worldAt k) at every k | FROZEN | propext, Quot.sound | S |
| block_all_accepted | 294 | each of the four block events changes the state, and the block lands on worldAt (k+1) | FROZEN | propext, Quot.sound | S |
| genesis_accepted | 343 | step genesis (admitTok 0) ≠ genesis | VERIFIED_FINITE | propext, Quot.sound | A |
| gen_quiescent | 351 | quiescentB (genWorld k).w at every k | FROZEN | propext, Quot.sound | S |
| gen_wf | 358 | WF (genWorld k).w at every k | FROZEN | propext, Quot.sound | S |
| interp_budget_bound | 371 | for every descriptor d, world, event: budget unchanged, or budget − 1 (Nat), or set by setBudget n | FROZEN | propext, Quot.sound | S |
| budget_saturation_noop | 411 | the audit descriptor and event are a no-op on satNoopWorld | VERIFIED_FINITE | propext, Quot.sound | S |
| mark_saturation_all_descs | 419 | all 64 descriptors agree the audit event is a no-op | VERIFIED_FINITE | propext, Quot.sound | S |

Count check: 26 theorems; 10 in the artifact, 16 helpers not.

## 4. External and admitted assumptions

- The specification `specWorld` is written by hand; the theorem `worldAt_spec` is what makes it binding. The stream `histUpTo` / `worldAt` is the supplied metatheoretic producer of Represented, and `genWorld` is Constitution's metatheoretic driver; `∀ k` ranges over Lean's Nat. Finitude flag: "at every horizon" is a statement about the Lean-indexed family, not about an unbounded run the system holds. The module uses "horizon-free" language only through the paper; its own docstrings say "at every stage".
- Library: `List.range_succ`, `List.map_append`, `List.mem_map`, `List.mem_range`, `List.mem_singleton`, `List.length_*`, `omega`, `simpa`.
- Unearned identity: none. Unrestricted external universe: none. Unbounded function treated as internally available: none beyond the disclosed stream. Silently assumed observer: none. Unspecified correspondence: none. Cost function: none. Admitted condition later described as forced: none; the specification is proved equal. Finite computation presented as universal: `budget_saturation_noop` is one instance and `mark_saturation_all_descs` is the exhaustive 64-descriptor version; `interp_budget_bound` is the general theorem. Correctly layered.

## 5. Derived consequences

Not imported by any Derivation module (checked: `grep Horizon lean4/Derivation` finds only the root import and `InterpreterBoundary`'s docstring-free use of nothing). Ledger CL-NC-AUTONOMY cites `worldAt_spec`, `gen_quiescent`, `gen_wf`, `block_all_accepted`, `genesis_accepted`; `pr11_correction_ledger.md` C6 and C10 cite the module; `paper_change_log.md` records the repair.

## 6. Counterexamples and limitations

- `budget_saturation_noop` is the pinned audit countermodel against the earlier Python behaviour (budget −1), not against a Lean claim.
- Not proved: anything about the `close` policy run (no driver exists for it); acceptance of events outside the tower blocks; anything about `interpStep` beyond the budget field. `block_all_accepted` proves each event "changes the state", which is the module's reading of "accepted" — correct for these four events because each guard, when it fails, yields the identity; a general equivalence "accepted ↔ state changed" is not stated (and would be false for `admitTok` of a present token, where rejection and no-op coincide by design).

## 7. Axiom dependencies

All 10 artifact lines within {propext, Quot.sound}. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 10 of 26 theorems in the artifact; the 16 helpers are not exported. Paper cites the exported ones (CL-NC-AUTONOMY, pr11 C6/C10). No probe run; proofs read in full (the `worldAt_spec` induction unfolds the four-event block through `w1`, `w2`, `w3` with explicit guard lemmas; checked).

## 9. Related Python implementations

`code/derivation/completion.py::interp_step` (saturating decrement), `protocols_report` (acceptance to 15 rounds); `code/derivation/represented.py::events_all_accepted`, `productivity_report`. Tests: `tests/test_completion.py::test_budget_saturation_matches_lean_nat`, `test_budget_trichotomy_every_descriptor_event`, `tests/test_represented.py::test_productive_run_prefix_compatible`.

## 10. Textbook placement proposal

- Prerequisites: `histUpTo`/`worldAt`/`blockEvents` from Represented; `towerGen`/`genWorld`/`driver_reproduces_tower` from Constitution; `interpStep`.
- Substantive: `specWorld` and `worldAt_spec` (the technique: characterise the whole record, then read properties off it), `worldAt_quiescent`, `worldAt_wf`, `block_all_accepted`, `gen_quiescent`/`gen_wf`, `interp_budget_bound` (as the cross-language pin).
- Auxiliary: all sixteen helpers, `genesis_accepted`, `budget_saturation_noop`, `mark_saturation_all_descs`.
- Lesson title: "From stage 3 to every stage: characterising the generated run." The one question: how does one turn an instance check into an every-horizon theorem, and what exactly does "lawful at every horizon" quantify over?
- Omit: the two saturation `decide` theorems (a footnote on the Python repair suffices).

## 11. Interpretation findings

1. Docstring of `block_all_accepted` (line 290–293): "no emitted event is ever silently rejected". Lean: each of the four events applied in order changes the state. For these events "changed" implies "accepted" because every rejected branch of `step` is the identity, so the reading is sound here; but the converse direction (an accepted event always changes the state) is false in general (`admitTok` of a present token) and is not claimed. Classification: none; noted so the textbook defines "accepted" as "guard passed", not "state changed".
2. Ledger CL-NC-AUTONOMY "lawfulness across extension ... at every horizon". Lean: for every Lean natural k. The run is the supplied/generated Nat-indexed family; the system has no object "the run at every horizon". Classification: INTERPRETATION DEFECT (mild, finitude): "every horizon" is metatheoretic quantification, which the Represented write-up already says of `histUpTo`; the Horizon docstrings themselves say "at every stage" without claiming an internal totality.
3. Vacuity: none.
