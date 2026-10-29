# Unit 07. Forgetting the tokens: the erasure bridge

**Claim.** Replaying a token-aware history (tokens kept, re-admissions
designate) and then forgetting the tokens gives the same ledger as
replaying the *erased* history in the counting model, where each
re-admission has first been turned into a bare supply. This is a sound abstraction between two Lean models for state claims
expressed through that erasure. Python implements the token-aware policy;
its connection to Lean is tested separately, not proved by this theorem.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** derived. **Lean:** `Derivation.erase_step`,
`Derivation.erase_replay` (`lean4/Derivation/Erasure.lean` lines 79-104,
138-158). **Axioms:** `propext`, `Quot.sound`. **Depends on:** `stepE`,
`replayE` (Unit 03), `supply_no_op` (Unit 03), `TRegime`, `stepT`
(Unit 06).

</details>

## First pass

A named store receives ⟨A⟩, ⟨A⟩ again, then ⟨AB⟩. Its counts after
the three events are 1, 1, and 2. A tally clerk who blindly counts
all three admissions would get 3.

Translate the duplicate admission into a supply event, which changes
nothing. The tally clerk now follows `admit, supply, admit` and gets
the same count 2. Whether an event is a duplicate depends on the
store at that point, so the translation must follow the history in order.

The Lean theorem compares two Lean models using this translation,
including refusals. It transports properties expressed through the
erased state. A token's spelling is deliberately absent from that state.
Checks against Python are separate executable evidence.

## Question

Unit 06 left a gap. Python and `stepT` keep tokens and dedup; the Lean
`Regime` that every theorem from Unit 08 on is about keeps only a count and
counts every `admitDatum`. Which claims does the Lean erasure theorem transport, and what still
needs checking before relating them to Python?

## What we already possess

- The counting model: `Regime`, `stepE`, `replayE` (Units 01, 03).
- The token-aware model: `TRegime`, `TEvent`, `stepT`, `replayT`
  (Unit 06).
- `supply_no_op`: a supply changes nothing (Unit 03).
- An `Option` result: `some r` on success, `none` when an event is refused;
  `replayE` and `replayT` stop at the first `none` (Unit 03).

## New concept: a simulation through an erasure map

An **erasure map** forgets part of a state. Here `TRegime.erase` keeps
the four structural fields and replaces the token list by its length:

```lean
-- Lean (Genesis), lean4/Derivation/Erasure.lean lines 62-63
def TRegime.erase (t : TRegime) : Regime :=
  ⟨t.tokens.length, t.forms, t.insts, t.rules, t.reqs⟩
```

Events are erased too, but *relative to the current state*: an admission
of a token already present becomes a supply (which does nothing in either
model); every other event is copied with its token dropped.

```lean
-- Lean (Genesis), lean4/Derivation/Erasure.lean lines 68-75
def eraseEvent (t : TRegime) : TEvent → Event
  | .supply tok => .supply tok
  | .admitDatum tok =>
      if tok ∈ t.tokens then .supply tok else .admitDatum
  | .admitForm a => .admitForm a
  | .admitInst f args => .admitInst f args
  | .admitRuleAll f => .admitRuleAll f
  | .impose i j => .impose i j
```

A **simulation** is a statement of the form: take a step in the detailed
model, then erase, and you get the same thing as erasing first and taking
the corresponding step in the coarse model. Drawn as a square, both paths
round it agree. `erase_step` is the square for one event; `erase_replay`
is the square for a whole history, which needs the history erased with the
state threaded through it (`eraseHistory`), because whether an admission is
a duplicate depends on what came before.

## Plain-language interpretation

Two clerks keep the same guest list. One writes names; the other only
keeps a tally. When a name is called that the first clerk already has, the
first clerk does nothing, and tells the second clerk "that was nobody
new", which the second clerk treats as a non-event. With that one
translation rule, the tally always equals the number of names. The theorem
is that promise, kept for every possible sequence of calls, including ones
that are refused halfway.

The promise transports a counting-state property through the stated
erasure. It does not transport arbitrary token-sensitive properties.
It is a bridge between two *Lean* models. The step from the Lean token-aware model to the actual
Python program is not a theorem; it is tested (`CL-TOKEN-ERASURE`, and the
check below).

