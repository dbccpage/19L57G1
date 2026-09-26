# PREDICTIONS: continuation one -- the engine

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this tree is built.  Scored mechanically by
`run_engine.py` for the computational rows and by `test_census.py` for
the census rows.  A missed prediction is recorded next to its value and
never edited.  A miss is a finding, not a defect.

The frozen question is `PROMPT.md`, sha256
`7a2768078d63dd222398c9d3f1b3b953ee753ac094a8a01228e3adc7dbfba919`,
committed alone at `03b67607`.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this attempt, so a hit evidences the ordering of
the work and not insight.  NOT FORCED means the run could have come out
the other way.  An argument written by this session before the run is
not a receipt: a row that leans on one is NOT FORCED.

Sources read before freezing, because a prediction below leans on them:
rung two's `rules.py`, `observables.py`, `generation.py` and `STATUS.md`
(the nine rules, the observables each reads, the dynamic no-regress
validity, the unpruned minimum responses, and the recorded behaviour of
E-four under growth); the two-sided tree's `two_sided.py` and `STATUS.md`
(the honour relation and the demand reading); the identification tree's
`dual.py` (its switch, its automorphisms over the sealed serialization);
rung one's `stream.py` (validity member two and the no-op filter); the
sealed `model.py`, `engine.py` (the Python genesis L holds two data and
nothing else, F three data and nothing else, neither a requirement) and
`candidates.py` (the unpruned enumeration and both measures); rung ten's
`PROMPT.md`, `PREDICTIONS.md`, `STATUS.md`, `FWDEF_CENSUS.json` and Lean
package; rung nine's `Carry.lean`.  The probe values below were reasoned
by hand from those sources.  No count of this attempt was computed
before this file was frozen.

## Declared before the compile: the FW-DEF census this tree commits to

Four classes, as the sibling rungs use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this tree's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion, including
exhaustion over the declared finite class); THIN (one genuine step, or a
direct corollary of a neighbour, or an assembly of carried pieces);
CONTENT (everything else).  Rung seven's rule for inductions is applied:
an induction closed by a step lemma alone is THIN.

Predicted RECONSTRUCTION, every theorem of `Kernel.lean`, the seventeen
rung ten reconstructed: `insertNew_nil`, `insertNew_of_not_mem`,
`insertNew_of_mem`, `mem_insertNew`, `separable_not_collapsed`,
`R2L_wf`, `R2F_wf`, `supply_no_op`, `genesis_underivable`,
`underivable_of_empty`, `collapsed_of_no_insts`, `R2L_collapsed`,
`R2F_collapsed`, `historyL_replays`, `historyF_replays`,
`admission_without_expressive_increase`, `replayE_append`.
`IsoKernel.lean` reconstructs definitions only.

Predicted DEFINITION:

- `plug_mapCtx`
- `derivable_fwd`
- `sortPair_swap`
- `flip_flip`
- `e3_flip_eq_e4`
- `e4_flip_eq_e3`
- `e1_flip_demands`
- `carried_flip`
- `e8_quiet_without_reqs`
- `genL_replays`
- `genL_one_orbit`
- `genL_collapsed`
- `e4_demands_at_genL`
- `e1_flip_demands_at_genL`
- `fixpoint_of_halt`
- `class_size`
- `literal_size`
- `count_ge_six`
- `count_six_members`
- `literal_count_ge_seven`
- `literal_count_seven_members`
- `literal_count2_seven_members`
- `same_caps_e3_e4`

Predicted THIN:

- `map_inv`
- `plug_args_lt`
- `wfCtx_mapCtx`
- `derivable_bwd`
- `derivable_mapCtx`
- `separable_iso`
- `collapsed_iso`
- `sortPair_map`
- `separable_iso_iff`
- `collapsed_iso_iff`
- `reqMember_iso`
- `e1_never_demands`
- `demand_carried`
- `e1_carried`
- `e3_carried`
- `e4_carried`
- `e8_carried`
- `e3_quiet_at_genL`
- `minima_differ_at_genL`
- `step_at_demand_is_response`
- `run_named`
- `e1_engine_quiet`
- `e1_halt_no_step`
- `no_one_declaration`
- `no_initial`
- `no_initial_of_two_measures`

