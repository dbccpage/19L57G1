# Unit 13. Two data need a second, different token

**Claim.** If a history run from the empty token-aware state ends with two
or more admitted data, then some event of that history admits a token
different from any given token `t0`. In particular two data never come
from one inscription alone: two-ness is purchased from outside.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** derived. **Lean:** `Bridge.second_token_required`, via
`Bridge.exists_not_of_not_ball` (`lean4/Derivation/Bridge.lean` lines
126-175). **Axioms:** `propext, Quot.sound` (the helper: none).
**Depends on:** `SingleTok`, `AtMostTok`, `single_token_carrier_bound`
(Unit 11); `replayT` (Unit 07); the `Decidable (SingleTok t0 e)` instance
(`Bridge.lean` lines 114-125).

</details>

## First pass

A successful history starts empty and finishes with tokens A and B.
If every datum admission had carried A, Unit 11 would have limited
the final store to one entry. So an admission of a different token
must occur somewhere in that finite history.

Predict which event can provide it: `supply(B)` or `admit(B)`?
Supply alone changes no admitted data. The required event is a
datum admission with a token different from the chosen reference.
The grammar does not require an earlier supply event for admission;
the seed's prescribed presentation order is a separate matter.

The proof uses a decidable check on each entry of the finite history
to locate a failing single-token condition. This explicit bounded-list
argument is the extra step from “not every entry passes” to an
identified counterexample.

## Question

Unit 11 bounded what one token can do: at most one datum. Challenge 3 is
about two data. So where does the second one come from? The answer should
not merely say "not from one token"; it should put a finger on the event
that brought it in.

## What we already possess

- `SingleTok t0 e`: if `e` admits a datum, its token is `t0`; `AtMostTok`;
  and the carrier bound: a single-token history from a state satisfying
  `AtMostTok` leaves at most one token (Unit 11).
- Deciding `SingleTok t0 e` for a concrete event: the instance at lines
  114-125 matches on the constructor and, for `admitDatum tok`, on whether
  `tok = t0`. Deciding it for every event of a list follows from Lean's
  decidability of bounded quantification over lists.
- `hist01 = [.supply 0, .admitDatum 0, .supply 1, .admitDatum 1]` replays
  to the store `[0, 1]` (Unit 11, book Lean `two_tokens_escape`).

## New concept: a contrapositive that names its witness

Unit 11 says: all admissions carry `t0` ⟹ at most one datum. Turned
around: two data ⟹ not all admissions carry `t0`. This negative statement does not yet name the event. The next
step locates *which* event breaks the pattern in the finite history.
That is what `exists_not_of_not_ball` supplies. Given a list and a
decidable property that does not hold of every member, it walks the list
and returns a member for which the property fails. No choice principle is
used: the walk decides the property at each element and stops at the first
failure. The theorem then opens that event: a non-admission satisfies
`SingleTok` for free, so the failing event must be `admitDatum tok` with
`tok ≠ t0`.

## Plain-language interpretation

Suppose the notebook ends with two words in it. Look back through the
history. If every admission wrote the same word, the notebook would hold
one word (Unit 11). So some admission wrote a different word, and the
proof hands you that line of the history. Whatever `t0` you name, there is
an admission of something else. The second datum was brought in; it did
not grow from the first.

The paper's provenance table records this as: carrier of size 2, "not
derivable from one inscription", mechanism "a second distinct external
token, or a declared occurrence-admission discipline". The theorem covers
the first route completely and says nothing about the second, which lives
outside `stepT`.

## Pseudocode

```
# Gloss
given: history h from the empty state ends with >= 2 tokens; any t0
decide: does every event of h satisfy SingleTok t0?
  yes:  Unit 11 gives <= 1 token.  contradiction with >= 2.
  no:   walk h; the first event e failing SingleTok t0 is found.
        e is not a supply, form, instance, rule or demand (those never fail),
        so e = admitDatum tok, and tok ≠ t0.
return e.
```

## Python

