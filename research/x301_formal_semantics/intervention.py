"""Executable interventions and empirical-reference checks.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

from formulas import Formula
from model import RelationalModel, evaluate
from valuation import RationalValuation


@dataclass(frozen=True)
class Intervention:
    """Executable state perturbation I: Carrier -> Carrier."""

    name: str
    delta_fn: Callable[[RelationalModel], RelationalModel]
    description: str = ""

    def apply(self, model: RelationalModel) -> RelationalModel:
        return self.delta_fn(model)

    def __repr__(self) -> str:
        return f"Intervention({self.name})"


def add_instance_intervention(form: int, args: tuple[int, ...], name: str = "") -> Intervention:
    def _apply(m: RelationalModel) -> RelationalModel:
        new_insts = m.insts | {(form, args)}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=new_insts,
            rules=m.rules,
            reqs=m.reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"add_inst({form}, {args})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Add instance ({form}, {args})")


def remove_instance_intervention(form: int, args: tuple[int, ...], name: str = "") -> Intervention:
    def _apply(m: RelationalModel) -> RelationalModel:
        new_insts = m.insts - {(form, args)}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=new_insts,
            rules=m.rules,
            reqs=m.reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"rem_inst({form}, {args})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Remove instance ({form}, {args})")


def toggle_rule_intervention(form: int, name: str = "") -> Intervention:
    def _apply(m: RelationalModel) -> RelationalModel:
        new_rules = m.rules - {form} if form in m.rules else m.rules | {form}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=m.insts,
            rules=new_rules,
            reqs=m.reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"toggle_rule({form})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Toggle all-tuples rule on form {form}")


def add_requirement_intervention(i: int, j: int, name: str = "") -> Intervention:
    pair = (min(i, j), max(i, j))
    def _apply(m: RelationalModel) -> RelationalModel:
        new_reqs = m.reqs | {pair}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=m.insts,
            rules=m.rules,
            reqs=new_reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"impose_req({pair[0]}, {pair[1]})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Add requirement ({pair[0]}, {pair[1]})")


def has_empirical_reference(
    formula: Formula,
    model: RelationalModel,
    intervention_pool: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
) -> bool:
    """Check if formula has empirical reference grounded in executable interventions.

    An assertion phi possesses empirical reference relative to an intervention pool
    iff there exists an intervention I in the pool whose observable readout discriminates phi:
    evaluate(model, phi) != evaluate(I(model), phi).
    """
    env = assignment or {}
    base_val = evaluate(model, formula, env)
    for interv in intervention_pool:
        perturbed = interv.apply(model)
        pert_val = evaluate(perturbed, formula, env)
        if base_val != pert_val:
            return True
    return False


def find_discriminating_witness(
    formula: Formula,
    model: RelationalModel,
    intervention_pool: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
) -> Optional[Intervention]:
    """Find a concrete counterfactual intervention witness that discriminates formula."""
    env = assignment or {}
    base_val = evaluate(model, formula, env)
    for interv in intervention_pool:
        perturbed = interv.apply(model)
        pert_val = evaluate(perturbed, formula, env)
        if base_val != pert_val:
            return interv
    return None


def are_behaviorally_congruent(
    phi: Formula,
    psi: Formula,
    models: Sequence[RelationalModel],
    intervention_pool: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
) -> bool:
    """Check behavioral congruence: phi =_obs psi.

    Two formulas are behaviorally congruent across a domain of carrier states and
    interventions iff no admissible intervention can ever distinguish them.
    Ungrounded decorative distinctions lacking an intervention witness are identified.
    """
    env = assignment or {}
    for m in models:
        if evaluate(m, phi, env) != evaluate(m, psi, env):
            return False
        for interv in intervention_pool:
            pert = interv.apply(m)
            if evaluate(pert, phi, env) != evaluate(pert, psi, env):
                return False
    return True


# ---------------------------------------------------------------------------
# 8. Multi-Observer Panel Consensus & The Grounding Firewall
