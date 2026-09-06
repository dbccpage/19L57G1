"""Tests of the Challenge 2 receipt: determinism, the frozen pins, replay
from genesis for every certified history, the scores of the frozen
predictions and of C1-X, the negative direction of the scorer, and the
unpruned cross-checks of the bounded enumerations."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
import unittest
from typing import Any
from unittest.mock import patch

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
sys.path.insert(0, str(TREE))

from boundary import challenge2  # noqa: E402
from boundary.challenge2 import (  # noqa: E402
    C0_PREDICTIONS_SHA256,
    C1_PREDICTIONS_SHA256,
    CENSUS_MAX_MARKS,
    DEFINITION_LEVEL_PREDICTIONS,
    DECLARED_POLICY,
    INSCRIPTIONS,
    POLICY_OCCURRENCE,
    POLICY_SHARED,
    POLICY_SPACE,
    PREDICTIONS_SHA256,
    SCORED_PREDICTIONS,
    SEED_SHA256,
    build,
    caller_history,
    different_sides_census,
    event_json,
    mark_form_invariant,
    policy_event,
    reading_facts,
    refusal,
    regime_domain,
    score,
    separating_mark_forms,
    tally,
)
from boundary.model import (  # noqa: E402
    AdmitMark,
    AdmitOccurrence,
    Event,
    Regime,
    Supply,
    automorphisms,
    genesis,
    permitted_images,
    replay,
    serialize,
)
from boundary.presentation import DECLARED_CONVENTION, read_whole  # noqa: E402
from run_challenge2 import render  # noqa: E402

Json = dict[str, Any]

# The same whole-word scan the Challenge 0 and Challenge 1 receipt tests use:
# a watched word glued to letters is not a hit, but one joined by an
# underscore or a digit is.
ENVIRONMENT_SCAN = re.compile(r"(?<![a-z])(timestamp|time|date|python|platform|user)(?![a-z])")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment_hits(payload: object) -> list[str]:
    return ENVIRONMENT_SCAN.findall(json.dumps(payload, sort_keys=True).lower())


def rebuild(history: list[dict[str, object]]) -> list[Event]:
    """Rebuild the events of a rendered history, so the receipt's own
    histories can be replayed rather than trusted."""
    out: list[Event] = []
    for row in history:
        token = str(row["token"])
        if row["kind"] == "Supply":
            out.append(Supply(token))
        elif row["kind"] == "AdmitMark":
            out.append(AdmitMark(token, int(str(row["side"]))))
        else:
            out.append(AdmitOccurrence(token, int(str(row["side"]))))
    return out


class PinTests(unittest.TestCase):
    def test_predictions_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "challenge2" / "PREDICTIONS.md"), PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge1" / "PREDICTIONS.md"), C1_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge0" / "PREDICTIONS.md"), C0_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "SEED.md"), SEED_SHA256)

    def test_predictions_file_has_lf_endings(self) -> None:
        self.assertNotIn(b"\r", (TREE / "challenge2" / "PREDICTIONS.md").read_bytes())


class ReceiptTests(unittest.TestCase):
    def test_build_is_deterministic(self) -> None:
        self.assertEqual(build(), build())

    def test_committed_receipt_matches_the_renderer(self) -> None:
        path = TREE / "receipts" / "challenge2.json"
        self.assertTrue(path.exists(), "run run_challenge2.py first")
        self.assertEqual(path.read_bytes(), render())
        self.assertNotIn(b"\r", path.read_bytes())

    def test_receipt_carries_no_timestamp_or_environment(self) -> None:
        receipt = build()
        self.assertEqual(environment_hits(receipt), [])
        self.assertIn("occurrence", json.dumps(receipt, sort_keys=True).lower())

    def test_receipt_shape(self) -> None:
        receipt = build()
        self.assertEqual(receipt["challenge"], 2)
        self.assertEqual(receipt["inscriptions"], list(INSCRIPTIONS))
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["event_kinds"], ["Supply", "AdmitMark", "AdmitOccurrence"])
        self.assertEqual(
            receipt["state_changing_event_kinds"], ["AdmitMark", "AdmitOccurrence"]
        )
        self.assertEqual(receipt["new_event_kinds_at_challenge_2"], ["AdmitOccurrence"])
        self.assertEqual(receipt["observation_vocabulary"], ["OnSide", "SideNamed"])
        self.assertEqual(receipt["state_event_generators"], [])
        self.assertEqual(
            receipt["event_returning_functions_by_module"],
            {
                "model": [],
                "presentation": ["admission_event", "supply_event"],
                "challenge1": [
                    "admission_event",
                    "one_step_admissions",
                    "probes",
                    "supply_event",
                ],
                # the census reads module members as they are, so the probes
                # and the supply constructor imported from elsewhere are here
                "challenge2": ["caller_history", "policy_event", "probes", "supply_event"],
            },
        )
        self.assertEqual(receipt["tally"], tally(receipt["scores"]))
        self.assertEqual(
            sorted(receipt["what_the_challenge_exercises"]),
            sorted(
                [
                    "supply",
                    "mention",
                    "admission",
                    "current-state designation",
                    "retention",
                    "observation",
                    "side",
                    "equality",
                ]
            ),
        )


class FactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = build()
        self.u = self.receipt["readings"]["U"]
        self.o = self.receipt["readings"]["O"]

    def test_scores(self) -> None:
        scores = self.receipt["scores"]
        for cid in SCORED_PREDICTIONS:
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C2-X"]["status"], "PENDING")
        self.assertEqual(scores["C1-X"]["status"], "PARTIAL")
        self.assertEqual(scores["C1-X"]["U_half_status"], "HIT")
        self.assertEqual(scores["C1-X"]["O_half_status"], "PARTIAL")
        self.assertEqual(scores["C1-X"]["O_names_clause_status"], "HIT")
        self.assertEqual(scores["C1-X"]["O_nothing_new_paid_clause_status"], "MISSED")
        self.assertEqual(scores["C1-X"]["condition_status"], "HIT")
        for cid in DEFINITION_LEVEL_PREDICTIONS:
            self.assertTrue(scores[cid]["result_basis"].startswith("DEFINITION-level"), cid)
            self.assertIn("not counted as content", scores[cid]["result_basis"], cid)
        for cid in ("C2-4", "C2-5", "C2-6", "C2-7", "C2-8"):
            self.assertTrue(scores[cid]["result_basis"].startswith("content"), cid)
        for cid in ("C2-2", "C2-4", "C2-5", "C2-6", "C2-7"):
            self.assertEqual(scores[cid]["label"], "FORCED", cid)
        for cid in ("C2-1", "C2-3", "C2-8", "C2-X", "C1-X"):
            self.assertEqual(scores[cid]["label"], "NOT FORCED", cid)

    def test_tally_counts(self) -> None:
        counted = self.receipt["tally"]
        self.assertEqual(counted["hit_as_content"], ["C2-4", "C2-5", "C2-6", "C2-7", "C2-8"])
        self.assertEqual(counted["hit_definition_level"], ["C2-1", "C2-2", "C2-3"])
        self.assertEqual(counted["partial"], [])
        self.assertEqual(counted["missed"], [])

    def test_every_certified_history_replays_from_genesis(self) -> None:
        # Replay is the certifying interface: every history the receipt reports
        # as certified is replayed here from genesis and must reach the
        # placement the receipt reports, and every refused one must be refused.
        checked = 0
        for name, rd in self.receipt["readings"].items():
            g = genesis(name)
            rows: list[Json] = list(rd["identity_policies"]["rows"])
            rows.append(
                {
                    "history": rd["retained"]["history"],
                    "refused": False,
                    "placement": rd["retained"]["placement"],
                }
            )
            rows.append(
                {
                    "history": rd["order"]["other_order_history"],
                    "refused": False,
                    "placement": rd["order"]["other_order_placement"],
                }
            )
            for row in rows:
                events = rebuild(list(row["history"]))
                if row["refused"]:
                    self.assertIsNone(replay_or_none(events, g), row)
                else:
                    after = replay(events, g)
                    self.assertEqual(list(after.placement), row["placement"], row)
                checked += 1
        # per reading: four policy-and-convention rows, the retained history,
        # and the other-order history.
        self.assertEqual(checked, 12)

    def test_the_declared_policy_is_the_only_one_that_retains_both(self) -> None:
        for rd in (self.u, self.o):
            pol = rd["identity_policies"]
            self.assertEqual(pol["space"], list(POLICY_SPACE))
            self.assertEqual(pol["space_size"], 2)
            self.assertEqual(pol["declared"], DECLARED_POLICY)
            self.assertEqual(pol["policies_admitting_both_wholes"], [POLICY_OCCURRENCE])
            self.assertEqual(
                pol["policies_refused_under_every_convention"], [POLICY_SHARED]
            )
            self.assertTrue(pol["declared_is_the_only_one_admitting_both"])
            for row in pol["rows"]:
                if row["policy"] == POLICY_SHARED:
                    self.assertTrue(row["refused"])
                    self.assertIn("would move it and is refused", str(row["refusal"]))
                    self.assertEqual(row["marks"], 0)
                else:
                    self.assertFalse(row["refused"])
                    self.assertEqual(row["marks"], 2)
                    self.assertEqual(row["labels"], ["a", "a"])

    def test_the_retained_state(self) -> None:
        for rd in (self.u, self.o):
            ret = rd["retained"]
            self.assertEqual(
                [e["kind"] for e in ret["history"]],
                ["Supply", "AdmitOccurrence", "Supply", "AdmitOccurrence"],
            )
            self.assertTrue(ret["certified"])
            self.assertTrue(ret["replays_from_genesis"])
            self.assertEqual(ret["marks"], 2)
            self.assertEqual(ret["placement"], [0, 1])
            self.assertEqual(ret["labels"], ["a", "a"])
            self.assertTrue(ret["labels_repeat"])
            self.assertTrue(ret["supplies_are_equal_values"])
            self.assertTrue(ret["supply_only_regime_equals_genesis"])
            self.assertTrue(ret["marks_on_different_sides"])
            self.assertFalse(ret["sides_collapsed"])
            self.assertTrue(ret["name_observations_unchanged"])
            self.assertTrue(ret["initial_datum_unchanged"])
            self.assertTrue(ret["reading_unchanged"])
            self.assertTrue(ret["event_follows_relation_empty"])
            self.assertEqual(ret["mentioned"], ["a"])
            self.assertEqual(ret["supplied"], ["a"])
            self.assertEqual(
                ret["new_observations"],
                [
                    {"kind": "OnSide", "mark": 0, "side": 0},
                    {"kind": "OnSide", "mark": 1, "side": 1},
                ],
            )
            later = ret["later_events"]
            self.assertEqual(later["judgments_retained_after_growth"], [True, True])
            self.assertEqual(later["growth_regime_marks"], 3)
            self.assertTrue(later["token_keyed_refused"])
            self.assertIn("names more than one admitted mark", str(later["token_keyed_refusal"]))
        self.assertEqual(self.u["retained"]["holding_judgments_before"], 0)
        self.assertEqual(self.u["retained"]["holding_judgments_after"], 2)
        self.assertEqual(self.o["retained"]["holding_judgments_before"], 2)
        self.assertEqual(self.o["retained"]["holding_judgments_after"], 4)

    def test_automorphisms_and_separation_under_each_reading(self) -> None:
        ua = self.u["automorphisms"]
        oa = self.o["automorphisms"]
        self.assertEqual(ua["count"], 2)
        self.assertEqual(oa["count"], 1)
        self.assertEqual(ua["mark_exchange_witness"], {"reflected": True, "permutation": [1, 0]})
        self.assertIsNone(oa["mark_exchange_witness"])
        self.assertFalse(ua["marks_internally_separable"])
        self.assertTrue(oa["marks_internally_separable"])
        self.assertEqual(ua["side_exchange_witness"], {"reflected": True, "permutation": [1, 0]})
        self.assertIsNone(oa["side_exchange_witness"])
        self.assertFalse(ua["sides_internally_separable"])
        self.assertTrue(oa["sides_internally_separable"])
        for auto in (ua, oa):
            self.assertFalse(auto["reflection_alone_fixes"])
            self.assertFalse(auto["mark_exchange_alone_fixes"])
            self.assertTrue(auto["fixed_by_reflection_up_to_mark_renaming"])
        self.assertEqual(self.u["separation"]["separating_mark_forms"], [0, 1])
        self.assertEqual(self.o["separation"]["separating_mark_forms"], [0, 1])
        self.assertEqual(self.u["separation"]["invariant_mark_forms"], [])
        self.assertEqual(self.o["separation"]["invariant_mark_forms"], [0, 1])
        self.assertEqual(self.u["separation"]["invariant_separating_mark_forms"], [])
        self.assertEqual(self.o["separation"]["invariant_separating_mark_forms"], [0, 1])
        self.assertEqual(self.u["separation"]["mark_side_names"], [])
        self.assertEqual(self.o["separation"]["mark_side_names"], ["near", "far"])

    def test_the_one_non_identity_U_automorphism_does_both_exchanges(self) -> None:
        # Under U the marks and the sides are not separated together rather
        # than independently: the single non-identity permitted automorphism
        # is the same witness in both searches.
        ua = self.u["automorphisms"]
        self.assertEqual(ua["mark_exchange_witness"], ua["side_exchange_witness"])
        self.assertEqual(
            ua["entries"],
            [
                {"reflected": False, "permutation": [0, 1]},
                {"reflected": True, "permutation": [1, 0]},
            ],
        )

    def test_order_label_and_convention_are_not_internally_available(self) -> None:
        for rd in (self.u, self.o):
            self.assertFalse(rd["order"]["regimes_equal"])
            self.assertTrue(rd["order"]["isomorphic"])
            self.assertTrue(rd["order"]["canonical_keys_equal"])
            self.assertFalse(rd["order"]["order_internally_available"])
            self.assertEqual(rd["order"]["other_order_placement"], [1, 0])
            self.assertFalse(rd["label"]["regimes_equal"])
            self.assertTrue(rd["label"]["isomorphic"])
            self.assertTrue(rd["label"]["serializations_equal"])
            self.assertFalse(rd["label"]["label_internally_available"])
            self.assertFalse(rd["convention"]["regimes_equal"])
            self.assertTrue(rd["convention"]["isomorphic_under_reading"])
            self.assertEqual(rd["convention"]["classes_under_isomorphism"], 1)
            self.assertEqual(rd["convention"]["other_placement"], [1, 0])

    def test_the_price_is_one_new_declaration_paid_by_the_run(self) -> None:
        for rd in (self.u, self.o):
            price = rd["price"]
            self.assertEqual(price["new_at_challenge_2"], ["occurrence identity"])
            self.assertEqual(price["new_event_kinds"], ["AdmitOccurrence"])
            self.assertEqual(price["paid_by_at_challenge_2"], "the run")
            self.assertFalse(price["nothing_new_paid_at_challenge_2"])
            self.assertEqual(price["capabilities"]["occurrence identity"]["paid_by"], "the run")
            self.assertEqual(
                price["capabilities"]["admitted boundary"]["paid_by"], "the seed"
            )
        self.assertFalse(self.u["price"]["separation_available"])
        self.assertEqual(self.u["price"]["capabilities_the_separation_uses"], [])
        self.assertTrue(self.o["price"]["separation_available"])
        self.assertEqual(
            self.o["price"]["capabilities_the_separation_uses"],
            ["admitted boundary", "side names under O", "occurrence identity"],
        )
        self.assertEqual(
            self.u["price"]["new_at_challenge_2"], self.o["price"]["new_at_challenge_2"]
        )

    def test_the_different_sides_census(self) -> None:
        census = self.receipt["different_sides_census"]
        self.assertEqual(census["max_marks"], CENSUS_MAX_MARKS)
        self.assertEqual(census["images_checked"], 177)
        self.assertTrue(census["invariant_under_every_permitted_renaming"])


def replay_or_none(events: list[Event], base: Regime) -> Regime | None:
    try:
        return replay(events, base)
    except Exception:  # noqa: BLE001 - any refusal is a refusal here
        return None


class EnumerationCrossChecks(unittest.TestCase):
    def test_automorphisms_match_an_unpruned_filter_of_the_images(self) -> None:
        # The declared automorphism list against a re-derivation that filters
        # the full permitted-image enumeration with no shared helper.
        for rd in ("U", "O"):
            for n in range(3):
                marks = tuple("a" for _ in range(n))
                for placement in ((0,) * n, (1,) * n, tuple(i % 2 for i in range(n))):
                    r = Regime(rd, marks, placement)
                    unpruned = [
                        (reflected, pi)
                        for reflected, pi, image in permitted_images(r)
                        if image.reading == r.reading and image.placement == r.placement
                    ]
                    self.assertEqual(automorphisms(r), unpruned, r)

    def test_mark_form_invariance_is_a_census_over_the_declared_domain(self) -> None:
        u_domain = regime_domain("U", 2)
        o_domain = regime_domain("O", 2)
        self.assertEqual(len(u_domain), 7)
        self.assertFalse(mark_form_invariant(0, u_domain))
        self.assertFalse(mark_form_invariant(1, u_domain))
        self.assertTrue(mark_form_invariant(0, o_domain))
        self.assertTrue(mark_form_invariant(1, o_domain))
        # a domain with no mark cannot see the difference: the census is
        # vacuous there and reports invariance under both readings
        self.assertTrue(mark_form_invariant(0, regime_domain("U", 0)))

    def test_separating_mark_forms_reads_the_holding_difference(self) -> None:
        r = Regime("O", ("a", "a"), (0, 1))
        self.assertEqual(separating_mark_forms(r, 0, 1), [0, 1])
        same = Regime("O", ("a", "a"), (1, 1))
        self.assertEqual(separating_mark_forms(same, 0, 1), [])

    def test_the_census_reports_a_property_that_is_not_invariant(self) -> None:
        # The negative direction of C2-7's census: a mark property that reads
        # a side rather than the difference of the two sides is moved by the
        # reflection, and the census says so instead of reporting invariance
        # for whatever it is handed.
        def reads_a_side(r: Regime) -> bool:
            return r.placement[:1] == (0,)

        with patch.object(challenge2, "marks_on_different_sides", reads_a_side):
            census = different_sides_census(CENSUS_MAX_MARKS)
        self.assertFalse(census["invariant_under_every_permitted_renaming"])
        self.assertEqual(census["images_checked"], 177)

    def test_the_census_bound_can_be_shortened(self) -> None:
        small = different_sides_census(1)
        self.assertEqual(small["max_marks"], 1)
        self.assertEqual(small["images_checked"], 9)
        self.assertTrue(small["invariant_under_every_permitted_renaming"])

    def test_policy_event_and_caller_history(self) -> None:
        self.assertEqual(policy_event(POLICY_SHARED, "a", 0), AdmitMark("a", 0))
        self.assertEqual(policy_event(POLICY_OCCURRENCE, "a", 1), AdmitOccurrence("a", 1))
        with self.assertRaisesRegex(ValueError, "unknown identity policy"):
            policy_event("by fiat", "a", 0)
        wholes = [read_whole(text) for text in INSCRIPTIONS]
        history = caller_history(wholes, DECLARED_CONVENTION, POLICY_OCCURRENCE)
        self.assertEqual(
            [event_json(e) for e in history],
            [
                {"kind": "Supply", "token": "a"},
                {"kind": "AdmitOccurrence", "token": "a", "side": 0},
                {"kind": "Supply", "token": "a"},
                {"kind": "AdmitOccurrence", "token": "a", "side": 1},
            ],
        )
        self.assertIsNone(refusal(history, genesis("U")))
        self.assertEqual(serialize(replay(history, genesis("U"))), ("U", (0, 1)))


class ScorerNegativeDirection(unittest.TestCase):
    def setUp(self) -> None:
        self.u = reading_facts("U")
        self.o = reading_facts("O")
        self.census = different_sides_census(CENSUS_MAX_MARKS)
        self.kinds = ["OnSide", "SideNamed"]
        self.events = ["Supply", "AdmitMark", "AdmitOccurrence"]

    def run_score(
        self,
        u: Json | None = None,
        o: Json | None = None,
        census: Json | None = None,
        kinds: list[str] | None = None,
    ) -> Json:
        return score(
            self.u if u is None else u,
            self.o if o is None else o,
            self.census if census is None else census,
            self.kinds if kinds is None else kinds,
            self.events,
        )

    def mutated(self, base: Json, path: list[Any], value: Any) -> Json:
        out = copy.deepcopy(base)
        node = out
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
        return out

    def test_baseline(self) -> None:
        scores = self.run_score()
        for cid in SCORED_PREDICTIONS:
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C1-X"]["status"], "PARTIAL")

    def test_c2_1_misses_on_a_state_with_fewer_marks_or_a_shared_side(self) -> None:
        u = self.mutated(self.u, ["retained", "marks"], 1)
        self.assertEqual(self.run_score(u=u)["C2-1"]["status"], "MISSED")
        o = self.mutated(self.o, ["retained", "marks_on_different_sides"], False)
        self.assertEqual(self.run_score(o=o)["C2-1"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["retained", "certified"], False)
        self.assertEqual(self.run_score(u=u2)["C2-1"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["retained", "supplies_are_equal_values"], False)
        self.assertEqual(self.run_score(u=u3)["C2-1"]["status"], "MISSED")
        # an event kind outside supply and admission fails the capability clause
        u4 = copy.deepcopy(self.u)
        u4["retained"]["history"] = list(u4["retained"]["history"]) + [{"kind": "Remove"}]
        self.assertEqual(self.run_score(u=u4)["C2-1"]["status"], "MISSED")

    def test_c2_2_misses_when_the_shared_policy_is_accepted_or_refused_otherwise(self) -> None:
        u = copy.deepcopy(self.u)
        for row in u["identity_policies"]["rows"]:
            if row["policy"] == POLICY_SHARED:
                row["refused"] = False
                row["refusal"] = None
        self.assertEqual(self.run_score(u=u)["C2-2"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        for row in o["identity_policies"]["rows"]:
            if row["policy"] == POLICY_SHARED:
                row["refusal"] = "mark 'a' was not supplied before admission"
        self.assertEqual(self.run_score(o=o)["C2-2"]["status"], "MISSED")

    def test_c2_3_misses_on_a_third_policy_or_a_free_retention(self) -> None:
        u = self.mutated(self.u, ["identity_policies", "space_size"], 3)
        self.assertEqual(self.run_score(u=u)["C2-3"]["status"], "MISSED")
        o = self.mutated(
            self.o, ["identity_policies", "declared_is_the_only_one_admitting_both"], False
        )
        self.assertEqual(self.run_score(o=o)["C2-3"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["price", "new_at_challenge_2"], [])
        self.assertEqual(self.run_score(u=u2)["C2-3"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["price", "paid_by_at_challenge_2"], "the boundary")
        self.assertEqual(self.run_score(u=u3)["C2-3"]["status"], "MISSED")
        # a price that differs between the readings misses the equality clause
        o2 = self.mutated(self.o, ["price", "withdrawn_rules"], [])
        self.assertEqual(self.run_score(o=o2)["C2-3"]["status"], "MISSED")

    def test_c2_4_misses_on_a_third_judgment_or_a_changed_name(self) -> None:
        extra = [
            {"kind": "OnSide", "mark": 0, "side": 0},
            {"kind": "OnSide", "mark": 1, "side": 1},
            {"kind": "OnSide", "mark": 2, "side": 0},
        ]
        u = self.mutated(self.u, ["retained", "new_observations"], extra)
        self.assertEqual(self.run_score(u=u)["C2-4"]["status"], "MISSED")
        o = self.mutated(self.o, ["retained", "name_observations_unchanged"], False)
        self.assertEqual(self.run_score(o=o)["C2-4"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["retained", "holding_judgments_after"], 5)
        self.assertEqual(self.run_score(o=o2)["C2-4"]["status"], "MISSED")
        u2 = self.mutated(
            self.u, ["retained", "later_events", "judgments_retained_after_growth"], [True, False]
        )
        self.assertEqual(self.run_score(u=u2)["C2-4"]["status"], "MISSED")
        self.assertEqual(
            self.run_score(kinds=self.kinds + ["Empty"])["C2-4"]["status"], "MISSED"
        )

    def test_c2_5_misses_when_U_separates_or_the_counts_move(self) -> None:
        u = self.mutated(self.u, ["automorphisms", "count"], 1)
        self.assertEqual(self.run_score(u=u)["C2-5"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["automorphisms", "mark_exchange_witness"], None)
        self.assertEqual(self.run_score(u=u2)["C2-5"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["separation", "invariant_mark_forms"], [0])
        self.assertEqual(self.run_score(u=u3)["C2-5"]["status"], "MISSED")
        o = self.mutated(self.o, ["automorphisms", "count"], 2)
        self.assertEqual(self.run_score(o=o)["C2-5"]["status"], "MISSED")

    def test_c2_6_misses_when_O_collapses_or_the_convention_splits(self) -> None:
        o = self.mutated(self.o, ["automorphisms", "marks_internally_separable"], False)
        self.assertEqual(self.run_score(o=o)["C2-6"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["separation", "invariant_separating_mark_forms"], [])
        self.assertEqual(self.run_score(o=o2)["C2-6"]["status"], "MISSED")
        o3 = self.mutated(self.o, ["separation", "mark_side_names"], ["far", "near"])
        self.assertEqual(self.run_score(o=o3)["C2-6"]["status"], "MISSED")
        o4 = self.mutated(self.o, ["convention", "classes_under_isomorphism"], 2)
        self.assertEqual(self.run_score(o=o4)["C2-6"]["status"], "MISSED")
        u = self.mutated(self.u, ["convention", "isomorphic_under_reading"], False)
        self.assertEqual(self.run_score(u=u)["C2-6"]["status"], "MISSED")
        o5 = self.mutated(
            self.o, ["price", "capabilities_the_separation_uses"], ["admitted boundary"]
        )
        self.assertEqual(self.run_score(o=o5)["C2-6"]["status"], "MISSED")

    def test_c2_7_misses_when_the_census_fails_or_U_gains_an_invariant(self) -> None:
        census = self.mutated(self.census, ["invariant_under_every_permitted_renaming"], False)
        self.assertEqual(self.run_score(census=census)["C2-7"]["status"], "MISSED")
        self.assertEqual(
            self.run_score(census=different_sides_census(1))["C2-7"]["status"], "MISSED"
        )
        u = self.mutated(self.u, ["separation", "invariant_separating_mark_forms"], [0])
        self.assertEqual(self.run_score(u=u)["C2-7"]["status"], "MISSED")
        o = self.mutated(self.o, ["retained", "marks_on_different_sides"], False)
        self.assertEqual(self.run_score(o=o)["C2-7"]["status"], "MISSED")

    def test_c2_8_misses_when_the_sides_separate_or_the_order_shows(self) -> None:
        u = self.mutated(self.u, ["automorphisms", "side_exchange_witness"], None)
        self.assertEqual(self.run_score(u=u)["C2-8"]["status"], "MISSED")
        o = self.mutated(
            self.o, ["automorphisms", "side_exchange_witness"], {"reflected": True, "permutation": [1, 0]}
        )
        self.assertEqual(self.run_score(o=o)["C2-8"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["retained", "sides_collapsed"], True)
        self.assertEqual(self.run_score(u=u2)["C2-8"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["order", "order_internally_available"], True)
        self.assertEqual(self.run_score(u=u3)["C2-8"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["label", "label_internally_available"], True)
        self.assertEqual(self.run_score(o=o2)["C2-8"]["status"], "MISSED")
        u4 = self.mutated(self.u, ["automorphisms", "sides_internally_separable"], True)
        self.assertEqual(self.run_score(u=u4)["C2-8"]["status"], "MISSED")

    def test_c1_x_halves_and_clauses_score_independently(self) -> None:
        # The U half, the O names clause, and the O price clause each move on
        # their own fact, and the frozen O price clause is a miss on the real
        # receipt: a new declaration was paid at this rung.
        scores = self.run_score()
        self.assertEqual(scores["C1-X"]["status"], "PARTIAL")
        u = self.mutated(self.u, ["automorphisms", "marks_internally_separable"], True)
        c1x = self.run_score(u=u)["C1-X"]
        self.assertEqual(c1x["U_half_status"], "MISSED")
        self.assertEqual(c1x["status"], "MISSED")
        o = self.mutated(self.o, ["separation", "mark_side_names"], ["near", "near"])
        c1x = self.run_score(o=o)["C1-X"]
        self.assertEqual(c1x["O_names_clause_status"], "MISSED")
        self.assertEqual(c1x["O_half_status"], "MISSED")
        self.assertEqual(c1x["status"], "MISSED")
        # had nothing new been paid, the frozen clause would have hit and the
        # whole extrapolation with it
        o2 = self.mutated(self.o, ["price", "nothing_new_paid_at_challenge_2"], True)
        c1x = self.run_score(o=o2)["C1-X"]
        self.assertEqual(c1x["O_nothing_new_paid_clause_status"], "HIT")
        self.assertEqual(c1x["O_half_status"], "HIT")
        self.assertEqual(c1x["status"], "HIT")
        # the condition the frozen text names: two internal identities for the
        # two wholes despite the shared visible mark
        u2 = self.mutated(self.u, ["retained", "labels_repeat"], False)
        self.assertEqual(self.run_score(u=u2)["C1-X"]["condition_status"], "MISSED")

    def test_tally_refuses_an_unknown_status_and_moves_a_miss(self) -> None:
        scores = self.run_score()
        missed_definition = self.mutated(scores, ["C2-2", "status"], "MISSED")
        counted = tally(missed_definition)
        self.assertEqual(counted["hit_definition_level"], ["C2-1", "C2-3"])
        self.assertEqual(counted["missed"], ["C2-2"])
        missed_content = self.mutated(scores, ["C2-5", "status"], "PARTIAL")
        counted = tally(missed_content)
        self.assertEqual(counted["partial"], ["C2-5"])
        self.assertEqual(counted["hit_as_content"], ["C2-4", "C2-6", "C2-7", "C2-8"])
        with self.assertRaisesRegex(ValueError, "unexpected status 'PENDING' for C2-1"):
            tally(self.mutated(scores, ["C2-1", "status"], "PENDING"))
        self.assertNotIn("C1-X", counted["scored"])
        self.assertNotIn("C2-X", counted["scored"])

    def test_the_module_declares_no_authority(self) -> None:
        self.assertEqual(build()["authority_effect"], "None")
        self.assertEqual(challenge2.DECLARED_POLICY, POLICY_OCCURRENCE)


if __name__ == "__main__":
    unittest.main()
