# Test Infrastructure & Methodology Specification

## 1. Overview & Epistemic Posture
This document specifies the test infrastructure, partition framework, and verification methodology for the Genesis Cohort 2 E2E test suite housed in `research/e2e_tests/`.

The test suite enforces the transition from static graph encodings to verified autonomous dynamics and foundational metatheoretic substrates across five core domains:
- **Target A (Represented Execution Substrate)**: Features 1-4
- **Target B (Coherent Observation Scales & Dynamics)**: Features 5-8
- **G001 (TOE Target-Class Charter)**: Features 9-10
- **G010 (Semantic Primitive Removal)**: Features 11-12
- **G011 (Internal Finitary Substrate)**: Features 13-15
- **Comprehensive E2E Verification & Governance**: Feature 16

### Claim Hygiene Posture
Every test case in this suite adheres to the Claim Hygiene Rule:
- All claims are scoped to the declared toy models and constructive bounds.
- No ungrounded claims of physical reality, infinite continua, or unencoded oracles are permitted.
- The suite operates under strict local execution without hosted CI reliance.

---

## 2. Category-Partition Framework (Tier 1)
The feature coverage tier (Tier 1) partitions the input and state space for each of the 16 features into well-defined equivalence classes, requiring at least 5 distinct test cases per feature (80 tests total).

### Feature 1: Represented Program & Lookup
- **P1.1 (Valid Edge Lookup)**: Lookup finds edge `(3 + k, [x, y])` and returns `y`.
- **P1.2 (Missing Edge Lookup)**: Lookup on absent source datum returns `None`.
- **P1.3 (Form Separation)**: Lookup with different form indices strictly separates distinct operation graphs.
- **P1.4 (Zero Host Oracle)**: Execution proceeds reading graph instances without consulting unencoded operation functions.
- **P1.5 (Multi-Edge Graph)**: Lookup distinguishes multiple edges within the same operation graph.

### Feature 2: Data-Driven Control & Branching
- **P2.1 (Unique Enablement Step)**: Exactly one enablement active fires the corresponding operation and advances state.
- **P2.2 (Zero Enablement Halt)**: No enablement active returns the terminal `HALT`.
- **P2.3 (Fork Refusal Branch)**: Multiple enablements active return the terminal `BRANCH` without silent selection.
- **P2.4 (Tape Extension)**: Each fired step appends the visited datum to the observable tape.
- **P2.5 (Monotonic Fuel Expenditure)**: Each fired step decrements fuel by exactly 1 and advances clock by 1.

### Feature 3: Memory Growth & Retained Records
- **P3.1 (Depth-1 Trace Record)**: Stepping records predecessor-successor pairs `[p, x]`.
- **P3.2 (Depth-2 Ternary Form)**: Stepping with tape length >= 3 records ternary history `[b, p, x]`.
- **P3.3 (Memory Expansion Invariant)**: Memory store grows monotonically with execution steps.
- **P3.4 (Historical Integrity)**: Retained records remain immutable throughout subsequent steps.
- **P3.5 (No Host Memory Shortcut)**: Memory records are constructed solely from observable execution states.

### Feature 4: Multi-Locus Independence
- **P4.1 (Product Pairing Bijectivity)**: Unpack inverses pack across finite bounds.
- **P4.2 (Independence Square Commutation)**: Disjoint locus transitions commute on state outcome.
- **P4.3 (Coupled Interaction Breakdown)**: Cross-locus dependencies break commutativity.
- **P4.4 (Local Stepping Invariance)**: A step on locus A does not alter the datum of locus B.
- **P4.5 (Multi-Step Independence)**: Sequences of disjoint locus operations commute across paths.

### Feature 5: Prefix Observation Scale System
- **P5.1 (Scale Projection Bond)**: `bond(c, n)` projects scale `n+1` to `n` by forgetting the last element.
- **P5.2 (Prefix Compatibility)**: Observation at scale `n` is a prefix of observation at scale `n + k`.
- **P5.3 (Inverse Limit Chain)**: Scale maps form a coherent inverse system over finite stages.
- **P5.4 (Fuel Independence)**: Observation at scale `n` is invariant under all fuel allocations >= `n`.
- **P5.5 (Scale Consistency)**: Repeated observations at identical scale yield identical prefixes.

### Feature 6: Sequence Space Limit Bijection
- **P6.1 (Thread to Sequence Map)**: Compatible threads map constructively to infinite sequence representations.
- **P6.2 (Sequence to Thread Map)**: Sequence representations induce compatible finite thread stages.
- **P6.3 (Two-Sided Inversion)**: `to_seq` and `of_seq` are two-sided inverses.
- **P6.4 (Refusal of Lax Agreement)**: Non-compatible threads violating prefix bonding are rejected.
- **P6.5 (Cofinal Subscale Invariance)**: Even-scale restriction preserves thread identity.

