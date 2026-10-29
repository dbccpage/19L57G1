# Unit 45. Replaying represented events under a fixed kernel

**Claim.** The fixed step function uses the represented world and supplied
event. Operational support ignores notes, although the full record keeps
them. Available repairs and augmentations still require the separate
execution guards, including budget and permission.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** `Represented` answers an external challenge of 2026-08-12
with one small kernel.

A `World` holds admitted tokens, view columns,
recorded requirements, recorded refusals, a budget, an augmentation
license and an inert `notes` field; eight kinds of `Event` carry their
own content; a guarded `step` takes the world and the event and nothing
else; `replay` folds a history.

Relative to this fixed constitution
(grammar, separation law, response menu, guards, history producer),
the step factors through the represented support
(`support_determines`), is invariant under replay-equivalence
(`equiv_step`, `equiv_replay`, `equiv_repairFamily`), keeps all tied
repairs (`repairFamily_retains_ties`), and an accepted repair or
augmentation is sound (`step_mark_sound`, `satB_aug`, `aug_increases`).

On a well-formed world every violation has a non-empty repair family or
is a certified obstruction whose one-column augmentation passes
`augOkB` and would discharge it under `augApply`
(`represented_progress`); this does not yet apply an event. Budget and license
gate the application (`progress_needs_budget`, `progress_needs_license`);
violations arise only from `require` (`violation_only_from_require`,
`quiescent_stable`); a supplied stream gives a prefix-compatible
unbounded run (`productive_run`); a refusal needs the certificate
(`refusal_needs_certificate`).

Certification by a panel of represented
evaluators is exactly joint separation by the panel's own columns
(`cert_scope`) and is not correspondence (`cert_not_correspondence`,
`cert_panel_relative`).

Eight countermodels fail exactly one theorem
each.

**Status:** derived relative to the declared constitution;
`represented_progress` conditional on `WF`, which is an invariant of
replay; `step_mark_sound` and `aug_increases` conditional on their
guards; the productive run is about a supplied stream; the countermodels
are decided instances. **Lean:** `lean4/Derivation/Represented.lean`
lines 58-1362, core Lean only. **Axioms:** `wf_genesis` and
`histUpTo_prefix` use none; `bool_eq_of_iff`, `or_not_eq_true`
`propext`; the other 44 reported theorems `{propext, Quot.sound}`;
17 congruence helpers are not in the report. **Depends on:** nothing in
Genesis; recorded requirements (Unit 17) and the separate interface of
Unit 44 provide comparison points. This module declares its own response
menu and exhaustion predicate.

</details>

## First pass

Use three positions, A, B, and C. One column says Yes on A and No on
B and C. Record only the requirement “separate B from C.” Give the world
one unit of budget.

Request a mark on B in that column:

| Pair | Before | After |
|---|---|---|
| B/C, required | Same answers | Different answers |
| A/B, not required | Different answers | Same answers |

The kernel accepts the mark. It meets the recorded requirement, and no
previously satisfied recorded requirement is lost. The unprotected A/B
distinction can disappear. This kernel's preservation rule is therefore
weaker than Unit 44's closure rule, which preserves every old distinction.

The world holds the current data, columns, requirements, policy fields,
and records. The event requests one specified operation; the step checks
its guards. Replaying the same events from the same starting world gives
the same result under this fixed definition.

**Predict:** is writing a note the same as doing nothing to the record?

<details>
<summary>Check your prediction</summary>

No. The notes list changes. The operational-support projection ignores
that list, so its value and future support behavior stay the same for the
same supplied events.

</details>

## Question

Earlier units let an evaluator, a tie-break or a "next fresh name" sit
in the metatheory. If every input that can change a transition must be
written into the state or the history, what does the machine look like,
what can still be proved about progress, and what does a hidden input
break?

## What we already possess

- Regimes, admission events and replay from genesis (Units 05-08).
- Recorded requirements (Unit 17) and the three-way obstruction interface
  (Unit 44). Exhaustive failure of this kernel's menu is a separate
  predicate defined below, not Unit 29's collapse-transport theorem.
- Reflection, obstruction, closure and proposal as types (Unit 44).
- Lists, `any`/`all`, `filter`, membership and `decide`.

## New concept: a world, an event, a guard

*World.* Seven fields: `data : List Nat` (admitted tokens, in order:
position is identity), `views : List View` (each a list of positions),
`reqs : List (Nat × Nat)` (pairs to be separated), `refusals`,
`budget : Nat`, `augLicensed : Bool`, `notes : List Nat`. `genesis` is
empty with budget 0 and license on.

Unlike the earlier regime's small-first impose guard, `reqOkB` requires
distinct admitted positions without requiring `i < j`. Both orientations
can be recorded. The model change is explicit; the two guards are not
interchangeable.

*Laws.* `sepB c i j` holds when exactly one of `i`, `j` is in column
`c`; `satB w r` when some view separates `r`; `violB w r` when `r` is
recorded and not satisfied; `quiescentB w` when every recorded pair is
satisfied.

