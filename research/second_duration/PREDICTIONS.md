# PREDICTIONS: rung seven -- duration under the CHANGING reading

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_duration.py` for the computational rows and by `test_census.py` for
the census rows.  A missed prediction is recorded next to its value and
never edited.  A miss is a finding, not a defect.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this rung, so a hit evidences the ordering of the
work and not insight.  NOT FORCED means the run could have come out the
other way.  An argument written by this rung's own session before the
run is not a receipt: a row that leans on one is NOT FORCED.

Receipts and sources read before freezing, because a prediction below
leans on them: rung four's `receipts/iso_index.json` through rung six's
`receipts/succession.json` (577, 3928 and 14293 sequences; 75, 523 and
1718 distinct regimes at EMPTY, L and F; zero classes reached with two
CHANGING counts within a base); the declared alphabet of the rectangle in
`research/second_nofirst/nofirst.py` (one supply token; five fresh datum
tokens, taken in order, so every datum admission of the rectangle is a
growth; arities one and two; at most five data, two forms and four
events); rung six's `lean/SecondSuccession/Count.lean`; and the sealed
Python genesis readings, whose regimes carry two data (L) and three data
(F) and no form, instance, rule or requirement.

## Declared before the compile: the FW-DEF census this rung commits to

Four classes, as the sibling rungs use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this rung's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion); THIN (one
genuine step, or a direct corollary of a neighbour); CONTENT (everything
else).

Predicted DEFINITION:

- `replayE_cons`
- `lead_splits`
- `gap_splits`

Predicted THIN:

- `insertNew_grows`
- `step_parts`
- `growths_counted`
- `growths_given_base`
- `rest_given_base`
- `after_le_rest`
- `naming_step`
- `segment_not_given_base`
- `gap_not_from_genesis`
- `tail_forced`
- `pinned_by_requirement`

Predicted CONTENT:

- `rest_counted`
- `naming_bounded`

The names above are the ones this rung commits to before Lean has run.  A
name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census and
is recorded in `STATUS.md` as unpredicted work.  Two of them repeat, as
statements, lemmas rung six proved (`replayE_cons` and `insertNew_grows`,
its lemmas of the same names); they are proved again here so that the
package imports nothing, and the ledger credits the statements to rung
six.

The Lean objects, declared here so the rows below can name them: `size`,
rung five's element count; `growths b h`, the growths of a history from
a base; `rest b h`, its rest rounds; `during n b h`, its rest rounds
taken while the regime has exactly `n` data, so that segment `i` from a
base with `k` data is `during (k + i)`; `after t b h`, its rest rounds
taken while the regime has more than `t` data; and `naming t r`, the
number of instances and requirements of a regime that name a datum index
at or above `t`.  An ill-formed event ends each count, as it ends replay.

## Stage one -- the duration vector in Lean

- **N-1** (NOT FORCED).  `growths_counted` and `rest_counted` are PROVED
  for every base and every history that replays: the regime reached has
  the base's data plus the growths, and its element count is the base's
  plus the growths plus the rest rounds.  `growths_given_base` and
  `rest_given_base` follow: a function of base and regime gives the
  number of segments less one and the sum of the vector.  No
  decidability hypothesis, no well-formedness hypothesis, and no
  hypothesis beyond the replay.
  Falsifier: any of the four OPEN, or needing a further hypothesis.
- **N-2** (FORCED).  The vector is NOT a function of base and regime.
  `lead_splits`: from the sealed empty regime, a form of arity one then
  a datum, and a datum then the form, reach one regime with segment zero
  one and zero.  `segment_not_given_base` refutes every function of a
  position, a base and a regime giving `during`.  Both by kernel
  computation and a corollary.
  Falsifier: the countermodel failing to compute.
- **N-3** (NOT FORCED).  A duration between two growths is NOT a
  function of the regime even from the sealed empty regime.
  `gap_splits`: a datum, a form of arity one, a datum; and a datum, a
  datum, the form; both from the empty regime, reach one regime, with
  `during 1` one and zero.  `gap_not_from_genesis` refutes every
  function of the regime alone giving `during 1` over histories from the
  empty regime.
  Falsifier: the countermodel failing to compute, or no two histories of
  three events from the empty regime splitting `during 1`.
- **N-4** (NOT FORCED).  `naming_bounded` is PROVED for every base, every
  history that replays and every `t`: `naming t` of the regime reached is
  at most `naming t` of the base plus `after t`.  No well-formedness
  hypothesis on the base.  `after_le_rest` holds for every history,
  replayed or not.
  Falsifier: either OPEN, or `naming_bounded` needing the base to be
  well formed.
- **N-5** (NOT FORCED).  `tail_forced`: when the base names nothing at or
  above `t` and the regime reached has as many instances and
  requirements naming `t` or later as the history has rest rounds, every
  rest round is taken after the regime has more than `t` data.
  `pinned_by_requirement`: every history from the sealed empty regime
  reaching the regime with two data and the one requirement between them
  takes exactly one rest round, and takes it after the second growth.
  Falsifier: either OPEN.
- **N-6** (NOT FORCED).  No theorem statement of this package mentions
  the sealed isomorphism, and none states that every tuple of the
  envelope is the vector of some history: both stay OPEN beyond the
  rectangle.
  Falsifier: the committed Lean proving either, or the ledger claiming
  either.
- **N-7** (FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.
  Falsifier: the committed axiom log naming any other axiom.

## Stage two -- the finite cross-check

The bases, the bound and the alphabet are rung three's and are not
chosen after seeing a count.

- **Declared rectangle.**  Rung three's, consumed through rung four's
  public population: three bases (EMPTY, L, F), every sequence of at most
  four declared events.  A regime is VECTOR-SPLIT at a base when two
  sequences of that base reaching it carry different duration vectors,
  and GAP-SPLIT when they carry different tuples of durations between
  growths (segments one to the number of growths less one).  The
  SHORTEST SPLITTING SEQUENCE for either is the least sequence, in order
  of length and then descriptor, whose value differs from that of a
  sequence of that base of no greater length reaching the same regime.
- **N-8** (FORCED).  577, 3928 and 14293 sequences; 75, 523 and 1718
  distinct regimes; zero replay mismatches.
  Falsifier: any other value.
- **N-9** (NOT FORCED).  On every sequence of every base, the vector has
  one entry more than the regime reached has new data, and its sum is
  the number of new elements other than data.  Zero violations of each.
  Falsifier: any violation.
- **N-10** (NOT FORCED).  At every base: every vector reached lies in the
  envelope of its base and regime (zero violations); for every regime
  reached, the set of vectors reached is exactly its envelope (zero
  regimes where they differ); so a regime is reached with exactly one
  vector exactly when its envelope has one tuple.
  Falsifier: a vector outside its envelope, or a regime at which some
  tuple of the envelope is not reached.
- **N-11** (NOT FORCED).  At every base at least one regime is
  vector-split and at least one is gap-split; no base has more gap-split
  than vector-split regimes; the shortest vector-splitting sequence has
  two events and the shortest gap-splitting sequence has three, at every
  base.
  Falsifier: an unsplit base under either, more gap-split than
  vector-split regimes at a base, or any other length.
- **N-12** (NOT FORCED).  At every base at least one regime with at least
  one growth and at least one rest round has an envelope of one tuple,
  whose rest rounds all lie in the tail.
  Falsifier: none at some base.
- **N-13** (NOT FORCED).  Taken up to the implemented isomorphism, within
  each base: at least one class is reached with two vectors; no class is
  reached with two vector sums; and at least one class carries two
  regimes with different envelopes.
  Falsifier: no class with two vectors at a base; a class with two sums;
  no class with two envelopes at a base.
- **N-14** (FORCED).  The three Lean countermodels of N-2, N-3 and N-5,
  replayed in the sealed Python grammar, reach one regime on both sides
  and give the claimed values.
  Falsifier: any side reaching another regime, or another value.

## Stage three -- the census row and the input count

- **N-15** (NOT FORCED).  The ledger decides one row of the
  challenge-five census, duration, under the CHANGING reading: the
  durations between growths NOT DEFINABLE from base and regime, nor from
  the regime from the empty base (COUNTERMODEL); the number of segments
  and the sum of the vector DEFINABLE from base and regime (PROVED); the
  lower bounds of N-4 DEFINABLE (PROVED); the vector fixed when every new
  element other than a datum names the newest datum (PROVED); that the
  vectors reached are exactly the envelope a finite computation on the
  rectangle and OPEN beyond it; up to the isomorphism a finite
  computation and OPEN beyond.  FORCED in the seed's sense is
  conditional on an engine whose rounds are the changing events of the
  sealed step, and no such engine exists yet; the row says so.
  Falsifier: the ledger recording the row without that condition, or
  recording a durations-between-growths reading as definable.
- **N-16** (FORCED).  This rung neither reduces the count of declared
  inputs nor proves it at a floor; the value stays two.
  Falsifier: any claim otherwise.
- **N-17** (FORCED).  The receipt regenerates byte-identically, every
  node replays from its base, and the grouped gate time stays under
  fifteen minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.
