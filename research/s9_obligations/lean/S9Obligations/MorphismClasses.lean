import Derivation.PrimDiff

/-!
# P2 -- S9.2, morphism classes and initiality: the carrier-general half (PROMPT.md step 19)

The finite sweep of `research/s9_obligations/morphism_classes.py` decides,
for every class `C` of the five-condition menu and every two-element
pointed structure `O` with an asserted pair, whether `O` is initial for
`C` over every object of carrier at most 4.  Initiality quantifies over
all objects, so every cell of that table is bounded.  This module carries
the cells beyond the bound, as P2 proposed (`P2_FINDINGS.md`, section 6):
positive cells as initiality over an arbitrary carrier `alpha`, with the
class's conditions stated literally as hypotheses on the morphism, and
negative cells as a concrete countermodel object with an explicit failure
of existence or of uniqueness.  It then states, per class, which
two-element objects are initial, and, over all 32 classes at once, which
classes leave some two-element object initial.

The menu, exactly as `morphism_classes.py` declares it (P2 step 15), for a
map `f : Bool -> alpha` out of the candidate `(Bool, r0, a0, b0)` into the
object `(alpha, r, a, b)`:

* P   `f a0 = a` and `f b0 = b`;
* E   `r0 x y -> r (f x) (f y)`;
* NE  `not r0 x y -> not r (f x) (f y)`, kept in this form and never
      replaced by its contrapositive, which is the same condition only
      over decidable relations;
* I   `f x = f y -> x = y`;
* S   every `z : alpha` is `f x` for some `x`.

The two object classes, exactly as P2 declares them: PRIMARY is every
pointed structure with an asserted pair (`r a b`), irreflexivity not
imposed, `a = b` allowed; SECONDARY is the same with `Irrefl r` imposed on
every object.  Candidates are pointed relations on `Bool` with the
asserted pair; every statement below quantifies over such candidates as
`(r0 : Bool -> Bool -> Prop) (a0 b0 : Bool)` with `r0 a0 b0`, which
contains the 32 raw candidates the sweep enumerated, so no transport
through the implemented isomorphism is needed for the two classes whose
representative is pointed at `(1, 0)`.

Sealed names are reused, never restated: `Irrefl`, `Transpose`, `D2`,
`D2rev`, `S2`, `D2_witness`, `D2_irrefl`, `S2_irrefl`,
`irrefl_witness_ne`, and above all `D2_initial_pointed`, which is cited
for the cell it already names (P2 step 14) and not re-proved.

Countermodel objects, named as in the receipt's witness legend: `SELF1`
is `(Unit, Full Unit, (), ())`, the object of the sealed
`selfdiff_consistent`; `D2` and `S2` are the sealed carriers pointed at
`(false, true)`; `FULL2` is the full relation on `Bool`; `n3:01:a0b1` is
`ThreeChain` on `Fin 3`; the doubled object `Doubled r0` on `Bool x Bool`
is this module's own uniform witness for uniqueness failures, which the
receipt records at smaller first witnesses.

AuthorityEffect: None.  Nothing under `lean4/Derivation/` is touched; this
module proposes.  A theorem here carries a cell of P2's table beyond its
carrier bound only within the scope its statement names: the declared
menu, the declared object class, and candidates on `Bool`.
-/

namespace S9Obligations.MorphismClasses

open PrimDiff

/-! ## The menu, as predicates on a map out of a two-element candidate -/

/-- P: designated points preserved, `f a0 = a` and `f b0 = b`. -/
abbrev PreservesPoints {α : Type} (f : Bool → α) (a0 b0 : Bool) (a b : α) : Prop :=
  f a0 = a ∧ f b0 = b

/-- E: edges preserved, `r0 x y -> r (f x) (f y)`. -/
abbrev PreservesEdges {α : Type} (r0 : Bool → Bool → Prop) (r : α → α → Prop)
    (f : Bool → α) : Prop :=
  ∀ x y, r0 x y → r (f x) (f y)

/-- NE: non-edges preserved, `not r0 x y -> not r (f x) (f y)`, in the
not -> not form the menu prescribes. -/
abbrev PreservesNonEdges {α : Type} (r0 : Bool → Bool → Prop) (r : α → α → Prop)
    (f : Bool → α) : Prop :=
  ∀ x y, ¬ r0 x y → ¬ r (f x) (f y)

/-- I: injective, `f x = f y -> x = y`. -/
abbrev Injective {α : Type} (f : Bool → α) : Prop :=
  ∀ x y, f x = f y → x = y

/-- S: surjective, every point of the target carrier is hit. -/
abbrev Surjective {α : Type} (f : Bool → α) : Prop :=
  ∀ z : α, ∃ x, f x = z

/-! ## Countermodel objects -/

/-- The full relation on a carrier.  On `Unit` it is the object of the
sealed `selfdiff_consistent`, the receipt's `SELF1`; on `Fin 3` it is the
three-point object with every pair asserted. -/
def Full (α : Type) : α → α → Prop := fun _ _ => True

/-- The full relation on `Bool`, the receipt's candidate `FULL2`
(`O01_1111` when pointed at `(false, true)`). -/
def FULL2 : Bool → Bool → Prop := fun _ _ => True

/-- Two disjoint copies of a candidate on `Bool x Bool`: a pair is related
exactly when both points lie in the same copy and the candidate relates
their first components.  The uniform witness for uniqueness failures. -/
def Doubled (r0 : Bool → Bool → Prop) : Bool × Bool → Bool × Bool → Prop :=
  fun p q => p.2 = q.2 ∧ r0 p.1 q.1

/-- The receipt's three-point irreflexive object `n3:01:a0b1`: the single
edge `(0, 1)` on `Fin 3`. -/
def ThreeChain : Fin 3 → Fin 3 → Prop := fun x y => x = 0 ∧ y = 1

/-- Two flags of one `Bool` cannot both hold. -/
theorem not_both {b : Bool} (h1 : b = false) (h2 : b = true) : False :=
  Bool.noConfusion (h1.symm.trans h2)