*Responses.* A mark `(v, p)` prepends position `p` to the column `v`
(matched by value, wherever it occurs); it is accepted (`markOkB`) when
`v` is a view, `p` is in bounds and not yet in `v`, the mark discharges
some violation and preserves every satisfied requirement. An
augmentation `c` appends a column; it is accepted (`augOkB`) when `c` is
in bounds, not already a view, and separates some bounded pair no view
separates. The `responseMenu` is every (view, position) pair; the
`repairFamily` of `r` is the menu filtered by "accepted and satisfies
`r`"; `obstructedB w r` is `violB` together with every menu item failing.

*Events and step.* `admitTok`, `require`, `mark`, `addView`, `refuse`,
`note`, `setBudget`, `setAugLicense`. Each guarded event is a no-op when
its guard fails; `mark` and `addView` also need `0 < budget` and spend
one; `addView` needs the license; `refuse i j` records the pair only if
`obstructedB` holds and it is not already recorded. `note`, `setBudget`
and `setAugLicense` have no guard.

*Support and equivalence.* `supp w` is the world without `notes`.
`WEquiv w w'`: equal data (literally), membership-equal views,
requirements and refusals, equal budget and license.

The progress theorem's `WF w` means every recorded requirement has
distinct endpoints below the datum count. It is not a certificate that
all fields of a raw `World` satisfy every desirable invariant. Replays
from genesis satisfy this particular predicate by `wf_replay`.

## Plain-language interpretation

Picture a ledger. Tokens are entered in order and never removed. Each
column is a yes/no question about positions. A requirement says "these
two positions must get different answers from some column". A repair
flips one answer in one existing column, and is allowed only if it
settles some open requirement and preserves every previously satisfied
recorded requirement. It can merge a pair that was never required. The
book checks a three-position example: with only `(1,2)` required,
marking position 1 in column `[0]` settles `(1,2)` while losing the old
separation of `(0,1)`. This is weaker than Unit 44's `ClosureStep`, which
preserves every old observer distinction. An augmentation adds a
column, and is allowed only if it tells apart a pair nothing told apart
before. An obstruction is a recorded, still-open requirement for which
every possible repair on the current columns has been tried and failed:
not "these two look alike", but "the whole menu is exhausted". A
refusal may be written down only with that certificate, and writing it
down stops nothing.

The point of the module is in the type of `step`: it reads the world
and the event. There is no clock, no random number, no outside judge.
So two runs with the same history from the same world agree, by the
fixed definition; the commentary field cannot influence the successor's
operational support. The whole world can still differ in its notes. Two
worlds whose columns are the same set but listed in different orders
behave the same; and the repair family is a filter, so no tie is ever
broken. What the module does not claim: that the grammar, the laws, the
menu or the guards derive themselves. They are the fixed constitution,
named as such in the header, and the theorems hold relative to it.

Two things the lesson flags. First, the budget and the license are
real gates, and `setBudget` has no guard: whatever feeds the event
stream can refill the budget before every repair, as the supplied
productive stream does at every stage. "Progress is never free" is true
of one step, not of a run. Second, the "represented König failure" is a
theorem about every Lean function `Nat → Nat`; the kernel represents no
such object. The adjective belongs to the conclusion (witnesses at
every length, no single source), not to the quantifier.

## Pseudocode

```
sep(c, i, j)   = (i ∈ c) xor (j ∈ c)
sat(w, r)      = ∃ c ∈ w.views, sep(c, r)
viol(w, r)     = r ∈ w.reqs ∧ ¬ sat(w, r)
markOk(w,v,p)  = v ∈ views ∧ p < |data| ∧ p ∉ v ∧ dischargesSome(w, mark(w,v,p)) ∧ preserves(w, mark(w,v,p))
augOk(w, c)    = c ⊆ positions ∧ c ∉ views ∧ ∃ i≠j bounded, sep(c,i,j) ∧ ¬ sat(w,(i,j))
menu(w)        = [(v, p) | v ∈ views, p < |data|]
family(w, r)   = [m ∈ menu(w) | markOk(w, m) ∧ sat(mark(w, m), r)]
obstructed     = viol(w, r) ∧ family(w, r) = []

step(w, e):  admitTok t    → append t unless present
             require i j   → append (i,j) if i≠j, bounded, new
             mark v p      → if markOk ∧ budget>0: apply, budget−1
             addView c     → if augOk ∧ licensed ∧ budget>0: append, budget−1
             refuse i j    → if obstructed ∧ new: record
             note / setBudget / setAugLicense → write the field
replay(h, w) = foldl step w h

progress (WF w, viol w (i,j)):  family(w,(i,j)) ≠ []  ∨  (obstructed ∧ augOk(w,[i]) ∧ sat(aug(w,[i]),(i,j)))
```

## Python

Genesis's mirror is `code/derivation/represented.py`, artifact
`artifacts/represented.json`.

```python
from derivation import represented as R
w = R.replay(R.PIGEON_HISTORY)      # three tokens, three requirements, one column [0]
R.repair_family(w, (1, 2))         # []  : no mark on [0] separates positions 1 and 2
R.obstructed(w, (1, 2))            # True
R.quiescent(R.step(w, ("addView", (1,))))   # True
```

The check script's run:

```text
story world: {'data': [10, 20, 30], 'views': [[0]], 'reqs': [[0, 1], [0, 2], [1, 2]], 'refusals': [], 'budget': 8, 'aug_licensed': True, 'notes': []}
  wf True; violated (1,2) True; repair family (1,2) []; obstructed (1,2) True
  menu: [((0,), 0), ((0,), 1), ((0,), 2)]
  addView [1] accepted True; sat (1,2) after True; quiescent after True; budget 8 -> 7
  artifact agrees: True
gates:
  budget 0: addView no-op True, mark no-op True; setBudget 4 -> budget 4 (no guard)
  license off: addView no-op True
refusal:
  refuse (1,2) records ((1, 2),); refuse (0,1) (satisfied) no-op True; after refusal the augmentation still fires: True, refusals kept ((1, 2),)
productive run, stages 0..15:
  k=0: history 1 events, carrier [0], quiescent True, prefix of next True
  k=1: history 5 events, carrier [0, 1], quiescent True, prefix of next True
  k=2: history 9 events, carrier [0, 1, 2], quiescent True, prefix of next True
  k=3: history 13 events, carrier [0, 1, 2, 3], quiescent True, prefix of next True
  ... all 16: {'all_prefix_compatible': True, 'carriers_are_initial_segments': True, 'all_events_accepted': True, 'all_quiescent': True}; artifact agrees: True
countermodels (name, kind, differs):
  unrecorded_scheduler: hidden_runtime_input, True
  unrecorded_fresh_name_source: hidden_runtime_input, True
  hidden_evaluator: hidden_runtime_input, True
  incomplete_search_false_obstruction: semantic_inference_failure, True
  destructive_rewrite_not_augmentation: semantic_inference_failure, True
  repetition_mislabeled_as_progress: semantic_inference_failure, True
  order_sensitive_semantics_splits_equivalents: hidden_runtime_input, True
  artifact agrees: True
  the kernel on the two equivalent worlds: True and True (equal: True)
  the repairs the truncated search missed: [((0,), 1), ((0,), 2)]
certification: {'panel_certifies_equivalent': True, 'outside_column_separates': True, 'certification_is_panel_relative': True}; artifact agrees: True
  panel [[0]] certifies (0,1): True; add a blind evaluator: False; give it the column: True
per-length witnesses: {'witness_at_every_length': True, 'sampled_infinite_sources_refuted': True}; artifact agrees: True
  wit_valid [3,3,3] True; wit_valid [0] False
mutation: {'replay_deterministic': True, 'every_single_event_mutation_detected': True, 'mutations_checked': 8}; artifact agrees: True
failures: []
```

## Line-by-line Python explanation

`World` is a frozen dataclass with the seven fields as tuples; `step`
dispatches on the event's first entry and rejects negative numbers,
which keeps the carrier the naturals as in Lean. `PIGEON_HISTORY` sets
budget 9, admits three tokens, records the three pairs and adds the
column `[0]`, which costs one budget. The menu has three items, marks
of positions 0, 1, 2 on `[0]`: 0 is already in it; marking 1 or 2
would make `[0, 1]` or `[0, 2]`, which still gives positions 1 and 2
the same answer. So the family is empty and the pair is obstructed.
The column `[1]` is in bounds, new, and separates 1 from 2, so
`addView` is accepted; afterwards all three pairs are satisfied.

The gate lines zero the budget and switch the license off and show the
no-ops, and show `setBudget 4` taking effect with no condition. The
refusal lines record `(1, 2)` and refuse to record `(0, 1)`, and show
that after the refusal the augmentation still fires and the refusal is
kept: refusal certifies, it does not terminate.

`productivity_report` replays the supplied stream `hist_up_to(k)`
(admit 0; then for each stage `setBudget 1`, admit `k`, require
`(0, k)`, add the column `[k]`): each history is a prefix of the next,
every event is accepted, every stage is quiescent, the carrier is
`0..k`. The countermodel rows reproduce the module's eight: the first
three and the seventh consume an input outside the state and history
(a scheduler bit, a seed, an oracle, the list position of a column);
the other three are a wrong definition or a wrong reading. Beside the
seventh, the check runs the kernel's own `step` on the two equivalent
worlds and gets the same verdict; beside the fourth it lists the two
repairs the truncated search never reached.

`certification_report` and the three panel lines: one evaluator with
the column `[0]` certifies `(0, 1)` separated; adding an evaluator
whose only column is `[0, 1]` breaks the unanimity; giving it the
column `[0]` as well restores it. `koenig_report` checks the witness
`[n, …, n]` at each length and refutes sampled sources; the two
`wit_valid` lines are the smallest instances. `mutation_report`
replaces each event of the story by a note and sees the final world
change every time.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Represented.lean lines 80-90, 94-101, 117-122, 133-135, 144-156
structure World where
  data : List Nat
  views : List View
  reqs : List Req
  refusals : List Req
  budget : Nat
  augLicensed : Bool
  notes : List Nat
deriving Repr, DecidableEq

def genesis : World := ⟨[], [], [], [], 0, true, []⟩

def sepB (c : View) (i j : Nat) : Bool :=
  (decide (i ∈ c)) != (decide (j ∈ c))

def satB (w : World) (r : Req) : Bool :=
  w.views.any (fun c => sepB c r.1 r.2)

def violB (w : World) (r : Req) : Bool :=
  (decide (r ∈ w.reqs)) && !satB w r

def markOkB (w : World) (v : View) (p : Nat) : Bool :=
  (decide (v ∈ w.views)) && (decide (p < w.data.length))
    && !(decide (p ∈ v))
    && dischargesSomeB w (markApply w v p)
    && preservesB w (markApply w v p)

