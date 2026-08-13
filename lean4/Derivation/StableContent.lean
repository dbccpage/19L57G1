import Derivation.PrimitivePassage

/-!
# Stable content: protected separation, and quiescence

Caller-requested final theorems, in the native passage calculus:

1. **Stable content IS protected separation**
   (`stable_content_persists`, `stable_content_replays`): once a
   PROTECTED pair is separated by the declared observation, every
   accepted event of the calculus preserves that separation — supply
   events do not touch observation, new columns only add separators,
   and same-level refinement is guarded by exactly the monotone
   preservation of protected separations.  Protection is
   load-bearing: an UNPROTECTED separation can be destroyed by an
   accepted refinement (`unprotected_separation_unstable`) — so the
   stable content is exactly the protected separations, not
   separation as such.
2. **Quiescence is protected pairs inside the stable content**
   (`quiescent_iff_protected_separated`,
   `quiescence_is_stable_content`): on a declared state, no pair is
   actively obstructed exactly when every retained protected pair is
   separated — i.e. exactly when every retained protected pair
   already belongs to the stable content.

Scope: theorems quantify over the declared event grammar of
`PrimitivePassage.step` only; nothing is claimed for other calculi,
and pre-observational states have no separations to stabilize.
-/

namespace StableContent

open PrimitivePassage

/-- Membership in the stable content: the pair is protected and the
declared observation separates it. -/
def stableSep (s : PState) (i j : Nat) : Bool :=
  (decide ((i, j) ∈ s.prot))
    && (match s.obs with
        | none => false
        | some cols => sepP cols i j)

theorem sepP_append (cols : List (List Nat)) (c : List Nat)
    (i j : Nat) (h : sepP cols i j = true) :
    sepP (cols ++ [c]) i j = true := by
  unfold sepP at h ⊢
  rw [List.any_append, h]
  rfl

/-- The refinement guard hands back exactly what stability needs:
an accepted refinement preserves every protected separation. -/
theorem sepP_refine (s : PState) (cols : List (List Nat))
    (v : List Nat) (p : Nat) (i j : Nat)
    (hobs : s.obs = some cols) (hro : refineOk s v p = true)
    (hp : (i, j) ∈ s.prot) (hsep : sepP cols i j = true) :
    sepP (cols.map (fun c => if c = v then p :: c else c)) i j
      = true := by
  unfold refineOk at hro
  rw [hobs] at hro
  simp only [Bool.and_eq_true] at hro
  have hall := hro.2
  rw [List.all_eq_true] at hall
  have hthis := hall (i, j) hp
  rw [hsep] at hthis
  simp only [Bool.not_true, Bool.false_or] at hthis
  exact hthis

/-- Protection is never lost: every event's result keeps every
protected pair protected. -/
theorem prot_mono (s : PState) (e : PEvent) (i j : Nat)
    (h : (i, j) ∈ s.prot) : (i, j) ∈ (step s e).prot := by
  cases e <;> unfold step <;> (repeat' split) <;>
    first
      | exact h
      | exact List.mem_append.mpr (Or.inl h)

/-- Separation of a protected pair survives every event. -/
theorem sep_preserved (s : PState) (e : PEvent) (i j : Nat)
    (cols : List (List Nat)) (hobs : s.obs = some cols)
    (hp : (i, j) ∈ s.prot) (hsep : sepP cols i j = true) :
    ∃ cols', (step s e).obs = some cols'
      ∧ sepP cols' i j = true := by
  cases e with
  | admitOcc t =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          repeat' split
          all_goals exact ⟨cols, hobs, hsep⟩
  | assertWit a b =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          repeat' split
          all_goals exact ⟨cols, hobs, hsep⟩
  | admitWit a b =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          repeat' split
          all_goals exact ⟨cols, hobs, hsep⟩
  | protect a b =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          repeat' split
          all_goals exact ⟨cols, hobs, hsep⟩
  | declareObs =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc),
              hobs]
          exact ⟨cols, hobs, hsep⟩
  | refineCol v p =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          by_cases hg : (refineOk s v p && decide (0 < s.budget))
              = true
          · have hg2 := hg
            simp only [Bool.and_eq_true] at hg2
            rw [if_pos hg, hobs]
            refine ⟨_, rfl, ?_⟩
            exact sepP_refine s cols v p i j hobs hg2.1 hp hsep
          · rw [if_neg hg]
            exact ⟨cols, hobs, hsep⟩
  | addCol c =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          by_cases hg : (colOk s c && s.licensed
              && decide (0 < s.budget)) = true
          · rw [if_pos hg, hobs]
            exact ⟨cols ++ [c], rfl, sepP_append cols c i j hsep⟩
          · rw [if_neg hg]
            exact ⟨cols, hobs, hsep⟩
  | refuse a b =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          repeat' split
          all_goals exact ⟨cols, hobs, hsep⟩
  | setBudget n =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          exact ⟨cols, hobs, hsep⟩
  | setLicense b =>
      cases hhb : s.halted with
      | true => rw [step_halted s _ hhb]; exact ⟨cols, hobs, hsep⟩
      | false =>
          simp only [step, hhb]
          rw [if_neg (fun hc : false = true => Bool.noConfusion hc)]
          exact ⟨cols, hobs, hsep⟩
  | halt => exact ⟨cols, hobs, hsep⟩

