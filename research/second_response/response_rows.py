"""The finite cross-check for rung ten: adjacency, reach, branching and
exhaustion.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel,
  the sealed profiles, the sealed responder and its candidate space, the
  sealed key procedure, the sealed genesis readings, rung three's
  ``research/second_index/index.py`` and rung four's
  ``research/second_iso/iso_index.py``, all imported read-only through
  their public functions and pinned by blob in ``SOURCE_MANIFEST.json``.
  No sibling source is copied.
* The rectangle and its three bases are rung three's, consumed unchanged
  through rung four's population.  A class of regimes is the sealed key
  procedure's, through rung four's memoized keys, and the key partition
  is compared again here with the sealed brute-force minimum.
* The RESPONDER is the sealed ``min_responses`` at the sealed default
  bounds, under each sealed measure, consumed unchanged.  It refuses to
  run on a regime holding a uniform rule; such a regime is OUTSIDE THE
  DOMAIN and is counted, never widened into.
* A DEMAND is a pair the sealed ``collapsed_pairs`` returns -- a demand
  read off the state, never emitted by an act.  A RESPONSE is a model
  proposal: the responded regime is read, and nothing of the rectangle
  is changed by it.
* A pair is MOVED when the sealed profiles of its two data are equal on
  one side of the response and different on the other.  The REACH of a
  response is the set of data other than the two demanded that lie in a
  moved pair.  Two pairs are ADJACENT when one response moves both.
  Tie classes are the sealed key procedure's classes of the regime the
  demanded requirement and the response's events reach, as the sealed
  engine forms them.
* A form is EXHAUSTED when no sealed context on it gives two admitted
  data different derivability.
* The enumeration is a FINITE COMPUTATION over a declared rectangle.
* Nothing here is a theorem.  The theorems of this rung are in ``lean/``.
"""

from __future__ import annotations

import pathlib
import sys
from collections import deque
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Sequence

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_ISO_TREE = str(REPO / "research" / "second_iso")
if _ISO_TREE not in sys.path:
    sys.path.insert(0, _ISO_TREE)

# Rung four's module puts rung three, the sealed kernel and the sibling
# trees on the path, and puts its OWN tree at the front.  Each of those
# trees carries modules named `verify_pins`, `check_coverage` and
# `test_*`, so this tree goes back to the front AFTER the import, or a
# sibling's module is silently loaded in place of this rung's -- the
# defect rung three found live, and rungs four to nine recorded again.
from iso_index import (  # noqa: E402
    ALPHABET,
    Keys,
    Population,
    build_population,
    partition_disagreements,
)
from index import BASE_NAMES, EMPTY_BASE  # noqa: E402
from nofirst import Alphabet  # noqa: E402
from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    MinResponses,
    NewInst,
    NewRuleAll,
    apply_delta,
    delta_events,
    iter_full_deltas,
    min_responses,
    mu2,
    response_valid_naive,
)
from derivation.iso import CanonKey, canonical, canonical_bruteforce  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Event,
    Impose,
    Pair,
    Regime,
    replay,
    step,
)
from derivation.observe import (  # noqa: E402
    Context,
    collapsed_pairs,
    contexts,
    derivable,
    plug,
    profiles,
)

if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

MEASURES = ("mu1", "mu2")
BOUNDS = Bounds()


# ---------------------------------------------------------------------------
# Exhaustion, read off one regime
# ---------------------------------------------------------------------------


def distinguishes(regime: Regime, form: int) -> bool:
    """Some sealed context on the form gives two admitted data different
    derivability."""
    n = regime.n_data()
    for ctx in contexts(regime):
        if ctx[0] != form:
            continue
        seen = {derivable(regime, plug(ctx, d)) for d in range(n)}
        if len(seen) > 1:
            return True
    return False


def exhausted_count(regime: Regime) -> int:
    return sum(1 for f in range(len(regime.forms)) if not distinguishes(regime, f))


