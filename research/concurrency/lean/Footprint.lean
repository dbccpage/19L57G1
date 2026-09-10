import Carrier

/-!
# Operational Footprints & Derived Interaction Dependency Graph

Defines read/write access footprints on the 3-locus carrier and derives the
operational interaction dependency graph directly from access patterns,
without any background spatial metric or coordinate embedding.

AuthorityEffect: None.
-/

namespace Concurrency

/-- Identification of loci in the 3-locus product carrier. -/
inductive Locus where
  | L1
  | L2
  | M
  deriving DecidableEq, Repr

/-- Read and write footprints represented as boolean access masks over {L1, L2, M}. -/
structure Footprint where
  r1 : Bool
  r2 : Bool
  rm : Bool
  w1 : Bool
  w2 : Bool
  wm : Bool
  deriving DecidableEq, Repr

/-- Query whether a footprint reads a given locus. -/
def Footprint.reads (fp : Footprint) (l : Locus) : Bool :=
  match l with
  | .L1 => fp.r1
  | .L2 => fp.r2
  | .M  => fp.rm

/-- Query whether a footprint writes to a given locus. -/
def Footprint.writes (fp : Footprint) (l : Locus) : Bool :=
  match l with
  | .L1 => fp.w1
  | .L2 => fp.w2
  | .M  => fp.wm

/-- Locus-level interference condition (Bernstein condition):
    Interference occurs if one operation writes while the other reads or writes. -/
def locusInterferes (wA rA wB rB : Bool) : Bool :=
  (wA && (rB || wB)) || (wB && (rA || wA))

/-- Two footprints interfere if they interfere at any locus. -/
def interferes (f1 f2 : Footprint) : Bool :=
  locusInterferes f1.w1 f1.r1 f2.w1 f2.r1 ||
  locusInterferes f1.w2 f1.r2 f2.w2 f2.r2 ||
  locusInterferes f1.wm f1.rm f2.wm f2.rm

/-- Two footprints are disjoint (independent) if they do not interfere at any locus. -/
def isDisjoint (f1 f2 : Footprint) : Bool :=
  !interferes f1 f2

/-- Locus interference is symmetric. -/
theorem locusInterferes_symm (wA rA wB rB : Bool) :
    locusInterferes wA rA wB rB = locusInterferes wB rB wA rA := by
  dsimp [locusInterferes]
  cases wA <;> cases rA <;> cases wB <;> cases rB <;> rfl

/-- Global footprint interference is symmetric. -/
theorem interferes_symm (f1 f2 : Footprint) :
    interferes f1 f2 = interferes f2 f1 := by
  dsimp [interferes]
  rw [locusInterferes_symm f1.w1 f1.r1 f2.w1 f2.r1,
      locusInterferes_symm f1.w2 f1.r2 f2.w2 f2.r2,
      locusInterferes_symm f1.wm f1.rm f2.wm f2.rm]

/-- Global footprint disjointness is symmetric. -/
theorem isDisjoint_symm (f1 f2 : Footprint) :
    isDisjoint f1 f2 = isDisjoint f2 f1 := by
  dsimp [isDisjoint]
  rw [interferes_symm]

/-- Standard footprint for local operations on Locus 1. -/
def fpL1 (r w : Bool) : Footprint :=
  { r1 := r, r2 := false, rm := false, w1 := w, w2 := false, wm := false }

/-- Standard footprint for local operations on Locus 2. -/
def fpL2 (r w : Bool) : Footprint :=
  { r1 := false, r2 := r, rm := false, w1 := false, w2 := w, wm := false }

/-- Standard footprint for local operations on Message Locus M. -/
def fpM (r w : Bool) : Footprint :=
  { r1 := false, r2 := false, rm := r, w1 := false, w2 := false, wm := w }

