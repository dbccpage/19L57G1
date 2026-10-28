import Derivation.Bridge
-- the off-diagonal hypothesis of no_swap_fixed_offdiag_pair is not needed: the swap has no fixed point on Bool × Bool
example : ∀ x y : Bool, (Bool.not x, Bool.not y) ≠ (x, y) := by decide
#print axioms Bridge.exists_not_of_not_ball
#check @Bridge.second_token_required
#eval Derivation.replayT Bridge.hist01 ⟨[], [], [], [], []⟩
#eval Derivation.replayT Bridge.hist10 ⟨[], [], [], [], []⟩
