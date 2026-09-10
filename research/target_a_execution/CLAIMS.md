# Claims Ledger: Target A (Represented Execution Substrate)

AuthorityEffect: None.  
Configuration status: DECLARED_HOST_CONFIG.

This ledger records the formal and empirical claims established for Target A,
adhering strictly to the Claim Hygiene Rule. Every claim is scoped to finite
settings under fuel bounds without ungrounded universality claims.

---

## 1. Inventory of Claims

### CL-TA-01: Graph-Reading Edge Lookup
- **Statement:** The function `lookup` retrieves the destination datum of form `3 + k` from active datum `x` by consulting stored graph instances without calling unencoded operation functions.
- **Formal Status:** Lean theorem `Execution.lookup_mem` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_runner.py::test_lookup_success`.
- **What it supports:** Reading operation edges directly from represented graph data.
- **What it does not support:** Evaluation of dynamic functions outside the finite graph.
- **Narrowest defensible claim:** For any edge `(f, [x, y])` in the graph, lookup returns `y` when unique.
- **Next test needed:** Evaluation over expanding dynamic graph modifications.

---

### CL-TA-02: Word Machine Stepwise Composition
- **Statement:** The stepwise word machine execution on the empty word acts as the identity unit (`run_nil`), and multi-step execution agrees with the reference fold (`run_evalWord`).
- **Formal Status:** Lean theorems `Execution.run_nil` (`#print axioms: [propext]`) and `Execution.run_evalWord` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_runner.py::test_word_machine_agreement_with_eval_word`.
- **What it supports:** Equivalence between stepwise configuration stepping and fold evaluation over encoded instances.
- **What it does not support:** Infinite instruction execution without fuel limits.
- **Narrowest defensible claim:** On finite words and finite graphs, configuration stepping matches reference fold evaluation.
- **Next test needed:** Stepping over non-terminating word streams with explicit observation scales.

---

### CL-TA-03: Deterministic Step Characterization
- **Statement:** Stepping the deterministic runner to a next state requires firing exactly the unique enabled operation named by the reader.
- **Formal Status:** Lean theorem `Execution.stepDetOf_inr` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_runner.py::test_parameterized_runner_terminals`.
- **What it supports:** Soundness of deterministic state transitions with respect to unique enablement.
- **What it does not support:** Autonomous resolution of non-deterministic transitions.
- **Narrowest defensible claim:** When the runner advances state, exactly one operation was enabled and fired.
- **Next test needed:** Testing reader parameterization over composite state products.

---

### CL-TA-04: Non-Deterministic Fork Refusal
- **Statement:** When two or more operations are simultaneously enabled at the active state, the interpreter halts with terminal `Terminal.branch`, refusing to select an arbitrary branch.
- **Formal Status:** Lean theorem `Execution.stepDetOf_branch` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_control.py::test_step_det_fork_refusal`.
- **What it supports:** Prevention of implicit scheduling or arbitrary choice at non-deterministic forks.
- **What it does not support:** Probabilistic or heuristic branch selection.
- **Narrowest defensible claim:** The runner never breaks ties using list order; it returns `branch`.
- **Next test needed:** Parallel thread exploration across all branches of the successor family.

---

### CL-TA-05: Strict Resource Accounting
- **Statement:** Each successful operation firing increments the semantic clock by 1 and decrements represented fuel by 1; with zero fuel, no firing occurs.
- **Formal Status:** Lean theorems `Execution.fire_clock` (`#print axioms: [propext]`), `Execution.fire_fuel` (`#print axioms: [propext]`), and `Execution.fire_exhausted` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_control.py::test_fire_monotonicity`.
- **What it supports:** Monotonic resource consumption without unrecorded host fuel replenishment.
- **What it does not support:** Physical conservation laws or thermodynamic principles in continuous systems.
- **Narrowest defensible claim:** Fuel and clock strictly track the count of applied operations.
- **Next test needed:** Endogenous fuel generation driven by lawful work cycles.

---

### CL-TA-06: Tape Monotonicity and Prefix Property
- **Statement:** Successful operational execution strictly appends the visited datum to the tape, preserving prior tape content as a prefix.
- **Formal Status:** Lean theorems `Execution.fire_tape` (`#print axioms: [propext]`) and `Execution.nextOf_tape` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_control.py::test_step_det_deterministic_execution`.
- **What it supports:** Monotonic history recording and prefix compatibility across execution steps.
- **What it does not support:** Tape mutation, overwriting, or non-append tape operations.
- **Narrowest defensible claim:** The state tape at step $n$ is a prefix of the state tape at step $n+k$.
- **Next test needed:** Prefix limits under infinite compatible thread sequences (Target B).

---

