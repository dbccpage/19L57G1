# Unit 36. Lists that mean sets

**Claim.** Genesis's Python keeps a regime's instances, rules and demands
as sets; its Lean keeps them as duplicate-free lists. Under the relation
`RegimeExt` (equal datum count, equal form table, membership-equal
instance, rule and demand lists) every observable of the development
transports: derivability, context well-formedness, collapse,
separability, item and delta application, and response validity
(`derivable_ext` through `validResponse_ext`). So no claim *stated in
terms of these observables* depends on the order in which admissions were
listed. That every exported claim factors through these observables is
not proved and not asserted. **Status:** derived. **Lean:**
`Derivation.SetEq` (`lean4/Derivation/Ext.lean` line 21), `RegimeExt`
(37-39), `derivable_ext` (50-52), `wfCtx_ext` (56-59), `collapsed_ext`
(62-71), `separable_ext` (74-83), `OptExt` (86-89), `applyItem_ext`
(92-126), `applyDelta_ext` (129-147), `validResponse_ext` (152-177).
**Axioms:** `derivable_ext` none; the rest `propext`. **Depends on:** the
token-erasure half of the bridge (Unit 07); `insertNew` (Unit 11); the
observables (Units 08, 09, 18).

## Question

Unit 07 connected the token-aware Python to the token-erased Lean for
*data*. One gap remained. A Python regime is a frozenset of instances;
a Lean regime is a list. Two admission orders give one Python regime and
two Lean regimes. Could anything proved about the Lean regime depend on
which of the two lists it has, and so fail to be a statement about the
Python regime at all?

## What we already possess

- `Regime` (Basic): `data : Nat`, `forms : List Nat`, `insts : List Inst`,
  `rules : List Nat`, `reqs : List (Nat × Nat)` (Unit 08).
- `insertNew l a = if a ∈ l then l else l ++ [a]` with `mem_insertNew`
  (Unit 11): admission never duplicates.
- The observables and their definitions, which read `insts`, `rules` and
  `reqs` only through `∈` (Units 08, 09, 18), and `data`, `forms` through
  `<`, `getD` and `length`.
- The Python `Regime` dataclass with `insts: frozenset[Inst]`,
  `rules: frozenset[int]`, `reqs: frozenset[Pair]` (`model.py` lines
  48-50), and `data`, `forms` as tuples.

## New concept: membership extensionality, one observable at a time

`SetEq l1 l2 := ∀ x, x ∈ l1 ↔ x ∈ l2` says two lists have the same
members. `RegimeExt r s` says the two regimes agree on the datum count
and the form table *as lists* (indices are names, so order is meaning
there) and are `SetEq` on the three collections where order is not
meaning. The theorems then go up the definitional ladder: `derivable`
reads two memberships, so it transports; `wfCtx` reads only `data` and
`forms`, which are equal; `collapsed` and `separable` quantify over
contexts and read `derivable`; `applyItem` reads the guards (which never
look at the three collections) and writes with `insertNew`, which
preserves `SetEq`; `applyDelta` folds; `validResponse` reads all of the
above. `OptExt` lifts the relation to `Option Regime` so that a delta that
fails on one side fails on the other.

The point is the direction of the claim. It is not "lists are sets". It
is "every observable we have defined cannot see the difference", proved
observable by observable, with the list of observables stated.

## Plain-language interpretation

Two clerks keep the same ledger. One writes entries in the order they
arrive; the other sorts them. The ledgers look different on the page. The
question is whether any decision made from the ledger could differ. The
answer is yes if a decision reads the page position of an entry, and no
if every decision asks only "is this entry present?" Genesis's decisions
all ask the second kind of question about instances, rules and demands,
and this unit proves it for each one. For data and forms the position
*is* the entry's name, so there the two clerks must agree on order, and
`RegimeExt` demands it.

## Pseudocode

