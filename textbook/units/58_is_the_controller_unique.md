# Unit 58. Is the controller unique? Simulations, the absorbing halt, and uniqueness only along replay

**Claim.** Controller uniqueness depends on the comparison and simulation requirements. The stated strict-controller result gives agreement along replay; unrestricted simulations allow many alternatives.

**Status:** FROZEN; VERIFIED_FINITE (the 1024
census, the 128, the three batteries); REFUTED (initiality; strict
global uniqueness); CONDITIONAL (the orbit agreement, for the one
hom-set the theorem names). **Lean:**
`lean4/Derivation/ControllerCategory.lean` lines 84-774, imports
`PrimitivePassage`. **Axioms:** 63 reports; `propext, Quot.sound` for
46, `propext` for `mem_bools`, none for 16 (the `decide` censuses and
the `setRef` field lemmas). **Depends on:** Unit 54 (`PState`, `PEvent`,
`step`, `replayP`, `genesisP`, `obstP`, `nextFamilyP`, `step_halted`),
Unit 49 (the six-toggle uniqueness and its scope note).

## First pass

A controller enables or disables specified kinds of event. A simulation is a state map that commutes with the controlled transition.

A constant map into an absorbing halted state can satisfy a weak simulation condition. Read the additional strictness requirements before interpreting uniqueness, and keep agreement on the reachable replay orbit separate from agreement on every state.

## Detailed claim and formal anchors

Unit 49 showed the kernel's descriptor unique among 64
guard-toggle descriptors under six probes, and its scope note said that
uniqueness was relative to that class. `ControllerCategory` widens the
class: a *controller* is one enable bit per event kind of the passage
dynamics (Unit 54), the supply event always on; an enabled event runs
the sealed `step`, a disabled one is inert.

There are 1024 controllers
(`allKinds_complete`), the all-on one is the sealed step
(`interpK_full`), and 128 of them enable the three response kinds
(`live_census`).

Every live controller resolves the funded obstruction
`OBST5` by the two-rule block (`tworule_executable_of_live`); disabling
`addCol`, `setBudget` or `refineCol` leaves an obstruction standing on a
state where that kind is load-bearing, over the kernel's own battery of
blocks (`dead_without_addcol`, `dead_without_budget`,
`dead_without_refine`).

Two live controllers, all-on and refusal-free,
agree on every refusal-free event at every state (`nonrefuse_agree`)
and differ at a certified obstruction (`refuse_distinguishes`): probe
compliance does not pin a controller.

A *simulation* between
controllers is a state map commuting with the controlled step; the
category laws hold (`comp_id`, `id_comp`, `comp_assoc`); refusal
erasure is a simulation from the all-on to the refusal-free controller
(`erase_sim`).

But the halted state absorbs every event, so every
constant map to a halted state is a simulation between any two
controllers: every pair is connected (`every_pair_connected`), no pair
has a unique simulation (`sims_never_unique`), and no controller is
initial, in the whole class or among the live ones (`no_initial_ctrl`,
`no_initial_live_ctrl`).

Demanding that a simulation fix genesis and
preserve liveness excludes the constants (`const_not_strict`) but not
non-uniqueness: a twist keyed to a step-invariant that genesis lacks is
a second strict simulation (`strict_not_unique`).

What survives is
agreement on the replay orbit: any two strict simulations from the
all-on to the refusal-free controller agree on every state replayed
from genesis (`strict_agree_on_reachable`, via `sim_pinned` and
`reachable_no_dup`).

## Question

Unit 49 proved one descriptor unique. Was that a fact about the kernel,
or a fact about the small class it was compared in? Put the kernel in a
class that varies which events it answers at all, define what it means
for one controller to simulate another, and ask whether any controller
has a unique map to every other. If not, what is the most that survives?

## What we already possess

- The passage state `PState` with nine fields, including `refusals`
  and `halted`; the eleven event kinds; `step`; `replayP h s`;
  `genesisP`; `obstP s i j`; `nextFamilyP s`, the kernel's own list of
  response blocks at an obstructed state; `step_halted`: on a halted
  state every event is inert (Unit 54).
- `Initiality.unique_compliant` and its scope note: unique among 64
  toggle descriptors under six probes, and nothing wider (Unit 49).

