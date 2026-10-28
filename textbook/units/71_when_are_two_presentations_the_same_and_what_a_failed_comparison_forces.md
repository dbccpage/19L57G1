# Unit 71 — When Are Two Presentations the Same, and What Does a Failed Comparison Force?

**Claim.** Two presentations `p : X → P` and `q : X → Q` of a finite domain list `D : List X` are presentation-identical on `D` (`PresentationIdentityOn D p q`, defined as mutual factorization `FactorsOn D p q ∧ FactorsOn D q p`) if and only if they have the same fibers on `D` (`FiberIdentityOn D p q`), and if and only if the directional residual `DirectionalResidual D p q` (an ordered pair `(x, y)` in `D` merged by `p` and separated by `q`) is empty in both directions. When `p` does not factor through `q` on `D`, `forced_split_of_factorization_failure` yields a witness `DirectionalResidual D p q` together with `classCount D p < classCount D (pQ D [p, q])`; `ClosureSymmetry` packages the same pair as an `InternalSymmetryBreak D p q` whose involutive `transpose` swaps `(x, y)` to `(y, x)`; and `ResidualClosure` shows that passing to `jointPresentation D p q := pQ D [p, q]` closes the current comparison obstruction `(jointPresentation D p q) → q` by splitting the left face while breaking invariance under the generating pair-swap. In the `Metatheory` sub-namespace, quantifying over all `Bool`-valued views collapses identification to meta-level Lean equality (`attempted_absolute_identification_collapses_to_equality`) and refutes simultaneously satisfying both polarities (`attempted_absolute_polarities_are_refuted`).

---

## Question

Suppose two observers or instruments report on the same listed domain `D : List X` through maps `p : X → P` and `q : X → Q`, where `P` and `Q` need not share a codomain type. Under what exact condition on `D` do `p` and `q` carry the same distinction content without appealing to a view-independent identity outside all presentations? And if `p` fails to factor through `q` on `D`, what concrete witness, symmetry-breaking structure, and refinement step are forced by that failure?

---

## What we already possess

From previous units we already have:

- **Finite-domain presentations and factorization (`lean4/Derivation/Compression.lean`, Unit 61).** For `[DecidableEq X]`, `[DecidableEq P]`, `[DecidableEq Q]`, and `D : List X`:
  - `SameFiber p x y : Prop := p x = p y` (lines 41–42).
  - `FactorsOn D p q : Prop := ∀ x ∈ D, ∀ y ∈ D, p x = p y → q x = q y` (lines 45–46), with `factorsOn_refl` (line 48) and `factorsOn_trans` (line 52).
  - `SplitsAt D p q x : Prop := ∃ y ∈ D, p x = p y ∧ q x ≠ q y` (lines 59–60), and `not_factorsOn_iff_exists_split : ¬ FactorsOn D p q ↔ ∃ x ∈ D, SplitsAt D p q x` (lines 63–75).
  - `classes D p : List P := (D.map p).eraseDup` (lines 80–81) and `classCount D p : Nat := (classes D p).length` (lines 84–85), together with `classCount_le_of_factorsOn : FactorsOn D p q → classCount D q ≤ classCount D p` (lines 201–215).
  - The question-family presentation `pQ D Q : X → List Bool` (lines 243–244), which evaluates each predicate `q ∈ Q : List (X → Bool)` when `x ∈ D` and returns `[]` outside `D`, plus `pQ_factors_member` (lines 257–266).
- **World support vs. decorative notes (`lean4/Derivation/NoOutside.lean`, Unit 67).** A `World` record has operational `support : List Rule` and non-operational `notes : List Nat`; `supportView w := w.support` projects the operational part, `kernelEval R w` depends only on `w.support`, and `panelEquiv P w₁ w₂` equates worlds that agree on every member of an admissibility panel `P : AdmissibilityPanel` (`certNeg P E w` certifies panel failure).
- **Declared depth-1 generator profiles (`lean4/Derivation/Generator.lean`, Unit 68).** On the five-world family `W0..W4`, `declaredGeneratorIndex : Fin 5 → Fin 4` groups indices `0` and `1` into image `0`, while `depthOneProfile : Fin 5 → Bool × Bool × Bool` evaluates the three depth-1 admissibility probes and separates `0` from `1`.

What we do **not** yet have is:
1. A codomain-polymorphic equivalence relation `PresentationIdentityOn D p q` equating two presentations when each factors through the other on `D`, together with its equivalence to pointwise fiber agreement `FiberIdentityOn D p q` and to bilateral emptiness of directional residuals (`PresentationRelativity.lean`, lines 62–173).
2. The strict class-count jump `classCount D p < classCount D r` under a refinement split (`classCount_lt_of_refinement_split`, line 265) and its specialization to `jointPresentation D p q := pQ D [p, q]` (`forced_split_of_factorization_failure`, line 290; `jointPresentation_strict_of_factorization_failure`, line 356).
3. The explicit metatheoretic contrast (`PresentationRelativity.Metatheory`, lines 379–419) showing that quantifying over all views `v : α → Bool` collapses identification to `x = y` and refutes holding both `ViewIdentifies v x y` and `ViewSeparates v x y` for one view, contrasted with concretely exhibited pairs of views on `World`, `AdmissibilityPanel`, and `Fin 5` (lines 427–635).
4. The transpose-equivariant symmetry-breaking repackaging (`ClosureSymmetry.lean`, lines 32–166) and the single-step obstruction closure (`ResidualClosure.lean`, lines 29–122).

---

## New concept

Three files in `lean4/Derivation/` form a single three-stage chain:

```
PresentationRelativity.lean  ──►  ClosureSymmetry.lean  ──►  ResidualClosure.lean
(Mutual factorization,            (Ordered pair transpose    (Pair-swap invariance
 fiber identity,                   on X × X;                  InvariantUnderOn;
 DirectionalResidual,              InternalSymmetryBreak      jointPresentation splits
 classCount strict increase,       bijection with             left face and empties
 Metatheory contrast,              DirectionalResidual;       current residual while
 World / Panel / Generator         closure failure iff        breaking generating
 concrete witnesses)               symmetry break)            pair-swap invariance)
```

### Stage 1: Presentation identity, directional residuals, and forced splits (`PresentationRelativity.lean`)

