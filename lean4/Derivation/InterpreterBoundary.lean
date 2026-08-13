import Derivation.Constitution
import Derivation.PrimitiveCore

/-!
# Phase VIII — the interpreter boundary (I0–I5)

The constitution module (`Derivation.Constitution`) seals a 64-member
description family (`ConstitutionDesc`, `allDescs`,
`allDescs_complete`) with one fixed family evaluator (`interpStep`)
and a verified self-description (`interp_describe`).  The family
evaluator is a function over the codes and is not itself a code; this
module makes that boundary the object of study.

* **I0** — the sealed status restated (`i0_status`): evaluation of the
  declared family is total and metatheoretic; quotation, executable
  description, and verified self-description are already separated by
  `Constitution.interp_describe` and `Constitution.allDescs_complete`.
* **I1** — `tower_persists`: for every finite list of codes and every
  evaluation map into `World → Event → World`, some function of that
  same type differs from every coded interpreter — a finite diagonal
  construction indexed by the world's carrier length.  Every
  represented finite interpreter family misses an interpreter, at
  every level, uniformly.
* **I2** — `i2_universal_in_class`: the code type `ConstitutionDesc`
  with evaluator `interpStep` covers the declared 64-family exactly
  (a restatement of `allDescs_complete` + `interp_describe`;
  "universal" is scoped to this declared class and nothing wider).
* **I3** — `evalOpt`: the typed-refusal evaluator over
  `Option ConstitutionDesc`.  The `none` code is a named new top that
  refuses self-evaluation (`i3_partial_top_refuses`); adding it is
  consistent (the definition compiles and its verdicts are `rfl`),
  while a total same-type top absorbed into a finite code family is
  impossible by `tower_persists`.  The boundary closes only by
  admitting typed refusal — partiality of the extended evaluator —
  never by a total same-type recoding.
* **I4** — `family_missed`: the recursion route.  `kernelDesc` is a
  description-level fixed point (`interp_describe`) and NOT an
  evaluation-level one: instantiating `tower_persists` at
  `cs := allDescs`, `ev := interpStep` yields a function of
  interpreter type that no family member evaluates to.
* **I5** — the boundary IS a primitive difference: `boundarySetting`
  places the 64 coded occurrences and one uncoded occurrence (the
  interpreter role, `none`) on a single carrier and witnesses the pair
  (kernel description, interpreter role).  `i5_boundary_is_A` (pointed
  witnessed irreflexive), `i5_boundary_is_F` (retained and protected —
  both stores are declared data, priced as such),
  `i5_collapse_obstructed` (identifying the endpoints loses
  irreflexivity of the pushforward, via
  `PrimDiff.obstruction_under_irrefl`), and `i5_difference_grounded`
  (the non-identification is behavioral, not notational:
  `family_missed`).

Conclusion tags: INTERPRETER_TOWER_PERSISTS (`tower_persists`) and
INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE (`i5_boundary_is_A` +
`i5_collapse_obstructed` + `i5_difference_grounded`).  NOT claimed: an
absolute no-outside.  These theorems bound every finite, represented
closure of the code family; they do not — and in this calculus cannot
— state that nothing exists beyond the represented apparatus.
-/

namespace InterpreterBoundary

open Represented Constitution

/-! ## I0 — the fixed external interpreter, sealed status restated

The real content of I0 is already proved and sealed elsewhere:
`Constitution.interp_describe` (the kernel's own description executes
to exactly the sealed step) and `Constitution.allDescs_complete` (the
64-member description family is exhaustively enumerated).  Quotation
(a `ConstitutionDesc` is inert data), executable description
(`interpStep d` is a semantics run by the fixed evaluator), and
verified self-description (`interp_describe`) are three separate
notions and remain separate here.  Evaluation of the family is total
and metatheoretic: `interpStep` is defined on every code and every
world/event, and it is constitution, not represented state.  A vacuous
restatement (`∀ d w e, interpStep d w e = interpStep d w e`) is not a
theorem worth exporting; the status string below records the sealed
facts with their proof names instead. -/

