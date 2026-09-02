# Pair 2 proofer: occurrence count and declared integer map

AuthorityEffect: None.

## Proposed lane

The frozen admission state deduplicates repeated tokens.  The proposal first
proves that such canonical data cannot determine how many separately named
occurrences were presented.  The witness histories `once` and `twice` have the
same ordered deduplicated result and different counts.

A separate occurrence-sensitive extension declares an occurrence identifier
and token for each list entry.  Identifier uniqueness is validity data.  Inside
that extension, token count has a zero law, is additive under append, and is
invariant under list permutation.  Mapping the count to an integer is kept as
an explicit argument.

The proposed strong result is a nonfactorization theorem for a count-separating
map, paired with a zero-map counterexample showing that not every declared map
fails to factor.

## Source classification

- PROVED: canonical dedup data does not determine token count; count zero,
  append, and permutation laws; conditional integer-map laws.
- DECLARED: occurrence identifiers, append-on-repeat semantics, and the map
  from a count to an integer.
- IMPORTED: unit calibration when the integer map is required to agree with
  ordinary counting.
- OPEN: deriving occurrence identifiers, append-on-repeat semantics, or the
  unit calibration from canonical admission.

Manager verdict: **IMPORT ISOLATED BUT NOT REMOVED**.
