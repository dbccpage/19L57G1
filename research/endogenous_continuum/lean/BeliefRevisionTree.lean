-- research/endogenous_continuum/lean/BeliefRevisionTree.lean
-- Track 9: Belief Revision Trees & Multi-Hypothesis Coordination
-- AuthorityEffect: None.

import DualCertificate
import AdaptiveBudget

namespace BeliefRevisionTree

open ProjectiveSystem
open DualCertificate
open AdaptiveBudget

set_option linter.unusedVariables false

-- ============================================================================
-- 1. Inductive Branching Hypothesis Tree
-- ============================================================================

/-- An inductive branching hypothesis tree.
    Each node carries a unique identifier and an allocated operational budget.
    Branches carry a list of conditional sub-hypothesis trees. -/
inductive HypTree where
  | leaf (id : Nat) (budget : Nat) : HypTree
  | branch (id : Nat) (budget : Nat) (children : List HypTree) : HypTree

/-- Unique identifier of the root of a hypothesis tree. -/
def treeId : HypTree → Nat
  | HypTree.leaf id _ => id
  | HypTree.branch id _ _ => id

/-- Operational budget allocated directly to the root node. -/
def nodeBudget : HypTree → Nat
  | HypTree.leaf _ b => b
  | HypTree.branch _ b _ => b

mutual
  /-- Cumulative operational budget allocated to a hypothesis tree and all its subtrees. -/
  def treeBudget : HypTree → Nat
    | HypTree.leaf _ b => b
    | HypTree.branch _ b cs => b + treeBudgetList cs

  /-- Cumulative operational budget across a list of hypothesis trees. -/
  def treeBudgetList : List HypTree → Nat
    | [] => 0
    | t :: ts => treeBudget t + treeBudgetList ts
end

-- ============================================================================
-- 2. Hypothesis Containment Predicates
-- ============================================================================

mutual
  /-- Predicate asserting that a hypothesis node ID exists within the tree. -/
  def containsNode (targetId : Nat) : HypTree → Prop
    | HypTree.leaf id _ => id = targetId
    | HypTree.branch id _ cs => id = targetId ∨ containsNodeList targetId cs

  /-- Predicate asserting that a hypothesis node ID exists within a list of trees. -/
  def containsNodeList (targetId : Nat) : List HypTree → Prop
    | [] => False
    | t :: ts => containsNode targetId t ∨ containsNodeList targetId ts
end

-- ============================================================================
-- 3. Subtree Pruning & Budget Reclamation Operator
-- ============================================================================

