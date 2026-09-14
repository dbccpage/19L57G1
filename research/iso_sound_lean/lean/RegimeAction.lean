import Permutation

/-!
# RegimeAction: Permutation Group Action on Regimes and Orbit Equivalence

Formalization of R1:
- Group action of S(n) on presentation regimes and arbitrary carrier types
- Lawful group action properties (identity and compatibility)
- Action inversion lemmas: `inv_act_act`, `act_inv_act`, `act_inj`
- Orbit relation `InOrbit r₁ r₂ ↔ ∃ p : Perm n, p • r₁ = r₂`
- Structural isomorphism `Iso r₁ r₂` matching the orbit relation
- Formal proof that `Iso` is an equivalence relation (reflexive, symmetric, transitive)
- Orbit characterization: regimes are isomorphic if and only if their orbits coincide

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero omissions.
AuthorityEffect: None.
-/

namespace IsoSoundLean

open Perm

/-- Typeclass for a left action of `Perm n` on a carrier type `α`. -/
class PermAction (n : Nat) (α : Type) where
  act : Perm n → α → α

infixr:73 " • " => PermAction.act

/-- Lawful permutation action axioms: identity acts trivially and composition is compatible. -/
class LawfulPermAction (n : Nat) (α : Type) [PermAction n α] : Prop where
  id_act : ∀ (x : α), Perm.id n • x = x
  comp_act : ∀ (p q : Perm n) (x : α), (Perm.comp p q) • x = p • (q • x)

variable {n : Nat} {α : Type} [PermAction n α] [LawfulPermAction n α]

/-- Inverting the acting permutation cancels the forward action. -/
@[simp] theorem inv_act_act (p : Perm n) (x : α) : (Perm.inv p) • (p • x) = x := by
  have h := LawfulPermAction.comp_act (Perm.inv p) p x
  rw [← h, Perm.comp_left_inv, LawfulPermAction.id_act]

/-- Forward action cancels the inverse action. -/
@[simp] theorem act_inv_act (p : Perm n) (x : α) : p • ((Perm.inv p) • x) = x := by
  have h := LawfulPermAction.comp_act p (Perm.inv p) x
  rw [← h, Perm.comp_right_inv, LawfulPermAction.id_act]

/-- Action by any permutation is injective on states. -/
theorem act_inj (p : Perm n) (x y : α) : p • x = p • y ↔ x = y := by
  constructor
  · intro h
    have h_cancel : (Perm.inv p) • (p • x) = (Perm.inv p) • (p • y) := by rw [h]
    rw [inv_act_act, inv_act_act] at h_cancel
    exact h_cancel
  · intro h
    rw [h]

/-- Action equality inversion principle. -/
theorem act_eq_iff (p : Perm n) (x y : α) : p • x = y ↔ x = (Perm.inv p) • y := by
  constructor
  · rintro rfl
    rw [inv_act_act]
  · rintro rfl
    rw [act_inv_act]

/-! ## Concrete Presentation Regimes -/

/-- Relational presentation regime on `n` presentation data tokens. -/
structure Regime (n : Nat) where
  tokens : Fin n → Nat
  forms : List Nat
  insts : List (Nat × List (Fin n))
  rules : List Nat
  reqs : List (Fin n × Fin n)

namespace Regime

theorem ext {r s : Regime n}
    (ht : r.tokens = s.tokens)
    (hf : r.forms = s.forms)
    (hi : r.insts = s.insts)
    (hru : r.rules = s.rules)
    (hre : r.reqs = s.reqs) : r = s := by
  cases r
  cases s
  dsimp at ht hf hi hru hre
  subst ht hf hi hru hre
  rfl

/-- Action of S(n) on presentation regimes: data tokens are re-indexed via `invFun`
while instance argument tuples and separation requirements are mapped via `toFun`. -/
def actRegime (p : Perm n) (r : Regime n) : Regime n where
  tokens := r.tokens ∘ p.invFun
  forms := r.forms
  insts := r.insts.map (fun (f, args) => (f, args.map p.toFun))
  rules := r.rules
  reqs := r.reqs.map (fun (i, j) => (p.toFun i, p.toFun j))

instance : PermAction n (Regime n) where
  act := actRegime

@[simp] theorem act_tokens (p : Perm n) (r : Regime n) :
    (p • r).tokens = r.tokens ∘ p.invFun := rfl

@[simp] theorem act_forms (p : Perm n) (r : Regime n) :
    (p • r).forms = r.forms := rfl

@[simp] theorem act_insts (p : Perm n) (r : Regime n) :
    (p • r).insts = r.insts.map (fun (f, args) => (f, args.map p.toFun)) := rfl

@[simp] theorem act_rules (p : Perm n) (r : Regime n) :
    (p • r).rules = r.rules := rfl

@[simp] theorem act_reqs (p : Perm n) (r : Regime n) :
    (p • r).reqs = r.reqs.map (fun (i, j) => (p.toFun i, p.toFun j)) := rfl

