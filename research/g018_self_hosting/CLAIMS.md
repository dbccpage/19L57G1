# Claims Ledger: G018 Self-Hosting, Internal Simulation & Reflection Boundary

This document formalizes the claims ledger for **G018 (Self-Hosting, Internal Simulation & Reflection Boundary)**,
specifying the mathematical definitions, constructive Lean 4 theorems, Python verification mirrors,
and epistemic boundaries.

AuthorityEffect: None.  
Terminal: `SELF_HOSTING_SIMULATION_ESTABLISHED`.

---

## Claims Summary Table

| Claim ID | Scope | Lean 4 Theorems | Python Mirror | Axiom Reliance | Status |
|---|---|---|---|---|---|
| **CL-G018-01** | Carrier Representation & Transitions | `stepMachine_halted`, `stepMachine_zero_fuel`, `stepMachine_fuel_decrement` | `test_carrier_repr.py` | None (0 axioms) / `{propext, Quot.sound}` | VERIFIED |
| **CL-G018-02** | Internalized Step-Simulation Correctness | `step_simulation_correctness`, `step_simulation_extract_commutes`, `sim_embed_extract_id` | `test_step_simulation_correctness_single_cycle`, `test_micro_step_simulation_k_steps` | `{propext, Quot.sound}` | VERIFIED |
| **CL-G018-03** | Termination & Invariant Preservation | `stepCarrier_zero_host_fuel`, `stepCarrier_guest_halted`, `stepCarrier_guest_zero_fuel`, `runCarrier_halted` | `test_multi_step_simulation_equivalence`, `test_direct_execution_counter` | None (0 axioms) | VERIFIED |
| **CL-G018-04** | Reflection Boundary Fuel Exhaustion | `reflection_fuel_closed_form`, `reflection_fuel_monotone`, `reflection_capacity_limit`, `reflection_boundary_exhaustion` | `test_fuel_required_calculation`, `test_max_reflection_depth`, `test_reflection_tower_fuel_exhaustion` | None (0 axioms) / `{propext, Quot.sound}` | VERIFIED |
| **CL-G018-05** | State Capacity Limit (Pigeonhole) | `carrier_state_pigeonhole_step`, `hasMatchNat_true`, `hasMatchNat_false` | `test_state_capacity_pigeonhole_collision`, `test_state_capacity_no_collision_when_sufficient` | None (0 axioms) | VERIFIED |
| **CL-G018-06** | Conditional Boolean self-negation and bounded predictor probes | `bool_neq_not_self`, `diagonal_self_evaluation_obstruction`, `halting_self_oracle_obstruction`, `total_transition_oracle_refutation` | `test_diagonal_machine_semantics`, `test_refute_always_halt_oracle`, `test_comprehensive_predictor_sweep`, `test_exact_finite_predictor_is_not_artificially_refuted` | None (0 axioms) | VERIFIED within stated scope |
| **CL-G018-07** | Constructive Metatheoretic Boundary | Census in `lean/Inventory.lean` (71 declarations) | `verify.py` audit | Strictly within `{"propext", "Quot.sound"}` | VERIFIED |

---

## Detailed Claim Specifications

### CL-G018-01: Carrier Representation & Transitions
- **Statement:** An execution engine's own operational states and transition graphs are encoded within the object carrier. Active operational steps decrement fuel by 1, and terminated states remain invariant under further steps.
- **Formal Theorems:**
  - `G018SelfHosting.stepMachine_halted`
  - `G018SelfHosting.stepMachine_zero_fuel`
  - `G018SelfHosting.stepMachine_fuel_decrement`
- **Claim Hygiene:**
  1. *Supports:* Endogenous representation of transition functions and configurations within carrier lists.
  2. *Does not support:* Non-discrete state spaces or unconstrained real numbers.
  3. *Narrowest defensible claim:* Deterministic transitions on discrete integer lists decrement represented fuel step-for-step.
  4. *Next test needed:* Encoding of multi-tape and tree-structured memory cells into the carrier.

### CL-G018-02: Internalized Step-Simulation Correctness
- **Statement:** The internalized carrier simulator tracks the guest machine step by step with zero external host oracles or metatheoretic loop counters: $\text{Step}_{\text{carrier}}(\text{simEmbed}(S)) = \text{simEmbed}(\text{stepMachine}(S))$.
- **Formal Theorems:**
  - `G018SelfHosting.step_simulation_correctness`
  - `G018SelfHosting.step_simulation_extract_commutes`
  - `G018SelfHosting.sim_embed_extract_id`
- **Claim Hygiene:**
  1. *Supports:* Strict commutation between carrier-internal simulation steps and direct machine transitions.
  2. *Does not support:* Infinite acceleration or hypercomputation.
  3. *Narrowest defensible claim:* Under non-zero host and guest fuel, carrier-internal simulation tracks the direct step function identically.
  4. *Next test needed:* Measurement of constant-factor time and space overhead for higher-arity alphabets.

