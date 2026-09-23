namespace ResearchEvidenceGraph

inductive DependencyPath (rank : Nat → Nat) : Nat → Nat → Prop where
  | edge {a b : Nat} : rank b < rank a → DependencyPath rank a b
  | step {a b c : Nat} : rank b < rank a → DependencyPath rank b c → DependencyPath rank a c

theorem rank_decreases {rank : Nat → Nat} {a b : Nat}
    (path : DependencyPath rank a b) : rank b < rank a := by
  induction path with
  | edge h => exact h
  | step h _ ih => exact Nat.lt_trans ih h

theorem no_self_dependency (rank : Nat → Nat) (a : Nat) :
    ¬ DependencyPath rank a a := by
  intro h
  exact Nat.lt_irrefl (rank a) (rank_decreases h)

end ResearchEvidenceGraph
