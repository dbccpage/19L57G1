"""The checked graph is independent of stored rows and of accepted claim links."""
import gzip
import json
from pathlib import Path

import pytest

from eg_sources import HERE, digest
from graph import OUTPUTS, build, compare_outputs


def test_complete_graph_regeneration_and_population(tmp_path: Path) -> None:
    expected = build()
    assert set(expected) == OUTPUTS
    claims = json.loads(gzip.decompress(expected["graph.json.gz"]))["records"]["claim"]
    identifiers = {digest(row["id"].encode("utf-8")): row for row in claims}
    ledgers = json.loads(expected["ledgers.json"])
    for row in ledgers["ledger_population"]:
        claim = identifiers[row["claim_id_sha256"]]
        assert digest(claim["public_id"].encode("utf-8")) == row["public_id_sha256"]
    assert set(ledgers["unresolved_citation_tokens"]) <= set(identifiers)
    compare_outputs(HERE / "evidence", expected)
    for name, raw in expected.items():
        (tmp_path / name).write_bytes(raw)
    (tmp_path / "extra.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="ARTIFACT_POPULATION_MISMATCH.*extra.json"):
        compare_outputs(tmp_path, expected)
    (tmp_path / "extra.json").unlink()
    (tmp_path / "graph.json.gz").write_bytes(b"{}")
    with pytest.raises(ValueError, match="GRAPH_ARTIFACT_DIFFERS: graph.json.gz"):
        compare_outputs(tmp_path, expected)
    (tmp_path / "graph.json.gz").unlink()
    with pytest.raises(ValueError, match="ARTIFACT_POPULATION_MISMATCH"):
        compare_outputs(tmp_path, expected)
