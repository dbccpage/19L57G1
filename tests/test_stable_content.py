"""Tests for the protected-separation / trace-stability mirror
(audit repair): sufficiency holds, the converse fails with two
countermodels, instability is witness-borne."""

from __future__ import annotations

from derivation.primitive_passage import GENESIS_P, PS, pstep
from derivation.stable_content import (
    event_battery,
    halted_countermodel,
    is_env_event,
    persistence_check,
    prot_sep,
    quiescence_check,
    quiescent_p,
    replay_persistence_check,
    sample_states,
    stable_content_report,
    unfunded_countermodel,
    unprotected_unstable,
)


def test_prot_sep_basics() -> None:
    # pre-observational states carry no protected separation
    assert not prot_sep(GENESIS_P, 0, 1)
    s = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
           prot=((0, 1),), obs=((0,),))
    assert prot_sep(s, 0, 1)
    # an unprotected pair is not protected-separated, even separated
    t = PS(occ=(0, 1), obs=((0,),))
    assert not prot_sep(t, 0, 1)


def test_sufficiency_single_step_and_traces() -> None:
    assert persistence_check(3)
    assert replay_persistence_check(3, 2)


def test_converse_is_false_absorbed() -> None:
    """Countermodel 1: a halted state absorbs the whole grammar, so
    an UNPROTECTED separation is trace stable."""
    cm = halted_countermodel()
    assert cm == {
        "separated": True,
        "not_protected": True,
        "every_event_inert": True,
        "trace_stable_but_unprotected": True,
    }


def test_converse_is_false_unfunded() -> None:
    """Countermodel 2: a live but unfunded state admits no internal
    observation change, so an UNPROTECTED separation is internally
    stable."""
    cm = unfunded_countermodel()
    assert cm == {
        "live": True,
        "separated": True,
        "not_protected": True,
        "internal_events_leave_obs_fixed": True,
        "internal_events_leave_budget_zero": True,
        "internally_stable_but_unprotected": True,
    }
    # the environment CAN refund — which is why budget is
    # environment-owned and this is only internal stability
    s = PS(occ=(0, 1), obs=((0,),), budget=0)
    assert pstep(s, ("setBudget", 3)).budget == 3
    assert is_env_event(("setBudget", 3))
    assert is_env_event(("admitOcc", 5))
    assert is_env_event(("setLicense", True))
    assert not is_env_event(("refineCol", (0,), 1))
    assert not is_env_event(("addCol", (0,)))


def test_instability_needs_witness() -> None:
    """Countermodel 3: with a funded accepted refinement routed
    through the separating column, the unprotected separation dies
    while the protected content survives."""
    cm = unprotected_unstable()
    assert cm == {
        "before_separated_unprotected": True,
        "refinement_accepted": True,
        "after_broken_unprotected": True,
        "protected_pair_now_separated": True,
        "protected_separation_intact": True,
    }


def test_report_records_the_open_gap() -> None:
    rep = stable_content_report(3)
    assert rep["sufficiency_single_step"] is True
    assert rep["sufficiency_along_traces"] is True
    assert rep["quiescence_iff_protected_separated"] is True
    assert rep["trace_depth_bound"] == 2
    assert rep["trace_breadth_bound"] == 24
    claim = rep["claim"]
    assert isinstance(claim, str)
    assert "SUFFICIENT" in claim and "converse is FALSE" in claim
    assert "OPEN" in claim
    gap = rep["open_exact_characterization"]
    assert isinstance(gap, str) and "OPEN" in gap
    # the report must not contain the retired "exactly" tag
    assert "stable_content_persists_battery" not in rep


def test_quiescence_battery() -> None:
    assert quiescence_check(3)
    s0, s1, s2, s3 = sample_states(3)
    assert s0.obs == ()
    assert s1.obs == ((0,),)
    assert s2.obs == ((0,), (1,))
    assert s3 != s1
    assert s3.obs == ((2, 0),)
    assert not quiescent_p(s0, 3)
    assert quiescent_p(s2, 3)
    assert quiescent_p(s3, 3)
    # quiescence is about protected separation, not trace stability
    assert quiescent_p(s3, 3) == all(
        prot_sep(s3, i, j)
        for (i, j) in s3.prot if (i, j) in s3.wit)


def test_battery_covers_every_kind() -> None:
    kinds = {e[0] for e in event_battery(3)}
    assert kinds == {"declareObs", "setBudget", "setLicense",
                     "admitOcc", "assertWit", "admitWit", "protect",
                     "refuse", "addCol", "refineCol", "halt"}
    # halted states keep their protected separations too
    s = sample_states(3)[3]
    h = pstep(s, ("halt",))
    for i in range(3):
        for j in range(3):
            assert prot_sep(h, i, j) == prot_sep(s, i, j)


def test_runner_includes_repaired_section(tmp_path: object) -> None:
    import json
    from pathlib import Path

    import run_primitive_passage

    d = tmp_path if isinstance(tmp_path, Path) else Path(str(tmp_path))
    assert run_primitive_passage.main(
        ["--artifacts", str(d), "--rounds", "3"]) == 0
    payload = json.loads(
        (d / "primitive_passage.json").read_text(encoding="utf-8"))
    sc = payload["stable_content"]
    assert sc["sufficiency_single_step"] is True
    assert sc["converse_false_absorbed"][
        "trace_stable_but_unprotected"] is True
    assert sc["converse_false_unfunded"][
        "internally_stable_but_unprotected"] is True
    assert sc["instability_needs_witness"][
        "after_broken_unprotected"] is True
