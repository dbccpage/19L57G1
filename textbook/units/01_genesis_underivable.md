# Unit 01. Nothing is derivable at genesis

**Claim.** In the starting ledger, no judgment instance is derivable.
**Status:** derived. **Lean:** `Derivation.genesis_underivable`
(`lean4/Derivation/Inertia.lean`, line 21). **Axioms:** none.

This is the first theorem of Genesis and the smallest one. It is worth
reading slowly, because every later proof uses the same three moves: unfold
a definition, split into cases, and close each case because the data rule it
out.

## What you need first

### 1. An instance

An instance is a candidate statement: a form number and a list of data.

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean line 21
abbrev Inst := Nat × List Nat
```

```python
# Python (Genesis), code/derivation/model.py line 23
Inst = tuple[int, Args]          # Args is tuple[int, ...]
```

```
# Gloss
an instance is a pair (form, args)
  form : which kind of statement, by number
  args : which data it is about, by number
(3, [0, 1])  reads  "form 3 holds of datum 0 and datum 1"
```

An instance is only a candidate. Writing one down does not assert it. Whether
it holds is the question `derivable` answers.

`i.1` in Lean means the first component of the pair `i`, the form number.
Python writes it `inst[0]`.

### 2. A regime (the ledger)

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean line 53
structure Regime where
  data  : Nat               -- how many data are admitted
  forms : List Nat          -- arity of each admitted form
  insts : List Inst         -- admitted instances
  rules : List Nat          -- forms whose every instance holds
  reqs  : List (Nat × Nat)  -- separation demands imposed from outside
```

```python
# Python (Genesis), code/derivation/model.py (abridged)
@dataclass(frozen=True)
class Regime:
    data: tuple[str, ...]      # admitted data, kept as tokens for audit only
    forms: tuple[int, ...]
    insts: frozenset[Inst]
    rules: frozenset[int]
    reqs: frozenset[Pair]
```

The comments on the Lean fields are this book's. Two differences between
the versions matter later and not here: Lean keeps `data` as a bare count
while Python keeps token strings, and Lean keeps lists while Python keeps
sets. Lean makes its lists behave as sets by refusing duplicates on insertion
(`insertNew`, Basic.lean line 25).

### 3. The starting regime

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean line 14
def genesis : Regime := ⟨0, [], [], [], []⟩
```

```python
# Python (Genesis), code/derivation/model.py line 56
EMPTY = Regime((), (), frozenset(), frozenset(), frozenset())
```

```
# Gloss
genesis:
  data  = 0
  forms = []
  insts = []
  rules = []
  reqs  = []
```

`⟨0, [], [], [], []⟩` fills the five fields in order. Both readings of the
seed start here: reading L keeps ⟨⟩ out of the ledger, and reading F admits
it as datum 0 by a later event (`Inertia.historyF_replays`, line 66). The
theorem is about this starting ledger, before any event.

**Status of these three definitions:** admitted. They are Genesis's choice
of representation (paper §3).

### 4. Derivability

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean line 85
def derivable (r : Regime) (i : Inst) : Prop :=
  i ∈ r.insts ∨ i.1 ∈ r.rules
```

```python
# Python (Genesis), code/derivation/observe.py line 52
def derivable(r: Regime, inst: Inst) -> bool:
    return inst[0] in r.rules or inst in r.insts
```

```
# Gloss
inst is derivable in r  if
    inst was admitted as an instance             (left half)
 or its form carries the all-instances rule      (right half)
```

This is all the inference there is in Genesis. No chaining, no closure, no
logic beyond these two lookups. **Status:** admitted (paper §3 item 4).

The Python checks the two halves in the other order. `or` does not care
about order, so the two definitions agree.

## The theorem

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean lines 20-25
/-- Nothing is derivable at genesis. -/
theorem genesis_underivable (i : Inst) : ¬ derivable genesis i := by
  intro h
  cases h with
  | inl h => cases h
  | inr h => cases h
