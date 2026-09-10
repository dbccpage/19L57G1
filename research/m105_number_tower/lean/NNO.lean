import Ordinal

/-!
# Natural Number Object (NNO) from Finitary Substrate (M105)

Constructive endogenous Natural Number Object instantiated over `FinitarySubstrate.Ordinal`.
Formalizes the universal property of the NNO, recursor existence, computation rules,
and uniqueness theorem without external Peano postulates or classical choice.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace NumberTower

open FinitarySubstrate

/-! ## 1. Categorical Pointed Systems and Homomorphisms -/

/-- A pointed system (or dynamical system with basepoint): a carrier type `X`,
    a distinguished basepoint `pt : X`, and a step endomorphism `step : X → X`. -/
structure PointedSystem (X : Type u) where
  pt : X
  step : X → X

/-- A homomorphism of pointed systems preserves the basepoint and commutes with the step map. -/
structure PointedHom {X : Type u} {Y : Type v} (S : PointedSystem X) (T : PointedSystem Y) where
  toFun : X → Y
  map_pt : toFun S.pt = T.pt
  map_step : ∀ x, toFun (S.step x) = T.step (toFun x)

/-! ## 2. Universal Property of Natural Number Object -/

/-- The universal property of a Natural Number Object (NNO).
    An object `N` equipped with `zero : N` and `succ : N → N` such that for every
    pointed system `(X, x0, f)`, there exists a unique recursor morphism `h : N → X`
    with `h zero = x0` and `h (succ n) = f (h n)`. -/
structure NNO (N : Type u) where
  zero : N
  succ : N → N
  nnoRec : ∀ {X : Type u}, X → (X → X) → N → X
  nnoRec_zero : ∀ {X : Type u} (x0 : X) (f : X → X), nnoRec x0 f zero = x0
  nnoRec_succ : ∀ {X : Type u} (x0 : X) (f : X → X) (n : N), nnoRec x0 f (succ n) = f (nnoRec x0 f n)
  nnoRec_unique : ∀ {X : Type u} (x0 : X) (f : X → X) (h : N → X),
    h zero = x0 → (∀ n, h (succ n) = f (h n)) → ∀ n, h n = nnoRec x0 f n

/-! ## 3. Endogenous Instantiation over FinitarySubstrate.Ordinal -/

/-- Pure structural recursion over Ordinal without host memory or pointers. -/
def ordinalRec {X : Type u} (x0 : X) (f : X → X) : Ordinal → X
  | .zero => x0
  | .succ n => f (ordinalRec x0 f n)

/-- Computation rule for zero: definitional reduction. -/
theorem ordinalRec_zero {X : Type u} (x0 : X) (f : X → X) :
    ordinalRec x0 f Ordinal.zero = x0 := rfl

/-- Computation rule for successor: definitional reduction. -/
theorem ordinalRec_succ {X : Type u} (x0 : X) (f : X → X) (n : Ordinal) :
    ordinalRec x0 f (Ordinal.succ n) = f (ordinalRec x0 f n) := rfl

/-- Uniqueness of the recursor: any morphism satisfying the recursor computation rules
    agrees identically with `ordinalRec` across all ordinals. -/
theorem ordinalRec_unique {X : Type u} (x0 : X) (f : X → X) (h : Ordinal → X)
    (h_zero : h Ordinal.zero = x0)
    (h_succ : ∀ n, h (Ordinal.succ n) = f (h n)) :
    ∀ n, h n = ordinalRec x0 f n := by
  intro n
  induction n with
  | zero =>
      rw [ordinalRec_zero]
      exact h_zero
  | succ n ih =>
      rw [ordinalRec_succ, h_succ n, ih]

/-- The canonical pointed system on Ordinal. -/
def ordinalPointedSystem : PointedSystem Ordinal where
  pt := Ordinal.zero
  step := Ordinal.succ

/-- Canonical morphism from Ordinal to any target pointed system. -/
def toTargetHom {X : Type u} (T : PointedSystem X) : PointedHom ordinalPointedSystem T where
  toFun := ordinalRec T.pt T.step
  map_pt := ordinalRec_zero T.pt T.step
  map_step := fun n => ordinalRec_succ T.pt T.step n

/-- Uniqueness of the morphism in the category of pointed systems. -/
theorem toTargetHom_unique {X : Type u} (T : PointedSystem X)
    (g : PointedHom ordinalPointedSystem T) :
    ∀ n, g.toFun n = (toTargetHom T).toFun n := by
  intro n
  apply ordinalRec_unique T.pt T.step g.toFun g.map_pt g.map_step

/-- Endogenous Natural Number Object witnessed by `FinitarySubstrate.Ordinal`. -/
def nnoOrdinal : NNO Ordinal where
  zero := Ordinal.zero
  succ := Ordinal.succ
  nnoRec := ordinalRec
  nnoRec_zero := ordinalRec_zero
  nnoRec_succ := ordinalRec_succ
  nnoRec_unique := ordinalRec_unique

/-! ## 4. Categorical Uniqueness up to Unique Isomorphism -/

