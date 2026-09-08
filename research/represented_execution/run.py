"""Write and check the artifact Target B consumes: ``evidence/process.json``.

AuthorityEffect: None.  ``--write`` creates the record deliberately;
``--check`` recomputes it and compares bytes.  The record carries no
timestamps and no machine-specific paths.  It names the fragment delivered
(``control``: the word machine of commit 1 and the data-driven machine of
commit 2), the machines' `Step`, `run` and reference, the correspondence
theorems, the configuration status, how a run is observed, recorded
word-runs, a branching example, an iteration example, the live class, and
the exact list of what is not delivered.

The receipt refuses to record a word-run whose active datum differs from
what the operations compute — the merged ``translation.run``, which reads
the operation tables and which this *check* may consult; the machines never
do — or whose word is not consumed; and a controlled run any of whose
transitions is not a reference step (``control.cstep``, likewise a check).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import cast

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RECEIPT = ROOT / "evidence" / "process.json"
JsonObj = dict[str, object]

# This tree's own directory stays first on the path: the merged sibling also
# has a ``run.py`` and a ``verify_sources.py``, and an import that resolved
# to the sibling would run the wrong custody guard silently.
for dependency in (REPO / "code", REPO / "research" / "setting_translation"):
    if str(dependency) not in sys.path:
        sys.path.append(str(dependency))

from verify_sources import PACKET, verify_sources  # noqa: E402

if PACKET != Path("research/represented_execution"):
    raise RuntimeError(f"wrong custody guard imported: {PACKET}")

import control as ct  # noqa: E402
import execution as ex  # noqa: E402
import translation as tr  # noqa: E402

# A three-point setting with two distinct operations: reading the letter and
# reading the graph both matter.
TWO_OPS = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 2, 0), (0, 0, 0)))

RUNS: tuple[tuple[str, tr.FiniteSetting, tuple[int, ...], int], ...] = (
    ("twoOps", TWO_OPS, (0, 1, 0, 0), 0),
    ("twoOps", TWO_OPS, (0, 0, 0), 0),
    ("twoOps", TWO_OPS, (), 2),
    ("d2Merged", tr.SEALED_SETTINGS["d2Merged"], (0, 0), 1),
    ("boolEmptyMerged", tr.SEALED_SETTINGS["boolEmptyMerged"], (0,), 1),
    ("s2Merged", tr.SEALED_SETTINGS["s2Merged"], (0, 0, 0), 0),
)

# Controlled settings on a three-point carrier with three operations: the
# cycle 0 -> 1 -> 2 -> 0, the constant 0, and the climb 0 -> 1 -> 2 -> 2.
CYCLE, ZERO, SUCC = (1, 2, 0), (0, 0, 0), (1, 2, 2)
BASE = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, (CYCLE, ZERO, SUCC))
PING = ct.Controlled(BASE, frozenset({(0, 0), (1, 1)}))
CLIMB = ct.Controlled(BASE, frozenset({(0, 2), (1, 2)}))
FOREVER = ct.Controlled(BASE, frozenset({(0, 0), (1, 0), (2, 0)}))
FORK = ct.Controlled(BASE, frozenset({(0, 0), (0, 1)}))

CONTROL_RUNS: tuple[tuple[str, ct.Controlled, int, int], ...] = (
    ("ping", PING, 0, 4),
    ("ping", PING, 1, 4),
    ("ping", PING, 2, 4),
    ("climb", CLIMB, 0, 10),
    ("climb", CLIMB, 1, 10),
    ("climb", CLIMB, 2, 10),
    ("forever", FOREVER, 0, 5),
    ("fork", FORK, 0, 5),
)


def word_run(name: str, F: tr.FiniteSetting, word: tuple[int, ...], start: int) -> JsonObj:
    c = ex.run(ex.init(F, word, start))
    if c is None:
        raise RuntimeError(f"{name}: the machine refused a well-formed word")
    reference = tr.run(F, word, start)
    if c.active != reference:
        raise RuntimeError(f"{name}: the machine's active datum {c.active} is not the operations' {reference}")
    if c.word != ():
        raise RuntimeError(f"{name}: the word was not consumed")
    return {
        "setting": name,
        "setting_json": F.json(),
        "start": start,
        "word": list(word),
        "active": c.active,
        "output": list(c.output),
        "reference_active": reference,
    }


def control_run(name: str, C: ct.Controlled, start: int, fuel: int) -> JsonObj:
    terminal, s = ct.trace(C, start, fuel)
    for x, y in zip(s.tape, s.tape[1:]):
        if not any(ct.cstep(C, x, k, y) for k in range(ct.nops(C))):
            raise RuntimeError(f"{name}: the transition {x} -> {y} is not a reference step")
    if s.clock != len(s.tape) - 1 or s.clock + s.fuel != fuel:
        raise RuntimeError(f"{name}: the clock does not count the firings")
    return {
        "program": name,
        "setting_json": C.F.json(),
        "enablements": sorted(list(pair) for pair in C.ctrl),
        "start": start,
        "fuel": fuel,
        "terminal": terminal.value,
        "tape": list(s.tape),
        "clock": s.clock,
        "fuel_left": s.fuel,
        "successors_at_end": sorted(t.active for t in ct.successors(s)),
    }


def record() -> JsonObj:
    ping = {x: ct.trace(PING, x, 4)[1].tape for x in range(3)}
    climb = {x: ct.trace(CLIMB, x, 10) for x in range(3)}
    return {
        "schema_version": 2,
        "classification": "deterministic computation: the word machine and the data-driven machine over "
                          "the sealed encoding",
        "authority_effect": "None",
        "fragment": "control",
        "config_status": "DECLARED_HOST_CONFIG",
        "config_status_meaning": "Config and State are metatheory records whose graph fields are copies of "
                                 "encoded instances; the processes read encoded data and do not themselves "
                                 "live in the sealed grammar.  The represented program of a controlled "
                                 "setting is itself a well-formed regime (Control.encodeC_wf).",
        "words": {
            "step": "Execution.step",
            "run": "Execution.run",
            "iterate": "Execution.iterate",
            "reference": "Execution.evalWord",
            "correspondence": "Execution.run_encode",
            "totality": "Execution.run_total",
            "concatenation": "Execution.run_append",
            "word": "a list of operation indices; step reads the edge of form 3 + k leaving the active datum",
        },
        "control": {
            "step": "Control.stepDet",
            "fire": "Control.fire",
            "successors": "Control.successors",
            "run": "Control.run",
            "reference": "Control.CStep",
            "soundness": "Control.successors_sound",
            "completeness": "Control.successors_complete",
            "well_formed_program": "Control.encodeC_wf",
            "enablement_read_faithfully": "Control.enabled_program",
            "never_selects": "Control.run_branch",
            "non_stuck_on_the_live_class": "Control.live_successor",
            "clock": "advances exactly when an operation edge is applied (Control.fire_ok); the machine has "
                     "no administrative step",
            "fuel": "a represented field, spent by one per firing (Control.fire_ok), renewed by nothing "
                    "(Control.fire_exhausted)",
            "terminals": ["halt", "exhausted", "refuse", "branch"],
            "program": "operation graphs and enablements; the enablement of operation k at datum x is the "
                       "self-instance (3 + nops + k, [x, x]); the stores are not loaded",
            "pair": "the initial state does not depend on the designated pair (Control.init_pair)",
        },
        "observation": {
            "active": "the final active datum, a member of the carrier",
            "output": "the tape of data visited, one entry per firing (the words machine: one per letter)",
        },
        "live_class": "Control.Live: an admitted active datum with an enabled operation and fuel",
        "branching_example": {
            "program": "ping",
            "meaning": "at datum 0 the cycle is enabled, at datum 1 the constant map, at datum 2 nothing: "
                       "which operation fires is read from the data",
            "tapes_by_start": {str(x): list(t) for x, t in ping.items()},
        },
        "iteration_example": {
            "program": "climb",
            "meaning": "the climb is enabled at 0 and 1 and nothing at 2: the run halts after a number of "
                       "firings set by the start datum, not by the interpreter",
            "firings_by_start": {str(x): climb[x][1].clock for x in range(3)},
            "terminals_by_start": {str(x): climb[x][0].value for x in range(3)},
        },
        "runs": [word_run(*entry) for entry in RUNS],
        "control_runs": [control_run(*entry) for entry in CONTROL_RUNS],
        "not_delivered": [
            "a retained record that a later operation reads: the tape is retained and observable, but no "
            "enablement reads it, so two states with one active datum and different tapes have one future",
            "represented storage growth beyond the tape",
            "an encoded configuration: the state is a declared host record",
        ],
    }


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    result = record()
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed after replay: " + "; ".join(failures))
    return (json.dumps(result, sort_keys=True, indent=1) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true", help="deliberately create the record")
    args = parser.parse_args(argv)
    fresh = receipt_bytes()
    if args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_bytes(fresh)
        print("WROTE: deterministic process record")
        return 0
    if not RECEIPT.is_file() or RECEIPT.read_bytes() != fresh:
        print("FAIL: evidence/process.json differs from fresh computation")
        return 1
    print("PASS: source pins, recorded runs against the operations, and record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
