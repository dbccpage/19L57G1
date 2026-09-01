"""Promotion, computational half: the price floor per obstructed
two-label census member, decided by full slot-space exhaustion with
the pinned predicate as the only verdict source, plus the Lean cure
witness (`slot_group_sections`) concretized and verified per member.

Two independent routes are computed and compared per member:

- the SLOT-SPACE exhaustion: every assignment of {identity, exchange}
  to every slot, verdict by the pinned `cone_section` on the pinned
  `relabelled` presentation (FINITE_COMPUTATION);
- the CONSUMED-CLASS route: the per-hop consumed parities determine
  the relabelled presentation up to the proved parity law, so the
  2^hops consumed classes are exhausted with the same pinned predicate
  and the price is recomputed from class distances.  Agreement of the
  two routes at every exhausted member is the recorded SUPPORT for the
  closed-form price CONJECTURE; it is not a proof of it.

Requires the pinned sign_slice modules on the path (`../sign_slice`).
AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import product

from cone_section import cone_section
from genpres import GenPres
from occ_relabel import pointwise_assignments, relabelled, undirected_hops
from parity import conjugation_obeys_parity_law, perm_parity

Perm = tuple[int, ...]

SLOT_EXHAUSTION_BOUND = 20
SWAP2: Perm = (1, 0)
IDENT2: Perm = (0, 1)


def hop_parities(p: GenPres, hops: list[tuple[int, int]]) -> tuple[int, ...]:
    return tuple(perm_parity(p.arrows[i].transport) for i, _ in hops)


def cure_assignment(p: GenPres, hops: list[tuple[int, int]]) -> tuple[int, ...]:
    """The Lean witness concretized: source-end slot the identity,
    target-end slot the hop's own parity."""

    bits: list[int] = []
    for i, _ in hops:
        bits.append(0)
        bits.append(perm_parity(p.arrows[i].transport))
    return tuple(bits)


def parity_law_checked(p: GenPres, hops: list[tuple[int, int]]) -> int:
    """Check the proved conjugation law on every hop and every slot
    combination of this member; return the number of checked
    instances.  Raises on the first violation."""

    checked = 0
    maps = (IDENT2, SWAP2)
    for i, _ in hops:
        t = p.arrows[i].transport
        for a in (0, 1):
            for b in (0, 1):
                if not conjugation_obeys_parity_law(t, maps[a], maps[b]):
                    raise AssertionError(
                        f"parity law violated at hop {i}, slots ({a}, {b})"
                    )
                checked += 1
    return checked


def _mask(bits: tuple[int, ...]) -> int:
    out = 0
    for k, v in enumerate(bits):
        out |= v << k
    return out


def exhaust_slots(p: GenPres) -> dict[str, object]:
    """Full slot-space exhaustion under the declared bound.  Records
    the flip census, the pointwise check, the price (least slot
    distance of a flipping assignment from the pointwise family), the
    tie count at the price, and the first cheapest flip in the
    deterministic order."""

    hops = undirected_hops(p)
    slots = 2 * len(hops)
    if slots > SLOT_EXHAUSTION_BOUND:
        return {
            "slots": slots,
            "refused": f"REFUSED: {slots} slots exceeds the declared"
            f" exhaustion bound of {SLOT_EXHAUSTION_BOUND}",
        }
    base = cone_section(p)
    pointwise = sorted(_mask(a) for a in pointwise_assignments(p, hops))
    pointwise_set = set(pointwise)
    flips = 0
    pointwise_moves = 0
    price: int | None = None
    price_ties = 0
    cheapest: tuple[int, ...] | None = None
    for bits in product((0, 1), repeat=slots):
        moved = cone_section(relabelled(p, hops, bits, SWAP2)) != base
        if not moved:
            continue
        flips += 1
        m = _mask(bits)
        if m in pointwise_set:
            pointwise_moves += 1
        d = min((m ^ q).bit_count() for q in pointwise)
        if price is None or d < price:
            price = d
            price_ties = 1
            cheapest = bits
        elif d == price:
            price_ties += 1
    return {
        "slots": slots,
        "assignments": 2**slots,
        "base_sectioned": base,
        "flip_count": flips,
        "pointwise_assignments": len(pointwise),
        "pointwise_moves": pointwise_moves,
        "price_min_slots_from_pointwise": price,
        "price_tie_count": price_ties,
        "first_cheapest_flip": list(cheapest) if cheapest is not None else None,
    }


def exhaust_consumed_classes(p: GenPres) -> dict[str, object]:
    """The consumed-class route: one pinned-predicate verdict per
    per-hop consumed-parity vector, prices from class distances.  The
    identification of an assignment's verdict with its consumed
    class's verdict is exactly the proved parity law, checked
    concretely by `parity_law_checked` -- and independently confirmed
    by agreement with `exhaust_slots`."""

    hops = undirected_hops(p)
    law_instances = parity_law_checked(p, hops)
    base = cone_section(p)
    # A consumed class is realized by source-end identity, target-end
    # the class bit at each hop.
    flipping: list[tuple[int, ...]] = []
    for cls in product((0, 1), repeat=len(hops)):
        bits: list[int] = []
        for c in cls:
            bits.append(0)
            bits.append(c)
        if cone_section(relabelled(p, hops, tuple(bits), SWAP2)) != base:
            flipping.append(cls)
    # Pointwise consumed classes and the class-level price: a flipping
    # class costs one slot per hop where it differs from a pointwise
    # class's consumed parity.
    objs = sorted(p.objects)
    pw_classes = set()
    for eps_bits in product((0, 1), repeat=len(objs)):
        eps = {o: eps_bits[k] for k, o in enumerate(objs)}
        pw_classes.add(
            tuple(eps[p.arrows[i].src] ^ eps[p.arrows[i].dst] for i, _ in hops)
        )
    price: int | None = None
    if flipping:
        price = min(
            sum(1 for x, y in zip(cls, q, strict=True) if x != y)
            for cls in flipping
            for q in sorted(pw_classes)
        )
    flip_count = len(flipping) * (2 ** len(hops))
    return {
        "hops": len(hops),
        "classes": 2 ** len(hops),
        "flipping_classes": len(flipping),
        "flip_count_from_classes": flip_count,
        "price_from_classes": price,
        "parity_law_instances_checked": law_instances,
    }


def cure_verified(p: GenPres) -> dict[str, object]:
    """Concretize the Lean cure witness on this member and verify it
    with the pinned predicate."""

    hops = undirected_hops(p)
    assignment = cure_assignment(p, hops)
    cured = relabelled(p, hops, assignment, SWAP2)
    return {
        "assignment": list(assignment),
        "cured_sectioned": cone_section(cured),
        "hop_parities": list(hop_parities(p, hops)),
    }
