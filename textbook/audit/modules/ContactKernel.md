# Audit: ContactKernel

| field | value |
|---|---|
| Path | lean4/Derivation/ContactKernel.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | ccd296f84f091ef7 |
| Lines | 1025 (inventory says 1026; `wc -l` gives 1025) |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.ContactBridge, Derivation.PrimitiveContact, Derivation.PrimitivePassage |
| Declarations | structure 2 (`WitnessedDiff`, `VHom`), def 21 (two of them `String` OPEN labels, one the 37-row cell literal), abbrev 2, theorem 53 |
| Axiom reports in `artifacts/lean_axioms.txt` | 53 lines (every theorem); 41 "none"; propext: `kernel_zero_not_trans`, `kernel_not_bc`, `kernel_no_terminal`, `kernel_no_terminal_collector`; Quot.sound: `vhom_unique_of_onto`, `kernel_gateway_unique`, `swapObs_boolEqObs`, `no_equivariant_pair_at_fixed_point`, `no_equivariant_pair_valued_map`; both: `passage_gateway_unique`, `kernel_licenses_entry`, `entry_pre_observation` |
| Forbidden tokens (sorry/admit/axiom) | none found (the word "axiom" occurs only in the header prose "axiom report"/"axiom-freedom", not as a declaration) |

## 1. Mathematical purpose

