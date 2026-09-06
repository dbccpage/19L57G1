# Status: the side-free control

One rung, one requirement, two carriers, one enumerator.  What follows is
what the machine returned, scored against predictions frozen before any code
of this tree existed.

## The order of the work, which is the evidence

1. `DESIGN.md` and `PREDICTIONS.md` were committed **alone**, before any code
   existed, in the commit whose message is
   *side_free: freeze the design and predictions before any code*.
   * `DESIGN.md` sha256
     `7cd9d5487614e6b542a53371f10f19a1daa2ace7447c5132695b6f1ce4a0880e`
   * `PREDICTIONS.md` sha256
     `24d6bdf5a6a7be653f1dd49d316457e92c43bfe58cebd2cc7a96149e1f517049`
2. Both digests are pinned in `verify_pins.py`, which checks them in the
   working tree, the index, `HEAD`, and every commit that touched the path.
   Neither file has been edited since.
3. Everything else — the kernel, the mirror, the enumerator, the gates, the
   Lean package, the receipt — arrived in the build commit that followed.

## The answer

All six gates passed; the record is not VOID.

| field | value |
|---|---|
| side-free minimum cost to meet the requirement, under `mu1` | **1** |
| tied non-isomorphic minima | **1**, and `unique` is true |
| the one minimum | `withdraw_mark_permutations` |
| does the withdrawal of the mark permutations port at the same cost | **yes** — `mu1 = 1` in both worlds, the capability sentence byte-identical, and it satisfies in both |
| unnamed-reading minimum (from the pin, reproduced by the mirror) | 1, in 3 tied classes |
| named-reading minimum | 0, in 1 class |
| `delta_vs_unnamed` | **0** |
| `delta_vs_named` | **+1** |
| `plurality_vs_unnamed` (its own column, never summed with price) | −2 |
| routes the admitted primitive bought | **2**: `withdraw_reflection` and `extra_mark`, both mediated by the sides |
| `what_the_admitted_primitive_bought` | **NOTHING_IN_COST** |

The two price lists agree at `base`, `withdraw_mark_permutations` and
`keep_labels`, and disagree at exactly **one** cell, `extra_mark`: the further
mark separates the two retained marks in the pinned world because the two
sides then carry different numbers of marks, and there are no sides here to
count.  That is the whole of the disagreement **inside the joined route
table**, and it is not the whole of what the admitted primitive bought.  The
second route it bought, `withdraw_reflection`, is outside the join altogether:
the mechanical deletion criterion drops it because its capability sentence
names the sides, so it is filed under `unmatched_pinned_routes` and can
disagree in no cell.  The receipt's `routes_bought_count` is **2**, and the
table above says so.

## The terminal sentence, and its scope

> Within the three declared coordinates, at the pinned requirement and prices,
> at the retained two-mark configuration, under `mu1`: the admitted primitive
> reduced the price of the required internal separation by ZERO under the
> unnamed reading and by ONE under the named reading.  What it bought under
> the unnamed reading is two additional routes at the same price, both
> mediated by the sides.  **It bought no price that the admission order could
> not buy at the same price.**

That last clause is the whole of the honesty here.  The tie holds only because
a route that satisfies the requirement without reading anything is counted —
`withdraw_mark_permutations`, which satisfies **by unfolding** and whose
`no_permitted_renaming_moves_an_index` flag the receipt computes and reports.
The pinned tree retains that route and records as OPEN whether the requirement
should have been declared so as to exclude it.  This control inherits that as
OPEN too, counts the route in the primary answer, and freezes the secondary
answer that excludes it.

**The residue this tree ends on:** what pays for separation in a world with no
container is the ADMISSION ORDER, and whether an order is itself a container
is a further question this control does not answer.

## The frozen predictions, scored

All 27 HIT; 0 MISS.  Four are labelled FORCED — fixed by a declaration of this
tree and true by unfolding it — and their hits are not counted as content.  A
fifth, P24, carries the label `NOT FORCED` in the frozen file and is FORCED in
fact; the mislabel is recorded in the notes below and its hit is not counted as
content either.

