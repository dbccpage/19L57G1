"""Rebuild this tree's Lean package from clean and compare the axiom reports.

Run from inside ``research/limit_and_observer``:

    python verify_lean.py

It rebuilds, scans every ``.lean`` file as plain text for the forbidden
tokens, checks that every module of the package is inside the census root's
import closure, requires every axiom report to lie within
``{propext, Quot.sound}``, and compares the whole report block byte for byte
against ``receipts/lean_axioms.txt``.

The closure check is here rather than in Lean for the reason the sealed tree
measured: a module that **nothing** imports is absent from the compiled
environment, so the in-Lean census in ``lean/LimitObserver/AxiomReport.lean``
cannot see that it is missing.  This half reads the source tree instead.

**This is a MANUAL receipt.** No CI gate runs this package's verifier.
A pass here is evidence a person ran
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
REPORT = re.compile(r"'(.+?)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)")
DECLARATION = re.compile(r"LIMIT_OBSERVER_DECL ([^\r\n]+)")

#: The module whose import closure must cover the package.  It is the census
#: root: ``lean/LimitObserver/AxiomReport.lean`` reports theorems declared in
#: LimitObserver only. Other library modules are refused even if imported.
CENSUS_ROOT = "LimitObserver.AxiomReport"

#: No ``$`` anchor: a trailing comment is blanked to spaces by
#: ``strip_lean_comments``, and requiring end-of-line would reject that legal
#: form.  The same shape as ``ci/check_parked_audit.py``'s, pinned there.
IMPORT = re.compile(
    r"^import[ \t]+(LimitObserver(?:\.[A-Za-z0-9_']+)*)[ \t]*(?=\n|$)", re.M
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def strip_lean_comments(text: str) -> str:
    """Blank out Lean comments, preserving line structure.

    Newlines are kept so that ``^import`` still anchors on the lines that
    survive.  Block comments nest in Lean, so the depth is counted rather than
    matched with a non-greedy regex.  Without this, a doc-string line wrapping
    onto a column-0 ``import`` would make an unreachable module look reachable
    — the silent failure mode ``CLAUDE.md`` records for text-based Lean
    censuses.  Taken from ``ci/check_parked_audit.py``, pinned in
    ``SOURCE_MANIFEST.json``.
    """
    out: list[str] = []
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if text.startswith("-/", i) and depth:
            depth -= 1
            i += 2
            continue
        ch = text[i]
        if depth:
            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue
        if text.startswith("--", i):
            j = text.find("\n", i)
            if j == -1:
                break
            out.append(" " * (j - i))
            i = j
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def module_name(path: str) -> str:
    rel = os.path.relpath(path, LEAN)
    return rel[: -len(".lean")].replace(os.sep, ".").replace("/", ".")


def module_census(sources: list[str]) -> dict[str, str]:
    """Every module file of the package, by module name.

    ``lakefile.lean`` is Lake's own configuration and declares no
    mathematics, so it is not a module of the library."""
    return {
        module_name(p): p
        for p in sources
        if os.path.basename(p) != "lakefile.lean"
    }


def check_import_closure(sources: list[str]) -> int:
    """Every module of the package is reached by the census root.

    Returns the number of modules in the closure.  A module outside it is
    never elaborated into the census's environment, so its theorems emit no
    report and its axioms go uninspected — with the forbidden-token scan and
    the receipt comparison both green."""
    census = module_census(sources)
    if CENSUS_ROOT not in census:
        fail(f"the census root {CENSUS_ROOT} is not a module of the package")
    reached = {CENSUS_ROOT}
    stack = [CENSUS_ROOT]
    while stack:
        name = stack.pop()
        with open(census[name], encoding="utf-8") as fh:
            text = strip_lean_comments(fh.read())
        for dep in IMPORT.findall(text):
            if dep in census and dep not in reached:
                reached.add(dep)
                stack.append(dep)
    for name in sorted(census):
        if name not in reached:
            fail(
                f"{name} is outside {CENSUS_ROOT}'s import closure, so no "
                f"axiom report is emitted for it; import it there"
            )
    unexpected = sorted(set(census) - {CENSUS_ROOT, "LimitObserver"})
    if unexpected:
        fail(f"modules outside the declared theorem census: {unexpected}; "
             "import closure alone does not extend the axiom census")
    return len(reached)


def parse_reports(log: str) -> list[str]:
    """Compare the independently emitted name population with parsed reports."""
    population = DECLARATION.findall(log)
    matches = list(REPORT.finditer(log))
    names = [m.group(1) for m in matches]
    if not population:
        raise ValueError("no LIMIT_OBSERVER_DECL population in the build log")
    if len(population) != len(set(population)) or len(names) != len(set(names)):
        raise ValueError("duplicate declaration or axiom report in the build log")
    if set(population) != set(names):
        raise ValueError(
            f"axiom report population mismatch: missing={sorted(set(population) - set(names))}, "
            f"unexpected={sorted(set(names) - set(population))}"
        )
    reports = []
    for m in matches:
        name, raw = m.group(1), m.group(2)
        axioms = sorted(a.strip() for a in raw.split(",") if a.strip()) if raw else []
        bad = set(axioms) - ALLOWED_AXIOMS
        if bad:
            raise ValueError(f"disallowed axioms {sorted(bad)} in {name}")
        reports.append(f"{name}: {axioms}")
    return sorted(reports)


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

    modules = check_import_closure(sorted(sources))

    clean = subprocess.run(["lake", "clean"], cwd=LEAN, capture_output=True, text=True)
    if clean.returncode != 0:
        fail(f"lake clean failed: {clean.stdout}{clean.stderr}")
    build = subprocess.run(
        ["lake", "build"], cwd=LEAN, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True,
    )
    log = build.stdout
    if build.returncode != 0:
        print(log)
        fail("lake build failed")

    try:
        reports = parse_reports(log)
    except ValueError as error:
        fail(str(error))

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
        f"{modules} modules in the census root's import closure, "
        f"{len(reports)} axiom reports, axioms within "
        f"{sorted(ALLOWED_AXIOMS)}  [MANUAL RECEIPT: no gate reads this]"
    )


if __name__ == "__main__":
    main(write="--write" in sys.argv)
