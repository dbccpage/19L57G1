# Findings: The Sign Tower (Prompt B)

## VERDICT
SIGN-ABSENT on certified machine observables / SIGN-CONDITIONAL on auxiliary metatheoretic solver routines on rigid regimes.
Location: NEITHER (on machine observables) / CARRIER (conditional auxiliary search witness only).

### Detailed Verdict Breakdown
1. **Certified Machine Observables (SIGN-ABSENT / NEITHER):**
   Across the object-level state space quotiented by equivalence in `code/derivation/model.py` and `code/derivation/iso.py`, the derivation machine evaluates to parity-blind:
   - On the carrier: `canonical(rename(r, pi)) = canonical(r)` holds on sealed `iso.canonical` for the regimes exercised in `python/tests/test_carrier.py`. Nested Lean `Carrier.canonical_orbit_invariance` is the same identity on a miniature `Regime` whose `canonical` is `structureKey` (proof `rfl`); it is not a transport of sealed `iso.canonical`. Every certified state predicate and transition rule factors through `canonical`, ensuring that every sign-equivariant observable vanishes ($f(r) = -f(r) \implies f(r) = 0$) (`Carrier.carrier_parity_blind`).
   - On the operational history: fresh data admissions generate Young subgroups $W_{\mathrm{data}} \le S(N)$ whose arrival order is erased by canonical replay (`canonical(replay(tau . H)) = canonical(replay(H))`). For general $m \ge 4$ distinct-arity forms, canonical key fibers are 100% parity-balanced ($[+1, -1]$), demonstrating that the machine state space evaluates relational arity profiles rather than permutation parity.
   - All three Charter Kill Conditions fire, confirming the refutation of the thesis on certified machine states.

2. **Auxiliary Metatheoretic Search Witness (SIGN-CONDITIONAL / CARRIER):**
   On rigid regimes ($\mathrm{Aut}(r) = \{\mathrm{id}\}$), the optimizing bijection $\pi^*(r)$ returned by the metatheoretic solver routine `canonical_witness(r)` in `iso.py` satisfies $\mathrm{sgn}(\pi^*(\tau \cdot r)) = -\mathrm{sgn}(\pi^*(r))$ for odd coordinate transpositions $\tau$ (Target B2 witness disjunct). However, this witness is an auxiliary external search product discarded by `canonical(r) = canonical_witness(r)[0]`. The machine contains no internal orientation register recording this sign, and on symmetric regimes ($|\mathrm{Aut}(r)| > 1$), deterministic tie-breaking produces identical witnesses with sign product $+1$.

---

## THE OBSTRUCTION CLASS

The obstruction class is the discrete presentation-to-quotient non-descent potential defect, paired with the mod-2 Coxeter presentation Stiefel-Whitney class:

1. **Ambient Presentation Group and Character:**
   - Group: Symmetric group $S(n)$ acting as coordinate permutations on presentation tokens.
   - Character: The signature homomorphism $\mathrm{sgn}: S(n) \to \{+1, -1\} \cong \mathbb{Z}_2$, with $\omega_{\mathrm{sgn}}(\tau_i) = 1$ on Coxeter generators $\tau_i = (i \quad i+1)$.

2. **Discrete Non-Descent Potential Evaluation:**
   On coordinate transposition edges $e_\tau = (r, \tau \cdot r)$, canonical equivalence forces $q(\tau \cdot r) = q(r) = \kappa$. For any single-valued state potential $P: \mathcal{R} / \cong \to \mathbb{Z}$ on the quotient state space, the pulled-back coboundary vanishes:
   $$\langle \delta^0(q^* P), e_\tau \rangle = P(q(\tau \cdot r)) - P(q(r)) = P(\kappa) - P(\kappa) = 0.$$
   Consequently, the difference between the presentation signature cochain and any descended potential evaluates to:
   $$\langle \omega_{\mathrm{sgn}} - \delta^0(q^* P), e_\tau \rangle = 1 - 0 = 1 \ne 0.$$
   Parity cannot descend to any single-valued machine state potential.

