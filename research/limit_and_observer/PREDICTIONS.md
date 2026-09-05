# research/limit_and_observer — predictions, frozen before any module

Frozen together with `REQUIREMENTS.md`, before any module of this tree
existed, and not edited afterwards. Both sha256 values are pinned in
`verify_pins.py`. Every miss is recorded next to its value in `STATUS.md`;
nothing here is revised after a run.

AuthorityEffect: None.

## How to read the labels

**FORCED** — the prediction follows from an argument, or from a measurement
already performed on the sealed derivation before this file was written. Where
it is a prior measurement, the measurement is named. Calling such a prediction
a guess would be dishonest, and so would presenting it as a discovery of the
run.

**NOT FORCED** — a genuine guess. If it lands, that is evidence; if it misses,
the miss is the finding.

**Disclosure, in full.** Before writing this file the following were run
read-only against the sealed derivation and the numbers recorded: the
quotiented depth-3 population size; the grammar-monotonicity census; the
non-vacuity census; the reading-axis and aggregation enumerations; the
exhaustive minimum sealed prefix reaching a state admitting a raw-bit rival;
and a prototype of the observer ladder. Predictions 1, 2, 4, 5, 6, 9, 12, 13,
14 and 16 are informed by those runs and are labelled FORCED with the source
named. Predictions 3, 7, 8, 10, 11, 15, 17 and 18 were not measured before
freezing.

---

### P-1 — Population and monotonicity
The quotiented depth-3 population is **85** stated-state-free regimes; the
grammar is monotone non-decreasing along every one-item move, with **0**
violations over **243** quotiented moves, of which **65** enlarge the context
set and **178** leave it unchanged.
**FORCED** (measured before freezing).
*Falsifier:* any count differing, or any move with `contexts(base)` not a
subset of `contexts(child)`.

### P-2 — Both sealed bases are observationally vacuous
Both sealed Challenge-3 bases carry **zero** forms and therefore **zero**
contexts, so no observation finding whatever can be sited at them, and they
can carry only the calibration.
**FORCED** (read from the sealed genesis histories).
*Falsifier:* a non-empty context tuple at either base.

### P-3 — The calibration holds
Restricting this tree's space to the four sealed item kinds with `Rho = ()`
and running this tree's pricing routine with the separation demand at the two
sealed bases reproduces `artifacts/challenges.json` `challenge3` field by
field: L/`mu1` cost `[2,-1]` with 6 deltas in 3 classes; L/`mu2` `[2,1]` with
2 deltas in 1 class; F/`mu1` `[2,-1]` with 10 deltas in 5 classes; F/`mu2`
`[2,1]` with 2 deltas in 1 class; `cost_below_minimum_all_fail` true
throughout.
**NOT FORCED** — this tree re-implements the kernel rather than importing it,
so agreement is a real test of the re-implementation and a failure voids the
tree.
*Falsifier:* any field differing from the committed sealed artifact.

### P-4 — The reading axis is complete and small
The sixteen readings collapse to **8** complement classes, of which **7** are
non-constant; and, more sharply, to exactly **4** induced-separation
behaviours, because at a fixed context the coverage bit is constant across
data, so a reading either varies with the admission bit there or is constant
there.
**FORCED** (measured before freezing; the sharper collapse is an argument).
*Falsifier:* a fifth induced-separation behaviour, or two readings in one
behaviour class inducing different relations at some state.

### P-5 — The sealed observer is a point in the reader space
The sealed observation relation is **exactly** the reader with selection all
contexts, the behaviour that reads the admission bit only where the coverage
bit is absent, and the aggregation `s >= 1` — with agreement at **every**
state of the population, not merely at the bases.
**FORCED** (an argument: sealed separation at a context is
`(A or B_i) != (A or B_j)`, which holds exactly when `A` is false and the
admission bits differ; verified over the population before freezing).
*Falsifier:* one state where the two relations differ.

### P-6 — Lawfulness is a measured split, and is not stable in the width
At `w_max = 3` exactly **4** of the **8** aggregations with `a(0) = false` are
lawful: the blind one, `s` odd, `s` not in `{0, w}`, and `s >= 1`. The count
is width-dependent: 2 of 2 at `w = 1`, 3 of 4 at `w = 2`, 4 of 8 at `w = 3`,
4 of 16 at `w = 4`.
**FORCED** (measured before freezing).
*Falsifier:* a different lawful count at any width, or a lawful aggregation
that is not the kernel of one of those four families.

