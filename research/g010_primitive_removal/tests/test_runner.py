"""Unit tests for the comparative execution runner."""

from runner import ComparativeRunner


def test_comparative_runner_standard_battery() -> None:
    runner = ComparativeRunner()
    results = runner.run_standard_battery()

    assert len(results) == 4

    # 1. Baseline task: both unrestricted and restricted pass
    r_base = results[0]
    assert r_base.task_name == "LINEAR_ARITHMETIC_TASK"
    assert r_base.unrestricted_passed
    assert r_base.restricted_passed
    assert r_base.status == "MATCHING_PASS"
    assert r_base.unrestricted_views[0].equals(r_base.restricted_views[0])

    # 2. Branching task: unrestricted passes, restricted is obstructed
    r_branch = results[1]
    assert r_branch.task_name == "CONDITIONAL_ROUTING_TASK"
    assert r_branch.unrestricted_passed
    assert not r_branch.restricted_passed
    assert r_branch.status == "OBSTRUCTED_AS_EXPECTED"
    assert "BRANCHING_OBSTRUCTION" in (r_branch.obstruction_witness or "")

    # 3. Memory task: unrestricted passes, restricted is obstructed
    r_mem = results[2]
    assert r_mem.task_name == "PERSISTENT_RETENTION_TASK"
    assert r_mem.unrestricted_passed
    assert not r_mem.restricted_passed
    assert r_mem.status == "OBSTRUCTED_AS_EXPECTED"
    assert "MEMORY_OBSTRUCTION" in (r_mem.obstruction_witness or "")

    # 4. Allocation task: unrestricted passes, restricted is obstructed
    r_alloc = results[3]
    assert r_alloc.task_name == "DYNAMIC_ALLOCATION_TASK"
    assert r_alloc.unrestricted_passed
    assert not r_alloc.restricted_passed
    assert r_alloc.status == "OBSTRUCTED_AS_EXPECTED"
    assert "ALLOCATION_OBSTRUCTION" in (r_alloc.obstruction_witness or "")


def test_comparative_runner_serialization() -> None:
    runner = ComparativeRunner()
    results = runner.run_standard_battery()
    for res in results:
        d = res.to_dict()
        assert "task_name" in d
        assert "status" in d
        assert "unrestricted_views" in d
        assert "restricted_views" in d
