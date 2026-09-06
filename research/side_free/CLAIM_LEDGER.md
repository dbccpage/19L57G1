# Claim ledger: the side-free control

Every claim this tree makes, with its status, what it rests on, what would
falsify it, and what survives it unanswered.  Identifiers are this tree's own
(`SF-*`); no identifier of any other tree appears here.

Statuses are drawn from the declared twelve: METATHEORY APPARATUS, SUPPLIED
DATUM, IMPOSED CHALLENGE, ADMITTED PRIMITIVE, DERIVED DEFINITION, PROVED
THEOREM, DETERMINISTIC COMPUTATION, COUNTERMODEL, OPTIONAL REALIZATION,
CONJECTURE, OPEN OBSTRUCTION, REFUTED CLAIM.  A claim that is true by
unfolding a declaration is additionally marked **DEFINITION-level** and is
never counted as content.

---

### SF-CARRIER-NOTHING-ADMITTED

* **Statement.**  This tree admits no primitive.  Its carrier is a regime with
  one variable field, the labels of the admitted marks in admission order.
* **Status.**  DERIVED DEFINITION.
* **Depends on.**  Nothing.
* **Assumes.**  That the pinned carrier's placement index space and its mark
  index space are the same set, which the pinned validator enforced by
  refusing any regime whose two tuples differ in length.
* **Python evidence.**  `code/sidefree/model.py`; `tests/test_model.py`.
* **Lean.**  `SideFree.Regime`, `SideFree.genesis`.
* **Axiom report.**  `SideFree.genesis_size` — no axioms.
* **Falsifier.**  A second variable field, or any state change outside an
  admission event.
* **Surviving boundary.**  None.

### SF-SUPPLY-INERT

* **Statement.**  The external presentation event changes no admitted state.
* **Status.**  PROVED THEOREM.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  Nothing.
* **Python evidence.**  `tests/test_model.py::Events::test_supply_changes_no_state`.
* **Lean.**  `SideFree.supply_no_op`, `SideFree.replay_supply_inert`,
  `SideFree.supply_is_not_an_admission`.
* **Axiom report.**  All three: no axioms.
* **Falsifier.**  A regime that differs after a presentation event.
* **Surviving boundary.**  None.

### SF-ADMISSION-ONLY

* **Statement.**  Admitted state changes only through an admission event, and
  every certified regime is the replay of an explicit history from genesis.
* **Status.**  PROVED THEOREM (Lean) and DETERMINISTIC COMPUTATION (every row).
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  The Lean carrier is total and carries no refusals; every
  refusal of the Python carrier is a declaration about well-formed histories.
  This is stated in the Lean file rather than left for a reader to find.
* **Python evidence.**  Every row's `certified` and `replays_from_genesis`
  fields; `tests/test_control.py::Enumerator::test_every_row_replays_from_genesis_and_agrees_with_its_carrier`.
* **Lean.**  `SideFree.step_changes_only_by_admission`,
  `SideFree.replay_deterministic`, `SideFree.replay_append`,
  `SideFree.retained_replays_from_genesis`,
  `SideFree.retainedPlus_replays_from_genesis`.
* **Axiom report.**  All five: no axioms.
* **Falsifier.**  A row whose regime is not its history's replay.
* **Surviving boundary.**  None.
* **Correction, recorded.**  `SideFree.replay_deterministic` previously stated
  `replay base h = replay base h`.  That is reflexivity of an arbitrary
  expression: it would elaborate against any definition whatever, so the
  PROVED THEOREM status it was cited for was carried by its doc line and not
  by its statement.  It is **restated** as the claim that has content — replay
  is a function of the base and the ADMISSION subsequence alone, so deleting
  every presentation event from a history leaves the replay unchanged, and two
  histories with the same admissions in the same order reach the same regime.
  Its name, its axiom report and the report count are unchanged.  The other
  four theorems cited above always carried content; `DESIGN.md` §1's "that
  replay is deterministic" is true of the restated theorem and was not true of
  the old one.

### SF-REQUIREMENT-INHERITED

* **Statement.**  The requirement and its second reading are the pinned texts
  with one declared phrase deleted each, byte for byte, and neither control
  string names any word the deletion removes.
