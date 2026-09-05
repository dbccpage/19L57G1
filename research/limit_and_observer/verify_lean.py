"""Rebuild this tree's Lean package from clean and compare the axiom reports.

Run from inside ``research/limit_and_observer``:

    python verify_lean.py

It rebuilds, scans every ``.lean`` file as plain text for the forbidden
tokens, requires every ``#print axioms`` report to lie within
``{propext, Quot.sound}``, and compares the whole report block byte for byte
against ``receipts/lean_axioms.txt``.

**This is a MANUAL receipt.**  No CI gate runs it — not here, and not in any
other research tree.  ``CLAUDE.md`` records that as the last live residual,
and this tree sits squarely inside it.  A pass here is evidence a person ran
it, not evidence a gate enforced it, and every claim resting on it is
labelled CITED rather than CHECKED.

AuthorityEffect: None.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(HERE, "lean")
RECEIPT = os.path.join(HERE, "receipts", "lean_axioms.txt")

FORBIDDEN = (
    r"\bsorry\b",
    r"\badmit\b",
    r"^\s*axiom\s",
    r"\bunsafe\b",
    r"\bpartial\b",
)
ALLOWED_AXIOMS = {"propext", "Quot.sound"}
REPORT = re.compile(r"'([^']+?)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main(write: bool = False) -> None:
    sources = []
    for root, _dirs, files in os.walk(LEAN):
        if ".lake" in root:
            continue
        for name in sorted(files):
            if name.endswith(".lean"):
                sources.append(os.path.join(root, name))
    if not sources:
        fail("no Lean sources found; the census would be vacuous")

    for path in sorted(sources):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for pattern in FORBIDDEN:
            for match in re.finditer(pattern, text, flags=re.M):
                line = text[: match.start()].count("\n") + 1
                fail(
                    f"forbidden token {match.group(0)!r} at "
                    f"{os.path.relpath(path, HERE)}:{line}"
                )

    build = subprocess.run(
        ["lake", "build"], cwd=LEAN, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True,
    )
    log = build.stdout
    if build.returncode != 0:
        print(log)
        fail("lake build failed")

    reports = []
    for m in REPORT.finditer(log):
        name = m.group(1)
        raw = m.group(2)
        axioms = (
            sorted(a.strip() for a in raw.split(",") if a.strip())
            if raw else []
        )
        bad = set(axioms) - ALLOWED_AXIOMS
        if bad:
            fail(f"disallowed axioms {sorted(bad)} in {name}")
        reports.append(f"{name}: {axioms}")
    if not reports:
        fail("no axiom reports in the build log; force a rebuild")

    text = "\n".join(sorted(reports)) + "\n"
    if write:
        with open(RECEIPT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"wrote {RECEIPT} ({len(reports)} reports)")
        return
    if not os.path.isfile(RECEIPT):
        fail(f"{RECEIPT} is missing; regenerate deliberately with --write")
    with open(RECEIPT, encoding="utf-8") as fh:
        committed = fh.read()
    if committed != text:
        fail(
            "axiom reports differ between the build and the committed "
            f"receipt\n--- committed ---\n{committed}\n--- build ---\n{text}"
        )
    print(
        f"limit_and_observer lean audit clean: {len(sources)} sources, "
        f"{len(reports)} axiom reports, axioms within "
        f"{sorted(ALLOWED_AXIOMS)}  [MANUAL RECEIPT: no gate reads this]"
    )


if __name__ == "__main__":
    main(write="--write" in sys.argv)
