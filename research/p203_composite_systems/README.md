# Target P203: Composite Systems & Pre-Spatial Locality

## Overview

This research package formalizes multi-locus composite carrier networks, relational interaction graphs derived from operation footprints, and pre-spatial locality under Target P203. It establishes constructive Lean 4 formalizations and verified Python simulation suites for:

1. **Multi-Locus Composite Networks & Associativity**: Multi-locus carrier networks equipped with associative tensor-like composition:
   $$(A \otimes B) \otimes C \cong A \otimes (B \otimes C)$$
   along with preservation of subsystem coordinate projections.
2. **Pre-Spatial Interaction Graphs**: Relational topologies derived directly from represented read/write footprints without background geometric metrics. Distance between loci is defined relationally as shortest path edge step count in the interaction graph.
3. **Strict Operational Non-Signaling Across Bipartite Cuts**: For an arbitrary bipartite cut $L = L_A \sqcup L_B$, any local intervention $T_A$ with footprint strictly contained in $L_A$ yields exact Total Variation Distance $TVD = 0.0$ on all observables in $L_B$ prior to mediating coupling transitions.
4. **Negative Controls**:
   - When an intervention footprint leaks across the cut to modify a locus in $L_B$, the marginal readout distribution shifts, yielding $TVD > 0$.
   - When a mediating relay transition coupling $L_A$ to $L_B$ executes after an intervention, the perturbation is transmitted, yielding $TVD > 0$.
5. **Duplicate Embedded Observers & Automorphism Invariance**: Duplicate observers embedded at automorphism-related loci obtain identical measurement marks on symmetric preparations. Physical connectivity and relational distance metrics remain invariant under graph automorphisms without reference to external coordinate frames.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly contained within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## Architecture

### 1. Multi-Locus Substrates and Associative Composition

A carrier network state maps each discrete locus identifier to a discrete value:
- Subsystem composition $A \otimes B$ merges disjoint locus valuations.
- The canonical associator isomorphism $\alpha_{A,B,C} : (A \otimes B) \otimes C \cong A \otimes (B \otimes C)$ maps left-bracketed groupings to right-bracketed groupings while preserving subsystem projections:
  $$\pi_A(\alpha(s)) = \pi_A(s), \quad \pi_B(\alpha(s)) = \pi_B(s), \quad \pi_C(\alpha(s)) = \pi_C(s)$$

### 2. Relational Footprints & Pre-Spatial Interaction Graphs

Every operational transition $T$ carries an explicit footprint:
$$\text{fp}(T) = (\text{reads}(T), \text{writes}(T))$$
An undirected interaction edge $\{u, v\}$ is induced whenever an elementary transition couples $u$ and $v$ (e.g. $u \in \text{reads}$ and $v \in \text{writes}$). Relational distance $d_G(u, v)$ is the shortest path edge step count in $G$:
- When two subsystems are disconnected (no mediating transitions crossing the cut), $d_G(u, v) = \infty$ (unreachable).
- When a mediating transition is introduced, relational paths form dynamically from operational couplings.

### 3. Bipartite Network Cuts & Operational Non-Signaling

Given a cut $L = L_A \sqcup L_B$:
- An intervention $T_A$ is localized to $L_A$ when $\text{reads}(T_A) \cup \text{writes}(T_A) \subseteq L_A$.
- An observable $O_B$ is localized to $L_B$ when $\text{footprint}(O_B) \subseteq L_B$.
- For any ensemble of states, the empirical marginal distribution of $O_B$ satisfies:
  $$P(O_B = o \mid T_A) = P(O_B = o \mid \text{Identity})$$
  yielding exact rational Total Variation Distance $TVD = 0.0$.

### 4. Negative Controls

1. **Leaky Footprint**: An intervention declaring footprint in $L_A$ that perturbs coordinate $b_1 \in L_B$ shifts the marginal distribution of $O_B$, resulting in $TVD > 0$.
2. **Mediated Causal Propagation**: An intervention strictly in $L_A$ followed by a mediating transition reading $a_2 \in L_A$ and writing to $b_1 \in L_B$ transmits information across the cut, resulting in $TVD > 0$.

### 5. Duplicate Observers and Presentation Symmetries

Duplicate observers $Obs_u$ and $Obs_v$ executing identical readout probes at loci related by graph automorphism $\sigma$ ($v = \sigma(u)$) satisfy:
- On $\sigma$-symmetric preparations ($s[\sigma(l)] = s[l]$), coincidence rate is $100\%$ ($r_u = r_v$).
- On asymmetric preparations, readout records diverge under injective probes.
- Readout operations satisfy equivariance with respect to presentation automorphisms.

---

## Verification and Execution

Run the complete verification harness:
```bash
python verify.py
```
This executes:
1. Source hygiene check: verifies zero occurrences of `sorry`, `admit`, `unsafe`, `partial`, or unverified axioms in Lean source files.
2. Pytest suite: executes all unit and property tests in `tests/test_composite_systems.py`.
3. Lake build: compiles `CompositeSystems.lean` and `Inventory.lean`.
4. Metatheoretic Census: verifies all 59 compiled theorems and confirms axioms are within `{propext, Quot.sound}`.
5. Emits `evidence/receipt.json`.
