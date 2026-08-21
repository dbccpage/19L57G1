import Derivation.PrimDiff

/-!
# Rung 4: does it exist?  The pointed invariant, and the new residual

POST-SEAL extension experiment artifact.  Imports `Derivation.PrimDiff`
unmodified; read-only proof receipt via `lake env lean`.  Derived from the
sealed layer; no new primitive/parameter/menu/policy/oracle introduced to make
progress.  The one admitted datum — a marked carrier point — is the *priced
import already charged at rung 3* (the symmetry-breaking name); rung 4 studies
the structure that lift produces.

## The reconciliation

Rung 3 proved: no isomorphism-invariant separates `D2` from `D2rev`, because they
are isomorphic (the swap).  Resolution required admitting a symmetry-breaking
observable (a carrier-point name).  That admission is the **up-functor lift**:
pass from bare relations to *pointed* relations `(r, m)`.

Rung 4 asks whether an invariant exists on the enriched structure.  It does
(`markIsSource_separates`, `markIsSource_swap_invariant`): the intrinsic pointed
invariant "the mark is a pure source" separates `(D2, •)` from `(D2rev, •)` and
is genuinely invariant (moving the mark with the relation preserves it) — unlike
rung 3's `readsFwd`.  So **rung 4 exists and resolves the sign gap**, confirming
that an invariant is available at the up-functor junction.

But it is not free: the resolution is CONDITIONAL on the admitted mark, and it
produces a NEW residual — the CHOICE of mark, `(D2, false)` vs `(D2rev, true)`,
which the swap identifies (`mark_choice_residual`).  So the tower does not
terminate: it alternates [invariant resolves → sign residual → iso-blind → pay
to name → invariant resolves …], with an invariant at every junction and a fresh
residual after every resolution.
-/

namespace PrimDiff
namespace Rung4

/-! ## The pointed invariant -/

/-- The intrinsic pointed invariant: the marked point is a *pure source* — it has
an outgoing edge and no incoming edge.  Defined only from `r` and `m`, with no
label constants, so it is preserved by every pointed isomorphism. -/
def markIsSource (r : Bool → Bool → Prop) (m : Bool) : Prop :=
  (∃ y, r m y) ∧ ¬ (∃ x, r x m)

/-- **Rung 4 resolves the sign gap.**  With the mark fixed at `false`, the pointed
invariant separates `D2` (mark is a source) from `D2rev` (mark is not). -/
theorem markIsSource_separates :
    markIsSource D2 false ∧ ¬ markIsSource D2rev false := by
  refine ⟨⟨⟨true, ?_⟩, ?_⟩, ?_⟩
  · decide
  · rintro ⟨x, hx⟩; cases x <;> exact absurd hx (by decide)
  · rintro ⟨⟨y, hy⟩, _⟩; cases y <;> exact absurd hy (by decide)

theorem markIsSource_D2rev_true : markIsSource D2rev true := by
  refine ⟨⟨false, ?_⟩, ?_⟩
  · decide
  · rintro ⟨x, hx⟩; cases x <;> exact absurd hx (by decide)

/-- The swap carries `D2` to `D2rev` (re-proved locally). -/
theorem D2rev_iso_D2 : ∀ x y, D2rev x y ↔ D2 (Bool.not x) (Bool.not y) := by decide

/-! ## markIsSource is a genuine pointed invariant -/

/-- Reindexing existentials along the swap (an involution). -/
theorem exists_swap {p : Bool → Prop} : (∃ y, p (Bool.not y)) ↔ (∃ y, p y) := by
  constructor
  · rintro ⟨y, h⟩; exact ⟨Bool.not y, h⟩
  · rintro ⟨y, h⟩; exact ⟨Bool.not y, by rw [Bool.not_not]; exact h⟩

/-- **The invariant that exists at the junction.**  Transporting `(r, m)` by the
swap (acting on BOTH the relation and the mark) preserves `markIsSource`.  This
is what distinguishes it from rung 3's `readsFwd`, which the swap broke: on the
enriched pointed structure the separator IS invariant. -/
theorem markIsSource_swap_invariant (r : Bool → Bool → Prop) (m : Bool) :
    markIsSource (fun x y => r (Bool.not x) (Bool.not y)) (Bool.not m)
      ↔ markIsSource r m := by
  have e1 : (∃ y, (fun x y => r (Bool.not x) (Bool.not y)) (Bool.not m) y)
              ↔ (∃ y, r m y) := by
    simp only [Bool.not_not]; exact @exists_swap (fun z => r m z)
  have e2 : (∃ x, (fun x y => r (Bool.not x) (Bool.not y)) x (Bool.not m))
              ↔ (∃ x, r x m) := by
    simp only [Bool.not_not]; exact @exists_swap (fun z => r z m)
  unfold markIsSource
  rw [e1, e2]

/-! ## The new residual: the choice of mark -/

/-- **The fresh residual.**  The very invariance that legitimises `markIsSource`
also shows the CHOICE of mark is a new blind spot: `(D2, false)` and
`(D2rev, true)` are swap-transports of each other, so `markIsSource` assigns them
the same value.  With the mark fixed the sign is resolved; the mark itself is the
next sign gap, invariant-blind again — the tower alternates, it does not stop. -/
theorem mark_choice_residual :
    (markIsSource D2 false ↔ markIsSource D2rev true) ∧
    (markIsSource D2 false ∧ ¬ markIsSource D2rev false) := by
  refine ⟨?_, markIsSource_separates⟩
  -- (D2rev, true) is the swap-transport of (D2, false); invariance identifies them
  have hinv := markIsSource_swap_invariant D2 false
  -- hinv : markIsSource (fun x y => D2 (!x)(!y)) (!false) ↔ markIsSource D2 false
  have hrel : (fun x y => D2 (Bool.not x) (Bool.not y)) = D2rev := by
    funext x y; apply propext; exact (D2rev_iso_D2 x y).symm
  rw [hrel] at hinv
  -- hinv : markIsSource D2rev (Bool.not false) ↔ markIsSource D2 false
  simpa using hinv.symm

/-! ## Summary -/

/-- **Rung 4, summary.**  Rung 4 EXISTS: on the pointed structure produced by the
rung-3 lift, the intrinsic invariant `markIsSource` (i) separates `D2` from
`D2rev` at a fixed mark and (ii) is a genuine pointed invariant.  So an invariant
is available at the up-functor junction.  The resolution is conditional on the
admitted mark and spawns a new residual (the mark choice), so the tower
continues. -/
theorem rung4_exists_and_recurses :
    (markIsSource D2 false ∧ ¬ markIsSource D2rev false) ∧
    (∀ r m, markIsSource (fun x y => r (Bool.not x) (Bool.not y)) (Bool.not m)
              ↔ markIsSource r m) ∧
    (markIsSource D2 false ↔ markIsSource D2rev true) :=
  ⟨markIsSource_separates, markIsSource_swap_invariant, (mark_choice_residual).1⟩

/-! ## Axiom receipts -/

#print axioms markIsSource_separates
#print axioms markIsSource_D2rev_true
#print axioms exists_swap
#print axioms markIsSource_swap_invariant
#print axioms mark_choice_residual
#print axioms rung4_exists_and_recurses

end Rung4
end PrimDiff