The second collision module asks what the native difference programme and the arriving apartness-style observer can both realize, and builds it: `WitnessedDiff`, a valued difference presentation with two designated endpoints, a diagonal-zero law and a refutation-grade non-zero witness at the designated pair, and nothing else — no symmetry, no transitivity of the zero side, no retention, no protection, no operation family. It shows the kernel is reached from a native candidate-A setting (exactly under pointwise decidability of the asserted relation) and from an observer only together with a chosen non-zero pair, and that for a fixed observer the admissible pairs and the same-data kernels correspond one for one, so the pair is the kernel. It prices what the kernel does not carry: the two observer law fields (symmetry, zero-transitivity) fail at kernels on carriers two and three, cotransitivity fails at three, protection and retention are never derivable, W, A, D and E-at-empty-stores hold outright. It records that value data is finer than the apartness it induces, that valued morphisms are not fixed by their carrier map except under surjectivity of the difference map, that every kernel presents a pointed witnessed relation into which the sealed two-element initial object has exactly one morphism while no terminal collector exists at that presentation grade, and that the kernel's endpoint distinctness sits beside the passage's pre-retention entry facts. A 37-row string literal indexes the collision cells. Everything is metatheory about Lean structures over `Type`; no system state owns a `WitnessedDiff`.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `WitnessedDiff` | 106 | structure | `delta : X → X → R`, `Zero : R → Prop`, endpoints `a b : X`, `diag_zero : ∀ x, Zero (delta x x)`, `apart_ab : ¬ Zero (delta a b)` | ADMITTED (the kernel signature; `diag_zero` and `apart_ab` are proof fields) |
| `kernelApart` | 115 | def | `fun x y => ¬ K.Zero (K.delta x y)` | ADMITTED |
| `boolKernel` | 140 | def | the oriented two-element kernel on `Bool`/`Bool`: `delta x y := !x && y`, zero = `false`, endpoints `false, true` | ADMITTED (finite model) |
| `toSetting` | 153 | def | the native `Setting` a kernel presents: `r := kernelApart K`, endpoints, `ret`/`prot` `False`, `Ops` empty | ADMITTED (declared empty-store policy) |
| `toNativeKernel` | 171 | def | `⟨toSetting K, toSetting_A K⟩ : PrimitiveContact.NativeKernel` (a `Type 1`) | ADMITTED |
| `ofSetting` | 179 | def | from `S` with `h : A S`: `delta := S.r`, `Zero := Not`, endpoints `S.a S.b` (Prop-valued) | ADMITTED |
| `open_kernel_grade` | 204 | def (String) | OPEN label: the round trip without decidability is `¬¬`-coarse | OPEN |
| `ofDiffObs` | 220 | def | from `O` and a chosen pair with `hw : ¬ ZeroRel O a b`: the observer's data with `diag_zero := O.zero_refl`, `apart_ab := hw` | ADMITTED |
| `NonZeroPair` | 305 | abbrev | `{p : X × X // ¬ ZeroRel O p.1 p.2}` | ADMITTED |
| `SameDataKernel` | 310 | abbrev | `{K // K.delta = O.delta ∧ K.Zero = O.Zero}` | ADMITTED |
| `toPair` | 316 | def | a same-data kernel's own endpoints as a non-zero pair | ADMITTED |
| `ofPair` | 324 | def | `ofDiffObs` at the pair, packaged as a same-data kernel | ADMITTED |
| `boolEqObs` | 402 | def | `DiffObs Bool Bool` with `delta := xor`, zero = `false` (zero relation is equality); laws by `decide` | ADMITTED (finite model; laws proved, not spent from an admission) |
| `swapObs` | 450 | def | relabelling action on `DiffObs Bool R`: negate both arguments of `delta` | ADMITTED |
| `toDiffObs` | 518 | def | from `K`, `hs` (zero symmetry) and `ht` (zero transitivity): the `DiffObs` with the same `delta`/`Zero`, `zero_refl := K.diag_zero` | ADMITTED (record identity; the two hypotheses are exactly the two law fields) |
| `open_kernel_bl` | 627 | def (String) | OPEN label: locatedness of `kernelApart` without decidability | OPEN |
| `unitValKernel` | 687 | def | two-element kernel on `Bool`/`Nat` with edge value 1 | ADMITTED (finite model) |
| `twoValKernel` | 697 | def | same, edge value 2 | ADMITTED (finite model) |
| `VHom` | 724 | structure | `f : X → X'`, `g : R → R'`, endpoint preservation, `K'.delta (f x) (f y) = g (K.delta x y)`, zero preservation | ADMITTED (a morphism signature; no identity/composition is defined in this module) |
| `DeltaOnto` | 755 | def | `∀ v, ∃ x y, K.delta x y = v` (surjectivity of the difference map) | ADMITTED |
| `apartObj` | 794 | def | `⟨X, kernelApart K, K.a, K.b, K.apart_ab⟩ : PrimitiveCats.PtdRel` | ADMITTED |
| `boolKernelSwap` | 831 | def | the oppositely pointed two-element kernel | ADMITTED (finite model) |
| `freeKernel` | 848 | def | three-point kernel on `Fin 3`/`Bool`, one oriented edge `0 → 1`, free third point | ADMITTED (finite model) |
| `passageObj` | 904 | def | `PtdRel` with carrier `Nat`, `r i j := (i, j) ∈ preRetained.asserted`, pointed at `0, 1`, witness by `decide` | ADMITTED (carrier `Nat`: metatheory) |
| `contactCells` | 960 | def | 37 triples `(id, status, evidence string)` | ADMITTED (literal) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `kernelApart_irrefl` | 120 | `∀ x, ¬ kernelApart K x x` (contrapositive of `diag_zero`) | FROZEN | none | S |
| `kernel_endpoints_ne` | 126 | `K.a ≠ K.b` (from `apart_ab` against `diag_zero`) | FROZEN | none | S |
| `no_kernel_on_subsingleton` | 133 | `[Subsingleton X] (K : WitnessedDiff X R) : False` | REFUTED (no kernel on a one-point carrier) / CONDITIONAL:`Subsingleton X` | none | S |
| `toSetting_A` | 164 | every kernel's setting satisfies candidate A | FROZEN | none | S |
| `ofSetting_exact` | 192 | under `[∀ x y, Decidable (S.r x y)]`, `kernelApart (ofSetting S h) x y ↔ S.r x y` | CONDITIONAL:`A S`, `Decidable (S.r x y)` pointwise | none | S |
| `ofSetting_ret_irrelevant` | 210 | replacing `ret`, `prot`, `Ops` of `S` gives the same kernel, by `rfl` | FROZEN (definitional) | none | A |
| `pair_choice_load_bearing` | 240 | `∃ O : DiffObs Bool Bool, ∃ a₁ b₁ a₂ b₂, ¬ ZeroRel O a₁ b₁ ∧ ZeroRel O a₂ b₂` | VERIFIED_FINITE (weak existence; docstring disclaims anything stronger) | none | A |
| `kernel_from_obs_iff_pair` | 261 | `(∃ K, K.delta = O.delta ∧ K.Zero = O.Zero) ↔ ∃ a b, ¬ ZeroRel O a b` | FROZEN | none | S |
| `eq_ofDiffObs_of_fields` | 276 | a same-data kernel equals `ofDiffObs O K.a K.b _` (cases on the field equalities) | FROZEN | none | A |
| `obs_eq_of_fields` | 295 | two observers with equal `delta` and `Zero` are equal (proof irrelevance of the law fields) | FROZEN | none | A |
| `toPair_ofPair` | 328 | `toPair O (ofPair O p) = p` | FROZEN | none | A |
| `ofPair_toPair` | 337 | `ofPair O (toPair O K) = K` | FROZEN | none | A |
| `ofPair_injective` | 348 | `ofPair O p = ofPair O q → p = q` | FROZEN | none | S |
| `transpose_kernel_ne` | 368 | `ofDiffObs O a b hw ≠ ofDiffObs O b a _` (the transposed pair is admissible by the ADMITTED `zero_symm`; the kernels differ in `a`) | FROZEN (presentation grade; uses `zero_symm`, `zero_refl`) | none | S |
| `kernel_not_unique_of_pair` | 390 | if `∃ a b, ¬ ZeroRel O a b` then two distinct same-data kernels exist | CONDITIONAL:`∃ a b, ¬ ZeroRel O a b` | none | S |
| `boolEqObs_nonzero_ft` | 416 | `¬ ZeroRel boolEqObs false true` | VERIFIED_FINITE | none | A |
| `boolEqObs_nonzero_tf` | 420 | `¬ ZeroRel boolEqObs true false` | VERIFIED_FINITE | none | A |
| `two_kernels_from_one_observer` | 427 | the two `ofDiffObs boolEqObs` kernels at `(false,true)` and `(true,false)` differ | VERIFIED_FINITE | none | A |
| `pair_choice_not_unique` | 438 | `∃ O K₁ K₂` over `Bool`/`Bool`, same data, `K₁ ≠ K₂` | VERIFIED_FINITE (hypothesis-free non-uniqueness witness) | none | S |
| `swapObs_boolEqObs` | 462 | `swapObs boolEqObs = boolEqObs` (`funext` + `decide`) | VERIFIED_FINITE | Quot.sound | A |
| `no_equivariant_pair_at_fixed_point` | 475 | any `sel : DiffObs Bool Bool → Bool × Bool` with the negation law at `boolEqObs` yields `False` | FROZEN (over all such total maps; metatheoretic function space) | Quot.sound | S |
| `no_equivariant_pair_valued_map` | 497 | `¬ ∃ sel, ∀ O, sel (swapObs O) = (!(sel O).1, !(sel O).2)` | REFUTED (no relabelling-equivariant total pair selector on `DiffObs Bool Bool`) | Quot.sound | S |
| `kernel_no_witness_from_collapse` | 507 | `∀ a b : Bool, ¬ obsApart collapseAllObs a b` (`h trivial`: the zero predicate is `True`) | FROZEN (definitional) | none | A |
| `toDiffObs_fields` | 532 | `delta`, `Zero` carried unchanged and `ofDiffObs (toDiffObs K hs ht) K.a K.b K.apart_ab = K`, all `rfl` | FROZEN (definitional record identity) | none | S |
| `toDiffObs_apart` | 543 | `obsApart (toDiffObs K hs ht) x y ↔ kernelApart K x y` (`Iff.rfl`) | FROZEN (definitional) | none | A |
| `kernel_not_observer` | 558 | `∃ K : WitnessedDiff Bool Prop, ¬ ∃ O : DiffObs Bool Prop, O.delta = K.delta ∧ O.Zero = K.Zero` (witness: `D2` read as a kernel; `zero_symm` would force `D2 true false`) | REFUTED (carrier 2, Prop-valued) | none | S |
| `kernel_zero_not_trans` | 578 | `∃ K : WitnessedDiff (Fin 3) Prop, K.Zero (K.delta 0 2) ∧ K.Zero (K.delta 2 1) ∧ ¬ K.Zero (K.delta 0 1)` (witness: complement of `triSymRel`, via sealed `symm_without_cotrans_breaks_trans`) | REFUTED (the kernel signature does not entail zero-transitivity; carrier 3) | propext | S |
| `kernel_not_bs` | 589 | `∃ K : WitnessedDiff Bool Prop, ¬ ∀ x y, kernelApart K x y → kernelApart K y x` (witness: `D2` as kernel) | REFUTED (the kernel signature does not entail symmetry of the induced apartness; carrier 2) | none | S |
| `kernel_not_bc` | 603 | `∃ K : WitnessedDiff (Fin 3) Prop, ¬ Cotrans (kernelApart K)` (same `triSymRel` witness) | REFUTED (carrier 3) | propext | S |
| `kernel_located_of_decidable` | 618 | under `[∀ v, Decidable (K.Zero v)]`, `Located (kernelApart K)` (sealed `located_of_decidable`) | CONDITIONAL:`Decidable (K.Zero v)` | none | S |
| `kernel_not_c` | 632 | `¬ C (toSetting K)` (`prot` is `False` by construction) | FROZEN (definitional policy read-back) | none | A |
| `kernel_not_f` | 638 | `¬ F (toSetting K)` (`ret` is `False` by construction) | FROZEN (definitional) | none | A |
| `kernel_to_w` | 643 | `W (toSetting K)` from `apart_ab` | FROZEN | none | A |
| `kernel_to_d` | 648 | `D (toSetting K)` via sealed `imp_a_d` | FROZEN | none | A |
| `kernel_to_e_empty` | 654 | `E (toSetting K)` via sealed `e_empty_iff_d` with `Ops` empty by construction | FROZEN (rests on the empty-`Ops` policy) | none | A |
| `kernel_not_e_merged` | 661 | `∃ K : WitnessedDiff Bool Bool, E (toSetting K) ∧ ¬ E {toSetting K with Ops := (· = fun _ => false)}` (`boolKernel`; sealed `merger_erases`) | VERIFIED_FINITE / REFUTED (E is not kernel content once a merger is declared) | none | S |
| `no_kernel_over_allzero` | 675 | `¬ ∃ K : WitnessedDiff Bool Bool, K.delta = collapseAllObs.delta ∧ K.Zero = collapseAllObs.Zero` (the zero predicate is `True`) | REFUTED (carrier 2) | none | A |
| `value_presentation_fork` | 709 | `unitValKernel` and `twoValKernel` have the same `kernelApart` and different `delta` | VERIFIED_FINITE | none | S |
| `vhom_not_unique` | 737 | two `VHom unitValKernel boolKernel` with equal `f` and `h₁ ≠ h₂` (differ at `g 2`, off the image of `delta`) | VERIFIED_FINITE | none | S |
| `vhom_unique_of_onto` | 763 | `DeltaOnto K → h₁.f = h₂.f → h₁ = h₂` for `h₁ h₂ : VHom K K'` (`funext` on `g`) | CONDITIONAL:`DeltaOnto K` (sufficiency only) | Quot.sound | S |
| `boolKernel_apart_iff` | 787 | `kernelApart boolKernel x y ↔ PrimDiff.D2 x y` | VERIFIED_FINITE | none | A |
| `apartObj_irrefl` | 798 | `IrreflObj (apartObj K)` | FROZEN | none | A |
| `apartObj_sym_of_observer` | 806 | `SymObj (apartObj (ofDiffObs O a b hw))` (contraposed `zero_symm`) | FROZEN (uses the ADMITTED `zero_symm` field) | none | A |
| `kernel_gateway_unique` | 815 | `∃ h : Hom d2Obj (apartObj K), ∀ h', h' = h` — literally `d2_initial (apartObj K)` | FROZEN (instantiation of the sealed initiality) | Quot.sound | S |
| `kernel_gateway_injective` | 824 | every `Hom d2Obj (apartObj K)` is injective on `Bool` (sealed `d2_map_injective` with `apartObj_irrefl`) | FROZEN | none | A |
| `kernel_gateways_not_identical` | 843 | `boolKernel ≠ boolKernelSwap` (differ at `a`) | VERIFIED_FINITE | none | A |
| `kernel_no_terminal` | 860 | for every `K'`, two distinct `Hom (apartObj freeKernel) (apartObj K')` (third point to `K'.a` or `K'.b`; distinct by `kernel_endpoints_ne`) | FROZEN (over all `K'`; apartObj grade) | propext | S |
| `kernel_no_terminal_collector` | 890 | `¬ ∃ (X' R' : Type) K', ∀ (X R : Type) K, ∃! h : Hom (apartObj K) (apartObj K')` | REFUTED (no terminal object among `apartObj` presentations, universe 0) | propext | S |
| `passage_gateway_unique` | 911 | `d2_initial passageObj` | FROZEN (instantiation; carrier `Nat`) | propext, Quot.sound | A |
| `kernel_licenses_entry` | 921 | `K.a ≠ K.b ∧ A (inducedSetting preRetained 0 1) ∧ preRetained.wit = []` — the last two conjuncts are the sealed `kernel_enters_preretained`, independent of `K` | FROZEN (conjunction; only the first conjunct mentions `K`) | propext, Quot.sound | S |
| `entry_pre_observation` | 936 | `preRetained.prot = [] ∧ preRetained.obs = none ∧ obstP preRetained 0 1 = false` (two `decide`s and sealed `obst_requires_observation`) | VERIFIED_FINITE (one concrete state) | propext, Quot.sound | A |
| `kernel_two_point_presentation` | 949 | `[DecidableEq X] (K) : ∃ p : X → Nat, p K.a = 0 ∧ p K.b = 1` | CONDITIONAL:`DecidableEq X` (sufficiency only) | none | A |
| `contactCells_length` | 1023 | `contactCells.length = 37` by `rfl` | VERIFIED_FINITE | none | A |

