# Unit 12. A fresh datum adds no power

**Claim.** Admitting a fresh datum is a real change of state, and yet the
pair that was collapsed before is collapsed after. More generally, in any
regime whose instances stay inside its data, admitting a fresh datum leaves
the collapse status of every existing pair exactly as it was, in both
directions. **Status:** derived (the first claim is the paper's
**[counterexample]** to "a new inscription necessarily increases
expressive power"). **Lean:**
`Derivation.admission_without_expressive_increase`
(`lean4/Derivation/Inertia.lean` lines 72-79) and
`Derivation.collapsed_fresh_datum` (`lean4/Derivation/Mention.lean` lines
118-148, residual R1). **Axioms:** `propext` for the first; `propext,
Quot.sound` for the second. **Depends on:** `stepE` (Unit 04),
`collapsed`, `wfCtx`, `plug`, `derivable` (Unit 08),
`collapsed_of_no_insts` (Unit 10), `R2L` (Unit 05).

## Question

After Challenge 2 the system holds two data it cannot tell apart (Unit 10).
Would one more datum help? A newcomer might think that each new inscription
enlarges what the system can express. The paper refutes that with one
counterexample, and then proves the general shape of the refutation: a
datum no instance mentions is invisible to every comparison between the
others.

## What we already possess

- `stepE R2L .admitDatum = some ⟨3, [], [], [], [(0, 1)]⟩`: admission adds
  one to the data count and copies the rest (Unit 04, `Basic.lean` line
  147).
- `collapsed r d d'`: every well-formed context plugs to equi-derivable
  instances (Unit 08). `wfCtx r c` has four conjuncts; the third is that
  `c` has a hole, the fourth that every filled slot names a datum below
  `r.data` (`Basic.lean` lines 106-110, `slotOk` lines 92-94).
- `collapsed_of_no_insts`: with no instances, every pair is collapsed
  (Unit 10).
- `derivable r i := i ∈ r.insts ∨ i.1 ∈ r.rules` (Unit 01).

## New concept: mention

An instance **mentions** a datum when the datum is among its arguments.
The mention lemma, residual R3 of the paper, is the fact under this whole
unit: a context plugged with `d` always mentions `d`, because every
well-formed context has a hole and the hole receives `d`
(`mem_plug_of_hole`, `Mention.lean` lines 40-43). So an instance that
does not mention `d` can never be `plug c d`, and adding such instances
cannot change whether `d` is collapsed with anything.

A fresh datum is the first corollary (R1). It does not add instances, but
it does add **contexts**: a slot may now name the new datum. Such a context
is genuinely new, and R1 shows it separates nothing. It mentions a datum no
instance mentions, so neither of its two plugs is an instance; and a rule
covers both plugs or neither. Both sides of the `collapsed` biconditional
fail or hold together. The paper's phrase: a context that reaches outside
the regime "does not separate; it only fails twice".

## Plain-language interpretation

Two words in the notebook, no sentences about either. Add a third word.
Nothing has been said about it, and nothing said about the first two has
changed, so they remain as alike as before. The third word is a real entry
in the ledger, with a real new count of three. It is not more *power*: the
system has gained a name it cannot use, not a way to tell its names apart.

The general theorem says more than the counterexample. Even in a regime
rich in instances, a fresh unmentioned datum changes no existing
comparison, in either direction: a collapsed pair stays collapsed and a
separated pair stays separated. What the fresh datum's *own* comparisons
look like is a separate question, and the theorem does not speak to it. In
`R2L` plus a datum, the new datum is collapsed with both old ones (Unit 10
again); in the link regime `BL` plus a datum, the new datum is separable
from both old ones, because the old instance mentions them and not it.

## Pseudocode

```
# Gloss
counterexample:
    s := R2L with data + 1          -- a different regime (3 ≠ 2)
    s has no instances, so (0, 1) is collapsed in s      -- Unit 10

R1, for a well-formed regime r and old data d, d':
    collapsed(r + fresh datum, d, d')  iff  collapsed(r, d, d')
    (→)  every old context is still a context; apply the new collapse to it
    (←)  take a new context c:
           if c names only old data:  it is an old context; apply the old collapse
           if c names the fresh datum:  plug(c, d) and plug(c, d') both
               mention the fresh datum, which no instance does, so neither
               is in insts; both sides reduce to "c's form has the rule";
               they agree.
```

## Python

```python
from derivation.engine import GENESIS_L
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, replay, step
from derivation.observe import collapsed_pairs, profiles, separable

r2 = replay(GENESIS_L)
r3 = step(r2, AdmitDatum("<abc>"))
print(r3 != r2, collapsed_pairs(r3), len(set(profiles(r3))))
bl = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(2), AdmitInst(0, (0, 1))])
bl3 = step(bl, AdmitDatum("fresh"))
print(separable(bl3, 0, 1), separable(bl3, 0, 2), separable(bl3, 1, 2))
```

Output:

```text
True ((0, 1), (0, 2), (1, 2)) 1
True True True
```

## Line-by-line Python explanation

`r2 = replay(GENESIS_L)`: reading L after Challenge 2, data `('<a>',
'<ab>')`, nothing else (Unit 05).

`r3 = step(r2, AdmitDatum("<abc>"))`: a token not yet admitted, so this is
an admission and not a designation (Unit 06); `r3.data` has three entries.

`r3 != r2`: `True`. The state changed. This is the "real admission" half of
the counterexample.

`collapsed_pairs(r3)`: all three pairs, the old `(0, 1)` among them. The
old pair stayed collapsed; the new pairs are collapsed too, by Unit 10.

`len(set(profiles(r3)))`: one observational class. This is the quantity
`engine.py` line 214 reports as `expressive_increase_over_challenge0 =
classes > 1`, recorded `False` for both readings in
`artifacts/challenges.json`.

`bl`, `bl3`: the link regime of Unit 19 (two data, a binary form, the
instance `(0, [0, 1])`), then a fresh datum. `separable(bl3, 0, 1)` is still
`True` (R1, the other direction: separated stays separated). `separable(bl3,
0, 2)` and `separable(bl3, 1, 2)` are also `True`, which R1 does not
predict either way; here the instance mentions 0 and 1 and not 2.

The check script runs the biconditional over 354 well-formed regimes with
up to three data, three form tables, up to two instances and an optional
rule: 866 old pairs, every one keeping its status; among the pairs with the
fresh datum, 530 separable and 426 collapsed.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean lines 72-79
/-- Non-increase countermodel: admitting a fresh datum is a real admission
(the state changes) yet the previously collapsed pair stays collapsed —
a new external inscription does not necessarily increase internal
expressive power. -/
theorem admission_without_expressive_increase :
    ∃ s, stepE R2L .admitDatum = some s ∧ s ≠ R2L ∧ collapsed s 0 1 := by
  refine ⟨⟨3, [], [], [], [(0, 1)]⟩, by decide, by decide, ?_⟩
  exact collapsed_of_no_insts _ rfl 0 1
```

```lean
-- Lean (Genesis), lean4/Derivation/Mention.lean lines 40-43 and 118-148
/-- Every plugged instance mentions its datum, because every
well-formed context has a hole and the hole receives it. -/
theorem mem_plug_of_hole {c : Ctx} (h : none ∈ c.slots) (d : Nat) :
    d ∈ (plug c d).2 := by
  simp only [plug]
  exact List.mem_map.mpr ⟨none, h, rfl⟩

/-- **R1.**  Admitting a fresh datum that no instance mentions leaves the
collapse of every existing pair exactly as it was. -/
theorem collapsed_fresh_datum (r : Regime) (d d' : Nat)
    (hwf : ∀ p ∈ r.insts, ∀ a ∈ p.2, a < r.data) :
    collapsed { r with data := r.data + 1 } d d' ↔ collapsed r d d' := by
  constructor
  · intro h c hc
    refine h c ⟨hc.1, hc.2.1, hc.2.2.1, ?_⟩
    intro s hs
    have := hc.2.2.2 s hs
    cases s with
    | none => trivial
    | some x => exact Nat.lt_succ_of_lt this
  · intro h c hc
    by_cases hin : ∀ s ∈ c.slots, slotOk r.data s
    · exact h c ⟨hc.1, hc.2.1, hc.2.2.1, hin⟩
    · -- some slot names the fresh datum: neither plug is an instance
      have hout := exists_out_of_range_slot r.data c.slots hin
      obtain ⟨x, hx, hxbig⟩ := hout
      have hmem : ∀ e : Nat, x ∈ (plug c e).2 := by
        intro e
        simp only [plug]
        exact List.mem_map.mpr ⟨some x, hx, rfl⟩
      have hnot : ∀ e : Nat, plug c e ∉ r.insts := fun e =>
        not_mem_of_arg_out_of_range hwf (hmem e) hxbig
      constructor
      · rintro (hm | hr)
        · exact absurd hm (hnot d)
        · exact Or.inr hr
      · rintro (hm | hr)
        · exact absurd hm (hnot d')
        · exact Or.inr hr
```

## Line-by-line Lean explanation

**The counterexample.** The statement is an existential: there is a state
`s` such that admitting a datum to `R2L` yields `s`, `s` differs from
`R2L`, and `(0, 1)` is collapsed in `s`. `refine ⟨⟨3, [], [], [], [(0, 1)]⟩,
by decide, by decide, ?_⟩` supplies the state (three data, the demand
kept) and discharges the first two conjuncts by computation: `stepE` on
`R2L` evaluates to exactly that state, and the two concrete regimes are
unequal (their `data` fields are 3 and 2). The remaining goal `?_` is
`collapsed ⟨3, …⟩ 0 1`, and `collapsed_of_no_insts _ rfl 0 1` closes it:
the instance list is `[]` by `rfl`. Nothing here is specific to datum 0 and
datum 1; the book's `new_pairs_collapsed` runs the same lemma on `(0, 2)`
and `(1, 2)`.

**The hole lemma.** `plug c d` is `(c.form, c.slots.map (fun s => s.getD
d))`. `simp only [plug]` unfolds it, so the goal is `d ∈ c.slots.map (…)`.
`List.mem_map.mpr` asks for an element of `c.slots` that the function sends
to `d`: the hole `none` is one (`h`), and `none.getD d` is `d` by `rfl`.

**R1, forward direction (`→`).** Assume `h`: collapse in the enlarged
regime. Take an old context `c` with `hc : wfCtx r c`. We must show it is
also a context of the enlarged regime, then apply `h`. The first three
conjuncts of `wfCtx` do not mention `data`, so `hc.1`, `hc.2.1`, `hc.2.2.1`
carry over. The fourth asks each slot to be `slotOk (r.data + 1)`; for a
hole that is `trivial`, and for a filled slot `some x` the old bound `x <
r.data` gives `x < r.data + 1` by `Nat.lt_succ_of_lt`. The plugs do not
depend on `data`, so `h c ⟨…⟩` is exactly the goal.

**R1, backward direction (`←`).** Assume `h`: collapse in `r`. Take a
context `c` of the enlarged regime. `by_cases hin` splits on whether every
slot of `c` is already in range for `r.data`.

- If so, `c` is an old context, and `h c ⟨…, hin⟩` closes the goal.
- If not, `exists_out_of_range_slot` (lines 56-78, proved by induction on
  the slot list so that the witness is extracted constructively) gives a
  filled slot `some x` with `¬ x < r.data`: a slot naming the fresh datum.
  `hmem` shows that `x` is an argument of `plug c e` for every `e`, by the
  same `List.mem_map` move as the hole lemma, with `some x` in place of
  `none`. `hnot` turns that into `plug c e ∉ r.insts` for every `e`, using
  `not_mem_of_arg_out_of_range` (lines 47-51): an instance in a regime
  satisfying `hwf` has all arguments below `data`, and `x` is not. Now the
  biconditional: in each direction, `rintro (hm | hr)` splits `derivable`
  into its two disjuncts. The membership disjunct `hm` is impossible by
  `hnot`; the rule disjunct `hr` is about the form alone and is the same on
  both sides, so `Or.inr hr` closes it. The context fails twice, as
  promised.

**Axioms.** The counterexample reports `propext` only: its two `decide`
calls compare a `Regime` built from `Nat` and `List` fields, and
`collapsed_of_no_insts` carries `propext` from the definitions. `R1`
reports `propext, Quot.sound`: `simp only [plug]` and `List.mem_map` go
through list lemmas that use `Quot.sound`. The helper
`not_mem_of_arg_out_of_range` uses no axioms, and
`exists_out_of_range_slot` only `propext`.

## What has been proved

- Admitting a datum to `R2L` changes the state and leaves `(0, 1)`
  collapsed (Genesis, derived; the paper's **[counterexample]**).
- In any regime whose instance arguments lie below its data count, a
  fresh datum leaves the collapse of every pair of old data exactly as it
  was, in both directions (Genesis, derived; R1).
- The two new pairs of `R2L`-plus-a-datum are collapsed as well, and in
  `BL`-plus-a-datum the old pair stays separable while the fresh datum is
  separable from datum 0 (book Lean, derived on examples).
- The hypothesis `hwf` of R1 is a conjunct of `Regime.wf` (`Basic.lean`
  lines 64-71); it is not a new assumption on well-formed regimes.

## What has not been proved

- That the number of observational classes stays 1. The paper's sentence
  says so, and it is true (the book's `new_pairs_collapsed` with Unit 10),
  but the Lean theorem states `collapsed s 0 1` and nothing about the
  pairs with the new datum. The audit records this as a prose-stronger-
  than-Lean note, not a defect.
- Anything about the fresh datum's own comparisons. R1 is silent on them,
  and the two examples go opposite ways.
- That a fresh datum *never* helps. It helps exactly when an instance
  mentioning it is also admitted: that is the Challenge-3 response space
  of Units 18 to 22, where `(NewDatum, NewInst mentioning it)` is one of
  the pruned delta shapes (`candidates.py` lines 288-296). R1 is what
  licenses the pruning of the *unmentioned* case; it does not promote
  `CL-PRUNE-STRUCTURAL` to a theorem (paper line 742).
- R2, the same result for a fresh form (`collapsed_fresh_form`, lines
  168-199). It is taught with the Challenge-3 candidate space.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `∃ s, …` | the counterexample's shape | metatheory existential; the witness is a concrete regime |
| `(r : Regime) (d d' : Nat)`, `∀ c : Ctx` | R1's universal statement | metatheory quantifiers over all regimes, data and contexts |
| `by_cases hin` on a decidable bounded `∀` | the case split | metatheory decision; constructive here because `slotOk` is decidable |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** After the admission: a data count of three, the
demand, and nothing else. It does not hold "the set of contexts": contexts
are the metatheory's way of enumerating comparisons, and `wfCtx` reads
them off the ledger. When the unit says the fresh datum "adds contexts", it
means the metatheory's census of well-formed contexts grows; nothing was
added to the ledger but one count.

**Phrases to read with care.**

- "Expressive power" is the paper's phrase for the number of observational
  classes. It is a metatheoretic count over profiles, not a capacity the
  system possesses.
- "A name it cannot use" is a gloss. The system does not hold names; the
  token stays in the metatheory (Unit 06).
- "Fails twice" means both plugs are underivable. It is not an event in the
  system; nothing was tried.

## Student exercise

Take the regime `⟨2, [1], [(0, [1])], [], []⟩` (two data, one unary form,
the instance "datum 1 is marked"; this is `U1` without its demand). Datum 0
and datum 1 are separable (Unit 09). Admit a fresh datum. Is `(0, 1)` still
separable, and by which theorem? Is the fresh datum 2 separable from datum
0? From datum 1? Give the witnessing context or the reason there is none.

## Answer

`(0, 1)` stays separable: R1 gives `collapsed r' 0 1 ↔ collapsed r 0 1`,
so `¬ collapsed r' 0 1` follows from `¬ collapsed r 0 1`
(`separable_not_collapsed` with Unit 09's witness `⟨0, [none]⟩`). The
hypothesis `hwf` holds because the only instance's argument `1 < 2`. Datum
2 against datum 1: separable, witness `⟨0, [none]⟩`; plugging 1 gives
`(0, [1])`, an instance; plugging 2 gives `(0, [2])`, not an instance, and
there is no rule. Datum 2 against datum 0: the only well-formed contexts
have the shape `⟨0, [none]⟩` (arity 1 forces a single slot, which must be
the hole), and plugging 0 or 2 gives a non-instance either way. So `(0, 2)`
is collapsed. (The check script's family includes this regime.)

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Inertia.lean` lines 72-79; `lean4/Derivation/Mention.lean` lines 40-51 (`mem_plug_of_hole`, `not_mem_of_arg_out_of_range`), 56-78 (`exists_out_of_range_slot`), 118-148 (`collapsed_fresh_datum`) |
| Axiom report | `artifacts/lean_axioms.txt`: `admission_without_expressive_increase` `[propext]`; `collapsed_fresh_datum`, `mem_plug_of_hole` `[propext, Quot.sound]`; `exists_out_of_range_slot` `[propext]`; `not_mem_of_arg_out_of_range` none |
| Paper | `paper/paper.md` §6 **[counterexample]** (lines 249-252); residuals R1–R3 (lines 425-432 and 734-742) |
| Ledger | `paper/paper_claim_ledger.md`, `CL-2-NONINCREASE` (class: counterexample; Python `challenge2.*.expressive_increase_over_challenge0 = false`); residual table row R1, discharged 2026-08-17 |
| Artifact | `artifacts/challenges.json`, `challenge2.readings.{L,F}.expressive_increase_over_challenge0: false`, `observational_classes: 1` |
| Test | `tests/test_engine.py::test_challenge2_collapse_and_no_expressive_increase`; `tests/test_candidates.py::test_pruned_cost2_contains_every_valid_full_delta` (the pruning R1 licenses, checked against the unpruned space) |
| Check (Python) | `python textbook/checks/u12_fresh_datum.py`: the counterexample on reading L; 354 well-formed regimes, 866 old pairs all keeping their status; fresh-datum pairs 530 separable and 426 collapsed; `BL3`; artifact flags reproduced |
| Check (book Lean) | `python textbook/checks/u12_lean.py`: twelve book theorems plus six Genesis theorems kernel-checked, Lean 4.33.0; axioms as listed above, `fresh_is_a_change`, `R2L_insts_wf`, `R3L_eq` and `BL_insts_wf` with none |
