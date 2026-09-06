import BoundarySeed.Basic
import BoundarySeed.Challenge1
import BoundarySeed.Challenge2
import BoundarySeed.Challenge3
import BoundarySeed.Challenge4

/-!
# Challenge 5: a whole within a side

Core Lean only.  The caller supplies and retains one opaque whole lying inside
one side of another, and the run must say what an admission does with an item
that is itself a whole.  The Python side declares four policies and prices
them; this file closes the three things the enumeration cannot close on its
own, and each of them is about the STATE and not about the policy space.

The first is the invisibility of the nesting.  A state that records one side
per mark is the image of a state that records the whole crossing under
`flattenDeep`, and that map is not injective: `flatten_nested_eq_flat` shows
the caller's nested whole and the flat whole of Challenge 1 have the SAME
image, so no property of the flattened state tells them apart.  Better,
`flattenDeep_exchangeLevel_succ` shows that flattening is blind to every
exchange below the outermost boundary, for an arbitrary state and an arbitrary
level, which is stronger than the caller's one inscription.

The second is what an exchange at a level can and cannot move.  Every level
exchange keeps an address's length, so `depth_invariant_under_exchange` says a
mark's depth is fixed by every renaming of this shape — the reason depth is
internally available once the state records the crossing.  Against that,
`exchangeLevel_one_nestedRetained` computes that the exchange of the inner
boundary's two sides DOES move the caller's retained state, and
`no_invariant_property_separates_the_inner_sides` turns that into a statement
about an arbitrary property of a state and a mark: nothing invariant under the
inner exchange tells the caller's whole from the one with the mark on the
other inner side.  `innerSideIsZero` is the countermodel that keeps the
hypothesis from being vacuous, and it is exactly the property the naming
declaration of the Python space makes available.

The third is inertia at depth.  `deepReplay_addresses_append` and
`nested_depth_survives_every_continuation` show that no later history of the
deep grammar moves an already admitted mark's depth, and
`deepReplay_initialDatum` that no history of it makes a second initial datum,
so the inner whole is never one.
-/

namespace BoundarySeed

/-- An address: the sides crossed to reach a mark, outermost first. -/
abbrev Address := List Bool

/-- Admitted state under a policy that records the crossing: for each mark, in
admission order, the sides crossed to reach it. -/
structure DeepRegime where
  reading : Reading
  initialDatum : OpaqueDatum
  addresses : List Address
  deriving DecidableEq, Repr

def deepGenesis (r : Reading) : DeepRegime := ⟨r, .initial, []⟩

/-- The deep events.  A supply presents and changes nothing; an admission
places one mark at an address. -/
inductive DeepEvent where
  | supply
  | placeAt (address : Address)
  deriving DecidableEq, Repr

def deepStep (r : DeepRegime) : DeepEvent → DeepRegime
  | .supply => r
  | .placeAt a => ⟨r.reading, r.initialDatum, r.addresses ++ [a]⟩

def deepReplay (h : List DeepEvent) (base : DeepRegime) : DeepRegime :=
  h.foldl deepStep base

/-- Challenge 5 declares no object-language rule from deep state to an event. -/
def DeepEventFollows (_r : DeepRegime) (_e : DeepEvent) : Prop := False

/-- The depth of a mark: how many boundaries were crossed to reach it. -/
def depthOf (r : DeepRegime) (i : Nat) : Nat := (r.addresses.getD i []).length

/-- What a policy that records one side per mark holds instead: the outermost
crossing of each address, with everything below it discarded. -/
def flattenAddress (a : Address) : Bool := a.getD 0 false

def flattenDeep (r : DeepRegime) : Regime :=
  ⟨r.reading, r.initialDatum, r.addresses.map flattenAddress⟩

/-- The exchange of one boundary level's two sides, on an address.  An address
that never crossed that boundary is unchanged. -/
def exchangeAt : Nat → Address → Address
  | _, [] => []
  | 0, s :: t => (!s) :: t
  | k + 1, s :: t => s :: exchangeAt k t

/-- The exchange of one boundary level's two sides, on a state. -/
def exchangeLevel (k : Nat) (r : DeepRegime) : DeepRegime :=
  ⟨r.reading, r.initialDatum, r.addresses.map (exchangeAt k)⟩

/-! ## The caller's whole, and the flat whole of Challenge 1 -/

/-- The caller's Challenge 5 history under the recording policy and the
declared convention: one supply, then one placement two boundaries in. -/
def challenge5History : List DeepEvent := [.supply, .placeAt [false, false]]

/-- The same inscription with its inner boundary discarded, which is what the
Challenge 1 inscription presents: one supply, then one placement one boundary
in. -/
def challenge5FlatHistory : List DeepEvent := [.supply, .placeAt [false]]

