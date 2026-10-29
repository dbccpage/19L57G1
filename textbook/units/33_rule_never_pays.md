# Unit 33. Uniform-rule items cannot minimize the declared costs

**Claim.** Removing every newly added uniform-rule item from a valid response
keeps it valid. If at least one was removed, the response is shorter with
the same new-form arity sum, so it wins under both declared cost measures.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** A response delta that contains a uniform-rule item is never a
minimum valid response under either declared measure. Dropping every rule
item from a valid delta leaves a valid delta (`validResponse_dropRules`)
that is strictly shorter when a rule item was present and has the same new-form arity sum
(`rule_item_never_minimal`), so it beats the original under `mu1` and
under lexicographic `mu2`. The bridge that makes this possible is
definitional: no guard of `applyItem` reads the rule field and only
`newRuleAll` writes it, so the rule-free part of a delta applies over any
rule field and produces the same regime except for `rules`
(`applyDelta_dropRules`).

**Status:** derived (R4, discharged 2026-08-18;
the comparison of measures is prose over the declared `mu1`, `mu2`).
**Lean:** `Derivation.dropRules` (`lean4/Derivation/RuleBridge.lean` lines
40-44), `applyItem_rules_mono` (46-73), `applyDelta_rules_mono` (75-93),
`applyDelta_dropRules` (100-181), `dropRules_length_le` (183),
`dropRules_length_lt` (195-223), `aritySum_dropRules` (225-238),
`validResponse_dropRules` (245-255), `rule_item_never_minimal` (259-266);
`separable_of_subrules` (`Progress.lean` lines 202-205). **Axioms:**
`propext` for all of RuleBridge. **Depends on:** `applyItem`, `applyDelta`
and the item grammar (Unit 17); valid responses (Unit 18); the uniform
rule and `derivable` (Unit 08); `mu1`, `mu2` (Units 21, 22).

</details>

## First pass

Start with two data, A and B, one unary form `marked`, and only the
instance `marked(A)`. Asking `marked(□)` gives Yes on A and No on B, so
the pair is separated.

Now add the uniform rule for that form: every instance of `marked`
counts as derivable. The question gives Yes on both data. The rule has
erased this distinction.

The general proof needs one more step. If a valid response contains
uniform-rule items, removing those items must still let its other items
apply. Here it does: the guards for data, forms, and instances never read
the rule field. The remaining response reaches the same other fields,
keeps all required separations, and costs fewer items.

**Predict:** does this mean a valid response can never contain a uniform
rule?

<details>
<summary>Check your prediction</summary>

No. A rule on another form can leave the required distinction intact.
Such a response can be valid but cannot be cheapest under these measures,
because its rule-free version is shorter.

</details>

These are the system's uniform rules, not a conclusion about rules in
ordinary life or about every possible cost measure.

## Question

The enumeration of two-item responses never tries a delta containing a
uniform rule (Unit 18 listed the pruning shapes; none has a `NewRuleAll`).
Why may it skip them? A uniform rule makes every instance of a form
derivable at once; that sounds like a lot of separating power for one
item. The claim is the reverse: a rule can only *remove* separations, so
a delta that imposes one can always be improved by leaving it out. Unit
18's `separable_of_subrules` proved half of this at the level of
*regimes*. The other half, at the level of delta *items*, was a test
until R4 was discharged.

## What we already possess

- `applyItem` and its four guards (Unit 17): a datum always applies; a
  form if its arity is at least 1; an instance if its form exists, its
  arity matches and its arguments are admitted; a rule if its form
  exists. `applyDelta` folds `applyItem` over the list (Unit 18).
- `derivable r i := i.1 ∈ r.rules ∨ i ∈ r.insts` (Unit 08): a rule on a
  form makes *every* instance of that form derivable.
