/-!
# Permutation: Finite Permutation Groups S(n)

Formalization of the symmetric group S(n) on Fin n:
- Permutation structure with explicit two-sided inverses
- Extensionality theorem (ext)
- Group operations: identity (id), composition (comp), inverse (inv)
- Group laws: associativity, identity laws, and inverse cancellation laws

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero omissions.
AuthorityEffect: None.
-/

namespace IsoSoundLean

/-- Permutation on Fin n with verified two-sided inverse. -/
structure Perm (n : Nat) where
  toFun : Fin n → Fin n
  invFun : Fin n → Fin n
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

namespace Perm

variable {n : Nat}

/-- Identity permutation in S(n). -/
def id (n : Nat) : Perm n where
  toFun := fun x => x
  invFun := fun x => x
  left_inv := fun _ => rfl
  right_inv := fun _ => rfl

/-- Composition of permutations: (p ∘ q)(x) = p(q(x)). -/
def comp (p q : Perm n) : Perm n where
  toFun := p.toFun ∘ q.toFun
  invFun := q.invFun ∘ p.invFun
  left_inv := by
    intro x
    show q.invFun (p.invFun (p.toFun (q.toFun x))) = x
    rw [p.left_inv (q.toFun x)]
    exact q.left_inv x
  right_inv := by
    intro y
    show p.toFun (q.toFun (q.invFun (p.invFun y))) = y
    rw [q.right_inv (p.invFun y)]
    exact p.right_inv y

/-- Inverse permutation in S(n). -/
def inv (p : Perm n) : Perm n where
  toFun := p.invFun
  invFun := p.toFun
  left_inv := p.right_inv
  right_inv := p.left_inv

/-- Extensionality principle for permutations: equality of forward maps implies equality of permutations. -/
theorem ext {p q : Perm n} (h : ∀ x, p.toFun x = q.toFun x) : p = q := by
  have h_to : p.toFun = q.toFun := funext h
  have h_inv : p.invFun = q.invFun := by
    funext y
    have h1 : p.invFun y = q.invFun (q.toFun (p.invFun y)) := (q.left_inv (p.invFun y)).symm
    have h2 : q.toFun (p.invFun y) = p.toFun (p.invFun y) := (h (p.invFun y)).symm
    rw [h2, p.right_inv y] at h1
    exact h1
  cases p
  cases q
  dsimp at h_to h_inv
  subst h_to h_inv
  rfl

@[simp] theorem toFun_id (x : Fin n) : (id n).toFun x = x := rfl
@[simp] theorem invFun_id (x : Fin n) : (id n).invFun x = x := rfl

@[simp] theorem toFun_comp (p q : Perm n) (x : Fin n) :
    (comp p q).toFun x = p.toFun (q.toFun x) := rfl

@[simp] theorem invFun_comp (p q : Perm n) (x : Fin n) :
    (comp p q).invFun x = q.invFun (p.invFun x) := rfl

@[simp] theorem toFun_inv (p : Perm n) (x : Fin n) :
    (inv p).toFun x = p.invFun x := rfl

@[simp] theorem invFun_inv (p : Perm n) (x : Fin n) :
    (inv p).invFun x = p.toFun x := rfl

/-- Left identity law. -/
@[simp] theorem id_comp (p : Perm n) : comp (id n) p = p := by
  apply ext
  intro x
  rfl

/-- Right identity law. -/
@[simp] theorem comp_id (p : Perm n) : comp p (id n) = p := by
  apply ext
  intro x
  rfl

/-- Associativity of composition. -/
theorem comp_assoc (p q r : Perm n) : comp (comp p q) r = comp p (comp q r) := by
  apply ext
  intro x
  rfl

/-- Left inverse cancellation law. -/
@[simp] theorem comp_left_inv (p : Perm n) : comp (inv p) p = id n := by
  apply ext
  intro x
  exact p.left_inv x

/-- Right inverse cancellation law. -/
@[simp] theorem comp_right_inv (p : Perm n) : comp p (inv p) = id n := by
  apply ext
  intro x
  exact p.right_inv x

/-- Inverse of identity is identity. -/
@[simp] theorem inv_id : inv (id n) = id n := by
  apply ext
  intro x
  rfl

/-- Inverse is an involution. -/
@[simp] theorem inv_inv (p : Perm n) : inv (inv p) = p := by
  apply ext
  intro x
  rfl

/-- Contravariant law for inverse of composition. -/
theorem inv_comp (p q : Perm n) : inv (comp p q) = comp (inv q) (inv p) := by
  apply ext
  intro x
  rfl

end Perm

end IsoSoundLean
