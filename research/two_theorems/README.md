# Two theorems from Genesis: sharp observation, institutional knowledge

AuthorityEffect: None.

A research tree outside the sealed derivation.  It consumes seven sealed
modules read-only (`input.json`), adds nothing to `lean4/`, and proves its
statements in core Lean 4.33 with no library beyond the sealed package.  Every
`#print axioms` report lies within `{propext, Quot.sound}`; the tree uses no
choice principle anywhere (`verify.py --check`, 119 declarations).

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
reading is a choice (status READING in `CLAIMS.md`); nothing here derives it.

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
| honest report (proposal, 2026-10-28) | `Honest D Q s := Knows D Q s`: the report claims no distinction the institution's questions cannot make; silence and under-claiming are permitted | `Reading.lean` |
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
- No absolute observer: an observer is adequate for every question exactly
  when it separates every pair of distinct carrier points, which `m` views
  cannot do on more than `2^m` points (`absolute_observer_iff`,
  `no_absolute_observer_of_large_carrier`).

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
(`no_closed_self_interpreter`); a finite catalogue of presentations misses
its own diagonal (`diag_not_member`), yet the diagonal can be known or
unknown to the catalogue depending on its size (`diag_known_witness`,
`diag_unknown_witness`, `membership_vs_knowledge`): membership
incompleteness is universal, knowledge incompleteness is contingent.  The
operational tower statement is ported (`tower_persists_operational`).  A
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
  question unknown to a family and known to a larger one forces a strict
  rise of information (`extension_forced`); no member knows what the family
  does not (`member_ignorant_of_family`); whoever knows the unknown question
  splits a pair the family merges (`finder_separates`).
- *One cannot know how intelligent another being is.*  An observer that
  merges two points cannot read the actor's resolution there: two actors
  consistent with every verdict it gives exist, one merging the pair and one
  splitting it (`observer_cannot_read_resolution`, with `Consistent`,
  `actor_consistent`, `markOne_consistent`).  A sharp observer is consistent
  (`sharp_consistent`); the converse fails by the same witness.
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
  to this equivalence, over the `|D|^|D|` tables on the carrier.
- Honesty (see Wisdom, re-examined): `honest_iff_no_overclaim`,
  `self_deceived_iff_witness`, `silence_honest`, `self_report_honest`,
  `member_report_honest`, `honest_mono`, `honest_antitone_carrier`,
  `knows_iff_knowsB`, `honest_iff_honestB`, `honest_or_demur`,
  `reports_do_not_certify`, `honest_here_not_there`.
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
space, know-or-witness over all `27` tables, honesty monotone in the
questions and antitone in the carrier); and on the guess witness (`half`,
`parity` and the identity on four points).  The results are under
`run_all()["reading_2026_10_28"]`.

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
| the type variable `C` in `no_closed_self_interpreter`, `tower_persists_operational` | metatheory | a parameter of the statement, instantiated at finite code lists; nothing is asserted of an infinite `C` |
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
- **Proposal** (READING, TT-R2): `Honest D Q s := Knows D Q s`.  A report is
  honest when it claims no distinction the institution's questions cannot
  make (`honest_iff_no_overclaim`); self-deception is a merged pair the
  report splits (`self_deceived_iff_witness`).  Demurral is honest: silence,
  the institution's own actor and every member's report are honest
  (`silence_honest`, `self_report_honest`, `member_report_honest`).
  Listening never makes an honest report dishonest (`honest_mono`); nor does
  a smaller carrier (`honest_antitone_carrier`).  Honesty is decided from the
  carrier (`honestB`, `honest_iff_honestB`), and every report is honest or
  has a witness of its over-claim (`honest_or_demur`).
- **No external verdict certifies it.**  Honesty is relative to the presented
  questions: the identity is honest for the institution that asks it and
  dishonest for the empty institution (`reports_do_not_certify`); and
  relative to the carrier: honest on two points, dishonest on three
  (`honest_here_not_there`).  A certificate of honesty says "no over-claim
  against these questions on this carrier", never "good judgment".  Whether
  a judgment was good has no measure in this tree, as the author says; the
  tree claims none.
- Whether an actor can run `honestB` on its own reports is the quotation
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
a distinction (`verdict_mono`, `knows_mono`, `honest_mono`,
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

- No observer is absolute: adequacy for every question needs every pair of
  distinct points separated, beyond `m` views on more than `2^m` points.
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
  (`own_guess_invisible`); a certificate of honesty does not travel to other
  questions or a larger carrier (`reports_do_not_certify`,
  `honest_here_not_there`).
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
  *Absolute* is sharp for every presentation, the view from nowhere, which no
  finite observer is (`absolute_observer_iff`,
  `no_absolute_observer_of_large_carrier`).  *Closed* is an evaluator
  realising every Boolean function of its own codes, which none is
  (`no_closed_self_interpreter`).  An interpreter can be primitive without
  being absolute or closed; the trees are compatible, and neither collapses
  the cosmos to one system.

## Not claimed

- That the readings above are forced by the author's words.
- That `Sharp`, `Knows`, `Wise` or `Honest` say anything about intelligence,
  knowledge, wisdom or honesty beyond the finite objects they name.
- That the author's hypotheses of 2026-10-28 are established; each is
  labelled above with its proved fragment and its proposal.
- That how intelligent another actor is can be read off a finite observer;
  under the reading, `observer_cannot_read_resolution` says the opposite.
- That the capacity threshold is exact beyond the tested parameters.
- That any statement here is a theorem of the sealed derivation: the tree
  consumes the seal and adds to nothing inside it.
- A denotational bridge to interpreters remains open, as in the seal.

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
