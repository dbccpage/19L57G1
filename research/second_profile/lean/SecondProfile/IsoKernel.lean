import SecondProfile.Kernel

/-!
# The sealed isomorphism relation, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from the sealed module `lean4/Derivation/Minimality.lean`, lines one
hundred and sixty-nine through two hundred and twenty-four, at the blob
recorded in `SOURCE_MANIFEST.json`, at the snapshot recorded there: the
requirement ordering `sortPair`, the isomorphism structure `Iso` that
mirrors the sealed Python relation, its identity instance `isoRefl` and
the swap of the first two data `swap01`.  The only change is the outer
namespace, so that this package stays self-contained and imports nothing
sealed.  Doc comments and proofs are the sealed ones, unedited.

`verify_pins.py` recomputes the blob hash of the sealed source and of the
span at the snapshot and reports drift at HEAD, and
`test_reconstruction.py` compares this file declaration by declaration
with the pinned blob AT THE SNAPSHOT.

What a pin proves: that the sealed source did not move.  An AUTOMORPHISM
in this rung is an `Iso r r`; nothing here adds a field to the sealed
structure or weakens one.

AuthorityEffect: None.
-/

namespace SecondProfile
namespace Sealed

def sortPair (p : Nat × Nat) : Nat × Nat :=
  if p.1 ≤ p.2 then p else (p.2, p.1)

/-- Isomorphism of regimes: bijections on datum and form indices (given by
two-sided inverses on the admitted ranges) preserving arities, instances,
rules, and requirements.  Mirrors `code/derivation/iso.py`; presentation
tokens are already absent from the Lean model. -/
structure Iso (r s : Regime) where
  dmap : Nat → Nat
  dinv : Nat → Nat
  fmap : Nat → Nat
  finv : Nat → Nat
  dmap_lt : ∀ d ∈ List.range r.data, dmap d < s.data
  dinv_lt : ∀ d ∈ List.range s.data, dinv d < r.data
  dinv_dmap : ∀ d ∈ List.range r.data, dinv (dmap d) = d
  dmap_dinv : ∀ d ∈ List.range s.data, dmap (dinv d) = d
  fmap_lt : ∀ f ∈ List.range r.forms.length, fmap f < s.forms.length
  finv_lt : ∀ f ∈ List.range s.forms.length, finv f < r.forms.length
  finv_fmap : ∀ f ∈ List.range r.forms.length, finv (fmap f) = f
  fmap_finv : ∀ f ∈ List.range s.forms.length, fmap (finv f) = f
  arity : ∀ f ∈ List.range r.forms.length,
      s.forms.getD (fmap f) 0 = r.forms.getD f 0
  insts_fwd : ∀ p ∈ r.insts, (fmap p.1, p.2.map dmap) ∈ s.insts
  insts_bwd : ∀ p ∈ s.insts, (finv p.1, p.2.map dinv) ∈ r.insts
  rules_fwd : ∀ f ∈ r.rules, fmap f ∈ s.rules
  rules_bwd : ∀ f ∈ s.rules, finv f ∈ r.rules
  reqs_fwd : ∀ q ∈ r.reqs, sortPair (dmap q.1, dmap q.2) ∈ s.reqs
  reqs_bwd : ∀ q ∈ s.reqs, sortPair (dinv q.1, dinv q.2) ∈ r.reqs

/-- Every regime with sorted requirement pairs is isomorphic to itself. -/
def isoRefl (r : Regime) (hreqs : ∀ q ∈ r.reqs, q.1 ≤ q.2) : Iso r r where
  dmap := id
  dinv := id
  fmap := id
  finv := id
  dmap_lt := fun d hd => List.mem_range.mp hd
  dinv_lt := fun d hd => List.mem_range.mp hd
  dinv_dmap := fun _ _ => rfl
  dmap_dinv := fun _ _ => rfl
  fmap_lt := fun f hf => List.mem_range.mp hf
  finv_lt := fun f hf => List.mem_range.mp hf
  finv_fmap := fun _ _ => rfl
  fmap_finv := fun _ _ => rfl
  arity := fun _ _ => rfl
  insts_fwd := fun p hp => by simpa [List.map_id] using hp
  insts_bwd := fun p hp => by simpa [List.map_id] using hp
  rules_fwd := fun _ hf => hf
  rules_bwd := fun _ hf => hf
  reqs_fwd := fun q hq => by
    simpa [sortPair, hreqs q hq] using hq
  reqs_bwd := fun q hq => by
    simpa [sortPair, hreqs q hq] using hq

/-- The swap of the two data. -/
def swap01 (d : Nat) : Nat :=
  if d = 0 then 1 else if d = 1 then 0 else d

end Sealed
end SecondProfile
