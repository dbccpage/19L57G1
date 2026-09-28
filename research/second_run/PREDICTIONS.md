# PREDICTIONS: continuation two -- run forward

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
of this attempt and before any Lean of this tree is built.  Scored
mechanically by `run_forward.py` for the computational rows and by
`test_census.py` for the Lean census rows.  A missed prediction is
recorded next to its value and never edited.  A miss is a finding, not a
defect.

The frozen question is `PROMPT.md`, sha256
`3fd06a04a81e39ee3e9b650fd34f76e0d01788559c7d7f21472ee9a2967a9810`,
committed alone at `c2530b12`.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this attempt, so a hit evidences the ordering of
the work and not insight.  NOT FORCED means the run could have come out
the other way.  An argument written by this session before the run is
not a receipt: a row that leans on one is NOT FORCED.

Sources read before freezing, because a prediction below leans on them:
continuation one's `PROMPT.md`, `PREDICTIONS.md`, `STATUS.md`,
`engine_decl.py`, `engine_probe.py` and Lean `Engine.lean` and
`Kernel.lean`; rung two track two's `rules.py`, `observables.py`,
`generation.py` and `STATUS.md`; rung ten's `response_rows.py`; the
sealed `candidates.py`, `iso.py` and `model.py`; the run's `paper.md`,
`claim_ledger.md` and `MANUAL.md`; the pending extrapolations of rung
two track two and rung three.  One act of apparatus is disclosed: before
the question was frozen, rung two track two's public `build_tree` was
timed on its E-four rule at both readings and both measures, to choose a
node guard that keeps the gate inside fifteen minutes; it printed the
node count and seconds of each of the four trees (one hundred and
twelve, forty, two hundred and fifty and two hundred and fifty-two
nodes), which its committed receipt already records.  Its trees are not
this attempt's runs: they quotient by the number of response rounds,
count only response rounds, and fire growth where these engines may
not.  No count of this attempt was computed before this file was
frozen; the values below were reasoned by hand from the sources.

## Readings applied, recorded before the predictions

Each resolves a point `PROMPT.md` leaves open, is fixed here before any
computation, and binds no later attempt.

- *Carries forward.*  "Every one of which is reached from the root by
  changing rounds only" is read literally on the recorded history: the
  history of every BOUND or GUARD node's representative holds no switch
  marker.  A run that is not closed but fails this is recorded as NOT
  CLOSED, and is not said to carry forward.
- *Closed runs with cycles under ONE VALUE PER NODE.*  The prompt
  declares HOLDS only for a closed acyclic run.  A closed run with a
  cycle and no failure is therefore UNDECIDED, and any set holding one
  is OPEN for that reading unless some run FAILS.  What the quantity
  does on such a run is reported beside it and is not a verdict.
- *Class order.*  The first failing member is the first in the order of
  continuation one's `engine_class()`, reading L before reading F.
- *Merges.*  Every edge whose state falls into a node already present
  is a merge, including a tie edge into a node an earlier edge of the
  same parent created; the label comparison runs at every one.
- *Moves.*  The pairs an edge moves are rung ten's moved pairs from the
  parent's representative regime to the regime the edge's events reach
  from it.  The data outside a response's demanded pair are those other
  than the pair the edge answers.
- *Values at the root.*  Every quantity carried along run paths is zero
  at the root.
- *Invariant candidates.*  The numbers of demands and of honoured
  labelled pairs are read by the engine's generator in the state's mode.

## Declared before the compile: the FW-DEF census this tree commits to

Four classes, as the sibling trees use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this tree's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion); THIN
(one genuine step, a direct corollary of a neighbour, or an assembly of
carried pieces); CONTENT (everything else).  An induction closed by a
step lemma alone is THIN.

Predicted RECONSTRUCTION, every theorem of `Kernel.lean`, the seventeen
continuation one reconstructed: `insertNew_nil`, `insertNew_of_not_mem`,
`insertNew_of_mem`, `mem_insertNew`, `separable_not_collapsed`,
`R2L_wf`, `R2F_wf`, `supply_no_op`, `genesis_underivable`,
`underivable_of_empty`, `collapsed_of_no_insts`, `R2L_collapsed`,
`R2F_collapsed`, `historyL_replays`, `historyF_replays`,
`admission_without_expressive_increase`, `replayE_append`.

Predicted DEFINITION:

- `insertNew_length_le`
- `insertNew_eq_or_succ`
- `switch_keeps_regime`
- `switch_switch`

Predicted THIN:

- `stepE_elems_le`
- `stepE_elems_lt_of_ne`
- `estep_elems_le`
- `estep_elems_lt_of_ne`
- `ereplay_elems_le`
- `ereplay_elems_lt_of_ne`
- `no_return`
- `cycle_regime_const`

Predicted CONTENT:

- `ereplay_regime_eq_of_elems_eq`