### Feature 7: Non-Density via Chain Functionality
- **P7.1 (Chain Functionality Satisfaction)**: Deterministic process traces satisfy single-valued successor relations.
- **P7.2 (Chain Functionality Refusal)**: Non-functional prefixes (e.g. `[0, 1, 0, 2]`) are rejected as non-realizable.
- **P7.3 (Evaluation Injectivity)**: Distinct execution trajectories produce distinct tape observations.
- **P7.4 (Topological Non-Density)**: The set of realized tapes is strictly non-dense in the full thread space.
- **P7.5 (Cycle Trace Functionality)**: Cyclic executions preserve chain functionality across arbitrary lengths.

### Feature 8: Commuting Dynamics Square
- **P8.1 (Operational Commutation)**: Commutation on compatible state embeddings.
- **P8.2 (Lost Fuel Obstruction)**: State projections forgetting fuel fail to commute across steps.
- **P8.3 (Non-Local Shift Obstruction)**: Tape window shifts fail to commute with prefix projections.
- **P8.4 (3-Cycle Rational Frequency)**: Limiting frequency of datum 0 on 3-cycle program satisfies `L <= 3 * zeros <= L + 2`.
- **P8.5 (Precision Budget Convergence)**: Rational error bound strictly decreases as `2 / (3L)`.

### Feature 9: 9-Criteria Target-Class Charter
- **P9.1 (Frozen Charter Dimensions)**: The 9 adequacy criteria are pre-registered and invariant.
- **P9.2 (Computational Capacity Evaluation)**: Target system evaluates computational adequacy dimension.
- **P9.3 (Mathematical Foundation Evaluation)**: Target system evaluates constructive mathematical adequacy.
- **P9.4 (Physical & Empirical Evaluation)**: Target system evaluates observational and calibration criteria.
- **P9.5 (Non-Circular Verification)**: Pre-registration prevents post-hoc self-definition.

### Feature 10: Comparison Morphism Category
- **P10.1 (Identity Morphism)**: Identity comparison morphism satisfies domain-codomain identity.
- **P10.2 (Morphism Composition)**: Compatible comparison morphisms compose associatively.
- **P10.3 (Adequacy Preservation)**: Morphisms preserve verified adequacy evidence.
- **P10.4 (Composition Identity Laws)**: Identity laws hold for morphism composition.
- **P10.5 (Categorical Domain Guard)**: Composition of mismatched domains raises an explicit error.

### Feature 11: Operational Capability Removal
- **P11.1 (Genuine Syntactic Absence)**: Candidate primitive is removed from available capability set.
- **P11.2 (Restricted Interpreter Execution)**: Tasks requiring only retained capabilities execute successfully.
- **P11.3 (Operational Refusal on Removed Primitive)**: Tasks requiring removed capability refuse or halt.
- **P11.4 (Fixed Comparison Interface)**: Public observation channel remains identical across before/after systems.
- **P11.5 (Zero Output Leakage)**: Removed capability produces no synthetic side channels.

### Feature 12: Constructive Obstruction Proofs
- **P12.1 (Direct Obstruction Witness)**: Formal witness shows task failure under capability restriction.
- **P12.2 (Adapter Bypass Refusal)**: Unpriced host adapters attempting to emulate removed capability are rejected.
- **P12.3 (Structural Derivation)**: Obstruction is derived from code paths, not post-hoc lookup tables.
- **P12.4 (Capability Monotonicity)**: Subsets of capabilities cannot solve super-capability tasks.
- **P12.5 (Obstruction Soundness)**: Restoring capability restores execution success.

### Feature 13: Endogenous Identity & Ordinals
- **P13.1 (Inductive Zero)**: Base ordinal zero representation.
- **P13.2 (Inductive Successor)**: Successor generates unique subsequent ordinals.
- **P13.3 (Trichotomy & Order)**: Finitary ordinals satisfy exact trichotomy.
- **P13.4 (Zero Predecessor Guard)**: Predecessor of zero raises an explicit exception.
- **P13.5 (No Host Pointer Dependence)**: Ordinal identity is independent of host memory addresses.

### Feature 14: Tree Addresses & Freshness
- **P14.1 (Root Address Structure)**: Root address forms tree base.
- **P14.2 (Hierarchical Extension)**: Extending an address generates a distinct sub-address.
- **P14.3 (Deterministic Freshness)**: Fresh address generator allocates disjoint addresses monotonically.
- **P14.4 (Zero Address Collision)**: Distinct allocation paths yield strictly unequal tree addresses.
- **P14.5 (Prefix Sub-Tree Invariance)**: Address prefixes accurately reflect tree containment.

