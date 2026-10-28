# Unit 48. Generating the stream from the state, and describing the kernel to itself: the one thing that stays outside

**Claim.** `Constitution` replaces the supplied stream of Unit 45 by a
generated one. A policy datum (`Policy`: idle, tower, close) sits beside
the world; a fixed interpreter `nextFamily` maps the pair to the
complete family of next event blocks (empty, one tower block, or every
accepted repair and extension of every violated requirement:
`closeBlocks_complete_repair`, `closeBlocks_complete_aug`); a quiescent
world generates the empty family (`nextFamily_stop`); the driver
`towerGen` appends the tower family's unique member at each stage and
reproduces the supplied stream exactly (`driver_reproduces_tower`). The
fresh name is the carrier length, fresh along the tower
(`freshName_fresh_on_tower`) and not in general
(`freshName_not_fresh_generally`). The driver is assessed on a
nine-level ladder (`tower_driver_autonomy`) whose level 4, internal
triggering, is stated as not attained. The kernel's guards are written
as a six-bit descriptor (`ConstitutionDesc`); a fixed family interpreter
`interpStep` executes any descriptor; the all-on descriptor executes to
exactly the sealed step (`interp_describe`); the family is completely
enumerated (`allDescs_complete`, 64 members). **Status:** derived
relative to the fixed interpreter and its metatheoretic iteration; the
interpreter is not a member of the family it interprets, the module's
named irreducible obligation and the one OPEN row of the dependency
map. **Lean:** `lean4/Derivation/Constitution.lean` lines 44-391,
imports `Completion`. **Axioms:** `budget_replenishment_represented` and
`allDescs_length` none; `allDescs_complete` `propext`; the other
thirteen `{propext, Quot.sound}`. **Depends on:** Unit 45 (`histUpTo`,
`worldAt`, `blockEvents`, `worldAt_growth`,
`worldAt_three_quiescent`), Unit 46 (`augFamily`,
`augFamily_retains_ties`).

## Question

Unit 45's productive run was fed by `histUpTo`, a list of events written
down in the metatheory. Can the next events be computed from the
represented state instead, with no hidden choice and no hidden source of
names? And can the kernel's own rules be written as a datum and run,
so that the kernel describes itself? If so, what is left outside?

## What we already possess

- `World`, `step`, `replay`, `genesis`, the guards `reqOkB`, `markOkB`,
  `augOkB`, `obstructedB`, and `markApply`, `augApply` (Unit 45).
- `blockEvents k`, `histUpTo k`, `worldAt k`, with `worldAt_growth`
  (the carrier at stage `k` has `k + 1` tokens), `worldAt_data` and
  `worldAt_three_quiescent` (Unit 45).
- `repairFamily`, `augFamily` and the tie theorem (Unit 46).

## New concept: a family interpreter, a driver, a descriptor

*Family interpreter.* `nextFamily ⟨w, pol⟩` is a list of blocks, each a
list of events. Idle gives none; tower gives one block
`[setBudget 1, admitTok n, require 0 n, addView [n]]` with `n` the
carrier length; close gives, for each violated requirement, one block
per accepted repair and one per accepted extension.

*Driver.* `towerGen 0 = [admitTok 0]`; `towerGen (k+1)` is `towerGen k`
followed by the head of the tower family at the replayed world. This is
recursion on a Lean natural number: the iteration is metatheory.

*Descriptor.* Six Booleans, one per guard: deduplicate admissions,
guard requirements, guard acceptance of marks and views, gate on
budget, gate on license, certify refusals. `interpStep d` is a copy of
`step` in which each guard is consulted only when its bit is on.

## Plain-language interpretation

In Unit 45 someone had to hand the kernel its next events. Here the
kernel reads its own state and a policy datum, and a fixed rule produces
the complete list of what could come next. For the tower policy that
list has exactly one entry, so appending it is not a choice. For the
closure policy the list holds every accepted response to every violated
requirement, both orientations of an extension included, and nothing is
picked. On a quiescent world the list is empty: the stop is an answer,
not a crash. The fresh name is simply "the number of tokens so far",
which is new along the tower because the tower admits the numbers in
order, and which is not new in general, as a one-line countermodel
shows. The budget is topped up by an event the driver itself emits, in
the open. The theorem that matters says the generated history is,
stage by stage, the list that Unit 45 had supplied.

