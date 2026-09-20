"""No Lean module name is supplied by two packages inside one research closure.

A research Lake package builds in a workspace made of itself and every
package its ``[[require]]`` entries (``lakefile.toml``) or ``require ... from
"path"`` lines (``lakefile.lean``) reach, transitively: its *require
closure*.  Inside one workspace a module name is resolved by search, so a
name supplied by two packages of the same closure is ambiguous and the
first match wins.  That has already bitten once: a resolver that bound module
names by search path picked a dependency's ``Inventory`` in seven trees,
because ``Inventory`` is supplied by the tree itself and by packages it
requires.

This file is a census of that ambiguity, not a repair of it.  Renaming the
existing ``Inventory`` modules is out of scope: they are pinned across the
chain of trees that consume one another.  The census freezes what exists and
fails when it moves, in either direction.

What the census reads, stated exactly
-------------------------------------

* **Packages** are the directories holding a tracked ``lakefile.toml`` or
  ``lakefile.lean``.  A package is named here by that directory, never by
  its declared ``name``: declared names are not unique (at the pinned
  commit, two trees each carry a root package and a ``lean/`` package under
  one name).
* **Requires** are path requires only.  A require with no path, or a
  ``lakefile.lean`` line this parser does not recognise, is refused by name
  rather than skipped, so an unreadable lakefile cannot shrink the census.
* **Module sets come from tracked ``.lean`` files** under each package's
  source directories: the package ``srcDir`` joined with each library's (or
  executable's) own ``srcDir``.  A tracked lakefile is not a module.  The
  sealed ``lean4`` package therefore supplies ``Derivation``,
  ``Derivation.*`` and ``ParkedAudit``, and a test below holds it to that.
* **Tracked sources only.**  Several trees compile staged copies from a
  gitignored source directory (``sealed/``, ``pinned/``) that a verifier
  fills at run time.  Those directories hold no tracked source, so they
  supply nothing to this census.  The census is over the git index, which is
  also what lets an injection be staged without being committed.

The four assertions
-------------------

1. The set of (colliding name, package context), with the supplying
   packages of each, equals ``PINNED_COLLISIONS``.  A new collision names
   the module and every supplying package; a vanished one names the stale
   pin; a changed supplier set names both sets.
2. Every research verifier that feeds a Lean script beginning ``import
   Inventory`` to the toolchain (all measured ones do so through
   ``--stdin``, where the import resolves by search path) runs in a package
   whose closure has exactly one ``Inventory`` supplier.
3. No tracked module of any package in a research closure imports a name
   that collides in that closure.  This is the Lean-side twin of (2): Lake
   resolves a module's imports across the whole workspace it is built in.
4. The census is not vacuous: it finds research packages, reads the sealed
   package as supplying exactly its own names, and finds ``Inventory``
   suppliers at all.

Updating the pin is a deliberate act.  Removing an entry because a
duplicate package or requirement was deleted is ordinary; adding one means
accepting a new ambiguity and should be argued in the pull request that
does it, not absorbed.

The census is written as functions over a file list and a reader so the
synthetic tests at the bottom can drive it without touching the tree.
"""

from __future__ import annotations

import posixpath
import re
import subprocess
import tomllib
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

Reader = Callable[[str], str]
Collisions = dict[tuple[str, str], tuple[str, ...]]

LAKEFILE_NAMES = ("lakefile.toml", "lakefile.lean")
RESEARCH_PREFIX = "research/"
SEALED_PACKAGE = "lean4"
INVENTORY = "Inventory"


class CensusError(ValueError):
    """A lakefile or verifier the census refuses to guess about."""


@dataclass(frozen=True)
class Package:
    """One Lake package, located by the directory of its lakefile."""

    directory: str
    lakefile: str
    source_dirs: tuple[str, ...]
    requires: tuple[str, ...]


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------


