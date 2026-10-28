# Unit 11. One token gives at most one datum

**Claim.** Any history whose datum admissions all carry one and the same
token leaves at most one admitted datum, however often that token is
re-supplied or re-admitted, and whatever forms, instances, rules or demands
are admitted along the way. **Status:** derived. **Lean:**
`Bridge.single_token_carrier_bound`, via `Bridge.stepT_preserves_atMostTok`
(`lean4/Derivation/Bridge.lean` lines 31-112). **Axioms:** `propext,
Quot.sound`. **Depends on:** `TRegime`, `TEvent`, `stepT`, `replayT`,
`replayT_cons` (Units 06, 07); designation by re-admission (Unit 06).

## Question

Challenge 3 will ask the system to tell two data apart. Before anything
can be told apart there must be two of it. The seed hands the system one
inscription, ⟨⟩. Can repeating it, presenting it again and admitting it
again as often as we like, ever make two data out of it?

## What we already possess

- The token-aware state `TRegime` with its `tokens` list, and the
  token-aware events `TEvent` (Unit 06).
- `stepT`: admitting a token already present returns the state unchanged;
  admitting a fresh token appends it (Unit 06, `Erasure.lean` lines 40-60).
- `replayT h base`: fold `stepT` over the history, `none` as soon as one
  step is refused (Unit 07, lines 107-108), and the unfolding lemma
  `replayT_cons` (lines 121-125).
- The other four events (`admitForm`, `admitInst`, `admitRuleAll`,
  `impose`) never touch the `tokens` field: each either copies it or is
  refused (Unit 06).

## New concept: an invariant carried along a history

The theorem is proved by naming a property that is true at the start and
stays true after every step. Such a property is an **invariant**. Here it
is `AtMostTok t0`: the token store is either empty or exactly `[t0]`. The
start satisfies it (the store is empty). One step preserves it: a supply
copies the store; admitting `t0` into an empty store gives `[t0]`;
admitting `t0` into `[t0]` is a designation and changes nothing; the other
four events copy the store. So after any number of steps the store is
still `[]` or `[t0]`, and a list of that shape has length at most one.

Two definitions name the hypothesis and the invariant:

```lean
-- Lean (Genesis), lean4/Derivation/Bridge.lean lines 31-38
/-- Histories whose every datum admission carries the same token. -/
def SingleTok (t0 : Nat) (e : TEvent) : Prop :=
  ∀ tok, e = TEvent.admitDatum tok → tok = t0

/-- Invariant: under single-token admission, the token store is empty or
exactly the singleton. -/
def AtMostTok (t0 : Nat) (t : TRegime) : Prop :=
  t.tokens = [] ∨ t.tokens = [t0]
```

`SingleTok t0 e` says: if `e` is a datum admission, its token is `t0`. An
event that is not a datum admission satisfies it for free, because the
"if" is never met. The theorem assumes `SingleTok t0 e` for every event
`e` in the history.

## Plain-language interpretation

One inscription, presented and admitted again and again, is still one
inscription. Genesis's admission rule treats the second admission of a
present token as pointing at the existing datum (Unit 06), so no repetition
adds to the ledger. Nothing else in the grammar adds a datum. So a carrier
of size two cannot come from ⟨⟩ alone. In the paper's phrase: "two-ness is
externally purchased". Either a second, different token is supplied from
outside (Unit 13 proves this is required), or a different admission
discipline is declared, one in which repeated admissions are told apart by
their position in the history. That second route is a declared import of
metatheoretic position, flagged as such in `paper/bridge_provenance.md`
§B4; it is not a derivation from the mark.

## Pseudocode

```
# Gloss
invariant(store) := store == [] or store == [t0]

start:  store == []                              -- invariant holds
for each event e in h (all single-token for t0):
    if e is supply:               store unchanged -- holds
    if e is admitDatum t0:
        if t0 in store:           store unchanged -- holds (designation)
        else:                     store := [t0]   -- holds
    otherwise:                    store unchanged -- holds (or refused)
at the end: store is [] or [t0], so length(store) <= 1
```

## Python

