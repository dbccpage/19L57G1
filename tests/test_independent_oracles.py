"""Independent-oracle strengthening tests (open work, outside the seal).

Provenance: these tests were written in response to an external source-audit
of this repository's Python module/test adequacy.  The audit's three
strengthening recommendations that can be honoured *without* touching the
sealed derivation are implemented here:

  1. exact-set pins in place of count-only pins, and
  2. an independent enumeration oracle in place of a shared one, and
  3. an independent census recount in place of a same-report subtotal
     reconciliation.

Nothing here modifies a sealed path.  `tests/` is outside the blind
contract (see CLAUDE.md, "Repository boundary"), so an *additional* test
file that only reads and re-derives committed values is open work — it pins
the load-bearing numbers harder without amending the frozen evidence.

Discipline: each test recomputes a committed result by a route that shares
as little machinery as possible with the code that first produced it, then
asserts the two agree.  The *semantics* under study (`pstep`, `comp_ren`,
`act`, `response_valid_naive`) are necessarily shared — re-implementing them
would test the re-implementation, not the derivation.  What is made
independent is the *enumeration*, the *validity route*, and the *counting
formula*.  No negative-input rejection test is included: the sealed guards
accept out-of-range indices by construction (a declared Nat-vs-int gap), so
such a test would fail against frozen code and belongs to a successor, not
here.
"""

from __future__ import annotations

import json
from math import comb

import pytest

from derivation.candidates import (
    Bounds,
    NewForm,
    NewInst,
    canonical_delta,
    iter_cost1_items,
    iter_full_deltas,
    min_responses,
    mu2,
    response_valid_naive,
)
from derivation.model import AdmitDatum, Pair, Regime, replay
from derivation.renaming_structure import (
    action_laws,
    act,
    comp_ren,
    group_laws,
    id_ren,
    inv_ren,
    sample_states,
)
from derivation.trace_algebra import (
    EVENT_BATTERY,
    comm_states,
    commutation_report,
    pstep,
    state_size,
)
from derivation.transition_alphabet import event_json

BOUNDS = Bounds(max_items=2, max_arity=2)


# ---------------------------------------------------------------------------
# 1. Candidates: the Challenge-3 minimum separators, as an EXACT SET, derived
#    independently of `min_responses`.
#
#    `min_responses` enumerates the *pruned* cost-2 space and validates with
#    the *fast incremental* checker.  The oracle below enumerates the
#    *unpruned brute-force* space (`iter_full_deltas`) and validates with the
#    *naive replay* checker (`response_valid_naive`) — two independent
#    substitutions — then pins the resulting set of minima member by member,
#    upgrading the shipped count-only `len(...) == 6` assertion to an
#    exact-set assertion and cross-checking `min_responses` against it.
# ---------------------------------------------------------------------------


def _c3_base() -> Regime:
    """The Challenge-3 reading-L regime: <a>, <ab> retained, before Impose."""
    return replay([AdmitDatum("<a>"), AdmitDatum("<ab>")])


def _independent_valid_cost2(base: Regime, target: Pair) -> set[tuple]:
    """Every well-formed cost-2 delta that separates ``target``, found by
    brute-force enumeration and replay validation — no pruning lemmas, no
    incremental checker."""
    return {
        canonical_delta(delta)
        for delta in iter_full_deltas(base, 2, BOUNDS)
        if response_valid_naive(base, target, delta)
    }


def test_c3_no_valid_delta_below_cost_two() -> None:
    """The minimum sits at cost 2 only because cost 0 and cost 1 are empty;
    the oracle below relies on that, so it is asserted here independently
    (naive replay, not the incremental checker)."""
    base = _c3_base()
    target: Pair = (0, 1)
    assert not response_valid_naive(base, target, ())
    for it in iter_cost1_items(base, BOUNDS):
        assert not response_valid_naive(base, target, (it,))


