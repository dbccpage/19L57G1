# Unit 35. A fresh mark answers a distinct pair under stated conditions

**Claim.** In a well-formed regime with all recorded demands already met, a
new unary form and one instance on a target datum give a valid response
for two distinct admitted data. This proves one response exists; it does
not prove it is cheapest or that a search procedure finds it.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** On any well-formed regime whose imposed demands are all met,
every supplied demand on two distinct admitted data has a valid response:
one fresh unary form, and one instance of it on the second datum
(`mark_progress`). The response applies, separates the target, and keeps
every imposed demand separated. This is response *existence* and nothing
more: it does not say where demands come from, and it does not say how
long the process runs.

**Status:** derived. **Lean:**
`Derivation.mark_progress` (`lean4/Derivation/Progress.lean` lines 75-193),
with `derivable_extend` (45-68), `getD_concat_self` (27-31),
`getD_append_lt` (34-41), `old_inst_form_lt` (22-24). **Axioms:** `propext,
Quot.sound` (`derivable_extend`: `propext`). **Depends on:** `Regime.wf`,
`wfCtx`, `derivable`, `separable`, `validResponse` (Units 08, 09, 18);
`applyItem` and its guards (Unit 17); the unary mark (Unit 22); the mention
lemma for the counterexample (Unit 30).

</details>

## First pass

Suppose two admitted data, A and B, need to be distinguished. The
current record is well formed, and all its recorded demands are met.

Admit a brand-new unary form `tag`, then admit only `tag(B)`. The new
question `tag(□)` gives No on A and Yes on B. Its form is new, so no old
instance or uniform rule already covers it. Old questions still have the
same answers, preserving the earlier demands.

Why keep the condition about earlier demands? Use three bare data A, B,
and C, with an unmet demand A/B. A new mark on C separates B/C, but A/B
still has two negative answers. This response fails validity because it
leaves an earlier demand unmet.

**Predict:** has that failure proved there is no response to B/C?

<details>
<summary>Check your prediction</summary>

No. Two different fresh forms, one marking A and the other marking C,
repair both demands in four items. Failure of one recipe is not failure
of every possible response.

</details>

The [Reasoning lab](../reasoning_lab/README.md) distinguishes an existence
claim from a claim about one particular witness.

## Question

Units 21 and 22 found the cheapest response to one demand on one regime.
The engine then keeps going: it imposes demand after demand and answers
each. Could it get stuck, with a demand that no delta answers? The engine
asserts not (`assert mr is not None, "progress lemma violated"`). This
unit is the proof behind the assertion, and the exact conditions under
which it holds.

## What we already possess

- `Regime.wf` (Basic line 64): instances name admitted forms with the right
  arity and admitted data, rules name admitted forms, demands are ordered
  pairs of admitted data, every form has arity at least one.
- `wfCtx r c`: the context's form is admitted, its slot count is the
  form's arity, it has a hole, its filled slots are admitted data (Basic
  106-110). `plug c d` fills every hole with `d` (80).
- `derivable r i := i ∈ r.insts ∨ i.1 ∈ r.rules` (85).
- `separable r d d' := ∃ c, wfCtx r c ∧ ¬ (derivable r (plug c d) ↔
  derivable r (plug c d'))` (123-125).
- `validResponse r i j δ := ∃ s, applyDelta r δ = some s ∧ separable s i j
  ∧ ∀ q ∈ r.reqs, separable s q.1 q.2` (198-200).
- `insertNew_of_not_mem`: inserting a new element appends it (Unit 17).

## New concept: a response that exists everywhere, by construction

The response is always the same shape: admit a unary form, which gets
the next free index `r.forms.length`, and admit one instance of it on the
datum `j`. Three things must then be shown about the result.

1. *It applies.* The form guard is `1 ≤ 1`. The instance guard asks that
   the form index be below the new form count, that the argument list
   have the form's arity (read at index `r.forms.length` of the extended
   table, which is where `getD_concat_self` is needed) and that `j` be an
   admitted datum.
2. *It separates `i` from `j`.* The witness context is the fresh form with
   one hole. Plugging `j` gives exactly the new instance, derivable.
   Plugging `i` gives `(fresh, [i])`, which is not among the old instances
   (they all name older forms, by well-formedness), is not the new
   instance (because `i ≠ j`), and is not covered by a rule (the rules all
   name older forms). So the two pluggings differ in derivability.
