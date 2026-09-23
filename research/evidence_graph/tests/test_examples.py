"""Six schema examples, all synthetic; none is a scientific replay receipt."""
from copy import deepcopy
from typing import Any

import pytest

from eg_schema import validate
from eg_sources import Snapshot, canonical, digest, load_snapshot
from refresh import refresh_views
from .test_schema import fixture_graph


@pytest.fixture(scope="module")
def snapshot() -> Snapshot:
    return load_snapshot()


def finite_example(snapshot: Snapshot) -> dict[str, Any]:
    graph = fixture_graph(snapshot)
    rows = graph["records"]
    source = rows["claim"][0]["statement"]
    row = {"id": "computation:finite", "source": source, "entrypoint": "synthetic fixture",
        "grammar": ["declared two-element carrier"], "bounds": {"size": 2}, "arithmetic": "exact integers",
        "receipt_sources": [], "replay_command": ["fixture-check"], "replay_receipt": "replay:fixture",
        "frontier_status": "synthetic complete finite population", "gap": None}
    rows["computation"] = [row]
    rows["claim"][0].update(status="VERIFIED_FINITE", source_class="deterministic computation", bounds={"size": 2}, evidence_ids=[row["id"]])
    rows["headline"][0]["scope_evidence_ids"] = [row["id"]]
    rows["headline"][0]["review"].update(theorem_scope_digests={}, computation_scope_digests={row["id"]: digest(canonical({k: row[k] for k in ("grammar", "bounds", "arithmetic")}))})
    return graph


def test_native_theorem_and_local_assumption_examples(snapshot: Snapshot) -> None:
    local = fixture_graph(snapshot)
    validate(local, snapshot)
    native = deepcopy(local)
    native["records"]["claim"][0]["status"] = "PROVED_THEOREM"
    validate(native, snapshot)


def test_finite_fixture_and_prose_bound_inflation(snapshot: Snapshot) -> None:
    graph = finite_example(snapshot)
    validate(graph, snapshot)
    graph["records"]["claim"][0]["bounds"]["size"] = 3
    with pytest.raises(ValueError, match="FINITE_BOUND_SCOPE_CHANGED"):
        validate(graph, snapshot)
    graph = finite_example(snapshot)
    graph["records"]["computation"][0]["bounds"]["size"] = 3
    graph["records"]["claim"][0]["bounds"]["size"] = 3
    with pytest.raises(ValueError, match="FINITE_BOUND_SCOPE_CHANGED"):
        validate(graph, snapshot)


def test_refuted_bridge_and_open_edge_examples(snapshot: Snapshot) -> None:
    graph = fixture_graph(snapshot)
    rows = graph["records"]
    source = rows["claim"][0]["statement"]
    rows["countermodel"] = [{"id": "countermodel:fixture", "source": source,
        "negated_claim_id": "claim:fixture", "retained_assumptions": ["assumption:fixture"],
        "removed_assumption": "supplied selector", "witness": {"orbit": [0, 1], "swap": [1, 0]},
        "checker": "synthetic fixture check", "replay_receipt": "replay:fixture", "gap": None}]
    rows["claim"][0].update(status="REFUTED", source_class="refuted claim", evidence_ids=["countermodel:fixture"])
    rows["headline"][0].update(scope_verdict="UNRESOLVED", scope_evidence_ids=[], review=None,
                              gap="The synthetic countermodel is not a public-wording review.")
    rows["bridge"] = [{"id": "bridge:open", "source": source, "source_carrier": "two-member orbit", "target_carrier": "selected singleton",
        "source_steps": "swap", "target_steps": "fixed selector", "supported_domain": "the displayed fixture",
        "state_maps": [], "event_maps": [], "observation_maps": [], "direction": "selection",
        "identity_composition": None, "refusal_guard": None, "proof_ids": [], "countermodel_ids": ["countermodel:fixture"],
        "gap": "No fixed singleton map exists in this synthetic orbit."}]
    rows["edge"] = [{"id": "edge:refutes", "kind": "refuted-by", "from": "claim:fixture", "to": "countermodel:fixture", "source": source, "gap": None}]
    validate(graph, snapshot)
    rows["claim"][0].update(status="OPEN", evidence_ids=[], gap="The larger carrier is unproved.")
    rows["edge"].append({"id": "edge:open", "kind": "simulates", "from": "claim:fixture", "to": "bridge:open", "source": source, "gap": "No larger-domain map is established."})
    validate(graph, snapshot)


def test_historical_result_with_head_drift_retains_its_source(snapshot: Snapshot) -> None:
    graph = fixture_graph(snapshot)
    validate(graph, snapshot)
    before = deepcopy(graph)
    path = graph["records"]["theorem"][0]["source"]["path"]
    current = refresh_views(graph, {path})
    assert "claim:fixture" in current["invalidated_ids"]
    assert graph == before
    validate(graph, snapshot)
