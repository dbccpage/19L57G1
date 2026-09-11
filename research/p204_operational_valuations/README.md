# Target P204: Operational Valuations & Convex State Spaces

## Overview
This directory implements and formalizes operational valuations and convex state spaces in finite discrete systems using exact rational arithmetic.

The operational framework represents:
1. Finite discrete outcome spaces $\Omega$.
2. Operational states as exact rational probability valuations $s: \Omega \to \mathbb{Q} \cap [0, 1]$ satisfying $\sum_{\omega \in \Omega} s(\omega) = 1$.
3. Operational effects as response functions $e: \Omega \to \mathbb{Q} \cap [0, 1]$ with unit effect $u(\omega) = 1$.
4. Operational valuation pairing $\langle e, s \rangle = \sum_{\omega \in \Omega} e(\omega) s(\omega)$, satisfying $\langle u, s \rangle = 1$ for all normalized states.
5. Convex mixtures of preparations $\sum_i p_i s_i$ and operational effects $\sum_j q_j e_j$.
6. Bilinearity of state-effect valuation: $\langle \sum_j q_j e_j, \sum_i p_i s_i \rangle = \sum_{j, i} q_j p_i \langle e_j, s_i \rangle$.
7. Distinction between classical simplex state spaces (where every state admits a unique convex decomposition into extreme indicator states) and general convex state spaces (such as the discrete 4-vertex square state space where mixed states admit non-unique convex decompositions into extreme states).
8. Tensor composition and operational non-signaling across bipartite cuts: for any operational partition of unity $\sum_i e_{A, i} = u_A$ on subsystem $A$ and test effect $e_B$ on subsystem $B$, the joint expectation satisfies $\sum_i \langle e_{A, i} \otimes e_B, s_{AB} \rangle = \langle u_A \otimes e_B, s_{AB} \rangle = \langle e_B, s_B \rangle$.

## Structure
- `valuations.py`: Pure Python module with exact rational arithmetic (`fractions.Fraction`).
- `tests/test_valuations.py`: Pytest suite covering all operational properties, edge cases, and negative controls.
- `pyproject.toml`: Package configuration with `pythonpath = ["."]`.
- `lean/`:
  - `lakefile.toml`: Lake configuration referencing `../../../lean4`.
  - `lean-toolchain`: Lean version pin (`leanprover/lean4:v4.33.0`).
  - `OperationalValuations.lean`: Constructive formalization in Lean 4 (zero mathlib, zero `Classical.choice`).
  - `Inventory.lean`: Metatheoretic census auditing all 85 theorems against `{propext, Quot.sound}`.
- `verify.py`: Independent verification harness.
- `evidence/receipt.json`: Audit receipt recording file hashes and verification metrics.
- `CLAIMS.md`: Claim ledger documenting what the implementation supports, bounds, and limits.

## Verification
Run verification with:
```bash
python verify.py --check
```
