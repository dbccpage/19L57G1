"""Build the tree's Lean package from clean, scan every .lean file for the
forbidden tokens as text, require every module under lean/SideFree/ to
lie in the root's transitive import closure (a module the root does not
reach is text-scanned but never elaborated, so a type error or a
disallowed axiom in it would go unseen), require every theorem declared
under lean/SideFree/ to carry a ``#print axioms`` line in the root
module, require every axiom report to lie within {propext, Quot.sound}, and
compare the reports with the committed lean/axioms.txt.  ``--regen``
rewrites that log deliberately.  MANUAL RECEIPT: no CI job builds this
package, so its axiom report is unchecked by any gate.  That is a live
residual of this tree, recorded and not closed.

The audit-totality check exists because the log-versus-build comparison
compares only the reports the build happens to emit: a theorem added with no
``#print axioms`` line left every check green while the paper claimed every
theorem carried a report.  Its population is read from the source text with
block and line comments stripped first, so a doc-comment line beginning with
the word for a theorem cannot enter or leave it."""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LEAN = HERE / "lean"
LOG = LEAN / "axioms.txt"
ALLOWED = {"propext", "Quot.sound"}
FORBIDDEN = [
    (re.compile(r"\bsorry\b"), "sorry"),
    (re.compile(r"\badmit\b"), "admit"),
    (re.compile(r"\bunsafe\b"), "unsafe"),
    (re.compile(r"\bpartial\b"), "partial"),
    (
        re.compile(
            r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected)\s+)?axiom\s"
        ),
        "axiom",
    ),
]
IMPORT = re.compile(r"^import\s+(SideFree(?:\.\w+)*)\s*$", re.M)
ROOT_MODULE = LEAN / "SideFree.lean"
BLOCK_COMMENT = re.compile(r"/-.*?-/", re.S)
LINE_COMMENT = re.compile(r"--[^\n]*")
IDENT = r"[A-Za-z_][A-Za-z0-9_'!?]*"
THEOREM = re.compile(rf"^\s*(?:(?:private|protected)\s+)?theorem\s+({IDENT})")
NAMESPACE = re.compile(rf"^namespace\s+({IDENT}(?:\.{IDENT})*)\s*$")
END_NAMESPACE = re.compile(rf"^end\s+({IDENT}(?:\.{IDENT})*)\s*$")
PRINT_AXIOMS = re.compile(r"^#print\s+axioms\s+(\S+)\s*$", re.M)
REPORT = re.compile(
    r"'(?P<name>[^']+)' "
    r"(?:depends on axioms: \[(?P<axioms>[^\]]*)\]|does not depend on any axioms)$"
)