- `separable_of_subrules s rs' hsub d d'` (Progress, Unit 18): if `rs' ⊆
  s.rules` and `d`, `d'` are separable in `s`, they are separable in `s`
  with rules replaced by `rs'`. A witness context never lives on a
  uniformly ruled form, because there both pluggings are derivable.
- `aritySum` and `mu2 = (length, aritySum)` (Unit 22).

## New concept: a bridge that is definitional, and a parametrized induction

The regime-level lemma says: shrinking the final rule set keeps
separations. To use it for *deltas*, one must know that removing the rule
items from a delta produces the same final regime with a smaller rule
set. That is not obvious from the lemma; it is a fact about how items
apply. Reading `applyItem`: the `newDatum`, `newForm` and `newInst`
cases never consult `r.rules` in their guards or their updates, and the
`newRuleAll` case changes nothing but `rules`. So the evolution of
`data`, `forms`, `insts` and `reqs` under a delta does not depend on the
rule field at all.

The master lemma `applyDelta_dropRules` states this with a free
parameter: for *any* replacement rule list `rs`, applying `dropRules δ`
to `r` with rules `rs` gives `s` with rules `rs`. The parameter is what
makes the induction go through: at a `newRuleAll` step the regime's
rules change, but the statement is for every `rs`, so the induction
hypothesis still applies to the new regime. The subset condition that
`separable_of_subrules` needs enters only at the end, supplied by
monotonicity: `r.rules ⊆ s.rules` because admission never removes a
rule.

## Plain-language interpretation

A uniform rule says "every sentence of this shape counts as asserted".
It fills in the whole column of the ledger at once. Filling a whole
column never helps you tell two objects apart with a stencil of that
shape, because the stencil now says yes to everything. It can only hide
differences that individual sentences were showing. So whatever a
response achieves with a rule in it, the same response with the rule
struck out achieves too, and it is shorter by the number of rule items
removed. Under either declared cost measure, a cheapest response never
contains a uniform-rule item. This concerns the book's `newRuleAll`
constructor; it is not a claim about every use of the word “rule.”

The careful part is that "strike out the rule and nothing else changes"
has to be checked against the admission procedure, item by item. It
holds because the procedure never *looks at* the rules when deciding
whether a datum, a form or an instance may be admitted.

## Pseudocode

```
# Gloss
dropRules([])                 = []
dropRules(newRuleAll f :: xs) = dropRules(xs)
dropRules(it :: xs)           = it :: dropRules(xs)

bridge (for every rs):
  applyDelta(r, delta) = some s
  ==> applyDelta(r with rules := rs, dropRules(delta)) = some (s with rules := rs)
  induction on delta:
    [] : s = r, nothing to do
    newRuleAll f :: rest : the item only changed rules; apply the hypothesis
                           to the changed regime with the same rs
    other item :: rest : its guard and update ignore rules; step, then hypothesis

validity transfers:
  valid(r, i, j, delta) gives s; bridge at rs := r.rules gives s' = s with rules r.rules
  r.rules ⊆ s.rules by monotonicity
  separable_of_subrules carries the target and every demand from s to s'

never minimal:
  valid drop; length strictly smaller (a rule item was removed);
  aritySum unchanged (rule items contribute nothing)
```

## Python

The check reproduces the full-space cross-check of Genesis's test suite
on the mixed regime, and shows the subset direction on the unary mark.

