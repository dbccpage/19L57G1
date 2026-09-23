import CliffordSymplectic
import ResearchConservationLadder.Native
import ResearchDomainAdapters.Adapter

/-!
# Four domains against the passage

AuthorityEffect: None.  Each domain's carrier and step are imported
read-only from the tree that defines them, or declared here and classified
as supplied.

* **A monotone counter** (supplied).  `counterAdapter` is a faithful
  adapter: the encoding is injective on the core, and the counter's value
  is the native occurrence count (`counter_core_injective`).
* **The P209b two-element-field carrier** (imported).  The matrix `matH`
  swaps the two basis vectors and is its own inverse.  So every
  translation of its action into the passage gives both basis vectors the
  same core (`quantum_core_collapse`), and none is faithful in the core
  (`no_core_faithful_quantum`).  A translation does exist, through budget
  writes (`quantum_budget_adapter`).
* **The conservation ladder's integer mechanics** (imported).  At
  coefficient 2 its step on pairs has period four.  So every translation
  gives a state and its successor the same core (`mechanics_core_collapse`).
* **Proposal and license** (the passage's own events).  A proposal is
  mapped to no native event, so it changes nothing.  Application is column
  creation, and it is inert without license (`apply_needs_license`) or
  without budget (`apply_needs_budget`).  These are the sealed gates, read
  through the adapter; no new law is attributed to the passage.
-/

namespace ResearchDomainAdapters

open PrimitivePassage TransitionAlphabet ResearchNativeBridge
open P209bCliffordSymplectic ResearchConservationLadder

/-! ## A monotone counter -/

def count (n : Nat) (_ : Unit) : Nat := n + 1

def counterEnc (n : Nat) : PState := { genesisP with occ := List.range n }

theorem counter_comm (n : Nat) (u : Unit) :
    run step [.admitOcc n] (counterEnc n) = counterEnc (count n u) := by
  show step (counterEnc n) (.admitOcc n) = counterEnc (n + 1)
  have hm : n ∉ List.range n := by simp
  simp only [step, counterEnc, genesisP, hm, if_false, List.range_succ]
  rfl

def counterSim : Sim count step where
  enc := counterEnc
  tr := fun n _ => [.admitOcc n]
  comm := counter_comm

def counterAdapter : Adapter count (fun n => n) (fun s => s.occ.length) where
  sim := counterSim
  obsMap := id
  obs_comm := fun n => by simp [counterSim, counterEnc]

theorem counter_core_injective (a b : Nat) (h : core (counterSim.enc a) = core (counterSim.enc b)) :
    a = b := by
  have := congrArg (fun c => c.occ.length) h
  simpa [core, counterSim, counterEnc] using this

/-! ## The P209b carrier -/

/-- The imported matrix action as a one-event step. -/
def hStep (v : Vec2) (_ : Unit) : Vec2 := matMulVec matH v

theorem hStep_twice (v : Vec2) (u : Unit) : hStep (hStep v u) u = v := by
  cases v with
  | mk x z => cases x <;> cases z <;> rfl

theorem basis_distinct : ex ≠ ez := by decide

theorem hStep_ex : hStep ex () = ez := rfl

theorem quantum_core_collapse (m : Sim hStep step) :
    core (m.enc ez) = core (m.enc ex) := by
  have := swap_core m ex () (hStep_twice ex ())
  rw [hStep_ex] at this
  exact this

theorem no_core_faithful_quantum :
    ¬ ∃ m : Sim hStep step, ∀ a b, core (m.enc a) = core (m.enc b) → a = b := by
  intro ⟨m, hinj⟩
  exact basis_distinct (hinj ex ez (quantum_core_collapse m).symm)

/-- A numbering of the four vectors. -/
def vecCode (v : Vec2) : Nat :=
  (match v.x with | .zero => 0 | .one => 1) + 2 * (match v.z with | .zero => 0 | .one => 1)

theorem vecCode_injective (a b : Vec2) (h : vecCode a = vecCode b) : a = b := by
  cases a with
  | mk ax az => cases b with
    | mk bx bz => cases ax <;> cases az <;> cases bx <;> cases bz <;> simp_all [vecCode]

theorem quantum_budget_adapter :
    ∃ m : Sim hStep step, ∀ a b, m.enc a = m.enc b → a = b :=
  ⟨budgetSim hStep vecCode, budgetSim_enc_injective hStep vecCode vecCode_injective⟩

/-! ## The ladder's integer mechanics at coefficient two -/

theorem tick_two_period (st : P × P) :
    tick 2 (tick 2 (tick 2 (tick 2 st ()) ()) ()) () = st := by
  obtain ⟨⟨a₁, a₂⟩, ⟨b₁, b₂⟩⟩ := st
  simp only [tick, next]
  simp only [Int.sub_self, Int.zero_mul, Int.zero_sub, Int.neg_neg]

theorem mechanics_core_collapse (m : Sim (tick 2) step) (st : P × P) :
    core (m.enc (tick 2 st ())) = core (m.enc st) := by
  have hback : run (tick 2) [(), (), ()] (tick 2 st ()) = st := tick_two_period st
  exact passage_sim_cycle m (Path.cons () (Path.nil _)) (Path.ofSub ⟨[(), (), ()], hback⟩)

theorem mechanics_moves : tick 2 ((1, 0), (0, 1)) () ≠ ((1, 0), (0, 1)) := by decide

/-! ## Proposal and license -/

/-- The declared proposal/license events. -/
inductive PL where
  | propose (c : List Nat)
  | grant (b : Bool)
  | apply (c : List Nat)

/-- The adapter's event map: a proposal is no native event. -/
def plEvents : PL → List PEvent
  | .propose _ => []
  | .grant b => [.setLicense b]
  | .apply c => [.addCol c]

/-- The passage stepped through the adapter's event map. -/
def plStep (s : PState) (e : PL) : PState := run step (plEvents e) s

def plSim : Sim plStep step where
  enc := id
  tr := fun _ e => plEvents e
  comm := fun _ _ => rfl

theorem propose_inert (s : PState) (c : List Nat) : plStep s (.propose c) = s := rfl

theorem apply_needs_license (s : PState) (c : List Nat) (hl : s.licensed = false)
    (hh : s.halted = false) : plStep s (.apply c) = s :=
  proposal_not_execution s c hl hh

theorem apply_needs_budget (s : PState) (c : List Nat) (hb : s.budget = 0)
    (hh : s.halted = false) : plStep s (.apply c) = s :=
  budget_gates_execution s c hb hh

end ResearchDomainAdapters
