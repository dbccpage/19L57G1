# Unit 72 — Round-Trip Coherence, Quotient Retention, and the Fidelity Closure

**Claim.** Across the five-module fidelity family (`PresentationDescent`, `QuotientRetention`, `FidelityClosure`, `NoOutsideFidelity`, and `EndogenousFidelityGenerator`), two presentation carriers `P` and `Q` connected by a totalized translation pair `u : Totalization t` admit a faithful common descent `FaithfulCommonDescent u` (injective embeddings `left : P → Carrier`, `right : Q → Carrier` satisfying the identification equations `left p = right (u.forward p)` and `right q = left (u.backward q)`) if and only if `u` is round-trip coherent (`faithful_descent_iff_round_trip_coherent`). When a relation refinement `RelationRefinement fine coarse` loses a coarse identification `coarse.r x y` (`¬ fine.r x y`), `failed_identification_retains_two_classes` retains two distinct `Quotient fine` classes over one `Quotient coarse` class and makes `collapseMap` non-injective (`collapseMap_injective_iff_reverse_refinement`). Over a `TranslationNetwork`, coherent steps generate the least equivalence relation `FidelityRel` (`fidelity_is_least_equivalence_containing_admitted_steps`) with quotient `FidelityQuotient` (`GeneratedMultiplicity`), labels descend to `FidelityQuotient` if and only if they are `FidelityRel`-invariant (`label_descends_iff_fidelity_invariant`), any nontrivial loop transport (`HolonomyResidual`) refutes global carrier descent (`holonomy_residual_refuses_faithful_network_descent`), and on `World` the operational projection `supportView` cannot be round-trip coherent with any candidate inverse because `noteVariantA` and `noteVariantB` share `support` while differing in `notes` (`no_support_inverse_faithfully_erases_index`).

---

## Question

In Unit 71, two presentations `p : X → P` and `q : X → Q` were compared by evaluating both on a shared finite list `D : List X`. What if no shared underlying substrate `D` is given ahead of time, and we instead have only attempted translations directly between presentation carriers `P` and `Q` (or across an indexed network `i : N.Index` of carriers `N.Carrier i`)? When can the presentation index be faithfully eliminated into a common carrier without erasing internal distinctions, when must distinct quotient classes be retained, and why does a single failed endomorphism at `i` not refute `i`'s self-fidelity whereas a nontrivial loop transport around `i` refutes global carrier descent?

---

## What we already possess

From previous units we already have:

- **Explicit bijections (`lean4/Derivation/PresentationNaturality.lean`, Unit 70).** `structure Bij (α β : Type)` packages `fwd : α → β`, `bwd : β → α`, `fwd_bwd : ∀ y, fwd (bwd y) = y`, and `bwd_fwd : ∀ x, bwd (fwd x) = x`, together with reflexivity (`Bij.rfl'`), symmetry (`Bij.symm`), and composition (`Bij.trans`).
- **World support vs. decorative notes (`lean4/Derivation/NoOutside.lean` and `PresentationRelativity.lean`, Units 67 and 71).** `noteVariantA` and `noteVariantB` are distinct `World` values (`noteVariantA.notes ≠ noteVariantB.notes`) with identical operational support (`supportView noteVariantA = supportView noteVariantB`), and `notes_update_kernel_results_agree` establishes that `kernelEval R w` is invariant under replacing `w.notes`.

What we do **not** yet have is:
1. A substrate-free criterion (`PresentationDescent.lean`) relating partial `TranslationAttempt P Q`, totalized `Totalization t`, two-way triangle closure `RoundTripCoherent u`, and `FaithfulCommonDescent u`.
2. A representative-free quotient retention calculus (`QuotientRetention.lean`) for `RelationRefinement fine coarse` and its induced `collapseMap : Quotient fine → Quotient coarse`.
3. A network-level closure (`FidelityClosure.lean` and `EndogenousFidelityGenerator.lean`) generating `FidelityPath`, `FidelityRel`, and `FidelityQuotient` (`GeneratedMultiplicity`), separating index-level path connectivity from carrier-level loop triviality (`HolonomyResidual` vs. `FaithfulNetworkDescent`), and characterizing when an index label `label : N.Index → Y` descends to the quotient.
4. The concrete `World` instance (`NoOutsideFidelity.lean`) proving that `supportView : World → List Rule` has no inverse that makes it round-trip coherent or faithfully erases the distinction between `World` and `List Rule`.

---

## New concept

Five modules in `lean4/Derivation/` form a single dependency spine:

```
PresentationNaturality.lean (Bij)
           │
           ▼
PresentationDescent.lean ──► QuotientRetention.lean
(TranslationAttempt,          (RelationRefinement,
 Totalization,                 collapseMap,
 RoundTripCoherent ↔           injectivity iff
 FaithfulCommonDescent)        reverse refinement)
           │                         │
           └────────────┬────────────┘
                        ▼
               FidelityClosure.lean
               (TranslationNetwork, FidelityPath,
                FidelityRel, FidelityQuotient,
                HolonomyResidual, LabelDescends)
                  │                        │
                  ▼                        ▼
       NoOutsideFidelity.lean   EndogenousFidelityGenerator.lean
       (supportView never       (AdmittedStep, least equivalence,
        round-trip coherent)     indiscreteSetoid, universalCollapse)
```

### 1. Scoped translations, round-trip coherence, and faithful common descent (`PresentationDescent.lean`)

