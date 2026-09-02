from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA = "proof-symbol-packet-v1"
KINDS = frozenset(
    {
        "hypothesis",
        "construction",
        "theorem",
        "computation",
        "countermodel",
        "bridge",
        "terminal",
    }
)
STATUSES = frozenset(
    {"candidate", "survives", "proved", "computed", "conditional", "refuted", "open"}
)
LIST_FIELDS = (
    "source_revisions",
    "write_boundary",
    "toolchains",
    "allowed_axioms",
    "consumers",
    "mutation_specs",
    "parents",
    "premises",
    "foundations",
    "imports",
    "new_primitives",
    "obligations",
    "falsifiers",
)
EVIDENCE_FIELDS = ("lean", "python", "receipts")


class PacketError(ValueError):
    pass


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PacketError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def string_list(packet_id: str, packet: dict[str, Any], field: str) -> list[str]:
    value = packet.get(field)
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise PacketError(f"{packet_id}: {field} must be a list of nonempty strings")
    return value


def evidence(packet_id: str, packet: dict[str, Any]) -> dict[str, list[str]]:
    raw = packet.get("evidence")
    if not isinstance(raw, dict) or set(raw) != set(EVIDENCE_FIELDS):
        raise PacketError(
            f"{packet_id}: evidence keys must be {sorted(EVIDENCE_FIELDS)}"
        )
    return {field: string_list(packet_id, raw, field) for field in EVIDENCE_FIELDS}


def validate_packet(packet: dict[str, Any]) -> None:
    packet_id = packet.get("id")
    if not isinstance(packet_id, str) or not packet_id:
        raise PacketError("packet id must be a nonempty string")
    if packet.get("schema") != SCHEMA:
        raise PacketError(f"{packet_id}: schema must be {SCHEMA}")
    for field in ("goal", "claim", "owner", "residual"):
        if not isinstance(packet.get(field), str):
            raise PacketError(f"{packet_id}: {field} must be a string")
    level = packet.get("level")
    if not isinstance(level, int) or isinstance(level, bool) or level < 0:
        raise PacketError(f"{packet_id}: level must be a nonnegative integer")
    kind = packet.get("kind")
    status = packet.get("status")
    if kind not in KINDS:
        raise PacketError(f"{packet_id}: unknown kind {kind!r}")
    if status not in STATUSES:
        raise PacketError(f"{packet_id}: unknown status {status!r}")
    lists = {field: string_list(packet_id, packet, field) for field in LIST_FIELDS}
    proof = evidence(packet_id, packet)
    sparse_cost = packet.get("l1")
    expected_cost = sum(len(lists[field]) for field in ("imports", "new_primitives", "obligations"))
    if sparse_cost != expected_cost:
        raise PacketError(
            f"{packet_id}: l1 is {sparse_cost!r}, expected {expected_cost}"
        )
    if status == "proved" and (lists["imports"] or not proof["lean"]):
        raise PacketError(f"{packet_id}: proved requires Lean evidence and no imports")
    if status == "computed" and (not proof["python"] or not proof["receipts"]):
        raise PacketError(f"{packet_id}: computed requires Python evidence and a receipt")
    if status == "conditional" and (not lists["imports"] or not proof["lean"]):
        raise PacketError(f"{packet_id}: conditional requires imports and Lean evidence")
    if status == "refuted" and (
        not lists["falsifiers"] or not any(proof.values())
    ):
        raise PacketError(f"{packet_id}: refuted requires a falsifier and evidence")
    if status == "open" and not packet["residual"]:
        raise PacketError(f"{packet_id}: open requires a residual")


def load_packets(path: Path) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line, object_pairs_hook=strict_object)
        except (json.JSONDecodeError, PacketError) as exc:
            raise PacketError(f"line {line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise PacketError(f"line {line_number}: packet must be a JSON object")
        validate_packet(value)
        packets.append(value)
    if not packets:
        raise PacketError("packet stream is empty")
    return packets


def validate_graph(packets: list[dict[str, Any]]) -> None:
    by_id: dict[str, dict[str, Any]] = {}
    for packet in packets:
        packet_id = str(packet["id"])
        if packet_id in by_id:
            raise PacketError(f"duplicate packet id: {packet_id}")
        by_id[packet_id] = packet
    for packet in packets:
        for parent_id in packet["parents"]:
            parent = by_id.get(parent_id)
            if parent is None:
                raise PacketError(f"{packet['id']}: missing parent {parent_id}")
            if parent["level"] >= packet["level"]:
                raise PacketError(
                    f"{packet['id']}: parent {parent_id} is not at a lower level"
                )
    roots = [packet for packet in packets if packet["level"] == 0]
    if len(roots) != 1 or roots[0]["kind"] != "hypothesis" or roots[0]["parents"]:
        raise PacketError(
            "packet stream must have one parentless level-zero hypothesis manifest"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packets", type=Path)
    args = parser.parse_args()
    try:
        packets = load_packets(args.packets)
        validate_graph(packets)
    except (OSError, PacketError) as exc:
        print(f"FAIL: {exc}")
        return 1
    statuses: dict[str, int] = {}
    for packet in packets:
        status = str(packet["status"])
        statuses[status] = statuses.get(status, 0) + 1
    print(
        f"packet stream clean: {len(packets)} packets; "
        + ", ".join(f"{key}={statuses[key]}" for key in sorted(statuses))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
