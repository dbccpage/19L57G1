"""The rung-four computation, its counters, its witnesses and its runner.

Every counter of `iso_index.py` is shown to COUNT: a blinded or tampered
procedure is fed to it and the counter moves.  A zero that cannot move is
not a measurement.  The exhibited histories of the Lean countermodels are
replayed through the sealed step and compared with the Lean text.  The
runner's scorer is shown to score a doctored report as a miss.

The full rectangle is built ONCE per test process and shared, because it
takes seconds; every negative test runs on a small declared rectangle or
on synthetic input instead.
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys
import tempfile
import unittest
from typing import Any, Optional
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import iso_index as ix  # noqa: E402

if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import run_iso_index as run  # noqa: E402

from derivation.iso import canonical, canonical_bruteforce  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
    step,
)
from index import Alphabet, Observations, first_index_scan  # noqa: E402
from nofirst import APART, FREE, SAME, demands  # noqa: E402

LEAN = HERE / "lean" / "SecondIso"
RECEIPT = HERE / "receipts" / run.RECEIPT_NAME

SMALL = Alphabet(
    supply_token="<z>",
    fresh_tokens=("<n0>", "<n1>", "<n2>", "<n3>", "<n4>"),
    arities=(1, 2),
    max_data=5,
    max_forms=2,
    max_length=2,
)

_PAYLOAD: Optional[dict[str, Any]] = None


def payload() -> dict[str, Any]:
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = run.build()
    return _PAYLOAD


def reports() -> dict[str, Any]:
    found = payload()["reports"]
    assert isinstance(found, dict)
    return found


def lean_event(event: Event) -> str:
    """The Lean spelling of a sealed event, for the textual comparison
    with the Lean countermodels.  The Lean datum admission carries no
    token, so a token is dropped here, never compared."""
    if isinstance(event, AdmitForm):
        return f".admitForm {event.arity}"
    if isinstance(event, AdmitDatum):
        return ".admitDatum"
    if isinstance(event, AdmitInst):
        return f".admitInst {event.form} [{', '.join(str(a) for a in event.args)}]"
    if isinstance(event, AdmitRuleAll):
        return f".admitRuleAll {event.form}"
    raise TypeError(type(event).__name__)


def lean_parity(i: int, j: int) -> str:
    """A transcription of the Lean `parity` label on a pair of distinct
    indices; compared with the Lean text below and with the sibling rule."""
    return SAME if (i + j) % 2 == 0 else APART


def lean_residue(i: int, j: int) -> str:
    return SAME if (max(i, j) - min(i, j)) % 3 == 0 else APART


def lean_chain(i: int, j: int) -> str:
    return APART if (i + 1 == j or j + 1 == i) else FREE


def regime_of(history: tuple[Event, ...]) -> Regime:
    return replay(history, EMPTY)


class ExhibitedHistoryTests(unittest.TestCase):
    """The Lean countermodels' histories, replayed in Python."""

    def setUp(self) -> None:
        self.histories = ix.exhibited_histories()
        self.seen = Observations()

    def test_the_pairs_are_class_matched_by_both_key_procedures(self) -> None:
        for pair in ("P", "Q"):
            one = ix.prefix_regimes(self.histories[pair + "1"])
            two = ix.prefix_regimes(self.histories[pair + "2"])
            self.assertEqual(len(one), len(two))
            for a, b in zip(one, two):
                self.assertEqual(canonical(a), canonical(b))
                self.assertEqual(canonical_bruteforce(a), canonical_bruteforce(b))

    def test_the_pairs_differ_in_one_event_and_it_is_the_rule(self) -> None:
        for pair in ("P", "Q"):
            one, two = self.histories[pair + "1"], self.histories[pair + "2"]
            differing = [(a, b) for a, b in zip(one, two) if a != b]
            self.assertEqual(len(differing), 1)
            self.assertIsInstance(differing[0][0], AdmitRuleAll)
            self.assertIsInstance(differing[0][1], AdmitRuleAll)

    def test_the_first_counts_by_both_rung_three_procedures(self) -> None:
        expected = {
            ("P", "parity"): (None, 8),
            ("P", "chain"): (None, 8),
            ("Q", "residue_three"): (None, 11),
        }
        for (pair, name), (first, second) in expected.items():
            stake = ix.stake_named(name)
            for label, want in ((pair + "1", first), (pair + "2", second)):
                history = self.histories[label]
                self.assertEqual(
                    ix.first_index_forward(EMPTY, history, stake, self.seen), want
                )
                self.assertEqual(first_index_scan(EMPTY, history, stake, self.seen), want)

    def test_uniform_stakes_give_the_pairs_one_count(self) -> None:
        """The rectangle's echo of `first_demand_matched_of_uniform`."""
        for name in ("free", "total_apart", "total_same", "one_sided_total"):
            stake = ix.stake_named(name)
            for pair in ("P", "Q"):
                self.assertEqual(
                    ix.first_index_forward(EMPTY, self.histories[pair + "1"], stake, self.seen),
                    ix.first_index_forward(EMPTY, self.histories[pair + "2"], stake, self.seen),
                )

    def test_the_python_histories_are_the_lean_ones(self) -> None:
        text = (LEAN / "Countermodel.lean").read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for name, history in self.histories.items():
            spelled = "[" + ", ".join(lean_event(e) for e in history) + "]"
            self.assertIn(f"def {name} : List Event := {spelled}", flat, name)

    def test_the_lean_stake_formulas_are_the_sibling_rules(self) -> None:
        """The transcriptions above against the sibling rules, on every pair
        of distinct indices below twelve; and the transcriptions against the
        Lean text, as text."""
        for name, formula in (
            ("parity", lean_parity),
            ("residue_three", lean_residue),
            ("chain", lean_chain),
        ):
            stake = ix.stake_named(name)
            for j in range(12):
                for i in range(j):
                    self.assertEqual(stake.label(i, j), formula(i, j), (name, i, j))
        text = (LEAN / "Countermodel.lean").read_text(encoding="utf-8")
        self.assertIn("else if (i + j) % 2 = 0 then Label.same else Label.apart", text)
        self.assertIn(
            "else if (max i j - min i j) % 3 = 0 then Label.same else Label.apart", text
        )
        self.assertIn(
            "if i + 1 = j ∨ j + 1 = i then Label.apart else Label.free", text
        )

    def test_the_lean_regime_pairs_carry_what_the_lean_says(self) -> None:
        tokens = ix.ALPHABET.fresh_tokens
        three = tuple(AdmitDatum(t) for t in tokens[:3])
        four = tuple(AdmitDatum(t) for t in tokens[:4])
        pr0 = regime_of(three + (AdmitForm(1), AdmitInst(0, (0,))))
        pr1 = regime_of(three + (AdmitForm(1), AdmitInst(0, (1,))))
        rr0 = regime_of(four + (AdmitForm(1), AdmitForm(1), AdmitInst(0, (0,)), AdmitInst(1, (2,))))
        rr1 = regime_of(four + (AdmitForm(1), AdmitForm(1), AdmitInst(0, (1,)), AdmitInst(1, (2,))))
        self.assertEqual(canonical(pr0), canonical(pr1))
        self.assertEqual(canonical(rr0), canonical(rr1))
        for name in ("parity", "chain"):
            stake = ix.stake_named(name)
            self.assertTrue(demands(stake, pr0), name)
            self.assertFalse(demands(stake, pr1), name)
        stake = ix.stake_named("residue_three")
        self.assertTrue(demands(stake, rr0))
        self.assertFalse(demands(stake, rr1))
        text = (LEAN / "Countermodel.lean").read_text(encoding="utf-8")
        for spelled in (
            "def pr0 : Regime := ⟨3, [1], [(0, [0])], [], []⟩",
            "def pr1 : Regime := ⟨3, [1], [(0, [1])], [], []⟩",
            "def rr0 : Regime := ⟨4, [1, 1], [(0, [0]), (1, [2])], [], []⟩",
            "def rr1 : Regime := ⟨4, [1, 1], [(0, [1]), (1, [2])], [], []⟩",
        ):
            self.assertIn(spelled, text)

    def test_an_unknown_stake_is_refused(self) -> None:
        with self.assertRaises(KeyError):
            ix.stake_named("no_such_stake")

    def test_the_lean_spelling_refuses_an_event_it_does_not_name(self) -> None:
        with self.assertRaises(TypeError):
            lean_event(Supply("<z>"))


