"""Finite mirrors of the institution_forces tree.  AuthorityEffect: None.

Everything here is computed exhaustively over declared bounds and is evidence
for the VERIFIED_FINITE rows of CLAIMS.md only.  The Lean modules are the
authority for the PROVED_THEOREM rows; no test here is cited for one of
those.

The bound: the carrier is `range(4)` (and, for carrier extension, each of its
subsets); a seat is a Boolean table on it (16 tables); an institution is an
ordered tuple of at most three seats, repetition allowed, because the
redundancy count is a count of seats (4369 institutions); a question is a
Boolean table (16).  Ballot maps send a seat's two values to {0, 1, 2}
(NAY, AYE, ABSTAIN): nine per seat.  Replacement seats in the L1 check range
over the 16 Boolean tables, which include the constants the Lean proof uses.
Every count is an exact integer.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
from typing import Iterator

HERE = Path(__file__).resolve().parent

N = 4
POINTS: tuple[int, ...] = tuple(range(N))
Table = tuple[int, ...]
Family = tuple[Table, ...]
BOOL_TABLES: tuple[Table, ...] = tuple(product((0, 1), repeat=N))
MAX_SEATS = 3

# --------------------------------------------------------------------------
# Pins: the modules this tree consumes, and the reach of its axiom report.


def _input() -> dict[str, object]:
    data = json.loads((HERE / "input.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("source_revision"), str):
        raise ValueError("input.json must name a source_revision")
    return data


def consumed_modules() -> list[str]:
    modules = _input().get("consumed_modules")
    if (not isinstance(modules, list) or not modules
            or any(not isinstance(m, str) or not m.startswith("Derivation.") for m in modules)
            or modules != sorted(set(modules))):
        raise ValueError("input.json: consumed_modules must be a sorted unique list of Derivation modules")
    return modules


def consumed_research_modules() -> dict[str, str]:
    modules = _input().get("consumed_research_modules")
    if (not isinstance(modules, dict) or not modules
            or any(not isinstance(k, str) or not isinstance(v, str) or not v.startswith("research/")
                   or v.startswith(f"research/{HERE.name}/") for k, v in modules.items())):
        raise ValueError("input.json: consumed_research_modules must map modules to files of other research trees")
    return modules


def lean_imports() -> list[str]:
    """Every outside import of every module of this tree's Lean package."""
    lean = HERE / "lean"
    own = {p.relative_to(lean).with_suffix("").as_posix().replace("/", ".")
           for p in lean.rglob("*.lean") if ".lake" not in p.parts}
    found: set[str] = set()
    for path in lean.rglob("*.lean"):
        if ".lake" in path.parts:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("import "):
                found.add(line.split()[1])
    return sorted(found - own)


MODULES = ("Joint", "Robust", "Staleness", "Ballot")
ROOT = "ResearchInstitutionForces"


def theorem_names() -> list[str]:
    """Every `theorem` of the four modules, fully qualified, in file order."""
    names: list[str] = []
    for module in MODULES:
        stack: list[str] = []
        text = (HERE / "lean" / ROOT / f"{module}.lean").read_text(encoding="utf-8")
        for line in text.splitlines():
            opened = re.match(r"^namespace (\S+)", line)
            if opened:
                stack.append(opened.group(1))
                continue
            closed = re.match(r"^end (\S+)", line)
            if closed and stack and stack[-1] == closed.group(1):
                stack.pop()
                continue
            theorem = re.match(r"^theorem (\S+)", line)
            if theorem:
                names.append(".".join(stack + [theorem.group(1)]))
    return names


def axiom_report_names() -> list[str]:
    text = (HERE / "lean" / ROOT / "AxiomReport.lean").read_text(encoding="utf-8")
    return [line.split()[2] for line in text.splitlines() if line.startswith("#print axioms ")]


def contract_declarations() -> list[str]:
    data = json.loads((HERE / "TREE_CONTRACT.json").read_text(encoding="utf-8"))
    decls = data.get("axiom_declarations")
    if not isinstance(decls, list) or any(not isinstance(d, str) for d in decls):
        raise ValueError("TREE_CONTRACT.json: axiom_declarations must be a list of names")
    return [str(d) for d in decls]


# --------------------------------------------------------------------------
# The vocabulary, read directly from its definitions.


def sig(Q: Family, x: int) -> tuple[int, ...]:
    return tuple(m[x] for m in Q)


def knows(D: tuple[int, ...], Q: Family, q: Table) -> bool:
    """`Knows D Q q` read by `knows_iff_determined`: equal signatures on `D`
    force equal answers."""
    return all(sig(Q, x) != sig(Q, y) or q[x] == q[y] for x in D for y in D)