### CL-G018-03: Termination & Invariant Preservation
- **Statement:** When host fuel reaches zero or the simulated machine reaches a halted state, the carrier simulator preserves the state as a fixed point.
- **Formal Theorems:**
  - `G018SelfHosting.stepCarrier_zero_host_fuel`
  - `G018SelfHosting.stepCarrier_guest_halted`
  - `G018SelfHosting.stepCarrier_guest_zero_fuel`
  - `G018SelfHosting.runCarrier_halted`
- **Claim Hygiene:**
  1. *Supports:* Predictable halting behavior without uncontrolled runaway loops.
  2. *Does not support:* Asymptotic decidability of arbitrary loops.
  3. *Narrowest defensible claim:* Simulator stepping is an identity on halted or fuel-exhausted configurations.
  4. *Next test needed:* Recovery of intermediate execution checkpoints from halted states.

### CL-G018-04: Reflection Boundary Fuel Exhaustion
- **Statement:** Simulating an evaluator through a tower of depth $d$ requires fuel strictly growing with depth: $F(d, S) = S + d$ under unit overhead. If host fuel $B < S + d$, simulation terminates with fuel exhaustion before completion.
- **Formal Theorems:**
  - `G018SelfHosting.reflection_fuel_closed_form`
  - `G018SelfHosting.reflection_fuel_monotone`
  - `G018SelfHosting.reflection_capacity_limit`
  - `G018SelfHosting.reflection_boundary_exhaustion`
- **Claim Hygiene:**
  1. *Supports:* An explicit mathematical formula bounding reflection depth by available host fuel.
  2. *Does not support:* Claims about human consciousness or general AI reflection architectures.
  3. *Narrowest defensible claim:* Finite fuel budgets impose a strict upper bound on self-evaluative depth.
  4. *Next test needed:* Empirical measurement of compounding fuel requirements under non-unit compilation overhead.

### CL-G018-05: State Capacity Limit (Pigeonhole)
- **Statement:** A carrier with state capacity $k$ cannot represent guest machines with state count $m > k$ without state collisions (pigeonhole principle).
- **Formal Theorems:**
  - `G018SelfHosting.carrier_state_pigeonhole_step`
  - `G018SelfHosting.hasMatchNat_true`
  - `G018SelfHosting.hasMatchNat_false`
- **Claim Hygiene:**
  1. *Supports:* Constructive derivation of state collision witnesses when guest capacity exceeds host capacity.
  2. *Does not support:* Continuous state spaces without discretization.
  3. *Narrowest defensible claim:* Any discrete state mapping from $k+1$ states into $k$ slots contains an identical pair.
  4. *Next test needed:* Extension to information capacity bounds over compressed carrier tapes.

### CL-G018-06: Conditional Boolean Diagonal Lemmas and Finite Probes
- **Statement:** An arbitrary Boolean table has no row equal to the negation of its own diagonal. Separate Python probes exhibit errors for the listed heuristic predictors on the same encoded machine that is executed.
- **Formal Theorems:**
  - `G018SelfHosting.bool_neq_not_self`
  - `G018SelfHosting.diagonal_self_evaluation_obstruction`
  - `G018SelfHosting.halting_self_oracle_obstruction`
  - `G018SelfHosting.total_transition_oracle_refutation`
- **Claim Hygiene:**
  1. *Supports:* Conditional self-negation contradictions with 0 axioms and finite same-code counterexamples for seven named heuristics.
  2. *Does not support:* A general halting or total self-oracle impossibility theorem, or impossibility of a predictor correct on this bounded family.
  3. *Narrowest defensible claim:* If a Boolean row equals the negated diagonal, substitution at its own index gives a contradiction; the Python sweep separately detects concrete bounded prediction errors.
  4. *Next test needed:* A proved coding/evaluation fixed point that binds an oracle query to the exact program it predicts.

### CL-G018-07: Constructive Metatheoretic Boundary & Census
- **Statement:** All 71 declarations compiled in namespace `G018SelfHosting` depend strictly on allowed constructive axioms in `{"propext", "Quot.sound"}` with 0 private theorems and zero `Classical.choice`.
- **Audit Source:** `research/g018_self_hosting/lean/Inventory.lean`, `verify.py`, `evidence/receipt.json`.
- **Claim Hygiene:**
  1. *Supports:* Strict adherence to the repository's constructive integrity mandate.
  2. *Does not support:* Verification of uncompiled outside files.
  3. *Narrowest defensible claim:* The compiled Lean 4 package `g018_self_hosting` is free of classical axioms and mathlib imports.
  4. *Next test needed:* Inclusion into estate-wide verification gate suite.
