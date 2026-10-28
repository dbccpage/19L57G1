# Audit: ContactBridge

| field | value |
|---|---|
| Path | lean4/Derivation/ContactBridge.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 1b23a9e7f1b730ab |
| Lines | 710 (inventory says 711; `wc -l` gives 710) |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.ObsDescent, Derivation.PrimitiveCore, Derivation.PrimitiveCats, Derivation.Apartness, Derivation.PrimitivePassage |
| Declarations | def 8, theorem 35, inductive 1 (`Tri`); two of the defs are `String` labels naming OPEN cells |
| Axiom reports in `artifacts/lean_axioms.txt` | 35 lines (every theorem); 29 "none", `triSym_not_obs_complement` propext, `pair_blocked_is_collapse_collision` Quot.sound, `declared_zero_as_view` / `observation_stage_realizes_observer` / `collapse_collision_is_pair_blocked` / `pair_blocked_iff_collapse_collision` propext+Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found (grep over the file; the word "axiom" does not occur) |

## 1. Mathematical purpose

The module is the first of the two "collision" modules: it puts the native difference observer (`DiffInterface.DiffObs`, a difference map with a zero predicate and three law fields) side by side with the arriving apartness signature (`Apartness.IsApart`: irreflexive, symmetric, cotransitive) and asks, in both directions, what one buys from the other and at what price. The native-to-arriving direction defines the complement of the zero relation (`obsApart`) and shows which of the nine native candidate readings of primitive difference (W, A, Bs, Bc, Bl, C, D, E, F from `PrimitiveCore`) hold for the setting an observer induces, once a non-zero pair is handed over as a hypothesis. The arriving-to-native direction builds an observer from an admitted apartness (`apartObs`) by spending its three admitted fields one for one. The module then prices the three unconditional law schemas (cotransitivity, stability, locatedness over every observer) against the weak law of excluded middle and double-negation elimination, gives a characterization of which relations are zero-complements of a Prop-valued observer, exhibits four compiled countermodels (carriers 1, 2, 3, 2) to representability, and places the arriving observer stratum at the passage's declared observation stage, where the zero column list of `PrimitivePassage` is shown to be a kernel observer's zero relation. Finally it ties `ActiveObstruction`-style "pair blocked" to a collapse collision through `ObsDescent`'s quotient. It is read, not system content: every quantifier over `X R : Type` and every `∀ P : Prop` is metatheory.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `obsApart` | 116 | def | `obsApart O x y := ¬ ZeroRel O x y`, the complement of an observer's zero relation | ADMITTED (definition) |
| `obsSetting` | 143 | def | the native `Setting` an observer induces given a pair `a b`: `X`, `r := obsApart O`, `ret := False`, `prot := False`, `Ops := False` (empty stores; probe: `ret`/`prot` are `False` by `rfl`) | ADMITTED (definition; the empty stores are a declared policy) |
| `apartObs` | 224 | def | `DiffObs X Prop` from `r` and `h : IsApart r`: `delta := r`, `Zero := Not`; `zero_refl := h.irrefl`, `zero_symm` from `h.symm`, `zero_trans` from `h.cotrans` (probe: `zero_refl` is literally `h.irrefl` by `rfl`) | ADMITTED (definition; the three law fields are discharged by the three admitted `IsApart` fields, one for one) |
| `Tri` | 443 | inductive | a three-point carrier `t0 | t1 | t2` used by `wlemZero` | ADMITTED |
| `wlemZero` | 454 | def | a `DiffObs Tri Prop` parametrized by a proposition `P`, whose zero relation puts `t0 ~ t1` iff `P`, `t1 ~ t2` iff `¬P` (and so on), the carrier used to extract WLEM from a cotransitivity schema | ADMITTED (construction inside a proof) |
| `open_bridge_cotrans` | 607 | def (String) | label for the OPEN cell: unconditional cotransitivity of `obsApart` for a fixed observer, priced at WLEM for the schema | OPEN |
| `open_bridge_located` | 612 | def (String) | label for the OPEN cell: unconditional locatedness, priced at (at least) WLEM for the schema | OPEN |
| `colView` | 620 | def | `colView cols : Nat → List Bool`, the view that reads the passage's observation column list `cols : List (List Nat)` at a point `i` as the list of membership bits | ADMITTED (definition over `Nat`; metatheoretic function) |
| `kernelStage` | 657 | def | the `DiffInterface.Stage` with `live := True`, `retained := False`, `guarded := False`, `obs := O` | ADMITTED (declared policy: no retention, no guarding) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `obsApart_irrefl` | 119 | for any `O : DiffObs X R`, `¬ obsApart O x x` (contrapositive of the `zero_refl` field) | FROZEN | none | S |
| `obsApart_symm` | 124 | `obsApart O x y → obsApart O y x` (contrapositive of `zero_symm`) | FROZEN | none | S |
| `obsApart_stable` | 130 | `¬¬ obsApart O x y → obsApart O x y` (triple negation collapses; pure logic) | FROZEN | none | S |
| `zeroRel_indist` | 135 | `ZeroRel O x y → Apartness.Indist (obsApart O) x y` (one direction only: a zero pair is indistinguishable in the complement; proof `fun hz hn => hn hz`) | FROZEN | none | A |
| `obsSetting_w` | 156 | given `hab : obsApart O a b`, candidate W holds for `obsSetting O a b` | CONDITIONAL:`hab : obsApart O a b` | none | S |
| `obsSetting_a` | 161 | with `hab`, candidate A (witness + irreflexivity) holds | CONDITIONAL:`hab` | none | S |
| `obsSetting_bs` | 166 | with `hab`, candidate Bs (A + symmetry) holds | CONDITIONAL:`hab` | none | S |
| `obsApart_cotrans` | 175 | under `[∀ x y, Decidable (ZeroRel O x y)]`, `obsApart O` is cotransitive | CONDITIONAL:`Decidable (ZeroRel O x y)` pointwise | none | S |
| `obsSetting_bc` | 184 | with `hab` and pointwise decidability of ZeroRel, candidate Bc (A + cotransitivity) holds | CONDITIONAL:`hab`, `Decidable (ZeroRel …)` | none | S |
| `obsSetting_bl` | 193 | with `hab` and pointwise decidability, candidate Bl (located) holds: the decision procedure is the `Bool` function | CONDITIONAL:`hab`, `Decidable (ZeroRel …)` | none | S |
| `obsSetting_d` | 203 | with `hab`, candidate D (witness, irreflexive, no prot requirement) holds | CONDITIONAL:`hab` | none | S |
| `obsSetting_e` | 211 | with `hab`, candidate E holds at the empty operation family (via sealed `e_empty_iff_d`) | CONDITIONAL:`hab`; the empty `Ops` is by construction | none | S |
| `apartObs_zeroRel` | 236 | `ZeroRel (apartObs r h) x y ↔ ¬ r x y` | FROZEN (`Iff.rfl`) | none | A |
| `apartObs_roundtrip` | 244 | under `IsApart r` and `[Decidable (r x y)]` pointwise, `obsApart (apartObs r h) x y ↔ r x y` | CONDITIONAL:`IsApart r`, `Decidable (r x y)` | none | S |
| `isApart_repr` | 256 | under the same two hypotheses, `∃ O : DiffObs X Prop, ∀ x y, obsApart O x y ↔ r x y` | CONDITIONAL:`IsApart r`, `Decidable (r x y)` | none | S |
| `obsApart_isApart` | 265 | under `[∀ x y, Decidable (ZeroRel O x y)]`, `IsApart (obsApart O)` | CONDITIONAL:`Decidable (ZeroRel …)` | none | S |
| `indist_obsApart_iff` | 274 | under the same decidability, `Indist (obsApart O) x y ↔ ZeroRel O x y` | CONDITIONAL:`Decidable (ZeroRel …)` | none | S |
| `obsSetting_not_c` | 290 | `¬ C (obsSetting O a b)`: C needs a protected pair and `prot` is `False` by construction | FROZEN (definitional) | none | A |
| `obsSetting_not_f` | 297 | `¬ F (obsSetting O a b)`: F needs retention and `ret` is `False` by construction | FROZEN (definitional) | none | A |
| `kernel_prot_independent` | 304 | with `hab : obsApart O a b`: `C` holds for `obsSetting O a b` with `prot` replaced by `fun _ _ => True`, and `¬ C (obsSetting O a b)` — protection is declarable, never derived | CONDITIONAL:`hab` | none | A |
| `obsApart_repr_iff` | 319 | for `r : X → X → Prop`: `(∃ O : DiffObs X Prop, ∀ x y, obsApart O x y ↔ r x y) ↔ Equivalence (¬ r) ∧ ∀ x y, ¬¬ r x y → r x y` (probe-checked statement) | FROZEN; Prop-valued observers only | none | S |
| `unit_total_not_repr` | 350 | `¬ ∃ O : DiffObs Unit Prop, ∀ x y, obsApart O x y ↔ True` (the total relation on one point is no Prop-valued zero-complement) | REFUTED (carrier 1; Prop-valued only) | none | S |
| `d2_not_obs_complement` | 362 | `¬ ∃ (R : Type) (O : DiffObs Bool R), ∀ x y, obsApart O x y ↔ PrimDiff.D2 x y` (the oriented two-point relation is not a zero-complement for any value type in universe 0) | REFUTED (carrier 2) | none | S |
| `triSym_not_obs_complement` | 377 | `¬ ∃ (R : Type) (O : DiffObs (Fin 3) R), ∀ x y, obsApart O x y ↔ Apartness.triSymRel x y` (uses `symm_without_cotrans_breaks_trans`) | REFUTED (carrier 3) | propext | S |
| `bool_bs_repr` | 398 | on `Bool`, any `r` with a witness `hw : r a b`, irreflexivity and symmetry is the zero-complement of some `DiffObs Bool Prop`, with no decidability hypothesis | CONDITIONAL:`r a b`, `Irrefl r`, symmetry; carrier `Bool` | none | S |
| `d_not_witnessed_repr` | 426 | `¬ ∃ (R : Type) (O : DiffObs Bool R), (∀ x y, obsApart O x y ↔ False) ∧ obsApart O false true` (an all-zero observer carries no endpoint witness; any value type in universe 0) | REFUTED (carrier 2; trivially, the two conjuncts contradict) | none | A |
| `cotrans_schema_iff_wlem` | 519 | `(∀ (X R : Type) (O : DiffObs X R), Cotrans (obsApart O)) ↔ ∀ P : Prop, ¬P ∨ ¬¬P` (probe-checked statement) | FROZEN (schema equivalence; the classical principle is a quantified statement, never a proof step) | none | S |
| `stability_schema_iff_dne` | 550 | `(∀ (X R : Type) (O : DiffObs X R), ∀ x y, ¬¬ ZeroRel O x y → ZeroRel O x y) ↔ ∀ P : Prop, ¬¬P → P` | FROZEN (schema equivalence) | none | S |
| `located_schema_implies_wlem` | 578 | `(∀ (X R : Type) (O : DiffObs X R), Located (obsApart O)) → ∀ P, ¬P ∨ ¬¬P` (one direction only) | FROZEN (one implication; converse OPEN) | none | S |
| `declared_zero_as_view` | 628 | for `cols : List (List Nat)` and `i j : Nat`: `PrimitivePassage.zeroP cols i j = true ↔ ZeroRel (kernelObs (colView cols)) i j` (list induction; the passage's declared zero column list is a kernel observer's view-equality) | FROZEN (over `Nat` and `List`; metatheoretic carrier) | propext, Quot.sound | S |
| `observation_stage_realizes_observer` | 648 | `∀ cols, ∃ O : DiffObs Nat (List Bool × List Bool), ∀ i j, zeroP cols i j = true ↔ ZeroRel O i j` (existential packaging of the previous) | FROZEN (carrier `Nat`) | propext, Quot.sound | S |
| `kernel_stage_no_obstruction` | 666 | `¬ ActiveObstruction (kernelStage O) x y`; proof `fun _ _ h => h.1` since `retained := False` | FROZEN but near-definitional (holds by the declared `retained := False`, not by any property of `O`) | none | A |
| `pair_blocked_is_collapse_collision` | 678 | for `ψ : X → Z` and the kernel observer of `ψ`: a non-zero pair (`ψ x ≠ ψ y`) gives distinct classes `ObsQuotient.mk` | FROZEN | Quot.sound | A |
| `collapse_collision_is_pair_blocked` | 688 | the converse: distinct quotient classes give `ψ x ≠ ψ y` (uses `obsQuotient_mk_eq_iff`) | FROZEN | propext, Quot.sound | A |
| `pair_blocked_iff_collapse_collision` | 701 | the biconditional of the two | FROZEN | propext, Quot.sound | S |

