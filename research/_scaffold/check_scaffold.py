"""Drift lint for the copied research-tree scaffold.

AuthorityEffect: None.  Not a sealed gate; a repository-wide check that the
recurring scaffold bugs have not been copied into any `research/<tree>/`.  Run
from the repository root: `python research/_scaffold/check_scaffold.py`.

The research trees are deliberately self-contained: each keeps its own
`check_coverage.py` and `run.py` rather than importing a shared module, so the
same bug can be pasted into a new tree verbatim.  This lint keeps those copies
in sync with the canonical `research/_scaffold/` versions on the defects that
have actually recurred, at two severities:

  ERROR (blocks) -- COVERAGE_LEAK by substring.  The recent coverage gate
    matched omit directories with `part in path` (a substring test), so a
    module under a directory like `clean/` was falsely flagged.  The marker of
    the buggy generation is the module-level name `OMIT_PARTS`; the fixed
    version uses `OMIT_DIRS` + a path-component `_directories()` helper.  This
    is a correctness bug and must never ship in a new tree.  (Older trees use a
    different, component-correct gate with no `OMIT_PARTS`; those are clean.)

  ERROR (blocks) -- quote-excluding name capture in an axiom-report pattern.
    Lean prints a report as `'<name>' depends on axioms: [...]` or `'<name>'
    does not depend on any axioms`, and a primed theorem name ends in a quote
    character.  A pattern that captures the name with a negated class that
    excludes the quote (`'([^']+)'`) stops short on such a name and the report
    is silently dropped.  The root parsers dropped that form on 2026-08-18;
    the fixed research form, with its comment, is at
    `research/balance_carrier/verify_lean.py`: `'(.+?)'`.  This check reads
    STRING LITERALS, because `research/house_diff.py` blanks every literal
    before comparing and so cannot see a defect carried inside a regex.  One
    literal at a time, with adjacent literals joined as Python joins them, and
    `+` chains of literals and the fixed parts of an f-string folded; a pattern
    assembled from separately named pieces is not seen, and neither is a
    positive class that happens to omit the quote (`[\\w.]+`).  Docstrings and
    comments are prose and are not read.

    Two pinned lists, each keyed by path and pinned to the SHA-256 of the
    file's bytes (CRLF read as LF, i.e. the committed form), are the only
    places such a capture may stand without an error, and both are printed on
    every run.  Neither makes the form an accepted house variant:

      FROZEN_EXCEPTIONS -- the one permanent exception,
        `research/boundary_seed/verify_lean.py`, whose bytes
        `research/boundary_seed/verify_freeze.py` freezes.  Repairing it would
        break the freeze, so it stays, and stays named.

      REPAIR_PENDING -- copies that carried the capture when this check was
        added (2026-09-18) and are to be repaired.  It may only shrink:
        `tests/test_research_drift.py` fails if it names a path that was not
        in the 2026-09-18 population.  An entry excuses only its pinned bytes:
        once the file changes, the entry is an error until it is dropped (if
        the capture was repaired) or the capture is repaired (if not).  So a
        repair lands as the tree's own commit plus a separate commit here that
        deletes the entry.

  WARNING (reported, non-fatal) -- double custody scan.  `run.py`'s
    `receipt_bytes()` calls the expensive `verify_sources()` twice, once before
    and once after a pure record computation that writes no files, so the
    second scan is redundant.  This is efficiency only, and it CANNOT be
    retrofitted freely: several older trees pin each other's whole `.py` tree at
    a baseline commit (e.g. `record_reading` pins `setting_translation`,
    `represented_execution` and `coherent_process_limits`), so editing one
    tree's `run.py` breaks a consumer's custody and cascades repins.  A NEW tree
    should drop the second scan at creation, before any consumer pins it; an
    existing pinned tree is left until its family is deliberately repinned.

The lint prints every offender by path.  It exits non-zero only if an ERROR is
present, so a newly copied tree cannot re-introduce a correctness bug
unnoticed, while the known double-scans and the pinned captures stay visible
without wedging the check.  The ERROR checks are also run over the live tree by
`tests/test_research_drift.py` in the root suite.
"""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research"
SCAFFOLD = "_scaffold"

# The two phrases Lean prints after a quoted declaration name in an axiom
# report.  A literal carrying neither is not an axiom-report pattern.
AXIOM_PHRASES = ("depends on axioms", "does not depend on any axioms")
# A negated character class whose members include the quote character:
# `[^']`, `[^'\n]`, `[^\]']`, `[^]']`.  Escapes inside the class are skipped
# as pairs so that `\]` does not end it early.
QUOTE_EXCLUDING_CLASS = re.compile(r"\[\^\]?(?:\\.|[^\]\\])*'(?:\\.|[^\]\\])*\]")
FIXED_FORM = "'(.+?)' as in research/balance_carrier/verify_lean.py"