```
# Gloss
SetEq l1 l2            := for every x: x in l1  iff  x in l2
RegimeExt r s          := r.data = s.data and r.forms = s.forms
                          and SetEq r.insts s.insts and SetEq r.rules s.rules
                          and SetEq r.reqs s.reqs

derivable_ext:   RegimeExt r s  ==>  derivable r i iff derivable s i
wfCtx_ext:       RegimeExt r s  ==>  wfCtx r c iff wfCtx s c      (reads data, forms only)
collapsed_ext,
separable_ext:   compose the two above under the context quantifier
applyItem_ext:   RegimeExt r s  ==>  OptExt (applyItem r it) (applyItem s it)
                 (the guards read data and forms; insertNew keeps SetEq)
applyDelta_ext:  fold applyItem_ext over the delta
validResponse_ext: RegimeExt r s ==> validResponse r i j δ iff validResponse s i j δ
```

## Python

```python
from derivation.candidates import Bounds, min_responses
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, replay
from derivation.observe import collapsed_pairs

head = [AdmitDatum("a"), AdmitDatum("b"), Impose(0, 1), AdmitForm(1), AdmitForm(1)]
ra = replay(head + [AdmitInst(0, (0,)), AdmitInst(1, (1,))])
rb = replay(head + [AdmitInst(1, (1,)), AdmitInst(0, (0,))])
print(ra == rb, sorted(ra.insts), collapsed_pairs(ra), collapsed_pairs(rb))
print(replay([AdmitDatum("a"), AdmitDatum("a")]).data)
d1 = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1), AdmitInst(0, (0,))])
d2 = replay([AdmitDatum("b"), AdmitDatum("a"), AdmitForm(1), AdmitInst(0, (0,))])
print(d1 == d2, d1.data[0], d2.data[0])
```

Output:

```text
True [(0, (0,)), (1, (1,))] () ()
('a',)
False a b
```

The check script's full output:

```text
two admission orders of the same instances: equal regimes True; insts [(0, (0,)), (1, (1,))]; collapsed pairs () ()
the same instance admitted twice: 1 instance; datum admitted twice: ('a',)
mixed regime, two orders: equal True; collapsed pairs ((1, 2),); mu2 minimum for (1, 2): (1, 0) (1, 0); same deltas True
datum order kept: data ('a', 'b') vs ('b', 'a'), equal False; the mark sits on 'a' vs 'b'; form order kept: forms (1, 2) vs (2, 1), equal False
```

## Line-by-line Python explanation

`ra` and `rb` admit the same two instances in opposite orders. Python
says `ra == rb`: the frozensets are equal, so the dataclasses are. The
collapsed pairs agree, trivially, since the regimes are one object. This
is the Python side of `RegimeExt`: the quotient is built into the
representation.

Admitting datum `"a"` twice yields one datum: the dedup of Unit 07 again
(`test_admit_datum_dedups_on_presentation_identity`). On the Lean side
this is `insertNew` returning its input.

The mixed regime shows an observable that is a *computation*, not a
predicate: `min_responses` returns the same cost `(1, 0)` and the same
set of deltas from either order. Lean has no `min_responses`; what Lean
proves is that `validResponse`, which the enumeration consults, agrees,
so the set of valid deltas is the same.

The last line is what is *not* quotiented. Admitting `"b"` before `"a"`
puts the mark on a different token, and the regimes differ. Likewise for
form order. In Lean, `RegimeExt` requires `r.data = s.data` and `r.forms =
s.forms` outright.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Ext.lean lines 21, 37-39, 50-52, 62-71
def SetEq {α : Type} (l1 l2 : List α) : Prop := ∀ x, x ∈ l1 ↔ x ∈ l2

def RegimeExt (r s : Regime) : Prop :=
  r.data = s.data ∧ r.forms = s.forms ∧ SetEq r.insts s.insts ∧
  SetEq r.rules s.rules ∧ SetEq r.reqs s.reqs

