"""Codecs, typed histories, task comparison, and common-measure pricing."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable, Mapping, Sequence

from .enumerate import Candidate, History
from .model import (
    BoundaryRefusal,
    BoundaryState,
    Mark,
    RawEvent,
    RawKind,
    SourceEvent,
    SourceReplay,
    SourceState,
    Transaction,
    flatten_transactions,
    measure,
    replay_boundary,
    replay_source,
    source_raw_trace,
    source_step,
)


TAGS: dict[str, tuple[int, int]] = {
    "datum": (0, 0),
    "form": (0, 1),
    "instance": (1, 0),
    "rule": (1, 1),
}

# label -> (role, logical side)
LABEL_SPECS: dict[str, tuple[str, int]] = {
    "d0": ("datum", 0),
    "d1": ("datum", 1),
    "form_0": ("form", 0),
    "form_1": ("form", 1),
    "inst_0": ("instance", 0),
    "inst_1": ("instance", 1),
    "rule_0": ("rule", 0),
    "rule_1": ("rule", 1),
    "comp_0": ("instance", 1),
    "comp_1": ("instance", 0),
}

REFUSAL_CODES: tuple[str, ...] = (
    "UNKNOWN_LABEL",
    "DUPLICATE_LABEL",
    "ROLE_STRUCTURE",
    "ADDRESS_FAMILY",
)


def address_for(label: str, family: str) -> tuple[int, int, int]:
    role, side = LABEL_SPECS[label]
    if family == "complemented":
        side = 1 - side
    elif family != "direct":
        raise ValueError(f"unknown address family {family!r}")
    tag = TAGS[role]
    return (side, tag[0], tag[1])


def labels_for_state(state: SourceState) -> frozenset[str]:
    labels: set[str] = set()
    for datum in state.data:
        labels.add(f"d{datum}")
    if state.form:
        labels.update(("form_0", "form_1"))
    for datum in state.instances:
        labels.add(f"inst_{datum}")
    if state.rule:
        labels.update(("rule_0", "rule_1"))
        for datum in state.instances:
            labels.add(f"comp_{datum}")
    return frozenset(labels)


def encode_state(state: SourceState, family: str) -> BoundaryState:
    return BoundaryState(
        frozenset(Mark(label, address_for(label, family)) for label in labels_for_state(state))
    )


@dataclass(frozen=True)
class DecodeResult:
    state: SourceState | None
    family: str | None
    refusal: str | None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _decoded_fields(labels: set[str]) -> SourceState | None:
    form_pair = {"form_0", "form_1"}
    rule_pair = {"rule_0", "rule_1"}
    if bool(labels & form_pair) and not form_pair <= labels:
        return None
    if bool(labels & rule_pair) and not rule_pair <= labels:
        return None
    data = frozenset(i for i in (0, 1) if f"d{i}" in labels)
    instances = frozenset(i for i in (0, 1) if f"inst_{i}" in labels)
    form = form_pair <= labels
    rule = rule_pair <= labels
    if instances and not form:
        return None
    if any(i not in data for i in instances):
        return None
    if rule and not form:
        return None
    expected_comp = {f"comp_{i}" for i in instances} if rule else set()
    present_comp = {label for label in labels if label.startswith("comp_")}
    if present_comp != expected_comp:
        return None
    return SourceState(data=data, form=form, instances=instances, rule=rule)


def decode_state(boundary: BoundaryState) -> DecodeResult:
    labels = [mark.label for mark in boundary.marks]
    if any(label not in LABEL_SPECS for label in labels):
        return DecodeResult(None, None, "UNKNOWN_LABEL")
    if len(labels) != len(set(labels)):
        return DecodeResult(None, None, "DUPLICATE_LABEL")
    for mark in boundary.marks:
        if (
            len(mark.address) != 3
            or any(bit not in (0, 1) for bit in mark.address)
            or tuple(mark.address[1:]) != TAGS[LABEL_SPECS[mark.label][0]]
        ):
            return DecodeResult(None, None, "ROLE_STRUCTURE")
    state = _decoded_fields(set(labels))
    if state is None:
        return DecodeResult(None, None, "ROLE_STRUCTURE")
    for family in ("direct", "complemented"):
        if encode_state(state, family) == boundary:
            return DecodeResult(state, family, None)
    return DecodeResult(None, None, "ADDRESS_FAMILY")


def typed_states(states: Iterable[SourceState]) -> tuple[BoundaryState, ...]:
    result = {
        encode_state(state, family)
        for state in states
        for family in ("direct", "complemented")
    }
    return tuple(
        sorted(
            result,
            key=lambda state: tuple((mark.label, mark.address) for mark in sorted(state.marks)),
        )
    )


def _fixed_labels(event: SourceEvent) -> frozenset[str]:
    if event is SourceEvent.ADMIT_D0:
        return frozenset({"d0"})
    if event is SourceEvent.ADMIT_D1:
        return frozenset({"d1"})
    if event is SourceEvent.ADMIT_FORM:
        return frozenset({"form_0", "form_1"})
    if event is SourceEvent.ADMIT_INST0:
        return frozenset({"inst_0"})
    if event is SourceEvent.ADMIT_INST1:
        return frozenset({"inst_1"})
    if event is SourceEvent.ADMIT_RULE:
        return frozenset({"rule_0", "rule_1"})
    raise ValueError(f"presentation event has no admission block: {event.value}")


def _event_marks(
    candidate: Candidate,
    event: SourceEvent,
    before: SourceState,
    after: SourceState,
) -> tuple[Mark, ...]:
    if candidate.event_context == "state_sensitive":
        labels = labels_for_state(after) - labels_for_state(before)
    elif candidate.event_context == "memoryless":
        labels = _fixed_labels(event)
    else:
        raise ValueError(f"unknown event context {candidate.event_context!r}")
    return tuple(
        sorted(Mark(label, address_for(label, candidate.address_family)) for label in labels)
    )


def translate_history(candidate: Candidate, history: History) -> tuple[Transaction, ...]:
    """Translate accepted source events without mutating either final state."""

    source = SourceReplay()
    presented: set[str] = set()
    transactions: list[Transaction] = []
    for event in history:
        if event in (SourceEvent.SUPPLY_D0, SourceEvent.SUPPLY_D1):
            label = "d0" if event is SourceEvent.SUPPLY_D0 else "d1"
            raw = RawEvent(RawKind.PRESENTATION, label)
            transactions.append(Transaction(RawKind.PRESENTATION, (raw,)))
            presented.add(label)
            source = source_step(source, event)
            continue

        before = source.state
        source = source_step(source, event)
        marks = _event_marks(candidate, event, before, source.state)
        raw_events: list[RawEvent] = []
        for mark in marks:
            if candidate.synthetic_supply and mark.label not in presented:
                raw_events.append(RawEvent(RawKind.PRESENTATION, mark.label))
                presented.add(mark.label)
            raw_events.append(RawEvent(RawKind.ADMISSION, mark.label, mark))
        transactions.append(Transaction(RawKind.ADMISSION, tuple(raw_events)))
    return tuple(transactions)


def decode_history(transactions: Sequence[Transaction]) -> History:
    """Decode source events from typed transactions and their admitted blocks."""

    source = SourceReplay()
    result: list[SourceEvent] = []
    for transaction in transactions:
        if transaction.kind is RawKind.PRESENTATION:
            presentation_labels = [raw.label for raw in transaction.raw]
            if presentation_labels == ["d0"]:
                event = SourceEvent.SUPPLY_D0
            elif presentation_labels == ["d1"]:
                event = SourceEvent.SUPPLY_D1
            else:
                raise BoundaryRefusal("UNDECODABLE_PRESENTATION")
        else:
            admission_labels = {
                raw.label for raw in transaction.raw if raw.kind is RawKind.ADMISSION
            }
            if admission_labels == {"d0"}:
                event = SourceEvent.ADMIT_D0
            elif admission_labels == {"d1"}:
                event = SourceEvent.ADMIT_D1
            elif admission_labels == {"form_0", "form_1"}:
                event = SourceEvent.ADMIT_FORM
            elif admission_labels in ({"inst_0"}, {"inst_0", "comp_0"}):
                event = SourceEvent.ADMIT_INST0
            elif admission_labels in ({"inst_1"}, {"inst_1", "comp_1"}):
                event = SourceEvent.ADMIT_INST1
            elif {"rule_0", "rule_1"} <= admission_labels and admission_labels <= {
                "rule_0",
                "rule_1",
                "comp_0",
                "comp_1",
            }:
                event = SourceEvent.ADMIT_RULE
            else:
                raise BoundaryRefusal("UNDECODABLE_ADMISSION")
        source = source_step(source, event)
        result.append(event)
    return tuple(result)


def _transformed_address(
    address: tuple[int, ...], outer: bool, tag0: bool, tag1: bool
) -> tuple[int, ...]:
    return (
        address[0] ^ int(outer),
        address[1] ^ int(tag0),
        address[2] ^ int(tag1),
    )


def boundary_task(candidate: Candidate, boundary: BoundaryState) -> bool | None:
    """Whether no permitted automorphism carries retained d0 to retained d1."""

    marks = {mark.label: mark for mark in boundary.marks}
    if "d0" not in marks or "d1" not in marks:
        return None
    if not candidate.mark_permutations:
        return True
    outer_choices = (False, True) if candidate.outer_exchange else (False,)
    tag_choices = (False,) if candidate.tag_levels_named else (False, True)
    original = sorted(
        (
            mark.label if candidate.keep_labels else "",
            mark.address,
        )
        for mark in boundary.marks
    )
    for outer, tag0, tag1 in product(outer_choices, tag_choices, tag_choices):
        moved = sorted(
            (
                mark.label if candidate.keep_labels else "",
                _transformed_address(mark.address, outer, tag0, tag1),
            )
            for mark in boundary.marks
        )
        carries = _transformed_address(
            marks["d0"].address, outer, tag0, tag1
        ) == marks["d1"].address
        if candidate.keep_labels:
            carries = False
        if moved == original and carries:
            return False
    return True


def nearby_shell(states: Sequence[BoundaryState]) -> tuple[BoundaryState, ...]:
    """Candidate-independent one-field mutation shell around typed states."""

    shell: set[BoundaryState] = set()
    allowed = tuple(sorted(LABEL_SPECS))
    for state in states:
        marks = set(state.marks)
        by_label = {mark.label: mark for mark in marks}
        for mark in tuple(marks):
            shell.add(BoundaryState(frozenset(marks - {mark})))
            shell.add(
                BoundaryState(
                    frozenset((marks - {mark}) | {Mark("unknown", mark.address)})
                )
            )
            for bit in range(3):
                changed = list(mark.address)
                changed[bit] = 1 - changed[bit]
                shell.add(
                    BoundaryState(
                        frozenset((marks - {mark}) | {Mark(mark.label, tuple(changed))})
                    )
                )
        for label in allowed:
            if label not in by_label:
                shell.add(
                    BoundaryState(
                        frozenset(marks | {Mark(label, address_for(label, "direct"))})
                    )
                )
            else:
                mark = by_label[label]
                flipped_address = (1 - mark.address[0], *mark.address[1:])
                shell.add(
                    BoundaryState(frozenset(marks | {Mark(label, flipped_address)}))
                )
        shell.add(BoundaryState(frozenset(marks | {Mark("unknown", (0, 0, 0))})))
    typed = set(states)
    invalid = shell - typed
    return tuple(
        sorted(
            invalid,
            key=lambda state: tuple((mark.label, mark.address) for mark in sorted(state.marks)),
        )
    )


def shell_report(shell: Sequence[BoundaryState]) -> dict[str, object]:
    counts = {code: 0 for code in REFUSAL_CODES}
    examples: dict[str, object] = {}
    silent: list[object] = []
    for state in shell:
        result = decode_state(state)
        if result.refusal is None:
            silent.append(state.as_record())
            continue
        counts[result.refusal] += 1
        examples.setdefault(result.refusal, state.as_record())
    return {
        "code_counts": counts,
        "codes": list(REFUSAL_CODES),
        "examples": examples,
        "population": len(shell),
        "silent_truncations": silent,
    }


@dataclass(frozen=True)
class CandidateVerdict:
    candidate: Candidate
    valid: bool
    clauses: dict[str, bool]
    counterexamples: dict[str, object]

    def as_record(self) -> dict[str, object]:
        return {
            "candidate": self.candidate.as_record(),
            "clauses": self.clauses,
            "counterexamples": self.counterexamples,
            "statement_capabilities": list(statement_capabilities(self.candidate)),
            "statement_price": len(statement_capabilities(self.candidate)),
            "valid": self.valid,
        }


def statement_capabilities(candidate: Candidate) -> tuple[str, ...]:
    capabilities: list[str] = []
    if candidate.event_context == "state_sensitive":
        capabilities.append("state_inspection")
    if candidate.synthetic_supply:
        capabilities.append("administrative_presentation")
    return tuple(capabilities)


def evaluate_candidate(
    candidate: Candidate,
    histories: Sequence[History],
    domain: Sequence[BoundaryState],
    shell: Sequence[BoundaryState],
) -> CandidateVerdict:
    clauses = {
        "accepted_events": True,
        "carrier": True,
        "costs_total": True,
        "histories": True,
        "refusal_shell": True,
        "tasks": True,
    }
    counterexamples: dict[str, object] = {}

    # A permitted tag exchange would exchange source sorts.  The source carrier
    # retains those sorts separately, so it is a carrier failure, not a price.
    if not candidate.tag_levels_named:
        clauses["carrier"] = False
        counterexamples["carrier"] = {
            "reason": "tag exchange does not preserve the four retained source sorts",
            "witness": "d0",
        }

    for index, history in enumerate(histories):
        translated = translate_history(candidate, history)
        source = replay_source(history)
        try:
            boundary = replay_boundary(translated)
        except BoundaryRefusal as exc:
            clauses["accepted_events"] = False
            counterexamples.setdefault(
                "accepted_events",
                {"history": index, "reason": str(exc)},
            )
            continue
        expected = encode_state(source.state, candidate.address_family)
        if boundary.state != expected:
            clauses["histories"] = False
            counterexamples.setdefault(
                "histories",
                {
                    "actual": boundary.state.as_record(),
                    "expected": expected.as_record(),
                    "history": index,
                },
            )
        decoded_state = decode_state(boundary.state)
        if decoded_state.state != source.state:
            clauses["carrier"] = False
            counterexamples.setdefault(
                "carrier",
                {"history": index, "reason": decoded_state.refusal or "state mismatch"},
            )
        try:
            decoded_history = decode_history(translated)
            decoded_replay = replay_source(decoded_history)
        except (BoundaryRefusal, ValueError) as exc:
            clauses["histories"] = False
            counterexamples.setdefault(
                "histories", {"history": index, "reason": str(exc)}
            )
        else:
            if decoded_replay.state != source.state:
                clauses["histories"] = False
                counterexamples.setdefault(
                    "histories", {"history": index, "reason": "decoded replay mismatch"}
                )
        if source.state.task() is not None:
            target_task = boundary_task(candidate, boundary.state)
            if target_task != source.state.task():
                clauses["tasks"] = False
                counterexamples.setdefault(
                    "tasks",
                    {
                        "history": index,
                        "source": source.state.task(),
                        "target": target_task,
                    },
                )
        # Calling the one shared function on both traces is the totality check.
        for name in ("mu1", "mu2"):
            measure(source_raw_trace(history), name)
            measure(flatten_transactions(translated), name)

    for state in domain:
        decoded = decode_state(state)
        if decoded.state is None or decoded.family is None:
            clauses["carrier"] = False
            counterexamples.setdefault(
                "carrier", {"reason": decoded.refusal, "state": state.as_record()}
            )
            continue
        if encode_state(decoded.state, decoded.family) != state:
            clauses["carrier"] = False
            counterexamples.setdefault(
                "carrier", {"reason": "typed round trip", "state": state.as_record()}
            )
        if decoded.state.task() is not None:
            target_task = boundary_task(candidate, state)
            if target_task != decoded.state.task():
                clauses["tasks"] = False
                counterexamples.setdefault(
                    "tasks",
                    {
                        "source": decoded.state.task(),
                        "state": state.as_record(),
                        "target": target_task,
                    },
                )

    shell_data = shell_report(shell)
    counts = shell_data["code_counts"]
    assert isinstance(counts, dict)
    shell_ok = (
        bool(shell)
        and not shell_data["silent_truncations"]
        and all(counts.get(code, 0) for code in REFUSAL_CODES)
    )
    if not shell_ok:
        clauses["refusal_shell"] = False
        counterexamples["refusal_shell"] = shell_data

    return CandidateVerdict(candidate, all(clauses.values()), clauses, counterexamples)


def _ratio(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "ZERO_BASE"
    value = Fraction(numerator, denominator)
    return f"{value.numerator}/{value.denominator}"


def distortion_report(candidate: Candidate, histories: Sequence[History]) -> dict[str, object]:
    table: list[dict[str, object]] = []
    for index, history in enumerate(histories):
        translated = translate_history(candidate, history)
        source_trace = source_raw_trace(history)
        target_trace = flatten_transactions(translated)
        row: dict[str, object] = {
            "history": [event.value for event in history],
            "history_id": index,
        }
        for name in ("mu1", "mu2"):
            source_cost = measure(source_trace, name)
            target_cost = measure(target_trace, name)
            row[name] = {
                "backward_additive": source_cost - target_cost,
                "backward_multiplicative": _ratio(source_cost, target_cost),
                "forward_additive": target_cost - source_cost,
                "forward_multiplicative": _ratio(target_cost, source_cost),
                "source": source_cost,
                "target": target_cost,
            }
        table.append(row)

    extrema: dict[str, object] = {}
    exact = True

    def additive(row: Mapping[str, object], measure_name: str, key: str) -> int:
        values = row[measure_name]
        assert isinstance(values, dict)
        value = values[key]
        assert isinstance(value, int)
        return value

    for name in ("mu1", "mu2"):
        forward = [additive(row, name, "forward_additive") for row in table]
        backward = [additive(row, name, "backward_additive") for row in table]
        exact = exact and all(value == 0 for value in forward)
        extrema[name] = {
            "backward_max": max(backward),
            "backward_max_witness": backward.index(max(backward)),
            "backward_min": min(backward),
            "backward_min_witness": backward.index(min(backward)),
            "forward_max": max(forward),
            "forward_max_witness": forward.index(max(forward)),
            "forward_min": min(forward),
            "forward_min_witness": forward.index(min(forward)),
        }
    return {"exact_both_measures": exact, "extrema": extrema, "table": table}


def provenance_witness(states: Sequence[SourceState], family: str) -> dict[str, object]:
    for left_index, left in enumerate(states):
        for right_index, right in enumerate(states[left_index + 1 :], left_index + 1):
            if (
                left.data == frozenset({0, 1})
                and right.data == frozenset({0, 1})
                and [left.profile(0), left.profile(1)]
                == [right.profile(0), right.profile(1)]
                and left.instances != right.instances
                and left.rule != right.rule
            ):
                left_labels = sorted(mark.label for mark in encode_state(left, family).marks)
                right_labels = sorted(mark.label for mark in encode_state(right, family).marks)
                if left_labels != right_labels:
                    return {
                        "equal_profile": [left.profile(0), left.profile(1)],
                        "left": left.as_record(),
                        "left_index": left_index,
                        "left_labels": left_labels,
                        "right": right.as_record(),
                        "right_index": right_index,
                        "right_labels": right_labels,
                    }
    raise AssertionError("no equal-profile provenance witness in the declared state space")
