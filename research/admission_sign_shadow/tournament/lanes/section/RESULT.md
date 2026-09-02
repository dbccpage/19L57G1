# Section lane result

AuthorityEffect: None.

## Result

Status: **CONDITIONAL**.

The module `lean/AdmissionSignShadow/ActualSectionAdapter.lean` states the
adapter against the exact types in
`lean4/Derivation/PresentationNaturality.lean`:

- `Family` at line 222;
- `Sec` at line 232;
- `IsNatural` at line 236;
- `PresIso.mapPair` as the arrow transport used by naturality.

The right-inverse law is not decorative.  `fiberOf` turns the
chosen representative into a value of `ReportFiber report q`, and `Kernel`
accepts only that typed fibre value.  `Kernel.toSec_isNatural` is the exact
arrow-commutation obligation.

## Negative instance

Status: **REFUTED**.

`report_section_does_not_determine_actual_section` applies the inhabited unit
report to the exact fixed-point-free family
`autoFamily ContactKernel.boolEqObs negIso` and contradicts
`no_natural_section_boolEq`.  `fixed_point_free_family_has_no_kernel` lifts
the same counterexample to the kernel type.

## Inputs that remain supplied

Status: **OPEN**.

- `query : D.Obj → Q`;
- `pairOf`, including each `NonZeroPair` proof;
- exact commutation under every declared `PresIso.mapPair`;
- an actual report section for a general report map;
- optional independence from the chosen right inverse;
- the corresponding varying-carrier kernel for `HFamily`.

Neither a report right inverse nor an existing natural section derives these
cross-interface maps.  The lane therefore closes the type and proof shape,
not the source of the adapter data.

## Narrow compatibility build

Status: **PROVED**.

Lean 4.33.0 elaborated the module against the exact frozen
`Derivation.PresentationNaturality` interface and its twelve-module import
closure, assembled only in an untracked temporary build root.  The semantic
root was Git blob `ef4d76c7a07d38966150923691d1a0bba65bde68`, the blob pinned at
the admission packet's frozen commit
`3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`.  No sealed source was copied into
the tracked tree.

The narrow axiom audit reports that all four promoted theorems depend on no
axioms:

- `Kernel.toSec_isNatural`;
- `no_kernel_of_no_actual_section`;
- `report_section_does_not_determine_actual_section`;
- `fixed_point_free_family_has_no_kernel`.

## Shared integration

Status: **PROVED** for compatibility replay. The module is intentionally not
added to the standalone local Lake root because it consumes the exact frozen
interface; the shared ephemeral verifier builds it and checks the exact
declaration census.

## Lane verdict

`ACTUAL_SECTION_ADAPTER`: **CONDITIONAL**.

`ACTUAL_SECTION_ADAPTER_FROM_EXISTING_DATA`: **OPEN**.
