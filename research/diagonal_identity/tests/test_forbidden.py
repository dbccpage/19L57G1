"""Denylist and outside-name scanners.  Injections are built at runtime.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Iterator

TREE = Path(__file__).resolve().parents[1]
REPO = TREE.parents[1]
DENYLIST_JSON = REPO / "contact" / "analysis" / "contact_countermodels.json"

OUTSIDE_STEMS = (
    "Law" + "vere",
    "Yano" + "fsky",
    "Can" + "tor",
    "Russ" + "ell",
    "Go" + "del",
    "Tur" + "ing",
    "Tars" + "ki",
)


def tree_files() -> Iterator[Path]:
    for path in sorted(TREE.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(TREE).parts
        if any(part.startswith(".") or part == "__pycache__" for part in relative[:-1]):
            continue
        if path.suffix in {".pyc", ".json"}:
            continue
        yield path


def working_denylist() -> list[str]:
    payload = json.loads(DENYLIST_JSON.read_text(encoding="utf-8"))
    block = payload["denylist"]
    assert isinstance(block, dict)
    full = block["full_census"]
    subtracted = block["subtracted_as_native_or_core"]
    assert isinstance(full, list) and isinstance(subtracted, list)
    names = [n for n in full if isinstance(n, str) and n not in set(subtracted)]
    assert len(names) == 102
    return names


def denylist_pattern(names: list[str]) -> re.Pattern[str]:
    return re.compile(r"(?<![\w])(?:" + "|".join(re.escape(n) for n in names) + r")(?![\w])")


class ForbiddenTests(unittest.TestCase):
    def test_denylist_absent_from_tree(self) -> None:
        pattern = denylist_pattern(working_denylist())
        hits: list[str] = []
        for path in tree_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            if pattern.search(text):
                hits.append(str(path.relative_to(TREE)))
        self.assertEqual(hits, [])

    def test_outside_stems_absent_from_tree(self) -> None:
        hits: list[str] = []
        for path in tree_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for stem in OUTSIDE_STEMS:
                if re.search(r"(?<![\w])" + re.escape(stem) + r"(?![\w])", text):
                    hits.append(f"{path.relative_to(TREE)}:{stem}")
        self.assertEqual(hits, [])

    def test_injection_is_detected(self) -> None:
        sample = "see " + OUTSIDE_STEMS[0] + " here"
        self.assertRegex(sample, r"(?<![\w])" + re.escape(OUTSIDE_STEMS[0]) + r"(?![\w])")
        names = working_denylist()
        self.assertTrue(denylist_pattern(names).search(" " + names[0] + " "))

    def test_lakefile_has_no_path_require(self) -> None:
        text = (TREE / "lean" / "lakefile.lean").read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.split("--", 1)[0].strip()
            self.assertFalse(stripped.startswith("require"))


if __name__ == "__main__":
    unittest.main()
