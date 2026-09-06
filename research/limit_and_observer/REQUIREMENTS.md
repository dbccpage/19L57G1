# research/limit_and_observer — requirements, candidate space, measures

Frozen before any module of this tree existed. Not edited afterwards. Its
sha256 is pinned in `verify_pins.py`; `PREDICTIONS.md` is pinned beside it.

AuthorityEffect: None.

## 0. Two words this repository already uses for something else

**`refinement`** here means *partition refinement*: one selection of contexts
splits a block of another selection's partition of the admitted data. It does
not mean a step getting smaller in any size, and no size on steps is declared
anywhere in this tree.

**`limit`** elsewhere in this repository means the scope of a theorem
(`TH-LIMIT-SCOPE`, "limit_scope" in receipts). Here it names the two
directions of the question below and nothing else. Neither prior sense is
intended, and no third sense is introduced.

No outside theory is named or targeted. Every notion below is either taken
from the sealed derivation under a pin or admitted here as this rung's own
primitive, and each is classified.

## 1. What is being priced

The sealed derivation is finite and discrete throughout. Two things it has
named as missing are priced here, in one tree, under one pair of cost
measures, so that the comparison is a computation rather than an analogy.

### 1.1 The limit

Whether an object determined by a family of admitted states, and equal to no
member of that family, can be stated at all in an admitted observation
grammar, and what admitting it costs. Two directions, priced **separately**,
because whether they cost the same is a result and not an assumption:

* **Refinement without end (LIM-R).** The carrier is fixed and the reader's
  induced partition of the admitted data is split again without end.
* **Growth without end (LIM-G).** The carrier grows along a declared run and a
  reader of fixed selection keeps separating.
* **The family-determined verdict (LIM-F).** A verdict determined by the whole
  finite family of stage verdicts and equal to no member of it.

### 1.2 The second observer

Observation in the sealed derivation is a relation on admitted state. A second
observer is a second such relation. What must be admitted for two to exist,
whether they can disagree, what agreement costs, and whether either is
derivable rather than admitted.

**Inherited premise, narrowed.** The brief's premise that the estate carries a
result that the system is *not self-certifying* is stronger than what the
estate holds. What it holds is: certification is panel-relative
(`cert_not_correspondence`, `cert_panel_relative`), an explicit refusal to
define a self-evaluation interface, and the named irreducible obligation in
`OPEN_BRIDGES` that "the family interpreter is not a member of its own
described family; the outermost interpretation relation remains
metatheoretic". This tree inherits that as an **open obligation** and does not
discharge it.

## 2. The observation grammar of the sealed derivation, read exactly

Pinned source `code/derivation/observe.py`, line 56, in full:

    def derivable(r: Regime, inst: Inst) -> bool:
        return inst[0] in r.rules or inst in r.insts

The sealed observation relation is an **or of two independent bits**:

* **coverage bit** `A(c) = c.form in r.rules` — the context's form carries the
  uniform all-tuples rule. It does not depend on the datum plugged in.
* **admission bit** `B(c, d) = plug(c, d) in r.insts` — the plugging is an
  admitted instance.

Sealed derivability is `A or B`. The repository's assumption discipline says
supply, mention, admission, current-state designation, retention, observation
and equality are never conflated. The sealed observation relation conflates
coverage with admission, inside itself, and nothing in the estate reads the
two bits apart. That is where a second observer lives.

Classification of the paragraph above: **derived definition** (a reading of a
pinned source), not a theorem.

## 3. The reader — this rung's admitted primitive

An **admitted reader** is a triple `(K, b, a)`.

* **`K`, the selection.** A finite sequence of contexts of the current regime,
  `|K| <= w_max`, declared `w_max = 3`. A reader reads only *through* the
  judgment grammar and never names a datum by index.
* **`b`, the reading.** A total function `Bool x Bool -> Bool` of the bit pair
  `(A, B)`. All sixteen are admitted; the axis is therefore complete by
  construction over the pair the sealed `derivable` is built from, so no answer
  can have been excluded by taste.
* **`a`, the aggregation.** A total function `{0..w_max} -> Bool` with
  `a(0) = false`, applied to `s`, the number of contexts of `K` at which `b`'s
  value differs between the two data. `a(0) = false` is the discipline's own
  direction: a reader finding no separating context reports **no separation**,
  never equality.

