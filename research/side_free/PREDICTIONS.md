# Frozen predictions

Frozen before any code of this tree existed, committed in the same commit as
`DESIGN.md` and ahead of every other file.  The sha256 of this file is pinned
in `verify_pins.py` in the build commit.  **This file is never edited.**  A
missed prediction is recorded next to its computed value in `STATUS.md`, with
the miss standing.

Each prediction carries a falsifier and one of two labels:

* **FORCED** — fixed by a declaration of this tree and true by unfolding it.
  A hit is not content.  A miss on a FORCED prediction is a defect in the
  implementation, not a discovery.
* **NOT FORCED** — a genuine computation whose value could come out otherwise.

Every value below is what the tree is expected to *recompute from scratch*.
None of it is read out of the pinned receipt except where a prediction says so.

---

## The four the caller named

**P1 — the side-free minimum cost to meet the requirement.**  `NOT FORCED`

`side_free_minimum = 1` under `mu1`, over the candidates that satisfy the
requirement and are base-or-one-step within the three declared coordinates.

*Falsifier:* any other value; in particular `0` (the base satisfying) or the
empty satisfying set (`NO_SATISFYING_CANDIDATE`).

**P2 — the number of tied non-isomorphic minima.**  `NOT FORCED`

`side_free_classes = 1`, and `unique` is `true`.  The single class is
`{withdraw_mark_permutations}`.

*Falsifier:* a class count above 1, or `unique` false, or a class whose
member set differs.

**P3 — whether the withdrawal of the mark permutations ports to this world at
the same cost.**  `NOT FORCED`

Yes.  It costs `mu1 = 1` in both worlds, it carries the same capability
sentence byte-identical, and it satisfies the requirement in both.  Its
side-free regime has exactly **1** automorphism.

*Falsifier:* a different `mu1` on either side; a capability text that is not
byte-identical; the coordinate failing to satisfy side-free; an automorphism
count other than 1.

**P4 — the difference between the two price lists.**  `NOT FORCED`

```
delta_vs_unnamed = side_free_minimum - unnamed_minimum = 1 - 1 =  0
delta_vs_named   = side_free_minimum - named_minimum   = 1 - 0 = +1
what_the_admitted_primitive_bought = NOTHING_IN_COST
```

The two price lists agree cell for cell at `base`,
`withdraw_mark_permutations` and `keep_labels`, and disagree at **exactly
one** cell, `extra_mark`.  That single cell is the whole of what the admitted
primitive bought at this rung: serialized content carried free from genesis.

*Falsifier:* `delta_vs_unnamed != 0`; `delta_vs_named != 1`; a number of
disagreeing cells other than one; a disagreeing cell other than `extra_mark`.

---

## The row vector

**P5 — `base`.**  `NOT FORCED`  `mu1 = 0`, **2** automorphisms, FAILS.

*Falsifier:* any other count or verdict.

**P6 — `keep_labels`.**  `NOT FORCED`  `mu1 = 1`, **2** automorphisms, FAILS.

*Falsifier:* any other count or verdict.  It fails because both retained marks
carry the same label, so keeping the labels distinguishes nothing.

**P7 — `extra_mark`.**  `NOT FORCED`  `mu1 = 1`, **6** automorphisms, FAILS.

*Falsifier:* any other count or verdict.  This is the cell the two worlds
disagree at: the further mark separates the two retained marks in the pinned
world because the two sides then carry different numbers of marks, and there
are no sides here to count.

**P8 — `withdraw_mark_permutations`.**  `FORCED`  `mu1 = 1`, **1**
automorphism, SATISFIES.

Definition-level: with no permitted renaming that moves an index, no renaming
carries one mark to another, so the requirement holds by unfolding.  The tree
computes it rather than asserting it, and reports
`no_permitted_renaming_moves_an_index` as a **computed** field beside it.

*Falsifier:* it failing, or an automorphism count other than 1 — either would
be an implementation defect, not a discovery.

**P9 — the four bundles.**  `FORCED`  Four of the eight points carry
`mu1 >= 2` and are refused as one-step augmentations; one is `base`; three are
one-step.