def nestedRetained (rd : Reading) : DeepRegime :=
  deepReplay challenge5History (deepGenesis rd)

def flatRetained (rd : Reading) : DeepRegime :=
  deepReplay challenge5FlatHistory (deepGenesis rd)

theorem nestedRetained_eq (rd : Reading) :
    nestedRetained rd = ⟨rd, .initial, [[false, false]]⟩ := rfl

theorem flatRetained_eq (rd : Reading) :
    flatRetained rd = ⟨rd, .initial, [[false]]⟩ := rfl

theorem nestedRetained_addresses (rd : Reading) :
    (nestedRetained rd).addresses = [[false, false]] := rfl

theorem deep_supply_no_op (r : DeepRegime) : deepStep r .supply = r := rfl

/-- Any deep event that changes state is a placement. -/
theorem deepStep_changes_only_by_placeAt (r : DeepRegime) (e : DeepEvent)
    (h : deepStep r e ≠ r) : ∃ a, e = .placeAt a := by
  cases e with
  | supply => exact absurd rfl h
  | placeAt a => exact ⟨a, rfl⟩

/-- No event follows from deep admitted state in the declared relation. -/
theorem deep_no_event_follows (r : DeepRegime) (e : DeepEvent) :
    ¬ DeepEventFollows r e := by
  simp [DeepEventFollows]

/-! ## Depth -/

theorem nestedRetained_depth (rd : Reading) : depthOf (nestedRetained rd) 0 = 2 := rfl

theorem flatRetained_depth (rd : Reading) : depthOf (flatRetained rd) 0 = 1 := rfl

/-- **The recording state tells the nested whole from the flat one**, and the
depth is what tells them apart. -/
theorem nestedRetained_ne_flatRetained (rd : Reading) :
    nestedRetained rd ≠ flatRetained rd := by
  intro h
  have hd : depthOf (nestedRetained rd) 0 = depthOf (flatRetained rd) 0 := by rw [h]
  rw [nestedRetained_depth, flatRetained_depth] at hd
  exact absurd hd (by decide)

/-- A level exchange keeps an address's length. -/
theorem exchangeAt_length (k : Nat) (a : Address) : (exchangeAt k a).length = a.length := by
  induction a generalizing k with
  | nil => cases k <;> rfl
  | cons s t ih =>
    cases k with
    | zero => rfl
    | succ m =>
      show (s :: exchangeAt m t).length = (s :: t).length
      simp [ih m]

/-- **A mark's depth is fixed by every level exchange.**  That is why depth is
internally available once the state records the crossing: no renaming of this
shape moves it. -/
theorem depth_invariant_under_exchange (k : Nat) (r : DeepRegime) (i : Nat) :
    depthOf (exchangeLevel k r) i = depthOf r i := by
  show ((r.addresses.map (exchangeAt k)).getD i []).length = (r.addresses.getD i []).length
  rw [List.getD_eq_getElem?_getD, List.getD_eq_getElem?_getD, List.getElem?_map]
  cases h : r.addresses[i]? with
  | none => rfl
  | some a =>
    show (exchangeAt k a).length = a.length
    exact exchangeAt_length k a

theorem exchangeAt_involutive (k : Nat) (a : Address) :
    exchangeAt k (exchangeAt k a) = a := by
  induction a generalizing k with
  | nil => cases k <;> rfl
  | cons s t ih =>
    cases k with
    | zero =>
      show (!(!s)) :: t = s :: t
      simp
    | succ m =>
      show s :: exchangeAt m (exchangeAt m t) = s :: t
      rw [ih m]

theorem exchangeLevel_involutive (k : Nat) (r : DeepRegime) :
    exchangeLevel k (exchangeLevel k r) = r := by
  cases r with
  | mk rd d p =>
    show DeepRegime.mk rd d ((p.map (exchangeAt k)).map (exchangeAt k))
        = DeepRegime.mk rd d p
    have : (p.map (exchangeAt k)).map (exchangeAt k) = p := by
      induction p with
      | nil => rfl
      | cons a t ih => simp [exchangeAt_involutive k a, ih]
    rw [this]

/-! ## What flattening cannot see -/

/-- Flattening reads the outermost crossing, which no exchange below the
outermost boundary moves. -/
theorem flattenAddress_exchangeAt_succ (k : Nat) (a : Address) :
    flattenAddress (exchangeAt (k + 1) a) = flattenAddress a := by
  cases a with
  | nil => rfl
  | cons s t => rfl

