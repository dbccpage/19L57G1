# Unit 17. The interpreter boundary at verdict level

**Claim.** The reflective step reads a carried guard code. Aligned coded and
reflective roles agree. Guard-changing separation witnesses and lawful
escape results have separate assumptions; the general semantic bridge
remains open.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** A reflective step reads the carried constitution code. The stated aligned roles agree; changing guards can give separating verdicts. The support-diagonal and lawful-escape results retain their separate hypotheses.

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
toggles (`dedupAdmit`, `guardRequire`, `guardAccept`, `gateBudget`, `gateLicense`,
`certRefusal`), `interpStep : ConstitutionDesc → World → Event → World` executes
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
  a datum on `.note 0`, which `step` never does), and gives the explicit
  per-entry support-difference witness criterion for lawful escape
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

**Earlier orientation.**

A reflective world stores both a constitution descriptor and a world.
Its reflective step reads that stored descriptor. A lifted step that
ignores the descriptor can therefore give a different verdict.

When the coded member matches the descriptor carried by the world, the
stated aligned roles agree. Keep that aligned case separate from the
witnesses where changing a guard changes quiescence. The later support
diagonal and lawful-escape results have their own explicit hypotheses.

**Further formal anchors.**

On reflective worlds `RWorld := ConstitutionDesc × World`, the two
supplied research-model laws `Interprets` and `Quotes` uniquely fix the reflective step `rstep`
at every point without function extensionality (`lawful_unique_at`), whereas any
step function `s : World → Event → World` lifted to `RWorld` ignores the carried
code and disagrees with `rstep` on quiescence at `genesis` under `.require 0 0`
(`quiescent_reads_guard`, `interp_not_step`) and at the well-formed reached
world `accWorld` under `.mark [0] 1` with the interpreter output
well-formed (`quiescent_reads_accept`, `interp_not_step_wf`). The coded-pair
witness has both outputs well-formed (`vsep_uncoded_wf`); no such guarantee
is made about an arbitrary s's output. Identifying
the uncoded role `none` with any coded member `some d` or lifted step function
changes a quiescence verdict (`identification_changes_quiescence`), while at an
aligned world `(d, w)` carrying `d` itself the coded member `some d` and the
uncoded role `none` are definitionally equal (`aligned_coded_equals_uncoded`,
`vsep_uncoded_iff`), and two codes can differ on quiescence at `(w, e)` only
when a kernel guard fails (`codes_agree_of_guardsPass`,
`codes_separated_needs_guard`). Alongside this, on `World → Event → World` the
support-level diagonal `opDiag` misses every finite catalogue on represented
support (`tower_persists_operational`) by violating the declared transition
(`opDiag_not_lawful`), and lawful escape has an explicit support-difference witness for each
catalogue entry (`lawful_escape_iff`, `lawful_no_escape`).

</details>

## First pass

A world carries a code specifying which guards to apply. Compare
a step fixed to code A with a reflective step that reads the carried code.
When the world carries A, these roles execute the same coded step.

When it carries another code B, a guard difference can matter. For
example, an acceptance guard can reject a mark that would destroy a
protected distinction; a relaxed code can accept it. The resulting
quiescence verdicts can differ at the stated witness.

The separating comparison therefore changes the code being executed.
It does not show a step differing from itself on the same input.

**Predict:** does escaping a finite catalogue by an arbitrary function
prove that a lawful step can also escape it?

<details><summary>Check your prediction</summary>

No. The support-changing diagonal is proved not lawful under this
definition. The lawful-escape theorem has its own catalogue hypotheses.
The lesson keeps those results separate from the open denotational bridge.

</details>

