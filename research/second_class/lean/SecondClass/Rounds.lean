import SecondClass.Kernel

/-!
# The three counts of a history, proved again

Native to rung eight, except for the statements it credits.

A history is replayed from a base by the sealed step.  A CHANGING event
is one after which the regime differs (rung six).  A GROWTH is a changing
event after which the regime has more data; a REST ROUND is a changing
event that is not a growth (rung seven).  An ill-formed event ends every
count, as it ends replay.

Credited statements, proved again here so that this package imports
nothing: `size` is rung five's element count; `changes` and
`changes_counted` are rung six's (rung five's `size_counts_changes`);
`growths`, `rest`, `step_parts`, `growths_counted` and `rest_counted` are
rung seven's; `replayE_cons` and `insertNew_grows` are rungs six and
seven's.  The definitions and statements are theirs, unedited but for
the namespace; `changes_counted` is proved here through `step_parts`
rather than rung six's step lemma.

Native here:

* `replayE_split`: a history cut in two replays as its first part, then
  its second from the regime the first reaches.
* `still_of_no_changes`: a history with CHANGING count zero that replays
  reaches its base.

Nothing here mentions the sealed isomorphism.

AuthorityEffect: None.
-/

namespace SecondClass
namespace Rounds

open Sealed

/-- The element count of a regime, as rung five defined it. -/
def size (r : Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

/-- The growths of a history replayed from a base. -/
def growths : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' => (if r'.data = r.data then 0 else 1) + growths r' es

/-- The rest rounds of a history replayed from a base. -/
def rest : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' => (if r' ≠ r ∧ r'.data = r.data then 1 else 0) + rest r' es

/-- The CHANGING count of a history replayed from a base, as rung six
defined it. -/
def changes : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' => (if r' = r then 0 else 1) + changes r' es

theorem replayE_cons (e : Event) (es : List Event) (b : Regime) :
    replayE (e :: es) b = (stepE b e).bind (fun r => replayE es r) := by
  cases hs : stepE b e <;> simp [replayE, List.foldlM, hs]

