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

## 2026-09-04, Challenge 1 predictions frozen

`challenge1/PREDICTIONS.md` committed at `152ed096` before the branch's
first Challenge 1 code-or-proof commit, sha256
`7cf17e56fffb4e45d4100750010265582fa921fabeed7fb1b84aa798f6e56dc7`.
The existing `challenge*/PREDICTIONS.md -text` attribute covers it.  (This
entry first read “before any Challenge 1 code or proof existed in the
working tree”; corrected in place by the review repair below, because git
establishes committed order only.)

## 2026-09-04, Challenge 1

Presentation layer (`code/boundary/presentation.py`: a reader bounded to
one bar and one mark, and the two presentation-to-side conventions),
kernel extensions (mention and supplied readings of a history, the mark
profile, new observations, permitted images, the isomorphism witness and
relation), `code/boundary/challenge1.py` with the bounded candidate
enumerator and the mechanical scorer of C1-1 to C1-7 and of C0-X,
`lean/BoundarySeed/Challenge1.lean` (29 theorems; the axiom log
regenerated once, 20 to 49 reports), the receipt, 44 new tests, the
registration, the paper, the ledger, and this entry.  C0-X scored HIT in
both halves; C1-1 to C1-7 HIT; C1-X pending.  Things repaired during the
challenge, recorded rather than hidden:

- The Challenge 0 generator census fired on the new candidate enumerator
  while it lived in the kernel, which failed the Challenge 0 kernel test
  and the Challenge 0 receipt's byte identity.  A live failure of the gate,
  not an injection.  The enumerator moved to the metatheory module, the
  Challenge 0 receipt is byte-unchanged, and the census is now reported per
  module so that the metatheory's event constructors are named rather than
  hidden.
- The no-timestamp scan of the new receipt matched the substring `date`
  inside `candidates`; it now matches whole words, and asserts that the
  word `candidates` is present so the repair cannot silently widen.
- The first `lake build` did not elaborate `Challenge1.lean` because the
  root did not import it: the tree's verifier text-scanned the file and
  reported a successful build with 20 reports.  The root now imports it,
  and `verify_lean.py` fails by name on any module under
  `lean/BoundarySeed/` outside the root's transitive import closure; proved
  by injection and by a committed negative test.
- Five Lean induction steps first failed because `simp only [replay,
  List.foldl]` unfolded past the induction hypothesis; they now step by a
  definitional `show`.  A drafting placeholder theorem was removed before
  the first build.
- Two names imported into the challenge module from the presentation
  module appear in that module's census row because the census reads
  module members as they are; the expectation says so rather than
  filtering them out.

WITHDRAWN from nothing: no earlier claim was narrowed by this rung.  The
Challenge 0 statement “a later challenge that adds an event kind re-runs
the census” is kept and annotated: Challenge 1 added no event kind, and the
census fired anyway on a metatheoretic enumerator.

## 2026-09-04, Challenge 1 exact-head review repair

`SEED.md`, `challenge0/PREDICTIONS.md`, and `challenge1/PREDICTIONS.md`
remain byte-identical.  Review of `8a8ed61e` found one blocking and ten
should-fix defects; every finding is addressed, none declined.  Recorded
rather than folded into the entry above:

- WITHDRAWN: the designation of the convention's admitted candidate as the
  current state.  The caller supplied and did not retain; the run's own
  results say the supply entails no admission; no admission event was the
  caller's; the only declared convention maps a presented side and
  licenses no admission.  Designating the admitted candidate current
  turned a candidate from the run's own enumerator into admitted state
  without an admission event, conflating supply with admission.  The
  current state after Challenge 1 is now the replay of the caller's
  history, the supply alone, and equals genesis; the two candidates are
  certified and retained in their isomorphism classes, none current; the
  convention selects a candidate admission and admits nothing (paper
  definition 25, ledger B1-CURRENT-STATE, receipt `current_state`,
  `candidate_classes`, `convention.candidate_event`, `selection_is_by`;
  `designated_current` and `retained_non_isomorphic_candidates` removed).
  Admission is deferred to Challenge 2's “retains”, whose price is that
  rung's first decision.
- Re-scored: C1-5 from HIT to PARTIAL.  Its clause “the designation is by
  convention and not by proof” was first scored as the current-state
  designation just withdrawn; the repaired run takes the alternative the
  frozen text said it was betting against, so the clause as first read is
  MISSED and the facts remain HIT.  Recorded next to its value in the
  receipt, the status, and the paper; the frozen file untouched.
- Re-scored: C1-4 from HIT to PARTIAL.  Its clause “the admission is the
  only event in the history” is false as written (each candidate history
  is one supply and one admission; a supply is an event by definition 5)
  and had been scored on the silently weakened reading “the only
  state-changing event”.  The scorer now scores both readings and reports
  them, following the C0-4 precedent.
- The kernel refuses an admission naming an already admitted token on the
  other side, by name, instead of absorbing it with the requested side
  discarded: the C1-2 falsifier “an event that moves the admitted mark”
  could not fire by construction before.  A same-side re-admission stays a
  no-op and is no longer called a designation; that word is reserved for
  current-state designation.  Both rules are Python-only DEFINITION (the
  Lean events carry no token), and the ledger's retention entry now
  separates the Lean-proved part (supplies and new placements) from them.
  Negative tests in both directions; C1-2's parenthetical annotated
  SHARPENED, its retention clause still HIT.
- Added in Lean: `exchangeSide`, `exchangeSide_exchangeSide`,
  `map_exchangeSide_map_exchangeSide`, `reflect_step`, `reflect_replay`
  (by induction on histories), `continuation_reflects`,
  `other_continuation_is_a_reflection`.  B1-REFLECT-COMMUTES had been
  PROVED on two single-step lemmas with its history-level “hence” clause a
  prose step and a cited Python test that checked only an involution; it
  now rests on the replay-level theorem and on
  `test_reflect_commutes_with_replay`, which matches the falsifier over
  86 accepted histories.  The axiom log was regenerated once, deliberately,
  49 to 55 reports, with no injection live.
- Narrowed: B1-CONVENTION-O's “related by no permitted renaming” from
  PROVED to PROVED for the Lean one-mark relation (which under O is raw
  inequality by unfolding `reflectionPermitted`) and COMPUTED for the
  general relation with mark permutations, over the unpruned search.  The
  one-mark relation's adequacy is prose, not a theorem; a Lean statement
  of it is recorded as a leftover, not attempted.
- Relabelled DEFINITION, in the ledger, the paper's 7.2, and the status
  table: B1-SUPPLY-PRESENTATION's state and judgment clauses (`rfl`), the
  step lemmas `step_reading`, `step_initialDatum`,
  `step_preserves_sideNamed` (by unfolding; their `replay_` inductions
  carry the content), `no_event_follows_admitted` (a bare instantiation
  of `no_event_follows`), and the permission halves of
  `candidates_related_U` and `candidates_not_related_O`.  The paper's
  DEFINITION-level sentence had listed five theorems and counted two of
  the same shape as content; it now lists all of them and says why.
- Narrowed the freeze-order sentence in the paper, the status, and the
  entry above to “before the branch's first Challenge 1 code-or-proof
  commit”, the Challenge 0 repair's wording; the working-tree claim is
  not something git can establish, and the sentence that followed it
  already retracted it.
- The no-timestamp scan matched whole words with `\b`, which treats `_`
  as a word character and so could not see `build_date`, `run_timestamp`,
  or `python_version` — the form every key in the receipt takes.  It now
  requires the watched word not to be glued to letters, is shared with
  the Challenge 0 receipt test so the two receipts are held to one
  standard, and is proved by a planted-key test and a `MANUAL.md` row
  recording the old scan's silence on the same plant.
- The workflow's test-count grep updated from 97 to 106 after observing
  the stale count fail on the fresh log.

WITHDRAWN from the Challenge 1 entry above: “C1-1 to C1-7 HIT” (two are
PARTIAL) and “WITHDRAWN from nothing” (the designation, the PROVED
labels, and the freeze wording are narrowed here).  The Challenge 0
status's note that the re-admission convention was remembered as a
“designation” is left as the historical record it is; the notion it
names is now called a same-side no-op.

## 2026-09-04, Challenge 1 second exact-head review repair

`SEED.md`, `challenge0/PREDICTIONS.md`, and `challenge1/PREDICTIONS.md`
remain byte-identical.  Review of `9a26a250` found one blocking defect,
reported three times, and five should-fix defects; every finding is
addressed, none declined.  Recorded rather than folded into the entries
above:

- Re-scored: C1-2 from HIT to PARTIAL.  Its frozen parenthetical, “a
  re-admission of the same token on either side, which is designation and
  not duplication”, predicts that a re-admission naming the other side is
  an accepted later event that leaves the mark's judgment unchanged, which
  is what the pre-repair kernel did.  The repaired kernel refuses that
  event by name, so the clause is false as written.  The first review
  repair labelled it SHARPENED from the overall boolean with no clause
  fact; SHARPENED at C0-5 named a clause that was true and too narrow, and
  this clause is contradicted, not narrowed.  WITHDRAWN.  The receipt now
  carries the clause's own fact, `moving_admission_accepted_and_inert`
  (false: a refused event has no after-state), reports
  `facts_status: HIT` and `either_side_readmission_clause_status: MISSED`,
  and scores PARTIAL by the rule that scored C1-4.  The facts accept a
  moving admission that is refused or accepted and inert, and miss on one
  accepted and moving the mark, which is the frozen falsifier.  Tests: the
  clause hits only when every moving admission is accepted and inert, and
  a kernel-level probe shows the fact true only under an absorbing step.
  The receipt regenerated deliberately with no injection live.
- Re-counted: “Five of seven hit, two PARTIAL” is WITHDRAWN.  Three hit as
  content (C1-1, C1-3, C1-6); C1-7 hits by construction and is
  DEFINITION-level, not counted as content; three are PARTIAL (C1-2, C1-4,
  C1-5).
- C1-7's mechanical part is true by construction: the regime type
  represents neither a second datum nor a second boundary, so
  `initial_datum_unchanged` cannot be reported false, and `marks == 1` is a
  proxy the frozen text does not name.  The receipt's `result_basis` and
  `mechanical_part` say so, and so does B1-ONE-BOUNDARY.  An earlier
  version counted it among the hits; `PLAN.md` says a target true by
  unfolding a definition is never counted as content.
- Narrowed, then proved: B1-SIDES-U's “no permitted-renaming-invariant
  judgment of the bounded domain separates the candidates” had been PROVED
  on `invariant_judgment_does_not_separate`, whose hypothesis is
  reflection-invariance at every regime, stronger than the Python bounded
  notion, so the theorem closed less than the clause: `OnSide(1, s)` is
  invariant on the one-mark domain and not everywhere.  Added
  `bounded_invariant_judgment_does_not_separate`, whose hypothesis is
  invariance under the reflection at every regime of the reading with at
  most one mark, which is the Python notion under U by inspection of
  `permitted_images` at one mark; the clause now rests on it, PROVED, with
  the enumeration COMPUTED.  The global theorem is kept and labelled as
  closing less.  The axiom log regenerated once, deliberately, 55 to 56,
  with no injection live.
- Relabelled DEFINITION: B1-CURRENT-STATE's state clause, “the supply-only
  history replays to genesis”, is the n = 1 instance of
  `replay_supply_inert`, which is `rfl`, and had been PROVED beside two
  entries labelling the same one-supply fact DEFINITION.
- Relabelled DEFINITION, one theorem one label: the first review repair
  called `supply_no_op` DEFINITION-level in B1-SUPPLY-PRESENTATION and
  left it PROVED in B0-INERTIA, the Challenge 0 status table, and the
  paper's 4.1 and 7.1, with `genesis_initial_datum`,
  `genesis_placement_nil`, `reflect_genesis`, `replay_deterministic`,
  `step_changes_only_by_place`, `reflection_permitted_U`,
  `reflection_not_permitted_O`, `side_names_distinct`, and
  `no_event_follows` of the same `rfl`, unfolding, substitution, or
  case-split shape.  All are DEFINITION-level now in B-DATUM, B0-INERTIA,
  B0-REFLECTION-U, B0-REFLECTION-O, the Challenge 0 status table, and the
  paper's 4.1 and a new 7.1 sentence parallel to 7.2's.  The Challenge 0
  status table is a prior rung's file; its labels are corrected in place
  with a note, because a known-wrong label left in a handoff propagates.
- `admitted_candidate_is_current`, the sole input of C1-5's designation
  clause, was computed as “the current regime has at least one mark”; a
  caller history admitting any other token would have made it true with
  no Challenge 1 candidate current.  It is now membership of the current
  regime in the candidate regimes, and a test with such a history shows
  the two readings differ.  The receipt value is unchanged, false.
- The workflow's test-count grep updated from 106 to 109 after observing
  the stale count fail on the fresh log.

WITHDRAWN from the entry above: “C1-2's parenthetical annotated SHARPENED,
its retention clause still HIT” and, from the paper and status it
describes, “Five of seven hit, two are PARTIAL”.  Declined: nothing.

## 2026-09-04, Challenge 1 third exact-head review repair

