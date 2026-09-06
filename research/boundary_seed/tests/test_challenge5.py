"""Tests of the Challenge 5 receipt: determinism, the frozen pins, the third
reader widening and what the two narrower readers refuse, the declared policy
space and its prices, replay from genesis for every retained state, the
invisibility of the nesting at every one-step policy, the separation of the two
one-step policies over the declared domain, the class key read over that domain
rather than at one inscription, the two senses of an available depth, the
naming coordinate and where it collapses, the two cost measures, the minima and
their quotient, the scores of the frozen predictions and of C4-X, the negative
direction of the scorer, and the unpruned cross-checks of every bounded
enumeration."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
import unittest
from itertools import permutations, product
from typing import Any

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
sys.path.insert(0, str(TREE))

from boundary import challenge5  # noqa: E402
from boundary.challenge5 import (  # noqa: E402
    ALPHABET,
    BASE_POINT,
    C0_PREDICTIONS_SHA256,
    C1_PREDICTIONS_SHA256,
    C2_PREDICTIONS_SHA256,
    C3_PREDICTIONS_SHA256,
    C4_PREDICTIONS_SHA256,
    CALLER_TOKEN,
    CAP_AS_MARK,
    CAP_NAME_INNER,
    CAP_REACH,
    CAP_RECORD,
    COLLATERAL_FACTS,
    COORDINATES,
    DEEPER_INSCRIPTION,
    DEFINITION_LEVEL_PREDICTIONS,
    FLAT_INSCRIPTION,
    INSCRIPTION,
    LEVELS,
    POLICY_ADDRESS,
    POLICY_CAPABILITIES,
    POLICY_FLATTEN,
    POLICY_NAMES,
    POLICY_OPAQUE,
    POLICY_REFUSE,
    POLICY_SPACE,
    PREDICTIONS_SHA256,
    PRICE_FIELDS_DECLARED,
    SCORED_PREDICTIONS,
    SEED_SHA256,
    WHAT_THE_INNER_WHOLE_IS,
    WHOLE_TOKEN,
    Point,
    PolicyRefusal,
    a_place_of_that_depth_is_nameable,
    behaviour_digest,
    build,
    capabilities,
    changed_coordinates,
    class_key,
    closed_grammar_forms_reading_depth,
    collateral_facts,
    deepest_place_a_policy_names,
    depth_determined_by_the_key,
    depth_signatures,
    depths_over_the_domain,
    differing_inscriptions,
    domain,
    domain_behaviour,
    domain_texts,
    effective_structure,
    effective_unnamed_levels,
    facts_agreeing_everywhere,
    flat_history,
    further_mark_within_the_inner_whole,
    holding,
    is_one_step,
    mu1,
    mu2,
    named,
    named_levels,
    order_facts,
    placements,
    point_detail,
    point_name,
    point_row,
    point_space,
    policy_count,
    policy_history,
    policy_is_one_step,
    policy_rows,
    policy_separation,
    price_facts,
    probes,
    reachable_levels,
    reader_facts,
    reading_facts,
    retain,
    retained_key,
    score,
    score_c4x,
    side_items,
    signatures_agree,
    tally,
    unnamed_levels,
)
from boundary.model import (  # noqa: E402
    READING_O,
    READING_U,
    AdmissionError,
    AdmitAt,
    DeepEvent,
    DeepRegime,
    Regime,
    OpaqueDatum,
    Supply,
    deep_automorphisms,
    deep_canonical,
    deep_certify,
    deep_event_follows,
    deep_genesis,
    deep_is_isomorphic,
    deep_mark_orbit,
    deep_permitted_images,
    deep_rename_marks,
    deep_replay,
    deep_serialize,
    deep_step,
    depth_of,
    exchange_level,
    flatten_deep,
    genesis,
    is_isomorphic,
    level_flip_sets,
    replay,
)
from boundary.presentation import (  # noqa: E402
    DECLARED_CONVENTION,
    NESTING_BOUND,
    OTHER_WITHIN_WHOLE_ORDER,
    NestedWhole,
    PresentationError,
    read_nested_whole,
    read_pair_whole,
    read_whole,
    render_whole,
    whole_depth,
)
from run_challenge5 import render  # noqa: E402

Json = dict[str, Any]

ENVIRONMENT_SCAN = re.compile(r"(?<![a-z])(timestamp|time|date|python|platform|user)(?![a-z])")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment_hits(payload: object) -> list[str]:
    return ENVIRONMENT_SCAN.findall(json.dumps(payload, sort_keys=True).lower())


def rebuild(history: list[dict[str, object]]) -> list[DeepEvent]:
    """Rebuild the events of a rendered deep history, so the receipt's own
    histories are replayed rather than trusted."""
    out: list[DeepEvent] = []
    for row in history:
        token = str(row["token"])
        if row["kind"] == "Supply":
            out.append(Supply(token))
        else:
            address = tuple(int(side) for side in list(row["address"]))  # type: ignore[call-overload]
            out.append(AdmitAt(token, address))
    return out


class PinTests(unittest.TestCase):
    def test_predictions_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "challenge5" / "PREDICTIONS.md"), PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge4" / "PREDICTIONS.md"), C4_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge3" / "PREDICTIONS.md"), C3_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge2" / "PREDICTIONS.md"), C2_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge1" / "PREDICTIONS.md"), C1_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge0" / "PREDICTIONS.md"), C0_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "SEED.md"), SEED_SHA256)

    def test_predictions_file_has_lf_endings(self) -> None:
        self.assertNotIn(b"\r", (TREE / "challenge5" / "PREDICTIONS.md").read_bytes())


class ReceiptTests(unittest.TestCase):
    def test_build_is_deterministic(self) -> None:
        self.assertEqual(build(), build())

    def test_committed_receipt_matches_the_renderer(self) -> None:
        path = TREE / "receipts" / "challenge5.json"
        self.assertTrue(path.exists(), "run run_challenge5.py first")
        self.assertEqual(path.read_bytes(), render())
        self.assertNotIn(b"\r", path.read_bytes())

    def test_receipt_is_inside_the_declared_split_threshold(self) -> None:
        # Over a megabyte the rung would owe a summary and a gzip with a
        # content hash.  This rung's space is eight points, so the receipt
        # carries every point in full and stays far inside.
        self.assertLess(len(render()), 1_000_000)

    def test_receipt_carries_no_timestamp_or_environment(self) -> None:
        receipt = build()
        self.assertEqual(environment_hits(receipt), [])
        self.assertIn("address", json.dumps(receipt, sort_keys=True).lower())


class ReaderTests(unittest.TestCase):
    def test_both_inherited_readers_refuse_the_inscription(self) -> None:
        facts = reader_facts()
        self.assertTrue(facts["inherited_readers_refuse_both"])
        with self.assertRaises(PresentationError):
            read_whole(INSCRIPTION)
        with self.assertRaises(PresentationError):
            read_pair_whole(INSCRIPTION)

    def test_the_widened_reader_reads_a_whole_within_a_side(self) -> None:
        whole = read_nested_whole(INSCRIPTION)
        self.assertIsInstance(whole.left, NestedWhole)
        self.assertIsNone(whole.right)
        self.assertEqual(whole_depth(whole), 2)
        self.assertEqual(render_whole(whole), INSCRIPTION)

    def test_the_widened_reader_refuses_what_is_beyond_its_bound(self) -> None:
        with self.assertRaisesRegex(PresentationError, "deeper than the declared bound"):
            read_nested_whole(DEEPER_INSCRIPTION)
        for text in ("<a|b|c>", "<ab|>", "<a|", ">a|<", "<a>b>", "<>", "<<a|>", "<"):
            with self.assertRaises(PresentationError):
                read_nested_whole(text)
        with self.assertRaisesRegex(PresentationError, "at least one"):
            read_nested_whole(INSCRIPTION, bound=0)

    def test_a_deeper_bound_reads_what_the_declared_one_refuses(self) -> None:
        # The refusal is the DECLARED bound and not a limit of the reader, so
        # the same text is read at a wider bound; the run declares two.
        whole = read_nested_whole(DEEPER_INSCRIPTION, bound=3)
        self.assertEqual(render_whole(whole), DEEPER_INSCRIPTION)
        self.assertEqual(whole_depth(whole), 3)

    def test_the_reader_reads_every_member_of_the_declared_domain(self) -> None:
        for text in domain_texts():
            self.assertEqual(render_whole(read_nested_whole(text)), text)


class PolicySpaceTests(unittest.TestCase):
    def test_the_space_is_the_product_of_its_declared_coordinates(self) -> None:
        points = point_space()
        self.assertEqual(len(points), len(POLICY_SPACE) * 2)
        self.assertEqual(len({point_name(p) for p in points}), len(points))
        self.assertEqual(list(COORDINATES), ["nesting_policy", "naming_reaches_inward"])

    def test_the_declared_policy_counts(self) -> None:
        self.assertEqual(
            [policy_count(policy) for policy in POLICY_SPACE], [0, 1, 1, 2]
        )
        self.assertEqual(
            [policy_is_one_step(policy) for policy in POLICY_SPACE],
            [False, True, True, False],
        )
        self.assertEqual(
            sorted({cap for caps in POLICY_CAPABILITIES.values() for cap in caps}),
            sorted([CAP_AS_MARK, CAP_REACH, CAP_RECORD]),
        )

    def test_one_step_is_capability_count_one_and_not_coordinate_count(self) -> None:
        # The rung's own finding: Challenge 4 could report the two counts as
        # the same number, and here they part at the recording policy, which
        # moves one coordinate and uses two capabilities.
        record = Point(POLICY_ADDRESS)
        self.assertEqual(len(changed_coordinates(record)), 1)
        self.assertEqual(mu1(record), 2)
        self.assertFalse(is_one_step(record))
        for point in point_space():
            self.assertEqual(is_one_step(point), mu1(point) == 1)
        self.assertNotEqual(
            [is_one_step(p) for p in point_space()],
            [len(changed_coordinates(p)) == 1 for p in point_space()],
        )

    def test_the_naming_coordinate_is_a_capability_of_its_own(self) -> None:
        self.assertEqual(capabilities(Point(POLICY_REFUSE, True)), [CAP_NAME_INNER])
        self.assertEqual(
            capabilities(Point(POLICY_ADDRESS, True)),
            [CAP_REACH, CAP_RECORD, CAP_NAME_INNER],
        )
        self.assertEqual(changed_coordinates(BASE_POINT), [])
        self.assertEqual(point_name(BASE_POINT), "refuse")

    def test_the_levels_a_reading_names_and_a_policy_reaches(self) -> None:
        for naming in (False, True):
            self.assertEqual(named_levels(READING_U, Point(POLICY_ADDRESS, naming)), ())
        self.assertEqual(named_levels(READING_O, Point(POLICY_ADDRESS)), (0,))
        self.assertEqual(named_levels(READING_O, Point(POLICY_ADDRESS, True)), LEVELS)
        self.assertEqual(reachable_levels(Point(POLICY_REFUSE)), ())
        self.assertEqual(reachable_levels(Point(POLICY_OPAQUE)), (0,))
        self.assertEqual(reachable_levels(Point(POLICY_FLATTEN)), (0,))
        self.assertEqual(reachable_levels(Point(POLICY_ADDRESS)), LEVELS)
        self.assertEqual(unnamed_levels(READING_U, Point(POLICY_ADDRESS)), LEVELS)
        self.assertEqual(unnamed_levels(READING_O, Point(POLICY_ADDRESS)), (1,))
        self.assertEqual(unnamed_levels(READING_O, Point(POLICY_ADDRESS, True)), ())

    def test_the_effective_structure_collapses_the_no_ops(self) -> None:
        # Under U the naming coordinate reaches nothing, because U names no
        # side at any level; at a policy that never crosses a second boundary
        # the inner exchange acts on nothing either.
        for policy in POLICY_SPACE:
            self.assertEqual(
                effective_structure(READING_U, Point(policy)),
                effective_structure(READING_U, Point(policy, True)),
            )
        for policy in (POLICY_REFUSE, POLICY_OPAQUE, POLICY_FLATTEN):
            self.assertEqual(
                effective_structure(READING_O, Point(policy)),
                effective_structure(READING_O, Point(policy, True)),
            )
        self.assertNotEqual(
            effective_structure(READING_O, Point(POLICY_ADDRESS)),
            effective_structure(READING_O, Point(POLICY_ADDRESS, True)),
        )
        self.assertEqual(effective_unnamed_levels(READING_O, Point(POLICY_OPAQUE)), ())
        self.assertEqual(effective_unnamed_levels(READING_U, Point(POLICY_OPAQUE)), (0,))


class HistoryTests(unittest.TestCase):
    def test_the_four_policies_on_the_caller_inscription(self) -> None:
        whole = read_nested_whole(INSCRIPTION)
        with self.assertRaisesRegex(PolicyRefusal, "refuses an item that is a whole"):
            placements(whole, POLICY_REFUSE)
        self.assertEqual(placements(whole, POLICY_OPAQUE), [(WHOLE_TOKEN, (0,))])
        self.assertEqual(placements(whole, POLICY_FLATTEN), [(CALLER_TOKEN, (0,))])
        self.assertEqual(placements(whole, POLICY_ADDRESS), [(CALLER_TOKEN, (0, 0))])

    def test_the_policies_part_on_a_two_mark_inner_whole(self) -> None:
        whole = read_nested_whole("<<a|b>|c>")
        self.assertEqual(
            placements(whole, POLICY_OPAQUE), [(WHOLE_TOKEN, (0,)), ("c", (1,))]
        )
        self.assertEqual(
            placements(whole, POLICY_FLATTEN),
            [("a", (0,)), ("b", (0,)), ("c", (1,))],
        )
        self.assertEqual(
            placements(whole, POLICY_ADDRESS),
            [("a", (0, 0)), ("b", (0, 1)), ("c", (1,))],
        )

    def test_a_flat_inscription_is_admitted_by_every_policy_alike(self) -> None:
        whole = read_nested_whole(FLAT_INSCRIPTION)
        for policy in POLICY_SPACE:
            self.assertEqual(placements(whole, policy), [(CALLER_TOKEN, (0,))])

    def test_an_unknown_policy_and_an_unknown_order_are_refused(self) -> None:
        whole = read_nested_whole(INSCRIPTION)
        with self.assertRaisesRegex(PolicyRefusal, "unknown nesting policy"):
            placements(whole, "zzz probe policy")
        with self.assertRaisesRegex(PresentationError, "unknown within-whole order"):
            side_items(whole, "middle first")

    def test_the_supplies_precede_every_admission(self) -> None:
        history = policy_history(read_nested_whole("<<a|b>|c>"), POLICY_ADDRESS)
        kinds = [type(e).__name__ for e in history]
        self.assertEqual(kinds, ["Supply"] * 3 + ["AdmitAt"] * 3)

    def test_a_recording_history_has_no_rendering_in_the_inherited_grammar(self) -> None:
        whole = read_nested_whole(INSCRIPTION)
        with self.assertRaisesRegex(PolicyRefusal, "no history in the inherited grammar"):
            flat_history(whole, POLICY_ADDRESS)
        self.assertEqual(len(flat_history(whole, POLICY_OPAQUE)), 2)

    def test_every_retained_state_replays_from_genesis(self) -> None:
        receipt = build()
        for reading in (READING_U, READING_O):
            g = deep_genesis(reading)
            for row in receipt["readings"][reading]["point_detail"]:
                history = rebuild(list(row["history"]))
                if row["retained"] is None:
                    self.assertEqual(history, [])
                    self.assertFalse(row["certified"])
                    continue
                rebuilt = deep_replay(history, g)
                self.assertEqual(
                    [list(a) for a in rebuilt.addresses], row["retained"]["addresses"]
                )
                self.assertEqual(list(rebuilt.marks), row["retained"]["marks"])
                self.assertTrue(deep_certify(history, g, rebuilt))
                self.assertTrue(row["certified"])
                self.assertTrue(row["replays_from_genesis"])

    def test_an_admission_of_a_token_never_supplied_is_refused(self) -> None:
        with self.assertRaisesRegex(AdmissionError, "was not supplied before admission"):
            deep_replay([AdmitAt("q", (0,))], deep_genesis(READING_U))


class NestingVisibilityTests(unittest.TestCase):
    def test_the_nesting_is_invisible_at_every_one_step_policy(self) -> None:
        for reading in (READING_U, READING_O):
            for policy in (POLICY_OPAQUE, POLICY_FLATTEN):
                point = Point(policy)
                levels = effective_unnamed_levels(reading, point)
                nested = retain(reading, read_nested_whole(INSCRIPTION), policy, INSCRIPTION)
                flat = retain(
                    reading, read_nested_whole(FLAT_INSCRIPTION), policy, FLAT_INSCRIPTION
                )
                assert nested.deep is not None and flat.deep is not None
                self.assertEqual(nested.deep.n_marks(), 1)
                self.assertEqual(nested.deep.addresses, ((0,),))
                self.assertTrue(deep_is_isomorphic(nested.deep, flat.deep, levels))
                assert nested.regime is not None and flat.regime is not None
                self.assertTrue(is_isomorphic(nested.regime, flat.regime))

    def test_the_discarding_policy_retains_the_flat_regime_exactly(self) -> None:
        # Stronger than isomorphic, and only for that policy: the opaque one
        # carries the declared whole token instead of the caller's.
        for reading in (READING_U, READING_O):
            nested = retain(
                reading, read_nested_whole(INSCRIPTION), POLICY_FLATTEN, INSCRIPTION
            )
            flat = retain(
                reading, read_nested_whole(FLAT_INSCRIPTION), POLICY_FLATTEN, FLAT_INSCRIPTION
            )
            self.assertEqual(nested.deep, flat.deep)
            opaque = retain(
                reading, read_nested_whole(INSCRIPTION), POLICY_OPAQUE, INSCRIPTION
            )
            assert opaque.deep is not None
            self.assertNotEqual(opaque.deep, flat.deep)
            self.assertEqual(opaque.deep.marks, (WHOLE_TOKEN,))

    def test_the_recording_policy_tells_the_two_inscriptions_apart(self) -> None:
        for reading in (READING_U, READING_O):
            point = Point(POLICY_ADDRESS)
            levels = effective_unnamed_levels(reading, point)
            nested = retain(
                reading, read_nested_whole(INSCRIPTION), POLICY_ADDRESS, INSCRIPTION
            )
            flat = retain(
                reading, read_nested_whole(FLAT_INSCRIPTION), POLICY_ADDRESS, FLAT_INSCRIPTION
            )
            assert nested.deep is not None and flat.deep is not None
            self.assertFalse(deep_is_isomorphic(nested.deep, flat.deep, levels))
            self.assertEqual(depth_of(nested.deep, 0), 2)
            self.assertEqual(depth_of(flat.deep, 0), 1)
            # And what the flattening throws away is exactly the difference.
            self.assertEqual(flatten_deep(nested.deep), flatten_deep(flat.deep))


class PolicySeparationTests(unittest.TestCase):
    def test_the_two_one_step_policies_are_two(self) -> None:
        for reading in (READING_U, READING_O):
            facts = policy_separation(reading)
            self.assertFalse(facts["same_policy_on_the_domain"])
            self.assertGreater(int(facts["inscriptions_where_they_part"]), 0)
            self.assertFalse(facts["part_at_the_caller_inscription"])
            witness = str(facts["first_inscriptions_where_they_part"][0])
            self.assertNotEqual(
                retained_key(reading, Point(POLICY_OPAQUE), read_nested_whole(witness)),
                retained_key(reading, Point(POLICY_FLATTEN), read_nested_whole(witness)),
            )

    def test_the_class_key_read_at_one_inscription_understates_the_tie(self) -> None:
        # The defect the domain-wide key exists to catch, injected here: with
        # the behaviour read at the caller's inscription alone, the two
        # one-step policies collapse into one class and the tie the seed
        # requires to be retained is reported as a unique minimum.
        caller = read_nested_whole(INSCRIPTION)
        for reading in (READING_U, READING_O):
            wide = {
                policy: class_key(
                    reading,
                    Point(policy),
                    behaviour_digest(domain_behaviour(reading, Point(policy))),
                )
                for policy in (POLICY_OPAQUE, POLICY_FLATTEN)
            }
            narrow = {
                policy: class_key(
                    reading,
                    Point(policy),
                    behaviour_digest([retained_key(reading, Point(policy), caller)]),
                )
                for policy in (POLICY_OPAQUE, POLICY_FLATTEN)
            }
            self.assertNotEqual(wide[POLICY_OPAQUE], wide[POLICY_FLATTEN])
            self.assertEqual(narrow[POLICY_OPAQUE], narrow[POLICY_FLATTEN])

    def test_the_digest_moves_with_the_behaviour(self) -> None:
        first = behaviour_digest(["a", "b"])
        self.assertEqual(first, behaviour_digest(["a", "b"]))
        self.assertNotEqual(first, behaviour_digest(["a", "c"]))
        self.assertEqual(len(first), 16)

    def test_differing_inscriptions_is_bounded_and_ordered(self) -> None:
        found = differing_inscriptions(READING_U, Point(POLICY_OPAQUE), Point(POLICY_FLATTEN))
        self.assertEqual(len(found), 4)
        self.assertEqual(
            found,
            [
                text
                for text in domain_texts()
                if retained_key(READING_U, Point(POLICY_OPAQUE), read_nested_whole(text))
                != retained_key(READING_U, Point(POLICY_FLATTEN), read_nested_whole(text))
            ][:4],
        )
        self.assertEqual(
            differing_inscriptions(READING_U, Point(POLICY_OPAQUE), Point(POLICY_OPAQUE)),
            [],
        )


class DomainTests(unittest.TestCase):
    def test_the_domain_is_every_whole_within_the_declared_bound(self) -> None:
        texts = domain_texts()
        self.assertEqual(len(texts), 144)
        self.assertEqual(len(set(texts)), len(texts))
        self.assertIn(INSCRIPTION, texts)
        self.assertIn(FLAT_INSCRIPTION, texts)
        self.assertNotIn(DEEPER_INSCRIPTION, texts)
        self.assertEqual(sorted({whole_depth(w) for w in domain()}), [1, 2])

    def test_the_domain_is_the_declared_product(self) -> None:
        flat = [
            NestedWhole(left, right)
            for left in [None, *ALPHABET]
            for right in [None, *ALPHABET]
        ]
        self.assertEqual(len(flat), 9)
        inner: list[Any] = [None, *ALPHABET, *flat]
        expected = [NestedWhole(left, right) for left in inner for right in inner]
        self.assertEqual(domain(), expected)
        self.assertEqual(NESTING_BOUND, 2)


class DepthTests(unittest.TestCase):
    def test_depth_is_one_at_every_one_step_policy(self) -> None:
        for reading in (READING_U, READING_O):
            for policy in (POLICY_REFUSE, POLICY_OPAQUE, POLICY_FLATTEN):
                self.assertEqual(depths_over_the_domain(reading, Point(policy)), [1])
            self.assertEqual(depths_over_the_domain(reading, Point(POLICY_ADDRESS)), [1, 2])

    def test_depth_is_determined_by_the_key_where_a_state_is_retained(self) -> None:
        for reading in (READING_U, READING_O):
            for policy in POLICY_SPACE:
                self.assertTrue(depth_determined_by_the_key(reading, Point(policy)))
                self.assertGreater(len(depth_signatures(reading, Point(policy))), 0)

    def test_the_key_determination_check_reads_both_ways(self) -> None:
        # Over the real policies no two inscriptions with equal keys carry
        # different depths, so the direction that returns FALSE is exercised
        # here rather than left unread.
        self.assertTrue(signatures_agree([("k", (1,)), ("k", (1,)), ("j", (2,))]))
        self.assertFalse(signatures_agree([("k", (1,)), ("k", (2,))]))
        self.assertFalse(signatures_agree([]))

    def test_no_form_of_the_closed_grammar_reads_depth(self) -> None:
        self.assertEqual(closed_grammar_forms_reading_depth(), [])
        for reading in (READING_U, READING_O):
            for row in reading_facts(reading)["points"]:
                self.assertNotIn(
                    "depth_expressible_in_the_closed_grammar",
                    row["collateral_facts_holding"],
                )

    def test_no_permitted_renaming_moves_a_mark_depth(self) -> None:
        base = deep_replay(
            [Supply("a"), AdmitAt("a", (0, 1)), Supply("b"), AdmitAt("b", (1,))],
            deep_genesis(READING_U),
        )
        for _flips, pi, image in deep_permitted_images(base, LEVELS):
            for i in range(base.n_marks()):
                self.assertEqual(depth_of(image, pi[i]), depth_of(base, i))

    def test_depth_and_the_key_part_from_the_closed_grammar(self) -> None:
        # The two senses the rung keeps apart: available in the key, and
        # expressible in the grammar.  The recording policy has the first and
        # no point of the space has the second.
        u = reading_facts(READING_U)
        record = named(u["points"], "record")
        self.assertIn("depth_determined_by_the_key", record["collateral_facts_holding"])
        self.assertNotIn(
            "depth_expressible_in_the_closed_grammar", record["collateral_facts_holding"]
        )


class NamingCoordinateTests(unittest.TestCase):
    def test_the_naming_coordinate_collapses_under_U_and_not_under_O(self) -> None:
        u = reading_facts(READING_U)
        o = reading_facts(READING_O)
        self.assertTrue(u["naming_coordinate_collapses_everywhere"])
        self.assertFalse(o["naming_coordinate_collapses_everywhere"])
        self.assertEqual(
            [pair[0] for pair in o["naming_coordinate_collapses_at"]],
            ["refuse", "opaque", "discard"],
        )

    def test_the_address_orbit_sizes_under_each_declaration(self) -> None:
        u = reading_facts(READING_U)
        o = reading_facts(READING_O)
        self.assertEqual(named(u["point_detail"], "record")["mark_address_orbit_size"], 4)
        self.assertEqual(named(o["point_detail"], "record")["mark_address_orbit_size"], 2)
        self.assertEqual(
            named(o["point_detail"], "record+naming_reaches_inward")[
                "mark_address_orbit_size"
            ],
            1,
        )

    def test_the_inner_side_is_unavailable_under_O_without_the_declaration(self) -> None:
        o = reading_facts(READING_O)
        self.assertNotIn(
            "inner_side_internally_available",
            named(o["points"], "record")["collateral_facts_holding"],
        )
        self.assertIn(
            "inner_side_internally_available",
            named(o["points"], "record+naming_reaches_inward")["collateral_facts_holding"],
        )
        self.assertIn(
            "outer_side_internally_available",
            named(o["points"], "record")["collateral_facts_holding"],
        )

    def test_under_U_neither_side_of_either_boundary_is_available(self) -> None:
        u = reading_facts(READING_U)
        for name in ("record", "record+naming_reaches_inward", "opaque", "discard"):
            holds = named(u["points"], name)["collateral_facts_holding"]
            self.assertNotIn("inner_side_internally_available", holds)
            self.assertNotIn("outer_side_internally_available", holds)


class InnerWholeTests(unittest.TestCase):
    def test_no_policy_makes_a_second_initial_datum(self) -> None:
        for reading in (READING_U, READING_O):
            g = deep_genesis(reading)
            for row in reading_facts(reading)["point_detail"]:
                self.assertTrue(row["initial_datum_unchanged"])
                self.assertTrue(row["reading_unchanged"])
            for policy in POLICY_SPACE:
                held = retain(reading, read_nested_whole(INSCRIPTION), policy, INSCRIPTION)
                if held.deep is not None:
                    self.assertEqual(held.deep.initial_datum, g.initial_datum)

    def test_a_further_mark_within_the_inner_whole_needs_the_recording_policy(self) -> None:
        for reading in (READING_U, READING_O):
            for policy in POLICY_SPACE:
                point = Point(policy)
                held = retain(reading, read_nested_whole(INSCRIPTION), policy, INSCRIPTION)
                facts = further_mark_within_the_inner_whole(reading, point, held)
                self.assertEqual(facts["possible"], policy == POLICY_ADDRESS)

    def test_the_deepest_place_a_policy_names_is_read_off_the_domain(self) -> None:
        # What refuses the probe at a one-step policy is this census and not
        # the policy's name: the deep grammar is policy-agnostic and records
        # the requested address under every admitting policy.
        for reading in (READING_U, READING_O):
            # The refusing policy admits every member of the domain that
            # carries no nested item, so its own admissions reach depth one.
            self.assertEqual(deepest_place_a_policy_names(reading, Point(POLICY_REFUSE)), 1)
            self.assertEqual(deepest_place_a_policy_names(reading, Point(POLICY_OPAQUE)), 1)
            self.assertEqual(deepest_place_a_policy_names(reading, Point(POLICY_FLATTEN)), 1)
            self.assertEqual(deepest_place_a_policy_names(reading, Point(POLICY_ADDRESS)), 2)

    def test_the_probe_reports_the_address_the_replay_kept_at_every_point(self) -> None:
        # The refusal must not deny what the same object reports: at the two
        # one-step policies the replay does record a length-two address, and
        # the reason given is that no admission of that policy produces one.
        for reading in (READING_U, READING_O):
            for policy in (POLICY_OPAQUE, POLICY_FLATTEN, POLICY_ADDRESS):
                held = retain(reading, read_nested_whole(INSCRIPTION), policy, INSCRIPTION)
                facts = further_mark_within_the_inner_whole(reading, Point(policy), held)
                self.assertEqual(facts["address"], [0, 1])
                self.assertTrue(facts["recorded_at_the_requested_place"])
                self.assertEqual(
                    facts["deepest_place_the_policy_names"],
                    deepest_place_a_policy_names(reading, Point(policy)),
                )
                self.assertIn(str(facts["deepest_place_the_policy_names"]), facts["because"])

    def test_a_place_is_nameable_exactly_when_the_policy_names_one_that_deep(self) -> None:
        self.assertTrue(a_place_of_that_depth_is_nameable(2, 2))
        self.assertTrue(a_place_of_that_depth_is_nameable(1, 2))
        self.assertFalse(a_place_of_that_depth_is_nameable(2, 1))
        self.assertFalse(a_place_of_that_depth_is_nameable(1, 0))
        self.assertFalse(a_place_of_that_depth_is_nameable(0, 2))

    def test_what_the_inner_whole_is_under_each_policy(self) -> None:
        self.assertEqual(sorted(WHAT_THE_INNER_WHOLE_IS), sorted(POLICY_SPACE))
        self.assertIn("MARK", WHAT_THE_INNER_WHOLE_IS[POLICY_OPAQUE])
        self.assertIn("NOTHING", WHAT_THE_INNER_WHOLE_IS[POLICY_FLATTEN])
        self.assertIn("BOUNDARY", WHAT_THE_INNER_WHOLE_IS[POLICY_ADDRESS])
        self.assertIn("not admissible", WHAT_THE_INNER_WHOLE_IS[POLICY_REFUSE])


class MeasureTests(unittest.TestCase):
    def test_the_minima_are_two_tied_classes_under_both_readings(self) -> None:
        for reading in (READING_U, READING_O):
            facts = reading_facts(reading)
            by_mu1 = facts["minima_by_mu1"]
            self.assertEqual(by_mu1["minimum"], 1)
            self.assertEqual(sorted(by_mu1["points"]), ["discard", "opaque"])
            self.assertEqual(by_mu1["class_count"], 2)
            self.assertFalse(by_mu1["unique"])

    def test_the_two_measures_select_different_minima(self) -> None:
        # The first rung at which they part under BOTH readings: at Challenge 3
        # they parted under O alone, and at Challenge 4 they agreed under both.
        for reading in (READING_U, READING_O):
            facts = reading_facts(reading)
            self.assertFalse(facts["measures_agree_on_minima"])
            self.assertTrue(facts["measures_differ_somewhere"])
            self.assertEqual(facts["minima_by_mu2"]["points"], ["discard"])
            self.assertEqual(facts["minima_by_mu2"]["class_count"], 1)

    def test_the_collateral_measure_counts_only_what_the_base_lacked(self) -> None:
        base = {name: False for name in COLLATERAL_FACTS}
        base[COLLATERAL_FACTS[0]] = True
        facts = {name: True for name in COLLATERAL_FACTS}
        self.assertEqual(mu2(facts, base), len(COLLATERAL_FACTS) - 1)
        self.assertEqual(mu2(base, base), 0)
        self.assertEqual(holding(base), [COLLATERAL_FACTS[0]])

    def test_a_fact_is_false_where_nothing_is_retained(self) -> None:
        for reading in (READING_U, READING_O):
            held = retain(
                reading, read_nested_whole(INSCRIPTION), POLICY_REFUSE, INSCRIPTION
            )
            self.assertIsNone(held.deep)
            self.assertIsNotNone(held.refusal)
            facts = collateral_facts(reading, BASE_POINT, held)
            self.assertFalse(facts["nesting_internally_visible"])
            self.assertFalse(facts["inner_side_internally_available"])
            self.assertFalse(facts["outer_side_internally_available"])
            self.assertFalse(facts["inner_whole_presentation_admitted"])

    def test_the_facts_that_agree_everywhere_are_named(self) -> None:
        # The measure counts facts and not independent facts, and the rung
        # reports where it counts one thing twice rather than leaving it.
        for reading in (READING_U, READING_O):
            rows = reading_facts(reading)["points"]
            pairs = facts_agreeing_everywhere(rows)
            self.assertIn(
                ["nesting_internally_visible",
                 "depth_takes_more_than_one_value_over_the_domain"],
                pairs,
            )
            for a, b in pairs:
                self.assertEqual(
                    [a in row["collateral_facts_holding"] for row in rows],
                    [b in row["collateral_facts_holding"] for row in rows],
                )

    def test_the_agreement_check_reads_both_ways(self) -> None:
        rows: list[Json] = [
            {"collateral_facts_holding": [COLLATERAL_FACTS[0], COLLATERAL_FACTS[1]]},
            {"collateral_facts_holding": [COLLATERAL_FACTS[1]]},
        ]
        pairs = facts_agreeing_everywhere(rows)
        self.assertNotIn([COLLATERAL_FACTS[0], COLLATERAL_FACTS[1]], pairs)
        rows[1]["collateral_facts_holding"] = [COLLATERAL_FACTS[0], COLLATERAL_FACTS[1]]
        self.assertIn(
            [COLLATERAL_FACTS[0], COLLATERAL_FACTS[1]], facts_agreeing_everywhere(rows)
        )

    def test_the_bundles_are_refused_and_counted(self) -> None:
        for reading in (READING_U, READING_O):
            facts = reading_facts(reading)
            self.assertEqual(facts["bundles_refused_count"], 4)
            self.assertIn("record", facts["bundles_refused"])
            self.assertNotIn("record", facts["one_step_points"])
            for row in facts["points"]:
                self.assertEqual(row["bundles"], row["mu1"] >= 2)

    def test_the_price_is_read_off_the_enumeration(self) -> None:
        for reading in (READING_U, READING_O):
            facts = reading_facts(reading)
            price = facts["price"]
            self.assertFalse(price["retained_without_a_new_capability"])
            self.assertEqual(price["minimum_capability_count"], 1)
            self.assertEqual(price["what_the_caller_asked_for_costs"], 2)
            self.assertFalse(price["what_the_caller_asked_for_is_one_step"])
            self.assertEqual(price["new_at_challenge_5"], sorted([CAP_AS_MARK, CAP_REACH]))
            self.assertEqual(price["paid_by"], "the run")

    def test_the_declared_price_fields_do_not_move_with_the_enumeration(self) -> None:
        rows = [
            {"name": "refuse", "capabilities": [], "admits": False},
            {"name": "opaque", "capabilities": [CAP_AS_MARK], "admits": True},
            {"name": "discard", "capabilities": [CAP_REACH], "admits": True},
        ]
        by_mu1: Json = {
            "minimum": 1,
            "classes": [{"members": ["opaque"]}, {"members": ["discard"]}],
        }
        moved = price_facts(READING_U, by_mu1, rows)
        alone: Json = {"minimum": 1, "classes": [{"members": ["opaque"]}]}
        other = price_facts(READING_U, alone, rows)
        for field in PRICE_FIELDS_DECLARED:
            self.assertEqual(moved[field], other[field])
        self.assertNotEqual(moved["new_at_challenge_5"], other["new_at_challenge_5"])


class OrderTests(unittest.TestCase):
    def test_the_within_whole_order_is_invisible_at_the_caller_inscription(self) -> None:
        for reading in (READING_U, READING_O):
            facts = order_facts(reading)
            self.assertTrue(facts["at_the_caller_inscription_isomorphic"])
            self.assertEqual(facts["domain_size"], 144)
            # It moves the STATE at most of the domain and no state's class:
            # a reordering of admissions is a permutation of the internal
            # identities, which every point of this space permits.
            self.assertGreater(int(facts["domain_inscriptions_where_the_states_differ"]), 0)
            self.assertEqual(
                int(facts["domain_inscriptions_where_the_orders_part_up_to_renaming"]), 0
            )

    def test_the_order_moves_the_state_and_not_its_class(self) -> None:
        whole = read_nested_whole("<a|b>")
        declared = deep_replay(
            policy_history(whole, POLICY_ADDRESS), deep_genesis(READING_U)
        )
        other = deep_replay(
            policy_history(whole, POLICY_ADDRESS, DECLARED_CONVENTION, OTHER_WITHIN_WHOLE_ORDER),
            deep_genesis(READING_U),
        )
        self.assertNotEqual(declared, other)
        self.assertTrue(deep_is_isomorphic(declared, other, LEVELS))


class EnumerationTests(unittest.TestCase):
    def test_the_permitted_images_match_an_unpruned_re_derivation(self) -> None:
        base = deep_replay(
            [Supply("a"), AdmitAt("a", (0, 1)), Supply("b"), AdmitAt("b", (1, 0))],
            deep_genesis(READING_U),
        )
        for levels in ((), (0,), (1,), (0, 1)):
            got = deep_permitted_images(base, levels)
            expected = []
            for flips in level_flip_sets(levels):
                moved = base
                for level in flips:
                    moved = exchange_level(moved, level)
                for pi in permutations(range(base.n_marks())):
                    expected.append((flips, tuple(pi), deep_rename_marks(moved, pi)))
            self.assertEqual(got, expected)
            self.assertEqual(len(got), 2 ** len(levels) * 2)

    def test_the_automorphisms_filter_the_full_enumeration(self) -> None:
        base = deep_replay(
            [Supply("a"), AdmitAt("a", (0,)), Supply("a"), AdmitAt("a", (1,))],
            deep_genesis(READING_U),
        )
        autos = deep_automorphisms(base, LEVELS)
        expected = [
            (flips, pi)
            for flips, pi, image in deep_permitted_images(base, LEVELS)
            if deep_serialize(image) == deep_serialize(base)
        ]
        self.assertEqual(autos, expected)
        self.assertTrue(any(flips for flips, _pi in autos))

    def test_the_canonical_key_is_the_minimum_over_the_images(self) -> None:
        base = deep_replay(
            [Supply("a"), AdmitAt("a", (1, 1))], deep_genesis(READING_U)
        )
        key = deep_canonical(base, LEVELS)
        images = [
            deep_serialize(image) for _f, _p, image in deep_permitted_images(base, LEVELS)
        ]
        self.assertEqual(key, min(images))
        self.assertEqual(key, (READING_U, ((0, 0),)))

    def test_the_flip_sets_are_the_power_set(self) -> None:
        self.assertEqual(level_flip_sets(()), [()])
        self.assertEqual(level_flip_sets((0,)), [(), (0,)])
        self.assertEqual(level_flip_sets((0, 1)), [(), (0,), (0, 1), (1,)])
        self.assertEqual(level_flip_sets((1, 1, 0)), level_flip_sets((0, 1)))

    def test_the_orbit_is_read_off_the_same_enumeration(self) -> None:
        base = deep_replay(
            [Supply("a"), AdmitAt("a", (0, 1))], deep_genesis(READING_U)
        )
        self.assertEqual(
            deep_mark_orbit(base, 0, LEVELS),
            frozenset({(0, 0), (0, 1), (1, 0), (1, 1)}),
        )
        self.assertEqual(deep_mark_orbit(base, 0, ()), frozenset({(0, 1)}))
        with self.assertRaisesRegex(ValueError, "is not admitted"):
            deep_mark_orbit(base, 5, LEVELS)


class ScoreTests(unittest.TestCase):
    def test_scores(self) -> None:
        receipt = build()
        scores = receipt["scores"]
        for cid in ("C5-2", "C5-3", "C5-4", "C5-5", "C5-6", "C5-7", "C5-8"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        # C5-1's readers clause hits and its ordinal clause misses, so the
        # prediction is PARTIAL and the miss is recorded next to its value.
        self.assertEqual(scores["C5-1"]["status"], "PARTIAL")
        self.assertEqual(scores["C5-X"]["status"], "PENDING")
        self.assertEqual(scores["C4-X"]["status"], "PARTIAL")

    def test_the_one_widening_is_given_two_ordinals_and_both_are_scored(self) -> None:
        # The frozen C4-X says the bound is widened "a second time" and the
        # frozen C5-1 says "a third time" of the same event.  One census of the
        # run's reader bounds settles both: three bounds, two widenings.
        receipt = build()
        reader = receipt["reader"]
        self.assertEqual(reader["reader_bounds_declared"], 3)
        self.assertEqual(reader["widenings_of_the_reader_bound"], 2)
        self.assertEqual(len(reader["inherited_readers"]), 2)
        self.assertEqual(
            receipt["scores"]["C4-X"]["widening_ordinal_clause_status"], "HIT"
        )
        self.assertEqual(
            receipt["scores"]["C5-1"]["widening_ordinal_clause_status"], "MISSED"
        )
        self.assertEqual(receipt["scores"]["C5-1"]["readers_clause_status"], "HIT")

    def test_the_previous_extrapolation_is_scored_clause_by_clause(self) -> None:
        scores = build()["scores"]["C4-X"]
        self.assertEqual(scores["reader_refuses_clause_status"], "HIT")
        self.assertEqual(scores["widening_priced_clause_status"], "HIT")
        self.assertEqual(scores["widening_ordinal_clause_status"], "HIT")
        self.assertEqual(
            scores["depth_not_available_without_a_declaration_clause_status"], "HIT"
        )
        self.assertEqual(
            scores["nesting_not_visible_without_a_declaration_clause_status"], "HIT"
        )
        self.assertEqual(scores["inner_whole_not_a_datum_clause_status"], "HIT")
        self.assertEqual(scores["declared_finite_policy_space_clause_status"], "HIT")
        self.assertEqual(scores["exactly_one_member_retains_clause_status"], "MISSED")
        self.assertEqual(len(scores["policies_admitting_the_inscription"]), 3)
        self.assertEqual(
            scores["points_where_the_nesting_is_internally_visible"],
            ["record", "record+naming_reaches_inward"],
        )

    def test_tally_counts(self) -> None:
        receipt = build()
        counts = receipt["tally"]
        self.assertEqual(list(counts["scored"]), list(SCORED_PREDICTIONS))
        self.assertEqual(
            list(counts["definition_level_declared"]), list(DEFINITION_LEVEL_PREDICTIONS)
        )
        self.assertEqual(counts["hit_definition_level"], ["C5-2"])
        self.assertEqual(
            counts["hit_as_content"], ["C5-3", "C5-4", "C5-5", "C5-6", "C5-7", "C5-8"]
        )
        self.assertEqual(counts["partial"], ["C5-1"])
        self.assertEqual(counts["missed"], [])

    def test_tally_refuses_an_unknown_status(self) -> None:
        scores = {cid: {"status": "HIT"} for cid in SCORED_PREDICTIONS}
        scores[SCORED_PREDICTIONS[0]] = {"status": "SHARPENED"}
        with self.assertRaisesRegex(ValueError, "unexpected status"):
            tally(scores)

    def test_tally_moves_a_miss_out_of_every_hit_list(self) -> None:
        scores = {cid: {"status": "HIT"} for cid in SCORED_PREDICTIONS}
        scores["C5-3"] = {"status": "MISSED"}
        scores["C5-1"] = {"status": "PARTIAL"}
        counts = tally(scores)
        self.assertEqual(counts["missed"], ["C5-3"])
        self.assertEqual(counts["partial"], ["C5-1"])
        self.assertNotIn("C5-3", counts["hit_as_content"])
        self.assertNotIn("C5-1", counts["hit_definition_level"])


class ScorerNegativeTests(unittest.TestCase):
    """Each frozen prediction is scored MISSED when the fact it names moves."""

    def setUp(self) -> None:
        self.u = reading_facts(READING_U)
        self.o = reading_facts(READING_O)
        self.reader = reader_facts()

    def scored(self, u: Json, o: Json, reader: Json) -> Json:
        return score(u, o, reader)

    def test_c5_1_misses_when_an_inherited_reader_accepts(self) -> None:
        reader = copy.deepcopy(self.reader)
        reader["inherited_readers_refuse_both"] = False
        self.assertEqual(self.scored(self.u, self.o, reader)["C5-1"]["status"], "MISSED")
        reader = copy.deepcopy(self.reader)
        reader["beyond_the_bound_refused"] = False
        self.assertEqual(self.scored(self.u, self.o, reader)["C5-1"]["status"], "MISSED")

    def test_c5_1_hits_only_where_the_run_has_widened_three_times(self) -> None:
        # The direction the real receipt cannot show: with a third widening in
        # the census the frozen ordinal would hold and C5-1 would be a HIT,
        # while C4-X's "a second time" would then miss.
        reader = copy.deepcopy(self.reader)
        reader["reader_bounds_declared"] = 4
        reader["widenings_of_the_reader_bound"] = 3
        scored = self.scored(self.u, self.o, reader)
        self.assertEqual(scored["C5-1"]["widening_ordinal_clause_status"], "HIT")
        self.assertEqual(scored["C5-1"]["status"], "HIT")
        self.assertEqual(scored["C4-X"]["widening_ordinal_clause_status"], "MISSED")
        self.assertEqual(scored["C4-X"]["status"], "PARTIAL")

    def test_c5_2_misses_when_a_policy_price_moves(self) -> None:
        u = copy.deepcopy(self.u)
        u["policies"][3]["capability_count"] = 1
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-2"]["status"], "MISSED")
        u = copy.deepcopy(self.u)
        u["one_step_iff_capability_count_one"] = False
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-2"]["status"], "MISSED")

    def test_c5_3_misses_when_a_one_step_policy_sees_the_nesting(self) -> None:
        u = copy.deepcopy(self.u)
        named(u["point_detail"], "opaque")["flat_inscription_isomorphic"] = False
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-3"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        named(o["points"], "discard")["collateral_facts_holding"].append(
            "nesting_internally_visible"
        )
        self.assertEqual(self.scored(self.u, o, self.reader)["C5-3"]["status"], "MISSED")

    def test_c5_4_misses_when_the_two_one_step_policies_agree(self) -> None:
        u = copy.deepcopy(self.u)
        u["policy_separation"]["same_policy_on_the_domain"] = True
        u["policy_separation"]["inscriptions_where_they_part"] = 0
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-4"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        o["minima_by_mu1"]["class_count"] = 1
        self.assertEqual(self.scored(self.u, o, self.reader)["C5-4"]["status"], "MISSED")

    def test_c5_5_misses_when_a_one_step_policy_enters_the_inner_whole(self) -> None:
        u = copy.deepcopy(self.u)
        named(u["point_detail"], "opaque")["further_mark_within_the_inner_whole"][
            "possible"
        ] = True
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-5"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        named(o["point_detail"], "record")["initial_datum_unchanged"] = False
        self.assertEqual(self.scored(self.u, o, self.reader)["C5-5"]["status"], "MISSED")

    def test_c5_6_misses_when_depth_moves_or_the_grammar_reads_it(self) -> None:
        u = copy.deepcopy(self.u)
        named(u["point_detail"], "record")["depths_over_the_domain"] = [1]
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-6"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        named(o["points"], "record")["collateral_facts_holding"].append(
            "depth_expressible_in_the_closed_grammar"
        )
        self.assertEqual(self.scored(self.u, o, self.reader)["C5-6"]["status"], "MISSED")

    def test_c5_7_misses_when_the_naming_coordinate_moves(self) -> None:
        u = copy.deepcopy(self.u)
        u["naming_coordinate_collapses_everywhere"] = False
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-7"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        named(o["point_detail"], "record")["mark_address_orbit_size"] = 1
        self.assertEqual(self.scored(self.u, o, self.reader)["C5-7"]["status"], "MISSED")

    def test_c5_8_misses_when_a_retained_state_does_not_replay(self) -> None:
        u = copy.deepcopy(self.u)
        named(u["point_detail"], "record")["replays_from_genesis"] = False
        self.assertEqual(self.scored(u, self.o, self.reader)["C5-8"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        named(o["point_detail"], "opaque")["event_follows_relation_empty"] = False
        self.assertEqual(self.scored(self.u, o, self.reader)["C5-8"]["status"], "MISSED")

    def test_c4x_hits_only_if_one_policy_admits_the_inscription(self) -> None:
        # The clause the rung records as MISSED, scored in both directions:
        # with two of the three admitting policies removed it would HIT.
        u = copy.deepcopy(self.u)
        for row in u["policies"]:
            if row["policy"] in ("opaque", "discard"):
                row["admits_the_caller_inscription"] = False
        scored = self.scored(u, self.o, self.reader)["C4-X"]
        self.assertEqual(scored["exactly_one_member_retains_clause_status"], "HIT")
        self.assertEqual(scored["status"], "HIT")

    def test_c4x_misses_when_the_reader_accepts_the_nested_whole(self) -> None:
        reader = copy.deepcopy(self.reader)
        for row in reader["inherited_readers"]:
            row["refused"] = False
        reader["inherited_readers_refuse_both"] = False
        scored = self.scored(self.u, self.o, reader)["C4-X"]
        self.assertEqual(scored["reader_refuses_clause_status"], "MISSED")
        self.assertEqual(scored["status"], "MISSED")

    def test_c4x_misses_when_depth_arrives_with_no_declaration(self) -> None:
        u = copy.deepcopy(self.u)
        named(u["points"], "opaque")["collateral_facts_holding"].append(
            "depth_takes_more_than_one_value_over_the_domain"
        )
        scored = self.scored(u, self.o, self.reader)["C4-X"]
        self.assertEqual(
            scored["depth_not_available_without_a_declaration_clause_status"], "MISSED"
        )
        self.assertEqual(scored["status"], "MISSED")

    def test_c4x_misses_when_a_one_step_policy_sees_the_boundary_within_a_side(
        self,
    ) -> None:
        # The direction the real receipt cannot show: the frozen clause "the
        # boundary within a side will not be visible without a new declaration"
        # would MISS if the nesting were visible at a policy of capability
        # count one.  It reads HIT on the real receipt, where the nesting is
        # visible only at the recording policy, which costs two.
        u = copy.deepcopy(self.u)
        named(u["points"], "discard")["collateral_facts_holding"].append(
            "nesting_internally_visible"
        )
        scored = self.scored(u, self.o, self.reader)["C4-X"]
        self.assertEqual(
            scored["nesting_not_visible_without_a_declaration_clause_status"], "MISSED"
        )
        self.assertEqual(scored["status"], "MISSED")
        o = copy.deepcopy(self.o)
        named(o["points"], "opaque")["collateral_facts_holding"].append(
            "nesting_internally_visible"
        )
        scored = self.scored(self.u, o, self.reader)["C4-X"]
        self.assertEqual(
            scored["nesting_not_visible_without_a_declaration_clause_status"], "MISSED"
        )


class ShapeTests(unittest.TestCase):
    def test_receipt_shape(self) -> None:
        receipt = build()
        self.assertEqual(receipt["challenge"], 5)
        self.assertEqual(receipt["inscription"], INSCRIPTION)
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["new_event_kinds_at_challenge_5"], ["AdmitAt"])
        self.assertEqual(receipt["withdrawn_rules_at_challenge_5"], [])
        self.assertEqual(receipt["state_event_generators"], [])
        self.assertEqual(receipt["closed_grammar_forms_reading_depth"], [])
        self.assertEqual(receipt["outside_of_the_outermost_boundary"]["status"], "OPEN")
        self.assertFalse(receipt["outside_of_the_outermost_boundary"]["formulable"])
        self.assertEqual(receipt["domain"]["size"], 144)
        self.assertTrue(receipt["domain"]["caller_inscription_in_the_domain"])
        self.assertEqual(receipt["policy_space"]["size"], 8)
        self.assertEqual(sorted(receipt["boundary_dependence"]), sorted(challenge5.BOUNDARY_DEPENDENCE))
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

    def test_the_event_census_names_this_rung_history_builders(self) -> None:
        census = build()["event_returning_functions_by_module"]
        self.assertEqual(census["model"], [])
        self.assertEqual(census["presentation"], ["admission_event", "supply_event"])
        self.assertIn("policy_history", census["challenge5"])
        self.assertIn("flat_history", census["challenge5"])
        self.assertIn("probes", census["challenge5"])

    def test_a_point_row_and_its_detail_agree(self) -> None:
        for reading in (READING_U, READING_O):
            base_facts = collateral_facts(
                reading,
                BASE_POINT,
                retain(reading, read_nested_whole(INSCRIPTION), POLICY_REFUSE, INSCRIPTION),
            )
            for point in point_space():
                row = point_row(reading, point, base_facts)
                detail = point_detail(reading, point, base_facts)
                for key, value in row.items():
                    self.assertEqual(detail[key], value, (reading, point_name(point), key))

    def test_the_probe_set_offers_every_event_kind_of_the_deep_grammar(self) -> None:
        kinds = {type(e).__name__ for e in probes(CALLER_TOKEN)}
        self.assertEqual(kinds, {"Supply", "AdmitAt"})
        self.assertTrue(
            all(not deep_event_follows(deep_genesis(READING_U), e) for e in probes("a"))
        )

    def test_the_policy_rows_report_what_admits_the_inscription(self) -> None:
        rows = policy_rows(READING_U)
        self.assertEqual(
            [row["admits_the_caller_inscription"] for row in rows],
            [False, True, True, True],
        )
        self.assertEqual([row["policy"] for row in rows], [POLICY_NAMES[p] for p in POLICY_SPACE])

    def test_named_refuses_an_absent_row(self) -> None:
        with self.assertRaises(StopIteration):
            named([{"name": "opaque"}], "zzz probe point")


class DeepKernelTests(unittest.TestCase):
    def test_a_deep_regime_refuses_an_ill_formed_address(self) -> None:
        with self.assertRaisesRegex(AdmissionError, "crosses at least one boundary"):
            DeepRegime(READING_U, ("a",), ((),))
        with self.assertRaisesRegex(AdmissionError, "names side 0 or side 1"):
            DeepRegime(READING_U, ("a",), ((2,),))
        with self.assertRaisesRegex(AdmissionError, "equal length"):
            DeepRegime(READING_U, ("a",), ())
        with self.assertRaisesRegex(AdmissionError, "unknown reading"):
            DeepRegime("Z", (), ())
        with self.assertRaisesRegex(AdmissionError, "initial datum is fixed"):
            DeepRegime(READING_U, (), (), OpaqueDatum(1))

    def test_a_deep_step_refuses_an_ill_formed_admission(self) -> None:
        g = deep_genesis(READING_U)
        with self.assertRaisesRegex(AdmissionError, "crosses at least one boundary"):
            deep_step(g, AdmitAt("a", ()))
        with self.assertRaisesRegex(AdmissionError, "names side 0 or 1"):
            deep_step(g, AdmitAt("a", (0, 3)))
        self.assertEqual(deep_step(g, Supply("a")), g)

    def test_deep_certify_reads_false_on_a_refused_history(self) -> None:
        g = deep_genesis(READING_U)
        self.assertFalse(deep_certify([AdmitAt("a", (0,))], g, g))
        self.assertTrue(deep_certify([Supply("a")], g, g))

    def test_flatten_deep_discards_every_crossing_but_the_outermost(self) -> None:
        r = DeepRegime(READING_U, ("a", "b"), ((0, 1), (1, 0)))
        self.assertEqual(flatten_deep(r), Regime(READING_U, ("a", "b"), (0, 1)))
        self.assertEqual(flatten_deep(exchange_level(r, 1)), flatten_deep(r))
        self.assertNotEqual(flatten_deep(exchange_level(r, 0)), flatten_deep(r))

    def test_exchange_level_leaves_a_shorter_address_alone(self) -> None:
        r = DeepRegime(READING_U, ("a", "b"), ((0,), (0, 0)))
        self.assertEqual(exchange_level(r, 1).addresses, ((0,), (0, 1)))
        self.assertEqual(exchange_level(r, 0).addresses, ((1,), (1, 0)))
        self.assertEqual(exchange_level(exchange_level(r, 1), 1), r)
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            exchange_level(r, -1)

    def test_deep_renaming_refuses_a_non_permutation(self) -> None:
        r = DeepRegime(READING_U, ("a", "b"), ((0,), (1,)))
        self.assertEqual(deep_rename_marks(r, (1, 0)).addresses, ((1,), (0,)))
        with self.assertRaisesRegex(ValueError, "not a permutation"):
            deep_rename_marks(r, (0, 0))

    def test_deep_serialize_keeps_the_labels_only_when_asked(self) -> None:
        r = DeepRegime(READING_U, ("a",), ((0,),))
        self.assertEqual(deep_serialize(r), (READING_U, ((0,),)))
        self.assertEqual(deep_serialize(r, True), (READING_U, ("a",), ((0,),)))

    def test_regimes_of_different_readings_are_never_isomorphic(self) -> None:
        u = DeepRegime(READING_U, ("a",), ((0,),))
        o = DeepRegime(READING_O, ("a",), ((0,),))
        self.assertFalse(deep_is_isomorphic(u, o, LEVELS))

    def test_depth_of_refuses_an_unadmitted_mark(self) -> None:
        r = DeepRegime(READING_U, ("a",), ((0, 1),))
        self.assertEqual(depth_of(r, 0), 2)
        with self.assertRaisesRegex(ValueError, "is not admitted"):
            depth_of(r, 1)

    def test_the_deep_model_at_unit_addresses_is_the_inherited_model(self) -> None:
        # The compatibility the rung rests on: a policy that records one side
        # per mark is the deep model with every address of length one, and its
        # flattening is exactly the inherited replay.
        for reading in (READING_U, READING_O):
            for text in domain_texts():
                whole = read_nested_whole(text)
                for policy in (POLICY_OPAQUE, POLICY_FLATTEN):
                    deep = deep_replay(policy_history(whole, policy), deep_genesis(reading))
                    inherited = replay(flat_history(whole, policy), genesis(reading))
                    self.assertEqual(flatten_deep(deep), inherited)


class BuildTimeTests(unittest.TestCase):
    def test_the_readings_are_separate_towers(self) -> None:
        receipt = build()
        u = receipt["readings"][READING_U]
        o = receipt["readings"][READING_O]
        self.assertEqual(u["reading"], READING_U)
        self.assertEqual(o["reading"], READING_O)
        self.assertNotEqual(
            [row["mu2"] for row in u["points"]], [row["mu2"] for row in o["points"]]
        )
        self.assertEqual(
            [row["mu1"] for row in u["points"]], [row["mu1"] for row in o["points"]]
        )

    def test_every_declared_product_is_enumerated(self) -> None:
        self.assertEqual(
            [(p.policy, p.naming_reaches_inward) for p in point_space()],
            [(policy, naming) for policy in POLICY_SPACE for naming in (False, True)],
        )
        self.assertEqual(
            len(list(product(POLICY_SPACE, (False, True)))), len(point_space())
        )


    def test_the_order_census_reads_a_different_count_at_each_policy(self) -> None:
        # The receipt's `order` block is computed at the recording policy and
        # carries no policy field, so the number 116 is that policy's.  The
        # same census at the other two admitting policies reads 121 and 108,
        # which is why the paper's row and B5-ORDER name the policy.  The
        # receipt is not regenerated for this; the scope is stated in prose and
        # the three numbers are computed here.
        counts = {}
        for policy in (POLICY_ADDRESS, POLICY_OPAQUE, POLICY_FLATTEN):
            moved = 0
            for whole in domain():
                declared = deep_replay(
                    policy_history(whole, policy), deep_genesis(READING_U)
                )
                other = deep_replay(
                    policy_history(
                        whole, policy, DECLARED_CONVENTION, OTHER_WITHIN_WHOLE_ORDER
                    ),
                    deep_genesis(READING_U),
                )
                moved += declared != other
            counts[POLICY_NAMES[policy]] = moved
        self.assertEqual(counts, {"record": 116, "opaque": 121, "discard": 108})
        self.assertEqual(
            int(order_facts(READING_U)["domain_inscriptions_where_the_states_differ"]),
            counts["record"],
        )


class C4XNegativeDirectionTests(unittest.TestCase):
    """The three C4-X clause statuses that were only ever asserted in the HIT
    direction.  Review found the gap: the rung claimed the negative direction of
    every scored clause was tested, and three of C4-X's eight were not."""

    def facts(self) -> tuple[Json, Json, Json]:
        return (
            reading_facts(READING_U),
            reading_facts(READING_O),
            reader_facts(),
        )

    def test_c4x_widening_priced_clause_misses_when_the_run_does_not_pay(self) -> None:
        u, o, reader = self.facts()
        moved = copy.deepcopy(reader)
        moved["paid_by"] = "the caller"
        self.assertEqual(
            score_c4x(u, o, moved)["widening_priced_clause_status"], "MISSED"
        )
        self.assertEqual(score_c4x(u, o, reader)["widening_priced_clause_status"], "HIT")

    def test_c4x_datum_clause_misses_when_a_point_changes_the_initial_datum(self) -> None:
        u, o, reader = self.facts()
        moved = copy.deepcopy(u)
        moved["point_detail"][0]["initial_datum_unchanged"] = False
        self.assertEqual(
            score_c4x(moved, o, reader)["inner_whole_not_a_datum_clause_status"],
            "MISSED",
        )
        self.assertEqual(
            score_c4x(u, o, reader)["inner_whole_not_a_datum_clause_status"], "HIT"
        )

    def test_c4x_space_clause_misses_when_the_policy_space_is_shorter(self) -> None:
        u, o, reader = self.facts()
        moved = copy.deepcopy(o)
        moved["policies"] = moved["policies"][:-1]
        self.assertEqual(
            score_c4x(u, moved, reader)["declared_finite_policy_space_clause_status"],
            "MISSED",
        )
        self.assertEqual(
            score_c4x(u, o, reader)["declared_finite_policy_space_clause_status"], "HIT"
        )


if __name__ == "__main__":
    unittest.main()
