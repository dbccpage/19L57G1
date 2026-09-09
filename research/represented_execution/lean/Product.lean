import Control

/-!
# Product: two loci of activity, and what makes them interact

Every process of this family so far has **one** locus: one active datum that
one firing moves.  The consumer families record that as a limit — no
independence and no interaction between two loci can be stated of a process
that has one.  This module builds the second locus.

A product datum carries both: `pack m a b = m * a + b` encodes the pair, and
`fstOf`/`sndOf` read the coordinates back.  A finite setting `F` and a finite
setting `G` give a product setting `prodSetting F G` on `F.n * G.n` data whose
operations are `F`'s acting on the first coordinate (`leftOp`) and `G`'s acting
on the second (`rightOp`).  It is a finite setting of the merged class
(`prodSetting`), so the merged encoder represents it and the control machine
runs it with no change at all: two loci are a *datum* here, not a new machine.

What is proved:

* **The independence square.**  A move at one locus and a move at the other
  commute, for any two operations, provided the second keeps its own
  coordinate in range (`left_right_comm`).  This is the two-update square the
  observing family recorded as not built.
* **Interaction is what reading both coordinates buys.**  A coupled move —
  one that reads the second locus to decide the first — does not commute with
  a move at the second locus (`coupling_breaks_the_square`).  So the square is
  a property of the *product* structure, not of the machine, and it fails
  exactly when an operation stops being local to its locus.
* **The loci are genuinely two.**  A left move changes only the first
  coordinate and a right move only the second (`leftOp_snd`, `rightOp_fst`).

AuthorityEffect: None.
-/

namespace Product

open Derivation Translation Control

/-! ## 1. Packing two loci into one datum -/

/-- The datum carrying the pair `(a, b)` when the second locus has `m` data. -/
def pack (m a b : Nat) : Nat := m * a + b

/-- The first locus of a product datum. -/
def fstOf (m x : Nat) : Nat := x / m

/-- The second locus of a product datum. -/
def sndOf (m x : Nat) : Nat := x % m

theorem fst_pack {m a b : Nat} (hm : 0 < m) (h : b < m) : fstOf m (pack m a b) = a := by
  show (m * a + b) / m = a
  rw [Nat.mul_add_div hm, Nat.div_eq_of_lt h]
  rfl

theorem snd_pack {m a b : Nat} (h : b < m) : sndOf m (pack m a b) = b := by
  show (m * a + b) % m = b
  rw [Nat.mul_add_mod, Nat.mod_eq_of_lt h]

theorem pack_lt {m n a b : Nat} (ha : a < n) (hb : b < m) : pack m a b < n * m := by
  have hexp : m * (a + 1) = m * a + m := Nat.mul_succ m a
  have hle : m * (a + 1) ≤ m * n := Nat.mul_le_mul_left m ha
  have hcomm : n * m = m * n := Nat.mul_comm n m
  show m * a + b < n * m
  omega

/-- The first locus of an admitted product datum is admitted.  Proved from
`Nat.div_mul_le_self` and a decidable comparison, rather than through
`Nat.div_lt_of_lt_mul` or `Nat.lt_of_mul_lt_mul_left`, both of which the axiom
census reported as relying on `Classical.choice`. -/
theorem fst_lt {m n x : Nat} (hx : x < n * m) : fstOf m x < n := by
  show x / m < n
  have h1 : x / m * m ≤ x := Nat.div_mul_le_self x m
  have h2 : x / m * m < n * m := Nat.lt_of_le_of_lt h1 hx
  rcases Nat.lt_or_ge (x / m) n with h | h
  · exact h
  · exact absurd (Nat.mul_le_mul_right m h) (by omega)

theorem snd_lt {m x : Nat} (hm : 0 < m) : sndOf m x < m := Nat.mod_lt x hm

/-! ## 2. The two families of moves -/

/-- A move at the first locus: apply `f` there, keep the second. -/
def leftOp (m : Nat) (f : Nat → Nat) (x : Nat) : Nat := pack m (f (fstOf m x)) (sndOf m x)

/-- A move at the second locus: apply `g` there, keep the first. -/
def rightOp (m : Nat) (g : Nat → Nat) (x : Nat) : Nat := pack m (fstOf m x) (g (sndOf m x))

/-- A left move leaves the second locus alone. -/
theorem leftOp_snd {m : Nat} (hm : 0 < m) (f : Nat → Nat) (x : Nat) :
    sndOf m (leftOp m f x) = sndOf m x :=
  snd_pack (snd_lt hm)

/-- A right move leaves the first locus alone. -/
theorem rightOp_fst {m : Nat} (hm : 0 < m) (g : Nat → Nat)
    (hg : ∀ b, b < m → g b < m) (x : Nat) : fstOf m (rightOp m g x) = fstOf m x :=
  fst_pack hm (hg _ (snd_lt hm))

