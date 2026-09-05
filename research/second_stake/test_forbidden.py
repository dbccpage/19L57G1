"""Boundary, vocabulary, temporal, and protected-open refusal gates."""

from __future__ import annotations

import datetime as dt
import gzip
import importlib.util
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
from types import ModuleType
from typing import Any, cast
from unittest import mock

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
SNAPSHOT = "3f44571240a0830a2fa8de639281670f4e50a511"
# This is rebound to the exact inherited base during ordered integration.  It
# is deliberately separate from SNAPSHOT, which remains the immutable source
# pin even after the scope comparison base advances.
#: The commit this rung's branch was cut from.  Kept because the frozen
#: source and receipt pins are taken there and that is the right base for a
#: pin.  It is the WRONG base for "what did this branch write": `main` moves,
#: and diffing the working tree against a commit that recedes into history
#: makes every LATER rung's merged work look like this rung's uncommitted
#: change.  See `comparison_base`.
SCOPE_BASE = "8dea98da841a862697a51d861a81f29ddc971f4e"
WRITE_ROOT = "research/second_stake/"
SHARED = (".github/workflows/verify.yml", "research/second/MANUAL.md")
ALLOWED = (WRITE_ROOT, *SHARED)
SEALED = ("prompt/", "paper/", "code/", "lean4/Derivation/", "artifacts/", "ci/")
OUTSIDE_NAME_DIGESTS = frozenset(
    {
        "b5fa4102bb18e5ad59ca341a805088caf71022fde564a480436642923c06aa5c",
        "040baadecf43b35030520a595630621776b2653faf2d5a90f8d5c52accaddad6",
        "a468285f70fd4f3f31e3f6a6b29918072a56b29cc64cd27285dd482aeafa5bf6",
        "666d83a02126d92598412bd2bb96ee181cc7bcc88a1014847b3ddf35fb8a87ea",
        "701fbfd68fbf2b9890d2d2bc8f61ded15153d9cbc5771376737d68ba9c1c9250",
        "874b4eedb60aa5724731fc8fff49c280d5f743565035f30b8e99cf2a81465468",
        "05ec28080374d83e95ef525efedbe41006ec04f7ba3ae61805da054707468eb1",
        "5a118d7e9e6cdfa0dcc8360e400011c6c1a376c61489275117d9bafafda969e1",
        "630471bc17c69d0bb5c0b2a31b8faf762b907eb27fba3204a0f15695d8f804b4",
    }
)
GENERATED_DIRS = frozenset({"__pycache__", ".mypy_cache", ".venv"})
VOLATILE_COVERAGE_FILES = frozenset({".coverage", "coverage.json"})
TEXT_SUFFIXES = frozenset({".json", ".md", ".py", ".toml"})
TEXT_NAMES = frozenset({".gitattributes", ".gitignore"})
FULL_RECEIPT = (HERE / "receipts" / "full" / "stake_full.json.gz").resolve()


def tree_files() -> list[pathlib.Path]:
    discovered = {
        path
        for path in HERE.rglob("*")
        if path.is_file()
        and path.name not in VOLATILE_COVERAGE_FILES
        and not any(part in GENERATED_DIRS for part in path.parts)
    }
    tracked = tracked_tree_files()
    for path in tracked:
        relative = path.relative_to(HERE)
        if any(part in GENERATED_DIRS for part in relative.parts):
            raise ValueError(f"tracked file in excluded generated directory: {relative}")
        if path.name in VOLATILE_COVERAGE_FILES:
            raise ValueError(f"tracked volatile coverage artifact: {relative}")
        discovered.add(path)
    return sorted(discovered)


def claim_files() -> list[pathlib.Path]:
    return [path for path in tree_files() if path.name != "test_forbidden.py"]