## Pseudocode

```
# Gloss
erase(state)            = (number of tokens, forms, insts, rules, reqs)
erase_event(state, e)   = supply(tok)   if e = admit(tok) and tok already present
                        = e with its token dropped, otherwise
erase_history(state, h) = erase each event in turn, threading the state;
                          stop after a refused event

THEOREM: erase(replayT(h, s)) = replayE(erase_history(s, h), erase(s))
```

## Python

Genesis's Python has no erasure function: it is the token-aware side. The
check script writes the gloss of `eraseHistory` in Python and verifies that
erasing a history never changes what Genesis's `replay` returns, and that
the data count equals the number of distinct admitted tokens.

```python
# Python (book), textbook/checks/u07_erasure.py
def erase_history(h: list[Event]) -> list[Event]:
    seen: set[str] = set()
    out: list[Event] = []
    for e in h:
        if isinstance(e, AdmitDatum):
            if e.token in seen:
                out.append(Supply(e.token))
            else:
                seen.add(e.token)
                out.append(e)
        else:
            out.append(e)
    return out
```

```python
h = [AdmitDatum("<a>"), AdmitDatum("<a>"), AdmitDatum("<ab>")]
print(replay(h) == replay(erase_history(h)), len(replay(h).data))
```

Output:

```text
True 2
```

## Line-by-line Python explanation

`seen: set[str] = set()`: a **set**, a collection with no duplicates and no
order, starting empty. It plays the part of `t.tokens` in `eraseEvent`:
the tokens admitted so far.

`out: list[Event] = []`: the erased history being built, starting empty.

`for e in h:`: walk the history in order. Order matters: whether an
admission is a duplicate depends on the admissions before it. This is the
"threading" of the state in `eraseHistory`.

`if isinstance(e, AdmitDatum):` only admissions of data can be duplicates.

`if e.token in seen: out.append(Supply(e.token))`: a duplicate becomes a
supply of the same token, exactly as `eraseEvent`'s second line says.
`append` adds to the end of the list.

`else: seen.add(e.token); out.append(e)`: a first admission is recorded in
`seen` and kept.

`else: out.append(e)`: every other kind of event is kept as it is. (The
Lean `eraseEvent` also drops the token from `admitDatum`; Python's
`AdmitDatum` keeps its token, and that is fine, because a first admission
is never a duplicate, so the two models agree on what it does.)

The example: two admissions of ⟨A⟩ then one of ⟨AB⟩. Erased, the middle
one is a supply. Both histories replay to the two-datum ledger, so the
comparison prints `True`, and the data count is 2.

What this shows: for these histories Python's own dedup agrees with the
erased history. The check script runs all 781 histories of length at most
four over five event atoms. That is a sample, not the theorem; the theorem
is the Lean below.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Erasure.lean lines 79-82 (statement)
theorem erase_step (t : TRegime) (e : TEvent) :
    (stepT t e).map TRegime.erase =
      stepE t.erase (eraseEvent t e) := by
  cases e with
  ...

-- lines 138-158
theorem erase_replay (h : List TEvent) (base : TRegime) :
    (replayT h base).map TRegime.erase =
      replayE (eraseHistory base h) base.erase := by
  induction h generalizing base with
  | nil => rfl
  | cons e rest ih =>
      have hstep := erase_step base e
      rw [replayT_cons]
      cases hs : stepT base e with
      | none =>
          rw [hs] at hstep
          have hE : eraseHistory base (e :: rest) = [eraseEvent base e] := by
            simp [eraseHistory, hs]
          rw [hE, replayE_cons, ← hstep]
          simp
      | some t1 =>
          rw [hs] at hstep
          have hE : eraseHistory base (e :: rest) =
              eraseEvent base e :: eraseHistory t1 rest := by
            simp [eraseHistory, hs]
          rw [hE, replayE_cons, ← hstep]
          simpa using ih t1
```

The book's Lean instantiates the theorem on reading L's history and on a
history with a duplicate, and recovers `historyL_replays` from the
token-aware side.

```lean
-- Lean (book), textbook/checks/u07_lean.py
def tL : List TEvent :=
  [.supply 0, .supply 1, .supply 1, .supply 2, .admitDatum 1, .admitDatum 2, .impose 0 1]