/-- Deduplicating insertion keeps a list or lengthens it by one. -/
theorem insertNew_grows {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew l a = l ∨ (insertNew l a).length = l.length + 1 := by
  unfold insertNew
  split
  · exact Or.inl rfl
  · exact Or.inr (by rw [List.length_append]; rfl)

/-- One event keeps the regime, or is a growth adding one element, or is a
rest round adding one element. -/
theorem step_parts {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    r' = r ∨ (r'.data = r.data + 1 ∧ size r' = size r + 1) ∨
      (r'.data = r.data ∧ size r' = size r + 1) := by
  cases e with
  | supply t =>
    exact Or.inl (Option.some.inj h).symm
  | admitDatum =>
    cases Option.some.inj h
    refine Or.inr (Or.inl ⟨rfl, ?_⟩)
    simp only [size]
    omega
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      refine Or.inr (Or.inr ⟨rfl, ?_⟩)
      simp only [size, List.length_append, List.length_singleton]
      omega
    · cases h
  | admitInst f args =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.insts (f, args) with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr (Or.inr ⟨rfl, ?_⟩)
        simp only [size, hk]
        omega
    · cases h
  | admitRuleAll f =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.rules f with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr (Or.inr ⟨rfl, ?_⟩)
        simp only [size, hk]
        omega
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.reqs (i, j) with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr (Or.inr ⟨rfl, ?_⟩)
        simp only [size, hk]
        omega
    · cases h

/-- The number of growths, read off the base and the regime reached. -/
theorem growths_counted (h : List Event) :
    ∀ b r : Regime, replayE h b = some r → r.data = b.data + growths b h := by
  induction h with
  | nil =>
    intro b r hr
    cases Option.some.inj hr
    rfl
  | cons e es ih =>
    intro b r hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hrest : r.data = b'.data + growths b' es := ih b' r hr
      have hc : growths b (e :: es) =
          (if b'.data = b.data then 0 else 1) + growths b' es := by
        simp only [growths, hs]
      rw [hc, hrest]
      rcases step_parts hs with heq | ⟨hd, _⟩ | ⟨hd, _⟩
      · rw [heq, if_pos rfl]
        omega
      · rw [if_neg (by omega), hd]
        omega
      · rw [if_pos hd, hd]
        omega

/-- The element count of the regime reached is the base's plus the growths
plus the rest rounds. -/
theorem rest_counted (h : List Event) :
    ∀ b r : Regime, replayE h b = some r →
      size r = size b + growths b h + rest b h := by
  induction h with
  | nil =>
    intro b r hr
    cases Option.some.inj hr
    rfl
  | cons e es ih =>
    intro b r hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hrest : size r = size b' + growths b' es + rest b' es := ih b' r hr
      have hg : growths b (e :: es) =
          (if b'.data = b.data then 0 else 1) + growths b' es := by
        simp only [growths, hs]
      have hq : rest b (e :: es) =
          (if b' ≠ b ∧ b'.data = b.data then 1 else 0) + rest b' es := by
        simp only [rest, hs]
      rw [hg, hq, hrest]
      rcases step_parts hs with heq | ⟨hd, hsz⟩ | ⟨hd, hsz⟩
      · subst heq
        rw [if_pos rfl, if_neg (fun hc => hc.1 rfl)]
        omega
      · have hne : b' ≠ b := fun hc => by rw [hc] at hd; omega
        rw [if_neg (by omega), if_neg (fun hc => by omega), hsz]
        omega
      · have hne : b' ≠ b := fun hc => by rw [hc] at hsz; omega
        rw [if_pos hd, if_pos ⟨hne, hd⟩, hsz]
        omega


/-- The element count of the regime reached is the base's plus the
CHANGING count (rung six's statement). -/
theorem changes_counted (h : List Event) :
    ∀ b r : Regime, replayE h b = some r → size r = size b + changes b h := by
  induction h with
  | nil =>
    intro b r hr
    cases Option.some.inj hr
    rfl
  | cons e es ih =>
    intro b r hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hrest : size r = size b' + changes b' es := ih b' r hr
      have hc : changes b (e :: es) = (if b' = b then 0 else 1) + changes b' es := by
        simp only [changes, hs]
      rw [hc, hrest]
      rcases step_parts hs with heq | ⟨_, hsz⟩ | ⟨_, hsz⟩
      · rw [if_pos heq, heq]
        omega
      · have hne : b' ≠ b := fun hq => by rw [hq] at hsz; omega
        rw [if_neg hne, hsz]
        omega
      · have hne : b' ≠ b := fun hq => by rw [hq] at hsz; omega
        rw [if_neg hne, hsz]
        omega

/-- A history cut in two replays as its first part, then its second from
the regime the first reaches. -/
theorem replayE_split (h₁ h₂ : List Event) (b : Regime) :
    replayE (h₁ ++ h₂) b = (replayE h₁ b).bind (fun r => replayE h₂ r) := by
  unfold replayE
  exact List.foldlM_append

/-- A history with CHANGING count zero that replays reaches its base. -/
theorem still_of_no_changes (h : List Event) :
    ∀ b r : Regime, replayE h b = some r → changes b h = 0 → r = b := by
  induction h with
  | nil =>
    intro b r hr _
    exact (Option.some.inj hr).symm
  | cons e es ih =>
    intro b r hr hz
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hc : changes b (e :: es) = (if b' = b then 0 else 1) + changes b' es := by
        simp only [changes, hs]
      rw [hc] at hz
      by_cases hb : b' = b
      · rw [if_pos hb] at hz
        have hr' := ih b' r hr (by omega)
        rw [hr', hb]
      · rw [if_neg hb] at hz
        omega

end Rounds
end SecondClass
