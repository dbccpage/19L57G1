# Unit 02. Nothing is derivable without instances or rules

**Claim.** In any regime with no admitted instances and no admitted rules,
no judgment instance is derivable, however many data, forms and demands the
regime holds. **Status:** derived. **Lean:**
`Derivation.underivable_of_empty` (`lean4/Derivation/Inertia.lean`, line
30). **Axioms:** none.
**Depends on (admitted):** `Inst`, `Regime`, `derivable` (Unit 01).

Unit 01 proved this for one regime, `genesis`. This unit proves it for every
regime whose two "source" fields are empty, and then shows that neither
condition can be dropped. The proof uses one new move, rewriting with an
equation, and that move is the whole difference between the two units.

## What you need first

### 1. Instances, regimes, derivability

The three definitions are Unit 01's, unchanged:

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean lines 21, 53, 85
abbrev Inst := Nat × List Nat

structure Regime where
  data  : Nat
  forms : List Nat
  insts : List Inst
  rules : List Nat
  reqs  : List (Nat × Nat)

def derivable (r : Regime) (i : Inst) : Prop :=
  i ∈ r.insts ∨ i.1 ∈ r.rules
```

```
# Gloss
inst is derivable in r  if
    inst was admitted as an instance             (looks at r.insts)
 or its form carries the all-instances rule      (looks at r.rules)
```

Read `derivable` once more with this unit's question in mind. It looks at
exactly two fields of the regime, `insts` and `rules`. It never looks at
`data`, `forms` or `reqs`. Everything in this unit follows from that.

`genesis` (Unit 01) is not used by the theorem. It comes back below as one
case of it.

### 2. Equality between Lean values

```
r.insts = []
```

This is Lean's equality, a proposition: "the `insts` field of `r` is the
empty list". A proof of it is something Lean can use to replace one side by
the other. Unit 01 never needed this, because there `r` was the specific
regime `genesis`, whose fields Lean can compute. Here `r` is an arbitrary
regime, and Lean cannot compute its fields. The hypothesis `r.insts = []`
supplies the fact Lean cannot work out.

**Status:** metatheory (Lean's logic). See **Outside the system**.

### 3. A hypothesis is a premise, not an admission

The theorem has two hypotheses, `hi : r.insts = []` and `hr : r.rules = []`.
They are premises of an implication: "if `r` has no instances and no rules,
then nothing is derivable in `r`". The theorem proves that implication with
no premise left over, so it is **derived**, not **conditional**. The README's
mark **conditional** is for a result proved only under a hypothesis admitted
from outside and never discharged, such as irreflexivity in Unit 24; here
nothing is admitted beyond the three definitions. To *use* the theorem on a particular regime you must supply
proofs of the two premises for that regime. Each use pays that price
separately (below: `genesis` and the Challenge 3 regime pay it with `rfl`).

## Where the theorem lives

As in Unit 01: the theorem is proved inside the admitted representation, in
Lean's metatheory, about the relation `derivable`. It is not derived from
⟨⟩, and it does not show that the representation was forced (Unit 00).

## The theorem

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean lines 27-35
/-- Nothing is derivable in any regime with no instances and no rules;
in particular no successor is generated internally: the only state
changes in the model are indexed by external events (`stepE`). -/
theorem underivable_of_empty (r : Regime) (hi : r.insts = [])
    (hr : r.rules = []) (i : Inst) : ¬ derivable r i := by
  intro h
  cases h with
  | inl h => rw [hi] at h; cases h
  | inr h => rw [hr] at h; cases h
```

Read the statement aloud: "for each regime `r`, if `r` has no instances and
`r` has no rules, then for each instance `i`, `i` is not derivable in `r`."
There are two universal quantifiers, over Lean's type `Regime` and over
Lean's type `Inst`. Both are genuine: the theorem is proved once, for an
arbitrary `r` and an arbitrary `i`, by a proof that never looks at which
regime or which instance it has. Both quantifiers are Lean's, not the
system's (see **Outside the system**).

Two things the statement does not ask for:

- **No well-formedness.** There is no hypothesis `r.wf`. The theorem covers
  every value of type `Regime`, including ones with out-of-range instances
  or demands that no admission history could produce. That makes the
  theorem stronger, not weaker; it does not make those regimes part of the
  system.
- **Nothing about `data`, `forms`, `reqs`.** They may hold anything.

