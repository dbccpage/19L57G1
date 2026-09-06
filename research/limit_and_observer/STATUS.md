# research/limit_and_observer — status

What was run, what it cost, what missed, and what remains open.

AuthorityEffect: None.

## Order of the work, which is the evidence

1. `REQUIREMENTS.md` and `PREDICTIONS.md` were written and committed with only
   the package's transport `.gitattributes`, before any module of this tree
   existed, in commit
   `ef26fc9eb3676e8edd3f4319bfd698c8951e0aad`. Their sha256 values are pinned
   in `SOURCE_MANIFEST.json` and checked by `verify_pins.py` at that snapshot
   and at HEAD. Neither has been edited since.
2. Pins, kernel, price, proofs, prose, registration, injections.

The commit order is the evidence that the predictions were not written to fit
the answers. It can be checked with `git log --diff-filter=A` on those two
paths.

## Disclosure, repeated from the freeze

`PREDICTIONS.md` records in full which predictions were informed by
measurements taken **before** the freeze. Ten of the eighteen were, and each
says so and names the measurement. Presenting those as discoveries of the run
would have been the dishonest move available here, and the labels exist so
that it is not made.

## Predictions: the score

Scored mechanically by `run_price.py` and written into `receipts/price.json`
under `predictions`. Each row below is the frozen text against what the run
produced, and `verify_prose.py` fails if a row here disagrees with the score
in the receipt.

**Three of these scores used to read literals this same script had written.**
P-7, P-10 and P-12 compared `outcome` and escape flags that `run_price.py`
emitted as constants a few lines earlier, so they could not miss whatever the
run produced; the supporting evidence existed elsewhere and was not what those
three scores looked at. Every such field is now computed from the enumeration
and the censuses. P-14 had the neighbouring defect — it was scored on the
prefix *shape* alone while the isomorphism class counts its frozen text
asserts were computed nowhere — and now scores the shape and all four counts.
P-14 still holds. The width-only countermodel makes P-12 miss: a necessary
capacity bound is not an escape construction. Restoring the frozen reader
classes reaches the candidate-budget refusal; affected search-based scores
are now OPEN, not counterexamples. P-10's smallest-extension clause is also
untested, not a proved existence claim.

| id | frozen claim | outcome |
|---|---|---|
| P-1 | population 85; 243 moves, 0 violations, 65/178 | **MISS on the move counts** |
| P-2 | both sealed bases have zero contexts | **HIT** |
| P-3 | calibration reproduces sealed `challenge3` field by field | **HIT** |
| P-4 | 8 complement classes, 7 non-constant, 4 behaviours | **HIT** |
| P-5 | the sealed observer is the full `uncovered` reader | **HIT** |
| P-6 | lawful counts 2/3/4/4 at widths 1 to 4 | **HIT** |
| P-7 | LIM-F is a proved obstruction | **OPEN**: search refused; independent evidence below |
| P-8 | LIM-F's core implication is definition-level and labelled | **HIT** |
| P-9 | LIM-R obstructed; ceiling attained at 26; none above | **OPEN**: search refused; bounded census retained |
| P-10 | no finite delta lifts LIM-R; a smallest extension exists | first half **OPEN**, second half **OPEN** |
| P-11 | LIM-G obstructed at the derived threshold 8 | **OPEN**: search refused; capacity evidence retained |
| P-12 | refinement and growth do **not** cost the same | **MISS**: width alone supplies no guaranteed escape |
| P-13 | OBS-3 costs 5 in both readings | **HIT** |
| P-14 | minimum rival prefix is form + rule + instance; 6 raw in 3 classes in L, 12 in 3 in F | **HIT** |
| P-15 | the rival is derived, not admitted | **MISS at three data** |
| P-16 | OBS-1/2 at 3; OBS-4 above OBS-3; **8 in L, 7 in F** | **MISS on the values** |
| P-17 | the second observer is decisively cheaper | **OPEN**: comparison requires completed search outcomes |
| P-18 | neither purchases the other; refinement purchases growth | first half **HIT**, second half **UNTESTABLE** |

