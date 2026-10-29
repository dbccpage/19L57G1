"""Unit 53 check: kernel-check the book's Lean for Unit 53.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u53_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimitiveContact

namespace Textbook.U53
open PrimitiveContact PrimitiveCore

/-- The witness's setting is Unit 51's `d2Bare`, field for field. -/
theorem witness_is_d2Bare : nativeKernelWitness.val = d2Bare := rfl

/-- What the kernel's membership proof says: the pair is asserted and the
relation is irreflexive. -/
theorem witness_reading_A :
    nativeKernelWitness.val.r nativeKernelWitness.val.a nativeKernelWitness.val.b ∧
    PrimDiff.Irrefl nativeKernelWitness.val.r :=
  nativeKernelWitness.property

/-- What A brings, read off Unit 51: the endpoints apart (`imp_a_d`) and,
with no operations admitted, irreducibility (`e_empty_iff_d`). -/
theorem witness_endpoints_apart : D nativeKernelWitness.val :=
  imp_a_d _ nativeKernelWitness.property

theorem witness_irreducible : E nativeKernelWitness.val :=
  (e_empty_iff_d _ rfl).mpr witness_endpoints_apart

/-- Every member of the kernel has its endpoints apart: the interface
promises D to any arrival, by Unit 51's `imp_a_d`. -/
theorem kernel_endpoints_apart (K : NativeKernel) : K.val.a ≠ K.val.b :=
  (D_iff_ne _).mp (imp_a_d _ K.property)

/-- The kernel is not a single object: the symmetric two-point setting
is a member too (the orientation fork, retained). -/
def symMember : NativeKernel := ⟨s2Bare, s2Bare_bs.1⟩

theorem two_members : nativeKernelWitness.val ≠ symMember.val := by
  intro h
  have h2 : HEq nativeKernelWitness.val.r symMember.val.r := by rw [h]
  have h3 : PrimDiff.D2 = PrimDiff.S2 := eq_of_heq h2
  have h4 : PrimDiff.S2 true false := Or.inr PrimDiff.D2_witness
  rw [← h3] at h4
  exact Bool.noConfusion h4.1

/-- The object of record is the witness's setting read as a `PtdRel`:
same carrier, relation and points. -/
theorem object_of_record :
    PrimitiveCats.d2Obj.X = nativeKernelWitness.val.X ∧
    PrimitiveCats.d2Obj.r = nativeKernelWitness.val.r ∧
    PrimitiveCats.d2Obj.a = nativeKernelWitness.val.a ∧
    PrimitiveCats.d2Obj.b = nativeKernelWitness.val.b :=
  ⟨rfl, rfl, rfl, rfl⟩

/-- Equality of proofs of this proposition; proof irrelevance means
this equality alone is not a provenance check. The source names the re-export. -/
theorem initial_is_reexport : native_kernel_initial = PrimitiveCats.d2_initial := rfl

/-- Why no observer complement is the oriented witness: an observer's
apartness is symmetric (its zero relation is), and `D2` is not. -/
theorem d2_not_symmetric : ¬ ∀ x y, PrimDiff.D2 x y → PrimDiff.D2 y x := by
  intro h
  exact Bool.noConfusion (h false true PrimDiff.D2_witness).1

theorem apart_symmetric {R : Type} (O : DiffInterface.DiffObs Bool R) :
    ∀ x y, ContactBridge.obsApart O x y → ContactBridge.obsApart O y x :=
  ContactBridge.obsApart_symm O

theorem not_representable_by_symmetry :
    ¬ ∃ (R : Type) (O : DiffInterface.DiffObs Bool R),
        ∀ x y, ContactBridge.obsApart O x y ↔ PrimDiff.D2 x y := by
  rintro ⟨R, O, hO⟩
  apply d2_not_symmetric
  intro x y hxy
  exact (hO y x).mp (apart_symmetric O x y ((hO x y).mpr hxy))

/-- The status strings, read: the sealed terminal is the first history
entry's prefix, and the current status is the second's. -/
theorem history_reads :
    contactStatusHistory.length = 2 ∧
    (contactStatusHistory.head? = some
      "CONTACT_INPUT_ABSENT (pre-contact, blind-native-base ccd3a53)") ∧
    contactStatus = "CONTACT_INPUT_ABSENT" ∧
    contactStatusCurrent = "CONTACT_PROCESSED_LEAN_ONLY" :=
  ⟨rfl, rfl, rfl, rfl⟩

theorem sealed_differs_from_current : contactStatus ≠ contactStatusCurrent := by
  decide

/-- The interface contains a symmetric member that an observer does represent.
The oriented witness's refutation is not a refutation of every member. -/
theorem symmetric_member_representable :
    ∃ O : DiffInterface.DiffObs Bool Prop,
      ∀ x y, ContactBridge.obsApart O x y ↔ symMember.val.r x y :=
  ContactBridge.bool_bs_repr PrimDiff.S2 (Or.inl PrimDiff.D2_witness)
    PrimDiff.S2_irrefl Apartness.s2_isApart.symm

end Textbook.U53

#print axioms Textbook.U53.witness_is_d2Bare
#print axioms Textbook.U53.witness_reading_A
#print axioms Textbook.U53.witness_endpoints_apart
#print axioms Textbook.U53.witness_irreducible
#print axioms Textbook.U53.kernel_endpoints_apart
#print axioms Textbook.U53.two_members
#print axioms Textbook.U53.object_of_record
#print axioms Textbook.U53.initial_is_reexport
#print axioms Textbook.U53.d2_not_symmetric
#print axioms Textbook.U53.apart_symmetric
#print axioms Textbook.U53.not_representable_by_symmetry
#print axioms Textbook.U53.history_reads
#print axioms Textbook.U53.sealed_differs_from_current
#print axioms Textbook.U53.symmetric_member_representable
#print axioms PrimitiveContact.native_kernel_initial
#print axioms PrimitiveContact.contact_status_count
#print axioms PrimitiveContact.native_interface_not_representable
#print axioms ContactBridge.d2_not_obs_complement
#print axioms ContactBridge.obsApart_symm
"""

EXPECTED = {
    "Textbook.U53.witness_is_d2Bare": NONE,
    "Textbook.U53.witness_reading_A": NONE,
    "Textbook.U53.witness_endpoints_apart": NONE,
    "Textbook.U53.witness_irreducible": NONE,
    "Textbook.U53.kernel_endpoints_apart": NONE,
    "Textbook.U53.two_members": NONE,
    "Textbook.U53.object_of_record": NONE,
    "Textbook.U53.initial_is_reexport": QUOT,
    "Textbook.U53.d2_not_symmetric": NONE,
    "Textbook.U53.apart_symmetric": NONE,
    "Textbook.U53.not_representable_by_symmetry": NONE,
    "Textbook.U53.history_reads": NONE,
    "Textbook.U53.sealed_differs_from_current": NONE,
    "Textbook.U53.symmetric_member_representable": NONE,
    "PrimitiveContact.native_kernel_initial": QUOT,
    "PrimitiveContact.contact_status_count": NONE,
    "PrimitiveContact.native_interface_not_representable": NONE,
    "ContactBridge.d2_not_obs_complement": NONE,
    "ContactBridge.obsApart_symm": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U53"))
