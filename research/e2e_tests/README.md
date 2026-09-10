# Genesis Cohort 2 E2E Test Suite

## Overview
This directory contains the comprehensive, requirement-driven opaque-box E2E test suite for Genesis Cohort 2 (Foundational Architecture & Execution Substrate), covering all 16 features inventoried in `PROJECT.md` across 4 verification tiers:

- **Tier 1 (Feature Coverage)**: At least 5 tests per inventoried feature (80 tests total across the 16 features from PROJECT.md).
- **Tier 2 (Boundary & Corner Cases)**: At least 5 tests per feature covering zero fuel, empty carrier, single vs multiple enablements, malformed regimes, address collisions, boundary scale prefixes, and unreached ordinals (80 tests total).
- **Tier 3 (Cross-Feature Combinations)**: Pairwise integration tests exercising interface contracts (Target A execution driving G010 capability removal, G011 finitary ordinals addressing Target A instruction memory, Target B prefix observation of Target A traces, G001 adequacy verification of Target A & B).
- **Tier 4 (Real-World Application Scenarios)**: Realistic multi-step workloads (complete autonomous program loop, cyclic process limiting frequency convergence, full 9-criteria charter evaluation of an admitted substrate, endogenous self-modifying execution pipeline).

## Directory Layout
```
research/e2e_tests/
|-- README.md              # Test suite documentation and overview
|-- TEST_INFRA.md          # Test infrastructure and partition specification
|-- TEST_READY.md          # Formal verification readiness declaration
|-- harness.py             # Opaque-box execution harness and reference models
|-- run_all_tests.py       # Master test runner discovering and executing all 4 tiers
`-- suites/
    |-- tier1_features.py    # Tier 1: Feature coverage (80 tests)
    |-- tier2_boundaries.py  # Tier 2: Boundary & corner cases (80 tests)
    |-- tier3_pairwise.py    # Tier 3: Cross-feature combinations (8 tests)
    `-- tier4_workloads.py   # Tier 4: Real-world application workloads (4 tests)
```

## Running the Tests
To execute all test tiers using the standalone verification runner:
```bash
python research/e2e_tests/run_all_tests.py
```

To run with pytest:
```bash
pytest research/e2e_tests/suites/
```

## Epistemic Posture & Claim Discipline
In accordance with the Claim Hygiene Rule, all assertions and tests demonstrate properties within the declared constructive toy models and finite bounds. No unencoded host oracles or infinite continuous assumptions are invoked.