* **Status.**  IMPOSED CHALLENGE.
* **Depends on.**  The vendored pin (SF-PIN).
* **Assumes.**  That deleting the tower index leaves the same requirement.
  This is a translation claim, and G4 is what checks it mechanically rather
  than by assertion.
* **Python evidence.**  Gate G2; `tests/test_space.py::Requirement`;
  the injection I3 in `MANUAL.md`.
* **Lean.**  None; the requirement is a text, not a theorem.
* **Axiom report.**  Not applicable.
* **Falsifier.**  Either deletion failing byte for byte, or a deleted word
  appearing in a control string.
* **Surviving boundary.**  The premise that a candidate's permitted renamings
  are closed under composition and inverse is inherited as OPEN — SF-OPEN-C.

### SF-TRANSLATION-REPLAYS

* **Statement.**  This tree's own verdict function, applied to the pinned
  world's own recorded automorphism sets, reproduces the pinned world's own
  recorded answers on all fourteen rows the minimum ranges over.
* **Status.**  DETERMINISTIC COMPUTATION.  **This is the load-bearing tie**
  between the two worlds, and it uses no re-declaration of anything.
* **Depends on.**  SF-PIN.
* **Assumes.**  Nothing beyond the pinned bytes.
* **Python evidence.**  Gate G4, 14 rows, 14 agreements;
  `tests/test_control.py::Gates`; the mutation probe in the same class.
* **Lean.**  None.
* **Axiom report.**  Not applicable.
* **Falsifier.**  Any disagreement — which VOIDS the run.
* **Surviving boundary.**  G4 is total over what the minimum is computed FROM,
  not over all 48 points per reading; a defect in a bundle row's recorded
  verdict is invisible to it.

### SF-FORGETFUL-LEMMA

* **Statement.**  Whatever renaming carries a side-typed regime — or its
  exchange — onto itself, the same renaming carries the forgotten regime onto
  itself.  Corollary: side-free separation implies side-typed separation.
* **Status.**  PROVED THEOREM (Lean, unbounded) with a bounded Python census
  as its cross-check.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED, SF-MIRROR.
* **Assumes.**  In Lean, that a renaming acts by reading marks at indices; the
  proof needs no permutation property, which is strictly stronger than needed.
* **Python evidence.**  Gate G5: 1344 cells, 2140 automorphisms checked, 0
  violations, 0 corollary violations; of the 1280 cells of two or more marks,
  **800** where the corollary's antecedent holds and **228** where the
  side-typed world separates and the forgotten one does not;
  `tests/test_mirror.py::Forgetting`; injection I6 in `MANUAL.md`.
* **Lean.**  `SideFree.forgetful_lemma_keeping_labels`,
  `SideFree.forgetful_lemma_forgetting_labels`,
  `SideFree.free_separation_implies_sided_separation`,
  `SideFree.free_separation_implies_sided_separation_forgetting_labels`,
  `SideFree.forget_rename`, `SideFree.forget_reflect`,
  `SideFree.reorder_map`, `SideFree.reorder_length_congr`.
* **Axiom report.**  Within `{propext, Quot.sound}`; the two label-forgetting
  statements and `reorder_length_congr` use both, the rest `propext` alone.
* **Falsifier.**  Any violating cell with no injection live.
* **Surviving boundary.**  The lemma is about the two carriers declared here.
  That the mirror is the pinned carrier is not claimed; see SF-MIRROR.
* **Correction, recorded not edited away.**  The 228 was reported as the
  corollary's non-vacuity, and it is not: the corollary says side-free
  separation implies side-typed separation, so at each of those cells its
  antecedent FAILS and it asserts nothing.  The count that shows the
  implication is not empty is the 800, which nothing reported until this
  repair.  The corollary is non-vacuous either way — that is what the 800 now
  establishes — but the number cited for it measured the converse's failure
  instead, which is worth reporting on its own and under its own name.  Both
  counts are now computed and reported, and gate G5 names whichever of the two
  it caught.  `DESIGN.md` §11 and `PREDICTIONS.md` P17 carry the mislabel and
  are frozen; the correction lives here and in `STATUS.md`.

