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

This file does both, in six steps.

1. One verdict reads one guard.  At `genesis`, under the event
   `require 0 0`, the quiescence verdict of the world the interpreter
   produces under code `c` is exactly `c.guardRequire`
   (`quiescent_reads_guard`); the obstruction certificate for `(0, 0)`
   is its negation (`obstructed_reads_guard`).
2. The interpreter is not a step function.  For every
   `s : World → Event → World` there is a code `c` on which the
   interpreter and `s` disagree at that verdict (`interp_not_step`).
   Every coded member is such an `s` (`coded_member_separated`), and
   so is the diagonal function of `tower_persists`.
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
   separated from every coded member (`vsep_uncoded`).  The setting
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
   difference (`verdict_entails_supp`); the scratch result
   `tower_persists_operational` of 2026-10-27 gave the support half.
6. Limits.  Not every presentational difference among codes is a
   verdict difference: a code and the code with `dedupAdmit` flipped are
   never separated by one quiescence verdict
   (`coded_pair_not_vsep`), so `VSep` is strictly coarser than `≠` on
   the carrier.  At the `genesis` witness the closure family
   `nextFamily` is empty either way (`nextFamily_blind_at_genesis`);
   the two-token world `twoWorld`, reached by two admissions, separates
   it (`family_reads_guard`, `interp_not_step_family`).

Not claimed: locatedness (candidate `Bl`) of `VSep`; retention and
protection of the pair other than by declaring the stores to be `VSep`
(`boundary_F`, same status as `i5_boundary_is_F`); anything about
evaluators of other types; an absolute no-outside.
-/

namespace ResearchInterpreterVerdict

open Represented Constitution InterpreterBoundary

/-! ## 1. One verdict reads one guard -/

theorem reqOkB_genesis_zero : reqOkB genesis 0 0 = false := by decide

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

/-- **The two laws leave no freedom.**  Any reflective step that
interprets and quotes is `rstep`.  Contrast `arbitrary_uncoded_assignment`
in the sealed module: at step-function type the uncoded role can be
given any meaning; at reflective type the laws fix it. -/
theorem lawful_unique (g : RWorld → Event → RWorld)
    (h1 : Interprets g) (h2 : Quotes g) : g = rstep := by
  funext p e
  obtain ⟨c, w⟩ := p
  calc g (c, w) e = ((g (c, w) e).1, (g (c, w) e).2) := rfl
    _ = (c, interpStep c w e) := by rw [h1 c w e, h2 c w e]

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

/-- A reading of the carrier that keeps every coded member's meaning. -/
def Reading (I : Option ConstitutionDesc → RWorld → Event → RWorld) :
    Prop :=
  ∀ d, I (some d) = meaning (some d)

/-- **Identifying the uncoded role with any coded member changes a
quiescence verdict.**  Any reading that keeps the coded meanings and
reads `none` as some coded member reports, at an accessible reflective
world, a quiescence verdict different from the lawful meaning's. -/
theorem identification_changes_quiescence
    (I : Option ConstitutionDesc → RWorld → Event → RWorld)
    (hI : Reading I) (d : ConstitutionDesc) (hid : I none = I (some d)) :
    ∃ (p : RWorld) (e : Event),
      quiescentB (I none p e).2 ≠ quiescentB (rstep p e).2 := by
  obtain ⟨p, e, h⟩ := rstep_not_lift (interpStep d)
  refine ⟨p, e, ?_⟩
  rw [hid, hI d]
  exact fun h' => h h'.symm

/-- Stronger: reading `none` as the lift of ANY step function — a coded
member, the missed function of `tower_persists`, any other — changes a
quiescence verdict.  The occurrence the coding omits is not of step
type. -/
theorem identification_with_step_changes_quiescence
    (I : Option ConstitutionDesc → RWorld → Event → RWorld)
    (s : World → Event → World) (hid : I none = liftStep s) :
    ∃ (p : RWorld) (e : Event),
      quiescentB (I none p e).2 ≠ quiescentB (rstep p e).2 := by
  obtain ⟨p, e, h⟩ := rstep_not_lift s
  refine ⟨p, e, ?_⟩
  rw [hid]
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

end ResearchInterpreterVerdict
