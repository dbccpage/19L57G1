"""History action, commutativity taxonomy, trace monoid, and parity balance.

Formalizes Prompt B Targets B1.2, B2.2, and B6.1:
- Three-tier adjacent event commutativity taxonomy
- Trace monoid non-group verification (Cartier-Foata trace semantics)
- Data replay parity-blindness
- Form fiber parity balance ([+1, -1]) for general m >= 4
"""

from __future__ import annotations

import sys
from itertools import permutations
from pathlib import Path
from typing import Sequence, Union

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.iso import canonical
from derivation.model import (
    EMPTY,
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
    step,
)
from carrier import perm_sign


def classify_adjacent_pair(s: Regime, e1: Event, e2: Event) -> str:
    """Classify adjacent pair (e1, e2) from state s into three-tier taxonomy:
    - CausallyBlocked: one order raises AdmissionError
    - ReplayCommuting: leaves raw replay regime invariant (s12 == s21)
    - OrderAltering: both orders execute but produce distinct regimes (s12 != s21)
    """
    try:
        s1 = step(s, e1)
        s12 = step(s1, e2)
    except AdmissionError:
        return "CausallyBlocked"

    try:
        s2 = step(s, e2)
        s21 = step(s2, e1)
    except AdmissionError:
        return "CausallyBlocked"

    if s12 == s21:
        return "ReplayCommuting"
    return "OrderAltering"


def enumerate_valid_executions(events: Sequence[Event]) -> list[tuple[int, ...]]:
    """Enumerate all permutation orderings of events that execute without AdmissionError."""
    n = len(events)
    valid = []
    for p in permutations(range(n)):
        ordered_events = [events[i] for i in p]
        try:
            replay(ordered_events, base=EMPTY)
            valid.append(p)
        except AdmissionError:
            continue
    return valid


def verify_data_replay_erasure(
    data_tokens: Sequence[str],
    continuation: Sequence[Event] = (),
) -> bool:
    """Verify canonical(replay(tau . H)) == canonical(replay(H)) for all data permutations."""
    n = len(data_tokens)
    events = [AdmitDatum(tok) for tok in data_tokens]
    base_r = replay(list(events) + list(continuation), base=EMPTY)
    base_key = canonical(base_r)

    for p in permutations(range(n)):
        permuted_events = [events[i] for i in p]
        r_perm = replay(permuted_events + list(continuation), base=EMPTY)
        if canonical(r_perm) != base_key:
            return False
    return True


def analyze_form_fiber_parity(arities: Sequence[int]) -> dict[str, object]:
    """Analyze parity distribution of canonical key fibers under form permutations.

    For m distinct-arity forms, permuting admission order yields distinct
    regimes. We group executions by canonical key and check the parity balance.
    """
    m = len(arities)
    events = [AdmitForm(a) for a in arities]
    all_perms = list(permutations(range(m)))

    fibers: dict[object, list[int]] = {}
    for p in all_perms:
        ordered = [events[i] for i in p]
        r = replay(ordered, base=EMPTY)
        key = canonical(r)
        sign = perm_sign(p)
        fibers.setdefault(key, []).append(sign)

    balanced = True
    fiber_summaries = {}
    for k, signs in fibers.items():
        pos_count = signs.count(1)
        neg_count = signs.count(-1)
        if pos_count != neg_count:
            balanced = False
        fiber_summaries[str(k)] = {
            "total": len(signs),
            "pos": pos_count,
            "neg": neg_count,
            "balanced": (pos_count == neg_count),
        }

    return {
        "m_forms": m,
        "total_executions": len(all_perms),
        "num_fibers": len(fibers),
        "all_fibers_balanced": balanced,
        "fiber_summaries": fiber_summaries,
    }
