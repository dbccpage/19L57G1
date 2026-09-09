import Select

/-!
# Depth: a record read two entries deep

Reading one entry of the record buys functionality in *pairs* and no more
(`Record.robs_functional`): a record-reading run cannot produce a tape in
which the same datum follows the same datum twice and is followed by two
different data.  This module reads two entries and produces exactly such a
tape.

The device changes in one way, and it is the point.  Every form of the merged
encoders is **binary** — an argument of an operation graph or a control form
is a pair of data.  A read of depth two needs three data at once, so its
control forms are **ternary**.  The sealed grammar admits that without any new
admission: `Regime.wf` constrains a form's arity only by `1 ≤ a`, so
`encodeR2` — binary stores, binary operation graphs, ternary control forms —
is a well-formed regime (`encodeR2_wf`).  This is the first family here whose
encoding is not all-binary, and nothing about the grammar had to move.

The enablement of operation `k` at the active datum `x`, after `p`, after `b`,
is the instance `(3 + nops + k, [b, p, x])`.  The interpreter reads it, then
the operation's edge, as before; `fire` is the merged one, unchanged.  The
read is membership (`r2enabled`), because several instances of one control
form may share a prefix — a relation, not a function — exactly as at depth
one.

What it delivers: `twist2` visits `0, 1, 2, 0, 1, 0` from datum 0
(`twist2_tape`).  That tape has the pair `(0, 1)` followed once by `2` and
once by `0`, so **no record-reading program realises it**
(`no_record_run_realises`, through `Record.robs_functional`) — the ceiling of
a depth-one read, broken.  The memoryless and depth-one classes both embed
(`lift2`), so the extension is conservative.

AuthorityEffect: None.
-/

namespace Depth

open Derivation Translation Execution Control Record

/-! ## 1. Mixed arity: the forms of a depth-two regime -/

/-- Three binary stores, one binary form per operation graph, and one
**ternary** form per operation for the depth-two enablement. -/
def formsOf (nops : Nat) : List Nat :=
  List.replicate (3 + nops) 2 ++ List.replicate nops 3

theorem formsOf_length (nops : Nat) : (formsOf nops).length = 3 + nops + nops := by
  show ((List.replicate (3 + nops) 2 ++ List.replicate nops 3)).length = _
  rw [List.length_append, List.length_replicate, List.length_replicate]

theorem formsOf_getD_binary {nops f : Nat} (h : f < 3 + nops) : (formsOf nops).getD f 0 = 2 := by
  show ((List.replicate (3 + nops) 2 ++ List.replicate nops 3)).getD f 0 = 2
  rw [List.getD_eq_getElem?_getD,
    List.getElem?_append_left (by rw [List.length_replicate]; exact h),
    List.getElem?_replicate_of_lt h]
  rfl

theorem formsOf_getD_ternary {nops k : Nat} (h : k < nops) :
    (formsOf nops).getD (3 + nops + k) 0 = 3 := by
  show ((List.replicate (3 + nops) 2 ++ List.replicate nops 3)).getD (3 + nops + k) 0 = 3
  rw [List.getD_eq_getElem?_getD,
    List.getElem?_append_right (by rw [List.length_replicate]; omega),
    List.length_replicate,
    show 3 + nops + k - (3 + nops) = k from by omega,
    List.getElem?_replicate_of_lt h]
  rfl

theorem formsOf_pos {nops : Nat} : ∀ a ∈ formsOf nops, 1 ≤ a := by
  intro a ha
  rcases List.mem_append.mp ha with h | h
  · rw [(List.mem_replicate.mp h).2]
    decide
  · rw [(List.mem_replicate.mp h).2]
    decide

/-! ## 2. Recorded settings of depth two, and their reference semantics -/

/-- A finite setting with an enablement that reads two entries of the record:
`hctrl2 b p x k` says operation `k` may fire at the active datum `x` when the
datum before it is `p` and the one before that is `b`. -/
structure Recorded2 where
  F : FiniteSetting
  hctrl2 : Nat → Nat → Nat → Nat → Bool