### P-7 — The limit is NOT statable in the admitted grammar
No object admissible by the six declared item kinds is determined by a family
of admitted states and equal to no member of it. Concretely: every admitted
reader's stage verdict is a function of that stage's regime alone, so no
admitted object realises a family verdict passing both the stability and the
novelty test. The outcome for LIM-F is **PROVED OBSTRUCTION**.
**NOT FORCED.**
*Falsifier:* an admitted delta whose reader passes both tests; or an item
sequence producing a reader whose stage verdict reads the stage index, an
earlier regime, or its own earlier verdict.

### P-8 — LIM-F's core implication is definition-level, and says so
The implication "stage-local readers agreeing at every stage have equal family
verdicts" is true by unfolding and carries **no content**; the content is the
exhaustiveness check over the enumerated grammar, which is a real property and
can fail. The receipt classifies it as definition-level.
**NOT FORCED.**
*Falsifier:* the receipt classifying it as content, or the exhaustiveness
check being absent.

### P-9 — Refinement without end is obstructed at the carrier
LIM-R is **PROVED OBSTRUCTION**. A lawful reader's induced partition of the
admitted data has at most `n_data` blocks, so a chain of strict splits has
length at most `n_data - 1`, and the demand asks for `m > n_data`. The ceiling
is **attained** at **26** states of the population, so the obstruction is not
vacuous.
**FORCED** (the bound is an argument of the shape of `Compression`'s
`chain_bounded`; the attainment count was measured before freezing).
*Falsifier:* a lawful reader chain strictly longer than `n_data - 1` at any
state — which would also refute the transport and mean the class count is not
the right monotone quantity for reader partitions.

### P-10 — No finite delta in the declared alphabet lifts LIM-R
Because the demand's threshold is stated relative to the carrier and the
ceiling tracks the carrier exactly, **no** finite delta over the six declared
item kinds lifts the LIM-R obstruction — not one `NewDatum`, and not any
number of them. The smallest lifting admission is therefore a **seventh item
kind**, and the receipt **names the capability** it would have to carry rather
than quoting a number for it.
**NOT FORCED.**
*Falsifier:* a delta over the six kinds after which LIM-R is satisfiable.

### P-11 — Growth without end is obstructed at a derived width threshold
LIM-G is **PROVED OBSTRUCTION** with the threshold **`2^w_max` = 8** admitted
data: equal signatures force `s = 0` and `a(0) = false`, so the non-separation
relation of any fixed-selection reader is coarser than signature equality and
has at most `2^w` blocks; once the carrier exceeds `2^w`, some pair is
identified, for **every** selection, **every** behaviour and **every** lawful
aggregation. The positive control passes: at carriers within the threshold a
reader separating every pair exists.
**NOT FORCED.**
*Falsifier:* a fixed-selection admitted reader separating every pair at a
carrier larger than `2^w_max`.

### P-12 — Refinement and growth do NOT cost the same
The two directions carry **different** outcomes and different escapes.
Refinement's obstruction is carrier-relative and is lifted by no finite delta.
Growth's obstruction is width-relative with an absolute threshold `2^w`, and
*is* lifted at any given carrier by buying width — one `AddContext` per
doubling of the carrier, hence a **rate** of about `log2(n)` items and not a
one-step price. Neither has a one-step price; they fail to have one for
different reasons, and the asymmetry is the result.
**FORCED** (given P-9, P-10 and P-11).
*Falsifier:* the two directions returning the same outcome with the same
escape.

### P-13 — The second observer has a price, and it is 5
OBS-3 (rival) has minimum `mu1 = 5` at **both** sealed genesis bases, and
`mu2 = (5, 1)`. The arithmetic is forced: 3 sealed items to reach a state
where both derivability bits are live at one context — verified exhaustively,
none at one or two items in either reading — plus `NewReader` and one
`AddContext`.
**FORCED** (measured before freezing, prototype).
*Falsifier:* any candidate answering OBS-3 at four items or fewer.

