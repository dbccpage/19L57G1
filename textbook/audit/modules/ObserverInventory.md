# Audit: ObserverInventory

| field | value |
|---|---|
| Path | lean4/Derivation/ObserverInventory.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 4f21d10defb38a3f |
| Lines | 231 |
| Imported by root `Derivation.lean` | yes (line 16) |
| Imports | `Derivation.PrimDiff` |
| Declarations | 1 inductive (`Slot`, deriving `DecidableEq`, `Repr`), 7 def (`slotList`, `EmptyRel`, `zeroW`, `oneW`, `pushNot`, `edgeCount`, `isSymBit`), 1 anonymous `Decidable` instance, 17 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 17 lines (every theorem); axioms seen: none / `propext` / `propext, Quot.sound` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module records a *declared* nine-slot classification of objects the development already possesses on the two-element carrier — carrier, local state, support, defect, reversal, closure, residual, maps, terminal — and proves the small facts that bind each slot on `Bool`. Its header says explicitly that it "is not a dynamics, not a next challenge, and not a necessity claim about any slot". The content it adds beyond `PrimDiff` is: the empty relation joins the census (every decidable irreflexive relation on `Bool` is empty, `D2`, `D2rev` or `S2`); two witness assignments exist as data and neither is derived as unique; collision of a collapse map and obstruction relative to `Irrefl` are two readings of "defect", kept apart by the one-point self-difference; relation transpose and pushforward along the swap agree on `D2` and are different operations; the empty operation family closes to the identity; two residual readings of a local state disagree; and irreflexivity alone does not determine a local state (empty and `D2` both qualify). The paper notes (`paper/observer_inventory.md` §1) that the slot names were chosen after an outside grid was refused as vocabulary; the carving is a declared classification, not a derived one.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Slot` | 43 | inductive | the nine slot names | ADMITTED (declared classification) |
| `slotList` | 48 | def | the list of the nine constructors in order | ADMITTED |
| `EmptyRel` | 58 | def | the empty relation on `Bool` | ADMITTED |
| (instance) | 60 | instance | `Decidable (EmptyRel x y)` | ADMITTED (auxiliary) |
| `zeroW` | 115 | def | the zero witness assignment `Bool → Bool → Nat` | ADMITTED |
| `oneW` | 117 | def | one witness on `(false, true)`, zero elsewhere | ADMITTED |
| `pushNot` | 151 | def | `fun x y => r (not x) (not y)`, pushforward of `r` along the swap (as a precomposition) | ADMITTED |
| `edgeCount` | 204 | def | off-diagonal occupancy count of a decidable relation on `Bool` | ADMITTED |
| `isSymBit` | 208 | def | `1` iff both off-diagonal pairs hold | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `slot_count` | 52 | `slotList.length = 9` | VERIFIED_FINITE (`rfl`) | none | A |
| `slots_nodup` | 54 | `slotList.Nodup` | VERIFIED_FINITE (`decide`) | none | A |
| `empty_irrefl` | 63 | `Irrefl EmptyRel` | VERIFIED_FINITE | none | A |
| `empty_ne_D2` | 66 | `EmptyRel ≠ D2` | VERIFIED_FINITE | none | A |
| `bool_irrefl_full_classification` | 74 | for decidable irreflexive `r` on `Bool`: `r = EmptyRel ∨ r = D2 ∨ r = D2rev ∨ r = S2` | CONDITIONAL:`[∀ x y, Decidable (r x y)]`, `Irrefl r` | propext, Quot.sound | S |
| `witnesses_are_data` | 124 | `zeroW ≠ oneW`, `oneW false true = 1`, `oneW true false = 0`, `zeroW` has empty presence, presence of `oneW` is exactly `D2` | VERIFIED_FINITE | propext | S |
| `collision_is_not_obstruction` | 145 | there is `r` on `Unit` with `r () ()` and `¬ Irrefl r` (witness: constant `True`) | REFUTED (countermodel to fusing the two defect readings) | none | S |
| `transpose_involutive` | 154 | `Transpose (Transpose r) = r` for any `r` on any `α` | FROZEN (`rfl`) | none | A |
| `transpose_D2_eq_D2rev` | 157 | `Transpose D2 = D2rev` | VERIFIED_FINITE | propext, Quot.sound | A |
| `transpose_D2rev_eq_D2` | 166 | `Transpose D2rev = D2` | VERIFIED_FINITE | propext, Quot.sound | A |
| `pushNot_D2_eq_D2rev` | 175 | `pushNot D2 = D2rev` | VERIFIED_FINITE | propext, Quot.sound | A |
| `transpose_eq_pushNot_on_D2` | 180 | `Transpose D2 = pushNot D2` | VERIFIED_FINITE | propext, Quot.sound | S |
| `transpose_ne_pushNot` | 185 | there is `r` on `Bool` with `Transpose r ≠ pushNot r` (witness: the self-loop `{(false,false)}`) | REFUTED (countermodel to "the two reversal maps are one operation") | none | S |
| `closure_empty_family_is_identity` | 198 | `Clos (fun _ => False) f → ∀ x, f x = x` on `Bool` (instance of `PrimDiff.clos_empty_id`) | VERIFIED_FINITE (specialisation of a FROZEN lemma) | none | A |
| `residuals_not_unique` | 212 | `edgeCount D2 = 1`, `edgeCount S2 = 2`, `isSymBit D2 = 0`, `isSymBit S2 = 1`, `edgeCount D2 ≠ isSymBit D2` | VERIFIED_FINITE (`decide`) | none | S |
| `swap_not_auto_of_D2` | 220 | `¬ (∀ x y, D2 x y ↔ D2 (not x) (not y))` | VERIFIED_FINITE | none | A |
| `swap_not_auto_of_D2rev` | 227 | same for `D2rev` | VERIFIED_FINITE (`decide`) | none | A |

## 4. External and admitted assumptions

- The slot classification is a declared policy (`Slot`, `slotList`); the module proves nothing about why there are nine slots or why these.
- Decidability `[∀ x y, Decidable (r x y)]` in `bool_irrefl_full_classification`, `edgeCount`, `isSymBit`: admitted condition, needed only to case-split without `Classical.choice`; stated in the paper and ledger (`CL-PD-INVENTORY` "Assumptions").
- `zeroW`, `oneW : Bool → Bool → Nat` are metatheoretic functions presented as "witness assignments ... present when supplied"; the header is careful that they are supplied data, not derived.
- `transpose_involutive` is generic over `{α : Type}`; everything else is on the concrete carrier `Bool`.
- Library lemmas doing work: `simp` on `Bool` cases, `Bool.noConfusion`, `funext`/`propext`. Unearned identity: none found. Unrestricted external universe: only `α` in `transpose_involutive`, harmless. Unbounded function treated as internally available: none found (the `Nat`-valued residuals are explicitly "readings"). Silently assumed observer: none found. Unspecified correspondence between presentations: none found. Cost function without justification: `edgeCount`/`isSymBit` are two residual readings and the theorem's point is precisely that neither is singled out; the paper says `mu1`/`mu2` "are not selected here". Admitted condition later described as forced: none found (the paper withdrew an earlier over-reading of the terminal slot; see §11). Finite computation presented as universal: none found (carrier 3 is stated as out of scope).

## 5. Derived consequences

No other Lean module references `ObserverInventory.*` (grep of `lean4/Derivation/*.lean`: no hits outside the file). The root `Derivation.lean` prints its axioms. Ledger: `CL-PD-INVENTORY` (owner), `CL-PD-TRANSPOSE` (cites `swap_not_auto_of_D2rev`). Paper: `paper/observer_inventory.md` §§1–7; `paper/primitive_difference.md` S7 cites `transpose_D2_eq_D2rev` and `transpose_ne_pushNot`.

## 6. Counterexamples and limitations

- `collision_is_not_obstruction`: the constant-`True` relation on `Unit` asserts its pair and is not irreflexive, so "a collision of a collapse map" (which exists on that structure) and "source irreflexivity" are different things. Note the Lean statement mentions neither `CollapseCollision` nor `FidelityObstruction`; it only says `r () () ∧ ¬ Irrefl r`. The reading "collision ≠ obstruction" is assembled in the docstring from this plus `PrimDiff.collapse_unobstructed_without_fidelity` and `PrimDiff.obstruction_under_irrefl` (see PrimDiff §11, finding 2: the second of these also does not mention obstruction).
- `transpose_ne_pushNot`: the self-loop `{(false,false)}` separates relation transpose from swap-pushforward.
- `residuals_not_unique`: `edgeCount` and `isSymBit` disagree on `D2`.
- Not proved: anything about carrier 3; any uniqueness of the slot carving; any next state or dynamics; that the witness store must be inhabited.
- `bool_irrefl_full_classification` holds for relations whose values are pointwise decidable; the proof duplicates the case analysis of `PrimDiff.bool_irrefl_nonempty_classification` rather than reusing it.

## 7. Axiom dependencies

All 17 within `{propext, Quot.sound}`; 10 use none. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 17 theorems are in `artifacts/lean_axioms.txt`; all are cited in `paper/observer_inventory.md` and listed under `CL-PD-INVENTORY` (all but `swap_not_auto_of_D2rev`, which `CL-PD-TRANSPOSE` lists). No probe run beyond the build (nothing in the file needed one: every proof is a finite case split or `decide`).

## 9. Related Python implementations

`code/derivation/observer_inventory.py`: `local_states`, `irrefl_census_on_two`, `witnesses_report`, `reversal_report`, `defect_report`, `edge_count`, `is_sym_bit`, `residuals_report`, `inventory_report`; artifact `artifacts/observer_inventory.json`. Tests `tests/test_observer_inventory.py`: `test_nine_slots_and_no_duplicates`, `test_irrefl_census_is_exactly_the_four`, `test_witnesses_are_data_not_a_unique_inhabitant`, `test_reversal_transpose_and_swap_agree_on_D2_and_differ`, `test_defect_collision_is_not_source_irreflexivity`, `test_residuals_are_not_unique`, `test_vocabulary_refusal_record_is_present_and_pinned`, and the named-elsewhere citation checks.

## 10. Textbook placement proposal

- Prerequisites: PrimDiff (`D2`, `D2rev`, `S2`, `Irrefl`, `Transpose`, `Clos`); the distinction between a declared classification and a derived one.
- Substantive: `bool_irrefl_full_classification` (the full four-element census), `witnesses_are_data`, `collision_is_not_obstruction` (as the "two defect readings" point), `transpose_eq_pushNot_on_D2` + `transpose_ne_pushNot` (two maps that agree on the one object studied and differ elsewhere), `residuals_not_unique`. Auxiliary: `slot_count`, `slots_nodup`, `empty_irrefl`, `empty_ne_D2`, the three `*_eq_D2rev`/`_eq_D2` equalities, `transpose_involutive`, `closure_empty_family_is_identity`, the two `swap_not_auto_*`.
- Lesson title: "An inventory is not a derivation." Question answered: on the two-point carrier, which objects already exist in each named slot, and which of the tempting uniqueness claims (one residual, one reversal, one witness store, one next state) fail.
- Recommend omitting: `Slot`/`slotList`/`slot_count`/`slots_nodup` as theorems (they only pin a list of names; mention the nine names in prose and the author's refusal note), and `closure_empty_family_is_identity` (a one-line specialisation of `PrimDiff.clos_empty_id`).

## 11. Interpretation findings

1. `collision_is_not_obstruction` — docstring: "Collision of a collapse exists on the one-point self-difference, which is not irreflexive. Collision of a map is therefore not the same reading as obstruction relative to `Irrefl`." Lean: `∃ r : Unit → Unit → Prop, r () () ∧ ¬ Irrefl r`. The statement establishes "asserts its pair and is not irreflexive"; the collision (`CollapseCollision r id` or along the constant map) and the obstruction notion are not in the statement, and the conclusion drawn ("not the same reading") is a gloss. The ledger `CL-PD-INVENTORY` phrases it correctly ("a structure can assert its pair while failing irreflexivity ... a collision exists without any protected law and rises to obstruction only relative to `Irrefl`"), citing the PrimDiff theorems for the second half. Classification: INTERPRETATION DEFECT (minor; the name promises a statement about two notions neither of which appears in the Lean).
2. Terminal slot — the paper and ledger record that an earlier sentence ("no next state is a function of the carrier and local state") was a non-sequitur and was withdrawn in favour of "irreflexivity does not determine the local state", which is exactly `empty_irrefl` + `D2_irrefl` + `empty_ne_D2`. The current prose matches the Lean. No defect (recorded as a corrected over-reading already handled by the authors).
3. Vacuity: none; all hypotheses satisfiable; the concrete equalities are non-trivial `decide`/case facts.
4. Finitude: `zeroW`/`oneW`/`edgeCount`/`isSymBit` are `Nat`-valued metatheoretic functions; the header calls them "data" supplied from outside; nothing reads them as system-internal. No defect.
