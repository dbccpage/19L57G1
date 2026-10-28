# Unit 46. Rule 1 in a fixed kernel: repair, or certified exhaustion plus a tied extension family

**Claim.** `Completion` builds one common state whose fields keep apart
what the programme refuses to merge: the admitted carrier,
metatheoretic inequality facts, positive witnessed difference, view
columns, retained pairs, protected pairs, budget, license, refusals.
Observer separation reads only the columns (`sepC`); the active
obstruction is retained ∧ protected ∧ observer-zero (`obstC`), and each
condition is necessary (`obstC_conditions_independent`). The
represented kernel transports exactly (`ofWorld_sep`,
`ofWorld_obstruction`), feeding retention and protection from one
store, a stated identification; the reflective chain transports
(`chain_transport`); the oriented two-element object is not
swap-invariant, the symmetric one is in its relation store only
(`d2_transport_oriented`, `s2_transport_symmetric`,
`s2_state_not_swap_invariant`). A witness is not a separation and a
separation is not a witness (`witness_not_separation`,
`separation_not_witness`); inequality bookkeeping moves nothing
(`meta_distinctness_inert`). Rule 1 for the fixed kernel: under
well-formedness and a recorded violation, the repair family is
non-empty, or the exhaustion certificate holds and both orientation
singletons are in the extension family (`augFamily_retains_ties`,
`rule1_repair_or_extension`). Refusal is recordable exactly under the
certificate, touches no object field and changes no verdict
(`refusal_recordable`, `refusal_object_inert`,
`refusal_non_absorbing`); every event keeps the presentation signature
or strictly grows it (`action_dichotomy`); with no requirement there is
no obstruction (`rule1_needs_fidelity`); a retraction keeps the
signature and breaks preservation (`retraction_breaks_preservation`).
**Status:** derived for the fixed kernel; Rule 1 conditional on `WF`,
a replay invariant; the common state is a declared interface; the
transport facts about two-element objects are decided instances.
**Lean:** `lean4/Derivation/Completion.lean` lines 41-528, imports
`Represented` and `RefusalFrontier`. **Axioms:** `d2_transport_oriented`
and `s2_state_not_swap_invariant` none; `chain_transport` `propext`;
the other 19 `{propext, Quot.sound}`. **Depends on:** Unit 45 (the
kernel), Unit 39 (the reflective chain), Unit 44 (three separate
conditions), Units 09-10 (the two-element objects).

## Question

Unit 45 proved progress for the kernel with one requirement store.
Unit 44 insisted that retention, protection and observer-zero are three
conditions. Can one state hold the kernel, the chain and the two-element
objects at once without merging what they keep apart, and when it
does, what is Rule 1 exactly: how many branches, which family, and
where does refusal go?

## What we already possess

- `World`, `step`, `violB`, `obstructedB`, `repairFamily`, `augOkB`,
  `WF`, `wf_replay` and `represented_progress` (Unit 45).
- `PState` and `reflState n` with their two chain theorems (Unit 39).
- The oriented and symmetric two-element objects (Units 09-10).
- `ActiveObstruction` as a three-way conjunction (Unit 44).

## New concept: a common state, a transport, a family

*Common state.* Nine fields. `sepC s i j` is `any` of `sepB` over the
views; `zeroC` its negation; `obstC s i j` is membership in `retained`,
membership in `protectedReqs`, and `zeroC`.

*Transports.* `ofWorld w` copies data, views, budget, license,
refusals, and puts `w.reqs` into both `retained` and `protectedReqs`.
`ofPState s` puts the chain's data in the carrier, its relation in
`posWitness`, its tags as the single view. `swapC` is the index swap on
the pair stores and the views; it does not touch the carrier or the
inequality facts.

*Extension family.* `augFamily w (i, j)` is the two singleton columns
`[i]`, `[j]` filtered by `augOkB`. Rule 1 says: repair family
non-empty, or obstruction certificate with both singletons accepted.

*Signature.* `sigOf w` is (number of data, number of views).

## Plain-language interpretation

