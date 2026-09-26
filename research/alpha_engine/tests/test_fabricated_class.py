"""A class key absent from the sealed quotient is refused."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import READING_L  # noqa: E402
from derivation.iso import CanonKey  # noqa: E402
from derivation.model import replay  # noqa: E402

from evaluate import evaluate, fresh_retained_keys  # noqa: E402
from harness import EvalResult, Node, RetainedClass, make_license  # noqa: E402
from search_policy import FabricatedClassError, record_census  # noqa: E402
from driver_a import apply_licensed, representative_delta  # noqa: E402


def _fake_key() -> CanonKey:
    return (999, (), (), (), ())


class FabricatedClass(unittest.TestCase):
    def test_census_refuses_a_key_absent_from_the_quotient(self) -> None:
        base = replay(READING_L.genesis)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        retained = tuple(item.key for item in result.retained)
        fake = _fake_key()
        self.assertNotIn(fake, retained)
        with self.assertRaises(FabricatedClassError):
            record_census(retained, (fake,), (), retained)

    def test_apply_licensed_refuses_a_fabricated_authorized_key(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        fake = _fake_key()
        license = make_license(
            granter="test",
            scope="fabricated",
            authorized=(fake,),
            source=node, target=READING_L.target, measure="mu1", bounds=Bounds(2, 2),
        )
        with self.assertRaises(FabricatedClassError):
            apply_licensed(node, result, license, fake, READING_L.target)

    def test_apply_licensed_refuses_a_license_with_an_extra_key(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        valid = result.retained[0].key
        fake = _fake_key()
        license = make_license(
            granter="test",
            scope="fabricated",
            authorized=tuple(sorted((valid, fake))),
            source=node, target=READING_L.target, measure="mu1", bounds=Bounds(2, 2),
        )
        with self.assertRaises(FabricatedClassError):
            apply_licensed(
                node, result, license, valid, READING_L.target
            )
        self.assertIsNone(node.license)
        self.assertEqual(node.regime, base)

    def test_representative_delta_refuses_a_fabricated_key(self) -> None:
        base = replay(READING_L.genesis)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        with self.assertRaises(FabricatedClassError):
            representative_delta(result, _fake_key())

    def test_explore_refuses_a_license_with_an_extra_key(self) -> None:
        from driver_a import explore
        from search_policy import record_census

        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        keys = tuple(item.key for item in result.retained)
        fake = _fake_key()
        census = record_census(keys, (), (), keys)
        license = make_license(
            granter="test",
            scope="fabricated",
            authorized=tuple(sorted(keys + (fake,))),
            source=node, target=READING_L.target, measure="mu1", bounds=Bounds(2, 2),
        )
        with self.assertRaises(FabricatedClassError):
            explore(node, result, license, census, READING_L.target)

    def test_forged_eval_result_is_checked_against_a_fresh_quotient(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        genuine = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        sealed = fresh_retained_keys(
            base, READING_L.target, "mu1", Bounds(2, 2)
        )
        fake = _fake_key()
        self.assertNotIn(fake, sealed)
        forged_members = genuine.retained[0].members
        forged = EvalResult(
            measure=genuine.measure,
            cost=genuine.cost,
            raw_minima=genuine.raw_minima,
            retained=tuple(
                sorted(
                    genuine.retained + (RetainedClass(fake, forged_members),),
                    key=lambda item: item.key,
                )
            ),
            found=True,
            max_items=genuine.max_items,
            max_arity=genuine.max_arity,
        )
        license = make_license(
            granter="test",
            scope="forged",
            authorized=tuple(sorted((genuine.retained[0].key, fake))),
            source=node, target=READING_L.target, measure="mu1", bounds=Bounds(2, 2),
        )
        with self.assertRaises(FabricatedClassError):
            apply_licensed(
                node, forged, license, fake, READING_L.target
            )
        with self.assertRaises(FabricatedClassError):
            apply_licensed(
                node, forged, license, genuine.retained[0].key, READING_L.target
            )


if __name__ == "__main__":
    unittest.main()