theorem simulation_on_L :
    (replayT tL tgenesis).map TRegime.erase = replayE (eraseHistory tgenesis tL) genesis :=
  erase_replay tL tgenesis

theorem historyL_via_erasure :
    replayE [.supply 0, .supply 1, .supply 1, .supply 2,
             .admitDatum, .admitDatum, .impose 0 1] genesis = some R2L := by
  rw [← tL_erases, ← simulation_on_L]
  exact tL_replays_erased

theorem dup_history_erases :
    eraseHistory tgenesis [.admitDatum 1, .admitDatum 1, .admitDatum 2]
      = [.admitDatum, .supply 1, .admitDatum] := by
  decide
```

## Line-by-line Lean explanation

**`erase_step`, the statement.** `(stepT t e)` is `some t'` or `none`.
`.map TRegime.erase` applies the erasure inside the `some` and leaves
`none` as `none`. The right side first erases the state, `t.erase`, and
the event, `eraseEvent t e`, then takes the counting model's step. The
theorem: the two are equal, for every state and every event.

**`erase_step`, the proof shape.** `cases e with` splits into the six event
kinds. The supply case is `rfl`: both sides are `some` of the erased state.
Each other case does `by_cases h : <the guard>`, splitting on whether the
event is accepted, and then `simp [...]` unfolds both sides and sees they
agree. The admission case is the one that carries the idea: if `tok ∈
t.tokens`, the left side is `some t` erased, and the right side is a
*supply* step on the erased state, which `stepE` returns unchanged
(`supply_no_op`). If not, the left appends a token, so the length rises by
one; the right side's `admitDatum` adds one to the count. Equal.

**`erase_replay`, the statement.** For a whole history `h` and base state:
replay then erase, against replay of the erased history from the erased
base.

**`induction h generalizing base with`.** Proof by induction on the list
`h`. `generalizing base` says: prove it for every base at once, so the
inductive hypothesis can be applied to the *next* state, not only the
original base. Without it the proof would be stuck at the second event.

**`| nil => rfl`.** Empty history: both sides are `some base.erase`.

**`| cons e rest ih =>`.** The history is `e` followed by `rest`, and `ih`
is the statement for `rest` (at every base).

`have hstep := erase_step base e`: the one-step square for the first event.

`rw [replayT_cons]`: rewrite `replayT (e :: rest) base` into "step once,
then bind the rest". `replayT_cons` is a small lemma proved just above.

`cases hs : stepT base e with`: split on whether the first step is refused
(`none`) or succeeds (`some t1`), remembering the outcome as `hs`.

*Refused case.* `rw [hs] at hstep` turns the square into
`none.map erase = stepE base.erase (eraseEvent base e)`, that is, the
erased step is refused too. `hE` computes `eraseHistory` of a history whose
first step is refused: it is the one erased event, then nothing
(`eraseHistory` cuts after a refusal). After rewriting with `hE`,
`replayE_cons` and the square, both sides are `none`; `simp` closes it.

*Accepted case.* `hE` now says the erased history is the erased first event
followed by the erased `rest` from `t1`. Rewriting with `hE`,
`replayE_cons` and the square brings the goal to
`(replayT rest t1).map erase = replayE (eraseHistory t1 rest) t1.erase`,
which is exactly `ih t1`. `simpa using ih t1` finishes.

No step is skipped: each `rw` names its lemma, each case names its
outcome, and the one place the idea enters (duplicate admission erases to
supply) is in `erase_step`'s admission case.

**`historyL_via_erasure`.** The book proves Unit 05's theorem a second
way. `tL_erases` says the erased token history is the exact list in
`historyL_replays`; `simulation_on_L` is the square; `tL_replays_erased`
computes the token side. Rewriting right to left with the first two turns
the goal into the third. Two independent routes to one equality is a check
that the token numbering of Unit 05 was honest.

**`dup_history_erases`.** `decide` computes `eraseHistory` on a history
with a repeat and shows the repeat becomes `.supply 1`.

**Axioms.** Both Genesis theorems report `propext, Quot.sound`
(`artifacts/lean_axioms.txt`): `propext` through `stepE`, `Quot.sound`
through `stepT`'s membership test (Unit 06).

## What has been proved

