"""Candidate actions and factories. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from . import _bootstrap  # noqa: F401
from derivation.iso import CanonKey
from research.x301_formal_semantics.semantics import RelationalModel
from .keys import compute_canon_key


@dataclass(frozen=True)
class CandidateAction:
    """Operational candidate: a pure function Carrier -> Carrier plus a fuel cost.

    `delta_fn` must not mutate its argument. RelationalModel is frozen; a
    mutating callable is a contract violation, not a licensed apply.
    """

    name: str
    fuel_cost: int
    delta_fn: Callable[[RelationalModel], RelationalModel]
    description: str = ""
    canon_key: Optional[CanonKey] = None

    def __post_init__(self) -> None:
        if self.fuel_cost < 0:
            raise ValueError(f"fuel_cost cannot be negative: {self.fuel_cost}")

    def apply(self, model: RelationalModel) -> RelationalModel:
        return self.delta_fn(model)

    def get_canon_key(self, resulting_model: RelationalModel) -> CanonKey:
        if self.canon_key is not None:
            return self.canon_key
        return compute_canon_key(resulting_model)

    def __repr__(self) -> str:
        return f"CandidateAction({self.name}, cost={self.fuel_cost})"


def _clone_model(
    m: RelationalModel,
    *,
    insts: Optional[frozenset[tuple[int, tuple[int, ...]]]] = None,
    rules: Optional[frozenset[int]] = None,
    reqs: Optional[frozenset[tuple[int, int]]] = None,
) -> RelationalModel:
    return RelationalModel(
        data=m.data,
        forms=m.forms,
        insts=m.insts if insts is None else insts,
        rules=m.rules if rules is None else rules,
        reqs=m.reqs if reqs is None else reqs,
        custom_relations=m.custom_relations,
        custom_domains=m.custom_domains,
    )


def add_instance_action(form: int, args: tuple[int, ...], fuel_cost: int = 1, name: str = "") -> CandidateAction:
    def _apply(m: RelationalModel) -> RelationalModel:
        return _clone_model(m, insts=m.insts | {(form, args)})

    lbl = name or f"add_inst({form}, {args})"
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Add instance ({form}, {args})")


def remove_instance_action(form: int, args: tuple[int, ...], fuel_cost: int = 1, name: str = "") -> CandidateAction:
    def _apply(m: RelationalModel) -> RelationalModel:
        return _clone_model(m, insts=m.insts - {(form, args)})

    lbl = name or f"rem_inst({form}, {args})"
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Remove instance ({form}, {args})")


def toggle_rule_action(form: int, fuel_cost: int = 1, name: str = "") -> CandidateAction:
    def _apply(m: RelationalModel) -> RelationalModel:
        new_rules = m.rules - {form} if form in m.rules else m.rules | {form}
        return _clone_model(m, rules=new_rules)

    lbl = name or f"toggle_rule({form})"
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Toggle rule for form {form}")


def add_requirement_action(i: int, j: int, fuel_cost: int = 1, name: str = "") -> CandidateAction:
    pair = (min(i, j), max(i, j))

    def _apply(m: RelationalModel) -> RelationalModel:
        return _clone_model(m, reqs=m.reqs | {pair})

    lbl = name or f"add_req({pair[0]}, {pair[1]})"
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Impose separation pair {pair}")