| id | label | what it said | status |
|---|---|---|---|
| P1 | NOT FORCED | side-free minimum 1 | HIT |
| P2 | NOT FORCED | 1 tied class, unique | HIT |
| P3 | NOT FORCED | the withdrawal ports at the same cost | HIT |
| P4 | NOT FORCED | delta 0 and +1, one disagreeing cell, NOTHING_IN_COST | HIT |
| P5 | NOT FORCED | base: mu1 0, 2 automorphisms, fails | HIT |
| P6 | NOT FORCED | keep_labels: mu1 1, 2 automorphisms, fails | HIT |
| P7 | NOT FORCED | extra_mark: mu1 1, 6 automorphisms, fails | HIT |
| P8 | FORCED | withdraw_mark_permutations: mu1 1, 1 automorphism, satisfies | HIT |
| P9 | FORCED | 8 points, 3 one-step, 4 refused bundles | HIT |
| P10 | NOT FORCED | class counts 1 against 3 | HIT |
| P11 | NOT FORCED | exactly 2 routes bought, and which | HIT |
| P12 | NOT FORCED | side-free `mu2` by row: 0, 1, 0, 0 | HIT |
| P13 | NOT FORCED | `mu2_restricted` minimum 0 in all three columns | HIT |
| P14 | NOT FORCED | the two transferring collateral facts, per row | HIT |
| P15 | NOT FORCED | 64/64 against 28/64; 8/8 against 2/8 | HIT |
| P16 | FORCED | 0 lemma violations, 0 corollary violations | HIT |
| P17 | NOT FORCED | 2140 automorphisms checked, 228 cells where the side-typed world separates and the side-free does not | HIT; the frozen file's LABEL for the second number is corrected in the note below |
| P18 | NOT FORCED | the injection gives 12 violations, first at U/("a","a")/(0,1)/(reflected,[1,0]) | HIT |
| P19 | NOT FORCED | the residue judgment separates nothing | HIT |
| P20 | NOT FORCED | G4 agrees on all fourteen rows | HIT |
| P21 | NOT FORCED | the mirror reproduces the pinned vector | HIT |
| P22 | NOT FORCED | the four numeric endowment rows | HIT; one of the ledger cells it reads is a declaration of this tree and not a measurement, see the note below |
| P23 | NOT FORCED | the shared policy retains one mark; the subject is refused | HIT |
| P24 | NOT FORCED in the frozen file; FORCED in fact, see the note | key-choice invariance at all eight points | HIT, and not counted as content |
| P25 | NOT FORCED | the secondary flips to NO_SATISFYING_CANDIDATE | HIT |
| P26 | NOT FORCED | the decided value is NOTHING_IN_COST | HIT |
| P27 | FORCED | the terminal sentence keeps its scope clause | HIT |

**Six notes on the scoring, recorded because a clean sweep invites suspicion.**

* P17 and P18 depend on the declared census domain and its declared iteration
  order, both fixed in `DESIGN.md` §11 before any code existed.  They are hits
  of a real computation against a number written down in advance, and the
  computation reproduced 2140, 228 and 12 exactly, with the injection's first
  violating cell matching the frozen one field for field.  If the domain had
  been implemented differently the counts would have moved and the misses
  would stand here.
* P27's falsifier as written in the frozen file — "the unscoped sentence
  appearing anywhere in this tree" — is **not implementable as a literal
  scan**, because `DESIGN.md` quotes the forbidden sentence in order to forbid
  it, and `DESIGN.md` may not be edited.  What is scored instead is that
  `terminal.sentence` carries the scope clause and does not carry the
  forbidden phrase.  The weaker check is recorded here rather than passed off
  as the frozen one.
