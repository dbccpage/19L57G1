"""Fail-closed record and scope checks. AuthorityEffect: None."""
from __future__ import annotations

from collections import deque
from typing import Any, cast

from eg_sources import HERE, Snapshot, SourceRef, canonical, digest, read_object


def required_string(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"STRING_REQUIRED: {context}")
    return value


def unique_strings(value: object, context: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(v, str) or not v for v in value):
        raise ValueError(f"STRING_LIST_REQUIRED: {context}")
    if len(value) != len(set(value)):
        raise ValueError(f"DUPLICATE_LINK: {context}")
    return cast(list[str], value)


def topological_ranks(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, int]:
    """Rank strictly decreases from a dependent to each prerequisite."""
    if len(set(nodes)) != len(nodes):
        raise ValueError("DEPENDENCY_NODE_DUPLICATE")
    waiting: dict[str, set[str]] = {node: set() for node in nodes}
    dependents: dict[str, set[str]] = {node: set() for node in nodes}
    for source, target in edges:
        if source not in waiting or target not in waiting:
            raise ValueError(f"DEPENDENCY_NODE_MISSING: {source} -> {target}")
        waiting[source].add(target)
        dependents[target].add(source)
    ready = deque(sorted(node for node in nodes if not waiting[node]))
    rank = {node: 0 for node in ready}
    while ready:
        node = ready.popleft()
        for dependent in sorted(dependents[node]):
            rank[dependent] = max(rank.get(dependent, 0), rank[node] + 1)
            waiting[dependent].remove(node)
            if not waiting[dependent]:
                ready.append(dependent)
    residual = sorted(node for node in nodes if waiting[node])
    if residual:
        raise ValueError(f"PROOF_DEPENDENCY_CYCLE: {residual}")
    return rank


def check_source_values(value: object, snapshot: Snapshot, fields: set[str]) -> None:
    if isinstance(value, dict):
        if "span_sha256" in value or {"start_line", "end_line"} <= value.keys():
            if set(value) != fields:
                raise ValueError("SOURCE_REFERENCE_FIELDS")
            snapshot.resolve(cast(SourceRef, value))
        else:
            for child in value.values():
                check_source_values(child, snapshot, fields)
    elif isinstance(value, list):
        for child in value:
            check_source_values(child, snapshot, fields)


