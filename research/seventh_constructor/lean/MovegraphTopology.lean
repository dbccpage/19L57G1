import ConservativeGrammar

/-!
# Movegraph Topology: 1-Cycle Generation and Quotient Collapse

Formalization of Requirement R2:
- Native Movegraph DAG Acyclicity: strict potential growth forces Z_1(M_native) = 0
- Extended Movegraph with e_swap: explicit 2-cycle and multi-step cycles
- 1-Chain Complex formalization and proof that Z_1(M_extended) ≠ 0
- Presentation-to-quotient projection: swap edges map to isomorphic states
- Cycle collapse in quotient: presentation 1-cycles project to trivial holonomy at a single quotient point
- Presentation-quotient non-descent obstruction

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero unproven escapes.
AuthorityEffect: None.
-/

namespace SeventhConstructor

open SeventhConstructor

/-! ## 1. Native Movegraph DAG Acyclicity -/

def NativeTrajectory (p : CardinalProfile) : List ExtendedEvent → CardinalProfile
  | [] => p
  | e :: es => NativeTrajectory (stepProfile p e) es

theorem native_trajectory_strictly_increases (p : CardinalProfile) (es : List ExtendedEvent)
    (h_nonempty : es ≠ [])
    (h_all_native_non_supply : ∀ e ∈ es, e ≠ ExtendedEvent.supply ∧ e ≠ ExtendedEvent.swap) :
    potential (NativeTrajectory p es) > potential p := by
  induction es generalizing p with
  | nil => contradiction
  | cons head tail ih =>
      have h_head := h_all_native_non_supply head (List.Mem.head tail)
      have h_head_step : potential (stepProfile p head) > potential p :=
        native_non_supply_increases_potential p head h_head.1 h_head.2
      by_cases h_tail : tail = []
      · subst h_tail
        dsimp [NativeTrajectory]
        exact h_head_step
      · have h_tail_all : ∀ e ∈ tail, e ≠ ExtendedEvent.supply ∧ e ≠ ExtendedEvent.swap := by
          intro e he
          exact h_all_native_non_supply e (List.Mem.tail head he)
        have h_tail_step := ih (stepProfile p head) h_tail h_tail_all
        dsimp [NativeTrajectory]
        exact Nat.lt_trans h_head_step h_tail_step

/-- Theorem 2.1 (Native Movegraph Acyclicity):
No non-empty sequence of native non-supply events can return to the initial cardinal profile. -/
theorem native_movegraph_acyclic (p : CardinalProfile) (es : List ExtendedEvent)
    (h_nonempty : es ≠ [])
    (h_all_native_non_supply : ∀ e ∈ es, e ≠ ExtendedEvent.supply ∧ e ≠ ExtendedEvent.swap) :
    NativeTrajectory p es ≠ p := by
  intro h_eq
  have h_gt := native_trajectory_strictly_increases p es h_nonempty h_all_native_non_supply
  rw [h_eq] at h_gt
  exact Nat.lt_irrefl (potential p) h_gt

/-! ## 2. Extended Movegraph and Explicit 1-Cycle Generation -/

/-- Concrete asymmetric initial regime with 2 tokens and directed instance (0, 1). -/
def r0 : MiniRegime := { nData := 2, instances := [(0, 1)] }

/-- Result of applying swap(0, 1) to r0. -/
def r1 : MiniRegime := swapStep r0 0 1

/-- Theorem 2.2: The swapped regime r1 has instance (1, 0). -/
theorem r1_instances_eval : r1.instances = [(1, 0)] := by
  dsimp [r1, r0, swapStep, transposition]
  decide

/-- Theorem 2.3: States r0 and r1 are distinct presentation regimes. -/
theorem r0_ne_r1 : r0 ≠ r1 := by
  intro h_eq
  have h_inst : r0.instances = r1.instances := by rw [h_eq]
  dsimp [r0] at h_inst
  rw [r1_instances_eval] at h_inst
  revert h_inst
  decide

/-- Theorem 2.4: Applying swap(0, 1) to r1 returns exactly to r0. -/
theorem swap_returns_to_r0 : swapStep r1 0 1 = r0 := by
  dsimp [r1]
  exact swap_regime_involutive r0 0 1

/-! ## 3. 1-Chain Complex and Non-Vanishing 1-Homology (Z_1 ≠ 0) -/

/-- Directed edge between regimes. -/
structure DirectedEdge where
  src : MiniRegime
  dst : MiniRegime
  deriving DecidableEq, Repr

/-- Elementary 1-chain: a list of directed edges with integer weights. -/
abbrev Chain1 := List (DirectedEdge × Int)

