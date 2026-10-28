# Unit 47. Putting the viewer on the books: certification as a replayed, panel-relative quotient

**Claim.** `NoOutside` extends the one-step support factorization of
Unit 45 to whole histories (`support_replay`), to the repair family
(`support_repairFamily`), to the obstruction certificate
(`support_obstructed`) and to the quiescence verdict
(`support_quiescent`), and bundles the four as the effectual-outside
dichotomy (`effectual_outside_dichotomy`): two worlds that agree on the
represented support and receive the same history agree on every
operational result, so whatever changes a result already differs in the
support, and what changes no result has no operational authority. The
invariance ceiling is restated for list-valued constructions
(`equivariant_family_invariant`). The evaluator panel, a free argument
in Unit 45, becomes a field of an extended state `CWorld` admitted by an
event; base events act as the sealed step and never touch the panel
(`stepC_conservative`), admission never touches the base
(`admitEvaluator_base_inert`), and the certificate is a function of the
replayed state (`certNegC`). Joint non-separation by a panel is an
equivalence (`panel_equiv`), the negative certificate is exactly
non-emptiness plus joint non-separation (`certNeg_iff_panelEquiv`), and
the ceiling of Unit 45 carries over verbatim (`certC_ceiling`).
**Status:** derived for the fixed kernel; the "outside" is the one
field `supp` forgets; the absolute form is recorded as unformulable, not
proved. **Lean:** `lean4/Derivation/NoOutside.lean` lines 32-268,
imports `Represented`. **Axioms:** `equivariant_family_invariant` and
`panel_equiv` none; the other ten `{propext, Quot.sound}`.
**Depends on:** Unit 45 (the kernel, `supp`, `support_determines`,
`certNegB`, `cert_not_correspondence`), Unit 39 (the single-output
ceiling).

## Question

Unit 45 proved that one step of the kernel reads only the represented
support, and it certified pairs with a panel handed in from outside the
state. Two things were left. Does the one-step fact survive a whole
history, and does it reach the verdicts and families a reader cares
about? And can the panel itself be put inside the replayed state, so
that a certificate is a fact about a history and not about an argument
someone supplied? If so, what does a certificate then say, and what
does it still not say?

## What we already possess

- `World`, `step`, `replay`, `supp`, `support_determines`,
  `repairFamily`, `obstructedB`, `quiescentB` (Unit 45).
- `Evaluator`, `verdictB`, `certPosB`, `certNegB`, `cert_scope`,
  `cert_not_correspondence`, `cert_panel_relative` (Unit 45).
- `equivariant_output_invariant`, the single-output ceiling (Unit 39).
- The fact that `World` has exactly one field `supp` does not read:
  `notes`.

## New concept: factorization through a projection, and a panel store

*Factorization.* A function of worlds factors through `supp` when two
worlds with the same support get the same value. `support_determines`
said this of one step. Induction on the history says it of `replay`;
the three other theorems say it of three functions that read the
world directly, by taking both worlds apart and substituting the six
equalities.

*The dichotomy.* Fix two worlds with the same support and one history.
Then the replayed supports, the repair families, the certificates and
the verdicts are equal. Read backwards: a difference that shows up in
any of these was already a difference of support.

*The panel store.* `CWorld` is a `World` and a list of evaluators;
`CEvent` is a base event or an admission; `stepC` runs the base event on
the base and appends a fresh evaluator on an admission; `certNegC` is
`certNegB` of the replayed panel.

*The joint quotient.* `PanelEquiv panel i j` says that no column of any
evaluator in the panel contains one of `i`, `j` without the other.

## Plain-language interpretation

Unit 45 kept a notebook field in the state that nothing reads. This
module checks that it stays unread along any run, however long, and
that the things a user asks of the kernel, the repair menu, the
certificate of exhaustion, the quiescence verdict, never consult it.
That is the whole content of "no observer from nowhere" inside this
kernel: the one place an outside could hide has been shown to have no
effect, and anything that does have an effect is in the books. The
module and the paper both say what this is not: it is not a theorem that
nothing exists outside the state. The type of `step` admits no other
input, and a statement about inputs that are not represented cannot be
written in this calculus at all. The paper gives that fact a name and
counts it as part of the verdict.

