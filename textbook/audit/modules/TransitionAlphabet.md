# Audit: TransitionAlphabet

| field | value |
|---|---|
| Path | lean4/Derivation/TransitionAlphabet.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 3a880489778eecf2 |
| Lines | 1893 (`wc -l`; inventory.json counts 1894) |
| Imported by root `Derivation.lean` | yes (line 45; `#print axioms` inventory present) |
| Imports | `Derivation.PrimitivePassage` (transitively `PrimDiff`, `PrimitiveCore`) |
| Declarations | 54 def, 5 structure (`FieldDelta`, `Profile`, `ClassSig`, `EffectSig`, `WFClass`), 7 inductive (`ObstEffect`, `ObstMove`, `GuardKind`, `BudgetDelta`, `Continuity`, `Origin`, `EffectClass`), 118 theorem (116 public + 2 `private`: `hfalse`, `hlive`) |
| Axiom reports in `artifacts/lean_axioms.txt` | 116 lines (every public theorem); axioms seen: `propext, Quot.sound` (most), `propext` only, `none` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module works on the passage dynamics of `PrimitivePassage` (`PState`, `PEvent`, `step`, `replayP`), **not** on the regime model of `Basic.lean`; no `Regime`, `Inst` or `stepE` appears. It asks: when an event is attempted at a state, is the transition accepted (does it move the represented state), and if so, what is the one-step *effect* in a declared finite vocabulary? It proves that acceptance is decided exactly by a per-constructor guard (`accepted_eq_guardHolds`), computes for each accepted transition a profile (nine field-change flags, discharged guard, what happened to the actively obstructed pairs, budget delta, continuation/absorption, a constructor policy label), and shows that on the declared well-formed class `WFClass` (live, protection ⊆ retention) every accepted transition realizes exactly one of thirteen declared class signatures (`exists_unique_class`). It then limits its own result: the signature is not a right congruence for sequential composition (two common-suffix countermodels), so codes never replace raw events and states in replay; two profile components are provably not transition invariants; refinement and extension have identical guard-erased effect (twelve codes after erasure) and differ only in acceptance domain. Finally it refutes a premise about the internal response generator: `nextFamilyP` emits `setBudget 1`, an event the policy table labels `environment`, so the `Origin` label is not provenance.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Accepted` | 78 | def | `decide (step s e ≠ s)`: the transition moves the state | ADMITTED |
| `occS`, `assS`, `witS`, `protS`, `obsS`, `refineS`, `colS`, `refuseS`, `budS`, `licS`, `haltS` | 104–127 | def | the eleven named post-states, one record update each | ADMITTED |
| `guardHolds` | 170 | def | the computed per-constructor acceptance condition | ADMITTED (declared; its agreement with `Accepted` is a theorem) |
| `ObstEffect` | 580 | inductive | created / preserved / removed / untouched | ADMITTED (declared classifier; ordered: `removed` wins) |
| `ObstMove` | 589 | inductive | creates / removes / inert | ADMITTED |
| `coarse` | 595 | def | `ObstEffect → ObstMove`, merging preserved/untouched | ADMITTED (declared projection) |
| `gainedPairs`, `lostPairs` | 601, 604 | def | list differences of `obstructedPairs` before/after | ADMITTED |
| `obstEffect` | 607 | def | the four-way classifier from the two difference lists | ADMITTED |
| `FieldDelta` | 906 | structure | nine Bool flags, one per `PState` field | ADMITTED |
| `fieldDelta` | 918 | def | which fields differ between two states | ADMITTED |
| `fdOcc` … `fdHalted` | 929–948 | def (10) | the ten single/double-field change patterns | ADMITTED |
| `GuardKind` | 1028 | inductive | eleven guard names, one per constructor | ADMITTED (declared label) |
| `guardOf` | 1042 | def | constructor → `GuardKind` | ADMITTED |
| `BudgetDelta` | 1055 | inductive | unchanged / spentOne / rewritten | ADMITTED |
| `budgetDeltaOf` | 1061 | def | compares budgets (`t+1 = s` read as spentOne) | ADMITTED |
| `Continuity` | 1066 | inductive | continuation / absorption | ADMITTED |
| `continuityOf` | 1071 | def | reads `halted` of the post-state | ADMITTED |
| `Origin` | 1092 | inductive | environment / internal | ADMITTED (declared **policy label**, explicitly not provenance) |
| `originOf`, `isEnvOwned` | 1097, 1104 | def | the policy table (admitOcc, setBudget, setLicense, halt = environment) | ADMITTED (declared policy) |
| `Profile` | 1117 | structure | fields, guard, obst, budget, cont, origin, accepted | ADMITTED |
| `profileOf` | 1127 | def | the computed profile of an attempt | ADMITTED |
| `ClassSig` | 1142 | structure | fields, guard, move, cont, origin (budget delta and the 4-way split dropped) | ADMITTED (declared projection) |
| `sigOf` | 1150 | def | computed class signature | ADMITTED |
| `EffectSig` | 1159 | structure | `ClassSig` with the guard erased | ADMITTED |
| `eraseGuard`, `effectSigOf` | 1166, 1169 | def | the erasure and its composite | ADMITTED |
| `WFClass` | 1180 | structure (Prop) | `halted = false` and `∀ p ∈ prot, p ∈ wit` | ADMITTED (declared class; shown replay-invariant) |
| `wfB` | 1184 | def | Bool form of `WFClass` | ADMITTED |
| `wAssert`, `wRetain`, `wProtectQuiet`, `wProtectObstructing`, `wDeclareObstructing`, `wObstructed`, `wFunded`, `wRefine`, `wFundedUnlicensed`, `wRefineUnlicensed` | 1239–1287 | def (10) | concrete two-occurrence witness states | ADMITTED (finite witnesses) |
| `outsideClass` | 1293 | def | a pair protected but not retained; outside `WFClass` | ADMITTED (countermodel state) |
| `EffectClass` | 1308 | inductive | the thirteen declared codes | ADMITTED (declared table) |
| `classSig` | 1324 | def | code → signature table | ADMITTED (declared) |
| `classOf` | 1352 | def | which code an attempt gets (`protect`/`declareObs` split by pre-state) | ADMITTED |
| `dedup` | 1592 | def | duplicate removal on a `DecidableEq` list | ADMITTED (metatheory helper) |
| `allClasses` | 1596 | def | the list of all thirteen codes | ADMITTED |
| `sizeP` | 1822 | def | a size measure on states (sum of list lengths + budget + obs size) | ADMITTED (declared metric, used only to report witness sizes) |

## 3. Theorems and lemmas

Hypothesis abbreviations: **L** = `s.halted = false`; **WF** = `WFClass s`; **PSW** = `∀ p ∈ s.prot, p ∈ s.wit`; **Acc** = `Accepted s e = true`.

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `accepted_true_iff` | 80 | `Accepted s e = true ↔ step s e ≠ s` | FROZEN | propext, Quot.sound | A |
| `accepted_false_iff` | 84 | `Accepted s e = false ↔ step s e = s` | FROZEN | propext, Quot.sound | A |
| `halted_accepts_nothing` | 91 | if `s.halted = true` then no event is accepted at `s` | CONDITIONAL:`s.halted = true` | propext, Quot.sound | S |
| `halt_inert_on_halted` | 97 | on a halted state `halt` is inert and not accepted | CONDITIONAL:`s.halted = true` | propext, Quot.sound | A |
| `append_ne` | 129 | `l ++ [a] ≠ l` | FROZEN (metatheory) | propext, Quot.sound | A |
| `occS_ne`, `assS_ne`, `witS_ne`, `protS_ne`, `refuseS_ne` | 135–147 | each append post-state differs from `s` | FROZEN | propext, Quot.sound | A |
| `obsS_ne` | 149 | if `s.obs = none` then `obsS s ≠ s` | CONDITIONAL:`s.obs = none` | propext | A |
| `budS_ne` | 155 | if `n ≠ s.budget` then `budS s n ≠ s` | CONDITIONAL:`n ≠ s.budget` | none | A |
| `licS_ne` | 158 | if `b ≠ s.licensed` then `licS s b ≠ s` | CONDITIONAL:`b ≠ s.licensed` | none | A |
| `haltS_ne` | 161 | if live then `haltS s ≠ s` | CONDITIONAL:L | none | A |
| `refineS_ne`, `colS_ne` | 167, 175 | if `0 < s.budget` the funded post-states differ from `s` | CONDITIONAL:`0 < s.budget` | propext, Quot.sound | A |
| `refineOk_declared`, `colOk_declared` | 196, 202 | an accepted refine/col guard implies `s.obs = some cols` | CONDITIONAL:guard true | propext, Quot.sound | A |
| `hfalse`, `hlive` | 208, 210 | private Bool helpers | FROZEN (private) | not in artifact | A |
| `step_admitOcc_acc` / `_inert` | 213, 219 | under L and `t ∉ s.occ` / `t ∈ s.occ`, `step` equals `occS` / `s` | CONDITIONAL:L + guard | propext, Quot.sound | A |
| `step_assertWit_acc` / `_inert` | 224, 231 | under L and the Bool guard true/false, `step` is `assS`/`s` | CONDITIONAL:L + guard | propext, Quot.sound | A |
| `step_admitWit_acc` / `_inert` | 239, 247 | same pattern for retention | CONDITIONAL:L + guard | propext, Quot.sound | A |
| `step_protect_acc` / `_inert` | 255, 262 | same pattern for protection | CONDITIONAL:L + guard | propext, Quot.sound | A |
| `step_declareObs_acc` / `_inert` | 269, 275 | under L, `obs = none` gives `obsS`, `obs = some _` is inert | CONDITIONAL:L + obs case | propext, Quot.sound | A |
| `step_refineCol_acc` / `_inert` | 281, 290 | under L, declared obs, `refineOk`, budget>0: `step = refineS`; guard false: inert | CONDITIONAL:L + guard | propext, Quot.sound | A |
| `step_addCol_acc` / `_inert` | 297, 306 | same pattern with license | CONDITIONAL:L + guard | propext, Quot.sound | A |
| `step_refuse_acc` / `_inert` | 313, 320 | same pattern for refusal | CONDITIONAL:L + guard | propext, Quot.sound | A |
| `step_setBudget_live`, `step_setLicense_live` | 327, 332 | under L, the writes always install `budS`/`licS` (possibly equal to `s`) | CONDITIONAL:L | propext, Quot.sound | A |
| `step_halt_eq` | 338 | `step s .halt = haltS s` (rfl) | FROZEN | propext, Quot.sound | A |
| `accepted_eq_guardHolds` | 344 | for all `s`, `e`: `Accepted s e = guardHolds s e` | FROZEN | propext, Quot.sound | S |
| `filter_notmem_eq_nil`, `filter_congr_mem`, `filter_all_true`, `filter_all_false`, `list_ne_nil_of_mem`, `isEmpty_not_of_ne` | 524–566 | List lemmas (metatheory, so labelled in the source) | FROZEN | propext / none | A |
| `obstructedPairs_sub`, `obst_of_mem_obstructedPairs`, `mem_obstructedPairs` | 613–623 | membership characterization of `obstructedPairs` | FROZEN | propext, Quot.sound | A |
| `lost_nil_of_eq`, `gained_nil_of_eq`, `obstMove_inert_of_eq` | 626–643 | equal obstructed lists give empty differences and `inert` | CONDITIONAL:`obstructedPairs t = obstructedPairs s` | propext, Quot.sound | A |
| `obstEffect_split_of_inert` | 653 | with equal obstructed lists: `untouched` iff pre-list empty, `preserved` iff nonempty | CONDITIONAL:equal lists | propext, Quot.sound | S |
| `obstructedPairs_eq_of_stores` | 670 | equal `wit`, `prot`, `obs` give equal obstructed lists | CONDITIONAL:three store equalities | propext, Quot.sound | A |
| `obstructedPairs_occS/assS/refuseS/budS/licS/haltS` | 682–717 | these post-states leave the obstructed list unchanged | FROZEN | propext, Quot.sound | A |
| `obstructedPairs_witS` | 723 | under PSW, retention leaves the obstructed list unchanged | CONDITIONAL:PSW | propext, Quot.sound | S |
| `obstructedPairs_protS` | 738 | protection appends `(i,j)` to the list iff it is obstructed afterwards | FROZEN | propext, Quot.sound | S |
| `obstructedPairs_obsS` | 758 | under `obs = none` and PSW: after declaring, obstructed = `prot`; before, empty | CONDITIONAL:`obs = none`, PSW | propext, Quot.sound | S |
| `sepP_append`, `zeroP_append_mono` | 781, 787 | appending a column can only add separation / only remove zero | FROZEN | propext, Quot.sound | A |
| `obstructedPairs_colS_sub`, `colS_lost_ne_nil`, `obstEffect_colS` | 796, 813, 841 | under declared obs (+ `colOk`): extension loses an obstructed pair and gains none; effect `removed` | CONDITIONAL:`s.obs = some cols`, `colOk s c = true` | propext, Quot.sound | S |
| `mem_map_refine`, `obstructedPairs_refineS_sub`, `refineS_lost_ne_nil`, `obstEffect_refineS` | 848–898 | same for refinement under `refineOk` | CONDITIONAL:`s.obs = some cols`, `refineOk s v p = true` | propext, Quot.sound | S |
| `bne_true_of_ne`, `map_replace_ne` | 950, 955 | Bool helper; refining a present column changes the list | FROZEN / CONDITIONAL:`v ∈ cols` | propext, Quot.sound | A |
| `fieldDelta_occS … fieldDelta_colS` | 970–1024 | each post-state's field delta is the expected single/double pattern (with the inequality hypotheses that make the post-state differ) | CONDITIONAL:per-case (e.g. `n ≠ s.budget`, `0 < s.budget`, `v ∈ cols`) | propext, Quot.sound | A |
| `continuityOf_live`, `continuityOf_halted` | 1074, 1078 | continuity reads `halted` | CONDITIONAL:halted value | none | A |
| `isEnvOwned_iff_origin` | 1111 | the Bool and inductive policy labels agree | FROZEN | propext | A |
| `wf_of_wfB` | 1187 | `wfB s = true → WFClass s` | CONDITIONAL:`wfB s = true` | propext, Quot.sound | A |
| `protSubWit_step` | 1193 | PSW is preserved by every `step` | CONDITIONAL:PSW | propext, Quot.sound | S |
| `protSubWit_replay` | 1213 | every replay from `genesisP` satisfies PSW | FROZEN (over all event lists) | propext, Quot.sound | S |
| `wf_of_replay` | 1228 | a live replay from genesis is in `WFClass` | CONDITIONAL:replayed state live | propext, Quot.sound | S |
| `sig_eq_classSig` | 1375 | under WF and Acc, `sigOf s e = classSig (classOf s e)` | CONDITIONAL:WF, Acc | propext, Quot.sound | S |
| `classSig_inj` | 1580 | `classSig` is injective on the 13 codes | VERIFIED_FINITE (`decide` over 13×13) | none | S |
| `classSig_pairwise_distinct` | 1584 | contrapositive of the above | VERIFIED_FINITE | none | A |
| `exists_unique_class` | 1589 | under WF and Acc there is exactly one code whose signature is `sigOf s e` | CONDITIONAL:WF, Acc | propext, Quot.sound | S |
| `allClasses_complete` | 1603 | every code is in `allClasses` | VERIFIED_FINITE | propext | A |
| `declared_codebook_size` | 1607 | `dedup (allClasses.map classSig)` has length 13 | VERIFIED_FINITE | propext | S |
| `guard_erased_codebook_size` | 1614 | after `eraseGuard`, length 12 | VERIFIED_FINITE | propext | S |
| `classSig_not_right_congruent_occurrence` | 1622 | at genesis `admitOcc 0`, `admitOcc 2` accepted with equal signatures, yet suffix `admitOcc 0` separates the results | REFUTED (countermodel, `decide`) | propext, Quot.sound | S |
| `classSig_not_right_congruent_budget` | 1634 | from `budS wObstructed 2`, `setBudget 0`/`setBudget 1` have one code; suffix `addCol [0]` separates | REFUTED (countermodel, `decide`) | propext, Quot.sound | S |
| `refine_addCol_effect_merge` | 1647 | any accepted refinement at a WF state and any accepted extension at a WF state have equal guard-erased signatures | CONDITIONAL:WF×2, Acc×2 | propext, Quot.sound | S |
| `refine_addCol_domain_countermodel` | 1660 | at `wRefineUnlicensed` refinement is accepted, at `wFundedUnlicensed` extension is not, at `wFunded` it is | VERIFIED_FINITE | propext, Quot.sound | S |
| `preserved_untouched_not_invariant` | 1669 | `admitOcc` yields `untouched` at genesis and `preserved` at `wObstructed`, both accepted | REFUTED (the split is not a transition invariant) | propext, Quot.sound | S |
| `budgetDelta_not_invariant` | 1679 | `setBudget 3` at genesis is `rewritten`; `setBudget 1` at budget 2 is `spentOne` | REFUTED (budget delta not an invariant of the constructor) | propext, Quot.sound | S |
| `budgetDelta_of_funded_guard` | 1686 | under WF, Acc and guard ∈ {refinement, column}: budget delta is `spentOne` | CONDITIONAL:WF, Acc, guard kind | propext, Quot.sound | S |
| `refuse_preserves` | 1729 | under WF and accepted `refuse i j`: effect is `preserved` | CONDITIONAL:WF, Acc | propext, Quot.sound | S |
| `retention_creates_outside_class` | 1750 | `outsideClass` fails `wfB`, accepts `admitWit 0 1`, and that step `creates` an obstruction | VERIFIED_FINITE (countermodel to dropping PSW) | propext, Quot.sound | S |
| `nextFamily_block_shape` | 1758 | every block of `nextFamilyP s` is `[refineCol m]` or `[setBudget 1, addCol c]` | FROZEN | propext, Quot.sound | S |
| `internal_family_no_occurrence_supply`, `_no_license_write`, `_no_terminal` | 1769–1781 | no block of `nextFamilyP s` contains `admitOcc t` / `setLicense x` / `halt` | FROZEN | propext, Quot.sound | S |
| `internal_family_emits_budget_write` | 1789 | `[setBudget 1, addCol [0]] ∈ nextFamilyP wObstructed` | VERIFIED_FINITE (refutation witness) | propext, Quot.sound | S |
| `env_ownership_claim_refuted` | 1793 | ∃ state, block, event with the block in the family and the event env-owned | REFUTED | propext, Quot.sound | S |
| `internal_family_env_only_unit_funding` | 1803 | an env-owned event in a family block is `setBudget 1` | FROZEN | propext, Quot.sound | S |
| `nonEnv_preserves_occ_licensed` | 1818 | a non-env event never changes `occ` or `licensed` | CONDITIONAL:`isEnvOwned e = false` | propext, Quot.sound | S |
| `class_witnesses` | 1829 | thirteen concrete (state, event) pairs: in `wfB`, accepted, with the tabulated signature | VERIFIED_FINITE | propext, Quot.sound | S |
| `class_witness_sizes` | 1865 | `sizeP` of nine witness states | VERIFIED_FINITE | none | A |

## 4. External and admitted assumptions

- **Base model.** `PState`/`PEvent`/`step`/`replayP`/`obstP`/`obstructedPairs`/`nextFamilyP` from `PrimitivePassage`, whose docstring records that the thirteen station names were an externally imposed challenge. This module inherits that status; it adds no new state.
- **Declared policies.** `Origin`/`originOf`/`isEnvOwned` (constructor labels), the `ObstEffect` ordering (`removed` wins when both lists are nonempty), the projection `ClassSig` (drops budget delta and the preserved/untouched split), the table `classSig`/`classOf`, `WFClass`, and `sizeP`. All declared; none derived. The source says so.
- **Recurring hypotheses.** `WFClass s` (liveness + protection ⊆ retention) on the partition theorems; `Accepted s e = true`; declared observation `s.obs = some cols` on the funded cases.
- **Library lemmas doing real work.** `List.mem_filter`, `List.filter_append`, `List.any_eq_true`, `List.all_eq_true`, `List.mem_map`, `List.mem_flatMap`, `decide_eq_true/false`, `omega` on `Nat` lengths and budgets. `DecidableEq PState` (derived) is what makes `Accepted` a Bool and the `decide` witnesses run.
- **Finitude rule.** `PState` fields are `List Nat`/`List (Nat × Nat)`; `budget : Nat`; `sizeP : PState → Nat`; `admitOcc (t : Nat)` ranges over all naturals. These are metatheoretic. No docstring in this module reads them as an internal totality; `classSig_not_right_congruent_occurrence` uses `admitOcc 2` only as a concrete term. `dedup` and `allClasses` are over the 13-element inductive. The "6,144-state battery" and "exhaustive minimum" belong to the Python mirror and are reported as computation (source and ledger agree).
- Unearned identity: none found. Unrestricted external universe: `append_ne`, `list_ne_nil_of_mem`, `bne_true_of_ne` are polymorphic in `{α : Type}` as metatheory helpers only. Unbounded function treated as internally available: none found. Silently assumed observer: none found (`obs : Option` is explicit; `obstructedPairs_obsS` names `obs = none`). Unspecified correspondence between presentations: none claimed; the source disclaims renaming invariance. Cost function without justification: `sizeP` is a declared size for reporting only; `budgetDeltaOf` reads `t.budget + 1 = s.budget` as "spent one", a declared reading. Admitted condition later described as forced: none found. Finite computation presented as universal: none found in Lean; see §11 for a header wording.

## 5. Derived consequences

- `TraceAlgebra` consumes `accepted_false_iff`, `halted_accepts_nothing`, `refineOk_declared`, `colOk_declared`, all eleven `step_*_acc` / `_live` / `_eq` lemmas, `accepted_eq_guardHolds`, `internal_family_no_occurrence_supply`, `internal_family_no_license_write`, `nonEnv_preserves_occ_licensed`, and the witness states `wAssert`, `wFunded`, `wObstructed`, plus `guardHolds`, `GuardKind`, `EffectClass`, `BudgetDelta`, `Profile`, `classOf`, `budgetDeltaOf`, `profileOf`, `WFClass`. The whole "step normal form" of `TraceAlgebra` (`step_eq_ite`) rests on `accepted_eq_guardHolds`.
- No other Lean module imports this one (grep of `lean4/`). The root `Derivation.lean` prints axioms for all 116 public theorems.
- Ledger: CL-PD2-TRANSITION-CODEBOOK cites 14 theorems (listed in §8). Dependency graph: all 116 rows `kind: generic`, `role: undeclared`.

## 6. Counterexamples and limitations

| theorem | what it refutes | witness |
|---|---|---|
| `classSig_not_right_congruent_occurrence` | "equal one-step codes may be identified for replay" | `genesisP`; `admitOcc 0` vs `admitOcc 2`; suffix `admitOcc 0` |
| `classSig_not_right_congruent_budget` | same, for the coarser 13-code projection and budget amount | `budS wObstructed 2`; `setBudget 0` vs `setBudget 1`; suffix `addCol [0]` |
| `refine_addCol_domain_countermodel` | "the effect merge means refine and addCol are the same event" | `wRefineUnlicensed`, `wFundedUnlicensed`, `wFunded` |
| `preserved_untouched_not_invariant` | "the 4-way obstruction effect is a property of the transition" | `admitOcc` at `genesisP` vs at `wObstructed` |
| `budgetDelta_not_invariant` | "budget delta is a property of the constructor" | `setBudget 3` at genesis vs `setBudget 1` at budget 2 |
| `retention_creates_outside_class` | "retention never creates an obstruction" (without PSW) | `outsideClass` |
| `internal_family_emits_budget_write`, `env_ownership_claim_refuted` | "no environment-labelled constructor is internally generated" | `wObstructed`, block `[setBudget 1, addCol [0]]` |

Not proved (and the source says so): that thirteen is presentation-invariant; genesis-reachability of every code (only `wf_of_replay` in the other direction: reachable-and-live ⇒ WF); minimality of the witnesses inside `WFClass` (the docstring at line 1811 explicitly withdraws it); that no accepted WF step both loses and gains obstructed pairs — the docstring at line 572 says "each constructor lemma below proves one of the two difference lists empty", but for `colS`/`refineS` only `lostPairs ≠ []` and a subset lemma are stated; `gainedPairs = []` follows from `obstructedPairs_colS_sub`/`_refineS_sub` via `filter_notmem_eq_nil` but is not written as a theorem (checked by reading; it is a one-line corollary). `exists_unique_class` is uniqueness of the *label* with a given signature, not uniqueness of a transition's description under any other projection.

## 7. Axiom dependencies

All 116 artifact lines are within `{propext, Quot.sound}` (many are `propext` only or `none`). None exceed the boundary. Private `hfalse`, `hlive` are not in the artifact (not exported); they are kernel-checked helpers with no axioms.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- Axiom artifact: 116/116 public theorems present (inventory.json `axiom_report_hits`), matching the `#print axioms` block in `lean4/Derivation.lean`.
- Paper: `paper/paper.md` does not name the module. `paper/paper_claim_ledger.md` CL-PD2-TRANSITION-CODEBOOK cites `accepted_eq_guardHolds`, `halted_accepts_nothing`, `sig_eq_classSig`, `classSig_inj`, `exists_unique_class`, `wf_of_replay`, `declared_codebook_size`, `guard_erased_codebook_size`, both `classSig_not_right_congruent_*`, `refine_addCol_effect_merge`, `refine_addCol_domain_countermodel`, `internal_family_emits_budget_write`, `internal_family_env_only_unit_funding`. `paper/paper_change_log.md` ("Goals 2 and 3", 2026-08-13) records the repair history (13 is an image size; the budget premise was false).
- Probe: none run for this module (all statements inspected by reading; the `decide` witnesses are closed terms).

