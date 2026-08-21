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
`D (U f) = f` only on the certified lift image.  This is a split retraction,
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
`ED444E23F3D567C731A264FF142081A1982F825DFE11C7D4F6953A0B77BFB1B1`.
For each of the fifteen emitted lift/closure transitions, it checks a strict
drop in the declared active-edge measure; it also checks exact replay, old-edge
retention, and certified up/down identity for the emitted stages.

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

Passed:

- `verify_manifest.py` checked the exact commit/tree, every listed source
  hash, the manifest's explicit transitive-citation declarations, and the
  unchanged sealed protected paths plus their baseline untracked set.  The
  successful Lean build separately resolved the cited source symbols used by
  the local fixture.
- The local Lean package built, including `AxiomReport`; the reported fixture
  results use only the displayed standard library axioms or none.  The build
  emitted only pre-existing unused-variable linter warnings in
  `Derivation/Apartness.lean`.
- A local forbidden-token scan found no `sorry`, `admit`, `unsafe`, `partial`,
  or user-declared `axiom` in the research Lean files.
- Eight standard-library Python unit tests passed, and the generated receipt
  matched `render_report(15)` byte-for-byte.  These executions used the
  available Python 3.9 runtime.

Not established or not run:

- No Python 3.14 verification or strict type-check was run in this session, so
  neither is claimed as a receipt.
- No global candidate-space enumeration or presentation quotient was
  performed.
- No formal bridge maps an arbitrary native stage or source active obstruction
  to this fixture.
- No universal impossibility theorem, physical interpretation, or external
  theory claim is issued.

No sealed source, artifact, paper, prompt, or derivation file was modified.