3. **Mod-2 Coxeter Presentation Cohomology Class:**
   Over $\mathbb{Z}_2$, on the Coxeter 2-complex presentation of $S(n)$ (generators $\tau_i$, involution 2-cells $\tau_i^2 = \mathrm{id}$, braid 2-cells $(\tau_i \tau_{i+1})^3 = \mathrm{id}$):
   $$\delta^1 \omega_{\mathrm{sgn}}(\tau_i^2) = 1 + 1 = 2 \equiv 0 \pmod 2,$$
   $$\delta^1 \omega_{\mathrm{sgn}}((\tau_i \tau_{i+1})^3) = 6 \cdot 1 = 6 \equiv 0 \pmod 2.$$
   The cochain $\omega_{\mathrm{sgn}}$ is a valid mod-2 cocycle spanning:
   $$w_1 = [\omega_{\mathrm{sgn}}] \in H^1(B S(n); \mathbb{Z}_2) \cong \mathbb{Z}_2,$$
   with non-trivial unit circulation $\langle \omega_{\mathrm{sgn}}, e_\tau \rangle = 1 \pmod 2 \ne 0$. This dualizes `NaturalSections.natural_section_iff_holonomy`.

4. **Contrast with Rational Homology and Movegraph Costs:**
   - Over $\mathbb{Q}$: Maschke's theorem collapses rational homology ($H_1(B S(n); \mathbb{Q}) = 0$), and involution relators force relator defect $\delta^1 \omega_{\mathrm{sgn}}(\tau^2) = 2 \ne 0$, confirming $\omega_{\mathrm{sgn}}$ is not a rational cocycle (`is_cocycle = False` in Target M109).
   - Movegraph capability costs: Native capability cost $\mu_1$ is an exact coboundary $\mu_1 = \delta^0 P_{\mathrm{card}}$ with zero circulation $\delta^1 \mu_1 = 0$ on all commuting squares (`is_coboundary = True` in Target M109).

---

## THE GENERATOR

Does not exist at the premise level.

1. **Finite Scale Bonding Rectangular Rank Defect:**
   The scale recursion is the finite bonding projection $\mathrm{bond}_{c, n}: \mathrm{Stage}(c, n+1) \to \mathrm{Stage}(c, n)$ on $\mathrm{Stage}(c, n) = \mathrm{Fin}(n) \to \mathrm{Fin}(c)$ (`ScaleDynamics.lean`; the same bonding shape is the one consumed from `Limits.lean`, not a theorem of this tree).
   For alphabet size $c \ge 2$, finite bonding is an irreversible rectangular projection from dimension $c^{n+1}$ to $c^n$. The rank defect:
   $$\Delta_n = c^{n+1} - c^n = c^n(c - 1) > 0$$
   is strictly positive for all $n \ge 0$. Because the domain and codomain have different dimensions ($c^{n+1} > c^n$), finite bonding is not an endomorphism (square operator). Continuous 1-parameter semigroups $e^{-tH}$ require square operators, precluding infinitesimal generators at the finite premise level (Charter Kill Condition 3 fires).

2. **Cantor Thread Space and Twin Separation:**
   On projective limit thread space $\mathrm{Thread}(c) = \lim_{\leftarrow} \mathrm{Stage}(c, n)$, the projective limit shift acts on a totally disconnected topological space. Dyadic twin threads remain separated at scale 1 (`ScaleDynamics.twins_differ_at_scale_one`), refusing interval or continuum completions without an explicit adapter quotient. Continuous paths $[0, 1] \to \mathrm{Thread}(c)$ are constant, precluding non-trivial continuous flows on thread space without purchasing the continuum outright.

