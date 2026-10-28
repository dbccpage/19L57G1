# Audit: Apartness

| field | value |
|---|---|
| Path | lean4/Derivation/Apartness.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | e9af3393bbcff170 |
| Lines | 337 |
| Imported by root `Derivation.lean` | yes (line 34) |
| Imports | `Derivation.PrimitiveCore` (and `open PrimDiff PrimitiveCore`) |
| Declarations | 1 structure (`IsApart`), 4 defs (`Indist`, `triSymRel`, `PreservesOriented`, `PreservesApart`), 1 instance (`Decidable (triSymRel x y)`), 28 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 28 lines (every theorem): 22 with no axioms; `triSymRel_irrefl`, `triSymRel_symm`, `symm_without_cotrans_breaks_trans`: propext; `oriented_preserver_unique`, `apart_preserver_pair`, `oriented_family_trivial`: Quot.sound (funext) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

A pre-observational module in the primitive-difference line: it asks what a positively asserted difference relation must carry for its negation — indistinguishability — to behave as sameness. `IsApart r` bundles three separately admitted laws (irreflexive, symmetric, cotransitive); under them `Indist r := ¬ r` is reflexive, symmetric and transitive, each law spent at exactly one clause (`indist_equivalence`). Three finite countermodels show the laws are not redundant: bare assertion breaks reflexivity on one point, irreflexivity alone breaks symmetry on two points (minimal, since on a subsingleton an irreflexive relation is empty), irreflexivity plus symmetry without cotransitivity breaks transitivity on three points (minimal by `PrimitiveCore.cotrans_auto_on_two`). The module then separates the retained orientation from the apartness it generates: the oriented two-point relation and its reverse have the same symmetrisation and the same indistinguishability while differing as data, and the swap fixes the apartness but moves the oriented witness. Finally, on the two-point carrier, the maps preserving the oriented witness are exactly the identity, those preserving the symmetric apartness exactly identity and swap, constants preserve neither, and a closure preserves the oriented witness iff every generator does.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `IsApart r` | 55 | structure (Prop) | irreflexive ∧ symmetric ∧ cotransitive (`r x y → ∀ z, r x z ∨ r z y`) | ADMITTED (three declared laws) |
| `Indist r x y` | 63 | def | `¬ r x y` | ADMITTED |
| `triSymRel` | 126 | def | on `Fin 3`: the single symmetrised edge `{(0,1),(1,0)}` | ADMITTED (countermodel datum) |
| `instance Decidable (triSymRel x y)` | 129 | instance | by unfolding | ADMITTED |
| `PreservesOriented f` | 226 | def | `D2 (f false) (f true)` | ADMITTED |
| `PreservesApart f` | 231 | def | `S2 (f false) (f true)` | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `indist_refl` | 67 | `IsApart r → ∀ x, Indist r x x` | CONDITIONAL:`IsApart r` | none | A |
| `indist_symm` | 71 | `IsApart r → Indist r x y → Indist r y x` | CONDITIONAL:`IsApart r` | none | A |
| `indist_trans` | 78 | `IsApart r → Indist r x y → Indist r y z → Indist r x z` (uses only `cotrans`) | CONDITIONAL:`IsApart r` | none | S |
| `indist_equivalence` | 88 | `IsApart r →` the three clauses | CONDITIONAL:`IsApart r` | none | S |
| `bare_breaks_refl` | 101 | `¬ Indist (fun _ _ : Unit => True) () ()` | REFUTED (one-point countermodel) | none | S |
| `irrefl_alone_breaks_symm` | 107 | `Indist D2 true false ∧ ¬ Indist D2 false true` | REFUTED (two-point countermodel) | none | S |
| `subsingleton_indist_total` | 118 | `[Subsingleton X] → Irrefl r → ∀ x y, Indist r x y` | CONDITIONAL:`Subsingleton X`, `Irrefl r` | none | A |
| `triSymRel_irrefl` | 132 | `Irrefl triSymRel` | VERIFIED_FINITE | propext | A |
| `triSymRel_symm` | 136 | `triSymRel` symmetric | VERIFIED_FINITE | propext | A |
| `symm_without_cotrans_breaks_trans` | 143 | `Indist 0 2 ∧ Indist 2 1 ∧ ¬ Indist 0 1` for `triSymRel` | REFUTED (three-point countermodel) | propext | S |
| `two_point_indist_trans` | 158 | on `Bool`, `Irrefl r →` `Indist r` transitive | CONDITIONAL:`Irrefl r`, carrier `Bool` | none | A |
| `s2_isApart` | 170 | `IsApart S2` | FROZEN | none | S |
| `s2_indist_equivalence` | 179 | the three clauses for `S2` | FROZEN | none | A |
| `orientations_same_apartness` | 188 | `∀ x y, Sym D2 x y ↔ Sym D2rev x y` | VERIFIED_FINITE | none | S |
| `orientations_same_indist` | 194 | `∀ x y, Indist (Sym D2) x y ↔ Indist (Sym D2rev) x y` | FROZEN (from the above) | none | A |
| `orientations_differ` | 207 | `¬ (∀ x y, D2 x y ↔ D2rev x y)` | REFUTED | none | S |
| `retained_orientation_not_swap_invariant` | 215 | `D2 false true ∧ ¬ D2 (not false) (not true)` | VERIFIED_FINITE | none | S |
| `oriented_pres_iff` | 236 | `PreservesOriented f ↔ (f false = false ∧ f true = true)` (`Iff.rfl`) | FROZEN | none | A |
| `oriented_preserver_unique` | 242 | `PreservesOriented f → f = id` | FROZEN (funext) | Quot.sound | S |
| `id_preserves_oriented` | 251 | `PreservesOriented id` | FROZEN | none | A |
| `apart_preserver_pair` | 255 | `PreservesApart f → f = id ∨ f = Bool.not` | FROZEN (funext) | Quot.sound | S |
| `id_preserves_apart` | 287 | `PreservesApart id` | FROZEN | none | A |
| `swap_preserves_apart` | 289 | `PreservesApart Bool.not` | FROZEN | none | A |
| `swap_breaks_oriented` | 294 | `¬ PreservesOriented Bool.not` | REFUTED | none | S |
| `collapse_preserves_neither` | 299 | `¬ PreservesOriented (fun _ => v) ∧ ¬ PreservesApart (fun _ => v)` | REFUTED | none | S |
| `oriented_comp` | 305 | `PreservesOriented f → PreservesOriented g → PreservesOriented (f ∘ g)` | FROZEN | none | A |
| `clos_oriented_iff` | 316 | `(∀ f, Clos F f → PreservesOriented f) ↔ (∀ f, F f → PreservesOriented f)` | FROZEN | none | S |
| `oriented_family_trivial` | 332 | `(∀ f, F f → PreservesOriented f) → ∀ f, F f → f = id` | FROZEN | Quot.sound | A |

