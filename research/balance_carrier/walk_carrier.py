"""Stage 2: the walk carrier -- the frozen menu, the four declared counts,
the exhaustive search at ``N <= 12``, and the extension routes.

The class (frozen in ``PREDICTIONS.md``): objects ``1..N``; arrows
``d -> m`` exactly when ``d`` divides ``m`` and ``d < m``; five weights
built from the balance, the divisor quotient and the constants; four
declared signed counts -- S1 walk sums, S1b totalled walk sums, S2 the
alternating sum over bijections of a square table with a declared
diagonal and first column, S3 signed section counts.  Ninety candidates,
each compared with the running balance at every ``N`` in ``1..12``.

Routes for S2 (declared readings 7): the literal alternating sum over all
``N!`` arrangements where affordable; fraction-free row elimination; and,
for a unit-magnitude diagonal, the reduction of the first column by the
other columns to a triangular table ("the column route").  The last two
rest on two elementary facts about the alternating sum (METATHEORY, not
proved in this tree) and are cross-checked against the literal count
wherever both run.  Nothing here uses floating point.

AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import permutations, product
from operator import mul

MENU_BOUND: int = 12
UNPRUNED_BOUND: int = 8
ELIMINATION_BOUND: int = 60
DIRECT_BOUND: int = 1_000
CHECKPOINTS: tuple[int, ...] = (10, 30, 100, 1_000, 10_000, 100_000, 1_000_000)
STEPPED_CHECKPOINTS: tuple[int, ...] = tuple(range(2_000, 10_001, 1_000))

WEIGHTS: tuple[str, ...] = ("W0", "W1", "W2", "W3", "W4")
DIAGONALS: tuple[int, ...] = (0, 1, -1)
COLUMNS: tuple[str, ...] = ("C0", "C1", "C-1", "Cbal", "C-bal")


def balance_table(limit: int) -> list[int]:
    """The balance at ``0..limit`` by the pinned divisor recursion:
    ``vals[1] = 1``; every proper divisor ``d`` of ``m`` contributes
    ``-vals[d]`` to ``vals[m]``."""

    vals = [0] * (limit + 1)
    if limit >= 1:
        vals[1] = 1
    for d in range(1, limit + 1):
        contribution = vals[d]
        if contribution != 0:
            for m in range(2 * d, limit + 1, d):
                vals[m] -= contribution
    return vals


def running_balance_table(bal: list[int]) -> list[int]:
    """Prefix sums of the balance: ``run[n]`` is the running balance at ``n``."""

    run = [0] * len(bal)
    total = 0
    for n in range(1, len(bal)):
        total += bal[n]
        run[n] = total
    return run


def proper_divisors(m: int) -> list[int]:
    return [d for d in range(1, m) if m % d == 0]


def weight(index: str, d: int, m: int, bal: list[int]) -> int:
    """The frozen weight menu on the arrow ``d -> m``, quotient ``q = m / d``."""

    q = m // d
    if index == "W0":
        return 0
    if index == "W1":
        return 1
    if index == "W2":
        return -1
    if index == "W3":
        return bal[q]
    if index == "W4":
        return -bal[q]
    raise ValueError(index)


def first_column(index: str, i: int, bal: list[int]) -> int:
    """The declared first column at row ``i >= 2``."""

    if index == "C0":
        return 0
    if index == "C1":
        return 1
    if index == "C-1":
        return -1
    if index == "Cbal":
        return bal[i]
    if index == "C-bal":
        return -bal[i]
    raise ValueError(index)


def weight_vector(index: str, i: int, n: int, bal: list[int]) -> list[int]:
    """The weights ``w(i -> j)`` for the multiples ``j = 2i, 3i, ..., <= n``
    of ``i``, in that order -- the same values as ``weight``, laid out for
    the strided loops of the recursion and the column route."""

    count = n // i - 1
    if count <= 0:
        return []
    if index == "W0":
        return [0] * count
    if index == "W1":
        return [1] * count
    if index == "W2":
        return [-1] * count
    if index == "W3":
        return bal[2 : count + 2]
    if index == "W4":
        return [-b for b in bal[2 : count + 2]]
    raise ValueError(index)


# ---------------------------------------------------------------- S1, S1b


def walk_sums(windex: str, limit: int, bal: list[int]) -> list[int]:
    """S1 at every ``m <= limit`` by the proper-divisor recursion: the empty
    chain at ``1`` contributes ``1``; a chain to ``m`` is a chain to a proper
    divisor ``d`` extended by the arrow ``d -> m``."""

    ws = [0] * (limit + 1)
    if limit >= 1:
        ws[1] = 1
    for d in range(1, limit + 1):
        here = ws[d]
        if here == 0:
            continue
        weights = weight_vector(windex, d, limit, bal)
        if not weights:
            continue
        segment = ws[2 * d :: d]
        ws[2 * d :: d] = [a + here * w for a, w in zip(segment, weights)]
    return ws


def chains_to(m: int) -> list[list[int]]:
    """Every strict divisor chain from ``1`` to ``m``, bottom first."""

    if m == 1:
        return [[1]]
    out: list[list[int]] = []
    for d in proper_divisors(m):
        for c in chains_to(d):
            out.append(c + [m])
    return out


def chain_weight(windex: str, chain: list[int], bal: list[int]) -> int:
    w = 1
    for a, b in zip(chain, chain[1:]):
        w *= weight(windex, a, b, bal)
    return w


def walk_sum_literal(windex: str, m: int, bal: list[int]) -> int:
    """S1 at ``m`` by enumerating the chains themselves."""

    return sum(chain_weight(windex, c, bal) for c in chains_to(m))


def total_walk_sums(windex: str, limit: int, bal: list[int]) -> list[int]:
    """S1b at every ``N <= limit``: S1 totalled over the endpoints ``1..N``."""

    ws = walk_sums(windex, limit, bal)
    out = [0] * (limit + 1)
    total = 0
    for n in range(1, limit + 1):
        total += ws[n]
        out[n] = total
    return out


# --------------------------------------------------------------------- S2


def table(windex: str, delta: int, cindex: str, n: int, bal: list[int]) -> list[list[int]]:
    """The menu table as a ``0``-indexed list of rows; row ``i`` and column
    ``j`` of the table are entry ``[i - 1][j - 1]``."""

    rows: list[list[int]] = []
    for i in range(1, n + 1):
        row: list[int] = []
        for j in range(1, n + 1):
            if i == j:
                row.append(delta)
            elif j == 1:
                row.append(first_column(cindex, i, bal))
            elif j % i == 0:
                row.append(weight(windex, i, j, bal))
            else:
                row.append(0)
        rows.append(row)
    return rows


def inversion_sign(arrangement: tuple[int, ...]) -> int:
    inv = 0
    for a in range(len(arrangement)):
        for b in range(a + 1, len(arrangement)):
            if arrangement[a] > arrangement[b]:
                inv += 1
    return 1 if inv % 2 == 0 else -1


def table_count_literal(rows: list[list[int]]) -> int:
    """S2 as declared: the alternating sum over every arrangement of the
    signed row products."""

    n = len(rows)
    total = 0
    for arrangement in permutations(range(n)):
        term = inversion_sign(arrangement)
        for i, j in enumerate(arrangement):
            if term == 0:
                break
            term *= rows[i][j]
        total += term
    return total


def table_count_supported(rows: list[list[int]]) -> int:
    """S2 as declared, with the arrangements that meet a zero entry pruned:
    those contribute `0` to the alternating sum, so this is the same count
    over the supported arrangements only.  Cross-checked against the
    unpruned enumeration by `table_count_literal` where that is affordable."""

    return sum(nonzero_terms(rows))


def table_count_elimination(rows: list[list[int]]) -> int:
    """S2 by fraction-free row elimination (exact integers; every division
    is exact).  METATHEORY: elimination computes the alternating sum."""

    n = len(rows)
    if n == 0:
        return 1
    a = [row[:] for row in rows]
    previous = 1
    sign = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // previous
        previous = a[k][k]
    return sign * a[n - 1][n - 1]


def table_count_column_route(
    windex: str, delta: int, cindex: str, n: int, bal: list[int]
) -> int:
    """S2 for a diagonal of magnitude one by reducing the first column by
    the other columns until rows ``2..N`` of it vanish; the table is then
    triangular and its alternating sum is the diagonal product.  Exact
    integers; ``O(N log N)`` over the multiples of each row."""

    if delta not in (1, -1):
        raise ValueError("the column route needs a diagonal of magnitude one")
    if n == 0:
        return 1
    if n == 1:
        return delta
    # x[i] for i in 2..n: delta * x[i] + sum_{j > i, i | j} w(i, j) * x[j] = f(i)
    x = [0] * (n + 1)
    for i in range(n, 1, -1):
        weights = weight_vector(windex, i, n, bal)
        acc: int = sum(map(mul, weights, x[2 * i :: i])) if weights else 0
        x[i] = (first_column(cindex, i, bal) - acc) * delta
    top: int = sum(map(mul, weight_vector(windex, 1, n, bal), x[2:]))
    head = delta - top
    block = delta if (n - 1) % 2 == 1 else 1
    return head * block


def nonzero_terms(rows: list[list[int]]) -> list[int]:
    """Every nonzero signed term of the alternating sum, found by walking
    the rows over the columns with a nonzero entry."""

    n = len(rows)
    allowed = [[j for j in range(n) if rows[i][j] != 0] for i in range(n)]
    column_rows = [[i for i in range(n) if rows[i][j] != 0] for j in range(n)]
    terms: list[int] = []
    used = [False] * n
    assigned = [-1] * n

    def rec(prod: int) -> None:
        # the unassigned row with the fewest free allowed columns; a row
        # with none, or a free column no unassigned row allows, ends the branch
        best = -1
        best_options: list[int] = []
        for i in range(n):
            if assigned[i] != -1:
                continue
            options = [j for j in allowed[i] if not used[j]]
            if not options:
                return
            if best == -1 or len(options) < len(best_options):
                best, best_options = i, options
                if len(options) == 1:
                    break
        if best == -1:
            terms.append(inversion_sign(tuple(assigned)) * prod)
            return
        for j in range(n):
            if not used[j] and all(assigned[i] != -1 for i in column_rows[j]):
                return
        for j in best_options:
            assigned[best] = j
            used[j] = True
            rec(prod * rows[best][j])
            assigned[best] = -1
            used[j] = False

    rec(1)
    return terms


# --------------------------------------------------------------------- S3


def sections_count(windex: str, n: int, bal: list[int]) -> int:
    """S3: the sum over sections -- one arrow into every object ``2..N`` --
    of the product of the chosen arrows' weights; enumerated, not
    factored."""

    choices = [[(d, m) for d in proper_divisors(m)] for m in range(2, n + 1)]
    total = 0
    for section in product(*choices):
        w = 1
        for d, m in section:
            w *= weight(windex, d, m, bal)
        total += w
    return total


# ---------------------------------------------------------------- search


def candidate_values(kind: str, spec: tuple[object, ...], bal: list[int]) -> list[int]:
    """The candidate's values at ``N = 1..MENU_BOUND``."""

    if kind == "S1":
        (windex,) = spec
        return walk_sums(str(windex), MENU_BOUND, bal)[1:]
    if kind == "S1b":
        (windex,) = spec
        return total_walk_sums(str(windex), MENU_BOUND, bal)[1:]
    if kind == "S2":
        windex, delta, cindex = spec
        out: list[int] = []
        for n in range(1, MENU_BOUND + 1):
            rows = table(str(windex), int(str(delta)), str(cindex), n, bal)
            literal = table_count_supported(rows)
            elimination = table_count_elimination(rows)
            if literal != elimination:
                raise AssertionError(
                    f"routes disagree at {menu_label(kind, spec)} N={n}:"
                    f" literal {literal}, elimination {elimination}"
                )
            out.append(literal)
        return out
    if kind == "S3":
        (windex,) = spec
        return [sections_count(str(windex), n, bal) for n in range(1, MENU_BOUND + 1)]
    raise ValueError(kind)


