# Unit 50. Proving the shape of every completed tower stage

**Claim.** Induction identifies the full state at every completed tower stage
and proves it well formed and quiescent. Intermediate event prefixes
can have an unmet requirement. The proof concerns this driver and
construction, indexed by Lean natural numbers.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** `Horizon` writes down the complete record of the generated
world at stage `k` (`specWorld k`: carrier `0..k`, one singleton column
`[i+1]` and one requirement `(0, i+1)` per earlier stage, no refusals,
budget spent to zero, licensed) and proves by induction that the supplied
run equals it at every stage (`worldAt_spec`).

From the characterisation
it reads off quiescence (`worldAt_quiescent`), well-formedness
(`worldAt_wf`) and the acceptance of each of the four events of every
block (`block_all_accepted`, `genesis_accepted`), and lifts the first two
to the driver's generated run (`gen_quiescent`, `gen_wf`) through Unit
48's `driver_reproduces_tower`.

A second theorem pins the budget
semantics shared with the Python mirror: for every descriptor and every
event the family interpreter leaves the budget alone, applies the
saturating `Nat` decrement, or sets it by an explicit `setBudget`
(`interp_budget_bound`). The audit's particular zero-budget mark is a
no-op in Lean for all 64 descriptors: it targets a column absent from
the store, and subtraction saturates. This is not a general claim that
zero budget blocks a descriptor whose budget gate is off.

**Status:** FROZEN (the
every-stage theorems), VERIFIED_FINITE (the two saturation instances);
correction module of the second review (C6 repaired upward, C10
repaired). **Lean:** `lean4/Derivation/Horizon.lean` lines 45-422,
imports `Initiality`. **Axioms:** all ten exported theorems `{propext,
Quot.sound}`. **Depends on:** Unit 45 (`histUpTo`, `worldAt`,
`blockEvents`, `worldAt_three_quiescent`, `WF`), Unit 48 (`towerGen`,
`genWorld`, `driver_reproduces_tower`, `interpStep`), Unit 49 (the probe
worlds, reused for the budget pin).

</details>

## First pass

Stage 0 has just position 0 and no requirements. To reach stage 1,
the tower performs four events:

| After this event | Budget | Requirement 0/1 |
|---|---|---|
| Set budget to 1 | 1 | Not recorded |
| Admit position 1 | 1 | Not recorded |
| Require 0/1 | 1 | Recorded and unmet |
| Add a column saying Yes only on 1 | 0 | Met |

The completed stage is quiescent. The moment after the third event is
not. “Every stage” refers to completed blocks, not every prefix of the
event history.

At stage k, positions run from 0 through k. Each positive position has
its own singleton column and a requirement to distinguish it from 0.
The proof checks this description at stage 0, then proves that the
four-event block carries it from any stage k to stage k+1. This is
induction; checking stages 3, 10, or 100 alone would not suffice.

**Predict:** does this prove that every process can keep growing while
meeting its requirements?

<details>
<summary>Check your prediction</summary>

No. The proof uses this exact state formula and block. Its external
iteration and explicit budget-replenishing event are assumptions of the
construction, not an empirical guarantee about other systems.

</details>

## Question

Unit 45 proved the generated world quiescent at stage 3, by running it.
The claim ledger said "lawful across extension". How does one turn an
instance check into a theorem at every stage, and what exactly does
"every stage" quantify over?

## What we already possess

- The supplied stream: `histUpTo 0 = [admitTok 0]`, `histUpTo (k+1) =
  histUpTo k ++ blockEvents (k+1)`, with `blockEvents k = [setBudget 1,
  admitTok k, require 0 k, addView [k]]`; `worldAt k = replay (histUpTo
  k) genesis` (Unit 45).
- `quiescentB`, `WF`, `sepB`, `satB`, `reqOkB`, `augOkB`, `increaseB`,
  and the sealed `step` with its guards (Unit 45).
- The driver `towerGen` and `driver_reproduces_tower : towerGen k =
  histUpTo k` (Unit 48); the family interpreter `interpStep` and the
  probe worlds (Units 48, 49).

