"""Boundary, vocabulary, temporal, and protected-open refusal gates."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import unittest
from types import ModuleType
from typing import Any, cast

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
SNAPSHOT = "3f44571240a0830a2fa8de639281670f4e50a511"
WRITE_ROOT = "research/second_stake/"
SHARED = (".github/workflows/verify.yml", "research/second/MANUAL.md")
ALLOWED = (WRITE_ROOT, *SHARED)
SEALED = ("prompt/", "paper/", "code/", "lean4/Derivation/", "artifacts/", "ci/")
OUTSIDE_NAME_DIGESTS = frozenset(
    {
        "b5fa4102bb18e5ad59ca341a805088caf71022fde564a480436642923c06aa5c",
        "040baadecf43b35030520a595630621776b2653faf2d5a90f8d5c52accaddad6",
        "a468285f70fd4f3f31e3f6a6b29918072a56b29cc64cd27285dd482aeafa5bf6",
        "666d83a02126d92598412bd2bb96ee181cc7bcc88a1014847b3ddf35fb8a87ea",
        "701fbfd68fbf2b9890d2d2bc8f61ded15153d9cbc5771376737d68ba9c1c9250",
        "874b4eedb60aa5724731fc8fff49c280d5f743565035f30b8e99cf2a81465468",
        "05ec28080374d83e95ef525efedbe41006ec04f7ba3ae61805da054707468eb1",
        "5a118d7e9e6cdfa0dcc8360e400011c6c1a376c61489275117d9bafafda969e1",
        "630471bc17c69d0bb5c0b2a31b8faf762b907eb27fba3204a0f15695d8f804b4",
    }
)


def tree_files() -> list[pathlib.Path]:
    ignored = {"__pycache__", ".mypy_cache"}
    return sorted(
        path
        for path in HERE.rglob("*")
        if path.is_file()
        and path.name not in {".coverage", "coverage.json"}
        and not any(part in ignored for part in path.parts)
    )


def claim_files() -> list[pathlib.Path]:
    return [path for path in tree_files() if path.name != "test_forbidden.py"]


def scanner_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "stake_prose_scan", REPO / "ci" / "check_prose_watchlist.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def changed_paths() -> set[str]:
    diff = subprocess.run(
        ["git", "diff", "--name-only", SNAPSHOT],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    return {path.replace("\\", "/") for path in diff + untracked}


def append_only(base: bytes, current: bytes) -> bool:
    return current.startswith(base)


def outside_declared(paths: set[str]) -> set[str]:
    return {
        path
        for path in paths
        if not (path.startswith(WRITE_ROOT) or path in SHARED)
    }


class VocabularyTests(unittest.TestCase):
    def test_repository_census_scanner_over_direct_write_root(self) -> None:
        scanner = scanner_module()
        data = cast(Any, scanner).load(REPO / cast(Any, scanner).WATCHLIST_REL)
        hits: list[str] = []
        for path in tree_files():
            text = cast(Any, scanner).read_text(path)
            if text is None:
                continue
            for hit in cast(Any, scanner).scan_text(text, data["watched"]):
                hits.append(f"{path.relative_to(HERE)}:{hit.line}: {hit.surface}")
        self.assertEqual(hits, [])

    def test_outside_names_for_orbit_readers_are_absent_by_digest(self) -> None:
        for path in tree_files():
            if path.name == "test_forbidden.py":
                continue
            text = path.read_text("utf-8", errors="replace")
            for word in re.findall(r"[A-Za-z]+", text):
                digest = hashlib.sha256(word.lower().encode("ascii")).hexdigest()
                self.assertNotIn(digest, OUTSIDE_NAME_DIGESTS, f"outside name in {path.name}")

    def test_working_identifier_denylist_is_absent(self) -> None:
        census = json.loads(
            (REPO / "contact" / "analysis" / "contact_countermodels.json").read_text("utf-8")
        )
        working = sorted(
            set(census["denylist"]["full_census"])
            - set(census["denylist"]["subtracted_as_native_or_core"])
        )
        self.assertEqual(len(working), 102)
        for path in tree_files():
            text = path.read_text("utf-8", errors="replace")
            for token in working:
                hit = re.search(
                    r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])",
                    text,
                )
                self.assertIsNone(hit, f"{path.name} contains denied identifier {token}")


class BoundaryTests(unittest.TestCase):
    def test_only_write_root_and_two_shared_appends_are_changed(self) -> None:
        paths = changed_paths()
        self.assertEqual(outside_declared(paths), set())
        for path in paths:
            self.assertFalse(any(path.startswith(prefix) for prefix in SEALED), path)

    def test_boundary_predicate_refuses_a_synthetic_outside_path(self) -> None:
        self.assertEqual(
            outside_declared({"research/second_stake/x", "research/outside_probe"}),
            {"research/outside_probe"},
        )

    def test_append_predicate_refuses_a_changed_prefix(self) -> None:
        self.assertFalse(append_only(b"base\n", b"changed\nbase\n"))
        self.assertTrue(append_only(b"base\n", b"base\nappend\n"))

    def test_shared_files_preserve_snapshot_as_exact_prefix(self) -> None:
        for name in SHARED:
            base = subprocess.run(
                ["git", "show", f"{SNAPSHOT}:{name}"],
                cwd=REPO,
                capture_output=True,
                check=True,
            ).stdout
            disk = (REPO / pathlib.PurePosixPath(name)).read_bytes().replace(b"\r\n", b"\n")
            self.assertTrue(append_only(base, disk), f"shared file is not append-only: {name}")


class ClaimBoundaryTests(unittest.TestCase):
    def test_protected_open_stays_open(self) -> None:
        status = (HERE / "STATUS.md").read_text("utf-8")
        self.assertIn("OB1_UNCHANGED", status)
        barred = (
            "OB-1 is closed",
            "OB-1 is answered",
            "OB-1 is superseded",
            "closes OB-1",
            "answers OB-1",
        )
        for path in claim_files():
            text = path.read_text("utf-8", errors="replace")
            for phrase in barred:
                self.assertNotIn(phrase, text, f"{path.name} changes the protected open")

    def test_no_unscoped_totality_or_input_drop_sentence(self) -> None:
        barred = (
            "every possible rule",
            "all endogenous stakes",
            "the stake is now derived",
            "the declared-input count dropped",
            "ALL_SOLUTIONS_FOUND",
        )
        for path in claim_files():
            text = path.read_text("utf-8", errors="replace")
            for phrase in barred:
                self.assertNotIn(phrase, text, f"{path.name} carries an unlicensed sentence")

    def test_receipts_have_no_temporal_or_environment_fields(self) -> None:
        def walk(value: object) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    lowered = str(key).lower()
                    self.assertNotIn(lowered, {"timestamp", "time", "date", "environment", "host"})
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        for path in (HERE / "receipts").rglob("*.json"):
            walk(json.loads(path.read_text("utf-8")))


if __name__ == "__main__":
    unittest.main()
