/-!
# Operational Protocols & Carrier State Architecture

Formalizes:
- Multi-locus process carrier state with target loci, coupling channels,
  and embedded observer memory registers.
- Operational protocol stages:
  1. Preparations: initializing carrier regions
  2. Interventions: localized perturbations
  3. Records: persistent marks in dedicated registers
  4. Comparisons: coincidence evaluators
  5. Measurement instruments: non-disturbing and disturbing readouts

AuthorityEffect: None.
Axiom Scope: Strictly constructive; `#print axioms` in `{propext, Quot.sound}`.
-/

namespace P200OperationalProtocols

/-- Discrete state of the multi-locus carrier substrate. -/
@[ext]
structure CarrierState where
  l1   : Nat := 0
  l2   : Nat := 0
  m    : Nat := 0
  r1   : Nat := 0
  r2   : Nat := 0
  dist : Nat := 0
  deriving DecidableEq, Repr

-- -------------------------------------------------------------------------
-- Preparations
-- -------------------------------------------------------------------------

/-- Prepare independent product state on L1 and L2 with cleared records. -/
def prepareProduct (v1 v2 m : Nat) (s : CarrierState) : CarrierState :=
  { s with l1 := v1, l2 := v2, m := m, r1 := 0, r2 := 0, dist := 0 }

/-- Prepare symmetric state where coordinates at L1 and L2 coincide. -/
def prepareSymmetric (v m : Nat) (s : CarrierState) : CarrierState :=
  { s with l1 := v, l2 := v, m := m, r1 := 0, r2 := 0, dist := 0 }

theorem prepare_product_l1 (v1 v2 m : Nat) (s : CarrierState) :
    (prepareProduct v1 v2 m s).l1 = v1 := rfl

theorem prepare_product_l2 (v1 v2 m : Nat) (s : CarrierState) :
    (prepareProduct v1 v2 m s).l2 = v2 := rfl

theorem prepare_product_records (v1 v2 m : Nat) (s : CarrierState) :
    (prepareProduct v1 v2 m s).r1 = 0 ∧ (prepareProduct v1 v2 m s).r2 = 0 :=
  ⟨rfl, rfl⟩

theorem prepare_symmetric_eq (v m : Nat) (s : CarrierState) :
    (prepareSymmetric v m s).l1 = (prepareSymmetric v m s).l2 := rfl

-- -------------------------------------------------------------------------
-- Interventions
-- -------------------------------------------------------------------------

/-- Local intervention strictly at Locus 1. -/
def interveneL1 (f : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with l1 := f s.l1 }

/-- Local intervention strictly at Locus 2. -/
def interveneL2 (g : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with l2 := g s.l2 }

/-- Local intervention at coupling locus M. -/
def interveneM (h : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with m := h s.m }

theorem intervene_l1_preserves_l2 (f : Nat → Nat) (s : CarrierState) :
    (interveneL1 f s).l2 = s.l2 := rfl

theorem intervene_l1_preserves_r2 (f : Nat → Nat) (s : CarrierState) :
    (interveneL1 f s).r2 = s.r2 := rfl

theorem intervene_l1_preserves_m (f : Nat → Nat) (s : CarrierState) :
    (interveneL1 f s).m = s.m := rfl

theorem intervene_l2_preserves_l1 (g : Nat → Nat) (s : CarrierState) :
    (interveneL2 g s).l1 = s.l1 := rfl

theorem intervene_l2_preserves_r1 (g : Nat → Nat) (s : CarrierState) :
    (interveneL2 g s).r1 = s.r1 := rfl

theorem intervene_l2_preserves_m (g : Nat → Nat) (s : CarrierState) :
    (interveneL2 g s).m = s.m := rfl

-- -------------------------------------------------------------------------
-- Records
-- -------------------------------------------------------------------------

/-- Write persistent mark into Observer 1 register R1. -/
def record1 (val : Nat) (s : CarrierState) : CarrierState :=
  { s with r1 := val }

/-- Write persistent mark into Observer 2 register R2. -/
def record2 (val : Nat) (s : CarrierState) : CarrierState :=
  { s with r2 := val }

theorem record1_preserves_target (val : Nat) (s : CarrierState) :
    (record1 val s).l1 = s.l1 ∧ (record1 val s).l2 = s.l2 := ⟨rfl, rfl⟩

theorem record2_preserves_target (val : Nat) (s : CarrierState) :
    (record2 val s).l1 = s.l1 ∧ (record2 val s).l2 = s.l2 := ⟨rfl, rfl⟩

-- -------------------------------------------------------------------------
-- Embedded Measurement Instruments
-- -------------------------------------------------------------------------

/-- Non-disturbing readout of Locus 1 into record register R1. -/
def readout1 (probe : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with r1 := probe s.l1 }

/-- Non-disturbing readout of Locus 2 into record register R2. -/
def readout2 (probe : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with r2 := probe s.l2 }

/-- Disturbing readout of Locus 1 with state alteration and price recording. -/
def readout1_disturbing (probe disturb : Nat → Nat) (cost : Nat) (s : CarrierState) : CarrierState :=
  { s with l1 := disturb s.l1, r1 := probe s.l1, dist := s.dist + cost }

theorem readout1_preserves_l1 (probe : Nat → Nat) (s : CarrierState) :
    (readout1 probe s).l1 = s.l1 := rfl

theorem readout1_preserves_l2 (probe : Nat → Nat) (s : CarrierState) :
    (readout1 probe s).l2 = s.l2 := rfl

theorem readout1_preserves_r2 (probe : Nat → Nat) (s : CarrierState) :
    (readout1 probe s).r2 = s.r2 := rfl

theorem readout2_preserves_l1 (probe : Nat → Nat) (s : CarrierState) :
    (readout2 probe s).l1 = s.l1 := rfl

theorem readout2_preserves_l2 (probe : Nat → Nat) (s : CarrierState) :
    (readout2 probe s).l2 = s.l2 := rfl

theorem readout2_preserves_r1 (probe : Nat → Nat) (s : CarrierState) :
    (readout2 probe s).r1 = s.r1 := rfl

theorem readout1_readout2_comm (p1 p2 : Nat → Nat) (s : CarrierState) :
    readout1 p1 (readout2 p2 s) = readout2 p2 (readout1 p1 s) := rfl

-- -------------------------------------------------------------------------
-- Projections and Comparisons
-- -------------------------------------------------------------------------

/-- Projected observation for Observer 1: (target state, recorded mark). -/
def proj1 (s : CarrierState) : Nat × Nat := (s.l1, s.r1)

/-- Projected observation for Observer 2: (target state, recorded mark). -/
def proj2 (s : CarrierState) : Nat × Nat := (s.l2, s.r2)

/-- Marginal readout record at Observer 2. -/
def marginal2 (s : CarrierState) : Nat := s.r2

/-- Coincidence evaluator comparing observer memory marks. -/
def coincidence (s : CarrierState) : Bool := s.r1 == s.r2

theorem coincidence_iff (s : CarrierState) :
    coincidence s = true ↔ s.r1 = s.r2 := by
  dsimp [coincidence]
  exact beq_iff_eq

end P200OperationalProtocols
