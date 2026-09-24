# FINDINGS: Operational Pricing of Dyadic Twin Identification and the Continuum Quotient

`AuthorityEffect: None.`

## VERDICT

**ENUMERATIVE-TWIN-PRICE-DIVERGENT / CONDITIONAL-ON-SEPARATE-PAIR-TARIFFS**

1. **Finite Stage Enumerative Sums**:
   At any finite scale $N \ge 1$, the cumulative sum of declared per-pair tariffs evaluates to finite sums: $\Sigma \mu_1(N) = 2^N - 1$ under capability cost and $\Sigma \mu_2(N) = (N - 1) 2^N + 1$ under transition history cost.

2. **Divergence of Declared Tariff Series**:
   In the limit $N \to \infty$, the cumulative cost under the declared per-pair measures $\mu_1$ (unit tariff per pair) and $\mu_2$ (depth-proportional tariff per pair) diverges without bound.

3. **Status of Operational Impossibility & Continuum Recovery**:
   These results establish price divergence for the declared sequence of separate per-pair tariffs. They do not exclude alternative implementations (such as batching, sharing, or reusable identification rules) or provide a universal trace-level operational lower bound. Similarly, formal topological recovery of the unit interval (connectedness and Hausdorff separation under a quotient topology) remains an open obligation.

---

## THE TWIN OBSTRUCTION

The algebraic, topological, and valuation profile of the dyadic twin adapter quotient:

1. **Cantor Thread Space Separation**:
   In the projective limit thread space $\mathrm{Thread}(c) = \lim_{\leftarrow} \mathrm{Stage}(c, n)$ over alphabet size $c \ge 2$, threads form a compact, totally disconnected Cantor space. Dyadic cylinder boundary twins:
   $$t_{\mathrm{lo}} = w \cdot a \cdot (c-1)^\infty \quad \text{and} \quad t_{\mathrm{hi}} = w \cdot (a+1) \cdot 0^\infty$$
   differ at coordinate $n - 1$ (`TwinRelation.twins_differ_at_scale`), defining distinct threads in Cantor space (`TwinRelation.twins_are_distinct`). At scale 1, the lower twin $0 \cdot 1^\infty$ and upper twin $1 \cdot 0^\infty$ differ at position 0 (`TwinRelation.scale_one_twins_differ`), showing that thread space remains separated without an external quotient.

2. **Boundary Glueing in the Quotient**:
   In the adapter quotient space $\mathrm{TwinQuotient}(c) = \mathrm{Thread}(c) / \sim_{\mathrm{twin}}$, elementary twin boundary threads project to identical points (`QuotientTopology.twin_collapse_in_quotient`). While finite cylinder sets $C(w_{\mathrm{lo}})$ and $C(w_{\mathrm{hi}})$ are strictly disjoint in Cantor space (`QuotientTopology.cylinders_disjoint`), their quotient images intersect at the collapsed boundary point (`QuotientTopology.adjacent_cylinders_glue`).

3. **Destruction of Clopen Partitions & Predicate Transport**:
   The clopen decomposition of Cantor thread space does not factor through the quotient: any predicate on the quotient separating adjacent cylinders must identify their boundary twin (`QuotientTopology.quotient_destroys_clopen_separation`). Because adjacent cylinders glue together across dyadic boundaries, predicates respecting equivalence transport across identified boundary points (`QuotientTopology.locally_constant_chain`, `QuotientTopology.twin_collapse_predicate_transport`). Formal topological connectedness (the absence of non-trivial clopen decompositions under a quotient topology) is not established here and remains an open obligation.

4. **Algebraic Separation of Distinct Points**:
   Distinct quotient points admit thread representatives that are not related under `TwinRel` (`QuotientTopology.quotient_points_distinct_iff`, `QuotientTopology.distinct_quotient_points_representatives_non_equivalent`). Formal Hausdorff separation (the existence of disjoint open neighborhoods in the quotient topology) is not established here and remains an open obligation.

5. **Dyadic Valuation Error Vanishing**:
   For every origin scale $n \ge 1$ and additional depth $k \ge 0$, the integer valuation difference between upper and lower twin representations is identically 1 unit (`QuotientTopology.dyadic_valuation_difference_at_depth`, `QuotientTopology.dyadic_valuation_integer_difference`). The normalized valuation difference $2^{-(n+k)}$ vanishes as resolution depth $k \to \infty$.

