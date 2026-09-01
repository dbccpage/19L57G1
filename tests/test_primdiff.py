"""Tests for the primitive-difference finite searches."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.primdiff import (
    CARRIER_ID,
    CARRIER_SWAP,
    D2,
    D2_REV,
    S2,
    Pointed,
    a1,
    a1i,
    a3,
    a4,
    automorphisms,
    carrier_table,
    collision,
    closure,
    collapse_report,
    compose,
    enumerate_pointed,
    frontier_profile_countermodel,
    implication_matrix,
    invariant_separating_classifiers,
    irreflexive_relations_on,
    merge_map,
    min_carrier_for_k,
    collision_profile,
    pointed_isomorphic,
    pushforward,
    symmetrize,
    transposition_report,
    transpose,
    two_element_report,
)

import run_primdiff


def test_candidate_basics() -> None:
    assert a1(D2) and a1i(D2) and a3(D2)
    self_edge = Pointed(1, frozenset({(0, 0)}), 0, 0)
    assert a1(self_edge) and not a1i(self_edge) and not a3(self_edge)
    empty = Pointed(2, frozenset(), 0, 1)
    assert not a1(empty) and a3(empty)


def test_closure_is_a_monoid() -> None:
    swap = (1, 0)
    cl = closure(2, [swap])
    assert (0, 1) in cl and swap in cl and len(cl) == 2
    const = (0, 0)
    cl2 = closure(2, [swap, const])
    # swap, id, const0, and swap.const0 = const1
    assert len(cl2) == 4


def test_a4_endpoints() -> None:
    # Empty family: irreducibility is exactly metatheoretic inequality.
    assert a4(D2, []) is True
    assert a4(Pointed(2, frozenset(), 0, 0), []) is False
    # A merger of the pair erases the difference.
    assert a4(D2, [merge_map(2, 0, 1)]) is False
    # Constants erase everything.
    assert a4(D2, [(0, 0), (1, 1)]) is False


def test_implication_matrix_structure() -> None:
    m = implication_matrix(2)
    imp = m["implications"]
    assert isinstance(imp, dict)
    # Theorem echoes.
    assert imp["A1i->A3"] is True
    assert imp["A1i->A1"] is True
    assert imp["A3->A4_empty"] is True and imp["A4_empty->A3"] is True
    # Orthogonality with countermodels.
    assert imp["A1->A3"] is False
    assert imp["A3->A1"] is False
    cms = m["countermodels"]
    assert isinstance(cms, dict)
    assert "A1->A3" in cms and "A3->A1" in cms
    # Vacuous candidates are flagged, and vacuous rows are excluded from
    # the non-vacuous view.
    assert m["vacuous_candidates"] == ["A4_all_constants", "A4_merge_ab"]
    nonvac = m["implications_nonvacuous"]
    assert isinstance(nonvac, dict)
    assert "A4_merge_ab->A1" not in nonvac
    extents = m["predicate_extents"]
    assert isinstance(extents, dict)
    assert extents["A1"] > 0 and extents["A4_merge_ab"] == 0


def test_two_element_report() -> None:
    rep = two_element_report(3)
    assert rep["initiality_universal_within_scope"] is True
    mins = rep["minimal_carrier_by_axiom_set"]
    assert isinstance(mins, dict)
    assert mins["bare"] == 1
    assert mins["irreflexive"] == 2
    assert mins["irreflexive+symmetric"] == 2
    assert rep["two_element_not_forced_without_irreflexivity"] is True
    assert rep["larger_witnessed_irreflexive_models_exist"] is True


def test_carrier_swap_carries_each_orientation_onto_the_other() -> None:
    """Mutation: swap the orientations in the image and this fails."""
    assert pushforward(D2.rel, CARRIER_SWAP) == D2_REV.rel
    assert pushforward(D2_REV.rel, CARRIER_SWAP) == D2.rel


def test_carrier_swap_twice_is_identity_and_restores_both() -> None:
    twice = compose(CARRIER_SWAP, CARRIER_SWAP)
    assert twice == CARRIER_ID
    assert pushforward(D2.rel, twice) == D2.rel
    assert pushforward(D2_REV.rel, twice) == D2_REV.rel


def test_both_orientations_have_the_same_symmetrization() -> None:
    assert symmetrize(D2.rel) == S2.rel
    assert symmetrize(D2_REV.rel) == S2.rel
    assert symmetrize(D2.rel) == symmetrize(D2_REV.rel)


def test_carrier_swap_is_auto_of_S2_not_of_either_orientation() -> None:
    assert pushforward(S2.rel, CARRIER_SWAP) == S2.rel
    assert pushforward(D2.rel, CARRIER_SWAP) != D2.rel
    assert pushforward(D2_REV.rel, CARRIER_SWAP) != D2_REV.rel


def test_unpointed_irrefl_nonempty_census_on_two() -> None:
    """Every inhabited irreflexive relation on carrier 2 is one of the three.

    Mutation: drop D2_REV from the right-hand set and the census is a lie
    about the unpointed signature (the pointed census already excludes it
    by fixing the designated pair).
    """
    nonempty = [rel for rel in irreflexive_relations_on(2) if rel]
    assert set(nonempty) == {D2.rel, D2_REV.rel, S2.rel}


def test_transposition_report_agrees_with_the_live_maps() -> None:
    rep = transposition_report()
    twice = compose(CARRIER_SWAP, CARRIER_SWAP)
    nonempty = [rel for rel in irreflexive_relations_on(2) if rel]
    assert rep["swap_pushes_D2_to_D2rev"] is (
        pushforward(D2.rel, CARRIER_SWAP) == D2_REV.rel
    )
    assert rep["swap_twice_is_identity"] is (twice == CARRIER_ID)
    assert rep["sym_D2rev_is_S2"] is (symmetrize(D2_REV.rel) == S2.rel)
    assert rep["swap_is_auto_of_S2"] is (
        pushforward(S2.rel, CARRIER_SWAP) == S2.rel
    )
    assert rep["swap_is_not_auto_of_D2"] is (
        pushforward(D2.rel, CARRIER_SWAP) != D2.rel
    )
    assert rep["unpointed_irrefl_nonempty_count"] == len(nonempty)
    assert rep["unpointed_irrefl_nonempty_are_exactly_the_three"] is (
        set(nonempty) == {D2.rel, D2_REV.rel, S2.rel}
    )
    assert all(
        rep[key] is True
        for key in (
            "swap_pushes_D2_to_D2rev",
            "swap_pushes_D2rev_to_D2",
            "swap_twice_is_identity",
            "swap_twice_restores_D2",
            "swap_twice_restores_D2rev",
            "sym_D2_is_S2",
            "sym_D2rev_is_S2",
            "swap_is_auto_of_S2",
            "swap_is_not_auto_of_D2",
            "swap_is_not_auto_of_D2rev",
            "unpointed_irrefl_nonempty_are_exactly_the_three",
        )
    )


def test_observer_orientation_gap() -> None:
    assert len(automorphisms(S2, pointed=False)) == 2
    assert len(automorphisms(D2, pointed=False)) == 1
    assert invariant_separating_classifiers(S2) == []
    assert len(invariant_separating_classifiers(D2)) == 2
    # Pointed automorphisms fix the designated pair.
    assert automorphisms(S2, pointed=True) == [(0, 1)]


def test_collapse_collision_and_pushforward() -> None:
    f = merge_map(2, 0, 1)
    assert collision(D2.rel, f)
    assert pushforward(D2.rel, f) == frozenset({(0, 0)})
    assert transpose(D2.rel) == D2_REV.rel
    rep = collapse_report(2)
    assert rep["collision_iff_pushforward_not_irreflexive"] is True
    assert rep["collision_transpose_invariant"] is True
    # D2 and S2 have identical collision behavior (Lean:
    # D2_S2_collapse_equiv); collision profiles agree.
    assert collision_profile(D2) == collision_profile(S2)


def test_pointed_isomorphic_transports_points() -> None:
    """The bijection may move the raw point indices (review fix): the
    oriented edge pointed at (0, 1) is isomorphic to its relabeling
    pointed at (1, 0), via the swap."""
    s = Pointed(2, frozenset({(0, 1)}), 0, 1)
    t = Pointed(2, frozenset({(1, 0)}), 1, 0)
    assert pointed_isomorphic(s, t)
    assert not pointed_isomorphic(s, Pointed(3, s.rel, 0, 1))


def test_carrier_table_matches_capacity_formula() -> None:
    table = carrier_table(6)
    oriented = table["oriented"]
    unordered = table["unordered"]
    assert isinstance(oriented, dict) and isinstance(unordered, dict)
    assert oriented["1"] == 2 and oriented["3"] == 3
    assert unordered["1"] == 2 and unordered["2"] == 3 and unordered["4"] == 4
    assert min_carrier_for_k(1, True) == 2


def test_frontier_profiles_do_not_classify() -> None:
    cm = frontier_profile_countermodel()
    assert cm["profiles_equal"] is True
    assert cm["pointed_isomorphic"] is False
    assert cm["profiles_classify"] is False
    assert collision_profile(D2) == collision_profile(D2_REV)
    assert not pointed_isomorphic(D2, D2_REV)
    assert pointed_isomorphic(D2, D2)


def test_enumeration_counts() -> None:
    # 2^(n*n) relations times n*n point choices.
    assert sum(1 for _ in enumerate_pointed(1)) == 2
    assert sum(1 for _ in enumerate_pointed(2)) == (1 << 4) * 4


def test_run_primdiff_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_primdiff.main(["--artifacts", str(out), "--max-n", "2"]) == 0
    payload = json.loads((out / "primdiff.json").read_text(encoding="utf-8"))
    assert payload["observer"]["orientation_gap"] is True
    assert payload["transposition"][
        "unpointed_irrefl_nonempty_are_exactly_the_three"
    ]
    assert payload["collapse"]["identifying_witnessed_pair_always_collides"]
    # Determinism.
    out2 = tmp_path / "artifacts2"
    run_primdiff.main(["--artifacts", str(out2), "--max-n", "2"])
    assert (out / "primdiff.json").read_bytes() == (
        out2 / "primdiff.json"
    ).read_bytes()
