# Unit 08. Contexts, profiles, collapse and separability

**Claim.** A context is a test with an empty slot. Two admitted data are separable when some well-formed context succeeds for one and fails for the other.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** admitted. **Lean:** `Derivation.Ctx`, `plug`,
`derivable`, `wfCtx`, `collapsed`, `separable`
(`lean4/Derivation/Basic.lean` lines 74-125). **Axioms:** `propext` in
the definitions (through `List.getD`). **Depends on:** `Regime`, `Inst`
(Unit 01); `derivable` was first met in Unit 01.

</details>

## First pass

Use two data, 0 and 1, and a one-place form called marked. The context
`marked(_)` leaves a hole. With only `marked(0)` admitted and no uniform
rule, plugging in 0 is derivable and plugging in 1 is not. That question
witnesses their separation.

A profile collects every well-formed question giving a derivable
answer for one datum. Equal profiles mean equal answers to those
questions; the indices can still be distinct. Not derivable here is
not a negative physical measurement.

Predict the result for a two-place context `linked(_,_)`. Both holes
receive the **same** tested datum: 0 gives `linked(0,0)`, not a pair
of independently chosen data. A fully filled record has no hole and
is not a context test. The formal well-formedness conditions below
separate available tests from arbitrary raw records.

## Detailed claim and formal anchors

Genesis declares what it means for the system to tell two data
apart: there is a well-formed context that is derivable when plugged with
one datum and not when plugged with the other.

Two data with no such
context are *collapsed*.

These are definitions, chosen by the external
constructor.

## Question

Challenge 3 will demand that ⟨A⟩ and ⟨AB⟩ be "internally separable". The
metatheory can tell them apart by looking at the strings. What could the
*system* do that counts as telling them apart, when it cannot see strings
at all?

## What we already possess

- A ledger with a data count, forms with arities, instances `(form, args)`,
  rules, demands (Unit 01).
- `derivable r i`: the instance `i` is admitted, or its form carries the
  uniform rule. Nothing else counts as derivation (Unit 01).
- Indices: the system's data are `0, 1, 2, ...`, positions in the ledger,
  not tokens (Units 06, 07).

## New concept: a context is a question with a hole

A raw **context record** contains a form index and a list of slots.
Each slot is a datum index or a **hole**, written `none`. To be
**well formed**, the form must be admitted, its arity must match the slot
count, filled slots must name admitted data, and at least one hole must
remain. Raw records failing these checks do not count as available tests.
At least one slot must be a hole. **Plugging** a datum into a context
fills every hole with that datum, producing an instance. A context is a
question the system can be asked about any datum: "is this instance, with
you in the holes, derivable?"

### Profile: collect the successful tests

The **profile** of a datum is the set of well-formed contexts whose
plugging with it is derivable.

### Collapse: all available tests agree

Two data are **collapsed** when every
well-formed context answers the same for both.

### Separation: one test disagrees

They are **separable**
when some well-formed context answers differently; that context is the
**witness**.

The definitions are *behavioral*: separability is about what is derivable,
never about tokens, order, or any property the metatheory can see.

## Plain-language interpretation

A form with a hole is a stencil: "___ is marked", or "___ is linked to
datum 1". Holding the stencil over a datum gives a sentence; the system
either derives that sentence or does not. Two data are told apart when
some stencil gives a derived sentence for one and not for the other. If
every stencil treats them the same, they have the same observable profile at that stage. Their admitted indices can still be distinct.

This is the only sense of "different" the derivation ever grants the
system. The paper calls it "behavioral separation by positive
derivability" (`paper/paper.md` §3 item 5, §7.1). "Positive" means a
context counts only by being derivable, never by failing to be.

## Pseudocode

```
# Gloss
context      = (form, slots)      with at least one slot a hole
well formed  = form admitted, slot count = arity, some hole,
               every filled slot < number of data
plug(c, d)   = (form, slots with every hole replaced by d)
profile(d)   = { c well formed : derivable(plug(c, d)) }
collapsed(d, d')  = profile(d) = profile(d')
separable(d, d')  = profile(d) ≠ profile(d')
```

