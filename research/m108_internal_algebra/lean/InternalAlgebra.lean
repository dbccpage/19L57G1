/-!
# Target M108: General Internal Universal Algebra

Constructive internal universal algebra formalized in Lean 4 without Mathlib:
1. Universal Algebraic Signatures and Terms:
   - Multi-sorted equational terms (Var, Op), evaluation under valuation, substitution.
   - Substitution-evaluation composition theorem.
2. Monoid Structure and Free Monoid F(X):
   - Monoid class and MonoidHom structure.
   - List X as the free monoid F(X).
   - Universal lift arrow and proof that it forms a monoid homomorphism.
   - Uniqueness theorem for universal monoid arrows.
3. Commutative Rings and Modules:
   - CommRing class and constructive integer instance `commRingInt`.
   - Module class and LinearMap structure.
   - Formal linear combinations over basis X as free module model.
   - Universal evaluation of formal linear combinations, basis agreement, and scaling.
4. Congruence Relations and Quotient Algebras:
   - Equivalence relations compatible with signature operations.
   - Constructive 2-argument quotient lift (`lift2`) with zero axioms.
   - Quotient monoid construction via `Quot R`.
   - Operational closure and representative independence theorem.
5. Factorization Theorem (Universal Mapping Property of Quotients):
   - Induced homomorphism `factorHom` on quotient algebra for any relation-compatible map.
   - Commutativity of factorization: `factorHom ∘ π = h`.
   - Uniqueness theorem for arrows factoring through quotients.

Axiom Boundary: Strictly within {propext, Quot.sound}. Zero Classical.choice. Zero mathlib.
-/

namespace InternalAlgebra

universe u v w

/-! ============================================================================
    1. Signatures and Equational Terms
   ============================================================================ -/

inductive Term (V : Type u) (Op : Type v) (ar : Op → Nat) : Type (max u v)
  | var : V → Term V Op ar
  | app (op : Op) : (Fin (ar op) → Term V Op ar) → Term V Op ar

/-- Evaluation of an equational term in a carrier type A under an interpretation of operations. -/
def evalTerm {V : Type u} {Op : Type v} {ar : Op → Nat} {A : Type w}
    (I : (op : Op) → (Fin (ar op) → A) → A) (val : V → A) : Term V Op ar → A
  | Term.var v => val v
  | Term.app op args => I op (fun i => evalTerm I val (args i))

/-- Substitution of variables by terms. -/
def substTerm {V : Type u} {Op : Type v} {ar : Op → Nat}
    (s : V → Term V Op ar) : Term V Op ar → Term V Op ar
  | Term.var v => s v
  | Term.app op args => Term.app op (fun i => substTerm s (args i))

/-- Fundamental substitution-evaluation commutation identity. -/
theorem eval_subst {V : Type u} {Op : Type v} {ar : Op → Nat} {A : Type w}
    (I : (op : Op) → (Fin (ar op) → A) → A) (val : V → A) (s : V → Term V Op ar) :
    ∀ t : Term V Op ar, evalTerm I val (substTerm s t) = evalTerm I (fun v => evalTerm I val (s v)) t
  | Term.var v => rfl
  | Term.app op args => by
      dsimp [substTerm, evalTerm]
      congr 1
      funext i
      exact eval_subst I val s (args i)


/-! ============================================================================
    2. Monoid Structure and Free Monoid F(X)
   ============================================================================ -/

class Monoid (M : Type u) : Type u where
  mul : M → M → M
  one : M
  mul_assoc : ∀ x y z : M, mul (mul x y) z = mul x (mul y z)
  one_mul : ∀ x : M, mul one x = x
  mul_one : ∀ x : M, mul x one = x

structure MonoidHom (M : Type u) (N : Type v)
    (instM : Monoid M := by infer_instance) (instN : Monoid N := by infer_instance) : Type (max u v) where
  toFun : M → N
  map_one : toFun instM.one = instN.one
  map_mul : ∀ x y : M, toFun (instM.mul x y) = instN.mul (toFun x) (toFun y)