/-- **The reference step**, on the setting before any encoding. -/
def R2Step (C : Recorded2) (b p x k y : Nat) : Prop :=
  k < C.F.ops.length ∧ C.hctrl2 b p x k = true ∧ y = C.F.ops.getD k id x

/-- All ordered triples over the carrier. -/
def carrierTriples (n : Nat) : List (Nat × Nat × Nat) :=
  (List.range n).flatMap (fun b =>
    (List.range n).flatMap (fun p => (List.range n).map (fun x => (b, p, x))))

theorem mem_carrierTriples {n : Nat} {t : Nat × Nat × Nat} :
    t ∈ carrierTriples n ↔ t.1 < n ∧ t.2.1 < n ∧ t.2.2 < n := by
  unfold carrierTriples
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨b, hb, h⟩
    rw [List.mem_flatMap] at h
    obtain ⟨p, hp, h⟩ := h
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp h
    exact ⟨List.mem_range.mp hb, List.mem_range.mp hp, List.mem_range.mp hx⟩
  · rintro ⟨hb, hp, hx⟩
    refine ⟨t.1, List.mem_range.mpr hb, ?_⟩
    rw [List.mem_flatMap]
    exact ⟨t.2.1, List.mem_range.mpr hp,
      List.mem_map.mpr ⟨t.2.2, List.mem_range.mpr hx, rfl⟩⟩

/-- The depth-two enablement instances: on the ternary control form of
operation `k`, the triple at which `k` is enabled. -/
def rec2Insts (C : Recorded2) : List Inst :=
  (List.range C.F.ops.length).flatMap (fun k =>
    ((carrierTriples C.F.n).filter (fun t => C.hctrl2 t.1 t.2.1 t.2.2 k)).map
      (fun t => (3 + C.F.ops.length + k, [t.1, t.2.1, t.2.2])))

theorem mem_rec2Insts {C : Recorded2} {i : Inst} :
    i ∈ rec2Insts C ↔
      ∃ k, k < C.F.ops.length ∧ ∃ b p x, b < C.F.n ∧ p < C.F.n ∧ x < C.F.n ∧
        C.hctrl2 b p x k = true ∧ i = (3 + C.F.ops.length + k, [b, p, x]) := by
  unfold rec2Insts
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨k, hk, hi⟩
    obtain ⟨t, ht, rfl⟩ := List.mem_map.mp hi
    have ht' := List.mem_filter.mp ht
    have hb := mem_carrierTriples.mp ht'.1
    exact ⟨k, List.mem_range.mp hk, t.1, t.2.1, t.2.2, hb.1, hb.2.1, hb.2.2, ht'.2, rfl⟩
  · rintro ⟨k, hk, b, p, x, hb, hp, hx, hc, rfl⟩
    exact ⟨k, List.mem_range.mpr hk,
      List.mem_map.mpr ⟨(b, p, x),
        List.mem_filter.mpr ⟨mem_carrierTriples.mpr ⟨hb, hp, hx⟩, hc⟩, rfl⟩⟩

/-- The represented program: the operation graphs and the depth-two
enablements.  The stores are not part of it. -/
def r2program (C : Recorded2) : List Inst := graphsFrom C.F.n 3 C.F.ops ++ rec2Insts C

theorem mem_r2program {C : Recorded2} {i : Inst} :
    i ∈ r2program C ↔
      (∃ k, k < C.F.ops.length ∧ ∃ x, x < C.F.n ∧ i = (3 + k, [x, C.F.ops.getD k id x])) ∨
      (∃ k, k < C.F.ops.length ∧ ∃ b p x, b < C.F.n ∧ p < C.F.n ∧ x < C.F.n ∧
        C.hctrl2 b p x k = true ∧ i = (3 + C.F.ops.length + k, [b, p, x])) := by
  show i ∈ graphsFrom C.F.n 3 C.F.ops ++ rec2Insts C ↔ _
  rw [List.mem_append, mem_graphsFrom, mem_rec2Insts]

/-- The depth-two regime: binary stores, binary operation graphs, **ternary**
control forms. -/
def encodeR2 (C : Recorded2) : Regime :=
  ⟨C.F.n,
   formsOf C.F.ops.length,
   storesFrom C.F.n 0 [C.F.rel, C.F.ret, C.F.prot] ++ r2program C,
   [],
   []⟩

