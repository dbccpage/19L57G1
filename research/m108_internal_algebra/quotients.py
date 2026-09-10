"""Homomorphisms, congruences, and quotient factorization for M108."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, Set, Tuple

from structures import Algebra


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
