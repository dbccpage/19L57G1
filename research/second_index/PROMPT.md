# PROMPT: rung three -- the first-demand index over an arbitrary run

`AuthorityEffect: None`.  This file is the rung's question.  It states no
expected value and names no expected terminal; every number in it is
spelled out.  It is frozen by hash before anything else in this rung is
written, and before any Lean is built.

## Where the question comes from

The previous rung's first track proved, over its own reconstruction of the
sealed grammar extended by a declared two-sided stake, that three of the
six event kinds leave every demand of every stake unchanged, and that a
run built only from those three kinds reaches, from a well-formed base,
only regimes carrying exactly the demands the base carried.  It named, as
a leftover priced and executed nowhere, the index over histories that
would locate the first demand of a run not so restricted.  The other
three kinds do change demand sets, and that rung exhibited the change
only by computation.

The seed's rule for choosing a rung takes the smallest named leftover
that either reduces the count of declared inputs or extends the census of
the seed's challenge five, and on a tie the one named first.  The
parallel track of the same rung recorded the count of declared inputs at
two with no reduction proved, so its leftovers do not rank ahead.  This
leftover is the one the rule selects: it extends the census at the row
for succession.

## The question

Fix a base regime and a history: a list of events of the sealed grammar
reconstructed here, of any of the six kinds the rung-zero census
recorded, in any order.  Each prefix of the history reaches at most one
regime, and a prefix carrying an admission the grammar refuses reaches
none.  Count the events a prefix consumes from the front, so that the
count zero names the base itself.  Ask, of a declared two-sided stake:

- *One.*  Does the phrase "the first count at which a demand stands"
  name at most one number, given the base, the history and the stake?  If
  it names at most one, by what argument; if it can name two, by what
  witness?
- *Two.*  When the first such count is a successor, what must hold of the
  event that the prefix consumes last?  The previous rung's three
  demand-inert kinds are available to the argument; can the last event
  before a first demand be one of them?
- *Three.*  Is the count bounded below by something the grammar itself
  imposes rather than the declared bound -- for instance by how many data
  the history must admit before a pair of held data exists at all?
- *Four.*  Is the count a function of the regime a prefix reaches, or
  only of the history that reaches it?  Take two histories from one base
  that reach one and the same regime: must the two counts agree?
- *Five.*  Once a demand stands at a prefix, does it stand at every
  longer prefix of the same history?  If it can cease, is a regime
  carrying no demand reached after one carrying a demand, and by which
  event kind?
- *Six.*  Under the stake that labels every pair free, and from a base
  carrying no demand along a run built only from the demand-inert kinds,
  is there such a count at all?

No answer to any of the six is stated here and none is expected.  Each is
closed by a proof, by an executable countermodel, or by an explicit OPEN
status.

The word "free" appears above, and appears throughout this rung, only as
the name of one of the three values a stake assigns to a pair.  It is
never the guarded adjective, which this rung writes nowhere.

## The decision problem the question raises, named before it is met

Whether a demand stands at a regime is, in the sealed grammar, a
statement over contexts.  A least count is extracted from a family of
statements only when each statement of the family can be decided, or when
the argument is arranged to need no such extraction.  Which of the two
this rung does, and at what price, is part of the question and is
recorded with the answer.

## What is reconstructed and what is native

The sealed kernel's regime, contexts, derivability, collapse,
separability, event kinds, step and replay are reconstructed verbatim
from the sealed sources, with a pin note for each group, as the sibling
trees do.  The two-sided stake, honour, and the demand predicate over the
sealed regime are reconstructed verbatim from the previous rung's first
track, with a pin note for each, together with the slice of its inertia
theorems this rung's arguments consume.  Nothing sealed and no sibling
package is imported by the Lean of this rung, and no sibling source is
copied into the Python of this rung: the sibling computation is consumed
read-only through its public functions, pinned by blob.

This rung's own objects are the prefix reading of a history, the property
of carrying a demand, the property of being a first count, and whatever
the six questions above require beyond them.

## The finite cross-check

From three declared bases -- the empty regime, and the two sealed genesis
readings the sealed engine declares -- enumerate without pruning every
sequence of declared events up to a declared length over a declared
finite alphabet, under declared bounds on the count of data and the count
of judgment forms.  At every sequence and for every declared stake,
compute the first count at which a demand stands, and compute it a second
time by an independently written procedure, and record disagreement as a
failure rather than as a number.  Record the distribution of the counts,
the kind of the event each count consumes last, the sequences from one
base that reach one regime with counts that differ, and the sequences at
which a demand stands at one prefix and does not stand at a longer one.
Every bound, every alphabet and every count is declared in
`PREDICTIONS.md` before the first computation and recorded in the receipt
afterwards.

## Discipline

Every substantive line carries exactly one evidence class.  A target true
by unfolding a definition is recorded as being at the level of a
definition, in those words, and is never counted as content.  No theorem
is stated without its grammar in the same sentence.  Predictions are
frozen before the first computation and before the first compile, scored
mechanically, and never edited.  A receipt is not a proof.  A pin proves
only that a source did not move.  A gate is proved by failing on the
defect it exists to catch, with the failure naming the injected object,
and by recovering when the injection is reversed.  Nothing of the sealed
estate's standing obstructions is treated here as anything other than
standing.
