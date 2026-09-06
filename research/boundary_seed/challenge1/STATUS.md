# Challenge 1 — repaired status

`AuthorityEffect: None`.  Session of 2026-09-04, branch
`research/boundary-run`, opened from main at `7d2e6e86` with Challenge 0
in its repaired state (53 tests, line and branch 100%, 20 Lean reports);
then five exact-head review repairs in further sessions on the same
branch.

## Order of the work, as committed

1. `152ed096` `challenge1/PREDICTIONS.md` frozen, sha256
   `7cf17e56fffb4e45d4100750010265582fa921fabeed7fb1b84aa798f6e56dc7`,
   before the branch's first Challenge 1 code-or-proof commit.  The
   existing `challenge*/PREDICTIONS.md -text` attribute already covered it
   (`git check-attr` reports `text: unset`), so no attributes change was
   needed.  An earlier version of this line said “before any Challenge 1
   code or proof existed in the working tree”; git cannot establish that,
   and the sentence is withdrawn in favour of the committed order.
2. `8a8ed61e`: presentation layer, kernel extensions, Lean, receipt, tests,
   prose, registration, and injections.
3. `9a26a250`: the first review repair, the corrections listed under
   “Repairs” below.
4. `00acb2f7`: the second review repair, the re-score of C1-2, the bounded
   separation theorem, the membership-based designation fact, and the
   label corrections listed under “Repairs” below.
5. `44d2f1b7`: the third review repair: the split of B0-X's status, the
   prediction tally as a receipt fact with C1-1 and C1-6 reported
   DEFINITION-level, the current regime stated as genesis with the supply
   a fact of the history, and the separation of retained from kept, listed
   under “Repairs” below.
6. `78c4a96c`: the fourth review repair: C1-5 re-scored on the frozen
   words with the convention pinned, C1-3's content basis corrected,
   `reflect_step` relabelled, the exactly-one-side clause given its
   status, the second sense of supply removed, and the witness-search
   provenance narrowed, listed under “Repairs” below.
7. The fifth review repair commit, which adds this version of the file:
   B1-ONE-BOUNDARY narrowed to the candidate regimes, the frozen file's
   bare “designation” declared, `reflect_admitted` proved by `rfl` and
   relabelled DEFINITION-level, and the cited-test-name totality gate
   added, listed under “Repairs” below.  No status changed.

This history proves “committed before” only.  It cannot prove when any
untracked or off-tree code or proof was written.

## Provenance ceiling

Inherited unchanged: `SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE`.  The
sessions that closed and repaired this rung read nothing outside the write
root, the seed, and the contract sections the harness loads, but they are
instruments of the same kind as the one that declared prior exposure, and
the notes below record where a remembered shape was used.

## Results

Inscription `<a|>`, supplied after the close of Challenge 0.  Receipt
`receipts/challenge1.json`; full tables in `paper.md` section 5.