## 4. External and admitted assumptions

- **Structures taken as given**: `DiffObs` (three admitted law fields; `transpose_kernel_ne`, `kernel_not_unique_of_pair`, `apartObj_sym_of_observer`, `ofDiffObs.diag_zero` spend `zero_symm`/`zero_refl`, and the docstrings say so); `PrimitiveCore.Setting` and candidates; `PrimitiveCats.PtdRel`, `Hom`, `Initial` (`∀ T, ∃ h, ∀ h', h' = h`), `d2Obj`, `d2_initial`, `d2_map_injective`, `SymObj`, `IrreflObj`; `PrimitiveContact.NativeKernel : Type 1`; `PrimitivePassage.preRetained`, `inducedSetting`, `obstP`, `kernel_enters_preretained`, `obst_requires_observation`; `ObsDescent.collapseAllObs`; `Apartness.triSymRel`, `triSymRel_irrefl`, `symm_without_cotrans_breaks_trans`; `PrimDiff.D2`, `D2_irrefl`, `D2_witness`, `merger_erases`.
- **Recurring hypotheses**: a chosen non-zero pair `hw : ¬ ZeroRel O a b` (never supplied by the observer: `pair_choice_load_bearing`, `kernel_from_obs_iff_pair`); `[∀ x y, Decidable (S.r x y)]` (`ofSetting_exact`) and `[∀ v, Decidable (K.Zero v)]` (`kernel_located_of_decidable`) — two different decidability admissions, as the ledger stresses; `DeltaOnto K`; `DecidableEq X`; the two law hypotheses `hs`, `ht` of `toDiffObs`.
- **Declared policies**: `toSetting` sets `ret`, `prot` to `False` and `Ops` to empty. `kernel_not_c`, `kernel_not_f`, `kernel_to_e_empty`, `ofSetting_ret_irrelevant` are consequences of that policy.
- **Universe/Type parameters**: `WitnessedDiff : Type → Type → Type` (probe). `kernel_no_terminal_collector` quantifies `∀ (X R : Type)` and `∃ (X' R' : Type)` in universe 0 — a metatheoretic quantification over all Lean types of that universe; the "collector" refuted is any `PtdRel` object presented by a kernel, not a system-internal object. `NativeKernel : Type 1` packages a `Setting` with its own `X : Type`.
- **Functions `Nat → …` or unbounded carriers treated as data**: `passageObj` has carrier `Nat` with `r` = membership in the finite list `preRetained.asserted`; `kernel_two_point_presentation` returns `p : X → Nat`; `no_equivariant_pair_valued_map` quantifies over all total maps `DiffObs Bool Bool → Bool × Bool`. All metatheory (finitude rule); none of these objects is a system state.
- **Library lemmas doing real work**: `funext` (hence Quot.sound) in `swapObs_boolEqObs`, `vhom_unique_of_onto`; `decide` over `Fin 3`/`Bool` and over list membership in `entry_pre_observation`; `simp` on `obstP` through `obst_requires_observation`.
- Unearned identity: none found (`toDiffObs_fields` is `rfl` and is declared a record identity). Unrestricted external universe: the `(X R : Type)` quantifications are universe 0 and the ledger says so for the companion refutations. Unbounded function treated as internally available: `passageObj`'s `Nat` carrier (flagged; the docstring does not claim internal availability). Silently assumed observer: none — the observer is always a parameter or a finite model. Unspecified correspondence between presentations: `kernel_gateways_not_identical`/`transpose_kernel_ne` are explicitly at presentation grade, and "up to isomorphism" is deferred to the sealed `initials_iso` (not re-proved here; not checked by me). Cost function: none. Admitted condition later described as forced: none found in the Lean; see §11 for prose. Finite computation presented as universal: none found — carrier-minimality remarks are marked METATHEORY/INHERITED in the docstrings.

