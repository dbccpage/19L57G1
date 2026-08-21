# Finite Lift/Descent Assessment

## Result

At sealed snapshot `f74ea9b7e40741429f74708c1f7671647b0962b6`, an
unqualified endogenous-push conclusion is **not established**.  The result is
instead a source-boundary analysis plus a separate declared finite fixture.
After that fixture admits a seed, labels, an anchor, and a successor grammar,
it has function-level lift identity/composition laws, a certificate-restricted
retraction, and a replayed active-edge counter.  None of those facts constructs
the fixture from an arbitrary native stage.

This distinction is decisive: the positive construction records what is
sufficient for one connected model, while the source analysis records why its
load-bearing inputs cannot be silently called derived structure.

## Pinned source boundary

The following are theorems at the manifest-pinned source bytes, not new
derivations.

| Source result | Exact scope | Consequence here |
|---|---|---|
| `lean4/Derivation/ContactKernel.lean:504-510` | The displayed all-collapse Boolean observer has no complement witness. | A claim that every raw source observer begins with an internally available positive witness is false. |
| `lean4/Derivation/PresentationNaturality.lean:316-339` | For the Boolean equality observer and its negation presentation map, a raw section exists but no natural one does. | A presentation-stable singleton choice is not automatic in that particular family. |
| `lean4/Derivation/PresentationNaturality.lean:403-432` | A different four-point presentation has a natural section. | The Boolean obstruction is not a general no-selector theorem. |
| `lean4/Derivation/ObsDescent.lean:100-206` | Quotient descent exists precisely under class constancy; the binary form has its corresponding compatibility condition. | A raw interface does not provide an arbitrary quotient descent without its stated premise. |
| `lean4/Derivation/DiffInterface.lean:237-255` | An extension is proposal data and is not applied by the interface. | A proposal does not select or authorize a successor. |
| `lean4/Derivation/DiffInterface.lean:297-370,485-493` | A concrete declared natural-number family has a pointwise successor witness, explicitly not a trace object. | The source does contain local successor material, but it is not a construction from every native stage nor a connected replay trace. |

Thus two different limits must be kept apart.  One source instance has no
first complement witness at all.  In another, a raw choice exists but a
presentation-natural singleton choice fails.  Neither limit says that every
witness is absent or that every presentation lacks a natural choice.

## Separate declared fixture

`finite_tower.py` explicitly records these inputs:

1. the two-label initial carrier;
2. the seed edge and its interpretation as an initial positive relation;
3. a distinguished anchor;
4. the next-index fresh-label convention;
5. the one-edge successor grammar;
6. the rule that settles the current active edges; and
7. the replay schedule of one lift followed by one closure.

These are not supplied by a map from `Derivation.DiffInterface.Stage` to the
fixture’s `Stage`, nor is any such map defined in the Lean development.  The
main trace is therefore deterministic only **after labelled admissions**.  It
does not model a quotient by presentation maps or prove uniqueness under a
presentation action; the separate two-pair swap calculation is only a finite
negative fixture.

The Lean fixture takes `Point n = Fin (n + 2)`.  Its declared map lift
`upMap` satisfies identity and composition (`upMap_id`, `upMap_comp`, and
`towerUpMorphism_comp_certified`).  These are function-level functorial laws;
no Lean category/functor object, adjunction, or general functor pair has been
declared.

`LiftedMap` stores a parent map and a proof that the raw map is its lift.
Accordingly, `towerDown_after_towerUp` proves
`D (U f) = f` only on the certified lift image.  Because `LiftedMap` stores
its parent, that equation holds by `rfl`; the fact with content is
`clampedRestriction_certified`, which computes the parent from the raw map and
finds the stored one.  This is a split retraction,
not an inverse or canonical descent for arbitrary larger maps.  The separate
total `clampedRestriction` operation shows the loss explicitly:
`down_freshPoint` maps the fresh point to the anchor.  It is also distinct
from the pinned source’s quotient descent, which has its own compatibility
premise.

The fixture’s `ReplayState` contains only a declared level and active-edge
counter.  Its completed rounds have the following Lean facts:

- `replay_rounds_succ`: append the named declared round;
- `replay_rounds_level`: reach the stated counter level;
- `replay_rounds_closed`: set the declared active counter to zero; and
- `replay_rounds_preserve_anchor`: retain the two-anchor distinction.

These theorems quantify over every natural index of the explicitly declared
move-counter schema.  They do not identify that counter with
`DiffInterface.ActiveObstruction`, construct finite source states, or give an
endogenous unbounded tower from raw data.

## Finite receipt and candidate boundary

