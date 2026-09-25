"""Build the self-contained Lean package and audit it: no forbidden
token in any committed `.lean` source, every `#print axioms` report
within the whitelist `{propext, Quot.sound}`, every theorem named
in `AxiomReport.lean` reported, and every theorem the package's modules
declare named in `AxiomReport.lean`.  Exit 0 on success, 1 with a named
failure otherwise.  AuthorityEffect: None.

2026-09-24: this docstring used to say "A manual receipt: no CI gate
runs this file."  That is withdrawn.  The `lean` job of
`.github/workflows/verify.yml` runs this file, locally through
`ci/run_gates.py`.  The source census was added in the same change: the
two diffs against `AxiomReport.lean` compare that list with the reports
it generates, so a line dropped from the list dropped its report too and
neither diff could see it.
"""

from __future__ import annotations

import sys
import re
import subprocess
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
LEAN = HERE / "lean"

# Assembled from fragments so this scan does not trip itself.
FORBIDDEN = ["so" + "rry", "ad" + "mit", "uns" + "afe", "par" + "tial", "native_" + "decide"]
LEADING_AXIOM = re.compile(r"^\s*ax" + r"iom\s", re.MULTILINE)
WHITELIST = {"propext", "Quot.sound"}

IDENT = r"[A-Za-z_][A-Za-z0-9_'!?]*"
THEOREM = re.compile(rf"^\s*(?:(?:private|protected)\s+)?theorem\s+({IDENT}(?:\.{IDENT})*)")
NAMESPACE = re.compile(rf"^namespace\s+({IDENT}(?:\.{IDENT})*)\s*$")
END_NAMESPACE = re.compile(rf"^end\s+({IDENT}(?:\.{IDENT})*)\s*$")
BLOCK_COMMENT = re.compile(r"/-.*?-/", re.S)
LINE_COMMENT = re.compile(r"--[^\n]*")


def declared_theorems(paths: list[Path]) -> dict[str, str]:
    """Theorem name -> declaring file, read from source, comments stripped.

    Namespaces are tracked so the names match `AxiomReport.lean`.  The
    population comes from the modules, not from the list it is checked
    against.
    """
    found: dict[str, str] = {}
    for path in paths:
        text = path.read_text("utf-8")
        stack: list[str] = []
        for line in LINE_COMMENT.sub("", BLOCK_COMMENT.sub("", text)).splitlines():
            opened = NAMESPACE.match(line)
            if opened:
                stack.append(opened.group(1))
                continue
            closed = END_NAMESPACE.match(line)
            if closed and stack and stack[-1] == closed.group(1):
                stack.pop()
                continue
            theorem = THEOREM.match(line)
            if theorem:
                found[".".join([*stack, theorem.group(1)])] = path.name
    return found


def main() -> int:
    failures = 0
    sources = sorted(LEAN.rglob("*.lean"))
    sources = [s for s in sources if ".lake" not in s.parts]
    for src in sources:
        text = src.read_text("utf-8")
        for token in FORBIDDEN:
            if token in text:
                print(f"FAIL: {src.name} contains forbidden token {token}")
                failures += 1
        if LEADING_AXIOM.search(text):
            print(f"FAIL: {src.name} contains a leading ax" + "iom declaration")
            failures += 1
    # Force re-elaboration of the report module: a cached build emits
    # no reports, and an audit of an empty log proves nothing.
    report_path = LEAN / "BalanceCarrier" / "AxiomReport.lean"
    report_path.touch()
    proc = subprocess.run(
        ["lake", "build"], capture_output=True, text=True, cwd=LEAN, check=False
    )
    log = proc.stdout + proc.stderr
    if proc.returncode != 0:
        print("FAIL: lake build exited nonzero")
        print(log[-2000:])
        return 1
    # `.+?` and not `[^']*?`: a primed theorem name ends in a quote
    # character, and the character-class pattern silently drops it --
    # the recorded primed-names parser defect.
    no_ax = re.findall(r"'(.+?)' does not depend on any axioms", log)
    with_ax = re.findall(r"'(.+?)' depends on axioms: \[([^\]]*)\]", log)
    reported = set(no_ax) | {name for name, _ in with_ax}
    for name, axes in with_ax:
        used = {a.strip() for a in axes.split(",") if a.strip()}
        extra = used - WHITELIST
        if extra:
            print(f"FAIL: {name} depends on disallowed axioms {sorted(extra)}")
            failures += 1
    report_src = report_path.read_text("utf-8")
    wanted = set(re.findall(r"#print axioms ([\w'.]+)", report_src))
    for name in sorted(wanted - reported):
        print(f"FAIL: {name} is listed in AxiomReport.lean but not reported")
        failures += 1
    for name in sorted(reported - wanted):
        print(f"FAIL: {name} is reported but not listed in AxiomReport.lean")
        failures += 1
    modules = [s for s in sources if s != report_path and s.name != "lakefile.lean"]
    declared = declared_theorems(modules)
    if not declared:
        print("FAIL: the source census found no theorem declaration")
        failures += 1
    for name in sorted(set(declared) - wanted):
        print(
            f"FAIL: {name} is declared in {declared[name]} but not listed in"
            " AxiomReport.lean"
        )
        failures += 1
    if failures:
        return 1
    print(
        f"lean audit clean: {len(sources)} sources, {len(reported)} axiom"
        f" reports ({len(no_ax)} axiom-free), axioms within {sorted(WHITELIST)},"
        f" {len(declared)} declared theorems all listed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