def holds_two(regime: Regime) -> bool:
    """Two admitted data with different sealed profiles."""
    return len(set(profiles(regime))) > 1


# ---------------------------------------------------------------------------
# The responder, and what one response does
# ---------------------------------------------------------------------------


def in_domain(regime: Regime) -> bool:
    """Whether the sealed responder runs on the regime.  Decided by calling
    it, not by reading the rule set: its refusal is a ``ValueError``."""
    try:
        min_responses(regime, (0, 0), "mu1", BOUNDS)
    except ValueError:
        return False
    return True


def moved_pairs(before: Regime, after: Regime) -> tuple[tuple[Pair, bool], ...]:
    """Every pair of data of ``before`` whose separability differs in
    ``after``, with True when it moved apart."""
    pb = profiles(before)
    pa = profiles(after)
    n = before.n_data()
    out: list[tuple[Pair, bool]] = []
    for i in range(n):
        for j in range(i + 1, n):
            sep_b = pb[i] != pb[j]
            sep_a = pa[i] != pa[j]
            if sep_b != sep_a:
                out.append(((i, j), sep_a))
    return tuple(out)


def mentioned(delta: Delta) -> frozenset[int]:
    return frozenset(a for it in delta if isinstance(it, NewInst) for a in it.args)


@dataclass(frozen=True)
class Response:
    delta: Delta
    moved: tuple[tuple[Pair, bool], ...]
    reach: frozenset[int]
    tie_key: CanonKey
    responded_imposed: Regime


@dataclass(frozen=True)
class Answer:
    """One demand at one regime under one measure."""

    target: Pair
    cost: Optional[tuple[int, int]]
    responses: tuple[Response, ...]

    def tie_classes(self) -> int:
        return len({r.tie_key for r in self.responses})


class Responder:
    """Memoized calls of the sealed responder and the sealed keys."""

    def __init__(self) -> None:
        self._answers: dict[tuple[Regime, Pair, str], Answer] = {}
        self._keys: dict[Regime, CanonKey] = {}
        self._domain: dict[Regime, bool] = {}

    def key(self, regime: Regime) -> CanonKey:
        found = self._keys.get(regime)
        if found is None:
            found = canonical(regime)
            self._keys[regime] = found
        return found

    def domain(self, regime: Regime) -> bool:
        found = self._domain.get(regime)
        if found is None:
            found = in_domain(regime)
            self._domain[regime] = found
        return found

    def answer(self, regime: Regime, target: Pair, measure: str) -> Answer:
        memo = (regime, target, measure)
        found = self._answers.get(memo)
        if found is not None:
            return found
        mr: Optional[MinResponses] = min_responses(regime, target, measure, BOUNDS)
        if mr is None:
            found = Answer(target, None, ())
        else:
            rows: list[Response] = []
            for delta in mr.deltas:
                responded = apply_delta(regime, delta)
                moved = moved_pairs(regime, responded)
                reach = frozenset(
                    k for pair, _ in moved for k in pair if k not in target
                )
                imposed = replay(
                    (Impose(target[0], target[1]),) + delta_events(regime, delta),
                    regime,
                )
                rows.append(Response(delta, moved, reach, self.key(imposed), imposed))
            found = Answer(target, mr.cost, tuple(rows))
        self._answers[memo] = found
        return found

    def answers(self, regime: Regime, measure: str) -> tuple[Answer, ...]:
        return tuple(
            self.answer(regime, t, measure) for t in collapsed_pairs(regime)
        )


# ---------------------------------------------------------------------------
# The adjacency graph of one regime
# ---------------------------------------------------------------------------


