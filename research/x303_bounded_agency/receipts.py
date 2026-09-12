"""Deterministic agency-step receipts. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Optional

FIXED_TIMESTAMP = "1970-01-01T00:00:00Z"


@dataclass(frozen=True)
class AgencyReceipt:
    """Cryptographic audit receipt emitted on agent decision or refusal."""

    schema: str = "agency-step-v1"
    timestamp: str = ""
    step_index: int = 0
    outcome: str = ""
    refusal_reason: Optional[str] = None
    action_repr: Optional[str] = None
    pre_state_sha256: str = ""
    post_state_sha256: str = ""
    fuel_before: int = 0
    fuel_after: int = 0
    receipt_sha256: str = ""

    def compute_sha256(self) -> str:
        data = {
            "schema": self.schema,
            "timestamp": self.timestamp,
            "step_index": self.step_index,
            "outcome": self.outcome,
            "refusal_reason": self.refusal_reason,
            "action_repr": self.action_repr,
            "pre_state_sha256": self.pre_state_sha256,
            "post_state_sha256": self.post_state_sha256,
            "fuel_before": self.fuel_before,
            "fuel_after": self.fuel_after,
        }
        canonical_bytes = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()

    @classmethod
    def create(
        cls,
        step_index: int,
        outcome: str,
        pre_state_sha256: str,
        post_state_sha256: str,
        fuel_before: int,
        fuel_after: int,
        action_repr: Optional[str] = None,
        refusal_reason: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> AgencyReceipt:
        ts = timestamp if timestamp is not None else FIXED_TIMESTAMP
        unhashed = cls(
            schema="agency-step-v1",
            timestamp=ts,
            step_index=step_index,
            outcome=outcome,
            refusal_reason=refusal_reason,
            action_repr=action_repr,
            pre_state_sha256=pre_state_sha256,
            post_state_sha256=post_state_sha256,
            fuel_before=fuel_before,
            fuel_after=fuel_after,
            receipt_sha256="",
        )
        digest = unhashed.compute_sha256()
        return cls(
            schema=unhashed.schema,
            timestamp=unhashed.timestamp,
            step_index=unhashed.step_index,
            outcome=unhashed.outcome,
            refusal_reason=unhashed.refusal_reason,
            action_repr=unhashed.action_repr,
            pre_state_sha256=unhashed.pre_state_sha256,
            post_state_sha256=unhashed.post_state_sha256,
            fuel_before=unhashed.fuel_before,
            fuel_after=unhashed.fuel_after,
            receipt_sha256=digest,
        )