1. **Fiber identity and presentation identity (lines 62–85).**
   - `FiberIdentityOn D p q : Prop := ∀ x ∈ D, ∀ y ∈ D, (p x = p y ↔ q x = q y)` (lines 62–63).
   - `PresentationIdentityOn D p q : Prop := FactorsOn D p q ∧ FactorsOn D q p` (lines 68–69).
   - `presentationIdentity_iff_fiberIdentity` (lines 71–85, axiom `[Quot.sound]`): `PresentationIdentityOn D p q ↔ FiberIdentityOn D p q`. Notice that `p : X → P` and `q : X → Q` can take values in completely different types `P` and `Q`; they are compared purely by which pairs in `D` they merge or separate.
2. **Directional residuals and equivalence properties (lines 91–173).**
   - `structure DirectionalResidual (D : List X) (p : X → P) (q : X → Q) where` (lines 91–97) has fields `left : X`, `right : X`, `left_mem : left ∈ D`, `right_mem : right ∈ D`, `identified_by_source : p left = p right`, and `separated_by_target : q left ≠ q right`. Because `DirectionalResidual` carries concrete elements `left, right : X`, it lives in `Type _`, not `Prop`.
   - `directionalResidual_refutes_identity` (lines 100–107): any `DirectionalResidual D p q` implies `¬ PresentationIdentityOn D p q`.
   - `ResidualEmptyOn D p q : Prop := ¬ Nonempty (DirectionalResidual D p q)` (lines 113–114).
   - `presentationIdentity_iff_residualEmpty` (lines 117–142): `PresentationIdentityOn D p q ↔ (ResidualEmptyOn D p q ∧ ResidualEmptyOn D q p)`. The reverse direction uses `Classical.byContradiction` to turn a failed equality `q x ≠ q y` (or `p x ≠ p y`) into a `DirectionalResidual`.
   - `presentationIdentity_equivalence` (lines 146–165): reflexivity, symmetry, and transitivity of `PresentationIdentityOn` on `D`. Notice that because the second and third arguments of `PresentationIdentityOn D` can have different codomain types, this is stated as a 3-way conjunction on a fixed codomain `P` rather than a Lean `Equivalence` instance across heterogeneous codomains.
   - `self_comparison_has_empty_residual` (lines 169–173): `ResidualEmptyOn D p p`.
3. **Relative identity against a question family and strict refinement under family enlargement (lines 179–258).**
   - `IdentityRelativeToQuestions D Q p : Prop := PresentationIdentityOn D p (pQ D Q)` (lines 179–180), with `identityRelativeToQuestions_iff` (lines 183–194): `IdentityRelativeToQuestions D Q p ↔ (FactorsOn D p (pQ D Q) ∧ FactorsOn D (pQ D Q) p)`.
   - `DirectionalResidualAt D p q x : Prop := ∃ y ∈ D, p x = p y ∧ q x ≠ q y` (lines 200–201), which is definitionally identical to `SplitsAt D p q x` (`splitsAt_iff_directionalResidualAt`, lines 207–210, proved by `Iff.rfl`).
   - When `Q₁ ⊆ Q₂` (`∀ q ∈ Q₁, q ∈ Q₂`), `family_enlargement_refines` (lines 225–234) shows `FactorsOn D (pQ D Q₂) (pQ D Q₁)`. If a new question `q` separates a `Q₁`-fiber (`SplitsAt D (pQ D Q₁) q x`), `family_split_refuses_relative_identity` (lines 239–246) shows `¬ IdentityRelativeToQuestions D (q :: Q₁) (pQ D Q₁)` and `family_enlargement_split_is_strict` (lines 251–258) combines `FactorsOn D (pQ D (q :: Q₁)) (pQ D Q₁)` with `¬ FactorsOn D (pQ D Q₁) (pQ D (q :: Q₁))`.
4. **Strict class-count increase and the joint presentation (lines 265–376).**
   - `classCount_lt_of_refinement_split` (lines 265–283, axioms `[propext, Quot.sound]`): if `FactorsOn D r p` and `SplitsAt D p r x` for some `x ∈ D`, then `classCount D p < classCount D r`. Its proof applies `Compression.strict_refinement_increases_classes` to `r` and `p`, converting `SplitsAt D p r x` into a pair separated by `r` and merged by `p`.
   - `forced_split_of_factorization_failure` (lines 290–321, axioms `[propext, Quot.sound]`): from `¬ FactorsOn D p q`, extracts `x, y ∈ D` with `p x = p y ∧ q x ≠ q y` via `Compression.not_factorsOn_iff_exists_split`, packages them as a `DirectionalResidual D p q`, and shows that on `pQ D [p, q]` the class count strictly increases: `classCount D p < classCount D (pQ D [p, q])`.
   - `jointPresentation D p q : X → List (P × Q) := pQ D [p, q]` (lines 327–328). Wait — why is the codomain `List (P × Q)` when `pQ` in `Compression.lean` took predicates? Let us check the exact signature in `PresentationRelativity.lean`! In `PresentationRelativity.lean`, lines 327–328, `p` and `q` have the **same** codomain type `P` (`(p q : X → P)`), so `[p, q] : List (X → P)` has homogeneous element type `X → P`, and `pQ D [p, q] : X → List P`!
   - `jointPresentation_factors_left` (lines 332–339) and `jointPresentation_factors_right` (lines 342–349) apply `pQ_factors_member` to the head `p` and second element `q` of `[p, q]`.
   - `jointPresentation_strict_of_factorization_failure` (lines 356–367, axioms `[propext, Quot.sound]`): for `p q : X → P`, `¬ FactorsOn D p q` implies `FactorsOn D (jointPresentation D p q) p ∧ FactorsOn D (jointPresentation D p q) q ∧ classCount D p < classCount D (jointPresentation D p q)`.
   - `directionalResidual_of_factorization_failure` (lines 372–376): for heterogeneous codomains `p : X → P` and `q : X → Q`, `¬ FactorsOn D p q → Nonempty (DirectionalResidual D p q)`.