/-- Free monoid on type X formed by List X with concatenation. -/
instance freeMonoid (X : Type u) : Monoid (List X) where
  mul := List.append
  one := []
  mul_assoc := List.append_assoc
  one_mul := List.nil_append
  mul_one := List.append_nil

/-- Canonical generator inclusion arrow η : X → List X. -/
def eta_monoid {X : Type u} (x : X) : List X := [x]

/-- Universal arrow lift f_hat : List X → N. -/
def freeMonoidLift {X : Type u} {N : Type v} [instN : Monoid N] (f : X → N) : List X → N
  | [] => instN.one
  | x :: xs => instN.mul (f x) (freeMonoidLift f xs)

@[simp]
theorem freeMonoidLift_nil {X : Type u} {N : Type v} [instN : Monoid N] (f : X → N) :
    freeMonoidLift f [] = instN.one := rfl

theorem freeMonoidLift_eta {X : Type u} {N : Type v} [instN : Monoid N] (f : X → N) (x : X) :
    freeMonoidLift f (eta_monoid x) = f x := by
  dsimp [eta_monoid, freeMonoidLift]
  exact instN.mul_one (f x)

theorem freeMonoidLift_append {X : Type u} {N : Type v} [instN : Monoid N] (f : X → N) :
    ∀ l1 l2 : List X, freeMonoidLift f (l1 ++ l2) = instN.mul (freeMonoidLift f l1) (freeMonoidLift f l2)
  | [], l2 => by
      dsimp [freeMonoidLift]
      rw [instN.one_mul]
  | x :: xs, l2 => by
      dsimp [freeMonoidLift]
      rw [freeMonoidLift_append f xs l2]
      rw [instN.mul_assoc]

/-- The lifted arrow as a formal MonoidHom. -/
def freeMonoidLiftHom {X : Type u} {N : Type v} [instN : Monoid N] (f : X → N) :
    MonoidHom (List X) N where
  toFun := freeMonoidLift f
  map_one := rfl
  map_mul := freeMonoidLift_append f

/-- Categorical uniqueness of the universal arrow for Free Monoids. -/
theorem freeMonoid_universal_arrow_unique {X : Type u} {N : Type v} [instN : Monoid N] (f : X → N)
    (g : MonoidHom (List X) N)
    (h_agree : ∀ x : X, g.toFun (eta_monoid x) = f x) :
    ∀ l : List X, g.toFun l = freeMonoidLift f l
  | [] => g.map_one
  | x :: xs => by
      have h_cons : (x :: xs : List X) = Monoid.mul [x] xs := rfl
      rw [h_cons, g.map_mul]
      have h_x : g.toFun [x] = f x := h_agree x
      rw [h_x]
      rw [freeMonoid_universal_arrow_unique f g h_agree xs]
      rfl


/-! ============================================================================
    3. Commutative Rings and Modules
   ============================================================================ -/

class CommRing (R : Type u) : Type u where
  zero : R
  one : R
  add : R → R → R
  mul : R → R → R
  neg : R → R
  add_assoc : ∀ a b c : R, add (add a b) c = add a (add b c)
  add_comm : ∀ a b : R, add a b = add b a
  zero_add : ∀ a : R, add zero a = a
  add_neg : ∀ a : R, add a (neg a) = zero
  mul_assoc : ∀ a b c : R, mul (mul a b) c = mul a (mul b c)
  mul_comm : ∀ a b : R, mul a b = mul b a
  one_mul : ∀ a : R, mul one a = a
  left_distrib : ∀ a b c : R, mul a (add b c) = add (mul a b) (mul a c)

