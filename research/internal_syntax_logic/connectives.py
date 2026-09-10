"""M103: Connectives by Universal Property & Refusal Separation.

Constructive implementation of:
1. Universal properties of internal products, coproducts, and internal homs.
2. Explicit ontological separation of operational refusal from constructive negation.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, Optional, TypeVar, Union

from logic import Bot, Formula, Lolli, PlusF, Tensor, WithF

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Categorical Proof-Terms / Morphisms
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MorId:
    obj: Formula

    def __repr__(self) -> str:
        return f"id({self.obj})"


@dataclass(frozen=True)
class MorComp:
    f: Mor
    g: Mor

    def __repr__(self) -> str:
        return f"({self.f} ⨟ {self.g})"


@dataclass(frozen=True)
class MorFst:
    a: Formula
    b: Formula

    def __repr__(self) -> str:
        return f"π1({self.a} & {self.b})"


@dataclass(frozen=True)
class MorSnd:
    a: Formula
    b: Formula

    def __repr__(self) -> str:
        return f"π2({self.a} & {self.b})"


@dataclass(frozen=True)
class MorPair:
    f: Mor
    g: Mor

    def __repr__(self) -> str:
        return f"⟨{self.f}, {self.g}⟩"


@dataclass(frozen=True)
class MorInl:
    a: Formula
    b: Formula

    def __repr__(self) -> str:
        return f"ι1({self.a} ⊕ {self.b})"


@dataclass(frozen=True)
class MorInr:
    a: Formula
    b: Formula

    def __repr__(self) -> str:
        return f"ι2({self.a} ⊕ {self.b})"


@dataclass(frozen=True)
class MorCopair:
    f: Mor
    g: Mor

    def __repr__(self) -> str:
        return f"[{self.f}, {self.g}]"


@dataclass(frozen=True)
class MorTensor:
    f: Mor
    g: Mor

    def __repr__(self) -> str:
        return f"({self.f} ⊗ {self.g})"


@dataclass(frozen=True)
class MorEval:
    a: Formula
    b: Formula

    def __repr__(self) -> str:
        return f"eval({self.a} ⊸ {self.b})"


@dataclass(frozen=True)
class MorCurry:
    f: Mor

    def __repr__(self) -> str:
        return f"curry({self.f})"


Mor = Union[
    MorId, MorComp, MorFst, MorSnd, MorPair,
    MorInl, MorInr, MorCopair, MorTensor, MorEval, MorCurry
]


def simplify_morphism(m: Mor) -> Mor:
    """Normalize morphisms using categorical beta-reduction equations."""
    if isinstance(m, MorComp):
        f = simplify_morphism(m.f)
        g = simplify_morphism(m.g)
        # Identity elimination
        if isinstance(f, MorId):
            return g
        if isinstance(g, MorId):
            return f
        # Product beta-reduction: comp(pair(f1, g1), fst) -> f1
        if isinstance(f, MorPair) and isinstance(g, MorFst):
            return f.f
        # Product beta-reduction: comp(pair(f1, g1), snd) -> g1
        if isinstance(f, MorPair) and isinstance(g, MorSnd):
            return f.g
        # Coproduct beta-reduction: comp(inl, copair(f1, g1)) -> f1
        if isinstance(f, MorInl) and isinstance(g, MorCopair):
            return g.f
        # Coproduct beta-reduction: comp(inr, copair(f1, g1)) -> g1
        if isinstance(f, MorInr) and isinstance(g, MorCopair):
            return g.g
        # Internal Hom beta-reduction: comp(tensor(curry(f1), id), eval) -> f1
        if isinstance(f, MorTensor) and isinstance(f.f, MorCurry) and isinstance(g, MorEval):
            return f.f.f
        return MorComp(f, g)
    elif isinstance(m, MorPair):
        return MorPair(simplify_morphism(m.f), simplify_morphism(m.g))
    elif isinstance(m, MorCopair):
        return MorCopair(simplify_morphism(m.f), simplify_morphism(m.g))
    elif isinstance(m, MorTensor):
        return MorTensor(simplify_morphism(m.f), simplify_morphism(m.g))
    elif isinstance(m, MorCurry):
        return MorCurry(simplify_morphism(m.f))
    return m


# ---------------------------------------------------------------------------
# Ontological Separation: Refusal vs. Negation
# ---------------------------------------------------------------------------

class RefusalReason(Enum):
    PROTECTION_VIOLATION = auto()
    RESOURCE_EXHAUSTION = auto()
    CONTRACT_BOUNDARY = auto()
    DESIGNATED_PAIR_SEPARATION = auto()


@dataclass(frozen=True)
class StepSuccess(Generic[T]):
    state: T


@dataclass(frozen=True)
class StepRefusal:
    reason: RefusalReason


@dataclass(frozen=True)
class StepHalted:
    pass


StepOutcome = Union[StepSuccess[T], StepRefusal, StepHalted]


def neg(a: Formula) -> Formula:
    """Constructive linear negation: ¬A ≡ A ⊸ ⊥."""
    return Lolli(a, Bot())


def step_with_state_preservation(step_fn, state: T) -> T:
    """Execute machine step while preserving exact state on refusal or halt."""
    outcome = step_fn(state)
    if isinstance(outcome, StepSuccess):
        return outcome.state
    elif isinstance(outcome, StepRefusal):
        # Explicit refusal preserves state unmutated
        return state
    elif isinstance(outcome, StepHalted):
        return state
    raise TypeError(f"Unknown step outcome: {type(outcome)}")
