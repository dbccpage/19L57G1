# redheffer: claims

AuthorityEffect: None.

### CL-REDHEFFER
- **Statement**: Verifies `det(R_n) = M(n)` for n≤6 via `decide +kernel`. The general-n theorem is transitivity of the conjuncts packed into `ColumnReductionEquivalence`, not an independent column-reduction proof. Python oracle to n=20. `|arrangements(n)| = n!` is permutation counting.
- **Evidence**: Lean finite checks; `adversarial_oracle.py`.
- **Falsifier**: a counterexample showing det(R_n) ≠ M(n) for n≤6.