The common state is a form with nine boxes, and the discipline is to
never write one box's content into another. "These two are different
as far as the bookkeeper knows" (`metaDistinct`), "there is a recorded
arrow between them" (`posWitness`), "some column answers differently on
them" (`views`) are three different facts; only the third counts as
seeing a difference. The theorems about failure of transport say this
in the strongest way: a recorded arrow with no column is an obstruction,
not a separation; a column with no arrow is a separation with no
witness. The kernel of Unit 45 fits the form, but it writes its one
requirement list into both the "still owed" and the "sworn to" boxes.
That is allowed as long as it is said, and the module says it.

Rule 1 is the content of the second half. Faced with a recorded pair
that no column separates, the kernel has repairs on the existing
columns, or it has none, and then the certificate of exhaustion holds
and a new column for either member of the pair is accepted. Two
branches. Refusal is not a third: it is a note in the margin, allowed
only with the certificate, changing nothing that any later check reads.
Every event either keeps the shape of the presentation (how many
things, how many columns) or makes it strictly bigger; refusal, notes
and policy writes are in the first class with repairs. And none of this
starts without a requirement: no protected pair, no obstruction. The
last theorem shows what the acceptance guard is buying: an operation
that keeps the shape but removes a mark breaks a satisfied requirement,
so "same shape" is not "safe".

## Pseudocode

```
sepC(s, i, j)  = ∃ c ∈ s.views, sep(c, i, j)
obstC(s, i, j) = (i,j) ∈ s.retained ∧ (i,j) ∈ s.protected ∧ ¬ sepC(s, i, j)

ofWorld(w)     = (carrier w.data; meta []; witness []; views w.views;
                  retained w.reqs; protected w.reqs; budget; license; refusals)
                 ⟹ obstC(ofWorld w, i, j) = violB(w, (i, j))

augFamily(w, (i,j)) = [c ∈ [[i],[j]] | augOk(w, c)]
rule 1 (WF w, viol w (i,j)):
    repairFamily(w,(i,j)) ≠ []   ∨   (obstructed ∧ [i] ∈ augFamily ∧ [j] ∈ augFamily)

refuse i j:  recorded iff obstructed;  data, views, reqs, budget, license unchanged;
             sat, viol, markOk, augOk unchanged
sigOf(step w e) = sigOf w  ∨  data grows  ∨  views grow
reqs = []  ⟹  ¬ viol ∧ ¬ obstructed
retractFirstMark keeps sigOf and can break a satisfied pair
```

## Python

`CommonState` has no Genesis Python mirror; the check builds it as
Python (book). The extension and close families are Genesis's
`code/derivation/completion.py` (`aug_family`, `close_blocks`,
`protocols_report`), compared with `artifacts/completion_protocols.json`.

```python
from derivation import completion as C, represented as R
w = R.replay(R.PIGEON_HISTORY)
C.aug_family(w, (1, 2))     # [(1,), (2,)]  both orientations
C.close_blocks(w)           # [[('addView', (1,))], [('addView', (2,))]]
```

The check script's run:

```text
transport of the story world:
  pair (0, 1): obstC False, violB False
  pair (0, 2): obstC False, violB False
  pair (1, 2): obstC True, violB True
  retained is protected: True
the three conditions, independently (retained, protected, view):
  retained only: obstC False
  protected only: obstC False
  both, but separated: obstC False
  both, no view: obstC True
extension family (Genesis completion.aug_family) and close family:
  augFamily (1,2) [(1,), (2,)]; augFamily (0,1) [(1,)]; close blocks [[('addView', (1,))], [('addView', (2,))]]
  both orientations discharge and quiesce: True, True; the two outcomes differ: True
  artifact agrees on {'close_family_retains_both_orientations': True, 'close_family_size_on_pigeonhole': True, 'stop_outcome_empty_family': True, 'G2_driver_reproduces_supplied_stream': True}; values [True, 2, True, True]
refusal is a record:
  recorded ((1, 2),); object fields unchanged True; every verdict unchanged True; extension after refusal quiesces True
signature dichotomy over every event kind on the story world:
  ('admit', 40): (3, 1) -> (4, 1) (carrier grows)
  ('admit', 10): (3, 1) -> (3, 1) (same)
  ('require', 2, 0): (3, 1) -> (3, 1) (same)
  ('mark', (0,), 1): (3, 1) -> (3, 1) (same)
  ('addView', (1,)): (3, 1) -> (3, 2) (views grow)
  ('refuse', 1, 2): (3, 1) -> (3, 1) (same)
  ('note', 3): (3, 1) -> (3, 1) (same)
  ('setBudget', 0): (3, 1) -> (3, 1) (same)
  ('setAugLicense', False): (3, 1) -> (3, 1) (same)
  ('mark', (0,), 1): (3, 1) -> (3, 1) (same)
fidelity reduction and the retraction countermodel:
  no requirement, no violation or obstruction: True
  retraction keeps the signature True and breaks (0,1): True -> False
witness is not separation, and back:
  d2: witness True, separated False, obstructed True
  tagOnly: witness False, separated True
  d2 with one column: obstructed False
failures: []
```

