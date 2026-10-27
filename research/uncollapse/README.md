# uncollapse

AuthorityEffect: None. Outside the seal. Consumes the sealed `Derivation`
package read-only (`lean/lakefile.toml` requires `../../../lean4`) and
changes nothing in it.

Question: can adding a regime `r'` undo `collapsed r a b`?

`collapsed : Regime → Nat → Nat → Prop` takes one regime, and
`Derivation/Basic.lean` has no regime set, so the question is empty as
stated. It has content under two readings, both answered here.

- **Extension** (`r'` is `r` after admissions). Yes. For a well-formed
  regime, one admitted item keeps a collapsed pair collapsed unless it is an
  instance whose arguments mention one of the two data
  (`uncollapse_only_by_mention`, assembled from R1, R2 and R3 of
  `Derivation/Mention.lean` and `collapsed_ruleAll`). Mentioning is
  necessary, not sufficient. The Challenge 3 response is a witness
  (`uncollapse_by_delta`). Extension is non-monotone in both directions: a
  rule or a second mark collapses a separated pair again
  (`recollapse_by_rule`, `recollapse_by_instance`).
- **Family** (collapse in every member of a list of regimes; `r'` joins).
  Yes, exactly when `r'` separates the pair (`collapsedIn_cons`,
  `uncollapse_family`).

Link to `Derivation/Apartness.lean`: `separable r` is an `IsApart`
(`separable_isApart`, constructive), and
`collapsed r d d' ↔ Indist (separable r) d d'` (`collapsed_iff_indist`), so
collapse is an equivalence by `Apartness.indist_equivalence`. The family
apartness is again an apartness and its indistinguishability is collapse in
every member.

Not claimed: anything about the observation-based collapse of
`ContactBridge.lean` or collapse under renaming; that `applyItem` preserves
`Regime.wf` (needed to chain the single-item result along a delta); that the
regime structure itself is forced by primitive difference.

`python verify.py --check` runs the input pin, tests, strict typing, the Lean
build and the named axiom reports. `python verify.py --write-pins`
regenerates the input digest. `verify.py` is the canonical new-tree copy.
