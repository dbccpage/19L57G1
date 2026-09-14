"""Tests for Track 4: Confluence-Driven Internal Quotienting.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

import pytest

# Ensure repository root and code directory are accessible
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from research.endogenous_continuum.internal_quotienting import (
    Divergence,
    EquivalenceClass,
    JoinProof,
    LocalConfluenceReport,
    ReductionResult,
    ReductionStrategy,
    RelationalState,
    RewriteRule,
    RewriteStep,
    RewriteSystem,
    create_relational_state,
    make_relational_quotient_system,
    make_sorting_rewrite_system,
    make_string_rewrite_system,
    make_string_rule,
    verify_equivalence_partition,
)


# =============================================================================
# 1. Local Confluence Holds on Defined Rewrite Systems
# =============================================================================


def test_local_confluence_holds_on_sorting_system() -> None:
    """Evaluate local confluence for alphabetical sorting rewrites on candidate words."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c", "d"))

    # Test candidate words with multiple inversions and branching possibilities
    test_words = [
        "ba",
        "cba",
        "dcba",
        "bca",
        "cbda",
        "badc",
        "dcab",
        "cbad",
        "bbccaa",
    ]

    report = system.check_local_confluence(test_words, max_join_depth=25)

    assert report.is_locally_confluent is True
    assert report.checked_states_count == len(test_words)
    assert report.divergences_count > 0
    assert report.joined_count == report.divergences_count
    assert len(report.unjoinable_divergences) == 0
    assert len(report.join_proofs) == report.divergences_count


def test_local_confluence_holds_on_relational_system() -> None:
    """Evaluate local confluence for relational alias contractions across branching networks."""
    system = make_relational_quotient_system()

    # Relational configurations with multiple simultaneous alias contracts
    s1 = create_relational_state(
        tokens=["t0", "t1", "t2"],
        relations=[("eq", "t0", "t1"), ("eq", "t0", "t2"), ("link", "t1", "t2")],
    )
    s2 = create_relational_state(
        tokens=["x", "y", "z", "w"],
        relations=[
            ("eq", "x", "y"),
            ("eq", "y", "z"),
            ("eq", "z", "w"),
            ("rel", "x", "w"),
        ],
    )
    s3 = create_relational_state(
        tokens=["a", "b", "c"],
        relations=[("eq", "a", "b"), ("eq", "b", "c"), ("eq", "a", "c")],
    )

    test_states = [s1, s2, s3]
    report = system.check_local_confluence(test_states, max_join_depth=20)

    assert report.is_locally_confluent is True
    assert report.checked_states_count == len(test_states)
    assert report.divergences_count > 0
    assert report.joined_count == report.divergences_count
    assert len(report.unjoinable_divergences) == 0


# =============================================================================
# 2. All One-Step Divergences Join Within Finite Rewrite Steps
# =============================================================================


def test_all_one_step_divergences_join_within_finite_steps() -> None:
    """Verify that every identified divergence produces a valid constructive join witness."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c"))
    states = ["cba", "bca", "bac", "cab", "cbba", "acba"]

    report = system.check_local_confluence(states, max_join_depth=30)
    assert report.is_locally_confluent is True
    assert report.divergences_count > 0

    for proof in report.join_proofs:
        assert proof.joined is True
        assert proof.join_state is not None
        # Trajectories must begin at branches and terminate at common join state
        assert proof.path_a[0] == proof.branch_a
        assert proof.path_a[-1] == proof.join_state
        assert proof.path_b[0] == proof.branch_b
        assert proof.path_b[-1] == proof.join_state

        # Check step consistency
        assert len(proof.rules_a) == len(proof.path_a) - 1
        assert len(proof.rules_b) == len(proof.path_b) - 1

        # Verify each step along path_a was valid under the system
        for idx, rule_name in enumerate(proof.rules_a):
            curr_state = proof.path_a[idx]
            next_state = proof.path_a[idx + 1]
            valid_targets = system.step(curr_state)
            assert next_state in valid_targets

        # Verify each step along path_b was valid under the system
        for idx, rule_name in enumerate(proof.rules_b):
            curr_state = proof.path_b[idx]
            next_state = proof.path_b[idx + 1]
            valid_targets = system.step(curr_state)
            assert next_state in valid_targets


def test_relational_divergences_join_within_finite_steps() -> None:
    """Verify join witness paths for relational state contractions."""
    system = make_relational_quotient_system()
    st = create_relational_state(
        tokens=["u", "v", "w", "x"],
        relations=[
            ("eq", "u", "v"),
            ("eq", "u", "w"),
            ("eq", "u", "x"),
            ("edge", "v", "w"),
        ],
    )

    divs = system.find_divergences_at(st)
    assert len(divs) >= 2

    for div in divs:
        proof = system.find_join(div.branch_a, div.branch_b, source=st, max_depth=15)
        assert proof.joined is True
        assert proof.join_state is not None
        assert proof.path_a[0] == div.branch_a
        assert proof.path_a[-1] == proof.join_state
        assert proof.path_b[0] == div.branch_b
        assert proof.path_b[-1] == proof.join_state
        # Join state must have exactly one contracted token representing u,v,w,x
        assert "u" in proof.join_state.tokens


# =============================================================================
# 3. Uniqueness of Normal Forms Regardless of Reduction Path Order
# =============================================================================


def test_uniqueness_of_normal_forms_across_all_reduction_paths() -> None:
    """Verify that exploring all maximal reduction paths yields a single unique normal form."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c", "d"))
    test_word = "dcba"

    all_paths = system.all_reduction_paths(test_word, max_depth=20)
    assert len(all_paths) > 1  # Multiple alternative reduction sequences exist

    normal_forms = system.all_normal_forms(test_word, max_depth=20)
    assert len(normal_forms) == 1
    assert "abcd" in normal_forms

    # Confirm every individual reduction path finished at 'abcd'
    for path in all_paths:
        assert path.is_normal_form is True
        assert path.normal_form == "abcd"


