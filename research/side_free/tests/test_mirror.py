"""The mirror, the forgetting map, and the forgetful lemma.

The lemma is the fairness guard that runs AGAINST the pinned world: any
structure the side-free carrier keeps beyond forgetting shrinks its
automorphism set below the image of the side-typed one, and the lemma then
fails by name at a named cell.  The injection here is what proves it fires.
"""

from __future__ import annotations

import json
import pathlib
import sys
import unittest
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "code"))

from sidefree import mirror as mir  # noqa: E402
from sidefree.enumerate import enumerate_rows, minima  # noqa: E402
from sidefree.model import Regime as SideFreeRegime  # noqa: E402
from sidefree.model import automorphisms_under as free_automorphisms  # noqa: E402
from sidefree.requirement import separates  # noqa: E402

TREE = pathlib.Path(__file__).resolve().parent.parent
PIN = json.loads((TREE / "pinned" / "boundary_challenge3.json").read_text("utf-8"))
LEMMA: Any = mir.forgetful_lemma(False)
INJECTED: Any = mir.forgetful_lemma(True)


class MirrorCarrierBasics(unittest.TestCase):
    def test_the_mirror_refuses_an_ill_formed_regime_by_name(self) -> None:
        with self.assertRaises(mir.MirrorError):
            mir.Regime("Q", (), ())
        with self.assertRaises(mir.MirrorError):
            mir.Regime("U", ("a",), ())
        with self.assertRaises(mir.MirrorError):
            mir.Regime("U", ("a",), (2,))
        with self.assertRaises(mir.MirrorError):
            mir.Regime("U", (), (), mir.OpaqueDatum(1))
        with self.assertRaises(mir.MirrorError):
            mir.MirrorCarrier("Q")

    def test_supply_changes_nothing_and_admission_does(self) -> None:
        g = mir.genesis("U")
        self.assertEqual(mir.step(g, mir.Supply("a")), g)
        self.assertEqual(mir.step(g, mir.AdmitOccurrence("a", 1)).placement, (1,))
        self.assertFalse(mir.event_follows(g, mir.Supply("a")))

    def test_the_moving_admission_refusal_fires_in_this_world(self) -> None:
        r = mir.Regime("U", ("a",), (0,))
        self.assertEqual(mir.step(r, mir.AdmitMark("a", 0)), r)
        with self.assertRaises(mir.MirrorError) as caught:
            mir.step(r, mir.AdmitMark("a", 1))
        self.assertIn("would move it and is refused", str(caught.exception))
        with self.assertRaises(mir.MirrorError):
            mir.step(mir.Regime("U", ("a", "a"), (0, 1)), mir.AdmitMark("a", 0))
        with self.assertRaises(mir.MirrorError):
            mir.step(r, mir.AdmitMark("a", 5))

    def test_replay_and_certify_behave_as_in_the_pinned_world(self) -> None:
        history: list[mir.Event] = [mir.Supply("a"), mir.AdmitOccurrence("a", 0)]
        claimed = mir.replay(history, mir.genesis("U"))
        self.assertTrue(mir.certify(history, mir.genesis("U"), claimed))
        self.assertFalse(
            mir.certify([mir.AdmitOccurrence("q", 0)], mir.genesis("U"), claimed)
        )
        with self.assertRaises(mir.MirrorError):
            mir.replay([mir.AdmitOccurrence("q", 0)], mir.genesis("U"))
        with self.assertRaises(mir.MirrorError):
            mir.replay([mir.AdmitMark("q", 0)], mir.genesis("U"))
        self.assertEqual(
            mir.replay(
                [mir.Supply("a"), mir.AdmitOccurrence("a", 0), mir.AdmitMark("a", 0)],
                mir.genesis("U"),
            ).n_marks(),
            1,
        )

    def test_the_reader_and_the_convention(self) -> None:
        self.assertEqual(mir.read_whole("<|>"), mir.Whole(None, None))
        self.assertEqual(mir.read_whole("<a|>").presented_side, "left")
        self.assertEqual(mir.read_whole("<|a>").presented_side, "right")
        with self.assertRaises(mir.MirrorError):
            mir.read_whole("<ab|>")
        with self.assertRaises(mir.MirrorError):
            mir.read_whole("nonsense")
        self.assertEqual(mir.admitted_side("left", mir.DECLARED_CONVENTION), 0)
        self.assertEqual(mir.admitted_side("left", mir.OTHER_CONVENTION), 1)
        with self.assertRaises(mir.MirrorError):
            mir.admitted_side("left", "no such convention")
        with self.assertRaises(mir.MirrorError):
            mir.admitted_side("sideways", mir.DECLARED_CONVENTION)
        with self.assertRaises(mir.MirrorError):
            mir.caller_history([mir.Whole(None, None)], mir.DECLARED_CONVENTION)

    def test_the_two_judgment_forms(self) -> None:
        r = mir.Regime("O", ("a",), (1,))
        self.assertTrue(mir.observation_holds(r, mir.OnSide(0, 1)))
        self.assertFalse(mir.observation_holds(r, mir.OnSide(0, 0)))
        self.assertFalse(mir.observation_holds(r, mir.OnSide(3, 1)))
        self.assertTrue(mir.observation_holds(r, mir.SideNamed(0, "near")))
        self.assertFalse(
            mir.observation_holds(mir.Regime("U", (), ()), mir.SideNamed(0, "near"))
        )

    def test_renaming_refuses_a_non_permutation(self) -> None:
        with self.assertRaises(ValueError):
            mir.rename_marks(mir.Regime("U", ("a", "z"), (0, 1)), (0, 0))

    def test_the_flagged_family_agrees_with_the_shared_verdict(self) -> None:
        r = mir.Regime("U", ("a", "a"), (0, 1))
        for refl in (False, True):
            for mp in (False, True):
                for kl in (False, True):
                    perms = [pi for _f, pi in mir.automorphisms_under(r, refl, mp, kl)]
                    self.assertEqual(
                        mir.marks_separable_under(r, 0, 1, refl, mp, kl),
                        separates(perms, 0, 1),
                    )

    def test_the_side_exchanging_witness_and_the_canonical_key(self) -> None:
        r = mir.Regime("U", ("a", "a"), (0, 1))
        self.assertIsNotNone(mir.side_exchanging_automorphism_under(r, True, True, False))
        self.assertIsNone(mir.side_exchanging_automorphism_under(r, False, True, False))
        self.assertEqual(mir.canonical_under(r, True, True, False), ("U", (0, 1)))
        self.assertTrue(mir.no_permitted_renaming_moves_an_index(r, False, False))
        self.assertFalse(mir.no_permitted_renaming_moves_an_index(r, True, True))

    def test_isomorphism_never_crosses_the_readings(self) -> None:
        a = mir.Regime("U", ("a",), (0,))
        b = mir.Regime("O", ("a",), (0,))
        self.assertFalse(mir.is_isomorphic_under(a, b, True, True, False))

    def test_the_orbit_and_the_relabelling(self) -> None:
        r = mir.Regime("U", ("a", "a"), (0, 1))
        self.assertEqual(len(mir.mark_orbit_under(r, 0, True, True, False)), 4)
        self.assertEqual(len(mir.mark_orbit_under(r, 0, False, False, False)), 1)
        self.assertEqual(mir.relabelled(r).marks, ("z", "z"))
        self.assertEqual(len(mir.mark_observations(r)), 2)

    def test_point_names_and_the_five_coordinates(self) -> None:
        self.assertEqual(mir.point_name(mir.NULL_AUGMENTATION), "base")
        self.assertEqual(mir.point_name(mir.Augmentation(extra_mark=1)), "extra_mark_1")
        self.assertEqual(mir.point_name(mir.READING_O_BUNDLE), "withdraw_reflection+admit_names")
        self.assertEqual(len(mir.candidate_space()), 48)
        self.assertEqual(len(mir.changed_coordinates(mir.READING_O_BUNDLE)), 2)

    def test_side_zero_is_a_moved_coordinate(self) -> None:
        """The pinned repair: ``extra_mark`` at 0 must not read as unmoved."""
        self.assertEqual(
            mir.changed_coordinates(mir.Augmentation(extra_mark=0)), ["extra_mark"]
        )

    def test_the_event_json_carries_the_side_only_for_admissions(self) -> None:
        self.assertEqual(mir.event_json(mir.Supply("a")), {"kind": "Supply", "token": "a"})
        self.assertEqual(
            mir.event_json(mir.AdmitOccurrence("a", 1)),
            {"kind": "AdmitOccurrence", "side": 1, "token": "a"},
        )
        self.assertEqual(len(mir.probes("a")), 5)

    def test_property_invariance_over_the_declared_domain(self) -> None:
        domain = mir.property_domain("U", 2)
        self.assertEqual(len(domain), 21)
        images = mir.domain_images(domain, True, True)
        side = dict(mir.DECLARED_MARK_PROPERTIES)["on_side_0"]
        index = dict(mir.DECLARED_MARK_PROPERTIES)["has_index_0"]
        self.assertFalse(mir.property_invariant(side, images))
        self.assertFalse(mir.property_invariant(index, images))
        self.assertTrue(
            mir.property_invariant(side, mir.domain_images(domain, False, False))
        )
        self.assertTrue(
            mir.property_separates(side, mir.Regime("U", ("a", "a"), (0, 1)))
        )
        self.assertFalse(dict(mir.DECLARED_MARK_PROPERTIES)["carries_label_a"](
            mir.Regime("U", (), ()), 0
        ))
        self.assertTrue(dict(mir.DECLARED_MARK_PROPERTIES)["on_side_1"](
            mir.Regime("U", ("a",), (1,)), 0
        ))
        self.assertTrue(dict(mir.DECLARED_MARK_PROPERTIES)["has_index_1"](
            mir.Regime("U", ("a", "a"), (0, 1)), 1
        ))


