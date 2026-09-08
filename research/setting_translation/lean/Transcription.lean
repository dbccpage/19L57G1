import Chains

/-!
# Transcription: the thirteen sealed concrete settings as finite settings

The sealed `PrimitiveCore` proves 42 verdicts on thirteen concrete settings
with carriers `Unit`, `Bool` and `Fin 3`.  Each is transcribed here as a
`FiniteSetting` (the one-point carrier as `{0}`, `false = 0`, `true = 1`,
`Fin 3` as `{0, 1, 2}`; the admitted merger `fun _ => false` as the constant
operation to `0`), and each sealed verdict is re-proved on the transcription
by deciding the reading's regime-level form through the `*_iff` theorems.
The theorem names repeat the sealed names inside this namespace, so the
correspondence is a name-to-name one that the Python census resolves
against both sources.

What this does not prove: an isomorphism of settings between a sealed
setting and its transcription.  It proves that the transcription, read
through the encoding, carries the verdicts the sealed setting is proved to
carry.

AuthorityEffect: None.
-/

namespace Transcription

open Derivation Translation Chains

/-! ## 1. A checked constructor -/

/-- Every operation closed on the carrier, as a boolean. -/
def closedOn (n : Nat) (ops : List (Nat → Nat)) : Bool :=
  ops.all (fun g => (List.range n).all (fun x => decide (g x < n)))

/-- Endpoints in the carrier and operations closed, as a boolean. -/
def ok (n a b : Nat) (ops : List (Nat → Nat)) : Bool :=
  decide (a < n) && decide (b < n) && closedOn n ops

theorem closedOn_spec {n : Nat} {ops : List (Nat → Nat)} (h : closedOn n ops = true) :
    ∀ g ∈ ops, ∀ x, x < n → g x < n := by
  intro g hg x hx
  have h1 : (List.range n).all (fun x => decide (g x < n)) = true :=
    List.all_eq_true.mp h g hg
  exact of_decide_eq_true (List.all_eq_true.mp h1 x (List.mem_range.mpr hx))

theorem ok_a {n a b : Nat} {ops : List (Nat → Nat)} (h : ok n a b ops = true) : a < n :=
  of_decide_eq_true ((Bool.and_eq_true _ _).mp ((Bool.and_eq_true _ _).mp h).1).1

theorem ok_b {n a b : Nat} {ops : List (Nat → Nat)} (h : ok n a b ops = true) : b < n :=
  of_decide_eq_true ((Bool.and_eq_true _ _).mp ((Bool.and_eq_true _ _).mp h).1).2

theorem ok_ops {n a b : Nat} {ops : List (Nat → Nat)} (h : ok n a b ops = true) :
    ∀ g ∈ ops, ∀ x, x < n → g x < n :=
  closedOn_spec ((Bool.and_eq_true _ _).mp h).2

/-- A finite setting from checked data. -/
def ofOk (n : Nat) (rel ret prot : Nat → Nat → Bool) (a b : Nat) (ops : List (Nat → Nat))
    (h : ok n a b ops = true) : FiniteSetting :=
  ⟨n, rel, ret, prot, a, b, ops, ok_a h, ok_b h, ok_ops h⟩

/-! ## 2. The stores and the merger -/

/-- Every pair asserted. -/
def every : Nat → Nat → Bool := fun _ _ => true

/-- No pair asserted. -/
def empty : Nat → Nat → Bool := fun _ _ => false

/-- The oriented edge from `0` to `1` (the sealed `D2` and `triR`). -/
def edge : Nat → Nat → Bool := fun x y => decide (x = 0 ∧ y = 1)

/-- The edge in both orientations (the sealed `S2` and `triSymR`). -/
def both : Nat → Nat → Bool := fun x y => decide ((x = 0 ∧ y = 1) ∨ (x = 1 ∧ y = 0))

/-- The admitted merger `fun _ => false`. -/
def merger : Nat → Nat := fun _ => 0

/-! ## 3. The thirteen transcriptions -/

def unitBare : FiniteSetting := ofOk 1 every empty empty 0 0 [] (by decide)
def unitFull : FiniteSetting := ofOk 1 every every every 0 0 [] (by decide)
def d2Bare : FiniteSetting := ofOk 2 edge empty empty 0 1 [] (by decide)
def d2Merged : FiniteSetting := ofOk 2 edge empty empty 0 1 [merger] (by decide)
def d2Protected : FiniteSetting := ofOk 2 edge every every 0 1 [] (by decide)
def d2ProtectedMerged : FiniteSetting := ofOk 2 edge every every 0 1 [merger] (by decide)
def s2Bare : FiniteSetting := ofOk 2 both empty empty 0 1 [] (by decide)
def s2Merged : FiniteSetting := ofOk 2 both empty empty 0 1 [merger] (by decide)
def tri : FiniteSetting := ofOk 3 edge empty empty 0 1 [] (by decide)
def triProtected : FiniteSetting := ofOk 3 edge every every 0 1 [] (by decide)
def triSym : FiniteSetting := ofOk 3 both empty empty 0 1 [] (by decide)
def boolEmpty : FiniteSetting := ofOk 2 empty empty empty 0 1 [] (by decide)
def boolEmptyMerged : FiniteSetting := ofOk 2 empty empty empty 0 1 [merger] (by decide)

