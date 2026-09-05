# Change log: the side-free control

Material changes, newest last, each with the reason it was made.  A repair that
narrows a claim says what the claim used to say; a receipt that moves says what
moved it.  `DESIGN.md` and `PREDICTIONS.md` are frozen: no entry here edits
either, and a mis-scored or mislabelled prediction is corrected in `STATUS.md`
and in the ledger beside its value instead.

## 2026-09-05 — repair pass on the review findings

* **The pin verifier's suite test asserted the wrong side of a split.**
  `test_the_verifier_runs_clean_from_the_repository_root` ran `verify_pins.py`
  with no argument and required exit 0.  The pinned commit is on an unmerged
  branch that a checkout fetching only remote refs cannot reach, and in default
  mode the verifier FAILS there by design, so the test reddened the job in
  exactly the clone the `--allow-unreachable-pin` flag exists for.  No document
  here recorded that a test invoked the default mode.  It now asserts the split
  the verifier reports: exit 0 with no flag where the commit is reachable, and
  exit 1 naming the commit then exit 0 under the flag where it is not.  Reason:
  a gate must be asserted where it runs, not where it was written.

* **The CI step that regenerates `receipts/side_free.json` required no diff
  unconditionally.**  That record carries the pinned commit's reachability in
  its own bytes, so a fresh run in a clone that cannot reach the commit cannot
  reproduce the committed bytes; the step was registered in that form even
  though this tree had already recorded the consequence.  The byte comparison
  is now hard where the commit is reachable, and where it is not the diff is
  printed under a named SKIP.  Reason: recording a defect is not a repair of
  it, and a job that goes red on a defect that is not in the code trains a
  reader to ignore it.  Residual, recorded and not closed: in that clone drift
  in this one record is visible in the log and is gated by nothing.

* **P14 scored four of the sixteen assertions its frozen sentence makes.**  Its
  clause set sampled two of the eight points for one fact and two for the
  other, so a violation at any of the twelve unchecked places would still have
  scored HIT.  It now carries both facts at all eight points; the prediction
  was and remains a HIT, and the point count is itself pinned by P9.  Reason: a
  scored population must be the population the frozen sentence quantifies over.

* **P24 is labelled `NOT FORCED` in the frozen file and is FORCED in fact.**
  Renaming permutes indices and never changes the mark count, and both declared
  key choices are constant across the permuted images, so the invariance table
  cannot disagree with itself.  The label is not editable and the machine still
  reports what the frozen file says; the mislabel is recorded in `STATUS.md`
  beside its score, and the hit is no longer counted as content.  Reason: a
  check that cannot fail is not backing, and `DESIGN.md` §12 cited it as
  backing.

* **The carrier module's key-choice comment read backwards.**  It said the
  declared choice "errs AGAINST this control -- the poorer key would give it
  fewer distinctions", while within the only pair that module declares the
  arity key is the richer and so the more generous of the two.  The comment now
  says which of the pair is which, states that neither is load-bearing and why
  that is true by unfolding, and attributes the "errs against" scope to the
  frozen design, which compares the arity key with richer keys outside this
  pair.  Reason: a fairness note that reverses its own sign is worse than none.

* **The collapse map's one-class justification was stated unscoped.**  R47, the
  same note in the record, and the `Collapsed` resolver all said the two pinned
  further-mark points "carry one class key and stand as the two members of one
  retained class".  Read at the pin that holds under the unnamed reading only:
  under the named reading those points carry two different class keys and are
  two classes.  The three places are scoped, and R36 and R38 — whose named
  column is resolved under the map and therefore shows five names where that
  reading has six points — now carry a note saying so.  No decided value moves:
  the decision is taken against the unnamed reading.  Reason: a sentence a
  reader can check against the pin must not be contradicted by it.

* **The Lean theorem cited for "replay is deterministic" stated a tautology.**
  `SideFree.replay_deterministic` was `replay base h = replay base h`, which
  would elaborate against any definition whatever, so the PROVED THEOREM status
  it backed was carried by its doc line.  It is restated as the claim with
  content — replay is a function of the base and the admission subsequence
  alone, so deleting the presentation events from a history leaves the replay
  unchanged.  Name, axiom report and report count are unchanged; the package
  was rebuilt and `lean/axioms.txt` needed no regeneration.  Reason: a citation
  must be carried by the statement, not by the comment above it.

* **The pinned dependence dictionary was described as living in runner modules
  and read by no test.**  Both halves were wrong: the constant is defined in
  the pinned tree's four challenge modules, which its runners import, and a
  test there holds the receipt's copy against that module constant.  The record,
  the rendered document, this tree's ledger and its module prose now say what
  is exactly true — nothing computes the dictionary, and nothing adjudicates
  it.  `DESIGN.md` carries the looser wording and is frozen, so the correction
  is recorded and not edited into it.  Reason: the sentence is the tree's own
  account of what it found, and it was checkable and false.

* **`STATUS.md`'s local-battery transcript was stale on arrival.**  It quoted
  comparison byte counts no committed file had and a pins line missing a field.
  The whole block is re-pasted from a fresh run of the battery at this commit.
  Reason: a status number that names no committed artifact is the drift this
  tree's own discipline forbids, and a stale figure invites doubt about the
  figures beside it that are load-bearing.

* **Receipts recomputed, never patched.**  `receipts/side_free.json` moves from
  541009 to 541191 bytes (P14's clause count and the scoped value-set note);
  `receipts/comparison.json` and `COMPARISON.md` are re-rendered from it.  The
  earlier byte pair quoted for the unreachable-clone computation is superseded
  and is not replaced by a new figure, because that length depends on the
  substituted commit id and on git's own message.
