import Derivation.InterpreterBoundary
import ResearchTwoTheorems.Institution

/-!
# Theorem II, the interpreter level — where wisdom stops

AuthorityEffect: None.  Outside the seal.

Question-level wisdom (`Institution.wise_of_represented`) decides every
question against a fixed represented family.  It does not extend to an
institution's own catalogue of members:

* `no_closed_self_interpreter`: no evaluator `ev : C → C → Bool` on a code
  type `C` has every function `C → Bool` among its rows.  The diagonal
  argument, in core Lean, with no axiom at all.
* `diag_not_member`: a catalogue's diagonal question is a member of no
  finite institution drawn from the catalogue — membership incompleteness
  is universal.
* `diag_known_witness`, `diag_unknown_witness`: the same uncatalogued
  diagonal is *known* to one institution of the catalogue and *unknown*
  to another — knowledge incompleteness is contingent.  Membership and
  knowledge come apart.
* `tower_persists_operational`: Genesis's `tower_persists` diagonal misses
  every coded interpreter only in the inert `notes` field; a diagonal that
  differs in the represented support also misses every coded interpreter.
  It is a diagonal over *unrestricted* world functions: `opDiag` appends a
  datum under `.note`, which the declared `step` never does
  (`opDiag_not_lawful`, `step_note_data`), so it is no interpreter and no
  lawful transition.  The interpreter is not derivable inside; it is
  supplied, as the irreflexivity admission is.  Genesis's
  `openDenotationalBridge` stays OPEN; nothing here closes it.
* `lawful_escape_iff`, `lawful_no_escape`: a function lawful on the
  represented support (agreeing with `step` there everywhere) escapes a
  catalogue exactly when no code of the catalogue is lawful; one lawful
  code closes the escape.  So the stronger tower statement, a lawful
  diagonal, holds only against catalogues that implement the transition
  nowhere.
* `no_closed_self_interpreter_fin`: the finite form on codes `Fin n`.  The
  general theorem is metatheory over any type `C`, infinite ones included.
-/

namespace ResearchTwoTheorems
namespace Diagonal

open Represented Compression Institution

/-- **No closed self-interpreter.**  Whatever `ev` is, the function that
runs each code on itself and flips the answer is no row of `ev`. -/
theorem no_closed_self_interpreter {C : Type} (ev : C → C → Bool) :
    ¬ ∀ f : C → Bool, ∃ c, ∀ x, ev c x = f x := by
  intro h
  obtain ⟨c, hc⟩ := h (fun x => !(ev x x))
  have hcc := hc c
  cases hev : ev c c <;> rw [hev] at hcc <;> exact Bool.noConfusion hcc

/-- The finite form, on codes `Fin n`: the one the tree's finite objects
instantiate.  `no_closed_self_interpreter` itself is metatheory over any
type `C`. -/
theorem no_closed_self_interpreter_fin (n : Nat) (ev : Fin n → Fin n → Bool) :
    ¬ ∀ f : Fin n → Bool, ∃ c, ∀ x, ev c x = f x :=
  no_closed_self_interpreter ev

/-- A catalogue of presentations coded by naturals, and the institution of
its first `n` members. -/
def catalogue (code : Nat → Nat → Nat) (n : Nat) : Institution :=
  (List.range n).map code

/-- The diagonal question of a catalogue. -/
def diag (code : Nat → Nat → Nat) : Nat → Nat := fun x => code x x + 1

theorem diag_ne_coded (code : Nat → Nat → Nat) (n : Nat) :
    code n n ≠ diag code n :=
  fun h => Nat.succ_ne_self (code n n) h.symm

/-- Membership incompleteness is universal: the diagonal is a member of
no institution drawn from the catalogue. -/
theorem diag_not_member (code : Nat → Nat → Nat) (n : Nat) :
    diag code ∉ catalogue code n := by
  intro h
  obtain ⟨m, _, hm⟩ := List.mem_map.mp h
  exact diag_ne_coded code m (congrArg (fun f => f m) hm)

/-- A catalogue: the `n`-th member reads `x` modulo `n + 1`. -/
def modCode (n x : Nat) : Nat := x % (n + 1)

/-- Knowledge incompleteness is contingent, witness one: the institution
of the first three members knows the uncatalogued diagonal. -/
theorem diag_known_witness :
    Knows [0, 1, 2, 3] (catalogue modCode 3) (diag modCode) := by decide

/-- Witness two: the institution of the first two members does not. -/
theorem diag_unknown_witness :
    ¬ Knows [0, 1, 2, 3] (catalogue modCode 2) (diag modCode) := by decide

/-- Membership and knowledge come apart. -/
theorem membership_vs_knowledge :
    (∀ n, diag modCode ∉ catalogue modCode n) ∧
    Knows [0, 1, 2, 3] (catalogue modCode 3) (diag modCode) ∧
    ¬ Knows [0, 1, 2, 3] (catalogue modCode 2) (diag modCode) :=
  ⟨diag_not_member modCode, diag_known_witness, diag_unknown_witness⟩

/-! ## The interpreter tower, operational form -/