/-- **The independence square.**  A move at one locus and a move at the other
commute.  Nothing is asked of the first operation; the second has only to keep
its own coordinate in range, which every operation of a finite setting does. -/
theorem left_right_comm {m : Nat} (hm : 0 < m) (f g : Nat → Nat)
    (hg : ∀ b, b < m → g b < m) (x : Nat) :
    leftOp m f (rightOp m g x) = rightOp m g (leftOp m f x) := by
  have hB : sndOf m x < m := snd_lt hm
  have hgB : g (sndOf m x) < m := hg _ hB
  show pack m (f (fstOf m (pack m (fstOf m x) (g (sndOf m x)))))
        (sndOf m (pack m (fstOf m x) (g (sndOf m x))))
      = pack m (fstOf m (pack m (f (fstOf m x)) (sndOf m x)))
        (g (sndOf m (pack m (f (fstOf m x)) (sndOf m x))))
  rw [fst_pack hm hgB, snd_pack hgB, fst_pack hm hB, snd_pack hB]

/-! ## 3. The product setting -/

/-- The product of two finite settings: the pairs as data, `F`'s operations at
the first locus and `G`'s at the second, no store, the endpoints paired. -/
def prodSetting (F G : FiniteSetting) : FiniteSetting where
  n := F.n * G.n
  rel := fun _ _ => false
  ret := fun _ _ => false
  prot := fun _ _ => false
  a := pack G.n F.a G.a
  b := pack G.n F.b G.b
  ops := F.ops.map (leftOp G.n) ++ G.ops.map (rightOp G.n)
  a_lt := pack_lt F.a_lt G.a_lt
  b_lt := pack_lt F.b_lt G.b_lt
  ops_closed := by
    have hm : 0 < G.n := Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt
    intro h hh x hx
    rcases List.mem_append.mp hh with hl | hr
    · obtain ⟨f, hf, rfl⟩ := List.mem_map.mp hl
      exact pack_lt (F.ops_closed f hf _ (fst_lt hx)) (snd_lt hm)
    · obtain ⟨g, hg, rfl⟩ := List.mem_map.mp hr
      exact pack_lt (fst_lt hx) (G.ops_closed g hg _ (snd_lt hm))

theorem prodSetting_n (F G : FiniteSetting) : (prodSetting F G).n = F.n * G.n := rfl

/-- The two loci are separately visible in the product's operations: a left
move keeps the second coordinate, a right move keeps the first. -/
theorem prod_left_local (F G : FiniteSetting) {h : Nat → Nat}
    (hh : h ∈ F.ops.map (leftOp G.n)) (x : Nat) : sndOf G.n (h x) = sndOf G.n x := by
  obtain ⟨f, -, rfl⟩ := List.mem_map.mp hh
  exact leftOp_snd (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) f x

theorem prod_right_local (G : FiniteSetting) {h : Nat → Nat}
    (hh : h ∈ G.ops.map (rightOp G.n)) (x : Nat) : fstOf G.n (h x) = fstOf G.n x := by
  obtain ⟨g, hg, rfl⟩ := List.mem_map.mp hh
  exact rightOp_fst (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) g
    (fun b hb => G.ops_closed g hg b hb) x

/-- **The square, for the product setting's own operations.** -/
theorem prod_comm (F G : FiniteSetting) {f g : Nat → Nat} (hf : f ∈ F.ops) (hg : g ∈ G.ops)
    (x : Nat) : leftOp G.n f (rightOp G.n g x) = rightOp G.n g (leftOp G.n f x) :=
  left_right_comm (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) f g
    (fun b hb => G.ops_closed g hg b hb) x

/-! ## 4. What interaction costs: a move that reads both loci -/

/-- A coupled move: it reads the second locus to decide the first.  It is not
of the form `leftOp` or `rightOp`, and that is the whole difference. -/
def coupleOp (m : Nat) (x : Nat) : Nat := pack m (sndOf m x) (sndOf m x)

/-- The two-point flip. -/
def flip (b : Nat) : Nat := if b = 0 then 1 else 0

/-- **Interaction breaks the square.**  On two two-point loci, the coupled
move and a move at the second locus do not commute: reading the other locus is
exactly what independence forbids. -/
theorem coupling_breaks_the_square :
    coupleOp 2 (rightOp 2 flip 0) ≠ rightOp 2 flip (coupleOp 2 0) := by decide

/-- And the square does hold there for the uncoupled pair, so the failure is
the coupling and not the carrier. -/
theorem uncoupled_square_holds (x : Nat) :
    leftOp 2 flip (rightOp 2 flip x) = rightOp 2 flip (leftOp 2 flip x) :=
  left_right_comm (by decide) flip flip (by decide) x

end Product

#print axioms Product.fst_pack
#print axioms Product.snd_pack
#print axioms Product.pack_lt
#print axioms Product.fst_lt
#print axioms Product.snd_lt
#print axioms Product.leftOp_snd
#print axioms Product.rightOp_fst
#print axioms Product.left_right_comm
#print axioms Product.prodSetting_n
#print axioms Product.prod_left_local
#print axioms Product.prod_right_local
#print axioms Product.prod_comm
#print axioms Product.coupling_breaks_the_square
#print axioms Product.uncoupled_square_holds
