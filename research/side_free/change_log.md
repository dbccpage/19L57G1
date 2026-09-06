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
  *Recorded later, in the pattern the other frozen-file corrections here
  already follow:* the sentence originates in the frozen `DESIGN.md` §7, whose
  paragraph on the one value-set change of the whole deletion says the receipt
  shows the two pinned further-mark points "carrying the same class key and
  standing as the two members of one retained class" with no reading named.
  That entry repaired the three editable copies and did not say where the
  unscoped copy came from, which is the half the other four corrections record.
  The frozen file is not edited; the scope lives in the three places this entry
  repaired, and in the R36 and R38 notes it added.

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

## 2026-09-05 — third repair pass: the registered step, and a mislabelled count

* **This tree's registered CI step could not pass.**  It asserts an exact test
  count so that an enumeration finding nothing cannot pass as a green suite,
  and the literal stood at 321 while the suite ran 323: the value was right
  when the step was written and was not moved when the second repair pass added
  two tests.  The failure is loud rather than silent — the step aborts on the
  grep and the three checks after it never run — but it reddens this tree's
  only gate in CI on a defect that is not in the code, which is the same thing
  the entry above repaired for the receipt comparison.  The count is corrected,
  and the mechanism that let it drift is closed rather than only the value:
  `tests/test_registration.py` parses the pinned number out of the workflow —
  from this tree's own step, selected by its working directory, since sibling
  steps carry the same guard with their own counts — and requires it to equal
  the count this suite discovers, failing in both directions and naming both
  numbers.  The guard is published as a row of `MANUAL.md`'s gate table, has an
  injection row (I18), and the obligation to bump the pin when the suite
  changes size is written beside the other deliberate acts in that file.  The
  literal itself stays: a wildcard would let an empty enumeration through,
  which is the whole point of the line.  Reason: a gate nobody can pass teaches
  a reader to ignore the job, and a pin held from one side only drifts again.

* **`STATUS.md` said one route-table cell was "the whole of what the admitted
  primitive bought", and its own table two paragraphs up said two.**  The
  receipt agrees with the table: `routes_bought_count` is 2, and the second
  route, `withdraw_reflection`, is dropped by the mechanical deletion criterion
  before the cross-world join, so it can disagree in no cell at all.  The
  sentence therefore dropped the more interesting half — the route the
  primitive bought that has no side-free counterpart whatever — while reading
  as a summary of everything.  It is narrowed to what the route table actually
  says.  The same unscored aside stands in the frozen `PREDICTIONS.md` beside
  P4, whose scored clauses are the two deltas, the decided value and
  `route_disagreements`; the frozen file is not edited and a fourth scoring
  note records that nothing in the machine holds that sentence.  Reason: a
  claim the computation does not bear must not be copied into a live document.

* **The count reported as the corollary's non-vacuity measured something
  else.**  Gate G5 published `non_vacuity_cells = 228`, computed as the cells
  where the side-typed world separates the two retained marks and the forgotten
  one does not.  At every one of those cells the corollary's antecedent —
  side-free separation — FAILS, so the implication asserts nothing there and
  the count cannot show it is non-empty; and G5's message on a zero would have
  said "the corollary is vacuous", which is the opposite of what a zero there
  means.  The corollary is non-vacuous, at **800** of the 1280 cells of two or
  more marks, and that number was computed by nothing.  Both are now reported
  under their own names — `corollary_antecedent_cells` and
  `converse_failure_cells` — and G5 carries one message for each, so a failure
  names which of the two it caught.  The 228 is unchanged, and what it measures
  is worth its own line: forgetting really does lose separations, so the
  converse of the corollary fails.  The frozen `DESIGN.md` §11 declares the
  check under the same mislabel and `PREDICTIONS.md` P17 repeats it; neither is
  edited, P17's clause follows the frozen file's own DESCRIPTION to the renamed
  field, both counts are unchanged and it remains a HIT, and the correction is
  recorded as a fifth scoring note in `STATUS.md` and beside
  SF-FORGETFUL-LEMMA in the ledger.  Injection I6 was re-run against the
  repaired gate: its third diagnostic line is now the converse line rather than
  the vacuity line, because the injection drives the converse count to zero
  while the corollary's antecedent still holds at 1040 cells, and the row
  records what was observed.  Reason: the substantive claim was true and the
  evidence cited for it measured a different property, which is the kind of
  agreement that survives review by accident.