*Falsifier:* a space size other than 8, a one-step count other than 3, or a
refused-bundle count other than 4.

---

## Plurality, routes, and the second measure

**P10 — class counts.**  `NOT FORCED`  Control **1** against the unnamed
reading's **3**.  `plurality_vs_unnamed = -2`, reported in its own column and
**never summed with the price**.

*Falsifier:* either count differing; any receipt field combining plurality
with price.

**P11 — the routes the admitted primitive bought.**  `NOT FORCED`  Exactly
**2**: `withdraw_reflection` and `extra_mark`, obtained by mapping the unnamed
reading's minimum members through the collapse map and subtracting the
side-free minimum members.  Both are mediated by the sides.

*Falsifier:* any other count or member set.

**P12 — side-free `mu2` by row.**  `NOT FORCED`  `base` 0, `keep_labels` 1,
`withdraw_mark_permutations` 0, `extra_mark` 0.

*Falsifier:* any other value.

**P13 — `mu2_restricted`.**  `NOT FORCED`  The minimum is **0** in all three
columns: control, unnamed reading, named reading.  The pinned two columns are
obtained by a data join from the receipt's per-point `collateral_facts`, never
by importing pinned code.

*Falsifier:* any non-zero minimum in any column; any cross-world raw `mu2`
difference field appearing anywhere in the receipt.

**P14 — the two transferring collateral facts, side-free.**  `NOT FORCED`
`order_internally_available` is `false` at every one of the eight points;
`label_internally_available` is `true` at `keep_labels` and at the bundles
that include it, and `false` elsewhere.

*Falsifier:* either fact taking another value anywhere.  Note the reason for
the first: the caller's two supplies carry the same token, so reversing them
is not a change to notice.  This is **not** "the admission order is
unavailable" — the order is the mark's internal identity and is exactly what
the result turns on.

---

## The censuses

**P15 — the withdrawal census.**  `NOT FORCED`

* mirror, 64 cells: **64 of 64** with the mark permutations withdrawn,
  **28 of 64** with them kept.
* control, 8 cells: **8 of 8** withdrawn, **2 of 8** kept.

*Falsifier:* any of the four fractions differing, or a domain size other than
64 and 8.

**P16 — the forgetful lemma holds.**  `FORCED`

**0** lemma violations and **0** corollary violations over the full declared
lemma census.  It is forced because it is a theorem of the two declared
carriers, proved in Lean without a finite bound; the Python census is its
bounded cross-check, so a violation would be an implementation defect.

*Falsifier:* any violation at any cell.

**P17 — the lemma census counts.**  `NOT FORCED`

**2140** side-typed automorphisms checked, and **228** cells at two or more
marks where the side-typed world separates the two retained marks and the
side-free world does not.  The second number is the lemma's non-vacuity: the
corollary is a real constraint and not an empty one.

*Falsifier:* either count differing.  These two depend on the declared census
domain and its declared iteration order, both fixed in `DESIGN.md` section 11;
a differing count means the domain implemented is not the domain declared.

**P18 — the smuggle injection fires.**  `NOT FORCED`

Re-admitting the side into the side-free key as a per-mark two-valued
attribute produces **12** lemma violations, the first at reading `U`, labels
`("a", "a")`, placement `(0, 1)`, automorphism `(reflected=True, pi=(1,0))` —
which is the retained configuration itself.  Reversing the injection returns
the count to 0.

*Falsifier:* zero violations (the tripwire is asleep); a different first cell;
a different total.

**P19 — `Admitted` is inert.**  `NOT FORCED`

The one positive judgment form separates the two retained marks at **no** cell
of the control's route census.

*Falsifier:* any cell at which it separates.

---

## The gates against the pin

**P20 — G4 agrees on all fourteen rows.**  `NOT FORCED`

The control's own verdict function, applied to the pinned world's own recorded
automorphism sets, reproduces the pinned world's own recorded `satisfies`
values on the base row and the six one-step rows of each reading.

*Falsifier:* any disagreement — which VOIDS the run rather than adjusting it.

