import Execution

/-!
# Control: data-dependent execution driven by represented instances

Commit 1 ran a *fixed word* of operation indices.  Here the next operation
is chosen by the data: a controlled setting adds an enablement relation
`ctrl x k` — operation `k` may fire at datum `x` — and the relation is
represented in the same device the merged encoder uses for stores and
operations, as one more binary form per operation whose **self-instance**
`(3 + nops + k, [x, x])` says `k` is enabled at `x`.  Every argument is a
datum, so the represented program (operation graphs and enablements) is a
well-formed regime of the sealed grammar (`encodeC_wf`).

A fixed interpreter reads the enablements at the active datum
(`enabledAt`), then the chosen operation's edge (`fire`), and moves.  Its
code never changes; the program is the instances it reads.  What it
delivers, and what it refuses:

* **Branching by data.** Which operation fires depends on the active datum;
  the successor family `successors` lists one state per enabled operation
  and is characterised by membership (`mem_successors`), never by a first
  element.
* **Determinism enforced, not assumed.** The deterministic runner `run`
  stops with the terminal `branch` when two operations are enabled; it never
  selects by list order (`runDet_branch`).
* **Terminals apart.** `halt` (no enabled operation), `exhausted` (the
  represented fuel is spent), `refuse` (an enabled operation without an
  edge: a malformed program), `branch`.
* **Bookkeeping laws.** `clock` advances exactly when an operation edge is
  applied (`fire_ok`); `fuel` is spent by exactly one per firing and is
  renewed by nothing (`fire_exhausted`).
* **Absent, not ignored.** The state carries the program only: operation
  and enablement instances.  The stores — the difference relation,
  retention, protection — are not loaded (`program`), and `init` does not
  depend on the designated pair (`init_pair`).
* **Simulation and reflection.** Against the reference relation `CStep`,
  stated on the setting before any encoding: every successor realises a
  reference step (`successors_sound`) and every reference step with fuel
  left is realised (`successors_complete`).

Configuration status remains **DECLARED_HOST_CONFIG**: `State` is a
metatheory structure carrying encoded instances.  The proofs unfold the
machine's definitions by `show` and by definitional `have`, never by `simp`.

AuthorityEffect: None.
-/

namespace Control

open Derivation Translation Execution

/-! ## 1. Controlled settings and their reference semantics -/

/-- A finite setting with an enablement relation: `ctrl x k` says the
`k`-th operation may fire at datum `x`. -/
structure Controlled where
  F : FiniteSetting
  ctrl : Nat → Nat → Bool

abbrev nops (C : Controlled) : Nat := C.F.ops.length

/-- **The reference step**, stated on the setting before any encoding:
from `x`, operation `k` is enabled and moves to its value at `x`. -/
def CStep (C : Controlled) (x k y : Nat) : Prop :=
  k < C.F.ops.length ∧ C.ctrl x k = true ∧ y = C.F.ops.getD k id x

/-! ## 2. The represented program -/

/-- The control form of operation `k`: the one after all operation forms. -/
abbrev ctrlForm (C : Controlled) (k : Nat) : Nat := 3 + C.F.ops.length + k

/-- The enablement instances: the self-instance of `k`'s control form at
each admitted datum where `k` is enabled. -/
def ctrlInsts (C : Controlled) : List Inst :=
  (List.range C.F.ops.length).flatMap (fun k =>
    ((List.range C.F.n).filter (fun x => C.ctrl x k)).map (fun x => (ctrlForm C k, [x, x])))

theorem mem_ctrlInsts {C : Controlled} {i : Inst} :
    i ∈ ctrlInsts C ↔
      ∃ k, k < C.F.ops.length ∧ ∃ x, x < C.F.n ∧ C.ctrl x k = true ∧
        i = (3 + C.F.ops.length + k, [x, x]) := by
  unfold ctrlInsts
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨k, hk, hi⟩
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hi
    have hx' := List.mem_filter.mp hx
    exact ⟨k, List.mem_range.mp hk, x, List.mem_range.mp hx'.1, hx'.2, rfl⟩
  · rintro ⟨k, hk, x, hx, hc, rfl⟩
    exact ⟨k, List.mem_range.mpr hk,
      List.mem_map.mpr ⟨x, List.mem_filter.mpr ⟨List.mem_range.mpr hx, hc⟩, rfl⟩⟩

/-- The represented program: the operation graphs and the enablements.  The
stores are not part of it. -/
def program (C : Controlled) : List Inst := graphsFrom C.F.n 3 C.F.ops ++ ctrlInsts C

