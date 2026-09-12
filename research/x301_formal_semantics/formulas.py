"""Operational formula AST for Target X301.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

@dataclass(frozen=True)
class Formula:
    """Base abstract syntax tree node for represented operational formulas."""
    pass


@dataclass(frozen=True)
class Atom(Formula):
    """Atomic relation statement R(t_1, ..., t_k)."""

    rel: str
    args: tuple[str, ...]

    def __init__(self, rel: str, args: Sequence[str]):
        object.__setattr__(self, "rel", str(rel))
        object.__setattr__(self, "args", tuple(str(a) for a in args))

    def __repr__(self) -> str:
        args_str = ", ".join(self.args)
        return f"{self.rel}({args_str})"


@dataclass(frozen=True)
class Identity(Formula):
    """Internal identity statement left == right."""

    left: str
    right: str

    def __repr__(self) -> str:
        return f"({self.left} = {self.right})"


@dataclass(frozen=True)
class Conj(Formula):
    """Compositional conjunction left and right."""

    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ∧ {self.right})"


@dataclass(frozen=True)
class Disj(Formula):
    """Compositional disjunction left or right."""

    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ∨ {self.right})"


@dataclass(frozen=True)
class Imp(Formula):
    """Compositional intuitionistic implication ant -> con."""

    ant: Formula
    con: Formula

    @property
    def antecedent(self) -> Formula:
        return self.ant

    @property
    def consequent(self) -> Formula:
        return self.con

    def __repr__(self) -> str:
        return f"({self.ant} → {self.con})"


@dataclass(frozen=True)
class Neg(Formula):
    """Operational refusal / constructive negation: inner -> False."""

    inner: Formula

    def __repr__(self) -> str:
        return f"¬({self.inner})"


@dataclass(frozen=True)
class BoundedForall(Formula):
    """Bounded universal quantifier over a finite carrier sort: forall var in sort. body."""

    var: str
    sort: str
    body: Formula

    @property
    def domain_sort(self) -> str:
        return self.sort

    def __repr__(self) -> str:
        return f"(∀{self.var}:{self.sort}. {self.body})"


@dataclass(frozen=True)
class BoundedExists(Formula):
    """Bounded existential quantifier over a finite carrier sort: exists var in sort. body."""

    var: str
    sort: str
    body: Formula

    @property
    def domain_sort(self) -> str:
        return self.sort

    def __repr__(self) -> str:
        return f"(∃{self.var}:{self.sort}. {self.body})"


# Formula AST convenience constructors
def atom(rel: str, *args: str) -> Atom:
    return Atom(rel, args)

def eq(left: str, right: str) -> Identity:
    return Identity(left, right)

def conj(left: Formula, right: Formula) -> Conj:
    return Conj(left, right)

def disj(left: Formula, right: Formula) -> Disj:
    return Disj(left, right)

def imp(ant: Formula, con: Formula) -> Imp:
    return Imp(ant, con)

def neg(inner: Formula) -> Neg:
    return Neg(inner)

def forall(var: str, sort: str, body: Formula) -> BoundedForall:
    return BoundedForall(var, sort, body)

def exists(var: str, sort: str, body: Formula) -> BoundedExists:
    return BoundedExists(var, sort, body)