`SEED.md`, `challenge0/PREDICTIONS.md`, and `challenge1/PREDICTIONS.md`
remain byte-identical.  Review of `00acb2f7` found four should-fix
defects; every finding is addressed, none declined.  No prediction's HIT,
PARTIAL, or MISSED status changed, no theorem was added or removed, and
the axiom log was not regenerated.  Recorded rather than folded into the
entries above:

- Split, one clause one label: B0-X had labelled each half PROVED as a
  whole.  Its U half's clause “no new event kind or judgment form” is
  decided in `score_c0x` by comparing the receipt's `event_kinds`,
  `observation_vocabulary`, and candidate `history` kinds against the
  Challenge 0 declarations, a receipt comparison and not a Lean theorem;
  its O half's “distinct before” clause rests on
  `sides_distinct_at_genesis_O`, which the entry's Lean list did not cite.
  Now PROVED for the profile and judgment theorems, DEFINITION for the
  declared history shape (`admitted_eq`, `rfl`), COMPUTED for the grammar
  clause, with `sides_distinct_at_genesis_O` and its report
  `propext, Quot.sound` added to the list.  Reason: a receipt comparison
  had been carried under a PROVED label, which is the receipt-as-proof
  move the seed forbids, and a cited theorem must be named where it is
  used.
- Re-counted, and the rule stated: “Three of seven hit as content (C1-1,
  C1-3, C1-6)” is WITHDRAWN.  C1-1's receipt facts are exactly the ones
  B1-SUPPLY-PRESENTATION and B1-CURRENT-STATE label DEFINITION (`rfl` by
  unfolding `step`), and C1-6's clauses are the empty relation by
  declaration, the step lemmas by unfolding, and a census of the run's
  own grammars, a modelling decision of the same kind as C1-7's; C1-7 had
  been excluded from the tally on that very rule while the other two were
  counted.  The rule is now stated once (a prediction counts as content
  only if at least one of its hitting clauses, read literally, rests on a
  theorem outside the DEFINITION-level lists or on a computation not
  fixed by a declaration alone) and applied by the scorer: the
  DEFINITION-level list is declared in `challenge1.py`, every listed
  prediction and the one content hit carry a `result_basis`, and the
  receipt's `tally` counts the statuses against the list, with negative
  tests for a miss on a listed prediction and for an unknown status.  One
  of seven hits as content (C1-3); C1-1, C1-6, and C1-7 hit by
  construction; three are PARTIAL; C0-X hit in both halves as content.
  Reason: `PLAN.md` says a target true by unfolding a definition is never
  counted as content, and a tally applied to one prediction and not to
  two others of the same shape is a judgement call the receipt could not
  check.  The receipt regenerated deliberately, 24663 to 26687 bytes, with
  no injection live.
- WITHDRAWN: “the current state is genesis with `a` presented”, from the
  paper's definition 25, its 5.1 and 9, and the status.  The current state
  is a regime, the replay of the caller's history; the regime type has no
  supplied or presented component (`Regime` carries reading, marks,
  placement, and the initial datum, and `replay`'s supplied set is a local
  of the replay); so “with `a` presented” read the supply into the state,
  the conflation of supply with state that the first review repair had
  withdrawn in its designation form.  The prose now says what the receipt
  says: the current regime is genesis, the caller's history is
  `[Supply(a)]`, and that `a` is supplied is a fact of the history
  (definition 20).  Reason: the seed lists supply and current-state
  designation among the notions never conflated.
- WITHDRAWN: “retained” for a candidate class the run does not drop.  The
  paper's section 1 defines retention as the placement tuple, the seed
  lists retention among the notions never conflated, and the run says what
  the caller's “retains” admits is Challenge 2's first decision; yet the
  candidate classes, which lie in no placement tuple and admit nothing,
  were called retained in the paper, the ledger, the status, the scorer,
  and a Lean docstring.  A candidate class is now *kept*, declared beside
  the definition in section 1 together with the seed's two other subjects
  of the verb (the caller's whole, the run's tied branch), and retained
  names the placement tuple alone; the caller's “retains” stays quoted.
  Reason: one word in two undeclared senses is a conflation whether or not
  either sense is wrong.
- The workflow's test-count grep updated from 109 to 111 after observing
  the stale count fail on the fresh log.

WITHDRAWN from the entry above: the count “Three hit as content (C1-1,
C1-3, C1-6)”.  Declined: nothing.

## 2026-09-04, Challenge 1 fourth exact-head review repair

`SEED.md`, `challenge0/PREDICTIONS.md`, and `challenge1/PREDICTIONS.md`
remain byte-identical.  Review of `44d2f1b7` found one blocking and six
should-fix defects that survived refutation; every finding is addressed,
none declined.  No theorem was added or removed and the axiom log was not
regenerated.  One prediction's status changed, C1-5, PARTIAL to HIT, for
the reason given first.  Recorded rather than folded into the entries
above:

- Re-scored: C1-5 from PARTIAL to HIT.  Its clause “the designation is by
  convention and not by proof” had been scored, since the first review
  repair, as current-state designation of the convention's admitted
  candidate and reported MISSED, while the paper said all three PARTIALs
  came from scoring the frozen text literally.  The frozen text does not
  contain the words “current-state designation”: it says the convention
  designates a candidate (“the designated one”, whose reflection is the
  regime under the other convention) and that the designation is by
  convention and not by proof.  The run does exactly that:
  `selection_is_by` reads “declared convention, not proof”, the candidate
  event is the convention's image of the presented side, and
  `other_is_reflection_of_candidate` is true.  So the clause hits on its
  own words, and the earlier MISSED was scored on a reading the frozen
  text does not contain, which the literal rule forbids in this direction
  as in the other; WITHDRAWN.  The withdrawal of the current-state
  designation itself (definition 25) stands: it is a fact about the run,
  not a clause of the prediction, and `admitted_candidate_is_current`
  stays a plain fact of the current state, read by no clause.  The scorer
  now reports `designation_clause_status` and `convention_clause_status`
  beside `facts_status`, and the tally follows mechanically from the
  statuses: two of seven hit as content (C1-3, C1-5), three by
  construction, two PARTIAL.  Reason: the rule of this tree is to score
  the frozen words and never a reading the text does not contain, in
  either direction, and the headline tally depended on the breach.
- The frozen convention pinned literally: “left is side 0, which O names
  `near`”.  The pre-repair scorer checked only that the declared
  convention was one of the two, so declaring the other convention with
  its swapped candidate event scored `facts_status: HIT` on the same
  facts, observed live before the repair.  The scorer now requires
  `declared == "left is side 0"`, that convention's left side `0`, the
  candidate event's side `0`, and the O name of side 0, carried into the
  receipt as `side_0_name_under_O`; a negative test declares the other
  convention by patching the declaration, recomputes the O facts, and
  expects `convention_clause_status: MISSED` with the facts and the
  designation clause still hitting, PARTIAL, and each pinned piece
  missing on its own.  The receipt regenerated deliberately, 26687 to
  27943 bytes, with no injection live.  Reason: a prediction that names
  its convention must be falsifiable by the other one.
- C1-3's content basis corrected: it had attributed the frozen per-event
  name clause (“hold after every event exactly as before”) to the
  history-level induction `replay_preserves_sideNamed` and said “none of
  them by unfolding”, while the paper's 7.2 lists the per-event lemma
  `step_preserves_sideNamed` as DEFINITION-level and C1-6's parallel
  clause was scored on exactly that per-event reading.  The basis, in the
  scorer, the receipt, the paper, the status, and B1-ONE-JUDGMENT, now
  rests C1-3's content on `admitted_onSide_true_iff`,
  `place_new_judgment`, and `place_other_side_false`, and says the name
  clause read per event is `step_preserves_sideNamed`, DEFINITION-level,
  as C1-6's was scored.  No status or tally change.  Reason: one clause
  shape, one label, across predictions.
- `reflect_step` removed from the paper's 7.2 DEFINITION-level list: its
  place branch is `reflect_step_place`, a Challenge 1 lemma proved by
  `simp` with the map of a placement over an append and carrying
  `propext`, not a case split onto `rfl`.  `reflect_step_place`,
  `exchangeSide_exchangeSide`, and `map_exchangeSide_map_exchangeSide`,
  cited in B1-REFLECT-COMMUTES with no label, are labelled PROVED there.
  No result changed.  Reason: a theorem in the DEFINITION-level list that
  carries `propext` through a proved branch is mislabelled.
- B1-SIDES-U's clause “‘the mark lies on exactly one side’ is a U fact”
  carried no status, evidence, or Lean theorem, and the closed grammar has
  no judgment expressing “exactly one side”.  It is now labelled PROVED as
  a metatheoretic statement, in each candidate exactly one `OnSide`
  judgment holds, mark 0 on the placed side (`admitted_onSide_true_iff`),
  where none held at genesis (`no_observation_at_genesis`), at both
  candidates, and stated not to be an internal judgment of the closed
  grammar; both theorems and their reports added to the entry.  Reason:
  every clause of a ledger statement carries a status.
- WITHDRAWN: “supply” in a second, undeclared sense.  Definition 25, the
  paper's 5.1, and B1-CURRENT-STATE's statement and falsifier used
  “nothing the caller did not supply” and “does not supply at this
  challenge” for the caller providing any event, an admission included,
  which is not the `Supply` presentation event of definition 5.  Reworded
  to “the replay of the caller's history and of no event the caller's
  history does not contain” and “no admission event is in the caller's
  history at this challenge”; the module docstring of `challenge1.py`
  carried the same phrase and is reworded too.  “Supply” and “supplies”
  now name the event and the seed's quoted words only.  Reason: the seed
  lists supply among the notions never conflated, and one word in two
  undeclared senses is a conflation.
- Narrowed: the Challenge 1 status said nothing in the isomorphism
  witness was remembered, but the Challenge 0 status had already declared
  the brute force over renamings with tokens forgotten as written from
  memory, and the witness search is that enumeration.  The sentence now
  covers the separating-judgment computation and the
  reflection-commutation theorems only, and says the witness search
  reuses the remembered shape, with only its use as a witness or relation
  and the canonical-key agreement test new to this rung.  Reason: a
  provenance claim that contradicts the prior rung's declaration
  overstates.
- The workflow's test-count grep updated from 111 to 112 after observing
  the stale count fail on the fresh log.

WITHDRAWN from the entry above: “One of seven hits as content (C1-3)”,
“three are PARTIAL”, and, from the paper and status it describes, “no
prediction's HIT, PARTIAL, or MISSED status changed” as a description of
every re-count.  Declined: nothing.

## 2026-09-05, Challenge 1 fifth exact-head review repair

`SEED.md`, `challenge0/PREDICTIONS.md`, and `challenge1/PREDICTIONS.md`
remain byte-identical.  Review of `78c4a96c` found five should-fix defects
that survived refutation, two of them the same defect reported by two
reviewers and repaired together; every finding is addressed, none
declined.  No theorem was added or removed, no prediction's status
changed, and the tally is unchanged.  Recorded rather than folded into the
entries above:

- Narrowed: B1-ONE-BOUNDARY's “every certified regime keeps the one
  initial datum and places one mark”.  The current state is a certified
  regime that places none — under both readings `current_state.certified`
  is true with `marks: 0` — while the scorer reads only the candidate
  regimes.  The ledger statement and the receipt's C1-7 evidence now say
  “every certified candidate regime”, name that population as the one the
  scorer reads, and add that the current state is certified and places
  none.  No status change.  Reason: a ledger sentence that generalizes
  past the population its evidence covers is an overclaim, and the
  receipt carried the same words.
- Declared: the frozen file's two other senses of “designation”.
  Section 1 reserves the word for current-state designation, and C1-5's
  clause is scored on the frozen file's bare use of it for the
  convention's selection; one word in two undeclared senses is the
  conflation the third and fourth repairs removed for “retained” and
  “supply”, and here the sense chosen decides C1-5's status and the
  content tally.  Section 1 now declares that the reservation is on this
  run's own prose and that the frozen file's two other senses — a
  re-admission of an already admitted token at C1-2, the convention's
  selection at C1-5 — are each read in their own context and neither as
  current-state designation; B1-CONVENTION-O, the kernel docstring, and
  the two receipt clause facts say the same, and C1-5's HIT is stated to
  depend on that declared reading.  No status change.  Reason: a word
  this run has reserved needs its other readings declared where they are
  scored, not glossed in one clause fact.
- Relabelled: `reflect_admitted` is DEFINITION-level.  Its statement is
  true by unfolding — both sides reduce to the one-element placement,
  exactly as `reflect_genesis` reduces on the empty one — but its proof
  was `simp [reflect]`, whose `propext` the axiom log then carried, and
  the paper called it the content of `candidates_related_U` while C1-5's
  basis said “none of them by unfolding”.  The proof is now `rfl`;
  `reflect_admitted` and `candidates_related_U`, whose other half is the
  permission by unfolding, join the paper's 7.2 DEFINITION-level list and
  are relabelled in B1-SIDES-U and B1-CONVENTION-O; their axiom reports
  become none and the log was regenerated deliberately, 56 reports with
  two lines changed, no injection live.  C1-5 stays HIT and counted as
  content, on its computed clause and `admitted_candidates_unequal`.
  Reason: a target true by unfolding is DEFINITION-level and never
  counted as content, and a tactic's axiom is not content either.