## Python

```python
# Python (Genesis), code/derivation/observe.py lines 37-57 and 68-69
def contexts(r: Regime) -> tuple[Context, ...]:
    """All contexts of the regime, deterministically ordered."""
    out: list[Context] = []
    for f, arity in enumerate(r.forms):
        for slots in slot_tuples(arity, r.n_data()):
            if any(s is None for s in slots):
                out.append((f, slots))
    return tuple(out)


def plug(c: Context, d: int) -> Inst:
    f, slots = c
    return (f, tuple(d if s is None else s for s in slots))


def derivable(r: Regime, inst: Inst) -> bool:
    return inst[0] in r.rules or inst in r.insts


def profile(r: Regime, d: int) -> frozenset[Context]:
    return frozenset(c for c in contexts(r) if derivable(r, plug(c, d)))


def separable(r: Regime, i: int, j: int) -> bool:
    return profile(r, i) != profile(r, j)
```

```python
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, replay
from derivation.observe import contexts, profile, separable, witness

r = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1), AdmitInst(0, (1,))])
print(contexts(r))
print(profile(r, 0), profile(r, 1))
print(separable(r, 0, 1), witness(r, 0, 1))
```

Output:

```text
((0, (None,)),)
frozenset() frozenset({(0, (None,))})
True (0, (None,))
```

## Line-by-line Python explanation

`def contexts(r):` builds the list of all contexts of a regime.

`for f, arity in enumerate(r.forms):`: `enumerate` walks the form table
giving each form's index `f` and its arity. So forms are numbered by
position, as data are.

`for slots in slot_tuples(arity, r.n_data()):`: `slot_tuples` (lines
30-34) yields every tuple of length `arity` whose entries are `None` or a
datum index below the data count. That is every way to fill the slots.

`if any(s is None for s in slots):`: keep only tuples with at least one
hole. `any` is true when at least one entry satisfies the test. A tuple
with no hole is an instance, not a context: it asks nothing about a
plugged datum.

`out.append((f, slots))` collects the context; `return tuple(out)` fixes
the list.

`def plug(c, d):` takes the context apart into `f, slots`, then rebuilds
the slot tuple replacing each `None` by `d` and keeping every other entry.
`d if s is None else s` is Python's conditional expression: "d when the
slot is a hole, otherwise the slot".

`def derivable(r, inst):` is Unit 01's: the instance's form is in the
rules, or the instance itself is admitted. `or` gives true if either side
is true.

`def profile(r, d):` the set of contexts `c` whose plugging with `d` is
derivable. `frozenset` is a set that cannot change afterwards, so it can
be compared with `!=` and `==`.

`def separable(r, i, j):` two data are separable when their profiles
differ. (`witness`, lines 72-78, walks the contexts in order and returns
the first that answers differently, or `None`.)

The example: two data, one unary form, one instance saying "datum 1 is
marked". There is one context, the unary stencil with a hole. Plugging 0
gives `(0, (0,))`, not admitted: profile of 0 is empty. Plugging 1 gives
`(0, (1,))`, admitted: profile of 1 holds the stencil. The profiles differ,
so the pair is separable, and the witness is the stencil.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean lines 74-86, 106-110, 117-125
structure Ctx where
  form  : Nat
  slots : List (Option Nat)
deriving Repr, DecidableEq

def plug (c : Ctx) (d : Nat) : Inst :=
  (c.form, c.slots.map (fun s => s.getD d))

def derivable (r : Regime) (i : Inst) : Prop :=
  i ∈ r.insts ∨ i.1 ∈ r.rules

def wfCtx (r : Regime) (c : Ctx) : Prop :=
  c.form < r.forms.length ∧
  c.slots.length = r.forms.getD c.form 0 ∧
  none ∈ c.slots ∧
  ∀ s ∈ c.slots, slotOk r.data s

