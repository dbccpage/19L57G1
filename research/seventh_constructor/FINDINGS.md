# FINDINGS: The 7th Constructor (Conservative In-Place Exchange) and Movegraph 1-Cycles

`AuthorityEffect: None.`

## VERDICT

**Z1-NONTRIVIAL-ON-PRESENTATION / QUOTIENT-COLLAPSED / MU1-EXACT-COBOUNDARY / MU2-DISSIPATIVE**

1. **Escape from DAG Acyclicity ($Z_1(\mathcal{M}_{\mathrm{extended}}) \ne 0$)**:
   The conservative 7th constructor $e_{\mathrm{swap}}$ preserves cardinal potential:
   $$N(\mathrm{step}(r, e_{\mathrm{swap}})) = N(r)$$
   (`SeventhConstructor.swap_preserves_cardinal_potential`). On asymmetric regimes, in-place witness exchange produces distinct presentation states ($r_1 \ne r_0$, `SeventhConstructor.r0_ne_r1`). By involutive symmetry ($e_{\mathrm{swap}}(e_{\mathrm{swap}}(r)) = r$, `SeventhConstructor.swap_regime_involutive`), repeated application generates closed execution paths and non-trivial 1-cycles ($r_0 \leftrightarrow r_1$). The directed 1-cycle space is non-vanishing: $Z_1(\mathcal{M}_{\mathrm{extended}}) \ne 0$ (`SeventhConstructor.z1_extended_nontrivial`), escaping the native movegraph DAG acyclicity constraint without external token supply (`SeventhConstructor.swap_preserves_internal_scope`).

2. **Presentation-to-Quotient Projection Collapse**:
   While $e_{\mathrm{swap}}$ generates directed loops in the presentation transition graph, each swap transition maps a regime $r$ to an isomorphic regime $r'$ (`SeventhConstructor.swap_step_isomorphic`). Under canonical quotient projection $q: \mathcal{M} \to \mathcal{M} / \cong$, every swap edge maps to an identity loop at a single quotient point ($q(r_1) = q(r_0)$, `SeventhConstructor.quotient_cycle_collapse`). Consequently, presentation 1-cycles collapse in the quotient state space, yielding vanishing quotient circulation.

3. **Valuation Decoupling ($\oint \mu_1 = 0$ vs $\oint \mu_2 = k > 0$)**:
   Under native capability cost $\mu_1$ (cardinal potential defect), $e_{\mathrm{swap}}$ is an exact 0-coboundary:
   $$\mu_1 = \delta^0 N$$
   (`SeventhConstructor.mu1_equals_potential_difference`), yielding vanishing circulation around every closed cycle ($\oint_\gamma \mu_1 = 0$, `SeventhConstructor.mu1_closed_cycle_circulation_vanishes`). Under cumulative transition history cost $\mu_2$, each operational transition incurs unit cost $\mu_2(e_{\mathrm{swap}}) = 1$ (`SeventhConstructor.mu2_swap_cost_positive`). A closed cycle of length $k$ incurs cumulative transition action:
   $$\oint_\gamma \mu_2 = k \ge 2 \ne 0$$
   (`SeventhConstructor.cycle2_mu2_circulation_strictly_positive`). Circulation is conservative in capability potential but dissipative in operational transition history (`SeventhConstructor.circulation_cost_contrast`).

---

## THE 1-CYCLE SPECTRUM

The topological and homological profile of the extended movegraph:

1. **Native Movegraph DAG Acyclicity**:
   In $\mathcal{M}_{\mathrm{native}}$, all non-supply event constructors strictly increase cardinal potential:
   $$N(\mathrm{step}(r, e)) > N(r)$$
   (`SeventhConstructor.native_non_supply_increases_potential`). This monotonic potential forces the native movegraph to be an acyclic DAG (`SeventhConstructor.native_movegraph_acyclic`), ensuring that the directed 1-cycle space vanishes ($Z_1(\mathcal{M}_{\mathrm{native}}) = 0$).

2. **Conservative 7th Constructor Grammar**:
   The 7th constructor $e_{\mathrm{swap}}(i, j)$ acts on regimes satisfying the admitting condition $n_{\mathrm{data}} \ge 2$ (`SeventhConstructor.admitting_regime_has_swap`). It transposes coordinates $i$ and $j$ on the carrier, preserving the number of data tokens (`SeventhConstructor.swap_data_cardinality`), relational instances (`SeventhConstructor.swap_instances_cardinality`), rules, and requirements without introducing external tokens (`SeventhConstructor.swap_preserves_internal_scope`).