```python
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Supply, replay
from derivation.bridge import occurrence_step, scenario_report

busy = [Supply("<>"), AdmitDatum("<>"), Supply("<>"), AdmitDatum("<>"),
        AdmitForm(2), AdmitInst(0, (0, 0)), AdmitDatum("<>")]
print(replay(busy).data)
print(replay([AdmitDatum("<>"), AdmitDatum("<a>")]).data)
print(occurrence_step(replay([AdmitDatum("<>")]), AdmitDatum("<>")).data)
rep = scenario_report("single_dedup", ["<>"], 7, False)
print(rep["states_reached"], rep["max_carrier"], rep["min_events_to"]["carrier_2"])
```

Output:

```text
('<>',)
('<>', '<a>')
('<>', '<>')
20 1 None
```

## Line-by-line Python explanation

`busy`: seven events, every datum admission carrying `"<>"`. It supplies
and admits the token twice, admits a binary form, admits the self-instance
`(0, 0)`, and admits the token a third time.

`replay(busy).data`: the ledger holds one datum. The second and third
admissions were designations (Unit 06, `model.py` lines 111-114); the form
and the instance did not touch the data.

`replay([AdmitDatum("<>"), AdmitDatum("<a>")]).data`: two different tokens
give two data. This is the hypothesis failing, not the theorem failing.

`occurrence_step(...)`: `bridge.py` lines 54-63 define a *different*
admission rule under which every datum admission appends, so the same token
twice gives two entries. Genesis declares this as an alternative discipline
and prices it (paper §B4); it is not the rule the sealed derivation uses.

`scenario_report("single_dedup", ["<>"], 7, False)`: a breadth-first search
(`bridge.py` lines 108-142) over every admissible history of at most seven
events from the single-token alphabet (supply, admit, one binary form,
every binary instance over at most two indices). It reaches 20 states, the
largest carrier is 1, and no number of events reaches carrier 2 (`None`).
These are the three values recorded in `artifacts/bridge.json`.

The check script also replays every history of at most six events over the
four-event alphabet one by one (5 461 histories, 1 945 admissible) and finds
the maximum data count 1.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Bridge.lean lines 40-85 (abridged: the
-- four cases that copy the store are alike; one is shown)
theorem stepT_preserves_atMostTok {t0 : Nat} {t : TRegime}
    (ht : AtMostTok t0 t) {e : TEvent} (he : SingleTok t0 e)
    {t' : TRegime} (hs : stepT t e = some t') : AtMostTok t0 t' := by
  cases e with
  | supply tok =>
      cases Option.some.inj hs
      exact ht
  | admitDatum tok =>
      have htok : tok = t0 := he tok rfl
      rw [htok] at hs
      by_cases hmem : t0 ∈ t.tokens
      · simp only [stepT] at hs
        rw [if_pos hmem] at hs
        cases Option.some.inj hs
        exact ht
      · simp only [stepT] at hs
        rw [if_neg hmem] at hs
        cases Option.some.inj hs
        cases ht with
        | inl h =>
            right
            show t.tokens ++ [t0] = [t0]
            rw [h]
            rfl
        | inr h =>
            exact absurd (by rw [h]; simp) hmem
  | admitForm a =>
      simp only [stepT] at hs
      split at hs
      · cases Option.some.inj hs; exact ht
      · cases hs
  -- admitInst, admitRuleAll, impose: the same three lines each
```

```lean
-- Lean (Genesis), lean4/Derivation/Bridge.lean lines 87-112
/-- **Carrier bound.**  One opaque inscription never yields a carrier of
size two: any history whose datum admissions all carry the same token
leaves at most one admitted datum, no matter how often the inscription is
re-supplied or re-admitted. -/
theorem single_token_carrier_bound (t0 : Nat) (h : List TEvent)
    (hall : ∀ e ∈ h, SingleTok t0 e) {t : TRegime}
    (ht : AtMostTok t0 t) {res : TRegime}
    (hr : replayT h t = some res) : res.tokens.length ≤ 1 := by
  induction h generalizing t with
  | nil =>
      have : t = res := Option.some.inj hr
      subst this
      cases ht with
      | inl h0 => rw [h0]; exact Nat.zero_le 1
      | inr h1 => rw [h1]; exact Nat.le_refl 1
  | cons e rest ih =>
      rw [replayT_cons] at hr
      cases hs : stepT t e with
      | none => rw [hs] at hr; cases hr
      | some t1 =>
          rw [hs] at hr
          exact ih
            (fun e' he' => hall e' (List.mem_cons_of_mem _ he'))
            (stepT_preserves_atMostTok ht
              (hall e (List.mem_cons_self)) hs)
            hr
