"""Coverage, import populations and owner handoff views. AuthorityEffect: None."""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import PurePosixPath
import re
from typing import Any

from eg_census import lean_imports
from eg_sources import Snapshot


def enrich_imports(snapshot: Snapshot, imports: dict[str, Any], capture: dict[str, Any]) -> dict[str, Any]:
    packages = sorted({str(PurePosixPath(path).parent) for path in snapshot.files
                       if PurePosixPath(path).name in {"lakefile.toml", "lakefile.lean"}}, key=len, reverse=True)
    module_files: dict[str, list[str]] = defaultdict(list)
    headers: dict[str, list[str]] = {}
    owner: dict[str, str] = {}
    for path in snapshot.files:
        if not path.endswith(".lean") or path.endswith("/lakefile.lean"):
            continue
        package = next((p for p in packages if path.startswith(p + "/")), None)
        if package is None:
            continue
        owner[path] = package
        module_files[path[len(package) + 1:-5].replace("/", ".")].append(path)
        headers[path] = lean_imports(snapshot.text(path))
    dependencies = {row["source"]["path"]: row for row in capture["dependencies"]}
    reports = {row["package"]: row for row in capture["reports"]}

    def closure(start: str) -> tuple[list[str], list[str]]:
        visited: set[str] = set()
        native: set[str] = set()
        unresolved: set[str] = set()
        waiting = [start]
        while waiting:
            path = waiting.pop()
            if path in visited:
                continue
            visited.add(path)
            for module in headers.get(path, []):
                if module == "Derivation" or module.startswith("Derivation."):
                    native.add(module)
                candidates = module_files.get(module, [])
                local = [p for p in candidates if owner.get(p) == owner.get(path)]
                selected = local or candidates
                if len(selected) == 1:
                    waiting.append(selected[0])
                elif module not in {"Init", "Lean", "Lake", "Std"} and not module.startswith(("Init.", "Lean.", "Lake.", "Std.")):
                    unresolved.add(module)
        return sorted(native), sorted(unresolved)

    for row in imports["files"]:
        path = row["source"]["path"]
        native, unresolved = closure(path)
        row["static_transitive_native_modules"] = native
        row["static_unresolved_imports"] = unresolved
        row["package"] = owner.get(path)
        row["compiler_dependencies"] = dependencies.get(path)
        report = reports.get(owner.get(path, ""))
        row["compiled_reach"] = None if report is None else {
            "report_id": report["report_id"], "selected_modules": report["modules"],
            "native_modules_in_environment": [m for m in report["compiled_environment_reach"] if m == "Derivation" or m.startswith("Derivation.")],
            "scope": report["reach_scope"]}
        if path in dependencies and dependencies[path]["result"] == "PASSED":
            observed = dependencies[path]["dependencies"]
            missing = [module for module in row["direct_native_imports"] if not any(p.endswith(module.replace(".", "/") + ".olean") for p in observed)]
            if missing:
                raise ValueError(f"COMPILER_NATIVE_IMPORT_MISMATCH: {path}: {missing}")
            row["gap"] = None if not unresolved else "Static cross-package resolution is incomplete; the captured compiler population is reported separately."
        else:
            row["gap"] = "Header and static transitive dependencies were inspected; no successful compiler dependency output is recorded for this file."
    imports["reconciliation"] = {
        "supplied_count": 38, "supplied_named_population": None,
        "header_count": len(imports["direct_files"]), "header_trees": len(imports["direct_trees"]),
        "resolution": "The independently saved header population has 35 files in 22 trees. Four additional files have only comment mentions. The supplied count 38 has no attached file population, so its exact counting error cannot be reconstructed; it is not adopted as a verified census.",
        "configuration_files": [row["source"]["path"] for row in imports["files"] if row["configuration"]],
        "compiler_checked_files": sorted(dependencies),
        "compiler_checked_direct_files": sorted(path for path in imports["direct_files"] if path in dependencies and dependencies[path]["result"] == "PASSED"),
        "scope": "Imports establish dependencies only. Static unresolved modules, report apparatus and product modules remain distinct."}
    return imports