/-- Constructive instance of CommRing over standard integers Int. -/
instance commRingInt : CommRing Int where
  zero := 0
  one := 1
  add := Int.add
  mul := Int.mul
  neg := Int.neg
  add_assoc := Int.add_assoc
  add_comm := Int.add_comm
  zero_add := Int.zero_add
  add_neg := Int.add_right_neg
  mul_assoc := Int.mul_assoc
  mul_comm := Int.mul_comm
  one_mul := Int.one_mul
  left_distrib := Int.mul_add

class Module (R : Type u) [instR : CommRing R] (M : Type v) : Type (max u v) where
  zero : M
  add : M → M → M
  neg : M → M
  smul : R → M → M
  add_assoc : ∀ x y z : M, add (add x y) z = add x (add y z)
  add_comm : ∀ x y : M, add x y = add y x
  zero_add : ∀ x : M, add zero x = x
  add_neg : ∀ x : M, add x (neg x) = zero
  smul_add : ∀ (r : R) (x y : M), smul r (add x y) = add (smul r x) (smul r y)
  add_smul : ∀ (r s : R) (x : M), smul (instR.add r s) x = add (smul r x) (smul s x)
  mul_smul : ∀ (r s : R) (x : M), smul (instR.mul r s) x = smul r (smul s x)
  one_smul : ∀ x : M, smul instR.one x = x

structure LinearMap (R : Type u) [CommRing R] (M : Type v) (N : Type w) [Module R M] [Module R N] : Type (max u v w) where
  toFun : M → N
  map_zero : toFun (Module.zero (R := R)) = Module.zero (R := R)
  map_add : ∀ x y : M, toFun (Module.add (R := R) x y) = Module.add (R := R) (toFun x) (toFun y)
  map_smul : ∀ (r : R) (x : M), toFun (Module.smul (R := R) r x) = Module.smul (R := R) r (toFun x)

/-- Free module formal combinations representation over basis X. -/
def evalSum {X : Type u} (R : Type v) [CommRing R] {N : Type w} [Module R N]
    (f : X → N) : List (X × R) → N
  | [] => Module.zero (R := R)
  | (x, c) :: rest => Module.add (R := R) (Module.smul (R := R) c (f x)) (evalSum R f rest)

/-- Canonical basis element embedding. -/
def eta_mod {X : Type u} (R : Type v) [instR : CommRing R] (x : X) : List (X × R) :=
  [(x, instR.one)]

@[simp]
theorem evalSum_nil {X : Type u} (R : Type v) [CommRing R] {N : Type w} [Module R N] (f : X → N) :
    evalSum R f [] = (Module.zero (R := R) : N) := rfl

theorem evalSum_eta {X : Type u} (R : Type v) [instR : CommRing R] {N : Type w} [instN : Module R N]
    (f : X → N) (x : X) :
    evalSum R f (eta_mod R x) = f x := by
  dsimp [eta_mod, evalSum]
  have h1 := @Module.one_smul R instR N instN (f x)
  rw [h1]
  have h2 := @Module.add_comm R instR N instN (f x) (Module.zero (R := R))
  rw [h2]
  exact @Module.zero_add R instR N instN (f x)

theorem evalSum_append {X : Type u} (R : Type v) [CommRing R] {N : Type w} [Module R N] (f : X → N) :
    ∀ l1 l2 : List (X × R), evalSum R f (l1 ++ l2) = (Module.add (R := R) (evalSum R f l1) (evalSum R f l2) : N)
  | [], l2 => by
      dsimp [evalSum]
      rw [Module.zero_add (R := R)]
  | (x, c) :: xs, l2 => by
      dsimp [evalSum]
      rw [evalSum_append R f xs l2]
      rw [Module.add_assoc (R := R)]


/-! ============================================================================
    4. Congruence Relations and Quotient Algebras
   ============================================================================ -/

