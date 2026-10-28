# Two theorems from Genesis: sharp observation, institutional knowledge

AuthorityEffect: None.

A research tree outside the sealed derivation.  It consumes seven sealed
modules read-only (`input.json`), adds nothing to `lean4/`, and proves its
statements in core Lean 4.33 with no library beyond the sealed package.  Every
`#print axioms` report lies within `{propext, Quot.sound}`; the tree uses no
choice principle anywhere (`verify.py --check`, 127 declarations).

This tree proves nothing about minds, intelligences or institutions in the
world.  It fixes a reading of two proposed theorems in Genesis's own objects
and reports what is proved, what is computed, what is conditional and what
does not follow under that reading.

## The two statements, as received

The author proposed two theorems in words: a *sharp intelligence
observability theorem* and an *institutional knowledge and wisdom theorem*,
together with a framing (actors and institutions are presentations and
presentation families; a fiber is a compressed presentation; information and
knowledge are to be derived from these; wisdom is undefined).  The framing is
the author's proposal, not Genesis structure; the exact theorem statements
had not arrived when this tree was built.  So the tree *declares* a reading
(next section) and proves what that reading supports.  When the statements
arrive, `CLAIMS.md` is to be re-mapped against them, and every row whose
reading differs is to be marked.

## Declared vocabulary

Each word on the left is read as the Genesis object on the right.  The
reading is a choice, declared in `CLAIMS.md` above its claims table (TT-R1,
TT-R2); nothing here derives it.

| word | object | where |
|---|---|---|
| actor, presentation | a presentation `Nat → Nat` read on a carrier `D : List Nat` | sealed `Compression`, `PresentationRelativity` |
| fiber of an actor | the points of `D` the presentation sends to one value | sealed `FiberIdentityOn`, `FiberConstant` |
| observer | an evaluator, a list of views; its verdicts `verdictB` | sealed `Represented` |
| sharp observation | `Sharp D E p`: the observer merges two points exactly when the actor does | `Observer.lean` |
| intelligence (the author's word) | not defined here; the only thing an observer can resolve of an actor is its fiber partition, and `Sharp` says it resolves exactly that | `Observer.lean` |
| institution | a family of questions `List (Nat → Nat)` (a presentation family) | `Institution.lean` |
| the institution's actor | Genesis's canonical compression `pQ D Q` | sealed `Compression` |
| information | `classCount D Q`, the number of signature classes on the carrier | sealed `Compression` |
| knowledge | `Knows D Q q := FactorsOn D (pQ D Q) q`: the question is a function of the institution's actor | `Institution.lean` |
| wisdom (question level; withdrawn as a reading of wisdom, 2026-10-28) | `Wise D Q`: for every question, knowledge or a witness pair of the ignorance.  It holds for every institution (`wise_of_represented`), so it names witness availability, not a virtue; see Wisdom, re-examined | `Institution.lean` |
| grounded report (proposal, 2026-10-28; named `Honest` until the review of that day) | `Grounded D Q s := Knows D Q s`: the report claims no distinction the institution's questions cannot make; silence and under-claiming are permitted.  Relative to the questions and the carrier; a report is grounded by being admitted; not truth, honesty or wisdom | `Reading.lean` |
| guess | `Guess D p s := ¬ Knows D [p] s`: a report the actor's own question does not determine | `Reading.lean` |
| consistent actor | `Consistent D E p`: every separation the observer reports is one of the actor's | `Reading.lean` |
| residuals of ignorance | `residuals D Q q`: the pairs the institution merges on which the question differs | `Reading.lean` |
| admitted carrier of a regime | `admitted r := List.range r.data` | `RegimeBridge.lean` |
| faithful correspondence | `Faithful D f`: `f` merges no two points of `D` | `Correspondence.lean` |

## What is proved (Lean)

All names live under `ResearchTwoTheorems`.  `CLAIMS.md` has one row per
claim with its evidence.

**Observer.lean, Theorem I.**

- The verdict kernel is Genesis signature equality for the observer's
  questions (`verdictB_false_iff_sigEq`).
- Sharpness is Genesis presentation identity between the actor and the
  observer's canonical compression (`sharp_iff_fiberIdentity`,
  `sharp_iff_presentationIdentity`).
