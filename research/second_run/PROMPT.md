# PROMPT: continuation two -- run forward

`AuthorityEffect: None`.  This file is the question of the second and
last research attempt of the continuation the author authorized on
twenty-fifth September twenty twenty-six.  It states no expected value
and names no expected terminal; every number in it is spelled out.  It
is frozen by hash before anything else in this tree is written, and
before any computation of this attempt and any Lean is built.

## Where the question comes from

The author's ruling of twenty-fifth September twenty twenty-six,
recorded verbatim in `research/second/MANUAL.md` and in `CLAUDE.md`,
authorizes at most two further research attempts: first the seed's
challenge three, then challenge four with its engine-dependent census
evaluations.  The first closed as `research/second_engine/` and was
integrated by the author.  Its `STATUS.md` names this attempt as its
leftover G-one, "run every member forward", with G-two, whether a member
without the stream carries the grammar forward, and G-seven, the probe
beyond level two, inside it.  This is the second attempt.  It keeps its
declared bounds, it may terminate OPEN, and no attempt after it is
authorized.  The seed is unchanged; the continuation is a protocol
intervention by the author, and this tree is a result of that
intervention, not of the seed's next-rung rule.

The seed's challenge four reads: for each surviving engine, from each
sealed genesis reading, run to the declared bounds, quotienting by the
implemented isomorphism, retaining ties, replaying every node from
genesis, and exporting the exact frontier; record every terminal by
kind: fixpoint, refusal, bound, guard.  Its challenge five asks that at
every stage of every run each notion of a declared list be decided by
an implemented algorithm as DEFINABLE, a USEFUL REALIZATION, FORCED
(proved to hold in every surviving engine), or none of these.  Rungs
three to ten decided the DEFINABLE and USEFUL REALIZATION columns of
twelve notions over histories supplied from outside; the FORCED column
of all twelve is undecided, and by the author's ruling a proved negative
decision resolves it as well as a proved positive one, while recording
OPEN does not.

## The supplied pieces, consumed and never copied

- The sealed kernel: regimes, the six event kinds, step, replay, the two
  sealed genesis readings L and F, the sealed profiles and separability,
  the sealed candidate space at the sealed bounds (at most two items,
  arities at most two), the two sealed cost measures, the sealed key
  procedure with its isomorphism witness and its brute-force minimum,
  and the sealed automorphisms, with the sealed permutation budget of one
  hundred thousand.
- Continuation one's declarations, through the public functions of
  `research/second_engine/engine_decl.py` and `engine_probe.py`: the
  class of one hundred and forty-four members and its seed-literal
  subclass of one hundred and eight, the state (a sealed regime and a
  mode), the generator read in the state's mode, the responder (the
  least responses of every demand under both measures and both validity
  members, every tie kept), growth below four data, the switch marker,
  the engine's replay rule, the capability sets and counts, the minima
  and initial-member functions, and the probe to level two with its
  LIVE and TWO-KINDED filters.
- Rung two track two's observables, through its public functions: the
  profile class count.
- Rung ten's readings, through the public functions of
  `research/second_response/response_rows.py`: holding two, the count of
  exhausted forms, and the pairs a change of regime MOVES (a pair of the
  earlier regime's data whose sealed separability differs across the
  change).

## The objects

The ENGINE, its STATE, its DEMANDS, its RESPONSES, GROWTH, SWITCH, the
CLASS, the SEED-LITERAL SUBCLASS, CAPABILITIES and the PROBE are
continuation one's, unchanged.

A ROUND is one step of an engine: the admission of one response, one
growth, or one switch.  A round is CHANGING when the regime after it
differs from the regime before it; a switch changes the mode and not the
regime.  A round is a DATUM ROUND when the regime after it holds more
data than before it, whether by growth or by a response whose delta
holds a datum; a REST ROUND is a changing round that is not a datum
round.

