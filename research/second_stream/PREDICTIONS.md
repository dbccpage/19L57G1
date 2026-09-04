# PREDICTIONS: rung one, the stream as a response

`AuthorityEffect: None`. Frozen by sha256 before any computation and
before any Lean, and never edited afterwards. A missed prediction is
recorded next to its value in `STATUS.md` and kept as a finding.

## Chronology, stated against this run

`PROMPT.md` existed when this file was hashed. **No module of this tree
existed, no receipt had been written, and nothing had been enumerated at
any item count.** The sealed kernel, the sibling trees, and their
committed receipts had been READ before these predictions were written,
and several were reasoned from what was read: each prediction below
carries a FORCED or NOT FORCED label saying so, and a prediction labelled
FORCED is a control on the apparatus rather than evidence about the
question.

## How these are scored

Each prediction carries a falsifier: the exact observation that scores it
MISSED. Scoring is mechanical, from `receipts/stream.json`, and the
scoring code is committed with the rung. A prediction whose population
turns out empty is scored VACUOUS and is recorded as evidence of nothing;
the verdict is never rounded up to HIT. `R1-X` is the extrapolation
required by the run's standing orders: it states a verdict for a rectangle
this rung does NOT compute, is scored PENDING here, and is scored for real
by the rung that reaches that rectangle.

## Predicted

### R1-1

The rung's item-count-parametric enumerator is exhaustive within its
declared bound, in both directions that can be checked. (a) At costs zero,
one and two it yields exactly what the sealed `iter_full_deltas` yields on
every base of the declared cross-check family. (b) At costs zero, two and
three its output set equals the independently written superset-and-filter
construction on every base of that family. (c) At cost one the superset-
and-filter construction exceeds it by exactly the set `{(NewRuleAll(f),) :
f in base.rules}`, which is non-empty on at least one base of the family.

**Falsifier.** For (a) or (b), one delta in the sealed item order present
in one construction and absent from the other, on any base of the family
at that item count. For (c), a difference set that is not exactly that
closed form, or a family in which that set is empty on every base.

**Forced?** SPLIT, and this is the correction against the draft, which
asserted (a) and (c) of the same construction and so contradicted itself.
(a) is FORCED by the delegation `yield from iter_full_deltas(...)` and is
kept only as a regression guard on that delegation. (b) is NOT FORCED and
is the rung's only mechanical guarantee that the three-item space is not
silently missing the two-new-form and two-fresh-datum shapes; the sealed
constants `len(base.forms) + 1` and `range(n0 + 1)` are two-item constants
and copying them is this rung's likeliest silent error. (c) is NOT FORCED
and, in the draft, was VACUOUS: every base of the draft's family had an
empty rule set, so the clause could never fire. It is now live because the
family carries ruled bases, which the aggregate receipt shows the runs
actually reach (`same:rule` 4, `same:inst+rule` 8). It rests on
`AdmitRuleAll` being idempotent rather than raising and on
`iter_cost1_items` excluding already-ruled forms; either reading being
wrong scores a MISS.

### R1-2

With its own bound set to two items, the rung's reconstructed tree loop
reproduces, for all twenty tree identities, the node count, the
`by_status` histogram, the edge count and the refusal list stored in the
committed sibling receipt; and the rung's selection returns delta-for-
delta and cost-for-cost what the public `two_sided.min_responses` returns
at every state and target of those runs.

**Falsifier.** Any one of those four quantities differing for any one of
the twenty trees, or any state and target at which the two selections
differ in the deltas returned or in the cost tuple.

**Forced?** NOT FORCED. It is a faithfulness claim about a loop the rung
is forbidden to copy and about a declared no-op and ordering policy
standing in for two private sibling helpers. A miss means the
reconstruction diverges from the pinned apparatus, not that the
mathematics moved.

### R1-3

Every one of the seventeen runs whose pinned two-item record contains no
refusal -- every run except L/parity/mu1, L/residue_three/mu1 and
F/parity/mu1 -- has, at the three-item bound, an identical node count,
identical per-status counts, identical edge count, identical growth-edge
count, and an identical count of edges carrying a datum item.