theorem id_act_insts (insts : List (Nat × List (Fin n))) :
    insts.map (fun (f, args) => (f, args.map (Perm.id n).toFun)) = insts := by
  induction insts with
  | nil => rfl
  | cons head tail ih =>
    have h_args : head.2.map (Perm.id n).toFun = head.2 := by
      induction head.2 with
      | nil => rfl
      | cons a as ihas =>
        simp only [List.map_cons]
        rw [Perm.toFun_id, ihas]
    simp only [List.map_cons]
    rw [h_args, ih]

theorem id_act_reqs (reqs : List (Fin n × Fin n)) :
    reqs.map (fun (i, j) => ((Perm.id n).toFun i, (Perm.id n).toFun j)) = reqs := by
  induction reqs with
  | nil => rfl
  | cons head tail ih =>
    simp only [List.map_cons]
    rw [Perm.toFun_id, Perm.toFun_id, ih]

theorem comp_act_insts (p q : Perm n) (insts : List (Nat × List (Fin n))) :
    insts.map (fun (f, args) => (f, args.map (Perm.comp p q).toFun)) =
    (insts.map (fun (f, args) => (f, args.map q.toFun))).map (fun (f, args) => (f, args.map p.toFun)) := by
  induction insts with
  | nil => rfl
  | cons head tail ih =>
    have h_args : head.2.map (Perm.comp p q).toFun = (head.2.map q.toFun).map p.toFun := by
      induction head.2 with
      | nil => rfl
      | cons a as ihas =>
        simp only [List.map_cons]
        rw [Perm.toFun_comp, ihas]
    simp only [List.map_cons]
    rw [h_args, ih]

theorem comp_act_reqs (p q : Perm n) (reqs : List (Fin n × Fin n)) :
    reqs.map (fun (i, j) => ((Perm.comp p q).toFun i, (Perm.comp p q).toFun j)) =
    (reqs.map (fun (i, j) => (q.toFun i, q.toFun j))).map (fun (i, j) => (p.toFun i, p.toFun j)) := by
  induction reqs with
  | nil => rfl
  | cons head tail ih =>
    simp only [List.map_cons]
    rw [Perm.toFun_comp, Perm.toFun_comp, ih]

instance : LawfulPermAction n (Regime n) where
  id_act := by
    intro r
    apply ext
    · funext x; rfl
    · rfl
    · exact id_act_insts r.insts
    · rfl
    · exact id_act_reqs r.reqs
  comp_act := by
    intro p q r
    apply ext
    · funext x; rfl
    · rfl
    · exact comp_act_insts p q r.insts
    · rfl
    · exact comp_act_reqs p q r.reqs

end Regime

/-! ## The Orbit Relation and Structural Isomorphism -/

set_option linter.unusedSectionVars false

section OrbitSection

variable (n : Nat) {α : Type} [PermAction n α] [LawfulPermAction n α]

/-- The orbit relation: `r₂` is in the orbit of `r₁` under S(n). -/
def InOrbit (r₁ r₂ : α) : Prop :=
  ∃ p : Perm n, p • r₁ = r₂

/-- Structural isomorphism is defined as membership in the same permutation orbit. -/
def Iso (r₁ r₂ : α) : Prop :=
  InOrbit n r₁ r₂

/-- Isomorphism is reflexive: every regime is isomorphic to itself via `id`. -/
theorem iso_refl (r : α) : Iso n r r :=
  ⟨Perm.id n, LawfulPermAction.id_act r⟩

/-- Isomorphism is symmetric: if `p • r₁ = r₂`, then `p⁻¹ • r₂ = r₁`. -/
theorem iso_symm {r₁ r₂ : α} (h : Iso n r₁ r₂) : Iso n r₂ r₁ := by
  rcases h with ⟨p, hp⟩
  exact ⟨Perm.inv p, by rw [← hp, inv_act_act]⟩

/-- Isomorphism is transitive: if `p • r₁ = r₂` and `q • r₂ = r₃`, then `(q ∘ p) • r₁ = r₃`. -/
theorem iso_trans {r₁ r₂ r₃ : α} (h₁ : Iso n r₁ r₂) (h₂ : Iso n r₂ r₃) : Iso n r₁ r₃ := by
  rcases h₁ with ⟨p, hp⟩
  rcases h₂ with ⟨q, hq⟩
  exact ⟨Perm.comp q p, by rw [LawfulPermAction.comp_act, hp, hq]⟩

/-- The orbit set of a regime `r`. -/
def Orbit (r : α) : α → Prop :=
  fun s => Iso n r s

/-- Membership in the orbit set is equivalent to isomorphism. -/
theorem mem_orbit_iff (r s : α) : Orbit n r s ↔ Iso n r s :=
  Iff.rfl

/-- Regimes are isomorphic if and only if their orbits are identical sets. -/
theorem iso_iff_same_orbit (r₁ r₂ : α) : (Iso n r₁ r₂) ↔ (∀ s, Orbit n r₁ s ↔ Orbit n r₂ s) := by
  constructor
  · intro h s
    constructor
    · intro h1
      exact iso_trans n (iso_symm n h) h1
    · intro h2
      exact iso_trans n h h2
  · intro h
    have h_refl : Orbit n r₂ r₂ := iso_refl n r₂
    exact (h r₂).mpr h_refl

end OrbitSection

end IsoSoundLean
