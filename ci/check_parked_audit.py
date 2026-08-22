"""Every module outside the root's import closure is named for audit.

Usage: python ci/check_parked_audit.py

``lean4/ParkedAudit.lean`` emits a ``#print axioms`` report for each theorem
of the modules ``lean4/Derivation.lean`` does not import.  Its own list is
checked against the compiled environment at build time, but that check has a
blind spot it cannot fix from inside Lean: a module that NOTHING imports is
absent from the environment altogether, so Lean cannot notice it is missing.

That is precisely the case this gate covers.  Adding a new parked module
fails the `elaborated_modules.txt` census pin, which names it -- but the
documented repair for that failure is to regenerate the pin, and a
regeneration alone would leave the module elaborated, pinned, and still
unaudited.  Here the population is enumerated from the source tree instead,
so the parked set is complete by construction rather than by maintenance.

Three sets, compared:

* census   -- every ``lean4/Derivation/**/*.lean``, as module names
* closure  -- the transitive import closure of ``lean4/Derivation.lean``
* declared -- the ``parkedModules`` array in ``lean4/ParkedAudit.lean``

``census - closure`` must equal ``declared``.

Imports are read as text, which is safe in a way a theorem census is not: an
``import`` must be the first token of a line and cannot be wrapped, commented
into existence, or spelled inside a doc-string in a way Lean would accept.
The failure that motivated the environment-based theorem census -- a
doc-string line beginning with the word ``theorem`` -- has no analogue here.
"""

from __future__ import annotations

import pathlib
import re
import sys

LEAN = pathlib.Path("lean4")
ROOT_MODULE = "Derivation"
IMPORT = re.compile(r"^import[ \t]+(Derivation(?:\.[A-Za-z0-9_']+)*)[ \t]*$",
                    re.MULTILINE)
PARKED_ENTRY = re.compile(r"`(Derivation(?:\.[A-Za-z0-9_']+)+)")


def module_path(name: str) -> pathlib.Path:
    return LEAN / (name.replace(".", "/") + ".lean")


def imports_of(name: str) -> list[str]:
    path = module_path(name)
    if not path.exists():
        return []
    return IMPORT.findall(path.read_text(encoding="utf-8"))


def closure_of(root: str) -> set[str]:
    """Transitive import closure, root included."""
    seen: set[str] = {root}
    stack = [root]
    while stack:
        for dep in imports_of(stack.pop()):
            if dep not in seen:
                seen.add(dep)
                stack.append(dep)
    return seen


def declared_parked() -> set[str]:
    text = (LEAN / "ParkedAudit.lean").read_text(encoding="utf-8")
    m = re.search(r"def parkedModules[^#]*#\[(?P<body>.*?)\]", text, re.DOTALL)
    if m is None:
        print("FAIL: could not find `parkedModules` in lean4/ParkedAudit.lean")
        sys.exit(1)
    return set(PARKED_ENTRY.findall(m.group("body")))


def main() -> int:
    census = {
        ".".join(p.relative_to(LEAN).with_suffix("").parts)
        for p in (LEAN / ROOT_MODULE).rglob("*.lean")
    }
    if not census:
        print("FAIL: census enumerated no modules - the enumeration is broken")
        return 1

    closure = closure_of(ROOT_MODULE)
    expected = census - closure
    declared = declared_parked()

    failures = []
    for name in sorted(expected - declared):
        failures.append(
            f"{name} is outside {ROOT_MODULE}.lean's import closure but is "
            f"not named in lean4/ParkedAudit.lean, so no axiom report covers it"
        )
    for name in sorted(declared - expected):
        failures.append(
            f"{name} is named in lean4/ParkedAudit.lean but IS inside "
            f"{ROOT_MODULE}.lean's import closure; remove it there"
        )

    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        print(
            "  after editing lean4/ParkedAudit.lean, rebuild and regenerate "
            "artifacts/lean_axioms.txt"
        )
        return 1

    print(
        f"parked audit complete: {len(census)} modules, "
        f"{len(closure & census)} in the root's closure, "
        f"{len(expected)} parked and all named for audit"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
