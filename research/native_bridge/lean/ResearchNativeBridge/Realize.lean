import Trace
import ResearchNativeBridge.Passage

/-!
# Reading a G013 trace back as a native path

AuthorityEffect: None.  The G013 tree's `Trace` module is consumed
read-only as a Lake dependency.  Its steps carry a source, a target and a
text label, and nothing ties the target to any dynamics.  Over the passage
states, a G013 trace is read back by a supplied label decoder: each step is
realized when its label decodes to an event whose sealed step, from the
step's source, is the step's target.

Proved here:

* `realize`, `realize_iff`: the read-back succeeds exactly when every step
  is realized in that sense.
* `realize_events`: on success, the native path's events are the decoded
  labels, and they replay from the start to the end (`Path.run_events`).
* `unrealized_step`: a one-step G013 trace whose endpoints are joined by a
  native path, but whose own step is not a native step, is refused.  So a
  G013 trace is not by itself a native trace, and the read-back refuses
  instead of asserting a bridge.
-/

namespace ResearchNativeBridge

open PrimitivePassage TransitionAlphabet G013TraceCalculus

/-- Decode every label of a G013 trace. -/
def labels : {s t : PState} → Trace PState s t → List String
  | _, _, .nil _ => []
  | _, _, .cons (.mk _ _ label) rest => label :: labels rest

/-- Every step's label decodes to an event whose sealed step lands on the
step's recorded target. -/
def Realized (dec : String → Option PEvent) : {s t : PState} → Trace PState s t → Prop
  | _, _, .nil _ => True
  | s, _, .cons (.mk _ m label) rest =>
      (∃ e, dec label = some e ∧ step s e = m) ∧ Realized dec rest

/-- Read a G013 trace back as a native path, or refuse. -/
def realize (dec : String → Option PEvent) :
    {s t : PState} → Trace PState s t → Option (NPath s t)
  | _, _, .nil s => some (.nil s)
  | s, _, .cons (.mk _ m label) rest =>
      match dec label with
      | none => none
      | some e =>
          if h : step s e = m then
            (realize dec rest).map (fun τ => .cons e (castSrc h.symm τ))
          else none

theorem realize_iff (dec : String → Option PEvent) {s t : PState}
    (τ : Trace PState s t) : (realize dec τ).isSome = true ↔ Realized dec τ := by
  induction τ with
  | nil _ => simp [realize, Realized]
  | @cons src dst _ st rest ih =>
      cases st with
      | mk label =>
          simp only [realize, Realized]
          cases hd : dec label with
          | none =>
              simp only [Option.isSome_none, Bool.false_eq_true, false_iff]
              intro ⟨⟨e, he, _⟩, _⟩
              cases he
          | some e =>
              simp only
              by_cases hs : step src e = dst
              · rw [dif_pos hs, Option.isSome_map, ih]
                constructor
                · intro hr; exact ⟨⟨e, rfl, hs⟩, hr⟩
                · intro hr; exact hr.2
              · rw [dif_neg hs]
                simp only [Option.isSome_none, Bool.false_eq_true, false_iff]
                intro ⟨⟨e', he', hs'⟩, _⟩
                cases he'
                exact hs hs'

theorem realize_events (dec : String → Option PEvent) {s t : PState}
    (τ : Trace PState s t) (ν : NPath s t) (h : realize dec τ = some ν) :
    (labels τ).map dec = (Path.events ν).map some := by
  induction τ with
  | nil _ =>
      simp only [realize, Option.some.injEq] at h
      subst h; rfl
  | @cons src dst _ st rest ih =>
      cases st with
      | mk label =>
          simp only [realize] at h
          cases hd : dec label with
          | none => rw [hd] at h; cases h
          | some e =>
              rw [hd] at h
              simp only at h
              by_cases hs : step src e = dst
              · rw [dif_pos hs] at h
                cases hr : realize dec rest with
                | none => rw [hr] at h; cases h
                | some ρ =>
                    rw [hr] at h
                    simp only [Option.map_some, Option.some.injEq] at h
                    subst h
                    simp only [labels, List.map_cons, Path.events, hd,
                      events_castSrc, ih ρ hr]
              · rw [dif_neg hs] at h; cases h

/-- The decoder used by the refusal witness. -/
def witnessDecoder : String → Option PEvent
  | "admitOcc" => some (.admitOcc 0)
  | "halt" => some .halt
  | _ => none

/-- A one-step G013 trace from genesis to the halted genesis state,
labelled with an occurrence admission. -/
def mislabelled : Trace PState genesisP (haltS genesisP) :=
  .cons (.mk genesisP (haltS genesisP) "admitOcc") (.nil _)

/-- **Refusal witness.**  The endpoints of `mislabelled` are joined by a
native path, but its step is not a native step, and the read-back
refuses. -/
theorem unrealized_step :
    Nonempty (NPath genesisP (haltS genesisP)) ∧
      realize witnessDecoder mislabelled = none :=
  ⟨⟨Path.cons .halt (Path.nil _)⟩, rfl⟩

end ResearchNativeBridge
