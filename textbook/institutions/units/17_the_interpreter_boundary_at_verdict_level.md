# Unit 17. The interpreter boundary at verdict level

**Claim.** A reflective step reads the carried constitution code. The stated aligned roles agree; changing guards can give separating verdicts. The support-diagonal and lawful-escape results retain their separate hypotheses.

**Status:** derived (`V11` refutes aligned self-difference; `Bl` and
`openDenotationalBridge` (`TT-18o`) remain open). **Lean:**
`ResearchInterpreterVerdict.quiescent_reads_guard`,
`ResearchInterpreterVerdict.obstructed_reads_guard`,
`ResearchInterpreterVerdict.interp_not_step`,
`ResearchInterpreterVerdict.coded_member_separated`,
`ResearchInterpreterVerdict.RWorld`, `ResearchInterpreterVerdict.liftStep`,
`ResearchInterpreterVerdict.rstep`, `ResearchInterpreterVerdict.Interprets`,
`ResearchInterpreterVerdict.Quotes`,
`ResearchInterpreterVerdict.lawful_unique_at`,
`ResearchInterpreterVerdict.meaning`, `ResearchInterpreterVerdict.VSep`,
`ResearchInterpreterVerdict.vsep_uncoded`,
`ResearchInterpreterVerdict.identification_changes_quiescence`,
`ResearchInterpreterVerdict.coded_pair_not_vsep`,
`ResearchInterpreterVerdict.aligned_coded_equals_uncoded`,
`ResearchInterpreterVerdict.aligned_no_verdict`,
`ResearchInterpreterVerdict.vsep_uncoded_iff`,
`ResearchInterpreterVerdict.guardsPass`,
`ResearchInterpreterVerdict.codes_agree_of_guardsPass`,
`ResearchInterpreterVerdict.codes_separated_needs_guard`,
`ResearchInterpreterVerdict.genesis_witness_unguarded_not_wf`,
`ResearchInterpreterVerdict.wf_interpStep`,
`ResearchInterpreterVerdict.accWorld`,
`ResearchInterpreterVerdict.quiescent_reads_accept`,
`ResearchInterpreterVerdict.interp_not_step_wf`,
`ResearchInterpreterVerdict.vsep_uncoded_wf` (`interpreter_verdict`);
`Diagonal.opDiag`, `Diagonal.tower_persists_operational`, `Diagonal.Lawful`,
`Diagonal.opDiag_not_lawful`, `Diagonal.lawful_escape_iff`,
`Diagonal.lawful_no_escape` (`two_theorems`). **Sources:**
`research/interpreter_verdict/lean/ResearchInterpreterVerdict.lean` lines
136–770; `research/two_theorems/lean/ResearchTwoTheorems/Diagonal.lean` lines
107–200.

In the sealed Genesis spine (`lean4/Derivation/Constitution.lean` and
`InterpreterBoundary.lean`), a `ConstitutionDesc` is a 6-boolean record of guard
toggles (`dedupAdmit`, `guardRequire`, `guardAccept`, `guardBudget`, `guardAug`,
`guardRefuse`), `interpStep : ConstitutionDesc → World → Event → World` executes
an event under those toggles, and `boundarySetting` places the coded kernel
`some kernelDesc` and the uncoded interpreter role `none` on the carrier
`Option ConstitutionDesc`. In the sealed module, two questions were left at the
level of declarations or inert `notes`:
1. At the step-function type `World → Event → World`, `arbitrary_uncoded_assignment`
   showed that `none` can be assigned any step function, and `boundarySetting`
   declared the relation `x = some kernelDesc ∧ y = none` rather than deriving
   it from verdicts.
2. In `InterpreterBoundary.lean`, the diagonal `diag` escaped any finite
   catalogue of codes by writing to the inert `notes` field of `World`.

