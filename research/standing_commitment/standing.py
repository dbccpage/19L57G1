"""The standing commitment, recomputed independently of Lean, and the race
it sets up between growth and discharge.

The Lean side proves that a state growing under a standing commitment
acquires demands with no act between the growth and the demand, and counts
how many: under the commitment that keeps every distinct pair apart, one
growth step on a state of ``n`` data adds exactly ``n``.

This module asks the question the counting theorem raises.  If growth
generates demands and discharge removes them, the two are in a race, and the
race is settled by two declared numbers: how DENSE the commitment is, and
how large the discharge budget is.  Nothing here derives either; both are
declared, and the point is exactly that the outcome depends on them.

Discharge is modelled as a declared budget -- up to ``rate`` demands removed
per round -- and not as a derived repair.  That is the honest model: the
sealed estate gates repair by a represented budget, and this tree does not
reconstruct the repair machinery.  A discharged demand is recorded as
discharged and never returns; nothing here claims a repair exists.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass

Req = tuple[int, int]


def pairs_of(data: list[int]) -> list[Req]:
    """The ordered pairs drawn from the data, mirroring the Lean `pairsOf`:
    each earlier element paired with each later one, head first."""

    out: list[Req] = []
    for i, d in enumerate(data):
        for e in data[i + 1 :]:
            out.append((d, e))
    return out


# --------------------------------------------------------------- commitments


def holds_total(i: int, j: int) -> bool:
    """Keep every distinct pair apart."""

    return i != j


def holds_adjacent(i: int, j: int) -> bool:
    """Keep apart only the pairs whose labels are consecutive."""

    return abs(i - j) == 1


def holds_shared_parity(i: int, j: int) -> bool:
    """Keep apart only the distinct pairs whose labels agree in parity."""

    return i != j and (i % 2) == (j % 2)


def holds_empty(i: int, j: int) -> bool:
    """Require nothing."""

    return False


def holds_bounded(i: int, j: int) -> bool:
    """Keep apart only the distinct pairs among the first four labels.

    Added AFTER the predictions freeze, and recorded as such: it exists to
    refute the regularity the frozen family exhibits, not to be scored
    against a prediction.  Its generation rises and then stops, which is
    exactly what the four frozen commitments never do."""

    return i != j and i < 4 and j < 4


COMMITMENTS: dict[str, object] = {
    "total": holds_total,
    "adjacent": holds_adjacent,
    "shared_parity": holds_shared_parity,
    "empty": holds_empty,
    "bounded": holds_bounded,
}


def commitment(name: str) -> object:
    return COMMITMENTS[name]


def holds(name: str, i: int, j: int) -> bool:
    fn = COMMITMENTS[name]
    assert callable(fn)
    return bool(fn(i, j))


# ------------------------------------------------------------------ the race


@dataclass(frozen=True)
class Round:
    """One round: the state grows by one datum, then the declared discharge
    budget is spent on the oldest outstanding demands."""

    index: int
    admitted: int
    generated: int
    discharged: int
    backlog: int


def generated_by_growth(name: str, data: list[int], new: int) -> list[Req]:
    """The demands the new datum brings: exactly the pairs the commitment
    keeps apart between the new datum and each datum already held.  Mirrors
    the Lean `demands_grow`."""

    return [(new, e) for e in data if holds(name, new, e)]


def race(name: str, rounds: int, rate: int, start: int = 0) -> dict[str, object]:
    """Grow one datum per round; discharge up to `rate` demands per round.

    Returns the per-round record and the two numbers that decide the run:
    whether the backlog ever falls back to zero after the first demand, and
    the largest backlog reached."""

    data: list[int] = []
    outstanding: list[Req] = []
    log: list[Round] = []
    total_generated = 0
    total_discharged = 0
    for k in range(rounds):
        new = start + k
        fresh = generated_by_growth(name, data, new)
        data.append(new)
        outstanding.extend(fresh)
        total_generated += len(fresh)
        spend = min(rate, len(outstanding))
        outstanding = outstanding[spend:]
        total_discharged += spend
        log.append(Round(k, new, len(fresh), spend, len(outstanding)))
    ever_cleared = any(r.backlog == 0 for r in log if r.index > 0) and total_generated > 0
    return {
        "commitment": name,
        "rounds": rounds,
        "discharge_rate": rate,
        "generated": total_generated,
        "discharged": total_discharged,
        "final_backlog": len(outstanding),
        "max_backlog": max((r.backlog for r in log), default=0),
        "ever_cleared_after_first": ever_cleared,
        "log": [
            {
                "round": r.index,
                "admitted": r.admitted,
                "generated": r.generated,
                "discharged": r.discharged,
                "backlog": r.backlog,
            }
            for r in log
        ],
    }


def threshold(name: str, rounds: int, max_rate: int) -> int | None:
    """The least declared discharge budget at which the backlog is empty at
    the end of the run.  `None` when no budget up to `max_rate` suffices.

    A number about THIS run length and nothing beyond it: a rate that clears
    a short run need not clear a longer one, and the table records both."""

    for rate in range(0, max_rate + 1):
        if int(str(race(name, rounds, rate)["final_backlog"])) == 0:
            return rate
    return None