/-- **A policy that records one side per mark is blind to every inner
exchange.**  Stated for an arbitrary state and an arbitrary level below the
outermost, so it covers every inscription and not the caller's alone. -/
theorem flattenDeep_exchangeLevel_succ (k : Nat) (r : DeepRegime) :
    flattenDeep (exchangeLevel (k + 1) r) = flattenDeep r := by
  cases r with
  | mk rd d p =>
    show Regime.mk rd d ((p.map (exchangeAt (k + 1))).map flattenAddress)
        = Regime.mk rd d (p.map flattenAddress)
    have : (p.map (exchangeAt (k + 1))).map flattenAddress = p.map flattenAddress := by
      induction p with
      | nil => rfl
      | cons a t ih => simp [flattenAddress_exchangeAt_succ k a, ih]
    rw [this]

/-- **The nesting is invisible to a policy that does not record the
crossing.**  The caller's nested whole and the flat whole of Challenge 1 have
the same flattened state, so no property of that state separates them. -/
theorem flatten_nested_eq_flat (rd : Reading) :
    flattenDeep (nestedRetained rd) = flattenDeep (flatRetained rd) := rfl

/-- And that common state is exactly what the Challenge 1 inscription retains
in the inherited model: one mark on side `false`. -/
theorem flatten_nested_eq_admitted (rd : Reading) :
    flattenDeep (nestedRetained rd) = admitted rd false := rfl

/-- So no property of the flattened state separates the two, whatever the
property.  This is the general form of the invisibility, over an arbitrary
property of a regime. -/
theorem no_flattened_property_separates_the_nesting
    (rd : Reading) (P : Regime → Bool) :
    P (flattenDeep (nestedRetained rd)) = P (flattenDeep (flatRetained rd)) := by
  rw [flatten_nested_eq_flat]

/-! ## What the inner exchange moves -/

/-- The caller's whole with the mark on the other side of the INNER boundary. -/
def innerReflected (rd : Reading) : DeepRegime := exchangeLevel 1 (nestedRetained rd)

theorem innerReflected_eq (rd : Reading) :
    innerReflected rd = ⟨rd, .initial, [[false, true]]⟩ := rfl

/-- The exchange of the inner boundary's two sides moves the caller's retained
state, so the two are different states; whether that difference is internally
available is what the naming declaration decides. -/
theorem exchangeLevel_one_nestedRetained (rd : Reading) :
    innerReflected rd ≠ nestedRetained rd := by
  rw [innerReflected_eq, nestedRetained_eq]
  intro h
  simp at h

/-- The outer exchange moves it too, and to a third state. -/
theorem exchangeLevel_zero_nestedRetained (rd : Reading) :
    exchangeLevel 0 (nestedRetained rd) ≠ nestedRetained rd := by
  rw [nestedRetained_eq]
  intro h
  simp [exchangeLevel, exchangeAt] at h

/-- **Nothing invariant under the inner exchange separates the two inner
sides.**  `P` ranges over every property of a state and a mark, so this covers
every judgment form the closed grammar might gain: under a reading whose
naming does not reach the inner boundary, the caller's whole and its inner
reflection satisfy exactly the same such properties. -/
theorem no_invariant_property_separates_the_inner_sides
    (rd : Reading) (P : DeepRegime → Nat → Bool)
    (hinv : ∀ (r : DeepRegime) (i : Nat), P (exchangeLevel 1 r) i = P r i) :
    P (nestedRetained rd) 0 = P (innerReflected rd) 0 := by
  rw [innerReflected]
  exact (hinv (nestedRetained rd) 0).symm

/-- The property that reads which side of the INNER boundary a mark lies on.
It is what a reading whose naming reaches inward makes available. -/
def innerSideIsZero (r : DeepRegime) (i : Nat) : Bool :=
  (r.addresses.getD i []).getD 1 true == false

/-- Its two values at the caller's whole and at that whole's inner reflection,
each with the reading projected away so that a decision procedure is offered a
goal with no free variable in it. -/
theorem innerSideIsZero_nestedRetained (rd : Reading) :
    innerSideIsZero (nestedRetained rd) 0 = true := rfl

theorem innerSideIsZero_innerReflected (rd : Reading) :
    innerSideIsZero (innerReflected rd) 0 = false := rfl

/-- It separates the caller's whole from its inner reflection. -/
theorem innerSideIsZero_separates (rd : Reading) :
    innerSideIsZero (nestedRetained rd) 0 ≠ innerSideIsZero (innerReflected rd) 0 := by
  rw [innerSideIsZero_nestedRetained, innerSideIsZero_innerReflected]
  decide

/-- So the hypothesis above is a real restriction and not a vacuous one: this
property lies outside it. -/
theorem innerSideIsZero_is_not_invariant_under_the_inner_exchange :
    ¬ (∀ (r : DeepRegime) (i : Nat), innerSideIsZero (exchangeLevel 1 r) i
        = innerSideIsZero r i) := by
  intro h
  have h0 := h (nestedRetained .U) 0
  rw [nestedRetained_eq] at h0
  simp [innerSideIsZero, exchangeLevel, exchangeAt] at h0

