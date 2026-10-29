# Unit 04. No successor is internally forced

**Claim.** In the admitted grammar, a ledger changes only when an event is
applied to it. There is no rule inside the model that produces a "next"
ledger from the current one.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** admitted (a property of the
declared grammar, `paper/paper.md` §4, third bullet). **Lean:** none in
Genesis; the book's Lean records three small consequences of the
grammar's shape (status **derived (book Lean)**).
**Depends on (admitted):** `Regime` (Unit 01), `Event`, `stepE`, `replayE`
(Unit 03).

This unit teaches a statement that is *not* a theorem, and says why. Units
01 to 03 proved things about `derivable` and about one event. This unit
steps back and asks what kinds of change exist at all.

</details>

## First pass

Give the replay function a notebook and an empty event list. It returns
the same notebook. Now hand it an admission event; the notebook may change.
The caller supplied that event.

Predict what happens if we write a separate policy that always chooses
an admission. The policy can use one of the existing six event kinds;
it does not need a seventh kind. Its choice is an added instruction,
not a choice proved to come from the notebook.

The event grammar tells us which inputs are permitted. It does not
by itself choose an input. This unit's structural claim is about the
declared replay model, not a law about physical objects remaining still.

## Question

Starting from any ledger, is there anything in the model that forces the
next ledger? Or does every change need someone outside to supply an event?

## What we already possess

- A ledger is a `Regime`: a data count, a list of form arities, admitted
  instances, admitted rules, and imposed demands (Unit 01).
- An `Event` is one of six kinds (Unit 03). `stepE r e` gives the ledger
  after event `e`, or `none` when `e` is refused.
- `replayE h r` applies a list of events in order (Unit 03).
- A supply event changes nothing: `supply_no_op` (Unit 03).

Nothing else has been admitted. In particular, nothing called "time",
"the next state", "a rule of evolution" or "a transition" has been admitted.

## New concept: a closed grammar

A **grammar** here means: the list of kinds of thing the model can be
asked to do. Genesis's grammar of changes is the six constructors of
`Event`. The word **closed** means that every event value has one of these six kinds.
It does not prevent a separately written policy from choosing events of
those kinds. A policy and a new event constructor are different additions.

In Lean, an `inductive` type is closed by definition. When you write

```lean
inductive Event where
  | supply       (token : Nat)
  | admitDatum
  | admitForm    (arity : Nat)
  | admitInst    (form : Nat) (args : List Nat)
  | admitRuleAll (form : Nat)
  | impose       (i j : Nat)
```

you are telling Lean: every value of type `Event` was built by exactly one
of these six lines, and Lean will let a proof split into exactly these six
cases and no others.

The second part of the concept is about **who calls `stepE`**. Look at its
type: `stepE (r : Regime) : Event → Option Regime`. It needs an event as
input. There is no function in `Basic.lean` or `Inertia.lean` of type
`Regime → Regime` or `Regime → Option Regime` that takes a ledger alone and
returns a changed one. The events come from the history, a list written by
someone outside the model (Unit 03, **Where the supply is recorded**).

## Plain-language interpretation

The ledger is like a notebook with six permitted kinds of entry. The
replay function applies the entries supplied to it; it does not choose
the next one. Give it an empty history and it returns the starting
notebook unchanged. The paper calls this **inertia** (`paper/paper.md` §4).
There is no elapsed-time model here, so this is not a physical law.

That is a fact about this notebook, the one Genesis chose. A different
model could add a seventh kind of entry, or a clock that writes entries on
its own. Nothing in this unit says such a model is wrong. It says that
Genesis did not admit one, so nothing in Genesis can be "the system
deciding to move".

## Pseudocode

```
# Gloss
to change a ledger r:
    you must hand in an event e           (one of six kinds)
    the model computes step(r, e)         (or refuses e)
there is no   next(r)                     (no such operation exists)
replay([], r) = r                         (no events, no change)
```

## Python

```python
# Python (Genesis), code/derivation/model.py line 103
Event = Union[Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose]
```

```python
# Python (Genesis), code/derivation/model.py lines 142-150 (docstring omitted)
def replay(history: Sequence[Event], base: Regime = EMPTY) -> Regime:
    r = base
    for e in history:
        r = step(r, e)
    return r
```

The smallest example:

```python
from derivation.model import EMPTY, replay

print(replay([]) == EMPTY)
```

Output:

```text
True
```

## Line-by-line Python explanation

`Event = Union[...]`: the name `Event` is given a value. `Union[A, B, C]`
is Python's way of writing "a value of type `A`, or of type `B`, or of type
`C`". The six names inside the brackets are the six classes defined just
above in the same file, one per kind of event. This is Python's version of
the Lean `inductive`: it lists the kinds. Python does not stop a programmer
from inventing a seventh class later, so the Python list is a convention
checked by tests, where the Lean list is enforced by the type checker.

`def replay(history, base=EMPTY):` defines a function with two inputs. The
second has a **default value**: if the caller does not give a `base`, the
function uses `EMPTY`, Genesis's name for the starting ledger.