def adjacency(
    n: int, answers: Sequence[Answer]
) -> tuple[int, tuple[int, ...], int]:
    """Edges, sorted sizes of the connected pieces, and the largest finite
    distance of the graph on the pairs of ``n`` data."""
    vertices = [(i, j) for i in range(n) for j in range(i + 1, n)]
    edges: set[tuple[Pair, Pair]] = set()
    for ans in answers:
        for resp in ans.responses:
            pairs = sorted(pair for pair, _ in resp.moved)
            for x in range(len(pairs)):
                for y in range(x + 1, len(pairs)):
                    edges.add((pairs[x], pairs[y]))
    nbrs: dict[Pair, set[Pair]] = {v: set() for v in vertices}
    for a, b in edges:
        nbrs[a].add(b)
        nbrs[b].add(a)
    largest = 0
    seen: set[Pair] = set()
    sizes: list[int] = []
    for v in vertices:
        dist = {v: 0}
        queue = deque([v])
        while queue:
            u = queue.popleft()
            for w in sorted(nbrs[u]):
                if w not in dist:
                    dist[w] = dist[u] + 1
                    queue.append(w)
        largest = max(largest, max(dist.values()))
        if v not in seen:
            seen.update(dist)
            sizes.append(len(dist))
    return len(edges), tuple(sorted(sizes)), largest


def signature(regime: Regime, measure: str, responder: Responder) -> tuple[object, ...]:
    """The response signature of a regime under a measure (PREDICTIONS.md,
    declared readings)."""
    if not responder.domain(regime):
        return (False,)
    answers = responder.answers(regime, measure)
    rows = sorted(
        (
            ans.cost if ans.cost is not None else (-1, -1),
            len(ans.responses),
            ans.tie_classes(),
            tuple(
                sorted(
                    (
                        sum(1 for _, apart in r.moved if apart),
                        sum(1 for _, apart in r.moved if not apart),
                        len(r.reach),
                    )
                    for r in ans.responses
                )
            ),
        )
        for ans in answers
    )
    return (True, tuple(rows), adjacency(regime.n_data(), answers))


# ---------------------------------------------------------------------------
# One base's rectangle
# ---------------------------------------------------------------------------


def _least(current: Optional[int], length: int) -> int:
    return length if current is None or length < current else current