## 9. Related Python implementations

- `code/derivation/transition_alphabet.py` — mirrors `accepted`, `guard_holds`, `field_delta`, `obstructed_pairs`, `gained/lost_pairs`, `obst_effect`, `budget_delta`, `continuity_of`, `profile_of`, `sig_of`, `erase_guard`, `wf_class`, `class_of`, `enumerate_states` (the 6,144-state battery), `state_size`, and the reports (`partition_report`, `codebook_report`, `contextual_countermodel_report`, `witness_report`, `invariance_report`, `ownership_report`).
- `code/run_transition_alphabet.py` → `artifacts/transition_alphabet.json`.
- `tests/test_transition_alphabet.py` — `test_accepted_agrees_with_guard_everywhere`, `test_partition_is_exhaustively_verified`, `test_declared_codebook_sizes_are_recomputed`, `test_declared_code_is_not_a_contextual_congruence`, `test_witnesses_are_minimal_in_the_declared_space` (minimality is here, not in Lean), `test_wellformedness_is_load_bearing`, `test_policy_class_is_not_provenance`, and others; also `tests/test_independent_oracles.py` mentions the module.

## 10. Textbook placement proposal

- Prerequisites: `PrimitivePassage` (`PState`, the eleven events, `step`, `obstP`, `obstructedPairs`, `nextFamilyP`, `step_halted`); the distinction attempt vs accepted; what a guard is; the notion of replay.
- Substantive: `accepted_eq_guardHolds` (the inertness law), `WFClass` + `wf_of_replay` + `retention_creates_outside_class` (why the class is declared and why it is load-bearing), `obstructedPairs_protS`/`_obsS`/`obstEffect_colS`/`obstEffect_refineS` (what each kind of step does to the active obstructions), `sig_eq_classSig`/`classSig_inj`/`exists_unique_class` (the partition), the two `classSig_not_right_congruent_*` countermodels (why codes cannot replace events), `refine_addCol_effect_merge` + its domain countermodel, the two `*_not_invariant` theorems, and the `nextFamilyP` block-shape result with its refutation `internal_family_emits_budget_write`.
- Auxiliary: all `*_ne`, `step_*_acc/_inert`, `fieldDelta_*`, `filter_*`, `continuityOf_*`, `isEnvOwned_iff_origin`, `wf_of_wfB`, `allClasses_complete`, `class_witness_sizes`.
- Suggested lesson: **"Thirteen codes and why they are not an alphabet"** — the one question: *if we label every accepted step by what it changed, can the labels replace the steps?* (Answer: no; the label is a one-step projection that a common suffix separates.)
- Recommend omitting: `sizeP` and `class_witness_sizes` (a reporting metric; minimality lives in Python); `dedup` (replace by the statement "13 distinct values"); the `Origin` naming history (teach `isEnvOwned` as a declared label and the refutation, not the legacy name).

