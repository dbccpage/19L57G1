# Claims Ledger: Target M114 / SP-03 (Solver Adapter & Bounded Search)

## 1. What it supports

1. **Operational Solver Boundary Interface**:
   Supports a deterministic interface mapping constraint problems across four problem classes (propositional SAT in CNF, bounded SMT linear rational inequalities, linear feasibility, and bounded integer feasibility) into an endogenous demand-and-refusal lifecycle without external solver oracles.
2. **Exact Rational Primal Witnesses in $\mathbb{Q}$**:
   Supports generation and independent $O(m \cdot n)$ verification of exact rational witness vectors $x^* \in \mathbb{Q}^n$ represented via `fractions.Fraction`, certifying primal feasibility against linear constraints, variable bounds, and boolean/integer restrictions.
3. **Certified Exact Rational Farkas Dual Receipts**:
   Supports generation and independent verification of exact non-negative dual multiplier vectors $y \in \mathbb{Q}_{\ge 0}^m$ satisfying $\sum_{i=1}^m y_i A_{ij} = 0$ for all variables $j$ and $\sum_{i=1}^m y_i b_i = c < 0$, constructively witnessing *linear* infeasibility via the separating hyperplane certificate $0 \le c < 0$. When the LP relaxation is feasible but no integer point exists, `solve()` emits `IntegerInfeasibilityReceipt`: both integer branches of the fractional witness carry child certificates that `verify()` against the original problem plus the integer cut. A child `DualReceipt` does not verify on the uncut original (linear Farkas of $Ax \le b$ cannot exist in that case).
4. **Typed Refusal & State Preservation Under Bounded Exhaustion**:
   Demonstrates explicit typed refusal (`StepResult.refusal`) when the finite search fuel budget is exhausted, preserving the original problem representation and intermediate state without mutation or default boolean hallucination.
5. **Constructive Formalization**:
   Establishes constructive Lean 4 formalization of primal soundness, Farkas dual soundness, fuel decrement monotonicity, and refusal state preservation in `lean/SolverAdapter.lean`, with `#print axioms` verified strictly in `{propext, Quot.sound}` (3 theorems axiom-free, 3 theorems dependent only on `propext`, zero `mathlib`, zero `Classical.choice`).

## 2. What it does not support

1. Does not support undecidable non-linear polynomial or transcendental arithmetic; all constraints are linear.
2. Does not support infinite-horizon search or unbounded variable branching without declared fuel limits.
3. Does not claim that an empty separation demand in an engine tie-set solves an arbitrary external SMT or SAT problem without an explicit verified certificate (adhering to Correction C06).
4. Does not provide asymptotic complexity guarantees beyond declared bounded step accounting.

## 3. The narrowest defensible claim

Under declared finite fuel bounds, the operational solver boundary adapter either constructs an exact rational primal feasibility witness in $\mathbb{Q}^n$ or an exact rational Farkas separating hyperplane certificate in $\mathbb{Q}_{\ge 0}^m$, or emits an explicit typed refusal preserving the problem state unchanged.

## 4. The next test needed

End-to-end integration into Alpha Engine search policies (`search_policy.py`) to drive multi-key licensed exploration across bounded solver steps under strict `PolicyCensus` disjoint cover invariants.