/-- A map out of `Bool` is injective exactly when it separates the two
points; only the direction used below is stated. -/
theorem injective_of_ne {α : Type} (f : Bool → α) (h : f false ≠ f true) :
    Injective f := by
  intro x y hxy
  cases x <;> cases y
  · rfl
  · exact absurd hxy h
  · exact absurd hxy.symm h
  · rfl

/-! ## Positive cells of the primary object class -/

/-- Target 1, class `{P}`, every candidate pointed at two distinct points
-- the receipt's 8 initial `{P}` cells
(`witness_groups.primary.groups.P_class_initial.cells`), the two whose
representative is pointed at `(1, 0)` included literally.  The candidate's
relation does not occur, which is why those eight tie.  Both pointings
cite the sealed `D2_initial_pointed`: `(false, true)` directly, with the
edge clause dropped from its existence half (the receipt's
`lean.sealed_theorem_cell`), and `(true, false)` through the sealed
`Transpose`.  Over the secondary object class the same statement carries
`({P}, D2)` and `({P}, S2)`, since it does not use irreflexivity. -/
theorem two_element_pointed_map_unique {α : Type} (r : α → α → Prop) (a b : α)
    (h : r a b) (a0 b0 : Bool) (hne : a0 ≠ b0) :
    ∃ f : Bool → α, PreservesPoints f a0 b0 a b ∧
      ∀ g : Bool → α, PreservesPoints g a0 b0 a b → ∀ t, g t = f t := by
  cases a0 with
  | false =>
    cases b0 with
    | false => exact absurd rfl hne
    | true =>
      obtain ⟨f, ⟨hfa, hfb, _⟩, hu⟩ := D2_initial_pointed r a b h
      exact ⟨f, ⟨hfa, hfb⟩, fun g ⟨hga, hgb⟩ => hu g hga hgb⟩
  | true =>
    cases b0 with
    | false =>
      obtain ⟨f, ⟨hfb, hfa, _⟩, hu⟩ :=
        D2_initial_pointed (Transpose r) b a (show Transpose r b a from h)
      exact ⟨f, ⟨hfa, hfb⟩, fun g ⟨hga, hgb⟩ => hu g hgb hga⟩
    | true => exact absurd rfl hne

/-- Target 2, cell `(primary, {P,E}, D2)`, the receipt's
`d2_initial_pointed_cell.corollary_cell`: the unique point-preserving map
out of `D2` preserves the oriented edge, so `D2` is initial for `{P,E}` on
every carrier.  Cites the sealed `D2_initial_pointed`. -/
theorem D2_initial_P_E {α : Type} (r : α → α → Prop) (a b : α) (h : r a b) :
    ∃ f : Bool → α, (PreservesPoints f false true a b ∧ PreservesEdges D2 r f) ∧
      ∀ g : Bool → α, (PreservesPoints g false true a b ∧ PreservesEdges D2 r g) →
        ∀ t, g t = f t := by
  obtain ⟨f, ⟨hfa, hfb, hfe⟩, hu⟩ := D2_initial_pointed r a b h
  exact ⟨f, ⟨⟨hfa, hfb⟩, hfe⟩, fun g ⟨⟨hga, hgb⟩, _⟩ => hu g hga hgb⟩

/-- Target 3, cell `(primary, {P,NE}, FULL2)`
(`initial_objects_by_class.primary.by_class.{P,NE}` = `[O01_1111]`): the
full candidate has no non-edge, so NE is vacuous and the point-preserving
map is the only one. -/
theorem FULL2_initial_P_NE {α : Type} (r : α → α → Prop) (a b : α) (h : r a b) :
    ∃ f : Bool → α, (PreservesPoints f false true a b ∧ PreservesNonEdges FULL2 r f) ∧
      ∀ g : Bool → α, (PreservesPoints g false true a b ∧ PreservesNonEdges FULL2 r g) →
        ∀ t, g t = f t := by
  obtain ⟨f, hf, hu⟩ := two_element_pointed_map_unique r a b h false true (by decide)
  refine ⟨f, ⟨hf, ?_⟩, fun g ⟨hg, _⟩ => hu g hg⟩
  intro x y hn
  exact absurd trivial hn

/-! ## Negative cells of the primary object class: one countermodel object each -/

/-- Target 4, the receipt's `I_classes` group
(`witness_groups.primary.groups.I_classes.cells` = 256): the one-point
self-difference `SELF1` is an object of the primary class, and no map from
`Bool` into a point is injective, so no class containing I has a morphism
into it from any candidate. -/
theorem no_injection_into_point :
    Full Unit () () ∧ ∀ f : Bool → Unit, ¬ Injective f :=
  ⟨trivial, fun _ hi => Bool.noConfusion (hi false true rfl)⟩

/-- Target 5, the receipt's `S_without_I_classes` group
(`witness_groups.primary.groups.S_without_I_classes.cells` = 128): the
three-point full object is an object of the primary class, and no map from
`Bool` onto three points exists, so no class containing S has a morphism
into it from any candidate.  The receipt's first witnesses lie at carriers
1, 2, or 3; the exhibited object is uniform.  Decided constructively over
`Fin 3`. -/
theorem no_surjection_onto_three :
    Full (Fin 3) 0 0 ∧ ∀ f : Bool → Fin 3, ¬ Surjective f := by
  refine ⟨trivial, fun f hs => ?_⟩
  have key : ∀ u v : Fin 3, ∃ z : Fin 3, z ≠ u ∧ z ≠ v := by decide
  obtain ⟨z, hzu, hzv⟩ := key (f false) (f true)
  obtain ⟨x, hx⟩ := hs z
  cases x with
  | false => exact hzu hx.symm
  | true => exact hzv hx.symm

