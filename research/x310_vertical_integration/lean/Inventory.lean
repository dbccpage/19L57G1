import VerticalIntegration

open X310VerticalIntegration

-- Core Mandatory Theorems
#print axioms end_to_end_commutation
#print axioms pipeline_preservation
#print axioms spacelike_non_signaling_preservation
#print axioms refusal_pipeline_preservation

-- Companion Commutation & Non-Signaling Theorems
#print axioms readout1_stepL2_commutation
#print axioms readout_stepM_commutation
#print axioms readout_replay_commutation
#print axioms codec_roundtrip_identity
#print axioms tvd_non_signaling_exact_zero
#print axioms readout1_readout2_comm

-- Companion Preservation & Soundness Theorems
#print axioms pipeline_result_state_on_refusal
#print axioms grounding_firewall_soundness
#print axioms farkas_duality_soundness
#print axioms tms_retract_preserves_axioms
#print axioms agency_viability_preservation

def main : IO Unit := do
  IO.println "Target X310 Vertical Integration Chain Lean 4 Census:"
  IO.println "  - end_to_end_commutation"
  IO.println "  - pipeline_preservation"
  IO.println "  - spacelike_non_signaling_preservation"
  IO.println "  - refusal_pipeline_preservation"
  IO.println "  - readout1_stepL2_commutation"
  IO.println "  - readout_stepM_commutation"
  IO.println "  - readout_replay_commutation"
  IO.println "  - codec_roundtrip_identity"
  IO.println "  - tvd_non_signaling_exact_zero"
  IO.println "  - readout1_readout2_comm"
  IO.println "  - pipeline_result_state_on_refusal"
  IO.println "  - grounding_firewall_soundness"
  IO.println "  - farkas_duality_soundness"
  IO.println "  - tms_retract_preserves_axioms"
  IO.println "  - agency_viability_preservation"
