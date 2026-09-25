import SecondSymmetry.Kernel
import SecondSymmetry.IsoKernel

/-!
# Automorphisms, survival across an event, images and fixing

Native to rung five.  An AUTOMORPHISM of a regime `r` is a sealed
`Iso r r`.  The sealed structure bundles four maps with the proofs that
they carry the regime onto itself; two isomorphisms with the same four
maps are the same pair of bijections, whatever proofs they carry.  So an
automorphism of `r` SURVIVES into `r'` when some automorphism of `r'`
carries the same four maps.

The five regimes after an admitting event are named here once, and each
is tied to the reconstructed sealed step by a theorem at the level of a
definition.  The IMAGE of an instance or a requirement under an
isomorphism is what its maps carry it to; a requirement's image is
re-ordered by the sealed `sortPair`, as the sealed structure's own
requirement fields are.

AuthorityEffect: None.
-/

namespace SecondSymmetry
namespace Aut

open Sealed

/-- Two isomorphisms carry the same four maps. -/
def SameMaps {r s r' s' : Regime} (σ : Iso r s) (τ : Iso r' s') : Prop :=
  σ.dmap = τ.dmap ∧ σ.dinv = τ.dinv ∧ σ.fmap = τ.fmap ∧ σ.finv = τ.finv

/-- An automorphism of `r` survives into `r'` when its maps are those of
an automorphism of `r'`. -/
def Survives {r : Regime} (σ : Iso r r) (r' : Regime) : Prop :=
  ∃ τ : Iso r' r', SameMaps σ τ

/-- The image of an instance: form index by `fmap`, arguments by `dmap`. -/
def instImage {r s : Regime} (σ : Iso r s) (e : Inst) : Inst :=
  (σ.fmap e.1, e.2.map σ.dmap)

/-- The image of a requirement, re-ordered as the sealed fields order it. -/
def reqImage {r s : Regime} (σ : Iso r s) (q : Nat × Nat) : Nat × Nat :=
  sortPair (σ.dmap q.1, σ.dmap q.2)

/-- The regime after admitting an instance. -/
def addInst (r : Regime) (e : Inst) : Regime :=
  { r with insts := insertNew r.insts e }

/-- The regime after admitting a uniform rule. -/
def addRule (r : Regime) (f : Nat) : Regime :=
  { r with rules := insertNew r.rules f }

/-- The regime after imposing a requirement. -/
def addReq (r : Regime) (q : Nat × Nat) : Regime :=
  { r with reqs := insertNew r.reqs q }

/-- The regime after admitting a datum. -/
def addDatum (r : Regime) : Regime :=
  { r with data := r.data + 1 }

/-- The regime after admitting a form. -/
def addForm (r : Regime) (a : Nat) : Regime :=
  { r with forms := r.forms ++ [a] }

/-- The element count of a regime: its data, its forms, and its
instances, rules and requirements, each counted as listed. -/
def size (r : Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

theorem sameMaps_symm {r s r' s' : Regime} {σ : Iso r s} {τ : Iso r' s'}
    (h : SameMaps σ τ) : SameMaps τ σ :=
  ⟨h.1.symm, h.2.1.symm, h.2.2.1.symm, h.2.2.2.symm⟩

/-- A supply leaves the regime, and so every automorphism, in place. -/
theorem supply_keeps (r : Regime) (t : Nat) (σ : Iso r r) :
    stepE r (.supply t) = some r ∧ Survives σ r :=
  ⟨rfl, σ, rfl, rfl, rfl, rfl⟩

theorem stepE_inst (r : Regime) (f : Nat) (args : List Nat)
    (h : f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
      (∀ x ∈ args, x < r.data)) :
    stepE r (.admitInst f args) = some (addInst r (f, args)) := by
  dsimp only [stepE]
  rw [if_pos h]
  rfl

theorem stepE_rule (r : Regime) (f : Nat) (h : f < r.forms.length) :
    stepE r (.admitRuleAll f) = some (addRule r f) := by
  dsimp only [stepE]
  rw [if_pos h]
  rfl

theorem stepE_req (r : Regime) (i j : Nat) (h : i < j ∧ j < r.data) :
    stepE r (.impose i j) = some (addReq r (i, j)) := by
  dsimp only [stepE]
  rw [if_pos h]
  rfl

theorem stepE_datum (r : Regime) :
    stepE r .admitDatum = some (addDatum r) := rfl

theorem stepE_form (r : Regime) (a : Nat) (h : 1 ≤ a) :
    stepE r (.admitForm a) = some (addForm r a) := by
  dsimp only [stepE]
  rw [if_pos h]
  rfl

end Aut
end SecondSymmetry
