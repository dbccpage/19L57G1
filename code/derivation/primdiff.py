"""Primitive difference: finite searches and countermodels.

Classification: metatheory apparatus for the investigation recorded in
``paper/primitive_difference.md``.  Everything here is exhaustive,
deterministic enumeration over declared finite scopes; nothing assumes
the regime model of the earlier development.

A *pointed structure* is ``(n, rel, a, b)``: a carrier ``range(n)``, a
relation ``rel`` (set of ordered pairs), and a designated pair.  The
candidate readings of "primitive difference" are predicates on pointed
structures:

* ``a1``   -- positive apartness datum: the pair is asserted;
* ``a1i``  -- ``a1`` and the relation is irreflexive;
* ``a3``   -- metatheoretic inequality of the designated points
              (equivalently: non-factorization through a point);
* ``a4``   -- irreducibility under an admitted operation family.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product
from typing import Callable, Iterator, Optional, Sequence

Rel = frozenset[tuple[int, int]]
Func = tuple[int, ...]


@dataclass(frozen=True)
class Pointed:
    n: int
    rel: Rel
    a: int
    b: int

    def json(self) -> dict[str, object]:
        return {
            "n": self.n,
            "rel": sorted(self.rel),
            "a": self.a,
            "b": self.b,
        }


def enumerate_pointed(n: int) -> Iterator[Pointed]:
    """All pointed structures on the carrier ``range(n)``, deterministic
    order."""
    pairs = [(x, y) for x in range(n) for y in range(n)]
    for mask in range(1 << len(pairs)):
        rel = frozenset(p for k, p in enumerate(pairs) if mask >> k & 1)
        for a in range(n):
            for b in range(n):
                yield Pointed(n, rel, a, b)


def a1(s: Pointed) -> bool:
    return (s.a, s.b) in s.rel


def irreflexive(rel: Rel) -> bool:
    return all(x != y for (x, y) in rel)


def a1i(s: Pointed) -> bool:
    return a1(s) and irreflexive(s.rel)


def a3(s: Pointed) -> bool:
    return s.a != s.b


def all_functions(n: int) -> list[Func]:
    return [tuple(f) for f in product(range(n), repeat=n)]


def compose(f: Func, g: Func) -> Func:
    return tuple(f[g[x]] for x in range(len(g)))


def closure(n: int, family: Sequence[Func]) -> frozenset[Func]:
    """Closure of an endofunction family under identity and composition
    (a finite monoid; computed to fixpoint)."""
    identity = tuple(range(n))
    out: set[Func] = {identity} | set(family)
    changed = True
    while changed:
        changed = False
        for f in list(out):
            for g in list(out):
                h = compose(f, g)
                if h not in out:
                    out.add(h)
                    changed = True
    return frozenset(out)


def a4(s: Pointed, family: Sequence[Func]) -> bool:
    return all(f[s.a] != f[s.b] for f in closure(s.n, family))


def merge_map(n: int, x: int, y: int) -> Func:
    """The map identifying ``y`` with ``x`` and fixing everything else."""
    return tuple(x if z == y else z for z in range(n))


# ---------------------------------------------------------------------------
# Candidate implication matrix over a declared finite scope
# ---------------------------------------------------------------------------


def candidate_predicates(
    s: Pointed,
) -> dict[str, bool]:
    """The candidate readings evaluated on one pointed structure.  A4 is
    sampled at the declared family choices."""
    merge = merge_map(s.n, min(s.a, s.b), max(s.a, s.b))
    constants = [tuple(v for _ in range(s.n)) for v in range(s.n)]
    return {
        "A1": a1(s),
        "A1i": a1i(s),
        "A3": a3(s),
        "A4_empty": a4(s, []),
        "A4_merge_ab": a4(s, [merge]),
        "A4_all_constants": a4(s, constants),
    }


def implication_matrix(max_n: int) -> dict[str, object]:
    """Exhaustively test every implication P -> Q between candidate
    readings over all pointed structures with carrier size <= ``max_n``;
    record a countermodel for every failure."""
    names: Optional[list[str]] = None
    holds: dict[tuple[str, str], bool] = {}
    counter: dict[tuple[str, str], dict[str, object]] = {}
    extents: dict[str, int] = {}
    for n in range(1, max_n + 1):
        for s in enumerate_pointed(n):
            preds = candidate_predicates(s)
            if names is None:
                names = sorted(preds)
                extents = {p: 0 for p in names}
                for p in names:
                    for q in names:
                        holds[(p, q)] = True
            for p in names:
                if preds[p]:
                    extents[p] += 1
                for q in names:
                    if preds[p] and not preds[q] and holds[(p, q)]:
                        holds[(p, q)] = False
                        counter[(p, q)] = {
                            "structure": s.json(),
                            "satisfies": p,
                            "violates": q,
                        }
    assert names is not None
    return {
        "scope": f"all pointed structures, carrier <= {max_n}",
        "candidates": names,
        "predicate_extents": extents,
        "vacuous_candidates": sorted(
            p for p in names if extents[p] == 0
        ),
        "implications": {
            f"{p}->{q}": holds[(p, q)] for p in names for q in names
        },
        "implications_nonvacuous": {
            f"{p}->{q}": holds[(p, q)]
            for p in names
            for q in names
            if extents[p] > 0
        },
        "countermodels": {
            f"{p}->{q}": cm for (p, q), cm in sorted(counter.items())
        },
    }


# ---------------------------------------------------------------------------
# The two-element question
# ---------------------------------------------------------------------------


def pointed_maps(src: Pointed, dst: Pointed) -> list[Func]:
    """All functions between the carriers preserving the designated
    points."""
    return [
        f
        for f in all_functions_between(src.n, dst.n)
        if f[src.a] == dst.a and f[src.b] == dst.b
    ]


def all_functions_between(n: int, m: int) -> list[Func]:
    return [tuple(f) for f in product(range(m), repeat=n)]


def preserves_rel(f: Func, src: Pointed, dst: Pointed) -> bool:
    return all((f[x], f[y]) in dst.rel for (x, y) in src.rel)


D2 = Pointed(2, frozenset({(0, 1)}), 0, 1)
S2 = Pointed(2, frozenset({(0, 1), (1, 0)}), 0, 1)
D2_REV = Pointed(2, frozenset({(1, 0)}), 0, 1)

# The unique non-identity permutation of the two-element carrier.
# Corresponds to ``Bool.not`` on ``{false, true}`` with ``false=0``.
CARRIER_SWAP: Func = (1, 0)
CARRIER_ID: Func = (0, 1)


def two_element_report(max_n: int) -> dict[str, object]:
    """Initiality of the oriented two-element structure among pointed
    witnessed structures, minimal carriers per axiom set, and
    non-forcedness evidence, all by brute force."""
    initial_ok = 0
    checked = 0
    for n in range(1, max_n + 1):
        for s in enumerate_pointed(n):
            if not a1(s):
                continue
            checked += 1
            maps = [
                f for f in pointed_maps(D2, s) if preserves_rel(f, D2, s)
            ]
            if len(maps) == 1:
                initial_ok += 1
    min_carrier = {}
    for axiom_set, pred in (
        ("bare", a1),
        ("irreflexive", a1i),
        (
            "irreflexive+symmetric",
            lambda s: a1i(s)
            and all((y, x) in s.rel for (x, y) in s.rel),
        ),
    ):
        found = None
        for n in range(1, max_n + 1):
            if any(pred(s) for s in enumerate_pointed(n)):
                found = n
                break
        min_carrier[axiom_set] = found
    return {
        "scope": f"all witnessed pointed structures, carrier <= {max_n}",
        "witnessed_structures_checked": checked,
        "unique_pointed_map_from_D2": initial_ok,
        "initiality_universal_within_scope": initial_ok == checked,
        "minimal_carrier_by_axiom_set": min_carrier,
        "two_element_not_forced_without_irreflexivity": any(
            a1(s) for s in enumerate_pointed(1)
        ),
        "larger_witnessed_irreflexive_models_exist": any(
            a1i(s) for s in enumerate_pointed(3)
        ),
    }


# ---------------------------------------------------------------------------
# Observers and the orientation gap
# ---------------------------------------------------------------------------


def automorphisms(s: Pointed, pointed: bool) -> list[Func]:
    out = []
    for perm in permutations(range(s.n)):
        f = tuple(perm)
        if pointed and (f[s.a] != s.a or f[s.b] != s.b):
            continue
        if frozenset((f[x], f[y]) for (x, y) in s.rel) == s.rel:
            out.append(f)
    return out


def invariant_separating_classifiers(s: Pointed) -> list[Func]:
    """Two-valued classifiers separating the designated pair and constant
    on every (unpointed) automorphism orbit: the definable observers."""
    autos = automorphisms(s, pointed=False)
    out = []
    for f in all_functions_between(s.n, 2):
        if f[s.a] == f[s.b]:
            continue
        if all(
            all(f[g[x]] == f[x] for x in range(s.n)) for g in autos
        ):
            out.append(f)
    return out


def observer_report() -> dict[str, object]:
    rows = []
    for name, s in (("D2_oriented", D2), ("S2_symmetric", S2)):
        rows.append(
            {
                "structure": name,
                "unpointed_automorphisms": len(
                    automorphisms(s, pointed=False)
                ),
                "definable_observers": len(
                    invariant_separating_classifiers(s)
                ),
            }
        )
    return {
        "rows": rows,
        "orientation_gap": (
            rows[0]["definable_observers"] != 0
            and rows[1]["definable_observers"] == 0
        ),
    }


# ---------------------------------------------------------------------------
# Collapse: collision, obstruction-relative-to-a-law, orientation-blindness
# ---------------------------------------------------------------------------


def pushforward(rel: Rel, f: Func) -> Rel:
    return frozenset((f[x], f[y]) for (x, y) in rel)


def collision(rel: Rel, f: Func) -> bool:
    return any(f[x] == f[y] for (x, y) in rel)


def transpose(rel: Rel) -> Rel:
    return frozenset((y, x) for (x, y) in rel)


def symmetrize(rel: Rel) -> Rel:
    return rel | transpose(rel)


def irreflexive_relations_on(n: int) -> list[Rel]:
    """Every irreflexive relation on ``range(n)``, deterministic order."""
    off = [(x, y) for x in range(n) for y in range(n) if x != y]
    return [
        frozenset(p for k, p in enumerate(off) if mask >> k & 1)
        for mask in range(1 << len(off))
    ]


def transposition_report() -> dict[str, object]:
    """Carrier-2 facts about ``CARRIER_SWAP``: it carries each orientation
    onto the other, squares to the identity, is an automorphism of the
    symmetrization and not of either orientation, and the unpointed
    inhabited irreflexive relations are exactly those three."""
    twice = compose(CARRIER_SWAP, CARRIER_SWAP)
    nonempty = [rel for rel in irreflexive_relations_on(2) if rel]
    three = frozenset({D2.rel, D2_REV.rel, S2.rel})
    return {
        "swap_pushes_D2_to_D2rev": (
            pushforward(D2.rel, CARRIER_SWAP) == D2_REV.rel
        ),
        "swap_pushes_D2rev_to_D2": (
            pushforward(D2_REV.rel, CARRIER_SWAP) == D2.rel
        ),
        "swap_twice_is_identity": twice == CARRIER_ID,
        "swap_twice_restores_D2": pushforward(D2.rel, twice) == D2.rel,
        "swap_twice_restores_D2rev": pushforward(D2_REV.rel, twice) == D2_REV.rel,
        "sym_D2_is_S2": symmetrize(D2.rel) == S2.rel,
        "sym_D2rev_is_S2": symmetrize(D2_REV.rel) == S2.rel,
        "swap_is_auto_of_S2": pushforward(S2.rel, CARRIER_SWAP) == S2.rel,
        "swap_is_not_auto_of_D2": pushforward(D2.rel, CARRIER_SWAP) != D2.rel,
        "swap_is_not_auto_of_D2rev": (
            pushforward(D2_REV.rel, CARRIER_SWAP) != D2_REV.rel
        ),
        "unpointed_irrefl_nonempty_count": len(nonempty),
        "unpointed_irrefl_nonempty_are_exactly_the_three": (
            frozenset(nonempty) == three
        ),
    }


def collapse_report(max_n: int) -> dict[str, object]:
    """Exhaustive verification over the declared scope:

    * pushforward irreflexivity fails exactly on collisions;
    * collision is invariant under transposition (orientation-blind);
    * identifying a witnessed pair always collides (an obstruction relative to the
      irreflexivity commitment) while the pushforward always exists as a
      bare structure (no obstruction without it)."""
    checked = 0
    for n in range(1, max_n + 1):
        for s in enumerate_pointed(n):
            for x in range(n):
                for y in range(n):
                    if x == y:
                        continue
                    f = merge_map(n, x, y)
                    checked += 1
                    assert collision(s.rel, f) == (
                        not irreflexive(pushforward(s.rel, f))
                    ), "collision must equal pushforward reflexivity"
                    assert collision(s.rel, f) == collision(transpose(s.rel), f)
                    if a1(s) and f[s.a] == f[s.b]:
                        assert collision(s.rel, f)
                    assert isinstance(pushforward(s.rel, f), frozenset)
    return {
        "scope": f"all pointed structures and merges, carrier <= {max_n}",
        "merge_cases_checked": checked,
        "collision_iff_pushforward_not_irreflexive": True,
        "collision_transpose_invariant": True,
        "identifying_witnessed_pair_always_collides": True,
        "pushforward_always_exists": True,
    }


# ---------------------------------------------------------------------------
# Minimal carriers for k distinctions; obstruction-profile frontier
# ---------------------------------------------------------------------------


def min_carrier_for_k(k: int, oriented: bool, max_n: int = 8) -> Optional[int]:
    """Smallest carrier hosting k distinct irreflexive asserted pairs."""
    for n in range(1, max_n + 1):
        capacity = n * (n - 1) if oriented else n * (n - 1) // 2
        if capacity >= k:
            return n
    return None  # pragma: no cover - max_n is ample for the table


def carrier_table(max_k: int) -> dict[str, object]:
    return {
        "oriented": {
            str(k): min_carrier_for_k(k, True) for k in range(1, max_k + 1)
        },
        "unordered": {
            str(k): min_carrier_for_k(k, False) for k in range(1, max_k + 1)
        },
    }


def collision_profile(s: Pointed) -> frozenset[tuple[int, int]]:
    """Which merges collide: the collapse-level shadow of the structure."""
    return frozenset(
        (x, y)
        for x in range(s.n)
        for y in range(s.n)
        if x < y and collision(s.rel, merge_map(s.n, x, y))
    )


def pointed_isomorphic(s: Pointed, t: Pointed) -> bool:
    """Pointed isomorphism: some carrier bijection transports the
    designated points onto the designated points and the relation onto
    the relation.  The bijection may move the raw point indices."""
    if s.n != t.n:
        return False
    for perm in permutations(range(s.n)):
        f = tuple(perm)
        if f[s.a] != t.a or f[s.b] != t.b:
            continue
        if frozenset((f[x], f[y]) for (x, y) in s.rel) == t.rel:
            return True
    return False


def frontier_profile_countermodel() -> dict[str, object]:
    """Obstruction profiles do not classify pointed structures: the
    oriented edge and its reverse share a profile yet are not
    pointed-isomorphic."""
    same_profile = collision_profile(D2) == collision_profile(D2_REV)
    iso = pointed_isomorphic(D2, D2_REV)
    return {
        "left": D2.json(),
        "right": D2_REV.json(),
        "profiles_equal": same_profile,
        "pointed_isomorphic": iso,
        "profiles_classify": not (same_profile and not iso),
    }
