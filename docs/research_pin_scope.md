# Whole-directory source pin scope

AuthorityEffect: None.

## Correction dated 2026-09-19

The source manifests in `research/represented_execution/` and
`research/setting_translation/` retain their historical scope text because
`research/record_reading/verify_sources.py` freezes their complete bytes.
Editing even the scope field makes that downstream custody check fail.

Any exact-consumption reading of those two historical scope statements is
withdrawn here: whole-directory pins establish custody of the listed
directories. They do not assert that the computation imports or reads every
pinned file. Their tree census is not a compiled transitive import closure.
No source digest, tree object, file census, baseline, or verifier is changed
by this clarification.

The same dated clarification is recorded directly in the source manifests
of `ignition`, `local_reuse`, `magnification`, `reachable`, `record_reading`,
`unboundedness`, and `iso_sound`. All nine families retain their existing
whole-directory custody pins.
