"""Tests for the challenge analyses, the generator, and the branch tree."""

from __future__ import annotations

from derivation.candidates import Bounds, NewDatum, NewForm, NewInst, NewRuleAll
from derivation.engine import (
    READING_F,
    READING_L,
    build_tree,
    challenge0_report,
    challenge1_report,
    challenge2_report,
    challenge3_report,
    delta_label,
)
from derivation.export import tree_json
from derivation.model import replay
from derivation.observe import collapsed_pairs

BOUNDS = Bounds(max_items=2, max_arity=2)


def test_challenge0_inertia() -> None:
    rep = challenge0_report()
    assert rep["supply_changes_state"] is False
    assert rep["admitted_data"] == []
    assert rep["context_count"] == 0
    assert rep["derivable_instances"] == []
    assert rep["internally_forced_successor"] is None


def test_challenge1_supply_vs_admission_and_convergence() -> None:
    rep = challenge1_report()
    assert rep["new_external_presentation"] is True
    assert rep["admitted_without_admission_event"] is False
    assert rep["sub_readings_converge_at_challenge2"] is True
    assert rep["internal_observable_distinction"] is False


def test_challenge2_collapse_and_no_expressive_increase() -> None:
    rep = challenge2_report()
    readings = rep["readings"]
    assert isinstance(readings, dict)
    assert readings["L"]["admitted_data"] == ["<a>", "<ab>"]
    assert readings["L"]["collapsed_pairs"] == [(0, 1)]
    assert readings["F"]["admitted_data"] == ["<>", "<a>", "<ab>"]
    assert len(readings["F"]["collapsed_pairs"]) == 3
    for name in ("L", "F"):
        assert readings[name]["observational_classes"] == 1
        assert readings[name]["expressive_increase_over_challenge0"] is False


def test_challenge3_reading_l_classes() -> None:
    rep = challenge3_report(READING_L, BOUNDS)
    assert rep["current_regime_satisfies"] is False
    assert rep["witness"] is None
    mu1 = rep["mu1"]
    mu2 = rep["mu2"]
    assert isinstance(mu1, dict) and isinstance(mu2, dict)
    assert mu1["minimum_cost"] == [2, -1]
    labels = [c["label"] for c in mu1["iso_classes"]]
    assert sorted(labels) == ["form1+inst1", "form2+inst2", "form2+inst2diag"]
    assert all(c["class_size"] == 2 for c in mu1["iso_classes"])
    assert mu2["minimum_cost"] == [2, 1]
    assert len(mu2["iso_classes"]) == 1
    caps = mu1["iso_classes"][0]["capabilities"]
    assert caps["new_forms"] == 1 and caps["new_instances"] == 1


def test_challenge3_reading_f_has_five_classes() -> None:
    rep = challenge3_report(READING_F, BOUNDS)
    mu1 = rep["mu1"]
    assert isinstance(mu1, dict)
    assert len(mu1["iso_classes"]) == 5
    mu2 = rep["mu2"]
    assert isinstance(mu2, dict)
    assert len(mu2["iso_classes"]) == 1


def test_delta_label_shapes() -> None:
    base = replay(READING_L.genesis)
    assert delta_label(base, ()) == "empty"
    assert delta_label(base, (NewDatum(),)) == "datum"
    assert delta_label(base, (NewForm(2), NewInst(0, (0, 0)))) == (
        "form2+inst2diag"
    )
    assert delta_label(base, (NewRuleAll(0),)) == "rule@0"
    assert (
        delta_label(base, (NewDatum(), NewInst(0, (0, 2))))
        == "datum+inst2+fresh"
    )


def test_build_tree_small_deterministic_and_certified() -> None:
    t1 = build_tree(READING_L, "mu2", BOUNDS, max_rounds=5, node_budget=40)
    t2 = build_tree(READING_L, "mu2", BOUNDS, max_rounds=5, node_budget=40)
    assert tree_json(t1) == tree_json(t2)
    stats = t1.stats()
    assert stats["all_certified"] is True
    assert stats["max_depth"] == 5
    assert "completed" in stats["by_status"]


def test_build_tree_root_uses_challenge3_target() -> None:
    t = build_tree(READING_F, "mu2", BOUNDS, max_rounds=1, node_budget=10)
    round1 = [e for e in t.edges if e.round_no == 1]
    assert round1 and all(e.challenge == "separate(1, 2)" for e in round1)


def test_build_tree_merges_isomorphic_nodes() -> None:
    t = build_tree(READING_L, "mu1", BOUNDS, max_rounds=5, node_budget=400)
    assert any(n.merged_count > 1 for n in t.nodes)


