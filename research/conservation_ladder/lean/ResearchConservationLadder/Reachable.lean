import ResearchConservationLadder.Native

/-!
# No nontrivial charge on the reachable passage

AuthorityEffect: None.  CL-13 asked for a symmetry and a charge of the
sealed passage itself.  The charge side has a no-go, and it is sharp.

* `passage_charge_genesis`, `passage_charge_const`: a quantity preserved
  by every event takes its genesis value at every state reachable from
  genesis, so it is constant on the reachable passage.  No action, however
  it is proposed, generates a charge that separates two reachable states.
  This is `conserved_path` applied to the paths from genesis.
* `occDistinct_step`, `occDistinct_split`, `dupState_unreachable`: the
  no-go rests on reachability, not on the state space.  Whether the
  occurrence tokens are distinct is preserved by every event, holds at
  genesis, and fails at a state with a repeated token.  So a nontrivial
  conserved quantity exists on the passage's states, and that state is
  not reachable.

The symmetry side is not settled here: a native action that is not
declared stays open (NS-17 in `native_structure`).
-/

namespace ResearchConservationLadder

open PrimitivePassage ResearchNativeBridge

/-- A state is reachable when some event list replays genesis to it. -/
def Reachable (s : PState) : Prop := ∃ l : List PEvent, replayP l genesisP = s

/-- A quantity preserved by every event keeps its genesis value along every
event list from genesis. -/
theorem passage_charge_genesis {κ : Type} (Q : PState → κ)
    (h : ∀ s e, Q (step s e) = Q s) (l : List PEvent) :
    Q (replayP l genesisP) = Q genesisP :=
  conserved_path step Q h (Path.ofEvents step genesisP l)

/-- **No nontrivial charge on the reachable passage.** -/
theorem passage_charge_const {κ : Type} (Q : PState → κ)
    (h : ∀ s e, Q (step s e) = Q s) {s t : PState}
    (hs : Reachable s) (ht : Reachable t) : Q s = Q t := by
  obtain ⟨l, rfl⟩ := hs
  obtain ⟨m, rfl⟩ := ht
  rw [passage_charge_genesis Q h l, passage_charge_genesis Q h m]

/-- The occurrence field under a step: unchanged, or one fresh token
appended. -/
theorem step_occ (s : PState) (e : PEvent) :
    (step s e).occ = s.occ ∨ ∃ t, t ∉ s.occ ∧ (step s e).occ = s.occ ++ [t] := by
  cases e with
  | admitOcc t =>
      simp only [step]
      by_cases hh : s.halted = true
      · left; rw [if_pos hh]
      · rw [if_neg hh]
        by_cases ht : t ∈ s.occ
        · left; rw [if_pos ht]
        · right; rw [if_neg ht]; exact ⟨t, ht, rfl⟩
  | _ =>
      left
      simp only [step]
      repeat' split
      all_goals rfl

/-- Occurrence distinctness: no occurrence token repeats. -/
def occDistinct (s : PState) : Prop := s.occ.Nodup

/-- Distinctness is preserved by every event. -/
theorem occDistinct_step (s : PState) (e : PEvent) :
    occDistinct (step s e) = occDistinct s := by
  apply propext
  unfold occDistinct
  rcases step_occ s e with h | ⟨t, ht, h⟩
  · rw [h]
  · rw [h, List.nodup_append]
    constructor
    · exact fun hn => hn.1
    · intro hn
      refine ⟨hn, List.nodup_cons.2 ⟨List.not_mem_nil, List.nodup_nil⟩, ?_⟩
      intro a ha b hb heq
      rw [List.mem_singleton] at hb
      exact ht (hb ▸ heq ▸ ha)

/-- A state whose occurrence field repeats a token. -/
def dupState : PState := { genesisP with occ := [0, 0] }

/-- A nontrivial conserved quantity on the passage's states: it holds at
genesis and fails at `dupState`. -/
theorem occDistinct_split : occDistinct genesisP ∧ ¬ occDistinct dupState := by
  refine ⟨List.nodup_nil, fun h => ?_⟩
  have := (List.nodup_cons.1 h).1
  exact this (List.mem_singleton.2 rfl)

/-- So `dupState` is not reachable: the no-go is about reachability. -/
theorem dupState_unreachable : ¬ Reachable dupState := by
  intro hr
  have hg := passage_charge_const occDistinct occDistinct_step hr ⟨[], rfl⟩
  have hd : occDistinct dupState := hg ▸ occDistinct_split.1
  exact occDistinct_split.2 hd

end ResearchConservationLadder
