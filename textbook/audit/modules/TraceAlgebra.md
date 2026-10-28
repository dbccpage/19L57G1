# Audit: TraceAlgebra

| field | value |
|---|---|
| Path | lean4/Derivation/TraceAlgebra.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f55f94af1c85460e |
| Lines | 1001 (`wc -l`; inventory.json counts 1002) |
| Imported by root `Derivation.lean` | yes (line 46; `#print axioms` inventory present) |
| Imports | `Derivation.TransitionAlphabet` (transitively `PrimitivePassage`) |
| Declarations | 15 def (`postOf`, `WFRecord`, `Aligned`, `endState`, `eraseTrace`, `LegalTrace`, `licenseInsensitive`, `budgetInsensitive`, `occInsensitive`, `wOneOcc`, `ReplayEqvOn`, `RepresentsZero`, `consNF`, `nf`, `noRedex`), 1 structure (`TRecord`), 2 inductive (`Rw`, `RwStar`), 72 theorem (71 public + `private hfalse`). inventory.json lists "class: 1"; no `class` declaration exists in the file (the count is a text match on `WFClass`/`EffectClass`). |
| Axiom reports in `artifacts/lean_axioms.txt` | 71 lines (every public theorem); axioms seen: `propext, Quot.sound`, `propext`, `none` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module studies the monoid of step functions of the passage dynamics (`PrimitivePassage.step` on `PState`, not the regime model of `Basic.lean`) and asks which algebraic laws it actually satisfies. It first puts every step into a normal form: an event either is inert or installs its named post-state, and `guardHolds` decides which (`step_eq_ite`). From that it derives the laws: inertness is exactly guard failure; the terminal absorbs; every event is idempotent at every state (`step_idem`), including the two funded events, for reasons the proof names (a refined column leaves the menu, a created column is already present). It then shows that disjoint written support is not enough for commutation — guards read fields their step never writes — proves three sufficient frame families (license, budget, occurrence supply), and records five concrete non-commutation countermodels, keeping presentation order of a list store apart from membership agreement. It defines typed transition records and legal traces and proves that erasing a chained trace to events and replaying recovers its end state (`replay_erases`): the typed layer adds nothing replay does not fix. Traces of non-environment-labelled events never change the occurrence store or the license. Refusal records are append-only under every event and every trace. Replay equivalence is shown to be scoped (a pair of event lists equivalent on a declared start class but not at genesis). Finally a two-rule rewrite system on event lists (adjacent idempotence, post-terminal absorption) is proved sound at every start state, terminating, and confluent with a computed unique normal form, and then proved incomplete: two budget writes in a row replay identically to the second alone at every state, yet receive different normal forms.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `postOf` | 86 | def | the named post-state an event installs when accepted (returns `s` on pre-observational refine/addCol, a case the guard excludes) | ADMITTED |
| `TRecord` | 285 | structure | pre, ev, guard, post, cls, spend, profile | ADMITTED (typed record) |
| `WFRecord` | 297 | def (Prop) | every component equals the computed one; accepted; pre in `WFClass` | ADMITTED |
| `Aligned` | 306 | def (Prop) | first record starts at `s`, `post = step pre ev`, chained | ADMITTED |
| `endState` | 311 | def | last post-state of a record list | ADMITTED |
| `eraseTrace` | 315 | def | the event list of a record list | ADMITTED |
| `LegalTrace` | 317 | def (Prop) | `Aligned` and all records `WFRecord` | ADMITTED |
| `licenseInsensitive` | 425 | def | declared Bool table: all events except `addCol`, `setLicense`, `halt` | ADMITTED (declared frame family) |
| `budgetInsensitive` | 431 | def | all except `refineCol`, `addCol`, `setBudget`, `halt` | ADMITTED (declared) |
| `occInsensitive` | 438 | def | exactly `protect`, `declareObs`, `refuse`, `setBudget`, `setLicense` | ADMITTED (declared) |
| `wOneOcc` | 614 | def | witness state with `occ = [5]`, `asserted = [(0,1)]` | ADMITTED (finite witness) |
| `ReplayEqvOn` | 712 | def (Prop) | `∀ s, C s → replayP l₁ s = replayP l₂ s` | ADMITTED |
| `RepresentsZero` | 717 | def (Prop) | `0 ∈ s.occ` | ADMITTED (declared scope) |
| `Rw` | 749 | inductive (Prop) | one-step rewrite: `idem`, `absorb`, closed under `cons` | ADMITTED (declared rewrite system) |
| `RwStar` | 754 | inductive (Prop) | reflexive-transitive closure of `Rw` | ADMITTED |
| `consNF` | 790 | def | cons with adjacent-duplicate collapse | ADMITTED |
| `nf` | 794 | def | the computed normal form (`halt` truncates) | ADMITTED |
| `noRedex` | 798 | def | Bool: no adjacent duplicate and no `halt` followed by anything | ADMITTED |

