"""The rung's certificates.  AuthorityEffect: None.

Every test here pins a sentence the rung writes in ``STATUS.md`` or in
``CLAIM_LEDGER.md``.  The docstring of each test names that sentence, so a
reader can go from a claim in the prose to the check that decides it and
back.  A receipt is never a proof, and nothing below turns one into a proof:
what these checks establish is that the numbers the prose quotes are the
numbers the code produces at the declared bounds, and that the apparatus
which produced them fails when it should.

Five groups.

``DeclaredSpaceTests`` scores R1-1.  The three-item candidate space is an
admitted primitive of this rung -- the sealed unpruned generator is declared
to two items and refuses above it -- so the space is certified rather than
asserted: against the sealed generator where the rung defers to it, and
against an independently written wider construction at every item count from
zero to three, in BOTH directions at each count.  A one-directional check
would pass a generator that quietly drops the two-new-form and two-fresh-datum
shapes, which is this rung's likeliest silent error.

``TwoItemReconstructionTests`` scores R1-2.  The rung's loop is a
reconstruction of a sibling loop it is forbidden to copy.  With the item
bound set to the sibling's own two, it must reproduce the sibling's committed
quantities and its selection must agree delta-for-delta with the public
sibling selection at every state and demanded pair of those runs.

``ReceiptReplayTests`` re-runs the whole entry point and compares bytes with
the committed receipt.  The compressed export is compared by the hash of its
UNCOMPRESSED bytes, never by its compressed bytes: this repository already
records that a local compression library rewrites those bytes without
changing the content, so a compressed-byte comparison would fail for a reason
that is not about the rung.

``ScoringTests`` checks that the scorer returns the verdicts the receipt
stores AND that it can return the other verdicts: a scorer that only ever
says HIT is a rubber stamp, so a synthetic body that should score MISSED is
constructed and asserted to score MISSED, and an emptied population is
asserted to score VACUOUS and never to be rounded up.

``ValidityClassTests`` and ``BudgetTests`` decide by running rather than by
assumption: whether the member this rung declares is strictly stronger than
the inherited one -- exhibited on a named delta at a named state -- and
whether each declared budget actually fires with its own terminal naming the
tree, the node and the demanded pair.

Classification: metatheory apparatus.  The sealed kernel and the two sibling
trees are consumed read-only by import through ``sys.path``; no line of their
source is transcribed, and the committed sibling receipt is read as a
supplied datum which this rung replays before comparing against.
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
import pathlib
import sys
import tempfile
import tomllib
import unittest
from itertools import combinations_with_replacement
from typing import Mapping, Optional, Sequence, cast
from unittest import mock

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Imported FIRST, while this tree is still the head of ``sys.path``: the
# rung's own modules put the sealed kernel and both sibling trees on the path
# ahead of it, and each sibling ships a module of this name.
import check_coverage as CC  # noqa: E402
import verify_pins as VP  # noqa: E402

import run_stream as RS  # noqa: E402
import stream as ST  # noqa: E402

from derivation.candidates import (  # noqa: E402
    Delta,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    apply_delta,
    canonical_delta,
    delta_events,
    iter_full_deltas,
)
from derivation.export import (  # noqa: E402
    Json,
    dumps_deterministic,
    read_json_gz,
)
from derivation.engine import Reading  # noqa: E402
from derivation.model import AdmissionError, Pair, Regime  # noqa: E402
from two_sided import (  # noqa: E402
    COMMITMENTS,
    SAME,
    TState,
    TStateKey,
    TSEvent,
    closure_targets,
    commitment_named,
    genesis_history,
    has_fresh_datum,
    honoured,
    min_responses,
    sealed_readings,
    ts_replay,
)

RECEIPT = HERE / "receipts" / "stream.json"
FULL = HERE / RS.FULL_PATH

# The values the prose quotes.  Each is pinned by the test that names it, so
# a run that moves one fails here rather than in a reader's memory.
EXPECTED_RUNS = 20
EXPECTED_NODES = 1974
EXPECTED_EDGES = 2209
EXPECTED_RESPONSE_EDGES = 1680
EXPECTED_EDGES_WITH_DATUM_ITEM = 0
# Of the 1680 retained minima, the item count each was selected at.  The
# headline is stated over all of them; only the third row was selected from
# the space this rung declares, and it is 32 in 3 of the 20 runs.  Pinned
# because the headline population is fifty-two times its three-item evidence
# and the receipt said so nowhere.
EXPECTED_EDGES_BY_ITEM_COUNT = {"1": 1081, "2": 567, "3": 32}
EXPECTED_EDGES_AT_THREE_ITEMS = 32
EXPECTED_RUNS_WITH_A_THREE_ITEM_SELECTION = {
    "F/parity/mu1": 1,
    "L/parity/mu1": 22,
    "L/residue_three/mu1": 9,
}
# The pre-expansion node guard stopped more than half the nodes reached, in
# six of the twenty runs, and wrote no truncation row while doing it.
EXPECTED_NODES_STOPPED_BY_THE_GUARD = 1039
EXPECTED_RUNS_TRUNCATED_BY_THE_GUARD = [
    "F/chain/mu1",
    "F/residue_three/mu1",
    "F/total_apart/mu1",
    "L/chain/mu1",
    "L/residue_three/mu1",
    "L/total_apart/mu1",
]
EXPECTED_REFUSAL_RECORDS_AT_THREE_ITEMS = 2
EXPECTED_RUNS_WITH_A_REFUSAL = ["L/parity/mu1"]
EXPECTED_THREE_ITEM_ENUMERATIONS = 20
EXPECTED_TWO_ITEM_REFUSAL_RECORDS = 15
EXPECTED_TWO_ITEM_REFUSAL_SITUATIONS = 14
EXPECTED_SITUATIONS_ANSWERED = 14
EXPECTED_SELECTION_COMPARISONS = 744
EXPECTED_FAMILY_SIZE = 8

# The frozen inputs, hashed before any module of this tree existed.
FROZEN_PROMPT_SHA = "efca5d969189bc2d887bd031f406cbdd9ffc3a2499491e754c1251683fb039a5"
FROZEN_PREDICTIONS_SHA = "b688840362287aa3101c640bfc063655501e19534a6b84a58b88a5808b663842"

SIBLING_RECEIPT = RS.SIBLING_RECEIPT

# The bases whose whole three-item multiset space is swept item by item.
# The sweep is linear in the multiset count, and the multiset count grows
# with the cube of the universe, so it is run on a named subset and the
# wider construction carries the rest.  The subset was three bases, all of
# them carrying at most one form and no rule, so the sweep saw no rule, no
# instance and no second form -- while seven of the nineteen real three-item
# enumerations run on two-form bases.  It now carries two RULED bases and one
# TWO-FORM base as well.
SWEPT_BASES = (
    "b0_no_datum_no_form",
    "b1_two_data",
    "b2_unary_form",
    "b3_unary_form_ruled",
    "b6_binary_ruled_three_data",
    "b7_two_forms_with_instances",
)


# ---------------------------------------------------------------------------
# Typed readers.  ``json.loads`` hands back an untyped tree; these turn one
# node of it into a typed value or fail by name.
# ---------------------------------------------------------------------------


def _obj(value: object) -> dict[str, Json]:
    if not isinstance(value, dict):
        raise TypeError(f"not an object: {value!r}")
    return {str(k): cast(Json, v) for k, v in value.items()}


def _arr(value: object) -> list[Json]:
    if not isinstance(value, list):
        raise TypeError(f"not an array: {value!r}")
    return [cast(Json, v) for v in value]


def _num(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"not a count: {value!r}")
    return value


def _txt(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError(f"not a string: {value!r}")
    return value


def _flag(value: object) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"not a flag: {value!r}")
    return value


def _at(row: Mapping[str, Json], *path: str) -> Json:
    here: Json = dict(row)
    for step in path:
        here = _obj(here)[step]
    return here


def _set(body: dict[str, Json], path: Sequence[str], value: Json) -> None:
    """Write one value into a receipt body IN PLACE.

    Written out rather than reached through the readers above: those copy the
    mapping they read, so a mutation applied through them lands on the copy
    and the synthetic body is identical to the one it was built from.  That
    defect would make every injection below pass silently, which is exactly
    the failure the injections exist to refuse.
    """

    node: object = body
    for step in path[:-1]:
        if not isinstance(node, dict):
            raise TypeError(f"not an object on the way to {step!r}")
        node = node[step]
    if not isinstance(node, dict):
        raise TypeError(f"not an object at {path[-1]!r}")
    if path[-1] not in node:
        raise KeyError(f"{path[-1]!r} is not a key of the receipt body")
    cast(dict[str, Json], node)[path[-1]] = value


def load_receipt() -> dict[str, Json]:
    return _obj(json.loads(RECEIPT.read_text(encoding="utf-8")))


def load_sibling() -> dict[str, dict[str, Json]]:
    payload = _obj(json.loads(SIBLING_RECEIPT.read_text(encoding="utf-8")))
    return {_txt(_obj(row)["id"]): _obj(row) for row in _arr(payload["trees"])}


# ---------------------------------------------------------------------------
# Work done once.  The whole entry point takes minutes; the two-item trees
# take seconds.  Both are built on first use and remembered, so the order in
# which the test runner walks the classes does not change what is computed.
# ---------------------------------------------------------------------------

_REPLAY: Optional[tuple[bytes, bytes, str]] = None
_TWO_ITEM: Optional[list[tuple[str, ST.STree]]] = None


def replay() -> tuple[bytes, bytes, str]:
    """``(summary bytes, compressed bytes, printed report)`` from a fresh run
    of the entry point into a temporary directory."""

    global _REPLAY
    if _REPLAY is None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            out = tmp / "stream.json"
            gz = tmp / "full" / "second_stream_full.json.gz"
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = RS.main(["--out", str(out), "--full", str(gz)])
            if code != 0:
                raise AssertionError(f"the entry point returned {code}")
            _REPLAY = (out.read_bytes(), gz.read_bytes(), buffer.getvalue())
    return _REPLAY


def two_item_trees() -> list[tuple[str, ST.STree]]:
    """The twenty runs of the rectangle at the sibling's own item bound,
    built by this rung's loop with the inherited validity member."""

    global _TWO_ITEM
    if _TWO_ITEM is None:
        built: list[tuple[str, ST.STree]] = []
        for reading in sealed_readings():
            for commitment in COMMITMENTS:
                for measure in ST.MEASURES:
                    tree = ST.build_stream_tree(
                        reading,
                        commitment,
                        measure,
                        ST.BOUNDS_TWO,
                        ST.RULE_NO_REGRESS,
                        census=False,
                    )
                    built.append((tree.ident, tree))
        _TWO_ITEM = built
    return _TWO_ITEM


def family() -> list[tuple[str, Regime]]:
    """The declared cross-check family, named once so every reader of it is
    typed against the sealed regime type."""

    return RS.cross_check_family()


def genesis_states() -> list[tuple[str, TState]]:
    """One state per sealed reading and named stake, replayed from genesis."""

    return [
        (f"{reading.name}/{commitment.name}", ts_replay(genesis_history(reading, commitment)))
        for reading in sealed_readings()
        for commitment in COMMITMENTS
    ]


# ---------------------------------------------------------------------------
# R1-1: the declared space at three items
# ---------------------------------------------------------------------------


class DeclaredSpaceTests(unittest.TestCase):
    """Pins: 'the rung's item-count-parametric generator agrees with the
    sealed unpruned generator at every item count where it defers to it, and
    with an independently written wider construction at every item count from
    zero to three, in both directions, on every base of the declared
    cross-check family of seven.'"""

    def test_the_family_is_eight_real_bases_two_ruled_and_one_two_formed(self) -> None:
        """Pins: 'the declared cross-check family is eight bases built by
        applying sealed deltas to the sealed empty regime, two of which carry
        a uniform rule -- which is what keeps R1-1's third clause from being
        scored over an empty difference on every base -- and one of which
        carries TWO forms of different arity, each with an instance.'

        The eighth base is the reviewer's finding: every other base tops out
        at one form, so the interleaving of two new-form items with the
        arities they introduce was certified nowhere, while seven of the
        nineteen real three-item enumerations run on two-form bases.
        """

        rows = family()
        self.assertEqual(len(rows), EXPECTED_FAMILY_SIZE)
        self.assertEqual(len({name for name, _base in rows}), EXPECTED_FAMILY_SIZE)
        ruled = [name for name, base in rows if base.rules]
        formed = [name for name, base in rows if base.forms]
        instanced = [name for name, base in rows if base.insts]
        multi_formed = [name for name, base in rows if len(base.forms) > 1]
        self.assertEqual(ruled, ["b3_unary_form_ruled", "b6_binary_ruled_three_data"])
        self.assertEqual(len(formed), 6, f"bases carrying a form: {formed}")
        self.assertEqual(
            instanced, ["b5_binary_form_with_instance", "b7_two_forms_with_instances"]
        )
        self.assertEqual(multi_formed, ["b7_two_forms_with_instances"])
        self.assertEqual(dict(rows)["b7_two_forms_with_instances"].forms, (1, 2))
        self.assertEqual(len(dict(rows)["b7_two_forms_with_instances"].insts), 2)
        self.assertEqual(
            sorted(base.n_data() for _name, base in rows), [0, 2, 2, 2, 2, 2, 2, 3]
        )

    def test_the_generator_agrees_with_the_sealed_one_where_it_defers(self) -> None:
        """Pins: 'at item counts zero, one and two the rung yields exactly
        what the sealed unpruned generator yields, on every base of the
        family; the difference is empty in both directions.'  A regression
        guard on the delegation, and nothing more: at those counts the rung
        declares nothing."""

        for name, base in family():
            for cost in (0, 1, 2):
                with self.subTest(base=name, item_count=cost):
                    mine = set(ST.iter_k_item_deltas(base, cost, ST.BOUNDS_THREE))
                    sealed = set(iter_full_deltas(base, cost, ST.BOUNDS_THREE))
                    self.assertEqual(sorted(map(repr, mine - sealed)), [])
                    self.assertEqual(sorted(map(repr, sealed - mine)), [])
                    self.assertTrue(mine, "the space at this item count is not empty")

    def test_the_generator_agrees_with_the_wider_construction_in_both_directions(
        self,
    ) -> None:
        """Pins: 'at item counts zero, two and three the rung's space equals
        the independently written wider construction on every base of the
        family, and at one item the wider construction exceeds it by exactly
        the uniform-rule items on forms that already carry the rule.'  This is
        the check that the three-item universe was widened rather than carried
        over from the two-item constants: a generator still using
        ``len(base.forms) + 1`` and ``range(n0 + 1)`` fails it at three items
        on every base that can offer two new forms or two fresh data."""

        difference_seen = 0
        for name, base in family():
            expected_at_one = {
                canonical_delta((NewRuleAll(int(f)),)) for f in sorted(base.rules)
            }
            for cost in (0, 1, 2, 3):
                with self.subTest(base=name, item_count=cost):
                    mine = set(ST.iter_k_item_deltas(base, cost, ST.BOUNDS_THREE))
                    wider = set(ST.iter_superset_deltas(base, cost, ST.BOUNDS_THREE))
                    self.assertEqual(
                        sorted(map(repr, mine - wider)),
                        [],
                        "the rung offers a delta the wider construction does not",
                    )
                    if cost == 1:
                        self.assertEqual(wider - mine, expected_at_one)
                        difference_seen += len(expected_at_one)
                    else:
                        self.assertEqual(sorted(map(repr, wider - mine)), [])
        self.assertGreater(
            difference_seen,
            0,
            "the one-item difference is empty on every base, so its clause decides nothing",
        )

    def test_the_three_item_space_offers_the_shapes_two_items_cannot(self) -> None:
        """Pins: 'the three-item space offers, for the first time, a delta
        carrying two fresh data and a delta carrying a fresh datum with two
        instances -- the shapes the two-item reasoning does not cover.'"""

        base = dict(family())["b4_binary_form"]
        space = list(ST.iter_k_item_deltas(base, 3, ST.BOUNDS_THREE))
        two_data = [d for d in space if sum(isinstance(i, NewDatum) for i in d) == 2]
        datum_two_insts = [
            d
            for d in space
            if any(isinstance(i, NewDatum) for i in d)
            and sum(isinstance(i, NewInst) for i in d) == 2
        ]
        self.assertTrue(two_data, "no three-item delta carries two fresh data")
        self.assertTrue(datum_two_insts, "no three-item delta carries a datum and two instances")

    def test_the_admission_prefilter_accepts_exactly_what_application_accepts(self) -> None:
        """Pins: 'the admission prefilter is an exact restatement of the
        sealed admission conditions and not a pruning lemma: over the whole
        three-item multiset space of the three smallest bases of the family it
        accepts a candidate exactly when application accepts it.'"""

        bases = dict(family())
        swept = 0
        for name in SWEPT_BASES:
            base = bases[name]
            universe = ST.universe_items(base, 3, ST.BOUNDS_THREE)
            for combo in combinations_with_replacement(universe, 3):
                delta = canonical_delta(combo)
                said = ST.admissible_shape(base, delta)
                try:
                    apply_delta(base, delta)
                    applied = True
                except AdmissionError:
                    applied = False
                swept += 1
                if said != applied:  # pragma: no cover - reported, never expected
                    self.fail(
                        f"{name}: prefilter said {said} and application said "
                        f"{applied} for {delta!r}"
                    )
        self.assertGreater(swept, 60000, f"the sweep examined only {swept} candidates")

    def test_the_datum_bearing_subspace_is_a_restriction_and_not_a_prune(self) -> None:
        """Pins: 'the census space is the declared space restricted to the
        deltas carrying at least one datum item -- every such delta is
        produced exactly once and nothing else is.'  The census counts a zero
        only if it looked at everything it claims to have looked at."""

        bases = dict(family())
        for name in SWEPT_BASES:
            base = bases[name]
            for cost in (1, 2, 3):
                with self.subTest(base=name, item_count=cost):
                    _made, space = ST.fresh_datum_space(base, cost, ST.BOUNDS_THREE)
                    got = [delta for delta, _after in space]
                    want = [
                        d
                        for d in ST.iter_k_item_deltas(base, cost, ST.BOUNDS_THREE)
                        if has_fresh_datum(d)
                    ]
                    self.assertEqual(len(got), len(set(got)), "a delta was produced twice")
                    self.assertEqual(set(got), set(want))

    def test_the_candidate_count_is_the_number_of_multisets_examined(self) -> None:
        """Pins: 'a candidate examined is one multiset over the declared
        universe, counted whether the admission conditions then accept it or
        reject it, so the candidate budget is answerable before an enumeration
        rather than part way through one.'"""

        bases = dict(family())
        for name in SWEPT_BASES:
            base = bases[name]
            universe = ST.universe_items(base, 3, ST.BOUNDS_THREE)
            walked = sum(1 for _ in combinations_with_replacement(universe, 3))
            self.assertEqual(ST.candidate_count(base, 3, ST.BOUNDS_THREE), walked)
        self.assertEqual(ST.multiset_count(0, 0), 1)
        self.assertEqual(ST.multiset_count(0, 3), 0)
        self.assertEqual(ST.multiset_count(4, 2), 10)

    def test_the_receipt_records_the_cross_check_this_test_recomputes(self) -> None:
        """Pins: 'R1-1 is HIT: all three clauses hold on all seven bases.'"""

        cross = _obj(load_receipt()["cross_check"])
        self.assertEqual(_num(cross["family_size"]), EXPECTED_FAMILY_SIZE)
        self.assertTrue(_flag(cross["agrees_with_sealed_at_zero_one_two"]))
        self.assertTrue(_flag(cross["agrees_with_wider_at_zero_two_three"]))
        self.assertTrue(_flag(cross["one_item_difference_is_closed_form_on_every_base"]))
        self.assertTrue(_flag(cross["one_item_difference_non_empty_on_some_base"]))


