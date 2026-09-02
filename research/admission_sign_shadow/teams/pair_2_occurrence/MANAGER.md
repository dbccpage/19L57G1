# Pair 2 manager: strongest count result

AuthorityEffect: None.

## Promoted theorems

- `occurrence_valid_append`
- `countToken_nil`
- `countToken_append`
- `countToken_perm`
- `perm_occurrence_equivalent`
- `occurrence_equivalent_refl`
- `occurrence_equivalent_symm`
- `occurrence_equivalent_trans`
- `canonical_forget_same_count_differs`
- `count_equivalent_but_ordered_forget_differs`
- `canonical_data_does_not_determine_count`
- `count_calibration_unique`
- `calibrated_occurrence_weight`
- `occurrenceWeight_zero`
- `occurrenceWeight_append`
- `separating_weight_does_not_factor`
- `zero_weight_factors_through_forget`

## Manager finding

Canonical deduplicated data does not recover occurrence count.  Count is
well-defined and additive only after the occurrence-sensitive list and its
identifier-validity rule are DECLARED.  A unit-calibrated integer map is unique
and agrees with the nonnegative count, but the calibration is IMPORTED rather
than produced by the admission state.

The repaired factorization statements are exact: a map that separates counts
`1` and `2` cannot factor through canonical deduplication, while the zero map
can.  Count equivalence does not identify ordered forgetful lists.

Still OPEN are identifier-renaming invariance, a replayable occurrence event
and forgetful projection tied to the frozen model, and a derivation of unit
calibration.

## Verdict

**IMPORT ISOLATED BUT NOT REMOVED**.

Advice to the final decider: accept the impossibility and conditional count
algebra, but do not treat multiplicity or its integer calibration as canonical
admission data.
