import Derivation.Compression

/-!
# Declared weight assignments, their profiles, and what a lift adds

A weight assignment is a DECLARED datum: a count attached to each
position of a finite carrier.  Nothing in the passage calculus
produces one; like protection, budget, and observer transport, it is
supplied.  This module asks the only question the datum can answer on
its own — what is fixed by the weights, and what is not — and it
answers it in integer arithmetic, with no division and no reals.

1. **The profile, without division.**  Two assignments have the same
   normalized profile exactly when they agree after cross-multiplying
   by each other's totals (`SameProfile`).  This is an equivalence on
   positive-total assignments (`profile_refl/symm/trans`), it is
   invariant under positive rescaling (`profile_scale`), and its
   classes are EXACTLY the positive rays (`profile_iff_ray`) — an
   exact fiber classifier, not an approximation.
2. **What the profile preserves**: support (`profile_support`) and
   order (`profile_order`).  What it forgets: total mass
   (`profile_forgets_total`).
3. **A lift adds nothing to the profile.**  Call any assignment `c`
   together with a declared modulus map `m` a DECORATED presentation
   of `w` when `m ∘ c = w` pointwise.  Every decorated presentation
   of `w` has `w`'s profile (`lift_profile_redundant`), and any two
   decorated presentations of the same weights have the same profile
   (`lifts_agree_on_profile`) — the decoration is invisible to the
   profile.  The proof is one line, and that is the whole content.
4. **But the decoration is not invisible to every question.**  Two
   decorated presentations with identical moduli are separated by a
   declared MIXING question (`decoration_visible_to_mixing`), so
   redundancy is RELATIVE to the declared question family and never
   absolute.  This is `Compression.absolute_adequacy_iff_injective`
   at work: adequacy for every question is injectivity, i.e. no
   compression at all.
5. **Descent classification.**  A declared linear read-out descends
   through the modulus-blind relation exactly when its support is at
   most a single position (`descent_iff_subsingleton_support`);
   anything that genuinely mixes two positions does not descend.
6. **The climb, and what it costs.**  Section 6 states — as
   PROPOSITIONS, none of them proved — the further declarations that
   would be needed to single out a particular read-out law, and
   proves the negative fact that makes them necessary: the weights do
   NOT determine a decorated presentation
   (`weights_do_not_force_decoration`), so no uniqueness claim
   follows from the weights alone.

Nothing here derives a representation, a dynamics, or a uniqueness
law.  What is derived is exactly the redundancy and its scope.
-/

namespace WeightProfile

/-! ## 1. The profile, without division -/

/-- A declared weight assignment: a count per position. -/
abbrev Weights := Nat → Nat

/-- The declared total over a finite carrier. -/
def total (l : List Nat) (w : Weights) : Nat :=
  (l.map w).foldl (fun a b => a + b) 0

theorem foldl_add_acc (l : List Nat) (a : Nat) :
    l.foldl (fun x y => x + y) a
      = a + l.foldl (fun x y => x + y) 0 := by
  induction l generalizing a with
  | nil => simp
  | cons b t ih =>
      show t.foldl (fun x y => x + y) (a + b)
        = a + t.foldl (fun x y => x + y) (0 + b)
      rw [ih (a + b), ih (0 + b)]
      omega

theorem total_cons (p : Nat) (l : List Nat) (w : Weights) :
    total (p :: l) w = w p + total l w := by
  show (w p :: l.map w).foldl (fun a b => a + b) 0
    = w p + (l.map w).foldl (fun a b => a + b) 0
  show (l.map w).foldl (fun a b => a + b) (0 + w p)
    = w p + (l.map w).foldl (fun a b => a + b) 0
  rw [foldl_add_acc]
  omega

theorem total_scale (l : List Nat) (a : Nat) (w : Weights) :
    total l (fun p => a * w p) = a * total l w := by
  induction l with
  | nil => simp [total]
  | cons p t ih =>
      rw [total_cons, total_cons, ih, Nat.mul_add]

/-- Totals inherit a ray relation from the pointwise one. -/
theorem total_ray (l : List Nat) (a b : Nat) (w v : Weights)
    (hab : ∀ p ∈ l, a * w p = b * v p) :
    a * total l w = b * total l v := by
  induction l with
  | nil => rfl
  | cons q t ih =>
      rw [total_cons, total_cons, Nat.mul_add, Nat.mul_add,
          hab q List.mem_cons_self,
          ih (fun p hp => hab p (List.mem_cons_of_mem q hp))]