def scanner_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "stake_prose_scan", REPO / "ci" / "check_prose_watchlist.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coverage_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "stake_coverage_gate", HERE / "check_coverage.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strict_scan_text(path: pathlib.Path) -> str:
    """Read the declared text population and the one declared binary receipt."""

    resolved = path.resolve()
    raw = path.read_bytes()
    if resolved == FULL_RECEIPT:
        try:
            raw = gzip.decompress(raw)
        except (gzip.BadGzipFile, EOFError, OSError) as exc:
            raise ValueError(f"compressed receipt cannot be decoded: {path}") from exc
    elif path.suffix not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
        raise ValueError(f"undeclared binary path in scan population: {path}")
    if b"\0" in raw:
        raise ValueError(f"NUL byte in scanned text: {path}")
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"invalid UTF-8 in scanned text: {path}") from exc


def nul_paths(raw: bytes) -> list[str]:
    """Decode fail-closed NUL-terminated path output from Git."""

    if not raw:
        return []
    if not raw.endswith(b"\0"):
        raise ValueError("Git path census is not NUL terminated")
    chunks = raw[:-1].split(b"\0")
    if any(not chunk for chunk in chunks):
        raise ValueError("Git path census contains an empty path")
    try:
        return [chunk.decode("utf-8", errors="strict").replace("\\", "/") for chunk in chunks]
    except UnicodeDecodeError as exc:
        raise ValueError("Git path census is not valid UTF-8") from exc


def tracked_tree_files() -> list[pathlib.Path]:
    raw = subprocess.run(
        ["git", "ls-files", "-z", "--", WRITE_ROOT],
        cwd=REPO,
        capture_output=True,
        check=True,
    ).stdout
    return [REPO / pathlib.PurePosixPath(name) for name in nul_paths(raw)]


