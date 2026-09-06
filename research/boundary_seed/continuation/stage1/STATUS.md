# Continuation stage 1 — status

`AuthorityEffect: None`.  Session of 2026-09-05, branch `research/boundary-run`,
opened with Challenge 5 in its second review-repair state (`27268b60`: 406
tests, line and branch 100%, 177 Lean reports).  One stage closed: the first
stage of the seed's autonomous continuation — the branches, the challenge
generator each of them justifies, and the resource bounds.  **No round is run.**

## Order of the work, as committed

1. `1b855b7e` `continuation/stage1/PREDICTIONS.md` frozen, sha256
   `ac401dafbfa5072f04b6ab532992eae41391f87b6fe4441592b86804c4bf8313`,
   committed alone before any stage-1 code or proof, with `.gitattributes`
   extended to mark `continuation/*/PREDICTIONS.md` `-text` (`git check-attr`
   reports `text: unset`).
2. The stage commit `68452c34`: kernel, Lean, receipt, tests, prose,
   registration, the Challenge 5 review repairs, and the injections below.
3. The repair commit: the six advisories of the review of `68452c34`, actioned
   in this stage's own module, tests, receipt and prose.  The frozen
   `PREDICTIONS.md` is untouched and its pin is unchanged; the stage-1 receipt
   is regenerated deliberately, and no closed rung's receipt moves.

This history proves “committed before” only.  It cannot prove when any
untracked or off-tree code or proof was written, and it is not evidence of
insight.  **This stage says more than that, and worse for itself**: the frozen
file names four numbers the writer had already computed in scratch against the
tree's own committed code before freezing — the branch counts, the first
challenge, the pairs the further-mark branch leaves undemanded, and the
arithmetic of the node bound.  Those hits are worth zero and the frozen file
says so.

## Provenance ceiling

Inherited unchanged: `SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE`.  This
session read nothing outside the write root and the seed, but the harness loads
the repository contract file **whole**, operating manual included, which is
wider than the five sections the seed's isolation clause names; and the session
is an instrument of the same kind as the one that declared prior exposure.  The
per-stage adversarial review channel, disclosed in the paper's section 0,
supplied this stage's advisory list; it supplied no definition, generator,
bound, or result.

## Results

Receipt `receipts/continuation1.json` (212629 bytes after the completed repair;
212495 before the remaining C5-X wording was narrowed, and 210774 as the stage
first closed); full tables in `paper.md`
sections 6.1 to 6.4.