* P24 is labelled `NOT FORCED` in the frozen file, and the label is **wrong**:
  it is true by unfolding the declarations, so its hit is not content.  The
  renaming function permutes indices and never changes the mark count, and the
  two declared key choices return the mark count or the empty tuple; so at
  every regime both choices are constant across the permuted images and admit
  exactly the same automorphisms, and at the four points that keep the labels
  the choice is not consulted at all.  The invariance table therefore cannot
  disagree with itself, and a check that cannot fail is not backing.
  `DESIGN.md` §12 cites it as backing for the guard against "order or index
  quietly made free content"; what carries that guard is the rest of that
  row — the admission index costs one capability here exactly as it does in
  the pinned world, and both worlds get the arity free — and not this test.
  The frozen file is not edited and the machine still reports the label the
  frozen file gives, so the correction lives here, as P27's weaker check does.
  The carrier module's comment on the same choice said it "errs AGAINST this
  control", and so did the sentence the RECORD carries at
  `key_choice_invariance.why_the_arity_is_declared`; within the only pair
  either of them declares, the arity key is the richer and so the more generous
  of the two.  Both now say so, and both attribute the "errs against" scope to
  the frozen design, which compares the arity key with richer keys that this
  pair does not contain.  The first repair reached the comment alone and left
  the record — the copy a reader cites — carrying the reversed sign for one
  commit; that is recorded here rather than smoothed.
* **P4's frozen sentence carries an aside the machine does not score, and this
  page had copied it.**  What P4 is scored on is four clauses: the two deltas,
  the decided value, and `route_disagreements == ["extra_mark"]`.  The frozen
  file adds, beside them, that the one disagreeing cell "is the whole of what
  the admitted primitive bought at this rung" — a sentence no clause holds, and
  a sentence that is wrong in the direction that flatters: the primitive bought
  two routes, and the second, `withdraw_reflection`, is dropped by the
  mechanical criterion before the join and so can disagree in no cell at all.
  The frozen file is not edited.  The copy that had reached this page's own
  answer section is narrowed above, and P4's hit stands on the four clauses it
  is scored on.
* **P17's second number is labelled wrong in the frozen file, and the machine
  now says what it measures.**  The frozen sentence DESCRIBES the count exactly
  — cells at two or more marks where the side-typed world separates the two
  retained marks and the side-free world does not — and then calls it "the
  lemma's non-vacuity".  It is not: the corollary says side-free separation
  implies side-typed separation, so at every one of those 228 cells the
  antecedent FAILS and the implication asserts nothing.  The count that shows
  the implication is not empty is the one nothing reported — the cells where
  the side-free world separates — and it is **800** of the 1280 cells of two or
  more marks.  The corollary really is non-vacuous, then, but the evidence
  cited for it measured a different property: that forgetting genuinely loses
  separations, and that the converse fails.  Both counts are now computed and
  reported under their own names, `corollary_antecedent_cells` and
  `converse_failure_cells`, and gate G5 names whichever it caught rather than
  calling either failure a vacuous corollary.  P17's clauses follow the frozen
  file's description to the renamed field; both counts are unchanged and it
  remains a HIT.  `DESIGN.md` §11 declares the check under the same mislabel
  and is frozen, so the correction is recorded here and beside
  SF-FORGETFUL-LEMMA in the ledger, as P24's and P27's are.
* **The cells the ledger lists under `declared_cells` are DECLARED by this
  tree and not computed, and P22 reads one of them.**  `DESIGN.md` §1 files
  every endowment row under deterministic computation, and §8 says every row
  is computed by the same code in each column.  That is true of the rows
  outside `rows_with_a_declared_column` and of the cells under
  `computed_cells`, and false of the cells under `declared_cells` — which are
  four, spread across those two rows, so the row count and the cell count are
  different numbers and an earlier draft of this note reported the first under
  the second's name.  The whole `declarations_at_genesis` row is three prose
  lists — nothing in either carrier enumerates its own genesis declaration, so
  those three cells are statements ABOUT the carriers and not readings taken
  off them — and the CONTROL cell of `coordinates the genesis declaration
  fixes` is a typed zero, because this control has no reading level to declare
  at and so has nothing to compare against its inherited defaults, while the
  two reading cells beside it really are computed.  All four are flagged in
  the record: every ledger row carries a `declared_columns` field, the rows
  carrying one are listed under `rows_with_a_declared_column` and the cells
  themselves under `declared_cells`, and each row says why — the instrument
  `comparison.py` already uses to keep a `Declared` cell apart from a
  `Computed` one, so that a typed-in value is not read as a measurement.
  P22's own population is computed too, beside its score at `ledger_cells`:
  twelve clauses over NINE cells, since the three cells of the renaming row
  are objects and two clauses read each of them.  Exactly one of the nine, the
  control zero of its first row, is in `declared_cells`, and that clause is an
  agreement true by unfolding a declaration; the other eight are in
  `computed_cells`, and the hit stands on them.  The frozen file is not edited
  and the correction lives here and beside SF-FAIRNESS-SIGN in the ledger, as
  P17's and P24's do.

