import Derivation.Minimality
import Derivation.MinimalityF

/-!
# Reading-F Challenge-3 Class Distinctness in Lean 4

Target 2 formalization: Pairwise non-isomorphism of five F-reading classes
at Challenge 3 under reading F ($R_{2F}$):
- `U0F`: Unary mark on required datum 1
- `BD_F`: Binary self-loop on required datum 1
- `BL_F`: Binary link between required data (1, 2)
- `FOUT_F`: Binary link from required datum 1 to genesis datum 0
- `FIN_F`: Binary link from genesis datum 0 to required datum 1

These five concrete F-reading regime literals are pairwise non-isomorphic under the sealed Iso definition. Their coverage of the full Challenge-3 F class space is verified separately by the enumerator, not by this module.

All 10 pairwise non-isomorphisms are established constructively without external
classification axioms:
1. Four arity invariants: `BD_F ≠ U0F`, `BL_F ≠ U0F`, `FOUT_F ≠ U0F`, `FIN_F ≠ U0F`.
2. Three diagonal argument invariants: `BD_F ≠ BL_F`, `BD_F ≠ FOUT_F`, `BD_F ≠ FIN_F`.
3. Two genesis-datum requirement preservation invariants: `BL_F ≠ FOUT_F`, `BL_F ≠ FIN_F`.
4. One directionality / ordering invariant: `FOUT_F ≠ FIN_F`.

Axioms used: strictly contained in `{propext, Quot.sound}`.
-/

namespace ReadingFIso

open Derivation

/-! ## 1. The Five F-Reading Representatives -/

/-- Class 1: Unary mark on one required datum (arity 1). -/
def U0F : Regime := Derivation.U0F

/-- Class 2: Binary self-loop on one required datum (arity 2, diagonal). -/
def BD_F : Regime := ⟨3, [2], [(0, [1, 1])], [], [(1, 2)]⟩

/-- Class 3: Binary link between required data (arity 2, internal pair). -/
def BL_F : Regime := ⟨3, [2], [(0, [1, 2])], [], [(1, 2)]⟩

/-- Class 4: Binary link from required datum to genesis datum 0 (arity 2, out). -/
def FOUT_F : Regime := ⟨3, [2], [(0, [1, 0])], [], [(1, 2)]⟩

/-- Class 5: Binary link from genesis datum 0 to required datum (arity 2, in). -/
def FIN_F : Regime := ⟨3, [2], [(0, [0, 1])], [], [(1, 2)]⟩

/-! ## 2. Auxiliary Lemma: Single Form Bijection Map -/

theorem single_form_fmap {r s : Regime} (iso : Iso r s)
    (hr : r.forms.length = 1) (hs : s.forms.length = 1) :
    iso.fmap 0 = 0 := by
  have hlt := iso.fmap_lt 0 (by
    rw [hr]; exact List.mem_range.mpr Nat.zero_lt_one)
  have : iso.fmap 0 < 1 := by
    simpa [hs] using hlt
  omega

/-! ## 3. Arity Invariants (4 Pairs) -/

-- Pair 1: BD_F vs U0F
theorem not_iso_BD_F_U0F (iso : Iso BD_F U0F) : False := by
  have h0 := single_form_fmap iso (by simp [BD_F]) (by simp [U0F, Derivation.U0F])
  have ha := iso.arity 0 (by simp [BD_F])
  rw [h0] at ha
  simp [BD_F, U0F, Derivation.U0F] at ha

theorem not_iso_U0F_BD_F (iso : Iso U0F BD_F) : False := by
  have h0 := single_form_fmap iso (by simp [U0F, Derivation.U0F]) (by simp [BD_F])
  have ha := iso.arity 0 (by simp [U0F, Derivation.U0F])
  rw [h0] at ha
  simp [U0F, Derivation.U0F, BD_F] at ha

theorem ne_BD_F_U0F : BD_F ≠ U0F := by
  intro h; cases h

-- Pair 2: BL_F vs U0F
theorem not_iso_BL_F_U0F (iso : Iso BL_F U0F) : False := by
  have h0 := single_form_fmap iso (by simp [BL_F]) (by simp [U0F, Derivation.U0F])
  have ha := iso.arity 0 (by simp [BL_F])
  rw [h0] at ha
  simp [BL_F, U0F, Derivation.U0F] at ha

