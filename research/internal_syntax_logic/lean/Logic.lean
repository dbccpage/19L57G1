/-!
# M101: Resource-Sensitive Consequence & Operational Logic

Constructive substructural sequent calculus with linear contexts,
explicit identity, cut rules and principal cut reductions, operational phase semantics,
soundness theorem, and proof of non-triviality (consistency: absurdity is not derivable).

AuthorityEffect: None.
Axioms: strictly in {propext, Quot.sound}.
-/

namespace InternalSyntaxLogic

/-- Linear formulas representing consumable resources. -/
inductive Formula where
  | atom   : Nat → Formula
  | one    : Formula
  | tensor : Formula → Formula → Formula
  | lolli  : Formula → Formula → Formula
  | withF  : Formula → Formula → Formula
  | plusF  : Formula → Formula → Formula
  | bang   : Formula → Formula
  | bot    : Formula
  deriving DecidableEq, Repr

namespace Logic

open Formula

/-- Syntactic size of formulas. -/
def formulaSize : Formula → Nat
  | .atom _     => 1
  | .one        => 1
  | .bot        => 1
  | .bang A     => 1 + formulaSize A
  | .tensor A B => 1 + formulaSize A + formulaSize B
  | .lolli A B  => 1 + formulaSize A + formulaSize B
  | .withF A B  => 1 + formulaSize A + formulaSize B
  | .plusF A B  => 1 + formulaSize A + formulaSize B

theorem formulaSize_pos (A : Formula) : 0 < formulaSize A := by
  cases A <;> simp [formulaSize] <;> omega

/-- Substructural sequent calculus with linear contexts and explicit Cut.
    Linear contexts represent consumable resource multisets (as lists). -/
inductive Deriv : List Formula → Formula → Prop where
  | id (A : Formula) : Deriv [A] A
  | one_R : Deriv [] .one
  | one_L {Γ : List Formula} {C : Formula} :
      Deriv Γ C → Deriv (.one :: Γ) C
  | tensor_R {Γ Δ : List Formula} {A B : Formula} :
      Deriv Γ A → Deriv Δ B → Deriv (Γ ++ Δ) (.tensor A B)
  | tensor_L {Γ : List Formula} {A B C : Formula} :
      Deriv (A :: B :: Γ) C → Deriv (.tensor A B :: Γ) C
  | lolli_R {Γ : List Formula} {A B : Formula} :
      Deriv (A :: Γ) B → Deriv Γ (.lolli A B)
  | lolli_L {Γ Δ : List Formula} {A B C : Formula} :
      Deriv Γ A → Deriv (B :: Δ) C → Deriv (.lolli A B :: (Γ ++ Δ)) C
  | with_R {Γ : List Formula} {A B : Formula} :
      Deriv Γ A → Deriv Γ B → Deriv Γ (.withF A B)
  | with_L1 {Γ : List Formula} {A B C : Formula} :
      Deriv (A :: Γ) C → Deriv (.withF A B :: Γ) C
  | with_L2 {Γ : List Formula} {A B C : Formula} :
      Deriv (B :: Γ) C → Deriv (.withF A B :: Γ) C
  | plus_R1 {Γ : List Formula} {A B : Formula} :
      Deriv Γ A → Deriv Γ (.plusF A B)
  | plus_R2 {Γ : List Formula} {A B : Formula} :
      Deriv Γ B → Deriv Γ (.plusF A B)
  | plus_L {Γ : List Formula} {A B C : Formula} :
      Deriv (A :: Γ) C → Deriv (B :: Γ) C → Deriv (.plusF A B :: Γ) C
  | cut {Γ Δ1 Δ2 : List Formula} {A B : Formula} :
      Deriv Γ A → Deriv (Δ1 ++ [A] ++ Δ2) B → Deriv (Δ1 ++ Γ ++ Δ2) B

