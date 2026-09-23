"""Ingest source assertions and independently captured evidence. AuthorityEffect: None."""
from __future__ import annotations

from collections import defaultdict
import re
from typing import Any

from eg_claims import LedgerEntry, claim_inventory
from eg_census import headlines, import_census
from eg_inventory import tree_inventory
from eg_reports import report_program, validate_payload
from eg_schema import validate
from eg_sources import HERE, Snapshot, canonical, digest, read_object


def source_refs(snapshot: Snapshot, paths: list[str]) -> list[dict[str, Any]]:
    return [dict(snapshot.reference(path)) for path in sorted(set(paths)) if snapshot.files[path].size]


def ingest_capture(snapshot: Snapshot, capture: dict[str, Any], groups: dict[str, list[dict[str, Any]]]) -> None:
    if capture["source_snapshot"] != snapshot.snapshot:
        raise ValueError("CAPTURE_WRONG_HEAD")
    runs = {row["id"]: row for row in capture["runs"]}
    if len(runs) != len(capture["runs"]):
        raise ValueError("CAPTURE_RUN_DUPLICATE")
    for run in capture["runs"]:
        if run["source_snapshot"] != snapshot.snapshot:
            raise ValueError("REPLAY_WRONG_HEAD")
        if run["source_tree"] != read_object(HERE / "source_population.json")["tree"]:
            raise ValueError("REPLAY_WRONG_TREE")
        cwd = run["cwd"]
        paths = [path for path in snapshot.files if path.startswith(cwd + "/") and path.endswith((".py", ".lean", ".toml", ".json"))]
        # The full input tree is separately bound by capture.source_tree; these are the local file references.
        groups["replay"].append({"id": "replay:" + run["id"], "source_snapshot": snapshot.snapshot,
            "tree": cwd.split("/")[1] if cwd.startswith("research/") else "sealed_core", "command": run["command"],
            "cwd": cwd, "input_sources": source_refs(snapshot, paths), "output_digest": run["output_digest"],
            "exit_code": run["exit_code"], "receipt_sources": source_refs(snapshot, [path for path in paths if "/evidence/" in path or "/receipts/" in path]),
            "result": run["result"], "gap": run["gap"]})
    for report in capture["reports"]:
        validate_payload(report)
        if report["source_snapshot"] != snapshot.snapshot or digest(report_program(report["modules"])) != report["report_program_sha256"]:
            raise ValueError("COMPILED_REPORT_SOURCE_CHANGED")
        for field in ("build_id", "report_id"):
            if report[field] not in runs or runs[report[field]]["result"] != "PASSED":
                raise ValueError("COMPILED_REPORT_REPLAY_MISSING")
        populations: dict[str, list[str]] = defaultdict(list)
        for theorem in report["theorems"]:
            populations[theorem["module"]].append(theorem["declaration"])
        for theorem in report["theorems"]:
            module = theorem["module"]
            groups["theorem"].append({"id": f"theorem:{report['package']}::{theorem['declaration']}",
                "source": snapshot.reference(report["module_sources"][module]), "module": module,
                "declaration": theorem["declaration"], "kind": theorem["kind"],
                "elaborated_type": theorem["elaborated_type"], "local_hypotheses": theorem["local_hypotheses"],
                "axioms": theorem["axioms"], "report_population": sorted(populations[module]),
                "build_receipt": "replay:" + report["report_id"], "gap": None})


def link_citations(snapshot: Snapshot, groups: dict[str, list[dict[str, Any]]], entries: dict[str, LedgerEntry]) -> dict[str, list[dict[str, Any]]]:
    """Resolved names are candidate links only; no scope verdict follows from them."""
    exact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    short: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for theorem in groups["theorem"]:
        exact[theorem["declaration"]].append(theorem)
        short[theorem["declaration"].rsplit(".", 1)[-1]].append(theorem)
    unresolved: dict[str, list[dict[str, Any]]] = {}
    for claim in groups["claim"]:
        entry = entries.get(claim["id"])
        if entry is None:
            continue
        refs = [reference for field, reference in entry.fields.items() if field in {"lean", "evidence"}]
        if not refs and entry.source == entry.statement:
            refs = [entry.source]
        tokens = {token for reference in refs for token in re.findall(r"`([A-Za-z_][\w'.]*(?:\.[\w']+)*)`", snapshot.resolve(reference))}
        found = []
        missing = []
        root = "/".join(entry.source["path"].split("/")[:2]) if entry.source["path"].startswith("research/") else "lean4/"
        for token in sorted(tokens):
            candidates = exact.get(token, []) or short.get(token, [])
            local = [t for t in candidates if t["source"]["path"].startswith(root)]
            candidates = local or candidates
            if len(candidates) == 1:
                found.append(candidates[0]["id"])
            elif token not in {"None", "True", "False", "OPEN"}:
                missing.append(token)
        claim["evidence_ids"] = sorted(set(found))
        if missing:
            unresolved[claim["id"]] = [{"token_sha256": digest(token.encode("utf-8")), "source": entry.source,
                "gap": "No unique compiled theorem match; the source token may instead name data, an entry point, or an unreported declaration."} for token in missing]
    return unresolved


