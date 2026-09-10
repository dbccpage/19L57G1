"""Negative batteries: the counters and the pin verifier are proved by the
defects they refuse.

Every counter the committed receipt reports as zero is shown here to be
able to fire, and every guard of `verify_pins.py` is shown to fail BY NAME
on the exact malformed manifest it exists to catch.  A verifier is not
proved by a clean run, and a counter reading zero is not evidence unless
it could have read otherwise.
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys
import tempfile
import unittest
from typing import Any, Callable

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import nofirst as nf  # noqa: E402
import run_nofirst as rn  # noqa: E402

# `nofirst` puts sibling trees on the path and one of them carries its own
# `verify_pins`; this tree goes back to the front first.  See the note in
# `nofirst.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import verify_pins as vp  # noqa: E402
from derivation.engine import READINGS  # noqa: E402

SMALL = nf.Alphabet(
    supply_token="<z>",
    fresh_tokens=("<n0>", "<n1>"),
    arities=(1, 2),
    max_data=3,
    max_forms=1,
    max_length=2,
)
L = READINGS[0]


class FailureCounterTests(unittest.TestCase):
    """Every counter the receipt reports as zero, shown able to fire."""

    def test_a_broken_free_stake_is_counted(self) -> None:
        broken = nf.Stake("free", lambda i, j: nf.APART)
        payload = rn.measure_reading("L", L.genesis, (broken,), SMALL, 1)
        self.assertGreater(
            payload["demands"]["free_stake_nodes_with_a_demand"], 0
        )

    def test_an_unstable_stake_trips_totality_and_agreement(self) -> None:
        """A stake whose rule is not a function of the pair alone is caught
        by the totality counter, by the unlabelled-pair counter, and by the
        first-demand agreement counter."""
        state = {"n": 0}

        def unstable(i: int, j: int) -> str:
            state["n"] += 1
            return (nf.APART, nf.SAME, nf.FREE)[state["n"] % 3]

        payload = rn.measure_reading(
            "L", L.genesis, (nf.Stake("unstable", unstable),), SMALL, 1
        )
        self.assertGreater(payload["demands"]["totality_mismatches"], 0)
        self.assertGreater(
            payload["demands"]["demands_at_an_unlabelled_pair"], 0
        )
        self.assertFalse(
            payload["first_demand"]["unstable"][
                "index_agrees_with_first_dishonoured"
            ]
        )

    def test_the_enumerator_counts_a_grammar_refusal(self) -> None:
        """The declared alphabet offers only events the sealed grammar
        accepts, so the committed receipt's refusal count is zero.  That is
        a property of the alphabet and not a dead branch: an alphabet
        declaring a form of arity zero makes the sealed model refuse, and
        the enumerator counts the refusal instead of failing."""
        _, _, refusals = nf.enumerate_rectangle(L.genesis, SMALL)
        self.assertEqual(refusals, 0)
        bad = nf.Alphabet("<z>", ("<a>",), (0,), 3, 1, 1)
        nodes, _, refusals2 = nf.enumerate_rectangle(L.genesis, bad)
        self.assertGreater(refusals2, 0)
        reach, _ = nf.enumerate_by_levels(L.genesis, bad, 1)
        self.assertEqual(reach, frozenset(n.regime for n in nodes))

    def test_runner_main_returns_zero_and_writes_where_told(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            argv = sys.argv
            sys.argv = ["run_nofirst.py", "--receipts", tmp]
            try:
                self.assertEqual(rn.main(), 0)
            finally:
                sys.argv = argv
            self.assertTrue((pathlib.Path(tmp) / "nofirst.json").exists())


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
            p["absent_at_snapshot"][0]["present_at_snapshot"] = False

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


if __name__ == "__main__":
    unittest.main()
