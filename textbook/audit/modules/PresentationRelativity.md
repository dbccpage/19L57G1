# Audit: PresentationRelativity

| field | value |
|---|---|
| Path | lean4/Derivation/PresentationRelativity.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 862da7363a07b257 |
| Lines | 637 |
| Imported by root `Derivation.lean` | yes (line 54) |
| Imports | Derivation.Compression, Derivation.NoOutside, Derivation.Generator |
| Declarations | 1 structure (`DirectionalResidual`), 18 defs, 32 theorems in two namespaces (`PresentationRelativity`, `PresentationRelativity.Metatheory`). (The inventory JSON lists 34 theorems: "`constructs`" and "`selects`" are prose words following the word "theorem" in docstrings at lines 25 and 606, not declarations.) |
| Axiom reports in `artifacts/lean_axioms.txt` | 32 lines (`Derivation.lean:1414`–`1445`); axioms seen: none (3), `propext` (3), `Quot.sound` (10), `propext, Quot.sound` (16). All 32 theorems are reported. |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module makes "two presentations are the same" a relative, typed relation on a supplied finite list of represented data `D`: two maps `p q : Nat → Nat` are identical on `D` when each factors through the other (`PresentationIdentityOn`). It proves this is exactly equality of the fiber relations they induce on `D`, exactly the absence of a *directional residual* (a represented pair `p` identifies and `q` separates) in both directions, and an equivalence relation. It then turns a factorization failure into a forced repair: if a supplied comparison `q` does not factor through `p` on `D`, there is a represented pair that every presentation carrying both `p` and `q` must split, with strictly larger class count; one such joint refinement, `pQ D [p,q]`, is exhibited without any claim that it is natural or preferred. The remaining sections re-read earlier results as presentation-indexed: within the seven-field `World` record the support projection identifies what the support-plus-notes view separates and notes never affect kernel results; admitting an evaluator refines the panel's joint quotient and can withdraw a negative certificate while the stored world is unchanged; and the declared generator's depth-one profile identifies the pair `1,2` that the identity-grade comparison separates, so the forced-refinement theorem applies at every `n ≥ 3` once `id` is *supplied*. A fenced `Metatheory` namespace shows that an attempted all-view identification predicate, quantified over ambient Lean types, collapses to equality and both "all views separate" and "all views identify" are refuted for a distinct pair.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `FiberIdentityOn D p q` | 62 | def | `∀ x y ∈ D, (p x = p y ↔ q x = q y)`. | ADMITTED |
| `PresentationIdentityOn D p q` | 68 | def | `FactorsOn D p q ∧ FactorsOn D q p` (mutual factorization on `D`). | ADMITTED (declared notion of relative identity) |
| `DirectionalResidual D p q` | 91 | structure | Data: `left right ∈ D`, `p left = p right`, `q left ≠ q right`. | ADMITTED |
| `ResidualEmptyOn D p q` | 113 | def | No `DirectionalResidual` in either direction (`¬ Nonempty …`). | ADMITTED |
| `IdentityRelativeToQuestions D Q p` | 179 | def | `PresentationIdentityOn D p (pQ D Q)`. | ADMITTED |
| `DirectionalResidualAt D p q x` | 200 | def | `∃ y ∈ D, p x = p y ∧ q x ≠ q y`. | ADMITTED |
| `jointPresentation D p q` | 327 | def | `pQ D [p, q]` — the ordered first-match signature presentation of the two-question family. | ADMITTED (a declared construction; docstring disclaims naturality) |
| `ViewIdentifies view x y` | 382 | def | `view x = view y`. | ADMITTED |
| `ViewSeparates view x y` | 385 | def | `view x ≠ view y`. | ADMITTED |
| `Metatheory.AllViewsIdentify x y` | 394 | def | `∀ (Y : Type) (view : X → Y), view x = view y`. Quantifies over the ambient universe `Type`. | ADMITTED (fenced diagnostic) |
| `supportNotesView w` | 427 | def | `(supp w, w.notes)`. | ADMITTED |
| `coarsePanel` | 522 | def | `[[[0,1]],[[0,1]]]` — two evaluators each with the single column `[0,1]`. | ADMITTED (fixture) |
| `separatingEvaluator` | 524 | def | `[[0]]`. | ADMITTED (fixture) |
| `sourcePanelWorld w` | 526 | def | `⟨w, coarsePanel⟩ : CWorld`. | ADMITTED (fixture) |
| `extendedPanelWorld w` | 529 | def | `stepC (sourcePanelWorld w) (.admitEvaluator separatingEvaluator)`. | ADMITTED (fixture) |
| `boolBit` | 547 | def | `false ↦ 0`, `true ↦ 1`. | ADMITTED |
| `encodeDepthOneProfile` | 553 | def | `4b₁ + 2b₂ + b₃` on `Bool × Bool × Bool`. | ADMITTED |
| `depthOnePresentation s i` | 565 | def | `encodeDepthOneProfile (profile1 s i)`. | ADMITTED |
| `generatorDomain n` | 574 | def | `List.range (n+1)`. | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `presentationIdentity_iff_fiberIdentity` | 71 | For every `D p q`, mutual factorization on `D` iff fiber identity on `D`. | FROZEN | Quot.sound | S |
| `directionalResidual_refutes_identity` | 100 | A `DirectionalResidual D p q` refutes `PresentationIdentityOn D p q`. | FROZEN | Quot.sound | S |
| `presentationIdentity_iff_residualEmpty` | 117 | Mutual factorization iff residual empty in both directions (uses `decide` on `Nat` equality). | FROZEN | Quot.sound | S |
| `presentationIdentity_equivalence` | 146 | `PresentationIdentityOn D` is an `Equivalence` on `Nat → Nat`. | FROZEN | Quot.sound | S |
| `self_comparison_has_empty_residual` | 169 | `ResidualEmptyOn D p p`. | FROZEN | Quot.sound | A |
| `identityRelativeToQuestions_iff` | 183 | `IdentityRelativeToQuestions D Q p` iff `∀ x y ∈ D, (p x = p y ↔ SigEq Q x y)`. | FROZEN | Quot.sound | A |
| `splitsAt_iff_directionalResidualAt` | 207 | For `x ∈ D`: `SplitsAt D Q Q' x ↔ DirectionalResidualAt D (pQ D Q) (pQ D Q') x`. | FROZEN | Quot.sound | S |
| `family_enlargement_refines` | 225 | If `Q ⊆ Q'` then `FactorsOn D (pQ D Q') (pQ D Q)`. | CONDITIONAL: `hsub : ∀ q ∈ Q, q ∈ Q'` | Quot.sound | A |
| `family_split_refuses_relative_identity` | 239 | If `x ∈ D` and `SplitsAt D Q Q' x` then `¬ PresentationIdentityOn D (pQ D Q) (pQ D Q')`. | CONDITIONAL: a witnessed split | Quot.sound | A |
| `family_enlargement_split_is_strict` | 251 | Under `Q ⊆ Q'` and a split at `x ∈ D`: `pQ D Q'` refines `pQ D Q` and they are not identical. | CONDITIONAL: `hsub`, `hs` | Quot.sound | S |
| `classCount_lt_of_refinement_split` | 265 | If `FactorsOn D r p`, `x y ∈ D`, `p x = p y`, `r x ≠ r y` then `classCount D [p] < classCount D [r]`. | CONDITIONAL: `FactorsOn D r p` and a split pair | propext, Quot.sound | S |
| `forced_split_of_factorization_failure` | 290 | If `¬ FactorsOn D p q` then `∃ x y ∈ D` with `p x = p y`, `q x ≠ q y`, and every `r` with `FactorsOn D r p ∧ FactorsOn D r q` has `r x ≠ r y` and larger class count. | CONDITIONAL: `¬ FactorsOn D p q` (the comparison `q` is supplied) | propext, Quot.sound | S |
| `jointPresentation_factors_left` | 332 | `FactorsOn D (pQ D [p,q]) p`. | FROZEN | propext, Quot.sound | A |
| `jointPresentation_factors_right` | 342 | `FactorsOn D (pQ D [p,q]) q`. | FROZEN | propext, Quot.sound | A |
| `jointPresentation_strict_of_factorization_failure` | 356 | Under `¬ FactorsOn D p q`: the joint presentation carries `p` and `q` and has strictly larger class count than `p`. | CONDITIONAL: `¬ FactorsOn D p q` | propext, Quot.sound | S |
| `directionalResidual_of_factorization_failure` | 372 | Under `¬ FactorsOn D p q`: `Nonempty (DirectionalResidual D p q)`. | CONDITIONAL: `¬ FactorsOn D p q` | propext, Quot.sound | A |
| `Metatheory.attempted_absolute_identification_collapses_to_equality` | 399 | `AllViewsIdentify x y ↔ x = y` (via `view := id`). | FROZEN (metatheoretic diagnostic; see §4) | none | S (as a warning) |
| `Metatheory.attempted_absolute_polarities_are_refuted` | 413 | For `x ≠ y`: not all ambient views separate them (constant view), and not all identify them (`id`). | CONDITIONAL: `x ≠ y` (metatheoretic diagnostic) | none | S (as a warning) |
| `world_eq_iff_support_eq_and_notes_eq` | 433 | `w = w' ↔ supp w = supp w' ∧ w.notes = w'.notes` (record extensionality for the 7-field `World`). | FROZEN (schema-relative) | propext | A |
| `supportNotesView_injective` | 446 | `supportNotesView` is injective. | FROZEN | propext | A |
| `support_identifies_while_supportNotes_separates` | 455 | If `supp w = supp w'` and `w.notes ≠ w'.notes` then `supp` identifies and `supportNotesView` separates. | CONDITIONAL: the two hypotheses (immediate) | none | A |
| `notes_update_kernel_results_agree` | 466 | Replaying any history from `{w with notes := n}` and from `w` gives equal support, repair family, obstruction verdict and quiescence. | FROZEN (instance of `effectual_outside_dichotomy`) | propext, Quot.sound | S |
| `panelEquiv_antitone` | 484 | `small ⊆ large` and `PanelEquiv large i j` imply `PanelEquiv small i j`. | CONDITIONAL: `hsub` | none | A |
| `panel_members_preserved_by_extension` | 493 | Every member of `cw.panel` is a member after `admitEvaluator E`. | FROZEN | propext, Quot.sound | A |
| `panel_extension_refines_equivalence` | 503 | `PanelEquiv` of the extended panel implies `PanelEquiv` of the source panel. | FROZEN | propext, Quot.sound | S |
| `certNeg_extension_implies_source` | 512 | If `cw.panel ≠ []` and the extended panel certifies `i,j` negative then so does the source panel. | CONDITIONAL: `cw.panel ≠ []` | propext, Quot.sound | S |
| `panel_extension_changes_verdict_not_world` | 536 | For every `w`: the extended fixture has the same `base`, the source panel certifies `(0,1)` negative, the extended one does not. | VERIFIED_FINITE (fixed panel, `simp` evaluation; universally quantified over `w` but `w` is inert) | propext, Quot.sound | S |
| `encodeDepthOneProfile_injective` | 556 | The 3-bit code is injective (64 cases). | VERIFIED_FINITE | propext | A |
| `depthOnePresentation_eq_iff` | 568 | `depthOnePresentation s i = depthOnePresentation s j ↔ profile1 s i = profile1 s j`. | FROZEN | propext, Quot.sound | A |
| `declared_generator_index_comparison_does_not_factor` | 582 | For `3 ≤ n`, `¬ FactorsOn (range (n+1)) (depthOnePresentation (reflState n)) id`. | CONDITIONAL: `3 ≤ n` | propext, Quot.sound | S |
| `declared_generator_index_comparison_forces_refinement` | 607 | For `3 ≤ n`, the forced-split conclusion for `p := depthOnePresentation (reflState n)`, `q := id`. | CONDITIONAL: `3 ≤ n`; `id` is the supplied comparison | propext, Quot.sound | S |
| `declared_generator_profiles_disagree_at_pair` | 630 | For `3 ≤ n`, `profile1 (reflState n)` identifies `1,2` and `profileV (reflState n)` separates them. | CONDITIONAL: `3 ≤ n` | propext, Quot.sound | A |

