import Derivation.StableContent
open PrimitivePassage StableContent

-- A genesis-reachable halted state carrying an unprotected separated pair.
def hist : List PEvent :=
  [.admitOcc 0, .admitOcc 1, .admitOcc 2, .assertWit 1 2, .admitWit 1 2,
   .protect 1 2, .declareObs, .setBudget 1, .addCol [1], .halt]

example : (replayP hist genesisP).obs = some [[1]] ∧
    (replayP hist genesisP).prot = [(1, 2)] ∧
    (replayP hist genesisP).halted = true ∧
    protSep (replayP hist genesisP) 0 1 = false ∧
    sepP [[1]] 0 1 = true := by decide

-- hence TraceStableSep holds there by replay_halted
example : TraceStableSep (replayP hist genesisP) 0 1 := by
  intro tr
  rw [replay_halted tr _ (by decide)]
  exact ⟨[[1]], by decide, by decide⟩

-- the module's own witness is NOT of this form: prot = [] with a nonempty column.
#eval sHalt.prot
#eval sHalt.obs
#print axioms StableContent.halted_stable_not_protected
#print axioms TraceAlgebra.rewrite_not_complete
#print axioms WeightProfile.descent_iff_subsingleton_support