| | reading U | reading O |
|---|---|---|
| the supply of `<a|>` | presentation only: regime equals genesis, no judgment changes (DEFINITION for one supply, by unfolding `step`; PROVED for a history of supplies, `replay_supply_inert`; COMPUTED for the certified history) | same |
| the current state after the challenge | the current regime is genesis: the replay of the caller's history `[Supply(a)]`, in which `a` is supplied and nothing is admitted, a regime carrying no supplied component; the caller supplied and did not retain, so no admission event is the caller's and no candidate is current (DEFINITION rule; DEFINITION state, the n = 1 instance of `replay_supply_inert`, which is `rfl`; COMPUTED history, with `admitted_candidate_is_current` as membership in the candidate regimes) | same |
| a new admitted state | none is current; two certified admission candidates show what an admission on either side would do, refused without the prior supply (DEFINITION); in a candidate the admitted mark's judgment survives every later event of the Lean grammar (PROVED), a same-side re-admission is a no-op and a moving admission is refused (Python-only DEFINITION) | same |
| new holding judgments after a candidate admission | exactly one, `OnSide(0, s)`; the other side's does not hold; no name judgment (PROVED) | exactly one, `OnSide(0, s)`; the two name judgments hold as at genesis (PROVED for every history; the one-event step is DEFINITION) |
| the mark's profile | its side, nothing else (DEFINITION) | same |
| the two sides after one candidate admission | profiles differ (PROVED); the admission would take the sides from collapsed to distinct | profiles differ (PROVED); the sides were already distinct by name |
| the two candidate regimes (`a` on side 0, on side 1) | unequal (PROVED), each the other's reflection (DEFINITION: `reflect_admitted` is `rfl`); related by the permitted reflection: one class (DEFINITION for the one-mark relation, both halves by unfolding; COMPUTED for the general relation) | unequal (PROVED), each the other's reflection (DEFINITION); related by no permitted renaming: two classes (COMPUTED over the unpruned search with mark permutations; the Lean one-mark relation, raw inequality under O, does not relate them, PROVED) |
| “which side” as an internal fact | not one: no permitted-renaming-invariant judgment of the bounded domain separates the candidates (PROVED by `bounded_invariant_judgment_does_not_separate`, whose hypothesis is the bounded notion under U; COMPUTED over the eight-judgment domain) | one, once admitted: `OnSide(0, s)` separates them and every renaming is the identity at one mark (PROVED, COMPUTED) |
| the presentation convention (left is side 0) | invisible up to the permitted reflection | visible; the other convention's candidate is the reflection of the convention's candidate (PROVED) and is a second class, kept |
| the convention's candidate | `a` on side 0, selected by convention and admitted by nothing | same; the side-1 candidate kept as a certified branch |
| every continuation of one candidate reflects to one of the other | yes (PROVED, `reflect_replay`) | yes; this carries the second class without a second tower (PROVED) |
| an event follows from a candidate regime | none (DEFINITION: the relation is empty by declaration) | same |
| initial datum and reading | unchanged by every history (PROVED); by one event (DEFINITION) | same |
| new event kind or judgment form needed | none | none |

Boundary dependence: the supply's inertia, the admission discipline, the
rule that the current state is the replay of the caller's history, the
invariance of the initial datum and reading, and the empty event-follows
relation do not require the admitted boundary.  The one new judgment, the
profiles, the two candidates, the convention, and the class counts require
it and are not formulated after removing it.

What the challenge exercises, by the seed's list: supply (yes, the
`Supply` event of the read whole's mark); mention (yes, the token is named
by the supply and by every candidate admission, and a mention is not an
event); admission (examined: applied only inside certified candidate
histories, never by the supply, and never by the caller at this
challenge); current-state designation (yes: the current state is the
replay of the caller's history, the supply alone, and equals genesis; no
candidate is current); retention (probed by hypothetical later events on
the candidates, none admitted); observation (yes, one new `OnSide`
judgment in each candidate); side (yes, the presented side mapped by
convention); equality (yes, structural, and distinct from the isomorphism
relation).  An earlier version of this paragraph said “current-state
designation (yes, by the declared convention)” and designated the
convention's admitted candidate current.  That could not stand beside
“admission … never by the supply”: it turned a candidate from the run's
own enumerator into admitted state with no admission event from the
caller.  WITHDRAWN.

## Predictions scored