def augOkB (w : World) (c : View) : Bool :=
  c.all (fun p => decide (p < w.data.length))
    && !(decide (c ∈ w.views))
    && increaseB w c

def responseMenu (w : World) : List (View × Nat) :=
  w.views.flatMap fun v =>
    (List.range w.data.length).map fun p => (v, p)

def repairsB (w : World) (m : View × Nat) (r : Req) : Bool :=
  markOkB w m.1 m.2 && satB (markApply w m.1 m.2) r

def repairFamily (w : World) (r : Req) : List (View × Nat) :=
  (responseMenu w).filter (fun m => repairsB w m r)

def obstructedB (w : World) (r : Req) : Bool :=
  violB w r && (responseMenu w).all (fun m => !repairsB w m r)
```

```lean
-- Lean (Genesis), lean4/Derivation/Represented.lean lines 164-200, 228-237, 317-322, 332-335, 525-526, 571-573
inductive Event where
  | admitTok (tok : Nat)
  | require (i j : Nat)
  | mark (v : View) (p : Nat)
  | addView (c : View)
  | refuse (i j : Nat)
  | note (n : Nat)
  | setBudget (n : Nat)
  | setAugLicense (b : Bool)
deriving Repr, DecidableEq

def step (w : World) : Event → World
  | .admitTok t =>
      if t ∈ w.data then w else { w with data := w.data ++ [t] }
  | .require i j =>
      if reqOkB w i j then { w with reqs := w.reqs ++ [(i, j)] } else w
  | .mark v p =>
      if markOkB w v p && decide (0 < w.budget) then
        { markApply w v p with budget := w.budget - 1 }
      else w
  | .addView c =>
      if augOkB w c && w.augLicensed && decide (0 < w.budget) then
        { augApply w c with budget := w.budget - 1 }
      else w
  | .refuse i j =>
      if obstructedB w (i, j) && !(decide ((i, j) ∈ w.refusals)) then
        { w with refusals := w.refusals ++ [(i, j)] }
      else w
  | .note n => { w with notes := w.notes ++ [n] }
  | .setBudget n => { w with budget := n }
  | .setAugLicense b => { w with augLicensed := b }

def replay (h : List Event) (w : World) : World := h.foldl step w

def supp (w : World) : Supp :=
  ⟨w.data, w.views, w.reqs, w.refusals, w.budget, w.augLicensed⟩

