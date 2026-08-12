"""Tests for the passage mirror and its growth driver."""

from __future__ import annotations

from pathlib import Path

import pytest

from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    arrow_report,
    col_ok,
    extension_proposals,
    graph_at,
    grow_block,
    grow_hist,
    growth_report,
    k4_passage_hist,
    next_family_p,
    obst_p,
    path_state,
    preplay,
    pstep,
    refine_ok,
    repair_family_p,
    response_menu,
    sep_col,
    sep_p,
    wf_pair,
    zero_p,
)
from dataclasses import replace


OBST = PS(occ=(0, 1), wit=((0, 1),), prot=((0, 1),), obs=(), budget=0)
FUNDED = replace(OBST, budget=5)


def test_observation_semantics() -> None:
    assert sep_col((1,), 0, 1)
    assert not sep_col((0, 1), 0, 1)
    assert sep_p(((1,),), 0, 1)
    assert zero_p((), 0, 1)
    assert not zero_p(((1,),), 0, 1)


def test_obstruction_four_conditions() -> None:
    # all four
    assert obst_p(OBST, 0, 1)
    # no observation declared: NOT obstructed (pre-observational)
    assert not obst_p(replace(OBST, obs=None), 0, 1)
    # separated observation
    assert not obst_p(replace(OBST, obs=((1,),)), 0, 1)
    # not protected
    assert not obst_p(replace(OBST, prot=()), 0, 1)
    # not retained
    assert not obst_p(replace(OBST, wit=()), 0, 1)


def test_step_guards_and_dedup() -> None:
    s = preplay([("admitOcc", 5), ("admitOcc", 5)], GENESIS_P)
    assert s.occ == (5,)
    # witness needs wf bounds
    assert pstep(GENESIS_P, ("admitWit", 0, 1)) == GENESIS_P
    assert not wf_pair(GENESIS_P, 0, 1)
    # protection needs a retained witness
    assert pstep(s, ("protect", 0, 0)) == s
    # declareObs only once
    s2 = pstep(pstep(s, ("declareObs",)), ("declareObs",))
    assert s2.obs == ()
    # duplicate witness silently deduped
    s3 = preplay([("admitOcc", 6)], s)
    s4 = preplay([("admitWit", 0, 1), ("admitWit", 0, 1)], s3)
    assert s4.wit == ((0, 1),)
    # duplicate protection deduped
    s5 = preplay([("protect", 0, 1), ("protect", 0, 1)], s4)
    assert s5.prot == ((0, 1),)
    # setLicense flips
    assert pstep(s5, ("setLicense", False)).licensed is False
    # malformed kind raises
    with pytest.raises(ValueError):
        pstep(s5, ("bogus",))


def test_refusal_certificate_and_record() -> None:
    # refusal needs the obstruction certificate
    live = replace(FUNDED, obs=((1,),))
    assert pstep(live, ("refuse", 0, 1)) == live
    refused = pstep(FUNDED, ("refuse", 0, 1))
    assert refused.refusals == ((0, 1),)
    # dedup
    assert pstep(refused, ("refuse", 0, 1)) == refused
    # object-inert
    assert refused.wit == FUNDED.wit
    assert refused.obs == FUNDED.obs
    assert not refused.halted


def test_terminal_absorbing() -> None:
    halted = pstep(FUNDED, ("halt",))
    assert halted.halted
    for e in [("admitOcc", 9), ("admitWit", 0, 1), ("protect", 0, 1),
              ("declareObs",), ("refineCol", (), 0),
              ("addCol", (1,)), ("refuse", 0, 1), ("setBudget", 3),
              ("setLicense", False)]:
        assert pstep(halted, e) == halted
    assert pstep(halted, ("halt",)) == halted