## 4. External and admitted assumptions

- Structures/definitions taken as given: `FactorsOn`, `FiberConstant`, `factors_iff_fiberConstant`, `pQ`, `pQ_exact`, `SigEq`, `SplitsAt`, `enlarge_refines`, `classCount`, `count_lt_of_split`, `sigList` (Compression); `World`, `Supp`, `supp`, `replay`, `repairFamily`, `obstructedB`, `quiescentB`, `effectual_outside_dichotomy`, `CWorld`, `stepC`, `Evaluator = List View`, `PanelEquiv`, `certNegB/C`, `certNeg_iff_panelEquiv`, `admitEvaluator_base_inert` (Represented/NoOutside); `PState`, `reflState`, `profile1`, `profileV`, `generation_never_dries`, `valued_marks_collapse_generation` (Generator).
- Presentations are `Nat → Nat` functions (metatheoretic data; finitude rule). Every theorem restricts them to a supplied finite list `D`, so the *content* is finite; but the objects quantified over (`p q r : Nat → Nat`, `Q : List (Nat → Nat)`) are ambient Lean functions. The docstrings say "supplied" and "represented list of natural numbers"; the flag stands as a reading hazard, not a defect.
- `Metatheory.AllViewsIdentify` quantifies over `(Y : Type) (view : X → Y)` — an unrestricted external universe used deliberately as a diagnostic. The module header (lines 45–47) and the ledger say these functions are not stored in `World`, admitted to `CWorld`, or produced by replay. Flagged as the finitude rule requires; the module itself already flags it.
- Unearned identity: none found. Equalities are either field-wise record extensionality (`world_eq_iff_support_eq_and_notes_eq`, proved by `rcases`) or consequences of `pQ_exact`/`factors_iff_fiberConstant`.
- Unrestricted external universe: present only in `Metatheory` (see above), fenced.
- Unbounded function treated as internally available: `id : Nat → Nat` is *supplied* as the comparison in §6; the docstrings (lines 580–581, 602–606) say "imported demand", "not generated by the depth-one profile". `generatorDomain n = List.range (n+1)` is finite for each `n`. None found beyond the stated supply.
- Silently assumed observer: none found; every claim names `D`, `p`, `q`, the panel or the profile.
- Unspecified correspondence between presentations: none found — identity is *defined* as mutual `FactorsOn` and the correspondence is the factoring map `g`.
- Cost function: `classCount` (the number of distinct signatures over `D`) is used as the measure of "strictly finer". It is a declared count from Compression, not a cost with a justification; the theorems only use its strict monotonicity under a split (`count_lt_of_split`). Not presented as a cost.
- Admitted condition later described as forced: the word "forced" in `forced_split_of_factorization_failure` is conditional on the supplied `q` not factoring; both the docstring and ledger say "The comparison `q` is supplied … not generated". None found beyond that.
- Finite computation presented as universal: `panel_extension_changes_verdict_not_world` is a `simp` evaluation on a fixed two-evaluator panel; its `∀ w` is genuine only because `certNegC` ignores `base`. Labelled as a fixture in the docstring. None found.
- Library lemmas doing real work: `decide`/`of_decide_eq_true`/`of_decide_eq_false` on `Nat` equalities and on the decidable `∃ x ∈ D, …` (list-bounded existential — decidable because `D` is a `List`); `List.mem_append_left`; `simp` with `Supp.mk.injEq`; `omega`.