## 3. Theorems and lemmas

Abbreviations: **Acc** = `Accepted s e = true`; **LI/BI/OI** = `licenseInsensitive e = true` etc.

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `hfalse` | 80 | private `¬ (false = true)` | FROZEN (private) | not in artifact | A |
| `live_of_accepted` | 104 | an accepted event implies the state is live | CONDITIONAL:Acc | propext, Quot.sound | A |
| `live_of_guardHolds` | 110 | a holding guard implies live | CONDITIONAL:`guardHolds s e = true` | propext, Quot.sound | A |
| `step_eq_ite` | 116 | for all `s`, `e`: `step s e = if guardHolds s e then postOf s e else s` | FROZEN | propext, Quot.sound | S |
| `inert_iff_guard_fails` | 183 | `step s e = s ↔ guardHolds s e = false` | FROZEN | propext, Quot.sound | S |
| `terminal_absorbs` | 194 | `step (step s halt) e = step s halt` (re-export of `terminal_absorbing`) | FROZEN | propext, Quot.sound | S |
| `replayP_halted` | 197 | on a halted state every replay is inert | CONDITIONAL:`s.halted = true` | propext, Quot.sound | A |
| `trace_absorbs` | 207 | `replayP (halt :: l) s = step s halt` | FROZEN | propext, Quot.sound | S |
| `mem_append_singleton` | 219 | `a ∈ l ++ [a]` | FROZEN (metatheory) | none | A |
| `v_not_mem_map` | 225 | the refined menu no longer contains `v` | FROZEN | propext, Quot.sound | A |
| `colOk_false_of_mem` | 237 | a column already present fails `colOk` | CONDITIONAL:`t.obs = some cols`, `c ∈ cols` | propext, Quot.sound | A |
| `refineOk_false_of_not_mem` | 245 | a column absent from the menu fails `refineOk` | CONDITIONAL:`t.obs = some cols`, `v ∉ cols` | propext, Quot.sound | A |
| `guardHolds_post_false` | 252 | after an accepted `e`, the guard of `e` fails at the post-state | CONDITIONAL:Acc | propext, Quot.sound | S |
| `step_idem` | 328 | for all `s`, `e`: `step (step s e) e = step s e` | FROZEN | propext, Quot.sound | S |
| `retention_idem`, `terminal_idem` | 337, 341 | instances of `step_idem` | FROZEN | propext, Quot.sound | A |
| `replayP_cons` | 319 | `replayP (a :: l) s = replayP l (step s a)` (rfl) | FROZEN | propext, Quot.sound | A |
| `replay_erases` | 326 | if `Aligned s tr` then replaying the erased events from `s` gives `endState s tr` | CONDITIONAL:`Aligned s tr` | propext, Quot.sound | S |
| `legal_trace_replays` | 338 | same under `LegalTrace s tr` (uses only `Aligned`) | CONDITIONAL:`LegalTrace s tr` | propext, Quot.sound | S |
| `ne_halt_of_licenseInsensitive` / `budget` / `occ` | 448–458 | an insensitive event is not `halt` | CONDITIONAL:LI/BI/OI | propext | A |
| `postOf_halted` | 460 | for `e ≠ halt`, `postOf` keeps `halted` | CONDITIONAL:`e ≠ halt` | propext | A |
| `halted_frame` | 467 | for `e ≠ halt`, `step` keeps `halted` | CONDITIONAL:`e ≠ halt` | propext, Quot.sound | A |
| `postOf_occ`, `occ_unchanged` | 474, 481 | OI events keep `occ` (post-state / step) | CONDITIONAL:OI | propext / propext, Quot.sound | A |
| `guardHolds_licS`, `postOf_licS`, `frame_licS` | 490, 498, 507 | for LI events the guard ignores the license write and the step commutes with `licS` as a record update | CONDITIONAL:LI | propext, Quot.sound | S (frame) |
| `comm_setLicense` | 514 | `step (step s (setLicense b)) e = step (step s e) (setLicense b)` for LI `e` | CONDITIONAL:LI | propext, Quot.sound | S |
| `guardHolds_budS`, `postOf_budS`, `frame_budS` | 528, 536, 544 | same for budget writes and BI events | CONDITIONAL:BI | propext, Quot.sound | S (frame) |
| `comm_setBudget` | 551 | budget writes commute with BI events | CONDITIONAL:BI | propext, Quot.sound | S |
| `comm_setBudget_setLicense` | 564 | the two environment writes commute | FROZEN | propext, Quot.sound | S |
| `guardHolds_occS`, `postOf_occS`, `frame_occS` | 571, 579, 587 | same for occurrence supply and OI events | CONDITIONAL:OI | propext, Quot.sound | S (frame) |
| `comm_admitOcc` | 595 | supply commutes with OI events, inert supply included | CONDITIONAL:OI | propext, Quot.sound | S |
| `noncomm_license_extension` | 620 | at `wFunded`: `setLicense false` then `addCol [0]` ≠ the reverse order | REFUTED (`decide`) | propext, Quot.sound | S |
| `noncomm_budget_extension` | 626 | at `wFunded`: `setBudget 0` / `addCol [0]` do not commute | REFUTED (`decide`) | propext, Quot.sound | S |
| `noncomm_terminal` | 632 | at `genesisP`: `halt` / `setLicense false` do not commute | REFUTED (`decide`) | propext, Quot.sound | S |
| `noncomm_supply_retention` | 640 | at `wOneOcc`: `admitOcc 6` / `admitWit 0 1` do not commute | REFUTED (`decide`) | propext, Quot.sound | S |
| `noncomm_same_store` | 647 | at `wAssert`: `assertWit 0 1` / `assertWit 1 0` do not commute (list order) | REFUTED (`decide`) | propext, Quot.sound | S |
| `same_store_observationally_equal` | 656 | the two results of the previous theorem have mutually included `asserted` lists | VERIFIED_FINITE | propext, Quot.sound | S |
| `internal_trace_preserves_occ` / `_license` | 670, 679 | a replay of events all with `isEnvOwned = false` keeps `occ` / `licensed` | CONDITIONAL:all events non-env | propext, Quot.sound | S |
| `internal_blocks_cannot_supply_or_license` | 691 | for any block of `nextFamilyP s`: no event equals `admitOcc 0`, none equals `setLicense false` | FROZEN (over all `s`, `b`) | propext, Quot.sound | S |
| `refusal_persists_step` / `_replay` | 705, 713 | a recorded refusal survives every event / every trace | CONDITIONAL:`(i,j) ∈ s.refusals` | propext, Quot.sound | S |
| `refusal_not_erasable` | 724 | at `wObstructed`, `refuse 0 1` is accepted and writes `[(0,1)]` | VERIFIED_FINITE | propext, Quot.sound | S |
| `replay_eqv_scoped` | 719 | on states with `0 ∈ occ`, `[admitOcc 0]` and `[]` replay equally | FROZEN (over the declared class) | propext, Quot.sound | S |
| `replay_eqv_not_unscoped` | 729 | at genesis the same pair replays differently | REFUTED (`decide`) | propext, Quot.sound | S |
| `rw_sound` | 762 | one `Rw` step preserves `replayP` at every start state | FROZEN | propext, Quot.sound | S |
| `rwStar_sound` | 776 | closure of the above | FROZEN | propext, Quot.sound | S |
| `rw_length` | 783 | every `Rw` step strictly shortens the list | FROZEN | propext, Quot.sound | S |
| `nf_halt`, `nf_cons_ne` | 807, 812 | unfolding equations of `nf` | FROZEN | none | A |
| `consNF_idem`, `nf_idem_cons`, `nf_cons_congr` | 818, 837, 843 | `nf` respects the idempotence rule and is a congruence for cons | FROZEN | none | A |
| `rw_preserves_nf`, `rwStar_preserves_nf` | 850, 856 | rewriting does not change `nf` | FROZEN | none | A |
| `noRedex_consNF`, `nf_noRedex` | 862, 881 | `nf` outputs are redex-free | FROZEN | none / none | S |
| `noRedex_nf_eq` | 890 | a redex-free list is its own `nf` | CONDITIONAL:`noRedex l = true` | propext | S |
| `rwStar_cons`, `rwStar_to_nf` | 908, 915 | every list rewrites to its `nf` | FROZEN | none | S |
| `rw_confluent` | 947 | any two reducts of `l` join (at `nf l`) | FROZEN | none | S |
| `nf_unique` | 956 | two redex-free reducts of one list are equal | CONDITIONAL:`noRedex a`, `noRedex b` | propext | S |
| `nf_sound` | 965 | `replayP (nf l) s = replayP l s` | FROZEN | propext, Quot.sound | S |
| `rewrite_not_complete` | 975 | `[setBudget 1, setBudget 2]` and `[setBudget 2]` replay equally at every state, yet `nf` differs | REFUTED (completeness of the two-rule system) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- **Base model and codebook.** Everything is over `PrimitivePassage.PState`/`step`/`replayP` and uses `TransitionAlphabet`'s `guardHolds`, `Accepted`, post-state lemmas and `accepted_eq_guardHolds`; `step_eq_ite` is a repackaging of that theorem plus the eleven `step_*_acc` lemmas.
- **Declared tables.** `licenseInsensitive`, `budgetInsensitive`, `occInsensitive` are declared Bool tables, chosen so that the two `rfl` halves of each frame hold; the source says necessity and exhaustiveness are not proved. `Rw` is a declared two-rule system. `RepresentsZero` is a declared start class for one example.
- **Recurring hypotheses.** `Accepted s e = true`; the insensitivity predicates; `Aligned`/`LegalTrace`; `noRedex`.
- **Typed records.** `TRecord` carries `cls`, `spend`, `profile`, but no theorem reads these fields: `replay_erases` uses only `r.pre`, `r.ev`, `r.post` and the `Aligned` equations; `WFRecord` appears only inside `LegalTrace`, and `legal_trace_replays` discards it (`h.1`). The record type is therefore admitted structure with no theorem-level consequence beyond `Aligned`.
- **Library lemmas doing real work.** `apply_ite` (the frame proofs), `List.mem_map`, `List.any_append`, `omega` on lengths; `DecidableEq PEvent` (derived) for `consNF`/`nf`/`noRedex` and for `decide` on the countermodels.
- **Finitude rule.** `Rw`/`RwStar` are `Prop`-valued inductives over `List PEvent` (metatheory); `ReplayEqvOn` quantifies over all `PState`; `rw_sound` is "sound at EVERY start state" — a metatheoretic universal, not a claim that the system holds a totality of states. No docstring reads these as internal. `nf : List PEvent → List PEvent` is a metatheoretic normalizer; the module says it is "deliberately much weaker than replay equivalence".
- Unearned identity: none found (`noncomm_same_store` keeps list order and membership apart explicitly). Unrestricted external universe: `mem_append_singleton` polymorphic in `{α : Type}` as helper only. Unbounded function treated as internally available: none found. Silently assumed observer: none found. Unspecified correspondence between presentations: none claimed. Cost function without justification: none. Admitted condition later described as forced: none found (the insensitivity tables are called "declared" throughout). Finite computation presented as universal: none found — the 153-pair commutation matrix is in the ledger as Python computation.

