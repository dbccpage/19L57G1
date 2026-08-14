"""The transport document's Lean citations must stay bound to the sources.

``contact/analysis/lean_theorem_transport.md`` is the evidence boundary for the
contact run: it says which declarations exist on disk and where.  PR #20 added
declarations to ``ContactKernel.lean`` without regenerating the document, so its
anchor undercounted the post-anchor set and every ``ContactKernel`` citation
below the insertion drifted -- in the worst case by 255 lines.  Nothing caught
it, because no gate read the document.

This test reads it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "ci"))

import check_transport_citations as checker  # noqa: E402


@pytest.fixture(autouse=True)
def _cwd(monkeypatch: pytest.MonkeyPatch) -> None:
    """The checker resolves its paths relative to the repository root."""
    monkeypatch.chdir(REPO)


def test_every_citation_resolves_and_matches() -> None:
    assert checker.main() == 0


def test_no_citation_is_left_unresolved() -> None:
    index = checker.index_sources()
    known = frozenset(index)
    text = checker.DOC.read_text(encoding="utf-8")
    unresolved = [
        (row.module, row.name)
        for row in checker.citations(text, known)
        if isinstance(row, checker.Verified)
        and checker.resolve(index[row.module], row.name) is None
    ]
    assert unresolved == []


def test_every_raw_token_receives_a_classification() -> None:
    index = checker.index_sources()
    text = checker.DOC.read_text(encoding="utf-8")
    rows = checker.citations(text, frozenset(index))

    assert checker.raw_token_count(text) == 188
    assert len(rows) == checker.raw_token_count(text)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("orphan `:12`", checker.Unresolvable),
        ("`hsurj : DeltaOnto K` (`:12`)", checker.WrappedIdentifier),
        ("`Missing.someDecl` (`Missing.lean:12`)", checker.UnknownModule),
    ],
)
def test_previously_silent_paths_are_typed(
    text: str, expected: type[object]
) -> None:
    rows = checker.citations(text, frozenset({"ContactKernel"}))

    assert len(rows) == 1
    assert isinstance(rows[0], expected)


def test_unclassifiable_token_makes_the_checker_fail(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    doc = tmp_path / "transport.md"
    doc.write_text("orphan `:12`\n", encoding="utf-8")
    monkeypatch.setattr(checker, "DOC", doc)

    assert checker.main() == 1
    assert "Unresolvable" in capsys.readouterr().out


def test_unknown_declaration_makes_the_checker_fail(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    doc = tmp_path / "transport.md"
    doc.write_text(
        "`ContactKernel.not_a_declaration` (`ContactKernel.lean:12`)\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "DOC", doc)

    assert checker.main() == 1
    assert "unresolved declaration" in capsys.readouterr().out


def test_fix_does_not_rewrite_unclassifiable_tokens() -> None:
    index = checker.index_sources()
    known = frozenset(index)
    texts = [
        "orphan `:12`\n",
        "`hsurj : DeltaOnto K` (`:12`)\n",
        "`Missing.someDecl` (`Missing.lean:12`)\n",
    ]

    for text in texts:
        assert checker.rewrite(text, index, known) == text


def test_fix_does_not_rewrite_an_error_with_the_same_line_number() -> None:
    index = {"Known": {"decl": 5}}
    text = "`Known.decl` (`Known.lean:12`) then orphan `:12`\n"

    fixed = checker.rewrite(text, index, frozenset(index))

    assert fixed == "`Known.decl` (`Known.lean:5`) then orphan `:12`\n"


def test_totality_assertion_rejects_a_dropped_classification() -> None:
    text = "orphan `:12` and `wrapped identifier` (`:13`)"
    rows = checker.citations(text, frozenset())
    assert len(rows) == 2

    # Models a future edit that reintroduces a silent ``continue`` after one
    # of the two raw matches instead of appending its typed classification.
    with pytest.raises(AssertionError, match="2 raw token.*1 classified"):
        checker._assert_totality(checker.raw_token_count(text), len(rows) - 1)


def test_checker_detects_injected_drift() -> None:
    """A negative test: the checker must actually fail on a bad citation."""
    index = checker.index_sources()
    known = frozenset(index)
    text = checker.DOC.read_text(encoding="utf-8")
    rows = [
        row
        for row in checker.citations(text, known)
        if isinstance(row, checker.Verified)
    ]
    assert rows, "no citations parsed at all"

    row = rows[0]
    lines = text.splitlines(keepends=True)
    lines[row.doc_line - 1] = lines[row.doc_line - 1].replace(
        f":{row.cited_line}`", f":{row.cited_line + 9999}`"
    )
    broken = "".join(lines)

    still_drifted = [
        (candidate.module, candidate.name)
        for candidate in checker.citations(broken, known)
        if isinstance(candidate, checker.Verified)
        and (
            actual := checker.resolve(
                index[candidate.module], candidate.name
            )
        )
        is not None
        and actual != candidate.cited_line
    ]
    assert still_drifted, "injected drift was not detected"


def test_index_finds_known_declarations() -> None:
    index = checker.index_sources()
    assert "ContactKernel" in index
    assert "obstP_factors" in index["PrimitivePassage"]
    assert "no_equivariant_pair_valued_map" in index["ContactKernel"]
