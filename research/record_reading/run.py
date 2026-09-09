"""Write and check this family's record: ``evidence/record.json``.

AuthorityEffect: None.  ``--write`` creates the record deliberately;
``--check`` recomputes it and compares bytes.  The record carries no
timestamps and no machine-specific paths.  It names the setting identified
from the represented execution family's artifact (read through the coherent
process limits family, never written here), the record-reading runs with
their operation tables in index order, the exhibited reading of the record
and its disappearance, the memoryless class that cannot produce it, the
lifted memoryless program, and the selection experiment: the protocol
declared before the readout, the survivors of both classes, the greedy
burden, the residual and its reason, the exhibited ambiguity and the
exhibited discrimination.

The receipt refuses a setting whose tables in index order are not the
transcribed ones the Lean programs are stated on, a recorded run any of
whose transitions is not a reference step at the recorded previous datum, a
clock that does not count the firings, a seen observation of the wrong
scale, a class none of whose laws replays it, and an exhibited pair that
does not survive.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import cast

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RECEIPT = ROOT / "evidence" / "record.json"
JsonObj = dict[str, object]

# This tree's own directory stays first on the path: the sibling families
# also have a ``run.py`` and a ``verify_sources.py``.  The consumed trees go
# immediately after it and never at the end: appended, they would sit behind
# ``PYTHONPATH`` and site-packages, and a same-named module found there would
# compute this record while the pins still passed.
sys.path[1:1] = [str(dependency) for dependency in
                 (REPO / "code", REPO / "research" / "setting_translation",
                  REPO / "research" / "represented_execution",
                  REPO / "research" / "coherent_process_limits")
                 if str(dependency) not in sys.path]

from verify_sources import PACKET, verify_sources  # noqa: E402

if PACKET != Path("research/record_reading"):
    raise RuntimeError(f"wrong custody guard imported: {PACKET}")

import control as ct  # noqa: E402
import limits as lm  # noqa: E402
import record as rc  # noqa: E402
import selection as sel  # noqa: E402


def record_run(name: str, C: rc.Recorded, start: int, fuel: int) -> JsonObj:
    terminal, s = rc.rtrace(C, start, fuel)
    tape = s.tape
    for i in range(1, len(tape)):
        p = tape[i - 2] if i >= 2 else tape[i - 1]
        x, y = tape[i - 1], tape[i]
        if not any(rc.rstep(C, p, x, k, y) for k in range(len(C.F.ops))):
            raise RuntimeError(f"{name}: the transition {x} -> {y} after {p} is not a reference step")
    if s.clock != len(tape) - 1 or s.clock + s.fuel != fuel:
        raise RuntimeError(f"{name}: the clock does not count the firings")
    return {
        "program": name,
        "setting_json": C.F.json(),
        "ops_in_index_order": [list(g) for g in C.F.ops],
        "enablements": sorted(list(triple) for triple in C.hctrl),
        "enablement_meaning": "[previous, active, k]: operation k may fire at the active datum when the datum "
                              "before it on the record is previous; represented as the instance "
                              "(3 + nops + k, [previous, active])",
        "start": start,
        "fuel": fuel,
        "terminal": terminal.value,
        "tape": list(tape),
        "clock": s.clock,
        "fuel_left": s.fuel,
        "previous_at_end": rc.previous(s),
        "successors_at_end": sorted(t.active for t in rc.rsuccessors(s)),
    }


def record() -> JsonObj:
    artifact = lm.load_artifact()
    programs, finding = lm.identify_programs(artifact)
    forever = programs["forever"]
    F = forever.F
    rc.check_base(F)
    runs = cast(list[lm.JsonObj], artifact["control_runs"])
    recorded = tuple(int(v) for v in cast(list[int], next(r for r in runs if r["program"] == "forever")["tape"]))
    observation = recorded[: sel.OBSERVED_SCALE + 1]
    twist, turncoat, lifted = rc.twist(F), rc.turncoat(F), rc.lift(forever)
    twist_run = rc.rinit(twist, 0, 3)
    actives = [rc.riter(n, twist_run).active for n in range(4)]
    memoryless = lm.deterministic_programs(F)
    forgotten = rc.forget(twist)
    forgotten_terminal, forgotten_state = ct.trace(forgotten, 0, 3)
    return {
        "schema_version": 1,
        "classification": "deterministic computation: the record-reading machine over the sealed encoding, "
                          "and the selection experiment on the represented process",
        "authority_effect": "None",
        "config_status": "DECLARED_HOST_CONFIG",
        "artifact": {
            "path": "research/represented_execution/evidence/process.json",
            "authored_by": "research/represented_execution",
            "read_through": "research/coherent_process_limits (limits.identify_programs)",
            "written_here": False,
            "finding_inherited": finding,
            "repair_here": "every run below records its operation tables in index order (ops_in_index_order)",
        },
        "record_reading": {
            "reference": "Record.RStep",
            "program": "Record.rprogram; well-formed regime Record.encodeR_wf",
            "read": "Record.renabled: the presence of the instance (3 + nops + k, [previous, active]); "
                    "Record.previous: the entry before the last on the record",
            "read_faithfully": "Record.renabled_rprogram",
            "record_is_what_the_process_wrote": "Record.previous_fire: after a firing the datum the step left "
                                                "is the previous the next enablement reads",
            "soundness": "Record.rsuccessors_sound",
            "completeness": "Record.rsuccessors_complete",
            "never_selects": "Record.rrun_branch",
            "only_appends": "Record.robs_prefix",
            "memoryless_embeds": "Record.lift, Record.lift_RStep, Record.lift_renabled",
        },
        "record_runs": [
            record_run("twist", twist, 0, 3),
            record_run("twist", twist, 0, 6),
            record_run("twist", twist, 1, 4),
            record_run("twist", twist, 2, 4),
            record_run("turncoat", turncoat, 0, 6),
            record_run("turncoat", turncoat, 2, 6),
            record_run("liftForever", lifted, 0, 6),
        ],
        "record_is_read": {
            "program": "twist",
            "actives_by_step": actives,
            "same_datum_at_steps": [0, 2],
            "left_towards": [actives[1], actives[3]],
            "meaning": "at its third step the run is at the datum it started from and moves elsewhere than "
                       "the first time: the enablement read the record (Record.record_is_read)",
            "memoryless_cannot": "a run of the merged machine that returns to a datum leaves it the same way "
                                 "(Record.memoryless_functional)",
            "memoryless_class_checked": {
                "class": "every program on the identified setting with at most one operation enabled per "
                         "datum, from every datum, at fuel 3",
                "programs": len(memoryless),
                "tape_0_1_0_0_realized": any(ct.trace(C, x, 3)[1].tape == (0, 1, 0, 0)
                                             for C in memoryless for x in range(F.n)),
                "tape_is_functional": lm.functional((0, 1, 0, 0)),
            },
        },
        "forget": {
            "projection": sorted(list(pair) for pair in forgotten.ctrl),
            "meaning": "the record forgotten: the enablement read at the datum as its own predecessor",
            "tape": list(forgotten_state.tape),
            "terminal": forgotten_terminal.value,
            "distinction_disappears": forgotten_state.tape != (0, 1, 0, 0),
        },
        "lift": {
            "program": "liftForever",
            "agrees_with_forever_at_every_declared_input": all(
                sel.observe(lifted, x, n) == sel.observe(forever, x, n) for x in sel.STARTS for n in sel.SCALES),
        },
        "selection": sel.experiment(F, observation, forever),
        "not_delivered": [
            "a record read deeper than one entry: the enablement reads the previous datum only",
            "an encoded configuration: the state is a declared host record",
            "an observable that reads which operation fired: the residual of the selection experiment is "
            "exactly what such an observable would separate",
            "a second locus of activity",
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
        print("WROTE: deterministic record")
        return 0
    if not RECEIPT.is_file() or RECEIPT.read_bytes() != fresh:
        print("FAIL: evidence/record.json differs from fresh computation")
        return 1
    print("PASS: source pins, the artifact consumed, the runs and the experiment replayed, and record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
