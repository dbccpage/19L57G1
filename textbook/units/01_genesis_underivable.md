# Unit 01. Nothing is derivable at genesis

**Claim.** In the starting ledger, no judgment instance is derivable.
**Status:** derived. **Lean:** `Derivation.genesis_underivable`
(`lean4/Derivation/Inertia.lean`, line 21). **Axioms:** none.
**Depends on (admitted):** `Inst`, `Regime`, `genesis`, `derivable`.

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

**A finite ledger, an unbounded extension.** Neither half looks at the
instance's arguments. The right half asks only whether the instance's form
number is in `rules`. So once a rule is admitted, `derivable` holds of
instances the ledger never admitted anything for. Take the well-formed
regime

```lean
-- one unary form, the all-instances rule on it, no data, no instances
⟨0, [1], [], [0], []⟩
```

Call it `R`. It is reached from `genesis` by two admission events: admit a
form of arity 1, then admit the rule on form 0. In `R`:

- `derivable R (0, [99])` holds, though datum 99 was never admitted (`R`
  admits no datum at all);
- `derivable R (0, [])` and `derivable R (0, [1, 2, 3])` hold, though form 0
  has arity 1;
- `derivable R (1, [0])` does not hold: form 1 was never admitted and
  carries no rule.

The proof of the first is one line from the definition: the right half
needs `0 ∈ [0]`, which holds. (Proved by hand from the definition above;
no Lean file in the repository states this example.) Genesis's own Python
agrees: `python textbook/checks/u01_rule_extension.py` builds `R` by
Genesis's `replay` and evaluates all four.

So the ledger is finite (one form, one rule) while the set of instances
`derivable` holds of, read in Lean, is unbounded. Both are true at once;
they are about different things. Three remarks keep them apart:

1. Nothing infinite is stored. The rule is one admitted item, the number 0
   in a list. The unbounded part is the metatheory's reading of
   `derivable`.
2. The comment on `rules` in `code/derivation/model.py` says "every
   well-formed instance of the form counts as derivable". The code checks
   only the form number, in Lean and in Python, so the extension also
   contains instances that are not well formed. The comment is narrower
   than the definition; the definition governs.
3. Genesis's observation is built to ask only about admitted data. A
   context's filled slots name admitted data (`contexts` in
   `code/derivation/observe.py`; `wfCtx` in `Basic.lean`; paper §3 item
   3), a profile is a profile of a datum (paper §3 item 5), and `profiles`
   plugs only data numbers below the data count. (`profile`, `separable`
   and `witness` take their data numbers from the caller.) In `R` there is
   one context, `(0, (None,))`, and no datum to plug in, so `profiles`
   asks nothing. That is a fact about how observation calls `derivable`,
   not a restriction on `derivable` itself.

None of this bears on `genesis`, which has no rule; it is here because the
definition is introduced here. Unit 02 uses `R` as the witness that its
no-rules hypothesis cannot be dropped. If a later unit needs derivability
restricted to admitted data, it introduces a separate, named predicate
outside the seal; the sealed `derivable` stays as it is.

## Where the theorem lives

Three things must be kept apart before reading the theorem.

1. **The inscription.** The seed gives one opaque whole, `<>` (Unit 00).
   Nothing in it supplies a regime, a form, an instance or a notion of
   derivation.
2. **The admitted representation.** `Inst`, `Regime`, `genesis` and
   `derivable` above are mathematical apparatus supplied from outside, in
   Lean's metatheory. They are chosen, and the choice is marked admitted.
3. **The theorem.** `genesis_underivable` is proved *inside* that
   representation, about the regime `genesis` and the relation `derivable`.

**We have not derived a regime from ⟨⟩. We have chosen a formal
representation in which to investigate what the initial mark can and cannot
establish.** The theorem needs no extra hypothesis, but it is a theorem about
the chosen representation. It does not show that this representation was
forced, and nothing later in the book shows that either.

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

