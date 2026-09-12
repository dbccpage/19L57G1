"""Typed refusal reasons. AuthorityEffect: None."""
from __future__ import annotations


class RefusalReason:
    """Standardized reasons for typed operational refusal."""

    FUEL_EXHAUSTED = "Declared operational fuel budget exhausted"
    VIABILITY_BOUNDARY_EXCEEDED = "All candidate actions drive state outside viability envelope"
    AUTHORIZATION_DENIED = "Metatheoretic authorization license denied"
    FIREWALL_CONSENSUS_OVERRIDE = "Grounding Firewall consensus override: empirical contradiction"
    NO_CANDIDATE_ACTIONS = "Candidate action pool is empty"
    UNLICENSED_ACTION = "Attempted unilateral mutation without authorized license"


class UnlicensedActionError(ValueError):
    """Refused: unilateral mutation attempted without an authorized license."""