def _resolve(base: str, *parts: str) -> str:
    """Join repo-relative ``base`` with ``parts``; refuse an escape."""
    joined = posixpath.normpath(posixpath.join(base or ".", *parts))
    if joined == ".." or joined.startswith("../") or posixpath.isabs(joined):
        raise CensusError(
            f"path {posixpath.join(base, *parts)!r} leaves the repository"
        )
    return joined


def _under(path: str, directory: str) -> str | None:
    """``path`` relative to ``directory``, or None when it is not under it."""
    if directory == ".":
        return path
    prefix = directory + "/"
    return path[len(prefix):] if path.startswith(prefix) else None


# --------------------------------------------------------------------------
# Lakefiles
# --------------------------------------------------------------------------


def parse_toml_lakefile(path: str, text: str) -> Package:
    """Read the source directories and path requires of a ``lakefile.toml``."""
    directory = posixpath.dirname(path) or "."
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise CensusError(f"{path}: not valid TOML: {exc}") from exc
    package_src = data.get("srcDir", ".")
    if not isinstance(package_src, str):
        raise CensusError(f"{path}: package srcDir is not a string")
    requires: list[str] = []
    for entry in data.get("require", []):
        target = entry.get("path") if isinstance(entry, dict) else None
        if not isinstance(target, str):
            raise CensusError(
                f"{path}: [[require]] {entry!r} has no path; the census "
                "resolves path requires only"
            )
        requires.append(_resolve(directory, target))
    targets = [*data.get("lean_lib", []), *data.get("lean_exe", [])]
    target_srcs: list[str] = []
    for target_table in targets:
        src = target_table.get("srcDir", ".") if isinstance(target_table, dict) else None
        if not isinstance(src, str):
            raise CensusError(f"{path}: target {target_table!r} has no readable srcDir")
        target_srcs.append(src)
    source_dirs = {_resolve(directory, package_src, s) for s in target_srcs or ["."]}
    return Package(directory, path, tuple(sorted(source_dirs)), tuple(requires))


def strip_lean_comments(text: str) -> str:
    """Remove ``--`` line comments and nested ``/- ... -/`` block comments.

    Line breaks inside a block comment are kept, so line structure survives.
    String literals are copied through untouched.
    """
    out: list[str] = []
    i, n, depth, in_string = 0, len(text), 0, False
    while i < n:
        pair = text[i:i + 2]
        char = text[i]
        if depth:
            if pair == "/-":
                depth, i = depth + 1, i + 2
            elif pair == "-/":
                depth, i = depth - 1, i + 2
            else:
                if char == "\n":
                    out.append("\n")
                i += 1
            continue
        if in_string:
            out.append(char)
            if char == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            in_string = char != '"'
            i += 1
            continue
        if pair == "/-":
            depth, i = 1, i + 2
        elif pair == "--":
            newline = text.find("\n", i)
            i = n if newline < 0 else newline
        else:
            in_string = char == '"'
            out.append(char)
            i += 1
    if depth:
        raise CensusError("unterminated block comment")
    return "".join(out)


_ATTRIBUTE = re.compile(r"^@\[[^\]]*\]\s*")
_LEAN_DECLARATIONS = frozenset(
    {"import", "open", "package", "lean_lib", "lean_exe", "require"}
)
_REQUIRE = re.compile(r'^require\s+\S+\s+from\s+"([^"]*)"$')
_SRC_DIR_WORD = re.compile(r"\bsrcDir\b")
_SRC_DIR_LINE = re.compile(r'^srcDir\s*:=\s*"([^"]*)"$')


