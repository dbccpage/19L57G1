"""Tests for P3 (PROMPT.md step 34): vocabulary sizes, the separating and
invisible pairs re-checked by evaluating every question on the reported
pairs, every ``first_*`` key re-derived by an independent scan in
enumeration order (round-1 repair), every count re-derived by a full pair
loop on the small spaces, the refusals, the per-cell bound rule,
deterministic enumeration order, byte-identical replay, the vocabulary
firewall over this part's own files, and the negative scans over
P3_FINDINGS.md for the forbidden closures of PROMPT.md steps 36, 37, and
40 plus a resolver for every receipt key the findings cite.  Round-2
repairs: the denial stripping is narrowed to the denial phrase, the
step-37 phrase list names phrases that reach past the bound, the
write-root probe never hands the writer a sealed path, and the
count-equal non-isomorphic pairs split by invariant are re-derived.

AuthorityEffect: None.  A green run here is a receipt for the code, not a
discharged obligation."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Callable

import common
import verify_lean
import witness_types as wt

Assignment = tuple[int, ...]

P3_FILES = (
    "witness_types.py",
    "run_witness_types.py",
    "test_witness_types.py",
    "receipts/witness_types.json",
    "P3_FINDINGS.md",
)
FINDINGS_PATH = common.TREE / "P3_FINDINGS.md"
PROMPT_PATH = common.TREE / "PROMPT.md"
RECEIPT_PATH = common.TREE / "receipts" / "witness_types.json"

FIRST_KEYS = (
    "first_pair",
    "first_non_isomorphic_pair",
    "first_non_isomorphic_count_equal_pair",
    "first_non_isomorphic_pair_no_invariant_differs",
)

# Spaces small enough for a full pair loop (every pair of assignments
# compared directly, no bucketing).
FULL_LOOP_AT_MOST = 200

# The (3, 2) witnessed space takes seconds to key and canonicalize; the
# independent re-derivations share one SpaceData per space.
_SPACE_DATA: dict[tuple[int, int, str], "SpaceData"] = {}


def space_data(n: int, t: int, space: str) -> "SpaceData":
    key = (n, t, space)
    if key not in _SPACE_DATA:
        _SPACE_DATA[key] = SpaceData(n, t, space)
    return _SPACE_DATA[key]


def as_dict(obj: object) -> dict[str, object]:
    assert isinstance(obj, dict)
    return obj


def as_list(obj: object) -> list[object]:
    assert isinstance(obj, list)
    return obj


def as_int(obj: object) -> int:
    assert isinstance(obj, int) and not isinstance(obj, bool)
    return obj


def masks_of(rendered: object) -> Assignment:
    return tuple(as_int(m) for m in as_list(as_dict(rendered)["masks"]))


def pair_of(rendered: object) -> tuple[Assignment, Assignment] | None:
    if rendered is None:
        return None
    return masks_of(as_dict(rendered)["left"]), masks_of(as_dict(rendered)["right"])


def enumerated_spaces() -> list[tuple[int, int, str]]:
    return [(n, t, space) for n, t in wt.CELLS if wt.cell_is_enumerated(n, t) for space in wt.SPACES]


# ---------------------------------------------------------------------------
# Negative scans (PROMPT.md steps 36, 37, 40), written here rather than
# borrowed from another part's test module.
# ---------------------------------------------------------------------------

# scanner-definitions-begin (this block is cut out of the test module's own
# text before the external-marker scan runs over it)
PROTECTED = r"(?:OB-1|S6\.6|(?:the\s+)?inscription\s+bridge|S9\s+last\s+bullet)"
VERBS = r"(?:clos(?:ing|ed|es|e)|narrow(?:ing|ed|s)?|pric(?:ing|ed|es|e))"
CLAIM_PATTERNS = (
    re.compile(PROTECTED + r"\s+(?:is|was|are|were|has\s+been|have\s+been|now)?\s*" + VERBS, re.I),
    re.compile(VERBS + r"\s+(?:the\s+)?" + PROTECTED, re.I),
)
# A denial is stripped as the phrase itself (with the list of verbs it
# denies and, where it names one, the protected open it is about) and
# nothing more.  Round-2 repair: the old pattern consumed the rest of the
# sentence, so "OB-1 is not closed here, but this part narrows OB-1 anyway"
# was invisible to the claim patterns.
DENIED_VERBS = (
    r"(?:closed|narrowed|priced)(?:\s*,\s*(?:closed|narrowed|priced))*"
    r"(?:\s*,?\s*(?:or|and|nor)\s+(?:closed|narrowed|priced))?"
)
DENIALS = re.compile(
    r"(?:makes?\s+no\s+claim\s+about\s+(?:the\s+)?" + PROTECTED + r"|"
    r"does\s+not\s+(?:claim|close|narrow|price)(?:\s+(?:the\s+)?" + PROTECTED + r")?|"
    r"not\s+" + DENIED_VERBS + r"|"
    r"none\s+(?:is|of\s+them\s+is)\s+" + DENIED_VERBS + r"|"
    r"neither\s+" + DENIED_VERBS + r"|"
    r"nor\s+" + DENIED_VERBS + r")",
    re.I,
)

# Phrases that promote a bounded sweep to a carrier-general claim (step 37).
GENERAL_PHRASES = (
    "for all carriers",
    "for every carrier",
    "for every finite carrier",
    "for all n",
    "for all t",
    "for any carrier",
    "for any n",
    "for any t",
    "every token domain",
    "all token domains",
    "in general",
    "holds generally",
    "for arbitrary",
    # round-2 repair: a one-cell observation projected onto every larger cell
    "from t = 2 on",
    "from t = 3 on",
    "from n = 2 on",
    "from n = 3 on",
    "for t >=",
    "for n >=",
    "for every t",
    "for every n",
    "and beyond",
    "onward",
    "onwards",
)
GENERAL_NEGATION = re.compile(r"\b(?:no|not|nothing|none|never|forbidden)\b", re.I)

# Markers of an external name, citation, or appeal (step 40).
EXTERNAL_MARKERS = (
    "http://",
    "https://",
    "www.",
    "et al",
    "well-known",
    "well known",
    "standard result",
    "literature",
    "textbook",
    "folklore",
    "arxiv",
    "doi:",
    "cf.",
    "see also",
    "known as",
    "classical result",
)

# Words the house rule restricts to a proof or a precise scope.  The first
# group is not used at all in this part's prose; the second may appear only
# in a sentence that also names its scope.
UNSCOPED_WORDS = re.compile(r"\b(?:canonical|forced|universal|equivalent|free)\b", re.I)
SCOPED_WORDS = re.compile(r"\b(?:complete(?:ly)?|minimal)\b", re.I)
SCOPE_MARKERS = re.compile(r"(?:declared|enumerated|bound|whole|within|N = |T = |cells? \()", re.I)


def flatten(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", flatten(text)) if s.strip()]


def protected_open_claims(text: str) -> list[str]:
    stripped = DENIALS.sub("", flatten(text))
    hits: list[str] = []
    for pattern in CLAIM_PATTERNS:
        hits.extend(match.group(0) for match in pattern.finditer(stripped))
    return hits


def carrier_general_phrases(text: str) -> list[str]:
    hits: list[str] = []
    for sentence in sentences(text):
        low = sentence.lower()
        for phrase in GENERAL_PHRASES:
            if re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", low):
                hits.append(phrase)
        if "carrier-general" in low and not GENERAL_NEGATION.search(sentence):
            hits.append("carrier-general (unnegated)")
    return hits


def external_markers(text: str) -> list[str]:
    """Markers matched as whole tokens on their word-character ends, so a
    marker inside a longer word does not fire."""

    low = text.lower()
    hits: list[str] = []
    for m in EXTERNAL_MARKERS:
        pattern = (r"(?<!\w)" if m[0].isalnum() else "") + re.escape(m) + (r"(?!\w)" if m[-1].isalnum() else "")
        if re.search(pattern, low):
            hits.append(m)
    return hits


def unscoped_words(text: str) -> list[str]:
    hits: list[str] = []
    for sentence in sentences(text):
        hits.extend(m.group(0) for m in UNSCOPED_WORDS.finditer(sentence))
        if SCOPED_WORDS.search(sentence) and not SCOPE_MARKERS.search(sentence):
            hits.append(f"unscoped: {sentence[:60]}")
    return hits


# scanner-definitions-end


def json_strings(obj: object) -> list[str]:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        out: list[str] = []
        for k, v in obj.items():
            out.append(str(k))
            out.extend(json_strings(v))
        return out
    if isinstance(obj, list):
        return [s for item in obj for s in json_strings(item)]
    return []


def receipt_paths(obj: object, prefix: str = "") -> tuple[set[str], set[str]]:
    """Every dotted path in a receipt (list indices as ``key[i]``) and
    every dict key name."""

    paths: set[str] = set()
    names: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            names.add(str(k))
            here = f"{prefix}.{k}" if prefix else str(k)
            paths.add(here)
            sub_paths, sub_names = receipt_paths(v, here)
            paths |= sub_paths
            names |= sub_names
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            here = f"{prefix}[{i}]"
            paths.add(here)
            sub_paths, sub_names = receipt_paths(v, here)
            paths |= sub_paths
            names |= sub_names
    return paths, names


def legal_terminals() -> set[str]:
    text = PROMPT_PATH.read_text(encoding="utf-8")
    start = text.index("## Legal terminals")
    end = text.index("---", start)
    return set(re.findall(r"^\s+([A-Z][A-Z0-9_]+)\s*$", text[start:end], re.M))


# ---------------------------------------------------------------------------
# Independent re-derivations: a scan in enumeration order for every first_*
# key, and a full pair loop for every count on the small spaces.  Neither
# uses bucketing, group order, or ``invisible_pairs``.
# ---------------------------------------------------------------------------


class SpaceData:
    def __init__(self, n: int, t: int, space: str) -> None:
        self.n, self.t = n, t
        self.assignments = list(wt.enumerate_space(n, t, space))
        self.size = len(self.assignments)
        generic = self.size <= 4000
        keyer = wt.Keyer(n, t)
        self.keys: dict[str, list[int]] = {}
        for name in wt.VOCABULARIES:
            if generic:
                vocab = wt.vocabulary(name, n, t)
                self.keys[name] = [wt.answer_vector(vocab, a, n) for a in self.assignments]
            else:
                self.keys[name] = [keyer.keys(a)[name] for a in self.assignments]
        transporter = wt.Transporter(n, t)
        self.canon = [transporter.least_transport(a) for a in self.assignments]
        self.counts = [tuple(wt.count_vector(a)) for a in self.assignments]
        self.inv = [wt.invariant_tuple(a, t) for a in self.assignments]

    def first_where(
        self, keys: list[int], cond: Callable[[int, int], bool]
    ) -> tuple[Assignment, Assignment] | None:
        for i in range(self.size):
            ki = keys[i]
            for j in range(i + 1, self.size):
                if keys[j] == ki and cond(i, j):
                    return self.assignments[i], self.assignments[j]
        return None

    def first_separating(self, coarse: str, fine: str) -> tuple[Assignment, Assignment] | None:
        kf = self.keys[fine]
        return self.first_where(self.keys[coarse], lambda i, j: kf[i] != kf[j])

    def conditions(self) -> dict[str, Callable[[int, int], bool]]:
        canon, counts, inv = self.canon, self.counts, self.inv
        return {
            "first_pair": lambda i, j: True,
            "first_non_isomorphic_pair": lambda i, j: canon[i] != canon[j],
            "first_non_isomorphic_count_equal_pair": lambda i, j: canon[i] != canon[j]
            and counts[i] == counts[j],
            "first_non_isomorphic_pair_no_invariant_differs": lambda i, j: canon[i] != canon[j]
            and inv[i] == inv[j],
        }

    def no_pair_by_grouping(self, vocab: str, key: str) -> bool:
        """Independent check that no qualifying pair exists, by grouping
        rather than scanning: every group holds one isomorphism class."""

        keys = self.keys[vocab]
        groups: dict[tuple[object, ...], set[Assignment]] = {}
        for i in range(self.size):
            if key == "first_pair" or key == "first_non_isomorphic_pair":
                g: tuple[object, ...] = (keys[i],)
            elif key == "first_non_isomorphic_count_equal_pair":
                g = (keys[i], self.counts[i])
            else:
                g = (keys[i], self.inv[i])
            groups.setdefault(g, set()).add(self.canon[i])
        if key == "first_pair":
            return len(groups) == self.size
        return all(len(classes) == 1 for classes in groups.values())

    def full_loop(self, vocab: str) -> dict[str, object]:
        """Every invisible-pair count and first pair of one vocabulary by a
        direct double loop over the space."""

        keys, canon, counts, inv = self.keys[vocab], self.canon, self.counts, self.inv
        totals = {
            "pair_count": 0,
            "isomorphic_pair_count": 0,
            "non_isomorphic_pair_count": 0,
            "non_isomorphic_count_equal_pair_count": 0,
        }
        by_invariant = {name: 0 for name in wt.INVARIANTS}
        by_invariant["none_of_the_computed_invariants"] = 0
        by_invariant_count_equal = {name: 0 for name in wt.COUNT_EQUAL_INVARIANTS}
        by_invariant_count_equal["none_of_the_computed_invariants"] = 0
        firsts: dict[str, tuple[Assignment, Assignment] | None] = {k: None for k in FIRST_KEYS}
        conds = self.conditions()
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if keys[i] != keys[j]:
                    continue
                pair = (self.assignments[i], self.assignments[j])
                totals["pair_count"] += 1
                if canon[i] == canon[j]:
                    totals["isomorphic_pair_count"] += 1
                else:
                    totals["non_isomorphic_pair_count"] += 1
                    if counts[i] == counts[j]:
                        totals["non_isomorphic_count_equal_pair_count"] += 1
                    differing = [name for k, name in enumerate(wt.INVARIANTS) if inv[i][k] != inv[j][k]]
                    for name in differing:
                        by_invariant[name] += 1
                        if counts[i] == counts[j] and name in by_invariant_count_equal:
                            by_invariant_count_equal[name] += 1
                    if not differing:
                        by_invariant["none_of_the_computed_invariants"] += 1
                        if counts[i] == counts[j]:
                            by_invariant_count_equal["none_of_the_computed_invariants"] += 1
                for k in FIRST_KEYS:
                    if firsts[k] is None and conds[k](i, j):
                        firsts[k] = pair
        return {
            **totals,
            "by_invariant": by_invariant,
            "by_invariant_count_equal": by_invariant_count_equal,
            "firsts": firsts,
        }

    def count_equal_by_invariant_by_groups(self, vocab: str) -> tuple[int, dict[str, int]]:
        """Round-2 repair, independent of ``invisible_pairs``: group by
        (answer vector, count vector), then a direct double loop inside
        each group; returns the count-equal non-isomorphic pair total and
        how many of those pairs differ in each non-count invariant."""

        keys, canon, counts, inv = self.keys[vocab], self.canon, self.counts, self.inv
        groups: dict[tuple[int, tuple[int, ...]], list[int]] = {}
        for i in range(self.size):
            groups.setdefault((keys[i], counts[i]), []).append(i)
        by = {name: 0 for name in wt.COUNT_EQUAL_INVARIANTS}
        by["none_of_the_computed_invariants"] = 0
        total = 0
        for members in groups.values():
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    i, j = members[a], members[b]
                    if canon[i] == canon[j]:
                        continue
                    total += 1
                    differing = [name for k, name in enumerate(wt.INVARIANTS) if inv[i][k] != inv[j][k]]
                    for name in differing:
                        if name in by:
                            by[name] += 1
                    if not differing:
                        by["none_of_the_computed_invariants"] += 1
        return total, by

    def separating_count(self, coarse: str, fine: str) -> int:
        kc, kf = self.keys[coarse], self.keys[fine]
        return sum(
            1
            for i in range(self.size)
            for j in range(i + 1, self.size)
            if kc[i] == kc[j] and kf[i] != kf[j]
        )


class VocabularyTests(unittest.TestCase):
    def test_sizes_match_the_declared_formulas_in_every_cell(self) -> None:
        for n, t in wt.CELLS:
            for name in wt.VOCABULARIES:
                self.assertEqual(
                    len(wt.vocabulary(name, n, t)),
                    wt.vocabulary_size_formula(name, n, t),
                    (name, n, t),
                )
        self.assertEqual(len(wt.vocabulary("V0", 2, 2)), 4)
        self.assertEqual(len(wt.vocabulary("V1", 2, 2)), 22)
        self.assertEqual(len(wt.vocabulary("V2_ANON", 2, 2)), 10)
        self.assertEqual(len(wt.vocabulary("V2_NAMED", 2, 2)), 12)
        self.assertEqual(len(wt.vocabulary("V1", 3, 3)), 117)

    def test_no_question_argument_is_a_map_and_kinds_are_declared(self) -> None:
        kinds = {"presence", "count_eq", "count_lt", "share", "token_at"}
        for n, t in wt.CELLS:
            for name in wt.VOCABULARIES:
                for q in wt.vocabulary(name, n, t):
                    self.assertIn(q.kind, kinds)
                    self.assertTrue(all(isinstance(x, int) for x in q.args))
                    self.assertTrue(q.text())
        with self.assertRaises(KeyError):
            wt.vocabulary("V3", 2, 2)

    def test_fast_keys_equal_generic_answer_vectors(self) -> None:
        """Whole cells (2, 2) and (2, 3) in both spaces, and the (3, 2)
        witnessed_irreflexive space; the (3, 2) witnessed space (196608
        assignments) is not compared generically here -- its rendered
        pairs are re-checked question by question by the receipt tests."""

        for n, t, space in ((2, 2, "witnessed"), (2, 2, "witnessed_irreflexive"),
                            (2, 3, "witnessed"), (2, 3, "witnessed_irreflexive"),
                            (3, 2, "witnessed_irreflexive")):
            keyer = wt.Keyer(n, t)
            vocab = {name: wt.vocabulary(name, n, t) for name in wt.VOCABULARIES}
            for a in wt.enumerate_space(n, t, space):
                keys = keyer.keys(a)
                for name in wt.VOCABULARIES:
                    self.assertEqual(keys[name], wt.answer_vector(vocab[name], a, n), (n, t, name, a))

    def test_refusals_raise_by_name(self) -> None:
        for construction, device, _why in wt.REFUSED_CONSTRUCTIONS:
            with self.assertRaises(wt.BelowFunctionSpaces) as ctx:
                wt.refuse(construction)
            self.assertIn(construction, str(ctx.exception))
            self.assertIn("refused by name", str(ctx.exception))
            self.assertIn(device, wt.BELOW_FUNCTION_SPACES_FORBIDS)
        with self.assertRaises(KeyError):
            wt.refuse("a construction nobody declared")
        with self.assertRaises(wt.BelowFunctionSpaces):
            wt.refuse_map_as_datum("probe")
        with self.assertRaises(wt.BelowFunctionSpaces):
            wt.refuse_composition("probe")
        with self.assertRaises(wt.BelowFunctionSpaces):
            wt.refuse_quotient("probe")
        devices = {device for _c, device, _w in wt.REFUSED_CONSTRUCTIONS}
        self.assertEqual(devices, set(wt.BELOW_FUNCTION_SPACES_FORBIDS))


class EnumerationTests(unittest.TestCase):
    def test_declared_counts_match_the_enumeration(self) -> None:
        for n, t, space in enumerated_spaces():
            self.assertEqual(
                sum(1 for _ in wt.enumerate_space(n, t, space)),
                wt.declared_assignment_count(n, t, space),
            )
        self.assertEqual(wt.declared_assignment_count(2, 2, "witnessed"), 192)
        self.assertEqual(wt.declared_assignment_count(2, 2, "witnessed_irreflexive"), 12)
        self.assertEqual(wt.declared_assignment_count(3, 2, "witnessed"), 196608)
        self.assertEqual(wt.declared_assignment_count(3, 3, "witnessed"), 117440512)
        self.assertEqual(wt.declared_assignment_count(3, 3, "witnessed_irreflexive"), 229376)
        self.assertEqual(wt.full_space_count(3, 3), 134217728)
        self.assertEqual(wt.full_space_count(2, 2), 256)

    def test_bound_rule_is_per_cell(self) -> None:
        """PREFLIGHT.md step 4, P3: the cell's declared assignment space is
        the witnessed space; a cell over the bound is enumerated in no
        space, even one whose own count is inside the number."""

        for n, t in wt.CELLS:
            self.assertEqual(wt.declared_cell_assignment_count(n, t), wt.declared_assignment_count(n, t, "witnessed"))
            self.assertEqual(wt.cell_is_enumerated(n, t), wt.declared_cell_assignment_count(n, t) <= wt.ASSIGNMENT_BOUND)
        self.assertEqual([c for c in wt.CELLS if wt.cell_is_enumerated(*c)], [(2, 2), (2, 3), (3, 2)])
        self.assertFalse(wt.cell_is_enumerated(3, 3))
        self.assertLess(wt.declared_assignment_count(3, 3, "witnessed_irreflexive"), wt.ASSIGNMENT_BOUND)
        self.assertEqual(wt.DECLARED_BOUNDS["rule_unit"], "cell")
        self.assertIn("per SPACE", str(wt.DECLARED_BOUNDS["withdrawn_application"]))

    def test_order_is_lexicographic_and_deterministic(self) -> None:
        for n, t in ((2, 2), (2, 3), (3, 2)):
            for space in wt.SPACES:
                first = list(wt.enumerate_space(n, t, space))
                second = list(wt.enumerate_space(n, t, space))
                self.assertEqual(first, second)
                self.assertEqual(first, sorted(first))
                self.assertEqual(len(set(first)), len(first))
                self.assertTrue(all(wt.is_witnessed(a, n) for a in first))
                if space == "witnessed_irreflexive":
                    self.assertTrue(all(wt.is_irreflexive(a, n) for a in first))
        self.assertEqual(next(wt.enumerate_space(2, 2, "witnessed")), (0, 1, 0, 0))

    def test_bounds_are_refused_by_name(self) -> None:
        with self.assertRaises(ValueError) as c1:
            next(wt.enumerate_space(4, 2, "witnessed"))
        self.assertIn("N = 4", str(c1.exception))
        with self.assertRaises(ValueError) as c2:
            next(wt.enumerate_space(2, 4, "witnessed"))
        self.assertIn("T = 4", str(c2.exception))
        with self.assertRaises(ValueError) as c3:
            next(wt.enumerate_space(3, 3, "witnessed"))
        self.assertIn("117440512", str(c3.exception))
        with self.assertRaises(ValueError) as c4:
            next(wt.enumerate_space(3, 3, "witnessed_irreflexive"))
        self.assertIn("per cell", str(c4.exception))
        self.assertIn("229376", str(c4.exception))
        self.assertIn("117440512", str(c4.exception))
        with self.assertRaises(KeyError):
            wt.declared_assignment_count(2, 2, "everything")
        with self.assertRaises(KeyError):
            next(wt.enumerate_space(2, 2, "everything"))

    def test_transporter_agrees_with_transport_and_least_transport(self) -> None:
        n, t = 2, 3
        transporter = wt.Transporter(n, t)
        for a in wt.enumerate_space(n, t, "witnessed_irreflexive"):
            expected = sorted(
                wt.transport(a, n, f, tau)
                for f in wt.carrier_bijections_fixing_designated(n)
                for tau in wt.token_bijections(t)
            )
            self.assertEqual(sorted(transporter.transports(a)), expected)
            self.assertEqual(transporter.least_transport(a), wt.least_transport(a, n, t))
        self.assertEqual(wt.carrier_bijections_fixing_designated(3), [(0, 1, 2)])
        self.assertEqual(len(wt.token_bijections(3)), 6)

    def test_invariants_are_constant_on_isomorphism_classes(self) -> None:
        n, t = 2, 3
        seen: dict[Assignment, tuple[tuple[int, ...], ...]] = {}
        for a in wt.enumerate_space(n, t, "witnessed"):
            c = wt.least_transport(a, n, t)
            inv = wt.invariant_tuple(a, t)
            self.assertEqual(seen.setdefault(c, inv), inv)
            self.assertEqual(wt.family_isomorphic_metatheory(a, c, n, t), True)
        # {t0,t1} at (0,1) and {t0,t2} at (1,0): counts (0,2,2,0); the one
        # nonzero intersection is |{t0,t1} & {t0,t2}| = 1 at pair-of-pairs
        # index 3 of the 6; t0 occurs twice, t1 and t2 once; common token t0.
        self.assertEqual(
            wt.invariant_tuple((0, 3, 5, 0), 3),
            ((0, 2, 2, 0), (0, 0, 0, 1, 0, 0), (1, 1, 2), (1,)),
        )

    def test_family_isomorphism_matches_least_transports(self) -> None:
        n, t = 2, 2
        space = list(wt.enumerate_space(n, t, "witnessed_irreflexive"))
        for a in space:
            for b in space:
                self.assertEqual(
                    wt.family_isomorphic_metatheory(a, b, n, t),
                    wt.least_transport(a, n, t) == wt.least_transport(b, n, t),
                )
        self.assertTrue(wt.family_isomorphic_metatheory((0, 1, 1, 0), (0, 2, 2, 0), n, t))
        self.assertFalse(wt.family_isomorphic_metatheory((0, 1, 1, 0), (0, 1, 2, 0), n, t))

    def test_least_pair_takes_the_minimum_not_the_first(self) -> None:
        self.assertEqual(wt.least_pair(None, (5, 9)), (5, 9))
        self.assertEqual(wt.least_pair((5, 9), None), (5, 9))
        self.assertEqual(wt.least_pair((5, 9), (3, 40)), (3, 40))
        self.assertEqual(wt.least_pair((3, 40), (5, 9)), (3, 40))
        self.assertEqual(wt.least_pair((3, 40), (3, 7)), (3, 7))
        self.assertIsNone(wt.least_pair(None, None))

    def test_lean_definition_renders_each_occurrence_once(self) -> None:
        text = wt.lean_definition("W1", (0, 1, 1, 0), 2, 2)
        self.assertIn("Fin 2", text)
        self.assertEqual(text.count("=> true"), 2)
        self.assertIn("| false, true, 0 => true", text)
        self.assertIn("| true, false, 0 => true", text)
        with self.assertRaises(ValueError):
            wt.lean_definition("W", (0,) * 9, 3, 2)

    def test_write_root_guard_refuses_a_directory_outside_the_tree(self) -> None:
        """Round-2 repair.  The guard is exercised on the resolver alone,
        which writes nothing, and on the writer with an empty directory
        under the OS temporary root -- outside the tree, outside the
        repository, and not a sealed path -- so that on the defect this
        test exists to catch, a guard that lets a path through, the writer
        cannot touch a sealed path.  The old probe passed the writer
        ``artifacts/`` itself."""

        with self.assertRaises(ValueError) as c1:
            common.assert_inside_tree(common.REPO / "artifacts")
        self.assertIn("refusing to write outside", str(c1.exception))
        outside = Path(tempfile.mkdtemp(prefix="tmp_p3_outside_probe_"))
        try:
            self.assertFalse(outside.resolve().is_relative_to(common.TREE))
            self.assertFalse(outside.resolve().is_relative_to(common.REPO))
            with self.assertRaises(ValueError):
                wt.write(str(outside))
            self.assertEqual(list(outside.iterdir()), [])
        finally:
            shutil.rmtree(outside)


class ReceiptTests(unittest.TestCase):
    receipt: dict[str, object]
    committed: bytes

    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = wt.build_receipt()
        cls.committed = RECEIPT_PATH.read_bytes()

    def cell(self, key: str) -> dict[str, object]:
        return as_dict(as_dict(self.receipt["cells"])[key])

    def space(self, key: str, space: str) -> dict[str, object]:
        return as_dict(as_dict(self.cell(key)["spaces"])[space])

    def invisible(self, n: int, t: int, space: str, vocab: str) -> dict[str, object]:
        return as_dict(as_dict(self.space(f"N{n}_T{t}", space)["invisible"])[vocab])

    def test_committed_receipt_equals_a_fresh_build_byte_for_byte(self) -> None:
        self.assertEqual(self.committed, common.receipt_bytes(self.receipt))
        self.assertNotIn(b"\r", self.committed)
        self.assertTrue(self.committed.endswith(b"}\n"))
        self.assertEqual(json.loads(self.committed.decode("ascii")), self.receipt)

    def test_receipt_replays_byte_identically_into_two_directories(self) -> None:
        dirs = [Path(tempfile.mkdtemp(prefix="tmp_test_replay_", dir=common.TREE)) for _ in range(2)]
        try:
            written = [common.write_receipt(d / "witness_types.json", self.receipt) for d in dirs]
            self.assertEqual(written[0].read_bytes(), written[1].read_bytes())
            self.assertEqual(written[0].read_bytes(), self.committed)
        finally:
            for d in dirs:
                shutil.rmtree(d)
        # The computation itself replays: the two small cells built twice.
        self.assertEqual(wt.analyze_cell(2, 2), wt.analyze_cell(2, 2))
        self.assertEqual(wt.analyze_cell(2, 3), wt.analyze_cell(2, 3))

    def test_header_bounds_and_numbering_note(self) -> None:
        for key, value in common.receipt_header().items():
            self.assertEqual(self.receipt[key], value)
        self.assertEqual(self.receipt["part"], "P3")
        self.assertEqual(self.receipt["declared_bounds"], wt.DECLARED_BOUNDS)
        self.assertIn("the prompt's, not the paper's", str(self.receipt["numbering_note"]))
        reached = as_dict(self.receipt["bounds_reached"])
        self.assertEqual(reached["carrier_reached"], 3)
        self.assertEqual(reached["carrier_reached_at"], ["T = 2"])
        self.assertEqual(reached["token_domain_reached"], 3)
        self.assertEqual(reached["token_domain_reached_at"], ["N = 2"])
        self.assertEqual(reached["cells_enumerated"], ["N2_T2", "N2_T3", "N3_T2"])
        self.assertEqual(reached["cells_not_enumerated"], ["N3_T3"])
        refused = [str(x) for x in as_list(reached["refused_by_name"])]
        self.assertIn("N = 4", refused)
        self.assertIn("T = 4", refused)
        self.assertTrue(any(x.startswith("cell N3_T3: 117440512") and "per-cell" in x for x in refused))

    def test_cells_bounded_exactly_where_declared(self) -> None:
        for key in ("N2_T2", "N2_T3", "N3_T2"):
            self.assertFalse(self.cell(key)["bounded"], key)
            self.assertTrue(self.cell(key)["enumerated"], key)
            for space in wt.SPACES:
                self.assertTrue(self.space(key, space)["enumerated"])
        cell = self.cell("N3_T3")
        self.assertTrue(cell["bounded"])
        self.assertFalse(cell["enumerated"])
        self.assertEqual(cell["declared_cell_assignment_count"], 117440512)
        self.assertIn("per cell", str(cell["bound_reached"]))
        for space in wt.SPACES:
            self.assertFalse(self.space("N3_T3", space)["enumerated"])
            self.assertTrue(self.space("N3_T3", space)["bounded"])
        self.assertEqual(self.space("N3_T3", "witnessed")["declared_assignment_count"], 117440512)
        self.assertEqual(self.space("N3_T3", "witnessed_irreflexive")["declared_assignment_count"], 229376)

    def test_vocabulary_sizes_in_the_receipt(self) -> None:
        sizes = as_dict(as_dict(self.receipt["step22_vocabularies"])["sizes_by_cell"])
        for n, t in wt.CELLS:
            row = as_dict(sizes[f"N{n}_T{t}"])
            for name in wt.VOCABULARIES:
                self.assertEqual(row[name], wt.vocabulary_size_formula(name, n, t))
            self.assertEqual(as_dict(self.cell(f"N{n}_T{t}")["vocabulary_sizes"]), row)

    def test_separating_pairs_rechecked_by_every_question(self) -> None:
        for n, t, space in enumerated_spaces():
            block = as_dict(self.space(f"N{n}_T{t}", space)["separating"])
            for coarse, fine in wt.SEPARATIONS:
                entry = as_dict(block[f"{coarse}_vs_{fine}"])
                self.assertGreater(as_int(entry["pair_count"]), 0, (n, t, space, coarse, fine))
                pair = as_dict(entry["first_pair"])
                a = masks_of(pair["left"])
                b = masks_of(pair["right"])
                self.assertLess(a, b)
                self.assertNotEqual(a, b)
                self.assertTrue(wt.is_witnessed(a, n) and wt.is_witnessed(b, n))
                for q in wt.vocabulary(coarse, n, t):
                    self.assertEqual(wt.evaluate(q, a, n), wt.evaluate(q, b, n), q.text())
                diff = wt.differing_questions(wt.vocabulary(fine, n, t), a, b, n)
                self.assertGreater(len(diff), 0)
                self.assertEqual(len(diff), entry["fine_differing_question_count"])
                self.assertEqual(diff[0].text(), entry["first_fine_differing_question"])
                self.assertEqual(entry["coarse_differing_question_count"], 0)

    def test_step_23_first_pair_is_the_computed_one(self) -> None:
        entry = as_dict(as_dict(self.space("N2_T2", "witnessed_irreflexive")["separating"])["V1_vs_V2_ANON"])
        pair = as_dict(entry["first_pair"])
        self.assertEqual(masks_of(pair["left"]), (0, 1, 1, 0))
        self.assertEqual(masks_of(pair["right"]), (0, 1, 2, 0))
        self.assertEqual(entry["first_fine_differing_question"], "share((0,1),(1,0))")
        self.assertEqual(entry["pair_count"], 6)

    def test_invisible_pairs_rechecked_by_every_question(self) -> None:
        for n, t, space in enumerated_spaces():
            for name in wt.INVISIBLE_IN:
                entry = self.invisible(n, t, space, name)
                vocab = wt.vocabulary(name, n, t)
                self.assertEqual(
                    as_int(entry["pair_count"]),
                    as_int(entry["isomorphic_pair_count"]) + as_int(entry["non_isomorphic_pair_count"]),
                )
                for pair_key, expect_iso in zip(FIRST_KEYS, (None, False, False, False)):
                    rendered = entry[pair_key]
                    if rendered is None:
                        continue
                    pair = as_dict(rendered)
                    a = masks_of(pair["left"])
                    b = masks_of(pair["right"])
                    self.assertLess(a, b)
                    for q in vocab:
                        self.assertEqual(wt.evaluate(q, a, n), wt.evaluate(q, b, n), (name, q.text()))
                    iso = wt.family_isomorphic_metatheory(a, b, n, t)
                    if expect_iso is not None:
                        self.assertEqual(iso, expect_iso, (n, t, space, name, pair_key))
                    if pair_key == "first_non_isomorphic_count_equal_pair":
                        self.assertEqual(wt.count_vector(a), wt.count_vector(b))
                    char = as_dict(entry[f"{pair_key}_characterization"])
                    self.assertEqual(char["isomorphic_as_families"], iso)
                    self.assertEqual(
                        char["invariants_that_differ"],
                        [k for k in wt.INVARIANTS if wt.invariants(a, t)[k] != wt.invariants(b, t)[k]],
                    )
                    if iso:
                        self.assertEqual(char["invariants_that_differ"], [])

    def test_every_first_pair_is_the_least_by_independent_scan(self) -> None:
        """Round-1 repair.  Every ``first_*`` key of every enumerated space is
        re-derived by scanning assignments in enumeration order and, for each,
        the later assignments in order, stopping at the first qualifying pair
        -- no buckets, no group order.  Where the receipt reports no pair, the
        absence is re-derived by grouping (one isomorphism class per group),
        since a scan for a pair that does not exist is the whole space
        squared."""

        for n, t, space in enumerated_spaces():
            data = space_data(n, t, space)
            conds = data.conditions()
            for vocab in wt.INVISIBLE_IN:
                entry = self.invisible(n, t, space, vocab)
                for key in FIRST_KEYS:
                    reported = pair_of(entry[key])
                    if reported is None:
                        self.assertTrue(data.no_pair_by_grouping(vocab, key), (n, t, space, vocab, key))
                    else:
                        found = data.first_where(data.keys[vocab], conds[key])
                        self.assertEqual(found, reported, (n, t, space, vocab, key))
            block = as_dict(self.space(f"N{n}_T{t}", space)["separating"])
            for coarse, fine in wt.SEPARATIONS:
                reported = pair_of(as_dict(block[f"{coarse}_vs_{fine}"])["first_pair"])
                self.assertEqual(data.first_separating(coarse, fine), reported, (n, t, space, coarse, fine))

    def test_counts_and_first_pairs_by_full_pair_loop_on_small_spaces(self) -> None:
        """On every enumerated space of at most 200 assignments, every count
        and every first pair of the invisible and separating blocks is
        re-derived by a full double loop over the space."""

        covered: list[tuple[int, int, str]] = []
        for n, t, space in enumerated_spaces():
            if wt.declared_assignment_count(n, t, space) > FULL_LOOP_AT_MOST:
                continue
            covered.append((n, t, space))
            data = space_data(n, t, space)
            for vocab in wt.INVISIBLE_IN:
                entry = self.invisible(n, t, space, vocab)
                loop = data.full_loop(vocab)
                for count_key in (
                    "pair_count",
                    "isomorphic_pair_count",
                    "non_isomorphic_pair_count",
                    "non_isomorphic_count_equal_pair_count",
                ):
                    self.assertEqual(entry[count_key], loop[count_key], (n, t, space, vocab, count_key))
                self.assertEqual(
                    entry["non_isomorphic_pairs_by_differing_invariant"], loop["by_invariant"], (n, t, space, vocab)
                )
                self.assertEqual(
                    entry["non_isomorphic_count_equal_pairs_by_differing_invariant"],
                    loop["by_invariant_count_equal"],
                    (n, t, space, vocab),
                )
                firsts = as_dict(loop["firsts"])
                for key in FIRST_KEYS:
                    self.assertEqual(pair_of(entry[key]), firsts[key], (n, t, space, vocab, key))
            block = as_dict(self.space(f"N{n}_T{t}", space)["separating"])
            for coarse, fine in wt.SEPARATIONS:
                sep = as_dict(block[f"{coarse}_vs_{fine}"])
                self.assertEqual(sep["pair_count"], data.separating_count(coarse, fine), (n, t, space, coarse, fine))
        self.assertEqual(covered, [(2, 2, "witnessed"), (2, 2, "witnessed_irreflexive"), (2, 3, "witnessed_irreflexive")])

    def test_v2_named_hides_nothing_and_v1_v2_anon_hides_renamings(self) -> None:
        for n, t, space in enumerated_spaces():
            block = as_dict(self.space(f"N{n}_T{t}", space)["invisible"])
            self.assertEqual(as_dict(block["V2_NAMED"])["pair_count"], 0)
            self.assertEqual(as_dict(block["V1_V2_NAMED"])["pair_count"], 0)
            anon = as_dict(block["V1_V2_ANON"])
            self.assertGreater(as_int(anon["isomorphic_pair_count"]), 0)
            self.assertEqual(
                anon["isomorphic_pair_count"],
                self.space(f"N{n}_T{t}", space)["isomorphic_pair_count_total"],
            )
            self.assertEqual(
                as_dict(anon["non_isomorphic_pairs_by_differing_invariant"])[
                    "none_of_the_computed_invariants"
                ],
                0,
            )
            noniso_count_equal = as_int(anon["non_isomorphic_count_equal_pair_count"])
            if t == 2:
                self.assertEqual(noniso_count_equal, 0)
            else:
                self.assertGreater(noniso_count_equal, 0)

    def test_count_equal_pairs_by_differing_invariant_in_every_space(self) -> None:
        """Round-2 repair: the kind-3 sentence -- every count-equal
        non-isomorphic invisible pair differs in how many tokens two pairs
        share -- is a receipt value, re-derived here by grouping and a
        direct loop inside each group."""

        for n, t, space in enumerated_spaces():
            data = space_data(n, t, space)
            for vocab in wt.INVISIBLE_IN:
                entry = self.invisible(n, t, space, vocab)
                total, by = data.count_equal_by_invariant_by_groups(vocab)
                self.assertEqual(entry["non_isomorphic_count_equal_pair_count"], total, (n, t, space, vocab))
                self.assertEqual(
                    entry["non_isomorphic_count_equal_pairs_by_differing_invariant"], by, (n, t, space, vocab)
                )
                self.assertEqual(
                    entry["every_non_isomorphic_count_equal_pair_differs_in_intersection_profile"],
                    by["intersection_profile"] == total,
                )
                self.assertLessEqual(by["intersection_profile"], total)
            anon = self.invisible(n, t, space, "V1_V2_ANON")
            self.assertTrue(anon["every_non_isomorphic_count_equal_pair_differs_in_intersection_profile"])
        self.assertEqual(
            self.invisible(2, 3, "witnessed", "V1_V2_ANON")["non_isomorphic_count_equal_pairs_by_differing_invariant"],
            {
                "intersection_profile": 7650,
                "token_degree_multiset": 5598,
                "common_token_count": 3330,
                "none_of_the_computed_invariants": 0,
            },
        )
        self.assertEqual(
            self.invisible(2, 3, "witnessed_irreflexive", "V1_V2_ANON")[
                "non_isomorphic_count_equal_pairs_by_differing_invariant"
            ],
            {
                "intersection_profile": 18,
                "token_degree_multiset": 18,
                "common_token_count": 18,
                "none_of_the_computed_invariants": 0,
            },
        )
        self.assertEqual(wt.COUNT_EQUAL_INVARIANTS, ("intersection_profile", "token_degree_multiset", "common_token_count"))

    def test_step_24_first_count_equal_invisible_pairs(self) -> None:
        entry = self.invisible(2, 3, "witnessed_irreflexive", "V1_V2_ANON")
        self.assertEqual(pair_of(entry["first_non_isomorphic_count_equal_pair"]), ((0, 3, 3, 0), (0, 3, 5, 0)))
        self.assertEqual(entry["non_isomorphic_count_equal_pair_count"], 18)
        self.assertEqual(pair_of(entry["first_pair"]), ((0, 1, 0, 0), (0, 2, 0, 0)))
        # A2's object at (2, 3): the least such pair has a singleton at the
        # designated pair and the two-token stores at (1, 0) and (1, 1);
        # the round-0 receipt reported (0,3,0,3)/(0,3,0,5), which is not least.
        witnessed = self.invisible(2, 3, "witnessed", "V1_V2_ANON")
        self.assertEqual(pair_of(witnessed["first_non_isomorphic_count_equal_pair"]), ((0, 1, 3, 3), (0, 1, 3, 5)))
        self.assertEqual(witnessed["non_isomorphic_count_equal_pair_count"], 7650)
        revision = as_dict(as_dict(self.receipt["revision"])["round_1"])
        withdrawn = as_dict(as_list(revision["withdrawn_values"])[0])
        self.assertEqual(as_dict(withdrawn["was"])["left_masks"], [0, 3, 0, 3])
        self.assertNotEqual(
            pair_of(witnessed["first_non_isomorphic_count_equal_pair"]),
            (tuple(as_list(as_dict(withdrawn["was"])["left_masks"])), tuple(as_list(as_dict(withdrawn["was"])["right_masks"]))),
        )

    def test_refinement_order_is_computed_not_assumed(self) -> None:
        for n, t, space in enumerated_spaces():
            w = self.space(f"N{n}_T{t}", space)
            ref = as_dict(w["refinement"])
            self.assertTrue(ref["V1 refines V0"])
            self.assertTrue(ref["V2_ANON refines V0"])
            self.assertFalse(ref["V1 refines V2_ANON"])
            self.assertFalse(ref["V2_ANON refines V1"])
            self.assertFalse(ref["V0 refines V1"])
            for other in wt.VOCABULARIES:
                if other != "V2_NAMED":
                    self.assertTrue(ref[f"V2_NAMED refines {other}"])
            inv = as_dict(w["invariant_under_token_bijections"])
            self.assertEqual(
                inv,
                {
                    "V0": True,
                    "V1": True,
                    "V2_ANON": True,
                    "V2_NAMED": False,
                    "V1_V2_ANON": True,
                    "V1_V2_NAMED": False,
                },
            )
            classes = as_dict(w["partition_class_counts"])
            self.assertEqual(classes["V2_NAMED"], w["assignment_count"])

    def test_summary_keys_agree_with_the_cells(self) -> None:
        summary = as_dict(self.receipt["summary"])
        for n, t, space in enumerated_spaces():
            row = as_dict(summary[f"N{n}_T{t}/{space}"])
            w = self.space(f"N{n}_T{t}", space)
            self.assertEqual(row["assignment_count"], w["assignment_count"])
            sep = as_dict(w["separating"])
            inv = as_dict(w["invisible"])
            self.assertEqual(row["V1_equal_V2_ANON_different"], as_dict(sep["V1_vs_V2_ANON"])["pair_count"])
            self.assertEqual(row["invisible_in_V1_V2_ANON"], as_dict(inv["V1_V2_ANON"])["pair_count"])
            self.assertEqual(
                row["invisible_in_V1_V2_ANON_non_isomorphic_count_equal"],
                as_dict(inv["V1_V2_ANON"])["non_isomorphic_count_equal_pair_count"],
            )
        for space in wt.SPACES:
            self.assertEqual(as_dict(summary[f"N3_T3/{space}"]), {"enumerated": False})

    def test_step25_halves_are_labelled(self) -> None:
        answer = as_dict(self.receipt["step25_answer"])
        self.assertIn("exactly when TOKEN_EQ is admitted on top of TOKEN_DOMAIN", str(answer["sentence"]))
        self.assertIn("the admission named in step 21", str(answer["sentence"]))
        self.assertIn("at T = 3 (cell (2, 3), the only T = 3 cell enumerated", str(answer["sentence"]))
        self.assertNotIn("from T = 3 on", str(answer["sentence"]))
        self.assertNotIn("T >= 2", str(answer["when_half"]))
        self.assertTrue(str(answer["when_half"]).startswith("computed"))
        self.assertTrue(str(answer["only_when_half"]).startswith("definitional"))
        self.assertIn("could not have come out otherwise", str(answer["only_when_half"]))
        self.assertIn("bounded", str(answer["scope"]))
        self.assertIn("(3, 3) not enumerated", str(answer["scope"]))

    def test_terminals_are_legal_scoped_and_bounded(self) -> None:
        legal = legal_terminals()
        self.assertIn("S9_3_WITNESS_OBSERVABLE", legal)
        self.assertEqual(len(legal), 25)
        terminals = [as_dict(x) for x in as_list(self.receipt["terminals"])]
        names = [str(x["terminal"]) for x in terminals]
        self.assertEqual(len(names), len(set(names)))
        for entry in terminals:
            self.assertIn(entry["terminal"], legal)
            self.assertTrue(str(entry["scope"]).strip())
        for result in ("S9_3_WITNESS_OBSERVABLE", "S9_3_WITNESS_INVISIBLE"):
            scope = str(terminals[names.index(result)]["scope"])
            self.assertIn("bounded", scope)
            self.assertIn("N = 3", scope)
            self.assertIn("T = 3", scope)
            self.assertIn("(3, 3) not enumerated", scope)
        self.assertIn("the only T = 3 cell enumerated", str(terminals[names.index("S9_3_WITNESS_INVISIBLE")]["scope"]))
        self.assertIn("on top of TOKEN_DOMAIN", str(terminals[names.index("S9_3_WITNESS_OBSERVABLE")]["scope"]))
        revision = as_dict(self.receipt["revision"])
        self.assertEqual(revision["rounds_completed"], 3)
        self.assertIn("round_1", revision)
        self.assertIn("round_2", revision)
        self.assertIn("round_3", revision)
        admission = str(terminals[names.index("S9_3_ADMISSION_NAMED")]["scope"])
        self.assertIn("not contained in A3's bill, which it does not contain either", admission)
        self.assertNotIn("strictly less", admission)
        price = str(as_dict(as_dict(as_dict(self.receipt["step21_admission"])["TOKEN_EQ"]))["price_vs_A3"])
        self.assertIn("not contained in A3's bill, which it does not contain either", price)
        self.assertNotIn("strictly less", price)
        self.assertIn("bounded", str(terminals[names.index("PYTHON_ONLY_SCOPE_DECLARED")]["scope"]))
        for name in ("OB1_UNCHANGED", "S66_UNCHANGED", "S9_LAST_UNCHANGED", "REFUSED", "PYTHON_ONLY_SCOPE_DECLARED"):
            self.assertIn(name, names)
        self.assertNotIn("LEAN_CARRIED", names)
        self.assertNotIn("LEAN_NOT_CARRIED", names)
        self.assertIn("LEAN_NOT_CARRIED", str(self.receipt["lean_stage_note"]))

    def test_terminal_strings_cite_only_audited_lean_theorems(self) -> None:
        """Every Lean theorem the receipt's terminal scopes and its
        lean_stage_note cite by name is an audited report: listed under
        LEAN_STAGE_MODULE in verify_lean.AXIOM_REPORT_DECLARATIONS and
        declared with ``theorem`` in the module's source.  A name that is
        only promised fails here; the strings no longer say "proposed, not
        proved" or "no Lean theorem of this part exists"."""

        declared = set(verify_lean.AXIOM_REPORT_DECLARATIONS)
        source = (common.TREE / "lean" / "S9Obligations" / "WitnessTypes.lean").read_text(encoding="utf-8")
        self.assertEqual(len(wt.LEAN_STAGE_CITED), 5)
        for name in wt.LEAN_STAGE_CITED:
            self.assertIn(f"{wt.LEAN_STAGE_MODULE}.{name}", declared, name)
            self.assertRegex(source, r"(?m)^theorem " + re.escape(name) + r"\b")
        terminals = [as_dict(x) for x in as_list(self.receipt["terminals"])]
        names = [str(x["terminal"]) for x in terminals]
        observable = str(terminals[names.index("S9_3_WITNESS_OBSERVABLE")]["scope"])
        python_only = str(terminals[names.index("PYTHON_ONLY_SCOPE_DECLARED")]["scope"])
        note = str(self.receipt["lean_stage_note"])
        for name in wt.LEAN_STAGE_CITED[:3]:
            self.assertIn(name, observable)
        for name in wt.LEAN_STAGE_CITED:
            self.assertIn(name, python_only)
            self.assertIn(name, note)
        for text in (observable, python_only, note):
            self.assertIn(wt.LEAN_STAGE_MODULE, text)
            for cited in re.findall(r"\bS9_3_\w+", text):
                self.assertIn(f"{wt.LEAN_STAGE_MODULE}.{cited}", declared, cited)
            self.assertNotIn("proposed, not proved", text)
            self.assertNotIn("no Lean theorem of this part", text)
        self.assertIn("LEAN_NOT_CARRIED", note)

    def test_token_names_price_cites_an_existing_key(self) -> None:
        price = str(as_dict(as_dict(self.receipt["step21_admission"])["TOKEN_NAMES"])["price"])
        self.assertIn("invariant_under_token_bijections.V2_NAMED", price)
        for n, t, space in enumerated_spaces():
            self.assertFalse(as_dict(self.space(f"N{n}_T{t}", space)["invariant_under_token_bijections"])["V2_NAMED"])

    def test_lean_targets_render_the_computed_pairs(self) -> None:
        targets = {str(as_dict(x)["name"]): as_dict(x) for x in as_list(self.receipt["lean_targets"])}
        defs = [str(d) for d in as_list(targets["S9_3_sep_W1_W2_definitions"]["definitions"])]
        self.assertEqual(defs[0], wt.lean_definition("W1", (0, 1, 1, 0), 2, 2))
        self.assertEqual(defs[1], wt.lean_definition("W2", (0, 1, 2, 0), 2, 2))
        inv = targets["S9_3_inv_W3_W4_definitions"]
        self.assertTrue(inv["present"])
        inv_defs = [str(d) for d in as_list(inv["definitions"])]
        self.assertEqual(inv_defs[0], wt.lean_definition("W3", (0, 3, 3, 0), 2, 3))
        self.assertEqual(inv_defs[1], wt.lean_definition("W4", (0, 3, 5, 0), 2, 3))
        for name in (
            "S9_3_sep_presence_equal",
            "S9_3_sep_count_equal",
            "S9_3_sep_V1_indistinguishable",
            "S9_3_sep_V2_ANON_separates",
            "S9_3_sep_not_isomorphic",
        ):
            self.assertIn(name, targets)