/-- Target 6, the receipt's `no_P_I_S_classes` group
(`witness_groups.primary.groups.no_P_I_S_classes.cells` = 64, classes
`{}`, `{E}`, `{NE}`, `{E,NE}`): the doubled candidate is an object of the
primary class, and the two copy inclusions are distinct maps that both
preserve edges and non-edges, so uniqueness fails for every class without
P, I, S and every candidate. -/
theorem two_copies_not_unique (r0 : Bool → Bool → Prop) (a0 b0 : Bool) (h : r0 a0 b0) :
    Doubled r0 (a0, false) (b0, false) ∧
    ∃ f1 f2 : Bool → Bool × Bool,
      (∃ t, f1 t ≠ f2 t) ∧
      PreservesEdges r0 (Doubled r0) f1 ∧ PreservesEdges r0 (Doubled r0) f2 ∧
      PreservesNonEdges r0 (Doubled r0) f1 ∧ PreservesNonEdges r0 (Doubled r0) f2 := by
  refine ⟨⟨rfl, h⟩, fun x => (x, false), fun x => (x, true), ⟨false, by decide⟩,
    ?_, ?_, ?_, ?_⟩
  · intro x y hxy
    exact ⟨rfl, hxy⟩
  · intro x y hxy
    exact ⟨rfl, hxy⟩
  · intro x y hn hd
    exact hn hd.2
  · intro x y hn hd
    exact hn hd.2

/-- Target 7, the diagonal candidates (`a0 = b0`) in every class containing
P -- the receipt's `P_class_non_initial` group and the
`non_initial_diagonal_candidates` of `{P,E}`, `{P,NE}`, `{P,E,NE}`: at the
object `D2` (sealed `D2_witness`) a point-preserving map would send the one
designated point to both `false` and `true`. -/
theorem diagonal_candidate_not_pointed_into_D2 (o : Bool) (f : Bool → Bool) :
    ¬ PreservesPoints f o o false true :=
  fun ⟨h1, h2⟩ => Bool.noConfusion (h1.symm.trans h2)

/-- Target 8, stated for a general pointing so that it covers `O10_1010`
and `O10_1110` literally: a candidate pointed at two distinct points that
asserts any pair other than its designated one has no point-preserving
edge-preserving map into `D2`.  Refutes existence at `D2` for the 7
non-initial off-diagonal cells of `{P,E}`
(`witness_groups.primary.groups.P_E_class.non_initial_off_diagonal_candidates`)
and for `({P,E,NE}, FULL2)`. -/
theorem extra_edge_not_into_D2 (r0 : Bool → Bool → Prop) (a0 b0 : Bool) (hne : a0 ≠ b0)
    (hextra : ∃ x y, (x, y) ≠ (a0, b0) ∧ r0 x y) (f : Bool → Bool)
    (hp : PreservesPoints f a0 b0 false true) : ¬ PreservesEdges r0 D2 f := by
  intro he
  obtain ⟨x, y, hxy, hr⟩ := hextra
  have hd : D2 (f x) (f y) := he x y hr
  obtain ⟨hfa, hfb⟩ := hp
  cases a0 <;> cases b0 <;> cases x <;> cases y <;> simp_all [D2]

/-- Target 9, every class containing NE and every candidate with a
non-edge, at the one-point self-difference `SELF1`: the only map into a
point sends the non-edge onto the loop.  Refutes existence for the 14 + 14
cells the receipt records there
(`witness_groups.primary.groups.P_NE_class.existence_witness_counts.SELF1`,
`witness_groups.primary.groups.P_E_NE_class.existence_witness_counts.SELF1`).
-/
theorem non_edge_not_into_point (r0 : Bool → Bool → Prop) (hn : ∃ x y, ¬ r0 x y)
    (f : Bool → Unit) : ¬ PreservesNonEdges r0 (Full Unit) f := by
  intro hne
  obtain ⟨x, y, hxy⟩ := hn
  exact hne x y hxy trivial

/-! ## The secondary object class (irreflexivity imposed) -/

/-- Target 10: over an irreflexive object the point-preserving map out of
a candidate pointed at two distinct points is injective, by the sealed
`irrefl_witness_ne`.  This is the carrier-general form of the observation
that adding I to a class containing P changes nothing over the secondary
object class. -/
theorem pointed_map_injective_of_irrefl {α : Type} {r : α → α → Prop} (hi : Irrefl r)
    {a b : α} (h : r a b) (a0 b0 : Bool) (hne : a0 ≠ b0) (f : Bool → α)
    (hp : PreservesPoints f a0 b0 a b) : Injective f := by
  have hab : a ≠ b := irrefl_witness_ne hi h
  cases a0 with
  | false =>
    cases b0 with
    | false => exact absurd rfl hne
    | true =>
      apply injective_of_ne
      rw [hp.1, hp.2]
      exact hab
  | true =>
    cases b0 with
    | false =>
      apply injective_of_ne
      rw [hp.1, hp.2]
      exact fun e => hab e.symm
    | true => exact absurd rfl hne

/-- Cells `(secondary, {P,I}, D2)` and `(secondary, {P,I}, S2)`
(`initial_objects_by_class.secondary.by_class.{P,I}`): any candidate
pointed at two distinct points is initial for `{P,I}` over irreflexive
objects. -/
theorem two_element_initial_P_I_irrefl {α : Type} (r : α → α → Prop) (hi : Irrefl r)
    (a b : α) (h : r a b) (a0 b0 : Bool) (hne : a0 ≠ b0) :
    ∃ f : Bool → α, (PreservesPoints f a0 b0 a b ∧ Injective f) ∧
      ∀ g : Bool → α, (PreservesPoints g a0 b0 a b ∧ Injective g) → ∀ t, g t = f t := by
  obtain ⟨f, hf, hu⟩ := two_element_pointed_map_unique r a b h a0 b0 hne
  exact ⟨f, ⟨hf, pointed_map_injective_of_irrefl hi h a0 b0 hne f hf⟩,
    fun g ⟨hg, _⟩ => hu g hg⟩

