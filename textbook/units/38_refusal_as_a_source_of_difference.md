# Unit 38. Five declared ways to record a repeated token

**Claim.** A repeat can leave only a history marker, update a counter, or
create a new occurrence record, depending on the declared rule. A tag can
distinguish occurrence positions in the two-record example. These are
different record-keeping choices, not consequences forced by repetition.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** When a token already admitted is offered again, a system may
*refuse* it, and there are several ways to record the refusal. Genesis
declares five disciplines on a reduced state (admitted tokens, tagged
positions, a refusal counter) and proves, rung by rung, what each one can
tell apart. Silent refusal and a history-only marker leave the same state
(`silent_eq_meta`, `markers_invisible`). Counting refusals changes the
state but never grows the carrier past one token
(`nonreify_carrier_bound`). Admitting the repeat as a second, untagged
datum is exactly occurrence admission (`reifyUntagged_eq_occurrence`),
and its two-datum state is swap-invariant. Admitting it with a position
tag gives a two-datum state the swap moves
(`tagged_state_not_swap_invariant`), with a designated occurrence; and
one hand-written correspondence represents the tag by a unary form and
one instance (`tagged_translation_separable`, `untagged_translation_collapsed`).
Those translation theorems do not prove a minimum over translation choices.

**Status:** derived, per discipline and per concrete history; the
four-way hierarchy as one theorem is OPEN (paper R9). **Lean:**
`Refusal.stepR` (`lean4/Derivation/Refusal.lean` lines 65-78),
`silent_eq_meta` (98-101), `markers_invisible` (131-133),
`nonreify_carrier_bound` (142-170), `reifyUntagged_eq_occurrence` (186-194),
`reifyTagged_two_admissions` (220-222), `tag_separates` (227-230),
`tagged_state_not_swap_invariant` (252-255), `canonical_designation`
(262-265), `tagged_translation_separable` (278-280),
`untagged_translation_collapsed` (285-287). **Axioms:** all `propext,
Quot.sound` except `untagged_translation_collapsed` (`propext`).
**Depends on:** the dedup discipline and the single-token carrier bound
(Units 06, 11); the second-token theorem (Unit 13) and Bridge's equivariance
obstruction (`Bridge.equivariant_not_D2`, `lean4/Derivation/Bridge.lean`
lines 244-281, audited in `textbook/audit/modules/Bridge.md`; no unit of
its own yet); `separable`, `collapsed`, `collapsed_of_no_insts` (Units
08-10).

</details>

## First pass

Present token X twice. Five declared modes give these results:

| Mode | Data list | Tagged positions | Repeat count |
|---|---|---|---|
| Silent | X | None | 0 |
| History marker only | X | None | 0 |
| Count the repeat | X | None | 1 |
| Append an occurrence | X, X | None | 0 |
| Append and tag it | X, X | Position 1 | 0 |

Positions start at 0. The two X entries are two occurrence records of
the same token. They do not establish two people or two physical objects.

The history-marker mode can retain an event in the history while
returning the same state. The counting mode changes a state field but
keeps one admitted position. The final mode gives the question “is this
position tagged?” different answers at 0 and 1.

**Predict:** does observing that the counter changed show that two
individual positions can now be distinguished?

<details>
<summary>Check your prediction</summary>

No. The counter records a repeat without creating or tagging a second
position. State change and separation of two admitted positions are
different claims.

</details>

The unary-mark comparison below is hand-written; a general translation
from these states to the earlier regime language is not supplied.

## Question

Unit 11 proved that one token, admitted and re-admitted under the dedup
discipline, never yields a second datum. Unit 13 proved that a second
datum needs a second token. Both assume the discipline that *drops* a
repeat. What if the system did something else with it? Refusing is also
an act. Does recording the refusal create a difference another object
could see? The answer depends on how the refusal is recorded, and the
module lays the options out as a ladder.

## What we already possess