class FindingsTests(unittest.TestCase):
    """Negative scans over P3_FINDINGS.md and the receipt (steps 36, 37,
    40; the house rule on restricted words), and a resolver for every
    receipt key, test name, function name, and file the findings cite."""

    findings: str
    receipt: dict[str, object]

    @classmethod
    def setUpClass(cls) -> None:
        cls.findings = FINDINGS_PATH.read_text(encoding="ascii")
        cls.receipt = json.loads(RECEIPT_PATH.read_text(encoding="ascii"))

    def test_scanners_fire_on_injected_claims(self) -> None:
        self.assertEqual(protected_open_claims("OB-1 is closed by this part."), ["OB-1 is closed"])
        self.assertTrue(protected_open_claims("this closes OB-1"))
        self.assertTrue(protected_open_claims("the inscription bridge is priced"))
        self.assertTrue(protected_open_claims("S6.6 now narrows"))
        self.assertEqual(protected_open_claims("it makes no claim about OB-1; none is closed here."), [])
        self.assertEqual(protected_open_claims("OB-1 is not closed, narrowed, or priced"), [])
        self.assertEqual(protected_open_claims("this part makes no claim about OB-1; it is not closed, narrowed, or priced here"), [])
        # round-2 repair: a denial followed by a claim in the same sentence
        self.assertEqual(
            protected_open_claims("OB-1 is not closed here, but this part narrows OB-1 anyway."), ["narrows OB-1"]
        )
        self.assertEqual(protected_open_claims("it does not close OB-1; it prices OB-1."), ["prices OB-1"])
        self.assertEqual(carrier_general_phrases("this holds for all carriers."), ["for all carriers"])
        # round-2 repair: a one-cell observation projected past the bound
        self.assertEqual(carrier_general_phrases("From T = 3 on, such pairs are invisible."), ["from t = 3 on"])
        self.assertEqual(carrier_general_phrases("this holds for T >= 3."), ["for t >="])
        self.assertEqual(
            carrier_general_phrases("at T = 3 (cell (2, 3), the only T = 3 cell enumerated) such pairs exist."), []
        )
        self.assertEqual(carrier_general_phrases("the result holds in general."), ["in general"])
        self.assertEqual(carrier_general_phrases("no carrier-general claim is made."), [])
        self.assertEqual(carrier_general_phrases("this is a carrier-general fact."), ["carrier-general (unnegated)"])
        self.assertEqual(external_markers("as is well-known, see https://x"), ["https://", "well-known"])
        self.assertEqual(unscoped_words("the canonical form is forced."), ["canonical", "forced"])
        self.assertEqual(unscoped_words("the lattice is complete."), ["unscoped: the lattice is complete."])
        self.assertEqual(unscoped_words("the cell is enumerated completely."), [])

    def test_findings_and_receipt_make_no_protected_open_claim(self) -> None:
        self.assertEqual(protected_open_claims(self.findings), [])
        for s in json_strings(self.receipt):
            self.assertEqual(protected_open_claims(s), [], s[:80])
        # The three UNCHANGED terminals must be present, each denying a claim.
        for name in ("OB1_UNCHANGED", "S66_UNCHANGED", "S9_LAST_UNCHANGED"):
            self.assertIn(f"**{name}**", self.findings)

    def test_findings_and_receipt_carry_no_carrier_general_phrase(self) -> None:
        self.assertEqual(carrier_general_phrases(self.findings), [])
        for s in json_strings(self.receipt):
            self.assertEqual(carrier_general_phrases(s), [], s[:80])

    def test_result_terminals_say_bounded_in_the_same_bullet(self) -> None:
        section = self.findings[self.findings.index("## Terminals, with scopes"):]
        bullets = re.split(r"\n\* ", section)
        for name in ("S9_3_WITNESS_OBSERVABLE", "S9_3_WITNESS_INVISIBLE"):
            bullet = [b for b in bullets if b.startswith(f"**{name}**")]
            self.assertEqual(len(bullet), 1, name)
            text = flatten(bullet[0])
            self.assertIn("bounded", text)
            self.assertIn("N = 3", text)
            self.assertIn("T = 3", text)
            self.assertIn("(3, 3)", text)
        self.assertIn("## Bounded, first", self.findings)
        self.assertIn("per cell", self.findings)
        for name in (str(as_dict(x)["terminal"]) for x in as_list(self.receipt["terminals"])):
            self.assertIn(f"**{name}**", self.findings)

    def test_no_external_name_marker_in_p3_files(self) -> None:
        """Over the five files; the test module's own scanner definitions
        and its injection test are cut out first, since they spell the
        markers in order to catch them."""

        for rel in P3_FILES:
            text = (common.TREE / rel).read_text(encoding="ascii")
            if rel == "test_witness_types.py":
                text = re.sub(
                    r"# scanner-definitions-begin.*?# scanner-definitions-end", "", text, flags=re.S
                )
                text = re.sub(
                    r"    def test_scanners_fire_on_injected_claims.*?\n    def ", "    def ", text, flags=re.S
                )
                self.assertNotIn("scanner-definitions-begin", text)
                self.assertNotIn("test_scanners_fire_on_injected_claims", text)
            self.assertEqual(external_markers(text), [], rel)

    def test_restricted_words_are_absent_or_scoped_in_findings(self) -> None:
        prose = re.sub(r"`[^`]*`", "", self.findings)
        prose = re.sub(r"^    .*$", "", prose, flags=re.M)  # indented code blocks
        self.assertEqual(unscoped_words(prose), [])

    def test_findings_sha_and_size_match_the_committed_receipt(self) -> None:
        raw = RECEIPT_PATH.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        self.assertIn(digest, self.findings)
        self.assertIn(f"{len(raw)} bytes", self.findings)

    def test_findings_cite_only_resolvable_names(self) -> None:
        """Every backticked token of the findings resolves: a file path
        exists; a dotted receipt path (with <cell>, <space>, <V> expanded
        over the enumerated cells, the spaces, and the invisible-in
        vocabularies) is a path of the receipt; an `X refines Y` token is a
        receipt key; a `common.<name>` token is an attribute of common; a
        `test_*` token is a test of this module; and a bare token carrying
        an underscore is a receipt key, a whole receipt string value, an
        attribute of witness_types, a terminal, a Lean-target name, or one
        of a short listed set.  Tokens with parentheses, braces, or other
        non-identifier words (rendered questions, stores, Lean snippets)
        are not receipt citations and are skipped."""

        paths, key_names = receipt_paths(self.receipt)
        values = set(json_strings(self.receipt))
        cells = [str(c) for c in as_list(as_dict(self.receipt["bounds_reached"])["cells_enumerated"])]
        lean_text = " ".join(json_strings(self.receipt["lean_targets"]))
        test_names = {
            name
            for cls in (VocabularyTests, EnumerationTests, ReceiptTests, FindingsTests, FirewallTests)
            for name in dir(cls)
            if name.startswith("test_")
        }
        allow_bare = {"TOKEN_DOMAIN", "PYTHONPATH", "PYTHONUTF8", "AXIOM_REPORT_DECLARATIONS"}
        sealed_lean = (common.REPO / "lean4" / "Derivation" / "PrimDiff.lean").read_text(encoding="utf-8")
        placeholders = (("<cell>", cells), ("<space>", list(wt.SPACES)), ("<V>", list(wt.INVISIBLE_IN)))
        unresolved: list[str] = []
        checked = 0
        for token in re.findall(r"`([^`\n]+)`", self.findings):
            head = re.split(r" (?:=|>|<|!=) ", token)[0]
            if head.endswith("*"):
                continue  # a key family such as first_*, named as a family
            if head.endswith((".py", ".md", ".json", ".lean")):
                checked += 1
                if not (common.TREE / head).exists() and not (common.REPO / head).exists():
                    unresolved.append(f"file {head}")
                continue
            if "(" in head or "{" in head:
                continue
            if " " in head:
                if re.fullmatch(r"\S+ refines \S+", head):
                    checked += 1
                    if head not in key_names:
                        unresolved.append(f"key {head}")
                continue
            if head.startswith("common."):
                checked += 1
                if not hasattr(common, head[len("common."):]):
                    unresolved.append(f"common attribute {head}")
                continue
            if "." in head:
                expansions = [head]
                for placeholder, options in placeholders:
                    if placeholder in head:
                        expansions = [e.replace(placeholder, v) for e in expansions for v in options]
                for path in expansions:
                    checked += 1
                    if path not in paths:
                        unresolved.append(f"path {path}")
                continue
            if "_" not in head:
                continue
            checked += 1
            if head.startswith("test_"):
                if head not in test_names:
                    unresolved.append(f"test {head}")
                continue
            if (
                head in key_names
                or head in values
                or hasattr(wt, head)
                or (head.startswith("S9_3_") and head in lean_text)
                or head in allow_bare
                or re.search(r"\btheorem\s+" + re.escape(head) + r"\b", sealed_lean) is not None
            ):
                continue
            unresolved.append(f"name {head}")
        self.assertEqual(unresolved, [])
        self.assertGreater(checked, 100)


class FirewallTests(unittest.TestCase):
    def test_no_working_denylist_identifier_in_p3_files(self) -> None:
        payload = json.loads(
            (common.REPO / "contact" / "analysis" / "contact_countermodels.json").read_text(
                encoding="utf-8"
            )
        )
        block = payload["denylist"]
        working = sorted(set(block["full_census"]) - set(block["subtracted_as_native_or_core"]))
        self.assertEqual(len(working), 102)
        patterns = [(name, re.compile(r"(?<![\w])" + re.escape(name) + r"(?![\w])")) for name in working]
        for rel in P3_FILES:
            path = common.TREE / rel
            if not path.exists():
                continue
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw, rel)
            text = raw.decode("ascii")
            leaks = [name for name, pat in patterns if pat.search(text)]
            self.assertEqual(leaks, [], rel)


if __name__ == "__main__":
    unittest.main()