- Repaired: the injection record's rows 88 and 89 named negative tests
  renamed at `00acb2f7` and `78c4a96c`, so a reader could not run the
  tests those rows cite.  Both rows now name the current tests beside the
  retired names, and `tests/test_prose_citations.py` makes the citation
  total: every backticked `test_*` token in the tree's Markdown, `SEED.md`
  excepted, must resolve to a test the suite defines, and a name that is
  deliberately not runnable is written in plain text.  It failed first on
  exactly those two rows, naming file, line, and name, and again on a
  planted citation in this file; a temporary-tree probe fixes the same
  direction.  Reason: prose that points at a test which cannot be run is
  the failure this repository closes with a totality gate, and these two
  were found by review because no gate read the names.
- The workflow's test-count grep updated from 112 to 114 after observing
  the stale count fail on the fresh log.

Declined: nothing.

## 2026-09-05, Challenge 2 predictions frozen

`challenge2/PREDICTIONS.md` committed at `22d9ea4b`, sha256
`95f9371b030b8df64b4842a5df7be695d9e7f1b2311a300e78d915a701c16474`,
before this rung's first code-or-proof commit.  Eight numbered predictions
with falsifiers and FORCED / NOT FORCED labels, and one extrapolation C2-X
about Challenge 3.  The existing `challenge*/PREDICTIONS.md -text`
attribute already covered the file (`git check-attr` reports `text:
unset`), so no attributes change was needed.  The commit order is what git
establishes; it establishes nothing about off-tree work.

## 2026-09-05, Challenge 2

The caller supplies and retains `<a|>` and `<|a>`.

- **Decided: what the caller's “retains” licenses.**  The admission of
  both wholes (paper definition 30, ledger B2-RETENTION), so this is the
  first rung whose caller history contains an admission and whose current
  state holds marks.  Reason: the seed's word, read against definition 25;
  the alternative, refusing the challenge and recording it OPEN, is stated
  in the paper and not taken.
- **Found live, then decided: the shared visible mark refuses the
  Challenge 1 admission.**  Formed with `AdmitMark`, the caller's history
  is refused by name under both readings and both conventions, by the
  moving-admission refusal, because that event keys the admitted mark by
  its presentation token.  A declared space of exactly two identity
  policies was enumerated, exactly one of which retains both wholes, and
  the run declared that one: a new admission event `AdmitOccurrence`, and
  the withdrawal of definition 3's rule that admitted labels be distinct.
  Reason: Challenge 1's own leftover required this decision to be made
  loudly and priced; the price is one declaration, paid by the run, equal
  under both readings (B2-SHARED-MARK-REFUSED, B2-IDENTITY-POLICY).
- **Withdrawn: the rule that admitted presentation tokens be unique.**  It
  identified presentation identity with internal identity, which the seed
  lists among the distinctions never to be conflated, and Challenge 2's two
  wholes carry the same visible mark.  A regime may now carry one label
  twice; the mark's internal identity is its admission index, which
  definition 3 now states.  The Challenge 1 negative test that asserted the
  old rule was rewritten as a positive test of the new one, recorded as a
  live failure in `MANUAL.md`.  Reason: the identification was a modelling
  decision that this challenge falsified.
- **Added: the token-keyed admission refuses a repeated label by name.**  On
  a regime carrying its label twice, `AdmitMark` cannot say which mark it
  names, so it refuses rather than taking the earliest.  Reason: a silent
  choice there would reinstate the conflation the rung withdrew.
- **Results.**  Two new holding judgments and nothing else; both survive
  every later history of the Lean grammar.  Under U the retained regime has
  exactly two permitted automorphisms, and the non-identity one exchanges
  the two marks and the two sides at once, so neither pair is internally
  separable and neither mark form is invariant; the Challenge 0 profile
  comparison is false there and is not the internal fact.  Under O the only
  automorphism is the identity, both mark forms are invariant and both
  separate the marks, one on `near` and one on `far`.  Under both readings
  the two marks do not share a side, and that property survives all 177
  permitted images of a census to three marks.  The admission order, the
  shared visible mark, and the presentation convention are all carried away
  by a permitted renaming.  Reason: these are the seed's Challenge 2
  questions, answered under each reading (B2-TWO-JUDGMENTS, B2-MARKS-U,
  B2-MARKS-O, B2-DIFFERENT-SIDES, B2-ORDER-AND-LABEL).
- **Added: definition 29, internal fact.**  Invariance under every
  permitted renaming of the reading, numbered so that the Challenge 1 table
  no longer identifies it with “permitted-renaming-invariant separating
  judgment” only through an evidence column, and so that the U “no” is seen
  for what it is: an immediate consequence of the definition once the
  antecedent is computed.  Reason: a review finding of the previous rung.
- **Scored: C1-X, PARTIAL.**  The U half hits.  The O half's names clause
  hits and its price clause — “nothing new is paid at Challenge 2” — is
  false as written, its own falsifier “under O a price beyond the names”
  having fired: the occurrence identity is a new declaration paid at this
  rung under both readings.  Recorded next to its value in
  `challenge2/STATUS.md`, the receipt, and B1-X; the frozen file is
  untouched.
- **Scored: C2-1 to C2-8, all HIT**, five as content and three by
  construction under the criterion Challenge 1 declared.  The paper says
  plainly that a clean sweep of a rung's own predictions is weak evidence,
  the predictions having been written by an instrument that had read the
  whole tree; the informative number is the previous rung's extrapolation,
  which is PARTIAL.
- **Added: the Lean audit-totality check.**  `verify_lean.py` now requires
  every theorem declared under `lean/BoundarySeed/` to carry a `#print
  axioms` line in the root, reading the source text with comments stripped
  first.  Proved by injection, with the counterfactual observed on the same
  tree: with the check removed the same injected theorem left the build
  reporting `lean ok: 84 axiom reports … matching`.  Reason: the paper's
  “every one with a `#print axioms` report” was a totality claim with no
  check behind it, a review finding of the previous rung
  (B2-AUDIT-TOTALITY).
- **Repaired, found live: `verify_lean.py` crashed instead of reporting a
  failing build.**  Its failure printer wrote Lake's non-ASCII progress
  marks straight to a console that could not encode them, so a real build
  failure surfaced as a `UnicodeEncodeError` traceback.  The printer now
  forces the output printable.  Reason: a diagnostic that cannot print is
  not a diagnostic.
- **Widened: the cited-test-name population.**  It read only backtick spans
  that are exactly a name, so a name quoted inside a longer span — a quoted
  failure line — was invisible, which is where two retired names were
  hiding.  It now reads every `test_*` token anywhere inside a span, and
  skips a token followed by `.py`, which is a file name and not a runnable
  test.  On the first run it named three: one retired scan test in
  `MANUAL.md` row 69 and two quoted names in row 107.  All three rows now
  give those names in plain text, as the tree's declared convention
  requires, and tests fix both directions.  Reason: a review finding of the
  previous rung, adapted because the suggested widening would also have
  fired on file-name citations in files this rung must not edit.
- **Repaired: the definitions locator sentence.**  It placed definitions 20
  to 27 in the Python modules while 27 and 28 were marked Lean; it now
  names the Lean-only pair and the Challenge 2 additions.  Reason: a review
  finding.
- **Repaired: definition 3 now states the identity rule.**  A mark's
  internal identity is its position in the admission order; the datum's own
  identity number lives in a different identity space and shares a numeral
  with mark 0 and nothing else; order is not thereby observable, because
  the mark permutations are permitted under both readings, and Challenge 2
  computes that the retention order is carried away.  Reason: a review
  finding that the model identified identity with order while the plan
  declared them kept distinct.
- **Repaired: the moving-admission refusal is attributed to `step`.**
  Section 1 said certifying `replay` refuses it, while the code and
  definition 6 place it in low-level `step`, which `replay` calls and whose
  refusal it surfaces.  Reason: a review finding.  The Challenge 1
  receipt's clause fact keeps the older phrase and was NOT regenerated; see
  the carried list in `challenge2/STATUS.md`.
- **Repaired: the two structural equalities are declared.**  Python
  `Regime` equality compares the presentation labels and the Lean `Regime`
  has none to compare; the Lean regime is the Python regime with tokens
  forgotten, which `serialize` computes.  The difference is live at this
  rung and the receipt reports it.  Reason: a review finding that
  Challenge 2's shared-mark question would make the difference live.
- **Repaired: what the second O class carries.**  The Challenge 1 table now
  says that the transported facts are the side-exchanged facts of the first
  class, because under O the reflection moves placements and not names.
  Reason: a review finding.
- **Repaired: B0-NAMES-O's status split** into PROVED for the two holding
  theorems and DEFINITION for the constructor distinctness, and
  **B1-ONE-JUDGMENT's supply clause given a status and a theorem**
  (`supply_preserves_holds`, DEFINITION-level).  No result changed.  Reason:
  two review findings, one clause one label.
- **Stated: where the DEFINITION-level line runs.**  `side_names_distinct`
  and `admitted_candidates_unequal` are both constructor distinctness after
  unfolding; the run's line is the shape of the obligation, a closed
  statement closed by `decide` against a parametrised one needing a rewrite
  and a case split.  That is a labelling convention, not a difference in
  depth, and the paper now says so and records that the stricter reading
  would move `admitted_candidates_unequal` without moving C1-5.  Reason: a
  review finding that the paper drew the line without saying where it ran.
- **Reworded: the continuation-reflection sentence of section 9** is now
  scoped to the Lean grammar, with the Python kernel's bound stated beside
  it.  Reason: a review finding.
- **Reworded: two Lean docstrings.**  `challenge1History` and `admitted`
  now say plainly that they are the candidate history and the candidate
  regime and that Challenge 1 admits nothing, and `oneMarkRelated` no longer
  asserts its adequacy for one-mark regimes flatly.  The names themselves
  are unchanged and carried as a leftover, with the reason in
  `challenge2/STATUS.md`.  Reason: two review findings.
- **Renamed: the Challenge 1 candidate-space cross-check.**  Its old name
  claimed an unpruned enumeration while it re-derived the same token
  population under a different filter; it now says so.  Reason: a review
  finding.  No minimality claim rested on it.
- **Registered** the rung in the research job: the test-count grep and
  `python run_challenge2.py`, with nothing else in that file changed.

## 2026-09-05, Challenge 2 apparatus and pins

- `challenge2/PREDICTIONS.md` added to the frozen table of
  `verify_pins.py`; the pin was proved by injection.
- `run_challenge2.py` added to the tree's mypy file list.
- The Challenge 0 and Challenge 1 receipts were confirmed byte-unchanged
  across the rung, which is the check that the kernel additions disturbed
  neither earlier rung.
- The axiom log was regenerated deliberately once, 56 to 84 reports, with
  no injection live.

## 2026-09-05, Challenge 2 exact-head review repair

`SEED.md`, `challenge0/PREDICTIONS.md`, `challenge1/PREDICTIONS.md`, and
`challenge2/PREDICTIONS.md` remain byte-identical.  Review of `befdcb05`
found two should-fix defects that survived refutation, both in `paper.md`
and both narrowings of a sentence that claimed more than the object it
described.  Every finding is addressed, none declined.  No theorem was
added or removed, no prediction's status changed, no receipt regenerated,
and the tally is unchanged.

- Narrowed: section 7.3's “every theorem is stated for both readings”.
  `retained_composite_permitted_U` takes no `(rd : Reading)`; it pairs the
  Challenge 0 permission with the composite and is stated at `.U`, which
  the table row beside it already said.  The sentence now scopes the claim
  to the theorems about the retained regime, names that one exception, and
  says that the three involution lemmas are about an arbitrary argument
  and name no reading.  Reason: a totality sentence about a table that the
  same table contradicts is an overclaim, and the paper's own row was the
  counterexample.
- Corrected: section 5.6's count of FORCED predictions among the content
  hits, three to four.  The receipt labels FORCED exactly C2-2, C2-4,
  C2-5, C2-6, C2-7, and `tally.hit_as_content` is C2-4 to C2-8, so the
  intersection is four; the fifth FORCED prediction, C2-2, is
  DEFINITION-level and not counted as content, and the sentence now says
  so.  No status and no tally moved: the wrong number was prose read off
  the receipt, and it is prose still — no gate computes this intersection,
  so it is corrected and named rather than pinned.  Reason: a number the
  paper attributes to the receipt must be the receipt's number.

Declined: nothing.

## 2026-09-05, Challenge 3 predictions frozen

`challenge3/PREDICTIONS.md` committed alone at `a4f2a688`, sha256
`27057895c47e5bd718b0ea8e51689f3325cef78102c912c6feea8e913a7e7755`, before
any Challenge 3 code or proof.  Nine predictions, C3-1 to C3-8 and the
extrapolation C3-X, each with a falsifier and a FORCED / NOT FORCED label.
The existing `challenge*/PREDICTIONS.md -text` attribute already covered the
new file, so no attributes change was needed.

## 2026-09-05, Challenge 3

The caller requires `<a|>` and `<|a>` to be internally separable in a
precisely declared sense.  `SEED.md` and the three earlier prediction files
remain byte-identical.

