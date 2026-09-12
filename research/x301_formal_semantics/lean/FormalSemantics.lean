/-!
# Target X301: Formal Semantics, Empirical Reference & Intervention Grounding
("Panel agreement is not truth").

Constructive formalization of:
1. Operational Formula Syntax & Exact Valuation Poset (Heyting truth structure).
2. Compositional Satisfaction (M, σ ⊨ φ).
3. Translation & Canonical Isomorphism Invariance (G012 translation commutation).
4. Executable Intervention Relations & Counterfactual Discrimination.
5. Behavioral Observational Congruence (φ ≡_obs ψ).
6. Multi-Observer Panel Consensus vs Ground Intervention Refutation (Grounding Firewall).

AuthorityEffect: None.
Constructive: 100% core Lean 4, zero Classical.choice, zero mathlib.
Axioms: strictly within {propext, Quot.sound}.
-/

namespace X301FormalSemantics

set_option linter.unusedVariables false

-- ============================================================================
-- 1. Exact Constructive Valuation Poset (Heyting Truth Structure)
-- ============================================================================

/-- Constructive truth valuation domain.
    Values represent degrees of constructive operational evidence:
    - `zero`: absolute operational refutation / refusal
    - `half`: intermediate / incomplete operational evidence
    - `one`: verified operational ground truth
-/
inductive TruthVal where
  | zero : TruthVal
  | half : TruthVal
  | one : TruthVal
  deriving DecidableEq, Repr

namespace TruthVal

/-- Poset ordering on truth valuations. -/
def le : TruthVal → TruthVal → Prop
  | zero, _ => True
  | half, zero => False
  | half, half => True
  | half, one => True
  | one, one => True
  | one, _ => False

instance : LE TruthVal where
  le := TruthVal.le

/-- Decidable poset ordering. -/
def leBool : TruthVal → TruthVal → Bool
  | zero, _ => true
  | half, zero => false
  | half, half => true
  | half, one => true
  | one, one => true
  | one, _ => false

instance (a b : TruthVal) : Decidable (a ≤ b) :=
  match a, b with
  | zero, zero => isTrue True.intro
  | zero, half => isTrue True.intro
  | zero, one => isTrue True.intro
  | half, zero => isFalse (by intro h; cases h)
  | half, half => isTrue True.intro
  | half, one => isTrue True.intro
  | one, zero => isFalse (by intro h; cases h)
  | one, half => isFalse (by intro h; cases h)
  | one, one => isTrue True.intro

/-- Meet (infimum / conjunction) in the truth poset. -/
def meet : TruthVal → TruthVal → TruthVal
  | zero, _ => zero
  | _, zero => zero
  | half, half => half
  | half, one => half
  | one, half => half
  | one, one => one

/-- Join (supremum / disjunction) in the truth poset. -/
def join : TruthVal → TruthVal → TruthVal
  | one, _ => one
  | _, one => one
  | half, half => half
  | half, zero => half
  | zero, half => half
  | zero, zero => zero

/-- Heyting operational implication: a ⇒ b.
    Constructively, evidence for a ⇒ b is maximum truth when a ≤ b, else b. -/
def imp : TruthVal → TruthVal → TruthVal
  | zero, _ => one
  | half, zero => zero
  | half, half => one
  | half, one => one
  | one, b => b

/-- Operational negation as refusal / disjointness: ¬a := a ⇒ 0. -/
def neg (a : TruthVal) : TruthVal :=
  imp a zero

end TruthVal

-- Poset & Heyting Truth Structure Theorems

theorem truth_val_le_refl (a : TruthVal) : a ≤ a := by
  cases a <;> decide

