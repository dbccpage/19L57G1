-- research/endogenous_continuum/lean/HypothesisTree.lean
-- Track 9: Branching hypothesis trees and subtree retraction
-- AuthorityEffect: None.

/-!
# Track 9: Branching hypothesis trees

A finite tree of hypotheses: every node carries an identifier and a
natural-number budget. `pruneSubtree k t` removes every subtree of `t` whose root
carries the identifier `k` and returns the budget those subtrees held. Nothing
here assumes that identifiers are unique.

Proved for every tree and every identifier:

* `prune_split`: the surviving tree's budget plus the reclaimed amount equals
  the original budget;
* `prune_conserves_total`: a ledger `total = unallocated + treeBudget t` stays
  balanced when the reclaimed amount moves to the unallocated pool;
* `prune_shrinks_of_pos`: a positive reclaimed amount strictly shrinks the tree;
* `prune_inclusion`: every identifier left after pruning was present before;
* `prune_success`: the identifier `k` is gone after pruning `k`;
* `prune_absent_unchanged`: pruning an absent identifier returns the tree
  unchanged and reclaims nothing.

Scope: this models structural removal over natural-number budgets. The Python
tree (`hypothesis_tree.py`) deactivates nodes in place over exact rationals and
refuses duplicate identifiers; the correspondence between the two is not proved.
-/

namespace HypothesisTree

-- ============================================================================
-- 1. Trees, budgets, identifiers
-- ============================================================================

/-- A branching hypothesis tree: a leaf, or a node with a list of subtrees.
    Each node carries an identifier and a budget. -/
inductive HypTree where
  | leaf (id : Nat) (budget : Nat) : HypTree
  | branch (id : Nat) (budget : Nat) (children : List HypTree) : HypTree

/-- Identifier of the root of a tree. -/
def treeId : HypTree → Nat
  | HypTree.leaf id _ => id
  | HypTree.branch id _ _ => id

mutual
  /-- Budget held by a tree and all its subtrees. -/
  def treeBudget : HypTree → Nat
    | HypTree.leaf _ b => b
    | HypTree.branch _ b cs => b + treeBudgetList cs

  /-- Budget held by a list of trees. -/
  def treeBudgetList : List HypTree → Nat
    | [] => 0
    | t :: ts => treeBudget t + treeBudgetList ts
end

mutual
  /-- The identifier `targetId` occurs somewhere in the tree. -/
  def containsNode (targetId : Nat) : HypTree → Prop
    | HypTree.leaf id _ => id = targetId
    | HypTree.branch id _ cs => id = targetId ∨ containsNodeList targetId cs

  /-- The identifier `targetId` occurs somewhere in a list of trees. -/
  def containsNodeList (targetId : Nat) : List HypTree → Prop
    | [] => False
    | t :: ts => containsNode targetId t ∨ containsNodeList targetId ts
end

/-- Budget of an optional tree; `none` (the whole tree was removed) holds none. -/
def optBudget : Option HypTree → Nat
  | none => 0
  | some t => treeBudget t

/-- The identifier occurs in an optional tree; `none` contains nothing. -/
def optContains (x : Nat) : Option HypTree → Prop
  | none => False
  | some t => containsNode x t

-- ============================================================================
-- 2. Subtree removal and the reclaimed budget
-- ============================================================================

mutual
  /-- Remove every subtree whose root carries `targetId`.
      Returns the surviving tree (`none` if the root itself is removed) and the
      budget held by the removed subtrees. -/
  def pruneSubtree (targetId : Nat) : HypTree → Option HypTree × Nat
    | HypTree.leaf id b =>
        if id = targetId then (none, b) else (some (HypTree.leaf id b), 0)
    | HypTree.branch id b cs =>
        if id = targetId then (none, b + treeBudgetList cs)
        else
          let r := pruneSubtreeList targetId cs
          (some (HypTree.branch id b r.1), r.2)

  /-- Remove every subtree carrying `targetId` from a list of trees. -/
  def pruneSubtreeList (targetId : Nat) : List HypTree → List HypTree × Nat
    | [] => ([], 0)
    | t :: ts =>
        let r1 := pruneSubtree targetId t
        let r2 := pruneSubtreeList targetId ts
        match r1.1 with
        | none => (r2.1, r1.2 + r2.2)
        | some t' => (t' :: r2.1, r1.2 + r2.2)
