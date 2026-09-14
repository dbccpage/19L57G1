"""Operational valuation and pricing of the 7th constructor under mu1 and mu2.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Sequence

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.model import (
    Regime,
    Supply,
)
from .conservative_grammar import (
    ExtendedEvent,
    SwapWitness,
    cardinal_potential,
    extended_step,
)


def capability_cost_mu1(e: ExtendedEvent) -> int:
    """Base capability cost mu1(e) in Nat.

    Assigns 0 to Supply and SwapWitness (conservative rewrite), 1 to native additions.
    """
    if isinstance(e, (Supply, SwapWitness)):
        return 0
    return 1


def transition_cost_mu2(e: ExtendedEvent) -> int:
    """Cumulative transition history cost mu2(e) in Nat.

    Assigns 0 to non-admitted Supply presentation events, 1 to all operational transitions.
    """
    if isinstance(e, Supply):
        return 0
    return 1


def evaluate_trajectory_costs(history: Sequence[ExtendedEvent]) -> tuple[int, int]:
    """Compute (cumulative_mu1, cumulative_mu2) along an event trajectory."""
    c_mu1 = sum(capability_cost_mu1(e) for e in history)
    c_mu2 = sum(transition_cost_mu2(e) for e in history)
    return c_mu1, c_mu2


def verify_coboundary_identity(r: Regime, e: ExtendedEvent) -> bool:
    """Verify exact coboundary identity: mu1(e) == N(step(r, e)) - N(r)."""
    p_before = cardinal_potential(r)
    r_after = extended_step(r, e)
    p_after = cardinal_potential(r_after)
    return capability_cost_mu1(e) == (p_after - p_before)


def evaluate_cycle_circulation(cycle_events: Sequence[ExtendedEvent]) -> dict[str, object]:
    """Compute line integrals oint mu1 and oint mu2 around a closed execution cycle."""
    c_mu1, c_mu2 = evaluate_trajectory_costs(cycle_events)
    k = len(cycle_events)

    return {
        "cycle_length": k,
        "oint_mu1": c_mu1,
        "oint_mu2": c_mu2,
        "is_mu1_exact_coboundary": (c_mu1 == 0),
        "is_mu2_circulation_strictly_positive": (c_mu2 > 0),
        "circulation_cost_contrast": (c_mu1 == 0 and c_mu2 > 0),
    }
