"""Clean-build and total-inventory verifier for the independent Lean package."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
LEAN = HERE / "lean"
ROOT = LEAN / "TypedTranslation.lean"
AXIOMS = LEAN / "axioms.txt"
ALLOWED = {"propext", "Quot.sound"}
FORBIDDEN = (
    (re.compile(r"\bsorry\b"), "sorry"),
    (re.compile(r"\badmit\b"), "admit"),
    (re.compile(r"\bunsafe\b"), "unsafe"),
    (re.compile(r"\bpartial\b"), "partial"),
    (re.compile(r"^\s*axiom\s"), "axiom"),
)
IDENT = r"[A-Za-z_][A-Za-z0-9_'!?]*"
THEOREM = re.compile(rf"^\s*theorem\s+({IDENT}(?:\.{IDENT})*)")
NAMESPACE = re.compile(rf"^namespace\s+({IDENT}(?:\.{IDENT})*)\s*$")
END_NAMESPACE = re.compile(rf"^end\s+({IDENT}(?:\.{IDENT})*)\s*$")
IMPORT = re.compile(r"^import\s+(TypedTranslation(?:\.\w+)*)\s*$", re.M)
PRINT = re.compile(r"^#print\s+axioms\s+(\S+)\s*$", re.M)
REPORT = re.compile(
    r"'(?P<name>.+?)' "
    r"(?:depends on axioms: \[(?P<axioms>[^\]]*)\]|does not depend on any axioms)$"
)
BLOCK_COMMENT = re.compile(r"/-.*?-/", re.S)
LINE_COMMENT = re.compile(r"--[^\n]*")


def strip_comments(text: str) -> str:
    return LINE_COMMENT.sub("", BLOCK_COMMENT.sub("", text))


def source_files() -> list[Path]:
    return sorted(path for path in LEAN.rglob("*.lean") if ".lake" not in path.parts)


def scan_sources() -> list[str]:
    problems: list[str] = []
    for path in source_files():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pattern, word in FORBIDDEN:
                if pattern.search(line):
                    problems.append(
                        f"{path.relative_to(HERE)}:{line_number}: forbidden token {word}"
                    )
    return problems


def module_census() -> set[str]:
    base = LEAN / "TypedTranslation"
    return {
        ".".join(("TypedTranslation", *path.relative_to(base).with_suffix("").parts))
        for path in base.rglob("*.lean")
    }


def import_closure() -> set[str]:
    seen: set[str] = set()
    todo = [ROOT]
    while todo:
        path = todo.pop()
        for name in IMPORT.findall(path.read_text(encoding="utf-8")):
            if name not in seen:
                seen.add(name)
                todo.append(LEAN / (name.replace(".", "/") + ".lean"))
    return seen


def declared_theorems() -> list[str]:
    result: list[str] = []
    for path in sorted((LEAN / "TypedTranslation").rglob("*.lean")):
        namespaces: list[str] = []
        for line in strip_comments(path.read_text(encoding="utf-8")).splitlines():
            opened = NAMESPACE.match(line)
            if opened:
                namespaces.append(opened.group(1))
                continue
            closed = END_NAMESPACE.match(line)
            if closed and namespaces and namespaces[-1] == closed.group(1):
                namespaces.pop()
                continue
            theorem = THEOREM.match(line)
            if theorem:
                result.append(".".join([*namespaces, theorem.group(1)]))
    return sorted(result)


def audited_theorems() -> list[str]:
    return sorted(PRINT.findall(ROOT.read_text(encoding="utf-8")))


def build() -> str:
    clean = subprocess.run(
        ["lake", "clean"], cwd=LEAN, capture_output=True, text=True, encoding="utf-8"
    )
    if clean.returncode != 0:
        raise RuntimeError(f"lake clean failed\n{clean.stdout}\n{clean.stderr}")
    built = subprocess.run(
        ["lake", "build"], cwd=LEAN, capture_output=True, text=True, encoding="utf-8"
    )
    if built.returncode != 0:
        raise RuntimeError(f"lake build failed\n{built.stdout}\n{built.stderr}")
    return built.stdout + built.stderr


def reports(log: str) -> list[str]:
    return sorted(
        match.group(0)
        for line in log.splitlines()
        if (match := REPORT.search(line.strip())) is not None
    )


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if any(arg not in {"--regen"} for arg in argv):
        print(f"FAIL: unknown arguments: {' '.join(argv)}")
        return 1
    problems = scan_sources()
    missing_modules = sorted(module_census() - import_closure())
    problems.extend(f"{name} is outside the root import closure" for name in missing_modules)
    declared = declared_theorems()
    audited = audited_theorems()
    if Counter(declared) != Counter(audited):
        problems.append(f"theorem inventory differs: declared {declared}, audited {audited}")
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        return 1
    try:
        log = build()
    except RuntimeError as exc:
        print(f"FAIL: {str(exc).encode('ascii', 'replace').decode('ascii')}")
        return 1
    found = reports(log)
    names = [REPORT.search(line).group("name") for line in found if REPORT.search(line)]
    if Counter(names) != Counter(audited):
        print(f"FAIL: build reports differ from requested inventory: {names}")
        return 1
    for line in found:
        match = REPORT.search(line)
        assert match is not None
        used = {name.strip() for name in (match.group("axioms") or "").split(",") if name.strip()}
        if not used <= ALLOWED:
            print(f"FAIL: {match.group('name')} uses {sorted(used - ALLOWED)}")
            return 1
    expected = ("\n".join(found) + "\n").encode("utf-8")
    if "--regen" in argv:
        AXIOMS.write_bytes(expected)
        print(f"wrote lean/axioms.txt: {len(found)} reports")
        return 0
    if not AXIOMS.is_file() or AXIOMS.read_bytes() != expected:
        print("FAIL: fresh reports differ from lean/axioms.txt")
        return 1
    print(
        f"lean ok: {len(module_census())} modules, {len(found)} theorem reports "
        f"within {sorted(ALLOWED)}, byte-identical inventory"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
