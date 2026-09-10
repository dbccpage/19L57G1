import Init

namespace ClaimExample

/-- An explicitly typed proposition, not unrestricted natural-language prose. -/
inductive State (P : Prop) where
  | certified (proof : P)
  | conjecture
  | refused

def checked (P : Prop) [Decidable P] : State P :=
  if h : P then .certified h else .refused

def isCertified {P : Prop} : State P → Bool
  | .certified _ => true
  | _ => false

theorem certified_has_proof {P : Prop} (s : State P) (h : isCertified s = true) : P := by
  cases s with
  | certified proof => exact proof
  | conjecture => cases h
  | refused => cases h

theorem false_refused : isCertified (checked (1 = 2)) = false := by decide
theorem true_certified : isCertified (checked (1 + 1 = 2)) = true := by decide
theorem conjecture_not_certified (P : Prop) : isCertified (State.conjecture (P := P)) = false := rfl

end ClaimExample