def menu() -> list[tuple[str, tuple[object, ...]]]:
    items: list[tuple[str, tuple[object, ...]]] = []
    for w in WEIGHTS:
        items.append(("S1", (w,)))
    for w in WEIGHTS:
        items.append(("S1b", (w,)))
    for w in WEIGHTS:
        for delta in DIAGONALS:
            for c in COLUMNS:
                items.append(("S2", (w, delta, c)))
    for w in WEIGHTS:
        items.append(("S3", (w,)))
    return items


def menu_label(kind: str, spec: tuple[object, ...]) -> str:
    return kind + "(" + ",".join(str(s) for s in spec) + ")"


def search(bal: list[int], run: list[int]) -> dict[str, object]:
    """Every candidate against the running balance at ``1..MENU_BOUND``."""

    target = run[1 : MENU_BOUND + 1]
    rows: list[dict[str, object]] = []
    hits: list[str] = []
    for kind, spec in menu():
        values = candidate_values(kind, spec, bal)
        agree = [n for n in range(1, MENU_BOUND + 1) if values[n - 1] == target[n - 1]]
        label = menu_label(kind, spec)
        hit = len(agree) == MENU_BOUND
        if hit:
            hits.append(label)
        rows.append(
            {
                "menu": label,
                "kind": kind,
                "values_1_12": values,
                "agreeing_N": agree,
                "meets_stage_2": hit,
            }
        )
    return {
        "bound": MENU_BOUND,
        "menu_size": len(rows),
        "target_running_balance_1_12": target,
        "candidates": rows,
        "hits": hits,
    }