Predicted CONTENT:

- `oneOrbit_iso`

The names above are the ones this tree commits to before Lean has run.
A name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census
and is recorded in `STATUS.md` as unpredicted work.  Several repeat, as
statements, lemmas earlier rungs proved: `map_inv`, `plug_mapCtx`,
`plug_args_lt`, `wfCtx_mapCtx`, `derivable_fwd`, `derivable_bwd`,
`derivable_mapCtx`, `separable_iso` and `collapsed_iso` (rung nine); the
definition `isoSymm` is rung eight's.  Each is proved or stated again
here so that the package imports nothing, and the ledger credits it.

The Lean objects, declared here so the rows below can name them.
`isoTrans σ τ`, the composite of two inhabitants of the sealed
isomorphism.  `OneOrbit r i j`, that some inhabitant of `Iso r r` sends
`i` to `j` -- the mirror of O-four.  `ReqMember r i j`, that the sorted
pair is a requirement of `r` -- the mirror of O-six.  A `Reading` is two
predicates on a regime and two data, labelled apart and labelled same;
`Reading.flip` exchanges them.  `Demand ρ r i j` holds when `i` and `j`
are labelled apart and collapsed, or labelled same and separable.  The
readings `E1`, `E3`, `E4` and `E8` mirror rung two's rules of those
names: `E1` apart when separable and same when collapsed; `E3` same on
one orbit and apart off it; `E4` the reverse; `E8` apart on a
requirement and never same.  `Carried ρ` says both predicates of `ρ` are
carried, in both directions, by every inhabitant of the sealed
isomorphism at admitted data.  `genL` is the regime of two data and
nothing else.  In `Engine.lean`: an `Engine` over a state type is a
demand predicate, a response predicate, a continuation predicate and an
apply function; `Named`, `Step` and `Run` are the histories the
declaration names at a state, one step, and a run.  In `Census.lean`:
the nine rules, the six observables, the capabilities, a declaration of
a class member, its capability list and count, the class list and the
seed-literal list, and the second count reading growth as two.

## Stage one -- the declaration and the stakes, in Lean

- **C-1** (NOT FORCED).  `fixpoint_of_halt`: an engine with no enabled
  continuation has no step from a demand-free state.
  `step_at_demand_is_response`: every step from a state with a demand is
  a response to one of its demands.  `run_named`: every history of every
  run is named by the declaration at the state it is taken from.  Each
  with no hypothesis beyond the one named.  `e1_engine_quiet` and
  `e1_halt_no_step`: an engine whose generator is `E1` has no demand at
  any plain state, and with no continuation has no step from any plain
  state.
  Falsifier: any of these OPEN or needing a further hypothesis.
- **C-2** (NOT FORCED).  `oneOrbit_iso` is PROVED as an equivalence for
  every pair of regimes, every inhabitant of the sealed isomorphism
  between them and every two data admitted in the source, with no other
  hypothesis; likewise `reqMember_iso`, `separable_iso_iff` and
  `collapsed_iso_iff`.
  Falsifier: any OPEN or needing a hypothesis beyond admission of the
  two data.
- **C-3** (NOT FORCED).  `demand_carried`: for every carried reading, a
  demand is carried to its image and back.  `e1_carried`, `e3_carried`,
  `e4_carried` and `e8_carried`: each of the four readings is carried;
  `carried_flip`: the flip of a carried reading is carried.  So the
  labels and demands of E-one, E-three, E-four and E-eight, in both
  modes, are invariant under renaming for every regime.
  Falsifier: any OPEN or needing a hypothesis beyond admission.
