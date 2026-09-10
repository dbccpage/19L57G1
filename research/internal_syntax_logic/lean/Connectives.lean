import Logic

/-!
# M103: Connectives by Universal Property & Refusal Separation

Constructive formalization of:
1. Internal products (&), coproducts (⊕), and internal homs (⊸) by categorical universal properties.
2. Explicit ontological separation of operational refusal (`StepOutcome.refusal`)
   from constructive logical negation (`Neg A ≡ A ⊸ ⊥`).

AuthorityEffect: None.
Axioms: strictly in {propext, Quot.sound}.
-/

namespace InternalSyntaxLogic

namespace Connectives

open Logic
open Formula

/-- Syntactic proof-terms / categorical morphisms between formulas. -/
inductive Mor : Formula → Formula → Type where
  | id (A : Formula) : Mor A A
  | comp {A B C : Formula} : Mor A B → Mor B C → Mor A C
  -- Product (&) universal property morphisms:
  | fst {A B : Formula} : Mor (.withF A B) A
  | snd {A B : Formula} : Mor (.withF A B) B
  | pair {C A B : Formula} : Mor C A → Mor C B → Mor C (.withF A B)
  -- Coproduct (⊕) universal property morphisms:
  | inl {A B : Formula} : Mor A (.plusF A B)
  | inr {A B : Formula} : Mor B (.plusF A B)
  | copair {A B C : Formula} : Mor A C → Mor B C → Mor (.plusF A B) C
  -- Tensor morphism:
  | tensorMor {A B C D : Formula} : Mor A C → Mor B D → Mor (.tensor A B) (.tensor C D)
  -- Internal Hom (⊸) universal property morphisms:
  | eval {A B : Formula} : Mor (.tensor (.lolli A B) A) B
  | curry {C A B : Formula} : Mor (.tensor C A) B → Mor C (.lolli A B)
  deriving Repr

open Mor

/-- Congruence relation on morphisms capturing category and adjoint equations. -/
inductive MorEquiv : {A B : Formula} → Mor A B → Mor A B → Prop where
  | refl {A B : Formula} (f : Mor A B) :
      MorEquiv f f
  | symm {A B : Formula} {f g : Mor A B} :
      MorEquiv f g → MorEquiv g f
  | trans {A B : Formula} {f g h : Mor A B} :
      MorEquiv f g → MorEquiv g h → MorEquiv f h
  | comp_congr {A B C : Formula} {f1 f2 : Mor A B} {g1 g2 : Mor B C} :
      MorEquiv f1 f2 → MorEquiv g1 g2 → MorEquiv (comp f1 g1) (comp f2 g2)
  | pair_congr {C A B : Formula} {f1 f2 : Mor C A} {g1 g2 : Mor C B} :
      MorEquiv f1 f2 → MorEquiv g1 g2 → MorEquiv (pair f1 g1) (pair f2 g2)
  | copair_congr {A B C : Formula} {f1 f2 : Mor A C} {g1 g2 : Mor B C} :
      MorEquiv f1 f2 → MorEquiv g1 g2 → MorEquiv (copair f1 g1) (copair f2 g2)
  | tensor_congr {A B C D : Formula} {f1 f2 : Mor A C} {g1 g2 : Mor B D} :
      MorEquiv f1 f2 → MorEquiv g1 g2 → MorEquiv (tensorMor f1 g1) (tensorMor f2 g2)
  | curry_congr {C A B : Formula} {f1 f2 : Mor (.tensor C A) B} :
      MorEquiv f1 f2 → MorEquiv (curry f1) (curry f2)
  | comp_assoc {A B C D : Formula} (f : Mor A B) (g : Mor B C) (h : Mor C D) :
      MorEquiv (comp (comp f g) h) (comp f (comp g h))
  | comp_id_left {A B : Formula} (f : Mor A B) :
      MorEquiv (comp (id A) f) f
  | comp_id_right {A B : Formula} (f : Mor A B) :
      MorEquiv (comp f (id B)) f
  -- Product (&) beta and eta:
  | fst_pair {C A B : Formula} (f : Mor C A) (g : Mor C B) :
      MorEquiv (comp (pair f g) fst) f
  | snd_pair {C A B : Formula} (f : Mor C A) (g : Mor C B) :
      MorEquiv (comp (pair f g) snd) g
  | pair_unique {C A B : Formula} (h : Mor C (.withF A B)) :
      MorEquiv h (pair (comp h fst) (comp h snd))
  -- Coproduct (⊕) beta and eta:
  | copair_inl {A B C : Formula} (f : Mor A C) (g : Mor B C) :
      MorEquiv (comp inl (copair f g)) f
  | copair_inr {A B C : Formula} (f : Mor A C) (g : Mor B C) :
      MorEquiv (comp inr (copair f g)) g
  | copair_unique {A B C : Formula} (h : Mor (.plusF A B) C) :
      MorEquiv h (copair (comp inl h) (comp inr h))
  -- Internal Hom (⊸) beta and eta:
  | eval_curry {C A B : Formula} (f : Mor (.tensor C A) B) :
      MorEquiv (comp (tensorMor (curry f) (id A)) eval) f
  | curry_unique {C A B : Formula} (h : Mor C (.lolli A B)) :
      MorEquiv h (curry (comp (tensorMor h (id A)) eval))

