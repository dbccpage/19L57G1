"""Regenerate ``artifacts/lean_axioms.txt`` from a ``lake build`` log.

The artifact is the sequence of axiom reports emitted by BOTH default
targets, with Lean's ``info: `` prefix stripped and the build-log ordering
preserved.

An earlier version of this paragraph said the reports come from
``lean4/Derivation.lean`` and that the ordering "is `Derivation.lean` line
order". Both are **WITHDRAWN**. ``lean4/ParkedAudit.lean`` is a second root
and contributes 48 reports, ordered by parked module and then by name, and
its whole block is anchored at that file's ``run_cmd`` position rather than
at each theorem's own line.

Two consequences worth knowing before regenerating:

* Forcing only ``Derivation.lean`` to rebuild produces an artifact missing
  every parked report, which ``ci/check_axiom_report.py`` then rejects.
  Touch both roots.
* Because the parked block carries one shared source position, editing the
  prose above ``run_cmd`` in ``ParkedAudit.lean`` shifts all 48 lines. The
  position is stripped by every gate that compares NAMES, so the only signal
  is the workflow's byte ``diff``, and the repair is the full cascade:
  regenerate this artifact, then the receipts that pin its SHA-256, then the
  research manifest.

Newlines are written explicitly as ``\\n``.  This is the whole point of the
script: ``.gitattributes`` marks ``artifacts/** -text``, so whatever bytes
land here are the bytes that get committed.  A plain shell redirect on
Windows writes CRLF and silently rewrites all 1000+ lines, which is what
happened in PR #20.  Never regenerate this artifact with a shell redirect.

Usage::

    cd lean4 && lake build 2>&1 | tee ../build.log
    python ci/regen_axiom_artifact.py build.log
"""

from __future__ import annotations

import pathlib
import re
import sys

REPORT = re.compile(
    r"'(?P<name>.+?)' (?:depends on axioms: \[[^\]]*\]|does not depend on any axioms)"
)
ARTIFACT = pathlib.Path("artifacts") / "lean_axioms.txt"


def extract(log_text: str) -> list[str]:
    """Return the axiom-report lines of a build log, prefix stripped."""
    out: list[str] = []
    for line in log_text.splitlines():
        if REPORT.search(line) is None:
            continue
        out.append(line.removeprefix("info: ").rstrip())
    return out


def render(lines: list[str]) -> str:
    """Render the artifact body with a trailing newline, LF throughout."""
    return "".join(f"{line}\n" for line in lines)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    lines = extract(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    if not lines:
        print("FAIL: no axiom reports found in the build log")
        return 1
    body = render(lines)
    ARTIFACT.write_bytes(body.encode("utf-8"))
    print(f"wrote {ARTIFACT} ({len(lines)} reports, LF, {len(body.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