def collapsed (r : Regime) (d d' : Nat) : Prop :=
  ∀ c : Ctx, wfCtx r c → (derivable r (plug c d) ↔ derivable r (plug c d'))

def separable (r : Regime) (d d' : Nat) : Prop :=
  ∃ c : Ctx, wfCtx r c ∧
    ¬ (derivable r (plug c d) ↔ derivable r (plug c d'))
```

The book's Lean exercises each definition on concrete values.

```lean
-- Lean (book), textbook/checks/u08_lean.py
def two_one : Regime := ⟨2, [1], [], [], []⟩

theorem ctx_hole_wf : wfCtx two_one ⟨0, [none]⟩ := by decide
theorem no_hole_not_ctx : ¬ wfCtx two_one ⟨0, [some 0]⟩ := by decide
theorem wrong_arity_not_ctx : ¬ wfCtx two_one ⟨0, [none, none]⟩ := by decide
theorem plug_example : plug ⟨0, [none, some 1, none]⟩ 0 = (0, [0, 1, 0]) := rfl
theorem sep_example : separable ⟨2, [1], [(0, [1])], [], []⟩ 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩
```

## Line-by-line Lean explanation

**`Ctx`.** A structure with two fields: a form index and a list of slots.
`Option Nat` is "a number, or nothing": `some 3` names datum 3, `none` is a
hole. `deriving Repr, DecidableEq` asks Lean to generate printing and an
equality test.

**`plug`.** `c.slots.map (fun s => s.getD d)` applies the function in
brackets to each slot. `s.getD d` is "the number inside `s`, or `d` if
`s` is `none`". So holes become `d` and filled slots stay. `getD` is where
`propext` enters this unit's definitions (Unit 03 traced the same source).

**`derivable`.** Unit 01's definition, with `∨` for "or".

**`wfCtx`.** Four conditions joined by `∧` ("and"): the form index is
below the number of forms; the slot count equals that form's arity
(`r.forms.getD c.form 0` reads the arity, with 0 as a default that never
applies once the first condition holds); `none ∈ c.slots` says some slot
is a hole; and every filled slot names a datum below the count (`slotOk`,
lines 92-94, is `True` on a hole and `x < n` on `some x`). These match
Python's enumeration exactly, and the paper says so (§3 item 3).

**`collapsed`.** `∀ c : Ctx, wfCtx r c → (... ↔ ...)`: for every context
(Lean quantifies over all `Ctx`, including ill-formed ones, and the
`wfCtx r c →` discards those), the two pluggings are derivable together or
not at all. `↔` is "if and only if".

**`separable`.** `∃ c : Ctx, wfCtx r c ∧ ¬ (... ↔ ...)`: there is a
well-formed context on which the two pluggings disagree. The docstring
says why it is stated with `∃`: every proof of separability must hand over
its witness. Unit 09 proves the two definitions exclude each other.

**The book theorems.** `ctx_hole_wf` and the three `¬ wfCtx` theorems are
decided by computation: `decide` evaluates the four conditions. Note the
second: `⟨0, [some 0]⟩` fails only the third condition, no hole. The fourth
book theorem in the check, `no_form_not_ctx`, fails the first. `plug_example`
is `rfl`: the `map` computes. `sep_example` supplies the witness
`⟨0, [none]⟩` in the first slot of the `∃`, then `decide` proves it is
well formed, then `decide` proves the two pluggings disagree: `(0, [0])` is
not in the instance list and `(0, [1])` is.

**Axioms.** The definitions `wfCtx`, `collapsed`, `separable` report
`propext` (through `List.getD`). Each `decide` on a concrete regime
reports `propext, Quot.sound`, because deciding list membership uses a
library procedure that carries `Quot.sound`. Genesis's own `U1_separable`
reports the same pair (`artifacts/lean_axioms.txt`).

## What has been proved

Nothing general in this unit: it introduces definitions. The book's Lean
proves concrete instances (a context is or is not well formed; a plugging
computes; a specific pair is separable). These are derived facts about
specific small regimes.

## What has not been proved

- That this is the right sense of "telling apart". It is the declared
  sense. Other senses exist (negative information, token comparison,
  counting), and the derivation uses none of them.
- That contexts exist at all in the Challenge regimes. They do not: with
  no forms there are no contexts (`contexts` yields nothing), so every
  pair is collapsed for want of a question to ask (Unit 10).
- That a datum's profile is something the system holds. The profile is
  computed by the metatheory from the ledger. The system holds the ledger.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Option Nat`, `List.map`, `getD` | holes and plugging | metatheory data |
| `∀ c : Ctx` in `collapsed` | ranging over all contexts, including ill-formed ones | metatheory quantifier; the `wfCtx` guard cuts it to the finite well-formed ones |
| `∃ c` in `separable` | the witness | metatheory; constructive, the witness is always exhibited |
| `Prop`, `↔`, `¬` | the statements | metatheory logic |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The ledger. Contexts, profiles and the words
"collapsed" and "separable" are the metatheory's descriptions of what the
ledger derives. Nothing is added to the ledger by defining them.

**Admissions and their price.** The definition of separability is the
largest single admission of the programme after the regime itself: every
later "minimum", "witness" and "obstruction" is relative to it. Its price
is that a system which could distinguish data some other way would not
count as doing so here.

**Phrases to read with care.**

- "The system sees the difference between ⟨A⟩ and ⟨AB⟩" should be read:
  some well-formed context is derivable for one plugging and not the
  other. The system sees no tokens.
- "A context observes" is a figure of speech. A context is a list; the
  metatheory evaluates derivability.
- "Negative information" (a context that *fails* for both) is not a
  witness. Only positive derivability counts, by definition.

## Student exercise

In the regime `⟨2, [2], [(0, [0, 1])], [], []⟩` (two data, one binary form,
one instance linking datum 0 to datum 1), list the well-formed contexts and
find a witness that 0 and 1 are separable.

## Answer

Arity 2 over 2 data gives `3² − 2² = 5` contexts: slot tuples over
`{hole, 0, 1}` with at least one hole: `[none, none]`, `[none, some 0]`,
`[none, some 1]`, `[some 0, none]`, `[some 1, none]`.

Take `⟨0, [none, some 1]⟩`. Plugging 0 gives `(0, [0, 1])`, admitted.
Plugging 1 gives `(0, [1, 1])`, not admitted. They disagree, so this
context is a witness. (Genesis uses exactly this witness in
`Minimality.BL_separable`, Unit 19.) `⟨0, [some 0, none]⟩` is a second
witness: `(0, [0, 0])` is not admitted, `(0, [0, 1])` is. `⟨0, [none, none]⟩`
is not a witness: both pluggings, `(0, [0, 0])` and `(0, [1, 1])`, are
underivable.

## Verification

| Item | Where |
|---|---|
| Definitions | `lean4/Derivation/Basic.lean`: `Ctx` 74-77, `plug` 80-81, `derivable` 85-86, `slotOk` 92-94, `wfCtx` 106-110, `collapsed` 117-118, `separable` 123-125 |
| Python | `code/derivation/observe.py`: module docstring 1-17, `slot_tuples` 30-34, `contexts` 37-44, `plug` 47-49, `derivable` 52-53, `profile` 56-57, `profiles` 60-65, `separable` 68-69, `witness` 72-78, `collapsed_pairs` 81-95 |
| Paper | `paper/paper.md` §3 items 3-5 (context, derivability, profile, collapse, internal separability); §7.1 **[definition]** |
| Axiom report | `artifacts/lean_axioms.txt`: `U1_separable` `[propext, Quot.sound]` (Genesis's own use of these definitions on a concrete regime) |
| Check (Python) | `python textbook/checks/u08_contexts.py`: the single unary context; counts `(n+1)^a − n^a` for `n ≤ 3`, `a ≤ 3`; plugging; derivability by instance and by rule; profiles, witness; separable is the complement of collapsed on every pair of four regimes |
| Check (book Lean) | `python textbook/checks/u08_lean.py`: eleven book theorems kernel-checked, Lean 4.33.0; `plug_example` no axioms, the `decide` theorems `propext, Quot.sound`, the three definitions `propext` |
