import SecondSymmetry.Grow

/-!
# Each adding kind loses an automorphism somewhere and gains one somewhere

Native to rung five.  Six concrete regimes, each with an automorphism
given by its four maps and its membership conditions closed by kernel
computation over the concrete lists.  A LOSS is an automorphism of the
regime before that is not one after; a GAIN is an automorphism after
whose maps are not an automorphism before.  Each is closed through the
fixing theorems of `Meet.lean`: the exhibited maps move the added
element, so they cannot be common to both sides.  Nothing here counts an
automorphism set.

Every witness uses at most three data and at most two forms, all of
arity one.

AuthorityEffect: None.
-/

namespace SecondSymmetry
namespace Aut

open Sealed

/-- The swap of data one and two. -/
def swap12 (d : Nat) : Nat :=
  if d = 1 then 2 else if d = 2 then 1 else d

/-- The swap of data zero and two. -/
def swap02 (d : Nat) : Nat :=
  if d = 0 then 2 else if d = 2 then 0 else d

/-! ## Instances: two data, one unary form -/

def instLossR : Regime := ⟨2, [1], [], [], []⟩
def instGainR : Regime := ⟨2, [1], [(0, [0])], [], []⟩

/-- The swap of the two data is an automorphism of two data under one
unary form with no instance. -/
def instLossAut : Iso instLossR instLossR where
  dmap := swap01
  dinv := swap01
  fmap := id
  finv := id
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := by decide
  finv_lt := by decide
  finv_fmap := by decide
  fmap_finv := by decide
  arity := by decide
  insts_fwd := by decide
  insts_bwd := by decide
  rules_fwd := by decide
  rules_bwd := by decide
  reqs_fwd := by decide
  reqs_bwd := by decide

/-- After both data carry the unary form, the swap is an automorphism. -/
def instGainAut : Iso (addInst instGainR (0, [1])) (addInst instGainR (0, [1])) where
  dmap := swap01
  dinv := swap01
  fmap := id
  finv := id
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := by decide
  finv_lt := by decide
  finv_fmap := by decide
  fmap_finv := by decide
  arity := by decide
  insts_fwd := by decide
  insts_bwd := by decide
  rules_fwd := by decide
  rules_bwd := by decide
  reqs_fwd := by decide
  reqs_bwd := by decide

/-! ## Uniform rules: no data, two unary forms -/

def ruleLossR : Regime := ⟨0, [1, 1], [], [], []⟩
def ruleGainR : Regime := ⟨0, [1, 1], [], [0], []⟩

def ruleLossAut : Iso ruleLossR ruleLossR where
  dmap := id
  dinv := id
  fmap := swap01
  finv := swap01
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := by decide
  finv_lt := by decide
  finv_fmap := by decide
  fmap_finv := by decide
  arity := by decide
  insts_fwd := by decide
  insts_bwd := by decide
  rules_fwd := by decide
  rules_bwd := by decide
  reqs_fwd := by decide
  reqs_bwd := by decide

def ruleGainAut : Iso (addRule ruleGainR 1) (addRule ruleGainR 1) where
  dmap := id
  dinv := id
  fmap := swap01
  finv := swap01
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := by decide
  finv_lt := by decide
  finv_fmap := by decide
  fmap_finv := by decide
  arity := by decide
  insts_fwd := by decide
  insts_bwd := by decide
  rules_fwd := by decide
  rules_bwd := by decide
  reqs_fwd := by decide
  reqs_bwd := by decide

/-! ## Requirements: three data, no forms -/

def reqLossR : Regime := ⟨3, [], [], [], []⟩
def reqGainR : Regime := ⟨3, [], [], [], [(0, 1)]⟩

def reqLossAut : Iso reqLossR reqLossR where
  dmap := swap12
  dinv := swap12
  fmap := id
  finv := id
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := by decide
  finv_lt := by decide
  finv_fmap := by decide
  fmap_finv := by decide
  arity := by decide
  insts_fwd := by decide
  insts_bwd := by decide
  rules_fwd := by decide
  rules_bwd := by decide
  reqs_fwd := by decide
  reqs_bwd := by decide