def _lean_declarations(path: str, text: str) -> list[tuple[str, list[str]]]:
    """Split a ``lakefile.lean`` into (keyword, lines) top-level declarations.

    A declaration starts at a non-blank line in column 0 and takes every
    indented line after it, each stripped.  A leading attribute such as
    ``@[default_target]`` is dropped.  A keyword outside the recognised set
    is refused by name.
    """
    try:
        stripped = strip_lean_comments(text)
    except CensusError as exc:
        raise CensusError(f"{path}: {exc}") from exc
    declarations: list[tuple[str, list[str]]] = []
    for number, line in enumerate(stripped.splitlines(), 1):
        if not line.strip():
            continue
        if line[0].isspace():
            if not declarations:
                raise CensusError(f"{path}:{number}: indented line before any declaration")
            declarations[-1][1].append(line.strip())
            continue
        body = _ATTRIBUTE.sub("", line).strip()
        if not body:
            continue
        keyword = body.split()[0]
        if keyword not in _LEAN_DECLARATIONS:
            raise CensusError(
                f"{path}:{number}: top-level {keyword!r} is not a declaration this "
                "census reads; extend the parser rather than skip it"
            )
        declarations.append((keyword, [body]))
    return declarations


def _src_dir(path: str, lines: Sequence[str]) -> str:
    """The one ``srcDir := "..."`` line of a declaration, or ``"."``.

    Any other line that mentions ``srcDir`` is refused, so a computed or
    inline value cannot be read as the default.
    """
    values: list[str] = []
    for line in lines:
        if _SRC_DIR_WORD.search(line):
            match = _SRC_DIR_LINE.match(line)
            if match is None:
                raise CensusError(f"{path}: cannot read srcDir in {line!r}")
            values.append(match.group(1))
    if len(values) > 1:
        raise CensusError(f"{path}: more than one srcDir in one declaration: {values}")
    return values[0] if values else "."


def parse_lean_lakefile(path: str, text: str) -> Package:
    """Read the source directories and path requires of a ``lakefile.lean``."""
    directory = posixpath.dirname(path) or "."
    package_src = "."
    target_srcs: list[str] = []
    requires: list[str] = []
    for keyword, lines in _lean_declarations(path, text):
        if keyword == "require":
            declaration = " ".join(lines)
            match = _REQUIRE.match(declaration)
            if match is None:
                raise CensusError(
                    f"{path}: {declaration!r} is not `require NAME from \"PATH\"`; "
                    "the census resolves path requires only"
                )
            requires.append(_resolve(directory, match.group(1)))
        elif keyword == "package":
            package_src = _src_dir(path, lines)
        elif keyword in ("lean_lib", "lean_exe"):
            target_srcs.append(_src_dir(path, lines))
    source_dirs = {_resolve(directory, package_src, s) for s in target_srcs or ["."]}
    return Package(directory, path, tuple(sorted(source_dirs)), tuple(requires))


def discover_packages(files: Sequence[str], read: Reader) -> dict[str, Package]:
    """Every package in ``files``, keyed by its directory."""
    by_directory: dict[str, list[str]] = {}
    for path in files:
        if posixpath.basename(path) in LAKEFILE_NAMES:
            by_directory.setdefault(posixpath.dirname(path) or ".", []).append(path)
    packages: dict[str, Package] = {}
    for directory in sorted(by_directory):
        lakefiles = by_directory[directory]
        if len(lakefiles) != 1:
            raise CensusError(f"{directory}: more than one lakefile: {sorted(lakefiles)}")
        lakefile = lakefiles[0]
        parse = parse_toml_lakefile if lakefile.endswith(".toml") else parse_lean_lakefile
        packages[directory] = parse(lakefile, read(lakefile))
    return packages


# --------------------------------------------------------------------------
# Modules and closures
# --------------------------------------------------------------------------


def module_files(package: Package, files: Iterable[str],
                 lakefiles: frozenset[str]) -> dict[str, tuple[str, ...]]:
    """Each module name the package supplies, with the tracked files behind it."""
    found: dict[str, set[str]] = {}
    for path in files:
        if not path.endswith(".lean") or path in lakefiles:
            continue
        for source_dir in package.source_dirs:
            relative = _under(path, source_dir)
            if relative is not None:
                name = relative[: -len(".lean")].replace("/", ".")
                found.setdefault(name, set()).add(path)
    return {name: tuple(sorted(paths)) for name, paths in sorted(found.items())}