```python
from derivation.candidates import (Bounds, NewRuleAll, iter_cost2_deltas, iter_full_deltas,
                                   min_responses, mu1, mu2, response_valid_naive)
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, AdmissionError, Impose, replay
from derivation.observe import collapsed_pairs

base = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1),
               AdmitForm(1), AdmitForm(2), AdmitInst(0, (1,)), AdmitInst(1, (0, 2))])
has_rule = lambda d: any(isinstance(it, NewRuleAll) for it in d)
print(any(has_rule(d) for d in iter_cost2_deltas(base, Bounds(2, 2), (1, 2))))
ok = True
for d in iter_full_deltas(base, 2, Bounds(2, 2)):
    if has_rule(d):
        try:
            valid = response_valid_naive(base, (1, 2), d)
        except AdmissionError:
            continue
        if valid:
            rest = tuple(it for it in d if not isinstance(it, NewRuleAll))
            ok &= response_valid_naive(base, (1, 2), rest) and mu1(rest) < mu1(d) and mu2(rest)[1] == mu2(d)[1]
print(ok)
u0 = replay([AdmitDatum("a"), AdmitDatum("b"), Impose(0, 1), AdmitForm(1), AdmitInst(0, (0,))])
print(collapsed_pairs(u0), collapsed_pairs(replay([AdmitRuleAll(0)], u0)))
```

Output (the check script prints the counts as well):

```text
False
True
() ((0, 1),)
```

```text
pruned two-item enumeration: 85 deltas, rule items present: False
full two-item space: 175 deltas, 35 with a rule item, 30 of those valid; every valid one has a valid rule-free part, shorter, same arity sum: True
  example: datum+rule@0 (2, 0) -> datum (1, 0)
```

## Line-by-line Python explanation

`base` is the test suite's mixed regime: three data, a unary and a binary
form, two instances, one standing demand. It is chosen so that rule items
*apply* (both forms exist) and some responses are valid.

`iter_cost2_deltas(base, bounds, target)` is the pruned enumeration; the
first print is `False`: no rule item is ever generated. That is the
pruning this unit licenses.

`iter_full_deltas(base, 2, bounds)` is the unpruned space, 175 two-item
deltas. Of them 35 contain a rule item; `response_valid_naive` raises
`AdmissionError` on the ill-formed ones and returns a verdict on the rest;
30 are valid. For each, `rest` drops the rule items, and three facts are
checked: `rest` is valid, `mu1(rest) < mu1(d)`, and the second component of
`mu2` is unchanged. All 30 pass. The first printed example admits a fresh
datum and a rule on form 0. The existing binary instance `(0,2)` still
separates the target `(1,2)` through the context `binary(0,□)` and the
standing pair `(0,1)` through `binary(□,2)`. Thus validity survives even
though the uniform unary rule erases that form's distinction.

The fresh datum is not automatically separable from everything: in this
ruled result, datum 1 and the newcomer 3 are collapsed. The check records
this pair explicitly. Removing the rule leaves a valid one-item response
here because the earlier distinctions already answered both demands.

The last line is the subset direction seen the other way. `u0` is the
unary mark, which separates `(0, 1)`. Adding the uniform rule on its only
form makes both pluggings of the one context derivable, and `(0, 1)` is
collapsed again. A rule can undo a separation; it cannot make one.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/RuleBridge.lean lines 40-44
def dropRules : List Item → List Item
  | [] => []
  | .newRuleAll _ :: rest => dropRules rest
  | it :: rest => it :: dropRules rest
```

```lean
-- Lean (Genesis), lean4/Derivation/RuleBridge.lean lines 100-111 and 163-181
-- (the statement, the base case and the rule case; the three other cases
-- have the same shape as the rule case with one more guard rewrite)
theorem applyDelta_dropRules {δ : List Item} :
    ∀ {r s : Regime} (rs : List Nat), applyDelta r δ = some s →
      applyDelta ⟨r.data, r.forms, r.insts, rs, r.reqs⟩ (dropRules δ)
        = some ⟨s.data, s.forms, s.insts, rs, s.reqs⟩ := by
  induction δ with
  | nil =>
    intro r s rs h
    injection h with h
    subst h
    rfl
  | cons it rest ih =>
    intro r s rs h
    rw [applyDelta_cons] at h
    cases it with
    ...
    | newRuleAll f =>
      simp only [applyItem] at h
      split at h
      next hg =>
        have h' : applyDelta
            { r with rules := insertNew r.rules f } rest = some s := h
        show applyDelta ⟨r.data, r.forms, r.insts, rs, r.reqs⟩
            (dropRules rest)
          = some ⟨s.data, s.forms, s.insts, rs, s.reqs⟩
        exact ih (r := { r with rules := insertNew r.rules f }) rs h'
      next =>
        have hnone : (none : Option Regime) = some s := by
          exact h
        exact nomatch hnone
