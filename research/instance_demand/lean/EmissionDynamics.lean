import RepresentedEmitter

/-!
Stage 4: iterate the explicitly declared emission/admission procedure.
Fixed data and forms give a finite bound. This does not establish E1.
AuthorityEffect: None.
-/

namespace InstanceDemand.Dynamics
open Derivation
open InstanceDemand.Closure
open InstanceDemand.Emitter

/-- A coarse finite carrier: every binary tuple, including nonbinary forms. -/
def slots (r : Regime) : List Inst :=
  (List.range r.forms.length).flatMap fun f =>
    (tuples r.data 2).map (fun xs => (f,xs))

def missing (xs stored : List Inst) : Nat :=
  (xs.filter fun i => decide (i ∉ stored)).length

def budget (r : Regime) : Nat := missing (slots r) r.insts

theorem slots_mem (r : Regime) (i : Inst) :
    i ∈ slots r ↔ i.1 < r.forms.length ∧ i.2.length = 2 ∧ ∀ x ∈ i.2, x < r.data := by
  rcases i with ⟨f,xs⟩
  simp [slots, tuples_mem]

theorem flatMap_length {α β : Type} (xs : List α) (f : α → List β) (n : Nat)
    (h : ∀ x ∈ xs, (f x).length = n) : (xs.flatMap f).length = xs.length * n := by
  induction xs with
  | nil => simp only [List.flatMap_nil, List.length_nil, Nat.zero_mul]
  | cons x xs ih =>
      have hx := h x List.mem_cons_self
      have ht := ih (fun y hy => h y (List.mem_cons_of_mem x hy))
      simp only [List.flatMap_cons, List.length_append, List.length_cons, hx, ht]
      simp only [Nat.add_mul, Nat.one_mul, Nat.add_comm]

theorem tuples_length (n a : Nat) : (tuples n a).length = n ^ a := by
  induction a with
  | zero => rfl
  | succ a ih =>
      change ((List.range n).flatMap fun x => (tuples n a).map (x :: ·)).length = _
      rw [flatMap_length _ _ (n ^ a) (fun _ _ => by rw [List.length_map, ih])]
      simp only [List.length_range, Nat.pow_succ, Nat.mul_comm]

theorem slots_length (r : Regime) : (slots r).length = r.forms.length * r.data ^ 2 := by
  unfold slots
  rw [flatMap_length _ _ (r.data ^ 2) (fun _ _ => by rw [List.length_map, tuples_length])]
  rw [List.length_range]

theorem missing_le (xs a b : List Inst) (h : ∀ i ∈ a, i ∈ b) :
    missing xs b ≤ missing xs a := by
  induction xs with
  | nil => exact Nat.le_refl 0
  | cons i xs ih =>
      by_cases ha : i ∈ a
      · have hb := h i ha
        simpa [missing, ha, hb] using ih
      · by_cases hb : i ∈ b
        · simp only [missing, List.filter_cons, ha, hb, not_false_eq_true,
            not_true_eq_false, decide_true, decide_false, Bool.false_eq_true,
            ↓reduceIte, List.length_cons]
          exact Nat.le_trans ih (Nat.le_succ _)
        · simpa [missing, ha, hb] using Nat.succ_le_succ ih

