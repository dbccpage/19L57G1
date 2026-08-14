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


def citations(
    text: str, known: frozenset[str]
) -> list[tuple[int, str, str, int]]:
    """Yield (doc_line, module, decl_name, cited_line) for each citation.

    The declaration name is the nearest backticked dotted identifier
    preceding the citation on the same line.  Its own namespace prefix wins
    when it names a known module (the document routinely cites, say,
    ``DiffInterface.ZeroRel`` in a paragraph whose last explicit file was
    ``ContactBridge.lean``); otherwise the most recently named file is
    inherited.
    """
    out: list[tuple[int, str, str, int]] = []
    current = ""
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in CITE.finditer(line):
            if m.group("file"):
                current = m.group("file")
            before = line[: m.start()]
            segments = BACKTICKED.findall(before)
            if not segments:
                continue
            # The name must be the IMMEDIATELY preceding backticked segment.
            # If that segment is not a plain dotted identifier -- e.g.
            # `hsurj : DeltaOnto K` -- the citation is left unresolved rather
            # than mis-attributed to an earlier name on the same line.
            raw = segments[-1].lstrip(".")
            if IDENT.fullmatch(raw) is None:
                continue
            parts = raw.split(".")
            if len(parts) > 1 and parts[0] in known:
                module, rest = parts[0], parts[1:]
            else:
                module, rest = current, parts
            if not module:
                continue
            # A declaration may itself be dotted (`ObsQuotient.mk`), so try the
            # longest remaining suffix first and fall back to the last segment.
            out.append((lineno, module, ".".join(rest), int(m.group("line"))))
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
    lines = text.splitlines(keepends=True)
    fixes: dict[tuple[int, int], int] = {}
    for doc_line, module, name, cited in citations(text, known):
        table = index.get(module)
        if table is None:
            continue
        actual = resolve(table, name)
        if actual is not None:
            fixes[(doc_line, cited)] = actual
    for (doc_line, cited), actual in fixes.items():
        if actual == cited:
            continue
        raw = lines[doc_line - 1]

        def sub(m: re.Match[str], _c: int = cited, _a: int = actual) -> str:
            if int(m.group("line")) != _c:
                return m.group(0)
            prefix = f"{m.group('file')}.lean" if m.group("file") else ""
            return f"`{prefix}:{_a}`"

        lines[doc_line - 1] = CITE.sub(sub, raw)
    return "".join(lines)


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
    for doc_line, module, name, cited in citations(text, known):
        table = index.get(module)
        if table is None:
            continue
        actual = resolve(table, name)
        if actual is None:
            unknown.append(f"  {DOC}:{doc_line}: {module}.{name} not found in source")
            continue
        checked += 1
        if actual != cited:
            drift.append(
                f"  {DOC}:{doc_line}: {module}.{name} cited :{cited}, actual :{actual}"
            )
    if drift:
        print(f"FAIL: {len(drift)} stale line citation(s) in {DOC}")
        for row in drift:
            print(row)
        return 1
    print(f"transport citations clean: {checked} verified, {len(unknown)} unresolved")
    for row in unknown:
        print(row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
