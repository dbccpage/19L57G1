"""OccRelabel: the first convention class strictly larger than the
proved pointwise re-presentation invariance.

An occurrence slot of a presentation is a pair (undirected hop, end).
An OccRelabel assigns one fibre bijection per slot, with NO requirement
that slots sharing an object carry the same bijection -- that stronger
requirement is exactly the pointwise class whose invariance the
sibling packet proved, and FW-T1 forbids citing that proof as an
answer here.  A transported arrow is conjugated by the two slot maps
at its own ends only; the two directions of one hop share their slot
maps, so inverse pairs stay inverse pairs.

The only question this module answers, inside the declared bound
(every slot map is the identity or the two-label exchange): does some
assignment move the ConeSection class of a census member?

AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import product

from cone_section import cone_section
from genpres import Arrow, GenPres, Perm, compose, identity, inverse


def undirected_hops(p: GenPres) -> list[tuple[int, int]]:
    """Pair each arrow with its reverse.  Every mover-family arrow has
    exactly one reverse; the pairing is by endpoints and inverse
    transport, taking the least available partner."""

    used: set[int] = set()
    hops: list[tuple[int, int]] = []
    for i, a in enumerate(p.arrows):
        if i in used:
            continue
        partner = -1
        for j in range(i + 1, len(p.arrows)):
            if j in used:
                continue
            b = p.arrows[j]
            if b.src == a.dst and b.dst == a.src and b.transport == inverse(a.transport):
                partner = j
                break
        if partner < 0:
            raise ValueError(f"arrow {i} has no reverse partner")
        used.add(i)
        used.add(partner)
        hops.append((i, partner))
    return hops


def relabelled(
    p: GenPres, hops: list[tuple[int, int]], assignment: tuple[int, ...], swap: Perm
) -> GenPres:
    """Apply slot maps.  ``assignment`` holds two bits per hop, in hop
    order: (source-end map, target-end map) of the forward arrow, each
    0 for identity and 1 for ``swap``."""

    maps = [identity(p.fibre), swap]
    new_arrows = list(p.arrows)
    for h, (i, j) in enumerate(hops):
        g_src = maps[assignment[2 * h]]
        g_dst = maps[assignment[2 * h + 1]]
        a = p.arrows[i]
        new_t = compose(g_dst, compose(a.transport, inverse(g_src)))
        new_arrows[i] = Arrow(a.src, a.dst, new_t, a.amp)
        b = p.arrows[j]
        new_arrows[j] = Arrow(b.src, b.dst, inverse(new_t), b.amp)
    return GenPres(p.objects, tuple(new_arrows), p.fibre, p.generators)


def pointwise_assignments(
    p: GenPres, hops: list[tuple[int, int]]
) -> list[tuple[int, ...]]:
    """Every assignment constant per object: the shape whose invariance
    the packet proved."""

    objs = sorted(p.objects)
    out: list[tuple[int, ...]] = []
    for bits in product((0, 1), repeat=len(objs)):
        g = {o: bits[k] for k, o in enumerate(objs)}
        assignment = []
        for i, _ in hops:
            a = p.arrows[i]
            assignment.append(g[a.src])
            assignment.append(g[a.dst])
        out.append(tuple(assignment))
    return out


def exhaust(p: GenPres, swap: Perm) -> dict[str, object]:
    """Exhaust the slot-map space under the declared bound.  Returns
    the census of flips, the pointwise check, and the price of the
    cheapest flipping assignment (its least distance from any pointwise
    assignment)."""

    hops = undirected_hops(p)
    slots = 2 * len(hops)
    base = cone_section(p)
    pointwise = set(pointwise_assignments(p, hops))
    pointwise_moves = 0
    flips: list[tuple[int, ...]] = []
    for assignment in product((0, 1), repeat=slots):
        moved = cone_section(relabelled(p, hops, assignment, swap)) != base
        if moved:
            flips.append(assignment)
            if assignment in pointwise:
                pointwise_moves += 1
    price = None
    cheapest: tuple[int, ...] | None = None
    if flips:
        best = slots + 1
        for f in flips:
            d = min(sum(1 for x, y in zip(f, q, strict=True) if x != y) for q in pointwise)
            if d < best:
                best = d
                cheapest = f
        price = best
    return {
        "slots": slots,
        "assignments": 2**slots,
        "base_sectioned": base,
        "flip_count": len(flips),
        "pointwise_assignments": len(pointwise),
        "pointwise_moves": pointwise_moves,
        "price_min_slots_from_pointwise": price,
        "cheapest_flip": list(cheapest) if cheapest is not None else None,
    }