The Lean objects, declared here so the rows below can name them.
`elems r`, the number of data of `r` plus the lengths of its lists of
forms, instances, uniform rules and requirements.  `EEvent`, a sealed
event or the switch marker.  `EState`, a regime and a flag for the
mode.  `estep`, one engine event: a sealed event steps the regime by the
sealed step, the switch marker flips the flag and keeps the regime.
`ereplay`, the fold of `estep` over a history, all or nothing.  The
names above are the ones this tree commits to before Lean has run; a
name that changes, a target moved between classes, or a declaration
added beyond this list is visible in the committed census and recorded
in `STATUS.md` as unpredicted work.

## Stage one -- the Lean mirror

- **R-1** (NOT FORCED).  `stepE_elems_le`: no sealed step lowers `elems`.
  `stepE_elems_lt_of_ne`: a sealed step that changes the regime raises
  `elems`.  `estep_elems_le` and `estep_elems_lt_of_ne`: the same for
  every engine event.  `switch_keeps_regime` and `switch_switch`: the
  switch marker keeps the regime, and two of them return the state.
  Each with no hypothesis beyond the step's success.
  Falsifier: any OPEN or needing a further hypothesis.
- **R-2** (NOT FORCED).  `ereplay_elems_le`: no history of engine events
  lowers `elems`.  `ereplay_regime_eq_of_elems_eq`: a history that
  leaves `elems` unchanged leaves the regime unchanged.
  `ereplay_elems_lt_of_ne`: a history that changes the regime raises
  `elems`.  `no_return`: after a history that changes the regime, no
  history reaches a state holding the first regime.
  `cycle_regime_const`: on a history that returns to its starting state,
  every intermediate state holds the starting regime.  Each for every
  history, whoever chose it.
  Falsifier: any OPEN or needing a hypothesis beyond the replays' success.