/-! ## 4. The 42 verdicts, decided on the encodings -/

theorem unitBare_w : PrimitiveCore.W (toSetting unitBare) := (W_iff _).mpr (by decide)
theorem unitBare_not_a : ¬ PrimitiveCore.A (toSetting unitBare) :=
  fun h => absurd ((A_iff _).mp h) (by decide)
theorem unitBare_not_c : ¬ PrimitiveCore.C (toSetting unitBare) :=
  fun h => absurd ((C_iff _).mp h) (by decide)
theorem unitBare_not_d : ¬ PrimitiveCore.D (toSetting unitBare) :=
  fun h => absurd ((D_iff _).mp h) (by decide)
theorem unitBare_not_e : ¬ PrimitiveCore.E (toSetting unitBare) :=
  fun h => absurd ((E_iff_noChain _).mp h) (by decide)

theorem unitFull_c : PrimitiveCore.C (toSetting unitFull) := (C_iff _).mpr (by decide)
theorem unitFull_not_a : ¬ PrimitiveCore.A (toSetting unitFull) :=
  fun h => absurd ((A_iff _).mp h) (by decide)
theorem unitFull_not_d : ¬ PrimitiveCore.D (toSetting unitFull) :=
  fun h => absurd ((D_iff _).mp h) (by decide)
theorem unitFull_not_e : ¬ PrimitiveCore.E (toSetting unitFull) :=
  fun h => absurd ((E_iff_noChain _).mp h) (by decide)

theorem d2Bare_a : PrimitiveCore.A (toSetting d2Bare) := (A_iff _).mpr (by decide)
theorem d2Bare_not_bs : ¬ PrimitiveCore.Bs (toSetting d2Bare) :=
  fun h => absurd ((Bs_iff _).mp h) (by decide)
theorem d2Bare_bc : PrimitiveCore.Bc (toSetting d2Bare) := (Bc_iff _).mpr (by decide)
theorem d2Bare_bl : PrimitiveCore.Bl (toSetting d2Bare) := (Bl_iff _).mpr (by decide)
theorem d2Bare_not_c : ¬ PrimitiveCore.C (toSetting d2Bare) :=
  fun h => absurd ((C_iff _).mp h) (by decide)
theorem d2Bare_not_f : ¬ PrimitiveCore.F (toSetting d2Bare) :=
  fun h => absurd ((F_iff _).mp h) (by decide)

theorem d2Merged_a : PrimitiveCore.A (toSetting d2Merged) := (A_iff _).mpr (by decide)
theorem d2Merged_bc : PrimitiveCore.Bc (toSetting d2Merged) := (Bc_iff _).mpr (by decide)
theorem d2Merged_bl : PrimitiveCore.Bl (toSetting d2Merged) := (Bl_iff _).mpr (by decide)
theorem d2Merged_not_e : ¬ PrimitiveCore.E (toSetting d2Merged) :=
  fun h => absurd ((E_iff_noChain _).mp h) (by decide)

theorem d2Protected_f : PrimitiveCore.F (toSetting d2Protected) := (F_iff _).mpr (by decide)
theorem d2Protected_not_bs : ¬ PrimitiveCore.Bs (toSetting d2Protected) :=
  fun h => absurd ((Bs_iff _).mp h) (by decide)

theorem d2ProtectedMerged_f : PrimitiveCore.F (toSetting d2ProtectedMerged) :=
  (F_iff _).mpr (by decide)
theorem d2ProtectedMerged_not_e : ¬ PrimitiveCore.E (toSetting d2ProtectedMerged) :=
  fun h => absurd ((E_iff_noChain _).mp h) (by decide)

theorem s2Bare_bs : PrimitiveCore.Bs (toSetting s2Bare) := (Bs_iff _).mpr (by decide)
theorem s2Bare_not_c : ¬ PrimitiveCore.C (toSetting s2Bare) :=
  fun h => absurd ((C_iff _).mp h) (by decide)
theorem s2Bare_not_f : ¬ PrimitiveCore.F (toSetting s2Bare) :=
  fun h => absurd ((F_iff _).mp h) (by decide)

