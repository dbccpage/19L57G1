import Derivation.Bridge
import AdmissionSignShadow.Core

/-!
# Exact frozen-pair facts and a chosen compatibility bridge

This module is compiled by `verify_frozen_compatibility.py` against the exact
frozen source tree at commit `3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`.
The frozen files are materialized only in an ephemeral build directory; they
are not copied into the post-seal research package. `encode` and
`sourceExchange` below are post-seal metatheoretic choices. The frozen source
proves endpoint distinction and erased equality, but supplies no exchange
operation and does not authorize either orientation of this equivalence.
-/

namespace AdmissionSignShadow
namespace FrozenPairBridge

open Derivation

def emptyT : TRegime := ⟨[], [], [], [], []⟩

def FrozenHistory :=
  { history : List TEvent // history = Bridge.hist01 ∨ history = Bridge.hist10 }

def encode : HistoryClass → FrozenHistory
  | .forward => ⟨Bridge.hist01, Or.inl rfl⟩
  | .reversed => ⟨Bridge.hist10, Or.inr rfl⟩

def decode : FrozenHistory → HistoryClass
  | ⟨history, _⟩ => if history = Bridge.hist01 then .forward else .reversed

theorem decode_encode (history : HistoryClass) : decode (encode history) = history := by
  cases history <;> decide

theorem encode_decode (history : FrozenHistory) : encode (decode history) = history := by
  rcases history with ⟨history, h01 | h10⟩
  · subst history
    rfl
  · subst history
    apply Subtype.ext
    decide

def sourceExchange (history : FrozenHistory) : FrozenHistory :=
  encode (exchange (decode history))

theorem exchange_commutes (history : HistoryClass) :
    sourceExchange (encode history) = encode (exchange history) := by
  rw [sourceExchange, decode_encode]

theorem source_exchange_involutive (history : FrozenHistory) :
    sourceExchange (sourceExchange history) = history := by
  unfold sourceExchange
  rw [decode_encode, exchange_involutive, encode_decode]

def sourceHistory (history : HistoryClass) : List TEvent :=
  (encode history).1

def sourceEndpoint (history : HistoryClass) : Option TRegime :=
  replayT (sourceHistory history) emptyT

def sourceErasedEndpoint (history : HistoryClass) : Option Regime :=
  (sourceEndpoint history).map TRegime.erase

theorem source_histories_distinct :
    sourceHistory .forward ≠ sourceHistory .reversed := by
  change Bridge.hist01 ≠ Bridge.hist10
  decide

theorem source_endpoints_distinct :
    sourceEndpoint .forward ≠ sourceEndpoint .reversed := by
  simpa [sourceEndpoint, sourceHistory, encode, emptyT] using
    Bridge.order_visible_to_metatheory

theorem source_erasure_equal :
    sourceErasedEndpoint .forward = sourceErasedEndpoint .reversed := by
  simpa [sourceErasedEndpoint, sourceEndpoint, sourceHistory, encode, emptyT]
    using Bridge.order_erased_at_object_level

theorem frozen_pair_observed_facts :
    Bridge.hist01 ≠ Bridge.hist10 ∧
      sourceEndpoint .forward ≠ sourceEndpoint .reversed ∧
      sourceErasedEndpoint .forward = sourceErasedEndpoint .reversed := by
  exact ⟨source_histories_distinct, source_endpoints_distinct,
    source_erasure_equal⟩

theorem chosen_pair_equivalence :
    (∀ left right, encode left = encode right → left = right) ∧
      (∀ target, ∃ source, encode source = target) ∧
      sourceExchange (encode .forward) = encode .reversed ∧
      sourceExchange (encode .reversed) = encode .forward ∧
      sourceEndpoint .forward ≠ sourceEndpoint .reversed ∧
      sourceErasedEndpoint .forward = sourceErasedEndpoint .reversed := by
  refine ⟨?_, ?_, ?_, ?_, source_endpoints_distinct, source_erasure_equal⟩
  · intro left right equal
    have mapped := congrArg decode equal
    simpa [decode_encode] using mapped
  · intro target
    exact ⟨decode target, encode_decode target⟩
  · exact exchange_commutes .forward
  · exact exchange_commutes .reversed

def ErasedReadout (Output : Type) := Option Regime → Output

theorem erased_readout_cannot_separate {Output : Type}
    (readout : ErasedReadout Output) :
    readout (sourceErasedEndpoint .forward) =
      readout (sourceErasedEndpoint .reversed) := by
  exact congrArg readout source_erasure_equal

theorem frozen_pair_supports_both_character_extensions :
    (∃ character : ExchangeCharacter, ¬ OperationalNontrivial character) ∧
      (∃ character : ExchangeCharacter, OperationalNontrivial character) := by
  refine ⟨⟨trivialCharacter, character_laws_do_not_force_nontrivial⟩,
    ⟨signCharacter, ?_⟩⟩
  simp [OperationalNontrivial, signCharacter]

#print axioms frozen_pair_observed_facts
#print axioms chosen_pair_equivalence
#print axioms erased_readout_cannot_separate
#print axioms frozen_pair_supports_both_character_extensions

end FrozenPairBridge
end AdmissionSignShadow