* **Source isolation was published as a gate and reached by no census.**  Its
  probes exist — the scan is run over an assembled example of each barred kind
  and required to name it — but neither permanent-probe paragraph in
  `MANUAL.md` mentioned them, so a reader auditing gate by gate would conclude
  the row was unproved.  That is the defect the entry above repaired for C2, C3
  and C4, under a principle stated generally, and this row was missed by it.
  The paragraph now names the diagnostics.  Reason: a census of what has been
  proved must reach every gate the table publishes.

* **Receipts recomputed, never patched.**  `receipts/side_free.json` moves from
  542219 to 542418 bytes, the two renamed fields and the added count being the
  whole of the difference; it is byte-identical on a second regeneration.
  `receipts/comparison.json` and `COMPARISON.md` are re-rendered and come back
  unchanged, since no value they carry moved.  The battery transcript in
  `STATUS.md` is re-pasted from a fresh run at this commit.

## 2026-09-05 — fourth repair pass: five carried findings

* **The endowment ledger was reported as computed and is not, at two cells.**
  `DESIGN.md` §1 files every endowment row under deterministic computation and
  §8 says every row is computed by the same code in each column; the record's
  own summary called the block a computed report.  In fact the whole
  `declarations_at_genesis` row is three prose lists, one per column, and the
  CONTROL cell of `coordinates the genesis declaration fixes` is a typed zero
  beside two computed reading cells.  This is the guard `DESIGN.md` §12 names
  against the hazard of a control crippled by starting with less, so a
  declaration inside it reading as a measurement is the worst place for one.
  Every row now carries a `declared_columns` field, total over the ledger, the
  two rows with a declared column are listed under `rows_with_a_declared_column`
  and each carries its reason, and the summary sentence says which cells the
  same code computed — the instrument `comparison.py` already uses to keep a
  `Declared` cell apart from a `Computed` one.  The frozen file is not edited:
  the correction is a sixth scoring note in `STATUS.md`, beside P22, whose one
  declared cell of twelve is no longer counted as content, and beside
  SF-FAIRNESS-SIGN in the ledger.  Reason: a fairness report whose declarations
  are indistinguishable from its measurements cannot do the job it is named for.

* **`STATUS.md` said the ledger names AND prices every mismatching row.**  Six
  rows mismatch, one carries `price_if_bought`, and the prose explains two.  The
  claim originates in the frozen `DESIGN.md` §8 — "named and priced, not
  smoothed" — and had been copied forward into a live document, which is the
  defect the entry of 2026-09-05 above records for P4.  Rather than soften the
  sentence alone, the record is made to bear it: the priced and the unpriced
  mismatching rows are reported as two computed lists whose union is the six and
  whose intersection is empty, so a reader can check the claim instead of taking
  it.  The `STATUS.md` sentence and the ledger's own summary now say only that.
  Reason: a claim copied from a frozen file is still this tree's claim once a
  live document repeats it.

* **R40's two boundary cells are computed here and were presented as pinned.**
  Every other row's boundary cell resolves through the pin and is held by gate
  C1's totality count; R40's two are minima of the restricted second measure,
  which no pinned path carries, so they are computed on this tree's own mirror
  and read out of this tree's record.  `STATUS.md` and the ledger's SF-NO-HAND-TYPED-BOUNDARY-NUMBER both disclose
  this and the rendered price list disclosed it nowhere, while R40 is counted
  among the items where the control reaches the unnamed reading's value at its
  price.  The row now carries a note saying the cells are
  mirror minima, that the totality gate does not reach them and never counted
  them, and that what holds them instead is the per-point data join
  `second_measures.data_join_against_the_pin`.  No value moves and no count
  moves.  Reason: a value produced locally and shown as if it came from the
  authoritative source is the failure this whole tree is built to avoid.

* **The same defect in the table of which minima read a side.**  Its first
  column was headed `world` and read "the pinned world" for the pinned rows,
  while the behavioural verdict beside it is computed on this tree's mirror over
  that mirror's route-census domain — the pinned world's kernel is not run here
  and no pinned path carries a placement verdict.  The header is now `whose
  minimum`, which is what the column actually says; the two criterion columns
  are headed with where each is evaluated; and the record carries a
  `where_each_criterion_is_evaluated` sentence that the document renders above
  the table.  Reason: as R40, and it is the same failure one table lower.