```

## Line-by-line Lean explanation

**The step lemma.** Its hypotheses: `ht`, the store is `[]` or `[t0]`;
`he`, the event is single-token; `hs`, the step succeeded and produced
`t'`. Its conclusion: `t'`'s store is `[]` or `[t0]`.

`cases e with`: six cases, one per constructor of `TEvent`.

`| supply tok`: `stepT t (.supply tok)` is `some t` by definition, so `hs`
reads `some t = some t'`. `Option.some.inj hs` turns that into `t = t'`,
and `cases` on it replaces `t'` by `t` everywhere. The goal is now `ht`.

`| admitDatum tok`: first `he tok rfl` applies the single-token hypothesis
to this very event, giving `htok : tok = t0`; `rw [htok] at hs` rewrites
the step so that it admits `t0`. Then the proof splits on `hmem : t0 ∈
t.tokens`, exactly the test `stepT` makes.

- Present: `simp only [stepT] at hs` unfolds the definition, `rw [if_pos
  hmem] at hs` picks the "already present" branch, which returns `some t`.
  As in the supply case, `t' = t` and the goal is `ht`. This is Unit 06's
  designation.
- Absent: the other branch returns the state with `tokens ++ [t0]`.
  After `cases Option.some.inj hs`, `t'` is that state. Now `cases ht`:
  if the old store was `[]` (`inl h`), the new store is `[] ++ [t0]`,
  which is `[t0]`; the proof chooses the right disjunct (`right`), states
  the goal in that form (`show`), rewrites with `h` and closes by `rfl`.
  If the old store was `[t0]` (`inr h`), then `t0 ∈ t.tokens` after all
  (`by rw [h]; simp`), which contradicts `hmem`; `absurd` closes the case.
  So "absent and already `[t0]`" cannot happen.

`| admitForm a` and the three cases after it: `stepT` tests a side
condition and returns either `some` of a state with the same `tokens` or
`none`. `split at hs` opens the two branches; in the `some` branch
`Option.some.inj hs` identifies `t'` and the store is unchanged, so `ht`
closes it; in the `none` branch `hs : none = some t'` is impossible and
`cases hs` closes it.

**The bound.** Induction on the history `h`, with `t` generalized so that
the induction hypothesis speaks about any starting state satisfying the
invariant.

`| nil`: an empty history replays to its base, so `hr : some t = some res`
gives `t = res`; `subst` replaces `res` by `t`. Then `cases ht`: an empty
store has length `0 ≤ 1` (`Nat.zero_le 1`); the store `[t0]` has length
`1 ≤ 1` (`Nat.le_refl 1`).

`| cons e rest ih`: `rw [replayT_cons] at hr` unfolds one step, so `hr`
says `(stepT t e).bind (replayT rest) = some res`. `cases hs : stepT t e`:
if the step was refused (`none`), the bind is `none` and `hr` is
impossible. If it produced `t1`, `hr` becomes `replayT rest t1 = some res`,
and the induction hypothesis `ih` applies to `t1`. It needs three things:
that every event of `rest` is single-token (every member of `rest` is a
member of `e :: rest`, `List.mem_cons_of_mem`); that `t1` satisfies the
invariant, which is the step lemma applied to `ht`, to `hall e` for the
head event (`List.mem_cons_self`), and to `hs`; and the replay fact `hr`.

**Axioms.** Both theorems report `[propext, Quot.sound]`: the proof
decides membership in a concrete list and unfolds `stepT` with `simp`,
which goes through `Quot.sound`. The definitions `SingleTok` and
`AtMostTok` use no axioms. The book's own `busy_all_singleTok` and
`hist01_not_singleTok`, proved by `decide` through the `Decidable
(SingleTok t0 e)` instance at line 114, report no axioms at all, because
that instance is built by pattern matching, not by list membership.

## What has been proved

- Under single-token admission, the token store is always `[]` or `[t0]`
  (Genesis, derived).
- Hence any single-token history, from any state satisfying the
  invariant, leaves at most one datum (Genesis, derived).
- The bound is reached: one admission gives exactly one (book Lean
  `bound_is_sharp`, derived).
- The hypothesis is needed: `hist01`, which admits tokens 0 and 1, reaches
  a store of length two (book Lean `two_tokens_escape`, derived).
- Within seven events, the single-token search reaches 20 states and
  carrier 1 only; two tokens, or the occurrence discipline, reach carrier
  2 in two events (Genesis, verified finite, `artifacts/bridge.json`).