### The first miss, recorded next to its value

**P-1 predicted 243 quotiented moves, 65 enlarging and 178 unchanged. The
tree's own census reports 1067, 227 and 840.** The violation count — the
load-bearing half — is **0** as predicted, and the population is **85** as
predicted.

The cause is a definitional difference, identified and not papered over. The
pre-freeze measurement counted moves during three breadth rounds, expanding
only the frontier each round, so the states discovered at depth 3 were never
expanded. The census expands **all 85** states of the population and counts
every item offered at each. The census figure is the better-defined one — it
is a property of the population rather than of the order in which it was
discovered — but the prediction said 243 and 243 is not what the tree
computes.

`PREDICTIONS.md` is not edited. The scorer still encodes 243/65/178 and still
reports `false`, and a companion line
`P-1-population-and-violations` records that the population and the violation
count did hold.

### The second miss, recorded next to its value

**P-16 predicted OBS-4 at `mu1 = 8` in reading L and `7` in reading F. The
tree's own exhaustive enumeration gives `7` and `6`.** Both are one item lower
than predicted, in both readings.

The cause is identified and is not a defect in the tree: the pre-freeze
prototype that produced 8 and 7 generated reader suffixes more restrictively
than this tree's enumerator does — it required a particular split of context
items between the two readers and broke out of its search early, so it never
offered the cheapest coexisting pair. The prototype was wrong by exactly one
item, uniformly.

What P-16 got right is kept and what it got wrong is not quietly repaired:

* OBS-1 and OBS-2 at `mu1 = 3` — **hit**.
* OBS-4 strictly above OBS-3 — **hit** (7 above 5, and 6 above 5).
* The two readings **differ** at OBS-4 — **hit** (7 against 6).
* The exact values — **miss**.

`PREDICTIONS.md` is not edited. The frozen text still reads 8 and 7, the
scorer still encodes 8 and 7, and the scorer still reports `false`. That is
what a frozen prediction is for.

### A narrowing found by the tree's own test, not by a reader

**The first statement of the refinement proof was too strong.** It said that
every strict split raises the block count, for every lawful reader.
`test_a_strict_split_raises_the_block_count` failed with
`AssertionError: 1 not greater than or equal to 2`: under the **parity**
aggregation, adding a context can **lower** the block count, because two data
separated at one context are identified once a second context also tells them
apart.

Measured consequence: exactly **2 of the 4** lawful aggregations at width 3
are block-count monotone — the blind one and "at least one separating
context" — and the count is 2 at every width from 1 to 4. The block-count
**proof** therefore covers those two. For the other two the chain bound is a
**bounded computation** over the declared population, verified with 0 chains
above the ceiling, and is reported as a computation rather than a theorem.

The statement was narrowed in `FINDINGS.md`, `CLAIM_LEDGER.md` LO-09 and the
receipt, and the countermodel is kept as a test. Keeping the wording and
leaning on the green receipt was the other option available, and it is the one
the estate's claim hygiene exists to refuse.

### The third miss, and an untestable half

**P-15 predicted the rival would be DERIVED. It is derived at two admitted
data and ADMITTED at three.** At reading L's minimum rival state the sealed
relation is empty and the rival's relation is its complement, so it lies in
the declared combination set. At reading F's, the carrier is 3 and the rival
separates one datum from the other two — neither the sealed relation, nor its
complement, nor anything else one application of the declared set reaches.
The prediction is not edited; the scorer reports `false` and a companion line
`P-15-at-two-data-only` records the half that held.

**P-18's second half cannot be tested here and is not scored as a hit.** "No
observer demand purchases a limit demand" is checked and holds, 0 of 30. But
"refinement purchases growth" has nothing certified to run: L has completed
empty minima and F has refused, unknown minima. Neither supplies a minimum
delta to feed the other predicate; F supplies no complete key set to compare.
The receipt records
`P-18-refinement-purchases-growth-UNTESTED` as `false` rather than letting the
narrower test stand in for the whole prediction.