- **The sense is declared** (definitions 38 and 39): no permitted
  automorphism of the regime carries one retained mark to the other — the
  sense Challenge 2 computed — with a second reading, that some mark
  property invariant under every permitted renaming holds of one and not the
  other.  The two agree **by unfolding**, the witness for the second being
  membership in the first mark's orbit, and the receipt computes the
  agreement at all 48 points under each reading rather than asserting it.
  Reason: the seed asks for a precisely declared meaning, and a second
  reading that agrees by unfolding is a restatement whose agreement can be
  checked, not a second fact.
- **Under O the requirement is already met, and the names are not what meets
  it.**  The four-cell counterfactual square (definition 46) is the same
  under both readings and turns on one coordinate only: the requirement
  holds exactly where the side exchange is not a permitted renaming, whether
  or not the two names are admitted.  This **narrows B2-MARKS-O**, which
  listed the side names among the capabilities the O separation uses; the
  receipt now records them under `capabilities_not_used`.  Reason: the seed
  requires the declaration that satisfies the requirement to be named and
  priced exactly, and the previous rung named one capability too many.
- **Under U no addition of judgment forms can meet it**, whatever the forms.
  This was a Challenge 2 leftover recorded as an argument and not a theorem;
  it is now PROVED in Lean for an ARBITRARY property of a `(Regime, Nat)`
  pair (`no_invariant_mark_property_separates_retained`), with a countermodel
  (`mark_form_is_not_invariant_under_the_composite`) showing that the
  hypothesis excludes exactly the two mark forms and is therefore a real
  restriction.  Reason: the leftover asked the rung to prove it or refuse to
  lean on it.
- **The candidate space is declared** (definition 40): five coordinates, 48
  points under each reading, exhaustive over those coordinates and nothing
  wider.  One step is one moved coordinate, which is exactly a capability
  count of one (definition 41); 41 points bundle and are refused, the
  candidate that adopts reading O under U among them at count two.
- **Three tied non-isomorphic minima under U, all retained; uniqueness
  refuted** inside the declared space.  Four one-step points meet the
  requirement and fall into three classes under the implemented quotient
  (definition 42).  Under O the minimum is zero and unique, the null
  augmentation alone.  Reason: the seed requires all tied minima to be
  retained unless uniqueness is proved, and it is refuted here rather than
  proved.
- **The three separate by three different mechanisms**, and one of them —
  withdrawing the mark permutations — meets the requirement **by unfolding**,
  by declaring the metatheoretic admission index to be an internal
  designation, leaving the admitted boundary idle.  It is reported and
  labelled DEFINITION-level rather than excluded: no declaration of the run
  rules it out, and the requirement as declared does not oblige the boundary
  to do the work.  Reason: the seed says not to assume the boundary makes
  the requirement trivial, and this is the other half of that warning.
- **A second cost measure is declared** (definition 44): the collateral
  count, over five declared facts, counting only what a candidate makes
  available that the same reading's base did not.  It selects the same three
  minima, and the two measures differ elsewhere in the space, so neither is
  the other.
- **Kernel**: `model.py` gains the flagged renaming enumerations
  (definition 37) — `permitted_images_under` and the six functions built on
  it, with `serialize_keeping_labels` — each of which reduces to its
  Challenge 2 counterpart at the flags the reading declares, checked over
  every regime of at most three marks under both readings.  No event kind
  and no judgment form is added at this rung.
- **Lean**: `lean/BoundarySeed/Challenge3.lean`, twenty-one theorems, all
  reports within `{propext, Quot.sound}`.  Besides the two above it proves
  the count argument — a renaming preserves how many marks lie on each side
  and the side exchange exchanges those counts, so at a placement whose
  sides carry different numbers no renaming undoes the exchange — over EVERY
  permutation, and records the converse at the retained regime, where the
  counts are equal and the argument says nothing.  That closes, in one
  direction and for this shape of placement, half of the equal-count law the
  Challenge 0 census left as a computation.
- The axiom log was regenerated deliberately once, 84 to 105 reports, with
  no injection live.
- `challenge3/PREDICTIONS.md` added to the frozen table of `verify_pins.py`;
  the pin was proved by injection.  `run_challenge3.py` added to the tree's
  mypy file list and to the research job, and the job's test-count grep
  moved from 165 to 222.
- The Challenge 0, Challenge 1, and Challenge 2 receipts were confirmed
  byte-unchanged across the rung, which is the check that the kernel
  additions disturbed no earlier rung.

Repairs and defects found during the rung, each recorded next to its value:

- **Found live, not injected**: `extra_mark = 0` was dropped from the
  enumeration because the coordinate test compared each value against a
  shared falsehood and `0` equals falsehood in this language.  The point
  `extra_mark_0` disappeared and the scorer raised on a missing row.  Each
  coordinate is now tested against its own inherited value, and
  `test_side_zero_is_a_moved_coordinate` holds it.
- **Found live, not injected**: the C3-3 clause was first scored against
  "no declared mark property is invariant at the U base", which is false —
  the property that reads the supplied label is invariant everywhere and
  separates nothing.  The frozen text names "the two mark forms of
  Challenge 2", and the clause is now scored on those two, with the label
  property reported separately.  Recorded because the first scoring would
  have reported a MISS on a clause the frozen file does not make.
- **Found live, not injected**: the C3-5 clause was first scored by
  comparing an ordered list, while the frozen text names four points and no
  order; the comparison is now by set, with the enumeration's own order kept
  in the receipt.
- **Found live, not injected**: a Lean decision procedure was offered a goal
  carrying the reading as a free variable and refused it — the same defect
  the Challenge 2 rung met.  Two placement lemmas project the reading away
  first; that is apparatus and the paper says so.

Advisories from the review of Challenge 2, actioned in living documents:

- Section 0 now discloses the adversarial review channel beside the
  surviving provenance claim, naming what it has supplied and what it has
  not.  Reason: the ceiling should be declared where the ceiling is
  declared, not only in the statuses.
- Definition 29 now says that the invariance is over the token-forgetting
  quotient of definition 14, and definition 33's justifying sentence is
  narrowed to mark properties that forget the presentation tokens.  Reason:
  as written, definition 33 was false in general — a permitted automorphism
  forgets tokens and definition 29's invariance did not, so a
  label-reading property could separate two marks a permitted automorphism
  exchanges.  The one line that closes it here is added: at the retained
  regime both labels are `a`, so the image is equal and not merely equal
  after forgetting.
- The definition-locator sentence of section 3 is corrected a second time:
  definition 36 is Lean-only, as 27 and 28 are, and 37 to 46 are Challenge
  3's.
- Section 5.6 now records the reading of C2-5's frozen phrase "permitted
  automorphism group" — the set of permitted automorphisms, scored by its
  size with its entries reported beside it — and scopes C2-8's content to
  its three search clauses, the O absence following from a declaration.
- `B2-SHARED-MARK-REFUSED` now attributes the moving-admission refusal to
  low-level `step`, surfaced by certifying `replay`, which is the
  attribution the same rung recorded as a repair in the paper and left
  contradicted in the ledger.
- `B2-TWO-JUDGMENTS` now covers its own clause that the two admissions
  change no initial datum and no reading, with the two theorems and the two
  receipt keys.
- `B2-DIFFERENT-SIDES` is narrowed: "under U it buys nothing further about
  them" was a totality the rung did not compute, and it is replaced by what
  is computed, with a pointer to how far Challenge 3 goes and where that
  stops too.
- The receipt keys `certified` and `replays_from_genesis` are tautologies of
  their own construction.  They are kept, and
  `placement_matches_the_declared_convention` is added beside them, computed
  from the presented sides and the declared convention alone (B3-PLACEMENT-
  CHECK).
- The Challenge 1 probe set offered no occurrence admission, so the event
  kind Challenge 2 declared was never offered to the empty relation.  This
  rung's probe set offers all three kinds, and a test holds it to that.
- The Challenge 3 price fields are read off the enumeration rather than
  written as literals: `nothing_new_paid_at_challenge_3` is the minimum
  being zero and `new_at_challenge_3` is the capability list of the retained
  minima.
- The root Lean module's doc comment now says Challenges 0 to 3.

Carried, with reasons, to a dedicated Challenge 1 or Challenge 2 repair
session: everything whose repair lies inside `code/boundary/challenge1.py`
or `code/boundary/challenge2.py` and would regenerate a closed rung's
receipt.  They are listed in `challenge3/STATUS.md`.

## 2026-09-05, Challenge 3 exact-head review repair

`SEED.md` and the four `challenge*/PREDICTIONS.md` remain byte-identical;
`challenge3/PREDICTIONS.md` was not edited and no prediction's status moved.
Review of `7bc2e57e` found eight defects that survived refutation — two
blocking, both the same sentence — and every one is addressed; none is
declined.  No theorem was added or removed and the axiom log was not
regenerated.  The Challenge 3 receipt WAS regenerated, deliberately and with
no injection live, 219403 to 219789 bytes; the Challenge 0, 1, and 2
receipts are unchanged.

- **Narrowed, blocking.**  Section 9 said that "under both readings the
  second declared measure, the collateral count, selects the same minima".
  The receipt says otherwise under O: `readings.O.measures_agree_on_minima`
  is false, the collateral count's minimum of zero being attained by five
  points in three classes while the capability count's is the null
  augmentation alone.  The sentence is now scoped to U with O's behaviour
  stated beside it; the table row in section 5.9 says the same and cites
  `readings.U.measures_agree_on_minima` rather than the wildcard; and
  B3-TWO-MEASURES's statement, evidence, and falsifier are scoped the same
  way.  Reason: the run's own scorer reads the U value only, and the paper
  claimed of both readings what the receipt computes of one.
  `test_the_measures_select_the_same_minima_under_U_and_not_under_O` now
  pins both values.
- **Corrected.**  Definition 44 said the second measure excludes the
  required separation "so that the measure reads what a candidate costs
  beside what it was asked for".  It does not: the first of the five
  declared facts is the required separation said of the two SIDES, and the
  enumeration computes that it takes the requirement's value at every one of
  the 48 points under each reading, so the "one" at each of the three U
  minima is that fact alone.  The definition now says what is true, the new
  receipt key `sides_fact_agrees_with_the_requirement_at_every_point`
  computes it per reading rather than leaving it to prose, and the `mu2`
  description in the receipt is corrected to match.  The declared fact list
  is NOT changed: revising it after the enumeration would fit the
  declaration to the answer, which is the same reason the rung gave for
  reporting the index-withdrawal minimum rather than excluding it.  The
  score of C3-6 is unmoved — its clauses are computed and hold — and
  B3-TWO-MEASURES now records the coincidence.
- **Narrowed.**  Definition 37 said the flagged enumerations are checked
  against their Challenge 2 counterparts "over every regime of at most three
  marks under both readings".  The tests check the image, automorphism, and
  canonical-key functions over every placement of at most three marks with
  fixed distinct labels, and the four separation and isomorphism functions
  at the two-mark placements only; the sentence now says that.  Reason: the
  85-regime population of definition 43 is a different and wider one, and
  the prose borrowed its size.
- **Corrected.**  The section 5.9 row and the `challenge3/STATUS.md` row
  saying the event-follows relation is "empty on all five event kinds" now
  say "empty on every event of all three declared kinds, five probes in
  all", which is what `probes` offers and what `event_kinds` records.
- **Repaired, a gate.**  `challenge3/STATUS.md` claimed that every gate the
  rung added or touched has an injection row.  Two did not: the placement
  check and the probe-set check, both added at that rung, had no row and no
  negative-direction test, so each could only ever read true.  Both are now
  injected, recorded, and reversed — the further mark's admission moved to
  the other side named `extra_mark_0`; the occurrence admissions dropped
  from `probes` named `AdmitOccurrence` — and
  `test_the_placement_key_reads_false_when_the_prediction_parts` and
  `test_the_probe_set_check_sees_a_dropped_event_kind` fix the negative
  direction of each.  The false sentence is corrected in place rather than
  deleted.
- **Recorded, provenance.**  `mu1` and `mu2` are the sealed derivation's own
  names for its two declared cost measures over a candidate space of
  one-step augmentations, and the contract file the harness loads says so;
  this rung introduced the same two identifiers for the same role without
  noticing.  A bullet in the rung's remembered-result section records it, so
  that no later comparison reads the coincidence of names as convergence.
  The same paragraph's provenance sentence is corrected: the harness loads
  the contract file whole, operating manual included, which is wider than
  the five sections the seed's isolation clause names.
- **Corrected.**  The paper's title said "Challenges 0 to 2" after the rung
  added the Challenge 3 sections; it now says "Challenges 0 to 3", which is
  the correction the rung already made to the root Lean module's doc
  comment and missed here.
- The research job's test-count grep moved from 222 to 227, five tests
  having been added; the move was proved by injection.

Declined: nothing.

## 2026-09-05, Challenge 3 second exact-head review repair

`SEED.md` and the four `challenge*/PREDICTIONS.md` remain byte-identical;
`challenge3/PREDICTIONS.md` was not edited and no prediction's status moved.
Review of `e2cc3f94` returned six findings that survived refutation — two of
them blocking and naming the same two stale numbers — and every one is
addressed; none is declined.  No theorem was added or removed and the axiom
log was not regenerated.  The Challenge 3 receipt WAS regenerated,
deliberately and with no injection live, 219789 to 220518 bytes; the
Challenge 0, 1, and 2 receipts are unchanged.

