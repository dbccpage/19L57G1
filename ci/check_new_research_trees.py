"""Enforce the copy-source contract for new research trees only.

Existing directories are frozen in the grandfathered list; their bytes are
not rewritten or held to the new naming convention. A rung of the second
derivation, a `second_<rung>` tree whose SOURCE_MANIFEST.json records the
pinned sha256 of research/second/SEED.md, is held to that seed's rung
contract instead: the seed is read-only, predates this contract, and fixes
CLAIM_LEDGER.md as the rung's claim document. AuthorityEffect: None.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

REPO = Path(__file__).resolve().parents[1]
SCAFFOLD = "research/_scaffold"
STATUSES = {"PROVED_THEOREM", "VERIFIED_FINITE", "CONDITIONAL", "OPEN", "REFUTED"}
CLAIM_NAMES = {"CLAIMS.md", "CLAIM_LEDGER.md", "claim_ledger.md", "claims.md", "RECONCILED_CLAIMS_LEDGER.md"}
SEED = "research/second/SEED.md"
SEED_SHA256 = "52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e"
# The seed's section 4 files; SOURCE_MANIFEST.json selects this contract, and
# CLAIM_LEDGER.md is checked as the one claim document.
RUNG_FILES = ("PROMPT.md", "PREDICTIONS.md", "STATUS.md", "verify_pins.py")


def tree_names(paths: list[str]) -> list[str]:
    return sorted({p.split("/")[1] for p in paths if p.startswith("research/")
                   and len(p.split("/")) > 2 and not p.split("/")[1].startswith(("_", "."))})


def own_files(tree: Path) -> list[Path]:
    files: list[Path] = []
    for folder, directories, names in os.walk(tree):
        directories[:] = sorted(d for d in directories if not d.startswith(".") and d != "__pycache__")
        files.extend(Path(folder)/name for name in names if not name.startswith("."))
    return sorted(files)


def tree_problems(tree: Path, canonical: bytes, roots: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    label = "research/"+tree.name
    def fail(relative: str, reason: str) -> None:
        errors.append(f"{label}/{relative}: {reason}")
    names = {p.name for p in tree.iterdir() if p.is_file()}
    if names & CLAIM_NAMES != {"CLAIMS.md"}:
        fail("CLAIMS.md", "require exactly this claim-document filename")
    else:
        rows = [line for line in (tree/"CLAIMS.md").read_text(encoding="utf-8").splitlines() if line.startswith("|")]
        if len(rows) < 3 or rows[0] != "| Claim | Status | Statement | Evidence |":
            fail("CLAIMS.md", "require the four-column claims table and at least one claim")
        for row in rows[2:]:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) != 4 or not all(cells) or cells[1] not in STATUSES:
                fail("CLAIMS.md", f"invalid claim row or status: {row}")
    verifier = tree/"verify.py"
    if not verifier.is_file() or verifier.read_bytes().replace(b"\r\n", b"\n") != canonical.replace(b"\r\n", b"\n"):
        fail("verify.py", "must copy the canonical --check entry point verbatim")
    try:
        config = json.loads((tree/"TREE_CONTRACT.json").read_text(encoding="utf-8"))
        if not isinstance(config, dict) or config.get("schema") != 1:
            raise ValueError("expected schema 1")
        root = config.get("lean_root")
        if not isinstance(root, str) or not re.fullmatch(r"Research[A-Z][A-Za-z0-9]*", root):
            raise ValueError("lean_root must be a tree-unique Research-prefixed module")
        others = roots.get(root, set()) - {tree.name}
        if others:
            raise ValueError(f"Lean root {root} is also supplied by {sorted(others)}")
        pins = config.get("pin_files")
        if (not isinstance(pins, list) or not pins or any(not isinstance(p, str) for p in pins)
                or len(set(pins)) != len(pins)):
            raise ValueError("pin_files must be a nonempty unique list")
        for name in pins:
            path = tree/name
            if Path(name).is_absolute() or ".." in Path(name).parts or not path.is_file() or not path.resolve().is_relative_to(tree.resolve()):
                raise ValueError(f"pin_files names a missing or nonlocal input: {name}")
        declarations = config.get("axiom_declarations")
        if (config.get("axiom_scope") != "explicit_reports" or not isinstance(declarations, list)
                or not declarations or any(not isinstance(n, str) or not n.startswith(root+".") for n in declarations)
                or len(set(declarations)) != len(declarations)):
            raise ValueError("declare a nonempty exact axiom-report scope")
        files = own_files(tree)
        packages = [p.relative_to(tree).as_posix() for p in files if p.name in ("lakefile.toml", "lakefile.lean")]
        if packages != ["lean/lakefile.toml"]:
            fail("lean/lakefile.toml", f"require one package under lean/; found {packages}")
        else:
            lake = tomllib.loads((tree/"lean/lakefile.toml").read_text(encoding="utf-8"))
            if lake.get("defaultTargets") != [root] or lake.get("lean_lib") != [{"name": root}]:
                fail("lean/lakefile.toml", "library and default target must equal lean_root")
        report = tree/"lean"/root/"AxiomReport.lean"
        report_text = report.read_text(encoding="utf-8")
        printed = re.findall(r"(?m)^#print axioms ([A-Za-z0-9_'.]+)\s*$", report_text)
        if printed != declarations:
            fail(f"lean/{root}/AxiomReport.lean", "printed declarations differ from the exact configured scope")
        for path in files:
            if path.suffix != ".lean":
                continue
            relative = path.relative_to(tree).as_posix()
            if not (relative == f"lean/{root}.lean" or relative.startswith(f"lean/{root}/")):
                fail(relative, "Lean modules must live under the unique tree root")
            text = path.read_text(encoding="utf-8")
            if re.search(r"(?m)^\s*import\s+(?:[^\n]*[. ])?(?:Inventory|AxiomReport)(?:\s|$)", text):
                fail(relative, "compile the census by file path; do not import a census module")
    except (OSError, ValueError, TypeError) as error:
        fail("TREE_CONTRACT.json", str(error))
    return errors


def seed_rung(tree: Path) -> bool:
    manifest = tree/"SOURCE_MANIFEST.json"
    return tree.name.startswith("second_") and manifest.is_file() and SEED_SHA256 in manifest.read_text(encoding="utf-8")


def rung_problems(tree: Path, roots: dict[str, set[str]], seed_intact: bool) -> list[str]:
    errors: list[str] = []
    label = "research/"+tree.name
    def fail(relative: str, reason: str) -> None:
        errors.append(f"{label}/{relative}: {reason}")
    if not seed_intact:
        errors.append(f"{SEED}: sha256 differs from the pinned seed, so no tree may claim its rung contract")
    names = {p.name for p in tree.iterdir() if p.is_file()}
    for name in RUNG_FILES:
        if name not in names:
            fail(name, f"a second-derivation rung requires this file ({SEED}, section 4)")
    if names & CLAIM_NAMES != {"CLAIM_LEDGER.md"}:
        fail("CLAIM_LEDGER.md", f"require exactly this claim-document filename ({SEED}, section 4)")
    files = own_files(tree)
    packages = [p.relative_to(tree).as_posix() for p in files if p.name in ("lakefile.toml", "lakefile.lean")]
    modules = [p.relative_to(tree).as_posix() for p in files if p.suffix == ".lean" and p.name != "lakefile.lean"]
    if (packages or modules) and packages not in (["lean/lakefile.lean"], ["lean/lakefile.toml"]):
        fail("lean", f"require one package directly under lean/; found {packages}")
    for relative in modules:
        if not relative.startswith("lean/"):
            fail(relative, "Lean modules must live under lean/")
    for root in sorted({m.split("/")[1].removesuffix(".lean") for m in modules if m.startswith("lean/")}):
        others = roots.get(root, set()) - {tree.name}
        if others:
            fail("lean", f"Lean root {root} is also supplied by {sorted(others)}")
    return errors


def problems(repo: Path) -> list[str]:
    record = json.loads((repo/SCAFFOLD/"grandfathered.json").read_text(encoding="utf-8"))
    baseline = record.get("baseline", "")
    if record.get("schema") != 1 or not isinstance(baseline, str) or not re.fullmatch(r"[0-9a-f]{40}", baseline):
        return [SCAFFOLD+"/grandfathered.json: invalid fixed baseline"]
    paths = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", baseline, "--", "research"], text=True, encoding="utf-8").splitlines()
    expected = tree_names(paths)
    if record.get("trees") != expected:
        return [SCAFFOLD+"/grandfathered.json: tree list differs from its fixed baseline"]
    trees = sorted(p for p in (repo/"research").iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))
    roots: dict[str, set[str]] = {}
    for tree in trees:
        for path in own_files(tree):
            relative = path.relative_to(tree).parts
            if path.suffix == ".lean" and "lean" in relative:
                after = relative[relative.index("lean")+1:]
                if after:
                    roots.setdefault(after[0].removesuffix(".lean"), set()).add(tree.name)
    canonical = (repo/SCAFFOLD/"new_tree_templates/verify.py.tmpl").read_bytes()
    seed = repo/SEED
    seed_intact = seed.is_file() and hashlib.sha256(seed.read_bytes()).hexdigest() == SEED_SHA256
    failures: list[str] = []
    for tree in trees:
        if tree.name in expected:
            continue
        if seed_rung(tree):
            failures.extend(rung_problems(tree, roots, seed_intact))
            continue
        errors = tree_problems(tree, canonical, roots)
        if errors and tree.name.startswith("second_"):
            errors.insert(0, f"research/{tree.name}/SOURCE_MANIFEST.json: records no pinned seed hash, so the new-tree contract applies")
        failures.extend(errors)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    args = parser.parse_args()
    try:
        failures = problems(args.repo.resolve())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        failures = [str(error)]
    for failure in failures:
        print("FAIL: "+failure, file=sys.stderr)
    if not failures:
        print("new research-tree contract clean; existing baseline directories grandfathered; second-derivation rungs held to their seed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
