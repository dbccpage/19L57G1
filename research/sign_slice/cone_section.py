"""ConeSection: the decision predicate, by the cited criterion.

ConeSection(P) iff the presentation admits a natural section.  The
implementation is the generator/holonomy criterion the sibling packet
proved (CONDITIONAL_THEOREM: `natural_section_iff_generators`,
`natural_section_iff_holonomy`; the phase form `section_iff_flux_zero`
is the same predicate on the phase fibre and is not forked here): per
component, take the declared forest (breadth first from the least
object), close the generator-walk transports into a group, and ask
for an admissible pair fixed by all of it.  With the kernel observer,
an admissible pair is an ordered pair of distinct labels, and a fixed
admissible pair exists iff the holonomy fixes at least two labels.

Twisted and total read-outs over declared weighted walk lists are the
packet's weighted layer, reconstructed (METATHEORY).

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import deque

from genpres import Arrow, GenPres, Perm, compose, identity, inverse


def components(p: GenPres) -> list[list[int]]:
    neighbours: dict[int, set[int]] = {o: set() for o in p.objects}
    for a in p.arrows:
        neighbours[a.src].add(a.dst)
        neighbours[a.dst].add(a.src)
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in sorted(p.objects):
        if start in seen:
            continue
        comp = []
        queue = deque([start])
        seen.add(start)
        while queue:
            u = queue.popleft()
            comp.append(u)
            for v in sorted(neighbours[u]):
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        out.append(sorted(comp))
    return out


def forest_paths(p: GenPres, component: list[int]) -> dict[int, Perm]:
    """The declared forest: breadth first from the least object, taking
    the least-indexed arrow available.  Returns, per object, the
    transport of the tree walk from the base to that object."""

    base = component[0]
    path: dict[int, Perm] = {base: identity(p.fibre)}
    queue = deque([base])
    while queue:
        u = queue.popleft()
        for a in p.arrows:
            if a.src == u and a.dst not in path:
                path[a.dst] = compose(a.transport, path[u])
                queue.append(a.dst)
            elif a.dst == u and a.src not in path:
                path[a.src] = compose(inverse(a.transport), path[u])
                queue.append(a.src)
    return path


def holonomy_group(p: GenPres, component: list[int]) -> set[Perm]:
    """The closure of the generator-walk transports at the base."""

    path = forest_paths(p, component)
    gens: set[Perm] = set()
    for i in p.generators:
        a = p.arrows[i]
        if a.src not in path or a.dst not in path:
            continue
        loop = compose(inverse(path[a.dst]), compose(a.transport, path[a.src]))
        gens.add(loop)
        gens.add(inverse(loop))
    group: set[Perm] = {identity(p.fibre)}
    frontier = list(gens)
    while frontier:
        g = frontier.pop()
        if g in group:
            continue
        group.add(g)
        for h in list(group):
            for prod in (compose(g, h), compose(h, g)):
                if prod not in group:
                    frontier.append(prod)
    return group


def fixed_labels(group: set[Perm], fibre: int) -> list[int]:
    return [l for l in range(fibre) if all(g[l] == l for g in group)]


def cone_section(p: GenPres) -> bool:
    """The predicate.  True iff every component's holonomy fixes an
    admissible pair -- at least two labels of the kernel observer."""

    if p.fibre < 2:
        return False
    return all(
        len(fixed_labels(holonomy_group(p, comp), p.fibre)) >= 2
        for comp in components(p)
    )


# ---------------------------------------------------------------------------
# Weighted read-outs over declared walk lists (the packet's weighted
# layer, reconstructed)
# ---------------------------------------------------------------------------


def closed_walks(p: GenPres, base: int, max_len: int) -> list[tuple[Perm, int]]:
    """Every closed walk at ``base`` of length at most ``max_len``,
    traversing arrows forward or backward, as (transport, amp product).
    Deterministic order: by length, then by step choices in arrow-index
    order (forward before backward)."""

    out: list[tuple[Perm, int]] = []
    steps: list[tuple[int, Perm, int, int]] = []
    for i, a in enumerate(p.arrows):
        steps.append((a.src, a.transport, a.dst, a.amp))
        steps.append((a.dst, inverse(a.transport), a.src, a.amp))

    def extend(at: int, transport: Perm, amp: int, length: int) -> None:
        if at == base:
            out.append((transport, amp))
        if length == max_len:
            return
        for src, t, dst, w in steps:
            if src == at:
                extend(dst, compose(t, transport), amp * w, length + 1)

    extend(base, identity(p.fibre), 1, 0)
    return out


def twisted_and_total(
    walks: list[tuple[Perm, int]], pair: tuple[int, int]
) -> tuple[int, int, int]:
    """(twisted at the pair, total, mover count under unit weights)."""

    twisted = 0
    total = 0
    movers = 0
    l1, l2 = pair
    for transport, amp in walks:
        total += amp
        if transport[l1] == l1 and transport[l2] == l2:
            twisted += amp
        else:
            movers += 1
    return twisted, total, movers
