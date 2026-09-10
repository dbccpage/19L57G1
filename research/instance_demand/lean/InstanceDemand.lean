import Derivation.Inertia

/-!
Stage 1: instance provenance and the original I1 witness.
An admission event's occurrence does not determine who generated that event.
No theorem here rules out a represented program generating admission events.
AuthorityEffect: None.
-/

namespace InstanceDemand
open Derivation

theorem step_insts_mem {r s : Regime} {e : Event} {i : Inst}
    (h : stepE r e = some s) :
    i ∈ s.insts ↔ i ∈ r.insts ∨ e = Event.admitInst i.1 i.2 := by
  rcases i with ⟨g, xs⟩
  cases e with
  | supply t => cases h; simp
  | admitDatum => cases h; simp
  | admitForm a =>
      change (if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none) = some s at h
      split at h
      · cases h; simp
      · cases h
  | admitInst f args =>
      change (if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data) then
        some { r with insts := insertNew r.insts (f, args) } else none) = some s at h
      split at h
      · cases h
        simp only [mem_insertNew, Prod.mk.injEq, Event.admitInst.injEq]
        simp only [eq_comm]
      · cases h
  | admitRuleAll f =>
      change (if f < r.forms.length then some { r with rules := insertNew r.rules f }
        else none) = some s at h
      split at h
      · cases h; simp
      · cases h
  | impose x y =>
      change (if x < y ∧ y < r.data then some { r with reqs := insertNew r.reqs (x,y) }
        else none) = some s at h
      split at h
      · cases h; simp
      · cases h

theorem replay_nil (r : Regime) : replayE [] r = some r := rfl

theorem replay_cons (e : Event) (h : List Event) (r : Regime) :
    replayE (e :: h) r = (stepE r e).bind (replayE h) := rfl

/-- Endpoint instance membership records event occurrence, not event authorship. -/
theorem replay_insts_mem {h : List Event} {r s : Regime} {i : Inst}
    (hr : replayE h r = some s) :
    i ∈ s.insts ↔ i ∈ r.insts ∨ Event.admitInst i.1 i.2 ∈ h := by
  induction h generalizing r s with
  | nil => rw [replay_nil] at hr; cases hr; simp
  | cons e tail ih =>
      rw [replay_cons] at hr
      cases hs : stepE r e with
      | none => rw [hs] at hr; cases hr
      | some r1 =>
          rw [hs] at hr
          rw [ih hr, step_insts_mem hs]
          simp only [List.mem_cons, or_assoc, eq_comm]

theorem genesis_instance_origin {h : List Event} {r : Regime} {i : Inst}
    (hr : replayE h genesis = some r) :
    i ∈ r.insts ↔ Event.admitInst i.1 i.2 ∈ h := by
  simpa only [genesis, List.not_mem_nil, false_or] using replay_insts_mem (i := i) hr

/-- Covers every faithful reader, including readers that do not select. -/
theorem faithful_read_origin (read : List Inst → Inst → Prop)
    (faithful : ∀ xs i, read xs i → i ∈ xs)
    {h : List Event} {r : Regime} {i : Inst}
    (hr : replayE h genesis = some r) (hi : read r.insts i) :
    Event.admitInst i.1 i.2 ∈ h :=
  (genesis_instance_origin hr).mp (faithful r.insts i hi)

theorem new_stored_instance_needs_event {r s : Regime} {e : Event} {i : Inst}
    (h : stepE r e = some s) (hi : i ∈ s.insts) (hn : i ∉ r.insts) :
    e = Event.admitInst i.1 i.2 := by
  exact ((step_insts_mem h).mp hi).resolve_left hn

theorem uniform_rule_keeps_instances {r s : Regime} {f : Nat}
    (h : stepE r (.admitRuleAll f) = some s) : s.insts = r.insts := by
  change (if f < r.forms.length then some { r with rules := insertNew r.rules f }
    else none) = some s at h
  split at h
  · cases h; rfl
  · cases h

/-- The native derivability rule has no premise test and covers its entire form. -/
theorem new_derivable_is_uniform {r : Regime} {i : Inst}
    (hi : derivable r i) (hn : i ∉ r.insts) :
    ∀ j : Inst, j.1 = i.1 → derivable r j := by
  have hf : i.1 ∈ r.rules := hi.resolve_left hn
  intro j hj
  exact Or.inr (hj ▸ hf)

def lone (n x y : Nat) : Regime := ⟨n, [2], [(0,[x,y])], [], []⟩
def covered (n x y : Nat) : Regime := ⟨n, [2], [(0,[x,y])], [0], []⟩

/-- The original I1 encoding itself makes its two distinct endpoints separable. -/
theorem lone_pair_separates (n x y : Nat) (hne : x ≠ y) (hy : y < n) :
    separable (lone n x y) x y := by
  refine ⟨⟨0, [none, some y]⟩, ?_, ?_⟩
  · simp [wfCtx, lone, slotOk, hy]
  · intro both
    have yes : derivable (lone n x y) (plug ⟨0,[none,some y]⟩ x) := by
      simp [derivable, lone, plug]
    have no : ¬ derivable (lone n x y) (plug ⟨0,[none,some y]⟩ y) := by
      simp [derivable, lone, plug, Ne.symm hne]
    exact no (both.mp yes)

/-- A rule-covered control prevents overgeneralizing the I1 failure. -/
theorem covered_pair_collapsed (n x y a b : Nat) : collapsed (covered n x y) a b := by
  intro c hc
  have hf : c.form = 0 := by
    have bound := hc.1
    change c.form < 1 at bound
    omega
  constructor <;> intro _ <;> apply Or.inr <;>
    change c.form ∈ [0] <;> simp [hf]

def historyL : List Event :=
  [.admitDatum, .admitDatum, .admitForm 2, .admitInst 0 [0,1]]
def historyF : List Event :=
  [.admitDatum, .admitDatum, .admitDatum, .admitForm 2, .admitInst 0 [1,2]]

theorem both_readings_replay :
    replayE historyL genesis = some (lone 2 0 1) ∧
    replayE historyF genesis = some (lone 3 1 2) := by decide

theorem both_readings_covered_replay :
    replayE (historyL ++ [.admitRuleAll 0]) genesis = some (covered 2 0 1) ∧
    replayE (historyF ++ [.admitRuleAll 0]) genesis = some (covered 3 1 2) := by decide

theorem samples_well_formed :
    (lone 2 0 1).wf ∧ (lone 3 1 2).wf ∧
    (covered 2 0 1).wf ∧ (covered 3 1 2).wf := by
  simp [Regime.wf, lone, covered]

end InstanceDemand

#print axioms InstanceDemand.step_insts_mem
#print axioms InstanceDemand.replay_nil
#print axioms InstanceDemand.replay_cons
#print axioms InstanceDemand.replay_insts_mem
#print axioms InstanceDemand.genesis_instance_origin
#print axioms InstanceDemand.faithful_read_origin
#print axioms InstanceDemand.new_stored_instance_needs_event
#print axioms InstanceDemand.uniform_rule_keeps_instances
#print axioms InstanceDemand.new_derivable_is_uniform
#print axioms InstanceDemand.lone_pair_separates
#print axioms InstanceDemand.covered_pair_collapsed
#print axioms InstanceDemand.both_readings_replay
#print axioms InstanceDemand.both_readings_covered_replay
#print axioms InstanceDemand.samples_well_formed
