# Unit 18. One item never answers the demand

**Claim.** With no forms and no instances to begin with, zero or one added
item cannot separate the demanded pair. Challenge 3 therefore needs at
least two items under the declared item-count measure.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** On any regime with no forms and no instances, no delta of zero
or one item is a valid response to a separation demand. Every such delta
either fails to apply (an instance or a rule with no form to attach to)
or applies and leaves the instance list empty, and with no instances the
pair stays collapsed. So the least cost of meeting the Challenge 3
demand, measured in items, is at least two.

**Status:** derived. **Lean:**
`Derivation.cost1_insufficient_general` (`lean4/Derivation/Minimality.lean`
lines 98-142), instantiated as `cost1_insufficient` (reading L) and
`cost1_insufficient_F` (reading F). **Axioms:** `propext`. **Depends on:**
`Item`, `applyItem`, `applyDelta`, `validResponse` (`Basic.lean` lines
171-200, introduced here); `collapsed_of_no_insts` (Unit 10);
`separable_not_collapsed` (Unit 09).

</details>

## First pass

Start with two data and no sentence shapes or instances. A **form**
is a sentence shape with a declared number of places. An **instance**
fills those places with admitted data. Each addition counts as one
item under the measure used here.

**Predict:** can one item make a test distinguish 0 from 1?
A form alone supplies a shape with no instance. An instance alone is
refused because its form does not exist. A uniform rule also needs a
form. A new datum supplies neither a form nor an instance. Doing
nothing does not help either.

Thus zero or one item cannot answer this demand under these starting
conditions. The next chapter supplies a two-item answer.

Change the starting conditions: admit a unary form first. Now one
instance, marking only 0, does distinguish the pair. The lower bound
depends on beginning without forms and instances; it is not a universal
price for making a distinction.

For a slower worked search with all tied plans visible, see the
[Search lab](../search_lab/README.md).

## Question

Unit 16 showed the demand is unmet. Now the system may be augmented. What
is the least that must be admitted? Could a single admission do it: one
new form, or one new datum, or one cleverly chosen instance? Genesis
answers absolutely, over the whole grammar of items, not just within the
enumerated bounds.

## What we already possess

- A regime with no instances has every pair collapsed, whatever its
  forms and rules (Unit 10), and a collapsed pair is not separable
  (Unit 09). Together: `no_insts_no_separation` (Minimality lines 94-96).
- `stepE` and the guards on admission (Units 03, 17).

## New concept: deltas, items and valid responses

An **item** is one unit of augmentation. `Basic.lean` lines 171-176:

| Item | Effect under `applyItem` | Guard |
|---|---|---|
| `newDatum` | `data + 1` | none |
| `newForm a` | append arity `a` to `forms` | `1 ≤ a` |
| `newInst f args` | insert `(f, args)` into `insts` | `f` is a form, `args.length` is its arity, every arg is an admitted datum |
| `newRuleAll f` | insert `f` into `rules` | `f` is a form |

A **delta** is a list of items, applied left to right (`applyDelta`,
lines 192-193, a `foldlM` like `replayE`). The item grammar mirrors the
admission events minus `supply` and `impose`: a delta is what the
*responder* may admit, and the responder cannot supply tokens or impose
demands.

A **valid response** to the demand `(i, j)` on `r` (lines 198-200) is a
delta that applies, whose result separates `i` from `j`, and whose result
still separates every pair previously in `r.reqs`.

The **cost** `mu1` of a delta is its length (paper §3, definition 6). The
theorem is about deltas of length at most one.

## Plain-language interpretation

Separation needs a sentence that is true of one datum and not the other.
A sentence needs a form to be a sentence *of*, and an instance to be
*admitted*. A single item can supply at most one of these. A lone form
gives sentence shapes with nothing asserted; a lone instance has no shape
to take and is refused at the door; a lone datum changes nothing about
the existing pair (Unit 12); a lone rule has no form either. So the first
possible answer costs two items: one form and one instance. Unit 19
shows that two do suffice.