def comparison_base() -> str | None:
    """The commit this branch's own changes are measured against.

    NOT `SCOPE_BASE`.  That is where the pins are taken and it never moves,
    which is exactly why it cannot answer "what did THIS branch write": every
    rung merged after it shows up in the diff as though this rung had written
    it.  The right base is the tip of `main` this branch has merged.

    Returns None when no base resolves, and the caller FAILS rather than
    passes.  An unavailable scan is not a clean scan.
    """
    for ref in ("origin/main", "main"):
        proc = subprocess.run(
            ["git", "merge-base", ref, "HEAD"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    return None


def head_commit() -> str:
    """The commit under test, so a caller can tell "no branch" from "no
    diff".  Failing closed: an unreadable HEAD is not an excuse to skip."""
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise ValueError("git rev-parse HEAD failed; the boundary scan cannot run")
    return proc.stdout.strip()


def changed_paths(base: str = SCOPE_BASE) -> set[str]:
    diff_raw = subprocess.run(
        ["git", "diff", "--no-renames", "--name-only", "-z", base],
        cwd=REPO,
        capture_output=True,
        check=True,
    ).stdout
    untracked_raw = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=REPO,
        capture_output=True,
        check=True,
    ).stdout
    return set(nul_paths(diff_raw) + nul_paths(untracked_raw))


def append_only(base: bytes, current: bytes) -> bool:
    return current.startswith(base)


def outside_declared(paths: set[str]) -> set[str]:
    return {
        path
        for path in paths
        if not (path.startswith(WRITE_ROOT) or path in SHARED)
    }


def temporal_or_environment_keys(value: object) -> list[str]:
    """Return keys matching the declared metadata spellings and aliases."""

    failures: list[str] = []

    def walk(item: object, location: str) -> None:
        if isinstance(item, dict):
            for key, child in item.items():
                surface = str(key).replace("-", "_")
                lowered = re.sub(r"(?<!^)(?=[A-Z])", "_", surface).lower()
                child_location = f"{location}.{key}" if location else str(key)
                exact = {
                    "timestamp",
                    "time",
                    "date",
                    "datetime",
                    "environment",
                    "env",
                    "host",
                    "host_name",
                    "hostname",
                    "platform",
                    "cwd",
                    "working_directory",
                }
                temporal_suffixes = (
                    "_at",
                    "_date",
                    "_datetime",
                    "_time",
                    "_timestamp",
                )
                if lowered in exact or lowered.endswith(temporal_suffixes):
                    failures.append(child_location)
                walk(child, child_location)
        elif isinstance(item, list):
            for index, child in enumerate(item):
                walk(child, f"{location}[{index}]")

    walk(value, "")
    return failures


class VocabularyTests(unittest.TestCase):
    def test_repository_census_scanner_over_direct_write_root(self) -> None:
        scanner = scanner_module()
        data = cast(Any, scanner).load(REPO / cast(Any, scanner).WATCHLIST_REL)
        hits: list[str] = []
        for path in tree_files():
            text = strict_scan_text(path)
            for hit in cast(Any, scanner).scan_text(text, data["watched"]):
                hits.append(f"{path.relative_to(HERE)}:{hit.line}: {hit.surface}")
        self.assertEqual(hits, [])

    def test_scan_population_fails_closed_on_binary_and_decode_defects(self) -> None:
        self.assertTrue(strict_scan_text(FULL_RECEIPT).startswith("{"))
        with self.subTest("NUL"):
            with mock.patch.object(pathlib.Path, "read_bytes", return_value=b"ok\0bad"):
                with self.assertRaisesRegex(ValueError, "NUL byte"):
                    strict_scan_text(HERE / "probe.md")
        with self.subTest("invalid UTF-8"):
            with mock.patch.object(pathlib.Path, "read_bytes", return_value=b"\xff"):
                with self.assertRaisesRegex(ValueError, "invalid UTF-8"):
                    strict_scan_text(HERE / "probe.md")
        with self.subTest("undeclared binary"):
            with mock.patch.object(pathlib.Path, "read_bytes", return_value=b"ascii"):
                with self.assertRaisesRegex(ValueError, "undeclared binary"):
                    strict_scan_text(HERE / "probe.bin")
        with self.subTest("read failure"):
            with mock.patch.object(pathlib.Path, "read_bytes", side_effect=OSError("probe")):
                with self.assertRaises(OSError):
                    strict_scan_text(HERE / "probe.md")
        with self.subTest("force-tracked generated-directory member"):
            tracked_probe = HERE / ".venv" / "test_evil.py"
            with mock.patch(
                f"{__name__}.tracked_tree_files", return_value=[tracked_probe]
            ):
                with self.assertRaisesRegex(ValueError, "tracked file in excluded"):
                    tree_files()
        for name in sorted(VOLATILE_COVERAGE_FILES):
            with self.subTest(force_tracked_coverage_artifact=name):
                tracked_probe = HERE / name
                with mock.patch(
                    f"{__name__}.tracked_tree_files", return_value=[tracked_probe]
                ):
                    with self.assertRaisesRegex(
                        ValueError, "tracked volatile coverage artifact"
                    ):
                        tree_files()

    def test_outside_names_for_orbit_readers_are_absent_by_digest(self) -> None:
        for path in tree_files():
            if path.name == "test_forbidden.py":
                continue
            text = strict_scan_text(path)
            for word in re.findall(r"[A-Za-z]+", text):
                digest = hashlib.sha256(word.lower().encode("ascii")).hexdigest()
                self.assertNotIn(digest, OUTSIDE_NAME_DIGESTS, f"outside name in {path.name}")

    def test_working_identifier_denylist_is_absent(self) -> None:
        census = json.loads(
            (REPO / "contact" / "analysis" / "contact_countermodels.json").read_text("utf-8")
        )
        working = sorted(
            set(census["denylist"]["full_census"])
            - set(census["denylist"]["subtracted_as_native_or_core"])
        )
        self.assertEqual(len(working), 102)
        for path in tree_files():
            text = strict_scan_text(path)
            for token in working:
                hit = re.search(
                    r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])",
                    text,
                )
                self.assertIsNone(hit, f"{path.name} contains denied identifier {token}")


