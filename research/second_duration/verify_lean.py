"""Build this rung's self-contained Lean package and audit it.

A hand copy of `research/second_succession/verify_lean.py`, with this rung's
paths.  The estate records that these verifiers are copies and that a
defect repaired in one stays live in the others until carried by hand;
`research/README.md` lists the copies and `research/house_diff.py
--families` finds them.

Six checks, none implying the others:

* no forbidden token in any committed ``.lean`` source of this package,
  matched at word boundaries exactly as the root gate ``ci/check_lean_audit.py``
  matches them, comments and doc strings included;
* every ``#print axioms`` report of a FRESH build lies within the whitelist
  ``{propext, Quot.sound}``;
* an independent Lean-environment census enumerates every explicit theorem
  declaration originating in every package module, including the library
  root and ``AxiomReport.lean``, and collects its axioms directly;
* the fresh ``#print axioms`` population equals that compiler census in both
  directions and axiom-for-axiom -- dropping a print drops only one side;
* the compiler census equals the FW-DEF census, with globally unique leaf
  names and the recorded source module checked for every row;
* the COMMITTED log ``receipts/lean_axioms.txt`` matches the fresh build
  exactly, line for line.

The seed requires each rung's axiom log to be committed and checked
against a fresh build rather than left as a manual receipt.  CI runs this
file in the Lean job, where elan is installed; the Python research job does
not need to install a second toolchain.

``--regen`` rewrites the committed log only after the fresh compiler census,
report population, FW-DEF totality, and axiom whitelist pass.  It cannot
validate the receipt bytes it is replacing, and must never be run while an
injection is live.

Exit 0 on success, 1 with a named failure otherwise.  AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = Path(__file__).resolve().parent
LEAN = HERE / "lean"
LOG = HERE / "receipts" / "lean_axioms.txt"
REPORT = LEAN / "SecondDuration" / "AxiomReport.lean"
FWDEF = HERE / "FWDEF_CENSUS.json"

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
DECL_PREFIX = (
    r"(?:@\[[^\]\r\n]*\]\s*)*"
    r"(?:(?:private|protected|noncomputable|local)\s+)*"
)
IDENT_SEGMENT = r"(?:«[^»\r\n]+»|(?:[^\W\d]|_)(?:\w|['!?])*)"
IDENTIFIER = rf"{IDENT_SEGMENT}(?:\.{IDENT_SEGMENT})*"
LEADING_AXIOM = re.compile(
    rf"^[ \t]*{DECL_PREFIX}ax" + r"iom\s", re.MULTILINE
)
THEOREM_DECL = re.compile(
    rf"^[ \t]*(?P<prefix>{DECL_PREFIX})(?:theorem|lemma)\s+"
    rf"(?P<name>{IDENTIFIER})",
    re.MULTILINE,
)
THEOREM_START = re.compile(
    rf"^[ \t]*{DECL_PREFIX}(?:theorem|lemma)\b", re.MULTILINE
)
WHITELIST = {"propext", "Quot.sound"}

CENSUS_MODULE_TAG = "MODULE_CENSUS\t"
CENSUS_DECL_TAG = "DECL_CENSUS\t"


def declaration_text(text: str) -> str:
    """Replace Lean comments with spaces while preserving line structure.

    Lean block comments nest.  A regex deletion can expose comment text or
    terminate at the wrong delimiter, so the declaration census uses this
    small scanner.  String literal contents are hidden too, while their
    comment-like bytes do not change scanner state.
    """
    out: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(text):
        pair = text[index : index + 2]
        char = text[index]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if in_string:
            out.append("\n" if char == "\n" else " ")
            if char == "\\" and index + 1 < len(text):
                out.append(" ")
                index += 2
            else:
                if char == '"':
                    in_string = False
                index += 1
            continue
        if pair == "/-":
            depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            out.extend("  ")
            index += 2
            while index < len(text) and text[index] != "\n":
                out.append(" ")
                index += 1
        else:
            out.append(char)
            if char == '"':
                in_string = True
            index += 1
    if depth:
        raise ValueError("unterminated Lean block comment")
    return "".join(out)


def canonical_identifier(name: str) -> str:
    """Decode quoted source segments to reconstruction/FW-DEF leaf keys."""
    return re.sub(r"«([^»]+)»", r"\1", name)


def theorem_names(text: str) -> list[str]:
    """Declared theorem/lemma names, comments excluded and quotes decoded."""
    visible = declaration_text(text)
    starts = list(THEOREM_START.finditer(visible))
    declarations = list(THEOREM_DECL.finditer(visible))
    if [match.start() for match in starts] != [
        match.start() for match in declarations
    ]:
        raise ValueError("unsupported theorem declaration syntax")
    names: list[str] = []
    for match in declarations:
        if re.search(r"\bprivate\b", match.group("prefix")):
            raise ValueError("private theorem declarations cannot be axiom-censused")
        names.append(canonical_identifier(match.group("name")))
    return names


def sources() -> list[Path]:
    found = [path for path in LEAN.rglob("*.lean") if ".lake" not in path.parts]
    return sorted(found, key=lambda path: path.relative_to(LEAN).as_posix())


def modules() -> list[Path]:
    """Every module source in the package, including both configured roots."""
    config = LEAN / "lakefile.lean"
    return [path for path in sources() if path != config]


def module_name(path: Path) -> str:
    relative = path.relative_to(LEAN).with_suffix("")
    for part in relative.parts:
        if re.fullmatch(r"(?:[^\W\d]|_)(?:\w|['!?])*", part) is None:
            raise ValueError(f"unsupported Lean module path component {part!r}")
    return ".".join(relative.parts)


def module_names() -> list[str]:
    paths = modules()
    names = [module_name(path) for path in paths]
    if len(names) != len(set(names)):
        raise ValueError("duplicate Lean module name in package census")
    basenames = [path.name for path in paths]
    if len(basenames) != len(set(basenames)):
        raise ValueError("duplicate module basename is ambiguous in FW-DEF census")
    if not names:
        raise ValueError("Lean package module census is empty")
    return names


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


def build() -> tuple[str, int, str]:
    """Clean, then build, naming which stage returned the status."""
    clean = subprocess.run(
        ["lake", "clean"], capture_output=True, text=True, encoding="utf-8",
        errors="strict", cwd=LEAN, check=False
    )
    clean_log = clean.stdout + clean.stderr
    if clean.returncode != 0:
        return "clean", clean.returncode, clean_log
    # Force re-elaboration of the report module after the clean.  This also
    # makes the intent explicit if Lake's clean implementation ever changes.
    REPORT.touch()
    proc = subprocess.run(
        ["lake", "build", *module_names()], capture_output=True, text=True,
        encoding="utf-8",
        errors="strict", cwd=LEAN, check=False
    )
    return "build", proc.returncode, proc.stdout + proc.stderr


def parse(log: str) -> tuple[dict[str, tuple[str, ...]], int]:
    """Every report of the build log, as name -> sorted axioms.

    ``.+?`` and not ``[^']*?``: a primed theorem name ends in a quote
    character, and the character-class pattern silently drops it -- the
    recorded primed-names parser defect.
    """
    reports: dict[str, tuple[str, ...]] = {}
    free = 0
    for name in re.findall(r"'(.+?)' does not depend on any axioms", log):
        if name in reports:
            raise ValueError(f"duplicate axiom report {name}")
        reports[name] = ()
        free += 1
    for name, axes in re.findall(
        r"'(.+?)' depends on axioms: \[([^\]]*)\]", log
    ):
        if name in reports:
            raise ValueError(f"duplicate axiom report {name}")
        reports[name] = tuple(sorted(a.strip() for a in axes.split(",") if a.strip()))
    return reports, free


def census_driver(names: list[str]) -> str:
    """A generated Lean command that asks the compiled environment itself.

    Module origins, declaration ranges, and projection metadata distinguish
    explicit theorem/lemma declarations from imported and compiler-generated
    theorem constants.  ``collectAxioms`` audits private declarations too;
    it does not depend on a source-spellable ``#print`` name.
    """
    imports = "\n".join(f"import {name}" for name in names)
    target_names = ", ".join(json.dumps(name, ensure_ascii=False) for name in names)
    return f'''import Lean
{imports}
open Lean Elab Command
run_cmd
  let targetModules := [{target_names}].map String.toName |>.toArray
  let env ← getEnv
  let mut targets : Array (Name × ModuleIdx) := #[]
  for targetName in targetModules do
    match env.getModuleIdx? targetName with
    | some idx =>
      targets := targets.push (targetName, idx)
      IO.println s!"MODULE_CENSUS\\t{{(Json.mkObj [("module", .str (targetName.toString (escape := true)))]).compress}}"
    | none => throwError "missing imported target module {{targetName}}"
  let mut declarations : Array (Name × ModuleIdx) := #[]
  for (name, info) in env.constants do
    match env.getModuleIdxFor? name with
    | none => pure ()
    | some idx =>
      if targets.any (fun target => target.2 == idx) &&
          ConstantKind.ofConstantInfo info == .thm && !env.isProjectionFn name then
        let range? ← liftCoreM <| findDeclarationRanges? name
        if range?.isSome then declarations := declarations.push (name, idx)
  declarations := declarations.qsort (fun a b => Name.quickLt a.1 b.1)
  for (name, idx) in declarations do
    let axioms := (← collectAxioms name).qsort Name.quickLt
    let record := Json.mkObj [
      ("name", .str (name.toString (escape := true))),
      ("leaf", .str name.getString!),
      ("module", .str (env.header.moduleNames[idx]!.toString (escape := true))),
      ("axioms", .arr (axioms.map fun ax => .str (ax.toString (escape := true))))]
    IO.println s!"DECL_CENSUS\\t{{record.compress}}"
'''


def run_compiler_census(names: list[str]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="second_duration_census_") as tmp:
        driver = Path(tmp) / "SecondDurationCensus.lean"
        driver.write_text(census_driver(names), encoding="utf-8", newline="\n")
        proc = subprocess.run(
            ["lake", "env", "lean", str(driver)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            cwd=LEAN,
            check=False,
        )
    return proc.returncode, proc.stdout + proc.stderr


def parse_compiler_census(
    log: str,
) -> tuple[set[str], dict[str, tuple[str, str, tuple[str, ...]]]]:
    """Return module names and full-name -> (leaf, module, axioms)."""
    found_modules: set[str] = set()
    records: dict[str, tuple[str, str, tuple[str, ...]]] = {}
    for line in log.splitlines():
        if line.startswith(CENSUS_MODULE_TAG):
            row = json.loads(line.removeprefix(CENSUS_MODULE_TAG))
            if set(row) != {"module"} or not isinstance(row["module"], str):
                raise ValueError("malformed compiler module-census row")
            if row["module"] in found_modules:
                raise ValueError(f"duplicate compiler module row {row['module']}")
            found_modules.add(row["module"])
        elif line.startswith(CENSUS_DECL_TAG):
            row = json.loads(line.removeprefix(CENSUS_DECL_TAG))
            if set(row) != {"name", "leaf", "module", "axioms"}:
                raise ValueError("malformed compiler declaration-census row")
            name = row["name"]
            leaf = row["leaf"]
            module = row["module"]
            axes = row["axioms"]
            if (
                not isinstance(name, str)
                or not isinstance(leaf, str)
                or not isinstance(module, str)
                or not isinstance(axes, list)
                or not all(isinstance(axis, str) for axis in axes)
            ):
                raise ValueError("malformed compiler declaration-census values")
            if name in records:
                raise ValueError(f"duplicate compiler declaration row {name}")
            records[name] = (leaf, module, tuple(sorted(axes)))
    if not found_modules:
        raise ValueError("compiler module census is empty")
    if not records:
        raise ValueError("compiler declaration census is empty")
    return found_modules, records


def render(reports: dict[str, tuple[str, ...]]) -> str:
    lines = [
        f"{name} :: {' '.join(axes) if axes else 'none'}"
        for name, axes in sorted(reports.items())
    ]
    return "\n".join(lines) + "\n"


def fwdef_failures(
    records: dict[str, tuple[str, str, tuple[str, ...]]],
) -> list[str]:
    """Compare compiler declarations with the leaf-keyed FW-DEF ledger."""
    payload = json.loads(FWDEF.read_text(encoding="utf-8"))
    rows = payload.get("classes")
    if not isinstance(rows, dict):
        return ["FAIL: FWDEF_CENSUS.json has no classes object"]
    by_leaf: dict[str, tuple[str, str]] = {}
    failures: list[str] = []
    for full_name, (leaf, module, _axes) in sorted(records.items()):
        if leaf in by_leaf:
            prior, _ = by_leaf[leaf]
            failures.append(
                f"FAIL: compiler declarations {prior} and {full_name} share FW-DEF"
                f" leaf key {leaf!r}"
            )
        else:
            by_leaf[leaf] = (full_name, module)
    for leaf in sorted(set(rows) - set(by_leaf)):
        failures.append(f"FAIL: FW-DEF row {leaf} has no compiler declaration")
    for leaf in sorted(set(by_leaf) - set(rows)):
        full_name, module = by_leaf[leaf]
        failures.append(
            f"FAIL: compiler declaration {full_name} from {module} has no FW-DEF row"
        )
    expected_files = {name: path.name for name, path in zip(module_names(), modules())}
    for leaf in sorted(set(rows) & set(by_leaf)):
        full_name, module = by_leaf[leaf]
        expected_file = expected_files.get(module)
        if expected_file is None:
            failures.append(
                f"FAIL: compiler declaration {full_name} has unexpected module {module}"
            )
            continue
        row = rows[leaf]
        if not isinstance(row, dict) or row.get("module") != expected_file:
            failures.append(
                f"FAIL: FW-DEF row {leaf} records module "
                f"{row.get('module') if isinstance(row, dict) else row!r}; compiler"
                f" origin is {expected_file}"
            )
    return failures


def audit(regen: bool) -> int:
    failures = token_scan()
    for line in failures:
        print(line)
    try:
        names = module_names()
        stage, code, log = build()
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: could not construct or build the module census: {exc}")
        return 1
    if code != 0:
        print(f"FAIL: lake {stage} exited nonzero")
        print(log[-2000:])
        return 1
    try:
        reports, free = parse(log)
    except (UnicodeError, ValueError) as exc:
        print(f"FAIL: could not parse the fresh axiom reports: {exc}")
        return 1
    if not reports:
        print("FAIL: the build produced no axiom report; nothing was audited")
        return 1
    census_code, census_log = run_compiler_census(names)
    if census_code != 0:
        print("FAIL: compiler declaration census exited nonzero")
        print(census_log[-2000:])
        return 1
    try:
        found_modules, records = parse_compiler_census(census_log)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: could not parse compiler declaration census: {exc}")
        return 1
    expected_modules = set(names)
    for name in sorted(expected_modules - found_modules):
        print(f"FAIL: compiler census did not load package module {name}")
        failures.append(name)
    for name in sorted(found_modules - expected_modules):
        print(f"FAIL: compiler census reported unexpected module {name}")
        failures.append(name)
    compiled = {name: row[2] for name, row in records.items()}
    for name in sorted(set(compiled) - set(reports)):
        print(f"FAIL: compiler declaration {name} has no fresh #print axioms report")
        failures.append(name)
    for name in sorted(set(reports) - set(compiled)):
        print(f"FAIL: fresh #print axioms report {name} is not a compiler declaration")
        failures.append(name)
    for name in sorted(set(reports) & set(compiled)):
        if reports[name] != compiled[name]:
            print(
                f"FAIL: {name} #print axioms {reports[name]} != compiler"
                f" collectAxioms {compiled[name]}"
            )
            failures.append(name)
    census_failures = fwdef_failures(records)
    for line in census_failures:
        print(line)
    failures.extend(census_failures)
    fresh = render(compiled)
    for name, axes in sorted(compiled.items()):
        extra = set(axes) - WHITELIST
        if extra:
            print(f"FAIL: {name} depends on disallowed axioms {sorted(extra)}")
            failures.append(name)
    if regen:
        if failures:
            print("FAIL: refusing to regenerate from an invalid compiler census")
            return 1
        LOG.parent.mkdir(parents=True, exist_ok=True)
        LOG.write_bytes(fresh.encode("utf-8"))
        print(f"regenerated {LOG.name}: {len(compiled)} reports")
        return 0
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
        f"lean audit clean: {len(sources())} sources, {len(compiled)} axiom"
        f" reports ({free} axiom-free), axioms within {sorted(WHITELIST)},"
        f" compiler-censused across {len(modules())} package modules,"
        f" fresh reports and FW-DEF rows exact,"
        f" committed log matches the fresh build"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit this rung's Lean package.")
    parser.add_argument(
        "--regen",
        action="store_true",
        help=(
            "rewrite the committed axiom log after live compiler/report/FW-DEF"
            " and axiom checks; does not validate the receipt being replaced"
        ),
    )
    args = parser.parse_args()
    return audit(args.regen)


if __name__ == "__main__":
    raise SystemExit(main())
