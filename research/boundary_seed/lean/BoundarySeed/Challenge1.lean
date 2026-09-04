import BoundarySeed.Basic

/-!
# Challenge 1: the supply of `<a|>`

Core Lean only.  The supplied whole is opaque except that the admitted
boundary places its mark on a side.  The Challenge 1 history under a
reading is one supply followed by one placement on a side `s`; which
side the presented left of the bar becomes is a metatheoretic
convention declared in the Python presentation layer, not derived here.
Everything below is stated for both sides `s`, so both candidates are
covered.
-/

namespace BoundarySeed

/-- The Challenge 1 history: a supply, then a placement on side `s`. -/
def challenge1History (s : Bool) : List Event := [.supply, .place s]

/-- The admitted one-mark regime under reading `rd` with the mark on `s`. -/
def admitted (rd : Reading) (s : Bool) : Regime :=
  replay (challenge1History s) (genesis rd)

theorem admitted_eq (rd : Reading) (s : Bool) :
    admitted rd s = ⟨rd, .initial, [s]⟩ := rfl

/-! ## Supply is presentation only -/

/-- A supply changes no judgment of the closed grammar. -/
theorem supply_preserves_holds (r : Regime) (j : Judgment) :
    holds (step r .supply) j = holds r j := rfl

/-! ## Every event keeps the reading and the initial datum -/

theorem step_reading (r : Regime) (e : Event) : (step r e).reading = r.reading := by
  cases e <;> rfl

theorem step_initialDatum (r : Regime) (e : Event) :
    (step r e).initialDatum = r.initialDatum := by
  cases e <;> rfl

theorem replay_reading (h : List Event) (base : Regime) :
    (replay h base).reading = base.reading := by
  induction h generalizing base with
  | nil => rfl
  | cons e t ih =>
    show (replay t (step base e)).reading = base.reading
    exact (ih (step base e)).trans (step_reading base e)

theorem replay_initialDatum (h : List Event) (base : Regime) :
    (replay h base).initialDatum = base.initialDatum := by
  induction h generalizing base with
  | nil => rfl
  | cons e t ih =>
    show (replay t (step base e)).initialDatum = base.initialDatum
    exact (ih (step base e)).trans (step_initialDatum base e)

/-! ## Side names never change -/

/-- A side-name judgment holds after any event exactly as before. -/
theorem step_preserves_sideNamed (r : Regime) (e : Event) (s : Bool) (n : Name) :
    holds (step r e) (.sideNamed s n) = holds r (.sideNamed s n) := by
  cases e <;> rfl

theorem replay_preserves_sideNamed (h : List Event) (base : Regime) (s : Bool) (n : Name) :
    holds (replay h base) (.sideNamed s n) = holds base (.sideNamed s n) := by
  induction h generalizing base with
  | nil => rfl
  | cons e t ih =>
    show holds (replay t (step base e)) (.sideNamed s n) = holds base (.sideNamed s n)
    exact (ih (step base e)).trans (step_preserves_sideNamed base e s n)

/-! ## Retention: an admitted mark's judgment survives every later event -/

