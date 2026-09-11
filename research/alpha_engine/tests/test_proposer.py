"""Proposer hole: Deltas only; selector occupancy is refused."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import NewForm  # noqa: E402
from derivation.engine import READING_L  # noqa: E402
from derivation.model import AdmitDatum, replay  # noqa: E402

from harness import Node  # noqa: E402
from proposer import OfferingError, SelectorOccupancyError, occupy  # noqa: E402


class EmptyProposer:
    def offerings(self, node: Node) -> tuple[object, ...]:
        del node
        return ()


class DeltaProposer:
    def offerings(self, node: Node) -> tuple[object, ...]:
        del node
        return ((NewForm(1),),)


class EmitProposer:
    def offerings(self, node: Node) -> tuple[object, ...]:
        del node
        return ()

    def emit(self) -> object:
        return None


class MaterializeProposer:
    def offerings(self, node: Node) -> tuple[object, ...]:
        del node
        return ()

    def materialize(self) -> object:
        return None


class HostDemandProposer:
    def offerings(self, node: Node) -> tuple[object, ...]:
        del node
        return ()

    def host_next_demand(self) -> object:
        return None


class EventProposer:
    def offerings(self, node: Node) -> tuple[object, ...]:
        del node
        return (AdmitDatum("x"),)


class ListProposer:
    def offerings(self, node: Node) -> tuple[object, ...]:
        del node
        return ["not-a-tuple"]  # type: ignore[return-value]


class ProposerTests(unittest.TestCase):
    def setUp(self) -> None:
        regime = replay(READING_L.genesis)
        self.node = Node(history=READING_L.genesis, regime=regime)

    def test_empty_offerings_are_a_proposal(self) -> None:
        proposal = occupy(EmptyProposer(), self.node)
        self.assertEqual(proposal.offerings, ())
        self.assertEqual(self.node.regime, replay(READING_L.genesis))

    def test_delta_offerings_are_accepted(self) -> None:
        proposal = occupy(DeltaProposer(), self.node)
        self.assertEqual(proposal.offerings, ((NewForm(1),),))

    def test_emit_occupancy_is_refused(self) -> None:
        with self.assertRaises(SelectorOccupancyError):
            occupy(EmitProposer(), self.node)

    def test_materialize_occupancy_is_refused(self) -> None:
        with self.assertRaises(SelectorOccupancyError):
            occupy(MaterializeProposer(), self.node)

    def test_host_next_demand_occupancy_is_refused(self) -> None:
        with self.assertRaises(SelectorOccupancyError):
            occupy(HostDemandProposer(), self.node)

    def test_event_offering_is_refused(self) -> None:
        with self.assertRaises(OfferingError):
            occupy(EventProposer(), self.node)

    def test_non_tuple_offerings_are_refused(self) -> None:
        with self.assertRaises(OfferingError):
            occupy(ListProposer(), self.node)

    def test_proposer_source_does_not_import_partial_decide(self) -> None:
        text = (
            Path(__file__).resolve().parents[1] / "proposer.py"
        ).read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                self.assertNotIn("partial_decide", stripped)
                self.assertNotIn("instance_demand", stripped)


if __name__ == "__main__":
    unittest.main()