class BoundaryTests(unittest.TestCase):
    def test_changed_path_census_disables_renames_and_parses_nul(self) -> None:
        completed = (
            subprocess.CompletedProcess([], 0, b"old.txt\0new.txt\0", b""),
            subprocess.CompletedProcess([], 0, b"untracked.txt\0", b""),
        )
        with mock.patch.object(subprocess, "run", side_effect=completed) as run:
            self.assertEqual(changed_paths(), {"old.txt", "new.txt", "untracked.txt"})
        self.assertEqual(
            run.call_args_list[0].args[0],
            ["git", "diff", "--no-renames", "--name-only", "-z", SCOPE_BASE],
        )
        self.assertEqual(
            run.call_args_list[1].args[0],
            ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        )
        with self.assertRaisesRegex(ValueError, "NUL terminated"):
            nul_paths(b"unterminated")
        with self.assertRaisesRegex(ValueError, "valid UTF-8"):
            nul_paths(b"\xff\0")
    def setUp(self) -> None:
        base = comparison_base()
        if base is None:  # pragma: no cover - a resolvable base exists here
            self.fail("no comparison base; the boundary scan cannot run")
        self.base = base
        self.head = head_commit()
        self.changed = changed_paths(base)

    def _require_this_rungs_branch(self) -> None:
        """Skip, named, when there is no branch of THIS rung under test.

        Two situations, and neither is a defect:

        * HEAD is the comparison base -- on `main` after this rung merged
          there is no branch at all;
        * the branch changed things, none of them under this write root --
          it is another rung's branch, and this rung's boundary is not what
          it is testing.

        An earlier version asserted through both, against a diff from the
        fixed `SCOPE_BASE`. That made every rung merged after this one look
        like this rung writing outside its root, so the claim these tests
        make -- "this rung wrote only its own tree and appended to two shared
        files" -- was silently re-read as "nothing in the repository has
        changed since `8dea98da` except this tree". It passed only because
        this rung merged last. WITHDRAWN: the repository's future is not this
        rung's write scope.
        """
        if self.base == self.head:
            self.skipTest(
                f"HEAD is the comparison base ({self.base[:12]}); no branch of "
                "this rung is under test"
            )
        if not self.changed:
            self.fail(
                f"HEAD {self.head[:12]} is ahead of comparison base "
                f"{self.base[:12]}, but the change census is empty; the scope "
                "claim cannot pass vacuously"
            )
        mine = {p for p in self.changed if p.startswith(WRITE_ROOT)}
        if self.changed and not mine:
            self.skipTest(
                f"this branch changed {len(self.changed)} path(s), none under "
                f"{WRITE_ROOT}; it is not this rung's branch"
            )

    def test_no_branch_writes_a_sealed_path(self) -> None:
        """Repository-wide, and therefore NOT scoped to this rung's branch.

        No rung may write a sealed path, so this one claim is checked on
        whatever branch is under test rather than skipped when the branch
        belongs to someone else. It is the half of the old combined test that
        was never this rung's alone.
        """
        sealed = sorted(
            p for p in self.changed
            if any(p.startswith(prefix) for prefix in SEALED)
        )
        self.assertEqual(sealed, [])

    def test_only_write_root_and_two_shared_appends_are_changed(self) -> None:
        self._require_this_rungs_branch()
        self.assertEqual(outside_declared(self.changed), set())

    def test_boundary_predicate_refuses_a_synthetic_outside_path(self) -> None:
        self.assertEqual(
            outside_declared({"research/second_stake/x", "research/outside_probe"}),
            {"research/outside_probe"},
        )

    def test_append_predicate_refuses_a_changed_prefix(self) -> None:
        self.assertFalse(append_only(b"base\n", b"changed\nbase\n"))
        self.assertTrue(append_only(b"base\n", b"base\nappend\n"))

    def test_shared_files_preserve_scope_base_as_exact_prefix(self) -> None:
        """This rung appends to the shared files; it never rewrites them.

        Measured against the COMPARISON BASE, not `SCOPE_BASE`. Against the
        fixed commit the claim was that no rung may ever modify a line of
        `.github/workflows/verify.yml` again -- not even to move its own
        registered test count, which registering a new test requires. That is
        a rule about everyone's future, and it is not this rung's to make.
        Against the comparison base the claim is the one this rung can own:
        whatever else has landed, THIS branch only appended.
        """
        self._require_this_rungs_branch()
        for name in SHARED:
            base = subprocess.run(
                ["git", "show", f"{self.base}:{name}"],
                cwd=REPO,
                capture_output=True,
                check=True,
            ).stdout
            disk = (REPO / pathlib.PurePosixPath(name)).read_bytes().replace(b"\r\n", b"\n")
            self.assertTrue(append_only(base, disk), f"shared file is not append-only: {name}")


