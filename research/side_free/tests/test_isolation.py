"""Source isolation, with exactly one carve.

No file of this tree may cite a sealed path, a sealed claim identifier, a
sealed Lean name, an import of the sealed kernel, or the name of another
research tree.  The single carve is that the pinned tree's own directory name
may appear in three declared files and nowhere else; every other tree name
stays barred everywhere, those three included.

Sibling names are accumulated from history as well as from the current tree,
so a name that appeared between commits cannot evade the scan.  Undecodable
or symlinked files fail closed, because an all-file scan cannot certify bytes
it did not inspect.

This file is itself scanned, so every barred example below is assembled from
pieces.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
ROOT = TREE.parent.parent
REL = "research/side_free"
OWN = "side_free"

# The one carve.  The pinned tree must be named somewhere -- a control that
# cannot name what it controls for is not reviewable -- and these are the
# three declared places.  Nothing else is exempt from anything.
CARVED_PATHS: tuple[str, ...] = (
    f"{REL}/SOURCE_MANIFEST.json",
    f"{REL}/pinned/BOUNDARY_PIN.json",
    f"{REL}/pinned/QUOTATIONS.md",
)
CARVED_TREE = "boundary" + "_" + "seed"

SEALED_PATTERNS: tuple[tuple[str, str], ...] = (
    ("citation into the sealed paper", r"\bpaper[\\/][^\s`'\"<>]+?\.md\b"),
    (
        "citation into the sealed artifacts",
        r"\bartifacts[\\/][A-Za-z0-9_.-][^\s`'\"<>]*",
    ),
    (
        "citation into the sealed Lean",
        r"\blean4[\\/]Derivation[\\/][A-Za-z0-9_.-][^\s`'\"<>]*",
    ),
    (
        "citation into the sealed kernel",
        r"\bcode[\\/]derivation[\\/][A-Za-z0-9_.-][^\s`'\"<>]*",
    ),
    ("sealed claim identifier", r"\bCL-[A-Za-z0-9]"),
    ("sealed Lean name", r"\bDerivation\.[A-Za-z_]"),
    ("import of the sealed kernel", r"^\s*(?:from|import)\s+derivation\b"),
)


def git_bytes(args: list[str]) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout


def nul_paths(data: bytes) -> list[str]:
    return sorted(
        item.decode("utf-8", errors="surrogateescape")
        for item in data.split(b"\0")
        if item
    )


def current_tree_names() -> set[str]:
    paths = nul_paths(
        git_bytes(["ls-tree", "-d", "-z", "--name-only", "HEAD", "--", "research/"])
    )
    return {path.replace("\\", "/").split("/")[-1] for path in paths if path}


def historical_tree_names() -> set[str]:
    paths = nul_paths(
        git_bytes(["log", "--format=", "--name-only", "-z", "HEAD", "--", "research/"])
    )
    names: set[str] = set()
    for repo_path in paths:
        parts = repo_path.replace("\\", "/").split("/")
        if len(parts) >= 2 and parts[0] == "research":
            names.add(parts[1])
    return names


def other_tree_names() -> list[str]:
    names = current_tree_names() | historical_tree_names()
    return sorted(name for name in names if name and name != OWN)


def tree_patterns(names: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for name in names:
        out.append(
            (f"other research tree {name}", rf"\bresearch[\\/]{re.escape(name)}\b")
        )
        if "_" in name:
            out.append((f"other research tree {name}", rf"\b{re.escape(name)}\b"))
    return out


def patterns_for(repo_path: str, names: list[str]) -> list[tuple[str, str]]:
    """The scan's patterns for one file, with the carve applied to that file."""
    barred = [name for name in names if not (repo_path in CARVED_PATHS and name == CARVED_TREE)]
    return list(SEALED_PATTERNS) + tree_patterns(barred)


def scan_text(text: str, patterns: list[tuple[str, str]]) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in patterns:
            if re.search(pattern, line):
                hits.append((lineno, label))
    return hits


def scan_bytes(data: bytes, source: str, patterns: list[tuple[str, str]]) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [f"{source}: non-UTF-8 content cannot be isolation-scanned"]
    return [f"{source}:{lineno}: {label}" for lineno, label in scan_text(text, patterns)]


def tracked_paths() -> list[str]:
    return nul_paths(
        git_bytes(
            ["ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", REL]
        )
    )