theorem missing_strict (xs a b : List Inst) (h : ∀ i ∈ a, i ∈ b)
    (fresh : ∃ i, i ∈ xs ∧ i ∉ a ∧ i ∈ b) : missing xs b < missing xs a := by
  induction xs with
  | nil => rcases fresh with ⟨i,hi,_⟩; cases hi
  | cons i xs ih =>
      by_cases ha : i ∈ a
      · have hb := h i ha
        have ft : ∃ j, j ∈ xs ∧ j ∉ a ∧ j ∈ b := by
          rcases fresh with ⟨j,hj,hn,hb'⟩
          rcases List.mem_cons.mp hj with he | ht
          · subst j; exact False.elim (hn ha)
          · exact ⟨j,ht,hn,hb'⟩
        simpa [missing, ha, hb] using ih ft
      · by_cases hb : i ∈ b
        · have hm := missing_le xs a b h
          simpa [missing, ha, hb] using Nat.lt_succ_of_le hm
        · have ft : ∃ j, j ∈ xs ∧ j ∉ a ∧ j ∈ b := by
            rcases fresh with ⟨j,hj,hn,hb'⟩
            rcases List.mem_cons.mp hj with he | ht
            · subst j; exact False.elim (hb hb')
            · exact ⟨j,ht,hn,hb'⟩
          simpa [missing, ha, hb] using Nat.succ_lt_succ (ih ft)

theorem budget_bound (r : Regime) : budget r ≤ r.forms.length * r.data ^ 2 := by
  exact Nat.le_trans (List.length_filter_le _ _) (Nat.le_of_eq (slots_length r))

theorem emission_extends (r : Regime) (i : Inst) (h : i ∈ r.insts) :
    i ∈ (emit r).insts := (emitted_membership r i).mpr (Or.inl h)

theorem pending_in_slots (r : Regime) (i : Inst) (h : i ∈ Emitter.pending r) :
    i ∈ slots r := by
  rcases (Emitter.pending_mem r i).mp h with ⟨he,hw,_⟩
  rcases he with ⟨k,l,o,x,z,y,_,_,_,_,rfl⟩
  exact (slots_mem r _).mpr ⟨hw.1,rfl,hw.2.2⟩

theorem budget_decreases (r : Regime) (h : Emitter.pending r ≠ []) :
    budget (emit r) < budget r := by
  cases hp : Emitter.pending r with
  | nil => exact False.elim (h hp)
  | cons i xs =>
      have hi : i ∈ Emitter.pending r := by rw [hp]; exact List.mem_cons_self
      have hm := (Emitter.pending_mem r i).mp hi
      exact missing_strict (slots r) r.insts (emit r).insts (emission_extends r)
        ⟨i,pending_in_slots r i hi,hm.2.2,(emitted_membership r i).mpr (Or.inr ⟨hm.1,hm.2.1⟩)⟩

theorem emit_of_empty (r : Regime) (h : Emitter.pending r = []) : emit r = r := by
  unfold emit
  rw [h]
  rfl

theorem empty_iff_fixed (r : Regime) : Emitter.pending r = [] ↔ emit r = r := by
  constructor
  · exact emit_of_empty r
  · intro he
    by_cases hp : Emitter.pending r = []
    · exact hp
    · have hb := budget_decreases r hp
      rw [he] at hb
      exact False.elim (Nat.lt_irrefl _ hb)

def rounds (r : Regime) (n : Nat) : Regime :=
  Nat.rec r (fun _ current => emit current) n

theorem rounds_succ_start (r : Regime) (n : Nat) :
    rounds r (n+1) = rounds (emit r) n := by
  induction n with
  | zero => rfl
  | succ n ih => change emit (rounds r (n+1)) = emit (rounds (emit r) n); rw [ih]

theorem rounds_add (r : Regime) (m n : Nat) :
    rounds r (m+n) = rounds (rounds r m) n := by
  induction n with
  | zero => rfl
  | succ n ih => change emit (rounds r (m+n)) = emit (rounds (rounds r m) n); rw [ih]

theorem rounds_of_fixed (r : Regime) (h : Emitter.pending r = []) (n : Nat) :
    rounds r n = r := by
  induction n with
  | zero => rfl
  | succ n ih => change emit (rounds r n) = r; rw [ih, emit_of_empty r h]

theorem reaches_fixed (n : Nat) : ∀ r : Regime, budget r ≤ n →
    ∃ k, k ≤ n ∧ Emitter.pending (rounds r k) = [] := by
  induction n with
  | zero =>
      intro r hb
      refine ⟨0,Nat.le_refl _,?_⟩
      by_cases hp : Emitter.pending r = []
      · exact hp
      · have hd := budget_decreases r hp; omega
  | succ n ih =>
      intro r hb
      by_cases hp : Emitter.pending r = []
      · exact ⟨0,Nat.zero_le _,hp⟩
      · have hd := budget_decreases r hp
        rcases ih (emit r) (by omega) with ⟨k,hk,hf⟩
        exact ⟨k+1,Nat.succ_le_succ hk,by rw [rounds_succ_start]; exact hf⟩

theorem stable_by_budget (r : Regime) : Emitter.pending (rounds r (budget r)) = [] := by
  rcases reaches_fixed (budget r) r (Nat.le_refl _) with ⟨k,hk,hf⟩
  have hn : budget r = k + (budget r - k) := by omega
  rw [hn, rounds_add, rounds_of_fixed _ hf]
  exact hf

theorem stable_after_budget (r : Regime) (n : Nat) (h : budget r ≤ n) :
    rounds r n = rounds r (budget r) := by
  have hn : n = budget r + (n - budget r) := by omega
  rw [hn, rounds_add, rounds_of_fixed _ (stable_by_budget r)]

theorem no_unbounded_strict_rounds (r : Regime) :
    ¬ (∀ n, rounds r (n+1) ≠ rounds r n) := by
  intro h
  exact h (budget r) (emit_of_empty _ (stable_by_budget r))

theorem pending_not_instruction (r : Regime) (i : Inst)
    (h : i ∈ Emitter.pending r) : codes i = [] := by
  rcases ((Emitter.pending_mem r i).mp h).1 with ⟨k,l,o,x,z,y,_,_,_,_,rfl⟩
  have hn : 3 + o ≠ 0 := by omega
  simp only [codes, hn, false_and, ↓reduceIte]

theorem instructions_addMany (base xs : List Inst)
    (h : ∀ i ∈ xs, codes i = []) : instructions (addMany base xs) = instructions base := by
  induction xs generalizing base with
  | nil => rfl
  | cons i xs ih =>
      have hi := h i List.mem_cons_self
      have ht := ih (insertNew base i) (fun j hj => h j (List.mem_cons_of_mem i hj))
      change instructions (addMany (insertNew base i) xs) = _
      rw [ht]
      by_cases hm : i ∈ base
      · rw [insertNew_of_mem hm]
      · rw [insertNew_of_not_mem hm]
        simp only [instructions, List.flatMap_append, List.flatMap_cons, hi,
          List.flatMap_nil, List.append_nil]

theorem emission_instructions (r : Regime) : instructions (emit r).insts = instructions r.insts :=
  instructions_addMany r.insts _ (pending_not_instruction r)

theorem rounds_fields (r : Regime) (n : Nat) :
    (rounds r n).data = r.data ∧ (rounds r n).forms = r.forms ∧
    (rounds r n).rules = r.rules ∧ (rounds r n).reqs = r.reqs := by
  induction n with
  | zero => exact ⟨rfl,rfl,rfl,rfl⟩
  | succ n ih => exact ih

theorem rounds_instructions (r : Regime) (n : Nat) :
    instructions (rounds r n).insts = instructions r.insts := by
  induction n with
  | zero => rfl
  | succ n ih => exact Eq.trans (emission_instructions _) ih

theorem rounds_wf (r : Regime) (h : r.wf) (n : Nat) : (rounds r n).wf := by
  induction n with
  | zero => exact h
  | succ n ih => exact emission_wf _ ih

def trace (r : Regime) (n : Nat) : List Event :=
  Nat.rec [] (fun k previous => previous ++ events (Emitter.pending (rounds r k))) n

theorem trace_replay (r : Regime) (n : Nat) : replayE (trace r n) r = some (rounds r n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change replayE (trace r n ++ events (Emitter.pending (rounds r n))) r = _
      rw [replay_append, ih, Option.bind_some, emission_replay]
      rfl

theorem trace_no_impose (r : Regime) (n x y : Nat) : .impose x y ∉ trace r n := by
  induction n with
  | zero => exact List.not_mem_nil
  | succ n ih =>
      intro h
      rcases List.mem_append.mp h with hp | hn
      · exact ih hp
      · exact events_no_impose _ x y hn

theorem whole_trace_replay (seed : List Event) (r : Regime)
    (h : replayE seed genesis = some r) (n : Nat) :
    replayE (seed ++ trace r n) genesis = some (rounds r n) := by
  rw [replay_append, h, Option.bind_some, trace_replay]

/-- Closed under this declared composition, not under a new native rule. -/
def Closed (r : Regime) : Prop := ∀ i, Enabled r.insts i → wfInst r i → i ∈ r.insts

theorem closed_iff_empty (r : Regime) : Closed r ↔ Emitter.pending r = [] := by
  constructor
  · intro hc
    cases hp : Emitter.pending r with
    | nil => rfl
    | cons i xs =>
        have hi : i ∈ Emitter.pending r := by rw [hp]; exact List.mem_cons_self
        have hm := (Emitter.pending_mem r i).mp hi
        exact False.elim (hm.2.2 (hc i hm.1 hm.2.1))
  · intro hp i he hw
    by_cases hi : i ∈ r.insts
    · exact hi
    · have hm := (Emitter.pending_mem r i).mpr ⟨he,hw,hi⟩
      rw [hp] at hm
      cases hm

theorem terminal_closed (r : Regime) : Closed (rounds r (budget r)) :=
  (closed_iff_empty _).mpr (stable_by_budget r)

theorem enabled_mono (a b : List Inst) (h : ∀ i ∈ a, i ∈ b)
    (i : Inst) (he : Enabled a i) : Enabled b i := by
  rcases he with ⟨k,l,o,x,z,y,hc,hp,hq,hxy,hi⟩
  exact ⟨k,l,o,x,z,y,h _ hc,h _ hp,h _ hq,hxy,hi⟩

theorem rounds_below_closed (r s : Regime) (hd : r.data = s.data)
    (hf : r.forms = s.forms) (hs : ∀ i ∈ r.insts, i ∈ s.insts) (hc : Closed s)
    (n : Nat) : ∀ i ∈ (rounds r n).insts, i ∈ s.insts := by
  induction n with
  | zero => exact hs
  | succ n ih =>
      intro i hi
      rcases (emitted_membership (rounds r n) i).mp hi with hm | ⟨he,hw⟩
      · exact ih i hm
      · apply hc i (enabled_mono _ _ ih i he)
        have hdn := Eq.trans (rounds_fields r n).1 hd
        have hfn := Eq.trans (rounds_fields r n).2.1 hf
        simpa only [wfInst, hdn, hfn] using hw

theorem terminal_extends (r : Regime) : ∀ i ∈ r.insts, i ∈ (rounds r (budget r)).insts := by
  have h : ∀ n i, i ∈ r.insts → i ∈ (rounds r n).insts := by
    intro n
    induction n with
    | zero => exact fun _ hi => hi
    | succ n ih => exact fun i hi => emission_extends _ i (ih i hi)
  exact h (budget r)

theorem terminal_least (r s : Regime) (hd : r.data = s.data)
    (hf : r.forms = s.forms) (hs : ∀ i ∈ r.insts, i ∈ s.insts) (hc : Closed s) :
    ∀ i ∈ (rounds r (budget r)).insts, i ∈ s.insts :=
  rounds_below_closed r s hd hf hs hc (budget r)

def chain (cover : Bool) : Regime :=
  ⟨4, [3,1,1,2], [(0,[0,0,0]),(3,[0,1]),(3,[1,2]),(3,[2,3])],
    if cover then [0,1,2,3] else [0,1,2], []⟩

def chainHistory (cover : Bool) : List Event :=
  List.replicate 4 Event.admitDatum ++ [3,1,1,2].map Event.admitForm ++
  events (chain cover).insts ++ (chain cover).rules.map Event.admitRuleAll

theorem chain_replay (cover : Bool) : replayE (chainHistory cover) genesis = some (chain cover) := by
  cases cover <;> decide

theorem chain_wf (cover : Bool) : (chain cover).wf := by
  cases cover <;> simp [Regime.wf, chain]

theorem chain_rounds (cover : Bool) :
    Emitter.pending (chain cover) = [(3,[0,2]),(3,[1,3])] ∧
    Emitter.pending (rounds (chain cover) 1) = [(3,[0,3]),(3,[0,3])] ∧
    Emitter.pending (rounds (chain cover) 2) = [] := by
  cases cover <;> decide

theorem chain_budget (cover : Bool) : budget (chain cover) = 61 := by
  cases cover <;> decide

theorem chain_not_one_pass (cover : Bool) : emit (emit (chain cover)) ≠ emit (chain cover) := by
  cases cover <;> decide

theorem chain_whole_replay (cover : Bool) :
    replayE (chainHistory cover ++ trace (chain cover) 2) genesis =
      some (rounds (chain cover) 2) := whole_trace_replay _ _ (chain_replay cover) 2

theorem chain_covered_collapsed (n x y : Nat) : collapsed (rounds (chain true) n) x y := by
  apply fully_covered_collapsed
  intro f hf
  rw [(rounds_fields (chain true) n).2.1] at hf
  rw [(rounds_fields (chain true) n).2.2.1]
  change f < 4 at hf
  change f ∈ [0,1,2,3]
  simp only [List.mem_cons, List.not_mem_nil, or_false]
  omega

def chainResponse : List Item := [.newForm 1, .newInst 4 [0]]
def chainResponseEvents : List Event := [.admitForm 1, .admitInst 4 [0]]
def chainAnswered : Regime :=
  { rounds (chain true) 2 with
    forms := [3,1,1,2,1]
    insts := insertNew (rounds (chain true) 2).insts (4,[0]) }

theorem chain_response_valid : validResponse (rounds (chain true) 2) 0 3 chainResponse := by
  refine ⟨chainAnswered,by decide,?_,?_⟩
  · refine ⟨⟨4,[none]⟩,by decide,?_⟩
    change ¬ (derivable chainAnswered (4,[0]) ↔ derivable chainAnswered (4,[3]))
    simp only [derivable]
    decide
  · change ∀ q ∈ ([] : List (Nat × Nat)), _
    intro q hq
    cases hq

theorem chain_response_replay :
    replayE (chainHistory true ++ trace (chain true) 2 ++ chainResponseEvents) genesis =
      some chainAnswered := by decide

theorem chain_answered_pair_retained : (3,[0,3]) ∈ chainAnswered.insts := by decide

theorem chain_functionality_boundary (cover : Bool) :
    Functional (chain cover).insts 3 ∧ ¬ Functional (rounds (chain cover) 1).insts 3 := by
  constructor
  · intro x y z hp hq
    simp [chain] at hp hq
    rcases hp with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ <;> simp_all
  · intro h
    have hp : (3,[0,1]) ∈ (rounds (chain cover) 1).insts := by cases cover <;> decide
    have hq : (3,[0,2]) ∈ (rounds (chain cover) 1).insts := by cases cover <;> decide
    have he := h 0 1 2 hp hq
    cases he

end InstanceDemand.Dynamics

#print axioms InstanceDemand.Dynamics.slots_mem
#print axioms InstanceDemand.Dynamics.flatMap_length
#print axioms InstanceDemand.Dynamics.tuples_length
#print axioms InstanceDemand.Dynamics.slots_length
#print axioms InstanceDemand.Dynamics.missing_le
#print axioms InstanceDemand.Dynamics.missing_strict
#print axioms InstanceDemand.Dynamics.budget_bound
#print axioms InstanceDemand.Dynamics.emission_extends
#print axioms InstanceDemand.Dynamics.pending_in_slots
#print axioms InstanceDemand.Dynamics.budget_decreases
#print axioms InstanceDemand.Dynamics.emit_of_empty
#print axioms InstanceDemand.Dynamics.empty_iff_fixed
#print axioms InstanceDemand.Dynamics.rounds_succ_start
#print axioms InstanceDemand.Dynamics.rounds_add
#print axioms InstanceDemand.Dynamics.rounds_of_fixed
#print axioms InstanceDemand.Dynamics.reaches_fixed
#print axioms InstanceDemand.Dynamics.stable_by_budget
#print axioms InstanceDemand.Dynamics.stable_after_budget
#print axioms InstanceDemand.Dynamics.no_unbounded_strict_rounds
#print axioms InstanceDemand.Dynamics.pending_not_instruction
#print axioms InstanceDemand.Dynamics.instructions_addMany
#print axioms InstanceDemand.Dynamics.emission_instructions
#print axioms InstanceDemand.Dynamics.rounds_fields
#print axioms InstanceDemand.Dynamics.rounds_instructions
#print axioms InstanceDemand.Dynamics.rounds_wf
#print axioms InstanceDemand.Dynamics.trace_replay
#print axioms InstanceDemand.Dynamics.trace_no_impose
#print axioms InstanceDemand.Dynamics.whole_trace_replay
#print axioms InstanceDemand.Dynamics.closed_iff_empty
#print axioms InstanceDemand.Dynamics.terminal_closed
#print axioms InstanceDemand.Dynamics.enabled_mono
#print axioms InstanceDemand.Dynamics.rounds_below_closed
#print axioms InstanceDemand.Dynamics.terminal_extends
#print axioms InstanceDemand.Dynamics.terminal_least
#print axioms InstanceDemand.Dynamics.chain_replay
#print axioms InstanceDemand.Dynamics.chain_wf
#print axioms InstanceDemand.Dynamics.chain_rounds
#print axioms InstanceDemand.Dynamics.chain_budget
#print axioms InstanceDemand.Dynamics.chain_not_one_pass
#print axioms InstanceDemand.Dynamics.chain_whole_replay
#print axioms InstanceDemand.Dynamics.chain_covered_collapsed
#print axioms InstanceDemand.Dynamics.chain_response_valid
#print axioms InstanceDemand.Dynamics.chain_response_replay
#print axioms InstanceDemand.Dynamics.chain_answered_pair_retained
#print axioms InstanceDemand.Dynamics.chain_functionality_boundary
