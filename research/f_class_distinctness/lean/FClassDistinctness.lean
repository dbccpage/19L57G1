import Derivation.Minimality
import Derivation.MinimalityF

/-!
# Reading-F Challenge-3 mu1 class distinctness

The sealed ledger records three reading-L classes as Lean
theorems and five reading-F classes as engine enumeration only.
This module names the five F representatives and proves they are
pairwise non-isomorphic, porting the L arity and instance arguments,
plus the requirement-preserving argument that separates a link out
of the required pair from a link into it.  The reading-L distinctness
theorems are not cited.

Reading L is not re-proved.  Both readings are carried: L remains the
sealed three-class theorem; F is the five-class theorem here.

AuthorityEffect: None.
-/

namespace FClassDistinctness

open Derivation

/-! ## The five class representatives

R2F has data `{0,1,2}` and requirement `(1,2)`.  Datum `0` is the
genesis inscription, outside the required pair.
-/

/-- Unary mark on a required datum.  Sealed `U0F`. -/
def MarkF : Regime := U0F

/-- Binary self-loop on a required datum. -/
def DiagF : Regime := ⟨3, [2], [(0, [1, 1])], [], [(1, 2)]⟩

/-- Binary link on the required pair. -/
def LinkF : Regime := ⟨3, [2], [(0, [1, 2])], [], [(1, 2)]⟩

/-- Binary link out of the required pair onto the genesis datum. -/
def OutF : Regime := ⟨3, [2], [(0, [1, 0])], [], [(1, 2)]⟩

/-- Binary link from the genesis datum into the required pair. -/
def InF : Regime := ⟨3, [2], [(0, [0, 1])], [], [(1, 2)]⟩

/-! ## Within-class collapses (the other member of each size-2 class) -/

def DiagF' : Regime := ⟨3, [2], [(0, [2, 2])], [], [(1, 2)]⟩
def LinkF' : Regime := ⟨3, [2], [(0, [2, 1])], [], [(1, 2)]⟩
def OutF' : Regime := ⟨3, [2], [(0, [2, 0])], [], [(1, 2)]⟩
def InF' : Regime := ⟨3, [2], [(0, [0, 2])], [], [(1, 2)]⟩

/-- Structure values as `def` generate a theorem per `Iso` field; a
single `Nonempty` theorem is the census object. -/
theorem isoDiagF'_exists : Nonempty (Iso DiagF' DiagF) :=
  ⟨{
    dmap := swap12, dinv := swap12, fmap := id, finv := id
    dmap_lt := by decide, dinv_lt := by decide
    dinv_dmap := by decide, dmap_dinv := by decide
    fmap_lt := by decide, finv_lt := by decide
    finv_fmap := by decide, fmap_finv := by decide
    arity := by decide, insts_fwd := by decide, insts_bwd := by decide
    rules_fwd := by decide, rules_bwd := by decide
    reqs_fwd := by decide, reqs_bwd := by decide
  }⟩

theorem isoLinkF'_exists : Nonempty (Iso LinkF' LinkF) :=
  ⟨{
    dmap := swap12, dinv := swap12, fmap := id, finv := id
    dmap_lt := by decide, dinv_lt := by decide
    dinv_dmap := by decide, dmap_dinv := by decide
    fmap_lt := by decide, finv_lt := by decide
    finv_fmap := by decide, fmap_finv := by decide
    arity := by decide, insts_fwd := by decide, insts_bwd := by decide
    rules_fwd := by decide, rules_bwd := by decide
    reqs_fwd := by decide, reqs_bwd := by decide
  }⟩

theorem isoOutF'_exists : Nonempty (Iso OutF' OutF) :=
  ⟨{
    dmap := swap12, dinv := swap12, fmap := id, finv := id
    dmap_lt := by decide, dinv_lt := by decide
    dinv_dmap := by decide, dmap_dinv := by decide
    fmap_lt := by decide, finv_lt := by decide
    finv_fmap := by decide, fmap_finv := by decide
    arity := by decide, insts_fwd := by decide, insts_bwd := by decide
    rules_fwd := by decide, rules_bwd := by decide
    reqs_fwd := by decide, reqs_bwd := by decide
  }⟩