### P-14 — Every minimum rival prefix has the same forced shape
Every minimum sealed prefix reaching a rival-admitting state is a **form**, a
**uniform rule on it**, and an **explicit instance** — 6 raw minima in 3
isomorphism classes in reading L, 12 raw in 3 classes in reading F — because
the conflation the sealed relation performs is invisible until both bits are
live at one context. Under `mu2` the classes collapse toward the arity-1
class.
**FORCED** (measured before freezing).
*Falsifier:* a minimum prefix of any other shape.

### P-15 — The rival is DERIVED, not admitted
OBS-5 returns **derived** at the minimum: the rival's induced relation is a
value of the declared combination set applied to the sealed observer's
relation. It is inside by construction, and is therefore **not** the outside
reader the estate's open bridge names. This is a negative answer to the
brief's sharpest question.
**NOT FORCED.**
*Falsifier:* a minimum-cost admitted reader outside the combination set at
every state where it is defined.

### P-16 — The degenerate answer is cheaper than the real one, and the ladder shows it
OBS-1 and OBS-2 are both answered at `mu1 = 3` by a **blind** reader, which is
strictly cheaper than the rival's 5. OBS-4, which bars the degenerate answer,
costs strictly more than OBS-3 and **differs between the readings**.
**FORCED** for the value 3 and for OBS-4 exceeding OBS-3 (measured before
freezing); the exact OBS-4 values are asserted as **8 in reading L and 7 in
reading F**, which is NOT FORCED beyond the prototype that produced them.
*Falsifier:* OBS-1 or OBS-2 above 3, or OBS-4 at or below OBS-3, or equal
OBS-4 values across the readings.

### P-17 — The second observer is decisively cheaper
The second observer is cheaper than the limit in the only sense the shared
units support: it has a finite one-step price in the declared space and every
limit direction has **none**. The comparison table records this as
"PRICE versus PROVED OBSTRUCTION", not as an inequality between two integers.
**NOT FORCED.**
*Falsifier:* any limit direction returning a finite one-step price, or OBS-3
returning an obstruction.

### P-18 — Neither purchases the other, with one expected containment
Neither demand's retained minima satisfy the other's predicate, in either
direction; no single delta is minimal for two demands of different evidence
arity; and the canonical key sets of the minima families are incomparable —
with the one expected exception that **refinement purchases growth**, because
a chain past the carrier needs the carrier to grow. The brief's "agrees with
the first only in the limit" possibility is expected to be **unavailable in
this grammar** rather than false: two stage-local readers agreeing at every
stage are indistinguishable to anything reading only their verdicts, and the
unavailability is the finding, not an omission.
**NOT FORCED.**
*Falsifier:* any purchase test returning true in an unexpected direction, or a
delta jointly minimal across evidence arities.

---

## What would surprise me, in order

1. **Most:** an admitted reader separating a pair on which the raw bit pair
   agrees at every context. That would mean a reader reading outside the
   judgment grammar and that the anti-richness guard has a hole. It is argued
   impossible and tested for anyway.
2. OBS-3 coming in below 5. The sealed **prefix** space was searched
   exhaustively; the full extended space with reader items interleaved was not
   searched before freezing, and an interaction not imagined here would be a
   genuine surprise and a better result.
3. A lawful aggregation at some other width in a pattern that is not the
   kernel of a derived view. `DiffInterface` says every concrete observer
   below it is a kernel observer and the `w = 3` enumeration reproduced that
   exactly; a counterexample would be a real find about the estate's own
   claim.
4. An admitted reader outside the combination set at every state — a genuinely
   admitted rather than derived observer. That would put a priced object next
   to the estate's open bridge instead of merely showing that the cheap
   candidate cannot be it.
5. **Least likely, most consequential:** a lawful reader chain strictly longer
   than the carrier. That would refute the transport, reopen refinement
   without end, and mean the class count is not the right monotone quantity. It
   would be reported and the run stopped.

## The honest caveat about scale, written before the run

The primary population is 85 quotiented states at depth 3, and a rival appears
at only **6** of them. That is non-zero and enough to price, but it is thin.
Depth 4 is where the finding would become robust rather than merely
non-vacuous. If depth 4 is not reached within the declared budget, the right
report is the depth-3 price with the exact population named and the depth-4
census recorded **OPEN** — never a price dressed as more general than the
states it was computed over.
