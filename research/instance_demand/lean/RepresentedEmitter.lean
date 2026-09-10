import ClosureMaterialization
import Execution

/-!
Stage 3: compose stored edges under a stored instruction.
The graph-reading bridge is proved. Applying the output admissions is a
declared host operation, not a new rule of the sealed grammar.
AuthorityEffect: None.
-/

namespace InstanceDemand.Emitter
open Derivation
open InstanceDemand.Closure

def codes (i : Inst) : List (Nat × Nat × Nat) :=
  if i.1 = 0 ∧ i.2.length = 3 then
    [(i.2.getD 0 0, i.2.getD 1 0, i.2.getD 2 0)] else []

def edge (f : Nat) (i : Inst) : List (Nat × Nat) :=
  if i.1 = f ∧ i.2.length = 2 then [(i.2.getD 0 0, i.2.getD 1 0)] else []

theorem length_two (xs : List Nat) (h : xs.length = 2) :
    xs = [xs.getD 0 0, xs.getD 1 0] := by
  cases xs with
  | nil => cases h
  | cons x xs =>
      cases xs with
      | nil => cases h
      | cons y tail =>
          have ht : tail.length = 0 := by change tail.length + 1 + 1 = 2 at h; omega
          have he := List.length_eq_zero_iff.mp ht
          subst tail
          rfl

theorem length_three (xs : List Nat) (h : xs.length = 3) :
    xs = [xs.getD 0 0, xs.getD 1 0, xs.getD 2 0] := by
  cases xs with
  | nil => cases h
  | cons x xs =>
      have ht : xs.length = 2 := by change xs.length + 1 = 3 at h; omega
      rw [length_two xs ht]
      rfl

theorem codes_mem (i : Inst) (k l o : Nat) :
    (k,l,o) ∈ codes i ↔ i = (0,[k,l,o]) := by
  unfold codes
  split
  · rename_i h
    constructor
    · intro hi
      have he := List.mem_singleton.mp hi
      have hk := congrArg Prod.fst he
      have hl := congrArg (fun p : Nat × Nat × Nat => p.2.1) he
      have ho := congrArg (fun p : Nat × Nat × Nat => p.2.2) he
      change k = i.2.getD 0 0 at hk
      change l = i.2.getD 1 0 at hl
      change o = i.2.getD 2 0 at ho
      have hs := length_three i.2 h.2
      rw [← hk, ← hl, ← ho] at hs
      exact Prod.ext h.1 hs
    · intro hi; subst i; exact List.mem_singleton.mpr rfl
  · rename_i h
    constructor
    · intro hi; cases hi
    · intro hi; subst i; exact False.elim (h ⟨rfl,rfl⟩)

theorem edge_mem (f : Nat) (i : Inst) (x y : Nat) :
    (x,y) ∈ edge f i ↔ i = (f,[x,y]) := by
  unfold edge
  split
  · rename_i h
    constructor
    · intro hi
      have he := List.mem_singleton.mp hi
      have hx := congrArg Prod.fst he
      have hy := congrArg Prod.snd he
      change x = i.2.getD 0 0 at hx
      change y = i.2.getD 1 0 at hy
      have hs := length_two i.2 h.2
      rw [← hx, ← hy] at hs
      exact Prod.ext h.1 hs
    · intro hi; subst i; exact List.mem_singleton.mpr rfl
  · rename_i h
    constructor
    · intro hi; cases hi
    · intro hi; subst i; exact False.elim (h ⟨rfl,rfl⟩)

def instructions (s : List Inst) := s.flatMap codes
def edges (s : List Inst) (f : Nat) := s.flatMap (edge f)

theorem instructions_mem (s : List Inst) (k l o : Nat) :
    (k,l,o) ∈ instructions s ↔ (0,[k,l,o]) ∈ s := by
  simp only [instructions, List.mem_flatMap, codes_mem]
  constructor
  · rintro ⟨i, hi, rfl⟩; exact hi
  · intro h; exact ⟨_,h,rfl⟩

