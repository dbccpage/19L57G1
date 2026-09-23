# CLAIMS — G013 Coherent Trace Calculus & Higher Cell Algebra

This ledger documents the formal claims, constructive definitions, theorems, empirical test suites, and verification receipts established in `research/g013_trace_calculus/`.

## Authority & Integrity Posture
- AuthorityEffect: None.
- Constructive Axiom Bound: `#print axioms` strictly contained in `{propext, Quot.sound}` (zero `Classical.choice`, zero mathlib).
- Repository Isolation: Zero edits outside `research/g013_trace_calculus/`.

---

## Claim Ledger

### 1. 0-Cells and 1-Cells (Traces)

| ID | Formal Name / Declaration | Description | Status | Evidence Path |
|:---|:---|:---|:---|:---|
| **C01** | `G013TraceCalculus.Trace` | Inductive definition of 1-cells as chained steps between 0-cells | VERIFIED | `lean/Trace.lean`, `trace.py` |
| **C02** | `G013TraceCalculus.concat` | 1-cell composition operator with endpoint boundary checks | VERIFIED | `lean/Trace.lean`, `trace.py` |
| **C03** | `G013TraceCalculus.nil_concat` | Left identity theorem: `nil * p = p` | VERIFIED | `lean/Trace.lean`, `tests/test_trace.py` |
| **C04** | `G013TraceCalculus.concat_nil` | Right identity theorem: `p * nil = p` | VERIFIED | `lean/Trace.lean`, `tests/test_trace.py` |
| **C05** | `G013TraceCalculus.concat_assoc` | Strict associativity of trace concatenation: `(p * q) * r = p * (q * r)` | VERIFIED | `lean/Trace.lean`, `tests/test_trace.py` |
| **C06** | `G013TraceCalculus.length_concat` | Additivity of trace length under composition | VERIFIED | `lean/Trace.lean`, `tests/test_trace.py` |

### 2. Higher 2-Cells and Replay Equivalences

| ID | Formal Name / Declaration | Description | Status | Evidence Path |
|:---|:---|:---|:---|:---|
| **C07** | `G013TraceCalculus.Cell2` | Inductive syntax of 2-cells between parallel traces; `step_comm` admits any parallel two-step routes | VERIFIED | `lean/HigherCell.lean`, `higher_cell.py` |
| **C08** | `G013TraceCalculus.v_comp` | Vertical composition of 2-cells: `(beta circ_1 alpha) : p => r` | VERIFIED | `lean/HigherCell.lean`, `higher_cell.py` |
| **C09** | `G013TraceCalculus.h_comp` | Horizontal composition of 2-cells: `(alpha circ_0 beta) : p1 * p2 => q1 * q2` | VERIFIED | `lean/HigherCell.lean`, `higher_cell.py` |
| **C10** | `G013TraceCalculus.interchange_source_coherence` | Reflexive equality of the shared source trace | VERIFIED | `lean/HigherCell.lean`, `tests/test_higher_cells.py` |
| **C11** | `G013TraceCalculus.interchange_target_coherence` | Reflexive equality of the shared target trace | VERIFIED | `lean/HigherCell.lean`, `tests/test_higher_cells.py` |
| **C12** | `verify_interchange_law` | Python comparison of the two constructed interchange terms | VERIFIED | `higher_cell.py`, `tests/test_higher_cells.py` |

### 3. General Endpoint Factorization

| ID | Formal Name / Declaration | Description | Status | Evidence Path |
|:---|:---|:---|:---|:---|
| **C13** | `G013TraceCalculus.future_factors_through_endpoint` | Constructive proof that deterministic continuations factor through intermediate state | VERIFIED | `lean/Factorization.lean`, `factorization.py` |
| **C14** | `G013TraceCalculus.future_factors_through_endpoint_guarded` | Constructive proof that guarded continuations factor through intermediate state | VERIFIED | `lean/Factorization.lean` |
| **C15** | `G013TraceCalculus.future_factors_through_endpoint_1cell` | Categorical 1-cell formulation: target alignment under suffix extension | VERIFIED | `lean/Factorization.lean` |
| **C16** | `sweep_factorization_grid` | Exhaustive factorization sweeps over 2D grid, diamond DAG, and cyclic machines | VERIFIED | `factorization.py`, `tests/test_endpoint_factorization.py` |