The honesty is in what the ladder leaves out. Nothing in the state
pulls the trigger: the loop that asks for the next family is a function
written outside, and the policy is a field no event can set. The
module says so in the words "metatheoretic iteration and a fixed
interpreter", and the paper counts level 4 as not attained.

The second half writes the kernel's guards as six switches. The machine
that reads the switches is the kernel's own text with each guard made
optional; all switches on is the kernel, by a proof that checks each
event kind. So the kernel is a member of a family of sixty-four
relaxations of itself, and the family is small enough to list. What is
not a member is the machine that reads the switches. That is the
boundary, and the module names it rather than hiding it. The audit
adds the plain reading of the headline: what is represented as data is
a choice among sixty-four relaxations of one hard-coded machine, not
the machine.

## Pseudocode

```
freshName w      = length w.data
towerBlock w     = [setBudget 1, admitTok (freshName w), require 0 (freshName w), addView [freshName w]]
closeBlocks w    = for r in w.reqs with violB w r:
                     [mark m] for m in repairFamily w r  ++  [addView c] for c in augFamily w r
nextFamily (w, idle)  = []
nextFamily (w, tower) = [towerBlock w]
nextFamily (w, close) = closeBlocks w

towerGen 0       = [admitTok 0]
towerGen (k+1)   = towerGen k ++ head (nextFamily (replay (towerGen k) genesis, tower))
theorem: towerGen k = histUpTo k

interpStep d w e = step w e with each guard consulted only if its bit in d is on
theorem: interpStep (all on) = step
allDescs = the 64 six-bit descriptors;  every descriptor is in it
```

## Python

Genesis's `code/derivation/completion.py` mirrors the module:
`fresh_name`, `tower_block`, `close_blocks`, `next_family(w, policy)`,
`tower_gen`, `all_descs`, `interp_step(d, w, e)`, `KERNEL_DESC`, and
`protocols_report` whose output is `artifacts/completion_protocols.json`.

```python
C.tower_gen(2)
# [('admit', 0), ('setBudget', 1), ('admit', 1), ('require', 0, 1), ('addView', (1,)),
#  ('setBudget', 1), ('admit', 2), ('require', 0, 2), ('addView', (2,))]
C.next_family(R.replay(C.PIGEON), "close")   # [[('addView', (1,))], [('addView', (2,))]]
C.interp_step(C.KERNEL_DESC, w, e) == R.step(w, e)
```

The check script's run:

```text
the driver, stage by stage (prefix, family size, block head, carrier growth, reproduces):
  k=0: prefix True, family 1, head ('setBudget', 1), grows True, reproduces True, fresh 1 not in data True
  k=1: prefix True, family 1, head ('setBudget', 1), grows True, reproduces True, fresh 2 not in data True
  k=2: prefix True, family 1, head ('setBudget', 1), grows True, reproduces True, fresh 3 not in data True
  k=3: prefix True, family 1, head ('setBudget', 1), grows True, reproduces True, fresh 4 not in data True
  k=4: prefix True, family 1, head ('setBudget', 1), grows True, reproduces True, fresh 5 not in data True
  k=5: prefix True, family 1, head ('setBudget', 1), grows True, reproduces True, fresh 6 not in data True
  towerGen 2: [('admit', 0), ('setBudget', 1), ('admit', 1), ('require', 0, 1), ('addView', (1,)), ('setBudget', 1), ('admit', 2), ('require', 0, 2), ('addView', (2,))]
  genWorld 2: {'data': [0, 1, 2], 'views': [[1], [2]], 'reqs': [[0, 1], [0, 2]], 'refusals': [], 'budget': 0, 'aug_licensed': True, 'notes': []}
  reproduces to stage 15: True
the policy is an argument, not a field any event writes:
  next_family(w, policy) takes the policy by hand; the kernel's events: ['addView', 'admit', 'require', 'setBudget']
the closure family and the stop outcome:
  close on the story: [[('addView', (1,))], [('addView', (2,))]]; idle: []; close on the quiescent stage-3 world: []
fresh names off the tower:
  world with data [1]: fresh_name 1 in data True
the constitution family:
  members 64; kernel description in it True
  kernel description = step on 91 (world, event) pairs: True
  descriptions that differ from the kernel somewhere on the battery: 63 of 64
  dedup off, admit 10 on the story: data (10, 20, 30, 10)
  protocols_report(15) equals the artifact: True
failures: []
```

