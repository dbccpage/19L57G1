# Unit 16. The demand is not met: ⟨A⟩ and ⟨AB⟩ are collapsed

**Claim.** When the caller requires ⟨A⟩ and ⟨AB⟩ to be internally
separable, the regime as it stands after Challenge 2 cannot comply: the
pair is collapsed, so no witness context exists. In reading L this is
`collapsed R2L 0 1`; in reading F, `collapsed R2F 1 2`, and the other two
pairs with it. **Status:** derived. **Lean:** `Derivation.R2L_collapsed`,
`Derivation.R2F_collapsed` (`lean4/Derivation/Inertia.lean` lines 48-55),
read through `Derivation.separable_not_collapsed` (`Basic.lean` lines
127-130). **Axioms:** `propext`. **Depends on:** `collapsed_of_no_insts`
(Unit 10), `separable_not_collapsed` (Unit 09), `R2L`, `R2F` (Unit 05),
the demand event `impose` (Unit 17).

Unit 10 proved these two theorems as instances of the general collapse
lemma. This unit reads them as the answer to a question the caller asks:
*the system has been told to tell the two apart; can it?* That reading
is the paper's §7.1 and the ledger's `CL-3-FAIL-CURRENT`, and it is the
reason the rest of Part I exists.

## Question

Challenge 3 is the first time the outside asks the system for something
rather than giving it something. The caller imposes a **separation
requirement**: ⟨A⟩ and ⟨AB⟩ must be internally separable. Does the
regime already satisfy it? If not, is the failure a matter of not having
looked hard enough for a witness, or is a witness impossible?

## What we already possess

- `collapsed r d d'` and `separable r d d'` (Unit 08), and the fact that
  a separable pair is never collapsed (Unit 09).
- `collapsed_of_no_insts`: no instances, every pair collapsed (Unit 10),
  with `R2L_collapsed` and `R2F_collapsed` as instances.
- `R2L = ⟨2, [], [], [], [(0, 1)]⟩` and `R2F = ⟨3, [], [], [], [(1, 2)]⟩`
  (Unit 05): two and three data, no forms, no instances, no rules, and
  one recorded demand each.

## New concept: a demand and its failure

A **demand** is the pair `(i, j)` in the field `reqs`. It is put there by
the event `impose i j` (Unit 17). It says what the caller wants, not what
the system can do. Whether the system *meets* the demand is a separate
question: it does so exactly when `separable r i j`.

Genesis answers it by contraposition. It does not search for a witness
and fail to find one; it proves there is none. `R2L_collapsed` says
every well-formed context agrees on 0 and 1. `separable_not_collapsed`
says a witness would contradict that. So `¬ separable R2L 0 1`.

The book adds a sharper remark: in these regimes there is no well-formed
context *at all*, witness or not, since `wfCtx` requires a form and no
form has been admitted. That is why the Python `witness` returns `None`
after inspecting an empty list of contexts.

## Plain-language interpretation

The outside says: "these two are different, show me." The system's whole
vocabulary for differences is contexts over admitted forms. It has no
forms, so it has no sentences, so it cannot show anything. The failure is
not a shortfall of effort; it is a shortfall of language. That is exactly
what the next units price: what is the least that has to be admitted
before the demand can be met (Unit 18), and what are the ways of meeting
it (Units 19 to 22)?

Two things the failure is not. It is not the metatheory failing: the
indices 0 and 1 are different, and Lean proves `0 ≠ 1` in one step
(book Lean `indices_differ`). And it is not a ban: nothing forbids a
later admission that separates the pair. The regime is behind the
demand, not against it.

## Pseudocode

```
# Gloss
demand := (0, 1) recorded in R2L.reqs
meets(demand) := exists well-formed context c with
                 derivable(plug(c, 0)) ≠ derivable(plug(c, 1))
R2L has no instances            -- Unit 10
so every context agrees on 0, 1 -- collapsed
so no context disagrees         -- not separable
so meets(demand) is false.
Stronger: R2L has no forms, so it has no well-formed context c at all.
```

## Python

