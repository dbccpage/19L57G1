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

## File pins replace directory pins, 2026-09-25

Nine of the twelve whole-directory custody families now pin the files they
consume instead of whole directories: `record_reading`, `unboundedness`,
`ignition`, `local_reuse`, `magnification`, `reachable`, `iso_sound`,
`alpha_engine` and `f_class_distinctness`. The statement above that all
nine named families retain their whole-directory pins is withdrawn for
the seven of them converted here.

- **How consumption was measured.** As in pull request #254: every Python
  file of the tree imported in a child interpreter, with the tree first on
  the path and `code/` last; the tree's tests and `run.py --check` run under
  an audit hook that records files opened outside the tree; and the Lean
  import closure of the tree's own modules through the `path` requires of
  its Lake configuration. In every tree the Python loaded equals the
  runtime modules already pinned by digest, so only the Lean side moved.
- **What each verifier pins now.** Its runtime modules, Lean configuration
  and artifacts, as before, and `LEAN_PATHS`: the Lean files of the
  import closure (from 1 file for `alpha_engine` to 45 for
  `unboundedness`), each by digest at the tree's unchanged baseline,
  compared with the working tree and covered by its tracked-diff check.
  The manifests drop `consumed_trees` and `tree_census`, bump their schema,
  and refuse either field by name (`MANIFEST_TREE_PINS`).
- **What no longer fails.** A change to a file beside the pinned ones that
  the tree does not read, and an untracked file there. A build or an import
  picks such a file up only if a pinned file imports it, and that edit fails
  as `SOURCE_CHANGED`; an extra Python module also fails the runtime census.
- **Gaps closed.** `iso_sound` read the sealed `tests/test_iso.py` by path
  without pinning it; it is now pinned. `unboundedness` consumed the Lake
  configuration of `research/magnification/lean` through its require chain
  without pinning it; it is now pinned.
- **Over-pins left in place.** Every family still pins `lean4/Derivation.lean`,
  which none of them imports, and `ignition`, `magnification` and
  `reachable` pin export summaries that only `reachable` reads. They are
  file pins, not directory pins, and removing them changes no coupling.

### Left open

`coherent_process_limits`, `represented_execution` and `setting_translation`
keep their whole-directory pins. Each is pinned whole by a downstream
custody verifier that runs `git diff` over its directory:
`represented_execution` by `coherent_process_limits`, and
`setting_translation` by both of those. Editing their manifests or
verifiers would turn the downstream verifier red. `record_reading`, which
also pinned all three whole, no longer does. The chain can now be converted
in order, `coherent_process_limits` first, then `represented_execution`,
then `setting_translation`, each as its own measured change with its own
repin. Measured on 2026-09-25, none of the three has a consumed input that
its directory pins miss.
