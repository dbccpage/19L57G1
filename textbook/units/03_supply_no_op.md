# Unit 03. Supplying a token changes nothing

**Claim.** For every regime `r` and every token `t`, the supply event
`.supply t` leaves `r` exactly as it was.

<details><summary>Source and classification record (optional)</summary>

**Status:** derived. **Lean:**
`Derivation.supply_no_op` (`lean4/Derivation/Inertia.lean`, line 17).
**Axioms:** `propext`, inherited from the definition of `stepE`, not from
the proof (see **Axioms**, below).
**Depends on (admitted):** `Regime` (Unit 01), `Event`, `stepE`.

Units 01 and 02 asked what is *derivable* in a regime. This unit asks a
different question: what does an *event* do to a regime? It takes the
simplest event, the supply of a token, and proves that it does nothing. The
proof is one word, `rfl`, and the unit's work is to say why one word is
enough, what it covers, and where its single axiom comes from.

</details>

## Question

Does recording a supply also put its token in the admitted-data ledger?

## First pass

An **event history** lists the inputs passed to the model. **Replay**
applies those events in order to a starting ledger. The history and the
ledger it produces are different records.

### Follow three events

Use the token-aware Python model, starting empty. Its data field keeps
admitted token strings. A **supply** records a presented token but leaves
the ledger unchanged. A datum-admission event runs a different rule.

| Event just recorded | Admitted token strings afterwards |
|---|---|
| Supply “x” | Empty |
| Admit datum “x” | [“x”] |
| Supply “y” | [“x”] |

<details><summary>Predict: does “y” now belong to the admitted-data ledger?</summary>

No. The history records its supply; the ledger still contains only “x”.
Supplying and admitting are separate event kinds under these definitions.

</details>

### Keep the two models separate

Python's datum-admission event takes a token. A fresh token extends its
admitted list; an already admitted token leaves that list unchanged.
Token-erased Lean instead keeps a datum count: its `admitDatum` event
has no token argument and always increases that count by one. Both
models' supply cases leave their ledger fixed.

For the Lean supply theorem, different token arguments give the same
step result. The event values and an external history can still retain
different token arguments. Equal final ledgers do not identify histories.

Change the example by admitting “x” again in Python. Its admitted list
stays [“x”]. This does not make every admission a supply, or change
Lean's different count-increasing event. The formal details below explain
the actual erasure bridge used in [Unit 07](07_erasure.md).

Try the six [changed questions](../core_start_practice.md) before the
[separate answers](../core_start_answers.md). Then continue to
[Unit 04](04_no_forced_successor.md) to distinguish an available event
kind from a supplied policy that chooses events.

<details><summary>More detail: What you need first</summary>

## What you need first

### 1. Regimes

`Regime` is Unit 01's, unchanged:

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean line 53
structure Regime where
  data  : Nat
  forms : List Nat
  insts : List Inst
  rules : List Nat
  reqs  : List (Nat × Nat)
```

Note what it does **not** have: a field for tokens. `data` is a count. The
Lean model is *token-erased*: it counts admitted data and forgets which
token each one came from (`lean4/Derivation/Basic.lean`, module docstring;
paper §3). So a supplied token has nowhere in a Lean regime to go. That is
not yet the theorem, but it is why the theorem is short.

### 2. Events

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean lines 134-141
inductive Event where
  | supply       (token : Nat)
  | admitDatum
  | admitForm    (arity : Nat)
  | admitInst    (form : Nat) (args : List Nat)
  | admitRuleAll (form : Nat)
  | impose       (i j : Nat)
deriving Repr, DecidableEq
```

An `Event` is one entry in a recorded history. There are exactly six kinds.
`supply t` presents the token numbered `t`. The other five admit something
or impose a demand. `inductive` means these six are the only ways to build an
event, which is what lets Lean compute with them by cases.

```
# Gloss
an event is one of:
  supply(token)              present a token from outside
  admitDatum                 add one datum
  admitForm(arity)           add a judgment form
  admitInst(form, args)      add a judgment instance
  admitRuleAll(form)         put the all-instances rule on a form
  impose(i, j)               demand that data i and j be told apart
```

**Status:** admitted (paper §3, item 2).

