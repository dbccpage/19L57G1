"""Estate entry points and explicit unexecuted dispositions. AuthorityEffect: None."""
from __future__ import annotations

import ast
from pathlib import PurePosixPath
from typing import Any

from eg_census import import_census, research_rows
from eg_sources import Snapshot

VERIFIERS = ("verify.py", "verify_sources.py", "verify_pins.py", "verify_manifest.py", "source_manifest.py", "verify_lean.py")
CONTRACT_NAMES = {"PROMPT.md", "PLAN.md", "SEED.md", "MANUAL.md", "TREE_CONTRACT.json", "SOURCE_MANIFEST.json"}


def declared_options(text: str) -> set[str]:
    module = ast.parse(text.removeprefix("\ufeff"))
    return {argument.value for node in ast.walk(module)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument"
            for argument in node.args if isinstance(argument, ast.Constant) and isinstance(argument.value, str)}


def tree_inventory(snapshot: Snapshot, imports: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    census = import_census(snapshot) if imports is None else imports
    snapshot.preload([path for path in snapshot.files if path.startswith("research/") and path.endswith(".py")])
    result: list[dict[str, Any]] = []
    for row in research_rows(snapshot):
        name = row["name"]
        prefix = f"research/{name}/"
        files = sorted(path for path in snapshot.files if path.startswith(prefix))
        entrypoints = [prefix + candidate for candidate in VERIFIERS if prefix + candidate in snapshot.files]
        # Also expose nonstandard root verifiers; an unknown interface is not run by guesswork.
        entrypoints += [path for path in files if PurePosixPath(path).parent.as_posix() == prefix[:-1]
                        and PurePosixPath(path).name.startswith("verify") and path.endswith(".py") and path not in entrypoints]
        commands = []
        for path in sorted(entrypoints):
            options = declared_options(snapshot.text(path))
            argv = ["python", PurePosixPath(path).name]
            if "--check" in options:
                argv.append("--check")
            commands.append({"source": snapshot.reference(path), "argv": argv, "cwd": prefix[:-1],
                             "role": "complete" if path == prefix + "verify.py" else "specialized",
                             "execution": "PENDING_INTERFACE_REVIEW",
                             "gap": "Run this tree's own checker in isolated custody after reviewing its write behavior; do not substitute an aggregate helper."})
        result.append({"id": "tree:" + name, "name": name, "source_snapshot": snapshot.snapshot,
                       "files": files, "entrypoints": entrypoints,
                       "contracts": [path for path in files if PurePosixPath(path).name in CONTRACT_NAMES],
                       "import_files": [item for item in census["files"] if item["source"]["path"].startswith(prefix)],
                       "pin_files": [path for path in files if path.endswith(".json") and any(token in PurePosixPath(path).name.upper() for token in ("MANIFEST", "PIN"))],
                       "verifier_commands": commands, "registration": row["registration"],
                       "maintenance_status": row["maintenance_status"], "claim_ids": [],
                       "last_checked_source_head": None, "verification": [],
                       "gap": "Source inventory is inspected; independent evidence replay has not yet been recorded." if commands else
                              "No tree-root independent verifier was found; inspect the declared tests, receipts, and build entry points separately."})
    return result


def require_local_verifier(tree: dict[str, Any], argv: list[str], cwd: str) -> dict[str, Any]:
    """A shared helper cannot be accepted as a tree's independent check."""
    candidates = [row for row in tree["verifier_commands"] if row["argv"] == argv and row["cwd"] == cwd]
    if len(candidates) != 1:
        raise ValueError(f"INDEPENDENT_VERIFIER_SUBSTITUTED: {tree['name']}: {argv}")
    row: dict[str, Any] = candidates[0]
    if not row["source"]["path"].startswith(f"research/{tree['name']}/"):
        raise ValueError(f"INDEPENDENT_VERIFIER_ORIGIN: {tree['name']}")
    return row