theorem getD_append_left (l l' : List Bool) (i : Nat) (d : Bool) (h : i < l.length) :
    (l ++ l').getD i d = l.getD i d := by
  induction l generalizing i with
  | nil => simp at h
  | cons b t ih =>
    cases i with
    | zero => rfl
    | succ k =>
      simp only [List.cons_append, List.getD_cons_succ]
      exact ih k (Nat.lt_of_succ_lt_succ h)

theorem step_preserves_onSide (r : Regime) (e : Event) (i : Nat) (t : Bool)
    (hi : i < r.placement.length) :
    holds (step r e) (.onSide i t) = holds r (.onSide i t) := by
  cases e with
  | supply => rfl
  | place s =>
    simp only [holds, onSide, step, List.length_append, List.length_singleton]
    rw [getD_append_left _ _ _ _ hi]
    have h1 : i < r.placement.length + 1 := Nat.lt_succ_of_lt hi
    simp [hi, h1]

theorem replay_preserves_onSide (h : List Event) (base : Regime) (i : Nat) (t : Bool)
    (hi : i < base.placement.length) :
    holds (replay h base) (.onSide i t) = holds base (.onSide i t) := by
  induction h generalizing base with
  | nil => rfl
  | cons e t' ih =>
    show holds (replay t' (step base e)) (.onSide i t) = holds base (.onSide i t)
    have hlen : i < (step base e).placement.length := by
      cases e with
      | supply => exact hi
      | place s =>
        simp only [step, List.length_append, List.length_singleton]
        exact Nat.lt_succ_of_lt hi
    exact (ih (step base e) hlen).trans (step_preserves_onSide base e i t hi)

/-! ## The new judgment, and only it -/

theorem getD_append_singleton (l : List Bool) (s d : Bool) :
    (l ++ [s]).getD l.length d = s := by
  induction l with
  | nil => rfl
  | cons b t ih =>
    simp only [List.cons_append, List.length_cons, List.getD_cons_succ]
    exact ih

/-- After a placement, the placed mark's judgment on its side holds. -/
theorem place_new_judgment (r : Regime) (s : Bool) :
    holds (step r (.place s)) (.onSide r.placement.length s) = true := by
  simp only [holds, onSide, step, List.length_append, List.length_singleton]
  rw [getD_append_singleton]
  simp

/-- After a placement, the placed mark's judgment on the other side does not hold. -/
theorem place_other_side_false (r : Regime) (s : Bool) :
    holds (step r (.place s)) (.onSide r.placement.length (!s)) = false := by
  simp only [holds, onSide, step, List.length_append, List.length_singleton]
  rw [getD_append_singleton]
  cases s <;> simp

/-- In the Challenge 1 admitted regime exactly one mark-on-side judgment holds:
mark `0` on the placed side. -/
theorem admitted_onSide_true_iff (rd : Reading) (s : Bool) (i : Nat) (t : Bool) :
    holds (admitted rd s) (.onSide i t) = true ↔ i = 0 ∧ t = s := by
  rw [admitted_eq]
  cases i with
  | zero => cases s <;> cases t <;> simp [holds, onSide]
  | succ k => simp [holds, onSide]

/-- Under `U` no side-name judgment holds in the admitted regime. -/
theorem admitted_U_no_sideNamed (s t : Bool) (n : Name) :
    holds (admitted .U s) (.sideNamed t n) = false := by
  rw [admitted_eq]; simp [holds]

/-- Under `O` the two name judgments hold in the admitted regime exactly as at
genesis. -/
theorem admitted_O_sideNamed (s t : Bool) (n : Name) :
    holds (admitted .O s) (.sideNamed t n) = holds (genesis .O) (.sideNamed t n) :=
  replay_preserves_sideNamed _ _ _ _

/-! ## The two sides after one mark -/

theorem admitted_contents_placed (rd : Reading) (s : Bool) :
    contents (admitted rd s) s = [0] := by
  rw [admitted_eq]; cases s <;> simp [contents, List.range, List.range.loop]

theorem admitted_contents_other (rd : Reading) (s : Bool) :
    contents (admitted rd s) (!s) = [] := by
  rw [admitted_eq]; cases s <;> simp [contents, List.range, List.range.loop]

/-- After one admitted mark the two extensional side profiles differ, under
either reading. -/
theorem admitted_sides_differ (rd : Reading) (s : Bool) :
    sideProfile (admitted rd s) s ≠ sideProfile (admitted rd s) (!s) := by
  intro h
  have hm := congrArg SideProfile.marks h
  simp only [sideProfile] at hm
  rw [admitted_contents_placed, admitted_contents_other] at hm
  exact List.cons_ne_nil 0 [] hm

/-! ## The reflection commutes with the events -/

theorem reflect_step_supply (r : Regime) :
    reflect (step r .supply) = step (reflect r) .supply := rfl

theorem reflect_step_place (r : Regime) (s : Bool) :
    reflect (step r (.place s)) = step (reflect r) (.place (!s)) := by
  simp [reflect, step]

/-- The two Challenge 1 candidates are each other's reflection. -/
theorem reflect_admitted (rd : Reading) (s : Bool) :
    reflect (admitted rd s) = admitted rd (!s) := by
  rw [admitted_eq, admitted_eq]; simp [reflect]

/-- The two candidates are unequal as raw data, under either reading. -/
theorem admitted_candidates_unequal (rd : Reading) (s : Bool) :
    admitted rd s ≠ admitted rd (!s) := by
  rw [admitted_eq, admitted_eq]
  intro h
  cases s <;> simp at h

/-- The Challenge 1 isomorphism relation, sufficient for regimes with at most
one mark: equality, or the reflection when the reading permits it.  Mark
permutations are the identity at one mark; the Python relation covers them
in general. -/
def oneMarkRelated (rd : Reading) (a b : Regime) : Prop :=
  a = b ∨ (reflectionPermitted rd ∧ b = reflect a)

/-- Under `U` the two candidates are related by a permitted renaming. -/
theorem candidates_related_U (s : Bool) :
    oneMarkRelated .U (admitted .U s) (admitted .U (!s)) :=
  Or.inr ⟨reflection_permitted_U, (reflect_admitted .U s).symm⟩

/-- Under `O` the two candidates are not related by any permitted renaming. -/
theorem candidates_not_related_O (s : Bool) :
    ¬ oneMarkRelated .O (admitted .O s) (admitted .O (!s)) := by
  intro h
  cases h with
  | inl heq => exact admitted_candidates_unequal .O s heq
  | inr hp => exact reflection_not_permitted_O hp.1

/-- A judgment whose holding is invariant under the reflection cannot separate
the two candidates.  Meaningful under `U`, where the reflection is permitted;
stated for every reading because it is a fact about the function. -/
theorem invariant_judgment_does_not_separate (rd : Reading) (s : Bool) (j : Judgment)
    (hinv : ∀ r, holds (reflect r) j = holds r j) :
    holds (admitted rd s) j = holds (admitted rd (!s)) j := by
  rw [← reflect_admitted]
  exact (hinv _).symm

/-- The placed mark's own judgment does separate the two candidates as raw
data; under `O` it is invariant under every permitted renaming, there being
none but the identity at one mark. -/
theorem onSide_separates_candidates (rd : Reading) (s : Bool) :
    holds (admitted rd s) (.onSide 0 s) = true ∧
      holds (admitted rd (!s)) (.onSide 0 s) = false := by
  constructor
  · exact (admitted_onSide_true_iff rd s 0 s).mpr ⟨rfl, rfl⟩
  · rw [admitted_eq]; cases s <;> simp [holds, onSide]

/-! ## Nothing follows -/

/-- No event follows from the admitted regime in the declared relation. -/
theorem no_event_follows_admitted (rd : Reading) (s : Bool) (e : Event) :
    ¬ EventFollows (admitted rd s) e :=
  no_event_follows _ _

end BoundarySeed