Note: `d_not_witnessed_repr` is immediate (its two conjuncts contradict at `(false, true)`); its content is the pairing of the D-reading with the all-zero observer, not a proof step.

## 4. External and admitted assumptions

- **Structures taken as given**: `DiffInterface.DiffObs X R` (three law fields `zero_refl`, `zero_symm`, `zero_trans` are PROOF FIELDS, i.e. admitted at every instance); `Apartness.IsApart r` (three admitted fields); `PrimitiveCore.Setting` and the nine candidate predicates; `DiffInterface.Stage`, `ActiveObstruction`; `PrimitivePassage.zeroP`; `ObsDescent`/`DiffInterface.ObsQuotient`.
- **Recurring hypotheses**: `hab : obsApart O a b` (a chosen non-zero pair, handed in — the observer does not supply it; cf. `ContactKernel.pair_choice_load_bearing`); `[∀ x y, Decidable (ZeroRel O x y)]` (observer→apartness direction); `[∀ x y, Decidable (r x y)]` + `IsApart r` (apartness→observer direction). The two decidability instances are not interchangeable; the ledger says so explicitly and the module never derives one from the other. Checked: no theorem uses `Classical`.
- **Declared policies**: `obsSetting` and `kernelStage` set retention and protection stores to `False` and the operation family to empty. Every "not C / not F / no obstruction" fact downstream of these is a consequence of the policy, not of the observer.
- **Universe/Type parameters**: all over `Type` (universe 0); `d2_not_obs_complement`, `triSym_not_obs_complement` quantify `∃ R : Type`. The paper's ledger notes the arriving structure is universe-polymorphic — the refutations do not cover other universes (metatheoretic scope limit, correctly stated in the ledger).
- **Functions `Nat → …` treated as data**: `colView cols : Nat → List Bool`; `observation_stage_realizes_observer` produces an observer on carrier `Nat`. These are metatheory (finitude rule): the passage's states are finite lists, but the observer built here is total over `Nat`, which no system state possesses.
- **Library lemmas doing real work**: list induction with `List.elem`/membership decidability in `declared_zero_as_view` (hence propext/Quot.sound); `Quotient.sound`/`Quotient.exact` via `ObsDescent` in the last three.
- Unearned identity: none found. Unrestricted external universe: the `∃ R : Type` refutations are scoped to universe 0 and say so (ledger). Unbounded function treated as internally available: `colView` (flagged above; the docstring does not claim internal availability). Silently assumed observer: none — every observer is a parameter or an explicit construction. Unspecified correspondence between presentations: none found. Cost function: none in this module. Admitted condition later described as forced: see §11 (the "three laws proved" header sentence). Finite computation presented as universal: none found; the three countermodels are stated at their carriers.

