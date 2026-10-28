import Derivation.InterpreterBoundary
import Derivation.NoOutside

/-!
# The interpreter boundary at verdict level

Outside the seal: a research tree that consumes the sealed `Derivation`
package read-only and changes nothing in it.  First built against
`fc6349e05fb135fe0bdc0613f2ea1cc16390de00`, core Lean 4.33.0.
AuthorityEffect: None.

`Derivation.InterpreterBoundary` leaves one obligation open
(`openDenotationalBridge`): give the uncoded occurrence `none` of the
boundary carrier `Option ConstitutionDesc` a meaning that is fixed by a
law rather than chosen freely (`arbitrary_uncoded_assignment` shows a
free choice of step function proves nothing), and show that identifying
that occurrence with a coded member changes an accessible operational
verdict, not only an inert field.

This file does both, in seven steps.

1. One verdict reads one guard.  At `genesis`, under the event
   `require 0 0`, the quiescence verdict of the world the interpreter
   produces under code `c` is exactly `c.guardRequire`
   (`quiescent_reads_guard`); the obstruction certificate for `(0, 0)`
   is its negation (`obstructed_reads_guard`).
2. The interpreter is not a step function.  For every
   `s : World → Event → World` there is a code `c` on which the
   interpreter and `s` disagree at that verdict (`interp_not_step`).
   Every coded member is such an `s` (`coded_member_separated`), and
   so is the diagonal function of `tower_persists`.  This is a fact of
   typing — a step function takes no code — made concrete by one
   guard; at a reflective world carrying `d`, the coded member `d` and
   the interpreter coincide (step 7).
3. The lawful meaning of the uncoded role.  On reflective worlds
   (`RWorld`, a world carrying its code), two laws stated in the sealed
   module's own vocabulary — interpretation (`Interprets`: the world
   part does what the carried code means) and quotation (`Quotes`: the
   code is inert data) — determine one reflective step, `rstep`
   (`lawful_unique`).  Every coded member lifts to a reflective step
   (`liftStep`) that quotes but does not interpret
   (`liftStep_not_interprets`).  So the meaning of `none` is forced,
   and it is not the lift of any step function (`rstep_not_lift`).
4. The derived relation.  `VSep x y` holds when the meanings of `x`
   and `y` disagree on quiescence at some reflective world and event.
   Irreflexivity, symmetry and cotransitivity are theorems
   (`vsep_irrefl`, `vsep_symm`, `vsep_cotrans`); the uncoded role is
   separated from every coded member (`vsep_uncoded`) — at a reflective
   world carrying another code, never at an aligned one (step 7).  The
   setting
   `verdictBoundary` therefore satisfies candidates A, Bs, Bc, D of
   `Derivation.PrimitiveCore` by proof (`boundary_A`, `boundary_Bs`,
   `boundary_Bc`, `boundary_D`), where `boundarySetting` satisfied A by
   declaration; and the declared relation is contained in the derived
   one (`declared_le_derived`).
5. Collapse.  Any map identifying `none` with any coded member is
   obstructed relative to `Irrefl` (`collapse_obstructed`), and any
   reading of the carrier that keeps the coded meanings and identifies
   `none` with a coded member — or with the lift of any step function
   at all — reports a quiescence verdict the lawful meaning does not
   (`identification_changes_quiescence`,
   `identification_with_step_changes_quiescence`).  By
   `NoOutside.support_quiescent` the verdict difference is a support
   difference (`verdict_entails_supp`), which re-proves the support half
   first shown by the scratch result `tower_persists_operational` of
   2026-10-27 (outside this repository, not an input here).
6. Limits.  Not every presentational difference among codes is a
   verdict difference: a code and the code with `dedupAdmit` flipped are
   never separated by one quiescence verdict
   (`coded_pair_not_vsep`), so `VSep` is strictly coarser than `≠` on
   the carrier.  At the `genesis` witness the closure family
   `nextFamily` is empty either way (`nextFamily_blind_at_genesis`);
   the two-token world `twoWorld`, reached by two admissions, separates
   it (`family_reads_guard`, `interp_not_step_family`).
7. The aligned code, the guards and well-formedness (section 7, added
   after the review of 2026-10-28).  At a reflective world carrying `d`
   the coded member `d` and the uncoded role coincide definitionally,
   under every function of the outcome and along every event sequence
   (`aligned_coded_equals_uncoded`, `aligned_no_verdict`,
   `aligned_trajectory`); `VSep (some d) none` is witnessed exactly at a
   world carrying another code (`vsep_uncoded_iff`).  Two codes differ
   only where a guard decides (`codes_agree_of_guardsPass`,
   `codes_separated_needs_guard`, `vsep_uncoded_needs_guard`).  The
   `genesis` witness is a rejected challenge whose unguarded outcome is
   not well formed (`genesis_witness_unguarded_not_wf`); every guard
   but `guardRequire` preserves well-formedness (`wf_interpStep`), and
   the well-formed, kernel-reachable world `accWorld` under `mark [0] 1`
   separates the interpreter from every step function and every coded
   member with both outcomes well formed (`quiescent_reads_accept`,
   `interp_not_step_wf`, `vsep_uncoded_wf`).

