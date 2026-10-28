# Audit: ControllerCategory

| field | value |
|---|---|
| Path | lean4/Derivation/ControllerCategory.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 7a0fe9e452a8c1f8 |
| Lines | 774 (inventory records 775) |
| Imported by root `Derivation.lean` | yes (line 36) |
| Imports | Derivation.PrimitivePassage (and through it PrimDiff, PrimitiveCore) |
| Declarations | 4 structure (`KindDesc`, `Ctrl`, `Sim`, `StrictSim`), 35 def (including the `Sim`/`StrictSim` values `eraseSim`, `constSim`, `twistSim`, `idStrict`, `eraseStrict`, `twistStrict`), 63 theorems; the inventory's "1 class" is the word in the docstring, there is no Lean `class` |
| Axiom reports in `artifacts/lean_axioms.txt` | 63 lines (every theorem); 46 `[propext, Quot.sound]`, 1 `[propext]` (`mem_bools`), 16 none (`allKinds_length`, `live_census`, `fullK_live`, `noRefK_live`, `noRefK_ne_fullK`, the eight `setRef_*` field lemmas, `wfPair_setRef`, `eraseRef_not_id`, `halted0_ne_halted1`) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module widens the comparison class in which the passage kernel's controller was earlier shown unique (the six-toggle class of `Initiality.unique_compliant`, whose scope note already restricted that claim). A controller here is one enable bit per event kind; an enabled event runs the sealed `step`, a disabled one is inert. The class has 1024 members and is enumerated completely. The module proves that all 128 controllers enabling the three response kinds (`refineCol`, `addCol`, `setBudget`) execute the funded extension at a concrete obstructed state, that disabling any one of the three kills the resolution on a state where it is load-bearing, and that two live controllers (all-on and refusal-free) agree on every refusal-free event yet differ at an obstruction, so probe compliance does not pin a unique controller. It then defines simulations between controllers (state maps commuting with the interpreted step), proves the category laws, exhibits refusal erasure as a genuine morphism, and refutes initiality: constant maps to halted states are simulations between any two controllers because the halted state is absorbing, so morphisms exist everywhere and are never unique. A strict refinement (genesis- and liveness-preserving) excludes the constants but still fails global uniqueness by an invariant-twist countermodel; what survives is agreement on the genesis-reachable orbit, proved for the one hom-set exhibited.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `KindDesc` | 84 | structure | ten Booleans, one per event kind except `assertWit` | ADMITTED (declared comparison class) |
| `enabled d` | 98 | def | reads the bit for the event's kind; `assertWit` is always `true` | ADMITTED (declared policy: supply is never toggled) |
| `interpK d s e` | 117 | def | `if enabled d e then step s e else s` | ADMITTED |
| `replayK d h s` | 120 | def | fold of `interpK d` | ADMITTED |
| `bools` | 123 | def | `[false, true]` | ADMITTED |
| `allKinds` | 126 | def | the 1024-element enumeration by nested `flatMap` | ADMITTED |
| `fullK` | 153 | def | all bits on | ADMITTED |
| `ResponseLiveB`, `ResponseLive` | 165–168 | def | the three response bits on (Bool and Prop) | ADMITTED |
| `OBST5` | 178 | def | two occurrences, both pairs asserted, `(0,1)` retained and protected, `obs = some []`, budget 5, licensed, live | ADMITTED (datum) |
| `noAddK`, `noBudgetK`, `noRefineK` | 202–204 | def | `fullK` with one response bit off | ADMITTED |
| `OBST0` | 207 | def | `OBST5` with budget 0 | ADMITTED |
| `LOBST` | 212 | def | unlicensed refinable obstructed state (`obs = some [[]]`) | ADMITTED |
| `noRefK` | 269 | def | `fullK` with `kRefuse := false` | ADMITTED |
| `isRefuse` | 274 | def | Boolean test for the `refuse` kind | ADMITTED |
| `Ctrl` | 293 | structure | wrapper of a `KindDesc` (an object) | ADMITTED |
| `Sim C1 C2` | 298 | structure | `f : PState → PState` with `comm : ∀ s e, f (interpK C1.d s e) = interpK C2.d (f s) e` | ADMITTED (the morphism notion; `f` is a metatheoretic function) |
| `idSim`, `compSim` | 314–316 | def | identity and composite simulations | ADMITTED |
| `fullCtrl`, `noRefCtrl` | 332–333 | def | the two objects used throughout | ADMITTED |
| `setRef rs s`, `eraseRef` | 336–339 | def | overwrite / clear the refusal store | ADMITTED |
| `eraseSim` | 465 | def (Sim) | refusal erasure as a simulation `fullCtrl → noRefCtrl` | ADMITTED (its `comm` is a proof; see `erase_sim`) |
| `HALTED0`, `HALTED1` | 499–500 | def | two distinct halted states | ADMITTED (data) |
| `constSim C T t ht` | 507 | def (Sim) | the constant map to a halted `t` | ADMITTED (its `comm` is a proof) |
| `InitialCtrl C` | 546 | def | `∀ T, ∃ u : Sim C T, ∀ v, v = u` | ADMITTED |
| `StrictSim C1 C2` | 583 | structure | a `Sim` with `gen : f genesisP = genesisP` and `live : halted = false → (f s).halted = false` | ADMITTED |
| `idStrict`, `eraseStrict` | 598–601 | def | identity and erasure as strict simulations | ADMITTED |
| `hasDup` | 607 | def | some element of a `List Nat` recurs | ADMITTED |
| `twistRef`, `twistF` | 644–647 | def | refusal store `[(0,0)]` iff `hasDup s.occ`, else `[]`; the map writing it | ADMITTED (countermodel apparatus) |
| `twistSim`, `twistStrict` | 661–682 | def | the twist as a (strict) simulation | ADMITTED |
| `DUPSTATE` | 687 | def | `occ = [5,5]`, refusals `[(3,4)]`, live | ADMITTED (unreachable datum) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `allKinds_length` | 133 | `allKinds.length = 1024` | VERIFIED_FINITE | none | A |
| `mem_bools` | 135 | every `Bool` is in `bools` | FROZEN | propext | A |
| `allKinds_complete` | 139 | every `KindDesc` is in `allKinds` | FROZEN | propext, Quot.sound | S |
| `interpK_full` | 157 | `interpK fullK s e = step s e` for all `s e` | FROZEN | propext, Quot.sound | S |
| `live_census` | 172 | `(allKinds.filter ResponseLiveB).length = 128` | VERIFIED_FINITE | none | S |
| `fullK_live` | 175 | `fullK` is live | VERIFIED_FINITE | none | A |
| `obst5_certified` | 183 | `obstP OBST5 0 1 = true` | VERIFIED_FINITE | propext, Quot.sound | A |
| `tworule_executable_of_live` | 190 | for every `d` with `ResponseLiveB d = true`, `obstP (interpK d (interpK d OBST5 (setBudget 1)) (addCol [0])) 0 1 = false` | CONDITIONAL: `ResponseLiveB d` (generic over the 128; proof by destructuring and `rfl`) | propext, Quot.sound | S |
| `obst0_certified`, `lobst_certified` | 218–219 | the two other states are obstructed | VERIFIED_FINITE | propext, Quot.sound | A |
| `battery_obst5_nonempty`, `battery_obst0_nonempty`, `battery_lobst_nonempty` | 223–225 | `nextFamilyP` of each state is nonempty | VERIFIED_FINITE | propext, Quot.sound | A |
| `dead_without_addcol` | 230 | every `nextFamilyP OBST5` block replayed under `noAddK` leaves the obstruction | VERIFIED_FINITE (REFUTED: `addCol` is dispensable) | propext, Quot.sound | S |
| `full_resolves_obst5` | 236 | `fullK` resolves OBST5 with `[setBudget 1, addCol [0]]` | VERIFIED_FINITE | propext, Quot.sound | A |
| `dead_without_budget` | 243 | every `nextFamilyP OBST0` block under `noBudgetK` leaves the obstruction | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | S |
| `full_resolves_obst0` | 247 | `fullK` resolves OBST0 | VERIFIED_FINITE | propext, Quot.sound | A |
| `dead_without_refine` | 255 | every `nextFamilyP LOBST` block under `noRefineK` leaves the obstruction | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | S |
| `full_resolves_lobst` | 259 | `fullK` resolves LOBST with `[refineCol [] 0]` | VERIFIED_FINITE | propext, Quot.sound | A |
| `noRefK_live`, `noRefK_ne_fullK` | 271–272 | the refusal-free controller is live and distinct | VERIFIED_FINITE | none | A |
| `nonrefuse_agree` | 280 | `isRefuse e = false → interpK fullK s e = interpK noRefK s e` for all `s` | CONDITIONAL: refusal-free event | propext, Quot.sound | S |
| `refuse_distinguishes` | 286 | the two controllers differ at `OBST5` on `refuse 0 1` | VERIFIED_FINITE | propext, Quot.sound | S |
| `sim_ext` | 304 | simulations with equal `f` are equal | FROZEN | propext, Quot.sound | A |
| `comp_id`, `id_comp`, `comp_assoc` | 320–326 | the category laws for `compSim`/`idSim` | FROZEN | propext, Quot.sound | S |
| `setRef_occ` … `setRef_halted` (8) | 341–355 | `setRef` changes only `refusals` | FROZEN | none | A |
| `wfPair_setRef`, `obstP_setRef`, `refineOk_setRef`, `colOk_setRef` | 358–365 | the guards ignore the refusal store | FROZEN | none / propext, Quot.sound | A |
| `setRef_step_comm` | 371 | `isRefuse e = false → setRef rs (step s e) = step (setRef rs s) e` | CONDITIONAL: refusal-free event | propext, Quot.sound | S |
| `erase_sim` | 489 | `∃ u : Sim fullCtrl noRefCtrl, u.f = eraseRef` | FROZEN | propext, Quot.sound | S |
| `eraseRef_not_id` | 493 | erasure moves a state with a nonempty refusal store | VERIFIED_FINITE | none | A |
| `halted0_ne_halted1` | 502 | the two halted states differ | VERIFIED_FINITE | none | A |
| `const_sims_distinct` | 518 | the two constant simulations differ, for every `C T` | FROZEN | propext, Quot.sound | S |
| `two_endo_sims` | 527 | a constant endo-simulation on `fullCtrl` is not the identity | FROZEN | propext, Quot.sound | A |
| `every_pair_connected` | 536 | `Nonempty (Sim C T)` for every `C T` | FROZEN | propext, Quot.sound | S |
| `sims_never_unique` | 540 | `∃ u v : Sim C T, u ≠ v` for every `C T` | FROZEN (REFUTED: uniqueness) | propext, Quot.sound | S |
| `no_initial_ctrl` | 551 | `¬ ∃ C, InitialCtrl C` | REFUTED (initiality) | propext, Quot.sound | S |
| `no_initial_live_ctrl` | 562 | no live controller is initial among live controllers | REFUTED | propext, Quot.sound | S |
| `const_not_strict` | 588 | a strict simulation's map is never a constant to a halted state | FROZEN | propext, Quot.sound | S |
| `hasDup_append_fresh` | 611 | appending a fresh element preserves `hasDup` | FROZEN | propext, Quot.sound | A |
| `hasDup_step` | 634 | `hasDup (step s e).occ = hasDup s.occ` for all `s e` | FROZEN | propext, Quot.sound | S |
| `twistRef_step` | 649 | `twistRef (step s e) = twistRef s` | FROZEN | propext, Quot.sound | A |
| `twist_step_comm` | 653 | on refusal-free events the twist commutes with `step` | CONDITIONAL: refusal-free event | propext, Quot.sound | A |
| `twist_ne_erase_at_dup` | 692 | `twistF DUPSTATE ≠ eraseRef DUPSTATE` | VERIFIED_FINITE | propext, Quot.sound | A |
| `strict_not_unique` | 698 | `∃ u v : StrictSim fullCtrl noRefCtrl, u ≠ v` | REFUTED (strict uniqueness) | propext, Quot.sound | S |
| `replay_hasDup` | 708 | `hasDup (replayP h s).occ = hasDup s.occ` | FROZEN | propext, Quot.sound | A |
| `reachable_no_dup` | 717 | `hasDup (replayP h genesisP).occ = false` for every history | FROZEN | propext, Quot.sound | S |
| `twist_eq_erase_of_no_dup` | 721 | `hasDup s.occ = false → twistF s = eraseRef s` | CONDITIONAL: no duplicate | propext, Quot.sound | A |
| `twist_erase_agree_reachable` | 730 | the twist equals erasure on every state replayed from genesis | FROZEN | propext, Quot.sound | S |
| `sim_pinned` | 737 | for `u : Sim fullCtrl noRefCtrl`, `u.f (replayP hist s) = foldl (interpK noRefK) (u.f s) hist` | FROZEN | propext, Quot.sound | S |
| `genesis_sims_agree_on_reachable` | 761 | two simulations `fullCtrl → noRefCtrl` fixing `genesisP` agree on every replayed state | CONDITIONAL: both fix genesis | propext, Quot.sound | S |
| `strict_agree_on_reachable` | 768 | two strict simulations `fullCtrl → noRefCtrl` agree on every state replayed from genesis | FROZEN (for this hom-set) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Taken as given: `PState`, `PEvent`, `step`, `replayP`, `genesisP`, `obstP`, `wfPair`, `refineOk`, `colOk`, `nextFamilyP`, `step_halted` (PrimitivePassage).
- Declared policy inside the class: `enabled` returns `true` for `assertWit` regardless of the controller (line 103, with a comment). So the "1024 controllers" never vary the supply of asserted differences; the class is 2^10 over ten of the eleven kinds. The docstring says "ten event kinds of the passage dynamics"; the `PEvent` type has eleven constructors. This is a declared scoping, stated in a code comment, not in the module docstring's summary line.
- Recurring hypotheses: `isRefuse e = false` (for commutation of refusal-store rewrites), `ResponseLiveB d = true`, `halted = true` (for `constSim`), `f genesisP = genesisP`.
- Library lemmas doing real work: `List.mem_flatMap`, `List.mem_map`, `List.mem_append`, `decide_eq_decide`; kernel `decide` over 1024-element lists (with `maxRecDepth 8192`).
- Functions `Nat → X` / `Type` as data: `Sim.f : PState → PState` is an arbitrary metatheoretic function; `constSim` and `twistF` exploit this. Finitude flag: the "category" lives in the metatheory (objects are 1024 finite descriptors, morphisms are arbitrary state maps). The docstring does not claim the system possesses the category; the paper (primitive_controller_universality.md) treats it as the comparison apparatus. No overread found.
- Unearned identity: none found; `sim_ext` is proved by cases, and the category laws reduce to `rfl` through it.
- Unrestricted external universe: none found (no `Type` parameters; everything is over `PState`).
- Unbounded function treated as internally available: none found.
- Silently assumed observer: none found.
- Unspecified correspondence between presentations: none found.
- Cost function without justification: none (no cost in this module).
- Admitted condition later described as forced: none found. The module's positive results are scoped ("exactly this proof" for "complete").
- Finite computation presented as universal: `live_census` (128) and the three `dead_without_*` theorems are finite over declared batteries, and the docstring says "over declared finite batteries". `tworule_executable_of_live` is generic over the 128 by a proof, not a `decide`; it is a single concrete state `OBST5`, which the docstring states.

