"""Compile this tree's Lean file and check every theorem's axioms against a census.

Usage, from any directory:

    python research/symmetry_floor/verify_lean.py --check

AuthorityEffect: None.  A local receipt: no gate runs this file, and a pass
is one run on one machine at one revision.

What ``--check`` establishes, in order.  Every failure is printed by name and
the exit status is 1; a pass prints one PASS line and exits 0.

1. File census.  The tree's ``.lean`` files are exactly ``EXPECTED_FILES``,
   so a module cannot join or leave unnoticed.
2. Token scan.  Each of those files is read as plain text, comments included,
   against the five patterns of the root Lean audit.  That file was written
   not to name them (STATUS.md), so ``KNOWN_PROSE_LINES`` is empty and any
   match fails.  The exemption mechanism is kept so that this verifier reads
   the same as its siblings in ``oriented_boundary`` and ``sign_tower``.
3. Toolchain.  ``lean --version``, run in ``lean/`` so that the
   ``lean-toolchain`` file there selects it, must report Lean 4.33.0.
4. Build.  ``lean SymmetryFloor.lean`` in ``lean/``: the command STATUS.md
   gives the reader.  There is no lakefile and this verifier adds none.  No
   output may report a declaration that uses the placeholder proof.
5. Reports.  The output of step 4 carries the file's own ``#print axioms``
   lines, parsed with the non-greedy pattern ``'(.+?)'``, which keeps a primed
   name whole where a character-class pattern would silently drop it.
6. Census.  The same file is compiled a second time, with ``-o``, to an
   object file in a temporary directory outside the repository.  A Lean file
   written to that directory imports it (``LEAN_PATH`` points there) and
   prints every theorem the module added to the compiled environment, with
   the axioms ``collectAxioms`` finds for it.  The population is Lean's record
   of what it compiled, not a reading of source text, so a comment or a
   docstring cannot move it.
7. Comparison.  Every census theorem, generated ones included, depends only
   on ``ALLOWED_AXIOMS``.  The theorems written in the source are exactly the
   keys of ``EXPECTED_AXIOMS``.  The reports name exactly those theorems, once
   each, and each report lists the axioms the census found.  Each theorem's
   axioms equal ``EXPECTED_AXIOMS``: ``floor`` and ``floor_iterated`` depend
   on no axioms, as CLAIM_LEDGER.md states for SF-1 and SF-2, and the four
   ``decide`` results depend on ``propext``, as STATUS.md states.
8. No writes.  Every file under this tree, outside Python caches, has the
   same bytes after the run as before, and no file appeared.

Which census theorems count as generated rather than written in the source is
decided by fixed rules on facts the census reads from the environment:
compiler-internal names (``Name.isInternalDetail`` of the user-facing name,
which covers auxiliary proofs and equation lemmas); the ``inj``, ``injEq``
and ``sizeOf_spec`` lemmas under a constructor; ``ofNat_ctorIdx`` under an
inductive type; and proof-valued structure fields (projections).  A private
theorem that is not compiler-internal fails the check, because a report file
cannot name it.  Generated theorems have no report line but are still held
to ``ALLOWED_AXIOMS``.

Scope.  This checks the Lean file of this tree only.  The exhaustion and
computation claims (SF-6 onward) belong to the Python suite, which this does
not run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

TREE = Path(__file__).resolve().parent
LEAN = TREE / "lean"
REPORT_FILE = "SymmetryFloor.lean"
LEAN_VERSION_PREFIX = "Lean (version 4.33.0,"
ALLOWED_AXIOMS = {"propext", "Quot.sound"}
TIMEOUT_SECONDS = 1800

EXPECTED_FILES = frozenset({"SymmetryFloor.lean"})

# Every theorem written in the source, with the axioms the recorded claims
# give it: SF-1 and SF-2 in CLAIM_LEDGER.md for the first two, and STATUS.md
# ("the four decide results depend on propext") for the rest.
EXPECTED_AXIOMS: dict[str, list[str]] = {
    "SymmetryFloor.floor": [],
    "SymmetryFloor.floor_iterated": [],
    "SymmetryFloor.start_still": ["propext"],
    "SymmetryFloor.offered_set_carried": ["propext"],
    "SymmetryFloor.members_move": ["propext"],
    "SymmetryFloor.price_is_two": ["propext"],
}
EXPECTED_THEOREMS = frozenset(EXPECTED_AXIOMS)

# SHA-256 of whole stripped prose lines that name a scanned token to say
# the file avoids it.  Empty: SymmetryFloor.lean names none.
KNOWN_PROSE_LINES: dict[str, frozenset[str]] = {}

# The root Lean audit's five patterns, assembled from fragments so that this
# file does not match them itself.
FORBIDDEN = tuple(
    re.compile(pattern, re.MULTILINE)
    for pattern in (
        r"\b" + "so" + r"rry\b",
        r"\b" + "ad" + r"mit\b",
        r"^\s*" + "ax" + r"iom\s",
        r"\b" + "un" + r"safe\b",
        r"\b" + "par" + r"tial\b",
    )
)
PLACEHOLDER_USE = "declaration uses '" + "so" + "rry'"

REPORT_WITH = re.compile(r"^'(.+?)' depends on axioms: \[([^\]]*)\]", re.MULTILINE)
REPORT_NONE = re.compile(r"^'(.+?)' does not depend on any axioms$", re.MULTILINE)
REPORT_ANY = re.compile(r"^'.*(?:depends on axioms|does not depend on any axioms)", re.MULTILINE)

CTOR_DERIVED = frozenset({"inj", "injEq", "sizeOf_spec"})
CACHE_DIRS = frozenset({".lake", "__pycache__", ".mypy_cache", ".pytest_cache"})

CENSUS_TEMPLATE = """\
import Lean.Elab.Command
import Lean.Util.CollectAxioms
import Lean.Data.Json
@@IMPORTS@@