def test_build_tree_budget_frontier() -> None:
    t = build_tree(READING_L, "mu1", BOUNDS, max_rounds=15, node_budget=5)
    stats = t.stats()
    assert stats["by_status"].get("frontier_budget", 0) > 0


def test_supply_alternation_in_mu2_lineage() -> None:
    """After the mark, the generator supplies a fresh datum; the fresh datum
    is collapsed with the unmarked one and gets separated at cost 1."""
    t = build_tree(READING_L, "mu2", BOUNDS, max_rounds=3, node_budget=30)
    supply_edges = [e for e in t.edges if e.challenge == "supply"]
    assert supply_edges, "expected a supply round within three rounds"
    for e in t.edges:
        if e.round_no == 3 and e.challenge != "supply":
            assert e.cost[0] == 1


def test_no_supply_variant_terminates_within_pair_bound() -> None:
    for reading in (READING_L, READING_F):
        t = build_tree(
            reading, "mu1", BOUNDS, max_rounds=15, node_budget=200,
            supply=False,
        )
        stats = t.stats()
        assert stats["by_status"].get("terminal_all_separated", 0) > 0
        assert "frontier_budget" not in stats["by_status"]
        n = t.nodes[0].regime.n_data()
        assert stats["max_depth"] <= n * (n - 1) // 2
        for node in t.nodes:
            if node.status == "terminal_all_separated":
                assert collapsed_pairs(node.regime) == ()


def test_delta_json_items_all_kinds() -> None:
    from derivation.engine import delta_json_items

    assert delta_json_items((NewDatum(), NewRuleAll(1))) == [
        {"kind": "datum"},
        {"kind": "rule_all", "form": 1},
    ]


def test_role_classification_of_rare_response_shapes() -> None:
    from derivation.engine import Edge, _role

    def edge(response: tuple) -> Edge:  # type: ignore[type-arg]
        return Edge(0, 1, 1, "separate(0, 1)", "x", response, 1, 1, (2, -1))

    assert _role(edge((NewDatum(), NewInst(0, (0, 2))))) == "auxiliary_witness"
    assert (
        _role(edge((NewInst(0, (0,)), NewInst(0, (1,)))))
        == "double_discrimination"
    )


def test_tree_terminal_when_no_response_within_bounds() -> None:
    """With a zero-item candidate space the root has no justified response:
    the branch stops and says so."""
    t = build_tree(
        READING_L,
        "mu1",
        Bounds(max_items=0, max_arity=2),
        max_rounds=3,
        node_budget=10,
    )
    assert t.nodes[0].status == "terminal_no_response"
    assert len(t.nodes) == 1


def test_endogenous_generator_is_token_blind() -> None:
    """Renaming every presentation token leaves the generated challenge
    unchanged: the endogenous generator reads no glyphs."""
    from derivation.engine import next_endogenous_challenge
    from derivation.model import Regime

    r = replay(READING_F.genesis)
    renamed = Regime(
        tuple(f"opaque-{k}" for k in range(r.n_data())),
        r.forms,
        r.insts,
        r.rules,
        r.reqs,
    )
    assert next_endogenous_challenge(r) == next_endogenous_challenge(renamed)
    assert next_endogenous_challenge(r) == (0, 1)


def test_endogenous_generator_fixpoint() -> None:
    """Once every pair is separated the endogenous generator yields
    nothing: no unresolved requirement is generatable from the admitted
    structure alone."""
    from derivation.engine import next_endogenous_challenge
    from derivation.model import AdmitForm, AdmitInst

    r = replay(
        (AdmitForm(1), AdmitInst(0, (1,))),
        replay(READING_L.genesis),
    )
    assert next_endogenous_challenge(r) is None


def test_closed_system_terminal_at_round_boundary() -> None:
    """A closed-system node that reaches the fixpoint exactly at the round
    limit is terminal, not round-cut."""
    t = build_tree(
        READING_F, "mu1", BOUNDS, max_rounds=3, node_budget=200,
        supply=False,
    )
    stats = t.stats()
    assert "completed" not in stats["by_status"]
    assert stats["by_status"].get("terminal_all_separated", 0) > 0


def test_generator_never_challenges_a_required_pair() -> None:
    t = build_tree(READING_L, "mu2", BOUNDS, max_rounds=6, node_budget=60)
    for node in t.nodes:
        assert not (set(collapsed_pairs(node.regime)) & set(node.regime.reqs))