theorem edges_mem (s : List Inst) (f x y : Nat) :
    (x,y) ∈ edges s f ↔ (f,[x,y]) ∈ s := by
  simp only [edges, List.mem_flatMap, edge_mem]
  constructor
  · rintro ⟨i, hi, rfl⟩; exact hi
  · intro h; exact ⟨_,h,rfl⟩

/-- Every matching path is retained, including repeated output witnesses. -/
def raw (s : List Inst) : List Inst :=
  (instructions s).flatMap fun c =>
    (edges s (3 + c.1)).flatMap fun p =>
      (edges s (3 + c.2.1)).flatMap fun q =>
        if p.2 = q.1 ∧ p.1 < q.2 then [(3 + c.2.2, [p.1,q.2])] else []

def Enabled (s : List Inst) (i : Inst) : Prop :=
  ∃ k l o x z y, (0,[k,l,o]) ∈ s ∧ (3+k,[x,z]) ∈ s ∧
    (3+l,[z,y]) ∈ s ∧ x < y ∧ i = (3+o,[x,y])

theorem raw_mem (s : List Inst) (i : Inst) : i ∈ raw s ↔ Enabled s i := by
  unfold raw
  constructor
  · intro hi
    rcases List.mem_flatMap.mp hi with ⟨⟨k,l,o⟩, hc, hi⟩
    rcases List.mem_flatMap.mp hi with ⟨⟨x,z⟩, hp, hi⟩
    rcases List.mem_flatMap.mp hi with ⟨⟨z',y⟩, hq, hi⟩
    split at hi
    · rename_i h
      have hz : z = z' := h.1
      subst z'
      exact ⟨k,l,o,x,z,y, (instructions_mem s k l o).mp hc,
        (edges_mem s _ _ _).mp hp, (edges_mem s _ _ _).mp hq,
        h.2, List.mem_singleton.mp hi⟩
    · cases hi
  · rintro ⟨k,l,o,x,z,y,hc,hp,hq,hxy,rfl⟩
    apply List.mem_flatMap.mpr
    refine ⟨(k,l,o), (instructions_mem s k l o).mpr hc, ?_⟩
    apply List.mem_flatMap.mpr
    refine ⟨(x,z), (edges_mem s _ _ _).mpr hp, ?_⟩
    apply List.mem_flatMap.mpr
    refine ⟨(z,y), (edges_mem s _ _ _).mpr hq, ?_⟩
    simp only [hxy, and_self, ↓reduceIte, List.mem_singleton]

def Functional (s : List Inst) (f : Nat) :=
  ∀ x y z, (f,[x,y]) ∈ s → (f,[x,z]) ∈ s → y = z

theorem lookup_of_functional (s : List Inst) (f x y : Nat)
    (hf : Functional s f) (he : (f,[x,y]) ∈ s) : Execution.lookup f x s = some y := by
  have hs := Execution.lookup_isSome he
  cases hl : Execution.lookup f x s with
  | none => rw [hl] at hs; cases hs
  | some z =>
      have hz := hf x z y (Execution.lookup_mem hl) he
      subst z
      rfl

theorem two_edge_bridge (s : List Inst) (k l x z y : Nat)
    (hk : Functional s (3+k)) (hl : Functional s (3+l))
    (hp : (3+k,[x,z]) ∈ s) (hq : (3+l,[z,y]) ∈ s) :
    (Execution.run ⟨s,[k,l],x,[]⟩).map Execution.Config.active = some y := by
  rw [Execution.run_evalWord]
  change (match Execution.lookup (3+k) x s with
    | none => none
    | some a => Execution.evalWord s [l] a) = some y
  rw [lookup_of_functional s _ _ _ hk hp]
  change (match Execution.lookup (3+l) z s with
    | none => none
    | some b => some b) = some y
  rw [lookup_of_functional s _ _ _ hl hq]

