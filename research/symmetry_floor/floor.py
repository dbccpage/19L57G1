"""The floor: what a rule that reads only the state can do, and what it cannot.

THE OBSTRUCTION

A rule that carries one inscription to one inscription, computed from the
inscription alone, cannot see which glyph is which -- so renaming the input
renames the output.  Call that agreeing with the renamings.  Then any renaming
that already left the input alone leaves the output alone:

    r(f(s)) = f(r(s)) = f(s)

So what an inscription holds still can only grow.  A start that every renaming
leaves alone has a successor that every renaming leaves alone, for every rule,
forever.  The seed is not the variable; single-valuedness is.

WHAT THIS MODULE ADDS TO THAT LINE

1.  The converse.  ``held(s) <= held(t)`` is not merely necessary for some rule
    to carry ``s`` to ``t`` -- it is sufficient.  Every such pair extends to a
    rule, and no further constraint exists.  So the containment is the complete
    description of what a state-read rule may do, not a side condition on it.

2.  Exhaustion.  Checked over every map on a closed carrier, by index
    arithmetic that does not consult the characterisation it is checking.

3.  The price of the exit.  Drop single-valuedness and a step offers a set.  The
    set must still be carried to itself, so it must hold every way of presenting
    what it contains.  The multiplicity that buys a break is that count, computed
    rather than asserted.

The one-line obstruction is proved in ``lean/SymmetryFloor.lean`` with no
appeal to any property of the carrier, so it is not about inscriptions.
"""

from __future__ import annotations

import itertools
from typing import Callable, NamedTuple, Sequence

from carrier import (
    DATA,
    RENAMINGS,
    Form,
    apply,
    held,
    name_of,
    render,
    still_everywhere,
    with_shape,
)


def closed_carrier(max_dividers: int, max_data: int) -> list[Form]:
    """Every inscription within the bound.

    Closed under the renamings by construction: both preserve the divider count
    and the data count, so neither can leave the bound.
    """
    out: list[Form] = []
    for dividers in range(max_dividers + 1):
        for data in range(max_data + 1):
            out.extend(with_shape(dividers, data))
    return sorted(set(out))


def agrees_with_renamings(rule: Callable[[Form], Form], carrier: Sequence[Form]) -> bool:
    """``f(r(s)) == r(f(s))`` for every renaming and every inscription."""
    return all(
        rule(apply(n, s)) == apply(n, rule(s)) for n in RENAMINGS for s in carrier
    )


def holds_the_floor(rule: Callable[[Form], Form], carrier: Sequence[Form]) -> bool:
    """``held(s) <= held(f(s))`` everywhere: what is held still can only grow."""
    return all(held(s) <= held(rule(s)) for s in carrier)


def rule_carrying(source: Form, target: Form) -> Callable[[Form], Form] | None:
    """Build a rule carrying ``source`` to ``target``, or report that none exists.

    Define ``f(r(source)) = r(target)`` and leave everything else alone.  This is
    well defined exactly when the held set is contained: the construction is
    attempted here rather than argued, and returns ``None`` when it collides.
    """
    table: dict[Form, Form] = {}
    for n in RENAMINGS:
        s, t = apply(n, source), apply(n, target)
        if s in table and table[s] != t:
            return None
        table[s] = t
    return lambda x: table.get(x, x)


def containment_matches_constructibility(carrier: Sequence[Form]) -> list[str]:
    """Where the held-set containment and the existence of a rule disagree.

    An empty result is the converse: containment is sufficient, not merely
    necessary, so it is the complete description of what a rule may do.
    """
    out: list[str] = []
    for source in carrier:
        for target in carrier:
            contained = held(source) <= held(target)
            rule = rule_carrying(source, target)
            constructible = rule is not None and agrees_with_renamings(rule, carrier)
            if contained != constructible:
                out.append(
                    render(source)
                    + " -> "
                    + render(target)
                    + ": contained="
                    + str(contained)
                    + " constructible="
                    + str(constructible)
                )
    return out


def predicted_rule_count(carrier: Sequence[Form]) -> int:
    """How many rules agree with the renamings, by the characterisation.

    One independent choice per object: any target whose held set contains the
    source object's.
    """
    total = 1
    seen: set[Form] = set()
    for s in carrier:
        if name_of(s) in seen:
            continue
        seen.add(name_of(s))
        total *= sum(1 for t in carrier if held(s) <= held(t))
    return total


def counted_rule_count(carrier: Sequence[Form]) -> int:
    """How many rules agree with the renamings, by trying every map there is.

    Index arithmetic only.  The characterisation is not consulted, so this is an
    independent count of the same quantity.
    """
    n = len(carrier)
    index = {s: i for i, s in enumerate(carrier)}
    moves = [tuple(index[apply(r, s)] for s in carrier) for r in RENAMINGS]
    count = 0
    for rule in itertools.product(range(n), repeat=n):
        for move in moves:
            if any(rule[move[i]] != move[rule[i]] for i in range(n)):
                break
        else:
            count += 1
    return count


class BreakPrice(NamedTuple):
    """What a break costs, per renaming and for the whole set of them."""

    held_by_everything: list[str]
    to_break_one_renaming: dict[str, int]
    to_break_every_renaming: int | None


def price_of_a_break(carrier: Sequence[Form]) -> BreakPrice:
    """What a symmetry break costs once single-valuedness is dropped.

    A set-valued step need only return a set carried to itself.  Its members need
    not be.  The smallest such set holding an inscription that some renaming
    moves is the count of ways that inscription can be presented.
    """
    per_renaming: dict[str, int] = {}
    for n in RENAMINGS:
        if n == "id":
            continue
        moved = [len({s, apply(n, s)}) for s in carrier if apply(n, s) != s]
        per_renaming[n] = min(moved) if moved else 0
    nothing_held = [
        len({apply(n, s) for n in RENAMINGS})
        for s in carrier
        if len(held(s)) == 1
    ]
    return BreakPrice(
        held_by_everything=[render(s) for s in still_everywhere(carrier)],
        to_break_one_renaming=per_renaming,
        to_break_every_renaming=min(nothing_held) if nothing_held else None,
    )


def report() -> list[str]:
    """The three results, as lines.  Deterministic."""
    out: list[str] = []
    big = closed_carrier(2, 3)
    small = closed_carrier(1, 1)

    built = 0
    broke = 0
    for source in big:
        for target in big:
            if not held(source) <= held(target):
                continue
            rule = rule_carrying(source, target)
            if rule is None:
                continue
            built += 1
            if not holds_the_floor(rule, big):
                broke += 1
    out.append("carrier: " + str(len(big)) + " inscriptions, dividers <= 2, data <= 3")
    out.append("rules built: " + str(built) + ", violating the floor: " + str(broke))

    disagreements = containment_matches_constructibility(big)
    out.append(
        "containment vs constructibility over "
        + str(len(big) ** 2)
        + " pairs: "
        + str(len(disagreements))
        + " disagreements"
    )
    out.extend("  " + d for d in disagreements[:5])

    predicted = predicted_rule_count(small)
    counted = counted_rule_count(small)
    out.append(
        "closed carrier of "
        + str(len(small))
        + ": "
        + str(len(small) ** len(small))
        + " maps, predicted "
        + str(predicted)
        + ", counted "
        + str(counted)
    )

    price = price_of_a_break(big)
    out.append("held by every renaming: " + str(price.held_by_everything))
    out.append("cost to break one renaming: " + str(price.to_break_one_renaming))
    out.append("cost to break every renaming: " + str(price.to_break_every_renaming))
    return out


if __name__ == "__main__":
    for line in report():
        print(line)