### SF-FAIRNESS-SIGN

* **Statement.**  The instrument cannot return a negative difference: the
  pinned minimum is at most the side-free minimum, so a tie is the strongest
  statement available against the admitted primitive.
* **Status.**  PROVED THEOREM (the corollary of SF-FORGETFUL-LEMMA), together
  with the DETERMINISTIC COMPUTATION that every side-free candidate has a
  side-typed counterpart at the same capability count.
* **Depends on.**  SF-FORGETFUL-LEMMA, SF-CAPABILITY-TEXTS.
* **Assumes.**  The counterpart map is the collapse map declared in
  `pinned/BOUNDARY_PIN.json`.
* **Python evidence.**  The route table's four joined rows; gate G5's
  `sign_consequence` field.
* **Lean.**  The two `free_separation_implies_sided_separation` theorems.
* **Falsifier.**  A negative `delta_vs_unnamed`.
* **Surviving boundary.**  None within the declared space.
* **Correction, recorded not edited away.**  The other guard against an unfair
  comparison — the endowment ledger, which `DESIGN.md` §12 names against the
  hazard of a control crippled by starting with less — was reported as
  computed throughout, and four of its cells are not.  The whole
  `declarations_at_genesis` row is three prose lists, one per column, and the
  CONTROL cell of `coordinates the genesis declaration fixes` is a typed zero;
  nothing in either carrier enumerates its own genesis declaration, and this
  control has no reading level to declare at.  Every row now carries a
  `declared_columns` field naming which of its columns are declarations, the
  two rows with one are listed under `rows_with_a_declared_column`, and each
  carries its reason — the instrument `comparison.py` uses to keep `Declared`
  apart from `Computed`, applied here for the same reason.  Whether a row is
  DEFINITION-level is computed and not asserted: `definition_level` is true of
  a row declared in every column, which here is `declarations_at_genesis`
  alone, and false of `coordinates the genesis declaration fixes`, whose one
  declared cell stands beside two computed ones — so that row is a
  declaration compared against measurements, which is not the same thing and
  the record no longer calls it so.  Neither row is struck from a tally by any
  computation of this tree: the only tally criterion here is the FORCED label
  on a prediction, P22 does not carry it, and its hit is counted as it stands
  with this correction qualifying it.  `DESIGN.md` §1 classifies
  every endowment row as deterministic computation and §8 says every row is
  computed by the same code in each column; both are frozen, so the correction
  lives here and in `STATUS.md`.  The ledger's own summary said mismatching
  rows are "NAMED and priced": one of the six carries a price, so the record
  now reports the priced and the unpriced rows as two lists whose union is the
  six, and the summary says only what those lists bear.

### SF-CAPABILITY-TEXTS

* **Statement.**  The three surviving coordinates carry their pinned
  capability sentences byte-identical, their names are string-identical, and
  the partition into surviving and deleted is the mechanical one: a coordinate
  transfers exactly when its pinned sentence contains no whole word *side* or
  *sides*.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-PIN.
* **Assumes.**  That the mechanical criterion is the right criterion.  It is
  declared, not derived; what is checked is that it partitions the pinned five
  with no borderline case and that its partition equals the implemented one.
* **Python evidence.**  Gate G3; `tests/test_space.py::DeletionCriterion`;
  injections I4, I5, I10.
* **Lean.**  None.
* **Falsifier.**  One altered character, one renamed coordinate, or a widened
  criterion — each of which was injected and each of which fired.
* **Surviving boundary.**  Whether the criterion is the right one is a
  judgement about words, not a computation.

### SF-MINIMUM

* **Statement.**  Within the three declared coordinates, at the pinned
  requirement and prices, at the retained two-mark configuration, under
  `mu1`: the side-free minimum is **1**, attained by exactly **one**
  non-isomorphic class, `{withdraw_mark_permutations}`.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED, SF-REQUIREMENT-INHERITED,
  SF-CAPABILITY-TEXTS.
* **Assumes.**  The declared exhaustiveness scope, inherited from the pinned
  world and widened by one clause: no augmentation admitting a new per-mark
  datum is enumerated.
