"""Tests for P1 (PROMPT.md step 34): the declared axiom space and its
counts, the transfer classifier against hand-checked cases, the N = 5
refusal, the step-12 defect path under each definition, the step-11 set
reported even when empty together with what decides it before the sweep,
byte-identical replay of the receipt, and negative tests for the forbidden
closures of steps 36, 37, 39 and 40 scoped to P1's own five files.

The bitset computation is cross-checked against the literal definitions,
evaluated with the sealed enumerator ``derivation.primdiff.enumerate_pointed``,
at N = 3.
"""

from __future__ import annotations

import contextlib
import dataclasses
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from typing import Sequence
from unittest import mock

import axiom_lattice as al
import common
import run_axiom_lattice
import verify_lean

TABLE3 = al.build_table(3)
ONE_POINT_FULL: dict[str, object] = {
    "carrier": 1,
    "relation": [[0, 0]],
    "a": 0,
    "b": 0,
    "asserted": True,
    "a_equals_b": True,
}
P1_FILES: tuple[str, ...] = (
    "axiom_lattice.py",
    "run_axiom_lattice.py",
    "test_axiom_lattice.py",
    "receipts/axiom_lattice.json",
    "P1_FINDINGS.md",
)
DENYLIST_JSON = common.REPO / "contact" / "analysis" / "contact_countermodels.json"
PROTECTED_OPENS: tuple[str, ...] = ("OB-1", "S6.6", "S9 last bullet")
PROTECTED_OPEN_MARKERS: tuple[str, ...] = (
    "not in scope",
    "untouched",
    "not claimed",
    "does not close",
    "not closed, narrowed, or priced",
)
CARRIER_GENERAL_PHRASES: tuple[str, ...] = (
    "every carrier",
    "all carriers",
    "every type",
    "every alpha",
    "carrier-general",
    # Added in repair round 2: the pure-fragment lemma was stated in two
    # receipt strings without a bound and none of the phrases above matched.
    "every lattice extent",
    "every pure extent",
    "every pure lattice extent",
    "no pure clause",
    "no clause of this fragment",
)
CARRIER_GENERAL_MARKERS: tuple[str, ...] = (
    "bounded",
    "target",
    "propos",
    "would",
    "not claimed",
    "no carrier-general",
    "forbidden",
    "never",
    "until lean",
    "without a lean theorem",
)
# Regex markers (word-bounded): a unit that says it was checked "at N" or
# names "N = <digit>" carries its bound.
CARRIER_GENERAL_MARKER_PATTERNS: tuple[str, ...] = (r"\bat n\b", r"\bn = \d")
EXTERNAL_MARKERS: tuple[str, ...] = ("http://", "https://", "www.", "et al", "doi:", "arxiv")


def lookup(obj: object, dotted: str) -> object:
    for key in dotted.split("."):
        assert isinstance(obj, dict), f"{dotted}: {key} reached a non-object"
        assert key in obj, f"{dotted}: missing key {key!r}"
        obj = obj[key]
    return obj


def working_denylist() -> set[str]:
    data = json.loads(DENYLIST_JSON.read_text(encoding="utf-8"))
    block = data["denylist"]
    return set(block["full_census"]) - set(block["subtracted_as_native_or_core"])


def denylist_leaks(text: str, denylist: set[str]) -> list[str]:
    """Identifier tokens of ``text`` that lie in the denylist (step 39)."""

    return sorted({tok for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text) if tok in denylist})


def protected_open_violations(text: str) -> list[str]:
    """Lines naming a protected open without a permitted scope marker (step 36)."""

    out: list[str] = []
    for line in text.splitlines():
        if any(name in line for name in PROTECTED_OPENS):
            low = line.lower()
            if not any(marker in low for marker in PROTECTED_OPEN_MARKERS):
                out.append(line)
    return out


def prose_units(text: str) -> list[str]:
    """Sentences of a markdown text; table rows are their own units.  A
    heuristic, declared as one."""

    units: list[str] = []
    for paragraph in text.split("\n\n"):
        lines = [ln for ln in paragraph.split("\n") if ln.strip()]
        if lines and all(ln.lstrip().startswith("|") for ln in lines):
            units.extend(lines)
        else:
            units.extend(re.split(r"(?<=[.!?])\s+", " ".join(lines)))
    return units


def carrier_general_violations(text: str) -> list[str]:
    """Units that speak of every carrier without a bound, a proposal, or a
    denial in the same unit (step 37)."""

    out: list[str] = []
    for unit in prose_units(text):
        low = unit.lower()
        if any(p in low for p in CARRIER_GENERAL_PHRASES):
            if not any(m in low for m in CARRIER_GENERAL_MARKERS) and not any(
                re.search(p, low) for p in CARRIER_GENERAL_MARKER_PATTERNS
            ):
                out.append(unit)
    return out


def receipt_strings(obj: object, path: str = "") -> list[tuple[str, str]]:
    """Every key and every string value of a receipt, with its dotted path."""

    out: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            out.append((path + "." + key, key))
            out.extend(receipt_strings(value, path + "." + key))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            out.extend(receipt_strings(value, f"{path}[{i}]"))
    elif isinstance(obj, str):
        out.append((path, obj))
    return out


def external_markers(text: str) -> list[str]:
    low = text.lower()
    return [m for m in EXTERNAL_MARKERS if m in low]


