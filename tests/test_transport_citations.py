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
        (module, name)
        for _, module, name, _ in checker.citations(text, known)
        if module in index and checker.resolve(index[module], name) is None
    ]
    assert unresolved == []


def test_checker_detects_injected_drift() -> None:
    """A negative test: the checker must actually fail on a bad citation."""
    index = checker.index_sources()
    known = frozenset(index)
    text = checker.DOC.read_text(encoding="utf-8")
    rows = checker.citations(text, known)
    assert rows, "no citations parsed at all"

    doc_line, module, name, cited = rows[0]
    lines = text.splitlines(keepends=True)
    lines[doc_line - 1] = lines[doc_line - 1].replace(f":{cited}`", f":{cited + 9999}`")
    broken = "".join(lines)

    still_drifted = [
        (m, n)
        for _, m, n, c in checker.citations(broken, known)
        if m in index
        and (actual := checker.resolve(index[m], n)) is not None
        and actual != c
    ]
    assert still_drifted, "injected drift was not detected"


def test_index_finds_known_declarations() -> None:
    index = checker.index_sources()
    assert "ContactKernel" in index
    assert "obstP_factors" in index["PrimitivePassage"]
    assert "no_swap_equivariant_pair_selector" in index["ContactKernel"]