- Unit 06's `stepT`: re-admitting a token designates, it does not add.
- Unit 11's `Bridge.single_token_carrier_bound`: under dedup, the carrier
  from one token has at most one datum.
- Bridge's equivariance obstruction (`equivariant_witness_is_S2`,
  `equivariant_not_D2`): from a symmetric two-element state, no
  equivariant rule chooses an orientation.
- Unit 13's `second_token_required`.
- `separable`, `collapsed`, `separable_not_collapsed`,
  `collapsed_of_no_insts` (Basic, Inertia).

## New concept: five disciplines on one reduced state

The reduced state is `RState := ⟨data, tags, refusals⟩`: the admitted
tokens in order, a list of tagged positions, a counter. Events are
`supply`, `admitTok`, `marker`. The stepper `stepR m` takes a `Mode`:

| mode | on a fresh token | on a repeat |
|---|---|---|
| `silent` | append | nothing |
| `metaMarker` | append | nothing (the marker event is for the history) |
| `fact` | append | `refusals + 1` |
| `reifyUntagged` | append | append again |
| `reifyTagged` | append | append again, and tag the new position |

`supply` and `marker` events never change the state. Then, with the
history `[admitTok 0, admitTok 0]` as the probe:

1. **Silent = marker.** The two modes have the same stepper, so the same
   replay. And markers are invisible to every mode: filtering them out of
   a history does not change the replay. So the "meta" discipline's
   record lives only in the history, outside the state.
2. **Fact: a difference without a carrier.** The counter becomes `1`. The
   state differs from the silent one. But `AtMostTokR t0`, "the data are
   `[]` or `[t0]`", is preserved by one step of any non-reifying mode on a
   single-token event. So no second datum ever appears.
3. **Untagged reification = occurrence.** Appending the repeat is the
   same as treating every admission as a new occurrence (`stepOcc`);
   the two steppers are equal as functions. The resulting `⟨[0, 0], [], 0⟩`
   is fixed by the swap of its two positions.
4. **Tagged reification.** `⟨[0, 0], [1], 0⟩`: position `1` is tagged,
   position `0` is not. The swap moves the tag, so the state is not
   swap-invariant; the head of the tag list designates occurrence `1`.
   The equivariance obstruction is not violated: the repeat operation
   supplies the tag as part of creating the second occurrence. It does
   not select an orientation from an already symmetric two-occurrence state.

**The price.** The tag is a unary observable built into the discipline.
Translating the tagged state into the regime language by hand gives
`⟨2, [1], [(0, [1])], [], []⟩`, the unary mark on datum 1, which is
separable at `(0, 1)`; the untagged state translates to `⟨2, [], [], [], []⟩`,
collapsed. So the tagged discipline reaches in two admissions what the
explicit route (second token, form, instance) reaches in four, by
*declaring* the form and instance in advance. The admission count falls;
the declared capability still needs to be counted. These are counts under
the two specified routes, not a proof that every representation of the
tag has the same cost.

## Plain-language interpretation

The same token is presented twice. A program can ignore the repeat,
leave a marker only in its event history, increment a counter, append a
second occurrence record, or append that record with a tag on its position.
Only the last two enlarge this model's data list. An extra occurrence
record is not evidence of an extra person or physical object.

For the two-occurrence example, a tag gives different membership answers
at positions 0 and 1. A counter alone records that a repeat happened
without marking an individual position. The tag can be represented by
the unary-mark shape studied in Unit 22, but that correspondence here is
hand-written, not a general proved translation or cost lower bound.

The diary (the marker) is worth a second look: it is a record, but it is
a record *outside* the state. Nothing in the room can read it. Genesis
proves this by showing the room is the same with or without the diary
entries. This concerns the returned state: an external reader of the
history can still detect the marker.

## Pseudocode