## 5. Derived consequences

No downstream Lean module imports `ControllerCategory` (grep: none). The ledger entry CL-PD2-CONTROLLER cites 16 theorems; paper/primitive_controller_universality.md is the write-up and names the terminals NONUNIQUE_CONTROLLER_FAMILY, INITIALITY_REFUTED_BY_constant_simulations_countermodel, STRICT_UNIQUENESS_ON_REACHABLE_ORBIT. Within the module: `step_halted` drives `constSim` and hence every initiality refutation; `setRef_step_comm` drives `eraseSim` and `twistSim`; `hasDup_step` drives `reachable_no_dup` and the twist; `sim_pinned` drives the orbit agreement.

## 6. Counterexamples and limitations

- `dead_without_addcol/budget/refine`: refute "a response kind is dispensable"; witnesses `OBST5`, `OBST0`, `LOBST` with the kernel's own `nextFamilyP` batteries (nonempty by the `battery_*` lemmas, so not vacuous).
- `refuse_distinguishes` with `nonrefuse_agree`: refutes "probe compliance pins the controller"; witness `noRefK`.
- `sims_never_unique`, `no_initial_ctrl`, `no_initial_live_ctrl`: refute initiality; witnesses `constSim … HALTED0` and `… HALTED1`.
- `strict_not_unique`: refutes uniqueness under the strict refinement; witness `twistStrict` versus `eraseStrict`, separated at `DUPSTATE`.
- Not proved: uniqueness on the reachable orbit for any hom-set other than `fullCtrl → noRefCtrl` (`sim_pinned` uses `interpK_full` on the source, so the source must be `fullCtrl`). The ledger says "no other ordered pair is claimed (pair scope made explicit 2026-08-18)". The module docstring's bullet says "any two genesis-preserving simulations agree" without naming the pair; the theorem statement names it.
- Not proved: that `ResponseLive` is behaviourally exact over all states (the docstring says "the two-rule response universe is supported by exactly the three response kinds"; the Lean shows executability at `OBST5` for all live members and failure of each kind at one state each; it does not show a non-live controller fails everywhere, nor that live controllers agree everywhere).
- Not proved: that the simulation category restricted to reachable states has an initial object (named as "the recorded boundary, not claimed here").
- The class does not vary `assertWit` (see section 4), so "no controller is initial" is a statement about this 1024-member class.