```python
from derivation.engine import GENESIS_L, READING_L, challenge3_report
from derivation.model import Impose, replay, step
from derivation.observe import contexts, satisfies, separable, witness
from derivation.candidates import Bounds

r = replay(GENESIS_L)
print(r.data, len(contexts(r)), separable(r, 0, 1), witness(r, 0, 1))
print(satisfies(step(r, Impose(0, 1))))
print(challenge3_report(READING_L, Bounds(2, 2))["current_regime_satisfies"])
```

Output:

```text
('<a>', '<ab>') 0 False None
False
False
```

## Line-by-line Python explanation

`replay(GENESIS_L)` rebuilds the reading-L regime from its recorded
history (Unit 05). Its data are the two tokens; it has no forms.

`contexts(r)` (`observe.py` lines 37-45) lists every context: for each
form, every slot tuple with at least one hole. With no forms the loop body
never runs, so the tuple is empty, `0`.

`separable(r, 0, 1)` (line 68) compares the two profiles. Both are empty
sets, so they are equal: `False`. `witness(r, 0, 1)` (lines 72-79) walks
the (empty) contexts looking for one that disagrees and returns `None`.

`step(r, Impose(0, 1))` records the demand (Unit 17), and `satisfies`
(line 97) asks whether every recorded demand is met: `False`.

One difference between the two models is worth knowing. In Lean the
demand is part of `R2L`; in Python the reading-L base regime carries no
demand, and the target pair is passed separately (`READING_L.target`,
`engine.py` line 89). `challenge3_report` (lines 230-287) reads
separability of the base at the target: `current_regime_satisfies` is
`False`, and the artifact records the same value for both readings.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean lines 48-55
/-- Challenge 2 (reading L): the two admitted, externally distinct data are
observationally collapsed. -/
theorem R2L_collapsed : collapsed R2L 0 1 :=
  collapsed_of_no_insts R2L rfl 0 1