/-- I0 status summary (data, not proof — the cited proofs are
`Constitution.interp_describe` and `Constitution.allDescs_complete`). -/
def i0_status : String :=
  "I0: evaluation of the declared 64-member description family is "
    ++ "total and metatheoretic (interpStep is a fixed function over "
    ++ "all codes, not a code); quotation / executable description / "
    ++ "verified self-description are separated by "
    ++ "Constitution.interp_describe and Constitution.allDescs_complete."

/-! ## I1 — every finite closure has a new top -/

/-- The world whose carrier length encodes the index `i`: its data
store is `List.range i`.  Only the length is load-bearing. -/
def indexWorld (i : Nat) : World :=
  ⟨List.range i, [], [], [], 0, true, []⟩

theorem indexWorld_len (i : Nat) : (indexWorld i).data.length = i :=
  List.length_range

/-- The diagonal interpreter against a finite code list `cs` under an
evaluation map `ev`: at a world whose carrier length is a valid index
into `cs`, run the interpreter coded at that index and then extend the
notes by one extra element; elsewhere, do nothing.  The extension is
on `notes`, the transition-inert commentary field, so the construction
perturbs no acceptance guard — it differs from the indexed interpreter
purely by output shape. -/
def diag {C : Type} (cs : List C) (ev : C → World → Event → World)
    (w : World) (e : Event) : World :=
  (cs[w.data.length]?).elim w
    (fun c => { ev c w e with notes := (ev c w e).notes ++ [999] })

theorem diag_hit {C : Type} {cs : List C}
    (ev : C → World → Event → World) {w : World} {c : C}
    (h : cs[w.data.length]? = some c) (e : Event) :
    diag cs ev w e =
      { ev c w e with notes := (ev c w e).notes ++ [999] } := by
  unfold diag
  rw [h]
  rfl

/-- **I1, the load-bearing theorem: every finite closure has a new
top.**  For every finite list of codes `cs` and every evaluation map
`ev` into `World → Event → World`, there is a function of that same
type differing from every coded interpreter.  Proof: the diagonal
`diag cs ev` — against the code at position `i`, evaluate both at the
world of carrier length `i`; the diagonal's notes are one element
longer, so the functions differ at that argument.  Consequence, and
the content of the tag INTERPRETER_TOWER_PERSISTS: every represented
finite interpreter family misses an interpreter, at every level,
uniformly — recoding the missed function as a 65th code only produces
a new finite family to which the theorem applies again. -/
theorem tower_persists {C : Type} (cs : List C)
    (ev : C → World → Event → World) :
    ∃ f : World → Event → World, ∀ c ∈ cs, f ≠ ev c := by
  refine ⟨diag cs ev, ?_⟩
  intro c hc hEq
  obtain ⟨i, hi⟩ := List.getElem?_of_mem hc
  have hidx : cs[(indexWorld i).data.length]? = some c := by
    rw [indexWorld_len]
    exact hi
  have happ : diag cs ev (indexWorld i) (.note 0) =
      ev c (indexWorld i) (.note 0) :=
    congrFun (congrFun hEq (indexWorld i)) (Event.note 0)
  rw [diag_hit ev hidx (Event.note 0)] at happ
  have hlen : ((ev c (indexWorld i) (.note 0)).notes ++ [999]).length =
      (ev c (indexWorld i) (.note 0)).notes.length :=
    congrArg (fun w : World => w.notes.length) happ
  simp only [List.length_append, List.length_cons,
    List.length_nil] at hlen
  omega

/-! ## I2 — universal code + evaluator for the DECLARED family

Three distinctions, kept separate (the string tags below record them
as data):

* **quotation** — a `ConstitutionDesc` is inert data;
* **interpretation** — `interpStep d` is the execution of the code
  `d` by the fixed family evaluator;