/-- **A regime of mixed arity is still a regime.**  The sealed grammar asks
only that every form have arity at least one, so the ternary control forms are
admitted with no new admission. -/
theorem encodeR2_wf (C : Recorded2) : (encodeR2 C).wf := by
  have hlen : (encodeR2 C).forms.length = 3 + C.F.ops.length + C.F.ops.length :=
    formsOf_length _
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro q hq
    rcases List.mem_append.mp hq with hs | hg
    · rcases (mem_storesFrom 0 _).mp hs with ⟨k, hk, x, y, hx, hy, _, rfl⟩
      have hk3 : k < 3 := hk
      refine ⟨by omega, ?_, two_args_lt hx hy⟩
      show [x, y].length = (encodeR2 C).forms.getD (0 + k) 0
      show [x, y].length = (formsOf C.F.ops.length).getD (0 + k) 0
      rw [formsOf_getD_binary (by omega)]
      rfl
    · rcases mem_r2program.mp hg with ⟨k, hk, x, hx, rfl⟩ | ⟨k, hk, b, p, x, hb, hp, hx, -, rfl⟩
      · refine ⟨by omega, ?_, two_args_lt hx (C.F.ops_closed _ (getD_mem hk) x hx)⟩
        show [x, C.F.ops.getD k id x].length = (formsOf C.F.ops.length).getD (3 + k) 0
        rw [formsOf_getD_binary (by omega)]
        rfl
      · refine ⟨by omega, ?_, ?_⟩
        · show [b, p, x].length =
            (formsOf C.F.ops.length).getD (3 + C.F.ops.length + k) 0
          rw [formsOf_getD_ternary hk]
          rfl
        · intro a ha
          rcases List.mem_cons.mp ha with rfl | ha
          · exact hb
          rcases List.mem_cons.mp ha with rfl | ha
          · exact hp
          rcases List.mem_cons.mp ha with rfl | ha
          · exact hx
          exact absurd ha List.not_mem_nil
  · intro f hf
    exact absurd hf List.not_mem_nil
  · intro q hq
    exact absurd hq List.not_mem_nil
  · exact formsOf_pos

/-! ## 3. Reading the depth-two program -/

/-- Operation `k` is enabled at `x` after `p` after `b` when the instance is
present.  Membership, not a lookup: several instances of one control form
share a prefix, so the read is a relation. -/
def r2enabled (g : List Inst) (nops b p x k : Nat) : Bool :=
  decide ((3 + nops + k, [b, p, x]) ∈ g)

theorem r2enabled_iff {g : List Inst} {nops b p x k : Nat} :
    r2enabled g nops b p x k = true ↔ (3 + nops + k, [b, p, x]) ∈ g := decide_eq_true_iff