The theorem is **absolute**: it does not say "within arity 2" or "within
the enumerated candidates". It quantifies over every item of the grammar,
with any arity and any argument list. That is what the Lean adds beyond
the Python enumeration, which is complete only within its declared
bounds.

## Pseudocode

```
# Gloss
given r with forms = [] and insts = [], a demand (i, j), a delta δ of length ≤ 1:
case δ = []:            result = r;  no instances;  (i, j) collapsed;  not separable.
case δ = [newDatum]:    result has one more datum; still no instances; collapsed.
case δ = [newForm a]:   if a ≥ 1, result has a form, still no instances; collapsed.
                        if a = 0, the item does not apply.
case δ = [newInst f _]: f < length [] is false; does not apply.
case δ = [newRuleAll f]: same; does not apply.
In every case δ is not a valid response.
```

## Python

```python
from derivation.candidates import Bounds, NodeView, iter_cost1_items, min_responses, response_valid_fast
from derivation.engine import GENESIS_L
from derivation.model import replay

base = replay(GENESIS_L)
view = NodeView.of(base)
items = list(iter_cost1_items(base, Bounds(2, 2)))
print(items)
print([response_valid_fast(view, (0, 1), (it,)) for it in items],
      response_valid_fast(view, (0, 1), ()))
print(min_responses(base, (0, 1), "mu1", Bounds(2, 2)).cost)
```

Output:

```text
[NewDatum(), NewForm(arity=1), NewForm(arity=2)]
[False, False, False] False
(2, -1)
```

## Line-by-line Python explanation

`iter_cost1_items(base, bounds)` (`candidates.py` line 260) lists the
one-item deltas worth trying within the bounds: a datum and the forms of
arity 1 and 2. It does not list instances or rules because, with no forms
in `base`, none would apply; the Lean proof handles those cases
explicitly instead.

`NodeView.of(base)` precomputes the contexts and profiles of the base so
that `response_valid_fast` (line 224) can judge a delta without
replaying; the tests cross-check it against the naive replay
(`test_fast_equals_naive_on_full_space`). All three items, and the empty
delta `()`, are invalid.

`min_responses` (line 370) walks costs 0, 1, 2 and returns the first
cost with a valid delta: `(2, -1)`, the `-1` marking that `mu1` has no
second component.

The check script also goes beyond the search's arity bound: it tries a
finite collection with form arities up to 5, form indices up to 2, and
argument-list lengths 1 or 2. Argument indices include one position
beyond the admitted data (45 deltas in reading L). The six that apply
(one datum, five forms)
leave the pair collapsed; the 39 instances and rules are refused. That is
the Lean case analysis, run by hand on a finite slice.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Minimality.lean lines 98-142 (abridged:
-- the four item cases are shown; the dead-end helper is lines 94-96)
theorem cost1_insufficient_general (r : Regime) (hforms : r.forms = [])
    (hinsts : r.insts = []) (i j : Nat) (δ : List Item)
    (hlen : δ.length ≤ 1) : ¬ validResponse r i j δ := by
  intro h
  cases h with
  | intro s hs =>
    have happ := hs.1
    have hsep := hs.2.1
    cases δ with
    | nil =>
        have hz : r = s := Option.some.inj happ
        subst hz
        exact no_insts_no_separation hinsts hsep
    | cons it rest =>
      cases rest with
      | cons b r2 => simp at hlen
      | nil =>
        rw [applyDelta_single] at happ
        cases it with
        | newDatum =>
            have hz := Option.some.inj happ
            subst hz
            refine no_insts_no_separation ?_ hsep
            exact hinsts
        | newForm a =>
            simp only [applyItem] at happ
            split at happ
            · have hz := Option.some.inj happ
              subst hz
              refine no_insts_no_separation ?_ hsep
              exact hinsts
            · cases happ
        | newInst f args =>
            simp only [applyItem] at happ
            rw [if_neg (by simp [hforms])] at happ
            cases happ
        | newRuleAll f =>
            simp only [applyItem] at happ
            rw [if_neg (by simp [hforms])] at happ
            cases happ