## Earlier battery record, before the eight-class repair

This table records the earlier run, not a fresh verification of the changed
candidate population. The isolated review results below supersede it where
source or receipts changed. In particular its receipt-determinism entry does
not establish a complete current price census.

| step | result |
|---|---|
| `verify_pins.py` | pins clean at the snapshot and at HEAD |
| `unittest discover -s tests` | all tests pass |
| `mypy` (strict) | clean |
| dual coverage gate | line and branch each at or above 95% |
| `run_price.py` | receipt regenerates byte-identically |
| `ci/check_prose_watchlist.py` | clean, **no pin regenerated** |
| `tests/test_primitive_contact.py` | vocabulary firewall clean |
| `verify_prose.py` | every explicitly bound published number matches the receipt |
| `verify_lean.py` | 21 axiom reports, all within `{propext, Quot.sound}` |

The exact commands live in `MANUAL.md`.

## Things found by the machinery rather than by reading

**The enumerator certification caught a real divergence.** The set-equality
check between `sealed_prefixes` (breadth over one-item moves) and the
independently written `superset_prefixes` failed at three items in reading L:
the superset admitted a delta containing `NewRuleAll(0)` **twice**, which
replays without complaint because admitting a rule is idempotent on the
regime, while the sealed offer condition never offers a rule for a form that
is already ruled.

Two repairs were available and they are not equivalent. Restating the sealed
offer condition exactly — which is what `admissible_shape` does — keeps the
space the sealed one. Widening the space to admit the doubled rule item would
have inflated every count in this tree by the size of a redundancy class while
leaving every gate green. The first was taken, and the condition carries the
incident in its docstring so that a later reader does not mistake it for a
convenience.

**The calibration caught the quotient being too coarse.** The first
calibration run reproduced the sealed costs and delta counts exactly but gave
3 isomorphism classes where reading F's `mu1` answer has 5. The sealed
`_quotient` imposes the target requirement on the child **before** taking the
canonical key, and a requirement constrains which bijections preserve the
structure. Carrying the imposed pair as a field of the demand — a parameter,
not a branch — reproduces the sealed grouping exactly.

Both are recorded here rather than only in a commit message, because both are
the kind of defect that passes every gate.

## Repairs after review, each with its reason

A review of the first commit of this tree found defects that every gate had
passed. They are listed here newest-last, with what changed and why. Nothing
frozen was restated: `REQUIREMENTS.md` and `PREDICTIONS.md` are byte-identical
to the freeze, mis-scored predictions are re-scored in the receipt and
recorded as misses, and every claim that rested on a question-begging step is
narrowed rather than kept with a receipt leaned on.

1. **`FINDINGS.md` published three refuted numbers as results.** The
   monotonicity census read 243/65/178 against the receipt's 1067/227/840; the
   price table and the divergence sentence read 8/7 for OBS-4 against the
   receipt's 7/6. In both cases the page printed the pre-freeze *prediction*
   in place of the computed value, in a page whose own preamble says it
   reports rather than computes, and in the section published so that no
   finding rests on an unchecked count. Corrected to the receipt's values,
   with the miss named and pointed at its record here. The predictions are not
   edited and the receipt still scores both false.
2. **`FINDINGS.md` asserted a containment the receipt does not hold.**
   "Refinement purchases growth" was written as the one containment that does
   hold, in a section claiming every answer is decided by an implemented
   algorithm. No such row exists: both limit demands have empty minima, so the
   purchase test has no delta to feed and the containment test no key set to
   compare, and the receipt already recorded
   `P-18-refinement-purchases-growth-UNTESTED` as false. The assertion is
   **WITHDRAWN** and replaced by the untested finding; "in both directions" is
   narrowed to the direction that ran.
