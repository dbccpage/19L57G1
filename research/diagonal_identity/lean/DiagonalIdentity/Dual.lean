import Derivation.PrimDiff
import DiagonalIdentity.Covering
import DiagonalIdentity.Combinator
import DiagonalIdentity.Collapse

/-!
# Dual shapes on the declared carriers, not identity

Two obstruction shapes, named by their data:

* **Pair-id.** A map identifies a related pair, and the pushforward
  violates `Irrefl`. Non-injectivity of that map plus a protected law.
  Declared inhabitant: `D2` along `Bool → Unit`.
* **Family-miss.** A `Nat`-indexed family of sequences misses a row.
  Non-surjectivity of that family. Declared inhabitant: `diagSeq` (which
  is `diagFlip` at `flipFin`).

They are not instances of each other on those carriers: the identifying
map is not a covering family (`Bool ≠ Nat`), and a covering family is not
the `D2` constant map (`(Nat → (Nat → Fin c)) ≠ (Bool → Unit)`).  The
square-then-flip combinator packages the covering side only.  The collapse
side is a self-loop of `Push`, a relation, not a row of `diagFlip`.

This does not prove a common lemma of which both are instances.  Identity
of `PrimDiff.obstruction_under_irrefl` with `Covering.seq_uncountable`
remains not proved.

AuthorityEffect: None.
-/

namespace DiagonalIdentity.Dual

open DiagonalIdentity.Covering
open DiagonalIdentity.Combinator
open DiagonalIdentity.Collapse

/-- Local injectivity, so this module does not depend on extra libraries.
AuthorityEffect: None. -/
def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y⦄, f x = f y → x = y

/-- Local surjectivity.
AuthorityEffect: None. -/
def Surjective {α β : Type} (f : α → β) : Prop :=
  ∀ y, ∃ x, f x = y

/-- Pair-id obstruction: collision of a related pair plus `Irrefl` failure
of the pushforward.  Same data as `FidelityObstruction Irrefl`.
AuthorityEffect: None. -/
def PairIdObstruction {α β : Type} (r : α → α → Prop) (k : α → β) : Prop :=
  PrimDiff.CollapseCollision r k ∧ ¬ PrimDiff.Irrefl (PrimDiff.Push r k)

/-- Family-miss: every row of `S` differs from `d` as a sequence.
AuthorityEffect: None. -/
def FamilyMiss (c : Nat) (S : Nat → (Nat → Fin c)) (d : Nat → Fin c) : Prop :=
  ∀ n, S n ≠ d

/-- Declared recoding: the identifying map *is* a `Nat`-indexed family of
sequences.  The D2 inhabitant is not of this shape.
AuthorityEffect: None. -/
def IdentifyingMapAsCoveringFamily {α β : Type} (_k : α → β) (c : Nat) : Prop :=
  α = Nat ∧ β = (Nat → Fin c)

/-- Declared recoding: a covering family *is* the D2 constant map
`Bool → Unit`.
AuthorityEffect: None. -/
def CoveringFamilyAsD2Const {c : Nat} (_S : Nat → (Nat → Fin c)) : Prop :=
  (Nat → (Nat → Fin c)) = (Bool → Unit)

/-- The declared identifying map of the D2 inhabitant.
AuthorityEffect: None. -/
def d2Const : Bool → Unit :=
  fun _ => ()

/-! ## Cast injectivity, used only to separate declared carriers -/

theorem rec_roundtrip {α β : Type} (h : α = β) (x : α) :
    h.symm ▸ h ▸ x = x := by
  subst h
  rfl

theorem cast_injective {α β : Type} (h : α = β) :
    Injective (fun x : α => (h ▸ x : β)) := by
  intro x y hxy
  have := congrArg (fun z : β => (h.symm ▸ z : α)) hxy
  simpa [rec_roundtrip] using this

/-- `Bool` is not `Nat`: a transport `Nat → Bool` cannot be injective.
AuthorityEffect: None. -/
theorem bool_ne_nat : Bool ≠ Nat := by
  intro h
  let f : Nat → Bool := fun n => h.symm ▸ n
  have hinj : Injective f := by
    intro a b hab
    have := congrArg (fun x : Bool => (h ▸ x : Nat)) hab
    change (h ▸ (h.symm ▸ a) : Nat) = (h ▸ (h.symm ▸ b) : Nat) at this
    rw [rec_roundtrip h.symm a, rec_roundtrip h.symm b] at this
    exact this
  have pigeon : f 0 = f 1 ∨ f 0 = f 2 ∨ f 1 = f 2 := by
    cases h0 : f 0 <;> cases h1 : f 1 <;> cases h2 : f 2 <;> simp
  rcases pigeon with h01 | h02 | h12
  · exact (by decide : (0 : Nat) ≠ 1) (hinj h01)
  · exact (by decide : (0 : Nat) ≠ 2) (hinj h02)
  · exact (by decide : (1 : Nat) ≠ 2) (hinj h12)