- **Corrected, blocking.**  Section 8 gave the Challenge 3 receipt as 219403
  bytes and the suite as 222 tests.  Both were pre-repair values: the
  committed receipt was 219789 bytes and the suite 227 when the review ran,
  and `challenge3/STATUS.md`, this log, and the research job's grep all
  carried the moved numbers while the paper alone did not.  Section 8 now
  reads 220518 bytes and 228 tests, this session's values, and the rest of
  section 8 was checked against the same battery in the same pass — the
  Challenge 2 receipt at 35499 bytes, the coverage at 100.00% line and
  branch over seven files, and the axiom log at 105 reports all hold.
  Reason: no gate reads the paper's numbers, so nothing caught either; the
  receipt size is stated once in the paper, with the history kept in
  `challenge3/STATUS.md`.
- **Narrowed.**  Section 9 said the Lean countermodel shows that the
  hypothesis of `no_invariant_mark_property_separates_retained` "excludes
  exactly the two mark forms".  The theorem shows only that it excludes
  them: for each side it puts that one mark form outside the hypothesis and
  says nothing about what else lies outside.  The sentence now says that the
  countermodel puts both mark forms outside the hypothesis, so the
  hypothesis is a real restriction and not a vacuous one, which is what
  section 7.4 and B3-NO-JUDGMENT-ADDITION already said.
- **Narrowed.**  Definition 38's second reading was an existential over mark
  properties invariant under every permitted renaming, with no clause about
  the presentation tokens, although definition 33 was repaired at the
  previous rung to carry exactly such a clause.  Without it a property that
  reads a label separates marks a permitted automorphism exchanges:
  `carries_label_a` reads a token and is reported invariant at the base and
  at every one-step point under both readings, and it fails to bite only
  because every enumerated regime carries the same label at every mark.  The
  second reading now requires a property to forget whatever the candidate's
  declared serialization forgets, which at the base is definition 14's token
  forgetting and at the label-keeping coordinate is nothing.  The declared
  text in the receipt (`requirement.second_reading`) says the same.
- **Narrowed.**  Definition 38 said "the receipt computes the agreement at
  all 48 points ... rather than asserting it".  The computed key compares the
  first reading with the DECLARED orbit witness, not with the existential:
  one direction of the agreement — that a property of the second reading's
  kind separating the two marks implies no permitted automorphism carries one
  to the other — is definition 33's justifying sentence, which is prose and
  is computed at no point.  Definitions 38 and 39, the receipt's
  `requirement.readings_agree_because`, the section 5.9 row, the
  `challenge3/STATUS.md` row, and B3-REQUIREMENT all now say which direction
  is computed and against what.  The score of C3-1 is unmoved: it was already
  DEFINITION-level and is not counted as content.
- **Recorded, a premise.**  Definition 39's "invariant by construction" rests
  on a candidate's permitted renamings being closed under composition and
  inverse.  The declared enumerations of definition 37 are — each offers the
  identity, the side exchange where its flag permits it, the mark
  permutations where its flag permits them, and their composites — but the
  closure is neither computed nor proved in this run, and definition 39, the
  receipt text, and B3-REQUIREMENT now say so rather than leaving the reader
  to supply it.
- **Corrected.**  `price_facts` said "Every field below is read off the
  enumeration".  Four of its eight are not: the capability list the
  satisfaction uses, the idle list, where the capability was declared, and
  who paid it are literals this module writes, and no run can move them.  The
  docstring now names the four fields that move and the four declared, the
  receipt names the four under `price.fields_declared_not_computed`, and
  `test_the_declared_price_fields_do_not_move_with_the_enumeration` fixes the
  direction by moving the enumeration and finding the four unmoved and the
  three moved.  Section 5.9's evidence for "what satisfies it under O" now
  cites `counterfactual_square` alone, the square being what shows the two
  names idle, and B3-O-ALREADY-MET records the attribution as a declaration.
  Reason: the C3-2 scorer compares that literal with an identical literal, so
  a citation of it as evidence would let a declaration read as a measurement.
  The previous rung actioned the same advisory for two of the fields and left
  the docstring claiming it of all of them; this finishes it for the rest.
- The research job's test-count grep moved from 227 to 228, one test having
  been added; the move was proved by injection.

Declined: nothing.

## 2026-09-05, Challenge 4 predictions frozen

`challenge4/PREDICTIONS.md` committed alone, before the branch's first
Challenge 4 code-or-proof commit, sha256
`42371f458e23ce89885a76c542863c112482c0ca6b4f1d9ff6a058b3c21f2041`, in commit
`f07a20c4`.  The existing `challenge*/PREDICTIONS.md -text` attribute already
covered it, so no attributes change was needed.

## 2026-09-05, Challenge 4

The caller supplies and retains `<a|b>` and `<b|a>` and requires their internal
separability.  Kernel, Lean, receipt, tests, prose, registration, and the
injections in `MANUAL.md`.  Seven of eight scored predictions hit, one is
PARTIAL, and the previous rung's extrapolation is PARTIAL with its own
falsifier naming the miss.

- **Two declarations were paid, and both are the run's.**  The Challenge 1
  reader refuses both of the caller's inscriptions by name, so the bound was
  widened to at most one mark on each side of the bar; and in which order the
  two marks of one whole are admitted is a second declaration of the same kind
  as the convention.  The narrower reader is left refusing so that what forced
  the widening stays visible.
- **The requirement fails under BOTH readings**, the first rung at which
  reading O does not already meet it.  The obstruction is the exchange of the
  two wholes, which carries the retained regime onto itself using no side
  exchange, so the withdrawal the O reading carries does not touch it.  That is
  the clause the Challenge 3 extrapolation got wrong, and its own falsifier —
  "the O requirement needing a new declaration" — fired.
- **A whole is a set of marks, and the regime carries no grouping.**  The
  requirement and its declared witness are therefore statements about the
  automorphisms of the state together with a grouping read off the caller's
  history, at every candidate that does not admit that grouping.  Recorded as a
  narrowing (B4-GROUPING-IS-METATHEORY) rather than repaired, and priced: the
  repair is the grouping coordinate, and with the naming it costs two.
- **The augmentation the caller's demand names is a bundle.**  The grouping
  alone leaves the tag exchange a renaming the object language cannot see; the
  names alone name tags no mark carries and collapse into the null point; the
  two together meet the requirement under both readings at a capability count
  of two and are refused as one step.  Neither half is a minimum.
- **Under U the minimum is unique inside the declared space**, and it is the
  candidate that meets the requirement by unfolding and leaves the boundary
  idle.  This is the run's first uniqueness statement, and it is uniqueness
  inside seven declared coordinates and nothing wider.  Under O there are two
  tied minima; keeping the presentation labels meets the requirement under O
  and fails under U, because the two wholes are each other's reflection.
- **Repaired during the rung, and live before review saw it.**  The
  whole-property census first carried invariance alone, and reported the
  property that reads the group tag as a witness at the very base where the
  requirement fails.  The repair is definition 55's second conjunct —
  determination by the candidate's key, which is definition 29's
  token-forgetting clause generalized — together with a domain that varies the
  grouping and a census over every two-element mark-set.  Injected and
  recorded; two tests fail by name without it.  The Challenge 3 census, which
  carried the first conjunct only, is left as it stands, with the difference
  named in section 10: no result of that rung moves, its one anomalous property
  having been reported there as invariant and separating nothing.
- **Repaired during the rung.**  The C4-3 and C3-X side-property clauses were
  first scored against "no declared whole property separates the two wholes",
  and both reported MISSED on clauses the frozen files do not make; both are
  now scored on the two side-reading properties the frozen texts name.  The
  same defect appeared twice at Challenge 3 and is recorded again.
- **Restructured for size and cost.**  The first build was 936733 bytes, a 6%
  margin under the megabyte at which the run owes a summary and a gzip, and
  took 9.9 seconds.  Every candidate's facts now come from one enumeration of
  its images rather than fifteen, and the point rows carry the collateral facts
  that HOLD rather than eight booleans: 795554 bytes and 2.9 seconds, with the
  full map on the nine rows reported in full.  A cross-check holds the derived
  values to the kernel's declared functions at every one-step point and at a
  sample of bundles, and it is proved by injection.
- The research job's test-count grep moved from 228 to 303, and
  `run_challenge4.py` was added after the earlier runners; the move was proved
  by injection.  The axiom log was regenerated once, 105 to 138 reports, with
  no injection live.

Advisories from the review of Challenge 3, actioned in this rung's living
documents.  The rule is the one Challenge 2 declared and Challenge 3 reused: an
advisory is actioned when the repair lies in a living document or in apparatus;
one that would regenerate a closed rung's receipt, or edit a previous rung's
`STATUS.md`, is carried with its reason.

- **Corrected.**  The paper's title said "Challenges 0 to 3"; it now says 0 to
  4, and section 0's counts move with it.
- **Corrected.**  Section 5.10's C2-X row counted four hitting clauses where
  the status and the receipt count five; it now counts five and says which.
- **Narrowed.**  Section 5.9 called `retained_counts_equal` "the converse half"
  of the equal-count law.  It is not: the converse — that at equal counts some
  renaming undoes the side exchange — is not proved, and what the theorem
  records is that the counting argument says nothing at the retained regime.
- **Corrected.**  Section 7.4 said the countermodel shows "the theorem above it
  is not vacuous"; what it shows is that the theorem's HYPOTHESIS is a real
  restriction, which is the statement the same section makes correctly four
  lines earlier.
- **Corrected.**  The 7.4 row for `retained_U_requirement_fails` said the
  composite is permitted; the theorem says the SIDE EXCHANGE is permitted and
  the composite fixes the regime.
- **Disclosed.**  Definition 41 now carries the note that `mu1` and `mu2` are
  the sealed derivation's own names for the same role, inherited vocabulary and
  not this run's, which lived only in the Challenge 3 status and this log.
- **Reworded.**  "Internal designation" was a second sense of a word section 1
  reserves for current-state designation, and the rung's central mechanism
  sentence used it; every use in the run's own prose now reads "internally
  available", including the one in definition 3.
- **Scoped.**  "The candidate that keeps the labels satisfies nothing" was
  written without a reading and is false under O, where the base already
  satisfies; the sentence is now scoped to U and says what happens under O.
- **Narrowed.**  The row citing `points_satisfying_with_grammar_change_only`
  now says that the key is empty under U by its own definition's reading
  clause, and that it admits the label-keeping coordinate, which definition 40
  keeps distinct from the judgment grammar.  The key itself is carried.
- **Corrected.**  Section 5.12's row read "every separation result of the
  rung" while the row above it classifies the index withdrawal as independent
  of the boundary; the exception is now named, with the receipt field carried.
- **Narrowed in place.**  B2-MARKS-O listed the side names among the
  capabilities the O separation uses, and its own falsifier — "a separation
  that survives removing the names" — fired at Challenge 3.  The narrowing is
  now written into that entry and noted at the paper's C2-6 row, and
  B3-O-ALREADY-MET's attribution sentence now names the Challenge 2 receipt's
  price field rather than the ledger entry.
- **Corrected.**  B3-THREE-MINIMA attributed the merge of the two further-mark
  points to the side exchange alone, which does not carry one regime to the
  other; it is the class key, the side exchange composed with a mark renaming.
- **Corrected.**  Section 9's restatement of the Challenge 3 second reading
  dropped the token-forgetting clause and asserted unrestricted agreement; it
  now names the clause and says which direction is by unfolding and which is
  prose.
- **Corrected, a docstring.**  `one_step_minima` said it works over the
  one-step candidates only while its filter also admits the null point; the
  docstring now says both and why.  No receipt carries a docstring, and all
  five regenerate byte-identically.

Carried, with reasons: the Challenge 3 receipt's `boundary_dependence` text,
its `points_satisfying_with_grammar_change_only` key, the C3-3 scorer's
judgment-vocabulary conjunct and its weaker Python proxy, and the Challenge 3
`STATUS.md` row that says "same" for the label-keeping candidate under O.  All
lie in `code/boundary/challenge3.py` or in a frozen `STATUS.md`, and repairing
them would regenerate a closed rung's receipt or edit a closed rung's status.
The paper carries the correction for each.

Declined: nothing.

## 2026-09-05, Challenge 4 exact-head review repair

Nine surviving findings from the review of `ea3da12c`, all `should_fix`, two of
them one defect seen from two sides.  The frozen `challenge4/PREDICTIONS.md` was
not touched, no prediction changed status, and no computed result of the rung
moved.  What moved is what the prose and the receipt claimed about those
results.

- **Proved, not narrowed.**  Three prose sites, the rung's status row, and two
  ledger entries said the boundary separates neither of the two pairs of marks
  that share a side and cited `crossRetained_marks_share_a_side`, which states
  it of marks 0 and 2 only.  The other such pair is marks 1 and 3.  The
  companion `crossRetained_other_marks_share_a_side` now states it of that
  pair, one line, immediate from the two evaluations already in the file, so
  the sentence is proved as written rather than weakened to fit.  The axiom log
  was regenerated deliberately, 138 to 139 reports, with no injection live.