3. **Explicit 1-Cycle Generation**:
   On asymmetric regime $r_0$ with 2 tokens and directed instance $(0, 1)$, applying $e_{\mathrm{swap}}(0, 1)$ yields $r_1$ with instance $(1, 0)$ (`SeventhConstructor.r1_instances_eval`). Since $(0, 1) \ne (1, 0)$, $r_0 \ne r_1$ (`SeventhConstructor.r0_ne_r1`). Applying $e_{\mathrm{swap}}(0, 1)$ to $r_1$ returns to $r_0$ (`SeventhConstructor.swap_returns_to_r0`), producing a directed 2-cycle $\gamma_2 = (r_0 \to r_1 \to r_0)$. In the 1-chain complex, $\partial \gamma_2 = 0$ everywhere (`SeventhConstructor.gamma2_is_cycle`), demonstrating non-trivial 1-homology $Z_1(\mathcal{M}_{\mathrm{extended}}) \ne 0$ (`SeventhConstructor.z1_extended_nontrivial`).

4. **Quotient Circulation & Non-Descent Obstruction**:
   Every swap transition preserves isomorphism: $r \cong \mathrm{step}(r, e_{\mathrm{swap}})$ (`SeventhConstructor.swap_step_isomorphic`). Any state invariant or quotient function $q$ factoring through isomorphism evaluates to identical values on $r_0$ and $r_1$ (`SeventhConstructor.quotient_cycle_collapse`). While the presentation signature cochain assigns $\langle \omega_{\mathrm{sgn}}, e \rangle = 1$ to each swap edge, any descended potential coboundary vanishes:
   $$\langle \delta^0(P \circ q), e \rangle = P(q(r_1)) - P(q(r_0)) = 0.$$
   The resulting difference evaluates to an exact unit defect:
   $$\langle \omega_{\mathrm{sgn}} - \delta^0(P \circ q), e \rangle = 1 \ne 0$$
   (`SeventhConstructor.presentation_quotient_obstruction`), demonstrating that presentation circulation does not descend to a quotient potential.

---

## THE VALUATION COST

Operational pricing under capability cost $\mu_1$ and transition cost $\mu_2$:

1. **Capability Cost $\mu_1$ (Cardinal Potential Defect)**:
   - Valuation: $\mu_1(e_{\mathrm{swap}}) = 0$ (`SeventhConstructor.mu1_swap_zero`).
   - Exact Coboundary Status: For every event constructor $e$, $\mu_1(e) = N(\mathrm{step}(p, e)) - N(p)$ (`SeventhConstructor.mu1_equals_potential_difference`).
   - Telescoping Identity: Along any trajectory $es$, the cumulative cost telescopes to $\Sigma \mu_1(es) = N(\mathrm{Trajectory}(p, es)) - N(p)$ (`SeventhConstructor.cumulative_mu1_telescopes`).
   - Vanishing Circulation: Around any closed execution loop returning to initial potential, circulation vanishes: $\oint_\gamma \mu_1 = 0$ (`SeventhConstructor.mu1_closed_cycle_circulation_vanishes`, `SeventhConstructor.cycle2_mu1_circulation_zero`).

2. **Cumulative Transition Cost $\mu_2$ (Operational Action)**:
   - Valuation: $\mu_2(e_{\mathrm{swap}}) = 1$ (`SeventhConstructor.mu2_swap_cost_positive`).
   - Cumulative Trajectory: Executing $k$ consecutive swap steps incurs cumulative transition action $\Sigma \mu_2(k) = k$ (`SeventhConstructor.cumulative_mu2_k_swaps`).
   - Non-Zero Circulation: Around the 2-cycle $\gamma_2$, circulation evaluates to $\oint_{\gamma_2} \mu_2 = 2 \ne 0$ (`SeventhConstructor.cycle2_mu2_circulation_strictly_positive`).

3. **Operational Decoupling**:
   In-place witness exchange permits closed loops without resource accumulation ($|D|, |F|, |I|, |R|, |Q|$ invariant), but each loop step accumulates non-zero operational transition action (`SeventhConstructor.circulation_cost_contrast`).