---

## THE PRICE FORMULA

Closed-form formulas and asymptotic scaling for operational twin identification:

1. **Twin Cohort Combinatorics**:
   For alphabet size $c \ge 2$ at scale $n \ge 1$, the number of elementary twin pairs is:
   $$N_{\mathrm{twin}}(c, n) = (c - 1) c^{n - 1}.$$
   For base $c = 2$, $N_{\mathrm{twin}}(2, n) = 2^{n - 1}$ (`ValuationPricing.twinCount_base2`), which is strictly positive for all $n \ge 1$ (`ValuationPricing.twinCount_strictly_positive`).

2. **Capability Cost $\mu_1$ (Declared Unit Tariff per Pair)**:
   - Per-pair cost: $\mu_1(\mathrm{pair}) = 1$.
   - Scale cohort cost: $\mu_1(n) = 2^{n - 1}$ (`ValuationPricing.mu1Scale_base2`).
   - Cumulative capability cost to scale $N$:
     $$\Sigma \mu_1(N) = \sum_{n=1}^N 2^{n - 1} = 2^N - 1$$
     (`ValuationPricing.cumulative_mu1_formula`).
   - Asymptotics: $\Sigma \mu_1(N)$ is strictly increasing (`ValuationPricing.mu1_strictly_divergent`) and unbounded (`ValuationPricing.cumulative_mu1_unbounded`).

3. **Cumulative Transition Cost $\mu_2$ (Declared Depth-Proportional Tariff per Pair)**:
   - Per-pair cost: $\mu_2(\mathrm{pair}_n) = n$.
   - Scale cohort cost: $\mu_2(n) = n \cdot 2^{n - 1}$ (`ValuationPricing.mu2Scale_base2`).
   - Cumulative history cost to scale $N$:
     $$\Sigma \mu_2(N) = \sum_{n=1}^N n \cdot 2^{n - 1} = (N - 1) 2^N + 1$$
     (`ValuationPricing.cumulative_mu2_formula`).
   - Asymptotics: $\Sigma \mu_2(N)$ is strictly increasing (`ValuationPricing.mu2_strictly_divergent`) and unbounded (`ValuationPricing.cumulative_mu2_unbounded`).

4. **Markov Cylinder Weighted Obstruction Measure**:
   - Under base-2 uniform Markov cylinder weights $W(w) = 2^{-|w|} = 2^{-n}$ (Kolmogorov consistency), the weighted capability cost at scale $n$ is:
     $$\Omega(n) = 2^{-n} \cdot \mu_1(n) = 2^{-n} \cdot 2^{n - 1} = \frac{1}{2}$$
     (`ValuationPricing.markov_weighted_scale_identity`).
   - The doubling of the twin population ($2^{n-1}$) balances the geometric shrinkage of cylinder volume ($2^{-n}$), leaving a constant weight of $1/2$ at each scale.
   - The cumulative Markov obstruction measure after $N$ scales is:
     $$\Sigma \Omega(N) = \frac{N}{2}$$
     (`ValuationPricing.markov_obstruction_diverges`), which diverges linearly to infinity (`ValuationPricing.markov_obstruction_unbounded`).

5. **Operational Realizability Summary**:
   - At finite scale $N$: $\Sigma \mu_1(N) = 2^N - 1 < \infty$ and $\Sigma \mu_2(N) = (N - 1) 2^N + 1 < \infty$ (`ValuationPricing.finite_stage_price_finite`).
   - At limit $N \to \infty$: the price sequences diverge under $\mu_1$, $\mu_2$, and the Markov obstruction measure (`ValuationPricing.continuum_price_infinite`).
   - A universal operational lower bound over all possible realization traces remains an open obligation.

---

## WHAT WOULD HAVE CHANGED OUR MIND

The following specific findings would have altered the conclusions:

1. **Automatic Limit Boundary Collapse**:
   If dyadic cylinder boundaries had collapsed automatically in the projective limit without an explicit quotient relation. Instead, Theorem 1.1 and Theorem 1.2 demonstrate that boundary twins remain separated at all finite scales and in the thread space limit.