This final unit presents the two research modules that sharpen both points and
precisely delimit their scope:
- `Diagonal.lean` (`two_theorems`) replaces the `notes`-writing diagonal with
  `opDiag`, which modifies the represented support `data` (`tower_persists_operational`),
  and then shows in Lean that `opDiag` is not `Lawful` (`opDiag_not_lawful`: it appends
  a datum on `.note 0`, which `step` never does), and that a `Lawful` function
  escapes a catalogue iff no code in the catalogue is `Lawful`
  (`lawful_escape_iff`, `lawful_no_escape`).
- `ResearchInterpreterVerdict.lean` (`interpreter_verdict`) moves to the
  reflective type `RWorld := ConstitutionDesc × World`, where the two laws
  `Interprets` and `Quotes` uniquely fix the meaning of `none` as `rstep`
  (`lawful_unique_at`), derives the apartness relation `VSep` from `quiescentB`
  verdicts (`vsep_uncoded`), shows that `VSep` is witnessed only when the
  reflective world carries a *different* code `c ≠ d` at an event where a guard
  fails (`aligned_coded_equals_uncoded`, `vsep_uncoded_iff`,
  `codes_separated_needs_guard`), and upgrades the witness from the unguarded
  self-requirement at `genesis` to the well-formedness-preserving acceptance
  guard at `accWorld` (`interp_not_step_wf`, `vsep_uncoded_wf`).

## First pass

A reflective world stores both a constitution descriptor and a world.
Its reflective step reads that stored descriptor. A lifted step that
ignores the descriptor can therefore give a different verdict.

When the coded member matches the descriptor carried by the world, the
stated aligned roles agree. Keep that aligned case separate from the
witnesses where changing a guard changes quiescence. The later support
diagonal and lawful-escape results have their own explicit hypotheses.

## Detailed claim and formal anchors

On reflective worlds `RWorld := ConstitutionDesc × World`, the two
sealed laws `Interprets` and `Quotes` uniquely fix the reflective step `rstep`
at every point without function extensionality (`lawful_unique_at`), whereas any
step function `s : World → Event → World` lifted to `RWorld` ignores the carried
code and disagrees with `rstep` on quiescence at `genesis` under `.require 0 0`
(`quiescent_reads_guard`, `interp_not_step`) and at the well-formed reached
world `accWorld` under `.mark [0] 1` with both outcomes well-formed
(`quiescent_reads_accept`, `interp_not_step_wf`, `vsep_uncoded_wf`). Identifying
the uncoded role `none` with any coded member `some d` or lifted step function
changes a quiescence verdict (`identification_changes_quiescence`), while at an
aligned world `(d, w)` carrying `d` itself the coded member `some d` and the
uncoded role `none` are definitionally equal (`aligned_coded_equals_uncoded`,
`vsep_uncoded_iff`), and two codes can differ on quiescence at `(w, e)` only
when a kernel guard fails (`codes_agree_of_guardsPass`,
`codes_separated_needs_guard`). Alongside this, on `World → Event → World` the
support-level diagonal `opDiag` misses every finite catalogue on represented
support (`tower_persists_operational`) by violating the declared transition
(`opDiag_not_lawful`), and a `Lawful` function escapes a catalogue iff no code
in the catalogue is `Lawful` (`lawful_escape_iff`, `lawful_no_escape`).

## What you need first

From the sealed Genesis spine (`lean4/Derivation/NoOutside.lean`,
`Constitution.lean`, `InterpreterBoundary.lean`, `PrimitiveCore.lean`):
- `World` has fields `data`, `views`, `reqs`, `refusals`, `budget`,
  `augLicensed`, and `notes`; `supp w` projects all fields except `notes`.
- `quiescentB w` tests whether every requirement `(i, j) ∈ w.reqs` is either
  separated by `w.views` or recorded in `w.refusals`; `obstructedB w (i, j)`
  tests whether `(i, j)` is required, unseparated, and unrepairable under the
  current budget and licence; `WF w` requires `i ≠ j` and `i, j < w.data.length`
  for every `(i, j) ∈ w.reqs`.
- `ConstitutionDesc` has 6 boolean fields (`dedupAdmit`, `guardRequire`,
  `guardAccept`, `guardBudget`, `guardAug`, `guardRefuse`); `kernelDesc` sets
  all 6 to `true`, and `interp_describe` shows `interpStep kernelDesc w e =
  step w e`.

