# Audit: Completion

| field | value |
|---|---|
| Path | lean4/Derivation/Completion.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f1ee7fda1304d3e6 |
| Lines | 529 |
| Imported by root `Derivation.lean` | yes (line 24) |
| Imports | Derivation.Represented, Derivation.RefusalFrontier |
| Declarations | 1 structure, 13 def, 22 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 22 lines; axioms seen: none / propext / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Stage II of the native-closure investigation builds one common state, `CommonState`, that keeps the distinctions the programme refuses to erase as literally separate fields: the admitted carrier (positions are occurrence identities), metatheoretic inequality facts, positive witnessed difference (relation instances), observation columns (the only source of observer-relative difference), retained and protected requirements, budget, license, and refusal records. "Transport" theorems map the represented kernel (`World`), the reflective chain (`PState`), and the two-element difference objects into this state and prove what each preserves; the failures of transport are stated as theorems too (a positive witness is not observer separation; separation is not a witness; metatheoretic inequality moves nothing). Stage III settles Rule 1 ("resolve the obstruction or create structure") for the fixed kernel: under well-formedness and a recorded violation, either the same-level repair family is non-empty or the exhaustion certificate holds and both orientation-canonical augmentations are accepted; refusal is shown to be a parallel record that touches no object field and changes no acceptance verdict; every event either preserves the presentation signature or strictly grows it; with no protected requirement there is no obstruction at all. These theorems are the Lean sources behind several PROVED and FALSE rows of the dependency map (`paper/native_derivation_map.md`), whose status taxonomy is PROVED / DECLARED / FALSE_WITH_COUNTERMODEL / OPEN.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| CommonState | 41 | structure | carrier, metaDistinct, posWitness, views, retained, protectedReqs, budget, licensed, refusals | ADMITTED (declared common interface) |
| sepC | 54 | def | some view column separates i, j (reads only `views`) | ADMITTED (observation law) |
| zeroC | 59 | def | negation of sepC: the observer sees no difference | ADMITTED |
| obstC | 67 | def | retained ∧ protected ∧ zeroC: the three-condition active obstruction | ADMITTED (declared obstruction notion) |
| ofWorld | 73 | def | transport of a kernel `World`; sets both `retained` and `protectedReqs` to `w.reqs`, empties metaDistinct/posWitness | ADMITTED (a stated identification of retention with protection) |
| ofPState | 135 | def | transport of a RefusalFrontier `PState`: posWitness := rel, views := [tags] | ADMITTED |
| swapIdx | 165 | def | the transposition 0 ↔ 1 on indices | ADMITTED |
| swapC | 167 | def | apply swapIdx to posWitness, views, retained, protectedReqs (not carrier, not metaDistinct) | ADMITTED |
| d2Common | 175 | def | two-element oriented object: posWitness [(0,1)], retained and protected [(0,1)], no views | ADMITTED |
| s2Common | 181 | def | d2Common with posWitness [(0,1),(1,0)] | ADMITTED |
| tagOnly | 219 | def | two-element state with one view [0] and no witness | ADMITTED |
| augFamily | 264 | def | `[[r.1],[r.2]].filter (augOkB w)`: both orientation-canonical singleton columns, filtered | ADMITTED (declared extension family) |
| sigOf | 443 | def | presentation signature (carrier length, view count) | ADMITTED (declared measure) |
| retractFirstMark | 514 | def | countermodel semantics: drop the head of the first view | ADMITTED (countermodel) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| ofWorld_sep | 84 | sepC (ofWorld w) i j = satB w (i,j), by rfl | FROZEN | propext, Quot.sound | S |
| ofWorld_obstruction | 87 | obstC (ofWorld w) i j = violB w (i,j) | FROZEN | propext, Quot.sound | S |
| obstC_conditions_independent | 95 | three concrete states each missing one condition fail obstC; the state with all three succeeds | VERIFIED_FINITE (four 2-element states) | propext, Quot.sound | S |
| ofWorld_quiescent | 115 | "all reqs not obstC in ofWorld w" = "all reqs not violB" | FROZEN | propext, Quot.sound | A |
| chain_transport | 147 | for every n, ofPState (reflState n) has carrier range (n+1) and posWitness the successor edges | FROZEN (relies on RefusalFrontier.reflective_chain_is_initial_segment / _successor_relation) | propext | S |
| d2_transport_oriented | 184 | swapC d2Common ≠ d2Common | VERIFIED_FINITE | none | S |
| s2_transport_symmetric | 189 | swapC s2Common keeps posWitness length and membership of (0,1) and (1,0) | VERIFIED_FINITE | propext, Quot.sound | S |
| s2_state_not_swap_invariant | 200 | swapC s2Common ≠ s2Common | VERIFIED_FINITE / REFUTED (refutes whole-state symmetry) | none | S |
| witness_not_separation | 213 | (0,1) ∈ d2Common.posWitness ∧ zeroC d2Common 0 1 | VERIFIED_FINITE / REFUTED (refutes witness ⇒ separation) | propext, Quot.sound | S |
| separation_not_witness | 224 | sepC tagOnly 0 1 ∧ tagOnly.posWitness = [] | VERIFIED_FINITE / REFUTED (refutes separation ⇒ witness) | propext, Quot.sound | S |
| meta_distinctness_inert | 231 | changing metaDistinct changes neither sepC nor obstC (both rfl) | FROZEN (definitional: neither reads the field) | propext, Quot.sound | S |
| early_collapse_transports | 241 | zeroC of a two-element state with no views is true | VERIFIED_FINITE (conclusion holds for any state with no views) | propext, Quot.sound | A |
| augFamily_sound | 267 | member of augFamily ⇒ augOkB | FROZEN | propext, Quot.sound | A |
| sepB_symm | 271 | sepB c i j = sepB c j i | FROZEN | propext, Quot.sound | A |
| augFamily_retains_ties | 279 | WF w ∧ violB w (i,j) ⇒ [i] and [j] both in augFamily w (i,j) | CONDITIONAL: WF | propext, Quot.sound | S |
| rule1_repair_or_extension | 362 | WF w ∧ violB w (i,j) ⇒ repairFamily non-empty ∨ (obstructedB ∧ [i],[j] ∈ augFamily) | CONDITIONAL: WF | propext, Quot.sound | S |
| refusal_recordable | 393 | obstructedB w (i,j) ⇒ (i,j) ∈ refusals after refuse | CONDITIONAL: obstructedB | propext, Quot.sound | S |
| refusal_object_inert | 416 | refuse leaves data, views, reqs, budget, license unchanged | FROZEN | propext, Quot.sound | S |
| refusal_non_absorbing | 428 | refuse leaves satB, violB, markOkB, augOkB verdicts unchanged | FROZEN | propext, Quot.sound | S |
| action_dichotomy | 445 | every step keeps sigOf or strictly increases carrier length or view count | FROZEN | propext, Quot.sound | S |
| rule1_needs_fidelity | 496 | reqs = [] ⇒ violB and obstructedB false for every r | CONDITIONAL: w.reqs = [] (the hypothesis is the point) | propext, Quot.sound | S |
| retraction_breaks_preservation | 520 | a concrete world is satisfied; after retractFirstMark it is not | VERIFIED_FINITE / REFUTED (refutes "same-level ⇒ preserving") | propext, Quot.sound | S |