- Verdict ceiling: whatever an observer computes of two points is a function
  of their signatures (`verdict_ceiling`); with `m` views any `2^m + 1`
  points contain a merged pair (`resolution_ceiling`).
- Resolution theorem, both directions: an actor on `D` has a sharp `m`-view
  observer exactly when it has at most `2^m` fibers (`sharp_observable_iff`,
  with the witness `bitObserver_sharp` and the refutation
  `not_sharp_observable_of_fibers_gt`).
- Absolute observation is carrier-relative: an observer is adequate for
  every question exactly when it separates every pair of distinct carrier
  points (`absolute_observer_iff`).  On the two-point carrier the one-view
  observer `[[0]]` is absolute (`absolute_observer_two_points`); `m` views
  cannot be on more than `2^m` points
  (`no_absolute_observer_of_large_carrier`).  No observer is absolute on
  every carrier, and none is once the carrier outgrows its views.  (The
  heading "no absolute observer" that stood here overstated the theorem;
  corrected 2026-10-28.)

**Capacity.lean, Theorem I(d).**  Genesis's capacity bound says a `d`-local
view over `k` colours collides on the interior of any carrier of size
`k^(2d+1) + 2d + 2`.  This tree shows the size is exact at every tested
parameter: one point below it, a colouring exists whose `d`-local code view
is injective on the interior (`tight_1_0`, `tight_2_0`, `tight_3_0`,
`tight_2_1`, `tight_3_1`, `tight_2_2`, assembled in `exact_threshold`).  The
colourings are produced in Python by a window-distinct cyclic word (every
word of length `2d + 1` occurs once) and decided in Lean.  The general
statement for all `k`, `d` is not in Lean (see Open).

**Institution.lean, Theorem II.**

- Knowledge is signature determination (`knows_iff_determined`), closed
  under every computation on known answers (`knows_comp`, `knows_join`),
  monotone in the institution (`knows_mono`); members and the institution's
  own actor are known (`knows_member`, `knows_actor`).
- Knowledge is information stationarity: adjoining a question leaves the
  information unchanged exactly when the question is known, and raises it
  strictly otherwise (`knows_iff_information_eq`,
  `information_lt_of_not_knows`, `not_knows_iff_split`).
- Known questions and the actor itself add nothing (`known_extension_inert`,
  `self_inclusion_inert`, `self_inclusion_information`); an institution is an
  actor with the institution's information (`institution_is_actor`).
- A member is fiber-identical to the institution exactly when it alone knows
  every member (`member_sharp_iff`); an institution can exceed every member
  (`institution_exceeds_members`: parity and half on four points).
- An observer is sharp for an institution's actor exactly when the two know
  each other's questions (`sharp_institution_iff_mutual_knowledge`).
- Panels: the pooled observer merges exactly when the panel certifies
  non-separation; unanimous separation implies pooled separation and not
  conversely (`pooled_merges_iff_certNeg`, `certPos_imp_pooled`,
  `pooled_not_certPos`).
- Information of `m` views is at most `2^m` (`information_le_resolution`).
- Know-or-witness holds on every represented carrier, constructively: for
  every question, knowledge or a witness pair (`know_or_witness`,
  `wise_of_represented`), decided by `knowsB` without excluded middle or
  choice.  Because it holds for *every* institution it is not a reading of
  wisdom (see Wisdom, re-examined).

