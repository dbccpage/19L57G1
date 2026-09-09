import Observe

/-!
# Record: an enablement that reads the retained record

The represented execution family's machine retains a tape of the data
visited, and its second commit named the obstacle it left: no enablement
reads that record, so two states with one active datum and different tapes
have one future.  Here an enablement reads it.  A *recorded* setting's
enablement relation `hctrl p x k` says operation `k` may fire at the active
datum `x` when the datum before it on the record is `p`, and the relation is
represented in the same device as before — one binary form per operation —
by the instance `(3 + nops + k, [p, x])` rather than the self-instance
`(3 + nops + k, [x, x])`.  The represented program is again a well-formed
regime of the sealed grammar (`encodeR_wf`).

The interpreter is the merged one with one change: before reading the edge
it reads the record.  `previous s` is the entry before the last on the tape
(the start is its own predecessor), `renabled` is the presence of the
instance `(3 + nops + k, [previous, active])`, and `fire` is the merged
`fire` unchanged.  What it delivers, and what it refuses:

* **The record is read by the process.**  A firing makes the datum it left
  the `previous` of the state it reaches (`previous_fire`): the enablement
  at the next step reads what the last step wrote, and nothing outside the
  state — no host log — supplies it.
* **Simulation and reflection** against the reference step `RStep`, stated
  on the setting before any encoding (`rsuccessors_sound`,
  `rsuccessors_complete`).
* **The memoryless class embeds.**  A controlled setting whose enablement
  ignores the record is a recorded setting (`lift`), with the same reference
  step (`lift_RStep`) and the same enablement read (`lift_renabled`).
* **The distinction is real, and disappears with the record.**  On the
  three-point setting of the observed family, the program `twist` visits
  `0, 1, 0, 0` from datum 0 (`twist_tape`): at its third step it sits at
  datum 0 as at its first and moves elsewhere (`record_is_read`).  No
  memoryless run does that — a run of the merged machine that returns to a
  datum leaves it the same way (`memoryless_functional`).  Forgetting the
  record (`forget`) projects `twist` to a memoryless program, and the
  distinction disappears: the run halts at `[0, 1]` (`forget_twist`).
* **Never selects; only appends.**  `rrun_branch`, `rnext_tape`,
  `robs_prefix`, as for the merged machine.

Configuration status remains **DECLARED_HOST_CONFIG**: the state is the
merged `State`, a metatheory structure carrying encoded instances.  The
proofs unfold the machine's definitions by `show` and by definitional
`have`, never by `simp`.

AuthorityEffect: None.
-/

namespace Record

open Derivation Translation Execution Control

/-! ## 1. Recorded settings and their reference semantics -/

/-- A finite setting with an enablement relation that reads the record:
`hctrl p x k` says the `k`-th operation may fire at datum `x` when the datum
before it on the record is `p`. -/
structure Recorded where
  F : FiniteSetting
  hctrl : Nat → Nat → Nat → Bool

/-- **The reference step**, stated on the setting before any encoding: with
`p` on the record before `x`, operation `k` is enabled and moves to its value
at `x`. -/
def RStep (C : Recorded) (p x k y : Nat) : Prop :=
  k < C.F.ops.length ∧ C.hctrl p x k = true ∧ y = C.F.ops.getD k id x

/-! ## 2. The represented program -/

/-- The record instances: on the control form of operation `k`, the pair
`[p, x]` of every admitted record entry and datum at which `k` is enabled. -/
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

/-- The represented program: the operation graphs and the record
enablements.  The stores are not part of it. -/
def rprogram (C : Recorded) : List Inst := graphsFrom C.F.n 3 C.F.ops ++ recInsts C

theorem mem_rprogram {C : Recorded} {i : Inst} :
    i ∈ rprogram C ↔
      (∃ k, k < C.F.ops.length ∧ ∃ x, x < C.F.n ∧ i = (3 + k, [x, C.F.ops.getD k id x])) ∨
      (∃ k, k < C.F.ops.length ∧ ∃ p x, p < C.F.n ∧ x < C.F.n ∧ C.hctrl p x k = true ∧
        i = (3 + C.F.ops.length + k, [p, x])) := by
  show i ∈ graphsFrom C.F.n 3 C.F.ops ++ recInsts C ↔ _
  rw [List.mem_append, mem_graphsFrom, mem_recInsts]

