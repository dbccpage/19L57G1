from copy import deepcopy
from typing import Any

import pytest

from refresh import affected_records, refresh_views


def graph() -> dict[str, Any]:
    def source(path: str) -> dict[str, str]:
        return {"path": path, "span_sha256": "1" * 64}
    return {"source_snapshot": "a" * 40, "records": {
        "theorem": [{"id": "proof", "source": source("proof.lean")}, {"id": "other", "source": source("other.lean")}],
        "claim": [{"id": "claim", "evidence_ids": ["proof"]}],
        "headline": [{"id": "headline", "source": source("claim.md"), "claim_ids": ["claim"]}],
        "edge": [{"id": "edge", "kind": "depends-on-proof", "from": "claim", "to": "proof"}]}}


def test_source_change_recomputes_only_descendants_and_recovery() -> None:
    g = graph()
    pristine = deepcopy(g)
    initial = refresh_views(g, set())
    changed = refresh_views(g, {"proof.lean"}, initial)
    assert set(changed["recomputed_ids"]) == {"proof", "claim", "headline", "edge"}
    assert changed["reused_ids"] == ["other"]
    assert changed["views"]["headline"]["requires_replay"]
    assert g == pristine  # historical proof and source remain unchanged
    assert not refresh_views(g, set(), changed)["views"]["headline"]["requires_replay"]
    assert affected_records(g, {"absent.md"}) == set()


def test_incremental_cache_cannot_delete_or_add_population() -> None:
    g = graph()
    previous = refresh_views(g, set())
    previous["views"].pop("headline")
    with pytest.raises(ValueError, match="REFRESH_CACHE_POPULATION_CHANGED"):
        refresh_views(g, set(), previous)
