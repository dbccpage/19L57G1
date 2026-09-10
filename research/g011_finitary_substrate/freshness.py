"""Deterministic Address Freshness Allocator.

Endogenous deterministic allocation of fresh disjoint tree addresses
from an admitted registry without host pointers or randomness oracles.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from ordinals import Ordinal, Zero, Succ
from address import Address, Root, Child


def root_branch_index(addr: Address) -> Ordinal | None:
    """Extract the top-level branch ordinal under root, or None if root."""
    if addr.is_root():
        return None
    curr = addr
    while True:
        p = curr.parent()
        assert p is not None
        if p.is_root():
            return curr.branch_ordinal()
        curr = p


def max_branch_index(allocated: Sequence[Address]) -> Ordinal:
    """Compute the maximum top-level branch ordinal occurring in allocated addresses."""
    curr_max: Ordinal = Zero()
    found_any = False
    for a in allocated:
        br = root_branch_index(a)
        if br is not None:
            if not found_any or curr_max < br:
                curr_max = br
            found_any = True
    return curr_max


def has_branch(allocated: Sequence[Address]) -> bool:
    """Return True iff allocated contains any address branching from root."""
    return any(root_branch_index(a) is not None for a in allocated)


def fresh_index(allocated: Sequence[Address]) -> Ordinal:
    """Compute the deterministic fresh branch ordinal strictly exceeding all allocated branch ordinals."""
    if has_branch(allocated):
        return max_branch_index(allocated).succ()
    return Zero()


def fresh_address(allocated: Sequence[Address]) -> Address:
    """Generate a deterministic fresh address under root guaranteed not in allocated."""
    return Address.root().child(fresh_index(allocated))


@dataclass(frozen=True)
class AddressRegistry:
    """An immutable, endogenous registry of allocated tree addresses."""

    allocated: tuple[Address, ...] = ()
    count: Ordinal = Zero()

    @classmethod
    def empty(cls) -> AddressRegistry:
        """Construct an empty address registry."""
        return cls((), Zero())

    def allocate(self) -> tuple[AddressRegistry, Address]:
        """Deterministically allocate a fresh address, returning updated registry and the fresh address."""
        fresh = fresh_address(self.allocated)
        updated_reg = AddressRegistry(
            allocated=(fresh,) + self.allocated,
            count=self.count.succ(),
        )
        return updated_reg, fresh

    def contains(self, addr: Address) -> bool:
        """Check whether an address is already allocated."""
        return addr in self.allocated