* **Python evidence.**  `receipts/side_free.json`, `decided.side_free_minimum`
  and `decided.side_free_classes`; `control.minima_by_mu1`.
* **Lean.**  `SideFree.base_exchange_is_an_automorphism`,
  `SideFree.exchange_moves_zero_to_one`,
  `SideFree.keep_labels_exchange_is_an_automorphism`,
  `SideFree.extra_mark_exchange_is_an_automorphism`,
  `SideFree.withdrawal_does_not_move_zero_to_one` — the four rows, at the
  retained regime, in Lean.
* **Axiom report.**  `propext` for each of the five.
* **Falsifier.**  Any other one-step candidate satisfying, or that one
  failing, or a class count above 1.
* **Surviving boundary.**  The minimum is attained **by unfolding** — see
  SF-DEFINITION-LEVEL — and the scope is these three coordinates and no wider.

### SF-DEFINITION-LEVEL

* **Statement.**  `withdraw_mark_permutations` satisfies the requirement by
  unfolding the declaration: with no permitted renaming that moves an index,
  no renaming carries one mark to another.
* **Status.**  DERIVED DEFINITION, marked **DEFINITION-level**, never counted
  as content.
* **Depends on.**  SF-MINIMUM.
* **Assumes.**  Nothing.
* **Python evidence.**  The COMPUTED field
  `no_permitted_renaming_moves_an_index`, reported beside the verdict rather
  than asserted; the route census, 4 of 4.
* **Lean.**  `SideFree.withdrawal_moves_no_index`,
  `SideFree.exchange_is_not_the_identity` (which shows the withdrawal is a
  real restriction and not a vacuous one).
* **Falsifier.**  The flag computing false while the row satisfies.
* **Surviving boundary.**  Whether the requirement should have been declared
  so as to exclude such a route is SF-OPEN-D.

### SF-DIFFERENCE

* **Statement.**  `delta_vs_unnamed = 0` and `delta_vs_named = +1`.  The
  admitted primitive reduced the price of the required separation by ZERO
  under the unnamed reading and by ONE under the named reading.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-MINIMUM, SF-TRANSLATION-REPLAYS, SF-FAIRNESS-SIGN,
  SF-MIRROR.
* **Assumes.**  The cross-world join by string equality on the coordinate
  names, and the declared collapse map for the two pinned further-mark points.
* **Python evidence.**  `decided.delta_vs_unnamed`, `decided.delta_vs_named`,
  `decided.what_the_admitted_primitive_bought = NOTHING_IN_COST`.
* **Lean.**  None; the difference is a computation over two enumerations.
* **Falsifier.**  Either delta differing; a disagreeing route table cell other
  than `extra_mark`.
* **Surviving boundary.**  Scoped to these three coordinates, this
  requirement, this configuration and this measure.  It is **not** the claim
  that the admitted primitive bought nothing — see SF-TERMINAL.

### SF-ROUTES

* **Statement.**  What the admitted primitive bought under the unnamed reading
  is **two additional routes at the same price**: `withdraw_reflection` and
  `extra_mark`, both mediated by the sides.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-DIFFERENCE.
* **Assumes.**  The collapse map.
* **Python evidence.**  `decided.routes_the_admitted_primitive_bought`,
  `decided.routes_bought_count`.
* **Falsifier.**  Any other member set.
* **Surviving boundary.**  Routes and price are separate columns and are never
  summed.  Two tests hold that, one per record: over `receipts/side_free.json`
  the only fields whose names carry both words are the two copies of the
  declaration that says so, and the set is pinned exactly rather than excluded
  by hand; over `receipts/comparison.json` there is no such field at all.  An
  earlier version of this line said a test asserted that no field of the
  side-free receipt combined them — the walk existed only over the comparison
  record, and the sentence is narrowed to what each test covers.

### SF-REFUTED-DEPENDENCE

* **Statement.**  The pinned clause that *every* separation result of that
  rung requires the admitted primitive is **REFUTED** — within the scope of
  this declared carrier, these three coordinates and this eight-point
  enumeration, and nowhere wider.
* **Status.**  REFUTED CLAIM.
* **Depends on.**  SF-MINIMUM, SF-CAPABILITY-TEXTS.
* **Assumes.**  That `withdraw_mark_permutations` is one of that rung's
  separation results, which the pinned receipt shows by retaining it as one of
  its three tied minima.