2. **Summable Capability Cost Series**:
   If the cumulative capability cost $\Sigma \mu_1(N)$ had formed a convergent series (for example, if identification at scale $n$ had cost $4^{-n}$ or decayed rapidly enough to yield a finite total sum). Under the declared unit tariff per pair, the cumulative sum grows exponentially as $2^N - 1$.

3. **Summable Markov Obstruction Measure**:
   If Markov cylinder weighting had yielded a summable measure (such as geometric decay $\sum 2^{-n} < \infty$). Instead, the doubling of the twin cohort ($2^{n-1}$) cancels the cylinder shrinkage ($2^{-n}$), yielding a constant weight of $1/2$ per scale and a divergent linear sum.

### Four-Point Claim Hygiene Summary

1. **What it supports**:
   Supports the conclusion that under the declared per-pair tariffs ($\mu_1 = 1$ per pair, $\mu_2 = n$ per pair), the cumulative cost to identify all dyadic boundary twins through scale $N$ scales as $2^N - 1$ and $(N - 1)2^N + 1$, diverging as $N \to \infty$.

2. **What it does not support**:
   Does not support an operational impossibility claim over all possible implementation strategies (batching, sharing, or reusable identification rules), nor does it establish formal topological connectedness or Hausdorff separation for the quotient space.

3. **The narrowest defensible claim**:
   Under the declared valuation tariffs $\mu_1$ and $\mu_2$, the sequence of cumulative prices for identifying all dyadic twins up to scale $N$ diverges to infinity.

4. **The next test needed**:
   Formalization of operational transition semantics with trace execution and lower-bound theorems over admissible identification strategies.

---

## LEDGER