## New concept: controllers, simulations, initiality

A `KindDesc` is ten booleans. `enabled d e` reads the bit for the kind
of `e`, except that `assertWit` is always enabled: the class varies the
response grammar, never the supply of asserted differences. `interpK d
s e` is `step s e` when enabled and `s` otherwise. `allKinds` lists all
1024.

`ResponseLiveB d` says the three response bits (`refineCol`, `addCol`,
`setBudget`) are on. A *simulation* `Sim C1 C2` is a function `f` on
states with `f (interpK C1 s e) = interpK C2 (f s) e` for every state
and event. `InitialCtrl C` says: to every controller `T` there is
exactly one simulation from `C`. A *strict* simulation also fixes
`genesisP` and sends non-halted states to non-halted states.

`eraseRef` empties the refusal store. `hasDup xs` says some element of
a list recurs. `twistRef s` is `[(0, 0)]` when `s.occ` has a duplicate
and `[]` otherwise; `twistF` writes it into the refusal store.

## Plain-language interpretation

Imagine 1024 switchboards. Each has ten switches, one per kind of
request the kernel can receive; a request whose switch is off is
ignored, one whose switch is on is handled exactly as the sealed kernel
handles it. The all-on board *is* the kernel.

First question: which boards can do the two-rule repair of Unit 54?
Those with the two repair switches and the funding switch on, 128 of
them. Each of the three switches matters somewhere: turn off `addCol`
and the funded obstruction `OBST5` cannot be cleared by any block the
kernel itself proposes; turn off `setBudget` and the unfunded version
cannot; turn off `refineCol` and the unlicensed, refinable one cannot.
But note the word "somewhere": at `OBST5` itself, which already has
budget 5, only `addCol` is needed, and 512 boards clear it (the book's
Python count). "Live" is a syntactic condition that suffices at the
chosen state and whose each part is necessary at some state; it is not
proved to be the same as "clears every obstruction".

Second question: does behaviour pin the board? No. The all-on board and
the board with `refuse` off behave identically on every request that is
not a refusal, at every state, and differ only when a refusal is
recorded at an obstruction. So two different boards pass every probe
that does not mention refusals. Unit 49's uniqueness was about its
class.

Third question, the real one: define a map between boards as a way of
translating states so that handling a request before translating gives
the same as translating and then handling. Translating by emptying the
refusal list is such a map from the all-on board to the refuse-off
board, and it is a real one: the kernel reads the refusal list only
when refusing. Is there a board from which there is exactly one such
map to every other board? No, and for a cheap reason. Once a board has
halted, it ignores everything. So the map "send every state to this
halted state" translates correctly from any board to any board: both
sides stay put. There are two different halted states, hence two
different maps, between every pair. Uniqueness fails everywhere, and
with it initiality, whether or not you restrict to live boards.

Fourth: forbid the cheap maps by demanding that genesis go to genesis
and live states to live states. The constants are gone; the identity
and refusal-erasure remain. Uniqueness still fails, now for an
interesting reason. "The occurrence list has a repeat" is a property no
request can create or destroy, and genesis lacks it. So "empty the
refusal list, unless the occurrence list has a repeat, in which case
write one junk refusal" is also a strict map, and it differs from plain
erasure exactly on states with a repeat. Such states exist on paper,
`[5, 5]`, and are never reached from genesis, because admission
deduplicates.

What survives: along any history replayed from genesis, every strict
map from the all-on board to the refuse-off board gives the same
answer, because such a map is pinned by its value at genesis and the
commutation square, one request at a time. That is a statement about
replay, not about a universal property, and it is proved for the one
pair of boards the theorem names.

## Pseudocode

```
interpK(d, s, e) := step(s, e) if enabled(d, e) else s
live(d)          := d.refineCol and d.addCol and d.setBudget

claim: for all live d, obstP(interpK(d, interpK(d, OBST5, setBudget 1), addCol [0]), 0, 1) = false
countermodels: noAddK at OBST5, noBudgetK at OBST0, noRefineK at LOBST:
    every block in nextFamilyP(state) leaves obstP true

Sim(C1, C2) := f with f(interpK(C1, s, e)) = interpK(C2, f(s), e) for all s, e
constSim(t) := s ↦ t, for any halted t     -- a Sim between any C1, C2
HALTED0 ≠ HALTED1, so two Sims between every pair: no initial object

strict: f(genesisP) = genesisP and f keeps halted = false
eraseRef(s) := s with refusals []
twistF(s)   := s with refusals ([(0,0)] if hasDup(s.occ) else [])
both strict Sims fullCtrl → noRefCtrl; differ at DUPSTATE; agree on replayP(h, genesisP)
```