theorem isoInF'_exists : Nonempty (Iso InF' InF) :=
  ⟨{
    dmap := swap12, dinv := swap12, fmap := id, finv := id
    dmap_lt := by decide, dinv_lt := by decide
    dinv_dmap := by decide, dmap_dinv := by decide
    fmap_lt := by decide, finv_lt := by decide
    finv_fmap := by decide, fmap_finv := by decide
    arity := by decide, insts_fwd := by decide, insts_bwd := by decide
    rules_fwd := by decide, rules_bwd := by decide
    reqs_fwd := by decide, reqs_bwd := by decide
  }⟩

/-! ## Arity is an invariant: mark is not any binary class -/

theorem one_form_fmap {r s : Regime} (iso : Iso r s)
    (hr : r.forms.length = 1) (hs : s.forms.length = 1) :
    iso.fmap 0 = 0 := by
  have hlt := iso.fmap_lt 0 (by
    rw [hr]; exact List.mem_range.mpr (Nat.zero_lt_one))
  have : iso.fmap 0 < 1 := by
    simpa [hs] using hlt
  omega

theorem MarkF_not_iso_LinkF (iso : Iso MarkF LinkF) : False := by
  have h0 := one_form_fmap iso (by simp [MarkF, U0F]) (by simp [LinkF])
  have ha := iso.arity 0 (by simp [MarkF, U0F])
  rw [h0] at ha
  simp [MarkF, U0F, LinkF] at ha

theorem MarkF_not_iso_DiagF (iso : Iso MarkF DiagF) : False := by
  have h0 := one_form_fmap iso (by simp [MarkF, U0F]) (by simp [DiagF])
  have ha := iso.arity 0 (by simp [MarkF, U0F])
  rw [h0] at ha
  simp [MarkF, U0F, DiagF] at ha

theorem MarkF_not_iso_OutF (iso : Iso MarkF OutF) : False := by
  have h0 := one_form_fmap iso (by simp [MarkF, U0F]) (by simp [OutF])
  have ha := iso.arity 0 (by simp [MarkF, U0F])
  rw [h0] at ha
  simp [MarkF, U0F, OutF] at ha

theorem MarkF_not_iso_InF (iso : Iso MarkF InF) : False := by
  have h0 := one_form_fmap iso (by simp [MarkF, U0F]) (by simp [InF])
  have ha := iso.arity 0 (by simp [MarkF, U0F])
  rw [h0] at ha
  simp [MarkF, U0F, InF] at ha

/-! ## Self-loop is not a mixed-endpoint link -/

theorem LinkF_not_iso_DiagF (iso : Iso LinkF DiagF) : False := by
  have h := iso.insts_fwd (0, [1, 2]) (by decide)
  have h12 : iso.dmap 1 = 1 ∧ iso.dmap 2 = 1 := by
    simp [DiagF] at h
    exact ⟨h.2.1, h.2.2⟩
  have i1 := iso.dinv_dmap 1 (by decide)
  have i2 := iso.dinv_dmap 2 (by decide)
  rw [h12.1] at i1
  rw [h12.2] at i2
  omega

/-! ## Required-pair link is not a genesis-touching link -/