## 7. Axiom dependencies

All 63 artifact lines lie within `{propext, Quot.sound}`; 16 use no axioms, 1 uses `propext` alone. None exceeds the whitelist.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 63 theorems appear in the axiom artifact; 16 are cited by CL-PD2-CONTROLLER and the write-up paper/primitive_controller_universality.md cites `sims_never_unique`, `no_initial_ctrl`, `no_initial_live_ctrl`, `strict_agree_on_reachable`, `sim_pinned`, `reachable_no_dup`, `twist_erase_agree_reachable`, `twist_ne_erase_at_dup`, `erase_sim`, `every_pair_connected`, `constSim`, `const_not_strict`, `strict_not_unique`. No probe was run for this module.

## 9. Related Python implementations

code/derivation/controller_category.py: `all_kinds`, `full_without`, `enabled`, `interp_k`, `replay_k`, `response_live`, `behavior_signature`, `live_behavior_classes`, `response_kind_countermodels`, `nonuniqueness_report`, `category_report`, `has_dup`, `erase_ref`, `twist_ref`, `twist_f`, `strict_refinement_report`, `controller_category_report`. tests/test_controller_category.py: `test_class_enumeration`, `test_enabled_and_interp`, `test_full_without`, `test_live_census_and_tworule`, `test_response_kind_countermodels`, `test_nonuniqueness`, `test_behavior_signature_distinguishes`, `test_constant_simulations`, `test_has_dup_and_twist`, `test_twist_and_erase_are_simulations`, `test_strict_refinement_report`, `test_reachable_orbit_agreement`, `test_serialization`, `test_full_report_shape`, `test_halted_states_absorb_under_every_controller`, `test_replay_k_disabled_prefix`, `test_runner_byte_stable`. Artifact: artifacts/primitive_controller_category.json.

