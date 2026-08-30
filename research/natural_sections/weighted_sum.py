"""Weighted sums over declared closed walks: what a natural section buys.

A layer over ``holonomy_group.py``: each hop carries an integer amplitude
(forward and backward); a walk's weight is the product; over a declared
finite list of closed walks at a base, ``total`` is the sum of weights and
``twisted(p)`` the sum of the weights of the walks whose holonomy fixes the
admissible pair ``p`` (an ordered pair of distinct labels).  Closed walks are
enumerated up to a declared length from the base; nothing about the
infinite set is claimed.  Amplitudes are ring elements, weights are
products; nothing else.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Sequence

import holonomy_fixture as two
import holonomy_group as hg

Config = tuple[int, ...]
Perm = tuple[int, ...]
Edge = tuple[int, int]
Arrow = tuple[Config, Config]
Walk = tuple[Arrow, ...]
Amplitude = Callable[[Config, Config, bool], int]  # (a, b, forward?) -> amplitude


def arrows(sites: int, edges: Sequence[Edge], k: int) -> dict[Config, list[tuple[Config, Perm]]]:
    objs: list[Config] = [tuple(c) for c in combinations(range(sites), k)]
    out: dict[Config, list[tuple[Config, Perm]]] = {o: [] for o in objs}
    for a in objs:
        for b in objs:
            perm = hg.hop_perm(edges, a, b)
            if perm is not None:
                out[a].append((b, perm))
    return out


def closed_walks(
    adj: dict[Config, list[tuple[Config, Perm]]], base: Config, max_len: int
) -> list[tuple[Walk, Perm]]:
    """Every closed walk at ``base`` of length at most ``max_len``, forward
    steps only (every hop's reverse is itself a declared hop), with its
    holonomy; in lexicographic order of the arrow sequence."""

    k = len(base)
    out: list[tuple[Walk, Perm]] = []

    def go(at: Config, walk: list[Arrow], perm: Perm) -> None:
        if at == base:
            out.append((tuple(walk), perm))
        if len(walk) == max_len:
            return
        for nxt, step in sorted(adj[at]):
            walk.append((at, nxt))
            go(nxt, walk, hg.compose(step, perm))
            walk.pop()

    go(base, [], hg.identity(k))
    return out


def weight(walk: Walk, amp: Amplitude) -> int:
    w = 1
    for a, b in walk:
        w *= amp(a, b, True)
    return w


def fixes(perm: Perm, pair: tuple[int, int]) -> bool:
    return perm[pair[0]] == pair[0] and perm[pair[1]] == pair[1]


def total(walks: Sequence[tuple[Walk, Perm]], amp: Amplitude) -> int:
    return sum(weight(w, amp) for w, _ in walks)


def twisted(walks: Sequence[tuple[Walk, Perm]], amp: Amplitude, pair: tuple[int, int]) -> int:
    return sum(weight(w, amp) for w, perm in walks if fixes(perm, pair))


def unit_amp(a: Config, b: Config, forward: bool) -> int:
    return 1


def sign_amp(edges: Sequence[Edge]) -> Amplitude:
    """``-1`` on a flipping hop, ``+1`` otherwise: a walk's weight is its parity."""

    def amp(a: Config, b: Config, forward: bool) -> int:
        is_hop, flip = two.hop(edges, (a[0], a[1]), (b[0], b[1])) if len(a) == 2 else (True, False)
        return -1 if (is_hop and flip) else 1

    return amp


@dataclass(frozen=True)
class Report:
    name: str
    k: int
    base: Config
    max_len: int
    walks: int
    pairs: dict[tuple[int, int], dict[str, int]]
    total_unit: int
    total_sign: int

    def json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "k": self.k,
            "base": list(self.base),
            "max_len": self.max_len,
            "closed_walks": self.walks,
            "total_unit": self.total_unit,
            "total_sign": self.total_sign,
            "pairs": {f"{p[0]},{p[1]}": v for p, v in sorted(self.pairs.items())},
        }