- **Partial vs. total translations (lines 41–77).**
  - `structure TranslationAttempt (P Q : Type)` (lines 41–43) holds `forward : P → Option Q` and `backward : Q → Option P`.
  - `structure Totalization {P Q : Type} (t : TranslationAttempt P Q)` (lines 48–52) supplies `forward : P → Q`, `backward : Q → P`, and the realization proofs `forward_realizes : ∀ p, t.forward p = some (forward p)` and `backward_realizes : ∀ q, t.backward q = some (backward q)`.
  - `inductive TranslationGap {P Q : Type} (t : TranslationAttempt P Q)` (lines 55–58) has constructors `.forward p (missing : t.forward p = none)` and `.backward q (missing : t.backward q = none)`. `translation_gap_refuses_totalization` (lines 63–76, axiom `[propext]`) shows `TranslationGap t → ¬ Nonempty (Totalization t)`.
- **Round-trip coherence vs. coherence residuals (lines 83–115).**
  - `structure RoundTripCoherent (u : Totalization t) : Prop` (lines 83–87) requires `left : ∀ p, u.backward (u.forward p) = p` and `right : ∀ q, u.forward (u.backward q) = q`.
  - `inductive CoherenceResidual (u : Totalization t) : Type` (lines 90–94) records `.left p (not_closed : u.backward (u.forward p) ≠ p)` or `.right q (not_closed : u.forward (u.backward q) ≠ q)`, and `coherence_residual_refutes_round_trip` (lines 96–104, axiom-free) establishes `CoherenceResidual u → ¬ RoundTripCoherent u`.
  - `coherent_to_bij` (lines 108–115) converts `RoundTripCoherent u` directly into `Bij P Q`.
- **Faithful common descent and the audit finding on identification equations vs. coincident images (lines 121–224).**
  - `def CoincidentImages {P Q C : Type} (left : P → C) (right : Q → C) : Prop` (lines 121–123) states `(∀ p, ∃ q, left p = right q) ∧ (∀ q, ∃ p, right q = left p)`.
  - `structure FaithfulCommonDescent (u : Totalization t)` (lines 129–139, living in `Type 1` because it bundles `Carrier : Type`) packs:
    - `Carrier : Type`
    - `left : P → Carrier` and `right : Q → Carrier`
    - `left_injective : Function.Injective left` and `right_injective : Function.Injective right`
    - `forward_identified : ∀ p, left p = right (u.forward p)`
    - `backward_identified : ∀ q, right q = left (u.backward q)`
  - From those two identification equations alone, `faithful_common_descent_has_coincident_images` (lines 142–150, axiom-free) derives `CoincidentImages d.left d.right`.
  - Using injectivity and the two identification equations, `faithful_descent_to_coherent` (lines 173–189, axiom-free) establishes `FaithfulCommonDescent u → RoundTripCoherent u`:
    $$d.\mathrm{left}(u.\mathrm{backward}(u.\mathrm{forward}\;p)) = d.\mathrm{right}(u.\mathrm{forward}\;p) = d.\mathrm{left}\;p \implies u.\mathrm{backward}(u.\mathrm{forward}\;p) = p,$$
    and symmetrically for `right`. Conversely, `coherent_to_faithful_descent` (lines 155–169) uses `Carrier := P`, `left := id`, and `right := u.backward` to construct a `FaithfulCommonDescent u` from `RoundTripCoherent u`. Thus `faithful_descent_iff_round_trip_coherent` (lines 192–200, axiom-free) establishes:
    $$\mathrm{Nonempty}\;(\mathrm{FaithfulCommonDescent}\;u) \;\Longleftrightarrow\; \mathrm{RoundTripCoherent}\;u,$$
    and `incoherence_forces_index_retention` (line 208) and `residual_forces_index_retention` (line 218) states the contrapositive.
  - **Audit finding (`PresentationDescent.md` §11.1):** Two prose passages in `paper/native_derivation_completion.md` (line 498) and `paper/endogenous_generator.md` (line 252) summarized `FaithfulCommonDescent` as "injective embeddings with coincident images." In fact, injective embeddings `left` and `right` with `CoincidentImages left right` do **not** suffice to force `RoundTripCoherent u` unless they are tied to `u.forward` and `u.backward` by `forward_identified` and `backward_identified`. Counterexample on `Bool`: let `u.forward b = !b`, `u.backward b = b`, and `left = right = id`. Then `left` and `right` are injective and have coincident images (`CoincidentImages id id`), yet `u.backward (u.forward false) = true ≠ false`, so `RoundTripCoherent u` fails (verified in Lean by `Textbook.U72.flip_coincident_but_incoherent`). The claim ledger entry `CL-FIDELITY-DESCENT` in `code/derivation/completion.py` (lines 1254–1267) explicitly records this correction.

### 2. Representative-free quotient retention (`QuotientRetention.lean`)

