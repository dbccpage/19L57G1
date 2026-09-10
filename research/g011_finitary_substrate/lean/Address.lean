import Ordinal

/-!
# Hierarchical Tree Addresses

Pure inductive tree addresses, depth calculation, prefix relations,
and sibling branch disjointness without host pointers or ambient memory.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace FinitarySubstrate

/-- Inductive hierarchical tree address: root or a child along an ordinal branch. -/
inductive Address where
  | root : Address
  | child : Address → Ordinal → Address
  deriving DecidableEq, Repr

namespace Address

/-! ## 1. Identity and Constructor Properties -/

theorem root_ne_child (p : Address) (o : Ordinal) : root ≠ child p o := by
  intro h
  nomatch h

theorem child_ne_root (p : Address) (o : Ordinal) : child p o ≠ root := by
  intro h
  nomatch h

theorem child_inj {p1 p2 : Address} {o1 o2 : Ordinal} (h : child p1 o1 = child p2 o2) :
    p1 = p2 ∧ o1 = o2 := by
  cases h
  exact ⟨rfl, rfl⟩

/-! ## 2. Structural Metrics and Projections -/

/-- Endogenous depth of an address in the tree hierarchy. -/
def depth : Address → Ordinal
  | .root => .zero
  | .child p _ => .succ (depth p)

/-- Structural immediate parent in the tree hierarchy. -/
def parent : Address → Option Address
  | .root => none
  | .child p _ => some p

theorem depth_root : depth root = .zero := rfl

theorem depth_child (p : Address) (o : Ordinal) : depth (child p o) = .succ (depth p) := rfl

theorem parent_root : parent root = none := rfl

theorem parent_child (p : Address) (o : Ordinal) : parent (child p o) = some p := rfl

/-! ## 3. Prefix Relations and Disjointness -/

/-- Decidable prefix relation: `isPrefix a b` is true iff `a` is an ancestor prefix of `b`. -/
def isPrefix (a : Address) : Address → Bool
  | .root => if a == .root then true else false
  | .child p o => if a == .child p o then true else isPrefix a p

/-- Strict prefix relation. -/
def isStrictPrefix (a b : Address) : Bool :=
  isPrefix a b && !(a == b)

/-- Two addresses are disjoint if neither is a prefix of the other. -/
def disjoint (a b : Address) : Bool :=
  !(isPrefix a b) && !(isPrefix b a)

theorem isPrefix_refl (a : Address) : isPrefix a a = true := by
  cases a with
  | root => rfl
  | child p o =>
      change (if child p o == child p o then true else isPrefix (child p o) p) = true
      have h : (child p o == child p o) = true := by
        simp only [beq_self_eq_true]
      rw [h]
      rfl

theorem isPrefix_root (b : Address) : isPrefix root b = true := by
  induction b with
  | root => rfl
  | child p o ih =>
      change (if root == child p o then true else isPrefix root p) = true
      have hne : (root == child p o) = false := by
        cases h : (root == child p o) with
        | false => rfl
        | true =>
            have heq : root = child p o := of_decide_eq_true h
            nomatch heq
      rw [hne]
      exact ih

theorem isPrefix_parent {a p : Address} {o : Ordinal} (h : isPrefix a p = true) :
    isPrefix a (child p o) = true := by
  change (if a == child p o then true else isPrefix a p) = true
  by_cases heq : a = child p o
  · have hbeq : (a == child p o) = true := by
      rw [heq]
      simp only [beq_self_eq_true]
    rw [hbeq]
    rfl
  · have hbeq : (a == child p o) = false := by
      cases h : (a == child p o) with
      | false => rfl
      | true =>
          have heq' : a = child p o := of_decide_eq_true h
          contradiction
    rw [hbeq]
    exact h

theorem isPrefix_depth {a b : Address} (h : isPrefix a b = true) :
    Ordinal.le (depth a) (depth b) = true := by
  induction b generalizing a with
  | root =>
      change (if a == root then true else false) = true at h
      split at h
      · rename_i heq
        have ha : a = root := of_decide_eq_true heq
        rw [ha]
        exact Ordinal.zero_le Ordinal.zero
      · contradiction
  | child p o ih =>
      change (if a == child p o then true else isPrefix a p) = true at h
      split at h
      · rename_i heq
        have ha : a = child p o := of_decide_eq_true heq
        rw [ha]
        exact Ordinal.le_refl (depth (child p o))
      · rename_i hne
        have hp : isPrefix a p = true := h
        have ih_le : Ordinal.le (depth a) (depth p) = true := ih hp
        have h_succ : Ordinal.le (depth p) (.succ (depth p)) = true :=
          Ordinal.le_succ_self (depth p)
        exact Ordinal.le_trans ih_le h_succ

theorem not_isPrefix_child_parent (p : Address) (o : Ordinal) :
    isPrefix (child p o) p = false := by
  cases h : isPrefix (child p o) p with
  | false => rfl
  | true =>
      have hle := isPrefix_depth h
      change Ordinal.le (.succ (depth p)) (depth p) = true at hle
      have h_lt : Ordinal.lt (depth p) (depth p) = true := hle
      have h_ir : Ordinal.lt (depth p) (depth p) = false := Ordinal.lt_irrefl (depth p)
      rw [h_ir] at h_lt
      contradiction

theorem disjoint_siblings {p : Address} {o1 o2 : Ordinal} (h : o1 ≠ o2) :
    disjoint (child p o1) (child p o2) = true := by
  have hne1 : (child p o1 == child p o2) = false := by
    cases hb : (child p o1 == child p o2) with
    | false => rfl
    | true =>
        have heq : child p o1 = child p o2 := of_decide_eq_true hb
        have ⟨_, ho⟩ := child_inj heq
        exact False.elim (h ho)
  have hne2 : (child p o2 == child p o1) = false := by
    cases hb : (child p o2 == child p o1) with
    | false => rfl
    | true =>
        have heq : child p o2 = child p o1 := of_decide_eq_true hb
        have ⟨_, ho⟩ := child_inj heq
        exact False.elim (h ho.symm)
  have hp1 : isPrefix (child p o1) (child p o2) = false := by
    change (if child p o1 == child p o2 then true else isPrefix (child p o1) p) = false
    rw [hne1]
    exact not_isPrefix_child_parent p o1
  have hp2 : isPrefix (child p o2) (child p o1) = false := by
    change (if child p o2 == child p o1 then true else isPrefix (child p o2) p) = false
    rw [hne2]
    exact not_isPrefix_child_parent p o2
  change (!(isPrefix (child p o1) (child p o2)) && !(isPrefix (child p o2) (child p o1))) = true
  rw [hp1, hp2]
  rfl

theorem disjoint_symm (a b : Address) : disjoint a b = disjoint b a := by
  change (!(isPrefix a b) && !(isPrefix b a)) = (!(isPrefix b a) && !(isPrefix a b))
  exact Bool.and_comm (!(isPrefix a b)) (!(isPrefix b a))

theorem disjoint_irrefl (a : Address) : disjoint a a = false := by
  change (!(isPrefix a a) && !(isPrefix a a)) = false
  rw [isPrefix_refl a]
  rfl

end Address

end FinitarySubstrate
