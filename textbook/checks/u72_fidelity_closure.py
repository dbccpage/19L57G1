from __future__ import annotations

import json
import pathlib
import sys
from collections import deque
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.completion import KIND_ROLE_OVERRIDES  # noqa: E402

P = TypeVar("P")
Q = TypeVar("Q")
C = TypeVar("C")
I = TypeVar("I")
L = TypeVar("L")


@dataclass(frozen=True)
class TranslationAttempt(Generic[P, Q]):
    forward: Callable[[P], Q | None]
    backward: Callable[[Q], P | None]


@dataclass(frozen=True)
class TranslationPair(Generic[P, Q]):
    forward: Callable[[P], Q]
    backward: Callable[[Q], P]


def translation_gaps(
    p_carrier: list[P], q_carrier: list[Q], attempt: TranslationAttempt[P, Q]
) -> list[tuple[str, object]]:
    gaps: list[tuple[str, object]] = []
    for p in p_carrier:
        if attempt.forward(p) is None:
            gaps.append(("missingForward", p))
    for q in q_carrier:
        if attempt.backward(q) is None:
            gaps.append(("missingBackward", q))
    return gaps


def totalizes(
    p_carrier: list[P],
    q_carrier: list[Q],
    attempt: TranslationAttempt[P, Q],
    pair: TranslationPair[P, Q],
) -> bool:
    return all(attempt.forward(p) == pair.forward(p) for p in p_carrier) and all(
        attempt.backward(q) == pair.backward(q) for q in q_carrier
    )


def round_trip_coherent(
    p_carrier: list[P], q_carrier: list[Q], pair: TranslationPair[P, Q]
) -> bool:
    return all(pair.backward(pair.forward(p)) == p for p in p_carrier) and all(
        pair.forward(pair.backward(q)) == q for q in q_carrier
    )


def coherence_residuals(
    p_carrier: list[P], q_carrier: list[Q], pair: TranslationPair[P, Q]
) -> list[tuple[str, object]]:
    residuals: list[tuple[str, object]] = []
    for p in p_carrier:
        if pair.backward(pair.forward(p)) != p:
            residuals.append(("leftFailure", p))
    for q in q_carrier:
        if pair.forward(pair.backward(q)) != q:
            residuals.append(("rightFailure", q))
    return residuals


def is_injective(carrier: list[P], fn: Callable[[P], C]) -> bool:
    seen = [fn(x) for x in carrier]
    return len(set(seen)) == len(carrier)


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


def relation_refines(
    carrier: list[I],
    r_fine: Callable[[I, I], bool],
    r_coarse: Callable[[I, I], bool],
) -> bool:
    return all(
        r_coarse(x, y)
        for x in carrier
        for y in carrier
        if r_fine(x, y)
    )


def quotient_classes(
    carrier: list[I], eq_rel: Callable[[I, I], bool]
) -> list[frozenset[I]]:
    classes_out: list[frozenset[I]] = []
    for x in carrier:
        cls = frozenset(y for y in carrier if eq_rel(x, y))
        if cls not in classes_out:
            classes_out.append(cls)
    return classes_out


def collapse_map(
    carrier: list[I],
    r_fine: Callable[[I, I], bool],
    r_coarse: Callable[[I, I], bool],
) -> dict[frozenset[I], frozenset[I]]:
    fine_classes = quotient_classes(carrier, r_fine)
    mapping: dict[frozenset[I], frozenset[I]] = {}
    for fc in fine_classes:
        rep = next(iter(fc))
        mapping[fc] = frozenset(y for y in carrier if r_coarse(rep, y))
    return mapping