```

## Line-by-line Lean explanation

The hypotheses: `hforms`, `hinsts` say the regime is form-less and
instance-less; `hlen` bounds the delta. The goal `¬ validResponse …` is
proved by assuming `h : validResponse r i j δ` and reaching `False`.

`cases h with | intro s hs`: a valid response is an existential; `s` is
the result regime and `hs` the three-part conjunction. `happ : applyDelta
r δ = some s`; `hsep : separable s i j`. The third part (previous demands
stay separated) is never needed.

`cases δ`. **Empty delta:** `applyDelta r [] = some r`, so `Option.some.inj
happ : r = s`; `subst` replaces `s` by `r`, and `no_insts_no_separation
hinsts hsep` is the contradiction: `r` has no instances, so (Unit 10) the
pair is collapsed, so (Unit 09) it is not separable.

**Two or more items:** `simp at hlen` finds `2 ≤ 1` false.

**One item** `it`: `applyDelta_single` (lines 21-25) rewrites the fold as
`applyItem r it`. Then one case per item kind.

- `newDatum`: the result is `r` with `data + 1`; its `insts` field is
  still `r.insts = []`, which is what `exact hinsts` supplies after
  `subst`. Same dead end.
- `newForm a`: `split at happ` on the guard `1 ≤ a`. If it holds, the
  result's `insts` is again `r.insts`; same dead end. If not,
  `happ : none = some s`, impossible.
- `newInst f args`: the guard begins `f < r.forms.length`, and
  `hforms` makes the length `0`; `if_neg` with `simp [hforms]` rewrites
  the `if` to `none`, and `cases happ` closes.
- `newRuleAll f`: identical.

Nothing in the proof looks at the arity `a`, the form index `f` or the
arguments `args` beyond the guards. That is the sense in which the
result is absolute over the grammar.

`cost1_insufficient` and `cost1_insufficient_F` (lines 144-151) apply the
theorem to `R2L` with `rfl, rfl` for the two emptiness hypotheses, and to
`R2F` with the demand `(1, 2)`.

**Axioms.** `propext` only: `simp` and `split` on the definitions, no
`decide` on concrete lists.

## What has been proved

- On every form-less, instance-less regime, for every pair and every
  delta of length at most one, the delta is not a valid response
  (Genesis, derived, absolute over the item grammar).
- Its instances at `R2L` and `R2F` (Genesis, derived).
- The book: the empty, datum-only and form-only deltas named, with their
  results computed; instance-only and rule-only deltas rejected for any
  `f`, `args`; the theorem applied to a five-datum regime with two
  demands; and, with a form already admitted, one instance *is* a valid
  response, so the hypothesis `forms = []` is doing work.
- Within the bounds, Python agrees: no valid delta below cost 2 in either
  reading, and the minimum is exactly 2 (Genesis, verified finite).
- With no forms, no well-formed context exists, regardless of what a raw
  record's instance list contains (book, `no_forms_no_separation`). The
  supplied unknown-form record is neither well formed nor separable.

## What has not been proved

- That two items suffice. That is Unit 19 (`deltaBL_valid`) and, for the
  cheapest, Unit 22; the paper's "minimum cost is exactly 2" combines
  this unit's floor with those witnesses (`CL-3-MIN-TWO`).
- That `mu1` is the right measure. It is declared (paper §3, definition
  6). Under `mu2` the same floor holds, since `mu2` orders by item count
  first.
- Anything about regimes that already have a form. The theorem's
  hypothesis excludes them, and the book's `one_item_suffices_with_a_form`
  shows the exclusion is necessary.
- That a "single step" cannot bundle a form and an instance. In this
  grammar it cannot: a bundle is two items, and the paper's negative test
  `test_smuggling_a_bundle_is_not_one_item` pins that reading.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Item`, `applyItem`, `applyDelta` | the candidate grammar | admitted; "metatheory apparatus … declared bounds of the derivation" (`candidates.py` docstring) |
