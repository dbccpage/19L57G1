# Change log: the boundary derivation

`AuthorityEffect: None`.  Material revisions, newest last, each with its
reason.

## 2026-09-04, seed commit

`SEED.md` committed byte-identically to the reviewed draft, sha256
`ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be`,
with `.gitattributes` marking the seed, the freeze file, and the receipts
`-text`.

## 2026-09-04, plan and manual

`PLAN.md` and `MANUAL.md` committed before any substantive work, with
three declared readings; reading zero records that blindness is by rule
and not by ignorance.  That provenance wording is withdrawn by the
exact-head review entry below because the declared prior exposure is material.

## 2026-09-04, Challenge 0 predictions frozen

`challenge0/PREDICTIONS.md` committed before the branch's first code-or-proof
commit, sha256
`a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395`.

## 2026-09-04, Challenge 0

Kernel, Lean package, tests, receipt, paper, ledger.  Three things were
repaired during the challenge and are recorded here rather than hidden:

- The Lean event constructor was first named with the forbidden word for
  admission and the tree's own forbidden-token scan failed on four lines
  of `Basic.lean`; the constructor became `place`.  A live failure of the
  gate, not an injection.
- The reflection census first compared regimes with their presentation
  tokens, so a placement that the reflection fixes only after a mark
  renaming looked moved and the equal-count law came out false; the
  census test caught it, and the comparison now forgets tokens.
- The Lean verifier first expected bare report lines and found none in
  Lake's prefixed output; the parser now finds the report inside the
  line.

Prediction C0-5's general clause was true and too narrow; the sharper
fact (fixed up to mark renaming exactly when the counts are equal) is
recorded as a computation to four marks, and the prediction file is
untouched.

## 2026-09-04, exact-head adversarial review repair

`SEED.md` and `challenge0/PREDICTIONS.md` remain byte-identical.  Review
found that the first Challenge 0 implementation and prose did not support
several of their claims.  The repair is recorded rather than folded into
the earlier entry:

- Restored the seed's supplied opaque initial datum to Python, Lean, the
  receipt, paper, and ledger.  The boundary is the admitted primitive
  exception, not a replacement for that datum.
- Replaced the ambiguous observation surface with a closed positive
  `OnSide | SideNamed` judgment grammar.  `contents` and `side_profile` are
  now explicitly metatheoretic extensions.  WITHDRAWN: “no observation
  fires” under both readings.  The supported claim is that no `OnSide`
  judgment holds; the two O name judgments do hold; no primitive empty or
  count constructor is declared.  No general nondefinability theorem is
  claimed.
- Added an explicit empty Challenge 0 event-follows relation and Lean
  theorem.  The Python return-annotation census is supplementary, not proof
  that state produces no event; it now detects nested/optional event return
  annotations.  Certifying replay refuses admission of a new unsupplied
  token.
- Corrected reflection semantics: raw O genesis is fixed, but reflection is
  not a permitted O automorphism.  The scorer now consumes both facts.  Its
  general-clause status fails closed and every machine-readable fact names
  the zero-through-four-mark bound and U-only permission.  The state-level
  automorphism predicate now requires stabilization up to mark renaming;
  sharing a canonical U orbit with a reflected state is not enough.
- Added regime invariant checks and withdrew the unbounded canonical-key
  iff.  Canonical completeness and class separation are claimed only for
  the enumerated bound.
- WITHDRAWN: “Five FORCED or DEFINITION-level hits ... in advance.”  C0-4
  was frozen as `NOT FORCED`; four genesis portions were labelled FORCED.
  C0-4 is scored PARTIAL: its emptiness target survives the closed grammar,
  but its frozen “no observation fires” rationale is false under O.
  Commit history establishes only that predictions were committed before
  branch code/proofs, not when off-tree work was written.
- WITHDRAWN: “blind derivation.”  The instrument's declared use of remembered
  prior structure leaves `SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE` and
  licenses no blind-independence or convergence inference.
- Added the seed-required boundary-dependence classification.  The initial
  datum, supply inertia, and empty event-follows relation survive boundary
  removal; side-specific results do not.
- Pinned frozen predictions and the axiom receipt as `-text` for clean
  Windows checkouts; hardened pin/source-isolation checks over working,
  index, HEAD, and history bytes; corrected sealed-name/path coverage and
  exact seed exemption; made undecodable content fail closed; required a
  successful `lake clean`.
- Corrected the coverage gate to compute true line coverage from covered
  lines/statements rather than Coverage.py's combined percentage.  The old
  “line 98.09%” was actually the combined metric and is withdrawn.  The
  repaired 53-test run measures line 100.00% and branch 100.00% over the
  three declared code files.
- A working or staged `FREEZE.md` no longer retires source isolation.  A
  committed marker does, but does not validate the seed's self-referential
  “hash every file” instruction; a verified parent-tree or explicit-exclusion
  protocol remains OPEN.