**Lawfulness.** An admitted reader must be lawful *in general* — the induced
non-separation relation must be transitive over the whole of `{0,1}^w`, not
merely at one state. This is not a preference: `DiffObs` carries `zero_refl`,
`zero_symm`, `zero_trans` as **fields**, so an observer is admitted only
together with its proofs. Lawfulness is decided by an implemented algorithm
before admission, per `w_max`. Unlawful aggregations are enumerated, counted
and **refused by name**; they are a named boundary, not a silent exclusion. An
unlawful aggregation induces no partition, so no class count is defined for it
and no chain bound can transport to it.

**Admission events, two new item kinds.**

* `NewReader(b, a)` admits a reader with an **empty** selection. Such a reader
  is blind and separates nothing.
* `AddContext(rho, c)` adds one context to admitted reader `rho`'s selection.

A reader's width is therefore exactly the items spent on it. This is the
load-bearing anti-smuggle: if `NewReader` carried its selection, a candidate
would buy unbounded observational capacity at unit price and every number on
both sides of the comparison would be wrong by an unbounded amount.

**The sealed observer is not an admitted reader.** `observe.py` classifies
itself as metatheory apparatus and this tree does not promote it. The
reader-free slice of this tree is therefore exactly the sealed derivation, and
every sealed result remains a result about it.

## 4. The stated state, the item alphabet, the bounds

A **stated state** is `S = (r, Rho)`: a sealed `Regime` and a finite tuple of
admitted readers. Genesis has `Rho = ()`. The projection `pi(S) = r` is
asserted by test to commute with every sealed event.

**Item alphabet, six kinds:** the four sealed (`NewDatum`, `NewForm(arity)`,
`NewInst(form, args)`, `NewRuleAll(form)`) plus `NewReader` and `AddContext`.
A delta is canonically ordered, extending the sealed `item_key` with readers
after instances and context-additions after readers, so the order stays total
and deterministic.

**Bounds, declared, each refused rather than exceeded, each with a named
terminal:**

| bound | value |
|---|---|
| `max_items` | 8, split as a sealed prefix of at most 4 and a reader suffix of at most 4 |
| `max_arity` | 2 (sealed, unchanged) |
| `w_max` | 3 |
| `max_readers` per stated state | 2 |
| growth horizon `H` | 15 |
| bijection budget | 100000, `BijectionBudgetRefused` a named terminal |
| population depth | 3 |
| candidate budget per enumeration | 4000000, `CandidateBudgetRefused` a named terminal |

**The widening above two items is forced, not convenient.** Exhaustive search
from both sealed genesis histories under the sealed `Bounds(2, 2)`: the
minimum number of sealed items reaching a state that admits any raw-bit rival
is exactly **3**, in both readings, with **none at one or two items**. A tree
bounded at the sealed two items would have reported an obstruction that was an
artefact of its own bound. Following `research/second_stream`, the widened
space is **this rung's admitted primitive** and is never called the sealed
candidate space at that width; the three- and four-item enumerator is
certified by set equality against an independently written superset
construction one coordinate wider in each direction.

**Not used, deliberately.** The sealed `iter_cost2_deltas` is never called:
its four pruning lemmas are justified against *pair separation*, and none of
this tree's demands is pair separation. Validity is decided by naive replay,
never by the fast path, which is forced rather than cautious because
`NodeView.of` refuses a rule-bearing base and every minimum rival prefix
contains `NewRuleAll`.

## 5. The cost measures, and the argument that the units are shared

Exactly two measures, both re-implemented in this tree against a pinned
sealed source (this tree imports nothing across trees) and both asserted by
test to agree with the sealed originals on the whole enumerated space:

* `mu1(delta) = len(delta)` — the item count.
* `mu2(delta) = (len(delta), sum of arity over NewForm items)`, lexicographic.

**Why the units are shared, stated exactly.** Both halves of this tree are
priced by the *same two expressions*, on deltas drawn from *one* item
alphabet, at *one* population, under *one* isomorphism quotient, by *one*
pricing routine in which the demand is a parameter and never a branch. That is
what comparability means here and it is all it means.

