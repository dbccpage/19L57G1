"""Tests for observer trace congruence and residual audit."""

import pytest
from congruence import (
    ObservationProjection,
    TransitionSystem,
    audit_observer_residuals,
    check_observer_trace_congruence,
    compute_congruence_partition,
)
from trace import State, Transition


def test_observer_congruence_zero_residuals() -> None:
    # Build a system with two internal states sA and sB that have different internal IDs
    # but produce identical observable outputs and transitions
    sA = State.create("sA", {"visible": 1, "hidden": 100})
    sB = State.create("sB", {"visible": 1, "hidden": 200})
    s_end = State.create("s_end", {"visible": 2, "hidden": 0})

    tA = Transition(sA, s_end, "tick")
    tB = Transition(sB, s_end, "tick")

    sys = TransitionSystem(
        states={"sA": sA, "sB": sB, "s_end": s_end},
        transitions=[tA, tB],
    )

    proj = ObservationProjection(
        name="visible_only",
        project_state=lambda s: s.get("visible"),
    )

    congruent, err = check_observer_trace_congruence(sA, sB, sys, proj, max_depth=3)
    assert congruent
    assert err is None

    audit = audit_observer_residuals(sys, proj, max_depth=3)
    assert audit.is_congruent
    assert not audit.unrecorded_residuals_detected
    assert len(audit.discrepancies) == 0


def test_observer_congruence_negative_control_residual_detection() -> None:
    # Negative control: sA and sB look identical initially (visible=1),
    # but transition differently: sA reaches visible=2, while sB reaches visible=3
    sA = State.create("sA", {"visible": 1, "flavor": "alpha"})
    sB = State.create("sB", {"visible": 1, "flavor": "beta"})
    sA_next = State.create("sA_next", {"visible": 2})
    sB_next = State.create("sB_next", {"visible": 3})

    tA = Transition(sA, sA_next, "step")
    tB = Transition(sB, sB_next, "step")

    sys = TransitionSystem(
        states={"sA": sA, "sB": sB, "sA_next": sA_next, "sB_next": sB_next},
        transitions=[tA, tB],
    )

    proj = ObservationProjection(
        name="visible_only",
        project_state=lambda s: s.get("visible"),
    )

    congruent, err = check_observer_trace_congruence(sA, sB, sys, proj, max_depth=2)
    assert not congruent
    assert err is not None
    assert "discrepancy" in err.lower() or "mismatch" in err.lower()


def test_observer_congruence_action_mismatch_negative_control() -> None:
    # sA and sB have same visible value, but sA allows action 'left', sB allows 'right'
    sA = State.create("sA", {"val": 5})
    sB = State.create("sB", {"val": 5})
    s_leaf = State.create("s_leaf", {"val": 10})

    tA = Transition(sA, s_leaf, "left")
    tB = Transition(sB, s_leaf, "right")

    sys = TransitionSystem(
        states={"sA": sA, "sB": sB, "s_leaf": s_leaf},
        transitions=[tA, tB],
    )

    proj = ObservationProjection(
        name="val_only",
        project_state=lambda s: s.get("val"),
    )

    congruent, err = check_observer_trace_congruence(sA, sB, sys, proj, max_depth=2)
    assert not congruent
    assert "actions differ" in err