```
# Gloss
RState  := (data : list of tokens, tags : list of positions, refusals : count)
stepR m s (supply _)  := s
stepR m s (marker _)  := s
stepR m s (admitTok t):
  if t not in s.data: append t to s.data
  else match m:
    silent, metaMarker -> s
    fact               -> s with refusals + 1
    reifyUntagged      -> append t to s.data
    reifyTagged        -> append t to s.data; append (old length) to s.tags
replayR m h := fold stepR m from emptyR over h

AtMostTokR t0 s := s.data = [] or s.data = [t0]
-- preserved by one step of silent / metaMarker / fact on an admitTok t0 event

swapState s := s with every tag index 0 <-> 1
taggedTranslation := regime with 2 data, one unary form, instance (0,[1])
```

## Python

```python
from derivation.refusal import DISCIPLINES, EMPTY, Adm, separable, step, swap_two

for name, readmit in DISCIPLINES.items():
    s = EMPTY
    for e in [Adm("<>"), Adm("<>")]:
        s = step(s, e, readmit)
    extra = (f"swap-invariant {swap_two(s) == s}, separable {separable(s, 0, 1)}"
             if len(s.data) == 2 else "one datum")
    print(f"{name:15s} data {list(s.data)} tags {sorted(s.tags)} refusals {s.refusals}; {extra}")
```

Output:

```text
silent          data ['<>'] tags [] refusals 0; one datum
meta            data ['<>'] tags [] refusals 0; one datum
fact            data ['<>'] tags [] refusals 1; one datum
reify_untagged  data ['<>', '<>'] tags [] refusals 0; swap-invariant True, separable False
reify_tagged    data ['<>', '<>'] tags [1] refusals 0; swap-invariant False, separable True
```

The check script also confirms occurrence admission equals the untagged
discipline, reruns the orientation and equivalence searches, and rebuilds
the paper's table from `discipline_report`, all against `artifacts/refusal.json`:

```text
occurrence admission gives the reify_untagged state: True
equivalence over 7 events: {'scope': 'single token, 7 events', 'reify_untagged_states': 10, 'occurrence_states': 10, 'state_sets_equal': True}
min events to carrier 2 / state difference / witnessed / oriented / witness without instances:
  silent          None / None / None / None / None  (5 states): no_new_object_level_difference
  meta            None / None / None / None / None  (5 states): one_object_plus_one_event
  fact            None / 2 / None / None / None  (20 states): two_states_only
  reify_untagged  2 / None / 4 / 4 / None  (10 states): two_carrier_objects_collapsed
  reify_tagged    2 / None / 2 / 2 / 2  (10 states): two_carrier_objects_witnessed_oriented
  occurrence      2 / None / 4 / 4 / None  (10 states): two_carrier_objects_collapsed
  second_token    2 / None / 4 / 4 / None  (18 states): two_carrier_objects_collapsed
failures: []
```

## Line-by-line Python explanation

The Python `RSt` carries two fields Lean's `RState` does not: `has_form`
and `insts`. They let the search ask the "explicit route" question
(admit a form, then an instance) alongside each discipline; Lean asks it
by writing the translation regime by hand. `step(s, e, readmit)` is
`stepR`: a fresh token appends; a repeat is handed to the discipline's
`readmit` function; `occurrence=True` bypasses the check, which is
`stepOcc`.

`separable(s, 0, 1)` compares the *observable profile* of the two
positions: `(i in s.insts, i in s.tags)`. Under `reify_untagged` both
profiles are `(False, False)`; under `reify_tagged` position 1 has the
tag. `swap_two` exchanges the two positions, carrying tags and instances
with them. The untagged state is fixed; the tagged one is not.

The table's columns are minimum event counts to reach: two data; a state
differing from the silent one; a witnessed pair; an oriented witnessed
pair; a witnessed pair with no instance events. `None` means unreachable
within the declared horizon (7 events, one token, carrier capped at 2).
The `fact` row reaches a state difference at 2 events and nothing else;
the three collapsed rows need 4 events (second datum, form, instance) to
witness; the tagged row witnesses at 2 with no instances. These are
finite searches within declared bounds, and the paper labels them so.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Refusal.lean lines 51-78
structure RState where
  data : List Nat
  tags : List Nat
  refusals : Nat