### CL-TA-07: CFG Control Representation in Graph Data
- **Statement:** Control-flow graph structures (sequential steps, conditional branches, jump tables) are represented as graph instances and resolved solely through instance lookups.
- **Formal Status:** Lean theorem `Branch.jump_table_lookup` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_branching.py::test_cfg_jump_table`.
- **What it supports:** Data-driven control-flow routing without external dispatch machinery.
- **What it does not support:** Arbitrary higher-order function calls or closure allocation.
- **Narrowest defensible claim:** Jump table entries in graph instances resolve to their declared targets.
- **Next test needed:** Indirect jump table chaining across multiple execution frames.

---

### CL-TA-08: CFG Branch Non-Selection
- **Statement:** In a represented CFG, if multiple branch edges match the current condition at a program counter, the interpreter halts with `Terminal.branch`.
- **Formal Status:** Lean theorem `Branch.branch_non_selection` (`#print axioms: [propext]`) and `Branch.stepCFG_fork` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_branching.py::test_cfg_non_deterministic_fork_refusal`.
- **What it supports:** Consistency of branch refusal across structured CFG representations.
- **What it does not support:** Backtracking search over branch trees.
- **Narrowest defensible claim:** Ambiguous branch declarations in CFGs lead directly to the branch terminal.
- **Next test needed:** Conversion of multi-target branches into relational successor sets.

---

### CL-TA-09: Retained Internal Record Step Simulation
- **Statement:** Firing an operation in a synced state places the previous active datum into the penultimate position of the tape, making it accessible to depth-1 enablements.
- **Formal Status:** Lean theorem `Memory.previous_fire_synced` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_memory.py::test_previous_and_before_fallback`.
- **What it supports:** Endogenous route tracking without external route logs.
- **What it does not support:** Arbitrary random access into execution history.
- **Narrowest defensible claim:** The previous datum is computable from the tape and matches the prior active datum.
- **Next test needed:** Reading records across multi-locus interacting systems.

---

### CL-TA-10: Memory Ladder Monotonicity
- **Statement:** Any sequence that is functional in single entries is functional in pairs of entries.
- **Formal Status:** Lean theorem `Memory.functional2_of_functional1` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_memory.py::test_functionality_ceilings`.
- **What it supports:** The property that increasing the reading window length preserves functionality.
- **What it does not support:** That higher-depth reading always yields new distinct tapes.
- **Narrowest defensible claim:** Single-entry functionality implies pair functionality on finite tapes.
- **Next test needed:** General depth-$d$ ladder formalization.

---

### CL-TA-11: Depth-1 Refutation of Memoryless Ceiling
- **Statement:** The sequence `twistTape = [0, 1, 0, 0]` is functional in pairs but not functional in single entries, refuting memoryless determinism.
- **Formal Status:** Lean theorems `Memory.twist_not_functional1` (`#print axioms: [propext]`) and `Memory.twist_functional2` (`#print axioms: [propext, Quot.sound]`).
- **Empirical Status:** Unit tests in `tests/test_memory.py::test_depth1_record_reading_twist`.
- **What it supports:** That retaining one past record entry allows distinguishing merged paths.
- **What it does not support:** Distinguishing paths that share two past entries.
- **Narrowest defensible claim:** The twist tape cannot be generated by a memoryless deterministic program.
- **Next test needed:** Enumeration of all reachable tapes at carrier size 3.

---

### CL-TA-12: Depth-2 Refutation of Depth-1 Pair Ceiling
- **Statement:** The sequence `twist2Tape = [0, 1, 2, 0, 1, 0]` is not functional in pairs, refuting depth-1 pair determinism.
- **Formal Status:** Lean theorem `Memory.twist2_not_functional2` (`#print axioms: [propext]`).
- **Empirical Status:** Unit tests in `tests/test_memory.py::test_depth2_ternary_reading_twist2`.
- **What it supports:** That ternary control forms `[b, p, x]` allow breaking the pair functionality ceiling.
- **What it does not support:** Breaking triple functionality ceilings (depth 3).
- **Narrowest defensible claim:** The twist2 tape cannot be generated by a depth-1 deterministic record program.
- **Next test needed:** Formalization of general depth-3 functionality refutations.

---

## 2. Axiom Reliance Summary

| Module | Declaration Count | Axiom-Free | Permitted Axioms (`propext`, `Quot.sound`) | Classical Choice | mathlib |
|---|---|---|---|---|---|
| `Execution.lean` | 38 | 15 | 23 (`propext`: 22, `propext, Quot.sound`: 1) | 0 | 0 |
| `Branch.lean` | 12 | 2 | 10 (`propext`: 10) | 0 | 0 |
| `Memory.lean` | 8 | 0 | 8 (`propext`: 4, `propext, Quot.sound`: 4) | 0 | 0 |
| **Total** | **58** | **17** | **41** | **0** | **0** |