## Line-by-line Python explanation

`Common` is the nine-field dataclass; `sep_c` and `obst_c` are the two
definitions; `of_world` copies the world and writes `w.reqs` twice. On
the story world of Unit 45 the obstruction verdict equals the violation
verdict on every recorded pair, which is `ofWorld_obstruction`.

The four two-element states are the four conjuncts of
`obstC_conditions_independent`: retained only, protected only, both but
with the column `[0]` separating, both with no column. Only the last
is obstructed.

`aug_family` filters `[(1,), (2,)]` by `aug_ok`; on the violated pair
both pass; on the satisfied pair `(0, 1)` the column `[0]` is already a
view, so only `[1]` passes, which shows the family is a filter and the
tie theorem needs the violation. `close_blocks` lists one event block
per accepted response over every violated pair: here two, both
augmentations. Each quiesces the world, and the two results differ:
two results kept, none chosen. The four artifact keys agree.

The refusal block records `(1, 2)`, compares the five object fields,
then every `sat`, `viol`, `mark_ok` over the menu and `aug_ok` over
four columns, before and after. The signature block runs one event of
every kind (a fresh and a repeated admission, a require, a rejected mark,
an augmentation, a refusal, a note, two policy writes) and an accepted
mark on the truncated world, and classifies each move. The fidelity
block clears the requirements; the retraction block drops the head of
the first column, which keeps the signature and un-separates `(0, 1)`.
The last block is `d2Common` and `tagOnly`, plus `d2Common` with one
column added: witness without separation is obstructed, separation
without witness is not a witness, and a column dissolves the
obstruction.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Completion.lean lines 41-82, 84-93
structure CommonState where
  carrier : List Nat
  metaDistinct : List (Nat × Nat)
  posWitness : List (Nat × Nat)
  views : List (List Nat)
  retained : List (Nat × Nat)
  protectedReqs : List (Nat × Nat)
  budget : Nat
  licensed : Bool
  refusals : List (Nat × Nat)
deriving Repr, DecidableEq

def sepC (s : CommonState) (i j : Nat) : Bool :=
  s.views.any (fun c => sepB c i j)

def zeroC (s : CommonState) (i j : Nat) : Bool := !sepC s i j

def obstC (s : CommonState) (i j : Nat) : Bool :=
  (decide ((i, j) ∈ s.retained))
    && (decide ((i, j) ∈ s.protectedReqs)) && zeroC s i j

def ofWorld (w : World) : CommonState :=
  { carrier := w.data
    metaDistinct := []
    posWitness := []
    views := w.views
    retained := w.reqs
    protectedReqs := w.reqs
    budget := w.budget
    licensed := w.augLicensed
    refusals := w.refusals }

theorem ofWorld_sep (w : World) (i j : Nat) :
    sepC (ofWorld w) i j = satB w (i, j) := rfl

theorem ofWorld_obstruction (w : World) (i j : Nat) :
    obstC (ofWorld w) i j = violB w (i, j) := by
  unfold obstC violB ofWorld zeroC sepC
  cases decide ((i, j) ∈ w.reqs) <;> rfl
```

```lean
-- Lean (Genesis), lean4/Derivation/Completion.lean lines 135-156, 165-229, 231-234
def ofPState (s : PState) : CommonState :=
  { carrier := s.data
    metaDistinct := []
    posWitness := s.rel
    views := [s.tags]
    retained := []
    protectedReqs := []
    budget := 0
    licensed := true
    refusals := [] }

