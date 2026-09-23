/-!
# Paths indexed by actual steps

AuthorityEffect: None.  A path from `s` to `t` over a deterministic step
function `f` is a list of events read as a chain of actual steps.  Each
constructor is indexed by the post-state that `f` computes, so no
intermediate state of a path is free data: the end state is a function of
the start state and the events.

Proved here, for every step function:

* `run_events`: replaying a path's events from its start gives its end.
* `events_ofEvents`, `sigma_ofEvents_events`, `toSub_ofSub`,
  `ofSub_toSub`: paths from `s` to `t` correspond exactly to event lists
  whose replay from `s` ends at `t`.  Encoding is `events`; decoding is
  `ofSub`.
* `append` with `nil_append`, `append_nil`, `append_assoc` and
  `events_append`: paths compose, with identities and associativity, and
  `events` sends composition to list concatenation.
* `events_injective`: two paths with the same endpoints and the same
  events are equal.
* `measure_mono`, `core_eq_of_measure_eq`, `cycle_core`: if a measure
  never decreases along a step, and a step that keeps the measure keeps a
  declared core, then every state that lies on a cycle through `s` has the
  core of `s`.  Both premises are hypotheses of these theorems.
-/

namespace ResearchNativeBridge

/-- Deterministic replay: fold the step function over an event list. -/
def run {σ ε : Type} (f : σ → ε → σ) (l : List ε) (s : σ) : σ :=
  l.foldl f s

theorem run_nil {σ ε : Type} (f : σ → ε → σ) (s : σ) : run f [] s = s := rfl

theorem run_cons {σ ε : Type} (f : σ → ε → σ) (e : ε) (l : List ε) (s : σ) :
    run f (e :: l) s = run f l (f s e) := rfl

theorem run_append {σ ε : Type} (f : σ → ε → σ) (l₁ l₂ : List ε) (s : σ) :
    run f (l₁ ++ l₂) s = run f l₂ (run f l₁ s) := by
  induction l₁ generalizing s with
  | nil => rfl
  | cons e rest ih => exact ih (f s e)

/-- A chain of actual steps from `s` to `t`. -/
inductive Path {σ ε : Type} (f : σ → ε → σ) : σ → σ → Type where
  | nil (s : σ) : Path f s s
  | cons {s t : σ} (e : ε) (rest : Path f (f s e) t) : Path f s t

namespace Path

variable {σ ε : Type} {f : σ → ε → σ}

/-- Encoding: the events of a path. -/
def events : {s t : σ} → Path f s t → List ε
  | _, _, .nil _ => []
  | _, _, .cons e rest => e :: events rest

/-- Decoding an arbitrary event list from `s`; its end is computed. -/
def ofEvents (f : σ → ε → σ) : (s : σ) → (l : List ε) → Path f s (run f l s)
  | s, [] => .nil s
  | s, e :: l => .cons e (ofEvents f (f s e) l)

/-- **The replay square.**  A path's events replay from its start to its
end. -/
theorem run_events {s t : σ} (τ : Path f s t) : run f (events τ) s = t := by
  induction τ with
  | nil _ => rfl
  | cons _ _ ih => exact ih

theorem events_ofEvents (s : σ) (l : List ε) :
    events (ofEvents f s l) = l := by
  induction l generalizing s with
  | nil => rfl
  | cons e rest ih => exact congrArg (List.cons e) (ih (f s e))

/-- Decoding the events of a path returns the path, with its end. -/
theorem sigma_ofEvents_events {s t : σ} (τ : Path f s t) :
    (⟨run f (events τ) s, ofEvents f s (events τ)⟩ : Σ u, Path f s u) =
      ⟨t, τ⟩ := by
  induction τ with
  | nil _ => rfl
  | cons e _ ih =>
      exact congrArg
        (fun (x : Σ u, Path f _ u) => (⟨x.1, Path.cons e x.2⟩ : Σ u, Path f _ u))
        ih

theorem events_cast {s t t' : σ} (h : t = t') (τ : Path f s t) :
    events (h ▸ τ) = events τ := by
  subst h
  rfl

theorem cast_eq_of_sigma {s a t : σ} {p : Path f s a} {τ : Path f s t}
    (hs : (⟨a, p⟩ : Σ u, Path f s u) = ⟨t, τ⟩) (h : a = t) : h ▸ p = τ := by
  subst h
  exact eq_of_heq (Sigma.mk.inj hs).2

