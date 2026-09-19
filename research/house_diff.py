"""Compare the house files across the research trees, by logic and not by text.

AuthorityEffect: None.  This tool reads; it changes nothing, pins nothing and
verifies nothing.  A clean report is not a receipt.

**Why this and not a shared module.**  Eight trees carry a hand copy of
``verify_sources.py``, ``verify_lean.py``, ``run.py``, ``verify.py`` and
``tests/test_sources.py``, differing in their constants; the same
runtime-origin gap and the same ``sys.path`` ordering defect were fixed three
times.  The obvious repair is a shared custody module.  It was declined, and
the reason is the point: a shared guard is a **single point of trust for eight
independent pins**.  Each tree's ``verify_sources.py`` pins a different
baseline commit, and a change that bent one tree's guard would silently bend
all eight.  The isolation is what the copies buy.

What is wanted instead is visibility: when the copies drift, say **where**,
and say whether the drift is a constant (expected — every tree pins its own
baseline, names its own schema, censuses its own modules) or *logic* (a
divergence to look at, and possibly a fix that landed in one tree and not the
others).

The comparison is therefore structural.  Each file is parsed, its top-level
functions extracted, and every literal — every string, number, boolean —
replaced by a placeholder before the bodies are compared.  Two trees agree on
a function when their normalised syntax trees are equal.  A function present
in some trees and absent in others is reported as such; docstrings are
compared separately from code, so a reworded comment is never reported as a
divergence in logic.

What this does **not** do: judge which version is right, and notice a defect
all eight copies share.  It reports drift, not correctness.  Nor can it see a
defect carried INSIDE a literal -- a regex that captures a theorem name with a
quote-excluding class is blanked like any other string.  That one is read by
``research/_scaffold/check_scaffold.py``, which reads the literals.

**Verifier families** (``--families``, added 2026-09-18).  The house report
above reads only the trees that carry ``verify_sources.py``.  Five verifier
files were copied more widely than that -- ``verify_sources.py``,
``verify_lean.py``, ``verify_pins.py``, ``test_forbidden.py`` and
``check_coverage.py`` -- and for each of them this mode reads EVERY copy under
``research/``, wherever it sits (``diagonal_identity`` keeps its
``test_forbidden.py`` under ``tests/``; ``research/_scaffold/`` holds the
copy-source of ``check_coverage.py``).  Per family it reports:

* the groups of byte-identical copies (CRLF read as LF, the committed form);
* the logic variants: copies grouped by their top-level definitions, each
  normalised as above.  Module-level statements are set aside, as in the house
  report: they are where a tree keeps its constants;
* for every variant but the most common, a compact summary against the most
  common one -- the definitions it adds, the ones it lacks, and the ones whose
  normalised body differs, with the number of normalised lines added and
  removed.  When variants tie for most common, the tie is said and the first
  by path is the reference.

Divergence is REPORTED, never failed: the copies differ on purpose, each pins
its own inputs, and the author declined both a shared helper and collapsing
the copies.  A copy that cannot be parsed is named, not silently dropped.

    python research/house_diff.py            # the report
    python research/house_diff.py --logic    # only the divergences in logic
    python research/house_diff.py --families # every copy of the five verifier files
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOUSE_FILES = ("verify_sources.py", "verify_lean.py", "run.py", "verify.py",
               "tests/test_sources.py")
FAMILIES = ("verify_sources.py", "verify_lean.py", "verify_pins.py",
            "test_forbidden.py", "check_coverage.py")
# How many definition names one summary clause prints before counting the rest.
SHOWN = 6


def trees() -> list[str]:
    """The trees carrying the house shape, found rather than listed: a tree is
    one with its own ``verify_sources.py``."""
    return sorted(path.parent.name for path in ROOT.glob("*/verify_sources.py"))


class Blank(ast.NodeTransformer):
    """Replace every literal with a placeholder, so that a tree's own
    constants — its baseline commit, its schema name, its module census — do
    not read as a difference in logic."""

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        return ast.copy_location(ast.Constant(value="<literal>"), node)


def _blanked(node: ast.AST) -> ast.AST:
    """One definition, reparsed, with its docstring removed and its literals
    blanked."""
    copied = ast.parse(ast.unparse(node))
    body = copied.body[0]
    if isinstance(body, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        first = body.body[0] if body.body else None
        if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            body.body = body.body[1:] or [ast.Pass()]
    blanked: ast.AST = Blank().visit(copied)
    return blanked


def normalise(node: ast.AST) -> str:
    """A function's shape, with its literals and its docstring removed."""
    return ast.dump(_blanked(node))


def normalised_source(node: ast.AST) -> str:
    """The same normalised definition as source text, for counting lines."""
    return ast.unparse(_blanked(node))


