# Concurrency & Observers: W06, W07 & Target B Operational Substrate

Package `research/concurrency/` implements Requirement R2 of Cohort 3:
- **W06 (Observer Record Exchange)**: Two observers with projected observations, symmetry agreement, represented message transmission, and causal decision divergence.
- **W07 (Interaction Dependency Graph & Commuting Squares)**: Operational independence squares ($S_1 \circ S_2 = S_2 \circ S_1$) for disjoint footprints, failing squares for interfering operations, and derived interaction graphs without background spatial metrics.

AuthorityEffect: None.

---

## Architecture & File Layout

```
research/concurrency/
├── CLAIMS.md                         # Formal claims ledger (CL-CC-01 through CL-CC-06)
├── README.md                         # Package overview and architectural documentation
├── pyproject.toml                    # Pytest configuration
├── verify.py                         # Verification harness (hygiene, pytest, lake build, census)
├── carrier.py                        # Multi-locus carrier (State3, packing, projections, updates)
├── footprint.py                      # Read/write footprints and derived DependencyGraph
├── commute.py                        # Commuting squares and failing witness finders
├── observer.py                       # W06 two-observer message exchange simulation
├── evidence/
│   └── receipt.json                  # Byte-pinned verification receipt
├── tests/
│   ├── test_carrier.py               # Tests for coordinates, packing, roundtrips
│   ├── test_footprint.py             # Tests for footprints and dependency graph
│   ├── test_commute_squares.py       # Sweeps over commuting and non-commuting squares
│   └── test_observer_exchange.py     # Tests for symmetry agreement & decision divergence
└── lean/
    ├── lakefile.toml                 # Lake build configuration
    ├── lean-toolchain                # Pinned toolchain (leanprover/lean4:v4.33.0)
    ├── Carrier.lean                  # Constructive multi-locus packing, projections, locality
    ├── Footprint.lean                # Access footprints and dependency graph derivation
    ├── CommuteSquare.lean            # Constructive independence square and failing witnesses
    ├── ObserverExchange.lean         # W06 observer projections, symmetry lemma, divergence
    └── Inventory.lean                # Axiom census auditing {propext, Quot.sound}
```

---

## Mathematical Formalization

### 1. Multi-Locus Carrier ($L_1 \times L_2 \times M$)
A state is an element $(l_1, l_2, m)$ where:
- $l_1 \in \{0, \dots, n_1-1\}$: Observer 1 local locus
- $l_2 \in \{0, \dots, n_2-1\}$: Observer 2 local locus
- $m \in \{0, \dots, n_m-1\}$: Shared communication/coupling cell

Packed into $\mathbb{N}$ via:
$$\text{pack3}(n_2, n_m, s) = n_m \cdot (n_2 \cdot l_1 + l_2) + m$$

### 2. Interaction Dependency Graph
Given operations with read footprints $R(S)$ and write footprints $W(S)$, conflict between $S_1$ and $S_2$ on locus $L$ is given by the Bernstein condition:
$$\text{conflict}_L(S_1, S_2) = (W_1 \cap (R_2 \cup W_2)) \cup (W_2 \cap (R_1 \cup W_1))$$
The dependency graph $G = (V, E)$ has edges strictly where footprints conflict. No background spatial metric or coordinate space is assumed.

### 3. Operational Independence Theorem
If two operations $S_1, S_2$ have disjoint footprints, then for all states $s$:
$$(S_1 \circ S_2)(s) = (S_2 \circ S_1)(s)$$
Proved constructively in `lean/CommuteSquare.lean` (`disjoint_commutes`) without external axioms.

### 4. W06 Observer Record Exchange
- **Projections**: $\pi_1(s) = (s.l_1, s.m)$, $\pi_2(s) = (s.l_2, s.m)$.
- **Symmetry Agreement**: For symmetric initial states ($s.l_1 = s.l_2$), $\pi_1(s) = \pi_2(s)$ and decisions agree.
- **Decision Divergence**: Message transmission from $L_1$ to $M$ causes Observer 2's subsequent decision to diverge between runs, demonstrating information transfer without external host oracles.
- **Negative Control**: Local mutations on $L_1$ without transmission to $M$ leave Observer 2 completely invariant.

---

## Verification

To run verification:

```pwsh
# 1. Run full test suite
python -m pytest -v tests

# 2. Build Lean 4 formalization
cd lean
lake build
lake env lean Inventory.lean
cd ..

# 3. Run automated verification harness and check receipt
python verify.py --check
```