`receipts/finite_tower_0_15.json` is the byte-stable report for completed
stages 0 through 15.  Its SHA-256 is
`C35E5DCCB3253C0263B8BB4295E33F39FCA1313B8E11570B538D493E0FDB3232`.
For each of the fifteen emitted lift/closure transitions, it checks a strict
drop in the declared active-edge measure; it also checks exact replay and
old-edge retention for the emitted stages, that a certificate-free structural
descent of each emitted lift (remove the fresh label and the extension edge
named by the last event, then drop that event) agrees with the certified
`down`, and that `down` refuses a record whose target `up` did not produce.
An earlier receipt also listed `descent_after_certified_up_is_identity`.  That
entry was true by construction, since `down` returns the parent stored in the
record, and it was removed so that every listed law is one that can fail.

The candidate grammar is exhaustive only over its five listed kinds and their
declared status/cost labels.  In it, `aggregate_all_carrier` and
`aggregate_active_orbit` are distinct retained aggregate candidates with the
same declared cost.  This does not prove global minimality.  The
`observer_extension` case is open because no compatible local grammar is
provided; it is not refuted.  The two-pair swap rejects a stable singleton
choice only in its displayed finite orbit and is not a proof about every
presentation selector.

## Imported-choice boundary

| Needed for the positive fixture | Status at the raw source boundary |
|---|---|
| A distinguished initial pair / anchor | Not derived by the fixture.  A witness is absent in the collapse countermodel; a raw choice can also be presentation-sensitive. |
| A finite carrier and ordered fresh label | Declared labelling and enumeration convention. |
| A seed relation and one-edge extension | Declared successor vocabulary rather than a forced choice from proposal data. |
| A closure operation and repeat schedule | Declared replay machinery, not identified with the native semantic obstruction. |
| Descent for every candidate map | Not supplied: `D` only retracts certified lifts, and source quotient descent has a compatibility premise. |
| A rule eliminating aggregate ties | Not supplied by the declared grammar. |

In this report, saying the raw input has “no container” means only that it
does not derive this fixture’s distinguished finite carrier, labels, seed, and
enumeration as a state record.  It is not an ontological statement that no
system can be represented by a container.

## Verification boundary

None of the checks below is run by `.github/workflows/verify.yml`, and nothing
under `ci/` reads this tree.  Each item is a manual receipt for the tree it was
run on, and it goes stale silently until someone reruns it.  The commands,
from the repository root, with the last two run inside
`research/primitive_difference_tower/`:

    python research/primitive_difference_tower/verify_manifest.py
    python research/primitive_difference_tower/verify_lean.py
    python -m unittest discover -s . -p "test_*.py"
    python -m mypy

`verify_manifest.py` prints the commit it ran at.  A repin after a sealed
change is `verify_manifest.py --repin`, which rewrites the module hashes from
the blobs at `HEAD`, moves the snapshot there, and then fails until the prose
citing the old snapshot is revised.

Passed on the tree committed with this wording:

- `verify_manifest.py`: every listed source hash against the canonical Git
  blob at the verification commit; the transitive-citation policy in both
  directions against the imports and qualified symbol uses in
  `PrimitiveDifferenceTower.lean`; the source snapshot is an ancestor of
  `HEAD` and no commit since it touched a protected path, walked with
  `git log --full-history` so that a touch a later commit reverts is still
  refused; the protected working tree is clean; the committed receipt equals
  `render_report(15)`, and its hash and the snapshot commit are cited here
  and in `CLAIM_LEDGER.md`.  Untracked protected paths are reported as local,
  non-Git/blob inputs rather than compared with an author-specific baseline.
  The verifier does not require `HEAD` to equal the pre-research snapshot.
- `verify_lean.py`: the forbidden-token scan over the three research Lean
  files; `lake build PrimitiveDifferenceTower.AxiomReport`, then
  `lake env lean` on the report file; the nine `#print axioms` lines parsed,
  each axiom list checked to lie within `{propext, Quot.sound}` (six depend
  on exactly that pair, three on no axioms), and the nine names checked
  against the inventory written in `AxiomReport.lean`.  The reach is that
  inventory only.  An earlier version of this script only looked for each
  name as a substring of the output, which a disallowed axiom would not have
  disturbed; a plain `lake build` now elaborates `AxiomReport.lean` because
  the lakefile names it as a root, but the audit does not rely on that.
- 32 standard-library unit tests under Python 3.14.2, and `mypy --strict`
  over the four modules and three test files.  The tests include negative
  cases for the former defects: an axiom list containing `Classical.choice`
  with the declaration name still present, a transitive module used without
  an explicit citation, a citation naming an unused symbol, a commit touching
  a protected path that the endpoint diff cannot see, an undecided ancestry
  query, a backslash-encoded `..` path, an unterminated string literal, a
  stale receipt, and prose that drops the receipt hash.

Not established or not run:

- Every receipt above was produced on Windows, with Lean `v4.33.0`.  Paths in
  verifier output are rendered with POSIX separators and no test asserts a
  platform-specific form, but no other platform was run.
- No global candidate-space enumeration or presentation quotient was
  performed.
- No formal bridge maps an arbitrary native stage or source active obstruction
  to this fixture.
- No universal impossibility theorem, physical interpretation, or external
  theory claim is issued.

No sealed source, artifact, paper, prompt, or derivation file was modified.
