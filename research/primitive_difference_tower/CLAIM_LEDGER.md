# Claim Ledger

The classifications below distinguish source theorems, declared fixture
inputs, theorems within that separate fixture, and finite computation.  A
green receipt does not change a classification.

| ID | Classification | Scoped statement | Evidence |
|---|---|---|---|
| PDT-0 | METATHEORETIC RECEIPT | The listed sealed source bytes and protected-path boundary are pinned at `f74ea9b7e40741429f74708c1f7671647b0962b6` / tree `4755d647c83db9926a2465e71c51aabb078cba9c`. | `verify_manifest.py` pass; `SOURCE_MANIFEST.json`. This is not a mathematical proof. |
| PDT-1 | IMPORTED COUNTERMODEL | The displayed all-collapse Boolean observer has no complement witness. | `ContactKernel.kernel_no_witness_from_collapse`, explicitly cited in the manifest and re-exported locally. This refutes a universal source-to-witness claim only. |
| PDT-2 | IMPORTED, PRESENTATION-SCOPED OBSTRUCTION | In the Boolean equality/negation family, a raw section exists but no natural single-pair section exists. | `PresentationNaturality.selection_is_possible_naturality_is_not`, re-exported as `raw_bool_single_pair_selector_exists` and `no_bool_single_pair_selector`. It does not rule out a natural section for every presentation. |
| PDT-3 | DECLARED FIXTURE INPUT | The two-label seed, seed relation, anchor, fresh-label enumeration, successor grammar, closure rule, and replay schedule are inputs to the positive construction. | `finite_tower.CONDITIONAL_ADMISSIONS`; fixture comments and `DeclaredRoundStep` in `lean/PrimitiveDifferenceTower.lean`. No bridge derives them from a native stage. |
| PDT-4 | THEOREM WITHIN DECLARED FIXTURE | The declared function lift preserves identity and composition.  Certified descent is a retraction on the lift image, while fresh-point clamping is explicitly lossy. | Lean: `upMap_id`, `upMap_comp`, `towerUpMorphism_comp_certified`, `towerDown_after_towerUp`, `fresh_not_in_upPoint_image`, `down_freshPoint`. No category/functor object or total descent is claimed. |
| PDT-5 | THEOREM WITHIN DECLARED FIXTURE | The declared move-counter schema replays to its indicated level, closes the declared active counter after every round, and retains its two anchors. | Lean: `replay_rounds_succ`, `replay_rounds_level`, `replay_rounds_closed`, `replay_rounds_preserve_anchor`. The counter is not identified with `DiffInterface.ActiveObstruction`. |
| PDT-6 | DETERMINISTIC FINITE COMPUTATION | Through stages 0 through 15, every emitted history replays exactly, old edges are retained, every emitted lift/closure transition lowers the declared active-edge measure, and certified up/down identity holds. | `receipts/finite_tower_0_15.json`, SHA-256 `ED444E23F3D567C731A264FF142081A1982F825DFE11C7D4F6953A0B77BFB1B1`; eight standard-library unit tests. |
| PDT-7 | DETERMINISTIC, GRAMMAR-SCOPED CLASSIFICATION | The two aggregate candidates tie under the declared cost/status classification and are retained.  The displayed two-pair swap rejects a stable singleton choice in that orbit. | `candidate_grammar`, `retained_ties`, and `symmetric_single_pair_failure` in `finite_tower.py`. This is not a global candidate census, a general presentation theorem, or a rejection of aggregates. |
| PDT-8 | OPEN / NOT ESTABLISHED | An arbitrary native stage with no added naming, presentation, or successor data uniquely compels this construction. | No formal bridge maps arbitrary `DiffInterface.Stage` data into PDT-3, and no presentation quotient is modeled for the main trace. The countermodels locate missing inputs but do not prove a universal no-go theorem. |

## Exact conclusion

The construction is valid only after PDT-3.  It does not turn PDT-3 into
derived structure.  Source-level quotient descent has a separate
class-constancy premise; the fixture's named descent only returns the parent
stored in a certified lift record.  Those operations must not be conflated.