`r = base`: a variable `r` is set to the starting ledger. `=` assigns.

`for e in history:`: a **loop**. The lines indented under it run once for
each element of `history`, in order, with `e` naming the current element.

`r = step(r, e)`: `step` is Unit 03's one-event function. Its result
replaces `r`. So after the loop, `r` is the ledger after every event.

`return r`: hand `r` back to the caller.

`replay([])`: calls `replay` with an empty list, `[]`, and the default
base. The loop body never runs, so the result is `EMPTY`.

`print(replay([]) == EMPTY)`: `==` compares two values for equality and
gives `True` or `False`; `print` displays it. The output is `True`.

What this example shows: with no events, Genesis's own replay returns the
starting ledger unchanged. It does not show that no model could ever
evolve by itself. It shows that this one does not.

## Lean 4

Genesis has no theorem for this unit, because the claim is about the
*shape* of the definitions, not about a proposition inside them. The
paper marks it **[definition]** (structural, model-scoped). The book's Lean
below records three consequences of that shape. Each is checked by Lean's
kernel against Genesis's compiled library when `u04_lean.py` runs.

```lean
-- Lean (book), textbook/checks/u04_lean.py
theorem event_is_one_of_six (e : Event) :
    (∃ t, e = .supply t) ∨ e = .admitDatum ∨ (∃ a, e = .admitForm a) ∨
    (∃ f args, e = .admitInst f args) ∨ (∃ f, e = .admitRuleAll f) ∨
    (∃ i j, e = .impose i j) := by
  cases e with
  | supply t => exact Or.inl ⟨t, rfl⟩
  | admitDatum => exact Or.inr (Or.inl rfl)
  | admitForm a => exact Or.inr (Or.inr (Or.inl ⟨a, rfl⟩))
  | admitInst f args => exact Or.inr (Or.inr (Or.inr (Or.inl ⟨f, args, rfl⟩)))
  | admitRuleAll f => exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨f, rfl⟩))))
  | impose i j => exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨i, j, rfl⟩))))

theorem no_event_no_change (r : Regime) : replayE [] r = some r := rfl

theorem change_needs_non_supply (r s : Regime) (e : Event)
    (h : replayE [e] r = some s) (hne : s ≠ r) : ∀ t, e ≠ .supply t := by
  intro t het
  subst het
  exact hne (Option.some.inj h).symm
```

## Line-by-line Lean explanation

**The first theorem.**

`theorem event_is_one_of_six (e : Event) :` names the theorem and takes one
input, an arbitrary event `e`. The colon separates the inputs from the
statement.

The statement is a chain of `∨` ("or"). Each piece says `e` equals one
kind of event. `∃ t, e = .supply t` reads "there is some number `t` such
that `e` is the supply of `t`". The dot in `.supply` tells Lean to look up
`supply` inside the type `Event`. There are six pieces, one per kind.

`:= by` begins the proof.

`cases e with` splits the proof into one case per constructor of `Event`.
This is the key move: Lean knows `Event` has exactly six constructors, so
it demands exactly six cases and accepts no more. If a seventh existed, the
proof would fail with a missing case.

`| supply t => exact Or.inl ⟨t, rfl⟩`: in the case where `e` is `supply t`,
prove the left piece of the `∨`. `Or.inl` chooses the left side. `⟨t, rfl⟩`
supplies the witness `t` for `∃ t, ...` and proves `supply t = supply t` by
`rfl`, "both sides are identical".

`| admitDatum => exact Or.inr (Or.inl rfl)`: skip the left piece with
`Or.inr`, then take the left piece of what remains with `Or.inl`, and prove
`admitDatum = admitDatum` by `rfl`. The remaining lines are the same
pattern, moving one `Or.inr` further right for each later constructor and
supplying the constructor's arguments as witnesses.

Why the proof is universal: `e` was never a specific event. The six cases
together cover every value of type `Event`, so the theorem holds for all
of them. The quantifier over `e` is Lean's quantifier (see **Outside the
system**).

**The second theorem.** `replayE [] r = some r`. `replayE` folds the
events of a list over `r`. With the empty list `[]` there is nothing to
fold, and the definition of `List.foldlM` on `[]` returns `some r` at once.
So the proof is `rfl`: the two sides compute to the same thing.

**The third theorem.** Inputs: two ledgers `r` and `s`, an event `e`, a
hypothesis `h` that the one-event history `[e]` takes `r` to `s`, and a
hypothesis `hne` that `s` is not `r`. The conclusion: for every `t`, `e` is
not `supply t`. In words: if a single event changed the ledger, that event
was not a supply.

`intro t het`: to prove `∀ t, e ≠ .supply t`, take an arbitrary `t` and
assume `het : e = .supply t`; the goal becomes `False`.

`subst het`: replace `e` by `.supply t` everywhere, using `het`.