---

## WHAT WOULD HAVE CHANGED OUR MIND

The following findings would have altered the verdict:

1. **External Token Requirement**:
   If executing an in-place swap had required supplying external presentation tokens or increasing carrier cardinality. Instead, Theorem 1.8 demonstrates that all exchanged components remain strictly within the internal scope of the admitted regime.

2. **Persistent Movegraph Acyclicity**:
   If the extended movegraph had remained an acyclic DAG with $Z_1 = 0$ after admitting $e_{\mathrm{swap}}$. Instead, Theorems 2.7 and 2.8 exhibit concrete closed 1-cycles and demonstrate in this model that $Z_1(\mathcal{M}_{\mathrm{extended}}) \ne 0$.

3. **Non-Trivial Capability Circulation ($\oint \mu_1 \ne 0$)**:
   If $e_{\mathrm{swap}}$ had accumulated or depleted cardinal capability potential along closed paths. Instead, Theorems 3.2 and 3.4 establish that $\mu_1$ is an exact coboundary with identically vanishing circulation.

4. **Quotient Loop Preservation**:
   If the generated 1-cycles had remained non-trivial after projection to the canonical isomorphism quotient state space ($q(r_1) \ne q(r_0)$). Instead, Theorem 2.10 demonstrates that all swap edges map to isomorphic states, collapsing cycles to single quotient points.

### Four-Point Claim Hygiene Summary

1. **What it supports**:
   Supports the conclusion that admitting the conservative 7th constructor $e_{\mathrm{swap}}$ escapes native DAG acyclicity, generating non-trivial presentation 1-cycles ($Z_1 \ne 0$) without external supply, with exact coboundary capability pricing ($\oint \mu_1 = 0$) and strictly positive transition action ($\oint \mu_2 = k$).

2. **What it does not support**:
   Does not support the claim that cycles survive canonical isomorphism quotienting (cycles collapse to trivial points under $q$), nor that presentation parity descends to internal quotient observables.

3. **The narrowest defensible claim**:
   Under $e_{\mathrm{swap}}$, the presentation movegraph admits non-trivial directed 1-cycles that cost zero capability potential but dissipate positive transition action, with all such cycles collapsing to single points in the canonical quotient space.

4. **The next test needed**:
   Exploration of non-invertible or quotient-separating rewrite rules to determine whether 1-cycles can be sustained on the quotient state space $\mathcal{M} / \cong$.

---

## LEDGER

