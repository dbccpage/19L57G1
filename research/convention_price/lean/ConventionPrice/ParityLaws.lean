/-
ParityLaws: the algebra of slot relabels on the two-label fibre, at
parity level, on an abstract family (DEFINITION + PROVED_THEOREM).

The model.  A two-label transport is the identity or the exchange, so
at parity level it is one `Bool`: `false` for the identity, `true` for
the exchange.  A slot map within the {identity, exchange} bound is
likewise one `Bool`.  Composition of transports is `xor` of parities,
and the inverse of a two-label transport is itself, so parity is
unchanged by traversal direction -- that is a fact of the model
declared here, not an imported theorem.  A `Step` is one traversal of
one hop: the hop's transport parity `t` and the two slot parities `a`,
`b` consumed at its ends.  Holonomy of a walk is the parity sum of its
steps.  Everything is core Lean; nothing sealed is imported.
-/

namespace ConventionPrice

/-- One traversal at parity level: transport parity `t`, consumed slot
parities `a` (near end) and `b` (far end). -/
structure Step where
  t : Bool
  a : Bool
  b : Bool

/-- The relabelled transport parity of a step: conjugation by the two
slot maps adds both slot parities. -/
def relabelled (s : Step) : Bool := s.a ^^ (s.t ^^ s.b)

/-- The slot parity a step consumes: the parity sum of its two slot
maps. -/
def consumed (s : Step) : Bool := s.a ^^ s.b

/-- Holonomy parity of a list of parities. -/
def holo (l : List Bool) : Bool := l.foldr (· ^^ ·) false

theorem holo_nil : holo [] = false := rfl

theorem holo_cons (x : Bool) (l : List Bool) : holo (x :: l) = (x ^^ holo l) := rfl

-- Parity bookkeeping, each proved by exhausting the finitely many
-- label cases explicitly; no decidability instance is consulted.

theorem xor_self' (b : Bool) : (b ^^ b) = false := by cases b <;> rfl

theorem xor_false' (b : Bool) : (b ^^ false) = b := by cases b <;> rfl

theorem false_xor' (b : Bool) : (false ^^ b) = b := by cases b <;> rfl

theorem xor_mix (p q r s : Bool) :
    ((p ^^ q) ^^ (r ^^ s)) = ((q ^^ r) ^^ (p ^^ s)) := by
  cases p <;> cases q <;> cases r <;> cases s <;> rfl

theorem xor_cancel_mid (p q r : Bool) : ((p ^^ q) ^^ (q ^^ r)) = (p ^^ r) := by
  cases p <;> cases q <;> cases r <;> rfl

/-- The relabelled parity is the consumed slot parity plus the original
transport parity. -/
theorem relabelled_eq (s : Step) : relabelled s = (consumed s ^^ s.t) := by
  obtain ⟨t, a, b⟩ := s
  cases t <;> cases a <;> cases b <;> rfl

/-- Target 1.  Composing a hop transport with the two slot maps at its
ends toggles its flip parity iff exactly one slot map is the
exchange. -/
theorem slot_toggles_parity (s : Step) : (relabelled s ≠ s.t) ↔ (s.a ≠ s.b) := by
  obtain ⟨t, a, b⟩ := s
  cases t <;> cases a <;> cases b <;> simp [relabelled]

/-- Target 2.  A walk's relabelled holonomy parity is the original
holonomy parity plus the parity sum of the slot parities its
traversals consume. -/
theorem cycle_parity_sum (w : List Step) :
    holo (w.map relabelled) =
      (holo (w.map Step.t) ^^ holo (w.map consumed)) := by
  induction w with
  | nil => rfl
  | cons s w ih =>
      show (relabelled s ^^ holo (w.map relabelled))
        = ((s.t ^^ holo (w.map Step.t)) ^^ (consumed s ^^ holo (w.map consumed)))
      rw [ih, relabelled_eq]
      exact xor_mix (consumed s) s.t (holo (w.map Step.t)) (holo (w.map consumed))

section Pointwise

variable {V : Type}

/-- The slot parities a pointwise assignment `eps` spends along a
vertex chain: one parity sum `eps u ^^ eps v` per traversed hop. -/
def chainConsumed (eps : V → Bool) : V → List V → List Bool
  | _, [] => []
  | u, v :: rest => (eps u ^^ eps v) :: chainConsumed eps v rest

/-- The final vertex of a chain. -/
def chainEnd (u : V) : List V → V
  | [] => u
  | v :: rest => chainEnd v rest

theorem chain_telescope (eps : V → Bool) (u : V) (l : List V) :
    holo (chainConsumed eps u l) = (eps u ^^ eps (chainEnd u l)) := by
  induction l generalizing u with
  | nil => exact (xor_self' (eps u)).symm
  | cons v rest ih =>
      show ((eps u ^^ eps v) ^^ holo (chainConsumed eps v rest))
        = (eps u ^^ eps (chainEnd v rest))
      rw [ih v]
      exact xor_cancel_mid (eps u) (eps v) (eps (chainEnd v rest))

/-- Target 3, first half.  On a closed chain, a pointwise assignment's
consumed slot parities cancel: each vertex's parity is spent an even
number of times. -/
theorem pointwise_parity_blind (eps : V → Bool) (u : V) (l : List V)
    (hclosed : chainEnd u l = u) : holo (chainConsumed eps u l) = false := by
  rw [chain_telescope, hclosed]
  exact xor_self' (eps u)

/-- A chain with transports: each entry is (transport parity, next
vertex).  Under a pointwise assignment the slot parities consumed are
the vertex parities at the two ends of each hop. -/
def chainSteps (eps : V → Bool) : V → List (Bool × V) → List Step
  | _, [] => []
  | u, (t, v) :: rest => ⟨t, eps u, eps v⟩ :: chainSteps eps v rest

/-- The final vertex of a chain with transports. -/
def stepsEnd (u : V) : List (Bool × V) → V
  | [] => u
  | (_, v) :: rest => stepsEnd v rest

theorem chainSteps_consumed (eps : V → Bool) (u : V) (w : List (Bool × V)) :
    (chainSteps eps u w).map consumed = chainConsumed eps u (w.map Prod.snd) := by
  induction w generalizing u with
  | nil => rfl
  | cons e rest ih =>
      obtain ⟨t, v⟩ := e
      show consumed ⟨t, eps u, eps v⟩ :: (chainSteps eps v rest).map consumed
        = (eps u ^^ eps v) :: chainConsumed eps v (rest.map Prod.snd)
      rw [ih v]
      rfl

theorem chainSteps_end (u : V) (w : List (Bool × V)) :
    chainEnd u (w.map Prod.snd) = stepsEnd u w := by
  induction w generalizing u with
  | nil => rfl
  | cons e rest ih => obtain ⟨t, v⟩ := e; exact ih v

/-- Target 3, second half.  A pointwise assignment leaves every closed
walk's holonomy parity unchanged: the invariance of the pinned packet,
at parity level, proved abstractly on this model. -/
theorem pointwise_cycle_invariant (eps : V → Bool) (u : V)
    (w : List (Bool × V)) (hclosed : stepsEnd u w = u) :
    holo ((chainSteps eps u w).map relabelled)
      = holo ((chainSteps eps u w).map Step.t) := by
  rw [cycle_parity_sum, chainSteps_consumed, chain_telescope, chainSteps_end,
    hclosed, xor_self', xor_false']

end Pointwise

end ConventionPrice