# ---------------------------------------------------------------------------
# R1-2: the reconstruction at the sibling's own item bound
# ---------------------------------------------------------------------------


class TwoItemReconstructionTests(unittest.TestCase):
    """Pins: 'with its own item bound set to two, the rung's reconstructed
    loop reproduces, for all twenty tree identities, the node count, the
    status histogram, the edge count and the refusal list stored in the
    committed sibling receipt.'"""

    def test_twenty_trees_are_built_and_the_pinned_record_names_twenty(self) -> None:
        """Pins: 'the rectangle is twenty runs: two sealed readings, five
        named stakes, two sealed measures.'"""

        built = two_item_trees()
        pinned = load_sibling()
        self.assertEqual(len(built), EXPECTED_RUNS)
        self.assertEqual(len(pinned), EXPECTED_RUNS)
        self.assertEqual(sorted(ident for ident, _t in built), sorted(pinned))

    def test_the_four_quantities_reproduce_the_committed_sibling_record(self) -> None:
        """Pins: 'all four quantities agree for all twenty trees.'  Compared
        here against the committed sibling receipt directly, not against this
        rung's own summary of it."""

        pinned = load_sibling()
        for ident, tree in two_item_trees():
            with self.subTest(tree=ident):
                stats = tree.stats()
                want = _obj(pinned[ident]["stats"])
                self.assertEqual(_num(stats["nodes"]), _num(want["nodes"]))
                self.assertEqual(_num(stats["edges"]), _num(want["edges"]))
                self.assertEqual(_obj(stats["by_status"]), _obj(want["by_status"]))
                mine = [dict(rec) for rec in tree.tree.refusals]
                theirs = [_obj(rec) for rec in _arr(pinned[ident]["refusals"])]
                self.assertEqual(mine, theirs)

    def test_the_recorded_two_item_refusals_are_fifteen_nodes_of_the_same_kind(self) -> None:
        """Pins: 'the pinned two-item record carries fifteen refusal records,
        every one of them a demand of the same kind, spread over the three
        runs L/parity/mu1, L/residue_three/mu1 and F/parity/mu1.'"""

        total = 0
        kinds: set[str] = set()
        with_a_refusal: list[str] = []
        for ident, tree in two_item_trees():
            if tree.tree.refusals:
                with_a_refusal.append(ident)
            for rec in tree.tree.refusals:
                total += 1
                kinds.add(_txt(rec["kind"]))
        self.assertEqual(total, EXPECTED_TWO_ITEM_REFUSAL_RECORDS)
        self.assertEqual(kinds, {SAME})
        self.assertEqual(
            sorted(with_a_refusal),
            sorted(RS.NAMED_RUNS_WITH_A_REFUSAL),
        )

    def test_the_selection_agrees_delta_for_delta_with_the_public_sibling_one(self) -> None:
        """Pins: 'the rung's selection returns delta-for-delta and
        cost-for-cost what the public sibling selection returns at every state
        and demanded pair of the twenty two-item runs -- 744 comparisons, no
        disagreement.'  The rung declares its own no-op filter and its own
        ordering because the sibling's helpers of that effect are private;
        this is the certificate for both."""

        comparisons = 0
        disagreements: list[str] = []
        for ident, tree in two_item_trees():
            measure = tree.tree.measure
            for node in tree.tree.nodes:
                for target in closure_targets(node.state):
                    mine = ST.min_responses_three(
                        node.state, target, measure, ST.BOUNDS_TWO, ST.RULE_NO_REGRESS
                    )
                    theirs = min_responses(node.state, target, measure, ST.BOUNDS_TWO)
                    comparisons += 1
                    where = f"{ident} node {node.node_id} {target[0]}{target[1]}"
                    if (mine is None) != (theirs is None):
                        disagreements.append(f"{where}: one refused and the other did not")
                    elif mine is not None and theirs is not None:
                        if mine.deltas != theirs.deltas:
                            disagreements.append(f"{where}: deltas differ")
                        elif mine.cost != theirs.cost:
                            disagreements.append(
                                f"{where}: cost {mine.cost} against {theirs.cost}"
                            )
        self.assertEqual(disagreements[:8], [])
        self.assertEqual(comparisons, EXPECTED_SELECTION_COMPARISONS)

    def test_the_receipt_records_the_reconstruction_this_test_recomputes(self) -> None:
        """Pins: 'R1-2 is HIT: twenty trees built against twenty pinned, all
        four quantities agreeing, and 744 selection comparisons with no
        disagreement.'"""

        recon = _obj(load_receipt()["two_item_reconstruction"])
        self.assertEqual(_num(recon["trees_built"]), EXPECTED_RUNS)
        self.assertEqual(_num(recon["trees_pinned"]), EXPECTED_RUNS)
        self.assertEqual(_num(recon["item_bound"]), 2)
        self.assertEqual(_txt(recon["validity_rule"]), ST.RULE_NO_REGRESS)
        self.assertTrue(_flag(recon["all_four_quantities_agree"]))
        self.assertTrue(_flag(recon["selection_agrees_everywhere"]))
        self.assertEqual(
            _num(recon["selection_comparisons"]), EXPECTED_SELECTION_COMPARISONS
        )
        self.assertEqual(_arr(recon["selection_mismatch_exhibits"]), [])


# ---------------------------------------------------------------------------
# The committed receipt
# ---------------------------------------------------------------------------


class ReceiptReplayTests(unittest.TestCase):
    """Pins: 'the committed receipt replays byte for byte from the entry
    point; a second invocation writes the same bytes, and the receipt carries
    no reading of a clock and no environment value.'"""

    def test_the_committed_receipt_replays_byte_for_byte(self) -> None:
        """Pins: 'receipts/stream.json regenerates byte-identically.'"""

        fresh, _gz, _report = replay()
        committed = RECEIPT.read_bytes()
        self.assertEqual(len(fresh), len(committed), "the receipt changed size")
        self.assertEqual(
            hashlib.sha256(fresh).hexdigest(), hashlib.sha256(committed).hexdigest()
        )
        self.assertEqual(fresh, committed)

    def test_the_committed_receipt_carries_no_carriage_return(self) -> None:
        """Pins: 'the receipt is LF-only, and its own serialization block says
        so from the bytes rather than from a policy.'"""

        self.assertNotIn(b"\r", RECEIPT.read_bytes())
        serial = _obj(load_receipt()["serialization"])
        self.assertFalse(_flag(serial["body_contains_a_carriage_return"]))
        self.assertTrue(_flag(serial["body_renders_identically_twice"]))

    def test_the_compressed_export_carries_the_content_the_receipt_hashes(self) -> None:
        """Pins: 'the compressed export holds the per-node census rows and the
        per-run edges, and the summary records the hash of its UNCOMPRESSED
        bytes.'  Compressed bytes are deliberately not compared: this
        repository records that a local compression library rewrites them
        without changing the content."""

        _fresh, gz_bytes, _report = replay()
        committed_content = read_json_gz(FULL)
        fresh_content = read_json_gz_bytes(gz_bytes)
        self.assertEqual(fresh_content, committed_content)
        recorded = _obj(load_receipt()["full_export"])
        digest = hashlib.sha256(dumps_deterministic(committed_content)).hexdigest()
        self.assertEqual(_txt(recorded["sha256_uncompressed"]), digest)
        self.assertEqual(_txt(recorded["path"]), RS.FULL_PATH)

    def test_both_receipts_carry_no_authority(self) -> None:
        self.assertEqual(_txt(load_receipt()["authority_effect"]), "None")
        self.assertEqual(_txt(_obj(read_json_gz(FULL))["authority_effect"]), "None")

    def test_frozen_disk_drift_refuses_before_touching_outputs(self) -> None:
        self.assertEqual(
            RS.verify_frozen_disk(),
            {path: digest for path, digest in RS.FROZEN_DISK_SHA256},
        )
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            frozen = root / "PROMPT.md"
            frozen.write_text("changed after freeze", encoding="utf-8")
            out = root / "stream.json"
            full = root / "full.json.gz"
            out.write_bytes(b"summary sentinel")
            full.write_bytes(b"full sentinel")
            stdout = io.StringIO()
            with (
                mock.patch.object(RS, "FROZEN_DISK_SHA256", ((frozen, "0" * 64),)),
                contextlib.redirect_stdout(stdout),
            ):
                code = RS.main(["--out", str(out), "--full", str(full)])
            self.assertEqual(code, 1)
            self.assertIn("frozen text moved on disk", stdout.getvalue())
            self.assertEqual(out.read_bytes(), b"summary sentinel")
            self.assertEqual(full.read_bytes(), b"full sentinel")

    def test_frozen_drift_during_build_refuses_before_touching_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            frozen = root / "PROMPT.md"
            frozen.write_text("frozen", encoding="utf-8")
            digest = hashlib.sha256(frozen.read_bytes()).hexdigest()
            out = root / "stream.json"
            full = root / "full.json.gz"
            out.write_bytes(b"summary sentinel")
            full.write_bytes(b"full sentinel")

            def mutate_during_build(*_args: object) -> dict[str, Json]:
                frozen.write_text("moved during build", encoding="utf-8")
                return {}

            stdout = io.StringIO()
            with (
                mock.patch.object(RS, "FROZEN_DISK_SHA256", ((frozen, digest),)),
                mock.patch.object(RS, "build_all", side_effect=mutate_during_build),
                contextlib.redirect_stdout(stdout),
            ):
                code = RS.main(["--out", str(out), "--full", str(full)])
            self.assertEqual(code, 1)
            self.assertIn("frozen text moved on disk", stdout.getvalue())
            self.assertEqual(out.read_bytes(), b"summary sentinel")
            self.assertEqual(full.read_bytes(), b"full sentinel")

    def test_the_frozen_texts_hash_to_what_the_receipt_records(self) -> None:
        """Pins: 'the frozen question and the frozen predictions were hashed
        before the first run and have not been edited since; the receipt
        carries both digests.'"""

        receipt = load_receipt()
        prompt = hashlib.sha256((HERE / "PROMPT.md").read_bytes()).hexdigest()
        predictions = hashlib.sha256((HERE / "PREDICTIONS.md").read_bytes()).hexdigest()
        self.assertEqual(prompt, FROZEN_PROMPT_SHA)
        self.assertEqual(predictions, FROZEN_PREDICTIONS_SHA)
        self.assertEqual(_txt(receipt["prompt_sha256"]), FROZEN_PROMPT_SHA)
        self.assertEqual(_txt(receipt["predictions_sha256"]), FROZEN_PREDICTIONS_SHA)

    def test_the_run_reports_the_headline_quantities_the_prose_quotes(self) -> None:
        """Pins: 'twenty runs, 1974 nodes, 2209 edges; 0 of 1680 retained
        minima carry a datum item, and 32 of those 1680 were selected from the
        three-item space, in 3 of 20 runs; two refusal records at three items,
        all in L/parity/mu1; twenty enumerations actually performed at three
        items.'  A zero here is a counted zero: the companion counter says the
        three-item enumerations happened.

        The three-item clause is the repair.  The headline was stated over
        1680 edges while only 32 of them were selected from the space this
        rung declares -- 1648 came from one or two items, which is the
        sibling's bound -- and no key of the receipt let a reader recover the
        32.  R1-3, scored HIT over seventeen runs, already establishes that
        most of the rectangle is byte-identical to the pinned two-item record.
        """

        agg = _obj(load_receipt()["aggregate"])
        counters = _obj(agg["counters"])
        self.assertEqual(_num(agg["runs"]), EXPECTED_RUNS)
        self.assertEqual(_num(agg["nodes"]), EXPECTED_NODES)
        self.assertEqual(_num(agg["edges"]), EXPECTED_EDGES)
        self.assertEqual(_num(agg["response_edges"]), EXPECTED_RESPONSE_EDGES)
        self.assertEqual(
            _num(agg["edges_with_datum_item"]), EXPECTED_EDGES_WITH_DATUM_ITEM
        )
        self.assertEqual(
            {k: _num(v) for k, v in _obj(agg["response_edges_by_item_count"]).items()},
            EXPECTED_EDGES_BY_ITEM_COUNT,
        )
        self.assertEqual(
            sum(EXPECTED_EDGES_BY_ITEM_COUNT.values()), EXPECTED_RESPONSE_EDGES
        )
        self.assertEqual(
            _num(agg["edges_selected_at_three_items"]), EXPECTED_EDGES_AT_THREE_ITEMS
        )
        self.assertEqual(
            {
                k: _num(v)
                for k, v in _obj(agg["runs_with_a_three_item_selection"]).items()
            },
            EXPECTED_RUNS_WITH_A_THREE_ITEM_SELECTION,
        )
        self.assertEqual(
            _num(agg["nodes_stopped_by_the_node_guard"]),
            EXPECTED_NODES_STOPPED_BY_THE_GUARD,
        )
        self.assertEqual(
            sorted(_obj(agg["runs_truncated_by_the_node_guard"])),
            EXPECTED_RUNS_TRUNCATED_BY_THE_GUARD,
        )
        self.assertEqual(
            _num(agg["refusal_records"]), EXPECTED_REFUSAL_RECORDS_AT_THREE_ITEMS
        )
        self.assertEqual(
            [_txt(v) for v in _arr(agg["runs_with_a_refusal"])],
            EXPECTED_RUNS_WITH_A_REFUSAL,
        )
        self.assertEqual(
            _num(counters["three_item_enumerations_performed"]),
            EXPECTED_THREE_ITEM_ENUMERATIONS,
        )
        self.assertEqual(_num(counters["nodes_censused"]), EXPECTED_NODES)
        self.assertFalse(_flag(agg["unhandled_abort"]))

    def test_the_refusal_situations_are_fourteen_and_every_one_is_answered(self) -> None:
        """Pins: 'the fifteen recorded refusal nodes present fourteen distinct
        situations, and all fourteen are answered by a response of exactly
        three items under the inherited no-regress rule.'  Fifteen counts
        NODES, not situations."""

        rect = _obj(load_receipt()["rectangle_a"])
        self.assertEqual(
            _num(rect["refusal_records"]), EXPECTED_TWO_ITEM_REFUSAL_RECORDS
        )
        self.assertEqual(
            _num(rect["distinct_situations"]), EXPECTED_TWO_ITEM_REFUSAL_SITUATIONS
        )
        self.assertEqual(
            _num(rect["situations_answered_at_exactly_three_items"]),
            EXPECTED_SITUATIONS_ANSWERED,
        )
        self.assertEqual(_txt(rect["validity_rule_of_the_refusal_population"]),
                         ST.RULE_NO_REGRESS)

    def test_the_printed_report_names_every_prediction_and_the_headline(self) -> None:
        """Pins: 'the run prints one line per prediction with its verdict and
        a summary line, so the verdicts are readable without opening the
        receipt.'"""

        _fresh, _gz, report = replay()
        for name in _obj(load_receipt()["predictions_scored"]):
            self.assertIn(f"{name}:", report)
        self.assertIn("rung 1 at item bound 3", report)
        self.assertIn("HIT=", report)
        self.assertIn("MISSED=", report)
        self.assertIn(
            f"{EXPECTED_EDGES_WITH_DATUM_ITEM} of {EXPECTED_RESPONSE_EDGES} retained "
            f"minima carry a datum item",
            report,
        )
        self.assertIn(
            f"{EXPECTED_EDGES_AT_THREE_ITEMS} of those {EXPECTED_RESPONSE_EDGES} were "
            f"selected from the three-item space",
            report,
        )
        self.assertIn(
            f"{EXPECTED_NODES_STOPPED_BY_THE_GUARD} nodes stopped by the node guard",
            report,
        )