**What shared units do not buy.** `mu1` counts items. "The rival costs 5 and
the limit costs k" is a statement about how many admitted items each requires
and nothing else — not difficulty, not importance, not order of payment.
`reach_measure` RM-22 records that even the *order type* of a base-relative
measure is OPEN. The substantive comparison therefore lives in the purchase
and containment tests of section 8, never in an inequality between two
integers.

**`mu2` is blind along the reader axis by the formula**, since reader items
declare no form arity. This is **reported as a finding and never repaired**:
amending `mu2` would stop it being the sealed function and would silently
change what every sealed answer means.

**Excluded by declaration, with reasons.** `mu3` and the nine
`path_dependent_cost` weightings are base-relative, and a base-relative cost
makes prices at different bases incomparable, which is the one thing this tree
must not permit. `mu_additive_atoms` (thinghood, 7 atoms, minimum 5) and
`mu_oriented_s9` (priced_admissions, 6 atoms, minimum 7/8) price nearly the
same object at different totals under differently chosen atom sets, and
`mu_fit_oriented_s9` is the latter renamed with no new computation; no total
from any of them appears here. `mu_type` and `mu_arity` are prose-only, with
no implementation and no gate. Every difference cost is proved
path-independent and zero around every closed walk (RA-9/10/11), so it cannot
witness a direction.

**Capability vector**, computed for every candidate and **never totalled into
a scalar** (totalling would invent a third measure): the sealed five keys
unchanged (`new_data`, `new_forms`, `new_form_arity_sum`, `new_instances`,
`new_rules`) plus `new_readers`, `new_reader_contexts`, `reading_class`,
`aggregation_lawful`. A price is reported as
`(mu1, mu2, capability vector, tie classes, base)` and never as a scalar.

## 6. The demands

Every demand is a total decidable predicate of `(stated state, delta)` with
one signature, priced by **one** routine: enumerate the space at item count
`0, 1, ..., max_items` in order; keep the satisfying deltas; return at the
first count with a non-empty set, refining by the measure's later coordinates;
quotient by the extended canonical key of the child stated state; retain every
tied class with its capability vector; decide `cost_below_minimum_all_fail` by
exhaustion and never by assertion. Because the demand is a parameter and not a
branch, no demand can acquire its own enumerator, bound or measure.

### The observer ladder — five rungs, fixed before any enumeration

* **OBS-1 EXISTENCE.** At least one admitted reader whose induced separation
  relation on the resulting state differs from the sealed observer's.
  Distinctness is decided by the **induced relation**, never by syntax.
* **OBS-2 SUB-READER.** OBS-1 with the admitted reader strictly coarser: it
  identifies a pair the sealed observer separates and separates none the
  sealed observer identifies.
* **OBS-3 RIVAL.** An admitted reader that **separates a pair the sealed
  observer identifies**. This is the rung that carries the question.
* **OBS-4 NON-DEGENERATE COEXISTENCE.** Two admitted readers, each separating
  at least one pair, giving opposite verdicts at the designated pair, neither
  an automorphism image of the other. This bars the answer bought by a reader
  that sees nothing — the estate already exhibits that reader
  (`natural_sections` NS-05, `blindObs`).
* **OBS-5 DERIVABILITY.** Whether an admitted reader's induced relation is a
  value of a declared finite combination set applied to the sealed observer's
  relation and to the other admitted reader — identity, complement,
  intersection, union, symmetric difference, and the two projections. Inside
  the set: **derived**. Outside for every combination: **admitted**. The
  enumeration says which; nothing is argued.

The designated pair is fixed **before** any enumeration by the equivariant
orbit policy (one representative per automorphism orbit of the collapsed
pairs), which replaced least-pair selection in the seal because least-pair
depends on the representative labelling.

### The limit — three demands, disjoint predicates, never summed

* **LIM-R REFINEMENT WITHOUT END.** `LIM-R` holds when there is a chain
  `K_0 ⊂ ... ⊂ K_m` of admitted selections, each step strictly splitting a
  block of the induced partition, with `m > n_data`, and **no `NewDatum` item
  anywhere in the delta**.
* **LIM-G GROWTH WITHOUT END.** `LIM-G` holds when an admitted reader whose
  selection is fixed at stage 0 (**no `AddContext` at any later stage**)
  separates every pair of admitted data at every stage of a declared growth
  run that reaches a carrier larger than `2^w_max`.