open Lean Elab Command in
run_cmd do
  let env <- getEnv
  let mut count := 0
  for modName in (@@MODULES@@ : Array Name) do
    let some idx := env.getModuleIdx? modName
      | throwError "census: module is not in the environment: {modName}"
    let data := env.header.moduleData[idx.toNat]!
    for declName in data.constNames do
      match env.find? declName with
      | some (.thmInfo _) =>
        let axioms <- liftCoreM (Lean.collectAxioms declName)
        let userName := (privateToUserName? declName).getD declName
        let parentKind : String := match declName with
          | .str parent _ =>
            (match env.find? parent with
              | some (.ctorInfo _) => "constructor"
              | some (.inductInfo _) => "inductive"
              | some _ => "other"
              | none => "none")
          | _ => "none"
        let lastPart : String := match declName with
          | .str _ last => last
          | _ => ""
        let record := Json.mkObj [
          ("module", toJson modName.toString),
          ("name", toJson declName.toString),
          ("private", toJson (isPrivateName declName)),
          ("internal", toJson userName.isInternalDetail),
          ("projection", toJson (env.isProjectionFn declName)),
          ("parent", toJson parentKind),
          ("last", toJson lastPart),
          ("axioms", toJson (axioms.map Name.toString))]
        liftIO <| IO.println ("CENSUS_THEOREM " ++ record.compress)
        count := count + 1
      | _ => pure ()
  liftIO <| IO.println ("CENSUS_DONE " ++ toString count)
