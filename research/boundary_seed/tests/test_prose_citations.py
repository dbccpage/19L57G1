"""Every test name a tree document presents as code must resolve to a test
this suite defines.

The injection record and the claim ledger cite negative tests by name.  A
rename leaves the citation naming a test that cannot be run; that happened
twice, and review found it because no gate read the names.  The declared
population is every ``test_*`` token appearing ANYWHERE inside a backtick
span of the write root's Markdown, except the read-only ``SEED.md``; a
retired name is written in plain text beside its successor, so a name
presented as code is always runnable.  The check reads names only: it cannot
say that a citation describes what its test does.

The population was first read as spans that are exactly a name, which missed
a name quoted inside a longer span — a quoted failure line, for instance,
which is where two retired names were hiding.  A token immediately followed
by ``.py`` is a FILE name and not a test name, so it is skipped: the tree
cites its own test files that way and those citations resolve as paths, not
as runnable tests.
"""

from __future__ import annotations

import pathlib
import re
import tempfile
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
SPAN = re.compile(r"`([^`]*)`")
NAME = re.compile(r"(?<![A-Za-z0-9_])(test_[A-Za-z0-9_]+)(\.py)?")
DEFINITION = re.compile(r"^\s*def (test_[A-Za-z0-9_]+)\s*\(", re.M)


def names_in_span(span: str) -> list[str]:
    """The test names a backtick span carries.  A token followed by ``.py``
    is a file name and is not one."""
    return [m.group(1) for m in NAME.finditer(span) if m.group(2) is None]


def defined_test_names(tests_dir: pathlib.Path) -> set[str]:
    """Every test this suite defines, by name."""
    names: set[str] = set()
    for path in sorted(tests_dir.glob("test_*.py")):
        names.update(DEFINITION.findall(path.read_text(encoding="utf-8")))
    return names


def cited_test_names(tree: pathlib.Path) -> list[tuple[str, int, str]]:
    """Every backticked test name in the tree's Markdown, with its place."""
    found: list[tuple[str, int, str]] = []
    for path in sorted(tree.rglob("*.md")):
        if path.name == "SEED.md" or ".lake" in path.parts:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for span in SPAN.findall(line):
                for name in names_in_span(span):
                    found.append((path.relative_to(tree).as_posix(), lineno, name))
    return found


def unresolved_citations(tree: pathlib.Path) -> list[str]:
    """Cited names that no test defines, each named with its place."""
    defined = defined_test_names(tree / "tests")
    return [
        f"{where}:{lineno}: {name} matches no test defined in tests/"
        for where, lineno, name in cited_test_names(tree)
        if name not in defined
    ]


class CitationTests(unittest.TestCase):
    def test_every_cited_test_name_resolves(self) -> None:
        cited = cited_test_names(TREE)
        self.assertGreater(len(cited), 0, "the citation scan found nothing to check")
        self.assertEqual(unresolved_citations(TREE), [])

    def test_planted_unresolvable_citation_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tree = pathlib.Path(tmp)
            (tree / "tests").mkdir()
            (tree / "tests" / "test_probe.py").write_text(
                "def test_kept() -> None:\n    pass\n", encoding="utf-8"
            )
            (tree / "SEED.md").write_text("`test_exempt_by_declaration`\n", encoding="utf-8")
            (tree / "MANUAL.md").write_text(
                "row one `test_kept` stands\nrow two `test_renamed_away` does not\n",
                encoding="utf-8",
            )
            self.assertEqual(
                unresolved_citations(tree),
                ["MANUAL.md:2: test_renamed_away matches no test defined in tests/"],
            )

    def test_a_name_quoted_inside_a_longer_span_is_found(self) -> None:
        # The direction the first population missed: a name inside a quoted
        # diagnostic, which is exactly where two retired names were hiding.
        self.assertEqual(
            names_in_span("FAIL: test_renamed_away matches no test defined in tests/"),
            ["test_renamed_away"],
        )
        self.assertEqual(names_in_span("`"), [])
        self.assertEqual(
            names_in_span("test_one and test_two"), ["test_one", "test_two"]
        )
        self.assertEqual(names_in_span("suffixed_test_one"), [])

    def test_a_test_file_name_is_not_a_test_name(self) -> None:
        # The tree cites its own test files; those citations resolve as paths
        # and never as runnable tests, so they are not in the population.  The
        # name must not be truncated to make the file suffix disappear.
        self.assertEqual(names_in_span("tests/test_prose_citations.py"), [])
        self.assertEqual(names_in_span("`tests/test_blind.py`"), [])
        self.assertEqual(
            names_in_span("test_kept in tests/test_probe.py"), ["test_kept"]
        )

    def test_the_planted_file_name_does_not_fire(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tree = pathlib.Path(tmp)
            (tree / "tests").mkdir()
            (tree / "tests" / "test_probe.py").write_text(
                "def test_kept() -> None:\n    pass\n", encoding="utf-8"
            )
            (tree / "MANUAL.md").write_text(
                "the gate lives in `tests/test_probe.py` and `tests/test_absent.py`\n",
                encoding="utf-8",
            )
            self.assertEqual(cited_test_names(tree), [])
            self.assertEqual(unresolved_citations(tree), [])


if __name__ == "__main__":
    unittest.main()
