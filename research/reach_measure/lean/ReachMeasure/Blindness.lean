/-!
# A base-free measure cannot separate a local response from a global one

The sealed measures are functions of the response alone.  `mu1` is the item
count; `mu2` refines it by new-form arity sum.  Neither reads the state the
response is applied to.

This file proves that no such measure can distinguish a single instance --
which makes one plugging derivable -- from a single uniform rule -- which
makes every plugging of its form derivable at once.  The two responses have
the same item count and the same new-form arity sum, so any measure that
factors through that pair assigns them the same cost, whatever the measure
is.  The result is about the FORM of the measure, not about any particular
choice of one.

The companion statement is the useful direction: a measure that does
separate them provably does not factor through the sealed pair, so it must
read something else.  Reach reads the base, and `sealed_side.py` exhibits
the same uniform rule with reach `1` on one pinned base and `19` on another
while `mu1 = 1` and `mu2 = (1, 0)` on both.

The last section shows that no constant bounds the gap, so the blindness
is not something a constant re-weighting could repair.

Core Lean only: no `Mathlib`, no choice principle, and no proof left
incomplete.  `AuthorityEffect: None.`
-/

namespace ReachMeasure

/-! ## 1. The sealed item grammar and the sealed measures -/

/-- The four item kinds of the sealed candidate grammar.  Arguments are
dropped: nothing below depends on them, and their absence makes the
blindness result sharper rather than weaker. -/
inductive Item where
  | datum : Item
  | form : Nat → Item
  | inst : Item
  | rule : Item
deriving DecidableEq, Repr

/-- New-form arity, zero on every other kind. -/
def arity : Item → Nat
  | Item.form a => a
  | _ => 0

def sumArity : List Item → Nat
  | [] => 0
  | it :: rest => arity it + sumArity rest

/-- The sealed item count. -/
def mu1 (d : List Item) : Nat := d.length

/-- The sealed refined measure: item count, then new-form arity sum. -/
def mu2 (d : List Item) : Nat × Nat := (d.length, sumArity d)

/-! ## 2. The two responses the measures cannot tell apart -/

/-- One instance: makes a single plugging derivable. -/
def localResponse : List Item := [Item.inst]

/-- One uniform rule: makes every plugging of its form derivable at once. -/
def globalResponse : List Item := [Item.rule]

theorem mu1_agree : mu1 localResponse = mu1 globalResponse := rfl

theorem mu2_agree : mu2 localResponse = mu2 globalResponse := rfl

/-- The two responses are nonetheless different responses. -/
theorem responses_differ : localResponse ≠ globalResponse := by decide

/-! ## 3. Blindness -/

/-- **Any measure that factors through the sealed pair is blind.**  If a
measure gives equal costs to responses of equal `mu2`, then it gives the
local and the global response the same cost.  Stated for an arbitrary
target type, so it covers numeric costs, tuples, orders, and anything
else. -/
theorem base_free_is_blind {β : Type} (G : List Item → β)
    (hfactors : ∀ d e : List Item, mu2 d = mu2 e → G d = G e) :
    G localResponse = G globalResponse :=
  hfactors localResponse globalResponse mu2_agree

/-- The same for a measure presented as a function OF the sealed pair,
which is the shape `mu1` and `mu2` actually have. -/
theorem of_mu2_is_blind {β : Type} (F : Nat × Nat → β) :
    F (mu2 localResponse) = F (mu2 globalResponse) := by
  rw [mu2_agree]

/-- **The useful direction.**  A measure that separates the local response
from the global one does not factor through the sealed pair: it must read
something the sealed measures do not.  This is why the reach measure takes
the base as an argument, and it is the whole justification for a
base-relative measure. -/
theorem separating_is_not_base_free {β : Type} (G : List Item → β)
    (hsep : G localResponse ≠ G globalResponse) :
    ¬ (∀ d e : List Item, mu2 d = mu2 e → G d = G e) :=
  fun hfactors => hsep (base_free_is_blind G hfactors)

/-! ## 4. No constant bounds the gap

A uniform rule over an `a`-ary form on a state of `n` data makes `n ^ a`
pluggings derivable; an instance makes one.  So the two responses differ by
an amount the state itself sets, and no constant re-weighting of a
base-free measure could stand in for reading the base. -/

/-- The pluggings a uniform rule over an `a`-ary form reaches, on `n`
data. -/
def ruleReach (n a : Nat) : Nat := n ^ a

/-- The pluggings a single instance reaches. -/
def instReach : Nat := 1

theorem instReach_eq_one : instReach = 1 := rfl

/-- At arity one the rule's reach is the size of the state. -/
theorem ruleReach_arity_one (n : Nat) : ruleReach n 1 = n := by
  show n ^ 1 = n
  simp

/-- **No constant separates them.**  For every bound `k` there is a state
on which a single uniform rule out-reaches a single instance by more than
`k`.  So the difference the sealed measures cannot see exceeds every
constant, and cannot be absorbed into a fixed weight. -/
theorem gap_unbounded (k : Nat) :
    ∃ n : Nat, ruleReach n 1 ≥ instReach + k := by
  refine ⟨1 + k, ?_⟩
  rw [ruleReach_arity_one]
  show 1 + k ≥ 1 + k
  exact Nat.le_refl _

/-- And the gap is monotone in the state: a larger state makes the same
rule reach further, while the instance is unmoved. -/
theorem ruleReach_monotone {m n : Nat} (h : m ≤ n) :
    ruleReach m 1 ≤ ruleReach n 1 := by
  rw [ruleReach_arity_one, ruleReach_arity_one]
  exact h

end ReachMeasure
