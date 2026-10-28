# Audit: PrimitiveCore

| field | value |
|---|---|
| Path | lean4/Derivation/PrimitiveCore.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 013507abbe2be33b |
| Lines | 918 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.PrimDiff |
| Declarations | 1 structure (`Setting`), 31 defs (13 concrete models, 9 candidate predicates, `Cotrans`, `Located`, `triR`, `triSymR`, 4 `open_cell_*` strings, `matrixCells`), 1 instance (`Decidable (triR x y)`), 129 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 81 lines (the 68 matrix theorems, 4 `not_*_of_not_a`, `D_iff_ne`, `located_of_decidable`, `cotrans_auto_on_two`, `e_empty_iff_d`, `prot_not_from_witness`, `ret_not_from_witness`, `f_ops_irrelevant`, `bool_class`, `matrixCells_length`); axioms seen: none / propext / propext+Quot.sound. The 48 model-fact theorems (lines 309–492) are not in the artifact. |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module asks what "a primitive difference" could mean inside one signature and which readings entail which. It fixes a single signature `Setting` (carrier, asserted difference relation, two designated endpoints, a retention store, a protected-demand store, an admitted operation family — and deliberately no observation field) and writes nine candidate readings as predicates on it: a bare witnessed pair W, the pointed witnessed irreflexive relation A, the three "axis" strengthenings Bs/Bc/Bl (symmetry, cotransitivity, locatedness), witnessed non-identification C (fact plus demand), non-factorization through the point D, irreducibility under the admitted family E, and the protected retained difference F. It then settles all 72 ordered cells P→Q: 17 implications proved for every `Setting`, 51 refuted by thirteen concrete finite models on `Unit`, `Bool`, `Fin 3`, and 4 cells into the located axis recorded OPEN with the reason that every decidable relation is located, so no finite countermodel can exist inside the development. The load-bearing content for the programme is that the irreflexivity law is the first thing that forces the endpoints apart (`imp_a_d` against `nimp_w_d`), that demand (protection) and retention are separate declared stores that no witness produces, and that irreducibility is relative to the admitted operation family all the way down (`e_empty_iff_d`, `nimp_d_e`). The literal cell table is exported for a Python cross-check.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Setting` | 36 | structure | carrier `X : Type`, relation `r`, endpoints `a b`, stores `ret prot`, operation family `Ops : (X → X) → Prop` | ADMITTED (the declared common signature; `X : Type` and `Ops` are metatheoretic) |
| `Cotrans` | 49 | def | `∀ x y, r x y → ∀ z, r x z ∨ r z y` | ADMITTED |
| `Located` | 55 | def | `∃ f : X → X → Bool, ∀ x y, r x y ↔ f x y = true` | ADMITTED (metatheoretic existential over a function type; declared "admitted as separate data") |
| `W` | 73 | def | `S.r S.a S.b` | ADMITTED |
| `A` | 76 | def | `S.r S.a S.b ∧ PrimDiff.Irrefl S.r` | ADMITTED |
| `Bs` | 79 | def | `A S ∧ symmetric` | ADMITTED |
| `Bc` | 82 | def | `A S ∧ Cotrans S.r` | ADMITTED |
| `Bl` | 85 | def | `A S ∧ Located S.r` | ADMITTED |
| `C` | 89 | def | `S.r S.a S.b ∧ S.prot S.a S.b` | ADMITTED |
| `D` | 93 | def | `¬ ∃ p : Unit → S.X, p () = S.a ∧ p () = S.b` | ADMITTED (shown equal to `a ≠ b` by `D_iff_ne`) |
| `E` | 99 | def | `PrimDiff.Irred S.Ops S.a S.b` | ADMITTED |
| `F` | 103 | def | `A S ∧ S.ret S.a S.b ∧ S.prot S.a S.b` | ADMITTED |
| `unitBare` | 159 | def | one point, `r` total, stores empty, no ops | ADMITTED (concrete model) |
| `unitFull` | 171 | def | one point, `r` total, stores total | ADMITTED (model) |
| `d2Bare` | 181 | def | `Bool`, `PrimDiff.D2`, false→true, stores empty | ADMITTED (model) |
| `d2Merged` | 192 | def | `d2Bare` with `Ops = {const false}` | ADMITTED (model) |
| `d2Protected` | 202 | def | `d2Bare` with both stores total | ADMITTED (model) |
| `d2ProtectedMerged` | 213 | def | `d2Protected` with `Ops = {const false}` | ADMITTED (model) |
| `s2Bare` | 223 | def | `Bool`, `PrimDiff.S2`, stores empty | ADMITTED (model) |
| `s2Merged` | 233 | def | `s2Bare` with one merger | ADMITTED (model) |
| `triR` | 243 | def | `Fin 3`, the single edge 0→1 | ADMITTED |
| (instance) | 245 | instance | `Decidable (triR x y)` | ADMITTED |
| `triSymR` | 249 | def | `PrimDiff.Sym triR` | ADMITTED |
| `tri` | 253 | def | `Fin 3`, `triR`, endpoints 0,1 | ADMITTED (model) |
| `triProtected` | 264 | def | `tri` with both stores total | ADMITTED (model) |
| `triSym` | 275 | def | `Fin 3`, `triSymR` | ADMITTED (model) |
| `boolEmpty` | 287 | def | `Bool`, empty relation, endpoints false,true | ADMITTED (model) |
| `boolEmptyMerged` | 298 | def | `boolEmpty` with one merger | ADMITTED (model) |
| `open_cell_a_bl` | 545 | def (String) | declared OPEN label for A→Bl | ADMITTED (declared label, not a proposition) |
| `open_cell_bs_bl` | 578 | def (String) | same for Bs→Bl | ADMITTED (label) |
| `open_cell_bc_bl` | 605 | def (String) | same for Bc→Bl | ADMITTED (label) |
| `open_cell_f_bl` | 770 | def (String) | same for F→Bl | ADMITTED (label) |
| `matrixCells` | 841 | def | literal list of 72 `(src, tgt, status)` strings | ADMITTED (declared label table; nothing in Lean ties a row to its theorem) |

## 3. Theorems and lemmas

Abbreviations: `∃S` = `∃ S : Setting, P S ∧ ¬ Q S` (a concrete countermodel refuting the implication P→Q); `∀S` = `∀ S : Setting, P S → Q S`. Axiom column from the artifact; "n/a" = not in artifact (probe values given where run).

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `located_of_decidable` | 64 | if `r` is pointwise decidable (instance) then `Located r` | CONDITIONAL:`[∀ x y, Decidable (r x y)]` | none | S |
| `D_iff_ne` | 107 | for every `Setting`, `D S ↔ S.a ≠ S.b` | FROZEN | none | S |
| `cotrans_auto_on_two` | 121 | every irreflexive relation on `Bool` is cotransitive | CONDITIONAL:`Irrefl r`, carrier fixed to `Bool` | none | S |
| `not_bs_of_not_a` | 137 | `¬ A S → ¬ Bs S` | FROZEN | none | A |
| `not_bc_of_not_a` | 140 | `¬ A S → ¬ Bc S` | FROZEN | none | A |
| `not_bl_of_not_a` | 143 | `¬ A S → ¬ Bl S` | FROZEN | none | A |
| `not_f_of_not_a` | 146 | `¬ A S → ¬ F S` | FROZEN | none | A |
| `unitBare_w` | 309 | `W unitBare` | VERIFIED_FINITE | n/a | A |
| `unitBare_not_a` | 311 | `¬ A unitBare` | VERIFIED_FINITE | n/a | A |
| `unitBare_not_c` | 313 | `¬ C unitBare` | VERIFIED_FINITE | n/a | A |
| `unitBare_not_d` | 315 | `¬ D unitBare` | VERIFIED_FINITE | n/a | A |
| `unitBare_not_e` | 318 | `¬ E unitBare` (identity is in the closure) | VERIFIED_FINITE | n/a | A |
| `unitFull_c` | 321 | `C unitFull` | VERIFIED_FINITE | n/a | A |
| `unitFull_not_a` | 323 | `¬ A unitFull` | VERIFIED_FINITE | n/a | A |
| `unitFull_not_d` | 325 | `¬ D unitFull` | VERIFIED_FINITE | n/a | A |
| `unitFull_not_e` | 328 | `¬ E unitFull` | VERIFIED_FINITE | n/a | A |
| `d2Bare_a` | 331 | `A d2Bare` | VERIFIED_FINITE | n/a | A |
| `d2Merged_a` | 333 | `A d2Merged` | VERIFIED_FINITE | n/a | A |
| `d2Protected_f` | 336 | `F d2Protected` | VERIFIED_FINITE | n/a | A |
| `d2ProtectedMerged_f` | 339 | `F d2ProtectedMerged` | VERIFIED_FINITE | n/a | A |
| `d2_not_symm` | 344 | `PrimDiff.D2` is not symmetric | VERIFIED_FINITE (`decide`) | n/a (probe: none) | A |
| `d2Bare_not_bs` | 347 | `¬ Bs d2Bare` | VERIFIED_FINITE | n/a | A |
| `d2Protected_not_bs` | 349 | `¬ Bs d2Protected` | VERIFIED_FINITE | n/a | A |
| `d2Bare_bc` | 351 | `Bc d2Bare` | VERIFIED_FINITE | n/a | A |
| `d2Merged_bc` | 354 | `Bc d2Merged` | VERIFIED_FINITE | n/a | A |
| `d2Bare_bl` | 357 | `Bl d2Bare` | VERIFIED_FINITE | n/a | A |
| `d2Merged_bl` | 360 | `Bl d2Merged` | VERIFIED_FINITE | n/a | A |
| `d2Bare_not_c` | 363 | `¬ C d2Bare` | VERIFIED_FINITE | n/a | A |
| `d2Bare_not_f` | 365 | `¬ F d2Bare` | VERIFIED_FINITE | n/a | A |
| `d2Merged_not_e` | 367 | `¬ E d2Merged` (via `merger_erases`) | VERIFIED_FINITE | n/a | A |
| `d2ProtectedMerged_not_e` | 371 | `¬ E d2ProtectedMerged` | VERIFIED_FINITE | n/a | A |
| `s2Bare_bs` | 375 | `Bs s2Bare` | VERIFIED_FINITE | n/a | A |
| `s2Merged_bs` | 379 | `Bs s2Merged` | VERIFIED_FINITE | n/a | A |
| `s2Bare_not_c` | 383 | `¬ C s2Bare` | VERIFIED_FINITE | n/a | A |
| `s2Bare_not_f` | 385 | `¬ F s2Bare` | VERIFIED_FINITE | n/a | A |
| `s2Merged_not_e` | 387 | `¬ E s2Merged` | VERIFIED_FINITE | n/a | A |
| `triR_edge` | 391 | `triR 0 1` | VERIFIED_FINITE | n/a | A |
| `triR_irrefl` | 393 | `Irrefl triR` | VERIFIED_FINITE (`decide`) | n/a | A |
| `tri_a` | 398 | `A tri` | VERIFIED_FINITE | n/a | A |
| `tri_bl` | 400 | `Bl tri` | VERIFIED_FINITE | n/a | A |
| `tri_not_bc` | 404 | `¬ Bc tri`: cotransitivity fails at the third point | VERIFIED_FINITE | n/a (probe: propext) | S |
| `triProtected_f` | 416 | `F triProtected` | VERIFIED_FINITE | n/a | A |
| `triProtected_not_bc` | 419 | `¬ Bc triProtected` | VERIFIED_FINITE | n/a | A |
| `triSymR_edge` | 431 | `triSymR 0 1` | VERIFIED_FINITE | n/a | A |
| `triSymR_irrefl` | 433 | `Irrefl triSymR` | VERIFIED_FINITE | n/a | A |
| `triSymR_symm` | 439 | `triSymR` symmetric | VERIFIED_FINITE | n/a | A |
| `triSym_bs` | 444 | `Bs triSym` | VERIFIED_FINITE | n/a | A |
| `triSym_not_bc` | 450 | `¬ Bc triSym` | VERIFIED_FINITE | n/a (probe: propext) | S |
| `boolEmpty_not_w` | 474 | `¬ W boolEmpty` | VERIFIED_FINITE | n/a | A |
| `boolEmpty_not_a` | 476 | `¬ A boolEmpty` | VERIFIED_FINITE | n/a | A |
| `boolEmpty_not_c` | 478 | `¬ C boolEmpty` | VERIFIED_FINITE | n/a | A |
| `boolEmpty_d` | 480 | `D boolEmpty` | VERIFIED_FINITE | n/a | A |
| `boolEmpty_e` | 483 | `E boolEmpty` (empty family) | VERIFIED_FINITE | n/a (probe: none) | A |
| `boolEmptyMerged_d` | 487 | `D boolEmptyMerged` | VERIFIED_FINITE | n/a | A |
| `boolEmptyMerged_not_e` | 490 | `¬ E boolEmptyMerged` | VERIFIED_FINITE | n/a | A |
| `nimp_w_a` … `nimp_w_f` (8) | 500–526 | `∃S` W∧¬Q for Q ∈ {A,Bs,Bc,Bl,C,D,E,F}, witness `unitBare` | REFUTED (W→Q) | none | `nimp_w_d` S; rest A |
| `imp_a_w` | 530 | `∀S` A→W | FROZEN | none | A |
| `nimp_a_bs` | 534 | `∃S` A∧¬Bs, witness `d2Bare` | REFUTED | none | S |
| `nimp_a_bc` | 541 | `∃S` A∧¬Bc, witness `tri` | REFUTED | propext | S |
| `nimp_a_c` | 548 | `∃S` A∧¬C, `d2Bare` | REFUTED | none | A |
| `imp_a_d` | 553 | `∀S` A→D | FROZEN | none | S |
| `nimp_a_e` | 559 | `∃S` A∧¬E, `d2Merged` | REFUTED | none | S |
| `nimp_a_f` | 562 | `∃S` A∧¬F, `d2Bare` | REFUTED | none | A |
| `imp_bs_w`, `imp_bs_a`, `imp_bs_d` | 567–584 | `∀S` Bs→W/A/D | FROZEN | none | A |
| `nimp_bs_bc` | 574 | `∃S` Bs∧¬Bc, `triSym` | REFUTED | propext | S |
| `nimp_bs_c`, `nimp_bs_e`, `nimp_bs_f` | 581–590 | `∃S` with `s2Bare`/`s2Merged` | REFUTED | none | A |
| `imp_bc_w`, `imp_bc_a`, `imp_bc_d` | 595–611 | `∀S` Bc→W/A/D | FROZEN | none | A |
| `nimp_bc_bs` | 601 | `∃S` Bc∧¬Bs, `d2Bare` | REFUTED | none | S |
| `nimp_bc_c`, `nimp_bc_e`, `nimp_bc_f` | 608–617 | `∃S`, `d2Bare`/`d2Merged` | REFUTED | none | A |
| `imp_bl_w`, `imp_bl_a`, `imp_bl_d` | 625–641 | `∀S` Bl→W/A/D | FROZEN | none | A |
| `nimp_bl_bs`, `nimp_bl_bc`, `nimp_bl_c`, `nimp_bl_e`, `nimp_bl_f` | 630–647 | `∃S`, `d2Bare`/`tri`/`d2Merged` | REFUTED | none (bc: propext) | A |
| `imp_c_w` | 656 | `∀S` C→W | FROZEN | none | A |
| `nimp_c_a`, `nimp_c_d` | 660, 676 | `∃S` C∧¬A, C∧¬D, `unitFull` | REFUTED | none | S |
| `nimp_c_bs`, `nimp_c_bc`, `nimp_c_bl`, `nimp_c_e`, `nimp_c_f` | 663–683 | `∃S`, `unitFull` | REFUTED | none | A |
| `nimp_d_w` … `nimp_d_f` (8) | 692–718 | `∃S` D∧¬Q, `boolEmpty` (`boolEmptyMerged` for E) | REFUTED | none | `nimp_d_e` S; rest A |
| `nimp_e_w`, `nimp_e_a`, `nimp_e_bs`, `nimp_e_bc`, `nimp_e_bl`, `nimp_e_c`, `nimp_e_f` | 726–751 | `∃S` E∧¬Q, `boolEmpty` | REFUTED | none | A |
| `imp_e_d` | 748 | `∀S` E→D | FROZEN | none | S |
| `imp_f_w`, `imp_f_a`, `imp_f_c`, `imp_f_d` | 756–776 | `∀S` F→W/A/C/D | FROZEN | none | A |
| `nimp_f_bs` | 761 | `∃S` F∧¬Bs, `d2Protected` | REFUTED | none | A |
| `nimp_f_bc` | 766 | `∃S` F∧¬Bc, `triProtected` | REFUTED | propext | A |
| `nimp_f_e` | 781 | `∃S` F∧¬E, `d2ProtectedMerged` | REFUTED | none | S |
| `e_empty_iff_d` | 792 | if `S.Ops = (fun _ => False)` then `E S ↔ D S` | CONDITIONAL:`S.Ops` empty | none | S |
| `prot_not_from_witness` | 804 | `∃ S, A S ∧ ¬ S.prot S.a S.b` (`d2Bare`) | REFUTED (A → prot) | none | S |
| `ret_not_from_witness` | 809 | `∃ S, A S ∧ ¬ S.ret S.a S.b` | REFUTED (A → ret) | none | S |
| `f_ops_irrelevant` | 818 | `F {S with Ops := O'} ↔ F S`, proof `Iff.rfl` | FROZEN (definitional) | none | A |
| `bool_class` | 827 | a decidable `r` on `Bool` with the A-laws at endpoints false,true is `D2` or `S2` | CONDITIONAL:`[∀ x y, Decidable (r x y)]` | propext, Quot.sound | S |
| `matrixCells_length` | 916 | `matrixCells.length = 72` by `rfl` | VERIFIED_FINITE | none | A |

## 4. External and admitted assumptions

- Structures: `Setting` is the whole admitted signature. `X : Type` (universe 0), `Ops : (X → X) → Prop`: both metatheoretic. No observation field — stated in the header and used by `f_ops_irrelevant`'s docstring.
- Recurring hypotheses: pointwise decidability instances in `located_of_decidable` and `bool_class`; `Irrefl` in `cotrans_auto_on_two`; `S.Ops = empty` in `e_empty_iff_d`.
- Declared policies: the four `open_cell_*_bl` strings and `matrixCells` are declared labels, not propositions. Nothing in Lean checks that the label in row (P,Q) matches the existence of `imp_P_Q`/`nimp_P_Q`; that cross-check is in Python (`code/derivation/primitive_core.py::lean_tag`, `tests/test_primitive_core.py::test_every_matrix_cell_status`).
- Library lemmas doing real work: `PrimDiff.irrefl_witness_ne`, `factors_through_point_iff`, `irred_empty_iff_ne`, `merger_erases`, `bool_irrefl_witness_classification` (which itself uses `by_cases` on a decidable instance), `Clos.id`. `decide` on `Bool`/`Fin 3` equalities.
- Unearned identity: none found. Unrestricted external universe: `Setting.X : Type` is an external universe, used only as the metatheoretic container of models; no theorem claims the system "has" a type. Unbounded function treated as internally available: `Located` is `∃ f : X → X → Bool`; the module itself says this is admitted data and that its underivability is metatheoretic — correctly scoped, but see finitude flags in §11. Silently assumed observer: none found (the signature has none by design). Unspecified correspondence between presentations: none found. Cost function: none. Admitted condition later described as forced: none found in this module (irreflexivity is argued for by `imp_a_d` vs `nimp_w_d`, not declared forced). Finite computation presented as universal: the "minimum carrier" claims — see §11.

## 5. Derived consequences

- `Setting`, `A`, `C`, `E`, `F`, `W`, `D`, `Cotrans`, `Located`, `located_of_decidable`, `imp_a_d`, `cotrans_auto_on_two`, `e_empty_iff_d`, `triR`, `prot_not_from_witness`, `ret_not_from_witness`, `nimp_w_d` are used by `PrimitivePassage`, `PrimitiveContact`, `ContactBridge`, `ContactKernel`, `Apartness`, `Compression`, `InterpreterBoundary` (grep counts: `Setting` 10, `A` 10, `located_of_decidable` 5, `imp_a_d` 4, `cotrans_auto_on_two` 4).
- `PrimitiveContact` re-exports essentially the whole `nimp_*` family (one mention each) as its pre-contact interface.
- `ContactKernel.toSetting_A`, `kernel_to_w/d/e_empty`, `kernel_located_of_decidable` lift the kernel into this signature's candidates.
- Paper: `CL-PD2-MATRIX` (ledger line ~1450), `paper/primitive_difference_contact.md` "formal spine", `paper/primitive_difference_map.md` lines 29–65.

## 6. Counterexamples and limitations

- 51 cells are countermodels; witnesses by model: `unitBare` (W row), `unitFull` (C row), `boolEmpty` (D, E rows), `boolEmptyMerged` (D→E), `d2Bare` (A/Bc/Bl → Bs/C/F; Bc→Bs), `d2Merged` (A/Bc/Bl → E), `d2Protected` (F→Bs), `d2ProtectedMerged` (F→E), `s2Bare`/`s2Merged` (Bs row), `tri` (A/Bl → Bc), `triSym` (Bs→Bc), `triProtected` (F→Bc). `prot_not_from_witness`/`ret_not_from_witness` refute "witness ⇒ store entry".
- Not proved: that the four Bl cells are underivable (OPEN by declaration; the module proves only that no decidable countermodel can exist). Not proved: that the countermodels have minimum carrier over all types of that cardinality — `cotrans_auto_on_two` is stated for `Bool` only and `no_witness_on_subsingleton` for subsingletons; no transport along bijections is formalized. Not proved in Lean: the correspondence between `matrixCells` rows and theorem names.
- The four `nimp_*_bl` cells with sources W, C, D, E fail Bl through the A-conjunct (the docstrings say so); nothing in the module separates any reading from `Located` itself.

## 7. Axiom dependencies

All 81 artifact reports ⊆ {propext, Quot.sound}. Probed model facts (`tri_not_bc`, `triSym_not_bc`: propext; `d2_not_symm`, `boolEmpty_e`: none) likewise. None exceed the budget.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 81 of 129 theorems are in the axiom artifact; the 48 model facts are not (they are internal to the countermodel theorems). Paper cites `matrixCells`, the 68 matrix theorems, `cotrans_auto_on_two`, `located_of_decidable`, `D_iff_ne`, `e_empty_iff_d` (ledger `CL-PD2-MATRIX`), and `imp_a_d`/`nimp_w_d` in `CL-PD2-INITIALITY`. Probe run: `lake env lean probes/D/core_probe.lean` — `#print axioms` on four model facts (results in §3); a check that `f_ops_irrelevant` is `Iff.rfl` compiled.

## 9. Related Python implementations

`code/derivation/primitive_core.py` (`Setting`, `enumerate_settings`, `irreflexive`, `symmetric`, `cotransitive`, `closure`, `evaluate`, `scan_settings`, `matrix_report`, `lean_tag`, `two_element_classification`), `code/run_primitive_core.py`; tests `tests/test_primitive_core.py` (`test_every_matrix_cell_status`, `test_a_bc_minimal_countermodel_is_carrier_three`, `test_witness_minimality_spot_checks`, `test_two_element_classification`). Artifacts `primitive_candidates.json`, `primitive_implication_matrix.json`.

## 10. Textbook placement proposal

- Prerequisites: relations on a type, irreflexivity/symmetry, `PrimDiff.Irred`/`Clos` (closure of an operation family), the two-point realizations `D2`/`S2`, the distinction between a metatheoretic inequality `a ≠ b` and an asserted relation `r a b`.
- Substantive: `Setting` and the nine predicates; `D_iff_ne`; `imp_a_d` with `nimp_w_d`; `nimp_c_a`/`nimp_c_d` (demand does not create difference); `imp_e_d`, `nimp_d_e`, `nimp_a_e`, `e_empty_iff_d` (family-relativity of irreducibility); `nimp_a_bc` with `cotrans_auto_on_two` and `tri_not_bc` (cotransitivity first bites at three points); `prot_not_from_witness`/`ret_not_from_witness`; `located_of_decidable` and the OPEN scope; `bool_class`.
- Auxiliary: all model facts, the `not_*_of_not_a` helpers, the remaining 40-odd routine cells, `f_ops_irrelevant`, `matrixCells(_length)`.
- Lesson title: "Nine readings of one difference". Question answered: which of the nine readings forces the two endpoints apart, and what each extra law or store costs.
- Omit: the `open_cell_*` strings (teach the OPEN scope in prose instead); the per-row routine cells can be summarised as a matrix figure rather than taught one by one.

## 11. Interpretation findings

1. **Minimum-carrier claims (INTERPRETATION DEFECT, minor).** Paper (`primitive_difference_contact.md`): "A → Bc fails at carrier 3, provably minimally … so no smaller countermodel exists"; ledger `CL-PD2-MATRIX`: "minimum carrier proved where cited". Lean: `cotrans_auto_on_two (r : Bool → Bool → Prop) (hi : Irrefl r) : Cotrans r` and `PrimDiff.no_witness_on_subsingleton`. These cover the carrier `Bool` and all subsingleton carriers; "carrier size" over an arbitrary `Type` and transport to other two-element types are not formalized. Missing lemma: `Cotrans` is invariant under bijection of carriers. The docstring at line 113–120 is correctly scoped to "the carrier `Bool`"; the prose generalizes.
2. **`matrixCells` as evidence (INTERPRETATION DEFECT, minor).** The header says the table is exported "for mechanical cross-checking against the theorem names in this file". Lean proves only `matrixCells.length = 72` (`rfl`). The row↔theorem correspondence is checked only in Python; `matrixCells` is a declared label table.
3. **Finitude flags.** `Located r := ∃ f : X → X → Bool, …` is a metatheoretic existential over a function space; the four OPEN cells are statements about constructive derivability in the ambient type theory, not about anything the system possesses. `Setting.X : Type` and `Ops : (X → X) → Prop` are metatheoretic containers of models. The module's own prose respects this ("underivability … is metatheoretic"); the paper's phrase "Located (boolean realizability)" should be read the same way.
4. **`f_ops_irrelevant` is definitional** (`Iff.rfl`): not vacuous, but its content is that `F` does not mention `Ops`; its docstring's further sentence ("not yet an obstruction, because obstruction requires an observation or collapse event") is commentary, not something this theorem establishes.
5. Vacuity check: all `∃S` countermodels have concrete witnesses; all `∀S` implications have satisfiable hypotheses (e.g. `d2Bare` satisfies A, Bc, Bl; `s2Bare` satisfies Bs; `d2Protected` satisfies F; `boolEmpty` satisfies D and E; `unitFull` satisfies C). None found vacuous.
