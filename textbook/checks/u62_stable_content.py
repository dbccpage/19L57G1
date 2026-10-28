"""Standalone verification for Textbook Unit 62: What protection buys.

Usage: python textbook/checks/u62_stable_content.py

Imports ``code/derivation/stable_content.py``, checks ``stable_content_report(3)``
against ``artifacts/primitive_passage.json["stable_content"]``, and verifies the
genesis-reachable halted and live-unfunded countermodels (from
``textbook/audit/probes/F1/sc_reachable_witness.lean``) plus the 5-event
continuation that breaks the unprotected separation ``(0, 1)`` from the
genesis-reachable live-unfunded state once ``setBudget 1`` leaves the
restricted fragment.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primitive_passage import (  # noqa: E402
    GENESIS_P,
    PEvent,
    obst_p,
    preplay,
    pstep,
    refine_ok,
    sep_p,
)
from derivation.stable_content import (  # noqa: E402
    event_battery,
    halted_countermodel,
    is_trace_excluded_event,
    persistence_check,
    prot_sep,
    quiescence_check,
    quiescent_p,
    replay_persistence_check,
    stable_content_report,
    unfunded_countermodel,
    unprotected_unstable,
)


def exercise_reachable_witnesses() -> dict[str, object]:
    """Build genesis-reachable live-unfunded and halted states carrying an
    unprotected separation of (0, 1) alongside a protected separation of (1, 2),
    then break (0, 1) from the live-unfunded state via setBudget + refineCol."""
    hist_live: list[PEvent] = [
        ("admitOcc", 0),
        ("admitOcc", 1),
        ("admitOcc", 2),
        ("assertWit", 1, 2),
        ("admitWit", 1, 2),
        ("protect", 1, 2),
        ("declareObs",),
        ("setBudget", 1),
        ("addCol", (1,)),
    ]
    s_live = preplay(hist_live, GENESIS_P)
    s_halt = pstep(s_live, ("halt",))

    assert s_live.obs is not None and s_halt.obs is not None

    battery = event_battery(3)
    restricted = [e for e in battery if not is_trace_excluded_event(e)]

    live_restricted_inert = all(
        pstep(s_live, e).obs == s_live.obs and pstep(s_live, e).budget == 0
        for e in restricted
    )
    halt_all_inert = all(pstep(s_halt, e) == s_halt for e in battery)

    # Now leave the restricted fragment from s_live by funding and protecting (0, 2),
    # then refining column (1,) with 0 -> (0, 1), which separates (0, 2) and (1, 2)
    # while destroying the unprotected separation of (0, 1).
    break_tail: list[PEvent] = [
        ("setBudget", 1),
        ("assertWit", 0, 2),
        ("admitWit", 0, 2),
        ("protect", 0, 2),
    ]
    s_pre_refine = preplay(break_tail, s_live)
    can_refine = (
        not s_pre_refine.halted
        and s_pre_refine.budget == 1
        and refine_ok(s_pre_refine, (1,), 0)
        and obst_p(s_pre_refine, 0, 2)
    )
    s_broken = pstep(s_pre_refine, ("refineCol", (1,), 0))
    assert s_broken.obs is not None

    return {
        "live_obs": s_live.obs,
        "live_prot": s_live.prot,
        "live_budget": s_live.budget,
        "live_halted": s_live.halted,
        "live_01_separated_unprotected": (
            sep_p(s_live.obs, 0, 1) and not prot_sep(s_live, 0, 1)
        ),
        "live_12_protected_separated": prot_sep(s_live, 1, 2),
        "live_quiescent": quiescent_p(s_live, 3),
        "live_restricted_inert": live_restricted_inert,
        "halt_all_inert": halt_all_inert,
        "halt_01_separated_unprotected": (
            sep_p(s_halt.obs, 0, 1) and not prot_sep(s_halt, 0, 1)
        ),
        "can_refine_from_live_continuation": can_refine,
        "broken_obs": s_broken.obs,
        "broken_01_destroyed": not sep_p(s_broken.obs, 0, 1),
        "broken_12_preserved": prot_sep(s_broken, 1, 2),
        "broken_02_now_protected_separated": prot_sep(s_broken, 0, 2),
        "broken_quiescent": quiescent_p(s_broken, 3),
    }


def main() -> int:
    failures: list[str] = []

    report = stable_content_report(3)
    if not report["sufficiency_single_step"]:
        failures.append("persistence_check(3) failed")
    if not report["sufficiency_along_traces"]:
        failures.append("replay_persistence_check(3, 2) failed")
    if not report["quiescence_iff_protected_separated"]:
        failures.append("quiescence_check(3) failed")

    hm = halted_countermodel()
    if not hm["trace_stable_but_unprotected"]:
        failures.append(f"halted_countermodel failed: {hm}")

    um = unfunded_countermodel()
    if not um["restricted_stable_but_unprotected"]:
        failures.append(f"unfunded_countermodel failed: {um}")

    uu = unprotected_unstable()
    if not (
        uu["before_separated_unprotected"]
        and uu["refinement_accepted"]
        and uu["after_broken_unprotected"]
        and uu["protected_pair_now_separated"]
        and uu["protected_separation_intact"]
    ):
        failures.append(f"unprotected_unstable failed: {uu}")

    ex = exercise_reachable_witnesses()
    if not (
        ex["live_obs"] == ((1,),)
        and ex["live_prot"] == ((1, 2),)
        and ex["live_budget"] == 0
        and not ex["live_halted"]
        and ex["live_01_separated_unprotected"]
        and ex["live_12_protected_separated"]
        and ex["live_quiescent"]
        and ex["live_restricted_inert"]
        and ex["halt_all_inert"]
        and ex["halt_01_separated_unprotected"]
        and ex["can_refine_from_live_continuation"]
        and ex["broken_obs"] == ((0, 1),)
        and ex["broken_01_destroyed"]
        and ex["broken_12_preserved"]
        and ex["broken_02_now_protected_separated"]
        and ex["broken_quiescent"]
    ):
        failures.append(f"reachable witness exercise failed: {ex}")

    art_path = ROOT / "artifacts" / "primitive_passage.json"
    art = json.loads(art_path.read_text(encoding="utf-8"))
    if art.get("stable_content") != report:
        failures.append(
            "artifacts/primitive_passage.json['stable_content'] mismatch with stable_content_report(3)"
        )

    print(
        f"Unit 62 StableContent check: sufficiency_step={report['sufficiency_single_step']}; "
        f"sufficiency_traces={report['sufficiency_along_traces']}; "
        f"quiescence_iff={report['quiescence_iff_protected_separated']}; "
        f"reachable_live_obs={ex['live_obs']}; "
        f"broken_obs={ex['broken_obs']}; "
        f"failures={failures}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
