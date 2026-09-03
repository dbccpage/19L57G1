"""Stage 1: the layer's characters, the value-carrier menu, and the fresh
totals, recomputed independently of Lean.

The layer of part count ``n`` has members ``0..n-1``.  Its step action is the
one the pinned sibling defines: the step ``a`` sends the member ``c`` to
``a * c`` taken in ``n``.  A CHARACTER indexed by step ``a`` sends ``c`` to
the value carrier's generator carried along that exponent; the carrier-free
record of the whole character is therefore the exponent word.

Six value carriers, frozen in ``PREDICTIONS.md`` before this file was
written.  Each answers, for a part count and a step: what the character's
values are, whether they are integers, what the fresh total is, and whether
that total is a plain integer multiple of the carrier's unit.

Nothing here claims a total equals anything.  AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

MENU: tuple[str, ...] = ("V1", "V2", "V3", "V4", "V5", "V6")
STEP_RULES: tuple[str, ...] = ("R0", "R1", "Rlast", "Rself")


# ---------------------------------------------------------------- the layer


def fresh_members(n: int) -> list[int]:
    """The fresh members of the layer of part count ``n``, increasing.

    Mirrors the pinned `freshCount`'s own filter over `range n`."""

    return [c for c in range(n) if gcd(c, n) == 1]


def fresh_count(n: int) -> int:
    return len(fresh_members(n))


def exponent(n: int, a: int, c: int) -> int:
    """The step action on values: the member carried by the step."""

    return (a * c) % n


def fresh_exp(n: int, a: int) -> list[int]:
    """The exponent multiset of the fresh total at step ``a``."""

    return [exponent(n, a, c) for c in fresh_members(n)]


def divisors_below(n: int) -> list[int]:
    return [d for d in range(n) if d != 0 and n % d == 0]


def divisors(n: int) -> list[int]:
    return divisors_below(n) + [n]


def balance_table_reference(limit: int) -> list[int]:
    """The pinned balance by its own divisor recursion, literally: one sum
    over the proper divisors per part count.  Index 0 unused.  Quadratic, and
    the reference the fast route is checked against."""

    out = [0] * (limit + 1)
    if limit >= 1:
        out[1] = 1
    for n in range(2, limit + 1):
        out[n] = -sum(out[d] for d in divisors_below(n))
    return out


def balance_table(limit: int) -> list[int]:
    """The same recursion, accumulated forward instead of summed backward:
    when a part count is reached its value is final, so it is subtracted from
    every multiple at once.  Cross-checked against the reference route by
    `test_fresh_characters.py`."""

    out = [0] * (limit + 1)
    if limit >= 1:
        out[1] = 1
    for d in range(1, limit + 1):
        v = out[d]
        if v == 0:
            continue
        for m in range(2 * d, limit + 1, d):
            out[m] -= v
    return out


def step_of(rule: str, n: int) -> int:
    """The four declared step rules, taken in the part count."""

    if rule == "R0":
        return 0
    if rule == "R1":
        return 1 % n
    if rule == "Rlast":
        return (n - 1) % n
    if rule == "Rself":
        return n % n
    raise ValueError(rule)


# ------------------------------------------------------- integer combinations

Poly = list[int]


def trim(p: Poly) -> Poly:
    q = list(p)
    while q and q[-1] == 0:
        q.pop()
    return q


def padd(p: Poly, q: Poly) -> Poly:
    m = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(m)]


def psub(p: Poly, q: Poly) -> Poly:
    return padd(p, [-x for x in q])


def shift(k: int, p: Poly) -> Poly:
    return [0] * k + list(p)


def mono_one(k: int) -> Poly:
    return shift(k, [1])


def pdivmod(p: Poly, g: Poly) -> tuple[Poly, Poly]:
    """Division with remainder by a MONIC divisor, from the top.

    Every divisor this tree uses is monic, so the division stays in the
    integers.  Mirrors the Lean `pdivmod`."""

    r = trim(p)
    tg = trim(g)
    q: Poly = []
    if not tg:
        return (q, r)
    while len(r) >= len(tg):
        k = len(r) - len(tg)
        c = r[-1]
        r = trim(psub(r, shift(k, [c * x for x in tg])))
        q = padd(q, shift(k, [c]))
    return (trim(q), r)


def layer_diff(n: int) -> Poly:
    """The layer's own difference: the generator's `n`-th power, less the
    unit."""

    return psub(mono_one(n), [1])


_FRESH_PART_CACHE: dict[int, Poly] = {}


def fresh_part(n: int) -> Poly:
    """The fresh part of the layer, by the same divisor recursion the pinned
    balance uses."""

    hit = _FRESH_PART_CACHE.get(n)
    if hit is not None:
        return hit
    acc = layer_diff(n)
    for d in divisors_below(n):
        quotient, remainder = pdivmod(acc, fresh_part(d))
        if remainder:
            raise AssertionError(f"fresh part of {d} does not divide the layer {n} exactly")
        acc = quotient
    _FRESH_PART_CACHE[n] = acc
    return acc


def fresh_poly(n: int, a: int) -> Poly:
    acc: Poly = []
    for e in fresh_exp(n, a):
        acc = padd(acc, mono_one(e))
    return trim(acc)


