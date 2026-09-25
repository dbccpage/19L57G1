import SecondSuccession.Kernel

/-!
# Three counts of a history, and the one the regime carries

Native to rung six.

A history is replayed from a base by the sealed step.  Three readings of
an accepted round are declared, each giving a count of a history:

* EVERY: every event; the count is the length of the history;
* ADMITTING: every event other than a supply, whether or not it changes
  the regime (`admitting`);
* CHANGING: exactly the events after which the regime differs from the
  regime before (`changes`).  An ill-formed event ends the count, as it
  ends replay.

The element count `size` is rung five's: data plus forms plus instances,
rules and requirements, each counted as listed.

* `changes_counted`: the element count of the regime a history reaches
  is the base's count plus the CHANGING count.  The statement is rung
  five's `size_counts_changes`; it is proved again here, with its step
  lemma `step_grows` (rung five's `size_step`), so that this package
  imports nothing.
* `changes_path_free`, `changes_given_base`: so the CHANGING count is a
  function of the base and the regime reached.
* `changes_from_genesis`: from the sealed empty regime it is the element
  count of the regime reached, with no base named.
* `changes_le_admitting`, `admitting_le_every`: the three counts are
  ordered, for every history, replayed or not.

Nothing here mentions the sealed isomorphism: whether the count is a
function of the class of a regime is not stated.

AuthorityEffect: None.
-/

namespace SecondSuccession
namespace Count

open Sealed

/-- The element count of a regime, as rung five defined it. -/
def size (r : Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

/-- The CHANGING count of a history replayed from a base. -/
def changes : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' => (if r' = r then 0 else 1) + changes r' es

/-- The weight of one event under ADMITTING: a supply is not accepted. -/
def weight : Event → Nat
  | .supply _ => 0
  | _ => 1

/-- The ADMITTING count of a history: its events other than supplies. -/
def admitting : List Event → Nat
  | [] => 0
  | e :: es => weight e + admitting es

theorem size_genesis : size genesis = 0 := rfl

theorem replayE_cons (e : Event) (es : List Event) (b : Regime) :
    replayE (e :: es) b = (stepE b e).bind (fun r => replayE es r) := by
  cases hs : stepE b e <;> simp [replayE, List.foldlM, hs]

/-- A supply is never a CHANGING round. -/
theorem supply_uncounted (b : Regime) (t : Nat) (h : List Event) :
    changes b (.supply t :: h) = changes b h := by
  show (if b = b then 0 else 1) + changes b h = changes b h
  rw [if_pos rfl, Nat.zero_add]

/-- Deduplicating insertion keeps a list or lengthens it by one. -/
theorem insertNew_grows {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew l a = l ∨ (insertNew l a).length = l.length + 1 := by
  unfold insertNew
  split
  · exact Or.inl rfl
  · exact Or.inr (by rw [List.length_append]; rfl)

/-- One event keeps the regime or raises its element count by one. -/
theorem step_grows {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    r' = r ∨ size r' = size r + 1 := by
  cases e with
  | supply t =>
    exact Or.inl (Option.some.inj h).symm
  | admitDatum =>
    cases Option.some.inj h
    refine Or.inr ?_
    simp only [size]
    omega
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      refine Or.inr ?_
      simp only [size, List.length_append, List.length_singleton]
      omega
    · cases h
  | admitInst f args =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.insts (f, args) with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr ?_
        simp only [size, hk]
        omega
    · cases h
  | admitRuleAll f =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.rules f with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr ?_
        simp only [size, hk]
        omega
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.reqs (i, j) with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr ?_
        simp only [size, hk]
        omega
    · cases h

/-- The CHANGING count, read off the base and the regime reached. -/
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
      rcases step_grows hs with heq | hsz
      · rw [if_pos heq, heq]
        omega
      · have hne : b' ≠ b := by
          intro hq
          rw [hq] at hsz
          omega
        rw [if_neg hne, hsz]
        omega

/-- Two histories from one base to one regime carry one CHANGING count. -/
theorem changes_path_free {h h' : List Event} {b r : Regime}
    (hr : replayE h b = some r) (hr' : replayE h' b = some r) :
    changes b h = changes b h' := by
  have h1 := changes_counted h b r hr
  have h2 := changes_counted h' b r hr'
  omega

/-- From the sealed empty regime the CHANGING count is the element count. -/
theorem changes_from_genesis {h : List Event} {r : Regime}
    (hr : replayE h genesis = some r) : changes genesis h = size r := by
  have h1 := changes_counted h genesis r hr
  rw [size_genesis] at h1
  omega

/-- A function of the base and the regime gives the CHANGING count. -/
theorem changes_given_base :
    ∃ F : Regime → Regime → Nat, ∀ (h : List Event) (b r : Regime),
      replayE h b = some r → changes b h = F b r :=
  ⟨fun b r => size r - size b, fun h b r hr => by
    have h1 := changes_counted h b r hr
    show changes b h = size r - size b
    omega⟩

/-- CHANGING never counts more than ADMITTING. -/
theorem changes_le_admitting (h : List Event) :
    ∀ b : Regime, changes b h ≤ admitting h := by
  induction h with
  | nil => intro _; exact Nat.le_refl 0
  | cons e es ih =>
    intro b
    show changes b (e :: es) ≤ weight e + admitting es
    cases hs : stepE b e with
    | none =>
      have h0 : changes b (e :: es) = 0 := by simp only [changes, hs]
      rw [h0]
      exact Nat.zero_le _
    | some b' =>
      have hc : changes b (e :: es) = (if b' = b then 0 else 1) + changes b' es := by
        simp only [changes, hs]
      have hk : (if b' = b then 0 else 1) ≤ weight e := by
        cases e with
        | supply t =>
          have hq : b' = b := (Option.some.inj hs).symm
          rw [if_pos hq]
          exact Nat.le_refl 0
        | _ =>
          show _ ≤ 1
          split <;> omega
      have hi := ih b'
      rw [hc]
      omega

/-- ADMITTING never counts more than EVERY. -/
theorem admitting_le_every : ∀ h : List Event, admitting h ≤ h.length
  | [] => Nat.le_refl 0
  | e :: es => by
    have ih := admitting_le_every es
    have hw : weight e ≤ 1 := by
      cases e <;> simp only [weight] <;> omega
    show weight e + admitting es ≤ es.length + 1
    omega

end Count
end SecondSuccession
