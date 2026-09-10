"""Unit tests for capability definitions and profiles in G010."""

from capability import (
    Capability,
    CapabilityProfile,
    FULL_PROFILE,
    WITHOUT_BRANCH,
    WITHOUT_MEMORY,
    WITHOUT_ALLOC,
    MINIMAL_PROFILE,
    PublicView,
)


def test_capability_enumeration() -> None:
    caps = {Capability.BRANCHING, Capability.MEMORY_RETENTION, Capability.ADDRESS_ALLOCATION}
    assert len(caps) == 3
    assert str(Capability.BRANCHING) == "BRANCHING"


def test_capability_profiles() -> None:
    assert FULL_PROFILE.has(Capability.BRANCHING)
    assert FULL_PROFILE.has(Capability.MEMORY_RETENTION)
    assert FULL_PROFILE.has(Capability.ADDRESS_ALLOCATION)

    assert not WITHOUT_BRANCH.has_branching
    assert WITHOUT_BRANCH.has_memory
    assert WITHOUT_BRANCH.has_alloc

    assert WITHOUT_MEMORY.has_branching
    assert not WITHOUT_MEMORY.has_memory
    assert WITHOUT_MEMORY.has_alloc

    assert WITHOUT_ALLOC.has_branching
    assert WITHOUT_ALLOC.has_memory
    assert not WITHOUT_ALLOC.has_alloc

    assert not MINIMAL_PROFILE.has_branching
    assert not MINIMAL_PROFILE.has_memory
    assert not MINIMAL_PROFILE.has_alloc


def test_profile_subsets() -> None:
    assert WITHOUT_BRANCH.is_subset_of(FULL_PROFILE)
    assert WITHOUT_MEMORY.is_subset_of(FULL_PROFILE)
    assert WITHOUT_ALLOC.is_subset_of(FULL_PROFILE)
    assert MINIMAL_PROFILE.is_subset_of(WITHOUT_BRANCH)
    assert not FULL_PROFILE.is_subset_of(WITHOUT_BRANCH)


def test_public_view_equality() -> None:
    v1 = PublicView(output_tape=(1, 2, 3), steps=5, halted=True, status="HALTED")
    v2 = PublicView(output_tape=(1, 2, 3), steps=5, halted=True, status="HALTED")
    v3 = PublicView(output_tape=(1, 2), steps=5, halted=True, status="HALTED")

    assert v1.equals(v2)
    assert not v1.equals(v3)