3. **The Lean refinement theorems were vacuous.** `chain_bounded`,
   `refinement_demand_unsatisfiable` and `refinement_obstruction_survives_growth`
   asked strictness at every index while bounding the block count at every
   index — jointly unsatisfiable, so no chain instantiated them and the chain
   length occurred in no hypothesis. LO-09 and LO-10 rested on exactly those
   names. Reproved with the hypotheses bounded by the chain, which is what a
   finite chain supplies, and `chain_bound_has_an_instance` now exhibits an
   instance so the vacuity cannot return unnoticed. The axiom receipt could
   not have caught this: it reports which axioms a proof used, never whether
   its hypotheses can be met.
4. **`cost_below_minimum_all_fail` was a hard-coded `True`.** It is declared
   in `REQUIREMENTS.md` as decided by exhaustion and never by assertion, and
   was written as a literal in both branches of the assembly — correct only by
   the accident that the walk ascends, with no test able to catch a
   reordering. It is now computed by `below_minimum_exhausted` from the item
   counts the walk exhausted, and `tests/test_price.py` requires it to be
   false for a walk that did not exhaust them. Every receipt value is
   unchanged.
5. **Three predictions were scored against literals this script wrote.** P-7,
   P-10 and P-12 read `outcome` and escape flags that `run_price.py` emitted
   as constants ten lines earlier, so they could not miss whatever the run
   produced. Each is now computed: an outcome is `PROVED OBSTRUCTION` only
   when the enumeration is empty **and** the positive control passes, which is
   `REQUIREMENTS.md` section 9 applied rather than restated, and each escape
   flag is computed from the censuses and the enumeration. All three still
   hold.
6. **P-14 was scored on a strictly weaker condition than its frozen text.**
   The shape alone was scored while the isomorphism class counts the
   prediction asserts — and `CLAIM_LEDGER.md` LO-06 and `FINDINGS.md` quote —
   were computed nowhere. `minimum_rival_prefix_census` now computes them: 6
   raw in 3 classes in reading L, 12 raw in 3 classes in reading F, matching
   what was quoted. P-14 is scored on the shape and all four counts and
   remains a hit.
7. **The projection test compared a value with itself.** Both sides of
   `test_projection_commutes_with_every_sealed_event` were built from a state
   with an empty reader tuple, so removing readers from `apply_delta` entirely
   would not have failed it, while `REQUIREMENTS.md` and the `StatedState`
   docstring cite it as the assertion that the projection commutes. The
   left-hand state now carries a reader, and a second test carries a reader
   with a non-empty selection over a regime that has contexts.
8. **The inert-context pruning claimed more than its argument covers.** The
   lemma shows the pruning sound for a predicate that is a function of the
   induced relations; OBS-4 reads the two readers' **selections**, so it is
   not covered, and the cross-check ran only OBS-1 and OBS-2 at a bound too
   tight for OBS-3 to be answered inside it. The docstring is narrowed, the
   separate width argument that covers OBS-4 at these bounds is recorded with
   its own test, the cross-check now runs every demand at a bound where OBS-3
   is answered, and OBS-4 is compared pruned against unpruned where it is
   answered.
9. **LIM-G's empty price row was not disclosed as an artefact of the item
   bound.** The demand needs a carrier above 8 and the declared space reaches
   6 and 7, so every candidate is rejected at the carrier test before a reader
   is examined and the empty row carries no information about readers. The
   receipt now records the reach, and the carrier-9 exhibit — eight sealed
   items, twice the declared bound — is named as an out-of-space positive
   control rather than left only in a test. LIM-R's reach is recorded beside
   it and is **not** zero: the width bound alone leaves the demand open at 24
   of the 85 states, and at those the chain bound rather than the item bound
   is what rules it out.
10. **The Lean axiom report claimed a population it did not cover.** Its
    header read "every exported theorem" while `separatesAt_eq_readsAt` had no
    report and nothing checked the population — the shape of overclaim
    `CLAUDE.md` withdrew for the sealed audit. The hand-written list is
    replaced by a census read out of the compiled environment, and
    `verify_lean.py` additionally refuses a module outside the census root's
    import closure, which is the half Lean cannot see. The receipt went from
    17 reports to 21: the missing one, the new witness, and two equation
    lemmas Lean generates.
