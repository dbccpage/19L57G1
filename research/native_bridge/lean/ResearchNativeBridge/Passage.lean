import Derivation.TraceAlgebra
import ResearchNativeBridge.Path

/-!
# Native passage paths

AuthorityEffect: None.  The sealed passage dynamics
`PrimitivePassage.step` is consumed read-only.  A native path is a
`Path step`: every constructor is indexed by the state the sealed step
computes.

Proved here:

* `run_step`: the generic replay is the sealed `replayP`.
* `records`, `records_aligned`, `eraseTrace_records`,
  `endState_records`, `records_legal`: every native path yields an
  aligned typed trace of the sealed trace algebra, with the same events
  and end state; it is legal when each step is accepted from a state of
  the sealed well-formed class.
* `ofAligned`, `events_ofAligned`, `replay_erases_via_paths`,
  `records_ofAligned`: every aligned typed trace is a native path, and
  every legal one is recovered exactly by `records`.
* `refusals_mono`, `halted_path`: refusal records persist along a path,
  and a path from a halted state ends where it started.
* `step_keep_or_grow`, `passage_cycle_core`,
  `passage_cycle_budget_license`: every step either keeps the fields
  other than budget and license, or strictly grows a size measure.  So a
  state on a cycle through `s` differs from `s` at most in its budget and
  license.
* `budget_cycle`, `license_cycle`: both of those fields do carry
  nontrivial cycles.
-/

namespace ResearchNativeBridge

open PrimitivePassage TraceAlgebra TransitionAlphabet

/-- Paths of the sealed passage dynamics. -/
abbrev NPath := Path step

theorem run_step (l : List PEvent) (s : PState) : run step l s = replayP l s := rfl

/-! ## Typed records -/

/-- The record the sealed dynamics computes for one step. -/
def recordOf (s : PState) (e : PEvent) : TRecord :=
  ⟨s, e, guardOf e, step s e, classOf s e, budgetDeltaOf s (step s e),
    profileOf s e⟩

def records : {s t : PState} → NPath s t → List TRecord
  | _, _, .nil _ => []
  | s, _, .cons e rest => recordOf s e :: records rest

theorem records_aligned {s t : PState} (τ : NPath s t) : Aligned s (records τ) := by
  induction τ with
  | nil _ => trivial
  | cons _ _ ih => exact ⟨rfl, rfl, ih⟩

theorem eraseTrace_records {s t : PState} (τ : NPath s t) :
    eraseTrace (records τ) = Path.events τ := by
  induction τ with
  | nil _ => rfl
  | cons e _ ih => exact congrArg (List.cons e) ih

theorem endState_records {s t : PState} (τ : NPath s t) :
    endState s (records τ) = t := by
  induction τ with
  | nil _ => rfl
  | cons _ _ ih => exact ih

/-- Every step of the path is accepted from a state of the sealed
well-formed class. -/
def AllAccepted : {s t : PState} → NPath s t → Prop
  | _, _, .nil _ => True
  | s, _, .cons e rest => Accepted s e = true ∧ WFClass s ∧ AllAccepted rest

theorem wfRecord_recordOf (s : PState) (e : PEvent) (ha : Accepted s e = true)
    (hw : WFClass s) : WFRecord (recordOf s e) :=
  ⟨rfl, rfl, rfl, rfl, rfl, ha, hw⟩

theorem records_legal {s t : PState} (τ : NPath s t) (h : AllAccepted τ) :
    LegalTrace s (records τ) := by
  refine ⟨records_aligned τ, ?_⟩
  induction τ with
  | nil _ => intro r hr; cases hr
  | cons e rest ih =>
      intro r hr
      rcases List.mem_cons.mp hr with hr | hr
      · rw [hr]; exact wfRecord_recordOf _ e h.1 h.2.1
      · exact ih h.2.2 r hr

/-- Change the source index of a path along an equation. -/
def castSrc {a b t : PState} (h : a = b) (τ : NPath a t) : NPath b t := h ▸ τ

theorem events_castSrc {a b t : PState} (h : a = b) (τ : NPath a t) :
    Path.events (castSrc h τ) = Path.events τ := by
  subst h; rfl

theorem records_castSrc {a b t : PState} (h : a = b) (τ : NPath a t) :
    records (castSrc h τ) = records τ := by
  subst h; rfl

/-- Every aligned typed trace is a native path. -/
def ofAligned : (s : PState) → (tr : List TRecord) → Aligned s tr →
    NPath s (endState s tr)
  | s, [], _ => .nil s
  | _, r :: rest, h =>
      .cons r.ev (castSrc (h.2.1.trans (congrArg (fun x => step x r.ev) h.1))
        (ofAligned r.post rest h.2.2))

