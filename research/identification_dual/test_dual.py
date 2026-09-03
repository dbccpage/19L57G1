"""Tests for the identification dual.

Run from this directory: ``python -m unittest discover -s . -p "test_*.py"``.
The sealed kernel is found through ``dual.py``, which puts the repository's
``code/`` directory on the path.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from dual import (  # noqa: E402
    IDENTIFY,
    SEPARATE,
    Genesis,
    RequireSame,
    Retract,
    State,
    Switch,
    automorphisms,
    closure_targets,
    dual_replay,
    dual_step,
    genesis_history,
    min_responses,
    pair_orbits,
    response_valid,
    sealed_fixpoints,
    separated_pairs,
    state_key,
)
from derivation.candidates import (  # noqa: E402
    Bounds,
    NewForm,
    NewInst,
    NewRuleAll,
    iter_full_deltas,
)
from derivation.iso import rename  # noqa: E402
from derivation.model import Regime  # noqa: E402
from derivation.observe import collapsed_pairs, profiles  # noqa: E402

FROZEN_PROMPT = "a194961da50e2422bfe93a8ec907ddb2c791a022369e309df5f1dcdd12318d02"
FROZEN_PREDICTIONS = "b5e066fca1cc262dfbef84db142a647c36d055bd887c0bf2f48084d180424e97"
BOUNDS = Bounds(max_items=2, max_arity=2)


def _sha(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def _genesis(reading: str, n_forms: int, arity: int) -> Genesis:
    for g in sealed_fixpoints(BOUNDS):
        if g.reading == reading and len(g.regime.forms) == n_forms and g.regime.forms[0] == arity:
            return g
    raise AssertionError("no such genesis state")


class FreezeTests(unittest.TestCase):
    def test_prompt_is_frozen(self) -> None:
        self.assertEqual(_sha("PROMPT.md"), FROZEN_PROMPT)

    def test_predictions_are_frozen(self) -> None:
        self.assertEqual(_sha("PREDICTIONS.md"), FROZEN_PREDICTIONS)

    def test_prompt_states_no_number(self) -> None:
        """The challenge spells its bounds out; the only digits it may
        carry are the sealed measure names."""
        text = (HERE / "PROMPT.md").read_text(encoding="utf-8")
        body = re.sub(r"^## [0-9]+\.", "##", text.replace("mu1", "").replace("mu2", ""), flags=re.M)
        self.assertIsNone(re.search(r"[0-9]", body))

    def test_frozen_texts_are_lf(self) -> None:
        for name in ("PROMPT.md", "PREDICTIONS.md"):
            self.assertNotIn(b"\r", (HERE / name).read_bytes(), name)


class GenesisTests(unittest.TestCase):
    def test_every_genesis_is_a_certified_all_separated_fixpoint(self) -> None:
        states = sealed_fixpoints(BOUNDS)
        self.assertTrue(states)
        for g in states:
            self.assertEqual(dual_replay(tuple(g.history)).regime, g.regime, g.genesis_id)
            self.assertEqual(collapsed_pairs(g.regime), (), g.genesis_id)
            self.assertIn(g.reading, ("L", "F"))
            self.assertFalse(g.regime.rules, "sealed fixpoints carry no uniform rule")

    def test_genesis_ids_are_distinct_and_ordered(self) -> None:
        ids = [g.genesis_id for g in sealed_fixpoints(BOUNDS)]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))

    def test_reading_r_retracts_and_reading_p_keeps(self) -> None:
        g = _genesis("L", 1, 1)
        p = dual_replay(genesis_history(g, "P"))
        r = dual_replay(genesis_history(g, "R"))
        self.assertEqual(p.regime.reqs, g.regime.reqs)
        self.assertEqual(r.regime.reqs, frozenset())
        self.assertEqual(p.regime.insts, r.regime.insts)


class ValidityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.g = _genesis("L", 1, 1)  # two data, one unary form, one mark
        self.r_state = dual_replay(genesis_history(self.g, "R"))
        self.p_state = dual_replay(genesis_history(self.g, "P"))

    def test_single_instance_fills_the_difference(self) -> None:
        self.assertTrue(response_valid(self.r_state, (0, 1), (NewInst(0, (1,)),)))

    def test_single_rule_collapses_the_form(self) -> None:
        self.assertTrue(response_valid(self.r_state, (0, 1), (NewRuleAll(0),)))

    def test_fresh_form_alone_identifies_nothing(self) -> None:
        self.assertFalse(response_valid(self.r_state, (0, 1), (NewForm(1),)))

    def test_empty_response_is_not_valid_on_a_separated_pair(self) -> None:
        self.assertFalse(response_valid(self.r_state, (0, 1), ()))

    def test_required_separation_blocks_identification(self) -> None:
        for delta in iter_full_deltas(self.p_state.regime, 1, BOUNDS):
            self.assertFalse(response_valid(self.p_state, (0, 1), delta), delta)
        self.assertIsNone(min_responses(self.p_state, (0, 1), "mu1", BOUNDS))

    def test_minimum_in_reading_r_is_one_item(self) -> None:
        mr = min_responses(self.r_state, (0, 1), "mu1", BOUNDS)
        self.assertIsNotNone(mr)
        assert mr is not None
        self.assertEqual(mr.cost[0], 1)
        for delta in mr.deltas:
            self.assertEqual(len(delta), 1)

    def test_unpruned_enumeration_offers_rule_items(self) -> None:
        items = [d for d in iter_full_deltas(self.r_state.regime, 1, BOUNDS)]
        self.assertIn((NewRuleAll(0),), items)

    def test_validity_is_full_recomputation(self) -> None:
        """The check agrees with the definition applied by hand."""
        from derivation.candidates import apply_delta

        for delta in iter_full_deltas(self.r_state.regime, 2, BOUNDS):
            got = response_valid(self.r_state, (0, 1), delta)
            after = apply_delta(self.r_state.regime, delta)
            profs = profiles(after)
            want = profs[0] == profs[1]
            self.assertEqual(got, want, delta)


class IsomorphismTests(unittest.TestCase):
    def test_key_is_invariant_under_renaming(self) -> None:
        g = _genesis("F", 2, 1)  # three data, two unary forms
        s = dual_replay(genesis_history(g, "R"))
        s = dual_step(s, RequireSame(0, 1))
        pi = (2, 0, 1)
        phi = (1, 0)
        renamed = rename(s.regime, pi, phi)
        same = frozenset(
            (min(pi[i], pi[j]), max(pi[i], pi[j])) for (i, j) in s.same
        )
        t = State(renamed, same, s.mode)
        self.assertEqual(state_key(s), state_key(t))

    def test_key_separates_different_stores(self) -> None:
        g = _genesis("F", 2, 1)
        s = dual_replay(genesis_history(g, "R"))
        t = dual_step(s, RequireSame(0, 1))
        self.assertNotEqual(state_key(s), state_key(t))
        u = State(s.regime, s.same, SEPARATE)
        self.assertNotEqual(state_key(s), state_key(u))

    def test_orbits_are_equivariant(self) -> None:
        g = _genesis("F", 1, 2)  # three data, one binary form
        s = dual_replay(genesis_history(g, "R"))
        pi = (1, 2, 0)
        t = State(rename(s.regime, pi, (0,)), frozenset(), s.mode)
        orbits_s = pair_orbits(s, separated_pairs(s.regime))
        orbits_t = pair_orbits(t, separated_pairs(t.regime))
        mapped = {
            frozenset((min(pi[i], pi[j]), max(pi[i], pi[j])) for (i, j) in orbit)
            for orbit in orbits_s
        }
        self.assertEqual(mapped, {frozenset(orbit) for orbit in orbits_t})

    def test_identity_is_an_automorphism(self) -> None:
        g = _genesis("L", 1, 2)
        s = dual_replay(genesis_history(g, "R"))
        ident = (tuple(range(s.regime.n_data())), tuple(range(len(s.regime.forms))))
        self.assertIn(ident, automorphisms(s))


class EventTests(unittest.TestCase):
    def test_switch_retracts_both_stores_and_flips(self) -> None:
        g = _genesis("L", 1, 1)
        s = dual_replay(genesis_history(g, "P"))
        s = State(s.regime, frozenset({(0, 1)}), IDENTIFY)
        t = dual_step(s, Switch())
        self.assertEqual(t.regime.reqs, frozenset())
        self.assertEqual(t.same, frozenset())
        self.assertEqual(t.mode, SEPARATE)
        self.assertEqual(dual_step(t, Switch()).mode, IDENTIFY)

    def test_retract_keeps_the_regime_structure(self) -> None:
        g = _genesis("L", 1, 1)
        s = dual_replay(genesis_history(g, "P"))
        t = dual_step(s, Retract())
        self.assertEqual(
            (t.regime.data, t.regime.forms, t.regime.insts, t.regime.rules),
            (s.regime.data, s.regime.forms, s.regime.insts, s.regime.rules),
        )

    def test_require_same_out_of_range_is_refused(self) -> None:
        from derivation.model import AdmissionError

        g = _genesis("L", 1, 1)
        s = dual_replay(genesis_history(g, "R"))
        with self.assertRaises(AdmissionError):
            dual_step(s, RequireSame(0, 5))

    def test_closure_targets_empty_exactly_at_fixpoint(self) -> None:
        collapsed = State(Regime(("x", "y"), (1,), frozenset(), frozenset(), frozenset()), frozenset(), IDENTIFY)
        self.assertEqual(closure_targets(collapsed), ())
        separated = State(Regime(("x", "y"), (1,), frozenset({(0, (0,))}), frozenset(), frozenset()), frozenset(), IDENTIFY)
        self.assertEqual(closure_targets(separated), ((0, 1),))


class ReceiptTests(unittest.TestCase):
    def test_receipts_regenerate_identically(self) -> None:
        """The summary regenerates byte-for-byte; the full export
        regenerates content-for-content, and its recorded sha256 matches.
        Compressed bytes are not compared: the sealed gate tolerates a
        different compressor producing the same content, and so does this."""
        from run_dual import build_all, split

        sys.path.insert(0, str(HERE.parents[1] / "code"))
        from derivation.export import dumps_deterministic, read_json_gz

        committed = (HERE / "receipts" / "identification_dual.json").read_bytes()
        self.assertNotIn(b"\r", committed)
        summary, full = split(build_all())
        self.assertEqual(dumps_deterministic(summary), committed)
        stored = read_json_gz(HERE / "receipts" / "full" / "identification_dual_full.json.gz")
        self.assertEqual(stored, full)
        recorded = summary["full_export"]
        assert isinstance(recorded, dict)
        self.assertEqual(
            hashlib.sha256(dumps_deterministic(full)).hexdigest(),
            recorded["sha256_uncompressed"],
        )

    def test_receipt_records_the_frozen_hashes(self) -> None:
        import json

        payload = json.loads((HERE / "receipts" / "identification_dual.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["prompt_sha256"], FROZEN_PROMPT)
        self.assertEqual(payload["predictions_sha256"], FROZEN_PREDICTIONS)
        self.assertEqual(payload["authority_effect"], "None")
        self.assertEqual(sorted(payload["predictions_scored"]), sorted(f"P{i}" for i in range(1, 11)))


if __name__ == "__main__":
    unittest.main()
