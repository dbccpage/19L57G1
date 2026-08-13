"""Tests for the attachment/ladder mirror."""

from __future__ import annotations

from pathlib import Path

import run_attachment_ladder
from derivation.attachment_ladder import (
    attach_moves,
    combs,
    d2_zero_dim,
    facets,
    full_shell_complex,
    is_tree,
    isomorphic_undirected,
    ladder_report,
    par,
    parent_orbits,
    path_pol,
    shape_report,
    shell_n,
    star_pol,
    step_n,
    step_v,
    store_automorphisms,
    tree_at,
    tree_report,
    tree_state,
    up_report,
    zigzag_pol,
)


def test_every_policy_yields_spec_trees() -> None:
    for pi in (path_pol, star_pol, zigzag_pol):
        for n in range(10):
            s = tree_at(pi, n)
            assert s == tree_state(pi, n)
            assert len(s.occ) - len(s.wit) == 1
            assert is_tree(s)
            assert s.obs is None
    assert par(star_pol, 5) == 0
    assert par(path_pol, 5) == 5


def test_shape_not_forced() -> None:
    rep = shape_report()
    assert rep["isomorphic_undirected"] is False
    assert rep["trees_but_shapes_differ"] is True
    # sanity: a tree IS isomorphic to itself
    p4 = tree_at(path_pol, 3).wit
    assert isomorphic_undirected(p4, p4, 4)


def test_up_family_and_orbits() -> None:
    rep = up_report()
    assert rep["family_length_equals_parents"] is True
    assert rep["presentation_invariant"] is True
    assert rep["star_leaves_one_orbit"] is True
    assert rep["oriented_path_rigid"] is True
    star3 = tree_at(star_pol, 2)
    assert len(store_automorphisms(star3)) == 2
    assert parent_orbits(star3) == [[0], [1, 2]]
    moves = attach_moves(star3)
    assert len(moves) == 3
    assert moves[1][1] == ("assertWit", 1, 3)


def test_tree_report_bounds() -> None:
    rep = tree_report(5)
    for name in ("path", "star", "zigzag"):
        entry = rep[name]
        assert isinstance(entry, dict)
        assert entry["all_spec_match"] is True
        assert entry["all_residue_one"] is True
        assert entry["all_trees"] is True


def test_is_tree_negatives() -> None:
    from derivation.primitive_passage import PS

    # duplicate child (two parents)
    bad1 = PS(occ=(0, 1, 2), wit=((0, 1), (2, 1)))
    assert not is_tree(bad1)
    # descending edge
    bad2 = PS(occ=(0, 1, 2), wit=((2, 1), (0, 2)))
    assert not is_tree(bad2)
    # missing child edge
    bad3 = PS(occ=(0, 1, 2), wit=((0, 1),))
    assert not is_tree(bad3)


def test_generalized_ladder() -> None:
    rep = ladder_report(5)
    assert rep["all_ladders_fire"] is True
    assert rep["all_guards_load_bearing"] is True
    assert rep["all_d2_zero"] is True
    # dimension-4 demo mirrors the Lean instance
    per = rep["per_dim"]
    assert isinstance(per, dict)
    d4 = per["4"]
    assert isinstance(d4, dict)
    assert d4["cells_per_dim"] == {
        "0": 5, "1": 10, "2": 10, "3": 5, "4": 1}
    # shell guard details
    shell = full_shell_complex(4, top=False)
    assert shell_n(shell, 3, (0, 1, 2, 3))
    assert not shell_n(shell, 3, (0, 1, 2))       # wrong arity
    assert not shell_n({}, 3, (0, 1, 2, 3))       # missing facets
    filled = step_n(shell, 3, (0, 1, 2, 3))
    assert not shell_n(filled, 3, (0, 1, 2, 3))   # already filled
    assert step_n(filled, 3, (0, 1, 2, 3)) == filled
    # vertex dedup
    assert step_v(step_v({}, 0), 0) == {0: [(0,)]}
    # facets and combs
    assert facets((0, 1, 2)) == [(1, 2), (0, 2), (0, 1)]
    assert len(combs(5, 2)) == 10
    assert d2_zero_dim((0, 1, 2, 3, 4, 5))  # dim-5 spot check


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_attachment_ladder.main(
        ["--artifacts", str(d1), "--rounds", "4",
         "--max-dim", "4"]) == 0
    assert run_attachment_ladder.main(
        ["--artifacts", str(d2), "--rounds", "4",
         "--max-dim", "4"]) == 0
    assert (d1 / "attachment_ladder.json").read_bytes() == \
        (d2 / "attachment_ladder.json").read_bytes()