## Line-by-line Python explanation

The first block runs six stages and prints the ladder's checkable rungs
at each: the generated history is a prefix of the next one, the tower
family has one member, that member opens with the budget event, the
carrier grows, the history equals the supplied one, and the fresh name
is not yet admitted. Then it compares the driver with the supplied
stream to stage 15, the mirror's declared bound.

The second block is the audit's second finding made visible: the
mirror's `next_family` takes the policy as an argument, and the
generated history contains only four kinds of event, none of which sets
a policy. The policy is data in the sense that it is a value; nothing
in the kernel writes it.

The third block is the closure family on the pigeonhole story (two
extension blocks, no repair) and the stop outcome on the quiescent
stage-3 world; the fourth is the one-token countermodel to general
freshness.

The last block enumerates the sixty-four descriptors, checks the
kernel's descriptor against `step` on seven worlds and thirteen events,
and counts how many descriptors differ from the kernel somewhere on
that battery: sixty-three, so every other descriptor is told apart by
some probe. Unit 49 proves the six load-bearing separations one guard
at a time. The dedup-off example shows one: the repeated token `10` is
admitted a second time. Finally the report is compared with the
artifact, key for key.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Constitution.lean lines 44-53, 62-83, 87-88, 106-115, 120-121
inductive Policy where
  | idle
  | tower
  | close
deriving Repr, DecidableEq

structure GWorld where
  w : World
  pol : Policy
deriving Repr, DecidableEq

def freshName (w : World) : Nat := w.data.length

def towerBlock (w : World) : List Event :=
  [.setBudget 1, .admitTok (freshName w),
   .require 0 (freshName w), .addView [freshName w]]

def closeBlocks (w : World) : List (List Event) :=
  (w.reqs.filter (fun r => violB w r)).flatMap fun r =>
    (repairFamily w r).map (fun m => [Event.mark m.1 m.2]) ++
      (Completion.augFamily w r).map (fun c => [Event.addView c])

def nextFamily : GWorld → List (List Event)
  | ⟨_, .idle⟩ => []
  | ⟨w, .tower⟩ => [towerBlock w]
  | ⟨w, .close⟩ => closeBlocks w

theorem nextFamily_tower_singleton (w : World) :
    (nextFamily ⟨w, .tower⟩).length = 1 := rfl

theorem closeBlocks_complete_aug {w : World} {r : Req} {c : View}
    (hr : r ∈ w.reqs) (hv : violB w r = true)
    (hc : c ∈ Completion.augFamily w r) :
    [Event.addView c] ∈ closeBlocks w := by
  unfold closeBlocks
  simp only [List.mem_flatMap]
  refine ⟨r, ?_, ?_⟩
  · exact List.mem_filter.mpr ⟨hr, hv⟩
  · simp only [List.mem_append, List.mem_map]
    exact Or.inr ⟨c, hc, rfl⟩

theorem nextFamily_stop {w : World} (hq : quiescentB w = true) :
    nextFamily ⟨w, .close⟩ = [] := by
  -- lines 122-141: the filter of violated requirements is empty,
  -- because a violated member would contradict quiescence.
```

```lean
-- Lean (Genesis), lean4/Derivation/Constitution.lean lines 152-171, 176-179, 189-199
def towerGen : Nat → List Event
  | 0 => [.admitTok 0]
  | k + 1 =>
      towerGen k ++
        (nextFamily ⟨replay (towerGen k) genesis, .tower⟩).headD []

theorem towerBlock_eq (k : Nat) :
    towerBlock (worldAt k) = blockEvents (k + 1) := by
  unfold towerBlock blockEvents freshName
  rw [worldAt_growth]

theorem freshName_fresh_on_tower (k : Nat) :
    ¬ (freshName (worldAt k) ∈ (worldAt k).data) := by
  intro hmem
  unfold freshName at hmem
  rw [worldAt_growth, worldAt_data] at hmem
  have := List.mem_range.mp hmem
  omega

theorem freshName_not_fresh_generally :
    freshName { data := [1], views := [], reqs := [], refusals := [],
                budget := 0, augLicensed := true, notes := [] } ∈
      ([1] : List Nat) := by decide