| id | label | status | note |
|---|---|---|---|
| C0-X | NOT FORCED | HIT | U half: genesis collapsed, every certified candidate not, with one supply and one admission and no new form; O half: sides distinct before and after, the only new holding judgment the mark's own side; scored against the candidates, on which the prediction is conditional |
| C1-1 | FORCED | HIT, DEFINITION-level | supply leaves the regime and every judgment unchanged; every clause is true by unfolding `step` (`supply_no_op`, `supply_preserves_holds`, and the n = 1 instance of `replay_supply_inert` are `rfl`), so the hit is by construction and is not counted as content, by the rule applied to C1-7; an earlier version counted it (`scores.C1-1.result_basis`, `tally`) |
| C1-2 | FORCED | PARTIAL | unsupplied admission refused; the admitted mark's judgment survives supplies, a same-side re-admission, and the hypothetical growth probe, and no accepted event moves or duplicates the mark: HIT (`facts_status`).  The frozen parenthetical “a re-admission of the same token on either side, which is designation and not duplication” predicts an accepted other-side re-admission, which the repaired kernel refuses by name; there is no after-state for the clause to hold in, so it is false as written and MISSED (`either_side_readmission_clause_status`, from the clause's own receipt fact `moving_admission_accepted_and_inert`).  The first review repair labelled it SHARPENED from the overall score; that label meant true-and-too-narrow at C0-5 and did not apply, and is WITHDRAWN.  PARTIAL, as C1-4 |
| C1-3 | FORCED | HIT | exactly one new judgment; other side false; names unchanged; supply adds none; counted as content, the one-judgment clauses resting on `admitted_onSide_true_iff`, `place_new_judgment`, and `place_other_side_false`, none by unfolding; the name clause, read per event as the frozen text has it, is `step_preserves_sideNamed`, DEFINITION-level, exactly as C1-6's parallel clause was scored, the induction `replay_preserves_sideNamed` being the rung's addition (`scores.C1-3.result_basis`); an earlier basis attributed the name clause to the induction, corrected, no status changing |
| C1-4 | FORCED | PARTIAL | U profiles differ; one class; no permitted-renaming-invariant judgment separates the candidates: HIT.  The clause “the admission is the only event in the history” is false as written: each candidate history is one supply and one admission, and a supply is an event by definition 5.  It was first scored HIT on the silently weakened reading “the only state-changing event”, which is now scored separately in the receipt (`only_state_changing_event_status: HIT`, `only_event_clause_status: MISSED`).  PARTIAL, as C0-4 was |
| C1-5 | NOT FORCED | HIT | the declared convention is the frozen one, left is side 0, which O names `near`, pinned piece by piece (`convention_clause_status: HIT`; declaring the other convention scores it MISSED, `test_c1_5_convention_clause_misses_under_the_other_convention`); two O classes; the other candidate is the reflection of the convention's candidate; both kept (`facts_status: HIT`); the clause “the designation is by convention and not by proof” is scored on the frozen words — the convention designates, that is selects, a candidate, and the regime under the other convention is the reflection of the designated one — from `selection_is_by` and `other_is_reflection_of_candidate` (`designation_clause_status: HIT`); counted as content, the two classes being COMPUTED over the unpruned search and the inequality PROVED, while `reflect_admitted` is `rfl` and DEFINITION-level (`scores.C1-5.result_basis`); the frozen bare word designation is read as the convention's selection, declared in the paper's section 1 and mirrored in the clause fact.  The first three repairs scored that clause MISSED as “current-state designation of the convention's admitted candidate” and reported PARTIAL; the frozen text contains no such words, and the run's withdrawal of that designation (definition 25) is a fact about the run, not a clause of the prediction; the earlier scoring is WITHDRAWN, recorded here next to its value, and the status moves PARTIAL to HIT |
| C1-6 | FORCED | HIT, DEFINITION-level | empty event-follows relation; datum and reading unchanged; no new form; the relation is empty by unfolding `EventFollows := False`, “unchanged by every event” is the step lemmas by unfolding (the history-level inductions are the rung's addition, not the prediction's), and the unchanged grammars are a census of the run's own declarations, a modelling decision as C1-7's, so the hit is by construction and is not counted as content; an earlier version counted it (`scores.C1-6.result_basis`, `tally`) |
| C1-7 | NOT FORCED | HIT by construction, DEFINITION-level | the regime type represents neither a second datum nor a second boundary, so `initial_datum_unchanged` cannot be reported false, and `marks == 1` is a proxy reading “the mark placed on a side” as exactly one placed mark, which the frozen text does not name; not counted as content; the modelling clause can only be falsified by a later challenge; whole-as-datum is OPEN for Challenge 5 |
| C1-X | NOT FORCED | PENDING | scored by Challenge 2 |

Two of seven scored predictions hit as content (C1-3, C1-5); three hit by
construction and are DEFINITION-level, not counted as content (C1-1,
C1-6, C1-7); two are PARTIAL (C1-2, C1-4); and C0-X hit in both
halves, as content, its profile clauses being PROVED (B0-X).  The
criterion, stated in the paper's 5.2 and in the receipt's
`tally.criterion`: a prediction counts as content only if at least one of
its hitting clauses, read literally, rests on a theorem outside the
DEFINITION-level lists of the paper's section 7 or on a computation not
fixed by a declaration alone; the DEFINITION-level list is declared in the
scorer and the counts are the receipt's `tally`.  An earlier version of
this table scored seven of seven; the first review repair five of seven,
with C1-2's parenthetical SHARPENED and C1-7 counted as a hit; the second
three of seven as content, counting C1-1 and C1-6 while excluding C1-7 on
the rule that also excludes them; and the third one of seven as content,
with C1-5 PARTIAL on a clause scored as “current-state designation”, words
the frozen text does not contain.  All four are WITHDRAWN.  The fourth
repair's re-score of C1-5 on its own words is the one status change across
the re-counts, PARTIAL to HIT, recorded next to its value above.  Each
PARTIAL row's facts hit and one of its clauses is false as written, scored
by its own receipt fact.  The frozen
file is untouched.  Five of the seven were labelled FORCED in the frozen
file; every FORCED hit follows from Challenge 0's definitions plus the
admission event that Challenge 0 already declared, and the two FORCED
PARTIALs each overstated an event-level clause.  The NOT FORCED C1-5 was
about a decision the run made, the declared convention, whose identity is
now pinned literally.  Git history establishes
that the prediction file was committed before this rung's code and
proofs; it establishes nothing about off-tree work and is not evidence of
insight.

