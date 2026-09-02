# Pair 2 adversary: validity, quotient, and factorization attacks

AuthorityEffect: None.

## Attacks

1. The first append witness reused identifier `0` on both sides, so the
   combined history was invalid.  Additivity must either assume disjoint
   identifiers or refresh the right-hand identifiers before append.
2. Count equivalence is insensitive to order, while the canonical forgetful
   list retains first-occurrence order.  Count equivalence therefore cannot be
   claimed to quotient that ordered list.
3. The first nonfactorization wording was too broad.  The count itself, and
   any count-separating integer map, fail to factor through deduplication; the
   constant-zero map does factor.
4. Reorder invariance of counts is weaker than a complete occurrence-identifier
   equivalence.  Identifier renaming and replay through an admitted occurrence
   event were not proved.
5. Additivity alone does not supply unit calibration.  The calibration must be
   a premise, followed by a uniqueness theorem, or remain OPEN.

## Repaired status

The current tree adds disjoint-identifier append, reflexive/symmetric/transitive
count equivalence, the ordered-forget counterexample, calibration uniqueness,
the calibrated count theorem, the separating-map nonfactorization theorem,
and the zero-map factorization witness.

Identifier-renaming invariance, a replayable occurrence-admission projection,
and derivation of calibration remain OPEN.

Manager verdict: **IMPORT ISOLATED BUT NOT REMOVED**.