def measure_report(
    nodes: Sequence[tuple[tuple[Event, ...], Regime]],
    measure: str,
    responder: Responder,
) -> dict[str, Any]:
    """What the responder does, under one measure, over one base."""
    regimes = sorted({r for _, r in nodes if responder.domain(r)}, key=repr)
    demands = refused = responses = 0
    by_cost: dict[str, int] = {}
    with_rule = without_mention = unmentioned_moves = demand_not_apart = 0
    together = empty_reach = nonempty_reach = reach_mismatch = class_violations = 0
    largest_reach = 0
    tie_hist: dict[int, int] = {}
    ties_one = 0
    largest_tie_classes = 0
    validity_failures = 0
    largest_distance = 0
    regimes_distance_two = 0
    largest_edges = 0
    edge_regimes: set[Regime] = set()
    branch_regimes: set[Regime] = set()
    for regime in regimes:
        answers = responder.answers(regime, measure)
        prof = profiles(regime)
        edges, _, dist = adjacency(regime.n_data(), answers)
        largest_edges = max(largest_edges, edges)
        largest_distance = max(largest_distance, dist)
        if dist >= 2:
            regimes_distance_two += 1
        if edges:
            edge_regimes.add(regime)
        for ans in answers:
            demands += 1
            if ans.cost is None:
                refused += 1
                continue
            key = str(ans.cost[0])
            by_cost[key] = by_cost.get(key, 0) + 1
            tie_hist[len(ans.responses)] = tie_hist.get(len(ans.responses), 0) + 1
            if len(ans.responses) == 1:
                ties_one += 1
            largest_tie_classes = max(largest_tie_classes, ans.tie_classes())
            if ans.tie_classes() >= 2:
                branch_regimes.add(regime)
            i, j = ans.target
            cls = {k for k in range(regime.n_data()) if prof[k] == prof[i]} - {i, j}
            for resp in ans.responses:
                responses += 1
                if not response_valid_naive(regime, ans.target, resp.delta):
                    validity_failures += 1
                if any(isinstance(it, NewRuleAll) for it in resp.delta):
                    with_rule += 1
                ment = mentioned(resp.delta)
                if not ment & {i, j}:
                    without_mention += 1
                if any(not (set(pair) & ment) for pair, _ in resp.moved):
                    unmentioned_moves += 1
                if (ans.target, True) not in resp.moved:
                    demand_not_apart += 1
                if any(not apart for _, apart in resp.moved):
                    together += 1
                if resp.reach:
                    nonempty_reach += 1
                else:
                    empty_reach += 1
                if bool(resp.reach) != (len(resp.moved) >= 2):
                    reach_mismatch += 1
                if not cls <= resp.reach:
                    class_violations += 1
                largest_reach = max(largest_reach, len(resp.reach))
    least_edge: Optional[int] = None
    least_branch: Optional[int] = None
    for history, regime in nodes:
        if regime in edge_regimes:
            least_edge = _least(least_edge, len(history))
        if regime in branch_regimes:
            least_branch = _least(least_branch, len(history))
    return {
        "regimes_in_domain": len(regimes),
        "demands": demands,
        "refused": refused,
        "answered_by_cost": dict(sorted(by_cost.items())),
        "responses": responses,
        "responses_with_rule_item": with_rule,
        "responses_mentioning_no_demanded_datum": without_mention,
        "responses_moving_an_unmentioned_pair": unmentioned_moves,
        "responses_not_moving_their_demand_apart": demand_not_apart,
        "responses_moving_a_pair_together": together,
        "responses_with_empty_reach": empty_reach,
        "responses_with_nonempty_reach": nonempty_reach,
        "reach_two_pair_mismatches": reach_mismatch,
        "reach_class_violations": class_violations,
        "largest_reach": largest_reach,
        "tie_count_histogram": {str(k): tie_hist[k] for k in sorted(tie_hist)},
        "demands_with_tie_count_one": ties_one,
        "largest_tie_class_count": largest_tie_classes,
        "largest_edge_count": largest_edges,
        "largest_finite_distance": largest_distance,
        "regimes_with_distance_at_least_two": regimes_distance_two,
        "least_length_with_an_edge": least_edge,
        "least_length_with_two_tie_classes": least_branch,
        "reference_validity_failures": validity_failures,
    }


def refinement_violations(
    nodes: Sequence[tuple[tuple[Event, ...], Regime]], responder: Responder
) -> dict[str, int]:
    """Whether the two measures refuse the same demands, and whether every
    ``mu2`` response is a ``mu1`` response."""
    refusal = subset = 0
    for regime in sorted({r for _, r in nodes if responder.domain(r)}, key=repr):
        for t in collapsed_pairs(regime):
            one = responder.answer(regime, t, "mu1")
            two = responder.answer(regime, t, "mu2")
            if (one.cost is None) != (two.cost is None):
                refusal += 1
            if not {r.delta for r in two.responses} <= {r.delta for r in one.responses}:
                subset += 1
    return {"refusal_disagreements": refusal, "mu2_not_among_mu1": subset}


def exhaustion_report(
    nodes: Sequence[tuple[tuple[Event, ...], Regime]], counts: dict[Regime, int]
) -> dict[str, Any]:
    by_history = dict(nodes)
    regimes = {r for _, r in nodes}
    histogram: dict[int, int] = {}
    mismatches = rule_violations = 0
    for r in regimes:
        c = counts[r]
        histogram[c] = histogram.get(c, 0) + 1
        if holds_two(r) != (c < len(r.forms)):
            mismatches += 1
        for f in r.rules:
            if distinguishes(r, f):
                rule_violations += 1
    changes: dict[str, set[int]] = {}
    least_any: Optional[int] = None
    least_two: Optional[int] = None
    for history, regime in nodes:
        if counts[regime] > 0:
            least_any = _least(least_any, len(history))
            if holds_two(regime):
                least_two = _least(least_two, len(history))
        if history:
            before = by_history[history[:-1]]
            kind = type(history[-1]).__name__
            changes.setdefault(kind, set()).add(counts[regime] - counts[before])
    return {
        "exhausted_count_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "holds_two_mismatches": mismatches,
        "ruled_forms_distinguishing": rule_violations,
        "changes_by_kind": {k: sorted(v) for k, v in sorted(changes.items())},
        "least_length_with_an_exhausted_form": least_any,
        "least_length_holding_two_with_an_exhausted_form": least_two,
    }