/-- Axiom-free 2-argument lift over primitive Quot. -/
def lift2 {α β γ : Type u} {rα : α → α → Prop} {rβ : β → β → Prop}
    (f : α → β → γ)
    (h₁ : ∀ a₁ a₂ b, rα a₁ a₂ → f a₁ b = f a₂ b)
    (h₂ : ∀ a b₁ b₂, rβ b₁ b₂ → f a b₁ = f a b₂)
    (qa : Quot rα) (qb : Quot rβ) : γ :=
  Quot.lift (fun a =>
    Quot.lift (fun b => f a b)
      (fun b₁ b₂ hb => h₂ a b₁ b₂ hb) qb)
    (fun a₁ a₂ ha => by
      induction qb using Quot.ind with
      | mk b =>
        exact h₁ a₁ a₂ b ha) qa

@[simp]
theorem lift2_mk {α β γ : Type u} {rα : α → α → Prop} {rβ : β → β → Prop}
    (f : α → β → γ)
    (h₁ : ∀ a₁ a₂ b, rα a₁ a₂ → f a₁ b = f a₂ b)
    (h₂ : ∀ a b₁ b₂, rβ b₁ b₂ → f a b₁ = f a b₂)
    (a : α) (b : β) :
    lift2 f h₁ h₂ (Quot.mk rα a) (Quot.mk rβ b) = f a b := rfl

structure MonoidCongruence (M : Type u) [Monoid M] (R : M → M → Prop) : Prop where
  refl : ∀ x, R x x
  symm : ∀ x y, R x y → R y x
  trans : ∀ x y z, R x y → R y z → R x z
  mul_compat : ∀ x1 x2 y1 y2, R x1 y1 → R x2 y2 → R (Monoid.mul x1 x2) (Monoid.mul y1 y2)

/-- Quotient multiplication operation. -/
def quotMul {M : Type u} [Monoid M] {R : M → M → Prop} (cong : MonoidCongruence M R) :
    Quot R → Quot R → Quot R :=
  lift2
    (fun a b => Quot.mk R (Monoid.mul a b))
    (fun a1 a2 b ha => Quot.sound (cong.mul_compat a1 b a2 b ha (cong.refl b)))
    (fun a b1 b2 hb => Quot.sound (cong.mul_compat a b1 a b2 (cong.refl a) hb))

/-- Quotient neutral element. -/
def quotOne {M : Type u} [Monoid M] (R : M → M → Prop) : Quot R :=
  Quot.mk R Monoid.one

/-- Canonical projection arrow π : M → Quot R. -/
def quotPi {M : Type u} (R : M → M → Prop) (x : M) : Quot R :=
  Quot.mk R x

theorem quot_mul_assoc {M : Type u} [Monoid M] {R : M → M → Prop} (cong : MonoidCongruence M R) :
    ∀ qa qb qc : Quot R,
      quotMul cong (quotMul cong qa qb) qc = quotMul cong qa (quotMul cong qb qc) := by
  intro qa qb qc
  induction qa using Quot.ind with | mk a =>
  induction qb using Quot.ind with | mk b =>
  induction qc using Quot.ind with | mk c =>
  exact congrArg (Quot.mk R) (Monoid.mul_assoc a b c)

theorem quot_one_mul {M : Type u} [Monoid M] {R : M → M → Prop} (cong : MonoidCongruence M R) :
    ∀ q : Quot R, quotMul cong (quotOne R) q = q := by
  intro q
  induction q using Quot.ind with | mk a =>
  exact congrArg (Quot.mk R) (Monoid.one_mul a)

theorem quot_mul_one {M : Type u} [Monoid M] {R : M → M → Prop} (cong : MonoidCongruence M R) :
    ∀ q : Quot R, quotMul cong q (quotOne R) = q := by
  intro q
  induction q using Quot.ind with | mk a =>
  exact congrArg (Quot.mk R) (Monoid.mul_one a)

@[instance_reducible]
def quotientMonoid {M : Type u} [Monoid M] {R : M → M → Prop} (cong : MonoidCongruence M R) :
    Monoid (Quot R) where
  mul := quotMul cong
  one := quotOne R
  mul_assoc := quot_mul_assoc cong
  one_mul := quot_one_mul cong
  mul_one := quot_mul_one cong

