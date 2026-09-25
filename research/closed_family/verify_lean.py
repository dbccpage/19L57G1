"""Build the self-contained Lean package and audit it: no forbidden
token in any committed `.lean` source, every `#print axioms` report
within the whitelist `{propext, Quot.sound}`, and every theorem named
in `AxiomReport.lean` reported.  Exit 0 on success, 1 with a named
failure otherwise.  AuthorityEffect: None.

2026-09-24: this docstring used to say "A manual receipt: no CI gate
runs this file."  That is withdrawn.  The `lean` job of
`.github/workflows/verify.yml` runs this file, locally through
`ci/run_gates.py`.  The source census below covers `Closure.lean` only;
the theorems of the reconstructed `Base.lean` are audited only where
`AxiomReport.lean` lists them or a listed theorem uses them.

2026-09-25: the previous sentence is withdrawn.  The source census now reads
both `Closure.lean` and `Base.lean`, so every theorem written in either file
must be listed in `AxiomReport.lean`; five `Base.lean` theorems were unlisted
and now are.  Each file's namespace lines are checked too, so a new nested
namespace cannot silently misname what the census expects.
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
    report_path = LEAN / "ClosedFamily" / "AxiomReport.lean"
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
    # Source census.  Found live: dropping a line from AxiomReport.lean also
    # drops its report, so neither direction of the diff above can see a
    # silent removal -- the list was checking itself against the environment
    # it generates.  This enumerates the originating module from SOURCE and
    # requires every theorem it declares to be listed.
    # 2026-09-25: Base.lean is censused too (it was not; five of its twelve
    # theorems were unlisted).  The prefix each file's theorems carry is
    # fixed by its namespace lines, which are checked rather than assumed.
    origins = (
        (LEAN / "ClosedFamily" / "Closure.lean", "ClosedFamily.Closure.",
         ["ClosedFamily", "Closure"]),
        (LEAN / "ClosedFamily" / "Base.lean", "ClosedFamily.", ["ClosedFamily"]),
    )
    declared: set[str] = set()
    for origin, prefix, namespaces in origins:
        text = origin.read_text("utf-8")
        found = re.findall(r"^\s*namespace\s+(\S+)", text, re.M)
        if found != namespaces:
            print(f"FAIL: {origin.name} opens namespaces {found}, expected {namespaces}")
            failures += 1
        for m in re.findall(r"^\s*theorem ([A-Za-z_][\w'.]*)", text, re.M):
            name = prefix + m
            declared.add(name)
            if name not in wanted:
                print(
                    f"FAIL: {name} is declared in {origin.name} but not listed in"
                    " AxiomReport.lean"
                )
                failures += 1
    if failures:
        return 1
    print(
        f"lean audit clean: {len(sources)} sources, {len(reported)} axiom"
        f" reports ({len(no_ax)} axiom-free), axioms within {sorted(WHITELIST)},"
        f" {len(declared)} written theorems of Closure.lean and Base.lean all listed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