class ClauseSpaceTests(unittest.TestCase):
    def test_pure_counts_before_and_after_swap(self) -> None:
        report = al.clause_space_report(al.PURE)
        self.assertEqual(report["raw_clause_count"], 80)
        self.assertEqual(report["swap_orbit_count"], 42)
        self.assertEqual(report["swap_fixed_clause_count"], 4)
        self.assertEqual(report["head_in_body_count"], 32)
        self.assertEqual(report["nontrivial_clause_count"], 48)
        self.assertEqual(report["nontrivial_swap_orbit_count"], 26)
        self.assertEqual(report["used_downstream"], "nontrivial_swap_orbit_count")
        self.assertEqual(len(al.generating_clauses(al.PURE)), 26)

    def test_pure_one_variable_clauses_are_seven_raw_and_four_orbits(self) -> None:
        report = al.clause_space_report(al.PURE)
        self.assertEqual(report["one_variable_meaning"], al.ONE_VARIABLE_MEANING)
        self.assertEqual(report["one_variable_clause_count_raw"], 7)
        self.assertEqual(report["one_variable_swap_orbit_count"], 4)
        self.assertEqual(report["two_variable_clause_count_raw"], 73)
        self.assertEqual(
            report["one_variable_clauses_raw"],
            [
                "-> r x x",
                "r x x -> r x x",
                "-> r y y",
                "r y y -> r y y",
                "-> falsum",
                "r x x -> falsum",
                "r y y -> falsum",
            ],
        )
        self.assertEqual(al.UNSATISFIABLE.variables(), frozenset())
        self.assertEqual(al.IRREFLEXIVITY.variables(), frozenset({"x"}))
        self.assertEqual(al.SYMMETRY.variables(), frozenset({"x", "y"}))
        self.assertFalse(al.SYMMETRY.one_variable())

    def test_eq_bearing_counts_before_and_after_swap(self) -> None:
        report = al.clause_space_report(al.EQ_BEARING)
        self.assertEqual(report["raw_clause_count"], 112)
        self.assertEqual(report["swap_orbit_count"], 62)
        self.assertEqual(report["swap_fixed_clause_count"], 12)
        self.assertEqual(report["head_in_body_count"], 48)
        self.assertEqual(report["nontrivial_clause_count"], 64)
        self.assertEqual(report["nontrivial_swap_orbit_count"], 36)
        self.assertEqual(report["one_variable_clause_count_raw"], 0)
        self.assertEqual(report["one_variable_swap_orbit_count"], 0)
        self.assertEqual(report["two_variable_clause_count_raw"], 112)
        self.assertEqual(len(al.generating_clauses(al.EQ_BEARING)), 36)
        for clause in al.enumerate_clauses(al.EQ_BEARING):
            self.assertTrue(clause.mentions_eq())
            self.assertEqual(clause.variables(), frozenset({"x", "y"}), clause.text())
        self.assertFalse(any(c.mentions_eq() for c in al.enumerate_clauses(al.PURE)))

    def test_merged_counts_are_sums_and_carry_the_merge_sentence(self) -> None:
        report = al.clause_space_report(al.MERGED)
        self.assertEqual(report["raw_clause_count"], 192)
        self.assertEqual(report["nontrivial_swap_orbit_count"], 62)
        self.assertEqual(report["one_variable_clause_count_raw"], 7)
        self.assertEqual(report["two_variable_clause_count_raw"], 185)
        self.assertEqual(report["merge_sentence"], al.MERGE_SENTENCE)
        self.assertEqual(len(al.generating_clauses(al.MERGED)), 62)

    def test_swap_is_an_involution_with_orbits_of_size_at_most_two(self) -> None:
        for fragment in (al.PURE, al.EQ_BEARING):
            for clause in al.enumerate_clauses(fragment):
                self.assertEqual(clause.swap().swap(), clause)
            for orbit in al.swap_orbits(al.enumerate_clauses(fragment)):
                self.assertIn(len(orbit), (1, 2))

    def test_swap_fixes_every_extent(self) -> None:
        for fragment in (al.PURE, al.EQ_BEARING):
            for clause in al.enumerate_clauses(fragment):
                self.assertEqual(
                    al.clause_extent(clause, TABLE3),
                    al.clause_extent(clause.swap(), TABLE3),
                    clause.text(),
                )

    def test_pure_clause_is_valid_iff_head_in_body(self) -> None:
        for clause in al.enumerate_clauses(al.PURE):
            self.assertEqual(
                al.clause_extent(clause, TABLE3) == TABLE3.top,
                clause.head_in_body(),
                clause.text(),
            )

    def test_eq_bearing_has_valid_clauses_beyond_head_in_body(self) -> None:
        valid = [
            c
            for c in al.generating_clauses(al.EQ_BEARING)
            if al.clause_extent(c, TABLE3) == TABLE3.top
        ]
        self.assertEqual(len(valid), 14)
        for clause in valid:
            self.assertFalse(clause.head_in_body())
            self.assertIn(al.EQ_ATOM, clause.body_atoms())
            self.assertIn(clause.head, al.R_ATOMS)

    def test_generating_set_drops_head_in_body_only(self) -> None:
        for fragment in (al.PURE, al.EQ_BEARING):
            generators = al.generating_clauses(fragment)
            self.assertFalse(any(c.head_in_body() for c in generators))
            orbits = al.swap_orbits(al.enumerate_clauses(fragment))
            self.assertEqual(
                len(generators), sum(1 for o in orbits if not o[0].head_in_body())
            )

    def test_clause_texts(self) -> None:
        self.assertEqual(al.IRREFLEXIVITY.text(), "r x x -> falsum")
        self.assertEqual(al.SYMMETRY.text(), "r x y -> r y x")
        self.assertEqual(al.FULL_FORCING.text(), "-> r x y")
        self.assertEqual(al.REFLEXIVITY.text(), "-> r x x")
        self.assertEqual(al.ASYMMETRY.text(), "r x y, r y x -> falsum")
        self.assertEqual(al.REFLEXIVE_POINT_FORCES_SINGLETON.text(), "r x x -> x = y")
        self.assertEqual(al.SINGLETON.text(), "-> x = y")


class RelationTableTests(unittest.TestCase):
    def test_census_and_classes_at_n3(self) -> None:
        self.assertEqual(TABLE3.census, {1: 2, 2: 16, 3: 512})
        self.assertEqual(TABLE3.class_total, 86)
        self.assertEqual(sum(TABLE3.class_count), 530)
        self.assertEqual(TABLE3.total_size(TABLE3.top), 530)

    def test_class_extents_expand_to_the_literal_extents(self) -> None:
        for clause in al.generating_clauses(al.MERGED):
            self.assertEqual(
                TABLE3.expand(al.clause_extent(clause, TABLE3)),
                al.literal_extent(clause, 3),
                clause.text(),
            )

    def test_irreflexivity_extent_is_exactly_the_irreflexive_relations(self) -> None:
        extent = al.clause_extent(al.IRREFLEXIVITY, TABLE3)
        for n, rel in TABLE3.expand(TABLE3.top):
            self.assertEqual(
                (n, rel) in TABLE3.expand(extent), all(x != y for x, y in rel)
            )
        self.assertEqual(TABLE3.size_by_carrier(extent), {"1": 1, "2": 4, "3": 64})

    def test_carrier_five_is_refused_by_name(self) -> None:
        with self.assertRaisesRegex(al.RefusedCarrier, "N = 5 is refused by name"):
            al.build_table(5)
        with self.assertRaisesRegex(al.RefusedCarrier, "refused by name"):
            al.check_carrier_bound(6)
        with self.assertRaises(al.RefusedCarrier):
            al.literal_extent(al.IRREFLEXIVITY, 5)
        with self.assertRaises(al.RefusedCarrier):
            al.build_receipt(attempted=5)
        record = al.refusal_record(5)
        self.assertEqual(record["terminal"], "REFUSED")
        self.assertEqual(record["carrier"], 5)
        self.assertEqual(record["relations_that_would_be_added"], 1 << 25)
        with self.assertRaises(ValueError):
            al.build_table(0)

    def test_full_relation_classes(self) -> None:
        self.assertEqual(al.full_relation_classes(TABLE3).bit_count(), 3)
        self.assertEqual(al.one_point_full_class(TABLE3).bit_count(), 1)
        self.assertEqual(al.two_point_full_class(TABLE3).bit_count(), 1)
        self.assertEqual(
            TABLE3.expand(al.one_point_full_class(TABLE3)), {(1, frozenset({(0, 0)}))}
        )
        self.assertEqual(
            TABLE3.expand(al.two_point_full_class(TABLE3)),
            {(2, frozenset({(0, 0), (0, 1), (1, 0), (1, 1)}))},
        )
        self.assertEqual(
            al.render_extent_relations(al.one_point_full_class(TABLE3), TABLE3),
            [{"carrier": 1, "relation": [[0, 0]]}],
        )
        rendered = al.render_extent_relations(
            al.clause_extent(al.EMPTY_FORCING, TABLE3), TABLE3
        )
        self.assertEqual(rendered, [{"carrier": n, "relation": []} for n in (1, 2, 3)])
        irrefl = al.render_extent_relations(al.clause_extent(al.IRREFLEXIVITY, TABLE3), TABLE3)
        self.assertEqual(len(irrefl), 69)
        self.assertEqual(irrefl[0], {"carrier": 1, "relation": []})
        self.assertEqual(irrefl[-1]["carrier"], 3)