theorem mem_program {C : Controlled} {i : Inst} :
    i ∈ program C ↔
      (∃ k, k < C.F.ops.length ∧ ∃ x, x < C.F.n ∧ i = (3 + k, [x, C.F.ops.getD k id x])) ∨
      (∃ k, k < C.F.ops.length ∧ ∃ x, x < C.F.n ∧ C.ctrl x k = true ∧
        i = (3 + C.F.ops.length + k, [x, x])) := by
  show i ∈ graphsFrom C.F.n 3 C.F.ops ++ ctrlInsts C ↔ _
  rw [List.mem_append, mem_graphsFrom, mem_ctrlInsts]

/-- The controlled regime of the sealed grammar: the stores, the operation
graphs, and the enablements, on `3 + 2 · nops` binary forms. -/
def encodeC (C : Controlled) : Regime :=
  ⟨C.F.n,
   [2, 2, 2] ++ C.F.ops.map (fun _ => 2) ++ C.F.ops.map (fun _ => 2),
   storesFrom C.F.n 0 [C.F.rel, C.F.ret, C.F.prot] ++ program C,
   [],
   []⟩

theorem encodeC_forms_length (C : Controlled) :
    (encodeC C).forms.length = 3 + C.F.ops.length + C.F.ops.length := by
  show ([2, 2, 2] ++ C.F.ops.map (fun _ => 2) ++ C.F.ops.map (fun _ => 2)).length = _
  rw [List.length_append, List.length_append, List.length_map]
  rfl

theorem encodeC_forms_two (C : Controlled) : ∀ a ∈ (encodeC C).forms, a = 2 := by
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

theorem encodeC_forms_getD (C : Controlled) {f : Nat} (hf : f < (encodeC C).forms.length) :
    (encodeC C).forms.getD f 0 = 2 :=
  getD_of_all_two _ (encodeC_forms_two C) f hf

/-- **The represented program is a well-formed regime.** -/
theorem encodeC_wf (C : Controlled) : (encodeC C).wf := by
  have hlen := encodeC_forms_length C
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    rcases List.mem_append.mp hp with hs | hg
    · rcases (mem_storesFrom 0 _).mp hs with ⟨k, hk, x, y, hx, hy, _, rfl⟩
      have hk3 : k < 3 := hk
      refine ⟨?_, ?_, two_args_lt hx hy⟩
      · show 0 + k < (encodeC C).forms.length
        omega
      · show [x, y].length = (encodeC C).forms.getD (0 + k) 0
        rw [encodeC_forms_getD C (by omega)]
        rfl
    · rcases mem_program.mp hg with ⟨k, hk, x, hx, rfl⟩ | ⟨k, hk, x, hx, _, rfl⟩
      · refine ⟨?_, ?_, two_args_lt hx (C.F.ops_closed _ (getD_mem hk) x hx)⟩
        · show 3 + k < (encodeC C).forms.length
          omega
        · show [x, C.F.ops.getD k id x].length = (encodeC C).forms.getD (3 + k) 0
          rw [encodeC_forms_getD C (by omega)]
          rfl
      · refine ⟨?_, ?_, two_args_lt hx hx⟩
        · show 3 + C.F.ops.length + k < (encodeC C).forms.length
          omega
        · show [x, x].length = (encodeC C).forms.getD (3 + C.F.ops.length + k) 0
          rw [encodeC_forms_getD C (by omega)]
          rfl
  · intro f hf
    exact absurd hf List.not_mem_nil
  · intro q hq
    exact absurd hq List.not_mem_nil
  · intro a ha
    rw [encodeC_forms_two C a ha]
    decide

/-! ## 3. Reading the program -/

/-- The operation-`k` edge leaving `x` in the program is the operation's
value: the operation forms of the program are those of the encoding. -/
theorem lookup_program_op (C : Controlled) {k x : Nat} (hk : k < C.F.ops.length)
    (hx : x < C.F.n) : lookup (3 + k) x (program C) = some (C.F.ops.getD k id x) := by
  have hmem : (3 + k, [x, C.F.ops.getD k id x]) ∈ program C :=
    mem_program.mpr (Or.inl ⟨k, hk, x, hx, rfl⟩)
  have hsome := lookup_isSome hmem
  cases hl : lookup (3 + k) x (program C) with
  | none =>
      rw [hl] at hsome
      cases hsome
  | some y =>
      have hy : (3 + k, [x, y]) ∈ program C := lookup_mem hl
      rcases mem_program.mp hy with ⟨k', _, x', _, h⟩ | ⟨k', _, x', _, _, h⟩
      · injection h with h1 h2
        have hkk : k' = k := by omega
        subst hkk
        obtain ⟨rfl, rfl⟩ := list_two_inj h2
        rfl
      · injection h with h1 _
        omega