/-- The recorded regime of the sealed grammar: the stores, the operation
graphs, and the record enablements, on `3 + 2 · nops` binary forms. -/
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

/-- **The represented program is a well-formed regime.** -/
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

/-- The operation-`k` edge leaving `x` in the program is the operation's
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

/-- Whether the instance `(f, [p, x])` is present in a graph.  A relation is
read, not a function: several instances of one form may leave `p`. -/
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

/-- Operation `k` is enabled at `x` after `p` when the instance `[p, x]` of
its control form is present. -/
def renabled (g : List Inst) (nops p x k : Nat) : Bool := present (3 + nops + k) p x g

theorem renabled_iff {g : List Inst} {nops p x k : Nat} :
    renabled g nops p x k = true ↔ (3 + nops + k, [p, x]) ∈ g :=
  present_iff _ _ _ _

/-- The enabled operations at `x` after `p`, in index order.  Nothing below
reads the first element as a choice. -/
def renabledAt (g : List Inst) (nops p x : Nat) : List Nat :=
  (List.range nops).filter (fun k => renabled g nops p x k)

theorem mem_renabledAt {g : List Inst} {nops p x k : Nat} :
    k ∈ renabledAt g nops p x ↔ k < nops ∧ renabled g nops p x k = true := by
  unfold renabledAt
  rw [List.mem_filter, List.mem_range]

/-- **The record enablement is read faithfully** from the program. -/
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

/-! ## 4. The record, and the interpreter that reads it -/

/-- The datum before the last on the record.  A record with one entry — the
start — has that entry as its own predecessor. -/
def previous (s : State) : Nat :=
  match s.tape.reverse with
  | _ :: p :: _ => p
  | _ => s.active

/-- The successor family: one state per operation enabled at the active
datum after the recorded one, that fires.  `fire` is the merged one. -/
def rsuccessors (s : State) : List State :=
  (renabledAt s.graph s.nops (previous s) s.active).filterMap (fun k =>
    match fire s k with
    | .ok s' => some s'
    | _ => none)

/-- One step of the deterministic runner: it reads the record, fires the one
enabled operation, halts when none is enabled, and stops with `branch` when
two are — it never selects. -/
def rstepDet (s : State) : Terminal ⊕ State :=
  match renabledAt s.graph s.nops (previous s) s.active with
  | [] => .inl .halt
  | [k] =>
    match fire s k with
    | .ok s' => .inr s'
    | .exhausted => .inl .exhausted
    | .noEdge => .inl .refuse
  | _ :: _ :: _ => .inl .branch

def rrunDet : Nat → State → Terminal × State
  | 0, s =>
    match rstepDet s with
    | .inl t => (t, s)
    | .inr _ => (.exhausted, s)
  | b + 1, s =>
    match rstepDet s with
    | .inl t => (t, s)
    | .inr s' => rrunDet b s'

def rrun (s : State) : Terminal × State := rrunDet s.fuel s

/-- The initial state of a recorded setting: its program, a start datum, the
start on the record, clock zero, a declared fuel. -/
def rinit (C : Recorded) (x fuel : Nat) : State :=
  ⟨rprogram C, C.F.ops.length, x, [x], 0, fuel⟩

/-- One step of the runner as a function: a terminal keeps the state. -/
def rnext (s : State) : State :=
  match rstepDet s with
  | .inr s' => s'
  | .inl _ => s

def riter : Nat → State → State
  | 0, s => s
  | n + 1, s => rnext (riter n s)

/-- The observation at scale `n`: the record after `n` steps. -/
def robs (n : Nat) (s : State) : List Nat := (riter n s).tape

/-- The value the record-reading runner moves to at the active datum after the
recorded one: the value of the one operation enabled there, and none when
none, two, or no edge.  The fuel is not read: this is what the *program* says
about the pair. -/
def rnextOf (g : List Inst) (nops p x : Nat) : Option Nat :=
  match renabledAt g nops p x with
  | [k] => lookup (3 + k) x g
  | _ => none

