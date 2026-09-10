"""M102: Resource Pricing & Structural Rules.

Constructive implementation of priced structural rules (exchange, weakening, contraction)
and copy-safe modality !A (Bang) with hierarchical address provenance tracking.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union
from logic import Formula, Derivation


@dataclass(frozen=True)
class RootAddress:
    id: int

    def __repr__(self) -> str:
        return f"Root({self.id})"


@dataclass(frozen=True)
class ChildAddress:
    parent: Address
    branch: int

    def __repr__(self) -> str:
        return f"Child({self.parent}, {self.branch})"


Address = Union[RootAddress, ChildAddress]


def address_origin(addr: Address) -> int:
    """Extract root origin identifier from address path."""
    curr = addr
    while isinstance(curr, ChildAddress):
        curr = curr.parent
    return curr.id


def address_depth(addr: Address) -> int:
    """Compute depth of address path from root."""
    d = 0
    curr = addr
    while isinstance(curr, ChildAddress):
        d += 1
        curr = curr.parent
    return d


@dataclass(frozen=True)
class TaggedFormula:
    addr: Address
    form: Formula

    def __repr__(self) -> str:
        return f"[{self.addr}]:{self.form}"


def duplicate_bang(parent: Address, form: Formula) -> tuple[TaggedFormula, TaggedFormula]:
    """Copy-safe duplication of a bang modality resource into two distinct branches."""
    c0 = TaggedFormula(ChildAddress(parent, 0), form)
    c1 = TaggedFormula(ChildAddress(parent, 1), form)
    return c0, c1


@dataclass(frozen=True)
class CostModel:
    cost_ex: int = 1
    cost_weak: int = 1
    cost_cont: int = 2


@dataclass
class PricedDerivation:
    rule: str
    structural_cost: int
    context: list[Formula]
    conclusion: Formula
    subderivs: list[PricedDerivation]


def priced_id(a: Formula, cm: CostModel) -> PricedDerivation:
    return PricedDerivation("id", 0, [a], a, [])


def priced_exchange(d: PricedDerivation, idx: int, cm: CostModel) -> PricedDerivation:
    """Exchange adjacent formulas at idx and idx + 1."""
    assert 0 <= idx < len(d.context) - 1
    new_ctx = list(d.context)
    new_ctx[idx], new_ctx[idx + 1] = new_ctx[idx + 1], new_ctx[idx]
    return PricedDerivation("exchange", d.structural_cost + cm.cost_ex, new_ctx, d.conclusion, [d])


def priced_weakening(d: PricedDerivation, f: Formula, idx: int, cm: CostModel) -> PricedDerivation:
    """Insert unused formula f at idx."""
    new_ctx = d.context[:idx] + [f] + d.context[idx:]
    return PricedDerivation("weakening", d.structural_cost + cm.cost_weak, new_ctx, d.conclusion, [d])


def priced_contraction(d: PricedDerivation, idx: int, cm: CostModel) -> PricedDerivation:
    """Contract two adjacent identical formulas at idx, idx + 1 into one."""
    assert 0 <= idx < len(d.context) - 1
    assert d.context[idx] == d.context[idx + 1]
    new_ctx = d.context[:idx] + [d.context[idx]] + d.context[idx + 2:]
    return PricedDerivation("contraction", d.structural_cost + cm.cost_cont, new_ctx, d.conclusion, [d])
