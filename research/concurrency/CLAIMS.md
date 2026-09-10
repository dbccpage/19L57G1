# Claims Ledger: Concurrency & Observers (Requirement R2 / W06, W07)

This ledger enumerates the formal mathematical and operational claims established
by `research/concurrency/` under constructive core Lean 4 and verified Python mirrors.

AuthorityEffect: None.
Axiom Scope: strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## CL-CC-01: Multi-Locus Product Carrier Bijective Representation

- **Statement**: A 3-locus carrier $L_1 \times L_2 \times M$ of finite capacities $(n_1, n_2, n_m)$ is canonically packed into $\mathbb{N}$ via $x = n_m \cdot (n_2 \cdot l_1 + l_2) + m$. Unpacking recovers the exact coordinates ($l_1, l_2, m$), and local coordinate updates preserve all uncoupled coordinates.
- **Formal Theorems**:
  - `Concurrency.unpack3_pack3`
  - `Concurrency.pack3_lt`
  - `Concurrency.updateL1_preserves_l2`, `Concurrency.updateL1_preserves_m`
  - `Concurrency.updateL2_preserves_l1`, `Concurrency.updateL2_preserves_m`
  - `Concurrency.updateM_preserves_l1`, `Concurrency.updateM_preserves_l2`
- **Axiom Status**: `{propext, Quot.sound}` / axiom-free.

---

## CL-CC-02: Derived Interaction Dependency Graph Without Spatial Metric

- **Statement**: An interaction dependency graph $G = (V, E)$ is derived strictly from operational read/write access footprints without assuming background Euclidean metrics, lattices, or geometric coordinates. Operations $S_i, S_j$ are connected by an edge iff their access footprints interfere under the Bernstein condition.
- **Formal Theorems**:
  - `Concurrency.locusInterferes_symm`
  - `Concurrency.interferes_symm`
  - `Concurrency.isDisjoint_symm`
  - `Concurrency.fpL1_fpL2_disjoint`
  - `Concurrency.fpL1_fpM_disjoint`
  - `Concurrency.fpL2_fpM_disjoint`
- **Axiom Status**: Axiom-free.

---

## CL-CC-03: Operational Independence Commuting Squares

- **Statement**: For any two operations $S_1, S_2$ respecting footprints $f_1, f_2$, if $f_1$ and $f_2$ are disjoint (independent), then the operations commute on all states: $(S_1 \circ S_2)(s) = (S_2 \circ S_1)(s)$.
- **Formal Theorems**:
  - `Concurrency.disjoint_commutes`
  - `Concurrency.updateL1_updateL2_commutes`
  - `Concurrency.updateL1_updateM_commutes`
  - `Concurrency.updateL2_updateM_commutes`
- **Axiom Status**: Axiom-free.

---

## CL-CC-04: Non-Commuting Failing Squares (Operational Interference)

- **Statement**: Operations sharing a mutable locus fail to commute in general. Concrete witnesses establish that write-write conflicts and read-write conflicts break operational commutation.
- **Formal Theorems**:
  - `Concurrency.write_write_conflict_fails_commute`
  - `Concurrency.read_write_conflict_fails_commute`
- **Axiom Status**: Axiom-free.

---

## CL-CC-05: Observer Symmetry and Observation Agreement (W06)

- **Statement**: Two observers receiving projected observations $\pi_1(s) = (s.l_1, s.m)$ and $\pi_2(s) = (s.l_2, s.m)$ obtain identical observations when the carrier state is symmetric under locus swap ($s.l_1 = s.l_2$). Identical local decision policies yield matching actions.
- **Formal Theorems**:
  - `Concurrency.swap_involutive`
  - `Concurrency.swap_symmetric_eq`
  - `Concurrency.symmetry_agreement`
  - `Concurrency.decision_agreement`
- **Axiom Status**: Axiom-free.

---

## CL-CC-06: Represented Message Transmission and Causal Decision Divergence (W06)

- **Statement**: When Observer 1 transmits its local coordinate into the shared buffer $M$, Observer 2 reading from $M$ diverges in its subsequent decision, even when Observer 2 begins in identical local states. Conversely, without transmission to $M$, Observer 1's local mutations leave Observer 2's subsequent state invariant.
- **Formal Theorems**:
  - `Concurrency.decision_divergence`
  - `Concurrency.uncoupled_preserves_receiver`
- **Axiom Status**: Axiom-free.
