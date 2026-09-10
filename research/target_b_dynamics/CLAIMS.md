# Scoped Claims Ledger: Target B (Coherent Observation Scales & Dynamics)

AuthorityEffect: None.
Strict adherence to the Claim Hygiene Rule: all claims are narrowly scoped, constructive, and free of hype verbs.

---

## Artifact Summaries (Claim Hygiene Discipline)

### 1. The Abstract Inverse System (`limits.py`, `Limits.lean`)
1. **What it supports**: Supports that finite prefix stages under truncation bonding form a constructive inverse system whose thread space admits a constructive bijection with sequence space $\mathbb{N} \to \text{Fin } c$ without non-constructive axioms (`Classical.choice`); demonstrates that restriction to even scales preserves the sequence space; demonstrates that shifting a prefix requires unobserved future data (`shift_not_local`).
2. **What it does not support**: Does not support that the thread space forms a connected topological manifold, real interval, or continuum; does not support character duality on continuous topological groups; does not claim category-theoretic universality over arbitrary cones.
3. **Narrowest defensible claim**: For finite words over finite carriers, prefix truncation bonding yields a thread space constructively bijective with sequences; dyadic sequences $0111\dots$ and $1000\dots$ are separated at scale 1 and remain distinct threads.
4. **Next test needed**: Construction of an explicit uniform structure or metric topology on thread spaces.

### 2. Step-Scale Observations (`observe.py`, `Observe.lean`)
1. **What it supports**: Supports that deterministic stepping of represented programs monotonically appends to the execution tape, inducing prefix compatibility across all finite step scales ($\text{obs}(n, s) \sqsubseteq \text{obs}(n + k, s)$); supports that observations at scale $n$ are invariant across all fuel amounts $\ge n$.
2. **What it does not support**: Does not support infinite non-terminating execution without finite fuel exhaustion; does not claim that bare tapes determine future transitions without fuel information (`lost_fuel`).
3. **Narrowest defensible claim**: For any configuration running under the deterministic runner with fuel $\ge n$, the tape after $n$ steps is a prefix of subsequent step tapes and is invariant under additional declared fuel.
4. **Next test needed**: Endogenous fuel replenishment and self-bounding resource accounting.

### 3. Commuting Dynamics Square (`commute.py`, `Commute.lean`)
1. **What it supports**: Supports that pointwise program transitions $F : \text{Fin } c \to \text{Fin } c$ commute with finite stage bonding ($\text{bond}_n \circ \text{step}_{n+1} = \text{step}_n \circ \text{bond}_n$), lifting to a continuous endomorphism on compatible threads; supports that observation trace stepping commutes with prefix projection.
2. **What it does not support**: Does not support that bare tape projections commute with state stepping under fuel exhaustion; does not support commuting dynamics for non-deterministic forks without explicit branch-lifting adapters.
3. **Narrowest defensible claim**: Pointwise evaluation maps commute with truncation bonding on stages and threads; observation trace projection commutes with deterministic stepping under sufficient fuel.
4. **Next test needed**: Verification of commuting dynamics on concurrent two-locus product carriers.

### 4. Quantitative Rational Limiting Bounds & Non-Density (`bounds.py`, `RationalBounds.lean`)
1. **What it supports**: Supports that realized deterministic execution tapes satisfy chain functionality; demonstrates that `[0, 1, 0, 2]` violates functionality and cannot be realized by any deterministic program, establishing that realized tapes are not dense in the thread space; supports that the 3-state cycle program satisfies $L \le 3 \cdot \text{zeros}(L) \le L + 2$, with rational error bounded by $2 / (3L)$ in $\mathbb{Q}$.
2. **What it does not support**: Does not support convergence in real analysis ($\mathbb{R}$) or Dedekind completeness; does not support identifying the discrete 3-cycle with the continuous circle $S^1$.
3. **Narrowest defensible claim**: The tape `[0, 1, 0, 2]` is not a chain for any single-valued transition function; on the declared 3-cycle program, the count of datum 0 obeys $L \le 3 \cdot \text{zeros}(L) \le L + 2$ in Peano arithmetic at all scales allowed by fuel.
4. **Next test needed**: Evaluation of limiting rational frequency readouts on non-periodic or multi-cycle configurations.

---

## Detailed Scoped Claims

### CL-TB-01 — Thread Space Bijective with Sequences
- **Statement**: There exists a constructive bijection between compatible threads of finite stages and sequences $\mathbb{N} \to \text{Fin } c$ (`toSeq_ofSeq`, `ofSeq_toSeq`).
- **Scope**: Discrete finite prefix inverse systems.
- **Axioms**: `Quot.sound` (from Subtype extensionality), zero `Classical.choice`, zero `mathlib`.
- **Refusal**: Lax eventual compatibility is refused (`eventual_not_compatible`).

### CL-TB-02 — Prefix Compatibility of Process Observations
- **Statement**: For every state $s$ and scales $n, k$, $\text{obs}(n, s) \sqsubseteq \text{obs}(n + k, s)$.
- **Scope**: Deterministic graph interpreter with monotonic tape appending.
- **Axioms**: `propext`.

### CL-TB-03 — Fuel Independence of Step Observations
- **Statement**: Two states with identical graph, active datum, and tape produce identical observations at scale $n$ for all fuel allocations $\ge n$.
- **Scope**: Fuel-guarded deterministic runner.
- **Axioms**: `propext`, `Quot.sound`.

### CL-TB-04 — Commuting Dynamics Square on Stages
- **Statement**: $\text{bond}_n(\text{step}_{n+1}(w)) = \text{step}_n(\text{bond}_n(w))$ for pointwise transitions.
- **Scope**: Finite stages over alphabet $\text{Fin } c$.
- **Axioms**: None (axiom-free definition equality `rfl`).

### CL-TB-05 — Continuous Endomorphism Lifting on Threads
- **Statement**: The pointwise transition lifts to an endomorphism on compatible threads commuting with sequence projection.
- **Scope**: Thread space $\text{Thread}(c)$.
- **Axioms**: None (`rfl`).

### CL-TB-06 — Topological Non-Density via Chain Functionality
- **Statement**: Deterministic execution tapes are single-valued chains; the sequence `[0, 1, 0, 2]` cannot be realized as a chain, exhibiting an open cylinder with zero realized runs.
- **Scope**: Finite graphs and discrete deterministic execution.
- **Axioms**: `propext`, `Quot.sound`.

### CL-TB-07 — Quantitative Rational Limiting Frequency Bound
- **Statement**: On the 3-state cycle program, the count of datum 0 obeys $L \le 3 \cdot \text{zeros}(L) \le L + 2$, with rational precision budget $\epsilon \le 2 / (3L)$ in $\mathbb{Q}$.
- **Scope**: Finitary arithmetic on natural and rational numbers.
- **Axioms**: `propext`, `Quot.sound`.

### CL-TB-08 — Refusal of Unconstructed Continua and Circles
- **Statement**: Discrete thread spaces are totally disconnected; quotienting dyadic twins or identifying the 3-cycle with continuous circle $S^1$ is explicitly refused without construction.
- **Scope**: Foundational ontology and topology boundaries.
- **Axioms**: None.