## New concept: a closed-form record, then an induction

The method has two halves. First, *say what the state is*, for every
`k`, as a term with `k` free: `specWorld k`. Second, prove `worldAt k =
specWorld k` by induction on `k`: at `0`, run it (`decide`); at `k+1`,
unfold the block into four steps and show each guard passes on the
characterised state, so each step lands on a named intermediate (`w1`,
`w2`, `w3`) and the last lands on `specWorld (k+1)`. Every later
property can be proved from `specWorld k` and transferred to the
specified run using that equality, without executing each stage.

The second concept is a *cross-language pin*: a Lean theorem that states
the arithmetic the Python mirror is meant to implement. Separate
Python checks compare that implementation with the intended behavior;
the Lean theorem alone does not verify the Python program.

## Plain-language interpretation

A run can be checked at stage 3 by turning the handle three times. It
cannot be checked at every stage that way. What `Horizon` does instead is
guess the shape of the state after `k` turns, in full, and then prove
the guess right by showing that one more turn preserves it. After that,
"is it quiescent at stage 1 000 000" is answered by looking at the shape,
not by turning the handle.

Two cautions, both from the audit. "Accepted" here means "the guard
passed". The theorem proves each event *changes the state*, which
certifies acceptance because every rejecting branch of `step` returns
the state unchanged. The converse is false: `setBudget 0` on a world at
budget 0 is accepted and changes nothing. And "every stage" means every
Lean natural number `k`. The run itself is a metatheoretic stream,
indexed from outside; the system holds no object called "the run at
every horizon". That is the finitude flag of Unit 45, carried forward.

The budget pin records a real defect found by review: the Python mirror
once computed `budget - 1` on integers, so a descriptor with the budget
gate switched off reached budget `-1` at budget zero, a state Lean's
`Nat` cannot hold. Lean's subtraction saturates. The theorem
`interp_budget_bound` states the only three things the budget can do
after any event, and the mirror now does the same.

## Pseudocode

```
specWorld k = { data = [0..k], views = [[1],...,[k]], reqs = [(0,1),...,(0,k)],
                refusals = [], budget = 0, licensed }
prove worldAt k = specWorld k by induction:
  k = 0: compute
  k+1:   specWorld k --setBudget 1--> w1 k --admitTok (k+1)--> w2 k
                     --require 0 (k+1)--> w3 k --addView [k+1]--> specWorld (k+1)
         each arrow: show the guard passes (fresh token; (0,k+1) not yet a
         requirement; old columns blind to it; new column separates it; budget 1)
then: quiescent, WF, each arrow changes the state  -- all read off specWorld
lift: genWorld k = replay (towerGen k) = replay (histUpTo k) = worldAt k
pin: for all d w e: budget' = budget | budget' = budget - 1 (Nat) | e = setBudget n ∧ budget' = n
```

## Python

Genesis's `code/derivation/represented.py` holds the stream
(`block_events`, `hist_up_to`), `events_all_accepted` and
`productivity_report`, whose output is the `productivity` key of
`artifacts/represented.json`; `code/derivation/completion.py::interp_step`
is the mirror with the saturating decrement. `specWorld` has no Genesis
Python; the check writes it as Python (book):

```python
def spec_world(k: int) -> R.World:
    return R.World(data=tuple(range(k + 1)),
                   views=tuple((i + 1,) for i in range(k)),
                   reqs=tuple((0, i + 1) for i in range(k)),
                   refusals=(), budget=0, aug_licensed=True, notes=())
```

The check's run:

```text
the generated world against its specification, stage by stage:
  k=0: worldAt = specWorld True; data [0], views [], reqs [], budget 0; quiescent True, wf True, all events accepted True
  k=1: worldAt = specWorld True; data [0, 1], views [[1]], reqs [[0, 1]], budget 0; quiescent True, wf True, all events accepted True
  k=2: worldAt = specWorld True; data [0, 1, 2], views [[1], [2]], reqs [[0, 1], [0, 2]], budget 0; quiescent True, wf True, all events accepted True
  k=3: worldAt = specWorld True; data [0, 1, 2, 3], views [[1], [2], [3]], reqs [[0, 1], [0, 2], [0, 3]], budget 0; quiescent True, wf True, all events accepted True
  k=4: worldAt = specWorld True; data [0, 1, 2, 3, 4], views [[1], [2], [3], [4]], reqs [[0, 1], [0, 2], [0, 3], [0, 4]], budget 0; quiescent True, wf True, all events accepted True
  k=15: worldAt = specWorld True; data [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], views [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15]], reqs [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], [0, 14], [0, 15]], budget 0; quiescent True, wf True, all events accepted True
block k+1 from stage k: each of the four events changes the state and the block lands on stage k+1:
  k=0: setBudget -> w1 True, admit -> w2 True, require -> w3 True, addView -> specWorld True; each changed True
  k=1: setBudget -> w1 True, admit -> w2 True, require -> w3 True, addView -> specWorld True; each changed True
  k=2: setBudget -> w1 True, admit -> w2 True, require -> w3 True, addView -> specWorld True; each changed True
  genesis accepted: step genesis (admit 0) = [0] != genesis True
  an unguarded event can change nothing: step genesis (setBudget 0) == genesis True (so 'changed' certifies 'accepted', not the converse)
the guards at every stage (old columns blind, the new column separates):
  m=0: old columns blind True, new column separates True, reqOk True, new req unsatisfied in w3 True, increase True, full addView guard True
  m=1: old columns blind True, new column separates True, reqOk True, new req unsatisfied in w3 True, increase True, full addView guard True
  m=2: old columns blind True, new column separates True, reqOk True, new req unsatisfied in w3 True, increase True, full addView guard True
  m=3: old columns blind True, new column separates True, reqOk True, new req unsatisfied in w3 True, increase True, full addView guard True
  m=4: old columns blind True, new column separates True, reqOk True, new req unsatisfied in w3 True, increase True, full addView guard True
  m=5: old columns blind True, new column separates True, reqOk True, new req unsatisfied in w3 True, increase True, full addView guard True
lifted to the driver:
  k=0: towerGen = histUpTo True, quiescent True, wf True
  k=3: towerGen = histUpTo True, quiescent True, wf True
  k=10: towerGen = histUpTo True, quiescent True, wf True
  k=15: towerGen = histUpTo True, quiescent True, wf True
  productivity_report(15) equals the artifact: True; rows 16, all_quiescent True, all_events_accepted True
the budget pin on all 64 descriptors:
  7168 (descriptor, world, event) triples: unchanged 5840, saturating decrement 816, set 512; negative budgets 0
  the audit countermodel: mark (1,) 0 at budget 0 is a no-op for all 64 True; for the audit descriptor True
  the arithmetic: Python 0 - 1 = -1; max(0, 0 - 1) = 0; Lean Nat 0 - 1 = 0
  markApply off the view store: views [[0]] unchanged True
failures: []
```

## Line-by-line Python explanation

`spec_world` builds the closed form; the first block compares it with
`replay(hist_up_to(k))` for `k` up to 15 and checks quiescence,
well-formedness and that every event on the stream changed the state.
This is the instance check at sixteen stages, not the theorem; the
theorem is the Lean induction.