## Python

Genesis's mirror, `code/derivation/controller_category.py`:

```python
def enabled(d: KindDesc, e: PEvent) -> bool:
    kind = e[0]
    if kind == "assertWit":
        return True
    if not isinstance(kind, str) or kind not in _KIND_INDEX:
        raise ValueError(f"unknown event kind: {kind!r}")
    return d[_KIND_INDEX[kind]]


def interp_k(d: KindDesc, s: PS, e: PEvent) -> PS:
    return pstep(s, e) if enabled(d, e) else s


def response_live(d: KindDesc) -> bool:
    return (d[_KIND_INDEX["refineCol"]] and d[_KIND_INDEX["addCol"]]
            and d[_KIND_INDEX["setBudget"]])


def _battery_persists(d: KindDesc, s: PS) -> bool:
    battery = next_family_p(s)
    return battery != [] and all(
        obst_p(replay_k(d, blk, s), 0, 1) for blk in battery)


def twist_ref(s: PS) -> tuple[tuple[int, int], ...]:
    return ((0, 0),) if has_dup(s.occ) else ()


def twist_f(s: PS) -> PS:
    return replace(s, refusals=twist_ref(s))
```

The book's check, `textbook/checks/u58_controller_category.py`, adds
Python (book):

```python
    resolves = [d for d in kinds
                if not obst_p(replay_k(d, TWORULE_BLOCK, OBST5), 0, 1)]
    inert_all = all(interp_k(d, h, e) == h
                    for d in kinds for h in (HALTED0, HALTED1) for e in BASIS_EVENTS)
```

## Line-by-line Python explanation

- `enabled`: the `assertWit` branch returns `True` before the table is
  consulted. This one line is the declared scope of the whole class.
- `interp_k`: the sealed `pstep` behind a switch. The step itself is
  never changed.
- `response_live`: three lookups. Nothing about behaviour is in it.
- `_battery_persists`: the battery is the kernel's own `next_family_p`
  at the state, required nonempty so the "all blocks fail" claim is not
  vacuous; then every block is replayed under the crippled controller
  and the obstruction must still be certified.
- `twist_ref`, `twist_f`: the countermodel map. `has_dup` is preserved
  by every event in both directions, which is why the square commutes.
- Python (book) `resolves`: all 1024 controllers replayed on the
  two-rule block at `OBST5`. The count is 512, every controller with
  `addCol` on, because `OBST5` already carries budget 5 and the block's
  `setBudget 1` is not what pays for the extension there. All 128 live
  controllers are among the 512.
- Python (book) `inert_all`: the two halted states under all 1024
  controllers and all ten basis events. True for every one: the
  constant-simulation argument has no exception in the class.

## Lean 4

The class and the live census (`lean4/Derivation/ControllerCategory.lean`
lines 98-176, abridged):

```lean
def enabled (d : KindDesc) : PEvent → Bool
  | .admitOcc _ => d.kAdmitOcc
  | .assertWit _ _ => true
  | .admitWit _ _ => d.kAdmitWit
  ...
  | .halt => d.kHalt

def interpK (d : KindDesc) (s : PState) (e : PEvent) : PState :=
  if enabled d e then step s e else s

theorem interpK_full (s : PState) (e : PEvent) :
    interpK fullK s e = step s e := by
  cases e <;> rfl

theorem live_census : (allKinds.filter ResponseLiveB).length = 128 := by
  decide

theorem tworule_executable_of_live (d : KindDesc)
    (hlive : ResponseLiveB d = true) :
    obstP (interpK d (interpK d OBST5 (.setBudget 1)) (.addCol [0]))
      0 1 = false := by
  obtain ⟨a, b, c, d0, e, f, g, h, i, j⟩ := d
  simp only [ResponseLiveB, Bool.and_eq_true] at hlive
  obtain ⟨⟨-, hf⟩, hh⟩ := hlive
  subst hf; subst hh
  rfl
```

