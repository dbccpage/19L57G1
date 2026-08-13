"""Deterministic mirror of ``lean4/Derivation/Compression.lean``.

Target-relative presentation compression over a represented finite
domain.  Mirrored results: factorization through a presentation is
exactly fiber-constancy (A); the signature quotient is exact,
adequate, and factors through every adequate presentation, uniquely
on that presentation's image (B); a descent failure is witnessed by a
declared question (C); enlargement refines and a split is exactly a
new separator across an old agreement (D); absolute adequacy is
exactly injectivity — every genuine compression is adequate only
relative to a declared, represented question family (E); duplicating
the family or appending a digest of existing answers refines nothing,
and a genuine split requires a question that is not
signature-determined (F); the class count is bounded by the domain
size and strictly increases under splits.

Declared exhaustive bounds: ``D = range(n)`` for ``n <= max_n``;
questions and presentations are total functions on ``D`` represented
as tuples into ``range(m)`` for ``m <= max_m``; families are ordered
tuples of at most ``max_family`` questions.  Off-domain values are
irrelevant to every mirrored statement and are not represented; the
unconditional statements are the Lean theorems.
"""

from __future__ import annotations

from itertools import product

from derivation.export import Json

Fn = tuple[int, ...]
Family = tuple[Fn, ...]

MAX_N = 3
MAX_M = 3
MAX_FAMILY = 2


def all_functions(n: int, m: int) -> list[Fn]:
    """All functions from ``range(n)`` to ``range(m)``, as tuples."""
    return [f for f in product(range(m), repeat=n)]


def all_families(n: int, m: int, max_size: int) -> list[Family]:
    """All ordered families of at most ``max_size`` questions."""
    fns = all_functions(n, m)
    out: list[Family] = []
    for size in range(max_size + 1):
        out.extend(product(fns, repeat=size))
    return out


def sig_list(Q: Family, x: int) -> Fn:
    """The answer signature of ``x`` under ``Q``, in family order."""
    return tuple(q[x] for q in Q)


def sig_eq(Q: Family, x: int, xp: int) -> bool:
    """Agreement of ``x`` and ``xp`` on every question of ``Q``."""
    return all(q[x] == q[xp] for q in Q)


def adequate(D: list[int], Q: Family, p: Fn) -> bool:
    """Points of ``D`` merged by ``p`` agree on every question."""
    return all(
        sig_eq(Q, x, xp)
        for x in D for xp in D if p[x] == p[xp])


def fiber_constant(D: list[int], p: Fn, q: Fn) -> bool:
    """The fibers of ``p`` over ``D`` are ``q``-constant."""
    return all(
        q[x] == q[xp]
        for x in D for xp in D if p[x] == p[xp])


def valid_factor_maps(
    D: list[int], p: Fn, q: Fn, m: int
) -> list[dict[int, int]]:
    """All maps on the ``p``-image of ``D`` (into ``range(m)``)
    factoring ``q`` through ``p``.  Off-image values never constrain
    the factoring equations, so this search is exhaustive for the
    mirrored statement."""
    image = sorted({p[x] for x in D})
    out: list[dict[int, int]] = []
    for values in product(range(m), repeat=len(image)):
        g = dict(zip(image, values))
        if all(g[p[x]] == q[x] for x in D):
            out.append(g)
    return out


def factors_on(D: list[int], p: Fn, q: Fn, m: int) -> bool:
    """``q`` factors through ``p`` on ``D`` (brute-force search)."""
    return len(valid_factor_maps(D, p, q, m)) > 0


def first_with_sig(D: list[int], Q: Family, s: Fn) -> int:
    """First element of ``D`` with signature ``s`` (``0`` if none,
    mirroring the Lean ``getD 0`` default)."""
    for d in D:
        if sig_list(Q, d) == s:
            return d
    return 0


def p_quotient(D: list[int], Q: Family) -> Fn:
    """The signature quotient presentation: each point of ``D`` goes
    to the first element of ``D`` carrying the same signature."""
    return tuple(first_with_sig(D, Q, sig_list(Q, x)) for x in D)


def injective_on(D: list[int], p: Fn) -> bool:
    """``p`` is injective on ``D``."""
    return all(
        x == xp
        for x in D for xp in D if p[x] == p[xp])


def splits_at(D: list[int], Q: Family, Qp: Family, x: int) -> bool:
    """The class of ``x`` splits under the enlargement ``Qp``."""
    return any(
        sig_eq(Q, x, xp) and not sig_eq(Qp, x, xp) for xp in D)


def sig_determined(D: list[int], Q: Family, q: Fn) -> bool:
    """``q`` is a function of the ``Q``-signature on ``D``."""
    return all(
        q[x] == q[xp]
        for x in D for xp in D
        if sig_list(Q, x) == sig_list(Q, xp))


def realized_sigs(D: list[int], Q: Family) -> list[Fn]:
    """The distinct signatures realized on ``D``, in first-occurrence
    order."""
    seen: list[Fn] = []
    for x in D:
        s = sig_list(Q, x)
        if s not in seen:
            seen.append(s)
    return seen


