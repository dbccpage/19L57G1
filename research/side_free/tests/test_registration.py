"""The registered CI step's own pin, held against the suite it counts.

The step that runs this tree in `.github/workflows/verify.yml` asserts an
EXACT test count, so that an enumeration finding nothing cannot pass as a
green suite.  That guard is worth its parameter: the literal was written when
this suite had 321 tests and was not moved when two later commits added two
more, so the step could not pass at all, and nothing here read the workflow
to say so.

This test closes that.  The pinned count is parsed out of the workflow --
from this tree's OWN step, selected by its working directory, since sibling
steps carry the same guard with their own counts -- and must equal the count
this suite discovers.  It fails in both directions, a pin above the suite and
a pin below it being the same defect, and it names both numbers.

Classification: METATHEORY APPARATUS.  It reads the workflow and asserts
nothing about the object language.
"""

from __future__ import annotations

import pathlib
import re
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
ROOT = TREE.parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "verify.yml"

# The step's own line, matched as it is written.  A looser pattern would match
# a sibling tree's count and defeat the totality check below.
PINNED_COUNT = re.compile(r"^\s*grep -Eq '\^Ran (\d+) tests in ' \"\$log\"$", re.M)
OUR_STEP = re.compile(r"^\s*working-directory: research/side_free$", re.M)
STEP_START = re.compile(r"^\s*- name: ")


def step_blocks(text: str) -> list[str]:
    """The workflow's steps, each from its own `- name:` to the next."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if STEP_START.match(line)]
    return [
        "\n".join(lines[start : (starts[k + 1] if k + 1 < len(starts) else len(lines))])
        for k, start in enumerate(starts)
    ]


def pinned_counts(text: str) -> list[int]:
    """Every test count pinned by a step of THIS tree."""
    return [
        int(value)
        for block in step_blocks(text)
        if OUR_STEP.search(block)
        for value in PINNED_COUNT.findall(block)
    ]


def discovered_test_count() -> int:
    """The number of tests `unittest discover` finds under `tests/`.

    A fresh loader, so nothing about the outer run's loader state is
    disturbed.  The modules are already imported by that run, so this is a
    re-enumeration and not a second execution.
    """
    suite = unittest.TestLoader().discover(
        str(TREE / "tests"), pattern="test_*.py", top_level_dir=str(TREE / "tests")
    )
    return suite.countTestCases()


class RegisteredStep(unittest.TestCase):
    def test_the_workflow_pins_the_count_this_suite_discovers(self) -> None:
        self.assertTrue(WORKFLOW.exists(), f"{WORKFLOW} is missing")
        found = pinned_counts(WORKFLOW.read_text(encoding="utf-8"))
        self.assertEqual(
            len(found),
            1,
            "this tree's steps must pin exactly one test count; found "
            f"{len(found)} in .github/workflows/verify.yml",
        )
        discovered = discovered_test_count()
        self.assertEqual(
            found[0],
            discovered,
            ".github/workflows/verify.yml pins Ran "
            f"{found[0]} tests and this suite discovers {discovered}; "
            "bump the pin in the same commit that changes the suite size",
        )


if __name__ == "__main__":
    unittest.main()