@dataclass(frozen=True)
class FiniteTranslationNetwork:
    indices: list[int]
    carriers: dict[int, list[int]]
    translations: dict[tuple[int, int], TranslationPair[int, int]]
    admitted: Callable[[int, int], bool]

    def step_coherent(self, i: int, j: int) -> bool:
        return self.admitted(i, j) and round_trip_coherent(
            self.carriers[i], self.carriers[j], self.translations[(i, j)]
        )

    def fidelity_rel(self, i: int, j: int) -> bool:
        visited = {i}
        queue = deque([i])
        while queue:
            curr = queue.popleft()
            if curr == j:
                return True
            for nxt in self.indices:
                if nxt not in visited and (
                    self.step_coherent(curr, nxt) or self.step_coherent(nxt, curr)
                ):
                    visited.add(nxt)
                    queue.append(nxt)
        return False

    def compose_path(self, path: list[tuple[str, int, int]]) -> Callable[[int], int]:
        def _run(x: int) -> int:
            val = x
            for direction, src, dst in path:
                if direction == "fwd":
                    val = self.translations[(src, dst)].forward(val)
                else:
                    val = self.translations[(dst, src)].backward(val)
            return val

        return _run


EXPECTED_THEOREMS = [
    # PresentationDescent (7)
    "PresentationDescent.translation_gap_refuses_totalization",
    "PresentationDescent.coherence_residual_refutes_round_trip",
    "PresentationDescent.faithful_common_descent_has_coincident_images",
    "PresentationDescent.faithful_descent_to_coherent",
    "PresentationDescent.faithful_descent_iff_round_trip_coherent",
    "PresentationDescent.incoherence_forces_index_retention",
    "PresentationDescent.residual_forces_index_retention",
    # QuotientRetention (9)
    "QuotientRetention.RelationRefinement.refl",
    "QuotientRetention.RelationRefinement.trans",
    "QuotientRetention.collapseMap_mk",
    "QuotientRetention.collapseMap_surjective",
    "QuotientRetention.failed_identification_retains_two_classes",
    "QuotientRetention.failed_identification_makes_collapse_noninjective",
    "QuotientRetention.collapseMap_injective_iff_reverse_refinement",
    "QuotientRetention.symmetry_failure_retains_multiplicity",
    "QuotientRetention.collapseMap_compose",
    # FidelityClosure (11)
    "FidelityClosure.fidelity_refl",
    "FidelityClosure.fidelity_symm",
    "FidelityClosure.fidelity_trans",
    "FidelityClosure.class_eq_iff_coherent_path",
    "FidelityClosure.no_coherent_path_retains_indices",
    "FidelityClosure.failed_endomorphism_does_not_refute_self_fidelity",
    "FidelityClosure.holonomy_residual_refuses_faithful_network_descent",
    "FidelityClosure.faithful_network_descent_forces_trivial_loops",
    "FidelityClosure.label_descends_iff_fidelity_invariant",
    "FidelityClosure.coherent_disagreement_refuses_label_descent",
    "FidelityClosure.polarity_flip_is_presentation_relative",
    # NoOutsideFidelity (6)
    "NoOutsideFidelity.support_fiber_contains_distinct_notes",
    "NoOutsideFidelity.support_projection_not_injective",
    "NoOutsideFidelity.support_translation_never_round_trip_coherent",
    "NoOutsideFidelity.support_translation_never_faithfully_erases_index",
    "NoOutsideFidelity.no_support_inverse_faithfully_erases_index",
    "NoOutsideFidelity.notes_fiber_has_no_operational_authority",
    # EndogenousFidelityGenerator (6)
    "EndogenousFidelityGenerator.admitted_step_has_fidelity_path",
    "EndogenousFidelityGenerator.fidelity_is_least_equivalence_containing_admitted_steps",
    "EndogenousFidelityGenerator.fidelity_refines_indiscrete",
    "EndogenousFidelityGenerator.universalCollapse_surjective",
    "EndogenousFidelityGenerator.no_coherent_path_retains_multiplicity",
    "EndogenousFidelityGenerator.generated_structure_is_failed_erasure",
]