* **Python evidence.**  The control's `withdraw_mark_permutations` row, which
  is formulated after removing the admitted primitive, costs the same, and
  satisfies the same requirement; `withdrawal_port.same_cost`.
* **Falsifier.**  That coordinate failing side-free, or costing more.
* **Surviving boundary.**  The refutation is of one clause at one rung.  The
  clause's other conjuncts — the side exchange, the two side mark properties,
  the counterfactual square — are untouched, and this tree does not price
  them.

### SF-MIRROR

* **Statement.**  The mirror is this tree's own re-declaration of a side-typed
  carrier, used only as the domain of the lemma and the censuses, and it
  reproduces the pinned vector on all 48 rows per reading.
* **Status.**  COUNTERMODEL — specifically a countermodel-domain object.
* **Depends on.**  SF-PIN.
* **Assumes.**  Nothing; a divergence VOIDS the run rather than adjusting it.
* **Python evidence.**  Gate G6, 96 rows compared;
  `tests/test_mirror.py::MirrorAgainstThePin`.
* **Falsifier.**  Any divergence on any row, minimum or class.
* **Surviving boundary.**  **It is never claimed to be the pinned carrier.**
  The load-bearing tie is SF-TRANSLATION-REPLAYS, which uses no
  re-declaration.

### SF-PIN

* **Statement.**  `pinned/boundary_challenge3.json` is the pinned receipt's
  bytes: sha256 `e4904075aaa07dd05a2f9d0cba313e77b6eb965a44efecb5cff51864f70a64ab`,
  git blob `dbb4cce3cdd49d15d0784c2a73bf7afeab9de7a0`, 220518 bytes, no CR,
  committed `-text`.
* **Status.**  METATHEORY APPARATUS.
* **Depends on.**  Nothing; the three digests need no git.
* **Assumes.**  For the fourth, conditional check: that the pinned commit is
  reachable.
* **Python evidence.**  Gate G1; `verify_pins.py`; injections I1 and I14.
* **Falsifier.**  Any digest, the byte count, a CR byte, or a blob at the
  pinned commit differing.
* **Surviving boundary.** The pinned commit has landed. The required verifier
  now fails on unavailable or differing source, and CI compares fresh receipt
  bytes unconditionally. The record's conditional field remains as frozen;
  a clone without the required source is not a validated execution.

### SF-OBSERVATION-INERT

* **Statement.**  The one positive judgment form, `Admitted`, separates the
  two retained marks at no cell of the control's route census.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  That `Admitted` is the honest residue of the pinned side
  judgment, which the pinned source bears out: that judgment is literally the
  conjunction of "the mark is admitted" and a placement test.
* **Python evidence.**  `observation_grammar.inert`;
  `tests/test_space.py::MarkProperties`.
* **Lean.**  `SideFree.no_judgment_at_genesis`, `SideFree.retained_judgments`.
* **Falsifier.**  Any census cell at which it separates.
* **Surviving boundary.**  Inertness is over the declared census, not over
  every conceivable regime.

### SF-SUBJECT-REFUSED

* **Statement.**  Under the pinned shared identity policy the control retains
  ONE mark, so the requirement has no subject and the retained-mark check
  raises by name.  This is a refusal of the subject, never a false and never a
  satisfied requirement.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  Occurrence identity is inherited already paid, exactly as the
  pinned world pays it one rung earlier.
* **Python evidence.**  `identity_policies.shared_policy`;
  `tests/test_control.py::Policies`.
* **Lean.**  `SideFree.shared_policy_retains_one_mark`.
* **Axiom report.**  No axioms.
* **Falsifier.**  Two marks under the shared policy, or a `false` reported
  where a refusal is due.
* **Surviving boundary.**  None.

### SF-REMOVED-REFUSAL

* **Statement.**  The pinned refusal of an admission that would move a mark to
  the other side is REMOVED, not absorbed: it has no side-free statement, and
  what is left in its place is exactly a no-op with nothing hidden inside it.