class Forgetting(unittest.TestCase):
    def test_forgetting_keeps_the_marks_and_drops_everything_else(self) -> None:
        r = mir.Regime("O", ("a", "z"), (1, 0))
        self.assertEqual(mir.forget(r), SideFreeRegime(("a", "z")))

    def test_the_lemma_holds_and_is_not_vacuous(self) -> None:
        self.assertTrue(LEMMA["holds"])
        self.assertEqual(LEMMA["violations"], 0)
        self.assertTrue(LEMMA["corollary_holds"])
        self.assertEqual(LEMMA["corollary_violations"], 0)
        self.assertTrue(LEMMA["non_vacuous"])
        self.assertGreater(LEMMA["non_vacuity_cells"], 0)
        self.assertIsNone(LEMMA["first_violation"])
        self.assertIsNone(LEMMA["first_corollary_violation"])
        self.assertFalse(LEMMA["injection_live"])

    def test_the_census_is_the_declared_one(self) -> None:
        self.assertEqual(len(mir.lemma_cells()), 1344)
        self.assertEqual(LEMMA["cells"], 1344)
        self.assertEqual(LEMMA["automorphisms_checked"], 2140)
        self.assertEqual(LEMMA["non_vacuity_cells"], 228)

    def test_the_injection_fires_and_names_its_first_cell(self) -> None:
        """Negative: re-admit the side as a per-mark attribute and the lemma
        must FAIL by name.  A guard that cannot fail is not a guard."""
        self.assertFalse(INJECTED["holds"])
        self.assertEqual(INJECTED["violations"], 12)
        first = INJECTED["first_violation"]
        assert isinstance(first, dict)
        self.assertEqual(first["reading"], "U")
        self.assertEqual(first["labels"], ["a", "a"])
        self.assertEqual(first["placement"], [0, 1])
        self.assertEqual(first["automorphism"], {"reflected": True, "permutation": [1, 0]})
        self.assertTrue(INJECTED["injection_live"])

    def test_reversing_the_injection_returns_the_count_to_zero(self) -> None:
        self.assertEqual(mir.forgetful_lemma(False)["violations"], 0)

    def test_the_injected_permutations_are_the_placement_preserving_ones(self) -> None:
        r = mir.Regime("U", ("a", "a"), (0, 1))
        clean = mir.side_free_permutations(r, True, False, False)
        injected = mir.side_free_permutations(r, True, False, True)
        self.assertEqual(sorted(clean), [(0, 1), (1, 0)])
        self.assertEqual(sorted(injected), [(0, 1)])
        self.assertEqual(sorted(clean), sorted(free_automorphisms(mir.forget(r), True, False)))