def require_closure(start: str, packages: Mapping[str, Package]) -> tuple[str, ...]:
    """``start`` and every package its requires reach, sorted."""
    seen = {start}
    pending = [start]
    while pending:
        current = packages[pending.pop()]
        for target in current.requires:
            if target not in packages:
                raise CensusError(
                    f"{current.lakefile} requires {target!r}, which holds no tracked lakefile"
                )
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return tuple(sorted(seen))


@dataclass(frozen=True)
class Census:
    """Packages, their module files, and the research contexts."""

    packages: dict[str, Package]
    modules: dict[str, dict[str, tuple[str, ...]]]
    contexts: tuple[str, ...]

    def closure(self, context: str) -> tuple[str, ...]:
        return require_closure(context, self.packages)

    def suppliers(self, context: str) -> dict[str, tuple[str, ...]]:
        """Each module name in the closure of ``context``, with its packages."""
        found: dict[str, list[str]] = {}
        for member in self.closure(context):
            for name in self.modules[member]:
                found.setdefault(name, []).append(member)
        return {name: tuple(sorted(who)) for name, who in sorted(found.items())}


def take_census(files: Sequence[str], read: Reader) -> Census:
    """The whole census over ``files``, reading lakefiles through ``read``."""
    packages = discover_packages(files, read)
    lakefiles = frozenset(p.lakefile for p in packages.values())
    modules = {d: module_files(p, files, lakefiles) for d, p in packages.items()}
    contexts = tuple(d for d in sorted(packages) if d.startswith(RESEARCH_PREFIX))
    return Census(packages, modules, contexts)


def collisions(census: Census) -> Collisions:
    """Every (name, context) whose name more than one closure member supplies."""
    found: Collisions = {}
    for context in census.contexts:
        for name, who in census.suppliers(context).items():
            if len(who) > 1:
                found[(name, context)] = who
    return found


def pin_problems(computed: Mapping[tuple[str, str], tuple[str, ...]],
                 pinned: Mapping[tuple[str, str], tuple[str, ...]]) -> list[str]:
    """Named differences between a computed collision set and its pin."""
    problems: list[str] = []
    for key in sorted(set(computed) | set(pinned)):
        name, context = key
        now, then = computed.get(key), pinned.get(key)
        if then is None and now is not None:
            problems.append(
                f"NEW COLLISION: module {name!r} is supplied by {len(now)} packages "
                f"in the require closure of {context}: {', '.join(now)}"
            )
        elif now is None and then is not None:
            problems.append(
                f"STALE PIN: module {name!r} no longer collides in the require "
                f"closure of {context} (pinned suppliers: {', '.join(then)}); "
                "remove the entry from PINNED_COLLISIONS"
            )
        elif now != then and now is not None and then is not None:
            problems.append(
                f"SUPPLIERS CHANGED: module {name!r} in the require closure of "
                f"{context}: now {', '.join(now)}; pinned {', '.join(then)}"
            )
    return problems


# --------------------------------------------------------------------------
# Imports: verifier scripts and tracked modules
# --------------------------------------------------------------------------

_INVENTORY_SCRIPT = re.compile(r"""["']import Inventory\b""")
_ROOT_BINDING = re.compile(r"^ROOT\s*=\s*Path\(__file__\)\.resolve\(\)\.parent\s*$", re.M)
_LEAN_DIR_BINDING = re.compile(r'^LEAN_DIR\s*=\s*ROOT\s*/\s*"([^"]+)"\s*$', re.M)
_CWD_LEAN_DIR = re.compile(r"\bcwd\s*=\s*LEAN_DIR\b")


