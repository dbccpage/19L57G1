# Target M114 / SP-03: Solver Adapter & Bounded Search

AuthorityEffect: None.

## 1. Overview & Scope

Target M114 / SP-03 provides an operational solver boundary adapter mapping external constraint problems into an endogenous demand-and-refusal lifecycle without host oracles or external unpinned solvers.

The package supports four constraint problem classes:
1. **Linear Feasibility**: Quantifier-free linear rational inequalities $A x \le b$ over $\mathbb{Q}^n$.
2. **Bounded SMT**: Linear inequalities with explicit lower and upper rational variable bounds $l_j \le x_j \le u_j$.
3. **Propositional SAT in CNF**: Mapped to 0-1 linear inequalities with boolean variable restrictions.
4. **Bounded Integer Linear Feasibility**: Bounded integer point search with integrality constraints.

## 2. Certified Exact Rational Duality Receipts in $\mathbb{Q}$

To satisfy correction C06 (*"A solved separation demand is not every solver's completed job"*), the solver adapter does not emit ungrounded boolean stamps. Every decision is certified by an exact rational receipt in `fractions.Fraction`:
- **Primal Feasibility Receipt (`PrimalReceipt`)**:
  - Exact rational witness vector $x^* \in \mathbb{Q}^n$.
  - Independent $O(m \cdot n)$ verification checking $A x^* \le b$, variable bounds, and boolean/integer constraints.
  - Verification failure raises `InvalidPrimalCertificateError`.
- **Dual Infeasibility Receipt (`DualReceipt`)**:
  - Exact non-negative rational multiplier vector $y \in \mathbb{Q}_{\ge 0}^m$.
  - Certified Farkas separating hyperplane: $\sum_{i=1}^m y_i A_{ij} = 0$ for all variables $j$, and $\sum_{i=1}^m y_i b_i = c < 0$.
  - Certifies that $0 \le c < 0$, a direct contradiction refuting the existence of any solution.
  - Verification failure raises `InvalidDualCertificateError`.

## 3. Explicit Typed Refusal & State Preservation

When the allocated fuel budget is exhausted before finding either a primal witness or a dual certificate:
- The adapter emits an explicit typed refusal:
  `StepResult.refusal(reason=RefusalReason.FUEL_EXHAUSTED, consumed_fuel=fuel, retained_state=state)`.
- **State Preservation Invariant**: The original constraint problem and intermediate state remain completely unmutated.
- **Refusal Semantics**: The solver never fabricates a decision, never defaults to "satisfiable" or "unsatisfiable" upon budget exhaustion, and does not mutate host configuration.

## 4. Constructive Lean 4 Formalization

The formalization in `lean/SolverAdapter.lean` establishes:
- `primal_soundness`: An assignment satisfying all constraints certifies feasibility.
- `int_nat_mul_le_mul`: Non-negative scaling preserves integer inequalities.
- `dual_combination_le`: Non-negative linear combination of satisfied constraints bounds the combined LHS by the combined RHS.
- `farkas_dual_soundness`: Existence of non-negative multipliers cancelling all variable coefficients with negative combined RHS constructively refutes feasibility.
- `fuel_monotonicity`: Operational transitions decrement fuel by exactly 1.
- `refusal_preserves_state`: Refusal transitions preserve the underlying problem representation unchanged.

Axiom audit (`lean/Inventory.lean`):
- Dependencies are strictly contained in `{propext, Quot.sound}`.
- Zero `Classical.choice`. Zero `mathlib`.

## 5. Claim Hygiene Summary

1. **What it supports**: Exact rational certificate generation and verification for finite linear feasibility, bounded SMT, and bounded boolean/integer problems under declared finite fuel.
2. **What it does not support**: Universal decision of arbitrary non-linear arithmetic, undecidable fragments, or infinite-horizon search.
3. **Narrowest defensible claim**: Operational solver boundary adapter produces exact rational primal witnesses or Farkas separating hyperplanes under declared finite fuel, and preserves state upon refusal.
4. **Next test needed**: Integration with Alpha Engine search policy extensions and Driver A multi-key exploration.
