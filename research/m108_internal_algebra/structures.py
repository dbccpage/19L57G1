"""Signatures, terms, and the generic Algebra carrier for M108."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


# ==============================================================================
# 2. Algebraic Signatures and Equational Terms
# ==============================================================================

@dataclass(frozen=True)
class Signature:
    """Algebraic signature assigning non-negative arities to operation symbols."""
    operations: Dict[str, int]

    def __post_init__(self) -> None:
        for symbol, arity in self.operations.items():
            if not isinstance(symbol, str) or not symbol:
                raise ValueError("Operation symbol must be a non-empty string")
            if not isinstance(arity, int) or arity < 0:
                raise ValueError(f"Arity for '{symbol}' must be a non-negative integer, got {arity}")

    def arity(self, symbol: str) -> int:
        if symbol not in self.operations:
            raise KeyError(f"Symbol '{symbol}' not in signature")
        return self.operations[symbol]

    def has_symbol(self, symbol: str) -> bool:
        return symbol in self.operations

    def __contains__(self, symbol: str) -> bool:
        return symbol in self.operations


# Common standard signatures
MONOID_SIGNATURE = Signature({"e": 0, "mul": 2})
GROUP_SIGNATURE = Signature({"e": 0, "mul": 2, "inv": 1})
RING_SIGNATURE = Signature({"zero": 0, "add": 2, "neg": 1, "one": 0, "mul": 2})


class Term:
    """Abstract base class for equational terms."""

    def eval(self, algebra: Algebra, valuation: Dict[str, Any]) -> Any:
        raise NotImplementedError

    def substitute(self, subst: Dict[str, Term]) -> Term:
        raise NotImplementedError

    def variables(self) -> Set[str]:
        raise NotImplementedError


@dataclass(frozen=True)
class Var(Term):
    """Variable term."""
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Variable name must be non-empty string")

    def eval(self, algebra: Algebra, valuation: Dict[str, Any]) -> Any:
        if self.name not in valuation:
            raise KeyError(f"Variable '{self.name}' unbound in valuation")
        return valuation[self.name]

    def substitute(self, subst: Dict[str, Term]) -> Term:
        return subst.get(self.name, self)

    def variables(self) -> Set[str]:
        return {self.name}

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Op(Term):
    """Operation application term."""
    symbol: str
    args: Tuple[Term, ...]

    def __init__(self, symbol: str, *args: Term) -> None:
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "args", tuple(args))

    def eval(self, algebra: Algebra, valuation: Dict[str, Any]) -> Any:
        sig = algebra.signature
        if not sig.has_symbol(self.symbol):
            raise ValueError(f"Symbol '{self.symbol}' not supported by algebra signature")
        expected_arity = sig.arity(self.symbol)
        if len(self.args) != expected_arity:
            raise ValueError(
                f"Symbol '{self.symbol}' requires arity {expected_arity}, got {len(self.args)}"
            )
        eval_args = [arg.eval(algebra, valuation) for arg in self.args]
        return algebra.interpret(self.symbol, *eval_args)

    def substitute(self, subst: Dict[str, Term]) -> Term:
        return Op(self.symbol, *(arg.substitute(subst) for arg in self.args))

    def variables(self) -> Set[str]:
        res: Set[str] = set()
        for a in self.args:
            res.update(a.variables())
        return res

    def __repr__(self) -> str:
        if not self.args:
            return f"{self.symbol}()"
        args_str = ", ".join(repr(a) for a in self.args)
        return f"{self.symbol}({args_str})"


@dataclass(frozen=True)
class Equation:
    """Equational identity between two terms: lhs = rhs."""
    lhs: Term
    rhs: Term

    def variables(self) -> Set[str]:
        return self.lhs.variables() | self.rhs.variables()

    def satisfied_under(self, algebra: Algebra, valuation: Dict[str, Any]) -> bool:
        v_lhs = self.lhs.eval(algebra, valuation)
        v_rhs = self.rhs.eval(algebra, valuation)
        return bool(v_lhs == v_rhs)

    def holds_for_valuations(self, algebra: Algebra, valuations: Iterable[Dict[str, Any]]) -> bool:
        return all(self.satisfied_under(algebra, v) for v in valuations)

    def __repr__(self) -> str:
        return f"{self.lhs!r} ≈ {self.rhs!r}"


# ==============================================================================
# 3. Internal Algebras
# ==============================================================================

class Algebra:
    """Universal algebraic structure over an explicit Signature."""

    def __init__(
        self,
        name: str,
        signature: Signature,
        interpretations: Dict[str, Callable[..., Any]],
        carrier_predicate: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        self.name = name
        self.signature = signature
        self._interpretations = dict(interpretations)
        self.carrier_predicate = carrier_predicate or (lambda x: True)

        for sym in signature.operations:
            if sym not in self._interpretations:
                raise ValueError(f"Missing interpretation for signature symbol '{sym}'")

    def interpret(self, symbol: str, *args: Any) -> Any:
        if symbol not in self._interpretations:
            raise KeyError(f"Symbol '{symbol}' has no interpretation in algebra '{self.name}'")
        expected_arity = self.signature.arity(symbol)
        if len(args) != expected_arity:
            raise ValueError(f"Symbol '{symbol}' requires {expected_arity} arguments, got {len(args)}")
        return self._interpretations[symbol](*args)

    def contains(self, element: Any) -> bool:
        return bool(self.carrier_predicate(element))

    def __repr__(self) -> str:
        return f"Algebra({self.name}, signature={list(self.signature.operations.keys())})"


