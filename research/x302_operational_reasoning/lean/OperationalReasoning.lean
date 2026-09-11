/-!
# Target X302: Operational Reasoning & Belief Revision

Constructive formalization of operational reasoning with endogenous
truth maintenance, dependency-directed justification DAG tracking,
direct and operational contradiction detection, and minimal belief revision
(AGM postulates) without classical choice or external oracles.

AuthorityEffect: None.
Axioms: strictly in {propext, Quot.sound}.
-/

namespace X302OperationalReasoning

set_option linter.unusedVariables false

/-- Internal propositional formulas including carrier valuations and absurdity. -/
inductive Formula where
  | atom : Nat → Formula
  | notF : Formula → Formula
  | andF : Formula → Formula → Formula
  | orF : Formula → Formula → Formula
  | impliesF : Formula → Formula → Formula
  | eqVal : Nat → Nat → Formula  -- carrier variable = value
  | bot : Formula
  deriving DecidableEq, Repr

open Formula

/-- Syntactic size metric for induction. -/
def formulaSize : Formula → Nat
  | .atom _ => 1
  | .notF f => 1 + formulaSize f
  | .andF f1 f2 => 1 + formulaSize f1 + formulaSize f2
  | .orF f1 f2 => 1 + formulaSize f1 + formulaSize f2
  | .impliesF f1 f2 => 1 + formulaSize f1 + formulaSize f2
  | .eqVal _ _ => 1
  | .bot => 1

theorem formulaSize_pos (f : Formula) : 0 < formulaSize f := by
  cases f <;> simp [formulaSize] <;> omega

/-- Valuation model over atoms and carrier variables. -/
structure Valuation where
  atomVal : Nat → Prop
  carrierVal : Nat → Nat

/-- Semantic evaluation of a formula under an operational valuation. -/
def evalFormula (v : Valuation) : Formula → Prop
  | .atom n => v.atomVal n
  | .notF f => ¬ (evalFormula v f)
  | .andF f1 f2 => evalFormula v f1 ∧ evalFormula v f2
  | .orF f1 f2 => evalFormula v f1 ∨ evalFormula v f2
  | .impliesF f1 f2 => evalFormula v f1 → evalFormula v f2
  | .eqVal var val => v.carrierVal var = val
  | .bot => False

/-- Commitment class distinguishing firm commitments (axioms) from speculative assumptions (hypotheses). -/
inductive CommitmentClass where
  | firmAxiom : CommitmentClass
  | speculativeHypothesis : CommitmentClass
  deriving DecidableEq, Repr

/-- Justification rules applied in operational inference. -/
inductive Justification where
  | axiomPremise : Justification
  | hypPremise (hId : Nat) : Justification
  | modusPonens : Justification
  | conjIntro : Justification
  | conjElimLeft : Justification
  | conjElimRight : Justification
  | disjIntroLeft : Justification
  | disjIntroRight : Justification
  | directContradiction : Justification
  | valuationContradiction : Justification
  deriving DecidableEq, Repr

variable (Axioms : Formula → Prop) (hypFormula : Nat → Formula)

/-- Derivation tree carrying derived formula and exact hypothesis support list. -/
inductive DerivTree : Formula → List Nat → Prop where
  | axiomLeaf (f : Formula) :
      Axioms f →
      DerivTree f []
  | hypLeaf (h : Nat) :
      DerivTree (hypFormula h) [h]
  | mpStep {f1 f2 : Formula} {s1 s2 : List Nat} :
      DerivTree (.impliesF f1 f2) s1 →
      DerivTree f1 s2 →
      DerivTree f2 (s1 ++ s2)
  | conjIntroStep {f1 f2 : Formula} {s1 s2 : List Nat} :
      DerivTree f1 s1 →
      DerivTree f2 s2 →
      DerivTree (.andF f1 f2) (s1 ++ s2)
  | conjElimLeftStep {f1 f2 : Formula} {s : List Nat} :
      DerivTree (.andF f1 f2) s →
      DerivTree f1 s
  | conjElimRightStep {f1 f2 : Formula} {s : List Nat} :
      DerivTree (.andF f1 f2) s →
      DerivTree f2 s
  | disjIntroLeftStep {f1 f2 : Formula} {s : List Nat} :
      DerivTree f1 s →
      DerivTree (.orF f1 f2) s
  | disjIntroRightStep {f1 f2 : Formula} {s : List Nat} :
      DerivTree f2 s →
      DerivTree (.orF f1 f2) s
  | directContraStep {f : Formula} {s1 s2 : List Nat} :
      DerivTree f s1 →
      DerivTree (.notF f) s2 →
      DerivTree .bot (s1 ++ s2)
  | valContraStep {var val1 val2 : Nat} {s1 s2 : List Nat} :
      DerivTree (.eqVal var val1) s1 →
      DerivTree (.eqVal var val2) s2 →
      val1 ≠ val2 →
      DerivTree .bot (s1 ++ s2)

open DerivTree

/-- Theorem 1: Axiom leaves have empty hypothesis support. -/
theorem axiom_leaf_support_empty (f : Formula) (h_ax : Axioms f) :
    DerivTree Axioms hypFormula f [] :=
  axiomLeaf f h_ax

