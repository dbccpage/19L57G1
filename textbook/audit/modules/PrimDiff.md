# Audit: PrimDiff

| field | value |
|---|---|
| Path | lean4/Derivation/PrimDiff.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f46c3bc439b7361b |
| Lines | 545 (inventory counts 546 with trailing newline) |
| Imported by root `Derivation.lean` | yes (line 15) |
| Imports | none (self-contained; imports nothing from the regime model) |
| Declarations | 10 def (`Irrefl`, `Sym`, `Transpose`, `D2`, `D2rev`, `S2`, `Push`, `CollapseCollision`, `FidelityObstruction`, `Irred`), 1 inductive (`Clos`), 3 anonymous `Decidable` instances, 44 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 44 lines (every theorem); axioms seen: none / `propext` / `propext, Quot.sound` |
| Forbidden tokens (sorry/admit/axiom) | none found (grep of the file; the word "axiom" occurs only inside prose comments, never at line start) |

## 1. Mathematical purpose

The module asks what the weakest formal object is that deserves the name *primitive difference*, before any regime, context, profile, observer, quotient or repair exists. It compares five candidate readings of "a and b are different": a bare asserted pair `r a b` (A1), the same with witness multiplicities (A2), non-factorization of the selection of `a, b` through a one-point carrier (A3), irreducibility of the pair under an admitted family of endomaps closed under identity and composition (A4), and the two-element carriers `D2` (one oriented edge) and `S2` (its symmetrization) (A5). It proves which readings imply which, exhibiting one-line countermodels for each failure, and isolates irreflexivity as the one axiom among {none, symmetry, irreflexivity} that turns an asserted pair into a metatheoretic inequality. It then separates *collision* (a collapse map identifies the endpoints of an asserted edge, `CollapseCollision`) from *obstruction* (a collision plus a protected law the pushforward violates, `FidelityObstruction P`), shows that collision is orientation-blind, and shows that the oriented and symmetric two-element objects differ exactly by the swap `Bool.not`: an automorphism of `S2`, not of `D2`. The metatheory declared in the header is types, functions, one relation symbol, propositional logic and finite case analysis; the finitude rule below records where that metatheory does work the system itself cannot do.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Irrefl` | 28 | def | `∀ x, ¬ r x x` for a relation `r : α → α → Prop`; the "weakest fidelity commitment" studied | ADMITTED (the one object-level law compared against none and symmetry) |
| `Sym` | 31 | def | symmetrization `r x y ∨ r y x` | ADMITTED |
| `Transpose` | 35 | def | `fun x y => r y x` | ADMITTED |
| `D2` | 89 | def | on `Bool`: `x = false ∧ y = true`, the oriented two-element difference | ADMITTED |
| `D2rev` | 92 | def | `x = true ∧ y = false`, the reverse orientation | ADMITTED |
| `S2` | 95 | def | `Sym D2`, the symmetric two-element difference | ADMITTED |
| (instances) | 97, 100, 103 | instance | `Decidable (D2 x y)`, `(D2rev x y)`, `(S2 x y)` by unfolding | ADMITTED (auxiliary) |
| `Push` | 165 | def | pushforward of `r` along `c : α → β`: `∃ u v, r u v ∧ c u = x ∧ c v = y` | ADMITTED |
| `CollapseCollision` | 174 | def | `∃ u v, r u v ∧ c u = c v`: some asserted edge has both endpoints identified | ADMITTED |
| `FidelityObstruction` | 181 | def | `CollapseCollision r c ∧ ¬ P (Push r c)`: a collision together with a protected law `P` that the pushforward violates | ADMITTED (declared policy: obstruction is *relative to a chosen `P`*) |
| `Clos` | 491 | inductive | closure of a family `F : (α → α) → Prop` under `id` and composition | ADMITTED |
| `Irred` | 498 | def | `∀ f, Clos F f → f a ≠ f b`: no admitted composite identifies the pair | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `irrefl_witness_ne` | 42 | if `Irrefl r` and `r a b` then `a ≠ b` (metatheoretic inequality) | CONDITIONAL:`Irrefl r` | none | S |
| `selfdiff_consistent` | 48 | there is `r : Unit → Unit → Prop` with `r () ()` (witness: the constant-`True` relation on the one-point carrier) | REFUTED (countermodel to A1 → A3, A1 → A1i) | none | S |
| `symm_selfdiff_consistent` | 55 | there is a symmetric `r` on `Unit` with `r () ()` (same witness) | REFUTED (countermodel to "symmetry restores soundness") | none | S |
| `meta_diff_without_assertion` | 63 | there is `r : Bool → Bool → Prop` with `¬ r false true ∧ false ≠ true` (witness: the empty relation) | REFUTED (countermodel to A3 → A1) | none | S |
| `factors_through_point_iff` | 72 | for any `a b : α`: `(∃ p : Unit → α, p () = a ∧ p () = b) ↔ a = b` | FROZEN | none | S |
| `no_witness_on_subsingleton` | 84 | if `α` is a `Subsingleton` and `Irrefl r` then `¬ r a b` for all `a b` | CONDITIONAL:`Irrefl r`, `[Subsingleton α]` | none | S |
| `D2_irrefl` | 106 | `Irrefl D2` | VERIFIED_FINITE (concrete, case split on `Bool`) | none | A |
| `S2_irrefl` | 112 | `Irrefl S2` | VERIFIED_FINITE | none | A |
| `D2_witness` | 118 | `D2 false true` | VERIFIED_FINITE (`decide`) | none | A |
| `D2_initial_pointed` | 123 | for any `r`, `a b` with `r a b`: there is `f : Bool → α` with `f false = a`, `f true = b`, carrying `D2` into `r`, and every `g` with `g false = a`, `g true = b` agrees with `f` pointwise | FROZEN | none | S |
| `one_point_hosts_bare_witness` | 143 | identical statement and proof term to `selfdiff_consistent` | REFUTED (alias) | none | A |
| `witnessed_irrefl_on_every_larger_carrier` | 149 | for every `n : Nat` there is an irreflexive `r` on `Fin (n+2)` with `r 0 1` | FROZEN (∀ n in the metatheory) | propext, Quot.sound | S |
| `push_witness` | 188 | `r a b → Push r c (c a) (c b)` for every `c` | FROZEN | none | A |
| `collision_of_identifying_witness` | 194 | `r a b → c a = c b → CollapseCollision r c` | FROZEN | none | A |
| `collision_not_irrefl` | 199 | `CollapseCollision r c → ¬ Irrefl (Push r c)` | FROZEN | none | A |
| `bare_collapse_admissible` | 209 | `r a b → c a = c b → CollapseCollision r c ∧ Push r c (c a) (c b)` | FROZEN | none | S |
| `collapse_unobstructed_without_fidelity` | 217 | literally `∃ r : Unit → Unit → Prop, r () ()` (the proof term is `selfdiff_consistent`) | REFUTED (alias; see §11) | none | A |
| `obstruction_under_irrefl` | 223 | `r a b → c a = c b → FidelityObstruction Irrefl r c`; **no** hypothesis that `r` itself is irreflexive | FROZEN (conditional only on a witnessed pair and its collision) | none | S |
| `collision_transpose_invariant` | 232 | `CollapseCollision r c ↔ CollapseCollision (Transpose r) c` | FROZEN | none | S |
| `orientation_data_invisible_to_collapse` | 245 | (i) no `f : Bool → Bool` fixing `false` and `true` satisfies `∀ x y, D2 x y ↔ D2rev (f x) (f y)`; (ii) `D2` and `D2rev` collide under the constant map to `Unit` equally (both sides true) | VERIFIED_FINITE | none | S |
| `bool_irrefl_witness_classification` | 265 | for `r` on `Bool` with pointwise `Decidable`, `Irrefl r`, `r false true`: `r = D2 ∨ r = S2` | CONDITIONAL:`[∀ x y, Decidable (r x y)]`, `Irrefl r`, `r false true` | propext, Quot.sound | S |
| `D2_not_pointed_iso_S2` | 288 | no `f` fixing both points satisfies `∀ x y, D2 x y ↔ S2 (f x) (f y)` | VERIFIED_FINITE | none | S |
| `D2_S2_collapse_equiv` | 299 | for every `β` and `c : Bool → β`: `CollapseCollision D2 c ↔ CollapseCollision S2 c` | FROZEN | none | S |
| `symmetric_no_equivariant_classifier` | 315 | every `f : Bool → Bool` with `f (not x) = f x` for all `x` has `f false = f true` (statement mentions neither `S2` nor any relation) | VERIFIED_FINITE | none | S |
| `swap_is_S2_automorphism` | 322 | `∀ x y, S2 x y ↔ S2 (not x) (not y)` | VERIFIED_FINITE (`decide`) | none | A |
| `oriented_rigid` | 328 | if `∀ x y, D2 x y ↔ D2 (f x) (f y)` then `f x = x` for all `x` | VERIFIED_FINITE | none | S |
| `oriented_classifier_exists` | 338 | there is `f` preserving-and-reflecting `D2` with `f false ≠ f true` (witness `id`) | VERIFIED_FINITE | none | S |
| `swap_carries_D2_to_D2rev` | 353 | `∀ x y, D2 x y ↔ D2rev (not x) (not y)` | VERIFIED_FINITE | none | A |
| `swap_twice_restores_D2` | 357 | `D2 (not (not x)) (not (not y)) ↔ D2 x y` | VERIFIED_FINITE | propext | A |
| `swap_twice_restores_D2rev` | 363 | same for `D2rev` | VERIFIED_FINITE | propext | A |
| `sym_D2_eq_S2` | 370 | `S2 = Sym D2` (`rfl`) | VERIFIED_FINITE (definitional) | none | A |
| `sym_D2rev_eq_S2` | 373 | `Sym D2rev = S2` | VERIFIED_FINITE | propext, Quot.sound | A |
| `swap_auto_of_S2_not_of_D2` | 379 | swap is an automorphism of `S2` and not of `D2` | VERIFIED_FINITE | none | S |
| `bool_irrefl_nonempty_classification` | 392 | for decidable irreflexive inhabited `r` on `Bool`: `r = D2 ∨ r = D2rev ∨ r = S2` | CONDITIONAL:`[∀ x y, Decidable (r x y)]`, `Irrefl r`, `∃ x y, r x y` | propext, Quot.sound | S |
| `single_oriented_witness_consistent` | 433 | there is `W : Bool → Bool → Nat` with `W false true = 1 ∧ W true false = 0` | REFUTED (countermodel to "two witnesses are forced") | none | S |
| `multiplicity_invisible_to_presence` | 441 | there are `W1 ≠ W2 : Bool → Bool → Nat` with identical presence `0 < W x y` (witness: constants 1 and 2) | REFUTED (countermodel to "multiplicity adds carrier-pair distinctions") | propext, Quot.sound | S |
| `repetition_no_new_content` | 453 | if `p ∈ L` then `q ∈ L ++ [p] ↔ q ∈ L` for all `q` | FROZEN (list lemma) | propext | A |
| `repetition_new_occurrence` | 472 | `(L ++ [p]).length = L.length + 1` | FROZEN (list lemma) | propext | A |
| `const_presentation_unfaithful` | 481 | given `Irrefl r'` and `v : β`, `¬ r' v v` (the hypothesis instantiated at `v`) | CONDITIONAL:`Irrefl r'` | none | A |
| `id_presentation_faithful` | 485 | `r a b → r (id a) (id b)` | FROZEN (trivial) | none | A |
| `clos_empty_id` | 502 | every `f` in `Clos (fun _ => False)` is pointwise the identity | FROZEN | none | A |
| `irred_empty_iff_ne` | 515 | `Irred (fun _ => False) a b ↔ a ≠ b` | FROZEN | none | S |
| `irred_antitone` | 527 | if `F ⊆ G` then `Irred G a b → Irred F a b` | FROZEN | none | S |
| `merger_erases` | 541 | if `F` contains the constant map `fun _ => v` then `¬ Irred F a b` for all `a b` | CONDITIONAL:`F (fun _ => v)` (a constant map, not merely a merge of the pair) | none | S |