class SourceIsolation(unittest.TestCase):
    def test_the_tree_is_source_isolated_under_the_one_carve(self) -> None:
        names = other_tree_names()
        self.assertGreater(len(names), 1)
        problems: list[str] = []
        scanned = 0
        for repo_path in tracked_paths():
            path = ROOT / repo_path
            if not path.exists():
                continue
            if path.is_symlink():
                problems.append(f"{repo_path}: symlink cannot be isolation-scanned")
                continue
            try:
                data = path.read_bytes()
            except OSError as exc:
                problems.append(f"{repo_path}: cannot be isolation-scanned: {exc}")
                continue
            scanned += 1
            problems.extend(scan_bytes(data, repo_path, patterns_for(repo_path, names)))
        self.assertGreater(scanned, 0)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_every_committed_version_of_the_tree_is_isolated(self) -> None:
        shallow = git_bytes(["rev-parse", "--is-shallow-repository"]).decode().strip()
        self.assertEqual(shallow, "false", "a shallow clone cannot certify history")
        names = other_tree_names()
        commits = [
            line
            for line in git_bytes(
                ["rev-list", "--reverse", "HEAD", "--", REL]
            ).decode("ascii").splitlines()
            if line
        ]
        self.assertGreater(len(commits), 0)
        problems: list[str] = []
        for commit in commits:
            for repo_path in nul_paths(
                git_bytes(["ls-tree", "-r", "-z", "--name-only", commit, "--", REL])
            ):
                data = git_bytes(["show", f"{commit}:{repo_path}"])
                problems.extend(
                    scan_bytes(
                        data,
                        f"{commit[:12]}:{repo_path}",
                        patterns_for(repo_path, names),
                    )
                )
        self.assertEqual(problems, [], "\n".join(problems))


class ScanProbes(unittest.TestCase):
    """Each barred example is assembled so this file carries no citation."""

    def hits(self, text: str, repo_path: str = "probe") -> list[str]:
        return [
            label
            for _line, label in scan_text(
                text, patterns_for(repo_path, other_tree_names())
            )
        ]

    def test_probe_sealed_paths(self) -> None:
        self.assertEqual(
            self.hits("see " + "paper/" + "paper.md"), ["citation into the sealed paper"]
        )
        self.assertEqual(
            self.hits("art" + "ifacts/" + "claims.json"),
            ["citation into the sealed artifacts"],
        )
        self.assertEqual(
            self.hits("lean4/Deri" + "vation/" + "Basic.lean"),
            ["citation into the sealed Lean"],
        )
        self.assertEqual(
            self.hits("code/deri" + "vation/" + "model.py"),
            ["citation into the sealed kernel"],
        )

    def test_probe_sealed_names(self) -> None:
        self.assertEqual(self.hits("C" + "L-" + "0-INERTIA"), ["sealed claim identifier"])
        self.assertEqual(self.hits("Deri" + "vation." + "Foo"), ["sealed Lean name"])
        self.assertEqual(
            self.hits("from deri" + "vation import model"),
            ["import of the sealed kernel"],
        )
        self.assertEqual(self.hits("from sidefree import model"), [])

    def test_bare_directory_names_are_not_citations(self) -> None:
        self.assertEqual(
            self.hits("nothing under paper/, artifacts/, or lean4/Derivation/ is read"),
            [],
        )

    def test_the_carve_is_exactly_three_files_wide(self) -> None:
        """Negative in both directions: carved in, barred out."""
        label = f"other research tree {CARVED_TREE}"
        self.assertEqual(self.hits(CARVED_TREE, "probe"), [label])
        for carved in CARVED_PATHS:
            self.assertEqual(self.hits(CARVED_TREE, carved), [])
        self.assertEqual(
            self.hits("research/" + CARVED_TREE, f"{REL}/DESIGN.md"), [label] * 2
        )

    def test_another_tree_stays_barred_inside_the_carved_files(self) -> None:
        others = [n for n in other_tree_names() if "_" in n and n != CARVED_TREE]
        self.assertGreater(len(others), 0)
        other = others[0]
        for carved in CARVED_PATHS:
            self.assertEqual(
                self.hits(other, carved), [f"other research tree {other}"]
            )

    def test_non_utf8_fails_closed(self) -> None:
        self.assertEqual(
            scan_bytes(bytes([0xFF]), "probe", []),
            ["probe: non-UTF-8 content cannot be isolation-scanned"],
        )

    def test_history_names_are_accumulated_as_well_as_current_ones(self) -> None:
        self.assertTrue(historical_tree_names() <= set(other_tree_names()) | {OWN})
        self.assertTrue(current_tree_names() <= set(other_tree_names()) | {OWN})


if __name__ == "__main__":
    unittest.main()