def reviewed_claim(snapshot: Snapshot, groups: dict[str, list[dict[str, Any]]], *, identifier: str,
                   text: str, source: dict[str, Any], evidence: list[str], lineage: str,
                   parents: list[str] | None = None, public_id: str | None = None) -> dict[str, Any]:
    theorems = {t["id"]: t for t in groups["theorem"]}
    selected = [theorems[key] for key in evidence]
    assumptions = []
    for theorem in selected:
        for index, binder in enumerate(theorem["local_hypotheses"]):
            key = f"assumption:{identifier}:{theorem['declaration']}:{index}"
            assumptions.append(key)
            groups["assumption"].append({"id": key, "statement": {"source": theorem["source"], "text": binder},
                "source_class": "supplied object-language datum", "gap": None})
    row = {"id": identifier, "public_id": public_id, "statement": {"source": source, "text": text},
        "source_class": "proved theorem", "status": "CONDITIONAL" if assumptions else "PROVED_THEOREM",
        "lineage": lineage, "bounds": [], "assumption_ids": assumptions, "parent_bridge_ids": parents or [],
        "evidence_ids": evidence, "gap": None}
    groups["claim"].append(row)
    for key in evidence:
        groups["edge"].append({"id": f"edge:{identifier}:{key}", "kind": "depends-on-proof", "from": identifier,
            "to": key, "source": source, "gap": None})
    for key in assumptions:
        groups["edge"].append({"id": f"edge:{identifier}:{key}", "kind": "uses-assumption", "from": identifier,
            "to": key, "source": source, "gap": None})
    return row


def graph_base(snapshot: Snapshot, capture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    specification = read_object(HERE / "SCHEMA.json")
    config = read_object(HERE / "input.json")
    graph: dict[str, Any] = {"schema": 1, "source_snapshot": snapshot.snapshot, "authority_effect": "None",
                             "records": {kind: [] for kind in specification["record_fields"]}}
    groups = graph["records"]
    imports = import_census(snapshot)
    groups["tree"] = tree_inventory(snapshot, imports)
    groups["headline"] = headlines(snapshot, config)
    groups["claim"], entries = claim_inventory(snapshot, config, groups["headline"])
    ingest_capture(snapshot, capture, groups)
    unresolved = link_citations(snapshot, groups, entries)
    for tree in groups["tree"]:
        prefix = "research/" + tree["name"] + "/"
        tree["claim_ids"] = [claim["id"] for claim in groups["claim"] if claim["statement"]["path"].startswith(prefix)]
        own = [run for run in groups["replay"] if run["tree"] == tree["name"]]
        tree["verification"] = [run["id"] for run in own]
        independent = [run for run in own if run["id"].startswith("replay:independent:")]
        tree["last_checked_source_head"] = snapshot.snapshot if independent else None
        tree["gap"] = ("Inspected source and verifier interfaces; no independent replay was selected for this capture. All source claims remain individually classified."
                       if not independent else "Independent command dispositions and any failures are recorded below. A replay or build does not certify every public statement of this tree.")
        for command in tree["verifier_commands"]:
            matches = [run for run in independent if run["command"] == command["argv"] and run["cwd"] == command["cwd"]]
            command["execution"] = matches[0]["result"] if matches else "NOT_REPLAYED"
            command["gap"] = matches[0]["gap"] if matches else "This specific independent command was not replayed in the captured population."
    return graph, {"imports": imports,
                   "identifier_policy": "Exact existing IDs remain in the graph. This secondary view joins by SHA-256 of the UTF-8 claim ID and binds the original ID to its source span.",
                   "unresolved_citation_tokens": {digest(key.encode("utf-8")): value for key, value in sorted(unresolved.items())},
                   "ledger_population": [{"claim_id_sha256": digest(key.encode("utf-8")), "public_id_sha256": digest(entry.public_id.encode("utf-8")), "source": entry.source, "statement": entry.statement,
                                           "fields": entry.fields} for key, entry in sorted(entries.items())]}


def validate_complete(graph: dict[str, Any], snapshot: Snapshot) -> None:
    expected = headlines(snapshot, read_object(HERE / "input.json"))
    trees = tree_inventory(snapshot)
    validate(graph, snapshot, expected_headlines={row["id"] for row in expected}, expected_trees={row["name"] for row in trees})


def theorem_scope_digest(row: dict[str, Any]) -> str:
    return digest(canonical({"type": row["elaborated_type"], "hypotheses": row["local_hypotheses"]}))
