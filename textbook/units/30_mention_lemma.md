# Unit 30. A context that reaches outside the regime separates nothing

**Claim.** Adding instances that mention neither `d` nor `d'` leaves the
collapse of the pair `(d, d')` exactly as it was: `collapsed { r with insts
:= r.insts ++ new } d d' ↔ collapsed r d d'` whenever no instance in `new`
mentions `d` or `d'` (R3, the mention lemma). Two corollaries follow by the
same argument: admitting a fresh datum (R1, Unit 12) or a fresh form that
no instance uses and no rule names (R2) changes no existing pair's
collapse. **Status:** derived. **Lean:** `Derivation.mem_plug_of_hole`
(`lean4/Derivation/Mention.lean` line 40), `not_mem_of_arg_out_of_range`
(47), `exists_out_of_range_slot` (56), `collapsed_append_unmentioning`
(88-110), `collapsed_fresh_datum` (124), `getD_append_left` (157),
`collapsed_fresh_form` (168-187). **Axioms:** `propext, Quot.sound` for
R3 and R1; `propext` for R2. **Depends on:** contexts, plugging,
derivability, collapse (Unit 08); `collapsed_of_no_insts` (Unit 10); the
fresh-datum corollary already taught (Unit 12); the cost-2 enumeration
(Unit 18).

## Question

Genesis's enumeration of two-item responses prunes most candidates
before testing them (Unit 18). One pruning rule says: if a candidate adds
only instances, and none of them mentions a datum of the demanded pair,
skip it. Why is that safe? The same question for a candidate that adds a
datum nothing refers to, or a form nothing uses. If the pruning were
unsound, a cheapest response could be missed and the minimality results of
Units 18 to 22 would rest on a gap.

## What we already possess

- A well-formed context has at least one hole (`none ∈ c.slots` is a
  conjunct of `wfCtx`, Unit 08). Plugging fills every hole with the
  datum.
- `derivable r i` is `i.1 ∈ r.rules ∨ i ∈ r.insts` (Unit 08).
- `collapsed_of_no_insts` (Unit 10): with no instances, every pair is
  collapsed.
- R1, `collapsed_fresh_datum`, taught in Unit 12 as "a fresh datum adds no
  power". This unit places it beside its siblings.
- The pruned enumeration `iter_cost2_deltas` and the unpruned
  `iter_full_deltas` (Unit 18).

## New concept: mention

An instance *mentions* a datum when the datum is among its arguments.
The lemma that drives everything is one line: every plugging of `d`
mentions `d`, because the context has a hole and the hole receives `d`
(`mem_plug_of_hole`). So an instance that does not mention `d` cannot be
`plug c d` for any well-formed `c`. Adding such instances cannot change
whether `plug c d` is derivable by membership, and the rule clause does
not read `insts` at all.

The two corollaries are not instances of R3, because a fresh datum or
form enlarges the set of well-formed contexts: new contexts appear. The
argument is the same in spirit: a new context mentions something no
instance mentions (the fresh datum, or the fresh form), so *both*
pluggings fail derivability, and the `iff` in `collapsed` holds because
both sides are false. A context that reaches outside the regime does not
separate; it fails twice.

## Plain-language interpretation

