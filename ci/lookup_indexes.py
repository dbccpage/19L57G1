"""Generate two lookup indexes under ``docs/index/``.

``docs/index/topics.md`` answers *topic -> files*.  The population is every
``code/run_*.py`` directly under ``code/`` in the git index, the same glob
the runner census uses.  For each runner stem it names the five files of
the family pattern that exist (``code/derivation/<topic>.py``,
``code/run_<topic>.py``, ``tests/test_<topic>.py``,
``lean4/Derivation/<Topic>.lean``, ``artifacts/<topic>.json``), then, read
from the runner's syntax tree, the ``derivation`` modules and sibling
runners it imports, the root tests that import it, and the committed
artifacts its source names.  ``<Topic>`` is the stem's underscore-separated
words, each capitalized and joined; when no tracked file has that exact
name but one differs from it only in letter case, that file is the member
and the cell says ``case differs``.

``docs/index/pins.md`` answers *path -> the research trees that pin it*.
The population of pin files is every tracked file under ``research/<tree>/``
whose name is capital letters, digits and underscores ending in
``MANIFEST.json``, ``PIN.json`` or ``PINS.json``, outside the directories
``ci/research_index.py`` does not count as trees.  Each file is parsed as
JSON and every string in it, key or value, is located by its field path.
``PIN_FIELDS`` names the field paths that record a pin and of what kind;
``NOT_PIN_FIELDS`` names the ones that mention a path without pinning it,
and why.  A string that names a path at a field path listed in neither
table fails generation by file, field and value, so a new manifest shape
cannot be indexed by guesswork or dropped in silence.  A ``tree`` pin
records one Git tree object; it is expanded to every tracked file under
that directory, because the tree verifiers diff the whole directory
against their baseline.  Paths inside ``prompt/``, ``paper/``, ``code/``,
``lean4/Derivation/``, ``artifacts/`` and the file ``lean4/Derivation.lean``
are listed as sealed; every other pinned path is listed too, separately.

Scope pins live in no pin file, so they are read from the syntax tree of
every tracked ``verify*.py`` at the top level of a tree: a module-level
tuple or list of strings passed starred (``*NAME``) to a call whose other
positional arguments include the string ``diff`` or ``log``.  That is a
verifier asking git whether anything under those pathspecs changed since
the commit it trusts, so every tracked path under them is pinned by that
tree.  The same tuple used only with ``status`` or a prefix test is a
cleanliness or write-scope check and pins nothing.  On 2026-09-18 a probe
change to one parked module and one kernel module, each run through every
``verify_sources.py``, ``verify_pins.py`` and ``verify_manifest.py``, failed
no verifier of a tree this index leaves out; without scope pins it failed
six.

What the index does not decide: whether a verifier compares a file pin
with the current file or only with the commit its pin file names.  Run the
verifier to know.  Digests written into Python source rather than a pin
file are not read.

Neither file carries a total: two branches that each add a row would both
rewrite a total line, and git could merge them into a wrong one.
``--summary`` prints the totals from the current tree instead.

Inputs: the path list comes from the git index; runner, test, pin-file
and verifier contents are read from the working tree.  The generator writes only the
two files under ``docs/index/`` and refuses any output path inside the
sealed directories.

``--check`` exits 1 and names each stale file; ``--write`` rewrites both
with LF line endings; ``--who-pins PATH ...`` prints the pin rows for the
paths given (a path ending in ``/`` selects every row under it), computed
from the working tree, so a change can be priced before the pull request.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import fnmatch
import importlib.util
import json
import posixpath
import re
import subprocess
import sys
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

REPO = Path(__file__).resolve().parent.parent
TOPICS_REL = "docs/index/topics.md"
PINS_REL = "docs/index/pins.md"
OUTPUTS = (TOPICS_REL, PINS_REL)
REGENERATE = "python ci/lookup_indexes.py --write"

SEALED_PREFIXES = ("prompt/", "paper/", "code/", "lean4/Derivation/", "artifacts/")
SEALED_FILES = frozenset({"lean4/Derivation.lean"})

PIN_FILE_NAME = re.compile(r"^[A-Z0-9_]*(?:MANIFEST|PIN|PINS)\.json$")

# Markers inside a field path.  KEY: this string is itself a dict key.
# ANY: any dict key at this position.  ITEM: any list element.
KEY = "<key>"
ANY = "<any>"
ITEM = "[]"

Shape = tuple[str, ...]


@dataclass(frozen=True)
class PinField:
    """One field path that records a pin: its kind, and what it is relative to."""

    kind: str
    relative_to_tree: bool = False


# Kinds: ``tree`` a Git tree object; ``file`` a digest or the exact content
# of one file; ``span`` a digest of a line span; ``copy`` the source a
# vendored copy was taken from; ``reconstruction`` the source of a
# reconstructed line range.
PIN_FIELDS: Mapping[Shape, PinField] = {
    ("consumed_trees", KEY): PinField("tree"),
    ("source_package", "path"): PinField("tree"),
    ("sources", ITEM, "path"): PinField("file"),
    ("sources", KEY): PinField("file"),
    ("pins", KEY): PinField("file"),
    ("source_sha256", KEY): PinField("file"),
    ("artifact_sha256", KEY): PinField("file"),
    ("modules", ITEM, "path"): PinField("file"),
    ("modules", ANY, "path"): PinField("file"),
    ("frozen_texts", ITEM, "path"): PinField("file"),
    ("frozen", KEY): PinField("file"),
    ("artifacts", ITEM, "path"): PinField("file"),
    ("toolchains", KEY): PinField("file"),
    ("status_inputs", ITEM, "path"): PinField("file"),
    ("landed_replay", "sources", ITEM, "path"): PinField("file"),
    ("prompt", "path"): PinField("file"),
    ("vendored_receipts", ITEM, "local_path"): PinField("file", relative_to_tree=True),
    ("vendored", "local_path"): PinField("file", relative_to_tree=True),
    ("spans", ITEM, "path"): PinField("span"),
    ("reconstructions", ITEM, "source_path"): PinField("reconstruction"),
    ("vendored_receipts", ITEM, "source_path"): PinField("copy"),
    ("vendored_blob", "source_path"): PinField("copy"),
    ("source_path",): PinField("copy"),
}

NOT_PIN_FIELDS: Mapping[Shape, str] = {
    ("tree_census", KEY): "the census of a tree pin; the tree pin itself is expanded",
    ("tree_census", ANY, ITEM): "the census of a tree pin; the tree pin itself is expanded",
    ("runtime_modules", ANY): "where a module must be imported from, not a digest",
    ("runtime_modules", ITEM, "path"): "where a module must be imported from, not a digest",
    ("what_each_pin_is_for", KEY): "prose about the pins recorded under pins",
    ("absent_at_snapshot", ITEM, "path"): "declared absent at the snapshot",
    ("carve", "allowed_paths", ITEM): "a write scope",
    ("write_root",): "a write scope",
    ("authorized_imports", KEY): "import authority of the tree's own files",
    ("package_files", ITEM): "the census of the tree's own package",
    ("exports", ITEM, "module"): "names a module that modules pins",
    ("lean_source", "path"): "the tree's own Lean source and its declared imports",
    ("reconstructions", ITEM, "local_path"): "the tree's own reconstruction target",
    ("vendored_blob", "local_path"): "names the copy that vendored_receipts pins",
}

KIND_ORDER = ("tree", "file", "span", "copy", "reconstruction")

ARTIFACT_SUFFIXES = (".json", ".json.gz", ".txt")

SCOPE_VERBS = frozenset({"diff", "log"})

ROLES: tuple[tuple[str, str], ...] = (
    ("computation", "code/derivation/"),
    ("runner", "code/"),
    ("tests", "tests/"),
    ("proofs", "lean4/Derivation/"),
    ("output", "artifacts/"),
)


def is_sealed(path: str) -> bool:
    """Whether a repository-relative path lies inside the sealed derivation."""
    return path in SEALED_FILES or path.startswith(SEALED_PREFIXES)


def _git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", *args], cwd=repo, capture_output=True, check=False
    )
    if result.returncode != 0:
        reason = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {reason}")
    return result.stdout


def tracked_files(repo: Path) -> list[str]:
    """Every path in the git index, sorted by code point."""
    raw = _git(repo, "ls-files", "-z")
    return sorted(p for p in raw.decode("utf-8").split("\0") if p)


def _read_text(repo: Path, rel: str) -> str:
    """UTF-8, a leading byte-order mark dropped, CRLF read as LF."""
    return (repo / rel).read_bytes().decode("utf-8-sig").replace("\r\n", "\n")


def _load_research_index() -> ModuleType:
    path = Path(__file__).resolve().parent / "research_index.py"
    spec = importlib.util.spec_from_file_location("_lookup_research_index", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tree_of(path: str, not_trees: Mapping[str, str]) -> str | None:
    parts = path.split("/")
    if len(parts) < 3 or parts[0] != "research":
        return None
    name = parts[1]
    if name.startswith("_") or name in not_trees:
        return None
    return name


# --------------------------------------------------------------------------
# topics.md


def topic_word_name(stem: str) -> str:
    """``primitive_core`` -> ``PrimitiveCore``."""
    return "".join(part[:1].upper() + part[1:] for part in stem.split("_"))


def runner_stems(files: Sequence[str]) -> list[str]:
    """Stems of every ``code/run_*.py`` directly under ``code/``."""
    return sorted(
        f[len("code/run_"):-len(".py")]
        for f in files
        if f.startswith("code/run_") and f.endswith(".py") and f.count("/") == 1
    )


def member(files: Sequence[str], role: str, stem: str) -> tuple[str | None, bool]:
    """The tracked file filling ``role`` for ``stem``, and whether its case is exact."""
    directory = dict(ROLES)[role]
    name = {
        "computation": f"{stem}.py",
        "runner": f"run_{stem}.py",
        "tests": f"test_{stem}.py",
        "proofs": f"{topic_word_name(stem)}.lean",
        "output": f"{stem}.json",
    }[role]
    exact = directory + name
    if exact in files:
        return exact, True
    folded = [
        f for f in files
        if f.startswith(directory) and "/" not in f[len(directory):]
        and f.lower() == exact.lower()
    ]
    if len(folded) == 1:
        return folded[0], False
    return None, False


def _string_patterns(tree: ast.AST) -> list[str]:
    """String constants, and f-strings read as globs with ``*`` per field."""
    inside: set[int] = set()
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            text = ""
            for part in node.values:
                if isinstance(part, ast.Constant) and isinstance(part.value, str):
                    text += part.value
                    inside.add(id(part))
                else:
                    text += "*"
            found.append(text)
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in inside):
            found.append(node.value)
    return found


def _imports(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
            if node.module == "derivation":
                names.update(f"derivation.{alias.name}" for alias in node.names)
    return names


def _artifacts_named(patterns: Sequence[str], artifacts: Sequence[str]) -> list[str]:
    """Committed artifacts whose path under ``artifacts/`` or whose file name
    equals a string of the runner, or matches one of its f-string globs.
    Only strings ending in an artifact suffix count."""
    named: set[str] = set()
    for artifact in artifacts:
        rel = artifact[len("artifacts/"):]
        base = posixpath.basename(rel)
        for pattern in patterns:
            if not pattern.endswith(ARTIFACT_SUFFIXES) or any(c.isspace() for c in pattern):
                continue
            if "*" in pattern:
                if fnmatch.fnmatchcase(base, pattern) or fnmatch.fnmatchcase(rel, pattern):
                    named.add(artifact)
            elif pattern in (rel, base, artifact):
                named.add(artifact)
    return sorted(named)


def _parse(repo: Path, rel: str) -> ast.AST:
    try:
        return ast.parse(_read_text(repo, rel), filename=rel)
    except SyntaxError as exc:
        raise ValueError(f"{rel} does not parse: {exc}") from exc


@dataclass(frozen=True)
class TopicRow:
    """What the topic index says about one runner stem."""

    stem: str
    members: Mapping[str, tuple[str | None, bool]]
    imports: tuple[str, ...]
    importers: tuple[str, ...]
    artifacts: tuple[str, ...]


def topic_rows(repo: Path, files: Sequence[str]) -> list[TopicRow]:
    """One record per runner stem; the data both renderings read."""
    artifacts = [f for f in files if f.startswith("artifacts/")]
    tests = [f for f in files if f.startswith("tests/") and f.count("/") == 1
             and posixpath.basename(f).startswith("test_") and f.endswith(".py")]
    test_imports = {t: _imports(_parse(repo, t)) for t in tests}
    rows: list[TopicRow] = []
    for stem in runner_stems(files):
        runner = f"code/run_{stem}.py"
        tree = _parse(repo, runner)
        members = {role: member(files, role, stem) for role, _ in ROLES}
        imports = sorted(
            name for name in _imports(tree)
            if name.startswith("derivation.") or name.startswith("run_")
        )
        importers = sorted(t for t, names in test_imports.items() if f"run_{stem}" in names)
        rows.append(TopicRow(
            stem=stem,
            members=members,
            imports=tuple(imports),
            importers=tuple(importers),
            artifacts=tuple(_artifacts_named(_string_patterns(tree), artifacts)),
        ))
    return rows


def _cell(path: str | None, exact: bool, directory: str) -> str:
    if path is None:
        return "absent"
    shown = f"`{path[len(directory):]}`"
    return shown if exact else f"{shown} (case differs)"


def render_topics(repo: Path, files: Sequence[str]) -> str:
    rows = topic_rows(repo, files)
    artifacts = [f for f in files if f.startswith("artifacts/")]
    named = {artifact for row in rows for artifact in row.artifacts}
    out = [
        "# Topic index",
        "",
        "AuthorityEffect: None.  Generated by `ci/lookup_indexes.py`; do not edit",
        f"by hand.  Regenerate with `{REGENERATE}`;",
        "`tests/test_lookup_indexes.py` fails, naming this file, when it is stale.",
        "",
        "One row per `code/run_*.py` directly under `code/`, the same glob the",
        "runner census uses.  The first table names the five files of the family",
        "pattern that exist for each runner stem; `absent` means no tracked file",
        "has that name.  The proofs member is the stem's words capitalized and",
        "joined; `case differs` marks a tracked file whose name differs from that",
        "only in letter case.  No total is committed; `python ci/lookup_indexes.py",
        "--summary` prints the totals.",
        "",
        "| topic | computation `code/derivation/` | runner `code/` | tests `tests/` "
        "| proofs `lean4/Derivation/` | output `artifacts/` | members |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        cells = [_cell(*row.members[role], directory) for role, directory in ROLES]
        have = sum(1 for path, _ in row.members.values() if path is not None)
        out.append(f"| `{row.stem}` | " + " | ".join(cells) + f" | {have} of 5 |")
    out += [
        "",
        "## Where each runner reaches",
        "",
        "Read from syntax trees, not from names.  *Imports*: the `derivation`",
        "modules and sibling runners the runner imports.  *Imported by*: the",
        "root tests that import the runner.  *Artifacts named*: committed files",
        "under `artifacts/` whose path or file name equals a string in the",
        "runner's source ending in `.json`, `.json.gz` or `.txt`, or matches such",
        "an f-string read as a glob with `*` for each replacement field; a runner",
        "names what it reads as well as what it writes.",
        "",
        "| topic | imports | imported by | artifacts named |",
        "|---|---|---|---|",
    ]
    for row in rows:
        imports = ", ".join(f"`{n}`" for n in row.imports) or "none"
        importers = ", ".join(f"`{posixpath.basename(t)}`" for t in row.importers) or "none"
        arts = ", ".join(f"`{a[len('artifacts/'):]}`" for a in row.artifacts) or "none"
        out.append(f"| `{row.stem}` | {imports} | {importers} | {arts} |")
    unnamed = [a for a in artifacts if a not in named]
    out += [
        "",
        "## Artifacts no runner names",
        "",
    ]
    out += [f"- `{a}`" for a in unnamed] or ["- none"]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# pins.md


@dataclass(frozen=True)
class Pin:
    """One path recorded by one pin file, or covered by one scope pin."""

    path: str
    source: str
    tree: str
    kind: str


@dataclass(frozen=True)
class Scope:
    """A verifier that asks git whether anything under its pathspecs moved."""

    verifier: str
    tree: str
    pathspecs: tuple[str, ...]


@dataclass(frozen=True)
class PinCensus:
    """Everything ``pins.md`` is rendered from."""

    pins: tuple[Pin, ...]
    pin_files: tuple[str, ...]
    scopes: tuple[Scope, ...]
    problems: tuple[str, ...]


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for name, value in pairs:
        if name in result:
            raise ValueError(f"duplicate JSON key {name!r}")
        result[name] = value
    return result


def _strings(value: object, shape: Shape = ()) -> Iterator[tuple[Shape, str]]:
    """Every string in a JSON value with its field path; dict keys end in KEY."""
    if isinstance(value, dict):
        for name, item in value.items():
            yield (*shape, KEY), name
            yield from _strings(item, (*shape, name))
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item, (*shape, ITEM))
    elif isinstance(value, str):
        yield shape, value


def _matches(rule: Shape, shape: Shape) -> bool:
    if len(rule) != len(shape):
        return False
    for want, have in zip(rule, shape):
        if want == ANY:
            if have in (KEY, ITEM):
                return False
        elif want != have:
            return False
    return True


def _lookup(shape: Shape) -> tuple[PinField | None, str | None]:
    for rule, field in PIN_FIELDS.items():
        if _matches(rule, shape):
            return field, None
    for rule, reason in NOT_PIN_FIELDS.items():
        if _matches(rule, shape):
            return None, reason
    return None, None


def _show_shape(shape: Shape) -> str:
    return "/" + "/".join(shape)


def pin_files(files: Sequence[str], not_trees: Mapping[str, str]) -> list[str]:
    """Every tracked pin file under a research tree."""
    return [
        f for f in files
        if _tree_of(f, not_trees) is not None and PIN_FILE_NAME.match(posixpath.basename(f))
    ]


def verifiers(files: Sequence[str], not_trees: Mapping[str, str]) -> list[str]:
    """Every tracked ``verify*.py`` at the top level of a research tree."""
    return [
        f for f in files
        if _tree_of(f, not_trees) is not None and f.count("/") == 2
        and posixpath.basename(f).startswith("verify") and f.endswith(".py")
    ]


def _string_tuples(tree: ast.Module) -> dict[str, tuple[str, ...]]:
    """Module-level names bound to a tuple or list of string constants."""
    found: dict[str, tuple[str, ...]] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, value = node.targets[0], node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            target, value = node.target, node.value
        else:
            continue
        if (isinstance(target, ast.Name) and isinstance(value, (ast.Tuple, ast.List))
                and value.elts
                and all(isinstance(e, ast.Constant) and isinstance(e.value, str)
                        for e in value.elts)):
            found[target.id] = tuple(str(e.value) for e in value.elts)  # type: ignore[attr-defined]
    return found


def scopes_of(repo: Path, rel: str, tree_name: str) -> list[Scope]:
    """The scope pins one verifier declares, read from its syntax tree.

    A scope pin is a module-level tuple or list of strings passed starred
    (``*NAME``) to a call whose other positional arguments include the
    string ``diff`` or ``log``: the verifier asks git whether anything
    under those pathspecs changed since the commit it trusts.
    """
    parsed = _parse(repo, rel)
    assert isinstance(parsed, ast.Module)
    constants = _string_tuples(parsed)
    found: set[tuple[str, ...]] = set()
    for node in ast.walk(parsed):
        if not isinstance(node, ast.Call):
            continue
        verbs = {a.value for a in node.args if isinstance(a, ast.Constant)}
        if not verbs & SCOPE_VERBS:
            continue
        for arg in node.args:
            if (isinstance(arg, ast.Starred) and isinstance(arg.value, ast.Name)
                    and arg.value.id in constants):
                found.add(constants[arg.value.id])
    return [Scope(rel, tree_name, specs) for specs in sorted(found)]


class _PathSpace:
    """What counts as naming a repository path."""

    def __init__(self, files: Sequence[str]) -> None:
        self.files = frozenset(files)
        dirs: set[str] = set()
        for f in files:
            parts = f.split("/")
            for i in range(1, len(parts)):
                dirs.add("/".join(parts[:i]))
        self.dirs = frozenset(dirs)
        self.top = frozenset(d for d in dirs if "/" not in d)

    def names_path(self, value: str, tree_root: str) -> bool:
        """A tracked file, from the root or the tree; or, with a ``/`` in it,
        a tracked directory or anything under a top-level tracked directory.
        A single word that happens to be a directory name is not a path."""
        if not value or any(ch.isspace() for ch in value) or ":" in value:
            return False
        bare = value.rstrip("/")
        if bare in self.files or f"{tree_root}/{bare}" in self.files:
            return True
        if "/" not in value:
            return False
        if bare in self.dirs or f"{tree_root}/{bare}" in self.dirs:
            return True
        return bare.split("/", 1)[0] in self.top


def _under(files: Sequence[str], spec: str) -> list[str]:
    """Tracked files a git pathspec without magic selects."""
    bare = spec.rstrip("/")
    return [f for f in files if f == bare or f.startswith(bare + "/")]


def collect_pins(repo: Path, files: Sequence[str]) -> PinCensus:
    """Every pin, every pin file and scope verifier, and every problem found."""
    not_trees: Mapping[str, str] = _load_research_index().NOT_TREES
    space = _PathSpace(files)
    sources = pin_files(files, not_trees)
    pins: set[Pin] = set()
    problems: list[str] = []
    for rel in sources:
        tree = _tree_of(rel, not_trees)
        assert tree is not None
        tree_root = f"research/{tree}"
        try:
            data = json.loads(_read_text(repo, rel), object_pairs_hook=_unique_object)
        except (OSError, ValueError) as exc:
            problems.append(f"{rel}: cannot be read as JSON: {exc}")
            continue
        for shape, value in _strings(data):
            field, reason = _lookup(shape)
            if field is None:
                if reason is None and space.names_path(value, tree_root):
                    problems.append(
                        f"{rel}: field {_show_shape(shape)} names the path {value!r} but is "
                        "in neither PIN_FIELDS nor NOT_PIN_FIELDS of ci/lookup_indexes.py"
                    )
                continue
            path = value.rstrip("/")
            if field.relative_to_tree:
                path = posixpath.normpath(f"{tree_root}/{path}")
            under = _under(files, path) if field.kind == "tree" else []
            if under:
                pins.update(Pin(f, rel, tree, "tree") for f in under)
            else:
                pins.add(Pin(path, rel, tree, field.kind))
    scopes: list[Scope] = []
    for rel in verifiers(files, not_trees):
        tree = _tree_of(rel, not_trees)
        assert tree is not None
        try:
            found = scopes_of(repo, rel, tree)
        except (OSError, ValueError) as exc:
            problems.append(f"{rel}: cannot be read for scope pins: {exc}")
            continue
        for scope in found:
            scopes.append(scope)
            for spec in scope.pathspecs:
                pins.update(Pin(f, rel, tree, "scope") for f in _under(files, spec))
    return PinCensus(
        pins=tuple(sorted(pins, key=lambda p: (p.path, p.tree, p.source, p.kind))),
        pin_files=tuple(sources),
        scopes=tuple(scopes),
        problems=tuple(problems),
    )


def _checked(census: PinCensus) -> PinCensus:
    if census.problems:
        raise ValueError("\n".join(census.problems))
    return census


def _label(source: str, tree: str) -> str:
    local = source[len(f"research/{tree}/"):]
    return f"`{tree}`" if local == "SOURCE_MANIFEST.json" else f"`{tree}/{local}`"


def _kinds(kinds: set[str]) -> str:
    return ", ".join(k for k in KIND_ORDER if k in kinds)


@dataclass(frozen=True)
class PinRow:
    """One rendered row of ``pins.md``."""

    trees: int
    pinned_by: str
    scope: str


def pin_rows(census: PinCensus) -> dict[str, PinRow]:
    """``path -> row``: distinct trees, the pin-file cell, and the scope cell."""
    explicit: dict[str, dict[tuple[str, str], set[str]]] = {}
    scoped: dict[str, set[tuple[str, str]]] = {}
    trees: dict[str, set[str]] = {}
    for pin in census.pins:
        trees.setdefault(pin.path, set()).add(pin.tree)
        if pin.kind == "scope":
            scoped.setdefault(pin.path, set()).add((pin.tree, pin.source))
        else:
            explicit.setdefault(pin.path, {}).setdefault((pin.tree, pin.source), set()).add(
                pin.kind)
    every_scope = {(s.tree, s.verifier) for s in census.scopes}
    rows: dict[str, PinRow] = {}
    for path in trees:
        holders = explicit.get(path, {})
        cell = ", ".join(
            f"{_label(source, tree)} ({_kinds(kinds)})"
            for (tree, source), kinds in sorted(holders.items())
        ) or "none"
        covering = scoped.get(path, set())
        if not covering:
            scope = "none"
        elif covering == every_scope:
            scope = f"all {len(every_scope)}"
        else:
            scope = ", ".join(_label(source, tree) for tree, source in sorted(covering))
        rows[path] = PinRow(len(trees[path]), cell, scope)
    return rows


def render_pins(repo: Path, files: Sequence[str]) -> str:
    census = _checked(collect_pins(repo, files))
    tracked = frozenset(files)
    rows = pin_rows(census)
    per_source: dict[str, set[str]] = {}
    for pin in census.pins:
        per_source.setdefault(pin.source, set()).add(pin.path)
    out = [
        "# Pin index",
        "",
        "AuthorityEffect: None.  Generated by `ci/lookup_indexes.py`; do not edit",
        f"by hand.  Regenerate with `{REGENERATE}`;",
        "`tests/test_lookup_indexes.py` fails, naming this file, when it is stale.",
        "",
        "For each tracked path, the research trees that pin it: before changing a",
        "path, its row says how many trees may need a repin.",
        "`python ci/lookup_indexes.py --who-pins PATH ...` prints the same rows",
        "from the working tree, so a change can be priced before its pull request.",
        "",
        "Pin files are the tracked files under `research/<tree>/` named in capital",
        "letters, digits and underscores ending in `MANIFEST.json`, `PIN.json` or",
        "`PINS.json`.  Each is read field by field: the generator's `PIN_FIELDS`",
        "and `NOT_PIN_FIELDS` tables decide which fields pin, and a path in any",
        "other field stops generation.  A label is the tree name when the pin file",
        "is that tree's `SOURCE_MANIFEST.json`, and the tree plus the file otherwise.",
        "Kinds: `tree`, a Git tree object, expanded here to every tracked file under",
        "it; `file`, a digest or the exact content of one file; `span`, a digest of",
        "a line span; `copy`, the source of a vendored copy; `reconstruction`, the",
        "source of a reconstructed line range.",
        "",
        "Scope pins are not in any pin file.  They are read from the syntax tree of",
        "each tree's top-level `verify*.py`: a module-level tuple or list of strings",
        "passed starred to a call that also passes the string `diff` or `log`,",
        "that is, a verifier asking git whether anything under those pathspecs",
        "changed since the commit it trusts.  Every tracked path under them is",
        "pinned by that tree; the last column says `all N` when every scope pin",
        "in the table below covers the path.  The `trees` column counts distinct",
        "trees over both kinds of pin.",
        "",
        "Whether a verifier compares a file pin with the current file or only with",
        "the commit its pin file names is not read here; run that verifier to know.",
        "Digests written into Python source are not read either.  No total is",
        "committed; `python ci/lookup_indexes.py --summary` prints the totals.",
        "",
        "## Pin files",
        "",
        "| pin file | sealed paths | other paths | paths not in the git index |",
        "|---|---|---|---|",
    ]
    for rel in census.pin_files:
        recorded = per_source.get(rel, set())
        sealed = sum(1 for p in recorded if p in tracked and is_sealed(p))
        other = sum(1 for p in recorded if p in tracked and not is_sealed(p))
        missing = sum(1 for p in recorded if p not in tracked)
        out.append(f"| `{rel}` | {sealed} | {other} | {missing} |")
    out += [
        "",
        "## Scope pins",
        "",
        "| verifier | pathspecs | tracked paths covered |",
        "|---|---|---|",
    ]
    for scope in census.scopes:
        specs = " ".join(f"`{s}`" for s in scope.pathspecs)
        covered = len({f for s in scope.pathspecs for f in _under(files, s)})
        out.append(f"| `{scope.verifier}` | {specs} | {covered} |")
    if not census.scopes:
        out.append("| none | none | 0 |")
    sections = (
        ("Sealed paths", [p for p in sorted(rows) if p in tracked and is_sealed(p)]),
        ("Other pinned paths", [p for p in sorted(rows) if p in tracked and not is_sealed(p)]),
    )
    header = ["| path | trees | pinned by | scope pins |", "|---|---|---|---|"]
    for title, paths in sections:
        out += ["", f"## {title}", "", *header]
        out += [f"| `{p}` | {rows[p].trees} | {rows[p].pinned_by} | {rows[p].scope} |"
                for p in paths] or ["| none | 0 | none | none |"]
    missing_paths = [p for p in sorted(rows) if p not in tracked]
    out += [
        "",
        "## Pinned paths not in the git index",
        "",
        "Recorded by a pin file but not tracked at this revision: pinned at a",
        "commit that had them, or declared by a field whose paths are not files.",
        "",
        *header,
    ]
    out += [f"| `{p}` | {rows[p].trees} | {rows[p].pinned_by} | {rows[p].scope} |"
            for p in missing_paths] or ["| none | 0 | none | none |"]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# driver


def expected(repo: Path) -> dict[str, str]:
    """``output path -> generated text`` for both indexes."""
    files = tracked_files(repo)
    return {TOPICS_REL: render_topics(repo, files), PINS_REL: render_pins(repo, files)}


def problems(repo: Path) -> list[str]:
    """Empty when both indexes are current; otherwise lines naming each stale file."""
    try:
        want = expected(repo)
    except ValueError as exc:
        return [f"cannot generate the lookup indexes: {exc}"]
    report: list[str] = []
    for rel, text in want.items():
        target = repo / rel
        have = _read_text(repo, rel) if target.is_file() else None
        if have == text:
            continue
        if have is None:
            report.append(f"{rel} is missing; generate it with: {REGENERATE}")
            continue
        report.append(f"{rel} is stale; regenerate it with: {REGENERATE}")
        report += difflib.unified_diff(
            have.splitlines(), text.splitlines(),
            f"{rel} (committed)", f"{rel} (generated)", lineterm="", n=0,
        )
    return report


def write(repo: Path) -> list[str]:
    """Rewrite both indexes; return one line per file."""
    lines: list[str] = []
    for rel, text in expected(repo).items():
        if is_sealed(rel):
            raise ValueError(f"refusing to write inside the sealed derivation: {rel}")
        target = repo / rel
        data = text.encode("utf-8")
        if target.is_file() and target.read_bytes().replace(b"\r\n", b"\n") == data:
            lines.append(f"{rel} already current")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        lines.append(f"wrote {rel}")
    return lines


def who_pins(repo: Path, queries: Sequence[str]) -> list[str]:
    """The pin rows for the paths given; a trailing ``/`` selects a directory."""
    census = _checked(collect_pins(repo, tracked_files(repo)))
    rows = pin_rows(census)
    lines: list[str] = []
    trees: set[str] = set()
    for raw in queries:
        query = raw.replace("\\", "/")
        if query.startswith("./"):
            query = query[2:]
        chosen = sorted(p for p in rows if p.startswith(query)) if query.endswith("/") else (
            [query] if query in rows else []
        )
        if not chosen:
            lines.append(f"{query}: pinned by no tree")
        for path in chosen:
            row = rows[path]
            lines.append(f"{path}: {row.trees} trees: {row.pinned_by}; scope pins: {row.scope}")
            trees.update(pin.tree for pin in census.pins if pin.path == path)
    lines.append(f"distinct trees pinning the paths given: {len(trees)}")
    return lines


def summary(repo: Path) -> list[str]:
    """Totals, printed rather than committed."""
    files = tracked_files(repo)
    rows = topic_rows(repo, files)
    full = sum(1 for r in rows if all(path is not None for path, _ in r.members.values()))
    exact = sum(1 for r in rows if all(path is not None and ok for path, ok in r.members.values()))
    census = _checked(collect_pins(repo, files))
    tracked = frozenset(files)
    paths = {p.path for p in census.pins}
    explicit = {p.path for p in census.pins if p.kind != "scope"}
    all_sealed = {f for f in files if is_sealed(f)}
    sealed = paths & all_sealed
    trees = {p.tree for p in census.pins}
    tree_object = {p.tree for p in census.pins
                   if p.kind == "tree" and p.path.startswith("lean4/Derivation/")}
    return [
        f"runners: {len(rows)}",
        f"runners with all five members: {full} ({exact} with every name in exact case)",
        f"pin files: {len(census.pin_files)} in "
        f"{len({_tree_of(s, {}) for s in census.pin_files})} trees",
        f"scope pins: {len(census.scopes)} verifiers in "
        f"{len({s.tree for s in census.scopes})} trees",
        f"trees pinning at least one path: {len(trees)}",
        f"trees pinning lean4/Derivation as one Git tree object: {len(tree_object)}",
        f"tracked sealed paths: {len(all_sealed)}; pinned by some tree: {len(sealed)}; "
        f"named by some pin file: {len(explicit & all_sealed)}",
        f"tracked other paths pinned: {len((paths & tracked) - all_sealed)}",
        f"pinned paths not in the git index: {len(paths - tracked)}",
    ]


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="exit 1 naming each stale index")
    mode.add_argument("--write", action="store_true", help="rewrite both indexes")
    mode.add_argument("--summary", action="store_true", help="print totals")
    mode.add_argument("--who-pins", nargs="+", metavar="PATH", help="print pin rows for paths")
    args = parser.parse_args(argv)
    try:
        if args.check:
            found = problems(REPO)
            print("\n".join(found) if found else "lookup indexes are current")
            return 1 if found else 0
        if args.write:
            print("\n".join(write(REPO)))
            return 0
        if args.summary:
            print("\n".join(summary(REPO)))
            return 0
        print("\n".join(who_pins(REPO, args.who_pins)))
        return 0
    except ValueError as exc:
        print(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
