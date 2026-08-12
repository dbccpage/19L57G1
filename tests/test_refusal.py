"""Tests for the refusal-discipline comparison."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.refusal import (
    DISCIPLINES,
    EMPTY,
    Adm,
    Form,
    Inst,
    RSt,
    Sup,
    capability_prices,
    discipline_report,
    equivalence_check,
    orientation_check,
    reachable,
    readmit_fact,
    readmit_reify_tagged,
    readmit_reify_untagged,
    readmit_silent,
    separable,
    step,
    swap_two,
)

import run_refusal


def _run(events: list[object], readmit: object, occ: bool = False) -> RSt:
    s = EMPTY
    for e in events:
        s = step(s, e, readmit, occ)  # type: ignore[arg-type]
    return s


def test_silent_readmission_is_designation() -> None:
    s = _run([Adm("<>"), Adm("<>")], readmit_silent)
    assert s.data == ("<>",) and s.refusals == 0 and not s.tags
    assert step(s, Sup("<>"), readmit_silent) == s


def test_fact_counts_without_growth() -> None:
    s = _run([Adm("<>"), Adm("<>"), Adm("<>")], readmit_fact)
    assert s.data == ("<>",)
    assert s.refusals == 2
    assert s != _run([Adm("<>")], readmit_fact)


def test_reify_tagged_two_admissions_witnessed_oriented() -> None:
    s = _run([Adm("<>"), Adm("<>")], readmit_reify_tagged)
    assert s.data == ("<>", "<>")
    assert s.tags == frozenset({1})
    assert separable(s, 0, 1)
    assert not s.insts
    assert swap_two(s) != s  # canonical orientation


def test_reify_untagged_symmetric_and_collapsed() -> None:
    s = _run([Adm("<>"), Adm("<>")], readmit_reify_untagged)
    assert s.data == ("<>", "<>") and not s.tags
    assert not separable(s, 0, 1)
    assert swap_two(s) == s  # per-act choice would be required


def test_explicit_route_needs_form_and_instance() -> None:
    s = _run(
        [Adm("<>"), Adm("<>"), Form(), Inst(1)], readmit_reify_untagged
    )
    assert separable(s, 0, 1)
    # instance before form, or out of range, is a no-op
    assert step(EMPTY, Inst(0), readmit_silent) == EMPTY
    s2 = _run([Adm("<>"), Form(), Form()], readmit_silent)
    assert s2.has_form
    assert step(s2, Inst(5), readmit_silent) == s2


def test_discipline_reports_four_way_outcomes() -> None:
    assert (
        discipline_report("silent", ["<>"], 5)["outcome"]
        == "no new object-level difference"
    )
    assert (
        discipline_report("meta", ["<>"], 5)["outcome"]
        == "one object plus one (metatheoretic) event"
    )
    assert (
        discipline_report("fact", ["<>"], 5)["outcome"]
        == "two states only"
    )
    for name in ("reify_untagged", "reify_tagged", "occurrence"):
        assert (
            discipline_report(name, ["<>"], 5)["outcome"]
            == "two carrier objects"
        )


def test_tagged_hits_witness_at_two_admissions() -> None:
    rep = discipline_report("reify_tagged", ["<>"], 5)
    mins = rep["min_events_to"]
    assert mins["witnessed_pair"] == 2
    assert mins["oriented_witnessed_pair"] == 2
    assert mins["witness_without_instances"] == 2


def test_untagged_and_baselines_need_four_events() -> None:
    for name, toks in (
        ("reify_untagged", ["<>"]),
        ("occurrence", ["<>"]),
        ("second_token", ["<>", "<a>"]),
    ):
        mins = discipline_report(name, toks, 6)["min_events_to"]
        assert mins["witnessed_pair"] == 4
        assert mins["witness_without_instances"] is None


def test_equivalence_reify_untagged_is_occurrence() -> None:
    eq = equivalence_check(6)
    assert eq["state_sets_equal"] is True


def test_orientation_check() -> None:
    oc = orientation_check()
    assert oc["tagged_swap_invariant"] is False
    assert oc["untagged_swap_invariant"] is True
    assert oc["tagged_separable_without_instances"] is True
    assert oc["untagged_separable"] is False


def test_capability_prices_cover_all_disciplines() -> None:
    rows = capability_prices()
    names = [r["discipline"] for r in rows]
    assert names == [
        "silent", "meta", "fact", "reify_untagged", "reify_tagged",
        "occurrence", "second_token",
    ]
    tagged = next(r for r in rows if r["discipline"] == "reify_tagged")
    assert len(tagged["imports"]) == 3


def test_reachable_respects_carrier_cap() -> None:
    states = reachable(["<>"], readmit_reify_untagged, 6, False)
    assert all(len(s.data) <= 2 for s in states)
    assert DISCIPLINES["silent"] is readmit_silent


def test_run_refusal_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_refusal.main(
        ["--artifacts", str(out), "--max-events", "5"]
    ) == 0
    payload = json.loads((out / "refusal.json").read_text(encoding="utf-8"))
    assert len(payload["disciplines"]) == 7
    assert payload["equivalence"]["state_sets_equal"] is True
    assert payload["orientation"]["tagged_swap_invariant"] is False
    out2 = tmp_path / "artifacts2"
    run_refusal.main(["--artifacts", str(out2), "--max-events", "5"])
    assert (out / "refusal.json").read_bytes() == (
        out2 / "refusal.json"
    ).read_bytes()
