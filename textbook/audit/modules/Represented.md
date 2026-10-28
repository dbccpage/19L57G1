# Audit: Represented

| field | value |
|---|---|
| Path | lean4/Derivation/Represented.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 7c331eaa25a87702 |
| Lines | 1363 |
| Imported by root `Derivation.lean` | yes (line 23) |
| Imports | none (core Lean only; the module is self-contained) |
| Declarations | 3 abbrev, 2 structure, 1 inductive, 44 def, 65 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 48 lines; axioms seen: none / propext / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module answers an externally imposed challenge (2026-08-12): can every runtime cause of represented progress — evaluator, requirement, scheduler, tie-break, fresh-name source, fuel, authorization, stopping condition — be carried in the represented state or the represented history, so that no hidden selector or evaluator sits outside replay? It builds one small kernel: a `World` (a data store of admitted tokens, a list of view columns, recorded separation requirements, recorded refusals, a budget, an augmentation license, and an inert `notes` field), an event grammar, and an acceptance-guarded `step` whose only inputs are the world and the event. Obstruction is defined as a recorded, currently violated requirement together with the exhaustive failure of a declared finite response menu; same-structure repair is `mark`, structure-creating augmentation is `addView`, and refusal is recordable only with that certificate. The theorems establish, relative to this fixed constitution, replay determinism, factorization of the step through the represented support, invariance under replay-equivalence (no order-sensitive tie-break), repair and augmentation soundness, the progress dichotomy (a non-empty repair family, or a certified obstruction with an accepted canonical augmentation), closure (violations come only from `require`), a supplied prefix-compatible unbounded run, and a panel-relative notion of certification. Eight countermodels show semantics that consume one unrepresented input, or that misread a definition, failing exactly the corresponding theorem. The module explicitly states that the constitution (grammar, laws, menu, guards, history producer) is fixed metatheory and does not derive itself.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| View | 70 | abbrev | `List Nat`: a column marking data positions; set-like by intent | ADMITTED |
| Req | 73 | abbrev | `Nat × Nat`: an ordered requirement "separate positions i and j" | ADMITTED |
| World | 80 | structure | data, views, reqs, refusals, budget : Nat, augLicensed : Bool, notes | ADMITTED (budget and license are declared policy fields) |
| genesis | 90 | def | empty world with budget 0 and license true | ADMITTED |
| sepB | 94 | def | column c separates i, j iff exactly one is a member | ADMITTED (declared separation law; constitution) |
| satB | 97 | def | some view separates the requirement | ADMITTED (constitution) |
| violB | 100 | def | recorded and not satisfied | ADMITTED |
| quiescentB | 103 | def | every recorded requirement satisfied | ADMITTED |
| markApply | 108 | def | prepend p to every view equal to v (match by value) | ADMITTED |
| preservesB | 111 | def | every requirement satisfied in w is satisfied in w' | ADMITTED |
| dischargesSomeB | 114 | def | some violated requirement of w is satisfied in w' | ADMITTED |
| markOkB | 117 | def | acceptance guard for a mark (in menu, in bounds, fresh in v, discharges, preserves) | ADMITTED (constitution) |
| augApply | 125 | def | append column c | ADMITTED |
| increaseB | 128 | def | c separates some bounded off-diagonal pair no view separates | ADMITTED |
| augOkB | 133 | def | acceptance guard for augmentation (bounded, fresh, increasing) | ADMITTED (constitution) |
| responseMenu | 144 | def | all (view, position) pairs: the declared finite menu | ADMITTED (declared policy; map row says "the menu is constitution") |
| repairsB | 148 | def | menu item is an accepted mark that satisfies r | ADMITTED |
| repairFamily | 151 | def | filter of the menu by repairsB (all ties retained) | ADMITTED |
| obstructedB | 154 | def | violated and every menu item fails | ADMITTED |
| Event | 164 | inductive | admitTok, require, mark, addView, refuse, note, setBudget, setAugLicense | ADMITTED (constitution: the event grammar) |
| reqOkB | 175 | def | guard for require: off-diagonal, in bounds, not already recorded | ADMITTED |
| step | 179 | def | the guarded transition; `setBudget`/`setAugLicense`/`note` are unguarded | ADMITTED (constitution) |
| replay | 200 | def | left fold of step | ADMITTED |
| Supp | 219 | structure | World minus notes | ADMITTED |
| supp | 228 | def | projection to Supp | ADMITTED |
| SameElems | 329 | def | membership-equal lists | ADMITTED |
| WEquiv | 332 | def | data equal literally; views/reqs/refusals membership-equal; budget, license equal | ADMITTED (declared replay-equivalence) |
| WF | 689 | def | every recorded requirement off-diagonal and in bounds | ADMITTED (invariant, proved to hold on replays) |
| blockEvents | 1013 | def | the four-event block of stage k | ADMITTED (supplied stream) |
| histUpTo | 1016 | def | `Nat → List Event`, the supplied prefix-compatible stream | ADMITTED (metatheoretic history producer, declared as such) |
| worldAt | 1020 | def | replay of histUpTo k from genesis | ADMITTED |
| witValid | 1090 | def | every entry ≥ list length | ADMITTED (countermodel) |
| prefixList | 1102 | def | first n values of g : Nat → Nat | ADMITTED (countermodel; g is metatheory) |
| Evaluator | 1130 | abbrev | `List View` | ADMITTED |
| verdictB | 1132 | def | some column of E separates | ADMITTED |
| certPosB | 1137 | def | non-empty panel, every evaluator says separated | ADMITTED |
| certNegB | 1140 | def | non-empty panel, every evaluator says not separated | ADMITTED |
| stepSched | 1194 | def | countermodel semantics with external scheduler bit | ADMITTED (countermodel) |
| schedWorld | 1199 | def | unused first attempt (the docstring at 1203 says so) | ADMITTED (dead definition) |
| schedWorld2 | 1206 | def | concrete world with a live repair | ADMITTED |
| stepGensym | 1214 | def | countermodel with external seed | ADMITTED |
| stepOracle | 1223 | def | countermodel with hidden evaluator | ADMITTED |
| oracleWorld | 1234 | def | concrete world | ADMITTED |
| obstructedTruncB | 1245 | def | truncated-search obstruction | ADMITTED (countermodel) |
| truncWorld | 1248 | def | concrete world | ADMITTED |
| overwriteFirst | 1262 | def | destructive rewrite of first column | ADMITTED (countermodel) |
| owWorld | 1265 | def | concrete world | ADMITTED |
| stepHead | 1292 | def | head-picking mark semantics | ADMITTED (countermodel) |
| headWorldA / headWorldB | 1301 / 1305 | def | two replay-equivalent worlds | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| bool_eq_of_iff | 58 | Bools equal when their truth is equivalent | FROZEN | propext | A |
| or_not_eq_true | 62 | `(!a \|\| b) = true ↔ (a → b)` | FROZEN | propext | A |
| replay_deterministic | 208 | if w = w' then replay h w = replay h w' (proof: rw) | FROZEN (conclusion trivially true; docstring says definitional) | propext, Quot.sound | S (as a design statement) |
| replay_nil | 211 | replay [] w = w | FROZEN | propext, Quot.sound | A |
| replay_append | 213 | replay (h1 ++ h2) w = replay h2 (replay h1 w) | FROZEN | propext, Quot.sound | A |
| support_determines | 234 | supp w = supp w' → supp (step w e) = supp (step w' e), all e | FROZEN | propext, Quot.sound | S |
| internal_support | 292 | contrapositive of support_determines | FROZEN | propext, Quot.sound | A |
| notes_inert | 298 | one concrete instance: notes do not affect supp of successor | VERIFIED_FINITE | propext, Quot.sound | A |
| repairFamily_sound | 305 | member of family ⇒ in menu and repairsB | FROZEN | propext, Quot.sound | A |
| repairFamily_complete | 310 | in menu and repairsB ⇒ member | FROZEN | propext, Quot.sound | A |
| repairFamily_retains_ties | 317 | two accepted menu items are both in the family | FROZEN | propext, Quot.sound | S |
| sameElems_refl | 337 | reflexivity | FROZEN | not in artifact | A |
| sameElems_append | 340 | append one element preserves SameElems | FROZEN | not in artifact | A |
| sameElems_map | 353 | map preserves SameElems | FROZEN | not in artifact | A |
| any_congr | 364 | `any` respects SameElems | FROZEN | not in artifact | A |
| all_congr | 374 | `all` respects SameElems | FROZEN | not in artifact | A |
| satB_congr | 384 | WEquiv ⇒ equal satB | FROZEN | not in artifact | A |
| violB_congr | 388 | WEquiv ⇒ equal violB | FROZEN | not in artifact | A |
| sameElems_flatMap_menu | 397 | WEquiv ⇒ menus membership-equal | FROZEN | not in artifact | A |
| markApply_equiv | 409 | WEquiv preserved by markApply | FROZEN | not in artifact | A |
| preservesB_congr | 415 | congruence | FROZEN | not in artifact | A |
| dischargesSomeB_congr | 433 | congruence | FROZEN | not in artifact | A |
| markOkB_congr | 451 | congruence | FROZEN | not in artifact | A |
| increaseB_congr | 463 | congruence | FROZEN | not in artifact | A |
| augOkB_congr | 479 | congruence | FROZEN | not in artifact | A |
| repairsB_congr | 489 | congruence | FROZEN | not in artifact | A |
| obstructedB_congr | 494 | congruence | FROZEN | not in artifact | A |
| reqOkB_congr | 512 | congruence | FROZEN | not in artifact | A |
| equiv_step | 525 | WEquiv w w' → WEquiv (step w e) (step w' e) | FROZEN | propext, Quot.sound | S |
| equiv_replay | 571 | WEquiv preserved by replay of any history | FROZEN | propext, Quot.sound | S |
| equiv_repairFamily | 579 | WEquiv ⇒ repair families membership-equal | FROZEN | propext, Quot.sound | S |
| mark_discharges | 594 | markOkB ⇒ some recorded violation becomes satisfied | FROZEN | propext, Quot.sound | A |
| mark_preserves | 606 | markOkB ⇒ every satisfied recorded requirement stays satisfied | FROZEN | propext, Quot.sound | A |
| step_mark_sound | 620 | markOkB ∧ 0 < budget ⇒ step discharges a violation and preserves satisfied ones | CONDITIONAL: markOkB, 0 < budget (both explicit) | propext, Quot.sound | S |
| satB_aug | 652 | satB after augApply = old verdict ∨ new column's | FROZEN | propext, Quot.sound | S |
| aug_preserves_satisfied | 658 | satisfied stays satisfied under augApply | FROZEN | propext, Quot.sound | A |
| aug_increases | 665 | augOkB ⇒ some bounded off-diagonal pair separated by c and by no view | CONDITIONAL: augOkB | propext, Quot.sound | S |
| wf_genesis | 693 | WF genesis | FROZEN | none | A |
| wf_step | 697 | WF preserved by every step | FROZEN | propext, Quot.sound | A |
| wf_replay | 762 | WF (replay h genesis) for every h | FROZEN | propext, Quot.sound | S |
| represented_progress | 778 | WF w ∧ violB w (i,j) ⇒ repairFamily non-empty ∨ (obstructedB ∧ augOkB w [i] ∧ satB (augApply w [i]) (i,j)) | CONDITIONAL: WF (an invariant on replays) | propext, Quot.sound | S |
| progress_needs_budget | 868 | budget = 0 ⇒ mark is a no-op | FROZEN | propext, Quot.sound | S |
| progress_needs_license | 880 | augLicensed = false ⇒ addView is a no-op | FROZEN | propext, Quot.sound | S |
| violation_only_from_require | 895 | a violation after a step was already present or the event is a require | FROZEN | propext, Quot.sound | S |
| quiescent_stable | 966 | quiescent and e not a require ⇒ quiescent after e | FROZEN | propext, Quot.sound | S |
| admit_data_fresh | 1022 | admitting a fresh token appends it | FROZEN | propext, Quot.sound | A |
| histUpTo_prefix | 1029 | histUpTo k is a prefix of histUpTo (k+1) | FROZEN (about the supplied stream) | none | A |
| worldAt_data | 1035 | (worldAt k).data = range (k+1) | FROZEN (about the supplied stream) | propext, Quot.sound | S |
| worldAt_growth | 1067 | data length k+1 | FROZEN | propext, Quot.sound | A |
| productive_run | 1074 | prefix and strict carrier growth | FROZEN (about the supplied stream) | propext, Quot.sound | S |
| worldAt_three_quiescent | 1084 | quiescentB (worldAt 3) by decide | VERIFIED_FINITE | propext, Quot.sound | A |
| wit_all_lengths | 1093 | replicate n n is witValid for every n | FROZEN | propext, Quot.sound | S (countermodel half) |
| wit_no_infinite | 1107 | for every g : Nat → Nat some prefix is not witValid | FROZEN (g is metatheory) | propext, Quot.sound | S (countermodel half) |
| cert_scope | 1146 | certPosB ↔ panel non-empty ∧ every evaluator has a separating column | FROZEN | propext, Quot.sound | S |
| cert_not_correspondence | 1176 | a unanimous negative panel while an outside column separates (concrete) | REFUTED (refutes "certification = correspondence"), VERIFIED_FINITE | propext, Quot.sound | S |
| cert_panel_relative | 1182 | extending a panel turns certPosB from true to false (concrete) | REFUTED (refutes monotonicity), VERIFIED_FINITE | propext, Quot.sound | S |
| scheduler_hidden | 1210 | external scheduler bit changes the result (concrete) | REFUTED / VERIFIED_FINITE | propext, Quot.sound | S |
| gensym_hidden | 1219 | external seed changes the carrier (concrete) | REFUTED / VERIFIED_FINITE | propext, Quot.sound | S |
| oracle_hidden | 1238 | hidden oracle pushes through a rejected mark (concrete) | REFUTED / VERIFIED_FINITE | propext, Quot.sound | S |
| incomplete_search_false_alarm | 1255 | truncated menu declares obstruction; exhaustive check refutes; family non-empty (concrete) | REFUTED / VERIFIED_FINITE | propext, Quot.sound | S |
| augmentation_destroys_old_replay | 1273 | overwrite kills a satisfied requirement (concrete) | REFUTED / VERIFIED_FINITE | propext, Quot.sound | S |
| repetition_not_progress | 1283 | three admissions replay to one; lengths differ (concrete) | VERIFIED_FINITE | propext, Quot.sound | S |
| order_sensitivity_splits_equivalents | 1315 | headWorldA, headWorldB WEquiv yet stepHead gives different satB (concrete) | REFUTED / VERIFIED_FINITE | propext, Quot.sound | S |
| refusal_needs_certificate | 1338 | if a refuse event changes the world then obstructedB holds | FROZEN | propext, Quot.sound | S |
| refusals_are_represented | 1351 | after refuse, the pair is recorded or the step was a no-op | FROZEN | propext, Quot.sound | S |