Count check: 22 theorems, all in the artifact.

## 4. External and admitted assumptions

- `CommonState` is a declared interface; nothing derives its field list. `obstC` is a declared conjunction. The kernel transport `ofWorld` identifies retention with protection (both := `w.reqs`); the source, ledger CL-NC-COMMON-STATE and `pr11_correction_ledger.md` §C1 all disclose this.
- From RefusalFrontier: `PState`, `reflState`, and the two chain theorems (`reflective_chain_is_initial_segment`, `reflective_chain_successor_relation`) do the work in `chain_transport`; `reflState : Nat → PState` is a Nat-indexed metatheoretic constructor (RefusalFrontier's own docstring: "under an explicitly supplied constructor").
- From Represented: `WF`, `violB`, `obstructedB`, `repairFamily`, `repairFamily_complete`, `augOkB`, `step`. Hypothesis `WF` recurs; it is discharged on replays by `Represented.wf_replay`.
- Library lemmas: `List.mem_filter`, `List.any_eq_true`, `List.all_eq_true`, `List.length_map/append`, `decide` on `CommonState` and `World`.
- Unearned identity: the retention/protection identification in `ofWorld` is earned only by disclosure (stated identification), not by theorem; flagged, already disclosed. Unrestricted external universe: none. Unbounded function treated as internally available: `reflState` and `chain_transport`'s ∀ n are metatheory; the paper calls the chain "horizon-free", which is a statement about the Lean quantifier, not about an object the system holds. Silently assumed observer: none (views are data). Unspecified correspondence between presentations: `swapC` is the declared common form of the transposition and does not act on `carrier` or `metaDistinct` (so `d2_transport_oriented` is partly a fact about which fields swap touches). Cost function: `sigOf` is a declared measure for `action_dichotomy`. Admitted condition later described as forced: none found. Finite computation presented as universal: `s2_transport_symmetric` is three `decide` facts about one concrete state, and the prose ("the relation store is swap-invariant as a set of instances") matches that scope.

## 5. Derived consequences

`Constitution.lean` uses `augFamily` (in `closeBlocks`) and cites `rule1_repair_or_extension`; `PrimitivePassage.lean` cites `refusal_object_inert` alongside its own refusal/terminal separation. Map rows: "active obstruction → same-level repair (dichotomy)" PROVED via `rule1_repair_or_extension`; "refusal terminalizes the run" FALSE via `refusal_non_absorbing`; "exhaustion certificate forces extension proposal" PROVED (tied family, both orientations). Ledger entries CL-NC-COMMON-STATE and CL-NC-RULE1.

## 6. Counterexamples and limitations

- Countermodels: `obstC_conditions_independent` (each of the three conditions is necessary), `s2_state_not_swap_invariant`, `witness_not_separation`, `separation_not_witness`, `retraction_breaks_preservation`. All are concrete two-element `decide` witnesses.
- Not proved: that `CommonState` is the right or the only common state; any transport of the full early `Regime` (the docstring at 236–240 says that goes through the token-erased simulation and is "recorded in the map, not erased here"); that `augFamily` exhausts all accepted augmentations (it contains exactly the two singleton candidates — a declared family, not a closure of all `augOkB` columns); any statement about refusal under a semantics other than the kernel's `step`.
- `early_collapse_transports` is a sanity instance: `zeroC` is true on every pair whenever `views = []`, so the theorem carries no information beyond "no views, no separation". Not a defect; it should not be taught as a transport theorem.
- `rule1_repair_or_extension` is the renamed `rule1_trichotomy`; the paper (`pr11_correction_ledger.md` §C4) records that no trichotomy is claimed.

## 7. Axiom dependencies

All 22 within {propext, Quot.sound}; `d2_transport_oriented` and `s2_state_not_swap_invariant` use none. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 22 theorems in the artifact (root inventory lines following the Represented block). Paper cites every theorem (ledger CL-NC-COMMON-STATE, CL-NC-RULE1; `paper/native_derivation_completion.md` §5, §7, §18; `pr11_correction_ledger.md` C1–C4). No probe run beyond reading; `decide` theorems are kernel-checked by the build.

## 9. Related Python implementations

`code/derivation/completion.py` is mainly the inventory/classification generator for `artifacts/completion_dependency_graph.json` (`classify`, `inventory`, `dependency_graph`), not a mirror of `CommonState`; its `aug_family(w, r)` (line 1219) mirrors `augFamily`. `tests/test_completion.py::test_close_family_complete_and_tie_retained` and `test_dependency_graph_statuses_and_evidence_resolve` exercise them. No Python mirror of `CommonState`, `ofWorld`, `swapC` found.

## 10. Textbook placement proposal

- Prerequisites: the Represented kernel (World, step, violB, obstructedB, repairFamily, WF); the RefusalFrontier reflective chain; the two-element oriented/symmetric objects from PrimDiff.
- Substantive: `CommonState`/`obstC` (the three-condition obstruction), `ofWorld_obstruction`, `obstC_conditions_independent`, `witness_not_separation`/`separation_not_witness`, `augFamily_retains_ties`, `rule1_repair_or_extension`, `refusal_recordable`/`refusal_object_inert`/`refusal_non_absorbing`, `action_dichotomy`, `rule1_needs_fidelity`, `retraction_breaks_preservation`.
- Auxiliary: `ofWorld_sep`, `ofWorld_quiescent`, `augFamily_sound`, `sepB_symm`, `chain_transport`, `early_collapse_transports`, the d2/s2 swap facts (a remark).
- Lesson title: "Rule 1 in a fixed kernel: repair, or certified exhaustion plus a tied extension family — and why refusal is a record, not a third option."
- Omit: `early_collapse_transports` (information-free), `ofWorld_quiescent` (a restatement of `ofWorld_obstruction`).

## 11. Interpretation findings

1. `ofWorld` / ledger CL-NC-COMMON-STATE "retention, protection, and observer-zero as three independent obstruction conditions". In the common state they are independent fields (proved by `obstC_conditions_independent`); in the kernel transport they are the same store. The ledger says so in the same sentence ("the kernel transport instantiates retention and protection from one store — a stated identification"). No defect; the textbook must keep the two scopes apart.
2. `s2_transport_symmetric` docstring "the relation store is swap-invariant as a set of instances". The Lean proves length preservation plus membership of the two specific pairs (0,1) and (1,0), on one concrete state. That is set-equality for this two-element store, so the statement is faithful at that instance; it is not a general lemma about `swapC` on any symmetric store. Classification: none (scope stated as "scoped exactly").
3. `early_collapse_transports` docstring "the Challenge-2 situation in common form". Conclusion trivially true for every viewless state. Classification: INTERPRETATION DEFECT (mild, vacuity-adjacent): the theorem does not transport anything from the early `Regime`; it only exhibits that `zeroC` is true with no views. The docstring itself concedes the real transport is elsewhere.
4. `rule1_repair_or_extension` / map row "active obstruction | dichotomy (refusal parallel) | same-level repair | PROVED | conditional on WF and constitution". Faithful: hypotheses WF and violB are named; WF is an invariant of replay.
5. Vacuity: no theorem with jointly unsatisfiable hypotheses found; `rule1_needs_fidelity` takes `w.reqs = []` deliberately and its conclusion is then immediate — it is a remark, correctly labelled "fidelity reduction".