def analyse(name: str, sites: int, edges: Sequence[Edge], k: int, max_len: int) -> Report:
    adj = arrows(sites, edges, k)
    objs = sorted(adj)
    base = objs[0]
    walks = closed_walks(adj, base, max_len)
    sign = sign_amp(edges)
    pairs: dict[tuple[int, int], dict[str, int]] = {}
    for i in range(k):
        for j in range(k):
            if i != j:
                pairs[(i, j)] = {
                    "twisted_unit": twisted(walks, unit_amp, (i, j)),
                    "twisted_sign": twisted(walks, sign, (i, j)),
                    "movers": sum(1 for _, perm in walks if not fixes(perm, (i, j))),
                }
    return Report(
        name=name,
        k=k,
        base=base,
        max_len=max_len,
        walks=len(walks),
        pairs=pairs,
        total_unit=total(walks, unit_amp),
        total_sign=total(walks, sign),
    )


def orbit_counterexample() -> dict[str, object]:
    """Ladder, four labels, holonomy the full symmetric group: with ``ws`` a
    single generator walk of holonomy a transposition, two pairs in one
    holonomy orbit have different twisted sums."""

    edges = two.grid(2, 3)
    adj = arrows(6, edges, 4)
    base = sorted(adj)[0]
    walks = closed_walks(adj, base, 6)
    transposition = next((w, perm) for w, perm in walks if sorted(perm) == [0, 1, 2, 3] and
                         sum(1 for i in range(4) if perm[i] != i) == 2)
    perm = transposition[1]
    moved = [i for i in range(4) if perm[i] != i]
    fixed = [i for i in range(4) if perm[i] == i]
    fixed_pair = (fixed[0], fixed[1])
    moved_pair = (moved[0], fixed[0])
    ws = [transposition]
    return {
        "generator_holonomy": list(perm),
        "pair_fixed": list(fixed_pair),
        "pair_moved": list(moved_pair),
        "twisted_at_fixed": twisted(ws, unit_amp, fixed_pair),
        "twisted_at_moved": twisted(ws, unit_amp, moved_pair),
        "same_orbit_note": "the holonomy group is the full symmetric group, transitive on ordered pairs",
    }


def every_value(values: Sequence[int]) -> dict[str, list[int]]:
    """A backtrack walk with amplitude ``v`` realises twisted = total = v, on the
    square (no section) and the chain (section) alike."""

    out: dict[str, list[int]] = {}
    for name, sites, edges in (("square_2x2", 4, two.grid(2, 2)), ("chain_P4", 4, two.chain(4))):
        adj = arrows(sites, edges, 2)
        base = sorted(adj)[0]
        nxt, step = sorted(adj[base])[0]
        back = hg.compose(hg.inverse(step), step)
        walk: tuple[Walk, Perm] = (((base, nxt), (nxt, base)), back)
        got: list[int] = []
        for v in values:
            def amp(a: Config, b: Config, forward: bool, v: int = v) -> int:
                return v if (a, b) == (base, nxt) else 1
            got.append(twisted([walk], amp, (0, 1)))
        out[name] = got
    return out


def fixtures() -> list[tuple[str, int, list[Edge], int, int]]:
    return [
        ("chain_P4_k2", 4, two.chain(4), 2, 6),
        ("square_2x2_k2", 4, two.grid(2, 2), 2, 6),
        ("star_K13_k2", 4, two.star(3), 2, 6),
    ]


def report() -> dict[str, object]:
    return {
        "layer": {
            "amplitude": "an integer per directed hop; a walk's weight is the product",
            "walks": "every closed walk at the base up to the declared length, forward steps",
            "total": "the sum of weights",
            "twisted(p)": "the sum of weights of walks whose holonomy fixes the ordered pair p",
        },
        "fixtures": [analyse(*f).json() for f in fixtures()],
        "orbit_counterexample": orbit_counterexample(),
        "every_value": every_value([-3, -1, 0, 2, 7]),
    }