# ------------------------------------------------------------- the six carriers


@dataclass(frozen=True)
class TotalReport:
    """One fresh total, read under one value carrier."""

    carrier: str
    n: int
    a: int
    defined: bool
    term_values: tuple[int, ...] | None
    """The character's values at the fresh members, when they are integers."""
    is_integer_total: bool
    integer_total: int | None
    note: str


def _v1(n: int, a: int) -> TotalReport:
    # additive receiver: the value at c is the receiver element (a*c mod n)/n,
    # and totals are added there, so the total is (sum of exponents mod n)/n.
    numer = sum(fresh_exp(n, a)) % n
    return TotalReport(
        "V1", n, a, True, None, False, None,
        f"receiver element {numer}/{n}; character values are added, so the total is a "
        f"receiver element and never an integer count",
    )


def _v2(n: int, a: int) -> TotalReport:
    terms = tuple(1 for _ in fresh_members(n))
    return TotalReport("V2", n, a, True, terms, True, len(terms),
                       "every character value is the unit, so the total is the fresh count")


def _v3(n: int, a: int) -> TotalReport:
    vec = fresh_poly(n, a)
    const = len(vec) <= 1
    return TotalReport("V3", n, a, True, None, const, (vec[0] if vec else 0) if const else None,
                       "formal integer combination of members; no relation imposed")


def _v4_reduce(n: int, vec: Poly) -> Poly:
    # modulo the single relation that the sum of all members is zero
    full = [1] * n
    v = list(vec) + [0] * (n - len(vec))
    top = v[n - 1]
    if top:
        v = [v[i] - top * full[i] for i in range(n)]
    return trim(v)


def _v4(n: int, a: int) -> TotalReport:
    vec = _v4_reduce(n, fresh_poly(n, a))
    const = len(vec) <= 1
    return TotalReport("V4", n, a, True, None, const, (vec[0] if vec else 0) if const else None,
                       "modulo the total of all members")


def _v5(n: int, a: int) -> TotalReport:
    if n % 2 != 0:
        return TotalReport("V5", n, a, False, None, False, None,
                           "the sign carrier is declared only at even part counts")
    terms = tuple((-1) ** ((a * c) % 2) for c in fresh_members(n))
    return TotalReport("V5", n, a, True, terms, True, sum(terms),
                       "two-element sign carrier")


def _v6(n: int, a: int) -> TotalReport:
    vec = trim(pdivmod(fresh_poly(n, a), fresh_part(n))[1])
    const = len(vec) <= 1
    return TotalReport("V6", n, a, True, None, const, (vec[0] if vec else 0) if const else None,
                       "modulo the layer's fresh part")


_CARRIERS = {"V1": _v1, "V2": _v2, "V3": _v3, "V4": _v4, "V5": _v5, "V6": _v6}


def total(carrier: str, n: int, a: int) -> TotalReport:
    if n < 1:
        raise ValueError("part counts start at one")
    return _CARRIERS[carrier](n, a % n)


# --------------------------------------------------------- the stage-1 targets


def target_report(limit: int) -> dict[str, object]:
    """The four stage-1 targets, recomputed per menu member up to ``limit``.

    Lean proves them carrier-free on the exponent word; this recomputation is
    the independent check the tree owes its own Lean statements."""

    bal = balance_table(limit)
    rows: list[dict[str, object]] = []
    for carrier in MENU:
        trivial_ok: list[int] = []
        trivial_miss: list[int] = []
        defined: list[int] = []
        for n in range(1, limit + 1):
            rep = total(carrier, n, 0)
            if not rep.defined:
                continue
            defined.append(n)
            if rep.is_integer_total and rep.integer_total == fresh_count(n):
                trivial_ok.append(n)
            else:
                trivial_miss.append(n)
        rows.append({
            "carrier": carrier,
            "defined_at": len(defined),
            "trivial_total_is_fresh_count": len(trivial_miss) == 0,
            "trivial_total_misses": trivial_miss[:8],
            "obstruction": (
                "" if not trivial_miss else
                "the step-zero total is not the fresh count at the part counts listed"
            ),
        })
    # carrier-free targets, checked directly on the exponent word
    wf_misses: list[int] = []
    restrict_misses: list[tuple[int, int, int, int]] = []
    injective_misses: list[tuple[int, int, int]] = []
    for n in range(1, limit + 1):
        if fresh_exp(n, 0) != [0] * fresh_count(n):
            wf_misses.append(n)
        for d in divisors_below(n) + [n]:
            q = n // d
            for a in range(min(n, 6)):
                for c in range(min(d, 6)):
                    if exponent(n, a, c * q) != q * exponent(d, a, c):
                        restrict_misses.append((n, d, a, c))
        for a in range(min(n, 8)):
            for b in range(a + 1, min(n, 8)):
                if all(exponent(n, a, c) == exponent(n, b, c) for c in range(n)):
                    injective_misses.append((n, a, b))
    return {
        "limit": limit,
        "menu": list(MENU),
        "rows": rows,
        "character_trivial_total_misses": wf_misses,
        "character_restricts_misses": restrict_misses[:8],
        "characters_are_steps_misses": injective_misses[:8],
        "balance_head": bal[1 : min(limit, 12) + 1],
    }
