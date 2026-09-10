# Claims Ledger: Target G015 / G017 (First-Demand, Invocation Bridge & Autonomous Stepping)

## 1. What it supports

1. **Event-Wise Demand Lifecycle**:
   Demonstrates that operational demands can be explicitly represented with lifecycle statuses (pending, active, discharged, reopened) within a discrete carrier state.
2. **First-Demand Deterministic Selection**:
   Shows in this model that pending demands can be ordered and selected deterministically by priority and canonical tie-breaking without external oracles.
3. **Autonomous Stepping without External Driver**:
   Demonstrates unprompted internal execution transitions driven solely by represented state until reaching quiescence.
4. **Prohibition of Spontaneous Demand**:
   Shows that an inert history under unchanged premises remains quiescent without creating unprovoked demands.
5. **Finite Saturation & Exact Accounting**:
   Demonstrates in this toy model that a demand chain with budget $B$ terminates in exactly $B$ steps, consuming exactly $B$ resource units in $\mathbb{Q}$.

## 2. What it does not support

1. Does not claim a solution to the general halting problem for arbitrary Turing machines.
2. Does not claim continuous-time physical dynamical systems; time is strictly discrete transition step count.
3. Does not claim unpriced or infinite perpetual computation.

## 3. The narrowest defensible claim

Under the declared discrete finite demand and carrier model, endogenous execution proceeds deterministically by first-demand selection until quiescence, conserving step and resource counts, and preserving state unmutated upon refusal or inert histories.

## 4. The next test needed

Progression to Target M104/M107: coherent equality layers and derived operational order families.
