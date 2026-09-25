# PROMPT: rung eight -- the element count across the isomorphism

`AuthorityEffect: None`.  This file is the rung's question.  It states no
expected value and names no expected terminal; every number in it is
spelled out.  It is frozen by hash before anything else in this rung is
written, and before any Lean is built.

## Where the question comes from

Rung five proved, for every history of the sealed step, that every event
keeps the regime or raises its element count by exactly one, and hence
that no history returns to a REGIME it left by a changing event.  It
named, as leftover Z-1, priced moderate and executed nowhere, the element
count across the isomorphism: whether two regimes the sealed isomorphism
relates have one element count.  It recorded the obstacle beside the
leftover: the Lean regime keeps its collections as lists, the sealed
well-formedness predicate does not forbid a repeated entry, and whether
every regime the sealed step reaches is free of repeated entries was not
proved.

Rungs six and seven left three statements open behind Z-1: the CHANGING
count up to the isomorphism, the sum of the duration vector up to the
isomorphism, and a return to a CLASS a history left.

The seed's rule for choosing a rung takes the smallest named leftover
that either reduces the count of declared inputs or extends the census of
the seed's challenge five, and on a tie the one named first.  Rung
seven's own application of that rule, recorded at the end of its
`STATUS.md`, selects Z-1: it extends the census rows for recurrence and
for irreversibility up to the isomorphism, it is the smaller of the two
eligible leftovers, and no leftover reduces the count of declared inputs.

No earlier rung decided the recurrence row.  This rung adds to the rows
it touches; it withdraws nothing.

## The objects

A HISTORY is a finite sequence of events of the six sealed kinds,
replayed from a BASE regime by the sealed step.  A history REACHES the
regime its replay returns.  A CHANGING event is one after which the
regime differs from the regime before, as rung six declared it.

The FIVE COMPONENT COUNTS of a regime are its number of data, the length
of its list of forms, and the lengths of its lists of instances, of
uniform rules and of requirements.  The ELEMENT COUNT is their sum, rung
five's.  A regime is DUPLICATE-FREE when none of its lists of instances,
of uniform rules and of requirements holds one entry twice.  A regime is
CLEAN when it is well formed in the sealed sense and duplicate-free.

Two regimes are ISOMORPHIC when the sealed isomorphism structure has an
inhabitant between them.  A CLASS, in the finite cross-check, is the set
of regimes the sealed key procedure gives one key.

A history RECURS when it reaches, after some non-empty prefix, a regime
isomorphic to the regime reached after an earlier prefix, the empty
prefix included.  The recurrence is a STUTTER when the two regimes are
equal, and a RETURN otherwise.

## The question

- *One.*  Does the sealed isomorphism keep each of the five component
  counts?  For which of them is no hypothesis on the two regimes needed,
  and for which are being well formed, being duplicate-free, or both,
  needed?  Where a hypothesis is needed, by what exhibited pair of
  regimes that meet every other hypothesis and differ in that count?
- *Two.*  Does every event of the sealed step keep a regime clean?  Is
  every regime reached by a history from the sealed empty regime, and
  from each of the two sealed reading regimes, clean?
- *Three.*  From a clean base, can a history return in the sense above?
  If a history reaches a regime isomorphic to one it reached earlier,
  which events lie between the two?
- *Four.*  From the sealed empty regime, are the CHANGING count, the
  number of growths and the number of rest rounds of a history functions
  of the class of the regime it reaches?  Within one clean base, are
  they?  Across two bases, does the answer change?
- *Five.*  Over the frozen rectangle, for each base: do the classes of
  the sealed key procedure carry one value of each of the five component
  counts; how many sequences recur, how many of those recurrences are
  stutters and how many returns, and by which event kinds is a stutter
  reached; and how many classes are reached at more than one base?
- *Six.*  Which of the above is proved for every history of the sealed
  step, which is a finite computation on the rectangle, and which stays
  open beyond it?

No answer to any of the six is stated here and none is expected.  Each is
closed by a proof, by an executable countermodel, or by an explicit OPEN
status.

## What is reconstructed and what is native

The sealed kernel's regime, well-formedness, event kinds, step, replay
and genesis, and the sealed isomorphism structure, are reconstructed
verbatim from the sealed sources, as rungs three to seven did, with a pin
note and a declaration-by-declaration comparison with the pinned sources.
Nothing sealed and no sibling package is imported by the Lean of this
rung.  Where a statement of this rung repeats a statement an earlier rung
proved, it is proved again inside this package so that the package stays
self-contained, and the ledger says whose statement it is.  No sibling
source is copied into the Python of this rung: the sealed kernel, the
sealed genesis readings, the sealed isomorphism procedure and the
rectangle of rungs three and four are consumed read-only through their
public functions, pinned by blob.

This rung's own objects are the five component counts, duplicate-freedom,
cleanness, recurrence, stutters and returns, and whatever the six
questions above require beyond them.

## The finite cross-check

The rectangle is rung three's, unchanged: the same three bases, the same
declared alphabet, every sequence of at most four declared events, run
without pruning, consumed through rung four's population.  Every node is
replayed from its base.  Every class is the sealed key procedure's, and
the key partition is compared again with the sealed brute-force minimum
over every bijection pair.  Every bound and every count is declared in
`PREDICTIONS.md` before the first computation and recorded in the receipt
afterwards.

## Discipline

Every substantive line carries exactly one evidence class.  A target true
by unfolding a definition or by kernel computation on concrete regimes is
recorded as being at the level of a definition, in those words, and is
never counted as content.  No theorem is stated without its grammar in
the same sentence.  The Python regime keeps its collections as sets, so
duplicate-freedom is a question about the Lean list presentation, and no
Python count is read as evidence about it.  A round of an engine is not
an event as declared here, and no statement here is about an engine.
Predictions are frozen before the first computation and before the first
compile, scored mechanically, and never edited.  A receipt is not a
proof.  A pin proves only that a source did not move.  A gate is proved
by failing on the defect it exists to catch, with the failure naming the
injected object, and by recovering when the injection is reversed.
Nothing of the sealed estate's standing obstructions is treated here as
anything other than standing.
