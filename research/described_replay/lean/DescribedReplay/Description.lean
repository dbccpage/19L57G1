import DescribedReplay.Core

namespace DescribedReplay

structure CodeToken where
  position : Nat
  event : Event
deriving DecidableEq, Repr

inductive DescriptionToken where
  | ordinary (token : Datum)
  | code (token : CodeToken)
deriving DecidableEq, Repr

structure DescriptionRegime where
  data : List DescriptionToken
  forms : List Nat
  instances : List (Nat × Nat)
  rules : List Nat
  requirements : List (Nat × Nat)
deriving DecidableEq, Repr

inductive DescriptionEvent where
  | addDatum (token : DescriptionToken)
  | addForm
  | addInstance
  | addRule
  | supply
  | impose
deriving DecidableEq, Repr

def encodeTokensFrom : Nat → List Event → List DescriptionToken
  | _, [] => []
  | position, event :: rest =>
      .code { position := position, event := event } ::
        encodeTokensFrom (position + 1) rest

def encodeTokens (history : List Event) : List DescriptionToken :=
  encodeTokensFrom 0 history

def encode (history : List Event) : DescriptionRegime :=
  { data := encodeTokens history, forms := [], instances := [], rules := [],
    requirements := [] }

def eventOfDescriptionToken : DescriptionToken → Event
  | .ordinary .a => .addA
  | .ordinary .b => .addB
  | .code token => token.event

def rawHistory (description : DescriptionRegime) : List Event :=
  description.data.map eventOfDescriptionToken

theorem events_encodeTokensFrom (position : Nat) (history : List Event) :
    (encodeTokensFrom position history).map eventOfDescriptionToken = history := by
  induction history generalizing position with
  | nil => rfl
  | cons event rest ih =>
      simp [encodeTokensFrom, eventOfDescriptionToken, ih]

theorem rawHistory_encode (history : List Event) :
    rawHistory (encode history) = history := by
  exact events_encodeTokensFrom 0 history

def decode (description : DescriptionRegime) : Option (List Event) :=
  let history := rawHistory description
  if description = encode history ∧ member history = true then some history else none

theorem decode_encode_id (history : List Event) (hmember : member history = true) :
    decode (encode history) = some history := by
  simp [decode, rawHistory_encode, hmember]

theorem encode_injective : Function.Injective encode := by
  intro left right hequal
  have hraw := congrArg rawHistory hequal
  simpa [rawHistory_encode] using hraw

def descriptionHistory (history : List Event) : List DescriptionEvent :=
  (encodeTokens history).map DescriptionEvent.addDatum

def descriptionAdmissionOnly : DescriptionEvent → Prop
  | .addDatum _ => True
  | .addForm => True
  | .addInstance => True
  | .addRule => True
  | .supply => False
  | .impose => False

theorem encode_admission_only (history : List Event) :
    ∀ event ∈ descriptionHistory history, descriptionAdmissionOnly event := by
  intro event hevent
  obtain ⟨token, _, rfl⟩ := List.mem_map.mp hevent
  trivial

theorem decoder_domain_iff (description : DescriptionRegime) (history : List Event) :
    decode description = some history ↔
      description = encode history ∧ member history = true := by
  unfold decode
  dsimp only
  split
  · rename_i hdomain
    constructor
    · intro hequal
      have hhistory : rawHistory description = history := Option.some.inj hequal
      subst history
      exact hdomain
    · rintro ⟨hdescription, hmember⟩
      have hencoded : encode (rawHistory description) = encode history :=
        hdomain.1.symm.trans hdescription
      have hhistory : rawHistory description = history := encode_injective hencoded
      exact congrArg some hhistory
  · rename_i houtside
    constructor
    · intro hequal
      cases hequal
    · rintro ⟨hdescription, hmember⟩
      have hhistory : rawHistory description = history := by
        rw [hdescription, rawHistory_encode]
      have hcanonical : description = encode (rawHistory description) := by
        simpa [hhistory] using hdescription
      have hrawMember : member (rawHistory description) = true := by
        simpa [hhistory] using hmember
      exact False.elim (houtside ⟨hcanonical, hrawMember⟩)

theorem endpoint_insufficient :
    member [] = true ∧
      member [.supplyA] = true ∧
      ([] : List Event) ≠ [.supplyA] ∧
      encode [] ≠ encode [.supplyA] ∧
      replay [] = replay [.supplyA] := by
  decide

def classEventOfDescriptionToken : DescriptionToken → Option Event
  | .ordinary .a => some .addA
  | .ordinary .b => some .addB
  | .code _ => none

def classHistory : List DescriptionToken → Option (List Event)
  | [] => some []
  | token :: rest =>
      match classEventOfDescriptionToken token, classHistory rest with
      | some event, some history => some (event :: history)
      | _, _ => none

def descriptionClean (description : DescriptionRegime) : Bool :=
  description.forms.isEmpty && description.instances.isEmpty &&
    description.rules.isEmpty && description.requirements.isEmpty

def descriptionClassMember (description : DescriptionRegime) : Bool :=
  descriptionClean description &&
    match classHistory description.data with
    | none => false
    | some history => member history

theorem empty_self_description_witness :
    decode (encode []) = some [] ∧ descriptionClassMember (encode []) = true := by
  decide

theorem nonempty_description_outside_class (event : Event) (rest : List Event) :
    descriptionClassMember (encode (event :: rest)) = false := by
  rfl

end DescribedReplay