theorem LinkF_not_iso_OutF (iso : Iso LinkF OutF) : False := by
  have h := iso.insts_fwd (0, [1, 2]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 1 = 1 ∧ iso.dmap 2 = 0 := by
    simp [OutF] at h
    exact ⟨h.2.1, h.2.2⟩
  have hsp : sortPair (iso.dmap 1, iso.dmap 2) = (0, 1) := by
    rw [hargs.1, hargs.2]; decide
  have : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [OutF] using hr
  rw [hsp] at this
  cases this

theorem LinkF_not_iso_InF (iso : Iso LinkF InF) : False := by
  have h := iso.insts_fwd (0, [1, 2]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 1 = 0 ∧ iso.dmap 2 = 1 := by
    simp [InF] at h
    exact ⟨h.2.1, h.2.2⟩
  have hsp : sortPair (iso.dmap 1, iso.dmap 2) = (0, 1) := by
    rw [hargs.1, hargs.2]; decide
  have : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [InF] using hr
  rw [hsp] at this
  cases this

theorem DiagF_not_iso_OutF (iso : Iso DiagF OutF) : False := by
  have h := iso.insts_fwd (0, [1, 1]) (by decide)
  have h11 : iso.dmap 1 = 1 ∧ iso.dmap 1 = 0 := by
    simp [OutF] at h
    exact ⟨h.2.1, h.2.2⟩
  omega

theorem DiagF_not_iso_InF (iso : Iso DiagF InF) : False := by
  have h := iso.insts_fwd (0, [1, 1]) (by decide)
  have h11 : iso.dmap 1 = 0 ∧ iso.dmap 1 = 1 := by
    simp [InF] at h
    exact ⟨h.2.1, h.2.2⟩
  omega

/-! ## Out is not In: a genesis endpoint cannot become a required endpoint -/

theorem OutF_not_iso_InF (iso : Iso OutF InF) : False := by
  have h := iso.insts_fwd (0, [1, 0]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 1 = 0 ∧ iso.dmap 0 = 1 := by
    simp [InF] at h
    exact ⟨h.2.1, h.2.2⟩
  have : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [InF] using hr
  rw [hargs.1] at this
  have hle : (0 : Nat) ≤ iso.dmap 2 := Nat.zero_le _
  have hsp : sortPair (0, iso.dmap 2) = (0, iso.dmap 2) := by
    simp [sortPair, hle]
  rw [hsp] at this
  cases this

/-! ## Conjunction: the five are pairwise non-isomorphic -/

theorem five_classes_pairwise_noniso :
    (Iso MarkF LinkF → False) ∧
    (Iso MarkF DiagF → False) ∧
    (Iso MarkF OutF → False) ∧
    (Iso MarkF InF → False) ∧
    (Iso LinkF DiagF → False) ∧
    (Iso LinkF OutF → False) ∧
    (Iso LinkF InF → False) ∧
    (Iso DiagF OutF → False) ∧
    (Iso DiagF InF → False) ∧
    (Iso OutF InF → False) :=
  ⟨MarkF_not_iso_LinkF, MarkF_not_iso_DiagF, MarkF_not_iso_OutF,
   MarkF_not_iso_InF, LinkF_not_iso_DiagF, LinkF_not_iso_OutF,
   LinkF_not_iso_InF, DiagF_not_iso_OutF, DiagF_not_iso_InF,
   OutF_not_iso_InF⟩

/-! ## Validity of the five two-item responses on R2F -/

theorem validResponse_R2F (δ : List Item) (s : Regime)
    (happ : applyDelta R2F δ = some s) (hsep : separable s 1 2) :
    validResponse R2F 1 2 δ := by
  refine ⟨s, happ, hsep, ?_⟩
  intro q hq
  have : q = (1, 2) := by
    cases hq with
    | head => rfl
    | tail _ h => cases h
  rw [this]
  exact hsep

theorem DiagF_separable : separable DiagF 1 2 :=
  ⟨⟨0, [none, some 1]⟩, by decide, by decide⟩

theorem LinkF_separable : separable LinkF 1 2 :=
  ⟨⟨0, [none, some 2]⟩, by decide, by decide⟩

theorem OutF_separable : separable OutF 1 2 :=
  ⟨⟨0, [none, some 0]⟩, by decide, by decide⟩

theorem InF_separable : separable InF 1 2 :=
  ⟨⟨0, [some 0, none]⟩, by decide, by decide⟩

def deltaMarkF : List Item := [.newForm 1, .newInst 0 [1]]
def deltaDiagF : List Item := [.newForm 2, .newInst 0 [1, 1]]
def deltaLinkF : List Item := [.newForm 2, .newInst 0 [1, 2]]
def deltaOutF : List Item := [.newForm 2, .newInst 0 [1, 0]]
def deltaInF : List Item := [.newForm 2, .newInst 0 [0, 1]]

theorem deltaMarkF_valid : validResponse R2F 1 2 deltaMarkF :=
  deltaU0F_valid

theorem deltaDiagF_valid : validResponse R2F 1 2 deltaDiagF :=
  validResponse_R2F _ DiagF (by decide) DiagF_separable

theorem deltaLinkF_valid : validResponse R2F 1 2 deltaLinkF :=
  validResponse_R2F _ LinkF (by decide) LinkF_separable

theorem deltaOutF_valid : validResponse R2F 1 2 deltaOutF :=
  validResponse_R2F _ OutF (by decide) OutF_separable

theorem deltaInF_valid : validResponse R2F 1 2 deltaInF :=
  validResponse_R2F _ InF (by decide) InF_separable

/-- The five representatives are two-item valid minima on R2F, pairwise
non-isomorphic.  Completeness of the catalog as *all* mu1 classes is
the sealed engine enumeration (CL-3-TIE-CLASSES), not this theorem. -/
theorem five_valid_pairwise_noniso :
    validResponse R2F 1 2 deltaMarkF ∧
    validResponse R2F 1 2 deltaDiagF ∧
    validResponse R2F 1 2 deltaLinkF ∧
    validResponse R2F 1 2 deltaOutF ∧
    validResponse R2F 1 2 deltaInF ∧
    (Iso MarkF LinkF → False) ∧
    (Iso MarkF DiagF → False) ∧
    (Iso MarkF OutF → False) ∧
    (Iso MarkF InF → False) ∧
    (Iso LinkF DiagF → False) ∧
    (Iso LinkF OutF → False) ∧
    (Iso LinkF InF → False) ∧
    (Iso DiagF OutF → False) ∧
    (Iso DiagF InF → False) ∧
    (Iso OutF InF → False) :=
  ⟨deltaMarkF_valid, deltaDiagF_valid, deltaLinkF_valid, deltaOutF_valid,
   deltaInF_valid,
   MarkF_not_iso_LinkF, MarkF_not_iso_DiagF, MarkF_not_iso_OutF,
   MarkF_not_iso_InF, LinkF_not_iso_DiagF, LinkF_not_iso_OutF,
   LinkF_not_iso_InF, DiagF_not_iso_OutF, DiagF_not_iso_InF,
   OutF_not_iso_InF⟩

end FClassDistinctness

#print axioms FClassDistinctness.isoDiagF'_exists
#print axioms FClassDistinctness.isoLinkF'_exists
#print axioms FClassDistinctness.isoOutF'_exists
#print axioms FClassDistinctness.isoInF'_exists
#print axioms FClassDistinctness.one_form_fmap
#print axioms FClassDistinctness.MarkF_not_iso_LinkF
#print axioms FClassDistinctness.MarkF_not_iso_DiagF
#print axioms FClassDistinctness.MarkF_not_iso_OutF
#print axioms FClassDistinctness.MarkF_not_iso_InF
#print axioms FClassDistinctness.LinkF_not_iso_DiagF
#print axioms FClassDistinctness.LinkF_not_iso_OutF
#print axioms FClassDistinctness.LinkF_not_iso_InF
#print axioms FClassDistinctness.DiagF_not_iso_OutF
#print axioms FClassDistinctness.DiagF_not_iso_InF
#print axioms FClassDistinctness.OutF_not_iso_InF
#print axioms FClassDistinctness.five_classes_pairwise_noniso
#print axioms FClassDistinctness.validResponse_R2F
#print axioms FClassDistinctness.DiagF_separable
#print axioms FClassDistinctness.LinkF_separable
#print axioms FClassDistinctness.OutF_separable
#print axioms FClassDistinctness.InF_separable
#print axioms FClassDistinctness.deltaMarkF_valid
#print axioms FClassDistinctness.deltaDiagF_valid
#print axioms FClassDistinctness.deltaLinkF_valid
#print axioms FClassDistinctness.deltaOutF_valid
#print axioms FClassDistinctness.deltaInF_valid
#print axioms FClassDistinctness.five_valid_pairwise_noniso