**Falsifier.** Any one of those five values differing, for any one of
those seventeen runs.

**Forced?** FORCED, and labelled so. A run that records no refusal never
has `min_responses` return None, so it never reaches an item count above
two; `iter_cost1_items` and `iter_full_deltas` at costs zero to two read
only `bounds.max_arity` and never `bounds.max_items`; and each run carries
its own merge map, so no divergence elsewhere reaches it. Only the
seventeen-unchanged half is forced: whether the OTHER three differ is
R1-7's question and is not asserted here. Recorded as a control on the
driver, the quotient and the attachment, explicitly not as evidence about
the three-item bound.

### R1-4

Headline. No retained minimum response at the three-item bound, at any
state any of the twenty runs reaches, under any of the five stakes, either
reading, or either measure, contains a datum item:
`two_sided.has_fresh_datum` is false for every retained delta of every
retained tie class.

**Falsifier.** One retained minimum delta for which
`two_sided.has_fresh_datum` is true, reported with its reading, stake,
measure, node, target, item count, tie class, and the number of ties
retained beside it.

**Forced?** NOT FORCED, and not a consequence of the two-item result.
TS-08 is a FINITE_COMPUTATION scoped to two items whose 'what does not
follow' column reads 'the same at three items, which was not run (TS-16)';
TS-15 is a CONJECTURE whose own column reads 'the same at three items';
TS-16 is flatly OPEN. The three-item space offers, for the first time, a
fresh datum with two instances -- and those two instances can name the
fresh index in DIFFERENT slots, so they add different contexts to two
different held data rather than the same context to both, which is exactly
the case TS-15's two-item reasoning does not cover. Equivalence the rung
states rather than leaves to inference: because `key_of`'s third component
begins with the datum count, a datum-bearing delta never shares a class
with a non-datum-bearing one and is therefore always a retained
representative, so 'no edge carries a datum item' and 'no minimum contains
a datum item' are the same statement.

### R1-5

No VALID three-item response to a demand of the same kind contains a datum
item -- valid, not merely minimum -- at any state where a three-item
enumeration is performed. All fifteen recorded refusals are same demands,
so this population is non-empty by construction.

**Falsifier.** One valid three-item delta containing a `NewDatum` item
that honours a same target under the inherited no-regress rule, at any
state reached.

**Forced?** NOT FORCED, and the mechanism behind it is recorded together
with the mechanism that would break it, so a hit is not read as
confirmation of the argument. For it: profiles only grow under delta
application, and an addition that falls identically on both members of a
pair cannot turn two unequal sets equal. Against it: two instances naming
the fresh index in different slots -- one as `(f, (i, k))`, one as `(f,
(k, j))` -- add `(f, (None, k))` to datum i and `(f, (k, None))` to datum
j, which are DIFFERENT contexts, so the symmetry argument does not close
and a same demand could in principle be honoured through a fresh anchor.
That is precisely the shape TS-15's two-item statement excludes by
counting items, and it is the reasoning commit `240dc2a2` demoted from a
terminal's justification to a conjecture.

### R1-6

Every valid three-item response to a demand of the same kind contains
either at least two instance items or at least one uniform-rule item.

**Falsifier.** One valid three-item response to a same target carrying at
most one `NewInst` item and no `NewRuleAll` item.

**Forced?** NOT FORCED, and NOT SCORED AS A HIT ON AN EMPTY POPULATION.
This is the correction against the draft: three-item enumeration is
reached only where every response of fewer items fails, and all fifteen
recorded refusals are same demands, so if R1-7 misses this population is
empty and a presence-blind reading would score it HIT on zero candidates
-- exactly the all-hit failure the trap list quotes rung 0 and `d2896e50`
against. The frozen text therefore declares that an empty population
scores VACUOUS, which is recorded as evidence of nothing. Where the
population is non-empty the claim is the constructive half of R1-5's
mechanism: a form item alone adds contexts nobody derives and a datum item
alone adds nothing to a held datum's profile, so only instances and
uniform rules move a held datum's profile. If R1-6 misses, R1-5's
mechanism is wrong even where R1-5's verdict happens to hold.

