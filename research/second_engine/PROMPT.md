# PROMPT: continuation one -- the engine

`AuthorityEffect: None`.  This file is the question of the first
research attempt of the continuation the author authorized on
twenty-fifth September twenty twenty-six.  It states no expected value
and names no expected terminal; every number in it is spelled out.  It
is frozen by hash before anything else in this tree is written, and
before any Lean is built.

## Where the question comes from

Rung ten recorded that the seed's next-rung rule selects no leftover,
that the original rung budget is spent when counted by tree, and that
the leftover every FORCED column of the census waits on is rung three's
X-five, the engine of the seed's challenge three.  The author then ruled,
in words recorded verbatim in `research/second/MANUAL.md` and in
`CLAUDE.md`, that resolving an unresolved FORCED classification extends
the census, that a named prerequisite of an eligible census question is
eligible, that X-five is eligible on that basis, and that at most two
further research attempts are authorized: first challenge three, then
challenge four with its engine-dependent census evaluations.  This is the
first.  It closes before the second opens, it keeps its declared bounds,
and it may terminate OPEN.  The seed is unchanged; the continuation is a
protocol intervention by the author, and this tree is a result of that
intervention, not of the seed's rule.

The seed's challenge three reads: declare precisely what an engine is --
a generator that reads demands off the state, a responder that answers a
demand by a minimum response under a declared measure, a continuation
rule, and a replay rule, such that after genesis no external act occurs
except those the engine's declaration names; enumerate every minimal
engine in a declared class formed from the surviving stakes of challenge
two, the two continuation rules already known (growth; switch of demand
kind), and the validity rules of challenge one; count every capability
each engine declares; reject any engine called "one declaration" that
bundles several; retain all tied minima.  The seed's required questions
four and ten ask whether a minimal engine exists, whether it is unique up
to isomorphism, and whether it is initial in its declared class, with the
universal property proved or the claim refused.

Running every engine forward to its bounds and reading the census off
the runs is challenge four and the second attempt.  This attempt runs no
engine forward beyond the short probe declared below.

## The supplied pieces, consumed and never copied

- The sealed kernel: regimes, the six event kinds, step, replay, the two
  sealed genesis readings L and F, the sealed profiles, the sealed
  candidate space of augmentations with its unpruned enumeration at the
  sealed bounds (at most two items, arities at most two), the two sealed
  cost measures, and the sealed key procedure with its brute-force
  minimum.
- The stake rule class of rung two, track two: the six observables it
  names, O-one to O-six, and the nine rules it names, E-one to E-nine,
  with the observables each rule reads.  Its receipt lists all nine as
  survivors of challenge two.  Its five controls are not members of its
  rule class, and are not stakes of this class.
- The honour relation and the demand reading of the two-sided commitment
  tree: a labelled pair is honoured when its label is apart and the
  pair's sealed profiles differ, when its label is same and they are
  equal, or when its label is free.
- The validity rules of challenge one, as rung one declared them for an
  index commitment: member one, no regress, inherited; member two, member
  one and in addition every labelled pair involving a datum the response
  itself introduces is honoured after the response.  Rung two's dynamic
  form of member one, for a rule that reads the state, is consumed
  through its public function.
- The two continuation rules: growth, the supply and admission of one
  fresh opaque datum taken only at a demand-free state; and the switch of
  the demand kind declared by the identification tree, taken at a
  demand-free state.

## The objects

A STATE of an engine is a sealed regime together with a MODE, plain or
flipped.  The genesis state of a reading is the sealed genesis regime of
that reading in plain mode.

A STAKE RULE labels every pair of held data apart, same or free by
reading the regime.  Read in plain mode, the label is the rule's label;
read in flipped mode, apart and same are exchanged and free is kept.

A DEMAND of a state under a stake rule is a pair of held data whose
label, read in the state's mode, is not honoured.  The demand is read
off the state; no event emits it.

