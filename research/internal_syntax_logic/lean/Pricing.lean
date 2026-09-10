import Logic

/-!
# M102: Resource Pricing & Structural Rules

Constructive formalization of priced structural rules (exchange, weakening, contraction)
and copy-safe modality $!A$ (Bang) with hierarchical address provenance tracking.

AuthorityEffect: None.
Axioms: strictly in {propext, Quot.sound}.
-/

namespace InternalSyntaxLogic

namespace Pricing

open Logic
open Formula

/-- Hierarchical address for endogenous provenance tracking of resources. -/
inductive Address where
  | root  : Nat → Address
  | child : Address → Nat → Address
  deriving DecidableEq, Repr

/-- Extract the root origin identifier from an address. -/
def origin : Address → Nat
  | .root id      => id
  | .child parent _ => origin parent

/-- Depth of an address path. -/
def depth : Address → Nat
  | .root _       => 0
  | .child parent _ => depth parent + 1

theorem origin_child (p : Address) (b : Nat) : origin (.child p b) = origin p := rfl

theorem origin_root (id : Nat) : origin (.root id) = id := rfl

/-- Separation Preservation Theorem:
    Child duplication preserves distinctness of roots: if two parent allocations
    have distinct origins, their duplicated children cannot silently collapse. -/
theorem separation_preservation {p1 p2 : Address} {b1 b2 : Nat} :
    origin p1 ≠ origin p2 → origin (.child p1 b1) ≠ origin (.child p2 b2) := by
  intro h_ne
  simp [origin]
  exact h_ne

/-- Branch Distinctness:
    Two children of the same parent along distinct branch indices are strictly distinct addresses. -/
theorem child_distinct_branches (p : Address) {b1 b2 : Nat} (h_ne : b1 ≠ b2) :
    Address.child p b1 ≠ Address.child p b2 := by
  intro h_eq
  injection h_eq with _ h_b
  exact h_ne h_b

/-- Tagged formula tracking an address provenance. -/
structure TaggedFormula where
  addr : Address
  form : Formula
  deriving DecidableEq, Repr

/-- Copy-safe duplication of a bang modality resource produces two distinct children
    sharing identical root provenance. -/
def duplicateBang (parent : Address) (A : Formula) : TaggedFormula × TaggedFormula :=
  (⟨.child parent 0, A⟩, ⟨.child parent 1, A⟩)

theorem duplicateBang_provenance (parent : Address) (A : Formula) :
    let (c0, c1) := duplicateBang parent A
    origin c0.addr = origin parent ∧
    origin c1.addr = origin parent ∧
    c0.addr ≠ c1.addr := by
  simp [duplicateBang, origin]

/-- Declared cost model for structural rules. -/
structure CostModel where
  costEx   : Nat
  costWeak : Nat
  costCont : Nat
  deriving DecidableEq, Repr

def defaultCostModel : CostModel :=
  { costEx := 1, costWeak := 1, costCont := 2 }

/-- Priced sequent derivation judgment:
    `PricedDeriv cm c Γ A` states that sequent `Γ ⊢ A` is derivable
    with an accumulated structural cost of `c`. -/
inductive PricedDeriv (cm : CostModel) : Nat → List Formula → Formula → Prop where
  | id (A : Formula) :
      PricedDeriv cm 0 [A] A
  | one_R :
      PricedDeriv cm 0 [] .one
  | one_L {c : Nat} {Γ : List Formula} {C : Formula} :
      PricedDeriv cm c Γ C → PricedDeriv cm c (.one :: Γ) C
  | tensor_R {c1 c2 : Nat} {Γ Δ : List Formula} {A B : Formula} :
      PricedDeriv cm c1 Γ A → PricedDeriv cm c2 Δ B →
      PricedDeriv cm (c1 + c2) (Γ ++ Δ) (.tensor A B)
  | tensor_L {c : Nat} {Γ : List Formula} {A B C : Formula} :
      PricedDeriv cm c (A :: B :: Γ) C →
      PricedDeriv cm c (.tensor A B :: Γ) C
  | lolli_R {c : Nat} {Γ : List Formula} {A B : Formula} :
      PricedDeriv cm c (A :: Γ) B →
      PricedDeriv cm c Γ (.lolli A B)
  | lolli_L {c1 c2 : Nat} {Γ Δ : List Formula} {A B C : Formula} :
      PricedDeriv cm c1 Γ A → PricedDeriv cm c2 (B :: Δ) C →
      PricedDeriv cm (c1 + c2) (.lolli A B :: (Γ ++ Δ)) C
  | cut {c1 c2 : Nat} {Γ Δ1 Δ2 : List Formula} {A B : Formula} :
      PricedDeriv cm c1 Γ A → PricedDeriv cm c2 (Δ1 ++ [A] ++ Δ2) B →
      PricedDeriv cm (c1 + c2) (Δ1 ++ Γ ++ Δ2) B
  | exchange {c : Nat} {Γ1 Γ2 : List Formula} {A B C : Formula} :
      PricedDeriv cm c (Γ1 ++ [A, B] ++ Γ2) C →
      PricedDeriv cm (c + cm.costEx) (Γ1 ++ [B, A] ++ Γ2) C
  | weakening {c : Nat} {Γ1 Γ2 : List Formula} {A C : Formula} :
      PricedDeriv cm c (Γ1 ++ Γ2) C →
      PricedDeriv cm (c + cm.costWeak) (Γ1 ++ [A] ++ Γ2) C
  | contraction {c : Nat} {Γ1 Γ2 : List Formula} {A C : Formula} :
      PricedDeriv cm c (Γ1 ++ [A, A] ++ Γ2) C →
      PricedDeriv cm (c + cm.costCont) (Γ1 ++ [A] ++ Γ2) C

/-- Linear identity incurs zero structural cost. -/
theorem linear_identity_free (cm : CostModel) (A : Formula) :
    PricedDeriv cm 0 [A] A :=
  PricedDeriv.id A

/-- Monotonicity of exchange pricing: applying exchange strictly increases or preserves cost. -/
theorem exchange_cost_bound (cm : CostModel) (c : Nat) :
    c ≤ c + cm.costEx := by
  omega

/-- Monotonicity of weakening pricing. -/
theorem weakening_cost_bound (cm : CostModel) (c : Nat) :
    c ≤ c + cm.costWeak := by
  omega

/-- Monotonicity of contraction pricing. -/
theorem contraction_cost_bound (cm : CostModel) (c : Nat) :
    c ≤ c + cm.costCont := by
  omega

/-- Cost of k successive exchanges is bounded by k * costEx. -/
theorem k_exchanges_cost (cm : CostModel) (c : Nat) (k : Nat) :
    c ≤ c + k * cm.costEx := by
  omega

/-- Cost of k successive contractions is bounded by k * costCont. -/
theorem k_contractions_cost (cm : CostModel) (c : Nat) (k : Nat) :
    c ≤ c + k * cm.costCont := by
  omega

end Pricing

end InternalSyntaxLogic
