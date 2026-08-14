"""Verify the transport document's Lean citations against the sources.

``contact/analysis/lean_theorem_transport.md`` cites Lean declarations by
file and line, in two forms::

    `ContactBridge.obsApart` (`ContactBridge.lean:116`)   -- explicit file
    `ContactBridge.obsApart_irrefl` (`:119`)              -- inherits the file

PR #20 added declarations to ``ContactKernel.lean`` without regenerating
these citations, so every ``ContactKernel`` line reference downstream of the
insertion drifted by about 33 lines and nothing caught it.  This checker
recomputes each cited line from the Lean sources and fails on any drift.

Usage::

    python ci/check_transport_citations.py
"""

from __future__ import annotations

import pathlib
import re
import sys
from dataclasses import dataclass
from typing import TypeAlias

DOC = pathlib.Path("contact") / "analysis" / "lean_theorem_transport.md"
LEAN_DIR = pathlib.Path("lean4") / "Derivation"

# A declaration head: `theorem foo`, `def foo`, `abbrev foo`, ...
DECL = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(?:theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_.']*)"
)
# A citation: `Foo.lean:123` or `:123`, always inside backticks.
CITE = re.compile(r"`(?:(?P<file>[A-Za-z_][A-Za-z0-9_]*)\.lean)?:(?P<line>\d+)`")
# Any backticked segment, and the shape a segment must have to name a decl.
BACKTICKED = re.compile(r"`([^`]*)`")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")


@dataclass(frozen=True)
class Verified:
    """A raw citation token with enough context to check against Lean."""

    doc_line: int
    raw_token: str
    module: str
    name: str
    cited_line: int
    token_start: int
    token_end: int


@dataclass(frozen=True)
class Unresolvable:
    """A citation with no preceding backticked declaration segment."""

    doc_line: int
    raw_token: str
    cited_line: int
    token_start: int
    token_end: int


@dataclass(frozen=True)
class WrappedIdentifier:
    """A citation preceded by a backticked segment that is not an identifier."""

    doc_line: int
    raw_token: str
    cited_line: int
    preceding_segment: str
    token_start: int
    token_end: int


@dataclass(frozen=True)
class UnknownModule:
    """A citation whose explicit or inherited module is absent from the index."""

    doc_line: int
    raw_token: str
    cited_line: int
    module: str
    name: str
    token_start: int
    token_end: int


CitationClassification: TypeAlias = (
    Verified | Unresolvable | WrappedIdentifier | UnknownModule
)
ClassificationError: TypeAlias = Unresolvable | WrappedIdentifier | UnknownModule


def index_sources() -> dict[str, dict[str, int]]:
    """Map module stem -> declaration name -> 1-indexed line number."""
    index: dict[str, dict[str, int]] = {}
    for path in sorted(LEAN_DIR.glob("*.lean")):
        table: dict[str, int] = {}
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            m = DECL.match(line)
            if m is not None:
                table.setdefault(m.group("name"), lineno)
        index[path.stem] = table
    return index


def raw_token_count(text: str) -> int:
    """Count every raw ``...:NNN`` citation token recognized by the checker."""
    return sum(1 for _ in CITE.finditer(text))


def _assert_totality(raw_count: int, classified_count: int) -> None:
    """Assert that the parser classified every raw citation token exactly once."""
    assert raw_count == classified_count, (
        "citation classification is not total: "
        f"{raw_count} raw token(s), {classified_count} classified"
    )


def citations(text: str, known: frozenset[str]) -> list[CitationClassification]:
    """Return one typed classification for every raw citation token.

    The declaration name is the nearest backticked dotted identifier
    preceding the citation on the same line.  Its own namespace prefix wins
    when it names a known module (the document routinely cites, say,
    ``DiffInterface.ZeroRel`` in a paragraph whose last explicit file was
    ``ContactBridge.lean``); otherwise the most recently named file is
    inherited.
    """
    out: list[CitationClassification] = []
    raw_count = 0
    current = ""
    line_start = 0
    for lineno, line in enumerate(text.splitlines(keepends=True), start=1):
        for m in CITE.finditer(line):
            raw_count += 1
            token_start = line_start + m.start()
            token_end = line_start + m.end()
            if m.group("file"):
                current = m.group("file")
            before = line[: m.start()]
            segments = BACKTICKED.findall(before)
            if not segments:
                classification: CitationClassification = Unresolvable(
                    doc_line=lineno,
                    raw_token=m.group(0),
                    cited_line=int(m.group("line")),
                    token_start=token_start,
                    token_end=token_end,
                )
            else:
                # The name must be the IMMEDIATELY preceding backticked
                # segment.  A wrapped proposition such as
                # `hsurj : DeltaOnto K` is not silently attributed to an
                # earlier name on the line.
                raw = segments[-1].lstrip(".")
                if IDENT.fullmatch(raw) is None:
                    classification = WrappedIdentifier(
                        doc_line=lineno,
                        raw_token=m.group(0),
                        cited_line=int(m.group("line")),
                        preceding_segment=segments[-1],
                        token_start=token_start,
                        token_end=token_end,
                    )
                else:
                    parts = raw.split(".")
                    if len(parts) > 1 and parts[0] in known:
                        module, rest = parts[0], parts[1:]
                    else:
                        module, rest = current, parts
                    name = ".".join(rest)
                    if module not in known:
                        classification = UnknownModule(
                            doc_line=lineno,
                            raw_token=m.group(0),
                            cited_line=int(m.group("line")),
                            module=module,
                            name=name,
                            token_start=token_start,
                            token_end=token_end,
                        )
                    else:
                        classification = Verified(
                            doc_line=lineno,
                            raw_token=m.group(0),
                            module=module,
                            name=name,
                            cited_line=int(m.group("line")),
                            token_start=token_start,
                            token_end=token_end,
                        )
            out.append(classification)
        line_start += len(line)
    _assert_totality(raw_count, len(out))
    return out


