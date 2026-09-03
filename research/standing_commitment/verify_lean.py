"""Build the self-contained Lean package and audit it: no forbidden
token in any committed `.lean` source, every `#print axioms` report
within the whitelist `{propext, Quot.sound}`, and every theorem named
in `AxiomReport.lean` reported.  A manual receipt: no CI gate runs
this file.  Exit 0 on success, 1 with a named failure otherwise.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys
import re
import subprocess
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
LEAN = HERE / "lean"

# Word-boundary patterns, mirroring the root gate `ci/check_lean_audit.py`
# exactly.  Found live in this tree: the copies inherited by the sibling
# research trees test `token in text`, a SUBSTRING scan, which flags the
# estate's own word "admitted" -- a word the sealed Lean uses throughout and
# the root gate allows, because the root gate is `admit`.  A local scan
# that is stricter than the gate it mirrors is a false alarm, not a stronger
# guarantee.  Patterns are assembled from fragments so this file does not
# trip itself.
FORBIDDEN = (
    r"\bso" + r"rry\b",
    r"\bad" + r"mit\b",
    r"\buns" + r"afe\b",
    r"\bpar" + r"tial\b",
    r"\bnative_" + r"decide\b",
)
LEADING_AXIOM = re.compile(r"^\s*ax" + r"iom\s", re.MULTILINE)
WHITELIST = {"propext", "Quot.sound"}


def main() -> int:
    failures = 0
    sources = sorted(LEAN.rglob("*.lean"))
    sources = [s for s in sources if ".lake" not in s.parts]
    for src in sources:
        text = src.read_text("utf-8")
        for pattern in FORBIDDEN:
            hit = re.search(pattern, text)
            if hit is not None:
                print(f"FAIL: {src.name} contains forbidden token {hit.group(0)!r}")
                failures += 1
        if LEADING_AXIOM.search(text):
            print(f"FAIL: {src.name} contains a leading ax" + "iom declaration")
            failures += 1
    # Force re-elaboration of the report module: a cached build emits
    # no reports, and an audit of an empty log proves nothing.
    report_path = LEAN / "StandingCommitment" / "AxiomReport.lean"
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
    # Source census: dropping a line from AxiomReport.lean drops its report
    # too, so the diff above cannot see a silent removal.  Recorded as a live
    # find in the closed_family tree and closed the same way here.
    origin = LEAN / "StandingCommitment" / "Commitment.lean"
    declared = {
        f"StandingCommitment.Standing.{m}"
        for m in re.findall(r"^theorem ([A-Za-z_][\w'.]*)", origin.read_text("utf-8"), re.M)
    }
    for name in sorted(declared - wanted):
        print(f"FAIL: {name} is declared in {origin.name} but not listed in AxiomReport.lean")
        failures += 1
    if failures:
        return 1
    print(
        f"lean audit clean: {len(sources)} sources, {len(reported)} axiom"
        f" reports ({len(no_ax)} axiom-free), axioms within {sorted(WHITELIST)},"
        f" {len(declared)} originating theorems all listed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
