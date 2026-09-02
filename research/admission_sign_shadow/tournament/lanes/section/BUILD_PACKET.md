# Section lane build packet

AuthorityEffect: None.

Only the statuses `PROVED`, `CONDITIONAL`, `REFUTED`, and `OPEN` occur in
the status column.

| obligation | status | evidence |
|---|---|---|
| Local core build | PROVED | `lake build AdmissionSignShadow` under `leanprover/lean4:v4.33.0`. |
| Exact interface compatibility | PROVED | The shared verifier materialized the exact frozen tree ephemerally and built the exact target. |
| Tracked sealed-source copy | REFUTED | The persistent exact-source match census is empty; identical toolchain text is recorded separately as apparatus. |
| Shared receipt registration | PROVED | `receipts/frozen_compatibility.json` carries the exact four-declaration report census. |

## Source identity

The exact semantic-root input was
`lean4/Derivation/PresentationNaturality.lean` at Git blob
`ef4d76c7a07d38966150923691d1a0bba65bde68`.  That is the blob recorded by
`research/admission_sign_shadow/SOURCE_MANIFEST.json` at frozen commit
`3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`. The build declares the entire
exact frozen `lean4` tree at that commit as its allowed compatibility input
and imports only the closure Lean resolves for this target. It does not
substitute later transitive blobs.

## Axiom packet

Status: **PROVED**.

The narrow audit emitted:

```text
'AdmissionSignShadow.ActualSectionAdapter.Kernel.toSec_isNatural' does not depend on any axioms
'AdmissionSignShadow.ActualSectionAdapter.no_kernel_of_no_actual_section' does not depend on any axioms
'AdmissionSignShadow.ActualSectionAdapter.report_section_does_not_determine_actual_section' does not depend on any axioms
'AdmissionSignShadow.ActualSectionAdapter.fixed_point_free_family_has_no_kernel' does not depend on any axioms
```

## Interpretation

The compatibility result is **PROVED**.  Kernel existence remains
**CONDITIONAL**, because `query`, `pairOf`, and `commutes` are supplied fields.
Derivation of those fields from the existing report or presentation-natural
interfaces remains **OPEN**.