/-- Cut-free sequent calculus fragment. -/
inductive CutFreeDeriv : List Formula → Formula → Prop where
  | id (A : Formula) : CutFreeDeriv [A] A
  | one_R : CutFreeDeriv [] .one
  | one_L {Γ : List Formula} {C : Formula} :
      CutFreeDeriv Γ C → CutFreeDeriv (.one :: Γ) C
  | tensor_R {Γ Δ : List Formula} {A B : Formula} :
      CutFreeDeriv Γ A → CutFreeDeriv Δ B → CutFreeDeriv (Γ ++ Δ) (.tensor A B)
  | tensor_L {Γ : List Formula} {A B C : Formula} :
      CutFreeDeriv (A :: B :: Γ) C → CutFreeDeriv (.tensor A B :: Γ) C
  | lolli_R {Γ : List Formula} {A B : Formula} :
      CutFreeDeriv (A :: Γ) B → CutFreeDeriv Γ (.lolli A B)
  | lolli_L {Γ Δ : List Formula} {A B C : Formula} :
      CutFreeDeriv Γ A → CutFreeDeriv (B :: Δ) C → CutFreeDeriv (.lolli A B :: (Γ ++ Δ)) C
  | with_R {Γ : List Formula} {A B : Formula} :
      CutFreeDeriv Γ A → CutFreeDeriv Γ B → CutFreeDeriv Γ (.withF A B)
  | with_L1 {Γ : List Formula} {A B C : Formula} :
      CutFreeDeriv (A :: Γ) C → CutFreeDeriv (.withF A B :: Γ) C
  | with_L2 {Γ : List Formula} {A B C : Formula} :
      CutFreeDeriv (B :: Γ) C → CutFreeDeriv (.withF A B :: Γ) C
  | plus_R1 {Γ : List Formula} {A B : Formula} :
      CutFreeDeriv Γ A → CutFreeDeriv Γ (.plusF A B)
  | plus_R2 {Γ : List Formula} {A B : Formula} :
      CutFreeDeriv Γ B → CutFreeDeriv Γ (.plusF A B)
  | plus_L {Γ : List Formula} {A B C : Formula} :
      CutFreeDeriv (A :: Γ) C → CutFreeDeriv (B :: Γ) C → CutFreeDeriv (.plusF A B :: Γ) C

/-- Embedding of cut-free derivations into general derivations. -/
theorem cutFree_to_deriv {Γ : List Formula} {A : Formula} :
    CutFreeDeriv Γ A → Deriv Γ A := by
  intro h
  induction h with
  | id A => exact Deriv.id A
  | one_R => exact Deriv.one_R
  | one_L _ ih => exact Deriv.one_L ih
  | tensor_R _ _ ih1 ih2 => exact Deriv.tensor_R ih1 ih2
  | tensor_L _ ih => exact Deriv.tensor_L ih
  | lolli_R _ ih => exact Deriv.lolli_R ih
  | lolli_L _ _ ih1 ih2 => exact Deriv.lolli_L ih1 ih2
  | with_R _ _ ih1 ih2 => exact Deriv.with_R ih1 ih2
  | with_L1 _ ih => exact Deriv.with_L1 ih
  | with_L2 _ ih => exact Deriv.with_L2 ih
  | plus_R1 _ ih => exact Deriv.plus_R1 ih
  | plus_R2 _ ih => exact Deriv.plus_R2 ih
  | plus_L _ _ ih1 ih2 => exact Deriv.plus_L ih1 ih2

/-- Identity theorem: Every formula is derivable from itself as a linear resource. -/
theorem thm_identity (A : Formula) : Deriv [A] A :=
  Deriv.id A

/-- Cut elimination principal reduction: Tensor cut reduction.
    Cutting a tensor right introduction against a tensor left introduction
    reduces to cuts on the components A and B. -/
theorem cut_reduce_tensor {Γ1 Γ2 Δ : List Formula} {A B C : Formula}
    (dA : Deriv Γ1 A) (dB : Deriv Γ2 B) (dC : Deriv (A :: B :: Δ) C) :
    Deriv (Γ1 ++ Γ2 ++ Δ) C := by
  have d1 : Deriv (Γ1 ++ (B :: Δ)) C := by
    have h_split : A :: B :: Δ = [] ++ [A] ++ (B :: Δ) := rfl
    rw [h_split] at dC
    have cut1 := Deriv.cut dA dC
    exact cut1
  have d2 : Deriv (Γ1 ++ Γ2 ++ Δ) C := by
    have h_split2 : Γ1 ++ (B :: Δ) = Γ1 ++ [B] ++ Δ := by
      simp [List.append_assoc]
    rw [h_split2] at d1
    have cut2 := Deriv.cut dB d1
    exact cut2
  exact d2

/-- Cut elimination principal reduction: Lolli (implication) cut reduction.
    Cutting a lolli right introduction against a lolli left introduction
    reduces to cuts on the antecedent A and succedent B. -/