class MirrorAgainstThePin(unittest.TestCase):
    def test_every_row_of_every_reading_matches_the_pinned_vector(self) -> None:
        fields = (
            "mu1",
            "mu2",
            "satisfies",
            "satisfies_second_reading",
            "class_key",
            "effective_structure",
            "collateral_facts",
            "one_step",
            "bundles",
        )
        for reading in ("U", "O"):
            rows = enumerate_rows(mir.MirrorCarrier(reading))
            pinned = {r["name"]: r for r in PIN["readings"][reading]["points"]}
            self.assertEqual(len(rows), 48)
            for row in rows:
                for field in fields:
                    self.assertEqual(
                        row[field], pinned[str(row["name"])][field], f"{row['name']}.{field}"
                    )

    def test_the_minima_match_the_pinned_minima(self) -> None:
        for reading in ("U", "O"):
            got: Any = minima(enumerate_rows(mir.MirrorCarrier(reading)), "mu1")
            want = PIN["readings"][reading]["minima_by_mu1"]
            self.assertEqual(got["minimum"], want["minimum"])
            self.assertEqual(got["class_count"], want["class_count"])
            self.assertEqual(got["unique"], want["unique"])
            self.assertEqual(got["points"], want["points"])
            self.assertEqual(
                [c["members"] for c in got["classes"]],
                [c["members"] for c in want["classes"]],
            )

    def test_the_withdrawal_census_reproduces_the_declared_fractions(self) -> None:
        kept = mir.withdrawal_census(True)
        withdrawn = mir.withdrawal_census(False)
        self.assertEqual(len(kept), 64)
        self.assertEqual(sum(kept), 28)
        self.assertEqual(sum(withdrawn), 64)

    def test_the_route_census_domain_carries_the_further_mark(self) -> None:
        base = mir.route_census_regimes("U", mir.NULL_AUGMENTATION)
        extra = mir.route_census_regimes("U", mir.Augmentation(extra_mark=1))
        self.assertEqual(len(base), 16)
        self.assertEqual({r.n_marks() for r in base}, {2})
        self.assertEqual({r.n_marks() for r in extra}, {3})
        self.assertEqual({r.placement[2] for r in extra}, {1})

    def test_the_carrier_view_refuses_a_candidate_of_the_other_world(self) -> None:
        carrier = mir.MirrorCarrier("U")
        with self.assertRaises(TypeError):
            carrier.point_name(object())
        verdicts: Any = carrier.satisfies_under_key_choice(mir.NULL_AUGMENTATION)
        self.assertEqual(verdicts, {"pinned": False})


if __name__ == "__main__":
    unittest.main()
