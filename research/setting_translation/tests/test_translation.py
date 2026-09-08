"""The translation against the sealed kernel: faithfulness, the readings, the
visibility criterion, the chain criterion, the restarts — and one named
negative case per check."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
from typing import cast
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import translation as tr  # noqa: E402
from derivation import primitive_core as sealed  # noqa: E402
from derivation.candidates import Bounds, NewInst, min_responses  # noqa: E402
from derivation.export import Json, tree_full_json, verify_full_export  # noqa: E402
from derivation.engine import build_tree  # noqa: E402
from derivation.model import AdmitForm, AdmitInst, Regime, replay  # noqa: E402
from derivation.observe import collapsed_pairs, derivable, separable  # noqa: E402


def two(rel: frozenset[tuple[int, int]]) -> tr.FiniteSetting:
    return tr.FiniteSetting(2, rel, tr.NONE, tr.NONE, 0, 1, ())


class Encoding(unittest.TestCase):
    def test_every_sealed_setting_encodes_faithfully(self) -> None:
        for s in sealed.enumerate_settings():
            F = tr.from_sealed(s)
            self.assertTrue(tr.faithful(F, tr.encode(F)), F)

    def test_an_extra_instance_is_not_faithful(self) -> None:
        F = tr.SEALED_SETTINGS["d2Bare"]
        r = tr.encode(F)
        smuggled = replay((AdmitInst(1, (0, 0)),), r)
        self.assertFalse(tr.faithful(F, smuggled))

    def test_a_rule_is_not_faithful(self) -> None:
        F = tr.SEALED_SETTINGS["boolEmpty"]
        r = tr.encode(F)
        ruled = Regime(r.data, r.forms, r.insts, frozenset({0}), r.reqs)
        self.assertFalse(tr.faithful(F, ruled))

    def test_ill_formed_settings_are_refused(self) -> None:
        with self.assertRaises(tr.TranslationError):
            tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 2, ())
        with self.assertRaises(tr.TranslationError):
            tr.FiniteSetting(2, frozenset({(0, 5)}), tr.NONE, tr.NONE, 0, 1, ())
        with self.assertRaises(tr.TranslationError):
            tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((0, 2),))
        with self.assertRaises(tr.TranslationError):
            tr.FiniteSetting(0, tr.NONE, tr.NONE, tr.NONE, 0, 0, ())

    def test_operations_are_graphs_on_their_own_forms(self) -> None:
        F = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 2, 0), (0, 0, 0)))
        r = tr.encode(F)
        self.assertEqual(r.forms, (2, 2, 2, 2, 2))
        self.assertEqual({i for i in r.insts if i[0] == 3}, {(3, (0, 1)), (3, (1, 2)), (3, (2, 0))})
        self.assertEqual({i for i in r.insts if i[0] == 4}, {(4, (0, 0)), (4, (1, 0)), (4, (2, 0))})


class Readings(unittest.TestCase):
    def test_readings_on_the_encoding_agree_with_the_sealed_evaluator(self) -> None:
        for s in sealed.enumerate_settings():
            F = tr.from_sealed(s)
            self.assertEqual(tr.readings(F), sealed.evaluate(s), F)

    def test_the_sealed_theorem_verdicts_are_reproduced(self) -> None:
        for setting, reading, verdict, theorem in tr.SEALED_VERDICTS:
            self.assertEqual(tr.readings(tr.SEALED_SETTINGS[setting])[reading], verdict, theorem)

    def test_a_wrong_verdict_table_is_detected(self) -> None:
        original = tr.SEALED_VERDICTS
        try:
            tr.SEALED_VERDICTS = (("d2Bare", "Bs", True, "injected_false_theorem"),)
            record = tr.sealed_settings_census()
            self.assertEqual(record["failures"], [{"setting": "d2Bare", "theorem": "injected_false_theorem"}])
        finally:
            tr.SEALED_VERDICTS = original

    def test_a_transcription_error_is_detected(self) -> None:
        original = dict(tr.SEALED_SETTINGS)
        try:
            tr.SEALED_SETTINGS["d2Bare"] = replace(original["d2Bare"], rel=tr.BOTH)
            record = tr.sealed_settings_census()
            failures = cast(list[Json], record["failures"])
            self.assertIn({"setting": "d2Bare", "theorem": "d2Bare_not_bs"}, failures)
        finally:
            tr.SEALED_SETTINGS.clear()
            tr.SEALED_SETTINGS.update(original)

    def test_the_chain_criterion_agrees_with_reachability(self) -> None:
        tables = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for k in range(1 << 4):
            ops = tuple(t for j, t in enumerate(tables) if k >> j & 1)
            F = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, ops)
            self.assertEqual(tr.no_chain(F), tr.no_chain_reach(F), ops)
        three = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 2, ((1, 2, 0), (0, 0, 1)))
        self.assertEqual(tr.no_chain(three), tr.no_chain_reach(three))

    def test_a_chain_longer_than_one_step_is_found(self) -> None:
        # 0 -> 1 -> 2 and 2 fixed: the endpoints 0 and 2 meet after two steps.
        F = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 2, ((1, 2, 2),))
        self.assertFalse(tr.no_chain(F))
        self.assertEqual(tr.run(F, (0, 0), 0), tr.run(F, (0, 0), 2))
        self.assertNotEqual(tr.run(F, (0,), 0), tr.run(F, (0,), 2))

    def test_the_bound_is_the_lean_bound(self) -> None:
        F = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 0),))
        self.assertEqual(sum(1 for _ in tr.words(len(F.ops), F.n * F.n)), 5)


class Visibility(unittest.TestCase):
    def test_visibility_is_the_sealed_separability_on_every_encoded_pair(self) -> None:
        for s in sealed.enumerate_settings():
            F = tr.from_sealed(s)
            r = tr.encode(F)
            for x in range(F.n):
                for y in range(x + 1, F.n):
                    self.assertEqual(tr.visible(r, x, y), separable(r, x, y), (F, x, y))

    def test_the_self_instance_clause_is_never_the_only_witness(self) -> None:
        for s in sealed.enumerate_settings():
            F = tr.from_sealed(s)
            r = tr.encode(F)
            for x in range(F.n):
                for y in range(x + 1, F.n):
                    self.assertEqual(tr.visible_rows_columns(r, x, y), tr.visible(r, x, y), (F, x, y))

    def test_dropping_a_column_clause_is_caught_by_the_universe(self) -> None:
        r = tr.encode(two(frozenset({(0, 0), (1, 0)})))
        self.assertTrue(tr.visible(r, 0, 1))
        n = r.n_data()
        rows_only = any(
            derivable(r, (f, (0, z))) != derivable(r, (f, (1, z)))
            for f in range(len(r.forms)) for z in range(n)
        )
        self.assertFalse(rows_only)

    def test_a_unary_form_is_outside_the_criterion(self) -> None:
        r = replay((AdmitForm(1),), tr.encode(tr.SEALED_SETTINGS["d2Bare"]))
        with self.assertRaises(tr.TranslationError):
            tr.visible(r, 0, 1)

    def test_the_two_point_exhibits_match_the_lean_verdicts(self) -> None:
        for name, (F, proved) in tr.TWO_POINT.items():
            r = tr.encode(F)
            self.assertEqual(tr.visible(r, 0, 1), proved, name)
            self.assertEqual(separable(r, 0, 1), proved, name)

    def test_a_witnessed_irreflexive_pair_is_always_visible(self) -> None:
        for s in sealed.enumerate_settings():
            F = tr.from_sealed(s)
            if tr.readings(F)["A"]:
                self.assertTrue(tr.visible(tr.encode(F), F.a, F.b), F)

    def test_the_witness_alone_can_leave_the_pair_collapsed(self) -> None:
        F = two(tr._all(2))
        self.assertTrue(tr.readings(F)["W"])
        self.assertIn((0, 1), collapsed_pairs(tr.encode(F)))

    def test_a_row_witness_and_a_self_witness(self) -> None:
        link = tr.encode(two(tr.EDGE))
        self.assertTrue(tr.visible(link, 0, 1))
        loop = tr.encode(two(frozenset({(0, 0)})))
        self.assertTrue(tr.visible(loop, 0, 1))
        self.assertFalse(tr.visible(tr.encode(two(tr.NONE)), 0, 1))


class Restarts(unittest.TestCase):
    def test_the_restart_export_is_certified_and_replays(self) -> None:
        F = tr.SEALED_SETTINGS["boolEmpty"]
        record = tr.restart("boolEmpty", F, "mu1", False, 3, 60)
        self.assertTrue(record["target_collapsed_at_root"])
        classes = cast(list[dict[str, Json]], record["root_round"])
        self.assertEqual(sorted(str(c["label"]) for c in classes), ["inst2", "inst2diag"])

    def test_a_tampered_restart_export_is_refused(self) -> None:
        F = tr.SEALED_SETTINGS["boolEmpty"]
        tree = build_tree(tr.reading_of("boolEmpty", F), "mu1", Bounds(2, 2), 3, 60, False)
        payload = tree_full_json(tree)
        self.assertTrue(verify_full_export(payload))
        nodes = list(payload["nodes"])  # type: ignore[arg-type]
        first = dict(nodes[1])  # type: ignore[arg-type]
        first["regime_sha256"] = "0" * 64
        nodes[1] = first
        payload["nodes"] = nodes
        self.assertFalse(verify_full_export(payload))

    def test_the_seed_target_needs_two_endpoints(self) -> None:
        with self.assertRaises(tr.TranslationError):
            tr.reading_of("unitBare", tr.SEALED_SETTINGS["unitBare"])

    def test_the_lean_minima_are_the_engine_minima_at_the_bare_pair(self) -> None:
        r = tr.encode(two(tr.NONE))
        for measure in ("mu1", "mu2"):
            mr = min_responses(r, (0, 1), measure, Bounds(2, 2))
            assert mr is not None
            self.assertEqual(mr.cost[0], 1)
            self.assertIn((NewInst(0, (0, 0)),), mr.deltas)
            self.assertIn((NewInst(0, (0, 1)),), mr.deltas)

    def test_at_a_visible_pair_the_engine_has_nothing_to_do(self) -> None:
        r = tr.encode(tr.SEALED_SETTINGS["d2Bare"])
        mr = min_responses(r, (0, 1), "mu1", Bounds(2, 2))
        assert mr is not None
        self.assertEqual(mr.deltas, ((),))


if __name__ == "__main__":
    unittest.main()
