# Claims: Target Endogenous Continuum

AuthorityEffect: None.

## What it supports

1. The checked Lean inventory reports 56 declarations: 33 axiom-free and the
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
6. Exact rational and integer Python modeling across the four tracks, with
   focused negative controls for float inputs, trace tampering, incomplete or
   non-commuting projections, malformed cycles, and non-confluent rewrites.

## What it does not support

1. It does not establish infinite-limit analytical structures, continuous topology, or smooth differential manifolds on top of discrete models.
2. It does not construct metric completions or analytical limits in Lean 4.
   The Lean carrier projection structure does not state that projections
   preserve its attached transition lists.
3. It does not assert that arbitrary unbounded discrete dynamics possess cyclic attractors; cycle existence is verified only for finite state spaces or declared conservative cycles.
4. It does not claim empirical validity for real-world continuous physics, remaining strictly scoped as a toy discrete relational model.
5. It does not import unverified third-party libraries or unsealed external theories.

## Narrowest defensible claim

Within the checked finite models, the package supplies append-only observer
records, complete carrier coarsenings, validated conservative cycles, and
conditional quotient representatives. Its declared Lean inventory stays within
the stated axiom allowlist, and its focused Python verifier rejects the recorded
negative controls. No continuous object or analytical limit follows.

## Next test needed

A cross-track model with an explicit map between observer records and projective
states; no such compatibility map is currently defined.
