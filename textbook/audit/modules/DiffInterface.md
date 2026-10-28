# Audit: DiffInterface

| field | value |
|---|---|
| Path | lean4/Derivation/DiffInterface.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 1548ab6eaf991e4d |
| Lines | 761 |
| Imported by root `Derivation.lean` | yes (line 22) |
| Imports | none (core `Init` only; `Quotient`, `List`, `Nat`, `Bool` from core) |
| Declarations | 6 structures (`DiffObs`, `Stage`, `BareReflection`, `StageMaps`, `ClosureStep`, `ExtensionProposal`; the inventory counts 7), 3 inductives (`RequestKind`, `ClosureOutcome`, `RunResult`), 1 derived instance line (`deriving Repr, DecidableEq` on `RequestKind`), 32 defs, 35 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 35 lines (every theorem). None: `zeroRel_equivalence`, `kernel_zeroRel`, `no_guard_no_obstruction`, `unretained_not_active`, `distinguished_not_active`, `bare_reflection_certifies_active_obstruction`, `refines_preserves_distinctions`, `closure_preserves_old_distinctions`, `closure_kills_demanded`, `closure_adds_no_obstruction`, `tower_demand_bound`, `bool_view_pigeonhole`, `cm_freshness`, `cm_tagging`, `cm_edge`, `cm_hash`, `cm_repetition`. `Quot.sound`: `obsQuotient_eq_of_zero`. `propext`: `tower_demand_characterized`. `propext, Quot.sound`: the other 16 |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

