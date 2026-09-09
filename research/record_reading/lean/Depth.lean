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

/-! ## 7. The ceiling of a depth-two read, and the ladder

Reading one entry buys functionality in pairs and no more; the ceiling of a
depth-two read should be functionality in *triples*, and this proves it.  The
argument is the depth-one one with one more coordinate: the tape of a
depth-two run is a chain of the machine's next value, and a chain of a
three-argument function is functional in its triples.

Two rungs of a ladder are then in hand, with their ceilings and their
exhibits, and the ladder is a chain: a tape functional in `d` entries is
functional in `d + 1`, so the classes only grow, and the exhibits show that
each of the two inclusions proved here is strict. -/

/-- The value the depth-two runner moves to at the active datum after the two
recorded ones: the value of the one operation enabled there, and none when
none, two, or no edge.  The fuel is not read: this is what the *program* says
about the triple. -/
def r2nextOf (g : List Inst) (nops b p x : Nat) : Option Nat :=
  match r2enabledAt g nops b p x with
  | [k] => lookup (3 + k) x g
  | _ => none

/-- **One step of the depth-two runner, by its next value.** -/
theorem r2stepDet_spec (s : State) :
    ((s.fuel = 0 ∨ r2nextOf s.graph s.nops (before s) (previous s) s.active = none) ∧
        ∃ t, r2stepDet s = .inl t) ∨
      ∃ f y, s.fuel = f + 1 ∧ r2nextOf s.graph s.nops (before s) (previous s) s.active = some y ∧
        r2stepDet s = .inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ := by
  have hstep : r2stepDet s =
      (match r2enabledAt s.graph s.nops (before s) (previous s) s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) := rfl
  have hval : r2nextOf s.graph s.nops (before s) (previous s) s.active =
      (match r2enabledAt s.graph s.nops (before s) (previous s) s.active with
        | [k] => lookup (3 + k) s.active s.graph
        | _ => none) := rfl
  rw [hstep, hval]
  cases r2enabledAt s.graph s.nops (before s) (previous s) s.active with
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

