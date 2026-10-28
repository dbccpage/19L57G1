# Audit: PrimitiveCats

| field | value |
|---|---|
| Path | lean4/Derivation/PrimitiveCats.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | a6ec08d67334d890 |
| Lines | 721 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.PrimDiff |
| Declarations | 6 structures (`PtdRel`, `Hom`, `Pres`, `PHom`, `Pres2`, `PHom2`), 26 defs, 49 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 49 lines (every theorem); axioms seen: none / propext / Quot.sound / propext+Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module asks what the morphism level says about the two two-point realizations of a witnessed difference. Objects are pointed witnessed relations (a carrier, a relation, two designated points, one asserted edge between them); morphisms are carrier maps preserving the points and the relation. It proves the category laws, then that the oriented two-point object `d2Obj` is initial among all such objects (no irreflexivity needed, so this is the universal property of the bare witness W), that the symmetric object `s2Obj` is initial only once every target is symmetric and has no morphism at all to `d2Obj`, that initiality is unique up to isomorphism and provably not up to presentation identity (`d2SwapObj` is a second, non-identical initial object), and that initiality is not minimum carrier size (objects with a free third point exist at every size and have two maps to `d2Obj`). It then models the observer as a *faithful presentation* of a source (a map out of the carrier keeping the witnessed pair apart) and proves the branching result: with three occurrences there is no presentation that receives a map from every presentation (the two maximal collapses are incomparable), and with two occurrences unrestricted terminality still fails because of a free point, the surviving positive fragment being uniqueness against surjective presentations. Orientation is shown to live in the pointing: the swap is an unpointed automorphism of `S2` only, and both pointed objects are rigid.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `PtdRel` | 36 | structure | `X : Type`, `r`, `a b : X`, `w : r a b` | ADMITTED (the object notion) |
| `Hom` | 45 | structure | `f : P.X → Q.X` with `f a = a'`, `f b = b'`, `r x y → r' (f x) (f y)` | ADMITTED (morphism notion) |
| `idH` | 65 | def | identity morphism | ADMITTED |
| `comp` | 69 | def | composition `g ∘ h` | ADMITTED |
| `IrreflObj` | 87 | def | `PrimDiff.Irrefl P.r` | ADMITTED |
| `SymObj` | 91 | def | `P.r` symmetric | ADMITTED |
| `d2Obj` | 97 | def | `Bool`, `D2`, false, true | ADMITTED (concrete object) |
| `s2Obj` | 102 | def | `Bool`, `S2`, false, true | ADMITTED |
| `d2SwapObj` | 109 | def | `Bool`, relation `x = true ∧ y = false`, true, false | ADMITTED |
| `Initial` | 132 | def | `∀ T, ∃ h : Hom R T, ∀ h', h' = h` | ADMITTED (standard notion, defined natively) |
| `WeaklyInitial` | 136 | def | `∀ T, Nonempty (Hom R T)` | ADMITTED |
| `wideObj` | 302 | def | `Fin (n+2)` with the single edge 0→1 | ADMITTED |
| `bigObj` | 320 | def | `Fin (n+3)` with the single edge 0→1 | ADMITTED |
| `bigHomA` | 327 | def | `bigObj n → d2Obj`, `x ↦ (x.val == 1)` | ADMITTED |
| `bigHomB` | 335 | def | `bigObj n → d2Obj`, `x ↦ !(x.val == 0)` | ADMITTED |
| `BoolBijective` | 373 | def | injective and surjective endofunction on `Bool` | ADMITTED |
| `IsRelAuto` | 378 | def | bijective and preserves/reflects `r` | ADMITTED |
| `bigObj3` | 439 | def | `Fin 3`, edge 0→1, points 0,1 | ADMITTED |
| `Pres` | 446 | structure | `Q : Type`, `q : Fin 3 → Q`, `q 0 ≠ q 1` | ADMITTED (the "faithful presentation" = observer-cut notion) |
| `PHom` | 453 | structure | `h : P.Q → R.Q` commuting with the presentations | ADMITTED |
| `pid`, `pcomp` | 467, 470 | def | identity / composition of `PHom` | ADMITTED |
| `idPres3` | 485 | def | the identity presentation on `Fin 3` | ADMITTED |
| `mergeA` | 502 | def | `Fin 3 → Bool`, `x ↦ decide (x = 1)` (merges 0,2) | ADMITTED |
| `mergeB` | 506 | def | `x ↦ decide (x = 0)` (merges 1,2) | ADMITTED |
| `Pres2` | 579 | structure | `Q : Type`, `q : Bool → Q`, `q false ≠ q true` | ADMITTED |
| `PHom2` | 585 | structure | commuting map of two-point presentations | ADMITTED |
| `idPres2` | 600 | def | identity presentation on `Bool` | ADMITTED |
| `swapPres2` | 603 | def | `Bool.not` as presentation | ADMITTED |
| `Epi2` | 608 | def | `∀ z : P.Q, ∃ x, P.q x = z` (surjectivity of `q`) | ADMITTED (named "epi" but defined as surjectivity, not the categorical cancellation property) |
| `freePres2` | 666 | def | `Fin 3`, `q = cond x 1 0` (point 2 free) | ADMITTED |
| `catsFindings` | 709 | def | list of string tags naming the theorems | ADMITTED (declared label list) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `hom_ext` | 54 | two `Hom`s with the same carrier map are equal | FROZEN | none | A |
| `comp_id` | 75 | `comp h (idH P) = h` | FROZEN | none | A |
| `id_comp` | 78 | `comp (idH Q) h = h` | FROZEN | none | A |
| `comp_assoc` | 81 | associativity of `comp` | FROZEN | none | A |
| `d2Obj_irrefl` | 112 | `IrreflObj d2Obj` | VERIFIED_FINITE | none | A |
| `s2Obj_irrefl` | 114 | `IrreflObj s2Obj` | VERIFIED_FINITE | none | A |
| `s2Obj_sym` | 116 | `SymObj s2Obj` | VERIFIED_FINITE | none | A |
| `d2_not_obj_sym` | 124 | `¬ SymObj d2Obj` | VERIFIED_FINITE | none | A |
| `weaklyInitial_of_initial` | 139 | `Initial R → WeaklyInitial R` | FROZEN | none | A |
| `d2_initial` | 156 | `Initial d2Obj`: for every `T : PtdRel` exactly one `Hom d2Obj T` | FROZEN | Quot.sound | S |
| `d2_initial_irrefl` | 174 | for every `P` with `IrreflObj P` (hypothesis unused), exactly one `Hom d2Obj P` | FROZEN (the hypothesis is discarded; it is `d2_initial P`) | Quot.sound | A |
| `d2_map_injective` | 185 | if `IrreflObj P` then every `Hom d2Obj P` is injective on `Bool` | CONDITIONAL:`IrreflObj P` | none | S |
| `d2_map_not_injective_without_irrefl` | 198 | there is a `P` (the one-point self-difference) and a `Hom d2Obj P` collapsing false and true | REFUTED (injectivity without irreflexivity) | none | S |
| `s2_initial_sym` | 209 | if `SymObj T` then exactly one `Hom s2Obj T` | CONDITIONAL:`SymObj T` | Quot.sound | S |
| `s2_no_hom_to_d2` | 234 | `¬ Nonempty (Hom s2Obj d2Obj)` | VERIFIED_FINITE / REFUTED (existence of such a morphism) | none | S |
| `s2_not_weakly_initial` | 245 | `¬ WeaklyInitial s2Obj` | REFUTED | none | S |
| `s2_not_initial` | 248 | `¬ Initial s2Obj` | REFUTED | none | A |
| `d2Swap_initial` | 256 | `Initial d2SwapObj` | FROZEN | Quot.sound | S |
| `two_initials_not_identical` | 275 | `d2Obj ≠ d2SwapObj` (as Lean terms) | VERIFIED_FINITE | none | S |
| `initials_iso` | 286 | any two initial objects have mutually inverse morphisms | FROZEN | none | S |
| `wideObj_irrefl` | 307 | `IrreflObj (wideObj n)` for all `n` | FROZEN (over metatheoretic `n : Nat`) | propext, Quot.sound | A |
| `ptd_on_every_larger_carrier` | 314 | for every `n` an irreflexive object with carrier `Fin (n+2)` exists | FROZEN (over `n : Nat`) | propext, Quot.sound | A |
| `bigHomA_ne_bigHomB` | 341 | the two maps `bigObj n → d2Obj` differ (at point 2) | FROZEN (over `n`) | propext, Quot.sound | A |
| `larger_not_initial` | 353 | `¬ Initial (bigObj n)` for every `n` | REFUTED (initiality of this family) | propext, Quot.sound | S |
| `d2_autos` | 384 | any `f` preserving and reflecting `D2` fixes both points | FROZEN (over `f : Bool → Bool`) | none | A |
| `s2_swap_auto` | 391 | `Bool.not` preserves/reflects `S2` | VERIFIED_FINITE | none | A |
| `s2_id_auto` | 396 | identity preserves/reflects `S2` | VERIFIED_FINITE (Iff.rfl) | none | A |
| `not_bijective` | 400 | `BoolBijective Bool.not` | VERIFIED_FINITE | none | A |
| `s2_swap_isRelAuto` | 410 | `IsRelAuto S2 Bool.not` | VERIFIED_FINITE | none | S |
| `not_not_d2_auto` | 414 | swap does not preserve/reflect `D2` (`decide`) | VERIFIED_FINITE | none | A |
| `d2_swap_not_isRelAuto` | 419 | `¬ IsRelAuto D2 Bool.not` | VERIFIED_FINITE | none | S |
| `pointed_rigid` | 426 | every endomorphism of `d2Obj` and of `s2Obj` fixes both points | FROZEN (immediate from `ha`,`hb`) | none | S |
| `phom_ext` | 457 | `PHom` extensionality | FROZEN | none | A |
| `pcomp_pid`, `pid_pcomp`, `pcomp_assoc` | 474–480 | category laws for `PHom` | FROZEN | none | A |
| `pres_initial` | 490 | `idPres3` has exactly one `PHom` to every `R : Pres` | FROZEN | propext, Quot.sound | A |
| `no_phom_mergeA_mergeB` | 511 | no `PHom mergeA mergeB` | VERIFIED_FINITE / REFUTED | propext | S |
| `no_phom_mergeB_mergeA` | 522 | no `PHom mergeB mergeA` | VERIFIED_FINITE / REFUTED | propext | S |
| `no_terminal_pres` | 548 | no `T : Pres` receives a `PHom` from every `P : Pres` | REFUTED (weak terminality) | propext | S |
| `phom2_ext` | 589 | `PHom2` extensionality | FROZEN | none | A |
| `idPres2_epi` | 610 | `Epi2 idPres2` | VERIFIED_FINITE | none | A |
| `swapPres2_epi` | 612 | `Epi2 swapPres2` | VERIFIED_FINITE | none | A |
| `phom2_unique_of_epi` | 619 | if `Epi2 P` then any two `PHom2 P idPres2` are equal | CONDITIONAL:`Epi2 P` | Quot.sound | S |
| `phom2_exists_from_id` | 627 | a `PHom2 idPres2 idPres2` exists | VERIFIED_FINITE | none | A |
| `phom2_exists_from_swap` | 632 | a `PHom2 swapPres2 idPres2` exists | VERIFIED_FINITE | none | A |
| `phom2_unique_exists_id` | 636 | exactly one `PHom2 idPres2 idPres2` | VERIFIED_FINITE | Quot.sound | A |
| `phom2_unique_exists_swap` | 644 | exactly one `PHom2 swapPres2 idPres2` | VERIFIED_FINITE | Quot.sound | A |
| `no_terminal_pres2` | 677 | no `T : Pres2` has exactly one `PHom2 P T` for every `P` (witness `freePres2`) | REFUTED (terminality in `Pres2`) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Structures: `PtdRel.X : Type`, `Pres.Q : Type`, `Pres2.Q : Type` — universe-0 carriers; the "category" is the metatheoretic class of all such structures (no `Category` typeclass; `Initial`, `WeaklyInitial`, "isomorphic" are written out as Props and proved).
- Recurring hypotheses: `IrreflObj P` (`d2_map_injective`; nominally in `d2_initial_irrefl`, unused), `SymObj T` (`s2_initial_sym`), `Epi2 P` (`phom2_unique_of_epi`).
- Library lemmas doing real work: `funext` (Quot.sound) in uniqueness proofs; `eq_of_heq` in `two_initials_not_identical`; `Bool.not_not`; `omega` in `wideObj`/`bigObj` index bounds; `decide` on `Bool`/`Fin 3`; `PrimDiff.oriented_rigid`, `swap_is_S2_automorphism`, `irrefl_witness_ne`.
- Functions `Nat → X` treated as data: `wideObj`, `bigObj`, `bigHomA/B : Nat → …` are metatheoretic families indexed by `n`; the prose "on every larger carrier" is a metatheoretic ∀ n, not a system totality.
- Unearned identity: none found. Unrestricted external universe: the quantification `∀ T : PtdRel` ranges over all universe-0 carriers; this is what "initial among ALL pointed witnessed relations" means, and nothing larger. Unbounded function treated as internally available: none beyond the `Nat`-indexed families (metatheoretic). Silently assumed observer: the word "observer" is prose for `Pres`/`Pres2` (a map `q` with one inequality); no observer structure is assumed. Unspecified correspondence between presentations: none found — `two_initials_not_identical` is literal structural inequality. Cost function: none. Admitted condition later described as forced: none found. Finite computation presented as universal: the "cut census 1, 2, 4, 8" cited in the ledger is Python/`HigherStructure`, not this module. Categorical vocabulary check: "initial", "weakly initial", "isomorphic", "rigid", "automorphism" are each a *name for a proved property* (`Initial` etc. are defined and the theorems prove them); "free pointed object on one witnessed arrow" (docstring of `d2_initial`, paper) is a gloss on the proved initiality, not an imported assumption; "epi" (`Epi2`) names surjectivity of `q`, not categorical epimorphism — a naming looseness only, since the theorem states its hypothesis explicitly.

