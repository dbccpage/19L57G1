# Section lane symbol packet

AuthorityEffect: None.

Only the statuses `PROVED`, `CONDITIONAL`, `REFUTED`, and `OPEN` occur in
the status column.

| symbol | status | exact scope |
|---|---|---|
| `ActualSectionAdapter.ReportFiber` | PROVED | Exact fibre `{a // report a = q}` for the supplied report map. |
| `ActualSectionAdapter.fiberOf` | PROVED | Uses `ReportSection.rightInverse` to inhabit the requested fibre. |
| `ActualSectionAdapter.Kernel` | CONDITIONAL | Supplied `query`, fibre-to-`NonZeroPair` map, and exact `PresIso.mapPair` commutation for `PresentationNaturality.Family`. |
| `ActualSectionAdapter.Kernel.toSec` | PROVED | Produces the exact `PresentationNaturality.Sec` from a supplied kernel and report section. |
| `ActualSectionAdapter.Kernel.toSec_isNatural` | PROVED | Produces the exact `PresentationNaturality.IsNatural` proof from `Kernel.commutes`. |
| `ActualSectionAdapter.Kernel.adapt` | PROVED | Packages the exact section and naturality proof. |
| `ActualSectionAdapter.no_kernel_of_no_actual_section` | PROVED | An inhabited report section plus failure of an actual natural section refutes kernel existence. |
| `ActualSectionAdapter.report_section_does_not_determine_actual_section` | REFUTED | Bare report-section data cannot produce a natural section for the exact fixed-point-free family. |
| `ActualSectionAdapter.fixed_point_free_family_has_no_kernel` | REFUTED | The exact fixed-point-free family has no kernel for the inhabited unit report. |
| `NARROW_EXACT_INTERFACE_BUILD` | PROVED | Lean 4.33.0 elaborates the module against the frozen `Derivation.PresentationNaturality` import closure in an untracked temporary build root. |
| `NARROW_AXIOM_PACKET` | PROVED | The four promoted theorems below report no dependencies. |
| `SHARED_COMPATIBILITY_RECEIPT` | PROVED | The shared ephemeral verifier binds the exact source hashes and four-declaration axiom census. |
| `ACTUAL_SECTION_ADAPTER_FROM_EXISTING_DATA` | OPEN | No existing premise derives `query`, `pairOf`, or `commutes`. |
| `HETEROGENEOUS_ACTUAL_SECTION_ADAPTER` | OPEN | No `HFamily`/`HSec`/`HIsNatural` adapter is supplied in this lane. |
| `REPORT_SECTION_INDEPENDENT_OUTPUT` | OPEN | Fibre constancy across different right inverses is not required or proved. |

## Import boundary

`Derivation.PresentationNaturality` supplies the exact family, pair transport,
section, and naturality types.  `AdmissionSignShadow.Core` supplies the report
section only.  The kernel fields are new supplied data; neither imported side
constructs them.

The semantic-root blob is `ef4d76c7a07d38966150923691d1a0bba65bde68`
at the admission packet's frozen commit
`3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`.  The same blob occurs at the
natural-sections source snapshot used to enumerate its twelve-module import
closure.  The compatibility build extracted every path in that closure from
the admission packet's frozen commit; it did not substitute the later closure
blobs.  This is compatibility evidence, not a new tracked copy.