theorem chain_transport (n : Nat) :
    (ofPState (reflState n)).carrier = List.range (n + 1) ∧
      (ofPState (reflState n)).posWitness =
        (List.range n).map (fun k => (k, k + 1)) := by
  constructor
  · show (reflState n).data = _
    exact reflective_chain_is_initial_segment n
  · show (reflState n).rel = _
    exact reflective_chain_successor_relation n

def swapIdx (x : Nat) : Nat := if x = 0 then 1 else if x = 1 then 0 else x

def swapC (s : CommonState) : CommonState :=
  { s with
    posWitness := s.posWitness.map (fun p => (swapIdx p.1, swapIdx p.2))
    views := s.views.map (fun c => c.map swapIdx)
    retained := s.retained.map (fun p => (swapIdx p.1, swapIdx p.2))
    protectedReqs :=
      s.protectedReqs.map (fun p => (swapIdx p.1, swapIdx p.2)) }

def d2Common : CommonState :=
  { carrier := [0, 1], metaDistinct := [(0, 1)],
    posWitness := [(0, 1)], views := [], retained := [(0, 1)],
    protectedReqs := [(0, 1)], budget := 0, licensed := true,
    refusals := [] }

def s2Common : CommonState :=
  { d2Common with posWitness := [(0, 1), (1, 0)] }

theorem d2_transport_oriented : swapC d2Common ≠ d2Common := by decide

theorem s2_transport_symmetric :
    (swapC s2Common).posWitness.length = s2Common.posWitness.length ∧
      ((0, 1) ∈ (swapC s2Common).posWitness ↔
        (0, 1) ∈ s2Common.posWitness) ∧
      ((1, 0) ∈ (swapC s2Common).posWitness ↔
        (1, 0) ∈ s2Common.posWitness) := by decide

theorem s2_state_not_swap_invariant : swapC s2Common ≠ s2Common := by
  decide

theorem witness_not_separation :
    (0, 1) ∈ d2Common.posWitness ∧ zeroC d2Common 0 1 = true := by
  decide

def tagOnly : CommonState :=
  { carrier := [0, 1], metaDistinct := [], posWitness := [],
    views := [[0]], retained := [], protectedReqs := [], budget := 0,
    licensed := true, refusals := [] }

theorem separation_not_witness :
    sepC tagOnly 0 1 = true ∧ tagOnly.posWitness = [] := by decide

theorem meta_distinctness_inert (s : CommonState) (facts) (i j : Nat) :
    sepC { s with metaDistinct := facts } i j = sepC s i j ∧
      obstC { s with metaDistinct := facts } i j = obstC s i j :=
  ⟨rfl, rfl⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/Completion.lean lines 264-269, 279-282 (statement), 362-386, 393-396, 416-422, 428-436, 443-447, 496-498, 514-528
def augFamily (w : World) (r : Req) : List View :=
  [[r.1], [r.2]].filter (fun c => augOkB w c)

theorem augFamily_sound {w : World} {r : Req} {c : View}
    (h : c ∈ augFamily w r) : augOkB w c = true :=
  (List.mem_filter.mp h).2

theorem augFamily_retains_ties {w : World} {i j : Nat} (hwf : WF w)
    (hviol : violB w (i, j) = true) :
    [i] ∈ augFamily w (i, j) ∧ [j] ∈ augFamily w (i, j) := by
  -- (i, j) recorded, unsatisfied; WF gives i ≠ j and bounds;
  -- satB w (j, i) = false by sepB_symm; then for each of a = i, b = j
  -- and a = j, b = i: [a] separates a from b, is not a view (else the
  -- pair were satisfied), is bounded, fresh and increasing; so augOkB.