## The price list

`receipts/comparison.json` and the document it renders, `COMPARISON.md`, put
the two worlds side by side item by item. Pinned-path boundary numbers are
READ from the four pinned receipts at `6c80c7ae43a704dcf9f109146cc6cf77139ed18e`. Other sources are named by cell path
and role in `boundary_source_census`: R03's boundary price cells read this
tree's endowment ledger; R40's boundary value cells are minima of the
restricted second measure, which no pinned path carries and
which are computed on this tree's own mirror and held by the per-point data
join against the pin instead. The former claim that R40 was the only
exception is WITHDRAWN: the census then omitted price columns. Every control
number is read from this tree's own record or computed from its carrier by
replay from genesis, and no
boundary number is typed into any source file of this tree.

| what the comparison found | value |
|---|---|
| items compared | **47**, across genesis, one admitted mark, two retained marks, the requirement, and the prices |
| the control reaches the unnamed reading's value at its price | **26** items |
| the control differs | **19** items |
| no statement in one world, so evidence for neither | **2** items: the collapse of the two sides at genesis, and the refusal of an admission that would move a mark |
| restricted to items that are verdicts or prices | same in **9**, differs in **7** |
| setting aside the two rows that read a field one world DECLARES rather than computes — R44, and R45, which is declared on BOTH sides and so DEFINITION-level | same in **25**, differs in **18**; restricted to verdicts and prices, same in **8**, differs in **6** |
| the pinned world's own dependence claims, now read | **20** entries: 5 dependent, 14 independent, 1 mixed, 0 unclassified |
| universal dependence claims selected mechanically | **1**, and it is **CONTRADICTED** within the declared scope |

Two findings the price list adds that the control alone did not carry.

* **The two criteria for "reads a side" disagree, and the record says where.**
  By NAME, a minimum reads a side when its pinned capability sentence carries
  the whole word *side* or *sides* — the deletion criterion run backwards.  By
  BEHAVIOUR, a minimum reads the placement when its separation verdict is not
  constant across the placements of one label configuration in its own
  route-census domain.  The two agree that `withdraw_mark_permutations` reads
  nothing and that `withdraw_reflection` reads a side.  They disagree on
  `extra_mark_0`, `extra_mark_1` and on the named reading's `base`: none of
  those names a side, and all three READ the placement.  The further mark
  separates because the two sides then carry different numbers of marks, and
  the named reading's zero-cost minimum reads the placement while naming no
  coordinate at all.
* **The pinned dependence dictionary is read for the first time.**  Its 20
  entries are classified by their own opening words, the classification is
  total, and the one entry whose subject claims *every* separation result of
  its rung requires the admitted primitive is contradicted by the computed
  evidence: `withdraw_mark_permutations` is one of that rung's own retained
  minima, its capability sentence is byte-identical here, it costs 1 in both
  worlds, and it satisfies in both.  The selector is declared; the evidence
  under it is computed; the contradiction is of that one universal clause and
  of nothing else in the dictionary.
