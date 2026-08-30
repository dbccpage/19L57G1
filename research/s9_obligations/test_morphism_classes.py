"""Tests for P2 (S9.2): the menu, the candidates, the D2_initial_pointed
cell, witnesses re-checked by hand, tie retention, the shape computation on
synthetic sets, the fast path against the slow path, the committed receipt
against a fresh render, and the vocabulary firewall over P2's own files.

Everything here is finite computation at the declared bounds; a green run
is not a discharged obligation (PROMPT.md house rule).
"""

from __future__ import annotations

import contextlib
import io
import json
import re
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any

import common  # first: disables bytecode writing before a sealed module loads
from derivation.primdiff import (
    D2,
    D2_REV,
    S2,
    Pointed,
    all_functions_between,
    enumerate_pointed,
    pointed_isomorphic,
    preserves_rel,
)

import morphism_classes as mc
import run_morphism_classes as runner

RECEIPT_PATH = common.TREE / "receipts" / runner.RECEIPT_NAME
FINDINGS_PATH = common.TREE / "P2_FINDINGS.md"
P2_FILES = (
    common.TREE / "morphism_classes.py",
    common.TREE / "run_morphism_classes.py",
    common.TREE / "test_morphism_classes.py",
    RECEIPT_PATH,
    FINDINGS_PATH,
)

# PROMPT.md "Legal terminals".
LEGAL_TERMINALS = frozenset(
    {
        "S9_1_LATTICE_COMPLETE",
        "S9_1_LATTICE_BOUNDED",
        "S9_1_TRANSFER_CHARACTERIZED",
        "S9_1_TRANSFER_OPEN",
        "F3_SUPPORTED_BOUNDED",
        "F3_REFUTED",
        "F3_UNTESTED",
        "EQ_FRAGMENT_SEPARATED",
        "S9_2_CLASSES_CLASSIFIED",
        "S9_2_CLASSES_BOUNDED",
        "S9_2_INTERVAL_SHAPE",
        "S9_2_INCOMPARABLE_CLASSES",
        "TIES_RETAINED",
        "S9_3_WITNESS_OBSERVABLE",
        "S9_3_WITNESS_INVISIBLE",
        "S9_3_ADMISSION_NAMED",
        "LEAN_CARRIED",
        "LEAN_NOT_CARRIED",
        "PYTHON_ONLY_SCOPE_DECLARED",
        "MANUAL_RECEIPT_DECLARED",
        "OB1_UNCHANGED",
        "S66_UNCHANGED",
        "S9_LAST_UNCHANGED",
        "PROPOSED_TEXT_WRITTEN",
        "REFUSED",
    }
)
# Terminals P2 must not emit itself (step 19: the Lean stage's).
NOT_P2_TERMINALS = frozenset({"S9_2_CLASSES_CLASSIFIED", "LEAN_CARRIED", "LEAN_NOT_CARRIED"})

PRIMARY, SECONDARY = mc.OBJECT_CLASSES


def candidates_for(object_class: mc.ObjectClass) -> list[mc.Candidate]:
    return mc.quotient_candidates(mc.raw_candidates(object_class.irreflexivity_imposed))


def pointed_from_json(blob: dict[str, Any]) -> Pointed:
    return Pointed(
        int(blob["n"]),
        frozenset((int(x), int(y)) for x, y in blob["rel"]),
        int(blob["a"]),
        int(blob["b"]),
    )


def load_receipt() -> dict[str, Any]:
    payload: Any = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def rows_by_cell(receipt: dict[str, Any]) -> dict[tuple[str, str, str], dict[str, Any]]:
    out: dict[tuple[str, str, str], dict[str, Any]] = {}
    for key in ("primary", "secondary"):
        for row in receipt["tables"][key]["rows"]:
            out[(key, row["class"], row["object"])] = row
    return out


# Witness objects named in the findings, written out here independently of
# the module's aliases so the recount below does not borrow its labels.
SELF1_JSON: dict[str, Any] = {"n": 1, "rel": [[0, 0]], "a": 0, "b": 0}
D2_JSON: dict[str, Any] = {"n": 2, "rel": [[0, 1]], "a": 0, "b": 1}
S2_JSON: dict[str, Any] = {"n": 2, "rel": [[0, 1], [1, 0]], "a": 0, "b": 1}
THREE_JSON: dict[str, Any] = {"n": 3, "rel": [[0, 1]], "a": 0, "b": 1}

# The protected opens (PROMPT.md step 36) and the verbs the findings may
# not attach to them, in any inflection, in either word order.
PROTECTED = r"(?:OB-1|S6\.6|(?:the\s+)?inscription\s+bridge|S9\s+last\s+bullet)"
VERBS = r"(?:clos(?:e|es|ed|ing)|narrow(?:s|ed|ing)?|pric(?:e|es|ed|ing))"
CLAIM_PATTERNS = (
    re.compile(PROTECTED + r"\s+(?:is|was|are|were|has\s+been|have\s+been|now)?\s*" + VERBS, re.I),
    re.compile(VERBS + r"\s+(?:the\s+)?" + PROTECTED, re.I),
)
# The one sentence the findings must carry, which mentions the verbs only
# under "does not claim".  Compared after whitespace is flattened, so a
# line wrap cannot hide or break it.
DISCLAIMER = (
    "It does not claim OB-1, S6.6, or the S9 last bullet (the inscription bridge) "
    "closed, narrowed, or priced"
)