* **A frozen-file correction was recorded in three places and not in the
  fourth.**  The entry above on the collapse map's one-class justification
  repaired R47, the record's copy and the `Collapsed` resolver, and did not say
  where the unscoped sentence came from.  It comes from the frozen `DESIGN.md`
  §7.  That half is what the tree's other four frozen-file corrections record,
  and the entry now records it too.  Reason: the corrections are only a series
  if each one names the frozen text it corrects.

* **Receipts recomputed, never patched.**  `receipts/side_free.json` moves from
  542418 to 543976 bytes: the per-row `declared_columns` fields, the two price
  lists, the declared-cell census and its reasons, and the narrowed summary
  sentence.  `receipts/comparison.json` moves from 130322 to 131468 bytes and
  `COMPARISON.md` from 28385 to 29546, carrying R40's note and the
  minima-table disclosure.  Both come back byte-identical on a second
  regeneration.  No decided value, no count and no verdict moves.  The suite
  stays at 325 tests: the registered CI step pins that number and this pass may
  not touch the workflow, so the new assertions were added to the endowment
  test already present rather than as a test of their own, and the reason is
  written in its docstring.  The battery transcript in `STATUS.md` is re-pasted
  from a fresh run at this commit.

## 2026-09-05 — fifth repair pass: the counts the fourth pass typed by hand

The pass above closed five findings and introduced three, and all three were
one defect: a count typed into prose by hand that the record contradicts.
Each is repaired below by naming the field that carries the count, and by
asserting the count where this tree can assert it, so that a sentence cannot
go stale on its own.

* **[A] Two sentences of one scoring note disagreed about P22's cells.**  The
  first said the frozen classification holds of "nine of P22's twelve cells"
  and is false of two; thirteen lines later the same note said one cell of
  twelve is a declaration and "the other eleven are computed".  Nine plus two
  is eleven.  Neither figure was the population: P22 carries twelve CLAUSES
  over NINE ledger cells, because the three cells of the renaming row are
  objects and two clauses read each of them.  The population is now computed
  for every prediction, at `ledger_cells` beside its score, and split by the
  ledger's own declared-cell census into `declared` and `computed`.  The note
  states the split once, and `tests/test_predictions.py` holds the twelve, the
  nine, the one and the eight, together with the totality of the split.
  Reason: a clause is not a cell, and a note that counts one under the other's
  name cannot be checked by reading it.

* **[B] The same note was headed with a ROW count under the word cells.**  It
  read "Two cells of the endowment ledger are DECLARED", while the record
  flags four cells and the paragraph under the heading described three cells
  in one row and one in another.  Two is the number of rows.  The heading now
  names `declared_cells` and says four, across the two rows of
  `rows_with_a_declared_column`; both censuses are asserted with their
  partition, declared plus computed equalling rows times columns with an empty
  intersection, so neither number can drift alone.  Reason: as [A], and in the
  sentence a reader quotes instead of re-deriving.

* **[C] A pre-existing error was corrected silently inside a repair announced
  for something else.**  The sentence listing what the machine reports beside
  the answer said the ledger names every mismatching row "including the two
  that are UNMATCHABLE".  `named_mismatches` carries two entries and exactly
  ONE of them says UNMATCHABLE, so the plural was wrong.  The pass above
  rewrote that sentence for a different finding and made it singular in
  passing, recording the change nowhere.  The singular STANDS, being what the
  record bears; this entry is the record of it, and the count is now asserted
  in the ledger test so the singular is held rather than believed.  Reason: a
  correction made inside another correction is invisible to a reader diffing
  for the finding that was announced.

* **[D] The declared-cell flag stopped before the place the value is read.**
  `declared_columns` was written onto `endowment_ledger.rows`, and the
  `by_row` projection, which enumerated three columns, dropped it — while
  `comparison.py` reads endowment cells only through `by_row`.  So R03's price
  control cell, which is one of the four declared cells, was still rendered in
  the price list as a measurement.  The projection now carries every field of
  the row it keys, total by construction rather than by enumeration, so the
  next field cannot be lost the same way.  `comparison.py` gained the mirror
  of its pinned-side check: every row and every price block reports
  `columns_reading_a_declared_ledger_cell`, the rows that read one are
  censused in `bought_table`, and `COMPARISON.md` renders that census beside
  the two declared-field censuses already there.  R03's price control column
  is the one entry.  Reason: a flag that does not reach the consumer has not
  been carried.