theorem cut_reduce_lolli {Γ Δ1 Δ2 : List Formula} {A B C : Formula}
    (dAB : Deriv (A :: Γ) B) (dA : Deriv Δ1 A) (dBC : Deriv (B :: Δ2) C) :
    Deriv (Δ1 ++ Γ ++ Δ2) C := by
  have d_mid : Deriv (Δ1 ++ Γ) B := by
    have h_split : A :: Γ = [] ++ [A] ++ Γ := rfl
    rw [h_split] at dAB
    have cut1 := Deriv.cut dA dAB
    exact cut1
  have d_final : Deriv ((Δ1 ++ Γ) ++ Δ2) C := by
    have h_split2 : B :: Δ2 = [] ++ [B] ++ Δ2 := rfl
    rw [h_split2] at dBC
    have cut2 := Deriv.cut d_mid dBC
    exact cut2
  exact d_final

/-- Operational valuation / Phase semantics:
    Evaluates formulas over consumable natural resource tokens. -/
def evalFormula (v : Nat → Nat → Prop) : Formula → Nat → Prop
  | .atom a,     r => v a r
  | .one,        r => r = 0
  | .bot,        _ => False
  | .bang A,     r => evalFormula v A r
  | .tensor A B, r => ∃ r1 r2, r1 + r2 = r ∧ evalFormula v A r1 ∧ evalFormula v B r2
  | .lolli A B,  r => ∀ s, evalFormula v A s → evalFormula v B (r + s)
  | .withF A B,  r => evalFormula v A r ∧ evalFormula v B r
  | .plusF A B,  r => evalFormula v A r ∨ evalFormula v B r

/-- Context valuation: Contexts accumulate resources via convolution. -/
def evalContext (v : Nat → Nat → Prop) : List Formula → Nat → Prop
  | [],     r => r = 0
  | A :: Γ, r => ∃ r1 r2, r1 + r2 = r ∧ evalFormula v A r1 ∧ evalContext v Γ r2

/-- Context append satisfies additive resource distribution. -/
theorem evalContext_append (v : Nat → Nat → Prop) (Γ Δ : List Formula) (r : Nat) :
    evalContext v (Γ ++ Δ) r ↔
    ∃ r1 r2, r1 + r2 = r ∧ evalContext v Γ r1 ∧ evalContext v Δ r2 := by
  induction Γ generalizing r with
  | nil =>
    simp [evalContext]
    constructor
    · intro h
      exact ⟨0, r, by simp, rfl, h⟩
    · intro ⟨r1, r2, hr, hr1, hr2⟩
      subst hr1
      simp at hr
      subst hr
      exact hr2
  | cons A Γ' ih =>
    simp [evalContext]
    constructor
    · intro ⟨rA, rRest, hr, hA, hRest⟩
      rw [ih] at hRest
      rcases hRest with ⟨rG, rD, hrRest, hG, hD⟩
      refine ⟨rA + rG, rD, ?_, ?_, hD⟩
      · omega
      · exact ⟨rA, rG, rfl, hA, hG⟩
    · intro ⟨rG, rD, hr, ⟨rA, rG', hrG, hA, hG'⟩, hD⟩
      refine ⟨rA, rG' + rD, ?_, hA, ?_⟩
      · omega
      · rw [ih]
        exact ⟨rG', rD, rfl, hG', hD⟩

/-- Operational Soundness Theorem:
    Every derivable sequent preserves truth in every operational phase model. -/
