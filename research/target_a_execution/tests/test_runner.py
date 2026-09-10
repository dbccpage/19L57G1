"""Unit tests for the fixed graph interpreter and parameterized runner."""

import pytest

from runner import (
    Config,
    ExecutionError,
    Refusal,
    Terminal,
    blind_reader,
    check_word,
    eval_word,
    forking_reader,
    iterate_word,
    lookup,
    next_of,
    next_value_of,
    obs_of,
    resume_word,
    run_det_of,
    run_word,
    step_det_of,
    step_word,
)


def test_lookup_success() -> None:
    # Form 3 has edge 0 -> 1 and 1 -> 2
    graph = frozenset({(3, (0, 1)), (3, (1, 2)), (4, (0, 0))})
    assert lookup(3, 0, graph) == 1
    assert lookup(3, 1, graph) == 2
    assert lookup(4, 0, graph) == 0
    assert lookup(3, 2, graph) is None
    assert lookup(5, 0, graph) is None


def test_lookup_ambiguous_edge_refusal() -> None:
    # Ambiguous: two edges leaving datum 0 on form 3
    graph = frozenset({(3, (0, 1)), (3, (0, 2))})
    with pytest.raises(ExecutionError, match="ambiguous graph"):
        lookup(3, 0, graph)


def test_check_word() -> None:
    check_word((0, 1, 2))
    with pytest.raises(ExecutionError, match="negative operation index"):
        check_word((0, -1, 1))


def test_word_machine_step_and_run() -> None:
    # Operation 0: 0 -> 1, 1 -> 2, 2 -> 0 (cycle on 3 elements)
    # Operation 1: constant 0
    graph = frozenset({
        (3, (0, 1)), (3, (1, 2)), (3, (2, 0)),
        (4, (0, 0)), (4, (1, 0)), (4, (2, 0)),
    })
    # Run word [0, 0, 1, 0] starting from active=0
    cfg = Config(graph=graph, word=(0, 0, 1, 0), active=0, output=())
    
    # Step 1: op 0 from 0 -> 1
    s1 = step_word(cfg)
    assert s1 is not None
    assert s1.active == 1
    assert s1.output == (1,)
    assert s1.word == (0, 1, 0)
    
    # Step 2: op 0 from 1 -> 2
    s2 = step_word(s1)
    assert s2 is not None
    assert s2.active == 2
    assert s2.output == (1, 2)
    
    # Full run
    final = run_word(cfg)
    assert final is not None
    assert final.word == ()
    assert final.active == 1  # 0 -> 1 -> 2 -> 0 -> 1
    assert final.output == (1, 2, 0, 1)


def test_word_machine_agreement_with_eval_word() -> None:
    graph = frozenset({
        (3, (0, 1)), (3, (1, 2)), (3, (2, 0)),
        (4, (0, 2)), (4, (1, 1)), (4, (2, 0)),
    })
    word = (0, 1, 0, 0, 1)
    cfg = Config(graph=graph, word=word, active=0, output=())
    res_cfg = run_word(cfg)
    res_eval = eval_word(graph, word, 0)
    assert res_cfg is not None
    assert res_cfg.active == res_eval


def test_word_machine_resume() -> None:
    graph = frozenset({(3, (0, 1)), (3, (1, 2)), (3, (2, 0))})
    cfg = Config(graph=graph, word=(0,), active=0, output=())
    res = run_word(cfg)
    assert res is not None
    assert res.active == 1
    res2 = resume_word(res, (0, 0))
    assert res2 is not None
    assert res2.active == 0
    assert res2.output == (1, 2, 0)


def test_missing_edge_refusal_in_word_machine() -> None:
    # Op 0 missing transition from datum 2
    graph = frozenset({(3, (0, 1)), (3, (1, 2))})
    cfg = Config(graph=graph, word=(0, 0, 0), active=0, output=())
    assert run_word(cfg) is None


# Dummy state for testing generic parameterized runner
class MockState:
    def __init__(self, active: int, fuel: int, tape: tuple[int, ...] = ()):
        self.active = active
        self.fuel = fuel
        self.tape = tape
        self.clock = 0
        self.graph = frozenset({(3, (0, 1)), (3, (1, 2))})


def mock_fire(s: MockState, op: int) -> MockState | Refusal:
    if s.fuel <= 0:
        return Refusal.EXHAUSTED
    if op == 0 and s.active == 0:
        nxt = MockState(active=1, fuel=s.fuel - 1, tape=s.tape + (1,))
        nxt.clock = s.clock + 1
        return nxt
    return Refusal.NO_EDGE


def test_parameterized_runner_terminals() -> None:
    # Blind reader -> HALT
    s = MockState(0, 5)
    assert step_det_of(blind_reader, s, mock_fire) is Terminal.HALT

    # Forking reader -> BRANCH (refuses non-deterministic choice)
    assert step_det_of(forking_reader, s, mock_fire) is Terminal.BRANCH

    # Single op fire
    single_reader = lambda _: (0,)
    nxt = step_det_of(single_reader, s, mock_fire)
    assert isinstance(nxt, MockState)
    assert nxt.active == 1
    assert nxt.fuel == 4

    # Out of fuel
    s_exhausted = MockState(0, 0)
    assert step_det_of(single_reader, s_exhausted, mock_fire) is Terminal.EXHAUSTED

    # Missing edge
    missing_reader = lambda _: (99,)
    assert step_det_of(missing_reader, s, mock_fire) is Terminal.REFUSE


def test_parameterized_runner_run_det_of() -> None:
    s = MockState(0, 10, tape=(0,))
    reader = lambda st: (0,) if st.active == 0 else ()
    term, final_s = run_det_of(reader, 10, s, mock_fire)
    assert term is Terminal.HALT
    assert final_s.active == 1
    assert obs_of(reader, 2, s, mock_fire) == (0, 1)