- **C-4** (NOT FORCED).  `e1_never_demands`: no regime and no two data
  give a demand under `E1`, with no hypothesis.  `e1_flip_demands`:
  under the flip of `E1` every collapsed pair and every separable pair
  is a demand.  `e3_flip_eq_e4` and `e4_flip_eq_e3` hold by `rfl`, and
  `flip_flip`.  `e8_quiet_without_reqs`: a regime holding no requirement
  gives no demand under `E8` or its flip.
  Falsifier: any failing, or `e1_never_demands` needing a hypothesis.
- **C-5** (NOT FORCED).  `genL_replays`: the sealed genesis history of
  reading L without its requirement replays to `genL`.
  `genL_one_orbit`, `genL_collapsed`, `e4_demands_at_genL`,
  `e3_quiet_at_genL`, `e1_flip_demands_at_genL`, and
  `minima_differ_at_genL`: at `genL` the reading `E4` has a demand and
  `E1` has none.
  Falsifier: any failing.
- **C-6** (NOT FORCED).  Over the declared class in Lean: one hundred and
  forty-four members (`class_size`) and one hundred and eight in the
  seed-literal subclass (`literal_size`); every count at least six
  (`count_ge_six`), sixteen members of count six (`count_six_members`);
  every seed-literal count at least seven, thirty-two of count seven
  (`literal_count_ge_seven`, `literal_count_seven_members`); sixteen of
  count seven when growth counts two (`literal_count2_seven_members`);
  no member of count one (`no_one_declaration`); no member whose
  capability list is inside every member's (`no_initial`); none in any
  subclass holding members of both measures
  (`no_initial_of_two_measures`); `E3` and `E4` members agreeing
  elsewhere have one capability list (`same_caps_e3_e4`).
  Falsifier: any other value or any failing.
