# Claims: the engine's class, restart, and magnification

AuthorityEffect: None.  Every claim names its hypotheses, its novelty against
the reused results, its evidence, its falsifier and its remaining obligation.
The words forced, minimal, free, canonical, equivalent, universal and complete
appear only where a proof is named.  Lean names are in `lean/` under the
namespaces `EngineClass`, `Restart` and `Magnification`; every report lies
within `{propext, Quot.sound}` (`evidence/lean.json`).

### CL-MG-01 — a minimum carries no rule item

- **Statement**: `IsMin m r i j δ → ∀ f, Item.newRuleAll f ∉ δ`, under either
  declared measure.
- **Hypotheses**: none beyond minimality inside the bounds.
- **Novelty**: the corollary of the sealed `rule_item_never_minimal` for the
  lexicographic cost.
- **Evidence**: `EngineClass.isMin_no_rule`, `mem_dropRules`, `inBounds_dropRules`.
- **Falsifier**: a minimum inside the bounds containing a rule item.
- **Obligation**: none.

### CL-MG-02 — the engine's step as a relation

- **Statement**: `Fire` (a collapsed pair answered by a minimum), `OrbitRep`
  (a collapsed pair least in its orbit under the automorphisms — datum and
  form bijections whose relabelling is the regime up to list order),
  `EngineStep` (fire on an orbit demand, or grow when quiet with supply on),
  `Path`, and `Rooted` (the seed round on the declared target followed by
  engine steps) are definitions over the sealed carrier; `Good` is preserved
  along every path.
- **Hypotheses**: `Good root`.
- **Novelty**: the engine's selection (orbits) and quotient (isomorphism)
  had no Lean object; `TransStep` quantified over every collapsed pair and
  every valid response.
- **Evidence**: `EngineClass.good_fire`, `good_step`, `good_path`,
  `good_rooted`; `fire_transStep`.
- **Falsifier**: a path of engine steps from a `Good` root to a state that
  is ill-formed, carries a rule, or collapses a standing requirement.
- **Obligation**: the relation is *stated*; that the Python engine computes
  exactly it is CL-MG-04, a finite certificate.

### CL-MG-03 — every step decodes to a sealed event block

- **Statement**: a firing replays through `LocalReuse.roundEvents`; a growth
  through `[admitDatum]`; a path and a rooted state through the concatenation.
- **Hypotheses**: none.
- **Novelty**: assembles the merged `local_reuse` replay-cut theorems with
  the relation.
- **Evidence**: `EngineClass.fire_replays`, `grow_replays`, `step_replays`,
  `path_replays`, `rooted_replays`.
- **Falsifier**: an engine step with no sealed event block.
- **Obligation**: none.

### CL-MG-04 — statuses and complete fans at exported representatives

- **Statement**: on each of the six exports, every node's status is the one
  the engine's decision order gives at the count of nodes created before it;
  every expanded node's fan is exactly one edge per orbit demand and per
  minimum class (recorded tie count, class size, cost and orbit count agree;
  the child is the class representative; the response passes the reference
  validity check, belongs to the computed minimum delta family, and matches
  the actual event block) with a fresh supply event block exactly when quiet.
  Duplicate class edges are rejected. Below the recorded cutoff depths
  (1, 3, 6, 15, 5, 15) no cutoff node occurs in the exported traversal.
- **Class**: finite computation over the pinned exports.
- **Evidence**: `magnification.check_export`; `evidence/census.json:exports.*.engine_class`
  (5240 nodes, 5498 edges, 1003 fans, 4546 rounds, 952 supplies, 0 failures).
- **Falsifier**: an exported edge that is not a minimum class, a missing
  class at an expanded node, a status the engine's order does not give; the
  negative tests exhibit each by name.
- **Obligation**: universal engine refinement, full orbit agreement and
  quotient transport remain unproved. Representative-level fan checks alone
  do not establish completeness for all paths of the Lean relation.

### CL-MG-05 — the orbit demands agree with brute force

- **Statement**: on every exported node with at most five data and three
  forms (2461 nodes), the sealed `closure_challenge_orbits` equals the least
  member per orbit under automorphisms enumerated over every datum and form
  bijection pair.
- **Class**: finite computation.
- **Evidence**: `magnification.brute_orbit_check`; `orbit_brute_force.disagreements = []`.
- **Falsifier**: a node where the colouring-based search and the exhaustive
  search give different representatives.
- **Obligation**: nodes above the size cut are not brute-forced.

### CL-MG-06 — restart is exact at the level of the class

- **Statement**: `Path r (l1 ++ l2) t ↔ ∃ c, Path r l1 c ∧ Path c l2 t`;
  the cut is unique; a rooted state restarted with any path is rooted; the
  rooted class is the seed round followed by a path.
- **Hypotheses**: none.
- **Novelty**: the engine-relation form of the merged `local_reuse`
  `responsePath_append_iff`, now with orbit demands and supply included.
- **Evidence**: `Restart.path_append_iff`, `path_cut_unique`,
  `rooted_restart`, `rooted_iff_path`.
- **Falsifier**: a path through a state that does not split there.
- **Obligation**: the measure and supply policy stay fixed; `Rooted` excludes
  the unadvanced root. A unique cut of a fixed state list is not a unique
  future or a liveness result.

### CL-MG-07 — Fire transports under datum renaming

- **Statement**: for a datum bijection `σ` and `Good r`, `Fire m r i j δ t`
  gives `Fire m (renameRegimeR σ.f r) (mapReq σ.f (i,j)).1 (mapReq σ.f (i,j)).2
  (δ.map (mapItem (padF n σ.f))) (renameRegimeR (padF n σ.f) t)`; at a datum
  automorphism the family at the image pair is the renamed family.
