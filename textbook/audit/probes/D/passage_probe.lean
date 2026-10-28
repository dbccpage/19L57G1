import Derivation.PrimitivePassage
open PrimitivePassage
-- the two helper steps not in the artifact
#print axioms PrimitivePassage.asserted_offdiag_step
#print axioms PrimitivePassage.retained_sub_asserted_step
-- the induced setting's carrier is all of Nat, not the occurrence list
example : (inducedSetting preRetained 0 1).X = Nat := rfl
-- no_outside_operational and replay_deterministic are congruences
example (s t : PState) (e : PEvent) (h : s = t) : step s e = step t e := congrArg (fun x => step x e) h
example (h1 h2 : List PEvent) (h : h1 = h2) : replayP h1 genesisP = replayP h2 genesisP := congrArg (fun x => replayP x genesisP) h
-- quotient_no_recovery holds for every binary g by substitution
example {X Q : Type} (q : X → Q) (a b : X) (hq : q a = q b) (g : Q → Q → Prop) : g (q a) (q b) ↔ g (q a) (q a) := by rw [hq]
-- extension_always_available: hprot is derivable from hobst
example (s : PState) (i j : Nat) (h : obstP s i j = true) : (i, j) ∈ s.prot := by
  have := (gates_of_obst s i j h).2.1
  unfold protectedP at this
  exact of_decide_eq_true this
