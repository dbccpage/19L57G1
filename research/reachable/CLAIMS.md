# Claims: what the derived process can build, and what it cannot

AuthorityEffect: None.  Every claim below names its Lean theorem or its
Python evidence, its falsifier, and its bound.  The words forced, minimal,
free, canonical, equivalent, universal and complete appear only where a
proof is named.

Definitions shared by the claims, from `lean/Reachable.lean`:

* **InBounds δ** — a delta of at most two items whose new forms have arity
  at most two: the declared candidate space.
* **MinResponse r i j δ** — `validResponse r i j δ`, `InBounds δ`, and no
  valid delta inside the bounds is shorter.  Both declared measures order
  first by item count, so every response the engine accepts is one of these.
* **MinStep r i j δ s** — the sealed `TransStep r i j δ s` (collapsed target,
  valid response, recorded successor) with `MinResponse r i j δ`.
* **Reach root t** — `t = root`, or a supply (`stepE s .admitDatum`) from a
  reachable `s`, or a `MinStep` from a reachable `s`.
* **rootL, rootF** — `⟨2, [], [], [], []⟩` and `⟨3, [], [], [], []⟩`: the
  Challenge 2 close of each reading, which is exactly the root regime of each
  exported tower.

### CL-RE-01 — no reachable state carries a rule

- **Statement**: `Reach root t → t.rules = root.rules`; from either root, a
  reachable state has no uniform rule.
- **Class**: theorem.
- **Lean**: `Reachable.reach_rules`, through `Reachable.minResponse_no_rule`
  (a shortest response has no rule item, from the sealed
  `rule_item_never_minimal`) and `Reachable.applyDelta_no_rule_rules`.
- **Python**: `census.py`, invariant `rule_free` on every exported node
  (`reachable.json:exports.*.invariants.rule_free`).
- **Falsifier**: a reachable state with a rule, or a shortest valid response
  inside the bounds containing `Item.newRuleAll`.
- **Bound**: none on the round count; the response relation is the declared
  candidate space.

### CL-RE-02 — well-formedness is kept

- **Statement**: `Reach root t → root.wf → t.wf`; in particular every
  instance of a reachable state names admitted data and an admitted form of
  matching arity.
- **Class**: theorem.
- **Lean**: `Reachable.reach_wf`, through `Reachable.wf_admitDatum`,
  `Reachable.wf_applyItem`, `Reachable.wf_applyDelta`, `Reachable.wf_impose`,
  `Reachable.wf_respond`.
- **Python**: invariant `well_formed` on every exported node.
- **Falsifier**: a reachable state failing any conjunct of `Regime.wf`.
- **Bound**: none.

### CL-RE-03 — every standing requirement is answered

- **Statement**: `Reach root t → Answered root → Answered t`, where
  `Answered r` says every pair in `r.reqs` is separable in `r`; both roots are
  answered vacuously.  A round answers its own target and keeps every earlier
  one (`answered_of_transStep`); a supply keeps every witness
  (`separable_addDatum`).
- **Class**: theorem.
- **Lean**: `Reachable.reach_answered`, `Reachable.answered_of_transStep`,
  `Reachable.answered_supply`, `Reachable.rootL_answered`,
  `Reachable.rootF_answered`.
- **Python**: invariant `answered` on every exported node.
- **Falsifier**: a reachable state with an imposed pair that no well-formed
  context separates.
- **Bound**: none.

### CL-RE-03b — demanding every pair suffices for a closure fixpoint

- **Statement**: `Reach root t → Answered root → AllPairsDemanded t → Fixpoint t`.
  `AllPairsDemanded` means every ordered admitted pair stands in `t.reqs`;
  `Fixpoint` means every such pair has a separating witness. The latter
  excludes collapsed pairs by `fixpoint_no_collapsed`. The converse from
  fixpoint to all pairs demanded is false, as `closed_F` node 3 demonstrates.
- **Class**: theorem.
- **Lean**: `Reachable.reach_allPairsDemanded_fixpoint`,
  `Reachable.answered_allPairsDemanded_fixpoint`, `Reachable.fixpoint_no_collapsed`.
- **Python**: `reachable.json:exports.*.fixpoints` and `answered_fixpoints`
  are equal in every export, totaling 2944; the separate `all_pairs_demanded`
  population totals 28. The former count of 28 fixpoints is withdrawn.
- **Falsifier**: a reachable fixpoint with a collapsed pair.
- **Bound**: none.

### CL-RE-04 — every admitted form carries an instance