11. **No gate bound the published prose to the receipt**, which is why the
    three divergences in item 1 survived every green run. `verify_prose.py`
    now binds each published number to the receipt value it claims to report
    and fails naming the file, the line, and both values. It is registered in
    the research job and its injections are in `MANUAL.md`.
12. **The line anchor for the one pinned fact was wrong in four files.**
    `derivable` is at line **52** of `code/derivation/observe.py`, not 56;
    line 56 is `profile`. The quoted body was always right, the blob pin
    verifies, and only the anchor was wrong. Corrected in `FINDINGS.md`,
    `code/grammar.py`, `lean/LimitObserver.lean` and `SOURCE_MANIFEST.json`.
    **`REQUIREMENTS.md` is frozen and still says 56**; that is what a frozen
    input is for, and the correction is recorded here instead.

## Deviations from the design, declared

* **LIM-G's run is this rung's own declared statement, at the state level, and
  is not the sealed continuation policy.** The design called for the sealed
  policy with its demand generator, retained minimum and node guard.
  Reproducing it would require re-implementing the sealed engine, which this
  tree does not do. The state-level statement is equivalent to the run-level
  one *for every run*, by the signature argument, and that is why the
  substitution costs nothing — but it is a substitution and it is declared.
* **Depth 4 was not reached.** The design named it as where the finding becomes
  robust rather than merely non-vacuous. It is recorded OPEN with the exact
  boundary, and the depth-3 price is reported as the depth-3 price.
* **The `2 ** w` growth threshold has no Lean proof.** Lean proves the growth
  obstruction with an explicit witness for growth by uninstantiated data; the
  sharper threshold needs a pigeonhole over signatures and is checked
  exhaustively in Python instead. Recorded OPEN rather than claimed.
* **The frozen reading-class quotient is restored.** The earlier behavior
  collapse proved only equality of induced relations, not full reader
  transport. In OBS-4, equal behaviors with distinct complement classes can
  change the non-automorphism verdict. All eight complement classes are now
  enumerated and retained in canonical keys and OBS-4 transport. The four
  behavior classes remain a theorem about relations, not reader identity.
* **All nine declared capability fields are now computed.** The missing
  `reading_class` and `aggregation_lawful` fields are per-reader lists of
  Boolean tables and lawfulness results. They are not scalar cost coordinates;
  adding them changes neither cost measure nor the isomorphism quotient.
  The prior seven-field shortfall is repaired without an invented weighting.
* **This tree imports nothing across trees.** The design called for importing
  the sealed `mu1` and `mu2` and asserting object identity. The order of the
  work forbids importing across trees, so the measures are re-implemented
  against a pinned source and asserted equal to the sealed originals **on the
  whole enumerated space**, with the sealed modules loaded only inside a test
  that refuses to run against unpinned bytes. That is a stronger check than
  identity on a handful of cases and a weaker one than sharing the object; the
  difference is stated rather than glossed.

## Open, with the exact boundary

1. **Depth 4 of the population.** 85 quotiented states at depth 3; a rival
   appears at 6 of them. Not reached within the declared budget.
2. **The `2 ** w` threshold in Lean.** Needs a pigeonhole over signatures,
   which core Lean without Mathlib does not supply. Checked exhaustively in
   Python at widths 1 to 3, and by an exhibited carrier above the threshold.
3. **`w_max` above 4.** Lawfulness was measured at widths 1 to 4 and is not
   stable in the width (2 of 2, 3 of 4, 4 of 8, 4 of 16). Nothing is claimed
   beyond 4.
4. **`max_readers` above 2.** Three or more coexisting readers are outside the
   declared space.
5. **The estate's open bridge is not discharged.** The rival priced here is
   inside by construction and is not the outside reader `OPEN_BRIDGES` names.
   That obligation is inherited unchanged.
6. **This tree's Lean axioms are ungated.** No CI gate runs this package's
   `verify_lean.py`; this is a package-specific statement.