def read_json_gz_bytes(raw: bytes) -> Json:
    """The compressed export's content, read out of bytes in hand."""

    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "x.json.gz"
        path.write_bytes(raw)
        return read_json_gz(path)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


class ScoringTests(unittest.TestCase):
    """Pins: 'scoring is mechanical, is a function of the receipt's own body,
    and is not a rubber stamp: it returns MISSED on a body that should score
    MISSED and VACUOUS on an emptied population, and it did return MISSED on
    this run.'"""

    def body(self) -> dict[str, Json]:
        return copy.deepcopy(load_receipt())

    def test_the_scorer_reproduces_the_verdicts_the_receipt_stores(self) -> None:
        """Pins: 'every verdict in the receipt is recomputable from the
        receipt's own body by the committed scorer.'"""

        receipt = load_receipt()
        scored, detail = RS.score_predictions(self.body())
        self.assertEqual(scored, _obj(receipt["predictions_scored"]))
        self.assertEqual(detail, _obj(receipt["prediction_detail"]))

    def test_the_scored_population_is_the_twelve_frozen_predictions(self) -> None:
        """Pins: 'eleven predictions plus the extrapolation are scored; the
        extrapolation is PENDING because it speaks of a rectangle this rung
        does not compute.'"""

        scored, _detail = RS.score_predictions(self.body())
        self.assertEqual(
            sorted(scored),
            sorted(
                ["R1-X"] + [f"R1-{n}" for n in range(1, 12)]
            ),
        )
        self.assertEqual(_txt(_at(_obj(scored["R1-X"]), "verdict")), RS.VERDICT_PENDING)
        self.assertFalse(_flag(_at(_obj(scored["R1-X"]), "hit")))

    def test_r1_9_is_recorded_missed_and_that_is_the_run_s_own_finding(self) -> None:
        """Pins: 'R1-9 is MISSED.  The two-item census records 219 priced-out
        rows, but 58 of them answer a demand of the same kind, and the
        prediction bet that every priced-out row would answer a demand of the
        apart kind.'  This is the verdict that shows the scorer is not a
        rubber stamp on this very run."""

        scored, detail = RS.score_predictions(self.body())
        self.assertEqual(_txt(_at(_obj(scored["R1-9"]), "verdict")), RS.VERDICT_MISSED)
        row = _obj(detail["R1-9"])
        self.assertGreater(_num(row["priced_out_rows"]), 0)
        self.assertGreater(_num(row["priced_out_rows_of_the_same_kind"]), 0)
        self.assertGreater(_num(row["three_item_enumerations_performed"]), 0)

    def test_the_scorer_returns_missed_on_a_body_built_to_be_missed(self) -> None:
        """Pins: 'the scorer can emit MISSED: a synthetic body carrying one
        retained minimum with a datum item scores the headline MISSED, and the
        same construction moves R1-7, R1-8 and R1-10 off HIT.'  Without this
        the eleven HITs would only show that the scorer says HIT."""

        cases: list[tuple[str, list[str], Json]] = [
            ("R1-4", ["aggregate", "edges_with_datum_item"], 1),
            ("R1-5", ["enumeration_situations", "same_kind_valid_with_datum_item"], 3),
            (
                "R1-6",
                [
                    "enumeration_situations",
                    "same_kind_valid_without_two_instances_and_without_a_rule",
                ],
                2,
            ),
            ("R1-7", ["rectangle_a", "situations_answered_at_exactly_three_items"], 0),
            ("R1-8", ["aggregate", "refusal_records"], 0),
            ("R1-11", ["rectangle_a", "distinct_situations"], 15),
        ]
        for name, path, value in cases:
            with self.subTest(prediction=name):
                body = self.body()
                _set(body, path, value)
                scored, _detail = RS.score_predictions(body)
                self.assertEqual(
                    _txt(_at(_obj(scored[name]), "verdict")),
                    RS.VERDICT_MISSED,
                    f"{name} stayed {scored[name]!r} after {path} was set to {value!r}",
                )
                self.assertFalse(_flag(_at(_obj(scored[name]), "hit")))

    def test_a_fired_budget_moves_the_no_truncation_prediction_to_missed(self) -> None:
        """Pins: 'a truncation is a MISS and a finding, never a silent
        footnote: R1-10 goes MISSED as soon as one declared budget terminal
        appears in the receipt.'"""

        for terminal in ST.BUDGET_TERMINALS:
            with self.subTest(terminal=terminal):
                body = self.body()
                _set(body, ["aggregate", "budget_terminals_fired"], [terminal])
                scored, _detail = RS.score_predictions(body)
                self.assertEqual(
                    _txt(_at(_obj(scored["R1-10"]), "verdict")), RS.VERDICT_MISSED
                )
        body = self.body()
        _set(body, ["wall_clock_truncation", "truncated"], True)
        scored, _detail = RS.score_predictions(body)
        self.assertEqual(_txt(_at(_obj(scored["R1-10"]), "verdict")), RS.VERDICT_MISSED)

    def test_an_empty_population_scores_vacuous_and_is_never_rounded_up(self) -> None:
        """Pins: 'a prediction whose population turns out empty is scored
        VACUOUS and is recorded as evidence of nothing; the verdict is never
        rounded up to HIT.'  Each case below empties a population while
        LEAVING THE HIT CONDITION SATISFIED, so a presence-blind scorer would
        return HIT on zero candidates -- the all-hit failure the rung's own
        trap list names."""

        cases: list[tuple[str, list[str]]] = [
            ("R1-1", ["cross_check", "family_size"]),
            ("R1-2", ["two_item_reconstruction", "trees_built"]),
            ("R1-3", ["three_item_versus_pinned", "rows_compared"]),
            ("R1-4", ["aggregate", "response_edges"]),
            ("R1-5", ["enumeration_situations", "same_kind_situations"]),
            (
                "R1-6",
                ["enumeration_situations", "same_kind_valid_three_item_responses"],
            ),
            ("R1-7", ["rectangle_a", "situations_examined"]),
            ("R1-8", ["aggregate", "runs"]),
            ("R1-9", ["availability", "census_two_rows"]),
            ("R1-11", ["rectangle_a", "refusal_records"]),
        ]
        for name, path in cases:
            with self.subTest(prediction=name):
                body = self.body()
                _set(body, path, 0)
                scored, _detail = RS.score_predictions(body)
                self.assertEqual(
                    _txt(_at(_obj(scored[name]), "verdict")),
                    RS.VERDICT_VACUOUS,
                    f"{name} was scored on an empty population",
                )
                self.assertFalse(_flag(_at(_obj(scored[name]), "hit")))

    def test_r1_6_scores_vacuous_when_no_same_demand_is_answered_at_three_items(
        self,
    ) -> None:
        """Pins: 'R1-6's population is the valid three-item responses to a
        demand of the same kind; had the three-item space answered none of
        them, R1-6 would have been VACUOUS rather than HIT.'  The frozen text
        declares that outcome in advance, which is why it is checked here."""

        body = self.body()
        _set(body, ["enumeration_situations", "same_kind_valid_three_item_responses"], 0)
        _set(
            body,
            [
                "enumeration_situations",
                "same_kind_valid_without_two_instances_and_without_a_rule",
            ],
            0,
        )
        scored, _detail = RS.score_predictions(body)
        self.assertEqual(_txt(_at(_obj(scored["R1-6"]), "verdict")), RS.VERDICT_VACUOUS)

    def test_scoring_reads_the_body_and_nothing_else(self) -> None:
        """Pins: 'the scorer opens no file, builds no tree and reads no clock,
        so a reader can recompute every verdict from the committed receipt
        alone.'  Checked by scoring a body whose paths do not exist and whose
        digests are wrong: the verdicts are unchanged."""

        body = self.body()
        _set(body, ["prompt_sha256"], "0" * 64)
        _set(body, ["predictions_sha256"], "0" * 64)
        _set(body, ["assumptions"], [])
        scored, _detail = RS.score_predictions(body)
        self.assertEqual(scored, _obj(load_receipt()["predictions_scored"]))


# ---------------------------------------------------------------------------
# The declared validity class
# ---------------------------------------------------------------------------


class ValidityClassTests(unittest.TestCase):
    """Pins: 'the class has two members: the inherited no-regress rule, and
    the member this rung declares, which is STRICTLY stronger -- an exhibited
    delta at an exhibited state is accepted by the first and refused by the
    second.'  Decided by running, not by assumption."""

    EXHIBIT_STATE = ("L", "total_apart")
    EXHIBIT_TARGET: tuple[str, Pair] = ("apart", (0, 1))

    def exhibit(self) -> tuple[TState, Delta]:
        reading = [r for r in sealed_readings() if r.name == self.EXHIBIT_STATE[0]][0]
        state = ts_replay(genesis_history(reading, commitment_named(self.EXHIBIT_STATE[1])))
        delta = canonical_delta((NewDatum(), NewForm(1), NewInst(0, (0,))))
        return state, delta

    def test_the_declared_member_refuses_a_delta_the_inherited_member_accepts(self) -> None:
        """Pins: 'the declared member is strictly stronger, exhibited at the
        L/total_apart genesis state on the demanded pair (0, 1) by the
        three-item delta (fresh datum, unary form, instance of that form on
        the fresh datum): the inherited member accepts it, because a pair
        involving a datum the response introduces is a new demand rather than
        regress, and the declared member refuses it, because it requires those
        new pairs to be honoured too.'"""

        state, delta = self.exhibit()
        target = self.EXHIBIT_TARGET
        self.assertIn(delta, set(ST.iter_k_item_deltas(state.regime, 3, ST.BOUNDS_THREE)))
        self.assertTrue(ST.response_valid(state, target, delta))
        self.assertFalse(ST.strict_response_valid(state, target, delta))

    def test_the_declared_member_accepts_nothing_the_inherited_one_refuses(self) -> None:
        """Pins: 'the declared member's valid set is contained in the
        inherited member's at every state, demanded pair and delta of the
        exhibited rectangle: it adds one conjunct and removes none.'  Swept
        over both readings, all five stakes and every delta of at most three
        items at the genesis states."""

        separations = 0
        for name, state in genesis_states():
            for target in closure_targets(state):
                for cost in (1, 2, 3):
                    for delta in ST.iter_k_item_deltas(state.regime, cost, ST.BOUNDS_THREE):
                        one = ST.response_valid(state, target, delta)
                        two = ST.strict_response_valid(state, target, delta)
                        if two and not one:  # pragma: no cover - reported, never expected
                            self.fail(
                                f"{name} {target}: the declared member accepted "
                                f"{delta!r} which the inherited member refused"
                            )
                        if one and not two:
                            separations += 1
        self.assertGreater(
            separations,
            0,
            "the two members agree everywhere in the swept rectangle, so the "
            "declared member is not strictly stronger there",
        )

    def test_the_judge_decides_what_the_imported_members_decide(self) -> None:
        """Pins: 'the per-candidate judge is a restructuring and not a third
        member: at every state, demanded pair and delta of at most two items
        of the genesis rectangle it accepts exactly what the member it names
        accepts.'"""

        for name, state in genesis_states():
            for target in closure_targets(state):
                for rule, fn in ST.VALIDITY_RULES:
                    judge = ST.Judge(state, target, rule)
                    for cost in (0, 1, 2):
                        for delta in ST.iter_k_item_deltas(
                            state.regime, cost, ST.BOUNDS_THREE
                        ):
                            after = apply_delta(state.regime, delta)
                            if judge.accepts(delta, after) != fn(state, target, delta):
                                self.fail(  # pragma: no cover - never expected
                                    f"{name} {target} {rule}: the judge and the "
                                    f"member disagree on {delta!r}"
                                )

    def test_a_member_is_named_or_the_lookup_fails(self) -> None:
        """Pins: 'every recorded row names the validity member that produced
        it, and a name outside the declared class is refused rather than
        defaulted.'"""

        self.assertIs(ST.validity_named(ST.RULE_NO_REGRESS), ST.response_valid)
        self.assertIs(ST.validity_named(ST.RULE_STRICT_NO_REGRESS), ST.strict_response_valid)
        with self.assertRaises(KeyError):
            ST.validity_named("zzz_not_a_member")
        state, _delta = self.exhibit()
        with self.assertRaises(KeyError):
            ST.Judge(state, self.EXHIBIT_TARGET, "zzz_not_a_member")

    def test_where_each_member_is_run_is_recorded(self) -> None:
        """Pins: 'the inherited member governs the twenty runs of the
        rectangle, the twenty runs of the two-item reconstruction, both
        censuses and the re-derivation of the refusal population; the declared
        member is run on the deduplicated situations and nowhere else.'"""

        block = _obj(load_receipt()["validity_class"])
        self.assertEqual(_txt(block["inherited_member"]), ST.RULE_NO_REGRESS)
        self.assertEqual(_txt(block["declared_member"]), ST.RULE_STRICT_NO_REGRESS)
        self.assertEqual(len(_arr(block["inherited_member_runs"])), 6)
        self.assertEqual(len(_arr(block["declared_member_runs"])), 2)
        for row in _arr(_obj(load_receipt()["rectangle_a"])["rows"]):
            entry = _obj(row)
            for rule in (ST.RULE_NO_REGRESS, ST.RULE_STRICT_NO_REGRESS):
                self.assertEqual(
                    _txt(_at(_obj(entry[f"by_{rule}"]), "validity_rule")), rule
                )