- **Hypotheses**: `r.data = n`, `Good r`.
- **Novelty**: the sealed `transStep_rename_fwd` transports the transition;
  the minimum transports too (`validResponse_rename`, cost invariance).
- **Evidence**: `Restart.fire_rename`, `fire_auto`, `cost_map`, `inBounds_map`.
- **Falsifier**: a firing whose renamed response is not a minimum of the
  renamed regime.
- **Obligation**: form bijections, `RegimeExt` automorphisms and transport
  of orbit-selected `EngineStep` are not covered. `fire_auto` requires literal
  equality of the datum-renamed regime. Finite key checks do not discharge
  the general obligation.

### CL-MG-08 — selected two-step restarts against the exports

- **Statement**: for every exported node whose children are all expanded,
  the keys two engine steps away, recomputed by continuing from one freshly
  replayed raw child per computed key without substituting the exported
  representative, equal
  the classes two edges away in the DAG (823 nodes); restarting the class at
  nodes 1, 2 and 3 of `tree_L_mu2` reproduces the exported classes at every
  layer to depth four.
- **Class**: finite computation.
- **Evidence**: `magnification.restart_check`, `restart_from_node`;
  `restart_two_step.failures = []`, `restart_samples`.
- **Falsifier**: a node whose recomputed two-step classes differ from the
  DAG's; the rewired-grandchild negative test exhibits it.
- **Obligation**: nodes with a cutoff child and other raw representatives
  are not checked. This is not universal equivariance.

### CL-MG-09 — the seed targets and the orbit demands

- **Statement**: `OrbitRep rootL 0 1`; `OrbitRep rootF 0 1`;
  `¬ OrbitRep rootF 1 2`.
- **Hypotheses**: none.
- **Novelty**: the reading-F seed round is the declared target, not an orbit
  step; the class up to isomorphism is unaffected (`fire_auto`).
- **Evidence**: `Restart.orbitRep_rootL_01`, `orbitRep_rootF_01`,
  `not_orbitRep_rootF_12`; `root_orbit_demands` in the record.
- **Falsifier**: an automorphism of the L root carrying `(0,1)` below itself.
- **Obligation**: none.

### CL-MG-10 — the declared induced map is constant

- **Statement**: `induced S = ⟨2, [], [], [], [(0,1)]⟩ = R2L` for every
  `PrimitiveCore.Setting`; it is well-formed and its pair is collapsed.
- **Class**: definition and its immediate consequences.
- **Evidence**: `Magnification.induced_eq_R2L`, `induced_constant`,
  `induced_wf`, `induced_collapsed`.
- **Falsifier**: none for this chosen definition. The function ignores every
  field and takes no difference witness; even a setting without related or
  distinct points is mapped to the demanded seed. Necessity, fidelity and
  uniqueness among translations are not established.
- **Obligation**: a translation of a setting's operations, retention or
  protection into the sealed grammar is not defined.

### CL-MG-11 — three fresh-form responses are valid in context

- **Statement**: for `Good r`, admitted distinct `i, j`, the unary mark, the
  binary link and the binary self-loop on a fresh form are valid responses;
  more generally any fresh form with one instance mentioning `i` is.
- **Hypotheses**: `Good r`, `i, j < r.data`, `i ≠ j`.
- **Novelty**: generalizes the sealed `mark_progress` (arity 1, argument
  `[j]`) to every arity and argument list.
- **Evidence**: `Magnification.fresh_form_valid`, `bare_round_embeds`;
  `seed_responses_valid = creation_rounds` in every export.
- **Falsifier**: a `Good` state and a collapsed pair where one of the three
  seed responses is invalid.
- **Obligation**: no whole-tree embedding, injective map of response classes,
  or preservation of minima is proved.

### CL-MG-12 — context changes the minimum

- **Statement**: at the bare difference no response of at most one item is
  valid; at `(1, 2)` in `⟨3, [1], [(0,[0])], [], []⟩` the one-item response
  `[newInst 0 [2]]` is a `mu1` minimum, and the seed's mark is valid there
  but not a minimum.
- **Hypotheses**: none.
- **Novelty**: a countermodel to preservation of the seed minimum family.
- **Evidence**: `Magnification.context_changes_minimum`, `ctx_min1`,
  `bare_mark_not_min_in_context`; the census: one-item minima at 4119 of
  4282 exported creation rounds, a chosen seed delta among the minima at 157.
  The remaining six have two-item minima of secondary `mu2` cost zero using
  existing forms; the fresh-form deltas lose on that second component.
- **Falsifier**: a proof that the minima at a difference depend only on the
  pair.
- **Obligation**: none.

### CL-MG-13 — the records replay

- **Statement**: `evidence/census.json` and `evidence/lean.json` recompute
  byte-identically; the negative tests and the injection record show each
  gate failing by name.
- **Class**: finite computation.
- **Evidence**: `run.py --check`, `verify_lean.py --check`, `tests/`.
- **Falsifier**: a differing byte on recomputation.
- **Obligation**: none.

## What is not claimed

* Universal engine refinement of `EngineStep`; the exports are certified
  at their recorded representatives, and the sealed colouring is not
  proved to compute `OrbitRep`.
* That the canonical key decides isomorphism (sealed residual).
* Transport of firings along form bijections in Lean.
* Any translation of a setting's operations into the sealed grammar; any
  claim about other carriers or three-item responses.
* That a magnification-invariant cost or candidate space, if declared,
  would produce a self-similar tree: that is the named extension, not a
  result.
