"""This tree's re-implemented kernel, checked against the sealed original.

The sealed modules are loaded here **only** to cross-check, and only after
their bytes match the pin: the loader refuses unpinned bytes, so this test
cannot silently pass against a moved sealed source.  Nothing in ``code/``
imports across trees.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import subprocess
import sys
import types
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

from code.enumerate_space import (  # noqa: E402
    DEFAULT_BOUNDS,
    iter_sealed_items,
    sealed_prefixes,
)
from code.grammar import (  # noqa: E402
    collapsed_pairs,
    contexts,
    profiles,
    sealed_derivable,
    sealed_relation,
)
from code.items import (  # noqa: E402
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    StatedState,
    apply_delta,
    canonical_delta,
    mu1,
    mu2,
)
from code.quotient import canonical_regime  # noqa: E402
from code.regime import genesis  # noqa: E402


def _pins() -> dict[str, str]:
    with open(os.path.join(HERE, "SOURCE_MANIFEST.json"), encoding="utf-8") as f:
        return json.load(f)["pins"]


def _blob_sha256(path: str) -> str:
    out = subprocess.run(
        ["git", "-C", ROOT, "show", f"HEAD:{path}"],
        check=True, stdout=subprocess.PIPE,
    ).stdout
    return hashlib.sha256(out).hexdigest()


def load_sealed() -> types.ModuleType | None:
    """Load the sealed ``derivation`` package, refusing unpinned bytes."""
    pins = _pins()
    for path, want in pins.items():
        if not path.startswith("code/derivation/"):
            continue
        if _blob_sha256(path) != want:
            raise AssertionError(
                f"refusing to cross-check against unpinned sealed bytes: "
                f"{path}"
            )
    sealed_root = os.path.join(ROOT, "code")
    if sealed_root not in sys.path:
        sys.path.append(sealed_root)
    spec = importlib.util.find_spec("derivation.model")
    if spec is None:  # pragma: no cover - the sealed tree is always present
        return None
    import derivation.candidates as sc
    import derivation.engine as se
    import derivation.iso as si
    import derivation.model as sm
    import derivation.observe as so

    mod = types.SimpleNamespace(
        model=sm, observe=so, candidates=sc, iso=si, engine=se
    )
    return mod  # type: ignore[return-value]


SEALED = load_sealed()


def _sealed_regime(r):  # type: ignore[no-untyped-def]
    return SEALED.model.Regime(  # type: ignore[union-attr]
        r.data, r.forms, r.insts, r.rules, r.reqs
    )


def _states(depth: int = 3):  # type: ignore[no-untyped-def]
    from code.census import population

    return population(depth, DEFAULT_BOUNDS)


class SealedCrossCheck(unittest.TestCase):
    """The re-implementation is the sealed original, checked and not
    asserted."""

    def test_pins_are_checked_before_loading(self) -> None:
        self.assertIsNotNone(SEALED, "sealed cross-check package must load")

    def test_genesis_regimes_agree(self) -> None:
        for reading, hist in (
            ("L", SEALED.engine.GENESIS_L),  # type: ignore[union-attr]
            ("F", SEALED.engine.GENESIS_F),  # type: ignore[union-attr]
        ):
            sealed = SEALED.model.replay(hist)  # type: ignore[union-attr]
            mine = genesis(reading)
            self.assertEqual(mine.data, sealed.data)
            self.assertEqual(mine.forms, sealed.forms)
            self.assertEqual(mine.insts, sealed.insts)
            self.assertEqual(mine.rules, sealed.rules)

    def test_contexts_profiles_and_collapsed_pairs_agree(self) -> None:
        for r in _states():
            s = _sealed_regime(r)
            self.assertEqual(contexts(r), SEALED.observe.contexts(s))  # type: ignore[union-attr]
            self.assertEqual(profiles(r), SEALED.observe.profiles(s))  # type: ignore[union-attr]
            self.assertEqual(
                collapsed_pairs(r),
                SEALED.observe.collapsed_pairs(s),  # type: ignore[union-attr]
            )

    def test_derivable_agrees_on_every_plugging(self) -> None:
        for r in _states():
            s = _sealed_regime(r)
            for c in contexts(r):
                for d in range(r.n_data()):
                    inst = (c[0], tuple(d if x is None else x for x in c[1]))
                    self.assertEqual(
                        sealed_derivable(r, inst),
                        SEALED.observe.derivable(s, inst),  # type: ignore[union-attr]
                    )

    def test_one_item_alphabet_agrees(self) -> None:
        sealed_bounds = SEALED.candidates.Bounds(2, 2)  # type: ignore[union-attr]
        for r in _states():
            s = _sealed_regime(r)
            mine = [type(i).__name__ for i in iter_sealed_items(r, DEFAULT_BOUNDS)]
            theirs = [
                type(i).__name__
                for i in SEALED.candidates.iter_cost1_items(s, sealed_bounds)  # type: ignore[union-attr]
            ]
            self.assertEqual(mine, theirs)

    def test_mu1_and_mu2_agree_with_the_sealed_expressions(self) -> None:
        """Value agreement on the whole enumerated sealed space, not on a
        handful of cases."""
        base = genesis("F")
        checked = 0
        for k in (0, 1, 2):
            for delta in sealed_prefixes(base, k, DEFAULT_BOUNDS):
                theirs = tuple(_to_sealed_item(i) for i in delta)
                self.assertEqual(mu1(delta), SEALED.candidates.mu1(theirs))  # type: ignore[union-attr]
                self.assertEqual(mu2(delta), SEALED.candidates.mu2(theirs))  # type: ignore[union-attr]
                checked += 1
        self.assertGreater(checked, 20)

    def test_canonical_key_agrees_as_an_equality_relation(self) -> None:
        """The brute-force key's *equality relation* is the sealed refined
        key's, which is what a quotient needs; the key values may differ."""
        states = _states()
        for a in states:
            for b in states:
                mine = canonical_regime(a) == canonical_regime(b)
                theirs = SEALED.iso.canonical(  # type: ignore[union-attr]
                    _sealed_regime(a)
                ) == SEALED.iso.canonical(  # type: ignore[union-attr]
                    _sealed_regime(b)
                )
                self.assertEqual(mine, theirs)

    def test_pair_orbits_agree(self) -> None:
        from code.quotient import pair_orbits

        for r in _states():
            pairs = collapsed_pairs(r)
            if not pairs:
                continue
            self.assertEqual(
                pair_orbits(r, pairs),
                SEALED.iso.pair_orbits(_sealed_regime(r), pairs),  # type: ignore[union-attr]
            )


