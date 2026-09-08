"""Write and check the artifact Target B consumes: ``evidence/process.json``.

AuthorityEffect: None.  ``--write`` creates the record deliberately;
``--check`` recomputes it and compares bytes.  The record carries no
timestamps and no machine-specific paths.  It names the fragment commit 1
delivers (``words``), the machine's `Step` and `run`, the correspondence
theorem, the configuration status, how a run is observed, and a set of
recorded word-runs.  The receipt refuses to record a run whose active datum
differs from what the operations compute — the merged ``translation.run``,
which reads the operation tables and which this *check* may consult; the
machine never does — or whose word is not consumed.
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


def record() -> JsonObj:
    return {
        "schema_version": 1,
        "classification": "deterministic computation: the configuration machine over the sealed encoding",
        "authority_effect": "None",
        "fragment": "words",
        "config_status": "DECLARED_HOST_CONFIG",
        "config_status_meaning": "Config is a metatheory record whose graph field is a copy of the encoded "
                                 "instances; the process reads encoded data and does not itself live in the "
                                 "sealed grammar.",
        "step": "Execution.step",
        "run": "Execution.run",
        "iterate": "Execution.iterate",
        "reference": "Execution.evalWord",
        "correspondence": "Execution.run_encode",
        "totality": "Execution.run_total",
        "concatenation": "Execution.run_append",
        "observation": {
            "active": "the final active datum, a member of the carrier",
            "output": "the tape of data visited, one entry per letter consumed",
        },
        "word": "a list of operation indices; step reads the edge of form 3 + k leaving the active datum",
        "runs": [word_run(*entry) for entry in RUNS],
        "not_delivered": ["control", "branching", "iteration", "retained record", "semantic_clock",
                          "resource ledger"],
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
    print("PASS: source pins, recorded word-runs against the operations, and record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