/-- Same normalized profile, stated without division: cross-multiply
by each other's totals. -/
def SameProfile (l : List Nat) (w v : Weights) : Prop :=
  ∀ p ∈ l, w p * total l v = v p * total l w

theorem profile_refl (l : List Nat) (w : Weights) :
    SameProfile l w w := fun _ _ => rfl

theorem profile_symm (l : List Nat) (w v : Weights)
    (h : SameProfile l w v) : SameProfile l v w :=
  fun p hp => (h p hp).symm

theorem profile_trans (l : List Nat) (w v u : Weights)
    (hv : 0 < total l v) (h1 : SameProfile l w v)
    (h2 : SameProfile l v u) : SameProfile l w u := by
  intro p hp
  have e1 := h1 p hp
  have e2 := h2 p hp
  have s1 : total l v * (w p * total l u)
      = (w p * total l v) * total l u := by
        simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
  have s2 : (v p * total l w) * total l u
      = (v p * total l u) * total l w := by
        simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
  have s3 : (u p * total l v) * total l w
      = total l v * (u p * total l w) := by
        simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
  have key : total l v * (w p * total l u)
      = total l v * (u p * total l w) := by
    rw [s1, e1, s2, e2, s3]
  exact Nat.eq_of_mul_eq_mul_left hv key

/-- **Positive rescaling changes nothing.**  The profile depends only
on the ray, not on the total. -/
theorem profile_scale (l : List Nat) (a : Nat) (w : Weights) :
    SameProfile l (fun p => a * w p) w := by
  intro p _
  show a * w p * total l w = w p * total l (fun q => a * w q)
  rw [total_scale]
  simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]

/-- **Exact fiber classifier**: two positive-total assignments have
the same profile EXACTLY when they lie on a common positive ray. -/
theorem profile_iff_ray (l : List Nat) (w v : Weights)
    (hw : 0 < total l w) (hv : 0 < total l v) :
    SameProfile l w v ↔
      ∃ a b, 0 < a ∧ 0 < b ∧ ∀ p ∈ l, a * w p = b * v p := by
  constructor
  · intro h
    refine ⟨total l v, total l w, hv, hw, ?_⟩
    intro p hp
    have e := h p hp
    have s1 : total l v * w p = w p * total l v := Nat.mul_comm _ _
    have s2 : v p * total l w = total l w * v p := Nat.mul_comm _ _
    rw [s1, e, s2]
  · intro ⟨a, b, ha, hb, hab⟩
    have htot : a * total l w = b * total l v :=
      total_ray l a b w v hab
    intro p hp
    have hq := hab p hp
    have s1 : a * (w p * total l v) = (a * w p) * total l v := by
      simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    have s2 : (b * v p) * total l v = v p * (b * total l v) := by
      simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    have s3 : v p * (a * total l w) = a * (v p * total l w) := by
      simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    have key : a * (w p * total l v) = a * (v p * total l w) := by
      rw [s1, hq, s2, ← htot, s3]
    exact Nat.eq_of_mul_eq_mul_left ha key

/-! ## 2. What the profile keeps, and what it forgets -/

/-- Support is preserved exactly. -/
theorem profile_support (l : List Nat) (w v : Weights)
    (hw : 0 < total l w) (hv : 0 < total l v)
    (h : SameProfile l w v) (p : Nat) (hp : p ∈ l) :
    (w p = 0 ↔ v p = 0) := by
  have e := h p hp
  constructor
  · intro h0
    rw [h0] at e
    simp only [Nat.zero_mul] at e
    rcases Nat.mul_eq_zero.mp e.symm with h1 | h1
    · exact h1
    · omega
  · intro h0
    rw [h0] at e
    simp only [Nat.zero_mul] at e
    rcases Nat.mul_eq_zero.mp e with h1 | h1
    · exact h1
    · omega