## What has not been proved

- That a second token is *required* for two data. That is the
  contrapositive, witness-producing theorem `second_token_required`
  (Unit 13); this unit proves only the bound.
- Anything about the erased state. The theorem is about `TRegime.tokens`;
  the erased `Regime.data` count equals its length (Unit 07,
  `TRegime.erase`), but that equality is a separate fact.
- That no admission discipline yields two data from one token. The
  occurrence discipline does, by design; Genesis prices it as an import
  of metatheoretic position rather than forbidding it.
- That the three bridge scenarios are exhaustive beyond seven events. The
  search is a finite computation at a declared horizon; the Lean theorem
  is what covers every length.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `(t0 : Nat)`, `(h : List TEvent)` | the universal statement over tokens and histories | metatheory quantifiers; the system holds one history at a time |
| `induction h generalizing t` | the proof | metatheory induction on Lean's lists |
| `Decidable (SingleTok t0 e)` | the book's `decide` proofs | metatheory decision procedure |
| `propext`, `Quot.sound` | inherited through `simp` and list membership | inside the declared boundary |

**What the system holds.** The token store, a finite list, and the events
it has been given. It does not hold the token `t0` as a name: the token is
metatheoretic (Unit 06), and the theorem is a metatheoretic statement about
every history that reuses one of them.

**Price of the two escapes.** A second token is an external supply
(Unit 13). The occurrence discipline imports *position in the history* as
what distinguishes two admissions of the same inscription; the paper
flags this at `paper/bridge_provenance.md` §B4 and the book counts it as
an admission with that price, never as something ⟨⟩ provides.

**Phrases to read with care.**

- "One inscription never yields two data" is right for Genesis's declared
  admission rule. It is not a theorem about every conceivable rule.
- "Carrier" in the paper means the admitted data count; it is not a set
  the system holds.

## Student exercise

Take the history `[.admitDatum 5, .supply 7, .admitDatum 5, .admitForm 1,
.admitDatum 5]` from the empty state. Is every event `SingleTok 5`? What is
the final token store, and what does the theorem guarantee about it? Then
change the last event to `.admitDatum 7`: which hypothesis fails, and what
is the store now?

## Answer

Every event is `SingleTok 5`: the supply and the form admission satisfy it
for free, and all three datum admissions carry 5. The store after the
history is `[5]`: the first admission appends 5, the second and third are
designations, the supply and the form admission copy the store. The
theorem guarantees `[5].length ≤ 1`, which holds. With `.admitDatum 7` at
the end, `SingleTok 5 (.admitDatum 7)` is false (it would require `7 = 5`),
so `hall` fails and the theorem says nothing; the store becomes `[5, 7]`,
length two. (The check script's `two_tokens_escape` is the same point with
tokens 0 and 1.)

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Bridge.lean` lines 31-112 (`SingleTok`, `AtMostTok`, `stepT_preserves_atMostTok`, `single_token_carrier_bound`); `Decidable` instance lines 114-125 |
| Axiom report | `artifacts/lean_axioms.txt`: `Bridge.stepT_preserves_atMostTok`, `Bridge.single_token_carrier_bound` each `[propext, Quot.sound]` |
| Paper | `paper/bridge_provenance.md` §B1 (scenario table) and §B2 (**[theorem]**) |
| Ledger | No `CL-*` entry names this theorem. Its record is the provenance table in `paper/bridge_provenance.md` (row "carrier (size 2)"), `paper/native_derivation_map.md` line 16 (seed yields two-ness: FALSE), and `code/derivation/bridge.py` `provenance_table` |
| Artifact | `artifacts/bridge.json`, scenario `single_dedup`: 20 states, max carrier 1, carrier 2 never |
| Test | `tests/test_bridge.py::test_single_token_never_reaches_two_or_witnessed_pair` |
| Check (Python) | `python textbook/checks/u11_single_token.py`: 5 461 single-token histories of at most six events, max data 1; 20 reachable states within seven events, max data 1; second token and occurrence discipline each give 2; artifact values reproduced |
| Check (book Lean) | `python textbook/checks/u11_lean.py`: thirteen book theorems plus the two Genesis theorems kernel-checked, Lean 4.33.0; `decide` over concrete replays reports `propext, Quot.sound`, `decide` through the `SingleTok` instance reports no axioms |
