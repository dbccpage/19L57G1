"""Build this rung's self-contained Lean package and audit it.

Five checks, none implying the others:

* no forbidden token in any committed ``.lean`` source of this package,
  matched at word boundaries exactly as the root gate ``ci/check_lean_audit.py``
  matches them, comments and doc strings included;
* every ``#print axioms`` report of a FRESH build lies within the whitelist
  ``{propext, Quot.sound}``;
* the set of reported names equals the set listed in ``AxiomReport.lean``,
  in both directions;
* every theorem DECLARED in any module of the package is listed in
  ``AxiomReport.lean`` -- dropping a line from that file drops its report
  too, so the previous check alone cannot see a silent removal;
* the COMMITTED log ``receipts/lean_axioms.txt`` matches the fresh build
  exactly, line for line.

The seed requires each rung's axiom log to be committed and checked
against a fresh build rather than left as a manual receipt.  No CI gate
runs this file: it needs elan, which the research job deliberately does
not install, so this remains a manual receipt for the BUILD while the
committed log makes the RESULT reviewable without one.

``--regen`` rewrites the committed log from a fresh build and verifies
nothing.  It is a deliberate act and must never be run while an injection
is live: regenerating under one adopts the defect as the baseline.

Exit 0 on success, 1 with a named failure otherwise.  AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
LEAN = HERE / "lean"
LOG = HERE / "receipts" / "lean_axioms.txt"
REPORT = LEAN / "SecondNoFirst" / "AxiomReport.lean"

# Word-boundary patterns, mirroring the root gate exactly.  Assembled from
# fragments so this file does not trip its own scan, and so that the estate's
# own word "admitted" -- which the root gate allows, because the root gate is
# the bare verb -- is not flagged by a substring test.
FORBIDDEN = (
    r"\bso" + r"rry\b",
    r"\bad" + r"mit\b",
    r"\buns" + r"afe\b",
    r"\bpar" + r"tial\b",
    r"\bnative_" + r"decide\b",
)
LEADING_AXIOM = re.compile(r"^\s*ax" + r"iom\s", re.MULTILINE)
WHITELIST = {"propext", "Quot.sound"}

# The module census is DERIVED, not hand-maintained: every `.lean` file of
# the library except the report module itself, with its namespace prefix
# parsed from its own `namespace` lines.  A hand list is a second place to
# forget a module, and the root repository records exactly that defect for
# its own parked-module census.
REPORT_MODULE = "AxiomReport.lean"


def sources() -> list[Path]:
    found = sorted(LEAN.rglob("*.lean"))
    return [s for s in found if ".lake" not in s.parts]


def token_scan() -> list[str]:
    failures: list[str] = []
    for src in sources():
        text = src.read_text("utf-8")
        for pattern in FORBIDDEN:
            hit = re.search(pattern, text)
            if hit is not None:
                failures.append(
                    f"FAIL: {src.name} contains forbidden token {hit.group(0)!r}"
                )
        if LEADING_AXIOM.search(text):
            failures.append(
                f"FAIL: {src.name} contains a leading ax" + "iom declaration"
            )
    return failures


def build() -> tuple[int, str]:
    # Force re-elaboration of the report module: a cached build emits no
    # reports, and an audit of an empty log proves nothing.
    REPORT.touch()
    proc = subprocess.run(
        ["lake", "build"], capture_output=True, text=True, cwd=LEAN, check=False
    )
    return proc.returncode, proc.stdout + proc.stderr


def parse(log: str) -> tuple[dict[str, tuple[str, ...]], int]:
    """Every report of the build log, as name -> sorted axioms.

    ``.+?`` and not ``[^']*?``: a primed theorem name ends in a quote
    character, and the character-class pattern silently drops it -- the
    recorded primed-names parser defect.
    """
    reports: dict[str, tuple[str, ...]] = {}
    free = 0
    for name in re.findall(r"'(.+?)' does not depend on any axioms", log):
        reports[name] = ()
        free += 1
    for name, axes in re.findall(r"'(.+?)' depends on axioms: \[([^\]]*)\]", log):
        reports[name] = tuple(sorted(a.strip() for a in axes.split(",") if a.strip()))
    return reports, free


def render(reports: dict[str, tuple[str, ...]]) -> str:
    lines = [
        f"{name} :: {' '.join(axes) if axes else 'none'}"
        for name, axes in sorted(reports.items())
    ]
    return "\n".join(lines) + "\n"


def listed() -> set[str]:
    return set(re.findall(r"#print axioms ([\w'.]+)", REPORT.read_text("utf-8")))


def modules() -> list[Path]:
    """Every source module of the library, the report module excluded."""
    found = sorted((LEAN / "SecondNoFirst").glob("*.lean"))
    return [m for m in found if m.name != REPORT_MODULE]


def namespace_of(path: Path) -> str:
    """The qualified namespace a module's declarations land in, parsed from
    the module's own `namespace` lines rather than from a table."""
    parts = re.findall(r"^namespace\s+([\w'.]+)", path.read_text("utf-8"), re.M)
    if not parts:
        raise ValueError(f"{path.name} declares no namespace")
    return ".".join(parts) + "."


def declared() -> dict[str, str]:
    """Every theorem declared in any module of this package, qualified."""
    out: dict[str, str] = {}
    for path in modules():
        prefix = namespace_of(path)
        text = path.read_text("utf-8")
        for name in re.findall(r"^theorem ([A-Za-z_][\w'.]*)", text, re.M):
            out[prefix + name] = path.name
    return out


def audit(regen: bool) -> int:
    failures = token_scan()
    for line in failures:
        print(line)
    code, log = build()
    if code != 0:
        print("FAIL: lake build exited nonzero")
        print(log[-2000:])
        return 1
    reports, free = parse(log)
    if not reports:
        print("FAIL: the build produced no axiom report; nothing was audited")
        return 1
    fresh = render(reports)
    if regen:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        LOG.write_bytes(fresh.encode("utf-8"))
        print(f"regenerated {LOG.name}: {len(reports)} reports")
        return 0
    for name, axes in sorted(reports.items()):
        extra = set(axes) - WHITELIST
        if extra:
            print(f"FAIL: {name} depends on disallowed axioms {sorted(extra)}")
            failures.append(name)
    want = listed()
    got = set(reports)
    for name in sorted(want - got):
        print(f"FAIL: {name} is listed in AxiomReport.lean but not reported")
        failures.append(name)
    for name in sorted(got - want):
        print(f"FAIL: {name} is reported but not listed in AxiomReport.lean")
        failures.append(name)
    for name, module in sorted(declared().items()):
        if name not in want:
            print(
                f"FAIL: {name} is declared in {module} but not listed in"
                " AxiomReport.lean"
            )
            failures.append(name)
    if not LOG.exists():
        print(f"FAIL: the committed axiom log {LOG.name} is missing")
        return 1
    committed = LOG.read_bytes()
    if b"\r" in committed:
        print(f"FAIL: {LOG.name} contains CR bytes; it is committed as -text")
        failures.append(LOG.name)
    if committed.decode("utf-8") != fresh:
        want_lines = set(committed.decode("utf-8").splitlines())
        got_lines = set(fresh.splitlines())
        for line in sorted(want_lines - got_lines):
            print(f"FAIL: committed log has a report the fresh build does not: {line}")
        for line in sorted(got_lines - want_lines):
            print(f"FAIL: fresh build has a report the committed log does not: {line}")
        failures.append(LOG.name)
    if failures:
        return 1
    print(
        f"lean audit clean: {len(sources())} sources, {len(reports)} axiom"
        f" reports ({free} axiom-free), axioms within {sorted(WHITELIST)},"
        f" {len(declared())} declared theorems across {len(modules())}"
        f" modules all listed,"
        f" committed log matches the fresh build"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit this rung's Lean package.")
    parser.add_argument(
        "--regen",
        action="store_true",
        help="rewrite the committed axiom log from a fresh build; verifies nothing",
    )
    args = parser.parse_args()
    return audit(args.regen)


if __name__ == "__main__":
    raise SystemExit(main())