def flatten(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def protected_open_claims(text: str) -> list[str]:
    """Every phrase of ``text`` that asserts a protected open closed,
    narrowed, or priced.  The disclaimer sentence and other explicit
    denials are removed first, since they name the verbs only to deny them."""

    stripped = flatten(text).replace(DISCLAIMER, "")
    stripped = re.sub(r"does not (?:claim|close|narrow|price)[^.]*", "", stripped)
    stripped = re.sub(r"not (?:closed|narrowed|priced|to close)[^.]*", "", stripped)
    hits: list[str] = []
    for pattern in CLAIM_PATTERNS:
        hits.extend(match.group(0) for match in pattern.finditer(stripped))
    return hits


def conditions(row: dict[str, Any]) -> set[str]:
    return set(row["class_conditions"])


# The witness groups, as row predicates written here rather than borrowed
# from the module, so the recount is independent of the producer.
ROW_PREDICATES: dict[str, dict[str, Callable[[dict[str, Any]], bool]]] = {
    "primary": {
        "I_classes": lambda r: "I" in conditions(r),
        "S_without_I_classes": lambda r: "S" in conditions(r) and "I" not in conditions(r),
        "no_P_I_S_classes": lambda r: not conditions(r) & {"P", "I", "S"},
        "P_class_initial": lambda r: r["class"] == "{P}" and bool(r["initial"]),
        "P_class_non_initial": lambda r: r["class"] == "{P}" and not r["initial"],
        "P_E_class": lambda r: r["class"] == "{P,E}",
        "P_NE_class": lambda r: r["class"] == "{P,NE}",
        "P_E_NE_class": lambda r: r["class"] == "{P,E,NE}",
    },
    "secondary": {
        "S_classes": lambda r: "S" in conditions(r),
        "no_P_no_S_classes": lambda r: not conditions(r) & {"P", "S"},
        "P_without_S_initial": lambda r: "P" in conditions(r)
        and "S" not in conditions(r)
        and bool(r["initial"]),
        "P_without_S_non_initial": lambda r: "P" in conditions(r)
        and "S" not in conditions(r)
        and not r["initial"],
    },
}


class MenuTests(unittest.TestCase):
    def test_menu_size_and_class_count(self) -> None:
        self.assertEqual(mc.MENU_NAMES, ("P", "E", "NE", "I", "S"))
        self.assertEqual(mc.MENU_SIZE, 5)
        self.assertEqual(mc.CLASS_COUNT, 32)
        self.assertLessEqual(mc.MENU_SIZE, mc.MENU_SIZE_BOUND)
        self.assertLessEqual(mc.CLASS_COUNT, mc.CLASS_COUNT_BOUND)
        names = [mc.class_name(c) for c in mc.ALL_CLASS_MASKS]
        self.assertEqual(len(set(names)), 32)
        self.assertEqual(mc.class_name(0), "{}")
        self.assertEqual(mc.class_name(mc.class_mask(["E", "P"])), "{P,E}")
        self.assertEqual(mc.class_members(mc.class_mask(["S", "NE"])), ("NE", "S"))
        self.assertEqual(mc.class_name(mc.CLASS_COUNT - 1), "{P,E,NE,I,S}")

    def test_ne_definition_states_its_decidability_scope(self) -> None:
        """The contrapositive form of NE is the same condition only over
        decidable relations; the menu says so where it states the form."""

        definition = dict(mc.MENU)["NE"]
        self.assertIn("not r x y -> not r' (f x) (f y)", definition)
        self.assertIn("decidable", definition)
        self.assertNotIn("equivalent", definition)
        receipt = load_receipt()
        self.assertEqual(
            [item["definition"] for item in receipt["menu"] if item["name"] == "NE"],
            [definition],
        )


class CandidateTests(unittest.TestCase):
    def test_primary_candidates_are_enumerated_and_quotiented(self) -> None:
        raw = mc.raw_candidates(False)
        expected = [s for s in enumerate_pointed(2) if (s.a, s.b) in s.rel]
        self.assertEqual(raw, expected)
        self.assertEqual(len(raw), 32)
        self.assertTrue(any(s.a == s.b for s in raw))
        classes = mc.quotient_candidates(raw)
        self.assertEqual(len(classes), 16)
        for candidate in classes:
            self.assertEqual(candidate.members[0], candidate.representative)
            for member in candidate.members:
                self.assertTrue(pointed_isomorphic(candidate.representative, member))
        representatives = [c.representative for c in classes]
        for i, s in enumerate(representatives):
            for t in representatives[i + 1 :]:
                self.assertFalse(pointed_isomorphic(s, t))
        self.assertEqual(sum(len(c.members) for c in classes), 32)
        self.assertIn(D2, representatives)
        self.assertIn(S2, representatives)
        self.assertIn(mc.FULL2, representatives)
        # D2_REV asserts (0, 1) but its relation is {(1, 0)}: not an object.
        self.assertFalse(mc.is_object(D2_REV, False))
        self.assertNotIn(D2_REV, raw)
        # The reversed orientation WITH its pair asserted is D2 up to pointed iso.
        reversed_asserted = Pointed(2, frozenset({(1, 0)}), 1, 0)
        d2_class = next(c for c in classes if c.representative == D2)
        self.assertIn(reversed_asserted, d2_class.members)
        self.assertEqual(mc.candidate_name(D2), "O01_0100")
        self.assertEqual(mc.candidate_name(S2), "O01_0110")
        self.assertEqual(mc.candidate_name(mc.FULL2), "O01_1111")

    def test_secondary_candidates_exclude_the_diagonal_pair(self) -> None:
        raw = mc.raw_candidates(True)
        self.assertEqual(len(raw), 4)
        self.assertTrue(all(s.a != s.b for s in raw))
        self.assertTrue(all(x != y for s in raw for (x, y) in s.rel))
        classes = mc.quotient_candidates(raw)
        self.assertEqual([c.representative for c in classes], [D2, S2])
        self.assertEqual([c.alias for c in classes], ["D2", "S2"])


class SweepTests(unittest.TestCase):
    primary: mc.Sweep
    secondary: mc.Sweep

    @classmethod
    def setUpClass(cls) -> None:
        cls.primary = mc.sweep(PRIMARY, candidates_for(PRIMARY), mc.REQUIRED_N)
        cls.secondary = mc.sweep(SECONDARY, candidates_for(SECONDARY), mc.REQUIRED_N)

    def cell(self, result: mc.Sweep, cls: list[str], obj: Pointed) -> mc.Cell:
        ci = next(i for i, c in enumerate(result.candidates) if c.representative == obj)
        return result.cell(ci, mc.class_mask(cls))

    def test_object_counts_at_required_carrier(self) -> None:
        self.assertEqual(self.primary.objects_by_carrier, {1: 1, 2: 32, 3: 2304})
        self.assertEqual(self.secondary.objects_by_carrier, {1: 0, 2: 4, 3: 192})
        # 2337 is the sealed artifact's witnessed-structure count at carrier <= 3.
        sealed: Any = json.loads(
            (common.REPO / "artifacts" / "primdiff.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            sum(self.primary.objects_by_carrier.values()),
            sealed["two_element"]["witnessed_structures_checked"],
        )

    def test_fast_path_matches_direct_enumeration(self) -> None:
        for result, object_class in ((self.primary, PRIMARY), (self.secondary, SECONDARY)):
            direct = mc.sweep_direct(object_class, result.candidates, mc.REQUIRED_N)
            self.assertEqual(direct.objects_by_carrier, result.objects_by_carrier)
            self.assertEqual(direct.cells, result.cells)

    def test_d2_initial_pointed_cell_agrees_with_the_theorem(self) -> None:
        """Step 14.  The theorem: every object of the primary class (no
        irreflexivity, a = b allowed) has exactly one point-preserving map
        from D2, and that map preserves the oriented edge."""

        direct = mc.d2_pointed_maps_direct(mc.REQUIRED_N)
        self.assertEqual(direct["objects_checked"], 2337)
        self.assertEqual(direct["objects_with_exactly_one_point_preserving_map"], 2337)
        self.assertEqual(direct["objects_where_that_map_preserves_the_edge"], 2337)
        self.assertTrue(direct["agrees_with_theorem"])
        # The same quantification, written out without the module's helpers.
        for n in range(1, mc.REQUIRED_N + 1):
            for y in enumerate_pointed(n):
                if (y.a, y.b) not in y.rel:
                    continue
                point_maps = [f for f in all_functions_between(2, n) if f[0] == y.a and f[1] == y.b]
                self.assertEqual(len(point_maps), 1)
                self.assertTrue(preserves_rel(point_maps[0], D2, y))
        # In the table: D2 initial for {P} (uniqueness class) and {P,E} (existence class).
        self.assertTrue(self.cell(self.primary, ["P"], D2).initial)
        self.assertTrue(self.cell(self.primary, ["P", "E"], D2).initial)
        record = mc.d2_cell_record(self.primary)
        self.assertEqual(record["in_menu_terms"]["uniqueness_class"], "{P}")  # type: ignore[index]
        self.assertEqual(record["in_menu_terms"]["existence_class"], "{P,E}")  # type: ignore[index]
        self.assertTrue(record["model_agrees_at_bound"])
        # Negative control: the theorem says nothing about {P,NE}, and D2 is
        # not initial there (existence fails at the one-point self-difference).
        control = self.cell(self.primary, ["P", "NE"], D2)
        self.assertFalse(control.initial)
        self.assertEqual(control.existence_failure, Pointed(1, frozenset({(0, 0)}), 0, 0))

    def test_existence_failures_carry_witnesses_rechecked_by_hand(self) -> None:
        # primary, {I}, D2: no injective map into the one-point self-difference.
        cell = self.cell(self.primary, ["I"], D2)
        witness = cell.existence_failure
        self.assertEqual(witness, Pointed(1, frozenset({(0, 0)}), 0, 0))
        functions = all_functions_between(2, 1)
        self.assertEqual(functions, [(0, 0)])
        self.assertEqual([f for f in functions if len(set(f)) == 2], [])
        # secondary, {P,E}, S2: the point-preserving map S2 -> D2 sends the
        # reverse edge (1, 0) to (1, 0), which D2 lacks.
        cell = self.cell(self.secondary, ["P", "E"], S2)
        self.assertEqual(cell.existence_failure, D2)
        by_hand = [
            f
            for f in all_functions_between(2, 2)
            if f[0] == D2.a and f[1] == D2.b and all((f[x], f[y]) in D2.rel for (x, y) in S2.rel)
        ]
        self.assertEqual(by_hand, [])
        self.assertEqual([f for f in all_functions_between(2, 2) if f[0] == 0 and f[1] == 1], [(0, 1)])
        self.assertNotIn((1, 0), D2.rel)
        # secondary, {P,NE}, D2: the point-preserving map D2 -> S2 sends the
        # non-edge (1, 0) onto the edge (1, 0) of S2.
        cell = self.cell(self.secondary, ["P", "NE"], D2)
        self.assertEqual(cell.existence_failure, S2)
        self.assertNotIn((1, 0), D2.rel)
        self.assertIn((1, 0), S2.rel)

    def test_uniqueness_failures_carry_two_distinct_morphisms_rechecked_by_hand(self) -> None:
        # primary, {}, D2: the first two-element object has four functions.
        cell = self.cell(self.primary, [], D2)
        self.assertIsNotNone(cell.uniqueness_failure)
        assert cell.uniqueness_failure is not None
        witness, f1, f2 = cell.uniqueness_failure
        self.assertEqual(witness, Pointed(2, frozenset({(0, 0)}), 0, 0))
        self.assertNotEqual(f1, f2)
        self.assertEqual((f1, f2), ((0, 0), (0, 1)))
        self.assertEqual(len(all_functions_between(2, 2)), 4)
        # secondary, {E}, D2: both the identity and the swap carry D2's edge
        # into S2.
        cell = self.cell(self.secondary, ["E"], D2)
        assert cell.uniqueness_failure is not None
        witness, f1, f2 = cell.uniqueness_failure
        self.assertEqual(witness, S2)
        self.assertEqual((f1, f2), ((0, 1), (1, 0)))
        for f in (f1, f2):
            self.assertTrue(all((f[x], f[y]) in S2.rel for (x, y) in D2.rel))
        # No cell is "not initial" without a witness.
        for cell in self.primary.cells + self.secondary.cells:
            if not cell.initial:
                self.assertTrue(
                    cell.existence_failure is not None or cell.uniqueness_failure is not None
                )

    def test_tie_retention(self) -> None:
        """Step 17.  D2 and S2 are both initial for {P} in the irreflexive
        class (the way S7 keeps both); in the primary class every a != b
        candidate is initial for {P}."""

        self.assertFalse(pointed_isomorphic(D2, S2))
        secondary = mc.ties(self.secondary)
        per_class = secondary["per_class"]
        assert isinstance(per_class, dict)
        self.assertEqual(per_class["{P}"], {"count": 2, "retained": ["O01_0100", "O01_0110"]})
        self.assertEqual(per_class["{P,I}"], {"count": 2, "retained": ["O01_0100", "O01_0110"]})
        self.assertEqual(per_class["{P,E}"], {"count": 1, "retained": ["O01_0100"]})
        self.assertEqual(per_class["{P,NE}"], {"count": 1, "retained": ["O01_0110"]})
        self.assertEqual(secondary["classes_with_ties"], ["{P}", "{P,I}"])
        self.assertEqual(secondary["max_tie"], 2)
        primary = mc.ties(self.primary)
        per_class = primary["per_class"]
        assert isinstance(per_class, dict)
        self.assertEqual(per_class["{P}"]["count"], 8)
        retained = per_class["{P}"]["retained"]
        self.assertEqual(len(retained), 8)
        for name in retained:
            candidate = next(c for c in self.primary.candidates if c.name == name)
            self.assertNotEqual(candidate.representative.a, candidate.representative.b)
        self.assertEqual(per_class["{P,E}"], {"count": 1, "retained": ["O01_0100"]})
        self.assertEqual(per_class["{P,NE}"], {"count": 1, "retained": ["O01_1111"]})
        self.assertEqual(primary["classes_with_ties"], ["{P}"])

    def test_shape_is_computed_from_the_table(self) -> None:
        primary = mc.shape(mc.admitting_masks(self.primary))
        self.assertEqual(primary["admitting_classes"], ["{P}", "{P,E}", "{P,NE}"])
        self.assertEqual(primary["minimal"], ["{P}"])
        self.assertEqual(primary["maximal"], ["{P,E}", "{P,NE}"])
        self.assertFalse(primary["is_interval"])
        self.assertEqual(primary["incomparable_pair"], ["{P,E}", "{P,NE}"])
        self.assertEqual(primary["incomparable_pair_source"], "maximal")
        self.assertEqual(primary["gap"], "{P,E,NE}")
        self.assertEqual(primary["terminal"], "S9_2_INCOMPARABLE_CLASSES")
        secondary = mc.shape(mc.admitting_masks(self.secondary))
        self.assertEqual(
            secondary["admitting_classes"],
            ["{P}", "{P,E}", "{P,NE}", "{P,I}", "{P,E,I}", "{P,NE,I}"],
        )
        self.assertEqual(secondary["minimal"], ["{P}"])
        self.assertEqual(secondary["maximal"], ["{P,E,I}", "{P,NE,I}"])
        self.assertFalse(secondary["is_interval"])
        self.assertEqual(secondary["incomparable_pair"], ["{P,E,I}", "{P,NE,I}"])
        self.assertEqual(secondary["incomparable_pair_source"], "maximal")
        # The admitting set is NOT a down-set of the class lattice: classes
        # below a maximal class that lack P do not admit.
        for result, sh in ((self.primary, primary), (self.secondary, secondary)):
            admitting = set(mc.admitting_masks(result))
            maximal_names = sh["maximal"]
            assert isinstance(maximal_names, list)
            maximal = [mc.class_mask(str(c).strip("{}").split(",")) for c in maximal_names]
            below = {c for c in mc.ALL_CLASS_MASKS if any(c & ~m == 0 for m in maximal)}
            self.assertTrue(below - admitting)
            self.assertIn(0, below - admitting)
            self.assertTrue(all(c & mc.BIT["P"] for c in admitting))
            # What it IS: every class containing P and contained in a maximal class.
            self.assertEqual(admitting, {c for c in below if c & mc.BIT["P"]})

    def test_no_p_class_admits_and_how_each_such_cell_fails(self) -> None:
        """The reason is read off the cells, never assumed: a class without P
        admits nothing at N = 3, but not because two maps always exist --
        some such cells carry only an existence witness."""

        for result, expected in (
            (self.primary, (256, 220, 36, 237)),
            (self.secondary, (32, 28, 4, 23)),
        ):
            cells = [
                result.cell(ci, cmask)
                for cmask in mc.ALL_CLASS_MASKS
                if not cmask & mc.BIT["P"]
                for ci in range(len(result.candidates))
            ]
            self.assertEqual(len(cells), expected[0])
            self.assertFalse(any(cell.initial for cell in cells))
            self.assertEqual(sum(1 for c in cells if c.uniqueness_failure), expected[1])
            only_existence = [c for c in cells if c.uniqueness_failure is None]
            self.assertEqual(len(only_existence), expected[2])
            self.assertEqual(sum(1 for c in cells if c.existence_failure), expected[3])
            for cell in only_existence:
                self.assertIsNotNone(cell.existence_failure)
                self.assertTrue(cell.cmask & mc.BIT["NE"] and cell.cmask & mc.BIT["S"])

    def test_table_at_required_carrier_equals_the_committed_table(self) -> None:
        """bounds_reached.*.table_identical_at_required_carrier, re-derived:
        the N = 3 sweep and the committed N = 4 rows agree cell for cell."""

        receipt = load_receipt()
        rows = rows_by_cell(receipt)
        for key, result in (("primary", self.primary), ("secondary", self.secondary)):
            self.assertTrue(receipt["bounds_reached"][key]["table_identical_at_required_carrier"])
            self.assertEqual(receipt["bounds_reached"][key]["required_carrier"], mc.REQUIRED_N)
            for cmask in mc.ALL_CLASS_MASKS:
                for ci, candidate in enumerate(result.candidates):
                    cell = result.cell(ci, cmask)
                    row = rows[(key, mc.class_name(cmask), candidate.name)]
                    self.assertEqual(row["initial"], cell.initial)
                    existence, uniqueness = mc.witness_json(cell)
                    self.assertEqual(row["existence_failure"], existence)
                    self.assertEqual(row["uniqueness_failure"], uniqueness)

    def test_per_class_right_hand_sides_match_the_table_at_the_candidates(self) -> None:
        """The right-hand sides of the four per-class Lean verdicts
        (`initial_P_iff`: a0 != b0; `initial_P_E_iff`: a0 != b0 and no pair
        beyond (a0, b0); `initial_P_NE_iff`, for a decidable candidate, which
        every finite one is: a0 != b0 and every pair; `not_initial_P_E_NE`:
        never), evaluated here at every primary candidate, equal the table's
        verdict in the 64 primary cells of {P}, {P,E}, {P,NE}, {P,E,NE} --
        at the required carrier in-process and at the attempted carrier in
        the committed receipt.  Finite computation, bounded by N = 4; it
        replaces the finite inspection P2_FINDINGS.md section 11 recorded
        with a test, and says nothing about a candidate outside the 16
        classes."""

        pairs = ((0, 0), (0, 1), (1, 0), (1, 1))

        def rhs(cls: str, s: Pointed) -> bool:
            distinct = s.a != s.b
            if cls == "{P}":
                return distinct
            if cls == "{P,E}":
                return distinct and all((x, y) == (s.a, s.b) for (x, y) in s.rel)
            if cls == "{P,NE}":
                return distinct and all(pair in s.rel for pair in pairs)
            if cls == "{P,E,NE}":
                return False
            raise AssertionError(cls)

        receipt = load_receipt()
        rows = rows_by_cell(receipt)
        self.assertEqual(len(self.primary.candidates), 16)
        checked = 0
        for cls in ("{P}", "{P,E}", "{P,NE}", "{P,E,NE}"):
            cmask = mc.class_mask(cls.strip("{}").split(","))
            for ci, candidate in enumerate(self.primary.candidates):
                expected = rhs(cls, candidate.representative)
                # The right-hand side is a property of the pointed relation
                # that pointed isomorphism preserves: constant on the class.
                for member in candidate.members:
                    self.assertEqual(rhs(cls, member), expected, (cls, candidate.name))
                self.assertEqual(self.primary.cell(ci, cmask).initial, expected, (cls, candidate.name))
                row = rows[("primary", cls, candidate.name)]
                self.assertEqual(row["initial"], expected, (cls, candidate.name))
                self.assertEqual(row["bound_reached"], mc.ATTEMPTED_N)
                checked += 1
        self.assertEqual(checked, 64)
        # The right-hand sides are met by the candidates the theorems name,
        # and by no other: eight for {P}, D2 alone for {P,E}, FULL2 alone for
        # {P,NE}, none for {P,E,NE} (receipt `initial_objects_by_class`).
        by_class = receipt["initial_objects_by_class"]["primary"]["by_class"]
        reps = [(c.name, c.representative) for c in self.primary.candidates]
        self.assertEqual(len([n for n, s in reps if rhs("{P}", s)]), 8)
        self.assertEqual([n for n, s in reps if rhs("{P,E}", s)], ["O01_0100"])
        self.assertEqual([n for n, s in reps if rhs("{P,NE}", s)], ["O01_1111"])
        self.assertEqual([n for n, s in reps if rhs("{P,E,NE}", s)], [])
        for cls in ("{P}", "{P,E}", "{P,NE}", "{P,E,NE}"):
            self.assertEqual(by_class[cls], [n for n, s in reps if rhs(cls, s)], cls)

    def test_i_is_extensionally_redundant_under_p_in_the_irreflexive_class(self) -> None:
        """Observed, not assumed: over irreflexive objects a != b holds, so a
        point-preserving map from a two-element candidate is injective."""

        for cmask in mc.ALL_CLASS_MASKS:
            if cmask & mc.BIT["P"] and not cmask & mc.BIT["I"]:
                for ci in range(len(self.secondary.candidates)):
                    with_i = self.secondary.cell(ci, cmask | mc.BIT["I"])
                    without_i = self.secondary.cell(ci, cmask)
                    self.assertEqual(with_i.initial, without_i.initial)


class ShapeSyntheticTests(unittest.TestCase):
    def test_incomparable_maxima_are_not_an_interval(self) -> None:
        masks = [mc.class_mask(c) for c in (["P"], ["P", "E"], ["P", "NE"])]
        result = mc.shape(masks)
        self.assertFalse(result["is_interval"])
        self.assertEqual(result["incomparable_pair"], ["{P,E}", "{P,NE}"])
        self.assertIsNone(result["lower"])
        self.assertEqual(result["terminal"], "S9_2_INCOMPARABLE_CLASSES")

    def test_gap_defeats_the_interval_check_even_with_unique_endpoints(self) -> None:
        masks = [mc.class_mask(c) for c in (["P"], ["P", "E", "I"])]
        result = mc.shape(masks)
        self.assertEqual(result["minimal"], ["{P}"])
        self.assertEqual(result["maximal"], ["{P,E,I}"])
        self.assertFalse(result["is_interval"])
        self.assertIsNone(result["incomparable_pair"])
        self.assertEqual(result["gap"], "{P,E}")
        self.assertEqual(result["terminal"], "S9_2_INCOMPARABLE_CLASSES")

    def test_a_full_interval_passes(self) -> None:
        masks = [mc.class_mask(c) for c in ([], ["P"], ["E"], ["P", "E"])]
        result = mc.shape(masks)
        self.assertTrue(result["is_interval"])
        self.assertEqual(result["lower"], "{}")
        self.assertEqual(result["upper"], "{P,E}")
        self.assertEqual(result["terminal"], "S9_2_INTERVAL_SHAPE")
        single = mc.shape([mc.class_mask(["P"])])
        self.assertTrue(single["is_interval"])
        self.assertEqual((single["lower"], single["upper"]), ("{P}", "{P}"))

    def test_empty_admitting_set_emits_no_shape_terminal(self) -> None:
        result = mc.shape([])
        self.assertFalse(result["is_interval"])
        self.assertIsNone(result["terminal"])
        self.assertEqual(result["admitting_count"], 0)

    def test_incomparable_non_extremal_members_are_not_the_reason(self) -> None:
        """{P} and {E} are incomparable, but with unique extremes {} and
        {P,E,NE} the set fails only by its gaps; the reason must say so and
        must not print the non-extremal pair."""

        masks = [mc.class_mask(c) for c in ([], ["P"], ["E"], ["P", "E", "NE"])]
        result = mc.shape(masks)
        self.assertFalse(result["is_interval"])
        self.assertEqual(result["minimal"], ["{}"])
        self.assertEqual(result["maximal"], ["{P,E,NE}"])
        self.assertIsNone(result["incomparable_pair"])
        self.assertIsNone(result["incomparable_pair_source"])
        self.assertEqual(result["gap"], "{P,E}")
        self.assertIn("{P,E}", str(result["reason"]))
        self.assertNotIn("incomparable", str(result["reason"]))
        # The same members with the gaps filled in ARE an interval, which is
        # why the non-extremal pair could never have been a valid reason.
        filled = mc.shape([c for c in mc.ALL_CLASS_MASKS if c & ~mc.class_mask(["P", "E", "NE"]) == 0])
        self.assertTrue(filled["is_interval"])
        self.assertEqual((filled["lower"], filled["upper"]), ("{}", "{P,E,NE}"))

    def test_incomparable_minima_are_named_as_such(self) -> None:
        masks = [mc.class_mask(c) for c in (["P"], ["E"], ["P", "E"])]
        result = mc.shape(masks)
        self.assertFalse(result["is_interval"])
        self.assertEqual(result["incomparable_pair"], ["{P}", "{E}"])
        self.assertEqual(result["incomparable_pair_source"], "minimal")
        self.assertIn("minimal", str(result["reason"]))


class ReceiptTests(unittest.TestCase):
    def test_refused_carrier_is_refused_by_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "N = 5 is refused by name"):
            mc.compute(mc.REFUSED_N)

    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        """Step 33 at the attempted carrier: two renders into two directories
        agree byte for byte, and the committed receipt is that render."""

        with tempfile.TemporaryDirectory(dir=common.TREE) as scratch:
            with contextlib.redirect_stdout(io.StringIO()) as printed:
                first = runner.main(["--out", str(Path(scratch) / "a")])
                second = runner.main(["--out", str(Path(scratch) / "b")])
            self.assertEqual((first, second), (0, 0))
            self.assertIn("menu_size: 5", printed.getvalue())
            one = (Path(scratch) / "a" / runner.RECEIPT_NAME).read_bytes()
            two = (Path(scratch) / "b" / runner.RECEIPT_NAME).read_bytes()
        self.assertEqual(one, two)
        self.assertNotIn(b"\r", one)
        self.assertEqual(one, RECEIPT_PATH.read_bytes())
        self.assertEqual(one, common.receipt_bytes(json.loads(one)))

    def test_committed_receipt_headline_keys(self) -> None:
        receipt = load_receipt()
        self.assertEqual(receipt["header"], common.receipt_header())
        self.assertEqual(receipt["menu_size"], 5)
        self.assertEqual(receipt["class_count"], 32)
        self.assertEqual(len(receipt["classes"]), 32)
        bounds = receipt["bounds_reached"]
        self.assertEqual(bounds["primary"]["carrier_reached"], mc.ATTEMPTED_N)
        self.assertEqual(bounds["secondary"]["carrier_reached"], mc.ATTEMPTED_N)
        self.assertTrue(bounds["primary"]["attempted_carrier_completed"])
        self.assertEqual(
            bounds["primary"]["objects_checked_by_carrier"],
            {"1": 1, "2": 32, "3": 2304, "4": 524288},
        )
        self.assertEqual(
            bounds["secondary"]["objects_checked_by_carrier"],
            {"1": 0, "2": 4, "3": 192, "4": 24576},
        )
        self.assertEqual(receipt["tables"]["primary"]["row_count"], 512)
        self.assertEqual(receipt["tables"]["secondary"]["row_count"], 64)
        self.assertEqual(receipt["cell_summary"]["primary"]["initial"], 10)
        self.assertEqual(receipt["cell_summary"]["secondary"]["initial"], 8)
        self.assertTrue(receipt["d2_initial_pointed_cell"]["model_agrees_at_bound"])
        self.assertTrue(receipt["python_only_scope"]["reproduces_s9_fifth_bullet"])
        self.assertFalse(receipt["lean"]["carried_by_this_part"])
        self.assertEqual(receipt["declared_bounds"]["object_carrier"]["refused_by_name"], 5)
        self.assertEqual(
            receipt["initial_objects_by_class"]["primary"]["by_class"]["{P,E}"], ["O01_0100"]
        )

    def test_every_bound_dependent_result_object_carries_bounded_and_bound_reached(self) -> None:
        """PREFLIGHT.md step 4 receipt convention, over every result object."""

        receipt = load_receipt()
        objects: list[Any] = [receipt["d2_initial_pointed_cell"], receipt["python_only_scope"]]
        for key in ("primary", "secondary"):
            for section in (
                "tables",
                "shape",
                "ties",
                "cell_summary",
                "initial_objects_by_class",
                "witness_groups",
            ):
                objects.append(receipt[section][key])
            objects.extend(receipt["tables"][key]["rows"])
        self.assertGreater(len(objects), 576)
        for obj in objects:
            self.assertIs(obj["bounded"], True)
            self.assertEqual(obj["bound_reached"], mc.ATTEMPTED_N)

    def test_every_committed_witness_is_rechecked_by_the_slow_path(self) -> None:
        receipt = load_receipt()
        candidates = {
            key: {c["name"]: pointed_from_json(c["representative"]) for c in blob["classes"]}
            for key, blob in receipt["candidates"].items()
        }
        rows = rows_by_cell(receipt)
        self.assertEqual(len(rows), 576)
        for (key, cls, obj), row in rows.items():
            source = candidates[key][obj]
            cmask = mc.class_mask(row["class_conditions"])
            self.assertEqual(mc.class_name(cmask), cls)
            self.assertTrue(row["bounded"])
            self.assertEqual(row["bound_reached"], mc.ATTEMPTED_N)
            if row["initial"]:
                self.assertIsNone(row["existence_failure"])
                self.assertIsNone(row["uniqueness_failure"])
                continue
            self.assertTrue(row["existence_failure"] or row["uniqueness_failure"])
            if row["existence_failure"]:
                y = pointed_from_json(row["existence_failure"]["witness"])
                self.assertTrue(mc.is_object(y, key == "secondary"))
                self.assertEqual(mc.morphisms(source, y, cmask), [])
            if row["uniqueness_failure"]:
                blob = row["uniqueness_failure"]
                y = pointed_from_json(blob["witness"])
                self.assertTrue(mc.is_object(y, key == "secondary"))
                f1, f2 = tuple(blob["morphism_1"]), tuple(blob["morphism_2"])
                self.assertNotEqual(f1, f2)
                found = mc.morphisms(source, y, cmask)
                self.assertIn(f1, found)
                self.assertIn(f2, found)
                self.assertEqual(found[:2], [f1, f2])

    def test_terminals_are_legal_scoped_and_not_the_lean_stages(self) -> None:
        """Every terminal whose result depends on the sweep says 'bounded'
        and names the bound in its own scope sentence; REFUSED names the
        refused carrier."""

        receipt = load_receipt()
        names = [item["terminal"] for item in receipt["terminals"]]
        for item in receipt["terminals"]:
            self.assertIn(item["terminal"], LEGAL_TERMINALS)
            self.assertNotIn(item["terminal"], NOT_P2_TERMINALS)
            self.assertTrue(item["scope"].strip())
            if item["terminal"] == "REFUSED":
                self.assertIn(f"N = {mc.REFUSED_N}", item["scope"])
                self.assertIn("refused by name", item["scope"])
            else:
                self.assertIn("bounded", item["scope"])
                self.assertIn(f"N = {mc.ATTEMPTED_N}", item["scope"])
        self.assertEqual(names.count("S9_2_CLASSES_BOUNDED"), 2)
        self.assertEqual(names.count("S9_2_INCOMPARABLE_CLASSES"), 2)
        self.assertEqual(names.count("TIES_RETAINED"), 2)
        self.assertIn("PYTHON_ONLY_SCOPE_DECLARED", names)
        self.assertIn("REFUSED", names)
        self.assertNotIn("S9_2_INTERVAL_SHAPE", names)
        for key in ("primary", "secondary"):
            self.assertEqual(receipt["shape"][key]["terminal"], "S9_2_INCOMPARABLE_CLASSES")
        self.assertEqual(
            receipt["not_in_scope"], ["OB-1", "S6.6", "S9 last bullet (inscription bridge)"]
        )


class FindingsTests(unittest.TestCase):
    """Every receipt key P2_FINDINGS.md cites in backticks must resolve."""

    @staticmethod
    def resolve(receipt: dict[str, Any], path: str) -> bool:
        node: Any = receipt
        for segment in path.split("."):
            if isinstance(node, dict) and segment in node:
                node = node[segment]
            elif isinstance(node, list) and segment.isdigit() and int(segment) < len(node):
                node = node[int(segment)]
            else:
                return False
        return True

    def test_cited_receipt_keys_resolve(self) -> None:
        receipt = load_receipt()
        text = FINDINGS_PATH.read_text(encoding="utf-8")
        cited = [
            token
            for token in re.findall(r"`([^`\n]+)`", text)
            if token.split(".")[0] in receipt
        ]
        self.assertGreater(len(cited), 20)
        unresolved = sorted({token for token in cited if not self.resolve(receipt, token)})
        self.assertEqual(unresolved, [])
        for key in receipt:
            self.assertRegex(key, r"^[a-z0-9_]+$")

    def test_findings_do_not_claim_the_protected_opens_or_the_lean_terminal(self) -> None:
        text = FINDINGS_PATH.read_text(encoding="utf-8")
        self.assertIn(DISCLAIMER, flatten(text))
        self.assertEqual(protected_open_claims(text), [])
        self.assertNotRegex(text, r"emit[s]? S9_2_CLASSES_CLASSIFIED")
        self.assertIn("bounded", text)

    def test_protected_open_detector_catches_every_inflection(self) -> None:
        """The detector must fail on the phrasings a literal check missed."""

        for injected in (
            "OB-1 closed",
            "OB-1 is closed",
            "this closes OB-1",
            "we narrowed S6.6",
            "S6.6 was narrowed",
            "the inscription bridge is priced",
            "pricing the inscription bridge",
            "the S9 last bullet has been closed",
            "OB-1 now closes",
        ):
            self.assertTrue(protected_open_claims(injected), injected)
        self.assertEqual(protected_open_claims(DISCLAIMER), [])
        self.assertEqual(protected_open_claims("it does not close OB-1 and OB-1 stays open"), [])

    def test_lean_target_names_agree_between_module_receipt_and_findings(self) -> None:
        """The proposed names are one list in three places, and every group's
        targets come from it."""

        receipt = load_receipt()
        names = list(mc.LEAN_TARGET_NAMES)
        self.assertEqual(len(names), 15)
        self.assertEqual(len(set(names)), 15)
        self.assertEqual(receipt["lean"]["proposed_target_names"], names)
        self.assertEqual(receipt["lean"]["proposed_target_count"], 15)
        from_groups: set[str] = set()
        for key in ("primary", "secondary"):
            for group in receipt["witness_groups"][key]["groups"].values():
                from_groups.update(group["lean_targets"])
        self.assertEqual(from_groups, set(names))
        text = FINDINGS_PATH.read_text(encoding="utf-8")
        section = text.split("**Lean targets.**", 1)[1].split("## 7.", 1)[0]
        listed = re.findall(r"^\s*\d+\. `([A-Za-z0-9_]+)`", section, re.M)
        self.assertEqual(listed, names)
        self.assertFalse(receipt["lean"]["carried_by_this_part"])
        self.assertEqual(receipt["lean"]["sealed_theorem_cell"]["theorem"], "PrimDiff.D2_initial_pointed")
        self.assertEqual(receipt["lean"]["sealed_theorem_cell"]["class"], "{P}")


class WitnessGroupTests(unittest.TestCase):
    """witness_groups.* re-derived from the receipt rows with predicates
    written here, not the module's; every count the findings state for a
    group is asserted against the receipt value."""

    receipt: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = load_receipt()

    @staticmethod
    def existence_witness(row: dict[str, Any]) -> dict[str, Any] | None:
        blob = row["existence_failure"]
        return None if blob is None else dict(blob["witness"])

    def rows(self, key: str) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = list(self.receipt["tables"][key]["rows"])
        return out

    def group(self, key: str, name: str) -> dict[str, Any]:
        blob: dict[str, Any] = self.receipt["witness_groups"][key]["groups"][name]
        return blob

    def test_partition_counts_match_a_row_recount(self) -> None:
        expected_counts = {
            "primary": [256, 128, 64, 8, 8, 16, 16, 16],
            "secondary": [32, 16, 8, 8],
        }
        for key in ("primary", "secondary"):
            wg = self.receipt["witness_groups"][key]
            self.assertEqual(wg["partition_order"], list(ROW_PREDICATES[key]))
            self.assertEqual(wg["partition_cell_counts"], expected_counts[key])
            self.assertEqual(wg["partition_cell_total"], sum(expected_counts[key]))
            self.assertEqual(wg["table_cells"], len(self.rows(key)))
            self.assertTrue(wg["partition_is_disjoint_and_exhaustive"])
            hits = [0] * len(self.rows(key))
            for name, predicate in ROW_PREDICATES[key].items():
                selected = [i for i, row in enumerate(self.rows(key)) if predicate(row)]
                for i in selected:
                    hits[i] += 1
                group = self.group(key, name)
                self.assertEqual(group["cells"], len(selected))
                self.assertEqual(group["initial"], sum(1 for i in selected if self.rows(key)[i]["initial"]))
                self.assertEqual(
                    group["existence_failures"],
                    sum(1 for i in selected if self.rows(key)[i]["existence_failure"]),
                )
                self.assertEqual(
                    group["uniqueness_failures"],
                    sum(1 for i in selected if self.rows(key)[i]["uniqueness_failure"]),
                )
            self.assertTrue(all(h == 1 for h in hits))

    def test_named_witness_counts_match_a_row_recount(self) -> None:
        def count_at(key: str, name: str, witness: dict[str, Any]) -> int:
            predicate_rows = [row for row in self.rows(key) if ROW_PREDICATES[key][name](row)]
            self.assertEqual(len(predicate_rows), self.group(key, name)["cells"])
            return sum(1 for row in predicate_rows if self.existence_witness(row) == witness)

        legend = self.receipt["witness_groups"]["primary"]["witness_legend"]
        self.assertEqual(legend["SELF1"], SELF1_JSON)
        self.assertEqual(legend["D2"], D2_JSON)
        self.assertEqual(legend["S2"], S2_JSON)
        # Primary: the groups the Lean targets rest on, each named witness recounted.
        self.assertEqual(count_at("primary", "I_classes", SELF1_JSON), 256)
        self.assertEqual(self.group("primary", "I_classes")["existence_witness_counts"], {"SELF1": 256})
        self.assertEqual(
            self.group("primary", "S_without_I_classes")["existence_witness_carriers"],
            {"1": 56, "2": 54, "3": 18},
        )
        self.assertEqual(self.group("primary", "no_P_I_S_classes")["uniqueness_failures"], 64)
        self.assertEqual(count_at("primary", "P_class_non_initial", D2_JSON), 8)
        self.assertEqual(self.group("primary", "P_class_non_initial")["non_initial_diagonal_candidates"], 8)
        self.assertEqual(count_at("primary", "P_E_class", D2_JSON), 15)
        self.assertEqual(self.group("primary", "P_E_class")["existence_witness_counts"], {"D2": 15})
        self.assertEqual(self.group("primary", "P_E_class")["non_initial_off_diagonal_candidates"], 7)
        self.assertEqual(count_at("primary", "P_NE_class", SELF1_JSON), 14)
        self.assertEqual(count_at("primary", "P_NE_class", D2_JSON), 1)
        self.assertEqual(self.group("primary", "P_NE_class")["existence_witness_counts"], {"D2": 1, "SELF1": 14})
        self.assertEqual(count_at("primary", "P_E_NE_class", SELF1_JSON), 14)
        self.assertEqual(count_at("primary", "P_E_NE_class", D2_JSON), 2)
        self.assertEqual(self.group("primary", "P_E_NE_class")["existence_witness_counts"], {"D2": 2, "SELF1": 14})
        # Secondary.
        self.assertEqual(self.group("secondary", "S_classes")["existence_failures"], 32)
        self.assertEqual(count_at("secondary", "S_classes", THREE_JSON), 16)
        self.assertEqual(
            self.group("secondary", "S_classes")["existence_witness_counts"],
            {"D2": 8, "S2": 8, "n3:01:a0b1": 16},
        )
        self.assertEqual(self.group("secondary", "no_P_no_S_classes")["uniqueness_failures"], 16)
        self.assertEqual(count_at("secondary", "P_without_S_non_initial", D2_JSON), 4)
        self.assertEqual(count_at("secondary", "P_without_S_non_initial", S2_JSON), 4)
        self.assertEqual(self.group("secondary", "P_without_S_initial")["initial"], 8)

    def test_no_p_summary_matches_a_row_recount(self) -> None:
        for key, expected in (
            ("primary", (256, 220, 36, 237, SELF1_JSON)),
            ("secondary", (32, 28, 4, 23, S2_JSON)),
        ):
            rows = [row for row in self.rows(key) if "P" not in conditions(row)]
            summary = self.receipt["witness_groups"][key]["no_P_classes"]
            self.assertEqual((len(rows), summary["cells"]), (expected[0], expected[0]))
            self.assertEqual(summary["initial"], 0)
            self.assertFalse(any(row["initial"] for row in rows))
            with_u = [row for row in rows if row["uniqueness_failure"]]
            without_u = [row for row in rows if not row["uniqueness_failure"]]
            self.assertEqual((len(with_u), summary["with_uniqueness_witness"]), (expected[1], expected[1]))
            self.assertEqual((len(without_u), summary["without_uniqueness_witness"]), (expected[2], expected[2]))
            self.assertEqual(
                (sum(1 for row in rows if row["existence_failure"]), summary["with_existence_witness"]),
                (expected[3], expected[3]),
            )
            self.assertEqual(summary["without_any_witness"], 0)
            self.assertEqual(
                summary["classes_without_uniqueness_witness"],
                ["{NE,S}", "{E,NE,S}", "{NE,I,S}", "{E,NE,I,S}"],
            )
            self.assertEqual(sorted({row["class"] for row in without_u}), sorted(summary["classes_without_uniqueness_witness"]))
            for row in without_u:
                self.assertEqual(self.existence_witness(row), expected[4])
            self.assertEqual(
                sum(summary["existence_witness_counts_without_uniqueness_witness"].values()), expected[2]
            )


class FirewallTests(unittest.TestCase):
    def test_p2_files_are_ascii_lf_and_denylist_clean(self) -> None:
        """PROMPT.md step 39 over the files P2 owns, with the working denylist
        loaded from the contact analysis (read-only)."""

        payload: Any = json.loads(
            (common.REPO / "contact" / "analysis" / "contact_countermodels.json").read_text(
                encoding="utf-8"
            )
        )
        census = payload["denylist"]["full_census"]
        subtracted = set(payload["denylist"]["subtracted_as_native_or_core"])
        working = [name for name in census if name not in subtracted]
        self.assertEqual(len(working), 102)
        pattern = re.compile(r"(?<![A-Za-z0-9_])(?:" + "|".join(map(re.escape, working)) + r")(?![A-Za-z0-9_])")
        for path in P2_FILES:
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw, path.name)
            raw.decode("ascii")
            hits = sorted(set(pattern.findall(raw.decode("ascii"))))
            self.assertEqual(hits, [], path.name)


if __name__ == "__main__":
    unittest.main()