### R1-7

At least one of the distinct refusal situations re-derived from the
fifteen recorded refusal records -- each a regime, a commitment, a demand
kind and a target pair -- admits at least one valid response of exactly
three items under the inherited no-regress rule, and is answered.

**Falsifier.** Every distinct refusal situation enumerates, unpruned and
to completion within the declared candidate and enumeration budgets, to no
valid three-item delta.

**Forced?** NOT FORCED, and it is the prediction this packet exists for.
Nothing committed decides it: TS-16 is OPEN ('Whether a three-item bound
admits a fresh datum into a minimum, or answers the 15 recorded refusals'
| OPEN | 'none; not run'), and TS-15 is a CONJECTURE whose own scope note
excludes three items. For it: at each refusal state, costs zero to two
exhaust a space of only thirteen, twenty or twenty-five single items and a
few thousand two-item deltas, while three items opens a pool two to three
orders of magnitude larger, offering compensation shapes that do not exist
at two items -- honour the target with two items and repair the one
regressed pair with a third. Against it: the profile symmetric difference
at those states may exceed what three items can close. Scoring note frozen
with the claim: 'fifteen refusals' counts NODES, not situations, and a
refusal short-circuits its node (the loop breaks on the first unanswerable
target), so fifteen is a lower bound on unanswerable targets and the
scored population is the deduplicated one.

### R1-8

The three-item run still records at least one refusal, whether one of the
fifteen or a newly reached one, somewhere across the twenty runs.

**Falsifier.** The three-item receipt records zero refusal records across
all twenty runs.

**Forced?** NOT FORCED. Paired with R1-7 it brackets the outcome from both
sides, so either miss is a finding rather than a null result. It also
decides the scope of any negative headline: a run that refuses nowhere has
a differently truncated frontier from one that does.

### R1-9

Availability, at the item bound the frozen question names. Across the
twenty runs the two-item census records more than zero nodes at which a
valid response containing a fresh datum exists while the retained minimum
sits at a STRICTLY SMALLER item count -- that is, at those nodes the fresh
datum is priced out rather than invalid; and at every such node the demand
it answers is of the apart kind. The companion counters record that the
census visited every node and that at least one three-item enumeration was
performed.

**Falsifier.** The two-item census reports zero such nodes; or it reports
one at which the answered demand is of the same kind; or
`three_item_enumerations_performed` is zero; or `nodes_censused` is below
the node population; or the count of fresh-datum candidates examined is
below the count the enumerator offered.

**Forced?** NOT FORCED, and the item bound is now declared in the frozen
question, which the draft's wording left open. The first clause measures
something no run in this repository has computed: `edges_with_fresh_datum`
records fresh data among RETAINED MINIMA, and first-cost-wins means a node
whose minimum is at zero or one item never examined a two-item delta at
all, so the census is neither a restatement of the sibling receipt nor
forced by it. The second clause is a genuine structural bet whose
mechanism is R1-5's. The counter clause is not decoration: commit
`dbaa4b73` repaired rung 0 for writing `"demands_all_free": 0,
"responses": 0, "single_chain": True` as literals, and rung 0's
`responses` counter is structurally zero because the string 'response' is
never appended anywhere in that module. A zero must be a counted zero.

### R1-10

Every run terminates under the declared bounds with no declared budget
fired and no unhandled abort: no `terminal_enumeration_budget`,
`terminal_candidate_budget`, `terminal_response_budget` or
`terminal_class_budget` appears in any receipt row; any bijection-budget
exhaustion is recorded as `terminal_iso_budget` on the node that raised it
rather than escaping; and `receipts/stream.json` regenerates byte-
identically on a second run with no CR byte.

**Falsifier.** Any of the four budget terminals present in the receipt; or
an unhandled `RuntimeError` from `dual._budget` escaping the loop; or a
receipt whose second generation differs by one byte.