theorem r2next_of_inl {s : State} {t : Terminal} (h : r2stepDet s = .inl t) : r2next s = s := by
  show (match r2stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

theorem r2next_of_inr {s s' : State} (h : r2stepDet s = .inr s') : r2next s = s' := by
  show (match r2stepDet s with | .inr s' => s' | .inl _ => s) = s'
  rw [h]

/-- The consecutive quadruples of a list: three entries and the one after them. -/
def quadsOf : List Nat → List (Nat × Nat × Nat × Nat)
  | w :: x :: y :: z :: rest => (w, x, y, z) :: quadsOf (x :: y :: z :: rest)
  | _ => []

/-- The last three entries of a list, in order. -/
def lastThree : List Nat → Option (Nat × Nat × Nat)
  | [] => none
  | [_] => none
  | [_, _] => none
  | [a, b, c] => some (a, b, c)
  | _ :: x :: y :: z :: rest => lastThree (x :: y :: z :: rest)

theorem lastThree_reverse : ∀ (l : List Nat) {b p x : Nat}, lastThree l = some (b, p, x) →
    ∃ r, l.reverse = x :: p :: b :: r
  | [], _, _, _, h => by cases h
  | [_], _, _, _, h => by cases h
  | [_, _], _, _, _, h => by cases h
  | [a, b, c], p, q, r, h => by
      have h' : (a, b, c) = (p, q, r) := Option.some.inj h
      injection h' with h1 h2
      injection h2 with h2 h3
      subst h1
      subst h2
      subst h3
      exact ⟨[], rfl⟩
  | a :: x :: y :: z :: rest, b, p, q, h => by
      obtain ⟨r, hr⟩ := lastThree_reverse (x :: y :: z :: rest) h
      refine ⟨r ++ [a], ?_⟩
      rw [List.reverse_cons, hr]
      rfl

theorem lastThree_ne_none : ∀ (a b c : Nat) (l : List Nat), lastThree (a :: b :: c :: l) ≠ none
  | _, _, _, [], h => by cases h
  | _, b, c, d :: rest, h => lastThree_ne_none b c d rest h

theorem quadsOf_snoc_none : ∀ (l : List Nat) (y : Nat), lastThree l = none →
    quadsOf (l ++ [y]) = quadsOf l
  | [], _, _ => rfl
  | [_], _, _ => rfl
  | [_, _], _, _ => rfl
  | _ :: _ :: _ :: _, _, h => absurd h (lastThree_ne_none _ _ _ _)

theorem quadsOf_snoc : ∀ (l : List Nat) {b p x : Nat} (y : Nat), lastThree l = some (b, p, x) →
    quadsOf (l ++ [y]) = quadsOf l ++ [(b, p, x, y)]
  | [], _, _, _, _, h => by cases h
  | [_], _, _, _, _, h => by cases h
  | [_, _], _, _, _, _, h => by cases h
  | [a, b, c], p, q, r, y, h => by
      have h' : (a, b, c) = (p, q, r) := Option.some.inj h
      injection h' with h1 h2
      injection h2 with h2 h3
      subst h1
      subst h2
      subst h3
      rfl
  | a :: b :: c :: d :: rest, p, q, r, y, h => by
      have h2 : lastThree (b :: c :: d :: rest) = some (p, q, r) := h
      show (a, b, c, d) :: quadsOf (b :: c :: d :: (rest ++ [y])) = _
      rw [show (b :: c :: d :: (rest ++ [y]) : List Nat) = (b :: c :: d :: rest) ++ [y] from rfl,
        quadsOf_snoc (b :: c :: d :: rest) y h2]
      rfl

/-- A tape is a chain of the depth-two machine when each entry is the next
value of the three before it. -/
def R2Chain (g : List Inst) (nops : Nat) (l : List Nat) : Prop :=
  ∀ q ∈ quadsOf l, r2nextOf g nops q.1 q.2.1 q.2.2.1 = some q.2.2.2

/-- **A depth-two chain is functional in its triples.** -/
theorem r2chain_functional {g : List Inst} {nops : Nat} {l : List Nat} (h : R2Chain g nops l)
    {q r : Nat × Nat × Nat × Nat} (hq : q ∈ quadsOf l) (hr : r ∈ quadsOf l)
    (h1 : q.1 = r.1) (h2 : q.2.1 = r.2.1) (h3 : q.2.2.1 = r.2.2.1) : q.2.2.2 = r.2.2.2 := by
  have hv := h q hq
  have hw := h r hr
  rw [h1, h2, h3] at hv
  exact Option.some.inj (hv.symm.trans hw)

theorem before_of_reverse {s : State} {b p x : Nat} {r : List Nat}
    (h : s.tape.reverse = x :: p :: b :: r) : before s = b := by
  show (match s.tape.reverse with | _ :: _ :: b :: _ => b | _ => previous s) = b
  rw [h]

/-- A step keeps the tape a depth-two chain and keeps the last entry active. -/
theorem r2next_chain {s : State} (hc : R2Chain s.graph s.nops s.tape)
    (hl : s.tape.getLast? = some s.active) :
    R2Chain (r2next s).graph (r2next s).nops (r2next s).tape ∧
      (r2next s).tape.getLast? = some (r2next s).active := by
  rcases r2stepDet_spec s with ⟨-, t, hs⟩ | ⟨f, y, -, hv, hs⟩
  · rw [r2next_of_inl hs]
    exact ⟨hc, hl⟩
  · rw [r2next_of_inr hs]
    refine ⟨?_, getLast?_snoc _ _⟩
    intro u hu
    cases h3 : lastThree s.tape with
    | none =>
        rw [quadsOf_snoc_none s.tape y h3] at hu
        exact hc u hu
    | some q =>
        obtain ⟨r, hr⟩ := lastThree_reverse s.tape (by rw [h3])
        have hb : q.1 = before s := (before_of_reverse hr).symm
        have hp : q.2.1 = previous s := (previous_of_reverse hr).symm
        have hx : q.2.2 = s.active := by
          have hh : s.tape.reverse.head? = s.tape.getLast? := by simp
          rw [hr] at hh
          exact Option.some.inj (hh.trans hl)
        rw [show q = (q.1, q.2.1, q.2.2) from rfl] at h3
        rw [quadsOf_snoc s.tape y h3, List.mem_append] at hu
        rcases hu with h | h
        · exact hc u h
        · rw [List.mem_singleton.mp h, hb, hp, hx]
          exact hv

theorem r2iter_succ : ∀ (n : Nat) (s : State), r2iter (n + 1) s = r2iter n (r2next s)
  | 0, _ => rfl
  | n + 1, s => by
      show r2next (r2iter (n + 1) s) = r2next (r2iter n (r2next s))
      rw [r2iter_succ n s]

theorem r2iter_chain : ∀ (n : Nat) (s : State), R2Chain s.graph s.nops s.tape →
    s.tape.getLast? = some s.active →
    R2Chain (r2iter n s).graph (r2iter n s).nops (r2iter n s).tape ∧
      (r2iter n s).tape.getLast? = some (r2iter n s).active
  | 0, _, hc, hl => ⟨hc, hl⟩
  | n + 1, s, hc, hl => by
      rw [r2iter_succ]
      obtain ⟨hc', hl'⟩ := r2next_chain hc hl
      exact r2iter_chain n (r2next s) hc' hl'

theorem r2init_chain (C : Recorded2) (x fuel : Nat) :
    R2Chain (r2init C x fuel).graph (r2init C x fuel).nops (r2init C x fuel).tape ∧
      (r2init C x fuel).tape.getLast? = some (r2init C x fuel).active :=
  ⟨fun _ hu => absurd hu List.not_mem_nil, rfl⟩

/-- **The ceiling of a depth-two read.**  Every tape a depth-two run realises
is functional in its triples: three entries determine the fourth.  A tape that
breaks this is realised by no depth-two program at all — which is the exact
statement `Record.robs_functional` makes one rung below. -/
theorem r2obs_functional (C : Recorded2) (x fuel n : Nat) {q r : Nat × Nat × Nat × Nat}
    (hq : q ∈ quadsOf (r2obs n (r2init C x fuel)))
    (hr : r ∈ quadsOf (r2obs n (r2init C x fuel)))
    (h1 : q.1 = r.1) (h2 : q.2.1 = r.2.1) (h3 : q.2.2.1 = r.2.2.1) : q.2.2.2 = r.2.2.2 :=
  r2chain_functional
    (r2iter_chain n _ (r2init_chain C x fuel).1 (r2init_chain C x fuel).2).1 hq hr h1 h2 h3

/-! ## 8. The ladder is a chain, and both proved rungs are strict -/

/-- The last two entries of a window of three are a window of two. -/
theorem pairsOf_of_triplesOf : ∀ (l : List Nat) {t : Nat × Nat × Nat},
    t ∈ Record.triplesOf l → (t.2.1, t.2.2) ∈ Observe.pairsOf l
  | [], _, h => absurd h List.not_mem_nil
  | [_], _, h => absurd h List.not_mem_nil
  | [_, _], _, h => absurd h List.not_mem_nil
  | x :: y :: z :: rest, t, h => by
      have h' : t ∈ (x, y, z) :: Record.triplesOf (y :: z :: rest) := h
      rcases List.mem_cons.mp h' with rfl | h''
      · exact List.Mem.tail _ (List.Mem.head _)
      · exact List.Mem.tail _ (pairsOf_of_triplesOf (y :: z :: rest) h'')

/-- The last three entries of a window of four are a window of three. -/
theorem triplesOf_of_quadsOf : ∀ (l : List Nat) {q : Nat × Nat × Nat × Nat},
    q ∈ quadsOf l → (q.2.1, q.2.2.1, q.2.2.2) ∈ Record.triplesOf l
  | [], _, h => absurd h List.not_mem_nil
  | [_], _, h => absurd h List.not_mem_nil
  | [_, _], _, h => absurd h List.not_mem_nil
  | [_, _, _], _, h => absurd h List.not_mem_nil
  | w :: x :: y :: z :: rest, q, h => by
      have h' : q ∈ (w, x, y, z) :: quadsOf (x :: y :: z :: rest) := h
      rcases List.mem_cons.mp h' with rfl | h''
      · exact List.Mem.tail _ (List.Mem.head _)
      · exact List.Mem.tail _ (triplesOf_of_quadsOf (x :: y :: z :: rest) h'')

/-- **The ladder only grows, first step.**  A tape functional in its single
entries is functional in its pairs. -/
theorem triples_of_pairs {l : List Nat}
    (h : ∀ p ∈ Observe.pairsOf l, ∀ q ∈ Observe.pairsOf l, p.1 = q.1 → p.2 = q.2)
    {t u : Nat × Nat × Nat} (ht : t ∈ Record.triplesOf l) (hu : u ∈ Record.triplesOf l)
    (h2 : t.2.1 = u.2.1) : t.2.2 = u.2.2 :=
  h _ (pairsOf_of_triplesOf l ht) _ (pairsOf_of_triplesOf l hu) h2

/-- **The ladder only grows, second step.**  A tape functional in its pairs is
functional in its triples. -/
theorem quads_of_triples {l : List Nat}
    (h : ∀ t ∈ Record.triplesOf l, ∀ u ∈ Record.triplesOf l,
      t.1 = u.1 → t.2.1 = u.2.1 → t.2.2 = u.2.2)
    {q r : Nat × Nat × Nat × Nat} (hq : q ∈ quadsOf l) (hr : r ∈ quadsOf l)
    (h2 : q.2.1 = r.2.1) (h3 : q.2.2.1 = r.2.2.1) : q.2.2.2 = r.2.2.2 :=
  h _ (triplesOf_of_quadsOf l hq) _ (triplesOf_of_quadsOf l hr) h2 h3

/-- The depth-one exhibit repeats a single entry with two different
successors, so it is not functional in its entries. -/
theorem twist_repeats_an_entry :
    ((0, 1) ∈ Observe.pairsOf [0, 1, 0, 0]) ∧ ((0, 0) ∈ Observe.pairsOf [0, 1, 0, 0]) := by decide

/-- **The two proved rungs, and both inclusions strict.**  A memoryless run's
tape is functional in its entries; the depth-one exhibit is not, and is
functional in its pairs.  A depth-one run's tape is functional in its pairs;
the depth-two exhibit is not, and is functional in its triples.  The ceilings
are `Observe.obs_functional`, `Record.robs_functional` and `r2obs_functional`;
the exhibits are `Record.twist_tape` and `twist2_tape`. -/
theorem the_ladder :
    (Record.robs 3 (Record.rinit Record.twist 0 3) = [0, 1, 0, 0] ∧
      ((0, 1) ∈ Observe.pairsOf [0, 1, 0, 0] ∧ (0, 0) ∈ Observe.pairsOf [0, 1, 0, 0])) ∧
    (r2obs 5 (r2init twist2 0 5) = [0, 1, 2, 0, 1, 0] ∧
      ((0, 1, 2) ∈ Record.triplesOf [0, 1, 2, 0, 1, 0] ∧
        (0, 1, 0) ∈ Record.triplesOf [0, 1, 2, 0, 1, 0])) :=
  ⟨⟨Record.twist_tape, twist_repeats_an_entry⟩, ⟨twist2_tape, twist2_repeats_a_pair⟩⟩


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
#print axioms Depth.r2stepDet_spec
#print axioms Depth.r2next_of_inl
#print axioms Depth.r2next_of_inr
#print axioms Depth.lastThree_reverse
#print axioms Depth.lastThree_ne_none
#print axioms Depth.quadsOf_snoc_none
#print axioms Depth.quadsOf_snoc
#print axioms Depth.r2chain_functional
#print axioms Depth.before_of_reverse
#print axioms Depth.r2next_chain
#print axioms Depth.r2iter_succ
#print axioms Depth.r2iter_chain
#print axioms Depth.r2init_chain
#print axioms Depth.r2obs_functional
#print axioms Depth.pairsOf_of_triplesOf
#print axioms Depth.triplesOf_of_quadsOf
#print axioms Depth.triples_of_pairs
#print axioms Depth.quads_of_triples
#print axioms Depth.twist_repeats_an_entry
#print axioms Depth.the_ladder
