import DescribedReplay.Stepper

namespace DescribedReplay

def candidateReplay (candidate : List Event)
    (description : DescriptionRegime) : Option Regime :=
  if member candidate then
    match decode description with
    | none => none
    | some _ => replay candidate
  else none

def ReplaysDeclaredClass (candidate : List Event) : Prop :=
  ∀ target : List Event, member target = true →
    candidateReplay candidate (encode target) = replay target

theorem empty_self_replay_witness :
    member [] = true ∧
      descriptionClassMember (encode []) = true ∧
      candidateReplay [] (encode []) = replay [] := by
  decide

theorem fixed_candidate_no_class_replay (candidate : List Event)
    (hcandidate : member candidate = true) :
    ¬ ReplaysDeclaredClass candidate := by
  intro hclass
  have hall : candidateReplay candidate (encode []) = replay [] ∧
      candidateReplay candidate (encode [.addA]) = replay [.addA] :=
    ⟨hclass [] (by decide), hclass [.addA] (by decide)⟩
  have hempty : replay candidate = replay [] := by
    simpa [candidateReplay, hcandidate, decode_encode_id [] (by decide)] using hall.1
  have hadd : replay candidate = replay [.addA] := by
    simpa [candidateReplay, hcandidate, decode_encode_id [.addA] (by decide)] using hall.2
  have himpossible : replay [] = replay [.addA] := hempty.symm.trans hadd
  exact (by decide : replay [] ≠ replay [.addA]) himpossible

end DescribedReplay