* **self-description** — `interp_describe` verifies the kernel's own
  code against the sealed step;
* **self-application** — ill-typed at the family level: the evaluator
  consumes codes and is not itself coded, and by `tower_persists` no
  finite recoding closes this (each recoding yields a finite family
  that again misses an interpreter);
* **verified fixed point** — `interp_describe` is a description-level
  fixed point, NOT an evaluation-level one (see `family_missed`). -/

/-- **I2.**  The code type `ConstitutionDesc` with evaluator
`interpStep` covers the declared 64-family exactly: every code is
enumerated (`Constitution.allDescs_complete`) and the kernel's code
executes to the sealed step (`Constitution.interp_describe`).
"Universal" is scoped to this declared class — the 64-member toggle
family under its fixed evaluator — and to nothing wider. -/
theorem i2_universal_in_class :
    (∀ d : ConstitutionDesc, d ∈ allDescs) ∧
      (∀ (w : World) (e : Event),
        interpStep kernelDesc w e = step w e) :=
  ⟨allDescs_complete, interp_describe⟩

def tag_quotation : String :=
  "quotation: a ConstitutionDesc is inert data"

def tag_interpretation : String :=
  "interpretation: interpStep d is execution of code d by the fixed evaluator"

def tag_self_description : String :=
  "self-description: interp_describe verifies kernelDesc against the sealed step"

def tag_self_application : String :=
  "self-application: ill-typed at the family level - the evaluator "
    ++ "consumes codes and is not itself coded; tower_persists shows no "
    ++ "finite recoding closes this"

def tag_verified_fixed_point : String :=
  "verified fixed point: interp_describe is description-level, not evaluation-level"

/-! ## I3 — typed refusal closes what totality cannot

The evaluator is extended by one occurrence: the code store becomes
`Option ConstitutionDesc`, and the `none` code is the named new top
that REFUSES evaluation.  The refusing top is consistent — the
construction compiles and both verdicts below are `rfl`.  A TOTAL
same-type top is impossible: by `tower_persists`, any finite family of
codes evaluated into `World → Event → World` misses a function of that
type, so no finite total recoding absorbs the evaluator role.  The
boundary closes only by admitting typed refusal — partiality of the
extended evaluator, carried in the `Option` codomain as data — never
by totality. -/

/-- The typed-refusal evaluator: coded members evaluate as before
(wrapped in `some`); the uncoded top `none` refuses. -/
def evalOpt (c : Option ConstitutionDesc) (w : World) (e : Event) :
    Option World :=
  match c with
  | some d => some (interpStep d w e)
  | none => none

/-- The named new top refuses self-evaluation — by definition, and
that is the point: refusal here is a typed verdict (`none` in the
codomain), not a hidden failure. -/
theorem i3_partial_top_refuses :
    evalOpt none = fun _ _ => none := rfl

/-- The extended evaluator covers the declared family exactly: on
coded members it is the sealed family evaluation, wrapped. -/
theorem i3_partial_covers (d : ConstitutionDesc) (w : World)
    (e : Event) : evalOpt (some d) w e = some (interpStep d w e) := rfl

/-! ## I4 — recursion route: self-description without self-evaluation

`kernelDesc` is a description-level fixed point: `interp_describe`
proves its execution equals the sealed step.  An evaluation-level
fixed point would require a family member to BE the evaluator; the
members' step functions have type `World → Event → World` while the
evaluator has type `ConstitutionDesc → World → Event → World`, so the
identification is ill-typed — definitionally, not merely unproved.
The honest content theorem is the instantiation of `tower_persists`
at the sealed family itself: -/

/-- **I4.**  The declared 64-family, evaluated by its own fixed
evaluator, provably misses an interpreter-grade function: direct
instantiation of `tower_persists` at `cs := allDescs`,
`ev := interpStep`.  Self-description (`interp_describe`) therefore
never becomes self-evaluation: description-level closure coexists
with evaluation-level escape. -/
theorem family_missed :
    ∃ f : World → Event → World, ∀ d ∈ allDescs, f ≠ interpStep d :=
  tower_persists allDescs interpStep