"""


class CheckFailed(Exception):
    """A stage failed; the message names what failed."""


def module_name(relative: str) -> str:
    return relative[: -len(".lean")].replace("/", ".")


def lean_files() -> set[str]:
    return {
        path.relative_to(LEAN).as_posix()
        for path in LEAN.rglob("*.lean")
        if not (CACHE_DIRS & set(path.relative_to(LEAN).parts)) and path.name != "lakefile.lean"
    }


def check_file_census() -> list[str]:
    actual = lean_files()
    failures = [f"unexpected Lean file: lean/{name}" for name in sorted(actual - EXPECTED_FILES)]
    failures += [f"expected Lean file is missing: lean/{name}" for name in sorted(EXPECTED_FILES - actual)]
    return failures


def line_digest(line: str) -> str:
    return hashlib.sha256(line.strip().encode("utf-8")).hexdigest()


def scan_tokens() -> list[str]:
    failures: list[str] = []
    for relative in sorted(EXPECTED_FILES):
        text = (LEAN / relative).read_bytes().decode("utf-8").replace("\r\n", "\n")
        lines = text.split("\n")
        digests = [line_digest(line) for line in lines]
        exempt = KNOWN_PROSE_LINES.get(relative, frozenset())
        for digest in sorted(exempt):
            numbers = [index + 1 for index, found in enumerate(digests) if found == digest]
            if len(numbers) != 1:
                failures.append(
                    f"stale token exemption: {digest[:12]} matches {len(numbers)} lines of lean/{relative}"
                )
            elif not any(pattern.search(lines[numbers[0] - 1]) for pattern in FORBIDDEN):
                failures.append(
                    f"stale token exemption: lean/{relative}:{numbers[0]} names no scanned token"
                )
        for pattern in FORBIDDEN:
            for match in pattern.finditer(text):
                # Counted from the end: a leading \s* may begin on a blank line above.
                number = text.count("\n", 0, match.end() - 1) + 1
                if digests[number - 1] in exempt:
                    continue
                failures.append(
                    f"forbidden token {match.group(0).strip()!r} at lean/{relative}:{number}"
                )
    return failures


def snapshot() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in TREE.rglob("*"):
        parts = set(path.relative_to(TREE).parts)
        if path.is_file() and not (CACHE_DIRS & parts):
            result[path.relative_to(TREE).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def executable(name: str) -> str:
    located = shutil.which(name)
    if located is not None:
        return located
    fallback = Path.home() / ".elan" / "bin" / (name + (".exe" if os.name == "nt" else ""))
    if fallback.is_file():
        return str(fallback)
    raise CheckFailed(f"{name} is not on PATH and not in ~/.elan/bin")


def run(args: list[str], cwd: Path, lean_path: str | None = None) -> str:
    environment = dict(os.environ)
    if lean_path is not None:
        environment["LEAN_PATH"] = lean_path
    try:
        result = subprocess.run(
            args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=TIMEOUT_SECONDS, check=False, env=environment,
        )
    except subprocess.TimeoutExpired as exc:
        raise CheckFailed(f"timed out after {TIMEOUT_SECONDS}s: {' '.join(args)}") from exc
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise CheckFailed(f"exit {result.returncode}: {' '.join(args)}\n{output[-4000:]}")
    if PLACEHOLDER_USE in output:
        raise CheckFailed(f"output reports a placeholder proof: {' '.join(args)}")
    return output


def parse_reports(text: str) -> tuple[dict[str, list[str]], list[str]]:
    reports: dict[str, list[str]] = {}
    failures: list[str] = []
    parsed = 0
    for match in REPORT_WITH.finditer(text):
        parsed += 1
        name = match.group(1)
        axioms = sorted(item.strip() for item in match.group(2).split(",") if item.strip())
        if name in reports:
            failures.append(f"duplicate #print axioms report: {name}")
        reports[name] = axioms
    for match in REPORT_NONE.finditer(text):
        parsed += 1
        name = match.group(1)
        if name in reports:
            failures.append(f"duplicate #print axioms report: {name}")
        reports[name] = []
    seen = len(REPORT_ANY.findall(text))
    if seen != parsed:
        failures.append(f"{seen} report lines but {parsed} parsed; a report shape was not recognised")
    return reports, failures


def census_source() -> str:
    modules = sorted(module_name(name) for name in EXPECTED_FILES)
    return (
        CENSUS_TEMPLATE
        .replace("@@IMPORTS@@", "\n".join(f"import {name}" for name in modules))
        .replace("@@MODULES@@", "#[" + ", ".join(f"`{name}" for name in modules) + "]")
    )


def parse_census(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    done: list[int] = []
    for line in text.splitlines():
        if line.startswith("CENSUS_THEOREM "):
            row = json.loads(line[len("CENSUS_THEOREM "):])
            if not isinstance(row, dict):
                raise CheckFailed(f"census row is not an object: {line}")
            rows.append(row)
        elif line.startswith("CENSUS_DONE "):
            done.append(int(line[len("CENSUS_DONE "):]))
    if done != [len(rows)]:
        raise CheckFailed(f"census incomplete: {len(rows)} rows read, completion lines {done}")
    return rows


def classify(row: dict[str, Any]) -> str:
    if row["internal"]:
        return "generated"
    if row["private"]:
        return "private"
    if row["last"] in CTOR_DERIVED and row["parent"] == "constructor":
        return "generated"
    if row["last"] == "ofNat_ctorIdx" and row["parent"] == "inductive":
        return "generated"
    if row["projection"]:
        return "generated"
    return "authored"


def compare(rows: list[dict[str, Any]], reports: dict[str, list[str]]) -> tuple[list[str], dict[str, int]]:
    failures: list[str] = []
    census: dict[str, list[str]] = {}
    kinds: dict[str, int] = {"authored": 0, "generated": 0}
    authored: set[str] = set()
    for row in rows:
        name = str(row["name"])
        axioms = sorted(str(item) for item in row["axioms"])
        if name in census:
            failures.append(f"census lists {name} twice")
        census[name] = axioms
        disallowed = sorted(set(axioms) - ALLOWED_AXIOMS)
        if disallowed:
            failures.append(f"{name} depends on disallowed axioms {disallowed}")
        kind = classify(row)
        if kind == "private":
            failures.append(f"private theorem {name} cannot be named by a report")
            continue
        kinds[kind] += 1
        if kind == "authored":
            authored.add(name)
    if not authored:
        failures.append("census found no theorem written in the source")
    for name in sorted(authored - EXPECTED_THEOREMS):
        failures.append(f"census theorem {name} is not in EXPECTED_THEOREMS")
    for name in sorted(EXPECTED_THEOREMS - authored):
        failures.append(f"expected theorem {name} is not in the compiled census")
    for name in sorted(authored - set(reports)):
        failures.append(f"census theorem {name} has no #print axioms report in lean/{REPORT_FILE}")
    for name in sorted(set(reports) - authored):
        failures.append(f"report for {name} names no theorem written in the source")
    for name in sorted(set(reports) & set(census)):
        if reports[name] != census[name]:
            failures.append(f"report for {name} lists {reports[name]}, census finds {census[name]}")
    for name, wanted in sorted(EXPECTED_AXIOMS.items()):
        if name in census and census[name] != wanted:
            failures.append(
                f"{name} depends on {census[name] or 'no axioms'}; "
                f"the recorded claim is {wanted or 'no axioms'}"
            )
    return failures, kinds


def check() -> tuple[list[str], str]:
    failures = check_file_census()
    if failures:
        return failures, ""
    failures = scan_tokens()
    if failures:
        return failures, ""
    before = snapshot()
    lean = executable("lean")
    version = run([lean, "--version"], LEAN).strip()
    if not version.startswith(LEAN_VERSION_PREFIX):
        return [f"unexpected Lean version: {version}"], ""
    reports, failures = parse_reports(run([lean, REPORT_FILE], LEAN))
    with tempfile.TemporaryDirectory(prefix=f"{TREE.name}_census_") as scratch:
        compiled = Path(scratch) / (module_name(REPORT_FILE) + ".olean")
        run([lean, "-R", ".", "-o", str(compiled), REPORT_FILE], LEAN)
        census_file = Path(scratch) / "Census.lean"
        census_file.write_bytes(census_source().encode("utf-8"))
        rows = parse_census(run([lean, str(census_file)], LEAN, lean_path=scratch))
    found, kinds = compare(rows, reports)
    failures += found
    after = snapshot()
    for name in sorted(set(before) | set(after)):
        if before.get(name) != after.get(name):
            failures.append(f"the run changed or created research/{TREE.name}/{name}")
    summary = (
        f"{kinds['authored']} theorems written in the source, each reported once "
        f"with the axioms its recorded claim gives; "
        f"{kinds['generated']} generated theorems; all {len(rows)} depend only on "
        f"{sorted(ALLOWED_AXIOMS)}; {len(EXPECTED_FILES)} Lean files; {version.split(',')[0]})"
    )
    return failures, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--check", action="store_true", required=True,
                        help="compile, census and compare; write nothing")
    parser.parse_args(argv)
    try:
        failures, summary = check()
    except (CheckFailed, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(f"PASS: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
