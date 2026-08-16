"""Cross-reference gate for prose documents.

Usage: python ci/check_paper_citations.py

Every repository-relative document path cited inside ``paper/`` must name a
real file inside ``paper/``. A citation to a sibling that was written but
never merged is a dead link, and reads as a completed chain that is not
there. That shipped once, and a reviewer caught it rather than a gate.

The rule, in one sentence: a citation is a ``paper/``-rooted path built from
ordinary name segments, and it must resolve to a file still under
``paper/``.

Both sides are nested-aware, and each had to be fixed separately -- the
source walk is recursive, and the citation grammar admits path segments.
Fixing one alone leaves the other silent at exactly the moment a
subdirectory appears.

Widening the grammar to allow ``/`` also admitted traversal. ``..`` and
``.`` are built from characters the segment class already permits, so
``paper/../README.md`` matched, and ``is_file`` followed it out of the
directory to a file that really exists -- the citation would have been
reported as resolving. Segments are therefore validated, and the resolved
path must stay under ``paper/``.

``EXTRACTS`` and ``ACCEPTS`` pin the two halves separately, because they
regress independently: the grammar can narrow while the segment rule stays
correct, and vice versa. A flat tree contains no real nested or traversing
citation, so without these the gate has nothing to detect such a regression
with. An earlier version tested only acceptance while claiming to pin both
-- replacing ``CITE`` with a pattern matching nothing left it green.

On a ``pull_request`` event ``actions/checkout`` materializes the merge
commit, so the tree CI sees is the state that would land and existence has
merge-result semantics. Locally on a branch it is weaker, which matters only
when ``main`` moves under the branch.

Nothing is truncated: every source is read, every match checked, and an
empty enumeration fails closed. A path cited twice in one document is
checked once, so the printed count is of distinct paths per document.
"""

import pathlib
import re
import sys

PAPER = pathlib.Path("paper")

CITE = re.compile(r"\bpaper/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.md\b")

# Two INDEPENDENT properties, pinned separately, because they can regress
# independently. An earlier version tested only the second and claimed to
# pin both; replacing CITE with a pattern matching nothing left it green.
#
# 1. EXTRACTION -- does CITE take the whole token?
EXTRACTS: tuple[tuple[str, bool], ...] = (
    ("paper/flat.md", True),
    ("paper/sub/nested.md", True),
    ("paper/a/b/deep.md", True),
    # Traversal is extracted and then refused; it must not be invisible,
    # or it would be silently uncheckable rather than reported.
    ("paper/../README.md", True),
    ("paper/foo/../../README.md", True),
    ("paper/./flat.md", True),
    # Guards against an over-broad pattern.
    ("notpaper/flat.md", False),
    ("paper/flat.txt", False),
    # Deliberate prose placeholders must stay out of the population.
    ("paper/*.md", False),
)

# 2. ACCEPTANCE -- does rejection() let the extracted token through?
ACCEPTS: tuple[tuple[str, bool], ...] = (
    ("paper/flat.md", True),
    ("paper/sub/nested.md", True),
    ("paper/a/b/deep.md", True),
    ("paper/../README.md", False),
    ("paper/foo/../../README.md", False),
    ("paper/./flat.md", False),
)


def extract(text: str) -> list[str]:
    """The one extraction operation.

    ``main`` and ``self_check`` both go through this, so the self-check
    cannot pass on a pattern that production would use differently. Testing
    ``fullmatch`` while production called ``findall`` left an anchored
    pattern green in the self-check and blind to every citation embedded in
    prose.
    """
    return CITE.findall(text)


def rejection(raw: str) -> str | None:
    """Reason the token is not a well-formed paper path, or None."""
    parts = raw.split("/")
    if not parts or parts[0] != "paper":
        return "is not rooted at paper/"
    for part in parts[1:]:
        if part in ("", ".", ".."):
            return f"contains the path segment {part!r}"
    return None


def self_check() -> list[str]:
    """Both halves must behave as declared, on a flat tree too.

    Extraction and acceptance are checked separately against ``CITE`` and
    ``rejection`` respectively, so that weakening either one is reported.
    """
    wrong = []
    for token, want_match in EXTRACTS:
        # Exercise the PRODUCTION operation, on a token embedded in prose
        # exactly as a real citation is.
        got_match = extract(f"see `{token}` here") == [token]
        if got_match != want_match:
            verb = "extracted" if got_match else "not extracted"
            wrong.append(f"self-check extraction: {token} was {verb}")
    for token, want_ok in ACCEPTS:
        got_ok = rejection(token) is None
        if got_ok != want_ok:
            verb = "accepted" if got_ok else "rejected"
            wrong.append(f"self-check acceptance: {token} was {verb}")
    return wrong


def main() -> int:
    failures = self_check()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print("The citation classifier does not match its declared behaviour.")
        return 1

    if not PAPER.is_dir():
        print(f"FAIL: {PAPER} is not a directory")
        return 1

    sources = sorted(PAPER.rglob("*.md"))
    if not sources:
        print(f"FAIL: no *.md found under {PAPER} - the enumeration is broken")
        return 1

    root = PAPER.resolve()
    citations = 0
    for source in sources:
        text = source.read_text(encoding="utf-8")
        for cited in sorted(set(extract(text))):
            citations += 1
            reason = rejection(cited)
            if reason is not None:
                failures.append(f"{source}: cites {cited}, which {reason}")
                continue
            target = pathlib.Path(cited)
            if not target.is_file():
                failures.append(
                    f"{source}: cites {cited}, which does not exist"
                )
                continue
            if root not in target.resolve().parents:
                failures.append(
                    f"{source}: cites {cited}, which resolves outside {PAPER}"
                )

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
