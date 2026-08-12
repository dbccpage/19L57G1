"""Tests for the ultra-closure inventory, graph, protocols, and
minimality class."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.completion import (
    BRIDGES,
    KERNEL_DESC,
    NODES,
    PIGEON,
    PROBES,
    VALID_KINDS,
    VALID_ROLES,
    VALID_STATUSES,
    all_descs,
    aug_family,
    close_blocks,
    compliant,
    cost_capabilities,
    cost_lex,
    countermodels_report,
    dependency_graph,
    interp_step,
    inventory,
    minimality_report,
    next_family,
    parse_axiom_reports,
    probe_results,
    protocols_report,
    tower_block,
    tower_gen,
)
from derivation.represented import (
    hist_up_to,
    quiescent,
    repair_family,
    replay,
    step,
    viol,
)

import run_completion


def test_inventory_covers_axiom_artifact_exactly() -> None:
    reports = parse_axiom_reports()
    inv = inventory()
    assert len(inv) == len(reports)
    assert [r["name"] for r in inv] == [r["name"] for r in reports]
    for rec in inv:
        assert rec["module"] != "UNRESOLVED", rec["name"]
        assert rec["statement"] != "UNRESOLVED", rec["name"]
        assert rec["kind"] in VALID_KINDS
        assert rec["role"] in VALID_ROLES
        axioms = rec["axioms"]
        assert isinstance(axioms, list)
        assert set(axioms) <= {"propext", "Quot.sound"}


def test_dependency_graph_statuses_and_evidence_resolve() -> None:
    graph = dependency_graph()
    names = {str(r["name"]) for r in parse_axiom_reports()}
    for b in BRIDGES:
        assert b["status"] in VALID_STATUSES
        assert b["source"] in NODES and b["target"] in NODES
        evidence = b["evidence"]
        assert isinstance(evidence, list) and evidence
        for ev in evidence:
            assert isinstance(ev, str)
            if not ev.startswith("DECLARED:"):
                assert ev in names, ev
    statuses = graph["statuses"]
    assert isinstance(statuses, dict)
    assert statuses["OPEN"] == 1  # exactly one named irreducible bridge
    assert statuses["FALSE_WITH_COUNTERMODEL"] >= 6


def test_driver_reproduces_supplied_stream() -> None:
    for k in range(13):
        assert tower_gen(k) == hist_up_to(k)


def test_tower_family_is_singleton_and_stop_is_empty() -> None:
    w = replay(hist_up_to(3))
    assert next_family(w, "tower") == [tower_block(w)]
    assert quiescent(w)
    assert next_family(w, "close") == []
    assert next_family(w, "idle") == []


def test_close_family_complete_and_tie_retained() -> None:
    w = replay(PIGEON)
    blocks = close_blocks(w)
    assert viol(w, (1, 2))
    assert repair_family(w, (1, 2)) == []  # certified exhaustion
    fam = aug_family(w, (1, 2))
    assert (1,) in fam and (2,) in fam  # both orientations retained
    assert [("addView", (1,))] in blocks
    assert [("addView", (2,))] in blocks


def test_protocols_report_flags() -> None:
    rep = protocols_report(10)
    assert rep["G2_driver_reproduces_supplied_stream"] is True
    assert rep["G2_all_stages_accepted_quiescent_wf"] is True
    assert rep["close_family_retains_both_orientations"] is True
    assert rep["stop_outcome_empty_family"] is True


def test_interp_kernel_desc_matches_step() -> None:
    for (_, w, e) in PROBES:
        assert interp_step(KERNEL_DESC, w, e) == step(w, e)
    for k in range(4):
        w = replay(hist_up_to(k))
        for e in tower_block(w):
            assert interp_step(KERNEL_DESC, w, e) == step(w, e)


def test_each_guard_is_load_bearing() -> None:
    for idx in range(6):
        d = tuple(
            (i != idx) for i in range(6)
        )  # all guards on except idx
        results = probe_results(d)  # type: ignore[arg-type]
        assert not all(results.values()), idx
    assert all(probe_results(KERNEL_DESC).values())


def test_unique_compliant_kernel_and_orders_agree() -> None:
    descs = all_descs()
    assert len(descs) == 64 and len(set(descs)) == 64
    comp = [d for d in descs if compliant(d)]
    assert comp == [KERNEL_DESC]
    rep = minimality_report()
    assert rep["unique_compliant_is_kernel"] is True
    assert rep["orders_agree_on_singleton"] is True
    assert rep["interp_of_kernel_desc_matches_step"] is True
    assert cost_capabilities(KERNEL_DESC) == 6
    assert cost_lex(KERNEL_DESC) == (3, 3)


def test_countermodels_report_shape() -> None:
    rep = countermodels_report()
    failed = rep["failed_bridges"]
    assert isinstance(failed, list)
    assert len(failed) >= 6
    for row in failed:
        assert row["evidence"], row["bridge"]


def test_negative_and_malformed_in_interp() -> None:
    import pytest

    w = replay(PIGEON)
    assert interp_step(KERNEL_DESC, w, ("admit", -1)) == w
    with pytest.raises(AssertionError):
        interp_step(KERNEL_DESC, w, ("admit", "x"))


def test_nat_domain_holds_for_every_descriptor() -> None:
    """Disabled guards never license negative states: the Nat-domain
    guards are unconditional, so every constitution descriptor agrees
    with the Lean carrier — including the all-off descriptor."""
    all_off = (False, False, False, False, False, False)
    w = replay(PIGEON)
    for d in [KERNEL_DESC, all_off]:
        assert interp_step(d, w, ("admit", -7)) == w
        assert interp_step(d, w, ("require", -1, 0)) == w
        assert interp_step(d, w, ("require", 0, -1)) == w
        assert interp_step(d, w, ("mark", (0,), -1)) == w
        assert interp_step(d, w, ("mark", (-1,), 0)) == w
        assert interp_step(d, w, ("addView", (-1,))) == w
        assert interp_step(d, w, ("refuse", -1, -2)) == w
    # and the all-off descriptor still acts on non-negative inputs
    assert interp_step(all_off, w, ("require", 0, 0)) != w


def test_freshness_scoped_to_tower_invariant() -> None:
    from derivation.completion import fresh_name, tower_gen
    from derivation.represented import World

    for k in range(10):
        w = replay(tower_gen(k))
        assert fresh_name(w) not in w.data  # fresh on the invariant
    collide = World(data=(1,))
    assert fresh_name(collide) in collide.data  # not fresh in general


def test_run_main_and_receipt(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    out.mkdir()
    # the receipt hashes the committed axiom artifact; copy nothing —
    # the runner reads the repository's own artifacts directory for
    # the hash and writes the five outputs to --artifacts
    assert run_completion.main(["--artifacts", str(out)]) == 0
    receipt = json.loads(
        (out / "completion_receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["base_commit"] == "2c605e2"
    assert receipt["prompt_sha256"]["prompt/prompt.md"].startswith(
        "a613a196"
    )
    assert receipt["theorem_count"] == len(parse_axiom_reports())
    assert "RELATIVE_REPLAY_CLOSURE_ONLY" in receipt["terminals"]
    assert receipt["open_bridges"]
    for terminal in receipt["terminals"]:
        assert terminal in receipt["terminal_evidence"]
    graph = json.loads(
        (out / "completion_dependency_graph.json").read_text(
            encoding="utf-8")
    )
    assert graph["graph"]["statuses"]["OPEN"] == 1
    out2 = tmp_path / "artifacts2"
    out2.mkdir()
    run_completion.main(["--artifacts", str(out2)])
    for name in [
        "completion_dependency_graph.json",
        "completion_countermodels.json",
        "completion_protocols.json",
        "completion_minimality.json",
        "completion_receipt.json",
    ]:
        assert (out / name).read_bytes() == (out2 / name).read_bytes()
