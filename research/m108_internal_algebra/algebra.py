"""Target M108: General Internal Universal Algebra.

Constructive mathematical architecture for internal universal algebra:
1. Exact Number Carriers:
   - InternalInt: Arbitrary precision integer arithmetic with zero floating-point logic.
   - InternalRat: Exact fraction pair (p, q) with q > 0 and gcd(p, q) = 1.
2. Signatures and Equational Terms:
   - Signature: Mapping of operation symbols to arities.
   - Term: Abstract syntax tree (Var, Op) with evaluation, substitution, and variables.
   - Equation: Equational identity lhs = rhs with valuation satisfaction testing.
3. Internal Algebraic Structures:
   - Algebra: General algebraic structure with Signature, carrier, and interpretations.
   - Specific structures: Monoid, Group, Module over R, Ring / Associative Algebra.
4. Free Algebraic Constructions:
   - Free Monoid F_Mon(X): Words under concatenation, unit (), generator embedding η.
   - Free Module F_Mod(X, R): Formal linear combinations over commutative ring R (Z or Q).
   - Free Ring F_Ring(X, R): Monoid ring R[F_Mon(X)] with Cauchy multiplication.
5. Homomorphisms:
   - Structure-preserving maps between algebras of matching signature.
   - Kernel equivalence and image subalgebras.
6. Congruence Relations and Quotient Algebras:
   - Equivalence relations compatible with all signature operations.
   - Quotient algebras with operational closure.
   - Verification of representative independence across operations.
   - Factorization Theorem (Universal Mapping Property of Quotients) and arrow uniqueness.
7. Universal Arrows and Categorical Uniqueness:
   - Universal mapping properties for Free Monoids, Free Modules, and Free Rings.
   - Algorithmic uniqueness checking for universal arrows.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Callable, Dict, FrozenSet, Iterable, Iterator, List, Optional, Sequence, Set, Tuple, Union


# ==============================================================================
# 1. Exact Internal Arithmetic (Z and Q)
# ==============================================================================

@dataclass(frozen=True)
class InternalInt:
    """Exact constructive integer with zero floating-point logic."""
    val: int

    def __init__(self, val: Union[int, InternalInt]) -> None:
        if isinstance(val, InternalInt):
            object.__setattr__(self, "val", val.val)
        elif isinstance(val, int):
            object.__setattr__(self, "val", val)
        else:
            raise TypeError(f"InternalInt expects int, got {type(val).__name__}")

    def __add__(self, other: Union[InternalInt, int]) -> InternalInt:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return InternalInt(self.val + o)

    def __radd__(self, other: int) -> InternalInt:
        return self.__add__(other)

    def __sub__(self, other: Union[InternalInt, int]) -> InternalInt:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return InternalInt(self.val - o)

    def __rsub__(self, other: int) -> InternalInt:
        return InternalInt(int(other) - self.val)

    def __mul__(self, other: Union[InternalInt, int]) -> InternalInt:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return InternalInt(self.val * o)

    def __rmul__(self, other: int) -> InternalInt:
        return self.__mul__(other)

    def __neg__(self) -> InternalInt:
        return InternalInt(-self.val)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InternalInt):
            return self.val == other.val
        if isinstance(other, int):
            return self.val == other
        return False

    def __lt__(self, other: Union[InternalInt, int]) -> bool:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return self.val < o

    def __le__(self, other: Union[InternalInt, int]) -> bool:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return self.val <= o

    def __hash__(self) -> int:
        return hash(self.val)

    def __repr__(self) -> str:
        return f"InternalInt({self.val})"


@dataclass(frozen=True)
class InternalRat:
    """Exact constructive rational pair (num, den) with den > 0 and gcd(num, den) = 1."""
    num: int
    den: int

    def __init__(self, num: Union[int, InternalInt, InternalRat], den: Union[int, InternalInt] = 1) -> None:
        if isinstance(num, InternalRat):
            if den != 1:
                raise ValueError("Cannot specify second denominator when numerator is InternalRat")
            object.__setattr__(self, "num", num.num)
            object.__setattr__(self, "den", num.den)
            return

        n = num.val if isinstance(num, InternalInt) else int(num)
        d = den.val if isinstance(den, InternalInt) else int(den)
        if d == 0:
            raise ZeroDivisionError("Rational denominator cannot be zero")
        if d < 0:
            n = -n
            d = -d
        g = math.gcd(abs(n), d)
        object.__setattr__(self, "num", n // g)
        object.__setattr__(self, "den", d // g)

    @classmethod
    def zero(cls) -> InternalRat:
        return cls(0, 1)

    @classmethod
    def one(cls) -> InternalRat:
        return cls(1, 1)

    def is_zero(self) -> bool:
        return self.num == 0

    def __add__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return InternalRat(self.num * o.den + o.num * self.den, self.den * o.den)

    def __radd__(self, other: Union[InternalInt, int]) -> InternalRat:
        return self.__add__(other)

    def __sub__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return InternalRat(self.num * o.den - o.num * self.den, self.den * o.den)

    def __rsub__(self, other: Union[InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return o.__sub__(self)

    def __mul__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return InternalRat(self.num * o.num, self.den * o.den)

    def __rmul__(self, other: Union[InternalInt, int]) -> InternalRat:
        return self.__mul__(other)

    def __truediv__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        if o.num == 0:
            raise ZeroDivisionError("Division by zero rational")
        return InternalRat(self.num * o.den, self.den * o.num)

    def __neg__(self) -> InternalRat:
        return InternalRat(-self.num, self.den)

    def inv(self) -> InternalRat:
        if self.num == 0:
            raise ZeroDivisionError("Cannot invert zero rational")
        return InternalRat(self.den, self.num)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InternalRat):
            return self.num == other.num and self.den == other.den
        if isinstance(other, (InternalInt, int)):
            o = other.val if isinstance(other, InternalInt) else other
            return self.den == 1 and self.num == o
        return False

    def __lt__(self, other: Union[InternalRat, InternalInt, int]) -> bool:
        o = self._to_rat(other)
        return self.num * o.den < o.num * self.den

    def __le__(self, other: Union[InternalRat, InternalInt, int]) -> bool:
        o = self._to_rat(other)
        return self.num * o.den <= o.num * self.den

    def __hash__(self) -> int:
        return hash((self.num, self.den))

    def __repr__(self) -> str:
        return f"InternalRat({self.num}/{self.den})"

    @staticmethod
    def _to_rat(x: Union[InternalRat, InternalInt, int]) -> InternalRat:
        if isinstance(x, InternalRat):
            return x
        if isinstance(x, InternalInt):
            return InternalRat(x.val, 1)
        if isinstance(x, int):
            return InternalRat(x, 1)
        raise TypeError(f"Cannot convert {type(x).__name__} to InternalRat")


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


# ==============================================================================
# 4. Free Monoid Construction F_Mon(X)
# ==============================================================================

@dataclass(frozen=True)
class Word:
    """Element of a free monoid F_Mon(X) represented as a finite tuple of generators."""
    letters: Tuple[Any, ...]

    def __init__(self, letters: Iterable[Any] = ()) -> None:
        object.__setattr__(self, "letters", tuple(letters))

    @classmethod
    def unit(cls) -> Word:
        return cls(())

    @classmethod
    def generator(cls, x: Any) -> Word:
        return cls((x,))

    def __add__(self, other: Word) -> Word:
        if not isinstance(other, Word):
            return NotImplemented
        return Word(self.letters + other.letters)

    def __len__(self) -> int:
        return len(self.letters)

    def __repr__(self) -> str:
        if not self.letters:
            return "ε"
        return "".join(str(x) for x in self.letters)


class FreeMonoid:
    """Free Monoid F_Mon(X) generated by a set of symbols X."""

    def __init__(self, generators: Iterable[Any]) -> None:
        self.generators = frozenset(generators)
        self.signature = MONOID_SIGNATURE
        self.algebra = Algebra(
            name=f"F_Mon({sorted(str(g) for g in self.generators)})",
            signature=self.signature,
            interpretations={
                "e": lambda: Word.unit(),
                "mul": lambda w1, w2: w1 + w2,
            },
            carrier_predicate=self._is_valid_word,
        )

    def _is_valid_word(self, w: Any) -> bool:
        if not isinstance(w, Word):
            return False
        return all(letter in self.generators for letter in w.letters)

    def eta(self, x: Any) -> Word:
        """Canonical generator insertion arrow η : X -> F_Mon(X)."""
        if x not in self.generators:
            raise ValueError(f"Element {x} is not in generator set {self.generators}")
        return Word.generator(x)

    def lift(
        self,
        f: Callable[[Any], Any],
        target_unit: Any,
        target_mul: Callable[[Any, Any], Any],
    ) -> Callable[[Word], Any]:
        """Universal arrow lift f_hat : F_Mon(X) -> M.
        
        Given a set map f : X -> M where M is a monoid with target_unit and target_mul,
        constructs the unique monoid homomorphism f_hat extending f.
        """
        def f_hat(w: Word) -> Any:
            acc = target_unit
            for letter in w.letters:
                acc = target_mul(acc, f(letter))
            return acc

        return f_hat

    def verify_universal_mapping_property(
        self,
        f: Callable[[Any], Any],
        target_unit: Any,
        target_mul: Callable[[Any, Any], Any],
        sample_words: Sequence[Word],
    ) -> Dict[str, Any]:
        """Verify existence and uniqueness of the universal arrow for Free Monoid."""
        f_hat = self.lift(f, target_unit, target_mul)

        # 1. Generator agreement: f_hat(η(x)) == f(x)
        for gen in self.generators:
            eta_x = self.eta(gen)
            if f_hat(eta_x) != f(gen):
                return {
                    "holds": False,
                    "reason": f"Failed generator agreement at {gen}: {f_hat(eta_x)} != {f(gen)}",
                }

        # 2. Monoid homomorphism properties:
        # Unit preservation: f_hat(ε) == target_unit
        if f_hat(Word.unit()) != target_unit:
            return {"holds": False, "reason": "Failed unit preservation"}

        # Binary operation preservation: f_hat(w1 + w2) == target_mul(f_hat(w1), f_hat(w2))
        for w1 in sample_words:
            for w2 in sample_words:
                lhs = f_hat(w1 + w2)
                rhs = target_mul(f_hat(w1), f_hat(w2))
                if lhs != rhs:
                    return {
                        "holds": False,
                        "reason": f"Failed multiplication homomorphism on {w1}, {w2}: {lhs} != {rhs}",
                    }

        return {
            "holds": True,
            "generators_verified": len(self.generators),
            "sample_words_tested": len(sample_words),
        }

    def verify_arrow_uniqueness(
        self,
        f: Callable[[Any], Any],
        candidate_hom: Callable[[Word], Any],
        target_unit: Any,
        target_mul: Callable[[Any, Any], Any],
        test_words: Sequence[Word],
    ) -> bool:
        """Check uniqueness: if candidate_hom agrees on generators and is a hom,
        it must equal f_hat on all test words."""
        f_hat = self.lift(f, target_unit, target_mul)
        for w in test_words:
            if candidate_hom(w) != f_hat(w):
                return False
        return True


# ==============================================================================
# 5. Free Module / Abelian Group Construction F_Mod(X, R)
# ==============================================================================

Scalar = Union[InternalInt, InternalRat, int]


@dataclass(frozen=True)
class LinearCombination:
    """Formal finite linear combination sum_{x in X} c_x * x over a scalar ring R.
    
    Canonical representation: sorted tuple of (generator, coefficient) pairs
    where coefficient != 0. Zero is represented by the empty tuple ().
    """
    terms: Tuple[Tuple[Any, Any], ...]

    def __init__(self, terms: Union[Dict[Any, Any], Iterable[Tuple[Any, Any]]] = ()) -> None:
        mapping: Dict[Any, Any] = {}
        items = terms.items() if isinstance(terms, dict) else terms
        for k, v in items:
            c = self._canonical_coeff(v)
            if not self._is_zero_coeff(c):
                mapping[k] = mapping.get(k, self._zero_like(c)) + c

        # Filter zeros that cancelled out and sort by string representation of key
        cleaned = [
            (k, v) for k, v in mapping.items()
            if not self._is_zero_coeff(v)
        ]
        cleaned.sort(key=lambda item: str(item[0]))
        object.__setattr__(self, "terms", tuple(cleaned))

    @staticmethod
    def _canonical_coeff(c: Any) -> Any:
        if isinstance(c, int):
            return InternalInt(c)
        return c

    @staticmethod
    def _is_zero_coeff(c: Any) -> bool:
        if isinstance(c, InternalInt):
            return c.val == 0
        if isinstance(c, InternalRat):
            return c.is_zero()
        if isinstance(c, int):
            return c == 0
        return False

    @staticmethod
    def _zero_like(c: Any) -> Any:
        if isinstance(c, InternalRat):
            return InternalRat.zero()
        if isinstance(c, InternalInt):
            return InternalInt(0)
        return 0

    @classmethod
    def zero(cls) -> LinearCombination:
        return cls(())

    @classmethod
    def generator(cls, x: Any, coeff: Any = InternalInt(1)) -> LinearCombination:
        return cls([(x, coeff)])

    def coefficient(self, x: Any, default: Any = InternalInt(0)) -> Any:
        for k, v in self.terms:
            if k == x:
                return v
        return default

    def is_zero(self) -> bool:
        return len(self.terms) == 0

    def support(self) -> Set[Any]:
        return {k for k, _ in self.terms}

    def __add__(self, other: LinearCombination) -> LinearCombination:
        if not isinstance(other, LinearCombination):
            return NotImplemented
        combined: Dict[Any, Any] = dict(self.terms)
        for k, v in other.terms:
            combined[k] = combined.get(k, self._zero_like(v)) + v
        return LinearCombination(combined)

    def __sub__(self, other: LinearCombination) -> LinearCombination:
        if not isinstance(other, LinearCombination):
            return NotImplemented
        return self.__add__(-other)

    def __neg__(self) -> LinearCombination:
        return LinearCombination([(k, -v) for k, v in self.terms])

    def smul(self, scalar: Any) -> LinearCombination:
        sc = self._canonical_coeff(scalar)
        if self._is_zero_coeff(sc):
            return LinearCombination.zero()
        return LinearCombination([(k, sc * v) for k, v in self.terms])

    def __repr__(self) -> str:
        if not self.terms:
            return "0"
        parts = []
        for k, v in self.terms:
            parts.append(f"{v}·{k}")
        return " + ".join(parts)


class FreeModule:
    """Free R-Module F_Mod(X, R) generated by basis set X over scalar ring R (InternalInt or InternalRat)."""

    def __init__(self, generators: Iterable[Any], scalar_type: type = InternalInt) -> None:
        self.generators = frozenset(generators)
        self.scalar_type = scalar_type
        self.one_scalar = InternalRat.one() if scalar_type is InternalRat else InternalInt(1)
        self.zero_scalar = InternalRat.zero() if scalar_type is InternalRat else InternalInt(0)

    def eta(self, x: Any) -> LinearCombination:
        """Canonical basis injection arrow η : X -> F_Mod(X, R)."""
        if x not in self.generators:
            raise ValueError(f"Element {x} is not in basis set {self.generators}")
        return LinearCombination.generator(x, self.one_scalar)

    def lift(
        self,
        f: Callable[[Any], Any],
        target_zero: Any,
        target_add: Callable[[Any, Any], Any],
        target_smul: Callable[[Any, Any], Any],
    ) -> Callable[[LinearCombination], Any]:
        """Universal arrow lift f_hat : F_Mod(X, R) -> N.
        
        Given a set map f : X -> N into an R-module N, constructs the unique
        R-linear map f_hat extending f.
        """
        def f_hat(lc: LinearCombination) -> Any:
            res = target_zero
            for basis_elem, coeff in lc.terms:
                term_val = target_smul(coeff, f(basis_elem))
                res = target_add(res, term_val)
            return res

        return f_hat

    def verify_universal_mapping_property(
        self,
        f: Callable[[Any], Any],
        target_zero: Any,
        target_add: Callable[[Any, Any], Any],
        target_smul: Callable[[Any, Any], Any],
        sample_elements: Sequence[LinearCombination],
    ) -> Dict[str, Any]:
        """Verify universal mapping property for Free Module:
        1. Generator agreement: f_hat(η(x)) == f(x)
        2. R-linearity: f_hat(u + v) == f_hat(u) + f_hat(v)
        3. Scalar homogeneity: f_hat(r · u) == r · f_hat(u)
        """
        f_hat = self.lift(f, target_zero, target_add, target_smul)

        # 1. Generator agreement
        for gen in self.generators:
            eta_x = self.eta(gen)
            if f_hat(eta_x) != f(gen):
                return {
                    "holds": False,
                    "reason": f"Failed generator agreement on {gen}: {f_hat(eta_x)} != {f(gen)}",
                }

        # 2. Linearity: additivity
        for u in sample_elements:
            for v in sample_elements:
                lhs = f_hat(u + v)
                rhs = target_add(f_hat(u), f_hat(v))
                if lhs != rhs:
                    return {
                        "holds": False,
                        "reason": f"Failed additivity on {u}, {v}: {lhs} != {rhs}",
                    }

        # 3. Scalar homogeneity
        scalars = (
            [InternalInt(0), InternalInt(1), InternalInt(-2), InternalInt(3)]
            if self.scalar_type is InternalInt
            else [InternalRat.zero(), InternalRat.one(), InternalRat(-3, 2), InternalRat(5, 4)]
        )
        for u in sample_elements:
            for sc in scalars:
                lhs = f_hat(u.smul(sc))
                rhs = target_smul(sc, f_hat(u))
                if lhs != rhs:
                    return {
                        "holds": False,
                        "reason": f"Failed scalar homogeneity on {sc} · {u}: {lhs} != {rhs}",
                    }

        return {
            "holds": True,
            "generators_verified": len(self.generators),
            "sample_elements_tested": len(sample_elements),
        }

    def verify_arrow_uniqueness(
        self,
        f: Callable[[Any], Any],
        candidate_linear: Callable[[LinearCombination], Any],
        target_zero: Any,
        target_add: Callable[[Any, Any], Any],
        target_smul: Callable[[Any, Any], Any],
        test_elements: Sequence[LinearCombination],
    ) -> bool:
        """Check uniqueness of linear extension on basis."""
        f_hat = self.lift(f, target_zero, target_add, target_smul)
        return all(candidate_linear(elem) == f_hat(elem) for elem in test_elements)


# ==============================================================================
# 6. Free Ring / Associative Algebra Construction F_Ring(X, R)
# ==============================================================================

@dataclass(frozen=True)
class FreeRingElement:
    """Element of the free associative R-algebra R[F_Mon(X)] (monoid ring).
    
    Formal linear combination of words over X with coefficients in R.
    Multiplication is Cauchy convolution of word coefficients.
    """
    linear_comb: LinearCombination  # keys are Word instances

    def __init__(self, terms: Union[LinearCombination, Dict[Word, Any], Iterable[Tuple[Word, Any]]] = ()) -> None:
        if isinstance(terms, LinearCombination):
            object.__setattr__(self, "linear_comb", terms)
        else:
            object.__setattr__(self, "linear_comb", LinearCombination(terms))

    @classmethod
    def zero(cls) -> FreeRingElement:
        return cls(LinearCombination.zero())

    @classmethod
    def one(cls, scalar_type: type = InternalInt) -> FreeRingElement:
        unit_coeff = InternalRat.one() if scalar_type is InternalRat else InternalInt(1)
        return cls(LinearCombination.generator(Word.unit(), unit_coeff))

    @classmethod
    def generator(cls, x: Any, scalar_type: type = InternalInt) -> FreeRingElement:
        unit_coeff = InternalRat.one() if scalar_type is InternalRat else InternalInt(1)
        return cls(LinearCombination.generator(Word.generator(x), unit_coeff))

    def is_zero(self) -> bool:
        return self.linear_comb.is_zero()

    def __add__(self, other: FreeRingElement) -> FreeRingElement:
        if not isinstance(other, FreeRingElement):
            return NotImplemented
        return FreeRingElement(self.linear_comb + other.linear_comb)

    def __sub__(self, other: FreeRingElement) -> FreeRingElement:
        if not isinstance(other, FreeRingElement):
            return NotImplemented
        return FreeRingElement(self.linear_comb - other.linear_comb)

    def __neg__(self) -> FreeRingElement:
        return FreeRingElement(-self.linear_comb)

    def smul(self, scalar: Any) -> FreeRingElement:
        return FreeRingElement(self.linear_comb.smul(scalar))

    def __mul__(self, other: FreeRingElement) -> FreeRingElement:
        """Cauchy product: (sum a_w * w) * (sum b_v * v) = sum (a_w * b_v) * (w + v)."""
        if not isinstance(other, FreeRingElement):
            return NotImplemented
        if self.is_zero() or other.is_zero():
            return FreeRingElement.zero()

        result_dict: Dict[Word, Any] = {}
        for w1, c1 in self.linear_comb.terms:
            for w2, c2 in other.linear_comb.terms:
                prod_word = w1 + w2
                coeff_prod = c1 * c2
                result_dict[prod_word] = result_dict.get(prod_word, LinearCombination._zero_like(c1)) + coeff_prod

        return FreeRingElement(result_dict)

    def __repr__(self) -> str:
        if self.is_zero():
            return "0_Ring"
        parts = []
        for w, c in self.linear_comb.terms:
            parts.append(f"{c}·{w!r}")
        return " + ".join(parts)


class FreeRing:
    """Free Associative Algebra / Free Ring F_Ring(X, R) over commutative ring R."""

    def __init__(self, generators: Iterable[Any], scalar_type: type = InternalInt) -> None:
        self.generators = frozenset(generators)
        self.scalar_type = scalar_type
        self.signature = RING_SIGNATURE

    def eta(self, x: Any) -> FreeRingElement:
        """Generator inclusion arrow η : X -> F_Ring(X, R)."""
        if x not in self.generators:
            raise ValueError(f"Generator {x} not in basis set {self.generators}")
        return FreeRingElement.generator(x, self.scalar_type)

    def lift(
        self,
        f: Callable[[Any], Any],
        target_zero: Any,
        target_one: Any,
        target_add: Callable[[Any, Any], Any],
        target_mul: Callable[[Any, Any], Any],
        target_smul: Callable[[Any, Any], Any],
    ) -> Callable[[FreeRingElement], Any]:
        """Universal arrow lift f_hat : F_Ring(X, R) -> A into an R-algebra A."""
        # First lift monoid words into A
        def word_lift(w: Word) -> Any:
            acc = target_one
            for letter in w.letters:
                acc = target_mul(acc, f(letter))
            return acc

        def f_hat(r_elem: FreeRingElement) -> Any:
            acc = target_zero
            for word, coeff in r_elem.linear_comb.terms:
                w_val = word_lift(word)
                scaled = target_smul(coeff, w_val)
                acc = target_add(acc, scaled)
            return acc

        return f_hat

    def verify_universal_mapping_property(
        self,
        f: Callable[[Any], Any],
        target_zero: Any,
        target_one: Any,
        target_add: Callable[[Any, Any], Any],
        target_mul: Callable[[Any, Any], Any],
        target_smul: Callable[[Any, Any], Any],
        sample_elements: Sequence[FreeRingElement],
    ) -> Dict[str, Any]:
        """Verify universal mapping property for Free Ring."""
        f_hat = self.lift(f, target_zero, target_one, target_add, target_mul, target_smul)

        # 1. Generator agreement
        for gen in self.generators:
            eta_x = self.eta(gen)
            if f_hat(eta_x) != f(gen):
                return {
                    "holds": False,
                    "reason": f"Failed generator agreement on {gen}: {f_hat(eta_x)} != {f(gen)}",
                }

        # 2. Ring homomorphisms: zero and one preservation
        if f_hat(FreeRingElement.zero()) != target_zero:
            return {"holds": False, "reason": "Failed zero preservation"}
        if f_hat(FreeRingElement.one(self.scalar_type)) != target_one:
            return {"holds": False, "reason": "Failed one preservation"}

        # 3. Additive and Multiplicative homomorphisms
        for u in sample_elements:
            for v in sample_elements:
                if f_hat(u + v) != target_add(f_hat(u), f_hat(v)):
                    return {"holds": False, "reason": f"Failed addition hom on {u}, {v}"}
                if f_hat(u * v) != target_mul(f_hat(u), f_hat(v)):
                    return {"holds": False, "reason": f"Failed multiplication hom on {u}, {v}"}

        return {
            "holds": True,
            "generators_verified": len(self.generators),
            "sample_elements_tested": len(sample_elements),
        }


# ==============================================================================
# 7. Internal Homomorphisms
# ==============================================================================

class Homomorphism:
    """Homomorphism f : A -> B between internal algebras of the same signature."""

    def __init__(
        self,
        source: Algebra,
        target: Algebra,
        mapping: Callable[[Any], Any],
        name: str = "hom",
    ) -> None:
        if source.signature.operations != target.signature.operations:
            raise ValueError("Source and target algebras must have identical signatures")
        self.source = source
        self.target = target
        self.mapping = mapping
        self.name = name

    def __call__(self, element: Any) -> Any:
        return self.mapping(element)

    def preserves_operation(self, symbol: str, sample_tuples: Sequence[Tuple[Any, ...]]) -> bool:
        """Verify f(op_A(x_1, ..., x_k)) == op_B(f(x_1), ..., f(x_k))."""
        for args in sample_tuples:
            lhs = self.mapping(self.source.interpret(symbol, *args))
            mapped_args = [self.mapping(a) for a in args]
            rhs = self.target.interpret(symbol, *mapped_args)
            if lhs != rhs:
                return False
        return True

    def compose(self, other: Homomorphism) -> Homomorphism:
        """Composite homomorphism (self o other) : other.source -> self.target."""
        if other.target != self.source:
            raise ValueError("Target of first homomorphism must match source of second")
        return Homomorphism(
            source=other.source,
            target=self.target,
            mapping=lambda x: self.mapping(other.mapping(x)),
            name=f"({self.name} ∘ {other.name})",
        )

    def kernel_relation(self) -> Callable[[Any, Any], bool]:
        """Kernel equivalence relation: x ~_ker y iff f(x) == f(y)."""
        return lambda x, y: bool(self.mapping(x) == self.mapping(y))


# ==============================================================================
# 8. Congruence Relations and Quotient Algebras
# ==============================================================================

class CongruenceRelation:
    """Equivalence relation on an algebra that is a congruence across all signature operations."""

    def __init__(
        self,
        algebra: Algebra,
        rel: Callable[[Any, Any], bool],
        name: str = "congruence",
    ) -> None:
        self.algebra = algebra
        self.rel = rel
        self.name = name

    def are_equivalent(self, x: Any, y: Any) -> bool:
        return bool(self.rel(x, y))

    def verify_congruence_axioms(
        self,
        samples: Sequence[Any],
        op_sample_tuples: Dict[str, Sequence[Tuple[Any, ...]]],
    ) -> Dict[str, Any]:
        """Verify reflexivity, symmetry, transitivity, and operational compatibility."""
        # 1. Reflexivity: x ~ x
        for x in samples:
            if not self.rel(x, x):
                return {"valid": False, "failure": f"Reflexivity failed at {x}"}

        # 2. Symmetry: x ~ y => y ~ x
        for x in samples:
            for y in samples:
                if self.rel(x, y) and not self.rel(y, x):
                    return {"valid": False, "failure": f"Symmetry failed at ({x}, {y})"}

        # 3. Transitivity: x ~ y and y ~ z => x ~ z
        for x in samples:
            for y in samples:
                if self.rel(x, y):
                    for z in samples:
                        if self.rel(y, z) and not self.rel(x, z):
                            return {"valid": False, "failure": f"Transitivity failed at ({x}, {y}, {z})"}

        # 4. Operational Compatibility
        # If x_i ~ y_i for all i, then op(x_1, ..., x_k) ~ op(y_1, ..., y_k)
        for sym, tuples in op_sample_tuples.items():
            for t1 in tuples:
                for t2 in tuples:
                    if len(t1) == len(t2) and all(self.rel(a, b) for a, b in zip(t1, t2)):
                        op_t1 = self.algebra.interpret(sym, *t1)
                        op_t2 = self.algebra.interpret(sym, *t2)
                        if not self.rel(op_t1, op_t2):
                            return {
                                "valid": False,
                                "failure": f"Operation compatibility failed on '{sym}': {t1} ~ {t2} but {op_t1} !~ {op_t2}",
                            }

        return {"valid": True, "samples_tested": len(samples)}


@dataclass(frozen=True)
class EquivalenceClass:
    """Canonical representation of an equivalence class in a quotient algebra."""
    canonical_representative: Any
    class_id: int

    def __repr__(self) -> str:
        return f"[{self.canonical_representative}]"


class QuotientAlgebra:
    """Quotient algebra A / ~ formed by factoring an algebra through a congruence relation."""

    def __init__(
        self,
        base_algebra: Algebra,
        congruence: CongruenceRelation,
        canonicalizer: Callable[[Any], Any],
        name: Optional[str] = None,
    ) -> None:
        self.base_algebra = base_algebra
        self.congruence = congruence
        self.canonicalizer = canonicalizer
        self.name = name or f"({base_algebra.name} / {congruence.name})"
        self.signature = base_algebra.signature

        # Build quotient interpretations
        q_ops: Dict[str, Callable[..., Any]] = {}
        for sym, arity in self.signature.operations.items():
            q_ops[sym] = self._make_quotient_op(sym, arity)

        self.algebra = Algebra(
            name=self.name,
            signature=self.signature,
            interpretations=q_ops,
        )

    def _make_quotient_op(self, sym: str, arity: int) -> Callable[..., Any]:
        if arity == 0:
            def nullary_op() -> Any:
                val = self.base_algebra.interpret(sym)
                return self.canonicalizer(val)
            return nullary_op

        def n_ary_op(*q_args: Any) -> Any:
            # Evaluate using canonical representatives
            base_res = self.base_algebra.interpret(sym, *q_args)
            return self.canonicalizer(base_res)

        return n_ary_op

    def pi(self, x: Any) -> Any:
        """Canonical projection homomorphism π : A -> A / ~."""
        return self.canonicalizer(x)

    def check_representative_independence(
        self,
        symbol: str,
        equivalent_input_pairs: Sequence[Tuple[Tuple[Any, ...], Tuple[Any, ...]]],
    ) -> bool:
        """Demonstrate operational closure and representative independence:
        If x_i ~ y_i, then pi(op(x_1, ..., x_k)) == pi(op(y_1, ..., y_k)).
        """
        for t1, t2 in equivalent_input_pairs:
            res1 = self.base_algebra.interpret(symbol, *t1)
            res2 = self.base_algebra.interpret(symbol, *t2)
            if self.pi(res1) != self.pi(res2):
                return False
        return True


# ==============================================================================
# 9. Factorization Theorem & Universal Mapping Properties of Quotients
# ==============================================================================

def quotient_factorization(
    h: Homomorphism,
    quotient: QuotientAlgebra,
) -> Homomorphism:
    """Universal Factorization Theorem for Quotient Algebras (First Isomorphism / UMP).
    
    Given a homomorphism h : A -> B that is constant on congruence classes
    (i.e. x ~ y implies h(x) == h(y)), construct the unique induced homomorphism
    h_bar : A / ~ -> B such that h_bar o pi == h.
    """
    def h_bar_map(q_elem: Any) -> Any:
        # Evaluate on the representative
        return h.mapping(q_elem)

    return Homomorphism(
        source=quotient.algebra,
        target=h.target,
        mapping=h_bar_map,
        name=f"({h.name}_bar)",
    )


def verify_quotient_factorization_uniqueness(
    h: Homomorphism,
    quotient: QuotientAlgebra,
    candidate_h_bar: Callable[[Any], Any],
    sample_elements: Sequence[Any],
) -> bool:
    """Verify uniqueness: if candidate o pi == h, then candidate must equal h_bar."""
    h_bar = quotient_factorization(h, quotient)
    for x in sample_elements:
        q = quotient.pi(x)
        if candidate_h_bar(q) != h_bar(q):
            return False
    return True