# ---------------------------------------------------------------------------
# The declared budgets
# ---------------------------------------------------------------------------


class BudgetTests(unittest.TestCase):
    """Pins: 'each declared budget carries its own terminal naming the tree,
    the node and the demanded pair at which it fired, and a node whose
    gathering is cut short attaches nothing.'  Each is driven to fire by
    setting it small; none fired in the committed run."""

    def reading_named(self, name: str) -> Reading:
        return [r for r in sealed_readings() if r.name == name][0]

    def assert_row_names_tree_node_and_pair(
        self, row: Mapping[str, object], terminal: str, tree: str
    ) -> None:
        self.assertEqual(_txt(row["terminal"]), terminal)
        self.assertEqual(_txt(row["tree"]), tree)
        self.assertGreaterEqual(_num(row["node"]), 0)
        self.assertIn(_txt(row["kind"]), (ST.SAME, ST.APART))
        self.assertEqual(len(_arr(row["target"])), 2)
        self.assertEqual(_num(row["attached"]), 0)

    def test_the_class_budget_fires_and_the_node_attaches_nothing(self) -> None:
        """Pins: 'the retained-class budget fires at the node whose retained
        classes pass it, records the class count against the bound, and
        attaches nothing.'"""

        reading = self.reading_named("L")
        with mock.patch.object(ST, "MAX_CLASSES_PER_NODE", 1):
            tree = ST.build_stream_tree(
                reading,
                commitment_named("total_apart"),
                "mu1",
                ST.BOUNDS_TWO,
                ST.RULE_NO_REGRESS,
                census=False,
            )
        rows = [
            r
            for r in tree.truncations
            if _txt(r["terminal"]) == ST.TERMINAL_CLASS_BUDGET
        ]
        self.assertTrue(rows, "the retained-class budget did not fire")
        row = dict(rows[0])
        self.assert_row_names_tree_node_and_pair(
            row, ST.TERMINAL_CLASS_BUDGET, "L/total_apart/mu1"
        )
        self.assertEqual(_num(row["bound"]), 1)
        self.assertGreater(_num(row["classes"]), 1)
        self.assertEqual(
            tree.tree.nodes[_num(row["node"])].status, ST.TERMINAL_CLASS_BUDGET
        )
        self.assertEqual(
            [e for e in tree.tree.edges if e.parent == _num(row["node"])], []
        )

        targets = ((ST.SAME, (0, 1)), (ST.APART, (0, 1)), (ST.SAME, (1, 2)))
        minima = ST.Minima3("mu1", (1, -1), ((),), 1, ST.RULE_NO_REGRESS, 1)
        quotient = mock.Mock(
            side_effect=(
                [((), 1)],
                [((), 1), ((), 1)],
                AssertionError("third target was quotiented"),
            )
        )
        with (
            mock.patch.object(ST, "closure_targets", return_value=targets),
            mock.patch.object(ST, "min_responses_three", return_value=minima),
            mock.patch.object(ST, "_quotient", quotient),
            mock.patch.object(ST, "MAX_CLASSES_PER_NODE", 2),
        ):
            crossed = ST.build_stream_tree(
                reading,
                commitment_named("total_apart"),
                "mu1",
                ST.BOUNDS_TWO,
                ST.RULE_NO_REGRESS,
                census=False,
            )
        self.assertEqual(quotient.call_count, 2)
        crossed_row = dict(crossed.truncations[0])
        self.assertEqual(_txt(crossed_row["kind"]), ST.APART)
        self.assertEqual(_arr(crossed_row["target"]), [0, 1])
        self.assertEqual(_num(crossed_row["classes"]), 3)
        self.assertEqual(_num(crossed_row["targets_gathered"]), 2)
        self.assertEqual(_num(crossed_row["targets_not_reached"]), 1)
        self.assertEqual(crossed.tree.edges, [])

    def test_the_response_budget_fires_and_no_partial_gathering_is_kept(self) -> None:
        """Pins: 'the gathered-response budget fires at the demanded pair
        whose valid set passes it, and the node keeps no partially gathered
        minimum.'"""

        reading = self.reading_named("L")
        with mock.patch.object(ST, "MAX_VALID_PER_TARGET", 1):
            tree = ST.build_stream_tree(
                reading,
                commitment_named("total_apart"),
                "mu1",
                ST.BOUNDS_TWO,
                ST.RULE_NO_REGRESS,
                census=False,
            )
        rows = [
            r for r in tree.truncations if _txt(r["terminal"]) == ST.TERMINAL_RESPONSE_BUDGET
        ]
        self.assertTrue(rows, "the gathered-response budget did not fire")
        row = dict(rows[0])
        self.assert_row_names_tree_node_and_pair(
            row, ST.TERMINAL_RESPONSE_BUDGET, "L/total_apart/mu1"
        )
        self.assertEqual(_num(row["bound"]), 1)
        self.assertGreater(_num(row["valid_gathered"]), 1)
        self.assertEqual(_num(row["targets_gathered"]), 0)

    def test_the_response_budget_stops_consuming_at_bound_plus_one(self) -> None:
        """The response cap bounds the walk, not only the retained list."""

        state, target, _delta = FreshWithFreshTests().state_and_delta()
        consumed = 0

        def offered(*_args: object):  # type: ignore[no-untyped-def]
            nonlocal consumed
            for _ in range(20):
                consumed += 1
                yield (), state.regime

        judge = mock.Mock()
        judge.accepts.return_value = True
        counters = ST.Counters()
        with (
            mock.patch.object(ST, "iter_k_item_deltas_applied", offered),
            mock.patch.object(ST, "has_noop_item", return_value=False),
            mock.patch.object(ST, "Judge", return_value=judge),
            mock.patch.object(ST, "MAX_VALID_PER_TARGET", 2),
        ):
            with self.assertRaises(ST.BudgetExceeded) as caught:
                ST.min_responses_three(
                    state, target, "mu1", ST.BOUNDS_TWO, counters=counters
                )
        self.assertEqual(caught.exception.terminal, ST.TERMINAL_RESPONSE_BUDGET)
        self.assertEqual(consumed, 3)
        self.assertEqual(counters.deltas_offered, 3)

    def test_the_enumeration_budget_fires_at_the_first_three_item_reach(self) -> None:
        """Pins: 'the per-run enumeration budget is counted at the item count
        it governs: it fires only where a three-item enumeration is reached,
        which is only where every response of fewer items fails, and the run
        that reaches one is L/parity/mu1.'"""

        reading = self.reading_named("L")
        with mock.patch.object(ST, "MAX_ENUMERATIONS_PER_RUN", 0):
            tree = ST.build_stream_tree(
                reading,
                commitment_named("parity"),
                "mu1",
                ST.BOUNDS_THREE,
                ST.RULE_NO_REGRESS,
                census=False,
            )
        rows = [
            r
            for r in tree.truncations
            if _txt(r["terminal"]) == ST.TERMINAL_ENUMERATION_BUDGET
        ]
        self.assertTrue(rows, "the per-run enumeration budget did not fire")
        row = dict(rows[0])
        self.assert_row_names_tree_node_and_pair(
            row, ST.TERMINAL_ENUMERATION_BUDGET, "L/parity/mu1"
        )
        self.assertEqual(_num(row["item_count"]), 3)
        self.assertEqual(_num(row["bound"]), 0)
        self.assertEqual(_num(row["enumerations_performed"]), 1)

    def test_the_candidate_budget_fires_before_the_enumeration_it_governs(self) -> None:
        """Pins: 'the candidate budget is answered BEFORE an enumeration
        rather than part way through one: the projected count is compared with
        the bound and the terminal names the projection.'"""

        reading = self.reading_named("L")
        with mock.patch.object(ST, "MAX_CANDIDATES_PER_ENUMERATION", 1):
            tree = ST.build_stream_tree(
                reading,
                commitment_named("parity"),
                "mu1",
                ST.BOUNDS_THREE,
                ST.RULE_NO_REGRESS,
                census=False,
            )
        rows = [
            r for r in tree.truncations if _txt(r["terminal"]) == ST.TERMINAL_CANDIDATE_BUDGET
        ]
        self.assertTrue(rows, "the candidate budget did not fire")
        row = dict(rows[0])
        self.assert_row_names_tree_node_and_pair(
            row, ST.TERMINAL_CANDIDATE_BUDGET, "L/parity/mu1"
        )
        self.assertEqual(_num(row["bound"]), 1)
        self.assertGreater(_num(row["candidate_multisets_projected"]), 1)
        self.assertEqual(_num(row["item_count"]), 3)

    def test_a_budget_that_fires_raises_the_named_terminal(self) -> None:
        """Pins: 'every budget is raised as one exception carrying its own
        terminal name, so a truncation cannot be recorded under the wrong
        terminal.'"""

        exc = ST.BudgetExceeded(ST.TERMINAL_RESPONSE_BUDGET, {"bound": 1})
        self.assertEqual(exc.terminal, ST.TERMINAL_RESPONSE_BUDGET)
        self.assertEqual(str(exc), ST.TERMINAL_RESPONSE_BUDGET)
        self.assertEqual(dict(exc.detail), {"bound": 1})
        self.assertEqual(
            list(ST.BUDGET_TERMINALS),
            [
                ST.TERMINAL_ENUMERATION_BUDGET,
                ST.TERMINAL_CANDIDATE_BUDGET,
                ST.TERMINAL_RESPONSE_BUDGET,
                ST.TERMINAL_CLASS_BUDGET,
            ],
        )
        self.assertNotIn(ST.TERMINAL_ISO_BUDGET, ST.BUDGET_TERMINALS)

    def test_no_declared_budget_fired_in_the_committed_run(self) -> None:
        """Pins: 'R1-10 is HIT: no declared budget terminal appears in the
        receipt, no truncation row was written, the bijection budget raised
        nothing, and the declared wall bound did not fire.'"""

        receipt = load_receipt()
        agg = _obj(receipt["aggregate"])
        self.assertEqual(_arr(agg["budget_terminals_fired"]), [])
        self.assertEqual(_num(agg["budget_terminal_truncation_rows"]), 0)
        self.assertEqual(_arr(agg["situation_budget_terminals_fired"]), [])
        self.assertEqual(_num(_at(receipt, "availability", "iso_budget_rows")), 0)
        self.assertFalse(_flag(_at(receipt, "wall_clock_truncation", "truncated")))
        for row in _arr(receipt["runs"]):
            entry = _obj(row)
            self.assertEqual(_arr(entry["budget_terminals_fired"]), [])
            self.assertEqual(_arr(entry["truncations"]), [])

    def test_the_declared_bounds_are_the_sibling_s_with_one_dial_moved(self) -> None:
        """Pins: 'this rung moves the item bound from two to three and holds
        every other bound at the value the sibling declared: fifteen accepted
        rounds, a pre-expansion node guard of two hundred and fifty, a growth
        data bound of five, and form arity at most two.'"""

        bounds = _obj(load_receipt()["declared_bounds"])
        self.assertEqual(_num(bounds["max_items"]), 3)
        self.assertEqual(_num(bounds["sibling_item_bound"]), 2)
        self.assertEqual(_num(bounds["max_arity"]), 2)
        self.assertEqual(_num(bounds["max_rounds"]), 15)
        self.assertEqual(_num(bounds["pre_expansion_node_guard"]), 250)
        self.assertEqual(_num(bounds["growth_data_bound"]), 5)
        budgets = _obj(load_receipt()["declared_budgets"])
        self.assertEqual(_num(budgets["max_enumerations_per_run"]), 40)
        self.assertEqual(_num(budgets["max_candidates_per_enumeration"]), 1_000_000)
        self.assertEqual(_num(budgets["max_valid_per_target"]), 2000)
        self.assertEqual(_num(budgets["max_classes_per_node"]), 200)


# ---------------------------------------------------------------------------
# The fresh-with-fresh conjunct, the gatherer's budgets, and the two censuses
# ---------------------------------------------------------------------------


class FreshWithFreshTests(unittest.TestCase):
    """Pins: 'the conjunct the declared member adds over pairs between two
    data the SAME response introduces is load-bearing and not decoration: a
    delta exists that the inherited member accepts and the declared member
    refuses solely because of it, with every pair involving a previously held
    datum honoured.'

    The shipped exhibit for strictness carries one fresh datum, so its
    separating pair is fresh-versus-held and the fresh-with-fresh clause --
    which the member's own docstring calls the point of the member -- was
    exercised by nothing.  This is that case, isolated.
    """

    def state_and_delta(self) -> tuple[TState, tuple[str, Pair], Delta]:
        reading = [r for r in sealed_readings() if r.name == "L"][0]
        history = genesis_history(reading, commitment_named("total_apart"))
        base = ts_replay(history)
        build = canonical_delta((NewDatum(), NewForm(2), NewInst(0, (0, 0))))
        state = ts_replay(history + tuple(delta_events(base.regime, build)))
        delta = canonical_delta((NewDatum(), NewDatum(), NewInst(0, (1, 2))))
        return state, ("apart", (1, 2)), delta

    def test_the_state_is_the_one_the_exhibit_names(self) -> None:
        state, target, delta = self.state_and_delta()
        self.assertEqual(state.regime.n_data(), 3)
        self.assertEqual(state.regime.forms, (2,))
        self.assertEqual(sorted(state.regime.insts), [(0, (0, 0))])
        self.assertEqual(state.commitment, "total_apart")
        self.assertEqual(target, ("apart", (1, 2)))
        self.assertIn(
            delta, set(ST.iter_k_item_deltas(state.regime, 3, ST.BOUNDS_THREE))
        )
        self.assertEqual(sum(1 for it in delta if isinstance(it, NewDatum)), 2)

    def test_only_the_fresh_with_fresh_pair_separates_the_two_members(self) -> None:
        """The separator, and the proof that it is the fresh-with-fresh
        conjunct doing the work: every committed pair between a previously
        held datum and a datum the response introduces is honoured after the
        response, and the one unhonoured pair joins two data the response
        introduced."""

        state, target, delta = self.state_and_delta()
        self.assertTrue(ST.response_valid(state, target, delta))
        self.assertFalse(ST.strict_response_valid(state, target, delta))

        after = apply_delta(state.regime, delta)
        commitment = commitment_named(state.commitment)
        n0 = state.regime.n_data()
        held_side: list[tuple[int, int]] = []
        fresh_side: list[tuple[int, int]] = []
        for k in range(n0, after.n_data()):
            for i in range(k):
                pair = (i, k)
                ok = honoured(after, commitment.label(i, k), pair)
                (fresh_side if i >= n0 else held_side).append((pair[0], pair[1]))
                if i < n0:
                    self.assertTrue(
                        ok, f"a fresh-versus-held pair {pair} is unhonoured"
                    )
        self.assertTrue(held_side, "no fresh-versus-held pair exists at this exhibit")
        self.assertEqual(fresh_side, [(3, 4)])
        self.assertFalse(
            honoured(after, commitment.label(3, 4), (3, 4)),
            "the fresh-with-fresh pair is honoured, so it separates nothing",
        )

    def test_the_demanded_pair_itself_is_honoured_by_the_refused_delta(self) -> None:
        """The refusal is not the demand going unanswered: the demanded pair
        is honoured and the delta is still refused."""

        state, target, delta = self.state_and_delta()
        after = apply_delta(state.regime, delta)
        self.assertTrue(honoured(after, target[0], target[1]))


