import FreshCharacters.Steps

/-!
# The layer's characters, and the fresh total's exponent record

Stage 1 of the fresh_characters run.  Every theorem in this file originates
here.

A layer of part count `n` has members `0..n-1` and a step action already
defined by the pinned sibling: `Steps.repAdd a c` has value `a * c % n`
(`Steps.repAdd_val`).  A CHARACTER of that layer, into a declared value
carrier with a distinguished element and one operation, is a map from the
members that turns each step into the carrier's operation.  Such a map is
determined by where it sends the unit member, and the whole of it is
recorded by the EXPONENT WORD `c |-> a * c % n`: whichever carrier is
chosen, the character indexed by step `a` sends member `c` to the carrier's
generator raised along that exponent.  Everything below is therefore stated
about the exponent word, which is carrier-free, and the carrier-specific
statements are the two obstruction theorems at the end.

The FRESH TOTAL at step `a` is the sum, over the fresh members, of those
values.  Its carrier-free record is the exponent multiset `freshExp n a`.

Nothing here claims a total equals anything; that is stage 2, and it is
computed, not asserted.  AuthorityEffect: None.
-/

namespace FreshCharacters
namespace Char

open Balance

/-! ## The members and the exponent word -/

/-- The fresh members of the layer of part count `n`, in increasing order.
Definitionally the list the pinned `freshCount` measures. -/
def freshMembers (n : Nat) : List Nat :=
  (List.range n).filter (fun j => Nat.gcd j n == 1)

/-- The fresh members are exactly what the pinned fresh count counts. -/
theorem freshMembers_length (n : Nat) :
    (freshMembers n).length = freshCount n := rfl

/-- The exponent word of the character indexed by step `a`, read at member
`c`: the layer's own step action on values (`Steps.repAdd_val`). -/
def exponent (n a c : Nat) : Nat := a * c % n

/-- The exponent word IS the pinned step action, read on values. -/
theorem exponent_eq_repAdd {k : Nat} (a : Nat) (c : Fin (k + 1)) :
    exponent (k + 1) a c.val = (Steps.repAdd a c).val :=
  (Steps.repAdd_val a c).symm

/-- The exponent multiset of the fresh total at step `a`. -/
def freshExp (n a : Nat) : List Nat := (freshMembers n).map (exponent n a)

/-! ## characters_are_steps -/

