"""Finite selection facts for the displayed non-fixed residual orbit.

The module proves a boundary about one declared two-coordinate presentation.
It does not say that every symmetric problem lacks a selector.  It does say
that no member of this particular non-fixed orbit can be chosen while also
being fixed by its declared swap.  A usable singleton may still be imported
through ``AnchoredSingletonChoice``; that import keeps its ``ADMITTED``
provenance rather than becoming a result of the symmetry calculation.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridge_contract import BinaryVector, BridgeContract, Origin, Provenance


def _require_residual_member(contract: BridgeContract, choice: BinaryVector) -> None:
    if choice not in contract.residual_orbit:
        raise ValueError("singleton choice must be a member of the residual orbit")


def residual_singleton_choices(contract: BridgeContract) -> tuple[BinaryVector, ...]:
    """Enumerate every singleton candidate in the declared residual orbit."""

    return contract.residual_orbit


def is_equivariant_singleton_choice(contract: BridgeContract, choice: BinaryVector) -> bool:
    """Decide whether a residual-orbit singleton is fixed by declared symmetry."""

    _require_residual_member(contract, choice)
    return contract.symmetry.apply_vector(choice) == choice


def no_equivariant_residual_singleton_choice(contract: BridgeContract) -> bool:
    """Exhaustively check the finite no-fixed-member boundary for this orbit."""

    choices = residual_singleton_choices(contract)
    return bool(choices) and all(
        not is_equivariant_singleton_choice(contract, choice) for choice in choices
    )


@dataclass(frozen=True)
class AnchoredSingletonChoice:
    """A singleton selected by a separately admitted anchor, not by symmetry."""

    choice: BinaryVector
    anchor: Provenance

    def __post_init__(self) -> None:
        if self.anchor.origin is not Origin.ADMITTED:
            raise ValueError("an anchored singleton must carry an admitted anchor")

    def to_data(self) -> dict[str, object]:
        return {"anchor": self.anchor.to_data(), "choice": list(self.choice)}


def anchored_singleton_choice(
    contract: BridgeContract, choice: BinaryVector, anchor: Provenance
) -> AnchoredSingletonChoice:
    """Accept a residual singleton only when the symmetry-breaking import is named."""

    _require_residual_member(contract, choice)
    return AnchoredSingletonChoice(choice=choice, anchor=anchor)