```

Read the statement aloud: "for every instance `i`, it is not the case that
`i` is derivable in `genesis`." The `(i : Inst)` before the colon means the
theorem holds for an arbitrary instance: any form number, any list of data,
including data that were never admitted.

## The proof, step by step

**Step 0. What `¬` means.** In Lean, `¬ P` is defined as `P → False`. To
prove it, you assume `P` and derive a contradiction.

**Step 1. `intro h`.** Assume the thing we want to rule out. Now we hold
`h : derivable genesis i` and must produce `False`.

**Step 2. Unfold.** `derivable genesis i` is, by its definition,
`i ∈ genesis.insts ∨ i.1 ∈ genesis.rules`. Lean sees through the definition
on its own; no explicit unfolding command is needed.

**Step 3. `cases h with`.** A proof of `A ∨ B` was built in one of two ways:
`Or.inl` from a proof of `A`, or `Or.inr` from a proof of `B`. `cases`
splits into those two possibilities, and in each one renames the inner proof
to `h` again.

**Step 4. Case `inl`.** Now `h : i ∈ genesis.insts`. Lean computes
`genesis.insts` to `[]`, so `h : i ∈ []`. List membership is an inductive
predicate with two constructors, and both of them prove membership in a list
of the form `x :: rest` (a list with a first element). The empty list `[]`
has no first element, so neither constructor could have produced `h`.
`cases h` asks Lean to list the constructors that could have; there are
none, and the case closes with nothing left to prove.

**Step 5. Case `inr`.** Now `h : i.1 ∈ genesis.rules`, which computes to
`i.1 ∈ []`. The same reason closes it.

**Step 6. Done.** Both ways of being derivable are impossible, so the
assumption in Step 1 is impossible, and `¬ derivable genesis i` holds.

Notice what the proof never looked at: `i` itself. It did not matter which
form or which data `i` names. The emptiness of two lists did all the work.

**Axioms.** `artifacts/lean_axioms.txt` line 2 reads
`'Derivation.genesis_underivable' does not depend on any axioms`. The proof
uses only computation and case analysis. This book did not rebuild Lean; it
reads Genesis's committed report.

## The same fact in Python

Python cannot quantify over every instance; there are infinitely many. The
check below tries every instance with form number at most 3 and argument
lists of length at most 3 over data numbers 0 to 3, and confirms none is
derivable in `EMPTY`. That is a finite sample, not a proof. The proof is the
Lean above.

```
python textbook/checks/u01_genesis_underivable.py
```

Genesis's own test of the same point is `tests/test_engine.py::
test_challenge0_inertia`, which checks that the list of derivable instances
at Challenge 0 is empty.

## What it shows, and what it does not

It shows that the starting ledger supports no judgment at all. There is no
"true" statement yet, not even about ⟨⟩, because there is no form to state
anything with and no instance to state.

It does not show that nothing will ever follow. Later events can admit forms
and instances. That nothing *must* follow, that no next step is forced, is a
different claim, and Genesis marks it admitted rather than proved
(Unit 04).

It does not show that the room is empty because ⟨⟩ is "nothing". The ledger
is empty because no admission event has happened. Whether ⟨⟩ belongs in it
is the open question of Unit 05.

It is a statement about one regime. Unit 02 proves the general version: any
regime with no instances and no rules derives nothing, however many data and
forms it holds.

## Sources

| Item | Where |
|---|---|
| Theorem | `lean4/Derivation/Inertia.lean` line 21, `Derivation.genesis_underivable` |
| Definitions | `lean4/Derivation/Basic.lean`: `Inst` line 21, `Regime` line 53, `derivable` line 85; `Inertia.lean`: `genesis` line 14 |
| Python | `code/derivation/model.py` (`Inst`, `Regime`, `EMPTY`); `code/derivation/observe.py` (`derivable`) |
| Axiom report | `artifacts/lean_axioms.txt` line 2: no axioms |
| Root inventory | `lean4/Derivation.lean` line 75 (`#print axioms`) |
| Ledger | `paper/paper_claim_ledger.md`, `CL-0-INERTIA` |
| Test | `tests/test_engine.py::test_challenge0_inertia` |
| Check | `textbook/checks/u01_genesis_underivable.py` |