## 5. Derived consequences

- `d2_initial` is the most-used export (9 external mentions): `ContactKernel.kernel_gateway_unique`, `passage_gateway_unique`, `PrimitiveContact`, `ContactBridge`. `Hom`, `d2Obj`, `d2_map_injective`, `s2_initial_sym`, `initials_iso`, `no_terminal_pres(2)`, `phom2_unique_of_epi` are re-exported by `PrimitiveContact` and used in `ContactKernel` (`apartObj`, `kernel_no_terminal`).
- Paper: `CL-PD2-INITIALITY`, `CL-PD2-BRANCHING` (ledger ~1470–1515), `primitive_difference_contact.md` §"Categories and the true universal properties" and §"The observer branching theorem", `primitive_difference_map.md` lines 47–55, 225, 249, `primitive_controller_universality.md` line 112.

## 6. Counterexamples and limitations

- Countermodels: `d2_map_not_injective_without_irrefl` (one-point self-difference target); `s2_no_hom_to_d2` ⇒ `s2_not_weakly_initial`, `s2_not_initial`; `two_initials_not_identical` (`d2SwapObj`); `larger_not_initial` via `bigHomA ≠ bigHomB` at the free point 2; `no_phom_mergeA_mergeB`/`B_A` and `no_terminal_pres` (receiver would identify 0 and 1); `no_terminal_pres2` via `freePres2`; `not_not_d2_auto`.
- Not proved: that *every* object whose carrier has a third point is non-initial (only the family `bigObj n`); the general fact follows from `initials_iso` (an initial object's carrier is in bijection with `Bool`) but is not stated. Not proved: existence of a `PHom2 P idPres2` for an arbitrary surjective `P` (so terminality of `idPres2` in the subcategory of `Epi2` presentations is neither proved nor refuted; only the uniqueness half is). Not proved: the cut census for any carrier (lives in `HigherStructure` / Python). "Observer" and "maximal faithful collapse" are prose glosses: `Pres` is any map with `q 0 ≠ q 1`, surjective or not, maximal or not.

## 7. Axiom dependencies

All 49 artifact reports ⊆ {propext, Quot.sound}. None exceed the budget.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 49 theorems are in the axiom artifact. The paper cites `d2_initial`, `d2_initial_irrefl`, `s2_initial_sym`, `s2_not_weakly_initial`, `initials_iso`, `two_initials_not_identical`, `larger_not_initial`, `pointed_rigid`, `no_terminal_pres`, `no_phom_mergeA/B`, `no_terminal_pres2`, `phom2_unique_of_epi`, `d2_map_injective`, `ptd_on_every_larger_carrier`. Probe run: `lake env lean probes/D/cats_probe.lean` — proved `Initial (wideObj 0)` (exit 0, axioms propext, Quot.sound), confirming finding 1 in §11; `#print axioms catsFindings`: none.

## 9. Related Python implementations

`code/derivation/primitive_core.py::presentation_branching` (finite mirror of `no_terminal_pres`: faithful surjective presentations of carrier 3, maximal kernels `{0}|{1,2}` and `{0,2}|{1}` incomparable), `surjections`, `kernel`, `partition_of`; `tests/test_primitive_core.py::test_presentation_branching`; the cut census in `primitive_passage.json` / `test_cut_census` (per ledger). No Python mirror of `d2_initial` or `initials_iso` found.

## 10. Textbook placement proposal

- Prerequisites: `PrimDiff.D2`/`S2`, irreflexivity and symmetry, what a structure-preserving map is, the difference between "equal as presentations" and "isomorphic", and (from PrimitiveCore) candidates W and A.
- Substantive: `PtdRel`/`Hom`, `d2_initial` (with its scope note: it characterizes W, not A), `d2_map_injective` + its countermodel (where irreflexivity is spent on the morphism side), `s2_initial_sym` + `s2_no_hom_to_d2` + `s2_not_weakly_initial`, `initials_iso` + `two_initials_not_identical`, `larger_not_initial`, `pointed_rigid` vs `s2_swap_isRelAuto`, `Pres`/`PHom`, `no_terminal_pres` with `mergeA`/`mergeB`, `no_terminal_pres2` with `phom2_unique_of_epi`.
- Auxiliary: category laws, extensionality lemmas, `d2_initial_irrefl` (restatement), `wideObj`, `bigHomA/B`, `BoolBijective`, `not_bijective`, `s2_id_auto`, `pres_initial`, the concrete `phom2_exists_*`/`phom2_unique_exists_*`, `catsFindings`.
- Lesson title: "The two-point witness is initial — and that is all initiality says". Question answered: which two-point realization every witnessed pointed relation receives a unique map from, and why that neither selects irreflexivity nor picks one presentation.
- Omit: `catsFindings` (label list); `d2Swap_initial` can be taught as "the same proof with roles exchanged" rather than as a separate theorem.

## 11. Interpretation findings

1. **`larger_not_initial` / `ptd_on_every_larger_carrier` (INTERPRETATION DEFECT).** Paper (`primitive_difference_contact.md` §Categories, item 4): "witnessed structures exist on every larger carrier (`ptd_on_every_larger_carrier`) and every one of them admits two distinct morphisms out". Lean: `ptd_on_every_larger_carrier n` produces `wideObj n` on `Fin (n+2)`, and `larger_not_initial n` refutes initiality of the different family `bigObj n` on `Fin (n+3)`. For `n = 0`, `wideObj 0` has carrier `Fin 2` and *is* initial (probe `wideObj0_initial`, this session), so "every one of them" is false as written; the docstring of `larger_not_initial` ("No carrier with a third point is initial") is also stated for the specific family only. The true general statement (an initial object's carrier is in bijection with `Bool`) follows from `initials_iso` but is not formalized. Smallest counterexample: `wideObj 0`.
2. **`d2_initial_irrefl` (minor, not a defect).** The hypothesis `IrreflObj P` is unused (`_`); the theorem is `d2_initial P` renamed. The docstring says so ("stated separately so the subcategory claim is explicit"). Recorded so a reader does not take it as a separate result.
3. **`s2_initial_sym` and "initial in the symmetric subcategory".** Lean proves a per-target statement conditional on `SymObj T`; no subcategory object is formed. Faithful, but the phrase in the paper is a gloss; the theorem is CONDITIONAL on `SymObj T`.
4. **Two-point terminality among surjective presentations (INTERPRETATION gap, not a defect).** Paper: "The positive fragment is exactly uniqueness against surjective presentations (`phom2_unique_of_epi`), where no free point exists." Accurate — but note that existence of a morphism `P → idPres2` for an arbitrary `Epi2 P` is not proved (it needs a retraction of `P.q`), so whether `idPres2` is terminal in the surjective subcategory is neither proved nor refuted. The module's own comment (lines 650–662) says this; the paper's "review-pass closure of the former OPEN cell" closes only the *unrestricted* question.
5. **Finitude flags.** `Initial` quantifies over all `T : PtdRel` with `T.X : Type`; `no_terminal_pres(2)` quantify over all `Pres(2)` with `Q : Type`. These are metatheoretic ∀ over universe 0; the paper's "among ALL pointed witnessed relations" means exactly this and nothing about a totality the system possesses. `wideObj`/`bigObj : Nat → PtdRel` are metatheoretic families.
6. **Vacuity check:** `d2_map_injective`'s hypothesis is satisfied by `d2Obj` itself; `s2_initial_sym`'s by `s2Obj`; `phom2_unique_of_epi`'s by `idPres2`. The `¬ ∃` theorems are refutations with named witnesses. None found vacuous.
