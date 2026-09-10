# P200: Operational Protocols & Embedded Observers

## Overview

This research package formalizes operational protocols and embedded observers within the process carrier substrate under Requirement R4 (Target P200). It establishes constructive Lean 4 formalizations and verified Python simulation suites for:
1. Operational protocols: preparations (initializing state regions), interventions (local perturbations), records (persistent memory marks), comparisons (coincidence evaluators), and measurement instruments embedded within the carrier.
2. Readout-to-step commutation: on non-disturbing sectors with mutually disjoint carrier footprints, embedded readout commutes with autonomous process state transitions: $\text{Readout} \circ \text{Step} = \text{Step} \circ \text{Readout}$.
3. Disturbance detection and explicit pricing: when an embedded instrument modifies the target locus, operational commutation fails in general on unpriced state coordinates, and the disturbance is explicitly recorded in diagnostic registers.
4. Duplicate embedded observers: observers located at distinct carrier loci related by presentation symmetries (locus swap involution and coordinate translation) show recorded inter-observer agreement on symmetric preparations.
5. Spacelike non-signaling: local interventions at Locus 1 do not perturb the marginal readout distribution at Locus 2 prior to relational step propagation through mediating channels.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly contained in `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## Architecture

### 1. Multi-Locus Process Carrier

The substrate consists of six discrete coordinates:
- $L_1$: Target physical subsystem 1
- $L_2$: Target physical subsystem 2
- $M$: Shared coupling channel / mediating register
- $R_1$: Embedded memory record register for Observer 1
- $R_2$: Embedded memory record register for Observer 2
- $DIST$: Disturbance diagnostic register

### 2. Operational Protocol Stages

1. **Preparations**: Initializing carrier state regions (independent product states, symmetric correlated states).
2. **Interventions**: Local perturbations strictly localized to specified loci ($L_1$, $L_2$, or $M$).
3. **Records**: Persistent marks stored in dedicated registers ($R_1$, $R_2$).
4. **Comparisons**: Coincidence evaluators assessing matching marks across observers ($R_1 = R_2$).
5. **Measurement Instruments**: Embedded apparatus reading target loci into record registers, classified into non-disturbing readouts and priced disturbing readouts.

### 3. Readout Commutation and Disturbance Pricing

For operations $A$ and $B$, commutation holds when their access footprints satisfy the Bernstein conditions:
- $\text{writes}(A) \cap \text{writes}(B) = \emptyset$
- $\text{reads}(A) \cap \text{writes}(B) = \emptyset$
- $\text{writes}(A) \cap \text{reads}(B) = \emptyset$

On non-disturbing sectors (e.g. Readout at $L_2$ into $R_2$, and Step at $L_1$ or $M$), commutation is established:
$$\text{Readout}_2 \circ \text{Step}_1 = \text{Step}_1 \circ \text{Readout}_2$$

When an instrument modifies its target locus, operational commutation fails on unpriced carrier coordinates, and the disturbance cost is recorded.

### 4. Duplicate Embedded Observers and Symmetry Relations

Duplicate observers are related by the locus swap involution:
$$\sigma(l_1, l_2, m, r_1, r_2, dist) = (l_2, l_1, m, r_2, r_1, dist)$$
Readout operations satisfy equivariance:
$$\text{Readout}_2(\sigma(s)) = \sigma(\text{Readout}_1(s))$$
On symmetric preparations where $s.l_1 = s.l_2$, executing identical local readout protocols yields matching recorded marks:
$$r_1 = r_2$$

### 5. Spacelike Non-Signaling

Because local interventions at $L_1$ and embedded readouts at $L_2$ have mutually disjoint footprints:
$$\{L_1\} \cap \{L_2, R_2\} = \emptyset$$
the marginal distribution of Observer 2's readout record is invariant under arbitrary interventions at $L_1$:
$$P(R_2 = r \mid I_1 = a) = P(R_2 = r \mid I_1 = b)$$
The total variation distance between marginal distributions across distinct interventions is zero. Causal signaling occurs only after relational step propagation through mediating channel $M$.

---

## Artifact Summary (Claim Hygiene Compliance)

1. **What it supports**:
   - Supports constructive readout-to-step commutation on disjoint carrier footprints.
   - Supports explicit disturbance detection and cost recording when instruments alter target coordinates.
   - Supports recorded inter-observer agreement for duplicate observers under presentation symmetry on symmetric preparations.
   - Supports spacelike non-signaling and zero marginal readout shift prior to relational step propagation.
2. **What it does not support**:
   - Does not support continuous geometric metrics, infinite function spaces, or non-constructive continuum limits.
   - Does not support signaling faster than discrete relational step propagation through mediating channels.
   - Does not support universality beyond the declared finite multi-locus carrier model.
3. **Narrowest Defensible Claim**:
   Within a constructive finite multi-locus carrier with disjoint access footprints, non-disturbing embedded readouts commute with localized step transitions, duplicate observers show equivariance and agreement on symmetric preparations, and local interventions at one locus produce zero marginal readout shift at a disjoint locus prior to relational step propagation.
4. **Next Test Needed**:
   Extend relational step propagation to network topologies with variable communication delays and multi-stage routing channels.

---

## Verification

Run the master verification suite:
```powershell
python verify.py --check
```
This executes:
1. Source hygiene check (prohibits `sorry`, `admit`, `unsafe`, `partial`, and naked `axiom`).
2. Python pytest suite (22 unit and property tests).
3. Lean 4 package build (`lake build`).
4. Metatheoretic theorem census and axiom audit (`Inventory.lean`) confirming 51 theorems within `{propext, Quot.sound}`.