/-- **One step of the record-reading runner, by its next value.**  Either it
stops — no fuel, or no next value — or it moves to the next value, appending
it, ticking the clock and spending one fuel. -/
theorem rstepDet_spec (s : State) :
    ((s.fuel = 0 ∨ rnextOf s.graph s.nops (previous s) s.active = none) ∧
        ∃ t, rstepDet s = .inl t) ∨
      ∃ f y, s.fuel = f + 1 ∧ rnextOf s.graph s.nops (previous s) s.active = some y ∧
        rstepDet s = .inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ := by
  have hstep : rstepDet s = (match renabledAt s.graph s.nops (previous s) s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) := rfl
  have hval : rnextOf s.graph s.nops (previous s) s.active =
      (match renabledAt s.graph s.nops (previous s) s.active with
        | [k] => lookup (3 + k) s.active s.graph
        | _ => none) := rfl
  rw [hstep, hval]
  cases renabledAt s.graph s.nops (previous s) s.active with
  | nil => exact Or.inl ⟨Or.inr rfl, Terminal.halt, rfl⟩
  | cons k rest =>
      cases rest with
      | nil =>
          show ((s.fuel = 0 ∨ lookup (3 + k) s.active s.graph = none) ∧
                ∃ t, (match fire s k with
                      | .ok s' => Sum.inr s'
                      | .exhausted => Sum.inl Terminal.exhausted
                      | .noEdge => Sum.inl Terminal.refuse) = Sum.inl t) ∨
              ∃ f y, s.fuel = f + 1 ∧ lookup (3 + k) s.active s.graph = some y ∧
                (match fire s k with
                 | .ok s' => Sum.inr s'
                 | .exhausted => Sum.inl Terminal.exhausted
                 | .noEdge => Sum.inl Terminal.refuse) =
                  Sum.inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩
          cases hfu : s.fuel with
          | zero =>
              rw [fire_exhausted hfu]
              exact Or.inl ⟨Or.inl rfl, Terminal.exhausted, rfl⟩
          | succ f =>
              rw [fire_succ s k f hfu]
              cases lookup (3 + k) s.active s.graph with
              | none => exact Or.inl ⟨Or.inr rfl, Terminal.refuse, rfl⟩
              | some y => exact Or.inr ⟨f, y, rfl, rfl, rfl⟩
      | cons k' rest' => exact Or.inl ⟨Or.inr rfl, Terminal.branch, rfl⟩

