"""Synthetic records exercise scope guards; they are not research receipts."""
from copy import deepcopy
from typing import Any

import pytest

from eg_schema import validate
from eg_sources import HERE, Snapshot, canonical, digest, load_snapshot, read_object


@pytest.fixture(scope="module")
def snapshot() -> Snapshot:
    return load_snapshot()


def fixture_graph(snapshot: Snapshot) -> dict[str, Any]:
    specification = read_object(HERE / "SCHEMA.json")
    source = snapshot.reference("lean4/Derivation/TraceAlgebra.lean", 392, 409)
    graph: dict[str, Any] = {"schema": 1, "source_snapshot": snapshot.snapshot, "authority_effect": "None",
                             "records": {kind: [] for kind in specification["record_fields"]}}
    graph["records"]["replay"] = [{"id": "replay:fixture", "source_snapshot": snapshot.snapshot, "tree": "fixture",
        "command": ["fixture-check"], "cwd": "fixture", "input_sources": [source], "output_digest": "1" * 64,
        "exit_code": 0, "receipt_sources": [], "result": "PASSED", "gap": None}]
    theorem = {"id": "theorem:fixture", "source": source, "module": "TraceAlgebra", "declaration": "fixture",
        "kind": "theorem", "elaborated_type": "P implies Q", "local_hypotheses": [{"name": "h", "type": "P"}],
        "axioms": [], "report_population": ["fixture"], "build_receipt": "replay:fixture", "gap": None}
    graph["records"]["theorem"] = [theorem]
    graph["records"]["assumption"] = [{"id": "assumption:fixture", "statement": source,
        "source_class": "admitted primitive", "gap": None}]
    graph["records"]["claim"] = [{"id": "claim:fixture", "public_id": "fixture", "statement": source,
        "source_class": "proved theorem", "status": "CONDITIONAL", "lineage": "native", "bounds": [],
        "assumption_ids": ["assumption:fixture"], "parent_bridge_ids": [], "evidence_ids": ["theorem:fixture"], "gap": None}]
    graph["records"]["headline"] = [{"id": "headline:fixture", "source": source, "kind": "prose",
        "claim_ids": ["claim:fixture"], "scope_verdict": "MATCHED", "scope_evidence_ids": ["theorem:fixture"],
        "review": {"scope_statement": "Synthetic implication fixture, including its premise.",
            "theorem_scope_digests": {"theorem:fixture": digest(canonical({"type": theorem["elaborated_type"], "hypotheses": theorem["local_hypotheses"]}))}},
        "gap": None}]
    return graph


def test_scoped_synthetic_fixture_passes(snapshot: Snapshot) -> None:
    assert len(validate(fixture_graph(snapshot), snapshot)) == 5


@pytest.mark.parametrize("mutation,error", [
    ("missing_parent", "LINK_MISSING"),
    ("missing_assumption", "LINK_MISSING"),
    ("empty_assumptions", "CONDITIONAL_ASSUMPTIONS_MISSING"),
    ("source_digest", "SOURCE_REFERENCE_MISMATCH"),
    ("stale_theorem", "THEOREM_NOT_IN_REPORT"),
    ("hidden_premise", "THEOREM_SCOPE_CHANGED"),
    ("wrong_head", "REPLAY_NOT_SUCCESSFUL"),
    ("parallel_as_native", "NATIVE_BRIDGE_MISSING"),
    ("declared_only", "EVIDENCE_UNRESOLVED"),
    ("bool_exit", "REPLAY_COMMAND_OR_EXIT_INVALID"),
])
def test_named_scope_failures(snapshot: Snapshot, mutation: str, error: str) -> None:
    graph = deepcopy(fixture_graph(snapshot))
    records = graph["records"]
    if mutation == "missing_parent":
        records["claim"][0]["parent_bridge_ids"] = ["absent"]
    elif mutation == "missing_assumption":
        records["assumption"] = []
    elif mutation == "empty_assumptions":
        records["claim"][0]["assumption_ids"] = []
    elif mutation == "source_digest":
        records["claim"][0]["statement"] = {**records["claim"][0]["statement"], "file_sha256": "0" * 64}
    elif mutation == "stale_theorem":
        records["theorem"][0]["declaration"] = "missing"
    elif mutation == "hidden_premise":
        records["theorem"][0]["local_hypotheses"].append({"name": "extra", "type": "Q"})
    elif mutation == "wrong_head":
        records["replay"][0]["source_snapshot"] = "0" * 40
    elif mutation == "parallel_as_native":
        records["claim"][0]["statement"] = snapshot.reference("research/concurrency/README.md", 1, 6)
    elif mutation == "declared_only":
        records["theorem"][0]["gap"] = "The compiled statement was not obtained."
    else:
        records["replay"][0]["exit_code"] = False
    with pytest.raises(ValueError, match=error):
        validate(graph, snapshot)


def test_deleted_headline_and_empty_population_fail(snapshot: Snapshot) -> None:
    graph = fixture_graph(snapshot)
    with pytest.raises(ValueError, match="HEADLINE_POPULATION_MISMATCH"):
        validate(graph, snapshot, expected_headlines={"headline:fixture", "headline:removed"})
    graph["records"]["headline"] = []
    with pytest.raises(ValueError, match="HEADLINE_POPULATION_EMPTY"):
        validate(graph, snapshot, expected_headlines=set())