def joint(D: tuple[int, ...], Q: Family) -> Table:
    """`pQ D Q` on `range(4)`: the first point of `D` with the same signature,
    and `0` off `D`."""
    return tuple(next((z for z in D if sig(Q, z) == sig(Q, x)), 0) for x in POINTS)


def redundancy(Q: Family, x: int, y: int) -> int:
    return sum(1 for m in Q if m[x] != m[y])


def families(max_seats: int = MAX_SEATS) -> Iterator[Family]:
    for size in range(max_seats + 1):
        yield from product(BOOL_TABLES, repeat=size)


def carriers() -> list[tuple[int, ...]]:
    return [c for size in range(N + 1) for c in combinations(POINTS, size)]


# --------------------------------------------------------------------------
# A fast form of the same relation: bit p = 4*x + y of `same(t)` is set when
# `t` merges `x` and `y`; a family merges what every seat merges.  The fast
# form is checked against `knows` on every case it is used for
# (`fast_form_check`).

FULL = (1 << (N * N)) - 1


def same(t: Table) -> int:
    return sum(1 << (N * x + y) for x in POINTS for y in POINTS if t[x] == t[y])


def same_family(Q: Family) -> int:
    mask = FULL
    for m in Q:
        mask &= same(m)
    return mask


def carrier_mask(D: tuple[int, ...]) -> int:
    return sum(1 << (N * x + y) for x in D for y in D)


def knows_fast(D: tuple[int, ...], Q: Family, q: Table) -> bool:
    return same_family(Q) & carrier_mask(D) & ~same(q) == 0


@lru_cache(maxsize=None)
def known_mask(merged: int, carrier: int = FULL) -> int:
    """Bit `i` set when the family whose merged pairs are `merged` knows the
    `i`-th Boolean question on the carrier."""
    return sum(1 << i for i, q in enumerate(BOOL_TABLES) if merged & carrier & ~same(q) == 0)


TABLE_INDEX: dict[Table, int] = {t: i for i, t in enumerate(BOOL_TABLES)}
ALL_QUESTIONS = (1 << len(BOOL_TABLES)) - 1


@lru_cache(maxsize=None)
def replaced_mask(size: int, S: tuple[int, ...], kept: Family) -> int:
    """The questions known by every family of `size` seats that has the
    tables `kept`, in order, outside the positions `S` and any Boolean
    tables at `S`.  It depends on nothing else, hence the cache."""
    mask = ALL_QUESTIONS
    for values in product(BOOL_TABLES, repeat=len(S)):
        seats: list[Table] = []
        rest = iter(kept)
        chosen = iter(values)
        for position in range(size):
            seats.append(next(chosen) if position in S else next(rest))
        mask &= known_mask(same_family(tuple(seats)))
    return mask


def fast_form_check() -> dict[str, int]:
    checked = violations = 0
    for D in carriers():
        for Q in families(2):
            for q in BOOL_TABLES:
                checked += 1
                if knows(D, Q, q) != knows_fast(D, Q, q):
                    violations += 1
    for Q in product(BOOL_TABLES, repeat=3):
        for q in BOOL_TABLES:
            checked += 1
            if knows(POINTS, Q, q) != knows_fast(POINTS, Q, q):
                violations += 1
    return {"checked": checked, "violations": violations}


# --------------------------------------------------------------------------
# L0


def l0_check() -> dict[str, int]:
    """`Knows D F q` iff `Knows D [pQ D F] q`, on every carrier."""
    checked = violations = 0
    for D in carriers():
        for F in families():
            p = joint(D, F)
            carrier = carrier_mask(D)
            checked += len(BOOL_TABLES)
            if known_mask(same_family(F), carrier) != known_mask(same(p), carrier):
                violations += 1
    return {"checked": checked, "violations": violations}


# --------------------------------------------------------------------------
# L1


def robust_condition(Q: Family, q: Table, k: int) -> bool:
    return all(redundancy(Q, x, y) >= k + 1 for x in POINTS for y in POINTS if q[x] != q[y])