theorem not_iso_U0F_BL_F (iso : Iso U0F BL_F) : False := by
  have h0 := single_form_fmap iso (by simp [U0F, Derivation.U0F]) (by simp [BL_F])
  have ha := iso.arity 0 (by simp [U0F, Derivation.U0F])
  rw [h0] at ha
  simp [U0F, Derivation.U0F, BL_F] at ha

theorem ne_BL_F_U0F : BL_F ≠ U0F := by
  intro h; cases h

-- Pair 3: FOUT_F vs U0F
theorem not_iso_FOUT_F_U0F (iso : Iso FOUT_F U0F) : False := by
  have h0 := single_form_fmap iso (by simp [FOUT_F]) (by simp [U0F, Derivation.U0F])
  have ha := iso.arity 0 (by simp [FOUT_F])
  rw [h0] at ha
  simp [FOUT_F, U0F, Derivation.U0F] at ha

theorem not_iso_U0F_FOUT_F (iso : Iso U0F FOUT_F) : False := by
  have h0 := single_form_fmap iso (by simp [U0F, Derivation.U0F]) (by simp [FOUT_F])
  have ha := iso.arity 0 (by simp [U0F, Derivation.U0F])
  rw [h0] at ha
  simp [U0F, Derivation.U0F, FOUT_F] at ha

theorem ne_FOUT_F_U0F : FOUT_F ≠ U0F := by
  intro h; cases h

-- Pair 4: FIN_F vs U0F
theorem not_iso_FIN_F_U0F (iso : Iso FIN_F U0F) : False := by
  have h0 := single_form_fmap iso (by simp [FIN_F]) (by simp [U0F, Derivation.U0F])
  have ha := iso.arity 0 (by simp [FIN_F])
  rw [h0] at ha
  simp [FIN_F, U0F, Derivation.U0F] at ha

theorem not_iso_U0F_FIN_F (iso : Iso U0F FIN_F) : False := by
  have h0 := single_form_fmap iso (by simp [U0F, Derivation.U0F]) (by simp [FIN_F])
  have ha := iso.arity 0 (by simp [U0F, Derivation.U0F])
  rw [h0] at ha
  simp [U0F, Derivation.U0F, FIN_F] at ha

theorem ne_FIN_F_U0F : FIN_F ≠ U0F := by
  intro h; cases h

/-! ## 4. Diagonal Argument Equality Invariants (3 Pairs) -/

