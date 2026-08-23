"""Tests for the blind-restart kernel, its key, and its scorer.

The scorer and the leak gate are the objects under test. The kernel is
prose and the solver is outside the machine; neither is testable here,
and STATUS.md says so rather than implying otherwise by testing around
them.
"""

from __future__ import annotations

import copy
import json
import pathlib
import tempfile
import unittest
from typing import Any
from unittest import mock

import score_packet
import scoring_key
import verify_pins

HERE = pathlib.Path(__file__).resolve().parent


def _perfect_packet() -> dict[str, Any]:
    return copy.deepcopy(scoring_key.expected())


class KeyTests(unittest.TestCase):
    def test_key_resolves_every_declared_field(self) -> None:
        resolved = scoring_key.expected()
        self.assertEqual(set(resolved), {s.stage_id for s in scoring_key.STAGES})
        for stage in scoring_key.STAGES:
            self.assertEqual(
                set(resolved[stage.stage_id]), {f.name for f in stage.fields}
            )

    def test_key_reads_its_values_rather_than_restating_them(self) -> None:
        """Change the artifact; the key must follow.

        Tested behaviourally, on purpose. The obvious version of this
        check greps the key's source for each rendered value and asserts
        absence -- but a single-digit value makes that match any line
        number, slice index or version string in the file, and
        ``paper/anti_skill_inbox.md`` records "count by grepping" as a
        failure mode this repository has already suffered twice. Mutating
        the input and watching the output move proves the dependency the
        grep only gestured at.
        """

        original = scoring_key.expected()
        with tempfile.TemporaryDirectory() as tmp:
            staged = pathlib.Path(tmp)
            for name in scoring_key.artifact_names():
                payload = scoring_key.load_artifact(name)
                (staged / name).write_text(
                    json.dumps(payload), encoding="utf-8"
                )
            probe = json.loads((staged / "challenges.json").read_text("utf-8"))
            probe["challenge0"]["context_count"] = 4242
            (staged / "challenges.json").write_text(
                json.dumps(probe), encoding="utf-8"
            )
            with mock.patch.object(scoring_key, "ARTIFACTS", staged):
                moved = scoring_key.expected()

        self.assertEqual(moved["inertia"]["context_count"], 4242)
        self.assertNotEqual(
            original["inertia"]["context_count"],
            moved["inertia"]["context_count"],
            "the key did not follow the artifact; it is restating a value",
        )

    def test_missing_field_fails_by_name(self) -> None:
        bogus = scoring_key.Field(
            "probe", "challenges.json", ("challenge0", "zzz_probe_absent")
        )
        stage = scoring_key.Stage("probe", "d", (), (bogus,))
        with mock.patch.object(scoring_key, "STAGES", (stage,)):
            with self.assertRaises(ValueError) as caught:
                scoring_key.expected()
        self.assertIn("zzz_probe_absent", str(caught.exception))

    def test_empty_stage_population_is_refused(self) -> None:
        with mock.patch.object(scoring_key, "STAGES", ()):
            with self.assertRaises(ValueError) as caught:
                scoring_key.expected()
        self.assertIn("empty", str(caught.exception))

    def test_every_artifact_the_key_reads_is_pinned(self) -> None:
        pins = json.loads((HERE / "SOURCE_PINS.json").read_text(encoding="utf-8"))
        pinned = {pathlib.PurePosixPath(a["path"]).name for a in pins["artifacts"]}
        self.assertEqual(set(scoring_key.artifact_names()) - pinned, set())


