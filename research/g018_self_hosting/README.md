# G018 Self-Hosting, Internal Simulation & Reflection Boundary

## 1. Overview

Target G018 formalizes an internalized finite simulator, step correctness,
reflection fuel bounds, and conditional Boolean diagonal lemmas for deterministic transition systems
represented within the object carrier.

The investigation addresses whether an execution engine's own operational stepping rule
can be faithfully tracked inside the carrier state space without external host oracles
or metatheoretic loop counters, and establishes the finite capacity limits bounding self-evaluation.

## 2. Core Components

### 2.1 Carrier Representation (`carrier_repr.py`, `CarrierRepr.lean`)
The execution engine represents transition functions as structured data (states, transitions,
cursor, tape, fuel). The machine state tracks operational coordinates:
- `state : Nat` (active state index)
- `cursor : Nat` (active tape head position)
- `tape : List Nat` (sequence of discrete symbols)
- `fuel : Nat` (remaining operational step resource)
- `halted : Bool` (termination flag)

Transitions are deterministic edges mapping `(curr_state, read_sym)` to `(next_state, write_sym, move_cursor, halt)`.
Flat carrier serialization tags each component with unique identifiers, enabling bidirectional serialization.

### 2.2 Internalized Simulator (`simulator.py`, `Simulator.lean`)
The simulator executes inside the carrier representation. It inspects the embedded guest configuration,
reads the tape symbol under the guest cursor, performs rule lookup within the embedded transition table,
and updates the guest configuration while decrementing host fuel.

Single-step simulation correctness is established:
$$\text{Step}_{\text{carrier}}(\text{simEmbed}(\text{spec}, s, \text{fuel})) = \text{simEmbed}(\text{spec}, \text{stepMachine}(\text{spec}, s), \text{fuel} - 1)$$

Micro-step internal simulation demonstrates step-equivalence at $k = 4$ micro-cycles per guest step:
$$\text{Step}_{\text{micro}}^4(\text{Sim}(S)) = \text{Sim}(\text{step}(S))$$

### 2.3 Reflection Boundary (`reflection_boundary.py`, `ReflectionBoundary.lean`)
The reflection boundary formalizes capacity limits on self-evaluation:
- **Fuel Compounding**: Executing a guest run of $S$ steps through a tower of $d$ evaluators requires
  $F(d, S) = S + d$ fuel under unit step overhead.
- **Fuel Exhaustion**: When host fuel $B < F(d, S)$, execution terminates at $B$ with incomplete simulation (`fuel_exhausted = True`).
- **State Capacity Limit**: By the constructive pigeonhole principle, any host carrier with state capacity $k$
  attempting to evaluate a guest with state space $m > k$ incurs state aliasing ($\exists s_1 \neq s_2, f(s_1) = f(s_2)$).

### 2.4 Conditional Diagonal Lemmas and Finite Predictor Probes (`diagonal_obstruction.py`, `Obstruction.lean`)
Lean proves that no row of a Boolean table equals the pointwise negation of
its own diagonal entry, and that explicitly assumed self-negating equations
are contradictory. It does not construct an evaluator, self-code fixed point,
or a general halting theorem. Python searches a declared finite family of
machines for errors by named heuristic predictors. Each reported prediction
and observed behavior now refer to the same machine and encoded input; an
exact predictor on that finite family has no reported counterexample.

## 3. Claim Hygiene Summary

### 1. What it supports
- Shows in this formal model that an internalized simulator faithfully reproduces the step-by-step state trajectory of a deterministic transition machine using carrier-represented data alone.
- Demonstrates in this finite setting that simulation depth is bounded by host fuel budgets according to $F(d, S) = S + d$.
- Gives same-code finite counterexamples for the listed heuristic predictors and conditional Boolean self-negation lemmas.

### 2. What it does not support
- Does not demonstrate computability across arbitrary infinite transition systems or general continuum dynamics.
- Does not claim that real-world hardware or LLMs possess or lack self-modeling capacity.
- Does not establish unstratified reflective self-modification without fuel decrement.
- Does not prove a general self-oracle or halting impossibility theorem; that would require a representation/evaluation fixed-point bridge.

### 3. The narrowest defensible claim
For the defined finite machines, internal simulation tracks operational steps under the stated fuel conditions. The Boolean contradiction theorems and bounded same-code predictor counterexamples are separate results.

### 4. The next test needed
For a general diagonal theorem, construct a coding/evaluation fixed point and prove that the encoded program's behavior is the one queried by the predictor. Keep multi-head and branching extensions separate from that proof obligation.
