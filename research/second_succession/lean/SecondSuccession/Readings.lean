import SecondSuccession.Count

/-!
# Which readings give a count the regime carries

Native to rung six.

* `every_splits`, `admitting_splits`: from the sealed empty regime, two
  histories reaching one regime with different counts under EVERY and
  under ADMITTING.  Both by kernel computation on concrete histories, so
  at the level of a definition.
* `every_not_given_base`, `admitting_not_given_base`: hence no function
  of the base and the regime gives either count.
* `base_matters`: the sealed reading-L regime is reached from the empty
  regime by the sealed reading-L history with CHANGING count three, and
  from itself by the empty history with count zero.
* `changing_not_of_regime`: hence no function of the regime alone gives
  the CHANGING count, across bases.  With the base named it does
  (`changes_given_base`), and from the empty regime no naming is needed
  (`changes_from_genesis`).

AuthorityEffect: None.
-/

namespace SecondSuccession
namespace Readings

open Sealed Count

theorem every_splits :
    replayE [] genesis = some genesis ∧
      replayE [.supply 0] genesis = some genesis ∧
      ([] : List Event).length ≠ [Event.supply 0].length := by
  decide

theorem admitting_splits :
    replayE [.admitForm 1, .admitRuleAll 0] genesis = some ⟨0, [1], [], [0], []⟩ ∧
      replayE [.admitForm 1, .admitRuleAll 0, .admitRuleAll 0] genesis
        = some ⟨0, [1], [], [0], []⟩ ∧
      admitting [.admitForm 1, .admitRuleAll 0] = 2 ∧
      admitting [.admitForm 1, .admitRuleAll 0, .admitRuleAll 0] = 3 := by
  decide

theorem base_matters :
    replayE
        [.supply 0, .supply 1, .supply 1, .supply 2,
         .admitDatum, .admitDatum, .impose 0 1] genesis = some R2L ∧
      replayE [] R2L = some R2L ∧
      changes genesis
        [.supply 0, .supply 1, .supply 1, .supply 2,
         .admitDatum, .admitDatum, .impose 0 1] = 3 ∧
      changes R2L [] = 0 :=
  ⟨historyL_replays, rfl, by decide, rfl⟩

theorem every_not_given_base :
    ¬ ∃ F : Regime → Regime → Nat, ∀ (h : List Event) (b r : Regime),
      replayE h b = some r → h.length = F b r := by
  rintro ⟨F, hF⟩
  have h0 : 0 = F genesis genesis := hF [] genesis genesis every_splits.1
  have h1 : 1 = F genesis genesis := hF [.supply 0] genesis genesis every_splits.2.1
  omega

theorem admitting_not_given_base :
    ¬ ∃ F : Regime → Regime → Nat, ∀ (h : List Event) (b r : Regime),
      replayE h b = some r → admitting h = F b r := by
  rintro ⟨F, hF⟩
  obtain ⟨h2, h3, c2, c3⟩ := admitting_splits
  have a := hF _ genesis _ h2
  have b := hF _ genesis _ h3
  rw [c2] at a
  rw [c3] at b
  omega

theorem changing_not_of_regime :
    ¬ ∃ F : Regime → Nat, ∀ (h : List Event) (b r : Regime),
      replayE h b = some r → changes b h = F r := by
  rintro ⟨F, hF⟩
  obtain ⟨hL, h0, c3, c0⟩ := base_matters
  have a := hF _ genesis R2L hL
  have b := hF [] R2L R2L h0
  rw [c3] at a
  rw [c0] at b
  omega

end Readings
end SecondSuccession
