import SecondIso.Transport

/-!
# The first count along class-matched histories

This file is this rung's own object.  Rung three proved the first count
unique and exhibited two histories reaching ONE regime with different
first counts, so the first count is not a function of the regime a
history reaches, and so not of its isomorphism class either.  The reading
examined here is the other one the rung-three leftover names: two
histories, each from its own base, whose prefixes reach regimes the
isomorphism relates AT EVERY COUNT -- class-matched histories.  Under a
uniform stake they have the same first counts; `Countermodel.lean` shows
that under the three stakes that are not uniform they need not.

A second, separate reading: renaming the token a supply carries.  Presentation
identity is not internal identity, and the reconstructed step ignores a
supply's token outright, so the first count does not move.  The Lean datum
admission carries no token at all, so this is the whole of presentation
renaming the Lean model can express; the Python rectangle checks a
renaming of datum tokens as well.

AuthorityEffect: None.
-/

namespace SecondIso
namespace Trajectory

open SecondIso.Sealed
open SecondIso.Inherited
open SecondIso.IndexSlice
open SecondIso.Transport

/-! ## 1. Class-matched histories -/

/-- Two prefix readings are RELATED when both reach regimes the
isomorphism relates, or both reach none. -/
def Related : Option Regime → Option Regime → Prop
  | some r, some s => Nonempty (Iso r s)
  | none, none => True
  | _, _ => False

/-- Two histories, each from its own base, are CLASS-MATCHED when their
prefixes are related at every count. -/
def Matched (base : Regime) (h : List Event) (base' : Regime)
    (h' : List Event) : Prop :=
  ∀ k, Related (stateAt h base k) (stateAt h' base' k)

/-- **related_symm.**  Relatedness is symmetric, through the sealed
inverse isomorphism. -/
theorem related_symm {a b : Option Regime} (hab : Related a b) :
    Related b a := by
  cases a with
  | none =>
    cases b with
    | none => trivial
    | some s => exact absurd hab (by simp [Related])
  | some r =>
    cases b with
    | none => exact absurd hab (by simp [Related])
    | some s =>
      obtain ⟨i⟩ := hab
      exact ⟨i.symm⟩

/-- **matched_symm.**  Class-matching is symmetric. -/
theorem matched_symm {base base' : Regime} {h h' : List Event}
    (hm : Matched base h base' h') : Matched base' h' base h :=
  fun k => related_symm (hm k)

/-- **related_some_left.**  A related reading of a reached regime reaches
an isomorphic regime. -/
theorem related_some_left {r : Regime} {b : Option Regime}
    (hab : Related (some r) b) : ∃ s, b = some s ∧ Nonempty (Iso r s) := by
  cases b with
  | none => exact absurd hab (by simp [Related])
  | some s => exact ⟨s, rfl, hab⟩

/-- **first_demand_transport.**  Under a uniform stake, a first count of
one history is a first count of any class-matched history. -/
theorem first_demand_transport {S : Stake} (hu : Uniform S)
    {base base' : Regime} {h h' : List Event}
    (hm : Matched base h base' h') {k : Nat}
    (hf : IsFirstDemand S base h k) : IsFirstDemand S base' h' k := by
  obtain ⟨⟨r, hr, hd⟩, hq⟩ := hf
  refine ⟨?_, ?_⟩
  · have hk := hm k
    rw [hr] at hk
    obtain ⟨s, hs, ⟨iso⟩⟩ := related_some_left hk
    exact ⟨s, hs, hasDemand_transport_of_uniform hu iso hd⟩
  · intro m hmk s hs hds
    have hk := related_symm (hm m)
    rw [hs] at hk
    obtain ⟨r', hr', ⟨iso⟩⟩ := related_some_left hk
    exact hq m hmk r' hr' (hasDemand_transport_of_uniform hu iso hds)

/-- **first_demand_matched_of_uniform.**  In the sealed grammar
reconstructed here, extended by a declared two-sided stake that is
uniform: two class-matched histories, from any two bases, have exactly
the same first counts.  No decidability hypothesis, and no hypothesis on
the bases or on the events. -/
theorem first_demand_matched_of_uniform {S : Stake} (hu : Uniform S)
    {base base' : Regime} {h h' : List Event}
    (hm : Matched base h base' h') (k : Nat) :
    IsFirstDemand S base h k ↔ IsFirstDemand S base' h' k :=
  ⟨first_demand_transport hu hm, first_demand_transport hu (matched_symm hm)⟩

/-! ## 2. Renaming the token a supply carries -/

/-- Rename the token of every supply by `g`, leaving every other event
as it is. -/
def renameSupply (g : Nat → Nat) : Event → Event
  | .supply t => .supply (g t)
  | e => e

/-- **stepE_renameSupply.**  AT THE LEVEL OF A DEFINITION: a supply steps
to its regime whatever its token, and no other event is touched. -/
theorem stepE_renameSupply (g : Nat → Nat) (r : Regime) (e : Event) :
    stepE r (renameSupply g e) = stepE r e := by
  cases e <;> rfl

/-- **replayE_renameSupply.**  A history with its supply tokens renamed
replays to what the history replays to, from every base. -/
theorem replayE_renameSupply (g : Nat → Nat) :
    ∀ (h : List Event) (base : Regime),
      replayE (h.map (renameSupply g)) base = replayE h base := by
  intro h
  induction h with
  | nil => intro base; rfl
  | cons e rest ih =>
    intro base
    show (renameSupply g e :: rest.map (renameSupply g)).foldlM stepE base =
      (e :: rest).foldlM stepE base
    simp only [List.foldlM_cons, stepE_renameSupply]
    cases stepE base e with
    | none => rfl
    | some r => exact ih r

/-- **stateAt_renameSupply.**  Every prefix of the renamed history reaches
what the same prefix of the history reaches. -/
theorem stateAt_renameSupply (g : Nat → Nat) (h : List Event)
    (base : Regime) (k : Nat) :
    stateAt (h.map (renameSupply g)) base k = stateAt h base k := by
  unfold stateAt
  rw [← List.map_take]
  exact replayE_renameSupply g (h.take k) base

/-- **first_demand_renameSupply.**  In the sealed grammar reconstructed
here, extended by any declared two-sided stake: renaming the token every
supply of a history carries moves no first count. -/
theorem first_demand_renameSupply (S : Stake) (g : Nat → Nat)
    (base : Regime) (h : List Event) (k : Nat) :
    IsFirstDemand S base (h.map (renameSupply g)) k ↔ IsFirstDemand S base h k := by
  unfold IsFirstDemand
  simp only [stateAt_renameSupply]

end Trajectory
end SecondIso