class TransferTests(unittest.TestCase):
    def verdict(self, clause: al.Clause, defn: al.TransferDefinition) -> al.TransferVerdict:
        return al.transfer_verdict(al.clause_extent(clause, TABLE3), defn, TABLE3)

    def test_irreflexivity_transfers_under_both_definitions(self) -> None:
        for defn in al.DEFINITIONS:
            verdict = self.verdict(al.IRREFLEXIVITY, defn)
            self.assertTrue(verdict.transfers, defn.name)
            self.assertIsNone(verdict.witness)
            self.assertTrue(al.literal_transfer(al.IRREFLEXIVITY, defn, 3)[0])
        model = al.witnessed_model(al.clause_extent(al.IRREFLEXIVITY, TABLE3), TABLE3)
        assert model is not None
        self.assertFalse(model["a_equals_b"])
        self.assertTrue(model["asserted"])

    def test_symmetry_does_not_transfer_and_names_its_witness(self) -> None:
        verdict = self.verdict(al.SYMMETRY, al.TRANSFER_ALL_CARRIERS)
        self.assertFalse(verdict.transfers)
        self.assertEqual(verdict.witness, ONE_POINT_FULL)
        above = self.verdict(al.SYMMETRY, al.TRANSFER_ABOVE_POINT)
        self.assertFalse(above.transfers)
        assert above.witness is not None
        self.assertEqual(above.witness["carrier"], 2)
        self.assertTrue(above.witness["a_equals_b"])
        pairs = above.witness["relation"]
        assert isinstance(pairs, list)
        rel = frozenset((int(x), int(y)) for x, y in pairs)
        self.assertTrue(al.clause_holds(al.SYMMETRY, 2, rel))
        literal, structure = al.literal_transfer(al.SYMMETRY, al.TRANSFER_ALL_CARRIERS, 3)
        self.assertFalse(literal)
        assert structure is not None
        self.assertEqual(structure.a, structure.b)

    def test_empty_axiom_and_full_forcing_do_not_transfer(self) -> None:
        top = al.transfer_verdict(TABLE3.top, al.TRANSFER_ALL_CARRIERS, TABLE3)
        self.assertFalse(top.transfers)
        self.assertEqual(top.witness, ONE_POINT_FULL)
        full = self.verdict(al.FULL_FORCING, al.TRANSFER_ALL_CARRIERS)
        self.assertFalse(full.transfers)
        self.assertEqual(full.witness, ONE_POINT_FULL)
        self.assertFalse(self.verdict(al.REFLEXIVITY, al.TRANSFER_ABOVE_POINT).transfers)

    def test_unsatisfiable_and_empty_forcing_transfer_vacuously(self) -> None:
        self.assertEqual(al.clause_extent(al.UNSATISFIABLE, TABLE3), 0)
        for clause in (al.UNSATISFIABLE, al.EMPTY_FORCING):
            for defn in al.DEFINITIONS:
                self.assertTrue(self.verdict(clause, defn).transfers)
            self.assertIsNone(al.witnessed_model(al.clause_extent(clause, TABLE3), TABLE3))
        self.assertEqual(
            TABLE3.size_by_carrier(al.clause_extent(al.EMPTY_FORCING, TABLE3)),
            {"1": 1, "2": 1, "3": 1},
        )

    def test_asymmetry_transfers_with_a_witnessed_model(self) -> None:
        self.assertTrue(self.verdict(al.ASYMMETRY, al.TRANSFER_ALL_CARRIERS).transfers)
        self.assertTrue(
            al.entails_irreflexivity(al.clause_extent(al.ASYMMETRY, TABLE3), TABLE3)
        )
        self.assertIsNotNone(al.witnessed_model(al.clause_extent(al.ASYMMETRY, TABLE3), TABLE3))

    def test_reflexive_point_forces_singleton_separates_the_definitions(self) -> None:
        extent = al.clause_extent(al.REFLEXIVE_POINT_FORCES_SINGLETON, TABLE3)
        below = al.transfer_verdict(extent, al.TRANSFER_ALL_CARRIERS, TABLE3)
        self.assertFalse(below.transfers)
        self.assertEqual(below.witness, ONE_POINT_FULL)
        self.assertTrue(al.transfer_verdict(extent, al.TRANSFER_ABOVE_POINT, TABLE3).transfers)
        self.assertFalse(al.entails_irreflexivity(extent, TABLE3))
        self.assertEqual(TABLE3.size_by_carrier(extent), {"1": 2, "2": 4, "3": 64})

    def test_transfer_is_containment_in_a_fixed_extent(self) -> None:
        irrefl = al.clause_extent(al.IRREFLEXIVITY, TABLE3)
        w_default = al.transfer_extent(al.TRANSFER_ALL_CARRIERS, TABLE3)
        w_above = al.transfer_extent(al.TRANSFER_ABOVE_POINT, TABLE3)
        self.assertEqual(w_default, irrefl)
        self.assertEqual(w_above, al.clause_extent(al.REFLEXIVE_POINT_FORCES_SINGLETON, TABLE3))
        self.assertEqual(w_above ^ irrefl, al.one_point_full_class(TABLE3))
        for clause in al.generating_clauses(al.MERGED):
            e = al.clause_extent(clause, TABLE3)
            for defn, w in ((al.TRANSFER_ALL_CARRIERS, w_default), (al.TRANSFER_ABOVE_POINT, w_above)):
                self.assertEqual(
                    al.transfer_verdict(e, defn, TABLE3).transfers, e & w == e, clause.text()
                )

    def test_W_from_raw_census_matches_the_literal_definition_at_n3(self) -> None:
        raw = al.reflexive_classes_from_raw_census(TABLE3)
        self.assertEqual(raw, TABLE3.reflexive_classes())
        everything = TABLE3.expand(TABLE3.top)
        for defn in al.DEFINITIONS:
            w = al.transfer_extent_from_raw_census(defn, TABLE3, raw)
            self.assertEqual(w, al.transfer_extent(defn, TABLE3), defn.name)
            literal = {
                (n, rel)
                for n, rel in everything
                if n < defn.min_carrier or all(x != y for x, y in rel)
            }
            self.assertEqual(TABLE3.expand(w), literal, defn.name)

    def test_raw_census_homogeneity_guard_bites(self) -> None:
        # Collapse every relation of a carrier into one pattern class; the
        # class then mixes reflexive and irreflexive relations and the guard
        # names it.
        with mock.patch.object(al, "pattern_set", lambda n, mask: 0):
            table = al.build_table(2)
            self.assertEqual(table.class_total, 2)
            with self.assertRaisesRegex(AssertionError, "mixes relations"):
                al.reflexive_classes_from_raw_census(table)

    def test_W_disagreement_between_the_two_paths_raises(self) -> None:
        def lie(defn: al.TransferDefinition, table: al.RelationTable, raw: int) -> int:
            return al.transfer_extent(defn, table) ^ 1

        with mock.patch.object(al, "transfer_extent_from_raw_census", lie):
            with self.assertRaisesRegex(AssertionError, "raw relation census disagrees"):
                al.analyze_fragment(al.PURE, TABLE3)

    def test_definition_flag_disagreeing_with_the_verdict_raises(self) -> None:
        wrong = dataclasses.replace(
            al.TRANSFER_ALL_CARRIERS, f3_set_empty_by_definitional_identity=False
        )
        with mock.patch.object(al, "DEFINITIONS", (wrong,)):
            with self.assertRaisesRegex(AssertionError, "definition-level"):
                al.analyze_fragment(al.PURE, TABLE3)

    def test_bitset_verdicts_match_the_literal_definition_at_n3(self) -> None:
        for clause in al.generating_clauses(al.MERGED):
            for defn in al.DEFINITIONS:
                literal, structure = al.literal_transfer(clause, defn, 3)
                verdict = self.verdict(clause, defn)
                self.assertEqual(verdict.transfers, literal, f"{clause.text()} {defn.name}")
                if structure is not None:
                    assert verdict.witness is not None
                    self.assertTrue(verdict.witness["a_equals_b"])

    def test_entails_irreflexivity_is_extent_containment(self) -> None:
        irrefl = al.clause_extent(al.IRREFLEXIVITY, TABLE3)
        for clause in al.generating_clauses(al.MERGED):
            extent = al.clause_extent(clause, TABLE3)
            self.assertEqual(
                al.entails_irreflexivity(extent, TABLE3), extent & irrefl == extent
            )


class LatticeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pure = al.analyze_fragment(al.PURE, TABLE3)
        self.eq = al.analyze_fragment(al.EQ_BEARING, TABLE3)
        self.merged = al.analyze_fragment(al.MERGED, TABLE3)

    def test_closure_contains_top_bottom_and_generators_and_is_meet_closed(self) -> None:
        generators = al.generating_clauses(al.PURE)
        extents = [al.clause_extent(c, TABLE3) for c in generators]
        lattice = al.meet_closure(extents, TABLE3.top, al.CLOSURE_BOUND)
        self.assertIn(TABLE3.top, lattice.elements)
        self.assertIn(0, lattice.elements)
        for e in extents:
            self.assertIn(e, lattice.elements)
        for a in lattice.elements:
            for b in lattice.elements:
                self.assertIn(a & b, lattice.representative)
        self.assertFalse(lattice.truncated)
        self.assertEqual(lattice.representative[TABLE3.top], ())

    def test_closure_bound_truncates_and_says_so(self) -> None:
        extents = [al.clause_extent(c, TABLE3) for c in al.generating_clauses(al.PURE)]
        lattice = al.meet_closure(extents, TABLE3.top, 5)
        self.assertTrue(lattice.truncated)
        self.assertEqual(len(lattice.elements), 5)
        result = al.analyze_fragment(al.PURE, TABLE3, closure_bound=5)
        self.assertTrue(lookup(result, "lattice.closure_bound_hit"))
        self.assertTrue(lookup(result, "bound_reached.closure_bound_hit"))

    def test_sizes_at_n3(self) -> None:
        self.assertEqual(lookup(self.pure, "single_clause_extents.extent_class_count"), 20)
        self.assertEqual(lookup(self.pure, "single_clause_extents.syntax_class_count"), 26)
        self.assertEqual(lookup(self.pure, "lattice.closure_size"), 75)
        self.assertEqual(lookup(self.pure, "lattice.syntax_axiom_count"), 1 << 26)
        self.assertEqual(lookup(self.eq, "single_clause_extents.extent_class_count"), 14)
        self.assertEqual(lookup(self.eq, "lattice.closure_size"), 37)
        self.assertEqual(lookup(self.merged, "single_clause_extents.extent_class_count"), 31)
        self.assertEqual(lookup(self.merged, "lattice.closure_size"), 147)
        for result in (self.pure, self.eq, self.merged):
            self.assertFalse(lookup(result, "lattice.truncated"))
            self.assertTrue(lookup(result, "lattice.irreflexivity_extent_in_lattice"))
            self.assertTrue(
                lookup(result, "lattice.transferring_iff_representative_has_falsum_head")
            )

    def test_step10_findings_under_the_default_in_the_pure_fragment(self) -> None:
        analysis = lookup(self.pure, "transfer.TRANSFER_ALL_CARRIERS")
        self.assertEqual(lookup(analysis, "transferring_count"), 5)
        self.assertTrue(lookup(analysis, "closed_under_strengthening"))
        self.assertTrue(lookup(analysis, "closed_under_meet"))
        self.assertFalse(lookup(analysis, "closed_under_weakening"))
        witness = lookup(analysis, "closed_under_weakening_witness")
        self.assertEqual(lookup(witness, "not_transferring.extent_size_total"), 530)
        self.assertEqual(lookup(witness, "failure"), ONE_POINT_FULL)
        self.assertTrue(lookup(analysis, "unique_weakest_exists"))
        self.assertEqual(
            lookup(analysis, "unique_weakest.representative_axiom"), ["r x x -> falsum"]
        )
        self.assertTrue(lookup(analysis, "unique_weakest_equals_irreflexivity_extent"))
        self.assertTrue(lookup(analysis, "unique_weakest_equals_W"))
        self.assertTrue(lookup(analysis, "generated_by_irreflexivity"))

    def test_transfer_as_containment_in_every_cell(self) -> None:
        for name, result in (("PURE", self.pure), ("EQ", self.eq), ("MERGED", self.merged)):
            for defn in al.DEFINITIONS:
                block = lookup(result, f"transfer.{defn.name}.transfer_as_containment")
                self.assertTrue(
                    lookup(block, "transferring_equals_lattice_extents_contained_in_W"),
                    f"{name} {defn.name}",
                )
                minus = lookup(block, "W_minus_irreflexivity_extent.relations")
                if defn is al.TRANSFER_ALL_CARRIERS:
                    self.assertTrue(lookup(block, "W_equals_irreflexivity_extent"))
                    self.assertEqual(minus, [])
                    self.assertTrue(lookup(block, "W_in_lattice"))
                else:
                    self.assertFalse(lookup(block, "W_equals_irreflexivity_extent"))
                    self.assertEqual(minus, [{"carrier": 1, "relation": [[0, 0]]}])
        self.assertFalse(
            lookup(self.pure, "transfer.TRANSFER_ABOVE_POINT.transfer_as_containment.W_in_lattice")
        )
        self.assertEqual(
            lookup(
                self.pure,
                "transfer.TRANSFER_ABOVE_POINT.transfer_as_containment.W_realized_by_generators",
            ),
            [],
        )
        self.assertFalse(lookup(self.pure, "transfer.TRANSFER_ABOVE_POINT.unique_weakest_equals_W"))
        for result in (self.eq, self.merged):
            block = lookup(result, "transfer.TRANSFER_ABOVE_POINT.transfer_as_containment")
            self.assertTrue(lookup(block, "W_in_lattice"))
            self.assertEqual(lookup(block, "W_realized_by_generators"), ["r x x -> x = y"])
            self.assertTrue(lookup(result, "transfer.TRANSFER_ABOVE_POINT.unique_weakest_equals_W"))

    def test_step11_set_is_reported_even_when_empty(self) -> None:
        for result in (self.pure, self.eq, self.merged):
            for defn in al.DEFINITIONS:
                f3 = lookup(result, f"transfer.{defn.name}.f3_set")
                assert isinstance(f3, dict)
                self.assertIn("members", f3)
                self.assertNotIn("empty_by_construction", f3)
                self.assertEqual(
                    lookup(f3, "empty_by_definitional_identity"),
                    defn.f3_set_empty_by_definitional_identity,
                )
                self.assertEqual(
                    lookup(f3, "empty_by_definitional_identity"),
                    lookup(f3, "decided_before_the_sweep.verdict")
                    == "empty_by_definitional_identity",
                )
            default = lookup(result, "transfer.TRANSFER_ALL_CARRIERS.f3_set")
            self.assertEqual(lookup(default, "count"), 0)
            self.assertEqual(lookup(default, "members"), [])
            self.assertFalse(lookup(default, "nonempty_by_construction"))
            self.assertEqual(
                lookup(default, "decided_before_the_sweep.verdict"),
                "empty_by_definitional_identity",
            )
        above = lookup(self.pure, "transfer.TRANSFER_ABOVE_POINT.f3_set")
        self.assertFalse(lookup(above, "empty_by_definitional_identity"))
        self.assertFalse(lookup(above, "nonempty_by_construction"))
        self.assertEqual(lookup(above, "count"), 0)
        self.assertEqual(lookup(above, "members"), [])
        self.assertEqual(lookup(above, "decided_before_the_sweep.verdict"), "empty_by_lemma")
        self.assertIsNone(lookup(above, "decided_before_the_sweep.named_generator"))
        premises = lookup(above, "decided_before_the_sweep.premises_checked_at_N")
        self.assertTrue(lookup(premises, "one_point_full_implies_two_point_full_on_lattice"))
        self.assertFalse(lookup(premises, "W_in_lattice"))
        self.assertEqual(lookup(premises, "bound_reached"), 3)

    def test_step10_and_step11_above_the_point_in_the_eq_fragment(self) -> None:
        analysis = lookup(self.eq, "transfer.TRANSFER_ABOVE_POINT")
        self.assertEqual(lookup(analysis, "transferring_count"), 10)
        self.assertTrue(lookup(analysis, "unique_weakest_exists"))
        self.assertEqual(
            lookup(analysis, "unique_weakest.representative_axiom"), ["r x x -> x = y"]
        )
        self.assertFalse(lookup(analysis, "unique_weakest_equals_irreflexivity_extent"))
        self.assertFalse(lookup(analysis, "generated_by_irreflexivity"))
        self.assertTrue(lookup(analysis, "closed_under_strengthening"))
        self.assertTrue(lookup(analysis, "closed_under_meet"))
        members = lookup(analysis, "f3_set.members")
        assert isinstance(members, list)
        self.assertEqual(len(members), 5)
        self.assertEqual(lookup(analysis, "f3_set.count"), 5)
        self.assertIn(["r x x -> x = y"], [m["representative_axiom"] for m in members])
        for member in members:
            self.assertTrue(member["uses_eq_atom"])
            self.assertEqual(member["not_entailing_witness"], ONE_POINT_FULL)
        self.assertTrue(lookup(analysis, "f3_set.nonempty_by_construction"))
        decision = lookup(analysis, "f3_set.decided_before_the_sweep")
        self.assertEqual(lookup(decision, "verdict"), "nonempty_by_named_generator")
        self.assertEqual(lookup(decision, "named_generator"), "r x x -> x = y")
        premises = lookup(decision, "premises_checked_at_N")
        self.assertFalse(lookup(premises, "one_point_full_implies_two_point_full_on_lattice"))
        self.assertTrue(lookup(premises, "W_admits_one_point_full"))
        self.assertTrue(lookup(premises, "W_transfers"))
        merged = lookup(self.merged, "transfer.TRANSFER_ABOVE_POINT")
        self.assertEqual(lookup(merged, "f3_set.count"), 6)
        self.assertTrue(lookup(merged, "f3_set.nonempty_by_construction"))
        merged_members = lookup(merged, "f3_set.members")
        assert isinstance(merged_members, list)
        self.assertTrue(all(m["uses_eq_atom"] for m in merged_members))
        # The pure fragment is rigid at N = 3: every pure lattice extent that
        # admits the one-point full relation also fails above the point.
        pure_elements = al.meet_closure(
            [al.clause_extent(c, TABLE3) for c in al.generating_clauses(al.PURE)],
            TABLE3.top,
            al.CLOSURE_BOUND,
        ).elements
        admitting = [e for e in pure_elements if TABLE3.size_by_carrier(e)["1"] == 2]
        self.assertGreater(len(admitting), 0)
        for e in admitting:
            self.assertFalse(al.transfer_verdict(e, al.TRANSFER_ABOVE_POINT, TABLE3).transfers)

    def test_f3_decision_disagreeing_with_the_sweep_raises(self) -> None:
        real = al.f3_decision

        def lie(
            defn: al.TransferDefinition,
            lattice: al.Lattice,
            generators: Sequence[al.Clause],
            extents: Sequence[int],
            table: al.RelationTable,
            w: int,
            irrefl_extent: int,
        ) -> dict[str, object]:
            record = real(defn, lattice, generators, extents, table, w, irrefl_extent)
            if record["verdict"] == "nonempty_by_named_generator":
                record["verdict"] = "empty_by_lemma"
            elif record["verdict"] == "empty_by_lemma":
                record["verdict"] = "nonempty_by_named_generator"
            return record

        with mock.patch.object(al, "f3_decision", lie):
            with self.assertRaisesRegex(AssertionError, "empty_by_lemma but the sweep found"):
                al.analyze_fragment(al.EQ_BEARING, TABLE3)
            with self.assertRaisesRegex(AssertionError, "found no member"):
                al.analyze_fragment(al.PURE, TABLE3)

    def test_lean_target_evidence_is_computed_and_bounded(self) -> None:
        for result in (self.pure, self.eq, self.merged):
            evidence = lookup(result, "lean_target_evidence")
            self.assertTrue(lookup(evidence, "bounded"))
            self.assertEqual(lookup(evidence, "bound_reached"), 3)
            assert isinstance(evidence, dict)
            self.assertFalse(any("every_carrier" in key for key in evidence))
            for key in (
                "T1_atom_headed_generators_admit_full_relation_on_carriers_1_to_N",
                "T2_non_falsum_generators_admit_one_point_full",
                "T3_falsum_headed_generators_entail_irreflexivity",
                "T4_lattice_transfers_iff_representative_has_falsum_head",
            ):
                self.assertTrue(lookup(evidence, key), key)
        self.assertEqual(
            lookup(
                self.pure,
                "lean_target_evidence."
                "T7_lattice_extents_admitting_one_point_full_and_transferring_above_point",
            ),
            0,
        )
        self.assertEqual(
            lookup(
                self.eq,
                "lean_target_evidence."
                "T7_lattice_extents_admitting_one_point_full_and_transferring_above_point",
            ),
            5,
        )
        pure_evidence = self.pure["lean_target_evidence"]
        assert isinstance(pure_evidence, dict)
        self.assertNotIn("T6_reflexive_point_forces_singleton", pure_evidence)
        t6 = lookup(self.eq, "lean_target_evidence.T6_reflexive_point_forces_singleton")
        self.assertTrue(lookup(t6, "transfers_above_point"))
        self.assertTrue(lookup(t6, "admits_one_point_full"))
        self.assertFalse(lookup(t6, "entails_irreflexivity"))

    def test_merged_carries_the_merge_sentence(self) -> None:
        self.assertEqual(self.merged["merge_sentence"], al.MERGE_SENTENCE)
        self.assertNotIn("merge_sentence", self.pure)
        self.assertNotIn("merge_sentence", self.eq)

    def test_closure_restriction_mechanics_from_n3_onto_n2(self) -> None:
        table2 = al.build_table(2)
        for fragment in al.FRAGMENTS:
            block = al.closure_restriction(fragment, TABLE3, table2)
            self.assertEqual(block["from_carrier"], 3)
            self.assertEqual(block["to_carrier"], 2)
            self.assertEqual(block["bound_reached"], 3)
            self.assertTrue(block["bounded"])
            self.assertFalse(block["truncated"])
            upper = int(str(block["upper_closure_size"]))
            distinct = int(str(block["distinct_restrictions"]))
            self.assertLessEqual(distinct, upper)
            self.assertEqual(block["injective"], distinct == upper)
            self.assertEqual("merge_sentence" in block, fragment == al.MERGED)
        self.assertEqual(
            al.closure_restriction(al.PURE, TABLE3, table2)["upper_closure_size"], 75
        )
        with self.assertRaises(ValueError):
            al.closure_restriction(al.PURE, table2, TABLE3)
        # extent_keys drops the classes above the target carrier.
        keys = al.extent_keys(TABLE3, TABLE3.top, 2)
        self.assertTrue(all(n <= 2 for n, _ in keys))
        self.assertEqual(len(keys), al.build_table(2).class_total)