## Where the run reached for a remembered result (declared reading 0)

- The shape of the answer to the seed's “presentation, admitted state, or
  observable distinction” question — presentation by one event, state by
  a separate event, distinction only after it — is the shape the
  instrument remembers from the sealed derivation's treatment of its own
  first supply.  The facts were computed and proved here; the framing was
  not re-derived.
- The presentation reader and the “left is side 0” convention were
  written from the instrument's habit of separating presentation from
  admission.  The convention's O-visibility and U-invisibility, and that
  the other convention's candidate is the reflection of this one, were
  derived here first and were not remembered.
- The first session's designation of the convention's admitted candidate
  as the current state was the instrument's habit, not a derivation; the
  review found it conflated supply with admission and the repair withdrew
  it.  Recorded here because it is exactly the kind of remembered move
  reading 0 warns about.
- The retention probes and the per-module generator census were written
  from the discipline the repository contract states, not from a
  remembered result.
- Nothing in the separating-judgment computation or the
  reflection-commutation theorems was remembered; the replay-level
  commutation theorem was written for the repair from the reviewers'
  falsifier.  The isomorphism witness search reuses the shape the
  Challenge 0 status already declared remembered, the brute force over
  renamings with tokens forgotten, and is not claimed unremembered; new
  to this rung are only its use as a witness or relation and the
  canonical-key agreement test.  An earlier version of this bullet said
  the witness was not remembered; narrowed.
- The SHARPENED label on C1-2's parenthetical at the first review repair
  was carried over from the shape of C0-5's general clause, where it named
  a clause that was true and too narrow; here the clause was contradicted,
  and the label was attached to the overall score with no clause fact.
  The second review found it; the repair scores the clause literally.
  Recorded because it is a remembered label applied where its meaning did
  not hold, which is the kind of move reading 0 warns about.
- The phrase “genesis with `a` presented”, written at the first review
  repair for the current state, described a regime by an event of its
  history; the regime type has no supplied component.  That is the same
  habit — carrying a history fact into the state — as the designation the
  first repair withdrew, and the third review found it.  Recorded as a
  remembered move.  Nothing else in the third repair was remembered: the
  content criterion is `PLAN.md`'s rule applied clause by clause and
  declared in the scorer, and the word kept for a candidate class was
  chosen against the seed's own two uses of retain.
- The cited-test-name gate added at the fifth repair is apparatus, and its
  shape — enumerate the citations, require each to resolve, fail in the
  direction the prose can drift — is the repository contract's, not this
  run's derivation; the reviewer proposed it in those terms and the run
  adopted it rather than deriving it.  Recorded because reading 0 asks for
  the reach as well as the result.  Its population, and the rule that a
  name which cannot be run is written in plain text, are this tree's.
  Nothing in the `rfl` proof of `reflect_admitted` was remembered: the
  reduction was checked by building it.

## Leftovers, for Challenge 2 and later

- Score C1-X: whether Challenge 2 admits two internal identities for the
  two wholes despite the shared glyph, and what the boundary alone
  distinguishes under each reading.
- Nothing is admitted at Challenge 1.  Challenge 2 “supplies and retains”:
  its first decision is what “retains” licenses — whether the caller's
  retention is the admission event, under which convention, and who pays
  — and it must not let the Challenge 1 candidates become current by
  inheritance.
