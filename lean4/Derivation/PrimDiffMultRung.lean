import Derivation.PrimDiff

/-!
# The multiplicity rung: the difference between two witness multiplicities

POST-SEAL extension experiment artifact.  Imports `Derivation.PrimDiff`
unmodified; read-only proof receipt via `lake env lean`.  Everything is derived
from the sealed A2 material (witness stores `Bool → Bool → Nat`, presence
`0 < W`, and `multiplicity_invisible_to_presence`).  No new primitive,
parameter, observation, menu, policy, or oracle is introduced.

## The move (the second F1 forgetful step)

The orientation rung produced an *oriented* `D2` (the tie resolved).  F1's OTHER
forgetful step is multiplicity → presence.  Here the outcome is the opposite:
the difference between two witness structures that differ only in multiplicity
is **invisible to presence**, so it is NOT a primitive difference below the
observer — only metatheoretic inequality (A3).  Making it visible requires an
observer strictly finer than presence; presence merges an unbounded family of
multiplicities, so the finer observer needs strictly more symbols — a vocabulary
the presence layer does not supply (an external act, S6.6 / S9).
-/

namespace PrimDiff
namespace MultRung

/-! ## The multiplicity layer and its presence truncation -/

/-- Multiplicity of the witnessed pair (the A2 counting datum). -/
def mult (W : Bool → Bool → Nat) : Nat := W false true

/-- Presence: the Bool-shadow that forgets multiplicity (A2 → A1). -/
def presence (W : Bool → Bool → Nat) : Bool → Bool → Prop := fun x y => 0 < W x y

/-! ## Carrier-general property difference (rung 2, any carrier) -/

/-- The rung-2 `P`-difference on any carrier `C`. -/
def PDiff {C : Type} (P : C → Prop) (u v : C) : Prop := P u ∧ ¬ P v

theorem PDiff_irrefl {C : Type} (P : C → Prop) (c : C) : ¬ PDiff P c c :=
  fun h => h.2 h.1

/-- Non-separating ⇒ empty: if `P` cannot tell `a` from `b`, the `P`-difference
between them has no witness in either direction. -/
theorem PDiff_nonsep_empty {C : Type} {P : C → Prop} {a b : C} (h : P a ↔ P b) :
    ¬ PDiff P a b ∧ ¬ PDiff P b a :=
  ⟨fun k => k.2 (h.mp k.1), fun k => k.2 (h.mpr k.1)⟩

/-! ## Two witness structures differing only in multiplicity -/

/-- Constant store of height 1 (the sealed `W1` of
`multiplicity_invisible_to_presence`). -/
def W1 : Bool → Bool → Nat := fun _ _ => 1
/-- Constant store of height 2. -/
def W2 : Bool → Bool → Nat := fun _ _ => 2

theorem W1_ne_W2 : W1 ≠ W2 := by
  intro h
  have : (1 : Nat) = 2 := congrFun (congrFun h false) false
  omega

theorem mult_W1_ne_mult_W2 : mult W1 ≠ mult W2 := by
  show (1 : Nat) ≠ 2; omega

theorem presence_W1_eq_W2 : presence W1 = presence W2 := by
  funext x y
  show (0 < W1 x y) = (0 < W2 x y)
  simp [W1, W2]

/-! ## The multiplicity rung: the difference is not primitive below presence -/

/-- **Headline.**  Any observer that reads only presence cannot separate `W1`
from `W2`, so the rung-2 difference it induces between them is empty in both
directions.  Unlike the orientation difference (the oriented `D2`), the
multiplicity difference is NOT a primitive difference at the presence layer — it
is only metatheoretic inequality (`W1 ≠ W2`, A3), invisible to presence. -/
theorem mult_diff_empty_through_presence
    (Q : (Bool → Bool → Prop) → Prop) :
    ¬ PDiff (fun W => Q (presence W)) W1 W2 ∧
    ¬ PDiff (fun W => Q (presence W)) W2 W1 := by
  apply PDiff_nonsep_empty
  show Q (presence W1) ↔ Q (presence W2)
  rw [presence_W1_eq_W2]

/-- Yet the difference is real above the presence layer: `W1 ≠ W2`, and the full
multiplicity observer separates them.  The multiplicity difference exists but is
visible only to an observer strictly finer than presence. -/
theorem mult_diff_visible_to_mult :
    W1 ≠ W2 ∧ mult W1 ≠ mult W2 := ⟨W1_ne_W2, mult_W1_ne_mult_W2⟩

/-! ## Vocabulary expansion: presence merges an unbounded family -/

/-- Presence merges every positive multiplicity into one class: for all positive
`m, n`, presence cannot tell multiplicity `m` from `n`.  The `true`-fibre of the
presence observer is the whole infinite set {1, 2, 3, …}. -/
theorem presence_merges_all_positive {m n : Nat} (hm : 0 < m) (hn : 0 < n) :
    (0 < m) ↔ (0 < n) := iff_of_true hm hn

/-- Distinct multiplicities are genuinely distinct data: for `i ≠ j` the constant
stores of heights `i` and `j` differ.  With the previous theorem, presence
collapses infinitely many pairwise-distinct multiplicities into one class. -/
theorem multiplicities_distinct {i j : Nat} (h : i ≠ j) :
    (fun _ _ : Bool => i) ≠ (fun _ _ : Bool => j) := by
  intro he
  exact h (congrFun (congrFun he false) false)

/-- **Two symbols cannot resolve three multiplicities.**  Every Bool-valued
observer identifies two of `{0, 1, 2}`.  The presence alphabet (size 2) is
already insufficient at the first refinement past presence; resolving more
multiplicities forces a strictly larger alphabet.  (General form: an `s`-symbol
alphabet resolves at most `s` multiplicities — pigeonhole; here `s = 2`.) -/
theorem two_symbols_cannot_resolve_three (o : Nat → Bool) :
    o 0 = o 1 ∨ o 0 = o 2 ∨ o 1 = o 2 := by
  cases h0 : o 0 <;> cases h1 : o 1 <;> cases h2 : o 2 <;> simp_all

/-! ## Summary -/

/-- **Multiplicity rung, summary.**  The multiplicity difference between `W1`
and `W2` is (i) empty for every presence-factoring observer — not a primitive
difference below the observer — yet (ii) real and separated by the full
multiplicity observer.  Making it visible requires an observer strictly finer
than presence: presence merges an unbounded family
(`presence_merges_all_positive` + `multiplicities_distinct`), and even a
3-multiplicity window overflows the 2-symbol alphabet
(`two_symbols_cannot_resolve_three`).  The finer observer is not supplied by the
presence layer (sealed `multiplicity_invisible_to_presence`): admitting it is an
external act. -/
theorem multiplicity_rung_summary :
    (∀ Q : (Bool → Bool → Prop) → Prop, ¬ PDiff (fun W => Q (presence W)) W1 W2) ∧
    (W1 ≠ W2 ∧ mult W1 ≠ mult W2) :=
  ⟨fun Q => (mult_diff_empty_through_presence Q).1, mult_diff_visible_to_mult⟩

/-! ## Axiom receipts -/

#print axioms mult_diff_empty_through_presence
#print axioms mult_diff_visible_to_mult
#print axioms presence_merges_all_positive
#print axioms multiplicities_distinct
#print axioms two_symbols_cannot_resolve_three
#print axioms multiplicity_rung_summary

end MultRung
end PrimDiff
