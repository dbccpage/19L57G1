"""A branching growth relation and its distance from the invariant thread.

THE STEP

The declared relation offers every result in which:

    one glyph appears.

A datum at some position in some region, or a divider splitting a region.
Nothing selects which.  The step agrees with the renamings not by construction
but because it was written without reference to which glyph is which, and
``step_agrees_with_renamings`` checks that rather than assuming it.

Two things the step deliberately lacks:

* no removal.  State grows and every history replays from the start.  Removal
  would need its own justification and does not get one here.
* no preference.  Every position is offered.

Because every inscription of size ``k`` has a predecessor of size ``k - 1``
(delete any one glyph), generation ``k`` is the complete set of inscriptions of
size ``k``.  Nothing is sampled.

THE THREAD

In each checked generation, exactly one object is held still by every renaming:
the one with no data at all.  These are different states along a fully invariant
thread, not an immobile state.  Distance from that thread is the data count.
"""

from __future__ import annotations

from collections import Counter
from typing import Sequence

from carrier import (
    DATA,
    RENAMINGS,
    Form,
    apply,
    data_count,
    generation,
    held,
    name_of,
    objects,
    render,
)


def step(form: Form) -> frozenset[Form]:
    """One glyph appears.  Every way it could, none preferred."""
    out: set[Form] = set()
    for i, region in enumerate(form):
        for pos in range(len(region) + 1):
            for datum in DATA:
                grown = region[:pos] + (datum,) + region[pos:]
                out.add(form[:i] + (grown,) + form[i + 1 :])
            out.add(form[:i] + (region[:pos], region[pos:]) + form[i + 1 :])
    return frozenset(out)


def step_agrees_with_renamings(carrier: Sequence[Form]) -> list[str]:
    """``step(r(s)) == r(step(s))`` as sets.  Failures, if any."""
    out: list[str] = []
    for s in carrier:
        for n in RENAMINGS:
            left = step(apply(n, s))
            right = frozenset(apply(n, t) for t in step(s))
            if left != right:
                out.append(render(s) + " under " + n)
    return out


def thread_at(k: int) -> Form:
    """The no-data, fully invariant representative at generation ``k``."""
    return tuple(() for _ in range(k + 1))


def distance(form: Form) -> int:
    """Distance from the thread: the data count.

    The bounded checks establish that ``held`` is the full declared renaming set
    exactly when this is zero, and that checked steps never lower it.
    """
    return data_count(form)


def thread_is_unique(k: int) -> bool:
    """Exactly one object at generation ``k`` is held still by every renaming."""
    everywhere = [c for c in objects(k) if len(held(c)) == len(RENAMINGS)]
    return everywhere == [name_of(thread_at(k))]


def distance_never_falls(k: int) -> list[str]:
    """Steps that lower the distance.  Empty means departure is permanent."""
    out: list[str] = []
    for s in generation(k):
        here = distance(s)
        for t in step(s):
            if distance(t) < here:
                out.append(render(s) + " -> " + render(t))
    return out


def held_can_return(k: int) -> list[tuple[Form, Form]]:
    """Steps from an inscription nothing holds still to one something does.

    Non-empty means a break does not ratchet: what is held still can rise again,
    even though the thread itself cannot be regained.
    """
    out: list[tuple[Form, Form]] = []
    for s in generation(k):
        if len(held(s)) != 1:
            continue
        for t in sorted(step(s)):
            if len(held(t)) > 1:
                out.append((s, t))
    return out


def population(k: int) -> dict[int, int]:
    """Objects at generation ``k``, counted by distance from the thread."""
    return dict(Counter(distance(c) for c in objects(k)))


def holds_by_distance(k: int) -> dict[int, list[int]]:
    """Which held-set sizes occur at each distance, at generation ``k``."""
    out: dict[int, set[int]] = {}
    for s in generation(k):
        out.setdefault(distance(s), set()).add(len(held(s)))
    return {d: sorted(v) for d, v in sorted(out.items())}


def object_count(k: int) -> int:
    return len(objects(k))


def object_count_closed_form(k: int) -> int:
    """``a(ceil(k/2)) * a(floor(k/2))`` with ``a(n) = (3**n + 1) // 2``.

    The count of objects factors into two halves, which is the reflection doing
    what a reflection does.
    """
    def a(n: int) -> int:
        power: int = 3**n
        return (power + 1) // 2

    return a((k + 1) // 2) * a(k // 2)


def pasts(k: int) -> dict[Form, set[Form]]:
    """For each object at generation ``k``, the objects it could have come from."""
    out: dict[Form, set[Form]] = {}
    for earlier in generation(k - 1):
        for later in step(earlier):
            out.setdefault(name_of(later), set()).add(name_of(earlier))
    return out


def single_past_count(k: int) -> int:
    """Objects at generation ``k`` with exactly one possible past."""
    return sum(1 for v in pasts(k).values() if len(v) == 1)


def report(horizon: int = 8) -> list[str]:
    """Every result in this module, as lines.  Deterministic."""
    out: list[str] = []
    carrier = [s for k in range(5) for s in generation(k)]
    out.append("step agrees with the renamings: " + str(not step_agrees_with_renamings(carrier)))

    out.append("")
    out.append("generation | objects | closed form | held-by-all | one past")
    for k in range(horizon + 1):
        one_past = single_past_count(k) if k else 1
        out.append(
            "%10d | %7d | %11d | %11d | %8d"
            % (
                k,
                object_count(k),
                object_count_closed_form(k),
                sum(1 for c in objects(k) if len(held(c)) == len(RENAMINGS)),
                one_past,
            )
        )

    out.append("")
    out.append(
        "thread unique through generation "
        + str(horizon)
        + ": "
        + str(all(thread_is_unique(k) for k in range(horizon + 1)))
    )
    out.append("distance never falls: " + str(all(not distance_never_falls(k) for k in range(horizon))))
    out.append("held can return after a break: " + str(bool(held_can_return(2))))

    out.append("")
    out.append("population by distance at generation " + str(horizon) + ":")
    for d, n in sorted(population(horizon).items()):
        out.append("  distance " + str(d) + ": " + str(n) + " objects")

    out.append("")
    out.append("held-set sizes available at each distance, generation " + str(horizon) + ":")
    for d, sizes in holds_by_distance(horizon).items():
        out.append("  distance " + str(d) + ": " + str(sizes))
    return out


if __name__ == "__main__":
    for line in report():
        print(line)
