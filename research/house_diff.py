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
all eight copies share.  It reports drift, not correctness.

    python research/house_diff.py            # the report
    python research/house_diff.py --logic    # only the divergences in logic
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOUSE_FILES = ("verify_sources.py", "verify_lean.py", "run.py", "verify.py",
               "tests/test_sources.py")


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


def normalise(node: ast.AST) -> str:
    """A function's shape, with its literals and its docstring removed."""
    copied = ast.parse(ast.unparse(node))
    body = copied.body[0]
    if isinstance(body, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        first = body.body[0] if body.body else None
        if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            body.body = body.body[1:] or [ast.Pass()]
    return ast.dump(Blank().visit(copied))


def definitions(path: Path) -> dict[str, str]:
    """Every top-level function and class of a file, by name, normalised."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logic", action="store_true",
                        help="report only the definitions whose logic differs")
    args = parser.parse_args(argv)
    return report(args.logic)


if __name__ == "__main__":
    raise SystemExit(main())