theorem driver_reproduces_tower : ∀ k, towerGen k = histUpTo k := by
  intro k
  induction k with
  | zero => rfl
  | succ m ih =>
      show towerGen m ++
        (nextFamily ⟨replay (towerGen m) genesis, .tower⟩).headD [] =
          histUpTo m ++ blockEvents (m + 1)
      rw [ih, show replay (histUpTo m) genesis = worldAt m from rfl]
      show histUpTo m ++ towerBlock (worldAt m) = _
      rw [towerBlock_eq]
```

```lean
-- Lean (Genesis), lean4/Derivation/Constitution.lean lines 255-279 (statement), 303-349 (statement), 377-391
theorem tower_driver_autonomy :
    (∀ k, towerGen k <+: towerGen (k + 1)) ∧
      (∀ k, nextFamily (genWorld k) =
        [towerBlock (genWorld k).w]) ∧
      (∀ k, towerGen (k + 1) =
        towerGen k ++ towerBlock (genWorld k).w) ∧
      (∀ k, (nextFamily (genWorld k)).length = 1) ∧
      (∀ k, (towerBlock (genWorld k).w).head? =
        some (.setBudget 1)) ∧
      (∀ k, (genWorld k).w.data.length <
        (genWorld (k + 1)).w.data.length) := by
  -- four conjuncts by rfl, the first by exhibiting the block, the last by gen_growth and omega

structure ConstitutionDesc where
  dedupAdmit : Bool
  guardRequire : Bool
  guardAccept : Bool
  gateBudget : Bool
  gateLicense : Bool
  certRefusal : Bool
deriving Repr, DecidableEq

def kernelDesc : ConstitutionDesc := ⟨true, true, true, true, true, true⟩

def interpStep (d : ConstitutionDesc) (w : World) : Event → World
  | .admitTok t =>
      if d.dedupAdmit && decide (t ∈ w.data) then w
      else { w with data := w.data ++ [t] }
  | .require i j =>
      if !d.guardRequire || reqOkB w i j then
        { w with reqs := w.reqs ++ [(i, j)] }
      else w
  -- lines 326-344: mark, addView, refuse with their guards made optional;
  -- note, setBudget, setAugLicense exactly as step.

theorem interp_describe (w : World) (e : Event) :
    interpStep kernelDesc w e = step w e := by
  -- lines 350-372: cases on the event; admitTok by cases on membership;
  -- require, mark, addView, refuse by simp only with the toggles true;
  -- the last three by rfl.

def bools : List Bool := [false, true]

def allDescs : List ConstitutionDesc :=
  bools.flatMap fun a => bools.flatMap fun b =>
    bools.flatMap fun c => bools.flatMap fun e =>
      bools.flatMap fun f => bools.map fun g => ⟨a, b, c, e, f, g⟩

theorem allDescs_length : allDescs.length = 64 := by decide

theorem allDescs_complete : ∀ d : ConstitutionDesc, d ∈ allDescs := by
  intro d
  cases d with
  | mk a b c e f g =>
      cases a <;> cases b <;> cases c <;> cases e <;> cases f <;>
        cases g <;> decide
```

The book's Lean evaluates the driver at small stages, applies the
Genesis theorems at those stages, records a second freshness
collision, runs the closure policy on the pigeonhole story, and shows
one relaxed descriptor differing from the kernel.

```lean
-- Lean (book), textbook/checks/u48_lean.py
def story : World :=
  replay [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
    .require 0 1, .require 0 2, .require 1 2, .addView [0]] genesis

theorem tower_gen_two :
    towerGen 2 = [.admitTok 0, .setBudget 1, .admitTok 1, .require 0 1, .addView [1],
                  .setBudget 1, .admitTok 2, .require 0 2, .addView [2]] := by decide

theorem gen_two_world :
    (genWorld 2).w.data = [0, 1, 2] ∧ (genWorld 2).w.views = [[1], [2]] ∧
    (genWorld 2).w.reqs = [(0, 1), (0, 2)] ∧ (genWorld 2).w.budget = 0 := by decide

theorem reproduces_five : towerGen 5 = histUpTo 5 := driver_reproduces_tower 5
theorem reproduces_five_evaluated : towerGen 5 = histUpTo 5 := by decide