## 10. Textbook placement proposal

- Prerequisites: `step`, `step_halted` (the halted state absorbs), `nextFamilyP` and `obstP` (PrimitivePassage); the earlier six-toggle uniqueness claim and its scope note (`Initiality`).
- Substantive: `interpK`/`KindDesc` with `allKinds_complete`; `live_census` and `tworule_executable_of_live`; the three `dead_without_*` countermodels; `nonrefuse_agree` + `refuse_distinguishes`; `Sim` with the three category laws; `erase_sim`; `constSim` with `every_pair_connected`, `sims_never_unique`, `no_initial_ctrl`; `StrictSim`, `const_not_strict`, `strict_not_unique`; `reachable_no_dup`, `sim_pinned`, `strict_agree_on_reachable`. Auxiliary: the `setRef_*` lemmas, `setRef_step_comm` (its 90-line case split can be described), `hasDup_*`, `twistRef_step`, the `*_certified` and `battery_*` facts, `two_endo_sims`, `eraseRef_not_id`, `halted0_ne_halted1`.
- Lesson title: "Is the controller unique? Simulations, the absorbing halt, and uniqueness only along replay." Question answered: in a class that varies the event grammar, does any controller have a unique map to every other? (No; two distinct constant simulations always exist; even strict simulations agree only on genesis-reachable states.)
- Recommend omitting: `two_endo_sims` (subsumed by `sims_never_unique`), `full_resolves_*` as separate items (fold into the countermodel presentation), the individual `setRef_*` lemmas.