/-- For `c ≥ 2`, `Nat → Fin c` is not a subsingleton, so not `Unit`.
AuthorityEffect: None. -/
theorem unit_ne_seq (c : Nat) (hc : 2 ≤ c) : Unit ≠ (Nat → Fin c) := by
  intro h
  let s0 : Nat → Fin c := fun _ => ⟨0, by omega⟩
  let s1 : Nat → Fin c := fun _ => ⟨1, by omega⟩
  have sne : s0 ≠ s1 := by
    intro heq
    exact Nat.zero_ne_one (Fin.mk.inj (congrFun heq 0))
  have : (h.symm ▸ s0 : Unit) = (h.symm ▸ s1 : Unit) := Subsingleton.elim _ _
  exact sne (cast_injective h.symm this)

/-- A family of sequences is not a map `Bool → Unit`.
AuthorityEffect: None. -/
theorem covering_family_type_ne_d2Const_type (c : Nat) (hc : 2 ≤ c) :
    (Nat → (Nat → Fin c)) ≠ (Bool → Unit) := by
  intro h
  let s0 : Nat → (Nat → Fin c) := fun _ _ => ⟨0, by omega⟩
  let s1 : Nat → (Nat → Fin c) := fun _ _ => ⟨1, by omega⟩
  have sne : s0 ≠ s1 := by
    intro heq
    exact Nat.zero_ne_one (Fin.mk.inj (congrFun (congrFun heq 0) 0))
  have : (h ▸ s0 : Bool → Unit) = (h ▸ s1 : Bool → Unit) := by
    funext
    exact Subsingleton.elim _ _
  exact sne (cast_injective h this)

/-! ## Pair-id side: non-injectivity plus protected law -/

theorem pair_id_iff_fidelity {α β : Type} {r : α → α → Prop} {k : α → β} :
    PairIdObstruction r k ↔ PrimDiff.FidelityObstruction PrimDiff.Irrefl r k :=
  Iff.rfl

theorem d2Const_not_injective : ¬ Injective d2Const := by
  intro hinj
  have : (false : Bool) = true := hinj rfl
  exact Bool.noConfusion this

theorem d2Const_pair_id : PairIdObstruction PrimDiff.D2 d2Const :=
  d2_constant_obstructs

theorem d2Const_not_as_covering_family (c : Nat) :
    ¬ IdentifyingMapAsCoveringFamily d2Const c := by
  rintro ⟨hα, _⟩
  exact bool_ne_nat hα

theorem d2Const_push_self_loop :
    PrimDiff.Push PrimDiff.D2 d2Const () () :=
  identifying_push_self_loop PrimDiff.D2_witness (rfl : d2Const false = d2Const true)

/-! ## Family-miss side: non-surjectivity; combinator is diagFlip -/

theorem family_miss_diagSeq (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) :
    FamilyMiss c S (diagSeq c hc S) := by
  intro n hn
  exact diagSeq_diff_at c hc S n (congrFun hn n).symm

theorem family_not_surjective (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) :
    ¬ Surjective S := by
  intro hsurj
  obtain ⟨d, hd⟩ := seq_uncountable c hc S
  obtain ⟨n, rfl⟩ := hsurj d
  exact hd n rfl

theorem family_not_as_d2_const (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) :
    ¬ CoveringFamilyAsD2Const S :=
  covering_family_type_ne_d2Const_type c hc

theorem covering_miss_witness_is_diagFlip
    (c : Nat) (hc : 2 ≤ c) (S : Nat → (Nat → Fin c)) :
    diagSeq c hc S = diagFlip (flipFin c hc) S :=
  diagSeq_is_diagFlip c hc S

/-! ## Dual package: both shapes, neither recodes the other, combinator
    only on the covering side -/

/-- On the declared carriers: pair-id at `D2`/`d2Const` (not injective, not
a covering family) and family-miss at `diagSeq` (not surjective, not the
D2 constant map, and equal to `diagFlip`).
AuthorityEffect: None. -/
theorem dual_on_declared_carriers (c : Nat) (hc : 2 ≤ c)
    (S : Nat → (Nat → Fin c)) :
    PairIdObstruction PrimDiff.D2 d2Const ∧
    ¬ Injective d2Const ∧
    ¬ IdentifyingMapAsCoveringFamily d2Const c ∧
    PrimDiff.Push PrimDiff.D2 d2Const () () ∧
    FamilyMiss c S (diagSeq c hc S) ∧
    ¬ Surjective S ∧
    ¬ CoveringFamilyAsD2Const S ∧
    diagSeq c hc S = diagFlip (flipFin c hc) S :=
  ⟨d2Const_pair_id,
   d2Const_not_injective,
   d2Const_not_as_covering_family c,
   d2Const_push_self_loop,
   family_miss_diagSeq c hc S,
   family_not_surjective c hc S,
   family_not_as_d2_const c hc S,
   covering_miss_witness_is_diagFlip c hc S⟩

end DiagonalIdentity.Dual