- One token-aware step, erased, equals one counting-model step of the
  erased event (`erase_step`, derived).
- The same for whole histories, refusals included (`erase_replay`,
  derived).
- Instances: reading L's history; a history with a duplicate; a refused
  history where both replays are `none` and the erased history is cut
  (book Lean).

## What has not been proved

- Anything about the Python program. The theorem relates two Lean models.
  The ledger says so in its endpoints: "the Python implementation is
  connected to the token-aware model by the executable checks named under
  Python, not by any proof over the Python source" (`CL-TOKEN-ERASURE`).
  The check script is one more such executable check.
- That the erasure loses nothing of interest. It loses the tokens and
  their order. Unit 11 shows the loss is exactly what the object level
  cannot see anyway (`Bridge.order_erased_at_object_level`), and the paper
  records a second bridge, membership extensionality (`Ext.lean`), for
  the fact that Python's collections are sets while Lean's are deduplicated
  lists. That second bridge is taught where its theorems are used.
- That every exported claim factors through the observables the bridges
  cover. The ledger narrowed this on 2026-08-18: claims stated at the
  representation level are covered only up to `RegimeExt`.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `List.length`, `Option.map`, `Option.bind`, `List.foldlM` | the erasure and the replays | metatheory library |
| `induction ... generalizing` | the proof of `erase_replay` | metatheory proof principle over Lean's lists |
| `(h : List TEvent) (base : TRegime)` | the universal statement | metatheory quantifiers |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** Nothing new. Erasure is a map between two
*descriptions* of the system kept by the metatheory. The system holds one
ledger; it does not hold both models or the map between them.

**Admissions and their price.** None beyond Unit 06's convention. The
bridge is a theorem about that convention.

**Phrases to read with care.**

- "Lean mirrors Python" is not claimed. The paper's words are "a sound
  abstraction of the token-aware model, not a claim of literal mirroring"
  (`Erasure.lean` header).
- "Tokens are forgotten" means forgotten by the counting model. The
  metatheory keeps them (Unit 00); the system never had them.
- "The two models agree" means: on the admitted state after any history.
  It says nothing about intermediate representations such as list order,
  which the second bridge handles.

## Student exercise

Take the history `[admit 1, admit 2, admit 1, impose 0 1]` from the empty
token-aware state. Write its erased history, its erased final state, and
check the square by hand.

## Answer

Threading the state: `admit 1` (fresh, tokens `[1]`) stays `admitDatum`;
`admit 2` (fresh, `[1, 2]`) stays `admitDatum`; `admit 1` is a duplicate,
becomes `supply 1`; `impose 0 1` is copied. Erased history:
`[admitDatum, admitDatum, supply 1, impose 0 1]`.

Token side: final state `⟨[1, 2], [], [], [], [(0, 1)]⟩`, erased to
`⟨2, [], [], [], [(0, 1)]⟩`, which is `R2L`.

Counting side: two admissions give count 2, the supply does nothing,
`impose 0 1` passes `0 < 1 ∧ 1 < 2`. Result `⟨2, [], [], [], [(0, 1)]⟩`.
The square commutes. (The book Lean's `simulation_on_dup` checks a close
variant by `decide`.)

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Erasure.lean`: `TRegime.erase` 62-63, `eraseEvent` 68-75, `erase_step` 79-104, `replayT` 107-108, `eraseHistory` 113-119, `replayT_cons` 121-125, `replayE_cons` 127-131, `erase_replay` 138-158 |
| Axiom report | `artifacts/lean_axioms.txt`: `erase_step`, `erase_replay` each `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §2, "Erasure simulation" **[theorem]**, and the endpoint statement of 2026-09-08 |
| Ledger | `paper/paper_claim_ledger.md`, `CL-TOKEN-ERASURE` (both components; the 2026-08-18 narrowing) |
| Check (Python) | `python textbook/checks/u07_erasure.py`: 781 histories of length ≤ 4 over five atoms, erased replay equals replay and data count equals distinct admitted tokens; `GENESIS_L` and `GENESIS_F` are fixed by erasure; a duplicate followed by structure |
| Check (book Lean) | `python textbook/checks/u07_lean.py`: eight book theorems plus `erase_step` and `erase_replay` kernel-checked, Lean 4.33.0; all report `propext, Quot.sound` |