### 3. One step

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean lines 143-162
/-- One admission step.  `none` signals an ill-formed admission.  A bare
supply provably changes nothing (`supply_no_op`). -/
def stepE (r : Regime) : Event → Option Regime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm a =>
      if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none
  | .admitInst f args =>
      if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data) then
        some { r with insts := insertNew r.insts (f, args) }
      else none
  | .admitRuleAll f =>
      if f < r.forms.length then
        some { r with rules := insertNew r.rules f }
      else none
  | .impose i j =>
      if i < j ∧ j < r.data then
        some { r with reqs := insertNew r.reqs (i, j) }
      else none
```

`stepE r e` is the regime after event `e`, or `none` if `e` is ill formed
in `r`. Its result type is `Option Regime`: either `some s` for a regime
`s`, or `none`. The `Option` is there because five of the six events can be
refused (an arity of 0, an instance on a form that was never admitted, a
demand on a datum that does not exist). One event can never be refused:
`supply`.

Two things to read off the first line, `| .supply _ => some r`:

- The pattern is `.supply _`. The underscore matches any token and gives it
  no name. The right-hand side cannot mention the token, because it has no
  name for it.
- The right-hand side is `some r`, the very regime that came in.

```
# Gloss
step(r, supply(_))   = r                       (never refused)
step(r, admitDatum)  = r with data + 1
step(r, other)       = r with one more item, or "refused"
```

**Status:** admitted (paper §3, item 2: "Admission events").

### 4. Replay

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean lines 164-167
/-- Replay: fold the recorded history over a base regime.  All-or-nothing:
an ill-formed event poisons the whole history. -/
def replayE (h : List Event) (base : Regime) : Option Regime :=
  h.foldlM stepE base
```

`replayE h base` runs the events of `h` in order, starting from `base`,
stopping with `none` at the first refused event. The paper's replay rule
says a regime is *certified* only if it equals the replay of its recorded
history from `genesis` (paper §3, item 2). This unit uses `replayE` only in
its consequences, not in the theorem.

**Status:** admitted.

</details>

<details><summary>More detail: Where the theorem lives</summary>

## Where the theorem lives

As in Units 01 and 02: the theorem is proved inside the admitted
representation, in Lean's metatheory, about the function `stepE`. It says
what that function does on supply events. It is not derived from ⟨⟩, and
it does not show that "supply" is the right name for an event that does
nothing (Unit 00).

</details>

<details><summary>More detail: The theorem</summary>

## The theorem

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean lines 16-18
/-- A bare supply changes no admitted state (supply is not admission). -/
theorem supply_no_op (r : Regime) (t : Nat) :
    stepE r (.supply t) = some r := rfl
```

Read it aloud: "for each regime `r` and each token number `t`, one step of
supplying `t` to `r` gives back `r`." Two universal quantifiers, over Lean's
types `Regime` and `Nat`. As always in this book, both are proved once, for
an arbitrary `r` and an arbitrary `t`, and both are Lean's quantifiers, not
the system's (see **Outside the system**).

What the statement does not ask for: no well-formedness of `r`, no
condition on `t`. It covers every value of type `Regime`, and every token
number, whether or not a datum was ever admitted from it.

</details>

<details><summary>More detail: The proof, step by step</summary>

## The proof, step by step

The proof is `rfl`: "both sides are the same, by computation". Here is what
Lean does to accept it.

**Step 0. What `rfl` proves.** `rfl : a = a`. It proves an equation only
when Lean can turn the left side into the right side (or both into a
common form) by unfolding definitions and computing. If that works, the
equation holds by definition and nothing more is needed.

**Step 1. The left side.** `stepE r (.supply t)`. Lean looks up `stepE`.
It is defined by cases on its event argument.

**Step 2. Pick the case.** The event is `.supply t`: built by the
constructor `supply`. Lean does not need to know what `t` is to see which
constructor built the event. So it can choose the first case,
`| .supply _ => some r`, even though `t` is an arbitrary number.

**Step 3. Compute.** That case returns `some r`. The `r` here is the same
`r` that was passed in. Lean does not need to know anything about `r`
either: the case does not look inside it. So the left side computes to
`some r`.

**Step 4. Compare.** The right side is `some r`. The two are now
identical, and `rfl` is accepted.

**Step 5. Why it covers every `r` and every `t`.** Steps 2 and 3 never
asked what `r` or `t` is. The computation goes through with both left as
variables. That is what "proved once, for an arbitrary `r` and `t`" means
here: there is one computation, and it does not branch on the input.

**Contrast with Unit 02.** In Unit 02, `cases h` on `h : i ∈ r.insts`
failed for an arbitrary `r`, because Lean could not compute `r.insts`
without knowing `r`. Here nothing about `r` has to be computed. The supply
case passes `r` through untouched, so its contents never matter.

### Axioms

`artifacts/lean_axioms.txt` line 1 reads
`'Derivation.supply_no_op' depends on axioms: [propext]` (printed from
`lean4/Derivation.lean` line 74). Units 01 and 02 had no axioms. Why does a
one-word proof that computes need one?

`#print axioms` lists every axiom reachable from a theorem: from its proof
**and from every definition its statement mentions**, and so on down. The
statement of `supply_no_op` mentions `stepE`, and `stepE`'s definition
reaches `propext` through two helpers used in its *other* cases:

