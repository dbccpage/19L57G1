"""Check script for Unit 66: Every step is idempotent, and that is almost all the algebra there is (TraceAlgebra).

Recomputes and verifies:
  1. Identity report (step normal form, all-state idempotence, inertness criterion,
     terminal absorption across 110,592 state-event pairs).
  2. Typed trace erasure report, commutation matrix report, and frame soundness/tightness report.
  3. Internal trace report, scoping report, and rewrite report (soundness, termination,
     confluence, unique normal form, and incompleteness witness).
  4. Student exercise verification on l and l'.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primitive_passage import PEvent, preplay  # noqa: E402
from derivation.trace_algebra import (  # noqa: E402
    commutation_report,
    frame_report,
    identity_report,
    internal_report,
    named_states,
    nf,
    no_redex,
    rewrite_report,
    scoping_report,
    trace_report,
)


def main() -> int:
    failures: list[str] = []

    ident = identity_report()
    if (
        ident["step_normal_form_failures"] != 0
        or ident["idempotence_failures"] != 0
        or ident["inertness_criterion_failures"] != 0
        or ident["terminal_absorption_failures"] != 0
        or not ident["every_event_idempotent"]
    ):
        failures.append(f"identity_report failed: {ident}")

    tr = trace_report()
    if not (
        tr["legal_trace"]
        and tr["replay_erases"]
        and tr["raw_history_same_end_state"]
    ):
        failures.append(f"trace_report failed: {tr}")

    comm = commutation_report()
    if comm["unordered_pairs"] != 153:
        failures.append(f"expected 153 unordered pairs, got {comm['unordered_pairs']}")

    frm = frame_report()
    if frm["frames_violated"] != 0 or frm["frames_verified"] != 20:
        failures.append(f"frame_report failed: {frm}")

    inter = internal_report()
    if not (
        inter["internal_trace_preserves_occurrences"]
        and inter["internal_trace_preserves_license"]
        and inter["refusal_is_accepted"]
        and inter["refusal_survives_every_event"]
        and inter["refusal_survives_terminal"]
    ):
        failures.append(f"internal_report failed: {inter}")

    scop = scoping_report()
    if not (scop["equivalent_on_scope"] and scop["equivalent_at_genesis"] is False):
        failures.append(f"scoping_report failed: {scop}")

    rw = rewrite_report(max_len=3)
    if (
        rw["soundness_failures"] != 0
        or rw["termination_failures"] != 0
        or rw["confluence_failures"] != 0
        or rw["normal_form_fixpoint_failures"] != 0
        or not rw["incompleteness_witness"]["same_replay_everywhere"]
        or rw["incompleteness_witness"]["identified_by_rewriting"] is not False
    ):
        failures.append(f"rewrite_report failed: {rw}")

    # Student exercise verification
    l_ex: list[PEvent] = [
        ("setBudget", 1),
        ("setBudget", 1),
        ("addCol", (0,)),
        ("addCol", (0,)),
        ("halt",),
        ("admitOcc", 9),
    ]
    nf_ex = nf(l_ex)
    expected_nf: list[PEvent] = [("setBudget", 1), ("addCol", (0,)), ("halt",)]
    if nf_ex != expected_nf or not no_redex(nf_ex):
        failures.append(f"unexpected nf(l_ex): {nf_ex}")
    l_prime: list[PEvent] = [
        ("setBudget", 2),
        ("setBudget", 1),
        ("addCol", (0,)),
        ("halt",),
    ]
    if nf(l_prime) == nf_ex:
        failures.append("expected nf(l_prime) != nf(l_ex)")
    for s in named_states():
        if preplay(l_ex, s) != preplay(nf_ex, s) or preplay(l_prime, s) != preplay(nf_ex, s):
            failures.append(f"replay mismatch on exercise lists at {s}")

    result = {
        "unit": 66,
        "module": "TraceAlgebra",
        "identity_pairs_checked": ident["pairs_checked"],
        "commuting_pairs_count": len(comm["commuting_pairs"]),
        "non_commuting_pairs_count": len(comm["non_commuting_pairs"]),
        "frames_verified": frm["frames_verified"],
        "rewrite_lists_checked": rw["lists_checked"],
        "exercise_nf": [list(e) for e in nf_ex],
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
