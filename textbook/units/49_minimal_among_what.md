# Unit 49. Minimal among what? A six-probe singleton in a 64-member class

**Claim.** Among the declared 64 guard-toggle descriptors, exactly one passes the six stated probes. This is uniqueness within a finite comparison class and test battery.

**Status:** VERIFIED_FINITE, class- and
battery-relative; categorical initiality is not claimed and the
terminal was renamed to say so. **Lean:** `lean4/Derivation/Initiality.lean`
lines 52-169, imports `Constitution` and `NoOutside`. **Axioms:**
`retract_section` none; the other ten `{propext, Quot.sound}`.
**Depends on:** Unit 48 (`ConstitutionDesc`, `interpStep`,
`kernelDesc`, `allDescs`, `allDescs_complete`), Unit 47 (`CWorld`,
`stepC`, `replayC`), Unit 45 (the sealed theorems the probes
instantiate).

## First pass

A probe supplies one world and one event, then checks the resulting behavior. Each of the six probes targets one guard.

Passing all six identifies one descriptor in the declared list of 64. It does not compare every possible controller or establish categorical initiality.

## Detailed claim and formal anchors

`Initiality` declares a comparison class, the 64 descriptors
of Unit 48 run by the family interpreter, and a compliance battery of
six probes, one per guard, each a single world and event on which the
sealed kernel is a no-op.

Switching any one guard off fails its probe
(`dedup_load_bearing`, `require_guard_load_bearing`,
`accept_guard_load_bearing`, `budget_gate_load_bearing`,
`license_gate_load_bearing`, `refusal_certificate_load_bearing`); the
kernel's descriptor is the unique compliant member (`unique_compliant`,
`minimum_unique_in_class`); the panel-extended kernel of Unit 47
projects back onto the kernel along every base event and history
(`extension_retract`, `extension_retract_replay`, split by
`retract_section`).

## Question

Is the kernel the most primitive engine of its kind? The question has
no answer until "its kind" is a declared set and "primitive" a declared
test. This unit declares both as small as they can be made, proves the
answer inside them, and says what the answer does not cover.

## What we already possess

- The six-bit descriptor, the family interpreter `interpStep`, and
  `interp_describe` (Unit 48); `allDescs` with its completeness.
- The sealed theorems the probes instantiate: repeated admission is
  silent, a requirement needs two distinct admitted tokens, an accepted
  mark preserves satisfied requirements, marks and views cost budget,
  views need the license, refusal needs the certificate (Unit 45).
- `CWorld`, `stepC`, `replayC` (Unit 47).

## New concept: a probe, a battery, a class

*Probe.* One world and one event on which the kernel does nothing.
`probeAccept d` asks whether `interpStep d` also does nothing on
`satWorld` under `mark [0] 1`.

*Battery.* `compliantB d` is the conjunction of the six probes.

*Class.* `allDescs`, the sixty-four descriptors. Uniqueness is
`allDescs.filter compliantB = [kernelDesc]`, decided by running every
probe on every member.

*Retract.* A projection from the extended state back to the kernel
that commutes with every base event: `(stepC cw (.base e)).base = step
cw.base e`, and by induction the same for histories.

## Plain-language interpretation

Ask whether a guard earns its place by taking it away and watching one
test. Six guards, six tests, six failures, each a concrete world on
which the relaxed machine does something the kernel refuses to do:
admits a token twice, records a requirement of a thing against itself,
accepts a mark that breaks a satisfied requirement, spends at zero,
adds a column without the license, records a refusal with no
certificate. Then run all six tests on all sixty-four settings. One
setting passes: the kernel's. Any cost you care to put on the settings
has the same minimum, because there is one candidate.