def test_c3_mu1_minimum_is_exactly_these_six_separators() -> None:
    """Exact-set pin (was count-only).  The six minimum one-step separators
    of <a> from <ab> are exactly: mark either datum with a fresh unary form,
    or relate the pair with any of the four fresh-binary-form instances."""
    base = _c3_base()
    target: Pair = (0, 1)

    expected = {
        canonical_delta((NewForm(1), NewInst(0, (0,)))),
        canonical_delta((NewForm(1), NewInst(0, (1,)))),
        canonical_delta((NewForm(2), NewInst(0, (0, 0)))),
        canonical_delta((NewForm(2), NewInst(0, (0, 1)))),
        canonical_delta((NewForm(2), NewInst(0, (1, 0)))),
        canonical_delta((NewForm(2), NewInst(0, (1, 1)))),
    }

    independent = _independent_valid_cost2(base, target)
    assert independent == expected

    # min_responses (pruned space + fast checker) must reproduce the same
    # SET, not merely the same count.
    mr = min_responses(base, target, "mu1", BOUNDS)
    assert mr is not None
    assert mr.cost[0] == 2
    assert set(mr.deltas) == expected
    assert len(mr.deltas) == len(expected)  # no duplicates in the shipped tuple


def test_c3_mu2_minimum_is_exactly_the_two_unary_marks() -> None:
    """Under mu2 (item count, then new-form arity sum) the four binary
    separators are strictly dearer, so the minimum is exactly the two unary
    marks at cost (2, 1) — re-derived from the independent valid set."""
    base = _c3_base()
    target: Pair = (0, 1)

    valid = _independent_valid_cost2(base, target)
    best = min(mu2(d) for d in valid)
    independent_min = {d for d in valid if mu2(d) == best}

    expected = {
        canonical_delta((NewForm(1), NewInst(0, (0,)))),
        canonical_delta((NewForm(1), NewInst(0, (1,)))),
    }
    assert best == (2, 1)
    assert independent_min == expected

    mr = min_responses(base, target, "mu2", BOUNDS)
    assert mr is not None
    assert mr.cost == (2, 1)
    assert set(mr.deltas) == expected


# ---------------------------------------------------------------------------
# 2. Renaming: the symmetric group and its action, reconstructed WITHOUT
#    `itertools.permutations`.
#
#    A shipped assertion of the form `len(list(permutations(range(3)))) == 6`
#    tests the standard library, not this repository's renaming action.  The
#    oracle below builds S_3 by hand, confirms it is the same population the
#    module uses, and then exercises the module's own `comp_ren`/`inv_ren`/
#    `id_ren`/`act` to certify the group and action laws over it.
# ---------------------------------------------------------------------------


def _perms_by_hand(n: int) -> list[tuple[int, ...]]:
    """All bijections of range(n), generated by backtracking — an
    independent construction of the symmetric group's carrier."""

    def rec(rem: tuple[int, ...]) -> list[tuple[int, ...]]:
        if not rem:
            return [()]
        out: list[tuple[int, ...]] = []
        for i, x in enumerate(rem):
            for tail in rec(rem[:i] + rem[i + 1 :]):
                out.append((x,) + tail)
        return out

    return rec(tuple(range(n)))


@pytest.mark.parametrize("n", [1, 2, 3])
def test_symmetric_group_reconstructed_independently_of_itertools(n: int) -> None:
    """The renaming carrier is a genuine symmetric group: the hand-built
    population has order n!, and the module's composition/inverse close it
    into a group (identity, closure, inverses, associativity)."""
    mine = _perms_by_hand(n)
    mine_set = set(mine)

    # independent order, and no duplicates from the backtracker
    assert len(mine) == len(mine_set)
    from math import factorial

    assert len(mine_set) == factorial(n)

    ident = id_ren(n)
    assert ident == tuple(range(n))
    assert ident in mine_set

    # group axioms verified over the module's own operations
    assert all(comp_ren(s, ident) == s == comp_ren(ident, s) for s in mine)
    assert all(comp_ren(s, t) in mine_set for s in mine for t in mine)  # closure
    assert all(
        comp_ren(inv_ren(s), s) == ident and comp_ren(s, inv_ren(s)) == ident
        for s in mine
    )
    assert all(
        comp_ren(comp_ren(a, b), c) == comp_ren(a, comp_ren(b, c))
        for a in mine
        for b in mine
        for c in mine
    )

    # and the module's own report agrees, over the same population
    laws = group_laws(n)
    assert laws["group_order"] == factorial(n)
    assert all(v is True for k, v in laws.items() if isinstance(v, bool))