deriving Repr, DecidableEq

def emptyR : RState := ⟨[], [], 0⟩

inductive Mode where
  | silent | metaMarker | fact | reifyUntagged | reifyTagged
deriving Repr, DecidableEq

def stepR (m : Mode) (s : RState) : REvent → RState
  | .supply _ => s
  | .marker _ => s
  | .admitTok tok =>
      if tok ∈ s.data then
        match m with
        | .silent => s
        | .metaMarker => s
        | .fact => { s with refusals := s.refusals + 1 }
        | .reifyUntagged => { s with data := s.data ++ [tok] }
        | .reifyTagged =>
            { s with data := s.data ++ [tok],
                     tags := s.tags ++ [s.data.length] }
      else { s with data := s.data ++ [tok] }
```

```lean
-- Lean (Genesis), lean4/Derivation/Refusal.lean lines 131-170, 252-255, 273-287
theorem markers_invisible (m : Mode) (h : List REvent) :
    replayR m (h.filter fun e => !isMarker e) = replayR m h :=
  markers_invisible_from m h emptyR

def AtMostTokR (t0 : Nat) (s : RState) : Prop :=
  s.data = [] ∨ s.data = [t0]

theorem nonreify_carrier_bound {m : Mode}
    (hm : m = .silent ∨ m = .metaMarker ∨ m = .fact) {t0 : Nat} {s : RState}
    (hs : AtMostTokR t0 s) {e : REvent}
    (he : ∀ tok, e = REvent.admitTok tok → tok = t0) :
    AtMostTokR t0 (stepR m s e) := by
  cases e with
  | supply tok => exact hs
  | marker tok => exact hs
  | admitTok tok =>
      have htok : tok = t0 := he tok rfl
      subst htok
      by_cases hmem : tok ∈ s.data
      · simp only [stepR]
        rw [if_pos hmem]
        cases hm with
        | inl h => subst h; exact hs
        | inr hm2 =>
            cases hm2 with
            | inl h => subst h; exact hs
            | inr h => subst h; exact hs
      · simp only [stepR]
        rw [if_neg hmem]
        cases hs with
        | inl h =>
            right
            show s.data ++ [tok] = [tok]
            rw [h]
            rfl
        | inr h => exact absurd (by rw [h]; simp) hmem

theorem tagged_state_not_swap_invariant :
    swapState (replayR .reifyTagged [.admitTok 0, .admitTok 0]) ≠
      replayR .reifyTagged [.admitTok 0, .admitTok 0] := by
  decide

def taggedTranslation : Regime := ⟨2, [1], [(0, [1])], [], []⟩

theorem tagged_translation_separable :
    Derivation.separable taggedTranslation 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem untagged_translation_collapsed :
    Derivation.collapsed ⟨2, [], [], [], []⟩ 0 1 :=
  collapsed_of_no_insts _ rfl 0 1
```

The book's Lean runs the probe history under each mode by `decide`,
instantiates the marker lemma, chains the carrier bound over two steps
(the induction the paper leaves unwritten, for one history), extends the
tagged discipline to three admissions, and reads the translation regime's
shape.

```lean
-- Lean (book), textbook/checks/u38_lean.py
theorem fresh_appends (m : Mode) : stepR m emptyR (.admitTok 7) = ⟨[7], [], 0⟩ := by
  cases m <;> decide

theorem silent_two : replayR .silent [.admitTok 0, .admitTok 0] = ⟨[0], [], 0⟩ := by decide
theorem meta_two : replayR .metaMarker [.admitTok 0, .marker 0, .admitTok 0] = ⟨[0], [], 0⟩ := by
  decide
theorem fact_two : replayR .fact [.admitTok 0, .admitTok 0] = ⟨[0], [], 1⟩ := by decide

