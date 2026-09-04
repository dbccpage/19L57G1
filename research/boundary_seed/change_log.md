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
and not by ignorance.

## 2026-09-04, Challenge 0 predictions frozen

`challenge0/PREDICTIONS.md` committed before any code or proof, sha256
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
