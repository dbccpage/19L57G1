"""Write the P1 receipt: ``receipts/axiom_lattice.json``.

Usage, from inside ``research/s9_obligations/``:

    PYTHONPATH=../../code PYTHONUTF8=1 python run_axiom_lattice.py --out receipts

Prints the step-5 clause counts before and after the swap quotient, the
declared "stronger" direction of the order (step 10), the relation census
per carrier, the closure sizes, the step-11 set per cell (its members, or
``[]`` when empty), the restriction of the closure at the attempted carrier
onto the required one, and the terminals, then writes the receipt through
``common.write_receipt`` (sorted keys, ASCII, LF, one trailing newline; no
timestamps, no paths, no environment data).  The elapsed wall time is
printed to stdout only and is NOT in the receipt.  Refuses an ``--out``
outside the tree.  AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import axiom_lattice as al
import common

RECEIPT_NAME = "axiom_lattice.json"


def _print_clause_space(report: dict[str, object]) -> None:
    print(
        f"clauses {report['fragment']}: raw {report['raw_clause_count']}, "
        f"swap orbits {report['swap_orbit_count']}, head-in-body "
        f"{report['head_in_body_count']}, nontrivial "
        f"{report['nontrivial_clause_count']}, nontrivial swap orbits "
        f"{report['nontrivial_swap_orbit_count']} (used downstream); "
        f"one-variable raw {report['one_variable_clause_count_raw']}, "
        f"one-variable orbits {report['one_variable_swap_orbit_count']}, "
        f"two-variable raw {report['two_variable_clause_count_raw']}"
    )


def _print_f3_set(f3: dict[str, object]) -> None:
    members = f3["members"]
    assert isinstance(members, list)
    decision = f3["decided_before_the_sweep"]
    assert isinstance(decision, dict)
    if not members:
        print(f"      f3 set: [] (decided before the sweep: {decision['verdict']})")
        return
    print(f"      f3 set (decided before the sweep: {decision['verdict']}):")
    for member in members:
        assert isinstance(member, dict)
        rep = member["representative_axiom"]
        assert isinstance(rep, list)
        axiom = " ; ".join(str(t) for t in rep)
        print(f"        [{axiom}] sizes {member['extent_size_by_carrier']}")


def _print_sweep(name: str, sweep: dict[str, object]) -> None:
    print(
        f"{name}: relations {sweep['relation_total']} "
        f"{sweep['relation_census']}, pattern classes "
        f"{sweep['pattern_class_total']}, completed inside bound "
        f"{sweep['completed_inside_bound']}"
    )
    fragments = sweep["fragments"]
    assert isinstance(fragments, dict)
    for fragment, result in fragments.items():
        single = result["single_clause_extents"]
        lattice = result["lattice"]
        print(
            f"  {fragment}: generators {result['generators']['count']}, "
            f"single-clause extents {single['extent_class_count']} "
            f"(syntax {single['syntax_class_count']}), closure "
            f"{lattice['closure_size']} (syntax {lattice['syntax_axiom_count']}), "
            f"truncated {lattice['truncated']}"
        )
        for defn_name, analysis in result["transfer"].items():
            print(
                f"    {defn_name}: transferring {analysis['transferring_count']}, "
                f"strengthening {analysis['closed_under_strengthening']}, "
                f"weakening {analysis['closed_under_weakening']}, "
                f"meet {analysis['closed_under_meet']}, unique weakest "
                f"{analysis['unique_weakest_exists']}, equals irreflexivity "
                f"{analysis['unique_weakest_equals_irreflexivity_extent']}, "
                f"W in lattice {analysis['transfer_as_containment']['W_in_lattice']}, "
                f"F3 set size {analysis['f3_set']['count']}"
            )
            _print_f3_set(analysis["f3_set"])
        for defn_name, audit in result["classifier_audit"].items():
            print(f"    audit {defn_name}: defect {audit['defect']}, kind {audit['kind']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the P1 (S9.1) receipt.")
    parser.add_argument("--out", default="receipts", help="output directory")
    args = parser.parse_args(argv)
    try:
        out_dir = common.assert_inside_tree(Path(args.out))
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    started = time.perf_counter()
    for fragment in (al.PURE, al.EQ_BEARING):
        _print_clause_space(al.clause_space_report(fragment))
    print(f"order: {al.ORDER_DECLARATION['order']}")
    print(f"stronger: {al.ORDER_DECLARATION['stronger']}")
    receipt = al.build_receipt()
    elapsed = time.perf_counter() - started
    sweeps = receipt["sweeps"]
    assert isinstance(sweeps, dict)
    for name, sweep in sweeps.items():
        _print_sweep(name, sweep)
    restriction = receipt["closure_restriction"]
    assert isinstance(restriction, dict)
    for fragment in al.FRAGMENTS:
        block = restriction.get(fragment)
        if isinstance(block, dict):
            print(
                f"closure restriction {fragment}: N{block['from_carrier']} -> "
                f"N{block['to_carrier']}: {block['upper_closure_size']} extents, "
                f"{block['distinct_restrictions']} distinct restrictions, injective "
                f"{block['injective']}, image equals lower closure "
                f"{block['image_equals_lower_closure']}"
            )
    terminals = receipt["terminals"]
    assert isinstance(terminals, dict)
    print(f"terminal: {terminals['lattice']}")
    for group in ("transfer", "f3"):
        block = terminals[group]
        assert isinstance(block, dict)
        for fragment, per_definition in block.items():
            for defn_name, line in per_definition.items():
                print(f"terminal [{fragment} / {defn_name}]: {line}")
    for key in ("eq_fragment", "refused", "lean"):
        print(f"terminal: {terminals[key]}")
    target = common.write_receipt(out_dir / RECEIPT_NAME, receipt)
    print(f"wrote {target.relative_to(common.TREE).as_posix()}")
    print(f"elapsed (stdout only, not in the receipt): {elapsed:.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