theorem events_ofAligned (s : PState) (tr : List TRecord) (h : Aligned s tr) :
    Path.events (ofAligned s tr h) = eraseTrace tr := by
  induction tr generalizing s with
  | nil => rfl
  | cons r rest ih =>
      show r.ev :: Path.events (castSrc _ (ofAligned r.post rest h.2.2)) =
        r.ev :: eraseTrace rest
      rw [events_castSrc, ih r.post h.2.2]

/-- The sealed erasure theorem, recovered from the path square. -/
theorem replay_erases_via_paths (tr : List TRecord) (s : PState)
    (h : Aligned s tr) : replayP (eraseTrace tr) s = endState s tr := by
  rw [← events_ofAligned s tr h]
  exact Path.run_events _

theorem recordOf_of_wf (s : PState) (r : TRecord) (hs : r.pre = s)
    (hw : WFRecord r) : recordOf s r.ev = r := by
  obtain ⟨hpost, hg, hc, hb, hp, _, _⟩ := hw
  cases r with
  | mk pre ev guard post cls spend profile =>
      simp only at hs hpost hg hc hb hp
      subst hs
      simp only [recordOf, hpost, hg, hc, hb, hp]

/-- A legal typed trace is recovered exactly by `records`. -/
theorem records_ofAligned (s : PState) (tr : List TRecord) (h : LegalTrace s tr) :
    records (ofAligned s tr h.1) = tr := by
  induction tr generalizing s with
  | nil => rfl
  | cons r rest ih =>
      have hw : WFRecord r := h.2 r (List.mem_cons_self ..)
      have hrest : LegalTrace r.post rest :=
        ⟨h.1.2.2, fun x hx => h.2 x (List.mem_cons_of_mem r hx)⟩
      show recordOf s r.ev :: records (castSrc _ (ofAligned r.post rest h.1.2.2)) =
        r :: rest
      rw [records_castSrc, ih r.post hrest, recordOf_of_wf s r h.1.1 hw]

/-! ## Refusal and the terminal along paths -/

theorem refusals_mono {s t : PState} (τ : NPath s t) (i j : Nat)
    (h : (i, j) ∈ s.refusals) : (i, j) ∈ t.refusals := by
  have hr := refusal_persists_replay (Path.events τ) s i j h
  rw [← Path.run_events τ]
  exact hr

theorem halted_path {s t : PState} (τ : NPath s t) (h : s.halted = true) : t = s := by
  rw [← Path.run_events τ]
  exact replayP_halted (Path.events τ) s h

/-! ## The size measure and the fields a cycle can move -/

/-- Number of columns plus their total length. -/
def colSize : List (List Nat) → Nat
  | [] => 0
  | c :: rest => 1 + c.length + colSize rest

def obsSize : Option (List (List Nat)) → Nat
  | none => 0
  | some cols => 1 + colSize cols

def bit : Bool → Nat
  | true => 1
  | false => 0

/-- Every field except budget and license. -/
def core (s : PState) :
    List Nat × List (Nat × Nat) × List (Nat × Nat) × List (Nat × Nat) ×
      Option (List (List Nat)) × List (Nat × Nat) × Bool :=
  (s.occ, s.asserted, s.wit, s.prot, s.obs, s.refusals, s.halted)

/-- A size read from the core fields only. -/
def size (s : PState) : Nat :=
  s.occ.length + s.asserted.length + s.wit.length + s.prot.length +
    obsSize s.obs + s.refusals.length + bit s.halted

theorem colSize_append (cols : List (List Nat)) (c : List Nat) :
    colSize (cols ++ [c]) = colSize cols + (1 + c.length) := by
  induction cols with
  | nil => simp [colSize]
  | cons d rest ih => simp only [List.cons_append, colSize, ih]; omega

theorem colSize_refine_le (cols : List (List Nat)) (v : List Nat) (p : Nat) :
    colSize cols ≤ colSize (cols.map (fun c => if c = v then p :: c else c)) := by
  induction cols with
  | nil => exact Nat.le_refl _
  | cons d rest ih =>
      simp only [List.map_cons, colSize]
      by_cases hd : d = v
      · rw [if_pos hd]; simp only [List.length_cons]; omega
      · rw [if_neg hd]; omega

theorem colSize_refine_lt (cols : List (List Nat)) (v : List Nat) (p : Nat)
    (h : v ∈ cols) :
    colSize cols < colSize (cols.map (fun c => if c = v then p :: c else c)) := by
  induction cols with
  | nil => cases h
  | cons d rest ih =>
      simp only [List.map_cons, colSize]
      by_cases hd : d = v
      · rw [if_pos hd]
        have := colSize_refine_le rest v p
        simp only [List.length_cons]; omega
      · rw [if_neg hd]
        have hv : v ∈ rest := by
          rcases List.mem_cons.mp h with h' | h'
          · exact absurd h'.symm hd
          · exact h'
        have := ih hv
        omega

