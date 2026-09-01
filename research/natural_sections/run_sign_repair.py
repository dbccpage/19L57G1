"""Write receipts/sign_repair.json deterministically (``--out DIR``)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

import sign_repair

HERE = Path(__file__).resolve().parent


def render(report: dict[str, object]) -> bytes:
    return (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
        "ascii"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    if not out.is_relative_to(HERE):
        print(f"refusing to write outside research/natural_sections/: {out}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    report = sign_repair.report()
    (out / "sign_repair.json").write_bytes(render(report))
    print(
        f"families: {report['family_count']}, fibrewise-odd {report['fibrewise_odd_count']}"
        f" with {report['fibrewise_odd_moved_total_misses']} moved-total misses"
    )
    print(
        f"certificate decisions: {report['certificate_agreement_misses']} disagreements"
        f" between counting and search; certified {report['certified_count']},"
        f" uncertified {report['uncertified_count']}"
    )
    print(
        f"separable {report['separable_count']}; interacting certified"
        f" {report['interacting_certified_count']}; positive-total uncertified"
        f" {report['positive_total_uncertified_count']}"
    )
    print(
        f"minimal positive-total uncertified: {report['minimal_positive_total_uncertified']};"
        f" minimal interacting certified: {report['minimal_interacting_certified']}"
    )
    print(
        f"pinned witness {report['pinned_witness']}: interacting"
        f" {report['pinned_witness_is_interacting']}, certificate"
        f" {report['pinned_witness_has_certificate']}; open question answered at bound:"
        f" {report['open_question_answer_at_bound']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
