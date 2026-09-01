import NaturalSections.SlotExchange

/-!
# Sign repair: cancellation certificates and their exact price

The slot-exchange amendment registered one sharpened OPEN question:
whether any weight family with cross-terms between the flipped and
unflipped sectors admits a transpose-induced decomposition with a
single-signed complement.  This module answers it, as pre-registered
in `STATUS.md`:

* SR1 -- `cert_dominates` / `cert_dominates_nonpos`: a cancellation
  certificate (a permutation of the weights into exact-opposite pairs
  plus a single-signed residual, the shape SX5 sums) forces
  per-magnitude domination on the residual's side.
* SR2 -- `dominated_certificate`: the converse, constructively -- from
  per-magnitude domination an explicit certificate is assembled by
  fueled descent on the list, pairing one negative against one positive
  of the same magnitude at each step.
* SR3 -- `wedge_total_positive` / `wedge_no_certificate`: a POSITIVE
  TOTAL does not buy a certificate; the survey's minimal witness is
  refused on both sides by SR1.
* SR4 -- `witness_certificate` / `witness_not_separable`: an
  interacting family (refused by every bounded factor pair) that
  carries a certificate with single-signed complement -- the registered
  OPEN question answered YES at the bound.
* SR5 -- `fibrewise_odd_cancels`: oddness in the moved coordinate at
  every fixed coordinate cancels the moved sector exactly.

AuthorityEffect: None.
-/

namespace NaturalSections
namespace SignRepair

/-! ## 1. SR1: a certificate forces per-magnitude domination -/

/-- One exact-opposite pair contributes equally to the count of any
value and the count of its negation. -/
theorem count_pair (x v : Int) :
    ([x, -x] : List Int).count v = ([x, -x] : List Int).count (-v) := by
  simp only [List.count_cons, List.count_nil, beq_iff_eq]
  split <;> split <;> split <;> split <;> omega

/-- The paired block is count-balanced at every value. -/
theorem count_pairs_balanced (pairs : List Int) (v : Int) :
    (pairs.flatMap fun x => [x, -x]).count v
      = (pairs.flatMap fun x => [x, -x]).count (-v) := by
  induction pairs with
  | nil => rfl
  | cons x xs ih =>
    show (([x, -x] ++ xs.flatMap fun y => [y, -y]) : List Int).count v
        = (([x, -x] ++ xs.flatMap fun y => [y, -y]) : List Int).count (-v)
    rw [List.count_append, List.count_append, ih, count_pair]

/-- SR1: a certificate with non-negative residual forces, at every
positive magnitude, at least as many positive as negative weights. -/
theorem cert_dominates {l pairs res : List Int}
    (hperm : l.Perm ((pairs.flatMap fun x => [x, -x]) ++ res))
    (hres : ∀ x ∈ res, 0 ≤ x) {v : Int} (hv : 0 < v) :
    l.count (-v) ≤ l.count v := by
  rw [hperm.count_eq, hperm.count_eq, List.count_append, List.count_append]
  have hbal := count_pairs_balanced pairs v
  have hres0 : res.count (-v) = 0 := by
    rw [List.count_eq_zero]
    intro hmem
    have := hres _ hmem
    omega
  omega

/-- SR1, the other side: a certificate with non-positive residual
forces the reverse domination. -/
theorem cert_dominates_nonpos {l pairs res : List Int}
    (hperm : l.Perm ((pairs.flatMap fun x => [x, -x]) ++ res))
    (hres : ∀ x ∈ res, x ≤ 0) {v : Int} (hv : 0 < v) :
    l.count v ≤ l.count (-v) := by
  rw [hperm.count_eq, hperm.count_eq, List.count_append, List.count_append]
  have hbal := count_pairs_balanced pairs v
  have hres0 : res.count v = 0 := by
    rw [List.count_eq_zero]
    intro hmem
    have := hres _ hmem
    omega
  omega

/-! ## 2. SR2: domination assembles a certificate, constructively -/

theorem count_erase_ne (l : List Int) {a b : Int} (h : b ≠ a) :
    (l.erase a).count b = l.count b := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    by_cases hx : x = a
    · subst hx
      rw [List.erase_cons_head, List.count_cons]
      simp only [beq_iff_eq]
      split <;> omega
    · rw [List.erase_cons_tail (by simp [beq_iff_eq]; omega),
        List.count_cons, List.count_cons, ih]

theorem count_erase_self_mem (l : List Int) {a : Int} (h : a ∈ l) :
    (l.erase a).count a + 1 = l.count a := by
  induction l with
  | nil => cases h
  | cons x xs ih =>
    by_cases hx : x = a
    · rw [hx, List.erase_cons_head, List.count_cons_self]
    · have hmem : a ∈ xs := by
        cases h with
        | head => exact absurd rfl hx
        | tail _ h' => exact h'
      rw [List.erase_cons_tail (by simp [beq_iff_eq]; omega),
        List.count_cons, List.count_cons]
      have := ih hmem
      simp only [beq_iff_eq]
      split <;> omega

