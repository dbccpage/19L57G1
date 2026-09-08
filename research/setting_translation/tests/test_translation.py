"""The translation against the sealed kernel: faithfulness, the readings, the
visibility criterion, the chain criteria, the verdict sources, the restarts
— and one named negative case per check.  The sealed universe is walked
once."""

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


class Universe(unittest.TestCase):
    def test_every_sealed_setting_translates(self) -> None:
        """One pass: faithful; readings agree with the sealed evaluator; the
        bounded chain criterion agrees with the unbounded one; visibility
        agrees with the sealed collapse verdict and with its row-column form;
        every A setting has a visible pair."""
        count = 0
        for s in sealed.enumerate_settings():
            count += 1
            F = tr.from_sealed(s)
            r = tr.encode(F)
            self.assertTrue(tr.faithful(F, r), F)
            ours = tr.readings(F, r)
            self.assertEqual(ours, sealed.evaluate(s), F)
            self.assertEqual(tr.no_chain(F), tr.no_chain_reach(F), F)
            collapsed = set(collapsed_pairs(r))
            for x in range(F.n):
                for y in range(x + 1, F.n):
                    vis = tr.visible(r, x, y)
                    self.assertEqual(vis, (x, y) not in collapsed, (F, x, y))
                    self.assertEqual(tr.visible_rows_columns(r, x, y), vis, (F, x, y))
            if ours["A"]:
                self.assertTrue(tr.visible(r, F.a, F.b), F)
        self.assertEqual(count, 56088)


class Encoding(unittest.TestCase):
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

    def test_the_encoding_forgets_the_designated_pair(self) -> None:
        one = tr.FiniteSetting(2, tr.EDGE, tr.NONE, tr.NONE, 0, 1, ())
        other = tr.FiniteSetting(2, tr.EDGE, tr.NONE, tr.NONE, 1, 0, ())
        self.assertEqual(tr.encode(one), tr.encode(other))
        self.assertNotEqual(tr.readings(one)["W"], tr.readings(other)["W"])

    def test_the_record_schema_is_the_sealed_one(self) -> None:
        F = tr.SEALED_SETTINGS["d2Merged"]
        self.assertEqual(F.json(), tr.to_sealed(F).json())
        self.assertEqual(tr.from_sealed(tr.to_sealed(F)), F)


class Readings(unittest.TestCase):
    def test_the_sealed_theorem_verdicts_are_reproduced(self) -> None:
        for setting, reading, verdict, theorem in tr.SEALED_VERDICTS:
            self.assertEqual(tr.readings(tr.SEALED_SETTINGS[setting])[reading], verdict, theorem)

    def test_the_verdict_table_resolves_against_both_lean_sources(self) -> None:
        sources = tr.verdict_sources()
        self.assertEqual(sources["failures"], [])
        self.assertEqual((sources["rows"], sources["sealed_rows"], sources["transcribed_rows"]), (42, 42, 42))

    def test_a_wrong_theorem_name_or_reading_is_named_by_the_sources(self) -> None:
        original = tr.SEALED_VERDICTS
        try:
            rows = list(original)
            rows[rows.index(("d2Bare", "Bs", False, "d2Bare_not_bs"))] = ("d2Bare", "E", True, "d2Bare_bc")
            tr.SEALED_VERDICTS = tuple(rows)
            failures = cast(list[dict[str, Json]], tr.verdict_sources()["failures"])
            self.assertIn({"check": "sealed source", "not_in_source": ["d2Bare", "E", True, "d2Bare_bc"]}, failures)
            self.assertIn({"check": "sealed source", "not_in_table": ["d2Bare", "Bs", False, "d2Bare_not_bs"]}, failures)
            self.assertIn({"check": "transcription", "not_in_source": ["d2Bare", "E", True, "d2Bare_bc"]}, failures)
        finally:
            tr.SEALED_VERDICTS = original

    def test_a_row_with_an_unknown_setting_is_named(self) -> None:
        original = tr.SEALED_VERDICTS
        try:
            tr.SEALED_VERDICTS = original + (("zzzNoSuchSetting", "W", True, "zzz_w"),)
            failures = cast(list[dict[str, Json]], tr.sealed_settings_census()["failures"])
            self.assertIn({"setting": "zzzNoSuchSetting", "theorem": "zzz_w", "check": "unknown setting"}, failures)
        finally:
            tr.SEALED_VERDICTS = original

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
            failures = cast(list[Json], tr.sealed_settings_census()["failures"])
            self.assertIn({"setting": "d2Bare", "theorem": "d2Bare_not_bs"}, failures)
        finally:
            tr.SEALED_SETTINGS.clear()
            tr.SEALED_SETTINGS.update(original)

    def test_an_unfaithful_encoding_of_a_full_store_setting_is_a_failure(self) -> None:
        original = tr.faithful
        try:
            tr.faithful = lambda F, r: F.n != 3
            failures = cast(list[Json], tr.sealed_settings_census()["failures"])
            for name in ("tri", "triProtected", "triSym"):
                self.assertIn({"setting": name, "check": "faithful"}, failures)
        finally:
            tr.faithful = original

    def test_the_chain_criteria_agree_and_the_bound_is_the_lean_bound(self) -> None:
        tables = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for k in range(1 << 4):
            ops = tuple(t for j, t in enumerate(tables) if k >> j & 1)
            F = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, ops)
            self.assertEqual(tr.no_chain(F), tr.no_chain_reach(F), ops)
            self.assertEqual(tr.no_chain_reach(F), all(f[0] != f[1] for f in sealed.closure(2, list(ops))), ops)
        three = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 2, ((1, 2, 0), (0, 0, 1)))
        self.assertEqual(tr.no_chain(three), tr.no_chain_reach(three))
        one_op = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 0),))
        self.assertEqual(sum(1 for _ in tr.words(len(one_op.ops), one_op.n * one_op.n)), 5)

    def test_a_chain_longer_than_one_step_is_found(self) -> None:
        # 0 -> 1 -> 2 and 2 fixed: the endpoints 0 and 2 meet after two steps.
        F = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 2, ((1, 2, 2),))
        self.assertFalse(tr.no_chain(F))
        self.assertFalse(tr.no_chain_reach(F))
        self.assertEqual(tr.run(F, (0, 0), 0), tr.run(F, (0, 0), 2))
        self.assertNotEqual(tr.run(F, (0,), 0), tr.run(F, (0,), 2))

    def test_reading_e_stays_polynomial_off_the_universe(self) -> None:
        F = tr.FiniteSetting(4, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 2, 3, 0), (0, 2, 1, 3), (3, 0, 1, 2)))
        self.assertTrue(tr.readings(F)["E"])


