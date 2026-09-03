import FreshCharacters.Balance

/-!
# The layer's own steps, reconstructed verbatim

PIN NOTE.  `repAdd`, `mod_idem`, `repAdd_val` and `repAdd_rot_zero` below are
reproduced verbatim from
`research/natural_sections/lean/NaturalSections/SlotExchange.lean`
at blob `f4f71ddd7197c2e40cf83e0347a76fa22abbaea0` (snapshot
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`, pinned in
`SOURCE_MANIFEST.json`), lines 41-66.  The one change is the outer namespace,
`FreshCharacters` in place of the sibling's.  Nothing in this file is claimed
as original: these are CONDITIONAL_THEOREM citations into the pinned packet,
compiled here so that this tree's characters are stated against the step
action the sibling already defined.  AuthorityEffect: None.

`repAdd_val` is the reason this file is here: the layer's own step action,
read on values, is multiplication of the member by the step, taken in the
part count.  Every character below is built on that and on nothing else.
-/

namespace FreshCharacters
namespace Steps

/-- `m` iterated additions of `c` in `Fin (k+1)`. -/
def repAdd {k : Nat} : Nat → Fin (k + 1) → Fin (k + 1)
  | 0, _ => 0
  | m + 1, c => c + repAdd m c

/-- Reduction of a double remainder, self-contained on positivity. -/
theorem mod_idem (a n : Nat) (hn : 0 < n) : a % n % n = a % n :=
  Nat.mod_eq_of_lt (Nat.mod_lt a hn)

theorem repAdd_val {k : Nat} (m : Nat) (c : Fin (k + 1)) :
    (repAdd m c).val = m * c.val % (k + 1) := by
  induction m with
  | zero => simp [repAdd]
  | succ n ih =>
    show ((c + repAdd n c) : Fin (k + 1)).val = (n + 1) * c.val % (k + 1)
    rw [Fin.val_add, ih, Nat.succ_mul]
    rw [Nat.add_mod, mod_idem (n * c.val) (k + 1) (Nat.succ_pos k)]
    rw [← Nat.add_mod, Nat.add_comm (n * c.val) c.val]

/-- SX1: every value is admissible for the rotation generator -- the
`k+1`-fold iterate of any `c : Fin (k+1)` is zero. -/
theorem repAdd_rot_zero {k : Nat} (c : Fin (k + 1)) :
    repAdd (k + 1) c = 0 := by
  apply Fin.ext
  rw [repAdd_val, Fin.val_zero, Nat.mul_comm, Nat.mul_mod_left]

end Steps
end FreshCharacters
