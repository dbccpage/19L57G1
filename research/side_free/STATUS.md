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
count.  That single cell is the whole of what the admitted primitive bought at
this rung.

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
tree and true by unfolding it — and their hits are not counted as content.

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
| P17 | NOT FORCED | 2140 automorphisms checked, 228 non-vacuity cells | HIT |
| P18 | NOT FORCED | the injection gives 12 violations, first at U/("a","a")/(0,1)/(reflected,[1,0]) | HIT |
| P19 | NOT FORCED | the residue judgment separates nothing | HIT |
| P20 | NOT FORCED | G4 agrees on all fourteen rows | HIT |
| P21 | NOT FORCED | the mirror reproduces the pinned vector | HIT |
| P22 | NOT FORCED | the four numeric endowment rows | HIT |
| P23 | NOT FORCED | the shared policy retains one mark; the subject is refused | HIT |
| P24 | NOT FORCED | key-choice invariance at all eight points | HIT |
| P25 | NOT FORCED | the secondary flips to NO_SATISFYING_CANDIDATE | HIT |
| P26 | NOT FORCED | the decided value is NOTHING_IN_COST | HIT |
| P27 | FORCED | the terminal sentence keeps its scope clause | HIT |

**Two notes on the scoring, recorded because a clean sweep invites suspicion.**

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
* **The pinned commit is on an unmerged branch.**  `verify_pins.py` fails by
  default when it is unreachable; the CI step downgrades that to a reported
  SKIP.  In CI the vendored bytes are held by their three digests alone.
  Re-take the pin when that branch merges.
* **G4's scope** is the fourteen rows the minimum ranges over, not all 48
  points per reading.
* **The control is one rung wide.**  It says nothing about what the admitted
  primitive bought at earlier rungs, nor about whether the requirement was the
  right one to impose.

## What the machine reports beside the answer

The receipt carries, and the tests hold, all of the following: the full route
table with its one disagreement; the two unmatched pinned routes with their
removal arguments; the endowment ledger with every mismatching row named and
priced, including the two that are UNMATCHABLE; both censuses; the deletion
register with its 69 deleted and 36 narrowed names; the two identity policies
replayed, with the shared one reported as a REFUSAL OF THE SUBJECT and never
as a false; the removed refusal and its computed consequence; `mu2` per carrier
with its non-comparability declared in the same object as the numbers, and no
cross-world `mu2` difference field anywhere; `mu2_restricted` on both sides,
the pinned side by data join from the receipt; the key-choice invariance table;
and the declared secondary computation, which flips the answer to
`NO_SATISFYING_CANDIDATE` and never decides.

## Local battery, all green

```
234 tests, OK
line 100.00% branch 100.00% over 8 files
mypy: Success: no issues found in 20 source files
receipt ok: 541009 bytes, byte-identical
lean ok: 35 axiom reports within ['Quot.sound', 'propext']
pins ok: 2 frozen file(s), the vendored pin e4904075aaa0 at 220518 bytes
```
