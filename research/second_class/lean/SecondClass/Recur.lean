import SecondClass.Kernel
import SecondClass.IsoKernel
import SecondClass.Rounds
import SecondClass.Count
import SecondClass.Clean

/-!
# No return to a class, recurrence only as a stutter, counts of a class

Native to rung eight.

Every statement here is over histories of the sealed step replayed from a
CLEAN base: well formed in the sealed sense and duplicate-free.  The
sealed empty regime and the two sealed reading regimes are clean
(`Clean.genesis_clean`, `Clean.R2L_clean`, `Clean.R2F_clean`), and
cleanness is kept by every event (`Clean.clean_replay`).  So the element
count of every regime reached is carried across the sealed isomorphism
(`Count.size_iso`).

* `no_return_class`: if the first event changes the regime, no regime the
  rest of the history reaches is isomorphic to the base.  Rung five's
  `no_return` said this of the regime; here it is said of the class.
* `recurrence_is_stutter`: if the regime reached after a whole history is
  isomorphic to the regime reached after a first part of it, the two
  regimes are EQUAL, and the rest of the history has CHANGING count zero.
* `counts_of_class`: two histories from one clean base that reach
  isomorphic regimes have one CHANGING count, one number of growths and
  one number of rest rounds.  `counts_of_class_genesis`: in particular
  from the sealed empty regime.

That the answer changes across two bases is `Counter.counts_not_of_class`.

AuthorityEffect: None.
-/

namespace SecondClass
namespace Recur

open Sealed
open Rounds
open Count (Clean size_iso components_iso)
open Clean (clean_step clean_replay genesis_clean)

/-- From a clean base, after a changing first event, no regime reached is
isomorphic to the base. -/
theorem no_return_class {b b' r : Regime} {e : Event} {h : List Event}
    (hb : Clean b) (hs : stepE b e = some b') (hch : b' ≠ b)
    (hr : replayE h b' = some r) (σ : Iso r b) : False := by
  have hb' : Clean b' := clean_step hb hs
  have hc : Clean r := clean_replay h b' r hb' hr
  have h1 : size r = size b := size_iso hc hb σ
  have h2 : size b' = size b + 1 := by
    rcases step_parts hs with heq | ⟨_, hsz⟩ | ⟨_, hsz⟩
    · exact absurd heq hch
    · exact hsz
    · exact hsz
  have h3 := changes_counted h b' r hr
  omega

/-- From a clean base, a regime reached after a whole history that is
isomorphic to the regime reached after a first part of it is that very
regime, and the rest of the history changes nothing. -/
theorem recurrence_is_stutter {b r₁ r₂ : Regime} (h₁ h₂ : List Event)
    (hb : Clean b) (hr₁ : replayE h₁ b = some r₁)
    (hr₂ : replayE (h₁ ++ h₂) b = some r₂) (σ : Iso r₂ r₁) :
    r₂ = r₁ ∧ changes r₁ h₂ = 0 := by
  rw [replayE_split, hr₁] at hr₂
  have h2 : replayE h₂ r₁ = some r₂ := hr₂
  have hc₁ : Clean r₁ := clean_replay h₁ b r₁ hb hr₁
  have hc₂ : Clean r₂ := clean_replay h₂ r₁ r₂ hc₁ h2
  have hsz : size r₂ = size r₁ := size_iso hc₂ hc₁ σ
  have hcount := changes_counted h₂ r₁ r₂ h2
  have hz : changes r₁ h₂ = 0 := by omega
  exact ⟨still_of_no_changes h₂ r₁ r₂ h2 hz, hz⟩

/-- From one clean base, two histories reaching isomorphic regimes have
one CHANGING count, one number of growths and one number of rest
rounds. -/
theorem counts_of_class {b r r' : Regime} {h h' : List Event} (hb : Clean b)
    (hr : replayE h b = some r) (hr' : replayE h' b = some r')
    (σ : Iso r r') :
    changes b h = changes b h' ∧ growths b h = growths b h' ∧
      rest b h = rest b h' := by
  have hc : Clean r := clean_replay h b r hb hr
  have hc' : Clean r' := clean_replay h' b r' hb hr'
  have hsz : size r = size r' := size_iso hc hc' σ
  have hd : r.data = r'.data := (components_iso hc hc' σ).1
  have c1 := changes_counted h b r hr
  have c2 := changes_counted h' b r' hr'
  have g1 := growths_counted h b r hr
  have g2 := growths_counted h' b r' hr'
  have s1 := rest_counted h b r hr
  have s2 := rest_counted h' b r' hr'
  refine ⟨?_, ?_, ?_⟩ <;> omega

/-- From the sealed empty regime, the three counts are carried by the
class of the regime reached. -/
theorem counts_of_class_genesis {r r' : Regime} {h h' : List Event}
    (hr : replayE h genesis = some r) (hr' : replayE h' genesis = some r')
    (σ : Iso r r') :
    changes genesis h = changes genesis h' ∧
      growths genesis h = growths genesis h' ∧
      rest genesis h = rest genesis h' :=
  counts_of_class genesis_clean hr hr' σ

end Recur
end SecondClass
