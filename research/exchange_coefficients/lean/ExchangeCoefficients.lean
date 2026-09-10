import NaturalSections.HopFixture

/-!
# Ordered insertion/removal coefficients and exchange transport

The ordered-occupancy convention and negative move weight are supplied inputs.
This file imports the pinned move and flip definitions unchanged. It proves a
coefficient correspondence, without supplying an endogenous transition rule.
AuthorityEffect: None.
-/

namespace ExchangeCoefficients
open NaturalSections.Hop

def bit (b : Bool) : Int := if b then 1 else 0

/-- Coefficient of |u,v> in c†_p |s>, with u < v.
Insertion on the left is positive; insertion past the occupied site is negative;
creation on an occupied site is zero. -/
def insertCoeff (p s u v : Nat) : Int :=
  if p < s then (if p = u ∧ s = v then 1 else 0)
  else if s < p then (if s = u ∧ p = v then -1 else 0)
  else 0

theorem insert_left (u v s : Nat) (h : u < v) :
    insertCoeff u s u v = if s = v then 1 else 0 := by
  by_cases hs : s = v
  · subst s; simp [insertCoeff, h]
  · simp [insertCoeff, hs, Nat.ne_of_lt h]

theorem insert_right (u v s : Nat) (h : u < v) :
    insertCoeff v s u v = if s = u then -1 else 0 := by
  by_cases hs : s = u
  · subst s; simp [insertCoeff, h, Nat.not_lt.mpr (Nat.le_of_lt h)]
  · simp [insertCoeff, hs, Nat.ne_of_gt h]

/-- A creation site absent from the final configuration contributes zero.
This justifies restricting the creation-site sum to the two final sites. -/
theorem insert_zero_off_target (p s u v : Nat) (hu : p ≠ u) (hv : p ≠ v) :
    insertCoeff p s u v = 0 := by
  simp [insertCoeff, hu, hv]

/-- Coefficient of sum_(p,q) A(q,p)c†_p c_q between the ordered two-site
basis states a and b. Annihilation at a.1 has sign +; at a.2 has sign -.
Only the two occupied removal sites and two target insertion sites contribute.
The scaled move matrix adds the overall factor -t below. -/
def orderedCoeff (adj : Nat → Nat → Bool) (a b : Nat × Nat) : Int :=
  bit (adj a.1 b.1) * insertCoeff b.1 a.2 b.1 b.2 +
  bit (adj a.1 b.2) * insertCoeff b.2 a.2 b.1 b.2 -
  (bit (adj a.2 b.1) * insertCoeff b.1 a.1 b.1 b.2 +
   bit (adj a.2 b.2) * insertCoeff b.2 a.1 b.1 b.2)

/-- The repository's transport sign, zero when no move exists. -/
def transportCoeff (adj : Nat → Nat → Bool) (a b : Nat × Nat) : Int :=
  if hopB adj a b then (if flipB adj a b then -1 else 1) else 0

/-- The general bridge: all ordered pairs of natural-number sites and every
loop-free Boolean adjacency, with no four-site or enumeration restriction.
Adjacency symmetry is unnecessary for this equality; it is a separate
assumption when interpreting the matrix as a symmetric matrix. -/
theorem ordered_eq_transport (adj : Nat → Nat → Bool)
    (noLoop : ∀ q, adj q q = false) (x y u v : Nat)
    (hxy : x < y) (huv : u < v) :
    orderedCoeff adj (x,y) (u,v) = transportCoeff adj (x,y) (u,v) := by
  have hxx := noLoop x
  have hyy := noLoop y
  have huu := noLoop u
  have hvv := noLoop v
  clear noLoop
  simp only [orderedCoeff, insert_left u v y huv, insert_left u v x huv,
    insert_right u v y huv, insert_right u v x huv]
  simp only [transportCoeff, hopB, flipB, Prod.fst, Prod.snd,
    Bool.or_eq_true, Bool.and_eq_true, Nat.beq_eq_true_eq]
  by_cases hxu : x = u <;> by_cases hyv : y = v <;>
    by_cases hxv : x = v <;> by_cases hyu : y = u
  all_goals first
    | (have impossible : False := by omega; exact False.elim impossible)
    | (cases h1 : adj x u <;> cases h2 : adj y v <;>
       cases h3 : adj y u <;> cases h4 : adj x v <;>
       simp_all [bit] <;>
         first | exact Ne.symm hxv | exact Ne.symm hyu |
           exact ⟨Ne.symm hxv, Ne.symm hyu⟩)