| Seat / Target | Claim / Theorem | Formal Type | Evidence / Location | Axioms Used | Status |
| --- | --- | --- | --- | --- | --- |
| **R1 / B3** | Swap Cardinality Preservation: $N(\mathrm{step}(p, \mathrm{swap})) = N(p)$ | Theorem | `SeventhConstructor.swap_preserves_cardinal_potential`, `test_conservative_grammar.py` | None | Verified |
| **R1 / B3** | Native Constructor Strict Monotonicity | Theorem | `SeventhConstructor.native_non_supply_increases_potential`, `test_conservative_grammar.py` | `propext`, `Quot.sound` | Verified |
| **R1 / B3** | Supply Identity on Cardinal Profile | Theorem | `SeventhConstructor.supply_is_identity`, `test_conservative_grammar.py` | None | Verified |
| **R1 / B3** | Admitting Regime Solvability: $n_{\mathrm{data}} \ge 2 \implies \exists \mathrm{swap}$ | Theorem | `SeventhConstructor.admitting_regime_has_swap`, `test_conservative_grammar.py` | `propext`, `Quot.sound` | Verified |
| **R1 / B3** | Transposition Involutive Property: $\tau(\tau(x)) = x$ | Theorem | `SeventhConstructor.transposition_involutive`, `test_conservative_grammar.py` | None | Verified |
| **R1 / B3** | Swap Data Cardinality Preservation | Theorem | `SeventhConstructor.swap_data_cardinality`, `test_conservative_grammar.py` | None | Verified |
| **R1 / B3** | Swap Instance Cardinality Preservation | Theorem | `SeventhConstructor.swap_instances_cardinality`, `test_conservative_grammar.py` | `propext` | Verified |
| **R1 / B3** | Swap Regime Involution: $e_{\mathrm{swap}}(e_{\mathrm{swap}}(r)) = r$ | Theorem | `SeventhConstructor.swap_regime_involutive`, `test_conservative_grammar.py` | None | Verified |
| **R1 / B3** | Scope Preservation Without External Supply | Theorem | `SeventhConstructor.swap_preserves_internal_scope`, `test_conservative_grammar.py` | `propext`, `Quot.sound` | Verified |
| **R2 / B3** | Native Movegraph DAG Acyclicity: $Z_1(\mathcal{M}_{\mathrm{native}}) = 0$ | Theorem | `SeventhConstructor.native_movegraph_acyclic`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **R2 / B3** | Distinctness of Swapped Regime: $r_0 \ne r_1$ | Theorem | `SeventhConstructor.r1_instances_eval`, `SeventhConstructor.r0_ne_r1`, `test_movegraph.py` | None | Verified |
| **R2 / B3** | Return to Initial State: $\mathrm{swap}(r_1) = r_0$ | Theorem | `SeventhConstructor.swap_returns_to_r0`, `test_movegraph.py` | None | Verified |
| **R2 / B3** | 2-Cycle Vanishing Boundary at $r_0$ | Theorem | `SeventhConstructor.gamma2_boundary_r0`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **R2 / B3** | 2-Cycle Vanishing Boundary at $r_1$ | Theorem | `SeventhConstructor.gamma2_boundary_r1`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **R2 / B3** | 2-Cycle Closeness: $\partial \gamma_2 = 0$ | Theorem | `SeventhConstructor.gamma2_is_cycle`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **R2 / B3** | Non-Trivial 1-Homology: $Z_1(\mathcal{M}_{\mathrm{extended}}) \ne 0$ | Theorem | `SeventhConstructor.z1_extended_nontrivial`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **R2 / B3** | Swap Step Preserves Isomorphism Class | Theorem | `SeventhConstructor.swap_step_isomorphic`, `test_movegraph.py` | None | Verified |
| **R2 / B3** | Cycle Collapse in Quotient: $q(r_0) = q(r_1)$ | Theorem | `SeventhConstructor.quotient_cycle_collapse`, `test_movegraph.py` | None | Verified |
| **R2 / B3** | Presentation-Quotient Non-Descent Defect | Theorem | `SeventhConstructor.presentation_quotient_obstruction`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **R3 / B3** | Capability Cost of Swap is Zero: $\mu_1(e_{\mathrm{swap}}) = 0$ | Theorem | `SeventhConstructor.mu1_swap_zero`, `test_valuation_pricing.py` | None | Verified |
| **R3 / B3** | Exact Coboundary Identity: $\mu_1 = \delta^0 N$ | Theorem | `SeventhConstructor.mu1_equals_potential_difference`, `test_valuation_pricing.py` | `propext`, `Quot.sound` | Verified |
| **R3 / B3** | Trajectory Capability Telescoping Sum | Theorem | `SeventhConstructor.cumulative_mu1_telescopes`, `test_valuation_pricing.py` | `propext`, `Quot.sound` | Verified |
| **R3 / B3** | Vanishing Cycle Circulation: $\oint \mu_1 = 0$ | Theorem | `SeventhConstructor.mu1_closed_cycle_circulation_vanishes`, `test_valuation_pricing.py` | `propext`, `Quot.sound` | Verified |
| **R3 / B3** | Transition Action of Swap is Positive: $\mu_2(e_{\mathrm{swap}}) = 1$ | Theorem | `SeventhConstructor.mu2_swap_cost_positive`, `test_valuation_pricing.py` | None | Verified |
| **R3 / B3** | 2-Cycle Capability Circulation Zero | Theorem | `SeventhConstructor.cycle2_mu1_circulation_zero`, `test_valuation_pricing.py` | None | Verified |
| **R3 / B3** | 2-Cycle Transition Circulation Positive: $\oint \mu_2 = 2$ | Theorem | `SeventhConstructor.cycle2_mu2_circulation_strictly_positive`, `test_valuation_pricing.py` | None | Verified |
| **R3 / B3** | Circulation Cost Contrast Decoupling | Theorem | `SeventhConstructor.circulation_cost_contrast`, `test_valuation_pricing.py` | None | Verified |