class ClassTests(unittest.TestCase):
    """Classes of reached regimes, and the two readings of carrying a
    demand, on a small declared rectangle."""

    population: ix.Population

    @classmethod
    def setUpClass(cls) -> None:
        cls.population = ix.build_population(SMALL)

    def test_the_small_population_is_sorted_and_distinct(self) -> None:
        regimes = self.population.regimes
        self.assertEqual(len(regimes), len(set(regimes)))
        self.assertEqual(list(regimes), sorted(regimes, key=ix.regime_order))

    def test_the_two_key_procedures_agree(self) -> None:
        self.assertEqual(
            ix.partition_disagreements(self.population.regimes, ix.Keys()), 0
        )

    def test_a_blinded_brute_force_key_is_counted(self) -> None:
        """NEGATIVE: a key that forgets everything but the data count merges
        classes, and the disagreement counter moves."""

        class Blind(ix.Keys):
            def brute(self, regime: Regime) -> Any:
                return regime.n_data()

        self.assertGreater(
            ix.partition_disagreements(self.population.regimes, Blind()), 0
        )

    def test_the_key_cache_returns_what_it_stored(self) -> None:
        keys = ix.Keys()
        regime = self.population.regimes[-1]
        self.assertIs(keys.key(regime), keys.key(regime))
        self.assertIs(keys.brute(regime), keys.brute(regime))

    def test_the_automorphism_counts_agree_and_a_wrong_one_is_counted(self) -> None:
        report = ix.automorphism_report(self.population.regimes)
        self.assertEqual(report["disagreements"], 0)
        with mock.patch.object(ix, "brute_automorphism_count", return_value=0):
            wrong = ix.automorphism_report(self.population.regimes)
        self.assertEqual(wrong["disagreements"], len(self.population.regimes))

    def test_the_brute_automorphism_count_of_known_regimes(self) -> None:
        self.assertEqual(ix.brute_automorphism_count(EMPTY), 1)
        tokens = ix.ALPHABET.fresh_tokens
        three = regime_of(tuple(AdmitDatum(t) for t in tokens[:3]))
        self.assertEqual(ix.brute_automorphism_count(three), 6)
        marked = step(three, AdmitForm(1))
        marked = step(marked, AdmitInst(0, (0,)))
        self.assertEqual(ix.brute_automorphism_count(marked), 2)

    def test_the_two_demand_procedures_agree_on_every_small_regime(self) -> None:
        seen = Observations()
        stakes = ix.declared_stakes()
        for regime in self.population.regimes:
            self.assertEqual(
                ix.statuses_from_profiles(stakes, regime),
                tuple(seen.carries(s, regime) for s in stakes),
            )
            for stake in stakes:
                self.assertEqual(
                    ix.carries_from_profiles(stake, regime), seen.carries(stake, regime)
                )

    def test_the_single_stake_procedure_reads_both_labels(self) -> None:
        tokens = ix.ALPHABET.fresh_tokens
        two = regime_of(tuple(AdmitDatum(t) for t in tokens[:2]))
        apart = ix.stake_named("total_apart")
        same = ix.stake_named("total_same")
        self.assertTrue(ix.carries_from_profiles(apart, two))
        self.assertFalse(ix.carries_from_profiles(same, two))
        split = step(step(two, AdmitForm(1)), AdmitInst(0, (0,)))
        self.assertFalse(ix.carries_from_profiles(apart, split))
        self.assertTrue(ix.carries_from_profiles(same, split))

    def test_a_blinded_second_procedure_is_counted(self) -> None:
        """NEGATIVE: a second procedure that never sees a demand disagrees
        with the sibling's, and the counter moves; the orbit, read through
        the blinded procedure, then misses a reached status too."""
        stakes = ix.declared_stakes()
        blind = tuple(False for _ in stakes)
        with mock.patch.object(ix, "statuses_from_profiles", return_value=blind):
            report = ix.class_split_report(self.population, stakes, Observations())
        self.assertGreater(report["demand_procedure_disagreements"], 0)
        self.assertGreater(report["orbit_misses_reached_status"], 0)

    def test_the_orbit_is_every_bijection_pair(self) -> None:
        tokens = ix.ALPHABET.fresh_tokens
        three = regime_of(tuple(AdmitDatum(t) for t in tokens[:3]) + (AdmitForm(1), AdmitForm(1)))
        presentations = list(ix.orbit(three))
        self.assertEqual(len(presentations), 12)
        self.assertEqual(len({canonical(r) for r in presentations}), 1)

    def test_an_orbit_beyond_the_declared_bound_is_refused(self) -> None:
        six = regime_of(tuple(AdmitDatum(f"<t{k}>") for k in range(6)))
        with self.assertRaises(ValueError) as caught:
            list(ix.orbit(six))
        self.assertIn("declared bound 240", str(caught.exception))

    def test_the_witness_of_a_split_class_replays(self) -> None:
        witness = reports()["class_split"]["reached_split_witness"]
        for name in ("parity", "chain", "residue_three"):
            entry = witness[name]
            regimes = []
            for side in ("carrying", "quiet"):
                base = entry[side]["base"]
                events = [e for e in _parse_history(entry[side]["history"])]
                regime = replay(ix.base_genesis(base) + tuple(events), EMPTY)
                regimes.append(regime)
            self.assertEqual(canonical(regimes[0]), canonical(regimes[1]), name)
            stake = ix.stake_named(name)
            self.assertTrue(demands(stake, regimes[0]), name)
            self.assertFalse(demands(stake, regimes[1]), name)
        for name in ("free", "total_apart", "total_same", "one_sided_total"):
            self.assertIsNone(witness[name])

    def test_the_first_reaching_witness_is_the_least_descriptor(self) -> None:
        found = ix.first_reaching(self.population)
        self.assertEqual(set(found), set(self.population.regimes))
        for regime, (base, history) in found.items():
            self.assertIn(base, ix.BASE_NAMES)
            self.assertIsInstance(history, tuple)