theorem rule1_repair_or_extension {w : World} {i j : Nat} (hwf : WF w)
    (hviol : violB w (i, j) = true) :
    (∃ m, m ∈ repairFamily w (i, j)) ∨
      (obstructedB w (i, j) = true ∧
        [i] ∈ augFamily w (i, j) ∧ [j] ∈ augFamily w (i, j)) := by
  cases hfam : repairFamily w (i, j) with
  | cons m t => exact Or.inl ⟨m, List.mem_cons_self⟩
  | nil =>
      right
      have hobs : obstructedB w (i, j) = true := by
        unfold obstructedB
        rw [hviol]
        have hall : (responseMenu w).all
            (fun m => !repairsB w m (i, j)) = true := by
          simp only [List.all_eq_true]
          intro m hm
          cases hb : repairsB w m (i, j) with
          | false => rfl
          | true =>
              have : m ∈ repairFamily w (i, j) :=
                repairFamily_complete hm hb
              rw [hfam] at this
              cases this
        rw [hall]
        rfl
      obtain ⟨h1, h2⟩ := augFamily_retains_ties hwf hviol
      exact ⟨hobs, h1, h2⟩

theorem refusal_recordable {w : World} {i j : Nat}
    (hobs : obstructedB w (i, j) = true) :
    (i, j) ∈ (step w (.refuse i j)).refusals := by

theorem refusal_object_inert (w : World) (i j : Nat) :
    (step w (.refuse i j)).data = w.data ∧
      (step w (.refuse i j)).views = w.views ∧
      (step w (.refuse i j)).reqs = w.reqs ∧
      (step w (.refuse i j)).budget = w.budget ∧
      (step w (.refuse i j)).augLicensed = w.augLicensed := by
  simp only [step]
  split <;> exact ⟨rfl, rfl, rfl, rfl, rfl⟩

theorem refusal_non_absorbing (w : World) (i j : Nat) (r : Req)
    (v : View) (p : Nat) (c : View) :
    satB (step w (.refuse i j)) r = satB w r ∧
      violB (step w (.refuse i j)) r = violB w r ∧
      markOkB (step w (.refuse i j)) v p = markOkB w v p ∧
      augOkB (step w (.refuse i j)) c = augOkB w c := by
  simp only [step]
  split <;> exact ⟨rfl, rfl, rfl, rfl⟩

def sigOf (w : World) : Nat × Nat := (w.data.length, w.views.length)

theorem action_dichotomy (w : World) (e : Event) :
    sigOf (step w e) = sigOf w ∨
      (sigOf w).1 < (sigOf (step w e)).1 ∨
      (sigOf w).2 < (sigOf (step w e)).2 := by

theorem rule1_needs_fidelity (w : World) (h : w.reqs = [])
    (r : Req) : violB w r = false ∧ obstructedB w r = false := by

def retractFirstMark (w : World) : World :=
  { w with views :=
      match w.views with
      | [] => []
      | c :: rest => c.drop 1 :: rest }

theorem retraction_breaks_preservation :
    satB { data := [10, 20], views := [[0]], reqs := [(0, 1)],
           refusals := [], budget := 9, augLicensed := true,
           notes := [] } (0, 1) = true ∧
      satB (retractFirstMark
        { data := [10, 20], views := [[0]], reqs := [(0, 1)],
          refusals := [], budget := 9, augLicensed := true,
          notes := [] }) (0, 1) = false := by decide
```

The book's Lean transports the story of Unit 45, applies Rule 1 to it,
shows the other orientation discharging, puts a refusal before an
extension, lists signatures, and makes the two-element facts concrete.

```lean
-- Lean (book), textbook/checks/u46_lean.py
def story : World :=
  replay [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
    .require 0 1, .require 0 2, .require 1 2, .addView [0]] genesis

theorem transport_instance :
    obstC (ofWorld story) 1 2 = true ∧ obstC (ofWorld story) 0 1 = false ∧
    sepC (ofWorld story) 0 1 = true := by decide

theorem same_store (w : World) : (ofWorld w).retained = (ofWorld w).protectedReqs := rfl

theorem family_instances :
    augFamily story (1, 2) = [[1], [2]] ∧ augFamily story (0, 1) = [[1]] ∧
    augFamily story (0, 2) = [[2]] := by decide

theorem rule1_instance :
    (∃ m, m ∈ repairFamily story (1, 2)) ∨
      (obstructedB story (1, 2) = true ∧
        [1] ∈ augFamily story (1, 2) ∧ [2] ∈ augFamily story (1, 2)) :=
  rule1_repair_or_extension (wf_replay _) (by decide)