A RESPONSE to a demand, under a measure and a validity rule, is a
minimum, under that measure, of the deltas of the sealed candidate space
that the validity rule accepts: the least item count at which some
accepted delta exists, and under the second measure the least cost among
them; every tied minimum is kept.  Member one accepts a delta when the
demanded pair is honoured afterwards under its label and every pair
honoured before is honoured afterwards under its label before, labels
read in the state's mode.  Member two accepts a delta when member one
does and every pair involving a datum the delta introduces is honoured
afterwards under its label read afterwards in the state's mode.  A
response is admitted by the admission events of its delta.  A demand
with no accepted delta within the sealed bounds is REFUSED.

GROWTH, at a demand-free state whose data number fewer than four, emits
the supply and the admission of one fresh token.  SWITCH, at a
demand-free state, emits one marker event that flips the mode and
changes nothing else; no requirement is retracted, because an engine
imposes none.

An ENGINE is a declaration of four parts: a GENERATOR, which is one
stake rule of the class read at every state; a RESPONDER, which is one
sealed measure and one validity rule; a CONTINUATION, which is a set of
continuation rules, each fired at every demand-free state where it is
enabled, every fired rule a branch; and the REPLAY rule, the sealed
replay extended by the switch marker.  A state with a demand is answered
by a response to some demand, every demand and every tied minimum a
branch; a demand-free state with no enabled continuation is a FIXPOINT.
After genesis the only events of a run are those of a response, a growth
or a switch.  Whether a run holds any other event is checked on every
edge the probe builds.

The CLASS is every engine whose generator is one of the nine rules,
whose measure is one of the two, whose validity rule is one of the two
members, and whose continuation is one of the four subsets of the two
continuation rules.  The subset with neither rule is declared a member
here, and is named HALT; every question below is also answered on the
SEED-LITERAL SUBCLASS, whose continuation holds at least one rule.

A CAPABILITY is one named element of an engine's declaration, from this
list: three skeleton capabilities every engine declares (the demand
reading, the least-response selection over the sealed candidate space,
and the replay rule); each observable its stake rule reads, counted as
rung two counted it; its measure; each clause of its validity rule, one
for member one and two for member two; and each continuation rule in its
continuation.  The CAPABILITY COUNT of an engine is the size of its
capability set.  Growth is read as one capability.  A second declared
reading counts growth as two, a trigger and an admission, and every
minimum below is also computed under it.

A member of a subclass is COUNT-MINIMAL there when no member has a
smaller count, and INCLUSION-MINIMAL there when no member's capability
set is strictly inside its own.  A member is INITIAL in a subclass when
its capability set is inside every member's; the morphisms of this
reading are inclusions of declarations and nothing else.  An engine is
CALLED ONE DECLARATION when a label, a name or prose gives it the count
one; any such label is refused unless the engine's count is one.

The INPUT TALLY of an engine records which of the seed's two named
inputs its declaration carries: the stake, carried by every generator,
and the stream, carried exactly when growth is in its continuation.

THE PROBE of an engine at a reading: the root is the genesis state.  At
level one, a root with demands is answered -- every demand, every tied
minimum, one edge each -- and a demand-free root fires every enabled
continuation rule, one edge each.  At level two, the demands of every
level-one state are read; at a level-one state reached by a continuation
edge, every demand is answered by the responder too, and its enabled
continuations are named; nothing beyond level two is built.  Every node
of the probe replays from the reading's genesis by the engine's replay
rule, and every edge is checked to hold only the events of the
capability it is attributed to.

Two engines are PROBE-ISOMORPHIC at a reading when their probes are
isomorphic as rooted labelled trees, a node labelled by the sealed key
of its regime, its mode, the kinds and number of its demands and, at a
level-one state reached by continuation, the kind, cost and tie count of
each of its answered or refused demands, and an edge labelled by its
kind and, for a response, the demand kind and cost.  They are
PROBE-ISOMORPHIC when they are so at both readings.

Two filters are declared on the probe.  An engine is LIVE when at each
of the two readings its probe holds at least one answered demand.  An
engine is TWO-KINDED when at each reading demands of both kinds are read
at nodes of its probe.

## The question

- *One.*  How many engines does the class hold, and the seed-literal
  subclass; what is the capability count of each, under each reading of
  growth; which are count-minimal and inclusion-minimal, over the class,
  over the seed-literal subclass, and over the live and the two-kinded
  members of each, with every tie retained?