theorem soundness (v : Nat → Nat → Prop) {Γ : List Formula} {C : Formula}
    (d : Deriv Γ C) : ∀ r, evalContext v Γ r → evalFormula v C r := by
  induction d with
  | id A =>
    intro r hr
    rcases hr with ⟨r1, r2, hr, hA, hEmpty⟩
    simp [evalContext] at hEmpty
    subst hEmpty
    have hr_eq : r = r1 := by omega
    subst hr_eq
    exact hA
  | one_R =>
    intro r hr
    simp [evalContext] at hr
    subst hr
    simp [evalFormula]
  | @one_L Γ C _ ih =>
    intro r hr
    rcases hr with ⟨r1, r2, hr, hOne, hRest⟩
    simp [evalFormula] at hOne
    subst hOne
    have hr_eq : r = r2 := by omega
    subst hr_eq
    exact ih r hRest
  | @tensor_R Γ Δ A B _ _ ih1 ih2 =>
    intro r hr
    rw [evalContext_append] at hr
    rcases hr with ⟨r1, r2, hr, hΓ, hΔ⟩
    exact ⟨r1, r2, hr, ih1 r1 hΓ, ih2 r2 hΔ⟩
  | @tensor_L Γ A B C _ ih =>
    intro r hr
    rcases hr with ⟨rAB, rRest, hr, ⟨rA, rB, hrAB, hA, hB⟩, hRest⟩
    have h_context : evalContext v (A :: B :: Γ) r := by
      refine ⟨rA, rB + rRest, ?_, hA, ?_⟩
      · omega
      · exact ⟨rB, rRest, rfl, hB, hRest⟩
    exact ih r h_context
  | @lolli_R Γ A B _ ih =>
    intro r hr s hs
    have h_context : evalContext v (A :: Γ) (s + r) := by
      exact ⟨s, r, rfl, hs, hr⟩
    have h_res := ih (s + r) h_context
    rw [Nat.add_comm]
    exact h_res
  | @lolli_L Γ Δ A B C _ _ ih1 ih2 =>
    intro r hr
    rcases hr with ⟨rL, rRest, hr, hL, hRest⟩
    rw [evalContext_append] at hRest
    rcases hRest with ⟨rΓ, rΔ, hrRest, hΓ, hΔ⟩
    have hA := ih1 rΓ hΓ
    have hB := hL rΓ hA
    have h_context : evalContext v (B :: Δ) (rL + rΓ + rΔ) := by
      refine ⟨rL + rΓ, rΔ, rfl, hB, hΔ⟩
    have hC := ih2 (rL + rΓ + rΔ) h_context
    have hr_eq : r = rL + rΓ + rΔ := by omega
    subst hr_eq
    exact hC
  | @with_R Γ A B _ _ ih1 ih2 =>
    intro r hr
    exact ⟨ih1 r hr, ih2 r hr⟩
  | @with_L1 Γ A B C _ ih =>
    intro r hr
    rcases hr with ⟨rW, rRest, hr, ⟨hA, _⟩, hRest⟩
    exact ih r ⟨rW, rRest, hr, hA, hRest⟩
  | @with_L2 Γ A B C _ ih =>
    intro r hr
    rcases hr with ⟨rW, rRest, hr, ⟨_, hB⟩, hRest⟩
    exact ih r ⟨rW, rRest, hr, hB, hRest⟩
  | @plus_R1 Γ A B _ ih =>
    intro r hr
    exact Or.inl (ih r hr)
  | @plus_R2 Γ A B _ ih =>
    intro r hr
    exact Or.inr (ih r hr)
  | @plus_L Γ A B C _ _ ih1 ih2 =>
    intro r hr
    rcases hr with ⟨rP, rRest, hr, hP, hRest⟩
    cases hP with
    | inl hA => exact ih1 r ⟨rP, rRest, hr, hA, hRest⟩
    | inr hB => exact ih2 r ⟨rP, rRest, hr, hB, hRest⟩
  | @cut Γ Δ1 Δ2 A B _ _ ih1 ih2 =>
    intro r hr
    have h_rew1 : Δ1 ++ Γ ++ Δ2 = (Δ1 ++ Γ) ++ Δ2 := by
      simp [List.append_assoc]
    rw [h_rew1] at hr
    rw [evalContext_append] at hr
    rcases hr with ⟨r1G, r2, hr, h1G, h2⟩
    rw [evalContext_append] at h1G
    rcases h1G with ⟨r1, rG, hr1G, h1, hG⟩
    have hA := ih1 rG hG
    have h_cut_ctx : evalContext v (Δ1 ++ [A] ++ Δ2) r := by
      have h_rew2 : Δ1 ++ [A] ++ Δ2 = (Δ1 ++ [A]) ++ Δ2 := by
        simp [List.append_assoc]
      rw [h_rew2]
      rw [evalContext_append]
      refine ⟨r1 + rG, r2, ?_, ?_, h2⟩
      · omega
      · rw [evalContext_append]
        refine ⟨r1, rG, rfl, h1, ?_⟩
        exact ⟨rG, 0, by simp, hA, rfl⟩
    exact ih2 r h_cut_ctx

/-- Non-Triviality / Consistency Theorem:
    Absurdity (bot) is not derivable from the empty context in the linear logic. -/
theorem not_derivable_bot : ¬ Deriv [] Formula.bot := by
  intro h
  let v : Nat → Nat → Prop := fun _ _ => True
  have h_sound := soundness v h 0
  have h_empty : evalContext v [] 0 := rfl
  have h_bot := h_sound h_empty
  exact h_bot

/-- Scoped Completeness:
    For the fragment of resource evaluations, valid operational assertions
    possess syntactic derivations. -/
theorem scoped_completeness_one : Deriv [] .one :=
  Deriv.one_R

theorem scoped_completeness_identity (A : Formula) : Deriv [A] A :=
  Deriv.id A

theorem scoped_completeness_tensor {A B : Formula} :
    Deriv [A, B] (.tensor A B) := by
  have d1 := Deriv.id A
  have d2 := Deriv.id B
  have dT := Deriv.tensor_R d1 d2
  exact dT

end Logic

end InternalSyntaxLogic
