"""Finite checking and finding ledger over a reconstructed response space.

Every count uses the cost frozen in PREDICTIONS.md.  Predicate evaluation,
state hashing, and canonical-key construction are deliberately outside that
declared count.  AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations, product
from typing import Iterator, TypeAlias

from description import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    AdmissionError,
    Event,
    Impose,
    Regime,
    regime_json,
    replay,
    step as apply_event,
)


Pair: TypeAlias = tuple[int, int]
Args: TypeAlias = tuple[int, ...]
Slot: TypeAlias = int | None
Context: TypeAlias = tuple[int, tuple[Slot, ...]]

TARGET: Pair = (0, 1)
MAX_ARITY = 1
MAX_ITEMS = 2


@dataclass(frozen=True)
class NewDatum:
    """One new datum item."""


@dataclass(frozen=True)
class NewForm:
    arity: int


@dataclass(frozen=True)
class NewInst:
    form: int
    args: Args


@dataclass(frozen=True)
class NewRuleAll:
    form: int


Item: TypeAlias = NewDatum | NewForm | NewInst | NewRuleAll
Delta: TypeAlias = tuple[Item, ...]
CanonKey: TypeAlias = tuple[
    int,
    tuple[int, ...],
    tuple[tuple[int, Args], ...],
    tuple[int, ...],
    tuple[Pair, ...],
]
MeasureValue: TypeAlias = int | tuple[int, int]


@dataclass(frozen=True)
class FinderResult:
    measure: str
    measure_value: MeasureValue
    checked: tuple[Delta, ...]
    winners: tuple[Delta, ...]
    finding_cost: int


@dataclass(frozen=True)
class ResponseEventRun:
    """Costed response execution, separate from the DR decoder surface."""

    endpoint: Regime
    description_admission_count: int
    stepper_application_count: int


def separation_base() -> Regime:
    """The frozen ledger row: two admitted data and one imposed pair."""

    return replay(
        (AdmitDatum("a"), AdmitDatum("b"), Impose(0, 1))
    )


def slot_tuples(arity: int, n_data: int) -> Iterator[tuple[Slot, ...]]:
    options: tuple[Slot, ...] = (None, *range(n_data))
    yield from product(options, repeat=arity)


def contexts(regime: Regime) -> tuple[Context, ...]:
    result: list[Context] = []
    for form, arity in enumerate(regime.forms):
        for slots in slot_tuples(arity, len(regime.data)):
            if any(slot is None for slot in slots):
                result.append((form, slots))
    return tuple(result)


def plug(context: Context, datum: int) -> tuple[int, Args]:
    form, slots = context
    return form, tuple(datum if slot is None else slot for slot in slots)


def derivable(regime: Regime, inst: tuple[int, Args]) -> bool:
    return inst[0] in regime.rules or inst in regime.insts


def profile(regime: Regime, datum: int) -> frozenset[Context]:
    return frozenset(
        context
        for context in contexts(regime)
        if derivable(regime, plug(context, datum))
    )


def separable(regime: Regime, pair: Pair) -> bool:
    return profile(regime, pair[0]) != profile(regime, pair[1])


def satisfies(regime: Regime) -> bool:
    return all(separable(regime, pair) for pair in sorted(regime.reqs))


def item_key(item: Item) -> tuple[int, int, Args]:
    if isinstance(item, NewDatum):
        return 0, 0, ()
    if isinstance(item, NewForm):
        return 1, item.arity, ()
    if isinstance(item, NewRuleAll):
        return 2, item.form, ()
    return 3, item.form, item.args


def canonical_delta(items: tuple[Item, ...]) -> Delta:
    return tuple(sorted(items, key=item_key))


def delta_key(delta: Delta) -> tuple[tuple[int, int, Args], ...]:
    return tuple(item_key(item) for item in delta)


def mu1(delta: Delta) -> int:
    return len(delta)


def mu2(delta: Delta) -> tuple[int, int]:
    return (
        len(delta),
        sum(item.arity for item in delta if isinstance(item, NewForm)),
    )


def delta_events(base: Regime, delta: Delta) -> tuple[Event, ...]:
    events: list[Event] = []
    n_data = len(base.data)
    for item in delta:
        if isinstance(item, NewDatum):
            events.append(AdmitDatum(f"w{n_data}"))
            n_data += 1
        elif isinstance(item, NewForm):
            events.append(AdmitForm(item.arity))
        elif isinstance(item, NewRuleAll):
            events.append(AdmitRuleAll(item.form))
        else:
            events.append(AdmitInst(item.form, item.args))
    return tuple(events)


def execute_response_events(
    base: Regime, events: tuple[Event, ...]
) -> ResponseEventRun:
    """Apply each supplied response event through one kernel transition.

    This is a response-event stepper, not the ``DR-C-2-1-3`` decoder
    surface: the response base and event tokens are outside that decoder's
    frozen alphabet.  Each event contributes one description admission to
    the declared price and exactly one transition call to the execution.
    """

    if not all(
        isinstance(event, (AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll))
        for event in events
    ):
        raise ValueError("response execution accepts admission events only")
    current = base
    applications = 0
    for event in events:
        current = apply_event(current, event)
        applications += 1
    return ResponseEventRun(current, len(events), applications)


def execute_delta(base: Regime, delta: Delta) -> ResponseEventRun:
    """Translate and execute one supplied response."""

    return execute_response_events(base, delta_events(base, delta))


def apply_delta(base: Regime, delta: Delta) -> Regime:
    return execute_delta(base, delta).endpoint


def response_valid(base: Regime, delta: Delta) -> bool:
    return satisfies(apply_delta(base, delta))


def has_removable_rule(delta: Delta) -> bool:
    """Named cost-two exclusion: a uniform rule cannot create a difference."""

    return any(isinstance(item, NewRuleAll) for item in delta)


def has_irrelevant_new_datum(base: Regime, delta: Delta) -> bool:
    """Named exclusion: a fresh datum is irrelevant unless an instance uses it."""

    fresh_index = len(base.data)
    return any(isinstance(item, NewDatum) for item in delta) and not any(
        isinstance(item, NewInst) and fresh_index in item.args for item in delta
    )


def has_irrelevant_new_form(base: Regime, delta: Delta) -> bool:
    """Named exclusion: a fresh form is irrelevant unless instantiated."""

    fresh_index = len(base.forms)
    return any(isinstance(item, NewForm) for item in delta) and not any(
        isinstance(item, NewInst) and item.form == fresh_index for item in delta
    )


def instances_miss_target(delta: Delta, target: Pair = TARGET) -> bool:
    """Named exclusion: an instance-only response must mention the target."""

    return bool(delta) and all(isinstance(item, NewInst) for item in delta) and not any(
        isinstance(item, NewInst)
        and any(argument in frozenset(target) for argument in item.args)
        for item in delta
    )


def iter_cost1_items(base: Regime) -> Iterator[Item]:
    yield NewDatum()
    for arity in range(1, MAX_ARITY + 1):
        yield NewForm(arity)
    for form in sorted(set(range(len(base.forms))) - set(base.rules)):
        yield NewRuleAll(form)
    for form, arity in enumerate(base.forms):
        for args in product(range(len(base.data)), repeat=arity):
            yield NewInst(form, tuple(args))


def iter_pruned_cost2(base: Regime) -> Iterator[Delta]:
    """Enumerate the three surviving shapes after four named exclusions."""

    n_data = len(base.data)
    new_form = len(base.forms)

    # Shape one: the fresh form is paid together with one instance on it.
    for arity in range(1, MAX_ARITY + 1):
        for args in product(range(n_data), repeat=arity):
            yield canonical_delta((NewForm(arity), NewInst(new_form, tuple(args))))

    # Shape two: a fresh datum is paid with an existing-form instance that
    # actually mentions it.
    for form, arity in enumerate(base.forms):
        for args in product(range(n_data + 1), repeat=arity):
            if n_data in args:
                yield canonical_delta((NewDatum(), NewInst(form, tuple(args))))

    # Shape three: two distinct existing-form instances, with at least one
    # mentioning the demanded pair.
    target_set = frozenset(TARGET)
    all_insts = [
        NewInst(form, tuple(args))
        for form, arity in enumerate(base.forms)
        for args in product(range(n_data), repeat=arity)
    ]
    mentioning = [
        item for item in all_insts if any(arg in target_set for arg in item.args)
    ]
    for left in mentioning:
        for right in all_insts:
            if left == right:
                continue
            if (
                any(arg in target_set for arg in right.args)
                and item_key(right) < item_key(left)
            ):
                continue
            yield canonical_delta((left, right))


def iter_full_deltas(base: Regime, cost: int) -> Iterator[Delta]:
    if cost == 0:
        yield ()
        return
    if cost == 1:
        yield from ((item,) for item in iter_cost1_items(base))
        return
    if cost != 2:
        raise ValueError("full enumeration is declared only through two items")

    n_data = len(base.data)
    universe: list[Item] = [NewDatum(), NewForm(1)]
    max_form = len(base.forms) + 1
    for form in range(max_form):
        universe.append(NewRuleAll(form))
        for args in product(range(n_data + 1), repeat=1):
            universe.append(NewInst(form, tuple(args)))
    seen: set[Delta] = set()
    for left in universe:
        for right in universe:
            delta = canonical_delta((left, right))
            if delta in seen:
                continue
            seen.add(delta)
            try:
                apply_delta(base, delta)
            except AdmissionError:
                continue
            yield delta


def candidates_at_cost(base: Regime, cost: int) -> tuple[Delta, ...]:
    if cost == 0:
        return ((),)
    if cost == 1:
        return tuple((item,) for item in iter_cost1_items(base))
    if cost == 2:
        return tuple(sorted(set(iter_pruned_cost2(base)), key=delta_key))
    raise ValueError("candidate cost is outside the declared bound")


def checking_cost(delta: Delta) -> int:
    run = execute_delta(separation_base(), delta)
    return run.description_admission_count + run.stepper_application_count


@lru_cache(maxsize=2)
def find_responses(measure: str) -> FinderResult:
    if measure not in {"mu1", "mu2"}:
        raise ValueError(f"unknown measure {measure}")
    base = separation_base()
    checked: list[Delta] = []
    total_cost = 0
    for cost in range(MAX_ITEMS + 1):
        level = candidates_at_cost(base, cost)
        checked.extend(level)
        runs = tuple((delta, execute_delta(base, delta)) for delta in level)
        total_cost += sum(
            run.description_admission_count + run.stepper_application_count
            for _, run in runs
        )
        valid = [delta for delta, run in runs if satisfies(run.endpoint)]
        if not valid:
            continue
        if measure == "mu1":
            best: MeasureValue = min(mu1(delta) for delta in valid)
            winners = tuple(sorted(valid, key=delta_key))
        else:
            best = min(mu2(delta) for delta in valid)
            winners = tuple(
                sorted(
                    (delta for delta in valid if mu2(delta) == best),
                    key=delta_key,
                )
            )
        return FinderResult(measure, best, tuple(checked), winners, total_cost)
    raise ValueError("no response inside the declared candidate bound")


def item_json(item: Item) -> dict[str, object]:
    if isinstance(item, NewDatum):
        return {"kind": "new_datum"}
    if isinstance(item, NewForm):
        return {"arity": item.arity, "kind": "new_form"}
    if isinstance(item, NewRuleAll):
        return {"form": item.form, "kind": "new_rule_all"}
    return {"args": list(item.args), "form": item.form, "kind": "new_inst"}


def delta_json(delta: Delta) -> list[dict[str, object]]:
    return [item_json(item) for item in delta]


def supplied_response_json(base: Regime, delta: Delta) -> dict[str, object]:
    run = execute_delta(base, delta)
    return {
        "check_cost": checking_cost(delta),
        "description_admission_count": run.description_admission_count,
        "response": delta_json(delta),
        "stepper_application_count": run.stepper_application_count,
    }


def canonical_regime_key(regime: Regime) -> CanonKey:
    n_data = len(regime.data)
    n_forms = len(regime.forms)
    keys: list[CanonKey] = []
    for data_perm in permutations(range(n_data)):
        for form_perm in permutations(range(n_forms)):
            forms_out = [0] * n_forms
            for old, new in enumerate(form_perm):
                forms_out[new] = regime.forms[old]
            insts_out = tuple(
                sorted(
                    (
                        form_perm[form],
                        tuple(data_perm[arg] for arg in args),
                    )
                    for form, args in regime.insts
                )
            )
            rules_out = tuple(sorted(form_perm[form] for form in regime.rules))
            reqs_out: tuple[Pair, ...] = tuple(
                sorted(
                    (
                        (data_perm[left], data_perm[right])
                        if data_perm[left] <= data_perm[right]
                        else (data_perm[right], data_perm[left])
                    )
                    for left, right in regime.reqs
                )
            )
            keys.append((n_data, tuple(forms_out), insts_out, rules_out, reqs_out))
    return min(keys)


def grouped_winners(result: FinderResult) -> tuple[tuple[Delta, ...], ...]:
    groups: dict[CanonKey, list[Delta]] = {}
    base = separation_base()
    for delta in result.winners:
        key = canonical_regime_key(apply_delta(base, delta))
        groups.setdefault(key, []).append(delta)
    ordered = sorted(groups.values(), key=lambda group: delta_key(group[0]))
    return tuple(tuple(sorted(group, key=delta_key)) for group in ordered)


def render_cost_ledger() -> dict[str, object]:
    base = separation_base()
    full_valid = tuple(
        sorted(
            (
                delta
                for delta in iter_full_deltas(base, 2)
                if response_valid(base, delta)
            ),
            key=delta_key,
        )
    )
    pruned_valid = tuple(
        delta for delta in candidates_at_cost(base, 2) if response_valid(base, delta)
    )
    rows: list[dict[str, object]] = []
    for measure in ("mu1", "mu2"):
        result = find_responses(measure)
        groups = grouped_winners(result)
        supplied = [
            supplied_response_json(base, delta)
            for delta in result.winners
        ]
        denominator = checking_cost(result.winners[0])
        rows.append(
            {
                "checked_candidate_count": len(result.checked),
                "finding_cost": result.finding_cost,
                "measure": measure,
                "measure_value": (
                    list(result.measure_value)
                    if isinstance(result.measure_value, tuple)
                    else result.measure_value
                ),
                "ratio": {
                    "denominator": denominator,
                    "numerator": result.finding_cost,
                },
                "retained_isomorphism_classes": [
                    [delta_json(delta) for delta in group] for group in groups
                ],
                "supplied_responses": supplied,
                "tied_response_count": len(result.winners),
            }
        )
    return {
        "authority_effect": None,
        "execution_surface": "response_event_stepper_not_dr_decoder",
        "base": regime_json(base),
        "bounds": {
            "max_arity": MAX_ARITY,
            "max_items": MAX_ITEMS,
            "max_new_data": 1,
            "max_new_forms": 1,
        },
        "cost_excludes": [
            "canonical_key_construction",
            "predicate_evaluation",
            "state_hashing",
        ],
        "cost_rule": "stepper_applications_plus_description_admission_events",
        "full_two_item_valid": [delta_json(delta) for delta in full_valid],
        "largest_completed_row": 2,
        "pruned_full_valid_agree": pruned_valid == full_valid,
        "pruned_two_item_valid": [delta_json(delta) for delta in pruned_valid],
        "rows": rows,
        "terminal": "COST_TABLE_WRITTEN",
        "unbounded": "OPEN_UNBOUNDED",
    }