## 5. Derived consequences

- `ClosureSymmetry` imports this module and uses `DirectionalResidual`, `PresentationIdentityOn`, `FactorsOn`-based statements (checked: `ClosureSymmetry.lean` opens `PresentationRelativity` and defines `transpose` on `DirectionalResidual`).
- `ResidualClosure` (via `ClosureSymmetry`) instantiates the residual notions on the current observer.
- `NoOutsideFidelity` imports it and reuses `notes_update_kernel_results_agree` (re-exported as `notes_fiber_has_no_operational_authority`); `support_identifies_while_supportNotes_separates` is not used there (grep: none).
- Paper: `paper/paper_claim_ledger.md` CL-PREL-RELATIVE-IDENTITY; `paper/native_derivation_completion.md` lines ~343–360 (NC3 "partially closed at the one-step refinement law"); `paper/endogenous_generator.md` lines ~229–239 (conditional refinement mechanism under "endogenous demands, exogenous payments"); change log 2026-08-14. `paper/paper.md` does not cite this module's theorem names (grep: none).
- `code/derivation/completion.py` binds 15 of the theorem names to classification tags (`generic`, `equivalence`/`classification`/`existence`/…) for the completion dependency graph; this is an inventory binding, not a computation of the mathematics.

## 6. Counterexamples and limitations

