import Chain

/-!
# Observe.TwoLoci: the observation of a two-locus run

The producer family builds two loci as a product carrier, proves the
independence square of the *operations*, and runs them by a schedule carried in
the data.  What this family owes is the square as a statement about
**observations**, and `obs_one_locus` is it.

Read it two-sidedly: the square itself does **not** lift — two orders reach the
same datum and record different tapes — and what does lift is the projection
with the adjacent repeats dropped.

AuthorityEffect: None.
-/

namespace Observe

open Derivation Translation Execution Control Product Schedule Runner

/-! ## 2c. Two loci: the observation moves one at a time

The producer family builds two loci as a product carrier, proves the
independence square of the *operations*, and runs them by a schedule carried
in the data.  What this family owes is the square as a statement about
**observations**, and this is it: along a whole run, at every scale, from
every start and with any fuel, consecutive entries of the observed tape
differ in at most one locus.

It is the same chain invariant as `obs_functional`, read through the
product's locality theorems rather than through determinism.  No admissible
range is assumed: the enablement instance the machine reads is what places
the datum in the carrier, so the hypothesis is the program and nothing else.
-/


/-- An operation of a product setting, named by its index, moves at most one
locus.  This is `Product.prod_left_local` and `prod_right_local` read at an
index rather than at a membership. -/
theorem prod_op_one_locus (F G : FiniteSetting) {k : Nat}
    (hk : k < (prodSetting F G).ops.length) (x : Nat) :
    fstOf G.n ((prodSetting F G).ops.getD k id x) = fstOf G.n x ∨
      sndOf G.n ((prodSetting F G).ops.getD k id x) = sndOf G.n x := by
  have hmem : (prodSetting F G).ops.getD k id ∈
      F.ops.map (leftOp G.n) ++ G.ops.map (rightOp G.n) := getD_mem hk
  rcases List.mem_append.mp hmem with hleft | hright
  · exact Or.inr (prod_left_local F G hleft x)
  · exact Or.inl (prod_right_local G hright x)

/-- **The step of a two-locus program moves one locus.**  Stated of the
program's next value, so it holds wherever the machine moves at all. -/
theorem nextOf_one_locus (F G : FiniteSetting) (sched : Nat → Nat) {x y : Nat}
    (h : nextOf (program (twoLocus F G sched)) (prodSetting F G).ops.length x = some y) :
    fstOf G.n y = fstOf G.n x ∨ sndOf G.n y = sndOf G.n x := by
  obtain ⟨k, he, hl⟩ := nextOf_some h
  have hk : k < (prodSetting F G).ops.length := by
    have hkmem : k ∈ enabledAt (program (twoLocus F G sched))
        (prodSetting F G).ops.length x := by
      rw [he]
      exact List.Mem.head []
    exact (mem_enabledAt.mp hkmem).1
  have hk2 : k < (twoLocus F G sched).F.ops.length := hk
  have hmem : ((3 + k : Nat), [x, y]) ∈ program (twoLocus F G sched) := lookup_mem hl
  rcases mem_program.mp hmem with ⟨k', hk', x', -, heq⟩ | ⟨k', -, x', -, -, heq⟩
  · injection heq with h1 h2
    have hkk : k' = k := by omega
    subst hkk
    obtain ⟨hx, hy⟩ := list_two_inj h2
    subst hx
    subst hy
    exact prod_op_one_locus F G hk' x
  · injection heq with h1 _
    omega

/-- A tape moves one locus at a time when each consecutive pair leaves one of
the two coordinates exactly where it was. -/
def OneLocus (m : Nat) (l : List Nat) : Prop :=
  ∀ p ∈ pairsOf l, fstOf m p.2 = fstOf m p.1 ∨ sndOf m p.2 = sndOf m p.1

/-- A chain of a two-locus program moves one locus at a time. -/
theorem chain_one_locus (F G : FiniteSetting) (sched : Nat → Nat) {l : List Nat}
    (h : Chain (program (twoLocus F G sched)) (prodSetting F G).ops.length l) :
    OneLocus G.n l := fun p hp => nextOf_one_locus F G sched (h p hp)


/-- **The square, lifted to the observation.**  At every scale, from every
start, with any fuel, the observed tape of a two-locus run moves one locus at
a time: the record never shows the two loci moving together.  This is what
the family's causal-footprint entry recorded as not delivered. -/
theorem obs_one_locus (F G : FiniteSetting) (sched : Nat → Nat) (x fuel n : Nat) :
    OneLocus G.n (obs n (Control.init (twoLocus F G sched) x fuel)) := by
  have hstart := init_chain (twoLocus F G sched) x fuel
  have hchain := (iter_chain n (Control.init (twoLocus F G sched) x fuel) hstart.1 hstart.2).1
  obtain ⟨hg, hn⟩ := iter_graph n (Control.init (twoLocus F G sched) x fuel)
  rw [hg, hn] at hchain
  exact chain_one_locus F G sched hchain

/-- And the run the producer family records is one: its observation at scale
four is the tape the theorem there names, and it moves one locus at a time. -/
theorem pair_obs : obs 4 (Control.init Schedule.pair 0 4) = [0, 2, 3, 1, 0] := by decide

end Observe

#print axioms Observe.chain_one_locus
#print axioms Observe.nextOf_one_locus
#print axioms Observe.obs_one_locus
#print axioms Observe.pair_obs
#print axioms Observe.prod_op_one_locus
