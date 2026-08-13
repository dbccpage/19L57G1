"""Tests for the repaired attachment/ladder mirror."""

from __future__ import annotations

from itertools import permutations
from pathlib import Path

import run_attachment_ladder
from derivation.attachment_ladder import (
    act,
    asc,
    attach_block,
    attach_checked,
    bad_choice,
    clamp_countermodel,
    clamped_par,
    combs,
    d2_zero_dim,
    facets,
    fresh_tok,
    full_shell_complex,
    is_tree,
    isomorphic_undirected,
    ladder_report,
    lawful_to,
    length_not_fresh_countermodel,
    par,
    parent_orbits,
    path_pol,
    pseudo_cell_countermodel,
    renaming_report,
    shape_report,
    shell_n,
    shell_n_legacy,
    star_pol,
    step_n,
    step_v,
    store_automorphisms,
    tree_at,
    tree_report,
    tree_state,
    up_block,
    up_family,
    up_report,
    wf_complex,
    zigzag_pol,
)
from derivation.primitive_passage import PS, preplay


def test_no_clamping_typed_refusal() -> None:
    # the retired clamp rewrote illegal input; recorded countermodel
    cm = clamp_countermodel()
    assert cm["rewritten_input_is_not_lawful"] is True
    assert clamped_par(bad_choice, 0) == 0
    assert bad_choice(1) == 8
    # illegal parent meets the typed refusal, never a rewrite
    s = tree_at(path_pol, 2)
    ref = attach_checked(s, bad_choice(2))
    assert ref == {"outcome": "refusedParent", "parent": 9,
                   "bound": 3}
    ok = attach_checked(s, 0)
    assert ok["outcome"] == "attached"
    assert ok["occ_len"] == 4
    # halted states are refused too
    halted = PS(occ=(0,), halted=True)
    assert attach_checked(halted, 0)["outcome"] == "refusedParent"
    # the used policies are lawful over the exercised range
    for pi in (path_pol, star_pol, zigzag_pol):
        assert lawful_to(pi, 20)


def test_tokens_positions_freshness() -> None:
    assert fresh_tok(PS(occ=())) == 0
    assert fresh_tok(PS(occ=(1, 2))) == 3
    cm = length_not_fresh_countermodel()
    assert cm["old_block_fails_to_extend"] is True
    assert cm["canonical_fresh_token"] == 3
    assert cm["repaired_block_extends"] is True


def test_up_family_registry_iff() -> None:
    rep = up_report()
    assert rep["every_member_is_legal"] is True
    assert rep["every_legal_is_member"] is True
    assert rep["out_of_registry_absent"] is True
    assert rep["grammar_uniform_same_carrier"] is True
    assert rep["star_leaves_one_orbit"] is True
    assert rep["oriented_path_rigid"] is True
    star3 = tree_at(star_pol, 2)
    assert len(store_automorphisms(star3)) == 2
    assert parent_orbits(star3) == [[0], [1, 2]]
    fam = up_family(star3)
    assert len(fam) == 3
    assert fam[1][1] == ("assertWit", 1, 3)


def test_every_policy_yields_spec_trees() -> None:
    for pi in (path_pol, star_pol, zigzag_pol):
        for n in range(10):
            s = tree_at(pi, n)
            assert s == tree_state(pi, n)
            assert len(s.occ) - len(s.wit) == 1
            assert is_tree(s)
            assert s.obs is None
            # the tree grammar IS the Up grammar on canonical states
            assert attach_block(pi, n) == up_block(
                tree_state(pi, n), par(pi, n))
    assert par(star_pol, 5) == 0
    assert par(path_pol, 5) == 5


def test_shape_not_forced() -> None:
    rep = shape_report()
    assert rep["isomorphic_undirected"] is False
    assert rep["trees_but_shapes_differ"] is True
    # sanity: a tree IS isomorphic to itself
    p4 = tree_at(path_pol, 3).wit
    assert isomorphic_undirected(p4, p4, 4)