theorem derivable_ext {r s : Regime} (h : RegimeExt r s) (i : Inst) :
    derivable r i ↔ derivable s i :=
  or_congr (h.2.2.1 i) (h.2.2.2.1 i.1)

theorem collapsed_ext {r s : Regime} (h : RegimeExt r s) (d d' : Nat) :
    collapsed r d d' ↔ collapsed s d d' := by
  constructor
  · intro hc c hwf
    have h1 := hc c ((wfCtx_ext h c).mpr hwf)
    exact ((derivable_ext h _).symm.trans h1).trans (derivable_ext h _)
  · intro hc c hwf
    have h1 := hc c ((wfCtx_ext h c).mp hwf)
    exact ((derivable_ext h _).trans h1).trans
      (derivable_ext h _).symm
```

```lean
-- Lean (Genesis), lean4/Derivation/Ext.lean lines 86-89, 103-116, 152-166
def OptExt : Option Regime → Option Regime → Prop
  | some a, some b => RegimeExt a b
  | none, none => True
  | _, _ => False

  -- applyItem_ext, the instance case
  | newInst f args =>
      have hcond : (f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data)) ↔
          (f < s.forms.length ∧ args.length = s.forms.getD f 0 ∧
          (∀ x ∈ args, x < s.data)) := by
        rw [h.1, h.2.1]
      by_cases h1 : f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data)
      · simp only [applyItem, if_pos h1, if_pos (hcond.mp h1)]
        exact ⟨h.1, h.2.1, SetEq.insertNew' h.2.2.1 _, h.2.2.2.1,
          h.2.2.2.2⟩
      · simp only [applyItem, if_neg h1,
          if_neg (fun hc => h1 (hcond.mpr hc))]
        trivial

theorem validResponse_ext {r s : Regime} (h : RegimeExt r s)
    (i j : Nat) (δ : List Item) :
    validResponse r i j δ ↔ validResponse s i j δ := by
  constructor
  · intro ⟨t, happ, hsep, hreqs⟩
    have hd := applyDelta_ext h δ
    rw [happ] at hd
    cases hs : applyDelta s δ with
    | none => rw [hs] at hd; exact absurd hd id
    | some t' =>
        rw [hs] at hd
        refine ⟨t', hs, (separable_ext hd i j).mp hsep, ?_⟩
        intro q hq
        exact (separable_ext hd q.1 q.2).mp
          (hreqs q ((h.2.2.2.2 q).mpr hq))
  · ...  -- the mirror image, through RegimeExt.symm'
```

The book's Lean builds the two-order example, shows it is two regimes and
one `RegimeExt` class, instantiates the transport, and shows the two
fields that are not quotiented.

```lean
-- Lean (book), textbook/checks/u36_lean.py
def twoA : Regime := ⟨2, [1, 1], [(0, [0]), (1, [1])], [], [(0, 1)]⟩
def twoB : Regime := ⟨2, [1, 1], [(1, [1]), (0, [0])], [], [(0, 1)]⟩

theorem twoA_ne_twoB : twoA ≠ twoB := by decide

theorem twoA_ext_twoB : RegimeExt twoA twoB := by
  refine ⟨rfl, rfl, ?_, SetEq.rfl' _, SetEq.rfl' _⟩
  intro x
  simp only [twoA, twoB, List.mem_cons, List.not_mem_nil, or_false]
  exact or_comm

theorem separable_agrees : separable twoA 0 1 ↔ separable twoB 0 1 :=
  separable_ext twoA_ext_twoB 0 1

theorem valid_agrees (δ : List Item) :
    validResponse twoA 0 1 δ ↔ validResponse twoB 0 1 δ :=
  validResponse_ext twoA_ext_twoB 0 1 δ

theorem dup_inst_noop : insertNew [((0 : Nat), [(0 : Nat)])] (0, [0]) = [(0, [0])] :=
  insertNew_of_mem (by simp)

theorem form_order_matters :
    ¬ RegimeExt ⟨2, [1, 2], [], [], []⟩ ⟨2, [2, 1], [], [], []⟩ := by
  intro h
  have h2 := h.2.1
  simp at h2