### 1. The operational diagonal and `Lawful` step functions (`two_theorems`)

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Diagonal.lean lines 107–142
def opDiag {C : Type} (cs : List C) (ev : C → World → Event → World)
    (w : World) (e : Event) : World :=
  (cs[w.data.length]?).elim w
    (fun c => { ev c w e with data := (ev c w e).data ++ [0] })

theorem tower_persists_operational {C : Type} (cs : List C)
    (ev : C → World → Event → World) :
    ∃ f : World → Event → World, ∀ c ∈ cs,
      ∃ w e, supp (f w e) ≠ supp (ev c w e) := by ...

def Lawful (f : World → Event → World) : Prop :=
  ∀ w e, supp (f w e) = supp (step w e)

theorem step_lawful : Lawful step := fun _ _ => rfl
```

At a world `w` whose `w.data.length` indexes a code `c` in `cs`, `opDiag cs ev w e`
runs `ev c w e` and appends `0` to `data`, so its support `supp` differs from
`ev c w e` (`tower_persists_operational`). A function `f : World → Event → World`
is `Lawful` when it agrees with the sealed transition `step` on `supp` at every
world and event.

### 2. Reflective worlds and the two laws (`interpreter_verdict`)

```lean
-- Lean (research), research/interpreter_verdict/lean/ResearchInterpreterVerdict.lean lines 208–247, 291–299
abbrev RWorld := ConstitutionDesc × World

def liftStep (s : World → Event → World) : RWorld → Event → RWorld :=
  fun p e => (p.1, s p.2 e)

def rstep : RWorld → Event → RWorld :=
  fun p e => (p.1, interpStep p.1 p.2 e)

def Interprets (g : RWorld → Event → RWorld) : Prop :=
  ∀ (c : ConstitutionDesc) (w : World) (e : Event),
    (g (c, w) e).2 = interpStep c w e

def Quotes (g : RWorld → Event → RWorld) : Prop :=
  ∀ (c : ConstitutionDesc) (w : World) (e : Event), (g (c, w) e).1 = c

theorem lawful_unique_at (g : RWorld → Event → RWorld)
    (h1 : Interprets g) (h2 : Quotes g)
    (c : ConstitutionDesc) (w : World) (e : Event) :
    g (c, w) e = rstep (c, w) e := by
  calc g (c, w) e = ((g (c, w) e).1, (g (c, w) e).2) := rfl
    _ = (c, interpStep c w e) := by rw [h1 c w e, h2 c w e]

def meaning : Option ConstitutionDesc → RWorld → Event → RWorld
  | some d => liftStep (interpStep d)
  | none => rstep

def VSep (x y : Option ConstitutionDesc) : Prop :=
  ∃ (p : RWorld) (e : Event),
    quiescentB (meaning x p e).2 ≠ quiescentB (meaning y p e).2
```

On `RWorld := ConstitutionDesc × World`, a coded member `some d` runs `d`
ignoring the carried code (`liftStep (interpStep d)`), while the uncoded role
`none` runs `rstep`, the unique reflective step satisfying both `Interprets`
and `Quotes` (`lawful_unique_at`). Two elements `x, y : Option ConstitutionDesc`
are verdict-separated (`VSep x y`) when their meanings disagree on `quiescentB`
at some `(p, e)`.

## The theorems

First, why `opDiag` is not `Lawful`, and when a `Lawful` function escapes a
catalogue:

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Diagonal.lean lines 161–200
theorem opDiag_not_lawful {C : Type} (c : C) (cs : List C)
    (ev : C → World → Event → World) : ¬ Lawful (opDiag (c :: cs) ev) := by ...

theorem lawful_escape_iff {C : Type} (cs : List C)
    (ev : C → World → Event → World) :
    (∃ f, Lawful f ∧ ∀ c ∈ cs, ∃ w e, supp (f w e) ≠ supp (ev c w e)) ↔
      (∀ c ∈ cs, ∃ w e, supp (ev c w e) ≠ supp (step w e)) := by ...

theorem lawful_no_escape {C : Type} (cs : List C)
    (ev : C → World → Event → World) {c₀ : C} (hc : c₀ ∈ cs)
    (hev : Lawful (ev c₀)) (f : World → Event → World) (hf : Lawful f) :
    ¬ ∀ c ∈ cs, ∃ w e, supp (f w e) ≠ supp (ev c w e) := by ...
```

