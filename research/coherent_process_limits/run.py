"""Write and check this family's record: ``evidence/limits.json``.

AuthorityEffect: None.  ``--write`` creates the record deliberately;
``--check`` recomputes it and compares bytes.  The record carries no
timestamps and no machine-specific paths.  It names the artifact consumed
(the represented execution family's ``evidence/process.json``, read and
never written here), the programs identified from it and the finding that
its schema loses the operation order, the observation system and its
theorems, the limit and its declared topology, which threads the process
generates, the three verdicts, the failure pairs, and the connected
experiment at four scales.

The receipt refuses to record an artifact whose fragment is not ``control``,
programs the recorded runs do not identify uniquely, observations that are
not prefix-compatible, a recorded tape not prefix-related to the observed
run, and a bound that fails at any scale.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import cast

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RECEIPT = ROOT / "evidence" / "limits.json"
JsonObj = dict[str, object]

# This tree's own directory stays first on the path: the sibling families
# also have a ``run.py`` and a ``verify_sources.py``.
for dependency in (REPO / "code", REPO / "research" / "setting_translation",
                   REPO / "research" / "represented_execution"):
    if str(dependency) not in sys.path:
        sys.path.append(str(dependency))

from verify_sources import PACKET, verify_sources  # noqa: E402

if PACKET != Path("research/coherent_process_limits"):
    raise RuntimeError(f"wrong custody guard imported: {PACKET}")

import limits as lm  # noqa: E402


def record() -> JsonObj:
    artifact = lm.load_artifact()
    programs, finding = lm.identify_programs(artifact)
    runs = cast(list[JsonObj], artifact["control_runs"])
    recorded = tuple(int(v) for v in cast(list[int], next(r for r in runs if r["program"] == "forever")["tape"]))
    forever = programs["forever"]
    return {
        "schema_version": 1,
        "classification": "deterministic computation: the represented process observed at step scales, "
                          "and the abstract inverse system mirrored",
        "authority_effect": "None",
        "artifact": {
            "path": "research/represented_execution/evidence/process.json",
            "authored_by": "research/represented_execution",
            "written_here": False,
            "fragment": artifact["fragment"],
            "pinned_by_digest_in": "SOURCE_MANIFEST.json",
            "programs_identified": sorted(programs),
            "finding_for_the_represented_execution_family": finding,
        },
        "observation_system": {
            "scale": "the number of steps of the deterministic runner watched",
            "observation": "the tape after n steps (Observe.obs)",
            "bonding": "forget the entries beyond the coarser length",
            "compatibility_at_every_scale": "Observe.obs_prefix, Observe.obs_prefix_add",
            "why": "a step only appends (Control.fire_ok through Observe.next_tape)",
        },
        "limit": {
            "stages": "words of length n over the carrier (Limits.Stage)",
            "thread_space": "compatible families at every scale (Limits.Compatible, Limits.Thread)",
            "construction": "Limits.ofSeq; universal property Limits.ofSeq_toSeq and Limits.toSeq_ofSeq: "
                            "the thread space is the sequence space; no choice or compactness is used",
            "eventual_agreement_is_not_compatibility": "Limits.eventual_not_compatible, Limits.eventual_agrees",
            "cofinal_rescaling": "Limits.thread_even, Limits.even_thread: the even scales have the same threads",
            "topology": "declared, not proved: the product of the discrete topologies on the finite stages; "
                        "totally disconnected; not an interval, not a circle; none is claimed, and an "
                        "interval would need an order or metric compatible with the stages and an "
                        "identification of threads this family does not make",
        },
        "which_threads": {
            "all_mathematical_sequences": "the thread space is all of them (the construction is total)",
            "process_generated": "functional tapes — equal entries have equal successors "
                                 "(Observe.next_active_det) — hence eventually periodic on a finite carrier; "
                                 "a strict subset",
            "computably_presented": "between the two; not characterised here",
        },
        "verdicts": lm.verdicts(forever.F, 4),
        "lost_fuel": lm.lost_fuel(forever),
        "shift": lm.shift_failure(),
        "connected_experiment": lm.connected_experiment(forever, recorded),
        "causal_footprint": {
            "reads": "a firing reads the enablement self-instance and the operation edge at the active datum "
                     "(Control.fire, Control.enabled)",
            "writes": "active, tape, clock, fuel; the program is kept (Control.fire_ok)",
            "independence": "an edit to an instance away from the active datum does not change the step; an "
                            "edit at it does (the represented execution family's mutation tests)",
            "not_delivered": "an interacting instance with two loci of activity; the process has one",
        },
        "not_delivered": [
            "an interval, circle or integration theory: the limit is a totally disconnected thread space and "
            "a rational frequency with a bound",
            "lifting the successor relation of a fork to threads: the deterministic runner stops at a fork",
            "a general theorem that every realized tape is eventually periodic: the determinism of the next "
            "datum is proved, the eventual periodicity is computed over the declared class",
            "a second locus of activity for causal independence between two processes",
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
        print("WROTE: deterministic limits record")
        return 0
    if not RECEIPT.is_file() or RECEIPT.read_bytes() != fresh:
        print("FAIL: evidence/limits.json differs from fresh computation")
        return 1
    print("PASS: source pins, the artifact consumed, the experiment replayed, and record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
