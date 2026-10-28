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
  The interpreter is not derivable inside; it is supplied, as the
  irreflexivity admission is.  Genesis's `openDenotationalBridge` stays
  OPEN; nothing here closes it.
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

end Diagonal
end ResearchTwoTheorems
