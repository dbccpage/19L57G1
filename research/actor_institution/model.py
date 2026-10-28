"""Finite mirrors of the actor_institution tree.  AuthorityEffect: None.

Everything here is computed exhaustively over declared bounds and is evidence
for the VERIFIED_FINITE rows of CLAIMS.md only.  The Lean modules are the
authority for the PROVED_THEOREM rows; no test here is cited for one of
those.  The data are `range(n)`; a presentation is a tuple of values on
them; an institution is a tuple of presentations.  Partitions are listed
once each as restricted growth strings, which loses nothing: knowledge,
information, exceeding, outcomes and acquisition depend on fibers only
(`Inst.knows_rename`).
"""
from __future__ import annotations

import json
import re
import sys
from itertools import combinations, product
from pathlib import Path
from typing import Iterator

HERE = Path(__file__).resolve().parent

Presentation = tuple[int, ...]
Institution = tuple[Presentation, ...]
Pair = tuple[int, int]
Entry = tuple[int, int, bool]
Transcript = tuple[Entry, ...]
View = tuple[int, ...]
Evaluator = tuple[View, ...]

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
        if ".lake" in path.parts or path.name == "lakefile.lean":
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("import "):
                found.add(line.split()[1])
    return sorted(found - own)


MODULES = ("Institution", "Chain", "Policy", "Acquisition")


def theorem_names() -> list[str]:
    """Every `theorem` of the four modules, fully qualified, in file order."""
    names: list[str] = []
    for module in MODULES:
        stack: list[str] = []
        text = (HERE / "lean" / "ResearchActorInstitution" / f"{module}.lean").read_text(encoding="utf-8")
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
    text = (HERE / "lean" / "ResearchActorInstitution" / "AxiomReport.lean").read_text(encoding="utf-8")
    return [line.split()[2] for line in text.splitlines() if line.startswith("#print axioms ")]


def contract_declarations() -> list[str]:
    data = json.loads((HERE / "TREE_CONTRACT.json").read_text(encoding="utf-8"))
    decls = data.get("axiom_declarations")
    if not isinstance(decls, list) or any(not isinstance(d, str) for d in decls):
        raise ValueError("TREE_CONTRACT.json: axiom_declarations must be a list of names")
    return [str(d) for d in decls]


# --------------------------------------------------------------------------
# The two-theorems vocabulary on a finite carrier.


def partitions(n: int) -> list[Presentation]:
    """Every partition of range(n) once, as a restricted growth string."""
    out: list[Presentation] = []

    def rec(prefix: list[int], bound: int) -> None:
        if len(prefix) == n:
            out.append(tuple(prefix))
            return
        for v in range(bound + 1):
            rec(prefix + [v], max(bound, v + 1))

    rec([], 0)
    return out


def sig(Q: Institution, x: int) -> tuple[int, ...]:
    return tuple(q[x] for q in Q)


def knows(n: int, Q: Institution, q: Presentation) -> bool:
    """`Institution.Knows` on range(n): equal signatures force equal values."""
    return all(sig(Q, x) != sig(Q, y) or q[x] == q[y] for x in range(n) for y in range(n))


def information(n: int, Q: Institution) -> int:
    """`Institution.information`: the number of distinct signatures."""
    return len({sig(Q, x) for x in range(n)})


def exceeds(n: int, Q: Institution, q: Presentation) -> bool:
    """`Inst.Exceeds`: the family knows `q` and no member alone does."""
    return knows(n, Q, q) and all(not knows(n, (p,), q) for p in Q)


def residuals(n: int, Q: Institution, q: Presentation) -> list[Pair]:
    return [(x, y) for x in range(n) for y in range(n) if sig(Q, x) == sig(Q, y) and q[x] != q[y]]


def representative(n: int, Q: Institution, x: int) -> int:
    """`pQ`: the first datum with the signature of `x`."""
    for z in range(n):
        if sig(Q, z) == sig(Q, x):
            return z
    raise AssertionError("x is its own witness")


# --------------------------------------------------------------------------
# Exceeding: the census that mirrors the minimal counts.