def _parse_history(descriptors: list[str]) -> list[Event]:
    """Read back rung three's event descriptors, for replaying a receipt
    witness by hand."""
    out: list[Event] = []
    for text in descriptors:
        kind, _, rest = text.partition("(")
        body = rest[:-1]
        if kind == "AdmitDatum":
            out.append(AdmitDatum(body))
        elif kind == "Supply":
            out.append(Supply(body))
        elif kind == "AdmitForm":
            out.append(AdmitForm(int(body)))
        elif kind == "AdmitRuleAll":
            out.append(AdmitRuleAll(int(body)))
        elif kind == "AdmitInst":
            form, _, args = body.partition(",")
            out.append(AdmitInst(int(form), tuple(json.loads(args))))
        elif kind == "Impose":
            i, _, j = body.partition(",")
            out.append(Impose(int(i), int(j)))
        else:  # pragma: no cover - every descriptor kind is listed
            raise ValueError(text)
    return out


class TrajectoryTests(unittest.TestCase):
    def test_varying_classes_reads_both_modes(self) -> None:
        stakes = ix.declared_stakes()[:2]
        groups: list[list[tuple[Optional[int], ...]]] = [
            [(1, None), (1, 2)],
            [(None, 3), (4, 3)],
        ]
        self.assertEqual(
            ix.varying_classes(groups, stakes, ignore_absent=False),
            {stakes[0].name: 1, stakes[1].name: 1},
        )
        self.assertEqual(
            ix.varying_classes(groups, stakes, ignore_absent=True),
            {stakes[0].name: 0, stakes[1].name: 0},
        )

    def test_a_tampered_count_in_a_shared_trajectory_is_counted(self) -> None:
        """NEGATIVE: one sequence of a class with two members given a
        different first count makes that class vary."""
        population = ix.build_population(SMALL)
        stakes = ix.declared_stakes()
        seen = Observations()
        table = ix.index_table(population, stakes, seen)
        clean = ix.trajectory_report(population, table, stakes)
        self.assertEqual(
            set(clean["trajectory_classes_with_varying_count"].values()), {0}
        )
        groups: dict[tuple[Any, ...], list[tuple[str, tuple[Event, ...]]]] = {}
        for base, history, traj in ix.trajectories(population):
            groups.setdefault(traj, []).append((base, history))
        shared = next(v for v in groups.values() if len(v) > 1)
        tampered = dict(table)
        tampered[shared[0]] = tuple(99 for _ in stakes)
        report = ix.trajectory_report(population, tampered, stakes)
        self.assertEqual(
            set(report["trajectory_classes_with_varying_count"].values()), {1}
        )

    def test_every_sequence_has_a_trajectory_as_long_as_it(self) -> None:
        population = ix.build_population(SMALL)
        for _base, history, traj in ix.trajectories(population):
            self.assertEqual(len(traj), len(history) + 1)