Simulations, constants and the refutation (lines 298-560, abridged):

```lean
structure Sim (C1 C2 : Ctrl) where
  f : PState → PState
  comm : ∀ s e, f (interpK C1.d s e) = interpK C2.d (f s) e

def constSim (C T : Ctrl) (t : PState) (ht : t.halted = true) :
    Sim C T where
  f := fun _ => t
  comm := by
    intro s e
    show t = interpK T.d t e
    unfold interpK
    split
    · exact (step_halted t e ht).symm
    · rfl

theorem sims_never_unique (C T : Ctrl) : ∃ u v : Sim C T, u ≠ v :=
  ⟨constSim C T HALTED0 rfl, constSim C T HALTED1 rfl,
    const_sims_distinct C T⟩

theorem no_initial_ctrl : ¬ ∃ C : Ctrl, InitialCtrl C := by
  intro hex
  obtain ⟨C, hC⟩ := hex
  obtain ⟨u, hu⟩ := hC fullCtrl
  exact const_sims_distinct C fullCtrl
    ((hu (constSim C fullCtrl HALTED0 rfl)).trans
      (hu (constSim C fullCtrl HALTED1 rfl)).symm)
```

The strict refinement and the orbit (lines 583-774, abridged):

```lean
structure StrictSim (C1 C2 : Ctrl) extends Sim C1 C2 where
  gen : toSim.f genesisP = genesisP
  live : ∀ s, s.halted = false → (toSim.f s).halted = false

theorem strict_not_unique :
    ∃ u v : StrictSim fullCtrl noRefCtrl, u ≠ v := by
  refine ⟨twistStrict, eraseStrict, ?_⟩
  intro hEq
  exact twist_ne_erase_at_dup
    (congrArg (fun u : StrictSim fullCtrl noRefCtrl =>
      u.toSim.f DUPSTATE) hEq)

theorem sim_pinned (u : Sim fullCtrl noRefCtrl) (hist : List PEvent)
    (s : PState) :
    u.f (replayP hist s)
      = List.foldl (interpK noRefCtrl.d) (u.f s) hist := by
  induction hist generalizing s with
  | nil => rfl
  | cons e rest ih =>
      show u.f (replayP rest (step s e))
        = List.foldl (interpK noRefCtrl.d)
            (interpK noRefCtrl.d (u.f s) e) rest
      rw [ih (step s e)]
      have hc : u.f (step s e) = interpK noRefCtrl.d (u.f s) e := by
        have h0 := u.comm s e
        rw [show interpK fullCtrl.d s e = step s e from
          interpK_full s e] at h0
        exact h0
      rw [hc]

theorem genesis_sims_agree_on_reachable
    (u v : Sim fullCtrl noRefCtrl)
    (hu : u.f genesisP = genesisP) (hv : v.f genesisP = genesisP)
    (hist : List PEvent) :
    u.f (replayP hist genesisP) = v.f (replayP hist genesisP) := by
  rw [sim_pinned u hist genesisP, sim_pinned v hist genesisP, hu, hv]
```

Lean (book), from `textbook/checks/u58_lean.py`: a non-live controller
that still clears `OBST5`; the erasure square evaluated; and, for a
pair the theorem does not name, two genesis-preserving simulations that
disagree on a replayed state.

