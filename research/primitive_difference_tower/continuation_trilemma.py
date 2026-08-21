"""The finite continuation grammar after a non-fixed residual orbit.

This grammar is intentionally small.  A continuation either carries a named
symmetry-breaking anchor, retains the complete residual orbit, or refuses to
continue.  It creates no anchor and collapses none of the anchors supplied by
the caller.  Thus it is a finite branch policy, not an account of every
possible response to every obstruction.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional, Union

from bridge_contract import BinaryVector, BridgeContract, Origin, Provenance
from equivariant_selection import AnchoredSingletonChoice


class ContinuationMode(str, Enum):
    """The three kinds of continuation allowed by the declared grammar."""

    ANCHORED_SINGLETON = "anchored-singleton"
    RETAIN_ORBIT = "retain-orbit"
    REFUSE = "refuse"


@dataclass(frozen=True)
class AnchoredContinuation:
    """A singleton continuation whose asymmetry remains a named import."""

    selection: AnchoredSingletonChoice

    @property
    def mode(self) -> ContinuationMode:
        return ContinuationMode.ANCHORED_SINGLETON

    def to_data(self) -> dict[str, object]:
        return {"mode": self.mode.value, "selection": self.selection.to_data()}


@dataclass(frozen=True)
class RetainedOrbitContinuation:
    """A symmetry-stable continuation with every residual-orbit member kept."""

    members: tuple[BinaryVector, ...]
    provenance: Provenance

    @property
    def mode(self) -> ContinuationMode:
        return ContinuationMode.RETAIN_ORBIT

    def to_data(self) -> dict[str, object]:
        return {
            "members": [list(member) for member in self.members],
            "mode": self.mode.value,
            "provenance": self.provenance.to_data(),
        }


@dataclass(frozen=True)
class RefusedContinuation:
    """An explicit terminal response that names its refusal instead of choosing."""

    reason: str
    provenance: Provenance

    def __post_init__(self) -> None:
        if not self.reason:
            raise ValueError("a refusal must state a nonempty reason")
        if self.provenance.origin is not Origin.REFUSED:
            raise ValueError("a refusal must retain refused provenance")

    @property
    def mode(self) -> ContinuationMode:
        return ContinuationMode.REFUSE

    def to_data(self) -> dict[str, object]:
        return {
            "mode": self.mode.value,
            "provenance": self.provenance.to_data(),
            "reason": self.reason,
        }


Continuation = Union[AnchoredContinuation, RetainedOrbitContinuation, RefusedContinuation]


def retained_orbit_continuation(contract: BridgeContract) -> RetainedOrbitContinuation:
    """Keep the entire computed orbit; no representative is selected."""

    return RetainedOrbitContinuation(
        members=contract.residual_orbit,
        provenance=Provenance("computed-full-residual-orbit", Origin.COMPUTED),
    )


def refused_continuation(reason: str) -> RefusedContinuation:
    """Construct the grammar's explicit no-choice branch."""

    return RefusedContinuation(
        reason=reason,
        provenance=Provenance("explicit-continuation-refusal", Origin.REFUSED),
    )


def declared_continuations(
    contract: BridgeContract,
    anchors: Iterable[AnchoredSingletonChoice],
    refusal_reason: str,
) -> tuple[Continuation, ...]:
    """Preserve supplied anchors, then append aggregate and refusal branches.

    No anchor is manufactured here.  The returned order keeps every supplied
    branch in its supplied order, including distinct anchors for tied orbit
    members.
    """

    anchored = tuple(AnchoredContinuation(selection=anchor) for anchor in anchors)
    for continuation in anchored:
        if continuation.selection.choice not in contract.residual_orbit:
            raise ValueError("an anchored continuation must select a residual-orbit member")
    return (*anchored, retained_orbit_continuation(contract), refused_continuation(refusal_reason))


def selected_singleton(continuation: Continuation) -> Optional[BinaryVector]:
    """Expose a singleton only for the explicitly anchored branch form."""

    if isinstance(continuation, AnchoredContinuation):
        return continuation.selection.choice
    return None


def is_swap_stable(contract: BridgeContract, continuation: Continuation) -> bool:
    """Decide stability without pretending an anchored singleton is invariant."""

    if isinstance(continuation, AnchoredContinuation):
        return contract.symmetry.apply_vector(continuation.selection.choice) == continuation.selection.choice
    if isinstance(continuation, RetainedOrbitContinuation):
        return continuation.members == tuple(
            sorted(contract.symmetry.apply_vector(member) for member in continuation.members)
        )
    return True