class GathererBudgetTests(unittest.TestCase):
    """Pins: 'the two budgets that govern one enumeration at one demanded pair
    -- the candidate budget and the response budget -- are enforced in the
    situation gatherer as well as in the tree loop, with the same terminals,
    and a gather that fires either attaches nothing.'

    The gatherer performed every three-item enumeration behind R1-5, R1-6 and
    R1-7 with no budget check at all, while R1-10 was scored on an empty
    terminal list.  Its zero was structural, not counted.
    """

    def situation(self) -> tuple[ST.RefusalSituation, RS.Gatherer]:
        reading = [r for r in sealed_readings() if r.name == "L"][0]
        state = ts_replay(genesis_history(reading, commitment_named("total_apart")))
        sit = ST.RefusalSituation(
            "L", "total_apart", "mu1", 0, "apart", (0, 1), state
        )
        return sit, RS.Gatherer()

    def test_the_candidate_budget_fires_in_the_gatherer_and_it_attaches_nothing(
        self,
    ) -> None:
        sit, gatherer = self.situation()
        with mock.patch.object(ST, "MAX_CANDIDATES_PER_ENUMERATION", 1):
            offered, valid = gatherer.gather(sit.state, (sit.kind, sit.pair), ST.RULE_NO_REGRESS)
        self.assertEqual(offered, 0)
        self.assertEqual(valid, [])
        self.assertEqual(len(gatherer.budget_terminals), 1)
        row = gatherer.budget_terminals[0]
        self.assertEqual(row["terminal"], ST.TERMINAL_CANDIDATE_BUDGET)
        self.assertEqual(row["where"], "situation gatherer")
        self.assertEqual(row["kind"], "apart")
        self.assertEqual(row["target"], [0, 1])
        self.assertEqual(row["bound"], 1)
        self.assertGreater(_num(row["candidate_multisets_projected"]), 1)

    def test_the_response_budget_fires_in_the_gatherer_and_it_attaches_nothing(
        self,
    ) -> None:
        sit, gatherer = self.situation()
        with mock.patch.object(ST, "MAX_VALID_PER_TARGET", 0):
            offered, valid = gatherer.gather(sit.state, (sit.kind, sit.pair), ST.RULE_NO_REGRESS)
        self.assertGreater(offered, 0)
        self.assertEqual(valid, [])
        self.assertEqual(len(gatherer.budget_terminals), 1)
        row = gatherer.budget_terminals[0]
        self.assertEqual(row["terminal"], ST.TERMINAL_RESPONSE_BUDGET)
        self.assertEqual(row["bound"], 0)
        self.assertGreater(_num(row["valid_gathered"]), 0)

    def test_the_gatherer_response_budget_stops_at_bound_plus_one(self) -> None:
        sit, gatherer = self.situation()
        consumed = 0

        def offered(*_args: object):  # type: ignore[no-untyped-def]
            nonlocal consumed
            for _ in range(20):
                consumed += 1
                yield (), sit.state.regime

        judge = mock.Mock()
        judge.accepts.return_value = True
        with (
            mock.patch.object(ST, "candidate_count", return_value=20),
            mock.patch.object(ST, "iter_k_item_deltas_applied", offered),
            mock.patch.object(ST, "has_noop_item", return_value=False),
            mock.patch.object(ST, "Judge", return_value=judge),
            mock.patch.object(ST, "MAX_VALID_PER_TARGET", 2),
        ):
            offered_count, valid = gatherer.gather(
                sit.state, (sit.kind, sit.pair), ST.RULE_NO_REGRESS
            )
        self.assertEqual(consumed, 3)
        self.assertEqual(offered_count, 3)
        self.assertEqual(valid, [])
        self.assertEqual(gatherer.budget_terminals[0]["valid_gathered"], 3)

    def test_a_repeat_is_answered_from_the_record_and_is_counted(self) -> None:
        sit, gatherer = self.situation()
        first = gatherer.gather(sit.state, (sit.kind, sit.pair), ST.RULE_NO_REGRESS)
        second = gatherer.gather(sit.state, (sit.kind, sit.pair), ST.RULE_NO_REGRESS)
        self.assertEqual(first, second)
        self.assertEqual(gatherer.enumerations, 1)
        self.assertEqual(gatherer.repeats, 1)
        self.assertGreater(gatherer.max_projected_candidates, 0)
        self.assertEqual(gatherer.budget_terminals, [])

    def test_the_receipt_records_the_margin_rather_than_only_the_pass(self) -> None:
        """Pins: 'no declared budget fired, and the receipt records how close
        the largest enumeration came to the candidate bound rather than
        recording only that it did not pass it.'"""

        receipt = load_receipt()
        agg = _obj(receipt["aggregate"])
        budgets = _obj(receipt["declared_budgets"])
        observed = _obj(budgets["observed_maxima"])
        bound = _num(budgets["max_candidates_per_enumeration"])
        largest = _num(agg["max_projected_candidates_in_one_enumeration"])
        self.assertEqual(
            _num(observed["tree_loop_max_projected_candidates_in_one_enumeration"]),
            largest,
        )
        self.assertGreater(largest, 0)
        self.assertLessEqual(largest, bound)
        where = _obj(agg["max_projected_candidates_at"])
        self.assertIn("run", where)
        self.assertIn("node", where)
        self.assertEqual(_arr(agg["situation_budget_terminals_fired"]), [])
        self.assertLessEqual(
            _num(observed["situation_gatherer_max_valid_at_one_pair"]),
            _num(budgets["max_valid_per_target"]),
        )


class AvailabilityCensusTests(unittest.TestCase):
    """Pins: 'the availability census counts four populations separately --
    offered, examined, judged and skipped as a declared no-op -- so a zero is
    a counted zero, and the receipt lifts the census headline quantities into
    the availability block rather than only the priced-out lens.'

    ``examined`` used to be ASSIGNED from ``offered``, with a docstring
    justifying it by a claim that was false, which made one clause of R1-9's
    frozen falsifier unable to fail.
    """

    def state(self) -> TState:
        reading = [r for r in sealed_readings() if r.name == "L"][0]
        history = genesis_history(reading, commitment_named("parity"))
        base = ts_replay(history)
        build = canonical_delta((NewForm(1), NewRuleAll(0)))
        return ts_replay(history + tuple(delta_events(base.regime, build)))

    def test_the_four_counts_are_maintained_separately(self) -> None:
        state = self.state()
        counters = ST.Counters()
        avail = ST.fresh_datum_availability(
            state, ("apart", (0, 1)), 2, ST.RULE_NO_REGRESS, counters
        )
        self.assertEqual(avail.examined, avail.offered)
        self.assertEqual(avail.judged, avail.offered - avail.skipped_as_noop)
        self.assertGreater(
            avail.skipped_as_noop,
            0,
            "this base carries a ruled form, so some candidate must be a no-op",
        )
        self.assertLess(avail.judged, avail.offered)
        self.assertEqual(counters.fresh_datum_candidates_offered, avail.offered)
        self.assertEqual(counters.fresh_datum_candidates_examined, avail.examined)
        self.assertEqual(counters.fresh_datum_candidates_judged, avail.judged)
        self.assertEqual(
            counters.fresh_datum_candidates_skipped_as_noop, avail.skipped_as_noop
        )
        row = avail.as_json()
        for key in ("offered", "examined", "judged", "skipped_as_noop", "valid"):
            self.assertIn(key, row)

    def test_the_census_reports_a_bound_it_found_nothing_in(self) -> None:
        """``least_cost`` is minus one and ``exists`` is false when no
        datum-bearing response is valid, and the counts still say the census
        looked."""

        reading = [r for r in sealed_readings() if r.name == "L"][0]
        state = ts_replay(genesis_history(reading, commitment_named("total_same")))
        avail = ST.fresh_datum_availability(state, ("same", (0, 1)), 1)
        self.assertEqual(avail.item_bound, 1)
        self.assertGreater(avail.offered, 0)
        self.assertEqual(avail.exists(), avail.least_cost >= 0)

    def test_the_receipt_lifts_both_censuses_and_not_only_the_priced_lens(
        self,
    ) -> None:
        avail = _obj(load_receipt()["availability"])
        for key in (
            "census_two_rows_by_kind",
            "census_two_rows_with_fresh_datum_available",
            "census_two_rows_with_fresh_datum_available_by_kind",
            "census_two_rows_available_where_no_minimum_was_retained",
            "census_three_rows_with_fresh_datum_available",
            "census_three_valid_fresh_datum_responses",
            "fresh_datum_candidates_judged",
            "fresh_datum_candidates_skipped_as_noop",
        ):
            self.assertIn(key, avail, f"{key} is measured but not aggregated")
        available = _num(avail["census_two_rows_with_fresh_datum_available"])
        self.assertEqual(
            available,
            _num(avail["priced_out_rows"])
            + _num(avail["census_two_rows_available_where_no_minimum_was_retained"]),
        )
        by_kind = _obj(avail["census_two_rows_with_fresh_datum_available_by_kind"])
        self.assertEqual(sum(_num(v) for v in by_kind.values()), available)
        self.assertGreater(
            _num(by_kind[SAME]),
            0,
            "no same-kind row carries an available fresh-datum response, so the "
            "mechanism note beside R1-5 has no subject",
        )
        self.assertGreaterEqual(
            _num(avail["fresh_datum_candidates_offered"]),
            _num(avail["fresh_datum_candidates_judged"]),
        )

    def test_r1_9_records_its_clauses_and_names_the_one_that_failed(self) -> None:
        """Pins: 'R1-9 is MISSED, and the receipt names which of its five
        clauses failed rather than reporting one flag.'"""

        detail = _obj(_at(load_receipt(), "prediction_detail", "R1-9"))
        clauses = _obj(detail["clauses"])
        self.assertEqual(len(clauses), 5)
        failing = [_txt(v) for v in _arr(detail["failing_clauses"])]
        self.assertEqual(failing, ["b_no_priced_out_row_of_the_same_kind"])
        self.assertTrue(_flag(clauses["e_examined_is_not_below_offered"]))


class MemberComparisonTests(unittest.TestCase):
    """Pins: 'the declared validity member was run at every situation of both
    situation tables and returned the same valid set at every one of them,
    while remaining strictly stronger as a predicate.'  A member that
    separated nothing where it was run is a finding, and the receipt records
    it rather than reporting the inherited member alone."""

    def test_the_receipt_records_the_declared_member_beside_the_inherited_one(
        self,
    ) -> None:
        receipt = load_receipt()
        compared = 0
        for table in ("rectangle_a", "enumeration_situations"):
            block = _obj(_at(receipt, table, "by_declared_member"))
            with self.subTest(table=table):
                self.assertGreater(_num(block["rows_compared"]), 0)
                self.assertEqual(_num(block["rows_on_which_the_two_members_differ"]), 0)
                self.assertEqual(_arr(block["differing_rows"]), [])
                for field in RS.COMPARED_FIELDS:
                    self.assertEqual(
                        _num(block[f"inherited_{field}"]),
                        _num(block[f"declared_{field}"]),
                    )
                self.assertIn("strictly stronger", _txt(block["finding"]))
            compared += _num(block["rows_compared"])
        # Both tables together: every situation at which the declared member
        # was run, and it separated nothing at any of them.
        self.assertEqual(compared, 33)

    def test_every_row_of_both_tables_names_the_member_that_produced_it(self) -> None:
        receipt = load_receipt()
        for table in ("rectangle_a", "enumeration_situations"):
            for raw in _arr(_at(receipt, table, "rows")):
                row = _obj(raw)
                self.assertIn("candidate_multisets_projected", row)
                for member, name in (
                    (RS.INHERITED, ST.RULE_NO_REGRESS),
                    (RS.DECLARED, ST.RULE_STRICT_NO_REGRESS),
                ):
                    sub = _obj(row[member])
                    self.assertEqual(_txt(sub["validity_rule"]), name)
                    self.assertIn("deltas_offered_at_three_items", sub)

    def test_the_three_candidate_words_name_three_populations(self) -> None:
        """Pins: 'the receipt reports three different populations under three
        different names -- the multisets the tree loop projected, the
        admissible deltas it walked, and the admissible deltas the situation
        gatherer walked -- where it once reported two of them under one
        word.'"""

        receipt = load_receipt()
        agg = _obj(receipt["aggregate"])
        counters = _obj(agg["counters"])
        avail = _obj(receipt["availability"])
        projected = _num(counters["candidate_multisets_projected"])
        offered = _num(counters["deltas_offered"])
        situation = _num(agg["situation_deltas_offered"])
        self.assertNotIn("candidates_examined", counters)
        self.assertNotIn("candidates_examined", agg)
        self.assertNotIn("candidates_examined", avail)
        # The three are pairwise different, and the projection dwarfs both
        # walks: it counts multisets over the declared universe, admissible
        # or not, while the other two count admissible deltas actually
        # walked -- the tree loop's, at every item count, and the situation
        # gatherer's, at three items only.
        self.assertGreater(projected, offered)
        self.assertGreater(projected, situation)
        self.assertNotEqual(offered, situation)
        self.assertEqual(_num(avail["candidate_multisets_projected"]), projected)

# ---------------------------------------------------------------------------
# The failure paths
# ---------------------------------------------------------------------------


class TypedReaderTests(unittest.TestCase):
    """Pins: 'every value the runner reads out of an untyped JSON tree is
    read through a reader that fails by name rather than coercing, and a flag
    is never read as a count.'

    These readers guard every number the scorer touches.  They were exercised
    only on values that pass, so the branch that refuses was reached by
    nothing and a silent coercion would have looked identical.
    """

    def test_a_flag_is_refused_where_a_count_is_wanted(self) -> None:
        with self.assertRaises(TypeError) as caught:
            RS._int(True)
        self.assertIn("a flag is not a count", str(caught.exception))
        self.assertEqual(RS._int(3), 3)

    def test_each_reader_refuses_the_shape_it_does_not_read(self) -> None:
        cases: Sequence[tuple[str, object]] = (
            ("_int", "3"),
            ("_str", 3),
            ("_bool", 1),
            ("_strs", "abc"),
            ("_rows", "abc"),
            ("_sub", []),
            ("_pair_of", [1, 2, 3]),
            ("_pair_of", "xy"),
        )
        for name, value in cases:
            with self.subTest(reader=name, value=value):
                with self.assertRaises(TypeError):
                    getattr(RS, name)(value)

    def test_a_row_that_is_not_an_object_is_refused(self) -> None:
        with self.assertRaises(TypeError) as caught:
            RS._rows([{"a": 1}, 7])
        self.assertIn("not an object", str(caught.exception))
        self.assertEqual(RS._rows([{"a": 1}]), [{"a": 1}])

    def test_a_value_that_is_not_json_is_refused(self) -> None:
        with self.assertRaises(TypeError) as caught:
            RS._j({"k": object()})
        self.assertIn("not JSON", str(caught.exception))
        self.assertEqual(RS._j((1, "a", None, True)), [1, "a", None, True])

    def test_the_readers_accept_what_they_read(self) -> None:
        self.assertEqual(RS._str("a"), "a")
        self.assertTrue(RS._bool(True))
        self.assertEqual(RS._strs(["a", "b"]), ["a", "b"])
        self.assertEqual(RS._sub({"a": 1})["a"], 1)
        self.assertEqual(RS._pair_of([1, 2]), (1, 2))