- `structure RelationRefinement {I : Type} (fine coarse : Setoid I) : Prop` (lines 29–30) holds `relates : ∀ {x y}, fine.r x y → coarse.r x y`, with `RelationRefinement.refl` (line 32) and `RelationRefinement.trans` (line 36).
- `collapseMap (h : RelationRefinement fine coarse) : Quotient fine → Quotient coarse` (lines 45–50) lifts `Quotient.mk coarse` along `h.relates` without choosing representatives (`collapseMap_mk`, line 52), is surjective (`collapseMap_surjective`, line 59, axiom `[Quot.sound]`), and composes functorially (`collapseMap_compose`, line 135, axiom `[Quot.sound]`).
- When `coarse.r x y` holds but `¬ fine.r x y`, `failed_identification_retains_two_classes` (lines 68–79, axioms `[propext, Quot.sound]`) establishes `Quotient.mk fine x ≠ Quotient.mk fine y ∧ collapseMap h (Quotient.mk fine x) = collapseMap h (Quotient.mk fine y)`, so `collapseMap h` is not injective (`failed_identification_makes_collapse_noninjective`, line 83).
- `collapseMap_injective_iff_reverse_refinement` (lines 98–115, axioms `[propext, Quot.sound]`): `Function.Injective (collapseMap h) ↔ (∀ {x y}, coarse.r x y → fine.r x y)`.
- **Audit finding (`QuotientRetention.md` §11.1):** The docstring of `symmetry_failure_retains_multiplicity` (lines 117–130) refers to "a former exchange identification that fails after refinement," which might suggest `sigma : I → I` must be an involution (`sigma (sigma x) = x`). In the formal statement, `sigma : I → I` is an arbitrary function with no involution hypothesis — the theorem directly instantiates `failed_identification_retains_two_classes` at `y := sigma x` (verified in Lean on a 3-cycle `cycle3 : Fin 3 → Fin 3` by `Textbook.U72.cycle3_retains_multiplicity`).

### 3. Fidelity paths, loop-action residuals, and label descent (`FidelityClosure.lean`)

- **Heterogeneous translation network and generated paths (lines 43–128).**
  - `structure TranslationNetwork` (lines 43–48, living in `Type 1`) bundles `Index : Type`, `Carrier : Index → Type`, `Attempt : Index → Index → Type`, and `pair : {i j : Index} → Attempt i j → TranslationAttempt (Carrier i) (Carrier j)`.
  - `inductive FidelityPath (N : TranslationNetwork) : N.Index → N.Index → Type` (lines 54–61) is generated by `.refl i`, `.step a u h` (where `u : Totalization (N.pair a)` and `h : RoundTripCoherent u`), `.symm`, and `.trans`.
  - `FidelityPath.toBij` (lines 65–71) evaluates any `FidelityPath N i j` to a concrete carrier bijection `Bij (N.Carrier i) (N.Carrier j)`.
  - `FidelityRel N i j : Prop := Nonempty (FidelityPath N i j)` (line 75) is an equivalence relation (`fidelity_refl`, `fidelity_symm`, `fidelity_trans`, lines 78–92), packaged as `fidelitySetoid N` (line 97) with quotient `FidelityQuotient N` (line 104) and projection `classOf N i` (line 106).
  - `class_eq_iff_coherent_path` (line 109) and `no_coherent_path_retains_indices` (line 122) show `classOf N i = classOf N j ↔ FidelityRel N i j` and `NoCoherentPath N i j → classOf N i ≠ classOf N j`.
- **Scope fence on failed endomorphisms (lines 133–138).**
  - `failed_endomorphism_does_not_refute_self_fidelity` takes `{t : TranslationAttempt (N.Carrier i) (N.Carrier i)}`, `{u : Totalization t}`, and an unused argument `_ : CoherenceResidual u`, and returns `fidelity_refl N i : FidelityRel N i i`. This records a critical distinction: a single bad translation attempt from `i` to `i` does not disconnect `i` from itself in `FidelityQuotient N`, because `.refl i` is always a valid coherent path.
- **Loop-action residuals vs. global network descent (lines 143–186).**
  - Even when indices are connected by `FidelityPath`, different paths between `i` and `j` (or a closed loop `loop : FidelityPath N i i`) need not induce the same carrier bijection!
  - `LoopTrivial loop : Prop := ∀ x, loop.toBij.fwd x = x` (lines 143–145).
  - `structure HolonomyResidual (N : TranslationNetwork)` (lines 149–153) packages `index : N.Index`, `loop : FidelityPath N index index`, `point : N.Carrier index`, and `moved : loop.toBij.fwd point ≠ point`.
  - `structure FaithfulNetworkDescent (N : TranslationNetwork)` (lines 158–163, in `Type 1`) requires a single `Carrier : Type` and injective embeddings `embed i : N.Carrier i → Carrier` such that `embed j (path.toBij.fwd x) = embed i x` along every `path : FidelityPath N i j`.
  - `holonomy_residual_refuses_faithful_network_descent` (lines 167–173, axiom-free) establishes `HolonomyResidual N → ¬ Nonempty (FaithfulNetworkDescent N)`, and `faithful_network_descent_forces_trivial_loops` (lines 180–185, axiom-free) establishes `FaithfulNetworkDescent N → AllLoopsTrivial N`.
- **Label descent (lines 189–233).**
  - `label_descends_iff_fidelity_invariant` (lines 198–211, axiom `[Quot.sound]`): a label `label : N.Index → Y` factors through `classOf N : N.Index → FidelityQuotient N` (`LabelDescends label`) if and only if `∀ i j, FidelityRel N i j → label i = label j` (`LabelInvariant label`).
  - Consequently, `coherent_disagreement_refuses_label_descent` (line 215) and its `Bool` specialization `polarity_flip_is_presentation_relative` (line 227) show that any label or boolean polarity that changes across a coherent path cannot descend to `FidelityQuotient N`.

### 4. Operational no-outside witness (`NoOutsideFidelity.lean`) and least coherent generator (`EndogenousFidelityGenerator.lean`)