/-- **Stable content persists at every step**: membership in the
stable content is preserved by every event of the declared
grammar. -/
theorem stable_content_persists (s : PState) (e : PEvent)
    (i j : Nat) (h : stableSep s i j = true) :
    stableSep (step s e) i j = true := by
  unfold stableSep at h
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨hp, hsep⟩ := h
  cases hobs : s.obs with
  | none => rw [hobs] at hsep; cases hsep
  | some cols =>
      rw [hobs] at hsep
      obtain ⟨cols', hobs', hsep'⟩ :=
        sep_preserved s e i j cols hobs hp hsep
      unfold stableSep
      rw [hobs', decide_eq_true (prot_mono s e i j hp)]
      show (true && sepP cols' i j) = true
      rw [hsep']
      exact rfl

/-- Stable content persists along every replay. -/
theorem stable_content_replays (h : List PEvent) :
    ∀ (s : PState) (i j : Nat), stableSep s i j = true →
      stableSep (replayP h s) i j = true := by
  induction h with
  | nil =>
      intro s i j hs
      exact hs
  | cons e t ih =>
      intro s i j hs
      show stableSep (replayP t (step s e)) i j = true
      exact ih (step s e) i j (stable_content_persists s e i j hs)

/-- **Protection is load-bearing** (countermodel): an accepted
refinement — discharging a protected obstruction, preserving every
protected separation — DESTROYS the separation of an unprotected
pair.  The stable content is exactly the protected separations, not
separation as such. -/
def sUnprot : PState :=
  { occ := [0, 1, 2], asserted := [(1, 2)], wit := [(1, 2)],
    prot := [(1, 2)], obs := some [[0]], budget := 1,
    licensed := true, refusals := [], halted := false }

theorem unprotected_separation_unstable :
    (sepP [[0]] 0 1 = true) ∧
    ((step sUnprot (.refineCol [0] 1)).obs = some [[1, 0]]) ∧
    (sepP [[1, 0]] 0 1 = false) ∧
    ((1, 2) ∈ sUnprot.prot) ∧
    (sepP [[1, 0]] 1 2 = true) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- Quiescence: no pair is actively obstructed. -/
def quiescentP (s : PState) : Prop := ∀ i j, obstP s i j = false

/-- **Quiescence ⟺ every retained protected pair is separated**, on
a declared state. -/
theorem quiescent_iff_protected_separated (s : PState)
    (cols : List (List Nat)) (hobs : s.obs = some cols) :
    quiescentP s ↔
      (∀ pr, pr ∈ s.prot → pr ∈ s.wit →
        sepP cols pr.1 pr.2 = true) := by
  constructor
  · intro hq pr hp hw
    obtain ⟨a, b⟩ := pr
    have h := hq a b
    rw [obst_agrees_when_declared s cols hobs] at h
    rw [decide_eq_true hw, decide_eq_true hp] at h
    simp only [Bool.true_and] at h
    cases hb : sepP cols a b with
    | true => rfl
    | false =>
        exfalso
        unfold zeroP at h
        rw [hb] at h
        exact Bool.noConfusion h
  · intro hs i j
    rw [obst_agrees_when_declared s cols hobs]
    by_cases hw : (i, j) ∈ s.wit
    · by_cases hp : (i, j) ∈ s.prot
      · have hsep := hs (i, j) hp hw
        unfold zeroP
        rw [decide_eq_true hw, decide_eq_true hp, hsep]
        rfl
      · rw [decide_eq_false hp]
        simp
    · rw [decide_eq_false hw]
      simp

/-- **Quiescence is protected pairs inside the stable content**: on
a declared state, no pair obstructs exactly when every retained
protected pair already belongs to the stable content. -/
theorem quiescence_is_stable_content (s : PState)
    (cols : List (List Nat)) (hobs : s.obs = some cols) :
    quiescentP s ↔
      (∀ pr, pr ∈ s.prot → pr ∈ s.wit →
        stableSep s pr.1 pr.2 = true) := by
  rw [quiescent_iff_protected_separated s cols hobs]
  constructor
  · intro hs pr hp hw
    unfold stableSep
    rw [hobs, decide_eq_true (show (pr.1, pr.2) ∈ s.prot from hp)]
    show (true && sepP cols pr.1 pr.2) = true
    rw [hs pr hp hw]
    exact rfl
  · intro hs pr hp hw
    have h := hs pr hp hw
    unfold stableSep at h
    rw [hobs] at h
    simp only [Bool.and_eq_true] at h
    exact h.2

end StableContent
