"""Comprehensive test suite for Target M114 / SP-03: Solver Adapter & Bounded Search.

AuthorityEffect: None.
Tests:
- Positive feasibility: exact rational primal witnesses in Q.
- Negative infeasibility: exact Farkas dual separating hyperplane receipts.
- Typed refusal: Fuel exhaustion preserving unmutated problem state.
- Problem classes: Linear feasibility, Bounded SMT, SAT in CNF, Integer feasibility.
- Negative control matrices: Tampered certificates, invalid multipliers, out-of-bounds witnesses.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from solver_adapter import (
    Constraint,
    ConstraintProblem,
    ConstraintSense,
    DualReceipt,
    IntegerInfeasibilityReceipt,
    InvalidDualCertificateError,
    InvalidPrimalCertificateError,
    PrimalReceipt,
    ProblemType,
    RefusalReason,
    SolverAdapter,
    SolverRefusal,
    StepResult,
    VariableBound,
)


class TestLinearFeasibility:
    """Tests for exact rational linear feasibility."""

    def test_constraint_and_bounds_refuse_float(self) -> None:
        with pytest.raises(TypeError, match="float is not exact"):
            Constraint(name="c", coefficients={"x": 0.5}, rhs=1)  # type: ignore[dict-item]
        with pytest.raises(TypeError, match="float is not exact"):
            Constraint(name="c", coefficients={"x": 1}, rhs=0.5)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="float is not exact"):
            VariableBound(lower=0.5, upper=1)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="float is not exact"):
            ConstraintProblem.from_linear_system(
                variables=["x"],
                a_matrix=[[0.5]],  # type: ignore[list-item]
                b_vector=[1],
            )

    def test_single_variable_bounded(self) -> None:
        adapter = SolverAdapter()
        # 2 <= x <= 5
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1], [-1]],
            b_vector=[5, -2],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.status == "FEASIBLE"
        assert res.receipt.witness["x"] in (Fraction(2), Fraction(7, 2), Fraction(5))
        assert res.receipt.verify(problem)

    def test_2d_triangle_polytope(self) -> None:
        adapter = SolverAdapter()
        # x + y <= 2, -x <= 0, -y <= 0
        problem = ConstraintProblem.from_linear_system(
            variables=["x", "y"],
            a_matrix=[
                [1, 1],
                [-1, 0],
                [0, -1],
            ],
            b_vector=[2, 0, 0],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        witness = res.receipt.witness
        assert witness["x"] >= 0
        assert witness["y"] >= 0
        assert witness["x"] + witness["y"] <= 2
        assert res.receipt.verify(problem)

    def test_large_rational_denominators(self) -> None:
        adapter = SolverAdapter()
        # Exact arithmetic without floating-point degradation
        # (10^18 + 1) * x <= 10^18  and  -x <= -1/2
        big_den = 10**18 + 1
        big_num = 10**18
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[
                [Fraction(big_den, 1)],
                [Fraction(-1, 1)],
            ],
            b_vector=[
                Fraction(big_num, 1),
                Fraction(-1, 2),
            ],
        )
        res = adapter.solve(problem, fuel=5)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        x_val = res.receipt.witness["x"]
        assert x_val >= Fraction(1, 2)
        assert x_val <= Fraction(big_num, big_den)
        assert res.receipt.verify(problem)

    def test_unbounded_variable(self) -> None:
        adapter = SolverAdapter()
        # x free, y >= 3
        problem = ConstraintProblem.from_linear_system(
            variables=["x", "y"],
            a_matrix=[[0, -1]],
            b_vector=[-3],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["y"] >= 3
        assert res.receipt.verify(problem)


class TestInfeasibilityFarkasReceipts:
    """Tests for certified exact rational Farkas dual receipts."""

    def test_1d_direct_contradiction(self) -> None:
        adapter = SolverAdapter()
        # x <= 2 and x >= 5 (i.e. -x <= -5)
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1], [-1]],
            b_vector=[2, -5],
        )
        res = adapter.solve(problem, fuel=5)
        assert res.is_success
        assert isinstance(res.receipt, DualReceipt)
        assert res.receipt.status == "INFEASIBLE"
        assert res.receipt.combined_rhs < 0
        # Multipliers must be non-negative and cancel x
        assert res.receipt.multipliers == (Fraction(1), Fraction(1))
        assert all(y >= Fraction(0) for y in res.receipt.multipliers)
        assert all(v == Fraction(0) for v in res.receipt.combined_lhs.values())
        assert res.receipt.combined_rhs == Fraction(-3)
        assert res.receipt.combined_rhs < Fraction(0)
        assert res.receipt.verify(problem)

    def test_degenerate_contradiction(self) -> None:
        adapter = SolverAdapter()
        # 0 * x <= -7
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[0]],
            b_vector=[-7],
        )
        res = adapter.solve(problem, fuel=5)
        assert res.is_success
        assert isinstance(res.receipt, DualReceipt)
        assert res.receipt.multipliers == (Fraction(1),)
        assert res.receipt.combined_rhs == Fraction(-7)
        assert res.receipt.verify(problem)

    def test_2d_infeasible_hyperplanes(self) -> None:
        adapter = SolverAdapter()
        # x + y <= 1, -x <= -1 (x >= 1), -y <= -1 (y >= 1)
        # Sum of last two implies x + y >= 2, contradicting x + y <= 1
        problem = ConstraintProblem.from_linear_system(
            variables=["x", "y"],
            a_matrix=[
                [1, 1],
                [-1, 0],
                [0, -1],
            ],
            b_vector=[1, -1, -1],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, DualReceipt)
        assert res.receipt.status == "INFEASIBLE"
        assert res.receipt.combined_rhs < 0
        assert res.receipt.verify(problem)


class TestBoundedSMT:
    """Tests for Bounded SMT linear rational arithmetic."""

    def test_smt_with_explicit_bounds(self) -> None:
        adapter = SolverAdapter()
        # 2*x + y == 4 with bounds 0 <= x <= 2, 0 <= y <= 4
        c_eq = Constraint(
            name="c_eq",
            coefficients={"x": Fraction(2), "y": Fraction(1)},
            sense=ConstraintSense.EQ,
            rhs=Fraction(4),
        )
        problem = ConstraintProblem.from_smt(
            variables=["x", "y"],
            constraints=[c_eq],
            bounds={
                "x": VariableBound(lower=Fraction(0), upper=Fraction(2)),
                "y": VariableBound(lower=Fraction(0), upper=Fraction(4)),
            },
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        w = res.receipt.witness
        assert 2 * w["x"] + w["y"] == Fraction(4)
        assert res.receipt.verify(problem)

    def test_smt_infeasible_bounds(self) -> None:
        adapter = SolverAdapter()
        # x + y <= 3, bounds x >= 2, y >= 2 => x + y >= 4
        c = Constraint(
            name="c_sum",
            coefficients={"x": Fraction(1), "y": Fraction(1)},
            sense=ConstraintSense.LE,
            rhs=Fraction(3),
        )
        problem = ConstraintProblem.from_smt(
            variables=["x", "y"],
            constraints=[c],
            bounds={
                "x": VariableBound(lower=Fraction(2), upper=Fraction(10)),
                "y": VariableBound(lower=Fraction(2), upper=Fraction(10)),
            },
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, DualReceipt)
        assert res.receipt.verify(problem)


class TestSATCNF:
    """Tests for Propositional SAT in CNF."""

    def test_sat_satisfiable(self) -> None:
        adapter = SolverAdapter()
        # (x1 or x2) and (-x1 or x2)
        clauses = [
            ["x1", "x2"],
            ["-x1", "x2"],
        ]
        problem = ConstraintProblem.from_sat_cnf(
            variables=["x1", "x2"],
            clauses=clauses,
        )
        res = adapter.solve(problem, fuel=15)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        w = res.receipt.witness
        # Boolean constraints: x2 must be 1
        assert w["x2"] == Fraction(1)
        assert w["x1"] in (Fraction(0), Fraction(1))
        assert res.receipt.verify(problem)

    def test_sat_unsatisfiable(self) -> None:
        adapter = SolverAdapter()
        # (x1) and (-x1)
        clauses = [
            ["x1"],
            ["-x1"],
        ]
        problem = ConstraintProblem.from_sat_cnf(
            variables=["x1"],
            clauses=clauses,
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, DualReceipt)
        assert res.receipt.status == "INFEASIBLE"
        assert res.receipt.verify(problem)


class TestIntegerLinearFeasibility:
    """Tests for bounded integer linear feasibility."""

    def test_integer_feasible(self) -> None:
        adapter = SolverAdapter()
        # 3*x + 2*y <= 12, x >= 1, y >= 1, x in Z, y in Z
        c = Constraint(
            name="c1",
            coefficients={"x": Fraction(3), "y": Fraction(2)},
            sense=ConstraintSense.LE,
            rhs=Fraction(12),
        )
        problem = ConstraintProblem.from_ilp(
            variables=["x", "y"],
            constraints=[c],
            bounds={
                "x": VariableBound(lower=Fraction(1), upper=Fraction(5)),
                "y": VariableBound(lower=Fraction(1), upper=Fraction(5)),
            },
            integer_vars=["x", "y"],
        )
        res = adapter.solve(problem, fuel=20)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        w = res.receipt.witness
        assert w["x"].denominator == 1
        assert w["y"].denominator == 1
        assert 3 * w["x"] + 2 * w["y"] <= 12
        assert res.receipt.verify(problem)

    def test_integer_infeasible_due_to_integrality(self) -> None:
        adapter = SolverAdapter()
        # 2*x <= 1 and -2*x <= -1 (forces x = 1/2) with x in Z
        c1 = Constraint(name="ub", coefficients={"x": Fraction(2)}, sense=ConstraintSense.LE, rhs=Fraction(1))
        c2 = Constraint(name="lb", coefficients={"x": Fraction(-2)}, sense=ConstraintSense.LE, rhs=Fraction(-1))
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[c1, c2],
            integer_vars=["x"],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, IntegerInfeasibilityReceipt)
        assert res.receipt.status == "INFEASIBLE"
        assert res.receipt.variable == "x"
        assert res.receipt.lp_value == Fraction(1, 2)
        assert res.receipt.verify(problem)
        left = res.receipt.left_certificate
        assert isinstance(left, DualReceipt)
        with pytest.raises(InvalidDualCertificateError):
            left.verify(problem)


class TestRefusalSemantics:
    """Tests for typed refusal and state preservation on budget exhaustion."""

    def test_zero_fuel_immediate_refusal(self) -> None:
        adapter = SolverAdapter()
        problem = ConstraintProblem.from_linear_system(
            variables=["x", "y"],
            a_matrix=[[1, 1]],
            b_vector=[5],
        )
        res = adapter.solve(problem, fuel=0)
        assert not res.is_success
        assert res.is_refusal
        assert res.refusal is not None
        assert res.refusal.reason == RefusalReason.FUEL_EXHAUSTED
        assert res.refusal.consumed_fuel == 0
        # State preservation invariant: problem is unmutated
        assert res.refusal.retained_state.problem == problem

    def test_partial_fuel_exhaustion(self) -> None:
        adapter = SolverAdapter()
        # 3 variables, each elimination takes 1 fuel, budget=1 will exhaust before completing
        problem = ConstraintProblem.from_linear_system(
            variables=["x", "y", "z"],
            a_matrix=[
                [1, 1, 1],
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, -1],
            ],
            b_vector=[10, 0, 0, 0],
        )
        res = adapter.solve(problem, fuel=1)
        assert not res.is_success
        assert res.is_refusal
        assert res.refusal is not None
        assert res.refusal.reason == RefusalReason.FUEL_EXHAUSTED
        assert res.refusal.retained_state.problem == problem


class TestNegativeControlMatrices:
    """Falsification tests: verifying that corrupted certificates are rejected."""

    def test_corrupted_primal_witness_violates_constraint(self) -> None:
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1]],
            b_vector=[2],
        )
        # Fake witness claiming x = 5 satisfies x <= 2
        fake_primal = PrimalReceipt(witness={"x": Fraction(5)}, constraints_checked=1)
        with pytest.raises(InvalidPrimalCertificateError):
            fake_primal.verify(problem)

    def test_corrupted_primal_witness_violates_bounds(self) -> None:
        problem = ConstraintProblem.from_smt(
            variables=["x"],
            constraints=[],
            bounds={"x": VariableBound(lower=Fraction(0), upper=Fraction(1))},
        )
        fake_primal = PrimalReceipt(witness={"x": Fraction(2)}, constraints_checked=0)
        with pytest.raises(InvalidPrimalCertificateError):
            fake_primal.verify(problem)

    def test_corrupted_primal_witness_non_boolean(self) -> None:
        problem = ConstraintProblem.from_sat_cnf(
            variables=["x"],
            clauses=[["x"]],
        )
        fake_primal = PrimalReceipt(witness={"x": Fraction(1, 2)}, constraints_checked=1)
        with pytest.raises(InvalidPrimalCertificateError):
            fake_primal.verify(problem)

    def test_corrupted_dual_receipt_negative_multiplier(self) -> None:
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1], [-1]],
            b_vector=[2, -5],
        )
        fake_dual = DualReceipt(
            multipliers=(Fraction(-1), Fraction(1)),
            combined_lhs={"x": Fraction(0)},
            combined_rhs=Fraction(-7),
        )
        with pytest.raises(InvalidDualCertificateError, match="Negative multiplier"):
            fake_dual.verify(problem)

    def test_corrupted_dual_receipt_non_cancelling_lhs(self) -> None:
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1], [-1]],
            b_vector=[2, -5],
        )
        # Multipliers (2, 1) gives 2*x - x = x != 0
        fake_dual = DualReceipt(
            multipliers=(Fraction(2), Fraction(1)),
            combined_lhs={"x": Fraction(0)},
            combined_rhs=Fraction(-1),
        )
        with pytest.raises(InvalidDualCertificateError, match="Non-zero combined coefficient"):
            fake_dual.verify(problem)

    def test_corrupted_dual_receipt_non_negative_rhs(self) -> None:
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1], [-1]],
            b_vector=[5, -2],
        )
        # Feasible problem, sum is 5 - 2 = 3 >= 0
        fake_dual = DualReceipt(
            multipliers=(Fraction(1), Fraction(1)),
            combined_lhs={"x": Fraction(0)},
            combined_rhs=Fraction(3),
        )
        with pytest.raises(InvalidDualCertificateError, match="not strictly negative"):
            fake_dual.verify(problem)

    def test_corrupted_primal_missing_variable(self) -> None:
        problem = ConstraintProblem.from_smt(
            variables=["x", "y"],
            constraints=[],
            bounds={"x": VariableBound(lower=Fraction(0), upper=Fraction(1))},
        )
        fake_primal = PrimalReceipt(witness={"y": Fraction(0)}, constraints_checked=0)
        with pytest.raises(InvalidPrimalCertificateError, match="Variable missing"):
            fake_primal.verify(problem)

    def test_corrupted_primal_violates_lower_bound(self) -> None:
        problem = ConstraintProblem.from_smt(
            variables=["x"],
            constraints=[],
            bounds={"x": VariableBound(lower=Fraction(2), upper=Fraction(5))},
        )
        fake_primal = PrimalReceipt(witness={"x": Fraction(1)}, constraints_checked=0)
        with pytest.raises(InvalidPrimalCertificateError, match="violates lower bound"):
            fake_primal.verify(problem)

    def test_corrupted_primal_violates_integer(self) -> None:
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[],
            integer_vars=["x"],
        )
        fake_primal = PrimalReceipt(witness={"x": Fraction(1, 3)}, constraints_checked=0)
        with pytest.raises(InvalidPrimalCertificateError, match="fractional value"):
            fake_primal.verify(problem)

    def test_corrupted_primal_violates_ge_constraint(self) -> None:
        c = Constraint(name="ge_row", coefficients={"x": Fraction(1)}, sense=ConstraintSense.GE, rhs=Fraction(5))
        problem = ConstraintProblem.from_smt(variables=["x"], constraints=[c])
        fake_primal = PrimalReceipt(witness={"x": Fraction(3)}, constraints_checked=1)
        with pytest.raises(InvalidPrimalCertificateError, match="< RHS"):
            fake_primal.verify(problem)

    def test_corrupted_primal_violates_eq_constraint(self) -> None:
        c = Constraint(name="eq_row", coefficients={"x": Fraction(1)}, sense=ConstraintSense.EQ, rhs=Fraction(5))
        problem = ConstraintProblem.from_smt(variables=["x"], constraints=[c])
        fake_primal = PrimalReceipt(witness={"x": Fraction(3)}, constraints_checked=1)
        with pytest.raises(InvalidPrimalCertificateError, match="!= RHS"):
            fake_primal.verify(problem)

    def test_corrupted_dual_multiplier_length_mismatch(self) -> None:
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1], [-1]],
            b_vector=[2, -5],
        )
        fake_dual = DualReceipt(
            multipliers=(Fraction(1),),  # Expected length 2
            combined_lhs={"x": Fraction(0)},
            combined_rhs=Fraction(-3),
        )
        with pytest.raises(InvalidDualCertificateError, match="Multiplier length"):
            fake_dual.verify(problem)

    def test_corrupted_dual_claimed_rhs_mismatch(self) -> None:
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1], [-1]],
            b_vector=[2, -5],
        )
        fake_dual = DualReceipt(
            multipliers=(Fraction(1), Fraction(1)),
            combined_lhs={"x": Fraction(0)},
            combined_rhs=Fraction(-99),  # Actual combined is 2 - 5 = -3
        )
        with pytest.raises(InvalidDualCertificateError, match="does not match claimed RHS"):
            fake_dual.verify(problem)


class TestBranchAndBoundVariants:
    """Tests covering branch-and-bound exploration branches and refusals."""

    def test_ge_constraint_feasibility(self) -> None:
        adapter = SolverAdapter()
        # x >= 3 and x <= 5
        c = Constraint(name="ge_test", coefficients={"x": Fraction(1)}, sense=ConstraintSense.GE, rhs=Fraction(3))
        problem = ConstraintProblem.from_smt(
            variables=["x"],
            constraints=[c],
            bounds={"x": VariableBound(lower=Fraction(0), upper=Fraction(5))},
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["x"] >= 3
        assert res.receipt.verify(problem)

    def test_contradictory_variable_bound(self) -> None:
        adapter = SolverAdapter()
        # Bound: 5 <= x <= 2
        problem = ConstraintProblem.from_smt(
            variables=["x"],
            constraints=[],
            bounds={"x": VariableBound(lower=Fraction(5), upper=Fraction(2))},
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, DualReceipt)
        assert res.receipt.verify(problem)

    def test_branch_and_bound_fuel_exhaustion(self) -> None:
        adapter = SolverAdapter()
        # Force branching: x in [0.4, 0.6] with x in Z
        # relaxation takes 1 fuel, so fuel=1 causes exhaustion during branching
        c1 = Constraint(name="c1", coefficients={"x": Fraction(10)}, sense=ConstraintSense.LE, rhs=Fraction(6))
        c2 = Constraint(name="c2", coefficients={"x": Fraction(-10)}, sense=ConstraintSense.LE, rhs=Fraction(-4))
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[c1, c2],
            integer_vars=["x"],
        )
        res = adapter.solve(problem, fuel=1)
        assert not res.is_success
        assert res.is_refusal
        assert res.refusal is not None
        assert res.refusal.reason == RefusalReason.FUEL_EXHAUSTED

    def test_branch_and_bound_left_success(self) -> None:
        adapter = SolverAdapter()
        # x in [-0.5, 0.5] with x in Z -> x = 0
        c1 = Constraint(name="c1", coefficients={"x": Fraction(2)}, sense=ConstraintSense.LE, rhs=Fraction(1))
        c2 = Constraint(name="c2", coefficients={"x": Fraction(-2)}, sense=ConstraintSense.LE, rhs=Fraction(1))
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[c1, c2],
            integer_vars=["x"],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["x"] == Fraction(0)
        assert res.receipt.verify(problem)

    def test_branch_and_bound_right_success(self) -> None:
        adapter = SolverAdapter()
        # x in [0.5, 1.5] with x in Z -> x = 1
        c1 = Constraint(name="c1", coefficients={"x": Fraction(2)}, sense=ConstraintSense.LE, rhs=Fraction(3))
        c2 = Constraint(name="c2", coefficients={"x": Fraction(-2)}, sense=ConstraintSense.LE, rhs=Fraction(-1))
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[c1, c2],
            integer_vars=["x"],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["x"] == Fraction(1)
        assert res.receipt.verify(problem)

    def test_integer_var_single_lower_bound(self) -> None:
        adapter = SolverAdapter()
        # x >= 3/2 with x in Z -> x = 2
        c = Constraint(name="c", coefficients={"x": Fraction(-2)}, sense=ConstraintSense.LE, rhs=Fraction(-3))
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[c],
            integer_vars=["x"],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["x"] >= Fraction(3, 2)
        assert res.receipt.witness["x"].denominator == 1

    def test_integer_var_single_upper_bound(self) -> None:
        adapter = SolverAdapter()
        # x <= 7/2 with x in Z -> x <= 3
        c = Constraint(name="c", coefficients={"x": Fraction(2)}, sense=ConstraintSense.LE, rhs=Fraction(7))
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[c],
            integer_vars=["x"],
        )
        res = adapter.solve(problem, fuel=10)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["x"] <= Fraction(7, 2)
        assert res.receipt.witness["x"].denominator == 1

    def test_invalid_constraint_sense(self) -> None:
        c = Constraint(name="bad", coefficients={"x": Fraction(1)}, sense="INVALID")  # type: ignore
        with pytest.raises(ValueError, match="Unknown constraint sense"):
            c.to_le_constraints()

    def test_int_rhs_conversion(self) -> None:
        c = Constraint(name="int_rhs", coefficients={"x": 1}, rhs=5)
        assert isinstance(c.rhs, Fraction)
        assert c.rhs == Fraction(5)

    def test_from_linear_system_with_bounds(self) -> None:
        problem = ConstraintProblem.from_linear_system(
            variables=["x"],
            a_matrix=[[1]],
            b_vector=[10],
            bounds={"x": (2, 8)},
        )
        assert problem.bounds["x"].lower == Fraction(2)
        assert problem.bounds["x"].upper == Fraction(8)

    def test_coupled_integer_problem(self) -> None:
        adapter = SolverAdapter()
        # 2*x + 2*y == 3 on 0 <= x, y <= 2 has no solution in Z
        c_le = Constraint(name="c_le", coefficients={"x": Fraction(2), "y": Fraction(2)}, sense=ConstraintSense.LE, rhs=Fraction(3))
        c_ge = Constraint(name="c_ge", coefficients={"x": Fraction(-2), "y": Fraction(-2)}, sense=ConstraintSense.LE, rhs=Fraction(-3))
        problem = ConstraintProblem.from_ilp(
            variables=["x", "y"],
            constraints=[c_le, c_ge],
            bounds={
                "x": VariableBound(lower=Fraction(0), upper=Fraction(2)),
                "y": VariableBound(lower=Fraction(0), upper=Fraction(2)),
            },
            integer_vars=["x", "y"],
        )
        res = adapter.solve(problem, fuel=30)
        assert res.is_success
        assert isinstance(res.receipt, (DualReceipt, IntegerInfeasibilityReceipt))
        assert res.receipt.verify(problem)

    def test_variable_bound_int_conversion(self) -> None:
        bnd = VariableBound(lower=1, upper=5)  # type: ignore
        assert bnd.lower == Fraction(1)
        assert bnd.upper == Fraction(5)

    def test_unbounded_integer_variable_defaults_zero(self) -> None:
        adapter = SolverAdapter()
        problem = ConstraintProblem.from_ilp(
            variables=["x"],
            constraints=[],
            integer_vars=["x"],
        )
        res = adapter.solve(problem, fuel=5)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["x"] == Fraction(0)

    def test_continuous_upper_bound_only(self) -> None:
        adapter = SolverAdapter()
        # x <= 3, no lower bound
        c = Constraint(name="ub", coefficients={"x": Fraction(1)}, rhs=Fraction(3))
        problem = ConstraintProblem.from_smt(variables=["x"], constraints=[c])
        res = adapter.solve(problem, fuel=5)
        assert res.is_success
        assert isinstance(res.receipt, PrimalReceipt)
        assert res.receipt.witness["x"] == Fraction(3)