def inventory_feeders(files: Sequence[str],
                      read: Reader) -> tuple[dict[str, str], list[str]]:
    """Research Python sources that build a Lean script importing Inventory.

    Returns the ones whose package can be bound (source -> package
    directory) and the ones that cannot.  A binding needs ``ROOT =
    Path(__file__).resolve().parent``, exactly one ``LEAN_DIR = ROOT /
    "<dir>"``, and ``cwd=LEAN_DIR``; anything else is reported, not guessed.
    """
    bound: dict[str, str] = {}
    unbound: list[str] = []
    for path in files:
        if not (path.startswith(RESEARCH_PREFIX) and path.endswith(".py")):
            continue
        text = read(path)
        if not _INVENTORY_SCRIPT.search(text):
            continue
        lean_dirs = _LEAN_DIR_BINDING.findall(text)
        if (_ROOT_BINDING.search(text) is None or len(lean_dirs) != 1
                or _CWD_LEAN_DIR.search(text) is None):
            unbound.append(path)
            continue
        bound[path] = _resolve(posixpath.dirname(path), lean_dirs[0])
    return bound, unbound


_HEADER_IMPORT = re.compile(
    r"(?:(?:public|private|meta)\s+)*import\s+(?:all\s+)?([^\s]+)"
)
_HEADER_KEYWORD = re.compile(r"(?:module|prelude)(?=\s|$)")


def header_imports(text: str) -> tuple[str, ...]:
    """The module names a Lean file's header imports, in order.

    Lean requires every import before any other command, so the header is
    read directly: whitespace and comments are skipped, ``module`` and
    ``prelude`` are passed over, and reading stops at the first command
    that is not an import.
    """
    names: list[str] = []
    i, n = (1 if text.startswith("\ufeff") else 0), len(text)
    while i < n:
        if text[i].isspace():
            i += 1
        elif text.startswith("--", i):
            newline = text.find("\n", i)
            i = n if newline < 0 else newline
        elif text.startswith("/-", i):
            depth, i = 1, i + 2
            while i < n and depth:
                if text.startswith("/-", i):
                    depth, i = depth + 1, i + 2
                elif text.startswith("-/", i):
                    depth, i = depth - 1, i + 2
                else:
                    i += 1
        elif (keyword := _HEADER_KEYWORD.match(text, i)) is not None:
            i = keyword.end()
        elif (imported := _HEADER_IMPORT.match(text, i)) is not None:
            names.append(imported.group(1))
            i = imported.end()
        else:
            break
    return tuple(names)


def colliding_imports(census: Census, found: Mapping[tuple[str, str], tuple[str, ...]],
                      read: Reader) -> list[str]:
    """Tracked modules that import a name colliding in a closure they build in."""
    by_context: dict[str, set[str]] = {}
    for name, context in found:
        by_context.setdefault(context, set()).add(name)
    problems: list[str] = []
    headers: dict[str, tuple[str, ...]] = {}
    for context in sorted(by_context):
        names = by_context[context]
        for member in census.closure(context):
            for paths in census.modules[member].values():
                for path in paths:
                    if path not in headers:
                        headers[path] = header_imports(read(path))
                    for imported in headers[path]:
                        if imported in names:
                            who = found[(imported, context)]
                            problems.append(
                                f"{path} imports {imported!r}, which the require "
                                f"closure of {context} takes from {len(who)} "
                                f"packages: {', '.join(who)}"
                            )
    return sorted(set(problems))


# --------------------------------------------------------------------------
# The tracked tree
# --------------------------------------------------------------------------


def tracked_files(repo: Path) -> list[str]:
    """Every path in the git index, slash-separated."""
    raw = subprocess.run(
        ["git", "ls-files", "-z"], cwd=repo, capture_output=True, check=True
    ).stdout
    return [p.replace("\\", "/") for p in raw.decode("utf-8").split("\0") if p]