def test_reduction_strategy_invariance() -> None:
    """Verify normal form identity between FIRST, LAST, and SHORTEST_PATH strategies."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c", "d"))
    complex_word = "dbcaadcb"

    res_first = system.reduce_to_normal_form(complex_word, strategy=ReductionStrategy.FIRST)
    res_last = system.reduce_to_normal_form(complex_word, strategy=ReductionStrategy.LAST)
    res_shortest = system.reduce_to_normal_form(
        complex_word, strategy=ReductionStrategy.SHORTEST_PATH
    )

    assert res_first.is_normal_form is True
    assert res_last.is_normal_form is True
    assert res_shortest.is_normal_form is True

    # All three reduction strategies reach the exact same irreducible normal form
    assert res_first.normal_form == res_last.normal_form == res_shortest.normal_form
    assert res_first.normal_form == "aabbccdd"

    # Shortest path steps must be less than or equal to alternative paths
    assert res_shortest.steps_count <= res_first.steps_count
    assert res_shortest.steps_count <= res_last.steps_count


def test_relational_normal_form_uniqueness() -> None:
    """Verify uniqueness of normal form for relational configurations across reduction orders."""
    system = make_relational_quotient_system()
    st = create_relational_state(
        tokens=["t1", "t2", "t3", "t4", "t5"],
        relations=[
            ("eq", "t1", "t2"),
            ("eq", "t2", "t3"),
            ("eq", "t3", "t4"),
            ("eq", "t4", "t5"),
            ("edge", "t1", "t5"),
            ("edge", "t2", "t4"),
        ],
    )

    all_paths = system.all_reduction_paths(st, max_depth=15)
    assert len(all_paths) > 1

    normal_forms = system.all_normal_forms(st, max_depth=15)
    assert len(normal_forms) == 1

    canonical_nf = next(iter(normal_forms))
    assert canonical_nf.tokens == ("t1",)
    assert canonical_nf.relations == frozenset({("edge", "t1", "t1")})

    res_first = system.reduce_to_normal_form(st, strategy=ReductionStrategy.FIRST)
    res_last = system.reduce_to_normal_form(st, strategy=ReductionStrategy.LAST)
    assert res_first.normal_form == res_last.normal_form == canonical_nf


# =============================================================================
# 4. Rejection of Non-Confluent Rewrite Systems (Detecting Unjoinable Critical Pairs)
# =============================================================================


def test_rejection_of_non_confluent_string_rewrite_system() -> None:
    """Verify that a rewrite system with unjoinable overlapping rules is rejected."""
    # Classic non-confluent system: ab -> c, ba -> d
    # Input word 'aba' branches to 'ca' (via ab->c at 0) and 'ad' (via ba->d at 1).
    # Both 'ca' and 'ad' are irreducible, so they cannot join.
    rules = [
        ("ab", "c"),
        ("ba", "d"),
    ]
    non_confluent_system = make_string_rewrite_system(rules, name="NonConfluentStringSystem")

    report = non_confluent_system.check_local_confluence(["aba"], max_join_depth=10)

    assert report.is_locally_confluent is False
    assert report.divergences_count == 1
    assert report.joined_count == 0
    assert len(report.unjoinable_divergences) == 1

    unjoinable = report.unjoinable_divergences[0]
    assert unjoinable.source == "aba"
    branches = {unjoinable.branch_a, unjoinable.branch_b}
    assert branches == {"ca", "ad"}

    # Confirm that multiple distinct normal forms exist for 'aba'
    normal_forms = non_confluent_system.all_normal_forms("aba", max_depth=10)
    assert normal_forms == frozenset({"ca", "ad"})
    assert len(normal_forms) == 2


def test_rejection_of_competing_terminal_branches() -> None:
    """Verify detection and rejection of competing terminal rules without join paths."""
    r1 = make_string_rule("x", "y1", name="rule_branch_1")
    r2 = make_string_rule("x", "y2", name="rule_branch_2")
    system = RewriteSystem(rules=[r1, r2], name="CompetingTerminalSystem")

    report = system.check_local_confluence(["x"], max_join_depth=10)

    assert report.is_locally_confluent is False
    assert report.divergences_count == 1
    assert report.joined_count == 0
    assert len(report.unjoinable_divergences) == 1
    assert report.unjoinable_divergences[0].branch_a in {"y1", "y2"}
    assert report.unjoinable_divergences[0].branch_b in {"y1", "y2"}


def test_rejection_of_conflicting_relational_rules() -> None:
    """Verify rejection when relational rules induce conflicting terminal states."""
    def rule_collapse_left(st: RelationalState) -> tuple[RelationalState, ...]:
        if "conflict" in st.tokens:
            return (RelationalState(tokens=("token_left",), relations=frozenset()),)
        return ()

    def rule_collapse_right(st: RelationalState) -> tuple[RelationalState, ...]:
        if "conflict" in st.tokens:
            return (RelationalState(tokens=("token_right",), relations=frozenset()),)
        return ()

    system = RewriteSystem(
        rules=[
            RewriteRule(name="left", apply_fn=rule_collapse_left),
            RewriteRule(name="right", apply_fn=rule_collapse_right),
        ],
        name="ConflictingRelationalSystem",
    )

    seed_state = RelationalState(tokens=("conflict",), relations=frozenset())
    report = system.check_local_confluence([seed_state], max_join_depth=10)

    assert report.is_locally_confluent is False
    assert report.divergences_count == 1
    assert len(report.unjoinable_divergences) == 1


# =============================================================================
# 5. Endogenous Equivalence Partitioner and Quotient Projection
# =============================================================================


def test_endogenous_equivalence_partitioner() -> None:
    """Verify grouping of words into exact multiset equivalence classes."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c"))

    # Six permutations of abc, three of aab, and three of abb
    words = [
        "abc", "acb", "bac", "bca", "cab", "cba",
        "aab", "aba", "baa",
        "abb", "bab", "bba",
    ]

    classes = system.partition_by_normal_form(words)

    # There must be exactly three distinct equivalence classes
    assert len(classes) == 3

    # Verify partition integrity using helper
    assert verify_equivalence_partition(classes, words) is True

    class_dict = {c.normal_form: c for c in classes}
    assert "abc" in class_dict
    assert "aab" in class_dict
    assert "abb" in class_dict

    assert class_dict["abc"].size == 6
    assert set(class_dict["abc"].members) == {"abc", "acb", "bac", "bca", "cab", "cba"}

    assert class_dict["aab"].size == 3
    assert set(class_dict["aab"].members) == {"aab", "aba", "baa"}

    assert class_dict["abb"].size == 3
    assert set(class_dict["abb"].members) == {"abb", "bab", "bba"}


