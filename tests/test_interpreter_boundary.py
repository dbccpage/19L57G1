"""Tests for the interpreter-boundary mirror (Phase VIII, I0-I5)."""

from __future__ import annotations

from pathlib import Path

import pytest

from derivation.interpreter_boundary import (
    BASIS,
    BROKE_WORLD,
    DUP_WORLD,
    KERNEL_DESC,
    NOTE_EVENT,
    SAT_WORLD,
    TERMINAL_EVIDENCE,
    TERMINALS,
    UNLICENSED_WORLD,
    Desc,
    all_descs,
    basis_report,
    behavior_vector,
    boundary_rel,
    boundary_report,
    candidate_a,
    candidate_f,
    carrier,
    collapse_obstructed,
    diag,
    diagonal_misses_all,
    distinct_on_basis,
    eval_opt,
    event_json,
    index_world,
    interp_step,
    interpreter_report,
    irrefl,
    self_description_on_basis,
)
from derivation.represented import Event, World, replay, step


# ---------------------------------------------------------------------------
# The code family
# ---------------------------------------------------------------------------

def test_family_enumeration() -> None:
    descs = all_descs()
    assert len(descs) == 64
    assert len(set(descs)) == 64
    # Lean order: first field slowest, last fastest, False before True.
    assert descs[0] == Desc(False, False, False, False, False, False)
    assert descs[1] == Desc(False, False, False, False, False, True)
    assert descs[32] == Desc(True, False, False, False, False, False)
    assert descs[63] == KERNEL_DESC
    assert KERNEL_DESC.json()["dedup_admit"] is True


# ---------------------------------------------------------------------------
# The family evaluator: kernel = sealed step (interp_describe mirror)
# ---------------------------------------------------------------------------

FULL_KIND_HISTORY: list[Event] = [
    ("setBudget", 3),
    ("admit", 0), ("admit", 1), ("admit", 0),      # fresh + dup
    ("require", 0, 1), ("require", 0, 0),          # ok + rejected
    ("addView", (0,)),                             # accepted
    ("mark", (0,), 1),                             # rejected (satisfied)
    ("refuse", 0, 1),                              # rejected (no cert)
    ("note", 7), ("setAugLicense", False),
    ("addView", (1,)),                             # rejected (license)
]


def test_kernel_matches_sealed_step_eventwise() -> None:
    w = World()
    for e in FULL_KIND_HISTORY:
        assert interp_step(KERNEL_DESC, w, e) == step(w, e)
        w = step(w, e)


def test_kernel_matches_sealed_step_on_basis() -> None:
    assert self_description_on_basis()
    for (_, w, e) in BASIS:
        assert interp_step(KERNEL_DESC, w, e) == step(w, e)


def test_each_toggle_load_bearing_on_its_probe() -> None:
    """Mirror of the six Initiality separations: switching one guard
    off changes the outcome on exactly that guard's probe."""
    for k, (name, w, e) in enumerate(BASIS):
        off = Desc(*(i != k for i in range(6)))
        assert getattr(off, name) is False
        assert interp_step(off, w, e) != interp_step(KERNEL_DESC, w, e)


def test_ungated_branches_fire() -> None:
    # dedup off: repeat admission appends a second occurrence
    no_dedup = Desc(False, True, True, True, True, True)
    assert interp_step(no_dedup, DUP_WORLD, ("admit", 5)).data == (5, 5)
    # require guard off: ill-formed requirement is recorded
    no_req = Desc(True, False, True, True, True, True)
    assert (0, 0) in interp_step(no_req, DUP_WORLD, ("require", 0, 0)).reqs
    # budget gate off at zero budget: fires, budget truncates at 0
    no_budget = Desc(True, True, True, False, True, True)
    fired = interp_step(no_budget, BROKE_WORLD, ("mark", (), 0))
    assert fired.views == ((0,),) and fired.budget == 0
    # license gate off: unlicensed augmentation fires
    no_license = Desc(True, True, True, True, False, True)
    aug = interp_step(no_license, UNLICENSED_WORLD, ("addView", (0,)))
    assert (0,) in aug.views and aug.budget == 8
    # refusal certificate off: uncertified refusal is recorded
    no_cert = Desc(True, True, True, True, True, False)
    assert (0, 1) in interp_step(no_cert, SAT_WORLD, ("refuse", 0, 1)).refusals
    # ... but never twice (dedup of refusals is outside the toggle)
    refused = interp_step(no_cert, SAT_WORLD, ("refuse", 0, 1))
    assert interp_step(no_cert, refused, ("refuse", 0, 1)) == refused


