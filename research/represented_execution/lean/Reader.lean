import Control
import Runner

/-!
# Reader: a reader that reads the retained record beside the active datum

AuthorityEffect: None.

The represented execution family's machine retains a tape of visited data
and named the obstacle it left: no enablement reads that record, so two states
with one active datum and different tapes have one future. Here an enablement
reads it. A recorded setting's enablement relation hctrl p x k says operation
k may fire at the active datum x when the datum before it on the record
is p. The relation is represented in the same device as before — one binary
form per operation — by the instance (3 + nops + k, [p, x]), generalizing
the self-instance (3 + nops + k, [x, x]). The represented program is a
well-formed regime of the sealed grammar (ncodeR_wf).

When the tape has at least one previous entry, the machine reads
[previous, active] from the tape (previous). The resulting machine has
history-dependent futures: two states with the same active datum but different
tapes yield different successors, different enablements, and different futures.

Configuration status remains DECLARED_HOST_CONFIG: State is a metatheory
structure carrying encoded instances.
-/

namespace Reader

open Derivation Translation Execution Control Runner

/-! ## 1. Recorded settings and their reference semantics -/

/-- A finite setting with an enablement relation that reads the record:
hctrl p x k says the k-th operation may fire at datum x when the
datum before it on the record is p. -/
structure Recorded where
  F : FiniteSetting
  hctrl : Nat → Nat → Nat → Bool

abbrev nops (C : Recorded) : Nat := C.F.ops.length

/-- The reference step, stated on the setting before any encoding: with
p on the record before x, operation k is enabled and moves to its value
at x. -/
def RStep (C : Recorded) (p x k y : Nat) : Prop :=
  k < C.F.ops.length ∧ C.hctrl p x k = true ∧ y = C.F.ops.getD k id x

/-! ## 2. The represented program -/

/-- The control form of operation k: the one after all operation forms. -/
abbrev ctrlForm (C : Recorded) (k : Nat) : Nat := 3 + C.F.ops.length + k

/-- The record instances: on the control form of operation k, the pair
[p, x] of every admitted record entry and datum at which k is enabled. -/
def recInsts (C : Recorded) : List Inst :=
  (List.range C.F.ops.length).flatMap (fun k =>
    ((pairs C.F.n).filter (fun q => C.hctrl q.1 q.2 k)).map
      (fun q => (3 + C.F.ops.length + k, [q.1, q.2])))

theorem mem_recInsts {C : Recorded} {i : Inst} :
    i ∈ recInsts C ↔
      ∃ k, k < C.F.ops.length ∧ ∃ p x, p < C.F.n ∧ x < C.F.n ∧ C.hctrl p x k = true ∧
        i = (3 + C.F.ops.length + k, [p, x]) := by
  unfold recInsts
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨k, hk, hi⟩
    obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hi
    have hq' := List.mem_filter.mp hq
    have hb := mem_pairs.mp hq'.1
    exact ⟨k, List.mem_range.mp hk, q.1, q.2, hb.1, hb.2, hq'.2, rfl⟩
  · rintro ⟨k, hk, p, x, hp, hx, hc, rfl⟩
    exact ⟨k, List.mem_range.mpr hk,
      List.mem_map.mpr ⟨(p, x), List.mem_filter.mpr ⟨mem_pairs.mpr ⟨hp, hx⟩, hc⟩, rfl⟩⟩

/-- The represented program: the operation graphs and the record enablements.
The stores are not part of it. -/
def rprogram (C : Recorded) : List Inst := graphsFrom C.F.n 3 C.F.ops ++ recInsts C

theorem mem_rprogram {C : Recorded} {i : Inst} :
    i ∈ rprogram C ↔
      (∃ k, k < C.F.ops.length ∧ ∃ x, x < C.F.n ∧ i = (3 + k, [x, C.F.ops.getD k id x])) ∨
      (∃ k, k < C.F.ops.length ∧ ∃ p x, p < C.F.n ∧ x < C.F.n ∧ C.hctrl p x k = true ∧
        i = (3 + C.F.ops.length + k, [p, x])) := by
  show i ∈ graphsFrom C.F.n 3 C.F.ops ++ recInsts C ↔ _
  rw [List.mem_append, mem_graphsFrom, mem_recInsts]