* **LIM-F THE FAMILY-DETERMINED VERDICT.** A reader's family verdict at the
  designated pair is a total function `F` of the **finite** verdict sequence
  `(v_0..v_H)`. `LIM-F` holds when some admitted object realises an `F` that
  is **stable** (`F(v_0..v_H) = F(v_0..v_k)` for every `k` in the declared
  window) and **novel** (`F(v_0..v_H) != v_k` for every `k <= H`).

The two limit directions are kept apart **mechanically, not by prose**: LIM-R
varies the questions with the carrier fixed and asserts that no `NewDatum`
item occurs; LIM-G varies the carrier with the selection fixed and asserts
that no `AddContext` occurs after stage 0. Both assertions are tests.

**No union, completion, or object over a family is formed anywhere.** The
phrase "the family" denotes nothing in this tree; only "the family up to `k`"
does, following CL-DI-TERMINATION, which states outright that its construction
is a pointwise successor-step family and **not** a formal trace object.

**Declared narrowing, recorded here rather than discovered later.** The growth
run of LIM-G is *this rung's own* declared run — one admission per stage — and
is **not** the sealed continuation policy (`closure_challenge_orbits` with the
retained minimum and the 1200-node guard). Reproducing that policy would
require re-implementing the sealed engine, which this tree does not do. LIM-G's
result is therefore scoped to the declared run and says so wherever it is
reported.

## 7. Population and quotient

* `P0` — the two sealed Challenge-3 bases. **Both have zero forms, hence zero
  contexts.** Every observation-grammar question is *vacuous* at them, so they
  carry the calibration and no observation finding whatever.
* `P1` — the states reachable from `P0` by at most three sealed one-item moves
  under the sealed `Bounds(2, 2)`, quotiented. Recomputed here, never trusted.

**Quotient.** The canonical key of a stated state is the minimum
serialization of `(r, Rho)` over **all** bijection pairs on data and forms —
the brute-force minimum, which is available because the population's regimes
are small, and which is asserted by test to induce the same equality relation
as the sealed refined `canonical` over the whole population. Each reader is
serialized as its reading class, aggregation table, and sorted transported
selection; the reader tuple is sorted. Ties are grouped on the **resulting**
stated state, reproducing the sealed `_quotient`. Every tied non-isomorphic
minimum is retained unless eliminated by proof.

## 8. The comparison, which is the deliverable

One table: rows are demands; columns are `mu1`, `mu2`, class count, grade
(`UniqueDelta` / `UniqueClass` / `Tie`), capability vector, and base. Then
three derived answers, each decided by an implemented algorithm and **none**
inferred from equal cost, which is exactly the inference a shared measure
invites:

1. **purchase** — run each demand's predicate on the other's retained minima,
   both directions;
2. **special case** — containment of the two canonical key sets, both
   directions;
3. **joint minimality** — whether any single delta is minimal for both.

Demands are additionally flagged by **evidence arity**, and the flag is
preserved in the report: the OBS ladder is decided **at a single state**,
LIM-R over a chain at a fixed state, LIM-G and LIM-F **on a run**. A candidate
answering demands of different arity is answering different kinds of question,
and that is a finding rather than a coincidence to smooth over.

## 9. Outcomes

Exactly three, distinguished, for each requirement:

* **PRICE** — with its minima, ties and capability counts.
* **PROVED OBSTRUCTION** — the requirement cannot be met from within the
  declared space, with the proof, together with the price of the smallest
  admission that would change that. Where no admission in the declared item
  alphabet lifts it, that is stated and the capability a lifting item would
  have to carry is **named**, rather than a number being invented.
* **OPEN** — with the exact boundary of what was searched and what was not.

Every reported obstruction requires a **positive control**: an exhibited
object showing the demand's tests can be passed at all. Without its control,
an empty minimum set is reported **OPEN**, never as an obstruction.

## 10. Evidence labelling

Every inherited claim is marked **CHECKED** (confirmed in the gated
`artifacts/lean_axioms.txt`) or **CITED** (a research tree's manual receipt,
read by no gate). No research tree's `verify_lean.py` is run by any gate;
`CLAUDE.md` records this as the last live residual, and this tree's own Lean
receipt is in exactly that position.
