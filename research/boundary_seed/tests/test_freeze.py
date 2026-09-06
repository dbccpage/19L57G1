"""Temporary-repository injections for the source-custody boundary."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests import test_blind
import verify_pins

from verify_freeze import (
    COMPARISON, MARKER, REL, audit, blobs, git, marker_bytes, tree, write_marker,
)


class FreezeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="boundary-freeze-probe-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q")
        self.write(f"{REL}/.gitattributes", b"FREEZE.md -text\n")
        self.write(f"{REL}/source.txt", b"source bytes\n")
        self.commit("initial source")
        self.source = git(self.root, "rev-parse", "HEAD").decode().strip()

    def write(self, path: str, data: bytes) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self, message: str) -> None:
        # This is a new disposable fixture, not a user checkout.
        git(self.root, "add", "--", REL)
        git(
            self.root, "-c", "user.name=Source custody probe", "-c",
            "user.email=probe@example.invalid", "-c", "commit.gpgsign=false",
            "commit", "-qm", message,
        )

    def freeze(self) -> None:
        write_marker(self.root)
        self.commit("dedicated source freeze")
        result = audit(self.root)
        self.assertTrue(result.frozen, result.problems)

    def merge(self, branch: str) -> None:
        git(
            self.root, "-c", "user.name=Source custody probe", "-c",
            "user.email=probe@example.invalid", "-c", "commit.gpgsign=false",
            "merge", "--no-ff", "-qm", "merge fixture branch", branch,
        )

    def assert_fails(self, needle: str) -> None:
        result = audit(self.root)
        self.assertFalse(result.frozen)
        self.assertIn(needle, "\n".join(result.problems))

    def test_absence_is_not_a_freeze_and_source_can_still_change(self) -> None:
        self.write(f"{REL}/new.txt", b"still deriving\n")
        result = audit(self.root)
        self.assertFalse(result.frozen)
        self.assertEqual(result.problems, ())
        with self.assertRaisesRegex(ValueError, "pending paths"):
            write_marker(self.root)

    def test_bare_working_and_staged_marker_cannot_retire_scan(self) -> None:
        self.write(MARKER, b"finished\n")
        self.assert_fails("uncommitted file")
        git(self.root, "add", "--", MARKER)
        self.assert_fails("uncommitted file")

    def test_valid_manifest_allows_only_later_comparison(self) -> None:
        self.freeze()
        self.write(COMPARISON, b"post-freeze comparison\n")
        self.assertTrue(audit(self.root).frozen)
        self.commit("comparison after source freeze")
        self.assertTrue(audit(self.root).frozen)
        with self.assertRaisesRegex(ValueError, "already frozen"):
            write_marker(self.root)

    def test_incomplete_wrong_typed_or_noncanonical_manifest_is_rejected(self) -> None:
        original = marker_bytes(self.root, self.source)
        mutations = (
            original.replace(b'"files": [', b'"files": [], "omitted": ['),
            original.replace(b'"bytes": 13', b'"bytes": true'),
            original.replace(b'"source.txt"', b'"../source.txt"'),
            original.replace(b'"100644"', b'"100755"', 1),
            original.replace(b'"schema":', b'"schema": "duplicate", "schema":', 1),
            original.replace(b'"sha256": "', b'"sha256": "0', 1),
            original.replace(b'"source_commit": "', b'"source_commit": "0', 1),
            original.replace(b"\n", b"\r\n"),
            b"finished\n",
        )
        # Audit each candidate as the marker's actual committed blob without
        # adopting a defective source baseline or regenerating any receipt.
        self.freeze()
        for candidate in mutations:
            with self.subTest(candidate=candidate[:60]):
                self.assertNotEqual(candidate, original)
                real_blobs = blobs
                marker_oid = tree(self.root, "HEAD")[MARKER].oid

                def injected(root: Path, identifiers: list[str]) -> dict[str, bytes]:
                    found = real_blobs(root, identifiers)
                    if marker_oid in found:
                        found[marker_oid] = candidate
                    return found

                with patch("verify_freeze.blobs", side_effect=injected):
                    self.assert_fails("complete parent manifest")
                self.assertTrue(audit(self.root).frozen)

    def test_real_committed_empty_marker_does_not_freeze(self) -> None:
        self.write(MARKER, b"finished\n")
        self.commit("invalid marker")
        self.assert_fails("complete parent manifest")

    def test_source_and_marker_in_same_commit_fail(self) -> None:
        self.write(MARKER, marker_bytes(self.root, self.source))
        self.write(f"{REL}/source.txt", b"changed with marker\n")
        self.commit("not a dedicated marker")
        self.assert_fails("dedicated commit")

    def test_pre_freeze_comparison_then_deletion_stays_visible(self) -> None:
        self.write(COMPARISON, b"too early\n")
        self.commit("premature comparison")
        (self.root / COMPARISON).unlink()
        self.commit("remove premature comparison")
        self.assert_fails("before a committed freeze")
        with self.assertRaisesRegex(ValueError, "before a committed freeze"):
            write_marker(self.root)

    def test_post_freeze_change_and_reversion_still_fail(self) -> None:
        self.freeze()
        self.write(f"{REL}/source.txt", b"changed after freeze\n")
        self.commit("source changed")
        self.assert_fails("source.txt: source changed")
        self.write(f"{REL}/source.txt", b"source bytes\n")
        self.commit("source reverted")
        self.assert_fails("source.txt: source changed")

    def test_index_working_and_untracked_source_changes_fail_then_recover(self) -> None:
        self.freeze()
        self.write(f"{REL}/source.txt", b"changed\n")
        self.assert_fails("source.txt: source changed")
        git(self.root, "add", "--", f"{REL}/source.txt")
        self.write(f"{REL}/source.txt", b"source bytes\n")
        self.assert_fails("source.txt: source changed")
        git(self.root, "add", "--", f"{REL}/source.txt")
        self.assertTrue(audit(self.root).frozen)
        self.write(f"{REL}/zzz_probe.txt", b"new source\n")
        self.assert_fails("zzz_probe.txt: source changed")
        (self.root / REL / "zzz_probe.txt").unlink()
        self.assertTrue(audit(self.root).frozen)

    def test_deleted_marker_and_recreation_do_not_erase_history(self) -> None:
        self.freeze()
        saved = (self.root / MARKER).read_bytes()
        (self.root / MARKER).unlink()
        self.commit("marker deleted")
        self.assert_fails("FREEZE.md: source changed")
        self.write(MARKER, saved)
        self.commit("marker recreated")
        self.assert_fails("expected one creation commit, found 2")

    def test_shallow_history_fails_closed(self) -> None:
        self.freeze()
        real_git = git

        def shallow(root: Path, *args: str, data: bytes | None = None) -> bytes:
            if args == ("rev-parse", "--is-shallow-repository"):
                return b"true\n"
            return real_git(root, *args, data=data)

        with patch("verify_freeze.git", side_effect=shallow):
            self.assert_fails("shallow history")
        self.assertTrue(audit(self.root).frozen)

    def test_git_unchanged_flags_cannot_hide_revised_working_bytes(self) -> None:
        self.freeze()
        for flag in ("assume-unchanged", "skip-worktree"):
            with self.subTest(flag=flag):
                git(self.root, "update-index", f"--{flag}", "--", f"{REL}/source.txt")
                self.write(f"{REL}/source.txt", b"unscanned revised source\n")
                self.assert_fails("source.txt: source changed")
                self.write(f"{REL}/source.txt", b"source bytes\n")
                git(self.root, "update-index", f"--no-{flag}", "--", f"{REL}/source.txt")
                self.assertTrue(audit(self.root).frozen)

    def test_generation_rejects_hidden_dirty_source_without_creating_marker(self) -> None:
        git(self.root, "update-index", "--assume-unchanged", "--", f"{REL}/source.txt")
        self.write(f"{REL}/source.txt", b"hidden revision\n")
        with self.assertRaisesRegex(ValueError, "requires unchanged source"):
            write_marker(self.root)
        self.assertFalse((self.root / MARKER).exists())

    def test_merged_side_history_and_replacements_cannot_hide_prior_defects(self) -> None:
        original_branch = git(self.root, "branch", "--show-current").decode().strip()
        git(self.root, "switch", "-qc", "history_probe")
        sibling = "probe_hidden_sibling"
        sibling_path = f"research/{sibling}/probe.txt"
        self.write(f"{REL}/source.txt", sibling.encode() + b"\n")
        self.write(sibling_path, b"name census fixture\n")
        self.write(COMPARISON, b"premature comparison\n")
        git(self.root, "add", "--", sibling_path)
        self.commit("side history defects")
        bad = git(self.root, "rev-parse", "HEAD").decode().strip()
        self.write(f"{REL}/source.txt", b"source bytes\n")
        (self.root / sibling_path).unlink()
        (self.root / COMPARISON).unlink()
        git(self.root, "add", "--", sibling_path)
        self.commit("side history reverted")
        git(self.root, "switch", "-q", original_branch)
        self.merge("history_probe")
        for replaced in (False, True):
            with self.subTest(replaced=replaced):
                if replaced:
                    git(
                        self.root, "-c", "user.name=Source custody probe", "-c",
                        "user.email=probe@example.invalid", "replace", "--graft", "HEAD", self.source,
                    )
                self.assert_fails("before a committed freeze")
                with patch.object(test_blind, "ROOT", self.root):
                    self.assertIn(sibling, test_blind.historical_other_trees())
                    problems, frozen = test_blind.scan_committed_history()
                self.assertFalse(frozen)
                self.assertTrue(any("other research tree " + sibling in p for p in problems))
                with patch.object(verify_pins, "ROOT", self.root):
                    self.assertIn(bad, verify_pins.history("source.txt"))

    def test_parallel_edit_and_reversion_are_newly_reachable_source(self) -> None:
        self.freeze()
        original_branch = git(self.root, "branch", "--show-current").decode().strip()
        git(self.root, "switch", "-qc", "parallel_probe", self.source)
        self.write(f"{REL}/source.txt", b"parallel revision\n")
        self.commit("parallel source changed")
        self.write(f"{REL}/source.txt", b"source bytes\n")
        self.commit("parallel source reverted")
        git(self.root, "switch", "-q", original_branch)
        self.merge("parallel_probe")
        self.assert_fails("source.txt: source changed")

    def test_parallel_entire_source_deletion_and_recovery_are_not_ignored(self) -> None:
        self.freeze()
        original_branch = git(self.root, "branch", "--show-current").decode().strip()
        git(self.root, "switch", "-qc", "deletion_probe", self.source)
        saved = {path: (self.root / path).read_bytes() for path in tree(self.root, "HEAD")}
        for path in saved:
            (self.root / path).unlink()
        self.commit("parallel source deleted")
        for path, data in saved.items():
            self.write(path, data)
        self.commit("parallel source restored")
        git(self.root, "switch", "-q", original_branch)
        self.merge("deletion_probe")
        self.assert_fails("newly reachable history deletes the source root")

    def test_dangling_untracked_symlink_is_not_skipped_before_refusal(self) -> None:
        missing = f"{REL}/zzz_dangling_probe"
        with (
            patch.object(test_blind, "ROOT", self.root),
            patch.object(test_blind, "working_paths", return_value=[missing]),
            patch.object(Path, "is_symlink", return_value=True),
        ):
            problems = test_blind.scan_index_and_working()
        self.assertIn(f"{missing}: symlink cannot be blind-scanned", problems)

    def test_manifest_requires_exact_sha_nonempty_source_and_byte_attribute(self) -> None:
        with self.assertRaisesRegex(ValueError, "exact full commit"):
            marker_bytes(self.root, "HEAD")
        with patch("verify_freeze.tree", return_value={}):
            with self.assertRaisesRegex(ValueError, "population is empty"):
                marker_bytes(self.root, self.source)
        self.write(f"{REL}/.gitattributes", b"FREEZE.md text\n")
        self.commit("remove byte attribute")
        head = git(self.root, "rev-parse", "HEAD").decode().strip()
        with self.assertRaisesRegex(ValueError, "marked -text"):
            marker_bytes(self.root, head)

    def test_real_invalid_marker_keeps_comparison_in_source_scan(self) -> None:
        self.write(MARKER, b"finished\n")
        self.commit("invalid marker")
        self.write(COMPARISON, ("paper/" + "zzz_probe.md\n").encode())
        self.commit("comparison after invalid marker")
        with patch.object(test_blind, "ROOT", self.root):
            problems, frozen = test_blind.scan_committed_history()
        self.assertFalse(frozen)
        self.assertTrue(any("complete parent manifest" in p for p in problems))
        self.assertTrue(any("comparison.md:1: citation" in p for p in problems))

    def test_valid_freeze_scans_prior_versions_but_not_later_comparison(self) -> None:
        self.freeze()
        self.write(COMPARISON, ("paper/" + "zzz_probe.md\n").encode())
        self.commit("permitted post-freeze comparison")
        with patch.object(test_blind, "ROOT", self.root):
            problems, frozen = test_blind.scan_committed_history()
        self.assertTrue(frozen)
        self.assertEqual(problems, [])

    def test_batch_scan_preserves_each_path_and_historical_reverted_defect(self) -> None:
        probe = ("paper/" + "zzz_probe.md\n").encode()
        self.write(f"{REL}/first.txt", probe)
        self.write(f"{REL}/second.txt", probe)
        self.commit("two paths sharing one defective blob")
        with patch.object(test_blind, "ROOT", self.root):
            got, _ = test_blind.scan_snapshot("HEAD", "probe", [])
            expected = []
            for path in test_blind.tree_paths("HEAD"):
                expected.extend(test_blind.scan_bytes(
                    git(self.root, "show", f"HEAD:{path}"),
                    f"probe:{path}", test_blind.all_patterns([]),
                ))
        self.assertEqual(got, expected)
        self.assertEqual(len(got), 2)
        self.write(f"{REL}/first.txt", b"repaired\n")
        self.write(f"{REL}/second.txt", b"repaired\n")
        self.commit("repair current source")
        with patch.object(test_blind, "ROOT", self.root):
            problems, frozen = test_blind.scan_committed_history()
        self.assertFalse(frozen)
        self.assertTrue(any("first.txt:1: citation" in p for p in problems))
        self.assertTrue(any("second.txt:1: citation" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