theorem fresh_instance :
    freshName (genWorld 4).w = 5 ∧ ¬ (freshName (genWorld 4).w ∈ (genWorld 4).w.data) := by
  decide
theorem fresh_on_tower_four : ¬ (freshName (worldAt 4) ∈ (worldAt 4).data) :=
  freshName_fresh_on_tower 4

theorem collides_elsewhere :
    freshName { story with data := [0, 1, 3] } = 3 ∧ 3 ∈ ([0, 1, 3] : List Nat) := by decide

theorem close_on_story :
    nextFamily ⟨story, .close⟩ = [[.addView [1]], [.addView [2]]] := by decide

theorem close_complete_instance : [Event.addView [2]] ∈ closeBlocks story :=
  closeBlocks_complete_aug (r := (1, 2)) (by decide) (by decide) (by decide)

theorem stop_instance : nextFamily ⟨(genWorld 3).w, .close⟩ = [] :=
  nextFamily_stop gen_three_quiescent
theorem idle_nothing (w : World) : nextFamily ⟨w, .idle⟩ = [] := rfl

theorem ladder_prefix : towerGen 2 <+: towerGen 3 := tower_driver_autonomy.1 2
theorem ladder_growth : (genWorld 2).w.data.length < (genWorld 3).w.data.length :=
  tower_driver_autonomy.2.2.2.2.2 2

theorem policy_kept (g : GWorld) (e : Event) :
    (⟨step g.w e, g.pol⟩ : GWorld).pol = g.pol := rfl

theorem describe_instance :
    interpStep kernelDesc story (.addView [1]) = step story (.addView [1]) :=
  interp_describe _ _
theorem relaxed_dedup_differs :
    (interpStep { kernelDesc with dedupAdmit := false } story (.admitTok 10)).data =
      [10, 20, 30, 10] ∧
    (step story (.admitTok 10)).data = [10, 20, 30] := by decide

theorem kernel_in_family : kernelDesc ∈ allDescs := allDescs_complete _
theorem all_off_in_family :
    (⟨false, false, false, false, false, false⟩ : ConstitutionDesc) ∈ allDescs := by decide