| | reading U | reading O |
|---|---|---|
| declared branches | **6** (COMPUTED: the closed rungs' minima recomputed and held to their receipts, then the implemented branch quotient) | **5** (COMPUTED) |
| what the branch quotient identifies | the two withdrawals of the mark permutations, one declaration named at Challenges 3 and 4 | the Challenge 3 null minimum with the base; the further-mark class is no minimum here |
| what Challenge 3's own quotient identifies, one level down | the two further-mark points, one class, which reaches the branch set as one candidate — `extra_mark_1` is never a branch, so this is not the branch quotient's doing and `branch_space.rung_minima.challenge3` and not `branch_classes` is the evidence | no further-mark class here |
| **the branch key read at the configuration alone** | **5**, one branch short: the two policy branches have the same least key (COMPUTED) | **4**, one short (COMPUTED) |
| every branch replays from genesis and is certified | yes (COMPUTED at every branch) | same |
| the live Challenge 4 requirement | unresolved at the base, at the side-exchange withdrawal and at the further mark; met at the withdrawal of the mark permutations; **disappeared** at both policy branches, whose configurations hold fewer than two retained wholes (COMPUTED) | unresolved at the base; met at both Challenge 4 minima; disappeared at both policy branches (COMPUTED) |
| the declared generator space | twelve points over three coordinates and four capabilities (DEFINITION) | same |
| **one step, and the coordinate count** | one step is capability count one; the two counts **part**, the state-reading source moving one coordinate and using two capabilities (COMPUTED against the declared rule) | same |
| bundles refused | 8 of the 12 (COMPUTED from the declared counts) | same |
| the generator of capability count zero | emits nothing, so it is not eligible (COMPUTED) | same |
| **the minimum capability count among the generators that emit** | **1** (COMPUTED) | **1** (COMPUTED) |
| the minimum is unique on every branch | **no**: two tied classes on the further-mark branch, both retained (COMPUTED) | **yes** (COMPUTED) |
| what the demand generator does | emits on the further-mark branch alone, whose grouping carries a third tag no caller whole introduced; the demand it emits is already met at that branch's own renamings (COMPUTED) | emits nowhere (COMPUTED) |
| **the first challenge** | `<|b>`, one mark at depth one — a further mark and not a deeper nesting — and the same on every branch (COMPUTED over the declared 144-member domain) | same |
| what the enumeration generator emits moves under any substitution of one branch for another | **no**, over all 36 ordered pairs, the branch set carrying four distinct configuration keys (COMPUTED).  That it reads no component of a branch is DEFINITION-level, by unfolding its source; the census computes constancy and not independence, and the demand generator under O is the run's own witness for the difference | **no**, over all 25 (COMPUTED); same reading of it |
| the state-reading source under the same census | moves at 22 of the 36 (COMPUTED) | moves at 12 of the 25 (COMPUTED) |
| what the generator names has not been presented, is inside the bound, is never named twice, and silence means exhaustion | PROVED for an arbitrary record and bound | same |
| the branching bound | **3**, read off the closed rungs' own minima (COMPUTED) | same |
| the round bound at the declared ceiling of one thousand | **4** (COMPUTED; PROVED that four is the largest fitting count and that fifteen does not fit) | **4** (COMPUTED; PROVED) |
| rounds accepted | **0** (COMPUTED) | **0** |
| initial datum, reading, both event-follows relations | unchanged, empty on every probe at every branch (DEFINITION for the relations; COMPUTED for the replay and certification) | same |
| new event kind, withdrawn rule | none, none | same |

Boundary dependence: the branch set, the one-adoption rule, the generator
space, the capability counts, the one-step rule, the refusal of bundles, the
node ceiling, the branching bound and the computed round bound do not require
the admitted boundary.  Every configuration the branch quotient compares does;
so does the declared domain the enumeration generator reads; so does the
requirement the demand generator imposes.

**The seed's questions for this stage, answered.**  *What is a surviving
branch?*  A certified line: the declarations in force, the caller history it
replays, and the configuration that replay produces — the base branch, which
adopts nothing, and one branch per retained tied-minimum class of a closed rung.
*What is the weakest deterministic finite procedure that generates the next
challenge from that branch alone?*  Among the generators that emit anything at
all, the one that names the least member of the declared domain the presented
record does not carry: capability count one, attained alone at every branch of
reading O and at five of the six under U.  *Does it import undeclared
object-language structure?*  No.  Its declared inputs are the domain
enumeration and the presented record, and no branch value enters its source,
which is DEFINITION-level and true by unfolding; and replacing any declared
branch by any other moves nothing it emits, over every ordered pair and over a
branch set carrying four distinct configuration keys, which is COMPUTED, while
the state-reading source moves under the same census, which is what makes the
census a test.  The census establishes the constancy and not the independence:
the demand generator is constant under O and moves under U, so a pass is not a
proof that a generator reads nothing.  *What are the resource bounds?*  A declared node
ceiling of one thousand, a branching bound of three read off the run's own
enumerations, and a round bound of four computed from them — short of the seed's
fifteen, so an exact frontier under a declared bound is owed.

**The sharpest single fact of the stage is what the weakest generator cannot
do.**  The generator that costs nothing emits nothing.  The cheapest one that
emits anything **supplies and does not retain**: retaining is a second
capability, the one Challenge 3 priced as the process issuing an event, and a
generator that both supplies and retains bundles and is refused as one step.  A
supply changes no admitted state, which this run proved at Challenge 0 and
again at Challenge 1.  So the weakest justified generator produces challenges
that are inert on the state, and what follows from that for the rounds is the
next stage's to compute — the frozen S1-X says what this stage expects and is
not scored here.

## Predictions scored

| id | label | status | note |
|---|---|---|---|
| C5-X | NOT FORCED | **PENDING** | four of five clauses decided here and all four HIT: the first challenge is a further mark and not a deeper nesting; the enumeration source uses its declared inputs only, a DEFINITION-level justification, while the executable clause reads output constancy and cannot establish independence; fifteen rounds are not reached; and a smaller bound is declared.  The fifth, the frontier export, is the work of the stage that runs the rounds and keeps the prediction open |
| S1-1 | NOT FORCED | HIT | content: the closed rungs' minima recomputed and held to their receipts, and the implemented quotient.  The branch counts were known before the freeze |
| S1-2 | FORCED | HIT | content: both keys computed at every candidate; the counts fall to five and four with the policy part dropped |
| S1-3 | NOT FORCED | **PARTIAL** | the space-size clause HITS, DEFINITION-level and not counted as content: the coordinates, the capability names and the counts are declarations.  **MISSED**, recorded next to its value: the frozen falsifier names “the capability count and the coordinate count disagreeing in this space”, and they disagree — `one_step_iff_capability_count_one` true, `one_step_iff_one_coordinate_moved` false, the state-reading source moving one coordinate and using two capabilities.  The stage keeps the capability reading, which the seed requires, and scores the frozen clause against it.  The stage as first closed scored this the other way round and is repaired; the frozen file is untouched |
| S1-4 | FORCED | HIT | content: an eligibility filter computed per branch with both values attained under U, and the implemented quotient of generators over the branch set |
| S1-5 | FORCED | HIT | content: an enumeration over the declared domain.  The text was known before the freeze |
| S1-6 | FORCED | **PARTIAL** | the substitution clause HITS over every ordered pair of branches.  **MISSED**, recorded next to its value: “the run's own census of functions returning an event finds none in this stage's module”.  It finds one, `inherited_history`, the reader of the recorded caller history each branch replays.  The code is not changed to make the clause true; what the census cannot see is computed beside it in `events_named_by_this_stage`.  The frozen file is untouched |
| S1-7 | FORCED | HIT | content in the enumeration for the record; PROVED in Lean for the non-repetition and for the condition under which the generator falls silent |
| S1-8 | NOT FORCED | HIT | content: the branching bound off the closed rungs and the round bound computed from the declared ceiling.  The arithmetic was known before the freeze |
| S1-9 | FORCED | HIT | content for the replay and certification at every branch; DEFINITION-level for the empty relations, reported apart |
| S1-X | NOT FORCED | PENDING | scored by the stage that runs the rounds |

Seven of nine scored predictions hit and two are PARTIAL, each with a miss
recorded next to its value: all seven hit as content, and the stage's one
DEFINITION-level prediction is among the two that part.  The criterion is the
one Challenge 1 declared and this stage reuses unchanged.  The counts are the
receipt's `tally`, computed from the statuses and a declared list, and the
negative direction of every clause is tested.

**This is the weakest near sweep the run has produced, and the stage says so in
its own frozen file.**  Four of the numbers were computed in scratch before the
freeze and are named there; the corresponding hits are worth nothing.  The
informative results are the three the predictions did not contain — that the
branch quotient needs the policy part or loses a branch under each reading,
that the demand generator is eliminated everywhere under O and on five of six
branches under U by a computed filter rather than by declaration, and that the
two readings of one step part again — and the **two misses**: the stage
asserting a clean event census for its own module and getting one entry, and
the stage writing a falsifier that named the two readings of one step
disagreeing, which is the third informative result.  The second miss was
scored the wrong way round when the stage first closed and is repaired here.

## Advisories carried from the review of Challenge 5

The rule, inherited: an advisory is **actioned** when the repair lies in a
living document of this stage or in apparatus; one that would require
regenerating a closed rung's receipt, or editing a previous rung's `STATUS.md`
or a frozen `PREDICTIONS.md`, is **carried** with its reason.  Every advisory is
listed; `change_log.md` carries each repair with its reason.

Actioned:

1. `paper.md:2280`, the section 7.6 DEFINITION-level / content partition leaving
   several theorems in neither half.  Eleven lay outside both, including
   `deep_no_event_follows`, which the ledger already called DEFINITION-level.
   Every theorem of the table now lies in exactly one half, and the paragraph
   says which eleven were unplaced and why.  The two non-fixing theorems are
   counted as content by the rule section 7.5 states for the structurally
   identical Challenge 4 pair.
2. `claim_ledger.md:2594` and the carried `:2669`, B5-INERTIA.  The datum clause
   now names `deepReplay_initialDatum` and the reading clause
   `deepReplay_reading` inside the PROVED status, and the empty deep
   event-follows relation moves out of that conjunction into a DEFINITION-level
   clause with `deep_no_event_follows` and its instantiation, matching the
   paper.  One theorem, one label, in both places.
3. `paper.md:2570`, section 9's unscoped minimum.  It now reads “the minimum
   capability count **among the points that admit the caller's inscription**”,
   the scope the 5.17 row and B5-TWO-TIED-MINIMA carry, and says why it is
   needed: the refusing policy sits in the same space at count zero.
4. `paper.md:2546`, section 9 not recording that no policy is taken.  The
   Challenge 5 paragraph now ends with the non-adoption and the unchanged
   configuration, in the shape the Challenge 1 paragraph of the same section
   already used.
5. `paper.md:2294`, the `depth_is_invariant_where_the_inner_side_is_not` gloss
   reading as a biconditional.  It now says what the theorem says: one equality
   at two named states, and no biconditional is claimed.
6. `paper.md:2276`, the missing word in the `flatRetained_eq` gloss.  Reworded.
7. `paper.md:713`, definition 64 restricting `AdmitAt` without the
   qualification.  It now says which policy needs the event and that the deep
   grammar is the policy-agnostic replay rendering the receipt uses at every
   admitting point, which the receipt's own histories show.
8. `paper.md:1731` and the carried item on the same line, the two order rows.
   Both rows now carry the claim identifier **B5-ORDER**, a new ledger entry,
   and the first carries its policy scope: the census reads 116 at the
   recording policy, 121 at the opaque one and 108 at the discarding one, which
   `test_the_order_census_reads_a_different_count_at_each_policy` computes.  The
   receipt is **not** regenerated — the advisory's suggested `order` policy
   field would regenerate a closed rung's receipt — and the second half of the
   row is policy-independent and is stated as such.
9. `paper.md:1761`, the terminal sentence.  It now reads “at any policy of
   capability count one”, and says why the scope is the policy and not the
   count.
10. `paper.md:1768`, the blanket claim that the negative direction of every
    scorer clause is tested.  **Repaired by adding the three missing tests**
    rather than by narrowing the sentence: the widening's price, the
    initial-datum clause and the policy-space clause of C4-X now each have a
    negative-direction assertion.  The suite grows by three and the Challenge 5
    receipt does not move.
11. `challenge5/STATUS.md:415`, the deliberate axiom-log regeneration with no
    row.  A row is added to `MANUAL.md` for the 139-to-177 regeneration, in the
    shape the two earlier deliberate regenerations use.
12. `challenge5/STATUS.md:322`, the over-broad claim that every gate the rung
    added or touched has an injection row.  **Two rows are added**: the
    nine-versus-144 domain defect as a found-live row, from that rung's own
    record, and the collateral-fact agreement census as an injected row, run at
    this stage and observed — `[False, False, False, False, False, False, True,
    True]` against all-false when the census reads one point instead of every
    point.  The earlier sentence is not edited, a previous rung's status not
    being edited, and this entry is its correction.
13. `challenge5/STATUS.md:317` and `MANUAL.md:159`, the free-variable recurrence
    count.  The `MANUAL.md` half is actioned: the cell no longer claims a
    Challenge 4 occurrence, which no row, status or change-log entry records,
    and says what the rows support — Challenges 2 and 3, making Challenge 5 the
    **third** occurrence and not the fourth.  The `challenge5/STATUS.md` half is
    carried and is answered by that cell.
14. `paper.md:664`, definition 59's “the third and last widening”.  **Confirmed
    rather than repeated**: the second review repair of Challenge 5 already
    corrected it, and the definition now opens “The third reader bound of this
    run, and the second widening of its reader”.  The advisory describes the
    pre-repair state.

Carried, with reasons:

15. `challenge5/STATUS.md:50`, the `(COMPUTED)` label covering a cross-rung
    comparison.  The **ledger half is actioned**: B5-TWO-TIED-MINIMA's Challenge
    4 comparison is now kept out of its COMPUTED status, in the words
    B5-MEASURES-PART uses.  The status half is carried: a previous rung's
    `STATUS.md` is not edited.
16. `challenge5/STATUS.md:46`, `flatten_nested_eq_flat` carrying two labels in
    that rung's status table.  Carried for the same reason.  Confirmed rather
    than repeated: the paper's 7.6 list and B5-NESTING-INVISIBLE agree with each
    other, the second review repair having moved the ledger clause to
    DEFINITION-level, so the surviving discrepancy is in the frozen status page
    alone.
17. `challenge5/PREDICTIONS.md:106`, C5-6's first frozen falsifier — a permitted
    renaming that changes a mark's depth — not consulted by the scorer.  Carried:
    the file is frozen and the scorer lives in a closed rung's module, so a
    repair would regenerate that rung's receipt.  Answered rather than repaired:
    the falsifier cannot fire, and the run's evidence that it cannot is the Lean
    `depth_invariant_under_exchange` for the level exchanges and
    `test_no_permitted_renaming_moves_a_mark_depth` for the mark permutations at
    one two-mark state.  What the scorer does not do is read that evidence.
18. `code/boundary/challenge5.py:1480`, two C4-X clauses reading reading U alone
    while every sibling clause quantifies over both.  Carried: the repair lies in
    a closed rung's module and would regenerate its receipt.  Recorded so that a
    reader of C4-X's `policies_admitting_the_inscription` and
    `points_where_the_nesting_is_internally_visible` knows they are U's numbers,
    and the two readings agree there, which the receipt shows.
19. The Challenge 1 to Challenge 4 items carried in `challenge5/STATUS.md`
    survive unchanged: they lie in `challenge1.py` to `challenge4.py` or in a
    frozen `STATUS.md`.

A dedicated repair session for Challenges 1 to 5 would clear items 15 to 19 in
one deliberate regeneration.  That is not this stage's work.

## Advisories from the review of this stage, actioned

Six advisories arrived from the review of the stage commit `68452c34`; all six
are actioned, none declined, and the repairs lie in this stage's own module,
tests, receipt and prose.  Each is a line in `change_log.md` with its reason.

1. **S1-3's third frozen falsifier fired and the stage had scored it
   inverted.**  The frozen words name the capability count and the coordinate
   count *disagreeing* as the falsifier; the run computes that they disagree;
   the scorer required that disagreement in order to score HIT.  The clause is
   now scored on the frozen words — agreement hits, the computed disagreement
   MISSES — S1-3 is PARTIAL, the receipt key is `counts_agree_clause_status`,
   and the miss is recorded next to its value in the receipt's evidence string,
   in the shape S1-6 already used.  The ledger's restatement of the falsifier,
   which had the same inversion, is corrected to the frozen polarity.  The
   frozen file is untouched, and the stage keeps the capability reading of one
   step, which the seed requires: what changed is which frozen clause that
   result satisfies.
2. **The branch quotient was credited with an identification it does not
   make.**  `extra_mark_1` is never a branch candidate — `branch_candidates`
   takes one member per rung class — so the two further-mark points are one
   class at *Challenge 3's own* quotient, one level down, and `branch_classes`
   shows the further-mark branch as a singleton.  The paper, the results table,
   section 9, this status page and S1-BRANCH-KEY now say which quotient makes
   which identification, and cite `branch_space.rung_minima.challenge3` for the
   further-mark one.  The S1-1 quotient clause, which had asked only that
   *some* class hold two members, now names the three identifications the
   frozen text names and reads both quotients.
3. **Definition 81 over-read its own census.**  It said that constancy of the
   emitted challenge over the branch set entails reading no component of a
   branch, and the run's receipt carries the countermodel: under O the demand
   generator passes the census while its emitted demand is computed from the
   branch's configuration, and the same generator moves under U.  The
   entailment is withdrawn from definition 81, from definition 79, from the
   module docstring, from the declared-inputs sentence, from section 9 and from
   S1-READS-NOTHING, whose status is split — COMPUTED for the constancy,
   DEFINITION-level for the independence, which holds by unfolding the source.
   The receipt gains `generator_space.substitution_census_reach` and the
   residual is listed in the paper's section 10.  **No computed value moves.**
4. **Section 7.7's DEFINITION-level / content partition was not total.**
   `firstMissingFrom_ge` and `contains_cons_self` lay in neither half.  Both
   halves now name theorems rather than descriptions and sum visibly to the
   table's twenty-eight: fifteen DEFINITION-level with `contains_cons_self`,
   one `simp` on a constructor, and thirteen content with `firstMissingFrom_ge`,
   an induction over an arbitrary record.  This is the same defect actioned at
   section 7.6 as item 1 of the Challenge 5 advisories above.
5. **S1-NON-REPETITION carried a conjunct under PROVED that names no theorem.**
   “The generator is a function of the presented record alone” has no Lean
   statement, and the Lean `firstMissing` takes a record *and a bound*.  The
   clause moves out of the PROVED status into a DEFINITION-level one, true by
   unfolding.  Same shape as the B5-INERTIA repair, item 2 of the Challenge 5
   advisories above.
6. **S1-BOUNDARY-DEPENDENCE was labelled COMPUTED over a prose block.**  The
   receipt's `boundary_dependence` is five declared sentences that nothing
   computes; every earlier rung's entry of the kind reads LIMITATION.  It now
   reads with them and names `test_the_receipt_reports_the_boundary_dependence`.

## Where the run reached for a remembered result (declared reading 0)

- **The vocabulary is standard and is not derived here.**  “Branch”, “generator”,
  “node”, “round”, “bound”, “ceiling”, “census”, and the geometric sum that
  bounds a tree of fixed branching are known to this instrument.  They are
  declared as definitions 72 to 82 and used.
- **The shape of the stage follows Challenges 3, 4 and 5**, which this session
  read: a declared finite space, a capability count per member, a one-step rule,
  an implemented quotient, an eligibility filter, and a scorer.  The one place
  the shape had to change is that there is **one** measure and not two, and the
  reason is stated rather than assumed: a generator makes no collateral fact
  available, so the run's second measure has no subject here.
- **The branch quotient's policy part was forced by a computed fact**, not by
  taste: the two policy branches have the same least key, which the code says
  and the injection reproduces.
- **The Lean file's shape** — a recursive search with its three properties, a
  monotone bound, and two concrete evaluations — is ordinary and is not a result
  of this run.  What is not inherited is which properties the run needed: that
  the generator falls silent only on exhaustion is the theorem that makes “a
  branch stops for want of a next challenge” mean something.
- **What was worked out before the predictions were frozen, and is therefore
  worth nothing as foresight**: the branch counts, `<|b>`, the undemanded pairs
  on the further-mark branch, and the node arithmetic.  The frozen file names
  all four.
- **What was not**: that the implemented quotient would identify the two
  withdrawals and the O null minimum; that the demand generator would be
  eliminated everywhere under O; that the two readings of one step would part
  again; and that this stage's own event census would fire.  The last two are
  the stage's two misses — the parting of the two readings is what the frozen
  S1-3 falsifier named, and the stage's first scoring of it inverted the
  clause.
- **Nothing in the numbers was remembered.**  6, 5, 12, 8, 22 of 36, 12 of 25,
  3, 4, 726, 605, 504 tests, 205 axiom reports: all the code's.

## Leftovers, for the next stage and later

- Score S1-X: whether any branch accepts an augmentation at the first round,
  whether the branch set grows, and whether the stage that runs the rounds
  reports termination rather than growth.
- Score C5-X's fifth clause: whether the stage that runs the rounds exports the
  exact frontier under the declared bound and proves what is complete within it.
- **The branch set is scoped to the one-adoption rule.**  A branch adopting two
  or more retained minima is not enumerated and nothing is claimed about it.
- **The current configuration is definition 25 read per challenge.**  A
  cumulative reading, under which a branch would carry every rung's retention at
  once, is available and is not taken.
- **The node ceiling is a declaration** and the round bound moves with it: six
  at ten thousand, two at one hundred.  Nothing here says which ceiling is right.
- **The branching bound is the largest tie the run has produced**, held to as a
  bound and not proved to be one.  A round producing more classes would stop at
  the bound and the frontier would be exported there.
- **No second measure is declared for generators**, so the tie under U is left
  standing.  Whether one should be declared is OPEN.
- **The substitution census computes constancy and not independence**, and its
  predicate is named for the wider reading.  A census over a wider branch set,
  or a check of the generator's inputs that a machine rather than a reader
  performs, is available and is not built; the run's own countermodel to the
  entailment is in its receipt and is named in the paper's section 10.
- A generator that read the branch's judgment grammar, or that named an
  inscription outside the declared 144-member domain, is outside the space.
- The correspondence between the Lean `firstMissing` and `nodes` and their
  Python counterparts is prose; the test that holds the Lean file's concrete
  numbers to the Python ones checks the numbers and not the correspondence.
- Challenge 0 to Challenge 5 leftovers survive: no Lean statement of the
  class-count closed forms; no unbounded canonical-key theorem; the closure
  premise under the orbit witnesses is still checked by nothing; the outside of
  the outermost boundary is OPEN; the freeze manifest protocol remains OPEN.

## Repairs and live failures during the stage

- **The frozen S1-6 asserted a clean event census for this stage's module and
  it is not clean.**  Found by the scorer on its first run, not by review.  The
  clause is scored MISSED and the module is left as written: making the clause
  true by inlining one function would be fitting the code to the prediction.
- **Two evidence strings were false after that miss** — the S1-6 and C5-X
  strings still said the census found nothing — and were corrected before the
  receipt was committed, with C5-X's clause rescoped to the substitution census,
  which is what its frozen words name.
- **`test_lean_gate.py` failed on the first full run**, its module census
  listing five modules where the tree now has six.  A gate catching its own
  stale list; the list now names `BoundarySeed.Continuation1`.
- **Two Lean tactics from outside core were reached for and removed**:
  `by_contra` and `rcases` are not core Lean, and the proofs use `cases
  Nat.lt_or_ge` and `omega` instead.  `Option.noConfusion` would not typecheck
  at `Option Nat`'s universe, so the three defining equations are named as
  theorems and the proofs rewrite with them and finish with `simp`.
- **An injection could not be reversed with `git checkout`** because the
  stage's module is untracked until the stage commit — the hazard the Challenge
  4 and Challenge 5 rows record.  Both stage-1 code injections were reversed by
  patching the module back and re-running the suite.
- Every gate this stage added has an injection row in `MANUAL.md`: the frozen
  pin, the receipt byte-identity, the branch key's policy part, the substitution
  census, the Lean import-closure census for the new module, the deliberate
  axiom-log regeneration, and the workflow test-count grep.  Three rows Challenge
  5 owed are added with them.
- **In the review-repair session: a frozen falsifier that had fired was found
  to have been scored inverted.**  Not found by any gate — no gate reads a
  frozen file's words against the clause that claims to score them, and the
  scorer's own negative test hard-coded the inversion, so the suite was green
  over the defect.  The repair is in the scorer and in both directions of that
  test.  Two `MANUAL.md` rows record the session's deliberate receipt
  regeneration and the test-count grep that moved with it; no new gate was
  added, so no new gate needs proving.

## Gates recorded when the stage first closed

| gate | result |
|---|---|
| `verify_pins.py` | `pins ok: seed ba30bcd600d8 and 7 frozen prediction file(s)` |
| `unittest discover -s tests` | `Ran 504 tests`, OK |
| `mypy` (strict, tree pyproject) | `Success: no issues found in 32 source files` |
| `coverage` + `check_coverage.py` | `line 100.00% branch 100.00% over 10 files` |
| `run_challenge0.py` … `run_challenge5.py` | `unchanged` for all six: 5553, 28363, 35499, 220518, 795960, 128086 bytes |
| `run_continuation1.py` | `receipts/continuation1.json`, 210774 bytes |
| `git diff --exit-code -- receipts` | clean |
| `verify_lean.py` | `lean ok: 205 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; the log was regenerated deliberately once, 177 to 205, with no injection live |
| `ci/check_prose_watchlist.py` | clean, no pin regenerated |
| `tests/test_primitive_contact.py` | firewall passes |
| `ci/check_paper_citations.py` | cross-references resolve |
| injections | ten rows in `MANUAL.md`: seven for this stage and three that Challenge 5 owed |

## Required-question progress at stage 1

This is a completion checklist for the seed's section 5, not a completion
receipt.  It adds no result, closes no continuation round, and does not permit
the comparison before the freeze.  Each positive entry is limited to the
claim or theorem named; wider questions stay OPEN.

| seed question | stage-1 evidence and remaining scope |
|---|---|
| 1. A transition from the initial inscription | B0-INERTIA: the declared event-follows relation is empty under U and O, DEFINITION-level; no successor is forced by this model. |
| 2. Change without a separate admission | B0-INERTIA and B1-ADMISSION-RETENTION: the model changes placement through explicit admission events only; the certifying replay checks their history. |
| 3. Supply necessarily adds expressive power | B1-SUPPLY-PRESENTATION: supply is inert under both readings. |
| 4. Distinct retained inscriptions can remain collapsed | B2-MARKS-U and B4-FAILS-UNDER-BOTH give the scoped counterexamples and their invariance obstructions. |
| 5. Recovering a distinction through an identifying abstraction | B5-NESTING-INVISIBLE names the theorem for any property factoring through this run's flattening.  No theorem about every possible abstraction is claimed. |
| 6. A corrective minimum is necessarily unique | B3-THREE-MINIMA and B5-TWO-TIED-MINIMA refute uniqueness inside their declared finite spaces. |
| 7. What enables long continuation | S1-GENERATOR-SPACE and S1-WEAKEST-GENERATOR price the declared generators.  Accepted rounds and their terminals await stage 2; unbounded continuation remains OPEN. |
| 8. Invariant unresolved-requirement counts | S1-REQUIREMENTS computes each declared branch's requirement status.  A count-invariance theorem under all permitted renamings is OPEN; the per-branch table is not that theorem. |
| 9. Recurring transition roles | Supply, retention, declaration changes, requirement imposition and replay are definitions already used by the run.  A derived classification of recurring roles is OPEN; this list claims no theorem. |
| 10. A minimal or initial process among a class | OPEN.  Every minimum claimed here is conditional on a declared finite candidate space; no universal property of the final process is claimed. |
| 11. Outside the outermost boundary | B5-OUTSIDE remains OPEN under both readings; no address for it is declared. |
| 12. Depth and convergence | B5-DEPTH-TWO-SENSES distinguishes invariant depth from an internal counting judgment.  Convergence from increasing-depth stages is OPEN; no such sequence has been run. |
| 13. Boundary cost and benefit | B-BOUNDARY and the per-rung capability tables state the paid declaration and scoped separations.  Comparison with a boundary-free run is withheld until the freeze. |
| 14. U versus O prices, counts and terminals | B3-O-ALREADY-MET, B3-THREE-MINIMA, B4-MINIMUM-U, B4-MINIMA-O and S1-BRANCHES give the price/count differences.  Continuation terminals await stage 2. |
| 15. Definability comparison | Withheld until the verified freeze and the seed's comparison step. |

## Operator-directed completion of the stage-1 repair

The takeover received the existing dirty repair after the earlier writer
stopped.  It reviewed execution apparatus and prior operational notes, and
rechecked this tree's evidence.  That additional review context is disclosed;
it supplies no new object-language definition or result and does not restore
blindness.  The inherited provenance ceiling remains in force.

The remaining C5-X evidence sentence and the test-module header are narrowed:
finite output constancy is the executable check; independence is justified by
the enumeration source's declared inputs at DEFINITION level.  The explicit
typing list now includes `run_continuation1.py`.  No stage-2 prediction, code,
proof or freeze marker is written by this repair.

The takeover pinned the open pull request at head
`68452c34f0a1186d97dd58741ee2fb3442d7edb1`, base
`b3f325be71c73a737a524fdbf784eb49765b5277`, and merge-base
`7d2e6e86b80987de53932f54a14c234b5808eaa2`.  The following gates were rerun
against the repaired working tree; the older table above is historical.

| gate | fresh takeover result |
|---|---|
| seed and prediction pins | exit 0: seed `ba30bcd600d8`, all seven frozen prediction files match working, index and committed history |
| complete tree suite under fresh coverage | exit 0: 508 tests in 250.336 seconds, including the source-isolation and receipt tests |
| independent coverage gate | exit 0: line 100.00%, branch 100.00%, ten source files; previous JSON removed first; test-and-coverage command took 252.579 seconds, within the fifteen-minute battery bound |
| exact workflow count | stale 504 pattern rejected; current 508 pattern matched the fresh test output |
| strict typing | exit 0: 33 source files, including the stage-1 runner |
| deterministic receipt replay | exit 0: all seven runners report unchanged; stage 1 is 212629 bytes; the six closed-rung receipts match the pinned head |
| clean Lean verifier | exit 0: 205 reports within `propext` and `Quot.sound`, matching `lean/axioms.txt`; the axiom log was not regenerated |
| prose watchlist | exit 0: 49 watched terms, 130 files, 1826 pinned hits; no pin regenerated |
| identifier firewall | exit 0; the test output includes one skip |
| scoped diff hygiene | `git diff --check` passes; only this tree and its own workflow test-count line change |

The stale stage-1 receipt check failed by name after the final C5-X explanation
edit and passed after deliberate regeneration, with no injection live; the
record is in `MANUAL.md`.  The S1-3 label was rechecked and already reads
NOT FORCED in this status, the frozen prediction and the scorer.

This session did not run the repository-wide coverage suite, the sealed Lean
package or remote CI.  These scoped results establish no continuation terminal,
freeze validity, comparison completion or permission to merge.

## Next session

The next stage is **continuation stage 2: run the accepted augmentation rounds
on the declared branches, under the declared bounds**.  This section is the
handoff; there is no separate handoff file.  It opens fresh: read `SEED.md`,
`PLAN.md`, `MANUAL.md`, and this file; write and commit
`continuation/stage2/PREDICTIONS.md` with its own extrapolation before any code;
score S1-X.

The state stage 2 inherits.  **Nothing was adopted at stage 1 and no round was
run.**  Under each reading the declared branches are exactly the six and the
five above, each carrying its own declarations and the replay of its own
recorded history; the weakest emitting generator on each is the enumeration
generator, with the demand generator tied beside it on the further-mark branch
of reading U alone; the first challenge is `<|b>` on every branch; and the
bounds are a declared node ceiling of one thousand, a branching bound of three,
and a computed round bound of four.

What stage 2 owes.  For each branch, in the order the seed gives: the challenge
its generator names; every minimum valid response to that challenge, enumerated
over a declared finite space and priced, with ties preserved as branches and
quotiented only under an implemented relation; the branch replayed from its
recorded history before any result of it is certified; unresolved requirements
tracked through the round — whether they persist, split, disappear, or create
new ones; and the branch stopped when no next challenge or no justified response
exists, or at the four-round bound.  A supply changes no admitted state, so the
question stage 2 must answer first is whether a challenge that only supplies
admits of any justified response but the null one; if it does not, the honest
result is termination, and the seed counts a proof of termination as a
successful result.  If the tree grows past the ceiling, stop at the bound,
export the exact frontier, and prove what is complete within it.  Freeze the
predictions before looking.