THE STATE RELATION: two states are one NODE when the sealed keys of
their regimes are equal and their modes are equal.  A node carries the
first state reached in it, its REPRESENTATIVE, and the history that
reached it.

THE RUN of an engine at a reading is a finite directed graph built
breadth-first from the ROOT, the node of the reading's genesis state.
The STAGE of a node is the least number of rounds on a path to it from
the root.  To EXPAND a node is to read its demands in its mode, and:

- when it has a demand, to answer every demand by the responder under
  the engine's measure and validity member, every tied minimum one edge,
  each edge carrying the admission events of its delta; a demand with no
  accepted delta within the sealed bounds is REFUSED;
- when it has none, to fire every continuation rule of the engine
  enabled there, each one edge.

Every edge is kept, including an edge into a node already present.  A
node is expanded exactly when its stage is below fifteen, the run holds
fewer than two hundred and fifty nodes when its expansion would begin,
and neither the sealed key procedure nor rung two's observables have
exceeded their permutation budgets on it.  Each node that is not
expanded, or is expanded and has no edge, is classified by exactly one
TERMINAL KIND:

- FIXPOINT: it has no demand and no enabled continuation rule;
- REFUSAL: it has a demand and every demand is refused;
- BOUND: it is not a fixpoint, its stage is fifteen, and it is not
  expanded;
- GUARD: it is not a fixpoint and is not expanded because of the node
  guard or a permutation budget.

The FRONTIER of a run is its BOUND and GUARD nodes, each exported
exactly: the sealed key of its representative, its mode, its stage, and
its demands.  A run is CLOSED when its frontier is empty.

A MERGE is an edge whose state falls into a node already present.  At
every merge the sealed isomorphism witness from the edge's state to the
node's representative is found, and the generator's label of every pair
of the edge's state is compared with the label of the witnessed image
pair in the representative, each read in the node's mode.  A
disagreement is a QUOTIENT DEFECT, and is counted.

REPLAY: every node's history replays by the engine's replay rule to its
representative; every edge's events replay from its parent's
representative to a state of its child node.  Every mismatch is counted.

A RUN PATH is a path in the run graph from the root.  The ROUND
POPULATION at round k, for k from zero to fifteen, is the set of nodes
at the end of some run path of exactly k edges, together with every
FIXPOINT and REFUSAL node at the end of a run path of fewer edges (no
act occurs at such a node, so its state persists).  The round population
at k is COMPLETE when no node at the end of a run path of fewer than k
edges is a BOUND or GUARD node.

## The census, as this attempt reads it

Twelve notions, the census rows of the seed's challenge five, in the
seed's order.  Each is given a STAGE READING, a RUN READING, or both.

A STAGE READING is a value computed at each node from its
representative's regime or its place in the run.  A stage reading of a
notion is FORCED AT ROUND k over a set of engines at a reading when every
round population at k of those engines' runs is complete and the value
is the same at every node of their union; it is NOT FORCED AT ROUND k
when two nodes of that union carry different values, with the two
engines and nodes named; otherwise it is UNDECIDED AT ROUND k.

A RUN READING is a property of a run with three outcomes: HOLDS, FAILS
with an exported witness, or UNDECIDED.  Three kinds are declared.

- EVERY RUN REACHES: every maximal run path takes a node or an edge with
  the property.  It HOLDS when every run path meets the property before
  it meets a BOUND or GUARD node; it FAILS when some run path avoids the
  property and ends at a FIXPOINT or REFUSAL node or enters a cycle of
  the graph that avoids it; otherwise it is UNDECIDED.
- NO EDGE VIOLATES: no edge of the run violates a declared condition.
  It FAILS when some edge does; it HOLDS when none does and the run is
  closed; it HOLDS AT BOUND when none does and the run is not closed.
- ONE VALUE PER NODE: a quantity carried along run paths takes exactly
  one value at each node.  It FAILS when two run paths of at most
  fifteen edges bring two values to one node, or when a closed run has a
  cycle that changes the quantity; it HOLDS when the run is closed and
  acyclic and every node has one value over all its paths; it HOLDS AT
  BOUND when no failure is found and the run is not closed.

