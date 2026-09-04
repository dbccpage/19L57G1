"""Build the tree's Lean package from clean, scan every .lean file for the
forbidden tokens as text, require every axiom report to lie within
{propext, Quot.sound}, and compare the reports with the committed
lean/axioms.txt.  ``--regen`` rewrites that log deliberately.  Manual
receipt: the research job does not build Lean."""

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
    (re.compile(r"^\s*axiom\s"), "axiom"),
]
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


def build() -> str:
    subprocess.run(["lake", "clean"], cwd=LEAN, capture_output=True)
    proc = subprocess.run(
        ["lake", "build"], cwd=LEAN, capture_output=True, text=True, encoding="utf-8"
    )
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
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