def main() -> int:
    failures: list[str] = []

    # 1. PresentationDescent: TranslationGap and RoundTripCoherent
    b_carrier = [False, True]
    partial_attempt: TranslationAttempt[bool, bool] = TranslationAttempt(
        forward=lambda p: None if p else False,
        backward=lambda q: q,
    )
    gaps = translation_gaps(b_carrier, b_carrier, partial_attempt)
    if gaps != [("missingForward", True)]:
        failures.append(f"unexpected translation gaps: {gaps}")
    all_bool_pairs = [
        TranslationPair(
            forward=lambda p, f0=f0, f1=f1: f1 if p else f0,
            backward=lambda q, b0=b0, b1=b1: b1 if q else b0,
        )
        for f0 in b_carrier
        for f1 in b_carrier
        for b0 in b_carrier
        for b1 in b_carrier
    ]
    if any(totalizes(b_carrier, b_carrier, partial_attempt, pair) for pair in all_bool_pairs):
        failures.append("partial attempt with gap should refuse every totalization")

    coherent_count = 0
    for pair in all_bool_pairs:
        coh = round_trip_coherent(b_carrier, b_carrier, pair)
        res = coherence_residuals(b_carrier, b_carrier, pair)
        if coh != (len(res) == 0):
            failures.append("round_trip_coherent must be equivalent to empty coherence_residuals")
        if coh:
            coherent_count += 1
            if not faithful_common_descent(b_carrier, b_carrier, pair, lambda p: p, pair.backward):
                failures.append("coherent_to_faithful_descent failed on coherent pair")
    if coherent_count != 2:
        failures.append(f"expected 2 coherent Bool bijections, got {coherent_count}")

    # 2. Audit finding (PresentationDescent.md §11.1):
    # CoincidentImages + injective embeddings WITHOUT the identification equations
    # does NOT force RoundTripCoherent.
    incoherent_pair = TranslationPair[bool, bool](
        forward=lambda b: not b,
        backward=lambda b: b,
    )
    id_embed = lambda b: b
    if not (
        is_injective(b_carrier, id_embed)
        and is_injective(b_carrier, id_embed)
        and coincident_images(b_carrier, b_carrier, id_embed, id_embed)
    ):
        failures.append("audit counterexample setup failed: embeddings should be injective with coincident images")
    if round_trip_coherent(b_carrier, b_carrier, incoherent_pair):
        failures.append("incoherent_pair must fail round_trip_coherent")
    if faithful_common_descent(b_carrier, b_carrier, incoherent_pair, id_embed, id_embed):
        failures.append("faithful_common_descent must reject incoherent_pair via identification equations")

    # 3. QuotientRetention: RelationRefinement, collapseMap, non-involutive sigma
    dom4 = [0, 1, 2, 3]
    r_id = lambda x, y: x == y
    r_mod2 = lambda x, y: (x % 2) == (y % 2)
    r_all = lambda x, y: True

    if not (relation_refines(dom4, r_id, r_mod2) and relation_refines(dom4, r_mod2, r_all)):
        failures.append("RelationRefinement chain r_id -> r_mod2 -> r_all failed")
    cmap_id_mod2 = collapse_map(dom4, r_id, r_mod2)
    cmap_mod2_all = collapse_map(dom4, r_mod2, r_all)
    cmap_id_all = collapse_map(dom4, r_id, r_all)
    for fc, cc in cmap_id_all.items():
        if cmap_mod2_all[cmap_id_mod2[fc]] != cc:
            failures.append("collapseMap_compose failed on r_id -> r_mod2 -> r_all")
    if len(set(cmap_id_mod2.values())) == len(cmap_id_mod2):
        failures.append("failed_identification_makes_collapse_noninjective failed")

    # Audit finding (QuotientRetention.md §11.1): sigma need not be an involution
    sigma_3cycle = lambda x: (x + 1) % 3 if x < 3 else 3
    if sigma_3cycle(sigma_3cycle(0)) == 0:
        failures.append("sigma_3cycle should not be an involution")
    if not (r_all(0, sigma_3cycle(0)) and not r_id(0, sigma_3cycle(0))):
        failures.append("symmetry_failure_retains_multiplicity should apply to non-involutive sigma_3cycle")

    # 4. FidelityClosure + EndogenousFidelityGenerator
    # Network on indices {0, 1, 2} with carrier {0, 1}:
    # (0, 1) has two admitted steps in a loop test, and index 2 is isolated.
    id_pair = TranslationPair[int, int](forward=lambda x: x, backward=lambda x: x)
    swap_pair = TranslationPair[int, int](forward=lambda x: 1 - x, backward=lambda x: 1 - x)
    collapse_pair = TranslationPair[int, int](forward=lambda _: 0, backward=lambda q: q)

    net = FiniteTranslationNetwork(
        indices=[0, 1, 2],
        carriers={0: [0, 1], 1: [0, 1], 2: [0, 1]},
        translations={
            (0, 0): collapse_pair,  # incoherent endomorphism at 0
            (0, 1): id_pair,
            (1, 0): swap_pair,
            (1, 2): collapse_pair,
            (2, 1): collapse_pair,
        },
        admitted=lambda i, j: (i, j) in {(0, 1), (1, 0)},
    )
    # Scope fence: failed endomorphism at (0, 0) does NOT refute self-fidelity at 0
    if round_trip_coherent([0, 1], [0, 1], net.translations[(0, 0)]):
        failures.append("(0, 0) endomorphism should be incoherent")
    if not net.fidelity_rel(0, 0):
        failures.append("failed_endomorphism_does_not_refute_self_fidelity failed")

    # Coherent path between 0 and 1, no coherent path to 2
    if not net.fidelity_rel(0, 1):
        failures.append("0 and 1 should be connected by an admitted coherent step")
    if net.fidelity_rel(0, 2):
        failures.append("0 and 2 should have NoCoherentPath")

    # Loop-action residual along (0 -> 1 -> 0)
    loop_fn = net.compose_path([("fwd", 0, 1), ("fwd", 1, 0)])
    if loop_fn(0) == 0:
        failures.append("loop (0 -> 1 -> 0) should move point 0 (HolonomyResidual witness)")

    # Label descent and polarity flip
    # Label L(0, x) = x, L(1, x) = 1 - x is invariant along swap_pair (1 -> 0),
    # and swaps boolean polarity between presentations 0 and 1.
    label_polarity = lambda i, x: (x == 1) if i == 0 else (x == 0)
    for x in [0, 1]:
        if label_polarity(1, swap_pair.forward(x)) == label_polarity(0, x):
            pass
        else:
            failures.append("polarity flip along swap_pair failed")

    # EndogenousFidelityGenerator: GeneratedMultiplicity has 2 classes ({0, 1} and {2}),
    # while universalCollapse sends both to the single indiscrete class {0, 1, 2}.
    gen_classes = quotient_classes(net.indices, net.fidelity_rel)
    indiscrete_classes = quotient_classes(net.indices, lambda _i, _j: True)
    if len(gen_classes) != 2 or len(indiscrete_classes) != 1:
        failures.append(f"unexpected GeneratedMultiplicity / indiscrete counts: {len(gen_classes)}, {len(indiscrete_classes)}")

    # 5. NoOutsideFidelity: support projection forgets decorative notes
    # Represent World as (support_tuple, notes_tuple)
    w_a = ((1, 2), (10,))
    w_b = ((1, 2), (20,))
    support_proj = lambda w: w[0]
    if support_proj(w_a) != support_proj(w_b) or w_a == w_b:
        failures.append("support_fiber_contains_distinct_notes setup failed")
    # For any candidate inverse inv(s), inv(support_proj(w)) cannot equal both w_a and w_b
    for inv_target in [w_a, w_b, ((1, 2), ())]:
        inv_pair = TranslationPair(forward=support_proj, backward=lambda _s, t=inv_target: t)
        if round_trip_coherent([w_a, w_b], [(1, 2)], inv_pair):
            failures.append("support_translation_never_round_trip_coherent violated")

    # 6. Verify all 39 theorem names in KIND_ROLE_OVERRIDES
    missing_roles = [name for name in EXPECTED_THEOREMS if name not in KIND_ROLE_OVERRIDES]
    if missing_roles:
        failures.append(f"missing from KIND_ROLE_OVERRIDES: {missing_roles}")

    result = {
        "unit": 72,
        "modules": [
            "PresentationDescent",
            "QuotientRetention",
            "FidelityClosure",
            "NoOutsideFidelity",
            "EndogenousFidelityGenerator",
        ],
        "coherent_bool_bijections": coherent_count,
        "generated_multiplicity_classes": len(gen_classes),
        "audited_theorem_count": len(EXPECTED_THEOREMS),
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