theorem other_orientation_discharges :
    satB (augApply story [2]) (1, 2) = true ∧ quiescentB (step story (.addView [2])) = true := by decide

theorem refusal_then_extension :
    (step (step story (.refuse 1 2)) (.addView [1])).views = [[0], [1]] ∧
    (step (step story (.refuse 1 2)) (.addView [1])).refusals = [(1, 2)] := by decide

theorem refusal_recordable_instance : (1, 2) ∈ (step story (.refuse 1 2)).refusals :=
  refusal_recordable (by decide)

theorem signature_instances :
    sigOf story = (3, 1) ∧ sigOf (step story (.addView [1])) = (3, 2) ∧
    sigOf (step story (.admitTok 40)) = (4, 1) ∧
    sigOf (step truncWorld (.mark [0] 1)) = sigOf truncWorld ∧
    (step truncWorld (.mark [0] 1)).views = [[1, 0]] := by decide

theorem fidelity_instance : obstructedB { story with reqs := [] } (1, 2) = false :=
  (rule1_needs_fidelity _ rfl _).2

def owW : World :=
  { data := [10, 20], views := [[0]], reqs := [(0, 1)], refusals := [], budget := 9,
    augLicensed := true, notes := [] }

theorem retraction_same_signature :
    sigOf (retractFirstMark owW) = sigOf owW ∧ satB (retractFirstMark owW) (0, 1) = false := by decide

theorem d2_with_view :
    obstC d2Common 0 1 = true ∧ obstC { d2Common with views := [[0]] } 0 1 = false := by decide

theorem swap_twice : swapC (swapC d2Common) = d2Common := by decide

theorem s2_swapped :
    (swapC s2Common).posWitness = [(1, 0), (0, 1)] ∧ (swapC s2Common).retained = [(1, 0)] := by decide

theorem chain_three :
    (ofPState (reflState 3)).carrier = [0, 1, 2, 3] ∧
    (ofPState (reflState 3)).posWitness = [(0, 1), (1, 2), (2, 3)] ∧
    sepC (ofPState (reflState 3)) 0 1 = true ∧
    zeroC (ofPState (reflState 3)) 1 2 = true := by decide

theorem meta_inert_instance :
    obstC { d2Common with metaDistinct := [] } 0 1 = obstC d2Common 0 1 :=
  (meta_distinctness_inert d2Common [] 0 1).2
