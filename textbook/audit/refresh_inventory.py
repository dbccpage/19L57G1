"""Reconcile source declaration candidates with compiled Lean locations.

AuthorityEffect: None. This is textbook apparatus, not a sealed census or
evidence of teaching completeness. Builds lean4/ before reading its environment.
The generated Lean file lives outside the repository; outputs go to the
explicit --out directory. Historical inventory.py/json are never rewritten.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from ci import check_declaration_axioms as compiled  # noqa: E402
from ci.check_ledger_evidence import count_decls, strip_lean_comments  # noqa: E402

ANONYMOUS_INSTANCE = re.compile(r"^\s*instance\s*(?=[({\[:])")
RAW_DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:private |protected |noncomputable |nonrec )*"
    r"(theorem|lemma|def|abbrev|structure|inductive|instance|class|axiom|opaque)"
    r"\s+([^\s:({\[]+)", re.M,
)


def source_candidates(path: Path, text: str) -> list[dict]:
    """Reuse the ledger's comment-aware scanner; add unnamed instances.

    This is a restricted source scanner, not a replacement Lean parser.
    Constructors, fields, generated constants and deriving commands are not
    separate source heads here. Compiled enumeration retains those constants.
    """
    rows = [dict(path=path.as_posix(), line=d.line, kind=d.head,
                 source_name=d.name)
            for d in count_decls(path, text) if d.head != "constructor"]
    for number, line in enumerate(strip_lean_comments(text), 1):
        if ANONYMOUS_INSTANCE.match(line):
            rows.append(dict(path=path.as_posix(), line=number,
                             kind="instance", source_name=None))
    return sorted(rows, key=lambda r: r["line"])


def bind_candidate(row: dict, constants: list[dict]) -> dict:
    """Require a unique same-module compiled name at the source location."""
    hits = [c for c in constants if c["location"]
            and c["location"]["line"] == row["line"]
            and (c["instance"] if row["source_name"] is None else
                 c["name"].endswith("." + row["source_name"]))]
    if len(hits) != 1:
        raise ValueError(f"{row}: expected one compiled location, found {len(hits)}")
    c = hits[0]
    expected = ("theorem" if row["kind"] in {"theorem", "lemma"} else
                "inductive" if row["kind"] in {"structure", "inductive", "class"}
                else "definition")
    if c["kind"] != expected:
        raise ValueError(f"{row}: compiled kind {c['kind']} != {expected}")
    return dict(row, name=c["name"], axioms=c["axioms"])


def render_census(modules: list[str]) -> str:
    """Add source locations to the existing full compiled-environment audit."""
    src = compiled.render_census(modules)
    changes = {
        "import Lean.Data.Json": "import Lean.Data.Json\nimport Lean.DeclarationRange",
        "let axioms <- liftCoreM (Lean.collectAxioms name)": """let axioms <- liftCoreM (Lean.collectAxioms name)
          let ranges ← findDeclarationRanges? name
          let location := match ranges with
            | none => Json.null
            | some r => Json.mkObj [
                ("start", toJson r.range.pos.line),
                ("end", toJson r.range.endPos.line),
                ("line", toJson r.selectionRange.pos.line),
                ("column", toJson r.selectionRange.pos.column),
                ("endColumn", toJson r.selectionRange.endPos.column)]""",
        '("internal", toJson name.isInternalDetail),':
        '("internal", toJson name.isInternalDetail),\n            ("location", location),',
    }
    for old, new in changes.items():
        if src.count(old) != 1:
            raise ValueError("compiled census template changed; review location extension")
        src = src.replace(old, new)
    return src


def fingerprint(paths: list[Path]) -> dict[str, str]:
    return {p.relative_to(REPO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def reconcile(files: list[Path], records: list[dict]) -> dict:
    by_module: dict[str, list[dict]] = defaultdict(list)
    for c in records:
        by_module[c["module"]].append(c)
    rows = []
    removed = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        relative = f.relative_to(REPO)
        candidates = source_candidates(relative, text)
        module = "Derivation" if f.name == "Derivation.lean" else "Derivation." + f.stem
        for row in candidates:
            rows.append(bind_candidate(row, by_module[module]))
        keys = {(r["line"], r["kind"], r["source_name"]) for r in candidates}
        clean = strip_lean_comments(text)
        for match in RAW_DECL.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            if (line, match[1], match[2]) not in keys:
                if clean[line - 1].strip():
                    raise ValueError(f"unresolved non-comment historical match: {relative}:{line}")
                removed.append(dict(path=relative.as_posix(), line=line,
                                    kind=match[1], false_name=match[2]))
    sealed = [c for c in records if c["module"] == "Derivation"
              or c["module"].startswith("Derivation.")]
    return dict(
        source_head_counts=dict(sorted(Counter(r["kind"] for r in rows).items())),
        source_heads=len(rows),
        compiled_constants=len(sealed),
        compiled_kind_counts=dict(sorted(Counter(c["kind"] for c in sealed).items())),
        removed_comment_matches=removed,
        declarations=rows,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True, check=True).stdout.strip()
    files = [REPO / "lean4/Derivation.lean", *sorted((REPO / "lean4/Derivation").glob("*.lean"))]
    before = fingerprint(files)
    pin = REPO / "artifacts/elaborated_modules.txt"
    modules = compiled.parse_pin(pin.read_text(encoding="utf-8"))
    actual = {"Derivation." + p.stem for p in files[1:]}
    if set(modules) != actual:
        raise ValueError("compiled module pin differs from current source-file population")
    args.out.mkdir(parents=True, exist_ok=True)
    build = subprocess.run(["lake", "build"], cwd=REPO / "lean4",
                           capture_output=True, text=True, encoding="utf-8")
    (args.out / "build.log").write_text(build.stdout + build.stderr, encoding="utf-8")
    if build.returncode:
        raise ValueError("lake build failed; inspect build.log")
    src = render_census(modules)
    code, output = compiled.run_lean(REPO / "lean4", src, compiled.DEFAULT_TIMEOUT)
    (args.out / "compiled.log").write_text(output, encoding="utf-8")
    if code:
        raise ValueError(f"Lean census failed with exit {code}; inspect compiled.log")
    verdict = compiled.evaluate(compiled.parse_output(output), modules)
    if verdict.failures:
        raise ValueError("; ".join(verdict.failures))
    records = [json.loads(line[len("DECLAX_CONST "):])
               for line in output.splitlines() if line.startswith("DECLAX_CONST ")]
    report = reconcile(files, records)
    if before != fingerprint(files):
        raise ValueError("source bytes changed during reconciliation")
    end_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                              capture_output=True, text=True, check=True).stdout.strip()
    if head != end_head:
        raise ValueError("repository head changed during reconciliation")
    report.update(source_commit=head, source_hashes=before,
                  census_sha256=hashlib.sha256(src.encode()).hexdigest(),
                  compiled_log_sha256=hashlib.sha256(output.encode()).hexdigest(),
                  compiled_verdict=verdict.summary,
                  scope="source-head reconciliation, not semantic coverage or a source parser")
    (args.out / "reconciled.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(verdict.summary)
    print(f"source heads: {report['source_heads']}; {report['source_head_counts']}")
    print(f"historical comment matches removed: {len(report['removed_comment_matches'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