/-- Cell `(secondary, {P,E,I}, D2)`
(`initial_objects_by_class.secondary.by_class.{P,E,I}` = `[O01_0100]`). -/
theorem D2_initial_P_E_I_irrefl {α : Type} (r : α → α → Prop) (hi : Irrefl r)
    (a b : α) (h : r a b) :
    ∃ f : Bool → α,
      (PreservesPoints f false true a b ∧ PreservesEdges D2 r f ∧ Injective f) ∧
      ∀ g : Bool → α,
        (PreservesPoints g false true a b ∧ PreservesEdges D2 r g ∧ Injective g) →
        ∀ t, g t = f t := by
  obtain ⟨f, ⟨hfp, hfe⟩, hu⟩ := D2_initial_P_E r a b h
  exact ⟨f, ⟨hfp, hfe, pointed_map_injective_of_irrefl hi h false true (by decide) f hfp⟩,
    fun g ⟨hgp, hge, _⟩ => hu g ⟨hgp, hge⟩⟩

/-- Target 11, cell `(secondary, {P,NE}, S2)`
(`initial_objects_by_class.secondary.by_class.{P,NE}` = `[O01_0110]`): the
non-edges of `S2` are the two loops, and irreflexivity of the object
supplies `not r a a` and `not r b b`. -/
theorem S2_initial_P_NE_irrefl {α : Type} (r : α → α → Prop) (hi : Irrefl r)
    (a b : α) (h : r a b) :
    ∃ f : Bool → α, (PreservesPoints f false true a b ∧ PreservesNonEdges S2 r f) ∧
      ∀ g : Bool → α, (PreservesPoints g false true a b ∧ PreservesNonEdges S2 r g) →
        ∀ t, g t = f t := by
  obtain ⟨f, hf, hu⟩ := two_element_pointed_map_unique r a b h false true (by decide)
  refine ⟨f, ⟨hf, ?_⟩, fun g ⟨hg, _⟩ => hu g hg⟩
  obtain ⟨hfa, hfb⟩ := hf
  intro x y hn
  cases x <;> cases y
  · rw [hfa]
    exact hi a
  · exact absurd (by decide : S2 false true) hn
  · exact absurd (by decide : S2 true false) hn
  · rw [hfb]
    exact hi b

/-- Cell `(secondary, {P,NE,I}, S2)`
(`initial_objects_by_class.secondary.by_class.{P,NE,I}` = `[O01_0110]`). -/
theorem S2_initial_P_NE_I_irrefl {α : Type} (r : α → α → Prop) (hi : Irrefl r)
    (a b : α) (h : r a b) :
    ∃ f : Bool → α,
      (PreservesPoints f false true a b ∧ PreservesNonEdges S2 r f ∧ Injective f) ∧
      ∀ g : Bool → α,
        (PreservesPoints g false true a b ∧ PreservesNonEdges S2 r g ∧ Injective g) →
        ∀ t, g t = f t := by
  obtain ⟨f, ⟨hfp, hfn⟩, hu⟩ := S2_initial_P_NE_irrefl r hi a b h
  exact ⟨f, ⟨hfp, hfn, pointed_map_injective_of_irrefl hi h false true (by decide) f hfp⟩,
    fun g ⟨hgp, hgn, _⟩ => hu g ⟨hgp, hgn⟩⟩

/-- Target 12, existence failure at the object `D2` (irreflexive by the
sealed `D2_irrefl`) for `(secondary, {P,E}, S2)` and its supersets
`{P,E,I}`, `{P,E,NE}`, `{P,E,NE,I}`
(`witness_groups.secondary.groups.P_without_S_non_initial.existence_witness_counts.D2`
= 4), and for `(primary, {P,E}, S2)`: the point-preserving map sends the
reverse edge of `S2` onto a non-edge of `D2`. -/
theorem S2_not_P_E_into_D2 (f : Bool → Bool) (hp : PreservesPoints f false true false true) :
    ¬ PreservesEdges S2 D2 f := by
  intro he
  have h1 : D2 (f true) (f false) := he true false (by decide)
  rw [hp.2, hp.1] at h1
  exact absurd h1 (by decide)

/-- Target 13, existence failure at the object `S2` (irreflexive by the
sealed `S2_irrefl`) for `(secondary, {P,NE}, D2)` and its supersets
`{P,NE,I}`, `{P,E,NE}`, `{P,E,NE,I}`
(`witness_groups.secondary.groups.P_without_S_non_initial.existence_witness_counts.S2`
= 4): the point-preserving map sends the non-edge `(true, false)` of `D2`
onto an edge of `S2`. -/
theorem D2_not_P_NE_into_S2 (f : Bool → Bool) (hp : PreservesPoints f false true false true) :
    ¬ PreservesNonEdges D2 S2 f := by
  intro hne
  have h1 : ¬ S2 (f true) (f false) := hne true false (by decide)
  rw [hp.2, hp.1] at h1
  exact h1 (by decide)

/-- Target 14, the receipt's `S_classes` group of the secondary object
class (`witness_groups.secondary.groups.S_classes.cells` = 32): the
three-point single-edge object `n3:01:a0b1` is irreflexive, asserts its
pair, and admits no surjection from `Bool`. -/
theorem no_surjection_onto_three_irrefl :
    Irrefl ThreeChain ∧ ThreeChain 0 1 ∧ ∀ f : Bool → Fin 3, ¬ Surjective f := by
  refine ⟨?_, ⟨rfl, rfl⟩, no_surjection_onto_three.2⟩
  intro x hx
  obtain ⟨h0, h1⟩ := hx
  rw [h0] at h1
  exact absurd h1 (by decide)

