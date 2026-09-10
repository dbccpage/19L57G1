import Trace

/-!
# Constructive Endpoint Factorization Theorem

Formalizes the principle that future state trajectories factor strictly
through terminal 0-cell endpoints (`future_factors_through_endpoint`).

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
Constructive formalization in Lean 4 without Classical.choice or Mathlib.
AuthorityEffect: None.
-/

namespace G013TraceCalculus

/-! ## 1. Categorical 1-Cell Endpoint Factorization -/

/-- In the 2-cell trace calculus, any two execution histories terminating at a shared
0-cell s factor future continuation paths strictly through s. -/
theorem future_factors_through_endpoint_1cell {σ : Type} {s1 s2 s dst : σ}
    (h1 : Trace σ s1 s) (h2 : Trace σ s2 s) (f : Trace σ s dst) :
    targetOf (concat h1 f) = targetOf (concat h2 f) := by
  rw [targetOf_concat, targetOf_concat]

/-- The terminal state reached by continuing from either history is identically the
terminal state of the future continuation trace. -/
theorem endpoint_factorization_target_eq {σ : Type} {s1 s s_target : σ}
    (h : Trace σ s1 s) (f : Trace σ s s_target) :
    targetOf (concat h f) = targetOf f :=
  rfl

/-! ## 2. Operational Deterministic Transition System Factorization -/

/-- A deterministic labeled transition system on state carrier σ. -/
structure System (σ : Type) where
  step : σ → String → σ

/-- Replay execution of a sequence of actions from a base state. -/
def replay {σ : Type} (sys : System σ) (s : σ) : List String → σ
  | [] => s
  | a :: rest => replay sys (sys.step s a) rest

/-- Replay execution decomposes over list concatenation (history append). -/
theorem replay_append {σ : Type} (sys : System σ) (s : σ) (h k : List String) :
    replay sys s (h ++ k) = replay sys (replay sys s h) k := by
  induction h generalizing s with
  | nil => rfl
  | cons a rest ih =>
    show replay sys (sys.step s a) (rest ++ k) = replay sys (replay sys (sys.step s a) rest) k
    exact ih (sys.step s a)

/-- General Endpoint Factorization Theorem (Deterministic):
Two computational histories h1 and h2 originating from possibly distinct states s1, s2
that reach an identical intermediate state s agree on all future continuations k. -/
theorem future_factors_through_endpoint {σ : Type} (sys : System σ) {s1 s2 s : σ}
    {h1 h2 k : List String}
    (e1 : replay sys s1 h1 = s)
    (e2 : replay sys s2 h2 = s) :
    replay sys s1 (h1 ++ k) = replay sys s2 (h2 ++ k) := by
  rw [replay_append, replay_append, e1, e2]

/-! ## 3. Guarded Transition System Factorization -/

/-- A guarded transition system where transitions may fail or refuse. -/
structure GuardedSystem (σ : Type) where
  step : σ → String → Option σ

/-- Replay execution for guarded transitions returning none upon refusal. -/
def replayGuarded {σ : Type} (sys : GuardedSystem σ) (s : σ) : List String → Option σ
  | [] => some s
  | a :: rest =>
      match sys.step s a with
      | none => none
      | some s' => replayGuarded sys s' rest

/-- Replay on guarded systems decomposes over event suffixes. -/
theorem replayGuarded_append {σ : Type} (sys : GuardedSystem σ) (s : σ) (h k : List String) :
    replayGuarded sys s (h ++ k) =
      match replayGuarded sys s h with
      | none => none
      | some mid => replayGuarded sys mid k := by
  induction h generalizing s with
  | nil => rfl
  | cons a rest ih =>
    show (match sys.step s a with
          | none => none
          | some s' => replayGuarded sys s' (rest ++ k)) =
         (match (match sys.step s a with
                 | none => none
                 | some s' => replayGuarded sys s' rest) with
          | none => none
          | some mid => replayGuarded sys mid k)
    cases hstep : sys.step s a with
    | none => rfl
    | some s' =>
      exact ih s'

/-- General Endpoint Factorization Theorem (Guarded / Refusal-Aware):
Two histories yielding the same valid intermediate state produce identical future continuations. -/
theorem future_factors_through_endpoint_guarded {σ : Type} (sys : GuardedSystem σ)
    {s1 s2 s : σ} {h1 h2 k : List String}
    (e1 : replayGuarded sys s1 h1 = some s)
    (e2 : replayGuarded sys s2 h2 = some s) :
    replayGuarded sys s1 (h1 ++ k) = replayGuarded sys s2 (h2 ++ k) := by
  rw [replayGuarded_append, replayGuarded_append, e1, e2]

end G013TraceCalculus