def validate(graph: dict[str, Any], snapshot: Snapshot, *, schema: dict[str, Any] | None = None,
             expected_headlines: set[str] | None = None, expected_trees: set[str] | None = None) -> dict[str, int]:
    specification = read_object(HERE / "SCHEMA.json") if schema is None else schema
    if set(graph) != {"schema", "source_snapshot", "authority_effect", "records"}:
        raise ValueError("GRAPH_FIELDS")
    if graph["schema"] != 1 or graph["source_snapshot"] != snapshot.snapshot or graph["authority_effect"] != "None":
        raise ValueError("GRAPH_HEADER")
    groups = graph["records"]
    if not isinstance(groups, dict) or set(groups) != set(specification["record_fields"]):
        raise ValueError("GRAPH_RECORD_POPULATION")
    registry: dict[str, tuple[str, dict[str, Any]]] = {}
    for kind, fields in specification["record_fields"].items():
        rows = groups[kind]
        if not isinstance(rows, list):
            raise ValueError(f"RECORD_LIST_REQUIRED: {kind}")
        for row in rows:
            if not isinstance(row, dict) or set(row) != set(fields):
                raise ValueError(f"RECORD_FIELDS: {kind}: {row.get('id') if isinstance(row, dict) else 'not-object'}")
            identifier = required_string(row["id"], kind)
            if identifier in registry:
                raise ValueError(f"RECORD_ID_DUPLICATE: {identifier}")
            registry[identifier] = (kind, row)
            if row["gap"] is not None:
                required_string(row["gap"], identifier + ".gap")
            check_source_values(row, snapshot, set(specification["source_reference_fields"]))
    if not registry:
        raise ValueError("GRAPH_EMPTY")

    def link(identifier: str, permitted: set[str], owner: str) -> dict[str, Any]:
        if identifier not in registry:
            raise ValueError(f"LINK_MISSING: {owner}: {identifier}")
        kind, target = registry[identifier]
        if kind not in permitted:
            raise ValueError(f"LINK_KIND: {owner}: {identifier}: {kind}")
        return target

    def links(row: dict[str, Any], field: str, permitted: set[str]) -> list[dict[str, Any]]:
        return [link(identifier, permitted, row["id"]) for identifier in unique_strings(row[field], row["id"] + "." + field)]

    def successful_replay(identifier: object, owner: str) -> dict[str, Any]:
        replay = link(required_string(identifier, owner + ".replay"), {"replay"}, owner)
        if replay["source_snapshot"] != snapshot.snapshot or replay["exit_code"] != 0 or replay["result"] != "PASSED":
            raise ValueError(f"REPLAY_NOT_SUCCESSFUL: {owner}")
        if not replay["input_sources"] or not replay["output_digest"] or not replay["command"]:
            raise ValueError(f"REPLAY_UNBOUND: {owner}")
        return replay

    def checked_evidence(row: dict[str, Any]) -> None:
        kind = registry[row["id"]][0]
        if row["gap"] is not None:
            raise ValueError(f"EVIDENCE_UNRESOLVED: {row['id']}")
        if kind == "theorem":
            if not row["elaborated_type"] or row["local_hypotheses"] is None or row["axioms"] is None:
                raise ValueError(f"THEOREM_REPORT_INCOMPLETE: {row['id']}")
            if row["declaration"] not in unique_strings(row["report_population"], row["id"]):
                raise ValueError(f"THEOREM_NOT_IN_REPORT: {row['id']}")
            successful_replay(row["build_receipt"], row["id"])
        elif kind in {"computation", "countermodel"}:
            successful_replay(row["replay_receipt"], row["id"])
            if kind == "computation" and (not row["grammar"] or not row["bounds"] or not row["arithmetic"]):
                raise ValueError(f"COMPUTATION_SCOPE_MISSING: {row['id']}")
        else:
            raise ValueError(f"EVIDENCE_NOT_DIRECT: {row['id']}")

    for kind, rows in groups.items():
        for row in rows:
            identifier = row["id"]
            if kind == "claim":
                if row["status"] not in specification["evidence_statuses"] or row["lineage"] not in specification["lineages"]:
                    raise ValueError(f"CLAIM_CLASSIFICATION: {identifier}")
                if row["source_class"] is not None and row["source_class"] not in specification["source_classes"]:
                    raise ValueError(f"SOURCE_CLASS_INVALID: {identifier}")
                assumptions = links(row, "assumption_ids", {"assumption"})
                parents = links(row, "parent_bridge_ids", {"bridge"})
                evidence = links(row, "evidence_ids", {"theorem", "computation", "countermodel"})
                if row["status"] == "OPEN":
                    required_string(row["gap"], identifier + ".open_gap")
                else:
                    if not evidence or row["gap"] is not None or row["source_class"] is None or row["lineage"] == "unresolved":
                        raise ValueError(f"CLAIM_EVIDENCE_INCOMPLETE: {identifier}")
                    for item in evidence:
                        checked_evidence(item)
                    if row["status"] == "CONDITIONAL" and not assumptions:
                        raise ValueError(f"CONDITIONAL_ASSUMPTIONS_MISSING: {identifier}")
                    if row["status"] == "PROVED_THEOREM" and not any(item.get("kind") == "theorem" for item in evidence):
                        raise ValueError(f"THEOREM_EVIDENCE_MISSING: {identifier}")
                    if row["status"] == "VERIFIED_FINITE" and not any(registry[item["id"]][0] == "computation" for item in evidence):
                        raise ValueError(f"FINITE_EVIDENCE_MISSING: {identifier}")
                    if row["status"] == "REFUTED" and not any(registry[item["id"]][0] == "countermodel" for item in evidence):
                        raise ValueError(f"COUNTERMODEL_MISSING: {identifier}")
                    for item in evidence:
                        if registry[item["id"]][0] == "computation" and row["bounds"] != item["bounds"]:
                            raise ValueError(f"FINITE_BOUND_SCOPE_CHANGED: {identifier}")
                statement_source = row["statement"].get("source", row["statement"])
                if row["lineage"] == "native" and not statement_source["path"].startswith(("paper/", "prompt/", "code/", "lean4/Derivation", "artifacts/")) and not parents:
                    raise ValueError(f"NATIVE_BRIDGE_MISSING: {identifier}")
                if row["lineage"] == "supplied_bridge" and not parents:
                    raise ValueError(f"PARENT_BRIDGE_MISSING: {identifier}")
                if row["status"] != "OPEN" and row["lineage"] == "supplied_bridge" and any(parent["gap"] is not None for parent in parents):
                    raise ValueError(f"PARENT_BRIDGE_UNRESOLVED: {identifier}")
                if row["lineage"] == "native" and statement_source["path"].startswith("research/") and any(parent["gap"] is not None for parent in parents):
                    raise ValueError(f"NATIVE_BRIDGE_UNRESOLVED: {identifier}")
            elif kind == "assumption":
                if row["source_class"] not in specification["source_classes"]:
                    raise ValueError(f"ASSUMPTION_CLASS: {identifier}")
            elif kind == "headline":
                links(row, "claim_ids", {"claim"})
                evidence = links(row, "scope_evidence_ids", {"theorem", "computation", "countermodel"})
                if row["scope_verdict"] not in specification["scope_verdicts"]:
                    raise ValueError(f"SCOPE_VERDICT: {identifier}")
                if row["scope_verdict"] == "MATCHED":
                    if not row["claim_ids"] or not evidence or row["gap"] is not None or not isinstance(row["review"], dict):
                        raise ValueError(f"SCOPE_REVIEW_MISSING: {identifier}")
                    for item in evidence:
                        checked_evidence(item)
                    reports = {item["id"]: digest(canonical({"type": item["elaborated_type"], "hypotheses": item["local_hypotheses"]}))
                               for item in evidence if registry[item["id"]][0] == "theorem"}
                    if row["review"].get("theorem_scope_digests") != reports:
                        raise ValueError(f"THEOREM_SCOPE_CHANGED: {identifier}")
                    computations = {item["id"]: digest(canonical({"grammar": item["grammar"], "bounds": item["bounds"], "arithmetic": item["arithmetic"]}))
                                    for item in evidence if registry[item["id"]][0] == "computation"}
                    if row["review"].get("computation_scope_digests", {}) != computations:
                        raise ValueError(f"FINITE_BOUND_SCOPE_CHANGED: {identifier}")
                    if row["review"].get("source_span_sha256", row["source"]["span_sha256"]) != row["source"]["span_sha256"]:
                        raise ValueError(f"REVIEW_SOURCE_CHANGED: {identifier}")
                    if not row["review"].get("scope_statement"):
                        raise ValueError(f"SCOPE_STATEMENT_MISSING: {identifier}")
                elif row["scope_verdict"] == "UNRESOLVED":
                    required_string(row["gap"], identifier + ".scope_gap")
                elif not row["review"]:
                    raise ValueError(f"CONTEXT_REVIEW_MISSING: {identifier}")
            elif kind == "tree":
                links(row, "claim_ids", {"claim"})
                links(row, "verification", {"replay"})
                if not row["files"]:
                    raise ValueError(f"TREE_FILES_EMPTY: {identifier}")
            elif kind in {"stage", "frontier"}:
                links(row, "claim_ids", {"claim"})
            elif kind == "bridge":
                proofs = links(row, "proof_ids", {"theorem"})
                links(row, "countermodel_ids", {"countermodel"})
                if row["gap"] is None and (not row["proof_ids"] or any(not row[field] for field in
                     ("source_carrier", "target_carrier", "source_steps", "target_steps", "supported_domain", "state_maps", "event_maps", "direction", "identity_composition", "refusal_guard"))):
                    raise ValueError(f"BRIDGE_CONTRACT_INCOMPLETE: {identifier}")
                if row["gap"] is None:
                    for proof in proofs:
                        checked_evidence(proof)
            elif kind in {"theorem", "computation"}:
                if row["gap"] is None:
                    checked_evidence(row)
                elif kind == "theorem" and row["build_receipt"] is not None:
                    link(row["build_receipt"], {"replay"}, identifier)
                elif kind == "computation" and row["replay_receipt"] is not None:
                    link(row["replay_receipt"], {"replay"}, identifier)
            elif kind == "countermodel":
                link(row["negated_claim_id"], {"claim"}, identifier)
                links(row, "retained_assumptions", {"assumption"})
                if row["gap"] is None:
                    if not row["witness"] or not row["checker"] or not row["removed_assumption"]:
                        raise ValueError(f"COUNTERMODEL_INCOMPLETE: {identifier}")
                    checked_evidence(row)
            elif kind == "replay":
                if type(row["exit_code"]) is not int or not isinstance(row["command"], list) or not row["command"]:
                    raise ValueError(f"REPLAY_COMMAND_OR_EXIT_INVALID: {identifier}")
                if row["result"] == "PASSED":
                    successful_replay(identifier, identifier)
                elif row["result"] != "FAILED" or row["exit_code"] == 0 or row["source_snapshot"] != snapshot.snapshot or not row["gap"]:
                    raise ValueError(f"FAILED_REPLAY_INCOMPLETE: {identifier}")
            elif kind == "edge":
                if row["kind"] not in specification["edge_kinds"]:
                    raise ValueError(f"EDGE_KIND_INVALID: {identifier}")
                link(row["from"], set(groups), identifier)
                targets = {"uses-assumption": {"assumption"}, "depends-on-proof": {"theorem", "claim"},
                           "refuted-by": {"countermodel"}, "simulates": {"bridge"}, "supersedes": {"claim", "theorem"}}
                link(row["to"], targets[row["kind"]], identifier)

    if expected_headlines is not None and {row["id"] for row in groups["headline"]} != expected_headlines:
        raise ValueError("HEADLINE_POPULATION_MISMATCH")
    if expected_trees is not None and {row["name"] for row in groups["tree"]} != expected_trees:
        raise ValueError("TREE_POPULATION_MISMATCH")
    if expected_headlines is not None and not expected_headlines:
        raise ValueError("HEADLINE_POPULATION_EMPTY")
    proof_edges = [(row["from"], row["to"]) for row in groups["edge"] if row["kind"] == "depends-on-proof"]
    ranks = topological_ranks(sorted(registry), proof_edges)
    historical = [(row["from"], row["to"]) for row in groups["edge"] if row["kind"] == "supersedes"]
    topological_ranks(sorted(registry), historical)
    return ranks