```

## Line-by-line Lean explanation

**`CommonState`, `sepC`, `zeroC`, `obstC` (41-69).** Nine fields with
`DecidableEq`, so the two-element facts close by `decide`. `sepC` reads
`views` only; `posWitness` and `metaDistinct` are never read by any
verdict, which the docstring calls the point. `obstC` is the Unit 44
conjunction with the three conditions as fields.

**`ofWorld` and its two theorems (73-93).** The transport writes
`w.reqs` into `retained` and into `protectedReqs`. `ofWorld_sep` is
`rfl` (`sepC` over `w.views` is `satB`). `ofWorld_obstruction` unfolds
both sides and cases on the one membership `decide`; with it `false`
both sides are `false`, with it `true` both reduce to `!satB`. The
book's `same_store` is the identification as a `rfl`, and the audit's
reading: in the common state the two are independent; in the kernel
transport they are one store, by declaration.

**`obstC_conditions_independent` (95-113).** Four concrete states, four
`decide`s. The third has `views := [[0]]`, so `zeroC` fails; the fourth
has no view and is obstructed.

**`ofPState` and `chain_transport` (135-162).** The chain's tags become
the one view. `chain_transport n` is the two chain theorems of Unit 39
behind a `show`. The book's `chain_three` evaluates depth 3: the tags
column `[1, 2, 3]` separates the root `0` from `1` and leaves `1`, `2`
observer-equal. A chain in the common state has one coarse column.

**The two-element objects (165-211).** `swapIdx` exchanges `0` and `1`;
`swapC` maps it over four fields and leaves `carrier` and
`metaDistinct` alone, which the audit flags as part of why
`d2_transport_oriented` holds. `s2_transport_symmetric` is three
`decide` facts about the one concrete state: same length, same two
members. `s2_state_not_swap_invariant` is the boundary: the retained
and protected stores carry `(0, 1)` and become `(1, 0)`. The book's
`s2_swapped` prints both: the relation store in the other order, the
protection store as the other pair; `swap_twice` is the involution on
the oriented object.

**The transport failures (213-229).** `witness_not_separation`: the
oriented object has its arrow and no column, so `zeroC`. The book's
`d2_with_view` shows the obstruction, then adds the column `[0]` and
the obstruction goes: an obstruction is dissolved by an observation,
not by an arrow. `separation_not_witness`: `tagOnly` has a column and
no arrow. `meta_distinctness_inert` is two `rfl`s because neither
definition reads the field.

**`early_collapse_transports` (241-247).** `zeroC` of a viewless state.
The audit calls it information-free; the lesson omits it.

**`augFamily` (264-269).** Two candidates filtered. `augFamily_sound`
is one direction of `List.mem_filter`. The book's `family_instances`
shows the filter at work on a satisfied pair: `[0]` is a view already.

**`augFamily_retains_ties` (279-360).** From the violation, membership
and `satB = false`; from `WF`, `i ≠ j` and bounds; `satB w (j, i) =
false` by `sepB_symm`; then a local lemma `haug` proves `augOkB w [a]`
from `a ≠ b`, bounds and `satB w (a, b) = false`, exactly the
`represented_progress` argument of Unit 45 made symmetric in the pair;
applied twice. The docstring says what changed: the orientation of the
recorded pair selects nothing, both selections are in the family.

**`rule1_repair_or_extension` (362-391).** Case on the repair family;
non-empty is the left branch; empty gives the certificate as in Unit 45,
then the tie theorem. It was once named `rule1_trichotomy`; the
correction ledger records that no third branch is claimed. The book's
`rule1_instance` applies it to the story and `other_orientation_discharges`
takes the branch the paper's story did not: `[2]` also quiesces.

**Refusal (393-440).** `refusal_recordable` cases on prior membership:
already there, or appended. `refusal_object_inert` and
`refusal_non_absorbing` `split` on the guard and close every conjunct by
`rfl`, because `refuse` writes only `refusals` and no verdict reads it.
The book's `refusal_then_extension` is the sequence the words describe.

**`sigOf` and `action_dichotomy` (443-494).** Eight cases: a fresh
admission grows the carrier by one (`List.length_append`), an accepted
augmentation grows the views by one, an accepted mark keeps both
(`List.length_map`), and every rejected or recording event is `rfl`.
The book's `signature_instances` shows all three moves.

**`rule1_needs_fidelity` (496-512).** With `reqs = []`, membership is
false, so `violB` is `false` and `obstructedB` with it. The book's
`fidelity_instance` applies it with `rfl` for the hypothesis.

**`retraction_breaks_preservation` (514-528).** Drop the head of the
first column; the concrete world is satisfied before and not after. The
book's `retraction_same_signature` adds that the signature is unchanged,
which is why the preservation law is the guard's work and not the
measure's.

## What has been proved

- The common state's obstruction equals the kernel's violation under
  the stated identification; each of the three conditions is necessary
  (Genesis).
- The chain transports with its carrier and arrows (Genesis) and with
  one coarse column (book, at depth 3).
- The oriented object is not swap-invariant; the symmetric one is in
  its relation store and not as a whole state (Genesis, decided
  instances).
- Witness and separation do not transport into each other; inequality
  bookkeeping is inert (Genesis).
- Rule 1 for the fixed kernel: repair family or certificate with both
  orientation singletons accepted, under `WF` and a violation (Genesis;
  applied to the story in the book, both branches of the extension
  shown to discharge).
- Refusal is recordable under the certificate, inert on object fields
  and on every verdict; the action algebra is binary by the signature;
  no requirement, no obstruction; retraction keeps the signature and
  breaks preservation (Genesis).

## What has not been proved

- That `CommonState` is the right or only common state, or that
  retention and protection should be one store: the identification is
  declared.
- That `augFamily` lists every accepted augmentation: it is the two
  singletons, a declared family.
- Any transport of the full early `Regime`; the docstring defers it to
  the token-erased simulation of the map.
- Swap-invariance of the symmetric object as a general lemma: it is
  three facts about one state.
- Anything about refusal under a semantics other than the kernel's.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `CommonState` and its nine fields | the common interface | declared |
| `ofWorld`'s double write of `w.reqs` | the kernel transport | declared identification, disclosed in the source and ledger |
| `reflState : Nat → PState` | the chain transport | supplied constructor (Unit 39); the `∀ n` is metatheory |
| `swapC` not touching `carrier`, `metaDistinct` | the two-element transport | declared common form of the transposition |
| `sigOf` | the action dichotomy | a declared measure |
| `List`, `decide`, `omega` | computation | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The separations: witness, separation and
bookkeeping are three fields and three verdicts; the repair family and
the extension family are filters with ties kept; refusal is a record
with a certificate.

**Phrases to read with care.**

- "Three independent obstruction conditions": in the common state; the
  kernel transport feeds two of them from one list.
- "S2 symmetry transports": for the relation store of one state; the
  protection stores are oriented.
- "Rule 1 settled for the fixed kernel": two branches, conditional on
  `WF` and the constitution; no trichotomy.
- "Refusal is outside the action algebra": by the signature measure and
  by the verdicts it leaves unchanged; the history producer still
  decides when a run ends.

## Student exercise

Take `s2Common`. Compute `obstC s2Common 0 1`, `obstC s2Common 1 0`,
and the same two on `swapC s2Common`. Then say which of the module's
two symmetry statements each result bears on, and what a reader would
get wrong by calling `s2Common` "swap-invariant" without the
qualification.

## Answer

`s2Common` has `retained = [(0, 1)]`, `protectedReqs = [(0, 1)]`, no
views. So `obstC s2Common 0 1 = true` (retained, protected, no column)
and `obstC s2Common 1 0 = false` (`(1, 0)` is in neither store).
`swapC s2Common` maps both stores to `[(1, 0)]` and the relation store
to `[(1, 0), (0, 1)]`; so `obstC (swapC s2Common) 0 1 = false` and
`obstC (swapC s2Common) 1 0 = true`. The relation store is the same set
before and after, which is `s2_transport_symmetric`; the obstruction
verdicts are exchanged, which is the content of
`s2_state_not_swap_invariant`. A reader who called the state
swap-invariant would conclude that the obstruction is symmetric, and it
is not: the symmetric object's relation is symmetric, its protection
bookkeeping is oriented, and the module's docstring scopes the claim to
the first.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Completion.lean` lines 41-93 (common state, kernel transport), 95-130 (independence, quiescence), 135-162 (chain), 165-211 (two-element objects), 213-247 (transport failures), 264-391 (extension family, Rule 1), 393-440 (refusal), 443-494 (signature), 496-528 (fidelity, retraction) |
| Axiom report | `artifacts/lean_axioms.txt` lines 259-280: `d2_transport_oriented`, `s2_state_not_swap_invariant` none; `chain_transport` `propext`; 19 `{propext, Quot.sound}` |
| Paper | `paper/native_derivation_completion.md` sections 5 (the common native interface) and 7 (the strongest form of Rule 1); `paper/native_derivation_map.md` rows "active obstruction" and "refusal"; `paper/paper_claim_ledger.md` `CL-NC-COMMON-STATE`, `CL-NC-RULE1`; `paper/pr11_correction_ledger.md` C1, C4 |
| Python | `code/derivation/completion.py` (`aug_family`, `close_blocks`, `protocols_report`), `artifacts/completion_protocols.json`, `tests/test_completion.py` (`test_close_family_complete_and_tie_retained`); no Genesis mirror of `CommonState` |
| Check (Python, partly book) | `python textbook/checks/u46_completion.py`: the transport and the four independence states (book), the families against the artifact, refusal inertness over every verdict, the signature over every event kind, fidelity, retraction, witness against separation |
| Check (book Lean) | `python textbook/checks/u46_lean.py`: fifteen book declarations plus sixteen Genesis theorems kernel-checked, Lean 4.33.0 |
