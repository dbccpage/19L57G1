"""SixLabel: the occupancy-3 square under four-valued slot maps
(FINITE_COMPUTATION, FW-LEAD held: nothing here states an outcome; the
exhaustion decides).

The member is the pinned census's `square_2x2_occ3`.  Slot maps range
over the identity and the three rank-exchange label actions -- the
label action of a rank bijection mirrors the pinned mover-family
transport construction: label `l` becomes the label `r -> l[sigma[r]]`.
Four choices per slot, eight slots; the space `4^8 = 65536` is
exhausted, not sampled.  Verdicts come from the pinned predicate only.

Requires the pinned sign_slice modules on the path (`../sign_slice`).
AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import permutations, product

from cone_section import cone_section
from genpres import Arrow, GenPres, Perm, compose, grid_sites, inverse, mover_family
from occ_relabel import relabelled as binary_relabelled
from occ_relabel import undirected_hops

OCCUPANCY = 3
RANK_EXCHANGES: tuple[Perm, ...] = ((1, 0, 2), (0, 2, 1), (2, 1, 0))


def label_action(sigma: Perm) -> Perm:
    """The label permutation induced by a rank bijection, mirroring the
    pinned transport construction."""

    labels = sorted(permutations(range(OCCUPANCY)))
    label_index = {l: i for i, l in enumerate(labels)}
    return tuple(
        label_index[tuple(l[sigma[r]] for r in range(OCCUPANCY))] for l in labels
    )


def slot_maps() -> tuple[Perm, ...]:
    """The declared four maps: identity first, then the three
    rank-exchange label actions in the declared order."""

    fibre = 1
    for k in range(2, OCCUPANCY + 1):
        fibre *= k
    ident = tuple(range(fibre))
    return (ident,) + tuple(label_action(s) for s in RANK_EXCHANGES)


def relabelled_multi(
    p: GenPres,
    hops: list[tuple[int, int]],
    assignment: tuple[int, ...],
    maps: tuple[Perm, ...],
) -> GenPres:
    """The four-valued generalization of the pinned binary relabel:
    identical shape, with `assignment` entries indexing `maps` instead
    of two bits.  Cross-checked against the pinned binary relabel on
    every binary sub-assignment (see `binary_crosscheck`)."""

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


def member() -> GenPres:
    return mover_family(4, grid_sites(2, 2), OCCUPANCY, signed=False)


def binary_crosscheck(p: GenPres) -> dict[str, int]:
    """PS3: for each single exchange, the four-valued relabel restricted
    to {identity, that exchange} agrees with the pinned binary relabel
    on every binary assignment."""

    hops = undirected_hops(p)
    slots = 2 * len(hops)
    maps = slot_maps()
    misses = 0
    checked = 0
    for k in (1, 2, 3):
        for bits in product((0, 1), repeat=slots):
            multi = relabelled_multi(p, hops, tuple(b * k for b in bits), maps)
            binary = binary_relabelled(p, hops, bits, maps[k])
            checked += 1
            if multi != binary:
                misses += 1
    return {"checked": checked, "misses": misses}


def pointwise_shaped(
    p: GenPres, hops: list[tuple[int, int]]
) -> list[tuple[int, ...]]:
    """Assignments constant per object: one of the four maps per
    object, each slot taking its object's map."""

    objs = sorted(p.objects)
    out: list[tuple[int, ...]] = []
    for choice in product(range(4), repeat=len(objs)):
        g = {o: choice[k] for k, o in enumerate(objs)}
        assignment: list[int] = []
        for i, _ in hops:
            a = p.arrows[i]
            assignment.append(g[a.src])
            assignment.append(g[a.dst])
        out.append(tuple(assignment))
    return out


def exhaust() -> dict[str, object]:
    """The experiment.  Both terminals were pre-agreed before this ran;
    the returned `terminal` is decided here and nowhere else."""

    p = member()
    hops = undirected_hops(p)
    slots = 2 * len(hops)
    maps = slot_maps()
    base = cone_section(p)
    pw = pointwise_shaped(p, hops)
    pw_set = set(pw)
    flips = 0
    pointwise_moves = 0
    witness: tuple[int, ...] | None = None
    price: int | None = None
    price_ties = 0
    for assignment in product(range(4), repeat=slots):
        moved = cone_section(relabelled_multi(p, hops, assignment, maps)) != base
        if not moved:
            continue
        flips += 1
        if witness is None:
            witness = assignment
        if assignment in pw_set:
            pointwise_moves += 1
        d = min(
            sum(1 for x, y in zip(assignment, q, strict=True) if x != y) for q in pw
        )
        if price is None or d < price:
            price = d
            price_ties = 1
        elif d == price:
            price_ties += 1
    terminal = "SIXLABEL_MOVES" if flips else "SIXLABEL_INVARIANT_BOUNDED"
    return {
        "member": "square_2x2_occ3",
        "base_sectioned": base,
        "slots": slots,
        "maps_per_slot": len(maps),
        "assignments": len(maps) ** slots,
        "flip_count": flips,
        "pointwise_shaped_assignments": len(pw),
        "pointwise_moves": pointwise_moves,
        "first_witness": list(witness) if witness is not None else None,
        "price_min_slots_from_pointwise": price,
        "price_tie_count": price_ties,
        "terminal": terminal,
        "bound": "four maps per slot (identity and the three rank"
        " exchanges), eight slots, 4^8 exhausted",
    }