def _parse(path: Path) -> ast.Module | None:
    """A file's syntax tree, or None if it cannot be read or parsed.

    Read as ``utf-8-sig``: a byte-order mark is legal at the head of a Python
    source file, and until 2026-09-18 this tool read it as a character, failed
    to parse, and dropped the copy without a word."""
    try:
        return ast.parse(path.read_text(encoding="utf-8-sig"))
    except (OSError, SyntaxError, UnicodeDecodeError, ValueError):
        return None


def definitions(path: Path) -> dict[str, str]:
    """Every top-level function and class of a file, by name, normalised."""
    tree = _parse(path)
    if tree is None:
        return {}
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[node.name] = normalise(node)
    return out


def compare(relative: str) -> list[tuple[str, dict[str, list[str]], list[str]]]:
    """For one house file: per definition, which trees agree with which, and
    which trees do not carry it at all."""
    present = {name: definitions(ROOT / name / relative) for name in trees()}
    carriers = [name for name, defs in present.items() if defs]
    everything = sorted({key for defs in present.values() for key in defs})
    rows: list[tuple[str, dict[str, list[str]], list[str]]] = []
    for key in everything:
        groups: dict[str, list[str]] = {}
        missing: list[str] = []
        for name in carriers:
            shape = present[name].get(key)
            if shape is None:
                missing.append(name)
            else:
                groups.setdefault(shape, []).append(name)
        rows.append((key, groups, missing))
    return rows


def report(logic_only: bool) -> int:
    found = 0
    for relative in HOUSE_FILES:
        rows = compare(relative)
        carriers = [name for name in trees() if (ROOT / name / relative).is_file()]
        if not rows:
            continue
        header = f"== {relative}  ({len(carriers)} trees carry it)"
        printed_header = False
        for key, groups, missing in rows:
            diverges = len(groups) > 1
            if logic_only and not diverges:
                continue
            if not printed_header:
                print(header)
                printed_header = True
            if diverges:
                found += 1
                print(f"  LOGIC DIFFERS: {key}")
                for index, members in enumerate(sorted(groups.values(), key=len, reverse=True)):
                    print(f"      shape {index + 1}: {', '.join(sorted(members))}")
            elif not logic_only:
                where = "all" if not missing else f"{len(groups[next(iter(groups))])} of {len(carriers)}"
                print(f"  agrees ({where}): {key}")
            if missing and not logic_only:
                print(f"      absent from: {', '.join(sorted(missing))}")
        if printed_header:
            print()
    print(f"{found} definition(s) differ in logic across the trees that carry them.")
    print("A difference is not a defect: read it, and decide whether a fix landed in one "
          "tree and not the others.")
    return 0


# --- verifier families ------------------------------------------------------


def family_copies(name: str, root: Path = ROOT) -> list[Path]:
    """Every file called ``name`` under ``root`` (the research directory), at
    any depth.  Hidden directories (a Lake package's ``.lake``, a ``.venv``)
    and ``__pycache__`` are not entered: they hold build products and
    vendored copies, not a tree's own source."""
    out: list[Path] = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d != "__pycache__")
        if name in files:
            out.append(Path(folder) / name)
    return sorted(out, key=lambda path: path.relative_to(root).as_posix())


def label(path: Path, root: Path = ROOT) -> str:
    """Where a copy sits, by its directory under ``root``: ``balance_carrier``,
    ``diagonal_identity/tests``, ``_scaffold``."""
    return path.parent.relative_to(root).as_posix()


def byte_digest(path: Path) -> str:
    """SHA-256 of a copy's bytes with CRLF read as LF."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


@dataclass(frozen=True)
class Variant:
    """Copies whose top-level definitions agree in logic."""

    members: tuple[str, ...]
    shapes: tuple[tuple[str, str], ...]
    sources: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Family:
    """What one family's copies look like, byte by byte and in logic."""

    name: str
    copies: tuple[str, ...]
    byte_groups: tuple[tuple[str, ...], ...]
    variants: tuple[Variant, ...]
    unparsable: tuple[str, ...]


def family(name: str, root: Path = ROOT) -> Family:
    """Group every copy of ``name`` by bytes and by logic.

    Byte groups and variants are ordered largest first, ties by first member,
    so the first variant is the most common one and the order is stable."""
    paths = family_copies(name, root)
    by_bytes: dict[str, list[str]] = {}
    by_logic: dict[tuple[tuple[str, str], ...], list[str]] = {}
    sources: dict[tuple[tuple[str, str], ...], tuple[tuple[str, str], ...]] = {}
    unparsable: list[str] = []
    for path in paths:
        where = label(path, root)
        by_bytes.setdefault(byte_digest(path), []).append(where)
        tree = _parse(path)
        if tree is None:
            unparsable.append(where)
            continue
        nodes = sorted(
            (node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))),
            key=lambda node: node.name,
        )
        key = tuple((node.name, normalise(node)) for node in nodes)
        by_logic.setdefault(key, []).append(where)
        sources.setdefault(key, tuple((node.name, normalised_source(node)) for node in nodes))

    def order(group: list[str]) -> tuple[int, str]:
        return (-len(group), group[0])

    return Family(
        name=name,
        copies=tuple(label(path, root) for path in paths),
        byte_groups=tuple(tuple(group) for group in sorted(by_bytes.values(), key=order)),
        variants=tuple(
            Variant(tuple(members), key, sources[key])
            for key, members in sorted(by_logic.items(), key=lambda item: order(item[1]))
        ),
        unparsable=tuple(unparsable),
    )