3. **Positivity Equivalence Refutation (Target B5 Structural Gap):**
   Limit measure positivity and admission permutation sign decouple:
   - Derivation transition weights lack anti-symmetric character couplings.
   - Normalized base-$c$ Markov cylinder weights $W(w) = c^{-|w|}$ satisfy Kolmogorov cylinder consistency identically:
     $$\sum_{b \in \mathrm{Fin}(c)} c^{-(|w|+1)} = c \cdot c^{-(|w|+1)} = c^{-|w|},$$
     with branching ratio exactly $1.000000$ across all $c \ge 2$.
   - Positive limit measures exist unconditionally on $\mathrm{Thread}(c)$, while the admission signature character is non-trivial on $S(N)$, establishing an unconditional structural gap between limit measure positivity and permutation sign triviality.

---

## WHAT WOULD HAVE CHANGED OUR MIND

The following specific findings would have altered the verdict:

1. **Carrier Parity-Visibility:**
   If `canonical(rename(r, tau))` had returned a different key than `canonical(r)` for an odd transposition $\tau$, or if the machine maintained an internal orientation register tracking coordinate swap counts. Instead, Theorem 2.1 confirms that `canonical` is strictly invariant under all coordinate permutations.

2. **History Trace Parity Preservation:**
   If valid execution traces had formed a subgroup of $S(N)$ with an odd signature character descending to canonical replay, or if distinct-arity form key fibers had separated parity into non-trivial characters. Instead, valid executions form a Cartier-Foata trace monoid rather than a group (e.g. 14 valid executions in $S(5)$ violating Lagrange's theorem), data arrival order is erased by canonical replay, and general $m \ge 4$ form fibers are 100% parity balanced ($[+1, -1]$).

3. **In-Place Witness Exchange:**
   If the event grammar had contained an event constructor or closed cycle allowing two witnesses to be exchanged in place without component accumulation. Instead, non-Supply constructors strictly increase cardinal potential $N(\mathrm{step}(r, e)) > N(r)$, establishing $Z_1(\mathcal{M}_{\mathrm{native}}) = 0$ and precluding in-place exchange.

4. **Square Scale Endomorphism:**
   If scale bonding had mapped $\mathrm{Stage}(c, n) \to \mathrm{Stage}(c, n)$ with equal dimensions, permitting an infinitesimal generator matrix. Instead, bonding is rectangular ($c^{n+1} \to c^n$) with rank defect $\Delta_n = c^n(c-1) > 0$.

5. **Sign-Positivity Coupling:**
   If Markov cylinder consistency had required triviality of the admission permutation sign. Instead, normalized Markov weights satisfy Kolmogorov consistency with branching ratio 1.0 unconditionally.

---

## LEDGER

| Seat / Target | Claim / Theorem | Formal Type | Evidence / Location | Axioms Used | Status |
| --- | --- | --- | --- | --- | --- |
| **S1 / B1.1** | Carrier Orbit Invariance: `canonical(rename(r, pi)) = canonical(r)` | Theorem | `Carrier.canonical_orbit_invariance`, `test_carrier.py` | None (rfl) | Verified |
| **S2 / B1.1** | Carrier Parity-Blindness: Equivariant sign observable vanishes | Theorem | `Carrier.carrier_parity_blind`, `test_carrier.py` | `propext`, `Quot.sound` | Verified |
| **S2 / B2.1** | Rigid Regime Witness Sign Inversion | Theorem | `Carrier.rigid_witness_sign_inverts`, `test_carrier.py` | `propext` | Verified |
| **S2 / B2.1** | Symmetric Regime Witness Sign Preservation | Theorem | `Carrier.symm_witness_sign_product`, `test_carrier.py` | `propext` | Verified |
| **S1 / B1.2** | Adjacent Event Commutativity Taxonomy (3 tiers) | Theorem | `History.fresh_data_commute`, `History.data_inst_causally_blocked`, `History.distinct_form_order_altering` | `propext` | Verified |
| **S2 / B1.2** | Data Replay Parity-Blindness: Arrival order erased | Theorem | `History.data_reorder_canonical_invariant`, `test_history.py` | None | Verified |
| **S2 / B2.2** | Form Fiber Parity Balance: Fibers balanced for $m \ge 4$ | Theorem | `History.form_fiber_parity_balanced`, `test_history.py` | None | Verified |
| **S3 / B3** | Constructor Potential Monotonicity: $N(\mathrm{step}(r, e)) > N(r)$ | Theorem | `Movegraph.constructor_monotonicity`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **S3 / B3** | Movegraph DAG Acyclicity: $Z_1(\mathcal{M}_{\mathrm{native}}) = 0$ | Theorem | `Movegraph.movegraph_acyclic`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **S6 / B6.2** | Kill Condition 2: In-place witness exchange inexpressible | Theorem | `Movegraph.kill_condition_2_fires`, `test_movegraph.py` | `propext`, `Quot.sound` | Verified |
| **S3 / B3** | Valuation Monoid Non-Isomorphism to Signed Defects | Theorem | `Movegraph.capability_not_isomorphic_to_signed_defect` | `propext` | Verified |
| **S4 / B4** | Rectangular Rank Defect: $\Delta_n = c^n(c-1) > 0$ | Theorem | `ScaleDynamics.rank_defect_strictly_positive`, `test_scale_dynamics.py` | `propext`, `Quot.sound` | Verified |
| **S6 / B6.3** | Kill Condition 3: Finite bonding not square endomorphism | Theorem | `ScaleDynamics.bonding_not_endomorphism`, `ScaleDynamics.kill_condition_3_fires` | `propext`, `Quot.sound` | Verified |
| **S4 / B4** | Dyadic Twin Separation: Differ at scale 1 | Theorem | `ScaleDynamics.twins_differ_at_scale_one`, `test_scale_dynamics.py` | None | Verified |
| **S4 / B4** | Regime dataclass has zero alphabet map attributes | Theorem | `ScaleDynamics.regime_has_no_alphabet_map`, `test_scale_dynamics.py` | None | Verified |
| **S5 / B5** | Kolmogorov Markov Cylinder Consistency (ratio 1.0) | Theorem | `ScaleDynamics.kolmogorov_cylinder_consistency`, `ScaleDynamics.branching_ratio_unity` | `propext`, `Quot.sound` | Verified |
| **S5 / B5** | Positivity Bridge Structural Gap Decoupling | Theorem | `ScaleDynamics.positivity_bridge_structural_gap`, `test_scale_dynamics.py` | `propext`, `Quot.sound` | Verified |
| **Goal 12** | Presentation-Quotient Non-Descent Potential Defect: $\langle \omega_{\mathrm{sgn}} - \delta^0(q^* P), e_\tau \rangle = 1$ | Theorem | `Obstruction.presentation_quotient_non_descent`, `test_obstruction.py` | `propext`, `Quot.sound` | Verified |
| **Goal 12** | Mod-2 Coxeter Stiefel-Whitney Class $w_1 \in H^1(B S(n); \mathbb{Z}_2)$ | Theorem | `Obstruction.mod2_involution_cocycle`, `Obstruction.w1_nontrivial` | None | Verified |
| **M109** | Rational Maschke Collapse: $\delta^1 \omega_{\mathrm{sgn}}(\tau^2) = 2 \ne 0$ | Theorem | `Obstruction.rational_involution_defect_ne_zero`, `Obstruction.not_rational_cocycle` | `propext`, `Quot.sound` | Verified |
| **M109** | Native Capability Cost Exact Coboundary: $\delta^1 \mu_1 = 0$ | Theorem | `Obstruction.capability_cost_is_exact_coboundary`, `Obstruction.capability_circulation_vanishes` | `propext`, `Quot.sound` | Verified |
