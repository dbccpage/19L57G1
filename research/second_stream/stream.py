"""Rung one of the second derivation: the stream as a response.

This module is the rung's library.  It answers nothing by itself; it
supplies the declared candidate space at three items, the two members of
the declared validity class, the declared budgets and their terminals, the
two availability censuses, and the reconstructed tree loop.  The runner,
the tests and the manifest live in other files and are owned elsewhere.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel
  (``code/derivation``) and on the sibling trees
  ``research/identification_dual`` and
  ``research/two_sided_commitment``.  All three are consumed READ-ONLY by
  import through ``sys.path``; no line of their source is transcribed.
* THE THREE-ITEM CANDIDATE SPACE IS AN ADMITTED PRIMITIVE OF THIS RUNG.
  The sealed ``iter_full_deltas`` is declared only to zero, one and two
  items and raises above that, and the sealed ``min_responses`` refuses
  beyond two items.  The space at three items is therefore declared here
  and must never be called the sealed candidate space at three items.  Its
  warrant is ``iter_superset_deltas``, an independently written wider
  construction one coordinate wider in each direction, and the certificates
  the test module builds on it.
* THE DEFERRAL BELOW THREE ITEMS IS NOT A DECLARATION.  At zero, one and
  two items ``iter_k_item_deltas`` yields from the sealed unpruned
  ``iter_full_deltas`` and nothing else, so nothing is declared there and no
  sealed pruning lemma is inherited.  ``iter_cost2_deltas`` -- the sealed
  PRUNED path, proved for a separation demand -- is never called at any
  cost.
* THE ADMISSION PREFILTER (``admissible_shape``) IS AN EXACT RESTATEMENT OF
  THE SEALED ADMISSION CONDITIONS, NOT A PRUNING LEMMA.  See its docstring
  for the argument and the test module for the set-equality certificate.
* THE NO-OP FILTER AND THE ORDERING ARE DECLARED BY THIS RUNG
  (``has_noop_item``, ``delta_order_key``).  The sibling's helpers of the
  same effect carry leading underscores and are not consumed.  Agreement
  with the public ``two_sided.min_responses`` at two items is the
  certificate.
* VALIDITY MEMBER ONE (``response_valid``) IS THE INHERITED NO-REGRESS
  RULE, re-exported from ``two_sided`` and never reimplemented.  Member two
  (``strict_response_valid``) is declared by this rung and additionally
  requires every committed pair involving a datum the response itself
  introduces to be honoured afterwards, whether the other member is a
  previously held datum or another datum the same response introduces.
* ``Judge`` IS A RESTRUCTURING, NOT A THIRD MEMBER.  It computes the
  augmented profile tuple once per candidate instead of once per honoured
  pair.  Its agreement with the imported definitions is certified by test,
  not asserted here.
* THE BUDGETS ARE DECLARED BOUNDS OF THIS RUNG, each with its own terminal
  naming the tree, the node and the demanded pair at which it fired.  A node
  whose gathering is cut short attaches nothing.
* THE ENUMERATION MEMO IS A CACHE, NEVER A LEMMA.  It answers a repeated
  enumeration from the record of the one before it exactly when the indexed
  state, the commitment and the demanded pair agree.
* The growth data bound governs growth alone and does not bind a response;
  a response admitting data beyond it is recorded with the count it reaches.

Public API
----------

Declared bounds and names::

    BOUNDS_TWO, BOUNDS_THREE, MAX_ROUNDS, GUARD, MAX_DATA, MEASURES
    MAX_ENUMERATIONS_PER_RUN, MAX_CANDIDATES_PER_ENUMERATION
    MAX_VALID_PER_TARGET, MAX_CLASSES_PER_NODE
    TERMINAL_ENUMERATION_BUDGET, TERMINAL_CANDIDATE_BUDGET
    TERMINAL_RESPONSE_BUDGET, TERMINAL_CLASS_BUDGET, TERMINAL_ISO_BUDGET
    RULE_NO_REGRESS, RULE_STRICT_NO_REGRESS, VALIDITY_RULES

Enumeration::

    universe_items(base, cost, bounds) -> list[Item]
    admissible_shape(base, delta) -> bool
    iter_k_item_deltas(base, cost, bounds) -> Iterator[Delta]
    iter_k_item_deltas_applied(base, cost, bounds) -> Iterator[tuple[Delta, Regime]]
    iter_superset_deltas(base, cost, bounds) -> Iterator[Delta]
    candidate_count(base, cost, bounds) -> int
    multiset_count(n, k) -> int
    has_noop_item(base, delta) -> bool
    delta_order_key(delta) -> tuple[tuple[int, int, Args], ...]

Validity::

    response_valid(s, target, delta) -> bool          # V1, imported
    strict_response_valid(s, target, delta) -> bool   # V2, declared here
    validity_named(name) -> ValidityRule
    Judge(s, target, rule).accepts(delta, after) -> bool

Selection, budgets, memo, counters::

    Minima3(measure, cost, deltas, valid_at_cost, rule, item_count)
    BudgetExceeded(terminal, detail)
    Counters()
    EnumerationMemo()
    min_responses_three(s, target, measure, bounds, rule, counters, memo,
                        state_tag) -> Optional[Minima3]

Census::

    Availability(item_bound, least_cost, generated, offered, examined, valid)
    fresh_datum_space(base, cost, bounds) -> tuple[int, list[tuple[Delta, Regime]]]
    fresh_datum_availability(s, target, item_bound, rule, counters) -> Availability

Tree::

    STree(tree, counters, truncations, census_two, census_three,
          enumerations, over_growth_bound)
    build_stream_tree(reading, commitment, measure, bounds, rule, max_rounds,
                      guard, max_data, census, counters, memo) -> STree

Rectangle A::

    RefusalSituation(reading, commitment, measure, node, kind, pair, state)
    refusal_states(bounds) -> list[RefusalSituation]
    situation_tag(sit) -> SituationTag
    distinct_situations(sits) -> list[tuple[SituationTag, list[RefusalSituation]]]

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
from collections import deque
from dataclasses import dataclass, field
from itertools import combinations_with_replacement, product
from typing import Callable, Iterator, Optional

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (
    str(REPO / "code"),
    str(REPO / "research" / "identification_dual"),
    str(REPO / "research" / "two_sided_commitment"),
):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    Item,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    apply_delta,
    canonical_delta,
    delta_events,
    item_key,
    iter_full_deltas,
    mu2,
)
from derivation.engine import READINGS, Reading, delta_label  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmissionError,
    AdmitDatum,
    Args,
    Pair,
    Regime,
    Supply,
)
from derivation.observe import Context, profiles  # noqa: E402
from two_sided import (  # noqa: E402
    APART,
    COMMITMENTS,
    SAME,
    Answer,
    Commitment,
    TEdge,
    TNode,
    TSEvent,
    TState,
    TStateKey,
    TTree,
    certify,
    closure_targets,
    commitment_named,
    demands,
    diagnostics,
    genesis_history,
    has_fresh_datum,
    honoured,
    honoured_pairs,
    key_of,
    response_valid,
    sealed_readings,
    ts_replay,
)

# ---------------------------------------------------------------------------
# Declared bounds.  Every value except the item bound is held at the value
# the sibling tree declared; the item bound is the one dial this rung moves.
# ---------------------------------------------------------------------------

BOUNDS_TWO = Bounds(max_items=2, max_arity=2)
BOUNDS_THREE = Bounds(max_items=3, max_arity=2)
MAX_ROUNDS = 15
GUARD = 250
MAX_DATA = 5
MEASURES: tuple[str, ...] = ("mu1", "mu2")

# The declared budgets of the frozen question, each with its own terminal.
MAX_ENUMERATIONS_PER_RUN = 40
MAX_CANDIDATES_PER_ENUMERATION = 1_000_000
MAX_VALID_PER_TARGET = 2000
MAX_CLASSES_PER_NODE = 200

TERMINAL_ENUMERATION_BUDGET = "terminal_enumeration_budget"
TERMINAL_CANDIDATE_BUDGET = "terminal_candidate_budget"
TERMINAL_RESPONSE_BUDGET = "terminal_response_budget"
TERMINAL_CLASS_BUDGET = "terminal_class_budget"
TERMINAL_ISO_BUDGET = "terminal_iso_budget"

BUDGET_TERMINALS: tuple[str, ...] = (
    TERMINAL_ENUMERATION_BUDGET,
    TERMINAL_CANDIDATE_BUDGET,
    TERMINAL_RESPONSE_BUDGET,
    TERMINAL_CLASS_BUDGET,
)

RULE_NO_REGRESS = "no_regress"
RULE_STRICT_NO_REGRESS = "strict_no_regress"

ValidityRule = Callable[[TState, tuple[str, Pair], Delta], bool]


# ---------------------------------------------------------------------------
# The candidate space
# ---------------------------------------------------------------------------


def universe_items(base: Regime, cost: int, bounds: Bounds) -> list[Item]:
    """Every item a delta of exactly ``cost`` items may offer over ``base``.

    Why the two widened values are the right ones.  The sealed item order is
    data, forms, rules, instances, and ``apply_delta`` replays a delta in
    that order, so a rule item or an instance item may name a form and a
    datum introduced by the SAME delta.  A delta of ``k`` items that
    contains at least one such referencing item has at most ``k - 1``
    remaining items, hence offers at most ``k - 1`` new forms and at most
    ``k - 1`` fresh data.  The offerable form indices are therefore
    ``range(len(base.forms) + (k - 1))`` and the offerable instance
    arguments ``range(base.n_data() + (k - 1))``.

    At ``k == 2`` those are ``len(base.forms) + 1`` and ``range(n0 + 1)``,
    which is exactly what the sealed cost-two universe uses; they are TWO-
    ITEM CONSTANTS, and carrying them unchanged to three items would drop
    every three-item delta carrying two new forms or two fresh data.  At
    ``k == 3`` they widen to ``len(base.forms) + 2`` and ``range(n0 + 2)``.
    The bound is pinned rather than restated: ``iter_superset_deltas`` is one
    coordinate wider in each direction and the test module asserts set
    equality with it.
    """

    if cost < 1:
        raise ValueError("a universe is offered only for a positive item count")
    n0 = base.n_data()
    f0 = len(base.forms)
    universe: list[Item] = [NewDatum()]
    for arity in range(1, bounds.max_arity + 1):
        universe.append(NewForm(arity))
    max_form = f0 + (cost - 1)
    max_arity_any = max([bounds.max_arity] + list(base.forms))
    for f in range(max_form):
        universe.append(NewRuleAll(f))
        for arity in range(1, max_arity_any + 1):
            for args in product(range(n0 + (cost - 1)), repeat=arity):
                universe.append(NewInst(f, tuple(args)))
    return universe


def admissible_shape(base: Regime, delta: Delta) -> bool:
    """Whether ``apply_delta(base, delta)`` succeeds, decided arithmetically.

    This is an EXACT RESTATEMENT of the sealed admission conditions, not a
    pruning lemma, and it must never be described as one.  ``delta_events``
    replays a delta in the sealed item order, so when a rule or instance
    item is applied every datum and every form of the same delta is already
    admitted.  Reading ``model.step``: ``AdmitDatum`` never raises;
    ``AdmitForm`` raises only for an arity below one, which no item in a
    universe of arity at least one carries; ``AdmitRuleAll`` raises exactly
    when its form index is out of range; ``AdmitInst`` raises exactly when
    its form index is out of range, when its argument count differs from
    that form's arity, or when an argument is out of range.  Those are the
    conditions tested below, over the form table and datum count the delta
    itself produces, so the test accepts a delta exactly when application
    accepts it.  Certified by set equality with unfiltered generate-and-apply
    in the test module.
    """

    n_forms = len(base.forms)
    n_data = base.n_data()
    arities: list[int] = list(base.forms)
    for it in delta:
        if isinstance(it, NewDatum):
            n_data += 1
        elif isinstance(it, NewForm):
            if it.arity < 1:
                return False
            arities.append(it.arity)
            n_forms += 1
    for it in delta:
        if isinstance(it, NewRuleAll):
            if not 0 <= it.form < n_forms:
                return False
        elif isinstance(it, NewInst):
            if not 0 <= it.form < n_forms:
                return False
            if len(it.args) != arities[it.form]:
                return False
            for a in it.args:
                if not 0 <= a < n_data:
                    return False
    return True


def iter_k_item_deltas_applied(
    base: Regime, cost: int, bounds: Bounds
) -> Iterator[tuple[Delta, Regime]]:
    """``iter_k_item_deltas``, each delta paired with its augmented regime.

    The augmented regime is wanted by every caller that then judges the
    delta, so it is produced once rather than twice.
    """

    if cost <= 2:
        for delta in iter_full_deltas(base, cost, bounds):
            yield delta, apply_delta(base, delta)
        return
    universe = universe_items(base, cost, bounds)
    seen: set[Delta] = set()
    for combo in combinations_with_replacement(universe, cost):
        delta = canonical_delta(combo)
        if not admissible_shape(base, delta):
            continue
        if delta in seen:  # pragma: no cover - unreachable, and pinned as such
            # ``universe_items`` returns no item twice, so distinct multisets
            # over it canonicalize to distinct deltas and this guard never
            # fires.  It is kept because the invariant is the generator's and
            # not this walk's, and excluded from coverage rather than left as
            # an untaken branch:
            # ``test_the_declared_universe_repeats_no_item`` is what makes the
            # exclusion honest.  The WIDER construction does need its own
            # guard -- it builds multisets a different way and that branch is
            # taken.
            continue
        try:
            after = apply_delta(base, delta)
        except AdmissionError:
            continue
        seen.add(delta)
        yield delta, after


def multiset_count(n: int, k: int) -> int:
    """The number of size-``k`` multisets over ``n`` distinct items."""

    if k == 0:
        return 1
    if n == 0:
        return 0
    total = 1
    for i in range(k):
        total = total * (n + i) // (i + 1)
    return total


def candidate_count(base: Regime, cost: int, bounds: Bounds) -> int:
    """How many candidates one enumeration at ``cost`` items examines.

    A CANDIDATE EXAMINED is one multiset over the declared universe, counted
    whether the sealed admission conditions then accept it or reject it: the
    rejected ones were examined too, and they are what the cost of an
    enumeration is mostly spent on.  The count is a function of the universe
    size alone, so the declared candidate budget can be answered BEFORE the
    enumeration rather than part way through it.
    """

    if cost <= 0:
        return 1
    return multiset_count(len(universe_items(base, cost, bounds)), cost)


def iter_k_item_deltas(base: Regime, cost: int, bounds: Bounds) -> Iterator[Delta]:
    """Every well-formed delta of exactly ``cost`` items over ``base``.

    Below three items this DEFERS to the sealed unpruned ``iter_full_deltas``
    and declares nothing.  At three items it generates over the same four
    item kinds under the sealed admission conditions alone, using no sealed
    pruning lemma: the sealed pruned path ``iter_cost2_deltas`` was proved
    for a separation demand and is never called here at any cost.

    Well-formedness is decided by APPLICATION, exactly as the seal decides
    it; ``admissible_shape`` only removes candidates application would
    reject.  ``AdmissionError`` is caught specifically -- it subclasses
    ``ValueError``, so a broad catch would swallow the seal's deliberate
    cost guard.
    """

    for delta, _after in iter_k_item_deltas_applied(base, cost, bounds):
        yield delta


def _wide_multisets(universe: list[Item], k: int) -> Iterator[tuple[Item, ...]]:
    """Every size-``k`` multiset over ``universe``, by index recursion.

    Written as its own recursion rather than through
    ``combinations_with_replacement`` so the cross-check shares no
    generation step with the construction it certifies.
    """

    if k == 0:
        yield ()
        return
    stack: list[tuple[int, tuple[Item, ...]]] = [(0, ())]
    while stack:
        start, acc = stack.pop()
        if len(acc) == k:
            yield acc
            continue
        for idx in range(len(universe) - 1, start - 1, -1):
            stack.append((idx, acc + (universe[idx],)))


def iter_superset_deltas(base: Regime, cost: int, bounds: Bounds) -> Iterator[Delta]:
    """An independently written wider construction, used only as a
    cross-check and never in a run.

    It offers form indices over ``range(len(base.forms) + cost)`` and
    instance arguments over ``range(base.n_data() + cost)`` -- one wider in
    each coordinate than ``universe_items`` -- takes every size-``cost``
    multiset over that wider universe by its own recursion, and filters by
    application alone.  Set equality with ``iter_k_item_deltas`` therefore
    PINS the ``cost - 1`` bound argued in ``universe_items`` rather than
    restating it.

    At exactly one item the two differ by a known closed form: this
    construction also carries ``{(NewRuleAll(f),) for f in base.rules}``,
    because ``AdmitRuleAll`` on an already-ruled form is idempotent rather
    than raising, while the sealed ``iter_cost1_items`` -- which
    ``iter_k_item_deltas`` defers to at that count -- emits rule items only
    for forms not already ruled.
    """

    if cost == 0:
        yield ()
        return
    n0 = base.n_data()
    f0 = len(base.forms)
    max_arity_any = max([bounds.max_arity] + list(base.forms))
    wide: list[Item] = [NewDatum()]
    for arity in range(1, bounds.max_arity + 1):
        wide.append(NewForm(arity))
    for g in range(f0 + cost):
        wide.append(NewRuleAll(g))
        for arity in range(1, max_arity_any + 1):
            for args in product(range(n0 + cost), repeat=arity):
                wide.append(NewInst(g, tuple(args)))
    emitted: set[Delta] = set()
    for combo in _wide_multisets(wide, cost):
        delta = canonical_delta(combo)
        if delta in emitted:
            continue
        try:
            apply_delta(base, delta)
        except AdmissionError:
            continue
        emitted.add(delta)
        yield delta


def has_noop_item(base: Regime, delta: Delta) -> bool:
    """This rung's declared no-op filter: a uniform-rule item on a form that
    already carries the rule changes no profile, so the delta is a longer
    presentation of a shorter one.

    Declared here in the rung's own words rather than consumed: the
    sibling's helper of the same effect carries a leading underscore.
    Agreement is certified by ``two_sided.min_responses`` at two items.
    """

    return any(isinstance(it, NewRuleAll) and it.form in base.rules for it in delta)


def delta_order_key(delta: Delta) -> tuple[tuple[int, int, Args], ...]:
    """This rung's declared ordering on deltas: the public
    ``candidates.item_key`` applied per item, in the sealed item order.

    Stated rather than left to be found: this reproduces the sealed
    ``candidates._delta_key``, which is private and is not consumed.
    """

    return tuple(item_key(it) for it in delta)


# ---------------------------------------------------------------------------
# The declared validity class
# ---------------------------------------------------------------------------


def strict_response_valid(s: TState, target: tuple[str, Pair], delta: Delta) -> bool:
    """Validity member two, declared by this rung.

    Member one (``response_valid``, imported unchanged) plus: every
    committed pair involving a datum THE RESPONSE ITSELF INTRODUCES is
    honoured after the response, whether the other member is a previously
    held datum or another datum the same response introduces.  The
    fresh-with-fresh case exists only at three items and is exactly where a
    ``(NewDatum, NewDatum, NewInst)`` delta under an all-apart stake
    separates this member from the inherited one: two bare fresh data carry
    equal profiles.

    Built only from the public ``two_sided.honoured`` and
    ``two_sided.commitment_named``; it introduces no grammar.  It adds one
    conjunct to member one, so its valid set is contained in member one's at
    every state, target and delta.
    """

    if not response_valid(s, target, delta):
        return False
    after = apply_delta(s.regime, delta)
    c = commitment_named(s.commitment)
    for k in range(s.regime.n_data(), after.n_data()):
        for i in range(k):
            if not honoured(after, c.label(i, k), (i, k)):
                return False
    return True


VALIDITY_RULES: tuple[tuple[str, ValidityRule], ...] = (
    (RULE_NO_REGRESS, response_valid),
    (RULE_STRICT_NO_REGRESS, strict_response_valid),
)


def validity_named(name: str) -> ValidityRule:
    for rule_name, rule in VALIDITY_RULES:
        if rule_name == name:
            return rule
    raise KeyError(name)


def _pair_ok(
    profs: tuple[frozenset[Context], ...], label: str, i: int, j: int
) -> bool:
    if label == APART:
        return profs[i] != profs[j]
    if label == SAME:
        return profs[i] == profs[j]
    return True


class Judge:
    """One state, one demanded pair, one validity member, many candidates.

    A restructuring and NOT a third member of the class: the imported
    definitions recompute the augmented profile tuple once per honoured
    pair, because ``two_sided.honoured`` calls ``profiles`` on every call,
    and this computes it once per candidate.  ``_pair_ok`` decides on that
    one tuple exactly what ``two_sided.honoured`` decides on its own.
    Agreement with the member it names is certified by test over the whole
    zero-, one- and two-item space, not asserted here.
    """

    def __init__(self, s: TState, target: tuple[str, Pair], rule: str) -> None:
        if rule not in (RULE_NO_REGRESS, RULE_STRICT_NO_REGRESS):
            raise KeyError(rule)
        self.rule = rule
        self.state = s
        self.target = target
        self.n0 = s.regime.n_data()
        self.commitment = commitment_named(s.commitment)
        self.target_label = target[0]
        self.target_pair = target[1]
        self.before: tuple[tuple[int, int, str], ...] = tuple(
            (i, j, self.commitment.label(i, j)) for (i, j) in sorted(honoured_pairs(s))
        )

    def accepts(self, delta: Delta, after: Regime) -> bool:
        profs = profiles(after)
        if not _pair_ok(profs, self.target_label, self.target_pair[0], self.target_pair[1]):
            return False
        for (i, j, label) in self.before:
            if not _pair_ok(profs, label, i, j):
                return False
        if self.rule == RULE_STRICT_NO_REGRESS:
            for k in range(self.n0, after.n_data()):
                for i in range(k):
                    if not _pair_ok(profs, self.commitment.label(i, k), i, k):
                        return False
        return True


# ---------------------------------------------------------------------------
# Budgets, counters, memo
# ---------------------------------------------------------------------------


class BudgetExceeded(Exception):
    """A declared budget fired.  The tree loop names the tree, the node and
    the demanded pair; the detail carried here names the counts."""

    def __init__(self, terminal: str, detail: dict[str, object]) -> None:
        super().__init__(terminal)
        self.terminal = terminal
        self.detail = detail


@dataclass
class Counters:
    """Deterministic counters.  No count is initialised to an answer and
    every count has a companion proving the procedure ran."""

    nodes_visited: int = 0
    nodes_censused: int = 0
    nodes_above_growth_data_bound: int = 0
    three_item_enumerations_performed: int = 0
    candidate_multisets_projected: int = 0
    deltas_offered: int = 0
    deltas_examined: int = 0
    enumeration_memo_hits: int = 0
    fresh_datum_candidates_generated: int = 0
    fresh_datum_candidates_offered: int = 0
    fresh_datum_candidates_examined: int = 0
    fresh_datum_candidates_judged: int = 0
    fresh_datum_candidates_skipped_as_noop: int = 0
    fresh_datum_candidates_valid: int = 0
    census_two_rows: int = 0
    census_three_rows: int = 0

    def as_json(self) -> dict[str, int]:
        return {
            "candidate_multisets_projected": self.candidate_multisets_projected,
            "census_three_rows": self.census_three_rows,
            "census_two_rows": self.census_two_rows,
            "deltas_examined": self.deltas_examined,
            "deltas_offered": self.deltas_offered,
            "enumeration_memo_hits": self.enumeration_memo_hits,
            "fresh_datum_candidates_examined": self.fresh_datum_candidates_examined,
            "fresh_datum_candidates_judged": self.fresh_datum_candidates_judged,
            "fresh_datum_candidates_generated": self.fresh_datum_candidates_generated,
            "fresh_datum_candidates_offered": self.fresh_datum_candidates_offered,
            "fresh_datum_candidates_skipped_as_noop": (
                self.fresh_datum_candidates_skipped_as_noop
            ),
            "fresh_datum_candidates_valid": self.fresh_datum_candidates_valid,
            "nodes_above_growth_data_bound": self.nodes_above_growth_data_bound,
            "nodes_censused": self.nodes_censused,
            "nodes_visited": self.nodes_visited,
            "three_item_enumerations_performed": self.three_item_enumerations_performed,
        }


MemoKey = tuple[object, str, str, Pair, str, str, int, int]


class EnumerationMemo:
    """A repeated enumeration answered from the record of the one before it.

    The key is the indexed state (the third component of the public
    ``two_sided.key_of``, which forgets presentation tokens), the commitment
    name and the demanded pair, together with the measure, the validity
    member and the two bounds.  Those last four are constant within one run,
    so the memo answers exactly the repeat the frozen question declares and
    never more.  Only a call that actually reached three items is recorded:
    below that the work is cheap and the record would be noise.

    Classification: metatheory apparatus.  It is a cache and never a lemma.
    """

    def __init__(self) -> None:
        self._store: dict[MemoKey, Optional[Minima3]] = {}
        self.hits = 0
        self.stores = 0

    @staticmethod
    def key(
        state_tag: object,
        s: TState,
        target: tuple[str, Pair],
        measure: str,
        rule: str,
        bounds: Bounds,
    ) -> MemoKey:
        return (
            state_tag,
            s.commitment,
            target[0],
            target[1],
            measure,
            rule,
            bounds.max_items,
            bounds.max_arity,
        )

    def get(self, key: MemoKey) -> tuple[bool, Optional[Minima3]]:
        if key in self._store:
            self.hits += 1
            return True, self._store[key]
        return False, None

    def put(self, key: MemoKey, value: Optional[Minima3]) -> None:
        self._store[key] = value
        self.stores += 1

    def __len__(self) -> int:
        return len(self._store)


# ---------------------------------------------------------------------------
# Minimum selection
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Minima3:
    """Minimum responses at the first item count with a non-empty valid set.

    ``cost`` carries the sibling's shape: ``(item_count, -1)`` under ``mu1``,
    where ``-1`` is a sentinel and not an arity, and the ``mu2`` value under
    ``mu2``.  ``rule`` names the validity member that produced the row.
    """

    measure: str
    cost: tuple[int, int]
    deltas: tuple[Delta, ...]
    valid_at_cost: int
    rule: str
    item_count: int


def min_responses_three(
    s: TState,
    target: tuple[str, Pair],
    measure: str,
    bounds: Bounds,
    rule: str = RULE_NO_REGRESS,
    counters: Optional[Counters] = None,
    memo: Optional[EnumerationMemo] = None,
    state_tag: Optional[object] = None,
) -> Optional[Minima3]:
    """Minimum valid responses within the declared bounds, or ``None``.

    The selection semantics are the sibling's, declared here rather than
    copied: iterate by item count from zero; at each count skip the declared
    no-op deltas and duplicates; collect the deltas the named validity
    member accepts; return at the FIRST count with a non-empty valid set;
    under ``mu1`` return every valid delta at that count, under ``mu2`` only
    those attaining the least ``mu2`` value there.  Every tie is retained, or
    the response budget fires and nothing is retained.

    Because the return is at the first non-empty count, an enumeration at
    three items happens ONLY where every response of fewer items fails.
    Setting ``max_items`` to three and observing no error is therefore not
    evidence that anything was enumerated at three items; the counter
    ``three_item_enumerations_performed`` is what says so.
    """

    if measure not in MEASURES:
        raise ValueError(f"unknown measure: {measure}")
    cnt = counters if counters is not None else Counters()
    memo_key: Optional[MemoKey] = None
    if memo is not None and bounds.max_items >= 3:
        tag = state_tag if state_tag is not None else key_of(s)[2]
        memo_key = EnumerationMemo.key(tag, s, target, measure, rule, bounds)
        hit, remembered = memo.get(memo_key)
        if hit:
            cnt.enumeration_memo_hits += 1
            return remembered
    judge = Judge(s, target, rule)
    reached_three = False
    result: Optional[Minima3] = None
    for cost in range(0, bounds.max_items + 1):
        if cost >= 3:
            reached_three = True
            cnt.three_item_enumerations_performed += 1
            if cnt.three_item_enumerations_performed > MAX_ENUMERATIONS_PER_RUN:
                raise BudgetExceeded(
                    TERMINAL_ENUMERATION_BUDGET,
                    {
                        "enumerations_performed": cnt.three_item_enumerations_performed,
                        "bound": MAX_ENUMERATIONS_PER_RUN,
                        "item_count": cost,
                    },
                )
            projected = candidate_count(s.regime, cost, bounds)
            if projected > MAX_CANDIDATES_PER_ENUMERATION:
                raise BudgetExceeded(
                    TERMINAL_CANDIDATE_BUDGET,
                    {
                        "candidate_multisets_projected": projected,
                        "bound": MAX_CANDIDATES_PER_ENUMERATION,
                        "item_count": cost,
                    },
                )
            cnt.candidate_multisets_projected += projected
        valid: list[Delta] = []
        for delta, after in iter_k_item_deltas_applied(s.regime, cost, bounds):
            cnt.deltas_offered += 1
            if has_noop_item(s.regime, delta):
                continue
            cnt.deltas_examined += 1
            if judge.accepts(delta, after):
                valid.append(delta)
                if len(valid) > MAX_VALID_PER_TARGET:
                    raise BudgetExceeded(
                        TERMINAL_RESPONSE_BUDGET,
                        {
                            "valid_gathered": len(valid),
                            "bound": MAX_VALID_PER_TARGET,
                            "item_count": cost,
                        },
                    )
        if not valid:
            continue
        if measure == "mu1":
            result = Minima3(
                "mu1",
                (cost, -1),
                tuple(sorted(valid, key=delta_order_key)),
                len(valid),
                rule,
                cost,
            )
        else:
            best = min(mu2(d) for d in valid)
            chosen = tuple(
                sorted((d for d in valid if mu2(d) == best), key=delta_order_key)
            )
            result = Minima3("mu2", best, chosen, len(valid), rule, cost)
        break
    if memo is not None and memo_key is not None and reached_three:
        memo.put(memo_key, result)
    return result


# ---------------------------------------------------------------------------
# The availability census
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Availability:
    """Whether a valid response carrying a fresh datum exists within an item
    bound, recorded independently of the item count at which the minimum was
    found.

    ``generated`` counts the multisets the generator produced; ``offered``
    counts those the sealed admission conditions accept; ``examined`` counts
    those the census actually looked at; ``judged`` counts those handed to
    the validity member, which is ``offered`` less the declared no-op
    filter's skips; ``skipped_as_noop`` reports that difference directly.

    ``examined`` is INCREMENTED in the loop, not assigned from ``offered``.
    An earlier version wrote ``examined = offered`` and justified it with a
    sentence that was false -- it said every offered candidate is judged,
    while the no-op filter drops some before the judge sees them.  The
    counts now say three different things and can diverge, which is what
    makes a zero here a counted zero rather than a literal.
    """

    item_bound: int
    least_cost: int
    generated: int
    offered: int
    examined: int
    judged: int
    skipped_as_noop: int
    valid: int

    def exists(self) -> bool:
        return self.least_cost >= 0

    def as_json(self) -> dict[str, object]:
        return {
            "examined": self.examined,
            "exists": self.exists(),
            "generated": self.generated,
            "item_bound": self.item_bound,
            "judged": self.judged,
            "least_cost": self.least_cost,
            "offered": self.offered,
            "skipped_as_noop": self.skipped_as_noop,
            "valid": self.valid,
        }


def fresh_datum_space(
    base: Regime, cost: int, bounds: Bounds
) -> tuple[int, list[tuple[Delta, Regime]]]:
    """``(generated, admissible)`` for the deltas of exactly ``cost`` items
    that carry at least one datum item, each admissible one paired with its
    augmented regime.

    This is the space ``iter_k_item_deltas`` describes, restricted to the
    deltas the census asks about.  The restriction is exact rather than a
    prune: a multiset over the universe with exactly ``d`` copies of
    ``NewDatum`` is the concatenation of those ``d`` copies with a multiset
    over the universe minus ``NewDatum``, and ``d`` runs from one to
    ``cost``, so every datum-bearing multiset is produced exactly once and
    nothing else is.

    SCOPE, stated because the frozen question's deferral clause does NOT
    describe this function.  ``PROMPT.md`` says the rung defers below three
    items to the sealed unpruned enumeration; ``iter_k_item_deltas`` does
    exactly that, and this construction does NOT -- it builds directly from
    ``universe_items`` at every item count, including one and two.  The
    deferral clause governs the CANDIDATE space of the selection; the census
    space is this rung's own declaration at every item count.  It is
    certified EQUAL as a set to the deferring generator's datum-bearing
    subset at costs zero to three, on every base of the declared
    cross-check family, by
    ``test_the_datum_bearing_subspace_is_a_restriction_and_not_a_prune``.
    An equality certified on that family is not an equality everywhere, and
    the family is the scope of the claim.
    """

    rest_universe = [
        it for it in universe_items(base, cost, bounds) if not isinstance(it, NewDatum)
    ]
    generated = 0
    out: list[tuple[Delta, Regime]] = []
    for d in range(1, cost + 1):
        head: tuple[Item, ...] = (NewDatum(),) * d
        for tail in combinations_with_replacement(rest_universe, cost - d):
            generated += 1
            delta = canonical_delta(head + tail)
            if not admissible_shape(base, delta):
                continue
            try:
                after = apply_delta(base, delta)
            except AdmissionError:
                continue
            out.append((delta, after))
    return generated, out


def fresh_datum_availability(
    s: TState,
    target: tuple[str, Pair],
    item_bound: int,
    rule: str = RULE_NO_REGRESS,
    counters: Optional[Counters] = None,
) -> Availability:
    """Record whether a valid response containing a fresh datum exists within
    ``item_bound`` items, for one state and one demanded pair.

    Every datum-bearing candidate up to the bound is looked at and every one
    that survives the declared no-op filter is judged; there is no early
    exit, so the census reports how many such responses are valid, not
    merely whether one is.  ``least_cost`` is the smallest item count at
    which one exists, or ``-1``.

    Four counts are maintained separately -- offered, examined, judged and
    the no-op skips -- so that an early exit introduced later would show as
    ``examined`` falling below ``offered`` instead of being invisible.
    """

    cnt = counters if counters is not None else Counters()
    judge = Judge(s, target, rule)
    bounds = Bounds(max_items=item_bound, max_arity=BOUNDS_THREE.max_arity)
    least = -1
    generated = 0
    offered = 0
    examined = 0
    judged = 0
    valid = 0
    for cost in range(1, item_bound + 1):
        made, space = fresh_datum_space(s.regime, cost, bounds)
        generated += made
        offered += len(space)
        for delta, after in space:
            examined += 1
            if has_noop_item(s.regime, delta):
                continue
            judged += 1
            if judge.accepts(delta, after):
                valid += 1
                if least < 0:
                    least = cost
    cnt.fresh_datum_candidates_generated += generated
    cnt.fresh_datum_candidates_offered += offered
    cnt.fresh_datum_candidates_examined += examined
    cnt.fresh_datum_candidates_judged += judged
    cnt.fresh_datum_candidates_skipped_as_noop += offered - judged
    cnt.fresh_datum_candidates_valid += valid
    return Availability(
        item_bound, least, generated, offered, examined, judged, offered - judged, valid
    )


# ---------------------------------------------------------------------------
# The tree
# ---------------------------------------------------------------------------


@dataclass
class STree:
    """The sibling's tree structure, kept as the sibling's own ``TTree`` so
    that its ``stats()`` is the sibling's code and not a restatement, plus
    the records this rung adds."""

    tree: TTree
    counters: Counters = field(default_factory=Counters)
    truncations: list[dict[str, object]] = field(default_factory=list)
    census_two: list[dict[str, object]] = field(default_factory=list)
    census_three: list[dict[str, object]] = field(default_factory=list)
    enumerations: list[dict[str, object]] = field(default_factory=list)
    over_growth_bound: list[dict[str, object]] = field(default_factory=list)

    @property
    def ident(self) -> str:
        return f"{self.tree.reading}/{self.tree.commitment}/{self.tree.measure}"

    def stats(self) -> dict[str, object]:
        return self.tree.stats()


def _grow_events(n: int) -> tuple[TSEvent, ...]:
    token = f"g{n}"
    return (Supply(token), AdmitDatum(token))


def build_stream_tree(
    reading: Reading,
    commitment: Commitment,
    measure: str,
    bounds: Bounds = BOUNDS_THREE,
    rule: str = RULE_NO_REGRESS,
    max_rounds: int = MAX_ROUNDS,
    guard: int = GUARD,
    max_data: int = MAX_DATA,
    census: bool = True,
    counters: Optional[Counters] = None,
    memo: Optional[EnumerationMemo] = None,
) -> STree:
    """The tree loop, reconstructed from the sibling's observable contract
    with this rung's enumerator injected.

    The status precedence is the sibling's, in the order its code has it:
    pop a node; compute the targets inside a handler for the bijection
    budget; then the round bound; then the pre-expansion node guard; then
    the empty-target branch, which grows or stops at the growth data bound;
    otherwise gather a minimum per target, breaking on the first target with
    no response; otherwise attach every retained class of every target.

    Two guards the sibling does not carry.  The bijection budget is raised
    inside the quotient key, which the sibling computes outside every
    handler, so its own terminal for it is unreachable; here every call site
    is wrapped and the terminal names the node.  And the four declared
    budgets are enforced with their four terminals: a node whose gathering is
    cut short attaches NOTHING, keeps no partially gathered minimum, and
    records how many targets were gathered and how many were not reached.
    """

    cnt = counters if counters is not None else Counters()
    tree = TTree(
        reading.name, commitment.name, measure, bounds, max_rounds, guard, max_data
    )
    out = STree(tree, cnt)
    history = genesis_history(reading, commitment)
    root_state = ts_replay(history)
    try:
        root_key = key_of(root_state)
    except RuntimeError as exc:
        out.truncations.append(
            _truncation(
                out, -1, None, TERMINAL_ISO_BUDGET,
                {"where": "root", "detail": str(exc)},
            )
        )
        return out
    root = TNode(0, history, root_state, 0, root_key)
    root.certified = certify(root.history, root.state)
    tree.nodes.append(root)
    key_map: dict[TStateKey, int] = {root.key: 0}
    queue: deque[int] = deque([0])
    while queue:
        nid = queue.popleft()
        node = tree.nodes[nid]
        cnt.nodes_visited += 1
        if node.state.regime.n_data() > max_data:
            cnt.nodes_above_growth_data_bound += 1
            out.over_growth_bound.append(
                {"node": nid, "data": node.state.regime.n_data(), "bound": max_data}
            )
        try:
            targets = closure_targets(node.state)
        except RuntimeError as exc:
            node.status = TERMINAL_ISO_BUDGET
            out.truncations.append(
                _truncation(out, nid, None, TERMINAL_ISO_BUDGET,
                            {"where": "targets", "detail": str(exc)})
            )
            continue
        if census:
            _census_two(out, nid, node, targets, rule, cnt)
        if node.depth >= max_rounds:
            node.status = "completed"
            continue
        if len(tree.nodes) > guard:
            node.status = "frontier_guard"
            continue
        if not targets:
            n = node.state.regime.n_data()
            if n >= max_data:
                node.status = "terminal_data_bound"
                continue
            grown = node.history + _grow_events(n)
            child_state = ts_replay(grown)
            info: dict[str, object] = {
                "demands_after_growth": len(demands(child_state)),
                "data_before": n,
            }
            if not _attach(out, key_map, queue, node, grown, "grow", "grow", (), 1, 1,
                           (0, 0), 1, info):
                continue
            node.status = "expanded"
            continue
        gathered: list[tuple[tuple[str, Pair], Minima3]] = []
        refused = False
        truncated = False
        for target in targets:
            enum_before = cnt.three_item_enumerations_performed
            try:
                mr = min_responses_three(
                    node.state, target, measure, bounds, rule, cnt, memo, node.key[2]
                )
            except BudgetExceeded as exc:
                out.truncations.append(
                    _truncation(
                        out, nid, target, exc.terminal,
                        dict(exc.detail)
                        | {
                            "targets_gathered": len(gathered),
                            "targets_not_reached": len(targets) - len(gathered) - 1,
                            "attached": 0,
                        },
                    )
                )
                node.status = exc.terminal
                truncated = True
                break
            except RuntimeError as exc:
                out.truncations.append(
                    _truncation(out, nid, target, TERMINAL_ISO_BUDGET,
                                {"where": "selection", "detail": str(exc)})
                )
                node.status = TERMINAL_ISO_BUDGET
                truncated = True
                break
            enum_after = cnt.three_item_enumerations_performed
            if enum_after > enum_before:
                out.enumerations.append(
                    {
                        "node": nid,
                        "kind": target[0],
                        "target": list(target[1]),
                        "data": node.state.regime.n_data(),
                        "forms": list(node.state.regime.forms),
                        "answered": mr is not None,
                        "item_count": -1 if mr is None else mr.item_count,
                        "projected_candidates": candidate_count(
                            node.state.regime, 3, bounds
                        ),
                        "valid_at_cost": 0 if mr is None else mr.valid_at_cost,
                    }
                )
                if census:
                    _census_three(out, nid, node, target, rule, cnt)
            if mr is None:
                tree.refusals.append(
                    {
                        "node": nid,
                        "kind": target[0],
                        "target": list(target[1]),
                        "data": node.state.regime.n_data(),
                        "open_demands": len(demands(node.state)),
                        "single_item_candidates": sum(
                            1 for _ in iter_full_deltas(node.state.regime, 1, bounds)
                        ),
                    }
                )
                refused = True
                break
            gathered.append((target, mr))
        if truncated:
            continue
        if refused:
            node.status = "terminal_no_response"
            continue
        per_target: list[
            tuple[tuple[str, Pair], Minima3, list[tuple[Delta, int]]]
        ] = []
        total_classes = 0
        quotient_truncated = False
        for target_index, (target, mr) in enumerate(gathered):
            try:
                classes = _quotient(node.state, mr)
            except RuntimeError as exc:
                out.truncations.append(
                    _truncation(
                        out,
                        nid,
                        target,
                        TERMINAL_ISO_BUDGET,
                        {"where": "quotient", "detail": str(exc), "attached": 0},
                    )
                )
                node.status = TERMINAL_ISO_BUDGET
                quotient_truncated = True
                break
            total_classes += len(classes)
            if total_classes > MAX_CLASSES_PER_NODE:
                out.truncations.append(
                    _truncation(
                        out,
                        nid,
                        target,
                        TERMINAL_CLASS_BUDGET,
                        {
                            "classes": total_classes,
                            "bound": MAX_CLASSES_PER_NODE,
                            "targets_gathered": target_index + 1,
                            "targets_not_reached": len(gathered) - target_index - 1,
                            "attached": 0,
                        },
                    )
                )
                node.status = TERMINAL_CLASS_BUDGET
                quotient_truncated = True
                break
            per_target.append((target, mr, classes))
        if quotient_truncated:
            continue
        prepared: list[
            tuple[
                tuple[str, Pair], Minima3, Delta, int, int, tuple[TSEvent, ...],
                tuple[int, int], dict[str, object], tuple[TState, TStateKey],
            ]
        ] = []
        attachment_failed = False
        for target, mr, classes in per_target:
            for rep, size in classes:
                history2 = (
                    node.history
                    + (Answer(target[0], target[1][0], target[1][1]),)
                    + tuple(delta_events(node.state.regime, rep))
                )
                cost = mr.cost if measure == "mu2" else (mr.cost[0], -1)
                info = diagnostics(node.state, target, rep)
                info["valid_at_cost"] = mr.valid_at_cost
                info["validity_rule"] = mr.rule
                info["item_count"] = mr.item_count
                try:
                    state_and_key = _prepare_attachment(history2)
                except RuntimeError as exc:
                    out.truncations.append(
                        _truncation(
                            out,
                            nid,
                            target,
                            TERMINAL_ISO_BUDGET,
                            {"where": "attach", "detail": str(exc), "attached": 0},
                        )
                    )
                    node.status = TERMINAL_ISO_BUDGET
                    attachment_failed = True
                    break
                prepared.append(
                    (
                        target,
                        mr,
                        rep,
                        size,
                        len(classes),
                        history2,
                        cost,
                        info,
                        state_and_key,
                    )
                )
            if attachment_failed:
                break
        if attachment_failed:
            continue
        for (
            target,
            mr,
            rep,
            size,
            tie_classes,
            history2,
            cost,
            info,
            state_and_key,
        ) in prepared:
            attached = _attach(
                out,
                key_map,
                queue,
                node,
                history2,
                f"{target[0]}{target[1]}",
                delta_label(node.state.regime, rep),
                rep,
                tie_classes,
                size,
                cost,
                len(targets),
                info,
                prepared=state_and_key,
            )
            if not attached:  # pragma: no cover - a prepared key cannot fail
                raise AssertionError("a prepared attachment unexpectedly failed")
        node.status = "expanded"
    return out


def _truncation(
    out: STree,
    node: int,
    target: Optional[tuple[str, Pair]],
    terminal: str,
    detail: dict[str, object],
) -> dict[str, object]:
    row: dict[str, object] = {
        "tree": out.ident,
        "node": node,
        "terminal": terminal,
        "kind": "" if target is None else target[0],
        "target": [] if target is None else list(target[1]),
    }
    row.update({str(k): v for k, v in sorted(detail.items())})
    return row


def _quotient(s: TState, mr: Minima3) -> list[tuple[Delta, int]]:
    """Retain one representative per state the sibling's repaired key merges.

    The key is the public ``two_sided.key_of``, which pairs the sibling's own
    state key with the exact indexed regime and the commitment name.  Its
    indexed component begins with the datum count, so a datum-bearing delta
    never shares a class with a delta carrying no datum item and is always a
    retained representative -- but two distinct datum-bearing deltas that
    produce the same regime DO merge, so no delta is said to land in a class
    of its own.  What follows, and no more, is that "no edge carries a datum
    item" and "no retained minimum carries a datum item" are one statement.
    """

    grouped: dict[TStateKey, list[Delta]] = {}
    for delta in mr.deltas:
        child = TState(apply_delta(s.regime, delta), s.commitment)
        grouped.setdefault(key_of(child), []).append(delta)
    return [(members[0], len(members)) for _key, members in sorted(grouped.items())]


def _prepare_attachment(history: tuple[TSEvent, ...]) -> tuple[TState, TStateKey]:
    """Replay and key one prospective child without mutating the tree."""

    state = ts_replay(history)
    return state, key_of(state)


def _attach(
    out: STree,
    key_map: dict[TStateKey, int],
    queue: "deque[int]",
    parent: TNode,
    history: tuple[TSEvent, ...],
    challenge: str,
    label: str,
    response: Delta,
    tie_classes: int,
    class_size: int,
    cost: tuple[int, int],
    target_count: int,
    info: dict[str, object],
    prepared: Optional[tuple[TState, TStateKey]] = None,
) -> bool:
    """Attach one child.  Returns False when the bijection budget fired, in
    which case nothing is attached and the parent carries the terminal."""

    tree = out.tree
    if prepared is None:
        try:
            state, key = _prepare_attachment(history)
        except RuntimeError as exc:
            out.truncations.append(
                _truncation(out, parent.node_id, None, TERMINAL_ISO_BUDGET,
                            {"where": "attach", "detail": str(exc)})
            )
            parent.status = TERMINAL_ISO_BUDGET
            return False
    else:
        state, key = prepared
    if key in key_map:
        child_id = key_map[key]
        kind = "merge"
        tree.nodes[child_id].merged_count += 1
    else:
        child_id = len(tree.nodes)
        kind = "creation"
        child = TNode(child_id, history, state, parent.depth + 1, key)
        child.certified = certify(child.history, child.state)
        child.grown_from = challenge == "grow"
        tree.nodes.append(child)
        key_map[key] = child_id
        queue.append(child_id)
    tree.edges.append(
        TEdge(
            parent.node_id, child_id, parent.depth + 1, challenge, label, response,
            tie_classes, class_size, cost, target_count, kind, info,
        )
    )
    return True


def _census_two(
    out: STree,
    nid: int,
    node: TNode,
    targets: tuple[tuple[str, Pair], ...],
    rule: str,
    cnt: Counters,
) -> None:
    """At every node reached, and independently of the item count at which
    the minimum was found, whether a valid response containing a fresh datum
    exists within a bound of two items."""

    cnt.nodes_censused += 1
    for target in targets:
        av = fresh_datum_availability(node.state, target, 2, rule, cnt)
        row: dict[str, object] = {
            "tree": out.ident,
            "node": nid,
            "kind": target[0],
            "target": list(target[1]),
            "data": node.state.regime.n_data(),
            "validity_rule": rule,
        }
        row.update({str(k): v for k, v in sorted(av.as_json().items())})
        out.census_two.append(row)
        cnt.census_two_rows += 1


def _census_three(
    out: STree,
    nid: int,
    node: TNode,
    target: tuple[str, Pair],
    rule: str,
    cnt: Counters,
) -> None:
    """At every state where a three-item enumeration is performed, the same
    within a bound of three items."""

    av = fresh_datum_availability(node.state, target, 3, rule, cnt)
    row: dict[str, object] = {
        "tree": out.ident,
        "node": nid,
        "kind": target[0],
        "target": list(target[1]),
        "data": node.state.regime.n_data(),
        "validity_rule": rule,
    }
    row.update({str(k): v for k, v in sorted(av.as_json().items())})
    out.census_three.append(row)
    cnt.census_three_rows += 1


# ---------------------------------------------------------------------------
# Rectangle A: the recorded two-item refusals, re-derived
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RefusalSituation:
    """One node at which the two-item bound answered no demanded pair."""

    reading: str
    commitment: str
    measure: str
    node: int
    kind: str
    pair: Pair
    state: TState

    def ident(self) -> str:
        return f"{self.reading}/{self.commitment}/{self.measure}"

    def as_json(self) -> dict[str, object]:
        return {
            "commitment": self.commitment,
            "data": self.state.regime.n_data(),
            "kind": self.kind,
            "measure": self.measure,
            "node": self.node,
            "reading": self.reading,
            "target": list(self.pair),
            "tree": self.ident(),
        }


SituationTag = tuple[object, str, str, Pair]


def situation_tag(sit: RefusalSituation) -> SituationTag:
    """Two refusals are the same situation exactly when the indexed regime
    component of the public ``two_sided.key_of``, the commitment name, the
    DEMAND KIND and the demanded pair all agree.  A refusal record counts a
    NODE, not a situation.

    Four components, and the fourth is the demand kind.  An earlier version
    of this sentence named three and the body returned four; assumption A5
    of the receipt named four throughout.  Nothing was scored differently --
    the recorded refusal population is of one kind, so the kind component is
    constant over it -- but the prose was the half that was wrong.
    """

    return (key_of(sit.state)[2], sit.commitment, sit.kind, sit.pair)


def distinct_situations(
    sits: list[RefusalSituation],
) -> list[tuple[SituationTag, list[RefusalSituation]]]:
    grouped: dict[SituationTag, list[RefusalSituation]] = {}
    order: list[SituationTag] = []
    for sit in sits:
        tag = situation_tag(sit)
        if tag not in grouped:
            grouped[tag] = []
            order.append(tag)
        grouped[tag].append(sit)
    return [(tag, grouped[tag]) for tag in order]


def refusal_states(
    bounds: Bounds = BOUNDS_TWO,
    rule: str = RULE_NO_REGRESS,
    census: bool = False,
) -> list[RefusalSituation]:
    """Re-derive the refusal population from the pinned sources rather than
    reading it out of a committed receipt.

    Run at the sibling's own item bound this returns the recorded two-item
    refusals, each carrying the state that produced it, so a three-item
    enumeration can be performed at exactly those states.
    """

    out: list[RefusalSituation] = []
    for reading in sealed_readings():
        for commitment in COMMITMENTS:
            for measure in MEASURES:
                tree = build_stream_tree(
                    reading, commitment, measure, bounds, rule, census=census
                )
                for rec in tree.tree.refusals:
                    nid = int(str(rec["node"]))
                    raw = rec["target"]
                    assert isinstance(raw, list)
                    pair: Pair = (int(str(raw[0])), int(str(raw[1])))
                    out.append(
                        RefusalSituation(
                            reading.name,
                            commitment.name,
                            measure,
                            nid,
                            str(rec["kind"]),
                            pair,
                            tree.tree.nodes[nid].state,
                        )
                    )
    return out


__all__ = [
    "APART",
    "BOUNDS_THREE",
    "BOUNDS_TWO",
    "BUDGET_TERMINALS",
    "Availability",
    "BudgetExceeded",
    "Counters",
    "EnumerationMemo",
    "GUARD",
    "Judge",
    "MAX_CANDIDATES_PER_ENUMERATION",
    "MAX_CLASSES_PER_NODE",
    "MAX_DATA",
    "MAX_ENUMERATIONS_PER_RUN",
    "MAX_ROUNDS",
    "MAX_VALID_PER_TARGET",
    "MEASURES",
    "Minima3",
    "READINGS",
    "RULE_NO_REGRESS",
    "RULE_STRICT_NO_REGRESS",
    "RefusalSituation",
    "SAME",
    "STree",
    "SituationTag",
    "TERMINAL_CANDIDATE_BUDGET",
    "TERMINAL_CLASS_BUDGET",
    "TERMINAL_ENUMERATION_BUDGET",
    "TERMINAL_ISO_BUDGET",
    "TERMINAL_RESPONSE_BUDGET",
    "VALIDITY_RULES",
    "ValidityRule",
    "admissible_shape",
    "build_stream_tree",
    "candidate_count",
    "delta_order_key",
    "distinct_situations",
    "fresh_datum_availability",
    "fresh_datum_space",
    "has_fresh_datum",
    "has_noop_item",
    "iter_k_item_deltas",
    "iter_k_item_deltas_applied",
    "iter_superset_deltas",
    "min_responses_three",
    "multiset_count",
    "refusal_states",
    "response_valid",
    "situation_tag",
    "strict_response_valid",
    "universe_items",
    "validity_named",
]
