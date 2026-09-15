# Claims: Target Endogenous Continuum

AuthorityEffect: None.

## What it supports

1. The checked Lean inventory reports 97 declarations: 49 axiom-free and the
   remainder depending only on `{propext, Quot.sound}`. The source scan rejects
   `sorry`, `admit`, `unsafe`, `partial`, and explicit `axiom` declarations in
   this package. This is an inventory claim, not a declaration-completeness
   theorem.
2. Track 1 (Endogenous Observer Enclosure): Verification of local observation evaluation without external history prefix inspection, inductive preservation of internal trace invariants, and immutability of earlier records under forward transitions.
3. Track 2: Python verifies complete finite bonding-map families, morphisms,
   composition, full threads, attainable path prices, and finite path-metric
   checks. Lean demonstrates carrier-prefix projection laws and cost preservation for
   transition sequences whose costs are copied by definition.
4. Track 3: Lean demonstrates acyclicity and a finite length bound for strictly
   decreasing trajectories whose potential has a declared lower bound. Python
   validates closed-cycle witnesses and finite graph pruning.
5. Track 4: Lean derives local-to-global confluence from explicit termination
   and local-confluence hypotheses, then derives conditional normal-form
   uniqueness. Python performs bounded constructive searches and fails closed
   on empty or truncated censuses.
6. Track 5 (Overlapping Dyadic Interval Domain): Lean formalizes exact dyadic
   intervals of width $2^{-(k-1)}$ with overlapping interior $2^{-k}$. Lean demonstrates:
   - Canonical cover chain-connectedness: every pair of intervals at scale $k$ is
     connected by an explicit constructive overlapping chain.
   - A finite partition boundary lemma: a binary cover-index partition with its
     endpoints in opposite parts contains an adjacent cross-label overlap.
   - Equality transport: observables assigning equal values to overlapping
     intervals are constant across a same-scale chain.
   - Explicit refinement children overlap their parent, and left-child images
     remain connected at the refined scale.
   - Confluent interval contraction: reduction toward canonical normal form is
     locally and globally confluent.
7. Track 6 (Interval Movegraph Dynamics & Discrete Metric Capacity): Lean formalizes
   canonical interval movegraphs with exact operational step costs $\mu_1 = 2^{-k}$
   and quadratic dissipation $\mu_2 = 4^{-k}$. Lean demonstrates:
   - Traversal step count across canonical cover is $2^k - 2$.
   - Cumulative primary traversal cost is strictly bounded: $(2^k - 2) \cdot 2^{-k} < 1$.
   - Cumulative dissipation vanishes exponentially: $(2^k - 2) \cdot 4^{-k} < 2^{-k}$.
   - Traversal dissipation ratio bound: $(2^k - 2) \le 2^k (2^k - 2)$.
   - Dyadic index coarsening $\lfloor i / 2 \rfloor$ preserves adjacent overlapping relations across scales.
   - Discrete metric capacity recurrence $N(k+1) = 2N(k) + 1$, strict capacity monotonicity, and doubling growth bounds.
8. Exact rational endpoints, integer cover counts, and discrete graph morphisms in the Python model, with
   explicitly approximate floating logarithmic summaries and
   focused negative controls for float inputs, trace tampering, incomplete or
   non-commuting projections, malformed cycles, non-confluent rewrites, and
   malformed interval covers and partitions.

## What it does not support

1. It does not construct a point-set topology, establish topological connectedness
   of a real interval, or establish a conventional intermediate-value theorem.
2. It does not construct a metric completion or any infinite analytical or
   projective limit. Its connectedness result is for a declared finite overlap graph.
3. It does not assert that arbitrary unbounded discrete dynamics possess cyclic attractors;
   cycle existence is verified only for finite state spaces or declared conservative cycles.
4. It does not establish continuous capacity or Hausdorff dimension, which require infinite limit constructions.
5. It does not claim empirical validity for real-world continuous physics, remaining
   strictly scoped as a constructive discrete relational model.
6. It does not import unverified third-party libraries or unsealed external theories.

## Narrowest defensible claim

Within the checked finite models, the package supplies append-only observer
records, complete carrier coarsenings, validated conservative cycles,
conditional quotient representatives, an overlapping dyadic interval
domain establishing finite overlap-chain connectedness and confluent rewriting,
and discrete interval movegraph dynamics demonstrating bounded primary traversal costs,
vanishing dissipation, and exact discrete metric capacity recurrence.
Its declared Lean inventory stays within the stated axiom allowlist, and its
focused Python verifier rejects the recorded negative controls. No classical
continuous object, Hausdorff dimension, or analytical limit follows.

## Next test needed

Constructive formalization of coherent projective thread sequences in the interval domain
satisfying operational cost convergence across infinite projective scales.
