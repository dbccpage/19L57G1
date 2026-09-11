"""Proposer hole: other research procedures may offer Deltas only.

AuthorityEffect: None.

Offerings are not ``decide()`` input and not Events.  Occupancy that
exposes ``emit``, ``materialize``, or ``host_next_demand`` as a selector
is refused.  This module does not import ``partial_decide``.
"""

from __future__ import annotations

from typing import Protocol, cast

from derivation.candidates import Delta, NewDatum, NewForm, NewInst, NewRuleAll

from harness import HarnessError, Node, Proposal

_ITEM_TYPES = (NewDatum, NewForm, NewInst, NewRuleAll)
_SELECTOR_NAMES = ("emit", "materialize", "host_next_demand")


class SelectorOccupancyError(HarnessError):
    """The proposer hole is not a demand or grade selector."""


class OfferingError(HarnessError):
    """An offering that is not a Delta is refused."""


class Proposer(Protocol):
    """Hole for other research procedures' Delta offerings."""

    def offerings(self, node: Node) -> tuple[object, ...]:
        """Return Delta tuples.  Not Events, not decide() input."""


def _is_delta(value: object) -> bool:
    if not isinstance(value, tuple):
        return False
    return all(isinstance(item, _ITEM_TYPES) for item in value)


def occupy(proposer: Proposer, node: Node) -> Proposal:
    """Record Delta offerings as a Supply-shaped proposal."""
    for name in _SELECTOR_NAMES:
        if getattr(proposer, name, None) is not None:
            raise SelectorOccupancyError(
                f"proposer occupancy cannot use {name} as a selector"
            )
    raw = proposer.offerings(node)
    if not isinstance(raw, tuple):
        raise OfferingError("offerings must be a tuple of Deltas")
    accepted: list[Delta] = []
    for item in raw:
        if not _is_delta(item):
            raise OfferingError("offerings must be Deltas, not Events")
        accepted.append(cast(Delta, item))
    return Proposal(token="delta-offerings", offerings=tuple(accepted))