- **C-7** (NOT FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.
  Falsifier: the committed axiom log naming any other axiom.

## Stage two -- the class census, computed

- **C-8** (FORCED).  One hundred and forty-four members and one hundred
  and eight seed-literal members; every count between six and ten; the
  count-minimal members of the class are the sixteen of count six --
  every rule but E-six, each measure, member one, HALT -- and of the
  seed-literal subclass the thirty-two of count seven -- the same eight
  rules and two measures, member one, growth alone or switch alone.
  Growth counted as two: the class minima unchanged; the seed-literal
  minima the sixteen with switch alone.
  Falsifier: any other value.
- **C-9** (FORCED).  The inclusion-minimal members of the class and of
  the seed-literal subclass are exactly their count-minimal members.
  Thirty-two unordered pairs of distinct members share one capability
  set: E-three with E-four and E-two with E-seven, at each of the sixteen
  settings of measure, validity and continuation.
  Falsifier: any other set or count.
- **C-10** (FORCED).  No member has count one, so every label calling a
  member one declaration is refused, and the refusal names the member
  and its count.
  Falsifier: a member of count one, or a refusal that does not fire.

## Stage three -- the probe

Declared bounds: the sealed candidate space at the sealed bounds (at most
two items, arities at most two), unpruned, the no-op filter of rung one;
growth enabled below four data; the probe of `PROMPT.md`, to level two.

- **C-11** (NOT FORCED).  In plain mode at both genesis regimes, E-four
  is the only rule with a demand: one at L and three at F, every one of
  kind apart; every other rule's root is demand-free.  In flipped mode
  at the genesis regimes, E-one, E-two, E-three, E-five, E-six and E-nine
  demand every held pair apart (one at L, three at F), and E-four,
  E-seven and E-eight have no demand.  Every growth state of the probe
  is demand-free.
  Falsifier: any other demand at any of these states.
- **C-12** (NOT FORCED).  Every demand at a genesis regime, plain or
  flipped, is answered at two items under both measures and both
  validity members, and the two members give the same minima there.
  At L the one demand has six tied minima under `mu1` and two under
  `mu2`; at F each of the three has ten under `mu1` and two under
  `mu2`.  Every minimum is one form admission and one instance
  admission, and none holds a datum item.  No demand of the probe is
  refused.
  Falsifier: any other cost, tie count or item shape, a disagreement
  between the members, or a refusal.
- **C-13** (NOT FORCED).  Every level-one state reached by a response
  from an E-four root reads at least one demand of kind same; at L each
  such state reads exactly one demand, of kind same.
  Falsifier: such a state with no same demand, or at L with any other
  demand.
- **C-14** (NOT FORCED).  Exactly sixty-four members are LIVE: the
  sixteen whose rule is E-four, and the forty-eight whose rule is E-one,
  E-two, E-three, E-five, E-six or E-nine and whose continuation holds
  switch.  Exactly the sixteen E-four members are TWO-KINDED.
  Falsifier: any other set.
- **C-15** (NOT FORCED).  The count-minimal LIVE members: of the class,
  the two E-four members with member one and HALT; of the seed-literal
  subclass, fourteen -- the four E-four members with member one and
  growth alone or switch alone, and the ten E-one, E-two, E-three,
  E-five and E-nine members with member one and switch alone.  Growth
  counted as two: two and twelve.  The count-minimal TWO-KINDED members:
  two of the class, four of the seed-literal subclass, two of it when
  growth counts two.
  Falsifier: any other set.
- **C-16** (NOT FORCED).  No minimum set above is unique up to
  probe-isomorphism.  The numbers of probe-isomorphism classes: the class
  minima three; the seed-literal minima six, and five when growth counts
  two; the LIVE minima two of the class and four of the seed-literal
  subclass, and four when growth counts two; the TWO-KINDED minima two
  in each of the three.
  Falsifier: a minimum set of one class, or any other class count.
- **C-17** (NOT FORCED).  No minimum set above has an initial member
  under inclusion of declarations: every one holds members of both
  measures.
  Falsifier: an initial member of any of them.
- **C-18** (NOT FORCED).  Every node of every probe replays from its
  genesis by the engine's replay rule, and every edge holds exactly the
  events of the capability it is attributed to: zero mismatches and zero
  violations.  The attribution check refuses an edge carrying a
  requirement, naming it.
  Falsifier: any mismatch, violation or silent acceptance.
- **C-19** (NOT FORCED).  The distinct situations of member one in the
  probe -- a regime, a demand and the set of pairs honoured before --
  number four: the one at L and the three at F.  On one representative
  of each, under each measure, this tree's responder with the clause of
  member two switched off agrees with rung two's minimum responses; and
  every other probe situation agrees with its representative.  The
  sealed key procedure and the brute-force minimum give one partition of
  every probe regime; the probe-isomorphism decided by labels agrees with
  an exhaustive search over the bijections of level-one states on every
  pair of probes compared.  Zero disagreements in each.
  Falsifier: any other number of situations or any disagreement.

## Stage four -- the answers, the census and the input count

- **C-20** (NOT FORCED).  The ledger answers the seed's required
  questions four and ten, on this declared class and probe: a minimal
  engine exists in every subclass named above (DEFINITION over the
  finite class); it is not unique up to probe-isomorphism in any
  (COUNTERMODEL, the probe, with `minima_differ_at_genL` in Lean for the
  class minima); no member is initial under inclusion of declarations
  (PROVED, `no_initial` and `no_initial_of_two_measures`), so the
  universal property is refused for this reading of morphism and the
  refusal is scoped to it.
  Falsifier: the ledger recording any of the three otherwise.
- **C-21** (NOT FORCED).  No row of the challenge-five census has its
  FORCED column decided here: every FORCED column stays conditional on
  running the engines, which is the second attempt's.
  Falsifier: the ledger deciding a FORCED column.
- **C-22** (NOT FORCED).  The input tally records thirty-two LIVE
  members whose declaration carries the stake and not the stream: the
  eight E-four members with HALT or switch alone, and the twenty-four
  E-one, E-two, E-three, E-five, E-six and E-nine members with switch
  alone.  This attempt neither reduces the count of declared inputs nor
  proves it at a floor; the value stays two, and whether such a member
  carries the grammar forward is named for the second attempt.
  Falsifier: any other tally, or any claim of a reduction or a floor.
- **C-23** (FORCED).  The receipt regenerates byte-identically, every
  node replays from its genesis, and the grouped gate time stays under
  fifteen minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.
