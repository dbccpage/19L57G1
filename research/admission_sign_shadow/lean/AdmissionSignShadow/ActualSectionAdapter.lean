import AdmissionSignShadow.Core
import Derivation.PresentationNaturality

/-!
# Actual section adapter

This compatibility module targets the exact `Family`, `Sec`, and
`IsNatural` types exported by `Derivation.PresentationNaturality`.
It does not change that source and does not infer any adapter data.

The report fibre makes the right-inverse law operational: the representative
passed to `pairOf` carries a proof that it reports to the query at that
object.  The one `commutes` field is exactly the `PresIso.mapPair` equation
required by `IsNatural`.

AuthorityEffect: None.
-/

namespace AdmissionSignShadow.ActualSectionAdapter

open ContactKernel DiffInterface PresentationNaturality

/-- The representatives of one report value. -/
def ReportFiber {A Q : Type} (report : A → Q) (q : Q) : Type :=
  {a : A // report a = q}

/-- A report section supplies a representative in the requested fibre.
The subtype proof is its right-inverse law. -/
def fiberOf {A Q : Type} {report : A → Q}
    (reportSection : AdmissionSignShadow.ReportSection A Q report) (q : Q) :
    ReportFiber report q :=
  ⟨reportSection.choose q, reportSection.rightInverse q⟩

/-- The minimal supplied data converting every report section into a section
of the exact presentation family.  No field is derived by this structure. -/
structure Kernel {A Q X R : Type} (report : A → Q) (D : Family X R) where
  query : D.Obj → Q
  pairOf : (object : D.Obj) →
    ReportFiber report (query object) → NonZeroPair (D.obs object)
  commutes : ∀
    (reportSection : AdmissionSignShadow.ReportSection A Q report)
    (arrow : D.Arr),
      (D.iso arrow).mapPair
          (pairOf (D.src arrow)
            (fiberOf reportSection (query (D.src arrow)))) =
        pairOf (D.tgt arrow)
          (fiberOf reportSection (query (D.tgt arrow)))

/-- Apply a supplied kernel to a supplied report section. -/
def Kernel.toSec {A Q X R : Type} {report : A → Q} {D : Family X R}
    (kernel : Kernel report D)
    (reportSection : AdmissionSignShadow.ReportSection A Q report) : Sec D :=
  fun object =>
    kernel.pairOf object (fiberOf reportSection (kernel.query object))

/-- The kernel's commuting field is exactly actual naturality. -/
theorem Kernel.toSec_isNatural {A Q X R : Type} {report : A → Q}
    {D : Family X R} (kernel : Kernel report D)
    (reportSection : AdmissionSignShadow.ReportSection A Q report) :
    IsNatural D (kernel.toSec reportSection) := by
  intro arrow
  exact kernel.commutes reportSection arrow

/-- Package the produced section with its exact naturality proof. -/
def Kernel.adapt {A Q X R : Type} {report : A → Q} {D : Family X R}
    (kernel : Kernel report D)
    (reportSection : AdmissionSignShadow.ReportSection A Q report) :
    {chosen : Sec D // IsNatural D chosen} :=
  ⟨kernel.toSec reportSection, kernel.toSec_isNatural reportSection⟩

/-- If one report section exists but the actual family has no natural
section, then no kernel of this type exists. -/
theorem no_kernel_of_no_actual_section {A Q X R : Type} {report : A → Q}
    {D : Family X R}
    (reportSection : AdmissionSignShadow.ReportSection A Q report)
    (noSection : ¬ ∃ chosen : Sec D, IsNatural D chosen) :
    ¬ Nonempty (Kernel report D) := by
  rintro ⟨kernel⟩
  exact noSection
    ⟨kernel.toSec reportSection, kernel.toSec_isNatural reportSection⟩

/-- The supplied unit report section cannot produce an actual natural
section for the fixed-point-free Boolean family. -/
theorem report_section_does_not_determine_actual_section :
    ¬ (AdmissionSignShadow.ReportSection Unit Unit AdmissionSignShadow.unitReport →
      ∃ chosen : Sec (autoFamily ContactKernel.boolEqObs negIso),
        IsNatural (autoFamily ContactKernel.boolEqObs negIso) chosen) := by
  intro produce
  exact no_natural_section_boolEq
    (produce AdmissionSignShadow.unitReportSection)

/-- The same negative result at the kernel type. -/
theorem fixed_point_free_family_has_no_kernel :
    ¬ Nonempty
      (Kernel AdmissionSignShadow.unitReport
        (autoFamily ContactKernel.boolEqObs negIso)) :=
  no_kernel_of_no_actual_section AdmissionSignShadow.unitReportSection
    no_natural_section_boolEq

#print axioms Kernel.toSec_isNatural
#print axioms no_kernel_of_no_actual_section
#print axioms report_section_does_not_determine_actual_section
#print axioms fixed_point_free_family_has_no_kernel

end AdmissionSignShadow.ActualSectionAdapter