Second, verdict separation at `genesis`, `VSep`, and identification changes
quiescence:

```lean
-- Lean (research), research/interpreter_verdict/lean/ResearchInterpreterVerdict.lean lines 136–180, 319–320, 387–396, 431–432
theorem quiescent_reads_guard (c : ConstitutionDesc) :
    quiescentB (interpStep c genesis (.require 0 0)) = c.guardRequire := by ...

theorem obstructed_reads_guard (c : ConstitutionDesc) :
    obstructedB (interpStep c genesis (.require 0 0)) (0, 0) =
      !c.guardRequire := by ...

theorem interp_not_step (s : World → Event → World) :
    ∃ c : ConstitutionDesc,
      quiescentB (interpStep c genesis (.require 0 0)) ≠
        quiescentB (s genesis (.require 0 0)) := by ...

theorem coded_member_separated (d : ConstitutionDesc) :
    quiescentB (interpStep (flipGuard d) genesis (.require 0 0)) ≠
      quiescentB (interpStep d genesis (.require 0 0)) := by ...

theorem vsep_uncoded (d : ConstitutionDesc) : VSep (some d) none :=
  ⟨(flipGuard d, genesis), .require 0 0, (coded_member_separated d).symm⟩

theorem identification_changes_quiescence
    (I : Option ConstitutionDesc → RWorld → Event → RWorld)
    (hI : Reading I) (d : ConstitutionDesc)
    (hid : ∀ (p : RWorld) (e : Event), I none p e = I (some d) p e) :
    ∃ (p : RWorld) (e : Event),
      quiescentB (I none p e).2 ≠ quiescentB (rstep p e).2 := by ...

theorem coded_pair_not_vsep (d : ConstitutionDesc) :
    ¬ VSep (some d) (some (flipDedup d)) := by ...
```

Third, alignment, kernel guards, and the well-formedness-preserving witness at
`accWorld`:

```lean
-- Lean (research), the same file, lines 534–627, 654–660, 674–676, 706–770
theorem aligned_coded_equals_uncoded (d : ConstitutionDesc) (w : World)
    (e : Event) :
    meaning (some d) (d, w) e = meaning none (d, w) e := rfl

theorem aligned_no_verdict {β : Type} (d : ConstitutionDesc) (w : World)
    (e : Event) (q : RWorld → β) :
    q (meaning (some d) (d, w) e) = q (meaning none (d, w) e) := rfl

theorem vsep_uncoded_iff (d : ConstitutionDesc) :
    VSep (some d) none ↔
      ∃ (c : ConstitutionDesc) (w : World) (e : Event),
        c ≠ d ∧ quiescentB (interpStep d w e) ≠ quiescentB (interpStep c w e) := by ...

theorem codes_agree_of_guardsPass (c : ConstitutionDesc) (w : World)
    (e : Event) (h : guardsPass w e = true) :
    interpStep c w e = step w e := by ...

theorem codes_separated_needs_guard (c d : ConstitutionDesc) (w : World)
    (e : Event)
    (h : quiescentB (interpStep c w e) ≠ quiescentB (interpStep d w e)) :
    guardsPass w e = false := by ...

theorem genesis_witness_unguarded_not_wf (c : ConstitutionDesc)
    (h : c.guardRequire = false) :
    ¬ WF (interpStep c genesis (.require 0 0)) := by ...

theorem wf_interpStep (c : ConstitutionDesc) {w : World} (hwf : WF w)
    (e : Event) (hreq : ∀ i j, e = .require i j → c.guardRequire = true) :
    WF (interpStep c w e) := by ...

def accWorld : World :=
  { data := [0, 1], views := [[0]], reqs := [(0, 1)], refusals := [],
    budget := 1, augLicensed := true, notes := [] }

theorem quiescent_reads_accept (c : ConstitutionDesc) :
    quiescentB (interpStep c accWorld (.mark [0] 1)) = c.guardAccept := by ...

theorem interp_not_step_wf (s : World → Event → World) :
    ∃ c : ConstitutionDesc,
      WF (interpStep c accWorld (.mark [0] 1)) ∧
        quiescentB (interpStep c accWorld (.mark [0] 1)) ≠
          quiescentB (s accWorld (.mark [0] 1)) := by ...

theorem vsep_uncoded_wf (d : ConstitutionDesc) :
    ∃ (c : ConstitutionDesc) (w : World) (e : Event),
      WF w ∧ WF (interpStep d w e) ∧ WF (interpStep c w e) ∧
        quiescentB (interpStep d w e) ≠ quiescentB (interpStep c w e) := by ...
```

