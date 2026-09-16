# Claims: Target Endogenous Continuum

AuthorityEffect: None.

## What it supports

1. The checked Lean inventory reports 116 declarations: 54 axiom-free and the
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
7. Track 6 (Interval Movegraphs and Finite Cover Counts):
   - Python constructs the declared canonical interval graph and assigns exact
     rational edge costs $\mu_1 = 2^{-k}$ and $\mu_2 = 4^{-k}$.
   - Lean constructs forward and backward adjacent overlap edges and proves the
     natural-number step-count and numerator inequalities used by the normalized
     finite cost formulas.
   - Lean proves that index-halving maps adjacent fine intervals to equal or
     adjacent coarse indices.
   - The declared finite cover count $N(k)=2^k-1$ obeys
     $N(k+1)=2N(k)+1$ and the recorded finite monotonicity bounds.
8. Track 7 (Path Potentials and Checked Hierarchical Pruning):
   - Lean proves that an admissible potential lower-bounds every supplied path,
     that a strict lower-bound/budget separation refuses that path, and that a
     tight admissible path is minimal among other admissible paths.
   - The Lean coarse-to-fine theorem is conditional on an explicit
     lifted-admissibility hypothesis. Its transition lemma separately requires
     an equal projected edge cost, while collapsed edges are immediate.
   - Python computes exact shortest-distance potentials on finite graphs after
     validating exact non-negative edge costs.
   - Before using a coarse numerical bound, Python verifies both the movegraph
     morphism and the lifted inequality on every relevant fine edge. If the
     lift fails, it uses an unguided exact fine search. Projected
     unreachability may still prune under a verified morphism.
9. Focused negative controls cover float inputs, negative costs, unknown states,
   malformed or incomplete projections, an inadmissible coarse lift, malformed
   cycles, non-confluent rewrites, and malformed interval covers and
   partitions.
10. The scale-$\{4,6,8\}$ benchmark is bounded telemetry only. For the default
    interval costs, it records that the raw cross-scale potential is not an
    admissible fine potential and that the solver falls back to fine search. It
    establishes no general node reduction or timing advantage.
11. Track 8 (Allocation Conservation and Budgeted Coordination):
    - Lean proves allocation/reclamation/redistribution conservation for a
      natural-number allocation state with no consumed-budget field. Its
      refusal result retains the explicit lifted-admissibility premise, and its
      step bound follows from a supplied unit-step accounting equation.
    - Python validates the full exact ledger equation including consumed
      budget, non-negative allocations and weights, unique goal identifiers,
      and one-shot execution.
    - `BudgetedReasoningCoordinator` screens allocations with exact finite
      shortest-distance bounds, reassigns reclaimed amounts, and then invokes
      checked coarse-to-fine search. Its SHA-256 values are deterministic
      content checksums, not signatures or authenticity proofs.

## What it does not support

1. It does not construct a point-set topology, establish topological connectedness
   of a real interval, or establish a conventional intermediate-value theorem.
2. It does not construct a metric completion or any infinite analytical or
   projective limit. Its connectedness result is for a declared finite overlap graph.
3. It does not assert that arbitrary unbounded discrete dynamics possess cyclic attractors;
   cycle existence is verified only for finite state spaces or declared conservative cycles.
4. It does not establish continuous capacity or any limiting dimension, which
   require infinite limit constructions.
5. It does not claim empirical validity for real-world continuous physics, remaining
   strictly scoped as a constructive discrete relational model.
6. It does not import unverified third-party libraries or unsealed external theories.
7. It does not provide a general continuous optimization solver, a general
   complexity theorem, or a performance guarantee for hierarchical search.
8. It does not establish the lifted-admissibility premise merely from a graph
   morphism. The executable checks that premise and falls back when it fails.
9. Its deterministic checksums do not establish provenance, authorization,
   tamper resistance, or external identity.

## Narrowest defensible claim

Within the checked finite models, the package supplies append-only observer
records, complete carrier coarsenings, validated conservative cycles,
conditional quotient representatives, an overlapping dyadic interval
domain establishing finite overlap-chain connectedness and confluent rewriting,
discrete interval movegraphs with finite cost summaries, exact finite-graph path
potentials, runtime-checked coarse-to-fine pruning with a safe fine-search
fallback, and a one-shot budgeted coordinator with exact rational conservation.
Its declared Lean inventory stays within the stated axiom allowlist, and its
focused Python verifier rejects the recorded negative controls. No classical
continuous object, limiting dimension, or analytical limit follows.

## Next test needed

Construct a non-identity finite abstraction whose projected potential passes
the executable lifted-edge check, then compare its bounded search telemetry
against the current fallback cases without extrapolating beyond those graphs.
