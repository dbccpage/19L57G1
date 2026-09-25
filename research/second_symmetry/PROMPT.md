# PROMPT: rung five -- the automorphisms of a regime along a history

`AuthorityEffect: None`.  This file is the rung's question.  It states no
expected value and names no expected terminal; every number in it is
spelled out.  It is frozen by hash before anything else in this rung is
written, and before any Lean is built.

## Where the question comes from

Rung four decided the census row for symmetry as definable at every
regime its rectangle reaches: the size of the automorphism set of a
regime is a function of the regime alone, computed by the sealed
procedure and checked against a brute-force count over every bijection
pair.  It named, as leftover Y-3, priced small and executed nowhere,
symmetry along a history: whether that size is preserved or monotone
along the events of a history, and at which event kinds it moves.

The seed's rule for choosing a rung takes the smallest named leftover
that either reduces the count of declared inputs or extends the census of
the seed's challenge five, and on a tie the one named first.  Rung four's
own application of that rule, recorded at the end of its `STATUS.md`,
selects Y-3: it extends the census rows for symmetry, for invariants and
for irreversibility, and no leftover reduces the count of declared
inputs.

## The objects

An AUTOMORPHISM of a regime is a sealed isomorphism from the regime to
itself: a pair of bijections, one on datum indices and one on form
indices, preserving arities and carrying the admitted instances, rules
and requirements onto themselves.  Presentation tokens are not part of
it.

An event of a history is one of the six sealed kinds: a supply, the
admission of a datum, of a form, of an instance, of a uniform rule, and
the imposition of a requirement.  An event CHANGES the regime when the
regime after it differs from the regime before it.

For an event that adds one element to a regime -- an instance, a rule or
a requirement not already admitted -- the IMAGES of the element under a
set of bijection pairs are the elements those pairs carry it to, and the
pairs that FIX it are those carrying it to itself.

A datum is UNTOUCHED in a regime when no admitted instance and no
admitted requirement names it.  A form is UNTOUCHED when no admitted
instance uses it and no admitted rule names it.

## The question

- *One.*  Along a single event of each of the six kinds, which
  automorphisms of the regime before are automorphisms of the regime
  after, which of the regime after are automorphisms of the regime
  before, and is either set fixed by a law stated in terms of the event
  alone?
- *Two.*  For the event kinds that add one element, is the set of
  pairs that are automorphisms both before and after the event exactly
  the set of automorphisms before that fix the element, and exactly the
  set of automorphisms after that fix it?  Is this proved for every
  regime, or only computed?
- *Three.*  For the admission of a datum and of a form, does every
  automorphism before extend to one after, and does the size of the set
  after follow from the size before and the count of untouched data or
  of untouched forms of the same arity?
- *Four.*  Over the frozen rectangle, at every event of every sequence,
  does the size of the automorphism set go up, stay, or go down, by event
  kind, counting changing events and events that change nothing apart?
  Which kinds move it in both directions?
- *Five.*  Along every sequence of the rectangle, is the size of the
  automorphism set constant, never decreasing, never increasing, or
  none of these?  How many sequences of each base fall in each class,
  and what is the shortest sequence of the last class?
- *Six.*  Is there a quantity read off a regime and its event that is
  preserved across every changing event of the three adding kinds?  Is
  there one read off the regime alone that never decreases along any
  sequence, and is it moved by every changing event?
- *Seven.*  Does any sequence of the rectangle reach, after a changing
  event, a regime the implemented isomorphism relates to a regime an
  earlier prefix of the same sequence reached?  Is the answer proved
  beyond the rectangle?

No answer to any of the seven is stated here and none is expected.  Each
is closed by a proof, by an executable countermodel, or by an explicit
OPEN status.

## What is reconstructed and what is native

The sealed kernel's regime, well-formedness, event kinds, step and replay
are reconstructed verbatim from the sealed sources, as rungs three and
four did.  The sealed isomorphism structure and its requirement ordering
are reconstructed verbatim from the sealed module that states them.  Each
reconstruction carries a pin note and is compared declaration by
declaration with its pinned source.  Nothing sealed and no sibling
package is imported by the Lean of this rung, and no sibling source is
copied into the Python of this rung: the sealed kernel, the sealed
isomorphism procedure and the rectangles and counts of rungs three and
four are consumed read-only through their public functions, pinned by
blob.

This rung's own objects are automorphisms, the survival of an
automorphism across an event, images and fixing, untouched data and
forms, the direction of each event, and whatever the seven questions
above require beyond them.

## The finite cross-check

The rectangle is rung three's, unchanged: the same three bases, the same
declared alphabet, every sequence of at most four declared events, run
without pruning.  Every automorphism set is computed by the sealed
procedure, and its size is checked against a brute-force count over every
bijection pair.  Every node is replayed from its base.  Every bound and
every count is declared in `PREDICTIONS.md` before the first computation
and recorded in the receipt afterwards.

## Discipline

Every substantive line carries exactly one evidence class.  A target true
by unfolding a definition is recorded as being at the level of a
definition, in those words, and is never counted as content.  No theorem
is stated without its grammar in the same sentence.  A size of an
automorphism set is a finite computation unless a theorem of this rung
counts it; a Lean statement about which pairs survive an event is not a
statement about how many do.  Predictions are frozen before the first
computation and before the first compile, scored mechanically, and never
edited.  A receipt is not a proof.  A pin proves only that a source did
not move.  A gate is proved by failing on the defect it exists to catch,
with the failure naming the injected object, and by recovering when the
injection is reversed.  Nothing of the sealed estate's standing
obstructions is treated here as anything other than standing.