## The proof, step by step

**Step 1. `opDiag_not_lawful` and `lawful_escape_iff`.**
At `indexWorld 0` (where `data = []`) and `.note 0`, `step` leaves `data`
empty (`step_note_data`), whereas `opDiag (c :: cs) ev` appends `0` to `data`
(`opDiag_appends`), so their `data.length` values disagree (`opDiag_not_lawful`).
If `f` is `Lawful`, then `supp (f w e) = supp (step w e)` everywhere, so `f`
differs from `ev c` on `supp` for all `c ∈ cs` iff `step` itself differs from
`ev c` on `supp` for all `c ∈ cs` (`lawful_escape_iff`). In particular, if any
`c₀ ∈ cs` implements `step` on `supp` (`Lawful (ev c₀)`), no `Lawful` function
escapes `cs` (`lawful_no_escape`).

**Step 2. `quiescent_reads_guard`, `interp_not_step`, and `vsep_uncoded`.**
At `genesis`, `.require 0 0` is blocked when `c.guardRequire = true` (leaving
`reqs = []`, so `quiescentB = true`) and recorded when `c.guardRequire = false`
(putting `(0, 0)` into `reqs`, which no view can separate, so `quiescentB =
false`). Given any `s : World → Event → World`, choosing `c` with
`c.guardRequire = !(quiescentB (s genesis (.require 0 0)))` forces
`interpStep c genesis (.require 0 0)` and `s genesis (.require 0 0)` to disagree
on `quiescentB` (`interp_not_step`). For a coded member `some d`, evaluating at
the reflective world `(flipGuard d, genesis)` under `.require 0 0` separates
`some d` from `none` (`vsep_uncoded`) and shows that reading `none` as `some d`
(or any `liftStep s`) alters a quiescence verdict
(`identification_changes_quiescence`). Meanwhile, `dedupAdmit` never affects
`quiescentB`, so `¬ VSep (some d) (some (flipDedup d))` (`coded_pair_not_vsep`).

**Step 3. Alignment and kernel guards (`aligned_coded_equals_uncoded`, `vsep_uncoded_iff`, `codes_separated_needs_guard`).**
At `(d, w)`, `meaning (some d) (d, w) e = (d, interpStep d w e) =
meaning none (d, w) e` by `rfl` (`aligned_coded_equals_uncoded`). Thus
`VSep (some d) none` is witnessed at `(c, w)` only when `c ≠ d`
(`vsep_uncoded_iff`). Furthermore, whenever `guardsPass w e = true`, every code
`c` executes the exact same transition `step w e` (`codes_agree_of_guardsPass`),
so two codes can differ on `quiescentB` at `(w, e)` only when
`guardsPass w e = false` (`codes_separated_needs_guard`).