class DeadlineTests(unittest.TestCase):
    """Pins: 'the wall bound is a declared terminal that records where it
    fired and how far the run had got, and a run that does not reach it puts
    no clock reading in the receipt.'

    A10 says the receipt is not byte-reproducible when the bound fires, so
    the firing path is exercised here rather than by a slow run.
    """

    def test_a_bound_that_has_not_passed_records_nothing(self) -> None:
        deadline = RS.Deadline(10_000.0)
        self.assertFalse(deadline.check("nowhere", 0))
        row = deadline.as_json()
        self.assertEqual(
            sorted(row), ["declared_bound_seconds", "truncated"]
        )
        self.assertFalse(_flag(row["truncated"]))
        self.assertGreaterEqual(deadline.elapsed(), 0.0)

    def test_the_first_firing_is_the_one_recorded(self) -> None:
        deadline = RS.Deadline(-1.0)
        self.assertTrue(deadline.check("two_item_reconstruction", 7))
        self.assertTrue(deadline.check("somewhere_later", 99))
        row = deadline.as_json()
        self.assertTrue(_flag(row["truncated"]))
        self.assertEqual(_txt(row["truncation_kind"]), "terminal_wall_bound")
        self.assertEqual(_txt(row["where"]), "two_item_reconstruction")
        self.assertEqual(_num(row["units_reached_before_truncation"]), 7)

    def test_every_loop_the_bound_governs_stops_at_it(self) -> None:
        """Each loop that asks the deadline stops on the first question, and
        the table it would have built comes back empty rather than partial."""

        recon = RS.two_item_reconstruction(RS.Deadline(-1.0))
        self.assertEqual(_num(recon["trees_built"]), 0)
        trees, rows = RS.three_item_runs(RS.Deadline(-1.0))
        self.assertEqual((trees, rows), ([], []))
        rect = RS.rectangle_a(RS.Gatherer(), RS.Deadline(-1.0))
        self.assertEqual(_num(rect["situations_examined"]), 0)
        self.assertGreater(_num(rect["refusal_records"]), 0)
        enum = RS.enumeration_situations([], RS.Gatherer(), RS.Deadline(-1.0))
        self.assertEqual(_num(enum["situations_examined"]), 0)


class UnhandledAbortTests(unittest.TestCase):
    """Pins: 'the bijection budget the sibling raises outside every handler is
    caught around the situation tables: both tables come back in their empty
    shape and the abort is recorded on the aggregate rather than ending the
    run.'"""

    class Raiser(RS.Gatherer):
        def gather(
            self, s: TState, target: tuple[str, Pair], rule: str
        ) -> tuple[int, list[Delta]]:
            raise RuntimeError("permutation budget exhausted")

    def test_the_abort_is_caught_and_both_tables_come_back_empty(self) -> None:
        empty_rect: dict[str, Json] = {"situations_examined": 0}
        empty_enum: dict[str, Json] = {"situations_examined": 0}
        rect, enum, unhandled = RS.situation_tables(
            [], self.Raiser(), RS.Deadline(10_000.0), empty_rect, empty_enum
        )
        self.assertEqual(rect, empty_rect)
        self.assertEqual(enum, empty_enum)
        self.assertIn("permutation budget exhausted", unhandled)
        self.assertTrue(unhandled.startswith("RuntimeError: "))

    def test_a_run_that_does_not_abort_reports_no_abort(self) -> None:
        rect, enum, unhandled = RS.situation_tables(
            [], RS.Gatherer(), RS.Deadline(-1.0), {}, {}
        )
        self.assertEqual(unhandled, "")
        self.assertIn("situations_examined", rect)
        self.assertIn("situations_examined", enum)

    def test_the_written_hash_is_compared_and_can_disagree(self) -> None:
        self.assertTrue(RS._written_hash_agrees("a" * 64, "a" * 64))
        self.assertFalse(RS._written_hash_agrees("a" * 64, "b" * 64))

    def test_a_member_comparison_names_the_rows_that_differ(self) -> None:
        """The comparison block reports zero differing rows on this run; the
        branch that reports one is exercised on a fabricated pair so that the
        zero is a measured zero."""

        def row(inherited: int, declared: int) -> Json:
            def side(n: int) -> Json:
                return {
                    "validity_rule": "x",
                    "valid_three_item_responses": n,
                    "valid_with_datum_item": 0,
                    "valid_without_two_instances_and_without_a_rule": 0,
                    "answered_at_exactly_three_items": n > 0,
                }

            return {
                "situation": "zz",
                "kind": "apart",
                "target": [0, 1],
                RS.INHERITED: side(inherited),
                RS.DECLARED: side(declared),
            }

        same = RS._member_comparison([row(3, 3)])
        self.assertEqual(_num(same["rows_on_which_the_two_members_differ"]), 0)
        differing = RS._member_comparison([row(3, 3), row(3, 1)])
        self.assertEqual(_num(differing["rows_on_which_the_two_members_differ"]), 1)
        self.assertEqual(len(_arr(differing["differing_rows"])), 1)
        self.assertEqual(_num(differing["inherited_valid_three_item_responses"]), 6)
        self.assertEqual(_num(differing["declared_valid_three_item_responses"]), 4)
        self.assertEqual(_num(differing["inherited_answered_at_exactly_three_items"]), 2)


class GeneratorEdgeTests(unittest.TestCase):
    """Pins: 'each edge of the declared generator and of the wider
    construction it is certified against behaves as its docstring says at the
    boundary: the empty item count, a non-positive universe, a duplicate
    multiset, and a candidate the sealed admission conditions reject.'"""

    def base(self) -> Regime:
        return dict(family())["b2_unary_form"]

    def test_a_universe_is_offered_only_for_a_positive_item_count(self) -> None:
        with self.assertRaises(ValueError) as caught:
            ST.universe_items(self.base(), 0, ST.BOUNDS_THREE)
        self.assertIn("positive item count", str(caught.exception))

    def test_the_projection_at_a_non_positive_item_count_is_one(self) -> None:
        self.assertEqual(ST.candidate_count(self.base(), 0, ST.BOUNDS_THREE), 1)
        self.assertEqual(ST.candidate_count(self.base(), -1, ST.BOUNDS_THREE), 1)

    def test_a_form_of_arity_below_one_is_not_an_admissible_shape(self) -> None:
        self.assertFalse(
            ST.admissible_shape(self.base(), canonical_delta((NewForm(0),)))
        )

    def test_the_wider_construction_yields_the_empty_delta_at_zero_items(self) -> None:
        self.assertEqual(
            list(ST.iter_superset_deltas(self.base(), 0, ST.BOUNDS_THREE)), [()]
        )
        self.assertEqual(list(ST.iter_k_item_deltas(self.base(), 0, ST.BOUNDS_THREE)), [()])

    def test_the_declared_universe_repeats_no_item(self) -> None:
        """Pins: 'the declared universe returns no item twice, so distinct
        multisets over it canonicalize to distinct deltas.'

        This is what makes the applied walk's duplicate guard unreachable,
        and that guard is excluded from coverage on the strength of this
        test.  The WIDER construction builds its multisets differently and
        does produce duplicates, which is why it keeps a live guard.
        """

        for name, base in family():
            for cost in (1, 2, 3):
                with self.subTest(base=name, item_count=cost):
                    universe = ST.universe_items(base, cost, ST.BOUNDS_THREE)
                    self.assertEqual(len(universe), len(set(universe)))
                    canonical = {
                        canonical_delta(combo)
                        for combo in combinations_with_replacement(universe, cost)
                    }
                    self.assertEqual(
                        len(canonical), ST.candidate_count(base, cost, ST.BOUNDS_THREE)
                    )

    def test_the_applied_walk_drops_what_application_refuses(self) -> None:
        """The applied walk yields each delta once and drops what the sealed
        admission conditions refuse; the drop is counted, not assumed."""

        base = self.base()
        pairs = list(ST.iter_k_item_deltas_applied(base, 2, ST.BOUNDS_THREE))
        deltas = [d for d, _after in pairs]
        self.assertEqual(len(deltas), len(set(deltas)))
        universe = ST.universe_items(base, 2, ST.BOUNDS_THREE)
        walked = 0
        refused = 0
        for combo in combinations_with_replacement(universe, 2):
            walked += 1
            try:
                apply_delta(base, canonical_delta(combo))
            except AdmissionError:
                refused += 1
        self.assertGreater(refused, 0, "no candidate was refused by application")
        self.assertLess(len(deltas), walked)

    def test_the_datum_bearing_space_drops_what_application_refuses(self) -> None:
        base = dict(family())["b5_binary_form_with_instance"]
        generated, space = ST.fresh_datum_space(base, 2, ST.BOUNDS_THREE)
        self.assertGreater(generated, len(space))
        for delta, _after in space:
            self.assertTrue(has_fresh_datum(delta))

    def test_the_situation_record_renders_itself(self) -> None:
        reading = [r for r in sealed_readings() if r.name == "L"][0]
        state = ts_replay(genesis_history(reading, commitment_named("parity")))
        sit = ST.RefusalSituation("L", "parity", "mu1", 4, "apart", (0, 1), state)
        row = sit.as_json()
        self.assertEqual(row["tree"], "L/parity/mu1")
        self.assertEqual(row["node"], 4)
        self.assertEqual(row["target"], [0, 1])
        self.assertEqual(row["data"], state.regime.n_data())


class SelectionEdgeTests(unittest.TestCase):
    """Pins: 'the selection refuses an unnamed measure, answers a repeat from
    the memo it declares, and the declared validity member accepts a response
    that introduces no datum.'"""

    def state(self) -> TState:
        reading = [r for r in sealed_readings() if r.name == "L"][0]
        return ts_replay(genesis_history(reading, commitment_named("parity")))

    def three_item_situation(self) -> ST.RefusalSituation:
        """A recorded refusal, which is by construction a state where every
        response of fewer than three items fails -- the only kind of call the
        memo records."""

        return ST.refusal_states(ST.BOUNDS_TWO, ST.RULE_NO_REGRESS, census=False)[0]

    def test_an_unnamed_measure_is_refused(self) -> None:
        with self.assertRaises(ValueError) as caught:
            ST.min_responses_three(self.state(), ("apart", (0, 1)), "mu3", ST.BOUNDS_THREE)
        self.assertIn("unknown measure", str(caught.exception))

    def test_the_memo_records_only_a_call_that_reached_three_items(self) -> None:
        """A call answered below three items is cheap and is not recorded, so
        the memo stays empty and the next call is a fresh enumeration."""

        memo = ST.EnumerationMemo()
        counters = ST.Counters()
        for _ in range(2):
            ST.min_responses_three(
                self.state(),
                ("apart", (0, 1)),
                "mu1",
                ST.BOUNDS_THREE,
                ST.RULE_NO_REGRESS,
                counters,
                memo,
            )
        self.assertEqual(len(memo), 0)
        self.assertEqual(memo.hits, 0)
        self.assertEqual(counters.enumeration_memo_hits, 0)

    def test_the_memo_answers_a_repeat_and_counts_it(self) -> None:
        situation = self.three_item_situation()
        state = situation.state
        target: tuple[str, Pair] = (situation.kind, situation.pair)
        memo = ST.EnumerationMemo()
        counters = ST.Counters()
        first = ST.min_responses_three(
            state, target, "mu1", ST.BOUNDS_THREE, ST.RULE_NO_REGRESS, counters, memo
        )
        stored = len(memo)
        second = ST.min_responses_three(
            state, target, "mu1", ST.BOUNDS_THREE, ST.RULE_NO_REGRESS, counters, memo
        )
        self.assertEqual(first, second)
        self.assertEqual(memo.hits, 1)
        self.assertEqual(counters.enumeration_memo_hits, 1)
        self.assertEqual(len(memo), stored)
        self.assertGreaterEqual(stored, 1)

    def test_the_declared_member_accepts_a_response_introducing_no_datum(self) -> None:
        """The added conjunct quantifies over the data the response
        introduces, so a response introducing none satisfies it vacuously and
        the member returns what the inherited one returned."""

        state = self.state()
        target: tuple[str, Pair] = ("apart", (0, 1))
        accepted = [
            delta
            for delta in ST.iter_k_item_deltas(state.regime, 2, ST.BOUNDS_THREE)
            if not has_fresh_datum(delta) and ST.response_valid(state, target, delta)
        ]
        self.assertTrue(
            accepted,
            "no response carrying no datum item is valid at this state, so the "
            "vacuous case of the added conjunct has no witness here",
        )
        for delta in accepted:
            self.assertTrue(ST.strict_response_valid(state, target, delta))

    def test_the_judge_carries_the_declared_member_s_added_conjunct(self) -> None:
        """The judge is the per-candidate restructuring of the two members;
        its strict branch must refuse the fresh-with-fresh exhibit."""

        state, target, delta = FreshWithFreshTests().state_and_delta()
        after = apply_delta(state.regime, delta)
        loose = ST.Judge(state, target, ST.RULE_NO_REGRESS)
        strict = ST.Judge(state, target, ST.RULE_STRICT_NO_REGRESS)
        self.assertTrue(loose.accepts(delta, after))
        self.assertFalse(strict.accepts(delta, after))