The second half moves the panel of evaluators from the margin into the
state. In Unit 45 one could ask "is this pair certified?" only after
handing over a panel. Now evaluators are admitted by an event, like
tokens, and the question has an answer that depends on the history
alone. What the answer means is then worked out exactly: a negative
certificate holds when there is at least one evaluator and none of their
columns splits the pair. That relation is an equivalence, a quotient. It
is the panel's quotient, and the ceiling from Unit 45 stands: a column
not on the panel may split a pair the panel certifies as equal.
Certification reaches the panel's joint quotient and nothing beyond it.

## Pseudocode

```
supp(w) = (data, views, reqs, refusals, budget, licensed)   -- notes dropped

support_replay:   supp w = supp w'  ⟹  supp (replay h w) = supp (replay h w')
                  by induction on h, one support_determines per event
support_X:        supp w = supp w'  ⟹  X w = X w'      for X in {repairFamily, obstructedB, quiescentB}
dichotomy:        the four conclusions at once, from support_replay

CWorld = (base : World, panel : [Evaluator])
stepC (base e)            = (step base e, panel)
stepC (admitEvaluator E)  = if E ∈ panel then unchanged else (base, panel ++ [E])
certNegC cw i j           = certNegB cw.panel i j

PanelEquiv panel i j  =  ∀ E ∈ panel, ∀ c ∈ E, (i ∈ c ↔ j ∈ c)
certNegB panel i j = true  ⟺  panel ≠ [] ∧ PanelEquiv panel i j
```

## Python

`supp`, `CWorld`, `stepC` and `PanelEquiv` have no Genesis Python
mirror; the check builds them as Python (book) over Genesis's
`represented.py`, whose `cert_pos`, `cert_neg`, `verdict` and
`certification_report` are the panel verdicts of Unit 45.

```python
def supp(w):                      # every field but notes
    return (w.data, w.views, w.reqs, w.refusals, w.budget, w.aug_licensed)

def panel_equiv(panel, i, j):     # no column of any evaluator tells i from j
    return all((i in c) == (j in c) for E in panel for c in E)
```

The check script's run:

```text
the dichotomy: beginnings differing only in notes, the story history:
  notes (): results agree True; notes after ()
  notes (7, 8): results agree True; notes after (7, 8)
  notes (0, 0, 0): results agree True; notes after (0, 0, 0)
  notes (999,): results agree True; notes after (999,)
the contrapositive over a small set of worlds:
  28 pairs, 27 with a differing result, all with differing support: True
the extended kernel:
  base is the story True; panel (((0,),), ((0, 1),))
  admission leaves the base True; a base event leaves the panel True and acts as step True
  split panel on (0,1): certPos False, certNeg False
the joint quotient on carrier {0,1,2}, every panel of up to two evaluators
  507 panels: equivalence failures 0; certNeg vs non-empty and joint quotient failures 0
  empty panel: joint quotient (0,1) True, certNeg False
the ceiling, against the artifact:
  blind panel certifies 0 ~ 1: True; the story's column [0] separates: True; artifact {'certification_is_panel_relative': True, 'outside_column_separates': True, 'panel_certifies_equivalent': True}
failures: []
```

## Line-by-line Python explanation

`results(w, r)` packs the four conclusions of the dichotomy: the support,
the repair family, the certificate and the verdict. The first block
replays the pigeonhole history from four beginnings that differ only in
`notes`; the four results agree with the story's, and the notes are
still there at the end, untouched and unread.

The second block is the contrapositive in finite form. Eight worlds
near the story: one of them, the story with a note added, has the same
results as the story, and that pair is the one of the twenty-eight whose
results agree. The other twenty-seven pairs differ in some result and
every one of them differs in support. This is a check of the theorem on
a sample, not a proof; the proof is the Lean.

The third block is `CWorld`. The history is the story's events, then two
admissions and a repeated one; the base equals the story and the panel
holds each evaluator once. An admission leaves the base; a base event
leaves the panel and acts as `step`. The panel `[[[0]], [[0, 1]]]` is
split on the pair `(0, 1)`: one evaluator separates it, the other does
not, so neither certificate holds.

The fourth block enumerates every panel of at most two evaluators of at
most two columns drawn from six columns over the carrier `{0, 1, 2}`,
five hundred and seven panels, and checks reflexivity, symmetry and
transitivity of `panel_equiv` on every pair and triple, and the
characterisation of `cert_neg` on every pair. No failure. The empty
panel is the scope condition in the open: its joint quotient relates
everything and it certifies nothing.

