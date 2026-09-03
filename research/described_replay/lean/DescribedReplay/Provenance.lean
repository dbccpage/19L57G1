import DescribedReplay.Reporting

namespace DescribedReplay

structure ReconstructionNote where
  declaration : String
  pinnedSource : String
  reconstruction : String
deriving DecidableEq, Repr

def kernelSnapshot : String :=
  "f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be"

def kernelModelBlob : String :=
  "b6f95a673853d423a0d73b4faa95b2cd22f306a3"

def kernelSource : String :=
  "code/derivation/model.py@b6f95a673853d423a0d73b4faa95b2cd22f306a3"

def kernelReconstructionNotes : List ReconstructionNote := [
  ⟨"Datum", kernelSource, "Regime.data projected to the declared a,b alphabet"⟩,
  ⟨"Event", kernelSource, "Event projected to the declared ordered nine-symbol alphabet"⟩,
  ⟨"Regime", kernelSource, "Regime projected to unary form zero and the two fixed instances"⟩,
  ⟨"emptyRegime", kernelSource, "EMPTY reconstructed field by field"⟩,
  ⟨"appendFresh", kernelSource, "datum designation keeps an existing token and appends a fresh token"⟩,
  ⟨"eventValid", kernelSource, "one-event range and arity guards reconstructed as a Boolean check"⟩,
  ⟨"applyEvent", kernelSource, "the six event families reconstructed on the finite projection"⟩,
  ⟨"transition", kernelSource, "the one-event check returns none exactly when a guard fails"⟩,
  ⟨"replayFrom", kernelSource, "left-to-right guarded event fold from a supplied base"⟩,
  ⟨"replay", kernelSource, "guarded event fold from emptyRegime"⟩,
  ⟨"replayTotalFrom", kernelSource, "unguarded fold used only after local validation"⟩,
  ⟨"replayTotal", kernelSource, "unguarded fold from emptyRegime used only after local validation"⟩,
  ⟨"wellFormedFrom", kernelSource, "every prefix guard checked in event order"⟩,
  ⟨"wellFormed", kernelSource, "prefix guard check from emptyRegime"⟩,
  ⟨"member", "PREDICTIONS.md@3c78da7af6d25296d34020eb5e6579070ad4e8dc529ef415b375a19f6bd1f204",
    "wellFormed conjoined with the declared length bound three"⟩
]

def reconstructedKernelDefinitionNames : List String := [
  "Datum", "Event", "Regime", "emptyRegime", "appendFresh", "eventValid",
  "applyEvent", "transition", "replayFrom", "replay", "replayTotalFrom",
  "replayTotal", "wellFormedFrom", "wellFormed", "member"
]

theorem reconstruction_notes_cover_kernel_definitions :
    kernelReconstructionNotes.map ReconstructionNote.declaration =
      reconstructedKernelDefinitionNames := by
  rfl

def localPolicySource : String :=
  "PREDICTIONS.md@3c78da7af6d25296d34020eb5e6579070ad4e8dc529ef415b375a19f6bd1f204"