5. **The `Metatheory` contrast and three concrete regime-calculus witnesses (lines 379–637).**
   - Inside `namespace Metatheory` (lines 379–419), for any type `α` and view `v : α → Bool`:
     - `ViewIdentifies v x y : Prop := v x = v y` (line 382).
     - `ViewSeparates v x y : Prop := v x ≠ v y` (line 385).
     - `AllViewsIdentify x y : Prop := ∀ v : α → Bool, ViewIdentifies v x y` (line 394).
     - `attempted_absolute_identification_collapses_to_equality` (lines 399–408, axiom-free): `AllViewsIdentify x y ↔ x = y`. For `[DecidableEq α]`, the forward direction instantiates `v := fun z => decide (z = x)`.
     - `attempted_absolute_polarities_are_refuted` (lines 413–417, axiom-free): `¬ (∃ v : α → Bool, ViewIdentifies v x y ∧ ViewSeparates v x y)`.
   - Outside `Metatheory`, three concrete domain families show that identification and separation coexist across **distinct** presentations without contradiction:
     1. **World support vs. support+notes (lines 427–478):** `supportNotesView (w : World) : List Rule × List Nat := (w.support, w.notes)` is injective (`supportNotesView_injective`, line 446, from `world_eq_iff_support_eq_and_notes_eq`, line 433). On `noteVariantA` and `noteVariantB` (imported from `NoOutside.lean`), `support_identifies_while_supportNotes_separates` (lines 455–461, axiom-free) establishes `supportView noteVariantA = supportView noteVariantB ∧ supportNotesView noteVariantA ≠ supportNotesView noteVariantB`, while `notes_update_kernel_results_agree` (lines 466–478) shows `kernelEval R w = kernelEval R { w with notes := notes' }`.
     2. **Panel extension (lines 484–541):** `panelEquiv_antitone` (line 484) and `panel_extension_refines_equivalence` (line 503) show that extending an admissibility panel `P₁` to `P₁ ++ P₂` refines `panelEquiv`, and `certNeg_extension_implies_source` (line 512) transfers a negative certificate backward. On the concrete worlds `sourcePanelWorld` and `extendedPanelWorld` (lines 522–532), `panel_extension_changes_verdict_not_world` (lines 536–541) shows that `coarsePanel` identifies them while `coarsePanel ++ [separatingEvaluator]` separates them and flips `certNeg`.
     3. **Declared generator index vs. depth-1 profile (lines 547–635):** `encodeDepthOneProfile : Bool × Bool × Bool → Fin 8` (lines 553–554) is injective (`encodeDepthOneProfile_injective`, line 556), so `depthOnePresentation : Fin 5 → Fin 8` has the same fibers as `depthOneProfile` (`depthOnePresentation_eq_iff`, line 568). On `generatorDomain := [0, 1, 2, 3, 4] : List (Fin 5)` (line 574), `declared_generator_index_comparison_does_not_factor` (lines 582–600) establishes `¬ FactorsOn generatorDomain declaredGeneratorIndex depthOnePresentation`, `declared_generator_index_comparison_forces_refinement` (lines 607–625) extracts a `DirectionalResidual` and strict `classCount` increase, and `declared_generator_profiles_disagree_at_pair` (lines 630–635) exhibits the exact witness `(0 : Fin 5), (1 : Fin 5)` merged by `declaredGeneratorIndex` and separated by `depthOneProfile`.

### Stage 2: Internal symmetry breaking (`ClosureSymmetry.lean`)

When `p` merges `x` and `y` (`p x = p y`) while `q` separates them (`q x ≠ q y`), what happens if we swap the roles of `x` and `y`?
- `transpose (pair : X × X) : X × X := (pair.2, pair.1)` (line 32) is an involution on `X × X` (`transpose_involutive`, line 50; `transpose_left`, line 35; `transpose_right`, line 39) whose fixed points are the diagonal pairs (`transpose_fixed : transpose pair = pair ↔ pair.1 = pair.2`, line 46).
- `structure InternalSymmetryBreak (D : List X) (p : X → P) (q : X → Q) where` (lines 72–80) packages `pair : X × X` with `left_mem : pair.1 ∈ D`, `right_mem : pair.2 ∈ D`, `pair_moved : transpose pair ≠ pair` (i.e. `pair` is off-diagonal, so `transpose` moves it), `source_invariant : p (transpose pair).1 = p pair.1 ∧ p (transpose pair).2 = p pair.2` (the source presentation `p` is invariant under `transpose` on `pair`), and `target_broken : ¬ (q (transpose pair).1 = q pair.1 ∧ q (transpose pair).2 = q pair.2)` (the target presentation `q` is not invariant under `transpose` on `pair`).
- `residual_to_internal_symmetry_break` (lines 84–113) and `internal_symmetry_break_to_residual` (lines 118–125) convert back and forth between `DirectionalResidual D p q` and `InternalSymmetryBreak D p q` on the **exact same underlying pair** `(r.left, r.right) = b.pair`.
- Consequently, `residual_nonempty_iff_internal_symmetry_break_nonempty` (lines 129–136, axiom `[propext]`) and `closure_failure_iff_internal_symmetry_break` (lines 154–164, axioms `[propext, Quot.sound]`) establish:
  $$\neg\,\mathrm{FactorsOn}\;D\;p\;q \;\Longleftrightarrow\; \mathrm{Nonempty}\;(\mathrm{InternalSymmetryBreak}\;D\;p\;q).$$

### Stage 3: Closing the current obstruction by common refinement (`ResidualClosure.lean`)

Once `¬ FactorsOn D p q` forces a witness `b : InternalSymmetryBreak D p q`, how is that specific comparison obstruction resolved, and what happens to the pair-swap invariance that `p` enjoyed?
- For any transformation `sigma : X → X`, `InvariantUnderOn D f sigma : Prop := ∀ x ∈ D, f (sigma x) = f x` (lines 29–30).
- `factorization_preserves_invariance` (lines 35–42, axiom `[Quot.sound]`): if `FactorsOn D p q`, `sigma` maps `D` into `D` (`∀ x ∈ D, sigma x ∈ D`), and `InvariantUnderOn D p sigma`, then `InvariantUnderOn D q sigma`.
- Contrapositively, `carrying_right_face_loses_generating_invariance` (lines 47–54, axiom `[Quot.sound]`): if `FactorsOn D r q` (so `r` carries the right face `q`), `sigma` preserves `D`, and `¬ InvariantUnderOn D q sigma`, then `¬ InvariantUnderOn D r sigma`.
- Specifically, on the pair `(x, y)` of a `DirectionalResidual D p q`, `carrying_right_face_splits_generating_pair` (lines 58–66) shows that any `r` with `FactorsOn D r q` separates `r.left` from `r.right` (`r res.left ≠ r res.right`), so `common_refinement_strictly_splits_left_face` (lines 72–82) yields `classCount D p < classCount D r` whenever `FactorsOn D r p` and `FactorsOn D r q`.
- For `jointPresentation D p q := pQ D [p, q]` (when `p, q : X → P` share a codomain), `current_directional_residual_is_empty` (lines 86–91) establishes `ResidualEmptyOn D (jointPresentation D p q) q`, `current_internal_symmetry_break_is_empty` (lines 95–102) establishes `¬ Nonempty (InternalSymmetryBreak D (jointPresentation D p q) q)`, and `common_refinement_closes_current_obstruction` (lines 106–120) packages the four-part closure receipt:
  1. `FactorsOn D (jointPresentation D p q) p`
  2. `FactorsOn D (jointPresentation D p q) q`
  3. `classCount D p < classCount D (jointPresentation D p q)`
  4. `ResidualEmptyOn D (jointPresentation D p q) q ∧ ¬ Nonempty (InternalSymmetryBreak D (jointPresentation D p q) q)`