- Countermodels: `directionalResidual_refutes_identity` (a residual refutes identity); `attempted_absolute_polarities_are_refuted` (constant view and `id` refute both absolute polarities for any `x ≠ y`); `panel_extension_changes_verdict_not_world` (the converse of `certNeg_extension_implies_source` fails: extending the panel with `[[0]]` withdraws the negative certificate on `(0,1)`); `declared_generator_index_comparison_does_not_factor` (the pair `1,2`).
- The forced-split theorem is a *finite common-carrier* result over `List Nat`; the heterogeneous version is in `PresentationDescent`, not here (the header says so).
- `forced_split_of_factorization_failure` is vacuous on `D = []` (every map factors through every other there; probe confirmed `FactorsOn [] p q` holds). Not a defect: the hypothesis `¬ FactorsOn` is simply unsatisfiable there.
- `jointPresentation` is one declared refinement; the module proves nothing about minimality, uniqueness or naturality of it, and says so.
- The "generator instance" uses the supplied `id`; it does not close G1 (ledger non-claim) and does not show the depth-one profile generates any comparison demand.
- `Metatheory` results are about ambient Lean functions, not about any observer the system possesses; reading them as "the system has no absolute outside" is excluded by the header and ledger (`ABSOLUTE_NO_OUTSIDE_UNFORMULABLE` retained).