**The docstring says more than the theorem.** Its second clause, "in
particular no successor is generated internally", is not what the theorem
states. The theorem is about `derivable`; it says nothing about which
regime comes next. The paper keeps the two apart: the derivability clause is
**[theorem]**, and "no successor is internally forced" is a structural
observation about the declared grammar, not a proved theorem (`paper/paper.md`
§4; ledger `CL-0-INERTIA`, scope stated 2026-09-08). This book follows the
paper. The structural observation is Unit 04, marked admitted.

## The proof, step by step

**Step 0. What `¬` means.** As in Unit 01: `¬ P` is `P → False`.

**Step 1. `intro h`.** Assume `h : derivable r i`. We must produce `False`.
At this point Lean also holds `r`, `hi`, `hr` and `i`, the four inputs
before the colon.

**Step 2. Unfold.** `derivable r i` is by definition
`i ∈ r.insts ∨ i.1 ∈ r.rules`.

**Step 3. `cases h with`.** Split the `∨` into its two ways of being built,
exactly as in Unit 01.

**Step 4. Case `inl`.** Now `h : i ∈ r.insts`. Here Unit 01 and Unit 02
part ways. In Unit 01 the regime was `genesis`, and Lean could compute
`genesis.insts` to `[]` by itself. Here `r` is arbitrary, and Lean cannot
compute `r.insts`. Leave out the `rw` and write `cases h` directly, and Lean
refuses: "Dependent elimination failed: Failed to solve equation
`r.3 = i :: as✝`". It cannot decide whether `r.insts` (written `r.3`, the
third field) has a first element. (The book ran this variant with Lean
4.33.0 to quote the message; it is not in any file.)

`rw [hi] at h` fixes this. `rw` ("rewrite") takes the equation
`hi : r.insts = []` and replaces every occurrence of its left side,
`r.insts`, by its right side, `[]`, inside `h`. After it,
`h : i ∈ []`.

Now `cases h` closes the case for Unit 01's reason: membership in a list is
built only by two constructors, both for a list with a first element, and
`[]` has none.

**Step 5. Case `inr`.** Now `h : i.1 ∈ r.rules`. `rw [hr] at h` turns it
into `h : i.1 ∈ []`, and `cases h` closes it the same way.

**Step 6. Done.** Neither way of being derivable is possible, so
`¬ derivable r i`.

What the proof never looked at: `i`, `r.data`, `r.forms`, `r.reqs`. The two
equations did all the work.

**Axioms.** `artifacts/lean_axioms.txt` line 3 reads
`'Derivation.underivable_of_empty' does not depend on any axioms`
(printed from `lean4/Derivation.lean` line 76), so the rewriting added no
axiom. To check its own Lean, the book compiled `Basic.lean` and
`Inertia.lean` with Lean 4.33.0, the pinned toolchain, and that build
printed the same report. It did not run Genesis's gates.

## Two cases of the theorem

The book's own Lean below (**Lean (book)**, see the README) applies the
theorem to two regimes. It was kernel-checked against Genesis's compiled
`Derivation` library with Lean 4.33.0 by `textbook/checks/u02_lean_witnesses.py`;
it is not part of Genesis's build or its axiom report. Each line was
reported free of axioms.

```lean
-- Lean (book), textbook/checks/u02_lean_witnesses.py
theorem genesis_case (i : Inst) : ¬ derivable genesis i :=
  underivable_of_empty genesis rfl rfl i

theorem r2l_case (i : Inst) : ¬ derivable R2L i :=
  underivable_of_empty R2L rfl rfl i
```