theorem truth_val_le_trans {a b c : TruthVal} (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  cases a <;> cases b <;> cases c <;> first | contradiction | decide

theorem truth_val_le_antisymm {a b : TruthVal} (h1 : a ≤ b) (h2 : b ≤ a) : a = b := by
  cases a <;> cases b <;> first | rfl | contradiction

theorem truth_val_meet_comm (a b : TruthVal) : TruthVal.meet a b = TruthVal.meet b a := by
  cases a <;> cases b <;> rfl

theorem truth_val_meet_assoc (a b c : TruthVal) :
    TruthVal.meet (TruthVal.meet a b) c = TruthVal.meet a (TruthVal.meet b c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem truth_val_join_comm (a b : TruthVal) : TruthVal.join a b = TruthVal.join b a := by
  cases a <;> cases b <;> rfl

theorem truth_val_join_assoc (a b c : TruthVal) :
    TruthVal.join (TruthVal.join a b) c = TruthVal.join a (TruthVal.join b c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem heyting_imp_self (a : TruthVal) : TruthVal.imp a a = TruthVal.one := by
  cases a <;> rfl

theorem heyting_modus_ponens (a b : TruthVal) : TruthVal.meet a (TruthVal.imp a b) ≤ b := by
  cases a <;> cases b <;> decide

theorem heyting_neg_refusal :
    TruthVal.neg TruthVal.one = TruthVal.zero ∧ TruthVal.neg TruthVal.zero = TruthVal.one := by
  decide

theorem constructive_non_contradiction (a : TruthVal) :
    TruthVal.meet a (TruthVal.neg a) = TruthVal.zero := by
  cases a <;> rfl

theorem constructive_lem_fails :
    ∃ a : TruthVal, TruthVal.join a (TruthVal.neg a) ≠ TruthVal.one :=
  ⟨TruthVal.half, by decide⟩


-- ============================================================================
-- 2. Operational Syntax, Relational Carrier Models & Satisfaction
-- ============================================================================

/-- Operational terms: variables or domain constant data elements. -/
inductive Term where
  | var : Nat → Term
  | const : Nat → Term
  deriving DecidableEq, Repr

/-- Evaluation of terms under a variable assignment σ. -/
def evalTerm (σ : Nat → Nat) : Term → Nat
  | .var v => σ v
  | .const c => c

/-- Operational formulas over relational carrier states. -/
inductive Formula where
  | atom : Nat → List Term → Formula
  | ident : Term → Term → Formula
  | conj : Formula → Formula → Formula
  | disj : Formula → Formula → Formula
  | imp : Formula → Formula → Formula
  | neg : Formula → Formula
  | bforall : Nat → List Nat → Formula → Formula
  | bexists : Nat → List Nat → Formula → Formula
  deriving DecidableEq, Repr

/-- Structural size of a formula. -/
def formulaSize : Formula → Nat
  | .atom _ _ => 1
  | .ident _ _ => 1
  | .conj f1 f2 => 1 + formulaSize f1 + formulaSize f2
  | .disj f1 f2 => 1 + formulaSize f1 + formulaSize f2
  | .imp f1 f2 => 1 + formulaSize f1 + formulaSize f2
  | .neg f => 1 + formulaSize f
  | .bforall _ _ body => 1 + formulaSize body
  | .bexists _ _ body => 1 + formulaSize body

/-- Relational carrier model representing ground state structure. -/
structure RelModel where
  dataCount : Nat
  relVal : Nat → List Nat → TruthVal

/-- Extend a variable assignment σ with var ↦ val. -/
def extendAssign (σ : Nat → Nat) (var : Nat) (val : Nat) : Nat → Nat :=
  fun x => if x = var then val else σ x

/-- Finite domain infimum helper. -/
def foldMeetDom (f : Nat → TruthVal) : List Nat → TruthVal
  | [] => TruthVal.one
  | d :: ds => TruthVal.meet (f d) (foldMeetDom f ds)

/-- Finite domain supremum helper. -/
def foldJoinDom (f : Nat → TruthVal) : List Nat → TruthVal
  | [] => TruthVal.zero
  | d :: ds => TruthVal.join (f d) (foldJoinDom f ds)

/-- Compositional evaluation of a formula under model M and assignment σ. -/
def evalFormula (M : RelModel) (σ : Nat → Nat) : Formula → TruthVal
  | .atom r args =>
      M.relVal r (args.map (evalTerm σ))
  | .ident t1 t2 =>
      if evalTerm σ t1 = evalTerm σ t2 then TruthVal.one else TruthVal.zero
  | .conj f1 f2 =>
      TruthVal.meet (evalFormula M σ f1) (evalFormula M σ f2)
  | .disj f1 f2 =>
      TruthVal.join (evalFormula M σ f1) (evalFormula M σ f2)
  | .imp f1 f2 =>
      TruthVal.imp (evalFormula M σ f1) (evalFormula M σ f2)
  | .neg f =>
      TruthVal.neg (evalFormula M σ f)
  | .bforall var dom body =>
      foldMeetDom (fun d => evalFormula M (extendAssign σ var d) body) dom
  | .bexists var dom body =>
      foldJoinDom (fun d => evalFormula M (extendAssign σ var d) body) dom

/-- Constructive compositional satisfaction: M, σ ⊨ φ. -/
def Satisfies (M : RelModel) (σ : Nat → Nat) (φ : Formula) : Prop :=
  evalFormula M σ φ = TruthVal.one

theorem meet_eq_one_iff (a b : TruthVal) :
    TruthVal.meet a b = TruthVal.one ↔ a = TruthVal.one ∧ b = TruthVal.one := by
  cases a <;> cases b <;> decide

theorem join_eq_one_of_left (a b : TruthVal) (h : a = TruthVal.one) :
    TruthVal.join a b = TruthVal.one := by
  subst h
  cases b <;> rfl

theorem join_eq_one_of_right (a b : TruthVal) (h : b = TruthVal.one) :
    TruthVal.join a b = TruthVal.one := by
  subst h
  cases a <;> rfl

theorem neg_eq_one_iff (a : TruthVal) :
    TruthVal.neg a = TruthVal.one ↔ a = TruthVal.zero := by
  cases a <;> decide

theorem satisfaction_compositional_conj (M : RelModel) (σ : Nat → Nat) (f1 f2 : Formula) :
    Satisfies M σ (.conj f1 f2) ↔ Satisfies M σ f1 ∧ Satisfies M σ f2 := by
  dsimp [Satisfies, evalFormula]
  exact meet_eq_one_iff (evalFormula M σ f1) (evalFormula M σ f2)

theorem satisfaction_compositional_disj (M : RelModel) (σ : Nat → Nat) (f1 f2 : Formula) :
    Satisfies M σ f1 ∨ Satisfies M σ f2 → Satisfies M σ (.disj f1 f2) := by
  intro h
  dsimp [Satisfies, evalFormula]
  cases h with
  | inl h1 => exact join_eq_one_of_left _ _ h1
  | inr h2 => exact join_eq_one_of_right _ _ h2

theorem satisfaction_compositional_neg (M : RelModel) (σ : Nat → Nat) (f : Formula) :
    Satisfies M σ (.neg f) ↔ evalFormula M σ f = TruthVal.zero := by
  dsimp [Satisfies, evalFormula]
  exact neg_eq_one_iff (evalFormula M σ f)

theorem satisfaction_modus_ponens (M : RelModel) (σ : Nat → Nat) (f1 f2 : Formula) :
    Satisfies M σ (.imp f1 f2) → Satisfies M σ f1 → Satisfies M σ f2 := by
  intro h_imp h_prem
  dsimp [Satisfies, evalFormula] at *
  rw [h_prem] at h_imp
  dsimp [TruthVal.imp] at h_imp
  exact h_imp

theorem satisfaction_refuses_contradiction (M : RelModel) (σ : Nat → Nat) (f : Formula) :
    ¬ Satisfies M σ (.conj f (.neg f)) := by
  intro h
  rw [satisfaction_compositional_conj] at h
  have h_val := h.1
  have h_neg := h.2
  rw [satisfaction_compositional_neg] at h_neg
  dsimp [Satisfies] at h_val
  rw [h_neg] at h_val
  contradiction


-- ============================================================================
-- 3. Canonical Isomorphisms, Signature Transport & Truth Invariance
-- ============================================================================

/-- Canonical isomorphism between two relational models M and N. -/
structure Iso (M N : RelModel) where
  f_data : Nat → Nat
  g_data : Nat → Nat
  f_rel : Nat → Nat
  g_rel : Nat → Nat
  h_data_left : ∀ x, g_data (f_data x) = x
  h_data_right : ∀ y, f_data (g_data y) = y
  h_rel_left : ∀ r, g_rel (f_rel r) = r
  h_rel_right : ∀ r, f_rel (g_rel r) = r
  rel_compat : ∀ r args, N.relVal (f_rel r) (args.map f_data) = M.relVal r args

theorem iso_data_inj (τ : Iso M N) {x y : Nat} (h : τ.f_data x = τ.f_data y) : x = y := by
  have h_left := congrArg τ.g_data h
  rw [τ.h_data_left, τ.h_data_left] at h_left
  exact h_left

/-- Transport a term under data renaming. -/
def renameTerm (f_data : Nat → Nat) : Term → Term
  | .var v => .var v
  | .const c => .const (f_data c)

/-- Transport a variable assignment σ under data renaming. -/
def transportAssign (τ : Iso M N) (σ : Nat → Nat) : Nat → Nat :=
  fun v => τ.f_data (σ v)

theorem translation_commutes_term (τ : Iso M N) (σ : Nat → Nat) (t : Term) :
    evalTerm (transportAssign τ σ) (renameTerm τ.f_data t) = τ.f_data (evalTerm σ t) := by
  cases t with
  | var v => rfl
  | const c => rfl

/-- Transport a formula under model isomorphism. -/
def renameFormula (τ : Iso M N) : Formula → Formula
  | .atom r args =>
      .atom (τ.f_rel r) (args.map (renameTerm τ.f_data))
  | .ident t1 t2 =>
      .ident (renameTerm τ.f_data t1) (renameTerm τ.f_data t2)
  | .conj f1 f2 =>
      .conj (renameFormula τ f1) (renameFormula τ f2)
  | .disj f1 f2 =>
      .disj (renameFormula τ f1) (renameFormula τ f2)
  | .imp f1 f2 =>
      .imp (renameFormula τ f1) (renameFormula τ f2)
  | .neg f =>
      .neg (renameFormula τ f)
  | .bforall var dom body =>
      .bforall var (dom.map τ.f_data) (renameFormula τ body)
  | .bexists var dom body =>
      .bexists var (dom.map τ.f_data) (renameFormula τ body)

theorem extendAssign_comm_transport (τ : Iso M N) (σ : Nat → Nat) (var val : Nat) :
    extendAssign (transportAssign τ σ) var (τ.f_data val) =
    transportAssign τ (extendAssign σ var val) := by
  funext x
  dsimp [extendAssign, transportAssign]
  by_cases h : x = var
  · subst h
    simp
  · simp [h]

theorem foldMeetDom_comm_transport (τ : Iso M N) (σ : Nat → Nat) (var : Nat) (body : Formula)
    (ih : ∀ σ', evalFormula N (transportAssign τ σ') (renameFormula τ body) = evalFormula M σ' body) :
    ∀ dom, foldMeetDom (fun d' => evalFormula N (extendAssign (transportAssign τ σ) var d') (renameFormula τ body)) (dom.map τ.f_data) =
           foldMeetDom (fun d => evalFormula M (extendAssign σ var d) body) dom
  | [] => rfl
  | d :: ds => by
      dsimp [foldMeetDom, List.map]
      rw [extendAssign_comm_transport]
      rw [ih (extendAssign σ var d)]
      have ih_ds := foldMeetDom_comm_transport τ σ var body ih ds
      rw [ih_ds]

theorem foldJoinDom_comm_transport (τ : Iso M N) (σ : Nat → Nat) (var : Nat) (body : Formula)
    (ih : ∀ σ', evalFormula N (transportAssign τ σ') (renameFormula τ body) = evalFormula M σ' body) :
    ∀ dom, foldJoinDom (fun d' => evalFormula N (extendAssign (transportAssign τ σ) var d') (renameFormula τ body)) (dom.map τ.f_data) =
           foldJoinDom (fun d => evalFormula M (extendAssign σ var d) body) dom
  | [] => rfl
  | d :: ds => by
      dsimp [foldJoinDom, List.map]
      rw [extendAssign_comm_transport]
      rw [ih (extendAssign σ var d)]
      have ih_ds := foldJoinDom_comm_transport τ σ var body ih ds
      rw [ih_ds]

theorem translation_commutes_formula (τ : Iso M N) (σ : Nat → Nat) (φ : Formula) :
    evalFormula N (transportAssign τ σ) (renameFormula τ φ) = evalFormula M σ φ := by
  induction φ generalizing σ with
  | atom r args =>
      dsimp [evalFormula, renameFormula]
      have h_comp : (evalTerm (transportAssign τ σ) ∘ renameTerm τ.f_data) = (τ.f_data ∘ evalTerm σ) := by
        funext t
        exact translation_commutes_term τ σ t
      have h_map : (args.map (renameTerm τ.f_data)).map (evalTerm (transportAssign τ σ)) =
                   (args.map (evalTerm σ)).map τ.f_data := by
        simp only [List.map_map, h_comp]
      rw [h_map]
      exact τ.rel_compat r (args.map (evalTerm σ))
  | ident t1 t2 =>
      dsimp [evalFormula, renameFormula]
      rw [translation_commutes_term τ σ t1, translation_commutes_term τ σ t2]
      by_cases h : evalTerm σ t1 = evalTerm σ t2
      · rw [if_pos h]
        have h_f : τ.f_data (evalTerm σ t1) = τ.f_data (evalTerm σ t2) := by rw [h]
        rw [if_pos h_f]
      · rw [if_neg h]
        have h_neq : τ.f_data (evalTerm σ t1) ≠ τ.f_data (evalTerm σ t2) := by
          intro h_eq
          exact h (iso_data_inj τ h_eq)
        rw [if_neg h_neq]
  | conj f1 f2 ih1 ih2 =>
      dsimp [evalFormula, renameFormula]
      rw [ih1, ih2]
  | disj f1 f2 ih1 ih2 =>
      dsimp [evalFormula, renameFormula]
      rw [ih1, ih2]
  | imp f1 f2 ih1 ih2 =>
      dsimp [evalFormula, renameFormula]
      rw [ih1, ih2]
  | neg f ih =>
      dsimp [evalFormula, renameFormula]
      rw [ih]
  | bforall var dom body ih =>
      dsimp [evalFormula, renameFormula]
      exact foldMeetDom_comm_transport τ σ var body ih dom
  | bexists var dom body ih =>
      dsimp [evalFormula, renameFormula]
      exact foldJoinDom_comm_transport τ σ var body ih dom

/-- Main Invariance Theorem (G012 translation commutation):
    Truth satisfaction is strictly invariant under canonical isomorphism. -/
theorem translation_commutes_satisfaction (τ : Iso M N) (σ : Nat → Nat) (φ : Formula) :
    Satisfies M σ φ ↔ Satisfies N (transportAssign τ σ) (renameFormula τ φ) := by
  dsimp [Satisfies]
  rw [translation_commutes_formula]


-- ============================================================================
-- 4. Executable Interventions & Counterfactual Discrimination
-- ============================================================================

/-- Executable atomic state interventions. -/
inductive AtomicIntervention where
  | setRel (r : Nat) (args : List Nat) (v : TruthVal)
  | addData (count : Nat)
  deriving DecidableEq, Repr

/-- Apply an atomic intervention to a model. -/
def applyAtomic (op : AtomicIntervention) (M : RelModel) : RelModel :=
  match op with
  | .setRel r args v =>
      { M with
        relVal := fun r' args' =>
          if r' = r ∧ args' = args then v else M.relVal r' args' }
  | .addData c =>
      { M with dataCount := M.dataCount + c }

/-- An intervention sequence is a finite chain of executable perturbations. -/
def InterventionSeq := List AtomicIntervention

/-- Apply an intervention sequence sequentially. -/
def applySeq (ops : InterventionSeq) (M : RelModel) : RelModel :=
  ops.foldl (fun m op => applyAtomic op m) M

theorem intervention_apply_empty (M : RelModel) : applySeq [] M = M := rfl

/-- An intervention sequence discriminates formula φ if the observable readout changes. -/
def Discriminates (I : InterventionSeq) (M : RelModel) (σ : Nat → Nat) (φ : Formula) : Prop :=
  evalFormula (applySeq I M) σ φ ≠ evalFormula M σ φ

/-- Operational empirical reference: φ has empirical reference at M iff
    there exists an admissible intervention sequence that discriminates φ. -/
def HasEmpiricalReferenceAt (admissible : List InterventionSeq) (M : RelModel)
    (σ : Nat → Nat) (φ : Formula) : Prop :=
  ∃ I ∈ admissible, Discriminates I M σ φ

theorem intervention_discriminates_reference (admissible : List InterventionSeq)
    (M : RelModel) (σ : Nat → Nat) (φ : Formula) (I : InterventionSeq)
    (h_mem : I ∈ admissible) (h_disc : Discriminates I M σ φ) :
    HasEmpiricalReferenceAt admissible M σ φ :=
  ⟨I, h_mem, h_disc⟩

theorem empty_intervention_cannot_discriminate (M : RelModel) (σ : Nat → Nat) (φ : Formula) :
    ¬ Discriminates [] M σ φ := by
  intro h
  dsimp [Discriminates, applySeq] at h
  contradiction


-- ============================================================================
-- 5. Behavioral Observational Congruence
-- ============================================================================

/-- Two formulas are behaviorally congruent across states and admissible interventions
    if no admissible intervention sequence can ever distinguish their observable readouts. -/
def BehavioralCongruent (admissible : List InterventionSeq) (states : List RelModel)
    (σ : Nat → Nat) (φ ψ : Formula) : Prop :=
  ∀ M ∈ states, ∀ I ∈ admissible,
    evalFormula (applySeq I M) σ φ = evalFormula (applySeq I M) σ ψ

theorem behavioral_congruence_refl (admissible : List InterventionSeq) (states : List RelModel)
    (σ : Nat → Nat) (φ : Formula) :
    BehavioralCongruent admissible states σ φ φ := by
  intros M _ I _
  rfl

theorem behavioral_congruence_symm (admissible : List InterventionSeq) (states : List RelModel)
    (σ : Nat → Nat) (φ ψ : Formula) :
    BehavioralCongruent admissible states σ φ ψ →
    BehavioralCongruent admissible states σ ψ φ := by
  intro h M hM I hI
  exact (h M hM I hI).symm

theorem behavioral_congruence_trans (admissible : List InterventionSeq) (states : List RelModel)
    (σ : Nat → Nat) (φ ψ θ : Formula) :
    BehavioralCongruent admissible states σ φ ψ →
    BehavioralCongruent admissible states σ ψ θ →
    BehavioralCongruent admissible states σ φ θ := by
  intro h1 h2 M hM I hI
  rw [h1 M hM I hI, h2 M hM I hI]

theorem decorative_distinction_rejected (admissible : List InterventionSeq) (states : List RelModel)
    (σ : Nat → Nat) (φ ψ : Formula) (h_cong : BehavioralCongruent admissible states σ φ ψ) :
    ∀ M ∈ states, ∀ I ∈ admissible,
      evalFormula (applySeq I M) σ φ = evalFormula (applySeq I M) σ ψ :=
  h_cong


-- ============================================================================
-- 6. "Panel Agreement Is Not Truth" & The Grounding Firewall
-- ============================================================================

/-- An observer equipped with a coarse projection capability. -/
structure Observer where
  id : Nat
  name : String
  project : RelModel → RelModel

/-- Observer vote on formula φ evaluated on its projected state. -/
def observerVote (obs : Observer) (M : RelModel) (σ : Nat → Nat) (φ : Formula) : TruthVal :=
  evalFormula (obs.project M) σ φ

/-- A multi-observer panel. -/
abbrev Panel := List Observer

/-- Unanimous consensus of a panel of size N ≥ 3. -/
def panelUnanimous (panel : Panel) (M : RelModel) (σ : Nat → Nat) (φ : Formula) (v : TruthVal) : Prop :=
  panel.length ≥ 3 ∧ ∀ obs ∈ panel, observerVote obs M σ φ = v

/-- Panel illusion: a panel unanimously certifies φ as true on coarse projections,
    yet an executable carrier intervention refutes φ to `zero`. -/
def PanelIllusion (panel : Panel) (M : RelModel) (σ : Nat → Nat) (φ : Formula) (I : InterventionSeq) : Prop :=
  panelUnanimous panel M σ φ TruthVal.one ∧
  evalFormula (applySeq I M) σ φ = TruthVal.zero

/-- Structured cryptographic receipt documenting an intercepted panel illusion. -/
structure PanelIllusionReceipt where
  formulaId : Nat
  panelSize : Nat
  panelConsensus : TruthVal
  groundVerdict : TruthVal
  refutingInterventionLength : Nat
  deriving DecidableEq, Repr

/-- StepResult distinguishing valid transition from state-preserving typed refusal. -/
inductive StepResult where
  | ok (nextState : RelModel)
  | refusal (reason : String) (receipt : PanelIllusionReceipt)

/-- Decidable check for panel consensus on TruthVal.one. -/
def checkPanelUnanimousOne (panel : Panel) (M : RelModel) (σ : Nat → Nat) (φ : Formula) : Bool :=
  panel.length ≥ 3 && panel.all (fun obs => observerVote obs M σ φ == TruthVal.one)

theorem checkPanelUnanimousOne_eq (panel : Panel) (M : RelModel) (σ : Nat → Nat) (φ : Formula) :
    checkPanelUnanimousOne panel M σ φ = true ↔
    panel.length ≥ 3 ∧ ∀ obs ∈ panel, observerVote obs M σ φ = TruthVal.one := by
  dsimp [checkPanelUnanimousOne]
  rw [Bool.and_eq_true, decide_eq_true_iff, List.all_eq_true]
  constructor
  · intro ⟨h_len, h_all⟩
    refine ⟨h_len, ?_⟩
    intro obs h_mem
    have h_b := h_all obs h_mem
    exact beq_iff_eq.mp h_b
  · intro ⟨h_len, h_all⟩
    refine ⟨h_len, ?_⟩
    intro obs h_mem
    have h_eq := h_all obs h_mem
    exact beq_iff_eq.mpr h_eq

/-- The Grounding Firewall: evaluates panel agreement against counterfactual intervention tests. -/
def groundingFirewall
    (panel : Panel) (M : RelModel) (σ : Nat → Nat) (φ : Formula) (formulaId : Nat)
    (candidateNext : RelModel) (testIntervention : InterventionSeq) : StepResult :=
  if checkPanelUnanimousOne panel M σ φ then
    if evalFormula (applySeq testIntervention M) σ φ == TruthVal.zero then
      StepResult.refusal
        "Grounding Firewall: Unanimous panel consensus refuted by carrier intervention"
        { formulaId := formulaId
          panelSize := panel.length
          panelConsensus := TruthVal.one
          groundVerdict := TruthVal.zero
          refutingInterventionLength := testIntervention.length }
    else
      StepResult.ok candidateNext
  else
    StepResult.ok candidateNext

/-- State transition execution enforcing state preservation under refusal. -/
def executeStep
    (panel : Panel) (current : RelModel) (σ : Nat → Nat) (φ : Formula) (formulaId : Nat)
    (candidateNext : RelModel) (testIntervention : InterventionSeq) : RelModel :=
  match groundingFirewall panel current σ φ formulaId candidateNext testIntervention with
  | .ok nextState => nextState
  | .refusal _ _ => current

/-- Theorem: "Panel agreement is not truth".
    There exist an operational carrier state M, assignment σ, formula φ, intervention I,
    and a panel of N = 3 observers such that the panel unanimously agrees that φ holds,
    yet the counterfactual carrier intervention refutes φ. -/
theorem panel_agreement_not_truth :
    ∃ (panel : Panel) (M : RelModel) (σ : Nat → Nat) (φ : Formula) (I : InterventionSeq),
      PanelIllusion panel M σ φ I := by
  let M : RelModel := {
    dataCount := 1
    relVal := fun _ _ => TruthVal.zero
  }
  let σ : Nat → Nat := fun _ => 0
  let φ : Formula := .atom 0 [Term.const 0]
  let coarseProj : RelModel → RelModel := fun m => {
    dataCount := m.dataCount
    relVal := fun r args => if r = 0 ∧ args = [0] then TruthVal.one else m.relVal r args
  }
  let obs1 : Observer := { id := 1, name := "obs1", project := coarseProj }
  let obs2 : Observer := { id := 2, name := "obs2", project := coarseProj }
  let obs3 : Observer := { id := 3, name := "obs3", project := coarseProj }
  refine ⟨[obs1, obs2, obs3], M, σ, φ, [], ?_⟩
  dsimp [PanelIllusion, panelUnanimous, observerVote, evalFormula, applySeq]
  constructor
  · constructor
    · decide
    · intro obs h_in
      match obs, h_in with
      | _, .head _ => decide
      | _, .tail _ (.head _) => decide
      | _, .tail _ (.tail _ (.head _)) => decide
  · rfl

/-- Theorem: The Grounding Firewall decisively refuses state mutation upon panel illusion. -/
theorem grounding_firewall_refuses_panel_illusion
    (panel : Panel) (M : RelModel) (σ : Nat → Nat) (φ : Formula) (fId : Nat)
    (candidateNext : RelModel) (I : InterventionSeq)
    (h_illusion : PanelIllusion panel M σ φ I) :
    ∃ reason receipt,
      groundingFirewall panel M σ φ fId candidateNext I = StepResult.refusal reason receipt := by
  dsimp [groundingFirewall]
  have h_pan := h_illusion.1
  have h_ref := h_illusion.2
  have h_check : checkPanelUnanimousOne panel M σ φ = true := by
    rw [checkPanelUnanimousOne_eq]
    exact h_pan
  have h_ref_b : (evalFormula (applySeq I M) σ φ == TruthVal.zero) = true := by
    rw [beq_iff_eq]
    exact h_ref
  rw [h_check]
  dsimp
  rw [h_ref_b]
  dsimp
  exact ⟨_, _, rfl⟩

/-- Theorem: State preservation under refusal.
    When a panel illusion is detected, the engine preserves the original carrier state unchanged. -/
theorem refusal_preserves_state
    (panel : Panel) (current : RelModel) (σ : Nat → Nat) (φ : Formula) (fId : Nat)
    (candidateNext : RelModel) (I : InterventionSeq)
    (h_illusion : PanelIllusion panel current σ φ I) :
    executeStep panel current σ φ fId candidateNext I = current := by
  dsimp [executeStep]
  have ⟨reason, receipt, h_res⟩ :=
    grounding_firewall_refuses_panel_illusion panel current σ φ fId candidateNext I h_illusion
  rw [h_res]

end X301FormalSemantics