Admitted, not derived: the two laws `Interprets` and `Quotes` are the
reading of the sealed tags chosen here; `lawful_unique_at` is relative
to them.

Not claimed: locatedness (candidate `Bl`) of `VSep`; retention and
protection of the pair other than by declaring the stores to be `VSep`
(`boundary_F`, same status as `i5_boundary_is_F`); anything about
evaluators of other types; an absolute no-outside; any difference
between a code and the interpreter at a reflective world carrying that
code (refuted, `aligned_no_verdict`); any separation at which no guard
decides (impossible, `codes_separated_needs_guard`).

What is metatheory and what is represented.  The represented objects are
the sealed module's: a world (finite lists), an event, a code (six
booleans, 64 in all) and the verdicts `quiescentB`, `obstructedB`,
`nextFamily` read off a world.  A reflective world is a world paired
with the code it runs under, as the sealed `Constitution.GWorld` pairs a
world with its represented policy.  The carrier of `verdictBoundary` is
the 65 occurrences, never a function type.  The meaning of the uncoded
role, `rstep`, is defined from `interpStep` and has the same status as
`interpStep` in the sealed module: constitution, fixed metatheory, not
represented state.  The statements that quantify over every step
function `s : World → Event → World` (`interp_not_step`, `rstep_not_lift`,
`identification_with_step_changes_quiescence`) and over every reading
`I` are schemata of the metatheory: each instance is about one `s` or
one `I`, the witness code is computed from one evaluation of `s` at
`genesis` under `require 0 0` (at `accWorld` under `mark [0] 1` in
`interp_not_step_wf`), and no collection of step functions,
readings or worlds is formed or admitted anywhere.  Existentials are
witnessed by concrete finite objects.  Hypotheses about readings are
stated value by value, and `lawful_unique_at` is the pointwise form of
the uniqueness; the one function equation, `lawful_unique`, is a
metatheoretic packaging by `funext` that nothing else uses.
-/

namespace ResearchInterpreterVerdict

open Represented Constitution InterpreterBoundary

/-! ## 1. One verdict reads one guard -/

/-- At genesis, `require 0 0` — a demand that datum 0 be separated from
itself — is admitted exactly when the code does not guard requirements.
The resulting quiescence verdict is the code's `guardRequire` bit. -/
theorem quiescent_reads_guard (c : ConstitutionDesc) :
    quiescentB (interpStep c genesis (.require 0 0)) = c.guardRequire := by
  cases c with
  | mk a b cc d e f =>
    cases b <;> rfl

/-- The obstruction certificate for `(0, 0)` after the same event is the
negation of the guard: with the guard off the self-requirement is
recorded, violated and unrepairable. -/
theorem obstructed_reads_guard (c : ConstitutionDesc) :
    obstructedB (interpStep c genesis (.require 0 0)) (0, 0) =
      !c.guardRequire := by
  cases c with
  | mk a b cc d e f =>
    cases b <;> rfl

/-- The code with the requirement guard flipped. -/
def flipGuard (c : ConstitutionDesc) : ConstitutionDesc :=
  { c with guardRequire := !c.guardRequire }

/-! ## 2. The interpreter is not a step function -/

/-- **The interpreter is verdict-separated from every step function.**
Whatever `s : World → Event → World` is — a coded member, the diagonal
of `tower_persists`, anything — some code `c` makes the interpreter and
`s` disagree on quiescence at genesis under `require 0 0`.  The proof
reads the verdict of `s` and picks the code with the opposite guard. -/
theorem interp_not_step (s : World → Event → World) :
    ∃ c : ConstitutionDesc,
      quiescentB (interpStep c genesis (.require 0 0)) ≠
        quiescentB (s genesis (.require 0 0)) := by
  refine ⟨{ kernelDesc with
    guardRequire := !(quiescentB (s genesis (.require 0 0))) }, ?_⟩
  rw [quiescent_reads_guard]
  generalize quiescentB (s genesis (.require 0 0)) = b
  cases b <;> decide

/-- Every coded member in particular: the code with the opposite guard
disagrees with it on quiescence at genesis. -/
theorem coded_member_separated (d : ConstitutionDesc) :
    quiescentB (interpStep (flipGuard d) genesis (.require 0 0)) ≠
      quiescentB (interpStep d genesis (.require 0 0)) := by
  rw [quiescent_reads_guard, quiescent_reads_guard]
  show (!d.guardRequire) ≠ d.guardRequire
  cases d.guardRequire <;> decide