**P21 — G6 reproduces the pinned vector.**  `NOT FORCED`

The mirror, enumerated by the same generic enumerator, gives space size
**48** per reading, refused-bundle count **41**, base automorphism counts
**2** under `U` and **1** under `O`, minimum **1** under `U` with **3**
classes whose members are `{withdraw_reflection}`,
`{withdraw_mark_permutations}` and `{extra_mark_0, extra_mark_1}`, and minimum
**0** under `O` with **1** class `{base}`.

*Falsifier:* any divergence on any of the 48 rows per reading — which VOIDS.

---

## The endowment ledger

**P22 — the four numeric rows.**  `NOT FORCED`

| row | control | unnamed | named |
|---|---|---|---|
| coordinates the genesis declaration fixes | 0 | 0 | 2 |
| judgments holding at genesis | 0 | 0 | 2 |
| automorphism order at the retained regime | 2 | 2 | 1 |
| renaming generators | 1 | 2 | 1 |

The named reading's 2 in the second row is **unmatchable** and is reported as
such.  The control's 1 in the fourth row is one generator fewer than the
unnamed reading's 2, and is named as a mismatch rather than smoothed.

*Falsifier:* any cell differing.

**P23 — the shared-policy replay.**  `NOT FORCED`

Side-free, the pinned shared identity policy admits then no-ops, yielding
**one** mark; the retained-mark check then raises **by name**.  This is
reported as a refusal of the subject, never as a false and never as a
satisfied requirement.  The pinned moving-admission refusal does **not** fire,
because it has no side-free statement; it is recorded in `DELETED.md` as a
removed refusal.

*Falsifier:* two marks under the shared policy; a `false` verdict reported
where a refusal is due; the removed refusal firing.

**P24 — key-choice invariance.**  `NOT FORCED`

Every reported side-free verdict is identical under `serialize = (n_marks,)`
and under `serialize = ()`, at all eight points.  The choice is therefore
shown not to be load-bearing rather than defended.

*Falsifier:* any verdict differing between the two keys.

---

## The declared secondary, frozen because the answer flips on it

**P25 — excluding every everywhere-satisfying candidate.**  `NOT FORCED`

`withdraw_mark_permutations` satisfies at **100%** of the route census in both
worlds and satisfies **by unfolding**.  With every candidate that satisfies at
every route-census point excluded:

* the control has **no** satisfying candidate at any price, so the secondary
  answer is `NO_SATISFYING_CANDIDATE`;
* the unnamed reading still has `withdraw_reflection`, `extra_mark_0` and
  `extra_mark_1` at price **one**, in **2** classes.

The answer therefore **flips** between the primary and the secondary, and both
numbers are frozen here precisely because it does.  The primary counts the
vacuous route, because excluding it in the control while it stands in the
pinned world would itself be the rigging.

*Falsifier:* the control retaining a satisfying candidate under the exclusion;
the unnamed reading losing one; either price or class count differing.

---

## Terminal

**P26 — the decided value.**  `NOT FORCED`
`what_the_admitted_primitive_bought = NOTHING_IN_COST`.

*Falsifier:* `VOID`, `NO_SATISFYING_CANDIDATE`, or any `COST_DIFFERENCE_<n>`.

**P27 — the terminal sentence stays inside its scope.**  `FORCED`

The tree writes "the admitted primitive bought no price that the admission
order could not buy at the same price", and does **not** write "the admitted
primitive bought nothing".  Whether an order is itself a container is open
obstruction (a) and is not answered here.

*Falsifier:* the unscoped sentence appearing anywhere in this tree.

---

## Global falsifiers

Any one of these falsifies the run as a whole rather than a single line:

1. any side-free one-step candidate other than `withdraw_mark_permutations`
   satisfying, or that one failing;
2. a control class count above 1;
3. `delta_vs_unnamed != 0`;
4. any G4 disagreement — which VOIDS;
5. a mirror reconstruction that fails to reproduce the pinned vector — which
   VOIDS;
6. any lemma violation with no injection live.