**Diagonal.lean, the interpreter level.**  No evaluator on a code set
realises every Boolean function of the codes
(`no_closed_self_interpreter`; the finite form on codes `Fin n` is
`no_closed_self_interpreter_fin`); a finite catalogue of presentations misses
its own diagonal (`diag_not_member`), yet the diagonal can be known or
unknown to the catalogue depending on its size (`diag_known_witness`,
`diag_unknown_witness`, `membership_vs_knowledge`): membership
incompleteness is universal, knowledge incompleteness is contingent.
`tower_persists_operational` is a diagonal over *unrestricted* world
functions: `opDiag` appends a datum under `.note`, which the declared
transition `step` never does (`opDiag_appends`, `opDiag_not_lawful`,
`step_note_data`), so it is no interpreter and no lawful transition, and the
statement is weaker than the words "the operational tower statement" that
stood here (qualified 2026-10-28).  Under the contract that a function agree
with `step` on the represented support (`Lawful`, `step_lawful`), a lawful
function escapes a catalogue exactly when no code of the catalogue is lawful
(`lawful_escape_iff`; the escaping function is `step` itself), and one
lawful code closes the escape (`lawful_no_escape`).  So the lawful tower
statement is no theorem against a catalogue that implements the transition
anywhere; contracts weaker than support-lawfulness are open (TT-40o).  A
statement quantifying over an infinite enumeration of catalogues was removed
on 2026-10-28 under the finitude rule (see Finitude); nothing cited it.

**Correspondence.lean, fidelity.**  A merged pair is collapsed under every
observer (`collapsed_of_merged`), so an unrestricted correspondence can erase
a distinction before any observer sees it; the constant map does so and is
not faithful (`constant_collapses_all`, `constant_not_faithful`).
Sharpness for an actor transports along *every* correspondence
(`sharp_pullback_iff`); what a sharp observation through `f` forces is that
`f` merges only within the observed actor's fibers
(`fiberConstant_of_sharp_pullback`), injectivity being the identity case
(`faithful_of_sharp_identity`, `sharp_identity_pullback`).  The institution's
actor is faithful exactly when the institution knows the identity
(`faithful_actor_iff`); the empty institution's actor is the constant
correspondence (`empty_actor_constant`, `empty_actor_not_faithful`).

**RegimeBridge.lean, Genesis regimes as observers.**  Each well-formed
context cuts a view out of the admitted carrier (the admitted data whose
plugging is derivable).  Relative to a list `cs` enumerating the well-formed
contexts, the regime's observer separates two admitted data exactly when
Genesis declares them `separable` and merges them exactly when Genesis
declares them `collapsed`; collapse is signature equality
(`verdict_regime_iff`, `collapsed_iff_verdict_false`, `collapsed_iff_sigEq`).
The regime's observer is sharp for an actor exactly when collapse coincides
with the actor's fibers (`sharp_regime_iff`); a regime knows a question
exactly when the question respects collapse (`regime_knows_iff`); a regime
with `n` contexts has at most `min(2^n, data)` observational classes
(`regimeInformation_le`).  Off the carrier a datum lies in no view
(`not_mem_ctxView_of_unadmitted`).

Views against admissions: an observer's verdicts are monotone in its views
(`verdict_mono`; `information_mono` for institutions), while a regime that
collapses a pair an earlier regime separated has lost or altered one of the
earlier views (`recollapse_changes_views`).  The two-datum regimes `R0` and
`R0rule` show one rule admission turning the view `[0]` into `[0, 1]`
(`recollapse_witness`, `recollapse_witness_changes_views`).

**Reading.lean, the author's statements of 2026-10-28.**  Each item gives the
author's statement in his words, then what the tree proves of it under the
declared reading.

- *An intelligence bigger than its sources finds a pattern no actor and no
  institution knew, and forces the presentation family to extend.*  A
  question unknown to a family and known to a larger one is known only at a
  strict rise of information (`knowledge_gain_requires_refinement`, named
  `extension_forced` until 2026-10-28: the theorem prices an extension and
  compels none); no member knows what the family does not
  (`member_ignorant_of_family`); whoever knows the unknown question splits a
  pair the family merges (`finder_separates`).  What would make the
  extension *forced*, an admitted fidelity condition under which an
  unresolved question requires it, is open (TT-38o).
