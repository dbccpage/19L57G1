# Unit 10. Without instances, everything is collapsed

**Claim.** In any regime with no admitted instances, every pair of data is
collapsed, whatever forms and rules it has. In particular the two
Challenge-2 regimes are totally collapsed: ⟨A⟩ and ⟨AB⟩, externally distinct, give the same answers to all admitted context
tests. Their internal datum indices remain distinct.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** derived. **Lean:**
`Derivation.collapsed_of_no_insts`, instantiated as `R2L_collapsed` and
`R2F_collapsed` (`lean4/Derivation/Inertia.lean` lines 37-55).
**Axioms:** `propext`. **Depends on:** `derivable` (Unit 01), `collapsed`,
`plug` (Unit 08), `R2L`, `R2F` (Units 01, 05).

</details>

## First pass

With no forms, there are no questions to distinguish two data.
Add the one-place form marked, but no instance: both answers are
not derivable. Now add a uniform rule saying marked holds for every
datum. Predict whether 0 and 1 become distinguishable.

They do not. Both answers change to derivable, so they still agree.
A blanket rule changes what can be derived without favoring one datum.
With no instances, the same reasoning works for every form and every pair.

An admitted instance is therefore necessary for a separation in this
grammar, but not sufficient by itself. Adding `marked(0)` under that
already uniform rule leaves both answers derivable. Collapse concerns
answers, not equality of internal indices.

## Question

After Challenge 2 the ledger holds two (or three) data that the metatheory
can tell apart by their tokens. Can the system tell any of them apart? And
would admitting forms, or even a rule, help?

## What we already possess

- `derivable r i := i ∈ r.insts ∨ i.1 ∈ r.rules` (Unit 01).
- `collapsed r d d'`: every well-formed context plugs to equi-derivable
  instances (Unit 08).
- The Challenge-2 regimes have no forms, no instances, no rules
  (Unit 05); so they have no contexts at all.

## New concept: a uniform rule floods

A **uniform rule** on a form makes every instance of that form derivable,
whatever its arguments. So a rule can make a context derivable, but it does
so for *every* datum plugged in. It cannot prefer one datum to another.
With no instances, derivability depends on the form alone, never on the
arguments, and so never on which datum was plugged.

The theorem is a little stronger than "no contexts, no separation". It
says: even if forms and rules are admitted, as long as no *instance* is,
every pair stays collapsed. A separation therefore requires some admitted instance in this
grammar. Merely having an instance does not guarantee separation: a
uniform rule on its form may already grant the same answer for everyone.

## Plain-language interpretation

Imagine stencils with holes but no sentences yet written in the notebook.
Holding a stencil over any datum gives a sentence that is not in the book:
same answer for all. Now add a rule: "every sentence of this stencil's
shape is granted." Holding it over any datum now gives a granted sentence:
again the same answer for all. Rules are blanket grants; they do not single
out. What singles out is a written sentence naming a particular datum, and
there are none.

For the derivation this is the collapse that Challenge 3 will demand be
broken. It is also the fact behind the paper's countermodel in §6:
admitting a fresh datum is a real change of state and yet leaves the
collapsed pair collapsed (Unit 12).

## Pseudocode

```
# Gloss
given: no instances
for any context c and data d, d':
    derivable(plug(c, d))   =  (form of c has the rule)     -- args ignored
    derivable(plug(c, d'))  =  (form of c has the rule)
    same answer.  so c does not separate d from d'.
therefore every pair is collapsed.
```

## Python

```python
from derivation.engine import GENESIS_F, GENESIS_L
from derivation.model import AdmitDatum, AdmitForm, AdmitRuleAll, replay
from derivation.observe import collapsed_pairs, profiles

print(collapsed_pairs(replay(GENESIS_L)), collapsed_pairs(replay(GENESIS_F)))
r = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1), AdmitRuleAll(0)])
print(profiles(r), collapsed_pairs(r))
```

Output:

```text
((0, 1),) ((0, 1), (0, 2), (1, 2))
(frozenset({(0, (None,))}), frozenset({(0, (None,))})) ((0, 1),)
```

## Line-by-line Python explanation

`collapsed_pairs(replay(GENESIS_L))`: replay reading L's history (two
data, nothing else) and list the pairs with equal profiles. There is one
pair, `(0, 1)`, and it is collapsed. Reading F has three data, so three
pairs, all collapsed.