end

-- ============================================================================
-- 3. Budget decomposition
-- ============================================================================

/-- The budget of a leaf is its own budget. -/
theorem tree_budget_leaf (id b : Nat) :
    treeBudget (HypTree.leaf id b) = b := rfl

/-- The budget of a branch is its own budget plus its subtrees' budgets. -/
theorem tree_budget_branch (id b : Nat) (cs : List HypTree) :
    treeBudget (HypTree.branch id b cs) = b + treeBudgetList cs := rfl

/-- Removing the root removes the whole tree and reclaims all of its budget. -/
theorem prune_root_exact (targetId : Nat) (t : HypTree) (h_root : treeId t = targetId) :
    pruneSubtree targetId t = (none, treeBudget t) := by
  cases t with
  | leaf id b =>
      simp only [treeId] at h_root
      simp [pruneSubtree, treeBudget, h_root]
  | branch id b cs =>
      simp only [treeId] at h_root
      simp [pruneSubtree, treeBudget, h_root]

-- ============================================================================
-- 4. Conservation: surviving budget + reclaimed = original budget
-- ============================================================================

mutual
  /-- Pruning splits a tree's budget exactly into what survives and what is
      reclaimed. -/
  theorem prune_split (k : Nat) : ∀ t : HypTree,
      treeBudget t = optBudget (pruneSubtree k t).1 + (pruneSubtree k t).2
    | .leaf id b => by
        by_cases h : id = k <;> simp [pruneSubtree, treeBudget, optBudget, h]
    | .branch id b cs => by
        have ih := prune_list_split k cs
        by_cases h : id = k
        · simp [pruneSubtree, treeBudget, optBudget, h]
        · simp [pruneSubtree, treeBudget, optBudget, h]
          omega

  /-- The list form of `prune_split`. -/
  theorem prune_list_split (k : Nat) : ∀ ts : List HypTree,
      treeBudgetList ts =
        treeBudgetList (pruneSubtreeList k ts).1 + (pruneSubtreeList k ts).2
    | [] => by simp [pruneSubtreeList, treeBudgetList]
    | t :: ts => by
        have ih1 := prune_split k t
        have ih2 := prune_list_split k ts
        cases h : (pruneSubtree k t).1 with
        | none =>
            simp [h, optBudget] at ih1
            simp [pruneSubtreeList, treeBudgetList, h]
            omega
        | some t' =>
            simp [h, optBudget] at ih1
            simp [pruneSubtreeList, treeBudgetList, h]
            omega
end

/-- A balanced ledger `total = unallocated + treeBudget t` stays balanced when the
    reclaimed budget of a pruning moves to the unallocated pool. -/
theorem prune_conserves_total (k B_total B_unalloc : Nat) (t : HypTree)
    (h_balanced : B_total = B_unalloc + treeBudget t) :
    B_total = (B_unalloc + (pruneSubtree k t).2) + optBudget (pruneSubtree k t).1 := by
  have h := prune_split k t
  omega

/-- A positive reclaimed amount strictly shrinks the tree's budget. -/
theorem prune_shrinks_of_pos (k : Nat) (t : HypTree) (h_pos : 0 < (pruneSubtree k t).2) :
    optBudget (pruneSubtree k t).1 < treeBudget t := by
  have h := prune_split k t
  omega

-- ============================================================================
-- 5. What survives: inclusion, removal of the identifier, absent identifiers
-- ============================================================================

