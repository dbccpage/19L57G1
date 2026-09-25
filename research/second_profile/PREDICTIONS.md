# PREDICTIONS: rung nine -- two-ness and the observational classes

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_profile.py` for the computational rows and by `test_census.py` for
the census rows.  A missed prediction is recorded next to its value and
never edited.  A miss is a finding, not a defect.

The frozen question is `PROMPT.md`, sha256
`df68d1cc735c3bfc8559e3dd96e3fc93b02f008cfdcb0679bbb1b19b8575a5f7`.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this rung, so a hit evidences the ordering of the
work and not insight.  NOT FORCED means the run could have come out the
other way.  An argument written by this rung's own session before the
run is not a receipt: a row that leans on one is NOT FORCED.

Receipts and sources read before freezing, because a prediction below
leans on them: rung four's `receipts/iso_index.json` (577, 3928 and
14293 sequences; 75, 523 and 1718 distinct regimes at EMPTY, L and F;
2316 distinct regimes in all, in 402 classes of the sealed key
procedure, with zero disagreements against the sealed brute-force
minimum); rung eight's `receipts/class_count.json` (54, 174 and 265
classes within EMPTY, L and F); the declared alphabet of the rectangle
in `research/second_nofirst/nofirst.py` (one supply token; five fresh
datum tokens, taken in order; every instance, rule and requirement the
regime allows is offered, whether held or not; arities one and two; at
most five data, two forms and four events); the sealed Python genesis
histories in `code/derivation/engine.py` (the Python base L holds two
data and nothing else, and the Python base F three data and nothing
else: neither holds a requirement, where the sealed Lean reading regimes
`R2L` and `R2F` each hold one, as rung eight's handoff warns); the
sealed profiles in `code/derivation/observe.py`; and the sealed Lean
kernel and isomorphism structure named in `PROMPT.md`.

## Declared before the compile: the FW-DEF census this rung commits to

Four classes, as the sibling rungs use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this rung's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion); THIN (one
genuine step, or a direct corollary of a neighbour); CONTENT (everything
else).

Predicted DEFINITION:

- `plug_mapCtx`
- `derivable_fwd`
- `collapsed_refl`
- `collapsed_symm`
- `collapsed_trans`
- `insertNew_le`
- `twoness_at_four`
- `twoness_at_two_L`
- `twoness_at_two_F`
- `two_classes_at_four`

Predicted THIN:

- `map_inv`
- `plug_args_lt`
- `wfCtx_mapCtx`
- `derivable_bwd`
- `separable_iso`
- `holdsTwo_iso`
- `holdsTwo_of_reps`
- `reps_of_no_insts`
- `no_twoness_without_insts`
- `step_parts_le`
- `holdsTwo_parts`
- `twoness_needs_four`
- `twoness_needs_two_L`
- `twoness_needs_two_F`
- `getD_append_lt`
- `holdsTwo_step_keep`
- `twoness_lost_by_rule`

Predicted CONTENT:

- `derivable_mapCtx`
- `collapsed_iso`
- `reps_iso`
- `replay_parts_le`
- `separable_step_keep`
- `twoness_lost_by_inst`

The names above are the ones this rung commits to before Lean has run.  A
name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census and
is recorded in `STATUS.md` as unpredicted work.  One of them repeats, as
a statement, a lemma an earlier rung proved: `getD_append_lt` (rung
five, proved again at rung eight).  The definition `isoSymm`, the sealed
isomorphism with its maps exchanged, repeats rung eight's.  Both are
proved or stated again here so that the package imports nothing, and the
ledger credits each to its rung.

The Lean objects, declared here so the rows below can name them:
`isoSymm`; `mapCtx σ c`, the context `c` carried along an isomorphism
`σ` -- its form by the form map, each filled slot by the data map, each
hole kept a hole; `HoldsTwo r`, that some two admitted data of `r` are
separable; `Reps r l`, that `l` is a representative list of `r` as
`PROMPT.md` declares it; `parts r`, the number of data plus the lengths
of the lists of forms and of instances.

## Stage one -- observation across the isomorphism, in Lean

- **Q-1** (NOT FORCED).  `separable_iso` and `collapsed_iso` are PROVED
  for every pair of regimes and every inhabitant of the sealed
  isomorphism between them, with the only hypotheses that the two data
  are admitted in the source: separability and collapse of the two data
  are carried to their images.  Neither needs well-formedness, nor
  duplicate-freedom, of either regime.
  Falsifier: either OPEN, or needing any hypothesis beyond the two data
  being admitted.
- **Q-2** (NOT FORCED).  `holdsTwo_iso` is PROVED as an equivalence --
  a regime holds two exactly when an isomorphic regime does -- with no
  hypothesis on either regime; and `reps_iso`: a representative list of
  the source, carried by the data map, is a representative list of the
  target, of the same length, with no hypothesis.
  Falsifier: either OPEN, or needing a hypothesis.
- **Q-3** (FORCED).  Collapse is reflexive, symmetric and transitive, by
  unfolding: `collapsed_refl`, `collapsed_symm`, `collapsed_trans`.
  Falsifier: any of the three OPEN.

## Stage two -- what holding two needs, in Lean

- **Q-4** (NOT FORCED).  `holdsTwo_parts`: a regime that holds two has
  at least two data, at least one form and at least one instance, with
  no hypothesis on the regime.  `replay_parts_le`: every history that
  replays reaches a regime whose `parts` is at most the base's plus the
  length of the history.  So `twoness_needs_four`: every history from
  the sealed empty regime reaching a regime that holds two has length at
  least four; and `twoness_needs_two_L`, `twoness_needs_two_F`: from each
  sealed Lean reading regime, at least two.  The bounds are attained:
  `twoness_at_four` exhibits a history of four events from the empty
  regime -- a datum, a datum, a form of arity one, the instance of that
  form at the first datum -- and `twoness_at_two_L`, `twoness_at_two_F`
  exhibit the last two of those events from each reading regime.
  `two_classes_at_four` exhibits the representative list of both data
  at the regime `twoness_at_four` reaches.
  Falsifier: any of these OPEN, a bound other than four and two, or a
  witness failing to compute.

## Stage three -- which events keep and which end it, in Lean

- **Q-5** (NOT FORCED).  `separable_step_keep` is PROVED for every
  regime, every pair of data and every event that is neither an instance
  admission nor a rule admission: a pair separable before the event is
  separable after it.  `holdsTwo_step_keep` follows.  No hypothesis on
  the regime is needed.
  Falsifier: either OPEN, or needing well-formedness.
- **Q-6** (NOT FORCED).  `twoness_lost_by_inst` and
  `twoness_lost_by_rule` each exhibit a regime that holds two and one
  event of the named kind the sealed step accepts, after which the
  regime does not hold two.  So holding two is not kept by every event,
  and the kinds that can end it are exactly the two that
  `separable_step_keep` excludes.
  Falsifier: either countermodel failing, or needing an event the sealed
  step refuses.
- **Q-7** (NOT FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.
  Falsifier: the committed axiom log naming any other axiom.

## Stage four -- the finite cross-check

The bases, the bound and the alphabet are rung three's and are not
chosen after seeing a count.

- **Declared rectangle.**  Rung three's, consumed through rung four's
  public population: three bases (EMPTY, L, F), every sequence of at
  most four declared events.  A regime HOLDS TWO, in Python, when two of
  its admitted data have different sealed profiles.  Its CLASS COUNT is
  the number of distinct sealed profiles among its admitted data.  A
  TRANSITION is a sequence of length at least one together with its
  prefix one event shorter; its KIND is the kind of its last event, and
  its CHANGE is the class count after it less the class count before.
  A transition ENDS two-ness when the regime before holds two and the
  regime after does not.  A datum is NAMED at a regime when it is an
  argument of some held instance.
- **Q-8** (FORCED).  577, 3928 and 14293 sequences; 75, 523 and 1718
  distinct regimes; zero replay mismatches; 54, 174 and 265 classes
  within EMPTY, L and F; 402 classes over the 2316 distinct regimes of
  all three; zero disagreements between the key partition and the
  brute-force partition.
  Falsifier: any other value.
- **Q-9** (NOT FORCED).  The least length of a sequence reaching a
  regime that holds two is four at EMPTY, two at L and two at F.  At
  EMPTY exactly twenty-two sequences reach a regime that holds two, all
  of length four, reaching six distinct regimes in three classes of the
  sealed key procedure.
  Falsifier: any other least length, or any other of the three EMPTY
  counts.
- **Q-10** (FORCED).  At every regime of the rectangle, the regime holds
  two exactly when its class count is at least two: zero mismatches.
  Falsifier: a mismatch.
- **Q-11** (NOT FORCED).  The largest class count reached is two at
  EMPTY, three at L and four at F; and at every regime the class count
  is at most the number of data, and at most the number of named data
  plus one: zero violations.
  Falsifier: any other largest value, or a violation.
- **Q-12** (NOT FORCED).  Zero classes of regimes, within any base and
  over all three together, carry two values of holding two, or two
  values of the class count.
  Falsifier: any such class.
- **Q-13** (NOT FORCED).  No transition at EMPTY ends two-ness; at L and
  at F the kinds of the transitions ending two-ness are exactly instance
  admission and rule admission.
  Falsifier: an ending transition at EMPTY, or any other set of kinds at
  L or F.
- **Q-14** (NOT FORCED).  Over the transitions of all three bases, by
  kind: every change by a supply, a requirement or a form admission is
  zero; the changes by a datum admission are exactly zero and one; the
  changes by a rule admission are exactly minus two, minus one and zero;
  the changes by an instance admission include minus one, zero, one and
  two, and every one lies between minus two and two inclusive.
  Falsifier: any other set, or a change outside the stated range.

## Stage five -- the census rows and the input count

- **Q-15** (NOT FORCED).  The ledger decides the challenge-five census
  row for two-ness: DEFINABLE, as a property of the regime's own
  observables that the sealed isomorphism carries with no hypothesis
  (PROVED); first at four events from the empty regime and two from each
  reading regime (PROVED bound, exhibited witness); not kept by every
  event, ended only by instance and rule admissions (PROVED and
  COUNTERMODEL); with no decision procedure built in Lean, which stays
  rung three's X-1.  FORCED in the seed's sense is conditional on an
  engine, and no engine is declared yet; the row says so.
  Falsifier: the ledger recording the row without the engine condition,
  or without its evidence classes.
- **Q-16** (NOT FORCED).  The ledger decides the row for observational
  classes: DEFINABLE as a relation that the sealed isomorphism carries
  both ways and as representative lists it carries, with no hypothesis
  (PROVED); the class count as a NUMBER is a finite computation on the
  rectangle, and in Lean it is OPEN behind a decision procedure; FORCED
  is conditional on an engine.
  Falsifier: the ledger claiming a Lean count, or omitting the engine
  condition.
- **Q-17** (FORCED).  This rung neither reduces the count of declared
  inputs nor proves it at a floor; the value stays two.
  Falsifier: any claim otherwise.
- **Q-18** (FORCED).  The receipt regenerates byte-identically, every
  node replays from its base, and the grouped gate time stays under
  fifteen minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.