- Lean's library function `List.getD`, in the `admitInst` case
  (`r.forms.getD f 0`, the arity of form `f`);
- Genesis's `insertNew` (`lean4/Derivation/Basic.lean` line 25), in the `admitInst`,
  `admitRuleAll` and `impose` cases, whose membership test `a ∈ l` is
  decided by a Lean library instance that uses `propext`.

The supply case and the proof `rfl` use neither. The book checked this with
its own Lean (below): `#print axioms` reports `propext` for `stepE`,
`insertNew` and `List.getD`, and reports **no axioms** for a probe function
that keeps only `stepE`'s first two cases and for the same `rfl` proof
about it.

So the right reading of the line in `artifacts/lean_axioms.txt` is: the
claim mentions a definition that depends on `propext`, so the claim does.
The `propext` is a cost of the definition of `stepE`, paid by every theorem
that mentions `stepE`. It is inside Genesis's axiom boundary,
`{propext, Quot.sound}` (`ci/check_lean_audit.py`; CLAUDE.md "The axiom
boundary"). The book compiled `Basic.lean` and `Inertia.lean` with Lean
4.33.0, the pinned toolchain, and that build printed the same report. It
did not run Genesis's gates.

**A correction to Unit 02.** Unit 02 said its replay witnesses got `propext`
"from `decide`" and its well-formedness witnesses got `propext` "from
`simp`". That was wrong as to `propext`: it is already in `replayE` (through
`stepE`) and in `Regime.wf` (through `List.getD`), which those statements
mention. Unit 02 now says so, with a dated note.

</details>

<details><summary>More detail: Consequences in the book's Lean</summary>

## Consequences in the book's Lean

The book's own Lean below (**Lean (book)**, see the README) draws the
following replay and admission consequences and contrast. It was kernel-checked against Genesis's
compiled `Derivation` library with Lean 4.33.0 by
`textbook/checks/u03_lean_witnesses.py`; it is not part of Genesis's build
or its axiom report. **Status of each:** derived (book Lean). Each reported
`propext` and nothing else, for the reason just given: every statement
mentions `stepE` or `replayE`. The probe reported no axioms.

```lean
-- Lean (book), textbook/checks/u03_lean_witnesses.py
/-- The token plays no part: any two supplies have the same outcome. -/
theorem supply_token_irrelevant (r : Regime) (t u : Nat) :
    stepE r (.supply t) = stepE r (.supply u) := rfl

/-- Admission is different: admitting a datum always changes the regime. -/
theorem admitDatum_changes (r : Regime) : stepE r .admitDatum ≠ some r := by
  intro h
  have h2 : r.data + 1 = r.data := congrArg Regime.data (Option.some.inj h)
  exact Nat.succ_ne_self r.data h2

/-- Admission does not wait for a supply: a history with no supply admits. -/
theorem admit_without_supply :
    replayE [.admitDatum] genesis = some ⟨1, [], [], [], []⟩ := rfl

/-- A supply at the head of a history can be dropped. -/
theorem replay_supply_cons (t : Nat) (h : List Event) (r : Regime) :
    replayE (.supply t :: h) r = replayE h r := rfl

/-- A history made only of supplies replays to its base. -/
theorem replay_only_supplies (h : List Event)
    (hs : ∀ e ∈ h, ∃ t, e = .supply t) (r : Regime) :
    replayE h r = some r := by
  induction h with
  | nil => rfl
  | cons e rest ih =>
    obtain ⟨t, rfl⟩ := hs e (List.Mem.head rest)
    rw [replay_supply_cons]
    exact ih (fun e' he' => hs e' (List.Mem.tail _ he'))

theorem historyL_without_supplies :
    replayE [.admitDatum, .admitDatum, .impose 0 1] genesis = some R2L := by
  decide

theorem historyF_without_supplies :
    replayE [.admitDatum, .admitDatum, .admitDatum, .impose 1 2] genesis
      = some R2F := by
  decide
```