- **Why `supportView : World → List Rule` has no coherent inverse (`NoOutsideFidelity.lean`, lines 30–104).**
  - `support_fiber_contains_distinct_notes` (lines 30–37, axiom `[propext]`) exhibits `noteVariantA` and `noteVariantB` with `supportView noteVariantA = supportView noteVariantB ∧ noteVariantA ≠ noteVariantB`, so ` ¬ Function.Injective supportView` (`support_projection_not_injective`, line 40).
  - For any proposed inverse `inv : List Rule → World`, `supportTotalization inv` (line 53) has `CoherenceResidual` on either `noteVariantA` or `noteVariantB`, so `support_translation_never_round_trip_coherent` (line 62), `support_translation_never_faithfully_erases_index` (line 75), and `no_support_inverse_faithfully_erases_index` (line 83) all hold with axiom footprint `[propext]`, while `notes_fiber_has_no_operational_authority` (line 92, axioms `[propext, Quot.sound]`) confirms that `kernelEval` ignores `notes`.
- **Least equivalence and indiscrete ceiling (`EndogenousFidelityGenerator.lean`, lines 33–109).**
  - `AdmittedStep N i j : Prop := ∃ (a : N.Attempt i j) (u : Totalization (N.pair a)), RoundTripCoherent u` (lines 33–35).
  - `admitted_step_has_fidelity_path` (line 37, axiom-free) and `fidelity_is_least_equivalence_containing_admitted_steps` (lines 46–57, axiom-free) show that `FidelityRel N` is the least equivalence relation on `N.Index` containing `AdmittedStep N`.
  - `indiscreteSetoid I` (lines 61–66) equates all indices (`r _ _ := True`), `fidelity_refines_indiscrete` (line 70) witnesses `RelationRefinement (fidelitySetoid N) (indiscreteSetoid N.Index)`, `GeneratedMultiplicity N` (line 74) is an `abbrev` for `FidelityQuotient N`, and `universalCollapse N` (line 78) is `collapseMap (fidelity_refines_indiscrete N)`, which is surjective (`universalCollapse_surjective`, line 82) and retains distinct classes whenever `NoCoherentPath N i j` holds (`no_coherent_path_retains_multiplicity`, line 89; `generated_structure_is_failed_erasure`, line 100).

---

## Plain-language interpretation

- **Pairwise translation (`PresentationDescent`):** Two descriptions `P` and `Q` can be merged into a single faithful table (`FaithfulCommonDescent`) without losing rows from either side if and only if translating `P → Q → P` and `Q → P → Q` lands every row back on itself (`RoundTripCoherent`). Only embedding `P` and `Q` injectively into the same set of rows (`CoincidentImages`) is not enough if the embeddings ignore the translation arrows!
- **Refinement memory (`QuotientRetention`):** Whenever a finer classification splits a bin that a coarser classification merged, the canonical forgetful map `collapseMap` from fine bins to coarse bins is surjective, requires no arbitrary choice of representative, and is non-injective on the split pair.
- **Network closure and loop transport (`FidelityClosure`):** Across a whole network of descriptions, we link two nodes `i` and `j` when a chain of round-trip coherent translations connects them (`FidelityPath`). A broken self-map at `i` does not un-link `i` from itself (because doing nothing, `.refl i`, is coherent). However, if following a closed cycle of coherent translations around `i` permutes the elements inside `N.Carrier i` (`HolonomyResidual`), then no single global carrier can embed all node carriers compatibly along every path (`¬ Nonempty (FaithfulNetworkDescent N)`).

---

## Pseudocode

```text
FUNCTION faithful_common_descent(P, Q, pair, left, right):
    IF NOT is_injective(P, left) OR NOT is_injective(Q, right):
        RETURN False
    FOR EACH p IN P:
        IF left(p) != right(pair.forward(p)):
            RETURN False
    FOR EACH q IN Q:
        IF right(q) != left(pair.backward(q)):
            RETURN False
    RETURN True

FUNCTION fidelity_rel(network, i, j):
    # Breadth-first search over steps (u, v) that totalize and are round-trip coherent
    visited = {i}
    queue = [i]
    WHILE queue NOT EMPTY:
        curr = POP_LEFT(queue)
        IF curr == j:
            RETURN True
        FOR EACH nxt IN network.indices:
            IF nxt NOT IN visited AND (step_coherent(curr, nxt) OR step_coherent(nxt, curr)):
                ADD nxt TO visited
                APPEND nxt TO queue
    RETURN False
```

---

## Python

The standalone check script `textbook/checks/u72_fidelity_closure.py` implements partial and totalized translations, round-trip coherence, faithful common descent, the `CoincidentImages` vs. identification-equation counterexample on `Bool`, quotient collapse maps, the non-involutive 3-cycle witness for `symmetry_failure_retains_multiplicity`, a 3-node translation network with an incoherent self-map, a nontrivial loop-action witness, `NoOutsideFidelity` on `World` pairs, and the `KIND_ROLE_OVERRIDES` check for all 39 theorems:

```python
@dataclass(frozen=True)
class TranslationAttempt(Generic[P, Q]):
    forward: Callable[[P], Q | None]
    backward: Callable[[Q], P | None]


@dataclass(frozen=True)
class TranslationPair(Generic[P, Q]):
    forward: Callable[[P], Q]
    backward: Callable[[Q], P]


def round_trip_coherent(
    p_carrier: list[P], q_carrier: list[Q], pair: TranslationPair[P, Q]
) -> bool:
    return all(pair.backward(pair.forward(p)) == p for p in p_carrier) and all(
        pair.forward(pair.backward(q)) == q for q in q_carrier
    )


def coincident_images(
    p_carrier: list[P],
    q_carrier: list[Q],
    left: Callable[[P], C],
    right: Callable[[Q], C],
) -> bool:
    return {left(p) for p in p_carrier} == {right(q) for q in q_carrier}


def faithful_common_descent(
    p_carrier: list[P],
    q_carrier: list[Q],
    pair: TranslationPair[P, Q],
    left: Callable[[P], C],
    right: Callable[[Q], C],
) -> bool:
    return (
        is_injective(p_carrier, left)
        and is_injective(q_carrier, right)
        and all(left(p) == right(pair.forward(p)) for p in p_carrier)
        and all(right(q) == left(pair.backward(q)) for q in q_carrier)
    )
```

---

## Line-by-line Python explanation

- **`TranslationAttempt` and `TranslationPair` (lines 22–31 of `u72_fidelity_closure.py`):** Model `PresentationDescent.TranslationAttempt` (`Option`-valued partial arrows) and `Totalization` (total arrows realizing the partial attempt).
- **`translation_gaps` and `totalizes` (lines 34–55):** Check that any `None` value produces a `TranslationGap` (`missingForward` or `missingBackward`) and prevents totalization across all $2^4 = 16$ total `Bool → Bool` pairs.
- **`round_trip_coherent` and `coherence_residuals` (lines 58–75):** Check the two triangle equations `backward(forward(p)) == p` and `forward(backward(q)) == q`. Out of the 16 total `Bool → Bool` pairs, only the 2 bijections (identity and negation) have empty `coherence_residuals`.
- **`coincident_images` vs. `faithful_common_descent` (lines 83–105 and 245–261):** Directly tests Audit Finding §11.1 of `PresentationDescent.md`. For `incoherent_pair = (forward: not, backward: id)` and `left = right = id` on `[False, True]`, `is_injective` and `coincident_images` both return `True`, whereas `round_trip_coherent` and `faithful_common_descent` both return `False` because `id(False) != id(not False)`.
- **`relation_refines`, `quotient_classes`, `collapse_map` (lines 108–143 and 263–285):** Implement `QuotientRetention.RelationRefinement` and `collapseMap`, verifying functoriality `collapseMap (hfm.trans hmc) = collapseMap hmc ∘ collapseMap hfm` on `r_id → r_mod2 → r_all` and testing `symmetry_failure_retains_multiplicity` on the non-involutive 3-cycle `sigma_3cycle(x) = (x + 1) % 3` (`QuotientRetention.md` §11.1).
- **`FiniteTranslationNetwork` (lines 146–182 and 287–336):** Implements `FidelityClosure` and `EndogenousFidelityGenerator` on a 3-node network `{0, 1, 2}`:
  - Node `0` has an incoherent endomorphism `(0, 0) ↦ collapse_pair`, confirming `failed_endomorphism_does_not_refute_self_fidelity` (`net.fidelity_rel(0, 0)` is `True`).
  - Nodes `0` and `1` are linked by `id_pair` (`0 → 1`) and `swap_pair` (`1 → 0`), producing a closed loop `0 → 1 → 0` whose composed bijection swaps `0` and `1` (`loop_fn(0) == 1 != 0`, a concrete `HolonomyResidual`).
  - Node `2` has no coherent path to `{0, 1}`, so `GeneratedMultiplicity` has 2 classes (`{0, 1}` and `{2}`) that collapse to 1 class (`{0, 1, 2}`) under `universalCollapse`.
- **`NoOutsideFidelity` and `EXPECTED_THEOREMS` (lines 338–355):** Verify that no candidate inverse makes `support_proj` round-trip coherent on `w_a = ((1, 2), (10,))` and `w_b = ((1, 2), (20,))`, and check that all 39 qualified theorem names appear in `KIND_ROLE_OVERRIDES`.

---

## Lean 4

The check script `textbook/checks/u72_lean.py` kernel-checks concrete witnesses and audit counterexamples across all five modules:

```lean
import Derivation.PresentationDescent
import Derivation.QuotientRetention
import Derivation.FidelityClosure
import Derivation.NoOutsideFidelity
import Derivation.EndogenousFidelityGenerator

namespace Textbook.U72

open PresentationDescent
open QuotientRetention
open FidelityClosure
open NoOutsideFidelity
open EndogenousFidelityGenerator

-- 1. Concrete TranslationGap on Bool
def partialAttempt : TranslationAttempt Bool Bool where
  forward b := if b then none else some false
  backward b := some b

def gapTrue : TranslationGap partialAttempt :=
  TranslationGap.forward true rfl

theorem partialAttempt_no_totalization :
    ¬ Nonempty (Totalization partialAttempt) :=
  translation_gap_refuses_totalization gapTrue

-- 2. Audit finding (PresentationDescent.md §11.1):
--    Injective embeddings with CoincidentImages on Bool that fail RoundTripCoherent
--    because the identification equation left p = right (u.forward p) fails.
def flipAttempt : TranslationAttempt Bool Bool where
  forward b := some (!b)
  backward b := some b

def flipTotal : Totalization flipAttempt where
  forward b := !b
  backward b := b
  forward_realizes _ := rfl
  backward_realizes _ := rfl

def flipResidual : CoherenceResidual flipTotal :=
  CoherenceResidual.left false (by decide)

theorem flip_coincident_but_incoherent :
    Function.Injective (id : Bool → Bool) ∧
    CoincidentImages (id : Bool → Bool) (id : Bool → Bool) ∧
    ¬ RoundTripCoherent flipTotal ∧
    ¬ Nonempty (FaithfulCommonDescent flipTotal) := by
  refine ⟨Function.injective_id, ?_, coherence_residual_refutes_round_trip flipResidual,
    residual_forces_index_retention flipResidual⟩
  exact ⟨fun p => ⟨p, rfl⟩, fun q => ⟨q, rfl⟩⟩

-- 3. Audit finding (QuotientRetention.md §11.1):
--    symmetry_failure_retains_multiplicity applies to a non-involutive 3-cycle on Fin 3.
def eqSetoid (α : Type) : Setoid α where
  r x y := x = y
  iseqv := ⟨fun _ => rfl, fun h => h.symm, fun h1 h2 => h1.trans h2⟩

theorem eqRefinesIndiscrete : RelationRefinement (eqSetoid (Fin 3)) (indiscreteSetoid (Fin 3)) :=
  ⟨fun _ => True.intro⟩

def cycle3 (x : Fin 3) : Fin 3 :=
  match x with
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨2, by decide⟩
  | ⟨2, _⟩ => ⟨0, by decide⟩

theorem cycle3_not_involutive : cycle3 (cycle3 0) ≠ 0 := by
  decide

theorem cycle3_retains_multiplicity :
    ∃ a b : Quotient (eqSetoid (Fin 3)),
      a ≠ b ∧ collapseMap eqRefinesIndiscrete a = collapseMap eqRefinesIndiscrete b :=
  symmetry_failure_retains_multiplicity eqRefinesIndiscrete cycle3 0 True.intro
    (by intro h; cases h)

-- 4. Concrete loop network with nontrivial loop action (HolonomyResidual)
def swapAttempt : TranslationAttempt Bool Bool where
  forward b := some (!b)
  backward b := some (!b)

def swapTotal : Totalization swapAttempt where
  forward b := !b
  backward b := !b
  forward_realizes _ := rfl
  backward_realizes _ := rfl

theorem swap_coherent : RoundTripCoherent swapTotal where
  left b := by cases b <;> rfl
  right b := by cases b <;> rfl

def loopNet : TranslationNetwork where
  Index := Unit
  Carrier _ := Bool
  Attempt _ _ := Unit
  pair _ := swapAttempt

def swapLoop : FidelityPath loopNet () () :=
  FidelityPath.step () swapTotal swap_coherent

def swapLoopResidual : HolonomyResidual loopNet where
  index := ()
  loop := swapLoop
  point := false
  moved := by intro h; cases h

theorem loopNet_no_faithful_descent :
    ¬ Nonempty (FaithfulNetworkDescent loopNet) :=
  holonomy_residual_refuses_faithful_network_descent swapLoopResidual

-- 5. Audit finding (EndogenousFidelityGenerator.md §4):
--    universalCollapse identifies every pair of classes by True.intro, even for
--    FidelityRel-equivalent indices.
theorem universalCollapse_always_eq (N : TranslationNetwork) (i j : N.Index) :
    universalCollapse N (classOf N i) = universalCollapse N (classOf N j) :=
  Quotient.sound True.intro

end Textbook.U72
```

---

## Line-by-line Lean explanation

- **Namespace note (`open PresentationDescent ...`, lines 9–13):** Unlike `PresentationRelativity`, `ClosureSymmetry`, and `ResidualClosure` (which open inside `namespace Derivation`), the five Unit 72 modules declare top-level namespaces `PresentationDescent`, `QuotientRetention`, `FidelityClosure`, `NoOutsideFidelity`, and `EndogenousFidelityGenerator`.
- **`partialAttempt`, `gapTrue`, `partialAttempt_no_totalization` (lines 16–25):** Exhibit a concrete `TranslationGap` at `true` (`forward true = none`) and apply `translation_gap_refuses_totalization` to refute `Nonempty (Totalization partialAttempt)`.
- **`flipAttempt`, `flipTotal`, `flipResidual`, `flip_coincident_but_incoherent` (lines 30–50):** Formalize Audit Finding §11.1 of `PresentationDescent.md` without using any axioms (`none`): `id : Bool → Bool` is injective and `CoincidentImages id id` holds, yet `flipTotal` (`forward b = !b`, `backward b = b`) has `flipResidual : CoherenceResidual flipTotal` at `false` and therefore fails both `RoundTripCoherent flipTotal` and `Nonempty (FaithfulCommonDescent flipTotal)`.
- **`eqSetoid`, `eqRefinesIndiscrete`, `cycle3`, `cycle3_not_involutive`, `cycle3_retains_multiplicity` (lines 54–74):** Formalize Audit Finding §11.1 of `QuotientRetention.md`: `cycle3` on `Fin 3` is a 3-cycle (`cycle3 (cycle3 0) = 2 ≠ 0`, not an involution), yet `symmetry_failure_retains_multiplicity` applies directly to `cycle3` at `0`.
- **`swapAttempt` .. `loopNet_no_faithful_descent` (lines 77–108):** Construct a concrete 1-node `TranslationNetwork` (`Index := Unit`, `Carrier _ := Bool`) whose single admitted step `swapLoop` negates `Bool`. Because `swapLoop` is round-trip coherent (`!(!b) = b`), `FidelityRel loopNet () ()` holds; yet `swapLoop.toBij.fwd false = true ≠ false`, giving `swapLoopResidual : HolonomyResidual loopNet` and proving `¬ Nonempty (FaithfulNetworkDescent loopNet)` axiom-free (`none`).
- **`universalCollapse_always_eq` (lines 112–114):** Formalizes Audit Finding §4 of `EndogenousFidelityGenerator.md`: the second conjunct `universalCollapse N (classOf N i) = universalCollapse N (classOf N j)` of `no_coherent_path_retains_multiplicity` holds for **all** `i, j : N.Index` (even when `i = j` or `FidelityRel N i j`) by `Quotient.sound True.intro`, because `indiscreteSetoid N.Index` relates every pair by `True`.

