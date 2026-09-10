# Claims Ledger: Operational Protocols & Embedded Observers (Target P200)

This ledger enumerates formal mathematical and operational claims established
by `research/p200_operational_protocols/` under constructive core Lean 4 and verified Python mirrors.

AuthorityEffect: None.
Axiom Scope: Strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## CL-P200-01: Multi-Locus Operational Carrier and Protocol Stages

- **Statement**: A multi-locus carrier $L_1 \times L_2 \times M \times R_1 \times R_2 \times DIST$ embeds the operational protocol lifecycle: preparations (product and symmetric configurations), localized interventions, persistent records in observer memory, coincidence comparisons, and embedded measurement instruments.
- **Formal Theorems**:
  - `P200OperationalProtocols.prepare_product_l1`
  - `P200OperationalProtocols.prepare_product_l2`
  - `P200OperationalProtocols.prepare_product_records`
  - `P200OperationalProtocols.prepare_symmetric_eq`
  - `P200OperationalProtocols.intervene_l1_preserves_l2`
  - `P200OperationalProtocols.intervene_l1_preserves_m`
  - `P200OperationalProtocols.intervene_l1_preserves_r2`
  - `P200OperationalProtocols.intervene_l2_preserves_l1`
  - `P200OperationalProtocols.intervene_l2_preserves_m`
  - `P200OperationalProtocols.intervene_l2_preserves_r1`
  - `P200OperationalProtocols.record1_preserves_target`
  - `P200OperationalProtocols.record2_preserves_target`
  - `P200OperationalProtocols.coincidence_iff`
- **Axiom Status**: Axiom-free / `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p200_operational_protocols/lean/Protocol.lean`
  - `research/p200_operational_protocols/protocol.py`
  - `research/p200_operational_protocols/tests/test_protocol.py`

---

## CL-P200-02: Non-Disturbing Readout Commutation and Disturbance Detection

- **Statement**: On non-disturbing sectors characterized by mutually disjoint access footprints, embedded observer readouts commute with autonomous process step transitions ($\text{Readout} \circ \text{Step} = \text{Step} \circ \text{Readout}$). When an instrument perturbs its target locus, operational commutation fails on unpriced carrier coordinates, and disturbance is recorded in diagnostic registers.
- **Formal Theorems**:
  - `P200OperationalProtocols.readout_step_commutation`
  - `P200OperationalProtocols.readout1_stepL2_commutation`
  - `P200OperationalProtocols.readout1_stepM_commutation`
  - `P200OperationalProtocols.readout2_stepM_commutation`
  - `P200OperationalProtocols.disturbing_readout_fails_commute`
- **Axiom Status**: Axiom-free.
- **Evidence Paths**:
  - `research/p200_operational_protocols/lean/Commutation.lean`
  - `research/p200_operational_protocols/commutation.py`
  - `research/p200_operational_protocols/tests/test_commutation.py`

---

## CL-P200-03: Presentation Symmetries, Equivariance, and Inter-Observer Agreement

- **Statement**: Duplicate observers embedded at distinct carrier loci related by presentation symmetries (locus swap involution and coordinate translations) satisfy operational equivariance. On symmetric preparations where $s.l_1 = s.l_2$, both observers record matching memory marks ($r_1 = r_2$). When preparations are asymmetric, recorded marks diverge under injective probes.
- **Formal Theorems**:
  - `P200OperationalProtocols.swap_involutive`
  - `P200OperationalProtocols.swap_preserves_m`
  - `P200OperationalProtocols.swap_preserves_dist`
  - `P200OperationalProtocols.readout2_swap`
  - `P200OperationalProtocols.readout1_swap`
  - `P200OperationalProtocols.swap_symmetric_eq`
  - `P200OperationalProtocols.inter_observer_agreement`
  - `P200OperationalProtocols.inter_observer_coincidence`
  - `P200OperationalProtocols.asymmetric_observation_divergence`
- **Axiom Status**: Axiom-free / `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p200_operational_protocols/lean/Observers.lean`
  - `research/p200_operational_protocols/embedded_observer.py`
  - `research/p200_operational_protocols/tests/test_duplicate_observers.py`

---

## CL-P200-04: Spacelike Non-Signaling and Marginal Readout Invariance

- **Statement**: Because local interventions at Locus 1 and embedded readouts at Locus 2 possess disjoint access footprints, Observer 2's readout record is invariant under arbitrary interventions at Locus 1 prior to relational step propagation. Over any state distribution, the marginal distribution shift is zero (total variation distance is 0.0). Signaling occurs strictly after relational step propagation through mediating channel $M$.
- **Formal Theorems**:
  - `P200OperationalProtocols.spacelike_non_signaling`
  - `P200OperationalProtocols.spacelike_marginal_invariance`
  - `P200OperationalProtocols.spacelike_marginal2_invariance`
  - `P200OperationalProtocols.spacelike_sequence_non_signaling`
  - `P200OperationalProtocols.causal_signaling_divergence`
- **Axiom Status**: Axiom-free.
- **Evidence Paths**:
  - `research/p200_operational_protocols/lean/NonSignaling.lean`
  - `research/p200_operational_protocols/non_signaling.py`
  - `research/p200_operational_protocols/tests/test_non_signaling.py`

---

## Artifact Assessment

1. **What it supports**:
   - Supports operational protocol formulation embedded within a finite discrete carrier.
   - Supports commutation between non-disturbing readouts and localized process steps.
   - Supports duplicate observer agreement on symmetric preparations under presentation symmetries.
   - Supports zero marginal shift under spacelike separation prior to relational step propagation.
2. **What it does not support**:
   - Does not support continuous geometric metrics, non-constructive continuum field theories, or infinite function spaces.
   - Does not support superluminal signaling across mediating channels.
   - Does not support claim scope outside the declared discrete multi-locus substrate.
3. **Narrowest Defensible Claim**:
   In a discrete multi-locus carrier with disjoint access footprints, non-disturbing embedded readouts commute with localized step transitions, duplicate observers show equivariance and agreement on symmetric preparations, and local interventions at one locus produce zero marginal readout shift at a disjoint locus prior to relational step propagation.
4. **Next Test Needed**:
   Model multi-observer network topologies with stochastic transition kernels and asymmetric coupling delays.