**Unit 01 is a case of Unit 02.** `genesis` has empty `insts` and empty
`rules`, so both premises hold, and Lean checks each with `rfl` ("both sides
compute to the same thing"). Genesis proves the two theorems separately; the
book's line shows that the first follows from the second. **Status:**
derived (book Lean).

**A demand is not a derivation.** `R2L` is Genesis's regime for Challenge 3
in reading L:

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean line 208
def R2L : Regime := ⟨2, [], [], [], [(0, 1)]⟩
```

Two admitted data, ⟨A⟩ and ⟨AB⟩ in the book's notation, no forms, no
instances, no rules, and one demand imposed from outside: separate datum 0
from datum 1. The theorem applies, so nothing is derivable in `R2L`. The
demand changes what is *required* of the next step; it derives nothing by
itself. Two admitted data do not derive anything either. **Status:**
derived (book Lean).

## Neither premise can be dropped

Each premise is needed. A theorem without `hr` would be false, and so would
one without `hi`. Two small regimes show it.

```lean
-- Lean (book), textbook/checks/u02_lean_witnesses.py
/-- Drop the no-rules hypothesis: one unary form with the rule on it. -/
def R : Regime := ⟨0, [1], [], [0], []⟩

/-- Drop the no-instances hypothesis: one datum, one unary form, one
admitted instance. -/
def R' : Regime := ⟨1, [1], [(0, [0])], [], []⟩

theorem R_wf : R.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [R]

theorem R'_wf : R'.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [R']

theorem R_replays :
    replayE [.admitForm 1, .admitRuleAll 0] genesis = some R := by
  decide

theorem R'_replays :
    replayE [.admitDatum, .admitForm 1, .admitInst 0 [0]] genesis = some R' := by
  decide

theorem R_insts : R.insts = [] := rfl

theorem R_derives : derivable R (0, [99]) :=
  Or.inr (List.Mem.head [])

theorem R'_rules : R'.rules = [] := rfl

theorem R'_derives : derivable R' (0, [0]) :=
  Or.inl (List.Mem.head [])

theorem R'_not_derives : ¬ derivable R' (0, [1]) := by
  intro h
  cases h with
  | inl h =>
    cases h with
    | tail _ h => cases h
  | inr h => cases h
```

**`R`, a rule and no instance.** `R` is Unit 01's regime: one unary form,
the all-instances rule on it, no data, no instances. It satisfies `hi`
(`R_insts`) and fails `hr`. And `derivable R (0, [99])` holds: the right half
of `derivable` needs only `0 ∈ [0]`, which `List.Mem.head` proves. Datum 99
was never admitted; `R` admits no datum at all.

**`R'`, an instance and no rule.** `R'` admits one datum, one unary form and
one instance, `(0, [0])`: "form 0 holds of datum 0". It satisfies `hr`
(`R'_rules`) and fails `hi`. `derivable R' (0, [0])` holds by the left half.

**Both are ordinary regimes.** Each is well formed (`R_wf`, `R'_wf`, proved
the way Genesis proves `R2L_wf`, Basic.lean line 211), and each is reached
from `genesis` by a short admission history that Genesis's own replay
accepts (`R_replays`, `R'_replays`, using `replayE`, Basic.lean line 166).
So neither premise can be weakened to "well-formed" or "reachable".

**Status:** derived (book Lean). Reported axioms: none for `R_derives`,
`R'_derives`, `R'_not_derives`, `R_insts`, `R'_rules`; `propext` and
`Quot.sound` for `R_wf` and `R'_wf` (from `simp`); `propext` for the two
replay lines (from `decide`). All lie inside Genesis's own axiom boundary
`{propext, Quot.sound}`.

**What the two witnesses teach.** The two halves of `derivable` reach very
differently.

- An admitted instance reaches exactly itself. In `R'`, `(0, [0])` is
  derivable and `(0, [1])` is not (`R'_not_derives`). The left half of
  `derivable` reaches only the instances listed in `insts`: one, in `R'`.
- An admitted rule reaches every instance of its form that Lean can write
  down, whatever its arguments: `(0, [99])`, `(0, [])`, `(0, [1, 2, 3])`
  (Unit 01, **A finite ledger, an unbounded extension**). One admitted item,
  an unbounded extension when the metatheory reads it.

So the two premises guard against two different things. `hi` rules out
pointwise derivations, one per admitted instance. `hr` rules out the
uniform rule, which on its own makes `derivable` hold of an unbounded set
read in Lean.

## The same fact in Python

The check runs Genesis's own model. It builds 43 regimes by Genesis's
`replay`, each with no `AdmitInst` and no `AdmitRuleAll` event: 0 to 3 data,
at most two forms of arity 1 or 2, and either no demand or every demand
`i < j`; plus `R2L`, built from `AdmitDatum("<a>")`, `AdmitDatum("<ab>")`,
`Impose(0, 1)`. In each it tries Unit 01's 340 instances (form 0 to 3, 0 to
3 arguments over data numbers 0 to 3) and finds none derivable: 14 620
evaluations. That is a sample, not a proof and not an exhaustive
verification; Lean's types `Regime` and `Inst` have no bound. The proof is
the Lean above.

It then builds `R` and `R'` by replay and evaluates the three witness lines,
and counts what each reaches in the sample: in `R`, all 85 sampled instances
of form 0; in `R'`, exactly one.

```
python textbook/checks/u02_underivable_of_empty.py
python textbook/checks/u02_lean_witnesses.py
```

The second script needs Lean: it runs `lake env lean` in `lean4/` after
`lake build`, or takes `--lean` and `--lean-path`. Without Lean it exits 2
and checks nothing.