theorem marker_dropped :
    replayR .fact ([.admitTok 0, .marker 0].filter fun e => !isMarker e)
      = replayR .fact [.admitTok 0, .marker 0] :=
  markers_invisible .fact _

theorem fact_stays_singleton :
    AtMostTokR 0 (stepR .fact (stepR .fact emptyR (.admitTok 0)) (.admitTok 0)) :=
  nonreify_carrier_bound (Or.inr (Or.inr rfl))
    (nonreify_carrier_bound (Or.inr (Or.inr rfl)) (Or.inl rfl)
      (fun _ h => (REvent.admitTok.inj h).symm))
    (fun _ h => (REvent.admitTok.inj h).symm)

theorem tagged_three :
    replayR .reifyTagged [.admitTok 0, .admitTok 0, .admitTok 0] = ⟨[0, 0, 0], [1, 2], 0⟩ := by
  decide

theorem untagged_is_occurrence_here :
    replayR .reifyUntagged [.admitTok 0, .admitTok 1, .admitTok 0]
      = replayOcc [.admitTok 0, .admitTok 1, .admitTok 0] :=
  reifyUntagged_replay_eq_occurrence _

theorem swap_fixes_data (s : RState) : (swapState s).data = s.data ∧ (swapState s).refusals = s.refusals :=
  ⟨rfl, rfl⟩

theorem tagged_translation_not_collapsed : ¬ collapsed taggedTranslation 0 1 :=
  separable_not_collapsed tagged_translation_separable

theorem translations_shape :
    taggedTranslation = ⟨2, [1], [(0, [1])], [], []⟩ ∧
    taggedTranslation.forms.length = 1 ∧ taggedTranslation.insts.length = 1 :=
  ⟨rfl, rfl, rfl⟩