HANDOFF_SUBJECTS = [
    ("initial_descriptor", "paper/native_derivation_completion.md", r"initial member", "The final conclusion still says initial; the earlier section states unique probe-compliance in 64 descriptors plus one split retract. No wider universal property follows.", "lean4/Derivation/Initiality.lean"),
    ("cell_relations", "research/g013_trace_calculus/", r"commut|coher|interchange|2-cell|2-category", "Cell constructors and reflexive coherence facts do not prove the additional composition/quotient laws or a guarded-native-step bridge. Preserve any narrower supported trace and price facts.", "research/g013_trace_calculus/lean/HigherCell.lean"),
    ("self_evaluation", "research/g018_self_hosting/", r"oracle|diagonal|self.*obstruction", "The compiled diagonal result excludes a row of a supplied Boolean table equal to its negated diagonal. It does not connect the Python predictor to one encoded machine and its own evaluation; the executable self-oracle application needs that representation/evaluation bridge.", "research/g018_self_hosting/lean/Obstruction.lean"),
    ("matrix_scope", "research/p209b_clifford_symplectic/", r"arbitrary|quotient|obstruction|general", "The reported matrix scope is the six displayed two-element-field matrices and their declared closure. General parameter and obstruction wording needs independent same-scope evidence.", "research/p209b_clifford_symplectic/lean/CliffordSymplectic.lean"),
    ("trace_domain", "research/p208c_commutator_tomography/", r"characteristic|field|commutator|trace", "The compiled trace and commutator theorem is over integer matrices. A field-generic statement needs a different typed result.", "research/p208c_commutator_tomography/lean/CommutatorTomography.lean"),
    ("codec_native", "research/g012_typed_translation/", r"native|isomorph|codec|commut|derivation", "A string codec with removal operations needs an actual state/step bridge to the monotone admission grammar; similarly named fields do not supply one.", "research/g012_typed_translation/codec.py"),
    ("pipeline_native", "research/x310_vertical_integration/", r"commut|carrier|six|integration|isomorph", "The audit uses a separately constructed sample carrier; prove the required squares on the live carrier and preserve all declared metadata before claiming full integration.", "research/x310_vertical_integration/commutation.py"),
    ("registered_count", "README.md", r"four registered", "The source index records twelve gate-11 trees. The older four-tree statement is a source-head documentation mismatch.", "research/README.md"),
    ("policy_custody", "paper/paper.md", r"policy|outside|vocabulary", "Repository vocabulary and the governing exclusion require an author-owned policy reconciliation. This consumer copies source spans by reference and makes no contract amendment.", "CLAUDE.md"),
]


def handoff_queue(snapshot: Snapshot, graph: dict[str, Any]) -> dict[str, Any]:
    rows = []
    groups = graph["records"]
    for name, root, pattern, scope, evidence_path in HANDOFF_SUBJECTS:
        candidates = [row for row in groups["headline"] if row["source"]["path"].startswith(root)
                      and re.search(pattern, snapshot.resolve(row["source"]), re.IGNORECASE)]
        if not candidates:
            raise ValueError("HANDOFF_SPAN_MISSING: " + name)
        rows.append({"id": "handoff:" + name, "owner": "section_3", "disposition": "UNRESOLVED_AT_SOURCE_SNAPSHOT",
                     "headline_ids": [row["id"] for row in candidates], "sources": [row["source"] for row in candidates],
                     "scope": scope, "evidence_source": snapshot.reference(evidence_path),
                     "theorem_ids": [row["id"] for row in groups["theorem"] if row["source"]["path"] == evidence_path],
                     "action": "Ingest an author-merged correction as a new source version; preserve this historical snapshot. Do not edit these sources in the evidence consumer."})
        for headline in candidates:
            if headline["scope_verdict"] != "MATCHED":
                headline["gap"] = scope
                headline["review"]["handoff_id"] = "handoff:" + name
    return {"source_snapshot": snapshot.snapshot, "authority_effect": "None", "items": rows,
            "scope": "A handoff identifies a scope question for its owner. It does not pronounce every selected sentence false; neighboring qualified and historical sentences remain context."}


