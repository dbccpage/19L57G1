"""The blindness scan.  Before FREEZE.md exists, no committed or staged
file of the write root may carry a citation into a sealed path, a sealed
claim identifier, a sealed Lean name, an import of the sealed kernel, or
the name of another research tree.  The seed states the rule and is the
input, not a file this run writes; every other file is scanned, this one
included, which is why the probes below are assembled from pieces."""

from __future__ import annotations

import pathlib
import re
import subprocess
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
ROOT = TREE.parent.parent
REL = "research/boundary_seed"
EXEMPT = {"SEED.md"}

SEALED_PATTERNS: tuple[tuple[str, str], ...] = (
    ("citation into the sealed paper", r"\bpaper/[A-Za-z0-9_]+\.md"),
    ("citation into the sealed artifacts", r"\bartifacts/[A-Za-z0-9_./]+"),
    ("citation into the sealed Lean", r"\blean4/Derivation/[A-Za-z]"),
    ("citation into the sealed kernel", r"\bcode/derivation/[A-Za-z_]"),
    ("sealed claim identifier", r"\bCL-[A-Z0-9]"),
    ("sealed Lean name", r"\bDerivation\.[A-Z]"),
    ("import of the sealed kernel", r"^\s*(?:from|import)\s+derivation\b"),
)


def other_trees() -> list[str]:
    """Names of the other research trees at HEAD.  A directory listing,
    not a reading of any tree."""
    proc = subprocess.run(
        ["git", "ls-tree", "--name-only", "HEAD", "research/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    names = [line.strip().split("/")[-1] for line in proc.stdout.splitlines() if line.strip()]
    return sorted(n for n in names if n and n != "boundary_seed")


def tree_patterns(names: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for name in names:
        out.append((f"other research tree {name}", rf"\bresearch/{re.escape(name)}\b"))
        if "_" in name:
            out.append((f"other research tree {name}", rf"\b{re.escape(name)}\b"))
    return out


def scan_text(text: str, patterns: list[tuple[str, str]]) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pat in patterns:
            if re.search(pat, line):
                hits.append((lineno, label))
    return hits


def write_root_files() -> list[pathlib.Path]:
    proc = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", REL],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(ROOT / line.strip() for line in proc.stdout.splitlines() if line.strip())


def all_patterns() -> list[tuple[str, str]]:
    return list(SEALED_PATTERNS) + tree_patterns(other_trees())


class BlindnessScan(unittest.TestCase):
    def test_write_root_is_blind_before_the_freeze(self) -> None:
        if (TREE / "FREEZE.md").exists():
            self.skipTest("FREEZE.md exists; the citation ban is retired")
        patterns = all_patterns()
        problems: list[str] = []
        for path in write_root_files():
            if path.name in EXEMPT or not path.exists():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for lineno, label in scan_text(text, patterns):
                problems.append(f"{path.relative_to(ROOT)}:{lineno}: {label}")
        self.assertEqual(problems, [], "\n".join(problems))


class ScanProbes(unittest.TestCase):
    """Each probe is assembled so that this file carries no citation."""

    def hits(self, text: str) -> list[str]:
        return [label for _, label in scan_text(text, all_patterns())]

    def test_probe_paper(self) -> None:
        self.assertEqual(self.hits("see " + "paper/" + "paper.md"), ["citation into the sealed paper"])

    def test_probe_artifacts(self) -> None:
        self.assertEqual(self.hits("art" + "ifacts/" + "claims.json"), ["citation into the sealed artifacts"])

    def test_probe_lean(self) -> None:
        self.assertEqual(self.hits("lean4/Deri" + "vation/" + "Basic.lean"), ["citation into the sealed Lean"])

    def test_probe_kernel(self) -> None:
        self.assertEqual(self.hits("code/deri" + "vation/" + "model.py"), ["citation into the sealed kernel"])

    def test_probe_claim_id(self) -> None:
        self.assertEqual(self.hits("C" + "L-" + "0-INERTIA"), ["sealed claim identifier"])

    def test_probe_lean_name(self) -> None:
        self.assertEqual(self.hits("Deri" + "vation." + "Foo"), ["sealed Lean name"])

    def test_probe_import(self) -> None:
        self.assertEqual(self.hits("from deri" + "vation import model"), ["import of the sealed kernel"])
        self.assertEqual(self.hits("import deri" + "vation"), ["import of the sealed kernel"])
        self.assertEqual(self.hits("from boundary import model"), [])

    def test_probe_other_tree(self) -> None:
        names = other_trees()
        self.assertGreater(len(names), 0)
        underscored = [n for n in names if "_" in n]
        self.assertGreater(len(underscored), 0)
        name = underscored[0]
        self.assertEqual(self.hits(name), [f"other research tree {name}"])
        self.assertEqual(self.hits("research/" + name), [f"other research tree {name}"] * 2)
        plain = [n for n in names if "_" not in n]
        if plain:
            self.assertEqual(self.hits("the " + plain[0] + " commit"), [])
            self.assertEqual(self.hits("research/" + plain[0]), [f"other research tree {plain[0]}"])

    def test_bare_directory_names_are_not_citations(self) -> None:
        self.assertEqual(self.hits("nothing under paper/, artifacts/, or lean4/Derivation/ is read"), [])


if __name__ == "__main__":
    unittest.main()
