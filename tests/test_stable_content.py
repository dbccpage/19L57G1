"""Tests for the stable-content mirror."""

from __future__ import annotations

from derivation.primitive_passage import GENESIS_P, PS, pstep, preplay
from derivation.stable_content import (
    event_battery,
    persistence_check,
    quiescence_check,
    quiescent_p,
    sample_states,
    stable_content_report,
    stable_sep,
    unprotected_unstable,
)


def test_stable_sep_basics() -> None:
    # pre-observational states have no stable content
    assert not stable_sep(GENESIS_P, 0, 1)
    s = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
           prot=((0, 1),), obs=((0,),))
    assert stable_sep(s, 0, 1)
    # unprotected pair is not in the stable content, even separated
    t = PS(occ=(0, 1), obs=((0,),))
    assert not stable_sep(t, 0, 1)


def test_persistence_and_quiescence_battery() -> None:
    assert persistence_check(3)
    assert quiescence_check(3)
    rep = stable_content_report(3)
    assert rep["stable_content_persists_battery"] is True
    assert rep["quiescence_iff_protected_in_stable_content"] is True


def test_unprotected_countermodel() -> None:
    cm = unprotected_unstable()
    assert cm == {
        "before_separated_unprotected": True,
        "refinement_accepted": True,
        "after_broken_unprotected": True,
        "protected_pair_now_separated": True,
        "protected_stable_content_intact": True,
    }


def test_sample_states_shapes() -> None:
    s0, s1, s2, s3 = sample_states(3)
    assert s0.obs == ()
    assert s1.obs == ((0,),)
    assert s2.obs == ((0,), (1,))
    # the refinement fired from s1 (obstruction discharged while
    # every protected separation is preserved)
    assert s3 != s1
    assert s3.obs == ((2, 0),)
    # quiescence flips as observation grows
    assert not quiescent_p(s0, 3)
    assert quiescent_p(s2, 3)
    assert quiescent_p(s3, 3)
    assert quiescent_p(s3, 3) == all(
        stable_sep(s3, i, j)
        for (i, j) in s3.prot if (i, j) in s3.wit)


def test_battery_covers_every_kind() -> None:
    kinds = {e[0] for e in event_battery(3)}
    assert kinds == {"declareObs", "setBudget", "setLicense",
                     "admitOcc", "assertWit", "admitWit", "protect",
                     "refuse", "addCol", "refineCol", "halt"}
    # halted states keep their stable content too
    s = sample_states(3)[3]
    h = pstep(s, ("halt",))
    for i in range(3):
        for j in range(3):
            assert stable_sep(h, i, j) == stable_sep(s, i, j)


def test_runner_includes_stable_content(tmp_path: object) -> None:
    import run_primitive_passage
    from pathlib import Path
    import json

    d = tmp_path if isinstance(tmp_path, Path) else Path(str(tmp_path))
    assert run_primitive_passage.main(
        ["--artifacts", str(d), "--rounds", "3"]) == 0
    payload = json.loads(
        (d / "primitive_passage.json").read_text(encoding="utf-8"))
    sc = payload["stable_content"]
    assert sc["stable_content_persists_battery"] is True
    assert sc["quiescence_iff_protected_in_stable_content"] is True
    cm = sc["unprotected_separation_unstable"]
    assert cm["after_broken_unprotected"] is True