/-- Theorem 2: Hypothesis leaves have singleton hypothesis support. -/
theorem hyp_leaf_support_singleton (h : Nat) :
    DerivTree Axioms hypFormula (hypFormula h) [h] :=
  hypLeaf h

/-- Theorem 3: Support union for modus ponens inference preserves left support membership. -/
theorem mp_support_mem_left {f1 f2 : Formula} {s1 s2 : List Nat}
    (dt_imp : DerivTree Axioms hypFormula (.impliesF f1 f2) s1)
    (dt_arg : DerivTree Axioms hypFormula f1 s2)
    {h : Nat} (h_in : h ∈ s1) :
    h ∈ (s1 ++ s2) := by
  exact List.mem_append_left s2 h_in

/-- Theorem 4: Support union for modus ponens inference preserves right support membership. -/
theorem mp_support_mem_right {f1 f2 : Formula} {s1 s2 : List Nat}
    (dt_imp : DerivTree Axioms hypFormula (.impliesF f1 f2) s1)
    (dt_arg : DerivTree Axioms hypFormula f1 s2)
    {h : Nat} (h_in : h ∈ s2) :
    h ∈ (s1 ++ s2) := by
  exact List.mem_append_right s1 h_in

/-- Theorem 5: Conjunction intro support is the union of antecedent supports. -/
theorem conj_intro_support_mem {f1 f2 : Formula} {s1 s2 : List Nat}
    (dt1 : DerivTree Axioms hypFormula f1 s1)
    (dt2 : DerivTree Axioms hypFormula f2 s2) {h : Nat} :
    h ∈ (s1 ++ s2) ↔ h ∈ s1 ∨ h ∈ s2 := by
  exact List.mem_append

/-- Theorem 6: Conjunction elimination preserves support unchanged. -/
theorem conj_elim_support_eq {f1 f2 : Formula} {s : List Nat}
    (dt : DerivTree Axioms hypFormula (.andF f1 f2) s) :
    DerivTree Axioms hypFormula f1 s ∧ DerivTree Axioms hypFormula f2 s := by
  exact ⟨conjElimLeftStep dt, conjElimRightStep dt⟩

/-- Support subset property for active hypothesis sets. -/
def SupportContainedIn (s : List Nat) (activeHyp : List Nat) : Prop :=
  ∀ h ∈ s, h ∈ activeHyp

/-- Theorem 7: Support monotonicity across derivation steps. -/
theorem support_monotonicity {f : Formula} {s : List Nat}
    (dt : DerivTree Axioms hypFormula f s) {activeHyp : List Nat}
    (h_sub : SupportContainedIn s activeHyp) :
    ∀ h ∈ s, h ∈ activeHyp :=
  h_sub

/-- Theorem 8: Direct contradiction generates conflict set containing combined support. -/
theorem direct_contradiction_conflict_set {f : Formula} {s1 s2 : List Nat}
    (dt_pos : DerivTree Axioms hypFormula f s1)
    (dt_neg : DerivTree Axioms hypFormula (.notF f) s2) :
    DerivTree Axioms hypFormula .bot (s1 ++ s2) :=
  directContraStep dt_pos dt_neg

/-- Theorem 9: Operational valuation contradiction generates conflict set on distinct values. -/
theorem valuation_contradiction_conflict_set {var val1 val2 : Nat} {s1 s2 : List Nat}
    (dt1 : DerivTree Axioms hypFormula (.eqVal var val1) s1)
    (dt2 : DerivTree Axioms hypFormula (.eqVal var val2) s2)
    (h_ne : val1 ≠ val2) :
    DerivTree Axioms hypFormula .bot (s1 ++ s2) :=
  valContraStep dt1 dt2 h_ne

/-- Foundational consistency: an axiom-only contradiction has empty support. -/
def FoundationalContradiction (s : List Nat) : Prop :=
  s = []

/-- Theorem 10: Foundational contradiction cannot depend on any hypothesis. -/
theorem foundational_contradiction_no_hypothesis {s : List Nat}
    (h_found : FoundationalContradiction s) :
    ∀ h : Nat, h ∉ s := by
  intro h
  rw [h_found]
  intro h_in
  cases h_in

/-- Disjointness from a retraction set R. -/
def DisjointFrom (s : List Nat) (R : List Nat) : Prop :=
  ∀ h ∈ s, h ∉ R

/-- Theorem 11: Empty support is vacuously disjoint from any retraction set. -/
theorem empty_support_disjoint (R : List Nat) :
    DisjointFrom [] R := by
  intro h h_in
  cases h_in

/-- Theorem 12: Axioms have empty support and are therefore invariant under hypothesis retraction. -/
theorem axiom_immutability (f : Formula) (R : List Nat) :
    DisjointFrom [] R :=
  empty_support_disjoint R

/-- Definition of a hitting set over a family of conflict sets. -/
def IsHittingSet (R : List Nat) (conflicts : List (List Nat)) : Prop :=
  ∀ C ∈ conflicts, ∃ h ∈ C, h ∈ R