```

```lean
-- Lean (Genesis), lean4/Derivation/RuleBridge.lean lines 245-266
theorem validResponse_dropRules {r : Regime} {i j : Nat} {δ : List Item}
    (h : validResponse r i j δ) : validResponse r i j (dropRules δ) := by
  obtain ⟨s, hs, hsep, hall⟩ := h
  have hbridge := applyDelta_dropRules (rs := r.rules) hs
  have hsub : ∀ g ∈ r.rules, g ∈ s.rules := applyDelta_rules_mono hs
  refine ⟨⟨s.data, s.forms, s.insts, r.rules, s.reqs⟩, hbridge, ?_, ?_⟩
  · exact separable_of_subrules s r.rules hsub i j hsep
  · intro q hq
    exact separable_of_subrules s r.rules hsub q.1 q.2 (hall q hq)

theorem rule_item_never_minimal {r : Regime} {i j : Nat} {δ : List Item}
    {f : Nat} (hf : Item.newRuleAll f ∈ δ)
    (h : validResponse r i j δ) :
    validResponse r i j (dropRules δ) ∧
    (dropRules δ).length < δ.length ∧
    aritySum (dropRules δ) = aritySum δ :=
  ⟨validResponse_dropRules h, dropRules_length_lt hf,
    aritySum_dropRules δ⟩
```

The book's Lean exhibits a valid four-item response to Challenge 3 that
carries a rule, applies the corollary to it, instantiates the bridge with
an arbitrary rule field, and shows the subset direction is not free.

```lean
-- Lean (book), textbook/checks/u33_lean.py
def ruleDelta : List Item := [.newForm 1, .newInst 0 [0], .newForm 1, .newRuleAll 1]
def ruled : Regime := ⟨2, [1, 1], [(0, [0])], [1], [(0, 1)]⟩

theorem ruleDelta_applies : applyDelta R2L ruleDelta = some ruled := by decide

theorem ruleDelta_valid : validResponse R2L 0 1 ruleDelta := by
  refine ⟨ruled, ruleDelta_applies, ?_, ?_⟩
  · exact ⟨⟨0, [none]⟩, by decide, by decide⟩
  · intro q hq
    have : q = (0, 1) := by
      cases hq with
      | head => rfl
      | tail _ h => cases h
    rw [this]
    exact ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem ruleDelta_dropped : dropRules ruleDelta = [.newForm 1, .newInst 0 [0], .newForm 1] := rfl

theorem ruleDelta_never_minimal :
    validResponse R2L 0 1 (dropRules ruleDelta) ∧
    (dropRules ruleDelta).length < ruleDelta.length ∧
    aritySum (dropRules ruleDelta) = aritySum ruleDelta :=
  rule_item_never_minimal (f := 1) (by decide) ruleDelta_valid

theorem bridge_example (rs : List Nat) :
    applyDelta ⟨2, [], [], rs, [(0, 1)]⟩ (dropRules ruleDelta)
      = some ⟨2, [1, 1], [(0, [0])], rs, [(0, 1)]⟩ :=
  applyDelta_dropRules rs ruleDelta_applies

theorem rule_on_mark_collapses : collapsed ⟨2, [1], [(0, [0])], [0], [(0, 1)]⟩ 0 1 := by
  intro c hc
  rw [one_unary_form_ctx_char _ rfl c] at hc
  subst hc
  decide