def worktree_reader(repo: Path) -> Reader:
    def read(path: str) -> str:
        return (repo / path).read_text(encoding="utf-8")
    return read


# Computed by take_census/collisions over the index at
# 827bf9834e7aaafa2b3d52c7b88bc4c781124829: one colliding name, ten contexts.
# 2026-09-19: the duplicate m105 root package was removed; nine remain.
PINNED_COLLISIONS: dict[tuple[str, str], tuple[str, ...]] = {
    ("Inventory", "research/coherent_process_limits/lean"): (
        "research/coherent_process_limits/lean",
        "research/ignition/lean",
        "research/local_reuse/lean",
        "research/magnification/lean",
        "research/represented_execution/lean",
        "research/setting_translation/lean",
    ),
    ("Inventory", "research/ignition/lean"): (
        "research/ignition/lean",
        "research/local_reuse/lean",
    ),
    ("Inventory", "research/instance_demand/lean"): (
        "research/ignition/lean",
        "research/instance_demand/lean",
        "research/local_reuse/lean",
        "research/magnification/lean",
        "research/represented_execution/lean",
        "research/setting_translation/lean",
    ),
    ("Inventory", "research/m105_number_tower/lean"): (
        "research/g011_finitary_substrate/lean",
        "research/m105_number_tower/lean",
    ),
    ("Inventory", "research/magnification/lean"): (
        "research/ignition/lean",
        "research/local_reuse/lean",
        "research/magnification/lean",
    ),
    ("Inventory", "research/record_reading/lean"): (
        "research/coherent_process_limits/lean",
        "research/ignition/lean",
        "research/local_reuse/lean",
        "research/magnification/lean",
        "research/record_reading/lean",
        "research/represented_execution/lean",
        "research/setting_translation/lean",
    ),
    ("Inventory", "research/represented_execution/lean"): (
        "research/ignition/lean",
        "research/local_reuse/lean",
        "research/magnification/lean",
        "research/represented_execution/lean",
        "research/setting_translation/lean",
    ),
    ("Inventory", "research/setting_translation/lean"): (
        "research/ignition/lean",
        "research/local_reuse/lean",
        "research/magnification/lean",
        "research/setting_translation/lean",
    ),
    ("Inventory", "research/unboundedness/lean"): (
        "research/coherent_process_limits/lean",
        "research/ignition/lean",
        "research/local_reuse/lean",
        "research/magnification/lean",
        "research/represented_execution/lean",
        "research/setting_translation/lean",
        "research/unboundedness/lean",
    ),
}


@pytest.fixture(scope="module")
def tree() -> tuple[list[str], Reader, Census]:
    files = tracked_files(REPO)
    read = worktree_reader(REPO)
    return files, read, take_census(files, read)


def test_census_is_not_vacuous(tree: tuple[list[str], Reader, Census]) -> None:
    _, _, census = tree
    assert census.contexts, "the census found no research Lake package"
    sealed = set(census.modules[SEALED_PACKAGE])
    assert {"Derivation", "ParkedAudit"} <= sealed
    strays = sorted(
        n for n in sealed
        if n not in ("Derivation", "ParkedAudit") and not n.startswith("Derivation.")
    )
    assert strays == [], f"the sealed package supplies unexpected names: {strays}"
    suppliers = [d for d in census.contexts if INVENTORY in census.modules[d]]
    assert suppliers, "no research package supplies Inventory; the census reads nothing"


def test_collisions_match_the_pin(tree: tuple[list[str], Reader, Census]) -> None:
    _, _, census = tree
    problems = pin_problems(collisions(census), PINNED_COLLISIONS)
    assert not problems, "\n".join(problems)