The last block is the ceiling of Unit 45 recomputed and compared with
the artifact's three recorded booleans.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/NoOutside.lean lines 32-39, 43-52, 91-99
theorem support_replay (h : List Event) :
    ∀ {w w' : World}, supp w = supp w' →
      supp (replay h w) = supp (replay h w') := by
  induction h with
  | nil => intro w w' hs; exact hs
  | cons e rest ih =>
      intro w w' hs
      exact ih (support_determines w w' hs e)

theorem support_repairFamily (w w' : World) (h : supp w = supp w')
    (r : Req) : repairFamily w r = repairFamily w' r := by
  cases w with
  | mk d v rq f b a nt =>
    cases w' with
    | mk d' v' rq' f' b' a' nt' =>
      simp only [supp, Supp.mk.injEq] at h
      obtain ⟨h1, h2, h3, h4, h5, h6⟩ := h
      subst h1; subst h2; subst h3; subst h4; subst h5; subst h6
      rfl

theorem effectual_outside_dichotomy (w w' : World)
    (hs : supp w = supp w') (h : List Event) (r : Req) :
    supp (replay h w) = supp (replay h w') ∧
      repairFamily (replay h w) r = repairFamily (replay h w') r ∧
      obstructedB (replay h w) r = obstructedB (replay h w') r ∧
      quiescentB (replay h w) = quiescentB (replay h w') := by
  have hrep := support_replay h hs
  exact ⟨hrep, support_repairFamily _ _ hrep r,
    support_obstructed _ _ hrep r, support_quiescent _ _ hrep⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/NoOutside.lean lines 108-114, 125-164
theorem equivariant_family_invariant {S R : Type} (actS : S → S)
    (actR : R → R) (F : S → List R)
    (hequiv : ∀ s, F (actS s) = (F s).map actR) :
    ∀ s, actS s = s → (F s).map actR = F s := by
  intro s hfix
  calc (F s).map actR = F (actS s) := (hequiv s).symm
    _ = F s := by rw [hfix]

structure CWorld where
  base : World
  panel : List Evaluator
deriving Repr, DecidableEq

inductive CEvent where
  | base (e : Event)
  | admitEvaluator (E : Evaluator)
deriving Repr, DecidableEq

def stepC (cw : CWorld) : CEvent → CWorld
  | .base e => ⟨step cw.base e, cw.panel⟩
  | .admitEvaluator E =>
      if E ∈ cw.panel then cw
      else ⟨cw.base, cw.panel ++ [E]⟩

def replayC (h : List CEvent) (cw : CWorld) : CWorld :=
  h.foldl stepC cw

theorem stepC_conservative (cw : CWorld) (e : Event) :
    (stepC cw (.base e)).base = step cw.base e ∧
      (stepC cw (.base e)).panel = cw.panel :=
  ⟨rfl, rfl⟩

theorem admitEvaluator_base_inert (cw : CWorld) (E : Evaluator) :
    (stepC cw (.admitEvaluator E)).base = cw.base := by
  simp only [stepC]
  split <;> rfl

def certPosC (cw : CWorld) (i j : Nat) : Bool :=
  certPosB cw.panel i j

def certNegC (cw : CWorld) (i j : Nat) : Bool :=
  certNegB cw.panel i j
```

```lean
-- Lean (Genesis), lean4/Derivation/NoOutside.lean lines 174-192 (statement), 266-268
def PanelEquiv (panel : List Evaluator) (i j : Nat) : Prop :=
  ∀ E ∈ panel, ∀ c ∈ E, ((i ∈ c) ↔ (j ∈ c))

theorem panel_equiv (panel : List Evaluator) :
    Equivalence (PanelEquiv panel) := by
  refine ⟨?_, ?_, ?_⟩
  · intro x E hE c hc
    exact Iff.rfl
  · intro x y hxy E hE c hc
    exact (hxy E hE c hc).symm
  · intro x y z hxy hyz E hE c hc
    exact (hxy E hE c hc).trans (hyz E hE c hc)

theorem certNeg_iff_panelEquiv (panel : List Evaluator) (i j : Nat) :
    certNegB panel i j = true ↔
      panel ≠ [] ∧ PanelEquiv panel i j := by
  -- lines 193-259: unfold certNegB to "non-empty and every evaluator's
  -- verdict is false"; each direction cases on `decide (i ∈ c)` and
  -- `decide (j ∈ c)` for a column c and discharges the four combinations.

theorem certC_ceiling :
    certNegC ⟨genesis, [[[0, 1]], [[0, 1]]]⟩ 0 1 = true ∧
      sepB [0] 0 1 = true := cert_not_correspondence
```

The book's Lean runs the story of Unit 45 from a beginning with notes,
states the contrapositive as a lemma and applies it, builds the extended
story with two admitted evaluators, and takes the joint quotient out of
the certificate by the characterisation.

```lean
-- Lean (book), textbook/checks/u47_lean.py
def storyH : List Event :=
  [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
   .require 0 1, .require 0 2, .require 1 2, .addView [0]]

def story : World := replay storyH genesis

theorem notes_inert_history :
    supp (replay storyH { genesis with notes := [7, 8] }) = supp (replay storyH genesis) :=
  support_replay storyH rfl

theorem notes_still_differ :
    (replay storyH { genesis with notes := [7, 8] }).notes = [7, 8] ∧
    (replay storyH genesis).notes = [] := by decide

theorem dichotomy_instance :
    supp (replay storyH { genesis with notes := [7, 8] }) = supp story ∧
    repairFamily (replay storyH { genesis with notes := [7, 8] }) (1, 2) =
      repairFamily story (1, 2) ∧
    obstructedB (replay storyH { genesis with notes := [7, 8] }) (1, 2) =
      obstructedB story (1, 2) ∧
    quiescentB (replay storyH { genesis with notes := [7, 8] }) = quiescentB story :=
  effectual_outside_dichotomy _ _ rfl storyH (1, 2)

theorem differs_in_support (w w' : World) (h : quiescentB w ≠ quiescentB w') :
    supp w ≠ supp w' :=
  fun hs => h (support_quiescent w w' hs)

theorem story_extension_differs :
    quiescentB story = false ∧ quiescentB (step story (.addView [1])) = true ∧
    supp story ≠ supp (step story (.addView [1])) := by
  refine ⟨by decide, by decide, differs_in_support _ _ ?_⟩
  decide

def cstory : CWorld :=
  replayC (storyH.map CEvent.base ++ [.admitEvaluator [[0]], .admitEvaluator [[0, 1]]])
    ⟨genesis, []⟩

theorem cstory_values : cstory.base = story ∧ cstory.panel = [[[0]], [[0, 1]]] := by
  decide

theorem admit_twice :
    (replayC [.admitEvaluator [[0]], .admitEvaluator [[0]]] ⟨genesis, []⟩).panel = [[[0]]] := by
  decide

theorem admit_inert_instance :
    (stepC cstory (.admitEvaluator [[1]])).base = story :=
  (admitEvaluator_base_inert cstory [[1]]).trans cstory_values.1

theorem cert_reads_panel (w : World) (p : List Evaluator) (i j : Nat) :
    certNegC ⟨w, p⟩ i j = certNegB p i j ∧ certPosC ⟨w, p⟩ i j = certPosB p i j :=
  ⟨rfl, rfl⟩

theorem split_panel :
    certPosC cstory 0 1 = false ∧ certNegC cstory 0 1 = false := by decide

theorem ceiling_on_story :
    certNegC ⟨story, [[[0, 1]], [[0, 1]]]⟩ 0 1 = true ∧ sepB [0] 0 1 = true ∧
    [0] ∈ story.views := by decide

theorem panel_equiv_instance : PanelEquiv [[[0, 1]], [[0, 1]]] 0 1 :=
  ((certNeg_iff_panelEquiv _ 0 1).mp (by decide)).2

theorem empty_panel : PanelEquiv [] 0 1 ∧ certNegB [] 0 1 = false := by
  refine ⟨?_, by decide⟩
  intro E hE
  cases hE

theorem quotient_trans (p : List Evaluator) (h1 : PanelEquiv p 0 1) (h2 : PanelEquiv p 1 2) :
    PanelEquiv p 0 2 :=
  (panel_equiv p).trans h1 h2

theorem family_ceiling_bool :
    ∀ b : Bool, (!b) = b → ([b, !b].map not) = [b, !b] :=
  equivariant_family_invariant not not (fun b => [b, !b]) (fun _ => rfl)

theorem no_fixed_point : ∀ b : Bool, (!b) ≠ b := by decide
```

## Line-by-line Lean explanation

**`support_replay` (32-39).** The statement quantifies the two worlds
inside the `∀`, after the history, so that the induction hypothesis is
usable at the successor worlds. The empty history is the hypothesis
itself. For `e :: rest`, one `support_determines` moves the agreement
from `w, w'` to `step w e, step w' e`, and the hypothesis does the rest.
The book's `notes_inert_history` supplies the agreement by `rfl`: the two
beginnings differ only in `notes`, which `supp` does not mention, so
their supports are definitionally equal.

**The three direct factorizations (43-77).** Each takes both worlds
apart into seven fields, turns the support equality into six field
equalities with `Supp.mk.injEq`, substitutes them, and closes by `rfl`:
after substitution the two worlds differ only in `nt` and `nt'`, and the
function on the left never mentions that field. The proof is the same
three times because the fact is the same: these functions do not read
`notes`.

**`effectual_outside_dichotomy` (91-99).** One `support_replay` and the
three direct theorems applied to the replayed supports. The docstring
states the scope twice: operational, for this constitution, not about
unrepresented existence. The book's `dichotomy_instance` is the theorem
at the story with the violated pair; `notes_still_differ` shows the two
worlds are not equal as worlds, which is what makes the agreement a
fact and not a tautology.

**The contrapositive (book).** `differs_in_support` is one line: if the
supports were equal, `support_quiescent` would make the verdicts equal.
`story_extension_differs` applies it to the story and its augmentation
by `[1]`; the verdict changes, so the support does, and it does in the
`views` field.

**`equivariant_family_invariant` (108-114).** A `calc` of two steps for
any types, any actions, any list-valued `F`, from the equivariance
hypothesis. It is a statement of the metatheory with no kernel in it;
the audit records it as a general identity presented as a lift. The
book's `family_ceiling_bool` instantiates it on `Bool` with the swap,
where `no_fixed_point` shows the premise is never met: the ceiling
constrains fixed points, and there is none there.

**`CWorld`, `CEvent`, `stepC`, `replayC` (125-142).** The panel is a
list; admission is guarded by membership, so the book's `admit_twice`
records one copy. `stepC_conservative` is two `rfl`s because the base
case of `stepC` is written as a pair whose components are `step` and the
old panel. `admitEvaluator_base_inert` splits on the guard; both
branches keep `base`. The book's `cstory_values` evaluates the extended
story: the base is the story of Unit 45 and the panel holds the two
evaluators in admission order. `admit_inert_instance` chains the
Genesis theorem with that value.

**`certPosC`, `certNegC` (160-164).** Unit 45's verdicts on the replayed
panel. The book's `cert_reads_panel` is `⟨rfl, rfl⟩` for any base: the
verdict does not read the base at all. That is the exact sense of
"replay-integrated": the panel is history-determined, and the verdict is
a function of it.

**`PanelEquiv` and `panel_equiv` (174-185).** Reflexivity is `Iff.rfl`
per column; symmetry and transitivity are `.symm` and `.trans` of the
column `Iff`s. No axiom is used. The book's `quotient_trans` takes the
third field of the `Equivalence`.

**`certNeg_iff_panelEquiv` (190-259).** Forwards: non-emptiness from
`!panel.isEmpty`, and for each evaluator and column, the four cases of
`decide (i ∈ c)` and `decide (j ∈ c)`; the two mixed cases make
`sepB c i j = true`, contradicting the evaluator's false verdict, and
the two agreeing cases give the `Iff`. Backwards: non-emptiness gives
`!isEmpty`, and a separating column would contradict the `Iff` at that
column. The book's `panel_equiv_instance` runs the forward direction on
the blind panel, and `empty_panel` shows why the right-hand side needs
`panel ≠ []`.

**`certC_ceiling` (266-268).** The proof term is Unit 45's
`cert_not_correspondence`, because `certNegC` of the pair is
definitionally `certNegB` of the panel. The book's `ceiling_on_story`
puts the story in the base and adds that `[0]` is one of the story's
own columns: the panel certifies a pair the state itself separates.

## What has been proved

- Support factorization along any history, and for the repair family,
  the certificate and the verdict (Genesis).
- The dichotomy, as the conjunction of those four (Genesis; at the
  story in the book, with the beginnings shown still to differ).
- The contrapositive form as a lemma and at an instance (book).
- The family form of the ceiling, as a general identity (Genesis); a
  `Bool` instance whose premise is never met (book).
- Conservativity of the extended kernel and inertness of admission
  (Genesis); the extended story's value and the idempotence of admission
  (book).
- Joint non-separation is an equivalence; the negative certificate is
  non-emptiness plus joint non-separation; the ceiling carries over
  (Genesis); the quotient at the blind panel, the empty panel's
  two faces, and the ceiling with the story as base (book).
- On a finite sample: the dichotomy from four beginnings; the
  contrapositive on twenty-seven pairs; the equivalence and the
  characterisation on five hundred and seven panels (Python (book)).

## What has not been proved

- That nothing outside `World` matters. The theorems quantify over
  worlds, and worlds differ outside `supp` in `notes` alone. The paper
  records the absolute statement as unformulable in this calculus.
- Anything about the positive certificate `certPosB` as a relation: it
  is characterised in Unit 45 (`cert_scope`) but not shown to be an
  equivalence, and it is not one in general.
- That the evaluator-admission grammar is complete, or that a panel
  could be anything but a list of column lists.
- That `equivariant_family_invariant` applies to any kernel
  construction: no kernel `F` is shown equivariant in this module.
- `replayC_deterministic` (167) has a trivially true conclusion and is
  omitted.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `World` and the `notes` field | the one unread field | declared constitution (Unit 45) |
| `supp` | the projection the factorization runs through | declared |
| `CWorld`, `CEvent`, `stepC` | the panel on the books | declared conservative extension |
| `Evaluator := List View` | what a panel member is | declared |
| `{S R : Type}`, `actS`, `actR`, `F`, `hequiv` | the family ceiling | metatheory; the equivariance is assumed |
| `List`, `decide`, `simp only`, `cases`, `subst` | computation and proof | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** Everything the kernel does reads the
support; the panel is data admitted by an event; a certificate is the
panel's quotient and nothing more.

**Phrases to read with care.**

- "No observer from nowhere, settled" (module header line 6): settled for
  the fixed constitution, meaning the `notes` field is inert and the
  panel is data; not a claim about unrepresented inputs. The paper's
  own ceiling says so.
- "The ceiling constrains tied menus exactly as single results"
  (docstring, 103-107): a two-line identity under an assumed
  equivariance; read it as a remark.
- "Panel-relative warrant is exactly joint-quotient closure": for a
  non-empty panel; the empty panel's quotient is total and its
  certificate false.

## Student exercise

Admit a third evaluator `[[1]]` to `cstory`. Does the pair `(0, 1)`
become certified either way? Then admit `[[2]]` instead. What are the
two certificates on `(0, 1)` now, and which theorem of this unit says
the base of the story played no part in either answer?

## Answer

With `[[1]]` added the panel is `[[[0]], [[0, 1]], [[1]]]`. On `(0, 1)`
the evaluators `[[0]]` and `[[1]]` separate and `[[0, 1]]` does not, so
`certPosC` is false (not every evaluator separates) and `certNegC` is
false (not every evaluator fails to separate). With `[[2]]` added
instead the panel is `[[[0]], [[0, 1]], [[2]]]`; the column `[2]`
contains neither `0` nor `1`, so that evaluator does not separate; still
one evaluator separates and two do not, and both certificates are false.
A panel certifies only when it is unanimous. `cert_reads_panel` says the
base is not read: both verdicts are `rfl`-equal to `certNegB` and
`certPosB` of the panel alone, whatever the base.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/NoOutside.lean` lines 32-99 (factorization, dichotomy), 108-114 (family ceiling), 125-168 (extended kernel, certificates), 174-259 (joint quotient, characterisation), 266-268 (ceiling) |
| Axiom report | `artifacts/lean_axioms.txt` lines 281-292: `equivariant_family_invariant`, `panel_equiv` none; ten `{propext, Quot.sound}` |
| Paper | `paper/native_derivation_completion.md` section 8 (the strongest form of Rule 2, ABSOLUTE_NO_OUTSIDE_UNFORMULABLE) and section 13 (the certification ceiling); `paper/paper_claim_ledger.md` `CL-NC-RULE2` (non-emptiness scope, 2026-08-18); `paper/native_derivation_map.md` rows "replay factors through support", "certification panel certifies up to Zero/ZeroRel" |
| Used later | `Initiality.lean` (`extension_retract`, `retract_section`) on `CWorld`, `stepC`, `replayC` |
| Python | `code/derivation/represented.py` (`verdict`, `cert_pos`, `cert_neg`, `certification_report`), `artifacts/represented.json` key `certification`; no Genesis mirror of `supp`, `CWorld`, `PanelEquiv` |
| Check (Python, partly book) | `python textbook/checks/u47_no_outside.py`: the dichotomy from four beginnings, the contrapositive on a sample, the extended kernel, the equivalence and characterisation on 507 panels, the ceiling against the artifact |
| Check (book Lean) | `python textbook/checks/u47_lean.py`: sixteen book declarations plus eleven Genesis theorems kernel-checked, Lean 4.33.0 |
