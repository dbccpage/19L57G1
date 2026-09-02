from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess


BASE_COMMIT = "be7476868e496e06d5dec6599fa4346394c512bd"
BASE_TREE = "0821fc9bc55fa551e0dd4752542221e109d3e36c"
PUBLICATION_BASE_COMMIT = "470eec30505ede6ed4b1ec16c689e00d91cc735d"
PUBLICATION_BASE_TREE = "34d77a4c9be4f7670fe03484f61de3bfb5c76da0"
FROZEN_TAG = "sealed-derivation-v1"
FROZEN_TAG_OBJECT = "e147f01cfed1d17410c55a1e78367fdadc63a5ae"
FROZEN_COMMIT = "3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a"
FROZEN_TREE = "d015d9085217267f5cf895935aad13236f1bb6b5"
WRITE_ROOT = "research/admission_sign_shadow/"
MANIFEST = WRITE_ROOT + "SOURCE_MANIFEST.json"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
SOURCES: tuple[tuple[str, str], ...] = (
    ("frozen", "code/derivation/model.py"),
    ("frozen", "lean4/Derivation/Basic.lean"),
    ("frozen", "lean4/Derivation/Bridge.lean"),
    ("frozen", "lean4/Derivation/Erasure.lean"),
    ("frozen", "lean4/Derivation/PresentationNaturality.lean"),
    ("frozen", "lean4/Derivation/PrimDiff.lean"),
    ("frozen", "lean4/Derivation/WeightProfile.lean"),
    ("frozen", "lean4/lean-toolchain"),
    ("base", "CLAUDE.md"),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def git_bytes(repo: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True
    )
    return completed.stdout


def git_text(repo: Path, *args: str) -> str:
    return git_bytes(repo, *args).decode("utf-8").strip()


def revision(name: str) -> str:
    if name == "frozen":
        return FROZEN_COMMIT
    if name == "base":
        return BASE_COMMIT
    raise ValueError(f"unknown revision name: {name}")


def source_entry(repo: Path, revision_name: str, path: str) -> dict[str, object]:
    rev = revision(revision_name)
    blob = git_text(repo, "rev-parse", f"{rev}:{path}")
    content = git_bytes(repo, "cat-file", "blob", blob)
    return {
        "git_blob": blob,
        "path": path,
        "revision": revision_name,
        "sha256": sha256(content).hexdigest(),
    }


def build_manifest(repo: Path) -> dict[str, object]:
    exact_values = (
        BASE_COMMIT,
        BASE_TREE,
        PUBLICATION_BASE_COMMIT,
        PUBLICATION_BASE_TREE,
        FROZEN_TAG_OBJECT,
        FROZEN_COMMIT,
        FROZEN_TREE,
    )
    if not all(HEX40.fullmatch(value) for value in exact_values):
        raise ValueError("one or more source identifiers are not exact hashes")
    observed = {
        "base_commit": git_text(repo, "rev-parse", BASE_COMMIT),
        "base_tree": git_text(repo, "rev-parse", f"{BASE_COMMIT}^{{tree}}"),
        "publication_base_commit": git_text(repo, "rev-parse", PUBLICATION_BASE_COMMIT),
        "publication_base_tree": git_text(
            repo, "rev-parse", f"{PUBLICATION_BASE_COMMIT}^{{tree}}"
        ),
        "frozen_tag_object": git_text(repo, "rev-parse", FROZEN_TAG),
        "frozen_commit": git_text(repo, "rev-parse", f"{FROZEN_TAG}^{{}}"),
        "frozen_tree": git_text(repo, "rev-parse", f"{FROZEN_TAG}^{{tree}}"),
    }
    expected = {
        "base_commit": BASE_COMMIT,
        "base_tree": BASE_TREE,
        "publication_base_commit": PUBLICATION_BASE_COMMIT,
        "publication_base_tree": PUBLICATION_BASE_TREE,
        "frozen_tag_object": FROZEN_TAG_OBJECT,
        "frozen_commit": FROZEN_COMMIT,
        "frozen_tree": FROZEN_TREE,
    }
    if observed != expected:
        raise ValueError(f"source identities differ: observed={observed}")
    entries = [source_entry(repo, rev, path) for rev, path in SOURCES]
    toolchains = {
        entry["path"]: git_bytes(
            repo,
            "cat-file",
            "blob",
            str(entry["git_blob"]),
        )
        .decode("utf-8")
        .strip()
        for entry in entries
        if str(entry["path"]).endswith("lean-toolchain")
    }
    return {
        "authority_effect": None,
        **expected,
        "sources": entries,
        "toolchains": toolchains,
        "write_root": WRITE_ROOT,
    }


def changed_paths(repo: Path) -> tuple[str, ...]:
    changed = set(
        line
        for line in git_text(
            repo, "diff", "--name-only", PUBLICATION_BASE_COMMIT, "--"
        ).splitlines()
        if line
    )
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    for line in status.splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        changed.add(path.replace("\\", "/"))
    return tuple(sorted(changed))


def render_manifest(repo: Path) -> bytes:
    return (
        json.dumps(build_manifest(repo), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def verify(repo: Path, *, enforce_scope: bool) -> None:
    head = git_text(repo, "rev-parse", "HEAD")
    for label, revision_id in (
        ("source base", BASE_COMMIT),
        ("publication base", PUBLICATION_BASE_COMMIT),
    ):
        if subprocess.run(
            ["git", "merge-base", "--is-ancestor", revision_id, head], cwd=repo
        ).returncode != 0:
            raise ValueError(f"{label} is not an ancestor of HEAD")
    if enforce_scope:
        invalid = [
            path for path in changed_paths(repo) if not path.startswith(WRITE_ROOT)
        ]
        if invalid:
            raise ValueError(f"paths outside write root changed: {invalid}")
    for revision_name, path in SOURCES:
        if revision_name == "base":
            base_blob = git_text(repo, "rev-parse", f"{BASE_COMMIT}:{path}")
            head_blob = git_text(repo, "rev-parse", f"HEAD:{path}")
            if base_blob != head_blob:
                raise ValueError(f"base source changed at HEAD: {path}")
    expected = render_manifest(repo)
    manifest_path = repo / MANIFEST
    if not manifest_path.exists() or manifest_path.read_bytes() != expected:
        raise ValueError("SOURCE_MANIFEST.json differs from exact source objects")
    print(
        f"source pins clean: base={BASE_COMMIT} "
        f"publication_base={PUBLICATION_BASE_COMMIT} frozen={FROZEN_COMMIT} "
        f"sources={len(SOURCES)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-scope", action="store_true")
    args = parser.parse_args()
    repo = repo_root()
    if args.write:
        (repo / MANIFEST).write_bytes(render_manifest(repo))
    verify(repo, enforce_scope=args.write or args.check_scope)


if __name__ == "__main__":
    main()
