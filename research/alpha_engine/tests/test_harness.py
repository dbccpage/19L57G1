"""Harness constructors, refusals, and Supply-shaped proposal."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds, NewForm  # noqa: E402
from derivation.engine import READING_L  # noqa: E402
from derivation.model import AdmitDatum, Supply, replay  # noqa: E402

from harness import (  # noqa: E402
    EvalResult,
    License,
    LicenseIsNotEventError,
    Node,
    PresentAsAdmitError,
    Proposal,
    RetainedClass,
    SeventhEventError,
    append_sealed_event,
    as_admit,
    as_event,
    jsonable,
    leftover_as_demand,
    LeftoverIsNotDemandError,
    make_license,
    present,
)


_NODE = Node(
    history=READING_L.genesis, regime=replay(READING_L.genesis), license=None
)


@dataclass(frozen=True)
class ExtraEvent:
    token: str


class HarnessTests(unittest.TestCase):
    def test_present_does_not_change_the_regime(self) -> None:
        regime = replay(READING_L.genesis)
        proposal = Proposal(token="offer", offerings=())
        self.assertEqual(present(regime, proposal), regime)

    def test_present_as_admit_is_refused(self) -> None:
        with self.assertRaises(PresentAsAdmitError):
            as_admit(Proposal(token="offer"))

    def test_license_is_not_an_event(self) -> None:
        license = make_license(
            granter="g", scope="s", authorized=(),
            source=_NODE, target=READING_L.target, measure="mu1",
            bounds=Bounds(2, 2),
        )
        with self.assertRaises(LicenseIsNotEventError):
            as_event(license)
        self.assertNotIsInstance(license, Supply)
        self.assertNotIsInstance(license, AdmitDatum)
        self.assertFalse(hasattr(License, "revoke"))
        # 2026-09-25: the three authorization fields plus the four binding
        # fields of the declaration.  Still no integer selector field.
        self.assertEqual(
            tuple(License.__dataclass_fields__),
            (
                "granter",
                "scope",
                "authorized",
                "source",
                "target",
                "measure",
                "bounds",
            ),
        )
        self.assertNotIn("index", License.__dataclass_fields__)

    def test_seventh_event_is_refused(self) -> None:
        with self.assertRaises(SeventhEventError):
            append_sealed_event((), ExtraEvent("x"))
        out = append_sealed_event((), Supply("<>"))
        self.assertEqual(out, (Supply("<>"),))

    def test_leftover_pairs_are_not_demand(self) -> None:
        with self.assertRaises(LeftoverIsNotDemandError):
            leftover_as_demand(((0, 1),))

    def test_jsonable_and_refusals(self) -> None:
        self.assertEqual(jsonable((1, (2,))), [1, [2]])
        self.assertEqual(jsonable("a"), "a")
        with self.assertRaises(TypeError):
            jsonable(True)
        with self.assertRaises(TypeError):
            jsonable([1])

    def test_retained_class_must_be_inhabited(self) -> None:
        key = (0, (), (), (), ())
        with self.assertRaises(ValueError):
            RetainedClass(key, ())
        delta = (NewForm(1),)
        with self.assertRaises(ValueError):
            RetainedClass(key, (delta, delta))

    def test_eval_result_guards(self) -> None:
        key = (0, (), (), (), ())
        delta = (NewForm(1),)
        item = RetainedClass(key, (delta,))
        with self.assertRaises(ValueError):
            EvalResult("mu3", (1, -1), (delta,), (item,), True, 2, 2)
        with self.assertRaises(ValueError):
            EvalResult("mu1", (1, -1), (delta,), (), True, 2, 2)
        with self.assertRaises(ValueError):
            EvalResult("mu1", None, (delta,), (item,), True, 2, 2)
        with self.assertRaises(ValueError):
            EvalResult("mu1", None, (), (item,), False, 2, 2)
        with self.assertRaises(ValueError):
            EvalResult("mu1", None, (), (), False, -1, 2)
        other = (1, (), (), (), ())
        with self.assertRaises(ValueError):
            EvalResult(
                "mu1",
                (1, -1),
                (delta, delta),
                (RetainedClass(other, (delta,)), item),
                True,
                2,
                2,
            )
        with self.assertRaises(ValueError):
            EvalResult(
                "mu1",
                (1, -1),
                (delta, delta),
                (item, RetainedClass(key, (delta,))),
                True,
                2,
                2,
            )

    def test_license_key_order(self) -> None:
        a = (0, (), (), (), ())
        b = (1, (), (), (), ())
        with self.assertRaises(ValueError):
            License(
                granter="g", scope="s", authorized=(b, a),
                source="0" * 64, target=(0, 1), measure="mu1",
                bounds=Bounds(2, 2),
            )
        with self.assertRaises(ValueError):
            License(
                granter="g", scope="s", authorized=(a, a),
                source="0" * 64, target=(0, 1), measure="mu1",
                bounds=Bounds(2, 2),
            )
        license = make_license(
            granter="g", scope="s", authorized=(a, b),
            source=_NODE, target=READING_L.target, measure="mu1",
            bounds=Bounds(2, 2),
        )
        self.assertEqual(license.authorized, (a, b))

    def test_node_optional_license(self) -> None:
        regime = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=regime)
        self.assertIsNone(node.license)


if __name__ == "__main__":
    unittest.main()