class AuditTests(unittest.TestCase):
    def test_all_transfer_is_a_defect_naming_the_one_point_full_relation(self) -> None:
        rows = [("r x x -> falsum", True, None), ("r x y -> r y x", True, None)]
        audit = al.audit_classifier(rows, TABLE3)
        self.assertTrue(audit["defect"])
        self.assertEqual(audit["kind"], "all transfer")
        self.assertEqual(audit["witness"], ONE_POINT_FULL)

    def test_none_transfer_is_a_defect_naming_irreflexivity(self) -> None:
        fake: dict[str, object] = {"carrier": 1, "relation": [[0, 0]], "a": 0, "b": 0}
        rows = [("r x x -> falsum", False, fake), ("r x y -> r y x", False, fake)]
        audit = al.audit_classifier(rows, TABLE3)
        self.assertTrue(audit["defect"])
        self.assertEqual(audit["kind"], "none transfer")
        self.assertEqual(
            audit["witness"], {"clause": "r x x -> falsum", "reported_failure": fake}
        )
        self.assertTrue(al.audit_classifier([], TABLE3)["defect"])

    def test_the_real_table_is_mixed_under_each_definition(self) -> None:
        expected = {
            al.PURE: {"TRANSFER_ALL_CARRIERS": (4, 16), "TRANSFER_ABOVE_POINT": (4, 16)},
            al.EQ_BEARING: {"TRANSFER_ALL_CARRIERS": (2, 12), "TRANSFER_ABOVE_POINT": (4, 10)},
            al.MERGED: {"TRANSFER_ALL_CARRIERS": (4, 27), "TRANSFER_ABOVE_POINT": (6, 25)},
        }
        for fragment in al.FRAGMENTS:
            audits = lookup(al.analyze_fragment(fragment, TABLE3), "classifier_audit")
            assert isinstance(audits, dict)
            self.assertEqual(sorted(audits), sorted(d.name for d in al.DEFINITIONS))
            for defn in al.DEFINITIONS:
                audit = lookup(audits, defn.name)
                self.assertFalse(lookup(audit, "defect"), f"{fragment} {defn.name}")
                self.assertEqual(lookup(audit, "kind"), "mixed")
                self.assertEqual(
                    (lookup(audit, "transferring_count"), lookup(audit, "non_transferring_count")),
                    expected[fragment][defn.name],
                    f"{fragment} {defn.name}",
                )
                # The rows are the single-clause extent classes, and the
                # receipt says so; the old key class_total (431, the pattern
                # classes of the table) is gone.
                assert isinstance(audit, dict)
                self.assertNotIn("class_total", audit)
                self.assertEqual(lookup(audit, "row_count"), sum(expected[fragment][defn.name]))
                self.assertIn("single-clause extent classes", str(lookup(audit, "rows_are")))


