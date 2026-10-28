# Audit: Breaking

| field | value |
|---|---|
| Path | lean4/Derivation/Breaking.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 542f74adfb6eb96e |
| Lines | 445 |
| Imported by root `Derivation.lean` | yes (line 62) |
| Imports | **none explicit** (no `import` line; the implicit core `Init` prelude only — the header says so and withdraws an earlier "imports NOTHING"). It imports no module of this development: not `Basic`, not `PrimDiff`, not `DiffInterface`. |
| Declarations | 2 structures (`Break`, `Symmetry`), 1 inductive (`Tri`, with `deriving DecidableEq`), 15 defs (`SingleOrbit`, `emptyBreak`, `fourBreak`, `Selector`, `Represents`, `OrbitConstant`, `Equivariant`, `boolBreak`, `constFalse`, `SymSelector`, `SymOrbitConstant`, `SymEquivariant`, `ofBreak`, `rot`, `triSymmetry`), 15 theorems; namespace `Breaking` |
| Axiom reports in `artifacts/lean_axioms.txt` | 7 lines, all with **no axioms**: `no_orbit_constant_equivariant_endomap`, `no_orbit_constant_equivariant_selector`, `no_selector_of_no_common_fixed_point`, `no_common_fixed_point`, `no_fixed_point_free_involution_on_Tri`, `selector_exists_at_common_fixed_point`, `selector_iff_common_fixed_point`. Not in artifact (8): `ne_image`, `two_cycle`, `fourBreak_not_singleOrbit`, `boolBreak_singleOrbit`, `constFalse_represents`, `constFalse_orbitConstant`, `constFalse_not_equivariant`, `imposable_but_not_equivariant` |
| Forbidden tokens (sorry/admit/axiom) | none found (the header's prose uses the word "axiom" mid-line; the gate pattern `^\s*axiom\s` is not triggered — not re-run here) |

## 1. Mathematical purpose

**Its model is not the regime model.** The module is a self-contained abstract setting with no reference to regimes, tokens, contexts, observers, `DiffObs` or anything else in the development; its header's last section says explicitly that it "proves nothing about `DiffObs`, `PresIso`, `NonZeroPair`, or any other structure in this repository" and that no bridge is proved. The paper (`paper/representative_selection.md`) calls it "Layer 2" and records that "Layer 3 still does not exist: no proof connects `Break` or `Symmetry` to the tied delta pair."

What it studies: a *reflection* — a carrier with a fixed-point-free involution (`Break`) — and, more generally, a family of transformations with no common fixed point (`Symmetry`). The question is whether a *selector* (an endomap meant to pick one element of each reflected pair) can be both orbit-constant (the same value on `w` and its reflection) and equivariant (commuting with the reflection). It cannot, given an inhabitant: the two laws compose to say the selected value is fixed by every symbol, and no point is. The exact cost is stated both ways: an orbit-constant equivariant selector exists iff some point is fixed by every symbol. The module polices its own ceiling: `Break` asserts no inhabitance (`emptyBreak`) and no single orbit (`fourBreak`), `ne_image` restates a field, the three-point carrier admits no fixed-point-free involution at all (so the `Symmetry` generalisation is not cosmetic), and a general even-cardinality claim is withdrawn as OPEN because the module uses no counting.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Break` | 84 | structure | `Whole : Type`, `e : Whole → Whole`, involutive, no fixed point | ADMITTED (declared shape; "not forced") |
| `SingleOrbit B` | 107 | def | any two elements are equal or reflections | ADMITTED |
| `emptyBreak` | 112 | def | `Break` on `Empty` — no inhabitance law | ADMITTED (witness) |
| `fourBreak` | 122 | def | `Break` on `Bool × Bool`, flipping the first coordinate | ADMITTED (witness) |
| `Selector B` | 146 | def | `B.Whole → B.Whole` | ADMITTED |
| `Represents B s` | 149 | def | `∀ w, s w = w ∨ s w = e w` | ADMITTED |
| `OrbitConstant B s` | 153 | def | `∀ w, s (e w) = s w` | ADMITTED |
| `Equivariant B s` | 157 | def | `∀ w, s (e w) = e (s w)` | ADMITTED |
| `boolBreak` | 179 | def | `Break` on `Bool` with `not` | ADMITTED (witness) |
| `constFalse` | 196 | def | the constant selector `false` on `boolBreak` | ADMITTED (witness) |
| `Symmetry` | 243 | structure | `Whole`, `Sym`, `act : Sym → Whole → Whole`, `no_common_fixed : ∀ w, ∃ g, act g w ≠ w` | ADMITTED (declared shape; no group laws) |
| `SymSelector`, `SymOrbitConstant`, `SymEquivariant` | 249–257 | def | the selector notions over a family | ADMITTED |
| `ofBreak B` | 314 | def | `Break` as a one-symbol `Symmetry` | ADMITTED |
| `Tri`, `rot`, `triSymmetry` | 322–334 | inductive/def/def | three points under a three-fold rotation | ADMITTED (witness) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `ne_image` | 94 | `w ≠ B.e w` (the `e_no_fixed` field, symmetric form) | FROZEN (field restated; docstring says so) | not in artifact | A |
| `two_cycle` | 99 | `B.e (B.e w) = w` (the `e_involutive` field) | FROZEN (field restated) | not in artifact | A |
| `fourBreak_not_singleOrbit` | 138 | `¬ SingleOrbit fourBreak` (witness `(false,false)`, `(false,true)`) | REFUTED (of "a `Break` has one orbit") | not in artifact | S |
| `no_orbit_constant_equivariant_endomap` | 172 | for any `B`, inhabitant `w`, selector `s`: `OrbitConstant ∧ Equivariant → False` | CONDITIONAL:an inhabitant `w : B.Whole` | none | S |
| `boolBreak_singleOrbit` | 188 | `SingleOrbit boolBreak` | VERIFIED_FINITE | not in artifact | A |
| `constFalse_represents` | 198 | `Represents boolBreak constFalse` | VERIFIED_FINITE | not in artifact | A |
| `constFalse_orbitConstant` | 204 | `OrbitConstant boolBreak constFalse` | FROZEN (rfl) | not in artifact | A |
| `constFalse_not_equivariant` | 210 | `¬ Equivariant boolBreak constFalse` | REFUTED | not in artifact | S |
| `imposable_but_not_equivariant` | 214 | `(Represents ∧ OrbitConstant) ∧ ¬ Equivariant` for `constFalse` | VERIFIED_FINITE (bundle) | not in artifact | S |
| `no_selector_of_no_common_fixed_point` | 269 | for any action, inhabitant `w`, `s`: `¬ ∃ p, ∀ g, act g p = p → OrbitConstant → Equivariant → False` | CONDITIONAL:inhabitant, no common fixed point | none | S |
| `no_common_fixed_point` | 283 | `Symmetry`'s field implies `¬ ∃ p, ∀ g, act g p = p` (one direction) | FROZEN | none | A |
| `no_orbit_constant_equivariant_selector` | 306 | for any `Symmetry`, inhabitant, selector: `SymOrbitConstant ∧ SymEquivariant → False` | CONDITIONAL:inhabitant | none | S |
| `no_fixed_point_free_involution_on_Tri` | 347 | no `e : Tri → Tri` is both involutive and fixed-point-free | REFUTED (case analysis on three points) | none | S |
| `selector_exists_at_common_fixed_point` | 398 | if `p` is fixed by every `g`, the constant selector at `p` is orbit-constant and equivariant | CONDITIONAL:a common fixed point | none | S |
| `selector_iff_common_fixed_point` | 415 | given an inhabitant: (∃ orbit-constant equivariant `s`) ↔ (∃ common fixed point) | CONDITIONAL:inhabitant `w : W` | none | S |

## 4. External and admitted assumptions

- `Break` and `Symmetry` are declared shapes; the header says neither is forced. `Symmetry.no_common_fixed` (`∀ w, ∃ g, act g w ≠ w`) is stronger than the premise the obstruction spends (`¬ ∃ p, ∀ g, act g p = p`); the converse would need decidability and is not proved (docstring, correct).
- The inhabitant hypothesis is explicit in every obstruction theorem; over `emptyBreak` the obstruction vanishes (docstring, correct). `Represents` is never a hypothesis of an obstruction theorem (docstring, correct).
- `Whole : Type`, `Sym : Type` are universe parameters (metatheory). No `Nat`, lists or counting are used — the header's "about USE rather than dependency" claim was checked by reading: the proofs use `Bool.noConfusion`, `Tri.noConfusion`, `congrArg`, `rfl`, `decide` (in `triSymmetry.no_common_fixed`) and equation composition only.
- Library lemmas doing work: `Bool.noConfusion`, `congrArg Prod.fst/snd`, `Empty.elim`, `decide` on `Tri`; nothing else.
- Unearned identity: none (the one identity-flavoured result, `ne_image`, is labelled as a field restated). Unrestricted external universe: `Type` parameters only. Unbounded function: none. Silently assumed observer: none. Unspecified correspondence between presentations: none inside the module — and the module says the correspondence to the tied delta pair is *not* established. Cost function: none. Admitted condition later described as forced: none found; the header withdraws two earlier overclaims ("two-ness derived", "every proof an immediate corollary of a field"). Finite computation presented as universal: the even-cardinality claim was withdrawn precisely to avoid this; only the `Tri` case is proved.

## 5. Derived consequences

No Lean module consumes `Breaking.*` (grep: only `Derivation.lean`'s `#print axioms`). No `CL-` ledger entry names any `Breaking` theorem (grep for the word "Breaking" in `paper/paper_claim_ledger.md`: no hit). The owning write-up is `paper/representative_selection.md` ("Layer 2 — proved, and now AUDITED", lines 118–160), which lists `no_orbit_constant_equivariant_endomap`, `imposable_but_not_equivariant`, `no_orbit_constant_equivariant_selector`, `no_fixed_point_free_involution_on_Tri`, `selector_exists_at_common_fixed_point`, `no_selector_of_no_common_fixed_point`, `no_common_fixed_point`, `selector_iff_common_fixed_point`, and states that Layer 3 (a connection to the tied delta pair) does not exist. `code/derivation/completion.py` lines 842–849 classify five of the theorem names.

## 6. Counterexamples and limitations

- Countermodels: `emptyBreak` (no inhabitance), `fourBreak` + `fourBreak_not_singleOrbit` (no single orbit), `constFalse_not_equivariant` (a representative orbit-constant selector exists and fails exactly at equivariance), `no_fixed_point_free_involution_on_Tri` (`Break` has no three-point model).
- Not proved (and stated as such): that every finite `Break` carrier has even cardinality (OPEN); any quotient/projection/section reading; any bridge to the repository's regime model, tied minima, or `DiffObs`; that `Break` or `Symmetry` is forced; the converse `¬ ∃ common fixed point → ∀ w, ∃ g, act g w ≠ w`.

## 7. Axiom dependencies

The seven reported theorems use no axioms at all. The eight unreported theorems were read: `boolBreak_singleOrbit`, `constFalse_*`, `imposable_but_not_equivariant`, `fourBreak_not_singleOrbit`, `ne_image`, `two_cycle` use only `rfl`, `Or.inl/inr`, `Bool.noConfusion`, `congrArg` — no `propext`, no `Quot.sound`, no `decide` on `Prop` instances; expected axiom-free, but **not measured** (no `#print axioms` exists for them and no probe was run). None exceed: none among the measured.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Seven of fifteen theorems appear in `artifacts/lean_axioms.txt` (root lines 1636–1642); the eight finite-example and field-restating theorems do not. The paper write-up cites eight theorems by name, of which seven are in the artifact and one (`imposable_but_not_equivariant`) is not. No probe run.

## 9. Related Python implementations

None implement `Break`/`Symmetry`/selectors. Grep hits for "equivariant" in `code/derivation/engine.py`, `iso.py`, `bridge.py` and `tests/test_equivariance.py` concern the regime model's isomorphism equivariance, a different notion; `code/derivation/boundary_cancellation.py` line 141 emits a report key `fixed_point_free` (relation to this module not checked). `code/derivation/completion.py` classifies five theorem names.

## 10. Textbook placement proposal

- Prerequisites: none from the development (the module is self-contained); the notion of an involution and of a map commuting with it.
- Substantive: `Break`, `Symmetry`, the selector laws, `no_orbit_constant_equivariant_selector`, `no_selector_of_no_common_fixed_point`, `selector_iff_common_fixed_point`, `imposable_but_not_equivariant`, `no_fixed_point_free_involution_on_Tri`, and the two omission witnesses (`emptyBreak`, `fourBreak_not_singleOrbit`). Auxiliary: `ne_image`, `two_cycle`, `boolBreak_singleOrbit`, `constFalse_*`, `no_common_fixed_point`, `ofBreak`.
- Lesson title: "A side can be imposed but not chosen symmetrically." Question answered: can a rule pick one of two reflected things while respecting the reflection? Only if something is fixed by every symmetry.
- Recommend omitting: `ne_image` and `two_cycle` as theorems (fields restated; the module says so); or, if kept, teach them as the example of a result that must not be cited as a derivation. Place the whole lesson outside the regime-model sequence, with the explicit note that no Layer 3 connects it.

## 11. Interpretation findings

1. Header "Verification boundary": "`lean4/Derivation.lean` imports this module and prints an axiom report for each of its exported theorems, so they appear in `artifacts/lean_axioms.txt`". Checked: the root prints seven reports; eight theorems (`ne_image`, `two_cycle`, `fourBreak_not_singleOrbit`, `boolBreak_singleOrbit`, `constFalse_represents`, `constFalse_orbitConstant`, `constFalse_not_equivariant`, `imposable_but_not_equivariant`) have none. The header's own last paragraph hedges ("'Axiom-free' here means those enumerated reports, not a proof that the inventory names every declaration in this file"), and `representative_selection.md` line 30 repeats "reports every one of its exported" theorems. Classification: INTERPRETATION DEFECT (minor; the unreported theorems are elementary and almost certainly axiom-free, but "each" is false as written).
2. `no_orbit_constant_equivariant_endomap` — paper: "given an inhabitant, no selector is both `OrbitConstant` and `Equivariant`". Accurate, inhabitant named. The module's self-corrections (withdrawn name `no_global_section`, withdrawn "two-ness derived", withdrawn even-cardinality claim, withdrawn "exactly what the obstruction costs") are all recorded in place and match the Lean. No defect.
3. Answer to the brief's question: the module imports nothing of the development and its model is a separate abstract one (a type with an involution / a family of maps), not the regime model; no theorem relates it to regimes, tokens, deltas or observers, and the paper says the connecting layer does not exist.
4. Vacuity: the obstruction theorems need an inhabitant, which they take as a hypothesis; over `emptyBreak` they would be vacuous and the module says so. `Symmetry` is inhabited (`triSymmetry`, `ofBreak boolBreak`). None vacuous as stated.