/-- Operation `k` is enabled at `x` when the self-instance of its control
form is present: the edge of that form leaving `x` returns `x`. -/
def enabled (g : List Inst) (nops x k : Nat) : Bool :=
  decide (lookup (3 + nops + k) x g = some x)

theorem enabled_iff {g : List Inst} {nops x k : Nat} :
    enabled g nops x k = true ↔ lookup (3 + nops + k) x g = some x :=
  decide_eq_true_iff

/-- The enabled operations at `x`, in index order.  A list, so that the
family can be stated; nothing below reads its first element as a choice. -/
def enabledAt (g : List Inst) (nops x : Nat) : List Nat :=
  (List.range nops).filter (fun k => enabled g nops x k)

theorem mem_enabledAt {g : List Inst} {nops x k : Nat} :
    k ∈ enabledAt g nops x ↔ k < nops ∧ enabled g nops x k = true := by
  unfold enabledAt
  rw [List.mem_filter, List.mem_range]

/-- **Enablement is read faithfully** from the program. -/
theorem enabled_program (C : Controlled) {x k : Nat} (hk : k < C.F.ops.length) (hx : x < C.F.n) :
    enabled (program C) C.F.ops.length x k = true ↔ C.ctrl x k = true := by
  rw [enabled_iff]
  constructor
  · intro hl
    have hy : (3 + C.F.ops.length + k, [x, x]) ∈ program C := lookup_mem hl
    rcases mem_program.mp hy with ⟨k', hk', x', _, h'⟩ | ⟨k', _, x', _, hc, h'⟩
    · injection h' with h1 _
      omega
    · injection h' with h1 h2
      have hkk : k' = k := by omega
      subst hkk
      obtain ⟨rfl, _⟩ := list_two_inj h2
      exact hc
  · intro hc
    have hmem : (3 + C.F.ops.length + k, [x, x]) ∈ program C :=
      mem_program.mpr (Or.inr ⟨k, hk, x, hx, hc, rfl⟩)
    have hsome := lookup_isSome hmem
    cases hl : lookup (3 + C.F.ops.length + k) x (program C) with
    | none =>
        rw [hl] at hsome
        cases hsome
    | some y =>
        have hy : (3 + C.F.ops.length + k, [x, y]) ∈ program C := lookup_mem hl
        rcases mem_program.mp hy with ⟨k', hk', x', _, h'⟩ | ⟨k', _, x', _, _, h'⟩
        · injection h' with h1 _
          omega
        · injection h' with _ h2
          obtain ⟨rfl, rfl⟩ := list_two_inj h2
          rfl

/-! ## 4. The state and the interpreter -/

/-- A state: the program, the operation count that locates the control
forms, the active datum, the tape of data visited, the semantic clock, the
represented fuel.  DECLARED_HOST_CONFIG. -/
structure State where
  graph : List Inst
  nops : Nat
  active : Nat
  tape : List Nat
  clock : Nat
  fuel : Nat

/-- The result of firing one operation. -/
inductive Fired
  | ok (s : State)
  | exhausted
  | noEdge

/-- Fire operation `k` at the active datum: with fuel left, read its edge,
move, extend the tape, tick the clock, spend one fuel. -/
def fire (s : State) (k : Nat) : Fired :=
  match s.fuel with
  | 0 => .exhausted
  | f + 1 =>
    match lookup (3 + k) s.active s.graph with
    | none => .noEdge
    | some y => .ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩

/-- The successor family: one state per enabled operation that fires. -/
def successors (s : State) : List State :=
  (enabledAt s.graph s.nops s.active).filterMap (fun k =>
    match fire s k with
    | .ok s' => some s'
    | _ => none)

/-- The terminals, kept apart. -/
inductive Terminal
  | halt
  | exhausted
  | refuse
  | branch
deriving DecidableEq, Repr

/-- One step of the deterministic runner: a terminal, or the next state.
It fires the one enabled operation, halts when none is enabled, and stops
with `branch` when two are — it never selects. -/
def stepDet (s : State) : Terminal ⊕ State :=
  match enabledAt s.graph s.nops s.active with
  | [] => .inl .halt
  | [k] =>
    match fire s k with
    | .ok s' => .inr s'
    | .exhausted => .inl .exhausted
    | .noEdge => .inl .refuse
  | _ :: _ :: _ => .inl .branch