**Step 4. Well-formedness at `accWorld` (`quiescent_reads_accept`, `interp_not_step_wf`, `vsep_uncoded_wf`).**
At `genesis`, `.require 0 0` with `guardRequire = false` produces an ill-formed
world because `(0, 0) ∈ reqs` violates `0 ≠ 0` (`genesis_witness_unguarded_not_wf`).
By contrast, `wf_interpStep` shows that every event other than an unguarded
`.require` preserves `WF`. The world `accWorld`—reached from `genesis` in 5
kernel steps (`accWorld_reached`) and satisfying `WF accWorld` (`accWorld_wf`)—has
`data = [0, 1]`, `views = [[0]]`, `reqs = [(0, 1)]`, and `budget = 1`. At event
`.mark [0] 1`, `markOkB accWorld [0] 1 = false` (`guardsPass = false`). A code
with `guardAccept = true` rejects the mark and stays quiescent (`quiescentB =
true`); a code with `guardAccept = false` adds `1` to `[0]`, collapsing `(0, 1)`
and making `quiescentB = false` (`quiescent_reads_accept`), while both output
worlds satisfy `WF` (`accWorld_outputs_wf`). Flipping `guardAccept` therefore
separates `interpStep` from every `s` (`interp_not_step_wf`) and `none` from
`some d` (`vsep_uncoded_wf`) with all worlds well-formed.

## The same fact in Python

The check verifies:

1. Pin and import parity for `research/interpreter_verdict/model.py` (`consumed_modules`
   vs `lean_imports`).
2. `diagonal_checks` and `self_evaluator_check` from `two_theorems/model.py`.
3. A direct finite Python check over all `2^6 = 64` codes `c ∈ ConstitutionDesc`:
   - at `genesis` under `require(0, 0)`, `quiescentB(interpStep(c, genesis,
     require(0, 0))) == c.guardRequire`;
   - at `accWorld` under `mark([0], 1)`, `quiescentB(interpStep(c, accWorld,
     mark([0], 1))) == c.guardAccept` and `WF` holds for all 64 output worlds;
   - at every aligned pair `(d, w)`, `meaning(some(d), (d, w), e) ==
     meaning(none, (d, w), e)`;
   - for all 64 codes `d`, `flipDedup(d) != d` has identical `quiescentB` across
     all events (`coded_pair_not_vsep`), while `flipAccept(d)` separates
     `some(d)` from `none` at `(flipAccept(d), accWorld)` with well-formed
     worlds (`vsep_uncoded_wf`).

