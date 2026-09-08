"""Recounts pinned by the 2026-09-08 reconciliation of the paper with its
evidence: identity is the index and not the profile, the requested depth
counts transition steps and not response rounds, the mu1 guard cuts sit
below the maximum depth, and a delta is applied in order."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence, cast

import pytest

from derivation.candidates import Bounds, NewForm, NewInst, apply_delta, min_responses
from derivation.engine import READING_F
from derivation.export import Json, read_json_gz
from derivation.model import AdmissionError, EMPTY, replay
from derivation.observe import collapsed_pairs, profiles

REPO = Path(__file__).resolve().parent.parent


def _leaf_counts(name: str) -> dict[str, list[tuple[int, int]]]:
    """For every node: (depth, separation-response rounds) along its
    creation path; keyed by status."""
    payload = cast(Mapping[str, Json], read_json_gz(REPO / "artifacts" / "full" / f"{name}.json.gz"))
    parent: dict[int, int] = {}
    response: dict[int, bool] = {}
    for edge in cast(Sequence[Mapping[str, Json]], payload["edges"]):
        if edge["kind"] == "creation":
            child = cast(int, edge["child"])
            parent[child] = cast(int, edge["parent"])
            response[child] = edge["challenge"] != "supply"
    out: dict[str, list[tuple[int, int]]] = {}
    for node in cast(Sequence[Mapping[str, Json]], payload["nodes"]):
        nid = cast(int, node["id"])
        depth = rounds = 0
        while nid != 0:
            depth += 1
            rounds += int(response[nid])
            nid = parent[nid]
        out.setdefault(cast(str, node["status"]), []).append((depth, rounds))
    return out


def test_identity_is_index_not_profile() -> None:
    base = replay(READING_F.genesis)
    minima = min_responses(base, READING_F.target, "mu2", Bounds(2, 2))
    assert minima is not None
    delta = (NewForm(1), NewInst(0, (1,)))
    assert delta in minima.deltas
    assert minima.cost == (2, 1)
    result = apply_delta(base, delta)
    assert [len(p) for p in profiles(result)] == [0, 1, 0]
    assert collapsed_pairs(result) == ((0, 2),)
    assert (1, 2) not in collapsed_pairs(result)


@pytest.mark.parametrize(
    "name, expected",
    [("tree_L_mu2", {(15, 10): 527, (15, 11): 41}),
     ("tree_F_mu2", {(15, 10): 268, (15, 11): 605, (15, 12): 12})],
)
def test_completed_mu2_leaves_carry_ten_to_twelve_response_rounds(
    name: str, expected: dict[tuple[int, int], int]
) -> None:
    counts = _leaf_counts(name)
    distribution: dict[tuple[int, int], int] = {}
    for key in counts["completed"]:
        distribution[key] = distribution.get(key, 0) + 1
    assert distribution == expected
    assert all(depth == 15 for depth, _ in counts["completed"])


@pytest.mark.parametrize(
    "name, first_cut, maximum, by_depth",
    [("tree_L_mu1", 6, 7, {6: 47, 7: 880}), ("tree_F_mu1", 5, 6, {5: 303, 6: 583})],
)
def test_mu1_first_guard_cut_below_maximum_depth(
    name: str, first_cut: int, maximum: int, by_depth: dict[int, int]
) -> None:
    counts = _leaf_counts(name)
    frontier: dict[int, int] = {}
    for depth, _ in counts["frontier_guard"]:
        frontier[depth] = frontier.get(depth, 0) + 1
    assert frontier == by_depth
    assert min(frontier) == first_cut
    assert max(depth for entries in counts.values() for depth, _ in entries) == maximum
    assert sum(frontier.values()) == sum(by_depth.values())


def test_delta_application_is_ordered() -> None:
    base = replay(READING_F.genesis)
    assert base.forms == ()
    apply_delta(base, (NewForm(1), NewInst(0, (0,))))
    with pytest.raises(AdmissionError):
        apply_delta(base, (NewInst(0, (0,)), NewForm(1)))
    assert EMPTY.forms == ()