def orderedMatrixCoeff (t : Int) (adj : Nat → Nat → Bool) (a b : Nat × Nat) : Int :=
  -t * orderedCoeff adj a b

def transportMatrixCoeff (t : Int) (adj : Nat → Nat → Bool) (a b : Nat × Nat) : Int :=
  -t * transportCoeff adj a b

theorem scaled_eq (t : Int) (adj : Nat → Nat → Bool)
    (noLoop : ∀ q, adj q q = false) (x y u v : Nat)
    (hxy : x < y) (huv : u < v) :
    orderedMatrixCoeff t adj (x,y) (u,v) = transportMatrixCoeff t adj (x,y) (u,v) := by
  unfold orderedMatrixCoeff transportMatrixCoeff
  rw [ordered_eq_transport adj noLoop x y u v hxy huv]

/-- A finite matrix equality for every size n, not just the fixtures.
Coefficients are indexed by ordered two-site configurations. -/
abbrev Config (n : Nat) := {p : Fin n × Fin n // p.1.val < p.2.val}

theorem finite_matrix_eq (n : Nat) (t : Int) (adj : Nat → Nat → Bool)
    (noLoop : ∀ q, adj q q = false) :
    (fun a b : Config n => orderedMatrixCoeff t adj (a.val.1.val,a.val.2.val)
      (b.val.1.val,b.val.2.val)) =
    (fun a b : Config n => transportMatrixCoeff t adj (a.val.1.val,a.val.2.val)
      (b.val.1.val,b.val.2.val)) := by
  funext a b
  exact scaled_eq t adj noLoop _ _ _ _ a.property b.property

theorem three_fixtures :
    ∀ a b : Pair4,
      orderedMatrixCoeff 1 chainAdj a.sites b.sites = transportMatrixCoeff 1 chainAdj a.sites b.sites ∧
      orderedMatrixCoeff 1 squareAdj a.sites b.sites = transportMatrixCoeff 1 squareAdj a.sites b.sites ∧
      orderedMatrixCoeff 1 starAdj a.sites b.sites = transportMatrixCoeff 1 starAdj a.sites b.sites := by
  intro a b
  cases a <;> cases b <;> decide

/-- Creation on an occupied singleton is zero: the added signed occupancy convention
already includes exclusion. This is not derived from the opaque seed. -/
theorem insertion_exclusion (p u v : Nat) : insertCoeff p p u v = 0 := by
  simp [insertCoeff]

def pathParity {X : Type} (edge : X → X → Bool) : X → List X → Bool
  | _, [] => false
  | a, b :: rest => Bool.xor (edge a b) (pathParity edge b rest)

def endpoint {X : Type} : X → List X → X
  | a, [] => a
  | _, b :: rest => endpoint b rest

def twist {X : Type} (g : X → Bool) (edge : X → X → Bool) (a b : X) : Bool :=
  Bool.xor (Bool.xor (g a) (edge a b)) (g b)

/-- Vertex sign changes cancel at internal vertices, for every path. -/
theorem path_gauge {X : Type} (g : X → Bool) (edge : X → X → Bool)
    (a : X) (rest : List X) :
    pathParity (twist g edge) a rest =
      Bool.xor (Bool.xor (g a) (pathParity edge a rest)) (g (endpoint a rest)) := by
  induction rest generalizing a with
  | nil => simp only [pathParity, endpoint]; cases g a <;> rfl
  | cons b rest ih =>
    simp only [pathParity, endpoint, twist, ih]
    cases g a <;> cases edge a b <;> cases g b <;>
      cases pathParity edge b rest <;> cases g (endpoint b rest) <;> rfl

/-- A closed odd exchange loop remains odd under every vertex sign assignment. -/
theorem closed_odd_gauge {X : Type} (g : X → Bool) (edge : X → X → Bool)
    (a : X) (rest : List X) (closed : endpoint a rest = a)
    (odd : pathParity edge a rest = true) :
    pathParity (twist g edge) a rest = true := by
  rw [path_gauge, closed, odd]
  cases g a <;> rfl

theorem star_odd :
    pathParity (fun a b : Pair4 => flipB starAdj a.sites b.sites) .c01
      [.c13, .c03, .c23, .c02, .c12, .c01] = true := by decide

theorem square_odd :
    pathParity (fun a b : Pair4 => flipB squareAdj a.sites b.sites) .c01
      [.c03, .c02, .c12, .c01] = true := by decide

end ExchangeCoefficients