def test_stdin_inventory_verifiers_see_one_supplier(
    tree: tuple[list[str], Reader, Census],
) -> None:
    files, read, census = tree
    bound, unbound = inventory_feeders(files, read)
    problems = [
        f"{path} feeds `import Inventory` to Lean but its package cannot be bound"
        for path in unbound
    ]
    assert bound or unbound, "no research verifier feeds `import Inventory`; recheck the pattern"
    for path, package in sorted(bound.items()):
        if package not in census.packages:
            problems.append(f"{path} runs in {package}, which holds no tracked lakefile")
            continue
        who = census.suppliers(package).get(INVENTORY, ())
        if len(who) != 1:
            problems.append(
                f"{path} feeds `import Inventory` in {package}, whose require "
                f"closure has {len(who)} Inventory suppliers: {', '.join(who) or 'none'}"
            )
    assert not problems, "\n".join(problems)


def test_no_tracked_module_imports_a_colliding_name(
    tree: tuple[list[str], Reader, Census],
) -> None:
    _, read, census = tree
    problems = colliding_imports(census, collisions(census), read)
    assert not problems, "\n".join(problems)


# --------------------------------------------------------------------------
# Synthetic fixtures: the census functions on trees that do not exist
# --------------------------------------------------------------------------


def _fixture(files: Mapping[str, str]) -> tuple[list[str], Reader]:
    def read(path: str) -> str:
        return files[path]
    return sorted(files), read


_BASE_TOML = 'name = "base"\n[[lean_lib]]\nname = "Base"\n[[lean_lib]]\nname = "Inventory"\n'
_TOP_TOML = (
    'name = "top"\n[[require]]\nname = "base"\npath = "../base"\n'
    '[[lean_lib]]\nname = "Top"\n[[lean_lib]]\nname = "Inventory"\n'
)


def test_synthetic_toml_reads_package_and_target_source_dirs() -> None:
    package = parse_toml_lakefile(
        "research/t/lakefile.toml",
        'name = "t"\nsrcDir = "lean"\n[[require]]\nname = "d"\npath = "../../lean4"\n'
        '[[lean_lib]]\nname = "A"\n[[lean_lib]]\nname = "B"\nsrcDir = "extra"\n',
    )
    assert package.source_dirs == ("research/t/lean", "research/t/lean/extra")
    assert package.requires == ("lean4",)


def test_synthetic_toml_refuses_a_require_without_a_path() -> None:
    with pytest.raises(CensusError, match="has no path"):
        parse_toml_lakefile("research/t/lakefile.toml", '[[require]]\nname = "x"\n')


def test_synthetic_lean_lakefile_ignores_comments_and_reads_blocks() -> None:
    text = (
        "import Lake\nopen Lake DSL\n\npackage p\n\n"
        '/-\nrequire ghost from "../../nowhere"\n-/\n'
        'require derivation from "../../../lean4" -- the sealed package\n\n'
        'lean_lib Derivation where\n  srcDir := "sealed"\n  roots := #[`Derivation.PrimDiff]\n\n'
        "@[default_target]\nlean_lib P where\n  roots := #[`P]\n"
    )
    package = parse_lean_lakefile("research/p/lean/lakefile.lean", text)
    assert package.requires == ("lean4",)
    assert package.source_dirs == ("research/p/lean", "research/p/lean/sealed")


def test_synthetic_lean_lakefile_refuses_what_it_cannot_read() -> None:
    with pytest.raises(CensusError, match="not a declaration this census reads"):
        parse_lean_lakefile("research/p/lakefile.lean", "package p\ntarget t : Unit := pure ()\n")
    with pytest.raises(CensusError, match="path requires only"):
        parse_lean_lakefile("research/p/lakefile.lean", 'require x from git "u" @ "main"\n')
    with pytest.raises(CensusError, match="cannot read srcDir"):
        parse_lean_lakefile("research/p/lakefile.lean", 'lean_lib L where\n  srcDir := "a" / "b"\n')
    with pytest.raises(CensusError, match="unterminated"):
        parse_lean_lakefile("research/p/lakefile.lean", "/- open\npackage p\n")


