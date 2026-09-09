import Cycle

/-!
# Observe.Fork: a fork observed as a family

The deterministic runner stops at a fork: `stepDet` returns `branch` and `next`
keeps the state, so the tape freezes.  The relational half of the lifting needs
no selection — observe the whole *family* of successors at each scale.

What is **not** proved, and is the point: a *thread* out of the family.  A
thread needs one tape per scale, and choosing one at a fork is exactly the
selection the runner refuses to make.

AuthorityEffect: None.
-/

namespace Observe

open Derivation Translation Execution Control Product Schedule Runner

/-! ## 6. A fork observed as a family

The deterministic runner stops at a fork: `stepDet` returns `branch` and
`next` keeps the state, so the tape freezes.  Every ledger here has recorded
that as the reason a fork's successor relation is not lifted to threads.  The
relational half is available without selecting anything: observe the whole
*family* of successors at each scale instead of one of them.

`branchStep` takes a state to its successors, or to itself where there are
none, so it is never empty; `frontier n` iterates it and `obsSet n` reads the
tapes off.  What is proved is the relational form of compatibility: every tape
at a scale is a prefix of some tape at the next (`obsSet_prefix`), and hence
of some tape at every later scale (`obsSet_prefix_add`).

What is **not** proved, and is the point: a *thread* out of the family.  A
thread needs one tape per scale, and choosing one at a fork is exactly the
selection the runner refuses to make.  The family is the honest object; the
lifting condition is that some choice function be declared, and none is. -/

/-- The successors of a state, or the state itself where there are none.
Never empty, so the frontier never dies at a terminal. -/
def branchStep (s : State) : List State :=
  match successors s with
  | [] => [s]
  | t :: rest => t :: rest

theorem branchStep_ne_nil (s : State) : branchStep s ≠ [] := by
  show (match successors s with | [] => [s] | t :: rest => t :: rest) ≠ []
  cases successors s with
  | nil => exact List.cons_ne_nil s []
  | cons t rest => exact List.cons_ne_nil t rest

/-- Whatever a branch step does, it only appends to the tape. -/
theorem branchStep_tape {s t : State} (h : t ∈ branchStep s) : s.tape <+: t.tape := by
  revert h
  show t ∈ (match successors s with | [] => [s] | u :: rest => u :: rest) → _
  cases hs : successors s with
  | nil =>
      intro h
      rw [List.mem_singleton.mp h]
      exact List.prefix_refl _
  | cons u rest =>
      intro h
      have hmem : t ∈ successors s := by
        rw [hs]
        exact h
      obtain ⟨k, -, hf⟩ := mem_successors.mp hmem
      obtain ⟨-, htape, -, -, -, -⟩ := fire_ok hf
      rw [htape]
      exact ⟨[t.active], rfl⟩

/-- The frontier at a scale: every state the process can be in after that
many steps, with no selection made. -/
def frontier : Nat → State → List State
  | 0, s => [s]
  | n + 1, s => (frontier n s).flatMap branchStep

/-- The family of observations at a scale. -/
def obsSet (n : Nat) (s : State) : List (List Nat) := (frontier n s).map (·.tape)

theorem frontier_ne_nil : ∀ (n : Nat) (s : State), frontier n s ≠ []
  | 0, s => List.cons_ne_nil s []
  | n + 1, s => by
      show (frontier n s).flatMap branchStep ≠ []
      cases hf : frontier n s with
      | nil => exact absurd hf (frontier_ne_nil n s)
      | cons t rest =>
          intro h
          have hmem : ∀ u ∈ branchStep t, u ∈ ((t :: rest).flatMap branchStep) := by
            intro u hu
            exact List.mem_flatMap.mpr ⟨t, List.Mem.head rest, hu⟩
          cases hb : branchStep t with
          | nil => exact branchStep_ne_nil t hb
          | cons u urest =>
              have : u ∈ ((t :: rest).flatMap branchStep) := hmem u (by rw [hb]; exact List.Mem.head urest)
              rw [h] at this
              exact absurd this List.not_mem_nil

/-- **Compatibility, relationally.**  Every tape observed at a scale is a
prefix of some tape observed at the next.  No branch is selected: the witness
is *some* member of the next family, not a designated one. -/
theorem obsSet_prefix (n : Nat) (s : State) :
    ∀ w ∈ obsSet n s, ∃ v ∈ obsSet (n + 1) s, w <+: v := by
  intro w hw
  obtain ⟨t, ht, rfl⟩ := List.mem_map.mp hw
  cases hb : branchStep t with
  | nil => exact absurd hb (branchStep_ne_nil t)
  | cons u urest =>
      have hu : u ∈ branchStep t := by
        rw [hb]
        exact List.Mem.head urest
      refine ⟨u.tape, List.mem_map.mpr ⟨u, ?_, rfl⟩, branchStep_tape hu⟩
      show u ∈ (frontier n s).flatMap branchStep
      exact List.mem_flatMap.mpr ⟨t, ht, hu⟩

/-- And hence of some tape at every later scale. -/
theorem obsSet_prefix_add (m : Nat) (s : State) :
    ∀ k, ∀ w ∈ obsSet m s, ∃ v ∈ obsSet (m + k) s, w <+: v
  | 0, w, hw => ⟨w, hw, List.prefix_refl w⟩
  | k + 1, w, hw => by
      obtain ⟨v, hv, hwv⟩ := obsSet_prefix_add m s k w hw
      obtain ⟨z, hz, hvz⟩ := obsSet_prefix (m + k) s v hv
      exact ⟨z, hz, hwv.trans hvz⟩

/-- **A fork has two observations where the runner has none.**  On the
represented family's forking program the family at scale one carries two
distinct tapes, while the deterministic runner's own observation has frozen at
the start.  That gap is the reason the successor relation is not lifted to a
thread here: a thread would need one of the two chosen. -/
def forking : Controlled := ⟨base, fun x k => decide (x = 0 ∧ (k = 0 ∨ k = 1))⟩

theorem fork_family_is_two :
    obsSet 1 (Control.init forking 0 5) = [[0, 1], [0, 0]] := by decide

theorem fork_runner_is_frozen :
    obs 1 (Control.init forking 0 5) = [0] := by decide

/-- The runner's observation is a member of the family only when the family is
a singleton; at the fork it is not even that, because the runner stayed. -/
theorem fork_runner_not_in_the_family :
    obs 1 (Control.init forking 0 5) ∉ obsSet 1 (Control.init forking 0 5) := by decide

end Observe

#print axioms Observe.branchStep_ne_nil
#print axioms Observe.branchStep_tape
#print axioms Observe.fork_family_is_two
#print axioms Observe.fork_runner_is_frozen
#print axioms Observe.fork_runner_not_in_the_family
#print axioms Observe.frontier_ne_nil
#print axioms Observe.obsSet_prefix
#print axioms Observe.obsSet_prefix_add