/-- **Every step keeps the core or strictly grows the size.** -/
theorem step_keep_or_grow (s : PState) (e : PEvent) :
    core (step s e) = core s ∨ size s < size (step s e) := by
  rw [step_eq_ite]
  by_cases hg : guardHolds s e = true
  · rw [if_pos hg]
    have hlive : s.halted = false := live_of_guardHolds s e hg
    cases e with
    | admitOcc t =>
        right; simp only [postOf, occS, size, List.length_append,
          List.length_singleton]; omega
    | assertWit i j =>
        right; simp only [postOf, assS, size, List.length_append,
          List.length_singleton]; omega
    | admitWit i j =>
        right; simp only [postOf, witS, size, List.length_append,
          List.length_singleton]; omega
    | protect i j =>
        right; simp only [postOf, protS, size, List.length_append,
          List.length_singleton]; omega
    | declareObs =>
        right
        have ho : s.obs = none := by
          simp only [guardHolds, Bool.and_eq_true, decide_eq_true_eq] at hg
          exact hg.2
        simp only [postOf, obsS, size, ho, obsSize, colSize]; omega
    | refineCol v p =>
        right
        have hok : refineOk s v p = true := by
          simp only [guardHolds, Bool.and_eq_true] at hg; exact hg.1.2
        obtain ⟨cols, ho⟩ := refineOk_declared s v p hok
        have hv : v ∈ cols := by
          rw [refineOk, ho] at hok
          simp only [Bool.and_eq_true, decide_eq_true_eq] at hok
          exact hok.1.1.1.1
        have hlt := colSize_refine_lt cols v p hv
        simp only [postOf, ho, refineS, size, obsSize]; omega
    | addCol c =>
        right
        have hok : colOk s c = true := by
          simp only [guardHolds, Bool.and_eq_true] at hg; exact hg.1.1.2
        obtain ⟨cols, ho⟩ := colOk_declared s c hok
        simp only [postOf, ho, colS, size, obsSize, colSize_append]; omega
    | refuse i j =>
        right; simp only [postOf, refuseS, size, List.length_append,
          List.length_singleton]; omega
    | setBudget n => left; rfl
    | setLicense b => left; rfl
    | halt =>
        right; simp only [postOf, haltS, size, hlive, bit]; omega
  · rw [if_neg hg]; left; rfl

theorem size_eq_of_core_eq {s t : PState} (h : core s = core t) : size s = size t := by
  simp only [core, Prod.mk.injEq] at h
  obtain ⟨h1, h2, h3, h4, h5, h6, h7⟩ := h
  simp only [size, h1, h2, h3, h4, h5, h6, h7]

theorem size_step_mono (s : PState) (e : PEvent) : size s ≤ size (step s e) := by
  rcases step_keep_or_grow s e with h | h
  · rw [size_eq_of_core_eq h]; exact Nat.le_refl _
  · exact Nat.le_of_lt h

theorem core_step_of_size_eq (s : PState) (e : PEvent)
    (h : size (step s e) = size s) : core (step s e) = core s := by
  rcases step_keep_or_grow s e with h' | h'
  · exact h'
  · exact absurd h (Nat.ne_of_gt h')

/-- **A cycle keeps the core.** -/
theorem passage_cycle_core {s t : PState} (p : NPath s t) (q : NPath t s) :
    core t = core s :=
  Path.cycle_core size core size_step_mono core_step_of_size_eq p q

/-- A state on a cycle through `s` is `s` with at most its budget and
license changed. -/
theorem passage_cycle_budget_license {s t : PState} (p : NPath s t) (q : NPath t s) :
    t = { s with budget := t.budget, licensed := t.licensed } := by
  have h := passage_cycle_core p q
  cases s
  cases t
  simp only [core, Prod.mk.injEq] at h
  obtain ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩ := h
  rfl

/-- The budget carries a nontrivial cycle at genesis. -/
theorem budget_cycle :
    ∃ (t : PState) (_ : NPath genesisP t) (_ : NPath t genesisP), t ≠ genesisP :=
  ⟨{ genesisP with budget := 1 },
    Path.cons (.setBudget 1) (Path.nil _),
    Path.cons (.setBudget 0) (Path.nil _),
    by decide⟩

/-- The license carries a nontrivial cycle at genesis. -/
theorem license_cycle :
    ∃ (t : PState) (_ : NPath genesisP t) (_ : NPath t genesisP), t ≠ genesisP :=
  ⟨{ genesisP with licensed := false },
    Path.cons (.setLicense false) (Path.nil _),
    Path.cons (.setLicense true) (Path.nil _),
    by decide⟩

end ResearchNativeBridge
