# PROMPT: rung six -- succession through the element count

`AuthorityEffect: None`.  This file is the rung's question.  It states no
expected value and names no expected terminal; every number in it is
spelled out.  It is frozen by hash before anything else in this rung is
written, and before any Lean is built.

## Where the question comes from

Rung five proved, for every history of the sealed step, that the element
count of the regime a history reaches from a base is the base's count
plus the number of the history's events that change the regime.  It
named, as leftover Z-4, priced small and executed nowhere, succession
through the element count: whether that reading of the number of
changing rounds off a regime and its base decides the census row for
succession of accepted rounds -- which rounds are accepted, and whether
the base must be named.

The seed's rule for choosing a rung takes the smallest named leftover
that either reduces the count of declared inputs or extends the census of
the seed's challenge five, and on a tie the one named first.  Rung five's
own application of that rule, recorded at the end of its `STATUS.md`,
selects Z-4: it extends the census row for succession, it is the only
eligible leftover priced small, and no leftover reduces the count of
declared inputs.

Two readings of the row already stand and are not revised here: rung
three's, succession as the index of the first demand along a history,
decided NOT DEFINABLE from the regime; and rung four's, the same index
taken up to the implemented isomorphism.  Neither counts rounds of any
kind.  This rung adds readings; it withdraws none.

## The objects

A HISTORY is a finite sequence of events of the six sealed kinds,
replayed from a BASE regime by the sealed step.  A history REACHES the
regime its replay returns.

A READING of an accepted round is a rule that marks some events of a
history as accepted.  Three readings are declared, and no other is
examined here:

- EVERY: every event of the history is accepted;
- ADMITTING: every event other than a supply is accepted, whether or not
  it changes the regime;
- CHANGING: exactly the events after which the regime differs from the
  regime before are accepted.

The COUNT of a history under a reading is the number of its accepted
events.

The ELEMENT COUNT of a regime is its number of data plus its number of
forms plus its numbers of instances, uniform rules and requirements, each
counted as listed, as rung five defined it.

A count is a FUNCTION OF THE BASE AND THE REGIME under a reading when any
two histories from one base reaching one regime carry the same count.  It
is a FUNCTION OF THE REGIME ALONE when any two histories, from any bases,
reaching one regime carry the same count.

## The question

- *One.*  Under each of the three readings, is the count a function of
  the base and the regime?  Where it is, by what expression; where it is
  not, by what shortest exhibited pair of histories?
- *Two.*  Under each reading, is the count a function of the regime
  alone, or must the base be named?  Is there a base from which no naming
  is needed?
- *Three.*  How do the three counts of one history compare with one
  another, for every history?
- *Four.*  Over the frozen rectangle, for each reading and each base: how
  many regimes are reached with more than one count, and what is the
  shortest sequence whose count differs from that of an earlier sequence
  reaching the same regime?
- *Five.*  Over the frozen rectangle, taken up to the implemented
  isomorphism: within one base, is any class reached with two counts
  under the reading that is a function of base and regime, if there is
  one?  Across bases, for the classes reached from more than one base, do
  the counts agree, and do they agree when every base is itself counted
  from the sealed empty regime by its sealed genesis history?
- *Six.*  Which of the above is proved for every history of the sealed
  step, which is a finite computation on the rectangle, and which stays
  open beyond it?

No answer to any of the six is stated here and none is expected.  Each is
closed by a proof, by an executable countermodel, or by an explicit OPEN
status.

## What is reconstructed and what is native

The sealed kernel's regime, well-formedness, event kinds, step, replay
and genesis are reconstructed verbatim from the sealed sources, as rungs
three, four and five did, with a pin note and a declaration-by-declaration
comparison with the pinned sources.  Nothing sealed and no sibling
package is imported by the Lean of this rung.  Where a statement of this
rung repeats a statement rung five proved, it is proved again inside this
package so that the package stays self-contained, and the ledger says the
statement is rung five's.  No sibling source is copied into the Python of
this rung: the sealed kernel, the sealed genesis readings, the sealed
isomorphism procedure and the rectangle of rungs three and four are
consumed read-only through their public functions, pinned by blob.

This rung's own objects are the three readings, their counts, the
comparison of counts across histories and across bases, and whatever the
six questions above require beyond them.

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
the same sentence.  A count taken up to the isomorphism is a finite
computation unless a theorem of this rung carries it across an
isomorphism.  A reading of an accepted round by an engine is not one of
the three readings above, and no statement here is about an engine.
Predictions are frozen before the first computation and before the first
compile, scored mechanically, and never edited.  A receipt is not a
proof.  A pin proves only that a source did not move.  A gate is proved
by failing on the defect it exists to catch, with the failure naming the
injected object, and by recovering when the injection is reversed.
Nothing of the sealed estate's standing obstructions is treated here as
anything other than standing.
