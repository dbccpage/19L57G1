# PREDICTIONS: rung five -- the automorphisms of a regime along a history

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_symmetry.py` for the computational rows and by `test_census.py` for
the census rows.  A missed prediction is recorded next to its value and
never edited.  A miss is a finding, not a defect.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this rung, so a hit evidences the ordering of the
work and not insight.  NOT FORCED means the run could have come out the
other way.

Receipts read before freezing, because a prediction below leans on them:
rung four's `receipts/iso_index.json` (automorphism sizes from one to two
hundred and forty over 2316 regimes; 577, 3928 and 14293 sequences) and
the sealed Python readings, which carry two data (L) and three data (F)
and no requirement at either.  Rung four's one computational miss came
from reading the Lean reading regimes, which carry a requirement, in
place of these; they are not used here.

## Declared before the compile: the FW-DEF census this rung commits to

Four classes, as the sibling rungs use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this rung's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion); THIN (one
genuine step, or a direct corollary of a neighbour); CONTENT (everything
else).

Predicted DEFINITION:

- `sameMaps_symm`
- `supply_keeps`
- `stepE_inst`
- `stepE_rule`
- `stepE_req`
- `stepE_datum`
- `stepE_form`

Predicted THIN:

- `inst_meet`
- `inst_meet_after`
- `rule_fixed_of_survives`
- `rule_survives_of_fixed`
- `rule_meet`
- `rule_meet_after`
- `req_meet`
- `req_meet_after`
- `size_step`
- `size_replay_mono`
- `no_return`
- `inst_loss`
- `inst_gain`
- `rule_loss`
- `rule_gain`
- `req_loss`
- `req_gain`
- `kinds_move_both_ways`

Predicted CONTENT:

- `inst_fixed_of_survives`
- `inst_survives_of_fixed`
- `inst_descends_of_fixed`
- `rule_descends_of_fixed`
- `req_fixed_of_survives`
- `req_survives_of_fixed`
- `req_descends_of_fixed`
- `datum_lift`
- `form_lift`
- `size_counts_changes`

The names above are the ones this rung commits to before Lean has run.  A
name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census and
is recorded in `STATUS.md` as unpredicted work.

## Stage one -- which automorphisms survive one event (Lean)

- **K-1** (NOT FORCED).  For each of the three adding kinds -- an
  instance, a uniform rule, a requirement -- and every regime, with the
  added element well-formed and not already admitted: a pair of maps that
  is an automorphism before the event and an automorphism after it FIXES
  the added element (`*_fixed_of_survives`); an automorphism before that
  fixes it is, with the same maps, an automorphism after
  (`*_survives_of_fixed`); and, for a well-formed regime before, an
  automorphism after that fixes it is, with the same maps, an
  automorphism before (`*_descends_of_fixed`).  So the pairs common to
  both sides are exactly the fixers before and exactly the fixers after
  (`*_meet`, `*_meet_after`).  PROVED, with no decidability hypothesis.
  Falsifier: any of the fifteen OPEN, or needing a hypothesis beyond
  well-formedness and newness of the element.
- **K-2** (NOT FORCED).  `datum_lift` and `form_lift` are PROVED: every
  automorphism of a well-formed regime extends, fixing the new index, to
  an automorphism of the regime after admitting a datum, and after
  admitting a form.  No automorphism is lost at either kind.
  Falsifier: either OPEN, or needing more than well-formedness.
- **K-3** (FORCED).  `supply_keeps`: a supply leaves the regime and so
  every automorphism in place, at the level of a definition.
  Falsifier: it needing more than unfolding the step.
- **K-4** (NOT FORCED).  At each of the three adding kinds there is a
  LOSS -- an automorphism before that is not one after -- and a GAIN --
  an automorphism after whose maps are not an automorphism before --
  each exhibited in Lean on a concrete regime and closed through the
  fixing theorems of K-1, never by counting.  The witnesses use at most
  three data and at most two forms, all of arity one.
  Falsifier: any of the six missing, or a witness exceeding those
  bounds.
- **K-5** (NOT FORCED).  No theorem of this rung counts an automorphism
  set.  Every statement about the SIZE of such a set is a finite
  computation on the rectangle.
  Falsifier: the committed Lean proving a size, or the ledger claiming
  one from Lean.

## Stage two -- a quantity that only grows (Lean)

- **K-6** (FORCED).  With the element count of a regime defined as its
  data plus its forms plus its instances, rules and requirements, each
  counted as listed, `size_step` is PROVED: every event either leaves the
  regime unchanged or raises the count by exactly one.  `size_replay_mono`
  and `no_return` follow: along any replayed history the count never
  falls, and no history returns to a regime it left by a changing event.
  Falsifier: an event raising the count by more than one, or either
  corollary needing more than an induction.
- **K-7** (NOT FORCED).  `size_counts_changes` is PROVED: the count of
  the regime a history reaches from a base equals the base's count plus
  the number of events of the history that change the regime.
  Falsifier: OPEN, or a hypothesis beyond the history replaying.
- **K-8** (NOT FORCED).  That two regimes the isomorphism relates have
  one and the same element count is NOT proved in Lean by this rung, so
  irreversibility up to the isomorphism beyond the rectangle is recorded
  OPEN and named as a leftover.
  Falsifier: the committed Lean proving it, or the ledger claiming it.
- **K-9** (FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.
  Falsifier: the committed axiom log naming any other axiom.

## Stage three -- the finite cross-check

The bases, the bound and the alphabet are rung three's and are not chosen
after seeing a count.

- **Declared rectangle.**  Rung three's, consumed through rung four's
  public population: three bases (EMPTY, L, F), every sequence of at most
  four declared events.  An EDGE is a sequence other than the empty one,
  read as its last event applied to the regime of its prefix; every event
  of every sequence is the last event of exactly one edge.
- **K-10** (FORCED).  577, 3928 and 14293 sequences, so 576, 3927 and
  14292 edges, 18795 in all; zero replay mismatches; at every regime
  reached the sealed automorphism count equals the brute-force count.
  Falsifier: any other value.
- **K-11** (NOT FORCED).  By kind: every supply edge and every edge that
  changes nothing leaves the size of the automorphism set equal; the
  admission of a datum and of a form never lowers it; and each of the
  three adding kinds raises it on at least one changing edge and lowers
  it on at least one.
  Falsifier: a supply or unchanging edge moving the size; a datum or form
  edge lowering it; an adding kind moving it in one direction only.
- **K-12** (NOT FORCED).  On every changing datum edge the size after
  equals the size before times one more than the count of untouched data
  before; on every form edge, times one more than the count of untouched
  forms of the new form's arity.  Zero violations.
  Falsifier: any violation.
- **K-13** (NOT FORCED).  On every changing edge of the three adding
  kinds, the pairs automorphisms both before and after, computed as the
  common members of the two sealed automorphism lists, are exactly the
  fixers of the added element before and exactly its fixers after; and
  the size before divided by the count of images of the element before
  equals the size after divided by the count of its images after.  Zero
  violations.
  Falsifier: any violation.
- **K-14** (NOT FORCED).  The largest ratio by which one edge RAISES the
  size is five, and every edge attaining it admits a datum.  The largest
  ratio by which one edge LOWERS it is twenty, and every edge attaining it
  admits an instance.
  Falsifier: any other maximum, or an edge of another kind attaining
  either.
- **K-15** (NOT FORCED).  Every sequence, the empty one included, is
  classed by the sizes along its prefixes as CONSTANT, RISING (never
  lower, not constant), FALLING (never higher, not constant) or MIXED.
  At L and at F all four classes are non-empty.  At EMPTY the FALLING
  class is empty, because the empty regime has one automorphism and no
  size is below one.  The shortest MIXED sequence has two events.
  Falsifier: an empty class at L or F; a FALLING sequence at EMPTY; a
  shortest MIXED sequence of any other length.
- **K-16** (FORCED).  On every changing edge the element count rises by
  exactly one and on every other edge it stays: zero violations.  No
  sequence reaches, after a changing event, a regime in the class of a
  regime an earlier prefix reached: zero revisits.
  Falsifier: any violation or revisit.
- **K-17** (FORCED).  The largest automorphism set over the rectangle has
  two hundred and forty members, and the smallest one.
  Falsifier: any other value.

## Stage four -- the census rows and the input count

- **K-18** (NOT FORCED).  The census rows this rung decides, and how:
  SYMMETRY along a history -- the size is definable at every regime and
  is neither preserved nor monotone along histories (countermodel, Lean
  and computation); INVARIANT -- the element count never falls and rises
  by exactly one at each changing event (PROVED for every history of the
  sealed step), and the count of fixers of the added element is kept by
  each adding event (the set identity PROVED; the numeric equality a
  finite computation); IRREVERSIBILITY -- no return to a regime PROVED,
  no return to a class a finite computation on the rectangle and OPEN
  beyond it.  Whether any of these is FORCED in the seed's sense is
  conditional on an engine whose accepted rounds are sealed events, and
  no such engine exists yet; the rows say so.
  Falsifier: the ledger recording any row without that condition.
- **K-19** (FORCED).  This rung neither reduces the count of declared
  inputs nor proves it at a floor; the value stays two.
  Falsifier: any claim otherwise.
- **K-20** (FORCED).  The receipt regenerates byte-identically, every
  node replays from its base, and the grouped gate time stays under
  fifteen minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.
