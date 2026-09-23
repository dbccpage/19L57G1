"""Regenerate and check complete graph artifacts twice. AuthorityEffect: None."""
from __future__ import annotations

import argparse
import gzip
from pathlib import Path

from eg_curated import apply_reviews, bridges, finite_fixture, stage_frontier_rows
from eg_graph import graph_base, validate_complete
from eg_sources import HERE, canonical, digest, load_snapshot, read_object
from eg_views import coverage, dependent_handoff, enrich_imports, handoff_queue, markdown

OUTPUTS = {"graph.json.gz", "coverage.json.gz", "imports.json", "ledgers.json", "section3_handoff.json", "handoff.json", "coverage.md", "summary.json", "artifacts.json"}
INPUTS = {"capture.json", "inventory.json.gz"}


def build() -> dict[str, bytes]:
    snapshot = load_snapshot()
    capture = read_object(HERE / "evidence" / "capture.json")
    snapshot.preload(list(snapshot.files))
    graph, detail = graph_base(snapshot, capture)
    groups = graph["records"]
    bridges(snapshot, groups)
    apply_reviews(snapshot, groups)
    finite_fixture(snapshot, groups)
    stage_frontier_rows(snapshot, groups)
    queue = handoff_queue(snapshot, graph)
    for tree in groups["tree"]:
        tree["claim_ids"] = [row["id"] for row in groups["claim"]
                             if row["statement"].get("source", row["statement"])["path"].startswith("research/" + tree["name"] + "/")]
    for rows in groups.values():
        rows.sort(key=lambda row: row["id"])
    imports = enrich_imports(snapshot, detail.pop("imports"), capture)
    validate_complete(graph, snapshot)
    report = coverage(graph, detail)
    values = {"graph.json.gz": graph, "coverage.json.gz": report, "imports.json": imports, "ledgers.json": detail,
              "section3_handoff.json": queue, "handoff.json": dependent_handoff(graph), "summary.json": report["summary"]}
    raw_values = {name: canonical(value) for name, value in values.items()}
    result = {name: gzip.compress(raw, mtime=0) if name.endswith(".gz") else raw for name, raw in raw_values.items()}
    result["coverage.md"] = markdown(graph, report, imports)
    result["artifacts.json"] = canonical({"source_snapshot": snapshot.snapshot, "authority_effect": "None",
        "outputs": {name: {"sha256": digest(raw), "size": len(raw), "decoded_sha256": digest(raw_values.get(name, raw))}
                    for name, raw in sorted(result.items())},
        "capture_sha256": digest((HERE / "evidence" / "capture.json").read_bytes()),
        "scope_reviews_sha256": digest((HERE / "scope_reviews.json").read_bytes())})
    return result


def compare_outputs(directory: Path, expected: dict[str, bytes]) -> None:
    actual = {path.name for path in directory.iterdir() if path.is_file()} - INPUTS
    if actual != OUTPUTS:
        raise ValueError(f"ARTIFACT_POPULATION_MISMATCH: missing={sorted(OUTPUTS-actual)} extra={sorted(actual-OUTPUTS)}")
    for name, raw in expected.items():
        if (directory / name).read_bytes() != raw:
            raise ValueError("GRAPH_ARTIFACT_DIFFERS: " + name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "evidence")
    args = parser.parse_args()
    first, second = build(), build()
    if first != second:
        raise ValueError("GRAPH_REGENERATION_NONDETERMINISTIC")
    if args.write:
        args.output.mkdir(parents=True, exist_ok=True)
        for name, raw in first.items():
            (args.output / name).write_bytes(raw)
    compare_outputs(args.output, first)
    print("PASS: complete source populations, scoped evidence, and two byte-identical graph generations; AuthorityEffect: None")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
