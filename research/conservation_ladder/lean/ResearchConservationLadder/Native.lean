import ResearchNativeBridge.Passage
import ResearchConservationLadder.Central

/-!
# The ladder's first rung, and where the passage stands on it

AuthorityEffect: None.  Paths are the actual-step paths of the
`native_bridge` tree.

Proved here:

* `conserved_path`: for any step function, a quantity preserved by every
  step is preserved along every path.  This is the conditional first rung.
  It supplies no conserved quantity by itself.
* `tick`, `charge_tick`, `tick_path_charge`: the central weight's
  generated history is a one-event step system on pairs of configurations.
  Its rotation charge is preserved by the step, and so along every path.
  The charge is constructed from the symmetry, not declared as an
  invariant.
* `passage_conserved_blind`: on the sealed passage, a quantity preserved
  by every event cannot distinguish a live state from its budget or
  license variants, or from its halted version.  The passage supplies no
  action, admissible variation or one-parameter symmetry; this tree
  supplies those only on its own integer carrier.
-/

namespace ResearchConservationLadder

open PrimitivePassage TransitionAlphabet ResearchNativeBridge

theorem conserved_path {σ ε κ : Type} (f : σ → ε → σ) (Q : σ → κ)
    (h : ∀ s e, Q (f s e) = Q s) {s t : σ} (τ : Path f s t) : Q t = Q s := by
  induction τ with
  | nil _ => rfl
  | cons e _ ih => rw [ih, h]

/-- One step of the generated history, on pairs of consecutive points. -/
def tick (c : Int) (st : P × P) (_ : Unit) : P × P := (st.2, next c st.1 st.2)

/-- The rotation charge of a pair. -/
def pairCharge (c : Int) (st : P × P) : Int := charge (central c) rot st.1 st.2

theorem charge_tick (c : Int) (st : P × P) (u : Unit) :
    pairCharge c (tick c st u) = pairCharge c st :=
  solve_charge_const c st.1 st.2 1

theorem tick_path_charge (c : Int) {s t : P × P} (τ : Path (tick c) s t) :
    pairCharge c t = pairCharge c s :=
  conserved_path (tick c) (pairCharge c) (charge_tick c) τ

theorem passage_conserved_blind {κ : Type} (Q : PState → κ)
    (h : ∀ s e, Q (step s e) = Q s) (s : PState) (hs : s.halted = false)
    (n : Nat) (b : Bool) :
    Q (budS s n) = Q s ∧ Q (licS s b) = Q s ∧ Q (haltS s) = Q s := by
  refine ⟨?_, ?_, ?_⟩
  · rw [← step_setBudget_live s n hs]; exact h s _
  · rw [← step_setLicense_live s b hs]; exact h s _
  · rw [← step_halt_eq s]; exact h s _

end ResearchConservationLadder