3. *It keeps every imposed demand separated.* An imposed demand `q` had a
   witness context `c` in `r`. That context's form is an old one, so
   `derivable_extend` says derivability of its pluggings is unchanged by
   the extension, and the same `c` witnesses `q` in the result.

The proof uses `hwf` for old instance and rule bounds, `hj` for the
instance guard, `hij` for the target witness, and `hreqs` for step 3.
The displayed body never uses `hi`: the statement deliberately keeps
both targets admitted, but the raw definitions allow plugging a hole with
any natural number. The book even proves a raw example with first target
7 and only one admitted datum. Thus “every stated hypothesis is logically
necessary” would be too strong. The stale-rule, unmet-demand, and
self-pair examples explain three actual failure modes.

## Plain-language interpretation

Whatever has been said so far, and whatever has been demanded and met,
there is always one more thing you can say that tells two named objects
apart: invent a brand-new one-place predicate and apply it to one of
them. It is new, so nothing already said interferes with it; it is
applied to one object and not the other, so it separates them; and it
touches none of the old predicates, so every distinction already drawn
survives. This argument assumes a well-formed regime and two distinct
admitted data. It also assumes every recorded demand is already met. A
malformed record can contain a rule referring to the supposedly fresh
form before that form exists; admitting the form then activates the rule
and ruins the proposed distinction. The book checks this raw-record
counterexample separately from valid admission histories.

If an earlier demand is unmet, this particular two-item response may fail
validity. That does not prove no response exists: a longer response might
repair both demands. The check gives such a four-item repair.

What this does not say: that anyone will make the demand. The regime does
not generate demands; they are imposed from outside (Unit 28's closure
policy is a declared policy, not a theorem). Nor does it say the process
ends. The supplied finite trees reach their round cap; they do not prove
an infinite execution (Unit 34).

## Pseudocode

```
# Gloss
given: r well-formed; i, j < r.data; i ≠ j; every q in r.reqs separable in r
let f := r.forms.length                       -- the next free form index
delta := [newForm 1, newInst f [j]]
result s := r with forms ++ [1], insts ++ [(f, [j])]
show applyDelta r delta = some s              -- the two guards hold
show separable s i j                          -- context (f, [hole]):
                                               --   plug j = (f,[j]) derivable
                                               --   plug i = (f,[i]) not derivable
show ∀ q ∈ r.reqs, separable s q.1 q.2        -- the old witness still works:
                                               --   its form is old, so
                                               --   derivable_extend applies
```

## Python

```python
from derivation.candidates import NewForm, NewInst, apply_delta, response_valid_naive
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, replay
from derivation.observe import collapsed_pairs, separable, satisfies

def mark(r, j):
    return (NewForm(1), NewInst(len(r.forms), (j,)))

mixed = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1),
                AdmitForm(1), AdmitForm(2), AdmitInst(0, (1,)), AdmitInst(1, (0, 2))])
print(satisfies(mixed), all(response_valid_naive(mixed, (i, j), mark(mixed, j))
                            for i in range(3) for j in range(3) if i < j))
unmet = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1)])
s = apply_delta(unmet, mark(unmet, 2))
print(separable(s, 1, 2), separable(s, 0, 1), response_valid_naive(unmet, (1, 2), mark(unmet, 2)))
print(separable(s, 1, 1))
```

Output:

```text
True True
True False False
False
```

The check script also runs the bare three-datum regime and `U0`, tests
the mark on either datum of each pair, and inspects both engine trees:

```text
bare3: 3 data, forms [], imposed demands met: True; fresh mark on either datum valid for all 3 pairs: True; after the mark on datum 1: forms [1], 1 instances, collapsed pairs ((0, 2),)
U0: 2 data, forms [1], imposed demands met: True; fresh mark on either datum valid for all 1 pairs: True; after the mark on datum 1: forms [1, 1], 2 instances, collapsed pairs ()
reading L tree: statuses {'expanded': 68, 'frontier_guard': 141}; terminal_no_response present: False
reading F tree: statuses {'expanded': 56, 'frontier_guard': 153}; terminal_no_response present: False
```