## 5. Derived consequences

Imported by `PrimitiveContact` (which re-exports the collision verdict and cites nearly every theorem by name — all 53 appear once there), `PresentationNaturality` (cites `no_equivariant_pair_valued_map` ×4 and `boolEqObs`; it states it does not derive that theorem), and the root. Ledger entries CL-PD2-CONTACT-KERNEL (the kernel, realizations, gateway, no-collector, value grade), CL-PD2-CONTACT-COUNTERMODELS (`kernel_not_observer`, `kernel_not_bs`, `kernel_zero_not_trans`, `kernel_not_bc`, `kernel_not_c`, `kernel_not_f`, `no_kernel_on_subsingleton`, `no_kernel_over_allzero`, `kernel_not_e_merged`), CL-PD2-CONTACT-ENTRY (`passageObj`, `passage_gateway_unique`, `kernel_licenses_entry`, `entry_pre_observation`, `kernel_two_point_presentation`). `artifacts/completion_dependency_graph.json` names ContactKernel theorems (22 mentions in `primitive_completion_receipt.json`, which also registers `open_kernel_grade`, `open_kernel_bl` as open obligations). The dependency map's scope note cites `kernel_not_bs`, `kernel_zero_not_trans` as the echo of the "irreflexivity fact → irreflexivity law FALSE" row: symmetry and transitivity are admissions on the arriving side too.

