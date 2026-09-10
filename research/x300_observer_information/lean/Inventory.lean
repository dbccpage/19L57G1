import ObserverInformation

open X300ObserverInformation

#print axioms channel_compose_assoc
#print axioms channel_compose_id_left
#print axioms channel_compose_id_right
#print axioms post_processing_coarse_graining
#print axioms dpi_distinguishability
#print axioms dpi_mutual_distinction
#print axioms dpi_decodability
#print axioms invertible_postprocessing_preserves_distinctions
#print axioms hartley_capacity_additive
#print axioms state_space_multiplicative
#print axioms coarse_graining_capacity_monotonic
#print axioms uniform_1bit_scaled_entropy
#print axioms uniform_2bit_scaled_entropy
#print axioms memory_retention_monotone
#print axioms erasure_collapses_states
#print axioms erasure_strictly_non_reversible
#print axioms erasure_image_singleton

def main : IO Unit := do
  IO.println "Target X300 Observer-Relative Information Lean 4 Census:"
  IO.println "  - channel_compose_assoc"
  IO.println "  - channel_compose_id_left"
  IO.println "  - channel_compose_id_right"
  IO.println "  - post_processing_coarse_graining"
  IO.println "  - dpi_distinguishability"
  IO.println "  - dpi_mutual_distinction"
  IO.println "  - dpi_decodability"
  IO.println "  - invertible_postprocessing_preserves_distinctions"
  IO.println "  - hartley_capacity_additive"
  IO.println "  - state_space_multiplicative"
  IO.println "  - coarse_graining_capacity_monotonic"
  IO.println "  - uniform_1bit_scaled_entropy"
  IO.println "  - uniform_2bit_scaled_entropy"
  IO.println "  - memory_retention_monotone"
  IO.println "  - erasure_collapses_states"
  IO.println "  - erasure_strictly_non_reversible"
  IO.println "  - erasure_image_singleton"
