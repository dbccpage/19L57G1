# Two theorems from Genesis: sharp observation, institutional knowledge

AuthorityEffect: None.

A research tree outside the sealed derivation.  It consumes seven sealed
modules read-only (`input.json`), adds nothing to `lean4/`, and proves its
statements in core Lean 4.33 with no library beyond the sealed package.  Every
`#print axioms` report lies within `{propext, Quot.sound}`; the tree uses no
choice principle anywhere (`verify.py --check`, 86 declarations).

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
| wisdom (question level) | `Wise D Q`: for every question, knowledge or a witness pair of the ignorance | `Institution.lean` |
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
- Wisdom at question level holds on every represented carrier,
  constructively: for every question, knowledge or a witness pair
  (`know_or_witness`, `wise_of_represented`), decided by `knowsB` without
  excluded middle or choice.

**Diagonal.lean, the interpreter level.**  No evaluator on a code set
realises every Boolean function of the codes
(`no_closed_self_interpreter`); every catalogue of presentations misses its
own diagonal (`catalogue_incomplete`, `diag_not_member`), yet the diagonal
can be known or unknown to the catalogue depending on its size
(`diag_known_witness`, `diag_unknown_witness`, `membership_vs_knowledge`):
membership incompleteness is universal, knowledge incompleteness is
contingent.  The operational tower statement is ported
(`tower_persists_operational`).

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

## What is conditional

- The regime bridge takes an enumeration `cs` with `∀ c, c ∈ cs ↔ wfCtx r c`
  as a hypothesis.  The ignition tree (`research/ignition`) provides one,
  `Ignition.ctxList` with `Ignition.mem_ctxList`; this tree does not import
  it.  For one-unary-form regimes the enumeration is proved here
  (`unary_enumeration`).
- The exactness of the capacity threshold is proved in Lean at six
  parameter pairs and checked in Python at twelve.  The general statement is
  open.

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

## Not claimed

- That the readings above are forced by the author's words.
- That `Sharp`, `Knows` or `Wise` say anything about intelligence, knowledge
  or wisdom beyond the finite objects they name.
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
                            Correspondence,RegimeBridge,AxiomReport}.lean
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