## 6. Counterexamples and limitations

- `kernel_not_bs` (carrier 2): the kernel `(D2, Not, false, true)` has `kernelApart = ¬¬D2`, which is not symmetric. It refutes "the kernel signature entails Bs". It says nothing about observers (a `DiffObs` cannot carry `D2`: `kernel_not_observer`, `ContactBridge.d2_not_obs_complement`). Minimum carrier 2 follows from `no_kernel_on_subsingleton` (no carrier-1 kernel at all), though the docstring conservatively labels it METATHEORY.
- `kernel_zero_not_trans` (carrier 3): the kernel `(triSymRel, Not, 0, 1)` has a non-transitive zero side `¬triSymRel`. Refutes "the kernel signature entails zero-transitivity" — i.e. refutes that `WitnessedDiff` is already a `DiffObs` once symmetry is added. Minimality at 3 is INHERITED (on two points any reflexive relation is transitive); not proved here.
- `kernel_not_observer` (carrier 2, Prop-valued): no `DiffObs Bool Prop` shares `D2`'s data.
- `kernel_not_bc` (carrier 3): `¬¬triSymRel` is not cotransitive.
- `no_kernel_over_allzero`, `kernel_no_witness_from_collapse`: the collapsed observer (zero everywhere) yields no kernel; both are immediate from `Zero = True`.
- `kernel_not_e_merged`: E dies under one declared merger with the kernel unchanged (`boolKernel`).
- `value_presentation_fork`, `vhom_not_unique`: value data and off-image value maps are not determined by the apartness.
- `kernel_no_terminal(_collector)`: no terminal object among `apartObj` presentations — at the `PrimitiveCats.Hom` grade, which forgets `R`; terminality in `VHom` is not addressed (ledger and paper say so).
- `no_equivariant_pair_valued_map`: no total pair selector on `DiffObs Bool Bool` commutes with the negation relabelling; the docstring scopes this exactly (non-equivariant selectors exist; no "preferred choice" refutation).
- NOT proved: necessity of `DeltaOnto` for `VHom` uniqueness; necessity of `DecidableEq X` for a two-point presentation; any map from a kernel into a passage state (`kernel_licenses_entry` is a conjunction, see §11); initiality "up to isomorphism" is cited from `PrimitiveCats`, not re-proved; that `VHom` forms a category (no identity/composition in this module; not checked elsewhere); minimal carriers except as noted.