/-- Target 15, the receipt's `no_P_no_S_classes` group of the secondary
object class (`witness_groups.secondary.groups.no_P_no_S_classes.cells` =
16): the doubled candidate of an irreflexive candidate is irreflexive, and
the two copy inclusions are distinct, preserve edges and non-edges, and
are injective, so uniqueness fails for every class without P and S. -/
theorem two_irrefl_copies_not_unique (r0 : Bool → Bool → Prop) (hi : Irrefl r0)
    (a0 b0 : Bool) (h : r0 a0 b0) :
    Irrefl (Doubled r0) ∧ Doubled r0 (a0, false) (b0, false) ∧
    ∃ f1 f2 : Bool → Bool × Bool,
      (∃ t, f1 t ≠ f2 t) ∧
      PreservesEdges r0 (Doubled r0) f1 ∧ PreservesEdges r0 (Doubled r0) f2 ∧
      PreservesNonEdges r0 (Doubled r0) f1 ∧ PreservesNonEdges r0 (Doubled r0) f2 ∧
      Injective f1 ∧ Injective f2 := by
  refine ⟨fun p hp => hi p.1 hp.2, ⟨rfl, h⟩, fun x => (x, false), fun x => (x, true),
    ⟨false, by decide⟩, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x y hxy
    exact ⟨rfl, hxy⟩
  · intro x y hxy
    exact ⟨rfl, hxy⟩
  · intro x y hn hd
    exact hn hd.2
  · intro x y hn hd
    exact hn hd.2
  · intro x y hxy
    exact congrArg Prod.fst hxy
  · intro x y hxy
    exact congrArg Prod.fst hxy

/-! ## Classes as data, and what each class admits -/

/-- A morphism class: one flag per menu condition, in menu order.  The 32
values are P2's 32 classes; `{P,E}` is `⟨true, true, false, false, false⟩`. -/
structure MClass where
  P : Bool
  E : Bool
  NE : Bool
  I : Bool
  S : Bool
  deriving DecidableEq

/-- The class `{P}`. -/
def classP : MClass := ⟨true, false, false, false, false⟩

/-- The class `{P,E}`. -/
def classPE : MClass := ⟨true, true, false, false, false⟩

/-- The class `{P,NE}`. -/
def classPNE : MClass := ⟨true, false, true, false, false⟩

/-- The class `{P,E,NE}`. -/
def classPENE : MClass := ⟨true, true, true, false, false⟩

/-- The class `{P,I}`. -/
def classPI : MClass := ⟨true, false, false, true, false⟩

/-- The class `{P,E,I}`. -/
def classPEI : MClass := ⟨true, true, false, true, false⟩

/-- The class `{P,NE,I}`. -/
def classPNEI : MClass := ⟨true, false, true, true, false⟩

/-- A `C`-morphism from the candidate `(Bool, r0, a0, b0)` to the object
`(alpha, r, a, b)`: every condition in `C` holds of `f`, each stated in
the menu's own form. -/
def MClass.Cond (C : MClass) {α : Type} (r0 : Bool → Bool → Prop) (a0 b0 : Bool)
    (r : α → α → Prop) (a b : α) (f : Bool → α) : Prop :=
  (C.P = true → PreservesPoints f a0 b0 a b) ∧
  (C.E = true → PreservesEdges r0 r f) ∧
  (C.NE = true → PreservesNonEdges r0 r f) ∧
  (C.I = true → Injective f) ∧
  (C.S = true → Surjective f)

/-- `(Bool, r0, a0, b0)` is initial for `C` over the primary object class:
every pointed structure with an asserted pair, on every carrier, has
exactly one `C`-morphism from it. -/
def MClass.InitialPrimary (C : MClass) (r0 : Bool → Bool → Prop) (a0 b0 : Bool) : Prop :=
  ∀ (α : Type) (r : α → α → Prop) (a b : α), r a b →
    ∃ f : Bool → α, C.Cond r0 a0 b0 r a b f ∧
      ∀ g : Bool → α, C.Cond r0 a0 b0 r a b g → ∀ t, g t = f t

/-- `(Bool, r0, a0, b0)` is initial for `C` over the secondary object
class: the same, over irreflexive objects only. -/
def MClass.InitialSecondary (C : MClass) (r0 : Bool → Bool → Prop) (a0 b0 : Bool) : Prop :=
  ∀ (α : Type) (r : α → α → Prop), Irrefl r → ∀ (a b : α), r a b →
    ∃ f : Bool → α, C.Cond r0 a0 b0 r a b f ∧
      ∀ g : Bool → α, C.Cond r0 a0 b0 r a b g → ∀ t, g t = f t

/-- `C` leaves some two-element object initial over the primary object
class. -/
def MClass.AdmitsPrimary (C : MClass) : Prop :=
  ∃ (r0 : Bool → Bool → Prop) (a0 b0 : Bool), r0 a0 b0 ∧ C.InitialPrimary r0 a0 b0

/-- `C` leaves some irreflexive two-element object initial over the
secondary object class. -/
def MClass.AdmitsSecondary (C : MClass) : Prop :=
  ∃ (r0 : Bool → Bool → Prop) (a0 b0 : Bool),
    Irrefl r0 ∧ r0 a0 b0 ∧ C.InitialSecondary r0 a0 b0

/-! ### Per-class verdicts over the primary object class, for the classes with P and without I, S -/

/-- Class `{P}`: a candidate is initial exactly when it is pointed at two
distinct points.  The 16 primary `{P}` cells are the two values of the
right-hand side (`witness_groups.primary.groups.P_class_initial`,
`witness_groups.primary.groups.P_class_non_initial`). -/
theorem initial_P_iff (r0 : Bool → Bool → Prop) (a0 b0 : Bool) :
    classP.InitialPrimary r0 a0 b0 ↔ a0 ≠ b0 := by
  constructor
  · intro hinit hab
    subst hab
    obtain ⟨f, hf, _⟩ := hinit Bool D2 false true D2_witness
    exact diagonal_candidate_not_pointed_into_D2 _ f (hf.1 rfl)
  · intro hne α r a b h
    obtain ⟨f, hf, hu⟩ := two_element_pointed_map_unique r a b h a0 b0 hne
    refine ⟨f, ⟨fun _ => hf, fun e => Bool.noConfusion e, fun e => Bool.noConfusion e,
      fun e => Bool.noConfusion e, fun e => Bool.noConfusion e⟩, ?_⟩
    intro g hg t
    exact hu g (hg.1 rfl) t