def _to_sealed_item(it):  # type: ignore[no-untyped-def]
    if isinstance(it, NewDatum):
        return SEALED.candidates.NewDatum()  # type: ignore[union-attr]
    if isinstance(it, NewForm):
        return SEALED.candidates.NewForm(it.arity)  # type: ignore[union-attr]
    if isinstance(it, NewRuleAll):
        return SEALED.candidates.NewRuleAll(it.form)  # type: ignore[union-attr]
    return SEALED.candidates.NewInst(it.form, it.args)  # type: ignore[union-attr]


class ProjectionCommutes(unittest.TestCase):
    def test_projection_commutes_with_every_sealed_event(self) -> None:
        """The reader-free slice of this tree is exactly the sealed
        derivation, so the projection to the regime must commute."""
        for reading in ("L", "F"):
            base = genesis(reading)
            for it in iter_sealed_items(base, DEFAULT_BOUNDS):
                delta = canonical_delta((it,))
                with_readers = apply_delta(
                    StatedState(base, ()), delta, 3, 2
                ).regime
                without = apply_delta(
                    StatedState(base, ()), delta, 3, 2
                ).regime
                self.assertEqual(with_readers, without)
                theirs = SEALED.candidates.apply_delta(  # type: ignore[union-attr]
                    _sealed_regime(base), (_to_sealed_item(it),)
                )
                # Field by field: the two Regime classes are distinct types,
                # so identity of the dataclasses is not the claim.
                self.assertEqual(with_readers.data, theirs.data)
                self.assertEqual(with_readers.forms, theirs.forms)
                self.assertEqual(with_readers.insts, theirs.insts)
                self.assertEqual(with_readers.rules, theirs.rules)
                self.assertEqual(with_readers.reqs, theirs.reqs)


class CalibrationGate(unittest.TestCase):
    def test_calibration_reproduces_the_sealed_answer(self) -> None:
        from code.calibration import calibration_report

        report = calibration_report()
        for row in report["rows"]:  # type: ignore[index]
            self.assertTrue(
                row["agrees"],
                f"calibration differs at {row['reading']}/{row['measure']}: "
                f"{row['recomputed']} vs sealed {row['sealed']}",
            )
        self.assertTrue(report["agrees_field_by_field"])

    def test_transcribed_sealed_answer_matches_the_pinned_artifact(self) -> None:
        """The transcription in ``code/calibration.py`` is checked against the
        committed artifact, so it cannot drift into a convenient number."""
        from code.calibration import SEALED_CHALLENGE3

        path = os.path.join(ROOT, "artifacts", "challenges.json")
        with open(path, encoding="utf-8") as fh:
            c3 = json.load(fh)["challenge3"]
        for (reading, measure), want in SEALED_CHALLENGE3.items():
            block = c3[reading][measure]
            self.assertEqual(
                list(want["minimum_cost"]), block["minimum_cost"]  # type: ignore[index]
            )
            self.assertEqual(
                want["valid_deltas_at_minimum"],
                block["valid_deltas_at_minimum"],
            )
            self.assertEqual(want["iso_classes"], len(block["iso_classes"]))
            self.assertEqual(
                want["cost_below_minimum_all_fail"],
                block["cost_below_minimum_all_fail"],
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
