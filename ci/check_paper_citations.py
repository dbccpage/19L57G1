"""Cross-reference gate for prose documents.

Usage: python ci/check_paper_citations.py

Every repository-relative document path cited inside ``paper/*.md`` must
exist. A citation to a sibling that was written but never merged is a dead
link, and it reads as a completed chain that is not there -- the wrong
defect class on pages whose subject is residual honesty.

This happened: ``paper/primitive_difference_ascent.md`` was opened for
review citing ``paper/representative_selection.md``, which existed only on
an unmerged branch. A reviewer caught it. No gate did.

WHAT THIS CHECKS, EXACTLY

The population is every ``paper/<name>.md`` token appearing inside a file
under ``paper/``. Each must resolve to a file on disk. Nothing else is
inspected: not whether a citation is apt, not whether the cited document
supports the sentence citing it, not merge order.

WHY DISK EXISTENCE IS THE RIGHT TEST HERE

On a ``pull_request`` event ``actions/checkout`` checks out the merge
commit, so the working tree in CI *is* the merge result -- the state that
would land. A plain existence check therefore has merge-result semantics
in CI without computing a merge.

Run on a branch locally it is weaker: it sees the branch, not the merge.
That difference matters only when ``main`` moves under the branch, which
is the case this gate does not claim to cover.

An earlier draft justified this gate by claiming a working-tree check
"passes on the very defect it is meant to catch". That was FALSE for the
incident above -- the cited file was on neither ``main`` nor the citing
branch, so existence alone would have caught it. The gate is worth having
for the plain reason, not the elaborate one.

POPULATION: NOTHING IS TRUNCATED

There is no cap, no sampling, and no "first N" anywhere here. Every source
under ``paper/`` is read and every match in it is checked. Enumeration
finding *nothing* fails closed, because a census that returns an empty set
is broken rather than clean.

The source walk is RECURSIVE, so a document placed in a subdirectory of
``paper/`` cannot escape it. ``paper/`` is flat today, so recursion changes
no current result; it is here because the Lean module census had to learn
the same lesson, and a non-recursive walk is silent exactly when a
subdirectory appears.

Two things are deduplicated rather than dropped: a path cited twice in one
document is checked once, and the reported count is of DISTINCT paths per
document, not of occurrences. That affects the number printed, never
whether a dead path is caught.
"""

import pathlib
import re
import sys

PAPER = pathlib.Path("paper")

# Deliberately narrow: a repository-relative path to a prose document.
# Anchored on the directory name so prose about "paper" is not swept in.
CITE = re.compile(r"\bpaper/[A-Za-z0-9_.-]+\.md\b")


def main() -> int:
    if not PAPER.is_dir():
        print(f"FAIL: {PAPER} is not a directory")
        return 1

    sources = sorted(PAPER.rglob("*.md"))
    if not sources:
        print(f"FAIL: no *.md found under {PAPER} - the enumeration is broken")
        return 1

    failures: list[str] = []
    citations = 0
    for source in sources:
        text = source.read_text(encoding="utf-8")
        for cited in sorted(set(CITE.findall(text))):
            citations += 1
            if not pathlib.Path(cited).is_file():
                failures.append(f"{source}: cites {cited}, which does not exist")

    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        print(
            "A cited document that is written but unmerged is still a dead "
            "link on main. Land the sibling, or remove the citation."
        )
        return 1
    print(
        f"paper cross-references resolve: {citations} citation(s) across "
        f"{len(sources)} document(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
