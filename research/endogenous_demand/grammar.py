"""Python mirror of the sealed reqs channel.

Classification: deterministic computation.  Every claim here is a replay
of ``derivation.model.step``.  It does not prove the Lean theorems; it
exhibits the same cases on the Python event language, in both admission
readings.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Sequence

from derivation.engine import GENESIS_F, GENESIS_L
from derivation.model import (
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Pair,
    Supply,
    replay,
    step,
)

READINGS: tuple[str, ...] = ("L", "F")
GENESIS: dict[str, tuple[Event, ...]] = {"L": GENESIS_L, "F": GENESIS_F}
# Challenge 3 closes by imposing the collapsed pair; genesis itself does not.
CHALLENGE3: dict[str, tuple[Event, ...]] = {
    "L": GENESIS_L + (Impose(0, 1),),
    "F": GENESIS_F + (Impose(1, 2),),
}


def is_impose(event: Event) -> bool:
    return isinstance(event, Impose)


def imposes_in(history: Sequence[Event]) -> tuple[Pair, ...]:
    """The impose events of a history, as ordered pairs."""
    pairs: list[Pair] = []
    for event in history:
        if isinstance(event, Impose):
            pairs.append((event.i, event.j))
    return tuple(pairs)


def reqs_of(history: Sequence[Event]) -> frozenset[Pair]:
    return replay(history).reqs


def last_event_extends_reqs(history: Sequence[Event]) -> bool:
    """Whether the last event strictly grew ``reqs``.

    Empty history does not extend.  Used by the E2 guard: a generating
    step that grows ``reqs`` must be an ``Impose``.
    """
    if not history:
        return False
    prefix = replay(history[:-1])
    whole = replay(history)
    return whole.reqs != prefix.reqs


def e2_violation(history: Sequence[Event]) -> str | None:
    """If the last event grew ``reqs`` without being ``Impose``, name it.

    Returning ``None`` means this history does not exhibit an E2 violation
    of the reqs channel.  It is not a proof that E2 holds.
    """
    if not history:
        return None
    last = history[-1]
    if last_event_extends_reqs(history) and not is_impose(last):
        return f"E2: last event {type(last).__name__} grew reqs without Impose"
    return None


def constructor_cases() -> dict[str, dict[str, object]]:
    """One successful step of each constructor from a two-datum base.

    The base has data ``a, b``, a unary form, no instances, no rules, no
    requirements.  Each case records whether ``reqs`` changed.
    """
    base = replay((Supply("a"), AdmitDatum("a"), Supply("b"), AdmitDatum("b"), AdmitForm(1)))
    cases: dict[str, dict[str, object]] = {}
    events: dict[str, Event] = {
        "Supply": Supply("c"),
        "AdmitDatum": AdmitDatum("c"),
        "AdmitForm": AdmitForm(2),
        "AdmitInst": AdmitInst(0, (0,)),
        "AdmitRuleAll": AdmitRuleAll(0),
        "Impose": Impose(0, 1),
    }
    for name, event in events.items():
        child = step(base, event)
        cases[name] = {
            "reqs_before": sorted(base.reqs),
            "reqs_after": sorted(child.reqs),
            "changed": child.reqs != base.reqs,
            "is_impose": is_impose(event),
        }
    return cases


def reading_replays() -> dict[str, dict[str, object]]:
    """Both Challenge-3 closes: ``reqs`` equals the impose events."""
    out: dict[str, dict[str, object]] = {}
    for name, history in CHALLENGE3.items():
        regime = replay(history)
        out[name] = {
            "history_length": len(history),
            "impose_events": [list(pair) for pair in imposes_in(history)],
            "reqs": [list(pair) for pair in sorted(regime.reqs)],
            "e2_violation": e2_violation(history),
            "last_is_impose": is_impose(history[-1]),
        }
    return out


def prefix_without_impose() -> dict[str, object]:
    """The Challenge-3 L prefix with the closing Impose dropped: empty reqs."""
    history = CHALLENGE3["L"][:-1]
    regime = replay(history)
    return {
        "reading": "L",
        "impose_events": [list(pair) for pair in imposes_in(history)],
        "reqs": [list(pair) for pair in sorted(regime.reqs)],
        "empty_reqs": regime.reqs == frozenset(),
    }


def grammar_record() -> dict[str, object]:
    cases = constructor_cases()
    writers = sorted(name for name, row in cases.items() if bool(row["changed"]))
    return {
        "schema": "endogenous-demand-grammar-v1",
        "authority_effect": "None",
        "class": "C_reqs",
        "outcome": "B",
        "readings": list(READINGS),
        "constructor_cases": cases,
        "reqs_writers": writers,
        "reading_replays": reading_replays(),
        "prefix_without_impose": prefix_without_impose(),
        "empty_is_empty": EMPTY.reqs == frozenset(),
    }
