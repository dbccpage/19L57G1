# Claims Ledger: Composite Systems & Pre-Spatial Locality (Target P203)

This ledger documents the formal mathematical and empirical claims established by `research/p203_composite_systems/` under constructive core Lean 4 and verified Python implementations.

AuthorityEffect: None.
Axiom Scope: Strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## CL-P203-01: Multi-Locus Substrate and Associative Tensor Composition

- **Statement**: Multi-locus carrier networks admit associative tensor-like composition:
  $$(A \otimes B) \otimes C \cong A \otimes (B \otimes C)$$
  via a canonical constructive associator isomorphism that preserves coordinate projections on each component subsystem.
- **Formal Theorems**:
  - `P203CompositeSystems.tensor_assoc`
  - `P203CompositeSystems.tensor_assoc_left_inv`
  - `P203CompositeSystems.tensor_assoc_right_inv`
  - `P203CompositeSystems.assoc_preserves_projA`
  - `P203CompositeSystems.assoc_preserves_projB`
  - `P203CompositeSystems.assoc_preserves_projC`
  - `P203CompositeSystems.assoc_inv_preserves_projA`
  - `P203CompositeSystems.assoc_inv_preserves_projB`
  - `P203CompositeSystems.assoc_inv_preserves_projC`
  - `P203CompositeSystems.toLeft_fromLeft`
  - `P203CompositeSystems.fromLeft_toLeft`
  - `P203CompositeSystems.toRight_fromRight`
  - `P203CompositeSystems.fromRight_toRight`
  - `P203CompositeSystems.assoc_carrier_commute`
  - `P203CompositeSystems.assoc_carrier_inv_commute`
- **Axiom Status**: Axiom-free.
- **Evidence Paths**:
  - `research/p203_composite_systems/lean/CompositeSystems.lean`
  - `research/p203_composite_systems/composite_systems.py`
  - `research/p203_composite_systems/tests/test_composite_systems.py`

---

## CL-P203-02: Pre-Spatial Interaction Graphs Derived from Footprints

- **Statement**: Interaction topologies and relational distance metrics between discrete loci are derived directly from elementary operation read/write footprints. Prior to introducing mediating coupling transitions across a cut, subsystems remain relationally disconnected, and shortest-path distance is infinite (unreachable).
- **Formal Theorems**:
  - `P203CompositeSystems.disconnected_cut_no_bridge`
  - `P203CompositeSystems.connected_cut_with_bridge`
- **Axiom Status**: Axiom-free.
- **Evidence Paths**:
  - `research/p203_composite_systems/lean/CompositeSystems.lean`
  - `research/p203_composite_systems/composite_systems.py`
  - `research/p203_composite_systems/tests/test_composite_systems.py`

---

## CL-P203-03: Strict Operational Non-Signaling Across Bipartite Cuts

- **Statement**: Across any bipartite cut $L = L_A \sqcup L_B$, interventions localized strictly to $L_A$ produce zero variation in the marginal readout distribution of observables in $L_B$ prior to mediating transitions:
  $$TVD(P(O_B \mid T_A), P(O_B \mid \text{Identity})) = 0.0$$
- **Formal Theorems**:
  - `P203CompositeSystems.non_signaling_bipartite`
  - `P203CompositeSystems.non_signaling_projB`
  - `P203CompositeSystems.non_signaling_a1_b1`
  - `P203CompositeSystems.non_signaling_a1_b2`
  - `P203CompositeSystems.non_signaling_a2_b1`
  - `P203CompositeSystems.non_signaling_a2_b2`
  - `P203CompositeSystems.non_signaling_sequenceA`
- **Axiom Status**: Axiom-free.
- **Evidence Paths**:
  - `research/p203_composite_systems/lean/CompositeSystems.lean`
  - `research/p203_composite_systems/composite_systems.py`
  - `research/p203_composite_systems/tests/test_composite_systems.py`

---

## CL-P203-04: Negative Controls (Leaky Footprints & Mediated Transmission)

- **Statement**: When an intervention leaks across a cut to modify $L_B$, or when a mediating coupling transition executes between intervention and readout, the marginal distribution of distant observables shifts, yielding $TVD > 0$.
- **Formal Theorems**:
  - `P203CompositeSystems.leaky_footprint_divergence`
  - `P203CompositeSystems.mediated_signaling_divergence`
- **Axiom Status**: Axiom-free.
- **Evidence Paths**:
  - `research/p203_composite_systems/lean/CompositeSystems.lean`
  - `research/p203_composite_systems/composite_systems.py`
  - `research/p203_composite_systems/tests/test_composite_systems.py`

---

## CL-P203-05: Duplicate Observer Agreement and Presentation Symmetries

- **Statement**: Duplicate embedded observers running identical local readout probes at automorphism-related loci record matching marks on symmetric preparations. Physical connectivity and relational distance metrics remain invariant under graph automorphisms without reference to external spatial embeddings.
- **Formal Theorems**:
  - `P203CompositeSystems.swap_involutive`
  - `P203CompositeSystems.swap_symmetric_eq`
  - `P203CompositeSystems.duplicate_observer_agreement`
  - `P203CompositeSystems.readout_swap_equivariance_B1`
  - `P203CompositeSystems.readout_swap_equivariance_A1`
  - `P203CompositeSystems.asymmetric_observer_divergence`
- **Axiom Status**: Axiom-free.
- **Evidence Paths**:
  - `research/p203_composite_systems/lean/CompositeSystems.lean`
  - `research/p203_composite_systems/composite_systems.py`
  - `research/p203_composite_systems/tests/test_composite_systems.py`

---

## Artifact Assessment

1. **What it supports**:
   - Supports constructive associative tensor composition for discrete multi-locus carrier networks.
   - Supports deriving pre-spatial interaction topologies from operational read/write footprints.
   - Supports exact zero marginal variation ($TVD = 0.0$) across arbitrary bipartite cuts prior to mediating coupling steps.
   - Supports duplicate observer agreement on symmetric states and symmetry invariance under graph automorphisms.
   - Supports detection of leaky footprints and mediated signaling via non-zero total variation distance.
2. **What it does not support**:
   - Does not support continuum spatial manifolds, differential geometry, or infinite-dimensional state carrier spaces.
   - Does not support superluminal signaling across mediating channels.
   - Does not support physical claims outside the declared finite discrete carrier substrate.
3. **Narrowest Defensible Claim**:
   In a finite discrete multi-locus carrier network where operations have explicit read/write footprints, disjoint subsystem footprints guarantee under the declared assumptions that local interventions on one partition produce exact total variation distance 0.0 on observables in a disjoint partition prior to mediating coupling transitions, while duplicate observers at automorphism-related loci show 100% agreement on symmetric preparations.
4. **Next Test Needed**:
   Investigate dynamic interaction graph re-wiring under adaptive feedback protocols and asynchronous distributed carrier transitions.
