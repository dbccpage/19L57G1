"""Tests for the bridge-provenance reachability searches."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.bridge import (
    classify,
    equivariant_scan,
    event_alphabet,
    occurrence_step,
    provenance_table,
    reachable_states,
    scenario_report,
)
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Regime,
    Supply,
    replay,
)

import run_bridge


def test_alphabet_shape() -> None:
    alpha = event_alphabet(["<>"], 2)
    assert Supply("<>") in alpha and AdmitDatum("<>") in alpha
    assert AdmitForm(2) in alpha
    assert AdmitInst(0, (0, 1)) in alpha and AdmitInst(0, (1, 1)) in alpha


def test_occurrence_step_appends_duplicates() -> None:
    r = replay([AdmitDatum("<>")])
    r2 = occurrence_step(r, AdmitDatum("<>"))
    assert r2.n_data() == 2
    assert r2.data == ("<>", "<>")
    # Non-admission events delegate to the standard step.
    assert occurrence_step(r, Supply("<>")) == r


def test_classify_shapes() -> None:
    d2ish = replay(
        [
            AdmitDatum("x"),
            AdmitDatum("y"),
            AdmitForm(2),
            AdmitInst(0, (0, 1)),
        ]
    )
    c = classify(d2ish)
    assert c.oriented_witness and not c.symmetric_witness
    assert c.irreflexive_fact and not c.self_edge
    s2ish = replay([AdmitInst(0, (1, 0))], d2ish)
    c2 = classify(s2ish)
    assert c2.symmetric_witness and not c2.oriented_witness
    selfish = replay(
        [AdmitDatum("x"), AdmitForm(2), AdmitInst(0, (0, 0))]
    )
    c3 = classify(selfish)
    assert c3.self_edge and not c3.irreflexive_fact


def test_single_token_never_reaches_two_or_witnessed_pair() -> None:
    """Exhaustive echo of the Lean carrier bound: one opaque token under
    dedup never yields carrier 2, and the only inhabited witness shape
    reachable is the self-edge."""
    rep = scenario_report("single_dedup", ["<>"], 7, False)
    assert rep["max_carrier"] == 1
    mins = rep["min_events_to"]
    assert mins["carrier_2"] is None
    assert mins["oriented_witness"] is None
    assert mins["symmetric_witness"] is None
    assert mins["self_edge"] == 3


def test_second_token_unlocks_the_target() -> None:
    rep = scenario_report("two_dedup", ["<>", "<a>"], 7, False)
    mins = rep["min_events_to"]
    assert rep["max_carrier"] == 2
    assert mins["carrier_2"] == 2
    assert mins["oriented_witness"] == 4
    assert mins["symmetric_witness"] == 5


def test_occurrence_discipline_matches_two_token_milestones() -> None:
    rep = scenario_report("occurrence", ["<>"], 7, True)
    mins = rep["min_events_to"]
    assert rep["max_carrier"] == 2
    assert mins["carrier_2"] == 2
    assert mins["oriented_witness"] == 4
    assert mins["symmetric_witness"] == 5


def test_equivariant_scan_unique_winner_is_symmetric() -> None:
    scan = equivariant_scan()
    assert len(scan["swap_invariant_relations"]) == 4
    assert scan["unique_equivariant_witness_is_symmetric"] is True


def test_reachable_states_depths_monotone() -> None:
    states = reachable_states(["<>"], 3)
    assert all(0 <= d <= 3 for d in states.values())
    empty = Regime((), (), frozenset(), frozenset(), frozenset())
    assert states[empty] == 0


def test_provenance_table_covers_all_ingredients() -> None:
    table = provenance_table()
    names = [row["ingredient"] for row in table]
    assert names == [
        "carrier (size 1)",
        "carrier (size 2)",
        "two designated occurrences",
        "relation (form)",
        "witness (instance)",
        "irreflexivity",
        "orientation",
    ]
    for row in table:
        assert row["verdict"] and row["mechanism"]


def test_run_bridge_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_bridge.main(
        ["--artifacts", str(out), "--max-events", "5"]
    ) == 0
    payload = json.loads((out / "bridge.json").read_text(encoding="utf-8"))
    assert len(payload["scenarios"]) == 3
    single = payload["scenarios"][0]
    assert single["max_carrier"] == 1
    assert single["min_events_to"]["oriented_witness"] is None
    # Determinism.
    out2 = tmp_path / "artifacts2"
    run_bridge.main(["--artifacts", str(out2), "--max-events", "5"])
    assert (out / "bridge.json").read_bytes() == (
        out2 / "bridge.json"
    ).read_bytes()