`r = replay([... AdmitForm(1), AdmitRuleAll(0)])`: two data, one unary
form, and the uniform rule on it. No instance.

`profiles(r)`: a tuple with one profile per datum. Both are the same set,
holding the single unary context: under the rule, the plugging of either
datum is derivable. Equal profiles, so `collapsed_pairs(r)` is `((0, 1),)`
again. The rule added a derivable context for both data and separated
nothing.

The check script runs this over 76 instance-free regimes with up to three
data, six form tables and every subset of rules, and finds every pair
collapsed and at most one distinct profile per regime.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean lines 37-55
/-- Key collapse lemma: with no admitted instances, derivability depends
only on the form, hence every pair of data is observationally collapsed
(uniform rules cannot separate). -/
theorem collapsed_of_no_insts (r : Regime) (hi : r.insts = [])
    (d d' : Nat) : collapsed r d d' := by
  intro c _
  constructor <;> intro h <;>
    cases h with
    | inl h => rw [hi] at h; cases h
    | inr h => exact Or.inr h

/-- Challenge 2 (reading L): the two admitted, externally distinct data are
observationally collapsed. -/
theorem R2L_collapsed : collapsed R2L 0 1 :=
  collapsed_of_no_insts R2L rfl 0 1

/-- Challenge 2 (reading F): all three pairs are collapsed. -/
theorem R2F_collapsed (d d' : Nat) : collapsed R2F d d' :=
  collapsed_of_no_insts R2F rfl d d'
```

The book's Lean unfolds the combinator `<;>` into its two halves, and adds
the rule example and the contrast.

```lean
-- Lean (book), textbook/checks/u10_lean.py
theorem collapsed_of_no_insts' (r : Regime) (hi : r.insts = [])
    (d d' : Nat) : collapsed r d d' := by
  intro c _
  constructor
  · intro h
    cases h with
    | inl hmem => rw [hi] at hmem; cases hmem
    | inr hrule => exact Or.inr hrule
  · intro h
    cases h with
    | inl hmem => rw [hi] at hmem; cases hmem
    | inr hrule => exact Or.inr hrule

def ruled : Regime := ⟨2, [1], [], [0], [(0, 1)]⟩
theorem ruled_both_derivable :
    derivable ruled (plug ⟨0, [none]⟩ 0) ∧ derivable ruled (plug ⟨0, [none]⟩ 1) := by
  decide
theorem ruled_collapsed : collapsed ruled 0 1 := collapsed_of_no_insts ruled rfl 0 1
theorem one_inst_separates : separable U1 0 1 := U1_separable
```

## Line-by-line Lean explanation

**The statement.** Any regime `r`, a hypothesis `hi` that its instance
list is empty, any two data `d`, `d'` (any numbers at all; they need not
even be admitted, since `collapsed` only asks about well-formed contexts).
Conclusion: `collapsed r d d'`.

`intro c _`: `collapsed` is a `∀` followed by an implication, so take an
arbitrary context `c` and the proof that it is well formed. The underscore
discards that proof: the argument will not need well-formedness. The goal
is now `derivable r (plug c d) ↔ derivable r (plug c d')`.

`constructor`: an `↔` is two implications; prove each.

`<;>`: "and then, on every goal just produced". So `constructor <;> intro h`
assumes the left side in the first goal and the right side in the second,
and `<;> cases h with ...` splits each assumed `derivable` into its two
disjuncts. The book version writes the two goals out with `·` bullets.

`| inl hmem => rw [hi] at hmem; cases hmem`: the first disjunct says the
plugged instance is a member of `r.insts`. `rw [hi] at hmem` rewrites
`r.insts` to `[]` in that fact, giving membership in the empty list.
`cases hmem`: there is no way to be a member of `[]`, so this case has no
constructors and is closed. This is the only place the hypothesis is used.

`| inr hrule => exact Or.inr hrule`: the second disjunct says the form of
the plugged instance carries the rule. The form of `plug c d` is `c.form`,
and so is the form of `plug c d'`: plugging changes the arguments, not the
form. So the same `hrule` proves the second disjunct for the other
plugging. `Or.inr` picks that disjunct. Lean accepts `hrule` for both sides
because `(plug c d).1` and `(plug c d').1` both reduce to `c.form` by
computation.

**`R2L_collapsed`.** Apply the lemma to `R2L` with `rfl` for the hypothesis
(`R2L.insts` is `[]` by definition) and the pair `0 1`. **`R2F_collapsed`**
likewise for any `d d'`.

**`ruled_both_derivable`.** On the regime with the rule, `decide` computes
both pluggings derivable. **`ruled_collapsed`** is the lemma again: the rule
is irrelevant to collapse. **`one_inst_separates`** is the contrast: the
regime `U1` differs from `ruled` by having an instance instead of a rule,
and it is separable (Unit 09). So the hypothesis `r.insts = []` is doing
real work; the book check also proves `U1.insts ≠ []`.

**Axioms.** `collapsed_of_no_insts`, `R2L_collapsed` and `R2F_collapsed`
report `propext`, inherited from the definitions. The ledger notes that an
earlier version recorded the two instantiations as axiom-free and was
corrected on 2026-08-18 against the artifact (`CL-2-COLLAPSED`).

## What has been proved

- Every regime with no instances has every pair of data collapsed, forms
  and rules notwithstanding (Genesis, derived).
- Both Challenge-2 regimes are totally collapsed (Genesis, derived).
- A uniform rule makes the context derivable for both data and separates
  nothing; one instance separates (book Lean, derived on examples).

## What has not been proved

- That instances are the *only* thing that can ever separate. In this
  grammar, yes: derivability has two disjuncts and the rule disjunct is
  uniform. A grammar with other inference would need its own theorem.
- That the collapse is a defect. It is the declared starting situation:
  nothing has been said about particular data, so nothing distinguishes
  them. Challenge 3 turns it into a demand (Unit 17).
- That the collapsed pair is "really the same". Externally the tokens
  differ; the ledger counts two. Collapse is an internal, behavioral
  statement (Unit 08).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `(r : Regime) (d d' : Nat)` | the universal statement | metatheory quantifiers |
| `rw`, `cases` on `List.Mem` | the proof | metatheory proof steps about Lean's lists |
| `propext` | inherited | inside the declared boundary |

**What the system holds.** Immediately after Challenge 2, the
admitted observation fields contain only the data count: no form, no
instance, and no rule. The Lean states named `R2L` and `R2F` also record
the later Challenge-3 demand in `reqs`; the Python base histories do not.
Recording that demand creates no context or distinguishing instance. The system
holds nothing that could tell two data apart, and the theorem says that
adding forms and rules alone would not change that.

**Phrases to read with care.**

- "The system cannot yet see any difference" is right if "see" means
  separate in Unit 08's sense. It does not mean the system is looking.
- "Uniform rules cannot separate" is the theorem's content and is
  specific to *uniform* (all-tuples) rules, the only kind Genesis admits.

## Student exercise

Regime: three data, forms `[2]`, the rule on form 0, no instances. How
many well-formed contexts are there, what is each datum's profile, and
which pairs are collapsed?

## Answer

Arity 2 over 3 data: `4² − 3² = 7` contexts. Under the rule every plugging
of form 0 is derivable, so each datum's profile is the full set of 7
contexts, and all three profiles are equal. All three pairs, `(0, 1)`,
`(0, 2)`, `(1, 2)`, are collapsed, by `collapsed_of_no_insts` with
`hi := rfl`. (The check script includes this regime among its 76.)

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Inertia.lean` lines 37-55 |
| Axiom report | `artifacts/lean_axioms.txt`: `collapsed_of_no_insts`, `R2L_collapsed`, `R2F_collapsed` each `[propext]` |
| Paper | `paper/paper.md` §5 third bullet and §6 second bullet (**[theorem]**) |
| Ledger | `paper/paper_claim_ledger.md`, `CL-1-SUPPLY-NOT-ADMISSION`, `CL-2-COLLAPSED` (with the 2026-08-18 axiom correction) |
| Artifact | `artifacts/challenges.json`, `challenge2` (observational classes = 1) |
| Check (Python) | `python textbook/checks/u10_no_insts.py`: 76 instance-free regimes, 76 pairs, all collapsed, at most one profile each; `GENESIS_L` one collapsed pair, `GENESIS_F` three; one instance separates |
| Check (book Lean) | `python textbook/checks/u10_lean.py`: six book theorems plus the three Genesis theorems kernel-checked, Lean 4.33.0; `propext` throughout, `propext, Quot.sound` where `decide` touches a concrete list, `U1_has_inst` no axioms |