theorem RegimeExt.trans' {r s t : Regime} (h1 : RegimeExt r s) (h2 : RegimeExt s t) :
    RegimeExt r t :=
  ⟨h1.1.trans h2.1, h1.2.1.trans h2.2.1,
   fun x => (h1.2.2.1 x).trans (h2.2.2.1 x),
   fun x => (h1.2.2.2.1 x).trans (h2.2.2.2.1 x),
   fun x => (h1.2.2.2.2 x).trans (h2.2.2.2.2 x)⟩
```

## Line-by-line Lean explanation

**`SetEq`, `RegimeExt`.** Five conjuncts; the projections `h.1`, `h.2.1`,
`h.2.2.1`, `h.2.2.2.1`, `h.2.2.2.2` pick them out in order, and the proofs
below are written with those projections.

**`derivable_ext`.** `derivable r i` is `i ∈ r.insts ∨ i.1 ∈ r.rules`;
`or_congr` combines the two `SetEq` facts at `i` and `i.1`. No tactic, no
axiom.

**`wfCtx_ext`.** Unfold and rewrite with the two equalities; `wfCtx` never
mentions the three collections.

**`collapsed_ext`.** Both directions have the same shape: given a context
well formed on one side, transport its well-formedness to the other side
(`wfCtx_ext`), apply the collapse there, and conjugate the resulting iff
by `derivable_ext` on each plugging. `separable_ext` is the same with the
existential witness carried across.

**`applyItem_ext`, the instance case.** `hcond`: the guard is the same
proposition on both sides, because it reads only `data` and `forms`.
Split on it. If it holds, both applications succeed and the results are
`RegimeExt`: the first two fields unchanged, the instance list by
`SetEq.insertNew'` (inserting the same element into `SetEq` lists keeps
them `SetEq`, by `mem_insertNew` on both sides), the rest unchanged. If
it fails, both are `none`, and `OptExt none none` is `True`. The datum,
form and rule cases are the same with their own guards.

**`applyDelta_ext`.** Induction on the delta, generalizing both regimes:
after one item, either both fail (done) or both succeed with `RegimeExt`
results (recurse). The mixed cases are refuted by `OptExt`'s `False`
clause.

**`validResponse_ext`.** Given a result `t` on the left, the delta lemma
says the right side also succeeds, with a `RegimeExt` result `t'`.
Separability of the target transports by `separable_ext hd`; for the
demands, `q ∈ s.reqs` is turned into `q ∈ r.reqs` by the fifth conjunct
of `h`, the hypothesis supplies separability in `t`, and it transports to
`t'`. The other direction uses `RegimeExt.symm'`.

**Book: `twoA`, `twoB`.** Two marks on two data, listed in both orders.
`decide` says the regimes are unequal (derived `DecidableEq` compares
the lists). `twoA_ext_twoB`: the first two conjuncts are `rfl`; the
instance conjunct unfolds membership in a two-element list to a
disjunction and applies `or_comm`; rules and demands are literally equal
lists, so `SetEq.rfl'`. Then every transport theorem instantiates at the
pair: `separable_agrees`, `valid_agrees` for every `δ`.

**Book: `dup_inst_noop`.** `insertNew` on an element already present
returns the list: Genesis's `insertNew_of_mem`. This is the Lean shadow
of the frozenset's idempotence.

**Book: `form_order_matters`, `RegimeExt.trans'`.** The second conjunct
of `RegimeExt` is list equality on `forms`, and `[1, 2] = [2, 1]` is
refuted by `simp`. Genesis proves reflexivity and symmetry; the book adds
transitivity, so `RegimeExt` is an equivalence relation. It is not stated
as one in Genesis because nothing there needs the third law.

**Axioms.** `derivable_ext` uses none. The others report `propext`, from
`rw` with iffs under binders. The book's concrete instances inherit
`propext`; `twoA_ne_twoB` by `decide` on a derived instance uses none.