---

## Plain-language interpretation

Think of `D` as a finite roster of items and `p`, `q` as two sorting clerks.
- Clerk `p` puts items into bins labeled by type `P`; clerk `q` puts the same items into bins labeled by type `Q`. Because their bin labels live in different alphabets (`P` vs. `Q`), asking whether `p(x) = q(x)` is a type error. Instead, we ask whether they group items the same way: whenever `p` puts `x` and `y` into the same bin, does `q` also put `x` and `y` into the same bin (`FactorsOn D p q`), and vice versa (`FactorsOn D q p`)?
- If `p` merges two items `x, y` that `q` separates, the pair `(x, y)` is a **directional residual** (`DirectionalResidual D p q`). Viewed as an ordered pair in `X × X`, swapping the two slots (`transpose (x, y) = (y, x)`) leaves `p`'s verdict unchanged (`p y = p x`) but changes `q`'s verdict (`q y ≠ q x`). That is an **internal symmetry break** (`InternalSymmetryBreak D p q`).
- To resolve the disagreement without throwing away either clerk's distinctions, we form the **joint presentation** `jointPresentation D p q`, which records `[p x, q x]` on `D`. The new clerk refines both `p` and `q`, has strictly more occupied bins than `p` (`classCount D p < classCount D (jointPresentation D p q)`), and has zero residual when compared against `q` (`ResidualEmptyOn D (jointPresentation D p q) q`). In doing so, the refined clerk necessarily gives up `p`'s invariance under swapping `x` and `y`.
- Crucially, closing the comparison `(jointPresentation D p q) → q` only resolves the **current** pair `(p, q)`. A third presentation `r` can still split a fiber of `jointPresentation D p q` and force another refinement step.

---

## Pseudocode

```text
FUNCTION factors_on(D, p, q):
    FOR EACH x IN D:
        FOR EACH y IN D:
            IF p(x) == p(y) AND q(x) != q(y):
                RETURN False
    RETURN True

FUNCTION presentation_identity_on(D, p, q):
    RETURN factors_on(D, p, q) AND factors_on(D, q, p)

FUNCTION directional_residuals(D, p, q):
    out = []
    FOR EACH x IN D:
        FOR EACH y IN D:
            IF p(x) == p(y) AND q(x) != q(y):
                APPEND (x, y) TO out
    RETURN out

FUNCTION internal_symmetry_breaks(D, p, q):
    out = []
    FOR EACH x IN D:
        FOR EACH y IN D:
            pair = (x, y)
            t = (y, x)
            IF t != pair:
                source_inv = (p(t.left) == p(pair.left)) AND (p(t.right) == p(pair.right))
                target_inv = (q(t.left) == q(pair.left)) AND (q(t.right) == q(pair.right))
                IF source_inv AND NOT target_inv:
                    APPEND pair TO out
    RETURN out

FUNCTION joint_presentation(D, p, q):
    RETURN (x |-> [p(x), q(x)] IF x IN D ELSE [])
```

---

## Python

The standalone check script `textbook/checks/u71_presentation_relativity.py` implements finite-domain presentations, fiber identity, directional residuals, transpose symmetry breaks, pair-swap invariance, the three concrete regime-calculus witnesses from `PresentationRelativity.lean`, the multi-pair involution counterexample from `ClosureSymmetry.md` / `ResidualClosure.md`, and the scope-separation check that closing `(p, q)` does not prevent a third presentation `r` from splitting `jointPresentation D p q`:

```python
from __future__ import annotations

import json
import pathlib
import sys
from typing import Callable, TypeVar

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.completion import KIND_ROLE_OVERRIDES  # noqa: E402

X = TypeVar("X")
P = TypeVar("P")
Q = TypeVar("Q")


def erase_dup(xs: list[P]) -> list[P]:
    out: list[P] = []
    for i, x in enumerate(xs):
        if x not in xs[i + 1 :]:
            out.append(x)
    return out


def classes(domain: list[X], p: Callable[[X], P]) -> list[P]:
    return erase_dup([p(x) for x in domain])


def class_count(domain: list[X], p: Callable[[X], P]) -> int:
    return len(classes(domain, p))


def factors_on(domain: list[X], p: Callable[[X], P], q: Callable[[X], Q]) -> bool:
    return all(
        q(x) == q(y)
        for x in domain
        for y in domain
        if p(x) == p(y)
    )


def fiber_identity_on(domain: list[X], p: Callable[[X], P], q: Callable[[X], Q]) -> bool:
    return all(
        (p(x) == p(y)) == (q(x) == q(y))
        for x in domain
        for y in domain
    )


def presentation_identity_on(domain: list[X], p: Callable[[X], P], q: Callable[[X], Q]) -> bool:
    return factors_on(domain, p, q) and factors_on(domain, q, p)


def directional_residuals(
    domain: list[X], p: Callable[[X], P], q: Callable[[X], Q]
) -> list[tuple[X, X]]:
    return [
        (x, y)
        for x in domain
        for y in domain
        if p(x) == p(y) and q(x) != q(y)
    ]


def transpose(pair: tuple[X, X]) -> tuple[X, X]:
    return (pair[1], pair[0])


def internal_symmetry_breaks(
    domain: list[X], p: Callable[[X], P], q: Callable[[X], Q]
) -> list[tuple[X, X]]:
    breaks: list[tuple[X, X]] = []
    for x in domain:
        for y in domain:
            pair = (x, y)
            t = transpose(pair)
            if t == pair:
                continue
            source_invariant = (p(t[0]) == p(pair[0])) and (p(t[1]) == p(pair[1]))
            target_broken = not ((q(t[0]) == q(pair[0])) and (q(t[1]) == q(pair[1])))
            if source_invariant and target_broken:
                breaks.append(pair)
    return breaks


def p_q(domain: list[X], questions: list[Callable[[X], P]]) -> Callable[[X], tuple[P, ...]]:
    domain_set = set(domain)

    def _present(x: X) -> tuple[P, ...]:
        if x in domain_set:
            return tuple(q(x) for q in questions)
        return ()

    return _present


def joint_presentation(
    domain: list[X], p: Callable[[X], P], q: Callable[[X], P]
) -> Callable[[X], tuple[P, ...]]:
    return p_q(domain, [p, q])


def invariant_under_on(
    domain: list[X], f: Callable[[X], P], sigma: Callable[[X], X]
) -> bool:
    return all(f(sigma(x)) == f(x) for x in domain)
```