* **Status.**  METATHEORY APPARATUS (a recorded deletion).
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Python evidence.**  `identity_policies.removed_refusal` and its computed
  consequence; `DELETED.md`.
* **Falsifier.**  The refusal firing, or the no-op changing state.
* **Surviving boundary.**  None.

### SF-DELETION-TOTAL

* **Statement.**  The deletion register's population is the mechanical closure
  over the pinned source's own names — 119 entries, 83 deleted and 36 narrowed
  — no deleted name survives in the side-free modules, and no narrowed name is
  absent from them.
* **Status.**  DETERMINISTIC COMPUTATION, with one judgement inside it.
* **Depends on.**  SF-PIN.
* **Assumes.**  The declared word stems.  Whether they are the right stems is
  a judgement about words, not a computation, and is recorded as such.
* **Python evidence.**  `deletion_register.totality`;
  `tests/test_deletion.py`; injection I7. The population check requires the
  landed pinned source and fails when it is unavailable.
* **Falsifier.**  A surviving deleted name, an absent narrowed one, or a stem
  leak outside the six-name allowlist.
* **Surviving boundary.**  `mirror.py` and `control.py` are excluded from the
  scan **by declaration**, because both must be able to name the deleted
  structure in order to compare against it.

### SF-SECONDARY

* **Statement.**  Excluding every candidate that separates at every cell of
  its own world's route census, the control has NO satisfying candidate while
  the unnamed reading still has three at price one in two classes.  The answer
  flips.
* **Status.**  DETERMINISTIC COMPUTATION, declared in advance and **never
  deciding**.
* **Depends on.**  SF-MINIMUM, SF-DEFINITION-LEVEL.
* **Assumes.**  The route census domain declared in `DESIGN.md` §9.
* **Python evidence.**  `secondary.decided`; prediction P25.
* **Falsifier.**  The control retaining a satisfying candidate under the
  exclusion, or the unnamed reading losing one.
* **Surviving boundary.**  The primary counts the vacuous route, because
  excluding it in the control while it stands in the pinned world would itself
  be the rigging.  Both numbers are frozen precisely because the answer flips.

### SF-TERMINAL

* **Statement.**  The admitted primitive bought **no price that the admission
  order could not buy at the same price**, within the declared scope.
* **Status.**  DETERMINISTIC COMPUTATION, scoped.
* **Depends on.**  SF-DIFFERENCE, SF-DEFINITION-LEVEL, SF-SECONDARY.
* **Assumes.**  Nothing further.
* **Python evidence.**  `terminal.sentence`,
  `terminal.sentence_is_the_scoped_one`.
* **Falsifier.**  The unscoped sentence — "the admitted primitive bought
  nothing" — being written anywhere as this tree's result.
* **Surviving boundary.**  SF-OPEN-A: whether an order is itself a container.

### SF-PRICE-LIST

* **Statement.**  Over 47 compared items at the pinned rungs 0 to 3, the
  control reaches the unnamed reading's value at the unnamed reading's stated
  price in 26, differs in 19, and has no statement in one world in 2.
  Restricted to the items that are verdicts or prices, it reaches the same
  value at the same price in 9 and differs in 7.  Two of the 47 — R44 and R45 —
  read a field one world or the other DECLARES rather than computes, and R45 is
  declared on both sides, so its agreement is true by unfolding and is
  DEFINITION-level.  Setting both aside: same in 25, differs in 18, and
  restricted to verdicts and prices same in 8 and differs in 6.  Both tallies
  are computed and reported; neither is the curated one.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-PIN, SF-DIFFERENCE, SF-MINIMUM.
* **Assumes.**  The declared item taxonomy, which says what KIND of thing each
  item is and is checked total in both directions by gate C4.  It does not
  decide any row's bucket: the bucket is the computation's, by the rule that
  an item is in BOUGHT_NOTHING exactly when the control reaches the same value
  at the same stated price.
* **Python evidence.**  `receipts/comparison.json`, `rows` and `bought_table`;
  `verdict.counts` and `verdict.counts_without_the_declared_field_rows`;
  `tests/test_comparison.py`; gates C0 to C4; injections I15, I16, I17.