class TreeLoopFailurePathTests(unittest.TestCase):
    """Pins: 'every call site of the sibling key is inside a handler, so the
    bijection budget the sibling raises outside every handler is recorded here
    as ``terminal_iso_budget`` on the node that raised it, at the root, at the
    targets, at the selection, at the quotient and at the attachment.'

    The sibling's own terminal for this is unreachable, so these paths are new
    code and are exercised by making the key raise rather than by waiting for
    a rectangle large enough to exhaust the real budget.
    """

    def reading(self) -> Reading:
        return [r for r in sealed_readings() if r.name == "L"][0]

    def build(self, max_rounds: int = ST.MAX_ROUNDS) -> ST.STree:
        return ST.build_stream_tree(
            self.reading(),
            commitment_named("parity"),
            "mu1",
            ST.BOUNDS_TWO,
            ST.RULE_NO_REGRESS,
            max_rounds=max_rounds,
            census=False,
        )

    @contextlib.contextmanager
    def key_raises_after(self, calls: int):  # type: ignore[no-untyped-def]
        """The sibling key, raising the bare ``RuntimeError`` its budget
        raises, after a declared number of successful calls."""

        real = getattr(ST, "key_of")
        state = {"n": 0}

        def fake(s: TState) -> object:
            state["n"] += 1
            if state["n"] > calls:
                raise RuntimeError("permutation budget exhausted")
            return real(s)

        with mock.patch("stream.key_of", fake):
            yield

    def terminals(self, tree: ST.STree) -> list[str]:
        return [_txt(dict(r)["where"]) for r in tree.truncations]

    def test_the_root_key_raising_stops_the_tree_before_a_node_exists(self) -> None:
        with self.key_raises_after(0):
            tree = self.build()
        self.assertEqual(self.terminals(tree), ["root"])
        self.assertEqual(len(tree.tree.nodes), 0)
        self.assertEqual(
            _txt(dict(tree.truncations[0])["terminal"]), ST.TERMINAL_ISO_BUDGET
        )

    def assert_injected_terminal(
        self, where: str, patcher: contextlib.AbstractContextManager[object]
    ) -> ST.STree:
        with patcher:
            tree = self.build()
        rows = [dict(row) for row in tree.truncations]
        self.assertEqual([_txt(row["where"]) for row in rows], [where])
        self.assertEqual(_txt(rows[0]["terminal"]), ST.TERMINAL_ISO_BUDGET)
        terminal = tree.tree.nodes[_num(rows[0]["node"])]
        self.assertEqual(terminal.status, ST.TERMINAL_ISO_BUDGET)
        self.assertFalse(
            [edge for edge in tree.tree.edges if edge.parent == terminal.node_id]
        )
        return tree

    def test_each_pre_attachment_key_site_refuses_by_its_exact_name(self) -> None:
        """Targets, selection and quotient are independent refusal sites."""

        error = RuntimeError("permutation budget exhausted")
        cases = (
            ("targets", mock.patch.object(ST, "closure_targets", side_effect=error)),
            (
                "selection",
                mock.patch.object(ST, "min_responses_three", side_effect=error),
            ),
            ("quotient", mock.patch.object(ST, "_quotient", side_effect=error)),
        )
        for where, patcher in cases:
            with self.subTest(where=where):
                self.assert_injected_terminal(where, patcher)

    def test_attachment_preflight_is_atomic_when_a_later_key_fails(self) -> None:
        """A later attachment-key failure cannot leave earlier sibling edges."""

        real = ST._prepare_attachment
        calls = 0

        def fail_second(history: tuple[TSEvent, ...]) -> tuple[TState, TStateKey]:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("permutation budget exhausted")
            return real(history)

        tree = self.assert_injected_terminal(
            "attach", mock.patch.object(ST, "_prepare_attachment", fail_second)
        )
        self.assertEqual(calls, 2)
        row = dict(tree.truncations[0])
        self.assertEqual(_num(row["attached"]), 0)

    def test_the_round_bound_completes_a_node_rather_than_expanding_it(self) -> None:
        tree = self.build(max_rounds=0)
        statuses = {node.status for node in tree.tree.nodes}
        self.assertEqual(statuses, {"completed"})
        self.assertEqual(tree.tree.edges, [])

    def test_a_run_past_the_growth_data_bound_is_recorded_with_its_count(self) -> None:
        counters = ST.Counters()
        tree = ST.build_stream_tree(
            self.reading(),
            commitment_named("parity"),
            "mu1",
            ST.BOUNDS_TWO,
            ST.RULE_NO_REGRESS,
            max_data=1,
            census=False,
            counters=counters,
        )
        self.assertGreater(counters.nodes_above_growth_data_bound, 0)
        self.assertTrue(tree.over_growth_bound)
        row = dict(tree.over_growth_bound[0])
        self.assertEqual(_num(row["bound"]), 1)
        self.assertGreater(_num(row["data"]), 1)

# ---------------------------------------------------------------------------
# The pin verifier
# ---------------------------------------------------------------------------


class ClaimLedgerClassTests(unittest.TestCase):
    """The ledger uses exactly one canonical class in the seed's declared scope."""

    def test_all_twenty_seven_rows_have_one_canonical_class(self) -> None:
        canonical = {
            "SUPPLIED DATUM",
            "DERIVED DEFINITION",
            "DETERMINISTIC COMPUTATION",
            "REFUTED CLAIM",
            "OPEN OBSTRUCTION",
            "METATHEORY APPARATUS",
        }
        rows = [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in (HERE / "CLAIM_LEDGER.md").read_text(encoding="utf-8").splitlines()
            if line.startswith("| ST-")
        ]
        self.assertEqual([row[0] for row in rows], [f"ST-{n:02d}" for n in range(1, 28)])
        self.assertTrue(all(len(row) == 5 for row in rows))
        self.assertTrue(all(row[1] in canonical for row in rows))


