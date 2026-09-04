/-!
# The boundary world, as far as Challenge 0 requires

Core Lean only; no dependency on any other package in this repository.

The one admitted primitive is the boundary with its two sides.  A regime
records, for each admitted mark in admission order, the side it lies on
(`false` and `true` for the two sides).  A reading is metatheory: `U`
leaves the sides unnamed, `O` names them.  Nothing else about a side is
observable; there is no admitted judgment that a side is empty.
-/

namespace BoundarySeed

/-- The declared reading of the boundary. -/
inductive Reading where
  | U
  | O
  deriving DecidableEq, Repr

/-- Admitted state: the reading and the side of every admitted mark. -/
structure Regime where
  reading : Reading
  placement : List Bool
  deriving DecidableEq, Repr

/-- The genesis regime for a reading: no mark is admitted. -/
def genesis (r : Reading) : Regime := ⟨r, []⟩

/-- The events.  A supply presents and changes nothing; an admission places
one mark on a side. -/
inductive Event where
  | supply
  | place (side : Bool)
  deriving DecidableEq, Repr

/-- One step.  Deterministic. -/
def step (r : Regime) : Event → Regime
  | .supply => r
  | .place s => ⟨r.reading, r.placement ++ [s]⟩

/-- Replay a history from a base regime. -/
def replay (h : List Event) (base : Regime) : Regime :=
  h.foldl step base

/-- The marks on a side, by internal identity. -/
def contents (r : Regime) (side : Bool) : List Nat :=
  (List.range r.placement.length).filter
    (fun i => r.placement.getD i (!side) == side)

/-- The admitted observation relation: mark `i` lies on side `s`. -/
def onSide (r : Regime) (i : Nat) (s : Bool) : Bool :=
  i < r.placement.length && r.placement.getD i (!s) == s

/-- The admitted names under reading `O`. -/
inductive Name where
  | near
  | far
  deriving DecidableEq, Repr

def name : Bool → Name
  | false => .near
  | true => .far

/-- The exchange of the two sides. -/
def reflect (r : Regime) : Regime :=
  ⟨r.reading, r.placement.map (fun b => !b)⟩

/-! ## Inertia -/

/-- A supply changes no state. -/
theorem supply_no_op (r : Regime) : step r .supply = r := rfl

/-- The only event that changes state carries an external side: nothing in
the state produces it. -/
theorem step_changes_only_by_place (r : Regime) (e : Event)
    (h : step r e ≠ r) : ∃ s, e = .place s := by
  cases e with
  | supply => exact absurd rfl h
  | place s => exact ⟨s, rfl⟩

theorem genesis_placement_nil (rd : Reading) : (genesis rd).placement = [] := rfl

/-- No observation fires at genesis, for any mark and either side. -/
theorem no_observation_at_genesis (rd : Reading) (i : Nat) (s : Bool) :
    onSide (genesis rd) i s = false := by
  simp [onSide, genesis]

theorem contents_genesis (rd : Reading) (s : Bool) : contents (genesis rd) s = [] := by
  simp [contents, genesis]

/-! ## The two sides at genesis -/

/-- Under reading `U`, everything observable of a side is its contents, and
at genesis both are empty: the sides are observationally collapsed. -/
theorem sides_collapsed_at_genesis_U :
    contents (genesis .U) false = contents (genesis .U) true := by
  simp [contents_genesis]

/-- Under reading `O` the sides carry admitted names and the names differ.
This is the declaration itself and nothing more: DEFINITION-level. -/
theorem side_names_distinct : name false ≠ name true := by
  decide

/-! ## The reflection -/

theorem map_not_not (p : List Bool) : (p.map (fun b => !b)).map (fun b => !b) = p := by
  induction p with
  | nil => rfl
  | cons b t ih => simp [ih]

theorem reflect_reflect (r : Regime) : reflect (reflect r) = r := by
  cases r with
  | mk rd p =>
    show Regime.mk rd ((p.map (fun b => !b)).map (fun b => !b)) = Regime.mk rd p
    rw [map_not_not]

theorem reflect_genesis (rd : Reading) : reflect (genesis rd) = genesis rd := rfl

/-- Once a mark is placed, the reflection moves it: the reflected regime
differs from the original.  Under `O` this is a different state; under
`U` it is the same state up to the renaming the reading cannot see. -/
theorem reflect_moves_a_mark (rd : Reading) (s : Bool) (rest : List Bool) :
    reflect ⟨rd, s :: rest⟩ ≠ ⟨rd, s :: rest⟩ := by
  intro h
  simp [reflect] at h

/-! ## Replay -/

theorem replay_deterministic (h1 h2 : List Event) (base : Regime) (heq : h1 = h2) :
    replay h1 base = replay h2 base := by
  rw [heq]

/-- A history of supplies alone replays to its base. -/
theorem replay_supply_inert (n : Nat) (base : Regime) :
    replay (List.replicate n .supply) base = base := by
  induction n generalizing base with
  | zero => rfl
  | succ k ih =>
    simp only [List.replicate, replay, List.foldl]
    exact ih base

end BoundarySeed