# The one permanent exception: frozen by research/boundary_seed/verify_freeze.py.
FROZEN_EXCEPTIONS: dict[str, str] = {
    "research/boundary_seed/verify_lean.py":
        "1ec8e85052547507f42e266f8588b6782e2d99042e29daea49893f4ba14f79db",
}
# Carried the capture on 2026-09-18 and are to be repaired; only shrinks.
REPAIR_PENDING: dict[str, str] = {
    "research/admission_sign_shadow/verify_frozen_compatibility.py":
        "d6f86ef4c70b7df19eb9c31d00ba667afb20188542dae28b66075f86fdcebebb",
    "research/admission_sign_shadow/verify_lean.py":
        "8b75c6349fafe96cc8f608c8ece5cd37f6dacc1b9b6d8bc716085ef9885b019c",
    "research/described_replay/verify_lean.py":
        "7fee00bb85124841128450d1deede63b12d0a6915985f3caa083b4b12aa38184",
}


def _tree_dirs(root: Path = ROOT) -> list[Path]:
    research = root / "research"
    return sorted(
        p for p in research.iterdir()
        if p.is_dir() and p.name != SCAFFOLD and not p.name.startswith(".")
    )


def coverage_errors(root: Path = ROOT) -> list[str]:
    """Trees whose check_coverage.py carries the substring-leak generation."""
    out: list[str] = []
    for tree in _tree_dirs(root):
        gate = tree / "check_coverage.py"
        if not gate.is_file():
            continue
        text = gate.read_text(encoding="utf-8")
        if "OMIT_PARTS" in text and "_directories" not in text:
            out.append(f"{gate.relative_to(root).as_posix()}: substring COVERAGE_LEAK (OMIT_PARTS)")
    return out


def custody_scan_calls(text: str) -> int:
    """How many times ``text`` CALLS ``verify_sources()``.

    Counted on the syntax tree, not the text: until 2026-09-18 this lint
    counted the substring, so a comment naming the call -- the canonical
    ``run.py`` carries one, and ``diagonal_identity`` copied it -- read as a
    second scan.  Raises ``SyntaxError`` if ``text`` does not parse."""
    calls = 0
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.id if isinstance(func, ast.Name) else (
                func.attr if isinstance(func, ast.Attribute) else None)
            if name == "verify_sources":
                calls += 1
    return calls


def run_warnings(root: Path = ROOT) -> list[str]:
    """Trees whose run.py scans custody twice per receipt."""
    out: list[str] = []
    for tree in _tree_dirs(root):
        runner = tree / "run.py"
        if not runner.is_file():
            continue
        rel = runner.relative_to(root).as_posix()
        try:
            n = custody_scan_calls(runner.read_text(encoding="utf-8-sig"))
        except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
            out.append(f"{rel}: cannot be read as Python ({type(exc).__name__}); custody scans not counted")
            continue
        if n > 1:
            out.append(f"{rel}: {n} verify_sources() calls (double custody scan)")
    return out


def python_files(root: Path = ROOT) -> list[Path]:
    """Every ``.py`` file under ``research/``, found by walking.  Hidden
    directories (a Lake package's ``.lake``, a ``.venv``) and ``__pycache__``
    are not entered: they hold build products and vendored copies, not a
    tree's own source."""
    out: list[Path] = []
    for folder, dirs, files in os.walk(root / "research"):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d != "__pycache__")
        out.extend(Path(folder) / name for name in files if name.endswith(".py"))
    return sorted(out)


def digest(path: Path) -> str:
    """SHA-256 of a file's bytes with CRLF read as LF: the committed form,
    whatever the checkout's line-ending conversion did to it."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _static_text(node: ast.AST) -> str | None:
    """The literal text of a string expression, or None if it has none:
    a string constant, a ``+`` chain of them, or the fixed parts of an
    f-string (each interpolation read as ``{}``)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _static_text(node.left), _static_text(node.right)
        if left is not None and right is not None:
            return left + right
        return None
    if isinstance(node, ast.JoinedStr):
        return "".join(
            part.value if isinstance(part, ast.Constant) and isinstance(part.value, str) else "{}"
            for part in node.values
        )
    return None


