"""Authorization license and licensed apply. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Sequence

from . import _bootstrap  # noqa: F401
from derivation.iso import CanonKey
from research.x301_formal_semantics.semantics import RelationalModel
from .actions import CandidateAction
from .evaluation import ActionEvaluation
from .refusal import UnlicensedActionError


@dataclass(frozen=True)
class AbilitySet:
    """Capability boundary. None means unrestricted; empty tuple means nothing is able."""

    admissible_actions: Optional[tuple[CandidateAction, ...]] = None

    def is_able(self, action: CandidateAction) -> bool:
        if self.admissible_actions is None:
            return True
        return any(a.name == action.name for a in self.admissible_actions)

    def filter_proposals(self, proposals: Sequence[CandidateAction]) -> list[CandidateAction]:
        return [a for a in proposals if self.is_able(a)]


@dataclass(frozen=True)
class ActionProposal:
    """Supply-shaped offering. Recording it changes no admitted state."""

    token: str
    offerings: tuple[CandidateAction, ...] = ()


@dataclass(frozen=True)
class License:
    """Authorization of projected-state canonical keys. Not a sealed Event."""

    granter: str
    scope: str
    authorized: tuple[CanonKey, ...]

    def __post_init__(self) -> None:
        if len(set(self.authorized)) != len(self.authorized):
            raise ValueError("Authorized keys must be distinct")
        if tuple(sorted(self.authorized)) != self.authorized:
            raise ValueError("Authorized keys must be sorted")


class ActionAuthorizer:
    """Independent authorization gate. Default policy is allow-if-viable.

    That default is an explicit policy, not a committee. Pass `policy` to
    refuse otherwise-viable evaluations.
    """

    def __init__(
        self,
        granter: str = "x303_authorizer",
        scope: str = "step_authorization",
        policy: Optional[Callable[[ActionEvaluation], bool]] = None,
    ):
        self.granter = granter
        self.scope = scope
        self.policy = policy

    def authorize_evaluation(self, evaluation: ActionEvaluation) -> Optional[License]:
        if not evaluation.viable:
            return None
        if evaluation.firewall_refuted:
            return None
        if self.policy is not None and not self.policy(evaluation):
            return None
        if evaluation.projected_state is None:
            raise ValueError("Cannot authorize an evaluation with no projected state")
        canon_key = evaluation.canon_key or evaluation.action.get_canon_key(evaluation.projected_state)
        return self.issue_license([canon_key])

    def issue_license(self, authorized_keys: Sequence[CanonKey]) -> License:
        distinct_sorted = tuple(sorted(set(authorized_keys)))
        return License(
            granter=self.granter,
            scope=self.scope,
            authorized=distinct_sorted,
        )

    def is_authorized(self, action_key: CanonKey, license: Optional[License]) -> bool:
        if license is None:
            return False
        return action_key in license.authorized


class LicensedDriver:
    """Applies a candidate only after its projected key is on the license."""

    def apply_licensed(
        self,
        model: RelationalModel,
        action: CandidateAction,
        license: License,
    ) -> RelationalModel:
        if action.canon_key is not None:
            if action.canon_key not in license.authorized:
                raise UnlicensedActionError(
                    f"Action {action.name} with key {action.canon_key} is not authorized by license {license}"
                )
            return action.apply(model)
        projected = action.apply(model)
        action_key = action.get_canon_key(projected)
        if action_key not in license.authorized:
            raise UnlicensedActionError(
                f"Action {action.name} with key {action_key} is not authorized by license {license}"
            )
        return projected