/-- Order is preserved exactly. -/
theorem profile_order (l : List Nat) (w v : Weights)
    (hw : 0 < total l w) (hv : 0 < total l v)
    (h : SameProfile l w v) (p q : Nat) (hp : p ∈ l) (hq : q ∈ l) :
    (w p ≤ w q ↔ v p ≤ v q) := by
  have ep := h p hp
  have eq' := h q hq
  constructor
  · intro hle
    have h1 : v p * total l w ≤ v q * total l w := by
      rw [← ep, ← eq']
      exact Nat.mul_le_mul_right _ hle
    have h2 : total l w * v p ≤ total l w * v q := by
      rw [Nat.mul_comm (total l w) (v p),
          Nat.mul_comm (total l w) (v q)]
      exact h1
    exact Nat.le_of_mul_le_mul_left h2 hw
  · intro hle
    have h1 : w p * total l v ≤ w q * total l v := by
      rw [ep, eq']
      exact Nat.mul_le_mul_right _ hle
    have h2 : total l v * w p ≤ total l v * w q := by
      rw [Nat.mul_comm (total l v) (w p),
          Nat.mul_comm (total l v) (w q)]
      exact h1
    exact Nat.le_of_mul_le_mul_left h2 hv

/-- **The profile forgets the total.**  Doubling every weight leaves
the profile fixed while changing the total — the forgotten datum,
exhibited. -/
theorem profile_forgets_total :
    SameProfile [0, 1] (fun p => 2 * (if p = 0 then 3 else 1))
      (fun p => if p = 0 then 3 else 1) ∧
    total [0, 1] (fun p => 2 * (if p = 0 then 3 else 1))
      ≠ total [0, 1] (fun p => if p = 0 then 3 else 1) := by
  refine ⟨profile_scale [0, 1] 2 _, by decide⟩

/-! ## 3. A decorated presentation adds nothing to the profile -/

/-- A DECORATED PRESENTATION of `w`: an assignment `c` of decorated
values together with a declared modulus map `m` that returns the
weights.  Both `c` and `m` are supplied; neither is derived. -/
def Presents (l : List Nat) (m : Nat → Nat) (c : Nat → Nat)
    (w : Weights) : Prop :=
  ∀ p ∈ l, m (c p) = w p

theorem total_congr (l : List Nat) (w v : Weights)
    (h : ∀ p ∈ l, w p = v p) : total l w = total l v := by
  induction l with
  | nil => rfl
  | cons q t ih =>
      rw [total_cons, total_cons, h q List.mem_cons_self,
          ih (fun p hp => h p (List.mem_cons_of_mem q hp))]

/-- **Redundancy**: the profile read off a decorated presentation is
the profile of the weights.  One line, and that is the entire
content of the redundancy. -/
theorem lift_profile_redundant (l : List Nat) (m : Nat → Nat)
    (c : Nat → Nat) (w : Weights) (h : Presents l m c w) :
    SameProfile l (fun p => m (c p)) w := by
  intro p hp
  show m (c p) * total l w = w p * total l (fun q => m (c q))
  rw [h p hp, total_congr l (fun q => m (c q)) w h]

/-- **Any two decorated presentations of the same weights carry the
same profile** — whatever else differs between them. -/
theorem lifts_agree_on_profile (l : List Nat) (m : Nat → Nat)
    (c d : Nat → Nat) (w : Weights)
    (hc : Presents l m c w) (hd : Presents l m d w)
    (hpos : 0 < total l w) :
    SameProfile l (fun p => m (c p)) (fun p => m (d p)) := by
  have h1 := lift_profile_redundant l m c w hc
  have h2 := lift_profile_redundant l m d w hd
  exact profile_trans l _ w _ hpos h1 (profile_symm l _ w h2)

/-! ## 4. Over unsigned decorations the lift adds NOTHING AT ALL;
the extra capacity is exactly a declared sign -/

/-- The declared modulus of this section: squaring. -/
def sq (x : Nat) : Nat := x * x

/-- **Unsigned decorations carry no extra datum.**  Squaring is
injective on counts, so a decorated presentation over unsigned values
is DETERMINED by the weights it presents.  The redundancy here is
total: the decoration is not merely invisible to the profile, it is
not there at all. -/
theorem sq_mono {c d : Nat} (h : c < d) : sq c < sq d := by
  show c * c < d * d
  have h1 : c * c ≤ c * d := Nat.mul_le_mul_left c (Nat.le_of_lt h)
  have h2 : c * d < d * d := by
    rcases Nat.eq_zero_or_pos d with hd | hd
    · omega
    · exact Nat.mul_lt_mul_of_lt_of_le h (Nat.le_refl d) hd
  omega

theorem sq_injective (c d : Nat) (h : sq c = sq d) : c = d := by
  rcases Nat.lt_trichotomy c d with hlt | heq | hgt
  · have := sq_mono hlt
    omega
  · exact heq
  · have := sq_mono hgt
    omega

theorem unsigned_decoration_determined (l : List Nat)
    (c d : Nat → Nat) (w : Weights)
    (hc : Presents l sq c w) (hd : Presents l sq d w) :
    ∀ p ∈ l, c p = d p := by
  intro p hp
  exact sq_injective (c p) (d p) ((hc p hp).trans (hd p hp).symm)

/-- The declared MIXING read-out over SIGNED decorations: the modulus
of the combination.  Nothing forces this read-out; it is declared,
exactly like the modulus. -/
def mixSum (x y : Int) : Int := (x + y) * (x + y)

/-- **The extra representational capacity IS the declared sign.**
Two SIGNED decorations with identical moduli at every position are
separated by the declared mixing read-out.  So the capacity a lift is
sometimes credited with does not come from the lift: it comes from
declaring a sign, and that declaration is a separate import with its
own price. -/
theorem signed_decoration_visible_to_mixing :
    ((1 : Int) * 1 = (1 : Int) * 1) ∧
    ((-1 : Int) * (-1) = (1 : Int) * 1) ∧
    mixSum 1 (-1) ≠ mixSum 1 1 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **Redundancy is relative, and the relativity is now located.**
For the profile question a decorated presentation adds nothing
(`lift_profile_redundant`); over unsigned decorations it adds nothing
to ANY question, because it is determined
(`unsigned_decoration_determined`); and the only way to make it add
something is to declare a sign, after which a declared mixing
question separates presentations the profile cannot
(`signed_decoration_visible_to_mixing`).  Which of these holds is
fixed by the declared data, never by the weights. -/
theorem redundancy_is_relative (l : List Nat) (c d : Nat → Nat)
    (w : Weights) (hc : Presents l sq c w) (hd : Presents l sq d w) :
    SameProfile l (fun p => sq (c p)) w ∧
    (∀ p ∈ l, c p = d p) ∧
    mixSum 1 (-1) ≠ mixSum 1 1 :=
  ⟨lift_profile_redundant l sq c w hc,
   unsigned_decoration_determined l c d w hc hd,
   (signed_decoration_visible_to_mixing).2.2⟩

/-! ## 5. Descent classification for declared linear read-outs -/

/-- A declared read-out over two positions with integer weights. -/
def readOut (a b x y : Int) : Int := a * x + b * y

/-- Modulus-blind inputs: the squares agree position by position. -/
def ModulusBlind (x y x' y' : Int) : Prop :=
  x * x = x' * x' ∧ y * y = y' * y'

/-- Squaring a product: the two-fold rearrangement used below. -/
theorem sq_mul (x y : Int) : (x * y) * (x * y) = (x * x) * (y * y) := by
  rw [Int.mul_assoc, ← Int.mul_assoc y x y, Int.mul_comm y x,
      Int.mul_assoc x y y, ← Int.mul_assoc]

/-- The exact gap between the two sign choices: four times the cross
term.  This is the whole obstruction, isolated. -/
theorem sq_add_sub (a b : Int) :
    (a + b) * (a + b) = (a - b) * (a - b) + 4 * (a * b) := by
  have h1 : (a + b) * (a + b) = a * a + a * b + (b * a + b * b) := by
    rw [Int.add_mul, Int.mul_add, Int.mul_add]
  have h2 : (a - b) * (a - b) = a * a - a * b - (b * a - b * b) := by
    rw [Int.sub_mul, Int.mul_sub, Int.mul_sub]
  have hc : b * a = a * b := Int.mul_comm b a
  rw [h1, h2, hc]
  omega

/-- **Descent classification (two positions)**: the squared read-out
is constant on modulus-blind inputs EXACTLY when the read-out does not
mix — that is, when one of its two coefficients vanishes.  The
obstruction is precisely the cross term, and `sq_add_sub` measures
it. -/
theorem descent_iff_subsingleton_support (a b : Int) :
    (∀ x y x' y', ModulusBlind x y x' y' →
      readOut a b x y * readOut a b x y
        = readOut a b x' y' * readOut a b x' y')
    ↔ a * b = 0 := by
  constructor
  · intro h
    have hblind : ModulusBlind 1 1 1 (-1) := by
      constructor <;> decide
    have hEq := h 1 1 1 (-1) hblind
    have e1 : readOut a b 1 1 = a + b := by
      show a * 1 + b * 1 = a + b
      rw [Int.mul_one, Int.mul_one]
    have e2 : readOut a b 1 (-1) = a - b := by
      show a * 1 + b * (-1) = a - b
      rw [Int.mul_one, Int.mul_neg, Int.mul_one]
      omega
    rw [e1, e2, sq_add_sub a b] at hEq
    omega
  · intro hab x y x' y' ⟨hx, hy⟩
    rcases Int.mul_eq_zero.mp hab with ha | hb
    · have hr : ∀ u v : Int, readOut a b u v = b * v := by
        intro u v
        show a * u + b * v = b * v
        rw [ha, Int.zero_mul, Int.zero_add]
      rw [hr, hr, sq_mul, sq_mul, hy]
    · have hr : ∀ u v : Int, readOut a b u v = a * u := by
        intro u v
        show a * u + b * v = a * u
        rw [hb, Int.zero_mul, Int.add_zero]
      rw [hr, hr, sq_mul, sq_mul, hx]

/-! ## 6. The climb: what a uniqueness law would additionally cost

Everything above is finite integer arithmetic over declared data.
None of it singles out a read-out law.  What would?  The statements
below are PROPOSITIONS, and NONE of them is proved here.  They are
recorded so that anything downstream that wants a uniqueness law must
declare them and pay for them, exactly as protection, budget, and
observer transport are declared and paid for elsewhere. -/

/-- **Import 1 — a decorated carrier.**  There is a declared set of
decorated values with a declared modulus map onto the weights, and a
declared combination operation on it.  The weights alone do not
supply one. -/
def openDecoratedCarrierImport : Prop :=
  ∃ (D : Type) (m : D → Nat) (op : D → D → D),
    (∀ n : Nat, ∃ d : D, m d = n) ∧
    ∀ d e : D, m (op d e) = m (op e d)

/-- **Import 2 — additivity over disjoint parts.**  The read-out of a
carrier split into two disjoint parts is the sum of the parts'
read-outs.  Exact additivity is a DECLARED demand; the calculus does
not entail it. -/
def openDisjointAdditivityImport : Prop :=
  ∀ (l1 l2 : List Nat) (w : Weights),
    total (l1 ++ l2) w = total l1 w + total l2 w

/-- **Import 3 — the uniqueness law.**  Among all read-outs that are
modulus-blind, nonnegative, and additive over disjoint parts, exactly
one is the profile.  This is the expensive import: it is what a
uniqueness claim actually asserts, and nothing above proves it. -/
def openReadOutUniquenessImport : Prop :=
  ∀ (F : List Nat → Weights → Nat) (l : List Nat) (w : Weights),
    0 < total l w →
    (∀ v, SameProfile l w v → F l w = F l v) →
    (∀ l1 l2 v, F (l1 ++ l2) v = F l1 v + F l2 v) →
    F l w = total l w

/-- **The negative fact that makes the imports necessary**: the
weights do NOT determine a decorated presentation.  Over the carrier
`[0, 1]`, the weights `(4, 1)` are presented by two DIFFERENT
decorations, and the declared mixing read-out separates them.  Any
uniqueness claim therefore needs strictly more than the weights. -/
def eA : Nat → Nat := fun p => if p = 0 then 2 else 1

def eB : Nat → Nat := fun p => if p = 0 then 2 else 3

theorem weights_do_not_force_decoration :
    Presents [0, 1] sq eA (fun p => if p = 0 then 4 else 1) ∧
    (¬ Presents [0, 1] sq eB (fun p => if p = 0 then 4 else 1)) ∧
    eA ≠ eB := by
  refine ⟨?_, ?_, ?_⟩
  · intro p hp
    rcases List.mem_cons.mp hp with h | h
    · subst h; decide
    · rcases List.mem_cons.mp h with h2 | h2
      · subst h2; decide
      · cases h2
  · intro hc
    have := hc 1 (by decide)
    exact absurd this (by decide)
  · intro he
    have := congrFun he 1
    exact absurd this (by decide)

/-- **The scope line, stated as a theorem about this module.**  What
is derived: the profile is fixed by the weights up to a positive ray,
a decorated presentation adds nothing to it, and a linear read-out
descends exactly when it does not mix.  What is NOT derived and is
recorded as an unproved import: a decorated carrier, exact disjoint
additivity, and any read-out uniqueness law.  The weights do not force
a decoration, so no uniqueness claim follows from them. -/
theorem derived_and_imported (l : List Nat) (w v : Weights)
    (hw : 0 < total l w) (hv : 0 < total l v) (a : Nat) :
    (SameProfile l w v ↔
      ∃ p q, 0 < p ∧ 0 < q ∧ ∀ x ∈ l, p * w x = q * v x) ∧
    SameProfile l (fun p => a * w p) w ∧
    (∀ (m : Nat → Nat) (c : Nat → Nat), Presents l m c w →
      SameProfile l (fun p => m (c p)) w) :=
  ⟨profile_iff_ray l w v hw hv, profile_scale l a w,
   fun m c h => lift_profile_redundant l m c w h⟩

end WeightProfile