## 7. Axiom dependencies

All 53 theorems within {propext, Quot.sound}: 41 none, 4 propext only, 5 Quot.sound only (each via `funext` or a `Quotient`-free `decide` on functions), 3 both. Axioms exceeding the budget: none. The header's "no quotient object occurs" is a statement about the propositions, not an axiom-freedom claim, and says so.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 53 theorems appear in `artifacts/lean_axioms.txt` with the axioms tabulated above (inventory match). The paper (`paper/primitive_difference_contact.md`, ledger CL-PD2-CONTACT-KERNEL/-COUNTERMODELS/-ENTRY) cites every theorem name; `kernel_not_bs`, `no_equivariant_pair_valued_map`, `ofPair_injective` are cited in the ledger/other modules rather than in the contact paper's prose. Probe `probes/D/kernel_probe.lean` (`lake env lean`): `#check` of `kernel_not_bs`, `kernel_zero_not_trans`, `kernel_not_observer`, `kernel_no_terminal_collector`, `d2_initial`, `kernel_licenses_entry`, `kernel_two_point_presentation` confirmed the statements tabulated; `#print PrimitiveCats.Initial/Hom/d2Obj` confirmed `Initial` is `∀ T, ∃ h, ∀ h', h' = h` and `Hom` is a structure of a function plus three proofs; `WitnessedDiff : Type → Type → Type`; `NativeKernel : Type 1`; `#print axioms` of `kernel_not_bs` none, `kernel_zero_not_trans` propext, `kernel_not_observer` none, `kernel_no_terminal_collector` propext, `entry_pre_observation` propext+Quot.sound, `contactCells_length` none; `#eval contactCells.length` = 37 and the 37 row ids are pairwise distinct (`eraseDups` length 37). Two scratch `example`s of my own in that probe failed (a `decide` on `kernelApart boolKernel` lacking a `Decidable` instance, and a hand-written `¬¬D2 ↔ D2` case split); both failures are in my probe text, not in the library, and nothing above depends on them. Row-by-row correspondence of `contactCells` evidence strings to existing theorem names: spot-checked (`kernel_not_bs`, `obsApart_repr_iff`, `declared_zero_as_view`, `no_terminal`), not exhaustively checked; `tests/test_primitive_contact.py::test_collision_cells_mirror_lean_literal` checks the Python mirror against the literal textually.