| `validResponse` | what counts as answering the demand | admitted (paper §3, definition 7) |
| `δ.length ≤ 1`, `mu1` | the cost | the metatheory's count of items; the measure is declared |
| `Option.some.inj`, `subst`, `split`, `simp` | the proof | metatheory logic over the definitions |

**What the system holds.** Nothing new: the theorem is about what a
responder *cannot* achieve with one admission. After any one-item delta
that applies, the regime has at most one more datum or one more form and
still no instance.

**Phrases to read with care.**

- "Absolute" means: over every item of the declared grammar. It does not
  mean over every conceivable augmentation; the grammar itself is
  admitted.
- "Cost" is a count of items in a list the metatheory wrote. The system
  does not pay anything.

## Student exercise

Take the regime `⟨2, [], [], [], [(0, 1)]⟩` and the one-item delta
`[.newForm 0]`. Does it apply? Which branch of the proof handles it, and
what does `happ` look like there? Then take `[.newInst 0 [0, 1]]`: which
part of the instance guard fails, and would the theorem still hold if
the guard were weakened to allow instances on unknown forms?

## Answer

<details>
<summary>Worked answer</summary>

`[.newForm 0]` does not apply: the guard is `1 ≤ 0`, false, so
`applyItem` returns `none`. In the proof, the `newForm a` case does
`split at happ`; the second branch has `happ : none = some s`, closed by
`cases happ`. For `[.newInst 0 [0, 1]]`, the first conjunct of the guard,
`0 < [].length`, fails. Removing only that conjunct would still not
admit this example: the remaining arity check compares the two arguments
with `[].getD 0 0 = 0`, and fails as well.

Suppose instead that a different admission operation forcibly inserts
the unknown-form instance. The existing proof's rejection branch would
no longer describe that operation. This alone would not refute the lower
bound: with no forms there is still no well-formed context, so the
inserted instance supplies no separability witness under the unchanged
definition. The book proves this no-form result separately. The raw
record would also fail `Regime.wf`.

To assess the changed system, specify all the changed guards and context
rules. A broken proof step is not by itself a counterexample to its
conclusion.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Minimality.lean` lines 94-151; `Basic.lean` lines 171-200 (items, `applyItem`, `applyDelta`, `validResponse`) |
| Axiom report | `artifacts/lean_axioms.txt`: `cost1_insufficient_general`, `cost1_insufficient`, `cost1_insufficient_F`, `no_insts_no_separation` each `[propext]` |
| Paper | `paper/paper.md` §7.2 (**[theorem]**, "candidate bounds: none … scope: absolute over the grammar"), §3 definitions 6-7 |
| Ledger | `paper/paper_claim_ledger.md`, `CL-3-COST1-IMPOSSIBLE`, `CL-3-MIN-TWO` |
| Artifact | `artifacts/challenges.json`, `challenge3.{L,F}.mu1.cost_below_minimum_all_fail = true`, `minimum_cost = [2, -1]`; `artifacts/claims.json`, `CL-3-MIN-TWO` |
| Test | `tests/test_candidates.py::test_c3_cost1_all_fail_and_min_is_two`, `::test_smuggling_a_bundle_is_not_one_item`, `::test_new_datum_alone_never_separates` |
| Check (Python) | `python textbook/checks/u18_cost1.py`: both readings, no valid delta at cost 0 or 1 within bounds by both validity checks; 45 (L) and 69 (F) attempted one-item deltas in the larger finite slice; minimum exactly 2; one instance suffices once a form exists; five-datum regime; remaining unknown-form arity guard fails and forced raw record has no contexts |
| Check (book Lean) | `python textbook/checks/u18_lean.py`: twelve book reports plus four Genesis theorems kernel-checked, Lean 4.33.0; `propext` except the form-first witness and unknown-form well-formedness refutation (`propext, Quot.sound`) |
