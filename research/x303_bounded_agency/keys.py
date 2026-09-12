"""Canonical digests and isomorphism keys. AuthorityEffect: None."""
from __future__ import annotations

import hashlib
import json

from . import _bootstrap  # noqa: F401
from derivation.iso import CanonKey, canonical
from research.x301_formal_semantics.semantics import RelationalModel


def canonical_model_digest(model: RelationalModel) -> str:
    """Deterministic SHA-256 digest of relational carrier state."""
    payload = [
        list(model.data),
        list(model.forms),
        sorted([[f, list(args)] for f, args in model.insts]),
        sorted(list(model.rules)),
        sorted([list(pair) for pair in model.reqs]),
    ]
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def compute_canon_key(model: RelationalModel) -> CanonKey:
    """Compute the sealed isomorphism key. Fail if the model cannot form a Regime."""
    return canonical(model.to_regime())
