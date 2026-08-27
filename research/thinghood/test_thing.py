"""Tests for the bounded thinghood construction run."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_thing
from thing import (
    PROMPT_SHA256,
    Candidate,
    PASSAGE_STORE_OPTIONS,
    all_candidates,
    candidate_isomorphic,
    class_results,
    collapse_fails_law,
    dynamics_report,
    implication_lattice,
    is_datum,
    is_difference,
    is_thing,
    law_order_report,
    minimality_report,
    prompt_hash,
    tick_analysis,
)


def _candidate(**kwargs: object) -> Candidate:
    defaults: dict[str, object] = {
        "n": 2,
        "rel": frozenset({(0, 1)}),
        "asserted": (0, 1),
        "law": "irreflexive",
        "meta_inequality": False,
        "stores": (),
        "designated": (0, 1),
    }
    defaults.update(kwargs)
    return Candidate(**defaults)  # type: ignore[arg-type]


def test_prompt_is_byte_identical() -> None:
    prompt = HERE / "PROMPT.md"
    raw = prompt.read_bytes()
    assert prompt_hash() == PROMPT_SHA256
    assert b"\r" not in raw
    assert raw


def test_declared_space_is_finite_and_well_formed() -> None:
    candidates = all_candidates()
    assert len(candidates) == 120640
    assert all(1 <= candidate.n <= 3 for candidate in candidates)
    assert all(len(candidate.rel) <= 3 for candidate in candidates)
    assert all(
        candidate.asserted is None or candidate.asserted in candidate.rel
        for candidate in candidates
    )
    assert all(candidate.designated is not None for candidate in candidates if candidate.meta_inequality)


def test_required_classes_have_witnesses_or_countermodels() -> None:
    classes = class_results()["required_classes"]
    assert isinstance(classes, dict)
    assert classes["carrier_no_relation_no_law"]["can_fail_law"] is False
    assert classes["a1_bare_asserted_pair"]["can_fail_law"] is False
    assert classes["a3_meta_inequality"]["can_fail_law"] is False
    assert classes["a1i_asserted_pair_irreflexive"]["can_fail_law"] is True
    assert classes["a1_asserted_pair_symmetry_only"]["can_fail_law"] is False
    assert classes["richer_law"]["can_fail_law"] is True
    assert classes["richer_law"]["representative_is_witness"] is True
    assert classes["richer_law"]["witness"] is not None
    for name in (
        "carrier_no_relation_no_law",
        "a1_bare_asserted_pair",
        "a3_meta_inequality",
        "a1_asserted_pair_symmetry_only",
    ):
        assert classes[name]["countermodel"] is not None


def test_symmetry_countermodel_really_preserves_symmetry() -> None:
    symmetric = _candidate(
        rel=frozenset({(0, 1), (1, 0)}),
        law="symmetric",
    )
    assert not collapse_fails_law(symmetric)
    assert classes_have_symmetric_countermodel(symmetric)


def classes_have_symmetric_countermodel(candidate: Candidate) -> bool:
    """Negative test helper: every admitted-pair collapse preserves symmetry."""

    from thing import collapsing_functions, law_holds, pushforward

    return all(
        law_holds(candidate.n, pushforward(candidate.rel, function), "symmetric")
        for function in collapsing_functions(candidate)
    )


def test_minimum_is_exhaustive_and_non_unique() -> None:
    report = minimality_report()
    assert report["minimum_cost"] == 5
    assert report["below_minimum_survivor_count"] == 0
    assert report["every_below_minimum_fails"] is True
    assert report["every_minimum_satisfies"] is True
    assert report["minimum_isomorphism_class_count"] == 2
    assert report["non_unique_first_answer"] is True
    laws = {row["law"] for row in report["minimum_representatives"]}
    assert laws == {"irreflexive", "asymmetric"}


def test_orientation_relabelling_is_quotiented_but_law_tie_is_not() -> None:
    forward = _candidate()
    reverse = _candidate(rel=frozenset({(1, 0)}), asserted=(1, 0), designated=(1, 0))
    asymmetric = _candidate(law="asymmetric")
    assert candidate_isomorphic(forward, reverse)
    assert not candidate_isomorphic(forward, asymmetric)


def test_lattice_keeps_datum_difference_and_thing_distinct() -> None:
    edges = implication_lattice()["edges"]
    assert edges["difference->datum"]["holds_in_declared_space"] is True
    assert edges["difference->thing"]["holds_in_declared_space"] is True
    assert edges["thing->datum"]["holds_in_declared_space"] is True
    assert edges["datum->thing"]["holds_in_declared_space"] is False
    assert edges["thing->difference"]["holds_in_declared_space"] is False
    assert is_datum(_candidate())
    assert is_difference(_candidate())
    assert is_thing(_candidate())
    assert not is_thing(_candidate(law="none"))


def test_asymmetric_tie_is_strictly_richer_by_declared_law_order() -> None:
    report = law_order_report()
    assert report["asymmetric_implies_irreflexive"] is True
    assert report["irreflexive_not_implies_asymmetric"] is True
    assert report["strictly_richer_in_declared_law_order"] is True
    assert report["reverse_countermodel"]["relation"] == [[0, 1], [1, 0]]


def test_passage_stores_are_separately_priced() -> None:
    options = class_results()["required_classes"]["sealed_passage_state"]["options"]
    assert set(options) == {"not_admitted", "retained", "protected", "observed", "retained+protected", "retained+observed", "protected+observed", "retained+protected+observed"}
    assert options["not_admitted"]["store_admissions"] == 0
    assert options["retained+protected+observed"]["store_admissions"] == 3
    assert len(PASSAGE_STORE_OPTIONS) == 8
    assert minimality_report()["minimum_cost"] < options["retained"]["candidate"]["bill"]["total"]
    base = _candidate()
    resourced = _candidate(budget_admitted=True, license_admitted=True)
    assert resourced.bill().total == base.bill().total + 2


def test_dynamics_has_all_five_conditions_and_three_opens() -> None:
    report = dynamics_report()
    assert report["terminal"] == "NO_FORCED_DYNAMICAL_LAW"
    assert report["open_terminals"] == ["OB1_UNCHANGED", "S66_UNCHANGED", "S9_LAST_UNCHANGED"]
    assert report["machine_check_status"] == "NOT_RUN"
    assert "does not elaborate or resolve" in report["machine_check_reason"]
    assert all(claim["machine_check"] is False for claim in report["claims"])
    assert report["declared_composite"]["not_inscription_forced"] is True
    assert report["declared_composite"]["repair_derived"] is False
    assert report["forbidden_closures"] == {"S6_item_6": True, "S9_last_bullet": True, "OB-1": True}
    assert report["claims"][3]["hypotheses"][:1] == ["hobst : obstP s i j = true"]


def test_resource_free_tick_probe_keeps_three_residuals_open() -> None:
    report = tick_analysis()
    assert report["candidate_kinds"] == ["collision", "equal_profiles", "directional_residual"]
    assert report["resource_free_survivor_count"] == 0
    assert report["all_three_fail_without_extra"] is True
    assert report["endogenous_successor_derived"] is False
    assert report["open_scope"].startswith("The three-kind probe does not close")
    fallbacks = {probe["kind"]: probe["fallback_classification"] for probe in report["probes"]}
    assert fallbacks == {
        "collision": "VOID_CYCLE",
        "equal_profiles": "CHALLENGE_0",
        "directional_residual": "VOID_CYCLE",
    }


def test_limit_theorem_scope_is_not_widened() -> None:
    import thing

    limit = thing.build_receipt()["limit_scope"]
    assert limit["scope"] == "LocalStrategy + FiniteDeclaration"
    assert limit["evidence"] == ["generation_never_dries", "g1_class_exclusion"]
    assert limit["unbounded_extension_claim"] is False


def test_apparatus_ethics_are_explicit() -> None:
    import thing

    ethics = thing.build_receipt()["apparatus_ethics"]
    assert ethics["withdrawals_remain_withdrawals"] is True
    assert ethics["counts_without_min_response_witness_are_not_claims"] is True
    assert ethics["authority_effect"] == "None"


def test_adversarial_attacks_cannot_smuggle_closures() -> None:
    from thing import adversarial_attacks

    attacks = adversarial_attacks()
    assert len(attacks) == 8
    assert attacks["1_datum_is_thing"]["disposition"] == "REFUSED"
    assert attacks["2_bare_asserted_pair_is_thing"]["disposition"] == "REFUSED"
    assert attacks["4_primitive_difference_is_definitionally_the_thing"]["disposition"] == "The local A1i member is retained without renaming; the tied asymmetric member prevents uniqueness."
    assert attacks["8_candidate_list_is_closed_by_narrative"]["status"] == "OPEN"


def test_receipt_is_sorted_timestamp_free_and_replayable() -> None:
    committed = (HERE / "receipts" / "thing.json").read_bytes()
    with tempfile.TemporaryDirectory() as scratch:
        first = Path(scratch) / "one"
        second = Path(scratch) / "two"
        assert run_thing.main(["--artifacts", str(first)]) == 0
        assert run_thing.main(["--artifacts", str(second)]) == 0
        first_bytes = (first / "thing.json").read_bytes()
        second_bytes = (second / "thing.json").read_bytes()
    assert first_bytes == second_bytes == committed
    assert b"\r" not in first_bytes
    payload = json.loads(first_bytes)
    assert payload["schema"] == "thinghood-v1"
    assert payload["AuthorityEffect"] == "None"
    assert payload["authority_effect"] == "None"
    assert payload["terminals"] == [
        "THINGHOOD_CHARACTERIZED",
        "THING_COINCIDES_WITH_A1I",
        "THING_STRICTLY_RICHER_THAN_A1I",
        "NO_FORCED_DYNAMICAL_LAW",
        "OB1_UNCHANGED",
        "S66_UNCHANGED",
        "S9_LAST_UNCHANGED",
        "CANDIDATE_SPACE_OPEN",
        "REFUSED",
    ]


if __name__ == "__main__":
    import traceback

    failed = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"PASS {name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {name}: {exc}")
            traceback.print_exc()
    raise SystemExit(failed)