/-- The deterministic runner, bounded by a copy of the fuel. -/
def runDet : Nat → State → Terminal × State
  | 0, s =>
    match stepDet s with
    | .inl t => (t, s)
    | .inr _ => (.exhausted, s)
  | b + 1, s =>
    match stepDet s with
    | .inl t => (t, s)
    | .inr s' => runDet b s'

def run (s : State) : Terminal × State := runDet s.fuel s

/-- The initial state of a controlled setting: its program, a start datum,
the start on the tape, clock zero, a declared fuel. -/
def init (C : Controlled) (x fuel : Nat) : State :=
  ⟨program C, C.F.ops.length, x, [x], 0, fuel⟩

/-! ## 5. Bookkeeping laws -/

/-- Fuel is never renewed: with none, nothing fires. -/
theorem fire_exhausted {s : State} {k : Nat} (h : s.fuel = 0) : fire s k = .exhausted := by
  show (match s.fuel with
        | 0 => Fired.exhausted
        | f + 1 =>
          match lookup (3 + k) s.active s.graph with
          | none => Fired.noEdge
          | some y => Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩) = .exhausted
  rw [h]

/-- With fuel, firing is reading the edge. -/
theorem fire_succ (s : State) (k f : Nat) (hf : s.fuel = f + 1) :
    fire s k = (match lookup (3 + k) s.active s.graph with
                | none => Fired.noEdge
                | some y => Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩) := by
  show (match s.fuel with
        | 0 => Fired.exhausted
        | f' + 1 =>
          match lookup (3 + k) s.active s.graph with
          | none => Fired.noEdge
          | some y => Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f'⟩) = _
  rw [hf]

/-- What one firing does: the edge is read, the datum moves to it, the tape
grows by it, the clock ticks once, one fuel is spent, the program is kept. -/
theorem fire_ok {s s' : State} {k : Nat} (h : fire s k = .ok s') :
    lookup (3 + k) s.active s.graph = some s'.active ∧ s'.tape = s.tape ++ [s'.active] ∧
      s'.clock = s.clock + 1 ∧ s'.fuel + 1 = s.fuel ∧ s'.graph = s.graph ∧ s'.nops = s.nops := by
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := by
    cases hfu : s.fuel with
    | zero =>
        rw [fire_exhausted hfu] at h
        cases h
    | succ f => exact ⟨f, rfl⟩
  rw [fire_succ s k f hf] at h
  cases hl : lookup (3 + k) s.active s.graph with
  | none =>
      rw [hl] at h
      cases h
  | some y =>
      rw [hl] at h
      have h'' : Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ = Fired.ok s' := h
      cases h''
      exact ⟨rfl, rfl, rfl, hf.symm, rfl, rfl⟩

/-- The successor family, by membership: a successor is exactly a firing of
an enabled operation.  No first element is named. -/
theorem mem_successors {s s' : State} :
    s' ∈ successors s ↔ ∃ k, k ∈ enabledAt s.graph s.nops s.active ∧ fire s k = .ok s' := by
  unfold successors
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

/-! ## 6. Simulation and reflection against the reference step -/

/-- **Soundness.**  Every successor of an initial state realises a
reference step: the operation was enabled at the datum, and the new datum
is its value. -/
theorem successors_sound (C : Controlled) {x fuel : Nat} (hx : x < C.F.n) {s' : State}
    (h : s' ∈ successors (init C x fuel)) : ∃ k, CStep C x k s'.active := by
  obtain ⟨k, hk, hf⟩ := mem_successors.mp h
  have hk' : k < C.F.ops.length ∧ enabled (program C) C.F.ops.length x k = true :=
    mem_enabledAt.mp hk
  have hen := (enabled_program C hk'.1 hx).mp hk'.2
  obtain ⟨hl, -, -, -, -, -⟩ := fire_ok hf
  have hl' : lookup (3 + k) x (program C) = some s'.active := hl
  rw [lookup_program_op C hk'.1 hx] at hl'
  exact ⟨k, hk'.1, hen, (Option.some.inj hl').symm⟩

/-- **Completeness.**  Every reference step from an admitted datum, given
fuel, is realised by a successor. -/
theorem successors_complete (C : Controlled) {x k y fuel : Nat} (hx : x < C.F.n)
    (hs : CStep C x k y) :
    ∃ s' ∈ successors (init C x (fuel + 1)), s'.active = y := by
  obtain ⟨hk, hc, rfl⟩ := hs
  have hen : enabled (program C) C.F.ops.length x k = true := (enabled_program C hk hx).mpr hc
  have hmem : k ∈ enabledAt (program C) C.F.ops.length x := mem_enabledAt.mpr ⟨hk, hen⟩
  refine ⟨⟨program C, C.F.ops.length, C.F.ops.getD k id x, [x] ++ [C.F.ops.getD k id x], 0 + 1, fuel⟩,
    mem_successors.mpr ⟨k, hmem, ?_⟩, rfl⟩
  rw [fire_succ (init C x (fuel + 1)) k fuel rfl]
  show (match lookup (3 + k) x (program C) with
        | none => Fired.noEdge
        | some y => Fired.ok ⟨program C, C.F.ops.length, y, [x] ++ [y], 0 + 1, fuel⟩) = _
  rw [lookup_program_op C hk hx]

/-- `init` does not read the designated pair: two controlled settings that
differ only in their endpoints have the same initial state. -/
theorem init_pair (C : Controlled) (x fuel a b : Nat) (ha : a < C.F.n) (hb : b < C.F.n) :
    init ⟨⟨C.F.n, C.F.rel, C.F.ret, C.F.prot, a, b, C.F.ops, ha, hb, C.F.ops_closed⟩, C.ctrl⟩ x fuel =
      init C x fuel := rfl

/-! ## 7. Non-stuckness on the live class, and the runner's terminals -/

/-- The live class: an admitted datum with an enabled operation and fuel. -/
def Live (C : Controlled) (s : State) : Prop :=
  s.graph = program C ∧ s.nops = C.F.ops.length ∧ s.active < C.F.n ∧ 0 < s.fuel ∧
    ∃ k, k ∈ enabledAt s.graph s.nops s.active

/-- **Non-stuckness.**  A live state has a successor. -/
theorem live_successor (C : Controlled) {s : State} (h : Live C s) : ∃ s', s' ∈ successors s := by
  obtain ⟨hg, hn, hx, hfuel, k, hk⟩ := h
  have hk' := mem_enabledAt.mp hk
  rw [hg, hn] at hk'
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := ⟨s.fuel - 1, by omega⟩
  refine ⟨⟨s.graph, s.nops, C.F.ops.getD k id s.active, s.tape ++ [C.F.ops.getD k id s.active],
    s.clock + 1, f⟩, mem_successors.mpr ⟨k, hk, ?_⟩⟩
  rw [fire_succ s k f hf, hg, lookup_program_op C hk'.1 hx]

/-- One step never selects: `branch` only when two operations are enabled. -/
theorem stepDet_branch {s : State} (h : stepDet s = .inl .branch) :
    2 ≤ (enabledAt s.graph s.nops s.active).length := by
  revert h
  show (match enabledAt s.graph s.nops s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.branch →
      2 ≤ (enabledAt s.graph s.nops s.active).length
  cases enabledAt s.graph s.nops s.active with
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

/-- The runner's `branch` is honest: at the state it returns, two operations
are enabled. -/
def BranchOk (p : Terminal × State) : Prop :=
  p.1 = .branch → 2 ≤ (enabledAt p.2.graph p.2.nops p.2.active).length

theorem runDet_branch : ∀ (b : Nat) (s : State), BranchOk (runDet b s)
  | 0, s => by
      show BranchOk (match stepDet s with
                     | .inl t => (t, s)
                     | .inr _ => (Terminal.exhausted, s))
      cases hs : stepDet s with
      | inl t =>
          intro h
          have ht : t = Terminal.branch := h
          subst ht
          exact stepDet_branch hs
      | inr s' =>
          intro h
          cases h
  | b + 1, s => by
      show BranchOk (match stepDet s with
                     | .inl t => (t, s)
                     | .inr s' => runDet b s')
      cases hs : stepDet s with
      | inl t =>
          intro h
          have ht : t = Terminal.branch := h
          subst ht
          exact stepDet_branch hs
      | inr s' => exact runDet_branch b s'

theorem run_branch (s : State) : BranchOk (run s) := runDet_branch s.fuel s

end Control

#print axioms Control.mem_ctrlInsts
#print axioms Control.mem_program
#print axioms Control.encodeC_forms_length
#print axioms Control.encodeC_forms_two
#print axioms Control.encodeC_forms_getD
#print axioms Control.encodeC_wf
#print axioms Control.lookup_program_op
#print axioms Control.enabled_iff
#print axioms Control.mem_enabledAt
#print axioms Control.enabled_program
#print axioms Control.fire_exhausted
#print axioms Control.fire_succ
#print axioms Control.fire_ok
#print axioms Control.mem_successors
#print axioms Control.successors_sound
#print axioms Control.successors_complete
#print axioms Control.init_pair
#print axioms Control.live_successor
#print axioms Control.stepDet_branch
#print axioms Control.runDet_branch
#print axioms Control.run_branch
