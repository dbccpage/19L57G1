"""Target M108: General Internal Universal Algebra.

Exact Z/Q carriers, signatures, free constructions, and quotient factorization.
Kernels live in arithmetic.py, structures.py, free.py, and quotients.py.
"""

from __future__ import annotations

from arithmetic import InternalInt, InternalRat
from structures import (
    Algebra,
    Equation,
    GROUP_SIGNATURE,
    MONOID_SIGNATURE,
    Op,
    RING_SIGNATURE,
    Signature,
    Term,
    Var,
)
from free import (
    FreeModule,
    FreeMonoid,
    FreeRing,
    FreeRingElement,
    LinearCombination,
    Word,
)
from quotients import (
    CongruenceRelation,
    Homomorphism,
    QuotientAlgebra,
    quotient_factorization,
    verify_quotient_factorization_uniqueness,
)

__all__ = [
    'Algebra', 'CongruenceRelation', 'Equation', 'FreeModule', 'FreeMonoid',
    'FreeRing', 'FreeRingElement', 'GROUP_SIGNATURE', 'Homomorphism',
    'InternalInt', 'InternalRat', 'LinearCombination', 'MONOID_SIGNATURE',
    'Op', 'QuotientAlgebra', 'RING_SIGNATURE', 'Signature', 'Term', 'Var',
    'Word', 'quotient_factorization', 'verify_quotient_factorization_uniqueness',
]