def l1_check() -> dict[str, int]:
    """For every family, every question and every `k ≤ 3`: every family with
    at most `k` seats replaced by Boolean tables knows `q` iff the count
    condition holds; and the same for at most `k` seats deleted."""
    checked = violations = robust_cases = 0
    for Q in families():
        size = len(Q)
        # For each set S of seats: the questions known by every assignment
        # to S (replacement), and by the family with S deleted (deletion).
        by_replaced: dict[tuple[int, ...], int] = {}
        by_deleted: dict[tuple[int, ...], int] = {}
        for r in range(size + 1):
            for S in combinations(range(size), r):
                kept = tuple(m for i, m in enumerate(Q) if i not in S)
                by_replaced[S] = replaced_mask(size, S, kept)
                by_deleted[S] = known_mask(same_family(kept))
        for k in range(MAX_SEATS + 1):
            replaced = deleted = ALL_QUESTIONS
            for S, mask in by_replaced.items():
                if len(S) <= k:
                    replaced &= mask
                    deleted &= by_deleted[S]
            for i, q in enumerate(BOOL_TABLES):
                checked += 1
                condition = robust_condition(Q, q, k)
                robust_cases += condition
                if bool(replaced >> i & 1) != condition or bool(deleted >> i & 1) != condition:
                    violations += 1
    return {"checked": checked, "violations": violations, "robust_cases": robust_cases}


# --------------------------------------------------------------------------
# L2


def l2_add_and_target_check() -> dict[str, int]:
    """(a) an added seat never breaks a decision; (d) an admitted target never
    breaks it, makes agreement known, and decisions failing their target
    exist."""
    checked = violations = target_failures = 0
    for Q in families():
        merged = same_family(Q)
        known = known_mask(merged)
        for i, q in enumerate(BOOL_TABLES):
            if not known >> i & 1:
                continue
            for t in BOOL_TABLES:
                checked += 1
                extended = known_mask(merged & same(t))
                agree = TABLE_INDEX[tuple(1 if q[x] == t[x] else 0 for x in POINTS)]
                if not extended >> i & 1 or not extended >> agree & 1:
                    violations += 1
                if q != t:
                    target_failures += 1
    return {"checked": checked, "violations": violations, "decisions_failing_a_target": target_failures}


def l2_removal_check() -> dict[str, int]:
    """(b) for every family and every set of removed seats: the kept seats
    know `q` iff every `q`-separated pair has fewer separating seats among the
    removed than in the whole; and the decision survives every Boolean
    replacement of the removed seats iff the kept seats know `q`."""
    checked = violations = 0
    for Q in families():
        size = len(Q)
        for r in range(size + 1):
            for S in combinations(range(size), r):
                kept = tuple(m for i, m in enumerate(Q) if i not in S)
                removed = tuple(Q[i] for i in S)
                every = replaced_mask(size, S, kept)
                kept_mask = known_mask(same_family(kept))
                for i, q in enumerate(BOOL_TABLES):
                    checked += 1
                    count = all(redundancy(removed, x, y) < redundancy(Q, x, y)
                                for x in POINTS for y in POINTS if q[x] != q[y])
                    kept_knows = knows(POINTS, kept, q)
                    if kept_knows != count or kept_knows != bool(kept_mask >> i & 1):
                        violations += 1
                    if bool(every >> i & 1) != kept_knows:
                        violations += 1
    return {"checked": checked, "violations": violations}


def l2_extension_check() -> dict[str, int]:
    """(c) for every carrier `D ⊂ range(4)`, every new point, every family and
    every question known on `D`: known on `D + [x]` iff `q` is constant on the
    signature class of `x` there.  Counts the decisions that break."""
    checked = violations = broken = 0
    question_same = [same(q) for q in BOOL_TABLES]
    steps = [(carrier_mask(D), carrier_mask(D + (x,)), D + (x,), x)
             for D in carriers() for x in POINTS if x not in D]
    for Q in families():
        merged = same_family(Q)
        for before_mask, after_mask, E, x in steps:
            for q, q_same in zip(BOOL_TABLES, question_same):
                if merged & before_mask & ~q_same:
                    continue
                checked += 1
                after = merged & after_mask & ~q_same == 0
                condition = all(q[x] == q[y] for y in E if merged >> (N * x + y) & 1)
                if after != condition:
                    violations += 1
                if not after:
                    broken += 1
    return {"checked": checked, "violations": violations, "broken_by_extension": broken}


# --------------------------------------------------------------------------
# L3


BALLOT_MAPS: tuple[tuple[int, int], ...] = tuple((a, b) for a in (0, 1, 2) for b in (0, 1, 2))


def ballot(f: tuple[int, int], m: Table) -> Table:
    return tuple(f[v] for v in m)


def sincere(D: tuple[int, ...], q: Table, m: Table) -> Table:
    """`Ballot.sincere`: NAY 0 or AYE 1 where `q` is settled on the seat's
    class, ABSTAIN 2 elsewhere."""
    out: list[int] = []
    for x in POINTS:
        settled = all(m[y] != m[x] or q[y] == q[x] for y in D)
        out.append((0 if q[x] == 0 else 1) if settled else 2)
    return tuple(out)