/-- The recorded regime of the sealed grammar: the stores, the operation
graphs, and the record enablements, on 3 + 2 * nops binary forms. -/
def encodeR (C : Recorded) : Regime :=
  ⟨C.F.n,
   [2, 2, 2] ++ C.F.ops.map (fun _ => 2) ++ C.F.ops.map (fun _ => 2),
   storesFrom C.F.n 0 [C.F.rel, C.F.ret, C.F.prot] ++ rprogram C,
   [],
   []⟩

theorem encodeR_forms_length (C : Recorded) :
    (encodeR C).forms.length = 3 + C.F.ops.length + C.F.ops.length := by
  show ([2, 2, 2] ++ C.F.ops.map (fun _ => 2) ++ C.F.ops.map (fun _ => 2)).length = _
  rw [List.length_append, List.length_append, List.length_map]
  rfl

theorem encodeR_forms_two (C : Recorded) : ∀ a ∈ (encodeR C).forms, a = 2 := by
  intro a ha
  rcases List.mem_append.mp ha with h | h
  · rcases List.mem_append.mp h with h | h
    · rcases List.mem_cons.mp h with rfl | h
      · rfl
      rcases List.mem_cons.mp h with rfl | h
      · rfl
      rcases List.mem_cons.mp h with rfl | h
      · rfl
      exact absurd h List.not_mem_nil
    · obtain ⟨_, _, rfl⟩ := List.mem_map.mp h
      rfl
  · obtain ⟨_, _, rfl⟩ := List.mem_map.mp h
    rfl

theorem encodeR_forms_getD (C : Recorded) {f : Nat} (hf : f < (encodeR C).forms.length) :
    (encodeR C).forms.getD f 0 = 2 :=
  getD_of_all_two _ (encodeR_forms_two C) f hf

/-- The represented program is a well-formed regime. -/
theorem encodeR_wf (C : Recorded) : (encodeR C).wf := by
  have hlen := encodeR_forms_length C
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro q hq
    rcases List.mem_append.mp hq with hs | hg
    · rcases (mem_storesFrom 0 _).mp hs with ⟨k, hk, x, y, hx, hy, _, rfl⟩
      have hk3 : k < 3 := hk
      refine ⟨?_, ?_, two_args_lt hx hy⟩
      · show 0 + k < (encodeR C).forms.length
        omega
      · show [x, y].length = (encodeR C).forms.getD (0 + k) 0
        rw [encodeR_forms_getD C (by omega)]
        rfl
    · rcases mem_rprogram.mp hg with ⟨k, hk, x, hx, rfl⟩ | ⟨k, hk, p, x, hp, hx, _, rfl⟩
      · refine ⟨?_, ?_, two_args_lt hx (C.F.ops_closed _ (getD_mem hk) x hx)⟩
        · show 3 + k < (encodeR C).forms.length
          omega
        · show [x, C.F.ops.getD k id x].length = (encodeR C).forms.getD (3 + k) 0
          rw [encodeR_forms_getD C (by omega)]
          rfl
      · refine ⟨?_, ?_, two_args_lt hp hx⟩
        · show 3 + C.F.ops.length + k < (encodeR C).forms.length
          omega
        · show [p, x].length = (encodeR C).forms.getD (3 + C.F.ops.length + k) 0
          rw [encodeR_forms_getD C (by omega)]
          rfl
  · intro f hf
    exact absurd hf List.not_mem_nil
  · intro q hq
    exact absurd hq List.not_mem_nil
  · intro a ha
    rw [encodeR_forms_two C a ha]
    decide

/-! ## 3. Reading the program: the edge, and the record -/

/-- The operation-k edge leaving x in the program is the operation's
value: the record instances live on later forms. -/
theorem lookup_rprogram_op (C : Recorded) {k x : Nat} (hk : k < C.F.ops.length)
    (hx : x < C.F.n) : lookup (3 + k) x (rprogram C) = some (C.F.ops.getD k id x) := by
  have hmem : (3 + k, [x, C.F.ops.getD k id x]) ∈ rprogram C :=
    mem_rprogram.mpr (Or.inl ⟨k, hk, x, hx, rfl⟩)
  have hsome := lookup_isSome hmem
  cases hl : lookup (3 + k) x (rprogram C) with
  | none =>
      rw [hl] at hsome
      cases hsome
  | some y =>
      have hy : (3 + k, [x, y]) ∈ rprogram C := lookup_mem hl
      rcases mem_rprogram.mp hy with ⟨k', _, x', _, h⟩ | ⟨k', _, p', x', _, _, _, h⟩
      · injection h with h1 h2
        have hkk : k' = k := by omega
        subst hkk
        obtain ⟨rfl, rfl⟩ := list_two_inj h2
        rfl
      · injection h with h1 _
        omega

