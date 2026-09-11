"""Operational Solver Boundary Adapter & Bounded Search Engine (Target M114 / SP-03).

AuthorityEffect: None.

Pure Python standard library implementation mapping external constraint problems
(SAT in CNF, bounded SMT, integer and rational linear feasibility) into a
deterministic demand-and-refusal lifecycle without host oracles.

Produces certified exact rational duality receipts in Q (fractions.Fraction):
- Feasibility: PrimalReceipt witnessing exact rational vector x* in Q^n.
- Infeasibility: DualReceipt witnessing Farkas separating hyperplane multipliers y in Q_>=0^m.
- Bounded exhaustion: Explicit typed refusal StepResult.refusal preserving state without mutation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Any, Dict, FrozenSet, List, Mapping, Optional, Sequence, Tuple


class ProblemType(str, Enum):
    LINEAR_FEASIBILITY = "LINEAR_FEASIBILITY"
    BOUNDED_SMT = "BOUNDED_SMT"
    SAT_CNF = "SAT_CNF"
    INTEGER_FEASIBILITY = "INTEGER_FEASIBILITY"


class RefusalReason(str, Enum):
    FUEL_EXHAUSTED = "FUEL_EXHAUSTED"
    HORIZON_EXCEEDED = "HORIZON_EXCEEDED"
    UNBOUNDED_VARIABLE = "UNBOUNDED_VARIABLE"


class ConstraintSense(str, Enum):
    LE = "<="
    GE = ">="
    EQ = "=="


class SolverAdapterError(Exception):
    """Base exception for solver adapter operations."""


class InvalidPrimalCertificateError(SolverAdapterError):
    """Raised when a primal feasibility certificate fails verification."""

    def __init__(self, row: int | str, violation: str):
        super().__init__(f"Primal certificate invalid at constraint {row!r}: {violation}")
        self.row = row
        self.violation = violation


class InvalidDualCertificateError(SolverAdapterError):
    """Raised when a dual Farkas infeasibility certificate fails verification."""

    def __init__(self, reason: str):
        super().__init__(f"Dual Farkas certificate invalid: {reason}")
        self.reason = reason


@dataclass(frozen=True)
class VariableBound:
    """Exact rational interval bounds on a single variable."""

    lower: Optional[Fraction] = None
    upper: Optional[Fraction] = None

    def __post_init__(self) -> None:
        if self.lower is not None and not isinstance(self.lower, Fraction):
            object.__setattr__(self, "lower", Fraction(self.lower))
        if self.upper is not None and not isinstance(self.upper, Fraction):
            object.__setattr__(self, "upper", Fraction(self.upper))
        if self.lower is not None and self.upper is not None and self.lower > self.upper:
            # Note: contradictory bound is allowed as input; solver will detect infeasibility.
            pass


@dataclass(frozen=True, init=False)
class Constraint:
    """Linear constraint: sum(coeffs[v] * v) sense rhs."""

    name: str
    coefficients: Mapping[str, Fraction]
    sense: ConstraintSense
    rhs: Fraction

    def __init__(
        self,
        name: str,
        coefficients: Mapping[str, Fraction | int],
        sense: ConstraintSense = ConstraintSense.LE,
        rhs: Fraction | int = Fraction(0),
    ) -> None:
        norm_coeffs: Dict[str, Fraction] = {}
        for k, v in coefficients.items():
            fr = v if isinstance(v, Fraction) else Fraction(v)
            if fr != 0:
                norm_coeffs[k] = fr
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "coefficients", dict(sorted(norm_coeffs.items())))
        object.__setattr__(self, "sense", sense)
        object.__setattr__(self, "rhs", rhs if isinstance(rhs, Fraction) else Fraction(rhs))

    def to_le_constraints(self) -> Tuple[Constraint, ...]:
        """Convert any constraint sense into one or two <= constraints."""
        if self.sense == ConstraintSense.LE:
            return (self,)
        elif self.sense == ConstraintSense.GE:
            neg_coeffs = {k: -v for k, v in self.coefficients.items()}
            return (Constraint(name=f"{self.name}_ge_norm", coefficients=neg_coeffs, sense=ConstraintSense.LE, rhs=-self.rhs),)
        elif self.sense == ConstraintSense.EQ:
            neg_coeffs = {k: -v for k, v in self.coefficients.items()}
            c_le = Constraint(name=f"{self.name}_eq_le", coefficients=dict(self.coefficients), sense=ConstraintSense.LE, rhs=self.rhs)
            c_ge = Constraint(name=f"{self.name}_eq_ge", coefficients=neg_coeffs, sense=ConstraintSense.LE, rhs=-self.rhs)
            return (c_le, c_ge)
        raise ValueError(f"Unknown constraint sense: {self.sense}")


@dataclass(frozen=True)
class ConstraintProblem:
    """Representation of an operational constraint problem."""

    problem_type: ProblemType
    variables: Tuple[str, ...]
    constraints: Tuple[Constraint, ...]
    bounds: Mapping[str, VariableBound] = field(default_factory=dict)
    boolean_vars: FrozenSet[str] = frozenset()
    integer_vars: FrozenSet[str] = frozenset()

    @classmethod
    def from_linear_system(
        cls,
        variables: Sequence[str],
        a_matrix: Sequence[Sequence[Fraction | int]],
        b_vector: Sequence[Fraction | int],
        bounds: Optional[Mapping[str, Tuple[Optional[Fraction | int], Optional[Fraction | int]]]] = None,
    ) -> ConstraintProblem:
        """Create a linear feasibility problem A x <= b."""
        var_tuple = tuple(variables)
        c_list: List[Constraint] = []
        for i, (row, rhs_val) in enumerate(zip(a_matrix, b_vector)):
            coeffs = {var_tuple[j]: Fraction(val) for j, val in enumerate(row) if val != 0}
            c_list.append(Constraint(name=f"row_{i}", coefficients=coeffs, sense=ConstraintSense.LE, rhs=Fraction(rhs_val)))

        v_bounds: Dict[str, VariableBound] = {}
        if bounds:
            for k, (lb, ub) in bounds.items():
                v_bounds[k] = VariableBound(
                    lower=Fraction(lb) if lb is not None else None,
                    upper=Fraction(ub) if ub is not None else None,
                )

        return cls(
            problem_type=ProblemType.LINEAR_FEASIBILITY,
            variables=var_tuple,
            constraints=tuple(c_list),
            bounds=v_bounds,
        )

    @classmethod
    def from_smt(
        cls,
        variables: Sequence[str],
        constraints: Sequence[Constraint],
        bounds: Optional[Mapping[str, VariableBound]] = None,
    ) -> ConstraintProblem:
        """Create a bounded SMT quantifier-free linear rational problem."""
        return cls(
            problem_type=ProblemType.BOUNDED_SMT,
            variables=tuple(variables),
            constraints=tuple(constraints),
            bounds=dict(bounds) if bounds else {},
        )

    @classmethod
    def from_sat_cnf(
        cls,
        variables: Sequence[str],
        clauses: Sequence[Sequence[str]],
    ) -> ConstraintProblem:
        """Create a SAT problem in CNF mapped to 0-1 linear inequalities.

        Each literal is 'x' or '-x'. Clause (l_1 or ... or l_k) is mapped to:
        sum_{pos} x_i + sum_{neg} (1 - x_j) >= 1
        which is: -sum_{pos} x_i + sum_{neg} x_j <= |neg| - 1
        with bounds 0 <= x_i <= 1 and boolean_vars.
        """
        var_tuple = tuple(variables)
        c_list: List[Constraint] = []
        v_bounds: Dict[str, VariableBound] = {
            v: VariableBound(lower=Fraction(0), upper=Fraction(1)) for v in var_tuple
        }

        for idx, clause in enumerate(clauses):
            coeffs: Dict[str, Fraction] = {}
            neg_count = 0
            for lit in clause:
                if lit.startswith("-"):
                    vname = lit[1:]
                    coeffs[vname] = coeffs.get(vname, Fraction(0)) + Fraction(1)
                    neg_count += 1
                else:
                    vname = lit
                    coeffs[vname] = coeffs.get(vname, Fraction(0)) - Fraction(1)
            rhs = Fraction(neg_count - 1)
            c_list.append(Constraint(name=f"clause_{idx}", coefficients=coeffs, sense=ConstraintSense.LE, rhs=rhs))

        return cls(
            problem_type=ProblemType.SAT_CNF,
            variables=var_tuple,
            constraints=tuple(c_list),
            bounds=v_bounds,
            boolean_vars=frozenset(var_tuple),
            integer_vars=frozenset(var_tuple),
        )

    @classmethod
    def from_ilp(
        cls,
        variables: Sequence[str],
        constraints: Sequence[Constraint],
        bounds: Optional[Mapping[str, VariableBound]] = None,
        integer_vars: Optional[Sequence[str]] = None,
    ) -> ConstraintProblem:
        """Create an integer linear feasibility problem."""
        var_tuple = tuple(variables)
        i_vars = frozenset(integer_vars) if integer_vars is not None else frozenset(var_tuple)
        return cls(
            problem_type=ProblemType.INTEGER_FEASIBILITY,
            variables=var_tuple,
            constraints=tuple(constraints),
            bounds=dict(bounds) if bounds else {},
            integer_vars=i_vars,
        )


@dataclass(frozen=True)
class PrimalReceipt:
    """Exact rational witness certifying primal feasibility."""

    witness: Mapping[str, Fraction]
    constraints_checked: int
    status: str = "FEASIBLE"

    def verify(self, problem: ConstraintProblem, check_integrality: bool = True) -> bool:
        """Verify that the primal witness satisfies all constraints and bounds."""
        # 1. Check variable bounds
        for vname, bound in problem.bounds.items():
            if vname not in self.witness:
                raise InvalidPrimalCertificateError(vname, "Variable missing in witness")
            val = self.witness[vname]
            if bound.lower is not None and val < bound.lower:
                raise InvalidPrimalCertificateError(vname, f"Value {val} violates lower bound {bound.lower}")
            if bound.upper is not None and val > bound.upper:
                raise InvalidPrimalCertificateError(vname, f"Value {val} violates upper bound {bound.upper}")

        # 2. Check integer / boolean restrictions
        if check_integrality:
            for vname in problem.boolean_vars:
                val = self.witness.get(vname, Fraction(0))
                if val not in (Fraction(0), Fraction(1)):
                    raise InvalidPrimalCertificateError(vname, f"Boolean variable has non-boolean value {val}")

            for vname in problem.integer_vars:
                val = self.witness.get(vname, Fraction(0))
                if val.denominator != 1:
                    raise InvalidPrimalCertificateError(vname, f"Integer variable has fractional value {val}")

        # 3. Check all constraints
        for c in problem.constraints:
            lhs = Fraction(0)
            for vname, coeff in c.coefficients.items():
                lhs += coeff * self.witness.get(vname, Fraction(0))

            if c.sense == ConstraintSense.LE:
                if lhs > c.rhs:
                    raise InvalidPrimalCertificateError(c.name, f"LHS {lhs} > RHS {c.rhs}")
            elif c.sense == ConstraintSense.GE:
                if lhs < c.rhs:
                    raise InvalidPrimalCertificateError(c.name, f"LHS {lhs} < RHS {c.rhs}")
            elif c.sense == ConstraintSense.EQ:
                if lhs != c.rhs:
                    raise InvalidPrimalCertificateError(c.name, f"LHS {lhs} != RHS {c.rhs}")

        return True


@dataclass(frozen=True)
class DualReceipt:
    """Exact rational Farkas separating certificate certifying infeasibility."""

    multipliers: Tuple[Fraction, ...]
    combined_lhs: Mapping[str, Fraction]
    combined_rhs: Fraction
    status: str = "INFEASIBLE"

    def verify(self, problem: ConstraintProblem) -> bool:
        """Verify Farkas separating hyperplane certificate: y >= 0, y^T A = 0, y^T b < 0."""
        # Normalize problem into standard <= constraints
        normalized_constraints: List[Constraint] = []
        for c in problem.constraints:
            normalized_constraints.extend(c.to_le_constraints())

        # Also add explicit bound constraints
        for vname, bnd in problem.bounds.items():
            if bnd.upper is not None:
                normalized_constraints.append(
                    Constraint(name=f"{vname}_ub", coefficients={vname: Fraction(1)}, sense=ConstraintSense.LE, rhs=bnd.upper)
                )
            if bnd.lower is not None:
                normalized_constraints.append(
                    Constraint(name=f"{vname}_lb", coefficients={vname: Fraction(-1)}, sense=ConstraintSense.LE, rhs=-bnd.lower)
                )

        if len(self.multipliers) != len(normalized_constraints):
            raise InvalidDualCertificateError(
                f"Multiplier length {len(self.multipliers)} does not match constraint count {len(normalized_constraints)}"
            )

        # 1. Non-negativity check
        for idx, y in enumerate(self.multipliers):
            if y < 0:
                raise InvalidDualCertificateError(f"Negative multiplier at row {idx}: {y}")

        # 2. Combined LHS check: sum y_i A_ij == 0
        comb_lhs: Dict[str, Fraction] = {v: Fraction(0) for v in problem.variables}
        for y, c in zip(self.multipliers, normalized_constraints):
            if y != 0:
                for vname, coeff in c.coefficients.items():
                    comb_lhs[vname] = comb_lhs.get(vname, Fraction(0)) + y * coeff

        for vname, val in comb_lhs.items():
            if val != 0:
                raise InvalidDualCertificateError(f"Non-zero combined coefficient for variable {vname}: {val}")

        # 3. Combined RHS check: sum y_i b_i < 0
        comb_rhs = Fraction(0)
        for y, c in zip(self.multipliers, normalized_constraints):
            if y != 0:
                comb_rhs += y * c.rhs

        if comb_rhs != self.combined_rhs:
            raise InvalidDualCertificateError(
                f"Combined RHS {comb_rhs} does not match claimed RHS {self.combined_rhs}"
            )

        if comb_rhs >= 0:
            raise InvalidDualCertificateError(f"Combined RHS {comb_rhs} is not strictly negative")

        return True


@dataclass(frozen=True)
class SolverState:
    """Immutable snapshot of the solver state at any point during search."""

    problem: ConstraintProblem
    eliminated_variables: Tuple[str, ...]
    active_constraints: Tuple[Constraint, ...]
    step_count: int


@dataclass(frozen=True)
class SolverRefusal:
    """Explicit typed refusal emitted when bounded resources are exhausted."""

    reason: RefusalReason
    consumed_fuel: int
    retained_state: SolverState


@dataclass(frozen=True)
class StepResult:
    """Result of a single solver step or complete bounded search."""

    is_success: bool
    is_refusal: bool
    receipt: Optional[PrimalReceipt | DualReceipt] = None
    refusal: Optional[SolverRefusal] = None
    fuel_remaining: int = 0

    @classmethod
    def success(cls, receipt: PrimalReceipt | DualReceipt, fuel_remaining: int) -> StepResult:
        return cls(is_success=True, is_refusal=False, receipt=receipt, fuel_remaining=fuel_remaining)

    @classmethod
    def refuse(cls, refusal: SolverRefusal) -> StepResult:
        return cls(is_success=False, is_refusal=True, refusal=refusal, fuel_remaining=0)


# Internal working row for Fourier-Motzkin elimination with exact multiplier tracking
@dataclass(frozen=True)
class _FMRow:
    coefficients: Mapping[str, Fraction]
    rhs: Fraction
    # Sparse multiplier map: constraint_index -> Fraction
    multipliers: Mapping[int, Fraction]

    def coeff(self, var: str) -> Fraction:
        return self.coefficients.get(var, Fraction(0))


class SolverAdapter:
    """Operational solver adapter connecting external constraints to demand-and-refusal lifecycle."""

    def __init__(self) -> None:
        pass

    def solve(self, problem: ConstraintProblem, fuel: int) -> StepResult:
        """Solve a constraint problem under bounded fuel without host oracles."""
        initial_state = SolverState(
            problem=problem,
            eliminated_variables=(),
            active_constraints=problem.constraints,
            step_count=0,
        )

        if fuel <= 0:
            return StepResult.refuse(
                SolverRefusal(
                    reason=RefusalReason.FUEL_EXHAUSTED,
                    consumed_fuel=0,
                    retained_state=initial_state,
                )
            )

        # 1. Flatten all constraints and variable bounds into a normalized list of <= constraints
        normalized_constraints: List[Constraint] = []
        for c in problem.constraints:
            normalized_constraints.extend(c.to_le_constraints())

        for vname, bnd in problem.bounds.items():
            if bnd.upper is not None:
                normalized_constraints.append(
                    Constraint(
                        name=f"{vname}_ub",
                        coefficients={vname: Fraction(1)},
                        sense=ConstraintSense.LE,
                        rhs=bnd.upper,
                    )
                )
            if bnd.lower is not None:
                normalized_constraints.append(
                    Constraint(
                        name=f"{vname}_lb",
                        coefficients={vname: Fraction(-1)},
                        sense=ConstraintSense.LE,
                        rhs=-bnd.lower,
                    )
                )

        m = len(normalized_constraints)

        # Build initial _FMRow list
        current_rows: List[_FMRow] = []
        for i, c in enumerate(normalized_constraints):
            current_rows.append(
                _FMRow(
                    coefficients=dict(c.coefficients),
                    rhs=c.rhs,
                    multipliers={i: Fraction(1)},
                )
            )

        # 2. Pre-check for immediate infeasibility (e.g. 0 <= -c where c > 0)
        for row in current_rows:
            if not row.coefficients:
                if row.rhs < 0:
                    # Immediate Farkas witness
                    mult_tuple = self._build_multiplier_tuple(m, row.multipliers)
                    dual = DualReceipt(
                        multipliers=mult_tuple,
                        combined_lhs={v: Fraction(0) for v in problem.variables},
                        combined_rhs=row.rhs,
                    )
                    dual.verify(problem)
                    return StepResult.success(dual, fuel_remaining=fuel - 1)

        # 3. For pure linear feasibility / bounded SMT, run continuous Fourier-Motzkin elimination
        if not problem.boolean_vars and not problem.integer_vars:
            return self._solve_continuous(problem, normalized_constraints, current_rows, fuel, initial_state)

        # 4. For SAT / integer problems, run bounded branch-and-bound with rational relaxations
        return self._solve_branch_and_bound(problem, normalized_constraints, current_rows, fuel, initial_state)

    def _solve_continuous(
        self,
        problem: ConstraintProblem,
        normalized_constraints: List[Constraint],
        rows: List[_FMRow],
        fuel: int,
        initial_state: SolverState,
    ) -> StepResult:
        """Run exact Fourier-Motzkin elimination over continuous variables."""
        m = len(normalized_constraints)
        current_rows = list(rows)
        eliminated: List[str] = []
        history: List[Tuple[str, List[_FMRow]]] = []

        fuel_remaining = fuel

        for var in problem.variables:
            if fuel_remaining <= 0:
                retained = SolverState(
                    problem=problem,
                    eliminated_variables=tuple(eliminated),
                    active_constraints=tuple(
                        Constraint(name=f"step_{i}", coefficients=r.coefficients, sense=ConstraintSense.LE, rhs=r.rhs)
                        for i, r in enumerate(current_rows)
                    ),
                    step_count=len(eliminated),
                )
                return StepResult.refuse(
                    SolverRefusal(
                        reason=RefusalReason.FUEL_EXHAUSTED,
                        consumed_fuel=fuel,
                        retained_state=retained,
                    )
                )

            # Record history for back-substitution
            history.append((var, list(current_rows)))
            eliminated.append(var)
            fuel_remaining -= 1

            pos_rows: List[_FMRow] = []
            neg_rows: List[_FMRow] = []
            zero_rows: List[_FMRow] = []

            for r in current_rows:
                c = r.coeff(var)
                if c > 0:
                    pos_rows.append(r)
                elif c < 0:
                    neg_rows.append(r)
                else:
                    zero_rows.append(r)

            new_rows: List[_FMRow] = list(zero_rows)

            # Combine pos and neg rows
            for p in pos_rows:
                cp = p.coeff(var)
                wp = Fraction(1, cp)
                for n in neg_rows:
                    cn = n.coeff(var)  # cn < 0
                    wn = Fraction(1, -cn)

                    # New coefficients
                    comb_coeffs: Dict[str, Fraction] = {}
                    all_vars = set(p.coefficients.keys()) | set(n.coefficients.keys())
                    for u in all_vars:
                        if u != var:
                            val = wp * p.coeff(u) + wn * n.coeff(u)
                            if val != 0:
                                comb_coeffs[u] = val

                    comb_rhs = wp * p.rhs + wn * n.rhs

                    # New multipliers
                    comb_mult: Dict[int, Fraction] = {}
                    all_indices = set(p.multipliers.keys()) | set(n.multipliers.keys())
                    for idx in all_indices:
                        val = wp * p.multipliers.get(idx, Fraction(0)) + wn * n.multipliers.get(idx, Fraction(0))
                        if val != 0:
                            comb_mult[idx] = val

                    # Check for contradiction 0 <= negative
                    if not comb_coeffs:
                        if comb_rhs < 0:
                            # Infeasibility certified!
                            mult_tuple = self._build_multiplier_tuple(m, comb_mult)
                            dual = DualReceipt(
                                multipliers=mult_tuple,
                                combined_lhs={v: Fraction(0) for v in problem.variables},
                                combined_rhs=comb_rhs,
                            )
                            dual.verify(problem)
                            return StepResult.success(dual, fuel_remaining=fuel_remaining)
                        else:
                            # Trivially satisfied 0 <= c, omit
                            continue

                    new_rows.append(
                        _FMRow(
                            coefficients=comb_coeffs,
                            rhs=comb_rhs,
                            multipliers=comb_mult,
                        )
                    )

            current_rows = new_rows

        # After all variables eliminated, check remaining rows
        for r in current_rows:
            if not r.coefficients and r.rhs < 0:
                mult_tuple = self._build_multiplier_tuple(m, r.multipliers)
                dual = DualReceipt(
                    multipliers=mult_tuple,
                    combined_lhs={v: Fraction(0) for v in problem.variables},
                    combined_rhs=r.rhs,
                )
                dual.verify(problem)
                return StepResult.success(dual, fuel_remaining=fuel_remaining)

        # Feasible! Back-substitute to extract primal witness
        witness = self._back_substitute(problem, history)
        primal = PrimalReceipt(
            witness=witness,
            constraints_checked=len(normalized_constraints),
        )
        primal.verify(problem, check_integrality=False)
        return StepResult.success(primal, fuel_remaining=fuel_remaining)

    def _solve_branch_and_bound(
        self,
        problem: ConstraintProblem,
        normalized_constraints: List[Constraint],
        rows: List[_FMRow],
        fuel: int,
        initial_state: SolverState,
    ) -> StepResult:
        """Bounded branch-and-bound search for integer / SAT problems."""
        # First solve the continuous linear relaxation
        rel_res = self._solve_continuous(problem, normalized_constraints, rows, fuel, initial_state)
        if not rel_res.is_success:
            return rel_res

        # If continuous relaxation is infeasible, the integer problem is also infeasible
        if isinstance(rel_res.receipt, DualReceipt):
            return rel_res

        assert isinstance(rel_res.receipt, PrimalReceipt)
        witness = rel_res.receipt.witness

        # Check if integer / boolean conditions are satisfied
        fractional_var: Optional[str] = None
        for vname in problem.variables:
            if vname in problem.boolean_vars:
                val = witness[vname]
                if val not in (Fraction(0), Fraction(1)):
                    fractional_var = vname
                    break
            elif vname in problem.integer_vars:
                val = witness[vname]
                if val.denominator != 1:
                    fractional_var = vname
                    break

        if fractional_var is None:
            # All integer/boolean constraints are met!
            return rel_res

        # Branch on the fractional variable
        val = witness[fractional_var]
        fuel_remaining = rel_res.fuel_remaining

        if fuel_remaining <= 0:
            retained = SolverState(
                problem=problem,
                eliminated_variables=(),
                active_constraints=problem.constraints,
                step_count=fuel,
            )
            return StepResult.refuse(
                SolverRefusal(
                    reason=RefusalReason.FUEL_EXHAUSTED,
                    consumed_fuel=fuel,
                    retained_state=retained,
                )
            )

        floor_val = val.numerator // val.denominator
        ceil_val = floor_val + 1

        # Branch Left: fractional_var <= floor_val
        left_bounds = dict(problem.bounds)
        old_bnd = left_bounds.get(fractional_var, VariableBound())
        new_ub = Fraction(floor_val) if old_bnd.upper is None else min(old_bnd.upper, Fraction(floor_val))
        left_bounds[fractional_var] = VariableBound(lower=old_bnd.lower, upper=new_ub)

        prob_left = ConstraintProblem(
            problem_type=problem.problem_type,
            variables=problem.variables,
            constraints=problem.constraints,
            bounds=left_bounds,
            boolean_vars=problem.boolean_vars,
            integer_vars=problem.integer_vars,
        )

        left_res = self.solve(prob_left, fuel=fuel_remaining)
        if left_res.is_success and isinstance(left_res.receipt, PrimalReceipt):
            # Found feasible integer solution!
            left_res.receipt.verify(problem)
            return left_res
        if left_res.is_refusal:
            return left_res

        fuel_remaining = left_res.fuel_remaining
        if fuel_remaining <= 0:
            retained = SolverState(
                problem=problem,
                eliminated_variables=(),
                active_constraints=problem.constraints,
                step_count=fuel,
            )
            return StepResult.refuse(
                SolverRefusal(
                    reason=RefusalReason.FUEL_EXHAUSTED,
                    consumed_fuel=fuel,
                    retained_state=retained,
                )
            )

        # Branch Right: fractional_var >= ceil_val
        right_bounds = dict(problem.bounds)
        old_bnd_r = right_bounds.get(fractional_var, VariableBound())
        new_lb = Fraction(ceil_val) if old_bnd_r.lower is None else max(old_bnd_r.lower, Fraction(ceil_val))
        right_bounds[fractional_var] = VariableBound(lower=new_lb, upper=old_bnd_r.upper)

        prob_right = ConstraintProblem(
            problem_type=problem.problem_type,
            variables=problem.variables,
            constraints=problem.constraints,
            bounds=right_bounds,
            boolean_vars=problem.boolean_vars,
            integer_vars=problem.integer_vars,
        )

        right_res = self.solve(prob_right, fuel=fuel_remaining)
        if right_res.is_success and isinstance(right_res.receipt, PrimalReceipt):
            right_res.receipt.verify(problem)
            return right_res
        if right_res.is_refusal:
            return right_res

        # Both branches are infeasible. Return DualReceipt from relaxation or left branch
        return right_res

    def _back_substitute(
        self,
        problem: ConstraintProblem,
        history: List[Tuple[str, List[_FMRow]]],
    ) -> Dict[str, Fraction]:
        """Back-substitute in reverse elimination order to find exact rational assignment."""
        witness: Dict[str, Fraction] = {}

        for var, rows in reversed(history):
            lowers: List[Fraction] = []
            uppers: List[Fraction] = []

            for r in rows:
                c = r.coeff(var)
                if c != 0:
                    other_sum = Fraction(0)
                    for u, coeff in r.coefficients.items():
                        if u != var:
                            other_sum += coeff * witness.get(u, Fraction(0))
                    rem_rhs = r.rhs - other_sum
                    bnd_val = rem_rhs / c
                    if c > 0:
                        uppers.append(bnd_val)
                    else:
                        lowers.append(bnd_val)

            lb = max(lowers) if lowers else None
            ub = min(uppers) if uppers else None

            is_int_var = var in problem.integer_vars or var in problem.boolean_vars
            is_bool_var = var in problem.boolean_vars

            if is_int_var:
                if lb is not None and ub is not None:
                    # Ceil of lb
                    ceil_lb = -(-lb.numerator // lb.denominator)
                    if ceil_lb <= ub:
                        if is_bool_var:
                            if lb <= 0 <= ub:
                                val = Fraction(0)
                            elif lb <= 1 <= ub:
                                val = Fraction(1)
                            else:
                                val = Fraction(ceil_lb)
                        else:
                            val = Fraction(ceil_lb)
                    else:
                        val = (lb + ub) / 2
                elif lb is not None:
                    ceil_lb = -(-lb.numerator // lb.denominator)
                    if is_bool_var and lb <= 1:
                        val = Fraction(max(0, ceil_lb))
                    else:
                        val = Fraction(ceil_lb)
                elif ub is not None:
                    floor_ub = ub.numerator // ub.denominator
                    if is_bool_var and ub >= 0:
                        val = Fraction(min(1, floor_ub))
                    else:
                        val = Fraction(floor_ub)
                else:
                    val = Fraction(0)
            else:
                if lb is not None and ub is not None:
                    if lb <= ub:
                        val = (lb + ub) / 2
                    else:
                        val = lb
                elif lb is not None:
                    val = lb
                elif ub is not None:
                    val = ub
                else:
                    val = Fraction(0)

            witness[var] = val

        return witness

    @staticmethod
    def _build_multiplier_tuple(total_constraints: int, multipliers: Mapping[int, Fraction]) -> Tuple[Fraction, ...]:
        """Convert a sparse multiplier mapping into an exact dense tuple of non-negative Fractions."""
        res: List[Fraction] = []
        for i in range(total_constraints):
            m = multipliers.get(i, Fraction(0))
            res.append(m)
        return tuple(res)