Count check: 65 theorems listed; 48 in artifact, 17 congruence helpers (lines 337–520) not in artifact.

## 4. External and admitted assumptions

- Structures and declared policy: `World` with its `budget : Nat` and `augLicensed : Bool` fields; `Event` grammar; `sepB`/`satB` laws; `responseMenu`; the guards `reqOkB`, `markOkB`, `augOkB`, `obstructedB`; the history producer `histUpTo`. All are declared by the module header (lines 34–41) to be fixed metatheory ("they do not say the constitution derives itself").
- Budget and license are **unguarded**: `setBudget n` and `setAugLicense b` overwrite the fields with no acceptance check (lines 197–198; probe below confirmed). The gates `progress_needs_budget` / `progress_needs_license` are therefore real but trivially replenishable by whatever supplies the event stream; the stream `histUpTo` does exactly that (`setBudget 1` at every block). The paper calls budget and license "represented choices (evidence class: policy)". The constraint is honest but weak: no theorem bounds how often budget is replenished. (Constitution.lean's `budget_replenishment_represented` restates this as a feature.)
- Recurring hypotheses: `WF w` (proved invariant by `wf_replay`, so discharged on replays from genesis but required for arbitrary worlds); `markOkB`/`augOkB`/`0 < budget` where named.
- Library lemmas doing real work: `List.mem_filter`, `List.any_eq_true`, `List.all_eq_true`, `List.foldl_append`, `List.range_succ`, `List.eq_of_mem_replicate`; `decide` instances on `World` (derived `DecidableEq`).
- `Nat → X` functions treated as data: `histUpTo : Nat → List Event` (unbounded supplied stream), `prefixList g` with `g : Nat → Nat` (a metatheoretic "infinite source"), `worldAt : Nat → World`. None is internally available to the kernel; the module and paper say so for `histUpTo`. Finitude flags: the phrase "represented König failure" (line 1088, paper RP8) names a theorem quantified over Lean functions `Nat → Nat`; nothing in `World` represents such a function. The result is metatheoretic.
- Unearned identity: none found. Unrestricted external universe: `SameElems {α : Type}` is a universe-polymorphic helper only. Silently assumed observer: none found (views are data). Unspecified correspondence between presentations: `WEquiv` is declared, and the paper says admission order is semantic by declaration ("an established import of this development"). Cost function without justification: none (budget is a counter, not a cost). Admitted condition later described as forced: `responseMenu` is declared, and the map marks it DECLARED; `WF` is proved, not admitted. Finite computation presented as universal: `worldAt_three_quiescent` is k = 3 only, and the paper says the exhaustive check to 15 rounds is Python; see §11 on `notes_inert`.

## 5. Derived consequences

Imported by `Completion.lean` (builds `Stage` over `World`, transports `represented_progress` into `rule1_repair_or_extension`, proves `refusal_non_absorbing`), `NoOutside.lean` (`support_replay`, `certC_ceiling`, `panel_equiv` reuse `supp`, `step`, `certNegB`), `Horizon.lean` (uses `histUpTo`, `worldAt`, `blockEvents`, `quiescentB`, `WF`), and indirectly Constitution / Initiality / InterpreterBoundary. `represented_progress`, `step_mark_sound`, `support_determines`, `progress_needs_*`, `refusal_needs_certificate`, `incomplete_search_false_alarm`, `cert_scope`, `cert_not_correspondence` are rows of `paper/native_derivation_map.md` and nodes of `artifacts/completion_dependency_graph.json`.

## 6. Counterexamples and limitations

- Countermodels: `scheduler_hidden` (external tick bit), `gensym_hidden` (external seed), `oracle_hidden` (hidden evaluator), `order_sensitivity_splits_equivalents` (list-order tie-break, refutes invariance), `incomplete_search_false_alarm` (truncated menu, k = 1, on `truncWorld`), `augmentation_destroys_old_replay` (overwrite), `repetition_not_progress`, `wit_all_lengths` + `wit_no_infinite` (per-length witnesses with no compatible infinite source), `cert_not_correspondence`, `cert_panel_relative`. All are concrete `decide` witnesses except `wit_*`, which are general.
- Not proved: uniqueness or canonicity of the kernel; any self-derivation of the constitution; that budget replenishment is bounded; that `[i]` is the only augmentation (the paper scopes no-hidden-choice to `repairFamily` and says augmentation candidates are not a retained family); any statement about the Python 15-round exhaustive check (Lean has k = 3 only); minimality of the countermodels (ledger says "small, not proved minimal").
- `schedWorld` (line 1199) is a dead definition superseded by `schedWorld2`; harmless.
- `replay_deterministic` has a trivially true conclusion (it is `rw [hw]`); the docstring acknowledges this is the design point. A textbook should not present it as a theorem with content.

## 7. Axiom dependencies

All 48 artifact lines within {propext, Quot.sound}; probe confirmed five key theorems. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 48 of 65 theorems in `artifacts/lean_axioms.txt` (listed in `Derivation.lean` lines 314–361). Paper cites them in `paper/represented_progress.md`, ledger CL-RP-*, and `paper/native_derivation_map.md`. Probe run: `lake env lean .../probes/C/represented_probe.lean` (exit 0): `obsW` (two data, no views, requirement (0,1), budget 0, license false) has `violB`, empty `repairFamily`, `obstructedB`, `augOkB [0]` all true (second branch of `represented_progress` inhabited); `setBudget 5` and `setAugLicense true` take effect unguarded; `addView [0]` is a no-op at budget 0; `refuse 0 1` records the pair; `#print axioms` of five theorems = [propext, Quot.sound].

## 9. Related Python implementations

`code/derivation/represented.py` mirrors every definition (`World`, `sep`, `sat`, `viol`, `mark_ok`, `aug_ok`, `response_menu`, `repair_family`, `obstructed`, `step`, `replay`, `wf`, `hist_up_to`, `wit_valid`, `cert_pos`/`cert_neg`, all seven countermodel semantics, `mutation_report`); artifact `artifacts/represented.json`. Tests in `tests/test_represented.py` (replay determinism, pigeonhole story, ties, budget/license, refusal certificate, productivity to 15 rounds, König witnesses, certification scope, countermodels, mutation detection).

## 10. Textbook placement proposal

- Prerequisites: lists and membership; Bool-valued predicates and `decide`; what a replay (fold) is; the programme's notions of requirement, separation by a column, obstruction as exhaustive menu failure.
- Substantive: `World`/`Event`/`step`/`replay` (as the kernel), `support_determines`, `equiv_step`/`equiv_replay`/`equiv_repairFamily`, `repairFamily_retains_ties`, `step_mark_sound`, `satB_aug`/`aug_increases`, `wf_replay`, `represented_progress`, `progress_needs_budget`/`progress_needs_license`, `violation_only_from_require`/`quiescent_stable`, `refusal_needs_certificate`/`refusals_are_represented`, `cert_scope`/`cert_not_correspondence`/`cert_panel_relative`, and the eight countermodels.
- Auxiliary: the 17 congruence lemmas, `bool_eq_of_iff`, `or_not_eq_true`, `mark_discharges`/`mark_preserves`, `admit_data_fresh`, `worldAt_growth`, `notes_inert`.
- Lesson title: "A kernel with no outside: what must be in the state for progress to be replayable?" The one question: if every input to a transition is in the state or the history, what does the progress rule look like, and what exactly do budget, license and refusal do?
- Omit from the textbook: `schedWorld` (dead), `replay_deterministic` as a theorem (present it as a remark on the type of `step`); treat `histUpTo` as a worked example, not as an internal object.

## 11. Interpretation findings

1. `wit_no_infinite` / module section title "Countermodel 8 — ... (a represented König failure)" (line 1087–1088) and paper RP8 "the represented König failure". Lean: `∀ g : Nat → Nat, witValid (prefixList g (g 0 + 1)) = false`. The "infinite source" is a Lean function; `World` carries no such object and no event supplies one. The theorem is correct and metatheoretic. Classification: INTERPRETATION DEFECT (mild): the adjective "represented" attaches to the countermodel's conclusion, not to its quantifier. The ledger CL-RP-PRODUCTIVITY phrases it as "the represented König failure" too.
2. `notes_inert` docstring: "The transition-inert field really is inert: worlds differing only in `notes` have support-equal successors (concrete instance)." The theorem is one `decide` instance (genesis with notes [7], event admitTok 3). The general statement is `support_determines` (notes are the only field outside `supp`), so the general claim is proved elsewhere; the docstring says "concrete instance". No defect, noted for the textbook: cite `support_determines` for generality.
3. `progress_needs_budget` / paper "Progress is conditional on represented resources, never free." Lean proves the gate; nothing bounds `setBudget`. The budget is represented and the gate is real, but the resource is supplied by the stream at will. Classification: INTERPRETATION DEFECT (mild): "never free" is true of a single step, not of a run whose stream may insert `setBudget` before every repair; the paper's own ceiling ("budget and license are represented choices") covers it, so no overclaim in the ledger, but a reader of the map row "budget gates same-level repair" should be told the gate is replenishable without a guard.
4. `represented_progress` second disjunct: non-vacuous (probe). Hypotheses jointly satisfiable. No vacuity found in any theorem.
5. `replay_deterministic`: conclusion trivially true (`rw`); the docstring and paper say so ("the kernel's type is the theorem"). Not a defect; flagged so the textbook does not present it as content.
