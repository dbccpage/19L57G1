"""Verify freeze order, exact source blobs, vendored values, and isolation."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FREEZE = "2f576e5803ae15f0475d20eabf4573fc79450935"
FROZEN = {
    "REQUIREMENTS.md": "4588457ed5ad0ac41868f214cc2041512f049c76d52f33200656c92783d2853a",
    "PREDICTIONS.md": "a3a8e79d32795a932d930b54f2eba984c3a04fbce68bfd758a0e51532c22dc23",
}
VENDORED_SHA256 = "e5c21ace212fb8d1f9ba759163337d0ca9e0ec4e14fc7d3b5a221fce83cf389c"
VENDORED_BYTES = 12726
STAGES = tuple([f"challenge{index}" for index in range(6)] + ["continuation1", "continuation2"])
ALLOWED_IMPORTS = {
    "__future__",
    "collections",
    "dataclasses",
    "enum",
    "fractions",
    "functools",
    "hashlib",
    "itertools",
    "json",
    "pathlib",
    "typing",
    "typed_translation",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(spec: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", spec], cwd=ROOT, capture_output=True, check=False
    )
    return proc.stdout if proc.returncode == 0 else None


def git_text(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    return proc.returncode, proc.stdout.strip()


def check_freeze() -> list[str]:
    problems: list[str] = []
    code, paths = git_text(
        "diff-tree", "--no-commit-id", "--name-only", "-r", f"{FREEZE}^", FREEZE
    )
    expected_paths = sorted(
        f"research/typed_translation/{name}" for name in FROZEN
    )
    if code != 0 or sorted(paths.splitlines()) != expected_paths:
        problems.append(
            f"freeze commit paths are {paths.splitlines()!r}, wanted {expected_paths!r}"
        )
    for name, wanted in FROZEN.items():
        path = HERE / name
        if not path.is_file():
            problems.append(f"frozen {name} is missing")
            continue
        current = path.read_bytes()
        frozen = git_bytes(f"{FREEZE}:research/typed_translation/{name}")
        if sha256(current) != wanted:
            problems.append(f"frozen {name} working bytes moved")
        if frozen is None or sha256(frozen) != wanted:
            problems.append(f"frozen {name} does not match its freeze-commit blob")
        code, later = git_text(
            "log", "--format=%H", f"{FREEZE}..HEAD", "--", f"research/typed_translation/{name}"
        )
        if code != 0 or later:
            problems.append(f"frozen {name} was edited after the freeze commit: {later}")
    return problems


def load_manifest() -> tuple[dict[str, Any] | None, list[str]]:
    path = HERE / "SOURCE_MANIFEST.json"
    try:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"cannot read SOURCE_MANIFEST.json: {exc}"]
    if not isinstance(raw, dict):
        return None, ["SOURCE_MANIFEST.json is not an object"]
    return raw, []


def check_manifest() -> tuple[list[str], int, str | None]:
    manifest, problems = load_manifest()
    if manifest is None:
        return problems, 0, None
    commit = manifest.get("pinned_commit")
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        return [*problems, f"pinned_commit is not exact lowercase hex: {commit!r}"], 0, None
    code, _ = git_text("cat-file", "-e", f"{commit}^{{commit}}")
    if code != 0:
        problems.append(f"pinned commit {commit} is unavailable")
    code, _ = git_text("merge-base", "--is-ancestor", commit, "HEAD")
    if code != 0:
        problems.append(f"pinned commit {commit} is not an ancestor of HEAD")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        return [*problems, "manifest has no source census"], 0, commit
    seen: set[str] = set()
    for item in sources:
        if not isinstance(item, dict):
            problems.append("manifest source is not an object")
            continue
        path = item.get("path")
        wanted = item.get("sha256")
        if not isinstance(path, str) or not isinstance(wanted, str):
            problems.append(f"malformed source row {item!r}")
            continue
        if path in seen:
            problems.append(f"duplicate source path {path}")
        seen.add(path)
        data = git_bytes(f"{commit}:{path}")
        if data is None:
            problems.append(f"{path} is absent at pinned commit {commit}")
        elif sha256(data) != wanted:
            problems.append(f"{path} blob digest differs at pinned commit")
    return problems, len(sources), commit


def source_dependence_rows(commit: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for stage in STAGES:
        path = f"research/boundary_seed/receipts/{stage}.json"
        data = git_bytes(f"{commit}:{path}")
        if data is None:
            raise ValueError(f"missing pinned source receipt {path}")
        payload: object = json.loads(data)
        if not isinstance(payload, dict):
            raise ValueError(f"pinned source receipt {path} is not an object")
        value = payload.get("boundary_dependence")
        if isinstance(value, dict):
            for subject, claim in value.items():
                rows.append((stage, str(subject), str(claim)))
        elif stage == "continuation2" and isinstance(value, str):
            rows.append(
                (
                    stage,
                    "inscriptions, placement, renaming, attempt accounting, replay, and resources",
                    value,
                )
            )
        else:
            raise ValueError(f"{path} has no recognized boundary_dependence value")
    return rows


def check_vendored(commit: str | None) -> tuple[list[str], int]:
    problems: list[str] = []
    path = HERE / "pinned" / "boundary_dependence.json"
    if not path.is_file():
        return ["vendored dependence file is missing"], 0
    data = path.read_bytes()
    if len(data) != VENDORED_BYTES or sha256(data) != VENDORED_SHA256:
        problems.append("vendored dependence bytes differ from the build pin")
    try:
        raw: object = json.loads(data)
    except json.JSONDecodeError as exc:
        return [*problems, f"vendored dependence JSON is invalid: {exc}"], 0
    if not isinstance(raw, dict) or not isinstance(raw.get("rows"), list):
        return [*problems, "vendored dependence JSON has no rows list"], 0
    if raw.get("snapshot") != commit:
        problems.append("vendored dependence snapshot differs from source manifest")
    actual: list[tuple[str, str, str]] = []
    for row in raw["rows"]:
        if not isinstance(row, dict):
            problems.append("vendored row is not an object")
            continue
        actual.append((str(row.get("stage")), str(row.get("subject")), str(row.get("claim"))))
    if commit is not None:
        try:
            expected = source_dependence_rows(commit)
        except (ValueError, json.JSONDecodeError) as exc:
            problems.append(str(exc))
        else:
            if actual != expected:
                problems.append("vendored dependence population differs from pinned receipts")
    if len(actual) != 37:
        problems.append(f"vendored dependence population is {len(actual)}, wanted 37")
    return problems, len(actual)


def check_isolation() -> tuple[list[str], int]:
    problems: list[str] = []
    files = sorted((HERE / "code" / "typed_translation").rglob("*.py"))
    if not files:
        return ["kernel source census is empty"], 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        if "sys.path" in text:
            problems.append(f"{path.relative_to(HERE)} mutates sys.path")
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            problems.append(f"{path.relative_to(HERE)} does not parse: {exc}")
            continue
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names.append(node.module)
            for name in names:
                root = name.split(".", 1)[0]
                if root not in ALLOWED_IMPORTS:
                    problems.append(
                        f"{path.relative_to(HERE)} imports undeclared external root {root}"
                    )
    return problems, len(files)


def check_attributes() -> list[str]:
    problems: list[str] = []
    names = [
        "REQUIREMENTS.md",
        "PREDICTIONS.md",
        "SOURCE_MANIFEST.json",
        "pinned/boundary_dependence.json",
        "receipts/typed_translation.json",
        "lean/axioms.txt",
    ]
    for name in names:
        path = HERE / name
        if not path.is_file():
            problems.append(f"byte-stable file {name} is missing")
            continue
        if b"\r" in path.read_bytes():
            problems.append(f"byte-stable file {name} contains CR bytes")
        code, output = git_text("check-attr", "text", "--", f"research/typed_translation/{name}")
        if code != 0 or not output.endswith(": text: unset"):
            problems.append(f"{name} is not protected by -text: {output}")
    return problems


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        print(f"FAIL: unknown arguments: {' '.join(argv)}")
        return 1
    problems = check_freeze()
    manifest_problems, source_count, commit = check_manifest()
    problems.extend(manifest_problems)
    vendored_problems, row_count = check_vendored(commit)
    problems.extend(vendored_problems)
    isolation_problems, module_count = check_isolation()
    problems.extend(isolation_problems)
    problems.extend(check_attributes())
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        return 1
    print(
        f"pins ok: {len(FROZEN)} frozen files at {FREEZE[:12]}, "
        f"{source_count} exact source blobs at {commit}, {row_count} vendored rows, "
        f"{module_count} isolated kernel modules"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
