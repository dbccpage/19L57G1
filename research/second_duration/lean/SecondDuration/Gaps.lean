import SecondDuration.Rounds

/-!
# Which durations the regime carries

Native to rung seven.

* `lead_splits`: from the sealed empty regime, a form then a datum, and a
  datum then the form, reach one regime with segment zero one and zero.
  By kernel computation, so at the level of a definition.
* `segment_not_given_base`: hence no function of a position, a base and a
  regime gives the rest rounds taken at that position.
* `gap_splits`: from the sealed empty regime, a datum, a form, a datum;
  and a datum, a datum, the form, reach one regime with the duration
  between the first and the second growth one and zero.  By kernel
  computation.
* `gap_not_from_genesis`: hence no function of the regime alone gives
  that duration, even over histories from the sealed empty regime.
* `tail_forced`: when the base names nothing at or above `t` and the
  regime reached has as many instances and requirements naming `t` or
  later as the history has rest rounds, every rest round is taken after
  the regime has more than `t` data.
* `pinned_by_requirement`: every history from the sealed empty regime
  reaching the regime with two data and the one requirement between them
  takes exactly one rest round, after the second growth.

Nothing here states which vectors some history attains: that the vectors
reached are exactly the ones the lower bounds allow is a finite
computation of this rung, and is not proved.

AuthorityEffect: None.
-/

namespace SecondDuration
namespace Gaps

open Sealed Rounds

theorem lead_splits :
    replayE [.admitForm 1, .admitDatum] genesis = some ⟨1, [1], [], [], []⟩ ∧
      replayE [.admitDatum, .admitForm 1] genesis = some ⟨1, [1], [], [], []⟩ ∧
      during 0 genesis [.admitForm 1, .admitDatum] = 1 ∧
      during 0 genesis [.admitDatum, .admitForm 1] = 0 := by
  decide

theorem segment_not_given_base :
    ¬ ∃ F : Nat → Regime → Regime → Nat, ∀ (n : Nat) (h : List Event) (b r : Regime),
      replayE h b = some r → during n b h = F n b r := by
  rintro ⟨F, hF⟩
  obtain ⟨h1, h2, c1, c2⟩ := lead_splits
  have a := hF 0 _ genesis _ h1
  have b := hF 0 _ genesis _ h2
  rw [c1] at a
  rw [c2] at b
  omega

theorem gap_splits :
    replayE [.admitDatum, .admitForm 1, .admitDatum] genesis = some ⟨2, [1], [], [], []⟩ ∧
      replayE [.admitDatum, .admitDatum, .admitForm 1] genesis = some ⟨2, [1], [], [], []⟩ ∧
      during 1 genesis [.admitDatum, .admitForm 1, .admitDatum] = 1 ∧
      during 1 genesis [.admitDatum, .admitDatum, .admitForm 1] = 0 := by
  decide

theorem gap_not_from_genesis :
    ¬ ∃ F : Regime → Nat, ∀ (h : List Event) (r : Regime),
      replayE h genesis = some r → during 1 genesis h = F r := by
  rintro ⟨F, hF⟩
  obtain ⟨h1, h2, c1, c2⟩ := gap_splits
  have a := hF _ _ h1
  have b := hF _ _ h2
  rw [c1] at a
  rw [c2] at b
  omega

theorem tail_forced {t : Nat} {h : List Event} {b r : Regime}
    (hr : replayE h b = some r) (hb : naming t b = 0)
    (hn : naming t r = rest b h) : after t b h = rest b h := by
  have h1 := naming_bounded t h b r hr
  have h2 := after_le_rest t h b
  omega

theorem pinned_by_requirement (h : List Event)
    (hr : replayE h genesis = some ⟨2, [], [], [], [(0, 1)]⟩) :
    rest genesis h = 1 ∧ after 1 genesis h = 1 := by
  have hg := growths_counted h genesis _ hr
  have hs := rest_counted h genesis _ hr
  have hsz : size ⟨2, [], [], [], [(0, 1)]⟩ = 3 := rfl
  have h0 : size genesis = 0 := rfl
  have hd : genesis.data = 0 := rfl
  have hone : rest genesis h = 1 := by
    simp only at hg
    omega
  refine ⟨hone, ?_⟩
  have hn : naming 1 ⟨2, [], [], [], [(0, 1)]⟩ = rest genesis h := by
    rw [hone]
    decide
  rw [tail_forced hr (by decide) hn, hone]

end Gaps
end SecondDuration
