"""Negative battery: the pin verifier is proved by the defects it refuses.

Every guard of `verify_pins.py` is shown to fail BY NAME on the exact
malformed manifest it exists to catch, and the repin path is exercised
against a COPY so that no committed pin is rewritten by a test.  A
verifier is not proved by a clean run.

A hand copy of `research/second_index/test_pins.py`, with this rung's
manifest; the guards exercised are unchanged, and the three tests of the
manifest's population are this rung's own.
"""

from __future__ import annotations

import copy
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from typing import Any, Callable

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import iso_index as ix  # noqa: E402

# `iso_index` puts sibling trees on the path and each of them carries its
# own `verify_pins`; this tree goes back to the front first.  See the note
# in `iso_index.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import verify_pins as vp  # noqa: E402


class ManifestShapeTests(unittest.TestCase):
    def test_the_committed_manifest_verifies(self) -> None:
        lines = vp.verify()
        self.assertTrue(any(line.startswith("source:") for line in lines))
        self.assertTrue(any(line.startswith("span:") for line in lines))
        self.assertTrue(any(line.startswith("frozen:") for line in lines))

    def test_every_reconstructed_source_is_pinned_whole_and_by_span(self) -> None:
        """The four reconstruction modules name four sealed modules, two
        modules of the track-one sibling and one of rung three; each must
        appear in the manifest both as a blob and as at least one span,
        because the two pins say different things."""
        manifest = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        blobs = {item["path"] for item in manifest["sources"]}
        spanned = {item["path"] for item in manifest["spans"]}
        for path in (
            "lean4/Derivation/Basic.lean",
            "lean4/Derivation/Inertia.lean",
            "lean4/Derivation/Minimality.lean",
            "lean4/Derivation/IsoCollapse.lean",
            "research/second_nofirst/lean/SecondNoFirst/Stake.lean",
            "research/second_nofirst/lean/SecondNoFirst/NoFirst.lean",
            "research/second_index/lean/SecondIndex/Index.lean",
        ):
            self.assertIn(path, blobs)
            self.assertIn(path, spanned)

    def test_the_consumed_python_sources_are_pinned(self) -> None:
        """`iso_index.py` imports the sealed kernel, the sealed isomorphism
        procedure and two rungs; all are pinned by blob, and nothing of any
        of them is copied."""
        manifest = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        blobs = {item["path"] for item in manifest["sources"]}
        for path in (
            "code/derivation/model.py",
            "code/derivation/engine.py",
            "code/derivation/observe.py",
            "code/derivation/iso.py",
            "research/second_nofirst/nofirst.py",
            "research/second_index/index.py",
            "research/two_sided_commitment/two_sided.py",
        ):
            self.assertIn(path, blobs)
        source = (HERE / "iso_index.py").read_text(encoding="utf-8")
        self.assertIn("from index import", source)
        self.assertIn("from derivation.iso import", source)
        for copied in ("def enumerate_rectangle(", "def first_index_forward(",
                       "def canonical(", "def _refine("):
            self.assertNotIn(copied, source)

    def test_the_rung_three_counts_this_rung_replays_are_pinned(self) -> None:
        manifest = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        blobs = {item["path"] for item in manifest["sources"]}
        self.assertIn("research/second_index/receipts/index.json", blobs)