- *One cannot know how intelligent another being is.*  An observer that
  merges two points cannot read the actor's resolution there: two actors
  consistent with every verdict it gives exist, one merging the pair and one
  splitting it (`observer_cannot_read_resolution`, with `Consistent`,
  `actor_consistent`, `markOne_consistent`).  A sharp observer is consistent
  (`sharp_consistent`); the converse fails by the same witness.
  `Consistent` is one-directional (every reported separation is the actor's;
  the actor may separate more), and the theorem is about verdicts on the
  carrier, not about an actor interacting with an observer through a
  transcript.  That protocol is not modelled here (TT-39o).
- *A quality institution can listen and not judge, hold the obstructions and
  let them stay.*  The residuals of a question are the merged pairs on which
  it differs (`residuals`, `mem_residuals`); they are empty exactly when the
  question is known (`residuals_nil_iff`); listening never adds one
  (`residuals_antitone`); a residual goes exactly when some new question
  splits its pair (`residual_removed_iff`).  Holding is inert: no theorem
  forces an institution to act on a residual.
- *Actors within the institution are presentations and presentation
  families.*  A sub-family nested as its own actor is the flat family
  (`nest_inert`, `nest_information`), so a hierarchy of families is one
  family; a family one member of which knows every other has that member's
  information (`participation_collapse`).
- Locality and the finite question space.  Knowledge depends only on the
  values taken on the carrier (`knows_congr`, `knows_member_congr`); the
  institution's actor stays on the carrier (`pQ_mem`); knowing a question is
  knowing its canonical representative (`knows_iff_knows_pQ`), a table
  `D → D`.  So every quantifier over "all questions" in this tree ranges, up
  to this equivalence, over the tables on the carrier, `|D|^|D|` of them
  when `D` lists each point once.
- Grounded reports (see Wisdom, re-examined): `grounded_iff_no_overclaim`,
  `ungrounded_iff_witness`, `silence_grounded`, `self_report_grounded`,
  `member_report_grounded`, `grounded_mono`, `grounded_antitone_carrier`,
  `knows_iff_knowsB`, `grounded_iff_groundedB`, `grounded_or_demur`,
  `reports_do_not_certify`, `grounded_here_not_there`.