def test_renaming_action_and_countermodels() -> None:
    rep = renaming_report()
    assert rep["act_up_comm_all_perms"] is True
    assert rep["up_family_transport_all_perms"] is True
    assert rep["fresh_tok_invariant"] is True
    eq = rep["equal_size_not_renaming_related"]
    assert isinstance(eq, dict)
    assert eq["same_carrier"] is True
    assert eq["families_equal"] is True
    assert eq["no_renaming_relates"] is True
    div = rep["equal_cost_divergence"]
    assert isinstance(div, dict)
    assert div["both_in_family"] is True
    assert div["equal_cost"] is True
    assert div["extensions_non_isomorphic"] is True
    # the action is a genuine group action on the sample carrier
    star3 = tree_at(star_pol, 2)
    ident = (0, 1, 2)
    assert act(ident, star3) == star3
    for perm in permutations(range(3)):
        inv = tuple(perm.index(i) for i in range(3))
        assert act(inv, act(perm, star3)) == star3
    # a genuine renaming of the path DOES relate to itself renamed
    path3 = tree_at(path_pol, 2)
    moved = act((1, 0, 2), path3)
    assert moved != path3
    assert act((1, 0, 2), moved) == path3


def test_tree_report_bounds() -> None:
    rep = tree_report(5)
    for name in ("path", "star", "zigzag"):
        entry = rep[name]
        assert isinstance(entry, dict)
        assert entry["lawful_to_rounds"] is True
        assert entry["all_spec_match"] is True
        assert entry["all_residue_one"] is True
        assert entry["all_trees"] is True
        assert entry["all_blocks_are_up_blocks"] is True


def test_is_tree_negatives() -> None:
    # duplicate child (two parents)
    bad1 = PS(occ=(0, 1, 2), wit=((0, 1), (2, 1)))
    assert not is_tree(bad1)
    # descending edge
    bad2 = PS(occ=(0, 1, 2), wit=((2, 1), (0, 2)))
    assert not is_tree(bad2)
    # missing child edge
    bad3 = PS(occ=(0, 1, 2), wit=((0, 1),))
    assert not is_tree(bad3)


def test_generalized_ladder_repaired() -> None:
    rep = ladder_report(5)
    assert rep["all_ladders_fire"] is True
    assert rep["all_guards_load_bearing"] is True
    assert rep["all_wf"] is True
    assert rep["all_d2_zero"] is True
    # the required pseudo-cell countermodel
    pc = rep["pseudo_cell"]
    assert isinstance(pc, dict)
    assert pc["legacy_admits_pseudo_cell"] is True
    assert pc["repaired_refuses"] is True
    assert pc["repaired_step_inert"] is True
    assert pseudo_cell_countermodel() == pc
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
    # ascent: the repaired guard refuses what legacy admitted
    one_v = step_v({}, 0)
    assert shell_n_legacy(one_v, 1, (0, 0))
    assert not shell_n(one_v, 1, (0, 0))
    assert not asc((0, 0))
    assert asc((0, 2, 5))
    assert wf_complex(filled)
    assert not wf_complex({1: [(0, 0)]})
    # vertex dedup
    assert step_v(step_v({}, 0), 0) == {0: [(0,)]}
    # facets and combs
    assert facets((0, 1, 2)) == [(1, 2), (0, 2), (0, 1)]
    assert len(combs(5, 2)) == 10
    assert d2_zero_dim((0, 1, 2, 3, 4, 5))  # dim-5 spot check


def test_act_maps_observation_columns() -> None:
    s = PS(occ=(0, 1), obs=((0, 1), (1, 0)))
    swapped = act((1, 0), s)
    assert swapped.obs == ((1, 0), (0, 1))
    # replay of the old block on a state with a column intact
    plain = preplay([("admitOcc", 0)], PS(occ=()))
    assert plain.occ == (0,)


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
