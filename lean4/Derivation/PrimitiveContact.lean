import Derivation.PrimitiveCore
import Derivation.PrimitiveCats

/-!
# Primitive contact: the collision protocol and its input status

Phases III–V of the contact-and-passage run.

The run protocol declares a contact package

    contact/omega_primdiff/
      CONTACT_MANIFEST.json
      lean4/
      prose/

to be read in two stages (Lean before prose), each only after the
corresponding native commitment.  **The package is absent from the
repository**: no `contact/` directory exists at the pre-contact commit
(`blind-native-base`) or at completion.  Per the protocol, the native
phases complete and the contact phases terminate with
`CONTACT_INPUT_ABSENT`; no contents are invented, no comparison is
fabricated, and no agreement pressure exists.

What this module does record, so that any FUTURE contact meets a fixed
interface rather than a movable one:

1. the native kernel, bound under its contact-facing name — the class
   of settings carrying a pointed witnessed irreflexive relation
   (candidate A of `PrimitiveCore`), inhabited by the two-element
   oriented realization;
2. the proved status the kernel brings to any collision: the complete
   72-cell implication/countermodel matrix over the nine candidate
   readings (`PrimitiveCore.matrixCells`), initiality of the
   two-element carrier in the pointed witnessed category
   (`PrimitiveCats.d2_initial`), the retained orientation fork
   (`PrimitiveCats.s2_initial_sym`, `PrimitiveCats.s2_not_weakly_initial`),
   and the observer-branching theorem
   (`PrimitiveCats.no_terminal_pres`);
3. the collision discipline that would apply: statements only, never
   comments; assumption graphs and axiom reports per supplied theorem;
   for every notion pair exactly one of equivalence-under-hypotheses,
   one-direction-with-countermodel, incomparability, or common-third
   realization.
-/

namespace PrimitiveContact

/-- The contact terminal for this run. -/
def contactStatus : String := "CONTACT_INPUT_ABSENT"

/-- The native kernel, under its contact-facing name: settings
carrying a pointed witnessed irreflexive relation. -/
def NativeKernel : Type 1 :=
  { S : PrimitiveCore.Setting // PrimitiveCore.A S }

/-- The kernel is inhabited by the oriented two-element realization
(bare: empty retention, protection, and operation stores). -/
def nativeKernelWitness : NativeKernel :=
  ⟨{ X := Bool, r := PrimDiff.D2, a := false, b := true,
     ret := fun _ _ => False, prot := fun _ _ => False,
     Ops := fun _ => False },
   ⟨PrimDiff.D2_witness, PrimDiff.D2_irrefl⟩⟩

/-- The kernel's carrier of record is initial in the pointed
witnessed category — the strongest universal status the native side
brings to any future collision (proved, not postured:
`PrimitiveCats.d2_initial`). -/
theorem native_kernel_initial : PrimitiveCats.Initial
    PrimitiveCats.d2Obj := PrimitiveCats.d2_initial

end PrimitiveContact