To tell two data apart you need a stencil that lights up for one and not
the other. A stencil lights up when the filled-in sentence is one the
regime has asserted. If every sentence you add is about other data, no
stencil's reading on `d` or `d'` moves, because every reading on `d`
contains `d` and you asserted nothing containing `d`. Likewise a stencil
that names a datum nobody has said anything about, or uses a form nobody
has filled in, reads dark on everything, and dark on both is agreement,
not separation.

The limit is as sharp as the lemma: an instance that *does* mention `d`
is exactly how separation happens. Units 19 and 20 separate `a` from `b`
by asserting something about one of them. R3 says the unmentioning part
of a candidate is dead weight, nothing more.

## Pseudocode

```
# Gloss, R3
given: new instances, none mentioning d, none mentioning d'
key: for e in {d, d'} and any context c with a hole,
     derivable(r + new, plug(c, e)) <-> derivable(r, plug(c, e))
   forward: if plug(c, e) is in new, then new mentions e -- excluded; so it was in r
   backward: membership in r is membership in r + new; rules unchanged
collapse in r + new  <->  for every c: both pluggings agree  <->  collapse in r

# Gloss, R1 and R2
a context naming the fresh datum / using the fresh form:
   neither plugging is derivable (no instance mentions it; no rule covers it)
   so both pluggings agree, for d and for d' alike
every other context: unchanged from r
```

## Python

The check takes a three-datum regime with one unary form and applies each
change in turn, then shows the pruning the lemma licenses on a four-datum
base.

```python
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, replay
from derivation.observe import collapsed_pairs

base = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"), AdmitForm(1)])
r3 = replay([AdmitInst(0, (2,))], base)      # mentions datum 2 only
r2 = replay([AdmitForm(2)], base)            # a fresh form, used by nothing
edge = replay([AdmitInst(0, (0,))], base)    # mentions datum 0
print(collapsed_pairs(base), collapsed_pairs(r3), collapsed_pairs(r2), collapsed_pairs(edge))
```

Output:

```text
((0, 1), (0, 2), (1, 2)) ((0, 1),) ((0, 1), (0, 2), (1, 2)) ((1, 2),)
```

The pruning count, from the check script's output on the four-datum base
with target `(0, 1)`:

```text
four data, target (0, 1): 59 two-item deltas, 26 kept, 33 dropped
  dropped by the mention lemma (two distinct instances, neither mentioning 0 or 1):
  [(NewInst(form=0, args=(2,)), NewInst(form=0, args=(3,)))]; valid: 0
  valid dropped deltas: 8; each has a valid one-item part: True
```

## Line-by-line Python explanation

`base` has three data and one unary form, nothing asserted: every pair is
collapsed, `((0, 1), (0, 2), (1, 2))`.

`replay([AdmitInst(0, (2,))], base)` appends one instance, the mark on
datum 2. It mentions neither 0 nor 1, and R3 says `(0, 1)` stays
collapsed: the output `((0, 1),)` confirms it. The other two pairs are
separated, because the instance mentions 2; R3 is about the pair it
names, not about every pair.

`replay([AdmitForm(2)], base)` appends a binary form with no instance and
no rule. New contexts appear (seven of them, with one or two holes), and
none separates anything: the collapsed pairs are unchanged (R2).

`edge` appends the mark on datum 0. It mentions 0, the lemma's hypothesis
fails, and `(0, 1)` is no longer collapsed. The boundary is exactly where
the lemma says.

The pruning numbers: on four data with the unary form, the unpruned
enumeration lists 59 two-item deltas (duplicates included, as Genesis's
cross-check test enumerates them); the pruned one keeps 26. Of the 33
dropped, one is the mention lemma's own case, two distinct marks on 2 and
3, and it is not a valid response to `(0, 1)`. The other dropped deltas
that are valid, 8 of them, each contain a one-item delta that is already
valid, so they are not minima; that is the other pruning rules at work.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Mention.lean lines 40-43
theorem mem_plug_of_hole {c : Ctx} (h : none ∈ c.slots) (d : Nat) :
    d ∈ (plug c d).2 := by
  simp only [plug]
  exact List.mem_map.mpr ⟨none, h, rfl⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/Mention.lean lines 88-110
theorem collapsed_append_unmentioning
    (r : Regime) (new : List Inst) (d d' : Nat)
    (hd : ∀ p ∈ new, d ∉ p.2) (hd' : ∀ p ∈ new, d' ∉ p.2) :
    collapsed { r with insts := r.insts ++ new } d d' ↔ collapsed r d d' := by
  have key : ∀ (e : Nat) (c : Ctx), none ∈ c.slots →
      (∀ p ∈ new, e ∉ p.2) →
      (derivable { r with insts := r.insts ++ new } (plug c e)
        ↔ derivable r (plug c e)) := by
    intro e c hhole hnew
    constructor
    · rintro (hm | hr)
      · rcases List.mem_append.mp hm with h | h
        · exact Or.inl h
        · exact absurd (mem_plug_of_hole hhole e) (hnew _ h)
      · exact Or.inr hr
    · rintro (hm | hr)
      · exact Or.inl (List.mem_append.mpr (Or.inl hm))
      · exact Or.inr hr
  constructor
  · intro h c hc
    have hhole : none ∈ c.slots := hc.2.2.1
    rw [← key d c hhole hd, ← key d' c hhole hd']
    exact h c hc
  · intro h c hc
    have hhole : none ∈ c.slots := hc.2.2.1
    rw [key d c hhole hd, key d' c hhole hd']
    exact h c hc
```

```lean
-- Lean (Genesis), lean4/Derivation/Mention.lean lines 168-187
theorem collapsed_fresh_form (r : Regime) (d d' : Nat) (k : Nat)
    (hinst : ∀ p ∈ r.insts, p.1 < r.forms.length)
    (hrule : ∀ f ∈ r.rules, f < r.forms.length) :
    collapsed { r with forms := r.forms ++ [k] } d d' ↔ collapsed r d d' := by
  constructor
  · intro h c hc
    refine h c ⟨?_, ?_, hc.2.2.1, hc.2.2.2⟩
    · exact Nat.lt_of_lt_of_le hc.1 (by simp)
    · rw [getD_append_left _ _ _ _ hc.1]; exact hc.2.1
  · intro h c hc
    by_cases hold : c.form < r.forms.length
    · refine h c ⟨hold, ?_, hc.2.2.1, hc.2.2.2⟩
      have := hc.2.1
      rwa [getD_append_left _ _ _ _ hold] at this
    · -- the context uses the fresh form: nothing is derivable either side
      have hnot : ∀ e : Nat, ¬ derivable r (plug c e) := by
        intro e hd
        cases hd with
        | inl hm => exact hold (hinst _ hm)
        | inr hr => exact hold (hrule _ hr)
      exact ⟨fun hx => absurd hx (hnot d), fun hx => absurd hx (hnot d')⟩
```

The book's Lean applies R3 and R2 to the three-datum regime and shows the
hypothesis is needed.

```lean
-- Lean (book), textbook/checks/u30_lean.py
def three : Regime := ⟨3, [1], [], [], []⟩
def marked2 : Regime := ⟨3, [1], [(0, [2])], [], []⟩

theorem marked2_collapsed_01 : collapsed marked2 0 1 := by
  rw [marked2_is_append,
    collapsed_append_unmentioning three [(0, [2])] 0 1 (by decide) (by decide)]
  exact collapsed_of_no_insts three rfl 0 1

theorem marked2_separable_02 : separable marked2 0 2 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem mentioning_separates :
    separable { three with insts := three.insts ++ [(0, [0])] } 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem fresh_form_collapsed_01 : collapsed { marked2 with forms := marked2.forms ++ [2] } 0 1 :=
  (collapsed_fresh_form marked2 0 1 2 (by decide) (by decide)).mpr marked2_collapsed_01

theorem wf_has_hole (r : Regime) (c : Ctx) (h : wfCtx r c) : none ∈ c.slots :=
  h.2.2.1
```

## Line-by-line Lean explanation

**`mem_plug_of_hole`.** `plug c d` maps each slot to `d` if it is a hole
and to its datum otherwise. `simp only [plug]` exposes that map.
`List.mem_map.mpr ⟨none, h, rfl⟩` says: `d` is in the mapped list because
it is the image of the element `none`, which is in `c.slots` by `h`, and
`none` maps to `d` by definition (`rfl`).

**`collapsed_append_unmentioning`, the `key`.** For any datum `e` and any
context with a hole, if no new instance mentions `e`, then derivability of
`plug c e` is the same before and after. Forward: a derivation is
membership (`hm`) or a rule (`hr`). Membership in `r.insts ++ new` splits
(`List.mem_append.mp`) into membership in `r.insts`, which is the goal, or
membership in `new`; but then that instance mentions `e`
(`mem_plug_of_hole`), contradicting `hnew`, so `absurd`. A rule is a rule
on both sides. Backward: membership in `r.insts` is membership in the
appended list; rules again unchanged.

**The two directions of the `iff`.** `intro h c hc`: take collapse on one
side and a well-formed context. `hhole` is the hole conjunct of
well-formedness. `rw [← key d ..., ← key d' ...]` rewrites the goal's two
derivabilities to the other regime's; `exact h c hc` is then the assumed
collapse at `c`. The second direction rewrites the other way. The
well-formedness `hc` is the same on both sides because `wfCtx` reads
`forms` and `data`, which the change leaves alone.

**`collapsed_fresh_form`.** The hypotheses say every instance's form and
every rule's form is below the current form count. Forward: a context of
the old regime is a context of the new one (its form index is below the
longer list, and `getD_append_left` says its arity is read from the old
part), so apply the assumed collapse. Backward: split on whether the
context's form is old. If old, as before. If it is the fresh form `k`,
`hnot` shows nothing plugged into it is derivable in `r`: a membership
derivation would put the form below the old count (`hinst`), as would a
rule (`hrule`), contradicting `hold`. Both pluggings underivable gives the
`iff` by two `absurd`s. (R1, `collapsed_fresh_datum`, has the same shape
with `exists_out_of_range_slot` finding the slot that names the fresh
datum; Unit 12 reads it line by line.)

**The book's `marked2_collapsed_01`.** `marked2` is `three` with the mark
on 2 appended, by `rfl`. Rewrite with R3, whose two side conditions
`(by decide)` check that `0 ∉ [2]` and `1 ∉ [2]`; the goal becomes
collapse in `three`, which `collapsed_of_no_insts` gives.
`marked2_separable_02` and `mentioning_separates` exhibit the two edges:
the mark separates the datum it mentions from the others, and a mark on
0 separates `(0, 1)`. `fresh_form_collapsed_01` is R2 applied with the
fresh arity 2, the side conditions decided on the concrete lists.
`wf_has_hole` is the conjunct the whole module turns on, extracted.

**Axioms.** R3 and R1 report `propext, Quot.sound`; R2 reports `propext`
alone, because its proof uses `simp` and `rw` on lists but never
`decide`. The book instances report `propext, Quot.sound` through the
decided side conditions.

## What has been proved

- Every plugging mentions its datum (Genesis, derived).
- R3: appending unmentioning instances preserves the collapse of the
  named pair, both ways (Genesis, derived).
- R1 and R2: a fresh unreferenced datum or form preserves the collapse of
  every existing pair, both ways, under hypotheses that are conjuncts of
  `Regime.wf` (Genesis, derived).
- On the three-datum regime, the mark on 2 leaves `(0, 1)` collapsed, a
  mark on 0 does not, and a fresh binary form changes nothing (book Lean).

## What has not been proved

- In Lean, the enclosing claim "the pruned enumeration contains every
  minimum". That quantifies over the declared cost-2 grammar slice and is
  the bounded computation `test_pruned_cost2_contains_every_valid_full_delta`,
  cross-checked against the unpruned space. The ledger's
  `CL-PRUNE-STRUCTURAL` says so under "Scope, exactly".
- Anything about a delta that mentions the target. R3 is silent about it,
  and such deltas are the ones that separate.
- The rule-removal pruning, which is a different lemma
  (`separable_of_subrules`, `rule_item_never_minimal`, `RuleBridge.lean`,
  Unit 33).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `List.mem_map`, `List.mem_append`, `List.getD` | membership in mapped and appended lists | metatheory |
| `rintro`, `rcases`, `by_cases`, `absurd` | case analysis on derivations | metatheory tactics; `by_cases` on a decidable `<` |
| `{ r with insts := ... }` | the changed regime | metatheory record update |
| `decide` on `d ∉ [2]`, on `wfCtx` | the book instances | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The instances. Mention is a fact about an
instance's argument list; the regime holds the list and the metatheory
reads it.

**Phrases to read with care.**

- "A fresh datum is useless" is not what R1 says. It says a fresh datum
  *by itself* separates nothing; a delta that admits a datum and then
  mentions it with a target is how an auxiliary witness works (Unit 21's
  `BL` admits nothing fresh, but the engine's trees contain such
  responses).
- "The pruning is proved" is true of the three irrelevance facts and
  bounded-computational for the enumeration that uses them.

## Student exercise

R3 is stated for a pair `(d, d')` that already exists in `r`. Why can it
not be used, as it stands, to prune a candidate that admits a fresh datum
and an instance mentioning only that fresh datum, and which theorem covers
that candidate instead?

## Answer

Such a candidate changes `data`, so the regime after it has new
well-formed contexts, the ones with a slot naming the fresh datum, and R3
only moves instances over a fixed context space. R1 is the theorem for the
datum admission: it shows the fresh datum, unreferenced by any instance of
`r`, leaves every existing pair's collapse unchanged. The instance that
mentions only the fresh datum then mentions neither target datum, so R3
applies in the enlarged regime and removes it too. The candidate is
therefore dropped by the two lemmas in sequence, which is exactly shape
(b) of `iter_cost2_deltas`: a fresh datum is kept only with an instance
that mentions it *and* is generated for the target pair.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Mention.lean` lines 40-43, 47-50, 56-80, 88-110, 124-153, 157-160, 168-187 |
| Axiom report | `artifacts/lean_axioms.txt`: `mem_plug_of_hole` `[propext, Quot.sound]`; `collapsed_append_unmentioning` `[propext, Quot.sound]`; `collapsed_fresh_datum` `[propext, Quot.sound]`; `collapsed_fresh_form` `[propext]` |
| Paper | `paper/paper.md` §8.3 (pruning lemmas) and §12 residuals R1 to R3 (discharged 2026-08-17); ledger `CL-PRUNE-STRUCTURAL` with its "Scope, exactly" paragraph |
| Check (Python) | `python textbook/checks/u30_mention.py`: the three-datum regime under R3, R2 and the mentioning edge; every plug mentions its datum over 8 contexts; on four data, 59 two-item deltas, 26 kept, the one mention-lemma drop invalid, every valid drop covered by a valid one-item part |
| Check (book Lean) | `python textbook/checks/u30_lean.py`: six book theorems plus four Genesis theorems kernel-checked, Lean 4.33.0 |