def test_quotient_projection_idempotence_and_compatibility() -> None:
    """Verify idempotence q(q(x)) == q(x) and step compatibility q(x) == q(y) for x -> y."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c"))

    test_words = ["cba", "cab", "acb", "bca", "bac"]
    for w in test_words:
        q_w = system.quotient_projection(w)
        assert system.quotient_projection(q_w) == q_w  # Idempotence

        # Compatibility across every 1-step successor
        successors = system.step(w)
        for succ in successors:
            assert system.quotient_projection(succ) == q_w
            assert system.are_equivalent(w, succ) is True


# =============================================================================
# 6. Exact Arithmetic and Cycle Detection Safeguards
# =============================================================================


def test_exact_rational_cost_tracking() -> None:
    """Verify that rewrite steps track exact rational Fraction costs."""
    def custom_cost(rule_name: str, src: str, dst: str) -> Fraction:
        if "ba" in src:
            return Fraction(3, 7)
        return Fraction(1, 11)

    base_system = make_sorting_rewrite_system(alphabet=("a", "b", "c"))
    system = RewriteSystem(
        rules=base_system.rules,
        name="ExactCostSortingSystem",
        cost_fn=custom_cost,
    )

    res = system.reduce_to_normal_form("ba")
    assert res.is_normal_form is True
    assert res.normal_form == "ab"
    assert res.steps_count == 1
    assert res.total_cost == Fraction(3, 7)

    res_cba = system.reduce_to_normal_form("cba", strategy=ReductionStrategy.FIRST)
    assert res_cba.is_normal_form is True
    assert res_cba.normal_form == "abc"
    assert isinstance(res_cba.total_cost, Fraction)


def test_cycle_detection_in_non_terminating_system() -> None:
    """Verify that circular rewrite rules trigger cycle detection rather than hanging."""
    r_ab = make_string_rule("a", "b", name="a_to_b")
    r_ba = make_string_rule("b", "a", name="b_to_a")
    system = RewriteSystem(rules=[r_ab, r_ba], name="OscillatingSystem")

    with pytest.raises(RuntimeError, match="Reduction cycle detected"):
        system.reduce_to_normal_form("a", strategy=ReductionStrategy.FIRST, max_steps=50)
