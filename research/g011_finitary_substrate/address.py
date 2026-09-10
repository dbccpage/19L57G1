"""Hierarchical Tree Addresses.

Inductive hierarchical tree addresses, depth metrics, prefix relations,
and sibling branch disjointness without host pointers or ambient memory.

AuthorityEffect: None.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
from ordinals import Ordinal, Zero, Succ


class Address(ABC):
    """Abstract base class for hierarchical tree addresses."""

    @abstractmethod
    def is_root(self) -> bool:
        """Return True iff this is the root address."""

    @abstractmethod
    def parent(self) -> Address | None:
        """Return the immediate structural parent address, or None for root."""

    @abstractmethod
    def branch_ordinal(self) -> Ordinal | None:
        """Return the branch ordinal from parent, or None for root."""

    @abstractmethod
    def depth(self) -> Ordinal:
        """Return endogenous depth from root as an Ordinal."""

    def child(self, branch: Ordinal) -> Address:
        """Extend this address by an ordinal branch."""
        if not isinstance(branch, Ordinal):
            raise TypeError(f"expected Ordinal branch, got {type(branch)}")
        return Child(self, branch)

    def is_prefix_of(self, other: Address) -> bool:
        """Return True iff this address is a prefix (ancestor or self) of other."""
        if not isinstance(other, Address):
            raise TypeError(f"expected Address, got {type(other)}")
        curr: Address | None = other
        while curr is not None:
            if self == curr:
                return True
            curr = curr.parent()
        return False

    def is_strict_prefix_of(self, other: Address) -> bool:
        """Return True iff this address is a strict prefix of other."""
        return self.is_prefix_of(other) and self != other

    def is_disjoint_from(self, other: Address) -> bool:
        """Return True iff neither address is a prefix of the other."""
        return not self.is_prefix_of(other) and not other.is_prefix_of(self)

    @classmethod
    def root(cls) -> Address:
        """Factory for root address."""
        return Root()

    def to_path(self) -> tuple[Ordinal, ...]:
        """Return path of branch ordinals from root."""
        segments: list[Ordinal] = []
        curr: Address | None = self
        while curr is not None and not curr.is_root():
            br = curr.branch_ordinal()
            assert br is not None
            segments.append(br)
            curr = curr.parent()
        return tuple(reversed(segments))

    @classmethod
    def from_path(cls, path: Sequence[Ordinal]) -> Address:
        """Construct an address by following a sequence of branch ordinals from root."""
        curr: Address = Root()
        for br in path:
            curr = curr.child(br)
        return curr


class Root(Address):
    """The root of the address tree."""

    _instance: Root | None = None

    def __new__(cls) -> Root:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_root(self) -> bool:
        return True

    def parent(self) -> Address | None:
        return None

    def branch_ordinal(self) -> Ordinal | None:
        return None

    def depth(self) -> Ordinal:
        return Zero()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Root)

    def __hash__(self) -> int:
        return hash((Root, ()))

    def __repr__(self) -> str:
        return "Address.root()"


class Child(Address):
    """A child address in the tree hierarchy."""

    __slots__ = ("_parent", "_branch", "_depth")

    def __init__(self, parent: Address, branch: Ordinal) -> None:
        if not isinstance(parent, Address):
            raise TypeError(f"expected Address parent, got {type(parent)}")
        if not isinstance(branch, Ordinal):
            raise TypeError(f"expected Ordinal branch, got {type(branch)}")
        self._parent = parent
        self._branch = branch
        self._depth = parent.depth().succ()

    def is_root(self) -> bool:
        return False

    def parent(self) -> Address | None:
        return self._parent

    def branch_ordinal(self) -> Ordinal | None:
        return self._branch

    def depth(self) -> Ordinal:
        return self._depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return False
        curr_self: Address | None = self
        curr_other: Address | None = other
        while curr_self is not None and curr_other is not None:
            if curr_self.is_root() != curr_other.is_root():
                return False
            if curr_self.is_root() and curr_other.is_root():
                return True
            if curr_self.branch_ordinal() != curr_other.branch_ordinal():
                return False
            curr_self = curr_self.parent()
            curr_other = curr_other.parent()
        return curr_self is None and curr_other is None

    def __hash__(self) -> int:
        return hash((Child, self.to_path()))

    def __repr__(self) -> str:
        return f"{self._parent!r}.child({self._branch!r})"