def resolve(table: dict[str, int], name: str) -> int | None:
    """Look up a possibly-dotted declaration name in a module's table."""
    parts = name.split(".")
    for start in range(len(parts)):
        found = table.get(".".join(parts[start:]))
        if found is not None:
            return found
    return None


def rewrite(text: str, index: dict[str, dict[str, int]], known: frozenset[str]) -> str:
    """Return the document with every resolvable citation line corrected."""
    fixes: list[tuple[int, int, str]] = []
    for row in citations(text, known):
        # Typed errors are deliberately excluded: --fix may only rewrite a
        # token whose module and declaration context were classified.
        if isinstance(row, Verified):
            actual = resolve(index[row.module], row.name)
            if actual is not None and actual != row.cited_line:
                match = CITE.fullmatch(row.raw_token)
                assert match is not None
                prefix = f"{match.group('file')}.lean" if match.group("file") else ""
                fixes.append(
                    (row.token_start, row.token_end, f"`{prefix}:{actual}`")
                )
    fixed = text
    for token_start, token_end, replacement in reversed(fixes):
        fixed = fixed[:token_start] + replacement + fixed[token_end:]
    return fixed


def main() -> int:
    if not DOC.exists():
        print(f"FAIL: {DOC} not found")
        return 1
    index = index_sources()
    known = frozenset(index)
    text = DOC.read_text(encoding="utf-8")

    if "--fix" in sys.argv[1:]:
        fixed = rewrite(text, index, known)
        if fixed != text:
            DOC.write_bytes(fixed.encode("utf-8"))
            print(f"rewrote {DOC}")
        else:
            print(f"{DOC} already current")
        text = DOC.read_text(encoding="utf-8")

    checked = 0
    drift: list[str] = []
    unknown: list[str] = []
    classification_errors: list[str] = []
    for row in citations(text, known):
        if not isinstance(row, Verified):
            classification_errors.append(format_classification_error(row))
            continue
        actual = resolve(index[row.module], row.name)
        if actual is None:
            unknown.append(
                f"  {DOC}:{row.doc_line}: "
                f"{row.module}.{row.name} not found in source"
            )
            continue
        checked += 1
        if actual != row.cited_line:
            drift.append(
                f"  {DOC}:{row.doc_line}: {row.module}.{row.name} "
                f"cited :{row.cited_line}, actual :{actual}"
            )
    failed = False
    if classification_errors:
        failed = True
        print(
            f"FAIL: {len(classification_errors)} unclassifiable citation(s) in {DOC}"
        )
        for row in classification_errors:
            print(row)
    if drift:
        failed = True
        print(f"FAIL: {len(drift)} stale line citation(s) in {DOC}")
        for row in drift:
            print(row)
    if unknown:
        failed = True
        print(f"FAIL: {len(unknown)} unresolved declaration citation(s) in {DOC}")
        for row in unknown:
            print(row)
    if failed:
        return 1
    print(f"transport citations clean: {checked} verified, 0 unresolved")
    return 0


def format_classification_error(row: ClassificationError) -> str:
    """Render a typed parser failure for the CI diagnostic."""
    prefix = f"  {DOC}:{row.doc_line}: {type(row).__name__}: {row.raw_token}"
    if isinstance(row, Unresolvable):
        return f"{prefix} has no preceding backticked declaration"
    if isinstance(row, WrappedIdentifier):
        return f"{prefix} follows `{row.preceding_segment}`, not a plain identifier"
    module = row.module or "<no inherited module>"
    return f"{prefix} names unknown module {module}"


if __name__ == "__main__":
    sys.exit(main())