---

## Line-by-line Python explanation

- **`erase_dup`, `classes`, `class_count` (lines 18–31):** Match `List.eraseDup`, `Compression.classes`, and `Compression.classCount` in `lean4/Derivation/Compression.lean` (lines 80–85), keeping the last occurrence of each image value in `D.map p` and counting distinct occupied fibers on `D`.
- **`factors_on` (lines 34–40):** Implements `FactorsOn D p q` (`∀ x ∈ D, ∀ y ∈ D, p x = p y → q x = q y`).
- **`fiber_identity_on` and `presentation_identity_on` (lines 43–52):** Implement `FiberIdentityOn D p q` and `PresentationIdentityOn D p q := FactorsOn D p q ∧ FactorsOn D q p`. The check script verifies on all 15 set partitions of `D = [0, 1, 2, 3]` (even across distinct codomain encodings, integer vs. string labels) that `presentation_identity_on`, `fiber_identity_on`, and bilateral emptiness of `directional_residuals` agree on every pair `(p, q)`.
- **`directional_residuals` (lines 55–63):** Enumerates all inhabitant pairs `(left, right)` of `DirectionalResidual D p q` (`left ∈ D`, `right ∈ D`, `p left = p right`, `q left ≠ q right`).
- **`transpose` and `internal_symmetry_breaks` (lines 66–84):** Implement `ClosureSymmetry.transpose` and `ClosureSymmetry.InternalSymmetryBreak`. For each ordered pair `pair = (x, y)` in `D × D`, `internal_symmetry_breaks` checks `transpose(pair) != pair`, `source_invariant`, and `target_broken`. In the check script, `internal_symmetry_breaks(D, p, q) == directional_residuals(D, p, q)` holds as an exact list equality on all $15 \times 15 = 225$ ordered pairs of partitions of `[0, 1, 2, 3]`, witnessing the pair-preserving bijection (`residual_to_internal_symmetry_break` and `internal_symmetry_break_to_residual`).
- **`p_q` and `joint_presentation` (lines 87–102):** Match `Compression.pQ D Q` and `PresentationRelativity.jointPresentation D p q := pQ D [p, q]`, returning `tuple(q(x) for q in questions)` when `x ∈ D` and `()` outside `D`.
- **`invariant_under_on` (lines 105–108):** Implements `ResidualClosure.InvariantUnderOn D f sigma` (`∀ x ∈ D, f (sigma x) = f x`).
- **Audit checks executed in `main()` of `u71_presentation_relativity.py` (lines 111–328):**
  1. **All 225 partition comparisons on `D = [0, 1, 2, 3]`:** Verifies `presentationIdentity_iff_fiberIdentity`, `presentationIdentity_iff_residualEmpty`, `residual_nonempty_iff_internal_symmetry_break_nonempty`, `closure_failure_iff_internal_symmetry_break`, and `common_refinement_closes_current_obstruction`.
  2. **The three concrete regime-calculus witnesses from `PresentationRelativity.lean`:**
     - `noteVariantA` vs. `noteVariantB` (`supportView` merges, `supportNotesView` separates, `kernelEval` agrees).
     - `sourcePanelWorld` vs. `extendedPanelWorld` (`coarsePanel` merges, `coarsePanel ++ [separatingEvaluator]` separates and flips `certNeg`).
     - `declaredGeneratorIndex` vs. `depthOnePresentation` on `generatorDomain = [0, 1, 2, 3, 4]` (merged at `(0, 1)` and `(1, 0)` by `declaredGeneratorIndex`, separated by `depthOnePresentation`, raising `classCount` from `4` to `5` under `jointPresentation`).
  3. **Audit counterexample 1 — multi-pair involutions (`ClosureSymmetry.md` §4 / `ResidualClosure.md` §4):** Defines `double_swap` on `[0, 1, 2, 3]` swapping `0 ↔ 1` and `2 ↔ 3` simultaneously. This is an involution moving 4 elements of `D`, showing that `InvariantUnderOn D f sigma` is broader than a single transposition, whereas `InternalSymmetryBreak` always isolates one 2-element ordered-pair orbit `{(x, y), (y, x)}` under `transpose`.
  4. **Audit counterexample 2 — closing the current obstruction does not close future comparisons (`ResidualClosure.md` §4):** On `D = [0, 1, 2]`, `p = const 0` (`classCount = 1`) and `q = (0 ↦ 0, 1 ↦ 1, 2 ↦ 1)` (`classCount = 2`) have `jointPresentation D p q` with `classCount = 2` and empty residual against `q`; yet a third presentation `r = id` (`classCount = 3`) still fails to be factored into by `jointPresentation D p q` at `(1, 2)`.
  5. **Ledger role check:** Confirms that all 46 theorem names exported by `PresentationRelativity` (32), `ClosureSymmetry` (7), and `ResidualClosure` (7) appear in `KIND_ROLE_OVERRIDES` in `code/derivation/completion.py`.

---

## Lean 4

The check script `textbook/checks/u71_lean.py` elaborates concrete witnesses and theorems against `Derivation.PresentationRelativity`, `Derivation.ClosureSymmetry`, and `Derivation.ResidualClosure` and verifies their `#print axioms` reports:

```lean
import Derivation.PresentationRelativity
import Derivation.ClosureSymmetry
import Derivation.ResidualClosure

namespace Textbook.U71

open Derivation
open Derivation.Compression
open Derivation.PresentationRelativity
open Derivation.ClosureSymmetry
open Derivation.ResidualClosure

abbrev D3 : List (Fin 3) := [0, 1, 2]

def const0 : Fin 3 → Nat := fun _ => 0
def split01 : Fin 3 → Nat := fun x => if x = 0 then 0 else 1
def idNat : Fin 3 → Nat := fun x => x.val

-- 1. Empty domain factorization is vacuous
theorem factorsOn_nil (p : Fin 3 → Nat) (q : Fin 3 → Bool) :
    FactorsOn ([] : List (Fin 3)) p q := by
  intro x hx
  cases hx

-- 2. Concrete DirectionalResidual between const0 and idNat on D3
def res01 : DirectionalResidual D3 const0 idNat where
  left := 0
  right := 1
  left_mem := by decide
  right_mem := by decide
  identified_by_source := rfl
  separated_by_target := by decide

theorem const0_id_not_identical :
    ¬ PresentationIdentityOn D3 const0 idNat :=
  directionalResidual_refutes_identity res01

theorem const0_id_not_factors :
    ¬ FactorsOn D3 const0 idNat := by
  intro h
  exact res01.separated_by_target (h 0 res01.left_mem 1 res01.right_mem res01.identified_by_source)

-- 3. Class counts and joint presentation strict increase on D3
theorem const0_id_counts :
    classCount D3 const0 = 1 ∧
    classCount D3 (jointPresentation D3 const0 idNat) = 3 := by
  decide

theorem const0_id_joint_strict :
    FactorsOn D3 (jointPresentation D3 const0 idNat) const0 ∧
    FactorsOn D3 (jointPresentation D3 const0 idNat) idNat ∧
    classCount D3 const0 < classCount D3 (jointPresentation D3 const0 idNat) :=
  jointPresentation_strict_of_factorization_failure const0_id_not_factors

-- 4. Round-trip between DirectionalResidual and InternalSymmetryBreak
def break01 : InternalSymmetryBreak D3 const0 idNat :=
  residual_to_internal_symmetry_break res01

theorem break01_swaps :
    ClosureSymmetry.transpose break01.pair = (1, 0) ∧
    ClosureSymmetry.transpose (ClosureSymmetry.transpose break01.pair) = break01.pair := by
  refine ⟨rfl, ClosureSymmetry.transpose_involutive break01.pair⟩

-- 5. Multi-pair involution on Fin 4 (Audit note: InvariantUnderOn allows multi-pair swaps)
def doubleSwap (x : Fin 4) : Fin 4 :=
  match x with
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨0, by decide⟩
  | ⟨2, _⟩ => ⟨3, by decide⟩
  | ⟨3, _⟩ => ⟨2, by decide⟩

theorem doubleSwap_involutive (x : Fin 4) :
    doubleSwap (doubleSwap x) = x := by
  fin_cases x <;> rfl

theorem doubleSwap_moves_four :
    doubleSwap 0 ≠ 0 ∧ doubleSwap 1 ≠ 1 ∧ doubleSwap 2 ≠ 2 ∧ doubleSwap 3 ≠ 3 := by
  decide

-- 6. ResidualClosure closes the current obstruction (const0 vs idNat),
--    and closing (const0 vs split01) does NOT close the next comparison against idNat.
theorem const0_id_closed :
    FactorsOn D3 (jointPresentation D3 const0 idNat) const0 ∧
    FactorsOn D3 (jointPresentation D3 const0 idNat) idNat ∧
    classCount D3 const0 < classCount D3 (jointPresentation D3 const0 idNat) ∧
    ResidualEmptyOn D3 (jointPresentation D3 const0 idNat) idNat ∧
    ¬ Nonempty (InternalSymmetryBreak D3 (jointPresentation D3 const0 idNat) idNat) :=
  common_refinement_closes_current_obstruction const0_id_not_factors

theorem closed_current_not_future :
    ResidualEmptyOn D3 (jointPresentation D3 const0 split01) split01 ∧
    ¬ FactorsOn D3 (jointPresentation D3 const0 split01) idNat := by
  refine ⟨current_directional_residual_is_empty (D := D3) (p := const0) (q := split01), ?_⟩
  intro h
  have h12 : jointPresentation D3 const0 split01 1 = jointPresentation D3 const0 split01 2 := by
    decide
  have hid : idNat 1 = idNat 2 := h 1 (by decide) 2 (by decide) h12
  revert hid
  decide

end Textbook.U71
```

---

## Line-by-line Lean explanation

- **`D3`, `const0`, `split01`, `idNat` (lines 12–16):** Declare the 3-element domain `[0, 1, 2] : List (Fin 3)` and three `Nat`-valued presentations: `const0` (1 fiber `{0, 1, 2}`), `split01` (2 fibers `{0}` and `{1, 2}`), and `idNat` (3 singleton fibers `{0}`, `{1}`, `{2}`).
- **`factorsOn_nil` (lines 19–22):** Shows that `FactorsOn [] p q` holds vacuously for any `p` and `q` by `cases hx` on `x ∈ []`. This witnesses the domain-dependence limitation noted in `PresentationRelativity.md` §4: all fiber and residual statements in these three modules are relative to the explicit finite list `D`, and are vacuous when `D = []`.
- **`res01`, `const0_id_not_identical`, `const0_id_not_factors` (lines 25–41):** Construct a concrete `DirectionalResidual D3 const0 idNat` with `left := 0` and `right := 1`, and apply `directionalResidual_refutes_identity` to refute `PresentationIdentityOn D3 const0 idNat` and `FactorsOn D3 const0 idNat`.
- **`const0_id_counts` and `const0_id_joint_strict` (lines 44–53):** Compute `classCount D3 const0 = 1` and `classCount D3 (jointPresentation D3 const0 idNat) = 3` by `decide`, and invoke `jointPresentation_strict_of_factorization_failure` to obtain both factorizations and the strict inequality `classCount D3 const0 < classCount D3 (jointPresentation D3 const0 idNat)`.
- **`break01` and `break01_swaps` (lines 56–62):** Apply `residual_to_internal_symmetry_break` to `res01`, obtaining `break01 : InternalSymmetryBreak D3 const0 idNat` on the pair `(0, 1)`, and verify both `transpose break01.pair = (1, 0)` and `transpose (transpose break01.pair) = break01.pair`.
- **`doubleSwap`, `doubleSwap_involutive`, `doubleSwap_moves_four` (lines 65–79):** Formalize the audit observation (`ClosureSymmetry.md` §4, `ResidualClosure.md` §4) that a domain transformation `sigma : X → X` on `Fin 4` can be a fixed-point-free involution moving all 4 elements (`0 ↔ 1` and `2 ↔ 3` at once), whereas `ClosureSymmetry.transpose` acts on `X × X` and isolates a single 2-element ordered-pair orbit `{(x, y), (y, x)}`. Notice that `doubleSwap_involutive` is proved by `fin_cases x <;> rfl` and is completely axiom-free (`none`).
- **`const0_id_closed` and `closed_current_not_future` (lines 83–99):** `const0_id_closed` applies `common_refinement_closes_current_obstruction` to `const0_id_not_factors`. Then `closed_current_not_future` establishes in Lean that while `jointPresentation D3 const0 split01` has empty directional residual against `split01` (`ResidualEmptyOn D3 (jointPresentation D3 const0 split01) split01`), it still fails to factor through `idNat` because it merges `1` and `2` (`jointPresentation D3 const0 split01 1 = [0, 1] = jointPresentation D3 const0 split01 2`) while `idNat 1 ≠ idNat 2`.