def test_state_events_unconditional() -> None:
    for d in (KERNEL_DESC, Desc(False, False, False, False, False, False)):
        assert interp_step(d, DUP_WORLD, ("note", 4)).notes == (4,)
        assert interp_step(d, DUP_WORLD, ("setBudget", 2)).budget == 2
        assert interp_step(
            d, DUP_WORLD, ("setAugLicense", False)
        ).aug_licensed is False


def test_malformed_event_rejected() -> None:
    with pytest.raises(AssertionError):
        interp_step(KERNEL_DESC, DUP_WORLD, ("admit", -1))


# ---------------------------------------------------------------------------
# Pairwise distinctness on the declared basis
# ---------------------------------------------------------------------------

def test_all_64_behaviorally_distinct_on_basis() -> None:
    assert distinct_on_basis() == 64
    vectors = [behavior_vector(d) for d in all_descs()]
    assert len(set(vectors)) == len(vectors)


def test_truncated_basis_fails_to_separate() -> None:
    """Negative control: the basis is load-bearing — one probe alone
    separates only its own toggle (2 classes, not 64)."""
    assert distinct_on_basis(BASIS[:1]) == 2
    assert distinct_on_basis(BASIS[:2]) == 4


# ---------------------------------------------------------------------------
# The diagonal (tower_persists mirror)
# ---------------------------------------------------------------------------

def test_diagonal_misses_every_member_exhaustively() -> None:
    descs = all_descs()
    assert diagonal_misses_all(lambda w, e: diag(descs, w, e), descs)
    # spot-check the mechanism: the diagonal differs exactly by the
    # extended transition-inert notes at the indexed world
    for i in (0, 31, 63):
        wi = index_world(i)
        member = interp_step(descs[i], wi, NOTE_EVENT)
        assert diag(descs, wi, NOTE_EVENT).notes == member.notes + (999,)


def test_diagonal_out_of_range_inert() -> None:
    descs = all_descs()
    w64 = index_world(64)
    assert diag(descs, w64, NOTE_EVENT) == w64


def test_fake_diagonal_copying_a_member_is_caught() -> None:
    """Negative control: a 'diagonal' that merely re-evaluates some
    member agrees with that member at its indexed world."""
    descs = all_descs()
    for k in (0, 63):
        fake = (
            lambda w, e, k=k: interp_step(descs[k], w, e)
        )
        assert not diagonal_misses_all(fake, descs)


def test_index_world_lengths() -> None:
    for i in (0, 1, 7, 64):
        assert len(index_world(i).data) == i


# ---------------------------------------------------------------------------
# The typed-refusal evaluator
# ---------------------------------------------------------------------------

def test_partial_top_refuses_and_coded_members_evaluate() -> None:
    assert eval_opt(None, DUP_WORLD, NOTE_EVENT) is None
    for (_, w, e) in BASIS:
        assert eval_opt(None, w, e) is None
        assert eval_opt(KERNEL_DESC, w, e) == step(w, e)
    all_off = Desc(False, False, False, False, False, False)
    assert eval_opt(all_off, DUP_WORLD, ("admit", 5)) != step(
        DUP_WORLD, ("admit", 5)
    )


# ---------------------------------------------------------------------------
# The boundary setting
# ---------------------------------------------------------------------------