## 4. External and admitted assumptions

- **Structures / universes.** Every generic theorem is parametrised by `{α β : Type}` and a relation `α → α → Prop`; the carrier is an arbitrary external type and the relation an arbitrary external predicate. The header declares this ("types, functions, one binary relation symbol ..."). The paper (S1) itself records that A3 and A4 need "function types, composition, and a one-point carrier", i.e. strictly more metatheory than A1.
- **Decidability as an admitted condition.** `bool_irrefl_witness_classification` and `bool_irrefl_nonempty_classification` carry `[∀ x y, Decidable (r x y)]`. It is used only for `by_cases` on `r true false` / `r false true`; it is there to stay inside `{propext, Quot.sound}` (no `Classical.choice`), not because the mathematics needs it. The paper and ledger (`CL-PD-TRANSPOSE`, `CL-PD-INVENTORY`) state the hypothesis explicitly; nothing describes the census as holding for undecidable `r`. Not an unearned identity.
- **Functions `Nat → X` / `Fin (n+2)` treated as data.** `witnessed_irrefl_on_every_larger_carrier` quantifies over `n : Nat` and builds a relation on `Fin (n+2)`; `single_oriented_witness_consistent` and `multiplicity_invisible_to_presence` use `W : Bool → Bool → Nat`. These are metatheoretic constructions (finitude rule). The paper's prose "a witnessed irreflexive structure exists on every carrier of size ≥ 2" is a metatheoretic ∀ over sizes; no docstring claims the system possesses the totality of carriers. Flagged for the textbook, not a defect.
- **Operation families** `F : (α → α) → Prop` and `Clos F` are external data; `Irred` quantifies over an inductively closed, possibly infinite family. A4 is thus explicitly "family-relative all the way down" (docstring of `merger_erases`), i.e. relative to an externally declared family. Not presented as internal.
- **Library lemmas doing work:** `List.mem_append`, `Bool.noConfusion`, `Bool.not_not`, `Subsingleton.elim`, `omega` (for `Fin` value inequality; this is where `propext, Quot.sound` enter in `witnessed_irrefl_on_every_larger_carrier` and `multiplicity_invisible_to_presence`). None smuggles content.
- Unearned identity: none found. Silently assumed observer: none found (the module's observer results are stated as facts about `Bool → Bool` classifiers). Unspecified correspondence between presentations: none found (a "presentation" is just a function; `const_presentation_unfaithful` names none, see §11). Cost function: none. Admitted condition later described as forced: see §11 on `Irrefl` and the phrase "forces the two-element carrier" — the paper says "with irreflexivity", so scoped. Finite computation presented as universal: none in Lean; the paper keeps `[finite computation]` (carrier ≤ 3) separate from the carrier-general theorems.

## 5. Derived consequences

Used by: `ObserverInventory` (`open PrimDiff`; whole module builds on `D2`, `D2rev`, `S2`, `Push`, `CollapseCollision`, `Clos`), `Bridge` (`Irrefl`, `S2`, `D2` in `irrefl_law_not_entailed`, `equivariant_witness_is_S2`, `equivariant_not_D2`), `Apartness` (`Irrefl`, `Sym`, `Clos`, `D2_irrefl`), `PrimitiveCore` (candidate `A` is `S.r S.a S.b ∧ Irrefl S.r`, candidate `E` is `Irred S.Ops S.a S.b`; `D2` as a concrete setting), `PrimitiveCats` (`IrreflObj`, `d2Obj`, `s2Obj`, swap automorphism facts), `ContactBridge` (`Irrefl (obsApart O)`, `CollapseCollision` of the non-identification relation), `ContactKernel` (`D2`, `D2_irrefl`, `D2_witness` as the Boolean kernel), `InterpreterBoundary` (`FidelityObstruction Irrefl`), `PrimitiveContact` (`D2` setting), `PrimitivePassage`, `Completion`, `RefusalFrontier` (re-uses `Irrefl`). `irrefl_witness_ne` is the lemma most often consumed downstream (dependency graph lists consumers `PrimitiveCats.lean`, `PrimitiveCore.lean`). The dependency graph records `citing_claims: []` for `selfdiff_consistent`; the ledger cites it only indirectly (through `CL-PD-INVENTORY`'s "a structure can assert its pair while failing irreflexivity").

## 6. Counterexamples and limitations

Countermodels: `selfdiff_consistent` / `one_point_hosts_bare_witness` / `collapse_unobstructed_without_fidelity` (all the same witness, `fun _ _ => True` on `Unit`): refute A1 → A3, A1 → A1i and "a two-element carrier is forced without irreflexivity". `symm_selfdiff_consistent`: symmetry does not restore A1 → A3. `meta_diff_without_assertion` (empty relation on `Bool`): A3 → A1 fails. `merger_erases` (a constant map in `F`): A3 → A4(F) fails for nonempty families. `orientation_data_invisible_to_collapse`, `D2_S2_collapse_equiv`: collision profiles do not classify. `single_oriented_witness_consistent`: two witnesses are not forced. `multiplicity_invisible_to_presence`: multiplicity is invisible to presence. `const_presentation_unfaithful`: fidelity of presentations is not automatic.

What the module does not prove:
- It does not prove that irreflexivity is the *weakest* axiom with the soundness-transfer property; only three axiom choices are compared (paper S9 says so).
- `D2_initial_pointed` proves initiality for *point-preserving* maps only (the uniqueness clause ranges over `g` with `g false = a`, `g true = b`); it does not say the edge-preserving maps from `D2` are unique.
- `obstruction_under_irrefl` does not use, and does not need, irreflexivity of the source `r`: the one-point self-difference's collapse along the identity is itself a `FidelityObstruction Irrefl` (checked by probe, §8). So "bare assertion's collisions never rise to obstruction" is not a theorem of this file; what is true is that `FidelityObstruction (fun _ => True)` is empty by definition.
- `multiplicity_invisible_to_presence`'s witnesses (`W1 = const 1`, `W2 = const 2`) have positive multiplicity on the diagonal, so their presence relation is the total relation, not an irreflexive one; the theorem is about presence truncation only.
- `merger_erases` needs a constant map in `F`; the weaker hypothesis "a merge of the designated pair is in `F`" (the paper's S8 wording) is handled in Python only.
- Nothing is proved about carriers of size 3 or more beyond existence (`witnessed_irrefl_on_every_larger_carrier`); the "exhaustive matrix" is `artifacts/primdiff.json`, carrier ≤ 3, Python only (paper S9 records this).

## 7. Axiom dependencies

All 44 theorems are within `{propext, Quot.sound}`; 31 use no axiom at all; `propext` appears where `funext`/`propext` or `simp` is used; `Quot.sound` enters via `funext`/`omega`. None exceed the allowed set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 44 theorems appear in `artifacts/lean_axioms.txt` and in the root's `#print axioms` inventory (`lean4/Derivation.lean` lines 140–182). The paper cites them in `paper/primitive_difference.md` (S2–S8), `paper/observer_inventory.md`, `paper/native_derivation_map.md` (row "two-ness ⇒ orientation FALSE"), and ledger entries `CL-PD-TRANSPOSE`, `CL-PD-INVENTORY`, `CL-G-DIRECT-SWAP` (contrast citation). Probe run (file `textbook/audit/probes/B/p1.lean`, `lake env lean`, exit 0): `#print axioms PrimDiff.selfdiff_consistent` → no axioms; `#print axioms PrimDiff.obstruction_under_irrefl` → no axioms; `#check` confirms the signature `r a b → c a = c b → FidelityObstruction Irrefl r c` with no `Irrefl r` premise; and the term `obstruction_under_irrefl (a := ()) (b := ()) trivial rfl : FidelityObstruction Irrefl (fun _ _ : Unit => True) (fun _ => ())` type-checks, i.e. the bare one-point self-difference is "obstructed relative to `Irrefl`".

## 9. Related Python implementations

`code/derivation/primdiff.py`: `Pointed`, `enumerate_pointed`, `a1`, `irreflexive`, `a1i`, `a3`, `closure`, `a4`, `merge_map`, `implication_matrix` (carrier ≤ 3), `two_element_report` (initiality echo), `automorphisms`, `invariant_separating_classifiers`, `observer_report`, `pushforward`, `collision`, `transpose`, `symmetrize`, `irreflexive_relations_on`, `transposition_report`, `collapse_report`, `carrier_table`, `collision_profile`, `pointed_isomorphic`, `frontier_profile_countermodel`. Artifact `artifacts/primdiff.json`. Tests `tests/test_primdiff.py` (e.g. `test_carrier_swap_carries_each_orientation_onto_the_other`, `test_unpointed_irrefl_nonempty_census_on_two`, `test_collapse_collision_and_pushforward`, `test_observer_orientation_gap`, `test_frontier_profiles_do_not_classify`).

## 10. Textbook placement proposal

- Prerequisites: a relation on a type; function composition; what a countermodel is; the difference between a statement *in* the object language (an asserted pair) and a statement *about* it (metatheoretic `≠`).
- Substantive: `irrefl_witness_ne`, `selfdiff_consistent`, `meta_diff_without_assertion`, `factors_through_point_iff`, `no_witness_on_subsingleton`, `D2_initial_pointed`, `witnessed_irrefl_on_every_larger_carrier`, `CollapseCollision`/`FidelityObstruction` with `bare_collapse_admissible`, `obstruction_under_irrefl`, `collision_transpose_invariant`, `D2_S2_collapse_equiv`, `D2_not_pointed_iso_S2`, `bool_irrefl_witness_classification`, `bool_irrefl_nonempty_classification`, `symmetric_no_equivariant_classifier` + `swap_is_S2_automorphism`, `oriented_rigid`, `oriented_classifier_exists`, `swap_auto_of_S2_not_of_D2`, `irred_empty_iff_ne`, `irred_antitone`, `merger_erases`, `multiplicity_invisible_to_presence`, `single_oriented_witness_consistent`. Auxiliary: the `decide`-level facts about `D2`/`S2`, the two list lemmas, `push_witness`, `collision_of_identifying_witness`, `collision_not_irrefl`, `clos_empty_id`, `id_presentation_faithful`, the swap-twice lemmas, `sym_*`.
- Lesson title: "One asserted pair: when does 'different' mean anything?" Question answered: which single axiom makes an asserted pair `r a b` entail that `a` and `b` are two things, and what does collapsing them then cost.
- Recommend omitting: `one_point_hosts_bare_witness` and `collapse_unobstructed_without_fidelity` (verbatim aliases of `selfdiff_consistent`; teach the one countermodel under one name), `const_presentation_unfaithful` (its statement is the hypothesis `Irrefl r'` at `v`; teach the idea in prose), `repetition_*` (generic list facts), `sym_D2_eq_S2` (`rfl`).

## 11. Interpretation findings

1. `obstruction_under_irrefl` — docstring: "With irreflexivity protected: the same collision now violates the protected law in the pushforward — collapse of a witnessed pair is obstructed *relative to preservation of `Irrefl`*"; paper S3: "**A1 + Irrefl: the same collision now violates the protected law**". Lean: `r a b → c a = c b → FidelityObstruction Irrefl r c`, with no `Irrefl r` premise. The theorem is *stronger* than the prose suggests (it holds for bare A1 too; probe in §8 instantiates it on the one-point self-difference). The prose is not false, but "preservation" and "A1 + Irrefl" invite the reading that the source must be irreflexive for the obstruction to arise; it need not. Answer to the brief's question: conditional on `r a b` and `c a = c b` only. Classification: INTERPRETATION DEFECT (minor; hypothesis structure misdescribed, no false claim).
2. `collapse_unobstructed_without_fidelity` — docstring: "Without a protected law the collision never rises to obstruction: the one-point self-difference is a legitimate bare-assertion structure"; paper S7: "Bare assertion ... its collisions never rise to obstruction (S3)". Lean statement: `∃ r : Unit → Unit → Prop, r () ()` (proof term `selfdiff_consistent`). The Lean says nothing about collisions or obstruction. The intended fact ("with `P := fun _ => True`, `FidelityObstruction P r c` is unsatisfiable") is true by unfolding the definition but is not what the cited theorem states; and with `P := Irrefl` the bare collision *does* rise to obstruction (finding 1). Classification: INTERPRETATION DEFECT (the theorem name and docstring promise a statement the Lean does not make).
3. `const_presentation_unfaithful` — docstring: "Constant presentations into any irreflexive target lose every asserted pair". Lean: `(hi : Irrefl r') (v : β) : ¬ r' v v`, i.e. `hi v`. No source relation, no presentation and no asserted pair occur in the statement; the conclusion is the hypothesis. Vacuity check: not vacuous (the hypothesis is satisfiable), but the theorem has no content beyond `Irrefl`. Classification: INTERPRETATION DEFECT (the docstring describes a theorem about presentations; the Lean is a restatement of irreflexivity).
4. `symmetric_no_equivariant_classifier` — docstring: "On the symmetric two-element difference, every classifier that is equivariant under the swap automorphism is constant: symmetric primitive difference admits no definable observer." Lean: `∀ f : Bool → Bool, (∀ x, f (not x) = f x) → f false = f true`; `S2` does not occur. The statement is a fact about swap-invariant maps on `Bool` and is true independently of any relation; the link to `S2` is `swap_is_S2_automorphism`. The paper (S4) scopes it correctly ("concerns invariant separating classifiers into `Bool`"); "no definable observer" in the docstring overreads. Classification: INTERPRETATION DEFECT (minor, docstring only).
5. `merger_erases` — paper S8: countermodel "merge map on the designated pair" refutes A3 → A4(F). Lean hypothesis: `F (fun _ => v)`, a *constant* map in `F`. The merge-map case is covered by the Python matrix (`merge_map`), not by this Lean theorem (the generalisation is one line, but it is not in the file). Classification: INTERPRETATION DEFECT (minor; evidence pointer slightly off).
6. Finitude: `witnessed_irrefl_on_every_larger_carrier` ("exists on *every* carrier of size at least two") and the `Nat`-valued multiplicity functions are metatheoretic quantifications; no prose was found treating them as system-internal totalities. No defect; noted for the textbook.
7. Vacuity: no theorem has jointly unsatisfiable hypotheses; `orientation_data_invisible_to_collapse` part (ii) is `True ↔ True` under the constant map (both relations collide), which is the intended content but is weak as a statement.
