import RepresentedEmitter

/-!
Scoped negative for the represented two-edge instance channel.

Class `InClass` is stored form-0 ternary instructions. Membership does
not mention E1, owed-separation, or separability. It is nonempty, and
every `Enabled` output names a member as its instruction.

E1 here is *native store*: a sealed step writes a new instance without
being that instance's `admitInst`. That is unsatisfiable on the sealed
grammar (`e1_impossible`), so E1 ∧ E2′ ∧ E3 is unsatisfiable
independently of class membership. The class is the scope of the ledger
row, not a hypothesis of the unsat proof.

The in-class E3 failure is unruled emission of the Enabled output, which
separates its endpoints. The Stage-1 I1 singleton is a different encoding
and is not a member of this class.

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

theorem class_independent_of_coverage :
    InClass (seed 3 0 2 1 false) (0, [0, 1, 2]) ∧
    InClass (seed 3 0 2 1 true) (0, [0, 1, 2]) :=
  ⟨⟨0, 1, 2, rfl, by simp [seed]⟩, ⟨0, 1, 2, rfl, by simp [seed]⟩⟩

theorem class_nonempty : ∃ r c, InClass r c :=
  ⟨seed 3 0 2 1 false, (0, [0, 1, 2]), class_independent_of_coverage.1⟩

/-- Every Enabled output names a stored form-0 ternary as its instruction. -/
theorem class_covers_enabled {r : Regime} {i : Inst}
    (h : Enabled r.insts i) :
    ∃ k l o, InClass r (0, [k, l, o]) ∧ i.1 = 3 + o := by
  rcases h with ⟨k, l, o, _x, _z, _y, hc, _, _, _, hi⟩
  exact ⟨k, l, o, ⟨k, l, o, rfl, hc⟩, congrArg Prod.fst hi⟩

theorem e1_impossible {r s : Regime} {e : Event} {out : Inst}
    (h : E1 r s e out) : False :=
  h.2.2.2 (new_stored_instance_needs_event h.1 h.2.1 h.2.2.1)

theorem shape_imposed_fails_E2p {r : Regime} {i j : Nat} :
    ¬ E2prime r (Event.impose i j) i j := by
  intro h
  exact h.2 i j rfl

/-- After unruled emission of the Enabled output, the endpoints separate. -/
theorem shape_unruled_emission_fails_E3 {n x z y : Nat}
    (hxy : x < y) (hyn : y < n) :
    ¬ E3 (emit (seed n x z y false)) x y :=
  fun h => h (unruled_emission_separates n x z y hxy hyn)

end InstanceDemand.NoGo

#print axioms InstanceDemand.NoGo.class_independent_of_coverage
#print axioms InstanceDemand.NoGo.class_nonempty
#print axioms InstanceDemand.NoGo.class_covers_enabled
#print axioms InstanceDemand.NoGo.e1_impossible
#print axioms InstanceDemand.NoGo.shape_imposed_fails_E2p
#print axioms InstanceDemand.NoGo.shape_unruled_emission_fails_E3