**The token does not affect this step.** `supply_token_irrelevant` says
that token 0 and token 7 give the same `stepE` outcome, by `rfl`. The
`Event` values and histories can still retain different token arguments.
Equality of step results does not equate the events that produced them. The added book theorem
`different_supplies_same_step` checks different supply events 0 and 7
with equal `stepE` results for every regime. Its sole reported axiom
is `propext`, inherited through `stepE`. The updated script checks thirteen
reports: eleven exactly `propext` and two empty sets, including its probes.

**Supply is not admission.** `supply_no_op` alone does not show that supply
and admission differ; it needs a contrast. `admitDatum_changes` is that
contrast in token-erased Lean: for every regime, `admitDatum` gives a
regime with one more datum, so never the regime it started from. The proof: if the two were
equal, their `data` fields would be equal (`congrArg Regime.data`, after
`Option.some.inj` strips the `some`), so `r.data + 1 = r.data`, which
`Nat.succ_ne_self` refutes. Genesis records the bridge "supply is
admission" as false with a countermodel (`code/derivation/completion.py`,
`BRIDGES`), citing `supply_no_op`; these two lines together are that
countermodel in full, for every regime.

**Admission does not wait for a supply.** `admit_without_supply`: a history
with one `admitDatum` and no supply admits one datum. In the model, a supply
is not a precondition of admission. The Challenge histories supply a token
before admitting it because the seed presents tokens that way, not because
`stepE` asks for it.

**A supply can be dropped from any history.** `replay_supply_cons` says a
supply at the head of a history can be removed without changing the replay,
whatever comes after. Its proof is `rfl`: `foldlM` unfolds one step to
`stepE r (.supply t)`, which is `some r`, and continues from `r`.

**A history of supplies alone does nothing.** `replay_only_supplies`
proves, for every history whose events are all supplies, that it replays
to its base. The proof is by induction on the history:

- *Empty history:* replay of `[]` is `some r` by definition (`rfl`).
- *A first event `e` and the rest:* the hypothesis `hs` says `e` is a supply,
  `.supply t` for some `t` (`obtain ⟨t, rfl⟩` takes the `t` and replaces
  `e` by `.supply t`). `replay_supply_cons` drops it. What is left is the
  rest of the history, which again has only supplies (`List.Mem.tail`), so
  the induction hypothesis `ih` finishes.

**The Challenge histories, without their supplies.** Genesis's recorded
history for reading L, `historyL_replays` (Inertia.lean lines 59-63),
has seven events, four of them supplies. Remove the four and the replay
still reaches `R2L`. Reading F (`historyF_replays`, lines 66-70) likewise
reaches `R2F` with its four supplies removed. So everything that Challenges
0 to 2 put into the ledger came from the admissions and the imposed demand.
The supplies are in the record because they happened in the challenge, not
because the regime depends on them.

### The probe

```lean
-- Lean (book), textbook/checks/u03_lean_witnesses.py
/-- A probe, not a model: only the first two cases of `stepE`, every other
event rejected. Used only to locate where `propext` enters. -/
def stepProbe (r : Regime) : Event → Option Regime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm _ => none
  | .admitInst _ _ => none
  | .admitRuleAll _ => none
  | .impose _ _ => none

theorem probe_supply_no_op (r : Regime) (t : Nat) :
    stepProbe r (.supply t) = some r := rfl

#print axioms Derivation.stepE      -- propext
#print axioms Derivation.insertNew  -- propext
#print axioms List.getD             -- propext
```

`stepProbe` is not part of Genesis or of the book's account of Genesis. It
refuses four kinds of event that Genesis accepts, so no claim about
Genesis's regimes is made with it. Its only job is the axiom report: the
probe and its `rfl` theorem report no axioms, so the supply case and the
proof contribute none.