- Guessing (see The author's hypotheses): `guess_iff_witness`,
  `own_guess_invisible`, `guess_visible_iff`, `shared_guess`,
  `guess_witness`.

## What is computed (Python, `model.py`)

Exhaustive checks on carriers of three and four points: the resolution
theorem for every presentation and every one- and two-view observer; the
verdict ceiling; every knowledge statement over eleven families drawn from a
pool of four questions; the panel statements over every pair of one-view
observers; mutual knowledge; the diagonal statements, and the self-evaluator
statement over every evaluator on two and three codes; faithfulness,
pullback transport and fiber constancy over every map of three points, every
observer of at most two views and every actor; the regime bridge on five
small regimes with the contexts enumerated in Python; the recollapse witness;
view monotonicity.  For the capacity threshold the construction produces the
colourings for every `k ≤ 4`, `d ≤ 2` with `k^(2d+1) ≤ 1100` and checks
injectivity, and an exhaustive search over all colourings confirms the
forced collision at the threshold for `(2, 0)`, `(3, 0)`, `(2, 1)`.  The six
lists decided in Lean are checked to be the construction's output.

The statements of 2026-10-28 are checked over the eleven families from the
four-question pool on four points (extension, residuals, nesting,
participation collapse); over every one- and two-view observer on three and
four points (for every merged pair, a consistent actor that merges it and
one that splits it); over every table on three points (the finite question
space, know-or-witness over all `27` tables, grounding monotone in the
questions and antitone in the carrier); and on the guess witness (`half`,
`parity` and the identity on four points).  The results are under
`run_all()["reading_2026_10_28"]`.  The absolute-observer check (adequacy
over every table against separation of every pair, for every one-view
observer on three points and every two-view observer on four; the two-point
witness and its three-point failure) is under `run_all()["absolute"]`.

## What is conditional

- The regime bridge takes an enumeration `cs` with `∀ c, c ∈ cs ↔ wfCtx r c`
  as a hypothesis.  The ignition tree (`research/ignition`) provides one,
  `Ignition.ctxList` with `Ignition.mem_ctxList`; this tree does not import
  it.  For one-unary-form regimes the enumeration is proved here
  (`unary_enumeration`).
- The exactness of the capacity threshold is proved in Lean at six
  parameter pairs and checked in Python at twelve.  The general statement is
  open.

## Finitude: metatheory against internal structure

The author's standing rule (2026-10-28): no observer from nowhere, no
container, no continuum; no infinite fiber, no infinite set of
presentations, of families or of observers; nothing beyond the present
carrier until it is derived here or imported with a priced admission.  Every
quantifier in the tree was audited against it.

| appears as | status | why |
|---|---|---|
| `Nat` as the name of a token | metatheory | Genesis's own token names; the sealed modules use them |
| `Nat → Nat` as the name of a presentation | metatheory | a presentation is read only on `D` (`knows_congr`); no theorem consults a value off `D` |
| `D`, `admitted r`, views, evaluators, institutions, `catalogue code n`, `classes`, every count | internal, finite | lists; every theorem is guarded by `x ∈ D` or `a < r.data` |
| `∀ q : Nat → Nat` in `Knows`, `Wise`, `absolute_observer_iff` | internal after reduction | `knows_iff_knows_pQ` and `pQ_mem` reduce it to the `\|D\|^\|D\|` tables `D → D`, which the model enumerates |
| the type variable `C` in `no_closed_self_interpreter`, `tower_persists_operational`, `lawful_escape_iff` | metatheory | a parameter of the statement, ranging over every type, infinite ones included; the internal forms are `no_closed_self_interpreter_fin` on codes `Fin n` and the finite code lists the other two take.  (Corrected 2026-10-28: this row said nothing was asserted of an infinite `C`, which is false of the general theorem.) |
| `sep_irrefl`, `verdict_irrefl`, `collapsed_of_merged`, `constant_collapses_all` over all of `Nat` | metatheory | `Bool` computations on the construction, true pointwise; they assert no law of a regime (see Fact against law) |
| `code : Nat → Nat → Nat` in `Diagonal.lean` | metatheory | an enumeration scheme of which only `List.range n` is ever used |

Two leaks were found and closed.  `catalogue_incomplete` quantified over an
infinite enumeration of catalogues; it is removed, and the finite
`diag_not_member` carries the diagonal fact.  `Wise` quantified over all
functions `Nat → Nat`; `knows_iff_knows_pQ` reduces it to the finite
tables, and the model checks know-or-witness over every table on three
points.  One artifact is named and given no reading: `verdictB` is defined
on all of `Nat`, so the model can print a verdict on an unadmitted datum
(`verdict(R0, 0, 99)`); no theorem reads such a verdict, and
`not_mem_ctxView_of_unadmitted` says the datum lies in no view.

## Wisdom, re-examined (2026-10-28)

The author: wisdom is not information; knowledge is a structure on top of
information; wisdom is knowing when to demur; no measure can resolve whether
a judgment was good; wisdom is not deceiving oneself.

- `Wise` is **refuted as a reading of wisdom**.  It holds for every
  institution on every represented carrier (`wise_of_represented`), so it
  distinguishes nothing; it names witness availability, for every question
  either knowledge or a pair that shows the ignorance.  TT-15 stays proved;
  its vocabulary row is withdrawn.
- **Proposal** (declared reading TT-R2): `Grounded D Q s := Knows D Q s`.
  A report is grounded when it claims no distinction the institution's
  questions cannot make (`grounded_iff_no_overclaim`); an ungrounded report
  splits a merged pair, its witness (`ungrounded_iff_witness`).  Demurral is
  grounded: silence, the institution's own actor and every member's report
  are grounded (`silence_grounded`, `self_report_grounded`,
  `member_report_grounded`).  Listening never makes a grounded report
  ungrounded (`grounded_mono`); nor does a smaller carrier
  (`grounded_antitone_carrier`).  Grounding is decided from the carrier
  (`groundedB`, `grounded_iff_groundedB`), and every report is grounded or
  has a witness of its over-claim (`grounded_or_demur`).
- **The vocabulary is provisional.**  The predicate was named `Honest` until
  the review of 2026-10-28, which observed that a member's report is
  grounded by admission whatever it says of anything outside the questions
  (`member_report_grounded`): the predicate is non-overclaiming relative to
  admitted questions, not honesty and not truth.  In this reading a question
  is not true or false, so "a false report" has no referent; the limitation
  is the theorem `reports_do_not_certify`, not a gap beside it.  `Grounded`
  (determined by the admitted questions) is the tree's word; the author's
  "not deceiving oneself" is what it proposes to read, and the proposal
  stands or falls with him.
- **No external verdict certifies it.**  Grounding is relative to the
  presented questions: the identity is grounded for the institution that asks
  it and ungrounded for the empty institution (`reports_do_not_certify`);
  and relative to the carrier: grounded on two points, ungrounded on three
  (`grounded_here_not_there`).  A certificate of grounding says "no
  over-claim against these questions on this carrier", never "good
  judgment".  Whether a judgment was good has no measure in this tree, as the
  author says; the tree claims none.
- Whether an actor can run `groundedB` on its own reports is the quotation
  boundary studied in `research/interpreter_verdict` and is not decided
  here.

## The author's hypotheses, labelled as his

Two hypotheses arrived on 2026-10-28.  Neither is proved.  Each has a proved
fragment under the declared reading and a proposal.

**Degradation** (predictive processing: brains guess; humans lack an
institutional structure in which to see their own errors; degraded
institutions).  Proved: a guess is a report the actor's own question does not
determine (`Guess`, `guess_iff_witness`); the actor never locates its own
guess, since every question it knows agrees on the witness pair
(`own_guess_invisible`); the family locates it exactly when another member
splits the pair (`guess_visible_iff`); a guess every member shares is the
family's own self-deception (`shared_guess`); on four points `half` guesses
the identity and `parity` locates it (`guess_witness`).  Proposed, not
proved as a reading: health is growth by views or members, which never loses
a distinction (`verdict_mono`, `knows_mono`, `grounded_mono`,
`information_mono`); degradation is acting by admission, which can
(`recollapse_changes_views`, `recollapse_witness`).  Not claimed: that any of
this is what brains or institutions in the world do.

**Institutional reasoning** (intelligence requires institutional structure;
bureaucracy on bureaucracy becomes computationally explosive; a self-similar
hierarchy crashes when participation stops: "you compress it").  Proved: a
hierarchy of families is one family (`nest_inert`, `nest_information`), and
when one member knows every other the family has that member's information
(`participation_collapse`).  Proposed, not in Lean (TT-35o): information is
monotone along a chain of families and bounded by the carrier
(`information_mono`, `information_le_carrier`), so a chain longer than `|D|`
has an inert level; whether that is the crash is the author's reading.  Not
started: the author has a paper on institutional reasoning; no larger proof
begins until he names it and confirms the scope.

## What does not follow

- No observer is absolute on every carrier: adequacy for every question
  needs every pair of distinct points separated, beyond `m` views on more
  than `2^m` points.  On a carrier the views cover an observer can be
  absolute (`absolute_observer_two_points`).
- A diagonal over unrestricted world functions is not a diagonal over
  interpreters (`opDiag_not_lawful`); a lawful diagonal exists only against
  a catalogue with no lawful code (`lawful_escape_iff`).
- Unanimous separation is not pooled separation's converse
  (`pooled_not_certPos`).
- Membership of a catalogue and knowledge by it come apart
  (`membership_vs_knowledge`).
- More admitted structure is not more distinction: admissions alter views,
  and a rule admission collapses a separated pair (`recollapse_witness`).
  More *views* are never fewer distinctions (`verdict_mono`).
- An unrestricted correspondence is not a faithful one; the constant map
  collapses everything under every observer.
- Observed separation never holds of a point and itself, and a view
  separating `0` from `1` says nothing of `0` and `2`
  (`separation_fact_not_law`).
- An observer's verdicts do not fix the actor's resolution on a merged pair
  (`observer_cannot_read_resolution`); a member does not see its own guess
  (`own_guess_invisible`); a certificate of grounding does not travel to
  other questions or a larger carrier (`reports_do_not_certify`,
  `grounded_here_not_there`).
- Know-or-witness does not single out any institution
  (`wise_of_represented`).

## Fact against law

Genesis admits irreflexivity; it does not derive it from the mark, and the
sealed `Bridge` records that the irreflexivity law is not entailed.  This
tree keeps that boundary.  Its irreflexivity statements
(`sep_irrefl`, `verdict_irrefl`) are computations of `Bool` inequality on a
point and itself: an observer's verdict is a comparison, and a comparison of
a thing with itself returns `false`.  That is a metatheoretic fact about the
observer calculus, priced as an import of decidable equality, and it is a
*fact about each pair*, never a law quantified over a regime.  Nothing in
this tree uses, derives or strengthens the admitted law, and no statement
here converts a witnessed off-diagonal separation into a universal one.

## Relation to other trees

- `research/uncollapse`: proves when admissions undo collapse and that a
  rule admission re-collapses a separated pair (`recollapse_by_rule`).  This
  tree's bridge reads those regime facts as observer facts and proves the
  general form (`recollapse_changes_views`); its correspondence module
  answers the review question raised there about unrestricted maps.
- `research/ignition`: the context enumeration the bridge takes as a
  hypothesis.
- `research/x300_observer_information`: information in an observer, with
  bounds of its own.  This tree's information is Genesis's `classCount` and
  does not restate that tree's results.
- `research/interpreter_verdict`: proves the interpreter boundary is a
  *primitive difference* for quiescence (`lawful_unique`, `interp_not_step`,
  `identification_changes_quiescence`).  The two trees use the words the
  same way.  *Primitive* is Genesis's primitive difference: a witnessed
  difference that identification cannot remove without changing a verdict.
  *Absolute* is adequate for every question on the carrier, which is
  separating every pair of distinct carrier points (`absolute_observer_iff`):
  possible on a carrier the views cover (`absolute_observer_two_points`),
  impossible once the carrier outgrows them
  (`no_absolute_observer_of_large_carrier`), and nothing is absolute on
  every carrier.  (Corrected 2026-10-28: the gloss "sharp for every
  presentation, the view from nowhere" that stood here names a property no
  observer has on two or more points, since distinct presentations have
  distinct fiber partitions; it was not the theorem.)  *Closed* is an
  evaluator realising every Boolean function of its own codes, which none is
  (`no_closed_self_interpreter`).  An interpreter can be primitive without
  being absolute or closed; the trees are compatible, and neither collapses
  the cosmos to one system.  The two trees' notions of a *lawful* function
  differ: that tree's `lawful_unique` is the uniqueness of a reflective step
  under its interpretation and quotation laws, this tree's `Lawful` is
  agreement with `step` on the represented support; `lawful_escape_iff` is
  about the second and says nothing of the first.

## Not claimed

- That the readings above are forced by the author's words.
- That `Sharp`, `Knows`, `Wise` or `Grounded` say anything about
  intelligence, knowledge, wisdom, honesty or truth beyond the finite objects
  they name; `Grounded` is non-overclaiming relative to admitted questions,
  and a report is grounded by admission.
- That `opDiag` is an interpreter or a lawful transition; it is a diagonal
  over unrestricted world functions (`opDiag_not_lawful`).
- That `knowledge_gain_requires_refinement` forces anything; it prices a
  gain of knowledge, and what would force an extension is open (TT-38o).
- That the author's hypotheses of 2026-10-28 are established; each is
  labelled above with its proved fragment and its proposal.
- That how intelligent another actor is can be read off a finite observer;
  under the reading, `observer_cannot_read_resolution` says the opposite.
- That the capacity threshold is exact beyond the tested parameters.
- That any statement here is a theorem of the sealed derivation: the tree
  consumes the seal and adds to nothing inside it.
- A denotational bridge to interpreters remains open, as in the seal.

## Corrections of 2026-10-28, after review

A review of the tree at `67fcfe1` (relayed by the author; its findings were
checked against the source one by one) led to these changes.  Each earlier
statement is kept above with a dated note where it stood.

1. *Absolute observation.*  "No absolute observer" overstated
   `absolute_observer_iff`: adequacy for every question is separation of
   every pair, which an observer can achieve on a carrier its views cover.
   Added `absolute_observer_two_points` and the model's `absolute_checks`;
   the gloss "sharp for every presentation" in Relation to other trees was
   wrong on its own terms and is replaced.
2. *The diagonal.*  `opDiag` appends a datum under `.note`, which `step`
   never does; `tower_persists_operational` is a diagonal over unrestricted
   world functions, not the operational tower statement.  Added
   `opDiag_appends`, `opDiag_not_lawful`, `step_note_data`, and the lawful
   form `Lawful`, `step_lawful`, `lawful_escape_iff`, `lawful_no_escape`
   (TT-18L): a lawful function escapes a catalogue exactly when no code of
   it is lawful.  Weaker contracts are open (TT-40o).
3. *Names.*  `extension_forced` is `knowledge_gain_requires_refinement`; it
   compels no extension.  `Honest` and its theorems are `Grounded`,
   `grounded_*`, `ungrounded_iff_witness`, `groundedB`; the vocabulary is
   provisional and is not honesty or truth.  The model's keys and functions
   follow (`grounding_checks`, `refinement_cases`, `refinement_violations`).
4. *Finitude.*  `no_closed_self_interpreter` is metatheory over every type
   `C`, infinite ones included; the row that said nothing was asserted of an
   infinite `C` is corrected, and `no_closed_self_interpreter_fin` is the
   internal form.
5. *Counting tables.*  `|D|^|D|` counts the tables when `D` lists each point
   once; said so in both places.
6. *Open questions recorded.*  TT-38o (what would force an extension),
   TT-39o (an interaction protocol behind "one cannot know how intelligent
   another is"; `Consistent` is one-directional and the theorem is about
   verdicts on the carrier), TT-40o (diagonals under weaker transition
   contracts).
7. *The claims ledger and the receipts.*  READING was never a status of the
   research-tree contract; the two readings are now prose above the table,
   and two rows that carried `|` inside a cell are reworded.  The gate that
   caught this, `tests/test_new_research_tree_contract.py`, runs in the
   repository suite, which had **not** been run on this tree at `67fcfe1`
   although the pull request then said the repository gates had been run
   locally.  Running it found three reds caused by this tree: the ledger
   rows above and two stale generated pages (`docs/index/pins.md`,
   `docs/lean_build_order.md`), all fixed in the same change as these
   corrections.  Reds in that suite not caused by this tree are listed in the
   pull request.

## Layout and how to run

```
research/two_theorems/
  README.md  CLAIMS.md  TREE_CONTRACT.json  SOURCE_MANIFEST.json  input.json
  model.py  tests/test_model.py  verify.py
  lean/lakefile.toml  lean/lean-toolchain  lean/lake-manifest.json
  lean/ResearchTwoTheorems.lean
  lean/ResearchTwoTheorems/{Observer,Capacity,Institution,Diagonal,
                            Correspondence,RegimeBridge,Reading,AxiomReport}.lean
```

`verify.py --check` is the tree's own receipt.  The repository suite
(`python -m pytest` at the root) holds the gates that see this tree from
outside: the research-tree contract, the generated index pages and the
identifier firewall.

From this directory, with Lean 4.33.0 on the path:

```
python verify.py --check        # pins, pytest, mypy --strict, forbidden tokens,
                                # lake build, the axiom report against the contract
python verify.py --write-pins   # after an intentional change to input.json
python model.py                 # the finite model's summary as JSON
```

`input.json` records the main commit the tree was built against; no gate
verifies that digest, and the Lean dependency is the working tree's
`lean4/`.