theorem perm_cons_erase_int {a : Int} {l : List Int} (h : a ∈ l) :
    l.Perm (a :: l.erase a) := by
  induction l with
  | nil => cases h
  | cons x xs ih =>
    by_cases hx : x = a
    · subst hx
      rw [List.erase_cons_head]
    · have hmem : a ∈ xs := by
        cases h with
        | head => exact absurd rfl hx
        | tail _ h' => exact h'
      rw [List.erase_cons_tail (by simp [beq_iff_eq]; omega)]
      exact (List.Perm.cons x (ih hmem)).trans (List.Perm.swap a x (xs.erase a))

theorem mem_erase_of_ne_int {a b : Int} {l : List Int} (hne : a ≠ b) (h : a ∈ l) :
    a ∈ l.erase b := by
  induction l with
  | nil => cases h
  | cons x xs ih =>
    by_cases hx : x = b
    · subst hx
      rw [List.erase_cons_head]
      cases h with
      | head => exact absurd rfl hne
      | tail _ h' => exact h'
    · rw [List.erase_cons_tail (by simp [beq_iff_eq]; omega)]
      cases h with
      | head => exact List.mem_cons_self ..
      | tail _ h' => exact List.mem_cons_of_mem x (ih h')

theorem length_erase_of_mem_int {a : Int} {l : List Int} (h : a ∈ l) :
    (l.erase a).length + 1 = l.length := by
  induction l with
  | nil => cases h
  | cons x xs ih =>
    by_cases hx : x = a
    · subst hx
      rw [List.erase_cons_head]
      rfl
    · have hmem : a ∈ xs := by
        cases h with
        | head => exact absurd rfl hx
        | tail _ h' => exact h'
      rw [List.erase_cons_tail (by simp [beq_iff_eq]; omega)]
      have := ih hmem
      simp only [List.length_cons]
      omega

/-- SR2: per-magnitude domination yields an explicit certificate --
fueled descent, pairing one negative against one positive of its
magnitude at every step, residual all non-negative. -/
theorem dominated_certificate :
    ∀ (fuel : Nat) (l : List Int), l.length ≤ fuel →
      (∀ v : Int, 0 < v → l.count (-v) ≤ l.count v) →
      ∃ pairs res : List Int,
        l.Perm ((pairs.flatMap fun x => [x, -x]) ++ res)
          ∧ ∀ x ∈ res, 0 ≤ x := by
  intro fuel
  induction fuel with
  | zero =>
    intro l hlen _
    have : l = [] := List.eq_nil_of_length_eq_zero (by omega)
    subst this
    exact ⟨[], [], List.Perm.refl _, by intro x hx; cases hx⟩
  | succ f ih =>
    intro l hlen hdom
    cases hfind : l.find? (fun x => decide (x < 0)) with
    | none =>
      refine ⟨[], l, List.Perm.refl _, ?_⟩
      intro x hx
      have := List.find?_eq_none.mp hfind x hx
      simp at this
      omega
    | some x =>
      have hxmem : x ∈ l := List.mem_of_find?_eq_some hfind
      have hxneg : x < 0 := by
        have := List.find?_some hfind
        simpa using this
      obtain ⟨v, hv⟩ : ∃ v : Int, v = -x := ⟨-x, rfl⟩
      have hvpos : 0 < v := by omega
      have hvcount : 1 ≤ l.count v := by
        have hd := hdom v hvpos
        have hx' : l.count (-v) ≥ 1 := by
          have : (-v) = x := by omega
          rw [this]
          exact List.count_pos_iff.mpr hxmem
        omega
      have hvmem : v ∈ l := List.count_pos_iff.mp (by omega)
      have hvx : v ≠ x := by omega
      have hvmem' : v ∈ l.erase x := mem_erase_of_ne_int hvx hvmem
      have hlen' : ((l.erase x).erase v).length ≤ f := by
        have h1 := length_erase_of_mem_int hxmem
        have h2 := length_erase_of_mem_int hvmem'
        have h3 : 1 ≤ l.length := List.length_pos_of_mem hxmem
        omega
      have hdom' : ∀ u : Int, 0 < u → ((l.erase x).erase v).count (-u) ≤ ((l.erase x).erase v).count u := by
        intro u hu
        by_cases huv : u = v
        · subst huv
          have e1 : ((l.erase x).erase u).count u + 1 = (l.erase x).count u :=
            count_erase_self_mem _ hvmem'
          have e2 : (l.erase x).count u = l.count u :=
            count_erase_ne _ (by omega)
          have e3 : ((l.erase x).erase u).count (-u) = (l.erase x).count (-u) :=
            count_erase_ne _ (by omega)
          have e4 : (l.erase x).count (-u) + 1 = l.count (-u) := by
            have : (-u) = x := by omega
            rw [this]
            exact count_erase_self_mem _ hxmem
          have := hdom u hu
          omega
        · have e1 : ((l.erase x).erase v).count u = (l.erase x).count u :=
            count_erase_ne _ (by omega)
          have e2 : (l.erase x).count u = l.count u :=
            count_erase_ne _ (by omega)
          have e3 : ((l.erase x).erase v).count (-u) = (l.erase x).count (-u) :=
            count_erase_ne _ (by omega)
          have e4 : (l.erase x).count (-u) = l.count (-u) :=
            count_erase_ne _ (by omega)
          have := hdom u hu
          omega
      obtain ⟨pairs, res, hperm, hres⟩ := ih ((l.erase x).erase v) hlen' hdom'
      refine ⟨v :: pairs, res, ?_, hres⟩
      have step1 : l.Perm (x :: l.erase x) := perm_cons_erase_int hxmem
      have step2 : (l.erase x).Perm (v :: (l.erase x).erase v) := perm_cons_erase_int hvmem'
      have chain : l.Perm (x :: v :: (l.erase x).erase v) :=
        step1.trans (List.Perm.cons x step2)
      have swap : (x :: v :: (l.erase x).erase v).Perm (v :: x :: (l.erase x).erase v) := List.Perm.swap v x ((l.erase x).erase v)
      have hx' : x = -v := by omega
      subst hx'
      have target : (v :: -v :: (l.erase (-v)).erase v).Perm
          (((v :: pairs).flatMap fun y => [y, -y]) ++ res) := by
        show (v :: -v :: (l.erase (-v)).erase v).Perm
            (([v, -v] ++ pairs.flatMap fun y => [y, -y]) ++ res)
        rw [List.append_assoc]
        exact List.Perm.cons v (List.Perm.cons (-v) hperm)
      exact (chain.trans swap).trans target