</details>

<details><summary>More detail: The same fact in Python</summary>

## The same fact in Python

Genesis's Python `step` has the same first case:

```python
# Python (Genesis), code/derivation/model.py lines 106-110
def step(r: Regime, e: Event) -> Regime:
    """Apply one event.  Deterministic; raises ``AdmissionError`` on
    ill-formed admissions."""
    if isinstance(e, Supply):
        return r
```

Two differences from the Lean:

- Python's `Supply` carries a token *string* (`Supply("<a>")`), and its
  `Regime.data` is a tuple of token strings, not a count. Python keeps the
  tokens of admitted data; Lean counts them. Either way the supply case
  returns the regime unchanged. The bridge between the two models is
  Genesis's erasure simulation (`lean4/Derivation/Erasure.lean`; Units 06 and
  07), whose token-aware step also passes a supply through unchanged
  (`stepT`, line 41) and whose simulation proof handles the supply case by
  `rfl` (line 83).
- Python returns `r` itself, not `some r`, and signals a refused event by
  raising `AdmissionError` instead of returning `none`.

The check script runs Genesis's own model:

```
python textbook/checks/u03_supply_no_op.py
python textbook/checks/u03_lean_witnesses.py
```

The first script:

1. Builds 50 regimes by Genesis's `replay` (0 to 3 data; no form, one unary
   form, or a unary and a binary form; with or without an admitted
   instance, the all-instances rule, and a demand, wherever these are well
   formed), plus the two Challenge 2 regimes from Genesis's own histories
   `GENESIS_L` and `GENESIS_F` (`code/derivation/engine.py`): 52 in all.
   To each it supplies seven tokens: three that may already be admitted
   (`"<>"`, `"<a>"`, `"<ab>"`), `"d0"`, a fresh `"zz"`, the empty string,
   and a 40-character string. In all 364 cases `step(r, Supply(tok))`
   returns the very object `r`.
2. Replays `GENESIS_L`, `GENESIS_F` and Challenge 1's two sub-reading
   histories with and without their `Supply` events and finds the same
   regime each time.
3. Replays all 40 histories of at most three supplies over three tokens and
   finds `EMPTY` each time.
4. Contrasts: in each of the 52 regimes, `AdmitDatum` of a fresh token
   changes the regime. In each of the 47 that have a datum, `AdmitDatum` of
   an already admitted token does not, which is a different fact about a
   different event (designation, Unit 06).
5. Replays `[AdmitDatum("x")]`, with no supply, and finds one admitted
   datum.

These are finite checks of the native Python implementation. The Lean
proofs establish their stated claims about the token-erased Lean model.
Unit 07 checks an erasure simulation between two Lean models; it does
not supply a general proof that the Python source implements Lean.

Genesis's own tests: `tests/test_model.py::test_supply_is_not_admission`
(`step(EMPTY, Supply(...)) == EMPTY` for two tokens) and
`tests/test_engine.py::test_challenge0_inertia` (`supply_changes_state` is
false at Challenge 0).

</details>

