# research/limit_and_observer — status

What was run, what it cost, what missed, and what remains open.

AuthorityEffect: None.

## Order of the work, which is the evidence

1. `REQUIREMENTS.md` and `PREDICTIONS.md` were written and committed **alone**,
   before any module of this tree existed, in commit
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
produced.

| id | frozen claim | outcome |
|---|---|---|
| P-1 | population 85; 243 moves, 0 violations, 65/178 | **MISS on the move counts** |
| P-2 | both sealed bases have zero contexts | **HIT** |
| P-3 | calibration reproduces sealed `challenge3` field by field | **HIT** |
| P-4 | 8 complement classes, 7 non-constant, 4 behaviours | **HIT** |
| P-5 | the sealed observer is the full `uncovered` reader | **HIT** |
| P-6 | lawful counts 2/3/4/4 at widths 1 to 4 | **HIT** |
| P-7 | LIM-F is a proved obstruction | **HIT** |
| P-8 | LIM-F's core implication is definition-level and labelled | **HIT** |
| P-9 | LIM-R obstructed; ceiling attained at 26; none above | **HIT, narrowed** |
| P-10 | no finite delta over the six kinds lifts LIM-R | **HIT** |
| P-11 | LIM-G obstructed at the derived threshold 8 | **HIT** |
| P-12 | refinement and growth do **not** cost the same | **HIT** |
| P-13 | OBS-3 costs 5 in both readings | **HIT** |
| P-14 | every minimum rival prefix is form + rule + instance | **HIT** |
| P-15 | the rival is derived, not admitted | **MISS at three data** |
| P-16 | OBS-1/2 at 3; OBS-4 above OBS-3; **8 in L, 7 in F** | **MISS on the values** |
| P-17 | the second observer is decisively cheaper | **HIT** |
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

### The miss, recorded next to its value

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
"refinement purchases growth" has nothing to run: LIM-R and LIM-G both have
**empty** minima, so there is no delta to feed the other predicate and no key
set to compare. The receipt records
`P-18-refinement-purchases-growth-UNTESTED` as `false` rather than letting the
narrower test stand in for the whole prediction.

## What each battery step reported

| step | result |
|---|---|
| `verify_pins.py` | pins clean at the snapshot and at HEAD |
| `unittest discover -s tests` | all tests pass |
| `mypy` (strict) | clean |
| dual coverage gate | line and branch each at or above 95% |
| `run_price.py` | receipt regenerates byte-identically |
| `ci/check_prose_watchlist.py` | clean, **no pin regenerated** |
| `tests/test_primitive_contact.py` | vocabulary firewall clean |
| `verify_lean.py` | 17 axiom reports, all within `{propext, Quot.sound}` |

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
* **The reading axis is keyed by behaviour, not by complement class.** The
  design specified the complement class. The behaviour is coarser and the
  collapse is proved — `behaviour_determines_separation` in Lean, and
  `test_same_behaviour_gives_the_same_relation_at_every_state` over the whole
  population — so this is elimination by proof rather than by convenience.
  Both counts are reported.
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
6. **This tree's Lean axioms are ungated.** No CI gate runs any research tree's
   `verify_lean.py`. `CLAUDE.md` records that as the last live residual and
   this tree is inside it.

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