## 7. Axiom dependencies

All 32 reports lie within {propext, Quot.sound}; 4 are axiom-free (the two `Metatheory.*` diagnostics, `support_identifies_while_supportNotes_separates`, `panelEquiv_antitone`), 3 use `propext` only, 10 `Quot.sound` only, 15 both. Nothing exceeds the pair: none.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All 32 theorems appear in `artifacts/lean_axioms.txt` (`Derivation.lean:1414`–`1445`). The ledger's "all 32 `PresentationRelativity.*` theorem reports" matches.
- Paper cites: ledger CL-PREL-RELATIVE-IDENTITY; `native_derivation_completion.md`; `endogenous_generator.md`; change log. Not in `paper/paper.md` by name.
- Probe: `textbook/audit/probes/F2/prel_probe.lean`, `lake env lean` inside `lean4/`, exit 0. Results: `forced_split_of_factorization_failure` axioms `[propext, Quot.sound]`; `Metatheory.attempted_absolute_identification_collapses_to_equality` axiom-free; `FactorsOn [] p q` holds for all `p q` (vacuity note above); on `D = [0,1]`, `p := const 0`, `q := id`, `¬ FactorsOn` is provable and `#eval` gives `classCount [0,1] [p] = 1`, `classCount [0,1] [jointPresentation [0,1] p id] = 2`, confirming the strict-growth conclusion on the smallest instance; `AllViewsIdentify : {X : Type} → X → X → Prop` quantifies over `Type`.

## 9. Related Python implementations

- `code/derivation/completion.py` lines 692–700: name-to-tag bindings for 15 theorems of this module (dependency-graph inventory, not an implementation of the notions).
- `tests/test_completion.py` lines 232–236: pins those tags.
- `tests/test_model.py:34` `test_admit_datum_dedups_on_presentation_identity`: tests the kernel's deduplication on *presentation identity* of data tokens in `model.py`, a different (earlier) notion from this module's `PresentationIdentityOn`; related by name only.
- No Python computes `FactorsOn`, `DirectionalResidual`, `jointPresentation` or `classCount` splits for this module (the ledger: "inventory and receipt binding only").

## 10. Textbook placement proposal

