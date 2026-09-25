# PREDICTIONS: rung ten -- adjacency, reach, branching and exhaustion

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_response.py` for the computational rows and by `test_census.py` for
the census rows.  A missed prediction is recorded next to its value and
never edited.  A miss is a finding, not a defect.

The frozen question is `PROMPT.md`, sha256
`09e9df8c4349b1ef3307f7cb606284534ca0e5b735163c6e7098805d18aa6093`.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this rung, so a hit evidences the ordering of the
work and not insight.  NOT FORCED means the run could have come out the
other way.  An argument written by this rung's own session before the
run is not a receipt: a row that leans on one is NOT FORCED.

Receipts and sources read before freezing, because a prediction below
leans on them: rung four's `receipts/iso_index.json` and rung nine's
`receipts/profile.json` (577, 3928 and 14293 sequences; 75, 523 and 1718
distinct regimes at EMPTY, L and F; 2316 distinct regimes in all, in 402
classes of the sealed key procedure, with zero disagreements against the
sealed brute-force minimum); the declared alphabet of the rectangle in
`research/second_nofirst/nofirst.py`; the sealed Python genesis
histories in `code/derivation/engine.py` (the Python base L holds two
data and nothing else, the Python base F three data and nothing else,
and neither holds a requirement); the sealed engine's quotient of tied
responses by the key of the regime reached after the demanded pair is
imposed; the sealed responder in `code/derivation/candidates.py` (its
enumeration at two items is pruned by four lemmas stated for a
separation demand; its fast validity refuses a regime holding a uniform
rule; its reference validity and its unpruned enumeration exist beside
it); the sealed profiles in `code/derivation/observe.py`; and the sealed
Lean kernel and isomorphism structure named in `PROMPT.md`.  No count of
this rung was computed before this file was frozen.

## Declared before the compile: the FW-DEF census this rung commits to

Four classes, as the sibling rungs use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this rung's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion); THIN (one
genuine step, or a direct corollary of a neighbour); CONTENT (everything
else).  Rung seven's rule for inductions is applied: an induction whose
step needs a case analysis on the shape of the step is CONTENT; one
closed by a step lemma and arithmetic alone is THIN.  Rung nine's
recorded lesson is applied before the compile: an assembly of carried
pieces is THIN.

Predicted DEFINITION:

- `plug_mapCtx`
- `derivable_fwd`
- `exhausted_of_rule`
- `no_exhausted_at_genesis`
- `exhaustion_at_one`
- `one_inst_moves_two_pairs`

Predicted THIN:

- `map_inv`
- `plug_args_lt`
- `wfCtx_mapCtx`
- `derivable_bwd`
- `derivable_mapCtx`
- `exhausted_iff_not_distinguishes`
- `holdsTwo_iff_distinguishes`
- `exhausted_of_no_inst`
- `exhausted_of_le_one`
- `exhausted_iso`
- `fresh_form_exhausted`
- `getD_append_lt`
- `separable_step_keep`
- `distinguishes_step_keep`
- `exhaustion_begun_by_rule`
- `exhaustion_ended_by_datum`
- `exhaustion_ended_by_inst`
- `mem_plug_of_hole`
- `derivable_inst_unmentioned`
- `separable_inst_unmentioned`
- `collapsed_inst_unmentioned`
- `slots_ok_of_plug_mem`
- `step_data_le`
- `moved_pairs_meet_mentions`
- `separation_needs_inst`

Predicted CONTENT:

- `ctx_step_keep`
- `exhausted_step_keep`
- `exhaustion_begun_by_inst`
- `collapsed_step_keep`
- `step_wf`
- `separation_needs_mention`
- `collapse_needs_mention_or_rule`
- `response_collapses_a_pair`

The names above are the ones this rung commits to before Lean has run.  A
name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census and
is recorded in `STATUS.md` as unpredicted work.  Several repeat, as
statements, lemmas earlier rungs proved: `map_inv`, `plug_mapCtx`,
`plug_args_lt`, `wfCtx_mapCtx`, `derivable_fwd`, `derivable_bwd` and
`derivable_mapCtx` (rung nine); `separable_step_keep` (rung nine);
`getD_append_lt` (rung five, proved again at rungs eight and nine);
`step_wf` (rung three's `wf_step_any`).  The definitions `isoSymm`
(rung eight) and `HoldsTwo` (rung nine) repeat earlier rungs'.  Each is
proved or stated again here so that the package imports nothing, and
the ledger credits each to its rung.

The Lean objects, declared here so the rows below can name them:
`Distinguishes r f`, that some well-formed context on form `f` tells two
admitted data apart; `Exhausted r f`, that every well-formed context on
form `f` reads every two admitted data alike; `HasExhausted r`, that some
admitted form of `r` is exhausted; `HoldsTwo r`, rung nine's.

## Stage one -- exhaustion, in Lean

- **R-1** (NOT FORCED).  `exhausted_iso` is PROVED as an equivalence for
  every pair of regimes and every inhabitant of the sealed isomorphism
  between them, with the only hypothesis that the form is admitted in
  the source: a form is exhausted exactly when its image is.  No
  well-formedness of either regime is needed.
  Falsifier: OPEN, or needing any hypothesis beyond the form being
  admitted.
- **R-2** (NOT FORCED).  `exhausted_iff_not_distinguishes` and
  `holdsTwo_iff_distinguishes` are PROVED with no hypothesis on the
  regime: a form is exhausted exactly when it does not distinguish, and
  a regime holds two exactly when some form distinguishes.  A form is
  exhausted by construction when it carries a uniform rule, when no held
  instance is on it, when the regime holds at most one datum
  (`exhausted_of_rule`, `exhausted_of_no_inst`, `exhausted_of_le_one`),
  each with no well-formedness hypothesis, and when it has just been
  admitted to a well-formed regime (`fresh_form_exhausted`).
  Falsifier: any of these OPEN, or needing a hypothesis beyond the one
  named.
- **R-3** (NOT FORCED).  `exhausted_step_keep`: a supply, a requirement,
  a form admission and a rule admission keep every exhausted admitted
  form exhausted, on every regime.  `distinguishes_step_keep`: a supply,
  a requirement, a form admission and a datum admission keep every
  distinguishing form distinguishing, on every regime.  And each of the
  other changes is exhibited: exhaustion begun by an instance admission
  and by a rule admission, and ended by a datum admission and by an
  instance admission.  So, besides a form admission adding a fresh
  exhausted form, exhaustion is begun only by instance and rule
  admissions and ended only by datum and instance admissions.
  Falsifier: any keep theorem OPEN or needing a hypothesis on the
  regime, or any of the four exhibits failing.
- **R-4** (NOT FORCED).  `no_exhausted_at_genesis` and
  `exhaustion_at_one`: the sealed empty regime has no exhausted form,
  and the history of one form admission of arity one reaches a regime
  that has one.
  Falsifier: either failing.

## Stage two -- which events move a pair, in Lean

- **R-5** (NOT FORCED).  `collapsed_step_keep`: on every WELL-FORMED
  regime, every accepted event that is not an instance admission keeps
  every collapsed pair collapsed; well-formedness is needed, for the
  datum and form admissions.  `separable_step_keep`: every accepted event
  that is neither an instance nor a rule admission keeps every separable
  pair separable, with no hypothesis.  `separable_inst_unmentioned` and
  `collapsed_inst_unmentioned`: an accepted instance admission whose
  arguments mention neither datum of a pair leaves the pair's
  separability and collapse as they were, with no hypothesis.
  `step_wf`: every accepted event keeps a regime well formed.
  Falsifier: any of these OPEN, or `collapsed_step_keep` proved without
  well-formedness (the prediction is that the hypothesis is used), or
  any other needing a hypothesis beyond the one named.
- **R-6** (NOT FORCED).  `separation_needs_mention`: for every
  well-formed regime and every history the sealed replay accepts from
  it, a pair of admitted data collapsed before and separable after is
  mentioned by the arguments of some instance admission of the history.
  `collapse_needs_mention_or_rule`: a pair separable before and
  collapsed after is so mentioned, or the history holds a rule
  admission.  `moved_pairs_meet_mentions` and `separation_needs_inst`
  follow.
  Falsifier: either OPEN, or needing a hypothesis beyond well-formedness
  of the base and the admission of the pair.
- **R-7** (NOT FORCED).  `one_inst_moves_two_pairs` exhibits a
  well-formed regime and one instance admission after which two pairs,
  both collapsed before, are separable; `response_collapses_a_pair`
  exhibits a well-formed regime, a collapsed pair, and one instance
  admission after which that pair is separable and a pair that was
  separable is collapsed.
  Falsifier: either failing.
- **R-8** (NOT FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.
  Falsifier: the committed axiom log naming any other axiom.

## Stage three -- the finite cross-check

The bases, the bound and the alphabet are rung three's and are not
chosen after seeing a count.

- **Declared rectangle.**  Rung three's, consumed through rung four's
  public population: three bases (EMPTY, L, F), every sequence of at
  most four declared events.
- **Declared responder.**  The sealed `min_responses`, at the sealed
  default bounds (two items, arity two), under each of `mu1` and `mu2`.
  The RESPONDER'S DOMAIN is the set of regimes holding no uniform rule;
  on every other regime the sealed responder refuses to run, and the
  regime is counted OUTSIDE THE DOMAIN.  A DEMAND of a regime in the
  domain is a pair the sealed `collapsed_pairs` returns.  A demand is
  REFUSED under a measure when `min_responses` returns nothing.
- **Declared readings.**  The RESPONDED regime of a response is the
  replay of the response's events from the demanded regime.  A pair of
  data of the demanded regime is MOVED when the sealed `separable`
  differs between the demanded and the responded regimes; it moves
  APART when separable after, TOGETHER when collapsed after.  A pair is
  UNMENTIONED by a response when neither datum is an argument of an
  instance item of the response.  The REACH of a response is the set of
  data of the demanded regime, other than the two demanded, that belong
  to a moved pair.  The ADJACENCY GRAPH, DISTANCE, tie count and
  tie-class count are those of `PROMPT.md`; the tie classes are formed
  by the sealed key procedure on the replay of the demanded pair's
  requirement followed by the response's events, as the sealed engine
  forms them.  The EXHAUSTED COUNT of a regime is the number of its
  forms that separate no two admitted data, read through the sealed
  contexts and derivability.  A TRANSITION is a sequence of length at
  least one with its prefix one event shorter; its KIND is the kind of
  its last event; its CHANGE is the exhausted count after less the
  count before.  The RESPONSE SIGNATURE of a regime under a measure is
  its domain membership, the sorted list over its demands of the cost,
  the tie count, the tie-class count and the sorted list over the
  demand's responses of the number of pairs moved apart, the number
  moved together and the reach size; and the adjacency graph's number
  of edges, the sorted sizes of its connected pieces, and its largest
  finite distance.
- **Declared cross-check family.**  Every regime in the domain reached
  from the EMPTY base.  On it, for every demand and each measure, the
  sealed responder's responses are compared with the minimum, under the
  same measure, of the sealed unpruned enumeration `iter_full_deltas` at
  zero, one and two items filtered by the sealed reference validity
  `response_valid_naive`; refusals are compared too; and the tie-class
  partition of each demand's responses by the sealed key procedure is
  compared with the partition by the sealed brute-force minimum.
- **R-9** (FORCED).  577, 3928 and 14293 sequences; 75, 523 and 1718
  distinct regimes; zero replay mismatches; 402 classes over the 2316
  distinct regimes of all three bases; zero disagreements between the
  key partition and the brute-force partition.
  Falsifier: any other value.
- **R-10** (NOT FORCED).  At every base some distinct regimes lie inside
  the responder's domain and some outside it; the sealed responder
  refuses to run on every regime outside the domain and on none inside.
  Falsifier: a base with no regime on one side, or a regime on which the
  responder's behaviour disagrees with its domain membership.
- **R-11** (NOT FORCED).  Zero demands are refused at EMPTY; at least one
  is refused at L and at least one at F; the two measures refuse exactly
  the same demands.
  Falsifier: a refusal at EMPTY, none at L or at F, or a demand refused
  under one measure and answered under the other.
- **R-12** (NOT FORCED).  Under both measures, at every base: no response
  holds a rule item; every response holds an instance item mentioning a
  demanded datum; and zero responses move an unmentioned pair.
  Falsifier: any such response.
- **R-13** (NOT FORCED).  Every response moves its demanded pair apart.
  Some response moves a pair together: zero such responses at EMPTY, at
  least one at L and at least one at F, under each measure.
  Falsifier: a response not moving its demand apart; a response moving a
  pair together at EMPTY; none at L or at F.
- **R-14** (NOT FORCED).  Under both measures: a response has a nonempty
  reach exactly when it moves at least two pairs (zero mismatches); at
  every response, every datum collapsed before with a demanded datum,
  other than the two demanded, is in the reach (zero violations); at
  every base some response has an empty reach and some a nonempty one.
  Falsifier: a mismatch, a violation, or a base lacking either kind.
- **R-15** (NOT FORCED).  Under both measures, the least length of a
  sequence reaching a regime in the domain whose adjacency graph has an
  edge is three at EMPTY, one at L and zero at F; and at least one
  regime's adjacency graph has a largest finite distance of at least
  two.
  Falsifier: any other least length, or every largest finite distance
  below two.
- **R-16** (NOT FORCED).  The least length of a sequence reaching a
  regime in the domain with a demand of tie-class count at least two is,
  under `mu1`, two at EMPTY, zero at L and zero at F; under `mu2`, three
  at EMPTY, one at L and one at F.  At every demand the `mu2` responses
  are among the `mu1` responses.  At L and at F some demand has tie
  count one under each measure.
  Falsifier: any other least length, a `mu2` response not among the
  `mu1` responses, or no demand of tie count one at L or at F.
- **R-17** (NOT FORCED).  Zero classes of regimes, within any base and
  over all three together, carry two values of the exhausted count, or
  two values of the response signature under either measure.
  Falsifier: any such class.
- **R-18** (NOT FORCED).  At every regime of the rectangle the regime
  holds two exactly when its exhausted count is below its number of
  forms (zero mismatches), and every form carrying a rule is exhausted
  (zero violations).  Over the transitions of all three bases, the
  changes by kind are: supply and requirement exactly zero; form
  admission exactly one; rule admission exactly zero and one; datum
  admission exactly minus one and zero; instance admission exactly
  minus one, zero and one.
  Falsifier: a mismatch, a violation, or any other set of changes for
  any kind.
- **R-19** (NOT FORCED).  The least length of a sequence reaching a
  regime with an exhausted form is one at every base; the least length
  reaching a regime that holds two and has an exhausted form is three at
  L and at F, and no sequence of the EMPTY rectangle reaches one.
  Falsifier: any other least length, or such a regime at EMPTY.
- **R-20** (NOT FORCED).  On the declared cross-check family: zero
  disagreements between the sealed responder and the unpruned minimum,
  under either measure, in responses or in refusals; zero disagreements
  between the key and brute-force tie-class partitions.  Over the whole
  population, every response passes the sealed reference validity:
  zero failures.
  Falsifier: any disagreement or failure.

## Stage four -- the census rows and the input count

- **R-21** (NOT FORCED).  The ledger decides the challenge-five row for
  exhaustion: DEFINABLE, as a property of a form read off the regime's
  own contexts and derivability, carried by the sealed isomorphism with
  no hypothesis on either regime (PROVED); first at one event from the
  empty regime (PROVED at the level of a definition); begun and ended by
  the kinds R-3 names (PROVED and COUNTERMODEL).  FORCED in the seed's
  sense is conditional on an engine, and none is declared; the row says
  so.
  Falsifier: the ledger recording the row otherwise, or without the
  engine condition.
- **R-22** (NOT FORCED).  The ledger decides the rows for adjacency,
  reach and branching: USEFUL REALIZATION, each under the named
  additional declaration that the row's response is the sealed
  responder under one chosen measure, priced in capabilities; the
  event-level statements of R-5 and R-6 PROVED for every well-formed
  regime and history, whatever responder is declared; the numbers FINITE
  COMPUTATION on the rectangle; the distance derived from adjacency with
  no further declaration; FORCED conditional on an engine.
  Falsifier: the ledger recording any of the three as DEFINABLE with no
  declaration, claiming a Lean statement about a minimum response, or
  omitting the engine condition.
- **R-23** (FORCED).  This rung neither reduces the count of declared
  inputs nor proves it at a floor; the value stays two.
  Falsifier: any claim otherwise.
- **R-24** (FORCED).  The receipt regenerates byte-identically, every
  node replays from its base, and the grouped gate time stays under
  fifteen minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.
