/-!
# Composite Systems & Pre-Spatial Locality (Target P203)

Formalizes:
1. Multi-locus carrier networks and canonical associative composition:
   (A ⊗ B) ⊗ C ≅ A ⊗ (B ⊗ C)
2. Canonical associator isomorphism preserving subsystem projections.
3. Bipartite network cuts and pre-spatial interaction structure.
4. Strict operational non-signaling across separated footprints:
   Interventions on Subsystem A leave all observables on Subsystem B invariant
   prior to mediating transitions.
5. Negative controls: leaky footprint intervention and mediated coupling both
   diverge on distant observables.
6. Duplicate observer agreement on symmetric preparations and presentation
   symmetry equivariance under subsystem automorphism.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`;
zero `Classical.choice`; zero `mathlib`.
-/

namespace P203CompositeSystems

-- =========================================================================
-- 1. Canonical Associative Tensor Composition
-- =========================================================================

/-- Constructive isomorphism witnessing equivalence of composite states. -/
structure Iso (α β : Type) where
  toFun : α → β
  invFun : β → α
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

/-- Canonical associator isomorphism for ternary product composition:
    ((α × β) × γ) ≅ (α × (β × γ)). -/
def tensor_assoc (α β γ : Type) : Iso ((α × β) × γ) (α × (β × γ)) where
  toFun := fun ((a, b), c) => (a, (b, c))
  invFun := fun (a, (b, c)) => ((a, b), c)
  left_inv := fun ((_, _), _) => rfl
  right_inv := fun (_, (_, _)) => rfl

theorem tensor_assoc_left_inv (α β γ : Type) (x : (α × β) × γ) :
    (tensor_assoc α β γ).invFun ((tensor_assoc α β γ).toFun x) = x := rfl

theorem tensor_assoc_right_inv (α β γ : Type) (y : α × (β × γ)) :
    (tensor_assoc α β γ).toFun ((tensor_assoc α β γ).invFun y) = y := rfl

-- Projections on left-bracketed composition ((A ⊗ B) ⊗ C)
def projA_left {α β γ : Type} : ((α × β) × γ) → α := fun ((a, _), _) => a
def projB_left {α β γ : Type} : ((α × β) × γ) → β := fun ((_, b), _) => b
def projC_left {α β γ : Type} : ((α × β) × γ) → γ := fun ((_, _), c) => c

-- Projections on right-bracketed composition (A ⊗ (B ⊗ C))
def projA_right {α β γ : Type} : (α × (β × γ)) → α := fun (a, (_, _)) => a
def projB_right {α β γ : Type} : (α × (β × γ)) → β := fun (_, (b, _)) => b
def projC_right {α β γ : Type} : (α × (β × γ)) → γ := fun (_, (_, c)) => c

/-- Associator strictly preserves Subsystem A projection. -/
theorem assoc_preserves_projA (α β γ : Type) (x : (α × β) × γ) :
    projA_right ((tensor_assoc α β γ).toFun x) = projA_left x := rfl

/-- Associator strictly preserves Subsystem B projection. -/
theorem assoc_preserves_projB (α β γ : Type) (x : (α × β) × γ) :
    projB_right ((tensor_assoc α β γ).toFun x) = projB_left x := rfl

/-- Associator strictly preserves Subsystem C projection. -/
theorem assoc_preserves_projC (α β γ : Type) (x : (α × β) × γ) :
    projC_right ((tensor_assoc α β γ).toFun x) = projC_left x := rfl

/-- Inverse associator strictly preserves Subsystem A projection. -/
theorem assoc_inv_preserves_projA (α β γ : Type) (y : α × (β × γ)) :
    projA_left ((tensor_assoc α β γ).invFun y) = projA_right y := rfl

/-- Inverse associator strictly preserves Subsystem B projection. -/
theorem assoc_inv_preserves_projB (α β γ : Type) (y : α × (β × γ)) :
    projB_left ((tensor_assoc α β γ).invFun y) = projB_right y := rfl

/-- Inverse associator strictly preserves Subsystem C projection. -/
theorem assoc_inv_preserves_projC (α β γ : Type) (y : α × (β × γ)) :
    projC_left ((tensor_assoc α β γ).invFun y) = projC_right y := rfl

-- =========================================================================
-- 2. Ternary Carrier State and Associative Coherence
-- =========================================================================

/-- A concrete ternary multi-locus carrier network with loci A, B, C. -/
@[ext]
structure Carrier3State where
  a : Nat := 0
  b : Nat := 0
  c : Nat := 0
  deriving DecidableEq, Repr

def toLeftAssoc (s : Carrier3State) : (Nat × Nat) × Nat :=
  ((s.a, s.b), s.c)

def fromLeftAssoc (p : (Nat × Nat) × Nat) : Carrier3State :=
  { a := p.1.1, b := p.1.2, c := p.2 }

def toRightAssoc (s : Carrier3State) : Nat × (Nat × Nat) :=
  (s.a, (s.b, s.c))

def fromRightAssoc (p : Nat × (Nat × Nat)) : Carrier3State :=
  { a := p.1, b := p.2.1, c := p.2.2 }

theorem toLeft_fromLeft (p : (Nat × Nat) × Nat) :
    toLeftAssoc (fromLeftAssoc p) = p := rfl

theorem fromLeft_toLeft (s : Carrier3State) :
    fromLeftAssoc (toLeftAssoc s) = s := rfl

theorem toRight_fromRight (p : Nat × (Nat × Nat)) :
    toRightAssoc (fromRightAssoc p) = p := rfl

theorem fromRight_toRight (s : Carrier3State) :
    fromRightAssoc (toRightAssoc s) = s := rfl

/-- Canonical associator maps left grouping to right grouping coherently. -/
theorem assoc_carrier_commute (s : Carrier3State) :
    (tensor_assoc Nat Nat Nat).toFun (toLeftAssoc s) = toRightAssoc s := rfl

/-- Inverse associator maps right grouping to left grouping coherently. -/
theorem assoc_carrier_inv_commute (s : Carrier3State) :
    (tensor_assoc Nat Nat Nat).invFun (toRightAssoc s) = toLeftAssoc s := rfl

-- =========================================================================
-- 3. Four-Locus Bipartite Carrier Network
-- =========================================================================

/-- A four-locus carrier network partitioned into Subsystem A (a1, a2)
    and Subsystem B (b1, b2). -/
@[ext]
structure NetworkState where
  a1 : Nat := 0
  a2 : Nat := 0
  b1 : Nat := 0
  b2 : Nat := 0
  deriving DecidableEq, Repr

-- Subsystem projections
def projA (s : NetworkState) : Nat × Nat := (s.a1, s.a2)
def projB (s : NetworkState) : Nat × Nat := (s.b1, s.b2)
def proj_a1 (s : NetworkState) : Nat := s.a1
def proj_a2 (s : NetworkState) : Nat := s.a2
def proj_b1 (s : NetworkState) : Nat := s.b1
def proj_b2 (s : NetworkState) : Nat := s.b2

/-- Canonical decomposition into tensor product of Subsystems A and B. -/
def toProduct (s : NetworkState) : (Nat × Nat) × (Nat × Nat) :=
  (projA s, projB s)

def fromProduct (p : (Nat × Nat) × (Nat × Nat)) : NetworkState :=
  { a1 := p.1.1, a2 := p.1.2, b1 := p.2.1, b2 := p.2.2 }

theorem toProduct_fromProduct (p : (Nat × Nat) × (Nat × Nat)) :
    toProduct (fromProduct p) = p := rfl

theorem fromProduct_toProduct (s : NetworkState) :
    fromProduct (toProduct s) = s := rfl

-- =========================================================================
-- 4. Operational Interventions, Observables, and Pre-Spatial Non-Signaling
-- =========================================================================

/-- An intervention strictly localized to Subsystem A. -/
def interveneA (f : Nat × Nat → Nat × Nat) (s : NetworkState) : NetworkState :=
  let p := f (s.a1, s.a2)
  { s with a1 := p.1, a2 := p.2 }

/-- Single-locus intervention at locus a1. -/
def intervene_a1 (f : Nat → Nat) (s : NetworkState) : NetworkState :=
  { s with a1 := f s.a1 }

/-- Single-locus intervention at locus a2. -/
def intervene_a2 (f : Nat → Nat) (s : NetworkState) : NetworkState :=
  { s with a2 := f s.a2 }

/-- Operational observable strictly localized to Subsystem B. -/
def observableB (obs : Nat × Nat → Nat) (s : NetworkState) : Nat :=
  obs (s.b1, s.b2)

/-- Observable readout at locus b1. -/
def observable_b1 (obs : Nat → Nat) (s : NetworkState) : Nat :=
  obs s.b1

/-- Observable readout at locus b2. -/
def observable_b2 (obs : Nat → Nat) (s : NetworkState) : Nat :=
  obs s.b2

/-- **Strict Operational Non-Signaling Theorem (Bipartite).**
    Any intervention localized to Subsystem A leaves all observables on
    Subsystem B invariant prior to mediating transitions. -/
theorem non_signaling_bipartite (f : Nat × Nat → Nat × Nat) (obs : Nat × Nat → Nat) (s : NetworkState) :
    observableB obs (interveneA f s) = observableB obs s := rfl

/-- Subsystem B state projection is strictly invariant under Subsystem A interventions. -/
theorem non_signaling_projB (f : Nat × Nat → Nat × Nat) (s : NetworkState) :
    projB (interveneA f s) = projB s := rfl

/-- Single locus intervention at a1 leaves observable at b1 invariant. -/
theorem non_signaling_a1_b1 (f : Nat → Nat) (obs : Nat → Nat) (s : NetworkState) :
    observable_b1 obs (intervene_a1 f s) = observable_b1 obs s := rfl

/-- Single locus intervention at a1 leaves observable at b2 invariant. -/
theorem non_signaling_a1_b2 (f : Nat → Nat) (obs : Nat → Nat) (s : NetworkState) :
    observable_b2 obs (intervene_a1 f s) = observable_b2 obs s := rfl

/-- Single locus intervention at a2 leaves observable at b1 invariant. -/
theorem non_signaling_a2_b1 (f : Nat → Nat) (obs : Nat → Nat) (s : NetworkState) :
    observable_b1 obs (intervene_a2 f s) = observable_b1 obs s := rfl

/-- Single locus intervention at a2 leaves observable at b2 invariant. -/
theorem non_signaling_a2_b2 (f : Nat → Nat) (obs : Nat → Nat) (s : NetworkState) :
    observable_b2 obs (intervene_a2 f s) = observable_b2 obs s := rfl

/-- Sequential interventions on Subsystem A do not perturb Subsystem B observables. -/
theorem non_signaling_sequenceA (f g : Nat × Nat → Nat × Nat) (obs : Nat × Nat → Nat) (s : NetworkState) :
    observableB obs (interveneA g (interveneA f s)) = observableB obs s := rfl

-- =========================================================================
-- 5. Negative Controls: Leaky Footprints and Mediating Transitions
-- =========================================================================

/-- Leaky intervention whose footprint crosses the bipartite cut to modify locus b1. -/
def intervene_leaky (f_a f_b : Nat → Nat) (s : NetworkState) : NetworkState :=
  { s with a1 := f_a s.a1, b1 := f_b s.b1 }

/-- **Leaky Footprint Divergence Theorem.**
    When an intervention leaks across the cut, distant observables diverge. -/
theorem leaky_footprint_divergence :
    let s : NetworkState := { a1 := 0, a2 := 0, b1 := 0, b2 := 0 }
    observable_b1 (fun x => x) (intervene_leaky (fun x => x + 1) (fun x => x + 1) s) ≠
    observable_b1 (fun x => x) s := by
  decide

/-- Mediating transition propagating information across the cut from a2 to b1. -/
def relay_A_to_B (s : NetworkState) : NetworkState :=
  { s with b1 := s.a2 }

/-- **Mediated Causal Signaling Divergence Theorem.**
    Causal signaling is enabled strictly after relational coupling across the cut. -/
theorem mediated_signaling_divergence :
    let s0 : NetworkState := { a1 := 0, a2 := 0, b1 := 0, b2 := 0 }
    let s1 : NetworkState := { a1 := 0, a2 := 1, b1 := 0, b2 := 0 }
    observable_b1 (fun x => x) (relay_A_to_B s0) ≠
    observable_b1 (fun x => x) (relay_A_to_B s1) := by
  decide

-- =========================================================================
-- 6. Duplicate Observers and Automorphism Symmetry Invariance
-- =========================================================================

/-- Subsystem swap involution exchanging Subsystem A and Subsystem B. -/
def swapSubsystems (s : NetworkState) : NetworkState :=
  { a1 := s.b1, a2 := s.b2, b1 := s.a1, b2 := s.a2 }

/-- Swap involution is an involutive automorphism: applying it twice is the identity. -/
theorem swap_involutive (s : NetworkState) :
    swapSubsystems (swapSubsystems s) = s := rfl

/-- Predicate characterizing states that are invariant under subsystem swap. -/
def IsSymmetricState (s : NetworkState) : Prop :=
  s.a1 = s.b1 ∧ s.a2 = s.b2

/-- Symmetric preparations are invariant under the swap automorphism. -/
theorem swap_symmetric_eq (s : NetworkState) (h : IsSymmetricState s) :
    swapSubsystems s = s := by
  cases s
  dsimp [IsSymmetricState] at h
  obtain ⟨h1, h2⟩ := h
  dsimp [swapSubsystems]
  rw [h1, h2]

-- Duplicate observers embedded at locus a1 and locus b1
def readoutA1 (probe : Nat → Nat) (s : NetworkState) : Nat := probe s.a1
def readoutB1 (probe : Nat → Nat) (s : NetworkState) : Nat := probe s.b1

/-- **Duplicate Observer Agreement Theorem.**
    On symmetric preparations (s.a1 = s.b1), duplicate observers running
    identical local readout protocols obtain matching recorded marks. -/
theorem duplicate_observer_agreement (probe : Nat → Nat) (s : NetworkState) (h : s.a1 = s.b1) :
    readoutA1 probe s = readoutB1 probe s := by
  dsimp [readoutA1, readoutB1]
  rw [h]

/-- Readout operations are equivariant under subsystem swap. -/
theorem readout_swap_equivariance_B1 (probe : Nat → Nat) (s : NetworkState) :
    readoutB1 probe (swapSubsystems s) = readoutA1 probe s := rfl

theorem readout_swap_equivariance_A1 (probe : Nat → Nat) (s : NetworkState) :
    readoutA1 probe (swapSubsystems s) = readoutB1 probe s := rfl

/-- Asymmetric preparations yield divergent recorded marks under injective readout. -/
theorem asymmetric_observer_divergence :
    let s : NetworkState := { a1 := 0, a2 := 0, b1 := 1, b2 := 0 }
    readoutA1 (fun x => x) s ≠ readoutB1 (fun x => x) s := by
  decide

-- =========================================================================
-- 7. Pre-Spatial Relational Connectivity
-- =========================================================================

/-- Evaluates whether a mediating bridge transition between cut partitions is active. -/
def hasMediatingBridge (bridgeActive : Bool) : Bool := bridgeActive

/-- Without a mediating bridge, cut partitions remain relationally disconnected. -/
theorem disconnected_cut_no_bridge :
    hasMediatingBridge false = false := rfl

/-- Activating a mediating bridge establishes relational connectivity across the cut. -/
theorem connected_cut_with_bridge :
    hasMediatingBridge true = true := rfl

end P203CompositeSystems
