/-!
# The boundary world, as far as Challenge 0 requires

Core Lean only; no dependency on any other package in this repository.

The initial inscription is one supplied opaque datum.  The one admitted
primitive exception is its boundary with two sides.  A regime records, for
each later mark in admission order, the side it lies on (`false` and `true`).
A reading is metatheory: `U` leaves the sides unnamed, `O` names them.  The
closed observation grammar has positive mark-on-side and side-name forms;
it has no empty-side or counting form.
-/

namespace BoundarySeed

/-- The declared reading of the boundary. -/
inductive Reading where
  | U
  | O
  deriving DecidableEq, Repr

/-- The one opaque supplied datum.  Its presentation spelling is not stored. -/
inductive OpaqueDatum where
  | initial
  deriving DecidableEq, Repr

/-- Admitted state: initial datum, reading, and every later mark placement. -/
structure Regime where
  reading : Reading
  initialDatum : OpaqueDatum
  placement : List Bool
  deriving DecidableEq, Repr

/-- The genesis regime: the opaque datum is present and no later mark is placed. -/
def genesis (r : Reading) : Regime := ⟨r, .initial, []⟩

/-- The events.  A supply presents and changes nothing; an admission places
one mark on a side. -/
inductive Event where
  | supply
  | place (side : Bool)
  deriving DecidableEq, Repr

/-- One step.  Deterministic. -/
def step (r : Regime) : Event → Regime
  | .supply => r
  | .place s => ⟨r.reading, r.initialDatum, r.placement ++ [s]⟩

/-- Replay a history from a base regime. -/
def replay (h : List Event) (base : Regime) : Regime :=
  h.foldl step base

/-- Challenge 0 declares no object-language rule from state to an event. -/
def EventFollows (_r : Regime) (_e : Event) : Prop := False

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

/-- The closed Challenge 0 observation grammar. -/
inductive Judgment where
  | onSide (mark : Nat) (side : Bool)
  | sideNamed (side : Bool) (visible : Name)
  deriving DecidableEq, Repr

/-- Whether a positive judgment in the closed grammar holds. -/
def holds (r : Regime) : Judgment → Bool
  | .onSide i s => onSide r i s
  | .sideNamed s n => r.reading == .O && name s == n

/-- Extensional metatheoretic profile; it is not an object-language list. -/
structure SideProfile where
  visibleName : Option Name
  marks : List Nat
  deriving DecidableEq, Repr

def sideProfile (r : Regime) (side : Bool) : SideProfile :=
  ⟨if r.reading == .O then some (name side) else none, contents r side⟩

/-- Whether reflection is an operation permitted by the reading. -/
def reflectionPermitted : Reading → Prop
  | .U => True
  | .O => False

/-- The exchange of the two sides. -/
def reflect (r : Regime) : Regime :=
  ⟨r.reading, r.initialDatum, r.placement.map (fun b => !b)⟩

/-! ## Inertia -/

/-- A supply changes no state. -/
theorem supply_no_op (r : Regime) : step r .supply = r := rfl

/-- Any already-provided event that changes state is a placement. -/
theorem step_changes_only_by_place (r : Regime) (e : Event)
    (h : step r e ≠ r) : ∃ s, e = .place s := by
  cases e with
  | supply => exact absurd rfl h
  | place s => exact ⟨s, rfl⟩

theorem genesis_initial_datum (rd : Reading) :
    (genesis rd).initialDatum = .initial := rfl

theorem genesis_placement_nil (rd : Reading) : (genesis rd).placement = [] := rfl

/-- No positive mark-on-side judgment holds at genesis. -/
theorem no_observation_at_genesis (rd : Reading) (i : Nat) (s : Bool) :
    holds (genesis rd) (.onSide i s) = false := by
  simp [holds, onSide, genesis]

theorem O_name_judgment_at_genesis (s : Bool) :
    holds (genesis .O) (.sideNamed s (name s)) = true := by
  simp [holds, genesis]

theorem U_no_name_judgment_at_genesis (s : Bool) (n : Name) :
    holds (genesis .U) (.sideNamed s n) = false := by
  simp [holds, genesis]

theorem contents_genesis (rd : Reading) (s : Bool) : contents (genesis rd) s = [] := by
  simp [contents, genesis]

/-! ## The two sides at genesis -/

/-- Under reading `U`, the two extensional side profiles agree at genesis. -/
theorem sides_collapsed_at_genesis_U :
    sideProfile (genesis .U) false = sideProfile (genesis .U) true := by
  simp [sideProfile, contents, genesis]

/-- Under reading `O` the two extensional profiles differ only by name. -/
theorem sides_distinct_at_genesis_O :
    sideProfile (genesis .O) false ≠ sideProfile (genesis .O) true := by
  simp [sideProfile, contents, genesis, name]

/-- The two name constructors differ.  Definition-level support only. -/
theorem side_names_distinct : name false ≠ name true := by
  decide

/-! ## The reflection -/

theorem map_not_not (p : List Bool) : (p.map (fun b => !b)).map (fun b => !b) = p := by
  induction p with
  | nil => rfl
  | cons b t ih => simp [ih]

theorem reflect_reflect (r : Regime) : reflect (reflect r) = r := by
  cases r with
  | mk rd d p =>
    show Regime.mk rd d ((p.map (fun b => !b)).map (fun b => !b)) = Regime.mk rd d p
    rw [map_not_not]

theorem reflect_genesis (rd : Reading) : reflect (genesis rd) = genesis rd := rfl

theorem reflection_permitted_U : reflectionPermitted .U := by
  trivial

theorem reflection_not_permitted_O : ¬ reflectionPermitted .O := by
  simp [reflectionPermitted]

/-- Once a mark is placed, the reflection moves it: the reflected regime
differs from the original.  Under `O` this is a different state; under
`U` it is the same state up to the renaming the reading cannot see. -/
theorem reflect_moves_a_mark (rd : Reading) (d : OpaqueDatum)
    (s : Bool) (rest : List Bool) :
    reflect ⟨rd, d, s :: rest⟩ ≠ ⟨rd, d, s :: rest⟩ := by
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

/-- No event follows from admitted state in the declared Challenge 0 relation. -/
theorem no_event_follows (r : Regime) (e : Event) : ¬ EventFollows r e := by
  simp [EventFollows]

end BoundarySeed