## 9. Related Python implementations

`code/run_primitive_contact.py`: `COLLISION_CELLS` (the 37-row mirror, line ~184 carries `K_to_Bs … kernel_not_bs`), `enum_settings_kernels` (E2: candidate-A settings vs. exact kernels at carriers 1–3, counts `[0, 4, 192]` per the ledger), `enum_value_fork` (E5: 81 tables, 2 oriented class presentations), `enum_bool_observers`, `contact_report`; artifact `artifacts/primitive_contact.json:verdict.kernel`; tests `tests/test_primitive_contact.py::test_verdict_block`, `::test_collision_cells_mirror_lean_literal`, `::test_kernel_scope_states_grades_and_record_identity`, `::test_enum_settings_kernels_pinned`, `::test_enum_flagship_and_value_fork_pinned`. `code/derivation/apartness.py` supplies the `triSymRel`-style countermodel census. I did not run these.

## 10. Textbook placement proposal

- Prerequisites: `DiffObs`/`ZeroRel` (DiffInterface); candidates W…F, `Cotrans`, `Located`, `located_of_decidable`, `imp_a_d`, `e_empty_iff_d` (PrimitiveCore); `PtdRel`, `Hom`, `Initial`, `d2_initial`, `d2_map_injective`, `SymObj` (PrimitiveCats); `IsApart`, `triSymRel`, `symm_without_cotrans_breaks_trans` (Apartness); `D2`, `merger_erases` (PrimDiff); `preRetained`, `inducedSetting`, `obstP` (PrimitivePassage); `ContactBridge.obsApart`.
- Substantive: `WitnessedDiff`, `kernelApart`, `kernel_endpoints_ne`, `no_kernel_on_subsingleton`; `ofSetting`/`ofSetting_exact`; `ofDiffObs`, `kernel_from_obs_iff_pair`, the `NonZeroPair ≃ SameDataKernel` round trips and `ofPair_injective`; `transpose_kernel_ne`/`kernel_not_unique_of_pair`; `no_equivariant_pair_valued_map`; `toDiffObs` + `toDiffObs_fields` (as a record identity); the four pricing refutations `kernel_not_observer`, `kernel_not_bs`, `kernel_zero_not_trans`, `kernel_not_bc`; `kernel_located_of_decidable`; `kernel_not_e_merged`; `value_presentation_fork`, `vhom_not_unique`, `vhom_unique_of_onto`; `kernel_gateway_unique`, `kernel_no_terminal_collector`.
- Auxiliary: the `rfl`/`decide` helpers, `kernel_not_c/_not_f`, `kernel_to_*`, `boolKernel_apart_iff`, `apartObj_*`, `kernel_gateway_injective`, `kernel_gateways_not_identical`, `passage_gateway_unique`, `entry_pre_observation`, `kernel_two_point_presentation`, `contactCells_length`.
- Lesson title: "The common kernel: what a witnessed difference carries, and what each side must declare on top." Question: given only a difference map, a zero predicate, two endpoints and one non-zero witness, which of the observer's three laws and the native nine readings come for free, and which are purchased?
- Recommend omitting: `kernel_licenses_entry` and `entry_pre_observation` as theorems (teach the passage entry facts from PrimitivePassage directly; see §11), `open_kernel_*` String labels, `contactCells` literal (present the matrix as a table in the lesson), `pair_choice_load_bearing` (superseded by `pair_choice_not_unique`).

## 11. Interpretation findings