/-- Whether the instance (f, [p, x]) is present in a graph. -/
def present (f p x : Nat) : List Inst → Bool
  | [] => false
  | i :: rest => (isEdge f p i && decide (value i = x)) || present f p x rest

theorem present_iff (f p x : Nat) : ∀ (g : List Inst), present f p x g = true ↔ (f, [p, x]) ∈ g
  | [] => by
      constructor
      · intro h
        cases h
      · intro h
        exact absurd h List.not_mem_nil
  | i :: rest => by
      show ((isEdge f p i && decide (value i = x)) || present f p x rest) = true ↔ _
      rw [Bool.or_eq_true_iff, Bool.and_eq_true_iff, present_iff f p x rest, List.mem_cons,
        decide_eq_true_iff]
      constructor
      · rintro (⟨he, hv⟩ | h)
        · obtain ⟨y, rfl⟩ := isEdge_true he
          rw [value_edge] at hv
          rw [hv]
          exact Or.inl rfl
        · exact Or.inr h
      · rintro (rfl | h)
        · exact Or.inl ⟨isEdge_self f p x, rfl⟩
        · exact Or.inr h

/-- Operation k is enabled at x after p when the instance [p, x] of
its control form is present. -/
def renabled (g : List Inst) (nops p x k : Nat) : Bool := present (3 + nops + k) p x g

theorem renabled_iff {g : List Inst} {nops p x k : Nat} :
    renabled g nops p x k = true ↔ (3 + nops + k, [p, x]) ∈ g :=
  present_iff _ _ _ _

/-- The enabled operations at x after p, in index order. -/
def renabledAt (g : List Inst) (nops p x : Nat) : List Nat :=
  (List.range nops).filter (fun k => renabled g nops p x k)

theorem mem_renabledAt {g : List Inst} {nops p x k : Nat} :
    k ∈ renabledAt g nops p x ↔ k < nops ∧ renabled g nops p x k = true := by
  unfold renabledAt
  rw [List.mem_filter, List.mem_range]

/-- The record enablement is read faithfully from the program. -/
theorem renabled_rprogram (C : Recorded) {p x k : Nat} (hk : k < C.F.ops.length)
    (hp : p < C.F.n) (hx : x < C.F.n) :
    renabled (rprogram C) C.F.ops.length p x k = true ↔ C.hctrl p x k = true := by
  rw [renabled_iff, mem_rprogram]
  constructor
  · rintro (⟨k', hk', x', _, h⟩ | ⟨k', _, p', x', _, _, hc, h⟩)
    · injection h with h1 _
      omega
    · injection h with h1 h2
      have hkk : k' = k := by omega
      subst hkk
      obtain ⟨rfl, rfl⟩ := list_two_inj h2
      exact hc
  · intro hc
    exact Or.inr ⟨k, hk, p, x, hp, hx, hc, rfl⟩

/-! ## 4. Reading previous from the tape -/

/-- The datum before the last on the record. When the tape has length at
least 2, returns the second-to-last datum. On a record with one entry — the
start — returns that entry as its own predecessor, generalizing the self-instance. -/
def previous (s : State) : Nat :=
  match s.tape.reverse with
  | _ :: p :: _ => p
  | _ => s.active

/-- The reader consulting [previous, active] from the state tape. -/
def recordReader (s : State) : List Nat :=
  renabledAt s.graph s.nops (previous s) s.active

/-- Successor family under the record reader. -/
def rsuccessors (s : State) : List State :=
  (recordReader s).filterMap (fun k =>
    match fire s k with
    | .ok s' => some s'
    | _ => none)