def l3_check() -> dict[str, int]:
    """For every family, every choice of per-seat ballot maps and every
    question: what the ballots know, the seats know.  Counts the strict
    losses.  Then the sincere ballots on each question: each is a function of
    its seat's answer, they know at most what the seats know, every tally of
    them knows at most what they know, and the losses of exceeding knowledge
    are counted."""
    checked = violations = strict_losses = 0
    ballot_same = {(f, m): same(ballot(f, m)) for f in BALLOT_MAPS for m in BOOL_TABLES}
    for Q in families():
        seats_mask = known_mask(same_family(Q))
        for fs in product(BALLOT_MAPS, repeat=len(Q)):
            merged = FULL
            for f, m in zip(fs, Q):
                merged &= ballot_same[(f, m)]
            ballots_mask = known_mask(merged)
            checked += len(BOOL_TABLES)
            if ballots_mask & ~seats_mask:
                violations += 1
            strict_losses += bin(seats_mask & ~ballots_mask).count("1")
    sincere_checked = sincere_violations = sincere_losses = exceeding_lost = 0
    for Q in families():
        for q in BOOL_TABLES:
            B = tuple(sincere(POINTS, q, m) for m in Q)
            sincere_checked += 1
            if any(not knows(POINTS, (m,), b) for m, b in zip(Q, B)):
                sincere_violations += 1
            if known_mask(same_family(B)) & ~known_mask(same_family(Q)):
                sincere_violations += 1
            for v in (0, 1, 2):
                tally = tuple(sum(1 for b in B if b[x] == v) for x in POINTS)
                if known_mask(same(tally)) & ~known_mask(same_family(B)):
                    sincere_violations += 1
            if knows(POINTS, Q, q) and not knows(POINTS, B, q):
                sincere_losses += 1
                if Q and not any(knows(POINTS, (m,), q) for m in Q):
                    exceeding_lost += 1
    return {"checked": checked, "violations": violations, "strict_losses": strict_losses,
            "sincere_checked": sincere_checked, "sincere_violations": sincere_violations,
            "sincere_losses": sincere_losses, "sincere_exceeding_lost": exceeding_lost}


# --------------------------------------------------------------------------
# The Lean examples, mirrored.

PARITY: Table = (0, 1, 0, 1)
HALF: Table = (0, 0, 1, 1)
IDENTITY: Table = (0, 1, 2, 3)
XOR_PH: Table = tuple((PARITY[x] + HALF[x]) % 2 for x in POINTS)


def robustness(Q: Family, q: Table) -> int:
    """The largest `k` with the L1 condition, or -1 when `Q` does not know `q`."""
    return min((redundancy(Q, x, y) for x in POINTS for y in POINTS if q[x] != q[y]), default=len(Q)) - 1


def examples() -> dict[str, object]:
    swap02 = (2, 1, 0, 3)
    swap12 = (0, 2, 1, 3)
    return {
        "robust_parity_half": [robustness((PARITY, HALF), IDENTITY),
                               robustness((PARITY, HALF, PARITY, HALF), IDENTITY)],
        "relabel_can_be_harmless": [knows(POINTS, (tuple(PARITY[swap02[x]] for x in POINTS), HALF), IDENTITY),
                                    knows(POINTS, (HALF,), IDENTITY)],
        "relabel_can_break": knows(POINTS, (tuple(PARITY[swap12[x]] for x in POINTS), HALF), IDENTITY),
        "extension_breaks": [knows((0, 2), (HALF,), PARITY), knows((0, 2, 1), (HALF,), PARITY)],
        "ballot_loses_exceeding": [knows(POINTS, (PARITY, HALF), XOR_PH),
                                   knows(POINTS, (PARITY,), XOR_PH), knows(POINTS, (HALF,), XOR_PH),
                                   [sincere(POINTS, XOR_PH, PARITY), sincere(POINTS, XOR_PH, HALF)],
                                   knows(POINTS, (sincere(POINTS, XOR_PH, PARITY), sincere(POINTS, XOR_PH, HALF)),
                                         XOR_PH)],
        "injective_ballot_keeps": knows(POINTS, (ballot((1, 0), PARITY), ballot((1, 0), HALF)), XOR_PH),
    }


def summary() -> dict[str, object]:
    return {
        "bound": {"points": N, "seat_tables": len(BOOL_TABLES), "max_seats": MAX_SEATS,
                  "institutions": sum(1 for _ in families()), "carriers": len(carriers())},
        "fast_form": fast_form_check(),
        "L0": l0_check(),
        "L1": l1_check(),
        "L2_add_target": l2_add_and_target_check(),
        "L2_removal": l2_removal_check(),
        "L2_extension": l2_extension_check(),
        "L3": l3_check(),
        "examples": examples(),
    }


if __name__ == "__main__":
    print(json.dumps(summary(), indent=2, sort_keys=True))
