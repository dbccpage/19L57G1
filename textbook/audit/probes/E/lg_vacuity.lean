import Derivation.LadderGeneral
open LadderGeneral

-- Signless boundary: replace sgn by the constant 1.
def bdN1 (σ : List Nat) : List (Int × List Nat) :=
  (List.range σ.length).map (fun i => ((1 : Int), σ.eraseIdx i))
def pushN1 (ch : List (Int × List Nat)) : List (Int × List Nat) :=
  ch.flatMap (fun p => (bdN1 p.2).map (fun q => (p.1 * q.1, q.2)))

-- The first two conjuncts of d2_zero_dims_2_3_4 with the WRONG (signless)
-- calculus: if they still decide to true, they are vacuous.
example :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => coeffN e (pushN1 (bdN1 t)) == 0) = true := by decide
example :
    ((combs 5 3).all fun q =>
      (facets q).all fun t2 => coeffN t2 (pushN1 (bdN1 q)) == 0) = true := by decide
-- The genuine codim-2 check with signless calculus FAILS (so it is not vacuous):
example :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => (facets e).all fun v =>
        coeffN v (pushN1 (bdN1 t)) == 0) = false := by decide
-- And the third conjunct, signless, also fails:
set_option maxRecDepth 4096 in
example :
    ((facets [0, 1, 2, 3, 4]).all fun q =>
      (facets q).all fun t2 => coeffN t2 (pushN1 (bdN1 [0, 1, 2, 3, 4])) == 0) = false := by decide
-- Direct: the support of the composite chain of a triangle is 1-element lists only.
example : (pushN (bdN [0,1,2])).map (·.2) = [[2],[1],[2],[0],[1],[0]] := by decide