```lean
theorem noRefine_resolves_obst5 :
    obstP (replayK noRefineK [.setBudget 1, .addCol [0]] OBST5) 0 1 = false := by decide

theorem noRefine_not_live : ResponseLiveB noRefineK = false := by decide

theorem erase_square_values :
    eraseRef (interpK fullK OBST5 (.refuse 0 1)) = OBST5 ∧
    interpK noRefK (eraseRef OBST5) (.refuse 0 1) = OBST5 := by
  constructor <;> decide

def refTag : PState → PState :=
  fun s => if s.refusals = [] then s else setRef [(0, 0)] s

theorem refusals_step_nonrefuse (s : PState) (e : PEvent) (h : isRefuse e = false) :
    (step s e).refusals = s.refusals := by
  have h1 := setRef_step_comm s.refusals s e h
  have h2 : setRef s.refusals s = s := rfl
  rw [h2] at h1
  exact (congrArg PState.refusals h1).symm

def refTagSim : Sim noRefCtrl noRefCtrl where
  f := refTag
  comm := by
    intro s e
    cases e with
    | admitOcc t => exact refTag_step_comm s (.admitOcc t) rfl
    ...
    | refuse i j => rfl
    ...

def refHist : List PEvent :=
  [.admitOcc 7, .admitOcc 8, .assertWit 0 1, .admitWit 0 1, .protect 0 1, .declareObs,
   .setBudget 1, .refuse 0 1]

theorem other_pair_counterexample :
    refTagSim.f genesisP = genesisP ∧ (idSim noRefCtrl).f genesisP = genesisP ∧
    refTagSim.f (replayP refHist genesisP) ≠ (idSim noRefCtrl).f (replayP refHist genesisP) := by
  refine ⟨rfl, rfl, ?_⟩
  show refTag (replayP refHist genesisP) ≠ replayP refHist genesisP
  decide

theorem same_under_own_replay :
    refTag (replayK noRefK refHist genesisP) = replayK noRefK refHist genesisP := by decide
```

## Line-by-line Lean explanation

- `enabled … | .assertWit _ _ => true`: the one hard-wired arm. The
  other ten read a field. So "1024 controllers" is 2 to the power ten
  over eleven kinds.
- `interpK_full … cases e <;> rfl`: eleven cases, each `if true then
  step s e else s`, which is `step s e` by computation.
- `live_census … by decide`: the kernel filters a 1024-element list and
  counts. It needs a raised recursion depth in the source file.
- `tworule_executable_of_live`: destructure the ten bits; from
  `hlive` extract that bits `f` (`addCol`) and `h` (`setBudget`) are
  `true`; substitute; the remaining goal is a closed computation and
  `rfl` runs it. The bit `c`-through-`j` that are not substituted
  stay free, which is what "generic over the 128" means: the proof
  never looks at them. Note that the refine bit is discarded (`-`),
  consistent with the book's finding that 512 controllers clear
  `OBST5`.
- `structure Sim`: a function and a proof. `sim_ext` (line 304) says
  two simulations with the same function are equal, because `comm` is
  a proposition; the three category laws are then `sim_ext rfl`.
- `constSim … show t = interpK T.d t e; unfold interpK; split`: the
  left side of the square is `f (interpK C s e) = t` by definition of
  a constant, so only the right side needs work. If the target enables
  `e`, `step t e = t` by `step_halted`; if not, `interpK` returns `t`
  outright. The source controller `C` never appears.
- `sims_never_unique`: the two constants, distinguished by their value
  at any state, since `HALTED0 ≠ HALTED1` by `decide`.
- `no_initial_ctrl`: suppose `C` initial; take its unique simulation
  `u` to `fullCtrl`; both constants equal `u`, hence each other,
  contradiction. The same four lines give `no_initial_live_ctrl`,
  because `fullCtrl` is itself live.
- `StrictSim … extends Sim`: two more fields. `const_not_strict`
  (line 588): a constant to a halted state sends `genesisP`, which is
  live, to a halted state, violating `live`.
- `strict_not_unique`: the twist and erasure, distinguished at
  `DUPSTATE`, whose occurrence list `[5, 5]` has a repeat. The twist's
  square commutes because `hasDup` is preserved by every step in both
  directions (`hasDup_step`, line 634) and the step never reads the
  refusal store except when refusing (`setRef_step_comm`, line 371,
  a case split over the eleven kinds).
- `sim_pinned`: induction on the history, generalising the start
  state. In the step case, `u.comm s e` says `u.f (interpK fullK s e) =
  interpK noRefK (u.f s) e`; `interpK_full` turns the left side into
  `u.f (step s e)`, which is what `replayP` produces. This is where the
  source must be `fullCtrl`: for any other source the left side would
  be `interpK C s e`, not `step s e`, and would not match `replayP`.
- `genesis_sims_agree_on_reachable`: pin both, then both start at
  `genesisP`.