## 5. Derived consequences

- No other Lean module imports `TraceAlgebra` (grep of `lean4/`; the dependency graph lists no consumers). The root prints axioms for all 71 public theorems.
- Ledger CL-PD2-TRACE-ALGEBRA cites 35 theorems (see §8). `paper/paper.md` and `paper/primitive_difference_map.md` do not name the module; `paper/paper_change_log.md` ("Goals 2 and 3", items 7–8) records that idempotence turned out universal and that the rewrite system is incomplete.
- Internally: `step_eq_ite` feeds every frame theorem; `step_idem` feeds `rw_sound`; `rwStar_preserves_nf` + `rwStar_to_nf` give confluence and unique normal forms.

## 6. Counterexamples and limitations

| theorem | what it refutes | witness |
|---|---|---|
| `noncomm_license_extension` | "license writes commute with everything" | `wFunded`, `setLicense false` / `addCol [0]` |
| `noncomm_budget_extension` | "budget writes commute with everything" | `wFunded`, `setBudget 0` / `addCol [0]` |
| `noncomm_terminal` | "the terminal is a frame" | `genesisP`, `halt` / `setLicense false` |
| `noncomm_supply_retention` | "occurrence supply commutes with retention" | `wOneOcc`, `admitOcc 6` / `admitWit 0 1` |
| `noncomm_same_store` | "two writes into one store commute" | `wAssert`, `assertWit 0 1` / `assertWit 1 0` |
| `replay_eqv_not_unscoped` | the particular pair `[admitOcc 0]`, `[]` is unscoped-equivalent | `genesisP` |
| `rewrite_not_complete` | completeness of the two-rule `nf` for universal replay equivalence | `[setBudget 1, setBudget 2]` vs `[setBudget 2]` |

