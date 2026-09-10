"""Formal definitions of computational capabilities and capability profiles for G010.

AuthorityEffect: None.
Reference: Genesis Research Program - G010 Semantic Primitive Removal.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Sequence


class Capability(Enum):
    """Primitive computational capabilities subject to genuine semantic removal."""

    BRANCHING = "BRANCHING"
    MEMORY_RETENTION = "MEMORY_RETENTION"
    ADDRESS_ALLOCATION = "ADDRESS_ALLOCATION"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class CapabilityProfile:
    """Immutable set of active capabilities defining an execution regime."""

    active: frozenset[Capability]

    def has(self, cap: Capability) -> bool:
        """Check whether a capability is present in the profile."""
        return cap in self.active

    @property
    def has_branching(self) -> bool:
        return Capability.BRANCHING in self.active

    @property
    def has_memory(self) -> bool:
        return Capability.MEMORY_RETENTION in self.active

    @property
    def has_alloc(self) -> bool:
        return Capability.ADDRESS_ALLOCATION in self.active

    def remove(self, cap: Capability) -> CapabilityProfile:
        """Return a new profile with the designated capability physically excluded."""
        return CapabilityProfile(self.active - {cap})

    def add(self, cap: Capability) -> CapabilityProfile:
        """Return a new profile with the designated capability included."""
        return CapabilityProfile(self.active | {cap})

    def is_subset_of(self, other: CapabilityProfile) -> bool:
        return self.active.issubset(other.active)


# Standard canonical profiles
FULL_PROFILE = CapabilityProfile(
    frozenset(
        {
            Capability.BRANCHING,
            Capability.MEMORY_RETENTION,
            Capability.ADDRESS_ALLOCATION,
        }
    )
)

WITHOUT_BRANCH = FULL_PROFILE.remove(Capability.BRANCHING)
WITHOUT_MEMORY = FULL_PROFILE.remove(Capability.MEMORY_RETENTION)
WITHOUT_ALLOC = FULL_PROFILE.remove(Capability.ADDRESS_ALLOCATION)
MINIMAL_PROFILE = CapabilityProfile(frozenset())


@dataclass(frozen=True)
class PublicView:
    """Frozen shared observation interface across all execution systems.

    Invariant under capability restriction.
    """

    output_tape: tuple[int, ...]
    steps: int
    halted: bool
    status: str
    error: str | None = None

    def equals(self, other: PublicView) -> bool:
        """Compare public observations for observational equivalence."""
        return (
            self.output_tape == other.output_tape
            and self.halted == other.halted
            and self.status == other.status
        )


@dataclass(frozen=True)
class Task:
    """A computational probe task evaluated strictly through the shared PublicView."""

    name: str
    description: str
    required_capabilities: frozenset[Capability]
    test_inputs: tuple[tuple[int, ...], ...]
    validator: Callable[[tuple[PublicView, ...]], bool]
    obstruction_witness: Callable[[tuple[PublicView, ...]], str]