A run reading of a notion is FORCED over a set of engines when it HOLDS
in every run of every member at both readings; FORCED AT BOUND when it
HOLDS or HOLDS AT BOUND in every one and HOLDS AT BOUND in at least one;
NOT FORCED when it FAILS in some run, with the first failing member in
the class order, its reading and its witness named; and OPEN otherwise.

The readings:

- *One, two-ness.*  Stage: whether the regime holds two.  Run: every run
  reaches a regime holding two.
- *Two, the count of observational classes.*  Stage: the profile class
  count.  Run: no edge lowers the profile class count.
- *Three, succession of accepted rounds.*  Run, two readings: one value
  per node of the number of rounds on the path (EVERY), and of the
  number of changing rounds on the path (CHANGING).
- *Four, duration, as rounds between growths.*  Run: one value per node
  of the number of rest rounds since the last datum round on the path,
  or since the root when there is none.
- *Five, adjacency, as which pairs a single response can change
  together.*  Run: every run reaches a response edge that moves at least
  two pairs.
- *Six, reach, as the third-party effect of a response.*  Run: every run
  reaches a response edge that moves a pair holding a datum outside the
  demanded pair.
- *Seven, an invariant.*  Run: no edge lowers the element count, the
  number of data plus the lengths of the lists of forms, instances,
  uniform rules and requirements.
- *Eight, irreversibility.*  Run: no changing edge lies on a cycle of
  the run graph.
- *Nine, symmetry.*  Stage: the number of sealed automorphisms of the
  regime.
- *Ten, branching.*  Stage: the number of distinct nodes the node's
  edges lead to, zero at a FIXPOINT or REFUSAL node; a BOUND or GUARD
  node has no value and makes the round populations after it incomplete.
- *Eleven, exhaustion.*  Stage: the number of exhausted forms.
- *Twelve, recurrence.*  Run: every run reaches a node that lies on a
  cycle of the run graph.

The DEFINABLE and USEFUL REALIZATION columns are recorded per notion
with the reason: a stage reading computed from the representative's
regime alone is DEFINABLE at every stage; a stage or run reading that
reads the engine's responder is DEFINABLE relative to the engine's
declaration, the declaration that rung ten priced as a realization; for
three and four, the value is a function of the state within a run
exactly when the run reading does not FAIL, and the attempt says so per
run.

The SETS OF ENGINES over which every census verdict is computed: the
class; the seed-literal subclass; the LIVE and the TWO-KINDED members as
continuation one's probe defines them, recomputed here and compared with
its receipt; the STREAMLESS members, whose continuation does not hold
growth; and the streamless LIVE members.  Each single engine is also a
set, and the attempt records for how many engines each stage reading is
forced at every complete round.

## Further readings

- A run CARRIES FORWARD when it is not closed: it has a BOUND or GUARD
  node, every one of which is reached from the root by changing rounds
  only.  It TERMINATES when it is closed and acyclic, and CYCLES when it
  is closed and holds a cycle.
- An INVARIANT CANDIDATE is one quantity from this list: the element
  count; the numbers of data, forms, instances and uniform rules; the
  profile class count; the number of sealed automorphisms; the number of
  demands; the number of honoured labelled pairs.  For each engine and
  each candidate, the attempt decides by the NO EDGE VIOLATES reading
  whether the candidate is preserved, never lowered, or never raised
  along every edge of both its runs.
- Two engines are RUN-ISOMORPHIC at a reading when their run graphs are
  isomorphic as rooted directed graphs with node labels (the sealed key
  of the representative, the mode, the terminal kind or none) and edge
  labels (the kind, the demand kind, the cost, and the number of edges
  so labelled between the two nodes); RUN-ISOMORPHIC when so at both
  readings.  Because the node labels are pairwise distinct within a run,
  the decision compares the labelled graphs keyed by those labels; it is
  cross-checked against an exhaustive search over node bijections on
  every run of at most eight nodes.