# ---------------------------------------------------------------------------
# Classes of regimes
# ---------------------------------------------------------------------------


def lumping(
    groups: Sequence[Sequence[Regime]],
    keys: Keys,
    counts: dict[Regime, int],
    responder: Responder,
) -> dict[str, int]:
    values: dict[str, dict[CanonKey, set[object]]] = {
        "exhausted_count": {},
        "signature_mu1": {},
        "signature_mu2": {},
    }
    for group in groups:
        for regime in group:
            key = keys.key(regime)
            values["exhausted_count"].setdefault(key, set()).add(counts[regime])
            for m in MEASURES:
                values[f"signature_{m}"].setdefault(key, set()).add(
                    signature(regime, m, responder)
                )
    out = {"classes": len(values["exhausted_count"])}
    for name, table in values.items():
        out[f"classes_with_two_values_of_{name}"] = sum(
            1 for v in table.values() if len(v) > 1
        )
    return out


def class_report(
    population: Population, counts: dict[Regime, int], responder: Responder
) -> dict[str, Any]:
    keys = population.keys
    within = {
        rect.base: lumping([[n.regime for n in rect.nodes]], keys, counts, responder)
        for rect in population.rects
    }
    return {
        "within_base": within,
        "over_all_bases": lumping([population.regimes], keys, counts, responder),
        "distinct_regimes_over_all_bases": len(population.regimes),
        "key_brute_disagreements": partition_disagreements(population.regimes, keys),
    }


# ---------------------------------------------------------------------------
# The declared cross-check family
# ---------------------------------------------------------------------------


def unpruned(regime: Regime, target: Pair, measure: str) -> Optional[frozenset[Delta]]:
    """The minimum, under the measure, of the sealed unpruned enumeration
    filtered by the sealed reference validity; None when none is valid
    within two items."""
    for cost in range(0, BOUNDS.max_items + 1):
        valid = [
            d
            for d in iter_full_deltas(regime, cost, BOUNDS)
            if response_valid_naive(regime, target, d)
        ]
        if not valid:
            continue
        if measure == "mu1":
            return frozenset(valid)
        best = min(mu2(d) for d in valid)
        return frozenset(d for d in valid if mu2(d) == best)
    return None


def crosscheck(regimes: Iterable[Regime], responder: Responder) -> dict[str, int]:
    situations = response_disagreements = refusal_disagreements = 0
    partition_disagreements_ = 0
    for regime in regimes:
        if not responder.domain(regime):
            continue
        for t in collapsed_pairs(regime):
            for m in MEASURES:
                situations += 1
                ans = responder.answer(regime, t, m)
                ref = unpruned(regime, t, m)
                if (ans.cost is None) != (ref is None):
                    refusal_disagreements += 1
                    continue
                if ref is not None and frozenset(r.delta for r in ans.responses) != ref:
                    response_disagreements += 1
                by_key: dict[object, set[Delta]] = {}
                by_brute: dict[object, set[Delta]] = {}
                for r in ans.responses:
                    by_key.setdefault(r.tie_key, set()).add(r.delta)
                    by_brute.setdefault(
                        canonical_bruteforce(r.responded_imposed), set()
                    ).add(r.delta)
                if {frozenset(v) for v in by_key.values()} != {
                    frozenset(v) for v in by_brute.values()
                }:
                    partition_disagreements_ += 1
    return {
        "situations": situations,
        "response_disagreements": response_disagreements,
        "refusal_disagreements": refusal_disagreements,
        "tie_partition_disagreements": partition_disagreements_,
    }


