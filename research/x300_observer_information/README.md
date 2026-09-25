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

## Correction, 2026-09-24: a row that does not sum to 1 is refused

Until this date `DiscreteDistribution` divided a row whose probabilities did not sum to 1 by that sum, so a malformed input distribution or channel row was silently replaced by a different, valid one. The package list above says the test suite exercises "distribution normalization"; that phrase referred to this rescaling. The constructor now raises `UnnormalizedDistributionError`, a `ValueError` naming the sum, as `research/p204_operational_valuations` raises on such a row and `research/p208b_contextuality_nonlocality` rejects one. `tests/test_information.py` holds five negative tests for the refusal.

No committed result depended on a rescaled row. An instrumented run of the 18 tests then present built 160 distributions, and every row summed to exactly 1. In `evidence/receipt.json` only the pytest count (18 to 23) and the source hashes of `information.py` and `tests/test_information.py` moved. No Lean statement is affected.
