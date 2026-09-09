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

Every run carries ``ops_in_index_order``.  Its ``setting_json`` is the sealed
``Setting.json``, whose ``ops`` field is set-valued: the tables are sorted
and repetitions collapsed, so the index order the words and enablements refer
to is not recoverable from that field alone.  The index-ordered list is what
a consumer replays with; ``tests/test_evidence.py`` replays every recorded
run from its own record through it.
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
# to the sibling would run the wrong custody guard silently.  The consumed
# trees go immediately after it and never at the end: appended, they would
# sit behind ``PYTHONPATH`` and site-packages, and a same-named module found
# there would compute this record while the pins still passed.
sys.path[1:1] = [str(dependency) for dependency in (REPO / "code", REPO / "research" / "setting_translation")
                 if str(dependency) not in sys.path]

from verify_sources import PACKET, verify_sources  # noqa: E402

if PACKET != Path("research/represented_execution"):
    raise RuntimeError(f"wrong custody guard imported: {PACKET}")

import control as ct  # noqa: E402
import execution as ex  # noqa: E402
import product as pr  # noqa: E402
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

# Two loci on one carrier: two two-point settings, the flip at each, and a
# schedule that names which locus moves at each datum.  The schedule reads
# both coordinates, which is what a schedule may do and an operation may not.
FLIP = (1, 0)
TWO = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, (FLIP,))


def alt(x: int) -> int:
    """Move the first locus when the two loci agree, the second when they differ."""
    return 0 if pr.fst_of(2, x) == pr.snd_of(2, x) else 1


def alt_mirror(x: int) -> int:
    """The same alternation begun at the other locus."""
    return 1 if pr.fst_of(2, x) == pr.snd_of(2, x) else 0


PAIR = pr.two_locus(TWO, TWO, alt)
PAIR_MIRROR = pr.two_locus(TWO, TWO, alt_mirror)
SOLO = pr.scheduled(TWO, lambda _: 0)

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
        "ops_in_index_order": [list(g) for g in F.ops],
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
        "ops_in_index_order": [list(g) for g in C.F.ops],
        "enablements": sorted(list(pair) for pair in C.ctrl),
        "start": start,
        "fuel": fuel,
        "terminal": terminal.value,
        "tape": list(s.tape),
        "clock": s.clock,
        "fuel_left": s.fuel,
        "successors_at_end": sorted(t.active for t in ct.successors(s)),
    }


def two_locus_record() -> JsonObj:
    """The two-locus run, its mirror, and what each locus reads off the tape.

    The receipt refuses to record a schedule the runner had to choose in
    (a ``BRANCH`` terminal), a step that moved both loci at once, a
    projection that is not the locus's own run, two orders that disagree on
    the datum they reach, or two orders that agree on the tape.
    """
    forward, mirror = ct.trace(PAIR, 0, 4), ct.trace(PAIR_MIRROR, 0, 4)
    solo = ct.trace(SOLO, 0, 2)
    half_forward, half_mirror = ct.trace(PAIR, 0, 2), ct.trace(PAIR_MIRROR, 0, 2)
    for name, (terminal, state) in (("alternating", forward), ("mirror", mirror),
                                    ("solo", solo)):
        if terminal is ct.Terminal.BRANCH:
            raise RuntimeError(f"{name}: the runner was left a choice; the schedule is not in the data")
        if not pr.moves_one_locus(2, state.tape):
            raise RuntimeError(f"{name}: a step moved both loci at once")
    readings = {which: pr.locus(2, which, forward[1].tape) for which in (0, 1)}
    for which, reading in readings.items():
        if pr.destutter(reading) != solo[1].tape:
            raise RuntimeError(f"locus {which}: the destuttered projection is not that locus's own run")
    if half_forward[1].active != half_mirror[1].active:
        raise RuntimeError("the two orders reach different data: the square fails of the outcome")
    if half_forward[1].tape == half_mirror[1].tape:
        raise RuntimeError("the two orders record the same tape: there is nothing for the order to be")
    return {
        "carrier": "pairs over two two-point loci, packed as m * a + b (Product.pack)",
        "setting_json": PAIR.F.json(),
        "ops_in_index_order": [list(g) for g in PAIR.F.ops],
        "schedule": {
            "alternating": {str(x): alt(x) for x in range(4)},
            "mirror": {str(x): alt_mirror(x) for x in range(4)},
            "carried_by": "enablement self-instances, exactly as for any controlled setting",
            "never_selects": "Schedule.enabledAt_scheduled, Schedule.scheduled_no_branch: at every datum "
                             "the enabled list is a singleton, so the interpreter has nothing to choose "
                             "and the two-locus run needs no host scheduler",
            "reads_both_loci": "a schedule may, and an operation may not: Product.coupling_breaks_the_square",
        },
        "alternating_run": {"tape": list(forward[1].tape), "terminal": forward[0].value},
        "mirror_run": {"tape": list(mirror[1].tape), "terminal": mirror[0].value},
        "one_locus_at_a_time": {
            "holds": pr.moves_one_locus(2, forward[1].tape),
            "theorem": "Schedule.step_moves_one_locus, from Product.prod_left_local and prod_right_local",
            "failure_case": "Schedule.swap_moves_both: an operation at neither locus moves both in one "
                            "step, so this is a property of the product's operations and not of the machine",
        },
        "square": {
            "on_the_outcome": {
                "alternating": half_forward[1].active,
                "mirror": half_mirror[1].active,
                "agree": half_forward[1].active == half_mirror[1].active,
                "theorem": "Schedule.square_on_the_outcome; the operations commute by Product.prod_comm",
            },
            "on_the_observation": {
                "alternating": list(half_forward[1].tape),
                "mirror": list(half_mirror[1].tape),
                "agree": half_forward[1].tape == half_mirror[1].tape,
                "theorem": "Schedule.square_fails_on_the_observation",
                "reading": "the commutation is real and the record still distinguishes the orders: a tape "
                           "totally orders events that the loci do not",
            },
        },
        "projections": {
            "first_locus": list(readings[0]),
            "second_locus": list(readings[1]),
            "destuttered": {"first_locus": list(pr.destutter(readings[0])),
                            "second_locus": list(pr.destutter(readings[1]))},
            "one_locus_run": list(solo[1].tape),
            "theorem": "Schedule.locus1_is_its_own_run, Schedule.locus2_is_its_own_run",
            "reading": "what lifts to observations is the projection with the repeats dropped; the repeats "
                       "are exactly the steps that moved the other locus",
        },
    }


def record() -> JsonObj:
    ping = {x: ct.trace(PING, x, 4)[1].tape for x in range(3)}
    climb = {x: ct.trace(CLIMB, x, 10) for x in range(3)}
    # Evaluated here rather than inside the literal below, so that the order
    # in which the receipt's refusals can fire is the order they are written
    # in and not the order the keys happen to appear.
    runs = [word_run(*entry) for entry in RUNS]
    control_runs = [control_run(*entry) for entry in CONTROL_RUNS]
    two_loci = two_locus_record()
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
        "two_loci": two_loci,
        "runs": runs,
        "control_runs": control_runs,
        "not_delivered": [
            "a retained record that a later operation reads: the tape is retained and observable, but no "
            "enablement reads it, so two states with one active datum and different tapes have one future",
            "represented storage growth beyond the tape",
            "an encoded configuration: the state is a declared host record",
            "the two-locus run observed at step scales: the run and its projections are recorded here, "
            "but the inverse system over them is the observing family's to build",
            "a schedule that is not a function of the active datum: a run whose choice of locus depends "
            "on the tape would need the record-reading enablement, which is a different family's machine",
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