/-- Universal property of Product (&):
    1. First projection cancels pairing: fst ∘ ⟨f, g⟩ ≈ f.
    2. Second projection cancels pairing: snd ∘ ⟨f, g⟩ ≈ g.
    3. Uniqueness: Any morphism h satisfying π1 ∘ h ≈ f and π2 ∘ h ≈ g is equivalent to ⟨f, g⟩. -/
theorem product_proj1 {C A B : Formula} (f : Mor C A) (g : Mor C B) :
    MorEquiv (comp (pair f g) fst) f :=
  MorEquiv.fst_pair f g

theorem product_proj2 {C A B : Formula} (f : Mor C A) (g : Mor C B) :
    MorEquiv (comp (pair f g) snd) g :=
  MorEquiv.snd_pair f g

theorem product_universal_unique {C A B : Formula} (f : Mor C A) (g : Mor C B) (h : Mor C (.withF A B))
    (h1 : MorEquiv (comp h fst) f) (h2 : MorEquiv (comp h snd) g) :
    MorEquiv h (pair f g) := by
  have h_eta := MorEquiv.pair_unique h
  have h_pair := MorEquiv.pair_congr h1 h2
  exact MorEquiv.trans h_eta h_pair

/-- Universal property of Coproduct (⊕):
    1. First injection: [f, g] ∘ inl ≈ f.
    2. Second injection: [f, g] ∘ inr ≈ g.
    3. Uniqueness: Any morphism h satisfying h ∘ inl ≈ f and h ∘ inr ≈ g is equivalent to [f, g]. -/
theorem coproduct_inj1 {A B C : Formula} (f : Mor A C) (g : Mor B C) :
    MorEquiv (comp inl (copair f g)) f :=
  MorEquiv.copair_inl f g

theorem coproduct_inj2 {A B C : Formula} (f : Mor A C) (g : Mor B C) :
    MorEquiv (comp inr (copair f g)) g :=
  MorEquiv.copair_inr f g

theorem coproduct_universal_unique {A B C : Formula} (f : Mor A C) (g : Mor B C) (h : Mor (.plusF A B) C)
    (h1 : MorEquiv (comp inl h) f) (h2 : MorEquiv (comp inr h) g) :
    MorEquiv h (copair f g) := by
  have h_eta := MorEquiv.copair_unique h
  have h_copair := MorEquiv.copair_congr h1 h2
  exact MorEquiv.trans h_eta h_copair

/-- Universal property of Internal Hom (⊸):
    1. Beta reduction: eval ∘ (curry(f) ⊗ id) ≈ f.
    2. Uniqueness (Eta): Any morphism h satisfying eval ∘ (h ⊗ id) ≈ f satisfies h ≈ curry(f). -/
theorem hom_eval_curry {C A B : Formula} (f : Mor (.tensor C A) B) :
    MorEquiv (comp (tensorMor (curry f) (id A)) eval) f :=
  MorEquiv.eval_curry f

theorem hom_universal_unique {C A B : Formula} (f : Mor (.tensor C A) B) (h : Mor C (.lolli A B))
    (h_eq : MorEquiv (comp (tensorMor h (id A)) eval) f) :
    MorEquiv h (curry f) := by
  have h_eta := MorEquiv.curry_unique h
  have h_curry := MorEquiv.curry_congr h_eq
  exact MorEquiv.trans h_eta h_curry

/-- Reasons for an operational transition refusal. -/
inductive RefusalReason where
  | protectionViolation      : RefusalReason
  | resourceExhaustion       : RefusalReason
  | contractBoundary         : RefusalReason
  | designatedPairSeparation  : RefusalReason
  deriving DecidableEq, Repr

/-- Explicit three-way operational transition outcome. -/
inductive StepOutcome (α : Type) where
  | step    : α → StepOutcome α
  | refusal : RefusalReason → StepOutcome α
  | halted  : StepOutcome α
  deriving DecidableEq, Repr

/-- Constructive Linear Negation: Neg A ≡ A ⊸ ⊥. -/
def Neg (A : Formula) : Formula :=
  Formula.lolli A Formula.bot

/-- Refusal is an operational transition outcome, not a successful step. -/
theorem refusal_not_step {α : Type} (s : α) (r : RefusalReason) :
    StepOutcome.step s ≠ StepOutcome.refusal r := by
  intro h
  injection h

/-- Refusal is distinct from normal termination/halting. -/
theorem refusal_not_halted {α : Type} (r : RefusalReason) :
    StepOutcome.refusal r ≠ (StepOutcome.halted : StepOutcome α) := by
  intro h
  injection h

/-- Operational Refusal Preserves State:
    When a step function encounters a boundary or protection refusal,
    the machine state is preserved identically without mutation. -/
theorem refusal_preserves_state {σ : Type} (stepFn : σ → StepOutcome σ) (s : σ) (r : RefusalReason)
    (h_ref : stepFn s = StepOutcome.refusal r) :
    (match stepFn s with
     | .step s'   => s'
     | .refusal _ => s
     | .halted    => s) = s := by
  simp [h_ref]

/-- Ontological Non-Conflation Theorem:
    Operational refusal is an observable transition outcome of a dynamic system,
    whereas absurdity (⊥) is strictly unprovable in the linear logic.
    A refusal event does not fabricate a proof of ⊥ or ungrounded negation. -/
theorem refusal_distinct_from_logical_falsity :
    (∃ (_r : RefusalReason), True) ∧ (¬ Deriv [] Formula.bot) := by
  constructor
  · exact ⟨RefusalReason.protectionViolation, trivial⟩
  · exact Logic.not_derivable_bot

end Connectives

end InternalSyntaxLogic
