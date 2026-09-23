"""Source populations independent of graph links. AuthorityEffect: None."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re
from typing import Any

from eg_sources import Snapshot, SourceRef, digest


@dataclass(frozen=True)
class Block:
    path: str
    start: int
    end: int
    kind: str
    text: str

    def reference(self, snapshot: Snapshot) -> SourceRef:
        return snapshot.reference(self.path, self.start, self.end)


def public_paths(snapshot: Snapshot, config: dict[str, Any]) -> list[str]:
    roots = tuple(config["public_roots"])
    exclusions = tuple(config["excluded_public_roots"])
    named = set(config["public_files"])
    return sorted(path for path in snapshot.files if path.endswith(".md")
                  and (path in named or path.startswith(roots)) and not path.startswith(exclusions))


def text_blocks(path: str, text: str) -> list[Block]:
    """Cover every nonblank line, including listings and metadata, by one block."""
    lines = text.splitlines(keepends=True)
    result: list[Block] = []
    index = 0
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        start = index
        line = lines[index].lstrip()
        fence = re.match(r"(`{3,}|~{3,})", line)
        if fence:
            token = fence.group(1)
            index += 1
            while index < len(lines) and not re.match(re.escape(token[0]) + "{" + str(len(token)) + r",}\s*$", lines[index].strip()):
                index += 1
            if index < len(lines):
                index += 1
            kind = "listing"
        elif line.startswith("#"):
            index += 1
            kind = "heading"
        elif line.startswith("|"):
            index += 1
            kind = "table_row"
        elif re.match(r"(?:[-*+] |\d+[.)] )", line):
            index += 1
            while index < len(lines) and lines[index].strip() and lines[index][:1].isspace():
                index += 1
            kind = "list_item"
        else:
            index += 1
            while index < len(lines) and lines[index].strip() and not re.match(r"\s*(?:#|\||`{3,}|~{3,}|[-*+] |\d+[.)] )", lines[index]):
                index += 1
            kind = "prose"
        result.append(Block(path, start + 1, index, kind, "".join(lines[start:index])))
    covered = {line for block in result for line in range(block.start, block.end + 1)}
    required = {i + 1 for i, line in enumerate(lines) if line.strip()}
    if not required <= covered:
        raise ValueError(f"TEXT_POPULATION_GAP: {path}")
    return result


def headlines(snapshot: Snapshot, config: dict[str, Any]) -> list[dict[str, Any]]:
    paths = public_paths(snapshot, config)
    if not paths:
        raise ValueError("HEADLINE_POPULATION_EMPTY")
    snapshot.preload(paths)
    result: list[dict[str, Any]] = []
    for path in paths:
        occurrences: Counter[str] = Counter()
        for block in text_blocks(path, snapshot.text(path)):
            anchor = digest(block.text.encode("utf-8"))[:20]
            occurrences[anchor] += 1
            result.append({"id": f"headline:{path}:{anchor}:{occurrences[anchor]}", "source": block.reference(snapshot),
                           "kind": block.kind, "claim_ids": [], "scope_verdict": "UNRESOLVED",
                           "scope_evidence_ids": [], "review": None,
                           "gap": "No same-scope reviewed statement and checked evidence have been assigned to this source block."})
    return result


def blank_lean_comments(text: str, *, strings: bool = False) -> str:
    """Preserve locations while erasing nested comments and optionally strings."""
    out = list(text)
    index, depth = 0, 0
    quoted = False
    while index < len(text):
        if depth:
            if text.startswith("/-", index):
                depth += 1
                width = 2
            elif text.startswith("-/", index):
                depth -= 1
                width = 2
            else:
                width = 1
            for offset in range(width):
                if out[index + offset] != "\n":
                    out[index + offset] = " "
            index += width
        elif quoted:
            width = 2 if text[index] == "\\" and index + 1 < len(text) else 1
            if text[index] == '"':
                quoted = False
            if strings:
                for offset in range(width):
                    if out[index + offset] != "\n":
                        out[index + offset] = " "
            index += width
        elif text.startswith("/-", index):
            depth = 1
            out[index:index + 2] = [" ", " "]
            index += 2
        elif text.startswith("--", index):
            while index < len(text) and text[index] != "\n":
                out[index] = " "
                index += 1
        elif text[index] == '"':
            quoted = True
            if strings:
                out[index] = " "
            index += 1
        else:
            index += 1
    if depth or quoted:
        raise ValueError("LEAN_UNTERMINATED_LEXEME")
    return "".join(out)


MODULE = r"(?:[\w']+|«[^»\n]+»)(?:\.(?:[\w']+|«[^»\n]+»))*"


def lean_imports(text: str) -> list[str]:
    """Read import commands only in the leading header, after comment lexing."""
    lines = blank_lean_comments(text, strings=True).splitlines()
    modules: list[str] = []
    pending = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped in {"prelude", "module"}:
            if pending:
                raise ValueError("LEAN_EMPTY_IMPORT")
            continue
        match = re.fullmatch(r"(?:(?:public|meta)\s+)*import\s*(.*)", stripped)
        if match:
            if pending:
                raise ValueError("LEAN_EMPTY_IMPORT")
            payload = match.group(1)
        elif pending:
            payload = stripped
        else:
            break
        found = re.findall(MODULE, payload)
        residue = re.sub(MODULE, "", payload)
        if residue.strip():
            raise ValueError(f"LEAN_IMPORT_SYNTAX_UNSUPPORTED: {stripped}")
        modules.extend(found)
        pending = not found
    if pending:
        raise ValueError("LEAN_EMPTY_IMPORT")
    return modules


def research_rows(snapshot: Snapshot) -> list[dict[str, str]]:
    text = snapshot.text("research/README.md")
    rows = [{"name": m.group(1), "registration": m.group(2), "maintenance_status": m.group(3).strip()}
            for m in re.finditer(r"(?m)^\| `([^`]+)` \| (workflow \(gate 11\)|local receipt only) \|([^|]*)\|$", text)]
    if not rows or len({r["name"] for r in rows}) != len(rows):
        raise ValueError("TREE_INDEX_EMPTY_OR_DUPLICATE")
    # The independent directory population follows the index's documented carve.
    excluded = {"notes", "e2e_tests"}
    actual = {p.split("/")[1] for p in snapshot.files if p.startswith("research/") and len(p.split("/")) > 2
              and not p.split("/")[1].startswith(("_", ".")) and p.split("/")[1] not in excluded}
    if actual != {r["name"] for r in rows}:
        raise ValueError(f"TREE_POPULATION_MISMATCH: {sorted(actual ^ {r['name'] for r in rows})}")
    return rows


def import_census(snapshot: Snapshot) -> dict[str, Any]:
    paths = sorted(p for p in snapshot.files if p.startswith("research/") and p.endswith(".lean"))
    snapshot.preload(paths)
    files: list[dict[str, Any]] = []
    for path in paths:
        text = snapshot.text(path)
        imports = lean_imports(text)
        direct = [name for name in imports if name == "Derivation" or name.startswith("Derivation.")]
        files.append({"source": snapshot.reference(path), "configuration": path.endswith("/lakefile.lean"),
                      "imports": imports, "direct_native_imports": direct,
                      "raw_mention": bool(re.search(r"import.*Derivation", text)),
                      "compiler_dependencies": None, "compiled_reach": None,
                      "gap": "Compiler dependency and compiled-environment evidence are collected separately."})
    direct_files = [r["source"]["path"] for r in files if r["direct_native_imports"]]
    return {"snapshot": snapshot.snapshot, "files": files, "tracked_lean_files": len(paths),
            "direct_files": direct_files, "direct_trees": sorted({p.split("/")[1] for p in direct_files}),
            "comment_only_mentions": [r["source"]["path"] for r in files if r["raw_mention"] and not r["direct_native_imports"]]}