1. **Module header item 6 / `kernel_licenses_entry`** — INTERPRETATION DEFECT (minor; corrected in the ledger, not in the module). Header: "the kernel enters the sealed passage at the pre-retention state — before retention, protection, and observation". Lean: `K.a ≠ K.b ∧ A (inducedSetting preRetained 0 1) ∧ preRetained.wit = []`. Only the first conjunct mentions `K`; the other two are sealed constants about `preRetained` (probe-checked statement), and no map from `K` into a `PState` is constructed. Nothing "enters". The ledger's "Sharper" paragraph says exactly this; the module docstring and header still read as a transport statement.
2. **Categorical vocabulary** — INTERPRETATION DEFECT (mild; scoped correctly in the ledger). "Universal status is inherited" names `d2_initial (apartObj K)`, a proved initiality in `PtdRel` whose morphisms are functions with three proofs: faithful as a name. "Symmetric subcategory" (`apartObj_sym_of_observer`) names the predicate `SymObj`; no subcategory is built. "Epi grade" (`vhom_unique_of_onto`) names `DeltaOnto` = surjectivity of the difference map, not a categorical epimorphism. `VHom` is called a "morphism" but this module defines no identity or composition for it (not checked elsewhere). No categorical assumption is imported; every such word labels a proved predicate or a sealed theorem.
3. **"Every kernel" / "every observer" universality** — checked. `kernel_no_terminal` and `kernel_no_terminal_collector` do quantify over all kernels/all `(X R : Type)` and the Lean matches the docstring; the ledger restricts terminality to the `apartObj` grade, which the Lean also does. `no_equivariant_pair_valued_map` quantifies over all total `sel : DiffObs Bool Bool → Bool × Bool`; its docstring is exact. No docstring claims a universality the Lean lacks. (Finitude flag: these are quantifiers over Lean's `Type`/function spaces, metatheory.)
4. **`kernel_not_bs`, `kernel_zero_not_trans`** — what they refute, checked: existence of a `WitnessedDiff` whose induced apartness is not symmetric / whose zero side is not transitive. Each is a refutation of "the kernel signature entails the observer law", not a statement about any `DiffObs`. The dependency map's "echoed on the other side, where the symmetry and transitivity fields are likewise admissions and not derivable" is a correct reading. The carrier-minimality phrases ("priced at carriers two and three") are labelled METATHEORY / INHERITED in the docstrings; minimality at 2 for `kernel_not_bs` is in fact implied by `no_kernel_on_subsingleton`, minimality at 3 for the zero-transitivity failure is not proved in this module.
5. **`kernel_not_observer`** — scope: refutes `∃ O : DiffObs Bool Prop` sharing the data of a Prop-valued kernel. Because the data equations fix `R = Prop`, this is the natural statement; no overread found. Value-typed kernels over `Bool` with oriented data are covered instead by `ContactBridge.d2_not_obs_complement`.
6. **`toDiffObs` + `toDiffObs_fields`** — the paper calls it "a record identity at DEFINITION grade, not a derivation"; the Lean is three `rfl`s and the two hypotheses are exactly the two law fields. Faithful. The header's phrase "losslessly" is correct for `delta`/`Zero`/the endpoints and is proved.
7. **`contactCells` rows** — as in PrimitiveCore's `matrixCells`: the evidence column is a string, so the row↔theorem correspondence is textual and several rows cite definitions with parenthetical reasoning ("ofSetting (Bs within A)", "ofSetting via imp_f_a") or citations outside this module ("Derivation.quot_barrier (citation)"). Lean checks only the length. Not exhaustively cross-checked here (see §8). INTERPRETATION DEFECT risk only if the matrix is read as kernel-checked; the module says "machine-checkable", which is true of the length and ids, not of the evidence strings.
8. **Policy read-backs**: `kernel_not_c`, `kernel_not_f`, `kernel_to_e_empty`, `kernel_no_witness_from_collapse`, `no_kernel_over_allzero` hold by construction of the empty stores / the `True` zero predicate. The ledger already records "a definitional fact, not a separate non-derivability theorem" for the operation family; the C/F rows ("never derivable") are the same kind of fact — the kernel carries no store, so the predicate that demands one is false. Not a defect; a lesson should present them as definitional.
9. **Finitude flags**: `passageObj` carrier `Nat` (finite asserted list read as a relation on all of `Nat`); `kernel_two_point_presentation` returns a total `X → Nat`; `WitnessedDiff` over arbitrary `Type`; `kernel_no_terminal_collector` over all universe-0 types. All metatheory; the docstrings do not claim the system possesses them.
10. **Vacuity check**: `no_kernel_on_subsingleton` has conclusion `False` by design (a refutation, not a vacuous theorem). `ofSetting_exact`, `kernel_located_of_decidable`, `vhom_unique_of_onto` (e.g. `boolKernel` is `DeltaOnto`), `kernel_two_point_presentation`, `kernel_not_unique_of_pair` (`boolEqObs`) all have satisfiable hypotheses. `toDiffObs_fields`, `toDiffObs_apart`, `ofSetting_ret_irrelevant` have definitionally true conclusions and are declared as such. No vacuous theorem found.
11. PROOF DEFECT: none found.