def scan_sources() -> list[str]:
    problems: list[str] = []
    for path in sorted(LEAN.rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pat, word in FORBIDDEN:
                if pat.search(line):
                    problems.append(f"{path.relative_to(HERE)}:{lineno}: forbidden token {word}")
    return problems


def module_census() -> list[str]:
    """Every module under lean/SideFree/, by dotted name."""
    base = LEAN / "SideFree"
    return sorted(
        ".".join(("SideFree", *path.relative_to(base).with_suffix("").parts))
        for path in base.rglob("*.lean")
    )


def import_closure() -> set[str]:
    """The root's transitive imports, read from the source text."""
    seen: set[str] = set()
    todo = [ROOT_MODULE]
    while todo:
        path = todo.pop()
        for name in IMPORT.findall(path.read_text(encoding="utf-8")):
            if name not in seen:
                seen.add(name)
                todo.append(LEAN / (name.replace(".", "/") + ".lean"))
    return seen


def unreached_modules() -> list[str]:
    """Modules the root never elaborates; each is a hole in the audit."""
    reached = import_closure()
    return [name for name in module_census() if name not in reached]


def strip_comments(text: str) -> str:
    """Block comments first, then line comments; doc text is not source."""
    return LINE_COMMENT.sub("", BLOCK_COMMENT.sub("", text))


def declared_theorems() -> list[str]:
    """Every theorem declared under lean/SideFree/, fully qualified.

    Namespaces are tracked so the names match the root module's citations.
    """
    out: list[str] = []
    base = LEAN / "SideFree"
    for path in sorted(base.rglob("*.lean")):
        stack: list[str] = []
        for line in strip_comments(path.read_text(encoding="utf-8")).splitlines():
            opened = NAMESPACE.match(line)
            if opened:
                stack.append(opened.group(1))
                continue
            closed = END_NAMESPACE.match(line)
            if closed and stack and stack[-1] == closed.group(1):
                stack.pop()
                continue
            declared = THEOREM.match(line)
            if declared:
                out.append(".".join([*stack, declared.group(1)]))
    return sorted(out)


def audited_theorems() -> list[str]:
    """Every name the root module asks for a ``#print axioms`` report on."""
    return sorted(PRINT_AXIOMS.findall(ROOT_MODULE.read_text(encoding="utf-8")))


def unaudited_theorems() -> list[str]:
    """Declared theorems the root module never asks for a report on."""
    audited = set(audited_theorems())
    return [name for name in declared_theorems() if name not in audited]


def echo(text: str) -> None:
    """Print build output that a console encoding may not carry.

    Lake writes non-ASCII progress marks, and on a console whose encoding
    cannot represent them a plain ``print`` raises instead of showing the
    failure it was called to show.  That happened, so the diagnostic is made
    unconditionally printable rather than left to the terminal.
    """
    print(text.encode("ascii", "replace").decode("ascii"))


def build() -> str:
    clean = subprocess.run(
        ["lake", "clean"],
        cwd=LEAN,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if clean.returncode != 0:
        echo(clean.stdout)
        echo(clean.stderr)
        raise SystemExit("FAIL: lake clean failed; refusing a non-clean verification")
    proc = subprocess.run(
        ["lake", "build"], cwd=LEAN, capture_output=True, text=True, encoding="utf-8"
    )
    if proc.returncode != 0:
        echo(proc.stdout)
        echo(proc.stderr)
        raise SystemExit("FAIL: lake build failed")
    return proc.stdout + proc.stderr


def reports(log: str) -> list[str]:
    out: list[str] = []
    for raw in log.splitlines():
        m = REPORT.search(raw.strip())
        if m:
            out.append(m.group(0))
    return sorted(out)


def main(argv: list[str]) -> int:
    problems = scan_sources()
    problems.extend(
        f"{name} is outside the root's import closure and is never elaborated"
        for name in unreached_modules()
    )
    problems.extend(
        f"{name} is declared under lean/SideFree/ but has no "
        f"#print axioms line in {ROOT_MODULE.name}"
        for name in unaudited_theorems()
    )
    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        return 1
    found = reports(build())
    if not found:
        print("FAIL: no axiom reports in the build log")
        return 1
    for line in found:
        m = REPORT.search(line)
        assert m is not None
        axioms = {a.strip() for a in (m.group("axioms") or "").split(",") if a.strip()}
        if not axioms <= ALLOWED:
            print(f"FAIL: disallowed axioms {sorted(axioms - ALLOWED)} in {m.group('name')}")
            return 1
    text = "\n".join(found) + "\n"
    if "--regen" in argv:
        LOG.write_bytes(text.encode("utf-8"))
        print(f"wrote {LOG.relative_to(HERE)}: {len(found)} reports")
        return 0
    if not LOG.exists():
        print("FAIL: lean/axioms.txt missing; run with --regen deliberately")
        return 1
    if LOG.read_bytes() != text.encode("utf-8"):
        print("FAIL: axiom reports differ between the fresh build and lean/axioms.txt")
        return 1
    print(f"lean ok: {len(found)} axiom reports within {sorted(ALLOWED)}, matching lean/axioms.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