---

## What has been proved

Across `PresentationRelativity.lean` (32 theorems), `ClosureSymmetry.lean` (7 theorems), and `ResidualClosure.lean` (7 theorems) — all 46 audited in `artifacts/lean_axioms.txt` (lines 1288–1333) within `{propext, Quot.sound}`:

| Module | Theorems | Axiom footprint in `artifacts/lean_axioms.txt` | Core established statements |
| :--- | :---: | :--- | :--- |
| `PresentationRelativity` | 32 | 5 axiom-free (`none`), 3 `[propext]`, 13 `[Quot.sound]`, 11 `[propext, Quot.sound]` | `presentationIdentity_iff_fiberIdentity`, `presentationIdentity_iff_residualEmpty`, `presentationIdentity_equivalence`, `classCount_lt_of_refinement_split`, `forced_split_of_factorization_failure`, `jointPresentation_strict_of_factorization_failure`, `Metatheory.attempted_absolute_identification_collapses_to_equality`, `Metatheory.attempted_absolute_polarities_are_refuted`, plus the 3 concrete witnesses on `World`, `AdmissibilityPanel`, and `Fin 5` |
| `ClosureSymmetry` | 7 | 5 `[propext]`, 1 `[Quot.sound]`, 1 `[propext, Quot.sound]` | `transpose_left`, `transpose_right`, `transpose_fixed`, `transpose_involutive`, `residual_nonempty_iff_internal_symmetry_break_nonempty`, `residual_refutes_factorization`, `closure_failure_iff_internal_symmetry_break` |
| `ResidualClosure` | 7 | 3 `[Quot.sound]`, 4 `[propext, Quot.sound]` | `factorization_preserves_invariance`, `carrying_right_face_loses_generating_invariance`, `carrying_right_face_splits_generating_pair`, `common_refinement_strictly_splits_left_face`, `current_directional_residual_is_empty`, `current_internal_symmetry_break_is_empty`, `common_refinement_closes_current_obstruction` |

1. **What it supports:**
   - Presentation identity on a finite domain list `D` (`FactorsOn D p q ∧ FactorsOn D q p`) is equivalent both to pointwise fiber agreement (`FiberIdentityOn D p q`) and to bilateral emptiness of `DirectionalResidual` (`presentationIdentity_iff_residualEmpty`).
   - Any failure of `FactorsOn D p q` produces an explicit inhabitant of `DirectionalResidual D p q`, an equivalent inhabitant of `InternalSymmetryBreak D p q` on the same ordered pair `(x, y)`, and a strict increase in occupied fiber count `classCount D p < classCount D (jointPresentation D p q)`.
   - Passing to `jointPresentation D p q` empties the directional residual and internal symmetry break against `q` while losing invariance under any `D`-preserving map `sigma` that fails to preserve `q`.
2. **What it does not support:**
   - It does not establish domain-independent equivalence: every statement is relative to an explicit finite list `D : List X` and holds vacuously when `D = []` (as shown by `Textbook.U71.factorsOn_nil`).
   - It does not establish a multi-step termination theorem or a global fixpoint closure across an open-ended family of future presentations: `common_refinement_closes_current_obstruction` closes only the comparison `(jointPresentation D p q) → q` (as shown by `Textbook.U71.closed_current_not_future`).
   - It does not force every domain-level symmetry `sigma : X → X` in `InvariantUnderOn D f sigma` to be a single 2-cycle: `ClosureSymmetry.transpose` acts on ordered pairs `X × X`, whereas `InvariantUnderOn` accepts any `sigma : X → X`, including multi-pair involutions such as `Textbook.U71.doubleSwap` or non-involutive maps.
3. **The narrowest defensible claim:**
   - On any finite list `D : List X` with decidable equality on `X` and codomains, mutual factorization `PresentationIdentityOn D p q`, fiber agreement `FiberIdentityOn D p q`, and bilateral emptiness of `DirectionalResidual` are equivalent; and any failure `¬ FactorsOn D p q` yields an ordered-pair witness `DirectionalResidual D p q` (equivalently `InternalSymmetryBreak D p q`) whose common refinement `jointPresentation D p q := pQ D [p, q]` strictly increases `classCount` over `p` and has empty directional residual against `q`.
4. **The next test needed:**
   - Move from comparing two presentations `p : X → P` and `q : X → Q` over a shared base list `D : List X` to translating directly between two presentation codomains `P` and `Q` via partial or total translation maps (`PresentationDescent`, `QuotientRetention`, `FidelityClosure`, `NoOutsideFidelity`, and `EndogenousFidelityGenerator` in Unit 72).

---

## What has not been proved