theorem emitted_has_represented_path (s : List Inst) (i : Inst)
    (hf : ∀ k, Functional s (3+k)) (hi : i ∈ raw s) :
    ∃ k l o x y, (0,[k,l,o]) ∈ s ∧ i = (3+o,[x,y]) ∧
      (Execution.run ⟨s,[k,l],x,[]⟩).map Execution.Config.active = some y := by
  rcases (raw_mem s i).mp hi with ⟨k,l,o,x,z,y,hc,hp,hq,_,he⟩
  exact ⟨k,l,o,x,y,hc,he,two_edge_bridge s k l x z y (hf k) (hf l) hp hq⟩

theorem execution_output_retained (s : List Inst) (k l o x y : Nat)
    (hc : (0,[k,l,o]) ∈ s) (hxy : x < y)
    (hr : (Execution.run ⟨s,[k,l],x,[]⟩).map Execution.Config.active = some y) :
    (3+o,[x,y]) ∈ raw s := by
  rw [Execution.run_evalWord] at hr
  change (match Execution.lookup (3+k) x s with
    | none => none
    | some z => Execution.evalWord s [l] z) = some y at hr
  cases hp : Execution.lookup (3+k) x s with
  | none => rw [hp] at hr; cases hr
  | some z =>
      rw [hp] at hr
      change (match Execution.lookup (3+l) z s with
        | none => none
        | some v => some v) = some y at hr
      cases hq : Execution.lookup (3+l) z s with
      | none => rw [hq] at hr; cases hr
      | some v =>
          rw [hq] at hr
          have he := Option.some.inj hr
          subst v
          exact (raw_mem s _).mpr ⟨k,l,o,x,z,y,hc,Execution.lookup_mem hp,
            Execution.lookup_mem hq,hxy,rfl⟩

theorem no_instruction_no_output (s : List Inst)
    (h : ∀ k l o, (0,[k,l,o]) ∉ s) : raw s = [] := by
  cases he : raw s with
  | nil => rfl
  | cons i rest =>
      have hi : i ∈ raw s := by rw [he]; exact List.mem_cons_self
      rcases (raw_mem s i).mp hi with ⟨k,l,o,_,_,_,hc,_⟩
      exact False.elim (h k l o hc)

theorem represented_run_keeps_graph (c d : Execution.Config)
    (h : Execution.run c = some d) : d.graph = c.graph := by
  exact Execution.iterate_graph c.graph c.word c.active c.output d h

instance wfInstDecidable (r : Regime) (i : Inst) : Decidable (wfInst r i) :=
  inferInstanceAs (Decidable (i.1 < r.forms.length ∧ i.2.length = r.forms.getD i.1 0 ∧
    ∀ x ∈ i.2, x < r.data))

def pending (r : Regime) := (raw r.insts).filter fun i => decide (wfInst r i ∧ i ∉ r.insts)
def emit (r : Regime) := storeMany r (pending r)

theorem pending_mem (r : Regime) (i : Inst) :
    i ∈ pending r ↔ Enabled r.insts i ∧ wfInst r i ∧ i ∉ r.insts := by
  simp only [pending, List.mem_filter, raw_mem, decide_eq_true_eq]

theorem emission_replay (r : Regime) :
    replayE (events (pending r)) r = some (emit r) :=
  storeMany_replay r _ fun i hi => ((pending_mem r i).mp hi).2.1

theorem emitted_membership (r : Regime) (i : Inst) :
    i ∈ (emit r).insts ↔ i ∈ r.insts ∨ (Enabled r.insts i ∧ wfInst r i) := by
  change i ∈ addMany r.insts (pending r) ↔ _
  rw [addMany_mem, pending_mem]
  by_cases h : i ∈ r.insts <;> simp [h]

theorem emission_fields (r : Regime) :
    (emit r).data = r.data ∧ (emit r).forms = r.forms ∧
    (emit r).rules = r.rules ∧ (emit r).reqs = r.reqs := ⟨rfl,rfl,rfl,rfl⟩