class TokenTests(unittest.TestCase):
    def test_the_declared_renaming(self) -> None:
        fresh = ix.ALPHABET.fresh_tokens
        self.assertEqual(ix.renamed_token(fresh[0], ix.ALPHABET), fresh[-1])
        self.assertEqual(ix.renamed_token(fresh[1], ix.ALPHABET), fresh[-2])
        self.assertEqual(
            ix.renamed_token(ix.ALPHABET.supply_token, ix.ALPHABET),
            ix.RENAMED_SUPPLY_TOKEN,
        )
        self.assertEqual(ix.renamed_token("<a>", ix.ALPHABET), "<a>")

    def test_the_renamed_supply_token_is_carried_by_no_base(self) -> None:
        for base in ix.BASE_NAMES:
            for event in ix.base_genesis(base):
                if isinstance(event, (Supply, AdmitDatum)):
                    self.assertNotEqual(event.token, ix.RENAMED_SUPPLY_TOKEN)

    def test_a_history_is_renamed_event_by_event(self) -> None:
        history: tuple[Event, ...] = (
            Supply("<z>"), AdmitDatum("<n0>"), AdmitForm(1), Impose(0, 1)
        )
        self.assertEqual(
            ix.rename_history(history, ix.ALPHABET),
            (Supply("<y>"), AdmitDatum("<n4>"), AdmitForm(1), Impose(0, 1)),
        )

    def test_a_collapsing_renaming_is_counted(self) -> None:
        """NEGATIVE: a renaming that sends every fresh token to one token
        turns a second datum admission into a designation, which moves the
        class of a prefix and the first count, and both counters move."""
        population = ix.build_population(SMALL)
        stakes = ix.declared_stakes()
        seen = Observations()
        table = ix.index_table(population, stakes, seen)
        clean = ix.token_report(population, table, stakes, seen, SMALL)
        self.assertEqual(clean["sequences_with_a_moved_count"], 0)
        self.assertEqual(clean["sequences_with_a_moved_class"], 0)
        self.assertGreater(clean["sequences_whose_presentation_changed"], 0)
        with mock.patch.object(ix, "renamed_token", return_value="<n0>"):
            moved = ix.token_report(population, table, stakes, seen, SMALL)
        self.assertGreater(moved["sequences_with_a_moved_count"], 0)
        self.assertGreater(moved["sequences_with_a_moved_class"], 0)

    def test_a_renamed_sequence_that_does_not_replay_is_refused(self) -> None:
        population = ix.build_population(SMALL)
        stakes = ix.declared_stakes()
        seen = Observations()
        table = ix.index_table(population, stakes, seen)
        with mock.patch.object(ix, "replay", return_value=EMPTY):
            with self.assertRaises(RuntimeError):
                ix.token_report(population, table, stakes, seen, SMALL)


