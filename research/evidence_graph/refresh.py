"""Incremental current-head views without rewriting historical evidence.

The full source/headline/tree census is always refreshed. Only records directly
bound to a changed source, and their dependency descendants, are recomputed.
AuthorityEffect: None.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from eg_census import headlines, research_rows
from eg_sources import HERE, Snapshot, canonical, digest, git, load_snapshot, read_object


def source_paths(value: object) -> set[str]:
    if isinstance(value, dict):
        result = {value["path"]} if "span_sha256" in value and isinstance(value.get("path"), str) else set()
        for child in value.values():
            result.update(source_paths(child))
        return result
    if isinstance(value, list):
        return set().union(*(source_paths(child) for child in value))
    return set()


def referenced_ids(value: object, registry: set[str]) -> set[str]:
    if isinstance(value, str):
        return {value} & registry
    if isinstance(value, dict):
        return set().union(*(referenced_ids(child, registry) for key, child in value.items() if key != "id"))
    if isinstance(value, list):
        return set().union(*(referenced_ids(child, registry) for child in value))
    return set()


def affected_records(graph: dict[str, Any], changed_paths: set[str]) -> set[str]:
    rows = {row["id"]: row for group in graph["records"].values() for row in group}
    registry = set(rows)
    affected = {key for key, row in rows.items() if source_paths(row) & changed_paths}
    descendants: dict[str, set[str]] = defaultdict(set)
    for key, row in rows.items():
        for target in referenced_ids(row, registry) - {key}:
            descendants[target].add(key)
    # A typed dependency also relates the actual endpoints, not only its edge record.
    for edge in graph["records"]["edge"]:
        if edge["kind"] != "supersedes":
            descendants[edge["to"]].add(edge["from"])
    waiting = deque(sorted(affected))
    while waiting:
        for dependent in descendants[waiting.popleft()] - affected:
            affected.add(dependent)
            waiting.append(dependent)
    return affected


def refresh_views(graph: dict[str, Any], changed_paths: set[str], previous: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {row["id"]: row for group in graph["records"].values() for row in group}
    fingerprint = digest(canonical(graph))
    if previous is not None and (previous["graph_sha256"] != fingerprint or set(previous["views"]) != set(rows)):
        raise ValueError("REFRESH_CACHE_POPULATION_CHANGED")
    affected = affected_records(graph, changed_paths)
    recompute = set(rows) if previous is None else affected_records(graph, changed_paths | set(previous["changed_paths"]))
    views = {} if previous is None else dict(previous["views"])
    for key in sorted(recompute):
        views[key] = {"id": key, "historical_source_snapshot": graph["source_snapshot"],
                      "current_applicability": "INVALIDATED_FOR_CURRENT_HEAD" if key in affected else "HISTORICAL_INPUTS_UNCHANGED",
                      "requires_replay": key in affected,
                      "boundary": "This view never changes the historical evidence's source head or claims a fresh replay."}
    return {"graph_sha256": fingerprint, "changed_paths": sorted(changed_paths), "views": views,
            "recomputed_ids": sorted(recompute), "reused_ids": sorted(set(rows) - recompute), "invalidated_ids": sorted(affected)}


def refresh(head: str, previous: dict[str, Any] | None = None) -> dict[str, Any]:
    snapshot = load_snapshot()
    graph = read_object(HERE / "evidence" / "graph.json.gz")
    head_sha = git(snapshot.repo, "rev-parse", head).decode().strip()
    current = Snapshot(snapshot.repo, head_sha)
    config = read_object(HERE / "input.json")
    current_rows = research_rows(current)
    old_trees = {row["name"] for row in graph["records"]["tree"]}
    new_trees = {row["name"] for row in current_rows}
    old_heads = {row["id"] for row in graph["records"]["headline"]}
    new_heads = {row["id"] for row in headlines(current, config)}
    drift = snapshot.drift(head_sha)
    views = refresh_views(graph, {row["path"] for row in drift}, previous)
    return {"source_snapshot": snapshot.snapshot, "execution_head": head_sha,
            "execution_tree": git(snapshot.repo, "rev-parse", head_sha + "^{tree}").decode().strip(),
            "authority_effect": "None", "source_drift": drift,
            "source_population_retained": len(snapshot.files), "execution_source_files": len(current.files),
            "source_tree_count": len(old_trees), "execution_tree_count": len(new_trees),
            "added_trees": sorted(new_trees - old_trees), "removed_trees": sorted(old_trees - new_trees),
            "consumer_tree": "evidence_graph", "consumer_policy": "The new consumer is reconciled as an addition, not silently inserted into its own frozen source population.",
            "new_headlines_requiring_review": sorted(new_heads - old_heads), "removed_or_changed_headlines": sorted(old_heads - new_heads),
            "historical_headline_count_retained": len(old_heads), "execution_headline_count": len(new_heads), "incremental": views}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(HERE.resolve()):
        raise ValueError("CURRENT_HEAD_METADATA_MUST_BE_EXTERNAL")
    previous = None if args.previous is None else read_object(args.previous)["incremental"]
    result = refresh(args.head, previous)
    args.output.write_bytes(canonical(result))
    print(f"refreshed {result['execution_tree_count']} trees; added={result['added_trees']} removed={result['removed_trees']}; historical census retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
