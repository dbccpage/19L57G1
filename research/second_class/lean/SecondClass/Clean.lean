import SecondClass.Kernel
import SecondClass.Rounds
import SecondClass.Count

/-!
# Every event of the sealed step keeps a regime clean

Native to rung eight.

A regime is CLEAN when it is well formed in the sealed sense and its lists
of instances, uniform rules and requirements each hold no entry twice
(`Count.Clean`).  The sealed well-formedness predicate does not forbid a
repeated entry; the sealed step never adds one, because it inserts
through the deduplicating `insertNew`.

* `nodup_insertNew`: deduplicating insertion keeps a list free of
  repeated entries.
* `clean_step`: for every clean regime and every event of the six kinds
  that the sealed step accepts, the regime after is clean.
* `clean_replay`: so every regime a history reaches from a clean base is
  clean.
* `genesis_clean`, `R2L_clean`, `R2F_clean`: the sealed empty regime and
  the two sealed reading regimes are clean, by kernel computation.

`getD_append_lt` repeats, as a statement, rung five's lemma of the same
name; it is proved again here so that this package imports nothing.

AuthorityEffect: None.
-/

namespace SecondClass
namespace Clean

open Sealed
open Rounds (replayE_cons)
open Count (Clean Dupfree)

/-- Deduplicating insertion keeps a list free of repeated entries. -/
theorem nodup_insertNew {α : Type} [DecidableEq α] {l : List α} (a : α)
    (h : l.Nodup) : (insertNew l a).Nodup := by
  by_cases ha : a ∈ l
  · rw [insertNew_of_mem ha]
    exact h
  · rw [insertNew_of_not_mem ha, List.nodup_append]
    refine ⟨h, List.pairwise_singleton _ a, ?_⟩
    intro x hx y hy hxy
    rw [List.mem_singleton] at hy
    rw [hxy, hy] at hx
    exact ha hx

/-- Reading a list extended at its end, at an index inside the list
(rung five's statement). -/
theorem getD_append_lt (l : List Nat) (a : Nat) {i : Nat} (h : i < l.length) :
    (l ++ [a]).getD i 0 = l.getD i 0 := by
  induction l generalizing i with
  | nil => exact absurd h (Nat.not_lt_zero i)
  | cons x xs ih =>
    cases i with
    | zero => rfl
    | succ k =>
      have hk : k < xs.length := Nat.lt_of_succ_lt_succ h
      exact ih hk

/-- Every event the sealed step accepts keeps a clean regime clean. -/
theorem clean_step {r r' : Regime} {e : Event} (hc : Clean r)
    (h : stepE r e = some r') : Clean r' := by
  obtain ⟨⟨hi, hru, hrq, hfo⟩, hni, hnr, hnq⟩ := hc
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact ⟨⟨hi, hru, hrq, hfo⟩, hni, hnr, hnq⟩
  | admitDatum =>
    cases Option.some.inj h
    refine ⟨⟨?_, hru, ?_, hfo⟩, hni, hnr, hnq⟩
    · intro p hp
      obtain ⟨h1, h2, h3⟩ := hi p hp
      exact ⟨h1, h2, fun a ha => Nat.lt_succ_of_lt (h3 a ha)⟩
    · intro q hq
      obtain ⟨h1, h2⟩ := hrq q hq
      exact ⟨h1, Nat.lt_succ_of_lt h2⟩
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · rename_i ha
      cases Option.some.inj h
      have hlen : (r.forms ++ [a]).length = r.forms.length + 1 := by
        rw [List.length_append]
        rfl
      refine ⟨⟨?_, ?_, hrq, ?_⟩, hni, hnr, hnq⟩
      · intro p hp
        obtain ⟨h1, h2, h3⟩ := hi p hp
        refine ⟨?_, ?_, h3⟩
        · show p.1 < (r.forms ++ [a]).length
          rw [hlen]
          exact Nat.lt_succ_of_lt h1
        · show p.2.length = (r.forms ++ [a]).getD p.1 0
          rw [getD_append_lt r.forms a h1]
          exact h2
      · intro f hf
        show f < (r.forms ++ [a]).length
        rw [hlen]
        exact Nat.lt_succ_of_lt (hru f hf)
      · intro x hx
        rcases List.mem_append.mp hx with hx | hx
        · exact hfo x hx
        · rw [List.mem_singleton] at hx
          rw [hx]
          exact ha
    · cases h
  | admitInst f args =>
    simp only [stepE] at h
    split at h
    · rename_i hg
      cases Option.some.inj h
      refine ⟨⟨?_, hru, hrq, hfo⟩, nodup_insertNew _ hni, hnr, hnq⟩
      intro p hp
      rcases mem_insertNew.mp hp with hp | hp
      · exact hi p hp
      · rw [hp]
        exact hg
    · cases h
  | admitRuleAll f =>
    simp only [stepE] at h
    split at h
    · rename_i hg
      cases Option.some.inj h
      refine ⟨⟨hi, ?_, hrq, hfo⟩, hni, nodup_insertNew _ hnr, hnq⟩
      intro g hg'
      rcases mem_insertNew.mp hg' with hg' | hg'
      · exact hru g hg'
      · rw [hg']
        exact hg
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · rename_i hg
      cases Option.some.inj h
      refine ⟨⟨hi, hru, ?_, hfo⟩, hni, hnr, nodup_insertNew _ hnq⟩
      intro q hq
      rcases mem_insertNew.mp hq with hq | hq
      · exact hrq q hq
      · rw [hq]
        exact hg
    · cases h

/-- Every regime a history reaches from a clean base is clean. -/
theorem clean_replay (h : List Event) :
    ∀ b r : Regime, Clean b → replayE h b = some r → Clean r := by
  induction h with
  | nil =>
    intro b r hb hr
    rw [← Option.some.inj hr]
    exact hb
  | cons e es ih =>
    intro b r hb hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      exact ih b' r (clean_step hb hs) hr

theorem genesis_clean : Clean genesis := by
  refine ⟨⟨?_, ?_, ?_, ?_⟩, ?_, ?_, ?_⟩ <;> decide

theorem R2L_clean : Clean R2L := by
  refine ⟨⟨?_, ?_, ?_, ?_⟩, ?_, ?_, ?_⟩ <;> decide

theorem R2F_clean : Clean R2F := by
  refine ⟨⟨?_, ?_, ?_, ?_⟩, ?_, ?_, ?_⟩ <;> decide

end Clean
end SecondClass
