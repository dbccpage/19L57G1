"""Produce the trace-algebra artifact deterministically.

Usage: python code/run_trace_algebra.py [--artifacts DIR] [--max-len N]

Writes ``trace_algebra.json``: the step normal form, the exact
inertness criterion, terminal absorption and universal idempotence,
all checked exhaustively over the declared state space; a typed
transition trace from genesis with its erasure/replay agreement; the
full ordered commutation matrix with the smallest witness for every
non-commuting pair; the three frame conditions with their soundness
and tightness audit; what an internal trace cannot do and why the
budget claim is not made; the non-erasability of a refusal record; the
scoping of replay equivalence with its unscoped countermodel; and the
two-rule rewrite system with soundness, termination, confluence and
its incompleteness witness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.trace_algebra import (
    REWRITE_ALPHABET,
    commutation_report,
    frame_report,
    identity_report,
    internal_report,
    named_states,
    rewrite_report,
    scoping_report,
    trace_report,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--max-len", type=int, default=3)
    args = parser.parse_args(argv)
    payload: dict[str, Json] = {
        "bounds": {
            "max_rewrite_list_length": args.max_len,
            "rewrite_alphabet": len(REWRITE_ALPHABET),
            "rewrite_soundness_states": len(named_states()),
        },
        "imported_inputs": [
            "the sealed passage step function and its guards",
            "the effect-class table of the transition alphabet",
            "the environment/internal ownership declaration",
            "the declared well-formed class",
        ],
        "scope": {
            "commutation": ("checked over the declared commutation "
                            "battery; the frame theorems are universal "
                            "in Lean, the countermodels are concrete"),
            "rewriting": ("sound at every start state, but far weaker "
                          "than replay equivalence, which is itself "
                          "state-relative"),
        },
        "identity": identity_report(),
        "trace": trace_report(),
        "commutation": commutation_report(),
        "frames": frame_report(),
        "internal": internal_report(),
        "scoping": scoping_report(),
        "rewriting": rewrite_report(args.max_len),
    }
    out_path = args.artifacts / "trace_algebra.json"
    write_json(out_path, payload)
    ident = payload["identity"]
    assert isinstance(ident, dict)
    print(f"identity: pairs={ident['pairs_checked']} "
          f"normal_form_fail={ident['step_normal_form_failures']} "
          f"idempotent={ident['every_event_idempotent']} "
          f"absorb_fail={ident['terminal_absorption_failures']}")
    comm = payload["commutation"]
    assert isinstance(comm, dict)
    commuting = comm["commuting_pairs"]
    failing = comm["non_commuting_pairs"]
    assert isinstance(commuting, list) and isinstance(failing, list)
    print(f"commutation: pairs={comm['unordered_pairs']} "
          f"commuting={len(commuting)} non_commuting={len(failing)}")
    frames = payload["frames"]
    assert isinstance(frames, dict)
    print(f"frames: verified={frames['frames_verified']} "
          f"violated={frames['frames_violated']}")
    rw = payload["rewriting"]
    assert isinstance(rw, dict)
    print(f"rewriting: lists={rw['lists_checked']} "
          f"sound_fail={rw['soundness_failures']} "
          f"terminating={rw['termination_failures'] == 0} "
          f"confluent={rw['confluence_failures'] == 0}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