# ---------------------------------------------------------------------------
# The Lean witnesses, written in the sealed Python grammar
# ---------------------------------------------------------------------------


def lean_witnesses() -> dict[str, Any]:
    """RECORDED, not scored.  The two moving countermodels of
    `lean/SecondResponse/Move.lean`, replayed by the sealed Python step
    from the sealed empty regime; the Lean regimes carry no presentation
    token, so the three data here are given the first three fresh tokens."""
    a, b, c = ALPHABET.fresh_tokens[:3]
    three = replay((AdmitDatum(a), AdmitDatum(b), AdmitDatum(c), AdmitForm(1)), EMPTY)
    two_pairs = step(three, AdmitInst(0, (0,)))
    ruled_two = step(three, AdmitInst(0, (2,)))
    collapses = step(ruled_two, AdmitInst(0, (0,)))
    return {
        "one_inst_moves_two_pairs": [
            [list(p), apart] for p, apart in moved_pairs(three, two_pairs)
        ],
        "response_collapses_a_pair": [
            [list(p), apart] for p, apart in moved_pairs(ruled_two, collapses)
        ],
    }


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------


def all_reports(alphabet: Alphabet = ALPHABET) -> dict[str, Any]:
    population = build_population(alphabet)
    responder = Responder()
    counts = {r: exhausted_count(r) for r in population.regimes}
    bases: dict[str, Any] = {}
    changes: dict[str, set[int]] = {}
    for rect in population.rects:
        nodes = [(node.history, node.regime) for node in rect.nodes]
        regimes = {r for _, r in nodes}
        inside = sum(1 for r in regimes if responder.domain(r))
        row: dict[str, Any] = {
            "sequences": len(nodes),
            "distinct_regimes": len(regimes),
            "replay_mismatches": sum(
                1 for h, r in nodes if replay(h, rect.regime) != r
            ),
            "regimes_in_domain": inside,
            "regimes_outside_domain": len(regimes) - inside,
            "outside_domain_without_rules": sum(
                1 for r in regimes if not responder.domain(r) and not r.rules
            ),
            "inside_domain_with_rules": sum(
                1 for r in regimes if responder.domain(r) and r.rules
            ),
            "measures": {m: measure_report(nodes, m, responder) for m in MEASURES},
            "refinement": refinement_violations(nodes, responder),
            "exhaustion": exhaustion_report(nodes, counts),
        }
        bases[rect.base] = row
        for kind, values in row["exhaustion"]["changes_by_kind"].items():
            changes.setdefault(kind, set()).update(values)
    empty_rect = next(rect for rect in population.rects if rect.base == EMPTY_BASE)
    family = sorted({n.regime for n in empty_rect.nodes}, key=repr)
    return {
        "base_order": list(BASE_NAMES),
        "bounds": {"max_items": BOUNDS.max_items, "max_arity": BOUNDS.max_arity},
        "bases": bases,
        "exhaustion_changes_over_all_bases": {
            k: sorted(v) for k, v in sorted(changes.items())
        },
        "classes": class_report(population, counts, responder),
        "crosscheck_empty_base": crosscheck(family, responder),
        "lean_witnesses": lean_witnesses(),
    }


__all__ = [
    "ALPHABET",
    "Answer",
    "MEASURES",
    "Responder",
    "adjacency",
    "all_reports",
    "crosscheck",
    "distinguishes",
    "exhausted_count",
    "exhaustion_report",
    "holds_two",
    "in_domain",
    "lean_witnesses",
    "measure_report",
    "mentioned",
    "moved_pairs",
    "signature",
    "unpruned",
]