def test_synthetic_require_to_an_untracked_directory_is_refused() -> None:
    files, read = _fixture({"research/top/lakefile.toml": _TOP_TOML})
    census = take_census(files, read)
    with pytest.raises(CensusError, match="holds no tracked lakefile"):
        collisions(census)


def test_synthetic_escape_from_the_repository_is_refused() -> None:
    with pytest.raises(CensusError, match="leaves the repository"):
        parse_toml_lakefile("lakefile.toml", '[[require]]\nname = "x"\npath = "../x"\n')


def test_synthetic_collision_names_the_module_and_every_supplier() -> None:
    files, read = _fixture({
        "research/base/lakefile.toml": _BASE_TOML,
        "research/base/Base.lean": "",
        "research/base/Inventory.lean": "import Base\n",
        "research/top/lakefile.toml": _TOP_TOML,
        "research/top/Top.lean": "import Base\n",
        "research/top/Inventory.lean": "import Top\n",
        "research/lone/lakefile.lean": "package lone\nlean_lib Lone\n",
        "research/lone/Lone.lean": "",
    })
    census = take_census(files, read)
    found = collisions(census)
    assert found == {("Inventory", "research/top"): ("research/base", "research/top")}
    problems = pin_problems(found, {})
    assert problems == [
        "NEW COLLISION: module 'Inventory' is supplied by 2 packages in the require "
        "closure of research/top: research/base, research/top"
    ]
    assert colliding_imports(census, found, read) == []


def test_synthetic_pin_fails_in_both_directions_and_on_changed_suppliers() -> None:
    key = ("Inventory", "research/top")
    stale = pin_problems({}, {key: ("research/a", "research/b")})
    assert len(stale) == 1 and stale[0].startswith("STALE PIN: module 'Inventory'")
    assert "research/top" in stale[0] and "research/a, research/b" in stale[0]
    moved = pin_problems({key: ("research/a", "research/c")}, {key: ("research/a", "research/b")})
    assert len(moved) == 1 and moved[0].startswith("SUPPLIERS CHANGED")
    assert pin_problems({key: ("research/a",)}, {key: ("research/a",)}) == []


def test_synthetic_module_importing_a_colliding_name_is_named() -> None:
    files, read = _fixture({
        "research/base/lakefile.toml": _BASE_TOML,
        "research/base/Base.lean": "/- header -/\n-- note\nimport Inventory\n",
        "research/base/Inventory.lean": "",
        "research/top/lakefile.toml": _TOP_TOML,
        "research/top/Top.lean": "",
        "research/top/Inventory.lean": "",
    })
    census = take_census(files, read)
    problems = colliding_imports(census, collisions(census), read)
    assert problems == [
        "research/base/Base.lean imports 'Inventory', which the require closure of "
        "research/top takes from 2 packages: research/base, research/top"
    ]


def test_synthetic_header_stops_at_the_first_command() -> None:
    text = (
        "module\n/- a /- nested -/ comment -/\npublic import A.B\n"
        "import all C\n-- import D\ndef x := 1\nimport E\n"
    )
    assert header_imports(text) == ("A.B", "C")


def test_synthetic_feeders_bind_their_package_or_are_reported() -> None:
    bound_text = (
        'ROOT = Path(__file__).resolve().parent\nLEAN_DIR = ROOT / "lean"\n'
        'script = "import Inventory\\n"\nrun(["lake", "env", "lean", "--stdin"], cwd=LEAN_DIR)\n'
    )
    files, read = _fixture({
        "research/top/verify.py": bound_text,
        "research/odd/verify.py": 'script = "import Inventory\\n"\n',
        "research/quiet/verify.py": 'script = "import Other\\n"\n',
        "tests/verify.py": bound_text,
    })
    bound, unbound = inventory_feeders(files, read)
    assert bound == {"research/top/verify.py": "research/top/lean"}
    assert unbound == ["research/odd/verify.py"]