**Forced?** NOT FORCED, and deliberately stated so that a truncation is a
MISS and a finding rather than a silent footnote. `terminal_iso_budget` is
dead code in the sibling -- the real raise site, `key_of` inside `_attach`
and at the root, sits outside every handler, and `closure_targets` is
`return demands(s)` and cannot raise -- so that guard is new code. It can
genuinely fire here: a three-item delta may carry two fresh data, the
growth data bound of five does not bind a response, and `dual._budget`
counts data-factorial times form permutations, which passes `PERM_BUDGET =
100_000` at eight data with three forms.

### R1-11

The fifteen recorded refusal nodes present strictly fewer than fifteen and
strictly more than three distinct enumeration situations, where two
situations are the same exactly when the indexed regime component of
`two_sided.key_of`, the commitment name and the demanded pair all agree.

**Falsifier.** A deduplicated count of fifteen or more, or of three or
fewer.

**Forced?** NOT FORCED, and always scorable regardless of how R1-7 falls
-- which is why it is here. Nothing in the repository records how many of
the twelve L/residue_three refusal nodes at target [0,3] and four data are
the same situation seen repeatedly; the receipt distinguishes them only by
`single_item_candidates`, which is 25 at node 66 and 20 at the other
eleven, so at least two situations exist among those twelve and at most
twelve do. The prediction also disciplines the prose: it is the count that
decides whether 'fifteen refusals' may ever be written as 'fifteen
situations', which the trap list forbids.

### R1-X — the extrapolation

R1-X, frozen before the three-item rectangle is computed and scored
PENDING in this rung: at a bound of FOUR items, at least one accepted
minimum response contains a datum item, and every accepted minimum that
contains one answers a demand of the apart kind rather than of the same
kind. WHY THIS ONE. The negative extrapolation -- 'no retained minimum
contains a datum item at four items either' -- is the status-quo
continuation and the weakest available bet: it is the sentence this rung
would already have written at three items, restated one bound up, and in
the branch where three items answers every refusal it becomes true by the
first-cost-wins rule alone, since `min_responses` returns at the first
item count with a non-empty valid set. The positive claim can fail
informatively in either direction and is not a restatement of this rung's
own result. Its mechanism, recorded beside the claim and REFUSED as
evidence: a fresh datum's only purchase is as a regress-free anchor -- an
instance binding it to a held datum adds a context to that held datum and
to no other, and unlike a held anchor its own pairs are new demands rather
than regress -- so it costs one item more than a held anchor and exactly
as much as a new unary form, tying under the first measure and winning
under the second, but only where every held anchor regresses. Four items
affords three co-marks, and the four-item runs go deeper past every
answered refusal, where honoured same-pairs and therefore regress pressure
accumulate. The apart clause follows from R1-5's mechanism: a same demand
needs the poorer profile enlarged, which a fresh anchor enlarges
asymmetrically.

**The next rectangle.** `Bounds(max_items=4, max_arity=2)`, the item bound
the only dial moved: both sealed admission readings L and F from
`derivation.engine.READINGS`, the five named stakes of
`two_sided.COMMITMENTS`, both sealed measures,
`two_sided.genesis_history(reading, commitment)` as the genesis, at most
fifteen accepted rounds, a growth data bound of five that does not bind a
response, a pre-expansion node guard of two hundred and fifty, the
inherited no-regress validity `two_sided.response_valid`, every demanded
pair a target with no orbit quotient, the same quotient key
`two_sided.key_of`, and the same unpruned generic enumeration extended by
the same universe rule (`max_form = len(base.forms) + 3`, instance
arguments over `range(n0 + 3)`), under the same four declared budgets
rescaled and named in that rung's own question.

**Falsifier.** The four-item run reports zero accepted minima containing a
`NewDatum` item, OR reports at least one that answers a demand of the same
kind. Either observation scores R1-X a MISS. FROZEN SCORING RULE, declared
here so it is not decided afterwards: if the three-item run answers every
refusal so that no state anywhere is unanswered at three items, the four-
item runs are identical to the three-item runs, the count of fresh-datum
minima at four items equals the three-item count, and R1-X is scored on
that value like any other -- it is not excused as vacuous, and the VACUOUS
verdict declared for R1-6 does not reach it. The four-item rung records
the value next to this prediction and never edits this text.