## 4. External and admitted assumptions

- `X : Type` is a universe parameter in the general theorems (metatheory). The countermodels and the characterisation are on `Unit`, `Bool`, `Fin 3` — declared finite carriers; `Bool` is the two-point carrier of record (`PrimDiff.D2`, `S2`, `D2rev`, `Sym`, `Clos` inherited from `PrimDiff`; `cotrans_auto_on_two` from `PrimitiveCore`).
- `IsApart` is a declared bundle; the header's claim that the three laws are independent cites `PrimitiveCore`'s implication matrix (not re-checked here; batch D).
- "Admitted operations" in the characterisation section means arbitrary `f : Bool → Bool` and arbitrary families `F : (Bool → Bool) → Prop`; nothing restricts `F` to object-language operations (the quantifier is metatheoretic).
- Library lemmas doing work: `funext` (hence `Quot.sound`) in the three `f = id` theorems; `Subsingleton.elim`; `Bool.noConfusion`; `decide` on `Bool`/`Fin 3`; the `Decidable` instance for `triSymRel`.
- Unearned identity: none. Unrestricted external universe: `X : Type` only as a parameter; none found. Unbounded function treated as internally available: none. Silently assumed observer: none (pre-observational by declaration). Unspecified correspondence between presentations: none. Cost function: none ("separately priced" is a phrase; no cost is computed here). Admitted condition later described as forced: none found. Finite computation presented as universal: the "exact characterization" is on the two-point carrier and is stated as such.

## 5. Derived consequences