theorem mem_rsuccessors {s s' : State} :
    s' ∈ rsuccessors s ↔
      ∃ k, k ∈ recordReader s ∧ fire s k = .ok s' := by
  unfold rsuccessors
  rw [List.mem_filterMap]
  constructor
  · rintro ⟨k, hk, h⟩
    refine ⟨k, hk, ?_⟩
    revert h
    cases fire s k with
    | ok t =>
        intro h
        have ht : some t = some s' := h
        cases ht
        rfl
    | exhausted => intro h; cases h
    | noEdge => intro h; cases h
  · rintro ⟨k, hk, h⟩
    refine ⟨k, hk, ?_⟩
    rw [h]

/-- The deterministic step of the record-reading machine: the generic runner
at the record reader. -/
def rstepDet (s : State) : Terminal ⊕ State := stepDetOf recordReader s

/-- State synced with tape: tape ends with active datum. -/
def Synced (s : State) : Prop := ∃ t, s.tape = t ++ [s.active]

theorem fire_synced {s s' : State} {k : Nat} (h : fire s k = .ok s') : Synced s' := by
  obtain ⟨-, htape, -, -, -, -⟩ := fire_ok h
  exact ⟨s.tape, htape⟩

theorem previous_fire {s s' : State} {k : Nat} (hs : Synced s) (h : fire s k = .ok s') :
    previous s' = s.active := by
  obtain ⟨t, ht⟩ := hs
  obtain ⟨-, htape, -, -, -, -⟩ := fire_ok h
  have hrev : s'.tape.reverse = s'.active :: s.active :: t.reverse := by
    rw [htape, ht, List.reverse_append, List.reverse_append]
    rfl
  show (match s'.tape.reverse with
        | _ :: p :: _ => p
        | _ => s'.active) = s.active
  rw [hrev]

/-! ## 5. Simulation and reflection -/

/-- Soundness: every successor realises a reference step at previous and active data. -/
theorem rsuccessors_sound (C : Recorded) {s s' : State} (hg : s.graph = rprogram C)
    (hn : s.nops = C.F.ops.length) (hp : previous s < C.F.n) (hx : s.active < C.F.n)
    (h : s' ∈ rsuccessors s) : ∃ k, RStep C (previous s) s.active k s'.active := by
  obtain ⟨k, hk, hf⟩ := mem_rsuccessors.mp h
  have hk' := mem_renabledAt.mp hk
  rw [hg, hn] at hk'
  have hen := (renabled_rprogram C hk'.1 hp hx).mp hk'.2
  obtain ⟨hl, -, -, -, -, -⟩ := fire_ok hf
  rw [hg, lookup_rprogram_op C hk'.1 hx] at hl
  exact ⟨k, hk'.1, hen, (Option.some.inj hl).symm⟩

/-- Completeness: every reference step with fuel left is realised by a successor. -/
theorem rsuccessors_complete (C : Recorded) {s : State} {k y : Nat} (hg : s.graph = rprogram C)
    (hn : s.nops = C.F.ops.length) (hp : previous s < C.F.n) (hx : s.active < C.F.n)
    (hs : RStep C (previous s) s.active k y) (hfuel : 0 < s.fuel) :
    ∃ s' ∈ rsuccessors s, s'.active = y := by
  obtain ⟨hk, hc, rfl⟩ := hs
  have hen : renabled (rprogram C) C.F.ops.length (previous s) s.active k = true :=
    (renabled_rprogram C hk hp hx).mpr hc
  have hmem : k ∈ recordReader s := by
    unfold recordReader
    rw [hg, hn]
    exact mem_renabledAt.mpr ⟨hk, hen⟩
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := ⟨s.fuel - 1, by omega⟩
  refine ⟨⟨s.graph, s.nops, C.F.ops.getD k id s.active, s.tape ++ [C.F.ops.getD k id s.active],
    s.clock + 1, f⟩, mem_rsuccessors.mpr ⟨k, hmem, ?_⟩, rfl⟩
  rw [fire_succ s k f hf, hg, lookup_rprogram_op C hk hx]

/-! ## 6. History-dependent futures -/

/-- A flip map on 2 points: maps 0 to 1 and anything else to 0. -/
def demoFlip (x : Nat) : Nat := if x = 0 then 1 else 0

theorem demoFlip_lt (x : Nat) : demoFlip x < 2 := by
  show (if x = 0 then 1 else 0) < 2
  split <;> decide

def demoOps : List (Nat → Nat) := [demoFlip, id]

theorem demoOps_closed : ∀ g ∈ demoOps, ∀ x, x < 2 → g x < 2 := by
  intro g hg x hx
  rcases List.mem_cons.mp hg with rfl | hg
  · exact demoFlip_lt x
  rcases List.mem_cons.mp hg with rfl | hg
  · exact hx
  exact absurd hg List.not_mem_nil

/-- A concrete setting with 2 carrier data {0, 1} and 2 operations. -/
def demoSetting : FiniteSetting where
  n := 2
  rel := fun _ _ => false
  ret := fun _ _ => false
  prot := fun _ _ => false
  a := 0
  b := 1
  ops := demoOps
  a_lt := by decide
  b_lt := by decide
  ops_closed := demoOps_closed

/-- Enablement depending on history:
At active datum 0:
- if previous was 0, operation 0 (flip) is enabled.
- if previous was 1, operation 1 (id) is enabled.
At active datum 1: no operation enabled. -/
def demoCtrl (p x k : Nat) : Bool :=
  decide ((p = 0 ∧ x = 0 ∧ k = 0) ∨ (p = 1 ∧ x = 0 ∧ k = 1))

def demoRecorded : Recorded := ⟨demoSetting, demoCtrl⟩

/-- Two states with the same active datum 0, but different tapes [0, 0] vs [1, 0]. -/
def s₁ : State := ⟨rprogram demoRecorded, 2, 0, [0, 0], 0, 5⟩
def s₂ : State := ⟨rprogram demoRecorded, 2, 0, [1, 0], 0, 5⟩

theorem same_active_datum : s₁.active = s₂.active := rfl

theorem different_tapes : s₁.tape ≠ s₂.tape := by decide

theorem different_previous : previous s₁ ≠ previous s₂ := by decide

/-- History dependence in enablements: state 1 enables operation 0, state 2 enables operation 1. -/
theorem history_dependent_enablements : recordReader s₁ ≠ recordReader s₂ := by decide

/-- History dependence in successors: state 1 transitions to 1, state 2 transitions to 0. -/
theorem history_dependent_successors : rsuccessors s₁ ≠ rsuccessors s₂ := by
  intro h
  have h1 : (rsuccessors s₁).map (fun s => s.active) = (rsuccessors s₂).map (fun s => s.active) := by rw [h]
  revert h1
  decide

/-- History dependence in deterministic futures: stepDet yields different next states. -/
theorem history_dependent_futures : rstepDet s₁ ≠ rstepDet s₂ := by
  intro h
  have h1 : Sum.map id (fun s : State => s.active) (rstepDet s₁) =
            Sum.map id (fun s : State => s.active) (rstepDet s₂) := by rw [h]
  revert h1
  decide

/-- In contrast, the memoryless machine gives identical enablements for states with same active datum. -/
theorem memoryless_same_enablements {sa sb : State} (hg : sa.graph = sb.graph)
    (hn : sa.nops = sb.nops) (ha : sa.active = sb.active) :
    Control.enabledAt sa.graph sa.nops sa.active = Control.enabledAt sb.graph sb.nops sb.active := by
  rw [ha, hg, hn]

end Reader

#print axioms Reader.mem_recInsts
#print axioms Reader.mem_rprogram
#print axioms Reader.encodeR_forms_length
#print axioms Reader.encodeR_forms_two
#print axioms Reader.encodeR_forms_getD
#print axioms Reader.encodeR_wf
#print axioms Reader.lookup_rprogram_op
#print axioms Reader.present_iff
#print axioms Reader.renabled_iff
#print axioms Reader.mem_renabledAt
#print axioms Reader.renabled_rprogram
#print axioms Reader.mem_rsuccessors
#print axioms Reader.fire_synced
#print axioms Reader.previous_fire
#print axioms Reader.rsuccessors_sound
#print axioms Reader.rsuccessors_complete
#print axioms Reader.same_active_datum
#print axioms Reader.different_tapes
#print axioms Reader.different_previous
#print axioms Reader.history_dependent_enablements
#print axioms Reader.history_dependent_successors
#print axioms Reader.history_dependent_futures
#print axioms Reader.memoryless_same_enablements