mutual
  /-- Every identifier left after pruning was present before. -/
  theorem prune_inclusion (k x : Nat) : ∀ t : HypTree,
      optContains x (pruneSubtree k t).1 → containsNode x t
    | .leaf id b => by
        by_cases h : id = k <;> simp [pruneSubtree, optContains, containsNode, h]
    | .branch id b cs => by
        have ih := prune_list_inclusion k x cs
        by_cases h : id = k
        · simp [pruneSubtree, optContains, h]
        · simp only [pruneSubtree, h, if_false, optContains, containsNode]
          intro hc
          cases hc with
          | inl hid => exact Or.inl hid
          | inr hcs => exact Or.inr (ih hcs)

  /-- The list form of `prune_inclusion`. -/
  theorem prune_list_inclusion (k x : Nat) : ∀ ts : List HypTree,
      containsNodeList x (pruneSubtreeList k ts).1 → containsNodeList x ts
    | [] => by simp [pruneSubtreeList, containsNodeList]
    | t :: ts => by
        have ih1 := prune_inclusion k x t
        have ih2 := prune_list_inclusion k x ts
        cases h : (pruneSubtree k t).1 with
        | none =>
            simp only [pruneSubtreeList, h, containsNodeList]
            intro hc
            exact Or.inr (ih2 hc)
        | some t' =>
            rw [h] at ih1
            simp only [optContains] at ih1
            simp only [pruneSubtreeList, h, containsNodeList]
            intro hc
            cases hc with
            | inl ht => exact Or.inl (ih1 ht)
            | inr hts => exact Or.inr (ih2 hts)
end

mutual
  /-- After pruning `k`, the identifier `k` no longer occurs. -/
  theorem prune_success (k : Nat) : ∀ t : HypTree, ¬ optContains k (pruneSubtree k t).1
    | .leaf id b => by
        by_cases h : id = k <;> simp [pruneSubtree, optContains, containsNode, h]
    | .branch id b cs => by
        have ih := prune_list_success k cs
        by_cases h : id = k
        · simp [pruneSubtree, optContains, h]
        · simp only [pruneSubtree, h, if_false, optContains, containsNode]
          intro hc
          cases hc with
          | inl hid => exact hid
          | inr hcs => exact ih hcs

  /-- The list form of `prune_success`. -/
  theorem prune_list_success (k : Nat) : ∀ ts : List HypTree,
      ¬ containsNodeList k (pruneSubtreeList k ts).1
    | [] => by simp [pruneSubtreeList, containsNodeList]
    | t :: ts => by
        have ih1 := prune_success k t
        have ih2 := prune_list_success k ts
        cases h : (pruneSubtree k t).1 with
        | none =>
            simp only [pruneSubtreeList, h]
            exact ih2
        | some t' =>
            rw [h] at ih1
            simp only [optContains] at ih1
            simp only [pruneSubtreeList, h, containsNodeList]
            intro hc
            cases hc with
            | inl ht => exact ih1 ht
            | inr hts => exact ih2 hts
end

mutual
  /-- Pruning an identifier that does not occur changes nothing and reclaims
      nothing. -/
  theorem prune_absent_unchanged (k : Nat) : ∀ t : HypTree,
      ¬ containsNode k t → pruneSubtree k t = (some t, 0)
    | .leaf id b => by
        intro h
        simp only [containsNode] at h
        simp [pruneSubtree, h]
    | .branch id b cs => by
        intro h
        simp only [containsNode, not_or] at h
        have hcs := prune_list_absent_unchanged k cs h.2
        simp [pruneSubtree, h.1, hcs]

  /-- The list form of `prune_absent_unchanged`. -/
  theorem prune_list_absent_unchanged (k : Nat) : ∀ ts : List HypTree,
      ¬ containsNodeList k ts → pruneSubtreeList k ts = (ts, 0)
    | [] => by
        intro _
        simp [pruneSubtreeList]
    | t :: ts => by
        intro h
        simp only [containsNodeList, not_or] at h
        have h1 := prune_absent_unchanged k t h.1
        have h2 := prune_list_absent_unchanged k ts h.2
        simp [pruneSubtreeList, h1, h2]
end

end HypothesisTree