```python
from derivation.bridge import scenario_report
from derivation.model import AdmitDatum, Supply, replay

h = [Supply("<>"), AdmitDatum("<>"), Supply("<a>"), AdmitDatum("<a>")]
print(replay(h).data)
print([e for e in h if isinstance(e, AdmitDatum) and e.token != "<>"])
rep = scenario_report("two_dedup", ["<>", "<a>"], 7, False)
print(rep["states_reached"], rep["max_carrier"], rep["min_events_to"]["carrier_2"])
```

Output:

```text
('<>', '<a>')
[AdmitDatum(token='<a>')]
130 2 2
```

## Line-by-line Python explanation

`h`: `hist01` with the tokens written out, supply then admit, twice.

`replay(h).data`: two data. The second admission carried a token not yet
present, so it appended (Unit 06).

The list comprehension is the theorem's conclusion computed: the
admissions of `h` whose token is not `"<>"`. There is one, the admission
of `"<a>"`. Running it with `"<a>"` in place of `"<>"` would return the
other admission; the theorem holds for every `t0`.

`scenario_report("two_dedup", ...)`: the breadth-first search of
`bridge.py` over the two-token alphabet. Within seven events it reaches
130 states, carrier 2, and the first two-datum state after exactly two
events (admit, admit). These are the artifact's values.

The check script replays every history of at most five events over the
two-token alphabet (66 430 histories, 5 138 admissible), finds 2 212 that
end with two data, and confirms for each of them and for each of three
choices of `t0` that some admission carries a token other than `t0`.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Bridge.lean lines 126-144
/-- A decidably refuted bounded universal yields an explicit witness. -/
theorem exists_not_of_not_ball {α : Type} (l : List α) (P : α → Prop)
    [DecidablePred P] (h : ¬ ∀ x ∈ l, P x) : ∃ x ∈ l, ¬ P x := by
  induction l with
  | nil => exact absurd (fun x hx => nomatch hx) h
  | cons a rest ih =>
      cases hd : decide (P a) with
      | true =>
          have ha : P a := of_decide_eq_true hd
          have hrest : ¬ ∀ x ∈ rest, P x := fun hr =>
            h (fun x hx => by
              cases hx with
              | head => exact ha
              | tail _ hx => exact hr x hx)
          have ⟨x, hx, hnp⟩ := ih hrest
          exact ⟨x, List.mem_cons_of_mem _ hx, hnp⟩
      | false =>
          exact ⟨a, List.mem_cons_self, of_decide_eq_false hd⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/Bridge.lean lines 146-175