```

## Line-by-line Lean explanation

**`RState`, `Mode`, `stepR`.** The state derives `DecidableEq`, which is
what lets every concrete fact below be settled by `decide`. `stepR` is
total: `supply` and `marker` are identities; `admitTok` tests membership
and, on a repeat, dispatches on the mode. The tag written by
`reifyTagged` is `s.data.length`, the position the repeat is about to
occupy: a metatheoretic count admitted as object data by the discipline's
declaration, which is the price the paper names.

**`markers_invisible`.** For every mode and history, replaying the
history with its marker events removed gives the same state. The proof is
an induction on the history generalizing the start state
(`markers_invisible_from`); at each step a marker is an identity and a
non-marker is kept. `silent_eq_meta` (line 98) is `rfl` on the steppers:
the two modes differ in no clause.

**`nonreify_carrier_bound`.** One step. `supply` and `marker` change
nothing. For `admitTok tok`, the hypothesis `he` forces `tok = t0`, and
`subst` makes it so. If `tok` is already present, the three admitted modes
all leave its data list alone (three `subst`s, each closing with `hs`);
the `fact` mode increments the counter, which `AtMostTokR` does not read. The two
reifying modes are excluded by `hm`. If `tok` is absent, `s.data` is not
`[t0]` (that would contain `tok`), so by `hs` it is `[]`, and appending
gives `[tok]`, the right disjunct. The statement is about one step on one
single-token event; "the carrier never leaves the singleton" over a whole
history is the induction the book's `fact_stays_singleton` performs by
hand for two steps. The audit records the gap between the paper's "never"
and the per-step Lean as a minor interpretation defect.

**`tagged_state_not_swap_invariant`, the translations.** `swapState`
maps the tag indices `0 ↔ 1` and leaves data and refusals alone (the book's
`swap_fixes_data` says so by `rfl`). With `data = [0, 0]` that is the only
action a swap could have, so swap-invariance here is a fair reading of
"the two occurrences are symmetric", for this state. `decide` compares
`⟨[0,0],[0],0⟩` with `⟨[0,0],[1],0⟩`. `taggedTranslation` is written by
hand; there is no function from `RState` to `Regime` in the module, so
the paper's "translates to" is an asserted correspondence, and what is
proved is that the hand-written regime is separable at `(0, 1)` (by the
context `⟨0, [none]⟩`) and the bare two-datum regime is collapsed (no
instances). The audit records this too as a minor interpretation defect:
the price table rests on a reading, and the reading is reasonable, but it
is not a theorem about `RState`.

**Book: the probe under each mode.** `fresh_appends`: on the empty state
every mode appends, by cases on the mode. `silent_two`, `meta_two`
(with a marker in the middle, which `stepR` ignores), `fact_two`: the
three non-reifying results, with only the counter differing.
`marker_dropped` instantiates the marker lemma at a history with a marker.

**Book: `fact_stays_singleton`.** Two applications of the carrier bound.
The inner one starts from `emptyR`, which satisfies the left disjunct
(`Or.inl rfl`); the mode is `fact`, the third option (`Or.inr (Or.inr rfl)`);
the event is `admitTok 0`, and the side condition "any token it admits is
`0`" is discharged by injectivity of the constructor. The outer one takes
the inner result as `hs`. Three steps would nest once more; the general
statement over a history is an induction with this shape, which the
module does not write. The book's new `nonreify_history` states it for any
initial `AtMostTokR` state and any history whose admissions name only the
fixed token. Its induction carries the current state as a parameter,
applies the native one-step bound to the head, and restricts the
single-token condition to the tail. It does not classify all modes or
make any translation claim.

**Book: `tagged_three`, `untagged_is_occurrence_here`.** A third
admission tags position `2`: the tags are the positions of every repeat,
in order. The stepper identity `reifyUntagged_eq_occurrence` is lifted to
replays by Genesis (`reifyUntagged_replay_eq_occurrence`); the book
instantiates it at a two-token history to show it is not specific to the
probe.

**Book: `tagged_translation_not_collapsed`, `translations_shape`.** The
translated regime is not collapsed, by Unit 09's exclusion; and its shape
is one form, one instance, read by `rfl`. That is the sentence "exactly
one form plus one instance" with "exactly" meaning "this regime has one of
each", which is all the Lean supports.

**Axioms.** Everything decided on a derived `DecidableEq` reports
`propext, Quot.sound`; `untagged_translation_collapsed` reports `propext`
through `collapsed_of_no_insts`; the book's `rfl` theorems report none.

## What has been proved

- The silent and marker disciplines have the same stepper, and markers
  are invisible to every replay (Genesis, derived).
- The counting discipline changes the state and preserves `AtMostTokR`
  one step at a time (Genesis); for two steps of the probe, chained
  (book). The book additionally proves the arbitrary-history carrier
  bound for non-reifying modes under the same single-token restriction.
- Untagged reification is occurrence admission, as steppers and as
  replays (Genesis); the probe's untagged state is swap-invariant and the
  tagged one is not; the tagged state designates occurrence `1` (Genesis,
  `decide`).
- The hand-written tagged translation is separable and the untagged one
  collapsed (Genesis).
- Within the declared bounds, the Python table's seven rows (finite
  computation, not theorem).

## What has not been proved

- The hierarchy as a single theorem quantified over histories and modes.
  The paper's R9 lists it as unresolved; every Lean fact is per mode, per
  step, or per concrete history.
- A translation function `RState → Regime`; hence any theorem that the
  tagged discipline's separating content *is* a unary mark. Two regimes
  are exhibited; the correspondence is read, not defined.
- A native arbitrary-history version of this carrier bound. The book
  now supplies the induction over `nonreify_carrier_bound`; it keeps the
  non-reifying-mode, single-token, and initial-carrier conditions.
- That `swapState` is the only automorphism to consider: it moves tags
  only, and is adequate for the probe state, not for `RState` in general.
- A general hierarchy at carrier three or more or with multiple distinct
  tokens re-admitted (R9). The book has particular three-position examples;
  those do not supply the missing classification.
- That a discipline can be *chosen* equivariantly. The tagged discipline
  supplies an orientation by declaration; whether some meta-rule could
  select it without a choice is the module's frontier conjecture F1 and
  is OPEN.
- Note on ownership: no ledger entry lists `Refusal.*` theorems (the
  ledger's refusal section points at the later `RefusalFrontier`); the
  module's claims are owned by `paper/refusal_difference.md`. The audit
  marks this "not checked whether intentional".

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Mode` and the five clauses of `stepR` | the disciplines | declared steppers; nothing derives one from another |
| `s.data.length` as a tag | position identity | metatheoretic count admitted as data by the tagged discipline's declaration (priced in R6) |
| `refusals : Nat` | the counting discipline | an admitted counter, outside the carrier |
| the `marker` event | the meta discipline | a history record the state cannot read (`markers_invisible`) |
| `taggedTranslation` | the price | a hand-written regime, not the image of a function |
| `DecidableEq`, `decide` | every concrete fact | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** In the two-presentation probe, the three
non-reifying disciplines retain one datum and possibly a counter. The two
reifying ones retain two occurrence positions, with one tag in the tagged
mode. Position membership is readable by the chosen observation. The
hand-written regime comparison accounts for that added capability; it
does not prove a universal price for every representation.