def _docstrings(tree: ast.Module) -> set[int]:
    """The ids of every docstring node: prose, not a pattern."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            first = node.body[0] if node.body else None
            if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                out.add(id(first.value))
    return out


def quote_excluding_captures(text: str) -> list[int]:
    """Line numbers of every string expression in ``text`` that is an
    axiom-report pattern capturing with a quote-excluding class.

    Raises ``SyntaxError`` if ``text`` does not parse."""
    if "axioms" not in text:
        return []
    tree = ast.parse(text)
    prose = _docstrings(tree)
    lines: set[int] = set()
    for node in ast.walk(tree):
        if id(node) in prose:
            continue
        literal = _static_text(node)
        if literal is None:
            continue
        if any(phrase in literal for phrase in AXIOM_PHRASES) and QUOTE_EXCLUDING_CLASS.search(literal):
            lines.add(getattr(node, "lineno", 0))
    return sorted(lines)


def axiom_capture_findings(
    root: Path = ROOT,
    frozen: dict[str, str] | None = None,
    pending: dict[str, str] | None = None,
) -> tuple[list[str], list[str]]:
    """``(errors, pinned)`` for quote-excluding axiom-report captures.

    ``errors`` names every capture outside the pinned lists, every pinned file
    whose bytes moved, and every pinned file that is gone.  ``pinned`` names
    the captures the two lists excuse, one line per file, so that they are
    reported on every run and never pass silently."""
    frozen = FROZEN_EXCEPTIONS if frozen is None else frozen
    pending = REPAIR_PENDING if pending is None else pending
    errors: list[str] = []
    pinned: list[str] = []
    found: dict[str, list[int]] = {}
    for path in python_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            # utf-8-sig: a byte-order mark is legal at the head of a Python
            # source file and two research files carry one.
            sites = quote_excluding_captures(path.read_text(encoding="utf-8-sig"))
        except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{rel}: cannot be read as Python ({type(exc).__name__}), so it cannot be checked")
            continue
        if sites:
            found[rel] = sites
    for rel, sites in sorted(found.items()):
        where = ",".join(str(n) for n in sites)
        if rel not in frozen and rel not in pending:
            errors.append(
                f"{rel}:{where}: quote-excluding name capture in an axiom-report pattern "
                f"(a primed theorem name is silently dropped); use {FIXED_FORM}"
            )
    for label, table in (("FROZEN_EXCEPTIONS", frozen), ("REPAIR_PENDING", pending)):
        for rel, want in sorted(table.items()):
            path = root / rel
            if not path.is_file():
                errors.append(f"{rel}: named in {label} but absent; drop the entry")
                continue
            have = digest(path)
            if have != want:
                if rel in found:
                    errors.append(
                        f"{rel}: named in {label} but its bytes moved (pinned {want[:12]}, now "
                        f"{have[:12]}) and it still carries the capture at line(s) "
                        f"{','.join(str(n) for n in found[rel])}; repair it, use {FIXED_FORM}"
                    )
                else:
                    errors.append(
                        f"{rel}: named in {label} but its bytes moved (pinned {want[:12]}, now "
                        f"{have[:12]}) and it no longer carries the capture; drop the entry"
                    )
                continue
            if rel not in found:
                errors.append(f"{rel}: named in {label} but its pinned bytes carry no capture; drop the entry")
                continue
            where = ",".join(str(n) for n in found[rel])
            kind = ("frozen by verify_freeze.py; the one permanent exception"
                    if label == "FROZEN_EXCEPTIONS" else "DEFECT, repair pending")
            pinned.append(f"{rel}:{where}: {kind}")
    return errors, pinned


def main(root: Path = ROOT) -> int:
    errors = coverage_errors(root)
    capture_errors, pinned = axiom_capture_findings(root)
    errors += capture_errors
    warnings = run_warnings(root)
    if errors:
        print("ERROR: correctness drift in a research tree (must fix):")
        for line in errors:
            print(f"  {line}")
    if pinned:
        print("PINNED: quote-excluding axiom-report captures, excused only at their pinned bytes"
              " (reported every run; not an accepted house form):")
        for line in pinned:
            print(f"  {line}")
    if warnings:
        print("WARNING: double custody scan (efficiency; fix in a NEW tree before it is pinned):")
        for line in warnings:
            print(f"  {line}")
    if errors:
        print(f"\n{len(errors)} error(s); sync with research/_scaffold/ and the fixed capture {FIXED_FORM}.")
        return 1
    print(f"\nscaffold clean of correctness drift; {len(pinned)} pinned quote-excluding capture file(s), "
          f"{len(warnings)} known double-scan warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
