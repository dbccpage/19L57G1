# PROMPT: rung seven -- duration under the CHANGING reading

`AuthorityEffect: None`.  This file is the rung's question.  It states no
expected value and names no expected terminal; every number in it is
spelled out.  It is frozen by hash before anything else in this rung is
written, and before any Lean is built.

## Where the question comes from

Rung six proved, for every history of the sealed step, that the number
of events after which the regime differs -- the CHANGING count -- is the
element count of the regime reached less that of the base.  It named, as
leftover W-1, priced small and executed nowhere, duration under the
CHANGING reading: the seed's census row for duration reads it as rounds
between growths, and whether the regime a history reaches carries the
number of changing rounds between two growths -- or only bounds on it,
through which data the admitted instances and requirements name -- was
not decided.

The seed's rule for choosing a rung takes the smallest named leftover
that either reduces the count of declared inputs or extends the census of
the seed's challenge five, and on a tie the one named first.  Rung six's
own application of that rule, recorded at the end of its `STATUS.md`,
selects W-1: it extends the census row for duration, it is the only
eligible leftover priced small, and no leftover reduces the count of
declared inputs.

No earlier rung decided the duration row.  This rung adds a reading of
it; it withdraws nothing.

## The objects

A HISTORY is a finite sequence of events of the six sealed kinds,
replayed from a BASE regime by the sealed step.  A history REACHES the
regime its replay returns.

A ROUND is an event of a history after which the regime differs from the
regime before: rung six's CHANGING reading, and no other reading is
examined here.  A GROWTH is a round after which the regime has more data
than before.  A REST ROUND is a round that is not a growth.

The SEGMENTS of a history are numbered from zero to its number of
growths: segment `i` is the number of rest rounds taken after exactly `i`
growths of that history and before the next.  The DURATION VECTOR of a
history is the tuple of its segments, in order.  The DURATION between
growth `i` and growth `i` plus one, for `i` from one to the number of
growths less one, is segment `i`; segment zero is the LEAD, before the
first growth, and the last segment is the TAIL, after the last growth.

For a base and a regime reached from it, an element of the regime is NEW
when the base does not carry it.  The LEVEL of a new element other than a
datum is zero for a form and for a uniform rule; for an instance or a
requirement it is the largest datum index it names, less the base's
number of data, plus one, and zero when that is negative.  The level is
the number of growths a history must have taken before it can admit that
element.

The ENVELOPE of a base and a regime is the set of tuples of natural
numbers, one entry for each segment position from zero to the number of
new data, whose entries sum to the number of new elements other than
data, and in which, for every position `i`, the sum of the entries from
`i` on is at least the number of new elements of level at least `i`.

A quantity of a history is a FUNCTION OF THE BASE AND THE REGIME when any
two histories from one base reaching one regime carry the same value.  It
is a FUNCTION OF THE REGIME FROM THE EMPTY BASE when that holds for
histories from the sealed empty regime.

## The question

- *One.*  Is the duration vector a function of the base and the regime?
  Is each duration between two growths?  Does the answer change when the
  base is the sealed empty regime?  Where the answer is no, by what
  shortest exhibited pair of histories?
- *Two.*  Which quantities of the vector are functions of the base and
  the regime: its number of entries, its sum?  By what expression, proved
  for every history of the sealed step?
- *Three.*  Is every history's number of rest rounds taken after a given
  datum exists at least the number of instances and requirements of the
  regime reached that name that datum or a later one, less those the base
  already carries?  And when every new element other than a datum names
  the newest datum, is the whole vector fixed?
- *Four.*  Over the frozen rectangle, for each base: how many regimes are
  reached with more than one duration vector, and with more than one
  value of some duration between two growths; what is the shortest
  sequence whose vector differs from that of a sequence of no greater
  length reaching the same regime; is every vector reached inside the
  envelope; is every tuple of the envelope reached; and is a regime
  reached with exactly one vector exactly when its envelope has one
  tuple?
- *Five.*  Over the frozen rectangle, taken up to the implemented
  isomorphism: within one base, how many classes are reached with two
  duration vectors, how many with two vector sums, and how many carry
  regimes with different envelopes?
- *Six.*  Which of the above is proved for every history of the sealed
  step, which is a finite computation on the rectangle, and which stays
  open beyond it?

No answer to any of the six is stated here and none is expected.  Each is
closed by a proof, by an executable countermodel, or by an explicit OPEN
status.

## What is reconstructed and what is native

The sealed kernel's regime, well-formedness, event kinds, step, replay
and genesis are reconstructed verbatim from the sealed sources, as rungs
three to six did, with a pin note and a declaration-by-declaration
comparison with the pinned sources.  Nothing sealed and no sibling
package is imported by the Lean of this rung.  Where a statement of this
rung repeats a statement an earlier rung proved, it is proved again
inside this package so that the package stays self-contained, and the
ledger says whose statement it is.  No sibling source is copied into the
Python of this rung: the sealed kernel, the sealed genesis readings, the
sealed isomorphism procedure and the rectangle of rungs three and four
are consumed read-only through their public functions, pinned by blob.

This rung's own objects are growths, rest rounds, segments, the duration
vector, levels, the envelope, and whatever the six questions above
require beyond them.

## The finite cross-check

The rectangle is rung three's, unchanged: the same three bases, the same
declared alphabet, every sequence of at most four declared events, run
without pruning, consumed through rung four's population.  Every node is
replayed from its base.  Every class is the implemented isomorphism's.
Every bound and every count is declared in `PREDICTIONS.md` before the
first computation and recorded in the receipt afterwards.

## Discipline

Every substantive line carries exactly one evidence class.  A target true
by unfolding a definition or by kernel computation on a concrete history
is recorded as being at the level of a definition, in those words, and is
never counted as content.  No theorem is stated without its grammar in
the same sentence.  A quantity taken up to the isomorphism is a finite
computation unless a theorem of this rung carries it across an
isomorphism.  A round of an engine is not a round as declared here, and
no statement here is about an engine.  Predictions are frozen before the
first computation and before the first compile, scored mechanically, and
never edited.  A receipt is not a proof.  A pin proves only that a source
did not move.  A gate is proved by failing on the defect it exists to
catch, with the failure naming the injected object, and by recovering
when the injection is reversed.  Nothing of the sealed estate's standing
obstructions is treated here as anything other than standing.