* **Lean.**  None; the price list is a computation over two receipt sets.
* **Falsifier.**  Any row whose difference is not what the two sources say, or
  a bucket membership that does not follow the stated rule.
* **Surviving boundary.**  Absence is in neither bucket.  Two items — the
  collapse of the two sides at genesis, and the refusal of an admission that
  would move a mark — have no side-free statement, and are evidence neither
  that the primitive bought something nor that it bought nothing.  And a row
  reading a declared field measures nothing: R44 compares a pinned declaration
  with a computed control list, and R45 compares two declarations.  An earlier
  version of this entry carried R45 in the headline as a computed sameness, its
  control cell being a typed-in string resolved as computed.

### SF-NO-HAND-TYPED-BOUNDARY-NUMBER

* **Statement.** Every pinned-path boundary value the comparison uses is read
  from a pinned receipt at a declared JSON path, is declared a second time in
  `pinned/BOUNDARY_PIN.json`, and the declaration is total in both directions:
  91 declared, 91 read, 91 checked. The boundary-source census separately names
  cells outside that population by output path and role. R03's boundary price
  cells read this tree's own endowment ledger. R40's boundary value columns
  are the minima of the restricted second measure, which the
  pinned receipts do not carry at any JSON path; they are computed on this
  tree's own mirror and are held instead by the per-point data join against the
  pin.  An earlier version of this line said *every* boundary value without
  an exception, then named only R40. Both claims are WITHDRAWN: gate C1
  records neither the price cells of R03 nor the value cells of R40.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-PIN.
* **Assumes.**  Nothing beyond the four pinned receipts' bytes.
* **Python evidence.**  Gate C1; `verify_pins.check_declared_values`;
  injections I15 and I16, each failing by name and recovering;
  `test_the_boundary_source_census_bears_r40s_claim` and
  `test_omitting_price_cells_from_the_census_fails_by_path_and_recovers`.
* **Falsifier.**  A boundary number in a source file of this tree; an
  undeclared value a row reads; a declared value no row reads.
* **Surviving boundary.**  Totality is not correctness.  A perfect pin of the
  wrong row set is still the wrong row set, and C1 cannot see that.  And the
  totality is over the values C1 can see: the resolver records a use only for a
  value read at a pinned path, so R03's boundary price cells and R40's
  mirror-computed boundary value cells are outside both directions of the
  count. R03 reads
  `endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes`
  from the generated control record and its endowment checks. What holds
  R40's cells is a different and weaker guarantee —
  `second_measures.data_join_against_the_pin`, which joins
  48 rows per reading against the pin and reports the mismatches — and it is
  named here rather than folded into the 91.

### SF-READS-A-SIDE

* **Statement.**  Two criteria decide which minima read a side, both computed.
  By NAME: the pinned capability sentence carries a whole word *side* or
  *sides*.  By BEHAVIOUR: the separation verdict is not constant across the
  placements of one label configuration in the candidate's own route-census
  domain.  They agree that `withdraw_mark_permutations` reads nothing and that
  `withdraw_reflection` reads a side, and disagree on `extra_mark_0`,
  `extra_mark_1` and the named reading's `base` — none of which names a side,
  and all three of which read the placement.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-MIRROR, SF-CAPABILITY-TEXTS.
* **Assumes.**  The route-census domain declared in `DESIGN.md` §9.
* **Python evidence.**  `minima_and_the_sides` and its
  `the_two_criteria_disagree_on` field; `tests/test_comparison.py`.
* **Falsifier.**  Either criterion returning a different partition.
* **Surviving boundary.**  The behaviour criterion is over the declared census
  domain, not over every conceivable configuration.

### SF-DEPENDENCE-READ

* **Statement.**  The pinned world's own dependence dictionary — 20 entries
  across its four rungs, hand written in its four challenge modules and filed
  by its own ledger as computed by nothing, its bytes held by a test against
  its own module constant and adjudicated by nothing — is READ here,
  classified mechanically by its sentences' own opening words with no entry
  left unclassified, and the one entry whose subject claims *every* separation
  result of its rung requires the admitted primitive is CONTRADICTED within
  the declared scope.