Read the statement aloud: "for each instance `i`, it is not the case that
`i` is derivable in `genesis`." The `(i : Inst)` before the colon makes `i`
a parameter, so the theorem is a genuine universal statement: it holds of
every instance of Lean's type `Inst`, any form number and any list of data
numbers, including numbers that name no admitted datum. It is proved once,
for an arbitrary `i`, by a proof that never looks at which instance it has;
it is not a collection of separate checks. The quantifier is Lean's, not the
system's: it ranges over a Lean type, and proving it puts no collection of
instances into the system (see **Outside the system** below).

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

The Lean statement covers whatever instance is written down; a script can
only write down a finite list. The check below tries every instance with
form number at most 3 and argument lists of length at most 3 over data
numbers 0 to 3, 340 in all, and confirms none is derivable in `EMPTY`. That
is a sample, not a proof and not an exhaustive verification: the Lean type
`Inst` has no bound, so no finite list exhausts it. The proof is the Lean
above.

```
python textbook/checks/u01_genesis_underivable.py
```

Genesis's own test of the same point is `tests/test_engine.py::
test_challenge0_inertia`, which checks that the list of derivable instances
at Challenge 0 is empty.

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `Nat` | the data count `data`, form numbers, arities, data numbers in an instance | metatheory (paper §2: indices, arithmetic) |
| `List`, `×` | the fields of a regime; an instance as a pair | metatheory (finite data structures) |
| `Prop`, `¬`, `∨`, `∈` | the statement "is derivable" and its negation | metatheory (Lean's logic) |
| `(i : Inst)` | the universal quantifier over the Lean type `Inst`, discharged once for an arbitrary instance | metatheory quantifier |
| Lean's kernel, `intro`, `cases` | checking the proof | metatheory (Unit 00, the external constructor) |

`Nat` and `List Nat` are unbounded types, and so is `Inst`. That is a
property of Lean, not of the system.

**What the system holds.** At `genesis`: a data count of 0 and four empty
lists. No datum, no form, no instance, no rule, no demand. In particular it
holds no collection of "all instances" for the theorem to range over; the
range belongs to Lean. Because `rules` is empty, the right half of
`derivable` holds of nothing here. That is a fact about this regime, not
about finite ledgers in general: the regime `R` above holds one form and
one rule, and `derivable R` holds of an unbounded set of instances when
read in Lean.

**Admissions relied on, and their price.** The four definitions `Inst`,
`Regime`, `genesis`, `derivable` (admitted, paper §3). No event, no
hypothesis, no axiom.

**Phrases to read with care.**

- "No instance is derivable" is the metatheory's universal statement about
  the system, at full strength: proved once, uniformly, for an arbitrary
  instance of a Lean type. What sits outside the system is the quantifier
  and its range, not any weakness in the statement. It does not give the
  system a totality of instances that are all underivable.
- "The ledger is finite" means what is stored is finite. It does not mean
  `derivable` holds of finitely many instances: with one admitted rule it
  holds of an unbounded set read in Lean (regime `R` above).
- "Any form number, any list of data" names Lean's numbers. The system has
  no form numbers yet.
- "However many data and forms it holds" (in Unit 02) means however many a
  finite history has admitted, never an unbounded supply.

## What it shows, and what it does not

It shows that the starting ledger supports no judgment instance: none is
derivable under the declared inference mechanism, not even one about ⟨⟩,
because there is no admitted instance and no admitted rule. This is a claim
about derivability inside the admitted judgment system. It is not a claim
about truth outside it, and Lean's own metatheory, in which the theorem is
proved, is full of true statements.

It does not show that nothing will ever follow. Later events can admit forms
and instances. That nothing *must* follow, that no next step is forced, is a
different claim, and Genesis marks it admitted rather than proved
(Unit 04).

It does not show that the room is empty because ⟨⟩ is "nothing". The ledger
is empty because no admission event has happened. Whether ⟨⟩ belongs in it
is the open question of Unit 05.

It does not show that the representation is the right one. The theorem is
exact inside `Regime` and `derivable`; why the starting point should be
modelled this way at all is admitted, not proved (Unit 00).

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
| Check (rule extension) | `textbook/checks/u01_rule_extension.py`; uses `replay`, `AdmitForm`, `AdmitRuleAll` (`model.py`) and `contexts`, `plug` (`observe.py`) |
| Context well-formedness | `lean4/Derivation/Basic.lean` line 106, `wfCtx` |