Consumed by `Attachment.lean`, `ContactKernel.lean`, `ContactBridge.lean` (names not enumerated here; grep hit on `Apartness.`). Ledger owner: `CL-PD2-APARTNESS` (lists 13 of the 28 theorems). Paper: `paper/primitive_difference.md`, `paper/primitive_difference_passage.md`, `paper/primitive_difference_contact.md`, `paper/primitive_difference_map.md`, `paper/native_derivation_map.md` mention apartness (rows not read in detail; not checked beyond the grep).

## 6. Counterexamples and limitations

- Countermodels: `bare_breaks_refl` (constant-true relation on `Unit`), `irrefl_alone_breaks_symm` (`D2`), `symm_without_cotrans_breaks_trans` (`triSymRel`), `orientations_differ`, `swap_breaks_oriented`, `collapse_preserves_neither`. Minimality of the two- and three-point countermodels is proved (`subsingleton_indist_total`, `two_point_indist_trans`).
- Not proved: anything about carriers beyond two points for the preserver characterisation (Python censuses go to carrier 4); that `IsApart` is the *only* bundle making `Indist` an equivalence (the module proves sufficiency and the non-redundancy of each law, not necessity of the bundle as a whole — e.g. an empty relation has `Indist` total without being a positive apartness in any interesting sense, but it is `IsApart` vacuously); "rigid" (`oriented_family_trivial` docstring) means every member is the identity, on two points.

## 7. Axiom dependencies

All 28 within `{propext, Quot.sound}`; 22 use none. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 28 theorems in the artifact; `CL-PD2-APARTNESS` cites 13 by name. No probe run.

## 9. Related Python implementations

`code/derivation/apartness.py`: `all_relations`, `is_irrefl`, `is_symm`, `is_cotrans`, `is_apart`, `indist`, `indist_is_equivalence`, `equivalence_theorem_exhaustive(max_n)` (exhaustive mirror to carrier 3), `insufficiency_countermodels`, `sym_closure`, `orientation_separation`, `all_endofunctions`, `preserves_oriented`, `preserves_apart`, `operation_censuses(max_n)` (to carrier 4); artifact `artifacts/apartness.json`; tests `tests/test_apartness.py`.

## 10. Textbook placement proposal

- Prerequisites: PrimDiff (`Irrefl`, `D2`, `S2`, `Sym`, `Clos`); PrimitiveCore's `cotrans_auto_on_two`; the idea that sameness is to be earned from asserted difference.
- Substantive: `IsApart`, `indist_equivalence` (with the clause-by-clause spending), the three countermodels and their minimality, `orientations_same_apartness` + `orientations_differ` + `retained_orientation_not_swap_invariant`, `oriented_preserver_unique`, `apart_preserver_pair`, `collapse_preserves_neither`, `clos_oriented_iff`. Auxiliary: the rest.
- Lesson title: "Sameness earned from difference, and what orientation adds." Question answered: which laws on a difference relation make 'not different' an equivalence, and what the symmetric quotient forgets.
- Recommend omitting: `s2_indist_equivalence`, `orientations_same_indist`, `id_preserves_*`, `oriented_pres_iff`, `oriented_family_trivial` (immediate corollaries).

## 11. Interpretation findings

1. `oriented_family_trivial` — docstring: "the orientation-preserving operations form no structure beyond the identity — the retained orientation is rigid." Lean: on `Bool`, any `f` with `f false = false ∧ f true = true` is `id`, so any family of such `f` is `{id}`. True, and a one-line corollary; "rigid" is a two-point fact. No defect; scope note.
2. Header item 1: "each a separately priced admission (the implication matrix of `PrimitiveCore` shows none follows from the others)". The independence is proved elsewhere; this module proves the weaker and more specific fact that dropping each law breaks one clause of the equivalence. Consistent. No defect.
3. `CL-PD2-APARTNESS`: "the oriented-witness preservers are exactly the identity, the apartness preservers exactly the identity and the swap". Lean gives both directions (`oriented_preserver_unique` + `id_preserves_oriented`; `apart_preserver_pair` + `id_preserves_apart` + `swap_preserves_apart`). Accurate.
4. Vacuity: `IsApart` is satisfiable (`S2`, and vacuously the empty relation); `Subsingleton X` + `Irrefl r` satisfiable. None found.