theorem emission_wf (r : Regime) (h : r.wf) : (emit r).wf := by
  refine ⟨?_,h.2⟩
  intro i hi
  rcases (emitted_membership r i).mp hi with hi | ⟨_,hi⟩
  · exact h.1 i hi
  · exact hi

def seed (n x z y : Nat) (cover : Bool) : Regime :=
  ⟨n, [3,1,1,2,2,2], [(0,[0,1,2]), (3,[x,z]), (4,[z,y])],
    if cover then [0,1,2,3,4,5] else [0,1,2,3,4], []⟩

theorem raw_seed (n x z y : Nat) (cover : Bool) (hxy : x < y) :
    raw (seed n x z y cover).insts = [(5,[x,y])] := by
  have hc : instructions (seed n x z y cover).insts = [(0,1,2)] := rfl
  have hp : edges (seed n x z y cover).insts 3 = [(x,z)] := rfl
  have hq : edges (seed n x z y cover).insts 4 = [(z,y)] := rfl
  unfold raw
  rw [hc]
  simp only [List.flatMap_cons, List.flatMap_nil, hp, hq, List.append_nil]
  exact if_pos ⟨True.intro,hxy⟩

theorem pending_seed (n x z y : Nat) (cover : Bool) (hxy : x < y) (hyn : y < n) :
    pending (seed n x z y cover) = [(5,[x,y])] := by
  have hxn := Nat.lt_trans hxy hyn
  unfold pending
  rw [raw_seed n x z y cover hxy]
  simp [wfInst, seed, hxn, hyn]

theorem emit_seed (n x z y : Nat) (cover : Bool) (hxy : x < y) (hyn : y < n) :
    emit (seed n x z y cover) =
      { seed n x z y cover with
        insts := [(0,[0,1,2]), (3,[x,z]), (4,[z,y]), (5,[x,y])] } := by
  unfold emit
  rw [pending_seed n x z y cover hxy hyn]
  simp [storeMany, addMany, seed, insertNew]

theorem fully_covered_collapsed (r : Regime)
    (h : ∀ f, f < r.forms.length → f ∈ r.rules) (x y : Nat) : collapsed r x y := by
  intro c hc
  exact ⟨fun _ => Or.inr (h c.form hc.1), fun _ => Or.inr (h c.form hc.1)⟩

theorem seed_collapsed (n x z y : Nat) (cover : Bool) (a b : Nat) :
    collapsed (seed n x z y cover) a b := by
  intro c hc
  have hf : c.form < 6 := hc.1
  cases cover with
  | false =>
      by_cases h5 : c.form = 5
      · simp [derivable, plug, seed, h5]
      · have hr : c.form ∈ (seed n x z y false).rules := by
          simp only [seed, Bool.false_eq_true, ↓reduceIte, List.mem_cons, List.not_mem_nil, or_false]
          omega
        exact ⟨fun _ => Or.inr hr, fun _ => Or.inr hr⟩
  | true =>
      have hr : c.form ∈ (seed n x z y true).rules := by
        simp only [seed, ↓reduceIte, List.mem_cons, List.not_mem_nil, or_false]
        omega
      exact ⟨fun _ => Or.inr hr, fun _ => Or.inr hr⟩

theorem unruled_output_not_derivable (n x z y : Nat) :
    ¬ derivable (seed n x z y false) (5,[x,y]) := by
  simp [derivable, seed]

theorem unruled_emission_separates (n x z y : Nat) (hxy : x < y) (hyn : y < n) :
    separable (emit (seed n x z y false)) x y := by
  rw [emit_seed n x z y false hxy hyn]
  refine ⟨⟨5,[none,some y]⟩, ?_, ?_⟩
  · simp [wfCtx, seed, slotOk, hyn]
  · have hne : y ≠ x := by omega
    simp [derivable, plug, seed, hne]