class PinVerifierTests(unittest.TestCase):
    """Pins: 'the pin verifier passes on the committed manifest, and fails by
    name on every malformation of it that the manifest could carry.'

    The verifier had no test of its own: it was run, and its passing was the
    only evidence that it could do anything.  A gate is not proved by being
    green, so each refusal is exercised on a mutated manifest and each is
    required to name the thing it refused.
    """

    def manifest(self) -> dict[str, Json]:
        return cast(dict[str, Json], json.loads(VP.MANIFEST.read_text("utf-8")))

    @contextlib.contextmanager
    def written(self, payload: Mapping[str, Json]):  # type: ignore[no-untyped-def]
        """The verifier pointed at a manifest written to a temporary file, so
        the committed one is never rewritten by a test."""

        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "SOURCE_MANIFEST.json"
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            with mock.patch.object(VP, "MANIFEST", path):
                yield path

    def refusal(self, payload: Mapping[str, Json]) -> str:
        with self.written(payload):
            with self.assertRaises(ValueError) as caught:
                VP.verify()
        return str(caught.exception)

    def test_the_committed_manifest_verifies_and_names_what_it_checked(self) -> None:
        lines = VP.verify()
        joined = "\n".join(lines)
        self.assertIn("verification commit:", joined)
        self.assertIn("snapshot commit:", joined)
        self.assertIn("(ancestor of HEAD)", joined)
        self.assertIn("committed scope:", joined)
        self.assertIn("working-tree scope: clean outside research/second_stream/", joined)
        self.assertIn("second_stream pins verified:", joined)
        sources = _arr(self.manifest()["sources"])
        self.assertEqual(sum(1 for line in lines if line.startswith("source: ")), len(sources))
        self.assertIn("ci/prose_watchlist.json", joined)
        self.assertIn("contact/analysis/contact_countermodels.json", joined)

    def test_both_refusal_tables_stay_pinned_so_a_prune_still_fails(self) -> None:
        """Pins: 'a committed prune of either table the rung's scans read
        fails this verifier instead of silently narrowing a scan.'  The two
        tables are pinned DIFFERENTLY, and the difference is recorded rather
        than silent: contact_countermodels.json is a source, checked at the
        snapshot and at HEAD; ci/prose_watchlist.json is a frozen text,
        checked at HEAD only, because a later and unrelated rung legitimately
        grew that shared census past this rung's snapshot.  Both remain
        pinned, and dropping either from its own list is a population-differs
        refusal -- which is the anti-narrowing guard, unmoved by the split."""

        source_paths = {_txt(_obj(row)["path"]) for row in _arr(self.manifest()["sources"])}
        frozen_paths = {_txt(_obj(row)["path"]) for row in _arr(self.manifest()["frozen_texts"])}
        self.assertIn("contact/analysis/contact_countermodels.json", source_paths)
        self.assertIn("ci/prose_watchlist.json", frozen_paths)

        pruned_source = self.manifest()
        pruned_source["sources"] = [
            row
            for row in _arr(pruned_source["sources"])
            if _txt(_obj(row)["path"]) != "contact/analysis/contact_countermodels.json"
        ]
        self.assertIn("source population differs", self.refusal(pruned_source))

        pruned_frozen = self.manifest()
        pruned_frozen["frozen_texts"] = [
            row
            for row in _arr(pruned_frozen["frozen_texts"])
            if _txt(_obj(row)["path"]) != "ci/prose_watchlist.json"
        ]
        self.assertIn("frozen text population differs", self.refusal(pruned_frozen))

    def test_source_and_frozen_populations_cannot_shrink(self) -> None:
        payload = self.manifest()
        source_rows = _arr(payload["sources"])
        source_paths = {_txt(_obj(row)["path"]) for row in source_rows}
        self.assertEqual(source_paths, VP.REQUIRED_SOURCE_PATHS)
        payload["sources"] = source_rows[:-1]
        self.assertIn("source population differs", self.refusal(payload))

        payload = self.manifest()
        frozen_rows = _arr(payload["frozen_texts"])
        frozen_paths = {_txt(_obj(row)["path"]) for row in frozen_rows}
        self.assertEqual(frozen_paths, VP.REQUIRED_FROZEN_PATHS)
        payload["frozen_texts"] = frozen_rows[:-1]
        self.assertIn("frozen text population differs", self.refusal(payload))

    def test_duplicate_json_names_are_refused_before_verification(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = pathlib.Path(raw) / "SOURCE_MANIFEST.json"
            path.write_text('{"schema": "one", "schema": "two"}', encoding="utf-8")
            with mock.patch.object(VP, "MANIFEST", path):
                with self.assertRaises(ValueError) as caught:
                    VP._read_manifest()
        self.assertIn("duplicate JSON key", str(caught.exception))

    def test_a_moved_source_fails_at_the_snapshot_and_at_head(self) -> None:
        payload = self.manifest()
        rows = _arr(payload["sources"])
        first = _obj(rows[0])
        first["sha256"] = "0" * 64
        payload["sources"] = [cast(Json, first), *rows[1:]]
        message = self.refusal(payload)
        self.assertIn("snapshot hash mismatch", message)
        self.assertIn(_txt(first["path"]), message)

    def test_every_malformation_is_refused_by_name(self) -> None:
        table: Sequence[tuple[str, str, object]] = (
            ("schema", "unexpected manifest schema", "second_stream/v0"),
            ("snapshot_commit", "40-digit lowercase hex", "HEAD"),
            ("sources", "at least one source", []),
            ("sources", "each source entry must be an object", ["x"]),
            ("absent_at_snapshot", "possibly empty", "none"),
            ("absent_at_snapshot", "each absent entry must be an object", ["x"]),
            ("landed_replay", "no subject for", []),
            ("frozen_texts", "must list the frozen texts", []),
            ("frozen_texts", "each frozen text entry must be an object", ["x"]),
        )
        for key, fragment, value in table:
            with self.subTest(key=key, value=value):
                payload = self.manifest()
                payload[key] = cast(Json, value)
                self.assertIn(fragment, self.refusal(payload))

    def test_a_manifest_that_is_not_an_object_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "SOURCE_MANIFEST.json"
            path.write_text("[]", encoding="utf-8")
            with mock.patch.object(VP, "MANIFEST", path):
                with self.assertRaises(ValueError) as caught:
                    VP.verify()
        self.assertIn("must be an object", str(caught.exception))

    def test_a_duplicate_or_unhashed_or_unsafe_source_is_refused(self) -> None:
        payload = self.manifest()
        rows = _arr(payload["sources"])
        payload["sources"] = [rows[0], rows[0]]
        self.assertIn("duplicate source entry", self.refusal(payload))

        payload = self.manifest()
        first = dict(_obj(_arr(payload["sources"])[0]))
        del first["sha256"]
        payload["sources"] = [cast(Json, first)]
        self.assertIn("missing sha256", self.refusal(payload))

        payload = self.manifest()
        payload["sources"] = [{"path": "../escape.py", "sha256": "0" * 64}]
        self.assertIn("unsafe path in manifest", self.refusal(payload))

        payload = self.manifest()
        payload["sources"] = [{"path": "/etc/passwd", "sha256": "0" * 64}]
        self.assertIn("unsafe path in manifest", self.refusal(payload))

        payload = self.manifest()
        payload["sources"] = [{"path": "", "sha256": "0" * 64}]
        self.assertIn("non-empty string", self.refusal(payload))

    def test_an_absent_record_that_is_wrong_is_refused_and_a_right_one_passes(
        self,
    ) -> None:
        payload = self.manifest()
        payload["absent_at_snapshot"] = [
            {"path": "code", "present_at_snapshot": False, "pull_request": 0}
        ]
        self.assertIn("absent-at-snapshot record wrong", self.refusal(payload))

        payload = self.manifest()
        payload["absent_at_snapshot"] = [
            {"path": "code", "present_at_snapshot": True, "pull_request": 0}
        ]
        with self.written(payload):
            lines = VP.verify()
        self.assertIn("absent at snapshot: code (pull request 0)", lines)

    def test_a_frozen_text_that_moved_is_refused(self) -> None:
        payload = self.manifest()
        rows = _arr(payload["frozen_texts"])
        first = dict(_obj(rows[0]))
        first["sha256"] = "0" * 64
        payload["frozen_texts"] = [cast(Json, first), *rows[1:]]
        message = self.refusal(payload)
        self.assertIn("frozen text moved", message)

        payload = self.manifest()
        second = dict(_obj(_arr(payload["frozen_texts"])[0]))
        del second["sha256"]
        payload["frozen_texts"] = [cast(Json, second)]
        self.assertIn("missing sha256", self.refusal(payload))

    def test_a_snapshot_that_is_not_an_ancestor_is_refused(self) -> None:
        payload = self.manifest()
        with mock.patch.object(VP, "_ancestor", return_value="not an ancestor"):
            self.assertIn("of HEAD", self.refusal(payload))

    def test_the_snapshot_cannot_move_to_shrink_the_audited_history(self) -> None:
        payload = self.manifest()
        payload["snapshot_commit"] = "0" * 40
        message = self.refusal(payload)
        self.assertIn("independent required snapshot", message)
        self.assertIn(VP.REQUIRED_SNAPSHOT_COMMIT, message)

    def test_the_ancestor_relation_reports_an_undecided_git(self) -> None:
        """A git exit other than zero or one is reported as undecided rather
        than silently read as 'not an ancestor'."""

        class Result:
            returncode = 128

        with mock.patch("verify_pins.subprocess.run", return_value=Result()):
            self.assertEqual(VP._ancestor("0" * 40), "undecided (git exit 128)")

    def test_a_failing_git_call_is_reported_with_its_own_message(self) -> None:
        with self.assertRaises(ValueError) as caught:
            VP._git_bytes("show", "0" * 40 + ":nowhere")
        self.assertIn("git show", str(caught.exception))

    def test_the_hex40_reader_accepts_only_a_commit_id(self) -> None:
        self.assertTrue(VP._is_hex40("a" * 40))
        self.assertFalse(VP._is_hex40("A" * 40))
        self.assertFalse(VP._is_hex40("a" * 39))
        self.assertFalse(VP._is_hex40(40))

    def test_the_porcelain_reader_splits_nul_safe_rename_records(self) -> None:
        record = b"R  a/new.py\0a/old.py\0 M a/space name.py\0"
        with mock.patch.object(VP, "_git_bytes", return_value=record):
            paths = VP._worktree_paths()
        self.assertEqual(paths, ["a/new.py", "a/old.py", "a/space name.py"])

    def test_the_commit_path_reader_is_nul_safe_and_disables_renames(self) -> None:
        record = b"paper/old.md\0research/second_stream/new.md\0"
        with (
            mock.patch.object(
                VP, "_git", return_value="a" * 40 + " " + "b" * 40
            ),
            mock.patch.object(VP, "_git_bytes", return_value=record) as called,
        ):
            self.assertEqual(
                VP._commit_paths("a" * 40),
                ["paper/old.md", "research/second_stream/new.md"],
            )
        self.assertIn("--no-renames", called.call_args.args)

    def test_only_commits_that_touch_the_rung_are_scope_attributable(self) -> None:
        commits = ["a" * 40, "b" * 40]
        changed = [
            ["unrelated/future.md"],
            ["research/second_stream/stream.py", ".github/workflows/verify.yml"],
        ]
        with (
            mock.patch.object(VP, "_scope_commits", return_value=commits),
            mock.patch.object(VP, "_commit_paths", side_effect=changed),
        ):
            attributable, paths = VP._committed_scope(VP.REQUIRED_SNAPSHOT_COMMIT)
        self.assertEqual(attributable, ["b" * 40])
        self.assertEqual(paths, changed[1])

    def test_a_merge_contributes_only_its_combined_diff(self) -> None:
        """A merge is read with --cc, so it reports what its author wrote.

        The first-parent diff of a merge is everything the other branch
        brought with it. Reading that as the merge's own change is what made
        unrelated integration merges attributable to this rung.
        """
        record = b"research/second/MANUAL.md\0"
        with (
            mock.patch.object(
                VP, "_git", return_value=" ".join(["m" * 40, "p" * 40, "q" * 40])
            ),
            mock.patch.object(VP, "_git_bytes", return_value=record) as called,
        ):
            self.assertEqual(
                VP._commit_paths("m" * 40), ["research/second/MANUAL.md"]
            )
        self.assertIn("--cc", called.call_args.args)
        self.assertIn("diff-tree", called.call_args.args)
        self.assertIn("--no-renames", called.call_args.args)

    def test_an_ordinary_commit_is_still_read_against_its_first_parent(self) -> None:
        """The repair changes merges only; a single-parent commit is
        unaffected, and a root commit still reports its whole tree."""
        record = b"research/second_stream/stream.py\0"
        with (
            mock.patch.object(
                VP, "_git", return_value=" ".join(["c" * 40, "p" * 40])
            ),
            mock.patch.object(VP, "_git_bytes", return_value=record) as called,
        ):
            VP._commit_paths("c" * 40)
        self.assertIn("diff", called.call_args.args)
        self.assertNotIn("--cc", called.call_args.args)
        with (
            mock.patch.object(VP, "_git", return_value="d" * 40),
            mock.patch.object(VP, "_git_bytes", return_value=record) as called,
        ):
            VP._commit_paths("d" * 40)
        self.assertIn("ls-tree", called.call_args.args)

    def test_a_merge_that_only_carries_this_rung_along_is_not_attributed(
        self,
    ) -> None:
        """The observed failure, as a unit.

        On `main` at `7d2e6e86` three integration merges were attributed to
        this rung because their first-parent diff contained its whole tree,
        and the gate named boundary_seed, second_nofirst and second_stake
        files it had never touched. A merge that contributes nothing under
        the write root is not this rung's commit.
        """
        commits = ["a" * 40, "b" * 40]
        contributed = [
            [],
            ["research/boundary_seed/paper.md", "research/second_nofirst/STATUS.md"],
        ]
        with (
            mock.patch.object(VP, "_scope_commits", return_value=commits),
            mock.patch.object(VP, "_commit_paths", side_effect=contributed),
        ):
            attributable, paths = VP._committed_scope(VP.REQUIRED_SNAPSHOT_COMMIT)
        self.assertEqual(attributable, [])
        self.assertEqual(paths, [])

    def test_a_merge_that_writes_inside_and_outside_the_root_is_still_caught(
        self,
    ) -> None:
        """The narrowing must not blunt the gate.

        A merge whose author edited this rung's tree AND something outside it
        contributes both paths to its combined diff, so it is attributed and
        the outside path is refused by name. This is the shape the historical
        bundled-edit merge had, and it is the one case the repair must keep.
        """
        contributed = [["research/second_stream/stream.py", "research/other/x.md"]]
        with (
            mock.patch.object(VP, "_scope_commits", return_value=["m" * 40]),
            mock.patch.object(VP, "_commit_paths", side_effect=contributed),
        ):
            attributable, paths = VP._committed_scope(VP.REQUIRED_SNAPSHOT_COMMIT)
        self.assertEqual(attributable, ["m" * 40])
        with self.assertRaises(ValueError) as caught:
            VP._check_paths(paths, "rung-attributable committed diff")
        self.assertIn("research/other/x.md", str(caught.exception))

    def test_the_observed_integration_merge_contributes_nothing_here(self) -> None:
        """The real commit that turned `main` red, read from history.

        `45c8b994` merged the batch after pull requests 136 and 134. Under
        the first-parent rule it contributed this rung's whole tree; under
        the combined diff it contributes only what its author resolved, none
        of which is under this write root. Skipped rather than failed where
        the commit is absent, so the test cannot pass by not looking.
        """
        commit = "45c8b994503bc5602cf42ff048f322d6a20e1f52"
        try:
            kind = VP._git("cat-file", "-t", commit).strip()
        except ValueError:
            self.skipTest(f"{commit} is not in this clone")
        self.assertEqual(kind, "commit")
        contributed = VP._commit_paths(commit)
        self.assertTrue(contributed, "the merge resolved something")
        under_root = [p for p in contributed if p.startswith(VP.WRITE_ROOT)]
        self.assertEqual(under_root, [])

    def test_literal_backslashes_never_become_authorized_separators(self) -> None:
        raw = b"research\\second_stream\\smuggle.py"
        path = VP._decode_path(raw)
        self.assertEqual(path, raw.decode("utf-8"))
        with self.assertRaises(ValueError) as caught:
            VP._check_paths([path], "committed diff")
        self.assertIn("outside the write root", str(caught.exception))

    def test_the_write_scope_names_a_sealed_path_and_an_outside_path(self) -> None:
        with (
            mock.patch.object(VP, "_committed_scope", return_value=([], [])),
            mock.patch.object(VP, "_worktree_paths", return_value=["paper/paper.md"]),
        ):
            with self.assertRaises(ValueError) as sealed:
                VP._check_write_scope("a" * 40)
        self.assertIn("sealed path changed", str(sealed.exception))
        self.assertIn("paper/paper.md", str(sealed.exception))

        with (
            mock.patch.object(VP, "_committed_scope", return_value=([], [])),
            mock.patch.object(VP, "_worktree_paths", return_value=["research/zz.md"]),
        ):
            with self.assertRaises(ValueError) as outside:
                VP._check_write_scope("a" * 40)
        self.assertIn("outside the write root", str(outside.exception))

        allowed = [
            "research/second_stream/stream.py",
            ".github/workflows/verify.yml",
            "research/second/HANDOFF.md",
        ]
        with (
            mock.patch.object(VP, "_committed_scope", return_value=(["a" * 40], allowed)),
            mock.patch.object(VP, "_worktree_paths", return_value=allowed),
        ):
            self.assertEqual(len(VP._check_write_scope("a" * 40)), 2)

        with self.assertRaises(ValueError) as committed:
            VP._check_paths(["artifacts/claims.json"], "committed diff")
        self.assertIn("committed diff", str(committed.exception))

    def test_repin_rewrites_source_hashes_and_moves_nothing_else(self) -> None:
        payload = self.manifest()
        rows = [dict(_obj(row)) for row in _arr(payload["sources"])]
        rows[0]["sha256"] = "0" * 64
        payload["sources"] = [cast(Json, row) for row in rows]
        frozen_before = payload["frozen_texts"]
        snapshot_before = payload["snapshot_commit"]
        with self.written(payload) as path:
            lines = VP.repin()
            after = cast(dict[str, Json], json.loads(path.read_text("utf-8")))
        self.assertTrue(any(line.startswith("rehashed: ") for line in lines))
        self.assertIn("snapshot_commit NOT moved", lines[-1])
        self.assertEqual(after["frozen_texts"], frozen_before)
        self.assertEqual(after["snapshot_commit"], snapshot_before)
        self.assertEqual(after["sources"], self.manifest()["sources"])

    def test_repin_refuses_a_manifest_whose_sources_are_not_a_list(self) -> None:
        payload = self.manifest()
        payload["sources"] = "all of them"
        with self.written(payload):
            with self.assertRaises(ValueError) as caught:
                VP.repin()
        self.assertIn("must list sources", str(caught.exception))

        payload = self.manifest()
        payload["sources"] = ["x"]
        with self.written(payload):
            with self.assertRaises(ValueError) as caught:
                VP.repin()
        self.assertIn("each source entry must be an object", str(caught.exception))

    def test_the_entry_point_returns_zero_on_a_pass_and_one_on_a_refusal(self) -> None:
        out = io.StringIO()
        with mock.patch.object(sys, "argv", ["verify_pins.py"]):
            with contextlib.redirect_stdout(out):
                self.assertEqual(VP.main(), 0)
        self.assertIn("second_stream pins verified:", out.getvalue())

        payload = self.manifest()
        payload["schema"] = "wrong"
        out = io.StringIO()
        with self.written(payload):
            with mock.patch.object(sys, "argv", ["verify_pins.py"]):
                with contextlib.redirect_stdout(out):
                    self.assertEqual(VP.main(), 1)
        self.assertTrue(out.getvalue().startswith("FAIL: "))

    def test_the_entry_point_can_repin_without_verifying(self) -> None:
        payload = self.manifest()
        out = io.StringIO()
        with self.written(payload):
            with mock.patch.object(sys, "argv", ["verify_pins.py", "--repin"]):
                with contextlib.redirect_stdout(out):
                    self.assertEqual(VP.main(), 0)
        self.assertIn("repinned sources from HEAD", out.getvalue())

# ---------------------------------------------------------------------------
# The coverage gate
# ---------------------------------------------------------------------------


class CoverageGateTests(unittest.TestCase):
    """Pins: 'the rung measures its own line and branch coverage from inside
    the tree and fails by name below ninety-five percent of either, on a
    measured file set that differs from its own modules, or on a report older
    than a source it claims to have measured.'

    ``research/second/SEED.md`` requires both thresholds and rung zero left
    them as an operator claim.  This rung shipped at 90.40% line and 85.55%
    branch with nothing anywhere that would have said so, so the gate is
    exercised on each of its refusals rather than trusted because it is
    green.
    """

    def report(self, **overrides: object) -> dict[str, Json]:
        body: dict[str, Json] = {
            "meta": {"timestamp": "2026-09-04T00:00:00.000000"},
            "files": {name: {} for name in CC.MEASURED},
            "totals": {
                "covered_lines": 99,
                "num_statements": 100,
                "covered_branches": 99,
                "num_branches": 100,
            },
        }
        for key, value in overrides.items():
            body[key] = cast(Json, value)
        return body

    @contextlib.contextmanager
    def written(self, payload: Mapping[str, Json]):  # type: ignore[no-untyped-def]
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "coverage.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with mock.patch.object(CC, "REPORT", path):
                with mock.patch.object(CC, "HERE", pathlib.Path(tmp)):
                    yield path

    def refusal(self, payload: Mapping[str, Json]) -> str:
        with self.written(payload):
            with self.assertRaises(ValueError) as caught:
                CC.check()
        return str(caught.exception)

    def test_the_committed_thresholds_are_the_seed_s(self) -> None:
        self.assertEqual(CC.LINE_FLOOR, 95.0)
        self.assertEqual(CC.BRANCH_FLOOR, 95.0)
        self.assertEqual(
            CC.MEASURED, ("run_stream.py", "stream.py", "verify_pins.py")
        )
        self.assertEqual(CC._production_modules(HERE), CC.MEASURED)
        config = tomllib.loads((HERE / "pyproject.toml").read_text(encoding="utf-8"))
        configured = tuple(sorted(config["tool"]["coverage"]["run"]["source"]))
        self.assertEqual(configured, tuple(sorted(pathlib.Path(n).stem for n in CC.MEASURED)))
        self.assertNotIn("check_coverage.py", CC.MEASURED)
        for name in CC.MEASURED:
            self.assertTrue((HERE / name).exists(), f"{name} is not a file of the tree")

    def test_the_production_census_recurses_without_collapsing_basenames(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            (root / "top.py").write_text("", encoding="utf-8")
            (root / "pkg").mkdir()
            (root / "pkg" / "top.py").write_text("", encoding="utf-8")
            (root / "pkg" / "worker.py").write_text("", encoding="utf-8")
            (root / "pkg" / "check_coverage.py").write_text("", encoding="utf-8")
            (root / "pkg" / "test_skip.py").write_text("", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "helper.py").write_text("", encoding="utf-8")
            self.assertEqual(
                CC._production_modules(root),
                (
                    "pkg/check_coverage.py",
                    "pkg/top.py",
                    "pkg/worker.py",
                    "top.py",
                ),
            )

    def test_a_well_formed_report_passes_and_names_what_it_measured(self) -> None:
        with self.written(self.report()):
            lines = CC.check()
        joined = "\n".join(lines)
        self.assertIn("line coverage 99.00%", joined)
        self.assertIn("branch coverage 99.00%", joined)
        self.assertIn("both thresholds of 95% met", joined)

    def test_line_and_branch_are_refused_independently(self) -> None:
        low_line = self.report(
            totals={
                "covered_lines": 90,
                "num_statements": 100,
                "covered_branches": 99,
                "num_branches": 100,
            }
        )
        message = self.refusal(low_line)
        self.assertIn("line coverage 90.00% is below 95%", message)
        self.assertNotIn("branch coverage", message)

        low_branch = self.report(
            totals={
                "covered_lines": 99,
                "num_statements": 100,
                "covered_branches": 85,
                "num_branches": 100,
            }
        )
        message = self.refusal(low_branch)
        self.assertIn("branch coverage 85.00% is below 95%", message)
        self.assertNotIn("line coverage", message)

    def test_a_dropped_module_fails_the_file_set_rather_than_raising_the_score(
        self,
    ) -> None:
        """The defect this gate was written after: a module named in the
        coverage source that no test imports is dropped with a warning, which
        makes the denominator smaller and the percentage larger."""

        dropped = self.report(
            files={name: {} for name in CC.MEASURED if name != "verify_pins.py"}
        )
        message = self.refusal(dropped)
        self.assertIn("measured file set differs", message)
        self.assertIn("verify_pins.py", message)

        extra = self.report(files={**{n: {} for n in CC.MEASURED}, "zz_probe.py": {}})
        self.assertIn("measured file set differs", self.refusal(extra))

    def test_a_report_older_than_a_source_it_measured_is_refused(self) -> None:
        with self.written(self.report()) as path:
            source = path.parent / "stream.py"
            source.write_text("# newer than the report" + chr(10), encoding="utf-8")
            stamp = path.stat().st_mtime + 60.0
            os.utime(source, (stamp, stamp))
            with self.assertRaises(ValueError) as caught:
                CC.check()
        self.assertIn("newer than the report", str(caught.exception))
        self.assertIn("stream.py", str(caught.exception))

    def test_every_malformation_of_the_report_is_refused_by_name(self) -> None:
        table: Sequence[tuple[str, object, str]] = (
            ("files", "all of them", "must carry a files object"),
            ("meta", [], "must carry a meta object"),
            ("meta", {}, "no meta.timestamp"),
            ("totals", [], "must carry a totals object"),
        )
        for key, value, fragment in table:
            with self.subTest(key=key, value=value):
                self.assertIn(fragment, self.refusal(self.report(**{key: value})))

        self.assertIn(
            "no statements at all",
            self.refusal(
                self.report(
                    totals={
                        "covered_lines": 0,
                        "num_statements": 0,
                        "covered_branches": 1,
                        "num_branches": 1,
                    }
                )
            ),
        )
        self.assertIn(
            "no branches at all",
            self.refusal(
                self.report(
                    totals={
                        "covered_lines": 1,
                        "num_statements": 1,
                        "covered_branches": 0,
                        "num_branches": 0,
                    }
                )
            ),
        )
        self.assertIn(
            "is not a count",
            self.refusal(
                self.report(
                    totals={
                        "covered_lines": True,
                        "num_statements": 1,
                        "covered_branches": 1,
                        "num_branches": 1,
                    }
                )
            ),
        )

    def test_a_missing_or_unreadable_report_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "coverage.json"
            with mock.patch.object(CC, "REPORT", path):
                with self.assertRaises(ValueError) as caught:
                    CC.check()
            self.assertIn("is missing", str(caught.exception))
            path.write_text("[]", encoding="utf-8")
            with mock.patch.object(CC, "REPORT", path):
                with self.assertRaises(ValueError) as caught:
                    CC.check()
            self.assertIn("must be an object", str(caught.exception))

    def test_the_entry_point_returns_zero_on_a_pass_and_one_on_a_refusal(self) -> None:
        out = io.StringIO()
        with self.written(self.report()):
            with contextlib.redirect_stdout(out):
                self.assertEqual(CC.main(), 0)
        self.assertIn("both thresholds", out.getvalue())

        out = io.StringIO()
        with self.written(self.report(files={})):
            with contextlib.redirect_stdout(out):
                self.assertEqual(CC.main(), 1)
        self.assertTrue(out.getvalue().startswith("FAIL: "))

if __name__ == "__main__":
    unittest.main()
