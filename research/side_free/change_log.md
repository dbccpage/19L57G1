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

## 2026-09-05 — second repair pass: what the first pass left behind

* **The key-choice repair reached the comment and not the record.**  The entry
  above says the reversed fairness note was repaired; it repaired
  `code/sidefree/model.py` and left the same reversed sentence in
  `control.py`'s `key_choice_invariance.why_the_arity_is_declared`, which is
  the copy that reaches `receipts/side_free.json` and so the copy a reader
  cites.  The record now carries the reconciled wording the module carries:
  within the two declared choices the arity key is the richer and so the more
  generous to this control, the "errs against" scope belongs to the frozen
  design's comparison with richer keys outside the pair, and neither declared
  choice is load-bearing, which is DEFINITION-level.  `STATUS.md` says the
  first repair reached only the comment.  Reason: a repair recorded as done and
  done in one of two places is worse than one recorded as partial.

* **A guard was claimed on the record it does not cover.**  The receipt's
  `decided.plurality_is_not_price` said "a test asserts that no field of this
  receipt combines them".  The only key-walking scan for routes against price
  ran over `receipts/comparison.json`, never over this one.  A second walk now
  runs over this record, and it pins an exact set rather than requiring an
  empty one: the declaration itself is a field whose name carries both words,
  in the primary block and in the secondary, and excluding it by hand would be
  curated where an exact set is not.  The receipt sentence and the ledger's
  SF-ROUTES boundary now say which test covers which record.  Reason: a
  sentence naming a guard must name a guard that runs where it says.

* **SF-OPEN-E quoted byte figures the entry above declared superseded.**  Its
  statement in `comparison.py` — and so `receipts/comparison.json` and
  `COMPARISON.md` — still read "a fresh computation returns 541041 bytes
  against the committed 541009", when the committed record then stood at
  541191, and still described the CI step in its pre-repair form.  A test
  asserted on the literal `541041`, so the stale figure was held in place by
  the suite.  The
  statement now says what the ledger and `STATUS.md` say: the fresh record
  differs in exactly the two lines of `gates.G1.commit_check`, no byte count is
  quoted because that length depends on the substituted id, and the CI step is
  repaired to the reachability split.  The test asserts on those two lines, and
  a second test asserts that the statement quotes no byte count at all.
  Reason: this is the drift this tree's own discipline forbids, and it had been
  written into the deliverable document.

* **The boundary-number totality claim was false for one row.**  SF-NO-HAND-
  TYPED-BOUNDARY-NUMBER said every boundary value the comparison uses is read
  at a pinned JSON path and declared a second time, 91 for 91.  R40's two
  boundary columns are minima of the restricted second measure, taken over this
  tree's own mirror rows; no pinned path carries them, the resolver records a
  use only for a pinned read, and so gate C1's totality never saw them.  The
  ledger and `STATUS.md` now state the exception and name what does hold those
  two cells — `second_measures.data_join_against_the_pin`, 48 rows per reading
  with its mismatches reported, which is a weaker guarantee than the one that
  was claimed.  `COMPARISON.md` already said "computed from a pinned receipt or
  from a carrier" and needed no change.  Reason: a totality claim with one
  unnamed exception is the kind of claim this tree exists to refuse.

* **R45's control cell was a typed-in string labelled "computed here".**  The
  row compares the pinned world's declared payer against the control's, and the
  control's was resolved through `Computed`, so the record cited it as computed
  and its BOUGHT_NOTHING status was an asserted sameness counted in the
  headline.  There is now a `Declared` source kind beside `Computed`: the value
  is declared in one table with the reason it is not computed — this carrier
  has no genesis declaration of a payer and its enumeration produces none — and
  the cell cites itself as declared.  Each row carries
  `the_control_field_is_declared_not_computed` and `is_definition_level`, the
  latter true exactly when both columns are declarations and the agreement is
  therefore true by unfolding.  R45 is the only such row.  Nothing is curated
  out: the verdict reports its tallies with the two declared-field rows and
  without them — 26 and 19 becomes 25 and 18, and 9 and 7 becomes 8 and 6 —
  and the reader may take either.  Reason: a declaration presented as a
  measurement is content this comparison did not earn.

* **Three published gates were absent from the injection census.**  `MANUAL.md`
  publishes C0 to C4 and recorded probes for C0 and C1 only, so a reader
  auditing gate by gate would conclude C2, C3 and C4 were unproved.  They were
  proved, as permanent tests over deep copies; the paragraph that names the
  other permanent probes now names these six with the diagnostics they produce.
  Reason: a census of what has been proved must reach every gate the table
  publishes.

* **The committed byte count was quoted in prose that outlives it.**  Repairing
  the item above left `CLAIM_LEDGER.md` and `STATUS.md` saying the fresh record
  "is not byte-identical to the committed 541191" — true when written, stale
  the moment either record is recomputed, and recomputing them is exactly what
  a repair does.  Both now say "the committed record" and send the reader to
  the re-pasted battery transcript, which is re-run rather than re-typed.
  Reason: the same defect one paragraph up, and writing a number into a
  sentence that no run regenerates is how it recurs.

* **Receipts recomputed, never patched.**  `receipts/side_free.json` and
  `receipts/comparison.json` are regenerated from the repaired computation, and
  `COMPARISON.md` is re-rendered from the latter.  No committed value was
  edited by hand.  The battery transcript in `STATUS.md` is re-pasted from a
  fresh run at this commit.
