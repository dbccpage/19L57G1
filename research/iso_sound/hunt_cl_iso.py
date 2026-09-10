"""hunt_cl_iso.py — Standalone Census and Falsification Hunt Runner for CL-ISO-SOUND.

This module evaluates partition equality between refined-key canonicalization
(canonical) and exhaustive permutation minimization (canonical_bruteforce)
over declared finite spaces:
    Baseline: n_data <= 3, n_forms <= 2, arity <= 2, |insts| <= 3 (56,020 regimes).
    Deep:     n_data <= 3, n_forms <= 1, arity <= 3, |insts| <= 4 (338,650 regimes)
              plus deterministic high-density sweeps for max_forms <= 2.

Claim Hygiene:
- Narrow claim: Confirms partition agreement across declared bounded regimes,
  yielding exact equivalence classes with zero discrepancies.
- Non-claim: Agreement within these finite settings supports partition soundness
  up to the declared horizon; it does not establish general isomorphism soundness.
- General soundness remains OPEN (tracked in paper claim ledger as CL-ISO-SOUND).

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping, Sequence

# Ensure code/ and research/iso_sound/ are importable regardless of invocation cwd
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CODE_DIR = REPO_ROOT / "code"
ISO_SOUND_DIR = REPO_ROOT / "research" / "iso_sound"

if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
if str(ISO_SOUND_DIR) not in sys.path:
    sys.path.insert(0, str(ISO_SOUND_DIR))

from derivation.iso import CanonKey, canonical, canonical_bruteforce  # noqa: E402
from derivation.model import Regime  # noqa: E402
from space import (  # type: ignore[import-not-found]  # noqa: E402
    BOUNDS,
    DEEP_BOUNDS,
    count_space,
    enumerate_regimes,
    regime_record,
    sample_regimes,
)
from corpus import corpus_agreement  # type: ignore[import-not-found]  # noqa: E402


PERM_BUDGET = 100_000
DEEP_RECEIPT_PATH = ISO_SOUND_DIR / "evidence" / "hunt_deep.json"


def encode_key(key: CanonKey) -> list[object]:
    """Serialize a CanonKey into a JSON-safe nested list structure."""
    n, forms, insts, rules, reqs = key
    return [
        n,
        list(forms),
        [[f, list(args)] for f, args in insts],
        list(rules),
        [[i, j] for i, j in reqs],
    ]


def first_split(
    groups: Mapping[CanonKey, list[int]],
    labels: Sequence[CanonKey],
) -> tuple[int, int] | None:
    """Find the first pair of regime indices belonging to the same group in
    'groups' but assigned different keys in 'labels'. Returns (index1, index2)
    or None if no split exists.
    """
    for ids in groups.values():
        seen: dict[CanonKey, int] = {}
        for i in ids:
            label = labels[i]
            if label not in seen:
                seen[label] = i
            if len(seen) > 1:
                members = list(seen.values())
                return members[0], members[1]
    return None


def run_census(
    regimes: Iterable[Regime] | None = None,
    bounds: Mapping[str, int] | None = None,
    perm_budget: int = PERM_BUDGET,
    check_corpus: bool = True,
    max_falsifiers: int = 10,
) -> dict[str, Any]:
    """Execute the partition census comparing refined-key against brute-force canonicalization.

    Uses an online streaming partition check to bound memory while exactly computing
    equivalence class counts and isolating discrepancy witnesses.
    """
    eval_bounds: dict[str, int]
    if bounds is not None:
        eval_bounds = dict(bounds)
    else:
        eval_bounds = dict(BOUNDS)

    if regimes is None:
        regime_iter: Iterable[Regime] = enumerate_regimes(
            max_data=eval_bounds.get("max_data", 3),
            max_forms=eval_bounds.get("max_forms", 2),
            max_arity=eval_bounds.get("max_arity", 2),
            max_insts=eval_bounds.get("max_insts", 3),
        )
    else:
        regime_iter = regimes

    refined_to_brute: dict[CanonKey, tuple[CanonKey, Regime]] = {}
    brute_to_refined: dict[CanonKey, tuple[CanonKey, Regime]] = {}
    falsifiers: list[dict[str, Any]] = []
    regime_count = 0

    for r in regime_iter:
        regime_count += 1
        rk = canonical(r, perm_budget)
        bk = canonical_bruteforce(r)

        if rk in refined_to_brute:
            prev_bk, prev_r = refined_to_brute[rk]
            if prev_bk != bk and len(falsifiers) < max_falsifiers:
                falsifiers.append({
                    "kind": "refined_merges_brute_split",
                    "left": regime_record(prev_r),
                    "right": regime_record(r),
                    "refined_equal": True,
                    "brute_equal": False,
                    "refined_left": encode_key(rk),
                    "refined_right": encode_key(rk),
                    "brute_left": encode_key(prev_bk),
                    "brute_right": encode_key(bk),
                })
        else:
            refined_to_brute[rk] = (bk, r)

        if bk in brute_to_refined:
            prev_rk, prev_r = brute_to_refined[bk]
            if prev_rk != rk and len(falsifiers) < max_falsifiers:
                falsifiers.append({
                    "kind": "brute_merges_refined_split",
                    "left": regime_record(prev_r),
                    "right": regime_record(r),
                    "refined_equal": False,
                    "brute_equal": True,
                    "refined_left": encode_key(prev_rk),
                    "refined_right": encode_key(rk),
                    "brute_left": encode_key(bk),
                    "brute_right": encode_key(bk),
                })
        else:
            brute_to_refined[bk] = (rk, r)

    refined_class_count = len(refined_to_brute)
    brute_class_count = len(brute_to_refined)
    agreement = len(falsifiers) == 0 and refined_class_count == brute_class_count

    receipt: dict[str, Any] = {
        "schema": "iso-sound-hunt-v1",
        "authority_effect": "None",
        "bounds": eval_bounds,
        "perm_budget": perm_budget,
        "regime_count": regime_count,
        "refined_class_count": refined_class_count,
        "brute_class_count": brute_class_count,
        "agreement": agreement,
        "falsifier_count": len(falsifiers),
        "falsifiers": falsifiers,
        "general_soundness": "OPEN",
        "scope": (
            f"evaluated over {regime_count} regimes; bounds={eval_bounds}; "
            "tokens dummy; agreement is not a proof of general CL-ISO-SOUND"
        ),
    }

    if check_corpus:
        receipt["seed_corpus"] = corpus_agreement()

    return receipt


def run_sample_sweep(
    max_data: int = 3,
    max_forms: int = 2,
    max_arity: int = 3,
    max_insts: int = 4,
    sample_count: int = 10_000,
    seed: int = 42,
    require_ternary: bool = True,
    perm_budget: int = PERM_BUDGET,
    max_falsifiers: int = 10,
) -> dict[str, Any]:
    """Deterministic sample sweep across higher parameter regimes comparing partition equality."""
    regimes = sample_regimes(
        max_data=max_data,
        max_forms=max_forms,
        max_arity=max_arity,
        max_insts=max_insts,
        sample_count=sample_count,
        seed=seed,
        require_ternary=require_ternary,
    )
    refined_to_brute: dict[CanonKey, tuple[CanonKey, Regime]] = {}
    brute_to_refined: dict[CanonKey, tuple[CanonKey, Regime]] = {}
    falsifiers: list[dict[str, Any]] = []
    evaluated = 0

    for r in regimes:
        evaluated += 1
        rk = canonical(r, perm_budget)
        bk = canonical_bruteforce(r)

        if rk in refined_to_brute:
            prev_bk, prev_r = refined_to_brute[rk]
            if prev_bk != bk and len(falsifiers) < max_falsifiers:
                falsifiers.append({
                    "kind": "refined_merges_brute_split",
                    "left": regime_record(prev_r),
                    "right": regime_record(r),
                    "refined_equal": True,
                    "brute_equal": False,
                    "refined_left": encode_key(rk),
                    "refined_right": encode_key(rk),
                    "brute_left": encode_key(prev_bk),
                    "brute_right": encode_key(bk),
                })
        else:
            refined_to_brute[rk] = (bk, r)

        if bk in brute_to_refined:
            prev_rk, prev_r = brute_to_refined[bk]
            if prev_rk != rk and len(falsifiers) < max_falsifiers:
                falsifiers.append({
                    "kind": "brute_merges_refined_split",
                    "left": regime_record(prev_r),
                    "right": regime_record(r),
                    "refined_equal": False,
                    "brute_equal": True,
                    "refined_left": encode_key(prev_rk),
                    "refined_right": encode_key(rk),
                    "brute_left": encode_key(bk),
                    "brute_right": encode_key(bk),
                })
        else:
            brute_to_refined[bk] = (rk, r)

    refined_class_count = len(refined_to_brute)
    brute_class_count = len(brute_to_refined)
    agreement = len(falsifiers) == 0 and refined_class_count == brute_class_count

    return {
        "bounds": {
            "max_data": max_data,
            "max_forms": max_forms,
            "max_arity": max_arity,
            "max_insts": max_insts,
        },
        "sample_count": evaluated,
        "seed": seed,
        "require_ternary": require_ternary,
        "refined_class_count": refined_class_count,
        "brute_class_count": brute_class_count,
        "agreement": agreement,
        "falsifier_count": len(falsifiers),
        "falsifiers": falsifiers,
    }


def run_deep_hunt(
    perm_budget: int = PERM_BUDGET,
    check_corpus: bool = True,
    include_sweep: bool = True,
    sweep_samples: int = 10_000,
    sweep_seed: int = 42,
) -> dict[str, Any]:
    """Execute the deep CL-ISO-SOUND hunt on arity >= 3 and |insts| >= 4:

    1. Bounded exhaustive census over max_data=3, max_forms=1, max_arity=3, max_insts=4 (338,650 regimes).
    2. Deterministic high-density sample sweep over max_forms=2, max_arity=3, max_insts=4.
    """
    deep_bounds = dict(DEEP_BOUNDS)
    receipt = run_census(
        bounds=deep_bounds,
        perm_budget=perm_budget,
        check_corpus=check_corpus,
    )
    receipt["scope"] = (
        f"exhaustive over well-formed regimes with n_data \u2264 {deep_bounds['max_data']}, "
        f"n_forms \u2264 {deep_bounds['max_forms']}, arity \u2264 {deep_bounds['max_arity']}, "
        f"|insts| \u2264 {deep_bounds['max_insts']}; tokens dummy; agreement is not a proof of CL-ISO-SOUND"
    )
    if include_sweep:
        sweep = run_sample_sweep(
            max_data=3,
            max_forms=2,
            max_arity=3,
            max_insts=4,
            sample_count=sweep_samples,
            seed=sweep_seed,
            require_ternary=True,
            perm_budget=perm_budget,
        )
        receipt["sample_sweep"] = sweep
        if not sweep["agreement"]:
            receipt["agreement"] = False
            receipt["falsifier_count"] += sweep["falsifier_count"]
            receipt["falsifiers"].extend(sweep["falsifiers"])

    return receipt


def verify_receipt_honesty(receipt: Mapping[str, Any]) -> list[str]:
    """Validate honesty guards on the census receipt."""
    errors: list[str] = []
    if receipt.get("general_soundness") != "OPEN":
        errors.append("SOUNDNESS_GUARD: general_soundness is not OPEN")
    if receipt.get("authority_effect") != "None":
        errors.append("AUTHORITY_GUARD: authority_effect is not None")
    if receipt.get("agreement") is True and receipt.get("falsifier_count", 0) != 0:
        errors.append("AGREEMENT_GUARD: agreement true with non-zero falsifier count")
    if receipt.get("agreement") is False and receipt.get("falsifier_count", 0) == 0:
        errors.append("AGREEMENT_GUARD: agreement false with zero falsifiers")
    corpus = receipt.get("seed_corpus")
    if corpus is not None and (not isinstance(corpus, dict) or corpus.get("agreement") is not True):
        errors.append("CORPUS_GUARD: seed corpus did not agree")
    sweep = receipt.get("sample_sweep")
    if sweep is not None and (not isinstance(sweep, dict) or sweep.get("agreement") is not True):
        errors.append("SWEEP_GUARD: sample sweep did not agree")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hunt CL-ISO-SOUND falsifiers across finite regime spaces."
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run fast smoke census on bounded subset (seed corpus).",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Execute deep hunt on arity >= 3 and |insts| >= 4 (338,650 regimes + sample sweep).",
    )
    parser.add_argument(
        "--deep-exhaustive-only",
        action="store_true",
        help="Execute only the 338,650-regime exhaustive census without sample sweep.",
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Execute deterministic high-density sample sweep for ternary regimes with max_forms=2.",
    )
    parser.add_argument(
        "--sweep-samples",
        type=int,
        default=10_000,
        help="Number of samples for sample sweep (default: 10,000).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit receipt as JSON to stdout.",
    )
    parser.add_argument(
        "--write-receipt",
        type=Path,
        default=None,
        help="Write JSON receipt to specified file path.",
    )
    parser.add_argument(
        "--deep-write",
        action="store_true",
        help="Execute deep hunt and write byte-pinned receipt to research/iso_sound/evidence/hunt_deep.json.",
    )
    args = parser.parse_args()

    if args.smoke:
        print("Executing CL-ISO-SOUND smoke verification...")
        from corpus import seed_corpus
        receipt = run_census(regimes=seed_corpus(), check_corpus=True)
    elif args.deep or args.deep_write:
        print(f"Executing deep CL-ISO-SOUND hunt over {count_space(3, 1, 3, 4):,} regimes (arity <= 3, |insts| <= 4)...")
        receipt = run_deep_hunt(sweep_samples=args.sweep_samples)
    elif args.deep_exhaustive_only:
        print(f"Executing deep exhaustive census over {count_space(3, 1, 3, 4):,} regimes...")
        receipt = run_deep_hunt(include_sweep=False)
    elif args.sweep:
        print(f"Executing deterministic sample sweep ({args.sweep_samples:,} samples) for ternary regimes...")
        sweep_result = run_sample_sweep(sample_count=args.sweep_samples)
        receipt = {
            "schema": "iso-sound-hunt-v1",
            "authority_effect": "None",
            "general_soundness": "OPEN",
            "bounds": sweep_result["bounds"],
            "sample_sweep": sweep_result,
            "regime_count": sweep_result["sample_count"],
            "refined_class_count": sweep_result["refined_class_count"],
            "brute_class_count": sweep_result["brute_class_count"],
            "agreement": sweep_result["agreement"],
            "falsifier_count": sweep_result["falsifier_count"],
            "falsifiers": sweep_result["falsifiers"],
            "seed_corpus": corpus_agreement(),
            "scope": f"sample sweep of {args.sweep_samples:,} regimes with seed=42; tokens dummy",
        }
    else:
        print(f"Executing full baseline CL-ISO-SOUND census over {count_space():,} regimes...")
        receipt = run_census()

    errors = verify_receipt_honesty(receipt)
    if errors:
        print("HONESTY GUARD FAILURES:")
        for err in errors:
            print(f"  - {err}")
        return 1

    formatted_json = json.dumps(receipt, sort_keys=True, indent=1) + "\n"

    if args.json:
        print(formatted_json, end="")
    else:
        print("=== CL-ISO-SOUND CENSUS RECEIPT ===")
        print(f"Regimes Evaluated:    {receipt['regime_count']:,}")
        print(f"Refined Classes:      {receipt['refined_class_count']:,}")
        print(f"Brute-Force Classes:  {receipt['brute_class_count']:,}")
        print(f"Partition Agreement:  {receipt['agreement']}")
        print(f"Falsifiers Found:     {receipt['falsifier_count']}")
        print(f"General Soundness:    {receipt['general_soundness']}")
        print(f"Authority Effect:     {receipt['authority_effect']}")
        if "seed_corpus" in receipt:
            sc = receipt["seed_corpus"]
            print(f"Seed Corpus Checks:   {sc.get('pair_checks', 0)} pairs (Agreement: {sc.get('agreement')})")
        if "sample_sweep" in receipt:
            sw = receipt["sample_sweep"]
            print(f"Sample Sweep:         {sw.get('sample_count', 0):,} samples (Agreement: {sw.get('agreement')})")

    target_write = args.write_receipt
    if args.deep_write:
        target_write = DEEP_RECEIPT_PATH

    if target_write is not None:
        target_write.parent.mkdir(parents=True, exist_ok=True)
        target_write.write_bytes(formatted_json.encode("utf-8"))
        print(f"Wrote byte-pinned receipt to: {target_write}")

    if not receipt["agreement"] or receipt["falsifier_count"] > 0:
        print("FALSIFIER DETECTED! Refined-key partition differs from brute-force.")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
