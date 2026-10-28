# Unit 06. Re-admitting a token designates, it does not add

**Claim.** Admitting a token that is already admitted changes nothing: it
points at the existing datum. This is a declared convention of the model,
not a theorem. Its Lean form is the token-aware step `stepT`.
**Status:** admitted. **Lean:** `Derivation.stepT`
(`lean4/Derivation/Erasure.lean` lines 40-60), a definition. **Axioms:**
`propext`, `Quot.sound` (the definition's membership test). **Depends on:**
`Regime`, `Event`, `stepE` (Units 01, 03); the admission dedup is what
made Unit 05's sub-readings converge.

## Question

Challenge 2 "supplies and retains" ⟨A⟩, which Challenge 1 already
supplied, and which one sub-reading already admitted. What happens when
an admitted token is admitted again? Does the ledger gain a second copy,
or does the second admission mean "that one, again"?

## What we already possess

- `stepE` on the Lean `Regime` has `admitDatum` with no token: it adds one
  to the count, every time (Unit 03). The Lean `Regime` cannot tell a
  repeat from a fresh datum because it keeps no tokens.
- Python's `step` keeps tokens and tests `e.token in r.data` (Unit 03).
- Unit 05 showed the two Challenge-1 sub-readings converge *because*
  admission dedups.

## New concept: designation, and a token-aware model

**Designation** is pointing at something already there, without changing
it. Genesis's convention: an `AdmitDatum(token)` whose token is already in
the ledger designates the existing datum; the ledger is returned as it is.
The paper calls the rule "dedup on presentation identity, a declared
metatheoretic convention" (`paper/paper.md` §3 item 2).

To state this in Lean, Genesis has a second state type, `TRegime`, whose
data field is a *list of tokens* instead of a count, and a second step
function `stepT`. This is the **token-aware model**. Unit 07 proves that it
and the counting model agree. This unit reads `stepT`'s admission case.

```lean
-- Lean (Genesis), lean4/Derivation/Erasure.lean lines 20-28, 31-38
structure TRegime where
  tokens : List Nat
  forms  : List Nat
  insts  : List Inst
  rules  : List Nat
  reqs   : List (Nat × Nat)
deriving Repr, DecidableEq

inductive TEvent where
  | supply       (token : Nat)
  | admitDatum   (token : Nat)
  | admitForm    (arity : Nat)
  | admitInst    (form : Nat) (args : List Nat)
  | admitRuleAll (form : Nat)
  | impose       (i j : Nat)
deriving Repr, DecidableEq
```

## Plain-language interpretation

A guest list. When a name is called out that is already on the list, the
host does not write it a second time; the call refers to the guest already
listed. Whether two calls of the same name mean one guest or two is not
something the list can decide by itself. The host decided it: one guest.
Genesis's host is the metatheory, and the decision is written in the
`AdmitDatum` docstring and in `stepT`.

What the decision rests on is **presentation identity**: two tokens are
"the same" when the metatheory says the strings are equal. The system never
compares tokens. It only ever receives the outcome: the ledger unchanged,
or one datum longer.

## Pseudocode

```
# Gloss
admit(token) on ledger L:
    if token is already in L's tokens:   return L            (designation)
    else:                                return L with token appended
```

## Python

```python
# Python (Genesis), code/derivation/model.py lines 67-75 and 111-114
class AdmitDatum:
    """Admission of a presented token as a datum.

    Re-admission of an already admitted token is a designation of the
    existing datum, not a duplication (declared metatheoretic convention:
    presentation identity dedups admissions).
    """

    token: str

    if isinstance(e, AdmitDatum):
        if e.token in r.data:
            return r
        return Regime(r.data + (e.token,), r.forms, r.insts, r.rules, r.reqs)
```

```python
from derivation.model import AdmitDatum, replay

print(replay([AdmitDatum("<a>"), AdmitDatum("<a>")]).data)
```

Output:

```text
('<a>',)
```

## Line-by-line Python explanation

`class AdmitDatum:` declares a kind of record. The text in triple quotes is
a **docstring**, documentation attached to the class. Here it is where the
convention is declared in words. `token: str` says the record holds one
field, a string.

`if isinstance(e, AdmitDatum):` inside `step`: "if the event `e` is an
admission of a datum". `isinstance` tests the kind of a value.

`if e.token in r.data:` tests whether the event's token is one of the
strings in the ledger's data tuple. `in` is Python's membership test; on a
tuple of strings it compares each string for equality. This comparison is
the metatheory's: Python compares the characters.

`return r`: when the token is present, hand back the ledger unchanged. The
same object, not a copy. That is designation.

`return Regime(r.data + (e.token,), ...)`: otherwise build a new ledger
whose data tuple is the old one with the token appended, `+` joining two
tuples, and the other four fields copied.

`replay([AdmitDatum("<a>"), AdmitDatum("<a>")])`: two admissions of the
same token. The first appends; the second finds the token present and
returns the ledger as it is. `.data` is `('<a>',)`, a one-element tuple.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Erasure.lean lines 40-45 (admission case)
def stepT (t : TRegime) : TEvent → Option TRegime
  | .supply _ => some t
  | .admitDatum tok =>
      if tok ∈ t.tokens then some t
      else some { t with tokens := t.tokens ++ [tok] }
  ...
```

The book's Lean states the two halves of the rule as theorems about
`stepT`, shows the counting model cannot dedup by itself, and shows that
admission order is kept by the token-aware state.

```lean
-- Lean (book), textbook/checks/u06_lean.py
theorem readmit_designates (t : TRegime) (tok : Nat) (h : tok ∈ t.tokens) :
    stepT t (.admitDatum tok) = some t := by
  simp [stepT, h]

theorem fresh_appends (t : TRegime) (tok : Nat) (h : tok ∉ t.tokens) :
    stepT t (.admitDatum tok) = some { t with tokens := t.tokens ++ [tok] } := by
  simp [stepT, h]

theorem twice_is_once :
    replayT [.admitDatum 1, .admitDatum 1] tgenesis = some ⟨[1], [], [], [], []⟩ := by
  decide

theorem erased_model_counts :
    replayE [.admitDatum, .admitDatum] genesis = some ⟨2, [], [], [], []⟩ := rfl

theorem order_kept :
    replayT [.admitDatum 1, .admitDatum 2] tgenesis
      ≠ replayT [.admitDatum 2, .admitDatum 1] tgenesis := by
  decide
```

## Line-by-line Lean explanation

**`stepT`.** `def stepT (t : TRegime) : TEvent → Option TRegime` names a
function of a state `t` and an event, returning a state or `none`. The
lines beginning with `|` match on the event's constructor, as `stepE`
does (Unit 03).

`| .admitDatum tok =>`: the admission case, now carrying a token `tok`.

`if tok ∈ t.tokens then some t`: `∈` is list membership. For `Nat` lists
Lean decides it by walking the list and comparing numbers. If the token is
present, the result is `some t`, the unchanged state. This line *is* the
convention.

`else some { t with tokens := t.tokens ++ [tok] }`: otherwise, the state
with its token list extended by one. `{ t with field := value }` copies `t`
changing one field; `++` joins lists; `[tok]` is the one-element list.

**`readmit_designates`.** Inputs: any state `t`, any token `tok`, and a
hypothesis `h` that `tok` is in `t.tokens`. Conclusion: the step returns
`some t`. Proof: `simp [stepT, h]` unfolds `stepT`, sees the `if`, uses `h`
to decide its condition is true, and reduces to `some t = some t`, which it
closes. `simp` is a rewriting engine; the list in brackets names what it
may unfold or use.

**`fresh_appends`.** The same with `∉` ("not in"). `simp` takes the `else`
branch.

**`twice_is_once`.** A concrete two-event history from the empty
token-aware state. First admission: `1 ∉ []`, append, tokens `[1]`.
Second: `1 ∈ [1]`, unchanged. `decide` runs it.

**`erased_model_counts`.** The counting model's `admitDatum` has no token
and always adds one. Two of them give count 2. `rfl` closes it because
both sides compute to the same value. So the counting model, on its own,
does not know about designation. Unit 07 shows how the two models are
reconciled: a duplicate admission is *erased to a supply* before the
counting model sees it.

**`order_kept`.** Admitting 1 then 2 gives tokens `[1, 2]`; 2 then 1 gives
`[2, 1]`. Different lists, different states; `decide` proves `≠`. The
token-aware state remembers admission order. Whether the *system* can see
that order is a different question, answered no in Unit 11
(`Bridge.order_erased_at_object_level`).

**Axioms.** Every statement that mentions `stepT` reports `propext` and
`Quot.sound`. The membership test `tok ∈ t.tokens` is decided by a
standard-library procedure on lists whose correctness proof uses both.
Both are inside Genesis's declared boundary `{propext, Quot.sound}`;
nothing here reaches `Classical.choice`.

## What has been proved

- In the token-aware model, re-admission of a present token is the
  identity, and admission of an absent token appends it (book Lean, from
  the definition; derived).
- The counting model by itself counts every `admitDatum` (book Lean).
- Admission order is kept by the token-aware state (book Lean).

## What has not been proved

- That dedup on presentation identity is the right convention. It is
  declared. A model that admitted a repeated token as a second datum is
  coherent too; Genesis did not choose it, and says so in the docstring.
  Under that other model Unit 05's sub-readings would not converge.
- That the system can tell a re-admission from a supply. It cannot: on a
  ledger holding the token, `step(r, AdmitDatum(t))` and
  `step(r, Supply(t))` return the same ledger (checked below), and
  Unit 07's erasure maps the re-admission *to* a supply.
- That "the same token" is an internal fact. Token equality is the
  metatheory's string comparison. The system receives only its effect.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `List Nat`, `∈`, `++` | the token list and its membership test | metatheory data and decision procedure |
| `Nat` tokens | names for ⟨⟩, ⟨A⟩, ⟨AB⟩ | metatheory labels, never compared inside the system |
| `(t : TRegime) (tok : Nat)` | the two general theorems | metatheory quantifiers |
| `propext`, `Quot.sound` | inherited through `stepT` | inside the declared boundary |

**What the system holds.** In the token-aware model, the list of admitted
tokens in admission order. In the counting model, their number. The
system holds no table of which token is which; that is the metatheory's
record (Unit 00).

**Admissions and their price.** The convention is an admission at the
level of the model's grammar. Its price: every claim about "how many data"
is a claim about distinct presentations, and a reader who meant
"how many admission events" must count the history instead.

**Phrases to read with care.**

- "The system recognises ⟨A⟩ when it comes back" imports recognition. The
  metatheory compares strings; the system is handed an unchanged ledger.
- "Re-admission is idempotent" is true of `stepT` and false of `stepE`,
  which never sees a token. Say which model.
- "Designation" names what the second admission *does* under the
  convention, not an act the system performs.

## Student exercise

Change one line of the gloss so that a repeated token becomes a second
datum. Then say what `replay([AdmitDatum("<a>"), AdmitDatum("<a>")]).data`
would be, and whether `historyL_replays` (Unit 05) would still be true of
reading L's history.

## Answer

The gloss becomes:

```
admit(token) on ledger L:   return L with token appended    (always)
```

Then `.data` would be `('<a>', '<a>')`, two data with the same token.
Reading L's history has no repeated admission (its repeated event is a
*supply* of ⟨A⟩, which changes nothing), so it would still replay to a
two-datum ledger and `historyL_replays` would still hold. What would break
is Unit 05's sub-reading convergence: the "admit on supply" sub-reading
would end with three data, ⟨A⟩, ⟨A⟩, ⟨AB⟩, and the question "is ⟨A⟩
admitted at Challenge 1?" would stay open instead of dissolving. That is
the whole effect of the convention on the derivation so far.

## Verification

| Item | Where |
|---|---|
| Convention | `code/derivation/model.py` lines 67-75 (docstring) and 111-114; `paper/paper.md` §3 item 2 ("dedup on presentation identity — a declared metatheoretic convention") |
| Lean | `lean4/Derivation/Erasure.lean` lines 20-28 (`TRegime`), 31-38 (`TEvent`), 40-60 (`stepT`) |
| Ledger | `paper/paper_claim_ledger.md`, `CL-TOKEN-ERASURE` (Python: `test_admit_datum_dedups_on_presentation_identity`) |
| Genesis test | `tests/test_model.py` lines 34-36 |
| Check (Python) | `python textbook/checks/u06_readmission.py`: twice is once; the same object is returned; all 121 admission histories of length ≤ 4 over three tokens give the distinct tokens in first-admission order; two orders are two regimes of equal count; re-admission equals supply on a full ledger |
| Check (book Lean) | `python textbook/checks/u06_lean.py`: seven book theorems kernel-checked against the compiled library, Lean 4.33.0; `stepT` and every statement mentioning it report `propext, Quot.sound`; `erased_model_counts` reports `propext` |
