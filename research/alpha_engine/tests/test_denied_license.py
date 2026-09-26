"""A denied License writes no node.license; integer selectors are refused."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import READING_L  # noqa: E402
from derivation.model import replay  # noqa: E402

from driver_a import apply_licensed, explore  # noqa: E402
from evaluate import evaluate  # noqa: E402
from harness import (  # noqa: E402
    LicenseSelectorError,
    Node,
    key_by_index,
    make_license,
)
from search_policy import record_census  # noqa: E402

_NODE = Node(
    history=READING_L.genesis, regime=replay(READING_L.genesis), license=None
)


class DeniedLicense(unittest.TestCase):
    def test_denied_license_writes_no_node_license(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        key = result.retained[0].key
        denied = make_license(
            granter="test", scope="denied", authorized=(),
            source=node, target=READING_L.target, measure="mu1", bounds=Bounds(2, 2),
        )
        out = apply_licensed(node, result, denied, key, READING_L.target)
        self.assertIsNone(out)
        self.assertIsNone(node.license)
        self.assertEqual(node.regime, base)

    def test_unlicensed_explore_of_a_retained_key_is_refused(self) -> None:
        from driver_a import UnlicensedExploreError

        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        keys = tuple(item.key for item in result.retained)
        census = record_census(keys, (keys[0],), (), keys[1:])
        denied = make_license(
            granter="test", scope="denied", authorized=(),
            source=node, target=READING_L.target, measure="mu1", bounds=Bounds(2, 2),
        )
        with self.assertRaises(UnlicensedExploreError):
            explore(node, result, denied, census, READING_L.target)
        self.assertIsNone(node.license)

    def test_integer_index_kwarg_is_refused(self) -> None:
        with self.assertRaises(LicenseSelectorError):
            make_license(
                granter="test",
                scope="c3",
                authorized=(),
                source=_NODE,
                target=READING_L.target,
                measure="mu1",
                bounds=Bounds(2, 2),
                index=0,
            )
        with self.assertRaises(LicenseSelectorError):
            make_license(
                granter="test",
                scope="c3",
                authorized=(),
                source=_NODE,
                target=READING_L.target,
                measure="mu1",
                bounds=Bounds(2, 2),
                index=1,
            )
        with self.assertRaises(LicenseSelectorError):
            make_license(
                granter="test",
                scope="c3",
                authorized=(),
                source=_NODE,
                target=READING_L.target,
                measure="mu1",
                bounds=Bounds(2, 2),
                index=-1,
            )

    def test_integer_index_is_not_a_tied_class_selector(self) -> None:
        with self.assertRaises(LicenseSelectorError):
            key_by_index((), 0)
        with self.assertRaises(LicenseSelectorError):
            key_by_index((), 2)

    def test_unknown_license_field_is_refused(self) -> None:
        with self.assertRaises(LicenseSelectorError):
            make_license(
                granter="test",
                scope="c3",
                authorized=(),
                source=_NODE,
                target=READING_L.target,
                measure="mu1",
                bounds=Bounds(2, 2),
                score=1,
            )


if __name__ == "__main__":
    unittest.main()