---

## What has been proved

Across the five modules, 39 theorems are exported and audited in `artifacts/lean_axioms.txt` (lines 1334–1372):

| Module | Theorems | Axiom footprint in `artifacts/lean_axioms.txt` | Core established statements |
| :--- | :---: | :--- | :--- |
| `PresentationDescent` | 7 | 6 axiom-free (`none`), 1 `[propext]` | `translation_gap_refuses_totalization`, `coherence_residual_refutes_round_trip`, `faithful_common_descent_has_coincident_images`, `faithful_descent_to_coherent`, `faithful_descent_iff_round_trip_coherent`, `incoherence_forces_index_retention`, `residual_forces_index_retention` |
| `QuotientRetention` | 9 | 3 axiom-free (`none`), 3 `[Quot.sound]`, 3 `[propext, Quot.sound]` | `RelationRefinement.refl`/`.trans`, `collapseMap_mk`, `collapseMap_surjective`, `failed_identification_retains_two_classes`, `failed_identification_makes_collapse_noninjective`, `collapseMap_injective_iff_reverse_refinement`, `symmetry_failure_retains_multiplicity`, `collapseMap_compose` |
| `FidelityClosure` | 11 | 6 axiom-free (`none`), 3 `[Quot.sound]`, 2 `[propext, Quot.sound]` | `fidelity_refl`/`_symm`/`_trans`, `class_eq_iff_coherent_path`, `no_coherent_path_retains_indices`, `failed_endomorphism_does_not_refute_self_fidelity`, `holonomy_residual_refuses_faithful_network_descent`, `faithful_network_descent_forces_trivial_loops`, `label_descends_iff_fidelity_invariant`, `coherent_disagreement_refuses_label_descent`, `polarity_flip_is_presentation_relative` |
| `NoOutsideFidelity` | 6 | 5 `[propext]`, 1 `[propext, Quot.sound]` | `support_fiber_contains_distinct_notes`, `support_projection_not_injective`, `support_translation_never_round_trip_coherent`, `support_translation_never_faithfully_erases_index`, `no_support_inverse_faithfully_erases_index`, `notes_fiber_has_no_operational_authority` |
| `EndogenousFidelityGenerator` | 6 | 3 axiom-free (`none`), 1 `[Quot.sound]`, 2 `[propext, Quot.sound]` | `admitted_step_has_fidelity_path`, `fidelity_is_least_equivalence_containing_admitted_steps`, `fidelity_refines_indiscrete`, `universalCollapse_surjective`, `no_coherent_path_retains_multiplicity`, `generated_structure_is_failed_erasure` |

1. **What it supports:**
   - For a fixed totalized pair `u : Totalization t`, existence of a `FaithfulCommonDescent u` is equivalent to `RoundTripCoherent u` (`faithful_descent_iff_round_trip_coherent`, axiom-free).
   - Over a `TranslationNetwork`, `FidelityRel` is the least equivalence relation containing `AdmittedStep`, labels descend to `FidelityQuotient` iff they are constant along `FidelityPath`, and any nontrivial loop bijection (`HolonomyResidual`) prevents global carrier descent (`FaithfulNetworkDescent`).
   - On `World`, `supportView` is non-injective (`noteVariantA` vs. `noteVariantB`) and therefore has no inverse making it round-trip coherent (`no_support_inverse_faithfully_erases_index`).
2. **What it does not support:**
   - It does not derive `TranslationNetwork` from `Regime` or `World`: `TranslationNetwork` is an admitted `Type 1` structure (`EndogenousFidelityGenerator.md` §4 & §11).
   - It does not prove the converse of `faithful_network_descent_forces_trivial_loops`: whether `AllLoopsTrivial N` suffices to construct a `FaithfulNetworkDescent N` is not proved in `FidelityClosure.lean` (`FidelityClosure.md` §4; constructing a quotient carrier across connected components without choosing basepoints requires quotienting the sigma type `(i : N.Index) × N.Carrier i` by path transport).
   - It does not make `CoincidentImages` alone sufficient for `RoundTripCoherent`: the identification equations `forward_identified` and `backward_identified` are essential (`PresentationDescent.md` §11.1, `Textbook.U72.flip_coincident_but_incoherent`).
3. **The narrowest defensible claim:**
   - Pairwise index elimination via `FaithfulCommonDescent u` is equivalent to `RoundTripCoherent u`; network-level index equivalence `FidelityRel N` is the least equivalence containing coherent totalized steps; labels descend to `FidelityQuotient N` iff they are `FidelityRel`-invariant; nontrivial loop transport (`HolonomyResidual`) refutes `FaithfulNetworkDescent N`; and `supportView : World → List Rule` has no round-trip coherent inverse.
4. **The next test needed:**
   - Examine what happens when a single symmetry or involution acts on a carrier without a common fixed point (`Breaking.lean`), and how relational composition behaves when no total binary composition operator is assumed (`Composing.lean`, Unit 73).

