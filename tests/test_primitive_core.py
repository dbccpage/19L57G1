"""Tests for the primitive-difference candidate-lattice enumerators."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import cast

import pytest

from derivation.primitive_core import (
    CANDIDATES,
    EXPECTED_MATRIX,
    EXPECTED_OPEN,
    ScanResult,
    Setting,
    candidates_payload,
    cell_names,
    closure,
    compose,
    cotransitive,
    decoration_rel,
    enumerate_base,
    enumerate_settings,
    evaluate,
    matrix_report,
    ops_family,
    presentation_branching,
    scan_settings,
    two_element_classification,
    witness_key,
)

import run_primitive_core


@pytest.fixture(scope="module")
def scan() -> ScanResult:
    return scan_settings()


def bare(n: int, r: frozenset[tuple[int, int]], a: int, b: int) -> Setting:
    return Setting(n, r, a, b, frozenset(), frozenset(), frozenset())


# ---------------------------------------------------------------------------
# Enumeration and evaluators
# ---------------------------------------------------------------------------


def test_enumeration_counts() -> None:
    # Base: 2^(n*n) relations times n*n point pairs; 12 decorations.
    assert sum(1 for _ in enumerate_base(1)) == 2
    assert sum(1 for _ in enumerate_base(2)) == (1 << 4) * 4
    assert sum(1 for _ in enumerate_base(3)) == (1 << 9) * 9
    total = sum(1 for _ in enumerate_settings())
    assert total == (2 + 64 + 4608) * 12 == 56088


def test_decoration_helpers() -> None:
    assert decoration_rel("empty", 0, 1) == frozenset()
    assert decoration_rel("designated_pair", 0, 1) == frozenset({(0, 1)})
    assert ops_family("empty", 2) == frozenset()
    assert ops_family("identity", 2) == frozenset({(0, 1)})
    assert ops_family("const_0", 3) == frozenset({(0, 0, 0)})
    with pytest.raises(ValueError):
        decoration_rel("bogus", 0, 1)
    with pytest.raises(ValueError):
        ops_family("bogus", 2)


def test_evaluate_one_point_self_witness() -> None:
    s = bare(1, frozenset({(0, 0)}), 0, 0)
    preds = evaluate(s)
    assert preds["W"] is True
    assert preds["A"] is False and preds["Bl"] is False
    assert preds["D"] is False and preds["E"] is False
    assert preds["C"] is False and preds["F"] is False
    protected = dataclasses.replace(s, prot=frozenset({(0, 0)}))
    assert evaluate(protected)["C"] is True


def test_evaluate_oriented_and_symmetric() -> None:
    oriented = bare(2, frozenset({(0, 1)}), 0, 1)
    preds = evaluate(oriented)
    assert preds["A"] and preds["Bl"] and preds["Bc"] and preds["D"]
    assert preds["E"]  # empty ops: closure is {identity}
    assert not preds["Bs"] and not preds["C"] and not preds["F"]
    sym = bare(2, frozenset({(0, 1), (1, 0)}), 0, 1)
    assert evaluate(sym)["Bs"] is True
    full = dataclasses.replace(
        oriented, ret=frozenset({(0, 1)}), prot=frozenset({(0, 1)})
    )
    fp = evaluate(full)
    assert fp["F"] and fp["C"]


def test_evaluate_cotransitivity_carrier_three() -> None:
    # The oriented edge stops being cotransitive on carrier 3: the
    # third point splits nothing.
    assert cotransitive(2, frozenset({(0, 1)})) is True
    assert cotransitive(3, frozenset({(0, 1)})) is False
    assert cotransitive(3, frozenset({(0, 1), (1, 0)})) is False
    off_diagonal = frozenset(
        (x, y) for x in range(3) for y in range(3) if x != y
    )
    assert cotransitive(3, off_diagonal) is True
    assert evaluate(bare(3, frozenset({(0, 1)}), 0, 1))["Bc"] is False


def test_evaluate_irreducibility_ops() -> None:
    oriented = bare(2, frozenset({(0, 1)}), 0, 1)
    with_id = dataclasses.replace(oriented, ops=frozenset({(0, 1)}))
    with_const = dataclasses.replace(oriented, ops=frozenset({(0, 0)}))
    assert evaluate(with_id)["E"] is True
    assert evaluate(with_const)["E"] is False


def test_closure_nontrivial_composition() -> None:
    # swap . const_0 = const_1: composition generates a table not in
    # the generating family.
    swap = (1, 0)
    const0 = (0, 0)
    assert compose(swap, const0) == (1, 1)
    cl = closure(2, [swap, const0])
    assert cl == frozenset({(0, 1), (1, 0), (0, 0), (1, 1)})
    # A 3-cycle generates the cyclic monoid of order 3.
    cyc = (1, 2, 0)
    cl3 = closure(3, [cyc])
    assert cl3 == frozenset({(0, 1, 2), (1, 2, 0), (2, 0, 1)})
    # Empty family: the closure is exactly the identity.
    assert closure(3, []) == frozenset({(0, 1, 2)})


# ---------------------------------------------------------------------------
# The implication matrix
# ---------------------------------------------------------------------------


def test_expected_matrix_shape() -> None:
    assert len(CANDIDATES) == 9
    assert len(cell_names()) == 72
    assert sorted(EXPECTED_MATRIX) == sorted(cell_names())
    statuses = list(EXPECTED_MATRIX.values())
    assert statuses.count("IMPLIES") == 17
    assert statuses.count("COUNTERMODEL") == 51
    assert statuses.count("OPEN_LOCATED") == 4
    assert EXPECTED_OPEN == {"A->Bl", "Bs->Bl", "Bc->Bl", "F->Bl"}
    # Spot-check the load-bearing rows.
    assert EXPECTED_MATRIX["A->D"] == "IMPLIES"
    assert EXPECTED_MATRIX["E->D"] == "IMPLIES"
    assert EXPECTED_MATRIX["F->C"] == "IMPLIES"
    assert EXPECTED_MATRIX["W->D"] == "COUNTERMODEL"
    assert EXPECTED_MATRIX["D->E"] == "COUNTERMODEL"
    assert EXPECTED_MATRIX["A->Bc"] == "COUNTERMODEL"
    assert EXPECTED_MATRIX["A->Bl"] == "OPEN_LOCATED"


def test_every_matrix_cell_status(scan: ScanResult) -> None:
    report = matrix_report(scan)
    cells = report["cells"]
    assert isinstance(cells, dict)
    assert sorted(cells) == sorted(cell_names())
    assert report["expected_equals_computed"] is True
    for cell in cell_names():
        entry = cells[cell]
        assert entry["status"] == EXPECTED_MATRIX[cell]
        p, q = cell.split("->")
        witness = scan.witnesses[cell]
        if EXPECTED_MATRIX[cell] == "COUNTERMODEL":
            assert entry["search"] == "COUNTERMODEL"
            assert entry["lean"] == f"nimp_{p.lower()}_{q.lower()}"
            assert witness is not None
            # Independent re-evaluation of the witness.
            preds = evaluate(witness)
            assert preds[p] is True and preds[q] is False
            assert entry["witness"] == witness.json()
        else:
            assert entry["search"] == "NO_COUNTERMODEL_IN_BOUNDS"
            assert witness is None and entry["witness"] is None
            if EXPECTED_MATRIX[cell] == "IMPLIES":
                assert entry["lean"] == f"imp_{p.lower()}_{q.lower()}"
            else:
                assert cell in EXPECTED_OPEN and q == "Bl"
                assert entry["lean"] == f"open_cell_{p.lower()}_bl"


def test_a_bc_minimal_countermodel_is_carrier_three(
    scan: ScanResult,
) -> None:
    w = scan.witnesses["A->Bc"]
    assert w is not None
    assert w.n == 3
    assert w.r == frozenset({(0, 1)}) and (w.a, w.b) == (0, 1)
    assert scan.cotrans_violation_le2 is False
    # Independent sub-bound check: cotransitivity is automatic for A
    # at carriers 1 and 2 (decorations are irrelevant to A and Bc).
    for n in (1, 2):
        for r, a, b in enumerate_base(n):
            preds = evaluate(bare(n, r, a, b))
            if preds["A"]:
                assert preds["Bc"]
    report = matrix_report(scan)
    minimality = report["minimality_assertions"]
    assert isinstance(minimality, dict)
    assert "cotrans_auto_on_two" in minimality["A->Bc"]


def test_witness_minimality_spot_checks(scan: ScanResult) -> None:
    w = scan.witnesses

    def js(cell: str) -> dict[str, object]:
        s = w[cell]
        assert s is not None
        return s.json()

    one_point = {
        "n": 1, "r": [[0, 0]], "a": 0, "b": 0,
        "ret": [], "prot": [], "ops": [],
    }
    assert js("W->A") == one_point
    assert js("W->D") == one_point
    assert js("A->Bs") == {
        "n": 2, "r": [[0, 1]], "a": 0, "b": 1,
        "ret": [], "prot": [], "ops": [],
    }
    assert js("Bc->Bs") == js("A->Bs")
    assert js("Bs->Bc") == {
        "n": 3, "r": [[0, 1], [1, 0]], "a": 0, "b": 1,
        "ret": [], "prot": [], "ops": [],
    }
    protected_point = {
        "n": 1, "r": [[0, 0]], "a": 0, "b": 0,
        "ret": [], "prot": [[0, 0]], "ops": [],
    }
    assert js("C->A") == protected_point
    assert js("C->D") == protected_point
    # The D->E and A->E countermodels need the admitted constant map.
    assert js("D->E") == {
        "n": 2, "r": [], "a": 0, "b": 1,
        "ret": [], "prot": [], "ops": [[0, 0]],
    }
    assert js("A->E")["ops"] == [[0, 0]]
    assert js("E->W") == {
        "n": 2, "r": [], "a": 0, "b": 1,
        "ret": [], "prot": [], "ops": [],
    }
    assert js("F->E")["ops"] == [[0, 0]]
    fbc = w["F->Bc"]
    assert fbc is not None and fbc.n == 3


def test_witness_key_orders_declared_components() -> None:
    small = bare(2, frozenset({(0, 1)}), 0, 1)
    large = bare(3, frozenset({(0, 1)}), 0, 1)
    decorated = dataclasses.replace(small, ret=frozenset({(0, 1)}))
    assert witness_key(small) < witness_key(large)
    assert witness_key(small) < witness_key(decorated)


def test_candidate_counts(scan: ScanResult) -> None:
    counts = scan.counts
    assert scan.total == 56088
    # Hand-derived extents (decorations multiply base counts by 12
    # unless the candidate constrains them).
    assert counts["W"] == 28044  # half of all settings
    assert counts["A"] == 2352  # (4 + 192) * 12
    assert counts["Bl"] == counts["A"]  # located automatic finitely
    assert counts["Bs"] == 312  # (2 + 24) * 12
    assert counts["C"] == 14022  # W and prot fixed to designated
    assert counts["D"] == 37248  # (32 + 3072) * 12
    assert counts["E"] == 24832  # a != b, ops without const_0
    assert counts["F"] == 588  # 196 * 3 (ret, prot fixed)
    assert counts["Bc"] == 1272  # computed; decoration-free base 106
    assert counts["Bc"] % 12 == 0
    assert counts["Bs"] < counts["Bc"] < counts["A"] < counts["W"]


# ---------------------------------------------------------------------------
# Negative tests: a wrong expected table raises
# ---------------------------------------------------------------------------


def test_wrong_expected_entry_raises(scan: ScanResult) -> None:
    # A true implication downgraded to COUNTERMODEL: no witness exists.
    wrong = {**EXPECTED_MATRIX, "A->D": "COUNTERMODEL"}
    with pytest.raises(ValueError, match="A->D"):
        matrix_report(scan, expected=wrong)
    # A refuted cell upgraded to IMPLIES: the search has a witness.
    wrong = {**EXPECTED_MATRIX, "W->A": "IMPLIES"}
    with pytest.raises(ValueError, match="W->A"):
        matrix_report(scan, expected=wrong)
    # An unknown status label.
    wrong = {**EXPECTED_MATRIX, "A->D": "SOMETIMES"}
    with pytest.raises(ValueError, match="unknown status"):
        matrix_report(scan, expected=wrong)
    # OPEN_LOCATED outside the declared OPEN set (witness-free cell).
    wrong = {**EXPECTED_MATRIX, "A->D": "OPEN_LOCATED"}
    with pytest.raises(ValueError, match="outside the declared"):
        matrix_report(scan, expected=wrong)
    # A declared-OPEN cell downgraded to IMPLIES.
    wrong = {**EXPECTED_MATRIX, "A->Bl": "IMPLIES"}
    with pytest.raises(ValueError, match="declared OPEN"):
        matrix_report(scan, expected=wrong)
    # A declared-OPEN cell claimed as COUNTERMODEL: none exists.
    wrong = {**EXPECTED_MATRIX, "A->Bl": "COUNTERMODEL"}
    with pytest.raises(ValueError, match="none found"):
        matrix_report(scan, expected=wrong)
    # A missing cell.
    incomplete = dict(EXPECTED_MATRIX)
    del incomplete["A->D"]
    with pytest.raises(ValueError, match="72"):
        matrix_report(scan, expected=incomplete)
    # A declared OPEN set not targeting Bl.
    with pytest.raises(ValueError, match="does not target Bl"):
        matrix_report(scan, expected_open=frozenset({"A->C"}))
    # A declared OPEN set missing a Bl cell the table marks OPEN.
    with pytest.raises(ValueError, match="F->Bl"):
        matrix_report(
            scan,
            expected_open=frozenset({"A->Bl", "Bs->Bl", "Bc->Bl"}),
        )


def test_doctored_scan_raises(scan: ScanResult) -> None:
    # A fabricated witness on a declared-OPEN cell must be rejected.
    fake_open = dataclasses.replace(
        scan,
        witnesses={**scan.witnesses, "A->Bl": scan.witnesses["A->Bs"]},
    )
    with pytest.raises(ValueError, match="A->Bl"):
        matrix_report(fake_open)
    # A fabricated carrier-2 witness for A->Bc must be rejected.
    fake_abc = dataclasses.replace(
        scan,
        witnesses={**scan.witnesses, "A->Bc": scan.witnesses["A->Bs"]},
    )
    with pytest.raises(ValueError, match="carrier 3"):
        matrix_report(fake_abc)
    # A claimed sub-bound cotransitivity violation must be rejected.
    fake_flag = dataclasses.replace(scan, cotrans_violation_le2=True)
    with pytest.raises(ValueError, match="automatic"):
        matrix_report(fake_flag)


# ---------------------------------------------------------------------------
# Two-element classification and presentation branching
# ---------------------------------------------------------------------------


def test_two_element_classification() -> None:
    payload = two_element_classification()
    assert payload["survivor_count"] == 2
    survivors = payload["survivors"]
    assert isinstance(survivors, list)
    assert survivors[0] == {"label": "oriented", "r": [[0, 1]]}
    assert survivors[1] == {
        "label": "symmetric",
        "r": [[0, 1], [1, 0]],
    }
    assert payload["lean"] == "bool_irrefl_witness_classification"
    with pytest.raises(ValueError, match="two-element"):
        two_element_classification(
            expected_survivors=(frozenset({(0, 1)}),)
        )


def test_presentation_branching() -> None:
    payload = presentation_branching()
    assert payload["faithful_surjection_count"] == 10
    assert payload["kernel_class_count"] == 3
    classes = payload["kernel_classes"]
    assert isinstance(classes, list)
    assert [c["map_count"] for c in classes] == [6, 2, 2]
    assert classes[0]["partition"] == [[0], [1], [2]]
    # Honest count: of the three two-block partitions, {0,1}|{2}
    # merges the designated edge; exactly two faithful maximal-coarse
    # kernel classes remain.
    assert payload["two_block_partitions_total"] == 3
    assert payload["unfaithful_two_block_partitions"] == [[[0, 1], [2]]]
    assert payload["maximal_coarse_class_count"] == 2
    assert payload["maximal_coarse_partitions"] == [
        [[0], [1, 2]],
        [[0, 2], [1]],
    ]
    assert payload["no_weakly_terminal"] is True
    with pytest.raises(ValueError, match="maximal-coarse"):
        presentation_branching(
            expected_maximal=(((0,), (1,), (2,)),)
        )


def test_candidates_payload_assembly(scan: ScanResult) -> None:
    payload = candidates_payload(scan)
    bounds = payload["bounds"]
    assert isinstance(bounds, dict)
    assert bounds["settings_enumerated"] == 56088
    assert bounds["ops_choices"] == ["empty", "identity", "const_0"]
    assert payload["bl_equals_a_in_finite_universe"] is True
    note = payload["bl_note"]
    assert isinstance(note, str) and "located_of_decidable" in note
    assert payload["candidate_counts"] == scan.counts


# ---------------------------------------------------------------------------
# Runner determinism
# ---------------------------------------------------------------------------


def test_run_primitive_core_byte_stable(tmp_path: Path) -> None:
    out1 = tmp_path / "artifacts1"
    out2 = tmp_path / "artifacts2"
    assert run_primitive_core.main(["--artifacts", str(out1)]) == 0
    assert run_primitive_core.main(["--artifacts", str(out2)]) == 0
    for name in (
        "primitive_candidates.json",
        "primitive_implication_matrix.json",
    ):
        b1 = (out1 / name).read_bytes()
        b2 = (out2 / name).read_bytes()
        assert b1 == b2
    candidates = json.loads(
        (out1 / "primitive_candidates.json").read_text(encoding="utf-8")
    )
    assert candidates["bounds"]["settings_enumerated"] == 56088
    matrix = json.loads(
        (out1 / "primitive_implication_matrix.json").read_text(
            encoding="utf-8"
        )
    )
    assert matrix["expected_equals_computed"] is True
    assert matrix["status_counts"] == {
        "COUNTERMODEL": 51,
        "IMPLIES": 17,
        "OPEN_LOCATED": 4,
    }
    assert matrix["open_cells"] == sorted(EXPECTED_OPEN)
    cell = matrix["cells"]["A->Bc"]
    assert cell["witness"]["n"] == 3
    minimality = cast(
        "dict[str, str]", matrix["minimality_assertions"]
    )
    assert minimality["A->Bc"] == (
        "carrier 3 minimum, cotransitivity automatic at 2 "
        "(Lean cotrans_auto_on_two)"
    )