An externally imposed challenge (2026-08-12): a self-contained package exposing the pipeline *reflection certificate → retained/protected observer-zero pair → active obstruction → map-saturated same-carrier closure step, or a separately represented extension proposal*. A difference observer is a typed difference operation `δ : X → X → R` with a zero predicate whose equivalence laws are fields; `ZeroRel` is proved an equivalence before the quotient is built. A stage carries liveness, retention, protection (`guarded`) and an observer; an active obstruction is the conjunction retained ∧ observer-zero ∧ protected, and dropping any conjunct blocks it. A bare reflection is a bundle of declared data whose parent/new pair is, by its own fields, an active obstruction. Closure discharges a map-saturated demand predicate by refining the observer on the same carrier, preserving every old distinction and creating no new obstruction; extension is a proposal (data), never a transition. A generic fuel driver terminates when a declared measure strictly decreases. The concrete realization is the reflective tower on `Nat` with the horizon-capped rank view: reflection adds a fresh point the stale observer cannot tell from its parent, closure re-synchronizes the horizon, the measure is the count of active pairs, and the driver terminates. A Boolean-view grammar on three protected points has no closed view (pigeonhole), so only a proposal is available. Five countermodels show freshness, tagging, an edge, a new hash and repetition each fail, by themselves, to produce an observer-visible difference.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `DiffObs X R` | 33 | structure | `delta`, `Zero`, and the three zero-laws as fields | ADMITTED (an observer is admitted with its proofs) |
| `ZeroRel O x y` | 42 | def | `O.Zero (O.delta x y)` | ADMITTED |
| `kernelObs view` | 54 | def | the observer `(view x, view y)`, zero iff equal views | ADMITTED |
| `obsSetoid`, `ObsQuotient`, `ObsQuotient.mk` | 69–75 | def | the quotient by `ZeroRel`, buildable only after `zeroRel_equivalence` | ADMITTED |
| `Stage X R` | 92 | structure | `live`, `retained`, `guarded`, `obs`; independent fields | ADMITTED |
| `ActiveObstruction S x y` | 101 | def | `retained ∧ ZeroRel ∧ guarded` | ADMITTED (definition of the obstruction) |
| `Stage.withObs` | 105 | def | replace the observer | ADMITTED |
| `BareReflection S S'` | 133 | structure | embed/retract, fresh point outside the old live image, declared parent, preservation fields, and the retained/guarded/zero pair fields | ADMITTED (declared certificate shape) |
| `Refines O₂ O₁` | 166 | def | every zero-pair of `O₂` is a zero-pair of `O₁` | ADMITTED |
| `StageMaps S` | 184 | structure | a list of maps containing the identity, each preserving live/retained/guarded/zero on the live region | ADMITTED |
| `MapSaturated G D` | 195 | def | `D` symmetric and closed under every declared map | ADMITTED |
| `ClosureStep S G` | 203 | structure | demand predicate `D` (active, off-diagonal, saturated), refined observer `obs'`, discharge of every demanded pair | ADMITTED (declared step shape) |
| `ClosureStep.apply` | 212 | def | `S.withObs C.obs'` | ADMITTED |
| `RequestKind`, `ExtensionProposal`, `ClosureOutcome` | 244–253 | inductive/structure/inductive | proposal data; the outcome sum | ADMITTED (discipline: proposals are data) |
| `RunResult`, `drive` | 259, 264 | inductive, def | fuel-indexed driver: closed / proposal / outOfFuel | ADMITTED |
| `cview h i` | 306 | def | `min i h` — the horizon-capped rank view | ADMITTED (declared observer family) |
| `mkStage s h` | 308 | def | live `i < s`; retained, guarded on live pairs (guarded also `i ≠ j`); observer `kernelObs (cview h)` | ADMITTED (the tower stage) |
| `towerReflection n` | 335 | def | the bare reflection `mkStage (n+1) n → mkStage (n+2) n`, fresh `n+1`, parent `n` | ADMITTED (instance) |
| `swapTop n` | 374 | def | `if x < n then x else 2n+1−x` — exchanges `n`, `n+1` on the live region | ADMITTED |
| `towerMaps n` | 386 | def | `[id, swapTop n]` with the preservation proofs | ADMITTED (instance) |
| `towerDemand n` | 433 | def | both orientations of `(n, n+1)` | ADMITTED |
| `towerClosure n` | 438 | def | the closure step refining to horizon `n+1` | ADMITTED (instance) |
| `activePairs s h`, `measureC s h` | 497, 523 | def | the list / count of live off-diagonal pairs with equal capped rank | ADMITTED (declared measure) |
| `towerDemandList n` | 567 | def | `[(n,n+1),(n+1,n)]` | ADMITTED |
| `towerNext` | 594 | def | `none` if no active pair, else step to `(s, s−1)` | ADMITTED (declared driver) |
| `bStage view` | 637 | def | three live protected points, observer `kernelObs view` for `view : Nat → Bool` | ADMITTED |
| `boolProposal view'` | 663 | def | an `observerStructure` proposal carrying the undischarged pairs | ADMITTED (data) |
| `freshUnguarded`, `tagView`, `tagStage`, `edgeView`, `edgeStage`, `hashStage`, `tokenOf`, `repetitionStage` | 680–752 | def | the five countermodel stages, all with `guarded := fun _ _ => False` | ADMITTED (countermodel data) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `zeroRel_equivalence` | 45 | `Equivalence (ZeroRel O)` from the three fields | FROZEN | none | S |
| `kernel_zeroRel` | 61 | `ZeroRel (kernelObs view) x y ↔ view x = view y` (`Iff.rfl`) | FROZEN | none | A |
| `obsQuotient_eq_of_zero` | 78 | `ZeroRel O x y → mk x = mk y` (soundness half; `Quotient.sound`) | FROZEN | Quot.sound | A |
| `no_guard_no_obstruction` | 111 | if nothing is guarded, nothing is an active obstruction | CONDITIONAL:`∀ x y, ¬ guarded` | none | A |
| `unretained_not_active` | 115 | `¬ retained x y → ¬ Active x y` | FROZEN | none | A |
| `distinguished_not_active` | 119 | `¬ ZeroRel x y → ¬ Active x y` | FROZEN | none | A |
| `bare_reflection_certifies_active_obstruction` | 155 | for any `B : BareReflection S S'`: `embed parent ≠ fresh ∧ Active S' (embed parent) fresh` (uses `fresh_from_live_image`, `parent_live`, the three pair fields) | FROZEN (given the certificate) | none | S |
| `refines_preserves_distinctions` | 171 | `Refines O₂ O₁ → ¬ ZeroRel O₁ x y → ¬ ZeroRel O₂ x y` | CONDITIONAL:`Refines` | none | A |
| `closure_preserves_old_distinctions` | 216 | `¬ ZeroRel S.obs x y → ¬ ZeroRel C.apply.obs x y` | FROZEN (given `C`) | none | S |
| `closure_kills_demanded` | 223 | `C.D x y → ¬ Active C.apply x y` | FROZEN (given `C`) | none | S |
| `closure_adds_no_obstruction` | 232 | `Active C.apply x y → Active S x y` | FROZEN (given `C`) | none | S |
| `drive_terminates` | 276 | if every `inl` step strictly decreases `μ`, then for `μ s < fuel` the driver ends `closed` or `proposal` | CONDITIONAL:strict decrease, `μ s < fuel` | propext, Quot.sound | S |
| `cview_distinct_mono` | 316 | `h ≤ h' → cview h i ≠ cview h j → cview h' i ≠ cview h' j` | FROZEN | propext, Quot.sound | A |
| `tower_closed` | 326 | `mkStage s (s−1)` has no active obstruction | FROZEN (∀ s) | propext, Quot.sound | S |
| `tower_obstruction` | 368 | `n ≠ n+1 ∧ Active (mkStage (n+2) n) n (n+1)` | FROZEN (∀ n) | propext, Quot.sound | S |
| `swapTop_view` | 376 | for `x < n+2`: `cview n (swapTop n x) = cview n x` | CONDITIONAL:`x < n+2` | propext, Quot.sound | A |
| `swapTop_live_inj` | 381 | `swapTop n` injective on `x, y < n+2` | CONDITIONAL:live | propext, Quot.sound | A |
| `tower_step_composes` | 482 | `(towerClosure n).apply = mkStage (n+2) (n+1)` (`rfl`) | FROZEN | propext, Quot.sound | S |
| `tower_successor_step` | 489 | `∃` reflection and closure step with `apply = mkStage (n+2) (n+1)` (pointwise in `n`) | FROZEN (∀ n) | propext, Quot.sound | S |
| `mem_activePairs` | 502 | membership ↔ `i < s ∧ j < s ∧ i ≠ j ∧ min i h = min j h` | FROZEN | propext, Quot.sound | A |
| `mem_activePairs_iff_active` | 526 | for `i ≠ j`: membership ↔ `Active (mkStage s h) i j` | CONDITIONAL:`i ≠ j` | propext, Quot.sound | S |
| `closed_measure_zero` | 537 | `measureC s (s−1) = 0` | FROZEN | propext, Quot.sound | S |
| `preclose_measure_pos` | 555 | `0 < measureC (n+2) n` | FROZEN | propext, Quot.sound | S |
| `tower_demand_characterized` | 570 | `towerDemand n x y ↔ (x,y) ∈ towerDemandList n` | FROZEN | propext | A |
| `tower_demand_bound` | 587 | `(towerDemandList n).length = 2` (`rfl`) | FROZEN | none | A |
| `towerNext_decrease` | 599 | an `inl` step of `towerNext` strictly decreases `measureC` (the target is measure 0) | FROZEN | propext, Quot.sound | S |
| `tower_fuel_terminates` | 617 | `measureC s h < fuel →` the tower driver ends closed or proposal | CONDITIONAL:`measureC s h < fuel` | propext, Quot.sound | S |
| `bool_view_pigeonhole` | 632 | any `view : Nat → Bool` identifies two of `0, 1, 2` | FROZEN (8-case `decide`) | none | S |
| `bool_grammar_obstruction` | 645 | every Boolean view leaves an active obstruction in `bStage view` | FROZEN | propext, Quot.sound | S |
| `no_bool_view_is_closed` | 656 | identical statement, `:= bool_grammar_obstruction` | FROZEN (alias) | propext, Quot.sound | A |
| `cm_freshness` | 683 | `0 ≠ 1`, observer-zero under horizon 0, not active in the unguarded stage | VERIFIED_FINITE | none | S |
| `cm_tagging` | 700 | both tagged, `1 ≠ 2`, observer-zero under the tag view, not active (unguarded) | VERIFIED_FINITE | none | S |
| `cm_edge` | 719 | both endpoints incident, observer-zero under the incidence view, not active (unguarded) | VERIFIED_FINITE | none | S |
| `cm_hash` | 736 | identity label injective, `0 ≠ 1`, observer-zero under the constant observer, not active (unguarded) | VERIFIED_FINITE | none | S |
| `cm_repetition` | 754 | one token for two occurrences, observer-zero, not active (unguarded) | VERIFIED_FINITE | none | S |

