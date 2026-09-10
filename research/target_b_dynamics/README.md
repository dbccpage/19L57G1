# Target B: Coherent Observation Scales & Dynamics

AuthorityEffect: None.

Target B establishes the mathematical and operational transition from discrete, finite step execution to inverse systems of finite observation scales, bijective thread spaces, commuting dynamics squares, topological non-density via chain functionality, and quantitative rational limiting bounds on cyclic programs.

---

## 1. Overview and Mathematical Architecture

### 1.1 The Abstract Inverse System (`limits.py`, `Limits.lean`)
- **Stage $c$ $n$**: Finite observation words of length $n$ over a carrier of size $c$: `Stage c n := Fin n → Fin c`.
- **Bonding Map**: Prefix projection forgetting the last entry: `bond c n (t) = t ⟨i, ...⟩`.
- **Thread Space**: Compatible families under bonding at every finite scale: `Compatible c t ↔ ∀ n, bond c n (t(n + 1)) = t(n)`.
- **Sequence Space Bijection**: Constructive bijection between threads and infinite sequences $\mathbb{N} \to \text{Fin } c$ (`toSeq_ofSeq`, `ofSeq_toSeq`) without `Classical.choice` or `mathlib`.
- **Lax Compatibility Refusal**: Eventual agreement does not constitute compatibility (`eventual_not_compatible`).
- **Cofinal Rescaling**: Restriction to even scales preserves the sequence space identically (`restrictEven_eq`, `thread_even`).
- **Non-Locality of Shift**: Shifting a prefix by one entry requires unobserved future data (`shift_not_local`).
- **Dyadic Twin Separation**: The sequences $0111\dots$ and $1000\dots$ differ at scale 1 (`twins_differ_at_scale_one`), refusing identification into an interval or circle without an explicit quotient.

### 1.2 Step-Scale Observations & Target A Process (`observe.py`, `Observe.lean`)
- **Scale Definition**: Observation at scale $n$ reads the execution tape after $n$ deterministic steps: `obs n s = (iter n s).tape`.
- **Prefix Compatibility Theorem**: $\forall n, k: \text{obs}(n, s) \sqsubseteq \text{obs}(n + k, s)$ because deterministic stepping strictly appends to the tape (`obs_prefix`, `obs_prefix_add`).
- **Fuel Independence**: For any $f_1, f_2 \ge n$, two states agreeing on graph, active datum, and tape yield identical observations at scale $n$ (`obs_fuel_indep`, `obs_fuel_eq`).
- **Lost Fuel Witness**: An observation capturing only the tape loses fuel information; states with fuel 0 and fuel 1 share tape `[0]` but diverge after one step (`lost_fuel`).

### 1.3 The Commuting Dynamics Square (`commute.py`, `Commute.lean`)
- **Operational Commuting Law**:
  $$\text{bond}_n(\text{step}_{n+1}(x)) = \text{step}_n(\text{bond}_n(x))$$
- **Trace Commuting Square**: For observation traces $Tr_n(s) = (\text{obs}(0, s), \dots, \text{obs}(n, s))$,
  $$\text{bondTrace}_n(\text{stepTrace}_{n+1}(s)) = \text{stepTrace}_n(s)$$
- **Pointwise Thread Dynamics**: Transition law $F : \text{Fin } c \to \text{Fin } c$ induces an endomorphism on finite stages commuting with bonding (`bond_stepStage_commute`), lifting to a continuous map on $\text{Thread}(c)$ (`stepThread`).
- **Fuel Exhaustion Boundary**: Commutativity holds when fuel is sufficient ($\ge n + 1$); fuel exhaustion halts the transition, exhibiting resource dependency.

### 1.4 Quantitative Readouts & Non-Density (`bounds.py`, `RationalBounds.lean`)
- **Chain Functionality**: Every realized deterministic tape is a chain where consecutive pairs obey $x_{i+1} = \text{nextOf}(g, x_i)$ (`chain_functional`).
- **Topological Non-Density**: The tape `[0, 1, 0, 2]` contains transitions $0 \to 1$ and $0 \to 2$ ($1 \neq 2$), violating functionality. No deterministic program can realize it (`twist_not_chain`). The open cylinder $U_{[0, 1, 0, 2]}$ contains zero realized process tapes, demonstrating in this discrete setting that realized tapes are not dense in the thread space.
- **Quantitative Rational Limiting Bounds**: On the 3-state cycle program ($0 \to 1 \to 2 \to 0$):
  $$L \le 3 \cdot \text{zeros}(L) \le L + 2$$
  $$\left|\frac{\text{zeros}(L)}{L} - \frac{1}{3}\right| \le \frac{2}{3L} \quad \text{in } \mathbb{Q}$$
  Precision budget: for any rational $\epsilon > 0$, taking $L \ge \lceil 2 / (3\epsilon) \rceil$ ensures error $\le \epsilon$. No real numbers ($\mathbb{R}$) or ungrounded continuum completions are used.

---

## 2. Directory Structure

```
research/target_b_dynamics/
├── pyproject.toml              # Pytest configuration
├── limits.py                   # Inverse systems and thread space bijections
├── observe.py                  # Step-scale observations and prefix compatibility
├── commute.py                  # Commuting dynamics square and fuel boundary
├── bounds.py                   # Rational frequency bounds, chain functionality, non-density
├── verify.py                   # Standalone verification and receipt generation harness
├── README.md                   # System documentation
├── CLAIMS.md                   # Scoped claim ledger adhering to Claim Hygiene
├── tests/
│   ├── test_limits.py          # 9 unit tests for inverse systems and thread spaces
│   ├── test_observe.py         # 9 unit tests for step scales and fuel independence
│   ├── test_commute.py         # 5 unit tests for commuting dynamics squares
│   └── test_bounds.py          # 5 unit tests for rational bounds and non-density
├── lean/
│   ├── lean-toolchain          # leanprover/lean4:v4.33.0
│   ├── lakefile.toml           # Lake package definition
│   ├── Limits.lean             # Formal inverse systems, bonding, and bijections
│   ├── Observe.lean            # Formal step scales, prefix compatibility, fuel independence
│   ├── Commute.lean            # Formal commuting dynamics square and thread endomorphisms
│   ├── RationalBounds.lean     # Formal chain functionality, non-density, and zeros bounds
│   └── Inventory.lean          # Metaprogrammed theorem census (114 declarations verified)
└── evidence/
    └── receipt.json            # Cryptographic audit receipt
```

---

## 3. Verification Commands

Run tests locally:
```pwsh
# 1. Python pytest test suite (28 passed)
python -m pytest tests -v

# 2. Lean 4 constructive package build
cd lean
lake build

# 3. Metaprogrammed axiom census and audit
lake env lean Inventory.lean

# 4. Automated verification harness
cd ..
python verify.py --check
```