What this is: a finite, decided fact about a declared list and a
declared test. What it is not: a theorem that the kernel is minimal
among engines in general, or that a guard is needed for a sealed
theorem. "Load-bearing" means "fails its probe", and the probe is one
instance chosen so that the kernel passes. The paper renamed the
terminal from "initial kernel proved" to "unique probe-compliant
descriptor in the declared toggle class" for exactly this reason. The
retract is the other small, true thing: adding a panel to the state
and then forgetting it gives back the kernel's run, event by event,
which is what "conservative extension" meant in Unit 47.

## Pseudocode

```
dupWorld  = data [5]                       probeDedup   d = interp d dupWorld (admit 5)   == dupWorld
                                           probeRequire d = interp d dupWorld (require 0 0) == dupWorld
satWorld  = [10,20], view [0], req (0,1)   probeAccept  d = interp d satWorld (mark [0] 1)  == satWorld
brokeWorld = ..., view [], budget 0        probeBudget  d = interp d brokeWorld (mark [] 0)  == brokeWorld
unlicensed = ..., license off              probeLicense d = interp d unlicensed (addView [0]) == unlicensed
                                           probeRefusal d = interp d satWorld (refuse 0 1)   == satWorld
compliant d = all six
theorem: [d ∈ allDescs | compliant d] = [kernelDesc]
retract:  (replayC (map base h) cw).base = replay h cw.base
```

## Python

Genesis's `code/derivation/completion.py` holds `PROBES`,
`probe_results`, `compliant`, `cost_capabilities`, `cost_lex` and
`minimality_report`, whose output is
`artifacts/completion_minimality.json` (the full 64-row table).

```python
C.probe_results(C.KERNEL_DESC)               # all six True
[d for d in C.all_descs() if C.compliant(d)] # [(True, True, True, True, True, True)]
```

The check script's run:

```text
the six probes on the sealed step (each must be a no-op):
  dedup: event ('admit', 5) on [5]/[]/budget 9/licensed True: no-op True
  require_guard: event ('require', 0, 0) on [5]/[]/budget 9/licensed True: no-op True
  accept_guard: event ('mark', (0,), 1) on [10, 20]/[[0]]/budget 9/licensed True: no-op True
  budget_gate: event ('mark', (), 0) on [10, 20]/[[]]/budget 0/licensed True: no-op True
  license_gate: event ('addView', (0,)) on [10, 20]/[[]]/budget 9/licensed False: no-op True
  refusal_certificate: event ('refuse', 0, 1) on [10, 20]/[[0]]/budget 9/licensed True: no-op True
one guard off, on its probe world:
  dedup off: {'data': [5, 5], 'views': [], 'reqs': [], 'refusals': [], 'budget': 9, 'aug_licensed': True, 'notes': []}; fails ['dedup']
  require_guard off: {'data': [5], 'views': [], 'reqs': [[0, 0]], 'refusals': [], 'budget': 9, 'aug_licensed': True, 'notes': []}; fails ['require_guard']
  accept_guard off: {'data': [10, 20], 'views': [[1, 0]], 'reqs': [[0, 1]], 'refusals': [], 'budget': 8, 'aug_licensed': True, 'notes': []}; fails ['accept_guard']
  budget_gate off: {'data': [10, 20], 'views': [[0]], 'reqs': [[0, 1]], 'refusals': [], 'budget': 0, 'aug_licensed': True, 'notes': []}; fails ['budget_gate']
  license_gate off: {'data': [10, 20], 'views': [[], [0]], 'reqs': [[0, 1]], 'refusals': [], 'budget': 8, 'aug_licensed': False, 'notes': []}; fails ['license_gate']
  refusal_certificate off: {'data': [10, 20], 'views': [[0]], 'reqs': [[0, 1]], 'refusals': [[0, 1]], 'budget': 9, 'aug_licensed': True, 'notes': []}; fails ['refusal_certificate']
all 64 descriptors:
  each probe fails exactly when its guard is off: True
  passed-probe histogram {0: 1, 1: 6, 2: 15, 3: 20, 4: 15, 5: 6, 6: 1} (binomial, 1 6 15 20 15 6 1)
  compliant: [(True, True, True, True, True, True)]; is the kernel: True
  cost orders on the compliant set: capabilities [6], lexicographic [(3, 3)]; the all-off member costs 0, (0, 0)
  minimality_report() equals the artifact: True; keys ['class_size', 'compliant', 'interp_of_kernel_desc_matches_step', 'orders_agree_on_singleton', 'table', 'unique_compliant_is_kernel']
the retract (CWorld as Python (book)):
  base after the story's events through the panel kernel equals the story: True; panel untouched: True
failures: []
```