## 5. Derived consequences

Imported by `ContactKernel`, `PrimitiveContact`, `DiffAnchor`, `DiffAnchorCompat` and the root. External uses (grep): `colView` ×10 and `declared_zero_as_view` / `observation_stage_realizes_observer` ×3 each (in `ContactKernel`'s passage-entry block and `PrimitiveContact`); `obsApart` ×3; `d2_not_obs_complement` re-exported as `PrimitiveContact.native_interface_not_representable`; `stability_schema_iff_dne` cited by `ContactKernel.open_kernel_grade`; the pair-blocked/collapse-collision trio used once each. Ledger entries: CL-PD2-CONTACT-BRIDGE (all 35 names), CL-PD2-CONTACT-COUNTERMODELS (the refutations and `obsApart_repr_iff`, `bool_bs_repr`). The dependency map's scope note cites `declared_zero_as_view` and `observation_stage_realizes_observer` as the station where "the arriving development ADMITS as three fields what this row PROVES", with the correction that it is an instance-level statement.

## 6. Counterexamples and limitations

- `unit_total_not_repr`: carrier `Unit`, Prop-valued observers only; refutes "the total relation on one point is a zero-complement". Does not refute existence of a Bool-valued (or other-valued) observer on `Unit` with `obsApart = True` — but that is impossible anyway since `obsApart O () ()` contradicts `zero_refl` for any `R`; the restriction to `Prop` is in the statement, not in the mathematics (minor under-statement, no defect).
- `d2_not_obs_complement`: carrier `Bool`, any `R : Type`; refutes orientation arriving through a difference map (symmetry of the zero relation forces symmetry of its complement).
- `triSym_not_obs_complement`: carrier `Fin 3`, any `R : Type`; refutes a symmetric, irreflexive but non-cotransitive relation being a zero-complement (transitivity of the zero relation fails).
- `d_not_witnessed_repr`: carrier `Bool`, any `R : Type`; an all-zero observer (the collapse shape) cannot also carry the endpoint witness `obsApart O false true` — the conjunction refutes itself, which is the point: metatheoretic endpoint distinctness does not become a complement witness.
- What is NOT proved: necessity of decidability for `obsSetting_bc`/`obsSetting_bl` at a fixed observer (only sufficiency; the schema pricing is a different statement — the ledger says so); the converse of `located_schema_implies_wlem` (OPEN, frontier conjecture LOCATEDNESS_SCHEMA_EQUALS_WLEM); `obsApart_repr_iff` backward direction for non-Prop value types; minimality of the carriers except where `bool_bs_repr` supplies it (carrier 3 for triSym). The docstrings of `unit_total_not_repr` say the "minimum carrier one" remark is metatheory.
- `kernel_stage_no_obstruction` proves nothing about observers: it is the `retained := False` policy read back.

## 7. Axiom dependencies

All 35 theorems within {propext, Quot.sound}; 29 use none. Axioms exceeding the budget: none. The classical principles (WLEM, DNE) occur only as quantified statements inside the three pricing theorems; probe confirmed `cotrans_schema_iff_wlem` depends on no axioms.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 35 theorems appear in `artifacts/lean_axioms.txt`. The paper cites every theorem name in CL-PD2-CONTACT-BRIDGE / -COUNTERMODELS and `paper/primitive_difference_contact.md`. Probe `probes/D/bridge_probe.lean` (`lake env lean`, exit 0): `(apartObs r h).zero_refl = fun {x} => h.irrefl x` by `rfl`; `(kernelStage O).retained x y = False` by `rfl`; `obsSetting` `ret`/`prot` are `False` by `rfl`; `#check` of `unit_total_not_repr`, `d2_not_obs_complement`, `obsApart_repr_iff`, `cotrans_schema_iff_wlem`, `observation_stage_realizes_observer` confirmed the statements tabulated above; `#print axioms` of `kernel_stage_no_obstruction`, `obsApart_repr_iff`, `bool_bs_repr`, `d_not_witnessed_repr`, `cotrans_schema_iff_wlem`: none.

## 9. Related Python implementations

`code/derivation/apartness.py` (`is_irrefl`, `is_symm`, `is_cotrans`, `is_apart`, `indist`, `indist_is_equivalence`, `insufficiency_countermodels`) mirrors the arriving side; `artifacts/primitive_contact.json:collision_cells` rows `Obs_to_Bs`, `Obs_to_Bc`, `Obs_to_Bl`, `meet_roundtrip`, `stability_price`, `observer_placement (H1)` and `enumerations.E2_settings_kernels.cotrans_equals_complement_transitivity` (per the ledger; the generating module `code/derivation/primitive_contact.py` is not present at this commit — `ls` fails — so where the JSON is produced was not checked); tests `tests/test_primitive_contact.py::test_equivalence_scope_splits_the_two_decidability_admissions`, `::test_enum_settings_kernels_pinned`, `::test_collision_cells_mirror_lean_literal`; `tests/test_apartness.py`.

## 10. Textbook placement proposal

- Prerequisites: `DiffObs`/`ZeroRel`/`zeroRel_equivalence` (DiffInterface); the nine candidate readings W…F and `Cotrans`/`Located` (PrimitiveCore); `IsApart`/`Indist` (Apartness); `zeroP` and the observation column list (PrimitivePassage); `ObsQuotient` (ObsDescent).
- Substantive: `obsApart` + the three free laws; the conditional cell table (`obsSetting_*`, `obsApart_cotrans`) with its two non-interchangeable decidability admissions; `apartObs` as the "spend three admitted fields" construction; `obsApart_repr_iff`; the three pricing schemas; the four countermodels; `declared_zero_as_view`.
- Auxiliary: `zeroRel_indist`, `apartObs_zeroRel`, `obsSetting_not_c/_not_f`, `kernel_prot_independent`, `kernel_stage_no_obstruction`, the pair-blocked trio.
- Lesson title: "What an observer buys from an apartness, and what it costs back." Question: which of the nine native readings does the complement of a zero relation satisfy for free, and which cost a decidability admission?
- Recommend omitting from the textbook: `kernel_stage_no_obstruction` (a policy read-back), `open_bridge_*` String labels (state the OPEN cells in prose instead).

## 11. Interpretation findings

1. **Module header item 7 vs. `declared_zero_as_view`** — INTERPRETATION DEFECT (minor, already corrected in the dependency map). The header says the stage "*proves* — at the sealed kernelObs, equality-grade — the three laws an arriving observer carries as proof fields". The Lean shows the passage's declared zero list equals `ZeroRel (kernelObs (colView cols))`; the laws there are proved because `kernelObs` is view-equality (`rfl`/`Eq.symm`/`Eq.trans`, DiffInterface line ~54). But `DiffObs` itself carries the laws as fields, and `apartObs` in this very module discharges them from the admitted `IsApart` fields one for one (probe: `zero_refl = h.irrefl` definitionally). So "native proves, arriving admits" is true of the kernel observer at the observation stage, not of native observers in general. The dependency map scope note (2026-08-13) already states this precisely; the module header does not carry the correction.
2. **`kernel_stage_no_obstruction`** — INTERPRETATION DEFECT (minor). Ledger: "with no retention and no guarding nothing obstructs there". The theorem is `fun _ _ h => h.1`: it reads back `retained := False` from `kernelStage`'s definition and says nothing about the observer or the stage's liveness. Faithful to the ledger wording, but a reader could take it as a property of the arriving stratum rather than of the declared policy.
3. **`unit_total_not_repr`** — INTERPRETATION DEFECT (scope, already disclosed). The paper calls it the carrier-1 instance; the Lean refutes only `∃ O : DiffObs Unit Prop`. The ledger says so ("refutes `∃ O : DiffObs Unit Prop` only"). No defect in the prose at this commit; recorded because a lesson should not generalize it to all value types without the (easy) extra argument.
4. **Finitude flags**: `colView : Nat → List Bool` and the carrier `Nat` of `observation_stage_realizes_observer`; the schemas quantify over all `(X R : Type)`; `obsApart_repr_iff` quantifies `∃ O : DiffObs X Prop` (an existential over a structure type). All metatheory; none of the docstrings claims the system owns these objects, but the ledger's phrase "the native side PROVES equality-grade at the passage's declared observation stage" should be read with the carrier `Nat` in mind — the passage state is a finite list, the observer built from it is a total function.
5. **Vacuity check**: the `hab`-conditional theorems are satisfiable (e.g. `kernelObs` with a two-valued view); the decidability instances are satisfiable on finite carriers; the schema antecedents are not provable internally (that is their point) but are classically true, so the biconditionals are not vacuous. `obsSetting_not_c`/`_not_f` have trivially true conclusions by construction (recorded as definitional, not as defects). No vacuous theorem found.
6. PROOF DEFECT: none found.
