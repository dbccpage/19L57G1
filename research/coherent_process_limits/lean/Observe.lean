import Cycle
import Fork
import Periodic
import TwoLoci

/-!
# Observe: the represented process at finite scales

This module is the family's root.  It imports the studies —
`Observe.Steps` (the machine at scales), `Observe.Chain` (functionality),
`Observe.TwoLoci`, `Observe.Cycle`, `Observe.Periodic`, `Observe.Fork` — all
of which share the namespace `Observe`, so a consumer writing `import
Observe` sees every `Observe.*` name whatever file it now lives in.

What is stated here is the one thing that is about the machine rather than
about any study over it: this family's step, iteration and observation are
the producer family's generic runner at the merged reader.

The file was 1208 lines carrying six studies.  Its numbered section headers
were already the split, and this is that split taken; no proof changed.

AuthorityEffect: None.
-/

namespace Observe

open Derivation Translation Execution Control Product Schedule Runner

/-! ## 7. This family's observation is the generic one at the merged reader

The producer family parameterised the interpreter over an enablement reader
and identified its own step with the generic step at `Runner.ctrlReader`.
This family's `next`, `iter` and `obs` are that machine's, at the same reader,
and the identifications are `rfl` or a one-line induction.

The point is not economy.  It is that the compatibility this family proves
(`obs_prefix_add`) and the compatibility the generic runner proves
(`Runner.obsOf_prefix_add`) are the same theorem, so a second reader — the
record-reading one, the depth-two one — inherits it instead of copying it. -/

theorem next_is_generic (s : State) : next s = Runner.nextOf Runner.ctrlReader s := rfl

theorem iter_is_generic : ∀ (n : Nat) (s : State),
    iter n s = Runner.iterOf Runner.ctrlReader n s
  | 0, _ => rfl
  | n + 1, s => by
      show next (iter n s) = Runner.nextOf Runner.ctrlReader (Runner.iterOf Runner.ctrlReader n s)
      rw [iter_is_generic n s, next_is_generic]

theorem obs_is_generic (n : Nat) (s : State) : obs n s = Runner.obsOf Runner.ctrlReader n s := by
  show (iter n s).tape = (Runner.iterOf Runner.ctrlReader n s).tape
  rw [iter_is_generic n s]

/-- And so this family's compatibility is the generic one, not a second proof
of it. -/
theorem obs_prefix_is_generic (m : Nat) (s : State) (k : Nat) :
    obs m s <+: obs (m + k) s := by
  rw [obs_is_generic m s, obs_is_generic (m + k) s]
  exact Runner.obsOf_prefix_add Runner.ctrlReader m s k

end Observe

#print axioms Observe.iter_is_generic
#print axioms Observe.next_is_generic
#print axioms Observe.obs_is_generic
#print axioms Observe.obs_prefix_is_generic