def digests(D: list[int], Q: Family, m: int) -> list[Fn]:
    """All digest questions ``x -> f(sig(x))`` for ``f`` into
    ``range(m)``: every hash or replay record of the existing answers
    is one of these."""
    sigs = realized_sigs(D, Q)
    out: list[Fn] = []
    for values in product(range(m), repeat=len(sigs)):
        f = dict(zip(sigs, values))
        out.append(tuple(f[sig_list(Q, x)] for x in D))
    return out


def partition_of(D: list[int], Q: Family) -> list[list[int]]:
    """The signature classes of ``D``, sorted by least member."""
    groups: dict[Fn, list[int]] = {}
    for x in D:
        groups.setdefault(sig_list(Q, x), []).append(x)
    return sorted(groups.values(), key=lambda g: g[0])


def class_count(D: list[int], Q: Family) -> int:
    """The number of distinct signatures on ``D``."""
    return len({sig_list(Q, x) for x in D})


# -- A: factorization ------------------------------------------------

def factorization_iff_exhaustive(max_n: int, max_m: int) -> bool:
    """Mirror of ``factors_iff_fiberConstant``: over every domain,
    presentation, and question within bounds, factoring is exactly
    fiber-constancy."""
    return all(
        factors_on(list(range(n)), p, q, m)
        == fiber_constant(list(range(n)), p, q)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for p in all_functions(n, m)
        for q in all_functions(n, m))


def factor_unique_on_image_exhaustive(max_n: int, max_m: int) -> bool:
    """Mirror of ``factor_unique_on_image``: any two factoring maps
    agree on the image of the domain."""
    return all(
        g1[p[x]] == g2[p[x]]
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for p in all_functions(n, m)
        for q in all_functions(n, m)
        for g1 in valid_factor_maps(list(range(n)), p, q, m)
        for g2 in valid_factor_maps(list(range(n)), p, q, m)
        for x in range(n))


def off_image_countermodel() -> dict[str, Json]:
    """Mirror of ``factor_not_unique_off_image``: on ``D = [0]`` with
    identity presentation and question, two factoring maps agree on
    the image ``{0}`` but differ at the off-image value ``1``."""
    D = [0]
    p: Fn = (0,)
    q: Fn = (0,)
    g1 = {0: 0, 1: 0}
    g2 = {0: 0, 1: 1}
    return {
        "domain": list(D),
        "g1_factors": all(g1[p[x]] == q[x] for x in D),
        "g2_factors": all(g2[p[x]] == q[x] for x in D),
        "agree_on_image": all(g1[p[x]] == g2[p[x]] for x in D),
        "maps_differ": g1 != g2,
    }


# -- B: the signature quotient ---------------------------------------

def sig_iff_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``sigEq_iff_sigList``: family agreement is exactly
    signature equality."""
    return all(
        sig_eq(Q, x, xp)
        == (sig_list(Q, x) == sig_list(Q, xp))
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family)
        for x in range(n)
        for xp in range(n))


def quotient_exact_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``pQ_exact``: the fibers of the quotient over ``D``
    are exactly the signature classes."""
    return all(
        (p_quotient(list(range(n)), Q)[x]
         == p_quotient(list(range(n)), Q)[xp])
        == sig_eq(Q, x, xp)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family)
        for x in range(n)
        for xp in range(n))


def quotient_adequate_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``pQ_adequate``."""
    return all(
        adequate(list(range(n)), Q, p_quotient(list(range(n)), Q))
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family))


def quotient_coarsest_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``pQ_coarsest``: the quotient factors through every
    adequate presentation (checked both as fiber-constancy and by
    explicit factor search; quotient values lie in ``range(n)``)."""
    return all(
        fiber_constant(list(range(n)), p,
                       p_quotient(list(range(n)), Q))
        and factors_on(list(range(n)), p,
                       p_quotient(list(range(n)), Q), n)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family)
        for p in all_functions(n, m)
        if adequate(list(range(n)), Q, p))


# -- C: descent failure witnessed ------------------------------------

def descent_witnessed_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``descent_witness``: whenever a presentation merges
    a separated pair, some declared question answers differently on
    the pair and is not fiber-constant."""
    return all(
        any(q[x] != q[xp]
            and not fiber_constant(list(range(n)), p, q)
            for q in Q)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family)
        for p in all_functions(n, m)
        for x in range(n)
        for xp in range(n)
        if p[x] == p[xp] and not sig_eq(Q, x, xp))


def descent_instance_count(
    max_n: int, max_m: int, max_family: int
) -> int:
    """Number of merged-but-separated instances checked above."""
    return sum(
        1
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family)
        for p in all_functions(n, m)
        for x in range(n)
        for xp in range(n)
        if p[x] == p[xp] and not sig_eq(Q, x, xp))


# -- D: enlargement refines; split characterization ------------------

def enlargements(
    n: int, m: int, max_family: int
) -> list[tuple[Family, Family]]:
    """All pairs ``(Q, Q + R)`` with ``|Q| <= max_family`` and
    ``|R| <= 1``."""
    fns = all_functions(n, m)
    extras: list[Family] = [()] + [(q,) for q in fns]
    return [
        (Q, Q + R)
        for Q in all_families(n, m, max_family)
        for R in extras]


def enlarge_refines_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``enlarge_refines``: agreement on the enlarged
    family implies agreement on the old one."""
    return all(
        (not sig_eq(Qp, x, xp)) or sig_eq(Q, x, xp)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for (Q, Qp) in enlargements(n, m, max_family)
        for x in range(n)
        for xp in range(n))


