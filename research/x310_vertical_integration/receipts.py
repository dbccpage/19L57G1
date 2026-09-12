"""Canonical JSON and grand-receipt digests. AuthorityEffect: None."""
from __future__ import annotations

import hashlib
import json
from typing import Mapping, Any

FIXED_TIMESTAMP = "1970-01-01T00:00:00Z"


def canonical_json_dumps(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def canonical_grand_receipt_digest(payload: Mapping[str, Any]) -> str:
    clean = {k: v for k, v in payload.items() if k != "grand_receipt_sha256"}
    raw = canonical_json_dumps(clean).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