- Prerequisites: `FactorsOn`, `FiberConstant`, `pQ`, `SigEq`, `SplitsAt`, `classCount` (Compression); the `World`/`Supp` record and `supp` (Represented); `CWorld`, panels, `certNegB`, `PanelEquiv` (NoOutside); `reflState`, `profile1`, `generation_never_dries` (Generator).
- Substantive: the three identity equivalences (`…_iff_fiberIdentity`, `…_iff_residualEmpty`, `…_equivalence`) and `directionalResidual_refutes_identity`; `splitsAt_iff_directionalResidualAt`; the forced-refinement spine (`classCount_lt_of_refinement_split`, `forced_split_of_factorization_failure`, `jointPresentation_strict_of_factorization_failure`); `notes_update_kernel_results_agree`; `panel_extension_refines_equivalence` + `certNeg_extension_implies_source` + the fixture `panel_extension_changes_verdict_not_world`; the two `Metatheory` diagnostics (taught as "what the ambient quantifier does, and why it is not a system observer"); `declared_generator_index_comparison_forces_refinement` with the explicit note that `id` is supplied.
- Auxiliary: `self_comparison_has_empty_residual`, `identityRelativeToQuestions_iff`, `family_enlargement_refines`, `family_split_refuses_relative_identity`, `family_enlargement_split_is_strict`, both `jointPresentation_factors_*`, `directionalResidual_of_factorization_failure`, `world_eq_iff_…`, `supportNotesView_injective`, `support_identifies_while_…`, `panelEquiv_antitone`, `panel_members_preserved_by_extension`, `encodeDepthOneProfile_injective`, `depthOnePresentation_eq_iff`, `declared_generator_profiles_disagree_at_pair`.
- Suggested lesson: "When are two presentations the same, and what does a failed comparison force?" — answering: identity is mutual factorization on the supplied data, equivalently no directional residual; a residual forces every joint refinement to split that pair and grow the class count by at least one, and one such refinement can be written down.
- Recommend omitting from the textbook: `encodeDepthOneProfile_injective` (a 64-case coding lemma); `world_eq_iff_support_eq_and_notes_eq` (schema extensionality, better stated in prose); `declared_generator_profiles_disagree_at_pair` (a restatement of two Generator theorems).

## 11. Interpretation findings

1. **`forced_split_of_factorization_failure` — "forced".** Lean: conditional on a *supplied* `q` with `¬ FactorsOn D p q`. The ledger and `endogenous_generator.md` both say the comparison is supplied, not generated. `endogenous_generator.md` line 229 calls it "the conditional refinement mechanism"; correct. None found.
2. **`declared_generator_index_comparison_forces_refinement` — docstring "the declared generator is a concrete instance of comparison-forced refinement".** Lean: `q := id`, i.e. an identity-grade comparison supplied from outside the depth-one regime. The docstring's first word is "Conditional on the supplied index comparison" and the ledger says it "does not close G1". None found, but a textbook must not phrase this as "the generator forces its own refinement".
3. **`Metatheory.attempted_absolute_identification_collapses_to_equality`.** Statement quantifies over `(Y : Type) (view : X → Y)`. If read as "the system can test whether all views identify `x y`", it would attribute an unrestricted universe to the system (finitude rule). Both the header (lines 45–47) and ledger ("quantify over ambient Lean functions … do not admit such views") read it correctly. None found; flagged for the textbook.
4. **`panel_extension_changes_verdict_not_world (w : World)`** — the `∀ w` could be read as "for every world the panel extension changes the verdict" with the world playing a role. In fact `certNegC` reads only `cw.panel`, so `w` is inert; the statement is a fixed finite computation on `coarsePanel`/`separatingEvaluator`. The docstring says "For every supplied base record … changes only the observation apparatus", which is accurate. Marked VERIFIED_FINITE rather than FROZEN for this reason. INTERPRETATION hazard, no defect found.
5. **`native_derivation_completion.md` line ~343: "`PresentationRelativity` makes the relative content exact."** The three equivalences are indeed `↔` theorems over all `D p q`; "exact" is justified. None found.
6. Vacuity checks: `forced_split_of_factorization_failure` is vacuous for `D = []` and for any `D` on which `q` factors through `p` (hypothesis unsatisfiable), non-vacuous on `D=[0,1]`, `p` constant, `q = id` (probe). `certNeg_extension_implies_source` requires `cw.panel ≠ []` because `certNegB [] i j = false`; without it the statement would still hold vacuously for the extended panel? — not checked (the hypothesis is used through `certNeg_iff_panelEquiv`). `attempted_absolute_polarities_are_refuted` requires `x ≠ y`; for `x = y` the second conjunct is false, so the hypothesis is necessary. No vacuous theorem found.