- **Statement**: `Reach root t → root.wf → FormsUsed root → FormsUsed t`,
  where `FormsUsed r` says every form index occurs in some admitted
  instance.  A shortest response inside the bounds never leaves a form
  without an instance: a lone new form separates nothing, so the empty
  response is valid and shorter (`separable_appendForm`); a new form beside
  an item that does not use it can be dropped, again leaving a shorter valid
  response; the only survivor is a new form followed by an instance of that
  very form.
- **Class**: theorem, relative to the declared candidate space (the case
  analysis is over deltas of at most two items).
- **Lean**: `Reachable.reach_formsUsed`, `Reachable.minResponse_formsUsed`,
  `Reachable.formsUsed_pair_not_form`, `Reachable.separable_appendForm`.
- **Python**: invariant `forms_used` on every exported node.
- **Falsifier**: a shortest valid response inside the bounds whose result
  has a form no instance names.
- **Bound**: the declared candidate space; a candidate space allowing three
  or more items is not covered.

### CL-RE-05 — a form without an instance is unreachable

- **Statement**: `formNoInst = ⟨2, [1], [], [], [(0, 1)]⟩` is well-formed,
  rule-free, inside the arity bound, and reachable from neither root.
- **Class**: countermodel (a state inside the bounds that the process cannot
  build).
- **Lean**: `Reachable.formNoInst_unreachable`, with
  `Reachable.formNoInst_wf`, `Reachable.formNoInst_rule_free`,
  `Reachable.formNoInst_arities`, `Reachable.formNoInst_not_formsUsed`.
- **Python**: `reachable.json:countermodels[form_without_instance]` — not
  isomorphic to any exported node; nearest exported node at structural
  distance one, with its replay certificate.
- **Falsifier**: a path of supplies and shortest rounds from a root to a
  state isomorphic to `formNoInst`.
- **Bound**: as CL-RE-04.

### CL-RE-06 — a ruled mark is unreachable

- **Statement**: `ruledMark = ⟨2, [1], [(0, [0])], [0], [(0, 1)]⟩` is
  well-formed and inside the bounds, carries a rule, and is reachable from
  neither root.
- **Class**: countermodel.
- **Lean**: `Reachable.ruledMark_unreachable`, `Reachable.ruledMark_wf`,
  `Reachable.ruledMark_rules_ne`.
- **Python**: `reachable.json:countermodels[ruled_mark]` — not isomorphic to
  any exported node; nearest exported node at structural distance one.
- **Falsifier**: as CL-RE-05, for `ruledMark`.
- **Bound**: none.

### CL-RE-07 — the exported towers agree with the reachability relation

- **Statement**: on every one of the six exported towers, the sealed
  certification passes, every node's regime replays from genesis to its
  recorded hash, every node satisfies CL-RE-01 to CL-RE-04, every supply edge
  admits exactly one fresh datum, and every round edge names a collapsed
  fresh target and carries a response inside the bounds that the sealed
  `min_responses` enumeration, re-run on the parent, returns as one of its
  minima at the recorded cost.
- **Class**: finite computation; this is the computational bridge between
  the engine's responses and `MinResponse`, and it is not a proof of engine
  refinement.
- **Python**: `python census.py --check`; `reachable.json:totals` (nodes,
  edges, rounds, supply, minimum_agreements, with rounds equal to
  minimum_agreements) and `exports.*.edges_checked`.
- **Falsifier**: an exported node failing an invariant or an exported round
  whose response is not among the re-derived minima; the negative tests in
  `tests/test_census.py` and the injection record in `README.md` show the
  check fails by name on each.
- **Bound**: the six committed exports at the pinned commit.

### CL-RE-08 — every exported node is its own isomorphism class

- **Statement**: within each export, the sealed canonical keys of the nodes
  are pairwise distinct, so the per-depth class census equals the per-depth
  node count.
- **Class**: finite computation.
- **Python**: `reachable.json:exports.*.classes_per_depth` and
  `distinct_classes_over_all_exports` (classes recur across exports, never
  within one).
- **Falsifier**: two nodes of one export with equal canonical keys.
- **Bound**: the six committed exports.

## What is not claimed

* That the engine refines `MinStep`: orbit selection, the isomorphism
  quotient and the node guards are not formalized; the correspondence is
  checked edge by edge (CL-RE-07), never proved.
* Anything about responses of three or more items (CL-RE-04, CL-RE-05).
* That the reachable states are exactly the states satisfying the four
  invariants: the invariants are necessary conditions, and CL-RE-05 and
  CL-RE-06 show two of the states they exclude.  Sufficiency is open.
* Any statement about a challenge kind other than pair separation and fresh
  supply.