7. **LIM-G's demand is unreachable in the declared candidate space.** It needs
   a carrier above `2 ** w_max = 8`; `max_sealed_items` is 4 and the genesis
   carriers are 2 and 3, so the largest carrier reached is 6 in reading L and
   7 in reading F. The completed L empty price row therefore carries no
   information about readers. F's refused search does not certify an empty
   minimum set; the carrier bound is not an enumeration-completion receipt.
   The obstruction rests on
   the signature argument, the capacity census and an out-of-space carrier-9
   exhibit; pricing the demand inside a space that reaches its threshold is
   OPEN and would need `max_sealed_items` above 6.
8. **LIM-R's demand is reachable at 24 of the 85 states, not all of them.** A
   chain longer than the carrier needs a width above the carrier, and
   `w_max = 3` allows that only at carriers below 3. At the other 61 states
   the width bound alone rules out the demand. The proof and the chain
   census cover all of them; the F price search remains refused, and the difference is
   recorded rather than left for a reader to derive.
9. **Four-item prefix certification is now checked at both genesis bases.**
   The independent grouped construction in `tests/test_prefix_certificate.py`
   widens coordinate pools before replay filtering and compares exact
   delta-to-child maps through counts 0–4. Counts are 1, 3, 14, 67, 333 in L
   and 1, 3, 20, 137, 934 in F. This uses shared replay semantics and does
   not close the separate depth-4 population or semantic-correspondence gaps.
10. **Escape feasibility and pricing.** LIM-R's bound implies that an escape
    must leave the declared space; it constructs no seventh item and proves
    no smallest extension. Those claims remain OPEN. For LIM-G, necessary
    width is not sufficient when all raw
    signatures coincide. The former one-item price is withdrawn, its price
    fields are null, and a countermodel now makes P-12 a MISS.

## Classification of every notion this tree introduces

| notion | class |
|---|---|
| the reader triple, and its two admission events | admitted primitive |
| the widened item bound above the sealed two | admitted primitive |
| the growth statement of LIM-G | admitted primitive (declared here) |
| `Regime`, events, replay, contexts, the two bits | metatheory apparatus |
| the induced separation relation; the behaviour of a reading | derived definition |
| the eight demands | imposed challenge |
| `chain_bounded`, `growth_defeats_every_reader`, `novel_forces_constant`, the behaviour collapse | proved theorem |
| every census, every price, every comparison row | deterministic computation |
| the blind reader; the doubled-rule delta; the parity aggregation lowering the block count | countermodel |
| the `2 ** w` threshold in Lean | open obstruction |
| depth 4; widths above 4; three or more readers | open obstruction |
| P-16's exact OBS-4 values; P-1's move counts; P-15's blanket DERIVED | refuted claim |
| "every strict split raises the block count for every lawful reader" | refuted claim |
| "refinement purchases growth", as a holding containment | refuted claim |
| the first, vacuous form of `chain_bounded` and its two corollaries | refuted claim |
| "every exported theorem has an axiom report", as first written | refuted claim |
| the inert-context lemma as sound for every demand | refuted claim |

## Review correction: observation is a projection, not a state conflation

The active LO-01 statement and findings now distinguish information lost by
the sealed observation from information retained in admitted state. The
state stores instances and uniform rules separately, with separate admission
events; positive derivability is explicitly their disjunction. Its covered
contexts erase admission variation, but that does not establish a breach of
the assumption discipline. No exhaustive estate-wide interface census was
performed here. The original frozen wording is unchanged and is not evidence
for that wider claim. The alternative reader remains an admitted primitive.

The covered and uncovered behaviours have complementary sensitivity to
admission. This is not pointwise negation of the sealed truth value, and it
does not assert complementary induced relations on every carrier.

## Review correction: declared reader transport and admission guards

OBS-4 originally compared selected contexts alone. Comparing every declared
reader field also exposed the behavior quotient as too coarse: at genesis F,
the two diagonal instances `(0,0)` and `(2,2)` under one binary form make the
corresponding selected contexts automorphism images, but readings `0101` and
`0110` have distinct complement classes. Both readers separate a pair and
disagree at `(0,1)`. The old predicate rejected this seven-item witness; the
frozen class-based predicate accepts it. This proves predicate drift, not a
lower minimum. Prices and tie counts are recomputed over all eight classes.