/-- Distinct steps below the part count give distinct characters: the
exponent word at the unit member already separates them. -/
theorem exponent_step_injective {n a b : Nat} (ha : a < n) (hb : b < n)
    (h : ∀ c, exponent n a c = exponent n b c) : a = b := by
  have h1 := h 1
  simp only [exponent, Nat.mul_one] at h1
  rwa [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at h1

/-- A character of the layer of part count `n`, stated carrier-free on its
exponent word: values are members, the zero member is fixed, and the step
structure is respected. -/
def IsCharacter (n : Nat) (f : Nat → Nat) : Prop :=
  (∀ c, f c < n) ∧ f 0 = 0 ∧ ∀ c d, f ((c + d) % n) = (f c + f d) % n

/-- Every step below a positive part count supplies a character.  This is
the construction half needed before injectivity and exhaustion can justify
the exact count. -/
theorem exponent_is_character {n a : Nat} (hn : 0 < n) :
    IsCharacter n (exponent n a) := by
  constructor
  · intro c
    exact Nat.mod_lt _ hn
  constructor
  · simp [exponent]
  · intro c d
    simp only [exponent]
    rw [Nat.mul_mod_mod, Nat.mul_add, Nat.add_mod]

/-- Every character is the exponent word of exactly one step: the value at
the unit member. -/
theorem character_determined_by_unit {n : Nat} {f : Nat → Nat}
    (hf : IsCharacter n f) : ∀ c, c < n → f c = exponent n (f 1) c := by
  obtain ⟨hlt, hzero, hadd⟩ := hf
  intro c
  induction c with
  | zero => intro _; simpa [exponent] using hzero
  | succ m ih =>
    intro hm
    have hn : 0 < n := by omega
    have hmlt : m < n := Nat.lt_of_succ_lt hm
    have hmod : (m + 1) % n = m + 1 := Nat.mod_eq_of_lt hm
    have hstep : f (m + 1) = (f m + f 1) % n := by
      have := hadd m 1
      rwa [hmod] at this
    rw [hstep, ih hmlt]
    show (f 1 * m % n + f 1) % n = f 1 * (m + 1) % n
    have e1 : f 1 * (m + 1) % n = (f 1 * m % n + f 1 % n) % n := by
      rw [Nat.mul_add, Nat.mul_one, Nat.add_mod]
    have e2 : (f 1 * m % n + f 1) % n = (f 1 * m % n % n + f 1 % n) % n := by
      rw [Nat.add_mod]
    rw [e1, e2, Steps.mod_idem (f 1 * m) n hn]

/-- The count of characters of the layer of part count `n` is `n`: the steps
are `0..n-1`, they are pairwise distinct as characters, and every character
is one of them. -/
theorem characters_are_steps (n : Nat) :
    (List.range n).length = n
      ∧ (∀ a, a < n → IsCharacter n (exponent n a))
      ∧ (∀ a b, a < n → b < n → (∀ c, exponent n a c = exponent n b c) → a = b)
      ∧ (∀ f, IsCharacter n f → ∀ c, c < n → f c = exponent n (f 1) c) :=
  ⟨List.length_range,
   fun _ ha => exponent_is_character (Nat.zero_lt_of_lt ha),
   fun _ _ ha hb h => exponent_step_injective ha hb h,
   fun _ hf => character_determined_by_unit hf⟩

/-! ## character_trivial_total -/

theorem map_const_replicate {α β : Type} (l : List α) (b : β) :
    l.map (fun _ => b) = List.replicate l.length b := by
  induction l with
  | nil => rfl
  | cons _ xs ih => simp [List.replicate, ih]

/-- The exponent word of the step-zero character is constantly the zero
member. -/
theorem exponent_zero_step (n c : Nat) : exponent n 0 c = 0 := by
  simp [exponent]

/-- character_trivial_total: the fresh total at step zero is the fresh count
many copies of the carrier's distinguished element -- so under any carrier
whose operation counts, that total IS the fresh count. -/
theorem freshExp_zero (n : Nat) :
    freshExp n 0 = List.replicate (freshCount n) 0 := by
  have hfun : (fun c => exponent n 0 c) = (fun _ : Nat => 0) := by
    funext c; exact exponent_zero_step n c
  show (freshMembers n).map (fun c => exponent n 0 c) = _
  rw [hfun, map_const_replicate, freshMembers_length]

/-! ## the counting law -/

/-- The counting hom: whatever the step, the fresh total has exactly the
fresh count many terms.  This is the carrier-free half of `V2`, the carrier
in which every character value is the unit. -/
theorem freshExp_length (n a : Nat) : (freshExp n a).length = freshCount n := by
  show ((freshMembers n).map (exponent n a)).length = freshCount n
  rw [List.length_map, freshMembers_length]

/-! ## character_restricts -/

/-- character_restricts: a character of the larger layer, read along the
divisor arrow that embeds the layer of part count `d` into the layer of part
count `n`, is the corresponding character of the smaller layer, scaled by the
arrow.  Stated on exponent words, where it is an exact identity. -/
theorem exponent_embed {n d a c : Nat} (hd : 0 < d) (h : n % d = 0) :
    exponent n a (c * (n / d)) = (n / d) * exponent d a c := by
  have hdvd : d ∣ n := Nat.dvd_of_mod_eq_zero h
  have hn : n / d * d = n := Nat.div_mul_cancel hdvd
  have key : ∀ q, q * d = n → a * (c * q) % n = q * (a * c % d) := by
    intro q hqd
    subst hqd
    rw [show a * (c * q) = q * (a * c) from by
          rw [← Nat.mul_assoc, Nat.mul_comm (a * c) q],
      Nat.mul_mod_mul_left]
  show a * (c * (n / d)) % n = (n / d) * (a * c % d)
  exact key (n / d) hn

/-! ## character_total_wf -/

/-- character_total_wf: the fresh total is a function of the receiver
element, not of the fresh representation chosen for it.  Rides entirely on
the pinned `fresh_rep_unique`. -/
theorem freshExp_wf {k k' : Nat} {c : Fin (k + 1)} {c' : Fin (k' + 1)} (a : Nat)
    (hf : FreshAt k c) (hf' : FreshAt k' c')
    (h : Receiver.layer k c = Receiver.layer k' c') :
    freshExp (k + 1) a = freshExp (k' + 1) a := by
  have hk := (fresh_rep_unique hf hf' h).1
  rw [hk]

/-! ## the two carrier obstructions

Both are stage-1 findings about menu members, and both are recorded rather
than used to drop a member. -/

/-- In an ADDITIVE carrier -- one whose distinguished element absorbs the
operation, as the receiver's zero does -- the step-zero character sends every
member to that element, so its fresh total is that element. -/
theorem additive_step_zero_total {V : Type} (zero : V) (op : V → V → V)
    (h_op : op zero zero = zero) (l : List Nat) :
    (l.map (fun _ => zero)).foldr op zero = zero := by
  induction l with
  | nil => rfl
  | cons _ xs ih => show op zero ((xs.map (fun _ => zero)).foldr op zero) = zero
                    rw [ih]; exact h_op

/-- The V1 obstruction, stated for the integers under addition, which is the
receiver's own operation in miniature: the step-zero fresh total is the
carrier's zero and NOT the fresh count, whenever the layer has a fresh
member.  So a carrier whose character values are added cannot satisfy
`character_trivial_total`; a carrier whose character values are composed and
whose totals are added can. -/
theorem additive_trivial_total_ne_freshCount (n : Nat) (h : 0 < freshCount n) :
    ((freshMembers n).map (fun _ => (0 : Int))).foldr (· + ·) 0
      ≠ (freshCount n : Int) := by
  rw [additive_step_zero_total (0 : Int) (· + ·) (by decide)]
  intro hcontra
  have : (0 : Nat) = freshCount n := Int.ofNat_inj.mp hcontra
  omega

end Char
end FreshCharacters