/-- Depth, by contrast, is invariant under the inner exchange, so it is
available where the inner side is not: the two facts are different and the run
keeps them apart. -/
theorem depth_is_invariant_where_the_inner_side_is_not (rd : Reading) :
    depthOf (nestedRetained rd) 0 = depthOf (innerReflected rd) 0 := by
  rw [innerReflected, depth_invariant_under_exchange]

/-! ## Inertia at depth -/

theorem deepStep_reading (r : DeepRegime) (e : DeepEvent) :
    (deepStep r e).reading = r.reading := by
  cases e <;> rfl

theorem deepStep_initialDatum (r : DeepRegime) (e : DeepEvent) :
    (deepStep r e).initialDatum = r.initialDatum := by
  cases e <;> rfl

theorem deepReplay_reading (h : List DeepEvent) (base : DeepRegime) :
    (deepReplay h base).reading = base.reading := by
  induction h generalizing base with
  | nil => rfl
  | cons e t ih => exact (ih (deepStep base e)).trans (deepStep_reading base e)

/-- **No history of the deep grammar makes a second initial datum**, so an
inner whole is never one, under any policy. -/
theorem deepReplay_initialDatum (h : List DeepEvent) (base : DeepRegime) :
    (deepReplay h base).initialDatum = base.initialDatum := by
  induction h generalizing base with
  | nil => rfl
  | cons e t ih => exact (ih (deepStep base e)).trans (deepStep_initialDatum base e)

/-- Replaying any deep history appends to the address list. -/
theorem deepReplay_addresses_append (h : List DeepEvent) (base : DeepRegime) :
    ∃ suffix, (deepReplay h base).addresses = base.addresses ++ suffix := by
  induction h generalizing base with
  | nil => exact ⟨[], (List.append_nil _).symm⟩
  | cons e t ih =>
    obtain ⟨s, hs⟩ := ih (deepStep base e)
    cases e with
    | supply => exact ⟨s, hs⟩
    | placeAt a =>
      refine ⟨a :: s, ?_⟩
      show (deepReplay t (deepStep base (.placeAt a))).addresses
          = base.addresses ++ (a :: s)
      rw [hs]
      show (base.addresses ++ [a]) ++ s = base.addresses ++ (a :: s)
      simp

/-- The list lemma of Challenge 1, at the type of an address list.  Core Lean
proves it once per type here rather than by a general instance, which keeps
the file free of any import beyond the run's own. -/
theorem getD_append_left_address (l l' : List Address) (i : Nat) (d : Address)
    (h : i < l.length) : (l ++ l').getD i d = l.getD i d := by
  induction l generalizing i with
  | nil => simp at h
  | cons a t ih =>
    cases i with
    | zero => rfl
    | succ k =>
      simp only [List.cons_append, List.getD_cons_succ]
      exact ih k (Nat.lt_of_succ_lt_succ h)

/-- An address already admitted is read the same after any later history. -/
theorem deepReplay_preserves_address (h : List DeepEvent) (base : DeepRegime)
    (i : Nat) (hi : i < base.addresses.length) :
    (deepReplay h base).addresses.getD i [] = base.addresses.getD i [] := by
  obtain ⟨s, hs⟩ := deepReplay_addresses_append h base
  rw [hs]
  exact getD_append_left_address base.addresses s i [] hi

/-- **A mark's depth survives every continuation.**  However many further
marks are admitted, at whatever depth, the caller's mark is still two
boundaries in. -/
theorem nested_depth_survives_every_continuation (rd : Reading) (h : List DeepEvent) :
    depthOf (deepReplay h (nestedRetained rd)) 0 = 2 := by
  have hlen : 0 < (nestedRetained rd).addresses.length := by
    rw [nestedRetained_addresses]; decide
  show ((deepReplay h (nestedRetained rd)).addresses.getD 0 []).length = 2
  rw [deepReplay_preserves_address h (nestedRetained rd) 0 hlen]
  rfl

theorem nestedRetained_reading (rd : Reading) : (nestedRetained rd).reading = rd :=
  deepReplay_reading _ _

theorem nestedRetained_initialDatum (rd : Reading) :
    (nestedRetained rd).initialDatum = .initial :=
  deepReplay_initialDatum _ _

/-- No event follows from the caller's retained deep state. -/
theorem no_event_follows_nestedRetained (rd : Reading) (e : DeepEvent) :
    ¬ DeepEventFollows (nestedRetained rd) e :=
  deep_no_event_follows _ _

end BoundarySeed