After this Unit, try the
[acquisition, changing-view and interpreter practice](../../reading_formal_practice.md#acquisition-changing-views-and-interpreters-i12i17)
before opening its separate answer page.

Quoted proofs below sometimes use `...` for omitted lines. Those
excerpts are not runnable Lean; the cited owner files contain the full proofs.

## What you need first

Recall the represented-world model from the Change lab and I16’s
difference between changing an existing view and appending a view.
Here, first read a guard as a supplied Yes/No setting that changes
whether an event is accepted. The optional names identify its owners.

<details>
<summary>Prerequisite source names (optional)</summary>

From the sealed Genesis spine (`lean4/Derivation/NoOutside.lean`,
`Constitution.lean`, `InterpreterBoundary.lean`, `PrimitiveCore.lean`):
- `World` has fields `data`, `views`, `reqs`, `refusals`, `budget`,
  `augLicensed`, and `notes`; `supp w` projects all fields except `notes`.
- `quiescentB w` tests whether every recorded requirement is separated
  by `w.views`. A refusal record does not satisfy an unmet requirement.
  `obstructedB w (i,j)` additionally checks exhaustion of the defined
  repair menu; budget and licence separately gate event execution.
  `WF w` checks distinct, in-range endpoints for each recorded requirement.
- `ConstitutionDesc` has 6 boolean fields (`dedupAdmit`, `guardRequire`,
  `guardAccept`, `gateBudget`, `gateLicense`, `certRefusal`); `kernelDesc` sets
  all 6 to `true`, and `interp_describe` shows `interpStep kernelDesc w e =
  step w e`.


</details>

### Name the two comparisons

A represented world records input tokens, Yes/No views, protected pairs,
refusals, a budget, a licence flag and notes. Views and requirements use
input positions. A reflective world additionally carries a six-bit guard
code. A fixed coded role uses its chosen code; the reflective role reads
the code carried by the world. The tag `none` is assigned that reflective
role by the supplied model laws. Its spelling alone derives no interpreter.

Compare fixed code A with the reflective role. At a world carrying A,
both execute A and give exactly the same result. At a world carrying B,
the reflective role executes B instead. A difference there compares
different guard settings, not a function with itself on the same input.

### Work one guard example

The reached world `accWorld` has two inputs 0,1, one view `{0}`, protected
pair 0/1 and enough budget for the mark. Try adding input 1 to that view:

| Acceptance guard | Resulting view | Pair 0/1 separated? | Quiescent? |
|---|---|---|---|
| On | `{0}` | Yes | Yes |
| Off | `{0,1}` | No | No |

The guarded code rejects this mark; the relaxed code accepts it.
Quiescent means every protected pair is currently separated. A refusal
record does not settle an unresolved pair. Neither quiescence nor a
guarded acceptance is a measurement of empirical correctness.

Both output worlds satisfy `WF`: their recorded pair still has distinct,
in-range endpoints. `WF` does not require that pair to be separated.
Thus a well-formed world can have an unmet requirement. For an arbitrary
comparison function s, `interp_not_step_wf` guarantees the chosen
interpreter output is well-formed; it makes no such guarantee about s’s
arbitrary output. The two *coded* outputs in `vsep_uncoded_wf` are both
well-formed.

### Keep the quantifiers in order

For each fixed step function s that ignores the carried code, a code
can be chosen whose guard verdict differs from s at the witness.
The chosen code may depend on s. The theorem does not give one fixed
code that differs from every s; taking s to be that code’s own step
would immediately defeat such a claim.

Distinct descriptors need not give distinct quiescence verdicts.
Changing the deduplication bit can change a stored list while leaving
this particular verdict unchanged. The separation relation `VSep`
asks for a verdict difference at some world/event, rather than mere
inequality of records.

### What the operational diagonal changes

A finite catalogue lists coded step functions. At a world whose input
count selects a catalogue entry, `opDiag` runs that entry and appends
one extra datum. Its result therefore differs from the selected entry
on represented support. The witness world may depend on the entry.

Here **support** includes all world fields except notes. **Lawful**
requires agreement with the declared kernel step on that support at
every world and event. Notes may still differ. This is a different
condition from `WF` and from the reflective laws `Interprets`/`Quotes`.
For a nonempty catalogue, the diagonal violates it by appending a datum
under a note event. The kernel’s note event keeps the data unchanged.

The constructive lawful-escape criterion requires, for each catalogue
entry, a particular world/event where it differs from the kernel on
support. Then the kernel step itself escapes the catalogue. If even
one entry agrees with the kernel everywhere on support, no Lawful
function can escape it. This states the witness condition directly;
it does not silently replace it with a general “not equal implies a
known differing input” principle.

The result is about this supplied catalogue, support projection and
transition rule. It does not prove that an arbitrary physical observer
escapes every description, or close the open semantic bridge.

### 1. The operational diagonal and `Lawful` step functions (`two_theorems`)

<details>
<summary>Quoted source 1 (optional)</summary>

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

</details>

At a world `w` whose `w.data.length` indexes a code `c` in `cs`, `opDiag cs ev w e`
runs `ev c w e` and appends `0` to `data`, so its support `supp` differs from
`ev c w e` (`tower_persists_operational`). A function `f : World → Event → World`
is `Lawful` when it agrees with the sealed transition `step` on `supp` at every
world and event.

### 2. Reflective worlds and the two laws (`interpreter_verdict`)

<details>
<summary>Quoted source 2 (optional)</summary>

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

</details>

On `RWorld := ConstitutionDesc × World`, a coded member `some d` runs `d`
ignoring the carried code (`liftStep (interpStep d)`), while the uncoded role
`none` runs `rstep`, the unique reflective step satisfying both `Interprets`
and `Quotes` (`lawful_unique_at`). Two elements `x, y : Option ConstitutionDesc`
are verdict-separated (`VSep x y`) when their meanings disagree on `quiescentB`
at some `(p, e)`.

## The theorems

First, why `opDiag` is not `Lawful`, and when a `Lawful` function escapes a
catalogue:

<details>
<summary>Quoted source 3 (optional)</summary>

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

</details>

Second, verdict separation at `genesis`, `VSep`, and identification changes
quiescence:

<details>
<summary>Quoted source 4 (optional)</summary>

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

</details>

Third, alignment, kernel guards, and the well-formedness-preserving witness at
`accWorld`:

<details>
<summary>Quoted source 5 (optional)</summary>

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

</details>

## Why the claims work

The two supplied reflective laws fix the carried code and the world
output, so they fix the resulting pair. At matching codes the roles
therefore agree. At the acceptance witness, switching one guard changes
whether a protected distinction survives. The separate diagonal adds
a datum to force a support difference, and the note-event witness shows
why that function violates Lawful. Each result retains its own premises.

<details>
<summary>Detailed proof steps (optional)</summary>

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
provides the coded-pair witness for `none` versus `some d`
(`vsep_uncoded_wf`) with both outputs well-formed. For each arbitrary
comparison function s, `interp_not_step_wf` chooses a guard based on s's
verdict; only the chosen interpreter output is guaranteed well-formed.

</details>

## The same fact in Python

The check verifies:

1. Import-list parity for `research/interpreter_verdict/model.py`
   (`consumed_modules` vs `lean_imports`); snapshot hashes and custody
   receipts are not revalidated by this comparison.
2. `diagonal_checks` and `self_evaluator_check` from `two_theorems/model.py`.
3. A direct finite Python check over all `2^6 = 64` codes `c ∈ ConstitutionDesc`:
   - at `genesis` under `require(0, 0)`, `quiescentB(interpStep(c, genesis,
     require(0, 0))) == c.guardRequire`;
   - at `accWorld` under `mark([0], 1)`, `quiescentB(interpStep(c, accWorld,
     mark([0], 1))) == c.guardAccept` and `WF` holds for all 64 output worlds;
   - at the one aligned `accWorld`/mark example for each code, the checker
     constructs the same native transition on both sides. This is a
     definitional sanity check, not exhaustive coverage of reflective
     worlds or an independent test of arbitrary meaning functions;
   - for all 64 codes, the finite deduplication comparison uses the four
     listed events and two sample worlds. The general result is the Lean
     theorem `coded_pair_not_vsep`. The acceptance-bit comparison separates
     `some(d)` from `none` at `(flipAccept(d), accWorld)` with well-formed
     worlds (`vsep_uncoded_wf`).

```
python textbook/institutions/checks/i17_interpreter_verdict.py
```

The checker now calls `derivation.completion.interp_step` and
`derivation.represented` directly. Its former copied helper counted a
refusal as resolution, used token membership for a position bound, and
appended marks instead of prepending them. The original samples did not
expose those differences. Added cases check a refused-but-unseparated pair,
tokens [10,20,30] with valid position 1, duplicate marks under a relaxed
guard, empty genesis, and structural obstruction independent of funding.
The changed-code comparison is also exercised rather than only described.
These are finite Python checks, not new Lean proofs.

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

For a nonempty catalogue, `opDiag` escapes on `supp` by violating
`Lawful` (`opDiag_not_lawful`). The constructive lawful-escape criterion
is a support-difference witness from the kernel for each entry
(`lawful_escape_iff`); an entry agreeing with the kernel everywhere
blocks every Lawful escape. Empty-catalogue escape is vacuous and does
not imply that `opDiag` on an empty catalogue violates Lawful.

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