class Visibility(unittest.TestCase):
    def test_a_unary_form_is_outside_the_criterion(self) -> None:
        r = replay((AdmitForm(1),), tr.encode(tr.SEALED_SETTINGS["d2Bare"]))
        with self.assertRaises(tr.TranslationError):
            tr.visible(r, 0, 1)

    def test_the_two_point_exhibits_match_the_lean_verdicts(self) -> None:
        for name, (F, proved) in tr.TWO_POINT.items():
            r = tr.encode(F)
            self.assertEqual(tr.visible(r, 0, 1), proved, name)
            self.assertEqual(separable(r, 0, 1), proved, name)

    def test_the_witness_alone_can_leave_the_pair_collapsed(self) -> None:
        F = two(tr._all(2))
        self.assertTrue(tr.readings(F)["W"])
        self.assertIn((0, 1), collapsed_pairs(tr.encode(F)))

    def test_protection_as_data_makes_the_universe_c_column_an_artifact(self) -> None:
        """A C setting is visible only through its protection form when the
        relation is constant: the same setting with the protection form
        emptied is collapsed."""
        F = tr.FiniteSetting(2, tr._all(2), tr.NONE, tr.EDGE, 0, 1, ())
        self.assertTrue(tr.readings(F)["C"])
        self.assertTrue(tr.visible(tr.encode(F), 0, 1))
        self.assertFalse(tr.visible(tr.encode(replace(F, prot=tr.NONE)), 0, 1))

    def test_dropping_the_column_clause_disagrees_with_separable_on_two_points(self) -> None:
        pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]
        disagreements = []
        for k in range(1 << 4):
            r = tr.encode(two(frozenset(p for j, p in enumerate(pairs) if k >> j & 1)))
            rows_only = any(
                derivable(r, (f, (0, z))) != derivable(r, (f, (1, z)))
                for f in range(len(r.forms)) for z in range(2)
            )
            if rows_only != separable(r, 0, 1):
                disagreements.append(k)
        mask_self_and_reverse_link = (1 << pairs.index((0, 0))) + (1 << pairs.index((1, 0)))
        self.assertIn(mask_self_and_reverse_link, disagreements)

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
        self.assertEqual({c["items"] for c in classes}, {1})
        self.assertEqual({c["new_form_arity"] for c in classes}, {None})
        self.assertEqual(record["designated_pair"], [0, 1])

    def test_a_reversed_pair_records_both_orders(self) -> None:
        F = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 1, 0, ())
        record = tr.restart("reversed", F, "mu2", False, 2, 20)
        self.assertEqual((record["designated_pair"], record["target"]), ([1, 0], [0, 1]))
        classes = cast(list[dict[str, Json]], record["root_round"])
        self.assertEqual({c["new_form_arity"] for c in classes}, {0})

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

    def test_the_minima_at_the_two_point_pair_with_no_assertion_are_exactly_the_absent_instances(self) -> None:
        r = tr.encode(two(tr.NONE))
        shapes = {(0, 0), (1, 1), (0, 1), (1, 0)}
        expected = {(NewInst(f, p),) for f in range(3) for p in shapes}
        for measure in ("mu1", "mu2"):
            mr = min_responses(r, (0, 1), measure, Bounds(2, 2))
            assert mr is not None
            self.assertEqual(mr.cost[0], 1)
            self.assertEqual(set(mr.deltas), expected)

    def test_at_a_visible_pair_the_engine_has_nothing_to_do(self) -> None:
        r = tr.encode(tr.SEALED_SETTINGS["d2Bare"])
        mr = min_responses(r, (0, 1), "mu1", Bounds(2, 2))
        assert mr is not None
        self.assertEqual(mr.deltas, ((),))

    def test_with_every_instance_present_no_one_instance_response_exists(self) -> None:
        """The scope of the minima theorems: every absent instance is a
        minimum; a setting with all three stores complete has none."""
        F = tr.FiniteSetting(2, tr._all(2), tr._all(2), tr._all(2), 0, 1, ())
        r = tr.encode(F)
        self.assertIn((0, 1), collapsed_pairs(r))
        for measure in ("mu1", "mu2"):
            mr = min_responses(r, (0, 1), measure, Bounds(2, 2))
            assert mr is not None
            self.assertEqual(mr.cost[0], 2)


if __name__ == "__main__":
    unittest.main()