## 4. External and admitted assumptions

- **Everything abstract is conditional on declared bundles.** `BareReflection` has 15 fields; the certificate theorem spends four (`fresh_from_live_image`, `parent_live`, `pair_retained`, `pair_guarded`, `pair_zero`). `retract`, `retract_embed`, `live_embed`, `zero_preserved`, `retained_embed`, `guarded_embed` are declared and not used by any theorem in this module (they are discharged for the tower instance). Likewise `StageMaps`' preservation fields are not used by any theorem here (`MapSaturated` reads only `G.maps`). `ClosureStep.discharges` carries an `x ≠ y` hypothesis already implied by `demand_offdiag`. These are shape declarations the caller asked for; the module's docstrings say what each theorem uses.
- **Decrease is not proved abstractly.** `closure_kills_demanded` and `closure_adds_no_obstruction` are "an ingredient of a decrease proof; finiteness and a removed active pair are separate obligations" — proved only for the concrete measure (`towerNext_decrease`). The ledger's `CL-DI-CLOSURE` is checked against this wording only through its first line (not read in full).
- **The concrete driver closes in one step.** `towerNext` always moves to `(s, s−1)`, which has measure 0 (`closed_measure_zero`); so `towerNext_decrease` is "anything positive > 0" and `tower_fuel_terminates` needs fuel ≥ 2 at most. The generic `drive_terminates` is exercised, but only trivially.
- `Nat` as the tower carrier and `n`-indexed families (`towerReflection n`, `mkStage`) are metatheoretic; "uniform successor-step family" is pointwise (docstring says so). Finitude flag only.
- `view : Nat → Bool` in the Boolean grammar is an arbitrary function; "the declared grammar" is all such views, and the theorem reads only `view 0, view 1, view 2`.
- Library lemmas doing work: `Quotient.sound`, `List.mem_flatMap/mem_map/mem_filter/mem_range`, `bne_iff_ne`, `beq_iff_eq`, `List.ne_nil_of_mem`, `List.mem_cons`, `injection`, `omega`, `decide`, `simp [drive, hn]`.
- Unearned identity: none. Unrestricted external universe: `X X' R V : Type` as variables; none found. Unbounded function treated as internally available: `view : Nat → Bool`, `cview`, the measure — all metatheory; the module makes no claim that the system holds them. Silently assumed observer: none; observers are the declared data. Unspecified correspondence between presentations: none inside the module; the caller's adapter is declared out of scope. Cost function without justification: `measureC` is a declared measure (docstring "the declared measure"). Admitted condition later described as forced: none found. Finite computation presented as universal: `bool_view_pigeonhole` is an 8-case check stated for all `view`, correctly.