---

## What has not been proved

1. **`CoincidentImages` wording vs. identification equations (`PresentationDescent.md` §11.1).** As proved in `Textbook.U72.flip_coincident_but_incoherent`, injective embeddings with `CoincidentImages` do not imply `RoundTripCoherent` without `forward_identified` and `backward_identified` (`CL-FIDELITY-DESCENT`).
2. **Pair-dependence in `PresentationDescent` (`PresentationDescent.md` §4).** `incoherence_forces_index_retention` and `residual_forces_index_retention` refute `FaithfulCommonDescent u` for the **specific** totalization `u`; they do not rule out that a *different* translation pair `u'` between the same types `P` and `Q` could be round-trip coherent (except in `NoOutsideFidelity.no_support_inverse_faithfully_erases_index`, where `forward` is fixed to the non-injective map `supportView` and all candidate backward maps `inv` are universally refuted).
3. **`AllLoopsTrivial N → Nonempty (FaithfulNetworkDescent N)` is not proved (`FidelityClosure.md` §4).** Only the necessity direction `faithful_network_descent_forces_trivial_loops` and its contrapositive `holonomy_residual_refuses_faithful_network_descent` are proved.
4. **Definitional naming in `EndogenousFidelityGenerator` (`EndogenousFidelityGenerator.md` §4 & §11).** `GeneratedMultiplicity N` is an `abbrev` for `FidelityQuotient N`, "endogenous" means relative to a supplied `N : TranslationNetwork`, and the second conjunct of `no_coherent_path_retains_multiplicity` (`universalCollapse N (classOf N i) = universalCollapse N (classOf N j)`) holds trivially by `Quotient.sound True.intro` for every pair `(i, j)` (`Textbook.U72.universalCollapse_always_eq`).

---

## Outside the system

- **Universe level `Type 1`.** Because `FaithfulCommonDescent`, `TranslationNetwork`, and `FaithfulNetworkDescent` bundle carrier types (`Carrier : Type`, `Index : Type`), they inhabit `Type 1` rather than `Type` (`PresentationDescent.md` §3, `FidelityClosure.md` §3).
- **Axiom usage.** All of `PresentationDescent` except `translation_gap_refuses_totalization` (which uses `simp` on `Option` equality and records `[propext]`) is completely axiom-free (`none`), as are `fidelity_refl`/`_symm`/`_trans`, `failed_endomorphism_does_not_refute_self_fidelity`, `holonomy_residual_refuses_faithful_network_descent`, `faithful_network_descent_forces_trivial_loops`, `admitted_step_has_fidelity_path`, `fidelity_is_least_equivalence_containing_admitted_steps`, and `fidelity_refines_indiscrete`. Quotient lifting and exactness in `QuotientRetention`, `FidelityClosure`, and `EndogenousFidelityGenerator` use `[Quot.sound]` or `[propext, Quot.sound]`. None uses `Classical.choice`.

---

## Student exercise

Consider a 2-index translation network `N` with `N.Index = {0, 1}`, `N.Carrier 0 = {0, 1, 2}`, and `N.Carrier 1 = {0, 1, 2}`. Suppose there are two admitted coherent steps from `0` to `1`:
- Step `a` has `forward(x) = x` and `backward(y) = y`.
- Step `b` has `forward(x) = (x + 1) % 3` and `backward(y) = (y - 1) % 3`.

1. Verify that both steps `a` and `b` are `RoundTripCoherent`.
2. How many equivalence classes does `FidelityQuotient N` (`GeneratedMultiplicity N`) have?
3. Construct a closed loop `loop : FidelityPath N 0 0` by following `b` forward (`0 → 1`) and `a.symm` backward (`1 → 0`). What is `loop.toBij.fwd(0)`?
4. Does `N` admit a `FaithfulNetworkDescent N`? Why or why not?

---

## Answer

1. For step `a`, `backward(forward(x)) = x` and `forward(backward(y)) = y` hold for all `x, y ∈ {0, 1, 2}`. For step `b`, `((x + 1) - 1) % 3 = x` and `((y - 1) + 1) % 3 = y` hold for all `x, y ∈ {0, 1, 2}`. Thus both steps are `RoundTripCoherent`.
2. Because step `a` (or `b`) connects index `0` to index `1`, `FidelityRel N 0 1` holds and `FidelityQuotient N` has **1** equivalence class `{0, 1}`.
3. Following `b` from `0` to `1` sends `0 ↦ (0 + 1) % 3 = 1`, and following `a.symm` from `1` to `0` applies `a.backward`, sending `1 ↦ 1`. Thus `loop.toBij.fwd(0) = 1 != 0`.
4. **No.** The triple `(index := 0, loop := b.trans a.symm, point := 0)` is a `HolonomyResidual N` (`loop.toBij.fwd(0) = 1 != 0`). By `holonomy_residual_refuses_faithful_network_descent`, any `FaithfulNetworkDescent N` would have to satisfy `embed 0 (loop.toBij.fwd 0) = embed 0 0`, forcing `embed 0 1 = embed 0 0` and violating `embed_injective 0`. Even though the index quotient `FidelityQuotient N` has 1 class, global carrier descent is refuted (`¬ Nonempty (FaithfulNetworkDescent N)`).

---

## Verification

Run both check scripts from the repository root:

```bash
python textbook/checks/u72_fidelity_closure.py
python textbook/checks/u72_lean.py
```

Both commands exit with status `0` and `failures: []`.