- `Supply` carries the token only; the presented side is metatheoretic and
  is consumed by the convention only when an admission is formed.
  Challenge 2 must say whether `<a|>` and `<|a>` are two presentations or
  one presented twice, and must not let the Challenge 0 token-uniqueness
  rule turn the second whole into a same-side no-op or a refused moving
  admission silently: the kernel now refuses an admission that would move
  an admitted token, so a second whole with the same glyph on the other
  side is refused unless Challenge 2 gives it a distinct internal
  identity, loudly.
- The reader is bounded to one mark and one bar by declaration; Challenge
  2 extends the bound deliberately, and Challenge 5 must revisit nesting.
- Whether a whole on a side is a datum (C1-7's modelling clause) is OPEN
  until Challenge 5 asks it.
- C1-2's other-side clause is a recorded miss: Challenge 2 must not
  re-read a re-admission naming the other side as a designation; the
  kernel refuses it and the receipt says so.
- The Lean isomorphism relation `oneMarkRelated` is intended for one mark
  only and that adequacy is prose; under O it is raw inequality.  The
  general relation with mark permutations is Python, cross-checked against
  the canonical key to three marks, with no unbounded theorem.  A Lean
  statement that the permitted renamings of a one-placement regime are
  exactly the identity and, under U, the reflection is a candidate target,
  not attempted.
- Challenge 0's leftovers survive: no Lean statement of the equal-count
  law or the class-count closed forms; no unbounded canonical-key theorem;
  the O names have now been proved never to change but nothing yet makes
  them earn their keep beyond separating the two one-mark candidates.
- The freeze manifest protocol remains OPEN as recorded at Challenge 0.

## Repairs and live failures during the challenge

Recorded in `change_log.md` and as rows in `MANUAL.md`.  During the rung:

- The Challenge 0 generator census fired on the new candidate enumerator
  while it lived in the kernel.  The enumerator moved to the metatheory
  module and the census is now reported per module; the kernel reports
  none.
- The no-timestamp scan matched the substring `date` inside `candidates`;
  it was narrowed to whole words, which the review then found blind to
  snake_case keys (below).
- The first `lake build` did not elaborate `Challenge1.lean` because
  nothing imported it; the root now imports it, and `verify_lean.py` fails
  on any module under `lean/BoundarySeed/` outside the root's import
  closure, proved by injection.
- Five Lean proofs first failed because `simp only [replay, List.foldl]`
  unfolded past the induction hypothesis; they now step by a definitional
  `show`.  A drafting placeholder theorem was removed before the build.

The exact-head review repair, in a further session:

- Current-state designation withdrawn from the admitted candidate: the
  current state is the replay of the caller's supplied-only history and
  equals genesis; the candidates are kept as certified candidates,
  none current; the convention selects and admits nothing (paper
  definition 25, ledger B1-CURRENT-STATE, receipt `current_state`,
  `candidate_classes`, `convention.candidate_event`).
- C1-4 and C1-5 re-scored PARTIAL as above, mechanically, with both
  readings of each disputed clause in the receipt; C1-2's parenthetical
  annotated SHARPENED.
- The kernel refuses an admission that would move an admitted mark, by
  name, instead of absorbing it with the requested side discarded; a
  same-side re-admission is a no-op and is no longer called a designation;
  negative tests in both directions.
- `reflect_replay` and its corollaries added in Lean, with a Python
  replay-commutation test over 86 accepted histories; the ledger's
  history-level clause now rests on them rather than on the step lemmas.
- DEFINITION-level relabelling: the `rfl` and case-split lemmas, the
  permission halves of the two relatedness theorems, and the instantiation
  `no_event_follows_admitted` are DEFINITION in the ledger, the paper's
  section 7.2, and this file's Results table; “related by no permitted
  renaming” under O is COMPUTED, the Lean one-mark relation being raw
  inequality there.
- The freeze-order wording narrowed to what git establishes.
- The no-timestamp scan now splits snake_case keys, is shared with the
  Challenge 0 receipt test, and is proved by a planted `build_date` key.
- The axiom log regenerated deliberately, 49 to 55 reports; the workflow's
  test-count grep updated, 97 to 106.

The second exact-head review repair, in a further session:

- C1-2 re-scored PARTIAL: the frozen parenthetical's other-side half is
  scored by its own receipt fact, `moving_admission_accepted_and_inert`,
  false because the moving admission is refused; the SHARPENED label,
  attached to the overall score with no clause fact, is withdrawn.  The
  scorer's facts now accept a moving admission that is either refused or
  accepted and inert, and miss on one that is accepted and moves the mark,
  which is the frozen falsifier.  Negative tests in both directions, and a
  kernel-level probe showing the fact true only under an absorbing `step`.
- `admitted_candidate_is_current` computed as membership of the current
  regime in the candidate regimes, not as “has a mark”; a test with a
  caller history admitting another token shows the difference.  The
  receipt value is unchanged.
- `bounded_invariant_judgment_does_not_separate` added in Lean, with the
  bounded hypothesis the Python computation checks under U; B1-SIDES-U's
  bounded-domain clause now rests on it rather than on the
  global-hypothesis theorem, which closes less.  The axiom log regenerated
  deliberately, 55 to 56.
- C1-7 reported as HIT by construction, DEFINITION-level, with `marks == 1`
  named as a proxy; excluded from the content tally.
- One theorem, one label: the Challenge 0 `rfl`, unfolding, substitution,
  and case-split theorems relabelled DEFINITION-level in the ledger, the
  paper's 4.1 and 7.1, and the Challenge 0 status table; the n = 1
  instance of `replay_supply_inert` in B1-CURRENT-STATE likewise.
- The workflow's test-count grep updated, 106 to 109.

The third exact-head review repair, in a further session:

- B0-X's status split, one clause one label: PROVED for the profile and
  judgment theorems, DEFINITION for the declared history shape, COMPUTED
  for the unchanged-grammar clause, which `score_c0x` decides by comparing
  receipt keys and no Lean theorem covers; `sides_distinct_at_genesis_O`,
  the O “distinct before” theorem, added to the entry's Lean list with its
  report.  No result changed.
- The prediction tally made a receipt fact (`tally`, from a declared
  DEFINITION-level list and the statuses) and applied uniformly: C1-1 and
  C1-6 join C1-7 as HIT by construction, DEFINITION-level, not counted as
  content, with their bases in `scores.*.result_basis`; C1-3 is the one
  content hit and says why.  Tests in both directions, including a miss on
  a DEFINITION-level prediction counted as a miss and an unknown status
  refused by name.  No status changed.  The receipt regenerated
  deliberately, 24663 to 26687 bytes, with no injection live.
- The current state stated as the current regime, genesis, with `a`
  supplied in the caller's history and not in the state; “genesis with `a`
  presented” withdrawn from the paper, this file, and the ledger.
- Retained reserved for the placement tuple; a candidate class the run
  does not drop is kept, declared in the paper's section 1 beside the
  definition; the caller's “retains” stays quoted for Challenge 2.  The
  receipt's C1-5 evidence, the scorer's docstrings, a test's local name,
  and a Lean docstring reworded; no theorem or axiom report changed.
- The workflow's test-count grep updated, 109 to 111.

The fourth exact-head review repair, in a further session:

- C1-5 re-scored HIT: its designation clause is scored on the frozen
  words (the convention designates, that is selects, a candidate; the
  other convention's regime is the reflection of the designated one), from
  `selection_is_by` and `other_is_reflection_of_candidate`; the earlier
  MISSED clause, “current-state designation of the admitted candidate”,
  was scored on words the frozen text does not contain and is withdrawn;
  `admitted_candidate_is_current` stays a plain fact read by no clause.
  The tally follows mechanically: two content hits, two PARTIAL.
- The frozen convention pinned literally in the scorer (`declared`, its
  left side, the candidate event's side, and `side_0_name_under_O`, a new
  receipt fact), with a negative test that declares the other convention
  with its swapped candidate event and expects the clause MISSED; the
  pre-repair scorer reported facts HIT on the same facts.  The receipt
  regenerated deliberately, 26687 to 27943 bytes, with no injection live.
- C1-3's content basis corrected: the name clause, read per event as the
  frozen text has it, is `step_preserves_sideNamed`, DEFINITION-level, as
  C1-6's parallel clause was scored; the content rests on the three
  judgment theorems.  No status changed.
- `reflect_step` removed from the paper's DEFINITION-level list, its place
  branch being the PROVED `reflect_step_place`; that lemma and the two
  involution lemmas labelled PROVED in B1-REFLECT-COMMUTES.
- B1-SIDES-U's “exactly one side” clause given its status: PROVED as a
  metatheoretic statement (`admitted_onSide_true_iff` with
  `no_observation_at_genesis`), not an internal judgment of the closed
  grammar.
- The second, undeclared sense of “supply” (the caller providing any
  event) removed from the current-state rule and its falsifier.
- The provenance note on the isomorphism witness narrowed, above.
- The workflow's test-count grep updated, 111 to 112.

The fifth exact-head review repair, in a further session:

- B1-ONE-BOUNDARY narrowed: “every certified regime keeps the one initial
  datum and places one mark” is false of the current state, which is
  certified and places none; the ledger and the receipt's C1-7 evidence
  now say “every certified candidate regime”, which is the population the
  scorer reads, and add what the current state does.  No status change.
- The frozen file's bare “designation” declared beside the run's
  reservation of the word: section 1 now says the reservation is on this
  run's own prose, and that the frozen file's two other senses — a
  re-admission of an already admitted token at C1-2, the convention's
  selection at C1-5 — are each read in their own context and neither as
  current-state designation, on which reading C1-5's HIT depends.
  B1-CONVENTION-O, the kernel docstring, and the two receipt clause facts
  say the same.  No status change.
- `reflect_admitted` proved by `rfl` and relabelled DEFINITION-level, with
  `candidates_related_U`, whose other half is the permission by
  unfolding: the statement is true by unfolding, both sides reducing to
  the one-element placement, and the earlier `simp [reflect]` carried a
  `propext` the axiom log reported as content.  Both are added to the
  paper's 7.2 DEFINITION-level list and relabelled in B1-SIDES-U and
  B1-CONVENTION-O; their axiom reports are now none and the log was
  regenerated deliberately, 56 reports with two lines changed.  C1-5 stays
  HIT and counted as content on its computed clause and
  `admitted_candidates_unequal`.
- The injection record's two rows naming renamed tests repaired, and
  `tests/test_prose_citations.py` added: every backticked `test_*` token
  in the tree's Markdown, `SEED.md` excepted, must resolve to a test the
  suite defines.  It failed on exactly those two rows, and again on a
  planted citation, with a temporary-tree probe fixing the same
  direction.
- The workflow's test-count grep updated, 112 to 114.

## Gates run in the latest repair session

| gate | result |
|---|---|
| `verify_pins.py` | `pins ok: seed ba30bcd600d8 and 2 frozen prediction file(s)` |
| `unittest discover -s tests` | `Ran 114 tests`, OK |
| `mypy` (strict, tree pyproject) | `Success: no issues found in 18 source files` |
| `coverage` + `check_coverage.py` | `line 100.00% branch 100.00% over 5 files` |
| `run_challenge0.py`, `run_challenge1.py` | Challenge 0 receipt byte-unchanged (5553 bytes); Challenge 1 receipt regenerated deliberately (28363 bytes), then byte-identical on rerun; `git diff --exit-code -- receipts` clean after commit |
| `verify_lean.py` | `lean ok: 56 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; no theorem added or removed, the log regenerated deliberately because `reflect_admitted` and `candidates_related_U` lost their `propext` |
| `ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, … census matches its pin`; no regeneration |
| `tests/test_primitive_contact.py` | firewall passes |
| `ci/check_paper_citations.py` | cross-references resolve |
| injections | the cited-test-name check failing on the two renamed tests and then on a planted citation, the stale-receipt failure observed before the deliberate regeneration, and the stale test-count grep observed failing on the fresh log, all in `MANUAL.md`; the earlier rows stand |

## Next session

Open Challenge 2 fresh: read the handoff, the seed, `PLAN.md`,
`MANUAL.md`, and this file; write and commit
`challenge2/PREDICTIONS.md` with its own extrapolation before any code;
extend the reader's bound to two wholes deliberately; decide what
“supplies and retains” admits and who pays; decide how the shared glyph
relates to internal identity; score C1-X.  The current regime under each
reading after Challenge 1 is genesis; the caller's history is
`[Supply(a)]`, in which `a` is supplied and nothing is admitted.  The two
admission candidates (`a` on side 0, on side 1) are certified and kept as
branches — one class under U, two under O — and the declared convention
selects the side-0 candidate as the admission the inscription's presented
side would license, without admitting it.  Retained means the placement
tuple and nothing else until Challenge 2 decides what the caller's
“retains” admits.