class CoverageGateTests(unittest.TestCase):
    @staticmethod
    def report() -> dict[str, object]:
        summary = {
            "covered_lines": 1,
            "missing_lines": 0,
            "num_statements": 1,
            "covered_branches": 1,
            "missing_branches": 0,
            "num_branches": 1,
            "num_partial_branches": 0,
        }
        files = {
            name: {"summary": dict(summary)}
            for name in (
                "generation.py",
                "observables.py",
                "rules.py",
                "run_stake.py",
                "verify_pins.py",
            )
        }
        totals = {name: value * len(files) for name, value in summary.items()}
        return {
            "meta": {
                "timestamp": (dt.datetime.now().astimezone() + dt.timedelta(days=1)).isoformat(),
                "branch_coverage": True,
            },
            "files": files,
            "totals": totals,
        }

    def check(self, report: dict[str, object]) -> list[str]:
        gate = cast(Any, coverage_module())
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "coverage.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            return cast(list[str], gate.check(path))

    def test_valid_synthetic_report_passes(self) -> None:
        self.assertEqual(self.check(self.report()), [])

    def test_new_production_source_enters_the_independent_census(self) -> None:
        gate = cast(Any, coverage_module())
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for name in ("generation.py", "helper.py", "test_helper.py", "check_coverage.py"):
                (root / name).write_text("pass\n", encoding="utf-8")
            with mock.patch.object(gate, "HERE", root):
                self.assertEqual(
                    gate.production_sources(), frozenset({"generation.py", "helper.py"})
                )
                report = self.report()
                report_path = root / "coverage.json"
                report_path.write_text(json.dumps(report), encoding="utf-8")
                failures = cast(list[str], gate.check(report_path))
        self.assertTrue(any("helper.py" in failure for failure in failures))

    def test_branch_metadata_and_freshness_fail_closed(self) -> None:
        for value in (False, None):
            report = self.report()
            meta = cast(dict[str, object], report["meta"])
            if value is None:
                del meta["branch_coverage"]
            else:
                meta["branch_coverage"] = value
            self.assertIn("branch_coverage must be true", self.check(report)[0])
        stale = self.report()
        cast(dict[str, object], stale["meta"])["timestamp"] = "2000-01-01T00:00:00"
        self.assertTrue(
            any("coverage report is stale for" in failure for failure in self.check(stale))
        )

    def test_zero_population_wrong_path_and_counter_injections_fail(self) -> None:
        zero = self.report()
        for record in cast(dict[str, dict[str, object]], zero["files"]).values():
            summary = cast(dict[str, int], record["summary"])
            summary["covered_branches"] = 0
            summary["num_branches"] = 0
        totals = cast(dict[str, int], zero["totals"])
        totals["covered_branches"] = 0
        totals["num_branches"] = 0
        self.assertIn("branch population is empty", self.check(zero)[0])

        duplicate = self.report()
        files = cast(dict[str, object], duplicate["files"])
        files["wrong/generation.py"] = files["generation.py"]
        self.assertIn("basename collision", self.check(duplicate)[0])

        traversal = self.report()
        traversal_files = cast(dict[str, object], traversal["files"])
        traversal_files["../generation.py"] = traversal_files.pop("generation.py")
        self.assertIn("not normalized relative", self.check(traversal)[0])

        arithmetic = self.report()
        arithmetic_files = cast(dict[str, dict[str, object]], arithmetic["files"])
        cast(dict[str, int], arithmetic_files["generation.py"]["summary"])[
            "missing_lines"
        ] = 1
        self.assertIn("line counters do not add up", self.check(arithmetic)[0])

        negative = self.report()
        cast(dict[str, int], negative["totals"])["missing_branches"] = -1
        self.assertIn("nonnegative integer", self.check(negative)[0])

        mismatch = self.report()
        cast(dict[str, int], mismatch["totals"])["covered_lines"] -= 1
        cast(dict[str, int], mismatch["totals"])["missing_lines"] += 1
        self.assertIn("totals do not equal file counters", self.check(mismatch)[0])