- Book `noRefine_resolves_obst5` with `noRefine_not_live`: a controller
  outside the live set clears `OBST5` by the same block. Together with
  the Python count of 512 this bounds the word "exactly" (see below).
- Book `erase_square_values`: both sides of the erasure square at a
  refuse event are `OBST5` itself: the all-on side records the refusal
  and erasure removes it; the refuse-off side ignores the event.
- Book `refTag`, `refTagSim`: on the refusal-free controller the
  refuse event is inert on both sides, so the square there is `rfl`;
  on the other ten kinds the step does not touch the refusal store
  (`refusals_step_nonrefuse`, derived from `setRef_step_comm` by
  taking the `refusals` field of both sides), so tagging commutes.
  `refTag` fixes `genesisP`, whose store is empty, and so does the
  identity.
- Book `other_pair_counterexample`: `refHist` is Unit 54's four-store
  history, funded and then refused, so the replayed state carries the
  refusal `(0, 1)`; `refTag` rewrites it to `(0, 0)` and the identity
  does not. Two genesis-preserving simulations `noRefCtrl → noRefCtrl`
  disagree on a state replayed from genesis by `replayP`.
- Book `same_under_own_replay`: replaying the same history under
  `noRefK` itself records no refusal, so there `refTag` is the identity.
  The counterexample is to the sentence as written with `replayP`; a
  reading in which "replayed" means "replayed by the source controller"
  is not what the theorem states and is not settled by this example.

## What has been proved

- `allKinds_length` (133), `mem_bools` (135), `allKinds_complete`
  (139), `interpK_full` (157): the class and its all-on member.
- `live_census` (172), `fullK_live` (175), `obst5_certified` (183),
  `tworule_executable_of_live` (190).
- `obst0_certified`, `lobst_certified` (218-219), the three
  `battery_*_nonempty` (223-225), `dead_without_addcol` (230),
  `full_resolves_obst5` (236), `dead_without_budget` (243),
  `full_resolves_obst0` (247), `dead_without_refine` (255),
  `full_resolves_lobst` (259).
- `noRefK_live`, `noRefK_ne_fullK` (271-272), `nonrefuse_agree` (280),
  `refuse_distinguishes` (286).
- `sim_ext` (304), `comp_id`, `id_comp`, `comp_assoc` (320-326); the
  eight `setRef_*` field lemmas (341-355), `wfPair_setRef`,
  `obstP_setRef`, `refineOk_setRef`, `colOk_setRef` (358-365),
  `setRef_step_comm` (371), `erase_sim` (489), `eraseRef_not_id` (493).
- `halted0_ne_halted1` (502), `const_sims_distinct` (518),
  `two_endo_sims` (527), `every_pair_connected` (536),
  `sims_never_unique` (540), `no_initial_ctrl` (551),
  `no_initial_live_ctrl` (562).
- `const_not_strict` (588), `hasDup_append_fresh` (611), `hasDup_step`
  (634), `twistRef_step` (649), `twist_step_comm` (653),
  `twist_ne_erase_at_dup` (692), `strict_not_unique` (698).
- `replay_hasDup` (708), `reachable_no_dup` (717),
  `twist_eq_erase_of_no_dup` (721), `twist_erase_agree_reachable`
  (730), `sim_pinned` (737), `genesis_sims_agree_on_reachable` (761),
  `strict_agree_on_reachable` (768).

## What has not been proved

- That "live" is the same as "clears every obstruction", or even
  "clears `OBST5`". The Lean proves sufficiency of the three bits at
  `OBST5` and necessity of each bit at one state each. At `OBST5`
  itself the budget bit is idle (budget is already 5), and 512
  controllers clear it, including non-live ones
  (`noRefine_resolves_obst5`). Audit finding 3: the docstring's
  "exactly the three response kinds" and the paper's "behaviorally
  exact" overread by this margin; a biconditional would need a
  quantification over states the module does not attempt.
- Audit finding 2: the class never toggles `assertWit`. The summary
  docstring says "ten event kinds"; the event type has eleven. The
  scoping sits in a code comment at line 100 and in the Python
  docstring, not in the summary or the paper. Every result is about
  this 1024-member class.
