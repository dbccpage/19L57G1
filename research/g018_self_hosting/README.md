# G018 Self-Hosting, Internal Simulation & Reflection Boundary

## 1. Overview

Target G018 formalizes the internalized self-simulation engine, step correctness,
reflection boundary, and diagonal obstruction for deterministic transition systems
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

### 2.4 Diagonal Obstruction (`diagonal_obstruction.py`, `Obstruction.lean`)
Proves that no finite carrier contains a total halting or transition self-oracle.
For every candidate total predictor $P(M, x) \to \text{Bool}$, the diagonal construction synthesizes
a machine $D_P$ that executes the opposite of $P$'s prediction on its own code:
- $P(D_P, \text{code}(D_P)) = \text{True} \implies D_P \text{ loops}$
- $P(D_P, \text{code}(D_P)) = \text{False} \implies D_P \text{ halts}$

The Lean 4 formalization derives the obstruction constructively with zero external axioms:
$$\neg \exists (P : \text{Nat} \to \text{Nat} \to \text{Bool}), \exists d, \forall x, P(d, x) = \neg P(x, x)$$

## 3. Claim Hygiene Summary

### 1. What it supports
- Shows in this formal model that an internalized simulator faithfully reproduces the step-by-step state trajectory of a deterministic transition machine using carrier-represented data alone.
- Demonstrates in this finite setting that simulation depth is bounded by host fuel budgets according to $F(d, S) = S + d$.
- Shows constructively that total halting self-prediction is obstructed for any candidate predictor within the carrier.

### 2. What it does not support
- Does not demonstrate universal computability across arbitrary infinite Turing machines or general continuum dynamics.
- Does not claim that real-world hardware or LLMs possess or lack self-modeling capacity.
- Does not establish unstratified reflective self-modification without fuel decrement.

### 3. The narrowest defensible claim
For the class of deterministic transition machines with finite state alphabets and discrete tapes, internal simulation tracks operational stepping step-for-step under finite fuel decrement, and total self-oracle evaluation is obstructed by diagonal inversion with zero classical axioms.

### 4. The next test needed
Scale the carrier representation to multi-head and branching non-deterministic transition graphs, verifying whether the reflection boundary maintains strict linear or polynomial overhead under parallel evaluation branches.
