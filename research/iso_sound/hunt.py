"""Hunt a CL-ISO-SOUND falsifier inside the declared finite space.

A falsifier is a pair of regimes on which refined-key equality disagrees
with brute-force-key equality.  The partitions are compared by grouping,
not by a quadratic pair loop.

Classification: deterministic computation.  Agreement on this space is
not a proof of general soundness.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Mapping, Sequence

from derivation.iso import CanonKey, canonical, canonical_bruteforce
from derivation.model import Regime

from corpus import corpus_agreement
from space import BOUNDS, count_space, enumerate_regimes, regime_record

PERM_BUDGET = 100_000


def _encode(key: CanonKey) -> list[object]:
    n, forms, insts, rules, reqs = key
    return [
        n,
        list(forms),
        [[f, list(args)] for f, args in insts],
        list(rules),
        [[i, j] for i, j in reqs],
    ]


def hunt() -> dict[str, object]:
    refined_of: list[CanonKey] = []
    brute_of: list[CanonKey] = []
    regimes: list[Regime] = []
    for regime in enumerate_regimes():
        refined_of.append(canonical(regime, PERM_BUDGET))
        brute_of.append(canonical_bruteforce(regime))
        regimes.append(regime)

    n = len(regimes)
    expected = count_space()
    if n != expected:
        raise RuntimeError(f"enumeration size {n} != closed form {expected}")

    by_refined: dict[CanonKey, list[int]] = defaultdict(list)
    by_brute: dict[CanonKey, list[int]] = defaultdict(list)
    for i, (rk, bk) in enumerate(zip(refined_of, brute_of)):
        by_refined[rk].append(i)
        by_brute[bk].append(i)

    falsifiers: list[dict[str, object]] = []
    split = first_split(by_refined, brute_of)
    kind = "refined_merges_brute_split"
    if split is None:
        split = first_split(by_brute, refined_of)
        kind = "brute_merges_refined_split"
    if split is not None:
        i, j = split
        falsifiers.append({
            "kind": kind,
            "left": regime_record(regimes[i]),
            "right": regime_record(regimes[j]),
            "refined_equal": refined_of[i] == refined_of[j],
            "brute_equal": brute_of[i] == brute_of[j],
            "refined_left": _encode(refined_of[i]),
            "refined_right": _encode(refined_of[j]),
            "brute_left": _encode(brute_of[i]),
            "brute_right": _encode(brute_of[j]),
        })

    return {
        "schema": "iso-sound-hunt-v1",
        "authority_effect": "None",
        "bounds": dict(BOUNDS),
        "perm_budget": PERM_BUDGET,
        "regime_count": n,
        "refined_class_count": len(by_refined),
        "brute_class_count": len(by_brute),
        "agreement": len(falsifiers) == 0,
        "falsifier_count": len(falsifiers),
        "falsifiers": falsifiers,
        "seed_corpus": corpus_agreement(),
        "general_soundness": "OPEN",
        "scope": (
            "exhaustive over well-formed regimes with n_data ≤ 3, "
            "n_forms ≤ 2, arity ≤ 2, |insts| ≤ 3; tokens dummy; "
            "agreement is not a proof of CL-ISO-SOUND"
        ),
    }


def first_split(
    groups: Mapping[CanonKey, list[int]],
    labels: Sequence[CanonKey],
) -> tuple[int, int] | None:
    """The first pair whose group is not constant on ``labels``, or None."""
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


def claim_errors(record: Mapping[str, object]) -> tuple[str, ...]:
    """Named failures of the hunt record's honesty guards."""
    errors: list[str] = []
    if record.get("general_soundness") != "OPEN":
        errors.append("SOUNDNESS_GUARD: general_soundness is not OPEN")
    if record.get("agreement") is True and record.get("falsifier_count") not in (0,):
        errors.append("AGREEMENT_GUARD: agreement true with a falsifier")
    if record.get("agreement") is False and record.get("falsifier_count") == 0:
        errors.append("AGREEMENT_GUARD: agreement false with no falsifier")
    corpus = record.get("seed_corpus")
    if not isinstance(corpus, dict) or corpus.get("agreement") is not True:
        errors.append("CORPUS_GUARD: seed corpus did not agree")
    return tuple(errors)

