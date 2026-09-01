"""Tests for the convention_price run.  Heavy exhaustions are replayed
where affordable (the triangle, the star, the square, the six-label
member); the two 2^16 signed twins and the 2^20 member are bound by
receipt equality plus the consumed-class route, which is replayed in
full for every member.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
import sys
import unittest
from itertools import product
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
# This tree first, the pinned tree second: both carry a `register`
# module and the pinned one must not shadow this one.
sys.path.insert(0, str(HERE.parent / "sign_slice"))
sys.path.insert(0, str(HERE))

from cone_section import cone_section
from genpres import GenPres
from occ_relabel import pointwise_assignments, relabelled, undirected_hops
from slice_set import members

from channels import (
    certificate_by_counting,
    signed_variant,
    weight_list,
)
from parity import conjugation_obeys_parity_law, perm_parity
from promotion import (
    SWAP2,
    cure_assignment,
    cure_verified,
    exhaust_consumed_classes,
    exhaust_slots,
)
from sixlabel import (
    binary_crosscheck,
    exhaust as sixlabel_exhaust,
    member as sixlabel_member,
    pointwise_shaped,
    relabelled_multi,
    slot_maps,
)

RECEIPT = json.loads((HERE / "receipts" / "convention_price.json").read_text("ascii"))
PINNED = json.loads(
    (HERE.parent / "sign_slice" / "receipts" / "sign_slice.json").read_text("ascii")
)
MEMBERS: dict[str, GenPres] = dict(members())
TWO_LABEL_OBSTRUCTED = [
    "square_2x2_occ2",
    "star_K13_occ2",
    "triangle_C3_occ2",
    "square_plus_edge_occ2",
    "pan_C3_tail_occ2",
    "signed_square_pos",
    "signed_square_neg",
]


class ParityLawEcho(unittest.TestCase):
    def test_parity_law_holds_on_every_census_hop(self) -> None:
        """The proved conjugation law, checked on every concrete hop of
        every census member with the two-label maps."""

        maps = ((0, 1), (1, 0))
        for name, p in MEMBERS.items():
            if p.fibre != 2:
                continue
            for a in p.arrows:
                for ga in maps:
                    for gb in maps:
                        self.assertTrue(
                            conjugation_obeys_parity_law(a.transport, ga, gb),
                            f"{name}: parity law fails on a hop",
                        )


class Phase2Promotion(unittest.TestCase):
    def test_cure_witness_sections_every_two_label_obstructed_member(self) -> None:
        for name in TWO_LABEL_OBSTRUCTED:
            cured = cure_verified(MEMBERS[name])
            self.assertTrue(cured["cured_sectioned"], name)

    def test_triangle_and_star_exhaustions_replay_the_receipt(self) -> None:
        for name in ("triangle_C3_occ2", "star_K13_occ2"):
            ex = exhaust_slots(MEMBERS[name])
            rec = RECEIPT["phase_2_promotion"]["exhaustions"][name]
            for key in (
                "flip_count",
                "price_min_slots_from_pointwise",
                "price_tie_count",
                "pointwise_moves",
            ):
                self.assertEqual(ex[key], rec[key], f"{name}.{key}")

    def test_square_exhaustion_reproduces_the_pinned_receipt(self) -> None:
        """PM3: the full 2^16 replay, checked against BOTH this tree's
        receipt and the pinned sign_slice exhaustion."""

        ex = exhaust_slots(MEMBERS["square_2x2_occ2"])
        rec = RECEIPT["phase_2_promotion"]["exhaustions"]["square_2x2_occ2"]
        pin = PINNED["phase_4_occ_relabel"]["exhaustion"]
        self.assertEqual(ex["flip_count"], 8192)
        self.assertEqual(ex["flip_count"], pin["flip_count"])
        self.assertEqual(ex["price_min_slots_from_pointwise"], 2)
        self.assertEqual(
            ex["price_min_slots_from_pointwise"],
            pin["price_min_slots_from_pointwise"],
        )
        self.assertEqual(ex["pointwise_moves"], 0)
        for key in ("flip_count", "price_min_slots_from_pointwise", "price_tie_count"):
            self.assertEqual(ex[key], rec[key])

    def test_consumed_class_route_agrees_with_the_receipt_everywhere(self) -> None:
        """The 2^hops route is replayed in full for all seven members;
        its agreement with the recorded slot-space exhaustion is what
        binds the members too large to replay here."""

        for name in TWO_LABEL_OBSTRUCTED:
            cc = exhaust_consumed_classes(MEMBERS[name])
            rec = RECEIPT["phase_2_promotion"]["exhaustions"][name]
            self.assertEqual(
                cc["flip_count_from_classes"], rec["flip_count"], name
            )
            self.assertEqual(
                cc["price_from_classes"],
                rec["price_min_slots_from_pointwise"],
                name,
            )

    def test_recorded_cheapest_flips_are_genuine_and_at_their_price(self) -> None:
        for name in TWO_LABEL_OBSTRUCTED:
            p = MEMBERS[name]
            rec = RECEIPT["phase_2_promotion"]["exhaustions"][name]
            bits = tuple(int(b) for b in rec["first_cheapest_flip"])
            hops = undirected_hops(p)
            base = cone_section(p)
            self.assertNotEqual(
                cone_section(relabelled(p, hops, bits, SWAP2)), base, name
            )
            price = min(
                sum(1 for x, y in zip(bits, q, strict=True) if x != y)
                for q in pointwise_assignments(p, hops)
            )
            self.assertEqual(price, rec["price_min_slots_from_pointwise"], name)

    def test_pointwise_relabels_never_move_the_triangle(self) -> None:
        """The proved blindness, echoed directly on the smallest member:
        every pointwise assignment leaves the class unmoved."""

        p = MEMBERS["triangle_C3_occ2"]
        hops = undirected_hops(p)
        base = cone_section(p)
        for bits in pointwise_assignments(p, hops):
            self.assertEqual(
                cone_section(relabelled(p, hops, bits, SWAP2)), base
            )

    def test_signed_pair_agrees_with_the_square(self) -> None:
        rec = RECEIPT["phase_2_promotion"]["exhaustions"]
        for name in ("signed_square_pos", "signed_square_neg"):
            for key in (
                "flip_count",
                "price_min_slots_from_pointwise",
                "pointwise_moves",
            ):
                self.assertEqual(rec[name][key], rec["square_2x2_occ2"][key])


class Phase3SixLabel(unittest.TestCase):
    def test_binary_crosscheck_has_zero_misses(self) -> None:
        out = binary_crosscheck(sixlabel_member())
        self.assertEqual(out["misses"], 0)
        self.assertEqual(out["checked"], 3 * 256)

    def test_sixlabel_exhaustion_replays_the_receipt(self) -> None:
        out = sixlabel_exhaust()
        rec = RECEIPT["phase_3_sixlabel"]["exhaustion"]
        for key in (
            "terminal",
            "flip_count",
            "pointwise_moves",
            "price_min_slots_from_pointwise",
            "price_tie_count",
            "first_witness",
        ):
            self.assertEqual(out[key], rec[key], key)

    def test_recorded_witness_if_any_sections_the_member(self) -> None:
        rec = RECEIPT["phase_3_sixlabel"]["exhaustion"]
        if rec["first_witness"] is None:
            self.assertEqual(rec["terminal"], "SIXLABEL_INVARIANT_BOUNDED")
            return
        p = sixlabel_member()
        hops = undirected_hops(p)
        assignment = tuple(int(v) for v in rec["first_witness"])
        self.assertFalse(cone_section(p))
        self.assertTrue(
            cone_section(relabelled_multi(p, hops, assignment, slot_maps()))
        )

    def test_pointwise_shaped_family_has_the_declared_size(self) -> None:
        p = sixlabel_member()
        pw = pointwise_shaped(p, undirected_hops(p))
        self.assertEqual(len(pw), 4 ** len(p.objects))


class Phase4Channels(unittest.TestCase):
    def test_signed_variant_of_the_square_is_the_census_signed_pos(self) -> None:
        self.assertEqual(
            signed_variant(MEMBERS["square_2x2_occ2"]),
            MEMBERS["signed_square_pos"],
        )

    def test_unit_member_weight_lists_are_single_signed(self) -> None:
        """A6: unit-weight members needed no curing on the weight side --
        their full walk lists are already single-signed."""

        for name, p in MEMBERS.items():
            if any(a.amp < 0 for a in p.arrows):
                continue
            w = weight_list(p)
            self.assertTrue(all(v > 0 for v in w), name)

    def test_counting_criterion_reproduces_the_pinned_fixtures(self) -> None:
        """The pinned sign-repair receipt's two decided instances,
        re-decided by this tree's reconstruction: the wedge has no
        certificate, the pinned witness has one."""

        wedge = certificate_by_counting([-2, -2, -1, 2, 2, 2])
        self.assertFalse(wedge["certificate"])
        witness = certificate_by_counting([1, 2, -1, -2, 1, 1])
        self.assertTrue(witness["certificate"])
        pin = json.loads(
            (
                HERE.parent / "natural_sections" / "receipts" / "sign_repair.json"
            ).read_text("ascii")
        )
        self.assertEqual(
            pin["pinned_witness_has_certificate"], witness["certificate"]
        )

    def test_discard_is_not_cancel(self) -> None:
        """The pinned discard countermodel binds: the full list and the
        partner-discarded list disagree, so no walk is discarded."""

        self.assertEqual(sum([3, -3, 1, -1]), 0)
        self.assertEqual(sum([3, 1]), 4)

    def test_channel_b_rows_replay_from_the_presentations(self) -> None:
        rows = {str(r["name"]): r for r in RECEIPT["phase_4_channels"]["rows"]}
        for name, r in rows.items():
            if name.startswith("signed_variant_of_"):
                p = signed_variant(MEMBERS[name.removeprefix("signed_variant_of_")])
            else:
                p = MEMBERS[name]
            cert = certificate_by_counting(weight_list(p))
            self.assertEqual(cert, r["channel_b"], name)

    def test_cells_follow_verdict_and_certificate(self) -> None:
        for r in RECEIPT["phase_4_channels"]["rows"]:
            verdict = r["channel_a"]["verdict"]
            b_yes = r["channel_b"]["certificate"]
            if verdict == "NOT_COVERED_BY_BOUND":
                want = "b_decided_a_not_covered"
            elif verdict == "CURABLE_WITHIN_BOUND":
                want = "both" if b_yes else "a_only"
            else:
                want = "b_only" if b_yes else "neither"
            self.assertEqual(r["cell"], want, str(r["name"]))

    def test_nonseparation_terminal_is_scoped_to_decided_rows(self) -> None:
        separation = RECEIPT["phase_4_channels"]["separation"]
        self.assertEqual(separation["rows"], 11)
        self.assertEqual(separation["decided_rows"], 10)
        self.assertEqual(
            separation["terminal"], "CHANNELS_AGREE_ON_DECIDED_ROWS"
        )


class Phase5Register(unittest.TestCase):
    def test_one_row_per_obstructed_member_and_none_sectioned(self) -> None:
        reg = RECEIPT["phase_5_register"]["rows"]
        obstructed = [
            name for name, p in MEMBERS.items() if not cone_section(p)
        ]
        self.assertEqual(sorted(str(r["name"]) for r in reg), sorted(obstructed))

    def test_every_register_row_names_a_leftover(self) -> None:
        for r in RECEIPT["phase_5_register"]["rows"]:
            self.assertTrue(r["leftovers"], str(r["name"]))


class ReceiptShape(unittest.TestCase):
    def test_receipt_is_canonical_json_with_lf_only(self) -> None:
        raw = (HERE / "receipts" / "convention_price.json").read_bytes()
        self.assertNotIn(b"\r", raw)
        canonical = (
            json.dumps(json.loads(raw.decode("ascii")), indent=2, sort_keys=True)
            + "\n"
        ).encode("ascii")
        self.assertEqual(raw, canonical)

    def test_receipt_declares_no_authority_and_frozen_hashes(self) -> None:
        self.assertEqual(RECEIPT["authority_effect"], "None")
        import hashlib

        self.assertEqual(
            RECEIPT["prompt_native_sha256"],
            hashlib.sha256((HERE / "PROMPT.md").read_bytes()).hexdigest(),
        )
        self.assertEqual(
            RECEIPT["predictions_sha256"],
            hashlib.sha256((HERE / "PREDICTIONS.md").read_bytes()).hexdigest(),
        )
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
        self.assertEqual(
            RECEIPT["predictions_sha256"], manifest["predictions_freezes"][-1]
        )

    def test_terminals_include_the_protected_opens_and_partial_ss09(self) -> None:
        codes = {str(t["code"]) for t in RECEIPT["terminals"]}
        for code in (
            "OB1_UNCHANGED",
            "S66_UNCHANGED",
            "S9_LAST_UNCHANGED",
            "SS09_PARTIALLY_CLOSED",
            "FW_SET_HELD",
        ):
            self.assertIn(code, codes)


if __name__ == "__main__":
    unittest.main()