class ScoreTests(unittest.TestCase):
    def test_perfect_packet_passes(self) -> None:
        lines, ok = score_packet.score(_perfect_packet())
        self.assertTrue(ok, "\n".join(lines))
        self.assertIn("25 of 25", lines[-1])

    def test_wrong_value_fails_and_names_the_field(self) -> None:
        packet = _perfect_packet()
        packet["cost_floor"]["minimum_cost.L"] = [1, -1]
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok)
        self.assertTrue(
            any("cost_floor.minimum_cost.L" in line and "FAIL" in line for line in lines),
            "\n".join(lines),
        )

    def test_claiming_a_unique_minimum_fails(self) -> None:
        """The tie under the first measure is the load-bearing one."""

        packet = _perfect_packet()
        packet["tie_under_first_measure"]["tie_classes.F"] = 1
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok)
        self.assertTrue(
            any("tie_under_first_measure.tie_classes.F" in line for line in lines)
        )

    def test_empty_packet_fails_on_totality(self) -> None:
        lines, ok = score_packet.score({})
        self.assertFalse(ok, "an empty packet must never score as a pass")
        absent = [line for line in lines if "absent from the packet" in line]
        self.assertEqual(len(absent), len(scoring_key.STAGES))
        self.assertIn("0 of 25", lines[-1])

    def test_unknown_stage_is_reported(self) -> None:
        packet = _perfect_packet()
        packet["zzz_probe_stage"] = {}
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok)
        self.assertTrue(any("zzz_probe_stage" in line for line in lines))

    def test_unknown_field_is_reported(self) -> None:
        packet = _perfect_packet()
        packet["inertia"]["zzz_probe_field"] = 0
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok)
        self.assertTrue(any("zzz_probe_field" in line for line in lines))

    def test_truth_value_is_not_satisfied_by_a_number(self) -> None:
        """``False == 0`` in Python. A packet must not pass on that."""

        packet = _perfect_packet()
        packet["inertia"]["supply_changes_state"] = 0
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok, "\n".join(lines))

    def test_a_float_does_not_satisfy_an_integer(self) -> None:
        """``2 == 2.0`` in Python, and inside a list a shallow check misses it."""

        packet = _perfect_packet()
        packet["cost_floor"]["minimum_cost.L"] = [2.0, -1.0]
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok, "\n".join(lines))

    def test_a_null_stage_is_not_mistaken_for_an_absent_one(self) -> None:
        packet = _perfect_packet()
        packet["inertia"] = None
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok)
        self.assertTrue(any("not an object" in line for line in lines))

    def test_stage_that_is_not_an_object_fails(self) -> None:
        packet = _perfect_packet()
        packet["inertia"] = "no"
        lines, ok = score_packet.score(packet)
        self.assertFalse(ok)
        self.assertTrue(any("not an object" in line for line in lines))

    def test_malformed_packet_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "packet.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                score_packet.load_packet(path)

    def test_packet_that_is_a_list_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "packet.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                score_packet.load_packet(path)


class LeakGateTests(unittest.TestCase):
    def test_committed_kernel_is_clean(self) -> None:
        text = (HERE / "KERNEL.md").read_text(encoding="utf-8")
        self.assertEqual(verify_pins.check_leak(text), [])

    def test_a_digit_is_caught(self) -> None:
        findings = verify_pins.check_leak("the minimum cost is 2 items\n")
        self.assertTrue(findings)
        self.assertIn("digit", findings[0])

    def test_a_truth_token_is_caught(self) -> None:
        findings = verify_pins.check_leak("supply_changes_state is false\n")
        self.assertTrue(findings)
        self.assertIn("false", findings[0])

    def test_case_does_not_evade_the_truth_rule(self) -> None:
        self.assertTrue(verify_pins.check_leak("the answer is FALSE\n"))

    def test_a_rendered_value_is_caught_when_no_token_rule_fires(self) -> None:
        """The empty list carries no digit and no truth token."""

        findings = verify_pins.check_leak("derivable instances are []\n")
        self.assertTrue(findings)
        self.assertIn("derivable_instances", " ".join(findings))

    def test_ordinary_prose_does_not_fire(self) -> None:
        self.assertEqual(
            verify_pins.check_leak("none of these terms is yours to redefine\n"), []
        )


class VerifyTests(unittest.TestCase):
    def test_verify_passes_on_the_committed_tree(self) -> None:
        self.assertTrue(verify_pins.verify())

    def test_unpinned_artifact_is_refused(self) -> None:
        bogus = scoring_key.Field(
            "probe", "bounds.json", ("challenge0",)
        )
        stage = scoring_key.Stage("probe", "d", (), (bogus,))
        with mock.patch.object(
            scoring_key, "STAGES", tuple(scoring_key.STAGES) + (stage,)
        ):
            with mock.patch.object(
                verify_pins, "STAGES", tuple(scoring_key.STAGES) + (stage,)
            ):
                with self.assertRaises(ValueError) as caught:
                    verify_pins.verify()
        self.assertIn("unpinned", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
