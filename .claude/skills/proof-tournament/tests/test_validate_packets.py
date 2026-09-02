from __future__ import annotations

import copy
import sys
from pathlib import Path
import unittest


SCRIPT_ROOT = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

import validate_packets as subject  # noqa: E402


def packet(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema": subject.SCHEMA,
        "id": "P0",
        "goal": "G0",
        "source_revisions": ["repo@sha:path#blob"],
        "write_boundary": ["research/run/"],
        "toolchains": ["leanprover/lean4:v4.33.0"],
        "allowed_axioms": ["propext", "Quot.sound"],
        "owner": "cell-0",
        "consumers": [],
        "mutation_specs": [],
        "level": 0,
        "parents": [],
        "kind": "theorem",
        "claim": "T : Prop",
        "premises": [],
        "foundations": ["Std"],
        "imports": [],
        "new_primitives": [],
        "obligations": [],
        "falsifiers": [],
        "evidence": {"lean": ["T"], "python": [], "receipts": []},
        "status": "proved",
        "residual": "",
        "l1": 0,
    }
    value.update(changes)
    return value


class PacketValidationTests(unittest.TestCase):
    def test_proved_packet_and_graph_are_valid(self) -> None:
        root = packet(kind="hypothesis", status="survives")
        child = packet(id="P1", level=1, parents=["P0"])
        subject.validate_packet(root)
        subject.validate_packet(child)
        subject.validate_graph([root, child])

    def test_proved_packet_cannot_hide_an_import(self) -> None:
        value = packet(imports=["I0"], l1=1)
        with self.assertRaisesRegex(subject.PacketError, "proved requires"):
            subject.validate_packet(value)

    def test_conditional_packet_requires_lean_and_import(self) -> None:
        value = packet(status="conditional", imports=["I0"], l1=1)
        subject.validate_packet(value)
        missing = copy.deepcopy(value)
        missing["evidence"] = {"lean": [], "python": [], "receipts": []}
        with self.assertRaisesRegex(subject.PacketError, "conditional requires"):
            subject.validate_packet(missing)

    def test_refuted_packet_requires_falsifier(self) -> None:
        value = packet(status="refuted")
        with self.assertRaisesRegex(subject.PacketError, "refuted requires"):
            subject.validate_packet(value)

    def test_sparse_cost_is_recomputed(self) -> None:
        value = packet(obligations=["O0"], l1=0)
        with self.assertRaisesRegex(subject.PacketError, "expected 1"):
            subject.validate_packet(value)

    def test_sparse_cost_rejects_bool(self) -> None:
        value = packet(l1=False)
        with self.assertRaisesRegex(subject.PacketError, "nonnegative integer"):
            subject.validate_packet(value)

    def test_proved_packet_cannot_retain_an_obligation(self) -> None:
        value = packet(obligations=["O0"], l1=1)
        with self.assertRaisesRegex(subject.PacketError, "no obligations"):
            subject.validate_packet(value)

    def test_graph_rejects_missing_or_same_level_parent(self) -> None:
        root = packet(kind="hypothesis", status="survives")
        missing = packet(id="P1", level=1, parents=["absent"])
        with self.assertRaisesRegex(subject.PacketError, "missing parent"):
            subject.validate_graph([root, missing])
        same = packet(id="P1", level=0, parents=["P0"])
        with self.assertRaisesRegex(subject.PacketError, "not at a lower level"):
            subject.validate_graph([root, same])

    def test_graph_rejects_disconnected_non_root_packet(self) -> None:
        root = packet(kind="hypothesis", status="survives")
        orphan = packet(id="P1", level=1, parents=[])
        with self.assertRaisesRegex(subject.PacketError, "must have a parent"):
            subject.validate_graph([root, orphan])

    def test_proved_terminal_rejects_imported_ancestor(self) -> None:
        root = packet(kind="hypothesis", status="survives")
        conditional = packet(
            id="P1",
            level=1,
            parents=["P0"],
            status="conditional",
            imports=["I0"],
            l1=1,
        )
        terminal = packet(
            id="P2",
            level=2,
            parents=["P1"],
            kind="terminal",
        )
        with self.assertRaisesRegex(subject.PacketError, "imported ancestor P1"):
            subject.validate_graph([root, conditional, terminal])


if __name__ == "__main__":
    unittest.main()