Genesis's ledger entry for the theorem cites the Lean proof and the
Challenge 0 report (`tests/test_engine.py::test_challenge0_inertia`), which
covers `genesis` only.

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `(r : Regime)` | the universal quantifier over Lean's type `Regime`, discharged once for an arbitrary regime | metatheory quantifier |
| `(i : Inst)` | the universal quantifier over Lean's type `Inst` | metatheory quantifier |
| `=` | the premises `r.insts = []`, `r.rules = []` | metatheory (Lean's equality) |
| `rw` | replacing `r.insts` by `[]` inside a hypothesis | metatheory (Lean's tactic language) |
| `intro`, `cases`, `rfl`, `simp`, `decide` | the proof and the book's witnesses | metatheory (the external constructor, Unit 00) |
| `Nat`, `List`, `×`, `Prop`, `¬`, `∨`, `∈` | as in Unit 01 | metatheory |

**What the system holds.** Whatever a finite admission history has put in
the ledger at that moment: a data count, finitely many forms, instances,
rules and demands. The theorem talks about every value of Lean's type
`Regime`, including ones no history reaches. That range is Lean's. The
system holds no collection of "all regimes", and it never holds more than
one regime at a time: the current ledger.

**Admissions relied on, and their price.** The definitions `Inst`,
`Regime`, `derivable` (admitted, paper §3). No event, no axiom. The two
premises are not admissions; each application of the theorem pays them
again, by a proof that the regime in hand has no instances and no rules.
The book's Lean adds `R`, `R'` and the two cases; they are examples written
in the metatheory, not events in any Genesis history. `R` and `R'`'s replay
histories are written out in full above.

**Phrases to read with care.**

- "However many data, forms and demands" means however many a regime
  records, which for a regime reached by admission is however many a finite
  history admitted. It is never an unbounded supply of data in the system.
- "Any regime" is Lean's quantifier over a Lean type. It is not a space of
  regimes the system ranges over.
- "Nothing follows" is about derivability only. It does not say that
  nothing comes next (the docstring's extra clause; Unit 04).
- "The rule reaches every instance of its form" is the metatheory's reading
  of `derivable` on a regime with a rule. The ledger stores one form number.

## What it shows, and what it does not

It shows that data, forms and imposed demands, in any number, derive
nothing on their own. Only the two source fields, `insts` and `rules`, can
make anything derivable, and with both empty nothing is. In particular the
Challenge 3 regime of reading L, with its two admitted data and its imposed
demand, derives nothing: the demand is a requirement on the next step, not
a derivation.

It shows that both premises are needed, by two well-formed, replayable
regimes, one for each.

It does not show that no successor is forced. That is a different claim,
which Genesis marks as a structural observation about the declared grammar
(Unit 04), whatever the theorem's docstring suggests.

It does not show anything about telling data apart. Whether two data can be
distinguished depends on contexts and profiles (Unit 08), not on
`derivable` alone.
The next theorem in `Inertia.lean`, `collapsed_of_no_insts` (line 40), needs
only the first premise: with no instances, every pair of data looks the
same, even when rules are admitted (Unit 10).

It does not show that the representation is the right one (Unit 00).

## Sources

| Item | Where |
|---|---|
| Theorem | `lean4/Derivation/Inertia.lean` lines 27-35, `Derivation.underivable_of_empty` |
| Definitions | `lean4/Derivation/Basic.lean`: `Inst` line 21, `Regime` line 53, `derivable` line 85, `Regime.wf` line 64; `replayE` line 166 |
| Challenge 3 regime | `lean4/Derivation/Basic.lean` line 208, `R2L`; `R2L_wf` line 211 |
| Python | `code/derivation/model.py` (`Regime`, `replay`, the admission events); `code/derivation/observe.py` (`derivable`) |
| Axiom report | `artifacts/lean_axioms.txt` line 3: no axioms |
| Root inventory | `lean4/Derivation.lean` line 76 (`#print axioms`) |
| Paper | `paper/paper.md` §4 (Challenge 0): the theorem, and the forcing clause marked structural |
| Ledger | `paper/paper_claim_ledger.md`, `CL-0-INERTIA` |
| Classification | `code/derivation/completion.py`: `underivable_of_empty` is ("generic", "countermodel") |
| Test | `tests/test_engine.py::test_challenge0_inertia` (Challenge 0 only) |
| Check | `textbook/checks/u02_underivable_of_empty.py` (Genesis Python) |
| Check (book Lean) | `textbook/checks/u02_lean_witnesses.py` |