/-- The same pair disagrees on the obstruction certificate. -/
theorem coded_member_separated_obstructed (d : ConstitutionDesc) :
    obstructedB (interpStep (flipGuard d) genesis (.require 0 0)) (0, 0) ≠
      obstructedB (interpStep d genesis (.require 0 0)) (0, 0) := by
  rw [obstructed_reads_guard, obstructed_reads_guard]
  show (!(!d.guardRequire)) ≠ (!d.guardRequire)
  cases d.guardRequire <;> decide

/-- A quiescence difference is a support difference
(`NoOutside.support_quiescent`, contrapositive). -/
theorem supp_ne_of_quiescent_ne {w w' : World}
    (h : quiescentB w ≠ quiescentB w') : supp w ≠ supp w' :=
  fun hs => h (NoOutside.support_quiescent w w' hs)

/-- The verdict-level separation entails the support-level one. -/
theorem verdict_entails_supp (s : World → Event → World) :
    ∃ (c : ConstitutionDesc) (w : World) (e : Event),
      supp (interpStep c w e) ≠ supp (s w e) :=
  let ⟨c, hc⟩ := interp_not_step s
  ⟨c, genesis, .require 0 0, supp_ne_of_quiescent_ne hc⟩

/-! ## 3. The lawful meaning of the uncoded role -/

/-- A reflective world: the represented state together with the code it
runs under.  The code is carried as data, as `ConstitutionDesc` already
is in the sealed module (quotation). -/
abbrev RWorld := ConstitutionDesc × World

/-- The canonical lift of a step function: step the world, leave the
carried code as it is. -/
def liftStep (s : World → Event → World) : RWorld → Event → RWorld :=
  fun p e => (p.1, s p.2 e)

/-- The reflective step: run the code the world carries. -/
def rstep : RWorld → Event → RWorld :=
  fun p e => (p.1, interpStep p.1 p.2 e)

/-- Law L1, interpretation (the sealed module's `tag_interpretation`):
on a world carrying code `c`, the world part does what `c` means. -/
def Interprets (g : RWorld → Event → RWorld) : Prop :=
  ∀ (c : ConstitutionDesc) (w : World) (e : Event),
    (g (c, w) e).2 = interpStep c w e

/-- Law L2, quotation (the sealed module's `tag_quotation`): the carried
code is inert data. -/
def Quotes (g : RWorld → Event → RWorld) : Prop :=
  ∀ (c : ConstitutionDesc) (w : World) (e : Event), (g (c, w) e).1 = c

theorem rstep_interprets : Interprets rstep := fun _ _ _ => rfl

theorem rstep_quotes : Quotes rstep := fun _ _ _ => rfl

/-- **The two laws leave no freedom, at every reflective world.**  Any
reflective step that interprets and quotes agrees with `rstep` wherever
it is evaluated.  This is the pointwise content — the value at the world
and event one is at — and it is all that the rest of the file uses.  No
function extensionality enters the proof.  Contrast
`arbitrary_uncoded_assignment` in the sealed module: at step-function
type the uncoded role can be given any meaning; at reflective type the
laws fix it. -/
theorem lawful_unique_at (g : RWorld → Event → RWorld)
    (h1 : Interprets g) (h2 : Quotes g)
    (c : ConstitutionDesc) (w : World) (e : Event) :
    g (c, w) e = rstep (c, w) e := by
  calc g (c, w) e = ((g (c, w) e).1, (g (c, w) e).2) := rfl
    _ = (c, interpStep c w e) := by rw [h1 c w e, h2 c w e]

/-- The extensional packaging of `lawful_unique_at` as one function
equation.  Metatheory only: `funext` (`Quot.sound`) turns "the same value
everywhere" into "one function"; nothing below depends on this form. -/
theorem lawful_unique (g : RWorld → Event → RWorld)
    (h1 : Interprets g) (h2 : Quotes g) : g = rstep := by
  funext p e
  obtain ⟨c, w⟩ := p
  exact lawful_unique_at g h1 h2 c w e

/-- Under the lawful meaning the kernel's own code still runs to the
sealed step (`Constitution.interp_describe`, unchanged). -/
theorem rstep_self_description (w : World) (e : Event) :
    (rstep (kernelDesc, w) e).2 = step w e :=
  interp_describe w e

theorem liftStep_quotes (s : World → Event → World) :
    Quotes (liftStep s) := fun _ _ _ => rfl

/-- No lifted step function interprets: the lift ignores the carried
code, and some code disagrees with it on quiescence. -/
theorem liftStep_not_interprets (s : World → Event → World) :
    ¬ Interprets (liftStep s) := by
  intro h
  obtain ⟨c, hc⟩ := interp_not_step s
  exact hc (congrArg quiescentB (h c genesis (.require 0 0))).symm

/-- So the interpreter is the lift of no step function. -/
theorem rstep_ne_lift (s : World → Event → World) : liftStep s ≠ rstep :=
  fun h => liftStep_not_interprets s (h ▸ rstep_interprets)

/-- And the difference is a quiescence verdict at an accessible world. -/
theorem rstep_not_lift (s : World → Event → World) :
    ∃ (p : RWorld) (e : Event),
      quiescentB (rstep p e).2 ≠ quiescentB (liftStep s p e).2 :=
  let ⟨c, hc⟩ := interp_not_step s
  ⟨(c, genesis), .require 0 0, hc⟩

/-! ## 4. The derived relation and the setting -/

/-- The meaning of each occurrence of the boundary carrier: a coded
member means the lift of its step; the uncoded role means the
reflective step, the one reflective step that interprets and quotes. -/
def meaning : Option ConstitutionDesc → RWorld → Event → RWorld
  | some d => liftStep (interpStep d)
  | none => rstep

/-- Verdict separation: the two meanings disagree on quiescence at some
reflective world and event. -/
def VSep (x y : Option ConstitutionDesc) : Prop :=
  ∃ (p : RWorld) (e : Event),
    quiescentB (meaning x p e).2 ≠ quiescentB (meaning y p e).2

theorem vsep_irrefl : PrimDiff.Irrefl VSep :=
  fun _ ⟨_, _, h⟩ => h rfl

theorem vsep_symm (x y : Option ConstitutionDesc) (h : VSep x y) :
    VSep y x :=
  let ⟨p, e, h⟩ := h
  ⟨p, e, fun h' => h h'.symm⟩

theorem vsep_cotrans : PrimitiveCore.Cotrans VSep := by
  intro x y ⟨p, e, hxy⟩ z
  cases hdec : decide
      (quiescentB (meaning x p e).2 = quiescentB (meaning z p e).2) with
  | true =>
      exact Or.inr ⟨p, e, fun hzy => hxy ((of_decide_eq_true hdec).trans hzy)⟩
  | false =>
      exact Or.inl ⟨p, e, of_decide_eq_false hdec⟩

/-- **The uncoded role is verdict-separated from every coded member.** -/
theorem vsep_uncoded (d : ConstitutionDesc) : VSep (some d) none :=
  ⟨(flipGuard d, genesis), .require 0 0, (coded_member_separated d).symm⟩

theorem vsep_kernel : VSep (some kernelDesc) none := vsep_uncoded kernelDesc

/-- The interpreter boundary as a `PrimitiveCore.Setting` with the
DERIVED relation: carrier `Option ConstitutionDesc`, relation `VSep`,
endpoints (kernel code, interpreter role).  The retention and
protected-demand stores are declared to be the derived relation; they
carry the same declared status as in `boundarySetting`. -/
def verdictBoundary : PrimitiveCore.Setting where
  X := Option ConstitutionDesc
  r := VSep
  a := some kernelDesc
  b := none
  ret := VSep
  prot := VSep
  Ops := fun _ => False

/-- Candidate A by proof: the pair is asserted by a verdict witness and
irreflexivity is a theorem about verdicts. -/
theorem boundary_A : PrimitiveCore.A verdictBoundary :=
  ⟨vsep_kernel, vsep_irrefl⟩

theorem boundary_Bs : PrimitiveCore.Bs verdictBoundary :=
  ⟨boundary_A, vsep_symm⟩

theorem boundary_Bc : PrimitiveCore.Bc verdictBoundary :=
  ⟨boundary_A, vsep_cotrans⟩

theorem boundary_D : PrimitiveCore.D verdictBoundary :=
  (PrimitiveCore.D_iff_ne verdictBoundary).mpr (fun h => nomatch h)

/-- Candidate F with the stores declared as `VSep`: declared, as before. -/
theorem boundary_F : PrimitiveCore.F verdictBoundary :=
  ⟨boundary_A, vsep_kernel, vsep_kernel⟩

/-- The sealed module's declared relation is contained in the derived
one: every declared pair is verdict-separated. -/
theorem declared_le_derived (x y : Option ConstitutionDesc)
    (h : boundarySetting.r x y) : VSep x y := by
  obtain ⟨hx, hy⟩ := h
  subst hx
  subst hy
  exact vsep_kernel

/-! ## 5. Collapse changes a verdict -/

/-- Identifying the uncoded role with ANY coded member is obstructed
relative to `Irrefl` — the sealed `i5_collapse_obstructed` covered the
kernel code only, and by declaration. -/
theorem collapse_obstructed {β : Type} (d : ConstitutionDesc)
    (q : Option ConstitutionDesc → β) (hq : q (some d) = q none) :
    PrimDiff.FidelityObstruction PrimDiff.Irrefl VSep q :=
  PrimDiff.obstruction_under_irrefl (vsep_uncoded d) hq

/-- A reading of the carrier that keeps every coded member's meaning,
value by value: no equation between whole functions is assumed. -/
def Reading (I : Option ConstitutionDesc → RWorld → Event → RWorld) :
    Prop :=
  ∀ (d : ConstitutionDesc) (p : RWorld) (e : Event),
    I (some d) p e = meaning (some d) p e

/-- **Identifying the uncoded role with any coded member changes a
quiescence verdict.**  Any reading that keeps the coded meanings and
reads `none` as some coded member — value by value, which is weaker
than identifying the functions — reports, at an accessible reflective
world, a quiescence verdict different from the lawful meaning's. -/
theorem identification_changes_quiescence
    (I : Option ConstitutionDesc → RWorld → Event → RWorld)
    (hI : Reading I) (d : ConstitutionDesc)
    (hid : ∀ (p : RWorld) (e : Event), I none p e = I (some d) p e) :
    ∃ (p : RWorld) (e : Event),
      quiescentB (I none p e).2 ≠ quiescentB (rstep p e).2 := by
  obtain ⟨p, e, h⟩ := rstep_not_lift (interpStep d)
  refine ⟨p, e, ?_⟩
  rw [hid p e, hI d p e]
  exact fun h' => h h'.symm

/-- Stronger: reading `none`, value by value, as the lift of ANY step
function — a coded member, the missed function of `tower_persists`, any
other — changes a quiescence verdict.  The occurrence the coding omits
is not of step type. -/
theorem identification_with_step_changes_quiescence
    (I : Option ConstitutionDesc → RWorld → Event → RWorld)
    (s : World → Event → World)
    (hid : ∀ (p : RWorld) (e : Event), I none p e = liftStep s p e) :
    ∃ (p : RWorld) (e : Event),
      quiescentB (I none p e).2 ≠ quiescentB (rstep p e).2 := by
  obtain ⟨p, e, h⟩ := rstep_not_lift s
  refine ⟨p, e, ?_⟩
  rw [hid p e]
  exact fun h' => h h'.symm

/-! ## 6. Limits -/

/-- The code with the admission deduplication flipped. -/
def flipDedup (c : ConstitutionDesc) : ConstitutionDesc :=
  { c with dedupAdmit := !c.dedupAdmit }

/-- Admitting a token never changes quiescence: the verdict reads
requirements and views, not data. -/
theorem quiescent_admitTok (d : ConstitutionDesc) (w : World) (t : Nat) :
    quiescentB (interpStep d w (.admitTok t)) = quiescentB w := by
  simp only [interpStep]
  split <;> rfl

/-- Not every presentational difference among codes is a verdict
difference: a code and its `dedupAdmit` flip are never separated by one
quiescence verdict.  So `VSep` is strictly coarser than `≠` on the
carrier, and the boundary separation of §4 is a fact about behaviour,
not inequality of names. -/
theorem coded_pair_not_vsep (d : ConstitutionDesc) :
    ¬ VSep (some d) (some (flipDedup d)) := by
  intro ⟨⟨c, w⟩, e, h⟩
  apply h
  show quiescentB (interpStep d w e) = quiescentB (interpStep (flipDedup d) w e)
  cases e with
  | admitTok t => rw [quiescent_admitTok, quiescent_admitTok]
  | require i j => rfl
  | mark v p => rfl
  | addView c => rfl
  | refuse i j => rfl
  | note n => rfl
  | setBudget n => rfl
  | setAugLicense b => rfl

/-- At the genesis witness the closure family is empty either way: the
recorded self-requirement has no repair and no extension there. -/
theorem nextFamily_blind_at_genesis (c : ConstitutionDesc) :
    nextFamily ⟨interpStep c genesis (.require 0 0), .close⟩ = [] := by
  cases c with
  | mk a b cc d e f =>
    cases b <;> rfl

/-- Two admitted tokens, nothing else: reached from genesis by two
admissions. -/
def twoWorld : World :=
  { data := [0, 1], views := [], reqs := [], refusals := [],
    budget := 0, augLicensed := true, notes := [] }

theorem twoWorld_reached :
    replay [.admitTok 0, .admitTok 1] genesis = twoWorld := by decide

/-- At `twoWorld` the closure family reads the guard too: with the guard
off, the recorded self-requirement `(0, 0)` is violated and the
extension family offers the view `[0]` (twice, once per endpoint). -/
theorem family_reads_guard (c : ConstitutionDesc) :
    nextFamily ⟨interpStep c twoWorld (.require 0 0), .close⟩ =
      if c.guardRequire then [] else [[.addView [0]], [.addView [0]]] := by
  cases c with
  | mk a b cc d e f =>
    cases b <;> rfl

/-- The interpreter is separated from every step function at the
closure-family verdict as well. -/
theorem interp_not_step_family (s : World → Event → World) :
    ∃ c : ConstitutionDesc,
      nextFamily ⟨interpStep c twoWorld (.require 0 0), .close⟩ ≠
        nextFamily ⟨s twoWorld (.require 0 0), .close⟩ := by
  refine ⟨{ kernelDesc with guardRequire :=
    !(decide (nextFamily ⟨s twoWorld (.require 0 0), .close⟩ = [])) }, ?_⟩
  rw [family_reads_guard]
  generalize nextFamily ⟨s twoWorld (.require 0 0), .close⟩ = L
  cases hL : decide (L = []) with
  | true =>
      have := of_decide_eq_true hL
      subst this
      decide
  | false =>
      have := of_decide_eq_false hL
      simp only [Bool.not_false, ite_true]
      exact fun h => this h.symm

/-! ## 7. The aligned code, the guards, and well-formedness

Two findings of the review of 2026-10-28 are answered here with
theorems.

**Alignment.**  At a reflective world carrying the code `d`, the coded
member `some d` and the uncoded role `none` have the same meaning,
definitionally, at every event (`aligned_coded_equals_uncoded`), under
every function of the outcome (`aligned_no_verdict`) and along every
event sequence (`aligned_trajectory`).  So the separation `VSep (some d)
none` is witnessed only at a reflective world carrying another code
(`vsep_uncoded_iff`): the interpreter is told from a coded member by
nothing but its reading of the other codes.  No "self-representational"
difference exists at this type; the claim that one does is refuted.

**Guards.**  Two codes can differ at `(w, e)` only when a guard decides
there: when every guard of the kernel passes (`guardsPass w e = true`),
every code performs the sealed step (`codes_agree_of_guardsPass`), so a
quiescence difference between two codes needs a guard to decide
(`codes_separated_needs_guard`), and so does every separation of the
uncoded role (`vsep_uncoded_needs_guard`).  The reviewer's requested
lemma is the `require` instance (`require_guard_irrelevant`).

**Well-formedness.**  The `genesis` witness is a rejected challenge:
`reqOkB genesis 0 0 = false`, the kernel's outcome is well formed, and
the unguarded outcome is not (`genesis_witness_rejected`,
`genesis_witness_kernel_wf`, `genesis_witness_unguarded_not_wf`).  Every
other guard preserves well-formedness (`wf_interpStep`), and a second
witness uses one: `accWorld`, reached from `genesis` by five kernel
steps, is well formed; the event `mark [0] 1` is rejected by the
kernel's acceptance guard because it discharges nothing, while a code
with `guardAccept` off applies it and breaks the one requirement.  Both
outcomes are well formed and they disagree on quiescence
(`quiescent_reads_accept`, `accWorld_outputs_wf`); so the separation of
the interpreter from every step function (`interp_not_step_wf`) and
from every coded member (`vsep_uncoded_wf`) survives the requirement
that both executions preserve well-formedness.  What no witness can
remove is the deciding guard, by `codes_separated_needs_guard`. -/

/-- At a reflective world carrying `d`, the coded member `d` and the
uncoded role agree, definitionally. -/
theorem aligned_coded_equals_uncoded (d : ConstitutionDesc) (w : World)
    (e : Event) :
    meaning (some d) (d, w) e = meaning none (d, w) e := rfl

/-- Hence no function of the outcome, of any type, tells them apart
there. -/
theorem aligned_no_verdict {β : Type} (d : ConstitutionDesc) (w : World)
    (e : Event) (q : RWorld → β) :
    q (meaning (some d) (d, w) e) = q (meaning none (d, w) e) := rfl

/-- Along every event sequence from an aligned reflective world the two
trajectories coincide. -/
theorem aligned_trajectory (d : ConstitutionDesc) (w : World)
    (es : List Event) :
    es.foldl (meaning (some d)) (d, w) = es.foldl (meaning none) (d, w) := by
  induction es generalizing w with
  | nil => rfl
  | cons e es ih =>
      simp only [List.foldl]
      exact ih (interpStep d w e)

/-- The separation of the uncoded role from `some d` is witnessed
exactly at a reflective world carrying a code other than `d`. -/
theorem vsep_uncoded_iff (d : ConstitutionDesc) :
    VSep (some d) none ↔
      ∃ (c : ConstitutionDesc) (w : World) (e : Event),
        c ≠ d ∧ quiescentB (interpStep d w e) ≠ quiescentB (interpStep c w e) := by
  constructor
  · rintro ⟨⟨c, w⟩, e, h⟩
    refine ⟨c, w, e, ?_, h⟩
    intro hcd
    subst hcd
    exact h rfl
  · rintro ⟨c, w, e, _, h⟩
    exact ⟨(c, w), e, h⟩

/-- The kernel's guards at `(w, e)`: every condition the sealed step
tests before acting (the duplicate test of `admitTok`, `reqOkB`,
`markOkB` with the budget, `augOkB` with licence and budget, the
obstruction certificate of `refuse`).  The three inert events have no
guard. -/
def guardsPass (w : World) : Event → Bool
  | .admitTok t => !(decide (t ∈ w.data))
  | .require i j => reqOkB w i j
  | .mark v p => markOkB w v p && decide (0 < w.budget)
  | .addView c => augOkB w c && w.augLicensed && decide (0 < w.budget)
  | .refuse i j => obstructedB w (i, j)
  | .note _ => true
  | .setBudget _ => true
  | .setAugLicense _ => true

/-- When every guard passes, every code performs the sealed step. -/
theorem codes_agree_of_guardsPass (c : ConstitutionDesc) (w : World)
    (e : Event) (h : guardsPass w e = true) :
    interpStep c w e = step w e := by
  cases e with
  | admitTok t =>
      have hmem : ¬ t ∈ w.data := by
        simpa [guardsPass] using h
      simp [interpStep, step, hmem]
  | require i j =>
      simp only [guardsPass] at h
      simp [interpStep, step, h]
  | mark v p =>
      simp only [guardsPass, Bool.and_eq_true] at h
      simp [interpStep, step, h.1, h.2]
  | addView v =>
      simp only [guardsPass, Bool.and_eq_true] at h
      simp [interpStep, step, h.1.1, h.1.2, h.2]
  | refuse i j =>
      simp only [guardsPass] at h
      simp [interpStep, step, h]
  | note n => rfl
  | setBudget n => rfl
  | setAugLicense b => rfl

/-- The reviewer's requested instance: when `reqOkB w i j` holds, the
`guardRequire` toggle is irrelevant to `require i j`. -/
theorem require_guard_irrelevant (c : ConstitutionDesc) (w : World)
    (i j : Nat) (h : reqOkB w i j = true) :
    interpStep c w (.require i j) = step w (.require i j) :=
  codes_agree_of_guardsPass c w _ h

/-- A quiescence difference between two codes needs a guard to decide. -/
theorem codes_separated_needs_guard (c d : ConstitutionDesc) (w : World)
    (e : Event)
    (h : quiescentB (interpStep c w e) ≠ quiescentB (interpStep d w e)) :
    guardsPass w e = false := by
  cases hg : guardsPass w e with
  | false => rfl
  | true =>
      rw [codes_agree_of_guardsPass c w e hg,
        codes_agree_of_guardsPass d w e hg] at h
      exact absurd rfl h

/-- Every separation of the uncoded role from a coded member is at a
reflective world carrying another code, at an event where a guard
decides. -/
theorem vsep_uncoded_needs_guard (d : ConstitutionDesc)
    (h : VSep (some d) none) :
    ∃ (c : ConstitutionDesc) (w : World) (e : Event),
      c ≠ d ∧ guardsPass w e = false ∧
        quiescentB (interpStep d w e) ≠ quiescentB (interpStep c w e) := by
  obtain ⟨c, w, e, hne, hq⟩ := (vsep_uncoded_iff d).1 h
  exact ⟨c, w, e, hne, codes_separated_needs_guard d c w e hq, hq⟩

/-! ### The `genesis` witness is a rejected challenge -/

/-- The kernel rejects `require 0 0`: a datum is never required to be
separated from itself. -/
theorem genesis_witness_rejected : reqOkB genesis 0 0 = false := by decide

theorem genesis_witness_guard_decides :
    guardsPass genesis (.require 0 0) = false := by decide

theorem genesis_witness_kernel_wf : WF (step genesis (.require 0 0)) :=
  wf_step wf_genesis _

/-- With `guardRequire` off the recorded self-requirement breaks the
sealed well-formedness invariant. -/
theorem genesis_witness_unguarded_not_wf (c : ConstitutionDesc)
    (h : c.guardRequire = false) :
    ¬ WF (interpStep c genesis (.require 0 0)) := by
  intro hwf
  have hmem : ((0, 0) : Req) ∈ (interpStep c genesis (.require 0 0)).reqs := by
    simp [interpStep, h, genesis]
  exact (hwf _ hmem).1 rfl

/-! ### Well-formedness under every other guard -/

/-- `WF` reads only the requirement list and the number of data. -/
theorem wf_of_reqs_data {w w' : World} (hwf : WF w) (hr : w'.reqs = w.reqs)
    (hd : w.data.length ≤ w'.data.length) : WF w' := by
  intro r hr'
  rw [hr] at hr'
  obtain ⟨h1, h2, h3⟩ := hwf r hr'
  exact ⟨h1, Nat.lt_of_lt_of_le h2 hd, Nat.lt_of_lt_of_le h3 hd⟩

/-- Every code preserves well-formedness at every event, except a code
with `guardRequire` off at a `require`. -/
theorem wf_interpStep (c : ConstitutionDesc) {w : World} (hwf : WF w)
    (e : Event) (hreq : ∀ i j, e = .require i j → c.guardRequire = true) :
    WF (interpStep c w e) := by
  cases e with
  | admitTok t =>
      simp only [interpStep]
      split
      · exact hwf
      · exact wf_of_reqs_data hwf rfl (by simp)
  | require i j =>
      have hg := hreq i j rfl
      have : interpStep c w (.require i j) = step w (.require i j) := by
        simp [interpStep, step, hg]
      rw [this]
      exact wf_step hwf _
  | mark v p =>
      simp only [interpStep]
      split <;> exact wf_of_reqs_data hwf rfl (Nat.le_refl _)
  | addView v =>
      simp only [interpStep]
      split <;> exact wf_of_reqs_data hwf rfl (Nat.le_refl _)
  | refuse i j =>
      simp only [interpStep]
      split <;> exact wf_of_reqs_data hwf rfl (Nat.le_refl _)
  | note n => exact wf_of_reqs_data hwf rfl (Nat.le_refl _)
  | setBudget n => exact wf_of_reqs_data hwf rfl (Nat.le_refl _)
  | setAugLicense b => exact wf_of_reqs_data hwf rfl (Nat.le_refl _)

/-! ### A well-formedness-preserving witness -/

/-- Two tokens, one view `[0]`, one requirement `(0, 1)` that the view
satisfies, one unit of budget. -/
def accWorld : World :=
  { data := [0, 1], views := [[0]], reqs := [(0, 1)], refusals := [],
    budget := 1, augLicensed := true, notes := [] }

theorem accWorld_reached :
    replay [.admitTok 0, .admitTok 1, .require 0 1, .setBudget 2,
      .addView [0]] genesis = accWorld := by decide

theorem accWorld_wf : WF accWorld := by
  unfold WF
  decide

/-- The kernel rejects `mark [0] 1`: it discharges no requirement. -/
theorem accWorld_kernel_rejects : markOkB accWorld [0] 1 = false := by decide

theorem accWorld_guard_decides :
    guardsPass accWorld (.mark [0] 1) = false := by decide

theorem accWorld_step_fixed : step accWorld (.mark [0] 1) = accWorld := by
  decide

/-- One verdict reads the acceptance guard: a code with it off applies
the mark, which puts `1` into the view and so stops separating `0`
from `1`. -/
theorem quiescent_reads_accept (c : ConstitutionDesc) :
    quiescentB (interpStep c accWorld (.mark [0] 1)) = c.guardAccept := by
  cases c with
  | mk a b cc d e f =>
    cases a <;> cases b <;> cases cc <;> cases d <;> cases e <;> cases f
      <;> decide

/-- Both outcomes are well formed, under every code. -/
theorem accWorld_outputs_wf (c : ConstitutionDesc) :
    WF (interpStep c accWorld (.mark [0] 1)) :=
  wf_interpStep c accWorld_wf _ (fun _ _ h => nomatch h)

/-- The code with the acceptance guard flipped. -/
def flipAccept (c : ConstitutionDesc) : ConstitutionDesc :=
  { c with guardAccept := !c.guardAccept }

/-- The interpreter is separated from every step function at a
well-formed world reached by the kernel, by a well-formed outcome. -/
theorem interp_not_step_wf (s : World → Event → World) :
    ∃ c : ConstitutionDesc,
      WF (interpStep c accWorld (.mark [0] 1)) ∧
        quiescentB (interpStep c accWorld (.mark [0] 1)) ≠
          quiescentB (s accWorld (.mark [0] 1)) := by
  refine ⟨{ kernelDesc with
    guardAccept := !(quiescentB (s accWorld (.mark [0] 1))) },
    accWorld_outputs_wf _, ?_⟩
  rw [quiescent_reads_accept]
  generalize quiescentB (s accWorld (.mark [0] 1)) = b
  cases b <;> decide

/-- The uncoded role is separated from every coded member at a
well-formed world, with both outcomes well formed. -/
theorem vsep_uncoded_wf (d : ConstitutionDesc) :
    ∃ (c : ConstitutionDesc) (w : World) (e : Event),
      WF w ∧ WF (interpStep d w e) ∧ WF (interpStep c w e) ∧
        quiescentB (interpStep d w e) ≠ quiescentB (interpStep c w e) := by
  refine ⟨flipAccept d, accWorld, .mark [0] 1, accWorld_wf,
    accWorld_outputs_wf d, accWorld_outputs_wf _, ?_⟩
  rw [quiescent_reads_accept, quiescent_reads_accept]
  show d.guardAccept ≠ (!d.guardAccept)
  cases d.guardAccept <;> decide

end ResearchInterpreterVerdict