## Line-by-line Python explanation

`mark(r, j)` is the Lean delta with `len(r.forms)` for `r.forms.length`:
the index the new form will receive.

`mixed` is a regime with two forms and two instances in which the one
imposed demand `(0, 1)` is met (`satisfies` is the Python for "every
imposed demand separable"). For every pair `i < j` the mark on `j` is a
valid response. The Python imposes only ordered pairs, which is why the
loop runs over `i < j`; Lean's theorem asks only `i ≠ j`, and the check
confirms the mark on `i` works too, since separability is symmetric.

`unmet` has the demand `(0, 1)` imposed and not met. The mark on datum 2
separates `(1, 2)`, the target, but leaves `(0, 1)` collapsed, so
`response_valid_naive` says `False`: the third conjunct of validity fails.
That is hypothesis `hreqs` doing work. The last line is hypothesis `hij`:
no context separates a datum from itself.

In the engine trees (the full policy, with supply, 200-node guard) no node
has status `terminal_no_response`. That status exists in the code
(`engine.py` line 527). The engine's own test
`test_tree_terminal_when_no_response_within_bounds` builds a tree with
`max_items=0` and finds the status at the root. Within the declared
bounds (two items, arity at most two), which contain the fresh mark, the
theorem supplies a valid delta on a well-formed regime whose demands are
met. The observed status also depends on the Python enumerator finding
that response; Lean does not verify the enumerator. Both finite trees
pass that separate check.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Progress.lean lines 45-49 (statement)
theorem derivable_extend {r : Regime} (hwf : r.wf) (j : Nat) (x : Inst)
    (hx : x.1 ≠ r.forms.length) :
    derivable
      ⟨r.data, r.forms ++ [1], r.insts ++ [(r.forms.length, [j])],
       r.rules, r.reqs⟩ x ↔ derivable r x
```

```lean
-- Lean (Genesis), lean4/Derivation/Progress.lean lines 75-84, 119-145, 162-193
theorem mark_progress (r : Regime) (hwf : r.wf) (i j : Nat)
    (hi : i < r.data) (hj : j < r.data) (hij : i ≠ j)
    (hreqs : ∀ q ∈ r.reqs, separable r q.1 q.2) :
    validResponse r i j [.newForm 1, .newInst r.forms.length [j]] := by
  have hfresh : ((r.forms.length, [j]) : Inst) ∉ r.insts := by
    intro hmem
    exact Nat.lt_irrefl _ ((hwf.1 _ hmem).1)
  have happ : applyDelta r [.newForm 1, .newInst r.forms.length [j]] =
      some ⟨r.data, r.forms ++ [1],
            r.insts ++ [(r.forms.length, [j])], r.rules, r.reqs⟩ := by
    ...
  refine ⟨_, happ, ?_, ?_⟩
  · -- the fresh context separates i from j
    refine ⟨⟨r.forms.length, [none]⟩, ⟨by simp, ?_, by simp, ?_⟩, ?_⟩
    · show ([none] : List (Option Nat)).length =
        (r.forms ++ [1]).getD r.forms.length 0
      rw [getD_concat_self]
      rfl
    · intro sl hsl
      have : sl = none := by
        cases hsl with
        | head => rfl
        | tail _ h => cases h
      rw [this]; trivial
    · intro hiff
      have hderj : derivable
          ⟨r.data, r.forms ++ [1], r.insts ++ [(r.forms.length, [j])],
           r.rules, r.reqs⟩
          (plug ⟨r.forms.length, [none]⟩ j) := by
        show derivable _ (r.forms.length, [j])
        exact Or.inl (List.mem_append.mpr (Or.inr (by simp)))
      have hderi := hiff.mpr hderj
      show False
      have hne : (r.forms.length, [i]) ≠ (r.forms.length, [j]) := by
        intro h
        have := congrArg (fun p => p.2) h
        simp at this
        exact hij this
      cases hderi with
      | inl h => ...   -- an old instance names an old form; or it is the new one, and i ≠ j
      | inr h => ...   -- a rule names an old form
  · -- every imposed requirement stays separated
    intro q hq
    have hsep := hreqs q hq
    cases hsep with
    | intro c hc =>
      have hwfc := hc.1
      have hne := hc.2
      have hform : c.form ≠ r.forms.length := by
        intro hbad
        exact Nat.lt_irrefl _ (hbad ▸ hwfc.1)
      have hplug : ∀ d, (plug c d).1 ≠ r.forms.length := by
        intro d
        show c.form ≠ r.forms.length
        exact hform
      refine ⟨c, ⟨?_, ?_, hwfc.2.2.1, hwfc.2.2.2⟩, ?_⟩
      · show c.form < (r.forms ++ [1]).length
        have := hwfc.1
        simp
        omega
      · show c.slots.length = (r.forms ++ [1]).getD c.form 0
        rw [getD_append_lt _ _ _ hwfc.1]
        exact hwfc.2.1
      · intro hiff
        apply hne
        constructor
        · intro h
          exact (derivable_extend hwf j _ (hplug q.2)).mp
            (hiff.mp ((derivable_extend hwf j _ (hplug q.1)).mpr h))
        · intro h
          exact (derivable_extend hwf j _ (hplug q.1)).mp
            (hiff.mpr ((derivable_extend hwf j _ (hplug q.2)).mpr h))
```

The book's Lean applies the theorem at two regimes, and states the two
hypotheses' failures as theorems.

```lean
-- Lean (book), textbook/checks/u35_lean.py
theorem U0_wf : U0.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [U0]

theorem U0_reqs_met : ∀ q ∈ U0.reqs, separable U0 q.1 q.2 := by
  intro q hq
  have : q = (0, 1) := by
    cases hq with
    | head => rfl
    | tail _ h => cases h
  subst this
  exact ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem second_mark_valid :
    validResponse U0 0 1 [.newForm 1, .newInst U0.forms.length [1]] :=
  mark_progress U0 U0_wf 0 1 (by decide) (by decide) (by decide) U0_reqs_met

theorem unmet_demand_blocks :
    ¬ validResponse ⟨3, [], [], [], [(0, 1)]⟩ 1 2 [.newForm 1, .newInst 0 [2]] := by
  rintro ⟨s, hs, -, hall⟩
  have happ : applyDelta (⟨3, [], [], [], [(0, 1)]⟩ : Regime) [.newForm 1, .newInst 0 [2]]
      = some ⟨3, [1], [(0, [2])], [], [(0, 1)]⟩ := by decide
  rw [happ] at hs
  injection hs with hs
  subst hs
  have hsep := hall (0, 1) (by simp)
  have base : collapsed (⟨3, [1], [], [], [(0, 1)]⟩ : Regime) 0 1 :=
    collapsed_of_no_insts _ rfl 0 1
  have hcol : collapsed (⟨3, [1], [(0, [2])], [], [(0, 1)]⟩ : Regime) 0 1 :=
    (collapsed_append_unmentioning ⟨3, [1], [], [], [(0, 1)]⟩
      [(0, [2])] 0 1 (by decide) (by decide)).mpr base
  exact separable_not_collapsed hsep hcol

theorem no_self_separation (r : Regime) (d : Nat) : ¬ separable r d d :=
  fun ⟨_, _, h⟩ => h Iff.rfl

theorem no_self_response (r : Regime) (d : Nat) (δ : List Item) :
    ¬ validResponse r d d δ :=
  fun ⟨s, _, hsep, _⟩ => no_self_separation s d hsep
```

## Line-by-line Lean explanation

**`derivable_extend`.** For an instance `x` whose form is *not* the fresh
one, derivability in the extended regime and in `r` agree. Its proof
unfolds `derivable` and splits the membership in `r.insts ++ [new]`: the
new instance is excluded by `hx`, and the rules are unchanged.

**`mark_progress`, the set-up.** `hfresh`: the new instance is not already
in `r.insts`, because every old instance names a form below
`r.forms.length` (the first conjunct of `hwf`), and `Nat.lt_irrefl` rules
out `r.forms.length < r.forms.length`. `happ` (elided) computes the
application step by step: the form guard by `omega`, the instance guard
as `hcond` (its middle conjunct is where `getD_concat_self` reads the new
form's arity at the old length), then `insertNew_of_not_mem hfresh` to
turn the insertion into an append, and a `calc` that unfolds the fold of
`applyDelta` over two items.

**The target, bullet one.** The witness is `⟨r.forms.length, [none]⟩`.
Its well-formedness has four parts: the form index is below the extended
length (`simp`), the slot count is the arity read at that index
(`getD_concat_self` again, then `rfl` for `1 = 1`), a hole is present
(`simp`), every filled slot is admitted (there is none; `trivial`). Then
`intro hiff`, assuming the pluggings agree. `hderj`: plugging `j` is the
new instance, which is in the appended list. `hderi`: by the assumed
iff, plugging `i` is derivable too. `hne`: the two instances differ,
because `i ≠ j` (read off the second components). `cases hderi`: if
`(fresh, [i])` is an instance, it is either old, impossible since old
instances name old forms, or the new one, contradicting `hne`; if it is
covered by a rule, the rule names an old form, impossible.

**The demands, bullet two.** For `q` imposed, `hreqs` gives a witness
`c`. `hform`: its form is old. `hplug`: so is the form of either plugging
(plugging does not change the form). The same `c` is well formed in the
extended regime (`omega` for the length, `getD_append_lt` because reading
below the old length is unaffected by the append, the last two parts
unchanged). Finally, if the pluggings agreed in the extended regime,
`derivable_extend` would transport the agreement back to `r`, against
`hne`.

**Book: `U0_wf`, `U0_reqs_met`, `second_mark_valid`.** The unary mark is
well formed (`simp` on each conjunct, as `R2L_wf` is proved in Basic);
its one demand is met by the context `⟨0, [none]⟩`; so the theorem gives
a *second* mark, on datum 1 with the fresh index `1`, as a valid
response to the already-met demand. Nothing says the demand must be new;
`ClosedRun.cons` (Unit 34) adds the freshness condition. `respond` alone
does not: its insertion silently absorbs an existing demand.

**Book: `unmet_demand_blocks`.** Open validity keeping the third
conjunct. Decide the application; identify `s`. `hall (0, 1)` says the
unmet demand is separated in the result. But the result is the
instance-less three-datum regime with one instance appended that
mentions only datum 2, so by `collapsed_of_no_insts` and the mention
lemma `(0, 1)` is still collapsed, and `separable_not_collapsed` closes.
This is a counterexample to extending the *specific fresh-mark recipe*
without its old-demand hypothesis. It is not a counterexample to the
existence of every possible response. The book proves that fresh marks
on data 0 and 2, using two different forms, repair both pairs in this
same record.

**Book: `stale_rule_breaks_mark`.** The raw record has two data, no forms,
and rule index 0. It violates `wf`. Admitting form 0 and marking datum 1
applies, but the stale rule now makes every instance of that form
derivable, so the pair remains collapsed. This is why well-formedness
cannot simply be omitted from the recipe's guarantee.

**Book: `no_self_separation`, `no_self_response`.** A separability
witness for `(d, d)` would have to refute `derivable (plug c d) ↔
derivable (plug c d)`, which is `Iff.rfl`. So `validResponse r d d δ` is
false for every `r` and `δ`. The hypothesis `hij` is not a convenience.

**Axioms.** `mark_progress` reports `propext, Quot.sound` through `simp`
and `omega`; `derivable_extend` reports `propext` only. The book's
`no_self_separation` and `no_self_response` report `propext`; the concrete
unmet-demand and stale-rule refutations report `propext, Quot.sound`.
Destructuring an existence statement in a proof does not itself require
`Classical.choice`.

## What has been proved

- The fresh-mark delta applies under the theorem's well-formedness and
  target-range hypotheses (Genesis).
- In that setting it separates the two distinct admitted target data
  (Genesis).
- It keeps every imposed demand that was met (Genesis).
- Therefore it is a valid response under the four hypotheses (Genesis,
  derived; ledger `CL-PROGRESS`).
- With an unmet imposed demand, the same delta is not a valid response;
  with `i = j`, nothing is (book Lean).
- The unmet-demand example has a longer valid repair; a raw stale-rule
  example defeats the fresh mark when well-formedness is dropped (book Lean).

## What has not been proved

- Anything about *which* demand comes next, or that one comes at all.
  The paper's §10.7 summary says "every supplied demand has a response"
  without the hypotheses; the audit records that as an interpretation
  defect in a summary sentence (the full statement in §8.2 and the ledger
  carries them).
- That the response is cheapest. It is two items; on `R2L` that is the
  minimum (Units 18 and 21), on a regime that already has a usable unary form a
  single instance may do (Unit 36's check finds a `mu2` minimum of
  `(1, 0)` on such a regime).
- That the response is well formed in the sense of `wf`. The result *is*
  well formed, but the theorem does not state it; `Rounds` and the
  engine's own invariants carry that separately.
- That the process terminates. With supply, the trees run to the round
  cap; the only termination theorem is the closed one (Unit 34).
- That the engine's declared `Bounds` contain the response. They do (two
  items, arity at most two, includes the mark), but that is a parameter
  choice outside the theorem; with `max_items=0` the root stops with
  `terminal_no_response`, as the engine's own test shows.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `r.forms.length` as the fresh index | naming the new form | metatheory `Nat`; the regime's own form count |
| `getD`, `List.mem_append`, `Nat.lt_irrefl` | the guards and the case splits | metatheory |
| `omega`, `simp`, `calc` | arithmetic and unfolding | metatheory tactics |
| `collapsed_append_unmentioning` | the book counterexample | a Genesis theorem of Unit 30 |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The regime before and after: one more form,
one more instance. The demand `(i, j)` is not written into the regime by
this theorem; `validResponse` reads `r.reqs` for the *old* demands and
takes the target as two numbers. Writing the new demand is `respond`'s
job (Unit 34).

**Phrases to read with care.**

- "Progress" means a response exists, not that anything progresses. The
  engine's name for the assertion is "progress lemma"; the paper and
  ledger say "response existence only".
- "Preserves every existing separation" was the earlier wording, narrowed
  on 2026-08-18: the theorem preserves the *imposed* demands. A separable
  pair that nobody demanded may be collapsed by some other response; this
  one happens to preserve all of them (it touches nothing old), but that
  is not what is stated.

## Student exercise

`mark_progress` puts the instance on `j`, the second datum of the demand.
Would the theorem hold with the instance on `i` instead? Would it hold
with the instance on some third datum `k`, admitted and different from
both?

## Answer

<details>
<summary>Worked answer</summary>

On `i`: yes, by the same proof with the roles of `i` and `j` exchanged
in the witness argument (plugging `i` is the new instance, plugging `j`
is not); the check script confirms it on every pair. On a third datum
`k`: there is no general guarantee. The fresh context has
`plug c i = (fresh, [i])` and `plug c
j = (fresh, [j])`, neither of which is the new instance `(fresh, [k])`,
so both are underivable and the context does not separate `i` from `j`;
and no old context can, if they were collapsed before. Unit 32's
`genesis_mark_not_separable` is exactly this failure with `k = 0`, `(i, j)
= (1, 2)`. If the target pair was already separated and the other
hypotheses hold, a mark on a third admitted datum can be valid: the old
witness still works. The failure concerns a target that needed repair.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Progress.lean` lines 22-68 (helpers), 75-193 (`mark_progress`) |
| Axiom report | `artifacts/lean_axioms.txt`: `mark_progress` `[propext, Quot.sound]`; `separable_of_subrules` `[propext]` |
| Paper | `paper/paper.md` §8.2 (**[theorem]** `mark_progress`, response existence only) and §10.7; ledger `CL-PROGRESS` (narrowed 2026-08-18) |
| Engine | `code/derivation/engine.py` line 261, `assert mr is not None, "progress lemma violated"`; the test with a zero-item bound reaches `terminal_no_response` (line 527); neither sampled tree in this unit reaches it |
| Tests | `tests/test_candidates.py::test_c3_cost1_all_fail_and_min_is_two`; `tests/test_engine.py::test_tree_terminal_when_no_response_within_bounds` |
| Check (Python) | `python textbook/checks/u35_progress.py`: the fresh mark on either datum is valid for every pair on three regimes with their demands met; an unmet imposed demand blocks it; a datum is never separable from itself; neither engine tree has a `terminal_no_response` node |
| Check (book Lean) | `python textbook/checks/u35_lean.py`: twelve book theorems plus three Genesis theorems kernel-checked, Lean 4.33.0 |