/-- Challenge 2 (reading F): all three pairs are collapsed. -/
theorem R2F_collapsed (d d' : Nat) : collapsed R2F d d' :=
  collapsed_of_no_insts R2F rfl d d'
```

```lean
-- Lean (book), textbook/checks/u16_lean.py
theorem demand_fails_L : ¬ separable R2L 0 1 :=
  fun h => separable_not_collapsed h R2L_collapsed

theorem no_context_L (c : Ctx) : ¬ wfCtx R2L c :=
  fun h => Nat.not_lt_zero _ h.1

theorem collapsed_of_not_separable (r : Regime) (d d' : Nat)
    (h : ¬ separable r d d') : collapsed r d d' :=
  fun c hc => Decidable.of_not_not (fun hn => h ⟨c, hc, hn⟩)
```

## Line-by-line Lean explanation

`R2L_collapsed` applies the general lemma to `R2L`. Its second argument,
`rfl`, proves `R2L.insts = []`: the instance list of `R2L` *is* the empty
list by definition, so reflexivity closes it. The last two arguments name
the pair. `R2F_collapsed` takes the pair as parameters, so it covers all
three pairs of reading F at once.

`demand_fails_L` (book): `h : separable R2L 0 1` is assumed;
`separable_not_collapsed h` is a proof of `¬ collapsed R2L 0 1`; applied
to `R2L_collapsed` it yields `False`. A function from `separable` to
`False` is the definition of `¬ separable`.

`no_context_L` (book): `h : wfCtx R2L c` is a four-part conjunction
(Unit 08); `h.1 : c.form < R2L.forms.length`. The form list is `[]`, so
the length is `0`, and `Nat.not_lt_zero` says nothing is below `0`.

`collapsed_of_not_separable` (book) is the converse of Unit 09, and it
shows why the two notions are exact opposites here. `collapsed` asks, for
each well-formed `c`, for the iff. Given `¬ separable`, the iff cannot
fail, since a failing `c` would be a witness; `Decidable.of_not_not`
turns "not not iff" into "iff", and it may do so because derivability is
decidable (Genesis declares the instance at `Basic.lean` lines 88-89).
No classical axiom is used; the axiom report shows only `propext` and
`Quot.sound`, the latter from the `decide`-style instance.

**Axioms.** `propext` for the two Genesis theorems and for the book's
failure theorems; `propext, Quot.sound` where `decide` checks a concrete
membership (`demand_recorded_L`) or the decidable instance is used.

## What has been proved

- `collapsed R2L 0 1` and `collapsed R2F d d'` for all `d, d'` (Genesis,
  derived).
- Hence `¬ separable R2L 0 1` and `¬ separable R2F 1 2` (book, derived,
  one line each from Unit 09).
- Neither regime has any well-formed context (book, derived).
- In general, a pair that is not separable is collapsed, by decidability
  of derivability (book, derived).
- The demand is recorded in `reqs` in both readings (book, by `decide`).

## What has not been proved

- That the demand *cannot* be met. The next units show it can, at a cost
  of two items.
- That the two data are "really" different. The metatheory knows they
  are, by index and by token; the system does not. Nothing in this unit
  carries the metatheory's `0 ≠ 1` across (Unit 15 is the general form of
  that gap).
- Anything about the pairs reading F does not demand. They are collapsed
  too (`R2F_all_pairs`), but no requirement names them, and the
  derivation never asks the system to separate them.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `(0, 1)` in `reqs` | the demand | admitted by the caller through `impose` (Unit 17) |
| `Nat.not_lt_zero`, `Nat.zero_ne_one` | the book's remarks | the metatheory's arithmetic on indices |
| `Decidable.of_not_not` | the converse of Unit 09 | the metatheory's logic, licensed by the declared decidability of `derivable` |
| `READING_L.target` in Python | the demand, kept outside the base regime | a modelling choice of the Python side; the Lean regime records it inside |

**What the system holds.** Two (or three) data and a demand. No form,
no instance, no rule, no context. The demand is a constraint the outside
has placed; the system has not acknowledged it, cannot read it, and has
no state that mentions it except the `reqs` entry itself.

**Phrases to read with care.**

- "The system fails the demand" means `¬ separable`. It does not mean the
  system did anything; it has no actions of its own (Unit 04).
- "Externally distinct" (the Lean docstring) is the metatheory's
  statement about tokens. It is the premise of the challenge, not a fact
  the system has.

## Student exercise

Reading F has three data. The caller demands `(1, 2)`. Suppose instead
the caller demanded `(0, 2)`: ⟨⟩ against ⟨AB⟩. Is that demand admissible
by the guard of Unit 17? Is it met? Which theorem decides it, and with
which arguments?

## Answer

`impose 0 2` on `R2F` is admissible: `0 < 2` and `2 < 3`. It is not met:
`R2F_collapsed 0 2 : collapsed R2F 0 2`, and `separable_not_collapsed`
turns that into `¬ separable R2F 0 2`. The general theorem covers every
pair because `R2F_collapsed` quantifies over `d` and `d'`; no new proof
is needed for a new demand. The Python check confirms it on the
reading-F regime: `collapsed_pairs` lists all three pairs.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Inertia.lean` lines 48-55; `Basic.lean` lines 127-130 (`separable_not_collapsed`), 208-209 (`R2L`, `R2F`) |
| Axiom report | `artifacts/lean_axioms.txt`: `R2L_collapsed`, `R2F_collapsed`, `separable_not_collapsed` each `[propext]` |
| Paper | `paper/paper.md` §6 second bullet, §7.1 (**[theorem]** "The current regime fails it; no witness context exists") |
| Ledger | `paper/paper_claim_ledger.md`, `CL-3-FAIL-CURRENT` (with the 2026-08-18 axiom correction), `CL-2-COLLAPSED` |
| Artifact | `artifacts/challenges.json`, `challenge3.L.current_regime_satisfies = false`, `witness = null`, and the same for `F`; `artifacts/claims.json`, `CL-3-FAIL-CURRENT = {L: false, F: false}` |
| Test | `tests/test_engine.py::test_challenge3_reading_l_classes` (`current_regime_satisfies is False`, `witness is None`) |
| Check (Python) | `python textbook/checks/u16_demand_fails.py`: both readings, no contexts, no witness, demand unmet; artifact and claims agree; 170 instance-free regimes with a demand imposed, none satisfied |
| Check (book Lean) | `python textbook/checks/u16_lean.py`: nine book theorems plus three Genesis theorems kernel-checked, Lean 4.33.0; `propext` throughout, `propext, Quot.sound` for `decide` and for the decidable converse, `indices_differ` axiom-free |