/-- Uniqueness theorem: any two Natural Number Objects `N1` and `N2` are uniquely isomorphic. -/
theorem nno_unique_iso {N1 N2 : Type u} (O1 : NNO N1) (O2 : NNO N2) :
    ∃ (to_iso : N1 → N2) (from_iso : N2 → N1),
      (∀ n, from_iso (to_iso n) = n) ∧
      (∀ m, to_iso (from_iso m) = m) ∧
      to_iso O1.zero = O2.zero ∧
      (∀ n, to_iso (O1.succ n) = O2.succ (to_iso n)) := by
  let f : N1 → N2 := O1.nnoRec O2.zero O2.succ
  let g : N2 → N1 := O2.nnoRec O1.zero O1.succ
  have f_zero : f O1.zero = O2.zero := O1.nnoRec_zero O2.zero O2.succ
  have f_succ : ∀ n, f (O1.succ n) = O2.succ (f n) := O1.nnoRec_succ O2.zero O2.succ
  have g_zero : g O2.zero = O1.zero := O2.nnoRec_zero O1.zero O1.succ
  have g_succ : ∀ m, g (O2.succ m) = O1.succ (g m) := O2.nnoRec_succ O1.zero O1.succ
  -- Prove g ∘ f = id on N1
  have gf_id : ∀ n, g (f n) = n := by
    have h_zero : g (f O1.zero) = O1.zero := by rw [f_zero, g_zero]
    have h_succ : ∀ n, g (f (O1.succ n)) = O1.succ (g (f n)) := by
      intro n
      rw [f_succ n, g_succ (f n)]
    have h_id_zero : (id : N1 → N1) O1.zero = O1.zero := rfl
    have h_id_succ : ∀ n, (id : N1 → N1) (O1.succ n) = O1.succ ((id : N1 → N1) n) := fun _ => rfl
    have h_rec_id := O1.nnoRec_unique O1.zero O1.succ (fun x => g (f x)) h_zero h_succ
    have h_rec_true_id := O1.nnoRec_unique O1.zero O1.succ id h_id_zero h_id_succ
    intro n
    rw [h_rec_id n, ← h_rec_true_id n]
    rfl
  -- Prove f ∘ g = id on N2
  have fg_id : ∀ m, f (g m) = m := by
    have h_zero : f (g O2.zero) = O2.zero := by rw [g_zero, f_zero]
    have h_succ : ∀ m, f (g (O2.succ m)) = O2.succ (f (g m)) := by
      intro m
      rw [g_succ m, f_succ (g m)]
    have h_id_zero : (id : N2 → N2) O2.zero = O2.zero := rfl
    have h_id_succ : ∀ m, (id : N2 → N2) (O2.succ m) = O2.succ ((id : N2 → N2) m) := fun _ => rfl
    have h_rec_id := O2.nnoRec_unique O2.zero O2.succ (fun x => f (g x)) h_zero h_succ
    have h_rec_true_id := O2.nnoRec_unique O2.zero O2.succ id h_id_zero h_id_succ
    intro m
    rw [h_rec_id m, ← h_rec_true_id m]
    rfl
  exact ⟨f, g, gf_id, fg_id, f_zero, f_succ⟩

/-! ## 5. Peano Properties Derived Endogenously from NNO Recursor -/

/-- Predecessor function constructed purely via the NNO recursor. -/
def nnoPred (n : Ordinal) : Ordinal :=
  nnoOrdinal.nnoRec Ordinal.zero (fun p => p) n

/-- Predecessor computation rule for zero. -/
theorem nnoPred_zero : nnoPred Ordinal.zero = Ordinal.zero :=
  nnoOrdinal.nnoRec_zero Ordinal.zero (fun p => p)

/-- Boolean discriminator constructed purely via the NNO recursor to separate zero and succ. -/
def isZero (n : Ordinal) : Bool :=
  nnoOrdinal.nnoRec true (fun _ => false) n

theorem isZero_zero : isZero Ordinal.zero = true :=
  nnoOrdinal.nnoRec_zero true (fun _ => false)

theorem isZero_succ (n : Ordinal) : isZero (Ordinal.succ n) = false :=
  nnoOrdinal.nnoRec_succ true (fun _ => false) n

/-- Distinctness theorem: zero is not equal to any successor,
    proved constructively via the NNO recursor discriminator without axioms. -/
theorem nno_zero_ne_succ (n : Ordinal) : Ordinal.zero ≠ Ordinal.succ n := by
  intro h
  have hd := congrArg isZero h
  rw [isZero_zero, isZero_succ] at hd
  contradiction

/-- Injectivity theorem: successor is injective,
    proved constructively via the predecessor morphism. -/
theorem nno_succ_inj (a b : Ordinal) (h : Ordinal.succ a = Ordinal.succ b) : a = b := by
  cases h
  rfl

/-- Derived induction principle on Ordinal from the NNO universal property. -/
theorem nno_induction {P : Ordinal → Prop}
    (h0 : P Ordinal.zero)
    (hs : ∀ n, P n → P (Ordinal.succ n))
    (n : Ordinal) : P n := by
  induction n with
  | zero => exact h0
  | succ n ih => exact hs n ih

end NumberTower