- Orbit agreement for any hom-set other than `fullCtrl → noRefCtrl`.
  `sim_pinned` needs `interpK_full` on the source. The ledger says so
  since 2026-08-18; the module docstring's "any two genesis-preserving
  simulations agree on every state replayed from genesis" still names
  no pair (audit finding 4). The audit record left open whether the
  unqualified sentence has a counterexample. The book supplies one for
  the pair `noRefCtrl → noRefCtrl` with "replayed" meaning `replayP`
  (`other_pair_counterexample`), and records that under replay by the
  source controller the same two maps agree (`same_under_own_replay`).
  So the sentence is false as written for that pair, and a repaired
  general statement would have to say which replay it means; none is
  proved here.
- An initial object in the category restricted to reachable states.
  Named by the paper as the boundary, not claimed.
- Audit finding 1 (categorical vocabulary): "category", "simulation",
  "initial" each name a proved law or an admitted definition; none
  labels a hidden axiom. No defect, but the reader should know that
  `Sim.f` is any function on states whatsoever. The "category" lives in
  the metatheory; the system holds 1024 finite descriptors and no
  object "the collection of all state maps".

## Outside the system

- `Sim.f : PState → PState` ranges over every function Lean can name,
  including the constants and the twist. The finitude rule flags this:
  the simulations are not represented data, and the refutation of
  initiality uses maps the kernel could never execute.
- The declared basis of six states and ten events in the Python mirror
  is the reader's probe set; `live_behavior_classes() == 128` is a
  statement about that basis.
- "Replayability, not universality" is the paper's verdict. The theorem
  behind it is `sim_pinned`, a fact about one pair; the verdict's reach
  beyond that pair is the paper's reading.

## Student exercise

`HALTED1` is `genesisP` with `occ := [0]` and `halted := true`. Write
down a third halted state, find every theorem in the module whose
statement or proof names `HALTED1`, say which of them would have to be
re-proved if the module had used your state instead, and explain why
`const_not_strict` does not depend on which halted state is chosen.

## Answer

Any state with `halted := true` and different from both, for instance
`genesisP` with `budget := 7` and `halted := true`. Five declarations
name `HALTED1`: `halted0_ne_halted1`, `const_sims_distinct`,
`sims_never_unique`, `no_initial_ctrl` and `no_initial_live_ctrl`. Only
the first two have proofs that look at the state: `halted0_ne_halted1`
is a `decide` on the two values, and `const_sims_distinct` applies
`congrArg (fun u => u.f genesisP)` and then that inequality. The other
three only pass `constSim … HALTED1 rfl` to `const_sims_distinct`; with
the name swapped they re-check unchanged, since `constSim` needs only
`t.halted = true`, which is `rfl` for any literal halted state.
`const_not_strict` is stated for an arbitrary `t` with
`t.halted = true`: it evaluates the strict map at `genesisP`, where
`live` demands a non-halted image, and `t` is halted. It never asks
which halted state `t` is, so no choice can affect it.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/ControllerCategory.lean` lines 84-139 (the class), 153-176 (all-on, live census), 178-262 (states, countermodels), 269-290 (non-uniqueness), 293-333 (category laws), 336-493 (erasure), 499-569 (constants, initiality refuted), 583-698 (strict refinement, twist), 708-774 (the orbit) |
| Axiom report | `artifacts/lean_axioms.txt` lines 593-655 |
| Paper | `paper/primitive_controller_universality.md`; `paper/paper_claim_ledger.md` `CL-PD2-CONTROLLER` (pair scope made explicit 2026-08-18) |
| Python | `code/derivation/controller_category.py`, `code/run_controller_category.py`, `tests/test_controller_category.py`, `artifacts/primitive_controller_category.json` |
| Audit | `textbook/audit/modules/ControllerCategory.md` findings 1-4 and section 6 |
| Check (Python) | `python textbook/checks/u58_controller_category.py`: census 1024/128, all live clear `OBST5` and 512 controllers in all (Python (book)), the three countermodels over the kernel's batteries, the all-on vs refuse-off pair, halted inertia under all 1024 (Python (book)), the twist and erasure squares, orbit agreement on six histories, report against artifact |
| Check (book Lean) | `python textbook/checks/u58_lean.py`: twenty-one book declarations plus twenty Genesis theorems kernel-checked, Lean 4.33.0 |