/-- **Two-ness needs a second external token** (contrapositive form):
a state with two admitted data comes only from a history admitting some
token different from the first. -/
theorem second_token_required (t0 : Nat) (h : List TEvent)
    {res : TRegime}
    (hr : replayT h ⟨[], [], [], [], []⟩ = some res)
    (htwo : 2 ≤ res.tokens.length) :
    ∃ e ∈ h, ∃ tok, e = TEvent.admitDatum tok ∧ tok ≠ t0 := by
  cases hd : decide (∀ e ∈ h, SingleTok t0 e) with
  | true =>
      have hall : ∀ e ∈ h, SingleTok t0 e := of_decide_eq_true hd
      have hle := single_token_carrier_bound t0 h hall (Or.inl rfl) hr
      exact absurd htwo (by omega)
  | false =>
      have hall : ¬ ∀ e ∈ h, SingleTok t0 e := of_decide_eq_false hd
      have ⟨e, he, hnot⟩ := exists_not_of_not_ball h (SingleTok t0) hall
      refine ⟨e, he, ?_⟩
      cases e with
      | admitDatum tok =>
          refine ⟨tok, rfl, fun htok => ?_⟩
          exact hnot (fun tok' hh => by cases hh; exact htok)
      | supply tok => exact absurd (fun _ hh => nomatch hh) hnot
      | admitForm a => exact absurd (fun _ hh => nomatch hh) hnot
      | admitInst f args => exact absurd (fun _ hh => nomatch hh) hnot
      | admitRuleAll f => exact absurd (fun _ hh => nomatch hh) hnot
      | impose i j => exact absurd (fun _ hh => nomatch hh) hnot
```

## Line-by-line Lean explanation

**The helper.** `l` is a list, `P` a property that can be decided
(`[DecidablePred P]`), `h` says `P` does not hold of every member. The
proof is by induction on `l`.

`| nil`: an empty list satisfies any bounded universal vacuously
(`fun x hx => nomatch hx`: there is no `x ∈ []`), which contradicts `h`.

`| cons a rest ih`: `cases hd : decide (P a)` asks the decision procedure
about the head. If it answers `true`, `of_decide_eq_true hd` gives `ha : P
a`; then `P` must fail somewhere in `rest` (`hrest`), because if it held of
every member of `rest`, together with `ha` it would hold of every member of
`a :: rest` (the inner `cases hx` splits membership into head and tail),
contradicting `h`. The induction hypothesis on `rest` returns a witness,
and `List.mem_cons_of_mem` lifts its membership to `a :: rest`. If the
decision answers `false`, `a` itself is the witness, with
`List.mem_cons_self` and `of_decide_eq_false hd`.

The helper reports no axioms: every step is a computation or a membership
proof.

**The theorem.** The base is fixed as the empty token-aware state, so the
invariant `AtMostTok t0` holds at the start (`Or.inl rfl`). `cases hd :
decide (∀ e ∈ h, SingleTok t0 e)` decides whether the history is
single-token for `t0`.

- `true`: `hall` is the single-token hypothesis, and Unit 11's bound gives
  `hle : res.tokens.length ≤ 1`. With `htwo : 2 ≤ res.tokens.length` this
  is a contradiction in arithmetic; `omega` finds it, and `absurd` closes
  the case. (The book's re-proof replaces `omega` by `Nat.le_trans htwo
  hle` followed by `decide` on `¬ 2 ≤ 1`, to show that no arithmetic
  automation is needed.)
- `false`: `hall` now says the history is *not* single-token, and the
  helper, with `P := SingleTok t0`, returns an event `e ∈ h` with `hnot :
  ¬ SingleTok t0 e`. `refine ⟨e, he, ?_⟩` offers that event; what remains
  is to exhibit its token. `cases e` opens the six constructors. For
  `admitDatum tok`, the token is `tok`, `e = admitDatum tok` is `rfl`, and
  `tok ≠ t0` is proved by assuming `htok : tok = t0` and deriving
  `SingleTok t0 (admitDatum tok)` from it, which `hnot` refutes. For each
  of the five other constructors, `SingleTok` holds for free
  (`fun _ hh => nomatch hh`: the equation `supply tok = admitDatum tok'`
  has no proof), which contradicts `hnot`; so those cases cannot occur.

**Axioms.** `second_token_required` reports `propext, Quot.sound`,
inherited from Unit 11's bound and from the decision over the concrete
history. The helper reports none.

## What has been proved

- From the empty state, any history ending with two or more tokens
  contains an admission of a token other than `t0`, for every `t0`
  (Genesis, derived).
- The witness is produced by a decision walk, not by a choice principle
  (Genesis, derived; the helper is axiom-free).
- On `hist01` the theorem yields a witness for `t0 = 0` and for `t0 = 1`;
  the explicit witnesses are the admissions of 1 and of 0 (book Lean,
  derived).
- On Unit 11's `busy` history the second hypothesis fails, and the bound
  shows why (book Lean `busy_not_two`, derived).
- Within seven events the two-token search reaches carrier 2 at two
  events (Genesis, verified finite, `artifacts/bridge.json`).

## What has not been proved

- That the *same* second token must be the one that counts. The theorem
  says "some token different from `t0`"; with three tokens in a history
  there are several witnesses, and the walk returns the first.