theorem rnext_of_inl {s : State} {t : Terminal} (h : rstepDet s = .inl t) : rnext s = s := by
  show (match rstepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

theorem rnext_of_inr {s s' : State} (h : rstepDet s = .inr s') : rnext s = s' := by
  show (match rstepDet s with | .inr s' => s' | .inl _ => s) = s'
  rw [h]

theorem mem_rsuccessors {s s' : State} :
    s' ∈ rsuccessors s ↔
      ∃ k, k ∈ renabledAt s.graph s.nops (previous s) s.active ∧ fire s k = .ok s' := by
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

/-! ## 5. The record is what the process wrote -/

/-- A state whose record ends with its active datum. -/
def Synced (s : State) : Prop := ∃ t, s.tape = t ++ [s.active]

theorem rinit_synced (C : Recorded) (x fuel : Nat) : Synced (rinit C x fuel) := ⟨[], rfl⟩

theorem previous_rinit (C : Recorded) (x fuel : Nat) : previous (rinit C x fuel) = x := rfl

/-- A firing keeps the record synced. -/
theorem fire_synced {s s' : State} {k : Nat} (h : fire s k = .ok s') : Synced s' := by
  obtain ⟨-, htape, -, -, -, -⟩ := fire_ok h
  exact ⟨s.tape, htape⟩

/-- **The record is read by the process.**  After a firing, the datum the
step left is the `previous` the next enablement reads. -/
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

/-! ## 6. Simulation and reflection against the reference step -/

/-- **Soundness.**  Every successor of a state carrying the program realises
a reference step at the recorded datum and the active one. -/
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

/-- **Completeness.**  Every reference step at the recorded and active data,
given fuel, is realised by a successor. -/
theorem rsuccessors_complete (C : Recorded) {s : State} {k y : Nat} (hg : s.graph = rprogram C)
    (hn : s.nops = C.F.ops.length) (hp : previous s < C.F.n) (hx : s.active < C.F.n)
    (hs : RStep C (previous s) s.active k y) (hfuel : 0 < s.fuel) :
    ∃ s' ∈ rsuccessors s, s'.active = y := by
  obtain ⟨hk, hc, rfl⟩ := hs
  have hen : renabled (rprogram C) C.F.ops.length (previous s) s.active k = true :=
    (renabled_rprogram C hk hp hx).mpr hc
  have hmem : k ∈ renabledAt s.graph s.nops (previous s) s.active := by
    rw [hg, hn]
    exact mem_renabledAt.mpr ⟨hk, hen⟩
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := ⟨s.fuel - 1, by omega⟩
  refine ⟨⟨s.graph, s.nops, C.F.ops.getD k id s.active, s.tape ++ [C.F.ops.getD k id s.active],
    s.clock + 1, f⟩, mem_rsuccessors.mpr ⟨k, hmem, ?_⟩, rfl⟩
  rw [fire_succ s k f hf, hg, lookup_rprogram_op C hk hx]

/-! ## 7. The memoryless class embeds -/

/-- A controlled setting read as a recorded one: the enablement ignores the
record. -/
def lift (C : Controlled) : Recorded := ⟨C.F, fun _ x k => C.ctrl x k⟩

theorem lift_RStep (C : Controlled) (p x k y : Nat) : RStep (lift C) p x k y ↔ CStep C x k y :=
  Iff.rfl

/-- The lifted program reads, at every record entry, what the merged program
reads at the datum. -/
theorem lift_renabled (C : Controlled) {p x k : Nat} (hk : k < C.F.ops.length) (hp : p < C.F.n)
    (hx : x < C.F.n) :
    renabled (rprogram (lift C)) C.F.ops.length p x k = true ↔
      enabled (program C) C.F.ops.length x k = true :=
  (renabled_rprogram (lift C) hk hp hx).trans (enabled_program C hk hx).symm

/-- A recorded setting read as a controlled one: the record is forgotten, and
the enablement is read at the datum as its own predecessor. -/
def forget (C : Recorded) : Controlled := ⟨C.F, fun x k => C.hctrl x x k⟩

/-! ## 8. The distinction, and its disappearance -/

/-- On the observed family's three-point setting: the cycle at datum 0 after
0, the constant map at datum 1 after 0, and the constant map at datum 0
after 1.  The operations are the family's: `0` the cycle, `1` the constant
map, `2` the climb. -/
def twist : Recorded :=
  ⟨Observe.base, fun p x k =>
    decide ((p = 0 ∧ x = 0 ∧ k = 0) ∨ (p = 0 ∧ x = 1 ∧ k = 1) ∨ (p = 1 ∧ x = 0 ∧ k = 1))⟩

/-- From datum 0 the run visits `0, 1, 0, 0`: it leaves datum 0 twice, by
different operations, because the record differs. -/
theorem twist_tape : robs 3 (rinit twist 0 3) = [0, 1, 0, 0] := by decide

theorem twist_period : robs 6 (rinit twist 0 6) = [0, 1, 0, 0, 1, 0, 0] := by decide

/-- **The record is read.**  At its third step the run is at the datum it
started from, and moves elsewhere than it did the first time. -/
theorem record_is_read :
    (riter 2 (rinit twist 0 3)).active = (rinit twist 0 3).active ∧
      (riter 3 (rinit twist 0 3)).active ≠ (riter 1 (rinit twist 0 3)).active := by decide

/-- **No memoryless run does that.**  Three steps of the merged machine
that return to the datum they started from leave it the same way. -/
theorem memoryless_functional {s s1 s2 s3 : State} (h1 : stepDet s = .inr s1)
    (h2 : stepDet s1 = .inr s2) (h3 : stepDet s2 = .inr s3) (ha : s2.active = s.active) :
    s3.active = s1.active := by
  obtain ⟨_, -, hf1⟩ := Observe.stepDet_inr h1
  obtain ⟨-, -, -, -, hg1, hn1⟩ := fire_ok hf1
  obtain ⟨_, -, hf2⟩ := Observe.stepDet_inr h2
  obtain ⟨-, -, -, -, hg2, hn2⟩ := fire_ok hf2
  exact Observe.next_active_det (by rw [hg2, hg1]) (by rw [hn2, hn1]) ha h3 h1

/-- **Remove the record and the distinction disappears.**  The projection of
`twist` to a memoryless program halts after one step. -/
theorem forget_twist : Observe.obs 3 (Control.init (forget twist) 0 3) = [0, 1] := by decide

/-! ## 9. The runner never selects, and only appends -/

theorem rstepDet_inr {s s' : State} (h : rstepDet s = .inr s') :
    ∃ k, renabledAt s.graph s.nops (previous s) s.active = [k] ∧ fire s k = .ok s' := by
  revert h
  show (match renabledAt s.graph s.nops (previous s) s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inr s' → _
  cases he : renabledAt s.graph s.nops (previous s) s.active with
  | nil =>
      intro h
      cases h
  | cons k rest =>
      cases rest with
      | nil =>
          show (match fire s k with
                | .ok s' => Sum.inr s'
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) = Sum.inr s' → _
          cases hf : fire s k with
          | ok t =>
              intro h
              have h' : Sum.inr t = Sum.inr s' := h
              cases h'
              exact ⟨k, rfl, hf⟩
          | exhausted =>
              intro h
              have h' : Sum.inl Terminal.exhausted = Sum.inr s' := h
              cases h'
          | noEdge =>
              intro h
              have h' : Sum.inl Terminal.refuse = Sum.inr s' := h
              cases h'
      | cons k' rest' =>
          intro h
          have h' : Sum.inl Terminal.branch = Sum.inr s' := h
          cases h'

/-- A step only appends. -/
theorem rnext_tape (s : State) : s.tape <+: (rnext s).tape := by
  show s.tape <+: (match rstepDet s with | .inr s' => s' | .inl _ => s).tape
  cases hs : rstepDet s with
  | inl t => exact List.prefix_refl _
  | inr s' =>
      obtain ⟨k, -, hf⟩ := rstepDet_inr hs
      obtain ⟨-, ht, -, -, -, -⟩ := fire_ok hf
      rw [ht]
      exact List.prefix_append _ _

/-- **Compatibility at every scale** for the record-reading process. -/
theorem robs_prefix (n : Nat) (s : State) : robs n s <+: robs (n + 1) s :=
  rnext_tape (riter n s)

theorem robs_prefix_add (m : Nat) (s : State) : ∀ k, robs m s <+: robs (m + k) s
  | 0 => List.prefix_refl _
  | k + 1 => (robs_prefix_add m s k).trans (robs_prefix (m + k) s)

/-- One step never selects: `branch` only when two operations are enabled. -/
theorem rstepDet_branch {s : State} (h : rstepDet s = .inl .branch) :
    2 ≤ (renabledAt s.graph s.nops (previous s) s.active).length := by
  revert h
  show (match renabledAt s.graph s.nops (previous s) s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.branch →
      2 ≤ (renabledAt s.graph s.nops (previous s) s.active).length
  cases renabledAt s.graph s.nops (previous s) s.active with
  | nil =>
      intro h
      cases h
  | cons k rest =>
      cases rest with
      | nil =>
          show (match fire s k with
                | .ok s' => Sum.inr s'
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.branch →
              2 ≤ [k].length
          cases fire s k with
          | ok s' =>
              intro h
              have h' : Sum.inr s' = Sum.inl Terminal.branch := h
              cases h'
          | exhausted =>
              intro h
              have h' : Sum.inl Terminal.exhausted = Sum.inl Terminal.branch := h
              cases h'
          | noEdge =>
              intro h
              have h' : Sum.inl Terminal.refuse = Sum.inl Terminal.branch := h
              cases h'
      | cons k' rest' =>
          intro _
          show 2 ≤ rest'.length + 2
          exact Nat.le_add_left 2 rest'.length

def RBranchOk (p : Terminal × State) : Prop :=
  p.1 = .branch → 2 ≤ (renabledAt p.2.graph p.2.nops (previous p.2) p.2.active).length

theorem rrunDet_branch : ∀ (b : Nat) (s : State), RBranchOk (rrunDet b s)
  | 0, s => by
      show RBranchOk (match rstepDet s with
                      | .inl t => (t, s)
                      | .inr _ => (Terminal.exhausted, s))
      cases hs : rstepDet s with
      | inl t =>
          intro h
          have ht : t = Terminal.branch := h
          subst ht
          exact rstepDet_branch hs
      | inr s' =>
          intro h
          cases h
  | b + 1, s => by
      show RBranchOk (match rstepDet s with
                      | .inl t => (t, s)
                      | .inr s' => rrunDet b s')
      cases hs : rstepDet s with
      | inl t =>
          intro h
          have ht : t = Terminal.branch := h
          subst ht
          exact rstepDet_branch hs
      | inr s' => exact rrunDet_branch b s'

theorem rrun_branch (s : State) : RBranchOk (rrun s) := rrunDet_branch s.fuel s

/-! ## 10. The record-reading tape is a chain, and functional in its pairs

The memoryless machine's tape is functional in its single entries (the
observed family's `obs_functional`).  Reading one entry of the record buys
exactly one more: the tape of a record-reading run is functional in its
*pairs* — the entry after two given entries is determined.  That is the ceiling
of a depth-one read, and what a deeper read has to break. -/

/-- The consecutive triples of a list: two entries and the one after them. -/
def triplesOf : List Nat → List (Nat × Nat × Nat)
  | x :: y :: z :: rest => (x, y, z) :: triplesOf (y :: z :: rest)
  | _ => []

/-- The last two entries of a list, in order. -/
def lastTwo : List Nat → Option (Nat × Nat)
  | [] => none
  | [_] => none
  | [a, b] => some (a, b)
  | _ :: y :: z :: rest => lastTwo (y :: z :: rest)

theorem lastTwo_reverse : ∀ (l : List Nat) {p x : Nat}, lastTwo l = some (p, x) →
    ∃ r, l.reverse = x :: p :: r
  | [], _, _, h => by cases h
  | [_], _, _, h => by cases h
  | [a, b], p, x, h => by
      have h' : (a, b) = (p, x) := Option.some.inj h
      injection h' with h1 h2
      subst h1
      subst h2
      exact ⟨[], rfl⟩
  | a :: y :: z :: rest, p, x, h => by
      obtain ⟨r, hr⟩ := lastTwo_reverse (y :: z :: rest) h
      refine ⟨r ++ [a], ?_⟩
      rw [List.reverse_cons, hr]
      rfl

theorem lastTwo_ne_none : ∀ (a b : Nat) (l : List Nat), lastTwo (a :: b :: l) ≠ none
  | _, _, [], h => by cases h
  | _, b, c :: rest, h => lastTwo_ne_none b c rest h

theorem triplesOf_snoc_none : ∀ (l : List Nat) (y : Nat), lastTwo l = none →
    triplesOf (l ++ [y]) = triplesOf l
  | [], _, _ => rfl
  | [_], _, _ => rfl
  | _ :: _ :: _, _, h => absurd h (lastTwo_ne_none _ _ _)

theorem triplesOf_snoc : ∀ (l : List Nat) {p x : Nat} (y : Nat), lastTwo l = some (p, x) →
    triplesOf (l ++ [y]) = triplesOf l ++ [(p, x, y)]
  | [], _, _, _, h => by cases h
  | [_], _, _, _, h => by cases h
  | [a, b], p, x, y, h => by
      have h' : (a, b) = (p, x) := Option.some.inj h
      injection h' with h1 h2
      subst h1
      subst h2
      rfl
  | a :: b :: c :: rest, p, x, y, h => by
      have h2 : lastTwo (b :: c :: rest) = some (p, x) := h
      show (a, b, c) :: triplesOf (b :: c :: (rest ++ [y])) = _
      rw [show (b :: c :: (rest ++ [y]) : List Nat) = (b :: c :: rest) ++ [y] from rfl,
        triplesOf_snoc (b :: c :: rest) y h2]
      rfl

/-- A tape is a chain of the record-reading machine when each entry is the
next value of the two before it. -/
def RChain (g : List Inst) (nops : Nat) (l : List Nat) : Prop :=
  ∀ t ∈ triplesOf l, rnextOf g nops t.1 t.2.1 = some t.2.2

/-- **A record chain is functional in its pairs.** -/
theorem rchain_functional {g : List Inst} {nops : Nat} {l : List Nat} (h : RChain g nops l)
    {t u : Nat × Nat × Nat} (ht : t ∈ triplesOf l) (hu : u ∈ triplesOf l)
    (h1 : t.1 = u.1) (h2 : t.2.1 = u.2.1) : t.2.2 = u.2.2 := by
  have hv := h t ht
  have hw := h u hu
  rw [h1, h2] at hv
  exact Option.some.inj (hv.symm.trans hw)

theorem previous_of_reverse {s : State} {p x : Nat} {r : List Nat}
    (h : s.tape.reverse = x :: p :: r) : previous s = p := by
  show (match s.tape.reverse with | _ :: p :: _ => p | _ => s.active) = p
  rw [h]

theorem getLast?_snoc (l : List Nat) (y : Nat) : (l ++ [y]).getLast? = some y := by simp

/-- A step keeps the tape a record chain and keeps the last entry active. -/
theorem rnext_chain {s : State} (hc : RChain s.graph s.nops s.tape)
    (hl : s.tape.getLast? = some s.active) :
    RChain (rnext s).graph (rnext s).nops (rnext s).tape ∧
      (rnext s).tape.getLast? = some (rnext s).active := by
  rcases rstepDet_spec s with ⟨-, t, hs⟩ | ⟨f, y, -, hv, hs⟩
  · rw [rnext_of_inl hs]
    exact ⟨hc, hl⟩
  · rw [rnext_of_inr hs]
    refine ⟨?_, getLast?_snoc _ _⟩
    intro u hu
    cases h2 : lastTwo s.tape with
    | none =>
        rw [triplesOf_snoc_none s.tape y h2] at hu
        exact hc u hu
    | some q =>
        obtain ⟨r, hr⟩ := lastTwo_reverse s.tape (by rw [h2])
        have hq : q.1 = previous s := (previous_of_reverse hr).symm
        have hx : q.2 = s.active := by
          have hh : s.tape.reverse.head? = s.tape.getLast? := by simp
          rw [hr] at hh
          exact Option.some.inj (hh.trans hl)
        rw [show q = (q.1, q.2) from rfl] at h2
        rw [triplesOf_snoc s.tape y h2, List.mem_append] at hu
        rcases hu with h | h
        · exact hc u h
        · rw [List.mem_singleton.mp h, hq, hx]
          exact hv

theorem riter_succ : ∀ (n : Nat) (s : State), riter (n + 1) s = riter n (rnext s)
  | 0, _ => rfl
  | n + 1, s => by
      show rnext (riter (n + 1) s) = rnext (riter n (rnext s))
      rw [riter_succ n s]

theorem riter_chain : ∀ (n : Nat) (s : State), RChain s.graph s.nops s.tape →
    s.tape.getLast? = some s.active →
    RChain (riter n s).graph (riter n s).nops (riter n s).tape ∧
      (riter n s).tape.getLast? = some (riter n s).active
  | 0, _, hc, hl => ⟨hc, hl⟩
  | n + 1, s, hc, hl => by
      rw [riter_succ]
      obtain ⟨hc', hl'⟩ := rnext_chain hc hl
      exact riter_chain n (rnext s) hc' hl'

theorem rinit_chain (C : Recorded) (x fuel : Nat) :
    RChain (rinit C x fuel).graph (rinit C x fuel).nops (rinit C x fuel).tape ∧
      (rinit C x fuel).tape.getLast? = some (rinit C x fuel).active :=
  ⟨fun _ hu => absurd hu List.not_mem_nil, rfl⟩

/-- **The ceiling of a depth-one read.**  Every tape a record-reading run
realises is functional in its pairs: two places where the same datum follows
the same datum are followed by the same datum.  A tape that breaks this is
realised by no record-reading program at all. -/
theorem robs_functional (C : Recorded) (x fuel n : Nat) {t u : Nat × Nat × Nat}
    (ht : t ∈ triplesOf (robs n (rinit C x fuel)))
    (hu : u ∈ triplesOf (robs n (rinit C x fuel)))
    (h1 : t.1 = u.1) (h2 : t.2.1 = u.2.1) : t.2.2 = u.2.2 :=
  rchain_functional
    (riter_chain n _ (rinit_chain C x fuel).1 (rinit_chain C x fuel).2).1 ht hu h1 h2

/-! ## 11. This machine is the generic runner at a deeper reader

The producer family parameterised the interpreter over an enablement reader
`State → List Nat` and asked whether a reader must see more than the state.
This family is the first answer: reading one entry of the record needs
`previous s`, which is a function of the state, so the reader is still a
reader and this runner is the generic one at it.

Every theorem of §9 and the compatibility of §7 are therefore instances, and
the copies in this file are copies and not obligations. -/

/-- What the record-reading machine reads: the enablements at the active datum
after the one before it on the record. -/
def recordReader (s : State) : List Nat :=
  renabledAt s.graph s.nops (previous s) s.active

/-- **The identification, by `rfl`.** -/
theorem rstepDet_is_generic (s : State) :
    rstepDet s = Runner.stepDetOf recordReader s := rfl

theorem rnext_is_generic (s : State) : rnext s = Runner.nextOf recordReader s := rfl

theorem riter_is_generic : ∀ (n : Nat) (s : State),
    riter n s = Runner.iterOf recordReader n s
  | 0, _ => rfl
  | n + 1, s => by
      show rnext (riter n s) = Runner.nextOf recordReader (Runner.iterOf recordReader n s)
      rw [riter_is_generic n s, rnext_is_generic]

theorem robs_is_generic (n : Nat) (s : State) :
    robs n s = Runner.obsOf recordReader n s := by
  show (riter n s).tape = (Runner.iterOf recordReader n s).tape
  rw [riter_is_generic n s]

theorem rrunDet_is_generic : ∀ (b : Nat) (s : State),
    rrunDet b s = Runner.runDetOf recordReader b s
  | 0, _ => rfl
  | b + 1, s => by
      cases h : rstepDet s with
      | inl t =>
          have h1 : rrunDet (b + 1) s = (t, s) := by
            show (match rstepDet s with | .inl t => (t, s) | .inr s' => rrunDet b s') = (t, s)
            rw [h]
          have h2 : Runner.runDetOf recordReader (b + 1) s = (t, s) := by
            show (match Runner.stepDetOf recordReader s with
                  | .inl t => (t, s)
                  | .inr s' => Runner.runDetOf recordReader b s') = (t, s)
            rw [← rstepDet_is_generic s, h]
          rw [h1, h2]
      | inr s' =>
          have h1 : rrunDet (b + 1) s = rrunDet b s' := by
            show (match rstepDet s with | .inl t => (t, s) | .inr s' => rrunDet b s') = _
            rw [h]
          have h2 : Runner.runDetOf recordReader (b + 1) s
              = Runner.runDetOf recordReader b s' := by
            show (match Runner.stepDetOf recordReader s with
                  | .inl t => (t, s)
                  | .inr s' => Runner.runDetOf recordReader b s') = _
            rw [← rstepDet_is_generic s, h]
          rw [h1, h2, rrunDet_is_generic b s']

/-- And so this family's compatibility is the generic one, not a second proof
of it. -/
theorem robs_prefix_is_generic (m : Nat) (s : State) (k : Nat) :
    robs m s <+: robs (m + k) s := by
  rw [robs_is_generic m s, robs_is_generic (m + k) s]
  exact Runner.obsOf_prefix_add recordReader m s k


end Record

#print axioms Record.mem_recInsts
#print axioms Record.mem_rprogram
#print axioms Record.encodeR_forms_length
#print axioms Record.encodeR_forms_two
#print axioms Record.encodeR_forms_getD
#print axioms Record.encodeR_wf
#print axioms Record.lookup_rprogram_op
#print axioms Record.present_iff
#print axioms Record.renabled_iff
#print axioms Record.mem_renabledAt
#print axioms Record.renabled_rprogram
#print axioms Record.rstepDet_spec
#print axioms Record.rnext_of_inl
#print axioms Record.rnext_of_inr
#print axioms Record.mem_rsuccessors
#print axioms Record.rinit_synced
#print axioms Record.previous_rinit
#print axioms Record.fire_synced
#print axioms Record.previous_fire
#print axioms Record.rsuccessors_sound
#print axioms Record.rsuccessors_complete
#print axioms Record.lift_RStep
#print axioms Record.lift_renabled
#print axioms Record.twist_tape
#print axioms Record.twist_period
#print axioms Record.record_is_read
#print axioms Record.memoryless_functional
#print axioms Record.forget_twist
#print axioms Record.rstepDet_inr
#print axioms Record.rnext_tape
#print axioms Record.robs_prefix
#print axioms Record.robs_prefix_add
#print axioms Record.rstepDet_branch
#print axioms Record.rrunDet_branch
#print axioms Record.lastTwo_reverse
#print axioms Record.lastTwo_ne_none
#print axioms Record.triplesOf_snoc_none
#print axioms Record.triplesOf_snoc
#print axioms Record.rchain_functional
#print axioms Record.previous_of_reverse
#print axioms Record.getLast?_snoc
#print axioms Record.rnext_chain
#print axioms Record.riter_succ
#print axioms Record.riter_chain
#print axioms Record.rinit_chain
#print axioms Record.robs_functional
#print axioms Record.rrun_branch
#print axioms Record.rstepDet_is_generic
#print axioms Record.rnext_is_generic
#print axioms Record.riter_is_generic
#print axioms Record.robs_is_generic
#print axioms Record.rrunDet_is_generic
#print axioms Record.robs_prefix_is_generic