* **Correction, recorded.**  An earlier version of this statement said the
  dictionary was "hand written in its runner modules" and "read by no test".
  Both halves are **WITHDRAWN**.  The constant is defined in the four challenge
  modules, which the runners import; and a test of that tree asserts the
  receipt's copy equals that module constant, so its bytes are pinned.  What
  is exactly true is what the corrected wording now says: nothing COMPUTES the
  dictionary — its own ledger files it as a classification reported and not
  computed — and nothing ADJUDICATES it.  `DESIGN.md` is frozen and carries
  the looser wording, so this correction is recorded here and in `STATUS.md`
  rather than by editing it, as that file's own arithmetic error already is.
* **Status.**  DETERMINISTIC COMPUTATION with a DECLARED selector.
* **Depends on.**  SF-REFUTED-DEPENDENCE, SF-PRICE-LIST.
* **Assumes.**  That the selector — DEPENDENT entries whose subject carries the
  whole word *every* — picks the claim worth adjudicating.  That is a
  declaration about words; the evidence under it is computed, and the record
  says which is which in the same object.
* **Python evidence.**  `pinned_dependence_claims`, its
  `classification_is_total` field, and its `adjudication` block with the
  computed evidence; `tests/test_comparison.py`, including the negative that
  turns the verdict to NOT CONTRADICTED when the evidence is removed.
* **Falsifier.**  An unclassified entry; a second universal entry the record
  does not name; the evidence failing.
* **Surviving boundary.**  The other 19 entries are reproduced and classified,
  **not adjudicated**.  They are prose, and no computation here decides them.

### SF-COMPARISON-RECORD-IS-CLONE-INDEPENDENT

* **Statement.**  `receipts/comparison.json` is the same file in a clone that
  cannot reach the pinned commit: its rows are held by the declared sha256
  alone, and the reachability report is printed by the runner rather than
  written into the record.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-PIN.
* **Assumes.**  Nothing.
* **Python evidence.**
  `tests/test_comparison.py::TheRecord::test_the_record_is_the_same_file_in_a_clone_that_cannot_reach_the_pin`,
  which makes every `git show` fail and requires the rendering back byte for
  byte.
* **Falsifier.**  Any environment value reaching the record.
* **Surviving boundary.**  **The sibling record does NOT have this property**
  — see SF-OPEN-E.

---

## Open obstructions

### SF-OPEN-A — is the admission order a container?

What pays for separation in a world with no container is the admission order.
This control prices that route; it does not decide what kind of thing an order
is.  **OPEN OBSTRUCTION.**

### SF-OPEN-B — the price of re-purchasing a per-mark two-valued datum

Outside the pinned candidate space, therefore priced in neither world.
Allowing it would price a route the pinned world was never charged for either,
and it answers a different question: the PRICE of rebuilding the admitted
primitive, not the WORTH of having it free.  **OPEN OBSTRUCTION.**

### SF-OPEN-C — closure of the permitted renamings

The pinned premise that a candidate's permitted renamings are closed under
composition and inverse is inherited, stated, and checked by nothing.  It is
not treated as discharged by the renaming set having shrunk.
**OPEN OBSTRUCTION.**

### SF-OPEN-D — should the requirement have excluded a vacuous route?

The pinned tree retains a route that satisfies its requirement without reading
anything, and records this question as OPEN.  This control inherits it.
**OPEN OBSTRUCTION.**

### SF-OPEN-E — the sibling record is not the same file in every clone

**Record-format limitation remains; the CI bypass is closed.**
`receipts/side_free.json` carries its conditional source check at
`gates.G1.commit_check`, as the frozen design requires. If that source is
unavailable, its diagnostic bytes can differ; no clone-independent claim is
made for this record. The reported source commit now comes from the manifest,
with the separate pin metadata required to agree.

The source pin now names its actual landed merge. The required verifier fails
on unavailable or differing source and on source outside the checked history;
the CI receipt comparison is unconditional. The earlier named-skip route is
retired. A clone lacking the source is invalid, not a passing execution with
ungated drift. Frozen design and predictions remain byte-identical.

`receipts/comparison.json` retains its distinct clone-independent rendering
property, covered by SF-COMPARISON-RECORD-IS-CLONE-INDEPENDENT.
**OPEN OBSTRUCTION.**