1. **Homogeneous codomain requirement for `jointPresentation` (`PresentationRelativity.md` §4, `ResidualClosure.md` §4).** While `FactorsOn D p q`, `PresentationIdentityOn D p q`, `DirectionalResidual D p q`, and `InternalSymmetryBreak D p q` allow `p : X → P` and `q : X → Q` to have distinct codomain types `P` and `Q`, `jointPresentation D p q := pQ D [p, q]` requires `p, q : X → P` to share a single codomain type `P` so that `[p, q] : List (X → P)` is well-typed. When `P ≠ Q` (for example `declaredGeneratorIndex : Fin 5 → Fin 4` vs. `depthOnePresentation : Fin 5 → Fin 8` in `declared_generator_index_comparison_forces_refinement`, lines 607–625), the theorem embeds both into a common carrier (`Nat`, via `Fin.val`) before forming `[p, q]`.
2. **Constructive vs. classical direction in `presentationIdentity_iff_residualEmpty` (`PresentationRelativity.md` §3).** Proving `PresentationIdentityOn D p q → ResidualEmptyOn D p q ∧ ResidualEmptyOn D q p` is constructive, but the converse (`ResidualEmptyOn D p q ∧ ResidualEmptyOn D q p → PresentationIdentityOn D p q`, lines 124–141) uses `Classical.byContradiction` to extract `q x = q y` from the absence of a `DirectionalResidual`.
3. **Single-step closure vs. multi-step tower (`ResidualClosure.md` §4).** `common_refinement_closes_current_obstruction` establishes `ResidualEmptyOn D (jointPresentation D p q) q`, which means `jointPresentation D p q` factors through `q`. It does **not** prove `ResidualEmptyOn D q (jointPresentation D p q)` (in fact, whenever `p` splits a `q`-fiber, `q` does not factor through `jointPresentation D p q`), nor does it close comparisons against a third presentation `r` (`closed_current_not_future`).
4. **Pair-level `transpose` vs. domain-level `sigma` (`ClosureSymmetry.md` §4, `ResidualClosure.md` §4).** `ClosureSymmetry.InternalSymmetryBreak` uses `transpose : X × X → X × X` on ordered pairs, which is always an involution whose off-diagonal orbits have size 2. By contrast, `ResidualClosure.InvariantUnderOn D f sigma` takes an arbitrary function `sigma : X → X` on the domain `X` (not required to be an involution or a single transposition). The connection between the two is given at a specific residual `r : DirectionalResidual D p q` by `carrying_right_face_splits_generating_pair` (`r.left ≠ r.right` in the refined presentation).

---

## Outside the system

- **Finitude and decidable equality.** `D : List X` is a finite list. `classCount_lt_of_refinement_split`, `forced_split_of_factorization_failure`, and `jointPresentation_strict_of_factorization_failure` rely on `[DecidableEq X]` and `[DecidableEq P]` both to evaluate `pQ D [p, q]` (`if x ∈ D then ... else []`) and to compute `List.eraseDup` in `classes D p`.
- **Axiom usage.** The two `Metatheory` theorems (`attempted_absolute_identification_collapses_to_equality`, `attempted_absolute_polarities_are_refuted`), `support_identifies_while_supportNotes_separates`, and `panelEquiv_antitone` are completely axiom-free (`none`). Fiber-identity and residual lemmas use `[Quot.sound]` (via `DecidableEq` / list membership plumbing), `transpose_*` and `world_eq_iff_support_eq_and_notes_eq` use `[propext]`, and the class-count / closure theorems use `[propext, Quot.sound]`. None uses `Classical.choice`.

---

## Student exercise

On `D = [0, 1, 2, 3]`, let `p(x) = x // 2` (so `p` merges `{0, 1}` into `0` and `{2, 3}` into `1`) and let `q(x) = x % 2` (so `q` merges `{0, 2}` into `0` and `{1, 3}` into `1`).

1. List all ordered pairs in `DirectionalResidual D p q` and in `DirectionalResidual D q p`.
2. Verify that `InternalSymmetryBreak D p q` has the exact same underlying pairs as `DirectionalResidual D p q`.
3. Compute `[p(x), q(x)]` for each `x ∈ D` under `jointPresentation D p q`. What are `classCount D p`, `classCount D q`, and `classCount D (jointPresentation D p q)`?
4. Let `sigma(x) = x ^ 1` (swapping `0 ↔ 1` and `2 ↔ 3`). Is `p` invariant under `sigma` on `D`? Is `q` invariant under `sigma` on `D`? Is `jointPresentation D p q` invariant under `sigma` on `D`?

---

## Answer

1. **`DirectionalResidual D p q`** consists of pairs `(x, y)` with `x // 2 == y // 2` and `x % 2 != y % 2`:
   $$[(0, 1),\; (1, 0),\; (2, 3),\; (3, 2)].$$
   **`DirectionalResidual D q p`** consists of pairs `(x, y)` with `x % 2 == y % 2` and `x // 2 != y // 2`:
   $$[(0, 2),\; (2, 0),\; (1, 3),\; (3, 1)].$$
2. Every pair `(x, y)` in `DirectionalResidual D p q` has `x != y` (so `transpose(x, y) = (y, x) != (x, y)`), satisfies `p(y) == p(x)` (`source_invariant`), and fails `q(y) == q(x)` (`target_broken`). Thus `InternalSymmetryBreak D p q` has the exact same four pairs `[(0, 1), (1, 0), (2, 3), (3, 2)]`.
3. Under `jointPresentation D p q`:
   - `0 ↦ [0, 0]`, `1 ↦ [0, 1]`, `2 ↦ [1, 0]`, `3 ↦ [1, 1]`.
   - `classCount D p = 2`, `classCount D q = 2`, and `classCount D (jointPresentation D p q) = 4`. Both `classCount D p < 4` and `classCount D q < 4` hold strictly, and `ResidualEmptyOn D (jointPresentation D p q) q` holds because all four fibers of `jointPresentation D p q` are singletons.
4. For `sigma(x) = x ^ 1`:
   - `p(sigma(x)) = (x ^ 1) // 2 = x // 2 = p(x)` for all `x ∈ D`, so `InvariantUnderOn D p sigma` is **True**.
   - `q(sigma(0)) = q(1) = 1 != 0 = q(0)`, so `InvariantUnderOn D q sigma` is **False**.
   - Because `FactorsOn D (jointPresentation D p q) q` holds (`jointPresentation_factors_right`), `carrying_right_face_loses_generating_invariance` forces `InvariantUnderOn D (jointPresentation D p q) sigma` to be **False** (`[0, 0] != [0, 1]`).

---

## Verification

Run both check scripts from the repository root:

```bash
python textbook/checks/u71_presentation_relativity.py
python textbook/checks/u71_lean.py
```

Both commands exit with status `0` and `failures: []`.