**Phrases to read with care.**

- "Strict hierarchy, separated at every gap" (paper header and R3) is
  assembled from concrete facts; it is a reading of them, not a theorem.
- "Translates to" (R6) names a correspondence nobody defined.
- "The equivariance obstruction is not violated": correct, and worth
  saying precisely. The obstruction (`Bridge.equivariant_not_D2`) concerns choosing from a
  symmetric two-occurrence state. The tagged repeat creates an asymmetric
  two-occurrence record by its declared rule; it does not choose from the
  symmetric untagged record. Empty and singleton earlier states are not
  counterexamples to that distinction.

## Student exercise

Under `reifyTagged`, replay `[admitTok 0, admitTok 1, admitTok 0]`. What
is the state? Which positions does `swapState` exchange, and is the result
equal to the state? What does this say about `swapState` as a test of
symmetry on three-element states?

## Answer

<details>
<summary>Worked answer</summary>

The state is `⟨[0, 1, 0], [2], 0⟩`: tokens `0`, `1` fresh at positions `0`
and `1`, the repeat of `0` at position `2`, tagged. `swapState` maps tags
`0 ↔ 1` and leaves other indices alone, so the tag `2` is fixed and the
result equals the state. That only says this tag-only operation fixes
the record. It is not a classification of its symmetries. In particular,
a literal exchange of data positions 0 and 1 would change `[0,1,0]` to
`[1,0,0]`, which `swapState` does not do. It is a test for the
two-element equal-token probe state only;
on a three-element state the relevant automorphisms are permutations of
three positions acting on data and tags together, which the module does
not define. This is the audit's note on `swapState` made concrete.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Refusal.lean` lines 43-90 (state, modes, steppers), 98-133 (silent, meta, markers), 139-178 (fact), 186-222 (reification), 227-265 (tag, swap, designation), 273-287 (price) |
| Axiom report | `artifacts/lean_axioms.txt`: the module's theorems `[propext, Quot.sound]`, `untagged_translation_collapsed` `[propext]` |
| Paper | `paper/refusal_difference.md` R1-R9 (R2 table, R5 orientation, R6 price, R9 unresolved); no `CL-` ledger entry names `Refusal.*` |
| Python | `code/derivation/refusal.py`; `artifacts/refusal.json` (`disciplines`, `equivalence`, `orientation`, `capability_prices`); `tests/test_refusal.py` |
| Check (Python) | `python textbook/checks/u38_refusal.py`: the probe under all five disciplines with swap and separability, occurrence equality, the orientation and 7-event equivalence searches, the seven-row table, all against the artifact |
| Check (book Lean) | `python textbook/checks/u38_lean.py`: twelve book theorems plus six Genesis theorems kernel-checked, Lean 4.33.0 |