class ReceiptTests(unittest.TestCase):
    def test_the_committed_receipt_matches_a_fresh_run(self) -> None:
        self.assertEqual(
            RECEIPT.read_bytes().replace(b"\r\n", b"\n"), run.render(payload())
        )

    def test_the_receipt_carries_no_environment_value(self) -> None:
        self.assertEqual(run.forbidden_keys(payload()), [])

    def test_the_forbidden_key_scan_reads_every_depth(self) -> None:
        probe = {"a": [{"b": 1}, {"Timestamp": 2}], "env": {}}
        self.assertEqual(sorted(run.forbidden_keys(probe)), ["a[1].Timestamp", "env"])

    def test_the_receipt_stays_under_one_megabyte(self) -> None:
        self.assertLess(len(run.render(payload())), run.MEGABYTE)

    def test_the_frozen_digests_are_checkout_independent(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        frozen = {item["path"]: item["sha256"] for item in manifest["frozen_texts"]}
        self.assertEqual(run.frozen_digest("PROMPT.md"), frozen["research/second_iso/PROMPT.md"])
        self.assertEqual(
            run.frozen_digest("PREDICTIONS.md"), frozen["research/second_iso/PREDICTIONS.md"]
        )

    def test_the_rung_three_counts_replay(self) -> None:
        sibling = json.loads(
            (HERE.parent / "second_index" / "receipts" / "index.json").read_text(encoding="utf-8")
        )
        recorded = {r["base"]: r["nodes"] for r in sibling["reports"]}
        found = {base: v["nodes"] for base, v in reports()["bases"].items()}
        self.assertEqual(found, recorded)

    def test_the_input_count_claim_is_absent(self) -> None:
        self.assertEqual(payload()["input_count_claim"], "none")


class ScoringTests(unittest.TestCase):
    def test_every_computational_prediction_is_scored_from_the_run(self) -> None:
        scored = payload()["predictions_scored"]
        verdicts = {pid: row["verdict"] for pid, row in scored.items()}
        self.assertEqual(verdicts["J-12"], "MISSED")
        for pid in ("J-10", "J-11", "J-13", "J-14", "J-15", "J-16", "J-17", "J-18"):
            self.assertEqual(verdicts[pid], "HIT", pid)
        for pid in ("J-1", "J-2", "J-3", "J-4", "J-5", "J-6", "J-7", "J-8", "J-9",
                    "J-19", "J-20", "J-21", "J-22"):
            self.assertEqual(verdicts[pid], "ELSEWHERE", pid)
        self.assertEqual(len(verdicts), 22)

    def test_the_recorded_miss_carries_its_value(self) -> None:
        row = payload()["predictions_scored"]["J-12"]
        self.assertEqual(row["value"]["largest"], 240)
        self.assertEqual(row["value"]["smallest"], 1)
        self.assertEqual(row["value"]["disagreements"], 0)

    def test_a_doctored_report_is_scored_as_a_miss(self) -> None:
        """NEGATIVE: each computational row turns to MISSED when the value
        it reads is doctored.  A scoreboard of hits is not a rubber stamp."""
        doctorings: dict[str, Any] = {
            "J-10": lambda r: r["bases"]["L"].__setitem__("nodes", 1),
            "J-11": lambda r: r.__setitem__("key_partition_disagreements", 1),
            "J-13": lambda r: r["class_split"]["reached_split_classes"].__setitem__("total_apart", 1),
            "J-14": lambda r: r["class_split"]["orbit_split_classes"].__setitem__("parity", 0),
            "J-15": lambda r: r["trajectory"]["trajectory_classes_with_varying_count"].__setitem__("chain", 1),
            "J-16": lambda r: r["trajectory"]["final_classes_with_two_counts"].__setitem__("free", 1),
            "J-17": lambda r: r["tokens"].__setitem__("sequences_with_a_moved_count", 1),
            "J-18": lambda r: r["exhibited"]["P"].__setitem__("prefix_pairs_in_two_classes", 1),
        }
        for pid, doctor in doctorings.items():
            doctored = copy.deepcopy(reports())
            doctor(doctored)
            self.assertEqual(run.score(doctored)[pid]["verdict"], "MISSED", pid)

    def test_a_corrected_extreme_would_have_hit(self) -> None:
        """The miss is the prediction's, not the scorer's: the same scorer
        gives HIT when the largest size is the one predicted."""
        doctored = copy.deepcopy(reports())
        doctored["automorphisms"]["largest"] = 24
        self.assertEqual(run.score(doctored)["J-12"]["verdict"], "HIT")


class RunnerTests(unittest.TestCase):
    def _main(self, argv: list[str], built: dict[str, Any]) -> int:
        with mock.patch.object(run, "build", return_value=built):
            return run.main(argv)

    def test_the_runner_writes_where_told_and_checks_what_it_wrote(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._main(["--receipts", tmp], payload()), 0)
            self.assertEqual(self._main(["--receipts", tmp, "--check"], payload()), 0)

    def test_a_missing_receipt_fails_the_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._main(["--receipts", tmp, "--check"], payload()), 1)

    def test_a_drifted_receipt_fails_the_check_without_being_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / run.RECEIPT_NAME
            target.write_bytes(b"{}\n")
            self.assertEqual(self._main(["--receipts", tmp, "--check"], payload()), 1)
            self.assertEqual(target.read_bytes(), b"{}\n")

    def test_a_payload_with_a_forbidden_key_is_refused(self) -> None:
        bad = copy.deepcopy(payload())
        bad["reports"]["timestamp"] = "now"
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._main(["--receipts", tmp], bad), 1)
            self.assertFalse((pathlib.Path(tmp) / run.RECEIPT_NAME).exists())

    def test_an_oversized_payload_is_refused(self) -> None:
        big = copy.deepcopy(payload())
        big["padding"] = "x" * run.MEGABYTE
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._main(["--receipts", tmp], big), 1)
            self.assertFalse((pathlib.Path(tmp) / run.RECEIPT_NAME).exists())


if __name__ == "__main__":
    unittest.main()