def exceeding_census(max_n: int, max_k: int) -> dict[str, bool]:
    """For every carrier size `n ≤ max_n` and member count `k ≤ max_k`: does
    some institution of `k` distinct partitions know some `q` that no member
    knows?  Exhaustive over partitions, which is exhaustive over fibers."""
    out: dict[str, bool] = {}
    for n in range(1, max_n + 1):
        parts = partitions(n)
        for k in range(0, max_k + 1):
            found = any(exceeds(n, Q, q) for Q in combinations(parts, k) for q in parts)
            out[f"{n},{k}"] = found
    return out


def exceeding_minimum(census: dict[str, bool]) -> dict[str, int]:
    """The least carrier size and the least member count at which a
    *nonempty* family exceeds its members.  The empty family is left out:
    `Exceeds D [] q` holds for every constant `q` (`Inst.exceeds_nil_iff`),
    vacuously, and the Lean minima `exceeds_three_data` and
    `exceeds_two_members` assume `Q ≠ []`."""
    pairs = [tuple(int(v) for v in key.split(",")) for key, found in census.items() if found]
    nonempty = [(n, k) for n, k in pairs if k >= 1]
    return {"min_data": min(n for n, _ in nonempty), "min_members": min(k for _, k in nonempty),
            "empty_family_exceeds_on_constants": int(all(census[f"{n},0"] for n in range(1, 5)))}


# --------------------------------------------------------------------------
# Acquisition by probes: the exact minimax game.


def splits(S: frozenset[int], parts: list[Presentation], x: int, y: int) -> tuple[frozenset[int], frozenset[int]]:
    same = frozenset(i for i in S if parts[i][x] == parts[i][y])
    return same, S - same


def game_value(n: int, start: frozenset[int], parts: list[Presentation]) -> int:
    """The least `k` such that some adaptive protocol fixes the partition of
    every actor in `start` within `k` probes: a probe on a pair splits the
    consistent set; the adversary picks the larger-valued side.  A pair the
    consistent set already decides is skipped (probing it changes nothing).
    Value 0 once at most one partition is consistent (`Fixes`)."""
    pairs = list(combinations(range(n), 2))
    memo: dict[frozenset[int], int] = {}

    def value(S: frozenset[int]) -> int:
        if len(S) <= 1:
            return 0
        cached = memo.get(S)
        if cached is not None:
            return cached
        best: int | None = None
        for x, y in pairs:
            same, diff = splits(S, parts, x, y)
            if not same or not diff:
                continue
            v = 1 + max(value(same), value(diff))
            if best is None or v < best:
                best = v
        if best is None:
            raise AssertionError("two distinct partitions differ on some pair")
        memo[S] = best
        return best

    return value(start)


def blocks(p: Presentation) -> int:
    return len(set(p))


def proposal_count(n: int, N: int) -> int:
    """TT-43o (ii): `N(N−1)/2 + (n−N)(N−1)`."""
    return N * (N - 1) // 2 + (n - N) * (N - 1)


