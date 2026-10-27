"""Finite executable model of the two theorems. AuthorityEffect: None.

Everything here is a check on small represented carriers.  It proves nothing
beyond the instances it enumerates; the Lean library under ``lean/`` carries
the proofs, and ``CLAIMS.md`` says which statement rests on which.  The model
exists so that every Lean statement has an independent executable reading,
so that the Lean instances of the capacity threshold are produced and checked
by a construction the Lean file does not know about, and so that the theorems
can be attacked exhaustively on tiny carriers where a counterexample would be
cheap to find.

Vocabulary follows ``README.md``: a view is a finite set of naturals, an
observer (evaluator) a tuple of views, an actor a presentation ``Nat -> Nat``
read on a carrier ``D``, an institution a tuple of presentations.
"""
from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from itertools import combinations, product
import json
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent

View = tuple[int, ...]
Evaluator = tuple[View, ...]
Carrier = tuple[int, ...]
Presentation = Callable[[int], int]


# ---------------------------------------------------------------- pins


def consumed_modules() -> list[str]:
    """The sealed modules this tree consumes, as pinned in ``input.json``."""
    data = json.loads((HERE / "input.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("source_revision"), str):
        raise ValueError("input.json must name a source_revision")
    modules = data.get("consumed_modules")
    if (not isinstance(modules, list) or not modules
            or any(not isinstance(m, str) or not m.startswith("Derivation.") for m in modules)
            or modules != sorted(set(modules))):
        raise ValueError("input.json: consumed_modules must be a sorted unique list of Derivation modules")
    return modules


def lean_imports() -> list[str]:
    """Every ``Derivation.*`` import of every module of the tree's library."""
    found: set[str] = set()
    for path in sorted((HERE / "lean" / "ResearchTwoTheorems").glob("*.lean")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("import Derivation."):
                found.add(line.split()[1])
    return sorted(found)


# ---------------------------------------------------------------- Theorem I


class Table:
    """A presentation given by a finite table; ``0`` off the table.

    A class rather than a closure so that enumerated presentations do not
    share late-bound variables and so that they print deterministically.
    """

    def __init__(self, values: dict[int, int]) -> None:
        self.values = dict(values)

    def __call__(self, x: int) -> int:
        return self.values.get(x, 0)

    def __repr__(self) -> str:
        return "Table(" + ", ".join(f"{k}:{v}" for k, v in sorted(self.values.items())) + ")"


def sep(c: View, i: int, j: int) -> bool:
    """Genesis ``sepB``: the view holds exactly one of the two points."""
    return (i in c) != (j in c)


def verdict(E: Evaluator, i: int, j: int) -> bool:
    """Genesis ``verdictB``: some view of the observer separates the pair."""
    return any(sep(c, i, j) for c in E)


def sig(Q: Sequence[Presentation], x: int) -> tuple[int, ...]:
    """Genesis ``sigList``: the answers of ``x`` to the family, in order."""
    return tuple(q(x) for q in Q)


def class_count(D: Carrier, Q: Sequence[Presentation]) -> int:
    """Genesis ``classCount``: distinct signatures on the carrier."""
    return len({sig(Q, x) for x in D})


def fibers(D: Carrier, p: Presentation) -> int:
    return class_count(D, [p])


def view_question(c: View) -> Presentation:
    """A view read as a two-valued question (``viewQ``)."""
    return Table({x: 1 for x in c})


def questions(E: Evaluator) -> list[Presentation]:
    return [view_question(c) for c in E]


def sharp(D: Carrier, E: Evaluator, p: Presentation) -> bool:
    """``Sharp D E p``: the verdict kernel is exactly the fiber partition."""
    return all((not verdict(E, x, y)) == (p(x) == p(y)) for x in D for y in D)


def fiber_identity(D: Carrier, p: Presentation, q: Presentation) -> bool:
    """Genesis ``FiberIdentityOn``."""
    return all((p(x) == p(y)) == (q(x) == q(y)) for x in D for y in D)


def joint_presentation(D: Carrier, Q: Sequence[Presentation]) -> Table:
    """A presentation with the kernel of Genesis ``pQ D Q`` on ``D``: the
    index of the signature in first-occurrence order.  (``pQ`` itself picks
    the first carrier point of the class; the kernel is the same.)"""
    order: dict[tuple[int, ...], int] = {}
    for x in D:
        order.setdefault(sig(Q, x), len(order))
    return Table({x: order[sig(Q, x)] for x in D})


def all_views(D: Carrier) -> list[View]:
    """Every subset of the carrier, as a sorted tuple."""
    out: list[View] = []
    for r in range(len(D) + 1):
        out.extend(tuple(sorted(c)) for c in combinations(D, r))
    return out


def all_evaluators(D: Carrier, m: int) -> Iterator[Evaluator]:
    yield from product(all_views(D), repeat=m)


def all_presentations(D: Carrier) -> Iterator[Table]:
    """Every presentation of the carrier into ``range(len(D))`` (every
    fiber partition occurs among them)."""
    for values in product(range(len(D)), repeat=len(D)):
        yield Table(dict(zip(D, values)))


def exists_sharp_observer(D: Carrier, p: Presentation, m: int) -> bool:
    return any(sharp(D, E, p) for E in all_evaluators(D, m))


def bit_observer(D: Carrier, idx: Presentation, m: int) -> Evaluator:
    """``bitObserver``: the ``m`` low bits of an index, as views."""
    return tuple(tuple(x for x in D if (idx(x) >> b) & 1) for b in range(m))


def fiber_index(D: Carrier, p: Presentation) -> Table:
    return joint_presentation(D, [p])


def resolution_check(D: Carrier, m: int) -> dict[str, int]:
    """Theorem I(c), exhaustively: an actor on ``D`` has a sharp ``m``-view
    observer exactly when it has at most ``2 ** m`` fibers; and the bit
    observer of the fiber index is such an observer when one exists."""
    agree = disagree = attained = 0
    for p in all_presentations(D):
        has = exists_sharp_observer(D, p, m)
        bound = fibers(D, p) <= 2 ** m
        if has == bound:
            agree += 1
        else:
            disagree += 1
        if bound:
            if sharp(D, bit_observer(D, fiber_index(D, p), m), p):
                attained += 1
    return {"presentations": agree + disagree, "agree": agree, "disagree": disagree,
            "bit_observer_sharp": attained}


def verdict_ceiling_check(D: Carrier, m: int) -> bool:
    """Theorem I(b): any Boolean of two signatures is constant on the verdict
    kernel.  Checked for every observer and every point pair on ``D`` by
    comparing signatures directly (the function cannot tell them apart)."""
    for E in all_evaluators(D, m):
        Q = questions(E)
        for x in D:
            for y in D:
                if not verdict(E, x, y) and sig(Q, x) != sig(Q, y):
                    return False
    return True


def separation_fact_not_law() -> dict[str, bool]:
    """The observer-calculus facts: ``sepB c i i`` is always false, and one
    view separating ``0`` from ``1`` says nothing about ``0`` and ``2``."""
    c: View = (0, 2)
    return {"irreflexive_on_examples": all(not sep(v, i, i) for v in all_views((0, 1, 2, 3)) for i in range(5)),
            "separates_0_1": sep(c, 0, 1), "merges_0_2": not sep(c, 0, 2)}


# ---------------------------------------------------------------- Theorem I(d)


def nat_sub(a: int, b: int) -> int:
    return a - b if a >= b else 0


def ball(i: int, d: int) -> list[int]:
    """Genesis ``SeparationCapacity.ball`` with truncated subtraction."""
    return [nat_sub(i, d) + t for t in range(2 * d + 1)]


def encode(k: int, word: Sequence[int]) -> int:
    """Genesis ``CapacityBound.encode``: little-endian ``k``-ary numeral."""
    value = 0
    for x in reversed(word):
        value = x + k * value
    return value


def window_distinct_cycle(k: int, d: int) -> list[int]:
    """A cyclic word over ``k`` letters in which every word of length
    ``2d+1`` occurs exactly once: a closed walk using every edge once in the
    graph whose vertices are words of length ``2d`` and whose edges are words
    of length ``2d+1``.  Deterministic (lexicographic edge choice)."""
    w = 2 * d + 1
    if k == 1:
        return [0]
    if d == 0:
        return list(range(k))
    m = w - 1
    next_letter: dict[tuple[int, ...], int] = {v: 0 for v in product(range(k), repeat=m)}
    start = tuple([0] * m)
    stack: list[tuple[int, ...]] = [start]
    letters: list[int] = []
    while stack:
        v = stack[-1]
        if next_letter[v] < k:
            a = next_letter[v]
            next_letter[v] += 1
            stack.append(v[1:] + (a,))
        else:
            stack.pop()
            if stack:
                letters.append(v[-1])
    seq = letters[::-1]
    if len(seq) != k ** w:
        raise ValueError(f"walk did not use every word: {len(seq)} of {k ** w}")
    return seq


def colouring_list(k: int, d: int) -> list[int]:
    """The list of length ``n = k^(2d+1) + 2d + 1`` whose positions
    ``1 .. n-1`` carry the linearised cycle; position ``0`` is never read by
    an interior window."""
    cyc = window_distinct_cycle(k, d)
    return [0] + [cyc[i % len(cyc)] for i in range(len(cyc) + 2 * d)]


def power(k: int, e: int) -> int:
    """``k ** e`` for natural ``e``, typed as an integer."""
    value = 1
    for _ in range(e):
        value *= k
    return value


def threshold(k: int, d: int) -> int:
    """Genesis's forcing size ``k^(2d+1) + 2d + 2``."""
    return power(k, 2 * d + 1) + 2 * d + 2


def interior(d: int, n: int) -> list[int]:
    return [i for i in range(n) if d < i and i + d < n]


def code_view(k: int, colour: Presentation, d: int) -> Presentation:
    """``codeView``: the local view reading its window as a numeral."""
    return lambda i: encode(k, [colour(j) for j in ball(i, d)])


def injective_on_interior(v: Presentation, d: int, n: int) -> bool:
    seen: dict[int, int] = {}
    for i in interior(d, n):
        if v(i) in seen:
            return False
        seen[v(i)] = i
    return True


def tight(k: int, d: int) -> bool:
    """``TightAt k d`` from the constructed list: one below the threshold,
    the code view of the window-distinct colouring has no interior
    collision."""
    n = threshold(k, d) - 1
    lst = colouring_list(k, d)
    if len(lst) != n or any(not 0 <= c < k for c in lst):
        return False
    colour = Table(dict(enumerate(lst)))
    return injective_on_interior(code_view(k, colour, d), d, n)


def forced_collision_exhaustive(k: int, d: int) -> bool:
    """At the threshold every ``k``-colouring's code view collides on the
    interior (hence every ``d``-local view does, since each factors through
    the window).  Exhaustive over all ``k ** n`` colourings; only for tiny
    parameters."""
    n = threshold(k, d)
    for values in product(range(k), repeat=n):
        colour = Table(dict(enumerate(values)))
        if injective_on_interior(code_view(k, colour, d), d, n):
            return False
    return True


# ---------------------------------------------------------------- Theorem II


def knows(D: Carrier, Q: Sequence[Presentation], q: Presentation) -> bool:
    """``Knows D Q q``: the question is constant on every signature class."""
    return all(sig(Q, x) != sig(Q, y) or q(x) == q(y) for x in D for y in D)


def witness_of_ignorance(D: Carrier, Q: Sequence[Presentation], q: Presentation) -> tuple[int, int] | None:
    for x in D:
        for y in D:
            if sig(Q, x) == sig(Q, y) and q(x) != q(y):
                return (x, y)
    return None


def information(D: Carrier, Q: Sequence[Presentation]) -> int:
    return class_count(D, Q)


def pooled(panel: Sequence[Evaluator]) -> Evaluator:
    return tuple(c for E in panel for c in E)


def cert_pos(panel: Sequence[Evaluator], i: int, j: int) -> bool:
    """Genesis ``certPosB``: a non-empty panel, every member separates."""
    return bool(panel) and all(verdict(E, i, j) for E in panel)


def cert_neg(panel: Sequence[Evaluator], i: int, j: int) -> bool:
    """Genesis ``certNegB``: a non-empty panel, no member separates."""
    return bool(panel) and all(not verdict(E, i, j) for E in panel)


def knowledge_checks(D: Carrier, pool: Sequence[Presentation], size: int) -> dict[str, int]:
    """Theorem II on every family of at most ``size`` members drawn from the
    pool and every question of the pool:

    * knowledge is information stationarity, ignorance a strict increase;
    * know-or-witness: a witness exists exactly when not known;
    * a known question adjoined changes nothing known; the actor is known;
    * the institution read as one actor has the institution's information;
    * every computation on known answers is known (checked on a sum);
    * a member is fiber-identical to the actor exactly when it alone knows
      every member.
    """
    families = 0
    failures: dict[str, int] = {"stationarity": 0, "witness": 0, "known_extension": 0,
                                "actor": 0, "closure": 0, "member_sharp": 0}
    for r in range(size + 1):
        for Q in combinations(pool, r):
            families += 1
            pq = joint_presentation(D, Q)
            if class_count(D, [pq]) != information(D, Q) or not knows(D, Q, pq):
                failures["actor"] += 1
            for q in pool:
                k = knows(D, Q, q)
                stationary = information(D, (*Q, q)) == information(D, Q)
                strict = information(D, Q) < information(D, (*Q, q))
                if k != stationary or (not k) != strict:
                    failures["stationarity"] += 1
                if (witness_of_ignorance(D, Q, q) is None) != k:
                    failures["witness"] += 1
                if k:
                    for q2 in pool:
                        if knows(D, (*Q, q), q2) != knows(D, Q, q2):
                            failures["known_extension"] += 1
                    for q2 in pool:
                        if knows(D, Q, q2):
                            both = Table({x: q(x) + 3 * q2(x) for x in D})
                            if not knows(D, Q, both):
                                failures["closure"] += 1
            for q in Q:
                if fiber_identity(D, q, pq) != all(knows(D, [q], q2) for q2 in Q):
                    failures["member_sharp"] += 1
    return {"families": families, **failures}


def institution_exceeds_members(D: Carrier) -> dict[str, int | bool]:
    parity = Table({x: x % 2 for x in D})
    half = Table({x: x // 2 for x in D})
    return {"information_joint": information(D, [parity, half]),
            "information_parity": information(D, [parity]),
            "information_half": information(D, [half]),
            "parity_knows_half": knows(D, [parity], half),
            "half_knows_parity": knows(D, [half], parity),
            "joint_knows_identity": knows(D, [parity, half], Table({x: x for x in D}))}


def mutual_knowledge_check(D: Carrier, m: int, pool: Sequence[Presentation], size: int) -> int:
    """Sharpness of an observer for an institution's actor equals mutual
    knowledge.  Returns the number of disagreements (expected 0)."""
    bad = 0
    for r in range(size + 1):
        for Q in combinations(pool, r):
            pq = joint_presentation(D, Q)
            for E in all_evaluators(D, m):
                mutual = (all(knows(D, questions(E), q) for q in Q)
                          and all(knows(D, Q, view_question(c)) for c in E))
                if sharp(D, E, pq) != mutual:
                    bad += 1
    return bad


def panel_checks(D: Carrier, m: int, members: int) -> dict[str, int]:
    """Pooled against unanimous, over every panel of ``members`` observers of
    ``m`` views each: pooled non-separation is the negative certificate;
    unanimous separation implies pooled separation; and pooled separation
    without unanimity occurs."""
    evaluators = list(all_evaluators(D, m))
    neg_mismatch = pos_violation = pooled_not_unanimous = panels = 0
    for panel in product(evaluators, repeat=members):
        panels += 1
        P = pooled(panel)
        for i in D:
            for j in D:
                if (not verdict(P, i, j)) != cert_neg(panel, i, j):
                    neg_mismatch += 1
                if cert_pos(panel, i, j) and not verdict(P, i, j):
                    pos_violation += 1
                if verdict(P, i, j) and not cert_pos(panel, i, j):
                    pooled_not_unanimous += 1
    return {"panels": panels, "neg_mismatch": neg_mismatch, "pos_violation": pos_violation,
            "pooled_not_unanimous": pooled_not_unanimous}


def information_le_resolution_check(D: Carrier, m: int) -> bool:
    return all(information(D, questions(E)) <= 2 ** m for E in all_evaluators(D, m))


# ---------------------------------------------------------------- Diagonal


def mod_code(n: int) -> Presentation:
    return lambda x: x % (n + 1)


def catalogue(code: Callable[[int], Presentation], n: int) -> list[Presentation]:
    return [code(i) for i in range(n)]


def diag(code: Callable[[int], Presentation]) -> Presentation:
    return lambda x: code(x)(x) + 1


def diagonal_checks(D: Carrier, upto: int) -> dict[str, list[int] | bool]:
    """The diagonal of the ``mod`` catalogue is never a member (it differs
    from member ``n`` at ``n``), and the institutions that know it on ``D``
    are listed by size."""
    code = mod_code
    dg = diag(code)
    never_member = all(code(n)(n) != dg(n) for n in range(upto))
    known = [n for n in range(upto + 1) if knows(D, catalogue(code, n), dg)]
    unknown = [n for n in range(upto + 1) if not knows(D, catalogue(code, n), dg)]
    return {"never_member": never_member, "known_by": known, "unknown_by": unknown}


def self_evaluator_check(size: int) -> bool:
    """Every evaluator ``ev`` on a code set of ``size`` elements misses the
    flipped diagonal row.  Exhaustive over all ``2 ** (size * size)``
    evaluators."""
    codes = range(size)
    for bits in product((False, True), repeat=size * size):
        ev = {(c, x): bits[c * size + x] for c in codes for x in codes}
        flipped = {x: not ev[(x, x)] for x in codes}
        if any(all(ev[(c, x)] == flipped[x] for x in codes) for c in codes):
            return False
    return True


# ---------------------------------------------------------------- Correspondences


def faithful(D: Carrier, f: Presentation) -> bool:
    """``Faithful D f``: the correspondence merges no two carrier points."""
    return all(f(x) != f(y) or x == y for x in D for y in D)


def pullback(D: Carrier, f: Presentation, E: Evaluator) -> Evaluator:
    """``pullback``: the observer's views read back along ``f`` onto ``D``."""
    return tuple(tuple(x for x in D if f(x) in c) for c in E)


def fiber_constant(D: Carrier, f: Presentation, q: Presentation) -> bool:
    """Genesis ``FiberConstant D f q``: ``f`` merges only within ``q``'s fibers."""
    return all(f(x) != f(y) or q(x) == q(y) for x in D for y in D)


def correspondence_checks(D: Carrier, pool: Sequence[Presentation], size: int) -> dict[str, int | bool]:
    """The correspondence module on a small carrier:

    * the constant map is not faithful and collapses every pair under every
      observer; the empty institution's actor is constant on the carrier;
    * the institution's actor is faithful exactly when the institution knows
      the identity (every family of at most ``size`` pool members);
    * sharpness transports along every map (``sharp_pullback_iff``), and a
      sharp observation through ``f`` forces ``f`` to merge only within the
      observed actor's fibers (``fiberConstant_of_sharp_pullback``), over
      every map of ``D`` into ``range(len(D))``, every observer of at most
      two views on ``range(len(D))`` and every actor.
    """
    const = Table({})
    out: dict[str, int | bool] = {
        "constant_faithful": faithful(D, const) if len(D) >= 2 else True,
        "constant_collapses_all": all(not verdict(E, const(x), const(y))
                                      for E in all_evaluators(D, 1) for x in D for y in D),
        "empty_actor_constant": len({joint_presentation(D, ())(x) for x in D}) <= 1,
    }
    actor_mismatch = 0
    for r in range(size + 1):
        for Q in combinations(pool, r):
            if faithful(D, joint_presentation(D, Q)) != knows(D, Q, Table({x: x for x in D})):
                actor_mismatch += 1
    out["faithful_actor_mismatch"] = actor_mismatch
    transport_mismatch = fiber_violation = 0
    letters: Carrier = tuple(range(len(D)))
    observers = list(all_evaluators(letters, 1)) + list(all_evaluators(letters, 2))
    for values in product(letters, repeat=len(D)):
        f = Table(dict(zip(D, values)))
        image: Carrier = tuple(f(x) for x in D)
        for E in observers:
            pb = pullback(D, f, E)
            for p in all_presentations(letters):
                composed = Table({x: p(f(x)) for x in D})
                if sharp(image, E, p) != sharp(D, pb, composed):
                    transport_mismatch += 1
            for q in all_presentations(D):
                if sharp(D, pb, q) and not fiber_constant(D, f, q):
                    fiber_violation += 1
    out["sharp_pullback_mismatch"] = transport_mismatch
    out["fiber_constant_violation"] = fiber_violation
    return out


# ---------------------------------------------------------------- Regimes


class Regime(NamedTuple):
    """Genesis's regime: a datum count, form arities, instances, rules."""

    data: int
    forms: tuple[int, ...]
    insts: tuple[tuple[int, tuple[int, ...]], ...]
    rules: tuple[int, ...]


Ctx = tuple[int, tuple[int | None, ...]]
Inst = tuple[int, tuple[int, ...]]


def plug(c: Ctx, d: int) -> Inst:
    form, slots = c
    return (form, tuple(d if s is None else s for s in slots))


def derivable(r: Regime, inst: Inst) -> bool:
    """Genesis ``derivable``: an admitted instance, or a form under the rule."""
    return inst in r.insts or inst[0] in r.rules


def wf_ctx(r: Regime, c: Ctx) -> bool:
    """Genesis ``wfCtx``: admitted form, matching arity, a hole, admitted data."""
    form, slots = c
    return (form < len(r.forms) and len(slots) == r.forms[form] and None in slots
            and all(s is None or s < r.data for s in slots))


def all_ctxs(r: Regime) -> list[Ctx]:
    """Every well-formed context of a small regime, in a fixed order."""
    out: list[Ctx] = []
    for form, arity in enumerate(r.forms):
        for slots in product((None, *range(r.data)), repeat=arity):
            c: Ctx = (form, slots)
            if wf_ctx(r, c):
                out.append(c)
    return out


def admitted(r: Regime) -> Carrier:
    return tuple(range(r.data))


def ctx_view(r: Regime, c: Ctx) -> View:
    """``ctxView``: the admitted data whose plugging is derivable."""
    return tuple(d for d in admitted(r) if derivable(r, plug(c, d)))


def regime_views(r: Regime) -> Evaluator:
    return tuple(ctx_view(r, c) for c in all_ctxs(r))


def separable(r: Regime, a: int, b: int) -> bool:
    """Genesis ``separable``: some well-formed context tells the data apart."""
    return any(derivable(r, plug(c, a)) != derivable(r, plug(c, b)) for c in all_ctxs(r))


R0 = Regime(2, (1,), ((0, (0,)),), ())
R0_RULE = Regime(2, (1,), ((0, (0,)),), (0,))
R0_BOTH = Regime(2, (1,), ((0, (0,)), (0, (1,))), ())
R_BINARY = Regime(3, (1, 2), ((0, (0,)), (1, (0, 1)), (1, (2, 1))), ())
R_RULE_ONLY = Regime(3, (1, 2), (), (1,))


def bridge_checks(regimes: Sequence[Regime]) -> dict[str, int | bool | list[int]]:
    """The regime bridge on small regimes: on admitted data the regime's
    observer separates exactly when Genesis declares ``separable``; the
    regime's information is bounded by ``2 ** contexts`` and by the datum
    count; an unadmitted datum lies in no view."""
    pairs = mismatch = bound_violation = 0
    informations: list[int] = []
    for r in regimes:
        E = regime_views(r)
        D = admitted(r)
        for a in D:
            for b in D:
                pairs += 1
                if verdict(E, a, b) != separable(r, a, b):
                    mismatch += 1
        info = information(D, questions(E))
        informations.append(info)
        if info > min(2 ** len(E), r.data):
            bound_violation += 1
    return {"pairs": pairs, "mismatch": mismatch, "bound_violation": bound_violation,
            "informations": informations,
            "unadmitted_in_no_view": all(99 not in v for r in regimes for v in regime_views(r)),
            "unadmitted_separated_from_0": verdict(regime_views(R0), 0, 99)}


def recollapse_witness() -> dict[str, object]:
    """One rule admission alters the view ``[0]`` into ``[0, 1]``: the pair
    ``0, 1`` goes from separated to collapsed, and a view of ``R0`` is not a
    view of ``R0rule``.  Views are altered, not added."""
    before, after = regime_views(R0), regime_views(R0_RULE)
    return {"views_before": [list(v) for v in before], "views_after": [list(v) for v in after],
            "separable_before": separable(R0, 0, 1), "separable_after": separable(R0_RULE, 0, 1),
            "lost_views": [list(v) for v in before if v not in after]}


def verdict_mono_check(D: Carrier, m: int) -> bool:
    """More views never fewer separations: adding any view to any observer of
    ``m`` views keeps every separation."""
    return all(not verdict(E, x, y) or verdict((*E, c), x, y)
               for E in all_evaluators(D, m) for c in all_views(D) for x in D for y in D)


# ---------------------------------------------------------------- summary


def run_all() -> dict[str, object]:
    D4: Carrier = (0, 1, 2, 3)
    D3: Carrier = (0, 1, 2)
    pool = [Table({x: x % 2 for x in D4}), Table({x: x // 2 for x in D4}),
            Table({x: (x == 1) * 1 for x in D4}), Table({x: 0 for x in D4})]
    return {
        "pins": {"consumed_modules": consumed_modules()},
        "theorem_I": {
            "resolution_D3_m1": resolution_check(D3, 1),
            "resolution_D4_m1": resolution_check(D4, 1),
            "resolution_D4_m2": resolution_check(D4, 2),
            "verdict_ceiling_D4_m2": verdict_ceiling_check(D4, 2),
            "fact_not_law": separation_fact_not_law(),
            "information_le_resolution_D4_m2": information_le_resolution_check(D4, 2),
        },
        "theorem_I_capacity": {
            "window_distinct": {f"{k},{d}": tight(k, d) for k in (1, 2, 3, 4) for d in (0, 1, 2) if k ** (2 * d + 1) <= 1100},
            "forced_at_threshold": {"2,0": forced_collision_exhaustive(2, 0),
                                    "3,0": forced_collision_exhaustive(3, 0),
                                    "2,1": forced_collision_exhaustive(2, 1)},
            "lean_lists": {f"{k},{d}": colouring_list(k, d) for k, d in ((1, 0), (2, 0), (3, 0), (2, 1), (3, 1), (2, 2))},
        },
        "theorem_II": {
            "knowledge_D4": knowledge_checks(D4, pool, 2),
            "exceeds": institution_exceeds_members(D4),
            "mutual_knowledge_disagreements_D3": mutual_knowledge_check(D3, 1, pool[:3], 2),
            "panels_D3": panel_checks(D3, 1, 2),
        },
        "diagonal": {
            "mod_catalogue_D4": diagonal_checks(D4, 5),
            "self_evaluator_2": self_evaluator_check(2),
            "self_evaluator_3": self_evaluator_check(3),
        },
        "correspondence": correspondence_checks(D3, pool[:3], 2),
        "regime_bridge": {
            "bridge": bridge_checks([R0, R0_RULE, R0_BOTH, R_BINARY, R_RULE_ONLY]),
            "recollapse": recollapse_witness(),
            "verdict_mono_D3_m1": verdict_mono_check(D3, 1),
        },
    }


def main() -> None:
    print(json.dumps(run_all(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
