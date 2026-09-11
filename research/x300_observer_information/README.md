# Target X300: Observer-Relative Information, Channels & Loss

This package implements and verifies observer-relative information models, operational communication channels between distributed observers, the Data Processing Inequality (DPI), exact rational dyadic operational uncertainty, Hartley capacity metrics, memory degradation limits, and Landauer operational erasure accounting.

## Package Structure

- `information.py`: Core Python operational information library implementing:
  - Exact rational discrete probability distributions in $\mathbb{Q}$.
  - Dyadic distributions with exact rational Shannon uncertainty and divergence in $\mathbb{Q}$.
  - Hartley capacity metrics over discrete observation alphabets.
  - Operational communication channels with Markov concatenation and composition.
  - Data Processing Inequality verification for general and deterministic post-processing.
  - Distributed observer communication protocols and transmission fidelity calculations.
  - Memory retention models and lossy coarse-graining projections.
  - Landauer operational erasure accounting and thermodynamic lower bounds.
- `tests/test_information.py`: Pytest suite exercising distribution normalization, exact dyadic divergence, Hartley additivity, channel composition associativity, DPI across diverse channel cascades, repetition coding protocols, memory retention monotonicity, and Landauer erasure accounting.
- `lean/ObserverInformation.lean`: Constructive core Lean 4 formalization containing 17 theorems covering channel composition, DPI for distinguishability and decodability, sufficient statistic preservation, additive Hartley capacity, scaled dyadic uncertainty, sequential memory retention monotonicity, and Landauer operational erasure non-reversibility.
- `lean/Inventory.lean`: Lean 4 theorem census and axiom dependency audit confirming zero Classical.choice, zero mathlib, and axioms strictly within `{propext, Quot.sound}` (16 axiom-free, 1 depending only on propext).
- `verify.py`: Top-level verification harness executing source hygiene checks, pytest suite, `lake build`, and Lean axiom audits, emitting `evidence/receipt.json`.
- `evidence/receipt.json`: Signed verification receipt recording source file sha256 hashes, test counts, and theorem audits.

## Execution and Verification

Run the verification harness:

```bash
python verify.py --check
```