The second block walks one block from `spec_world(k)` through the three
intermediates `w1`, `w2`, `w3` (Python (book), mirroring Lean's) and
confirms each step lands where the Lean proof says and changes the
state. Then the two cautions: `admit 0` on genesis changes it;
`setBudget 0` on genesis does not, though no guard refused it.

The third block checks the six guard facts the induction step rests on,
for `m` up to 5: every old column `[i+1]` with `i < m` contains neither
`0` nor `m+1`, so it is blind to the new requirement; the new column
`[m+1]` separates it; `reqOk` holds on `w2`; the new requirement is
unsatisfied on `w3` (so the new column is an increase); the full
`addView` guard passes.

The fourth block lifts through the driver and compares
`productivity_report(15)` with the artifact. The last block runs the
budget pin: on 64 descriptors, 8 worlds and 14 events, every outcome is
one of the three cases and none is negative; the audit countermodel is
a no-op for all 64; the integer arithmetic that caused the defect is
printed beside the saturating form; and `mark_apply` on a column not in
the store leaves the views alone, which is why the countermodel is a
no-op rather than a changed world at budget 0.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Horizon.lean lines 45-74
def specViews (k : Nat) : List View :=
  (List.range k).map (fun i => [i + 1])

def specReqs (k : Nat) : List (Nat × Nat) :=
  (List.range k).map (fun i => (0, i + 1))

def specWorld (k : Nat) : World :=
  { data := List.range (k + 1), views := specViews k,
    reqs := specReqs k, refusals := [], budget := 0,
    augLicensed := true, notes := [] }

def w1 (m : Nat) : World :=
  { data := List.range (m + 1), views := specViews m,
    reqs := specReqs m, refusals := [], budget := 1,
    augLicensed := true, notes := [] }

def w2 (m : Nat) : World :=
  { data := List.range (m + 1) ++ [m + 1], views := specViews m,
    reqs := specReqs m, refusals := [], budget := 1,
    augLicensed := true, notes := [] }

def w3 (m : Nat) : World :=
  { data := List.range (m + 1) ++ [m + 1], views := specViews m,
    reqs := specReqs m ++ [(0, m + 1)], refusals := [], budget := 1,
    augLicensed := true, notes := [] }
```

```lean
-- Lean (Genesis), lean4/Derivation/Horizon.lean lines 118-140 (two of the sixteen helpers)
theorem sep_new_col (m : Nat) : sepB [m + 1] 0 (m + 1) = true := by
  unfold sepB
  rw [decide_eq_false (by
        intro h
        cases List.mem_singleton.mp h),
      decide_eq_true (List.mem_singleton.mpr rfl)]
  rfl

theorem old_cols_blind (m : Nat) {c : View} (hc : c ∈ specViews m) :
    sepB c 0 (m + 1) = false := by
  obtain ⟨i, hi, heq⟩ := List.mem_map.mp hc
  have h3 : i < m := List.mem_range.mp hi
  subst heq
  unfold sepB
  rw [decide_eq_false (by
        intro h
        cases List.mem_singleton.mp h),
      decide_eq_false (by
        intro h
        have := List.mem_singleton.mp h
        omega)]
  rfl
```

```lean
-- Lean (Genesis), lean4/Derivation/Horizon.lean lines 236-254, 261-271, 294-304, 351-355
theorem worldAt_spec (k : Nat) : worldAt k = specWorld k := by
  induction k with
  | zero => decide
  | succ m ih =>
      have h0 : worldAt (m + 1)
          = replay (blockEvents (m + 1)) (worldAt m) := by
        show replay (histUpTo m ++ blockEvents (m + 1)) genesis = _
        rw [replay_append]
        rfl
      rw [h0, ih]
      show step (step (step (step (specWorld m) (.setBudget 1))
        (.admitTok (m + 1))) (.require 0 (m + 1))) (.addView [m + 1])
        = specWorld (m + 1)
      rw [show step (specWorld m) (.setBudget 1) = w1 m from rfl]
      rw [show step (w1 m) (.admitTok (m + 1)) = w2 m from by
        rw [step_admit_fresh (fresh_not_mem m)]; rfl]
      rw [show step (w2 m) (.require 0 (m + 1)) = w3 m from by
        rw [step_require_ok (req_guard m)]; rfl]
      rw [step_addView_ok (aug_guard m), final_assembly m]

theorem worldAt_quiescent (k : Nat) :
    quiescentB (worldAt k) = true := by
  rw [worldAt_spec]
  show (specReqs k).all (fun r => satB (specWorld k) r) = true
  apply List.all_eq_true.mpr
  intro r hr
  obtain ⟨i, hi, heq⟩ := List.mem_map.mp hr
  subst heq
  show (specViews k).any (fun c => sepB c 0 (i + 1)) = true
  apply List.any_eq_true.mpr
  exact ⟨[i + 1], List.mem_map.mpr ⟨i, hi, rfl⟩, sep_new_col i⟩

theorem block_all_accepted (k : Nat) :
    step (worldAt k) (.setBudget 1) ≠ worldAt k ∧
    step (w1 k) (.admitTok (k + 1)) ≠ w1 k ∧
    step (w2 k) (.require 0 (k + 1)) ≠ w2 k ∧
    step (w3 k) (.addView [k + 1]) ≠ w3 k ∧
    step (w3 k) (.addView [k + 1]) = worldAt (k + 1) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [worldAt_spec]
    intro h
    have hb : (1 : Nat) = 0 := congrArg World.budget h
    cases hb
  -- the other four cases compare a length before and after, lines 305-339

theorem gen_quiescent (k : Nat) :
    quiescentB (genWorld k).w = true := by
  show quiescentB (replay (towerGen k) genesis) = true
  rw [driver_reproduces_tower]
  exact worldAt_quiescent k
```

```lean
-- Lean (Genesis), lean4/Derivation/Horizon.lean lines 371-398, 402-404, 411-414
theorem interp_budget_bound (d : ConstitutionDesc) (w : World)
    (e : Event) :
    (interpStep d w e).budget = w.budget ∨
      (interpStep d w e).budget = w.budget - 1 ∨
      ∃ n, e = .setBudget n ∧ (interpStep d w e).budget = n := by
  cases e with
  | admitTok t =>
      simp only [interpStep]
      split <;> exact Or.inl rfl
  | require i j =>
      simp only [interpStep]
      split <;> exact Or.inl rfl
  | mark v p =>
      simp only [interpStep]
      split
      · exact Or.inr (Or.inl rfl)
      · exact Or.inl rfl
  | addView c =>
      simp only [interpStep]
      split
      · exact Or.inr (Or.inl rfl)
      · exact Or.inl rfl
  | refuse i j =>
      simp only [interpStep]
      split <;> exact Or.inl rfl
  | note n => exact Or.inl rfl
  | setBudget n => exact Or.inr (Or.inr ⟨n, rfl, rfl⟩)
  | setAugLicense b => exact Or.inl rfl

def satNoopWorld : World :=
  { data := [10, 20], views := [[0]], reqs := [(0, 1)],
    refusals := [], budget := 0, augLicensed := true, notes := [] }

theorem budget_saturation_noop :
    interpStep
      { kernelDesc with guardAccept := false, gateBudget := false }
      satNoopWorld (.mark [1] 0) = satNoopWorld := by decide
```

The book's Lean writes stage 3 out and reaches it both ways (by the
theorem and by computation), walks block 3 through the intermediates,
instantiates the helpers and the every-stage theorems at stages no
`decide` would reach cheaply, reads the carrier size off the
specification, shows the two cautions, and takes instances of the pin.

```lean
-- Lean (book), textbook/checks/u50_lean.py
theorem spec_three :
    specWorld 3 = ⟨[0, 1, 2, 3], [[1], [2], [3]], [(0, 1), (0, 2), (0, 3)], [], 0, true, []⟩ := by
  decide

theorem worldAt_three_by_spec : worldAt 3 = specWorld 3 := worldAt_spec 3

theorem worldAt_three_by_computation :
    worldAt 3 = ⟨[0, 1, 2, 3], [[1], [2], [3]], [(0, 1), (0, 2), (0, 3)], [], 0, true, []⟩ := by
  decide

theorem block_three_steps :
    step (specWorld 2) (.setBudget 1) = w1 2 ∧
    step (w1 2) (.admitTok 3) = w2 2 ∧
    step (w2 2) (.require 0 3) = w3 2 ∧
    step (w3 2) (.addView [3]) = specWorld 3 := by decide

theorem columns_at_two :
    sepB [1] 0 3 = false ∧ sepB [2] 0 3 = false ∧ sepB [3] 0 3 = true := by decide

theorem old_cols_blind_instance : sepB [2] 0 3 = false :=
  old_cols_blind 2 (by decide)

theorem stage_ten_quiescent : quiescentB (worldAt 10) = true := worldAt_quiescent 10
theorem stage_hundred_wf : WF (worldAt 100) := worldAt_wf 100
theorem gen_hundred_quiescent : quiescentB (genWorld 100).w = true := gen_quiescent 100

theorem block_three_accepted : step (w3 3) (.addView [4]) = worldAt 4 :=
  (block_all_accepted 3).2.2.2.2

theorem carrier_size (k : Nat) : (worldAt k).data.length = k + 1 := by
  rw [worldAt_spec]
  show (List.range (k + 1)).length = k + 1
  exact List.length_range

theorem genesis_first_step : step genesis (.admitTok 0) = ⟨[0], [], [], [], 0, true, []⟩ := by
  decide

theorem unguarded_can_be_silent : step genesis (.setBudget 0) = genesis := by decide

theorem nat_sub_saturates : (0 : Nat) - 1 = 0 := by decide

theorem budget_instances :
    (interpStep kernelDesc satNoopWorld (.mark [1] 0)).budget = 0 ∧
    (interpStep { kernelDesc with guardAccept := false, gateBudget := false }
      satNoopWorld (.mark [1] 0)).budget = 0 ∧
    (interpStep { kernelDesc with gateBudget := false } brokeWorld (.mark [] 0)).budget = 0 ∧
    (interpStep kernelDesc satWorld (.mark [0] 1)).budget = 9 ∧
    (interpStep kernelDesc satWorld (.setBudget 4)).budget = 4 := by decide

theorem trichotomy_instance (d : ConstitutionDesc) :
    (interpStep d brokeWorld (.mark [] 0)).budget = 0 := by
  rcases interp_budget_bound d brokeWorld (.mark [] 0) with h | h | ⟨n, hn, _⟩
  · rw [h]; rfl
  · rw [h]; rfl
  · cases hn

theorem relaxed_acts_on_present_view :
    interpStep { kernelDesc with guardAccept := false, gateBudget := false }
      satNoopWorld (.mark [0] 1) ≠ satNoopWorld := by decide
```

## Checked scope examples (optional)

These additional Lean (book) checks make the scope distinctions
above explicit. Their exact axiom reports stay within the existing
`{propext, Quot.sound}` boundary.

```lean
theorem completed_not_every_prefix :
    quiescentB (specWorld 2) = true ∧ quiescentB (w3 2) = false ∧
    quiescentB (specWorld 3) = true := by decide
```

## Line-by-line Lean explanation

**The specification (45-74).** `specViews k` maps `i ↦ [i+1]` over
`range k`; `specReqs k` maps `i ↦ (0, i+1)`; `specWorld k` assembles
them with carrier `range (k+1)`, budget `0`, licensed. `w1`, `w2`, `w3`
are the three states inside block `m+1`: budget replenished, fresh
token appended, requirement appended. The book's `spec_three` evaluates
the closed form at 3 and `worldAt_three_by_computation` runs the stream;
`worldAt_three_by_spec` connects them through the theorem.

**The helpers (76-232).** `specViews_succ`, `specReqs_succ` peel one
element off the end. `fresh_not_mem`: `m+1 ∉ range (m+1)`.
`req_not_mem`, `view_not_mem`: the new requirement and the new column
are not yet present, both by `mem_map` then `omega`. `sep_new_col`:
`[m+1]` contains `m+1` and not `0`, so it separates `(0, m+1)`;
`old_cols_blind`: a column `[i+1]` with `i < m` contains neither, so it
does not. The three `step_*_ok` lemmas unfold one branch of `step` under
a hypothesis that its guard holds. `req_guard`, `satB_w3_false`,
`increase_guard`, `aug_guard` establish the guards on the named
intermediates: the new requirement is unsatisfied on `w3` because every
column there is old and blind, so the new column is an increase, so
`augOkB` holds; the license is set and the budget is 1.
`final_assembly` shows applying the column to `w3 m` and spending the
budget is `specWorld (m+1)`, by rewriting the three `_succ` lemmas
backwards. The book's `columns_at_two` and `old_cols_blind_instance`
are these facts at `m = 2`.

**`worldAt_spec` (236-254).** Induction. Base: `decide`. Step: `h0`
splits the history with `replay_append`; `ih` replaces `worldAt m` by
`specWorld m`; the `show` writes the block as four nested steps; four
rewrites, each justified by a `step_*_ok` lemma and a guard, walk
through `w1`, `w2`, `w3`; `final_assembly` closes. The book's
`block_three_steps` is this walk at `m = 2`, decided.

**Reading properties off the form (261-288).** `worldAt_quiescent`:
after `rw [worldAt_spec]` the goal is `all` over `specReqs k`; each
requirement is `(0, i+1)` for some `i < k`, and the column `[i+1]` is in
`specViews k` and separates it, by `sep_new_col i`. `worldAt_wf`: each
`(0, i+1)` is off-diagonal and in bounds since the carrier has `k+1`
elements. The book's `stage_ten_quiescent`, `stage_hundred_wf` and
`gen_hundred_quiescent` are instances at stages where running would be
expensive; `carrier_size` reads the carrier length off the form.

**`block_all_accepted` (294-339).** Five conjuncts. The first: if
`setBudget 1` left the state fixed, the budgets `1` and `0` would be
equal. The next three compare a length (data, requirements, views)
before and after; `omega` closes. The fifth is the walk again. The book's
`block_three_accepted` takes the fifth conjunct at `k = 3`.
`genesis_accepted` (343) is the first event, decided; the book writes
out what it produces.

**The lift (351-361).** `genWorld k` is `replay (towerGen k) genesis`;
rewrite with `driver_reproduces_tower` and apply the every-stage
theorem.

**The pin (371-422).** `interp_budget_bound` cases on the event. The
admission, requirement and refusal branches never touch the budget
(`Or.inl rfl` after `split`); `mark` and `addView` either apply the
decrement or do nothing; `setBudget n` is the third case; `note` and
`setAugLicense` do nothing. The subtraction is `Nat` subtraction, so
`0 - 1 = 0` (`nat_sub_saturates`). The book's `trichotomy_instance`
takes the theorem at `brokeWorld` and `mark [] 0` for an arbitrary
descriptor: the budget is 0 in the first two cases and the third is
impossible. `budget_saturation_noop` and `mark_saturation_all_descs` are
the audit's countermodel decided for one and for all descriptors;
`relaxed_acts_on_present_view` shows the same relaxed descriptor is not
inert in general, so the no-op is the decrement saturating and
`markApply` missing the store, not the guard.

## What has been proved

- `worldAt k = specWorld k` for every `k` (Genesis, induction); the
  closed form evaluated and the stream run at stage 3 agree (book).
- Quiescence and well-formedness at every completed generated stage,
  and of the driver's run (Genesis); instances at stages 10 and 100
  (book); the carrier has `k+1` elements (book, off the form).
  `completed_not_every_prefix` checks an unmet requirement inside a
  block between two quiescent completed stages.
- Each of the four events of every block changes the state and the
  block lands on the next stage; genesis's first event is accepted
  (Genesis); block 3 walked explicitly (book).
- The budget trichotomy for every descriptor and event; the audit
  countermodel is a no-op for all 64 descriptors (Genesis); instances
  and the arbitrary-descriptor instance at `brokeWorld` (book).
- The Python stream reproduces the form, the driver and the artifact
  to stage 15; the trichotomy on 7 168 triples with no negative budget
  (mirror).

## What has not been proved

- Anything about the `close` policy's run (no driver exists for it) or
  about events outside the tower blocks.
- "Accepted ⇔ changed": only "changed ⇒ guard passed" is used, and the
  book shows the converse fails (`unguarded_can_be_silent`).
- Anything about `interpStep` beyond the budget field.
- A run "at every horizon" as an object: `∀ k` ranges over Lean's `Nat`,
  and the stream is supplied from outside (Unit 45).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `histUpTo`, `worldAt` | the supplied stream | metatheoretic producer (Unit 45) |
| `specWorld`, `w1`, `w2`, `w3` | the closed form | declared, then proved equal |
| `∀ k : Nat` | "every stage" | metatheory; finitude flag |
| `towerGen`, `genWorld` | the driver | metatheoretic (Unit 48) |
| `List.range_succ`, `mem_map`, `mem_range`, `omega` | the helpers | library |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The kernel's `step` and its guards; every
state on the stream is reached through them alone.

**Phrases to read with care.**

- "No emitted event is ever silently rejected" (docstring, 290-293):
  proved as "each event changes the state"; sound here because a
  rejection is the identity. Define "accepted" as "guard passed".
- "Lawfulness across extension ... at every horizon" (ledger
  CL-NC-AUTONOMY): for every Lean natural `k`. The Horizon docstrings
  say "at every stage" and claim no internal totality.
- "The gap is closed upward, not rescoped" (ledger): true of C6; the
  stage-3 theorem of Unit 45 is now an instance.
- "Identical facts on the same declared basis" (C10): the Python suite
  checks the countermodel and a finite basis of worlds and events; the
  Lean theorem is for every descriptor, world and event.

## Student exercise

Suppose the block were `[setBudget 1, admitTok k, require 0 k, addView
[0, k]]`, with a two-element column. Which helper breaks first in the
induction step, and would `worldAt_quiescent` still hold at every
stage?

## Answer

<details>
<summary>Worked answer</summary>

`sep_new_col` is the first to break in spirit, though its statement is
about `[m+1]`: the column `[0, m+1]` contains both `0` and `m+1`, so
`sepB [0, m+1] 0 (m+1) = false`, and the new requirement `(0, m+1)`
would not be separated by its own column. `increase_guard` then fails
on `w3 m`: the new column separates no unsatisfied pair with a
requirement, since the only unsatisfied requirement is `(0, m+1)` and
`[0, m+1]` does not separate it. So `augOkB` fails, `step` rejects the
`addView`, the block does not land on a `specWorld (m+1)` of the same
shape, and from stage 1 the requirement `(0, 1)` is recorded and
unsatisfied: the generated world is not quiescent at stage 1 or after.
The characterisation technique still applies, but the closed form it
would prove is a different one, with views empty and requirements
accumulating.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Horizon.lean` lines 45-74 (specification, intermediates), 76-232 (sixteen helpers), 236-254 (`worldAt_spec`), 261-344 (every-stage theorems), 351-361 (lift), 371-422 (budget pin) |
| Axiom report | `artifacts/lean_axioms.txt` lines 320-329: ten theorems, all `{propext, Quot.sound}`; sixteen helpers not exported |
| Paper | `paper/paper_claim_ledger.md` `CL-NC-AUTONOMY` (level 8); `paper/pr11_correction_ledger.md` C6 and C10 |
| Python | `code/derivation/represented.py` (`block_events`, `hist_up_to`, `events_all_accepted`, `productivity_report`), `code/derivation/completion.py::interp_step`, `artifacts/represented.json` key `productivity`, `tests/test_represented.py::test_productive_run_prefix_compatible`, `tests/test_completion.py::test_budget_saturation_matches_lean_nat`, `test_budget_trichotomy_every_descriptor_event` |
| Check (Python, partly book) | `python textbook/checks/u50_horizon.py`: `spec_world` and the intermediates as Python (book) against the stream to stage 15, the block walk, the guard facts, the lift and the artifact, the trichotomy on 7 168 triples, the countermodel on all 64 |
| Check (book Lean) | `python textbook/checks/u50_lean.py`: eighteen book reports plus the ten Genesis theorems kernel-checked, Lean 4.33.0 |