class BoundaryScopeSituationTests(unittest.TestCase):
    """The five situations the boundary scan can meet, injected as state.

    They cannot all be staged as real commits from one checkout: once a
    repaired file of this tree is committed, every situation with HEAD ahead
    of the base necessarily carries a change under this write root, so the
    two requiring otherwise are unreachable from here. The scan reads three
    attributes and nothing else, so setting them is exact.

    The situation that CAN be staged for real is the one that mattered -- a
    branch of another rung -- and it is recorded in STATUS.md.
    """

    @staticmethod
    def _case(base: str, head: str, changed: set[str], name: str):
        case = BoundaryTests(name)
        case.base = base
        case.head = head
        case.changed = changed
        return case

    def test_at_the_base_the_write_scope_claim_skips(self) -> None:
        case = self._case(
            "a" * 40, "a" * 40, set(),
            "test_only_write_root_and_two_shared_appends_are_changed",
        )
        with self.assertRaises(unittest.SkipTest) as caught:
            case.test_only_write_root_and_two_shared_appends_are_changed()
        self.assertIn("HEAD is the comparison base", str(caught.exception))

    def test_an_ahead_head_with_an_empty_census_fails_closed(self) -> None:
        case = self._case(
            "a" * 40, "b" * 40, set(),
            "test_only_write_root_and_two_shared_appends_are_changed",
        )
        with self.assertRaises(AssertionError) as caught:
            case.test_only_write_root_and_two_shared_appends_are_changed()
        self.assertIn("change census is empty", str(caught.exception))

    def test_this_rungs_own_branch_is_still_checked(self) -> None:
        case = self._case(
            "a" * 40, "b" * 40, {WRITE_ROOT + "generation.py"},
            "test_only_write_root_and_two_shared_appends_are_changed",
        )
        case.test_only_write_root_and_two_shared_appends_are_changed()
        breach = self._case(
            "a" * 40, "b" * 40,
            {WRITE_ROOT + "generation.py", "research/outside_probe"},
            "test_only_write_root_and_two_shared_appends_are_changed",
        )
        with self.assertRaises(AssertionError):
            breach.test_only_write_root_and_two_shared_appends_are_changed()

    def test_another_rungs_branch_skips_rather_than_failing(self) -> None:
        """The observed failure. A branch doing `second_stream` work owes this
        rung nothing; demanding otherwise made every later rung's work fail
        here, and would have failed every future rung's."""
        case = self._case(
            "a" * 40, "b" * 40, {"research/second_stream/verify_pins.py"},
            "test_only_write_root_and_two_shared_appends_are_changed",
        )
        with self.assertRaises(unittest.SkipTest) as caught:
            case.test_only_write_root_and_two_shared_appends_are_changed()
        self.assertIn("not this rung's branch", str(caught.exception))

    def test_a_sealed_path_fails_on_any_branch_including_a_foreign_one(
        self,
    ) -> None:
        """The half that is NOT scoped. No rung may write a sealed path, so
        this claim is checked on whatever branch is under test -- including
        one that touches nothing of this rung and skips everything else."""
        case = self._case(
            "a" * 40, "b" * 40,
            {"research/second_stream/x.py", "paper/paper.md"},
            "test_no_branch_writes_a_sealed_path",
        )
        with self.assertRaises(AssertionError) as caught:
            case.test_no_branch_writes_a_sealed_path()
        self.assertIn("paper/paper.md", str(caught.exception))
        clean = self._case(
            "a" * 40, "b" * 40, {"research/second_stream/x.py"},
            "test_no_branch_writes_a_sealed_path",
        )
        clean.test_no_branch_writes_a_sealed_path()

    def test_the_append_claim_is_scoped_the_same_way(self) -> None:
        case = self._case(
            "a" * 40, "b" * 40, {"research/second_stream/x.py"},
            "test_shared_files_preserve_scope_base_as_exact_prefix",
        )
        with self.assertRaises(unittest.SkipTest):
            case.test_shared_files_preserve_scope_base_as_exact_prefix()

    def test_the_base_helpers_fail_closed(self) -> None:
        self.assertEqual(len(head_commit()), 40)
        with mock.patch.object(
            subprocess, "run",
            return_value=subprocess.CompletedProcess([], 1, "", "boom"),
        ):
            with self.assertRaises(ValueError):
                head_commit()
            self.assertIsNone(comparison_base())