open InterpreterBoundary in
/-- A diagonal that differs from the `i`-th coded interpreter in the
represented support, not only in notes. -/
def opDiag {C : Type} (cs : List C) (ev : C → World → Event → World)
    (w : World) (e : Event) : World :=
  (cs[w.data.length]?).elim w
    (fun c => { ev c w e with data := (ev c w e).data ++ [0] })

open InterpreterBoundary in
/-- Every finite family of coded interpreters is missed by a diagonal
that differs in the represented support, so the miss is operational,
not an artefact of the inert notes field used by Genesis's own
diagonal. -/
theorem tower_persists_operational {C : Type} (cs : List C)
    (ev : C → World → Event → World) :
    ∃ f : World → Event → World, ∀ c ∈ cs,
      ∃ w e, supp (f w e) ≠ supp (ev c w e) := by
  refine ⟨opDiag cs ev, ?_⟩
  intro c hc
  obtain ⟨i, hi⟩ := List.getElem?_of_mem hc
  refine ⟨indexWorld i, .note 0, ?_⟩
  have hidx : cs[(indexWorld i).data.length]? = some c := by
    rw [indexWorld_len]; exact hi
  intro h
  have hd := congrArg (fun s : Supp => s.data.length) h
  simp only [opDiag, hidx, Option.elim, supp, List.length_append,
    List.length_cons, List.length_nil] at hd
  omega

/-! ## Lawful functions: the diagonal is unrestricted, and what a lawful
one can escape (2026-10-28, after review) -/

/-- Lawful on the represented support: the function agrees with the
declared transition `step` on every world and event, up to the inert
notes. -/
def Lawful (f : World → Event → World) : Prop :=
  ∀ w e, supp (f w e) = supp (step w e)

theorem step_lawful : Lawful step := fun _ _ => rfl

/-- The declared transition keeps the data under a note. -/
theorem step_note_data (w : World) (n : Nat) :
    (step w (.note n)).data = w.data := rfl

/-- Wherever a code sits at the world's index, `opDiag` appends a datum. -/
theorem opDiag_appends {C : Type} (cs : List C)
    (ev : C → World → Event → World) (w : World) (e : Event) (c : C)
    (h : cs[w.data.length]? = some c) :
    (opDiag cs ev w e).data = (ev c w e).data ++ [0] := by
  simp only [opDiag, h, Option.elim]

open InterpreterBoundary in
/-- **The diagonal is not lawful.**  With any code at index `0`, `opDiag`
appends a datum under `.note 0` at the empty-data world, which `step` never
does: it escapes the catalogue by an operation the declared transition does
not authorize.  `tower_persists_operational` is therefore a diagonal over
unrestricted world functions, not over interpreters. -/
theorem opDiag_not_lawful {C : Type} (c : C) (cs : List C)
    (ev : C → World → Event → World) : ¬ Lawful (opDiag (c :: cs) ev) := by
  intro h
  have hidx : (c :: cs)[(indexWorld 0).data.length]? = some c := by
    rw [indexWorld_len]; rfl
  have h1 := congrArg (fun s : Supp => s.data.length)
    (h (indexWorld 0) (.note 0))
  simp only [supp] at h1
  rw [opDiag_appends (c :: cs) ev (indexWorld 0) (.note 0) c hidx,
    step_note_data] at h1
  simp only [indexWorld, List.length_append, List.length_cons, List.length_nil,
    List.length_range] at h1
  omega

/-- **A lawful diagonal escapes a catalogue exactly when no code of the
catalogue is lawful.**  Right to left the escaping function is `step`
itself.  The stronger tower statement, a diagonal that respects the
admitted transition and still misses every coded interpreter, holds only
against catalogues that implement the transition nowhere. -/
theorem lawful_escape_iff {C : Type} (cs : List C)
    (ev : C → World → Event → World) :
    (∃ f, Lawful f ∧ ∀ c ∈ cs, ∃ w e, supp (f w e) ≠ supp (ev c w e)) ↔
      (∀ c ∈ cs, ∃ w e, supp (ev c w e) ≠ supp (step w e)) := by
  constructor
  · intro ⟨f, hf, h⟩ c hc
    obtain ⟨w, e, hne⟩ := h c hc
    exact ⟨w, e, fun heq => hne (by rw [hf w e, heq])⟩
  · intro h
    refine ⟨step, step_lawful, fun c hc => ?_⟩
    obtain ⟨w, e, hne⟩ := h c hc
    exact ⟨w, e, fun heq => hne heq.symm⟩

/-- One lawful code in the catalogue, and no lawful function escapes it. -/
theorem lawful_no_escape {C : Type} (cs : List C)
    (ev : C → World → Event → World) {c₀ : C} (hc : c₀ ∈ cs)
    (hev : Lawful (ev c₀)) (f : World → Event → World) (hf : Lawful f) :
    ¬ ∀ c ∈ cs, ∃ w e, supp (f w e) ≠ supp (ev c w e) := by
  intro h
  obtain ⟨w, e, hne⟩ := h c₀ hc
  exact hne (by rw [hf w e, hev w e])

end Diagonal
end ResearchTwoTheorems
