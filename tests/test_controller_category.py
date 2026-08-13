"""Tests for the controller-category mirror."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from derivation.controller_category import (
    BASIS_EVENTS,
    BASIS_STATES,
    DUPSTATE,
    FULL_K,
    HALTED0,
    HALTED1,
    KIND_NAMES,
    LOBST,
    NO_ADD_K,
    NO_BUDGET_K,
    NO_REFINE_K,
    NO_REFUSE_K,
    OBST0,
    OBST5,
    TWORULE_BLOCK,
    all_kinds,
    behavior_signature,
    category_report,
    controller_category_report,
    enabled,
    erase_ref,
    event_json,
    full_without,
    has_dup,
    interp_k,
    kind_json,
    live_behavior_classes,
    nonuniqueness_report,
    ps_json,
    replay_k,
    response_kind_countermodels,
    response_live,
    strict_refinement_report,
    twist_f,
    twist_ref,
)
from derivation.primitive_passage import (
    GENESIS_P,
    grow_hist,
    next_family_p,
    obst_p,
    preplay,
    pstep,
)


def test_class_enumeration() -> None:
    kinds = all_kinds()
    assert len(kinds) == 1024
    assert len(set(kinds)) == 1024
    assert kinds[0] == (False,) * 10
    assert kinds[-1] == FULL_K
    assert FULL_K in kinds


def test_enabled_and_interp() -> None:
    assert enabled(FULL_K, ("halt",))
    assert not enabled(NO_ADD_K, ("addCol", (0,)))
    assert enabled(NO_ADD_K, ("setBudget", 1))
    # disabled events are inert; enabled events step
    assert interp_k(NO_ADD_K, OBST5, ("addCol", (0,))) == OBST5
    assert interp_k(FULL_K, OBST5, ("setBudget", 1)).budget == 1
    with pytest.raises(ValueError):
        enabled(FULL_K, ("bogus",))
    with pytest.raises(ValueError):
        enabled(FULL_K, (7,))


def test_full_without() -> None:
    assert NO_REFUSE_K[KIND_NAMES.index("refuse")] is False
    assert sum(1 for b in NO_REFUSE_K if not b) == 1
    with pytest.raises(ValueError):
        full_without("bogus")


def test_live_census_and_tworule() -> None:
    live = [d for d in all_kinds() if response_live(d)]
    assert len(live) == 128
    assert response_live(FULL_K)
    assert not response_live(NO_ADD_K)
    assert not response_live(NO_BUDGET_K)
    assert not response_live(NO_REFINE_K)
    assert response_live(NO_REFUSE_K)
    # every live member executes and resolves the funded extension
    for d in live:
        after = replay_k(d, TWORULE_BLOCK, OBST5)
        assert not obst_p(after, 0, 1)


def test_response_kind_countermodels() -> None:
    # addCol off at OBST5: empty repair menu, extension is the only
    # route; obstruction survives the whole driver battery
    battery5 = next_family_p(OBST5)
    assert battery5 != []
    assert all(obst_p(replay_k(NO_ADD_K, blk, OBST5), 0, 1)
               for blk in battery5)
    # setBudget off at the unfunded obstruction
    battery0 = next_family_p(OBST0)
    assert battery0 != []
    assert all(obst_p(replay_k(NO_BUDGET_K, blk, OBST0), 0, 1)
               for blk in battery0)
    # refineCol off at the unlicensed refinable obstruction
    batteryl = next_family_p(LOBST)
    assert batteryl != []
    assert all(obst_p(replay_k(NO_REFINE_K, blk, LOBST), 0, 1)
               for blk in batteryl)
    # the all-on controller resolves each state
    assert not obst_p(replay_k(FULL_K, TWORULE_BLOCK, OBST5), 0, 1)
    assert not obst_p(replay_k(FULL_K, TWORULE_BLOCK, OBST0), 0, 1)
    assert not obst_p(
        replay_k(FULL_K, (("refineCol", (), 0),), LOBST), 0, 1)
    rep = response_kind_countermodels()
    for name in ("addCol", "setBudget", "refineCol"):
        case = rep[name]
        assert isinstance(case, dict)
        assert case["obstruction_certified"] is True
        assert case["obstruction_persists_on_all_blocks"] is True
        assert case["full_controller_resolves"] is True


def test_nonuniqueness() -> None:
    # identical on every refusal-free basis cell
    for s in BASIS_STATES:
        for e in BASIS_EVENTS:
            if e[0] == "refuse":
                continue
            assert interp_k(FULL_K, s, e) == interp_k(NO_REFUSE_K, s, e)
    # distinct on a refuse event at the certified obstruction
    assert obst_p(OBST5, 0, 1)
    assert (interp_k(FULL_K, OBST5, ("refuse", 0, 1))
            != interp_k(NO_REFUSE_K, OBST5, ("refuse", 0, 1)))
    rep = nonuniqueness_report()
    assert rep["both_live"] is True
    assert rep["agree_on_all_nonrefuse_basis_cells"] is True
    assert rep["differ_on_refuse_at_certified_obstruction"] is True
    assert rep["conclusion"] == "NONUNIQUE_CONTROLLER_FAMILY"
    basis = rep["behavioral_basis"]
    assert isinstance(basis, dict)
    assert basis["live_members"] == 128
    assert basis["distinct_behavioral_classes"] == 128


def test_behavior_signature_distinguishes() -> None:
    assert live_behavior_classes() == 128
    assert (behavior_signature(FULL_K)
            != behavior_signature(NO_REFUSE_K))
    # two identical controllers share a signature
    assert behavior_signature(FULL_K) == behavior_signature(
        tuple(True for _ in KIND_NAMES))


def test_constant_simulations() -> None:
    assert HALTED0 != HALTED1
    for c in (HALTED0, HALTED1):
        for e in BASIS_EVENTS:
            assert interp_k(FULL_K, c, e) == c
    rep = category_report()
    assert rep["objects"] == 1024
    inert = rep["constant_simulation_targets_inert"]
    assert isinstance(inert, dict)
    assert inert["halted0"] is True
    assert inert["halted1"] is True
    assert rep["constants_distinct"] is True
    assert rep["two_distinct_endo_simulations_on_full"] is True


def test_has_dup_and_twist() -> None:
    assert not has_dup(())
    assert not has_dup((1, 2, 3))
    assert has_dup((5, 5))
    assert has_dup((1, 2, 1))
    assert twist_ref(DUPSTATE) == ((0, 0),)
    assert twist_ref(GENESIS_P) == ()
    assert twist_f(GENESIS_P) == GENESIS_P
    assert erase_ref(GENESIS_P) == GENESIS_P
    # distinct off the orbit, at the duplicate state
    assert twist_f(DUPSTATE) != erase_ref(DUPSTATE)
    assert twist_f(DUPSTATE).refusals == ((0, 0),)
    assert erase_ref(DUPSTATE).refusals == ()


def test_twist_and_erase_are_simulations() -> None:
    # the simulation square on the declared battery, including the
    # off-orbit duplicate state
    for f in (twist_f, erase_ref):
        for s in BASIS_STATES + (DUPSTATE,):
            for e in BASIS_EVENTS:
                assert (f(interp_k(FULL_K, s, e))
                        == interp_k(NO_REFUSE_K, f(s), e))


def test_strict_refinement_report() -> None:
    rep = strict_refinement_report()
    assert rep["constants_excluded_by_liveness"] is True
    assert rep["erase_is_strict"] is True
    assert rep["twist_is_strict"] is True
    assert rep["erase_comm_on_battery"] is True
    assert rep["twist_comm_on_battery"] is True
    assert rep["twist_ne_erase"] is True
    assert rep["global_uniqueness"] == "REFUTED_BY_INVARIANT_TWIST"
    orbit = rep["reachable_orbit"]
    assert isinstance(orbit, dict)
    assert orbit["occurrence_stores_duplicate_free"] is True
    assert orbit["twist_agrees_with_erase"] is True


def test_reachable_orbit_agreement() -> None:
    for k in range(6):
        s = preplay(grow_hist(k), GENESIS_P)
        assert not has_dup(s.occ)
        assert twist_f(s) == erase_ref(s)


def test_serialization() -> None:
    js = ps_json(OBST5)
    assert js["occ"] == [0, 1]
    assert js["obs"] == []
    assert ps_json(DUPSTATE)["obs"] is None
    kj = kind_json(NO_REFUSE_K)
    assert kj["refuse"] is False and kj["halt"] is True
    assert event_json(("addCol", (0,))) == ["addCol", [0]]
    assert event_json(("setLicense", False)) == ["setLicense", False]
    with pytest.raises(AssertionError):
        event_json(("addCol", (0, "x")))
    with pytest.raises(AssertionError):
        event_json((("nested",), 1.5))


def test_full_report_shape() -> None:
    rep = controller_category_report()
    assert rep["class_size"] == 1024
    assert rep["live_census"] == 128
    assert rep["tworule_all_live_pass"] is True
    assert rep["initiality"] == "REFUTED_BY_CONSTANT_SIMULATIONS"
    assert set(rep) == {
        "class_size", "live_census", "tworule_all_live_pass",
        "response_kind_countermodels", "nonuniqueness", "initiality",
        "category", "strict_refinement"}


def test_halted_states_absorb_under_every_controller() -> None:
    # spot-check the constant-simulation source side: whatever the
    # controller does to the source state, the constant lands on an
    # inert halted state
    sample = [FULL_K, NO_REFUSE_K, NO_ADD_K, (False,) * 10]
    for d in sample:
        for s in (OBST5, GENESIS_P):
            for e in BASIS_EVENTS:
                assert pstep(HALTED0, e) == HALTED0
                assert interp_k(d, HALTED0, e) == HALTED0


def test_replay_k_disabled_prefix() -> None:
    # a fully disabled controller replays to the start state
    dead = (False,) * 10
    assert replay_k(dead, list(TWORULE_BLOCK), OBST5) == OBST5
    # the twist state stays off-orbit under growth events
    grown = interp_k(FULL_K, DUPSTATE, ("admitOcc", 2))
    assert has_dup(grown.occ)
    assert replace(twist_f(grown), refusals=()) == erase_ref(grown)


def test_runner_byte_stable(tmp_path: Path) -> None:
    import run_controller_category

    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_controller_category.main(["--artifacts", str(d1)]) == 0
    assert run_controller_category.main(["--artifacts", str(d2)]) == 0
    b1 = (d1 / "primitive_controller_category.json").read_bytes()
    b2 = (d2 / "primitive_controller_category.json").read_bytes()
    assert b1 == b2