/-- Local operations on L1 and L2 have disjoint footprints for all access modes. -/
theorem fpL1_fpL2_disjoint (r1 w1 r2 w2 : Bool) :
    isDisjoint (fpL1 r1 w1) (fpL2 r2 w2) = true := by
  cases r1 <;> cases w1 <;> cases r2 <;> cases w2 <;> rfl

/-- Local operations on L1 and M have disjoint footprints for all access modes. -/
theorem fpL1_fpM_disjoint (r1 w1 rm wm : Bool) :
    isDisjoint (fpL1 r1 w1) (fpM rm wm) = true := by
  cases r1 <;> cases w1 <;> cases rm <;> cases wm <;> rfl

/-- Local operations on L2 and M have disjoint footprints for all access modes. -/
theorem fpL2_fpM_disjoint (r2 w2 rm wm : Bool) :
    isDisjoint (fpL2 r2 w2) (fpM rm wm) = true := by
  cases r2 <;> cases w2 <;> cases rm <;> cases wm <;> rfl

/-- Two writes to L1 interfere (write-write conflict). -/
theorem fpL1_write_conflict : interferes (fpL1 false true) (fpL1 false true) = true := by
  decide

/-- A read and a write to L1 interfere (read-write conflict). -/
theorem fpL1_read_write_conflict : interferes (fpL1 true false) (fpL1 false true) = true := by
  decide

/-- Specification that an operation preserves unwritten coordinates. -/
def PreservesUnwritten (fp : Footprint) (op : State3 → State3) : Prop :=
  (fp.w1 = false → ∀ s, (op s).l1 = s.l1) ∧
  (fp.w2 = false → ∀ s, (op s).l2 = s.l2) ∧
  (fp.wm = false → ∀ s, (op s).m = s.m)

