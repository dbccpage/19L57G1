"""Score a submitted packet against the key derived from the artifacts.

Usage: python score_packet.py <packet.json>

The submitted packet is DATA. This script decides whether it matches; the
solver that produced it decides nothing. ``prompt/seed_prompt.md`` fixes
that direction and is sealed:

    never ask an LLM to decide equality, minimality, isomorphism,
    survivor counts, or proof status.

Totality is checked in both directions and before any comparison. A
packet missing a stage fails by name, and so does a packet carrying a
stage or field the key does not define. An empty packet is the worst
case, not the easiest one: it must fail loudly rather than match nothing
and report success.

A pass says the submitted values equal the committed exports. It says
nothing about how they were obtained, and nothing about the mathematics
-- that is settled by the Lean proofs and the enumeration, not by
agreement. See STATUS.md.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

from scoring_key import STAGES, expected


def _render(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def load_packet(path: pathlib.Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read packet: {exc}") from exc
    try:
        payload: object = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"packet is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("packet must be a JSON object keyed by stage id")
    return payload


def score(packet: dict[str, Any]) -> tuple[list[str], bool]:
    """Compare a packet to the key. Returns report lines and whether it passed."""

    key = expected()
    if not key:
        raise ValueError("the key resolved no stages; refusing to score")

    lines: list[str] = []
    ok = True

    unknown = sorted(set(packet) - set(key))
    for stage_id in unknown:
        ok = False
        lines.append(f"FAIL  {stage_id}: not a stage of this kernel")

    for stage in STAGES:
        fields = key[stage.stage_id]
        if stage.stage_id not in packet:
            ok = False
            lines.append(f"FAIL  {stage.stage_id}: absent from the packet")
            continue
        submitted = packet[stage.stage_id]
        if not isinstance(submitted, dict):
            ok = False
            lines.append(f"FAIL  {stage.stage_id}: not an object")
            continue

        stray = sorted(set(submitted) - set(fields))
        for name in stray:
            ok = False
            lines.append(f"FAIL  {stage.stage_id}.{name}: not a field of this stage")

        for name, want in fields.items():
            if name not in submitted:
                ok = False
                lines.append(f"FAIL  {stage.stage_id}.{name}: absent from the packet")
                continue
            got = submitted[name]
            # Compared as canonical renderings, not with ``==``. Python
            # equates False with 0 and 2 with 2.0, and a nested list makes
            # a shallow type check miss both. Rendering settles it at
            # every depth: "false" is not "0" and "2" is not "2.0".
            if _render(got) == _render(want):
                lines.append(f"pass  {stage.stage_id}.{name} = {_render(want)}")
            else:
                ok = False
                lines.append(
                    f"FAIL  {stage.stage_id}.{name}: "
                    f"expected {_render(want)}, got {_render(got)}"
                )

    total = sum(len(v) for v in key.values())
    passed = sum(1 for line in lines if line.startswith("pass "))
    lines.append(f"{passed} of {total} field(s) matched across {len(key)} stage(s)")
    return lines, ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a submitted packet.")
    parser.add_argument("packet", help="path to the submitted packet JSON")
    args = parser.parse_args()
    try:
        lines, ok = score(load_packet(pathlib.Path(args.packet)))
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
