# Claims: Target Endogenous Continuum

AuthorityEffect: None.

## What it supports

1. The checked Lean inventory reports 83 declarations: 47 axiom-free and the
   remainder depending only on `{propext, Quot.sound}`. The source scan rejects
   `sorry`, `admit`, `unsafe`, `partial`, and explicit `axiom` declarations in
   this package. This is an inventory claim, not a declaration-completeness
   theorem.
2. Track 1 (Endogenous Observer Enclosure): Verification of local observation evaluation without external history prefix inspection, inductive preservation of internal trace invariants, and immutability of earlier records under forward transitions.
3. Track 2: Python verifies complete finite bonding-map families, morphisms,
   composition, full threads, attainable path prices, and finite path-metric
   checks. Lean proves carrier-prefix projection laws and cost preservation for
   transition sequences whose costs are copied by definition.
4. Track 3: Lean proves acyclicity and a finite length bound for strictly
   decreasing trajectories whose potential has a declared lower bound. Python
   validates closed-cycle witnesses and finite graph pruning.
5. Track 4: Lean proves local-to-global confluence from explicit termination
   and local-confluence hypotheses, then derives conditional normal-form
   uniqueness. Python performs bounded constructive searches and fails closed
   on empty or truncated censuses.
6. Track 5 (Overlapping Dyadic Interval Domain): Lean formalizes exact dyadic
   intervals of width $2^{-(k-1)}$ with overlapping interior $2^{-k}$. Lean proves:
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
7. Exact rational endpoints and integer cover counts in the Python model, with
   explicitly approximate floating logarithmic summaries and
   focused negative controls for float inputs, trace tampering, incomplete or
   non-commuting projections, malformed cycles, non-confluent rewrites, and
   malformed interval covers and partitions.

## What it does not support

1. It does not construct a point-set topology, prove topological connectedness
   of a real interval, or establish a conventional intermediate-value theorem.
2. It does not construct a metric completion or any infinite analytical or
   projective limit. Its connectedness result is for a declared finite overlap graph.
3. It does not assert that arbitrary unbounded discrete dynamics possess cyclic attractors;
   cycle existence is verified only for finite state spaces or declared conservative cycles.
4. It does not claim empirical validity for real-world continuous physics, remaining
   strictly scoped as a constructive discrete relational model.
5. It does not import unverified third-party libraries or unsealed external theories.

## Narrowest defensible claim

Within the checked finite models, the package supplies append-only observer
records, complete carrier coarsenings, validated conservative cycles,
conditional quotient representatives, and an overlapping dyadic interval
domain establishing finite overlap-chain connectedness and confluent rewriting.
Its declared Lean inventory stays within the stated axiom allowlist, and its
focused Python verifier rejects the recorded negative controls. No classical
continuous object or analytical limit follows.

## Next test needed

A separately defined topology or ordered codomain, with hypotheses strong enough
to state the corresponding connectedness or value-attainment theorem.