## 11. Interpretation findings

- Categorical vocabulary check (requested): "category" names proved laws (`comp_id`, `id_comp`, `comp_assoc` over `Sim`, via `sim_ext`); "simulation" is the admitted structure `Sim` whose `comm` field is a proof obligation, discharged for `idSim`, `compSim`, `eraseSim`, `constSim`, `twistSim`; "initial" is the admitted definition `InitialCtrl`, refuted. "Complete" (for `allKinds`) names `allKinds_complete`. None of these words labels an admitted axiom-like field. No defect.
- Module docstring line 10–11 "each of the ten event kinds" versus the eleven-constructor `PEvent` with `assertWit` hard-wired to `true` (line 103): the comparison class excludes the supply kind by declaration. The docstring at line 100–102 states this in a code comment; the summary docstring and the paper ("ten Booleans, one per passage event kind") do not say that one kind is never toggled. INTERPRETATION DEFECT (minor, scoping): a reader could think the class ranges over all event-kind grammars. The missing clause: "the supply event `assertWit` is enabled in every member". The results stand within the declared class.
- Docstring bullet (lines 20–22) "the two-rule response universe is supported by exactly the three response kinds": the Lean proves sufficiency at `OBST5` for every live member and necessity of each kind at one chosen state each. "Exactly" is justified in the sense "each of the three is load-bearing somewhere and the three together suffice at `OBST5`", not "live iff resolves every obstruction". The paper's phrase "behaviorally exact" overreads by the same margin. INTERPRETATION DEFECT (minor): missing hypothesis for a biconditional would be a quantification over states that the module does not attempt.
- Docstring bullet (lines 63–66) "any two genesis-preserving simulations agree on every state replayed from genesis" omits the pair `fullCtrl → noRefCtrl` that `genesis_sims_agree_on_reachable` and `strict_agree_on_reachable` fix; the proof relies on `interpK_full` for the source. The ledger corrected this on 2026-08-18 ("no other ordered pair is claimed"). INTERPRETATION DEFECT already recorded by the ledger; the module docstring was not updated. Counterexample to the unqualified reading: not supplied by the module, and not checked here whether it exists.
- `tworule_executable_of_live` (line 190): the docstring says "generic over all 128 live members"; the proof destructures `d`, substitutes the three live bits and closes by `rfl`, so the seven free bits are genuinely irrelevant. Correct; not a `decide` over 128 cases.
- Vacuity check: the `dead_without_*` theorems are `List.all` over `nextFamilyP` batteries proved nonempty (`battery_*_nonempty`), so not vacuous; `const_not_strict` has satisfiable hypotheses (`idStrict` exists); `genesis_sims_agree_on_reachable` has at least two distinct instances (`eraseSim`, `twistSim`). None vacuous.
- No theorem in the module reads as "forced", "necessary", "universal" or "canonical" positively; the universality-flavoured statements are all negations or orbit-relative, and the Lean matches the negative readings.
