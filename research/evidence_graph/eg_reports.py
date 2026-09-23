"""Fresh compiled report framing and payload validation. AuthorityEffect: None."""
from __future__ import annotations

import json
import re
from typing import Any

from eg_sources import HERE, canonical, digest

MODULE = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*")


def report_program(modules: list[str]) -> bytes:
    if not modules or len(modules) != len(set(modules)) or any(not MODULE.fullmatch(m) for m in modules):
        raise ValueError("REPORT_MODULE_POPULATION")
    template = (HERE / "compiled_report.lean.in").read_text(encoding="utf-8")
    return template.replace("@@IMPORTS@@", "\n".join("import " + m for m in sorted(modules))).replace(
        "@@MODULES@@", "#[" + ", ".join(json.dumps(m) for m in sorted(modules)) + "]").encode("utf-8")


def parse_report(output: str, modules: list[str]) -> dict[str, Any]:
    observed: list[str] = []
    records: list[dict[str, Any]] = []
    terminal: list[dict[str, int]] = []
    reach: list[list[str]] = []
    for line in output.splitlines():
        if line.startswith("EG_REACH "):
            reach.append(json.loads(line[len("EG_REACH "):]))
        elif line.startswith("EG_MODULE "):
            observed.append(json.loads(line[len("EG_MODULE "):]))
        elif line.startswith("EG_THEOREM "):
            row = json.loads(line[len("EG_THEOREM "):])
            if set(row) != {"module", "declaration", "kind", "elaborated_type", "local_hypotheses", "conclusion", "axioms"}:
                raise ValueError("COMPILED_REPORT_FIELDS")
            if row["module"] not in modules or not row["elaborated_type"] or not isinstance(row["local_hypotheses"], list):
                raise ValueError("COMPILED_REPORT_SCOPE")
            row["axioms"] = sorted(row["axioms"])
            records.append(row)
        elif line.startswith("EG_END "):
            terminal.append(json.loads(line[len("EG_END "):]))
        elif "EG_" in line:
            raise ValueError("COMPILED_REPORT_UNFRAMED")
    if sorted(observed) != sorted(modules) or len(terminal) != 1 or len(reach) != 1 or not set(modules) <= set(reach[0]):
        raise ValueError("COMPILED_MODULE_POPULATION")
    if terminal[0] != {"modules": len(modules), "theorems": len(records)} or not records:
        raise ValueError("COMPILED_THEOREM_POPULATION")
    records.sort(key=lambda row: (row["module"], row["declaration"]))
    if len({row["declaration"] for row in records}) != len(records):
        raise ValueError("COMPILED_THEOREM_DUPLICATE")
    return {"modules": sorted(modules), "theorems": records, "payload_sha256": digest(canonical(records)),
            "compiled_environment_reach": sorted(reach[0]),
            "reach_scope": "Environment after importing all selected product modules plus the report observer's Lean apparatus imports; not the product root's default-target closure."}


def validate_payload(report: dict[str, Any]) -> None:
    if not report["theorems"] or report["payload_sha256"] != digest(canonical(report["theorems"])):
        raise ValueError("COMPILED_PAYLOAD_CHANGED")