def reqGainAut : Iso (addReq reqGainR (1, 2)) (addReq reqGainR (1, 2)) where
  dmap := swap02
  dinv := swap02
  fmap := id
  finv := id
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := by decide
  finv_lt := by decide
  finv_fmap := by decide
  fmap_finv := by decide
  arity := by decide
  insts_fwd := by decide
  insts_bwd := by decide
  rules_fwd := by decide
  rules_bwd := by decide
  reqs_fwd := by decide
  reqs_bwd := by decide

/-! ## The six witnesses -/

theorem inst_loss : ¬ Survives instLossAut (addInst instLossR (0, [0])) := by
  intro ⟨τ, hs⟩
  have h := inst_fixed_of_survives (e := (0, [0])) (by decide) (by decide)
    (by decide) instLossAut τ hs
  exact absurd h (by decide)

theorem inst_gain : ¬ ∃ σ : Iso instGainR instGainR, SameMaps instGainAut σ := by
  intro ⟨σ, hs⟩
  have h := inst_fixed_of_survives (e := (0, [1])) (by decide) (by decide)
    (by decide) σ instGainAut (sameMaps_symm hs)
  unfold instImage at h
  rw [← hs.1, ← hs.2.2.1] at h
  exact absurd h (by decide)

theorem rule_loss : ¬ Survives ruleLossAut (addRule ruleLossR 0) := by
  intro ⟨τ, hs⟩
  have h := rule_fixed_of_survives (e := 0) (by decide) (by decide)
    ruleLossAut τ hs
  exact absurd h (by decide)

theorem rule_gain : ¬ ∃ σ : Iso ruleGainR ruleGainR, SameMaps ruleGainAut σ := by
  intro ⟨σ, hs⟩
  have h := rule_fixed_of_survives (e := 1) (by decide) (by decide)
    σ ruleGainAut (sameMaps_symm hs)
  rw [← hs.2.2.1] at h
  exact absurd h (by decide)

theorem req_loss : ¬ Survives reqLossAut (addReq reqLossR (0, 1)) := by
  intro ⟨τ, hs⟩
  have h := req_fixed_of_survives (e := (0, 1)) (by decide) (by decide)
    (by decide) reqLossAut τ hs
  exact absurd h (by decide)

theorem req_gain : ¬ ∃ σ : Iso reqGainR reqGainR, SameMaps reqGainAut σ := by
  intro ⟨σ, hs⟩
  have h := req_fixed_of_survives (e := (1, 2)) (by decide) (by decide)
    (by decide) σ reqGainAut (sameMaps_symm hs)
  unfold reqImage at h
  rw [← hs.1] at h
  exact absurd h (by decide)

/-- Each of the three adding kinds loses an automorphism at some regime
and gains one at some regime. -/
theorem kinds_move_both_ways :
    (∃ (r : Regime) (e : Inst) (σ : Iso r r), ¬ Survives σ (addInst r e)) ∧
    (∃ (r : Regime) (e : Inst) (τ : Iso (addInst r e) (addInst r e)),
      ¬ ∃ σ : Iso r r, SameMaps τ σ) ∧
    (∃ (r : Regime) (f : Nat) (σ : Iso r r), ¬ Survives σ (addRule r f)) ∧
    (∃ (r : Regime) (f : Nat) (τ : Iso (addRule r f) (addRule r f)),
      ¬ ∃ σ : Iso r r, SameMaps τ σ) ∧
    (∃ (r : Regime) (q : Nat × Nat) (σ : Iso r r), ¬ Survives σ (addReq r q)) ∧
    (∃ (r : Regime) (q : Nat × Nat) (τ : Iso (addReq r q) (addReq r q)),
      ¬ ∃ σ : Iso r r, SameMaps τ σ) :=
  ⟨⟨_, _, _, inst_loss⟩, ⟨_, _, _, inst_gain⟩,
   ⟨_, _, _, rule_loss⟩, ⟨_, _, _, rule_gain⟩,
   ⟨_, _, _, req_loss⟩, ⟨_, _, _, req_gain⟩⟩

end Aut
end SecondSymmetry