def acquisition_values(max_n: int) -> dict[str, object]:
    """Exact game values for `n ≤ max_n`: with no promise, with "at most N
    classes" promised, and with "exactly N classes" promised; each promised
    value beside the proposal's count."""
    unpromised: dict[str, int] = {}
    at_most: dict[str, list[int]] = {}
    exactly: dict[str, list[int]] = {}
    for n in range(1, max_n + 1):
        parts = partitions(n)
        unpromised[str(n)] = game_value(n, frozenset(range(len(parts))), parts)
        for N in range(1, n + 1):
            le = frozenset(i for i, p in enumerate(parts) if blocks(p) <= N)
            eq = frozenset(i for i, p in enumerate(parts) if blocks(p) == N)
            at_most[f"{n},{N}"] = [game_value(n, le, parts), proposal_count(n, N)]
            exactly[f"{n},{N}"] = [game_value(n, eq, parts), proposal_count(n, N)]
    return {
        "unpromised": unpromised,
        "half_square": {str(n): n * (n - 1) // 2 for n in range(1, max_n + 1)},
        "at_most": at_most,
        "exactly": exactly,
        "at_most_mismatches": sorted(k for k, (v, f) in at_most.items() if v != f),
        "exactly_mismatches": sorted(k for k, (v, f) in exactly.items() if v != f),
    }


# --------------------------------------------------------------------------
# Transcripts, consistency, the closure evaluator and `Fixes`.


def transcripts(n: int) -> Iterator[Transcript]:
    """Every transcript asking each pair at most once, in a fixed order."""
    pairs = list(combinations(range(n), 2))
    for answers in product((None, True, False), repeat=len(pairs)):
        yield tuple((x, y, a) for (x, y), a in zip(pairs, answers) if a is not None)


def consistent(p: Presentation, T: Transcript) -> bool:
    return all((p[x] == p[y]) == a for x, y, a in T)


def closure_evaluator(n: int, T: Transcript) -> Evaluator:
    """One view per class of the equivalence closure of the "same" answers."""
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for x, y, a in T:
        if a:
            parent[find(x)] = find(y)
    classes: dict[int, list[int]] = {}
    for z in range(n):
        classes.setdefault(find(z), []).append(z)
    return tuple(tuple(c) for c in classes.values())


def verdict(E: Evaluator, x: int, y: int) -> bool:
    """`Represented.verdictB`: some view separates the pair."""
    return any((x in c) != (y in c) for c in E)


def sharp(n: int, E: Evaluator, p: Presentation) -> bool:
    return all((not verdict(E, x, y)) == (p[x] == p[y]) for x in range(n) for y in range(n))


def fixes(n: int, T: Transcript, parts: list[Presentation]) -> bool:
    """`Acquisition.Fixes`: every two consistent actors agree on every pair."""
    cons = [p for p in parts if consistent(p, T)]
    return all((p[x] == p[y]) == (q[x] == q[y]) for p in cons for q in cons for x in range(n) for y in range(n))


def fixes_converse_check(n: int) -> dict[str, int]:
    """Over every transcript on range(n): when the transcript fixes the
    partition and some actor is consistent with it, the closure evaluator is
    sharp for every consistent actor.  Counts the cases and the violations."""
    parts = partitions(n)
    total = inconsistent = fixing = violations = 0
    for T in transcripts(n):
        total += 1
        cons = [p for p in parts if consistent(p, T)]
        if not cons:
            inconsistent += 1
            continue
        if not fixes(n, T, parts):
            continue
        fixing += 1
        E = closure_evaluator(n, T)
        if not all(sharp(n, E, p) for p in cons):
            violations += 1
    return {"transcripts": total, "inconsistent": inconsistent, "fixing": fixing, "violations": violations}


# --------------------------------------------------------------------------
# Chains of institutions: the stationary step and its tightness.


def has_stationary(n: int, chain: list[Institution]) -> bool:
    infos = [information(n, Q) for Q in chain]
    return any(a == b for a, b in zip(infos, infos[1:]))


def chain_check(n: int) -> dict[str, int | bool]:
    """Every chain of `n + 1` institutions in which each step adds one
    partition of the pool (or repeats one) has a stationary step; and some
    chain of `n` institutions has none, so the bound `|D| < length` is tight."""
    pool = partitions(n)
    chains = violations = 0
    for size in range(len(pool) + 1):
        for start in combinations(pool, size):
            for adds in product(pool, repeat=n):
                chain: list[Institution] = [tuple(start)]
                for p in adds:
                    last = chain[-1]
                    chain.append(last if p in last else last + (p,))
                chains += 1
                if not has_stationary(n, chain):
                    violations += 1
    tight = False
    for adds in product(pool, repeat=n - 1):
        chain = [()]
        for p in adds:
            chain.append(chain[-1] + (p,))
        if not has_stationary(n, chain):
            tight = True
            break
    return {"chains": chains, "violations": violations, "shorter_chain_without_stationary_step": tight}


# --------------------------------------------------------------------------
# Policy: outcomes of pair claims, and the demurred claim.


def separates(Q: Institution, x: int, y: int) -> bool:
    return any(p[x] != p[y] for p in Q)


def outcome(Q: Institution, kind: str, x: int, y: int) -> str:
    """`Policy.outcome` on `same x y` and `apart x y`."""
    if kind == "same":
        return "refuted" if separates(Q, x, y) else "unresolved"
    if kind == "apart":
        return "supported" if separates(Q, x, y) else "unresolved"
    raise ValueError(kind)


def outcome_check(n: int) -> dict[str, int]:
    """Over every institution drawn from the pool, every extension of it by
    pool members and every pair: `same` is never supported, `apart` is never
    refuted, a supported `apart` and a refuted `same` persist under extension,
    and for distinct data some extension refutes `same`."""
    pool = partitions(n)
    checked = violations = 0
    subsets = [tuple(Q) for size in range(len(pool) + 1) for Q in combinations(pool, size)]
    for Q in subsets:
        for Q2 in subsets:
            if not all(p in Q2 for p in Q):
                continue
            for x in range(n):
                for y in range(n):
                    checked += 1
                    if outcome(Q, "same", x, y) == "supported" or outcome(Q, "apart", x, y) == "refuted":
                        violations += 1
                    if outcome(Q, "apart", x, y) == "supported" and outcome(Q2, "apart", x, y) != "supported":
                        violations += 1
                    if outcome(Q, "same", x, y) == "refuted" and outcome(Q2, "same", x, y) != "refuted":
                        violations += 1
        for x in range(n):
            for y in range(n):
                if x != y and not any(outcome(Q2, "same", x, y) == "refuted" for Q2 in subsets
                                      if all(p in Q2 for p in Q)):
                    violations += 1
    return {"checked": checked, "violations": violations}


def settled(n: int, Q: Institution, s: Presentation, x: int) -> bool:
    return all(sig(Q, x) != sig(Q, y) or s[x] == s[y] for y in range(n))


def demurred(n: int, Q: Institution, s: Presentation) -> Presentation:
    """`Policy.demurred`: the claim with its unsettled points marked 0."""
    return tuple(s[x] + 1 if settled(n, Q, s, x) else 0 for x in range(n))


def demurred_check(n: int) -> dict[str, int]:
    """The demurred claim is known by every institution of pool members, and
    it is total exactly when the claim itself is known."""
    pool = partitions(n)
    checked = violations = 0
    for size in range(len(pool) + 1):
        for Q in combinations(pool, size):
            for s in pool:
                checked += 1
                d = demurred(n, Q, s)
                if not knows(n, Q, d):
                    violations += 1
                if all(v != 0 for v in d) != knows(n, Q, s):
                    violations += 1
    return {"checked": checked, "violations": violations}


# --------------------------------------------------------------------------
# The Lean examples, mirrored.

P1: Presentation = (0, 1, 0)
P2: Presentation = (0, 1, 1)
Q3: Presentation = (0, 0, 1)
PARITY4: Presentation = (0, 1, 0, 1)
HALF4: Presentation = (0, 0, 1, 1)
ID4: Presentation = (0, 1, 2, 3)


def examples() -> dict[str, object]:
    return {
        "exceeds_three_two": exceeds(3, (P1, P2), Q3),
        "exceeds_three_two_resolution": [information(3, (P1,)), information(3, (P2,)),
                                         information(3, (Q3,)), information(3, (P1, P2))],
        "correspondence_matters": [knows(3, (P1, P2), Q3), knows(3, (P1, (P2[1], P2[0], P2[2])), Q3)],
        "aggregate_hides_exceeding": [
            [representative(4, (PARITY4, HALF4), x) for x in range(4)],
            exceeds(4, (PARITY4, HALF4), ID4), exceeds(4, (ID4,), ID4)],
        "consensus_after_loss": [sig((P1, P2), 0) != sig((P1, P2), 2), sig((P1,), 0) == sig((P1,), 2),
                                 knows(3, (P1, P2), Q3), knows(3, (P1,), Q3)],
        "information_without_determination": [information(4, (PARITY4,)), knows(4, (PARITY4,), HALF4)],
        "residuals_parity_half": residuals(4, (PARITY4,), HALF4),
    }


def summary(max_game_n: int = 5) -> dict[str, object]:
    census = exceeding_census(4, 3)
    return {
        "exceeding_census": census,
        "exceeding_minimum": exceeding_minimum(census),
        "acquisition": acquisition_values(max_game_n),
        "fixes_converse": {str(n): fixes_converse_check(n) for n in range(1, 5)},
        "chains": {"3": chain_check(3)},
        "outcomes": {"3": outcome_check(3)},
        "demurred": {"3": demurred_check(3)},
        "examples": examples(),
    }


if __name__ == "__main__":
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(json.dumps(summary(max_n), indent=2, sort_keys=True))