theorem covered_emission_collapsed (n x z y a b : Nat) :
    collapsed (emit (seed n x z y true)) a b := by
  apply fully_covered_collapsed
  intro f hf
  change f < 6 at hf
  change f ∈ [0,1,2,3,4,5]
  simp only [List.mem_cons, List.not_mem_nil, or_false]
  omega

def seedHistory (n x z y : Nat) (cover : Bool) : List Event :=
  List.replicate n .admitDatum ++
    [.admitForm 3, .admitForm 1, .admitForm 1, .admitForm 2, .admitForm 2, .admitForm 2,
     .admitInst 0 [0,1,2], .admitInst 3 [x,z], .admitInst 4 [z,y],
     .admitRuleAll 0, .admitRuleAll 1, .admitRuleAll 2, .admitRuleAll 3, .admitRuleAll 4] ++
    if cover then [.admitRuleAll 5] else []

theorem seeds_replay :
    replayE (seedHistory 3 0 2 1 false) genesis = some (seed 3 0 2 1 false) ∧
    replayE (seedHistory 3 0 2 1 true) genesis = some (seed 3 0 2 1 true) ∧
    replayE (seedHistory 4 1 3 2 false) genesis = some (seed 4 1 3 2 false) ∧
    replayE (seedHistory 4 1 3 2 true) genesis = some (seed 4 1 3 2 true) := by decide

theorem seeds_wf : (seed 3 0 2 1 false).wf ∧ (seed 3 0 2 1 true).wf ∧
    (seed 4 1 3 2 false).wf ∧ (seed 4 1 3 2 true).wf := by simp [Regime.wf, seed]

theorem seed_execution_bridge :
    (Execution.run ⟨(seed 3 0 2 1 true).insts,[0,1],0,[]⟩).map Execution.Config.active = some 1 ∧
    (Execution.run ⟨(seed 4 1 3 2 true).insts,[0,1],1,[]⟩).map Execution.Config.active = some 2 := by
  decide

theorem histories_no_impose (n x z y a b : Nat) (cover : Bool) :
    Event.impose a b ∉ seedHistory n x z y cover ++ events (pending (seed n x z y cover)) := by
  cases cover <;> simp [seedHistory, Closure.events_no_impose]

/-- Concrete refutation of identifying this host join with sealed derivability. -/
theorem native_closure_counterexample :
    Enabled (seed 3 0 2 1 false).insts (5,[0,1]) ∧
    ¬ derivable (seed 3 0 2 1 false) (5,[0,1]) := by
  refine ⟨(raw_mem _ _).mp ?_, unruled_output_not_derivable _ _ _ _⟩
  rw [raw_seed 3 0 2 1 false (by decide)]
  exact List.mem_singleton.mpr rfl

theorem no_native_join_rule :
    ¬ (∀ (r : Regime) (i : Inst), r.wf → Enabled r.insts i → derivable r i) := by
  intro h
  exact native_closure_counterexample.2
    (h _ _ seeds_wf.1 native_closure_counterexample.1)

def response (x : Nat) : List Item := [.newForm 1, .newInst 6 [x]]
def responseEvents (x : Nat) : List Event := [.admitForm 1, .admitInst 6 [x]]
def answered (n x z y : Nat) : Regime :=
  { emit (seed n x z y true) with
    forms := [3,1,1,2,2,2,1]
    insts := insertNew (emit (seed n x z y true)).insts (6,[x]) }

theorem response_applies (n x z y : Nat) (hxy : x < y) (hyn : y < n) :
    applyDelta (emit (seed n x z y true)) (response x) = some (answered n x z y) ∧
    replayE (responseEvents x) (emit (seed n x z y true)) = some (answered n x z y) := by
  have hxn := Nat.lt_trans hxy hyn
  unfold answered
  rw [emit_seed n x z y true hxy hyn]
  simp [applyDelta, applyItem, response, replayE, responseEvents, stepE, seed, hxn]