## What has been proved

- The seven observables transport along `RegimeExt` (Genesis, derived;
  the second half of ledger `CL-TOKEN-ERASURE`).
- `RegimeExt` is reflexive and symmetric (Genesis); transitive (book).
- Two concrete admission orders are two Lean regimes and one `RegimeExt`
  class, with identical separability and identical valid responses (book
  Lean); the Python makes them one object (check).

## What has not been proved

- That every *exported claim* factors through the seven observables. The
  ledger narrowed this on 2026-08-18: claims stated at the representation
  level, such as the concrete replay equalities of Unit 07, are covered
  only up to `RegimeExt`. Unit 07 says the same in its own terms.
- Anything about the Python source. The bridge relates two Lean models;
  the Python is connected to the token-aware model by executable checks,
  not by a proof over the Python (ledger, endpoints stated 2026-09-08).
- That `data` and `forms` *could* be quotiented. They are not, by
  design: an index is a name.
- That the Lean lists are duplicate-free. `insertNew` keeps them so when
  starting from duplicate-free lists; `RegimeExt` does not require it, and
  the transport holds with or without duplicates.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `List.mem_*` lemmas, `or_congr`, `or_comm` | membership reasoning | metatheory |
| `OptExt` on `Option Regime` | lifting to possibly failing application | metatheory |
| `induction δ generalizing r s` | the fold | metatheory |
| `decide` on `Regime` equality | the book's `twoA ≠ twoB` | metatheory; derived instance |
| `propext` | inherited | inside the declared boundary |

**What the system holds.** The regime, however listed. The *order* of
instances is a fact about the representation, not about the regime; the
order of data and forms is a fact about the regime, because it names
them.

**Phrases to read with care.**

- "Lean works with sets" is false; it works with lists and proves that
  the observables do not care.
- "No claim depends on representation" is the *narrowed* claim's
  negation. The correct statement names the observables.

## Student exercise

`RegimeExt` compares `forms` as lists but `insts` as sets. Suppose someone
proposed to also compare `forms` as sets. Give a pair of regimes that
would then be related, and an observable of this unit that would fail to
transport.

## Answer

`⟨2, [1, 2], [], [], []⟩` and `⟨2, [2, 1], [], [], []⟩` have the same set
of arities. In the first, form `0` is unary; in the second, form `0` is
binary. `wfCtx` fails to transport: the context `⟨0, [none]⟩` is well
formed in the first (slot count `1 = getD [1,2] 0 = 1`) and not in the
second (`1 ≠ 2`). So `wfCtx_ext`, and everything above it, would be
false. Form order is meaning because `applyItem`, `wfCtx` and `plug` all
address forms by index; the same holds for data, which `newInst` and
`slotOk` bound by `< r.data`.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Ext.lean` lines 21-47 (relations), 50-83 (observables), 86-147 (application), 152-177 (validity) |
| Axiom report | `artifacts/lean_axioms.txt`: `derivable_ext` none; `wfCtx_ext`, `collapsed_ext`, `separable_ext`, `applyItem_ext`, `applyDelta_ext`, `validResponse_ext` `[propext]` |
| Paper | `paper/paper.md` §2 (membership extensionality; "no claim stated in terms of them depends on list order or representation … not proved and is not asserted" for the rest); ledger `CL-TOKEN-ERASURE` (ii), narrowed 2026-08-18 |
| Python | `code/derivation/model.py` lines 48-50 (frozensets); `tests/test_model.py::test_admit_datum_dedups_on_presentation_identity` |
| Check (Python) | `python textbook/checks/u36_ext.py`: two admission orders give one regime with one set of collapsed pairs and one set of `mu2` minima; duplicate admission dedups; datum and form order are kept |
| Check (book Lean) | `python textbook/checks/u36_lean.py`: nine book theorems plus five Genesis theorems kernel-checked, Lean 4.33.0 |
