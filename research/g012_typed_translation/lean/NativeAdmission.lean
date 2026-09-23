import Derivation.Basic

/-!
A scoped obstruction using the actual native admission and replay functions.
Successful native traces cannot form a nontrivial state cycle. Consequently,
a carrier with such a cycle cannot have a left-invertible state encoding
whose two transitions commute with finite native admission traces.
This is a negative result, not a construction of native encode/decode maps.
The Python replacement-cycle witness is checked separately.
AuthorityEffect: None.
-/

namespace G012TypedTranslation.NativeAdmission

open Derivation

def weight (r : Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

theorem step_identity_or_weight_increases (r s : Regime) (e : Event)
    (h : stepE r e = some s) : s = r ∨ weight r < weight s := by
  cases e with
  | supply token =>
      simp only [stepE, Option.some.injEq] at h
      exact Or.inl h.symm
  | admitDatum =>
      simp only [stepE, Option.some.injEq] at h
      subst s
      right
      simp only [weight]
      omega
  | admitForm arity =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst s
        right
        simp only [weight, List.length_append, List.length_cons, List.length_nil]
        omega
      · contradiction
  | admitInst form args =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst s
        by_cases hm : (form, args) ∈ r.insts
        · left
          simp [insertNew, hm]
        · right
          simp only [weight, insertNew, hm, ↓reduceIte, List.length_append,
            List.length_cons, List.length_nil]
          omega
      · contradiction
  | admitRuleAll form =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst s
        by_cases hm : form ∈ r.rules
        · left
          simp [insertNew, hm]
        · right
          simp only [weight, insertNew, hm, ↓reduceIte, List.length_append,
            List.length_cons, List.length_nil]
          omega
      · contradiction
  | impose i j =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst s
        by_cases hm : (i, j) ∈ r.reqs
        · left
          simp [insertNew, hm]
        · right
          simp only [weight, insertNew, hm, ↓reduceIte, List.length_append,
            List.length_cons, List.length_nil]
          omega
      · contradiction

theorem replay_identity_or_weight_increases (r s : Regime) (history : List Event)
    (h : replayE history r = some s) : s = r ∨ weight r < weight s := by
  induction history generalizing r with
  | nil =>
      have he : r = s := Option.some.inj h
      exact Or.inl he.symm
  | cons e history ih =>
      have hb : (stepE r e >>= fun t => replayE history t) = some s := h
      cases hs : stepE r e with
      | none => simp [hs] at hb
      | some t =>
          simp only [hs] at hb
          rcases step_identity_or_weight_increases r t e hs with he | hi
          · subst t
            exact ih r hb
          rcases ih t hb with he | hj
          · subst s
            exact Or.inr hi
          exact Or.inr (Nat.lt_trans hi hj)

theorem trace_cycle_is_identity (r s : Regime) (forward backward : List Event)
    (hf : replayE forward r = some s) (hb : replayE backward s = some r) : s = r := by
  rcases replay_identity_or_weight_increases r s forward hf with he | hi
  · exact he
  rcases replay_identity_or_weight_increases s r backward hb with he | hj
  · exact he.symm
  omega

theorem no_roundtrip_commuting_trace_cycle {α : Type} (a b : α) (different : a ≠ b)
    (encode : α → Regime) (decode : Regime → α)
    (roundtrip : ∀ x, decode (encode x) = x)
    (forward backward : List Event)
    (hf : replayE forward (encode a) = some (encode b))
    (hb : replayE backward (encode b) = some (encode a)) : False := by
  have he := trace_cycle_is_identity (encode a) (encode b) forward backward hf hb
  have hd := congrArg decode he
  rw [roundtrip, roundtrip] at hd
  exact different hd.symm

end G012TypedTranslation.NativeAdmission