* **Where that dictionary lives, corrected.**  This tree described it as "hand
  written in its runner modules" and "read by no test", and both halves were
  wrong.  The constant is defined in the pinned tree's four challenge modules,
  which its runners import; and a test there asserts that the receipt's copy
  equals the module constant, so its bytes are pinned.  What is exactly true —
  and what this tree now says, in the record, in the rendered document and in
  the ledger — is that nothing COMPUTES the dictionary, its own ledger filing
  it as a classification reported and not computed, and that nothing
  ADJUDICATES it.  `DESIGN.md` is frozen and carries the looser wording, so
  the correction is recorded rather than edited into it.

## Residuals, open and not closed

* **(a) Whether the admission order is itself a container.**  What pays for
  separation in a world with no container is that order.  This control prices
  the route; it does not decide what kind of thing an order is.
* **(b) The price of re-purchasing a per-mark two-valued datum.**  It lies
  outside the pinned candidate space and is therefore priced in neither world.
  Allowing it would price a route the pinned world was never charged for
  either, and it answers a different question — the PRICE of rebuilding the
  admitted primitive, not the WORTH of having it free.
* **(c) The pinned premise** that a candidate's permitted renamings are closed
  under composition and inverse is inherited as OPEN, and is not treated as
  discharged by the renaming set having shrunk.
* **(d) Whether the requirement should have been declared** so as to exclude a
  route that satisfies it by unfolding.  Inherited as OPEN.
* **The Lean package is a manual receipt.**  No CI job builds it, so its
  35 axiom reports are unchecked by any gate.  A live residual.
* **The pinned source has landed.** `verify_pins.py` requires its exact
  commit, source bytes and ancestry to `HEAD`; no CI downgrade remains.
  The fresh-receipt comparison is unconditional.
* **G4's scope** is the fourteen rows the minimum ranges over, not all 48
  points per reading.
* **The control is one rung wide.**  It says nothing about what the admitted
  primitive bought at earlier rungs, nor about whether the requirement was the
  right one to impose.  The price list widens the COMPARISON to the pinned
  rungs 0 to 2, but the requirement and its price are still priced at one rung
  only, and the verdict says so.
* **(e) `receipts/side_free.json` is not the same file in every clone.**
  The frozen conditional source-check field remains. Missing source may
  change diagnostic bytes, so clone independence is not claimed for this
  record. The CI loophole is closed: the source pin names the landed merge,
  unavailable source fails the required verifier, and fresh receipt bytes
  are compared unconditionally. `receipts/comparison.json` retains its
  separately tested clone-independent rendering property.
* **The dependence adjudication is one clause wide.**  The selector that picks
  the universal claim is DECLARED; only the evidence under it is computed.
  The other 19 entries of the pinned dictionary are reproduced and classified,
  not adjudicated: they are prose, and no computation here decides them.

## What the machine reports beside the answer

The receipt carries, and the tests hold, all of the following: the full route
table with its one disagreement; the two unmatched pinned routes with their
removal arguments; the endowment ledger with every mismatching row named, the
one row this tree computes a price for carrying that price and the other five
listed by name as carrying none, and the mismatch the ledger calls UNMATCHABLE
named as such; both censuses; the deletion register with its 83 deleted and 36
narrowed names; the two identity policies replayed, with the shared one
reported as a REFUSAL OF THE SUBJECT and never as a false; the removed refusal
and its computed consequence; `mu2` per carrier with its non-comparability
declared in the same object as the numbers, and no cross-world `mu2`
difference field anywhere; `mu2_restricted` on both sides, the pinned side by
data join from the receipt; the key-choice invariance table;
and the declared secondary computation, which flips the answer to
`NO_SATISFYING_CANDIDATE` and never decides.

## Current verification inventory

Discovery and fresh receipt checks at the landed-source repin are listed
below. Full-suite, typing and Lean results are reported against the exact
reviewed revision in the pull request; discovery is not execution evidence.
The earlier full-battery transcript is historical, not evidence for this repin.

```
364 tests discovered
receipt ok: 552262 bytes, byte-identical
comparison ok: 156108 receipt bytes and 29457 document bytes, byte-identical
```
