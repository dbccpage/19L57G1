"""Unit tests for CFG branching, jump tables, and fork refusal."""

from branch import (
    CFGBuilder,
    CFGState,
    get_cfg_successors,
    init_cfg,
    resolve_jump_table_target,
    run_cfg,
    step_cfg,
)
from runner import Terminal


def test_cfg_sequential_steps() -> None:
    # 0 -> 1 -> 2 -> 3
    builder = CFGBuilder()
    builder.add_step(0, 1).add_step(1, 2).add_step(2, 3)
    graph = builder.to_graph()

    state = init_cfg(graph, start_pc=0, initial_data=0, fuel=10)
    term, final_s = run_cfg(10, state)

    assert term is Terminal.HALT
    assert final_s.pc == 3
    assert final_s.clock == 3
    assert final_s.fuel == 7
    assert final_s.history == ((0, 0), (1, 0), (2, 0), (3, 0))


def test_cfg_conditional_if_then_else() -> None:
    # From PC 0: if data == 1 go to PC 10 (then), if data == 0 go to PC 20 (else)
    builder = CFGBuilder()
    builder.add_if_then_else(pc=0, true_target=10, false_target=20)
    builder.add_step(10, 100)
    builder.add_step(20, 200)
    graph = builder.to_graph()

    # Case 1: data = 1 -> jumps to 10 -> 100 -> halt
    s_true = init_cfg(graph, start_pc=0, initial_data=1, fuel=10)
    term_true, final_true = run_cfg(10, s_true)
    assert term_true is Terminal.HALT
    assert final_true.pc == 100
    assert final_true.history == ((0, 1), (10, 1), (100, 1))

    # Case 2: data = 0 -> jumps to 20 -> 200 -> halt
    s_false = init_cfg(graph, start_pc=0, initial_data=0, fuel=10)
    term_false, final_false = run_cfg(10, s_false)
    assert term_false is Terminal.HALT
    assert final_false.pc == 200
    assert final_false.history == ((0, 0), (20, 0), (200, 0))


def test_cfg_jump_table() -> None:
    # Indirect jump at PC 0 via table 1
    # Table 1: index 0 -> 10, index 1 -> 20, index 2 -> 30
    builder = CFGBuilder()
    builder.add_jump_table(table_id=1, targets=(10, 20, 30))
    builder.add_indirect_jump(pc=0, table_id=1)
    graph = builder.to_graph()

    # Index 0
    s0 = init_cfg(graph, start_pc=0, initial_data=0, fuel=5)
    term0, final0 = run_cfg(5, s0)
    assert term0 is Terminal.HALT
    assert final0.pc == 10

    # Index 2
    s2 = init_cfg(graph, start_pc=0, initial_data=2, fuel=5)
    term2, final2 = run_cfg(5, s2)
    assert term2 is Terminal.HALT
    assert final2.pc == 30

    # Index 3 (out of bounds) -> no target -> halt
    s3 = init_cfg(graph, start_pc=0, initial_data=3, fuel=5)
    assert step_cfg(s3) is Terminal.HALT


def test_cfg_non_deterministic_fork_refusal() -> None:
    # Ambiguous branch: at PC 0 with data 1, two branches are declared: target 10 and target 20
    builder = CFGBuilder()
    builder.add_branch(pc=0, cond_val=1, target_pc=10)
    builder.add_branch(pc=0, cond_val=1, target_pc=20)
    graph = builder.to_graph()

    state = init_cfg(graph, start_pc=0, initial_data=1, fuel=10)
    # The runner must refuse to select and signal BRANCH
    assert step_cfg(state) is Terminal.BRANCH


def test_cfg_fuel_exhaustion() -> None:
    # Self-loop at PC 0: 0 -> 0 -> 0 ...
    builder = CFGBuilder()
    builder.add_step(0, 0)
    graph = builder.to_graph()

    state = init_cfg(graph, start_pc=0, initial_data=0, fuel=3)
    term, final_s = run_cfg(10, state)
    assert term is Terminal.EXHAUSTED
    assert final_s.clock == 3
    assert final_s.fuel == 0


def test_cfg_dynamic_data_mutation_and_branching() -> None:
    # Program starts with data=0 at PC 0.
    # PC 0: mutates data to 42, jumps to PC 1
    # PC 1: conditional branch: if data == 42 -> PC 100, if data == 0 -> PC 200
    # PC 100: halt
    builder = CFGBuilder()
    builder.add_assignment(pc=0, new_data=42, next_pc=1)
    builder.add_branch(pc=1, cond_val=42, target_pc=100)
    builder.add_branch(pc=1, cond_val=0, target_pc=200)
    graph = builder.to_graph()

    state = init_cfg(graph, start_pc=0, initial_data=0, fuel=10)
    term, final_s = run_cfg(10, state)

    assert term is Terminal.HALT
    assert final_s.pc == 100
    assert final_s.data == 42
    assert final_s.clock == 2
    assert final_s.history == ((0, 0), (1, 42), (100, 42))