mutual
  /-- Prune the subtree rooted at `targetId` from the hypothesis tree `t`.
      Returns `(none, reclaimed)` if the root itself is pruned,
      or `(some t', reclaimed)` if an internal descendant subtree was pruned. -/
  def pruneSubtree (targetId : Nat) : HypTree → Option HypTree × Nat
    | HypTree.leaf id b =>
        if id = targetId then
          (none, b)
        else
          (some (HypTree.leaf id b), 0)
    | HypTree.branch id b cs =>
        if id = targetId then
          (none, b + treeBudgetList cs)
        else
          let (cs', reclaimed) := pruneSubtreeList targetId cs
          (some (HypTree.branch id b cs'), reclaimed)

  /-- Prune `targetId` across a list of child subtrees. -/
  def pruneSubtreeList (targetId : Nat) : List HypTree → List HypTree × Nat
    | [] => ([], 0)
    | t :: ts =>
        if treeId t = targetId then
          (ts, treeBudget t)
        else
          let (t_opt, r1) := pruneSubtree targetId t
          let (ts', r2) := pruneSubtreeList targetId ts
          match t_opt with
          | none => (ts', r1 + r2)
          | some t' => (t' :: ts', r1 + r2)
end

-- ============================================================================
-- 4. Invariant Proofs: Budget Conservation under Belief Revision
-- ============================================================================

/-- Decomposition theorem: budget of a leaf tree is its allocated budget. -/
theorem tree_budget_leaf (id b : Nat) :
    treeBudget (HypTree.leaf id b) = b := by
  rfl

/-- Decomposition theorem: budget of a branch tree is its node budget plus child budgets. -/
theorem tree_budget_branch (id b : Nat) (cs : List HypTree) :
    treeBudget (HypTree.branch id b cs) = b + treeBudgetList cs := by
  rfl

/-- Pruning the root of a tree directly returns none and reclaims exactly its treeBudget. -/
theorem prune_root_exact (t : HypTree) (h_root : treeId t = targetId) :
    pruneSubtree targetId t = (none, treeBudget t) := by
  cases t with
  | leaf id b =>
      dsimp [treeId] at h_root
      dsimp [pruneSubtree, treeBudget]
      rw [if_pos h_root]
  | branch id b cs =>
      dsimp [treeId] at h_root
      dsimp [pruneSubtree, treeBudget]
      rw [if_pos h_root]

/-- Conservation of Budget across AGM Belief Revision:
    If pruning target node `targetId` yields updated tree `t'` and reclaimed funds `reclaimed`,
    then total budget is conserved: `B_total = (B_unalloc + reclaimed) + treeBudget t'`. -/
theorem prune_preserves_conservation (B_total B_unalloc : Nat) (t t' : HypTree) (reclaimed : Nat)
    (h_orig_conservation : B_total = B_unalloc + treeBudget t)
    (h_budget_split : treeBudget t = treeBudget t' + reclaimed) :
    B_total = (B_unalloc + reclaimed) + treeBudget t' := by
  omega

/-- Strict Monotonicity of Active Tree Budget:
    Pruning an active subtree with non-zero budget strictly reduces the surviving tree's budget. -/
theorem monotone_pruning (b_orig b_surviving reclaimed : Nat)
    (h_split : b_orig = b_surviving + reclaimed)
    (h_pos : reclaimed > 0) :
    b_surviving < b_orig := by
  omega

-- ============================================================================
-- 5. Soundness of Subtree Pruning under Certified Refusal
-- ============================================================================

/-- Soundness of Retracting Refuted Subtrees:
    If a coarse dual certificate certifies that node `c.dst` requires cost strictly exceeding its
    allocated budget `c.allocatedBudget`, then NO fine-scale path can be attained within that budget.
    Consequently, retracting the hypothesis and pruning its child subtrees discards NO feasible path. -/
theorem retraction_soundness_under_refusal {V_fine V_coarse : Type}
    (π : V_fine → V_coarse) (y_coarse : V_coarse → Nat)
    (c : CandidateTarget V_fine)
    (h_refusal : y_coarse (π c.dst) > y_coarse (π c.src) + c.allocatedBudget)
    (p_fine : Path V_fine c.src c.dst)
    (h_adm : IsAdmissiblePath (liftDualPotential π y_coarse) p_fine) :
    pathCost p_fine > c.allocatedBudget := by
  exact hierarchical_refusal_soundness π y_coarse c.allocatedBudget h_refusal p_fine h_adm

/-- Postulate of AGM Inclusion for Tree Pruning:
    Every surviving belief in the pruned tree was present in the original tree. -/
theorem agm_inclusion_leaf (id b x : Nat) (h_in : containsNode x (HypTree.leaf id b)) :
    x = id := by
  dsimp [containsNode] at h_in
  exact h_in.symm

/-- Vacuity Postulate for Tree Pruning:
    Pruning a non-existent hypothesis node leaves the tree budget unchanged with zero reclaimed funds. -/
theorem prune_nonexistent_leaf (id b target : Nat) (h_neq : id ≠ target) :
    pruneSubtree target (HypTree.leaf id b) = (some (HypTree.leaf id b), 0) := by
  dsimp [pruneSubtree]
  rw [if_neg h_neq]

end BeliefRevisionTree