/-- Class `{P,E}`: a candidate is initial exactly when it is pointed at two
distinct points and asserts no pair beyond its designated one -- that is,
exactly when it is `D2` up to the pointing.  Left to right uses the object
`D2` twice (targets 7 and 8); right to left is target 1 with the edge
condition read off the single edge.  The 16 primary `{P,E}` cells are the
values of the right-hand side (`witness_groups.primary.groups.P_E_class`). -/
theorem initial_P_E_iff (r0 : Bool → Bool → Prop) (a0 b0 : Bool) :
    classPE.InitialPrimary r0 a0 b0 ↔ (a0 ≠ b0 ∧ ∀ x y, r0 x y → x = a0 ∧ y = b0) := by
  constructor
  · intro hinit
    obtain ⟨f, hf, _⟩ := hinit Bool D2 false true D2_witness
    have hp : PreservesPoints f a0 b0 false true := hf.1 rfl
    have he : PreservesEdges r0 D2 f := hf.2.1 rfl
    have hne : a0 ≠ b0 := fun hab => by
      subst hab
      exact diagonal_candidate_not_pointed_into_D2 _ f hp
    refine ⟨hne, fun x y hr => ?_⟩
    by_cases hxy : x = a0 ∧ y = b0
    · exact hxy
    · exfalso
      exact extra_edge_not_into_D2 r0 a0 b0 hne
        ⟨x, y, fun e => hxy ⟨congrArg Prod.fst e, congrArg Prod.snd e⟩, hr⟩ f hp he
  · intro ⟨hne, hsingle⟩ α r a b h
    obtain ⟨f, hf, hu⟩ := two_element_pointed_map_unique r a b h a0 b0 hne
    refine ⟨f, ⟨fun _ => hf, fun _ x y hr => ?_, fun e => Bool.noConfusion e,
      fun e => Bool.noConfusion e, fun e => Bool.noConfusion e⟩, ?_⟩
    · obtain ⟨hx, hy⟩ := hsingle x y hr
      rw [hx, hy, hf.1, hf.2]
      exact h
    · intro g hg t
      exact hu g (hg.1 rfl) t

/-- Class `{P,NE}`: a decidable candidate is initial exactly when it is
pointed at two distinct points and asserts every pair -- that is, exactly
when it is `FULL2` up to the pointing.  Left to right uses `D2` (target 7)
and the one-point self-difference (target 9); decidability of the
candidate's relation is what turns "no non-edge" into "every pair", as it
does for the 32 finite candidates.  The 16 primary `{P,NE}` cells are the
values of the right-hand side (`witness_groups.primary.groups.P_NE_class`). -/
theorem initial_P_NE_iff (r0 : Bool → Bool → Prop) [∀ x y, Decidable (r0 x y)]
    (a0 b0 : Bool) :
    classPNE.InitialPrimary r0 a0 b0 ↔ (a0 ≠ b0 ∧ ∀ x y, r0 x y) := by
  constructor
  · intro hinit
    obtain ⟨f, hf, _⟩ := hinit Bool D2 false true D2_witness
    have hp : PreservesPoints f a0 b0 false true := hf.1 rfl
    have hne : a0 ≠ b0 := fun hab => by
      subst hab
      exact diagonal_candidate_not_pointed_into_D2 _ f hp
    refine ⟨hne, fun x y => ?_⟩
    by_cases hr : r0 x y
    · exact hr
    · exfalso
      obtain ⟨fU, hfU, _⟩ := hinit Unit (Full Unit) () () trivial
      exact non_edge_not_into_point r0 ⟨x, y, hr⟩ fU (hfU.2.2.1 rfl)
  · intro ⟨hne, hfull⟩ α r a b h
    obtain ⟨f, hf, hu⟩ := two_element_pointed_map_unique r a b h a0 b0 hne
    refine ⟨f, ⟨fun _ => hf, fun e => Bool.noConfusion e, fun _ x y hn => absurd (hfull x y) hn,
      fun e => Bool.noConfusion e, fun e => Bool.noConfusion e⟩, ?_⟩
    intro g hg t
    exact hu g (hg.1 rfl) t