```

## Line-by-line Lean explanation

**`Policy`, `GWorld` (44-53).** Three constructors and a pair. The
docstring says the policy is "admitted into the generative state";
there is no event that admits or changes it, and `towerGen` writes
`.tower` into the pair by hand at every stage. The book's `policy_kept`
is `rfl` because the only way to step a `GWorld` is to step its world
and copy its policy. Read "admitted" as "a field".

**`freshName`, `towerBlock` (62-66).** The length of the carrier, then
the four-event block of Unit 45 with that number in the three places
`blockEvents (k+1)` had `k + 1`. The docstring prices the import:
arithmetic and ordering, the successor structure the reflective chain
already paid for.

**`closeBlocks`, `nextFamily` (71-83).** The filter keeps the violated
requirements; `flatMap` concatenates, per requirement, the marks from
the repair family and the views from `augFamily`. `nextFamily` reads
the policy. `nextFamily_tower_singleton` is `rfl`: the tower case is a
one-element list by construction. The book's `close_on_story` runs the
closure policy on the story of Unit 46: no repair, both extensions.

**The two completeness theorems (92-115).** Membership in a `flatMap`
is an existential over the outer list; the requirement is in the
filtered list by `mem_filter`, and the block is in the left or right
summand by `mem_map`. The book's `close_complete_instance` supplies the
three hypotheses by `decide` with `r` named explicitly.

**`nextFamily_stop` (120-141).** If the filtered list had a head `x`,
then `x` would be a violated requirement; but quiescence says every
requirement is satisfied, and `violB` is `membership ∧ ¬ satB`, so
`hviol.2` is `!true = true`, closed by `decide`. The book's
`stop_instance` feeds `gen_three_quiescent`.

**`towerGen` (152-156).** The seed admission, then at each stage the
head of the tower family at the replayed world. `headD []` is a total
head; the family is never empty on the tower policy, so the default is
never used. The book's `tower_gen_two` is the list in full and
`gen_two_world` the world it reaches: three tokens, two columns, two
requirements, budget zero after the two augmentations.

**`towerBlock_eq`, `freshName_fresh_on_tower`,
`freshName_not_fresh_generally` (158-179).** At stage `k` the carrier has
`k + 1` tokens, so the fresh name is `k + 1` and the block is
`blockEvents (k+1)`. Freshness on the tower: the carrier is
`List.range (k+1)` by `worldAt_data`, so membership of `k + 1` gives
`k + 1 < k + 1`, closed by `omega`. Off the tower, a carrier `[1]` has
fresh name `1`. The book's `collides_elsewhere` is a second collision.

**`driver_reproduces_tower` (189-199).** Induction. The successor step
rewrites with the hypothesis, identifies `replay (histUpTo m) genesis`
with `worldAt m` definitionally, and closes with `towerBlock_eq`. The
audit's note: the content is `freshName (worldAt k) = k + 1`; the rest
is definitional unfolding. The book's two `reproduces_five` prove the
same instance by the theorem and by evaluation.

**`tower_driver_autonomy` (255-279).** Six conjuncts for every stage:
prefix, family value, append equation, family length, block head,
strict growth. Four are `rfl`; the prefix exhibits the block; the
growth is `gen_growth` twice and `omega`. The docstring lists nine
levels; the theorem states six facts. Level 4 is absent by design,
level 8 is carried by Unit 50, and the correction ledger C6 records
that an earlier ledger entry cited this theorem for lawfulness it does
not contain. The book's two `ladder_*` theorems take conjuncts at stage
2.

**`ConstitutionDesc`, `kernelDesc`, `interpStep` (303-344).** Six bits.
`interpStep` is `step` with each guard behind `!d.bit || guard`, so an
off bit makes the guard pass. Everything else, the event grammar, the
application functions, the budget decrement, the `notes` field, is
written into `interpStep` itself and is not described by any bit. The
book's `relaxed_dedup_differs` turns one bit off: the story admits
`10` again.

**`interp_describe` (348-372).** Cases on the event. For `admitTok`
the two `if`s are aligned by cases on membership; for the four guarded
events `simp only` with the bits true reduces `!true || g` to `g` and
the two sides coincide; the last three are `rfl`. It is an extensional
equality of two Lean functions, one of which is a parameterised copy
of the other. The book's `describe_instance` applies it.

**`allDescs`, `allDescs_length`, `allDescs_complete` (377-391).** Six
nested `flatMap`s over `[false, true]`; sixty-four by `decide`;
completeness by sixty-four `cases` and a `decide` each, which is why
that theorem needs only `propext`. The book's `kernel_in_family` and
`all_off_in_family` are two members.

## What has been proved

- The tower family is a singleton; the closure family contains every
  accepted repair and every accepted extension of every violated
  requirement; a quiescent world's closure family is empty (Genesis).
- The generated history equals the supplied stream at every stage
  (Genesis; at stage 5 twice in the book, by the theorem and by
  evaluation; to stage 15 in Python).
- The fresh name is new along the tower and not in general (Genesis;
  two collisions in the book and the mirror).
- Six ladder facts at every stage: prefix, singleton family, append
  equation, family length, budget head, strict growth (Genesis; two at
  stage 2 in the book; six at six stages in Python).
- The all-on descriptor executes as the sealed step for every world
  and event (Genesis; one instance in the book; ninety-one in Python);
  one relaxed descriptor differs (book); sixty-three of sixty-four
  differ somewhere on the battery (Python).
- The family has sixty-four members and every descriptor is one of
  them (Genesis).

## What has not been proved

- Internal triggering (level 4): no represented transition invokes
  `nextFamily`; the recursion of `towerGen` is Lean's.
- Lawfulness at every stage: `gen_three_quiescent` is stage 3; Unit 50
  proves every stage.
- That any driver runs the closure policy: `closeBlocks` has
  completeness theorems and no generation theorem.
- That the policy can be changed by an event: it cannot; `Event` has no
  such constructor.
- That the kernel's semantics is described by data: the six bits select
  guards of a machine whose text is `interpStep`; the machine is not a
  descriptor.
- An interpreter that interprets `interpStep`: not formulated; the OPEN
  row of the map (Unit 51).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `nextFamily`, `towerBlock`, `closeBlocks` | the fixed interpreter | declared constitution |
| `freshName := w.data.length` | the name source | declared; imports arithmetic and ordering, priced in the paper |
| `towerGen : Nat → List Event` | the driver | metatheoretic recursion; `∀ k` is over Lean's `Nat` |
| `Policy` as a field of `GWorld` | the policy datum | declared; written by no event |
| `interpStep` | the family interpreter | declared constitution; not a member of `allDescs` |
| `ConstitutionDesc` | the six switches | declared family |
| `List.flatMap`, `mem_filter`, `mem_range`, `omega`, `decide` | computation and proof | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** A complete next-event family computed from
the state, with the tower member unique and the closure members all
retained; a stop that is a verdict; the six guards of the kernel as six
switches, with the kernel the all-on setting.

**Phrases to read with care.**

- "The kernel constitution is represented as data" (header, ledger
  `CL-NC-CONSTITUTION`, map row 41): a six-bit choice among sixty-four
  relaxations of one hard-coded machine is represented; the machine is
  not. The audit records this as a moderate interpretation defect in the
  prose; the theorem is correct.
- "The policy store: first-order data, admitted into the generative
  state" (line 40): a field, not an admission.
- "Self-description": `interpStep kernelDesc = step`, relative to
  `interpStep`. Not a coded interpreter inside the world, not an
  independent semantics, not an absolute self-interpreter.
- "Nothing stronger is claimed" (line 254): level 4 is not attained and
  level 8 is carried by `Horizon`.

## Student exercise

Write out `nextFamily ⟨(genWorld 1).w, .close⟩` by hand. First find the
world at stage 1 (use `tower_gen_two` cut after the first block), then
its violated requirements. Then say why `nextFamily_stop` applies, or
does not, and what `closeBlocks` would contain if it did not.

## Answer

After `[admitTok 0, setBudget 1, admitTok 1, require 0 1, addView [1]]`
the world has data `[0, 1]`, views `[[1]]`, requirements `[(0, 1)]`,
budget 0. The column `[1]` contains `1` and not `0`, so `(0, 1)` is
satisfied and no requirement is violated; the world is quiescent, so
`nextFamily_stop` applies and the family is `[]`. Had the requirement
been violated, say with no column, `closeBlocks` would hold one block
per accepted mark in the repair family and one per accepted extension
in `augFamily`, which here would be `[[.addView [0]], [.addView [1]]]`
under a positive budget, and nothing at budget 0, since `augOkB`
requires budget through `increaseB` only indirectly; the check is the
kernel's, not the family's, and the family lists what the kernel
accepts.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Constitution.lean` lines 44-141 (policy, blocks, interpreter, completeness, stop), 152-231 (driver, freshness, reproduction, growth, stage 3), 255-279 (ladder), 303-391 (descriptor, family interpreter, self-description, enumeration) |
| Axiom report | `artifacts/lean_axioms.txt` lines 293-308: `budget_replenishment_represented`, `allDescs_length` none; `allDescs_complete` `propext`; thirteen `{propext, Quot.sound}` |
| Paper | `paper/native_derivation_completion.md` sections 9 (event production, fresh-name pricing), 10 (the constitution, KERNEL_CONSTITUTION_REMAINS_META), 11 (autonomy versus iterability); `paper/paper_claim_ledger.md` `CL-NC-EVENT-SOURCE`, `CL-NC-AUTONOMY` (C6 correction), `CL-NC-CONSTITUTION`; `paper/native_derivation_map.md` rows 40-42; `paper/pr11_correction_ledger.md` C6 |
| Used later | `Horizon.lean` (every stage), `Initiality.lean` (the six separations, `unique_compliant`), `InterpreterBoundary.lean` (the diagonal) |
| Python | `code/derivation/completion.py` (`tower_gen`, `next_family`, `close_blocks`, `fresh_name`, `interp_step`, `all_descs`, `protocols_report`), `artifacts/completion_protocols.json`, `tests/test_completion.py` (`test_driver_reproduces_supplied_stream`, `test_interp_kernel_desc_matches_step`, `test_freshness_scoped_to_tower_invariant`) |
| Check (Python) | `python textbook/checks/u48_constitution.py`: six stages of the ladder, reproduction to 15, the closure family and stop, the freshness countermodel, the 64 descriptors on a 91-pair battery, the report against the artifact |
| Check (book Lean) | `python textbook/checks/u48_lean.py`: eighteen book declarations plus eleven Genesis theorems kernel-checked, Lean 4.33.0 |