class ReceiptTests(unittest.TestCase):
    receipt: dict[str, object]

    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = al.build_receipt()

    def test_header_bounds_and_refusal(self) -> None:
        self.assertEqual(self.receipt["header"], common.receipt_header())
        self.assertEqual(self.receipt["declared_bounds"], al.DECLARED_BOUNDS)
        self.assertEqual(
            lookup(self.receipt, "bounds_reached.carrier_completed_inside_bound"),
            {"3": True, "4": True},
        )
        self.assertEqual(lookup(self.receipt, "bounds_reached.carrier_refused.carrier"), 5)
        self.assertEqual(
            lookup(self.receipt, "bounds_reached.carrier_refused.terminal"), "REFUSED"
        )

    def test_n4_completed_inside_the_bound(self) -> None:
        self.assertEqual(lookup(self.receipt, "sweeps.N4.relation_total"), 66066)
        self.assertEqual(lookup(self.receipt, "sweeps.N4.pattern_class_total"), 431)
        self.assertTrue(lookup(self.receipt, "sweeps.N4.completed_inside_bound"))
        self.assertEqual(lookup(self.receipt, "sweeps.N3.relation_total"), 530)
        for n in ("N3", "N4"):
            for fragment, size in ((al.PURE, 75), (al.EQ_BEARING, 37), (al.MERGED, 147)):
                self.assertEqual(
                    lookup(self.receipt, f"sweeps.{n}.fragments.{fragment}.lattice.closure_size"),
                    size,
                )
                self.assertFalse(
                    lookup(self.receipt, f"sweeps.{n}.fragments.{fragment}.lattice.truncated")
                )

    def test_terminals(self) -> None:
        terminals = self.receipt["terminals"]
        assert isinstance(terminals, dict)
        lattice_line = str(terminals["lattice"])
        self.assertTrue(lattice_line.startswith("S9_1_LATTICE_COMPLETE"))
        self.assertIn("carriers <= 4", lattice_line)
        self.assertIn("bounded by N = 4", lattice_line)
        f3 = terminals["f3"]
        assert isinstance(f3, dict)
        for fragment in al.FRAGMENTS:
            line = str(lookup(f3, f"{fragment}.TRANSFER_ALL_CARRIERS"))
            self.assertTrue(line.startswith("F3_UNTESTED"))
            self.assertIn(f"in {fragment}", line)
            self.assertIn("same containment", line)
        pure_above = str(lookup(f3, "PURE.TRANSFER_ABOVE_POINT"))
        self.assertTrue(pure_above.startswith("F3_SUPPORTED_BOUNDED"))
        self.assertIn("bounded by N = 4", pure_above)
        self.assertIn("could not have come out otherwise", pure_above)
        self.assertIn("two-point full relation", pure_above)
        for fragment in (al.EQ_BEARING, al.MERGED):
            line = str(lookup(f3, f"{fragment}.TRANSFER_ABOVE_POINT"))
            self.assertTrue(line.startswith("F3_REFUTED"))
            self.assertIn(f"in {fragment}", line)
            self.assertIn("nonempty by construction", line)
            self.assertIn("r x x -> x = y", line)
            self.assertIn("bounded by N = 4", line)
            self.assertIn("discounting the one-point carrier", line)
            # Repair round 2: the string says which bill F3 as written
            # ranges over and which bill the refutation lives in.
            self.assertIn("under A1's bill", line)
            self.assertIn("uses A3's identity atom (uses_eq_atom = true)", line)
            self.assertIn("extended to A3's bill under a soundness weaker than S7's", line)
            self.assertIn("not F3 as written", line)
            self.assertIn("selfdiff_consistent", line)
        for group in ("f3", "transfer"):
            block = terminals[group]
            assert isinstance(block, dict)
            for defn in al.DEFINITIONS:
                merged_line = str(lookup(block, f"{al.MERGED}.{defn.name}"))
                self.assertIn("MERGED_PURE_AND_EQ_BEARING, which merges", merged_line)
                self.assertIn("merge_sentence applies", merged_line)
                pure_line = str(lookup(block, f"{al.PURE}.{defn.name}"))
                self.assertNotIn("merge_sentence", pure_line)
        transfer = terminals["transfer"]
        assert isinstance(transfer, dict)
        for fragment in al.FRAGMENTS:
            for defn in al.DEFINITIONS:
                line = str(lookup(transfer, f"{fragment}.{defn.name}"))
                self.assertTrue(line.startswith("S9_1_TRANSFER_CHARACTERIZED"))
                self.assertIn("bounded by N = 4", line)
                self.assertIn("automatic", line)
        self.assertIn("generated by irreflexivity", str(lookup(transfer, "PURE.TRANSFER_ALL_CARRIERS")))
        self.assertIn("W is NOT in the lattice", str(lookup(transfer, "PURE.TRANSFER_ABOVE_POINT")))
        self.assertIn(
            "NOT generated by irreflexivity",
            str(lookup(transfer, "EQ_BEARING.TRANSFER_ABOVE_POINT")),
        )
        self.assertTrue(str(terminals["refused"]).startswith("REFUSED"))
        # The Lean terminal pair (repair after full-run audit 1): every
        # theorem LEAN_CARRIED names is an audited report of the tree's
        # package, and LEAN_NOT_CARRIED names its bound and its residual.
        lean = terminals["lean"]
        assert isinstance(lean, dict)
        self.assertEqual(sorted(lean), ["LEAN_CARRIED", "LEAN_NOT_CARRIED"])
        carried = str(lean["LEAN_CARRIED"])
        self.assertTrue(carried.startswith("LEAN_CARRIED -- S9.1"))
        self.assertEqual(len(al.LEAN_CARRIED_THEOREMS), 10)
        source = (common.TREE / "lean" / "S9Obligations" / "AxiomLattice.lean").read_text(encoding="utf-8")
        for name in al.LEAN_CARRIED_THEOREMS:
            self.assertIn(name, carried)
            self.assertIn(f"{al.LEAN_MODULE}.{name}", verify_lean.AXIOM_REPORT_DECLARATIONS, name)
            self.assertRegex(source, r"(?m)^theorem " + re.escape(name) + r"\b")
        self.assertIn(al.LEAN_MODULE, carried)
        self.assertNotIn("What blocked", carried)
        not_carried = str(lean["LEAN_NOT_CARRIED"])
        self.assertTrue(not_carried.startswith("LEAN_NOT_CARRIED -- S9.1"))
        self.assertIn("bounded by N = 4", not_carried)
        self.assertIn("no Lean theorem", not_carried)
        self.assertIn("not attempted", not_carried)
        self.assertTrue(
            str(lookup(self.receipt, "eq_fragment.terminal")).startswith("EQ_FRAGMENT_SEPARATED")
        )

    def test_terminal_branches_not_reached_by_the_sweep(self) -> None:
        f3: dict[str, object] = {
            "count": 0,
            "decided_before_the_sweep": {"verdict": "undecided_before_the_sweep"},
        }
        analysis: dict[str, object] = {"f3_set": f3}
        line = al.f3_terminal(al.PURE, al.TRANSFER_ABOVE_POINT, analysis, 4)
        self.assertTrue(line.startswith("F3_SUPPORTED_BOUNDED"))
        self.assertIn("not decided by argument", line)
        f3["count"] = 2
        line = al.f3_terminal(al.MERGED, al.TRANSFER_ABOVE_POINT, analysis, 4)
        self.assertTrue(line.startswith("F3_REFUTED"))
        self.assertIn("not decided by argument", line)
        self.assertIn("merge_sentence applies", line)
        # A refuting set with a member that uses no identity atom would
        # reach A1's bill; the sweep never produces one, so the branch is
        # exercised here.
        f3["decided_before_the_sweep"] = {
            "verdict": "nonempty_by_named_generator",
            "named_generator": "r x x -> x = y",
        }
        f3["members"] = [{"uses_eq_atom": True}, {"uses_eq_atom": False}]
        line = al.f3_terminal(al.EQ_BEARING, al.TRANSFER_ABOVE_POINT, analysis, 4)
        self.assertTrue(line.startswith("F3_REFUTED"))
        self.assertIn("1 of the 2 members use no identity atom", line)
        self.assertIn("reaches A1's bill", line)
        self.assertNotIn("not F3 as written", line)
        open_line = al.transfer_terminal(
            al.PURE,
            al.TRANSFER_ABOVE_POINT,
            {
                "unique_weakest": None,
                "unique_weakest_exists": False,
                "closed_under_strengthening": True,
                "closed_under_meet": True,
                "transfer_as_containment": {"W_in_lattice": False},
            },
            4,
        )
        self.assertTrue(open_line.startswith("S9_1_TRANSFER_OPEN"))
        self.assertIn("bounded by N = 4", open_line)
        conj_line = al.transfer_terminal(
            al.EQ_BEARING,
            al.TRANSFER_ABOVE_POINT,
            {
                "unique_weakest": {"representative_axiom": ["a", "b"]},
                "unique_weakest_exists": True,
                "closed_under_strengthening": True,
                "closed_under_meet": True,
                "generated_by_irreflexivity": False,
                "transfer_as_containment": {"W_in_lattice": True, "W_realized_by_generators": []},
            },
            4,
        )
        self.assertIn("realized in the lattice by a conjunction", conj_line)
        self.assertIn("[a ; b]", conj_line)

    def test_keys_cited_in_the_findings_exist(self) -> None:
        for dotted in (
            "revision",
            "axiom_space.one_variable_meaning",
            "axiom_space.PURE.raw_clause_count",
            "axiom_space.PURE.swap_orbit_count",
            "axiom_space.PURE.head_in_body_count",
            "axiom_space.PURE.nontrivial_swap_orbit_count",
            "axiom_space.PURE.one_variable_clause_count_raw",
            "axiom_space.PURE.one_variable_clauses_raw",
            "axiom_space.PURE.one_variable_swap_orbit_count",
            "axiom_space.PURE.two_variable_clause_count_raw",
            "axiom_space.EQ_BEARING.raw_clause_count",
            "axiom_space.EQ_BEARING.nontrivial_swap_orbit_count",
            "axiom_space.EQ_BEARING.one_variable_clause_count_raw",
            "axiom_space.EQ_BEARING.two_variable_clause_count_raw",
            "transfer_definitions.TRANSFER_ALL_CARRIERS.displayed",
            "transfer_definitions.TRANSFER_ABOVE_POINT.displayed",
            "transfer_definitions.TRANSFER_ABOVE_POINT.why",
            "transfer_definitions.TRANSFER_ALL_CARRIERS.f3_set_empty_by_definitional_identity",
            "transfer_definitions.TRANSFER_ABOVE_POINT.f3_set_empty_by_definitional_identity",
            "entails_irreflexivity",
            "f3_sweep_scope",
            "closure_restriction.PURE.injective",
            "closure_restriction.PURE.distinct_restrictions",
            "closure_restriction.PURE.image_equals_lower_closure",
            "closure_restriction.EQ_BEARING.injective",
            "closure_restriction.MERGED_PURE_AND_EQ_BEARING.injective",
            "closure_restriction.MERGED_PURE_AND_EQ_BEARING.merge_sentence",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment."
            "W_recomputed_from_raw_census_equals_W",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment.meaning",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.f3_set.empty_by_definitional_identity",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.f3_set.flags_meaning",
            "sweeps.N4.fragments.PURE.classifier_audit.TRANSFER_ALL_CARRIERS.row_count",
            "sweeps.N4.fragments.PURE.classifier_audit.TRANSFER_ALL_CARRIERS.rows_are",
            "sweeps.N4.fragments.EQ_BEARING.transfer.TRANSFER_ALL_CARRIERS.closed_under_weakening_witness."
            "transferring.representative_axiom",
            "sweeps.N4.fragments.EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.closed_under_weakening_witness."
            "failure",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.closed_under_weakening_witness.failure",
            "sweeps.N4.fragments.PURE.lean_target_evidence."
            "T1_atom_headed_generators_admit_full_relation_on_carriers_1_to_N",
            "order.stronger",
            "order.principal_downset",
            "sweeps.N4.fragments.PURE.generators.valid_by_extent_count",
            "sweeps.N4.fragments.EQ_BEARING.generators.valid_by_extent_count",
            "sweeps.N4.fragments.PURE.single_clause_extents.extent_class_count",
            "sweeps.N4.fragments.PURE.lattice.transferring_iff_representative_has_falsum_head",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ALL_CARRIERS.transferring_count",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.f3_set.members",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.f3_set.decided_before_the_sweep.verdict",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.f3_set.decided_before_the_sweep."
            "premises_checked_at_N.one_point_full_implies_two_point_full_on_lattice",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment.W_in_lattice",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment."
            "transferring_equals_lattice_extents_contained_in_W",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment."
            "W_minus_irreflexivity_extent.relations",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment.W_size_by_carrier",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ABOVE_POINT.unique_weakest_equals_W",
            "sweeps.N4.fragments.EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.unique_weakest",
            "sweeps.N4.fragments.EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.f3_set.count",
            "sweeps.N4.fragments.EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.f3_set.nonempty_by_construction",
            "sweeps.N4.fragments.EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.f3_set.decided_before_the_sweep."
            "named_generator",
            "sweeps.N4.fragments.EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment."
            "W_realized_by_generators",
            "sweeps.N4.fragments.MERGED_PURE_AND_EQ_BEARING.merge_sentence",
            "sweeps.N4.fragments.MERGED_PURE_AND_EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.f3_set.count",
            "sweeps.N4.fragments.PURE.classifier_audit.TRANSFER_ALL_CARRIERS.defect",
            "sweeps.N4.fragments.PURE.classifier_audit.TRANSFER_ABOVE_POINT.transferring_count",
            "sweeps.N4.fragments.EQ_BEARING.classifier_audit.TRANSFER_ABOVE_POINT.non_transferring_count",
            "sweeps.N4.fragments.PURE.transfer.TRANSFER_ALL_CARRIERS.closed_under_weakening_witness",
            "axiom_space.PURE.swap_fixed_clause_count",
            "axiom_space.PURE.head_in_body_policy",
            "declared_bounds.raw_clause_count_arithmetic",
            "bounds_reached.carrier_refused.relations_that_would_be_added",
            "sweeps.N3.fragments.PURE.lattice.closure_size",
            "sweeps.N4.fragments.PURE.generators.valid_by_extent_clauses",
            "sweeps.N4.fragments.PURE.lattice.top_is_empty_axiom",
            "sweeps.N4.fragments.PURE.lattice.bottom_is_empty_extent",
            "sweeps.N4.fragments.PURE.lattice.irreflexivity_extent_size_by_carrier",
            "sweeps.N4.fragments.PURE.lean_target_evidence."
            "T7_lattice_extents_admitting_one_point_full_and_transferring_above_point",
            "sweeps.N4.fragments.EQ_BEARING.lean_target_evidence."
            "T6_reflexive_point_forces_singleton.transfers_above_point",
            "terminals.transfer.EQ_BEARING.TRANSFER_ABOVE_POINT",
            "terminals.f3.PURE.TRANSFER_ABOVE_POINT",
            "terminals.f3.MERGED_PURE_AND_EQ_BEARING.TRANSFER_ABOVE_POINT",
            "terminals.refused",
            "terminals.lean",
        ):
            lookup(self.receipt, dotted)

    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=common.TREE) as scratch:
            first = Path(scratch) / "a"
            second = Path(scratch) / "b"
            with contextlib.redirect_stdout(io.StringIO()) as captured:
                self.assertEqual(run_axiom_lattice.main(["--out", str(first)]), 0)
                self.assertEqual(run_axiom_lattice.main(["--out", str(second)]), 0)
            one = (first / run_axiom_lattice.RECEIPT_NAME).read_bytes()
            two = (second / run_axiom_lattice.RECEIPT_NAME).read_bytes()
        printed = captured.getvalue()
        self.assertIn("stronger: a SMALLER extent is a STRONGER axiom", printed)
        self.assertIn("f3 set: [] (decided before the sweep: empty_by_lemma)", printed)
        self.assertIn("[r x x -> x = y] sizes", printed)
        self.assertIn(
            "closure restriction PURE: N4 -> N3: 75 extents, 75 distinct restrictions, "
            "injective True, image equals lower closure True",
            printed,
        )
        self.assertEqual(one, two)
        self.assertNotIn(b"\r", one)
        self.assertTrue(one.endswith(b"}\n"))
        one.decode("ascii")
        self.assertEqual(one, common.receipt_bytes(self.receipt))
        committed = common.TREE / "receipts" / run_axiom_lattice.RECEIPT_NAME
        self.assertTrue(committed.exists(), "run run_axiom_lattice.py --out receipts first")
        self.assertEqual(committed.read_bytes(), one, "committed receipt is stale")

    def test_closure_restriction_from_n4_onto_n3(self) -> None:
        restriction = self.receipt["closure_restriction"]
        assert isinstance(restriction, dict)
        self.assertEqual(sorted(k for k in restriction if k != "meaning"), sorted(al.FRAGMENTS))
        for fragment, size in ((al.PURE, 75), (al.EQ_BEARING, 37), (al.MERGED, 147)):
            block = lookup(restriction, fragment)
            self.assertEqual(lookup(block, "from_carrier"), 4)
            self.assertEqual(lookup(block, "to_carrier"), 3)
            self.assertEqual(lookup(block, "upper_closure_size"), size)
            self.assertEqual(lookup(block, "lower_closure_size"), size)
            self.assertEqual(lookup(block, "distinct_restrictions"), size)
            self.assertTrue(lookup(block, "injective"))
            self.assertTrue(lookup(block, "image_equals_lower_closure"))
            self.assertTrue(lookup(block, "bounded"))
            self.assertEqual(lookup(block, "bound_reached"), 4)
            self.assertFalse(lookup(block, "truncated"))
        assert isinstance(restriction[al.MERGED], dict)
        self.assertEqual(restriction[al.MERGED]["merge_sentence"], al.MERGE_SENTENCE)
        assert isinstance(restriction[al.PURE], dict)
        self.assertNotIn("merge_sentence", restriction[al.PURE])
        # With one bound only, nothing is restricted and the key says so.
        single = al.build_receipt(required=3, attempted=3)
        only = single["closure_restriction"]
        assert isinstance(only, dict)
        self.assertEqual(sorted(only), ["meaning"])

    def test_runner_refuses_an_out_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            with contextlib.redirect_stdout(io.StringIO()) as captured:
                self.assertEqual(run_axiom_lattice.main(["--out", outside]), 1)
            self.assertIn("refusing to write outside", captured.getvalue())
            self.assertFalse((Path(outside) / run_axiom_lattice.RECEIPT_NAME).exists())