class ClaimBoundaryTests(unittest.TestCase):
    def test_protected_open_stays_open(self) -> None:
        status = (HERE / "STATUS.md").read_text("utf-8")
        self.assertIn("OB1_UNCHANGED", status)
        barred = (
            "OB-1 is closed",
            "OB-1 is answered",
            "OB-1 is superseded",
            "closes OB-1",
            "answers OB-1",
        )
        for path in claim_files():
            text = strict_scan_text(path)
            for phrase in barred:
                self.assertNotIn(phrase, text, f"{path.name} changes the protected open")

    def test_no_unscoped_totality_or_input_drop_sentence(self) -> None:
        barred = (
            "every possible rule",
            "all endogenous stakes",
            "the stake is now derived",
            "the declared-input count dropped",
            "ALL_SOLUTIONS_FOUND",
        )
        for path in claim_files():
            text = strict_scan_text(path)
            for phrase in barred:
                self.assertNotIn(phrase, text, f"{path.name} carries an unlicensed sentence")

    def test_receipts_have_no_declared_temporal_or_environment_metadata_keys(self) -> None:
        for path in (HERE / "receipts").rglob("*.json"):
            self.assertEqual(
                temporal_or_environment_keys(json.loads(path.read_text("utf-8"))),
                [],
                str(path),
            )
        for path in (HERE / "receipts").rglob("*.json.gz"):
            self.assertEqual(
                temporal_or_environment_keys(json.loads(gzip.decompress(path.read_bytes()))),
                [],
                str(path),
            )

    def test_compressed_receipt_semantic_probe_is_named(self) -> None:
        raw = gzip.compress(
            json.dumps(
                {
                    "nodes": [
                        {
                            "environment": "probe",
                            "created_at": "probe",
                            "datetime": "probe",
                            "hostName": "probe",
                            "platform": "probe",
                            "cwd": "probe",
                            "env": "probe",
                        }
                    ]
                }
            ).encode()
        )
        loaded: object = json.loads(gzip.decompress(raw))
        self.assertEqual(
            temporal_or_environment_keys(loaded),
            [
                "nodes[0].environment",
                "nodes[0].created_at",
                "nodes[0].datetime",
                "nodes[0].hostName",
                "nodes[0].platform",
                "nodes[0].cwd",
                "nodes[0].env",
            ],
        )


if __name__ == "__main__":
    unittest.main()