- **R-3** (NOT FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.
  Falsifier: the committed axiom log naming any other axiom.
- **R-4** (NOT FORCED).  Every declaration `Kernel.lean` shares with the
  pinned sealed sources is identical to it after comments and namespace
  lines are stripped and whitespace is normalized.
  Falsifier: any differing declaration.

## Stage two -- the runs

Declared bounds: the sealed candidate space at the sealed bounds (at most
two items, arities at most two), unpruned, with rung one's no-op filter
as continuation one consumes it; growth enabled below four data; fifteen
rounds; a node guard of two hundred and fifty per run; the sealed
permutation budget.

- **R-5** (FORCED).  One hundred and forty-four engines, one hundred and
  eight seed-literal, two hundred and eighty-eight runs.
  Falsifier: any other count.
- **R-6** (NOT FORCED).  Zero replay mismatches over every node and every
  edge; zero quotient defects over every merge; zero disagreements
  between the sealed key partition and the brute-force partition.
  Falsifier: any mismatch, defect or disagreement.
- **R-7** (NOT FORCED).  The engines whose runs hold a response edge at
  both readings are exactly continuation one's sixty-four LIVE members,
  and no run of any other engine holds a response edge at either
  reading.  So the QUIET engines are the eighty others: every E-seven
  and E-eight member, and every E-one, E-two, E-three, E-five, E-six and
  E-nine member whose continuation does not hold switch.
  Falsifier: any other set.
- **R-8** (NOT FORCED).  The quiet runs, at L and at F: with HALT, one
  node, a FIXPOINT, no edge; with growth alone, three nodes and two
  edges at L and two nodes and one edge at F, ending in a FIXPOINT at
  four data; with switch alone, two nodes and two edges, no terminal;
  with growth and switch, six nodes and ten edges at L and four nodes and
  six edges at F, no terminal.  Every quiet run is closed.
  Falsifier: any other shape.
- **R-9** (NOT FORCED).  At reading L, the run of E-four with `mu2`, HALT
  and either validity member has twenty-three nodes and thirty edges:
  seven FIXPOINT nodes, one BOUND node at stage fifteen, no GUARD and no
  REFUSAL.
  Falsifier: any other count.
- **R-10** (NOT FORCED).  At reading L, the run of E-four with `mu1`,
  HALT and either validity member has fifty-three nodes and seventy-six
  edges: twenty-one FIXPOINT nodes, three BOUND nodes at stage fifteen,
  no GUARD and no REFUSAL.
  Falsifier: any other count.
- **R-11** (NOT FORCED).  At both readings, no run of an E-four member
  is closed, and no run of an E-one, E-two, E-three, E-five or E-nine
  member whose continuation holds switch is closed.  At reading L, the
  run of every E-six member with switch alone is closed.
  Falsifier: any such run closed, or such an E-six run not closed.
- **R-12** (NOT FORCED).  Under `mu1` at reading F, the run of every
  E-four member holds a GUARD node.
  Falsifier: any of those eight runs with no GUARD node.
- **R-13** (NOT FORCED).  The members that carry forward at both
  readings are exactly the eight E-four members whose continuation is
  HALT or growth alone.  The streamless ones among them are the four
  E-four members with HALT.  Among the eight, the count-minimal members
  are E-four with `mu1`, member one, HALT and E-four with `mu2`, member
  one, HALT, at count six under both readings of growth; the
  inclusion-minimal members are the same two; no member is initial.
  Falsifier: any other set, count or initial member.
- **R-14** (NOT FORCED).  No response edge of any run carries a datum.
  Falsifier: one that does.
- **R-15** (NOT FORCED).  For every rule, measure and continuation, the
  runs of the member-one and member-two engines are run-isomorphic at
  both readings.
  Falsifier: any pair that is not.
- **R-16** (NOT FORCED).  The class holds thirty-six run-isomorphism
  classes: one each for the quiet engines with HALT, with growth alone,
  with switch alone, and with growth and switch; eight for E-four, one
  per measure and continuation; and twenty-four for the E-one, E-two,
  E-three, E-five, E-six and E-nine members holding switch, one per
  rule, measure and continuation.  The run partition refines
  continuation one's probe partition.
  Falsifier: any other count, or a run class meeting two probe classes.

## Stage three -- the census

Every verdict below is over the whole class unless another set is named,
at both readings.

- **R-17** (NOT FORCED).  The stage readings.  Two-ness is FORCED at
  round zero with the value false and NOT FORCED at every round from one
  to fifteen.  The profile class count is FORCED at round zero with the
  value one and NOT FORCED at every round from one to fifteen.
  Symmetry is FORCED at round zero with the value two at L and six at F,
  and NOT FORCED at every round from one to fifteen.  Exhaustion is
  FORCED at rounds zero and one with the value zero and NOT FORCED at
  every round from two to fifteen.  Branching is NOT FORCED at every
  round from zero to fifteen.
  Falsifier: any other verdict or value at any round.
- **R-18** (NOT FORCED).  The run readings of two-ness, adjacency, reach
  and recurrence are NOT FORCED, each first failing at E-one with `mu1`,
  member one and HALT, at reading L.  The run reading of the class count
  is NOT FORCED, first failing at E-one with `mu1`, member one and
  switch alone, at reading L.  Succession under EVERY is NOT FORCED.
  Succession under CHANGING and duration are OPEN: no run FAILS either.
  Falsifier: any other verdict or first failing member.
- **R-19** (FORCED).  The run readings of an invariant and of
  irreversibility are FORCED AT BOUND: no edge of any run lowers the
  element count, and no changing edge of any run lies on a cycle; the
  runs that are not closed make it AT BOUND.  Every cycle of every run
  is made of switch edges only.
  Falsifier: an edge lowering the element count, a changing edge on a
  cycle, a cycle holding another edge, or no run left open.
- **R-20** (NOT FORCED).  Over the LIVE members, the run readings of
  adjacency and reach are NOT FORCED, each first failing at E-four with
  `mu1`, member one and HALT, at reading L; and at reading F both hold
  in the run of every LIVE member.
  Falsifier: any other verdict, first failing member, or a LIVE run at F
  in which either does not hold.
- **R-21** (NOT FORCED).  Every stage reading is forced at every complete
  round within one engine for exactly seventy-four engines: the eighty
  quiet engines less the eight E-seven and E-eight members with growth
  and switch, and the two E-six members with `mu2` and switch alone.
  Falsifier: any other set.
- **R-22** (NOT FORCED).  The invariant candidates.  The element count
  and the numbers of data, forms, instances and uniform rules are never
  lowered along any edge of any run of any of the one hundred and
  forty-four engines.  The profile class count is never lowered in the
  runs of each of the eighty quiet engines, and is lowered on some edge
  of some run of each of the fifty-six active engines whose rule is not
  E-six.
  Falsifier: any other outcome for those engines.

## Stage four -- the answers

- **R-23** (NOT FORCED).  The ledger answers the seed's required question
  one within the declared bounds and under the literal reading of
  carrying forward: four streamless engines carry forward at both
  readings, so under the input tally the grammar is carried forward
  within the bounds by an engine that declares the stake and not the
  stream.  The ledger records this as a finite computation at the
  declared bounds, not as a proof that one is the floor and not as a
  reduction of the seed's count of declared inputs outside those
  bounds.
  Falsifier: the ledger recording a floor proof, an unbounded reduction,
  or no streamless engine carrying forward.
- **R-24** (FORCED).  The receipt regenerates byte-identically, every
  node and edge replays, and the grouped gate time stays under fifteen
  minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.

## Not scored here

Rung two track two's extrapolation X, to five data, and rung three's
I-X, a first count under a run driven by a responder from the empty
base, stay PENDING: these runs hold at most four data and start at the
sealed genesis readings, not at the empty base.