def coverage(graph: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    groups = graph["records"]
    statuses = Counter(row["scope_verdict"] for row in groups["headline"])
    runs = [r for r in groups["replay"] if r["id"].startswith("replay:independent:")]
    summary = {"source_trees": len(groups["tree"]), "public_files": len({r["source"]["path"] for r in groups["headline"]}),
        "public_blocks": len(groups["headline"]), "ledger_entries": len(detail["ledger_population"]),
        "claims": len(groups["claim"]), "compiled_theorems": len(groups["theorem"]),
        "scope_verdicts": dict(sorted(statuses.items())), "claim_statuses": dict(sorted(Counter(r["status"] for r in groups["claim"]).items())),
        "independent_commands": len(runs), "independently_replayed_trees": len({r["tree"] for r in runs}),
        "independent_results": dict(sorted(Counter(r["result"] for r in runs).items())),
        "inventory_complete": True, "all_headlines_supported": statuses["UNRESOLVED"] == 0,
        "interpretation": "Complete source-block disposition is distinct from mathematical adequacy. Unreviewed metadata, listings and historical prose are conservatively unresolved, so the unresolved count is not a count of false theorems."}
    return {"source_snapshot": graph["source_snapshot"], "authority_effect": "None", "summary": summary,
            "headline_dispositions": [{"id": row["id"], "source": row["source"], "verdict": row["scope_verdict"],
                                        "claim_ids": row["claim_ids"], "gap": row["gap"]} for row in groups["headline"]]}


def dependent_handoff(graph: dict[str, Any]) -> dict[str, Any]:
    rows = [
        ("C", ["claim:scoped:aligned_replay", "claim:scoped:legal_replay", "bridge:typed_trace_erasure", "bridge:token_erasure"],
         "Start with the actual native state, event, guard and typed-record maps. Additional reverse maps and event selection remain obligations."),
        ("D", ["claim:scoped:rewrite_sound", "claim:scoped:price_premise", "claim:research/path_dependent_cost/CLAIM_LEDGER.md::PD-3", "claim:research/path_dependent_cost/CLAIM_LEDGER.md::PD-5", "bridge:cells_native"],
         "Keep the action, branch-cost equality, congruence, invariance and guard hypotheses separate. The open cell bridge must not be replaced by matching names."),
        ("E", ["precedent:additive_cost", "precedent:budget_accounting", "precedent:signed_boundary", "precedent:path_cost"],
         "No broad conserved-charge theorem is supplied by these precedents. A common native transition domain and every extra premise must be specified first."),
        ("F", ["bridge:represented_readback", "bridge:pipeline_carrier", "frontier:driver_b", "frontier:analytic_limit", "frontier:demand_channel"],
         "Declare every imported carrier and law, prove each claimed state/step/observation map, and preserve proposal/evaluation/license distinctions."),
    ]
    registry = {r["id"] for group in graph["records"].values() for r in group}
    if any(identifier not in registry for _, identifiers, _ in rows for identifier in identifiers):
        raise ValueError("DEPENDENT_HANDOFF_LINK_MISSING")
    return {"source_snapshot": graph["source_snapshot"], "authority_effect": "None",
            "plans": [{"plan": plan, "input_ids": identifiers, "boundary": boundary} for plan, identifiers, boundary in rows]}


def markdown(graph: dict[str, Any], report: dict[str, Any], imports: dict[str, Any]) -> bytes:
    groups, summary = graph["records"], report["summary"]
    lines = ["# Evidence coverage", "", "AuthorityEffect: None.", "", f"Source snapshot: `{graph['source_snapshot']}`.", "",
        f"The source inventory is complete: {summary['source_trees']} trees, {summary['public_files']} public files and {summary['public_blocks']} nonblank text blocks.",
        f"The stronger all-headlines-supported criterion is **unmet**: {summary['scope_verdicts'].get('UNRESOLVED', 0)} blocks have explicit unresolved dispositions.",
        "This conservative number includes metadata, listings and historical prose; it is not a count of false mathematical claims.", "",
        f"Fresh compiled reports contain {summary['compiled_theorems']} theorem records (including generated public theorems, excluding compiler-internal names).",
        f"Independent commands: {summary['independent_commands']} across {summary['independently_replayed_trees']} trees; results `{summary['independent_results']}`.",
        "A successful specialized check, a successful build and a successful complete verifier have different scopes. The graph does not replace any independent checker.", "",
        "## Reading the artifacts", "", "- `graph.json.gz`: scoped records and typed links; deterministic gzip of canonical JSON.", "- `coverage.json.gz`: every public span and its disposition.",
        "- `capture.json`: independently observed commands, theorem types, binders, axioms and compiler dependencies.",
        "- `ledgers.json`: source-bound ledger population and unresolved citation digests; joins to exact graph IDs by their UTF-8 SHA-256.",
        "- `imports.json`: exact header, comment, static-transitive and compiler populations.",
        "- `section3_handoff.json`: source spans and scope boundaries for the separate correction owner.",
        "- `handoff.json`: input IDs and remaining obligations for dependent work.", "",
        "Use `python query.py --id RECORD_ID` to inspect one record, or `--source PATH --line N` to inspect public text at a source location.", "",
        "## Stages", "", "| Stage | Boundary | Scoped inputs |", "|---|---|---|"]
    for row in groups["stage"]:
        lines.append(f"| {row['stage']} | {row['boundary']} | {', '.join('`'+i+'`' for i in row['claim_ids']) or 'supplied source and definitions'} |")
    lines += ["", "## Import populations", "", imports["reconciliation"]["resolution"], "",
              "The saved compiler reach includes the report observer's apparatus imports; it is not mislabeled as the default product-root closure.", "",
              "| Direct native import source | Compiler check |", "|---|---|"]
    checked = set(imports["reconciliation"]["compiler_checked_direct_files"])
    for path in imports["direct_files"]:
        lines.append(f"| `{path}` | {'captured' if path in checked else 'not replayed'} |")
    lines += ["", "## Research census", "", "| Tree | Registration | Status | Lean files | Test files | Independent command results |", "|---|---|---|---:|---:|---|"]
    runs = {r["id"]: r for r in groups["replay"]}
    for tree in groups["tree"]:
        local = [runs[key] for key in tree["verification"] if key.startswith("replay:independent:")]
        disposition = "; ".join(" ".join(r["command"]) + ": " + r["result"] for r in local) or "inspected; not replayed"
        lean = sum(p.endswith(".lean") and not p.endswith("lakefile.lean") for p in tree["files"])
        tests = sum(PurePosixPath(p).name.startswith("test_") and p.endswith(".py") for p in tree["files"])
        lines.append(f"| `{tree['name']}` | {tree['registration']} | {tree['maintenance_status'] or 'unmarked'} | {lean} | {tests} | {disposition} |")
    lines += ["", "## Open work and precedents", "", "| ID | Disposition | Required evidence or scope |", "|---|---|---|"]
    for row in groups["frontier"]:
        lines.append(f"| `{row['id']}` | {row['disposition']} | {row['required_evidence']} |")
    lines += ["", "Every row is bound to the immutable input snapshot. Run `refresh.py` for current-head drift and added/removed populations; do not silently replace the historical receipt.", ""]
    return "\n".join(lines).encode("utf-8")