- The sealed key partition of every distinct regime reached is compared
  with the sealed brute-force minimum on every regime whose count of
  datum and form bijections is at most one thousand four hundred and
  forty; the regimes above that count are counted.

## The question

- *One.*  For each of the one hundred and forty-four engines, at each of
  the two readings, what is its run: how many nodes and edges, at which
  stages, how many merges and ties, which terminals of which kinds, which
  refusals, and what exact frontier; is it closed, and does it carry
  forward, terminate, or cycle?  Does every node and edge replay, and is
  there any quotient defect?
- *Two.*  At every round from zero to fifteen, for each stage reading and
  each set of engines, is the reading FORCED, NOT FORCED or UNDECIDED,
  and with which value or which pair of witnesses?  For each run
  reading and each set of engines, is it FORCED, FORCED AT BOUND, NOT
  FORCED or OPEN, and with which witness?
- *Three.*  Which invariant candidates are preserved or monotone along
  every edge of every run of each engine, and is each such fact an
  invariant of every run of the engine (its runs closed) or of the
  bounds?
- *Four.*  Does any streamless engine carry forward at both readings;
  which, with which capability count; and which of the class's engines
  that carry forward at both readings are count-minimal,
  inclusion-minimal, or initial among them, every tie retained?
- *Five.*  How many run-isomorphism classes does the class hold, and do
  they refine, coarsen, or cross continuation one's probe classes?
- *Six.*  Does any response edge of any run carry a datum, and in which
  engines?
- *Seven.*  In the Lean mirror of the sealed kernel: is the element count
  never lowered by any sealed step or switch, and raised by every step
  that changes the regime; can any history of engine events return to a
  regime after a step that changed it; and is every cycle of engine
  states made of steps that leave the regime unchanged?
- *Eight.*  What does this attempt leave: what of the seed's required
  questions one to ten, of the count of declared inputs, and of the
  census, is proved, countermodelled, computed or OPEN here, at which
  bounds?

No answer to any of the eight is stated here and none is expected.
Each is closed by a proof, by an executable countermodel, by a finite
computation with its scope, or by an explicit OPEN status.

## What is reconstructed and what is native

The sealed kernel's regime, event kinds, step and replay are
reconstructed verbatim from the sealed sources, as the earlier trees
did, with a pin note and a declaration-by-declaration comparison with
the pinned sources.  Nothing sealed and no sibling package is imported
by the Lean of this tree.  No sibling source is copied into its Python;
every supplied piece named above is consumed read-only through its
public functions, pinned by blob.

The sealed candidate space, the responder, the observables and the
generators are NOT reconstructed in Lean.  So no Lean statement here is
about a minimum, a tie, a demand, a key, or a run graph: the Lean speaks
of every history of sealed events and switch markers, whoever chose it,
and the run graphs and census verdicts are finite computations.

## Discipline

Every substantive line carries exactly one evidence class.  A target
true by unfolding a definition, by kernel computation over concrete
objects or by case exhaustion is recorded as being at the level of a
definition, in those words, and is never counted as content.  A verdict
over the class at the declared bounds is a finite computation at those
bounds and is written with them; a FAILS outcome is an executable
countermodel and is written with its witness.  A demand read off the
state is kept distinct from a requirement imposed by an event and from
an edge's marker.  A response is a model proposal until its admission
events are replayed; every run replays them.  Predictions are frozen
before the first computation and before the first compile, scored
mechanically, and never edited.  A receipt is not a proof.  A pin proves
only that a source did not move.  A gate is proved by failing on the
defect it exists to catch, with the failure naming the injected object,
and by recovering when the injection is reversed.  Nothing of the sealed
estate's standing obstructions is treated here as anything other than
standing.