## Line-by-line Python explanation

The first block runs each probe's event on its world through the sealed
`step` and confirms a no-op: this is the calibration the module's
header describes, done in the open.

The second block switches one guard off at a time and prints the
outcome: the duplicated token, the self-requirement, the mark `1` put
on the column `[0]` (the mirror prepends, as `markApply` does) with the
budget spent, the mark at budget zero with the budget still zero (the
mirror saturates as Lean's `Nat` does), the unlicensed column, the
uncertified refusal. Each fails exactly its own probe.

The third block is stronger than the six theorems: on all sixty-four
descriptors, the set of failed probes is exactly the set of off guards.
So the probes are independent, the histogram of passed probes is the
binomial row 1 6 15 20 15 6 1, and the compliant set is the all-on
member alone. The two cost orders are printed on that singleton; the
all-off member shows the orders are not constant on the class. Then the
report is compared with the artifact.

The last block replays the story's events through a base-and-panel
pair with a one-evaluator panel and checks the base equals the story
and the panel is as it was.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Initiality.lean lines 52-90
def dupWorld : World :=
  { data := [5], views := [], reqs := [], refusals := [],
    budget := 9, augLicensed := true, notes := [] }

def satWorld : World :=
  { data := [10, 20], views := [[0]], reqs := [(0, 1)],
    refusals := [], budget := 9, augLicensed := true, notes := [] }

def brokeWorld : World :=
  { data := [10, 20], views := [[]], reqs := [(0, 1)],
    refusals := [], budget := 0, augLicensed := true, notes := [] }

def unlicensedWorld : World :=
  { data := [10, 20], views := [[]], reqs := [(0, 1)],
    refusals := [], budget := 9, augLicensed := false, notes := [] }

def probeDedup (d : ConstitutionDesc) : Bool :=
  interpStep d dupWorld (.admitTok 5) == dupWorld

def probeRequire (d : ConstitutionDesc) : Bool :=
  interpStep d dupWorld (.require 0 0) == dupWorld

def probeAccept (d : ConstitutionDesc) : Bool :=
  interpStep d satWorld (.mark [0] 1) == satWorld

def probeBudget (d : ConstitutionDesc) : Bool :=
  interpStep d brokeWorld (.mark [] 0) == brokeWorld

def probeLicense (d : ConstitutionDesc) : Bool :=
  interpStep d unlicensedWorld (.addView [0]) == unlicensedWorld

def probeRefusal (d : ConstitutionDesc) : Bool :=
  interpStep d satWorld (.refuse 0 1) == satWorld

def compliantB (d : ConstitutionDesc) : Bool :=
  probeDedup d && probeRequire d && probeAccept d && probeBudget d
    && probeLicense d && probeRefusal d
```

```lean
-- Lean (Genesis), lean4/Derivation/Initiality.lean lines 99-101, 107-109, 128-142, 154-169
theorem dedup_load_bearing :
    probeDedup { kernelDesc with dedupAdmit := false } = false ∧
      probeDedup kernelDesc = true := by decide

theorem accept_guard_load_bearing :
    probeAccept { kernelDesc with guardAccept := false } = false ∧
      probeAccept kernelDesc = true := by decide
-- and four more of the same shape, lines 103-121

theorem unique_compliant :
    allDescs.filter compliantB = [kernelDesc] := by decide

theorem minimum_unique_in_class :
    ∀ d ∈ allDescs.filter compliantB, d = kernelDesc := by
  intro d hd
  rw [unique_compliant] at hd
  cases hd with
  | head => rfl
  | tail _ h => cases h

theorem extension_retract (cw : NoOutside.CWorld) (e : Event) :
    (NoOutside.stepC cw (.base e)).base = step cw.base e := rfl

theorem extension_retract_replay (h : List Event) :
    ∀ cw : NoOutside.CWorld,
      (NoOutside.replayC (h.map .base) cw).base = replay h cw.base := by
  induction h with
  | nil => intro cw; rfl
  | cons e rest ih =>
      intro cw
      exact ih (NoOutside.stepC cw (.base e))

theorem retract_section (w : World) :
    (NoOutside.CWorld.mk w []).base = w := rfl
```

The book's Lean calibrates the probes on the sealed step, prints what
each relaxation does, shows a single toggle fails only its own probe,
derives non-compliance of a two-toggle descriptor from the uniqueness
theorem, defines a cost order (Genesis defines none in Lean) and shows
it constant on the compliant set, and runs the retract on the story.

```lean
-- Lean (book), textbook/checks/u49_lean.py
def storyH : List Event :=
  [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
   .require 0 1, .require 0 2, .require 1 2, .addView [0]]

theorem probes_are_step_noops :
    step dupWorld (.admitTok 5) = dupWorld ∧ step dupWorld (.require 0 0) = dupWorld ∧
    step satWorld (.mark [0] 1) = satWorld ∧ step brokeWorld (.mark [] 0) = brokeWorld ∧
    step unlicensedWorld (.addView [0]) = unlicensedWorld ∧
    step satWorld (.refuse 0 1) = satWorld := by decide

theorem kernel_compliant : compliantB kernelDesc = true := by decide

theorem off_outcomes :
    (interpStep { kernelDesc with dedupAdmit := false } dupWorld (.admitTok 5)).data = [5, 5] ∧
    (interpStep { kernelDesc with guardRequire := false } dupWorld (.require 0 0)).reqs = [(0, 0)] ∧
    (interpStep { kernelDesc with guardAccept := false } satWorld (.mark [0] 1)).views = [[1, 0]] ∧
    (interpStep { kernelDesc with gateBudget := false } brokeWorld (.mark [] 0)).views = [[0]] ∧
    (interpStep { kernelDesc with gateBudget := false } brokeWorld (.mark [] 0)).budget = 0 ∧
    (interpStep { kernelDesc with gateLicense := false } unlicensedWorld (.addView [0])).views =
      [[], [0]] ∧
    (interpStep { kernelDesc with certRefusal := false } satWorld (.refuse 0 1)).refusals =
      [(0, 1)] := by decide

theorem accept_off_breaks :
    satB satWorld (0, 1) = true ∧
    satB (interpStep { kernelDesc with guardAccept := false } satWorld (.mark [0] 1)) (0, 1) =
      false := by decide

theorem accept_off_passes_others :
    probeDedup { kernelDesc with guardAccept := false } = true ∧
    probeRequire { kernelDesc with guardAccept := false } = true ∧
    probeBudget { kernelDesc with guardAccept := false } = true ∧
    probeLicense { kernelDesc with guardAccept := false } = true ∧
    probeRefusal { kernelDesc with guardAccept := false } = true := by decide

theorem two_off_not_compliant :
    (⟨true, true, true, false, true, false⟩ : ConstitutionDesc) ∉ allDescs.filter compliantB := by
  intro h
  have := minimum_unique_in_class _ h
  exact absurd this (by decide)

theorem compliant_count : (allDescs.filter compliantB).length = 1 := by
  rw [unique_compliant]
  rfl

def costCap (d : ConstitutionDesc) : Nat :=
  (if d.dedupAdmit then 1 else 0) + (if d.guardRequire then 1 else 0) +
  (if d.guardAccept then 1 else 0) + (if d.gateBudget then 1 else 0) +
  (if d.gateLicense then 1 else 0) + (if d.certRefusal then 1 else 0)

theorem cost_values :
    costCap kernelDesc = 6 ∧ costCap ⟨false, false, false, false, false, false⟩ = 0 ∧
    costCap { kernelDesc with gateBudget := false } = 5 := by decide

theorem cost_constant_on_compliant :
    ∀ d ∈ allDescs.filter compliantB, costCap d = 6 := by
  intro d hd
  rw [minimum_unique_in_class d hd]
  rfl

theorem retract_on_story :
    (NoOutside.replayC (storyH.map .base) ⟨genesis, [[[0]]]⟩).base = replay storyH genesis :=
  extension_retract_replay storyH _

theorem retract_keeps_panel :
    (NoOutside.replayC (storyH.map .base) ⟨genesis, [[[0]]]⟩).panel = [[[0]]] := by decide

theorem section_instance : (NoOutside.CWorld.mk (replay storyH genesis) []).base =
    replay storyH genesis := retract_section _
```

## Line-by-line Lean explanation

**The four probe worlds (52-66).** One token for the admission and
requirement probes; a satisfied two-token world for the acceptance and
refusal probes; the same two tokens with an empty column and no budget
for the budget probe; with budget but no license for the license probe.
The book's `probes_are_step_noops` runs the sealed `step` on each pair:
these are the kernel's refusals, decided.

**The six probes and `compliantB` (70-90).** Each is a Boolean equality
of worlds (`==` from `DecidableEq`). The battery is their conjunction.
The book's `kernel_compliant` is the all-on evaluation.

**The six separations (99-121).** Each is a pair of `decide`s: the
relaxed descriptor fails, the kernel passes. The book's `off_outcomes`
shows what the relaxed machine did instead, field by field;
`accept_off_breaks` connects the acceptance probe to the sealed
preservation theorem at this instance: the requirement `(0, 1)` is
satisfied before the mark and not after. `accept_off_passes_others`
makes the audit's point concrete: the relaxed descriptor fails one
probe and passes five, so "load-bearing" is a statement about that
probe.

**`unique_compliant` (128-129).** Sixty-four descriptors, six probes
each, one `decide`. The kernel checks three hundred and eighty-four
world equalities. **`minimum_unique_in_class` (136-142).** Membership
in a one-element list is the head case or an impossible tail. The
book's `two_off_not_compliant` uses it the other way: a descriptor in
the compliant list would equal `kernelDesc`, and this one does not;
`compliant_count` rewrites with the theorem.

**The cost orders (book only).** Genesis defines no cost order in Lean;
the mirror defines two. The book's `costCap` counts enabled guards,
takes values 6, 0 and 5 on three descriptors, and is constant on the
compliant set by rewriting with the uniqueness theorem. Any order is.

**The retract (154-169).** `extension_retract` is `rfl` because `stepC`
on a base event is written as the pair `⟨step cw.base e, cw.panel⟩`.
`extension_retract_replay` is an induction on the history with the
world quantified inside, as in Unit 47's `support_replay`.
`retract_section` is `rfl`. The book's `retract_on_story` runs the
story's events through a panel kernel and lands on the story, with the
panel untouched (`retract_keeps_panel`).

## What has been proved

- Six separations: each guard off fails its probe while the kernel
  passes (Genesis); each relaxed machine's outcome, and that a single
  toggle fails only its own probe (book); on all sixty-four
  descriptors, failed probes equal off guards (Python).
- The compliant set is `[kernelDesc]` (Genesis); its length is one and
  a two-toggle descriptor is outside it (book).
- Any cost order is constant on the compliant set (book, for a
  declared order; the mirror for its two).
- The panel extension projects back to the kernel on every base event
  and history (Genesis; on the story in the book and the mirror).
- The acceptance probe is an instance of preservation (book).

## What has not been proved

- Categorical initiality, or minimality in any class other than the
  sixty-four descriptors; the paper says "underdetermined as an
  absolute claim".
- That a guard is necessary for a sealed theorem. The probes are
  calibrated instances; `accept_off_breaks` shows the connection at one
  world, not in general.
- That the battery characterises the sealed theorems: a descriptor
  outside the class could pass all six probes and still differ.
- A cost order in Genesis's Lean: none is defined; "both orders agree"
  is a mirror computation on a singleton.
- That the retract is more than one projection commuting with one
  declared extension's base events.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `allDescs` as the class | the comparison | declared (Unit 48) |
| the four probe worlds and six probes | compliance | declared, calibrated by the author on the kernel |
| `compliantB` | the battery | declared |
| `NoOutside.CWorld`, `stepC` | the retract | declared extension (Unit 47) |
| `costCap` | a cost order | Lean (book), declared here |
| `decide`, `List.filter`, `List.Mem` | computation and proof | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** A finite table, decided: six guards, six
failures, one survivor; a projection that commutes with the kernel's
step.

**Phrases to read with care.**

- "Each guard is load-bearing" (header line 25): probe-relative. The
  guard's necessity for the sealed theorem is not what is proved.
- "The retract half of initiality" (section title, line 144): one
  declared projection on one declared extension; the correction ledger
  C8 rescoped the terminal, and the title keeps the older words.
- "Minimality under both declared cost orders" (docstring, 131-135):
  the orders live in the mirror; the Lean theorem is the singleton.
- "Most primitive engine": answered as "unique probe-compliant
  descriptor in the declared toggle class" and nothing wider.

## Student exercise

Design a seventh probe for the `notes` field: a world and an event on
which the kernel is a no-op, so that switching some guard off would
fail it. Then explain why no such probe exists inside this class, and
what that says about what the six bits describe.

## Answer

The kernel appends every note (`step w (.note n)` writes `notes ++
[n]`), so no `note` event is a no-op on any world: a probe needs a
no-op to calibrate on. Nor does any bit of the descriptor touch the
`notes` branch of `interpStep`, which is `{ w with notes := w.notes ++
[n] }` for every `d`. So no descriptor in the class can be told from
the kernel by a `note` event, and no probe of the kind used here can
exist for that field. This says what Unit 48 said: the six bits select
which guards are consulted; the handling of notes, like the event
grammar and the application functions, is written into `interpStep`
and is not described by any member of the class.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Initiality.lean` lines 52-90 (probe worlds, probes, battery), 99-121 (six separations), 128-142 (uniqueness), 154-169 (retract) |
| Axiom report | `artifacts/lean_axioms.txt` lines 309-319: `retract_section` none; ten `{propext, Quot.sound}` |
| Paper | `paper/native_derivation_completion.md` section 12 (minimality and universality, terminal UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_CLASS); `paper/paper_claim_ledger.md` `CL-NC-INITIALITY`; `paper/pr11_correction_ledger.md` C8 |
| Python | `code/derivation/completion.py` (`PROBES`, `probe_results`, `compliant`, `cost_capabilities`, `cost_lex`, `minimality_report`), `artifacts/completion_minimality.json`, `tests/test_completion.py` (`test_each_guard_is_load_bearing`, `test_unique_compliant_kernel_and_orders_agree`) |
| Check (Python, partly book) | `python textbook/checks/u49_initiality.py`: the six probes on `step`, the six relaxations, the probe-toggle correspondence and histogram on all 64, the two cost orders, the report against the artifact, the retract with a Python (book) panel |
| Check (book Lean) | `python textbook/checks/u49_lean.py`: twelve book declarations plus ten Genesis theorems kernel-checked, Lean 4.33.0 |