def test_carrier_and_witness() -> None:
    xs = carrier()
    assert len(xs) == 65
    assert xs.count(None) == 1
    assert boundary_rel(KERNEL_DESC, None)
    assert not boundary_rel(None, KERNEL_DESC)
    assert not boundary_rel(KERNEL_DESC, KERNEL_DESC)


def test_candidates_a_and_f() -> None:
    assert candidate_a()
    assert candidate_f()
    assert irrefl(boundary_rel, carrier())


def test_irrefl_check_catches_reflexive_relation() -> None:
    """Negative control: the irreflexivity checker is not vacuous."""
    assert not irrefl(lambda x, y: x is None and y is None, carrier())


def test_collapse_obstruction() -> None:
    # constant map identifies the endpoints: obstructed
    assert collapse_obstructed(lambda _x: 0)
    # a map keeping the endpoints apart is NOT an identification
    assert not collapse_obstructed(
        lambda x: 0 if x == KERNEL_DESC else 1
    )


# ---------------------------------------------------------------------------
# Reports and the artifact
# ---------------------------------------------------------------------------

def test_event_json_shapes() -> None:
    assert event_json(("mark", (0,), 1)) == ["mark", [0], 1]
    assert event_json(("setAugLicense", False)) == ["setAugLicense", False]


def test_basis_report_names_match_toggles() -> None:
    names = [row["name"] for row in basis_report()]
    assert names == [
        "dedup_admit", "guard_require", "guard_accept",
        "gate_budget", "gate_license", "cert_refusal",
    ]


def test_interpreter_report_payload() -> None:
    payload = interpreter_report()
    assert payload["family_size"] == 64
    assert payload["behaviorally_distinct_on_basis"] == 64
    assert payload["self_description_on_basis"] is True
    assert payload["diagonal_misses_all"] is True
    assert payload["partial_top"] == "REFUSES"
    boundary = payload["boundary_setting"]
    assert isinstance(boundary, dict)
    assert boundary["occurrences"] == 65
    assert boundary["candidates"] == {"A": True, "F": True}
    assert boundary["retention_protection"] == "DECLARED"
    assert boundary["collapse_obstructed"] is True
    assert payload["terminals"] == list(TERMINALS)
    assert set(payload["terminal_evidence"]) == set(TERMINAL_EVIDENCE)  # type: ignore[arg-type]
    # absolute no-outside is NOT claimed
    assert "NO_OUTSIDE" not in str(payload["terminals"])


def test_boundary_report_deterministic() -> None:
    assert boundary_report() == boundary_report()


def test_runner_byte_stable(tmp_path: Path) -> None:
    import run_interpreter_boundary

    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_interpreter_boundary.main(["--artifacts", str(d1)]) == 0
    assert run_interpreter_boundary.main(["--artifacts", str(d2)]) == 0
    b1 = (d1 / "primitive_interpreter.json").read_bytes()
    b2 = (d2 / "primitive_interpreter.json").read_bytes()
    assert b1 == b2


def test_runner_matches_committed_artifact(tmp_path: Path) -> None:
    committed = Path("artifacts") / "primitive_interpreter.json"
    if not committed.exists():  # pragma: no cover - first generation
        pytest.skip("artifact not yet generated")
    import run_interpreter_boundary

    assert run_interpreter_boundary.main(
        ["--artifacts", str(tmp_path)]) == 0
    fresh = (tmp_path / "primitive_interpreter.json").read_bytes()
    assert fresh == committed.read_bytes()


# ---------------------------------------------------------------------------
# Replay grounding: the mirror rides the sealed kernel, not a copy
# ---------------------------------------------------------------------------

def test_kernel_desc_tracks_replay_from_genesis() -> None:
    hist: list[Event] = [("setBudget", 2), ("admit", 0), ("admit", 1),
                         ("require", 0, 1), ("addView", (0,))]
    w_kernel = World()
    for e in hist:
        w_kernel = interp_step(KERNEL_DESC, w_kernel, e)
    assert w_kernel == replay(hist)