- **Withdrawn.**  "Which is proved rather than computed", in the same sentence:
  the receipt's `base.separable_mark_pairs` computes both exclusions, so the
  contrast was false in the direction that flatters the proof.  The sentence
  now says the receipt computes it and Lean proves it.
- **Corrected.**  The boundary's price table said two of the five declared
  whole properties are not formulable without the boundary; the receipt's own
  capability text says every one but the index and the tag properties, which is
  three, and the paper's own section 5.16 row and the ledger say three.  The
  third is the label-and-side property, whose body reads the placement.  The
  table now says three and names which.
- **Scoped.**  B4-WITNESS-CLAUSE claimed the witness list is empty "at every
  point that fails the requirement".  The census is computed only at the base
  and the eight one-step points — nine rows per reading — and the 192 point rows
  carry no witness column at all; under U 42 points fail the requirement and
  eight of them carry a census.  The entry now says what is computed.
- **Corrected, in this rung's own receipt.**  The Challenge 4
  `boundary_dependence` field repeated verbatim the defect the rung recorded
  itself as correcting: its fifth key read "every separation result of the
  rung" with no exception, contradicting the key immediately above it, which
  classifies the withdrawal of the mark permutations — a separation result of
  this rung, and the unique satisfying one-step point under U — as independent
  of the boundary.  It also omitted the grouping square's cells, which the
  paper's row and the status include.  The key now carries both, and
  `receipts/challenge4.json` was regenerated deliberately, 795554 to 795960
  bytes, with no injection live.  The field is this rung's own, so regenerating
  it closes no other rung's receipt; that is why this one is corrected where
  the Challenge 3 field is carried.
- **Corrected.**  B4-GROUPING-IS-METATHEORY was the only one of the ledger's
  entries with no **Axiom report** field, which the ledger's header and the
  seed's section 9 require of every entry; it now reads "not applicable", as
  the other Lean-less entries do.
- **Reworded, and the earlier claim narrowed.**  "Internal designation", a
  second sense of a word section 1 reserves for current-state designation, was
  reintroduced by this rung in `challenge4.py`'s capability text for the
  withdrawal of the mark permutations and in the `Challenge4.lean` doc comment,
  and reached the receipt three times — while the rung recorded that every use
  in the run's own prose had been reworded.  Both now read "internally
  available", the receipt carries the phrase nowhere, and the sweep claim in
  `challenge4/STATUS.md` is narrowed to the documents it actually covered.
  `challenge3.py` keeps the phrase and is carried with that rung's other items,
  its repair regenerating a closed rung's receipt.
- **Relabelled DEFINITION-level.**  The reduction of the whole sense to the
  Challenge 3 sense was presented as computed and counted among C4-8's content.
  At the Challenge 3 configuration each whole is a single mark, and
  `group_carrying_automorphism`'s set test is then
  `mark_carrying_automorphism`'s mark test over the same list of automorphisms:
  the agreement is true by unfolding, and the frozen falsifier "the two senses
  disagreeing at the Challenge 3 configuration" cannot fire.  Definition 52,
  the C4-8 basis in the paper and in the receipt, and B4-REQUIREMENT and
  B4-TWO-SENSES now say so, and C4-8's content is the 192-point census and the
  parting points.  C4-8 remains HIT; what changes is what it is a hit on.
- The paper's Lean counts move from 138 to 139 with the companion theorem, and
  the Challenge 4 receipt's recorded size from 795554 to 795960 bytes.  Both
  regenerations are recorded as rows in `MANUAL.md`, and the stale-receipt
  failure was observed before the regeneration rather than assumed.

Carried, with reasons: `challenge3.py`'s capability text carrying "internal
designation", alongside that rung's already-carried items, for the same reason
— repairing it regenerates a closed rung's receipt.

Declined: nothing.

## Challenge 5, the caller retains `<<a|>|>`

Session of 2026-09-05, opened at `75b7ed1a`.  The frozen
`challenge5/PREDICTIONS.md` was committed alone at `67d3e320` before any
Challenge 5 code or proof, and is never edited.

**Added, with reasons.**

- **A third reader bound** (definition 59).  Both readers the run had refuse
  the caller's inscription by name, neither reading an item on a side that is
  itself a whole.  The new reader takes an item to be nothing, one mark, or one
  whole, to a declared depth of two, and refuses a deeper item by name; the two
  narrower readers are left refusing so that what forced each widening stays
  visible.  The split of a whole's body at its own bar counts nesting levels,
  because a body may itself contain bars and a regular expression over the text
  cannot find the right one.
- **A declared four-member policy space** (definitions 61 and 62), because
  what an admission does with an item that is a whole is not decided by the
  admitted boundary and the run must not decide it silently.  Three
  capabilities for policies and a fourth for the naming coordinate; counts
  `0, 1, 1, 2`.
- **The one-step rule is stated in capabilities and not in coordinates**
  (definition 62), and Challenge 4's identity of the two counts is **narrowed**
  to that rung's space.  The recording policy moves one coordinate and uses
  two capabilities, so the two numbers part for the first time; the seed
  requires a candidate called one step not to bundle, so the capability reading
  is the one kept.  The receipt reports both readings at every point, and the
  key `one_step_iff_one_coordinate_moved` is false by design rather than by
  accident.
- **A second state type** (definitions 63 to 67): the deep regime, one address
  per admitted mark, with its admission event `AdmitAt`, its replay, its
  flattening onto a regime, the level exchanges, and the permitted renamings at
  depth.  It is available only under the recording policy.  Flattening is not
  injective, which is the rung's central fact.
- **The naming coordinate** (definition 68), because reading O names the
  outermost sides and says nothing about the inner ones, and the run must not
  read a decision into the seed's one exception that the exception does not
  make.
- **A declared 144-member domain of inscriptions, and a sameness relation on
  policies over it** (definition 69).  This is the first quotient the run takes
  over a function rather than over a state, and it was forced: the two one-step
  policies retain isomorphic states at the caller's own inscription, so a class
  key read there alone reports one class where the enumeration finds two and
  understates a tie the seed requires to be retained.  The defect is
  demonstrated by injection and by a test in both directions.
- **Eight collateral facts and a second measure** (definition 70), with the
  facts that take the same value at every point of the space **named in the
  receipt**.  The measure counts facts and not independent facts, and rather
  than re-weight it the run reports where it counts one thing twice.  That is
  the general form of a Challenge 4 review finding, made into a receipt key
  instead of a repair of a closed rung.
- **Thirty-eight Lean theorems** (`Challenge5.lean`), with the axiom log
  regenerated deliberately from 139 to 177 reports, no injection live.
- `research/boundary_seed/challenge5/PREDICTIONS.md` and `STATUS.md`,
  `code/boundary/challenge5.py`, `run_challenge5.py`, `tests/test_challenge5.py`,
  `receipts/challenge5.json`, the pin in `verify_pins.py`, the module in
  `tests/test_lean_gate.py`, the mypy entry in `pyproject.toml`, and the
  registration of the runner and the test count in the research job.

**Changed, with reasons.**

- `code/boundary/challenge3.py`: `minima` and `one_step_minima` take a
  defaulted `predicate` naming the row key that says whether a candidate
  answers the rung's demand.  Challenge 5's demand is the caller's retention
  and not a separability requirement, and reusing the word `satisfies` for a
  second predicate would conflate two things the run keeps apart.  The
  parameter is defaulted, no earlier rung passes it, and the Challenge 0 to
  Challenge 4 receipts regenerate byte-identically, which is checked.

**Repaired, from the review of Challenge 4.**

- The 5.13 results row for the side exchange said it "is a permitted
  automorphism of the configuration", which is false as written and is
  contradicted by the Lean theorem cited in the same row.  The row now says
  what the receipt computes: a side-exchanging automorphism exists and is the
  side exchange composed with the mark permutation `[1, 0, 3, 2]`, and
  `reflect_crossRetained_ne` supports it rather than contradicting it.
- Section 9's bare "which is proved" was attached to a conjunction whose first
  half is COMPUTED only.  It now says which half the receipt computes and which
  Lean proves.
- B4-NO-JUDGMENT-ADDITION said "the two marks that share a side", a definite
  description that does not uniquely denote — there are two such pairs — while
  the mark-level theorem covers marks 0 and 2.  The entry now names those marks
  and says where the other pair is covered.
- "A complete invariant" was used as an undefined technical term in the paper's
  5.13 prose.  It now reads "separates the four marks", with the scope stated.
- The boundary's price table counted six of the eight collateral facts as
  needing the boundary.  No receipt key, ledger entry, or test carries that
  number, so the count is WITHDRAWN from the row rather than left standing.
- B4-TWO-SENSES said the grouping-with-names point is among the parting points
  under both readings.  Under O it is not, satisfying the pointwise sense as
  well, so the clause is scoped to U.
- Three Lean theorems were listed as DEFINITION-level in the paper's section
  7.5 while the ledger gave them PROVED and counted them as content, which
  breaks the run's rule of one theorem and one label.  The paper's list was the
  error — the structurally identical Challenge 2 theorem is listed as content —
  so `exchangeWholesRegime_crossRetained`, `crossRetained_marks_share_a_side`
  and `crossRetained_other_marks_share_a_side` move to the content sentence and
  the ledger is unchanged.
- `MANUAL.md`'s Challenge 0 coverage-gate row recorded a failure whose recovery
  line had been withdrawn without replacement, so the row recorded no recovery.
  It now names the row that carries the recovery.
- Six advisories in `code/boundary/challenge4.py` and five in
  `challenge4/STATUS.md` are **carried** with their reasons in
  `challenge5/STATUS.md`: repairing them regenerates a closed rung's receipt or
  edits a frozen status.  Three of the five are answered by this rung's own
  results rather than by an edit, and the sixth code advisory — two clause
  statuses equal by construction — is answered by this rung's
  `collateral_facts_agreeing_everywhere` key.

**Live failures and repairs during the rung**, recorded rather than smoothed:
the reader's depth allowance was off by one on its first run and refused the
caller's own inscription; the declared domain was nine members instead of 144;
the receipt byte-identity test fired when the order census was restructured; a
`git checkout` of the root Lean module during an injection reversal dropped the
whole rung's audit lines for the second rung running, and the audit-totality
check named all thirty-eight theorems; and a decision procedure was offered a
goal carrying the reading as a free variable for the third rung running.  Each
is in `challenge5/STATUS.md`, and the gate events are rows in `MANUAL.md`.

Declined: nothing.

## 2026-09-05, Challenge 5 exact-head review repair

Eleven surviving findings, one `blocking` and ten `should_fix`, two of the ten
being the same defect from two sides.  The frozen `challenge5/PREDICTIONS.md`
was not touched.  One prediction changed status — C5-1, HIT to PARTIAL, on an
ordinal the frozen file gets wrong — and no computed result of the rung moved.
No Lean theorem was added, removed, or reproved, so `lean/axioms.txt` was not
regenerated.

**Repaired, from the review of Challenge 5.**

- **WITHDRAWN, and it was the `blocking` finding.**  "The two cost measures
  select different minima **for the first time in the run**" is false.
  `receipts/challenge3.json` records `readings.O.measures_agree_on_minima`
  false, B3-TWO-MEASURES says "under O they do not" in words, and the paper's
  own section 9 says so four paragraphs above the claim; Challenge 4 agreed
  under both.  What the three receipts support is that this is the first rung
  at which the measures part under **both** readings, and that is what the
  paper's 5.18 and section 9, B5-MEASURES-PART, `challenge5/STATUS.md` and the
  test comment now say.  The narrower claim is not a receipt leaned on: the
  comparison is read off the earlier receipts' own key.
- **Corrected.**  Three rows of the paper's section 7.6 reported "none" for
  theorems `lean/axioms.txt` reports as `[propext]`: `nestedRetained_depth`,
  `flatRetained_depth`, and `flattenAddress_exchangeAt_succ`.  The build log is
  the authority and the cells now match it.  The remaining thirty-five rows of
  that table were checked against the log mechanically, not by eye, and agree.
- **Narrowed.**  Section 9 and the 5.17 evidence cell said a mark's depth is
  invariant under **every** permitted renaming "which is proved", while
  `depth_invariant_under_exchange` covers level exchanges only and the
  mark-permutation half is `test_no_permitted_renaming_moves_a_mark_depth`, a
  bounded computation at one two-mark state.  Both now split the halves, in the
  words B5-DEPTH-TWO-SENSES already used, and the evidence cell cites the test.
  The prose is weakened rather than the proof stretched.
- **Scoped.**  The address-orbit row gave 4 / 2 / 1 with no scope; those are the
  recording policy's numbers, and at the two one-step policies the same key
  reads 2 under U and 1 under O.  The paper's 5.17 row, section 9's sentence,
  `challenge5/STATUS.md`, and B5-NAMING now name the policy.  The computation
  was already scoped; the prose was not.
- **Scoped.**  Section 5.17 said the U-versus-O price "is one capability per
  level", which sections 5.19 and 10 record as not computed and not settled by
  the two-level result.  It now says what holds at the two declared levels and
  points at the open item.