```
python textbook/institutions/checks/i17_interpreter_verdict.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `cases` on the 6 booleans of `ConstitutionDesc`, `decide` | `quiescent_reads_guard`, `quiescent_reads_accept`, `accWorld_reached`, `accWorld_wf` | finite case exhaustion over `2^6 = 64` codes and kernel evaluation |
| `rfl` | `lawful_unique_at` (with `rw`), `aligned_coded_equals_uncoded`, `aligned_no_verdict` | definitional equality; `lawful_unique_at` uses no `funext` |
| `List.getElem?_of_mem`, `omega` | `tower_persists_operational`, `opDiag_not_lawful` | list indexing and length arithmetic in `Diagonal.lean` |

**What the system holds.** Finite `ConstitutionDesc` 6-tuples, finite `World`
records, pairs `RWorld := ConstitutionDesc × World`, and `Option ConstitutionDesc`.

**Admissions relied on, and their price.**
1. In `ResearchInterpreterVerdict.lean`, the reflective state is typed as
   `RWorld := ConstitutionDesc × World` and constrained by the two laws
   `Interprets` and `Quotes` (`V4`). Moreover, the retention and protected-demand
   stores of `verdictBoundary` are declared as `VSep` (`V6`), and the local
   condition `PrimitiveCore.Bl` remains open (`Bl` in `CLAIMS.md`).
2. In `Diagonal.lean`, `opDiag` escapes finite catalogues only by stepping
   outside `Lawful` (`opDiag_not_lawful`, `lawful_no_escape`, `TT-18L`), and
   `openDenotationalBridge` (whether a lawful internal bridge can evaluate every
   coded family without diagonal escape) remains open (`TT-18o`).

**Phrases to read with care.**

- "The uncoded role `none` is separated from every coded member `some d`."
  At the aligned world `(d, w)` carrying `d` itself, `some d` and `none` produce
  the *exact same* outcome (`aligned_coded_equals_uncoded`, `V11`). Their
  separation `VSep (some d) none` holds solely because `none` (`rstep`) also
  interprets *other* codes `c ≠ d` at worlds `(c, w)` when a guard fails
  (`vsep_uncoded_iff`, `codes_separated_needs_guard`, `V9`, `V11`).
- "The operational diagonal escapes every finite catalogue." `opDiag` is an
  unrestricted function `World → Event → World`, not a `Lawful` transition
  (`opDiag_not_lawful`). Against any catalogue containing `kernelDesc` (for
  which `interpStep kernelDesc = step` is `Lawful`), no `Lawful` function
  escapes (`lawful_no_escape`).

## What it shows, and what it does not

It shows that on `RWorld := ConstitutionDesc × World`, `Interprets` and `Quotes`
uniquely determine `rstep` at every world and event without `funext`
(`lawful_unique_at`), and that `VSep` separates `none` from every `some d` both
at `genesis` (`vsep_uncoded`) and at the well-formed reached world `accWorld`
with well-formed outcomes (`vsep_uncoded_wf`, `interp_not_step_wf`).

It shows that `some d` and `none` coincide at every aligned world `(d, w)`
(`aligned_coded_equals_uncoded`, refuting any self-representational difference at
aligned states, `V11`), that two codes can differ on quiescence only when
`guardsPass w e = false` (`codes_separated_needs_guard`, `V9`), and that `VSep`
is strictly coarser than `≠` (`coded_pair_not_vsep`, `V8`).

It shows that `opDiag` escapes finite catalogues on `supp` by violating `Lawful`
(`opDiag_not_lawful`), and that a `Lawful` function escapes a catalogue iff the
catalogue contains no `Lawful` code (`lawful_escape_iff`).

It does not close `PrimitiveCore.Bl` (`Bl` in `interpreter_verdict/CLAIMS.md`)
or `openDenotationalBridge` (`TT-18o` in `two_theorems/CLAIMS.md`); both remain
open.

## Sources

| Item | Where |
|---|---|
| `quiescent_reads_guard`, `obstructed_reads_guard`, `flipGuard`, `interp_not_step`, `coded_member_separated` | `research/interpreter_verdict/lean/ResearchInterpreterVerdict.lean` lines 136–188 |
| `RWorld`, `liftStep`, `rstep`, `Interprets`, `Quotes`, `lawful_unique_at`, `rstep_not_lift` | the same file, lines 208–284 |
| `meaning`, `VSep`, `vsep_uncoded`, `verdictBoundary`, `identification_changes_quiescence`, `coded_pair_not_vsep` | the same file, lines 291–444 |
| `aligned_coded_equals_uncoded`, `aligned_no_verdict`, `vsep_uncoded_iff`, `guardsPass`, `codes_agree_of_guardsPass`, `codes_separated_needs_guard` | the same file, lines 534–627 |
| `genesis_witness_unguarded_not_wf`, `wf_interpStep`, `accWorld`, `quiescent_reads_accept`, `interp_not_step_wf`, `vsep_uncoded_wf` | the same file, lines 654–770 |
| `opDiag`, `tower_persists_operational`, `Lawful`, `opDiag_not_lawful`, `lawful_escape_iff`, `lawful_no_escape` | `research/two_theorems/lean/ResearchTwoTheorems/Diagonal.lean` lines 107–200 |
| Python mirrors | `research/interpreter_verdict/model.py` lines 15–45; `research/two_theorems/model.py` lines 484–518 (`diagonal_checks`, `self_evaluator_check`) |
| Check | `textbook/institutions/checks/i17_interpreter_verdict.py` |
| Ledger | `research/interpreter_verdict/CLAIMS.md` V1–V11, Bl (open); `research/two_theorems/CLAIMS.md` TT-18, TT-18L, TT-18o (open) |