def test_gates_and_resolution() -> None:
    # unlicensed: proposal is not execution
    unl = replace(FUNDED, licensed=False)
    assert pstep(unl, ("addCol", (0,))) == unl
    # unfunded
    assert pstep(OBST, ("addCol", (0,))) == OBST
    # funded + licensed: resolves
    done = pstep(FUNDED, ("addCol", (0,)))
    assert done.obs == ((0,),)
    assert done.budget == 4
    assert not obst_p(done, 0, 1)
    # col_ok rejects stale/out-of-bounds/duplicate columns
    assert not col_ok(FUNDED, (7,))
    assert not col_ok(done, (0,))
    assert not col_ok(replace(FUNDED, obs=None), (0,))


def test_refine_family_and_menu() -> None:
    # a refinable state: column () present, obstruction (0,1) active
    s = PS(occ=(0, 1), wit=((0, 1),), prot=((0, 1),), obs=((),),
           budget=3)
    assert obst_p(s, 0, 1)
    menu = response_menu(s)
    assert ((), 0) in menu and ((), 1) in menu
    assert refine_ok(s, (), 0)
    fam = repair_family_p(s, 0, 1)
    assert ((), 0) in fam and ((), 1) in fam
    refined = pstep(s, ("refineCol", (), 0))
    assert refined.obs == ((0,),)
    assert not obst_p(refined, 0, 1)
    # refineCol on undeclared observation refuses
    assert response_menu(replace(s, obs=None)) == []
    assert repair_family_p(replace(s, obs=None), 0, 1) == []
    assert not refine_ok(replace(s, obs=None), (), 0)
    assert pstep(replace(s, obs=None),
                 ("refineCol", (), 0)) == replace(s, obs=None)


def test_two_rule_and_next_family() -> None:
    fam = next_family_p(FUNDED)
    assert (("setBudget", 1), ("addCol", (0,))) in fam
    # quiescent: family empty (the represented stop verdict)
    assert next_family_p(path_state(3)) == []
    # every emitted block executes and reduces the obstruction count
    for block in fam:
        after = preplay(list(block), FUNDED)
        assert not obst_p(after, 0, 1)
    # extension always available at an obstruction
    assert (0,) in extension_proposals(FUNDED, 0, 1)


def test_growth_matches_spec_to_fifteen_rounds() -> None:
    for k in range(15):
        assert graph_at(k + 1) == path_state(k)
        g = graph_at(k + 1)
        assert len(g.occ) - len(g.wit) == 1
        assert all(not obst_p(g, r[0], r[1]) for r in g.prot)


def test_round_records() -> None:
    for k in range(6):
        pre = preplay(grow_block(k + 2)[:4], path_state(k))
        assert obst_p(pre, k + 1, k + 2)
        assert (k + 1,) in extension_proposals(pre, k + 1, k + 2)
        assert pstep(pre, ("addCol", (k + 1,))) == path_state(k + 1)
        assert grow_block(k + 2)[-1] == ("addCol", (k + 1,))


def test_k4_passage() -> None:
    s = preplay(k4_passage_hist(), GENESIS_P)
    assert s.wit == ((0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3))
    assert s.prot == s.wit
    assert all(not obst_p(s, r[0], r[1]) for r in s.prot)


def test_reports_and_replay_determinism() -> None:
    rep = growth_report(5)
    assert rep["all_spec_match"] is True
    assert rep["all_quiescent"] is True
    assert rep["all_rounds_obstructed_then_resolved"] is True
    arrows = arrow_report()
    assert all(v is True for v in arrows.values())
    # replay determinism
    assert preplay(grow_hist(4), GENESIS_P) == preplay(
        grow_hist(4), GENESIS_P)


def test_runner_byte_stable(tmp_path: Path) -> None:
    import run_primitive_passage

    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_primitive_passage.main(
        ["--artifacts", str(d1), "--rounds", "5"]) == 0
    assert run_primitive_passage.main(
        ["--artifacts", str(d2), "--rounds", "5"]) == 0
    b1 = (d1 / "primitive_passage.json").read_bytes()
    b2 = (d2 / "primitive_passage.json").read_bytes()
    assert b1 == b2