/-! ## I5 — the boundary IS a primitive difference

The carrier `Option ConstitutionDesc` has the 64 coded occurrences
(`some d`) plus ONE uncoded occurrence — the interpreter role,
`none`.  The witnessed difference is the pair (kernel description,
interpreter role).  Retention and protection here are DECLARED: the
stores are data supplied with the setting, and their price is recorded
as such — what is NOT merely declared is the ground of the difference,
which is behavioral (`i5_difference_grounded` below). -/

/-- The interpreter boundary as a `PrimitiveCore.Setting`: carrier
`Option ConstitutionDesc` (65 occurrences), asserted difference =
retention store = protected-demand store = exactly the pair (kernel
code, interpreter role), no admitted operations. -/
def boundarySetting : PrimitiveCore.Setting where
  X := Option ConstitutionDesc
  r := fun x y => x = some kernelDesc ∧ y = none
  a := some kernelDesc
  b := none
  ret := fun x y => x = some kernelDesc ∧ y = none
  prot := fun x y => x = some kernelDesc ∧ y = none
  Ops := fun _ => False

/-- The carrier's occurrence count: 64 coded occurrences plus the one
uncoded interpreter role. -/
theorem i5_carrier_occurrences :
    ((allDescs.map Option.some) ++
      ([none] : List (Option ConstitutionDesc))).length = 65 := by
  decide

/-- **I5, candidate A** — the boundary is a pointed witnessed
irreflexive difference: the pair (kernel code, interpreter role) is
asserted, and no occurrence differs from itself (a self-pair would
force `some kernelDesc = none`). -/
theorem i5_boundary_is_A : PrimitiveCore.A boundarySetting :=
  ⟨⟨rfl, rfl⟩, fun _x h => nomatch h.1.symm.trans h.2⟩

/-- **I5, candidate F** — the boundary difference is retained and
protected.  Scope, stated exactly: retention and protection are
DECLARED here — the `ret` and `prot` stores are data of
`boundarySetting`, priced as declarations; the theorem records that
the declared stores do cover the witnessed pair. -/
theorem i5_boundary_is_F : PrimitiveCore.F boundarySetting :=
  ⟨i5_boundary_is_A, ⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩

/-- **I5, collapse obstruction** — any map `q` identifying the two
endpoints loses irreflexivity of the pushforward: the identification
is obstructed relative to the protected law `Irrefl`
(`PrimDiff.obstruction_under_irrefl`, instantiated at the boundary
witness). -/
theorem i5_collapse_obstructed {β : Type}
    (q : Option ConstitutionDesc → β)
    (hq : q (some kernelDesc) = q none) :
    PrimDiff.FidelityObstruction PrimDiff.Irrefl
      boundarySetting.r q :=
  PrimDiff.obstruction_under_irrefl ⟨rfl, rfl⟩ hq

/-- **I5, the ground of the difference** — the non-identification of
(kernel code, interpreter role) is behaviorally grounded, not
notational: by `family_missed` (the proof term of this theorem), no
total same-type recoding absorbs the interpreter role into the coded
occurrences — the family's own evaluation misses an interpreter-grade
function, so the uncoded occurrence names a genuinely unabsorbed
behavior, not a spelling. -/
theorem i5_difference_grounded :
    ∃ f : World → Event → World, ∀ d ∈ allDescs, f ≠ interpStep d :=
  family_missed

/-- The exported conclusion tags.  NOT included, and not claimed: any
absolute no-outside tag — the theorems above bound finite represented
closures and say nothing about what lies beyond the represented
apparatus. -/
def conclusionTags : List String :=
  ["INTERPRETER_TOWER_PERSISTS",
   "INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE"]

end InterpreterBoundary