### Feature 15: Fuel-Bounded Endogenous Recursion
- **P15.1 (Base Case Termination)**: Zero ordinal depth terminates immediately with success.
- **P15.2 (Inductive Step Evaluation)**: Successor ordinal depth decrements and computes output.
- **P15.3 (Fuel Exhaustion Guard)**: Insufficient fuel halts recursion before completion.
- **P15.4 (Strict Fuel Monotonicity)**: Fuel is strictly decremented by 1 at each recursion step.
- **P15.5 (Total Boundedness)**: Structural recursion terminates within bounded fuel.

### Feature 16: Comprehensive E2E Verification & Governance
- **P16.1 (4-Tier Suite Discovery)**: All 4 test tiers are discoverable and executable.
- **P16.2 (Exit Code Contract)**: Test runner exits with 0 on 100% pass, non-zero on failure.
- **P16.3 (Lean Axiom Census Compliance)**: Proof axioms strictly within `{propext, Quot.sound}`.
- **P16.4 (Vocabulary Firewall)**: Zero denylist tokens leak into codebase.
- **P16.5 (Claim Hygiene Enforcement)**: All claims reflect constructive bounds and narrow scopes.

---

## 3. Boundary Value Analysis (BVA) Framework (Tier 2)
Tier 2 targets boundary conditions, extreme states, and corner cases across all 16 features (80 tests total):
1. **Fuel Boundaries**: `fuel = 0` (instant exhaustion), `fuel = 1`, `fuel = steps - 1`, `fuel = steps`, negative fuel rejection.
2. **Carrier Boundaries**: Carrier of size 1 (loop on self), carrier of size 2, large carrier, empty carrier rejection.
3. **Enablement Boundaries**: Empty enablement (instant `HALT`), single enablement (deterministic step), dual enablement (instant `BRANCH`), multi-enablement (branch without selection), missing edge enablement (`REFUSE`).
4. **Scale Boundaries**: Prefix scale 0 (singleton tape), scale 1 (start datum), boundary scale N, out-of-bounds scale request.
5. **Ordinal Boundaries**: Zero ordinal, large finite ordinal, predecessor of zero refusal, successor comparison.
6. **Address Boundaries**: Root address, deep tree nesting, branch collisions, disjoint siblings.
7. **Charter Boundaries**: Subsystem satisfying 0/9 criteria, 8/9 criteria (borderline failure), exactly 9/9 criteria (full pass).
8. **Capability Boundaries**: Empty capability set, singleton capability, full capability set, conflicting capability requirements.

---

## 4. Pairwise Combinatorial Framework (Tier 3)
Tier 3 exercises cross-feature combinations and interface contracts:
- **T3.1 (Target A x G010)**: Target A execution driving G010 capability removal across a fixed observation interface.
- **T3.2 (Target A x G011)**: G011 finitary ordinals addressing Target A instruction memory and active states.
- **T3.3 (Target A x Target B)**: Target B prefix scale observation observing Target A execution traces.
- **T3.4 (G001 x Target A & Target B)**: G001 adequacy charter evaluating Target A execution and Target B dynamics.
- **T3.5 (Multi-Locus x G011)**: Two-locus product pairing mapped to G011 hierarchical tree addresses.
- **T3.6 (Memory Growth x Target B)**: Target A depth-2 memory records verified against Target B chain functionality.
- **T3.7 (G010 x G011)**: Fuel-bounded endogenous recursion executing under restricted capability environments.
- **T3.8 (Target B x G001)**: Quantitative rational limiting bounds evaluated as empirical adequacy evidence under G001.

---

## 5. Real-World Workload Scenarios (Tier 4)
Tier 4 tests multi-step, end-to-end operational workflows:
- **T4.1 (Complete Autonomous Program Loop)**: Full cycle: loading encoded program graph, data-driven execution, memory record accumulation, terminal classification.
- **T4.2 (Cyclic Frequency Convergence)**: Execution of 3-cycle program across scales 3, 6, 12, 24, 48, computing rational frequencies and verifying convergence to 1/3 within `epsilon <= 2/(3L)`.
- **T4.3 (Full 9-Criteria Charter Evaluation)**: End-to-end evaluation of an admitted substrate candidate against all 9 charter criteria, generating a complete formal admission receipt.
- **T4.4 (Endogenous Synthesis & Execution Pipeline)**: G011 address allocation -> program generation -> Target A execution -> capability removal verification.

---

## 6. Test Execution & Verification Protocol
- **Runner**: `python research/e2e_tests/run_all_tests.py`
- **Pytest**: `pytest research/e2e_tests/suites/`
- **Exit Code**: Returns `0` if and only if 100% of tests across all 4 tiers pass.