```

## Line-by-line Lean explanation

**`dropRules`.** Three equations. The middle one matches a rule item and
drops it; the last matches any other item and keeps it. Lean orders the
patterns, so the last line never sees a rule item.

**`applyDelta_dropRules`, the shape.** The statement quantifies `r`, `s`
and the replacement `rs` *inside* the induction, so that each step may
instantiate them anew. The base case: an empty delta returns its input,
so `s = r`, and the two sides are literally the same regime with rules
`rs`. The `cons` case rewrites `applyDelta (it :: rest)` as "apply `it`,
then `rest`" and splits on `it`.

*The rule case.* `simp only [applyItem] at h` exposes the guard `f <
r.forms.length`; `split at h` gives the two branches. If the guard held,
`h'` says the rest of the delta applies to `r` with `f` inserted into its
rules. The goal, after `show`, concerns `dropRules rest` (the rule item is
gone) applied to `r` with rules `rs`; the induction hypothesis, used at
the *changed* regime `{ r with rules := insertNew r.rules f }` and the
same `rs`, is exactly it, because that regime differs from `r` only in
the field the statement overrides. If the guard failed, `h` says `none =
some s`, impossible.

*The three other cases* (not reproduced) have one extra step: the guard
of a datum, form or instance is rewritten with `if_pos hg`, which is
possible because the guard mentions `data`, `forms` and `insts` but not
`rules`, so it reads the same on the regime with rules `rs`. That is the
"definitional" observation of the module header, done once per
constructor.

**`validResponse_dropRules`.** Open validity: the result `s`, the
application, the target separable, every demand separable. `hbridge` is
the master lemma at `rs := r.rules`: the drop applies and lands on `s`
with the *original* rules. `hsub`: the original rules are among `s`'s,
by monotonicity (`applyDelta_rules_mono`, itself a fold of
`applyItem_rules_mono`, whose rule case uses `mem_insertNew`). The new
result is `s` with rules `r.rules`; the application is `hbridge`; the
target and each demand are carried by `separable_of_subrules` with
`hsub`.

**`rule_item_never_minimal`.** A triple: the drop is valid (above),
strictly shorter (`dropRules_length_lt`, which needs the hypothesis that
some rule item is in `δ`; without it the drop could be the identity), and
of equal arity sum (`aritySum_dropRules`: rule items contribute nothing
to `aritySum`, which reads `newForm` only).

**The book's `ruleDelta`.** On `R2L`, two forms must be admitted before a
rule can be placed on a form that is *not* the one carrying the mark;
`ruleDelta` admits the mark's form, the mark, a second unary form and the
rule on it. `ruleDelta_applies` is decided; `ruleDelta_valid` follows the
pattern of `deltaU0F_valid`. The dropped delta is the three admissions,
by `rfl`. `ruleDelta_never_minimal` is Genesis's corollary at this delta:
three items against four, equal arity sum 2, and validity kept.
`bridge_example` is the master lemma with `rs` left free: for every rule
list, the drop applied to `R2L` with that rule list gives `ruled` with
that rule list.

**`rule_on_mark_collapses`.** With the rule on the mark's own form, the
one well-formed context (by `one_unary_form_ctx_char`, Unit 31) has both
pluggings derivable through the rule clause, so the pair is collapsed
again. This is why `separable_of_subrules` goes one way only: shrinking
the rules keeps separations, growing them may not.

**Axioms.** Every RuleBridge theorem reports `propext` alone: the proofs
are inductions and rewrites with no `decide` on concrete data. The book's
concrete instances report `propext, Quot.sound` where they decide.

## What has been proved

- Admission never removes a rule (Genesis, derived).
- The rule-free part of a delta applies over any rule field and yields
  the same regime up to `rules` (Genesis, derived; the bridge).
- Dropping rule items keeps validity (Genesis, derived).
- A delta with a rule item has a valid drop that is strictly shorter with
  equal arity sum (Genesis, derived).
- A concrete rule-bearing valid response to Challenge 3 and its drop
  (book Lean); the uniform rule on the mark's form collapses the pair
  again (book Lean).

## What has not been proved