* **[E] The claim ledger asserted a classification no field carried.**  It
  said the declared endowment cells "are DEFINITION-level and are not counted
  as content".  This tree's own definition-level test — declared on BOTH
  sides — is true of `declarations_at_genesis`, all three of whose columns are
  declared, and FALSE of `coordinates the genesis declaration fixes`, whose
  one declared cell stands beside two computed ones.  The flag is computed per
  row now, reported as `definition_level` and `definition_level_rows`, and the
  ledger says what those bear.  The "not counted as content" half is
  WITHDRAWN: the only tally criterion this tree computes is the FORCED label
  on a prediction, P22 does not carry it, and nothing subtracts these cells
  from any count.  Reason: a classification asserted in prose beside a
  computed flag that contradicts it is worse than no classification.

* **The two further reviewer notes, fixed because both fixes are computed.**
  The minima table's first column was relabelled "whose minimum" in the pass
  above while the record still keyed it `world`; the key is renamed to match,
  which asserts nothing that was not already asserted.  R40's note claimed to
  be "the ONLY row whose two boundary cells are not read from a pinned path".
  That is true, and it is now decided rather than typed: `boundary_source_census`
  puts every row's two boundary columns through one rule — a pinned path, or
  the length or the collapse of one — and names the rows that fail it.  The
  note names the field, the census names R40, and a test holds both.

* **Receipts recomputed, never patched.**  `receipts/side_free.json` moves
  from 543976 to 550107 bytes: the ledger's column list, its declared-cell and
  computed-cell censuses, the per-row `definition_level` flag, the projection
  that no longer drops a field, and the per-prediction `ledger_cells` block.
  `receipts/comparison.json` moves from 131468 to 140158 bytes and
  `COMPARISON.md` from 29546 to 30238, carrying the declared-cell flags, the
  boundary-source census, the renamed minima key and R40's reworded note.
  Both come back byte-identical on a second regeneration.  No decided value,
  no verdict and no computed count moves.  The suite moves from 325 tests to
  331, and the literal the registered CI step pins moves with it in this
  commit; that one literal in that one step is this pass's only change outside
  `research/side_free/`.  The battery transcript in `STATUS.md` is re-pasted
  from a fresh run at this commit.

## Guard repair

Adopted the unfinished numerical prose guard and tightened its claim
selectors. A changed quantity is now read under the same binding as the
original quantity; the selector cannot depend on the value it is checking.
The ledger's declared-cell sentence now matches its cell population, and the
corollary-domain total is computed from the declared census. The retained
generic determiner exemptions and quoted-source exemption remain explicit.

A reachable pin mismatch now makes the pin gate fail and the decision VOID.
The Lean audit recognizes primed names and theorem attributes, and compares
the requested report population against the fresh parsed reports. Permanent
probes cover each repaired failure and recovery without editing any receipt.

Removed the status transcript's claimed coverage percentages and the guard's
literal full-percentage source. The coverage gate supplies the independently
computed fresh measurements. The test registration and status file counts
move with the measured suite. The frozen design, frozen predictions and
vendored boundary inputs are unchanged; this repair does not rebind the pin.

## Boundary price-column census repair

The earlier statement that R40 was the only row with boundary cells outside
the pinned-path population is WITHDRAWN. The census inspected value columns
and omitted stated-price columns: R03's boundary prices read the control
record's endowment ledger. The census now includes those slots, names output
paths and roles, and reports R03's price cells alongside R40's value cells.

The census test independently gathers rendered source metadata. A permanent
probe removes R03's price cells, requires a failure naming the omitted path,
and checks recovery without rewriting any receipt. The comparison record and
its document are regenerated; the ledger and status state the corrected
provenance boundary. The registered test count follows the added probe.
No comparison value, price, minimum, verdict, frozen input or source pin is
changed by this repair.

## Landed-source repin

The source now binds its actual merge on main, with the dedicated source
freeze preserved. Vendored receipts and their extracted and declared values
are byte-identical. Later source definitions expand the deletion population;
each added name is classified as absent from the control, with its source
dependency stated. This does not widen the control's declared challenge scope.

The emitted source label now comes from the manifest, and the separate pin
metadata must agree. Missing or differing source fails required verification;
the historical CI downgrade and conditional receipt-diff bypass are retired.
The frozen conditional diagnostic field remains, so record-format dependence
outside validated clones is still named. Frozen design and predictions are
unchanged. The permanent probes exercise source and provenance failures with
recovery, without regenerating under an injected defect.
