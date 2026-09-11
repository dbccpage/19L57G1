import FormalSemantics

open X301FormalSemantics

-- Poset & Heyting Truth Structure Theorems
#print axioms truth_val_le_refl
#print axioms truth_val_le_trans
#print axioms truth_val_le_antisymm
#print axioms truth_val_meet_comm
#print axioms truth_val_meet_assoc
#print axioms truth_val_join_comm
#print axioms truth_val_join_assoc
#print axioms heyting_imp_self
#print axioms heyting_modus_ponens
#print axioms heyting_neg_refusal
#print axioms constructive_non_contradiction
#print axioms constructive_lem_fails

-- Compositional Semantics & Satisfaction
#print axioms meet_eq_one_iff
#print axioms join_eq_one_of_left
#print axioms join_eq_one_of_right
#print axioms neg_eq_one_iff
#print axioms satisfaction_compositional_conj
#print axioms satisfaction_compositional_disj
#print axioms satisfaction_compositional_neg
#print axioms satisfaction_modus_ponens
#print axioms satisfaction_refuses_contradiction

-- Canonical Isomorphism & Semantic Truth Invariance
#print axioms iso_data_inj
#print axioms translation_commutes_term
#print axioms extendAssign_comm_transport
#print axioms foldMeetDom_comm_transport
#print axioms foldJoinDom_comm_transport
#print axioms translation_commutes_formula
#print axioms translation_commutes_satisfaction

-- Interventions & Empirical Reference
#print axioms intervention_apply_empty
#print axioms intervention_discriminates_reference
#print axioms empty_intervention_cannot_discriminate

-- Behavioral Observational Congruence
#print axioms behavioral_congruence_refl
#print axioms behavioral_congruence_symm
#print axioms behavioral_congruence_trans
#print axioms decorative_distinction_rejected

-- Multi-Observer Panels & Grounding Firewall
#print axioms checkPanelUnanimousOne_eq
#print axioms panel_agreement_not_truth
#print axioms grounding_firewall_refuses_panel_illusion
#print axioms refusal_preserves_state

def main : IO Unit := do
  IO.println "Target X301 Formal Semantics Lean 4 Census:"
  IO.println "  - truth_val_le_refl"
  IO.println "  - truth_val_le_trans"
  IO.println "  - truth_val_le_antisymm"
  IO.println "  - truth_val_meet_comm"
  IO.println "  - truth_val_meet_assoc"
  IO.println "  - truth_val_join_comm"
  IO.println "  - truth_val_join_assoc"
  IO.println "  - heyting_imp_self"
  IO.println "  - heyting_modus_ponens"
  IO.println "  - heyting_neg_refusal"
  IO.println "  - constructive_non_contradiction"
  IO.println "  - constructive_lem_fails"
  IO.println "  - meet_eq_one_iff"
  IO.println "  - join_eq_one_of_left"
  IO.println "  - join_eq_one_of_right"
  IO.println "  - neg_eq_one_iff"
  IO.println "  - satisfaction_compositional_conj"
  IO.println "  - satisfaction_compositional_disj"
  IO.println "  - satisfaction_compositional_neg"
  IO.println "  - satisfaction_modus_ponens"
  IO.println "  - satisfaction_refuses_contradiction"
  IO.println "  - iso_data_inj"
  IO.println "  - translation_commutes_term"
  IO.println "  - extendAssign_comm_transport"
  IO.println "  - foldMeetDom_comm_transport"
  IO.println "  - foldJoinDom_comm_transport"
  IO.println "  - translation_commutes_formula"
  IO.println "  - translation_commutes_satisfaction"
  IO.println "  - intervention_apply_empty"
  IO.println "  - intervention_discriminates_reference"
  IO.println "  - empty_intervention_cannot_discriminate"
  IO.println "  - behavioral_congruence_refl"
  IO.println "  - behavioral_congruence_symm"
  IO.println "  - behavioral_congruence_trans"
  IO.println "  - decorative_distinction_rejected"
  IO.println "  - checkPanelUnanimousOne_eq"
  IO.println "  - panel_agreement_not_truth"
  IO.println "  - grounding_firewall_refuses_panel_illusion"
  IO.println "  - refusal_preserves_state"