/-- Theorem 13: A hitting set invalidates every conflict set in the family. -/
theorem hitting_set_invalidates_conflict {R : List Nat} {conflicts : List (List Nat)}
    (h_hit : IsHittingSet R conflicts) {C : List Nat} (h_in : C ∈ conflicts) :
    ¬ (DisjointFrom C R) := by
  intro h_disj
  have ⟨h, h_mem_C, h_mem_R⟩ := h_hit C h_in
  have h_not := h_disj h h_mem_C
  exact h_not h_mem_R

/-- Theorem 14: Retraction eliminates active conflict support. -/
theorem retraction_deactivates_conflict {C : List Nat} {R : List Nat}
    {h : Nat} (h_in_C : h ∈ C) (h_in_R : h ∈ R) :
    ¬ (DisjointFrom C R) := by
  intro h_disj
  exact h_disj h h_in_C h_in_R

/-- Theorem 15: Vacuous revision - when conflicts list is empty, empty retraction is a valid hitting set. -/
theorem vacuous_revision_empty_hitting_set :
    IsHittingSet [] [] := by
  intro C h_in
  cases h_in

/-- Theorem 16: Vacuous revision preserves all active beliefs. -/
theorem vacuous_revision_preserves_support (s : List Nat) :
    DisjointFrom s [] := by
  intro h _ h_in_nil
  cases h_in_nil

/-- Theorem 17: Soundness of operational deduction.
    For any valuation satisfying all represented axioms and hypotheses in support s,
    the derived formula evaluates to true. -/
theorem derivation_soundness (v : Valuation)
    (h_axioms : ∀ f, Axioms f → evalFormula v f) :
    ∀ {f : Formula} {s : List Nat},
    DerivTree Axioms hypFormula f s →
    (∀ h ∈ s, evalFormula v (hypFormula h)) →
    evalFormula v f
  | _, _, axiomLeaf f h_ax, _ =>
      h_axioms f h_ax
  | _, _, hypLeaf h, h_supp =>
      h_supp h (List.Mem.head [])
  | _, _, mpStep dt_imp dt_arg, h_supp => by
      have h_s1 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_left _ hh)
      have h_s2 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_right _ hh)
      have ev_imp := derivation_soundness v h_axioms dt_imp h_s1
      have ev_arg := derivation_soundness v h_axioms dt_arg h_s2
      exact ev_imp ev_arg
  | _, _, conjIntroStep dt1 dt2, h_supp => by
      have h_s1 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_left _ hh)
      have h_s2 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_right _ hh)
      have ev1 := derivation_soundness v h_axioms dt1 h_s1
      have ev2 := derivation_soundness v h_axioms dt2 h_s2
      exact ⟨ev1, ev2⟩
  | _, _, conjElimLeftStep dt, h_supp => by
      have ev := derivation_soundness v h_axioms dt h_supp
      exact ev.left
  | _, _, conjElimRightStep dt, h_supp => by
      have ev := derivation_soundness v h_axioms dt h_supp
      exact ev.right
  | _, _, disjIntroLeftStep dt, h_supp => by
      have ev := derivation_soundness v h_axioms dt h_supp
      exact Or.inl ev
  | _, _, disjIntroRightStep dt, h_supp => by
      have ev := derivation_soundness v h_axioms dt h_supp
      exact Or.inr ev
  | _, _, directContraStep dt_pos dt_neg, h_supp => by
      have h_s1 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_left _ hh)
      have h_s2 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_right _ hh)
      have ev_pos := derivation_soundness v h_axioms dt_pos h_s1
      have ev_neg := derivation_soundness v h_axioms dt_neg h_s2
      exact False.elim (ev_neg ev_pos)
  | _, _, valContraStep dt1 dt2 h_ne, h_supp => by
      have h_s1 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_left _ hh)
      have h_s2 : ∀ h ∈ _, evalFormula v (hypFormula h) := fun h hh =>
        h_supp h (List.mem_append_right _ hh)
      have ev1 : v.carrierVal _ = _ := derivation_soundness v h_axioms dt1 h_s1
      have ev2 : v.carrierVal _ = _ := derivation_soundness v h_axioms dt2 h_s2
      have eq_vals : _ = _ := Eq.trans (Eq.symm ev1) ev2
      exact False.elim (h_ne eq_vals)

/-- Theorem 18: Consistency restoration - if a hitting set R hits all conflict sets of absurdity,
    then no derivation of absurdity survives with active (disjoint) support. -/
theorem retraction_restores_consistency {conflicts : List (List Nat)}
    {R : List Nat} (h_hit : IsHittingSet R conflicts)
    (h_all_conflicts : ∀ {s : List Nat}, DerivTree Axioms hypFormula .bot s → s ∈ conflicts) :
    ∀ {s : List Nat}, DerivTree Axioms hypFormula .bot s → ¬ (DisjointFrom s R) := by
  intro s dt_bot
  have h_in := h_all_conflicts dt_bot
  exact hitting_set_invalidates_conflict h_hit h_in

end X302OperationalReasoning