theorem support_determines (w w' : World) (h : supp w = supp w')
    (e : Event) : supp (step w e) = supp (step w' e) := by
  cases w with
  | mk d v r f b a nt =>
    cases w' with
    | mk d' v' r' f' b' a' nt' =>
      simp only [supp, Supp.mk.injEq] at h
      obtain ⟨h1, h2, h3, h4, h5, h6⟩ := h
      subst h1; subst h2; subst h3; subst h4; subst h5; subst h6
      cases e with
      | admitTok t =>
          simp only [step]
          split <;> rfl
      -- the other seven events likewise: each guard is `rfl`-equal
      -- across the two worlds, then `split <;> rfl`

theorem repairFamily_retains_ties {w : World} {r : Req}
    {m m' : View × Nat}
    (hm : m ∈ responseMenu w) (hm' : m' ∈ responseMenu w)
    (h1 : repairsB w m r = true) (h2 : repairsB w m' r = true) :
    m ∈ repairFamily w r ∧ m' ∈ repairFamily w r :=
  ⟨repairFamily_complete hm h1, repairFamily_complete hm' h2⟩

def WEquiv (w w' : World) : Prop :=
  w.data = w'.data ∧ SameElems w.views w'.views ∧
    SameElems w.reqs w'.reqs ∧ SameElems w.refusals w'.refusals ∧
    w.budget = w'.budget ∧ w.augLicensed = w'.augLicensed

theorem equiv_step {w w' : World} (h : WEquiv w w') (e : Event) :
    WEquiv (step w e) (step w' e) := by
  obtain ⟨hd, hv, hr, hf, hb, ha⟩ := h
  cases e with
  -- eight cases, each through the congruence lemmas of lines 384-520

theorem equiv_replay {w w' : World} (h : WEquiv w w')
    (hist : List Event) : WEquiv (replay hist w) (replay hist w') := by
  induction hist generalizing w w' with
  | nil => exact h
  | cons e rest ih => exact ih (equiv_step h e)
```

```lean
-- Lean (Genesis), lean4/Derivation/Represented.lean lines 689-691, 762-769, 778-782, 806-860 (abridged), 868-870, 895-897, 966-968, 1013-1020, 1074-1080, 1107-1109, 1146-1148, 1176-1178, 1338-1340
def WF (w : World) : Prop :=
  ∀ r ∈ w.reqs, r.1 ≠ r.2 ∧ r.1 < w.data.length ∧
    r.2 < w.data.length

theorem wf_replay (h : List Event) : WF (replay h genesis) := by
  have : ∀ w, WF w → WF (replay h w) := by
    induction h with
    | nil => intro w hw; exact hw
    | cons e rest ih =>
        intro w hw
        exact ih _ (wf_step hw e)
  exact this genesis wf_genesis

theorem represented_progress {w : World} {i j : Nat} (hwf : WF w)
    (hviol : violB w (i, j) = true) :
    (∃ m, m ∈ repairFamily w (i, j)) ∨
      (obstructedB w (i, j) = true ∧ augOkB w [i] = true ∧
        satB (augApply w [i]) (i, j) = true) := by
  -- (i, j) is recorded and unsatisfied; WF gives i ≠ j and bounds;
  -- hsep : sepB [i] i j = true
  cases hfam : repairFamily w (i, j) with
  | cons m t => exact Or.inl ⟨m, List.mem_cons_self⟩
  | nil =>
      right
      have hallfail : ∀ m ∈ responseMenu w,
          repairsB w m (i, j) = false := by
        -- an accepted item would be in the family by repairFamily_complete
      have hobs : obstructedB w (i, j) = true := by
        unfold obstructedB; rw [hviol]; -- then `all` from hallfail
      have hfresh : ¬ ([i] ∈ w.views) := by
        -- if [i] were a view, satB w (i, j) would hold, against hnots
      have haug : augOkB w [i] = true := by
        -- bounded (hib), fresh (hfresh), increasing (i, j, hsep, hnots)
      refine ⟨hobs, haug, ?_⟩
      rw [satB_aug, hsep]
      simp

theorem progress_needs_budget (w : World) (v : View) (p : Nat)
    (h : w.budget = 0) : step w (.mark v p) = w := by

theorem violation_only_from_require {w : World} {e : Event} {r : Req}
    (h : violB (step w e) r = true) :
    violB w r = true ∨ ∃ i j, e = .require i j := by

theorem quiescent_stable {w : World} (hq : quiescentB w = true)
    {e : Event} (hnotreq : ∀ i j, e ≠ .require i j) :
    quiescentB (step w e) = true := by

def blockEvents (k : Nat) : List Event :=
  [.setBudget 1, .admitTok k, .require 0 k, .addView [k]]

def histUpTo : Nat → List Event
  | 0 => [.admitTok 0]
  | k + 1 => histUpTo k ++ blockEvents (k + 1)

def worldAt (k : Nat) : World := replay (histUpTo k) genesis

theorem productive_run (k : Nat) :
    histUpTo k <+: histUpTo (k + 1) ∧
      (worldAt k).data.length < (worldAt (k + 1)).data.length := by
  refine ⟨histUpTo_prefix k, ?_⟩
  rw [worldAt_growth, worldAt_growth]
  omega

theorem wit_no_infinite (g : Nat → Nat) :
    witValid (prefixList g (g 0 + 1)) = false := by

theorem cert_scope (panel : List Evaluator) (i j : Nat) :
    certPosB panel i j = true ↔
      panel ≠ [] ∧ ∀ E ∈ panel, ∃ c ∈ E, sepB c i j = true := by

theorem cert_not_correspondence :
    certNegB [[[0, 1]], [[0, 1]]] 0 1 = true ∧
      sepB [0] 0 1 = true := by decide

theorem refusal_needs_certificate {w : World} {i j : Nat}
    (h : step w (.refuse i j) ≠ w) :
    obstructedB w (i, j) = true := by
```

```lean
-- Lean (Genesis), lean4/Derivation/Represented.lean lines 1194-1212, 1245-1259, 1292-1320 (abridged)
def stepSched (ext : Bool) (w : World) (e : Event) : World :=
  match e with
  | .mark v p => if ext then step w (.mark v p) else w
  | _ => step w e

theorem scheduler_hidden :
    stepSched true schedWorld2 (.mark [] 0) ≠
      stepSched false schedWorld2 (.mark [] 0) := by decide

def obstructedTruncB (k : Nat) (w : World) (r : Req) : Bool :=
  violB w r && ((responseMenu w).take k).all (fun m => !repairsB w m r)

theorem incomplete_search_false_alarm :
    obstructedTruncB 1 truncWorld (1, 2) = true ∧
      obstructedB truncWorld (1, 2) = false ∧
      repairFamily truncWorld (1, 2) ≠ [] := by decide

def stepHead (w : World) (e : Event) : World :=
  match e with
  | .mark _ p =>
      { w with views :=
          match w.views with
          | [] => []
          | c :: rest => (p :: c) :: rest }
  | _ => step w e

theorem order_sensitivity_splits_equivalents :
    WEquiv headWorldA headWorldB ∧
      satB (stepHead headWorldA (.mark [] 1)) (0, 1) ≠
        satB (stepHead headWorldB (.mark [] 1)) (0, 1) := by
```

The book's Lean replays the paper's story, applies the progress theorem
to it, shows the two gates and the unguarded refill, generalizes
`notes_inert`, runs the kernel on the worlds the countermodels split,
and makes the panel examples concrete.

```lean
-- Lean (book), textbook/checks/u45_lean.py
def story : World :=
  replay [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
    .require 0 1, .require 0 2, .require 1 2, .addView [0]] genesis

theorem story_values :
    story.data = [10, 20, 30] ∧ story.views = [[0]] ∧
    story.reqs = [(0, 1), (0, 2), (1, 2)] ∧ story.budget = 8 ∧
    violB story (1, 2) = true ∧ repairFamily story (1, 2) = [] ∧
    obstructedB story (1, 2) = true ∧ augOkB story [1] = true ∧
    quiescentB (step story (.addView [1])) = true := by decide

theorem story_progress_instance :
    (∃ m, m ∈ repairFamily story (1, 2)) ∨
      (obstructedB story (1, 2) = true ∧ augOkB story [1] = true ∧
        satB (augApply story [1]) (1, 2) = true) :=
  represented_progress (wf_replay _) (by decide)

theorem story_right_branch :
    obstructedB story (1, 2) = true ∧ augOkB story [1] = true ∧
      satB (augApply story [1]) (1, 2) = true := by decide

theorem budget_gate_instance :
    step { story with budget := 0 } (.addView [1]) = { story with budget := 0 } := by decide

theorem budget_replenished_unguarded (w : World) (n : Nat) :
    (step w (.setBudget n)).budget = n := rfl

theorem license_gate_instance :
    step { story with augLicensed := false } (.addView [1]) =
      { story with augLicensed := false } :=
  progress_needs_license _ _ rfl

theorem refuse_instance :
    (step story (.refuse 1 2)).refusals = [(1, 2)] ∧
      step story (.refuse 0 1) = story := by decide

theorem notes_inert_general (w : World) (n : List Nat) (e : Event) :
    supp (step { w with notes := n } e) = supp (step w e) :=
  support_determines { w with notes := n } w rfl e

theorem kernel_ignores_order :
    satB (step headWorldA (.mark [] 1)) (0, 1) =
      satB (step headWorldB (.mark [] 1)) (0, 1) := by decide

theorem kernel_ignores_order_general :
    SameElems (repairFamily headWorldA (0, 1)) (repairFamily headWorldB (0, 1)) :=
  equiv_repairFamily order_sensitivity_splits_equivalents.1 (0, 1)

theorem trunc_family : repairFamily truncWorld (1, 2) = [([0], 1), ([0], 2)] := by decide

theorem repetition_data :
    (replay [.admitTok 5, .admitTok 5, .admitTok 5] genesis).data = [5] := by decide

theorem require_makes_violation :
    quiescentB (step story (.addView [1])) = true ∧
    quiescentB (step (step story (.addView [1])) (.admitTok 40)) = true ∧
    quiescentB (step (step (step story (.addView [1])) (.admitTok 40)) (.require 2 3)) = false := by
  decide

theorem wit_instances : witValid [3, 3, 3] = true ∧ witValid [0] = false := by decide

theorem wit_identity_fails : witValid (prefixList (fun n => n) 1) = false :=
  wit_no_infinite (fun n => n)

theorem panel_instances :
    certPosB [[[0]]] 0 1 = true ∧ certPosB [[[0]], [[0, 1]]] 0 1 = false ∧
    certPosB [[[0]], [[0], [0, 1]]] 0 1 = true ∧ certPosB [] 0 1 = false := by decide

theorem worldAt_two :
    (worldAt 2).data = [0, 1, 2] ∧ (worldAt 2).views = [[1], [2]] ∧
    (worldAt 2).reqs = [(0, 1), (0, 2)] ∧ quiescentB (worldAt 2) = true := by decide
```

## Line-by-line Lean explanation

**`World` and `genesis` (80-90).** `deriving DecidableEq` is what lets
every concrete statement below close by `decide`. `budget` and
`augLicensed` are policy fields: the module declares them, it does not
derive them.

**The laws (94-105).** `sepB` is exclusive-or of two memberships;
`satB` is `any` over views; `violB` conjoins recorded with not
satisfied; `quiescentB` is `all`. Everything is `Bool`, so the proofs
convert with `Bool.and_eq_true`, `List.any_eq_true`, `List.all_eq_true`.

**The guards (108-156).** `markApply` maps over all views and prepends
`p` to every view equal to `v`: the repair is identified by the column's
value, not its position in the list, which is what `equiv_step` needs
later. `markOkB` has five conjuncts, the last two computed on the
would-be successor. `increaseB` is a double `any` over `range`;
`augOkB` three conjuncts. `responseMenu` is a `flatMap` over views of a
`map` over positions, finite by construction; `repairFamily` filters
it; `obstructedB` is the violation together with `all` of the negated
test over the menu. The docstring says it: never lookalikeness.

**`Event`, `step`, `replay` (164-200).** The step's type is the
theorem of Target 1: `replay_deterministic` (208) is proved by `rw`,
and the docstring says this is the design point. Present it as a remark
on the type, not as content. `replay_append` (213) is `List.foldl_append`.

**`supp` and `support_determines` (228-290).** Both worlds are
destructured into seven fields; `Supp.mk.injEq` turns the hypothesis
into six equations; `subst` six times leaves two worlds differing only
in `notes`; then `cases e` and, for each event, the guard is shown
`rfl`-equal across the two worlds and `split <;> rfl` finishes. The
book's `notes_inert_general` is this theorem applied to `{w with notes
:= n}` and `w`, with `rfl` for the support equation, for every `w`, `n`
and `e`: the generality `notes_inert` (298) states for one instance.

**The repair family (305-322).** `List.mem_filter` both ways; ties kept
is two applications of completeness.

**`WEquiv` and the invariance theorems (329-590).** Data is compared
literally (position is identity); views, requirements and refusals by
membership. Seventeen congruence lemmas carry `SameElems` through
`any`, `all`, `map`, `flatMap`, and each guard; `equiv_step` is eight
cases over them; `equiv_replay` is induction on the history;
`equiv_repairFamily` membership-equality of the families. The book's
`kernel_ignores_order_general` applies it to the two worlds of the
seventh countermodel.

**Repair soundness (594-650).** `mark_discharges` and `mark_preserves`
unfold the fourth and fifth conjuncts of `markOkB`. `step_mark_sound`
first shows the guard, together with the budget test, is `true`, so
`step` reduces to the applied mark with the budget decremented, and
that `satB` ignores the budget; then it is the two lemmas.

**Augmentation soundness (652-688).** `satB_aug` is `List.any_append`:
the verdict after is the old verdict or the new column's. `aug_increases`
unpacks `increaseB` into a witness pair with `bne_iff_ne`.

**`WF` and `wf_replay` (689-769).** Off-diagonal and bounded, for every
recorded pair; `wf_step` is eight cases (an `admitTok` only lengthens
`data`; a `require` passes `reqOkB`); `wf_replay` is induction
generalized over the start world.

**`represented_progress` (778-860).** From `violB` take membership and
`satB = false`; from `WF` take `i ≠ j` and the bounds; show `[i]`
separates `i` from `j` (membership in a singleton). Case on the family:
non-empty gives the left disjunct with the head. Empty: every menu item
fails, else completeness would put it in the family; so `obstructedB`
holds (`all` of the negations); `[i]` is not a view, else `(i, j)` would
be satisfied; `augOkB w [i]` is bounded, fresh and increasing with the
witness `(i, j)`; finally `satB_aug` with `hsep`. The orientation of
`[i]` comes from the recorded ordered pair, which the header calls a
represented datum and a stated scoping, not a selector. The book's
`story_progress_instance` discharges `WF` by `wf_replay` because
`story` is a replay from genesis.

**The gates (868-893).** Each unfolds `step`, takes the `if_neg` branch
and derives the contradiction from the field being 0 or `false`. The
book's `budget_replenished_unguarded` is `rfl`: `setBudget` writes the
field. That is the audit's point about "never free".

**Closure (895-1010).** `violation_only_from_require` is eight cases:
a `require` is the right disjunct; a `mark` that fired would have
preserved the requirement (`mark_preserves`), so the violation was
already there; an `addView` by `satB_aug`; the rest leave requirements
and views unchanged. `quiescent_stable` uses it: a new violation after a
non-`require` event was an old one, against quiescence. The book's
`require_makes_violation` shows the one way in: admit a fourth token,
require `(2, 3)`, and nothing separates them.

**Productivity (1013-1086).** `histUpTo` is a supplied stream, named
metatheoretic in the docstring; `blockEvents` refills the budget at
every stage. `worldAt_data` is induction with `List.range_succ`;
`productive_run` is the prefix fact plus `omega` on the lengths;
`worldAt_three_quiescent` is one `decide`. The book's `worldAt_two`
shows the stage: views `[1]`, `[2]`, requirements `(0, 1)`, `(0, 2)`,
quiescent.

**Countermodel 8 (1090-1128).** `witValid l` says every entry is at
least the length. `wit_all_lengths`: `replicate n n` passes, so a
witness exists at every length. `wit_no_infinite`: for any `g`, the
prefix of length `g 0 + 1` contains `g 0`, which is below the length,
so it fails. The quantifier is over Lean functions; the kernel carries
no `g`. The book's instances: `[3, 3, 3]` passes, `[0]` fails, and the
identity fails already at length 1.

**Certification (1130-1192).** An evaluator is a list of columns;
`certPosB` needs a non-empty panel and unanimity. `cert_scope`
rewrites `all` and `any` into the stated iff. `cert_not_correspondence`:
two evaluators that only have `[0, 1]` certify `0` and `1` equivalent,
and `[0]` separates them. `cert_panel_relative`: adding a blind
evaluator turns a positive certificate off. The book's
`panel_instances` adds the repair (give the blind evaluator the column)
and the empty panel.

**Countermodels 1-7 (1194-1336).** Each is a different `step`
consuming one extra input (`ext`, `seed`, `oracle`, `k`, a destructive
rewrite, repetition read as progress, list position), with a concrete
world and a `decide`. `schedWorld` (1199) is a dead first attempt, as
its docstring says; `schedWorld2` is used. `order_sensitivity_splits_equivalents`
proves `WEquiv` by hand (two-element lists, membership both ways) and
the split by `decide`; the book runs the kernel's `step` on the same
two worlds and gets equal verdicts.

**Refusal (1338-1362).** If a `refuse` event changed the world, the
guard held, so `obstructedB` held; and after the event the pair is
recorded or nothing happened. The book's `refuse_instance`: `(1, 2)` is
recorded, `(0, 1)` is not, being satisfied.

## What has been proved

- Relative to the declared constitution: the step factors through the
  support; replay-equivalent worlds stay equivalent under every history
  and have membership-equal repair families; ties are kept (Genesis).
- Accepted mark repairs discharge a violation and preserve previously
  satisfied recorded requirements; accepted augmentations are
  conservative on satisfied requirements and add capacity (Genesis).
- On well-formed worlds, which include every replay from genesis, a
  violation has a repair or is a certified obstruction with an accepted
  augmentation passing the structural guard that would discharge it under
  `augApply` (Genesis; applied to the
  story in the book).
- Budget and license gate the applying step; violations come only from
  `require`; a supplied stream gives a prefix-compatible unbounded run;
  refusal needs the certificate and ends nothing (Genesis).
- Certification by a panel is exactly the panel's joint separation and
  is not correspondence (Genesis; the book adds the repair of a broken
  panel).
- Eight countermodels each fail the matching theorem, as decided
  instances (Genesis); the kernel itself does not split the worlds the
  order-sensitive semantics splits (book).

## What has not been proved

- That the constitution derives itself, or that the kernel is unique or
  canonical among kernels satisfying the eight targets.
- Any bound on how often `setBudget` refills the budget: the gate is
  real per step and replenishable per run.
- That `[i]` is the only augmentation; no-hidden-choice is scoped to
  the repair family.
- Minimality of the countermodels.
- Anything about the Python exhaustive check beyond `k = 3` in Lean.
- That the per-length witnesses say anything about an object the kernel
  represents: `wit_no_infinite` quantifies over Lean functions.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `World`, `Event`, `sepB`, `satB`, `responseMenu`, the guards | the constitution | declared metatheory, named as such in the header and the paper |
| `budget : Nat`, `augLicensed : Bool`, `setBudget`, `setAugLicense` | policy fields and their unguarded writes | declared; replenishable |
| `histUpTo : Nat → List Event` | the productive run | supplied stream; the finitude rule flags the unbounded producer |
| `g : Nat → Nat` in `wit_no_infinite` | the eighth countermodel | metatheory; not represented |
| `List`, `Nat`, `decide`, `omega` | computation | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The runtime inputs: tokens arrive as events,
requirements are recorded, the budget and license are fields, the
tie-break is absent (a filter), the fresh name is the event's own
content, refusal is a recorded certificate. The theorems are about this
and say so.

**Phrases to read with care.**

- "No hidden input reaches a transition": relative to the fixed
  constitution; the constitution is the outside that remains.
- "Progress is never free": per step; the stream refills the budget
  with an unguarded event.
- "The represented König failure": the failure is metatheoretic; what
  is represented is each finite witness.
- "Certification": the panel's joint quotient, never agreement with an
  outside column.

## Student exercise

Take the story world after `addView [1]` (data `[10, 20, 30]`, views
`[[0], [1]]`, three satisfied requirements, budget 7). Admit a fourth
token and require `(2, 3)`. List the response menu, decide the repair
family of `(2, 3)`, and say which branch of `represented_progress`
applies and what the kernel does next if the stream sends `addView [2]`
and then `refuse 2 3`.

## Answer

<details>
<summary>Worked answer</summary>

After `admitTok 40` the data is `[10, 20, 30, 40]`; `require 2 3`
passes `reqOkB` (distinct, in bounds, new), so the world has four
recorded pairs, three satisfied and `(2, 3)` violated. The menu is every
(view, position) pair: `([0], p)` and `([1], p)` for `p = 0..3`, eight
items. Four of them make `(2, 3)` satisfied: marking 2 or 3 on either
column. Two of those are rejected by `preservesB`: `([0], 2)` turns
`[0]` into `[2, 0]`, and then nothing separates `0` from `2`;
`([1], 2)` turns `[1]` into `[2, 1]`, and then nothing separates `1`
from `2`. The other two are accepted: `([0], 3)` gives `[3, 0]` and
`([1], 3)` gives `[3, 1]`, each separating `3` from `2` while `[0]` or
`[1]` still separates the old pairs. So the repair family is
`[([0], 3), ([1], 3)]`, both ties kept, the left branch of
`represented_progress` applies, and the pair is not obstructed. If the
stream sends `addView [2]` anyway, it is accepted (`[2]` is in bounds,
new, and separates `(2, 3)`, which no view did), costs one budget
(7 to 6) and leaves the world quiescent. `refuse 2 3` is then a no-op:
the pair is satisfied, so `obstructedB` is false, and
`refusal_needs_certificate` says the step changes nothing. The check
script's mirror confirms each line.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Represented.lean` lines 70-156 (world, laws, guards, menu), 164-215 (events, step, replay), 219-322 (support, repair family), 329-590 (equivalence), 594-688 (soundness), 689-769 (`WF`), 778-893 (progress, gates), 895-1010 (closure), 1013-1128 (productivity, countermodel 8), 1130-1192 (certification), 1194-1336 (countermodels 1-7), 1338-1362 (refusal) |
| Axiom report | `artifacts/lean_axioms.txt` lines 211-258: `wf_genesis`, `histUpTo_prefix` none; `bool_eq_of_iff`, `or_not_eq_true` `propext`; 44 `{propext, Quot.sound}` |
| Paper | `paper/represented_progress.md` (TERMINAL, the required definitions, the eight targets, the internal candidate for truth, the countermodels split by class, the exact ceiling); `paper/paper_claim_ledger.md` `CL-RP-TERMINAL` through `CL-RP-CEILING` |
| Python | `code/derivation/represented.py`, `artifacts/represented.json`, `tests/test_represented.py` |
| Check (Python) | `python textbook/checks/u45_represented.py`: the story, the gates and the refill, refusal, the run to 15 stages, the countermodels with the kernel beside them, certification, witnesses, mutation, all against the artifact |
| Check (book Lean) | `python textbook/checks/u45_lean.py`: nineteen book reports plus seventeen Genesis theorems kernel-checked, Lean 4.33.0 |