def split_characterization_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``splits_iff_new_separator``: a class splits exactly
    when the enlarged family carries a separator across an old
    agreement."""
    return all(
        splits_at(list(range(n)), Q, Qp, x)
        == any(
            sig_eq(Q, x, xp)
            and any(qp[x] != qp[xp] for qp in Qp)
            for xp in range(n))
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for (Q, Qp) in enlargements(n, m, max_family)
        for x in range(n))


def split_count(max_n: int, max_m: int, max_family: int) -> int:
    """Number of (enlargement, point) split instances in bounds."""
    return sum(
        1
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for (Q, Qp) in enlargements(n, m, max_family)
        for x in range(n)
        if splits_at(list(range(n)), Q, Qp, x))


# -- E: no absolute adequacy without a declared family ---------------

def absolute_adequacy_iff_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``absolute_adequacy_iff_injective``: adequacy for
    every family in the declared enumeration (codomain up to
    ``max_m``, which contains the indicator questions used by the
    Lean proof) is exactly injectivity on the domain."""
    return all(
        all(adequate(list(range(n)), Q, p)
            for Q in all_families(n, max_m, max_family))
        == injective_on(list(range(n)), p)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for p in all_functions(n, m))


# -- F: repetition, digests, replay ----------------------------------

def dup_no_refine_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``dup_no_refine``: duplicating the family separates
    nothing new."""
    return all(
        sig_eq(Q + Q, x, xp) == sig_eq(Q, x, xp)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family)
        for x in range(n)
        for xp in range(n))


def digest_no_refine_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``postcompose_no_refine``: appending any digest of
    the existing answers separates nothing new."""
    return all(
        sig_eq(Q + (dg,), x, xp) == sig_eq(Q, x, xp)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family)
        for dg in digests(list(range(n)), Q, m)
        for x in range(n)
        for xp in range(n))


def separator_required_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``refine_requires_separator``: whenever a class
    splits, the enlarged family contains a question that is not
    signature-determined on the domain."""
    return all(
        any(not sig_determined(list(range(n)), Q, qp) for qp in Qp)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for (Q, Qp) in enlargements(n, m, max_family)
        for x in range(n)
        if splits_at(list(range(n)), Q, Qp, x))


# -- Class-count measure and refinement bound ------------------------

def class_bound_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``refine_bounded``: the class count never exceeds
    the domain length."""
    return all(
        class_count(list(range(n)), Q) <= n
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family))


def class_pos_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``classCount_pos``: at least one class on a
    nonempty domain."""
    return all(
        class_count(list(range(n)), Q) >= 1
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for Q in all_families(n, m, max_family))


def strict_split_increases_exhaustive(
    max_n: int, max_m: int, max_family: int
) -> bool:
    """Mirror of ``strict_split_increases``: an enlargement that
    splits some class strictly increases the class count."""
    return all(
        class_count(list(range(n)), Q)
        < class_count(list(range(n)), Qp)
        for n in range(1, max_n + 1)
        for m in range(1, max_m + 1)
        for (Q, Qp) in enlargements(n, m, max_family)
        if any(splits_at(list(range(n)), Q, Qp, x)
               for x in range(n)))


# -- Countermodels to refinement uniqueness --------------------------

def countermodel_instances() -> dict[str, Json]:
    """Mirrors of ``refinement_not_unique`` and ``refinement_tie``:
    on ``D = [0,1,2]`` from the empty family, the indicator
    enlargements of ``0`` and of ``1`` both split the single class,
    have equal cost (one question each), and induce different class
    structures — the tie is recorded, neither is unique-minimum."""
    D = [0, 1, 2]
    ind0: Fn = (1, 0, 0)
    ind1: Fn = (0, 1, 0)
    base: Family = ()
    fam1: Family = (ind0,)
    fam2: Family = (ind1,)
    part1 = partition_of(D, fam1)
    part2 = partition_of(D, fam2)
    return {
        "domain": list(D),
        "family_base": [],
        "family_one": [list(ind0)],
        "family_two": [list(ind1)],
        "both_split_at_zero": (
            splits_at(D, base, fam1, 0)
            and splits_at(D, base, fam2, 0)),
        "equal_cost": len(fam1) == len(fam2),
        "classes_one": [list(g) for g in part1],
        "classes_two": [list(g) for g in part2],
        "classes_differ": part1 != part2,
        "class_count_increases": (
            class_count(D, fam1) > class_count(D, base)
            and class_count(D, fam2) > class_count(D, base)),
    }
