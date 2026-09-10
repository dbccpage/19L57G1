"""M100: Internal Syntax, Renaming Functoriality & Capture-Free Substitution.

Constructive implementation of De Bruijn syntax, renaming functoriality,
and capture-free substitution without external freshness oracles.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Union


@dataclass(frozen=True)
class Var:
    index: int

    def __repr__(self) -> str:
        return f"Var({self.index})"


@dataclass(frozen=True)
class Lam:
    body: Term

    def __repr__(self) -> str:
        return f"Lam({self.body})"


@dataclass(frozen=True)
class App:
    fn: Term
    arg: Term

    def __repr__(self) -> str:
        return f"App({self.fn}, {self.arg})"


@dataclass(frozen=True)
class Const:
    val: int

    def __repr__(self) -> str:
        return f"Const({self.val})"


Term = Union[Var, Lam, App, Const]


def term_size(t: Term) -> int:
    """Compute structural size metric of term."""
    if isinstance(t, (Var, Const)):
        return 1
    elif isinstance(t, Lam):
        return 1 + term_size(t.body)
    elif isinstance(t, App):
        return 1 + term_size(t.fn) + term_size(t.arg)
    raise TypeError(f"Unknown term type: {type(t)}")


def lift_renaming(rho: Callable[[int], int]) -> Callable[[int], int]:
    """Lift a renaming function across a binder: variable 0 is untouched, others shifted."""
    def lifted(n: int) -> int:
        if n == 0:
            return 0
        return rho(n - 1) + 1
    return lifted


def rename(rho: Callable[[int], int], t: Term) -> Term:
    """Apply variable renaming to term."""
    if isinstance(t, Var):
        return Var(rho(t.index))
    elif isinstance(t, Const):
        return t
    elif isinstance(t, App):
        return App(rename(rho, t.fn), rename(rho, t.arg))
    elif isinstance(t, Lam):
        return Lam(rename(lift_renaming(rho), t.body))
    raise TypeError(f"Unknown term type: {type(t)}")


def lift_subst(sigma: Callable[[int], Term]) -> Callable[[int], Term]:
    """Lift a substitution across a binder."""
    def lifted(n: int) -> Term:
        if n == 0:
            return Var(0)
        return rename(lambda k: k + 1, sigma(n - 1))
    return lifted


def subst(sigma: Callable[[int], Term], t: Term) -> Term:
    """Apply capture-free parallel substitution to term."""
    if isinstance(t, Var):
        return sigma(t.index)
    elif isinstance(t, Const):
        return t
    elif isinstance(t, App):
        return App(subst(sigma, t.fn), subst(sigma, t.arg))
    elif isinstance(t, Lam):
        return Lam(subst(lift_subst(sigma), t.body))
    raise TypeError(f"Unknown term type: {type(t)}")


def subst_single(s: Term, t: Term) -> Term:
    """Apply single substitution t[s / 0]."""
    def sigma(n: int) -> Term:
        if n == 0:
            return s
        return Var(n - 1)
    return subst(sigma, t)


def id_renaming(n: int) -> int:
    return n


def id_subst(n: int) -> Term:
    return Var(n)