- *Two.*  Is any engine of the class one declaration; does any label in
  the supplied trees call a bundle one declaration, and what does that
  bundle count?
- *Three.*  In each of those subclasses, does a minimal member exist, are
  its minima unique up to probe-isomorphism, and is any member initial
  under inclusion of declarations?  Where the claim is refused, by which
  countermodel?
- *Four.*  At each reading, what does the probe of every engine hold:
  its root's demands and their kinds, the cost and tie count of every
  answered demand, every refusal, every continuation fired, the demands
  of every level-one state, and every fixpoint; does every node replay,
  and does every edge hold only the events of its capability?
- *Five.*  In the Lean mirror of the sealed kernel and isomorphism: what
  is an engine, as a definition, and is every step of every run one the
  declaration names; is a demand-free state of an engine with no
  continuation a fixpoint; are the labels and demands of each rule of
  the class reading only the first, fourth or sixth observable, in each
  mode, carried by every inhabitant of the sealed isomorphism, and under
  which hypotheses; which rule never demands, in which mode; which two
  rules are one another's flip; what does each rule of the class read at
  the sealed genesis of reading L; and which of the capability-count
  facts of question one hold by proof over the declared class?
- *Six.*  Does the probe's responder agree with rung two's minimum
  responses wherever both apply, and does the probe's partition by the
  sealed key procedure agree with the brute-force minimum over every
  bijection pair; does the probe-isomorphism decided by labels agree with
  a brute-force search over the bijections of each probe's level-one
  states?
- *Seven.*  What does this attempt leave for the second: which engines
  must challenge four run, from which readings, and to which bounds; and
  what of the seed's required questions four and ten, and of the count
  of declared inputs, is proved, countermodelled, computed or OPEN here?

No answer to any of the seven is stated here and none is expected.  Each
is closed by a proof, by an executable countermodel, by a finite
computation with its scope, or by an explicit OPEN status.

## What is reconstructed and what is native

The sealed kernel's regime, well-formedness, contexts, derivability,
collapse, separability, event kinds, step, replay and genesis, and the
sealed isomorphism structure, are reconstructed verbatim from the sealed
sources, as rungs three to ten did, with a pin note and a
declaration-by-declaration comparison with the pinned sources.  Nothing
sealed and no sibling package is imported by the Lean of this tree.
Where a statement here repeats one an earlier rung proved, it is proved
again inside this package so that the package stays self-contained, and
the ledger credits it.  No sibling source is copied into the Python of
this tree: the sealed kernel, the sealed profiles, the sealed candidate
space and measures, the sealed key procedure, the sealed genesis
readings, rung two's rule class, observables, dynamic validity and
minimum responses, rung one's validity members and no-op filter, and the
two-sided tree's honour relation are consumed read-only through their
public functions, pinned by blob.

The sealed candidate space and minimum responses are NOT reconstructed
in Lean, and neither are the observables O-two, O-three and O-five.  So
no Lean statement here is about a minimum, a cost, a tie, a profile
size or a class count; the capability census is proved over its declared
finite class, and the probe's numbers are finite computations.

## Discipline

Every substantive line carries exactly one evidence class.  A target
true by unfolding a definition, by kernel computation over concrete
objects or by case exhaustion over the declared finite class is
recorded as being at the level of a definition, in those words, and is
never counted as content.  No theorem is stated without its grammar in
the same sentence.  A demand read off the state is kept distinct from a
requirement imposed by an event and from an edge's marker.  A response
computed by the responder is a model proposal until its admission events
are replayed; the probe replays them.  An engine's count is a count of
its declaration, and says nothing of what the engine does.  Predictions
are frozen before the first computation and before the first compile,
scored mechanically, and never edited.  A receipt is not a proof.  A pin
proves only that a source did not move.  A gate is proved by failing on
the defect it exists to catch, with the failure naming the injected
object, and by recovering when the injection is reversed.  Nothing of
the sealed estate's standing obstructions is treated here as anything
other than standing.
