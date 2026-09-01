"""Tests for the nine-slot inventory of existing objects."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import run_observer_inventory
from derivation.observer_inventory import (
    NAMED_ELSEWHERE,
    SLOTS,
    as_json,
    defect_report,
    edge_count,
    inventory_report,
    irrefl_census_on_two,
    is_sym_bit,
    local_states,
    residuals_report,
    reversal_report,
    witnesses_report,
)
from derivation.primdiff import D2, D2_REV, S2


def test_nine_slots_and_no_duplicates() -> None:
    assert len(SLOTS) == 9
    assert len(set(SLOTS)) == 9
    assert SLOTS == (
        "carrier",
        "local_state",
        "support",
        "defect",
        "reversal",
        "closure",
        "residual",
        "maps",
        "terminal",
    )


def test_irrefl_census_is_exactly_the_four() -> None:
    states = local_states()
    assert states["empty"] == frozenset()
    assert states["D2"] == D2.rel
    assert states["D2rev"] == D2_REV.rel
    assert states["S2"] == S2.rel
    census = irrefl_census_on_two()
    assert census["count"] == 4
    assert census["are_exactly_the_four"] is True
    assert census["names"] == ["D2", "D2rev", "S2", "empty"]


def test_witnesses_are_data_not_a_unique_inhabitant() -> None:
    rep = witnesses_report()
    assert rep["zero_ne_one"] is True
    assert rep["one_forward"] is True
    assert rep["one_reverse"] is True
    assert rep["zero_presence_empty"] is True
    assert rep["one_presence_is_D2"] is True


def test_reversal_transpose_and_swap_agree_on_D2_and_differ() -> None:
    rep = reversal_report()
    assert all(rep[k] is True for k in rep)


def test_defect_collision_is_not_source_irreflexivity() -> None:
    rep = defect_report()
    assert rep["D2_collides_under_merge"] is True
    assert rep["S2_collides_under_merge"] is True
    assert rep["empty_does_not_collide_under_merge"] is True
    assert rep["unit_self_loop_not_irreflexive"] is True
    assert rep["source_D2_still_irreflexive"] is True


def test_residuals_are_not_unique() -> None:
    assert edge_count(D2.rel) == 1
    assert edge_count(S2.rel) == 2
    assert is_sym_bit(D2.rel) == 0
    assert is_sym_bit(S2.rel) == 1
    assert is_sym_bit(D2_REV.rel) == 0
    assert is_sym_bit(frozenset()) == 0
    rep = residuals_report()
    assert rep["edge_count_D2"] == 1
    assert rep["edge_count_S2"] == 2
    assert rep["is_sym_bit_D2"] == 0
    assert rep["is_sym_bit_S2"] == 1
    assert rep["residuals_disagree_on_D2"] is True


def test_named_elsewhere_is_a_string_table() -> None:
    assert "carrier" in NAMED_ELSEWHERE
    assert "witness" in NAMED_ELSEWHERE
    for vals in NAMED_ELSEWHERE.values():
        assert vals
        assert all(isinstance(v, str) and v for v in vals)


def _derivation_lean_source() -> str:
    root = Path(__file__).resolve().parents[1] / "lean4" / "Derivation"
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*.lean"))
    )


def _declared_in_source(source: str, name: str) -> bool:
    """A citation `A.B.x` declared inside `namespace A.B` appears in the
    source under some dotted suffix, so every suffix is a candidate
    spelling (the trick used by the natural-sections resolution test).
    Declarations are `theorem`/`def`/`inductive`/`structure`/`abbrev`
    followed by the name and a space; a structure field appears as an
    indented `name :` line."""
    parts = name.split(".")
    candidates = [".".join(parts[i:]) for i in range(len(parts))]
    for candidate in candidates:
        for keyword in ("theorem", "def", "inductive", "structure", "abbrev"):
            if f"{keyword} {candidate} " in source:
                return True
        if re.search(rf"(?m)^\s+{re.escape(candidate)} :", source):
            return True
    return False


def test_every_named_elsewhere_citation_is_declared_in_the_source() -> None:
    """Mutation: rename or fabricate any NAMED_ELSEWHERE string and this
    fails naming the string."""
    source = _derivation_lean_source()
    for vals in NAMED_ELSEWHERE.values():
        for name in vals:
            assert _declared_in_source(source, name), name


def test_fabricated_named_elsewhere_string_does_not_resolve() -> None:
    source = _derivation_lean_source()
    assert not _declared_in_source(source, "PrimDiff.zzz_probe_missing")


# Digest of the vocabulary-refusal record in
# paper/observer_inventory.md §1.  The refusal is an author ruling;
# rewording or removing it must be a deliberate act that updates this
# pin, mirroring the ledger body pin.
REFUSAL_MARKER = "**[declared metatheory] — provenance and refusal.**"
REFUSAL_PIN = (
    "9075ade86f7220b49d691ef0b729b224bae7a0e85adb9a53e3c28085d03aa2b1"
)


def test_vocabulary_refusal_record_is_present_and_pinned() -> None:
    paper = Path(__file__).resolve().parents[1] / "paper"
    lines = (paper / "observer_inventory.md").read_text(
        encoding="utf-8"
    ).splitlines()
    starts = [
        i for i, line in enumerate(lines) if line.startswith(REFUSAL_MARKER)
    ]
    assert len(starts) == 1, "exactly one refusal record expected"
    end = starts[0]
    while end < len(lines) and lines[end].strip():
        end += 1
    para = "\n".join(lines[starts[0]:end])
    digest = hashlib.sha256(para.encode("utf-8")).hexdigest()
    assert digest == REFUSAL_PIN, (
        "the vocabulary-refusal record drifted; if the change is a "
        "deliberate author act, update REFUSAL_PIN"
    )


def test_inventory_report_flags() -> None:
    payload = inventory_report()
    assert payload["slot_count"] == 9
    assert payload["empty_ne_D2"] is True
    assert payload["witnesses_not_derived_as_necessary"] is True
    bindings = payload["bindings"]
    assert isinstance(bindings, dict)
    assert set(bindings) == set(SLOTS)
    copied = as_json(payload)
    assert copied["slot_count"] == 9


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_observer_inventory.main(["--artifacts", str(d1)]) == 0
    assert run_observer_inventory.main(["--artifacts", str(d2)]) == 0
    p1 = d1 / "observer_inventory.json"
    p2 = d2 / "observer_inventory.json"
    assert p1.read_bytes() == p2.read_bytes()
    payload = json.loads(p1.read_text(encoding="utf-8"))
    assert payload["irrefl_census"]["are_exactly_the_four"] is True
    assert payload["reversal"]["operations_differ_on_self_loop"] is True
    assert payload["witnesses"]["one_presence_is_D2"] is True