## 11. Interpretation findings

1. **Section header vs. docstring, line 1807–1811** — header "## 9. One minimum witness per class"; the docstring immediately below: "they are NOT in general the smallest states of the declared class that realize their letter … The exhaustive minimum … is the Python mirror's computation". The Lean (`class_witnesses`, `class_witness_sizes`) proves membership, acceptance, signature and a size number, not minimality. Ledger agrees with the docstring ("Witness minimality is only exhaustive computation within the declared finite space, not a Lean theorem"). Classification: INTERPRETATION DEFECT (header word "minimum"), self-corrected in place; no prose downstream overreads it.
2. **Docstring line 572–575** — "No accepted step of the declared class exercises that order — each constructor lemma below proves one of the two difference lists empty." For the two removal cases the lemmas prove `lostPairs ≠ []` and a subset inclusion; `gainedPairs = []` is an unstated one-line corollary. Classification: INTERPRETATION DEFECT (minor; the claim is true and provable from what is stated, but not literally "proved" as written).
3. **Ledger CL-PD2-TRANSITION-CODEBOOK**: "Erasing the guard leaves twelve declared code values (`declared_codebook_size`, `guard_erased_codebook_size`)" — the first theorem proves 13, the second 12; the sentence cites both for the 12. Harmless citation imprecision; INTERPRETATION DEFECT (minor).
4. Vacuity check: `WFClass` is inhabited (`genesisP`, `class_witnesses`); the funded hypotheses `0 < s.budget`, `refineOk`, `colOk` are jointly satisfied at `wRefine`/`wFunded`. No vacuous theorem found. `exists_unique_class` is not trivially true: it depends on `classSig_inj`, which is checked by `decide`.
5. Docstring "Scope discipline: every statement below is either universally quantified over the declared well-formed class `WFClass`, or is a concrete witness closed by `decide`" (lines 58–60) — several theorems are stronger (quantified over all `PState`, e.g. `accepted_eq_guardHolds`, `nextFamily_block_shape`, `nonEnv_preserves_occ_licensed`). Under-, not over-statement; recorded, not a defect.
6. Words "determined"/"forced"/"unique"/"complete": `exists_unique_class` (unique label — correct as quantified), `allClasses_complete` (finite list membership — correct), `internal_family_env_only_unit_funding` ("exact repaired statement" — correct over all `s`). No instance found where the Lean quantifies over less than the prose says.