def localReconstructionNotes : List ReconstructionNote := [
  ⟨"CodeToken", localPolicySource, "position and event fields implement the frozen token shape"⟩,
  ⟨"DescriptionToken", localPolicySource, "ordinary and coded tokens keep class membership distinct from coding"⟩,
  ⟨"DescriptionRegime", localPolicySource, "the five frozen regime fields are reconstructed for descriptions"⟩,
  ⟨"DescriptionEvent", localPolicySource, "description changes distinguish datum admission from other event kinds"⟩,
  ⟨"encodeTokensFrom", localPolicySource, "each position and event is encoded by one fresh coded token"⟩,
  ⟨"encodeTokens", localPolicySource, "description positions begin at zero"⟩,
  ⟨"encode", localPolicySource, "coding admits only tokens and leaves all other fields empty"⟩,
  ⟨"eventOfDescriptionToken", localPolicySource, "coded tokens project to their recorded event"⟩,
  ⟨"rawHistory", localPolicySource, "the raw event list is the token projection in order"⟩,
  ⟨"decode", localPolicySource, "decoding requires canonical encoding and declared-class membership"⟩,
  ⟨"descriptionHistory", localPolicySource, "one datum-admission event is charged per coded token"⟩,
  ⟨"descriptionAdmissionOnly", localPolicySource, "the coding history excludes supply and imposition"⟩,
  ⟨"classEventOfDescriptionToken", localPolicySource, "ordinary tokens alone denote class events"⟩,
  ⟨"classHistory", localPolicySource, "ordinary description tokens are decoded in order"⟩,
  ⟨"descriptionClean", localPolicySource, "non-data description fields must remain empty"⟩,
  ⟨"descriptionClassMember", localPolicySource, "description histories are checked against the declared class"⟩,
  ⟨"eventAt", localPolicySource, "the costed step reads only the event at the current pointer"⟩,
  ⟨"prefixFoldFrom", localPolicySource, "proof-only prefix fold states the agreement invariant"⟩,
  ⟨"prefixState", localPolicySource, "proof-only prefix state starts at the empty regime"⟩,
  ⟨"stateTraceFrom", localPolicySource, "preparation caches every expected current regime outside the costed step"⟩,
  ⟨"stateTrace", localPolicySource, "the cached trace begins at the empty regime"⟩,
  ⟨"PreparedDescription", localPolicySource, "a separate witness binds decoding, class membership, and cached states"⟩,
  ⟨"prepare", localPolicySource, "description validation and trace construction occur once before stepping"⟩,
  ⟨"preparedEncode", localPolicySource, "a known class history constructs its validated witness"⟩,
  ⟨"DescribedState", localPolicySource, "the frozen runtime state is description, pointer, and current regime"⟩,
  ⟨"StepResult", localPolicySource, "the result alternatives are stepped, done, and invalid"⟩,
  ⟨"stepper", localPolicySource, "cached alignment is checked before one reconstructed transition"⟩,
  ⟨"preparationDispatcher", localPolicySource, "the one-time metatheoretic dispatcher maps failed preparation to invalid"⟩,
  ⟨"runSteps", localPolicySource, "iteration repeats the one-event step without revalidation"⟩,
  ⟨"initialState", localPolicySource, "a prepared run begins at pointer zero and the empty regime"⟩,
  ⟨"completedState", localPolicySource, "the proved terminal state records the full endpoint"⟩,
  ⟨"candidateReplay", localPolicySource, "a fixed member ignores decoded target contents after validation"⟩,
  ⟨"ReplaysDeclaredClass", localPolicySource, "class-wide reproduction quantifies over every declared target"⟩,
  ⟨"reachesTerminal", localPolicySource, "the frozen terminal predicate is nonempty admitted data"⟩,
  ⟨"resultReports", localPolicySource, "the candidate report tests for datum b in a successful result"⟩,
  ⟨"candidateReport", localPolicySource, "a candidate reports from its own fixed endpoint"⟩,
  ⟨"reportDiagonal", localPolicySource, "the selected empty-or-add-a member opposes a fixed report"⟩,
  ⟨"describedCost", localPolicySource, "outside reporting charges target steps and target admissions"⟩,
  ⟨"reportCost", localPolicySource, "fixed-candidate interaction charges candidate steps and target admissions"⟩,
  ⟨"outsideReporter", localPolicySource, "the outside reporter validates and then applies the terminal predicate"⟩
]

def reconstructedLocalDefinitionNames : List String := [
  "CodeToken", "DescriptionToken", "DescriptionRegime", "DescriptionEvent",
  "encodeTokensFrom", "encodeTokens", "encode", "eventOfDescriptionToken",
  "rawHistory", "decode", "descriptionHistory", "descriptionAdmissionOnly",
  "classEventOfDescriptionToken", "classHistory", "descriptionClean",
  "descriptionClassMember", "eventAt", "prefixFoldFrom", "prefixState",
  "stateTraceFrom", "stateTrace", "PreparedDescription", "prepare",
  "preparedEncode", "DescribedState", "StepResult", "stepper", "preparationDispatcher",
  "runSteps", "initialState", "completedState", "candidateReplay", "ReplaysDeclaredClass",
  "reachesTerminal", "resultReports", "candidateReport", "reportDiagonal",
  "describedCost", "reportCost", "outsideReporter"
]

theorem reconstruction_notes_cover_local_definitions :
    localReconstructionNotes.map ReconstructionNote.declaration =
      reconstructedLocalDefinitionNames := by
  rfl

end DescribedReplay