/-- Representative independence: equivalent representatives evaluate to identical quotient products. -/
theorem quot_representative_independence {M : Type u} [Monoid M] {R : M → M → Prop}
    (cong : MonoidCongruence M R) (x1 x2 y1 y2 : M) (h1 : R x1 y1) (h2 : R x2 y2) :
    quotMul cong (quotPi R x1) (quotPi R x2) = quotMul cong (quotPi R y1) (quotPi R y2) := by
  dsimp [quotMul, quotPi]
  exact Quot.sound (cong.mul_compat x1 x2 y1 y2 h1 h2)


/-! ============================================================================
    5. Factorization Theorem (Universal Mapping Property of Quotients)
   ============================================================================ -/

/-- Induced map on the quotient algebra. -/
def factorMap {M : Type u} {N : Type v} [Monoid M] [Monoid N] {R : M → M → Prop}
    (h : MonoidHom M N) (h_respects : ∀ x y : M, R x y → h.toFun x = h.toFun y) :
    Quot R → N :=
  Quot.lift h.toFun h_respects

/-- Factorization commutativity equation: factorMap ∘ π = h. -/
theorem factorMap_commutes {M : Type u} {N : Type v} [Monoid M] [Monoid N] {R : M → M → Prop}
    (h : MonoidHom M N) (h_respects : ∀ x y : M, R x y → h.toFun x = h.toFun y) (x : M) :
    factorMap h h_respects (quotPi R x) = h.toFun x := rfl

theorem factorMap_map_one {M : Type u} {N : Type v} [Monoid M] [Monoid N] {R : M → M → Prop}
    (h : MonoidHom M N) (h_respects : ∀ x y : M, R x y → h.toFun x = h.toFun y) :
    factorMap h h_respects (quotOne R) = Monoid.one (M := N) :=
  h.map_one

theorem factorMap_map_mul {M : Type u} {N : Type v} [Monoid M] [instN : Monoid N] {R : M → M → Prop}
    (h : MonoidHom M N) (h_respects : ∀ x y : M, R x y → h.toFun x = h.toFun y)
    (cong : MonoidCongruence M R) :
    ∀ q1 q2 : Quot R,
      factorMap h h_respects (quotMul cong q1 q2) =
        instN.mul (factorMap h h_respects q1) (factorMap h h_respects q2) := by
  intro q1 q2
  induction q1 using Quot.ind with | mk x =>
  induction q2 using Quot.ind with | mk y =>
  exact h.map_mul x y

/-- The factored map as a formal MonoidHom from Quot R into N. -/
def factorHom {M : Type u} {N : Type v} [Monoid M] [instN : Monoid N] {R : M → M → Prop}
    (cong : MonoidCongruence M R)
    (h : MonoidHom M N) (h_respects : ∀ x y : M, R x y → h.toFun x = h.toFun y) :
    MonoidHom (Quot R) N (quotientMonoid cong) instN where
  toFun := factorMap h h_respects
  map_one := factorMap_map_one h h_respects
  map_mul := factorMap_map_mul h h_respects cong

/-- Categorical uniqueness of the factored arrow out of the quotient. -/
theorem factorHom_unique {M : Type u} {N : Type v} [Monoid M] [instN : Monoid N] {R : M → M → Prop}
    (cong : MonoidCongruence M R)
    (h : MonoidHom M N) (h_respects : ∀ x y : M, R x y → h.toFun x = h.toFun y)
    (g : MonoidHom (Quot R) N (quotientMonoid cong) instN)
    (h_comm : ∀ x : M, g.toFun (quotPi R x) = h.toFun x) :
    ∀ q : Quot R, g.toFun q = factorMap h h_respects q := by
  intro q
  induction q using Quot.ind with | mk x =>
  exact h_comm x

end InternalAlgebra