# ------------------------------------------------------------- extension


def parse_s2(label: str) -> tuple[str, int, str]:
    inner = label[len("S2(") : -1]
    w, delta, c = inner.split(",")
    return w, int(delta), c


def parse_weight_only(label: str) -> str:
    return label[label.index("(") + 1 : -1]


def s1b_extension(windex: str, bal: list[int], run: list[int]) -> dict[str, object]:
    """S1b recomputed by its recursion at every ``N`` up to the table's
    bound, compared with the running balance; the chain enumeration
    cross-checks the recursion at small ``N``."""

    limit = len(run) - 1
    totals = total_walk_sums(windex, limit, bal)
    misses = [n for n in range(1, limit + 1) if totals[n] != run[n]]
    ws = walk_sums(windex, 200, bal)
    literal_misses = [m for m in range(1, 201) if walk_sum_literal(windex, m, bal) != ws[m]]
    return {
        "recursion_vs_running_balance_misses_to": limit,
        "recursion_vs_running_balance_misses": misses,
        "chain_enumeration_vs_recursion_bound": 200,
        "chain_enumeration_vs_recursion_misses": literal_misses,
        "checkpoints": {str(n): totals[n] for n in CHECKPOINTS if n <= limit},
    }


def s2_extension(label: str, bal: list[int], run: list[int]) -> dict[str, object]:
    """An S2 hit taken beyond the menu bound: routes compared where they
    overlap; the column route against the running balance to
    ``DIRECT_BOUND`` at every ``N`` and at the stepped and pinned
    checkpoints within the table's bound."""

    windex, delta, cindex = parse_s2(label)
    limit = len(run) - 1
    literal_vs_supported = [
        n
        for n in range(1, UNPRUNED_BOUND + 1)
        if table_count_literal(table(windex, delta, cindex, n, bal))
        != table_count_supported(table(windex, delta, cindex, n, bal))
    ]
    supported_vs_elim = [
        n
        for n in range(1, ELIMINATION_BOUND + 1)
        if table_count_supported(table(windex, delta, cindex, n, bal))
        != table_count_elimination(table(windex, delta, cindex, n, bal))
    ]
    out: dict[str, object] = {
        "unpruned_vs_supported_bound": UNPRUNED_BOUND,
        "unpruned_vs_supported_misses": literal_vs_supported,
        "supported_vs_elimination_bound": ELIMINATION_BOUND,
        "supported_vs_elimination_misses": supported_vs_elim,
    }
    if delta in (1, -1):
        elim_vs_column = [
            n
            for n in range(1, ELIMINATION_BOUND + 1)
            if table_count_elimination(table(windex, delta, cindex, n, bal))
            != table_count_column_route(windex, delta, cindex, n, bal)
        ]
        direct = [
            n
            for n in range(1, min(DIRECT_BOUND, limit) + 1)
            if table_count_column_route(windex, delta, cindex, n, bal) != run[n]
        ]
        checkpoint_values: dict[str, int] = {}
        checkpoint_misses: list[int] = []
        for n in sorted(set(STEPPED_CHECKPOINTS) | set(CHECKPOINTS)):
            if n > limit:
                continue
            value = table_count_column_route(windex, delta, cindex, n, bal)
            checkpoint_values[str(n)] = value
            if value != run[n]:
                checkpoint_misses.append(n)
        out.update(
            {
                "elimination_vs_column_bound": ELIMINATION_BOUND,
                "elimination_vs_column_misses": elim_vs_column,
                "column_vs_running_balance_every_N_to": min(DIRECT_BOUND, limit),
                "column_vs_running_balance_misses": direct,
                "column_route_checkpoints": checkpoint_values,
                "column_route_checkpoint_misses": checkpoint_misses,
            }
        )
    else:
        out["extension"] = "diagonal of magnitude zero: no column route; elimination only"
        direct0 = [
            n
            for n in range(1, ELIMINATION_BOUND + 1)
            if table_count_elimination(table(windex, delta, cindex, n, bal)) != run[n]
        ]
        out["elimination_vs_running_balance_to"] = ELIMINATION_BOUND
        out["elimination_vs_running_balance_misses"] = direct0
    return out


def report(bal: list[int], run: list[int]) -> dict[str, object]:
    """Stage 2 on a balance table and its running balance up to the
    extension bound (the caller computes both once)."""

    limit = len(run) - 1
    found = search(bal, run)
    hits = found["hits"]
    assert isinstance(hits, list)
    extensions: dict[str, object] = {}
    for label in hits:
        if label.startswith("S2("):
            extensions[label] = s2_extension(label, bal, run)
        elif label.startswith("S1b("):
            extensions[label] = s1b_extension(parse_weight_only(label), bal, run)
    return {
        "search": found,
        "extension_bound": limit,
        "extensions": extensions,
        "pinned_checkpoints_direct": {str(n): run[n] for n in CHECKPOINTS if n <= limit},
    }