- **Repaired, and now computed.**  The further-mark probe decided its answer
  with the conjunct `point.policy == POLICY_ADDRESS` — the policy's own name —
  and its `because` text denied a length-two address the same object reported.
  It now decides on `deepest_place_the_policy_names`, the longest address a
  policy's own admissions produce over the declared 144-member domain: one at
  each one-step policy, two at the recording one.  The recorded address is
  reported beside it as `recorded_at_the_requested_place`, and the text no
  longer contradicts it.  The answer is unchanged; what changed is that it is
  read off a census.  With it, `what_the_caller_asked_for_costs` and
  `what_the_caller_asked_for_is_one_step` join
  `price.fields_declared_not_computed`, because which policy the demand names
  is computed and what it costs is definition 62's declared count.
- **Corrected.**  The receipt's declared text for the second measure described
  all eight collateral facts as facts about the caller's retained whole, which
  definition 70 contradicts: four are, two are censuses over the declared
  domain, one is about the closed grammar, one about the reading.  The constant
  and its comment now say what definition 70 says.  No measure value moves.
- **Added, because it was load-bearing and unnumbered.**  The declared
  presentation token of an opaquely admitted whole is one of the rung's three
  recorded declarations and is the ONE collateral fact separating the two tied
  minima, so the rung's unpredicted result rests on it; it had no numbered
  definition and no ledger entry.  It is now **definition 71**, cited from
  definition 61, an assumption of B5-POLICY-SPACE, and named in
  B5-MEASURES-PART as the fact that parts the measures.  It is numbered after
  definition 70 rather than beside 61 because renumbering would move every
  citation of definitions 62 to 70; definition 62 already forward-refers to
  definition 68, so a forward reference is the established shape here.
- **Corrected, and both frozen ordinals scored.**  The paper, this rung's
  status, `challenge5.py` and `presentation.py` called the new reader bound the
  third *widening*.  The run has three reader bounds and two widenings: the
  Challenge 1 bound was declared and not widened.  `challenge4/STATUS.md`, the
  frozen C4-X, B5-READER and this log already said "second"; the four wrong
  sites are corrected.  The receipt now carries the census —
  `reader.reader_bounds_declared` and `reader.widenings_of_the_reader_bound` —
  and **both** frozen files are scored against it rather than one being left
  unread: C4-X's "a second" HITS, and C5-1's "a third" MISSES, which makes C5-1
  PARTIAL.  Scoring only C4-X would have reproduced the defect one file over.
  The frozen files are untouched and the miss is recorded next to its value in
  the receipt, in `challenge5/STATUS.md`, in the paper's 5.18, and in
  B5-READER.
- **Corrected.**  B4-X was carried OPEN with "none yet" evidence after this rung
  scored it PARTIAL with a clause MISSED, against the run's own convention in
  B0-X and B1-X.  It now reads SCORED at Challenge 5: PARTIAL, names the six
  clauses that hit and the "exactly one member" clause that missed with its
  value, and cites `scores.C4-X` and the tests.
- Five tests were added — the depth census, the nameability predicate in both
  directions, the probe's reported address, the one-widening census with both
  ordinals, and the direction in which C5-1's ordinal would hold — taking the
  suite from 400 to 405, and `receipts/challenge5.json` from 123522 to 127455
  bytes.  The stale-receipt failure was observed before the regeneration rather
  than assumed, and both are rows in `MANUAL.md`.

Carried: nothing new.  The Challenge 1 to Challenge 4 items already carried in
`challenge5/STATUS.md` are unchanged.

Declined: nothing.

## 2026-09-05, Challenge 5 second exact-head review repair

Eight surviving findings, one `blocking` and seven `should_fix`.  The frozen
`challenge5/PREDICTIONS.md` was not touched.  **No prediction changed status**
and no computed result of the rung moved: one clause of the frozen C4-X that
was computed and reported without a verdict is now scored, and it HITS.  No
Lean theorem was added, removed, or reproved, so `lean/axioms.txt` was not
regenerated.

**Repaired, from the second review of Challenge 5.**

- **Corrected, and it was the `blocking` finding.**  Definition 59 still opened
  "The third and last widening of this run's reader", the one site the previous
  repair's own account claimed to have corrected.  The receipt's census says
  three reader bounds and two widenings, section 5.17's own bolded lead,
  B5-READER and `challenge5/STATUS.md` all say "the second widening", and
  `scores.C5-1`
  scores the frozen "a third" MISSED on exactly that wording.  The definition
  now reads "The third reader bound of this run, and the second widening of its
  reader — the Challenge 1 bound was declared and not widened".  **"and last"
  is dropped as well**: nothing in the rung establishes that no later widening
  occurs, and the same definition says in its next sentence that the bound "is
  a declaration too and not a limit".
- **Corrected, second surviving site of the same ordinal.**  The `NestedWhole`
  docstring in `presentation.py` called the nested reader "the third declared
  widening of the metatheory", five lines below a module docstring that already
  said "the second widening".  It now says "the run's third declared reader
  bound and its second widening of the reader", and "and last" is dropped from
  the module docstring for the reason above.  Neither edit touches a receipt
  value.
- **Narrowed.**  B5-CLASS-KEY gave status COMPUTED to a conjunct that is a
  superlative about the run's own history — "the first quotient the run takes
  over a FUNCTION rather than over a state" — with no receipt key, census, or
  test behind it, which is the shape of the ordinal defect above.  Nothing in
  this rung reads an earlier one.  The sentence is now recorded as a **reading**
  of the earlier rungs' own class keys, each of which pairs a declared structure
  with the canonical key of ONE retained state, and is kept out of the COMPUTED
  status; definition 69 and `challenge5/STATUS.md` say the same.
- **Scored, the clause that was computed and left without a verdict.**  The
  frozen C4-X carries eight clauses and `scores.C4-X` gave seven of them a
  status: "and the boundary within a side will not be visible without a new
  declaration" was reported only as the bare fact
  `points_where_the_nesting_is_internally_visible`, consulted by no verdict, so
  the tally of "six clauses HIT" scored seven of eight clauses.  The scorer now
  computes `nesting_not_visible_without_a_declaration_clause_status` from the
  same census — the nesting is internally visible at no point of capability
  count one, under either reading — folds it into the verdict, and the count is
  **seven** in B4-X, the paper's 5.18 and this rung's status.  The clause HITS,
  so no miss was hidden; the scoring was simply not total.  Its negative
  direction is `test_c4x_misses_when_a_one_step_policy_sees_the_boundary_within_a_side`,
  and C4-X's own status is unchanged at PARTIAL.
- **Corrected.**  B5-INERTIA gave PROVED to "any deep history keeps the reading
  and the datum" while its Lean theorem field named four theorems and not
  `BoundarySeed.deepReplay_initialDatum`, the only one covering the datum half,
  and its axiom-report field enumerated exactly those four.  The theorem is
  added to the entry and the axiom report extended to cover it, so every
  conjunct of the entry's PROVED status names its theorem in the entry.  The
  theorem itself is unchanged and was already audited.
- **Relabelled DEFINITION-level.**  `depth_determined_by_the_key` was labelled
  COMPUTED and counted as C5-6's content, with a falsifier that cannot fire.
  It is true by unfolding: the declared serialization carries every address,
  every permitted renaming keeps each address its length, so equal keys force
  equal depth signatures — and the receipt bears it out, the fact holding at
  all eight points of each reading, the refusing base included, so it never
  separates one candidate from another and never enters the second measure.
  The clause is now DEFINITION-level and reported apart, exactly as the grammar
  clause of the same prediction already was, and C5-6's content is its
  contingent half: the depths a policy can hold, `[1]` at every one-step policy
  against `[1, 2]` at the recording one.  The falsifier that cannot fire is
  dropped from the ledger with its reason recorded, and the paper's 5.17 row
  stops attributing the key to the recording policy, the key being true at
  every point.
- **Corrected, one theorem and one label.**  `flatten_nested_eq_flat` and
  `flatten_nested_eq_admitted` were called DEFINITION-level in one paragraph of
  the paper's section 7.6, omitted from that section's DEFINITION-level list,
  and given PROVED in B5-NESTING-INVISIBLE.  Both are `rfl`.  They now appear
  in the list, and "that the two flatten alike" moves out of the ledger entry's
  PROVED clause into a DEFINITION-level one, leaving
  `flattenDeep_exchangeLevel_succ` and
  `no_flattened_property_separates_the_nesting` as its PROVED content.  This is
  the defect the Challenge 4 review repaired under the same rule.
- **Scoped.**  The receipt's own C5-7 evidence string still gave the
  address-orbit numbers 4 / 1 / 2 with no policy scope — the recording policy's
  numbers — which is the defect the previous repair scoped out of the paper's
  row, section 9, this rung's status and B5-NAMING, and the receipt is the site
  it missed.  The string now names the recording policy and reports what the
  same key reads at the two one-step policies beside it.  No value moves.
- One test was added, the negative direction of the newly scored clause, taking
  the suite from 405 to 406 and `receipts/challenge5.json` from 127455 to
  128086 bytes.  The stale-receipt failure was observed before the regeneration
  rather than assumed, and both it and the test-count grep are rows in
  `MANUAL.md`.

Carried: nothing new.  The Challenge 1 to Challenge 4 items already carried in
`challenge5/STATUS.md` are unchanged.

Declined: nothing.

## 2026-09-05, continuation stage 1 predictions frozen

`continuation/stage1/PREDICTIONS.md` committed before the branch's first
stage-1 code-or-proof commit, sha256
`ac401dafbfa5072f04b6ab532992eae41391f87b6fe4441592b86804c4bf8313`, with
`.gitattributes` extended to mark `continuation/*/PREDICTIONS.md` `-text`.  The
frozen file discloses, in its own text, the four numbers the writer had
computed in scratch against the tree's own committed code before freezing — the
branch counts, the first challenge, the undemanded pairs on the further-mark
branch, and the arithmetic of the node bound — so that a reader can discount
the corresponding hits to zero.  That disclosure is sharper than the earlier
rungs gave and is the reason the near sweep below is weak evidence.

## 2026-09-05, continuation stage 1: the branches, the generators, and the bounds

The seed's autonomous continuation opens.  This stage declares, for each
surviving branch under each reading, the weakest deterministic challenge
generator the run can justify from that branch alone, and the resource bounds
the rounds will run under; **it runs no round**, adopts no candidate, admits
nothing, and declares no event kind.

Added: `code/boundary/continuation1.py` with definitions 72 to 82,
`run_continuation1.py`, `receipts/continuation1.json`,
`lean/BoundarySeed/Continuation1.lean` with twenty-eight theorems,
`tests/test_continuation1.py` with ninety-four tests, paper section 6 with its
four parts, paper section 7.7, the ledger's `S1-*` entries, and the stage's
registration in the research job.  The ledger's ID convention is extended:
`B<challenge>-` for the mandatory sequence, `S<stage>-` for a continuation
stage.

What the stage found, in the order it was derived:

- **The branch set is six under U and five under O.**  The run adopted nothing
  at any rung, so the base branch is what stands and every other declared
  branch adopts exactly one retained tied-minimum class of one closed rung.
  The minima are recomputed from the closed rungs' own modules, not restated,
  and a test holds the recomputation to their committed receipts.
- **The branch quotient keeps the two policy branches apart although their
  configurations agree.**  Both retain one mark on one side and have the same
  least key, so a key read at the configuration alone reports five branches and
  four — one short under each reading.  The key carries the policy's own
  Challenge 5 class key, which is the defect that rung's domain-wide key was
  written to avoid, met again one level up.
- **The generator of capability count zero emits nothing, so the minimum is
  taken among the generators that emit**, exactly as Challenge 5 took its
  minima among the policies that admit.  That minimum is one under both
  readings.
- **The two counts of one step part again.**  The state-reading source moves
  one coordinate and uses two capabilities, as the recording policy did at
  Challenge 5, so Challenge 5's parting is not an accident of that rung's
  space.
- **A tie under U and none under O.**  On the further-mark branch the grouping
  carries a third tag no caller whole introduced, so a pair remains that was
  never demanded; the demand generator emits there and nowhere else, and two
  tied classes are retained.  Under O that branch does not exist, the Challenge
  3 minimum there being the null point.
- **The first challenge is `<|b>`** — one mark at depth one, a further mark and
  not a deeper nesting — and it is the same on every branch and under both
  readings.  The generator that names it reads no component of any branch,
  which a census over every ordered pair of branches computes and which the
  state-reading source fails under.
- **The round bound is four, computed, and short of the seed's fifteen.**  The
  node ceiling of one thousand is a declaration and the branching bound of
  three is read off the closed rungs' own minima; that four is the largest
  round count fitting the ceiling, and that fifteen does not fit, are proved.
- **The requirement of Challenge 4 parts the branches**: unresolved at three of
  the six under U, met at one, and gone at the two policy branches, whose
  configurations hold fewer than two retained wholes.  Disappearance is one of
  the fates the seed lists and is recorded rather than read as satisfaction.

**One prediction MISSED and is recorded next to its value.**  The frozen S1-6
asserted that the run's census of functions returning an event would find none
in this stage's module.  It finds one, `inherited_history`, which reads the
recorded caller history each branch replays.  The clause is scored MISSED, S1-6
is PARTIAL, and the code is **not** changed to make the clause true: what the
census cannot see is recorded beside the miss instead, in the receipt's
`events_named_by_this_stage` — it reads a return annotation and cannot tell a
function that names the events of a recorded history from one that issues a new
event, so a clean census would not have been evidence either.  The frozen file
is untouched.