Replay now refuses unlawful or malformed readers, and exact field censuses
cover all six item kinds, including stage-bearing sealed items. The Lean
report parser preserves primed names and independently compares the emitted
declaration population against parsed reports. Import closure cannot silently
extend the theorem audit beyond its declared main-module domain. The gate
controls and their limits are recorded in `MANUAL.md`.

## Isolated eight-class review result

The review continued in an isolated worktree based on
`623704c67c43cf9407a529d812a5f5cd72ce6dd2`; the original shared worktree was
not used as a verification surface after another writer remained active.
The source and prediction freeze history is preserved. No sealed source or
frozen requirement/prediction bytes changed in this repair.

The actual replay over all eight reading classes completed the following
candidate levels; the counts belong to each reading and item level, shared
by all demands and both measures:

| item count | L completed candidates | F completed candidates |
|---|---:|---:|
| 0 | 1 | 1 |
| 1 | 35 | 35 |
| 2 | 638 | 644 |
| 3 | 2099 | 2361 |
| 4 | 10061 | 16262 |
| 5 | 57232 | 126240 |
| 6 | 280896 | 808464 |
| 7 | 707008 | 2808720 |
| 8 | 982608 | **REFUSED**, not a completed count |

L is COMPLETE within these declared levels. F yielded 4000000 candidates at
level 8, then refused ordinal 4000001. The receipt names its last yielded and
first refused deltas, with zero observed hits for each pending limit demand.
Zero in this observed prefix is not an empty minimum census. The six F limit
rows (three demands, two measures) are OPEN, have null cost/count fields,
`incomplete = true`, and `cost_below_minimum_all_fail = false`. Their unseen
suffix remains unexamined. The completed L limit rows remain certified empty
within their declared scope.

All five observer demands completed their lower and successful levels in both
readings. Their new minima and complete ties are retained, with class keys
using the frozen complement class, aggregation and transported selection.
OBS-3 still costs 5 in each reading; OBS-4 still costs 7 in L and 6 in F.
This does not retain the old four-behaviour tie census. Nor is the former
whole-space price/tie/containment census retained: F's incomplete minimum-set
comparisons are omitted and named OPEN, rather than treated as empty sets.
The 30 direct observer-to-limit purchase rows remain false; 15 mixed
containment rows use the completed L sets and the corresponding F rows are
omitted. The five unfinished prediction clauses are OPEN, not MISS solely
because the budget was exhausted. LIM-F's suggested outside-contract escape,
like LIM-R's extension, has no constructed minimum price.

Verification of the repaired measured core: all 191 tests in the full scoped
battery passed. After the final runner-only description/summary changes, all
16 focused regressions passed, including two new tests; current discovery is
193 tests. The refreshed independent coverage gate reports 1066/1078 lines
(98.89%) and 420/432 branches (97.22%), over 11 measured source files. Strict
typing passes for 16 source files. The clean Lean audit reports 21 allowed
reports, and the primed-name failure/recovery control is recorded above.

The full true-bound run wrote receipt SHA256
`f5e5e7004af1af09715b891400b9eeeae096989dc2c4bb2f92256d0d54584a19`.
A subsequent metadata-only rerender corrected two reach descriptions, removed
LIM-F's unsupported smallest-extension claim, and made refused relation-count
summaries null. Prices, searches, censuses, predictions, bounds, scope and
calibration were hash-checked unchanged together, using sorted-key JSON:
`955ed9099459ee6fd7c6a8f308ad2d465fe1b7f111887ed2aad9305e660de97e`.
The resulting receipt SHA256 is
`63f9070021f63ab64eb472e75b2eace0df911a467146602ae1706bcc20e605a5`.
Its serializer check passed and the 33 explicit prose bindings and prediction
table passed. No second expensive full search was run after this metadata-only
change; serialization identity is not presented as a second independent
search replay. No receipt was regenerated under a live injection.
