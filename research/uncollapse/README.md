# uncollapse

AuthorityEffect: None. Outside the seal. Consumes the sealed `Derivation`
package and the `ignition` research tree read-only (`lean/lakefile.toml`
requires `../../../lean4` and `../../ignition/lean`) and changes nothing in
either.

Question: can adding a regime `r'` undo `collapsed r a b`?

`collapsed : Regime → Nat → Nat → Prop` takes one regime, and
`Derivation/Basic.lean` has no regime set, so the question is empty as
stated. It has content under two readings, both answered here.

- **Extension** (`r'` is `r` after admissions). Yes; the Challenge 3
  response, a two-item delta, is a witness (`uncollapse_by_delta`). For a
  well-formed regime, one admitted item keeps a collapsed pair collapsed
  unless it is an instance whose arguments mention one of the two data
  (`uncollapse_only_by_mention`, assembled from R1, R2 and R3 of
  `Derivation/Mention.lean` and `collapsed_ruleAll`), and so does a whole
  delta (`uncollapse_only_by_mention_delta`, chained by
  `Ignition.applyItem_wf`). Well-formedness is needed: on a regime with an
  instance argument beyond its data, a fresh datum can uncollapse. Mentioning
  is necessary, not sufficient (`mention_not_sufficient`). Extension is non-monotone in both directions: a
  rule or a second mark collapses a separated pair again
  (`recollapse_by_rule`, `recollapse_by_instance`).
- **Family** (collapse in every member of a list of regimes; `r'` joins).
  Yes, exactly when `r'` separates the pair (`uncollapse_family_sep_iff`;
  the witness comes from the context enumeration `Ignition.ctxList`). This
  compares the same indices in every member, so
  it presupposes that an index names one datum across the family. Indices
  are presentation: a regime and its renaming disagree on a raw pair
  (`family_index_dependence`). With a correspondence map per member
  (`collapsedInR`) the same two members agree (`family_index_repaired`), and
  adding a member's renaming with the composed map never uncollapses
  (`collapsedInR_rename_cons`). The maps are presentation data supplied with
  the family; nothing here derives them.

Re-collapse is an operation, not an authorized response. A delta that
separates its target `(1, 2)` but collapses `U0`'s imposed requirement
`(0, 1)` fails `validResponse` by the requirement clause
(`recollapse_breaks_requirement`). The rule re-collapse fails it for the
plainer reason that it collapses its own target (`recollapse_not_validResponse`).
Erasing a distinction and being licensed to erase it are different.

`separable` and `collapsed` take bare naturals, not admitted data
(`separable_unadmitted`: `separable U0 0 99` with 99 unadmitted). Nothing
here is restricted to `d, d' < r.data`.

Link to `Derivation/Apartness.lean`: `separable r` is an `IsApart`
(`separable_isApart`, constructive), and
`collapsed r d d' ↔ Indist (separable r) d d'` (`collapsed_iff_indist`).
`collapsed_equivalence` transports `Apartness.indist_equivalence` along that
link as a consistency check; collapse is an equivalence directly, context by
context, without cotransitivity. The family
apartness is again an apartness and its indistinguishability is collapse in
every member.

Not claimed: anything about the observation-based collapse of
`ContactBridge.lean`; collapse under renaming beyond the statements named
above (U9, U9r), which rest on `Derivation.collapsed_rename`; that the
regime structure itself is forced by primitive difference; that
`input.json`'s `source_revision` is checked, or that the consumed modules are
unchanged (the Lean dependencies are the working tree's, and no module
digests are pinned; the tests check that the pinned modules are exactly the
imports and that their files exist).

`python verify.py --check` runs the input pin, tests, strict typing, the Lean
build and the named axiom reports. `python verify.py --write-pins`
regenerates the input digest. `verify.py` is the canonical new-tree copy.