C5-X is scored PENDING with four of its five clauses HIT: the frontier export
is the work of the stage that runs the rounds, and its clause is the one that
keeps the prediction open.  The clause about importing undeclared
object-language structure is scored on the substitution census, which is what
the frozen words name, and not on this stage's own function census, which is
S1-6's clause; the two are kept apart rather than one verdict being carried
into the other.

## 2026-09-05, review repairs carried into continuation stage 1

Fifteen advisories arrived from the review of Challenge 5.  Each is actioned or
carried with its reason in `continuation/stage1/STATUS.md`; the repairs that
lie in a living document or in apparatus are listed here.

- **Section 7.6's partition is now total.**  Eleven theorems lay in neither the
  DEFINITION-level list nor the content sentence, `deep_no_event_follows` among
  them, which the ledger already called DEFINITION-level — one theorem with a
  label in the ledger and none in the paper.  Every theorem of the table now
  lies in exactly one half, and the two non-fixing theorems are counted as
  content by the rule section 7.5 states for the structurally identical
  Challenge 4 pair.
- **B5-INERTIA now names the theorem for every conjunct of its PROVED status**,
  and the empty deep event-follows relation moves out of that conjunction into
  a DEFINITION-level clause, matching the paper.  Two earlier versions were
  wrong in two different ways and both are corrected.
- **B5-TWO-TIED-MINIMA's Challenge 4 comparison is out of its COMPUTED
  status**, in the words B5-MEASURES-PART already uses: it is read off the
  Challenge 4 receipt and is computed by nothing in this rung.
- **A word was missing from the `flatRetained_eq` gloss** in section 7.6; and
  the `depth_is_invariant_where_the_inner_side_is_not` gloss read as a
  biconditional where the theorem is one equality at two named states.  Both
  are reworded.
- **The within-whole order rows of section 5.17 carry a claim identifier and a
  policy scope.**  The receipt's `order` block is computed at the recording
  policy and carries no policy field; the census reads 116 there, 121 at the
  opaque policy and 108 at the discarding one, which a new test computes.  The
  new ledger entry is B5-ORDER, and the Challenge 5 receipt is not regenerated:
  the scope is stated in prose, and the second half of the row, that the order
  moves no state's class, is policy-independent and needs none.
- **Section 9 now scopes its minimum sentence** to the points that admit the
  caller's inscription, as the 5.17 row and B5-TWO-TIED-MINIMA do, and **records
  that no policy is taken** and the configuration is unchanged, which 5.19 and
  section 10 make a headline and the Challenge 1 paragraph of the same section
  already recorded for itself.
- **The rung's terminal sentence** says "at any policy of capability count one",
  the scope every other statement of it carries.
- **Definition 64** no longer reads as if the deep grammar belonged to the
  recording policy: it says which policy needs `AdmitAt` and states that the
  deep grammar is the policy-agnostic replay rendering the receipt uses at
  every admitting point.
- **Three C4-X clause statuses that were only ever asserted in the hitting
  direction now have their negative directions tested**, which is what the
  paper's blanket sentence about the scorer requires: the widening's price, the
  initial-datum clause, and the policy-space clause.  Adding the tests was
  preferred to narrowing the sentence.
- **Three injection rows that Challenge 5 owed are added to `MANUAL.md`**: the
  deliberate axiom-log regeneration from 139 to 177 reports, the found-live
  nine-versus-144 domain defect, and an injection of the collateral-fact
  agreement census, run at this stage and observed.  The free-variable
  recurrence count in the Challenge 5 row is corrected against what the rows
  actually record: Challenges 2 and 3, so Challenge 5 is the third occurrence
  and not the fourth.

Carried, with reasons, in the status: the six items in `challenge4.py` and the
items in `challenge5.py` and in earlier `STATUS.md` pages, all of which would
regenerate a closed rung's receipt or edit a previous rung's status.

## 2026-09-05, continuation stage 1: review repair at the exact head

Six advisories arrived from the review of the stage commit `68452c34`.  All six
are actioned; none is declined.  Every repair lies in this stage's own module,
tests, receipt or prose, so no closed rung's receipt is regenerated and no
frozen `PREDICTIONS.md` is touched.

- **S1-3 is re-scored against its frozen words and is PARTIAL.**  The frozen
  falsifier names "the capability count and the coordinate count disagreeing in
  this space".  They disagree — `one_step_iff_capability_count_one` is true and
  `one_step_iff_one_coordinate_moved` is false, the state-reading source moving
  one coordinate and using two capabilities — so the falsifier fired and the
  clause MISSED.  The scorer had required that same disagreement in order to
  score HIT, which is the falsifier inverted, and the negative test hard-coded
  the inversion.  Both are repaired: the clause hits only where the two counts
  agree, the receipt key is `counts_agree_clause_status`, and the miss is
  recorded next to its value in the evidence string in the shape S1-6 already
  used.  The reason for the repair is the rule the run has followed since
  Challenge 1: a frozen clause is scored on the frozen words and only those, in
  either direction.  **What does not change is the result**: one step is
  capability count one, the seed requiring a candidate called one step not to
  bundle, and the two readings part.  What changes is that the stage no longer
  reports a frozen clause as hit by the very fact that refutes it.  The
  ledger's restatement of the falsifier carried the same inversion and is
  corrected to the frozen polarity, with the miss recorded there; the paper's
  and the status page's "eight of nine hit" sentences become seven of nine with
  two PARTIAL, and the event census is no longer called the single miss.
- **The branch quotient is no longer credited with identifying the two
  further-mark points.**  `branch_candidates` forms one candidate per rung
  class, taking its first member, so `extra_mark_1` is never a branch and the
  further-mark branch is a singleton of `branch_classes` — the very key the
  paper, the results table, section 9, the status page and S1-BRANCH-KEY cited
  for the identification.  The identification is real and is Challenge 3's own
  quotient, one level down; all five places now say which quotient makes which
  identification and cite `branch_space.rung_minima.challenge3`.  The S1-1
  quotient clause had asked only that *some* class hold more than one member,
  which cannot see any of the three identifications the frozen text names; it
  now names all three and reads both quotients, and
  `test_s1_1_reads_both_quotients_the_frozen_text_names` fixes the direction
  that splitting the adopted class alone must MISS.  The reason: an evidence
  citation that does not carry the claim is worse than none, because a reader
  who checks it finds a singleton and cannot tell whether the claim or the
  citation is wrong.
- **Definition 81 no longer entails independence from constancy.**  It said
  that a generator whose emitted challenge is constant over the branch set
  "reads no component of any branch, state included", and the run's own receipt
  is a countermodel: under O the demand generator has
  `reads_nothing_of_the_branch: true` while its emitted demand is computed from
  the branch's configuration, and the same generator moves under U.  The
  entailment is withdrawn from definition 81, from definition 79, from
  `branch_substitution_census`'s docstring, from the declared-inputs sentence,
  from section 9 and from S1-READS-NOTHING, whose status is split: COMPUTED for
  the constancy over the declared branch set, DEFINITION-level for the
  independence, which is true by unfolding the generator's source and not by
  the census.  The receipt gains `generator_space.substitution_census_reach`,
  `test_constancy_over_the_branch_set_does_not_entail_reading_nothing` pins the
  countermodel, and the residual is listed in section 10.  **No computed value
  moves**: the enumeration generator's conclusion was true on other grounds all
  along, and what was wrong was the stated inference and the label on it.
- **Section 7.7's partition is now total, and names theorems.**
  `firstMissingFrom_ge` and `contains_cons_self` lay in neither the
  DEFINITION-level list nor the content sentence — the defect actioned at 7.6
  in the previous session, in the next section down.  Both halves now name
  theorems rather than descriptions and sum visibly to the table's
  twenty-eight: fifteen DEFINITION-level, `contains_cons_self` among them as
  one `simp` on a constructor, and thirteen content, `firstMissingFrom_ge`
  among them as an induction over an arbitrary record.
- **S1-NON-REPETITION's PROVED status covers only clauses that name a
  theorem.**  "The generator is a function of the presented record alone" has
  no Lean statement, and the Lean `firstMissing` takes a record *and* a bound;
  the clause moves into a DEFINITION-level one, true by unfolding, and the four
  proved clauses keep their four theorems.  This is the shape repaired for
  B5-INERTIA in the previous session.
- **S1-BOUNDARY-DEPENDENCE reads LIMITATION.**  The receipt's
  `boundary_dependence` block is five declared sentences that nothing computes,
  and every earlier rung's entry of the kind — B3, B4, B5 — reads "LIMITATION,
  a dependency classification of the run.  It is reported in the receipt and is
  not computed by anything."  This one now reads with them, and names
  `test_the_receipt_reports_the_boundary_dependence`, which is what holds the
  receipt to the declared block.

The stage-1 receipt is regenerated deliberately with no injection live, 210774
to 212495 bytes; the six closed-rung receipts report unchanged.  The suite
grows by four tests and the workflow's test-count grep moves with it.  The Lean
theorem set does not move, so `lean/axioms.txt` is not regenerated.

## Operator-directed completion of the stage-1 review repair

The existing repair was taken over after its writer stopped.  The remaining
C5-X evidence sentence and the test-module introduction still attributed
independence to the finite substitution census.  They now separate its
computed output constancy from the DEFINITION-level inspection of the
enumeration source's declared inputs, matching S1-READS-NOTHING.  The C5-X
score values do not move; its receipt explanation is regenerated deliberately
with no injection live.  B5-X now points to that pending stage-1 evidence
instead of saying no evidence exists.

The stage-1 runner is included in the explicit strict-typing file list.  The
paper's current suite count is corrected from 504 to 508, including 98 tests
of stage 1.  The status separates the original stage's gate record from the
takeover verification, discloses the additional operational review context,
and adds the seed's fifteen-question progress census with unresolved work
marked OPEN or awaiting a later stage.  No continuation round, stage-2
prediction, freeze or comparison is produced by this repair.

The completed repair passes 508 tests in 250.336 seconds with fresh 100% line
and branch coverage over ten source files, strict typing over 33 files, all
seven receipt replays, the seed and seven frozen-prediction pins, and a clean
205-report Lean audit.  The prose watchlist and identifier firewall also
return exit 0.  The status records each check's boundary, the firewall skip,
and the repository-wide gates not run by this scoped session.

## Continuation stage 2: null success and the exact resource frontier

Predictions were frozen in their own commit `20855969` before stage-2 code or
Lean. The stage recomputes every inherited state branch and minimum emitting
generator class, preserving seven U and five O lines. It declares an atomic
response space including inherited positive capabilities and recomputes
challenge validity rather than inferring it from supply inertia.

The run executes 26 U and 20 O successful attempts, with no accepted
augmentation. The additional U demand line exhausts its pairs after two null
responses. Eleven supply lines reach the explicit four-attempt frontier;
index 6, `<|<a|>>`, remains pending. The attempt cap is kept separate from four
accepted augmentations and the seed's fifteen-augmentation target. All
requirements, histories, candidates, minima and exact pending challenges are
exported. The paper, ledger and stage status record the finite scope and OPEN
continuation beyond it. Required questions 1 to 14 receive an updated census;
question 15 and comparison remain withheld.

The first regression caught a genuine replay defect: starting suffix replay
from an existing regime discarded the earlier supply witnesses and wrongly
refused positive occurrence candidates. Full origin history plus suffix now
replays from genesis; policy origins use the existing checked flat rendering.
The candidate rows changed, while null minima and line counts did not.
Thirty-six new tests exercise nontrivial demand validity, all inherited
generator roots, tie retention, history corruption, resource frontiers and
positive-candidate supply provenance. Thirteen scoped Lean reports bring the
audit to 218. The fresh build rejected the stale log before deliberate
regeneration; no receipt was regenerated during a live injection.

S1-X is now PARTIAL: its demand-generator omission and no-response terminal
prediction are recorded as misses beside the values. C5-X's remaining frontier
clause is HIT within the stated finite computed scope. S2-1 through S2-6 HIT;
S2-X is PENDING. Frozen predictions, earlier status pages and earlier receipts
are unchanged. The configured verification procedures and operator apparatus
exposure are disclosed without any stronger provenance claim.

Final verification passes 565 unique tests, fresh 100.00% line and branch
coverage over eleven code files, strict typing over 38 files, the seed and
eight prediction pins, all eight deterministic receipt replays, the clean
218-report Lean audit, the unchanged prose-watchlist pin and identifier
firewall (one skip). Stage 2's receipt is 349533 bytes. The parallel coverage
workers initially exposed binary temporary shards to the source scan; the
gate rejected them, coverage combine consumed them, and the unchanged scan
then passed. The ordering correction and actual failed/recovered populations
are recorded in the manual. No scan exemption was introduced.

Final independent source review corrected the status's assertion that the
accepted-round-bound falsifier fires: the eleven lines reach the separate
attempt cap and accept zero augmentations. The assertion is withdrawn, with
S1-X still PARTIAL for its generator and terminal misses. S2-2 now checks that
a positive-cost candidate is actually valid, not merely present; one new
negative-direction regression raises the suite to 566. The affected 37-test
stage suite is rerun with coverage; the receipt stays byte-identical and its
scores, branch populations and minimum prices do not move.