theorem s2Merged_bs : PrimitiveCore.Bs (toSetting s2Merged) := (Bs_iff _).mpr (by decide)
theorem s2Merged_not_e : ¬ PrimitiveCore.E (toSetting s2Merged) :=
  fun h => absurd ((E_iff_noChain _).mp h) (by decide)

theorem tri_a : PrimitiveCore.A (toSetting tri) := (A_iff _).mpr (by decide)
theorem tri_bl : PrimitiveCore.Bl (toSetting tri) := (Bl_iff _).mpr (by decide)
theorem tri_not_bc : ¬ PrimitiveCore.Bc (toSetting tri) :=
  fun h => absurd ((Bc_iff _).mp h) (by decide)

theorem triProtected_f : PrimitiveCore.F (toSetting triProtected) := (F_iff _).mpr (by decide)
theorem triProtected_not_bc : ¬ PrimitiveCore.Bc (toSetting triProtected) :=
  fun h => absurd ((Bc_iff _).mp h) (by decide)

theorem triSym_bs : PrimitiveCore.Bs (toSetting triSym) := (Bs_iff _).mpr (by decide)
theorem triSym_not_bc : ¬ PrimitiveCore.Bc (toSetting triSym) :=
  fun h => absurd ((Bc_iff _).mp h) (by decide)

theorem boolEmpty_not_w : ¬ PrimitiveCore.W (toSetting boolEmpty) :=
  fun h => absurd ((W_iff _).mp h) (by decide)
theorem boolEmpty_not_a : ¬ PrimitiveCore.A (toSetting boolEmpty) :=
  fun h => absurd ((A_iff _).mp h) (by decide)
theorem boolEmpty_not_c : ¬ PrimitiveCore.C (toSetting boolEmpty) :=
  fun h => absurd ((C_iff _).mp h) (by decide)
theorem boolEmpty_d : PrimitiveCore.D (toSetting boolEmpty) := (D_iff _).mpr (by decide)
theorem boolEmpty_e : PrimitiveCore.E (toSetting boolEmpty) := (E_iff_noChain _).mpr (by decide)

theorem boolEmptyMerged_d : PrimitiveCore.D (toSetting boolEmptyMerged) := (D_iff _).mpr (by decide)
theorem boolEmptyMerged_not_e : ¬ PrimitiveCore.E (toSetting boolEmptyMerged) :=
  fun h => absurd ((E_iff_noChain _).mp h) (by decide)

end Transcription

#print axioms Transcription.closedOn_spec
#print axioms Transcription.ok_a
#print axioms Transcription.ok_b
#print axioms Transcription.ok_ops
#print axioms Transcription.unitBare_w
#print axioms Transcription.unitBare_not_a
#print axioms Transcription.unitBare_not_c
#print axioms Transcription.unitBare_not_d
#print axioms Transcription.unitBare_not_e
#print axioms Transcription.unitFull_c
#print axioms Transcription.unitFull_not_a
#print axioms Transcription.unitFull_not_d
#print axioms Transcription.unitFull_not_e
#print axioms Transcription.d2Bare_a
#print axioms Transcription.d2Bare_not_bs
#print axioms Transcription.d2Bare_bc
#print axioms Transcription.d2Bare_bl
#print axioms Transcription.d2Bare_not_c
#print axioms Transcription.d2Bare_not_f
#print axioms Transcription.d2Merged_a
#print axioms Transcription.d2Merged_bc
#print axioms Transcription.d2Merged_bl
#print axioms Transcription.d2Merged_not_e
#print axioms Transcription.d2Protected_f
#print axioms Transcription.d2Protected_not_bs
#print axioms Transcription.d2ProtectedMerged_f
#print axioms Transcription.d2ProtectedMerged_not_e
#print axioms Transcription.s2Bare_bs
#print axioms Transcription.s2Bare_not_c
#print axioms Transcription.s2Bare_not_f
#print axioms Transcription.s2Merged_bs
#print axioms Transcription.s2Merged_not_e
#print axioms Transcription.tri_a
#print axioms Transcription.tri_bl
#print axioms Transcription.tri_not_bc
#print axioms Transcription.triProtected_f
#print axioms Transcription.triProtected_not_bc
#print axioms Transcription.triSym_bs
#print axioms Transcription.triSym_not_bc
#print axioms Transcription.boolEmpty_not_w
#print axioms Transcription.boolEmpty_not_a
#print axioms Transcription.boolEmpty_not_c
#print axioms Transcription.boolEmpty_d
#print axioms Transcription.boolEmpty_e
#print axioms Transcription.boolEmptyMerged_d
#print axioms Transcription.boolEmptyMerged_not_e