def test_action_laws_hold_over_independently_generated_group() -> None:
    """The renaming *action* (not just the group) satisfies identity,
    composition, and inversion on the declared sample states, checked over
    the hand-built S_3 through the module's own `act`."""
    n = 3
    perms = _perms_by_hand(n)
    ident = id_ren(n)
    states = sample_states(n)
    assert len(states) == 2  # star, path

    assert all(act(ident, s) == s for s in states)
    assert all(
        act(comp_ren(a, b), s) == act(a, act(b, s))
        for a in perms
        for b in perms
        for s in states
    )
    assert all(
        act(inv_ren(a), act(a, s)) == s for a in perms for s in states
    )

    laws = action_laws(n)
    assert all(v is True for k, v in laws.items() if isinstance(v, bool))


# ---------------------------------------------------------------------------
# 3. Trace: the unordered-pair commutation census, recounted independently.
#
#    The shipped report exposes commuting/non-commuting subtotals and their
#    sum.  Reconciling the sum against its own addends is a tautology.  The
#    oracle below recomputes the pair count from C(k, 2), reclassifies every
#    pair by a full scan of the battery (not the report's early-exit smallest
#    -witness search), and independently recomputes each witness size, then
#    asserts agreement.
# ---------------------------------------------------------------------------


def _pair_key(e1: object, e2: object) -> tuple[str, str]:
    """Order-independent key for an unordered event pair, via the shared
    canonical `event_json`."""
    a = json.dumps(event_json(e1), sort_keys=True)
    b = json.dumps(event_json(e2), sort_keys=True)
    return (a, b) if a <= b else (b, a)


def test_commutation_census_matches_independent_recount() -> None:
    """91 commuting and 62 non-commuting unordered pairs, partitioning all
    C(18, 2) = 153 pairs — recounted from scratch and matched to the
    shipped report."""
    states = list(comm_states())
    k = len(EVENT_BATTERY)
    assert k == 18
    n_pairs = comb(k, 2)
    assert n_pairs == 153

    commuting = 0
    non_commuting = 0
    for a in range(k):
        for b in range(a + 1, k):
            e1, e2 = EVENT_BATTERY[a], EVENT_BATTERY[b]
            if any(
                pstep(pstep(s, e1), e2) != pstep(pstep(s, e2), e1)
                for s in states
            ):
                non_commuting += 1
            else:
                commuting += 1

    assert commuting + non_commuting == n_pairs
    assert (commuting, non_commuting) == (91, 62)

    rep = commutation_report()
    assert rep["battery_events"] == k
    assert rep["battery_states"] == len(states)  # same battery, independently
    assert rep["unordered_pairs"] == n_pairs
    assert len(rep["commuting_pairs"]) == commuting
    assert len(rep["non_commuting_pairs"]) == non_commuting


def test_every_reported_witness_is_the_smallest_distinguishing_state() -> None:
    """For each non-commuting pair the report names a witness of minimum
    state size; recompute that minimum by a full scan and require equality.
    For each commuting pair, require that no battery state distinguishes the
    two orders at all."""
    states = list(comm_states())
    k = len(EVENT_BATTERY)

    independent_min: dict[tuple[str, str], int] = {}
    commuting_keys: set[tuple[str, str]] = set()
    for a in range(k):
        for b in range(a + 1, k):
            e1, e2 = EVENT_BATTERY[a], EVENT_BATTERY[b]
            distinguishers = [
                s
                for s in states
                if pstep(pstep(s, e1), e2) != pstep(pstep(s, e2), e1)
            ]
            key = _pair_key(e1, e2)
            if distinguishers:
                independent_min[key] = min(state_size(s) for s in distinguishers)
            else:
                commuting_keys.add(key)

    rep = commutation_report()

    reported_non_commuting: set[tuple[str, str]] = set()
    for entry in rep["non_commuting_pairs"]:
        key = (
            json.dumps(entry["left"], sort_keys=True),
            json.dumps(entry["right"], sort_keys=True),
        )
        key = key if key[0] <= key[1] else (key[1], key[0])
        reported_non_commuting.add(key)
        assert key in independent_min, key
        assert entry["witness_size"] == independent_min[key]

    # the two partitions agree as sets, not merely in size
    assert reported_non_commuting == set(independent_min)
    for entry in rep["commuting_pairs"]:
        left, right = entry
        key = (
            json.dumps(left, sort_keys=True),
            json.dumps(right, sort_keys=True),
        )
        key = key if key[0] <= key[1] else (key[1], key[0])
        assert key in commuting_keys, key