Not proved: necessity or exhaustiveness of the three frame families; any commutation outside them; that `nf` is complete for any equivalence; that the typed record fields `cls`, `spend`, `profile` carry any law; a general "disjoint support ⇒ commutes" (shown false). `internal_blocks_cannot_supply_or_license` is instantiated at `admitOcc 0` and `setLicense false` only; the general forms are `TransitionAlphabet.internal_family_no_occurrence_supply` / `_no_license_write`. `same_store_observationally_equal` checks mutual membership of the `asserted` field only (the other fields are equal by construction); it is not the programme's profile-based observational equivalence of `observe.py`.

## 7. Axiom dependencies

All 71 artifact lines lie within `{propext, Quot.sound}`; the rewrite-system lemmas are mostly axiom-free. None exceed the boundary.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- Axiom artifact: 71/71 public theorems present.
- Ledger CL-PD2-TRACE-ALGEBRA cites `replay_erases`, `legal_trace_replays`, `inert_iff_guard_fails`, `terminal_absorbs`, `trace_absorbs`, `step_idem`, `frame_licS/budS/occS`, `comm_setLicense`, `comm_setBudget`, `comm_setBudget_setLicense`, `comm_admitOcc`, the five `noncomm_*`, `same_store_observationally_equal`, `internal_trace_preserves_occ/license`, `internal_blocks_cannot_supply_or_license`, `refusal_persists_step/replay`, `refusal_not_erasable`, `replay_eqv_scoped`, `replay_eqv_not_unscoped`, `rw_sound`, `rwStar_sound`, `rw_length`, `rw_confluent`, `nf_unique`, `nf_sound`, `rewrite_not_complete` (also `nf_noRedex`, `noRedex_nf_eq` in the dependency graph).
- Probe: none run for this module; every `decide` witness is a closed term and was read.

