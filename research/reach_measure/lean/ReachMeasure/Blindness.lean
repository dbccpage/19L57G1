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
read something else.  It need not read the base: inspecting the response
constructor would also escape that factorisation.  Reach deliberately reads
the base, and `sealed_side.py` exhibits the same uniform rule with reach `1`
on one pinned base and `19` on another while `mu1 = 1` and
`mu2 = (1, 0)` on both.

The last section is an abstract fresh-plugging model.  It shows that its
rule-versus-instance gap has no constant bound.  It does not establish a
correspondence with the Python `reach` function, which subtracts pluggings
already derivable at the base.

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
something the sealed measures do not.  Reading the base is one such choice;
this result does not say it is the only one. -/
theorem separating_is_not_base_free {β : Type} (G : List Item → β)
    (hsep : G localResponse ≠ G globalResponse) :
    ¬ (∀ d e : List Item, mu2 d = mu2 e → G d = G e) :=
  fun hfactors => hsep (base_free_is_blind G hfactors)

/-! ## 4. An abstract fresh-plugging model

The functions below model a base with no previously derivable plugging of
the selected form: a uniform rule reaches `n ^ a` fresh pluggings and an
instance reaches one.  They are not connected here to the reconstructed
Python state or its subtraction of already derivable pluggings. -/

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

/-- In the abstract fresh-plugging model, for every bound `k` there is a
size at which the uniform-rule value exceeds the instance value by more
than `k`. -/
theorem gap_unbounded (k : Nat) :
    ∃ n : Nat, ruleReach n 1 > instReach + k := by
  refine ⟨2 + k, ?_⟩
  rw [ruleReach_arity_one]
  change 1 + k < 2 + k
  exact Nat.add_lt_add_right (by decide) k

/-- The abstract rule value is monotone in its size parameter. -/
theorem ruleReach_monotone {m n : Nat} (h : m ≤ n) :
    ruleReach m 1 ≤ ruleReach n 1 := by
  rw [ruleReach_arity_one, ruleReach_arity_one]
  exact h

end ReachMeasure