<details><summary>More detail: Outside the system</summary>

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `(r : Regime)`, `(t : Nat)` | the theorem's two universal quantifiers, discharged once for arbitrary values | metatheory quantifiers |
| `Event`, `Option`, `some`, `none` | the type of history entries; the possible outcomes of a step | metatheory (admitted representation) |
| `rfl`, definitional unfolding | the proof | metatheory (Lean's kernel) |
| `List.foldlM` | `replayE`, running a history | metatheory |
| `induction`, `obtain`, `rw`, `congrArg`, `decide` | the book's consequences | metatheory (the external constructor, Unit 00) |
| `#print axioms` | reading the axiom report | metatheory (Lean's tooling) |
| `propext` | an axiom reached through `List.getD` and `insertNew`, not through the proof | metatheory, inside Genesis's declared boundary |

**What the system holds.** The current ledger: a data count, finitely many
forms, instances, rules and demands. A supply puts nothing into it. In the
Lean model there is not even a place a token could go. In the Python model
the ledger records tokens only for *admitted* data. A token that was only
supplied is recorded nowhere in the regime.

**Where the supply is recorded.** In the history: the list of events, kept
outside the regime and used by the replay rule to certify it. The history
is metatheory apparatus (`code/derivation/model.py` docstring: "`Regime`
and `Event` are metatheory apparatus"). So "⟨A⟩ was supplied" is a true
statement about the record, not about the ledger.

**Admissions relied on, and their price.** `Regime`, `Event`, `stepE`,
`replayE` (admitted, paper §3). No event. One axiom, `propext`, reached
through the definition of `stepE` and paid by every claim that mentions it.
The book's Lean adds the consequences and the probe; they are statements
in the metatheory, not events in any Genesis history.

**Phrases to read with care.**

- "Supplying a token" is an event in the external record. It is not
  something the system receives, sees, or stores. There is no internal
  receiver.
- "The system ignores the token" imports an observer that looks at the
  token and then discards it. Read instead: `stepE`'s supply case does not
  depend on the token. Nothing looks.
- "The supplied token is available for admission" is false in the model.
  Admission has no precondition on what was supplied
  (`admit_without_supply`). A token is not "waiting" anywhere.
- "Every token" means every value of Lean's `Nat` (or, in Python, every
  string). It is not a supply of tokens the system has.

</details>

<details><summary>More detail: What it shows, and what it does not</summary>

## What it shows, and what it does not

It shows that a supply event never changes a regime and is never refused,
whatever the regime and whatever the token. With `admitDatum_changes` it
shows that in token-erased Lean supply always leaves the regime fixed
while `admitDatum` always changes its count. Python has a different
datum-admission case: repeated admitted tokens leave its regime fixed. With the replay consequences it
shows that every supply can be removed from any history without changing
where the history leads, so everything in a Genesis ledger was put there by
an admission or an imposed demand.

It does not show that the model's events are the only possible events, or
that nothing else could follow a supply. "No successor is internally
forced" is the structural observation of Unit 04, not a consequence of this
theorem.

It does not say what happens when an *admission* repeats a token already
admitted. In the Python model that is also a no-op, but it is a fact about
`AdmitDatum` and presentation identity, not about `Supply` (Unit 06), and
the token-erased Lean model handles it by turning such an admission into a
supply (Erasure.lean line 66; Unit 07).

It does not show that the Challenge 1 sub-readings (admit ⟨A⟩ on supply, or
not) converge. Genesis computes that convergence (paper §5); it rests on
deduplication of admissions, not on this theorem.

It does not show that the representation is the right one (Unit 00).

</details>

<details><summary>More detail: Sources</summary>

## Sources

| Item | Where |
|---|---|
| Theorem | `lean4/Derivation/Inertia.lean` lines 16-18, `Derivation.supply_no_op` |
| Definitions | `lean4/Derivation/Basic.lean`: `insertNew` line 25, `Regime` line 53, `Event` lines 134-141, `stepE` lines 143-162, `replayE` lines 164-167 |
| Challenge histories | `lean4/Derivation/Inertia.lean`: `historyL_replays` lines 59-63, `historyF_replays` lines 66-70; `code/derivation/engine.py`: `GENESIS_L`, `GENESIS_F` |
| Token-aware model | `lean4/Derivation/Erasure.lean`: `stepT` supply case line 41, `eraseEvent` line 66, `erase_step` supply case line 83 |
| Python | `code/derivation/model.py`: `Supply`, `step` (lines 106-110 for the supply case), `replay` |
| Axiom report | `artifacts/lean_axioms.txt` line 1: `propext` |
| Root inventory | `lean4/Derivation.lean` line 74 (`#print axioms`) |
| Paper | `paper/paper.md` §2 (supply kept apart from admission), §3 item 2 (events and replay), §4 (the theorem), §5 (Challenge 1) |
| Ledger | `paper/paper_claim_ledger.md`, `CL-0-INERTIA`, `CL-0-NO-PROPOSAL-MUTATION`, `CL-1-SUPPLY-NOT-ADMISSION` |
| Classification | `code/derivation/completion.py`: `supply_no_op` is ("generic", "preservation"); bridges "seed forces successor state" and "supply is admission", both FALSE_WITH_COUNTERMODEL |
| Tests | `tests/test_model.py::test_supply_is_not_admission`; `tests/test_engine.py::test_challenge0_inertia` |
| Check | `textbook/checks/u03_supply_no_op.py` (Genesis Python) |
| Check (book Lean) | `textbook/checks/u03_lean_witnesses.py` |

</details>
