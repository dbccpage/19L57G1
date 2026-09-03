import DescribedReplay.Reproduction

namespace DescribedReplay

def reachesTerminal (history : List Event) : Bool :=
  !(replayTotal history).data.isEmpty

def resultReports : Option Regime → Bool
  | none => false
  | some regime => decide (Datum.b ∈ regime.data)

def candidateReport (history : List Event) : Bool :=
  resultReports (replay history)

theorem candidate_report_uses_described_replay (candidate target : List Event)
    (hcandidate : member candidate = true) (htarget : member target = true) :
    candidateReplay candidate (encode target) = replay candidate ∧
      resultReports (candidateReplay candidate (encode target)) =
        candidateReport candidate := by
  have hrun : candidateReplay candidate (encode target) = replay candidate := by
    simp [candidateReplay, hcandidate, decode_encode_id target htarget]
  exact ⟨hrun, by rw [hrun]; rfl⟩

def reportDiagonal (candidate : List Event) : List Event :=
  if candidateReport candidate then [] else [.addA]

def describedCost (history : List Event) : Nat :=
  history.length + (encode history).data.length

def reportCost (candidate target : List Event) : Nat :=
  candidate.length + (encode target).data.length

theorem bounded_reporter_diagonal_member (candidate : List Event)
    (hcandidate : member candidate = true) :
    member (reportDiagonal candidate) = true ∧
      reportCost candidate (reportDiagonal candidate) ≤ 6 := by
  have hlength : candidate.length ≤ 3 := by
    have hbound := hcandidate
    simp [member] at hbound
    exact hbound.1
  constructor
  · unfold reportDiagonal
    split <;> decide
  · unfold reportDiagonal
    split <;> simp [reportCost, encode, encodeTokens, encodeTokensFrom] <;> omega

theorem diagonal_disagrees (candidate : List Event) :
    candidateReport candidate ≠ reachesTerminal (reportDiagonal candidate) := by
  cases hreport : candidateReport candidate with
  | false =>
      simp [reportDiagonal, hreport, reachesTerminal, replayTotal,
        replayTotalFrom, applyEvent, appendFresh, emptyRegime]
  | true =>
      simp [reportDiagonal, hreport, reachesTerminal, replayTotal,
        replayTotalFrom, emptyRegime]

theorem no_fixed_candidate_reporter :
    ¬ ∃ candidate : List Event,
      member candidate = true ∧
        ∀ target : List Event, member target = true →
          candidateReport candidate = reachesTerminal target := by
  rintro ⟨candidate, hcandidate, hall⟩
  have hagree := hall (reportDiagonal candidate)
    (bounded_reporter_diagonal_member candidate hcandidate).1
  exact diagonal_disagrees candidate hagree

def outsideReporter (description : DescriptionRegime) : Bool :=
  match decode description with
  | none => false
  | some history => reachesTerminal history

theorem outside_reporter_correct (history : List Event)
    (hmember : member history = true) :
    outsideReporter (encode history) = reachesTerminal history := by
  simp [outsideReporter, decode_encode_id history hmember]

end DescribedReplay