/-- **The enablement is read faithfully** from the program. -/
theorem r2enabled_r2program (C : Recorded2) {b p x k : Nat} (hk : k < C.F.ops.length)
    (hb : b < C.F.n) (hp : p < C.F.n) (hx : x < C.F.n) :
    r2enabled (r2program C) C.F.ops.length b p x k = true ↔ C.hctrl2 b p x k = true := by
  rw [r2enabled_iff, mem_r2program]
  constructor
  · rintro (⟨k', hk', x', -, h⟩ | ⟨k', -, b', p', x', -, -, -, hc, h⟩)
    · injection h with h1 h2
      omega
    · injection h with h1 h2
      have hkk : k' = k := by omega
      subst hkk
      obtain ⟨rfl, rfl, rfl⟩ : b = b' ∧ p = p' ∧ x = x' := by
        injection h2 with e1 h2
        injection h2 with e2 h2
        injection h2 with e3 _
        exact ⟨e1, e2, e3⟩
      exact hc
  · intro hc
    exact Or.inr ⟨k, hk, b, p, x, hb, hp, hx, hc, rfl⟩

def r2enabledAt (g : List Inst) (nops b p x : Nat) : List Nat :=
  (List.range nops).filter (fun k => r2enabled g nops b p x k)

theorem mem_r2enabledAt {g : List Inst} {nops b p x k : Nat} :
    k ∈ r2enabledAt g nops b p x ↔ k < nops ∧ r2enabled g nops b p x k = true := by
  unfold r2enabledAt
  rw [List.mem_filter, List.mem_range]

/-- The datum two before the last on the record; a record too short for it
falls back to the one before the last, as that falls back to the active
datum. -/
def before (s : State) : Nat :=
  match s.tape.reverse with
  | _ :: _ :: b :: _ => b
  | _ => previous s

/-- The operation-`k` edge leaving `x` in the depth-two program is the
operation's value: the enablement instances live on later forms. -/
theorem lookup_r2program_op (C : Recorded2) {k x : Nat} (hk : k < C.F.ops.length)
    (hx : x < C.F.n) : lookup (3 + k) x (r2program C) = some (C.F.ops.getD k id x) := by
  have hmem : (3 + k, [x, C.F.ops.getD k id x]) ∈ r2program C :=
    mem_r2program.mpr (Or.inl ⟨k, hk, x, hx, rfl⟩)
  have hsome := lookup_isSome hmem
  cases hl : lookup (3 + k) x (r2program C) with
  | none =>
      rw [hl] at hsome
      cases hsome
  | some y =>
      have hy : (3 + k, [x, y]) ∈ r2program C := lookup_mem hl
      rcases mem_r2program.mp hy with ⟨k', -, x', -, h⟩ | ⟨k', -, b', p', x', -, -, -, -, h⟩
      · injection h with h1 h2
        have hkk : k' = k := by omega
        subst hkk
        obtain ⟨rfl, rfl⟩ := list_two_inj h2
        rfl
      · injection h with h1 _
        omega

/-! ## 4. The interpreter -/

def r2stepDet (s : State) : Terminal ⊕ State :=
  match r2enabledAt s.graph s.nops (before s) (previous s) s.active with
  | [] => .inl .halt
  | [k] =>
    match fire s k with
    | .ok s' => .inr s'
    | .exhausted => .inl .exhausted
    | .noEdge => .inl .refuse
  | _ :: _ :: _ => .inl .branch

def r2next (s : State) : State :=
  match r2stepDet s with
  | .inr s' => s'
  | .inl _ => s

def r2iter : Nat → State → State
  | 0, s => s
  | n + 1, s => r2next (r2iter n s)

def r2obs (n : Nat) (s : State) : List Nat := (r2iter n s).tape

def r2init (C : Recorded2) (x fuel : Nat) : State :=
  ⟨r2program C, C.F.ops.length, x, [x], 0, fuel⟩

/-- The successor family: one state per enabled operation that fires. -/
def r2successors (s : State) : List State :=
  (r2enabledAt s.graph s.nops (before s) (previous s) s.active).filterMap (fun k =>
    match fire s k with
    | .ok s' => some s'
    | _ => none)

theorem mem_r2successors {s s' : State} :
    s' ∈ r2successors s ↔
      ∃ k, k ∈ r2enabledAt s.graph s.nops (before s) (previous s) s.active ∧
        fire s k = .ok s' := by
  unfold r2successors
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

/-- **Soundness.**  Every successor of a state carrying the program realises a
reference step at the two recorded data and the active one. -/
theorem r2successors_sound (C : Recorded2) {s s' : State} (hg : s.graph = r2program C)
    (hn : s.nops = C.F.ops.length) (hb : before s < C.F.n) (hp : previous s < C.F.n)
    (hx : s.active < C.F.n) (h : s' ∈ r2successors s) :
    ∃ k, R2Step C (before s) (previous s) s.active k s'.active := by
  obtain ⟨k, hk, hf⟩ := mem_r2successors.mp h
  have hk' := mem_r2enabledAt.mp hk
  rw [hg, hn] at hk'
  have hen := (r2enabled_r2program C hk'.1 hb hp hx).mp hk'.2
  obtain ⟨hl, -, -, -, -, -⟩ := fire_ok hf
  rw [hg, lookup_r2program_op C hk'.1 hx] at hl
  exact ⟨k, hk'.1, hen, (Option.some.inj hl).symm⟩

/-! ## 5. The memoryless and depth-one classes embed -/

/-- A depth-one recorded setting read as a depth-two one: the enablement
ignores the older entry. -/
def lift2 (C : Recorded) : Recorded2 := ⟨C.F, fun _ p x k => C.hctrl p x k⟩

theorem lift2_R2Step (C : Recorded) (b p x k y : Nat) :
    R2Step (lift2 C) b p x k y ↔ RStep C p x k y := Iff.rfl

/-! ## 6. The ceiling of a depth-one read, broken -/

/-- The cycle after `(0, 0)` at 0 and at 1, after `(0, 1)` at 2, after
`(1, 2)` at 0; the constant map after `(2, 0)` at 1.  Five keys, all
distinct. -/
def twist2 : Recorded2 :=
  ⟨Observe.base, fun b p x k =>
    decide ((b = 0 ∧ p = 0 ∧ x = 0 ∧ k = 0) ∨ (b = 0 ∧ p = 0 ∧ x = 1 ∧ k = 0) ∨
      (b = 0 ∧ p = 1 ∧ x = 2 ∧ k = 0) ∨ (b = 1 ∧ p = 2 ∧ x = 0 ∧ k = 0) ∨
      (b = 2 ∧ p = 0 ∧ x = 1 ∧ k = 1))⟩

/-- From datum 0 the run visits `0, 1, 2, 0, 1, 0`. -/
theorem twist2_tape : r2obs 5 (r2init twist2 0 5) = [0, 1, 2, 0, 1, 0] := by decide

/-- That tape carries the pair `(0, 1)` twice, followed once by `2` and once
by `0`. -/
theorem twist2_repeats_a_pair :
    (0, 1, 2) ∈ Record.triplesOf [0, 1, 2, 0, 1, 0] ∧
      (0, 1, 0) ∈ Record.triplesOf [0, 1, 2, 0, 1, 0] := by decide

/-- **No record-reading program realises that tape.**  A depth-one read is
functional in its pairs (`Record.robs_functional`), and this tape is not. -/
theorem no_record_run_realises (C : Recorded) (x fuel n : Nat)
    (h : Record.robs n (Record.rinit C x fuel) = [0, 1, 2, 0, 1, 0]) : False := by
  have h1 : ((0, 1, 2) : Nat × Nat × Nat) ∈
      Record.triplesOf (Record.robs n (Record.rinit C x fuel)) := by
    rw [h]
    exact twist2_repeats_a_pair.1
  have h2 : ((0, 1, 0) : Nat × Nat × Nat) ∈
      Record.triplesOf (Record.robs n (Record.rinit C x fuel)) := by
    rw [h]
    exact twist2_repeats_a_pair.2
  have hf := Record.robs_functional C x fuel n h1 h2 rfl rfl
  exact absurd hf (by decide)

/-- **The depth-two read is strictly deeper.**  A depth-two program realises a
tape that no depth-one program realises. -/
theorem depth_two_is_deeper :
    r2obs 5 (r2init twist2 0 5) = [0, 1, 2, 0, 1, 0] ∧
      ∀ (C : Recorded) (x fuel n : Nat),
        Record.robs n (Record.rinit C x fuel) ≠ [0, 1, 2, 0, 1, 0] :=
  ⟨twist2_tape, fun C x fuel n h => no_record_run_realises C x fuel n h⟩

end Depth

#print axioms Depth.formsOf_length
#print axioms Depth.formsOf_getD_binary
#print axioms Depth.formsOf_getD_ternary
#print axioms Depth.formsOf_pos
#print axioms Depth.mem_carrierTriples
#print axioms Depth.mem_rec2Insts
#print axioms Depth.mem_r2program
#print axioms Depth.encodeR2_wf
#print axioms Depth.lookup_r2program_op
#print axioms Depth.r2enabled_iff
#print axioms Depth.r2enabled_r2program
#print axioms Depth.mem_r2enabledAt
#print axioms Depth.mem_r2successors
#print axioms Depth.r2successors_sound
#print axioms Depth.lift2_R2Step
#print axioms Depth.twist2_tape
#print axioms Depth.twist2_repeats_a_pair
#print axioms Depth.no_record_run_realises
#print axioms Depth.depth_two_is_deeper
