"""Write and check this family's record: ``evidence/limits.json``.

AuthorityEffect: None.  ``--write`` creates the record deliberately;
``--check`` recomputes it and compares bytes.  The record carries no
timestamps and no machine-specific paths.  It names the artifact consumed
(the represented execution family's ``evidence/process.json``, read and
never written here), the programs identified from it and the finding that its
schema is set-valued, the observation system and its theorems, the proof that
the observed tape is the sequence and that the bound holds of the run, the
limit and its declared topology, which threads the process generates, the
three verdicts, the failure pairs, and the connected experiment at four
scales.

The receipt refuses to record an artifact whose fragment is not ``control``,
programs the recorded runs do not identify uniquely, observations that are
not prefix-compatible, a recorded tape not prefix-related to the observed
run, and a bound that fails at any scale.  For the two-locus run it refuses a
recorded tape identifying no single factorization of the carrier, a step that
moved both loci, and a locus reading that is not prefix-related to that
locus's own run.
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
# also have a ``run.py`` and a ``verify_sources.py``.  The consumed trees go
# immediately after it and never at the end: appended, they would sit behind
# ``PYTHONPATH`` and site-packages, and a same-named module found there would
# compute this record while the pins still passed.
sys.path[1:1] = [str(dependency) for dependency in
                 (REPO / "code", REPO / "research" / "setting_translation",
                  REPO / "research" / "represented_execution")
                 if str(dependency) not in sys.path]

from verify_sources import PACKET, verify_sources  # noqa: E402

if PACKET != Path("research/coherent_process_limits"):
    raise RuntimeError(f"wrong custody guard imported: {PACKET}")

import control as ct  # noqa: E402
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
            "fuel_independence": "Observe.obs_fuel_indep, obs_fuel_eq: two states agreeing on graph, "
                                 "operation count, active datum and tape, each with at least n fuel, have "
                                 "the same observation at scale n; the fuel is consulted only to refuse",
        },
        "limit": {
            "stages": "words of length n over the carrier (Limits.Stage)",
            "thread_space": "compatible families at every scale (Limits.Compatible, Limits.Thread)",
            "construction": "Limits.ofSeq; the inverse pair Limits.ofSeq_toSeq and Limits.toSeq_ofSeq: "
                            "the thread space is the sequence space, a bijection and not a "
                            "mediating-map statement; no choice or compactness is used",
            "eventual_agreement_is_not_compatibility": "Limits.eventual_not_compatible, Limits.eventual_agrees",
            "cofinal_rescaling": "Limits.thread_even, Limits.even_thread: the even scales have the same "
                                 "threads, through the sequences; Limits.restrictEven and "
                                 "Limits.restrictEven_eq: the map that carries them is the restriction "
                                 "of a thread to the even scales, which is what limits.even_family computes",
            "topology": "declared, not proved: the product of the discrete topologies on the finite stages; "
                        "totally disconnected; not an interval, not a circle; none is claimed, and an "
                        "interval would need an order or metric compatible with the stages and an "
                        "identification of threads this family does not make",
        },
        "which_threads": {
            "all_mathematical_sequences": "the thread space is all of them (the construction is total)",
            "process_generated": "functional tapes — equal entries have equal successors, proved along the "
                                 "whole run for every setting, start and scale (Observe.obs_functional, from "
                                 "the chain invariant Observe.iter_chain) — and therefore eventually "
                                 "periodic on a finite carrier, with preperiod and period together at most "
                                 "the carrier size (Observe.eventually_periodic_run, carried to the record "
                                 "by Observe.obs_last_repeats).  An earlier version of this line called the "
                                 "periodicity the standard consequence and left it unformalized; that is "
                                 "WITHDRAWN.  A strict subset",
            "computably_presented": "between the two; not characterised here",
        },
        "tape_is_the_sequence": {
            "theorem": "Observe.forever_iter, forever_obs: after n steps of the cycle-everywhere program "
                       "from datum 0, with fuel to spare, the active datum is n % 3 and the tape is the "
                       "first n + 1 entries of i -> i % 3",
            "bound_on_the_run": "Observe.forever_length, forever_zeros, forever_run_bound: the readout of "
                                "the observation itself obeys L <= 3 * count <= L + 2",
            "was": "computed at every recorded scale and labelled the missing connection; proved now",
        },
        "verdicts": lm.verdicts(forever.F, 4),
        "lost_fuel": lm.lost_fuel(forever),
        "shift": lm.shift_failure(),
        "connected_experiment": lm.connected_experiment(forever, recorded),
        "two_locus_experiment": lm.two_locus_experiment(artifact),
        "periodicity": lm.periodicity(forever.F, 12),
        "fork_family": lm.fork_family(
            ct.Controlled(forever.F, frozenset({(0, 0), (0, 1)})), 0, 5, (0, 1, 2, 3)),
        "causal_footprint": {
            "reads": "a firing reads the enablement self-instance and the operation edge at the active datum "
                     "(Control.fire, Control.enabled)",
            "writes": "active, tape, clock, fuel; the program is kept (Control.fire_ok)",
            "independence": "an edit to an instance away from the active datum does not change the step, and "
                            "an edit at it does: the represented execution family's "
                            "test_an_edit_away_from_the_active_datum_leaves_the_step_unchanged and its "
                            "mutation tests.  Computed on those populations; no theorem states it",
            "two_loci": "delivered.  The producer family runs two loci by a schedule carried in the "
                        "data, and Observe.obs_one_locus lifts the independence to the observation: at "
                        "every scale, from every start, with any fuel and for every schedule, the "
                        "observed tape of a two-locus run moves one locus at a time.  What does NOT "
                        "lift is the square itself — two orders reach the same datum and record "
                        "different tapes — and what does is the projection with the repeats dropped.  "
                        "Computed here at five scales in two_locus_experiment, over the factorization "
                        "identified from the artifact rather than declared",
        },
        "not_delivered": [
            "an interval, circle or integration theory: the limit is a totally disconnected thread space and "
            "a rational frequency with a bound",
            "a thread out of a fork's family of observations: the family is observed at four scales "
            "and its members are proved prefix-compatible, but a thread needs one tape chosen per "
            "scale at each fork, and that selection is refused",
            "the limit of a two-locus run as an inverse system in its own right: the two-locus "
            "observation is taken at five scales and its one-locus-at-a-time property proved along "
            "every run, but the thread space over the product carrier, and whether the two loci give "
            "two commuting inverse systems, are not built",
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