/-- Class `{P,E,NE}`: no candidate is initial over the primary object class
(`initial_objects_by_class.primary.by_class.{P,E,NE}` = `[]`, the
receipt's `shape.primary.gap`).  The edge-preserving map into `D2` refutes
`r0 a0 a0`; the non-edge-preserving map into the one-point self-difference
refutes its negation.  No decidability is needed. -/
theorem not_initial_P_E_NE (r0 : Bool → Bool → Prop) (a0 b0 : Bool) :
    ¬ classPENE.InitialPrimary r0 a0 b0 := by
  intro hinit
  obtain ⟨fD, hfD, _⟩ := hinit Bool D2 false true D2_witness
  obtain ⟨fU, hfU, _⟩ := hinit Unit (Full Unit) () () trivial
  have hp : PreservesPoints fD a0 b0 false true := hfD.1 rfl
  have he : PreservesEdges r0 D2 fD := hfD.2.1 rfl
  have hn : PreservesNonEdges r0 (Full Unit) fU := hfU.2.2.1 rfl
  have hloop : ¬ r0 a0 a0 := fun hr => by
    have hd : D2 (fD a0) (fD a0) := he a0 a0 hr
    rw [hp.1] at hd
    exact absurd hd (by decide)
  exact hn a0 a0 hloop trivial

/-! ### Which classes leave some two-element object initial -/

/-- Over the primary object class, on every carrier: a class leaves some
two-element object initial exactly when it contains P, contains neither I
nor S, and does not contain both E and NE.  Left to right: I fails at the
one-point self-difference (target 4), S at the three-point full object
(target 5), a class without P at the doubled candidate (target 6), and E
with NE by `not_initial_P_E_NE`.  Right to left: `D2` for the classes
containing E, `FULL2` for the classes containing NE, `D2` again for `{P}`.
This is the carrier-general form of the receipt's
`shape.primary.admitting_classes`. -/
theorem admits_primary_iff (C : MClass) :
    C.AdmitsPrimary ↔ (C.P = true ∧ C.I = false ∧ C.S = false ∧ ¬ (C.E = true ∧ C.NE = true)) := by
  constructor
  · intro ⟨r0, a0, b0, h, hinit⟩
    have hI : C.I = false := by
      cases hi : C.I with
      | false => rfl
      | true =>
        exfalso
        obtain ⟨f, hf, _⟩ := hinit Unit (Full Unit) () () trivial
        exact no_injection_into_point.2 f (hf.2.2.2.1 hi)
    have hS : C.S = false := by
      cases hs : C.S with
      | false => rfl
      | true =>
        exfalso
        obtain ⟨f, hf, _⟩ := hinit (Fin 3) (Full (Fin 3)) 0 0 trivial
        exact no_surjection_onto_three.2 f (hf.2.2.2.2 hs)
    have hP : C.P = true := by
      cases hp : C.P with
      | true => rfl
      | false =>
        exfalso
        obtain ⟨hobj, f1, f2, ⟨t, hne⟩, he1, he2, hn1, hn2⟩ := two_copies_not_unique r0 a0 b0 h
        obtain ⟨f, _, hu⟩ := hinit (Bool × Bool) (Doubled r0) (a0, false) (b0, false) hobj
        have c1 : C.Cond r0 a0 b0 (Doubled r0) (a0, false) (b0, false) f1 :=
          ⟨fun e => (not_both hp e).elim, fun _ => he1, fun _ => hn1,
           fun e => (not_both hI e).elim, fun e => (not_both hS e).elim⟩
        have c2 : C.Cond r0 a0 b0 (Doubled r0) (a0, false) (b0, false) f2 :=
          ⟨fun e => (not_both hp e).elim, fun _ => he2, fun _ => hn2,
           fun e => (not_both hI e).elim, fun e => (not_both hS e).elim⟩
        exact hne ((hu f1 c1 t).trans (hu f2 c2 t).symm)
    refine ⟨hP, hI, hS, fun ⟨hE, hNE⟩ => ?_⟩
    apply not_initial_P_E_NE r0 a0 b0
    intro α r a b hab
    obtain ⟨f, hf, hu⟩ := hinit α r a b hab
    refine ⟨f, ⟨fun _ => hf.1 hP, fun _ => hf.2.1 hE, fun _ => hf.2.2.1 hNE,
      fun e => Bool.noConfusion e, fun e => Bool.noConfusion e⟩, ?_⟩
    intro g hg t
    exact hu g ⟨fun _ => hg.1 rfl, fun _ => hg.2.1 rfl, fun _ => hg.2.2.1 rfl,
      fun e => (not_both hI e).elim, fun e => (not_both hS e).elim⟩ t
  · intro ⟨hP, hI, hS, hEN⟩
    cases hE : C.E with
    | true =>
      refine ⟨D2, false, true, D2_witness, ?_⟩
      intro α r a b h
      obtain ⟨f, ⟨hfp, hfe⟩, hu⟩ := D2_initial_P_E r a b h
      refine ⟨f, ⟨fun _ => hfp, fun _ => hfe, fun hn => absurd ⟨hE, hn⟩ hEN,
        fun e => (not_both hI e).elim, fun e => (not_both hS e).elim⟩, ?_⟩
      intro g hg t
      exact hu g ⟨hg.1 hP, hg.2.1 hE⟩ t
    | false =>
      cases hNE : C.NE with
      | true =>
        refine ⟨FULL2, false, true, trivial, ?_⟩
        intro α r a b h
        obtain ⟨f, ⟨hfp, hfn⟩, hu⟩ := FULL2_initial_P_NE r a b h
        refine ⟨f, ⟨fun _ => hfp, fun e => (not_both hE e).elim, fun _ => hfn,
          fun e => (not_both hI e).elim, fun e => (not_both hS e).elim⟩, ?_⟩
        intro g hg t
        exact hu g ⟨hg.1 hP, hg.2.2.1 hNE⟩ t
      | false =>
        refine ⟨D2, false, true, D2_witness, ?_⟩
        intro α r a b h
        obtain ⟨f, hfp, hu⟩ := two_element_pointed_map_unique r a b h false true (by decide)
        refine ⟨f, ⟨fun _ => hfp, fun e => (not_both hE e).elim, fun e => (not_both hNE e).elim,
          fun e => (not_both hI e).elim, fun e => (not_both hS e).elim⟩, ?_⟩
        intro g hg t
        exact hu g (hg.1 hP) t

/-- The same, listed: over the primary object class exactly `{P}`, `{P,E}`,
and `{P,NE}` leave a two-element object initial, on every carrier -- the
receipt's `shape.primary.admitting_classes` without its bound.  Decided
over the 32 classes. -/
theorem admits_primary_exactly (C : MClass) :
    C.AdmitsPrimary ↔ (C = classP ∨ C = classPE ∨ C = classPNE) := by
  rw [admits_primary_iff]
  obtain ⟨p, e, n, i, s⟩ := C
  cases p <;> cases e <;> cases n <;> cases i <;> cases s <;> decide

/-- Over the secondary object class, on every carrier: a class leaves some
irreflexive two-element object initial exactly when it contains P, does
not contain S, and does not contain both E and NE; I is free there,
because the point-preserving map out of an irreflexive candidate is
injective (target 10).  Left to right: S fails at `n3:01:a0b1` (target
14), a class without P at the doubled irreflexive candidate (target 15),
and E with NE at the objects `D2` and `S2` together, which disagree about
the reverse pair.  Right to left: `D2` for the classes containing E, `S2`
for the classes containing NE, `D2` again otherwise.  This is the
carrier-general form of the receipt's `shape.secondary.admitting_classes`. -/
theorem admits_secondary_iff (C : MClass) :
    C.AdmitsSecondary ↔ (C.P = true ∧ C.S = false ∧ ¬ (C.E = true ∧ C.NE = true)) := by
  constructor
  · intro ⟨r0, a0, b0, hi0, h, hinit⟩
    have hS : C.S = false := by
      cases hs : C.S with
      | false => rfl
      | true =>
        exfalso
        obtain ⟨hi3, h3, hno⟩ := no_surjection_onto_three_irrefl
        obtain ⟨f, hf, _⟩ := hinit (Fin 3) ThreeChain hi3 0 1 h3
        exact hno f (hf.2.2.2.2 hs)
    have hP : C.P = true := by
      cases hp : C.P with
      | true => rfl
      | false =>
        exfalso
        obtain ⟨hirr, hobj, f1, f2, ⟨t, hne⟩, he1, he2, hn1, hn2, hi1, hi2⟩ :=
          two_irrefl_copies_not_unique r0 hi0 a0 b0 h
        obtain ⟨f, _, hu⟩ :=
          hinit (Bool × Bool) (Doubled r0) hirr (a0, false) (b0, false) hobj
        have c1 : C.Cond r0 a0 b0 (Doubled r0) (a0, false) (b0, false) f1 :=
          ⟨fun e => (not_both hp e).elim, fun _ => he1, fun _ => hn1,
           fun _ => hi1, fun e => (not_both hS e).elim⟩
        have c2 : C.Cond r0 a0 b0 (Doubled r0) (a0, false) (b0, false) f2 :=
          ⟨fun e => (not_both hp e).elim, fun _ => he2, fun _ => hn2,
           fun _ => hi2, fun e => (not_both hS e).elim⟩
        exact hne ((hu f1 c1 t).trans (hu f2 c2 t).symm)
    refine ⟨hP, hS, fun ⟨hE, hNE⟩ => ?_⟩
    obtain ⟨fD, hfD, _⟩ := hinit Bool D2 D2_irrefl false true D2_witness
    obtain ⟨fS, hfS, _⟩ := hinit Bool S2 S2_irrefl false true (by decide)
    have hpD : PreservesPoints fD a0 b0 false true := hfD.1 hP
    have heD : PreservesEdges r0 D2 fD := hfD.2.1 hE
    have hpS : PreservesPoints fS a0 b0 false true := hfS.1 hP
    have hnS : PreservesNonEdges r0 S2 fS := hfS.2.2.1 hNE
    have hrev : ¬ r0 b0 a0 := fun hr => by
      have hd : D2 (fD b0) (fD a0) := heD b0 a0 hr
      rw [hpD.1, hpD.2] at hd
      exact absurd hd (by decide)
    have hs : ¬ S2 (fS b0) (fS a0) := hnS b0 a0 hrev
    rw [hpS.1, hpS.2] at hs
    exact hs (by decide)
  · intro ⟨hP, hS, hEN⟩
    cases hE : C.E with
    | true =>
      refine ⟨D2, false, true, D2_irrefl, D2_witness, ?_⟩
      intro α r hi a b h
      obtain ⟨f, ⟨hfp, hfe, hfi⟩, hu⟩ := D2_initial_P_E_I_irrefl r hi a b h
      refine ⟨f, ⟨fun _ => hfp, fun _ => hfe, fun hn => absurd ⟨hE, hn⟩ hEN,
        fun _ => hfi, fun e => (not_both hS e).elim⟩, ?_⟩
      intro g hg t
      exact hu g ⟨hg.1 hP, hg.2.1 hE, pointed_map_injective_of_irrefl hi h false true
        (by decide) g (hg.1 hP)⟩ t
    | false =>
      cases hNE : C.NE with
      | true =>
        refine ⟨S2, false, true, S2_irrefl, by decide, ?_⟩
        intro α r hi a b h
        obtain ⟨f, ⟨hfp, hfn, hfi⟩, hu⟩ := S2_initial_P_NE_I_irrefl r hi a b h
        refine ⟨f, ⟨fun _ => hfp, fun e => (not_both hE e).elim, fun _ => hfn,
          fun _ => hfi, fun e => (not_both hS e).elim⟩, ?_⟩
        intro g hg t
        exact hu g ⟨hg.1 hP, hg.2.2.1 hNE, pointed_map_injective_of_irrefl hi h false true
          (by decide) g (hg.1 hP)⟩ t
      | false =>
        refine ⟨D2, false, true, D2_irrefl, D2_witness, ?_⟩
        intro α r hi a b h
        obtain ⟨f, ⟨hfp, hfi⟩, hu⟩ :=
          two_element_initial_P_I_irrefl r hi a b h false true (by decide)
        refine ⟨f, ⟨fun _ => hfp, fun e => (not_both hE e).elim, fun e => (not_both hNE e).elim,
          fun _ => hfi, fun e => (not_both hS e).elim⟩, ?_⟩
        intro g hg t
        exact hu g ⟨hg.1 hP, pointed_map_injective_of_irrefl hi h false true
          (by decide) g (hg.1 hP)⟩ t

/-- The same, listed: over the secondary object class exactly `{P}`,
`{P,E}`, `{P,NE}`, `{P,I}`, `{P,E,I}`, and `{P,NE,I}` leave an irreflexive
two-element object initial, on every carrier -- the receipt's
`shape.secondary.admitting_classes` without its bound.  Decided over the
32 classes. -/
theorem admits_secondary_exactly (C : MClass) :
    C.AdmitsSecondary ↔
      (C = classP ∨ C = classPE ∨ C = classPNE ∨ C = classPI ∨ C = classPEI ∨ C = classPNEI) := by
  rw [admits_secondary_iff]
  obtain ⟨p, e, n, i, s⟩ := C
  cases p <;> cases e <;> cases n <;> cases i <;> cases s <;> decide

end S9Obligations.MorphismClasses