/-- Encoding into event lists that replay to the end. -/
def toSub {s t : σ} (τ : Path f s t) : {l : List ε // run f l s = t} :=
  ⟨events τ, run_events τ⟩

/-- Decoding from event lists that replay to the end. -/
def ofSub {s t : σ} (x : {l : List ε // run f l s = t}) : Path f s t :=
  x.2 ▸ ofEvents f s x.1

theorem toSub_ofSub {s t : σ} (x : {l : List ε // run f l s = t}) :
    toSub (ofSub x) = x := by
  apply Subtype.ext
  show events (x.2 ▸ ofEvents f s x.1) = x.1
  rw [events_cast]
  exact events_ofEvents s x.1

theorem ofSub_toSub {s t : σ} (τ : Path f s t) : ofSub (toSub τ) = τ :=
  cast_eq_of_sigma (sigma_ofEvents_events τ) (run_events τ)

/-- Paths with the same endpoints are determined by their events. -/
theorem events_injective {s t : σ} (τ τ' : Path f s t)
    (h : events τ = events τ') : τ = τ' := by
  have hsub : toSub τ = toSub τ' := Subtype.ext h
  rw [← ofSub_toSub τ, ← ofSub_toSub τ', hsub]

/-! ## Composition -/

def append : {s t w : σ} → Path f s t → Path f t w → Path f s w
  | _, _, _, .nil _, q => q
  | _, _, _, .cons e rest, q => .cons e (append rest q)

theorem nil_append {s t : σ} (q : Path f s t) : append (.nil s) q = q := rfl

theorem append_nil {s t : σ} (p : Path f s t) : append p (.nil t) = p := by
  induction p with
  | nil _ => rfl
  | cons e _ ih => exact congrArg (Path.cons e) ih

theorem append_assoc {s t v w : σ} (p : Path f s t) (q : Path f t v)
    (r : Path f v w) : append (append p q) r = append p (append q r) := by
  induction p with
  | nil _ => rfl
  | cons e _ ih => exact congrArg (Path.cons e) (ih q)

theorem events_append {s t w : σ} (p : Path f s t) (q : Path f t w) :
    events (append p q) = events p ++ events q := by
  induction p with
  | nil _ => rfl
  | cons e _ ih => exact congrArg (List.cons e) (ih q)

/-! ## Monotone measures and cycles -/

/-- A measure that no step decreases does not decrease along a path. -/
theorem measure_mono (μ : σ → Nat) (hmono : ∀ s e, μ s ≤ μ (f s e))
    {s t : σ} (τ : Path f s t) : μ s ≤ μ t := by
  induction τ with
  | nil _ => exact Nat.le_refl _
  | cons e _ ih => exact Nat.le_trans (hmono _ e) ih

/-- If a step that keeps the measure keeps the core, a path whose end has
the start's measure keeps the core. -/
theorem core_eq_of_measure_eq {κ : Type} (μ : σ → Nat) (core : σ → κ)
    (hmono : ∀ s e, μ s ≤ μ (f s e))
    (hkeep : ∀ s e, μ (f s e) = μ s → core (f s e) = core s)
    {s t : σ} (τ : Path f s t) (h : μ t ≤ μ s) : core t = core s := by
  induction τ with
  | nil _ => rfl
  | @cons s' t' e rest ih =>
      have h1 : μ s' ≤ μ (f s' e) := hmono s' e
      have h2 : μ (f s' e) ≤ μ t' := measure_mono μ hmono rest
      have heq : μ (f s' e) = μ s' :=
        Nat.le_antisymm (Nat.le_trans h2 h) h1
      rw [ih (Nat.le_trans h h1), hkeep s' e heq]

/-- **Cycles keep the core.**  A state `t` that lies on a cycle through
`s` has the core of `s`. -/
theorem cycle_core {κ : Type} (μ : σ → Nat) (core : σ → κ)
    (hmono : ∀ s e, μ s ≤ μ (f s e))
    (hkeep : ∀ s e, μ (f s e) = μ s → core (f s e) = core s)
    {s t : σ} (p : Path f s t) (q : Path f t s) : core t = core s :=
  core_eq_of_measure_eq μ core hmono hkeep p (measure_mono μ hmono q)

end Path

end ResearchNativeBridge
