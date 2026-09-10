import RepresentedEmitter

/-!
Scoped negative for the represented two-edge instance channel.

Class `InClass` is the stored form-0 ternary instruction of Stage 3.
It does not mention E1, owed-separation, or separability. It is nonempty
and contains every `Enabled` program's instruction.

E1 here is *native store*: a sealed step writes a new instance without
being that instance's `admitInst` event. That is the Target 1 item-3
demand. It is unsatisfiable by `new_stored_instance_needs_event`.

This closes OB-1 negatively for this class only. It does not license a
general close. Literal `reqs` E2 is not used.

AuthorityEffect: None.
-/

namespace InstanceDemand.NoGo
open Derivation
open InstanceDemand
open InstanceDemand.Emitter

/-- Stored Stage-3 instruction. Membership does not mention the output. -/
def InClass (r : Regime) (c : Inst) : Prop :=
  ∃ k l o, c = (0, [k, l, o]) ∧ c ∈ r.insts

/-- Native production: a sealed step stores `out` without being `admitInst` of `out`. -/
def E1 (r s : Regime) (e : Event) (out : Inst) : Prop :=
  stepE r e = some s ∧ out ∈ s.insts ∧ out ∉ r.insts ∧
    e ≠ Event.admitInst out.1 out.2

/-- Owed pair at the pre-state; the step is not an `impose`. Not `reqs` membership. -/
def E2prime (r : Regime) (e : Event) (i j : Nat) : Prop :=
  ¬ separable r i j ∧ (∀ x y, e ≠ Event.impose x y)

/-- Non-vacuous: the designated pair is not already separable. -/
def E3 (r : Regime) (i j : Nat) : Prop :=
  ¬ separable r i j

theorem class_nonempty : ∃ r c, InClass r c :=
  ⟨seed 3 0 2 1 false, (0, [0, 1, 2]), ⟨0, 1, 2, rfl, by simp [seed]⟩⟩

theorem class_covers_enabled {r : Regime} {i : Inst}
    (h : Enabled r.insts i) : ∃ c, InClass r c := by
  rcases h with ⟨k, l, o, _x, _z, _y, hc, _, _, _, _⟩
  exact ⟨(0, [k, l, o]), ⟨k, l, o, rfl, hc⟩⟩

theorem e1_impossible {r s : Regime} {e : Event} {out : Inst}
    (h : E1 r s e out) : False :=
  h.2.2.2 (new_stored_instance_needs_event h.1 h.2.1 h.2.2.1)

theorem no_member_is_endogenous
    {r s : Regime} {e : Event} {c out : Inst} {i j : Nat}
    (_hc : InClass r c)
    (h : E1 r s e out ∧ E2prime r e i j ∧ E3 r i j) : False :=
  e1_impossible h.1

theorem shape_uncovered_fails_native_join :
    Enabled (seed 3 0 2 1 false).insts (5, [0, 1]) ∧
      ¬ derivable (seed 3 0 2 1 false) (5, [0, 1]) :=
  native_closure_counterexample

theorem shape_imposed_fails_E2p {r : Regime} {i j : Nat} :
    ¬ E2prime r (Event.impose i j) i j := by
  intro h
  exact h.2 i j rfl

theorem shape_separated_fails_E3 {n x y : Nat}
    (hne : x ≠ y) (hy : y < n) :
    ¬ E3 (lone n x y) x y :=
  fun h => h (lone_pair_separates n x y hne hy)

/-- A seventh constructor that wrote instances without being `admitInst`
    of the new tuple would sit outside the sealed `Event` type. -/
theorem missing_operation_is_extension {r s : Regime} {e : Event} {i : Inst}
    (h : stepE r e = some s) (hi : i ∈ s.insts) (hn : i ∉ r.insts) :
    e = Event.admitInst i.1 i.2 :=
  new_stored_instance_needs_event h hi hn

theorem class_contains_seed_instruction :
    InClass (seed 3 0 2 1 false) (0, [0, 1, 2]) :=
  ⟨0, 1, 2, rfl, by simp [seed]⟩

theorem covered_seed_instruction :
    InClass (seed 3 0 2 1 true) (0, [0, 1, 2]) :=
  ⟨0, 1, 2, rfl, by simp [seed]⟩

end InstanceDemand.NoGo

#print axioms InstanceDemand.NoGo.class_nonempty
#print axioms InstanceDemand.NoGo.class_covers_enabled
#print axioms InstanceDemand.NoGo.e1_impossible
#print axioms InstanceDemand.NoGo.no_member_is_endogenous
#print axioms InstanceDemand.NoGo.shape_uncovered_fails_native_join
#print axioms InstanceDemand.NoGo.shape_imposed_fails_E2p
#print axioms InstanceDemand.NoGo.shape_separated_fails_E3
#print axioms InstanceDemand.NoGo.missing_operation_is_extension
#print axioms InstanceDemand.NoGo.class_contains_seed_instruction
#print axioms InstanceDemand.NoGo.covered_seed_instruction