class PinFailureTests(unittest.TestCase):
    """One malformed manifest per guard, each failing by name."""

    def _fails(self, mutate: Callable[[dict[str, Any]], None]) -> str:
        original = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        payload = copy.deepcopy(original)
        mutate(payload)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "SOURCE_MANIFEST.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            saved = vp.MANIFEST
            vp.MANIFEST = path
            try:
                with self.assertRaises(ValueError) as caught:
                    vp.verify()
                return str(caught.exception)
            finally:
                vp.MANIFEST = saved

    def test_a_short_snapshot_is_refused(self) -> None:
        self.assertIn(
            "40-digit", self._fails(lambda p: p.__setitem__("snapshot_commit", "abc"))
        )

    def test_a_non_ancestor_snapshot_is_refused(self) -> None:
        self.assertIn(
            "of HEAD",
            self._fails(lambda p: p.__setitem__("snapshot_commit", "0" * 40)),
        )

    def test_an_empty_source_list_is_refused(self) -> None:
        self.assertIn(
            "at least one consumed source",
            self._fails(lambda p: p.__setitem__("sources", [])),
        )

    def test_a_moved_source_is_named(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["sources"][0]["sha256"] = "0" * 64

        msg = self._fails(mutate)
        self.assertIn("hash mismatch at the snapshot", msg)
        wanted = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )["sources"][0]["path"]
        self.assertIn(wanted, msg)

    def test_a_source_without_a_hash_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            del p["sources"][0]["sha256"]

        self.assertIn("missing sha256", self._fails(mutate))

    def test_a_source_entry_that_is_not_an_object_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["sources"][0] = "not an object"

        self.assertIn("must be an object", self._fails(mutate))

    def test_an_unsafe_source_path_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["sources"][0]["path"] = "../outside.txt"

        self.assertIn("unsafe path", self._fails(mutate))

    def test_an_empty_source_path_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["sources"][0]["path"] = ""

        self.assertIn("non-empty string", self._fails(mutate))

    def test_an_empty_span_list_is_refused(self) -> None:
        self.assertIn(
            "at least one span", self._fails(lambda p: p.__setitem__("spans", []))
        )

    def test_a_moved_span_is_named(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["spans"][0]["sha256"] = "0" * 64

        self.assertIn("span mismatch at the snapshot", self._fails(mutate))

    def test_span_bounds_out_of_order_are_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["spans"][0]["first_line"] = 9
            p["spans"][0]["last_line"] = 1

        self.assertIn("bounds out of order", self._fails(mutate))

    def test_a_span_past_the_end_of_its_file_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["spans"][0]["last_line"] = 1000000

        self.assertIn("runs past the end", self._fails(mutate))

    def test_a_span_without_a_hash_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            del p["spans"][0]["sha256"]

        self.assertIn("missing span sha256", self._fails(mutate))

    def test_a_span_entry_that_is_not_an_object_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["spans"][0] = 7

        self.assertIn("must be an object", self._fails(mutate))

    def test_a_span_line_that_is_not_an_integer_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["spans"][0]["first_line"] = "3"

        self.assertIn("must be an integer", self._fails(mutate))

    def test_a_wrong_absence_record_is_named(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["absent_at_snapshot"][0]["present_at_snapshot"] = True

        self.assertIn("absent-at-snapshot record wrong", self._fails(mutate))

    def test_a_missing_absence_list_is_refused(self) -> None:
        self.assertIn(
            "absent_at_snapshot", self._fails(lambda p: p.pop("absent_at_snapshot"))
        )

    def test_an_absent_entry_that_is_not_an_object_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["absent_at_snapshot"] = ["nope"]

        self.assertIn("must be an object", self._fails(mutate))

    def test_a_moved_frozen_text_is_named(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["frozen_texts"][0]["sha256"] = "0" * 64

        self.assertIn("frozen text moved", self._fails(mutate))

    def test_an_empty_frozen_list_is_refused(self) -> None:
        self.assertIn(
            "frozen texts", self._fails(lambda p: p.__setitem__("frozen_texts", []))
        )

    def test_a_frozen_entry_without_a_hash_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            del p["frozen_texts"][0]["sha256"]

        self.assertIn("missing sha256", self._fails(mutate))

    def test_a_frozen_entry_that_is_not_an_object_is_refused(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["frozen_texts"] = [3]

        self.assertIn("must be an object", self._fails(mutate))

    def test_a_manifest_that_is_not_an_object_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "m.json"
            path.write_text("[]", encoding="utf-8")
            saved = vp.MANIFEST
            vp.MANIFEST = path
            try:
                with self.assertRaises(ValueError) as caught:
                    vp.verify()
                self.assertIn("must be an object", str(caught.exception))
            finally:
                vp.MANIFEST = saved

    def test_a_missing_file_fails_the_git_read(self) -> None:
        def mutate(p: dict[str, Any]) -> None:
            p["sources"][0]["path"] = "research/second_iso/not_a_file.txt"

        self.assertIn("git show", self._fails(mutate))


class AncestryTests(unittest.TestCase):
    """The three answers `_ancestor` can give, each from a real commit.

    An unknown identifier is UNDECIDED, not "not an ancestor": git exits
    with a status other than zero or one, and conflating the two would
    report a missing commit as a moved one.  A commit that exists and is
    not an ancestor is the third case, and it is built here with
    `git commit-tree`, which writes one unreferenced object and touches no
    ref, no index and no working file.
    """

    def test_the_committed_snapshot_is_an_ancestor(self) -> None:
        manifest = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        self.assertEqual(vp._ancestor(manifest["snapshot_commit"]), "ancestor")

    def test_an_unknown_commit_is_undecided(self) -> None:
        self.assertIn("undecided", vp._ancestor("0" * 40))

    def test_a_real_commit_off_this_line_is_not_an_ancestor(self) -> None:
        tree = subprocess.run(
            ["git", "rev-parse", "HEAD^{tree}"],
            capture_output=True, text=True, cwd=vp.REPO, check=True,
        ).stdout.strip()
        made = subprocess.run(
            ["git", "commit-tree", tree, "-m", "pin verifier probe"],
            capture_output=True, text=True, cwd=vp.REPO, check=True,
            env={**os.environ,
                 "GIT_AUTHOR_NAME": "probe", "GIT_AUTHOR_EMAIL": "probe@invalid",
                 "GIT_COMMITTER_NAME": "probe", "GIT_COMMITTER_EMAIL": "probe@invalid",
                 "GIT_AUTHOR_DATE": "@0 +0000", "GIT_COMMITTER_DATE": "@0 +0000"},
        ).stdout.strip()
        self.assertEqual(len(made), 40)
        self.assertEqual(vp._ancestor(made), "not an ancestor")


class PinRepinTests(unittest.TestCase):
    def _repin_of(self, payload: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "SOURCE_MANIFEST.json"
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            saved = vp.MANIFEST
            vp.MANIFEST = path
            try:
                lines = vp.repin()
            finally:
                vp.MANIFEST = saved
            return lines, json.loads(path.read_text(encoding="utf-8"))

    def test_repin_rewrites_hashes_and_leaves_frozen_texts_alone(self) -> None:
        """A repin is a logged act, run here against a COPY with one source
        hash and one span hash deliberately stale, so it has something to
        report and the frozen texts are seen to survive it."""
        original = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        payload = copy.deepcopy(original)
        payload["sources"][0]["sha256"] = "0" * 64
        payload["spans"][0]["sha256"] = "0" * 64
        lines, after = self._repin_of(payload)
        self.assertTrue(any(line.startswith("rehashed:") for line in lines))
        self.assertTrue(any(line.startswith("rehashed span:") for line in lines))
        self.assertEqual(
            after["sources"][0]["sha256"], original["sources"][0]["sha256"]
        )
        self.assertEqual(after["spans"][0]["sha256"], original["spans"][0]["sha256"])
        self.assertEqual(after["frozen_texts"], original["frozen_texts"])

    def test_a_clean_repin_reports_only_its_own_warning(self) -> None:
        original = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        lines, _ = self._repin_of(copy.deepcopy(original))
        self.assertEqual(len(lines), 1)
        self.assertIn("re-read by hand", lines[0])

    def _repin_refuses(self, payload: dict[str, Any]) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "m.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            saved = vp.MANIFEST
            vp.MANIFEST = path
            try:
                with self.assertRaises(ValueError):
                    vp.repin()
            finally:
                vp.MANIFEST = saved

    def test_repin_refuses_a_manifest_without_sources(self) -> None:
        self._repin_refuses({"sources": {}})

    def test_repin_refuses_a_non_object_source_entry(self) -> None:
        self._repin_refuses({"sources": [2]})

    def test_repin_refuses_a_manifest_without_spans(self) -> None:
        self._repin_refuses({"sources": [], "spans": {}})

    def test_repin_refuses_a_non_object_span_entry(self) -> None:
        self._repin_refuses({"sources": [], "spans": [1]})


class HeadDriftTests(unittest.TestCase):
    """2026-09-24: a source or span that moved at HEAD is drift, reported
    and not failed; `--require-current` restores the failure by name."""

    def _moved_at_head(self, which: str) -> Callable[..., bytes]:
        original = vp._git_bytes
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        target = manifest["sources"][0]["path"] if which == "source" else manifest["spans"][0]["path"]

        def fake(*args: str) -> bytes:
            if args[:1] == ("show",) and args[1] == f"HEAD:{target}":
                return b"moved at HEAD\n" * 2000
            return original(*args)

        return fake

    def test_a_source_moved_at_head_is_drift(self) -> None:
        from unittest import mock

        with mock.patch.object(vp, "_git_bytes", side_effect=self._moved_at_head("source")):
            lines = vp.verify()
            self.assertTrue(any(line.startswith("DRIFT: source moved at HEAD") for line in lines))
            self.assertRegex(lines[-1], r"^drift since the snapshot: [1-9]")
            with self.assertRaisesRegex(ValueError, "--require-current"):
                vp.verify(require_current=True)

    def test_a_span_moved_at_head_is_drift(self) -> None:
        from unittest import mock

        with mock.patch.object(vp, "_git_bytes", side_effect=self._moved_at_head("span")):
            lines = vp.verify()
        self.assertTrue(any(line.startswith("DRIFT: span moved at HEAD") for line in lines))

    def test_unreadable_and_absent_at_head(self) -> None:
        from unittest import mock

        original = vp._git_bytes
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        source = manifest["sources"][0]["path"]
        span = manifest["spans"][0]["path"]

        def unreadable(path: str) -> Callable[..., bytes]:
            def fake(*args: str) -> bytes:
                if args[:1] == ("show",) and args[1] == f"HEAD:{path}":
                    raise ValueError("git show failed: unreadable")
                return original(*args)

            return fake

        for path in (source, span):
            with mock.patch.object(vp, "_git_bytes", side_effect=unreadable(path)):
                with self.assertRaisesRegex(ValueError, "could not read"):
                    vp.verify()
            with mock.patch.object(vp, "_git_bytes", side_effect=unreadable(path)), \
                    mock.patch.object(vp, "_tracked_at_head", return_value=False):
                lines = vp.verify()
            self.assertTrue(any(line.startswith("DRIFT: ") for line in lines), path)

    def test_main_accepts_require_current(self) -> None:
        argv = sys.argv
        sys.argv = ["verify_pins.py", "--require-current"]
        try:
            self.assertEqual(vp.main(), 0)
        finally:
            sys.argv = argv


class VerifierEntryPointTests(unittest.TestCase):
    def test_main_reports_a_failure_and_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "m.json"
            path.write_text(json.dumps({"snapshot_commit": "x"}), encoding="utf-8")
            saved, argv = vp.MANIFEST, sys.argv
            vp.MANIFEST = path
            sys.argv = ["verify_pins.py"]
            try:
                self.assertEqual(vp.main(), 1)
            finally:
                vp.MANIFEST, sys.argv = saved, argv

    def test_main_passes_on_the_committed_manifest(self) -> None:
        argv = sys.argv
        sys.argv = ["verify_pins.py"]
        try:
            self.assertEqual(vp.main(), 0)
        finally:
            sys.argv = argv

    def test_main_can_repin_a_copy(self) -> None:
        original = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "m.json"
            path.write_text(json.dumps(original, indent=2), encoding="utf-8")
            saved, argv = vp.MANIFEST, sys.argv
            vp.MANIFEST = path
            sys.argv = ["verify_pins.py", "--repin"]
            try:
                self.assertEqual(vp.main(), 0)
            finally:
                vp.MANIFEST, sys.argv = saved, argv

    def test_the_rung_module_is_not_shadowed_by_a_sibling(self) -> None:
        """`iso_index.py` consumes three sibling trees that carry modules
        of the same names as this rung's.  The verifier under test must be this
        rung's, and the surest witness is that it reads this manifest."""
        self.assertEqual(vp.HERE, HERE)
        self.assertEqual(ix.HERE, HERE)
        self.assertTrue(str(vp.MANIFEST).startswith(str(HERE)))


if __name__ == "__main__":
    unittest.main()
