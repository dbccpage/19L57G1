"""The source-isolation scan historically called the blindness scan.

Before the committed freeze, every distinct committed write-root version, the
current HEAD and index, and the working/untracked files must be free of a
citation into a sealed path, a sealed claim identifier or Lean name, an import
of the sealed kernel, or the name of another research tree.  Historical tree
names are accumulated before the versions are scanned, so a sibling name that
appeared between write-root commits cannot evade the check.  Only the root
``SEED.md`` is exempt.  Undecodable or symlinked files fail closed because an
all-file scan cannot certify bytes it did not inspect.

The seed states the rule and is the input, not a file this run writes; this
test file is itself scanned, so the probes below assemble barred examples from
pieces.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import unittest

from verify_freeze import audit as audit_freeze, blobs as read_blobs, tree as read_tree

TREE = pathlib.Path(__file__).resolve().parent.parent
ROOT = TREE.parent.parent
REL = "research/boundary_seed"
SEED_REPO_PATH = f"{REL}/SEED.md"
FREEZE_REPO_PATH = f"{REL}/FREEZE.md"

SEALED_PATTERNS: tuple[tuple[str, str], ...] = (
    (
        "citation into the sealed paper",
        r"\bpaper[\\/][^\s`'\"<>]+?\.md\b",
    ),
    (
        "citation into the sealed artifacts",
        r"\bartifacts[\\/][A-Za-z0-9_.-][^\s`'\"<>]*",
    ),
    (
        "citation into the sealed Lean",
        r"\blean4[\\/]Derivation[\\/][A-Za-z0-9_.-][^\s`'\"<>]*",
    ),
    (
        "citation into the sealed kernel",
        r"\bcode[\\/]derivation[\\/][A-Za-z0-9_.-][^\s`'\"<>]*",
    ),
    ("sealed claim identifier", r"\bCL-[A-Za-z0-9]"),
    ("sealed Lean name", r"\bDerivation\.[A-Za-z_]"),
    ("import of the sealed kernel", r"^\s*(?:from|import)\s+derivation\b"),
)


def git_bytes(args: list[str]) -> bytes:
    proc = subprocess.run(["git", "--no-replace-objects", *args], cwd=ROOT, capture_output=True)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout


def nul_paths(data: bytes) -> list[str]:
    return sorted(
        item.decode("utf-8", errors="surrogateescape")
        for item in data.split(b"\0")
        if item
    )


def other_trees(ref: str = "HEAD") -> list[str]:
    """Names of the other research trees at ``ref``; names only, no reads."""

    paths = nul_paths(
        git_bytes(["ls-tree", "-d", "-z", "--name-only", ref, "--", "research/"])
    )
    names = [path.replace("\\", "/").split("/")[-1] for path in paths]
    return sorted(name for name in names if name and name != "boundary_seed")


def tree_patterns(names: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for name in names:
        out.append(
            (
                f"other research tree {name}",
                rf"\bresearch[\\/]{re.escape(name)}\b",
            )
        )
        if "_" in name:
            out.append((f"other research tree {name}", rf"\b{re.escape(name)}\b"))
    return out


def scan_text(text: str, patterns: list[tuple[str, str]]) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in patterns:
            if re.search(pattern, line):
                hits.append((lineno, label))
    return hits


def scan_bytes(
    data: bytes, source: str, patterns: list[tuple[str, str]]
) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [f"{source}: non-UTF-8 content cannot be blind-scanned"]
    return [
        f"{source}:{lineno}: {label}"
        for lineno, label in scan_text(text, patterns)
    ]


def is_exempt(repo_path: str) -> bool:
    return repo_path.replace("\\", "/") == SEED_REPO_PATH


def all_patterns(names: list[str] | None = None) -> list[tuple[str, str]]:
    return list(SEALED_PATTERNS) + tree_patterns(other_trees() if names is None else names)


def tree_paths(ref: str) -> list[str]:
    return nul_paths(
        git_bytes(["ls-tree", "-r", "-z", "--name-only", ref, "--", REL])
    )


def index_paths() -> list[str]:
    return nul_paths(git_bytes(["ls-files", "--cached", "-z", "--", REL]))


def working_paths() -> list[str]:
    return nul_paths(
        git_bytes(
            [
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
                "--",
                REL,
            ]
        )
    )


def current_research_paths() -> list[str]:
    return nul_paths(
        git_bytes(
            [
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
                "--",
                "research",
            ]
        )
    )


def history_commits(ref: str = "HEAD") -> list[str]:
    data = git_bytes(["rev-list", "--reverse", "--full-history", ref, "--", REL])
    return [line for line in data.decode("ascii").splitlines() if line]


def historical_other_trees() -> list[str]:
    """All sibling research-tree names reachable from ``HEAD`` history."""

    paths = nul_paths(
        git_bytes(["log", "--full-history", "--format=", "--name-only", "-z", "HEAD", "--", "research/"])
    )
    names = {
        parts[1]
        for repo_path in paths
        if len(parts := repo_path.replace("\\", "/").split("/")) >= 2
        and parts[0] == "research"
        and parts[1] != "boundary_seed"
    }
    return sorted(names)


def scan_snapshot(
    ref: str, label: str, names: list[str],
    cache: dict[str, list[str]] | None = None,
) -> tuple[list[str], bool]:
    # All versions and paths remain in the population. Only repeated reads and
    # scans of identical immutable Git blobs are shared within this invocation.
    population = read_tree(ROOT, ref)
    patterns = all_patterns(names)
    cached = {} if cache is None else cache
    missing = [
        blob.oid for path, blob in population.items()
        if not is_exempt(path) and blob.oid not in cached
    ]
    for oid, data in read_blobs(ROOT, missing).items():
        cached[oid] = scan_bytes(data, "", patterns)
    problems: list[str] = []
    for repo_path, blob in population.items():
        if is_exempt(repo_path):
            continue
        problems.extend(f"{label}:{repo_path}{suffix}" for suffix in cached[blob.oid])
    return problems, FREEZE_REPO_PATH in population


def scan_committed_history() -> tuple[list[str], bool]:
    """Scan every distinct pre-freeze write-root version and the freeze."""

    freeze = audit_freeze(ROOT)
    problems = list(freeze.problems)
    frozen = freeze.frozen
    shallow = git_bytes(["rev-parse", "--is-shallow-repository"]).decode("ascii").strip()
    if shallow != "false":
        return ["history: repository is shallow; blindness history is incomplete"], False
    tip = freeze.commit if frozen and freeze.commit is not None else "HEAD"
    commits = history_commits(tip)
    if not commits:
        return ["history: no commit contains the write root"], False
    names = historical_other_trees()
    cache: dict[str, list[str]] = {}
    for commit in commits:
        try:
            found, _marker_present = scan_snapshot(commit, commit[:12], names, cache)
            problems.extend(found)
        except (ValueError, OSError, UnicodeError) as exc:
            problems.append(f"{commit}: source population cannot be scanned: {exc}")
    head = git_bytes(["rev-parse", tip]).decode("ascii").strip()
    if commits[-1] != head:
        try:
            found, _marker_present = scan_snapshot(tip, tip, names, cache)
            problems.extend(found)
        except (ValueError, OSError, UnicodeError) as exc:
            problems.append(f"{tip}: source population cannot be scanned: {exc}")
    return problems, frozen


def current_other_trees(paths: list[str]) -> list[str]:
    names = set(other_trees())
    for repo_path in paths:
        parts = repo_path.replace("\\", "/").split("/")
        if len(parts) >= 2 and parts[0] == "research" and parts[1] != "boundary_seed":
            names.add(parts[1])
    return sorted(names)


def scan_index_and_working() -> list[str]:
    working = working_paths()
    patterns = all_patterns(current_other_trees(current_research_paths()))
    problems: list[str] = []
    indexed: list[tuple[str, str]] = []
    for record in git_bytes(["ls-files", "--stage", "-z", "--", REL]).split(b"\0"):
        if not record:
            continue
        header, raw_path = record.split(b"\t", 1)
        mode, oid, stage = header.decode("ascii").split()
        repo_path = raw_path.decode("utf-8")
        if is_exempt(repo_path):
            continue
        if mode not in ("100644", "100755") or stage != "0":
            problems.append(f"INDEX:{repo_path}: nonregular or unresolved source cannot be scanned")
            continue
        indexed.append((repo_path, oid))
    content = read_blobs(ROOT, [oid for _path, oid in indexed])
    for repo_path, oid in indexed:
        problems.extend(scan_bytes(content[oid], f"INDEX:{repo_path}", patterns))
    for repo_path in working:
        if is_exempt(repo_path):
            continue
        path = ROOT / repo_path
        if path.is_symlink():
            problems.append(f"{repo_path}: symlink cannot be blind-scanned")
            continue
        if not path.exists():
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            problems.append(f"{repo_path}: cannot be blind-scanned: {exc}")
            continue
        problems.extend(scan_bytes(data, repo_path, patterns))
    return problems


class SourceIsolationScan(unittest.TestCase):
    def test_write_root_is_source_isolated_before_the_freeze(self) -> None:
        problems, frozen = scan_committed_history()
        if not frozen:
            problems.extend(scan_index_and_working())
        self.assertEqual(problems, [], "\n".join(problems))


class ScanProbes(unittest.TestCase):
    """Each barred example is assembled so this file carries no citation."""

    def hits(self, text: str) -> list[str]:
        return [label for _, label in scan_text(text, all_patterns())]

    def test_probe_paper(self) -> None:
        label = "citation into the sealed paper"
        self.assertEqual(self.hits("see " + "paper/" + "paper.md"), [label])
        self.assertEqual(self.hits("see " + "paper/nested/" + "foo-bar.md"), [label])
        self.assertEqual(self.hits("see " + "paper\\nested\\" + "foo-bar.md"), [label])

    def test_probe_artifacts(self) -> None:
        label = "citation into the sealed artifacts"
        self.assertEqual(self.hits("art" + "ifacts/" + "claims.json"), [label])
        self.assertEqual(self.hits("art" + "ifacts\\nested\\" + "claim-one.json"), [label])

    def test_probe_lean(self) -> None:
        label = "citation into the sealed Lean"
        self.assertEqual(self.hits("lean4/Deri" + "vation/" + "Basic.lean"), [label])
        self.assertEqual(self.hits("lean4\\Deri" + "vation\\" + "Sub\\Basic.lean"), [label])

    def test_probe_kernel(self) -> None:
        label = "citation into the sealed kernel"
        self.assertEqual(self.hits("code/deri" + "vation/" + "model.py"), [label])
        self.assertEqual(self.hits("code\\deri" + "vation\\" + "sub\\model.py"), [label])

    def test_probe_claim_id(self) -> None:
        self.assertEqual(self.hits("C" + "L-" + "0-INERTIA"), ["sealed claim identifier"])

    def test_probe_lean_name(self) -> None:
        label = "sealed Lean name"
        self.assertEqual(self.hits("Deri" + "vation." + "Foo"), [label])
        self.assertEqual(self.hits("Deri" + "vation." + "supply_no_op"), [label])

    def test_probe_import(self) -> None:
        label = "import of the sealed kernel"
        self.assertEqual(self.hits("from deri" + "vation import model"), [label])
        self.assertEqual(self.hits("import deri" + "vation"), [label])
        self.assertEqual(self.hits("from boundary import model"), [])

    def test_probe_other_tree(self) -> None:
        names = other_trees()
        self.assertGreater(len(names), 0)
        underscored = [name for name in names if "_" in name]
        self.assertGreater(len(underscored), 0)
        name = underscored[0]
        self.assertEqual(self.hits(name), [f"other research tree {name}"])
        self.assertEqual(
            self.hits("research/" + name), [f"other research tree {name}"] * 2
        )
        self.assertEqual(
            self.hits("research\\" + name), [f"other research tree {name}"] * 2
        )
        plain = [candidate for candidate in names if "_" not in candidate]
        if plain:
            self.assertEqual(self.hits("the " + plain[0] + " commit"), [])
            self.assertEqual(
                self.hits("research/" + plain[0]),
                [f"other research tree {plain[0]}"],
            )

    def test_bare_directory_names_are_not_citations(self) -> None:
        self.assertEqual(
            self.hits("nothing under paper/, artifacts/, or lean4/Derivation/ is read"),
            [],
        )

    def test_only_root_seed_is_exempt(self) -> None:
        self.assertTrue(is_exempt(SEED_REPO_PATH))
        self.assertFalse(is_exempt(f"{REL}/challenge0/SEED.md"))

    def test_non_utf8_fails_closed(self) -> None:
        self.assertEqual(
            scan_bytes(bytes([0xFF]), "working:probe", []),
            ["working:probe: non-UTF-8 content cannot be blind-scanned"],
        )


if __name__ == "__main__":
    unittest.main()