## 9. Related Python implementations

- `code/derivation/trace_algebra.py`: `post_of`, `step_by_normal_form`, `TRecord`, `make_record`, `wf_record`, `aligned`, `end_state`, `erase_trace`, `legal_trace`, `build_trace`, `cons_nf`, `nf`, `no_redex`, `rw_reducts`, `normal_forms`, `list_battery`, and the reports (`identity_report`, `trace_report`, `commutation_report` with the 153-pair matrix, `frame_report`, `internal_report`, `scoping_report`, `rewrite_report`).
- `code/run_trace_algebra.py` → `artifacts/trace_algebra.json`.
- `tests/test_trace_algebra.py`: `test_post_of_and_step_normal_form`, `test_identity_laws_hold_everywhere`, `test_typed_records_and_legal_traces`, `test_commutation_matrix_and_countermodels`, `test_frames_are_sound_and_tight`, `test_internal_traces_and_refusal_records`, `test_replay_equivalence_is_scoped`, `test_rewrite_system_is_sound_terminating_confluent`, `test_normal_form_computation`, `test_runner_byte_stable`.

## 10. Textbook placement proposal

- Prerequisites: `PrimitivePassage.step`/`replayP`, `TransitionAlphabet.guardHolds` and `accepted_eq_guardHolds`, the named post-states; the idea of a guard reading a field.
- Substantive: `step_eq_ite`, `inert_iff_guard_fails`, `step_idem` (with `guardHolds_post_false` as its mechanism), the three frame families and `comm_*`, the five `noncomm_*` with `same_store_observationally_equal` (presentation vs membership), `replay_erases`, `refusal_persists_replay`, `replay_eqv_scoped`/`_not_unscoped`, and the rewrite system as a unit (`rw_sound`, `rw_length`, `rw_confluent`, `nf_unique`, `rewrite_not_complete`).
- Auxiliary: `live_of_*`, `ne_halt_of_*`, `postOf_*`, `guardHolds_*S`, `v_not_mem_map`, `colOk_false_of_mem`, `refineOk_false_of_not_mem`, all `nf`/`consNF`/`noRedex` unfolding lemmas, `retention_idem`, `terminal_idem`, `replayP_cons`.
- Suggested lesson: **"Every step is idempotent, and that is almost all the algebra there is"** — the one question: *which rearrangements of an event list leave replay unchanged, and can a list-only rewrite find them all?* (Answer: idempotence and absorption always; most commutations fail because guards read; the two-rule normalizer is sound and confluent but incomplete.)
- Recommend omitting: `TRecord`/`WFRecord`/`LegalTrace` beyond a remark — no theorem uses the typed fields, and `replay_erases` is a statement about `Aligned` alone; `internal_blocks_cannot_supply_or_license` (teach the general `TransitionAlphabet` forms instead); `RepresentsZero` as a named definition (inline the example).

