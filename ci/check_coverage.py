"""Independent coverage gate: line and branch coverage must EACH reach
95% over project Python code (``coverage.json`` from ``coverage json``).
Lives outside ``code/`` so it is not itself part of the measured code.

Reading a report is not the same as measuring coverage, and this file used
to conflate the two. It called ``json.load(open("coverage.json"))`` with no
existence check and no freshness check, so it reported whatever report
happened to be on disk. ``coverage.json`` was also TRACKED, which meant a
fresh clone shipped one. On a machine where ``coverage`` is not on PATH,
``coverage run`` and ``coverage json`` both fail, and this gate then printed
the committed file's percentages and exited 0. That produced a real false
pass: 99.20% / 96.92% reported against a true 99.10% / 96.73%.

Two things changed. ``coverage.json`` is no longer tracked, so there is no
committed report to fall back onto. And the report is now checked for
staleness before its numbers are believed:

* a missing report is a NAMED failure, not a traceback;
* the set of files in the report must equal the set of ``code/**/*.py`` on
  disk. The two populations are gathered independently -- one from the
  report, one from the filesystem -- so a report generated before a module
  was added or removed fails instead of being silently trusted;
* the report must not predate any measured source file. Coverage stamps
  ``meta.timestamp`` when it writes; if a source file has been modified
  since, the percentages describe code that no longer exists.

The file-set check alone is NOT enough, and the proof is the incident that
motivated this file. A tracked ``coverage.json`` is restored by git on any
branch switch, silently replacing a fresh report with the committed one --
which is what happened here, reverting a just-measured report to a
two-day-old one. The file set was identical across that swap, so only the
timestamp check catches it.

Stated limit: the timestamp check is conservative in one direction. Touching
a source file without changing its contents will fail the gate until the
report is regenerated. That is the safe direction for a gate to err, and it
is preferred to trusting a report of unknown age.

Second stated limit -- the CLOCK DOMAIN. ``meta.timestamp`` is written by
coverage and read back with ``datetime.fromisoformat``; the mtimes come from
``datetime.fromtimestamp``. Both are naive local times, so the comparison
assumes the report writer and this gate ran against a SHARED CLOCK. That
holds in CI, where checkout and the coverage run happen on one runner, and
it holds for ordinary local use. It is unproven across machines, across
timezones, and under clock skew, where the check could false-fail or -- in
principle, by up to the offset -- false-pass. Recorded rather than fixed:
making it robust means either an aware timestamp coverage does not emit, or
a monotonic marker written beside the report, and neither is worth adding
before a case exists. This is a bound on the CHECK, not on the gate's other
two conditions.
"""

import datetime
import json
import pathlib
import sys

REPORT = pathlib.Path("coverage.json")
SOURCE = pathlib.Path("code")


def normalise(name: str) -> str:
    """Coverage keys use the OS separator; compare on a single spelling."""
    return name.replace("\\", "/")


def main() -> int:
    if not REPORT.is_file():
        print(
            f"FAIL: {REPORT} not found. Generate it in the same session as "
            "the measurement:\n"
            "  python -m coverage run -m pytest -q\n"
            "  python -m coverage json -q\n"
            "Use `python -m coverage`, not bare `coverage`, which is not "
            "always on PATH and fails silently."
        )
        return 1

    data = json.loads(REPORT.read_text(encoding="utf-8"))

    reported = {normalise(name) for name in data["files"]}
    on_disk = {normalise(str(path)) for path in SOURCE.rglob("*.py")}
    if reported != on_disk:
        missing = sorted(on_disk - reported)
        extra = sorted(reported - on_disk)
        print(
            f"FAIL: {REPORT} is stale. It describes a different set of source "
            "files than the working tree, so its percentages describe a "
            "different codebase."
        )
        for name in missing:
            print(f"  on disk, absent from the report: {name}")
        for name in extra:
            print(f"  in the report, absent from disk: {name}")
        print("Regenerate it, then re-run this gate.")
        return 1

    stamped = data.get("meta", {}).get("timestamp")
    if not stamped:
        print(f"FAIL: {REPORT} carries no meta.timestamp; its age is unknown")
        return 1
    written = datetime.datetime.fromisoformat(stamped)
    newer = [
        (path, datetime.datetime.fromtimestamp(path.stat().st_mtime))
        for path in sorted(SOURCE.rglob("*.py"))
        if datetime.datetime.fromtimestamp(path.stat().st_mtime) > written
    ]
    if newer:
        print(
            f"FAIL: {REPORT} was written {written.isoformat()} and "
            f"{len(newer)} measured source file(s) have changed since. Its "
            "percentages describe code that is no longer on disk."
        )
        for path, when in newer[:5]:
            print(f"  {path} modified {when.isoformat()}")
        if len(newer) > 5:
            print(f"  ... and {len(newer) - 5} more")
        print("Regenerate it, then re-run this gate.")
        return 1

    totals = data["totals"]
    line = (
        totals["covered_lines"]
        / (totals["covered_lines"] + totals["missing_lines"])
        * 100.0
    )
    branch = totals["covered_branches"] / totals["num_branches"] * 100.0
    print(
        f"report covers {len(reported)} source files, matching the tree, "
        f"written {written.isoformat()} with no source modified since"
    )
    print(f"line coverage   {line:6.2f}%  (gate 95%)")
    print(f"branch coverage {branch:6.2f}%  (gate 95%)")
    return 0 if line >= 95.0 and branch >= 95.0 else 1


if __name__ == "__main__":
    sys.exit(main())
