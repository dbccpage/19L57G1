"""M101: Resource-Sensitive Consequence & Operational Logic.

Constructive implementation of substructural sequent calculus, cut reductions,
operational phase-space valuation semantics, and non-triviality verification.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Union


@dataclass(frozen=True)
class Atom:
    id: int

    def __repr__(self) -> str:
        return f"Atom({self.id})"


@dataclass(frozen=True)
class One:
    def __repr__(self) -> str:
        return "One"


@dataclass(frozen=True)
class Tensor:
    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ⊗ {self.right})"


@dataclass(frozen=True)
class Lolli:
    ante: Formula
    succ: Formula

    def __repr__(self) -> str:
        return f"({self.ante} ⊸ {self.succ})"


@dataclass(frozen=True)
class WithF:
    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} & {self.right})"


@dataclass(frozen=True)
class PlusF:
    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ⊕ {self.right})"


@dataclass(frozen=True)
class Bang:
    sub: Formula

    def __repr__(self) -> str:
        return f"!({self.sub})"


@dataclass(frozen=True)
class Bot:
    def __repr__(self) -> str:
        return "Bot"


Formula = Union[Atom, One, Tensor, Lolli, WithF, PlusF, Bang, Bot]


def formula_size(f: Formula) -> int:
    """Structural size metric of formulas."""
    if isinstance(f, (Atom, One, Bot)):
        return 1
    elif isinstance(f, Bang):
        return 1 + formula_size(f.sub)
    elif isinstance(f, Lolli):
        return 1 + formula_size(f.ante) + formula_size(f.succ)
    elif isinstance(f, (Tensor, WithF, PlusF)):
        return 1 + formula_size(f.left) + formula_size(f.right)
    raise TypeError(f"Unknown formula type: {type(f)}")


# ---------------------------------------------------------------------------
# Operational Valuation / Phase-Space Semantics
# ---------------------------------------------------------------------------

def eval_formula(v: Callable[[int, int], bool], f: Formula, r: int, max_bound: int = 20) -> bool:
    """Evaluate whether formula f is satisfied with consumable resource r."""
    if isinstance(f, Atom):
        return v(f.id, r)
    elif isinstance(f, One):
        return r == 0
    elif isinstance(f, Bot):
        return False
    elif isinstance(f, Bang):
        return eval_formula(v, f.sub, r, max_bound)
    elif isinstance(f, Tensor):
        for r1 in range(r + 1):
            r2 = r - r1
            if eval_formula(v, f.left, r1, max_bound) and eval_formula(v, f.right, r2, max_bound):
                return True
        return False
    elif isinstance(f, Lolli):
        for s in range(max_bound + 1):
            if eval_formula(v, f.ante, s, max_bound):
                if not eval_formula(v, f.succ, r + s, max_bound):
                    return False
        return True
    elif isinstance(f, WithF):
        return eval_formula(v, f.left, r, max_bound) and eval_formula(v, f.right, r, max_bound)
    elif isinstance(f, PlusF):
        return eval_formula(v, f.left, r, max_bound) or eval_formula(v, f.right, r, max_bound)
    raise TypeError(f"Unknown formula: {f}")


def eval_context(v: Callable[[int, int], bool], ctx: list[Formula], r: int, max_bound: int = 20) -> bool:
    """Evaluate whether context multiset is satisfied with resource r."""
    if not ctx:
        return r == 0
    first, rest = ctx[0], ctx[1:]
    for r1 in range(r + 1):
        r2 = r - r1
        if eval_formula(v, first, r1, max_bound) and eval_context(v, rest, r2, max_bound):
            return True
    return False


# ---------------------------------------------------------------------------
# Sequent Derivations and Cut Elimination Reductions
# ---------------------------------------------------------------------------

@dataclass
class Derivation:
    rule: str
    premises: list[Derivation]
    context: list[Formula]
    conclusion: Formula


def d_id(a: Formula) -> Derivation:
    return Derivation("id", [], [a], a)


def d_one_r() -> Derivation:
    return Derivation("one_R", [], [], One())


def d_one_l(d: Derivation) -> Derivation:
    return Derivation("one_L", [d], [One()] + d.context, d.conclusion)


def d_tensor_r(d1: Derivation, d2: Derivation) -> Derivation:
    return Derivation("tensor_R", [d1, d2], d1.context + d2.context, Tensor(d1.conclusion, d2.conclusion))


def d_tensor_l(d: Derivation) -> Derivation:
    assert len(d.context) >= 2, "Tensor-L requires at least 2 formulas in context"
    a, b = d.context[0], d.context[1]
    rest = d.context[2:]
    return Derivation("tensor_L", [d], [Tensor(a, b)] + rest, d.conclusion)


def d_lolli_r(d: Derivation) -> Derivation:
    assert len(d.context) >= 1, "Lolli-R requires antecedent in context"
    a = d.context[0]
    rest = d.context[1:]
    return Derivation("lolli_R", [d], rest, Lolli(a, d.conclusion))


def d_lolli_l(d1: Derivation, d2: Derivation) -> Derivation:
    assert len(d2.context) >= 1, "Lolli-L requires succedent in second context"
    b = d2.context[0]
    rest2 = d2.context[1:]
    return Derivation("lolli_L", [d1, d2], [Lolli(d1.conclusion, b)] + d1.context + rest2, d2.conclusion)


def d_cut(d1: Derivation, d2: Derivation, idx: int) -> Derivation:
    """Cut d1.conclusion into d2 at position idx."""
    assert d2.context[idx] == d1.conclusion, f"Cut mismatch: {d2.context[idx]} != {d1.conclusion}"
    new_ctx = d2.context[:idx] + d1.context + d2.context[idx + 1:]
    return Derivation("cut", [d1, d2], new_ctx, d2.conclusion)


def reduce_tensor_cut(dA: Derivation, dB: Derivation, dC: Derivation) -> Derivation:
    """Principal reduction: cut(tensor_R(dA, dB), tensor_L(dC)) -> cut(dB, cut(dA, dC))."""
    # dC context is [A, B] + rest
    d1 = d_cut(dA, dC, 0) # yields dA.ctx + [B] + rest
    # find position of B in d1.context
    idx_B = len(dA.context)
    d2 = d_cut(dB, d1, idx_B) # yields dA.ctx + dB.ctx + rest
    return d2


def reduce_lolli_cut(dAB: Derivation, dA: Derivation, dBC: Derivation) -> Derivation:
    """Principal reduction: cut(lolli_R(dAB), lolli_L(dA, dBC)) -> cut(cut(dA, dAB), dBC)."""
    # dAB context is [A] + rest1, conclusion is B
    # dA context is ctxA, conclusion is A
    d_mid = d_cut(dA, dAB, 0) # ctxA + rest1 |- B
    # dBC context is [B] + rest2, conclusion is C
    d_final = d_cut(d_mid, dBC, 0) # (ctxA + rest1) + rest2 |- C
    return d_final