`exact hne (Option.some.inj h).symm`: now `h` says
`replayE [.supply t] r = some s`. The left side computes to `some r` (one
supply step, `supply_no_op`). So `h` is really `some r = some s`.
`Option.some.inj` strips the `some` from both sides, giving `r = s`.
`.symm` turns it into `s = r`. That is exactly what `hne` denies, so
applying `hne` to it gives `False`. Done.

## What has been proved

In Genesis: nothing new in this unit. `supply_no_op` (Unit 03) is the one
theorem the paper cites for the bare-supply case.

In the book's Lean, against Genesis's definitions: the grammar has exactly
six kinds of event; an empty history leaves any ledger as it is; and any
one-event change of ledger was caused by an event that is not a supply.
The axiom report for the three is `none`, `propext`, `propext`: the second
and third mention `replayE`, which reaches `propext` through `stepE`
(Unit 03, **Axioms**).

## What has not been proved

- That "no successor is forced" is a theorem about a forcing predicate.
  There is no predicate `forced` in Genesis, so there is nothing to prove
  about it. The paper says so (`paper/paper.md` §4; an earlier version had
  tagged the whole item **[theorem]** and was corrected on 2026-09-08).
- That no extension of the grammar could force a successor. Adding a
  constructor to `Event`, or a function `Regime → Regime`, is a different
  model. Genesis makes no claim about it.
- That the ledger "wants" to stay still, or "resists" change. Those
  phrases import an agent. The ledger is a value; `stepE` is a function
  that needs an event argument.
- That events themselves come from nowhere. They are written in the history
  by the external constructor or the caller (Unit 00). Where *they* come
  from is outside the model.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `(e : Event)`, `(r s : Regime)`, `(t : Nat)` | universal quantifiers of the book's theorems, discharged once for arbitrary values | metatheory quantifiers |
| `inductive`, `cases` | the closed grammar and the case split | metatheory (Lean's type theory) |
| `∃`, `∨`, `Or.inl`, `Or.inr` | stating "one of six" | metatheory logic |
| `List.foldlM`, `Option.some.inj` | `replayE` and stripping `some` | metatheory library |
| `propext` | reached through `stepE`, as in Unit 03 | inside Genesis's axiom boundary |

**What the system holds.** The current ledger, finite. It holds no list of
possible events, no notion of "next", and no history: the history is the
metatheory's record (Unit 03).

**Phrases to read with care.**

- "Every event is one of six kinds" is a statement about Lean's type
  `Event`, made in the metatheory. The system holds events only as they
  are applied to it, one at a time; it does not hold the type.
- "The system does nothing by itself" imports a self that could act. Read
  instead: no function in the model maps a ledger to a different ledger
  without an event argument.
- "Inertia" is the paper's word for this; it is not a physical law and
  nothing here is about motion.

## Student exercise

Suppose someone proposes a new function for Genesis:

```python
def next_ledger(r):
    return step(r, AdmitDatum("fresh"))
```

and says: "Now the ledger has a successor; the system forces admission of a
fresh datum." Is this a successor forced *by the system*? Point to the
event.

## Answer

No. The function still calls `step(r, e)` with an event, `AdmitDatum("fresh")`,
and the event is chosen by whoever wrote `next_ledger`. The choice of event
has been moved from the history into the program text, but it is still a
choice made outside the ledger, and the ledger still changes only through
`step`. What has been added is a *policy* that always picks the same event.
Genesis does admit policies of that kind later, and names them as declared
external policies: the "external continuation policy" supplies one fresh
token at a fixpoint (`paper/paper.md` §3 item 10). It is tagged
**[declared metatheory]**, never derived. Your `next_ledger` would be
classified the same way.

A second point: if the token `"fresh"` is already admitted in `r`, the
Python `step` returns `r` unchanged (re-admission designates, Unit 06). So
even the policy does not always change the ledger.

## Verification

| Item | Where |
|---|---|
| Claim and tag | `paper/paper.md` §4, third bullet (**[definition]**, structural, model-scoped); §10 question 2 |
| Grammar | `lean4/Derivation/Basic.lean` lines 134-141 (`Event`), 145-163 (`stepE`), 166-167 (`replayE`) |
| Bare-supply theorem | `lean4/Derivation/Inertia.lean` line 17, `Derivation.supply_no_op` (Unit 03) |
| Python | `code/derivation/model.py`: `Event` line 103, `step` from line 106, `replay` lines 142-150 |
| Ledger | `paper/paper_claim_ledger.md`, `CL-0-NO-PROPOSAL-MUTATION` |
| Classification | `code/derivation/completion.py`, bridge "seed forces successor state": FALSE_WITH_COUNTERMODEL |
| Check (Python) | `python textbook/checks/u04_no_forced_successor.py`: six event kinds; the only functions in `model.py` are `step(r, e)`, `replay(history, base)`, `certify(history, claimed)`, none taking a ledger alone; `replay([]) == EMPTY`; on a three-item ledger, every one-event change came from a non-supply event, and the three refused events raised `AdmissionError` |
| Check (book Lean) | `python textbook/checks/u04_lean.py`: three theorems kernel-checked against Genesis's compiled library, Lean 4.33.0; axiom reports none / propext / propext |
