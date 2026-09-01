"""The refusal scans: supplied names, working denylist, sealed paths,
and the three protected opens.  Any hit fails the run.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

# The supplied vocabulary, assembled from fragments so this scan does
# not trip itself: the scan matches whole tokens in committed files.
_FRAGMENTS = [
    ("Hamil", "tonian"),
    ("hamil", "tonian"),
    ("Fermi", "on"),
    ("fermi", "on"),
    ("Sign ", "Problem"),
    ("sign ", "problem"),
    ("sto", "quastic"),
    ("Mars", "hall"),
    ("Hubb", "ard"),
    ("Grass", "mann"),
    ("Pfaff", "ian"),
    ("Major", "ana"),
    ("Hilb", "ert"),
    ("Schr", "odinger"),
    ("Monte ", "Carlo"),
]
SUPPLIED_TOKENS = ["".join(f) for f in _FRAGMENTS] + ["QMC", "FSP", "QCD"]

SEALED_PREFIXES = ("prompt/", "paper/", "code/", "lean4/Derivation/", "artifacts/")


def tree_files() -> list[Path]:
    return sorted(
        f for f in HERE.rglob("*")
        if f.is_file() and "receipts_replay" not in f.parts
        and "__pycache__" not in f.parts
    )


class SuppliedNameScan(unittest.TestCase):
    def test_no_supplied_vocabulary_in_the_write_root(self) -> None:
        for f in tree_files():
            if f.name == "test_forbidden.py":
                continue
            text = f.read_text("utf-8", errors="replace")
            for token in SUPPLIED_TOKENS:
                self.assertNotIn(
                    token, text, f"{f.name} contains a supplied token"
                )


class DenylistScan(unittest.TestCase):
    def test_no_working_denylist_identifier_in_the_write_root(self) -> None:
        census = json.loads(
            (REPO / "contact" / "analysis" / "contact_countermodels.json").read_text(
                "utf-8"
            )
        )
        full = set(census["denylist"]["full_census"])
        subtracted = set(census["denylist"]["subtracted_as_native_or_core"])
        working = sorted(full - subtracted)
        allowed = {"PrimitiveDifference"}
        for f in tree_files():
            text = f.read_text("utf-8", errors="replace")
            for token in working:
                if token in allowed:
                    continue
                self.assertNotIn(
                    token, text, f"{f.name} contains working-denylist token {token}"
                )


class SealedPathScan(unittest.TestCase):
    def test_no_sealed_path_is_modified(self) -> None:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=REPO, check=True,
        ).stdout
        for line in out.splitlines():
            path = line[3:].strip().strip('"')
            for prefix in SEALED_PREFIXES:
                self.assertFalse(
                    path.startswith(prefix),
                    f"sealed path touched: {path}",
                )


class ProtectedOpensScan(unittest.TestCase):
    def test_the_three_protected_opens_stay_open(self) -> None:
        status = (HERE / "STATUS.md").read_text("utf-8")
        for terminal in ("OB1_UNCHANGED", "S66_UNCHANGED", "S9_LAST_UNCHANGED"):
            self.assertIn(terminal, status)
        for f in tree_files():
            if f.name == "test_forbidden.py":
                continue
            text = f.read_text("utf-8", errors="replace")
            for bad in ("OB-1 is closed", "closes OB-1", "S6.6 is closed",
                        "discharges S6.6"):
                self.assertNotIn(bad, text, f"{f.name} claims a protected open closed")


class TotalitySentenceScan(unittest.TestCase):
    def test_no_completed_totality_sentence(self) -> None:
        for f in tree_files():
            if f.name == "test_forbidden.py":
                continue
            text = f.read_text("utf-8", errors="replace")
            for bad in ("the set of all presentations", "all solutions",
                        "ALL_SOLUTIONS_FOUND"):
                self.assertNotIn(bad, text, f"{f.name} claims totality")


if __name__ == "__main__":
    unittest.main()