## 5. Derived consequences

Consumed by `ObsDescent.lean`, `ContactBridge.lean` (`DiffObs`, `ZeroRel`, `kernelObs`, `obsApart := ¬ ZeroRel`), `PrimitiveContact.lean` (`DiffObs` in `native_interface_not_representable`). Ledger owners: `CL-DI-EQUIVALENCE`, `CL-DI-OBSTRUCTION`, `CL-DI-REFLECTION`, `CL-DI-CLOSURE`, `CL-DI-TERMINATION`, `CL-DI-PROPOSAL`, `CL-DI-COUNTERMODELS`; `zeroRel_equivalence` also cited by `CL-PD2-CONTACT-COUNTERMODELS`. Not cited by any `CL-` entry: `kernel_zeroRel`, `refines_preserves_distinctions`, `swapTop_view`, `swapTop_live_inj`, `mem_activePairs_iff_active`. Paper: `paper/difference_interface.md` (DELIVERED table, boundary statements, open extensions). `paper/native_derivation_map.md` line 58 compares `DiffObs` with the arriving development's laws.

## 6. Counterexamples and limitations

- Countermodels: the five `cm_*` (each exhibits an observer blind to the named feature; the "not active" conjunct holds because the stage is unguarded), `bool_grammar_obstruction` (no Boolean view closes three protected points).
- Not proved: the completeness half of the quotient (`mk x = mk y → ZeroRel`; the paper's `CL-PD2-CONTACT` says `ObsDescent.obsQuotient_exact` supplies it); an abstract decrease theorem; any proposal-processing step; termination without the measure hypothesis; anything about maps off the live region (boundary statement: `swapTop` is not view-preserving there).

## 7. Axiom dependencies

All 35 within `{propext, Quot.sound}`; 17 use none. None exceed: none. (The paper's boundary note records that `omega` on compound goals and `List.eq_nil_iff_forall_not_mem` were avoided because they leak `Classical.choice` on this toolchain; `closed_measure_zero` and `preclose_measure_pos` are written by case analysis for that reason.)

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 35 theorems in the artifact (35 `#print axioms DiffInterface.*` lines in the root). The paper's DELIVERED table and the seven `CL-DI-*` entries cite them. No probe run.

## 9. Related Python implementations

`code/derivation/diff_interface.py`: `cview`, `active_pairs`, `measure`, `swap_top`, `tower_demand_support`, `tower_round`, `tower_report`, `drive`, `tower_next`, `fuel_report`, `bool_views`, `bool_grammar_report`, `obstruction_active`, `countermodel_report`; artifact `artifacts/diff_interface.json`; tests `tests/test_diff_interface.py` (`test_closed_stage_measure_zero`, `test_reflection_produces_active_obstruction`, `test_demand_is_map_saturated_and_uniformly_bounded`, `test_closure_discharges_preserves_and_decreases`, `test_fuel_driver_terminates_closed`, `test_fuel_driver_out_of_fuel_without_budget`, `test_no_bool_grammar_view_is_closed`, `test_countermodels_all_zero_all_unprotected_and_inactive`, `test_activity_is_exactly_the_three_way_conjunction`, …). `code/derivation/represented.py` / `tests/test_represented.py::test_pigeonhole_progress_story` narrate the Boolean pigeonhole.

## 10. Textbook placement proposal

- Prerequisites: the three obstruction conditions as separate predicates (from the first checkpoint's closure policy); equivalence relations and quotients; a fuel-indexed recursion.
- Substantive: `DiffObs`/`ZeroRel`/`zeroRel_equivalence`; `ActiveObstruction` and the three blocking lemmas; `BareReflection` + `bare_reflection_certifies_active_obstruction`; `ClosureStep` with its three theorems; `ExtensionProposal` as data; `drive_terminates`; the tower (`tower_obstruction`, `tower_step_composes`, `closed_measure_zero`, `tower_fuel_terminates`); `bool_grammar_obstruction`; the five countermodels. Auxiliary: `kernel_zeroRel`, `obsQuotient_eq_of_zero`, `refines_preserves_distinctions`, `cview_distinct_mono`, `swapTop_*`, `mem_activePairs*`, `tower_demand_*`, `no_bool_view_is_closed`.
- Lesson title: "Reflect, obstruct, close, or propose." Question answered: what minimal typed interface carries a reflection certificate to a same-carrier closure step, and what it refuses to do (choose a representative, apply a proposal, run without fuel).
- Recommend omitting: `no_bool_view_is_closed` (duplicate name), `tower_demand_characterized`/`tower_demand_bound` (bookkeeping), the unused certificate fields from the lesson's statement of `BareReflection` (teach the four fields the theorem spends, then say the rest are the caller's shape).

## 11. Interpretation findings

1. `cm_*` countermodels — docstring: "Each names a feature that does **not**, by itself, produce observer-visible difference." Lean: each theorem's `¬ ActiveObstruction` conjunct follows from `guarded := fun _ _ => False` alone (`no_guard_no_obstruction`), and its `ZeroRel` conjunct holds for one chosen observer that does not read the feature (constant observer for the hash, token view for repetition). So the content is "there exists an observer blind to the feature, and without protection no obstruction is active" — a correct countermodel to "feature ⇒ difference for every observer", but the `¬ Active` conjunct is by construction. The module's own preamble says the stages are unprotected. Classification: INTERPRETATION DEFECT (minor; a reader could take the `¬ Active` conjunct as showing the feature is inert under protection — it shows nothing under protection).
2. `tower_fuel_terminates` / paper DELIVERED "finite fuel ⇒ termination … instantiated by `tower_fuel_terminates`". Lean: `towerNext` jumps straight to the closed horizon, so every run is at most one step; the measure hypothesis `measureC s h < fuel` is far more than needed and the instance tests the generic theorem only degenerately. The conditional generic theorem is correct. Classification: INTERPRETATION DEFECT (minor; "concrete fuel termination" is a one-step instance).
3. `no_bool_view_is_closed` — docstring "No Boolean view in the declared grammar closes the family"; Lean: the same proposition as `bool_grammar_obstruction`, proved by naming it. Two names for one theorem. Vacuity: not vacuous, but no second content. Classification: INTERPRETATION DEFECT (minor; the ledger `CL-DI-PROPOSAL` cites both as if two facts — not checked whether it distinguishes them).
4. `BareReflection` / `CL-DI-REFLECTION` ("a bare reflection step (embedding + retraction, …)"). Lean: the retraction and the preservation fields are not spent by `bare_reflection_certifies_active_obstruction` (docstring: "uses the certificate's three pair fields"). The ledger describes the shape; the theorem uses less. Not a defect; a scope note for the textbook (the unused fields are the caller's shape, not hypotheses the result needs).
5. `tower_successor_step` — correctly disclaims a trace object. `drive_terminates` — correctly conditional. `bool_view_pigeonhole` — correctly universal via 8 cases. No defect.
6. Vacuity: `no_guard_no_obstruction`'s hypothesis is satisfiable (the countermodel stages); `drive_terminates`' `μ s < fuel` satisfiable; `mem_activePairs_iff_active` needs `i ≠ j` (without it the list side is false and the `Active` side is false too via `guarded`, so the restriction is harmless). None vacuous.