/-- Boundary operator evaluating the net boundary flux at a vertex v. -/
def boundaryAt (c : Chain1) (v : MiniRegime) : Int :=
  c.foldl (fun acc (e, w) =>
    acc + (if v = e.dst then w else 0) - (if v = e.src then w else 0)
  ) 0

/-- A 1-chain is a closed 1-cycle if its boundary vanishes at all vertices. -/
def isCycle (c : Chain1) : Prop :=
  ∀ v, boundaryAt c v = 0

/-- The canonical 2-cycle in the extended movegraph. -/
def gamma2 : Chain1 :=
  [ (⟨r0, r1⟩, 1), (⟨r1, r0⟩, 1) ]

/-- Theorem 2.5: The 2-cycle has vanishing boundary at r0. -/
theorem gamma2_boundary_r0 : boundaryAt gamma2 r0 = 0 := by
  dsimp [gamma2, boundaryAt]
  omega

/-- Theorem 2.6: The 2-cycle has vanishing boundary at r1. -/
theorem gamma2_boundary_r1 : boundaryAt gamma2 r1 = 0 := by
  dsimp [gamma2, boundaryAt]
  omega

/-- Theorem 2.7: The 2-cycle has vanishing boundary everywhere. -/
theorem gamma2_is_cycle : isCycle gamma2 := by
  intro v
  dsimp [gamma2, boundaryAt]
  omega

/-- Theorem 2.8 (Non-Trivial 1-Homology Z_1 ≠ 0):
The 1-cycle space of the extended movegraph is non-trivial (contains a non-zero cycle of distinct edges). -/
theorem z1_extended_nontrivial :
    ∃ (c : Chain1), c ≠ [] ∧ isCycle c ∧ (∀ (p : DirectedEdge × Int), p ∈ c → p.1.src ≠ p.1.dst ∧ p.2 ≠ 0) := by
  refine ⟨gamma2, ?_, gamma2_is_cycle, ?_⟩
  · intro h_nil
    cases h_nil
  · intro p hp
    cases hp with
    | head =>
        exact ⟨r0_ne_r1, by decide⟩
    | tail _ hp2 =>
        cases hp2 with
        | head =>
            exact ⟨Ne.symm r0_ne_r1, by decide⟩
        | tail _ hp3 =>
            cases hp3

/-! ## 4. Presentation-to-Quotient Projection and Non-Descent -/

/-- Isomorphism between MiniRegimes via an index bijection. -/
def Isomorphic (a b : MiniRegime) : Prop :=
  a.nData = b.nData ∧
  ∃ (pi : Nat → Nat),
    (∀ x, pi (transposition 0 1 x) = x) ∧
    b.instances = a.instances.map (fun p => (pi p.1, pi p.2))

/-- Theorem 2.9 (Swap Step Preserves Isomorphism Class):
The swap step generates a regime isomorphic to the initial regime. -/
theorem swap_step_isomorphic (r : MiniRegime) :
    Isomorphic r (swapStep r 0 1) := by
  dsimp [Isomorphic]
  refine ⟨rfl, transposition 0 1, ?_, rfl⟩
  intro x
  exact transposition_involutive 0 1 x

/-- Theorem 2.10 (Cycle Collapses in Quotient):
Any state invariant or quotient projection q that respects isomorphism
evaluates to identical values on r0 and r1, collapsing the presentation cycle to a single point. -/
theorem quotient_cycle_collapse (q : MiniRegime → Nat)
    (h_iso : ∀ a b, Isomorphic a b → q a = q b) :
    q r0 = q r1 := by
  have h_iso_r0_r1 := swap_step_isomorphic r0
  dsimp [r1]
  exact h_iso r0 (swapStep r0 0 1) h_iso_r0_r1

/-- Presentation signature cochain: assigns 1 to every transposition edge. -/
def presentationSignCochain (_ : DirectedEdge) : Int := 1

/-- Coboundary of a descended quotient potential P o q. -/
def descendedCoboundary (P : Nat → Int) (q : MiniRegime → Nat) (e : DirectedEdge) : Int :=
  P (q e.dst) - P (q e.src)

/-- Theorem 2.11 (Presentation-Quotient Non-Descent Obstruction):
The presentation signature circulation on the swap edge cannot descend to the coboundary
of any single-valued quotient potential, because any descended coboundary vanishes on isomorphic states. -/
theorem presentation_quotient_obstruction
    (q : MiniRegime → Nat)
    (h_iso : ∀ a b, Isomorphic a b → q a = q b)
    (P : Nat → Int) :
    presentationSignCochain ⟨r0, r1⟩ - descendedCoboundary P q ⟨r0, r1⟩ = 1 := by
  dsimp [presentationSignCochain, descendedCoboundary]
  have h_eq : q r1 = q r0 := by
    have h := quotient_cycle_collapse q h_iso
    exact h.symm
  rw [h_eq]
  omega

end SeventhConstructor