-- Pair 5: BD_F vs BL_F
theorem not_iso_BD_F_BL_F (iso : Iso BD_F BL_F) : False := by
  have h := iso.insts_fwd (0, [1, 1]) (by decide)
  have h11 : iso.dmap 1 = 1 ∧ iso.dmap 1 = 2 := by
    simp [BL_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have : (1 : Nat) = 2 := h11.1.symm.trans h11.2
  cases this

theorem not_iso_BL_F_BD_F (iso : Iso BL_F BD_F) : False := by
  have h := iso.insts_fwd (0, [1, 2]) (by decide)
  have h12 : iso.dmap 1 = 1 ∧ iso.dmap 2 = 1 := by
    simp [BD_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have i1 := iso.dinv_dmap 1 (by decide)
  have i2 := iso.dinv_dmap 2 (by decide)
  rw [h12.1] at i1
  rw [h12.2] at i2
  omega

theorem ne_BD_F_BL_F : BD_F ≠ BL_F := by
  intro h; cases h

-- Pair 6: BD_F vs FOUT_F
theorem not_iso_BD_F_FOUT_F (iso : Iso BD_F FOUT_F) : False := by
  have h := iso.insts_fwd (0, [1, 1]) (by decide)
  have h11 : iso.dmap 1 = 1 ∧ iso.dmap 1 = 0 := by
    simp [FOUT_F] at h
    exact ⟨h.2.1, h.2.2⟩
  omega

theorem not_iso_FOUT_F_BD_F (iso : Iso FOUT_F BD_F) : False := by
  have h := iso.insts_fwd (0, [1, 0]) (by decide)
  have h10 : iso.dmap 1 = 1 ∧ iso.dmap 0 = 1 := by
    simp [BD_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have i1 := iso.dinv_dmap 1 (by decide)
  have i0 := iso.dinv_dmap 0 (by decide)
  rw [h10.1] at i1
  rw [h10.2] at i0
  omega

theorem ne_BD_F_FOUT_F : BD_F ≠ FOUT_F := by
  intro h; cases h

-- Pair 7: BD_F vs FIN_F
theorem not_iso_BD_F_FIN_F (iso : Iso BD_F FIN_F) : False := by
  have h := iso.insts_fwd (0, [1, 1]) (by decide)
  have h11 : iso.dmap 1 = 0 ∧ iso.dmap 1 = 1 := by
    simp [FIN_F] at h
    exact ⟨h.2.1, h.2.2⟩
  omega

theorem not_iso_FIN_F_BD_F (iso : Iso FIN_F BD_F) : False := by
  have h := iso.insts_fwd (0, [0, 1]) (by decide)
  have h01 : iso.dmap 0 = 1 ∧ iso.dmap 1 = 1 := by
    simp [BD_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have i0 := iso.dinv_dmap 0 (by decide)
  have i1 := iso.dinv_dmap 1 (by decide)
  rw [h01.1] at i0
  rw [h01.2] at i1
  omega

theorem ne_BD_F_FIN_F : BD_F ≠ FIN_F := by
  intro h; cases h

/-! ## 5. Genesis Datum Requirement Preservation Invariants (2 Pairs) -/

-- Pair 8: BL_F vs FOUT_F
theorem not_iso_BL_F_FOUT_F (iso : Iso BL_F FOUT_F) : False := by
  have h := iso.insts_fwd (0, [1, 2]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 1 = 1 ∧ iso.dmap 2 = 0 := by
    simp [FOUT_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have hsp : sortPair (iso.dmap 1, iso.dmap 2) = (0, 1) := by
    rw [hargs.1, hargs.2]; decide
  have : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [FOUT_F] using hr
  rw [hsp] at this
  cases this

theorem not_iso_FOUT_F_BL_F (iso : Iso FOUT_F BL_F) : False := by
  have h := iso.insts_fwd (0, [1, 0]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 1 = 1 ∧ iso.dmap 0 = 2 := by
    simp [BL_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have hsp : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [BL_F] using hr
  rw [hargs.1] at hsp
  have hd2 : iso.dmap 2 = 2 := by
    have hlt : iso.dmap 2 < 3 := iso.dmap_lt 2 (by decide)
    match hx : iso.dmap 2 with
    | 0 =>
      have : sortPair (1, 0) = (0, 1) := by decide
      rw [hx, this] at hsp
      cases hsp
    | 1 =>
      have : sortPair (1, 1) = (1, 1) := by decide
      rw [hx, this] at hsp
      cases hsp
    | 2 => rfl
    | _ + 3 => omega
  have i0 := iso.dinv_dmap 0 (by decide)
  have i2 := iso.dinv_dmap 2 (by decide)
  rw [hargs.2] at i0
  rw [hd2] at i2
  omega

theorem ne_BL_F_FOUT_F : BL_F ≠ FOUT_F := by
  intro h; cases h

-- Pair 9: BL_F vs FIN_F
theorem not_iso_BL_F_FIN_F (iso : Iso BL_F FIN_F) : False := by
  have h := iso.insts_fwd (0, [1, 2]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 1 = 0 ∧ iso.dmap 2 = 1 := by
    simp [FIN_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have hsp : sortPair (iso.dmap 1, iso.dmap 2) = (0, 1) := by
    rw [hargs.1, hargs.2]; decide
  have : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [FIN_F] using hr
  rw [hsp] at this
  cases this

theorem not_iso_FIN_F_BL_F (iso : Iso FIN_F BL_F) : False := by
  have h := iso.insts_fwd (0, [0, 1]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 0 = 1 ∧ iso.dmap 1 = 2 := by
    simp [BL_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have hsp : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [BL_F] using hr
  rw [hargs.2] at hsp
  have hd2 : iso.dmap 2 = 1 := by
    have hlt : iso.dmap 2 < 3 := iso.dmap_lt 2 (by decide)
    match hx : iso.dmap 2 with
    | 0 =>
      have : sortPair (2, 0) = (0, 2) := by decide
      rw [hx, this] at hsp
      cases hsp
    | 1 => rfl
    | 2 =>
      have : sortPair (2, 2) = (2, 2) := by decide
      rw [hx, this] at hsp
      cases hsp
    | _ + 3 => omega
  have i0 := iso.dinv_dmap 0 (by decide)
  have i2 := iso.dinv_dmap 2 (by decide)
  rw [hargs.1] at i0
  rw [hd2] at i2
  omega

theorem ne_BL_F_FIN_F : BL_F ≠ FIN_F := by
  intro h; cases h

/-! ## 6. Directionality / Argument Ordering Invariant (1 Pair) -/

-- Pair 10: FOUT_F vs FIN_F
theorem not_iso_FOUT_F_FIN_F (iso : Iso FOUT_F FIN_F) : False := by
  have h := iso.insts_fwd (0, [1, 0]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 1 = 0 ∧ iso.dmap 0 = 1 := by
    simp [FIN_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [FIN_F] using hr
  rw [hargs.1] at this
  have hle : (0 : Nat) ≤ iso.dmap 2 := Nat.zero_le _
  have hsp : sortPair (0, iso.dmap 2) = (0, iso.dmap 2) := by
    simp [sortPair, hle]
  rw [hsp] at this
  cases this

theorem not_iso_FIN_F_FOUT_F (iso : Iso FIN_F FOUT_F) : False := by
  have h := iso.insts_fwd (0, [0, 1]) (by decide)
  have hr := iso.reqs_fwd (1, 2) (by decide)
  have hargs : iso.dmap 0 = 1 ∧ iso.dmap 1 = 0 := by
    simp [FOUT_F] at h
    exact ⟨h.2.1, h.2.2⟩
  have : sortPair (iso.dmap 1, iso.dmap 2) = (1, 2) := by
    simpa [FOUT_F] using hr
  rw [hargs.2] at this
  have hle : (0 : Nat) ≤ iso.dmap 2 := Nat.zero_le _
  have hsp : sortPair (0, iso.dmap 2) = (0, iso.dmap 2) := by
    simp [sortPair, hle]
  rw [hsp] at this
  cases this

theorem ne_FOUT_F_FIN_F : FOUT_F ≠ FIN_F := by
  intro h; cases h

/-! ## 7. Master Pairwise Non-Isomorphism Conjunction -/

theorem ten_pairwise_non_isomorphic :
    (Iso BD_F U0F → False) ∧
    (Iso BL_F U0F → False) ∧
    (Iso FOUT_F U0F → False) ∧
    (Iso FIN_F U0F → False) ∧
    (Iso BD_F BL_F → False) ∧
    (Iso BD_F FOUT_F → False) ∧
    (Iso BD_F FIN_F → False) ∧
    (Iso BL_F FOUT_F → False) ∧
    (Iso BL_F FIN_F → False) ∧
    (Iso FOUT_F FIN_F → False) :=
  ⟨not_iso_BD_F_U0F,
   not_iso_BL_F_U0F,
   not_iso_FOUT_F_U0F,
   not_iso_FIN_F_U0F,
   not_iso_BD_F_BL_F,
   not_iso_BD_F_FOUT_F,
   not_iso_BD_F_FIN_F,
   not_iso_BL_F_FOUT_F,
   not_iso_BL_F_FIN_F,
   not_iso_FOUT_F_FIN_F⟩

theorem ten_pairwise_disequal :
    BD_F ≠ U0F ∧
    BL_F ≠ U0F ∧
    FOUT_F ≠ U0F ∧
    FIN_F ≠ U0F ∧
    BD_F ≠ BL_F ∧
    BD_F ≠ FOUT_F ∧
    BD_F ≠ FIN_F ∧
    BL_F ≠ FOUT_F ∧
    BL_F ≠ FIN_F ∧
    FOUT_F ≠ FIN_F :=
  ⟨ne_BD_F_U0F,
   ne_BL_F_U0F,
   ne_FOUT_F_U0F,
   ne_FIN_F_U0F,
   ne_BD_F_BL_F,
   ne_BD_F_FOUT_F,
   ne_BD_F_FIN_F,
   ne_BL_F_FOUT_F,
   ne_BL_F_FIN_F,
   ne_FOUT_F_FIN_F⟩

end ReadingFIso

#print axioms ReadingFIso.single_form_fmap
#print axioms ReadingFIso.not_iso_BD_F_U0F
#print axioms ReadingFIso.not_iso_BL_F_U0F
#print axioms ReadingFIso.not_iso_FOUT_F_U0F
#print axioms ReadingFIso.not_iso_FIN_F_U0F
#print axioms ReadingFIso.not_iso_BD_F_BL_F
#print axioms ReadingFIso.not_iso_BD_F_FOUT_F
#print axioms ReadingFIso.not_iso_BD_F_FIN_F
#print axioms ReadingFIso.not_iso_BL_F_FOUT_F
#print axioms ReadingFIso.not_iso_BL_F_FIN_F
#print axioms ReadingFIso.not_iso_FOUT_F_FIN_F
#print axioms ReadingFIso.ten_pairwise_non_isomorphic
#print axioms ReadingFIso.ten_pairwise_disequal