class ForbiddenClosureTests(unittest.TestCase):
    """Negative tests for PROMPT.md steps 36, 37, 39, 40 (step 34), scoped to
    P1's five files.  Each checker is shown to bite on an injected string
    built at runtime, so no forbidden text is written into this file.  The
    step-37 and step-40 checkers are heuristics and are declared as such."""

    def read(self, name: str) -> str:
        return (common.TREE / name).read_bytes().decode("ascii")

    def test_p1_files_are_ascii_and_lf_only(self) -> None:
        for name in P1_FILES:
            raw = (common.TREE / name).read_bytes()
            raw.decode("ascii")
            self.assertNotIn(b"\r", raw, name)

    def test_step39_denylist_identifiers_absent_from_p1_files(self) -> None:
        denylist = working_denylist()
        self.assertEqual(len(denylist), 102)
        for name in P1_FILES:
            self.assertEqual(denylist_leaks(self.read(name), denylist), [], name)
        injected = f"def probe():\n    return {sorted(denylist)[0]}\n"
        self.assertEqual(denylist_leaks(injected, denylist), [sorted(denylist)[0]])
        self.assertEqual(denylist_leaks("a b c", {"zzz"}), [])

    def test_step36_protected_opens_only_inside_a_scope_sentence(self) -> None:
        text = self.read("P1_FINDINGS.md")
        self.assertTrue(any(name in text for name in PROTECTED_OPENS))
        self.assertEqual(protected_open_violations(text), [])
        injected = text + "\n" + PROTECTED_OPENS[0] + " is closed by this part.\n"
        self.assertEqual(
            protected_open_violations(injected), [PROTECTED_OPENS[0] + " is closed by this part."]
        )

    def test_step37_carrier_general_sentences_carry_a_bound_or_a_proposal(self) -> None:
        text = self.read("P1_FINDINGS.md")
        self.assertEqual(carrier_general_violations(text), [])
        # Repair round 2: the population is every key and every string value
        # of the receipt, not only the eighteen terminal strings.
        receipt = json.loads(self.read("receipts/axiom_lattice.json"))
        strings = receipt_strings(receipt)
        self.assertGreater(len(strings), 1000)
        self.assertTrue(any(path.endswith(".why") for path, _ in strings))
        self.assertTrue(any(path == ".f3_sweep_scope" for path, _ in strings))
        for path, value in strings:
            self.assertEqual(carrier_general_violations(value), [], path)
        injected = "The transferring axioms are generated by irreflexivity on every carrier."
        self.assertEqual(carrier_general_violations(injected), [injected])
        self.assertEqual(
            carrier_general_violations(injected.replace(".", ", bounded by N = 4.")), []
        )
        # The round-2 phrases bite on the lemma stated without its bound, and
        # a word-bounded "at N" or "N = 4" in the same unit is a bound.
        lemma = "No pure clause separates the one-point full relation from the two-point one."
        self.assertEqual(carrier_general_violations(lemma), [lemma])
        self.assertEqual(carrier_general_violations(lemma.replace(".", ", checked at N.")), [])
        self.assertEqual(carrier_general_violations(lemma.replace(".", " at N = 4.")), [])
        self.assertEqual(carrier_general_violations("Note that no pure clause does."), ["Note that no pure clause does."])
        extents = "Every lattice extent admitting the one-point full relation fails above the point."
        self.assertEqual(carrier_general_violations(extents), [extents])

    def test_step40_no_external_citation_markers(self) -> None:
        for name in P1_FILES:
            if name == "test_axiom_lattice.py":
                continue  # this file holds the marker list itself
            self.assertEqual(external_markers(self.read(name)), [], name)
        self.assertEqual(external_markers("see https" + "://x"), ["http" + "s://"])


if __name__ == "__main__":
    unittest.main()