/-- Two states agree on all coordinates read by a footprint. -/
def AgreesOnReads (fp : Footprint) (s s' : State3) : Prop :=
  (fp.r1 = true → s.l1 = s'.l1) ∧
  (fp.r2 = true → s.l2 = s'.l2) ∧
  (fp.rm = true → s.m = s'.m)

/-- Specification that an operation's write values depend strictly on its read set. -/
def ReadsOnly (fp : Footprint) (op : State3 → State3) : Prop :=
  ∀ s s', AgreesOnReads fp s s' →
    (fp.w1 = true → (op s).l1 = (op s').l1) ∧
    (fp.w2 = true → (op s).l2 = (op s').l2) ∧
    (fp.wm = true → (op s).m = (op s').m)

/-- An operation respects a footprint if it preserves unwritten loci and reads only declared loci. -/
structure Respects (fp : Footprint) (op : State3 → State3) : Prop where
  preserves : PreservesUnwritten fp op
  readsOnly : ReadsOnly fp op

/-- Local update at L1 respects fpL1 true true. -/
theorem updateL1_respects (f : Nat → Nat) :
    Respects (fpL1 true true) (updateL1 f) where
  preserves := by
    dsimp [PreservesUnwritten, fpL1]
    exact ⟨fun h => Bool.noConfusion h, fun _ _ => rfl, fun _ _ => rfl⟩
  readsOnly := by
    intro s s' hAgr
    dsimp [fpL1] at *
    refine ⟨?_, fun h => Bool.noConfusion h, fun h => Bool.noConfusion h⟩
    intro _
    dsimp [updateL1]
    rw [hAgr.1 rfl]

/-- Local update at L2 respects fpL2 true true. -/
theorem updateL2_respects (g : Nat → Nat) :
    Respects (fpL2 true true) (updateL2 g) where
  preserves := by
    dsimp [PreservesUnwritten, fpL2]
    exact ⟨fun _ _ => rfl, fun h => Bool.noConfusion h, fun _ _ => rfl⟩
  readsOnly := by
    intro s s' hAgr
    dsimp [fpL2] at *
    refine ⟨fun h => Bool.noConfusion h, ?_, fun h => Bool.noConfusion h⟩
    intro _
    dsimp [updateL2]
    rw [hAgr.2.1 rfl]

/-- Local update at M respects fpM true true. -/
theorem updateM_respects (h : Nat → Nat) :
    Respects (fpM true true) (updateM h) where
  preserves := by
    dsimp [PreservesUnwritten, fpM]
    exact ⟨fun _ _ => rfl, fun _ _ => rfl, fun h => Bool.noConfusion h⟩
  readsOnly := by
    intro s s' hAgr
    dsimp [fpM] at *
    refine ⟨fun h => Bool.noConfusion h, fun h => Bool.noConfusion h, ?_⟩
    intro _
    dsimp [updateM]
    rw [hAgr.2.2 rfl]

/-- If f1 reads L1 and f1, f2 are disjoint, then f2 does not write L1. -/
theorem not_w1_of_r1_disjoint {f1 f2 : Footprint} (h : isDisjoint f1 f2 = true) (hr : f1.r1 = true) :
    f2.w1 = false := by
  rcases f1 with ⟨r1, r2, rm, w1, w2, wm⟩
  rcases f2 with ⟨r1', r2', rm', w1', w2', wm'⟩
  revert r1 r2 rm w1 w2 wm r1' r2' rm' w1' w2' wm'
  decide

/-- If f1 reads L2 and f1, f2 are disjoint, then f2 does not write L2. -/
theorem not_w2_of_r2_disjoint {f1 f2 : Footprint} (h : isDisjoint f1 f2 = true) (hr : f1.r2 = true) :
    f2.w2 = false := by
  rcases f1 with ⟨r1, r2, rm, w1, w2, wm⟩
  rcases f2 with ⟨r1', r2', rm', w1', w2', wm'⟩
  revert r1 r2 rm w1 w2 wm r1' r2' rm' w1' w2' wm'
  decide

/-- If f1 reads M and f1, f2 are disjoint, then f2 does not write M. -/
theorem not_wm_of_rm_disjoint {f1 f2 : Footprint} (h : isDisjoint f1 f2 = true) (hr : f1.rm = true) :
    f2.wm = false := by
  rcases f1 with ⟨r1, r2, rm, w1, w2, wm⟩
  rcases f2 with ⟨r1', r2', rm', w1', w2', wm'⟩
  revert r1 r2 rm w1 w2 wm r1' r2' rm' w1' w2' wm'
  decide

/-- If f1 and f2 are disjoint, they cannot both write to L1. -/
theorem not_both_w1_disjoint {f1 f2 : Footprint} (h : isDisjoint f1 f2 = true)
    (hw1 : f1.w1 = true) (hw2 : f2.w1 = true) : False := by
  rcases f1 with ⟨r1, r2, rm, w1, w2, wm⟩
  rcases f2 with ⟨r1', r2', rm', w1', w2', wm'⟩
  revert r1 r2 rm w1 w2 wm r1' r2' rm' w1' w2' wm'
  decide

/-- If f1 and f2 are disjoint, they cannot both write to L2. -/
theorem not_both_w2_disjoint {f1 f2 : Footprint} (h : isDisjoint f1 f2 = true)
    (hw1 : f1.w2 = true) (hw2 : f2.w2 = true) : False := by
  rcases f1 with ⟨r1, r2, rm, w1, w2, wm⟩
  rcases f2 with ⟨r1', r2', rm', w1', w2', wm'⟩
  revert r1 r2 rm w1 w2 wm r1' r2' rm' w1' w2' wm'
  decide

/-- If f1 and f2 are disjoint, they cannot both write to M. -/
theorem not_both_wm_disjoint {f1 f2 : Footprint} (h : isDisjoint f1 f2 = true)
    (hw1 : f1.wm = true) (hw2 : f2.wm = true) : False := by
  rcases f1 with ⟨r1, r2, rm, w1, w2, wm⟩
  rcases f2 with ⟨r1', r2', rm', w1', w2', wm'⟩
  revert r1 r2 rm w1 w2 wm r1' r2' rm' w1' w2' wm'
  decide

end Concurrency