- "Never a minimum under `mu2`" as a Lean statement. Lean has no `mu1` or
  `mu2`; the step from "shorter with equal arity sum" to "smaller under
  the lexicographic pair" is made in the docstring, over the Python
  definition. The audit records this as an interpretation point; the
  Python `mu2` is indeed lexicographic (`min_responses`, lines 376-420).
- That the enumeration applies the prune correctly. That is
  `test_rule_never_appears_in_minimum_responses` and this unit's check.
- A prohibition on rule items in non-minimal responses. Some are valid
  (30 of 35 rule-bearing candidates in this particular full two-item
  space); only their minimality under the declared measures is excluded.
- Anything about measures other than the two declared.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| structural recursion `dropRules` | the drop | metatheory |
| `induction δ`, `cases it`, `split at h`, `injection` | the bridge | metatheory tactics |
| `∀ {r s} (rs)` inside the induction | the parametrized invariant | metatheory quantification |
| `List.mem_cons`, `mem_insertNew` | monotonicity and length | metatheory |
| `decide` on `applyDelta R2L ruleDelta` | the book instance | metatheory; derived `DecidableEq` |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The rule list, as a list of form indices. A
rule is admitted like any other item and recorded; what it "means" is the
metatheory's `derivable`, which reads the list.

**Phrases to read with care.**

- "Rules are useless" is false; they are not *minimal*. A regime may
  carry rules for reasons the challenge sequence does not reward.
- "The bridge is obvious" is what "definitional" tempts one to say. It is
  an induction with four cases and a free parameter, and it was a test,
  not a theorem, until 2026-08-18.

## Student exercise

`applyDelta_dropRules` is stated for *any* replacement rule list `rs`,
but `validResponse_dropRules` only ever uses it at `rs := r.rules`. Why
not state the lemma for that case alone?

## Answer

<details>
<summary>Worked answer</summary>

The displayed induction needs a stronger invariant. In the `newRuleAll` case the
regime after the item has rules `insertNew r.rules f`, and the induction
hypothesis must be applied to *that* regime. A lemma fixed at "the
original regime's rules" would, at that step, need the statement for a
regime whose rules are not the original's. Quantifying `rs` separately
from `r` makes the invariant independent of what the rule field happens
to be at each step, so the hypothesis applies verbatim. The choice of
`rs := r.rules` is made once, at the end, where `separable_of_subrules`
needs the final rule set to be a subset of `s.rules`, and monotonicity
supplies exactly that. This explains this proof's generalization; it is
not a claim that no other proof of the restricted statement could work.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/RuleBridge.lean` lines 40-44, 46-93, 100-181, 183-238, 245-266; `Progress.lean` lines 195-205 |
| Axiom report | `artifacts/lean_axioms.txt`: `applyItem_rules_mono`, `applyDelta_rules_mono`, `applyDelta_dropRules`, `dropRules_length_le`, `dropRules_length_lt`, `aritySum_dropRules`, `validResponse_dropRules`, `rule_item_never_minimal`, `separable_of_subrules` all `[propext]` |
| Paper | `paper/paper.md` §8.3 (pruning lemmas) and §12 residual R4 (discharged 2026-08-18); ledger `CL-PRUNE-RULE` (i) theorem, (ii) theorem with the bridge; `paper/representative_selection.md` cites `rule_item_never_minimal` |
| Test | `tests/test_candidates.py::test_rule_never_appears_in_minimum_responses` |
| Check (Python) | `python textbook/checks/u33_rule_bridge.py`: no rule item in any `mu1` minimum on two bases; none generated by the pruned enumeration (85 deltas); in the full space (175 deltas) all 30 valid rule-bearing deltas have a valid, shorter, equal-arity drop; the uniform rule on the mark's form collapses `(0, 1)` |
| Check (book Lean) | `python textbook/checks/u33_lean.py`: eight book theorems plus four Genesis theorems kernel-checked, Lean 4.33.0 |
