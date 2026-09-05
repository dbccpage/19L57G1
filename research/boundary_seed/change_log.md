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