- Anything from a base other than the empty state. The statement fixes
  `⟨[], [], [], [], []⟩`; Unit 11's bound is the general form.
- That two data require two tokens under *every* admission discipline.
  The occurrence discipline (`bridge.py` lines 54-63; paper §B4) reaches
  two data from one token by appending on every admission; Genesis prices
  that as an import of metatheoretic position and does not model it in
  `stepT`.
- That a second datum answers Challenge 3. Two data after Challenge 2 are
  still collapsed (Units 10, 12). The second token buys two-ness, not
  separation.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `∃ e ∈ h, ∃ tok, …` | the conclusion | metatheory existential, with its witness computed by the helper |
| `decide (∀ e ∈ h, …)` | the case split | metatheory decision over a concrete finite list |
| `{α : Type} (P : α → Prop) [DecidablePred P]` | the helper's generality | metatheory polymorphism; used here only at `TEvent` and `SingleTok t0` |
| `omega` | one arithmetic contradiction | metatheory automation; replaceable by `Nat.le_trans` and `decide` |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The token store with two entries, and nothing
that says which came first or which is "the second": the store is a list
in the metatheory, and `TRegime.erase` forgets it (Unit 07; Units 26 and
later return to admission order under `order_erased_at_object_level`).
The token `t0` and the witness event are metatheoretic objects. The
system did not "notice" a second token; the metatheory proved that one
was supplied.

**Phrases to read with care.**

- "Externally purchased" (paper) means: no history over one token reaches
  it. It does not say who the external party is or why they supplied a
  second token; that is the caller's intervention (Unit 00).
- "The first token" in the Lean docstring is `t0`, any token at all; the
  theorem does not single out an earliest admission.

## Student exercise

Apply the theorem to the history `[.admitDatum 3, .admitDatum 3,
.admitDatum 5, .admitDatum 3, .admitDatum 7]` from the empty state, with
`t0 = 3`. What is the final store, is the hypothesis `2 ≤ length` met,
which event does the proof's walk return, and would it return a different
event for `t0 = 5`?

## Answer

The store is `[3, 5, 7]`: the first admission appends 3, the second
designates, the third appends 5, the fourth designates, the fifth appends
7. Length 3, so `2 ≤ 3` holds. The walk decides `SingleTok 3` event by
event; the first failure is the third event, `admitDatum 5`, and the proof
returns it with `tok = 5 ≠ 3`. For `t0 = 5` the first failure is the very
first event, `admitDatum 3`, so the witness is that one with `3 ≠ 5`. (The
admission of 7 is also a witness in both cases, but the walk stops at the
first.)

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Bridge.lean` lines 126-144 (`exists_not_of_not_ball`), 146-175 (`second_token_required`); the `Decidable (SingleTok t0 e)` instance lines 114-125 |
| Axiom report | `artifacts/lean_axioms.txt`: `Bridge.second_token_required` `[propext, Quot.sound]`; `exists_not_of_not_ball` is not in the root inventory, the book check reports it axiom-free |
| Paper | `paper/bridge_provenance.md` §B2 (**[theorem]**, contrapositive form) and the provenance table row "carrier (size 2)"; `paper/native_derivation_map.md` line 16 |
| Ledger | No `CL-*` entry names this theorem; its record is the provenance table (as for Unit 11) |
| Artifact | `artifacts/bridge.json`, scenario `two_dedup`: 130 states, max carrier 2, carrier 2 at 2 events |
| Test | `tests/test_bridge.py::test_second_token_unlocks_the_target` |
| Check (Python) | `python textbook/checks/u13_second_token.py`: 66 430 histories of at most five events over two tokens, 5 138 admissible, 2 212 ending with two data, each with an admission of a token other than each of three choices of `t0`; shortest two events; artifact values reproduced |
| Check (book Lean) | `python textbook/checks/u13_lean.py`: seven book theorems plus the two Genesis theorems kernel-checked, Lean 4.33.0; the re-proof without `omega` reports the same `propext, Quot.sound`; the helper and its example report none |