### 4. Observer Trace Congruence

| ID | Formal Name / Declaration | Description | Status | Evidence Path |
|:---|:---|:---|:---|:---|
| **C17** | `G013TraceCalculus.ObserverCongruent` | Observer congruence relation across all execution continuation paths | VERIFIED | `lean/Congruence.lean`, `congruence.py` |
| **C18** | `G013TraceCalculus.observer_congruent_step` | Invariance of observer congruence under single-step transition | VERIFIED | `lean/Congruence.lean` |
| **C19** | `G013TraceCalculus.observer_congruent_immediate` | Congruent states possess identical immediate observation readouts | VERIFIED | `lean/Congruence.lean` |
| **C20** | `G013TraceCalculus.quotient_zero_residuals` | Zero unrecorded residuals: congruent states agree on all observations | VERIFIED | `lean/Congruence.lean`, `tests/test_observer_congruence.py` |
| **C21** | `audit_observer_residuals` | Python audit identifying zero unrecorded residuals and detecting discrepancies | VERIFIED | `congruence.py`, `tests/test_observer_congruence.py` |

### 5. Additive Trace Prices and Conditional Cell Price Equality

| ID | Formal Name / Declaration | Description | Status | Evidence Path |
|:---|:---|:---|:---|:---|
| **C22** | `G013TraceCalculus.price_concat_additive` | Trace price additivity: `C(p * q) = C(p) + C(q)` | VERIFIED | `lean/Price.lean`, `price.py` |
| **C23** | `G013TraceCalculus.price_commute_invariance` | Equality of two diamond prices given equality of branch-cost sums | VERIFIED | `lean/Price.lean`, `price.py` |
| **C24** | `G013TraceCalculus.price_h_comp_invariance` | Horizontal composition preserves price equality | VERIFIED | `lean/Price.lean`, `tests/test_price.py` |
| **C25** | `G013TraceCalculus.price_v_comp_invariance` | Vertical composition preserves price equality | VERIFIED | `lean/Price.lean`, `tests/test_price.py` |
| **C26** | `audit_2cell_homotopy_invariance` | Python audit of price equality for its selected composite cell sets; historical function name | VERIFIED | `price.py`, `tests/test_price.py` |

---

## Artifact Claim Hygiene Assessment

1. **What It Supports**:
   - Demonstrates in constructive Lean 4 that execution traces form a strict 1-category with associative concatenation and identity traces.
   - Defines 2-cell syntax between parallel traces and includes interchange as a declared generator of `EqCell2`; source and target alignment are reflexive equalities.
   - Demonstrates that future trajectories from any history factor strictly through the terminal endpoint for deterministic and guarded systems.
   - Demonstrates that observer trace congruence preserves continuation observations without unrecorded residuals.
   - Proves additive trace prices and conditional equality when the two diamond branches have equal costs.

2. **What It Does Not Support**:
   - Does not establish completeness of finite 2-cell rewrites for undecidable execution systems.
   - Does not claim that all real-world observers admit finite projective descriptions.
   - Does not model continuous-time or non-discrete dynamical manifolds.

3. **Narrowest Defensible Claim**:
   For the declared directed-graph syntax, traces compose with identities and associativity, and the conditional endpoint, observation, and price statements hold. `Cell2` and `EqCell2` are presentations of candidate higher cells; this package does not establish a strict 2-category or a guarded native replay equivalence.

4. **Next Test Needed**:
   Prove the vertical and horizontal unit and associativity laws, compatibility of composition with a specified quotient, and a bridge from each nontrivial cell to permitted guarded native steps before expanding the cell syntax.