theorem answer_separates (n x z y : Nat) (hxy : x < y) (hyn : y < n) :
    separable (answered n x z y) x y := by
  refine ⟨⟨6,[none]⟩, ?_, ?_⟩
  · simp [wfCtx, answered, slotOk]
  · have hne : y ≠ x := by omega
    unfold answered
    rw [emit_seed n x z y true hxy hyn]
    simp [derivable, plug, mem_insertNew, seed, hne]

theorem covered_answerable (n x z y : Nat) (hxy : x < y) (hyn : y < n) :
    validResponse (emit (seed n x z y true)) x y (response x) := by
  refine ⟨answered n x z y, (response_applies n x z y hxy hyn).1,
    answer_separates n x z y hxy hyn, ?_⟩
  simp [emit, storeMany, seed]

theorem covered_histories_replay :
    replayE (seedHistory 3 0 2 1 true ++ events (pending (seed 3 0 2 1 true)) ++
      responseEvents 0) genesis = some (answered 3 0 2 1) ∧
    replayE (seedHistory 4 1 3 2 true ++ events (pending (seed 4 1 3 2 true)) ++
      responseEvents 1) genesis = some (answered 4 1 3 2) := by
  simp only [Closure.replay_append, seeds_replay.2.1, seeds_replay.2.2.2,
    Option.bind_some, emission_replay]
  exact ⟨(response_applies 3 0 2 1 (by decide) (by decide)).2,
    (response_applies 4 1 3 2 (by decide) (by decide)).2⟩

end InstanceDemand.Emitter

#print axioms InstanceDemand.Emitter.length_two
#print axioms InstanceDemand.Emitter.length_three
#print axioms InstanceDemand.Emitter.codes_mem
#print axioms InstanceDemand.Emitter.edge_mem
#print axioms InstanceDemand.Emitter.instructions_mem
#print axioms InstanceDemand.Emitter.edges_mem
#print axioms InstanceDemand.Emitter.raw_mem
#print axioms InstanceDemand.Emitter.lookup_of_functional
#print axioms InstanceDemand.Emitter.two_edge_bridge
#print axioms InstanceDemand.Emitter.emitted_has_represented_path
#print axioms InstanceDemand.Emitter.execution_output_retained
#print axioms InstanceDemand.Emitter.no_instruction_no_output
#print axioms InstanceDemand.Emitter.represented_run_keeps_graph
#print axioms InstanceDemand.Emitter.pending_mem
#print axioms InstanceDemand.Emitter.emission_replay
#print axioms InstanceDemand.Emitter.emitted_membership
#print axioms InstanceDemand.Emitter.emission_fields
#print axioms InstanceDemand.Emitter.emission_wf
#print axioms InstanceDemand.Emitter.raw_seed
#print axioms InstanceDemand.Emitter.pending_seed
#print axioms InstanceDemand.Emitter.emit_seed
#print axioms InstanceDemand.Emitter.fully_covered_collapsed
#print axioms InstanceDemand.Emitter.seed_collapsed
#print axioms InstanceDemand.Emitter.unruled_output_not_derivable
#print axioms InstanceDemand.Emitter.unruled_emission_separates
#print axioms InstanceDemand.Emitter.covered_emission_collapsed
#print axioms InstanceDemand.Emitter.seeds_replay
#print axioms InstanceDemand.Emitter.seeds_wf
#print axioms InstanceDemand.Emitter.seed_execution_bridge
#print axioms InstanceDemand.Emitter.histories_no_impose
#print axioms InstanceDemand.Emitter.native_closure_counterexample
#print axioms InstanceDemand.Emitter.no_native_join_rule
#print axioms InstanceDemand.Emitter.response_applies
#print axioms InstanceDemand.Emitter.answer_separates
#print axioms InstanceDemand.Emitter.covered_answerable
#print axioms InstanceDemand.Emitter.covered_histories_replay