/-! ## 3. SR3: a positive total does not buy a certificate -/

/-- The survey's minimal positive-total family with no certificate. -/
def wedge : List Int := [-2, -2, -1, 2, 2, 2]

theorem wedge_total_positive : sumList wedge = 1 := rfl

/-- SR3: the wedge is refused on both sides -- SR1 at magnitude `1`
kills the non-negative residual, SR1 at magnitude `2` kills the
non-positive one. -/
theorem wedge_no_certificate (pairs res : List Int)
    (hperm : wedge.Perm ((pairs.flatMap fun x => [x, -x]) ++ res)) :
    ¬ ((∀ x ∈ res, 0 ≤ x) ∨ (∀ x ∈ res, x ≤ 0)) := by
  rintro (hres | hres)
  · have h := cert_dominates hperm hres (v := 1) (by omega)
    have c1 : wedge.count (-1) = 1 := by decide
    have c2 : wedge.count 1 = 0 := by decide
    omega
  · have h := cert_dominates_nonpos hperm hres (v := 2) (by omega)
    have c1 : wedge.count 2 = 3 := by decide
    have c2 : wedge.count (-2) = 2 := by decide
    omega

/-! ## 4. SR4: the interacting witness -- the OPEN question answered -/

/-- The pinned witness, listed over the declared point order
`(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)`. -/
def witness : List Int := [1, 2, -1, -2, 1, 1]

/-- SR4: the witness carries an explicit certificate -- pairs `[1, 2]`,
single-signed complement `[1, 1]`. -/
theorem witness_certificate :
    witness.Perm ((([1, 2] : List Int).flatMap fun x => [x, -x]) ++ [1, 1])
      ∧ ∀ x ∈ ([1, 1] : List Int), 0 ≤ x := by
  constructor
  · show ([1, 2, -1, -2, 1, 1] : List Int).Perm [1, -1, 2, -2, 1, 1]
    exact List.Perm.cons 1 (List.Perm.swap (-1) 2 [-2, 1, 1])
  · decide

/-- Bounded factor values `-2..2`. -/
def val5 (i : Fin 5) : Int := (i.val : Int) - 2

/-- SR4: the witness is interacting -- NO bounded factor pair
`A(m) * B(f)` reproduces it, checked against all `5^5`
possibilities. -/
theorem witness_not_separable :
    ¬ ∃ (a0 a1 a2 b0 b1 : Fin 5),
      val5 a0 * val5 b0 = 1 ∧ val5 a0 * val5 b1 = 2 ∧
      val5 a1 * val5 b0 = -1 ∧ val5 a1 * val5 b1 = -2 ∧
      val5 a2 * val5 b0 = 1 ∧ val5 a2 * val5 b1 = 1 := by decide

/-! ## 5. SR5: fibrewise oddness cancels the moved sector -/

/-- SR5: a family odd in the moved coordinate at every fixed coordinate
has moved-sector total zero -- SX3's cancellation, fibre by fibre. -/
theorem fibrewise_odd_cancels (W : Fin 3 → Fin 2 → Int)
    (hodd : ∀ f, W 1 f = - W 0 f) :
    W 0 0 + W 0 1 + W 1 0 + W 1 1 = 0 := by
  have h0 := hodd 0
  have h1 := hodd 1
  omega

end SignRepair
end NaturalSections