## 11. Interpretation findings

1. **Docstring at line 731–733 vs `rewrite_not_complete`** — docstring: "Replay equivalence without a declared start class is not a relation this dynamics satisfies." The Lean (`replay_eqv_not_unscoped`) proves only that ONE pair, `[admitOcc 0]` vs `[]`, is not unscoped-equivalent. The same module's `rewrite_not_complete` (line 975) proves an unscoped equivalence `∀ s, replayP [setBudget 1, setBudget 2] s = replayP [setBudget 2] s`, so unscoped replay equivalence is a nontrivial relation the dynamics does satisfy for some pairs. The ledger's wording "(viii) Replay equivalence is SCOPED: `replay_eqv_scoped` holds on a declared start class while `replay_eqv_not_unscoped` refutes the unscoped form" is accurate only for that pair. Classification: INTERPRETATION DEFECT (docstring and ledger overgeneralize one countermodel; the Lean is correct).
2. **Ledger CL-PD2-TRACE-ALGEBRA statement** — "a typed transition record binds pre-state, event, discharged guard, post-state, effect class, resource delta, and the complete computed profile; … From there the laws are DERIVED". The laws are derived from `step`/`guardHolds`, not from the record type; no theorem mentions `cls`, `spend` or `profile`. Classification: INTERPRETATION DEFECT (minor; the record is inert structure, and "from there" overstates its role).
3. **Name `same_store_observationally_equal`** — the theorem checks mutual membership of the `asserted` lists of two concrete states. "Observationally" is used elsewhere in the programme for profile-based equivalence (`observe.py`). The docstring says "the two results carry the same asserted pairs", which is exact. Classification: INTERPRETATION DEFECT (naming only).
4. **Docstring of `internal_blocks_cannot_supply_or_license`** — "The generator's blocks are internal in exactly this sense for occurrence supply and the license": the Lean states the two instances `admitOcc 0` and `setLicense false`; the general statements live in `TransitionAlphabet`. Not a defect in the ledger, which cites both modules; recorded for the textbook.
5. Vacuity check: `Aligned s []` is `True`, so `replay_erases` on the empty trace is trivial but the induction is genuine; `LegalTrace` is inhabitable (any accepted step at a `WFClass` state with the computed components). Frame hypotheses are satisfiable (e.g. `protect` is in all three tables). No vacuous theorem found. `step_idem` is proved for all `s`, `e` with no hypothesis — the docstring word "EVERY" is matched by the quantifier.
6. Words "sound", "confluent", "unique": `rw_sound` is quantified over all `s : PState` (matches "EVERY start state"); `nf_unique` is uniqueness among redex-free reducts of a fixed source (matches); "complete" appears only in the negative theorem. None found overreading.
