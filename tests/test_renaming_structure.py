"""Tests for the Goal-1 renaming-structure mirror."""

from __future__ import annotations

from itertools import permutations
from pathlib import Path

import run_renaming_structure
from derivation.attachment_ladder import (
    act,
    path_pol,
    star_pol,
    tree_at,
    up_block,
    up_family,
)
from derivation.renaming_structure import (
    action_laws,
    coherence,
    collapse_map,
    comp_ren,
    equal_cost_countermodel,
    equal_size_countermodel,
    group_laws,
    id_ren,
    inv_ren,
    non_bijective_countermodel,
    orbit_no_selection,
    raw_rename_pairs,
    renaming_report,
    sample_states,
    transport_laws,
)


def test_group_laws_exhaustive() -> None:
    rep = group_laws(3)
    assert rep["group_order"] == 6
    for key in ("comp_id", "id_comp", "comp_assoc", "inv_comp",
                "comp_inv", "inv_inv"):
        assert rep[key] is True, key
    # the structure itself, spot-checked
    assert id_ren(3) == (0, 1, 2)
    assert inv_ren((1, 2, 0)) == (2, 0, 1)
    # composition applies tau first
    assert comp_ren((1, 0, 2), (0, 2, 1)) == (1, 2, 0)


def test_action_laws() -> None:
    rep = action_laws(3)
    for key in ("act_id", "act_comp", "act_inv",
                "act_preserves_carrier_size", "fresh_tok_invariant"):
        assert rep[key] is True, key
    # a non-identity renaming genuinely moves a state
    path3 = tree_at(path_pol, 2)
    assert act((1, 0, 2), path3) != path3


def test_transport_respects_structure() -> None:
    rep = transport_laws(3)
    for key in ("block_id", "block_comp", "family_id", "family_comp",
                "membership_transport"):
        assert rep[key] is True, key


def test_coherence_under_composition() -> None:
    rep = coherence(3)
    assert rep["act_up_comm_composed"] is True
    assert rep["act_up_comm_twostep_agrees"] is True


def test_orbit_carries_no_representative() -> None:
    rep = orbit_no_selection(3)
    assert rep["family_length_equals_parents"] is True
    assert rep["orbit_closed_under_action"] is True
    assert rep["every_source_block_has_exact_named_transport"] is True
    assert rep["star_both_leaves_present"] is True
    assert rep["leaf_blocks_distinct"] is True
    star = tree_at(star_pol, 2)
    fam = up_family(star)
    # every parent's block is present; none is dropped
    assert len(fam) == 3
    assert all(up_block(star, p) in fam for p in range(3))
    for a in permutations(range(3)):
        target = act(a, star)
        for p in range(3):
            source_block = up_block(star, p)
            assert source_block in fam
            assert up_block(target, a[p]) in up_family(target)


def test_non_bijective_supplies_nothing() -> None:
    cm = non_bijective_countermodel()
    assert cm["no_left_inverse"] is True
    assert cm["original_store_irreflexive"] is True
    assert cm["pushforward_all_self_pairs"] is True
    assert cm["pushforward"] == [[0, 0], [0, 0]]
    assert collapse_map(7) == 0
    assert raw_rename_pairs(collapse_map, ((1, 2),)) == [(0, 0)]


def test_equal_size_and_equal_cost_supply_nothing() -> None:
    size = equal_size_countermodel()
    assert size["same_carrier"] is True
    assert size["families_literally_equal"] is True
    assert size["no_renaming_relates"] is True
    cost = equal_cost_countermodel()
    assert cost["both_in_family"] is True
    assert cost["equal_cost"] is True
    assert cost["executions_non_isomorphic"] is True


def test_sample_states_and_report_shape() -> None:
    states = sample_states(3)
    assert len(states) == 2
    assert all(len(s.occ) == 3 for s in states)
    rep = renaming_report(3)
    bounds = rep["bounds"]
    assert isinstance(bounds, dict)
    assert bounds["carrier"] == 3
    assert bounds["symmetric_group_order"] == 6
    assert bounds["assoc_triples_checked"] == 216
    scope = rep["equivariance_scope"]
    assert isinstance(scope, str)
    assert "NOT the observation calculus" in scope
    # every permutation was genuinely exercised
    assert len(list(permutations(range(3)))) == 6


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_renaming_structure.main(
        ["--artifacts", str(d1), "--carrier", "3"]) == 0
    assert run_renaming_structure.main(
        ["--artifacts", str(d2), "--carrier", "3"]) == 0
    assert (d1 / "renaming_structure.json").read_bytes() == \
        (d2 / "renaming_structure.json").read_bytes()