def _names(names: list[str]) -> str:
    shown = ", ".join(names[:SHOWN])
    rest = len(names) - SHOWN
    return shown + (f", +{rest} more" if rest > 0 else "")


def _line_delta(reference: str, other: str) -> tuple[int, int]:
    """Normalised lines added and removed going from ``reference`` to ``other``."""
    added = removed = 0
    for line in difflib.unified_diff(reference.splitlines(), other.splitlines(),
                                     lineterm="", n=0):
        if line.startswith(("+++", "---", "@@")):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            removed += 1
    return added, removed


def summary(variant: Variant, reference: Variant) -> str:
    """What ``variant`` changes against ``reference``, in one line."""
    ours, theirs = dict(variant.shapes), dict(reference.shapes)
    ours_src, theirs_src = dict(variant.sources), dict(reference.sources)
    extra = sorted(set(ours) - set(theirs))
    missing = sorted(set(theirs) - set(ours))
    changed = sorted(key for key in set(ours) & set(theirs) if ours[key] != theirs[key])
    parts: list[str] = []
    if extra:
        parts.append(f"adds {len(extra)} ({_names(extra)})")
    if missing:
        parts.append(f"lacks {len(missing)} ({_names(missing)})")
    if changed:
        deltas = []
        for key in changed:
            added, removed = _line_delta(theirs_src[key], ours_src[key])
            deltas.append(f"{key} +{added}/-{removed}")
        parts.append(f"changes {len(changed)} ({_names(deltas)})")
    return "; ".join(parts) if parts else "no difference in top-level definitions"


def family_report(root: Path = ROOT) -> int:
    """Print every family's byte groups and logic variants.  Always 0: the
    copies differ on purpose, so drift is reported and never failed."""
    total_copies = total_variants = 0
    for name in FAMILIES:
        found = family(name, root)
        total_copies += len(found.copies)
        total_variants += len(found.variants)
        print(f"== {name}: {len(found.copies)} copies")
        same = [group for group in found.byte_groups if len(group) > 1]
        if same:
            for group in same:
                print(f"  byte-identical ({len(group)}): {', '.join(group)}")
            singles = sum(1 for group in found.byte_groups if len(group) == 1)
            print(f"  byte-unique: {singles}")
        elif found.copies:
            print(f"  byte-identical groups: none; all {len(found.copies)} copies differ in their bytes")
        for where in found.unparsable:
            print(f"  UNPARSABLE, logic not compared: {where}")
        if not found.variants:
            print()
            continue
        sizes = [len(variant.members) for variant in found.variants]
        tied = sizes.count(sizes[0]) - 1
        tie = (f"; tied with {tied} other variant(s) of {sizes[0]} cop"
               f"{'y' if sizes[0] == 1 else 'ies'}, so the first by path is the reference"
               if tied else "")
        print(f"  logic variants: {len(found.variants)}{tie}")
        reference = found.variants[0]
        for index, variant in enumerate(found.variants, start=1):
            role = " (most common: the reference)" if index == 1 else ""
            print(f"  variant {index}{role}, {len(variant.members)} cop"
                  f"{'y' if len(variant.members) == 1 else 'ies'}: {', '.join(variant.members)}")
            if index > 1:
                print(f"      vs variant 1: {summary(variant, reference)}")
        print()
    print(f"{total_copies} copies in {len(FAMILIES)} verifier families, "
          f"{total_variants} logic variant(s).")
    print("Divergence is reported, not failed: the copies differ on purpose. Read a variant "
          "against the reference and decide whether a fix landed in one copy and not the others.")
    print("Literals are blanked here, so a defect inside a regex does not show: "
          "research/_scaffold/check_scaffold.py reads the literals.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logic", action="store_true",
                        help="report only the definitions whose logic differs")
    parser.add_argument("--families", action="store_true",
                        help="report every copy of the five verifier files, "
                             "by bytes and by logic")
    args = parser.parse_args(argv)
    if args.families:
        return family_report()
    return report(args.logic)


if __name__ == "__main__":
    raise SystemExit(main())