| Target | Claim | Type | Lean Name | Axioms | Status |
|---|---|---|---|---|---|
| **R1.1** | Twins differ at scale $n$ | Theorem | `TwinRelation.twins_differ_at_scale` | `propext`, `Quot.sound` | Verified |
| **R1.2** | Twins are distinct in Cantor space | Theorem | `TwinRelation.twins_are_distinct` | `propext`, `Quot.sound` | Verified |
| **R1.3** | Scale 1 twins differ | Theorem | `TwinRelation.scale_one_twins_differ` | `propext`, `Quot.sound` | Verified |
| **R1.4** | Twins related by equivalence | Theorem | `TwinRelation.twins_are_related` | `propext`, `Quot.sound` | Verified |
| **R1.5** | Twin pair distinctness and relatedness | Theorem | `TwinRelation.twin_pair_distinct_and_related` | `propext`, `Quot.sound` | Verified |
| **R1.6** | Quotient boundary collapse | Theorem | `QuotientTopology.twin_collapse_in_quotient` | `propext`, `Quot.sound` | Verified |
| **R1.7** | Thread separation vs quotient collapse | Theorem | `QuotientTopology.separation_quotient_contrast` | `propext`, `Quot.sound` | Verified |
| **R1.8** | Adjacent cylinders glue at twin | Theorem | `QuotientTopology.adjacent_cylinders_glue` | `propext`, `Quot.sound` | Verified |
| **R1.9** | Destruction of clopen partition | Theorem | `QuotientTopology.quotient_destroys_clopen_separation` | `propext`, `Quot.sound` | Verified |
| **R1.10** | Connected line chain property | Theorem | `QuotientTopology.locally_constant_chain` | `propext`, `Quot.sound` | Verified |
| **R1.11** | Twin collapse predicate transport | Theorem | `QuotientTopology.twin_collapse_predicate_transport` | `propext`, `Quot.sound` | Verified |
| **R1.11a** | Topological connectedness (quotient topology) | Open Obligation | N/A | N/A | Open |
| **R1.12** | Distinct quotient points characterization | Theorem | `QuotientTopology.quotient_points_distinct_iff` | `propext`, `Quot.sound` | Verified |
| **R1.13** | Distinct points have non-equivalent representatives | Theorem | `QuotientTopology.distinct_quotient_points_representatives_non_equivalent` | `propext`, `Quot.sound` | Verified |
| **R1.13a** | Hausdorff separation (disjoint open neighborhoods) | Open Obligation | N/A | N/A | Open |
| **R1.14** | Scale 1 valuation difference is 1 | Theorem | `QuotientTopology.scale_one_valuation_difference` | `propext`, `Quot.sound` | Verified |
| **R1.15** | Dyadic valuation difference identically 1 at all depths | Theorem | `QuotientTopology.dyadic_valuation_difference_at_depth` | `propext`, `Quot.sound` | Verified |
| **R1.16** | Unscaled integer valuation difference is 1 | Theorem | `QuotientTopology.dyadic_valuation_integer_difference` | `propext`, `Quot.sound` | Verified |
| **R2.1** | Base 2 twin count is $2^{n-1}$ | Theorem | `ValuationPricing.twinCount_base2` | None | Verified |
| **R2.2** | Twin count strictly positive | Theorem | `ValuationPricing.twinCount_strictly_positive` | `propext`, `Quot.sound` | Verified |
| **R2.3** | Scale $\mu_1$ cost is $2^{n-1}$ | Theorem | `ValuationPricing.mu1Scale_base2` | None | Verified |
| **R2.4** | Closed-form $\Sigma \mu_1(N) = 2^N - 1$ | Theorem | `ValuationPricing.cumulative_mu1_formula` | `propext`, `Quot.sound` | Verified |
| **R2.5** | Scale $\mu_2$ cost is $n 2^{n-1}$ | Theorem | `ValuationPricing.mu2Scale_base2` | None | Verified |
| **R2.6** | Closed-form $\Sigma \mu_2(N) = (N-1)2^N + 1$ | Theorem | `ValuationPricing.cumulative_mu2_formula` | `propext`, `Quot.sound` | Verified |
| **R2.7** | Cumulative $\mu_1$ strictly increases | Theorem | `ValuationPricing.mu1_strictly_divergent` | `propext`, `Quot.sound` | Verified |
| **R2.8** | Cumulative $\mu_1$ unbounded | Theorem | `ValuationPricing.cumulative_mu1_unbounded` | `propext`, `Quot.sound` | Verified |
| **R2.9** | Cumulative $\mu_2$ strictly increases | Theorem | `ValuationPricing.mu2_strictly_divergent` | `propext`, `Quot.sound` | Verified |
| **R2.10** | Cumulative $\mu_2$ unbounded | Theorem | `ValuationPricing.cumulative_mu2_unbounded` | `propext`, `Quot.sound` | Verified |
| **R2.11** | Markov weighted scale identity $2 \cdot N_{\mathrm{twin}} = 2^n$ | Theorem | `ValuationPricing.markov_weighted_scale_identity` | `propext`, `Quot.sound` | Verified |
| **R2.12** | Linear Markov obstruction $\Sigma \Omega = N$ | Theorem | `ValuationPricing.markov_obstruction_diverges` | None | Verified |
| **R2.13** | Markov obstruction unbounded | Theorem | `ValuationPricing.markov_obstruction_unbounded` | `propext`, `Quot.sound` | Verified |
| **R2.14** | Closed-form finite stage prices | Theorem | `ValuationPricing.finite_stage_price_finite` | `propext`, `Quot.sound` | Verified |
| **R2.15** | Price sequence divergence under declared tariffs | Theorem | `ValuationPricing.continuum_price_infinite` | `propext`, `Quot.sound` | Verified |
| **R2.16** | Universal operational trace lower bound | Open Obligation | N/A | N/A | Open |

## Source pin semantics (2026-09-23)

By the author's ruling of 2026-09-22, `verify_sources.py` separates two claims
that it used to merge.

- **Provenance, which still fails.** Every pinned source hashes to its recorded value at the snapshot; the
  snapshot resolves to a commit that is an ancestor of HEAD and carries
  the recorded tree; and the worktree carries nothing under a sealed
  prefix.
- **Currency, which is now reported.** That nothing pinned has moved
  between the snapshot and HEAD is printed as `DRIFT:` lines, followed by
  a `drift since the snapshot:` count.  It no longer fails.  Pass
  `--require-current` to restore the old failure.

Why the change: the snapshot blob is fixed history, so every authorized
sealed edit turned this check red until a repin, whatever this tree
claimed; the most recent was on 2026-09-23, for pull request 231.  What
this tree claims is about its snapshot, and that is what the check now
enforces.  Runs recorded above were made under the
earlier wording and stand as dated records of those runs.
