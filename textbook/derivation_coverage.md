# Derivation Coverage Matrix and Lesson Dependency Graph

**AuthorityEffect: None.** This is a source-placement index and a recorded
prerequisite graph. It is not a certification that every declaration is
explained or that every prerequisite is taught before use.

**2026-11-01 continuation:** the author requested deeper declaration coverage.
[Batch 1](audit/DECLARATION_COVERAGE_BATCH_01_2026-11-01.md) reconciles a
bounded 53-head sealed/research cluster with actual teaching and identifies
five explanation/scope gaps. Its findings supplement the proposed placement
below; they do not certify the other entries as taught.

The existing index records:

1. Every frozen module under `lean4/Derivation/` (all 75 modules: 62 directly
   imported by `lean4/Derivation.lean`, 63 in its transitive import closure,
   and the remaining 12 parked modules imported by
   `lean4/ParkedAudit.lean`) and its mapping to Part 1 textbook units
   (`Unit 00`–`Unit 74`) and module audit records (`textbook/audit/modules/`).
2. Proposed declaration placement across those modules: a **Substantive
   textbook lesson** (`S`), **Auxiliary dependency** (`A`), **Technical
   appendix / audit record**, or **Proposed omission with justification**.
   Some entries group names or use ellipses. Their presence does not prove
   exhaustive declaration coverage or substantive teaching of each entry.
3. Every research theorem taught in Part 2 (`textbook/institutions/units/00`–`17`),
   identifying its originating research tree (`research/actor_institution`,
   `research/two_theorems`, `research/uncollapse`,
   `research/interpreter_verdict`) and its exact evidence classification.
4. The explicitly recorded prerequisite edges among the formal units.
   Checking these edges for cycles does not discover missing conceptual
   prerequisites. The beginner routes and the
   [formal-reading guide](reading_formal_statements.md) address some of them.

The old opening's total of 708 definitions/structures/inductives did not
match its historical inventory's counters. A fresh
[source/compiled reconciliation](audit/DECLARATION_REVIEW_2026-10-28.md)
excludes 20 comment matches and includes ten unnamed instance declarations.
Its restricted source scan finds 2,564 declaration heads, each matched to
one same-module compiled Lean declaration at the recorded source location:
1,676 theorem heads and 888 other heads. The latter include 763 `def`,
68 `structure`, 38 `inductive`, nine `abbrev`, and ten `instance` heads.
Fields, constructors, and generated constants are a separate population.
These counts describe the scan, not complete semantic teaching coverage;
the historical inventory and module records remain preserved.

## 1. Evidence Status Classifications

Every declaration in this matrix carries one or more of the seven status marks:

- `FROZEN` — Historical source custody: the declaration belongs to the
  sealed derivation (`lean4/Derivation/`). This mark alone does not say
  that a declaration is a theorem or that its hypotheses hold. Definitions
  remain admitted choices; theorems establish their stated conclusions
  under their exact hypotheses. Kernel and axiom-audit evidence is separate
  from that custody mark.
- `POST_FREEZE_PROVED` — Proved in a post-freeze research tree under
  `research/` (`uncollapse`, `two_theorems`, `interpreter_verdict`,
  `actor_institution`), kernel-checked in Lean 4.33.0 with zero `sorry` and
  axioms within `{propext, Quot.sound}`. **Historical boundary:** A
  `POST_FREEZE_PROVED` theorem may explain or sharpen a question raised by the
  sealed derivation, and never alters or retroactively enters the sealed
  derivation.
- `CONDITIONAL` — Proved in Lean under explicit hypotheses (`Regime.wf`,
  decidability assumptions, fiber-constancy, or scope assumptions); the
  theorem establishes the implication from those hypotheses, not that the
  hypotheses are forced.
- `VERIFIED_FINITE` — Computational evidence on an explicitly declared
  finite population. Read each row's actual statement and evidence: a
  kernel-checked theorem about a finite carrier remains a theorem, and a
  concrete counterexample can refute a universal claim. Tactics such as
  `rfl` or `decide` alone do not determine a theorem's quantifier scope.
  The existing row classifications still need semantic reconciliation.
- `REFUTED` — A formal counterexample or negative theorem refuting a candidate
  bridge, uniqueness claim, or overstrong statement.
- `ADMITTED` — A declared structure, inductive grammar, cost measure,
  representation choice, or requirement. A price applies only where a
  specific model's cost rule assigns one. A definition is not a derivation.
- `OPEN` — An unresolved mathematical obligation (`InterpreterBoundary`'s
  `OpenBridgeObligation` / `ResearchInterpreterVerdict.openDenotationalBridge`,
  and institutional wisdom beyond non-overclaiming `Grounded`). Preserved as
  open; never taught as solved.

---

## 2. Module-to-Lesson Summary Matrix (All 75 Frozen Modules + Root)

| # | Module | Path | Root Import | Lines | Matched other heads | Matched theorem heads | Primary Textbook Units | Audit Appendix |
|---|---|---|---|---|---|---|---|---|
| 0 | `Derivation` (root) | `lean4/Derivation.lean` | root | 1642 | 0 | 0 | Part 1 source index (`Unit 00`–`Unit 74`) | [`audit/README.md`](audit/README.md) |
| 1 | `Apartness` | `lean4/Derivation/Apartness.lean` | yes | 337 | 6 | 28 | `Unit 56` | [`audit/modules/Apartness.md`](audit/modules/Apartness.md) |
| 2 | `Attachment` | `lean4/Derivation/Attachment.lean` | yes | 1172 | 41 | 54 | `Unit 59` | [`audit/modules/Attachment.md`](audit/modules/Attachment.md) |
| 3 | `Basic` | `lean4/Derivation/Basic.lean` | yes | 217 | 23 | 7 | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` | [`audit/modules/Basic.md`](audit/modules/Basic.md) |
| 4 | `BoundaryCancellation` | `lean4/Derivation/BoundaryCancellation.lean` | yes | 661 | 7 | 37 | `Unit 60` | [`audit/modules/BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md) |
| 5 | `Breaking` | `lean4/Derivation/Breaking.lean` | yes | 445 | 18 | 15 | `Unit 73` | [`audit/modules/Breaking.md`](audit/modules/Breaking.md) |
| 6 | `Bridge` | `lean4/Derivation/Bridge.lean` | yes | 316 | 5 | 12 | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` | [`audit/modules/Bridge.md`](audit/modules/Bridge.md) |
| 7 | `CapacityBound` | `lean4/Derivation/CapacityBound.lean` | yes | 254 | 3 | 10 | `Unit 42` | [`audit/modules/CapacityBound.md`](audit/modules/CapacityBound.md) |
| 8 | `ClosureSymmetry` | `lean4/Derivation/ClosureSymmetry.lean` | yes | 166 | 4 | 7 | `Unit 71` | [`audit/modules/ClosureSymmetry.md`](audit/modules/ClosureSymmetry.md) |
| 9 | `Completion` | `lean4/Derivation/Completion.lean` | yes | 529 | 14 | 22 | `Unit 46` | [`audit/modules/Completion.md`](audit/modules/Completion.md) |
| 10 | `Composing` | `lean4/Derivation/Composing.lean` | no (`ParkedAudit.lean`) | 228 | 11 | 7 | `Unit 73` | [`audit/modules/Composing.md`](audit/modules/Composing.md) |
| 11 | `Compression` | `lean4/Derivation/Compression.lean` | yes | 787 | 14 | 38 | `Unit 61` | [`audit/modules/Compression.md`](audit/modules/Compression.md) |
| 12 | `Constitution` | `lean4/Derivation/Constitution.lean` | yes | 393 | 13 | 16 | `Unit 48` | [`audit/modules/Constitution.md`](audit/modules/Constitution.md) |
| 13 | `ContactBridge` | `lean4/Derivation/ContactBridge.lean` | yes | 710 | 9 | 35 | `Unit 53`, `Unit 68` | [`audit/modules/ContactBridge.md`](audit/modules/ContactBridge.md) |
| 14 | `ContactKernel` | `lean4/Derivation/ContactKernel.lean` | yes | 1025 | 25 | 53 | `Unit 69` | [`audit/modules/ContactKernel.md`](audit/modules/ContactKernel.md) |
| 15 | `ControllerCategory` | `lean4/Derivation/ControllerCategory.lean` | yes | 774 | 39 | 63 | `Unit 58` | [`audit/modules/ControllerCategory.md`](audit/modules/ControllerCategory.md) |
| 16 | `CountTransport` | `lean4/Derivation/CountTransport.lean` | yes | 306 | 6 | 13 | `Unit 29` | [`audit/modules/CountTransport.md`](audit/modules/CountTransport.md) |
| 17 | `Counting` | `lean4/Derivation/Counting.lean` | yes | 86 | 1 | 4 | `Unit 28` | [`audit/modules/Counting.md`](audit/modules/Counting.md) |
| 18 | `DiffAnchor` | `lean4/Derivation/DiffAnchor.lean` | no (`ParkedAudit.lean`) | 73 | 1 | 3 | `Unit 68` | [`audit/modules/DiffAnchor.md`](audit/modules/DiffAnchor.md) |
| 19 | `DiffAnchorCompat` | `lean4/Derivation/DiffAnchorCompat.lean` | no (`ParkedAudit.lean`) | 17 | 0 | 0 | `Unit 68` | [`audit/modules/DiffAnchorCompat.md`](audit/modules/DiffAnchorCompat.md) |
| 20 | `DiffInterface` | `lean4/Derivation/DiffInterface.lean` | yes | 761 | 41 | 35 | `Unit 44` | [`audit/modules/DiffInterface.md`](audit/modules/DiffInterface.md) |
| 21 | `EndogenousFidelityGenerator` | `lean4/Derivation/EndogenousFidelityGenerator.lean` | yes | 109 | 4 | 6 | `Unit 72` | [`audit/modules/EndogenousFidelityGenerator.md`](audit/modules/EndogenousFidelityGenerator.md) |
| 22 | `Erasure` | `lean4/Derivation/Erasure.lean` | yes | 161 | 7 | 4 | `Unit 06`, `Unit 07` | [`audit/modules/Erasure.md`](audit/modules/Erasure.md) |
| 23 | `Ext` | `lean4/Derivation/Ext.lean` | yes | 179 | 3 | 12 | `Unit 36` | [`audit/modules/Ext.md`](audit/modules/Ext.md) |
| 24 | `FidelityClosure` | `lean4/Derivation/FidelityClosure.lean` | yes | 234 | 14 | 11 | `Unit 72` | [`audit/modules/FidelityClosure.md`](audit/modules/FidelityClosure.md) |
| 25 | `FormRenaming` | `lean4/Derivation/FormRenaming.lean` | no (`ParkedAudit.lean`) | 147 | 3 | 9 | `Unit 74` | [`audit/modules/FormRenaming.md`](audit/modules/FormRenaming.md) |
| 26 | `FormTransport` | `lean4/Derivation/FormTransport.lean` | no (`ParkedAudit.lean`) | 196 | 1 | 11 | `Unit 74` | [`audit/modules/FormTransport.md`](audit/modules/FormTransport.md) |
| 27 | `FormTransportCompat` | `lean4/Derivation/FormTransportCompat.lean` | no (`ParkedAudit.lean`) | 23 | 0 | 0 | `Unit 74` | [`audit/modules/FormTransportCompat.md`](audit/modules/FormTransportCompat.md) |
| 28 | `G1Class` | `lean4/Derivation/G1Class.lean` | yes | 45 | 0 | 3 | `Unit 43` | [`audit/modules/G1Class.md`](audit/modules/G1Class.md) |
| 29 | `Generator` | `lean4/Derivation/Generator.lean` | yes | 296 | 4 | 16 | `Unit 40` | [`audit/modules/Generator.md`](audit/modules/Generator.md) |
| 30 | `GraphGenesis` | `lean4/Derivation/GraphGenesis.lean` | yes | 720 | 12 | 28 | `Unit 63` | [`audit/modules/GraphGenesis.md`](audit/modules/GraphGenesis.md) |
| 31 | `HigherStructure` | `lean4/Derivation/HigherStructure.lean` | yes | 816 | 34 | 39 | `Unit 55` | [`audit/modules/HigherStructure.md`](audit/modules/HigherStructure.md) |
| 32 | `Horizon` | `lean4/Derivation/Horizon.lean` | yes | 424 | 7 | 26 | `Unit 50` | [`audit/modules/Horizon.md`](audit/modules/Horizon.md) |
| 33 | `Inertia` | `lean4/Derivation/Inertia.lean` | yes | 94 | 1 | 10 | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` | [`audit/modules/Inertia.md`](audit/modules/Inertia.md) |
| 34 | `Initiality` | `lean4/Derivation/Initiality.lean` | yes | 171 | 11 | 11 | `Unit 49` | [`audit/modules/Initiality.md`](audit/modules/Initiality.md) |
| 35 | `InterpreterBoundary` | `lean4/Derivation/InterpreterBoundary.lean` | yes | 394 | 13 | 13 | `Unit 57` | [`audit/modules/InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md) |
| 36 | `IsoBridge` | `lean4/Derivation/IsoBridge.lean` | no (`ParkedAudit.lean`) | 75 | 1 | 0 | `Unit 74` | [`audit/modules/IsoBridge.md`](audit/modules/IsoBridge.md) |
| 37 | `IsoBridgeCompat` | `lean4/Derivation/IsoBridgeCompat.lean` | no (`ParkedAudit.lean`) | 17 | 0 | 0 | `Unit 74` | [`audit/modules/IsoBridgeCompat.md`](audit/modules/IsoBridgeCompat.md) |
| 38 | `IsoCanon` | `lean4/Derivation/IsoCanon.lean` | no (`ParkedAudit.lean`) | 232 | 4 | 10 | `Unit 74` | [`audit/modules/IsoCanon.md`](audit/modules/IsoCanon.md) |
| 39 | `IsoCanonCompat` | `lean4/Derivation/IsoCanonCompat.lean` | no (`ParkedAudit.lean`) | 17 | 0 | 0 | `Unit 74` | [`audit/modules/IsoCanonCompat.md`](audit/modules/IsoCanonCompat.md) |
| 40 | `IsoCollapse` | `lean4/Derivation/IsoCollapse.lean` | no (`ParkedAudit.lean`) | 177 | 3 | 8 | `Unit 74` | [`audit/modules/IsoCollapse.md`](audit/modules/IsoCollapse.md) |
| 41 | `IsoCollapseCompat` | `lean4/Derivation/IsoCollapseCompat.lean` | no (`ParkedAudit.lean`) | 17 | 0 | 0 | `Unit 74` | [`audit/modules/IsoCollapseCompat.md`](audit/modules/IsoCollapseCompat.md) |
| 42 | `LadderGeneral` | `lean4/Derivation/LadderGeneral.lean` | yes | 329 | 22 | 13 | `Unit 60` | [`audit/modules/LadderGeneral.md`](audit/modules/LadderGeneral.md) |
| 43 | `LocalStrategy` | `lean4/Derivation/LocalStrategy.lean` | no (`ParkedAudit.lean`) | 262 | 18 | 23 | `Unit 43` | [`audit/modules/LocalStrategy.md`](audit/modules/LocalStrategy.md) |
| 44 | `Mention` | `lean4/Derivation/Mention.lean` | yes | 199 | 0 | 7 | `Unit 12`, `Unit 30` | [`audit/modules/Mention.md`](audit/modules/Mention.md) |
| 45 | `Minimality` | `lean4/Derivation/Minimality.lean` | yes | 487 | 16 | 26 | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` | [`audit/modules/Minimality.md`](audit/modules/Minimality.md) |
| 46 | `MinimalityF` | `lean4/Derivation/MinimalityF.lean` | yes | 197 | 4 | 2 | `Unit 32` | [`audit/modules/MinimalityF.md`](audit/modules/MinimalityF.md) |
| 47 | `NoOutside` | `lean4/Derivation/NoOutside.lean` | yes | 270 | 7 | 12 | `Unit 47` | [`audit/modules/NoOutside.md`](audit/modules/NoOutside.md) |
| 48 | `NoOutsideFidelity` | `lean4/Derivation/NoOutsideFidelity.lean` | yes | 105 | 2 | 6 | `Unit 72` | [`audit/modules/NoOutsideFidelity.md`](audit/modules/NoOutsideFidelity.md) |
| 49 | `ObsDescent` | `lean4/Derivation/ObsDescent.lean` | yes | 539 | 8 | 37 | `Unit 67` | [`audit/modules/ObsDescent.md`](audit/modules/ObsDescent.md) |
| 50 | `ObserverInventory` | `lean4/Derivation/ObserverInventory.lean` | yes | 231 | 9 | 17 | `Unit 37` | [`audit/modules/ObserverInventory.md`](audit/modules/ObserverInventory.md) |
| 51 | `Pigeonhole` | `lean4/Derivation/Pigeonhole.lean` | yes | 232 | 1 | 11 | `Unit 42` | [`audit/modules/Pigeonhole.md`](audit/modules/Pigeonhole.md) |
| 52 | `PresentationDescent` | `lean4/Derivation/PresentationDescent.lean` | yes | 225 | 9 | 7 | `Unit 72` | [`audit/modules/PresentationDescent.md`](audit/modules/PresentationDescent.md) |
| 53 | `PresentationNaturality` | `lean4/Derivation/PresentationNaturality.lean` | yes | 665 | 40 | 29 | `Unit 70` | [`audit/modules/PresentationNaturality.md`](audit/modules/PresentationNaturality.md) |
| 54 | `PresentationRelativity` | `lean4/Derivation/PresentationRelativity.lean` | yes | 637 | 19 | 32 | `Unit 71` | [`audit/modules/PresentationRelativity.md`](audit/modules/PresentationRelativity.md) |
| 55 | `PrimDiff` | `lean4/Derivation/PrimDiff.lean` | yes | 545 | 14 | 44 | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` | [`audit/modules/PrimDiff.md`](audit/modules/PrimDiff.md) |
| 56 | `PrimitiveCats` | `lean4/Derivation/PrimitiveCats.lean` | yes | 721 | 32 | 49 | `Unit 52` | [`audit/modules/PrimitiveCats.md`](audit/modules/PrimitiveCats.md) |
| 57 | `PrimitiveContact` | `lean4/Derivation/PrimitiveContact.lean` | yes | 142 | 6 | 3 | `Unit 53` | [`audit/modules/PrimitiveContact.md`](audit/modules/PrimitiveContact.md) |
| 58 | `PrimitiveCore` | `lean4/Derivation/PrimitiveCore.lean` | yes | 918 | 33 | 129 | `Unit 51` | [`audit/modules/PrimitiveCore.md`](audit/modules/PrimitiveCore.md) |
| 59 | `PrimitivePassage` | `lean4/Derivation/PrimitivePassage.lean` | yes | 1298 | 31 | 58 | `Unit 54` | [`audit/modules/PrimitivePassage.md`](audit/modules/PrimitivePassage.md) |
| 60 | `Progress` | `lean4/Derivation/Progress.lean` | yes | 237 | 0 | 6 | `Unit 35` | [`audit/modules/Progress.md`](audit/modules/Progress.md) |
| 61 | `Quot` | `lean4/Derivation/Quot.lean` | yes | 37 | 1 | 3 | `Unit 27` | [`audit/modules/Quot.md`](audit/modules/Quot.md) |
| 62 | `QuotientRetention` | `lean4/Derivation/QuotientRetention.lean` | yes | 143 | 2 | 9 | `Unit 72` | [`audit/modules/QuotientRetention.md`](audit/modules/QuotientRetention.md) |
| 63 | `Refusal` | `lean4/Derivation/Refusal.lean` | yes | 289 | 13 | 18 | `Unit 38` | [`audit/modules/Refusal.md`](audit/modules/Refusal.md) |
| 64 | `RefusalFrontier` | `lean4/Derivation/RefusalFrontier.lean` | yes | 371 | 16 | 20 | `Unit 39` | [`audit/modules/RefusalFrontier.md`](audit/modules/RefusalFrontier.md) |
| 65 | `RenamingStructure` | `lean4/Derivation/RenamingStructure.lean` | yes | 482 | 5 | 28 | `Unit 59` | [`audit/modules/RenamingStructure.md`](audit/modules/RenamingStructure.md) |
| 66 | `Represented` | `lean4/Derivation/Represented.lean` | yes | 1363 | 50 | 65 | `Unit 45` | [`audit/modules/Represented.md`](audit/modules/Represented.md) |
| 67 | `ResidualClosure` | `lean4/Derivation/ResidualClosure.lean` | yes | 122 | 1 | 7 | `Unit 71` | [`audit/modules/ResidualClosure.md`](audit/modules/ResidualClosure.md) |
| 68 | `Rounds` | `lean4/Derivation/Rounds.lean` | yes | 482 | 2 | 25 | `Unit 34` | [`audit/modules/Rounds.md`](audit/modules/Rounds.md) |
| 69 | `RuleBridge` | `lean4/Derivation/RuleBridge.lean` | yes | 268 | 1 | 8 | `Unit 33` | [`audit/modules/RuleBridge.md`](audit/modules/RuleBridge.md) |
| 70 | `SeparationCapacity` | `lean4/Derivation/SeparationCapacity.lean` | yes | 238 | 2 | 14 | `Unit 41` | [`audit/modules/SeparationCapacity.md`](audit/modules/SeparationCapacity.md) |
| 71 | `StableContent` | `lean4/Derivation/StableContent.lean` | yes | 582 | 11 | 18 | `Unit 62` | [`audit/modules/StableContent.md`](audit/modules/StableContent.md) |
| 72 | `TraceAlgebra` | `lean4/Derivation/TraceAlgebra.lean` | yes | 1001 | 18 | 72 | `Unit 66` | [`audit/modules/TraceAlgebra.md`](audit/modules/TraceAlgebra.md) |
| 73 | `TransitionAlphabet` | `lean4/Derivation/TransitionAlphabet.lean` | yes | 1893 | 66 | 118 | `Unit 65` | [`audit/modules/TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md) |
| 74 | `TransitionTransport` | `lean4/Derivation/TransitionTransport.lean` | yes | 1070 | 11 | 53 | `Unit 31` | [`audit/modules/TransitionTransport.md`](audit/modules/TransitionTransport.md) |
| 75 | `WeightProfile` | `lean4/Derivation/WeightProfile.lean` | yes | 522 | 15 | 31 | `Unit 64` | [`audit/modules/WeightProfile.md`](audit/modules/WeightProfile.md) |

---

The source-head columns above are the reconciled scan's counts, excluding
constructors, structure fields, and generated declarations. “Other”
includes definitions, abbreviations, structures, inductives, and explicit
instance heads. A Lean `structure` elaborates to an inductive plus several
other constants; the two populations must not be added together. Line
counts are physical source lines, excluding a phantom line after a final
newline. Neither the number of heads nor the assigned unit proves that
each concept has been taught.

## 3. Lesson Dependency Graph and Acyclicity Verification

The tables record prerequisites for Part 1 (`Unit 00`–`Unit 74`) and
Part 2 (`Part 2 Unit 00`–`17`). Their declared edges can be checked for
ordering and cycles. That check does not establish that every term is
introduced before use. For example, Unit 44's original prerequisite list
assumed Lean setoids and quotients; its revised explanation and the Map lab
now introduce their grouping meaning. Further conceptual review remains.

### 3.1 Part 1: Frozen Derivation Curriculum (`Unit 00`–`Unit 74`)

| Unit | File | Title | Frozen Modules Covered | Prerequisite Units |
|---|---|---|---|---|
| `Unit 00` | [`units/00_mark_and_constructor.md`](units/00_mark_and_constructor.md) | The mark and the external constructor | `Basic` | None (entry point after `START_HERE.md`) |
| `Unit 01` | [`units/01_genesis_underivable.md`](units/01_genesis_underivable.md) | Nothing is derivable at genesis | `Inertia` | `Unit 00` |
| `Unit 02` | [`units/02_underivable_of_empty.md`](units/02_underivable_of_empty.md) | Nothing is derivable without instances or rules | `Inertia` | `Unit 01` |
| `Unit 03` | [`units/03_supply_no_op.md`](units/03_supply_no_op.md) | Supplying a token changes nothing | `Inertia` | `Unit 01` |
| `Unit 04` | [`units/04_no_forced_successor.md`](units/04_no_forced_successor.md) | No successor is internally forced | `Inertia` | `Unit 01`, `Unit 02`, `Unit 03` |
| `Unit 05` | [`units/05_two_readings.md`](units/05_two_readings.md) | Is the mark admitted? Readings L and F | `Inertia` | `Unit 01`, `Unit 03` |
| `Unit 06` | [`units/06_readmission_designates.md`](units/06_readmission_designates.md) | Re-admitting a token designates, it does not add | `Erasure` | `Unit 03`, `Unit 05` |
| `Unit 07` | [`units/07_erasure.md`](units/07_erasure.md) | Forgetting tokens loses nothing the room can use | `Erasure` | `Unit 06` |
| `Unit 08` | [`units/08_contexts_and_collapse.md`](units/08_contexts_and_collapse.md) | Contexts, plugging, collapsed, separable | `Basic` | `Unit 01`, `Unit 07` |
| `Unit 09` | [`units/09_separable_not_collapsed.md`](units/09_separable_not_collapsed.md) | Separable and collapsed exclude each other | `Basic` | `Unit 08` |
| `Unit 10` | [`units/10_collapsed_of_no_insts.md`](units/10_collapsed_of_no_insts.md) | With no instances, every pair is collapsed | `Inertia` | `Unit 08`, `Unit 09` |
| `Unit 11` | [`units/11_single_token_bound.md`](units/11_single_token_bound.md) | One token gives at most one datum | `Bridge` | `Unit 06`, `Unit 07` |
| `Unit 12` | [`units/12_fresh_datum_no_power.md`](units/12_fresh_datum_no_power.md) | A fresh datum preserves old comparisons | `Inertia`, `Mention` | `Unit 08`, `Unit 10` |
| `Unit 13` | [`units/13_second_token_required.md`](units/13_second_token_required.md) | Two data need a second, different token | `Bridge` | `Unit 11` |
| `Unit 14` | [`units/14_factors_through_point.md`](units/14_factors_through_point.md) | Factoring through a point is equality | `PrimDiff` | `Unit 00` |
| `Unit 15` | [`units/15_meta_diff_without_assertion.md`](units/15_meta_diff_without_assertion.md) | An outside difference is not an asserted one | `PrimDiff` | `Unit 14` |
| `Unit 16` | [`units/16_demand_not_met.md`](units/16_demand_not_met.md) | Admitted tokens without instances remain collapsed | `Inertia` | `Unit 05`, `Unit 10` |
| `Unit 17` | [`units/17_impose_guard.md`](units/17_impose_guard.md) | Demands are irreflexive by guard | `Basic` | `Unit 05`, `Unit 16` |
| `Unit 18` | [`units/18_cost1_insufficient.md`](units/18_cost1_insufficient.md) | One item never answers the demand | `Minimality` | `Unit 10`, `Unit 17` |
| `Unit 19` | [`units/19_link_separates.md`](units/19_link_separates.md) | The link regime BL separates | `Minimality` | `Unit 09`, `Unit 18` |
| `Unit 20` | [`units/20_loop_separates.md`](units/20_loop_separates.md) | The self-loop regime BD separates | `Minimality` | `Unit 19` |
| `Unit 21` | [`units/21_mu1_not_unique.md`](units/21_mu1_not_unique.md) | The cheapest answer is not unique under mu1 | `Minimality` | `Unit 18`, `Unit 19`, `Unit 20` |
| `Unit 22` | [`units/22_mu2_unique.md`](units/22_mu2_unique.md) | The cheapest answer is unique under mu2 | `Minimality` | `Unit 18`, `Unit 21` |
| `Unit 23` | [`units/23_selfdiff_consistent.md`](units/23_selfdiff_consistent.md) | A related pair alone does not give non-identity | `PrimDiff` | `Unit 15`, `Unit 20` |
| `Unit 24` | [`units/24_irrefl_witness_ne.md`](units/24_irrefl_witness_ne.md) | Under irreflexivity, a related pair gives non-identity | `PrimDiff` | `Unit 23` |
| `Unit 25` | [`units/25_obstruction_under_irrefl.md`](units/25_obstruction_under_irrefl.md) | Under irreflexivity, collapsing a related pair is obstructed | `PrimDiff` | `Unit 24` |
| `Unit 26` | [`units/26_irrefl_law_not_entailed.md`](units/26_irrefl_law_not_entailed.md) | Keeping positive entries does not exclude a self-pair | `Bridge` | `Unit 24`, `Unit 25` |
| `Unit 27` | [`units/27_abstraction_barrier.md`](units/27_abstraction_barrier.md) | An abstraction cannot see what it identifies | `Quot` | `Unit 08`, `Unit 16` |
| `Unit 28` | [`units/28_closure_must_stop.md`](units/28_closure_must_stop.md) | Fixed data bound rounds that add new demands | `Counting` | `Unit 17` |
| `Unit 29` | [`units/29_renaming_changes_nothing_seen.md`](units/29_renaming_changes_nothing_seen.md) | Renaming the data changes nothing a context can see | `CountTransport` | `Unit 08`, `Unit 09` |
| `Unit 30` | [`units/30_mention_lemma.md`](units/30_mention_lemma.md) | Adding instances that avoid both targets preserves their comparison | `Mention` | `Unit 08`, `Unit 12` |
| `Unit 31` | [`units/31_transition_transport.md`](units/31_transition_transport.md) | Renaming carries transitions; choosing by index can change the outcome | `TransitionTransport` | `Unit 22`, `Unit 29` |
| `Unit 32` | [`units/32_same_proof_one_more_datum.md`](units/32_same_proof_one_more_datum.md) | The same proof with one more datum | `MinimalityF` | `Unit 05`, `Unit 22`, `Unit 29` |
| `Unit 33` | [`units/33_rule_never_pays.md`](units/33_rule_never_pays.md) | Uniform-rule items cannot minimize the declared costs | `RuleBridge` | `Unit 02`, `Unit 22` |
| `Unit 34` | [`units/34_closed_run_bound.md`](units/34_closed_run_bound.md) | Closed runs bound recorded new demands | `Rounds` | `Unit 28`, `Unit 31` |
| `Unit 35` | [`units/35_a_demand_can_always_be_met.md`](units/35_a_demand_can_always_be_met.md) | A fresh mark answers a distinct pair under stated conditions | `Progress` | `Unit 19`, `Unit 34` |
| `Unit 36` | [`units/36_lists_that_mean_sets.md`](units/36_lists_that_mean_sets.md) | Lists can agree on membership while differing as records | `Ext` | `Unit 08`, `Unit 35` |
| `Unit 37` | [`units/37_an_inventory_is_not_a_derivation.md`](units/37_an_inventory_is_not_a_derivation.md) | An inventory is not a derivation | `ObserverInventory`, `Bridge` | `Unit 24`, `Unit 26` |
| `Unit 38` | [`units/38_refusal_as_a_source_of_difference.md`](units/38_refusal_as_a_source_of_difference.md) | Five declared ways to record a repeated token | `Refusal`, `Bridge` | `Unit 11`, `Unit 17` |
| `Unit 39` | [`units/39_refusal_routes_and_their_prices.md`](units/39_refusal_routes_and_their_prices.md) | Comparing refusal protocols under declared prices | `RefusalFrontier` | `Unit 38` |
| `Unit 40` | [`units/40_a_demand_that_never_stops.md`](units/40_a_demand_that_never_stops.md) | A growing chain keeps equal three-bit profiles | `Generator` | `Unit 39` |
| `Unit 41` | [`units/41_looking_farther_does_not_help.md`](units/41_looking_farther_does_not_help.md) | Every fixed radius misses some deep pairs in a long enough chain | `SeparationCapacity` | `Unit 40` |
| `Unit 42` | [`units/42_how_many_things_can_a_window_tell_apart.md`](units/42_how_many_things_can_a_window_tell_apart.md) | Bounded colour windows limit the number of distinct views | `Pigeonhole`, `CapacityBound` | `Unit 41` |
| `Unit 43` | [`units/43_no_bounded_local_repair_clears_a_growing_demand.md`](units/43_no_bounded_local_repair_clears_a_growing_demand.md) | Fixed colour bounds and local windows cannot clear every chain stage | `LocalStrategy`, `G1Class` | `Unit 42` |
| `Unit 44` | [`units/44_reflect_obstruct_close_or_propose.md`](units/44_reflect_obstruct_close_or_propose.md) | Retained, protected, and unseen: when a pair is active | `DiffInterface` | `Unit 25`, `Unit 39` |
| `Unit 45` | [`units/45_a_kernel_with_no_outside.md`](units/45_a_kernel_with_no_outside.md) | Replaying represented events under a fixed kernel | `Represented` | `Unit 44` |
| `Unit 46` | [`units/46_rule_1_in_a_fixed_kernel.md`](units/46_rule_1_in_a_fixed_kernel.md) | Repair or menu exhaustion, with two column-extension candidates | `Completion` | `Unit 45` |
| `Unit 47` | [`units/47_putting_the_viewer_on_the_books.md`](units/47_putting_the_viewer_on_the_books.md) | Recording the evaluator panel: agreement depends on the tests | `NoOutside` | `Unit 45`, `Unit 46` |
| `Unit 48` | [`units/48_generating_the_stream_from_the_state.md`](units/48_generating_the_stream_from_the_state.md) | Generating candidates from a stored policy | `Constitution` | `Unit 45`, `Unit 46` |
| `Unit 49` | [`units/49_minimal_among_what.md`](units/49_minimal_among_what.md) | One descriptor passes six probes in a class of 64 | `Initiality` | `Unit 48` |
| `Unit 50` | [`units/50_from_stage_3_to_every_stage.md`](units/50_from_stage_3_to_every_stage.md) | Proving the shape of every completed tower stage | `Horizon` | `Unit 45`, `Unit 48` |
| `Unit 51` | [`units/51_nine_readings_of_one_difference.md`](units/51_nine_readings_of_one_difference.md) | Separate the witness, the laws, and the allowed operations | `PrimitiveCore` | `Unit 14`, `Unit 23`, `Unit 25` |
| `Unit 52` | [`units/52_the_two_point_witness_is_initial.md`](units/52_the_two_point_witness_is_initial.md) | A unique map out of the two-point arrow | `PrimitiveCats` | `Unit 24`, `Unit 51` |
| `Unit 53` | [`units/53_the_fixed_interface_a_collision_meets.md`](units/53_the_fixed_interface_a_collision_meets.md) | A fixed interface and the scope of its comparison | `PrimitiveContact`, `ContactBridge` | `Unit 51`, `Unit 52` |
| `Unit 54` | [`units/54_from_an_asserted_difference_to_a_response.md`](units/54_from_an_asserted_difference_to_a_response.md) | From an asserted difference to a response | `PrimitivePassage` | `Unit 51`, `Unit 53` |
| `Unit 55` | [`units/55_the_first_graph_is_supplied_its_observer_is_created.md`](units/55_the_first_graph_is_supplied_its_observer_is_created.md) | The first graph is supplied, its observer is created | `HigherStructure` | `Unit 54` |
| `Unit 56` | [`units/56_sameness_earned_from_difference.md`](units/56_sameness_earned_from_difference.md) | When not-apart forms an equivalence | `Apartness` | `Unit 24`, `Unit 51` |
| `Unit 57` | [`units/57_the_interpreter_is_not_in_its_own_family.md`](units/57_the_interpreter_is_not_in_its_own_family.md) | The interpreter is not in its own family: what a notes-diagonal does and does not show | `InterpreterBoundary` | `Unit 48`, `Unit 54` |
| `Unit 58` | [`units/58_is_the_controller_unique.md`](units/58_is_the_controller_unique.md) | Is the controller unique? Simulations, the absorbing halt, and uniqueness only along replay | `ControllerCategory` | `Unit 54`, `Unit 57` |
| `Unit 59` | [`units/59_growing_the_carrier_by_one_and_renaming_the_supply.md`](units/59_growing_the_carrier_by_one_and_renaming_the_supply.md) | Growing the carrier by one and renaming the supply | `Attachment`, `RenamingStructure` | `Unit 54`, `Unit 55` |
| `Unit 60` | [`units/60_one_guard_for_every_dimension_and_boundary_cancellation.md`](units/60_one_guard_for_every_dimension_and_boundary_cancellation.md) | One guard for every dimension and boundary cancellation | `LadderGeneral`, `BoundaryCancellation` | `Unit 55`, `Unit 59` |
| `Unit 61` | [`units/61_compressing_a_presentation_against_a_question_list.md`](units/61_compressing_a_presentation_against_a_question_list.md) | Compressing a presentation against a question list | `Compression` | `Unit 45`, `Unit 51` |
| `Unit 62` | [`units/62_what_protection_buys.md`](units/62_what_protection_buys.md) | What protection buys | `StableContent` | `Unit 54`, `Unit 61` |
| `Unit 63` | [`units/63_where_new_occurrences_come_from.md`](units/63_where_new_occurrences_come_from.md) | Where new occurrences come from | `GraphGenesis` | `Unit 59`, `Unit 62` |
| `Unit 64` | [`units/64_a_profile_without_division.md`](units/64_a_profile_without_division.md) | A profile without division | `WeightProfile` | `Unit 61` |
| `Unit 65` | [`units/65_thirteen_codes_and_why_they_are_not_an_alphabet.md`](units/65_thirteen_codes_and_why_they_are_not_an_alphabet.md) | Thirteen codes and why they are not an alphabet | `TransitionAlphabet` | `Unit 57`, `Unit 63` |
| `Unit 66` | [`units/66_every_step_is_idempotent_and_that_is_almost_all_the_algebra_there_is.md`](units/66_every_step_is_idempotent_and_that_is_almost_all_the_algebra_there_is.md) | Every step is idempotent and that is almost all the algebra there is | `TraceAlgebra` | `Unit 65` |
| `Unit 67` | [`units/67_descending_a_view_through_the_observer_quotient.md`](units/67_descending_a_view_through_the_observer_quotient.md) | Descending a view through the observer quotient | `ObsDescent` | `Unit 56`, `Unit 61` |
| `Unit 68` | [`units/68_what_an_observer_buys_from_an_apartness_and_what_it_costs_back.md`](units/68_what_an_observer_buys_from_an_apartness_and_what_it_costs_back.md) | What an observer buys from an apartness and what it costs back | `ContactBridge`, `DiffAnchor`, `DiffAnchorCompat` | `Unit 53`, `Unit 56`, `Unit 67` |
| `Unit 69` | [`units/69_the_common_kernel_of_a_witnessed_difference.md`](units/69_the_common_kernel_of_a_witnessed_difference.md) | The common kernel of a witnessed difference | `ContactKernel` | `Unit 68` |
| `Unit 70` | [`units/70_can_a_pair_be_chosen_in_a_way_every_relabelling_respects.md`](units/70_can_a_pair_be_chosen_in_a_way_every_relabelling_respects.md) | Can a pair be chosen in a way every relabelling respects? | `PresentationNaturality` | `Unit 59`, `Unit 69` |
| `Unit 71` | [`units/71_when_are_two_presentations_the_same_and_what_a_failed_comparison_forces.md`](units/71_when_are_two_presentations_the_same_and_what_a_failed_comparison_forces.md) | When are two presentations the same, and what a failed comparison forces | `PresentationRelativity`, `ClosureSymmetry`, `ResidualClosure` | `Unit 61`, `Unit 70` |
| `Unit 72` | [`units/72_round_trip_coherence_quotient_retention_and_the_fidelity_closure.md`](units/72_round_trip_coherence_quotient_retention_and_the_fidelity_closure.md) | Round-trip coherence, quotient retention, and the fidelity closure | `PresentationDescent`, `QuotientRetention`, `FidelityClosure`, `NoOutsideFidelity`, `EndogenousFidelityGenerator` | `Unit 67`, `Unit 71` |
| `Unit 73` | [`units/73_a_side_can_be_imposed_but_not_chosen_symmetrically_and_composition_without_an_operator.md`](units/73_a_side_can_be_imposed_but_not_chosen_symmetrically_and_composition_without_an_operator.md) | A side can be imposed but not chosen symmetrically, and composition without an operator | `Breaking`, `Composing` | `Unit 59`, `Unit 70` |
| `Unit 74` | [`units/74_renaming_forms_transporting_collapse_and_canonical_keys.md`](units/74_renaming_forms_transporting_collapse_and_canonical_keys.md) | Renaming forms, transporting collapse, and canonical keys | `FormRenaming`, `FormTransport`, `FormTransportCompat`, `IsoCollapse`, `IsoCollapseCompat`, `IsoCanon`, `IsoCanonCompat`, `IsoBridge`, `IsoBridgeCompat` | `Unit 07`, `Unit 29`, `Unit 59` |

### 3.2 Part 2: Post-Freeze Research Curriculum (`Part 2 Unit 00`–`Part 2 Unit 17`)

| Unit | File | Title | Originating Research Trees | Prerequisite Units |
|---|---|---|---|---|
| `Part 2 Unit 00` | [`institutions/units/00_presentations_and_families.md`](institutions/units/00_presentations_and_families.md) | Presentations and families | `research/actor_institution`, `research/two_theorems` | `Unit 61` |
| `Part 2 Unit 01` | [`institutions/units/01_representative_exact.md`](institutions/units/01_representative_exact.md) | A representative of the joint partition | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 00` |
| `Part 2 Unit 02` | [`institutions/units/02_knowing_is_factoring.md`](institutions/units/02_knowing_is_factoring.md) | Knowing a claim is factoring | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 01` |
| `Part 2 Unit 03` | [`institutions/units/03_information_counts_classes.md`](institutions/units/03_information_counts_classes.md) | Information counts classes | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 01`, `Part 2 Unit 02` |
| `Part 2 Unit 04` | [`institutions/units/04_family_knows_more.md`](institutions/units/04_family_knows_more.md) | When a family knows more than every member | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 02`, `Part 2 Unit 03` |
| `Part 2 Unit 05` | [`institutions/units/05_correspondence_is_an_admission.md`](institutions/units/05_correspondence_is_an_admission.md) | The shared carrier is an admission | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 04` |
| `Part 2 Unit 06` | [`institutions/units/06_degradation_and_loss.md`](institutions/units/06_degradation_and_loss.md) | Degradation, essential members, and invisible guesses | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 04` |
| `Part 2 Unit 07` | [`institutions/units/07_long_chains_go_stationary.md`](institutions/units/07_long_chains_go_stationary.md) | A long finite extension chain has a stationary step | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 03`, `Part 2 Unit 06` |
| `Part 2 Unit 08` | [`institutions/units/08_determination_is_not_truth.md`](institutions/units/08_determination_is_not_truth.md) | Determination is not truth | `research/actor_institution` | `Part 2 Unit 02`, `Part 2 Unit 07` |
| `Part 2 Unit 09` | [`institutions/units/09_assert_or_demur.md`](institutions/units/09_assert_or_demur.md) | Assert or demur: retaining the residual witness | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 06`, `Part 2 Unit 08` |
| `Part 2 Unit 10` | [`institutions/units/10_scoped_authorization.md`](institutions/units/10_scoped_authorization.md) | Scoped authorization is not correctness | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 09` |
| `Part 2 Unit 11` | [`institutions/units/11_same_and_apart_outcomes.md`](institutions/units/11_same_and_apart_outcomes.md) | Asymmetry of same and apart outcomes under refinement | `research/actor_institution` | `Part 2 Unit 09`, `Part 2 Unit 10` |
| `Part 2 Unit 12` | [`institutions/units/12_probing_an_actor.md`](institutions/units/12_probing_an_actor.md) | Probing an actor and tabulating finite questions | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 01` |
| `Part 2 Unit 13` | [`institutions/units/13_the_probe_lower_bound.md`](institutions/units/13_the_probe_lower_bound.md) | The worst-case probe lower bound and its scope | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 12` |
| `Part 2 Unit 14` | [`institutions/units/14_the_complete_table_acquires.md`](institutions/units/14_the_complete_table_acquires.md) | Complete-table acquisition versus sharp observer capacity | `research/actor_institution`, `research/two_theorems` | `Part 2 Unit 13` |
| `Part 2 Unit 15` | [`institutions/units/15_fixing_a_partition_and_the_promised_count_refutation.md`](institutions/units/15_fixing_a_partition_and_the_promised_count_refutation.md) | Fixing a partition and refuting the promised-count shortcut | `research/actor_institution` | `Part 2 Unit 14` |
| `Part 2 Unit 16` | [`institutions/units/16_uncollapse_and_recollapse.md`](institutions/units/16_uncollapse_and_recollapse.md) | Uncollapse by mention and recollapse by admission | `research/uncollapse` | `Unit 30`, `Part 2 Unit 01` |
| `Part 2 Unit 17` | [`institutions/units/17_the_interpreter_boundary_at_verdict_level.md`](institutions/units/17_the_interpreter_boundary_at_verdict_level.md) | The interpreter boundary at verdict level | `research/interpreter_verdict`, `research/two_theorems` | `Unit 57`, `Part 2 Unit 05` |

### 3.3 Forward-Reference Audit

- **Recorded prerequisite graph:** The explicit tables have 75 Part 1 nodes
  and 18 Part 2 nodes. Their cycles and ordering are mechanical properties
  of those recorded edges, not a proof that the prerequisite list is complete.
- **Observational equivalence before quotients:** Observational collapse and
  witnessed separability are introduced in `Unit 08`–`Unit 09` (`Basic.lean`),
  the abstraction barrier in `Unit 27` (`Quot.lean`), represented evaluators in
  `Unit 45` (`Represented.lean`), and setoid/quotient constructions
  (`ObsQuotient`, `Quot.sound`) already appear in Unit 44
  (`DiffInterface.lean`), with later treatments in Unit 56 (`Apartness.lean`)
  and Unit 67 (`ObsDescent.lean`). This is a placement description, not a
  completed comprehension audit.
- **Functions and homomorphisms before initiality:** Structure-preserving maps
  and homomorphisms are introduced in `Unit 52` (`PrimitiveCats.lean`) and
  `Unit 58` (`ControllerCategory.lean`) before proving initiality or refuting
  global controller initiality.
- **Presentations and partitions before institutions:** Actor presentations,
  fibers, and question lists are introduced in `Unit 61` (`Compression.lean`)
  and `Part 2 Unit 00`–`01` before institutional determination (`Part 2 Unit 02`)
  and exceeding (`Part 2 Unit 04`).
- **Explicitly labeled historical notes:** `Unit 60` pairs `LadderGeneral.lean`
  with `BoundaryCancellation.lean` so that the vacuity defect in the first two
  conjuncts of `LadderGeneral.d2_zero_dims_2_3_4` is immediately contrasted
  with the general pairing proof `BoundaryCancellation.d2_zero_unrestricted`
  and `signless_countermodel`. `Unit 57` states `InterpreterBoundary.lean`'s
  open denotational bridge as `OPEN` and points forward (without
  retroactively altering the frozen module) to `Part 2 Unit 17`
  (`research/interpreter_verdict/`).

---

## 4. Research-Extension Theorem Coverage Matrix (Part 2)

Every theorem below belongs to a post-freeze research tree under `research/`
and is taught in Part 2 (`textbook/institutions/`). None is part of the
sealed derivation.

| Originating Tree & PR | Lean Module | Declaration | Status Mark | Axioms | Part 2 Unit & Check |
|---|---|---|---|---|---|
| `research/actor_institution (#284)` | `ResearchActorInstitution.Institution` | `SigEq, sigEq_refl, sigEq_symm, sigEq_trans, FiberConstant, FiberIdentityOn` | ADMITTED / POST_FREEZE_PROVED | `none` | Part 2 Unit 00 (`i00_partitions.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Institution` | `pQ, Information, pQ_exact, pQ_bounds, information_bounds, single_member_classes` | ADMITTED / POST_FREEZE_PROVED | `propext` | Part 2 Unit 01 (`i01_pQ_information.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Institution` | `Knows, knows_iff_determined, knows_iff_information_eq, knows_refl_member` | ADMITTED / POST_FREEZE_PROVED | `propext` | Part 2 Unit 02 (`i02_knows_determined.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Institution` | `information_mono_append, knows_mono, add_redundant_iff, add_strict_iff` | POST_FREEZE_PROVED | `propext` | Part 2 Unit 03 (`i03_monotonicity.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Institution` | `Exceeds, institution_exceeds_members, exceeds_iff_split_witness, min_exceeds_witness` | POST_FREEZE_PROVED / VERIFIED_FINITE | `propext` | Part 2 Unit 04 (`i04_exceeds.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Institution` | `swap01, correspondence_matters, knows_rename` | REFUTED / POST_FREEZE_PROVED | `propext` | Part 2 Unit 05 (`i05_correspondence.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Institution` | `aggregates_inert, essential_iff, aggregate_hides_exceeding, consensus_after_loss` | POST_FREEZE_PROVED / REFUTED | `propext` | Part 2 Unit 06 (`i06_degradation.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Chain` | `long_chain_stationary, stationary_step_known, stationary_step_inert` | POST_FREEZE_PROVED | `propext` | Part 2 Unit 07 (`i07_chain_stationary.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Chain` | `information_without_determination, determination_not_truth, truth_is_a_further_question, truth_from_admitted_target, agreement_known_of_admitted` | REFUTED / CONDITIONAL / POST_FREEZE_PROVED | `propext` | Part 2 Unit 08 (`i08_determination_not_truth.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Policy` | `Verdict, demur_carries_witness, residual_answerable, evidence_is_not_a_digest, demurred_known, demurred_total_iff` | ADMITTED / POST_FREEZE_PROVED / REFUTED | `propext` | Part 2 Unit 09 (`i09_assert_or_demur.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Policy` | `ScopedSound, scoped_sound_refuses_residual, knowsB_scoped_sound, scoped_sound_le_knowsB, authorization_not_correctness` | ADMITTED / CONDITIONAL / REFUTED | `propext` | Part 2 Unit 10 (`i10_authorization.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Policy` | `same_never_supported, apart_never_refuted, same_never_established, established_iff_eq, scoped_identity_not_absolute` | POST_FREEZE_PROVED / REFUTED | `propext` | Part 2 Unit 11 (`i11_outcomes.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Acquisition` | `Query, run, run_congr, Acquires, Fixes` | ADMITTED / POST_FREEZE_PROVED | `propext` | Part 2 Unit 12 (`i12_probing.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Acquisition` | `uncovered_pair, lower_bound, no_acquisition_below_bound, transcripts_identical_capabilities_differ` | CONDITIONAL / POST_FREEZE_PROVED / REFUTED | `propext` | Part 2 Unit 13 (`i13_lower_bound.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Acquisition` | `table_sharp, complete_table_acquires, acquisition_cost_exact, acquired_kernel, log_views` | POST_FREEZE_PROVED | `propext` | Part 2 Unit 14 (`i14_acquisition_exact.py`) |
| `research/actor_institution (#284)` | `ResearchActorInstitution.Acquisition` | `acquires_implies_fixes, exact_promise_zero_probes_two, complete_evaluator_for_two` | POST_FREEZE_PROVED / REFUTED | `propext` | Part 2 Unit 15 (`i15_promise_refuted.py`) |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.Observer` | `Sharp, sharp_observable_iff, sharpObserver` | ADMITTED / POST_FREEZE_PROVED | `propext, Quot.sound` | Part 2 Unit 14 (`i14_acquisition_exact.py`) |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.Sufficiency` | `Sufficient, Consistent, sharp_iff_sufficient_and_consistent, sufficient_not_sharp, consistent_not_sufficient, sharpObserver_views, sharp_fixes_partition` | POST_FREEZE_PROVED / REFUTED | `propext, Quot.sound` | Part 2 Unit 14 (`i14_acquisition_exact.py`) |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.FiniteQuestions` | `encoding_faithful, knows_tabulated` | POST_FREEZE_PROVED | `propext` | Part 2 Unit 12 (`i12_probing.py`) |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.Institution` | `Knows, knows_iff_determined, knows_iff_information_eq, institution_exceeds_members, wise_of_represented` | POST_FREEZE_PROVED / REFUTED (Wise non-discriminating; wisdom kept OPEN) | `propext` | Part 2 Units 01–04, 09 (`i09_assert_or_demur.py`) |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.Reading` | `Guess, own_guess_invisible, guess_visible_iff, shared_guess, nest_inert, participation_collapse, Grounded, grounded_iff_no_overclaim, grounded_or_demur, reports_do_not_certify, grounded_here_not_there, observer_cannot_read_resolution` | POST_FREEZE_PROVED / CONDITIONAL / REFUTED | `propext` | Part 2 Units 06, 07, 09, 10, 13 |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.Correspondence` | `Faithful, collapsed_of_merged, constant_collapses_all, faithful_actor_iff, pullback, verdict_pullback, sharp_pullback_iff, fiberConstant_of_sharp_pullback, faithful_of_sharp_identity, sharp_identity_pullback` | POST_FREEZE_PROVED / CONDITIONAL | `propext, Quot.sound` | Part 2 Unit 05 (`i05_correspondence.py`) |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.Diagonal` | `opDiag, opDiag_not_lawful, lawful_escape_iff, lawful_no_escape` | POST_FREEZE_PROVED / REFUTED | `propext` | Part 2 Unit 17 (`i17_interpreter_verdict.py`) |
| `research/two_theorems (#277)` | `ResearchTwoTheorems.RegimeBridge` | `regimeEvaluator, regime_verdict_iff_separable` | POST_FREEZE_PROVED | `propext, Quot.sound` | Part 2 Unit 14 (`i14_acquisition_exact.py`) |
| `research/uncollapse (#275)` | `ResearchUncollapse` | `uncollapse_only_by_mention, uncollapse_only_by_mention_delta, uncollapse_family_sep_iff, recollapse_by_rule, recollapse_by_instance, recollapse_breaks_requirement, separable_isApart, collapsed_iff_indist, family_index_dependence, family_index_repaired` | POST_FREEZE_PROVED / CONDITIONAL / REFUTED | `propext, Quot.sound` | Part 2 Unit 16 (`i16_uncollapse.py`) |
| `research/interpreter_verdict (#278)` | `ResearchInterpreterVerdict` | `lawful_unique_at, quiescent_reads_guard, interp_not_step, vsep_uncoded, aligned_coded_equals_uncoded, aligned_no_verdict, vsep_uncoded_iff, codes_separated_needs_guard, interp_not_step_wf, vsep_uncoded_wf, openDenotationalBridge` | POST_FREEZE_PROVED / CONDITIONAL / OPEN (`openDenotationalBridge` kept OPEN) | `propext` | Part 2 Unit 17 (`i17_interpreter_verdict.py`) |

---

## 5. Complete Per-Module Declaration Coverage Matrix (All 75 Frozen Modules)

For the 75 modules in `lean4/Derivation/`, the historical tables below
propose declaration placement and record selected source locations, status
marks and axiom information. Grouped names and ellipses remain; these tables
are not an independently verified exhaustive declaration or teaching census:

- **Substantive lesson (`S`)**: Proposed main-lesson placement in the listed
  unit(s); the label alone does not establish that the claim is fully taught.
- **Auxiliary dependency (`A`)**: Proposed supporting material; consult the
  module audit record (`textbook/audit/modules/<Module>.md`) for its recorded scope.
- **Omission note**: A proposed reason for omitting the named items from
  standalone exposition. Such notes do not certify that every unlisted
  declaration has received an individual teaching decision.

### 5.1 `Apartness` (`lean4/Derivation/Apartness.lean`) — Root-imported — `Unit 56`

- **Audit appendix:** [`textbook/audit/modules/Apartness.md`](audit/modules/Apartness.md)
- **Auxiliary / omission justification:** Recommend omitting: `s2_indist_equivalence`, `orientations_same_indist`, `id_preserves_*`, `oriented_pres_iff`, `oriented_family_trivial` (immediate corollaries).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `IsApart r` | 55 | structure (Prop) | ADMITTED (three declared laws) | n/a (definition) | `Unit 56` (Definition / Structure) |
| `Indist r x y` | 63 | def | ADMITTED | n/a (definition) | `Unit 56` (Definition / Structure) |
| `triSymRel` | 126 | def | ADMITTED (countermodel datum) | n/a (definition) | `Unit 56` (Definition / Structure) |
| `instance Decidable (triSymRel x y)` | 129 | instance | ADMITTED | n/a (definition) | `Unit 56` (Definition / Structure) |
| `PreservesOriented f` | 226 | def | ADMITTED | n/a (definition) | `Unit 56` (Definition / Structure) |
| `PreservesApart f` | 231 | def | ADMITTED | n/a (definition) | `Unit 56` (Definition / Structure) |
| `indist_refl` | 67 | theorem | CONDITIONAL:`IsApart r` | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `indist_symm` | 71 | theorem | CONDITIONAL:`IsApart r` | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `indist_trans` | 78 | theorem | CONDITIONAL:`IsApart r` | none | `Unit 56` — Substantive (`S`) |
| `indist_equivalence` | 88 | theorem | CONDITIONAL:`IsApart r` | none | `Unit 56` — Substantive (`S`) |
| `bare_breaks_refl` | 101 | theorem | REFUTED (one-point countermodel) | none | `Unit 56` — Substantive (`S`) |
| `irrefl_alone_breaks_symm` | 107 | theorem | REFUTED (two-point countermodel) | none | `Unit 56` — Substantive (`S`) |
| `subsingleton_indist_total` | 118 | theorem | CONDITIONAL:`Subsingleton X`, `Irrefl r` | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `triSymRel_irrefl` | 132 | theorem | VERIFIED_FINITE | propext | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `triSymRel_symm` | 136 | theorem | VERIFIED_FINITE | propext | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `symm_without_cotrans_breaks_trans` | 143 | theorem | REFUTED (three-point countermodel) | propext | `Unit 56` — Substantive (`S`) |
| `two_point_indist_trans` | 158 | theorem | CONDITIONAL:`Irrefl r`, carrier `Bool` | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `s2_isApart` | 170 | theorem | FROZEN | none | `Unit 56` — Substantive (`S`) |
| `s2_indist_equivalence` | 179 | theorem | FROZEN | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `orientations_same_apartness` | 188 | theorem | VERIFIED_FINITE | none | `Unit 56` — Substantive (`S`) |
| `orientations_same_indist` | 194 | theorem | FROZEN (from the above) | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `orientations_differ` | 207 | theorem | REFUTED | none | `Unit 56` — Substantive (`S`) |
| `retained_orientation_not_swap_invariant` | 215 | theorem | VERIFIED_FINITE | none | `Unit 56` — Substantive (`S`) |
| `oriented_pres_iff` | 236 | theorem | FROZEN | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `oriented_preserver_unique` | 242 | theorem | FROZEN (funext) | Quot.sound | `Unit 56` — Substantive (`S`) |
| `id_preserves_oriented` | 251 | theorem | FROZEN | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `apart_preserver_pair` | 255 | theorem | FROZEN (funext) | Quot.sound | `Unit 56` — Substantive (`S`) |
| `id_preserves_apart` | 287 | theorem | FROZEN | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `swap_preserves_apart` | 289 | theorem | FROZEN | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `swap_breaks_oriented` | 294 | theorem | REFUTED | none | `Unit 56` — Substantive (`S`) |
| `collapse_preserves_neither` | 299 | theorem | REFUTED | none | `Unit 56` — Substantive (`S`) |
| `oriented_comp` | 305 | theorem | FROZEN | none | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |
| `clos_oriented_iff` | 316 | theorem | FROZEN | none | `Unit 56` — Substantive (`S`) |
| `oriented_family_trivial` | 332 | theorem | FROZEN | Quot.sound | `Unit 56` — Auxiliary (`A`, [`Apartness.md`](audit/modules/Apartness.md)) |

### 5.2 `Attachment` (`lean4/Derivation/Attachment.lean`) — Root-imported — `Unit 59`

- **Audit appendix:** [`textbook/audit/modules/Attachment.md`](audit/modules/Attachment.md)
- **Auxiliary / omission justification:** Recommend omitting from the textbook: `zigzagL` (defined, never used in a theorem), `swap12`/`flip02`/`renamePair`/`blockAt` (used only inside three finite checks; a lesson can state the checks without them), `unlawful_refused` (a special case of `attachChecked_refuses`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `LawfulPolicy` | 61 | structure | ADMITTED (declared policy; function Nat → Nat, metatheory) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `par` | 67 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `clampedPar` | 73 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `badChoice` | 77 | def | ADMITTED (countermodel datum) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `AttachOutcome` | 92 | inductive | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `natMax` | 99 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `freshTok` | 114 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `upBlock` | 138 | def | ADMITTED (the Up grammar) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `upFamily` | 144 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `LegalOneEdgeExtension` | 148 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `WFStores` | 164 | def | ADMITTED (recurring hypothesis) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `upS1`..`upS4` | 172–181 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `attachChecked` | 306 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `s12` | 334 | def | ADMITTED (countermodel datum) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `Renaming n` | 367 | structure | ADMITTED (Nat → Nat functions, metatheory) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `renPair` | 427 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `act` | 433 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `attachBlock`, `attachHist`, `treeAt`, `treeState` | 675–689 | def | ADMITTED (`treeAt : Nat → PState`, metatheory) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `t1`, `t2`, `t3` | 713–721 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `Reaches E` | 955 | inductive | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `pathPolL`, `starPolL`, `zigzagL` | 990–1002 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `path4E`, `star4E` | 1030–1032 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `tuples4`, `app4`, `edgeInU`, `isoMatch` | 1040–1055 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `swap12`, `flip02`, `renamePair`, `blockAt` | 1069–1078 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `par_le` | 69 | theorem | FROZEN | none | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `clamp_rewrote_input` | 84 | theorem | VERIFIED_FINITE (REFUTED: clamping is not a faithful reading) | none | `Unit 59` — Substantive (`S`) |
| `le_natMax_of_mem` | 101 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `freshTok_fresh` | 119 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `up_iff_legal` | 153 | theorem | FROZEN (near-definitional: `mem_map` + `mem_range`) | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `up_exec_eq` | 187 | theorem | CONDITIONAL: WFStores, live, `p < len` | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `up_executes` | 252 | theorem | CONDITIONAL: same | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `attachChecked_refuses` | 312 | theorem | CONDITIONAL: `¬ p < len` | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `unlawful_refused` | 325 | theorem | CONDITIONAL: length 3 | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `length_not_fresh_countermodel` | 345 | theorem | VERIFIED_FINITE (REFUTED: "length is the fresh token" is false) | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `halted_up_inert` | 354 | theorem | CONDITIONAL: halted | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `Renaming.f_inj` | 375 | theorem | FROZEN | none | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `Renaming.gbound` | 381 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `Renaming.gfix` | 391 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `Renaming.fbound_iff` | 403 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `getD_lt` | 414 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `getD_append_lt` | 419 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `act_occ_length` | 444 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `act_occ_mem` | 451 | theorem | CONDITIONAL: `n = len` | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `freshTok_act` | 472 | theorem | CONDITIONAL: `n = len` | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `upBlock_transport` | 513 | theorem | CONDITIONAL: `n = len` | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `upBlock_parent_inj` | 525 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `upFamily_transport` | 533 | theorem | CONDITIONAL: `n = len` | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `act_up_comm` | 561 | theorem | CONDITIONAL: four hypotheses | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `upFamily_grammar_uniform` | 663 | theorem | CONDITIONAL: equal occ stores | none | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `attach_fresh` | 699 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `attach_pair_not_mem` | 703 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `attach_len` | 726 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `attach_wf_guard` | 730 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `attach_wit_guard` | 747 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `attach_prot_guard` | 768 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `range_map_succ` | 781 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `treeAt_spec` | 791 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `natMax_append_singleton` | 837 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `natMax_range_le` | 848 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `tree_occ_len` | 855 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `freshTok_treeState` | 862 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `attachBlock_is_upBlock` | 879 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `treeState_wf` | 886 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `attach_residue` | 903 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `parent_lt` | 915 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `parent_unique` | 925 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `parent_exists` | 940 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `all_reach_aux` | 959 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `all_reach` | 984 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `path_edges` | 1011 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `star_edges` | 1023 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `tree4_concrete` | 1034 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `path4_star4_not_isomorphic` | 1063 | theorem | VERIFIED_FINITE (REFUTED: shape is not forced by cost) | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `star_orbit_swap` | 1085 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `path_oriented_rigid` | 1102 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `path_center_separate` | 1110 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`Attachment.md`](audit/modules/Attachment.md)) |
| `equal_size_not_renaming_related` | 1130 | theorem | REFUTED (general over σ) | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `equal_cost_non_isomorphic_extensions` | 1160 | theorem | VERIFIED_FINITE (REFUTED: equal cost does not force shape) | propext, Quot.sound | `Unit 59` — Substantive (`S`) |

### 5.3 `Basic` (`lean4/Derivation/Basic.lean`) — Root-imported — `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17`

- **Audit appendix:** [`textbook/audit/modules/Basic.md`](audit/modules/Basic.md)
- **Auxiliary / omission justification:** Omit from the textbook: the `insertNew` lemmas as theorems (explain dedup in one sentence); the `Decidable` instances.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Inst` | 21 | abbrev | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `insertNew` | 25 | def | ADMITTED (declared policy: re-admission is idempotent, matching Python) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `Regime` | 53 | structure | ADMITTED (the declared state shape, paper C1) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `Regime.wf` | 64 | def | ADMITTED (a predicate, NOT enforced by the structure) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `Ctx` | 74 | structure | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `plug` | 80 | def | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `derivable` | 85 | def | ADMITTED (declared derivability) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| instance `Decidable (derivable r i)` | 88 | instance | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `slotOk` | 92 | def | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| instance `Decidable (slotOk n s)` | 96 | instance | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `wfCtx` | 106 | def | ADMITTED (the "at least one hole" clause is a declared choice matching the Python enumeration) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| instance `Decidable (wfCtx r c)` | 112 | instance | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `collapsed` | 117 | def | ADMITTED (declared sense of collapse) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `separable` | 123 | def | ADMITTED (declared sense, paper 3.5) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `Event` | 134 | inductive | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `stepE` | 145 | def | ADMITTED (the declared admission semantics) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `replayE` | 166 | def | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `Item` | 171 | inductive | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `applyItem` | 178 | def | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `applyDelta` | 192 | def | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `validResponse` | 198 | def | ADMITTED (declared acceptance criterion) | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `R2L` | 208 | def | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `R2F` | 209 | def | ADMITTED | n/a (definition) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` (Definition / Structure) |
| `insertNew_nil` | 28 | theorem | FROZEN | not in artifact | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` — Auxiliary (`A`, [`Basic.md`](audit/modules/Basic.md)) |
| `insertNew_of_not_mem` | 31 | theorem | FROZEN | not in artifact (probe: propext) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` — Auxiliary (`A`, [`Basic.md`](audit/modules/Basic.md)) |
| `insertNew_of_mem` | 35 | theorem | FROZEN | not in artifact (probe: propext) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` — Auxiliary (`A`, [`Basic.md`](audit/modules/Basic.md)) |
| `mem_insertNew` | 40 | theorem | FROZEN | not in artifact (probe: propext) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` — Auxiliary (`A`, [`Basic.md`](audit/modules/Basic.md)) |
| `separable_not_collapsed` | 128 | theorem | FROZEN | propext | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` — Substantive (`S`) |
| `R2L_wf` | 211 | theorem | VERIFIED_FINITE (simp on a concrete regime) | not in artifact (probe: propext, Quot.sound) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` — Auxiliary (`A`, [`Basic.md`](audit/modules/Basic.md)) |
| `R2F_wf` | 214 | theorem | VERIFIED_FINITE | not in artifact (probe: propext, Quot.sound) | `Unit 00`, `Unit 08`, `Unit 09`, `Unit 17` — Auxiliary (`A`, [`Basic.md`](audit/modules/Basic.md)) |

### 5.4 `BoundaryCancellation` (`lean4/Derivation/BoundaryCancellation.lean`) — Root-imported — `Unit 60`

- **Audit appendix:** [`textbook/audit/modules/BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)
- **Auxiliary / omission justification:** Recommend omitting: `d2_zero_general`, `d2_zero_facets` as separate items (restatements with unused hypotheses; teach `d2_zero_unrestricted` and remark that the ascending form follows); `signless_countermodel_dim3` (duplicate of the dimension-2 exhibit). Keep the "not formalized" note about the two-per-face count so students do not read `codim2_distinct` as that count.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `sumTo` | 95 | def | ADMITTED (metatheory apparatus, so labelled) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `sumFrom` | 100 | def | ADMITTED (metatheory) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `rowTri` | 151 | def | ADMITTED (metatheory) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `colTri` | 155 | def | ADMITTED (metatheory) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `dterm` | 293 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `bdNoSign` | 592 | def | ADMITTED (countermodel exhibit) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `pushNoSign` | 596 | def | ADMITTED (countermodel exhibit) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `sumTo_const_zero` | 104 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `sumTo_congr` | 111 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `sumTo_add` | 119 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `sumTo_split` | 129 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `sumFrom_shift` | 139 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `tri_transpose` | 159 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `eraseIdx_eraseIdx_succ` | 193 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `eraseIdx_swap` | 207 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `sgn_succ` | 215 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `sgn_cancel` | 222 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `coeffN_nil` | 233 | theorem | FROZEN (rfl) | none | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `foldl_acc` | 235 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `coeffN_append` | 245 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `coeffN_singleton` | 253 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `coeffN_map_range` | 262 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `coeffN_flatMap_range` | 277 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `coeff_push_bd` | 296 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `coeff_rect` | 313 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `ite_pair_cancel` | 323 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `dterm_cancel` | 333 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `rect_zero` | 339 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d2_zero_unrestricted` | 377 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d2_zero_general` | 387 | theorem | FROZEN (hypotheses recorded, not used; named `_hasc`, `_hlen`) | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d2_zero_facets` | 395 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `d2_zero_replayed` | 406 | theorem | CONDITIONAL: `1 ≤ k`, membership in a replayed complex (both trivially discharged — the conclusion holds unconditionally by `d2_zero_unrestricted`) | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d2_zero_d4` | 415 | theorem | CONDITIONAL as above (instance) | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `ascB_tail` | 423 | theorem | FROZEN | propext | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `ascB_head_lt` | 428 | theorem | FROZEN | propext | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `eraseIdx_inj_of_asc` | 442 | theorem | CONDITIONAL: `ascB l = true`, `i, j < l.length` | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `codim2_distinct` | 485 | theorem | CONDITIONAL: `ascB l = true` and the range/order hypotheses | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `eraseIdx_map` | 534 | theorem | FROZEN | propext | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `ascB_map` | 545 | theorem | CONDITIONAL: `∀ x y, x < y → r x < r y` | propext | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `d2_zero_renamed` | 568 | theorem | CONDITIONAL: monotone `r`, `ascB σ`, `2 ≤ σ.length` (only the first three conjuncts use them) | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d2_zero_shift` | 580 | theorem | CONDITIONAL: `ascB σ`, `2 ≤ σ.length` | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `signless_countermodel` | 607 | theorem | VERIFIED_FINITE / REFUTED (refutes "the vanishing is independent of the sign convention") | none | `Unit 60` — Substantive (`S`) |
| `signless_countermodel_dim3` | 622 | theorem | VERIFIED_FINITE / REFUTED | none | `Unit 60` — Auxiliary (`A`, [`BoundaryCancellation.md`](audit/modules/BoundaryCancellation.md)) |
| `illformed_countermodel` | 648 | theorem | VERIFIED_FINITE / REFUTED (refutes "distinct positions give distinct facets" without ascent; confirms vanishing is not refuted) | propext, Quot.sound | `Unit 60` — Substantive (`S`) |

### 5.5 `Breaking` (`lean4/Derivation/Breaking.lean`) — Root-imported — `Unit 73`

- **Audit appendix:** [`textbook/audit/modules/Breaking.md`](audit/modules/Breaking.md)
- **Auxiliary / omission justification:** Recommend omitting: `ne_image` and `two_cycle` as theorems (fields restated; the module says so); or, if kept, teach them as the example of a result that must not be cited as a derivation. Place the whole lesson outside the regime-model sequence, with the explicit note that no Layer 3 connects it.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Break` | 84 | structure | ADMITTED (declared shape; "not forced") | n/a (definition) | `Unit 73` (Definition / Structure) |
| `SingleOrbit B` | 107 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `emptyBreak` | 112 | def | ADMITTED (witness) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `fourBreak` | 122 | def | ADMITTED (witness) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `Selector B` | 146 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `Represents B s` | 149 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `OrbitConstant B s` | 153 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `Equivariant B s` | 157 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `boolBreak` | 179 | def | ADMITTED (witness) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `constFalse` | 196 | def | ADMITTED (witness) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `Symmetry` | 243 | structure | ADMITTED (declared shape; no group laws) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `SymSelector`, `SymOrbitConstant`, `SymEquivariant` | 249–257 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `ofBreak B` | 314 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `Tri`, `rot`, `triSymmetry` | 322–334 | inductive/def/def | ADMITTED (witness) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `ne_image` | 94 | theorem | FROZEN (field restated; docstring says so) | not in artifact | `Unit 73` — Auxiliary (`A`, [`Breaking.md`](audit/modules/Breaking.md)) |
| `two_cycle` | 99 | theorem | FROZEN (field restated) | not in artifact | `Unit 73` — Auxiliary (`A`, [`Breaking.md`](audit/modules/Breaking.md)) |
| `fourBreak_not_singleOrbit` | 138 | theorem | REFUTED (of "a `Break` has one orbit") | not in artifact | `Unit 73` — Substantive (`S`) |
| `no_orbit_constant_equivariant_endomap` | 172 | theorem | CONDITIONAL:an inhabitant `w : B.Whole` | none | `Unit 73` — Substantive (`S`) |
| `boolBreak_singleOrbit` | 188 | theorem | VERIFIED_FINITE | not in artifact | `Unit 73` — Auxiliary (`A`, [`Breaking.md`](audit/modules/Breaking.md)) |
| `constFalse_represents` | 198 | theorem | VERIFIED_FINITE | not in artifact | `Unit 73` — Auxiliary (`A`, [`Breaking.md`](audit/modules/Breaking.md)) |
| `constFalse_orbitConstant` | 204 | theorem | FROZEN (rfl) | not in artifact | `Unit 73` — Auxiliary (`A`, [`Breaking.md`](audit/modules/Breaking.md)) |
| `constFalse_not_equivariant` | 210 | theorem | REFUTED | not in artifact | `Unit 73` — Substantive (`S`) |
| `imposable_but_not_equivariant` | 214 | theorem | VERIFIED_FINITE (bundle) | not in artifact | `Unit 73` — Substantive (`S`) |
| `no_selector_of_no_common_fixed_point` | 269 | theorem | CONDITIONAL:inhabitant, no common fixed point | none | `Unit 73` — Substantive (`S`) |
| `no_common_fixed_point` | 283 | theorem | FROZEN | none | `Unit 73` — Auxiliary (`A`, [`Breaking.md`](audit/modules/Breaking.md)) |
| `no_orbit_constant_equivariant_selector` | 306 | theorem | CONDITIONAL:inhabitant | none | `Unit 73` — Substantive (`S`) |
| `no_fixed_point_free_involution_on_Tri` | 347 | theorem | REFUTED (case analysis on three points) | none | `Unit 73` — Substantive (`S`) |
| `selector_exists_at_common_fixed_point` | 398 | theorem | CONDITIONAL:a common fixed point | none | `Unit 73` — Substantive (`S`) |
| `selector_iff_common_fixed_point` | 415 | theorem | CONDITIONAL:inhabitant `w : W` | none | `Unit 73` — Substantive (`S`) |

### 5.6 `Bridge` (`lean4/Derivation/Bridge.lean`) — Root-imported — `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38`

- **Audit appendix:** [`textbook/audit/modules/Bridge.md`](audit/modules/Bridge.md)
- **Auxiliary / omission justification:** Recommend omitting: `no_swap_fixed_offdiag_pair` as a named result (its content is "the swap on `Bool × Bool` has no fixed point", the off-diagonal qualifier does nothing; teach it as a remark inside `equivariant_not_D2`); `exists_not_of_not_ball` (library-grade helper).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `SingleTok t0 e` | 32 | def | ADMITTED | n/a (definition) | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` (Definition / Structure) |
| `AtMostTok t0 t` | 37 | def | ADMITTED (invariant) | n/a (definition) | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` (Definition / Structure) |
| (instance) | 114 | instance | ADMITTED (auxiliary) | n/a (definition) | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` (Definition / Structure) |
| `hist01` | 289 | def | ADMITTED (concrete history) | n/a (definition) | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` (Definition / Structure) |
| `hist10` | 293 | def | ADMITTED (concrete history) | n/a (definition) | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` (Definition / Structure) |
| `stepT_preserves_atMostTok` | 40 | theorem | CONDITIONAL:`AtMostTok t0 t`, `SingleTok t0 e` (and the dedup `stepT`) | propext, Quot.sound | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Auxiliary (`A`, [`Bridge.md`](audit/modules/Bridge.md)) |
| `single_token_carrier_bound` | 91 | theorem | CONDITIONAL:`∀ e ∈ h, SingleTok t0 e`, `AtMostTok t0 t`; rests on the deduplicating `stepT` | propext, Quot.sound | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `exists_not_of_not_ball` | 128 | theorem | FROZEN (generic list lemma; needs `[DecidablePred P]`) | not in artifact (probe: none) | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Auxiliary (`A`, [`Bridge.md`](audit/modules/Bridge.md)) |
| `second_token_required` | 149 | theorem | CONDITIONAL:`replayT h ⟨[],[],[],[],[]⟩ = some res`, `2 ≤ res.tokens.length`; rests on dedup `stepT` | propext, Quot.sound | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `no_admitForm_no_forms` | 177 | theorem | CONDITIONAL:`∀ e ∈ h, ∀ a, e ≠ admitForm a`, `t.forms = []` | propext, Quot.sound | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `no_forms_no_witness` | 220 | theorem | CONDITIONAL:`t.forms = []` (one step; a property of the declared `stepT` guard) | propext, Quot.sound | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `irrefl_law_not_entailed` | 230 | theorem | FROZEN (requires an element `a : α`) | none | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `equivariant_witness_is_S2` | 244 | theorem | CONDITIONAL:swap-invariance, `Irrefl S`, inhabited off-diagonal | none | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `equivariant_not_D2` | 267 | theorem | CONDITIONAL:same | none | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `no_swap_fixed_offdiag_pair` | 281 | theorem | VERIFIED_FINITE (`decide`); hypothesis `x ≠ y` unused, see §11 | none | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `order_visible_to_metatheory` | 301 | theorem | VERIFIED_FINITE (`decide`) | propext, Quot.sound | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |
| `order_erased_at_object_level` | 311 | theorem | VERIFIED_FINITE (`decide`) | propext, Quot.sound | `Unit 11`, `Unit 13`, `Unit 26`, `Unit 37`, `Unit 38` — Substantive (`S`) |

### 5.7 `CapacityBound` (`lean4/Derivation/CapacityBound.lean`) — Root-imported — `Unit 42`

- **Audit appendix:** [`textbook/audit/modules/CapacityBound.md`](audit/modules/CapacityBound.md)
- **Auxiliary / omission justification:** Recommend omitting: `encode_nil`/`encode_cons` (definitional), `capacity_at_one_colour` (degenerate; one sentence suffices).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `encode` | 59 | def | ADMITTED | n/a (definition) | `Unit 42` (Definition / Structure) |
| `colourBall` | 131 | def | ADMITTED | n/a (definition) | `Unit 42` (Definition / Structure) |
| `ViewLocal` | 151 | def | ADMITTED (declared hypothesis; load-bearing) | n/a (definition) | `Unit 42` (Definition / Structure) |
| `encode_nil` | 63 | theorem | FROZEN (rfl) | not in artifact | `Unit 42` — Auxiliary (`A`, [`CapacityBound.md`](audit/modules/CapacityBound.md)) |
| `encode_cons` | 65 | theorem | FROZEN (rfl) | not in artifact | `Unit 42` — Auxiliary (`A`, [`CapacityBound.md`](audit/modules/CapacityBound.md)) |
| `encode_lt` | 70 | theorem | FROZEN | propext, Quot.sound | `Unit 42` — Auxiliary (`A`, [`CapacityBound.md`](audit/modules/CapacityBound.md)) |
| `encode_inj` | 90 | theorem | FROZEN | propext, Quot.sound | `Unit 42` — Auxiliary (`A`, [`CapacityBound.md`](audit/modules/CapacityBound.md)) |
| `colourBall_length` | 134 | theorem | FROZEN | propext | `Unit 42` — Auxiliary (`A`, [`CapacityBound.md`](audit/modules/CapacityBound.md)) |
| `colourBall_bounded` | 139 | theorem | CONDITIONAL:`∀ x, colour x < k` | propext, Quot.sound | `Unit 42` — Auxiliary (`A`, [`CapacityBound.md`](audit/modules/CapacityBound.md)) |
| `local_view_blind` | 156 | theorem | CONDITIONAL:`ViewLocal` | none | `Unit 42` — Substantive (`S`) |
| `capacity_bound` | 178 | theorem | CONDITIONAL:bounded colouring, `ViewLocal`, the threshold | propext, Quot.sound | `Unit 42` — Substantive (`S`) |
| `capacity_at_one_colour` | 212 | theorem | CONDITIONAL:`2d + 3 ≤ n` (conclusion's equality is trivial; the content is the deep pair) | propext, Quot.sound | `Unit 42` — Auxiliary (`A`, [`CapacityBound.md`](audit/modules/CapacityBound.md)) |
| `local_view_can_separate` | 227 | theorem | VERIFIED_FINITE (witness `x % 2`; `decide`/case split) | propext, Quot.sound | `Unit 42` — Substantive (`S`) |

### 5.8 `ClosureSymmetry` (`lean4/Derivation/ClosureSymmetry.lean`) — Root-imported — `Unit 71`

- **Audit appendix:** [`textbook/audit/modules/ClosureSymmetry.md`](audit/modules/ClosureSymmetry.md)
- **Auxiliary / omission justification:** Recommend omitting: `residual_refutes_factorization` as a separate item (it restates `PresentationRelativity.directionalResidual_refutes_identity`'s content for `FactorsOn`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `transpose a b x` | 31 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `InternalSymmetryBreak D p q` | 73 | structure (Type) | ADMITTED (declared form of "internal symmetry break"; its `symmetry` is any ambient `Nat → Nat` satisfying the laws, not only a transposition) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `residual_to_internal_symmetry_break r` | 87 | def | ADMITTED (construction; content is in the field proofs) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `internal_symmetry_break_to_residual b` | 122 | def | ADMITTED (construction) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `transpose_left` | 35 | theorem | FROZEN | propext | `Unit 71` — Auxiliary (`A`, [`ClosureSymmetry.md`](audit/modules/ClosureSymmetry.md)) |
| `transpose_right` | 39 | theorem | FROZEN | propext | `Unit 71` — Auxiliary (`A`, [`ClosureSymmetry.md`](audit/modules/ClosureSymmetry.md)) |
| `transpose_fixed` | 46 | theorem | FROZEN | propext | `Unit 71` — Auxiliary (`A`, [`ClosureSymmetry.md`](audit/modules/ClosureSymmetry.md)) |
| `transpose_involutive` | 50 | theorem | FROZEN | propext | `Unit 71` — Auxiliary (`A`, [`ClosureSymmetry.md`](audit/modules/ClosureSymmetry.md)) |
| `residual_nonempty_iff_internal_symmetry_break_nonempty` | 134 | theorem | FROZEN | propext | `Unit 71` — Substantive (`S`) |
| `residual_refutes_factorization` | 146 | theorem | FROZEN | Quot.sound | `Unit 71` — Auxiliary (`A`, [`ClosureSymmetry.md`](audit/modules/ClosureSymmetry.md)) |
| `closure_failure_iff_internal_symmetry_break` | 158 | theorem | FROZEN | propext, Quot.sound | `Unit 71` — Substantive (`S`) |

### 5.9 `Completion` (`lean4/Derivation/Completion.lean`) — Root-imported — `Unit 46`

- **Audit appendix:** [`textbook/audit/modules/Completion.md`](audit/modules/Completion.md)
- **Auxiliary / omission justification:** Omit: `early_collapse_transports` (information-free), `ofWorld_quiescent` (a restatement of `ofWorld_obstruction`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| CommonState | 41 | structure | ADMITTED (declared common interface) | n/a (definition) | `Unit 46` (Definition / Structure) |
| sepC | 54 | def | ADMITTED (observation law) | n/a (definition) | `Unit 46` (Definition / Structure) |
| zeroC | 59 | def | ADMITTED | n/a (definition) | `Unit 46` (Definition / Structure) |
| obstC | 67 | def | ADMITTED (declared obstruction notion) | n/a (definition) | `Unit 46` (Definition / Structure) |
| ofWorld | 73 | def | ADMITTED (a stated identification of retention with protection) | n/a (definition) | `Unit 46` (Definition / Structure) |
| ofPState | 135 | def | ADMITTED | n/a (definition) | `Unit 46` (Definition / Structure) |
| swapIdx | 165 | def | ADMITTED | n/a (definition) | `Unit 46` (Definition / Structure) |
| swapC | 167 | def | ADMITTED | n/a (definition) | `Unit 46` (Definition / Structure) |
| d2Common | 175 | def | ADMITTED | n/a (definition) | `Unit 46` (Definition / Structure) |
| s2Common | 181 | def | ADMITTED | n/a (definition) | `Unit 46` (Definition / Structure) |
| tagOnly | 219 | def | ADMITTED | n/a (definition) | `Unit 46` (Definition / Structure) |
| augFamily | 264 | def | ADMITTED (declared extension family) | n/a (definition) | `Unit 46` (Definition / Structure) |
| sigOf | 443 | def | ADMITTED (declared measure) | n/a (definition) | `Unit 46` (Definition / Structure) |
| retractFirstMark | 514 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 46` (Definition / Structure) |
| ofWorld_sep | 84 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| ofWorld_obstruction | 87 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| obstC_conditions_independent | 95 | theorem | VERIFIED_FINITE (four 2-element states) | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| ofWorld_quiescent | 115 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Auxiliary (`A`, [`Completion.md`](audit/modules/Completion.md)) |
| chain_transport | 147 | theorem | FROZEN (relies on RefusalFrontier.reflective_chain_is_initial_segment / _successor_relation) | propext | `Unit 46` — Substantive (`S`) |
| d2_transport_oriented | 184 | theorem | VERIFIED_FINITE | none | `Unit 46` — Substantive (`S`) |
| s2_transport_symmetric | 189 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| s2_state_not_swap_invariant | 200 | theorem | VERIFIED_FINITE / REFUTED (refutes whole-state symmetry) | none | `Unit 46` — Substantive (`S`) |
| witness_not_separation | 213 | theorem | VERIFIED_FINITE / REFUTED (refutes witness ⇒ separation) | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| separation_not_witness | 224 | theorem | VERIFIED_FINITE / REFUTED (refutes separation ⇒ witness) | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| meta_distinctness_inert | 231 | theorem | FROZEN (definitional: neither reads the field) | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| early_collapse_transports | 241 | theorem | VERIFIED_FINITE (conclusion holds for any state with no views) | propext, Quot.sound | `Unit 46` — Auxiliary (`A`, [`Completion.md`](audit/modules/Completion.md)) |
| augFamily_sound | 267 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Auxiliary (`A`, [`Completion.md`](audit/modules/Completion.md)) |
| sepB_symm | 271 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Auxiliary (`A`, [`Completion.md`](audit/modules/Completion.md)) |
| augFamily_retains_ties | 279 | theorem | CONDITIONAL: WF | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| rule1_repair_or_extension | 362 | theorem | CONDITIONAL: WF | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| refusal_recordable | 393 | theorem | CONDITIONAL: obstructedB | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| refusal_object_inert | 416 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| refusal_non_absorbing | 428 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| action_dichotomy | 445 | theorem | FROZEN | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| rule1_needs_fidelity | 496 | theorem | CONDITIONAL: w.reqs = [] (the hypothesis is the point) | propext, Quot.sound | `Unit 46` — Substantive (`S`) |
| retraction_breaks_preservation | 520 | theorem | VERIFIED_FINITE / REFUTED (refutes "same-level ⇒ preserving") | propext, Quot.sound | `Unit 46` — Substantive (`S`) |

### 5.10 `Composing` (`lean4/Derivation/Composing.lean`) — Parked (`ParkedAudit.lean`) — `Unit 73`

- **Audit appendix:** [`textbook/audit/modules/Composing.md`](audit/modules/Composing.md)
- **Auxiliary / omission justification:** Omit: nothing; but the textbook should state, as the module does, that this proves nothing about the regime calculus.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Web` | 79 | structure | ADMITTED (declared shape; header: "It does not claim `Web` is forced") | n/a (definition) | `Unit 73` (Definition / Structure) |
| `Composable W a b c f g` | 86 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `noneCompose` | 92 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `HasIdentity W a` | 105 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `allCompose` | 118 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `allSelect` | 134 | def | ADMITTED (witness) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `LeftReach`, `RightReach` | 151, 156 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `RelAssoc W` | 163 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `RelAssocLeft W` | 171 | def | ADMITTED | n/a (definition) | `Unit 73` (Definition / Structure) |
| `skewCompose` | 181 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 73` (Definition / Structure) |
| `composition_may_fail` | 99 | theorem | REFUTED (refutes "composition is total") | none | `Unit 73` — Substantive (`S`) |
| `noneCompose_no_identity` | 112 | theorem | REFUTED (refutes "identities exist") | none | `Unit 73` — Substantive (`S`) |
| `composite_may_be_nonunique` | 126 | theorem | REFUTED (refutes "composition is single-valued") | none | `Unit 73` — Substantive (`S`) |
| `selection_is_possible` | 142 | theorem | FROZEN (over `allCompose`; a positive witness refuting the withdrawn "no selection function") | none | `Unit 73` — Substantive (`S`) |
| `relAssocLeft_of_relAssoc` | 176 | theorem | FROZEN | none | `Unit 73` — Auxiliary (`A`, [`Composing.md`](audit/modules/Composing.md)) |
| `skew_not_relAssocLeft` | 188 | theorem | REFUTED (witness `f = true, g = false, k = true, w = false`, `u = true`) | none | `Unit 73` — Substantive (`S`) |
| `skew_not_relAssoc` | 198 | theorem | REFUTED | none | `Unit 73` — Substantive (`S`) |

### 5.11 `Compression` (`lean4/Derivation/Compression.lean`) — Root-imported — `Unit 61`

- **Audit appendix:** [`textbook/audit/modules/Compression.md`](audit/modules/Compression.md)
- **Auxiliary / omission justification:** Omit: `refinement_tie` as a separate theorem (same witnesses as `refinement_not_unique`, plus a length equation); the `memB`/`dedupL` apparatus (explain `classCount` as "number of distinct signatures" inline).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| sigList | 66 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| SigEq | 71 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| Adequate | 95 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| FiberConstant | 100 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| FactorsOn | 104 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| pick | 110 | def | ADMITTED (replaces library search) | n/a (definition) | `Unit 61` (Definition / Structure) |
| pQ | 223 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| SplitsAt | 345 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| ind | 447 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| memB | 519 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| dedupL | 549 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| classCount | 584 | def | ADMITTED (the declared measure) | n/a (definition) | `Unit 61` (Definition / Structure) |
| StrictRefine | 732 | def | ADMITTED (declared step relation) | n/a (definition) | `Unit 61` (Definition / Structure) |
| StrictChain | 737 | def | ADMITTED | n/a (definition) | `Unit 61` (Definition / Structure) |
| sigEq_iff_sigList | 75 | theorem | FROZEN | none | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| pick_cons | 115 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| pick_mem | 118 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| pick_holds | 134 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| pick_some_of_mem | 151 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| factors_iff_fiberConstant | 171 | theorem | FROZEN | Quot.sound | `Unit 61` — Substantive (`S`) |
| factor_unique_on_image | 192 | theorem | FROZEN | none | `Unit 61` — Substantive (`S`) |
| factor_not_unique_off_image | 200 | theorem | REFUTED (of off-image uniqueness) | none | `Unit 61` — Substantive (`S`) |
| pQ_spec | 229 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| pQ_exact | 248 | theorem | FROZEN | Quot.sound | `Unit 61` — Substantive (`S`) |
| pQ_adequate | 267 | theorem | FROZEN | Quot.sound | `Unit 61` — Substantive (`S`) |
| pQ_coarsest | 275 | theorem | CONDITIONAL: Adequate D Q p | Quot.sound | `Unit 61` — Substantive (`S`) |
| pQ_unique_on_image | 286 | theorem | FROZEN | none | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| sigEq_decompose | 298 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| exists_separator_of_not_sigEq | 312 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| descent_witness | 328 | theorem | CONDITIONAL: p x = p x', ¬ SigEq Q x x' | none | `Unit 61` — Substantive (`S`) |
| enlarge_refines | 338 | theorem | FROZEN | none | `Unit 61` — Substantive (`S`) |
| splits_iff_new_separator | 353 | theorem | FROZEN | none | `Unit 61` — Substantive (`S`) |
| absolute_adequacy_iff_injective | 375 | theorem | FROZEN | none | `Unit 61` — Substantive (`S`) |
| dup_no_refine | 398 | theorem | FROZEN | propext | `Unit 61` — Substantive (`S`) |
| postcompose_no_refine | 410 | theorem | FROZEN | propext | `Unit 61` — Substantive (`S`) |
| refine_requires_separator | 432 | theorem | CONDITIONAL: SplitsAt D Q Q' x | none | `Unit 61` — Substantive (`S`) |
| refinement_not_unique | 455 | theorem | REFUTED (of unique refinement) | none | `Unit 61` — Substantive (`S`) |
| refinement_tie | 487 | theorem | REFUTED (of a unique minimum-length refinement) | none | `Unit 61` — Substantive (`S`) |
| memB_cons | 523 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| memB_iff | 526 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| dedupL_cons | 553 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| length_dedupL_le | 557 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| dedupL_ne_nil | 567 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| memG_of_memF | 590 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| count_le_of_determines | 602 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| count_lt_of_split | 631 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| refine_bounded | 693 | theorem | FROZEN | propext, Quot.sound | `Unit 61` — Substantive (`S`) |
| classCount_pos | 701 | theorem | CONDITIONAL: D ≠ [] | none | `Unit 61` — Substantive (`S`) |
| strict_split_increases | 715 | theorem | CONDITIONAL: subfamily and a split | propext, Quot.sound | `Unit 61` — Substantive (`S`) |
| chain_count | 745 | theorem | FROZEN | not in artifact | `Unit 61` — Auxiliary (`A`, [`Compression.md`](audit/modules/Compression.md)) |
| chain_bounded | 766 | theorem | CONDITIONAL: D ≠ [] | propext, Quot.sound | `Unit 61` — Substantive (`S`) |
| strict_steps_lt | 780 | theorem | CONDITIONAL: D ≠ [] | propext, Quot.sound | `Unit 61` — Substantive (`S`) |

### 5.12 `Constitution` (`lean4/Derivation/Constitution.lean`) — Root-imported — `Unit 48`

- **Audit appendix:** [`textbook/audit/modules/Constitution.md`](audit/modules/Constitution.md)
- **Auxiliary / omission justification:** Omit: `nextFamily_complete` and `budget_replenishment_represented` as separate items (both `rfl`; fold into the discussion of `towerBlock`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| Policy | 44 | inductive | ADMITTED (declared generation policy) | n/a (definition) | `Unit 48` (Definition / Structure) |
| GWorld | 50 | structure | ADMITTED | n/a (definition) | `Unit 48` (Definition / Structure) |
| freshName | 62 | def | ADMITTED (declared fresh-name function; imports arithmetic/ordering, stated) | n/a (definition) | `Unit 48` (Definition / Structure) |
| towerBlock | 64 | def | ADMITTED (declared block shape) | n/a (definition) | `Unit 48` (Definition / Structure) |
| closeBlocks | 71 | def | ADMITTED | n/a (definition) | `Unit 48` (Definition / Structure) |
| nextFamily | 80 | def | ADMITTED (the fixed interpreter; constitution) | n/a (definition) | `Unit 48` (Definition / Structure) |
| towerGen | 152 | def | ADMITTED (declared metatheoretic driver) | n/a (definition) | `Unit 48` (Definition / Structure) |
| genWorld | 214 | def | ADMITTED | n/a (definition) | `Unit 48` (Definition / Structure) |
| ConstitutionDesc | 303 | structure | ADMITTED (the declared description family) | n/a (definition) | `Unit 48` (Definition / Structure) |
| kernelDesc | 312 | def | ADMITTED | n/a (definition) | `Unit 48` (Definition / Structure) |
| interpStep | 318 | def | ADMITTED (constitution; metatheory) | n/a (definition) | `Unit 48` (Definition / Structure) |
| bools / allDescs | 377 / 379 | def | ADMITTED | n/a (definition) | `Unit 48` (Definition / Structure) |
| nextFamily_tower_singleton | 87 | theorem | FROZEN (definitional) | propext, Quot.sound | `Unit 48` — Auxiliary (`A`, [`Constitution.md`](audit/modules/Constitution.md)) |
| closeBlocks_complete_repair | 92 | theorem | FROZEN | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| closeBlocks_complete_aug | 106 | theorem | FROZEN | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| nextFamily_stop | 120 | theorem | CONDITIONAL: quiescentB (that is the point) | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| towerBlock_eq | 158 | theorem | FROZEN | propext, Quot.sound | `Unit 48` — Auxiliary (`A`, [`Constitution.md`](audit/modules/Constitution.md)) |
| freshName_fresh_on_tower | 165 | theorem | FROZEN (on the tower invariant) | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| freshName_not_fresh_generally | 176 | theorem | VERIFIED_FINITE / REFUTED (refutes general freshness) | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| driver_reproduces_tower | 189 | theorem | FROZEN | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| nextFamily_complete | 204 | theorem | FROZEN (definitional) | propext, Quot.sound | `Unit 48` — Auxiliary (`A`, [`Constitution.md`](audit/modules/Constitution.md)) |
| budget_replenishment_represented | 211 | theorem | FROZEN (definitional) | none | `Unit 48` — Auxiliary (`A`, [`Constitution.md`](audit/modules/Constitution.md)) |
| gen_growth | 217 | theorem | FROZEN | propext, Quot.sound | `Unit 48` — Auxiliary (`A`, [`Constitution.md`](audit/modules/Constitution.md)) |
| gen_three_quiescent | 227 | theorem | VERIFIED_FINITE (k = 3, via worldAt_three_quiescent) | propext, Quot.sound | `Unit 48` — Auxiliary (`A`, [`Constitution.md`](audit/modules/Constitution.md)) |
| tower_driver_autonomy | 255 | theorem | FROZEN (four conjuncts rfl) | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| interp_describe | 348 | theorem | FROZEN | propext, Quot.sound | `Unit 48` — Substantive (`S`) |
| allDescs_length | 384 | theorem | VERIFIED_FINITE | none | `Unit 48` — Auxiliary (`A`, [`Constitution.md`](audit/modules/Constitution.md)) |
| allDescs_complete | 386 | theorem | FROZEN (64-way case split + decide) | propext | `Unit 48` — Substantive (`S`) |

### 5.13 `ContactBridge` (`lean4/Derivation/ContactBridge.lean`) — Root-imported — `Unit 53`, `Unit 68`

- **Audit appendix:** [`textbook/audit/modules/ContactBridge.md`](audit/modules/ContactBridge.md)
- **Auxiliary / omission justification:** Recommend omitting from the textbook: `kernel_stage_no_obstruction` (a policy read-back), `open_bridge_*` String labels (state the OPEN cells in prose instead).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `obsApart` | 116 | def | ADMITTED (definition) | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `obsSetting` | 143 | def | ADMITTED (definition; the empty stores are a declared policy) | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `apartObs` | 224 | def | ADMITTED (definition; the three law fields are discharged by the three admitted `IsApart` fields, one for one) | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `Tri` | 443 | inductive | t1 | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `wlemZero` | 454 | def | ADMITTED (construction inside a proof) | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `open_bridge_cotrans` | 607 | def (String) | OPEN | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `open_bridge_located` | 612 | def (String) | OPEN | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `colView` | 620 | def | ADMITTED (definition over `Nat`; metatheoretic function) | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `kernelStage` | 657 | def | ADMITTED (declared policy: no retention, no guarding) | n/a (definition) | `Unit 53`, `Unit 68` (Definition / Structure) |
| `obsApart_irrefl` | 119 | theorem | FROZEN | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsApart_symm` | 124 | theorem | FROZEN | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsApart_stable` | 130 | theorem | FROZEN | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `zeroRel_indist` | 135 | theorem | FROZEN | none | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `obsSetting_w` | 156 | theorem | CONDITIONAL:`hab : obsApart O a b` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsSetting_a` | 161 | theorem | CONDITIONAL:`hab` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsSetting_bs` | 166 | theorem | CONDITIONAL:`hab` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsApart_cotrans` | 175 | theorem | CONDITIONAL:`Decidable (ZeroRel O x y)` pointwise | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsSetting_bc` | 184 | theorem | CONDITIONAL:`hab`, `Decidable (ZeroRel …)` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsSetting_bl` | 193 | theorem | CONDITIONAL:`hab`, `Decidable (ZeroRel …)` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsSetting_d` | 203 | theorem | CONDITIONAL:`hab` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsSetting_e` | 211 | theorem | CONDITIONAL:`hab`; the empty `Ops` is by construction | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `apartObs_zeroRel` | 236 | theorem | FROZEN (`Iff.rfl`) | none | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `apartObs_roundtrip` | 244 | theorem | CONDITIONAL:`IsApart r`, `Decidable (r x y)` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `isApart_repr` | 256 | theorem | CONDITIONAL:`IsApart r`, `Decidable (r x y)` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsApart_isApart` | 265 | theorem | CONDITIONAL:`Decidable (ZeroRel …)` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `indist_obsApart_iff` | 274 | theorem | CONDITIONAL:`Decidable (ZeroRel …)` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `obsSetting_not_c` | 290 | theorem | FROZEN (definitional) | none | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `obsSetting_not_f` | 297 | theorem | FROZEN (definitional) | none | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `kernel_prot_independent` | 304 | theorem | CONDITIONAL:`hab` | none | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `obsApart_repr_iff` | 319 | theorem | FROZEN; Prop-valued observers only | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `unit_total_not_repr` | 350 | theorem | REFUTED (carrier 1; Prop-valued only) | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `d2_not_obs_complement` | 362 | theorem | REFUTED (carrier 2) | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `triSym_not_obs_complement` | 377 | theorem | REFUTED (carrier 3) | propext | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `bool_bs_repr` | 398 | theorem | CONDITIONAL:`r a b`, `Irrefl r`, symmetry; carrier `Bool` | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `d_not_witnessed_repr` | 426 | theorem | REFUTED (carrier 2; trivially, the two conjuncts contradict) | none | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `cotrans_schema_iff_wlem` | 519 | theorem | FROZEN (schema equivalence; the classical principle is a quantified statement, never a proof step) | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `stability_schema_iff_dne` | 550 | theorem | FROZEN (schema equivalence) | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `located_schema_implies_wlem` | 578 | theorem | FROZEN (one implication; converse OPEN) | none | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `declared_zero_as_view` | 628 | theorem | FROZEN (over `Nat` and `List`; metatheoretic carrier) | propext, Quot.sound | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `observation_stage_realizes_observer` | 648 | theorem | FROZEN (carrier `Nat`) | propext, Quot.sound | `Unit 53`, `Unit 68` — Substantive (`S`) |
| `kernel_stage_no_obstruction` | 666 | theorem | FROZEN but near-definitional (holds by the declared `retained := False`, not by any property of `O`) | none | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `pair_blocked_is_collapse_collision` | 678 | theorem | FROZEN | Quot.sound | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `collapse_collision_is_pair_blocked` | 688 | theorem | FROZEN | propext, Quot.sound | `Unit 53`, `Unit 68` — Auxiliary (`A`, [`ContactBridge.md`](audit/modules/ContactBridge.md)) |
| `pair_blocked_iff_collapse_collision` | 701 | theorem | FROZEN | propext, Quot.sound | `Unit 53`, `Unit 68` — Substantive (`S`) |

### 5.14 `ContactKernel` (`lean4/Derivation/ContactKernel.lean`) — Root-imported — `Unit 69`

- **Audit appendix:** [`textbook/audit/modules/ContactKernel.md`](audit/modules/ContactKernel.md)
- **Auxiliary / omission justification:** Recommend omitting: `kernel_licenses_entry` and `entry_pre_observation` as theorems (teach the passage entry facts from PrimitivePassage directly; see §11), `open_kernel_*` String labels, `contactCells` literal (present the matrix as a table in the lesson), `pair_choice_load_bearing` (superseded by `pair_choice_not_unique`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `WitnessedDiff` | 106 | structure | ADMITTED (the kernel signature; `diag_zero` and `apart_ab` are proof fields) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `kernelApart` | 115 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `boolKernel` | 140 | def | ADMITTED (finite model) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `toSetting` | 153 | def | ADMITTED (declared empty-store policy) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `toNativeKernel` | 171 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `ofSetting` | 179 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `open_kernel_grade` | 204 | def (String) | OPEN | n/a (definition) | `Unit 69` (Definition / Structure) |
| `ofDiffObs` | 220 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `NonZeroPair` | 305 | abbrev | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `SameDataKernel` | 310 | abbrev | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `toPair` | 316 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `ofPair` | 324 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `boolEqObs` | 402 | def | ADMITTED (finite model; laws proved, not spent from an admission) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `swapObs` | 450 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `toDiffObs` | 518 | def | ADMITTED (record identity; the two hypotheses are exactly the two law fields) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `open_kernel_bl` | 627 | def (String) | OPEN | n/a (definition) | `Unit 69` (Definition / Structure) |
| `unitValKernel` | 687 | def | ADMITTED (finite model) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `twoValKernel` | 697 | def | ADMITTED (finite model) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `VHom` | 724 | structure | ADMITTED (a morphism signature; no identity/composition is defined in this module) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `DeltaOnto` | 755 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `apartObj` | 794 | def | ADMITTED | n/a (definition) | `Unit 69` (Definition / Structure) |
| `boolKernelSwap` | 831 | def | ADMITTED (finite model) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `freeKernel` | 848 | def | ADMITTED (finite model) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `passageObj` | 904 | def | ADMITTED (carrier `Nat`: metatheory) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `contactCells` | 960 | def | ADMITTED (literal) | n/a (definition) | `Unit 69` (Definition / Structure) |
| `kernelApart_irrefl` | 120 | theorem | FROZEN | none | `Unit 69` — Substantive (`S`) |
| `kernel_endpoints_ne` | 126 | theorem | FROZEN | none | `Unit 69` — Substantive (`S`) |
| `no_kernel_on_subsingleton` | 133 | theorem | REFUTED (no kernel on a one-point carrier) / CONDITIONAL:`Subsingleton X` | none | `Unit 69` — Substantive (`S`) |
| `toSetting_A` | 164 | theorem | FROZEN | none | `Unit 69` — Substantive (`S`) |
| `ofSetting_exact` | 192 | theorem | CONDITIONAL:`A S`, `Decidable (S.r x y)` pointwise | none | `Unit 69` — Substantive (`S`) |
| `ofSetting_ret_irrelevant` | 210 | theorem | FROZEN (definitional) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `pair_choice_load_bearing` | 240 | theorem | VERIFIED_FINITE (weak existence; docstring disclaims anything stronger) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_from_obs_iff_pair` | 261 | theorem | FROZEN | none | `Unit 69` — Substantive (`S`) |
| `eq_ofDiffObs_of_fields` | 276 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `obs_eq_of_fields` | 295 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `toPair_ofPair` | 328 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `ofPair_toPair` | 337 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `ofPair_injective` | 348 | theorem | FROZEN | none | `Unit 69` — Substantive (`S`) |
| `transpose_kernel_ne` | 368 | theorem | FROZEN (presentation grade; uses `zero_symm`, `zero_refl`) | none | `Unit 69` — Substantive (`S`) |
| `kernel_not_unique_of_pair` | 390 | theorem | CONDITIONAL:`∃ a b, ¬ ZeroRel O a b` | none | `Unit 69` — Substantive (`S`) |
| `boolEqObs_nonzero_ft` | 416 | theorem | VERIFIED_FINITE | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `boolEqObs_nonzero_tf` | 420 | theorem | VERIFIED_FINITE | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `two_kernels_from_one_observer` | 427 | theorem | VERIFIED_FINITE | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `pair_choice_not_unique` | 438 | theorem | VERIFIED_FINITE (hypothesis-free non-uniqueness witness) | none | `Unit 69` — Substantive (`S`) |
| `swapObs_boolEqObs` | 462 | theorem | VERIFIED_FINITE | Quot.sound | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `no_equivariant_pair_at_fixed_point` | 475 | theorem | FROZEN (over all such total maps; metatheoretic function space) | Quot.sound | `Unit 69` — Substantive (`S`) |
| `no_equivariant_pair_valued_map` | 497 | theorem | REFUTED (no relabelling-equivariant total pair selector on `DiffObs Bool Bool`) | Quot.sound | `Unit 69` — Substantive (`S`) |
| `kernel_no_witness_from_collapse` | 507 | theorem | FROZEN (definitional) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `toDiffObs_fields` | 532 | theorem | FROZEN (definitional record identity) | none | `Unit 69` — Substantive (`S`) |
| `toDiffObs_apart` | 543 | theorem | FROZEN (definitional) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_not_observer` | 558 | theorem | REFUTED (carrier 2, Prop-valued) | none | `Unit 69` — Substantive (`S`) |
| `kernel_zero_not_trans` | 578 | theorem | REFUTED (the kernel signature does not entail zero-transitivity; carrier 3) | propext | `Unit 69` — Substantive (`S`) |
| `kernel_not_bs` | 589 | theorem | REFUTED (the kernel signature does not entail symmetry of the induced apartness; carrier 2) | none | `Unit 69` — Substantive (`S`) |
| `kernel_not_bc` | 603 | theorem | REFUTED (carrier 3) | propext | `Unit 69` — Substantive (`S`) |
| `kernel_located_of_decidable` | 618 | theorem | CONDITIONAL:`Decidable (K.Zero v)` | none | `Unit 69` — Substantive (`S`) |
| `kernel_not_c` | 632 | theorem | FROZEN (definitional policy read-back) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_not_f` | 638 | theorem | FROZEN (definitional) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_to_w` | 643 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_to_d` | 648 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_to_e_empty` | 654 | theorem | FROZEN (rests on the empty-`Ops` policy) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_not_e_merged` | 661 | theorem | VERIFIED_FINITE / REFUTED (E is not kernel content once a merger is declared) | none | `Unit 69` — Substantive (`S`) |
| `no_kernel_over_allzero` | 675 | theorem | REFUTED (carrier 2) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `value_presentation_fork` | 709 | theorem | VERIFIED_FINITE | none | `Unit 69` — Substantive (`S`) |
| `vhom_not_unique` | 737 | theorem | VERIFIED_FINITE | none | `Unit 69` — Substantive (`S`) |
| `vhom_unique_of_onto` | 763 | theorem | CONDITIONAL:`DeltaOnto K` (sufficiency only) | Quot.sound | `Unit 69` — Substantive (`S`) |
| `boolKernel_apart_iff` | 787 | theorem | VERIFIED_FINITE | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `apartObj_irrefl` | 798 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `apartObj_sym_of_observer` | 806 | theorem | FROZEN (uses the ADMITTED `zero_symm` field) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_gateway_unique` | 815 | theorem | FROZEN (instantiation of the sealed initiality) | Quot.sound | `Unit 69` — Substantive (`S`) |
| `kernel_gateway_injective` | 824 | theorem | FROZEN | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_gateways_not_identical` | 843 | theorem | VERIFIED_FINITE | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_no_terminal` | 860 | theorem | FROZEN (over all `K'`; apartObj grade) | propext | `Unit 69` — Substantive (`S`) |
| `kernel_no_terminal_collector` | 890 | theorem | REFUTED (no terminal object among `apartObj` presentations, universe 0) | propext | `Unit 69` — Substantive (`S`) |
| `passage_gateway_unique` | 911 | theorem | FROZEN (instantiation; carrier `Nat`) | propext, Quot.sound | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_licenses_entry` | 921 | theorem | FROZEN (conjunction; only the first conjunct mentions `K`) | propext, Quot.sound | `Unit 69` — Substantive (`S`) |
| `entry_pre_observation` | 936 | theorem | VERIFIED_FINITE (one concrete state) | propext, Quot.sound | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `kernel_two_point_presentation` | 949 | theorem | CONDITIONAL:`DecidableEq X` (sufficiency only) | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |
| `contactCells_length` | 1023 | theorem | VERIFIED_FINITE | none | `Unit 69` — Auxiliary (`A`, [`ContactKernel.md`](audit/modules/ContactKernel.md)) |

### 5.15 `ControllerCategory` (`lean4/Derivation/ControllerCategory.lean`) — Root-imported — `Unit 58`

- **Audit appendix:** [`textbook/audit/modules/ControllerCategory.md`](audit/modules/ControllerCategory.md)
- **Auxiliary / omission justification:** Recommend omitting: `two_endo_sims` (subsumed by `sims_never_unique`), `full_resolves_*` as separate items (fold into the countermodel presentation), the individual `setRef_*` lemmas.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `KindDesc` | 84 | structure | ADMITTED (declared comparison class) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `enabled d` | 98 | def | ADMITTED (declared policy: supply is never toggled) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `interpK d s e` | 117 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `replayK d h s` | 120 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `bools` | 123 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `allKinds` | 126 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `fullK` | 153 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `ResponseLiveB`, `ResponseLive` | 165–168 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `OBST5` | 178 | def | ADMITTED (datum) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `noAddK`, `noBudgetK`, `noRefineK` | 202–204 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `OBST0` | 207 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `LOBST` | 212 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `noRefK` | 269 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `isRefuse` | 274 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `Ctrl` | 293 | structure | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `Sim C1 C2` | 298 | structure | ADMITTED (the morphism notion; `f` is a metatheoretic function) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `idSim`, `compSim` | 314–316 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `fullCtrl`, `noRefCtrl` | 332–333 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `setRef rs s`, `eraseRef` | 336–339 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `eraseSim` | 465 | def (Sim) | ADMITTED (its `comm` is a proof; see `erase_sim`) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `HALTED0`, `HALTED1` | 499–500 | def | ADMITTED (data) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `constSim C T t ht` | 507 | def (Sim) | ADMITTED (its `comm` is a proof) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `InitialCtrl C` | 546 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `StrictSim C1 C2` | 583 | structure | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `idStrict`, `eraseStrict` | 598–601 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `hasDup` | 607 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `twistRef`, `twistF` | 644–647 | def | ADMITTED (countermodel apparatus) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `twistSim`, `twistStrict` | 661–682 | def | ADMITTED | n/a (definition) | `Unit 58` (Definition / Structure) |
| `DUPSTATE` | 687 | def | ADMITTED (unreachable datum) | n/a (definition) | `Unit 58` (Definition / Structure) |
| `allKinds_length` | 133 | theorem | VERIFIED_FINITE | none | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `mem_bools` | 135 | theorem | FROZEN | propext | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `allKinds_complete` | 139 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `interpK_full` | 157 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `live_census` | 172 | theorem | VERIFIED_FINITE | none | `Unit 58` — Substantive (`S`) |
| `fullK_live` | 175 | theorem | VERIFIED_FINITE | none | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `obst5_certified` | 183 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `tworule_executable_of_live` | 190 | theorem | CONDITIONAL: `ResponseLiveB d` (generic over the 128; proof by destructuring and `rfl`) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `obst0_certified`, `lobst_certified` | 218–219 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `battery_obst5_nonempty`, `battery_obst0_nonempty`, `battery_lobst_nonempty` | 223–225 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `dead_without_addcol` | 230 | theorem | VERIFIED_FINITE (REFUTED: `addCol` is dispensable) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `full_resolves_obst5` | 236 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `dead_without_budget` | 243 | theorem | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `full_resolves_obst0` | 247 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `dead_without_refine` | 255 | theorem | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `full_resolves_lobst` | 259 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `noRefK_live`, `noRefK_ne_fullK` | 271–272 | theorem | VERIFIED_FINITE | none | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `nonrefuse_agree` | 280 | theorem | CONDITIONAL: refusal-free event | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `refuse_distinguishes` | 286 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `sim_ext` | 304 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `comp_id`, `id_comp`, `comp_assoc` | 320–326 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `setRef_occ` … `setRef_halted` (8) | 341–355 | theorem | FROZEN | none | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `wfPair_setRef`, `obstP_setRef`, `refineOk_setRef`, `colOk_setRef` | 358–365 | theorem | FROZEN | none / propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `setRef_step_comm` | 371 | theorem | CONDITIONAL: refusal-free event | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `erase_sim` | 489 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `eraseRef_not_id` | 493 | theorem | VERIFIED_FINITE | none | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `halted0_ne_halted1` | 502 | theorem | VERIFIED_FINITE | none | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `const_sims_distinct` | 518 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `two_endo_sims` | 527 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `every_pair_connected` | 536 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `sims_never_unique` | 540 | theorem | FROZEN (REFUTED: uniqueness) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `no_initial_ctrl` | 551 | theorem | REFUTED (initiality) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `no_initial_live_ctrl` | 562 | theorem | REFUTED | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `const_not_strict` | 588 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `hasDup_append_fresh` | 611 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `hasDup_step` | 634 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `twistRef_step` | 649 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `twist_step_comm` | 653 | theorem | CONDITIONAL: refusal-free event | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `twist_ne_erase_at_dup` | 692 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `strict_not_unique` | 698 | theorem | REFUTED (strict uniqueness) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `replay_hasDup` | 708 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `reachable_no_dup` | 717 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `twist_eq_erase_of_no_dup` | 721 | theorem | CONDITIONAL: no duplicate | propext, Quot.sound | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `twist_erase_agree_reachable` | 730 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `sim_pinned` | 737 | theorem | FROZEN | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `genesis_sims_agree_on_reachable` | 761 | theorem | CONDITIONAL: both fix genesis | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `strict_agree_on_reachable` | 768 | theorem | FROZEN (for this hom-set) | propext, Quot.sound | `Unit 58` — Substantive (`S`) |
| `setRef_wit` | (grouped in [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `setRef_prot` | (grouped in [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `setRef_obs` | (grouped in [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `setRef_budget` | (grouped in [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `setRef_licensed` | (grouped in [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |
| `setRef_refusals` | (grouped in [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 58` — Auxiliary (`A`, [`ControllerCategory.md`](audit/modules/ControllerCategory.md)) |

### 5.16 `CountTransport` (`lean4/Derivation/CountTransport.lean`) — Root-imported — `Unit 29`

- **Audit appendix:** [`textbook/audit/modules/CountTransport.md`](audit/modules/CountTransport.md)
- **Auxiliary / omission justification:** Omit: `list_map_inj`, `mapInst_inj` (standard); keep the countermodel.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `DRen n` | 50 | structure | ADMITTED (a bijection on all of `Nat`, not merely on the admitted range) | n/a (definition) | `Unit 29` (Definition / Structure) |
| `DRen.inv` | 68 | def | ADMITTED | n/a (definition) | `Unit 29` (Definition / Structure) |
| `mapInst` | 79 | def | ADMITTED | n/a (definition) | `Unit 29` (Definition / Structure) |
| `mapCtx` | 83 | def | ADMITTED | n/a (definition) | `Unit 29` (Definition / Structure) |
| `renameRegime` | 90 | def | ADMITTED (declared action; `reqs` deliberately not renamed) | n/a (definition) | `Unit 29` (Definition / Structure) |
| `cmRegime` | 286 | def | ADMITTED | n/a (definition) | `Unit 29` (Definition / Structure) |
| `DRen.f_inj` | 62 | theorem | FROZEN | not in artifact | `Unit 29` — Auxiliary (`A`, [`CountTransport.md`](audit/modules/CountTransport.md)) |
| `list_map_inj` | 93 | theorem | FROZEN | not in artifact | `Unit 29` — Auxiliary (`A`, [`CountTransport.md`](audit/modules/CountTransport.md)) |
| `mapInst_inj` | 110 | theorem | FROZEN | not in artifact | `Unit 29` — Auxiliary (`A`, [`CountTransport.md`](audit/modules/CountTransport.md)) |
| `plug_mapCtx` | 125 | theorem | FROZEN | propext, Quot.sound | `Unit 29` — Substantive (`S`) |
| `derivable_rename` | 137 | theorem | CONDITIONAL: `f` injective (named hypothesis `hf`) | propext, Quot.sound | `Unit 29` — Substantive (`S`) |
| `wfCtx_rename` | 154 | theorem | CONDITIONAL: `r.data = n` and the bound fields of `σ` | propext, Quot.sound | `Unit 29` — Substantive (`S`) |
| `mapCtx_f_g` | 189 | theorem | FROZEN | not in artifact | `Unit 29` — Auxiliary (`A`, [`CountTransport.md`](audit/modules/CountTransport.md)) |
| `collapsed_rename` | 204 | theorem | CONDITIONAL: `σ` a `DRen n` with `r.data = n` (bounds used only through `wfCtx_rename`) | propext, Quot.sound | `Unit 29` — Substantive (`S`) |
| `collapsedCount_rename` | 239 | theorem | CONDITIONAL: `hp`, `hq` (caller-supplied decision procedures), `σ`, `r.data = n` | propext, Quot.sound | `Unit 29` — Substantive (`S`) |
| `rename_insts_wf` | 258 | theorem | CONDITIONAL: `r.data = n`, the instance conjunct holds for `r` | propext, Quot.sound | `Unit 29` — Auxiliary (`A`, [`CountTransport.md`](audit/modules/CountTransport.md)) |
| `cmRegime_wf` | 288 | theorem | VERIFIED_FINITE (simp on a concrete regime) | not in artifact | `Unit 29` — Auxiliary (`A`, [`CountTransport.md`](audit/modules/CountTransport.md)) |
| `cm_separable` | 292 | theorem | VERIFIED_FINITE (`decide`) | propext, Quot.sound | `Unit 29` — Auxiliary (`A`, [`CountTransport.md`](audit/modules/CountTransport.md)) |
| `non_injective_does_not_transport` | 300 | theorem | REFUTED (countermodel to transport without injectivity) | propext, Quot.sound | `Unit 29` — Substantive (`S`) |

### 5.17 `Counting` (`lean4/Derivation/Counting.lean`) — Root-imported — `Unit 28`

- **Audit appendix:** [`textbook/audit/modules/Counting.md`](audit/modules/Counting.md)
- **Auxiliary / omission justification:** Omit: `index_le_strict_mono` as a displayed theorem; present `no_supply_round_bound` as the instance of the law at `B = n(n-1)/2`.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `allPairs` | 61 | def | ADMITTED (the declared requirement language) | n/a (definition) | `Unit 28` (Definition / Structure) |
| `index_le_strict_mono` | 15 | theorem | CONDITIONAL: `hstrict` (a law about an arbitrary measure) | propext, Quot.sound | `Unit 28` — Auxiliary (`A`, [`Counting.md`](audit/modules/Counting.md)) |
| `strict_bounded_length` | 30 | theorem | CONDITIONAL: `hstrict`, `hbound` | propext, Quot.sound | `Unit 28` — Substantive (`S`) |
| `no_supply_round_bound` | 53 | theorem | CONDITIONAL: `hstrict`, `hbound` (docstring itself says "Conditional") | propext, Quot.sound | `Unit 28` — Substantive (`S`) |
| `allPairs_length` | 69 | theorem | FROZEN | propext, Quot.sound | `Unit 28` — Substantive (`S`) |

### 5.18 `DiffAnchor` (`lean4/Derivation/DiffAnchor.lean`) — Parked (`ParkedAudit.lean`) — `Unit 68`

- **Audit appendix:** [`textbook/audit/modules/DiffAnchor.md`](audit/modules/DiffAnchor.md)
- **Auxiliary / omission justification:** Recommend omitting from the textbook: the module as a separate unit. Its content is a three-line corollary of ContactBridge + ObsDescent; it is parked, uncited by the paper, and labelled with an undefined task code ("BR-0"). Fold the two substantive facts into the ObsDescent/ContactBridge lesson and note that `DiffAnchor` exists as the named handle.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `colObs cols` | 44 | def | ADMITTED (a name for an existing witness; `cols : List (List Nat)` is declared data) | n/a (definition) | `Unit 68` (Definition / Structure) |
| `colObs_zeroRel_iff_zeroP` | 48 | theorem | FROZEN (over all declared `cols`) | propext, Quot.sound | `Unit 68` — Auxiliary (`A`, [`DiffAnchor.md`](audit/modules/DiffAnchor.md)) |
| `colObs_quotient_eq_iff_zeroP` | 56 | theorem | FROZEN | propext, Quot.sound | `Unit 68` — Substantive (`S`) |
| `colObs_deltaConstant` | 64 | theorem | FROZEN | propext, Quot.sound | `Unit 68` — Substantive (`S`) |

### 5.19 `DiffAnchorCompat` (`lean4/Derivation/DiffAnchorCompat.lean`) — Parked (`ParkedAudit.lean`) — `Unit 68`

- **Audit appendix:** [`textbook/audit/modules/DiffAnchorCompat.md`](audit/modules/DiffAnchorCompat.md)
- **Auxiliary / omission justification:** All substantive declarations are taught in the unit; auxiliary helpers (`A`) are documented in the audit record.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|

### 5.20 `DiffInterface` (`lean4/Derivation/DiffInterface.lean`) — Root-imported — `Unit 44`

- **Audit appendix:** [`textbook/audit/modules/DiffInterface.md`](audit/modules/DiffInterface.md)
- **Auxiliary / omission justification:** Recommend omitting: `no_bool_view_is_closed` (duplicate name), `tower_demand_characterized`/`tower_demand_bound` (bookkeeping), the unused certificate fields from the lesson's statement of `BareReflection` (teach the four fields the theorem spends, then say the rest are the caller's shape).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `DiffObs X R` | 33 | structure | ADMITTED (an observer is admitted with its proofs) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `ZeroRel O x y` | 42 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `kernelObs view` | 54 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `obsSetoid`, `ObsQuotient`, `ObsQuotient.mk` | 69–75 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `Stage X R` | 92 | structure | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `ActiveObstruction S x y` | 101 | def | ADMITTED (definition of the obstruction) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `Stage.withObs` | 105 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `BareReflection S S'` | 133 | structure | ADMITTED (declared certificate shape) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `Refines O₂ O₁` | 166 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `StageMaps S` | 184 | structure | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `MapSaturated G D` | 195 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `ClosureStep S G` | 203 | structure | ADMITTED (declared step shape) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `ClosureStep.apply` | 212 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `RequestKind`, `ExtensionProposal`, `ClosureOutcome` | 244–253 | inductive/structure/inductive | ADMITTED (discipline: proposals are data) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `RunResult`, `drive` | 259, 264 | inductive, def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `cview h i` | 306 | def | ADMITTED (declared observer family) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `mkStage s h` | 308 | def | ADMITTED (the tower stage) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `towerReflection n` | 335 | def | ADMITTED (instance) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `swapTop n` | 374 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `towerMaps n` | 386 | def | ADMITTED (instance) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `towerDemand n` | 433 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `towerClosure n` | 438 | def | ADMITTED (instance) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `activePairs s h`, `measureC s h` | 497, 523 | def | ADMITTED (declared measure) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `towerDemandList n` | 567 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `towerNext` | 594 | def | ADMITTED (declared driver) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `bStage view` | 637 | def | ADMITTED | n/a (definition) | `Unit 44` (Definition / Structure) |
| `boolProposal view'` | 663 | def | ADMITTED (data) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `freshUnguarded`, `tagView`, `tagStage`, `edgeView`, `edgeStage`, `hashStage`, `tokenOf`, `repetitionStage` | 680–752 | def | ADMITTED (countermodel data) | n/a (definition) | `Unit 44` (Definition / Structure) |
| `zeroRel_equivalence` | 45 | theorem | FROZEN | none | `Unit 44` — Substantive (`S`) |
| `kernel_zeroRel` | 61 | theorem | FROZEN | none | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `obsQuotient_eq_of_zero` | 78 | theorem | FROZEN | Quot.sound | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `no_guard_no_obstruction` | 111 | theorem | CONDITIONAL:`∀ x y, ¬ guarded` | none | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `unretained_not_active` | 115 | theorem | FROZEN | none | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `distinguished_not_active` | 119 | theorem | FROZEN | none | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `bare_reflection_certifies_active_obstruction` | 155 | theorem | FROZEN (given the certificate) | none | `Unit 44` — Substantive (`S`) |
| `refines_preserves_distinctions` | 171 | theorem | CONDITIONAL:`Refines` | none | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `closure_preserves_old_distinctions` | 216 | theorem | FROZEN (given `C`) | none | `Unit 44` — Substantive (`S`) |
| `closure_kills_demanded` | 223 | theorem | FROZEN (given `C`) | none | `Unit 44` — Substantive (`S`) |
| `closure_adds_no_obstruction` | 232 | theorem | FROZEN (given `C`) | none | `Unit 44` — Substantive (`S`) |
| `drive_terminates` | 276 | theorem | CONDITIONAL:strict decrease, `μ s < fuel` | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `cview_distinct_mono` | 316 | theorem | FROZEN | propext, Quot.sound | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `tower_closed` | 326 | theorem | FROZEN (∀ s) | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `tower_obstruction` | 368 | theorem | FROZEN (∀ n) | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `swapTop_view` | 376 | theorem | CONDITIONAL:`x < n+2` | propext, Quot.sound | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `swapTop_live_inj` | 381 | theorem | CONDITIONAL:live | propext, Quot.sound | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `tower_step_composes` | 482 | theorem | FROZEN | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `tower_successor_step` | 489 | theorem | FROZEN (∀ n) | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `mem_activePairs` | 502 | theorem | FROZEN | propext, Quot.sound | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `mem_activePairs_iff_active` | 526 | theorem | CONDITIONAL:`i ≠ j` | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `closed_measure_zero` | 537 | theorem | FROZEN | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `preclose_measure_pos` | 555 | theorem | FROZEN | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `tower_demand_characterized` | 570 | theorem | FROZEN | propext | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `tower_demand_bound` | 587 | theorem | FROZEN | none | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `towerNext_decrease` | 599 | theorem | FROZEN | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `tower_fuel_terminates` | 617 | theorem | CONDITIONAL:`measureC s h < fuel` | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `bool_view_pigeonhole` | 632 | theorem | FROZEN (8-case `decide`) | none | `Unit 44` — Substantive (`S`) |
| `bool_grammar_obstruction` | 645 | theorem | FROZEN | propext, Quot.sound | `Unit 44` — Substantive (`S`) |
| `no_bool_view_is_closed` | 656 | theorem | FROZEN (alias) | propext, Quot.sound | `Unit 44` — Auxiliary (`A`, [`DiffInterface.md`](audit/modules/DiffInterface.md)) |
| `cm_freshness` | 683 | theorem | VERIFIED_FINITE | none | `Unit 44` — Substantive (`S`) |
| `cm_tagging` | 700 | theorem | VERIFIED_FINITE | none | `Unit 44` — Substantive (`S`) |
| `cm_edge` | 719 | theorem | VERIFIED_FINITE | none | `Unit 44` — Substantive (`S`) |
| `cm_hash` | 736 | theorem | VERIFIED_FINITE | none | `Unit 44` — Substantive (`S`) |
| `cm_repetition` | 754 | theorem | VERIFIED_FINITE | none | `Unit 44` — Substantive (`S`) |

### 5.21 `EndogenousFidelityGenerator` (`lean4/Derivation/EndogenousFidelityGenerator.lean`) — Root-imported — `Unit 72`

- **Audit appendix:** [`textbook/audit/modules/EndogenousFidelityGenerator.md`](audit/modules/EndogenousFidelityGenerator.md)
- **Auxiliary / omission justification:** Recommend omitting: `generated_structure_is_failed_erasure` as a separate theorem (an existential repackaging of the preceding one); `fidelity_refines_indiscrete` (trivially `True`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `AdmittedStep N i j` | 33 | def | ADMITTED (the declared admission criterion, restated as a Prop) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `indiscreteSetoid I` | 61 | def | ADMITTED (the "attempted universal collapse" — a comparison ceiling) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `GeneratedMultiplicity N` | 74 | abbrev | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `universalCollapse N` | 78 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `admitted_step_has_fidelity_path` | 37 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`EndogenousFidelityGenerator.md`](audit/modules/EndogenousFidelityGenerator.md)) |
| `fidelity_is_least_equivalence_containing_admitted_steps` | 46 | theorem | FROZEN | none | `Unit 72` — Substantive (`S`) |
| `fidelity_refines_indiscrete` | 70 | theorem | FROZEN (trivial: target is `True`) | none | `Unit 72` — Auxiliary (`A`, [`EndogenousFidelityGenerator.md`](audit/modules/EndogenousFidelityGenerator.md)) |
| `universalCollapse_surjective` | 82 | theorem | FROZEN (instance of `collapseMap_surjective`) | Quot.sound | `Unit 72` — Auxiliary (`A`, [`EndogenousFidelityGenerator.md`](audit/modules/EndogenousFidelityGenerator.md)) |
| `no_coherent_path_retains_multiplicity` | 89 | theorem | CONDITIONAL: `NoCoherentPath N i j` | propext, Quot.sound | `Unit 72` — Substantive (`S`) |
| `generated_structure_is_failed_erasure` | 100 | theorem | CONDITIONAL: `NoCoherentPath N i j` | propext, Quot.sound | `Unit 72` — Substantive (`S`) |

### 5.22 `Erasure` (`lean4/Derivation/Erasure.lean`) — Root-imported — `Unit 06`, `Unit 07`

- **Audit appendix:** [`textbook/audit/modules/Erasure.md`](audit/modules/Erasure.md)
- **Auxiliary / omission justification:** Omit: the two `_cons` lemmas.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `TRegime` | 20 | structure | ADMITTED (the token-aware specification) | n/a (definition) | `Unit 06`, `Unit 07` (Definition / Structure) |
| `TEvent` | 29 | inductive | ADMITTED | n/a (definition) | `Unit 06`, `Unit 07` (Definition / Structure) |
| `stepT` | 40 | def | ADMITTED (declared Python dedup semantics) | n/a (definition) | `Unit 06`, `Unit 07` (Definition / Structure) |
| `TRegime.erase` | 62 | def | ADMITTED | n/a (definition) | `Unit 06`, `Unit 07` (Definition / Structure) |
| `eraseEvent` | 68 | def | ADMITTED (state-relative) | n/a (definition) | `Unit 06`, `Unit 07` (Definition / Structure) |
| `replayT` | 107 | def | ADMITTED | n/a (definition) | `Unit 06`, `Unit 07` (Definition / Structure) |
| `eraseHistory` | 113 | def | ADMITTED (state-relative; the erased history depends on the token-aware run) | n/a (definition) | `Unit 06`, `Unit 07` (Definition / Structure) |
| `erase_step` | 79 | theorem | FROZEN | propext, Quot.sound | `Unit 06`, `Unit 07` — Substantive (`S`) |
| `replayT_cons` | 121 | theorem | FROZEN | not in artifact | `Unit 06`, `Unit 07` — Auxiliary (`A`, [`Erasure.md`](audit/modules/Erasure.md)) |
| `replayE_cons` | 127 | theorem | FROZEN | not in artifact | `Unit 06`, `Unit 07` — Auxiliary (`A`, [`Erasure.md`](audit/modules/Erasure.md)) |
| `erase_replay` | 138 | theorem | FROZEN | propext, Quot.sound | `Unit 06`, `Unit 07` — Substantive (`S`) |

### 5.23 `Ext` (`lean4/Derivation/Ext.lean`) — Root-imported — `Unit 36`

- **Audit appendix:** [`textbook/audit/modules/Ext.md`](audit/modules/Ext.md)
- **Auxiliary / omission justification:** Omit: `SetEq.*`, `RegimeExt.refl'/symm'`, `applyItem_ext` (fold into one sentence).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `SetEq` | 21 | def | ADMITTED | n/a (definition) | `Unit 36` (Definition / Structure) |
| `RegimeExt` | 37 | def | ADMITTED (the declared bridge relation) | n/a (definition) | `Unit 36` (Definition / Structure) |
| `OptExt` | 86 | def | ADMITTED | n/a (definition) | `Unit 36` (Definition / Structure) |
| `SetEq.rfl'` | 23 | theorem | FROZEN | not in artifact | `Unit 36` — Auxiliary (`A`, [`Ext.md`](audit/modules/Ext.md)) |
| `SetEq.symm'` | 26 | theorem | FROZEN | not in artifact | `Unit 36` — Auxiliary (`A`, [`Ext.md`](audit/modules/Ext.md)) |
| `SetEq.insertNew'` | 29 | theorem | FROZEN | not in artifact | `Unit 36` — Auxiliary (`A`, [`Ext.md`](audit/modules/Ext.md)) |
| `RegimeExt.refl'` | 41 | theorem | FROZEN | not in artifact | `Unit 36` — Auxiliary (`A`, [`Ext.md`](audit/modules/Ext.md)) |
| `RegimeExt.symm'` | 44 | theorem | FROZEN | not in artifact | `Unit 36` — Auxiliary (`A`, [`Ext.md`](audit/modules/Ext.md)) |
| `derivable_ext` | 50 | theorem | FROZEN | none | `Unit 36` — Substantive (`S`) |
| `wfCtx_ext` | 56 | theorem | FROZEN | propext | `Unit 36` — Substantive (`S`) |
| `collapsed_ext` | 62 | theorem | FROZEN | propext | `Unit 36` — Substantive (`S`) |
| `separable_ext` | 74 | theorem | FROZEN | propext | `Unit 36` — Substantive (`S`) |
| `applyItem_ext` | 92 | theorem | FROZEN | propext | `Unit 36` — Substantive (`S`) |
| `applyDelta_ext` | 129 | theorem | FROZEN | propext | `Unit 36` — Substantive (`S`) |
| `validResponse_ext` | 152 | theorem | FROZEN | propext | `Unit 36` — Substantive (`S`) |

### 5.24 `FidelityClosure` (`lean4/Derivation/FidelityClosure.lean`) — Root-imported — `Unit 72`

- **Audit appendix:** [`textbook/audit/modules/FidelityClosure.md`](audit/modules/FidelityClosure.md)
- **Auxiliary / omission justification:** Recommend omitting: `polarity_flip_is_presentation_relative` (pure restatement with `Y := Bool`), unless the lesson wants the inside/outside vocabulary made explicit.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `TranslationNetwork` | 43 | structure (Type 1) | ADMITTED (the supplied network; three `Type`-valued fields) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `FidelityPath N i j` | 54 | inductive (Type) | ADMITTED (the generating rule for fidelity — a declared admission criterion) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `FidelityPath.toBij` | 65 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `FidelityRel N i j` | 75 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `fidelitySetoid N` | 97 | def | ADMITTED (derived from the three theorems below) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `FidelityQuotient N` | 104 | abbrev | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `classOf N i` | 106 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `NoCoherentPath N i j` | 119 | def | ADMITTED (a proposition, not a decision procedure — header of EndogenousFidelityGenerator says so) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `LoopTrivial loop` | 143 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `HolonomyResidual N` | 149 | structure | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `FaithfulNetworkDescent N` | 158 | structure (Type 1) | ADMITTED (declared notion of global descent; `Carrier : Type` is metatheoretic existential output) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `AllLoopsTrivial N` | 177 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `LabelInvariant label` | 189 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `LabelDescends label` | 193 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `fidelity_refl` | 78 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`FidelityClosure.md`](audit/modules/FidelityClosure.md)) |
| `fidelity_symm` | 82 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`FidelityClosure.md`](audit/modules/FidelityClosure.md)) |
| `fidelity_trans` | 87 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`FidelityClosure.md`](audit/modules/FidelityClosure.md)) |
| `class_eq_iff_coherent_path` | 109 | theorem | FROZEN | propext, Quot.sound | `Unit 72` — Substantive (`S`) |
| `no_coherent_path_retains_indices` | 122 | theorem | CONDITIONAL: `NoCoherentPath N i j` | propext, Quot.sound | `Unit 72` — Substantive (`S`) |
| `failed_endomorphism_does_not_refute_self_fidelity` | 133 | theorem | FROZEN (the residual hypothesis is unused; the conclusion is `fidelity_refl`) | none | `Unit 72` — Substantive (`S`) |
| `holonomy_residual_refuses_faithful_network_descent` | 167 | theorem | CONDITIONAL: a round-trip transport residual | none | `Unit 72` — Substantive (`S`) |
| `faithful_network_descent_forces_trivial_loops` | 180 | theorem | FROZEN | none | `Unit 72` — Substantive (`S`) |
| `label_descends_iff_fidelity_invariant` | 198 | theorem | FROZEN | Quot.sound | `Unit 72` — Substantive (`S`) |
| `coherent_disagreement_refuses_label_descent` | 215 | theorem | CONDITIONAL: the two hypotheses | Quot.sound | `Unit 72` — Auxiliary (`A`, [`FidelityClosure.md`](audit/modules/FidelityClosure.md)) |
| `polarity_flip_is_presentation_relative` | 227 | theorem | CONDITIONAL: same | Quot.sound | `Unit 72` — Auxiliary (`A`, [`FidelityClosure.md`](audit/modules/FidelityClosure.md)) |

### 5.25 `FormRenaming` (`lean4/Derivation/FormRenaming.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/FormRenaming.md`](audit/modules/FormRenaming.md)
- **Auxiliary / omission justification:** Omit: nothing beyond folding the auxiliary lemmas inline.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `permForms g forms` | 41 | def | ADMITTED | n/a (definition) | `Unit 74` (Definition / Structure) |
| `mapInstForm φ i` | 64 | def | ADMITTED | n/a (definition) | `Unit 74` (Definition / Structure) |
| `renameForms φ g r` | 69 | def | ADMITTED (the form action) | n/a (definition) | `Unit 74` (Definition / Structure) |
| `permForms_length` | 44 | theorem | FROZEN | propext, Quot.sound | `Unit 74` — Auxiliary (`A`, [`FormRenaming.md`](audit/modules/FormRenaming.md)) |
| `permForms_getD` | 53 | theorem | CONDITIONAL: `j < forms.length` (docstring explains why: out of range `g` may map back in) | propext | `Unit 74` — Auxiliary (`A`, [`FormRenaming.md`](audit/modules/FormRenaming.md)) |
| `renameForms_data`, `renameForms_reqs` | 75, 78 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`FormRenaming.md`](audit/modules/FormRenaming.md)) |
| `renameForms_forms_length` | 81 | theorem | FROZEN | propext, Quot.sound | `Unit 74` — Auxiliary (`A`, [`FormRenaming.md`](audit/modules/FormRenaming.md)) |
| `renameForms_arity` | 90 | theorem | CONDITIONAL: bound and local inverse | propext | `Unit 74` — Substantive (`S`) |
| `Regime.ext'` | 99 | theorem | FROZEN | not in artifact; probed propext | `Unit 74` — Auxiliary (`A`, [`FormRenaming.md`](audit/modules/FormRenaming.md)) |
| `mapInstForm_gf` | 106 | theorem | CONDITIONAL: `g (φ i.1) = i.1` | none | `Unit 74` — Auxiliary (`A`, [`FormRenaming.md`](audit/modules/FormRenaming.md)) |
| `renameForms_gf` | 120 | theorem | FROZEN (over any `DRen r.forms.length`) | propext, Quot.sound | `Unit 74` — Substantive (`S`) |

### 5.26 `FormTransport` (`lean4/Derivation/FormTransport.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/FormTransport.md`](audit/modules/FormTransport.md)
- **Auxiliary / omission justification:** Omit: the three `rfl` projections.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `mapCtxForm φ c` | 76 | def | ADMITTED | n/a (definition) | `Unit 74` (Definition / Structure) |
| `renameForms_forms`, `renameForms_insts`, `renameForms_rules` | 62–68 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`FormTransport.md`](audit/modules/FormTransport.md)) |
| `plug_mapCtxForm` | 80 | theorem | FROZEN | none | `Unit 74` — Auxiliary (`A`, [`FormTransport.md`](audit/modules/FormTransport.md)) |
| `mapCtxForm_f_g` | 84 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`FormTransport.md`](audit/modules/FormTransport.md)) |
| `mapInstForm_inj` | 91 | theorem | CONDITIONAL: `φ` injective | propext | `Unit 74` — Auxiliary (`A`, [`FormTransport.md`](audit/modules/FormTransport.md)) |
| `derivable_renameForms` | 102 | theorem | CONDITIONAL: `φ` injective | propext, Quot.sound | `Unit 74` — Substantive (`S`) |
| `wfCtx_renameForms` | 118 | theorem | FROZEN (over any such `σ`) | propext, Quot.sound | `Unit 74` — Substantive (`S`) |
| `collapsed_renameForms` | 137 | theorem | FROZEN (over any `σ : DRen r.forms.length`) | propext, Quot.sound | `Unit 74` — Substantive (`S`) |
| `collapsed_congr` | 165 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`FormTransport.md`](audit/modules/FormTransport.md)) |
| `collapsed_renameDataForm` | 189 | theorem | CONDITIONAL: `r.data = n` | propext, Quot.sound | `Unit 74` — Substantive (`S`) |

### 5.27 `FormTransportCompat` (`lean4/Derivation/FormTransportCompat.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/FormTransportCompat.md`](audit/modules/FormTransportCompat.md)
- **Auxiliary / omission justification:** All substantive declarations are taught in the unit; auxiliary helpers (`A`) are documented in the audit record.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|

### 5.28 `G1Class` (`lean4/Derivation/G1Class.lean`) — Root-imported — `Unit 43`

- **Audit appendix:** [`textbook/audit/modules/G1Class.md`](audit/modules/G1Class.md)
- **Auxiliary / omission justification:** Recommend omitting: `local_strategy_cycle_impossible` as a separate theorem (it is the third conjunct of `g1_class_exclusion`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `local_strategy_cycle_impossible` | 22 | theorem | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `g1_class_exclusion` | 30 | theorem | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `clears_does_not_imply_not_fires` | 41 | theorem | REFUTED (of "clears ⇒ not fires") | propext, Quot.sound | `Unit 43` — Substantive (`S`) |

### 5.29 `Generator` (`lean4/Derivation/Generator.lean`) — Root-imported — `Unit 40`

- **Audit appendix:** [`textbook/audit/modules/Generator.md`](audit/modules/Generator.md)
- **Auxiliary / omission justification:** Recommend omitting: `le_foldr_max` (library-grade); possibly `valued_marks_collapse_generation` as a theorem (its content is definitional — the index is in the profile — and is better taught as one sentence).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `profile1` | 55 | def | ADMITTED (declared observation regime) | n/a (definition) | `Unit 40` (Definition / Structure) |
| `profileV` | 243 | def | ADMITTED (declared "valued automark" regime; identity-grade by construction) | n/a (definition) | `Unit 40` (Definition / Structure) |
| `swap12` | 259 | def | ADMITTED | n/a (definition) | `Unit 40` (Definition / Structure) |
| `profile2` | 277 | def | ADMITTED (declared depth-2 regime) | n/a (definition) | `Unit 40` (Definition / Structure) |
| `reflective_chain_tags` | 35 | theorem | FROZEN (∀ n) | propext | `Unit 40` — Auxiliary (`A`, [`Generator.md`](audit/modules/Generator.md)) |
| `chain_tagged_iff` | 60 | theorem | FROZEN | propext, Quot.sound | `Unit 40` — Auxiliary (`A`, [`Generator.md`](audit/modules/Generator.md)) |
| `chain_hasIn_iff` | 70 | theorem | FROZEN | propext, Quot.sound | `Unit 40` — Auxiliary (`A`, [`Generator.md`](audit/modules/Generator.md)) |
| `chain_hasOut_iff` | 82 | theorem | FROZEN | propext, Quot.sound | `Unit 40` — Auxiliary (`A`, [`Generator.md`](audit/modules/Generator.md)) |
| `middle_profile` | 97 | theorem | CONDITIONAL:`1 ≤ i`, `i < n` | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `endpoint0_profile` | 105 | theorem | CONDITIONAL:`1 ≤ n` | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `endpointN_profile` | 115 | theorem | CONDITIONAL:`1 ≤ n` | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `depth1_obstructions_are_exactly_middle_pairs` | 131 | theorem | CONDITIONAL:`1 ≤ n`, `i ≤ n`, `j ≤ n`, `i ≠ j` | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `generation_never_dries` | 183 | theorem | CONDITIONAL:`3 ≤ n` (∀ n, metatheoretic) | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `automark_presence_vacuous` | 198 | theorem | CONDITIONAL:`3 ≤ n` | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `le_foldr_max` | 204 | theorem | FROZEN (list lemma) | propext, Quot.sound | `Unit 40` — Auxiliary (`A`, [`Generator.md`](audit/modules/Generator.md)) |
| `finite_marks_outrun` | 221 | theorem | FROZEN (∀ finite list) | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `valued_marks_collapse_generation` | 246 | theorem | FROZEN (immediate: the second component is `i`) | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `middle_swap_not_relation_preserving` | 261 | theorem | CONDITIONAL:`2 ≤ n` | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `depth2_separates_near_ends_n4` | 287 | theorem | VERIFIED_FINITE (`decide`) | propext, Quot.sound | `Unit 40` — Substantive (`S`) |
| `depth2_obstruction_n5` | 292 | theorem | VERIFIED_FINITE (`decide`) | propext, Quot.sound | `Unit 40` — Substantive (`S`) |

### 5.30 `GraphGenesis` (`lean4/Derivation/GraphGenesis.lean`) — Root-imported — `Unit 63`

- **Audit appendix:** [`textbook/audit/modules/GraphGenesis.md`](audit/modules/GraphGenesis.md)
- **Auxiliary / omission justification:** Recommend omitting: `refineCol_only_obs` and `addCol_only_obs` as separate items (special cases of `response_step_fixes_graph`); `preserves_separated` detail of `ProposalRecord` can be summarised.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `MentionsOnlyExisting s` | 137 | def | ADMITTED | n/a (definition) | `Unit 63` (Definition / Structure) |
| `IsInternal` | 190 | def | ADMITTED (declared fragment) | n/a (definition) | `Unit 63` (Definition / Structure) |
| `IsResponseEvent` | 224 | def | ADMITTED | n/a (definition) | `Unit 63` (Definition / Structure) |
| `GraphStoresFixed s t` | 244 | def | ADMITTED | n/a (definition) | `Unit 63` (Definition / Structure) |
| `ProposalRecord s` | 381 | structure | ADMITTED (a declared proposal schema; `embed`/`retract` are Nat → Nat data) | n/a (definition) | `Unit 63` (Definition / Structure) |
| `upProposal s hwf hh p hp` | 452 | def | ADMITTED | n/a (definition) | `Unit 63` (Definition / Structure) |
| `tri` | 552 | def | ADMITTED (datum) | n/a (definition) | `Unit 63` (Definition / Structure) |
| `triProp1`, `triProp2` | 564–568 | def | ADMITTED | n/a (definition) | `Unit 63` (Definition / Structure) |
| `funded s` | 606 | def | ADMITTED | n/a (definition) | `Unit 63` (Definition / Structure) |
| `FamilyGrowsCarrier s` | 651 | def | ADMITTED | n/a (definition) | `Unit 63` (Definition / Structure) |
| `blindPair` | 666 | def | ADMITTED (datum) | n/a (definition) | `Unit 63` (Definition / Structure) |
| `refineCol_only_obs` | 59 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `addCol_only_obs` | 75 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `extensionProposals_range_over_existing` | 99 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `repairFamily_range_over_existing` | 116 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `nextFamilyP_block_shape` | 146 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `nextFamilyP_range_over_existing` | 165 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `IsInternal_exact` | 204 | theorem | FROZEN | none | `Unit 63` — Auxiliary (`A`, [`GraphGenesis.md`](audit/modules/GraphGenesis.md)) |
| `internal_is_response` | 237 | theorem | FROZEN | none | `Unit 63` — Auxiliary (`A`, [`GraphGenesis.md`](audit/modules/GraphGenesis.md)) |
| `response_step_fixes_graph` | 250 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `internal_step_fixes_graph` | 259 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Auxiliary (`A`, [`GraphGenesis.md`](audit/modules/GraphGenesis.md)) |
| `replay_fixes_graph_of_all` | 264 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Auxiliary (`A`, [`GraphGenesis.md`](audit/modules/GraphGenesis.md)) |
| `internal_family_cannot_grow_carrier` | 283 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `response_replay_fixes_graph` | 291 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `nextFamilyP_blocks_are_responses` | 299 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Auxiliary (`A`, [`GraphGenesis.md`](audit/modules/GraphGenesis.md)) |
| `nextFamilyP_block_fixes_graph` | 317 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `graph_growth_is_supplied` | 340 | theorem | CONDITIONAL: WFStores, live, `p < len` | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `proposal_confers_no_execution` | 441 | theorem | CONDITIONAL: halted | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `upProposal_executes` | 507 | theorem | CONDITIONAL: WFStores, live, `p < len` | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `proposal_transports` | 533 | theorem | CONDITIONAL: `n = len`, WFStores, live | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `tri_wf`, `tri_live`, `tri_parent1`, `tri_parent2` | 554–561 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 63` — Auxiliary (`A`, [`GraphGenesis.md`](audit/modules/GraphGenesis.md)) |
| `proposal_family_retains_ties` | 576 | theorem | VERIFIED_FINITE (REFUTED: equal cost does not select) | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `obstruction_resolved_in_carrier` | 614 | theorem | CONDITIONAL: six named hypotheses | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `family_never_grows_carrier` | 655 | theorem | FROZEN | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `growth_demand_not_obstruction_consequence` | 693 | theorem | VERIFIED_FINITE (first four conjuncts) + FROZEN (last) | propext, Quot.sound | `Unit 63` — Substantive (`S`) |
| `blindPair_resolution_keeps_carrier` | 711 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 63` — Auxiliary (`A`, [`GraphGenesis.md`](audit/modules/GraphGenesis.md)) |

### 5.31 `HigherStructure` (`lean4/Derivation/HigherStructure.lean`) — Root-imported — `Unit 55`

- **Audit appendix:** [`textbook/audit/modules/HigherStructure.md`](audit/modules/HigherStructure.md)
- **Auxiliary / omission justification:** Recommend omitting from the textbook: `altNum` and `altNum_stages` (a statistic on one example, with a docstring that calls it an invariant; nothing is proved about it), and `path_connectivity_residue` as a standalone claim (it is a corollary of `graph_growth` and proves neither connectedness nor acyclicity). Teach `cutCensus` only as a finite count on carriers 2–4 with the general growth left open.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `growBlock` | 72 | def | ADMITTED (declared driver policy; the graph data is supplied, not derived) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `growHist` | 80 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `graphAt` | 85 | def | ADMITTED (a `Nat → PState` family; metatheoretic indexing) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `pathState` | 91 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `g1`, `gA`, `g2`, `preCol`, `g3` | 248, 257, 263, 271, 287 | def | ADMITTED (proof scaffolding) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `Complex` | 555 | structure | ADMITTED (declared realization layer) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `emptyComplex` | 562 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `shell1` | 565 | def | ADMITTED (declared guard) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `edgeIn` | 569 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `shell2` | 574 | def | ADMITTED (declared guard) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `triIn` | 578 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `shell3` | 583 | def | ADMITTED (declared guard) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `CEvent` | 587 | inductive | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `cstep` | 597 | def | ADMITTED (declared policy) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `creplay` | 609 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `k4PassageHist` | 664 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `k4Events` | 684 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `k4` | 691 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `k4Boundary` | 693 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `altNum` | 722 | def | c0 | n/a (definition) | `Unit 55` (Definition / Structure) |
| `subsetsOf` | 737 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `cutCensus` | 745 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `bd1`, `bd2`, `bd2'`, `bd3` | 765, 768, 772, 775 | def | ADMITTED (declared convention) | n/a (definition) | `Unit 55` (Definition / Structure) |
| `push1`, `push2` | 780, 783 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `coeffV`, `coeffE` | 787, 790 | def | ADMITTED | n/a (definition) | `Unit 55` (Definition / Structure) |
| `grow_fresh` | 101 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `grow_wit_not_mem` | 105 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `grow_col_not_mem` | 114 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `grow_cols_blind` | 126 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `grow_col_separates` | 144 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `grow_pair_separated` | 156 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `grow_zero` | 168 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `pstep_admit` | 187 | theorem | CONDITIONAL: `s.halted = false`, `t ∉ s.occ` | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `pstep_assert` | 194 | theorem | CONDITIONAL: halted = false, guard | not in artifact | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `pstep_wit` | 203 | theorem | CONDITIONAL: halted = false, guard | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `pstep_prot` | 211 | theorem | CONDITIONAL: halted = false, guard | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `pstep_budget` | 219 | theorem | CONDITIONAL: halted = false | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `pstep_addCol` | 224 | theorem | CONDITIONAL: halted = false, `obs = some cols`, guard | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `colOk_some` | 236 | theorem | CONDITIONAL: `s.obs = some cols` | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `grow_len` | 282 | theorem | FROZEN | propext | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `assert_guard` | 298 | theorem | FROZEN | not in artifact | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `wit_guard` | 313 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `prot_guard` | 333 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `reach_preCol` | 350 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `round_obstruction` | 381 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `round_two_rule` | 395 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `round_resolution` | 406 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `round_creation_record` | 469 | theorem | FROZEN (definitional) | none | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `graphAt_spec` | 476 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `graph_growth` | 495 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `graphAt_quiescent` | 510 | theorem | FROZEN | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `path_connectivity_residue` | 536 | theorem | occ | − | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |
| `ladder_dim2` | 616 | theorem | CONDITIONAL: `shell2 C i j k = true` (over all `C`) | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `ladder_dim3` | 635 | theorem | CONDITIONAL: `shell3 = true` | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `shell_guard_load_bearing` | 654 | theorem | VERIFIED_FINITE (countermodel to "incomplete boundaries fill") | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `k4_skeleton_from_passage` | 672 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `k4_builds` | 699 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `k4_skeleton_agrees` | 708 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `filling_not_forced` | 714 | theorem | VERIFIED_FINITE (countermodel to "a complete boundary fills itself") | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `altNum_stages` | 730 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `cut_census_growth` | 752 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `d2_zero_triangles` | 796 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `d2_zero_tet` | 801 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `boundary_not_forced` | 808 | theorem | VERIFIED_FINITE (countermodel to "the boundary convention is determined by the graph") | propext, Quot.sound | `Unit 55` — Substantive (`S`) |
| `instantiated` | (grouped in [`HigherStructure.md`](audit/modules/HigherStructure.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 55` — Auxiliary (`A`, [`HigherStructure.md`](audit/modules/HigherStructure.md)) |

### 5.32 `Horizon` (`lean4/Derivation/Horizon.lean`) — Root-imported — `Unit 50`

- **Audit appendix:** [`textbook/audit/modules/Horizon.md`](audit/modules/Horizon.md)
- **Auxiliary / omission justification:** Omit: the two saturation `decide` theorems (a footnote on the Python repair suffices).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| specViews | 45 | def | ADMITTED (specification) | n/a (definition) | `Unit 50` (Definition / Structure) |
| specReqs | 49 | def | ADMITTED | n/a (definition) | `Unit 50` (Definition / Structure) |
| specWorld | 53 | def | ADMITTED | n/a (definition) | `Unit 50` (Definition / Structure) |
| w1 / w2 / w3 | 59 / 65 / 71 | def | ADMITTED | n/a (definition) | `Unit 50` (Definition / Structure) |
| satNoopWorld | 402 | def | ADMITTED | n/a (definition) | `Unit 50` (Definition / Structure) |
| specViews_succ | 76 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| specReqs_succ | 82 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| fresh_not_mem | 90 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| req_not_mem | 95 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| view_not_mem | 103 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| data_len | 113 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| sep_new_col | 118 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| old_cols_blind | 127 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| step_admit_fresh | 144 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| step_require_ok | 149 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| step_addView_ok | 155 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| req_guard | 165 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| satB_w3_false | 176 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| increase_guard | 185 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| aug_guard | 201 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| final_assembly | 222 | theorem | FROZEN | not in artifact | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| worldAt_spec | 236 | theorem | FROZEN | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| worldAt_quiescent | 261 | theorem | FROZEN | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| worldAt_wf | 275 | theorem | FROZEN | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| block_all_accepted | 294 | theorem | FROZEN | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| genesis_accepted | 343 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |
| gen_quiescent | 351 | theorem | FROZEN | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| gen_wf | 358 | theorem | FROZEN | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| interp_budget_bound | 371 | theorem | FROZEN | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| budget_saturation_noop | 411 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| mark_saturation_all_descs | 419 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 50` — Substantive (`S`) |
| `with` | (grouped in [`Horizon.md`](audit/modules/Horizon.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 50` — Auxiliary (`A`, [`Horizon.md`](audit/modules/Horizon.md)) |

### 5.33 `Inertia` (`lean4/Derivation/Inertia.lean`) — Root-imported — `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16`

- **Audit appendix:** [`textbook/audit/modules/Inertia.md`](audit/modules/Inertia.md)
- **Auxiliary / omission justification:** Omit: `replayE_append` as a displayed theorem (state it in prose as "replay is a fold").

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `genesis` | 14 | def | ADMITTED | n/a (definition) | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` (Definition / Structure) |
| `supply_no_op` | 17 | theorem | FROZEN | propext | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `genesis_underivable` | 21 | theorem | FROZEN (structural proof; an instance of `underivable_of_empty` on a concrete regime) | none | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `underivable_of_empty` | 30 | theorem | CONDITIONAL: `insts = []`, `rules = []` | none | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `collapsed_of_no_insts` | 40 | theorem | CONDITIONAL: `insts = []` | propext | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `R2L_collapsed` | 50 | theorem | FROZEN (instance of the previous on a concrete regime) | propext | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `R2F_collapsed` | 54 | theorem | FROZEN (instance) | propext | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `historyL_replays` | 59 | theorem | VERIFIED_FINITE (`decide`) | propext | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `historyF_replays` | 66 | theorem | VERIFIED_FINITE (`decide`) | propext | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `admission_without_expressive_increase` | 76 | theorem | REFUTED (countermodel to "a new inscription necessarily increases expressive power"); witness `⟨3,[],[],[],[(0,1)]⟩`, two conjuncts by `decide`, the third by `collapsed_of_no_insts` | propext | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Substantive (`S`) |
| `replayE_append` | 83 | theorem | FROZEN | propext, Quot.sound | `Unit 01`, `Unit 02`, `Unit 03`, `Unit 04`, `Unit 05`, `Unit 10`, `Unit 12`, `Unit 16` — Auxiliary (`A`, [`Inertia.md`](audit/modules/Inertia.md)) |

### 5.34 `Initiality` (`lean4/Derivation/Initiality.lean`) — Root-imported — `Unit 49`

- **Audit appendix:** [`textbook/audit/modules/Initiality.md`](audit/modules/Initiality.md)
- **Auxiliary / omission justification:** Omit: `retract_section` and `extension_retract` as separate items (both `rfl`; mention in one sentence).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| dupWorld | 52 | def | ADMITTED (probe world) | n/a (definition) | `Unit 49` (Definition / Structure) |
| satWorld | 56 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| brokeWorld | 60 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| unlicensedWorld | 64 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| probeDedup | 70 | def | ADMITTED (declared probe) | n/a (definition) | `Unit 49` (Definition / Structure) |
| probeRequire | 73 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| probeAccept | 76 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| probeBudget | 79 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| probeLicense | 82 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| probeRefusal | 85 | def | ADMITTED | n/a (definition) | `Unit 49` (Definition / Structure) |
| compliantB | 88 | def | ADMITTED (declared battery) | n/a (definition) | `Unit 49` (Definition / Structure) |
| dedup_load_bearing | 99 | theorem | VERIFIED_FINITE / REFUTED (refutes "dedup is redundant") | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| require_guard_load_bearing | 103 | theorem | VERIFIED_FINITE / REFUTED | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| accept_guard_load_bearing | 107 | theorem | VERIFIED_FINITE / REFUTED | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| budget_gate_load_bearing | 111 | theorem | VERIFIED_FINITE / REFUTED | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| license_gate_load_bearing | 115 | theorem | VERIFIED_FINITE / REFUTED | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| refusal_certificate_load_bearing | 119 | theorem | VERIFIED_FINITE / REFUTED | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| unique_compliant | 128 | theorem | VERIFIED_FINITE (64 descriptors × 6 probes, decide) | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| minimum_unique_in_class | 136 | theorem | VERIFIED_FINITE (corollary) | propext, Quot.sound | `Unit 49` — Auxiliary (`A`, [`Initiality.md`](audit/modules/Initiality.md)) |
| extension_retract | 154 | theorem | FROZEN (definitional) | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| extension_retract_replay | 157 | theorem | FROZEN | propext, Quot.sound | `Unit 49` — Substantive (`S`) |
| retract_section | 168 | theorem | FROZEN (definitional) | none | `Unit 49` — Auxiliary (`A`, [`Initiality.md`](audit/modules/Initiality.md)) |

### 5.35 `InterpreterBoundary` (`lean4/Derivation/InterpreterBoundary.lean`) — Root-imported — `Unit 57`

- **Audit appendix:** [`textbook/audit/modules/InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)
- **Auxiliary / omission justification:** Omit: the String labels (report them as receipt text, not as declarations); `i5_family_not_extensionally_complete` (a duplicate name for `family_missed`, kept for the audit trail).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| i0_status | 103 | def (String) | ADMITTED (label, not a proposition) | n/a (definition) | `Unit 57` (Definition / Structure) |
| indexWorld | 114 | def | ADMITTED | n/a (definition) | `Unit 57` (Definition / Structure) |
| diag | 127 | def | ADMITTED (diagonal construction) | n/a (definition) | `Unit 57` (Definition / Structure) |
| tag_quotation … tag_verified_fixed_point | 205–218 | def (String ×5) | ADMITTED (labels) | n/a (definition) | `Unit 57` (Definition / Structure) |
| evalOpt | 233 | def | ADMITTED (one declared extension) | n/a (definition) | `Unit 57` (Definition / Structure) |
| boundarySetting | 286 | def | ADMITTED (declared model; relation, retention and protection inserted by definition) | n/a (definition) | `Unit 57` (Definition / Structure) |
| openDenotationalBridge | 371 | def (String) | OPEN (label) | n/a (definition) | `Unit 57` (Definition / Structure) |
| conclusionTags | 380 | def (List String) | ADMITTED (labels) | n/a (definition) | `Unit 57` (Definition / Structure) |
| frontierConjecture | 390 | def (String) | OPEN (label) | n/a (definition) | `Unit 57` (Definition / Structure) |
| indexWorld_len | 117 | theorem | FROZEN | propext | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| diag_hit | 132 | theorem | FROZEN | propext | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| tower_persists | 156 | theorem | FROZEN (metatheoretic function-space statement) | propext, Quot.sound | `Unit 57` — Substantive (`S`) |
| i2_universal_in_class | 199 | theorem | FROZEN (re-packaging of two Constitution theorems) | propext, Quot.sound | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| i3_refusal_code_returns_none | 241 | theorem | FROZEN (definitional) | propext, Quot.sound | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| i3_coded_member_returns_some | 246 | theorem | FROZEN (definitional) | propext, Quot.sound | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| family_missed | 264 | theorem | FROZEN | propext, Quot.sound | `Unit 57` — Substantive (`S`) |
| i5_carrier_occurrences | 297 | theorem | VERIFIED_FINITE | none | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| i5_boundary_is_A | 306 | theorem | FROZEN (but every conjunct is by definition of `boundarySetting`) | none | `Unit 57` — Substantive (`S`) |
| i5_boundary_is_F | 314 | theorem | FROZEN (definitional) | none | `Unit 57` — Substantive (`S`) |
| i5_collapse_obstructed | 322 | theorem | CONDITIONAL: the presentation identifies the two endpoints | none | `Unit 57` — Substantive (`S`) |
| i5_family_not_extensionally_complete | 349 | theorem | FROZEN | propext, Quot.sound | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| arbitrary_uncoded_assignment | 356 | theorem | FROZEN (trivially true: define `I` by cases) | propext, Quot.sound | `Unit 57` — Substantive (`S`) |
| `worth` | (grouped in [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |
| `applies` | (grouped in [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 57` — Auxiliary (`A`, [`InterpreterBoundary.md`](audit/modules/InterpreterBoundary.md)) |

### 5.36 `IsoBridge` (`lean4/Derivation/IsoBridge.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/IsoBridge.md`](audit/modules/IsoBridge.md)
- **Auxiliary / omission justification:** Omit: nothing; one declaration.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Iso.of_components A B hdata hforms hInst hRule hReq hAord hBord` | 37 | def (Type) | ADMITTED (construction); CONDITIONAL on equal data, equal forms, membership-equal insts/rules/reqs, both requirement lists ordered | n/a (definition) | `Unit 74` (Definition / Structure) |

### 5.37 `IsoBridgeCompat` (`lean4/Derivation/IsoBridgeCompat.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/IsoBridgeCompat.md`](audit/modules/IsoBridgeCompat.md)
- **Auxiliary / omission justification:** All substantive declarations are taught in the unit; auxiliary helpers (`A`) are documented in the audit record.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|

### 5.38 `IsoCanon` (`lean4/Derivation/IsoCanon.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/IsoCanon.md`](audit/modules/IsoCanon.md)
- **Auxiliary / omission justification:** Omit: the projection lemmas.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Iso.trans h k` | 90 | def | ADMITTED (construction) | n/a (definition) | `Unit 74` (Definition / Structure) |
| `relabel r π φ` | 136 | def | ADMITTED (the combined action `serialize` reads off) | n/a (definition) | `Unit 74` (Definition / Structure) |
| `relabel_iso r π φ hord` | 158 | def (Type) | ADMITTED (construction; the mathematical content is in its fields) | n/a (definition) | `Unit 74` (Definition / Structure) |
| `iso_of_relabel_eq … hr hs heq` | 225 | def (Type) | ADMITTED (construction) | n/a (definition) | `Unit 74` (Definition / Structure) |
| `sortPair_eq_minmax` | 53 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `sortPair_comm` | 60 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `mapReq_eq_sortPair` | 65 | theorem | FROZEN | propext | `Unit 74` — Substantive (`S`) |
| `sortPair_map_sortPair` | 70 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `sortPair_of_le` | 77 | theorem | CONDITIONAL: `x ≤ y` | propext | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `relabel_data`, `_forms`, `_insts`, `_rules`, `_reqs` | 139–152 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `relabel_forms` | (grouped in [`IsoCanon.md`](audit/modules/IsoCanon.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `relabel_insts` | (grouped in [`IsoCanon.md`](audit/modules/IsoCanon.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `relabel_rules` | (grouped in [`IsoCanon.md`](audit/modules/IsoCanon.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |
| `relabel_reqs` | (grouped in [`IsoCanon.md`](audit/modules/IsoCanon.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 74` — Auxiliary (`A`, [`IsoCanon.md`](audit/modules/IsoCanon.md)) |

### 5.39 `IsoCanonCompat` (`lean4/Derivation/IsoCanonCompat.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/IsoCanonCompat.md`](audit/modules/IsoCanonCompat.md)
- **Auxiliary / omission justification:** All substantive declarations are taught in the unit; auxiliary helpers (`A`) are documented in the audit record.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|

### 5.40 `IsoCollapse` (`lean4/Derivation/IsoCollapse.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/IsoCollapse.md`](audit/modules/IsoCollapse.md)
- **Auxiliary / omission justification:** Omit: nothing; the chain is short.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Iso.symm h` | 59 | def | ADMITTED | n/a (definition) | `Unit 74` (Definition / Structure) |
| `Iso.imap h i` | 88 | def | ADMITTED | n/a (definition) | `Unit 74` (Definition / Structure) |
| `Iso.cmap h c` | 91 | def | ADMITTED | n/a (definition) | `Unit 74` (Definition / Structure) |
| `map_eq_self_of_mem` | 33 | theorem | FROZEN | propext | `Unit 74` — Auxiliary (`A`, [`IsoCollapse.md`](audit/modules/IsoCollapse.md)) |
| `plug_args_lt` | 44 | theorem | CONDITIONAL: `wfCtx r c`, `d < r.data` | propext, Quot.sound | `Unit 74` — Auxiliary (`A`, [`IsoCollapse.md`](audit/modules/IsoCollapse.md)) |
| `Iso.symm_dmap` | 85 | theorem | FROZEN | propext, Quot.sound | `Unit 74` — Auxiliary (`A`, [`IsoCollapse.md`](audit/modules/IsoCollapse.md)) |
| `Iso.plug_cmap` | 95 | theorem | FROZEN | propext, Quot.sound | `Unit 74` — Auxiliary (`A`, [`IsoCollapse.md`](audit/modules/IsoCollapse.md)) |
| `Iso.wfCtx_cmap` | 107 | theorem | FROZEN | propext, Quot.sound | `Unit 74` — Substantive (`S`) |
| `Iso.derivable_imap` | 125 | theorem | CONDITIONAL: bounds on `i` | propext, Quot.sound | `Unit 74` — Substantive (`S`) |
| `Iso.collapsed_fwd` | 151 | theorem | CONDITIONAL: `d, d' < r.data` | propext, Quot.sound | `Unit 74` — Auxiliary (`A`, [`IsoCollapse.md`](audit/modules/IsoCollapse.md)) |
| `Iso.collapsed_transport` | 164 | theorem | CONDITIONAL: `d, d' < r.data` | propext, Quot.sound | `Unit 74` — Substantive (`S`) |

### 5.41 `IsoCollapseCompat` (`lean4/Derivation/IsoCollapseCompat.lean`) — Parked (`ParkedAudit.lean`) — `Unit 74`

- **Audit appendix:** [`textbook/audit/modules/IsoCollapseCompat.md`](audit/modules/IsoCollapseCompat.md)
- **Auxiliary / omission justification:** All substantive declarations are taught in the unit; auxiliary helpers (`A`) are documented in the audit record.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|

### 5.42 `LadderGeneral` (`lean4/Derivation/LadderGeneral.lean`) — Root-imported — `Unit 60`

- **Audit appendix:** [`textbook/audit/modules/LadderGeneral.md`](audit/modules/LadderGeneral.md)
- **Auxiliary / omission justification:** Recommend omitting: `d2_zero_dims_2_3_4` — its first two conjuncts are vacuous (§11) and the general theorem `BoundaryCancellation.d2_zero_unrestricted` supersedes it; if mentioned, present only its third conjunct as a dimension-4 spot check. Do not present the guard as "the obstruction one dimension up" without saying it is an analogy to `obstP`, not a proved bridge.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `ComplexN` | 51 | structure | ADMITTED (a `Nat`-indexed function treated as data; see §4) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `emptyN` | 54 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `facets` | 57 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `ascB` | 62 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `shellN` | 71 | def | ADMITTED (declared guard / policy) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `shellNLegacy` | 78 | def | ADMITTED (retired policy) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `stepV` | 84 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `stepN` | 89 | def | ADMITTED (declared policy) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `oneVertex` | 140 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `WFComplex` | 155 | def (Prop) | ADMITTED (named invariant) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `NEvent` | 212 | inductive | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `nstep` | 216 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `nreplay` | 220 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `combsAux`, `combs` | 246, 253 | def | ADMITTED (metatheoretic enumeration) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `d4Events` | 256 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `d4Complex` | 263 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `d4MissingEvents` | 284 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `sgn` | 299 | def | ADMITTED (declared sign convention) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `bdN` | 302 | def | ADMITTED (declared) | n/a (definition) | `Unit 60` (Definition / Structure) |
| `pushN` | 306 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `coeffN` | 310 | def | ADMITTED | n/a (definition) | `Unit 60` (Definition / Structure) |
| `uniform_guarded_filler` | 100 | theorem | CONDITIONAL: `shellN C k σ = true` (over all `C`, `k`, `σ`) | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `shell_refuses_general` | 122 | theorem | CONDITIONAL: `shellN = false` | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `shell_no_self_fill` | 130 | theorem | CONDITIONAL: `shellN = true` (near-definitional: the last conjunct of the guard) | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`LadderGeneral.md`](audit/modules/LadderGeneral.md)) |
| `pseudo_cell_countermodel` | 146 | theorem | VERIFIED_FINITE / REFUTED (refutes "the legacy guard admits only well-formed cells") | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `wf_empty` | 158 | theorem | FROZEN | none | `Unit 60` — Auxiliary (`A`, [`LadderGeneral.md`](audit/modules/LadderGeneral.md)) |
| `wf_stepV` | 162 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`LadderGeneral.md`](audit/modules/LadderGeneral.md)) |
| `wf_stepN` | 182 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`LadderGeneral.md`](audit/modules/LadderGeneral.md)) |
| `wf_nstep` | 223 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`LadderGeneral.md`](audit/modules/LadderGeneral.md)) |
| `wf_nreplay` | 233 | theorem | FROZEN | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d4_demo` | 269 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d4_wf` | 279 | theorem | FROZEN-derived instance | propext, Quot.sound | `Unit 60` — Auxiliary (`A`, [`LadderGeneral.md`](audit/modules/LadderGeneral.md)) |
| `d4_guard_load_bearing` | 292 | theorem | VERIFIED_FINITE / REFUTED (refutes "an incomplete 4-shell fills") | propext, Quot.sound | `Unit 60` — Substantive (`S`) |
| `d2_zero_dims_2_3_4` | 318 | theorem | VERIFIED_FINITE (conjunct 3 only; conjuncts 1–2 vacuous) | none | `Unit 60` — Substantive (`S`) |

### 5.43 `LocalStrategy` (`lean4/Derivation/LocalStrategy.lean`) — Parked (`ParkedAudit.lean`) — `Unit 43`

- **Audit appendix:** [`textbook/audit/modules/LocalStrategy.md`](audit/modules/LocalStrategy.md)
- **Auxiliary / omission justification:** Recommend omitting: `presence` as a separate member (it is `bare`); `class_nonvacuity` (a restatement); the `ImportDiscipline` tag from theorem statements — teach it as a label the Lean does not interpret.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `ImportDiscipline` | 21 | inductive | recurring`, a declared tag | n/a (definition) | `Unit 43` (Definition / Structure) |
| `LocalStrategy d` | 28 | structure | ADMITTED (the declared class) | n/a (definition) | `Unit 43` (Definition / Structure) |
| `FiniteDeclaration k S` | 35 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `RecurringImport S` | 39 | def | ADMITTED (reads the tag) | n/a (definition) | `Unit 43` (Definition / Structure) |
| `BaseObstructed n i j` | 44 | structure | ADMITTED (the inherited depth-1 obstruction) | n/a (definition) | `Unit 43` (Definition / Structure) |
| `Fires S` | 51 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `ClearsOn S n` | 56 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `Clears S` | 60 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `IdentityGrade S` | 64 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `OneTimeIdentity S` | 69 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `zeroRadiusStrategy` | 123 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `boolCode`, `profileCode` | 134, 138 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `bare` | 147 | def | ADMITTED (concrete member) | n/a (definition) | `Unit 43` (Definition / Structure) |
| `presence` | 154 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `depthTwo` | 158 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `perPairFreshMark` | 169 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `valued` | 174 | def | ADMITTED | n/a (definition) | `Unit 43` (Definition / Structure) |
| `fires_every_strategy` | 72 | theorem | FROZEN (trivially in `S`) | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `identityGrade_implies_clears` | 78 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `strategy_capacity_collision` | 84 | theorem | CONDITIONAL:`FiniteDeclaration k S`, threshold | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `finite_local_not_clears` | 93 | theorem | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `finite_local_not_identityGrade` | 104 | theorem | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `g1_local_finite_alphabet_class` | 113 | theorem | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `profileCode_lt_eight` | 141 | theorem | VERIFIED_FINITE | none | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `bare_finite` | 177 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `presence_finite` | 181 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `presence_eq_bare` | 183 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `depthTwo_finite` | 185 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `depthTwo_clears_n4` | 191 | theorem | VERIFIED_FINITE (case split + `decide`) | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `perPair_recurring` | 203 | theorem | FROZEN | propext | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `perPair_identityGrade` | 205 | theorem | FROZEN | propext | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `perPair_not_finite` | 209 | theorem | REFUTED (of finiteness; witness `x = k`) | propext | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `valued_oneTimeIdentity` | 214 | theorem | FROZEN | propext | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `valued_not_finite` | 220 | theorem | REFUTED (of finiteness) | propext | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `valued_clears` | 224 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `class_nonvacuity` | 227 | theorem | FROZEN/VERIFIED_FINITE (conjunction of the above) | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `bare_not_identityGrade` | 232 | theorem | REFUTED | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `bare_classification` | 241 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Substantive (`S`) |
| `presence_classification` | 248 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Auxiliary (`A`, [`LocalStrategy.md`](audit/modules/LocalStrategy.md)) |
| `depthTwo_classification` | 255 | theorem | FROZEN | propext, Quot.sound | `Unit 43` — Substantive (`S`) |

### 5.44 `Mention` (`lean4/Derivation/Mention.lean`) — Root-imported — `Unit 12`, `Unit 30`

- **Audit appendix:** [`textbook/audit/modules/Mention.md`](audit/modules/Mention.md)
- **Auxiliary / omission justification:** Omit: the three list helpers.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `mem_plug_of_hole` | 40 | theorem | FROZEN | propext, Quot.sound | `Unit 12`, `Unit 30` — Auxiliary (`A`, [`Mention.md`](audit/modules/Mention.md)) |
| `not_mem_of_arg_out_of_range` | 47 | theorem | CONDITIONAL: instance-argument conjunct of `wf` | none | `Unit 12`, `Unit 30` — Auxiliary (`A`, [`Mention.md`](audit/modules/Mention.md)) |
| `exists_out_of_range_slot` | 56 | theorem | FROZEN | propext | `Unit 12`, `Unit 30` — Auxiliary (`A`, [`Mention.md`](audit/modules/Mention.md)) |
| `collapsed_append_unmentioning` | 88 | theorem | CONDITIONAL: `hd`, `hd'` (non-mention) | propext, Quot.sound | `Unit 12`, `Unit 30` — Substantive (`S`) |
| `collapsed_fresh_datum` | 124 | theorem | CONDITIONAL: instance-argument conjunct of `wf` | propext, Quot.sound | `Unit 12`, `Unit 30` — Substantive (`S`) |
| `getD_append_left` | 157 | theorem | FROZEN | propext | `Unit 12`, `Unit 30` — Auxiliary (`A`, [`Mention.md`](audit/modules/Mention.md)) |
| `collapsed_fresh_form` | 168 | theorem | CONDITIONAL: instance-form and rule conjuncts of `wf` | propext | `Unit 12`, `Unit 30` — Substantive (`S`) |

### 5.45 `Minimality` (`lean4/Derivation/Minimality.lean`) — Root-imported — `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22`

- **Audit appendix:** [`textbook/audit/modules/Minimality.md`](audit/modules/Minimality.md)
- **Auxiliary / omission justification:** Omit: `U1_separable`/`deltaU1_valid` as displayed results (mention as the swapped twin); `applyDelta_single/pair`.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `aritySum` | 15 | def | ADMITTED (declared cost measure) | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `U0`, `U1` | 38, 40 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `BL`, `BD` | 42, 44 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `deltaU0`, `deltaU1`, `deltaBL`, `deltaBD` | 60–63 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `sortPair` | 169 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `Iso r s` | 176 | structure (Type-valued) | ADMITTED (declared isomorphism; docstring: "Mirrors `code/derivation/iso.py`") | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `isoRefl` | 199 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `swap01` | 223 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `isoU1U0` | 227 | def | ADMITTED (data; VERIFIED_FINITE fields) | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `markK k` | 297 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `deltaK k` | 300 | def | ADMITTED | n/a (definition) | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` (Definition / Structure) |
| `applyDelta_single` | 21 | theorem | FROZEN | not in artifact | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `applyDelta_pair` | 27 | theorem | FROZEN | not in artifact | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `U0_separable` | 46 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `U1_separable` | 49 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `BL_separable` | 52 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `BD_separable` | 55 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `validResponse_R2L` | 67 | theorem | FROZEN (instance over `R2L`, general in `δ`, `s`) | not in artifact | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `deltaU0_valid` … `deltaBD_valid` | 79–89 | theorem | VERIFIED_FINITE (application by `decide`) | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `no_insts_no_separation` | 94 | theorem | CONDITIONAL: `insts = []` | not in artifact | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `cost1_insufficient_general` | 102 | theorem | CONDITIONAL: `forms = []`, `insts = []` (general over the whole item grammar and all regimes of that shape) | propext | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `cost1_insufficient` | 144 | theorem | FROZEN (instance) | propext | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `cost1_insufficient_F` | 149 | theorem | FROZEN (instance) | propext | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `deltaU0F_valid` | 155 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `U0_not_iso_BL` | 250 | theorem | REFUTED (over all `Iso` structures; symbolic proof, not `decide`) | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `U0_not_iso_BD` | 259 | theorem | REFUTED | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `BL_not_iso_BD` | 270 | theorem | REFUTED | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `mu1_minimum_not_unique` | 284 | theorem | REFUTED (refutes uniqueness of the `mu1` minimum, reading L, up to the declared `Iso`); components VERIFIED_FINITE + `cost1_insufficient` + `U0_not_iso_BL` | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `deltaK_applies` | 303 | theorem | CONDITIONAL: `1 ≤ k` | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `markK_separable` | 325 | theorem | CONDITIONAL: `1 ≤ k` | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `deltaK_valid` | 346 | theorem | CONDITIONAL: `1 ≤ k` | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `deltaK_length` | 351 | theorem | FROZEN | none | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `markK_pairwise_noniso` | 355 | theorem | REFUTED (general in `j`, `k`) | propext | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `mu2_unique` | 371 | theorem | FROZEN (general over the item grammar; the hypotheses `hval`, `har` are the claim's scope: reading L, two items, `mu2` second component ≤ 1) | propext, Quot.sound | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Substantive (`S`) |
| `deltaU1_valid` | (grouped in [`Minimality.md`](audit/modules/Minimality.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |
| `deltaBL_valid` | (grouped in [`Minimality.md`](audit/modules/Minimality.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 18`, `Unit 19`, `Unit 20`, `Unit 21`, `Unit 22` — Auxiliary (`A`, [`Minimality.md`](audit/modules/Minimality.md)) |

### 5.46 `MinimalityF` (`lean4/Derivation/MinimalityF.lean`) — Root-imported — `Unit 32`

- **Audit appendix:** [`textbook/audit/modules/MinimalityF.md`](audit/modules/MinimalityF.md)
- **Auxiliary / omission justification:** Omit: nothing beyond folding the definitions into one sentence.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `U0F` | 37 | def | ADMITTED | n/a (definition) | `Unit 32` (Definition / Structure) |
| `U2F` | 40 | def | ADMITTED | n/a (definition) | `Unit 32` (Definition / Structure) |
| `swap12` | 43 | def | ADMITTED | n/a (definition) | `Unit 32` (Definition / Structure) |
| `isoU2F_U0F` | 47 | def (Type-valued) | ADMITTED (VERIFIED_FINITE fields) | n/a (definition) | `Unit 32` (Definition / Structure) |
| `genesis_mark_not_separable` | 72 | theorem | FROZEN (instance: `collapsed_of_no_insts` + `collapsed_append_unmentioning`, non-mention side conditions by `decide`) | propext, Quot.sound | `Unit 32` — Substantive (`S`) |
| `mu2_unique_F` | 86 | theorem | FROZEN (general over the item grammar; hypotheses `hval`, `har` are the claim's scope) | propext, Quot.sound | `Unit 32` — Substantive (`S`) |

### 5.47 `NoOutside` (`lean4/Derivation/NoOutside.lean`) — Root-imported — `Unit 47`

- **Audit appendix:** [`textbook/audit/modules/NoOutside.md`](audit/modules/NoOutside.md)
- **Auxiliary / omission justification:** Omit: `replayC_deterministic` (no content); present `equivariant_family_invariant` as a one-line remark if at all.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| CWorld | 125 | structure | ADMITTED (conservative extension) | n/a (definition) | `Unit 47` (Definition / Structure) |
| CEvent | 130 | inductive | ADMITTED (extended event grammar) | n/a (definition) | `Unit 47` (Definition / Structure) |
| stepC | 135 | def | ADMITTED | n/a (definition) | `Unit 47` (Definition / Structure) |
| replayC | 141 | def | ADMITTED | n/a (definition) | `Unit 47` (Definition / Structure) |
| certPosC / certNegC | 160 / 163 | def | ADMITTED | n/a (definition) | `Unit 47` (Definition / Structure) |
| PanelEquiv | 174 | def | ADMITTED (the declared joint quotient) | n/a (definition) | `Unit 47` (Definition / Structure) |
| support_replay | 32 | theorem | FROZEN | propext, Quot.sound | `Unit 47` — Substantive (`S`) |
| support_repairFamily | 43 | theorem | FROZEN | propext, Quot.sound | `Unit 47` — Auxiliary (`A`, [`NoOutside.md`](audit/modules/NoOutside.md)) |
| support_quiescent | 56 | theorem | FROZEN | propext, Quot.sound | `Unit 47` — Auxiliary (`A`, [`NoOutside.md`](audit/modules/NoOutside.md)) |
| support_obstructed | 68 | theorem | FROZEN | propext, Quot.sound | `Unit 47` — Auxiliary (`A`, [`NoOutside.md`](audit/modules/NoOutside.md)) |
| effectual_outside_dichotomy | 91 | theorem | FROZEN | propext, Quot.sound | `Unit 47` — Substantive (`S`) |
| equivariant_family_invariant | 108 | theorem | FROZEN (pure metatheory; two-line calc) | none | `Unit 47` — Auxiliary (`A`, [`NoOutside.md`](audit/modules/NoOutside.md)) |
| stepC_conservative | 146 | theorem | FROZEN (definitional) | propext, Quot.sound | `Unit 47` — Substantive (`S`) |
| admitEvaluator_base_inert | 153 | theorem | FROZEN | propext, Quot.sound | `Unit 47` — Substantive (`S`) |
| replayC_deterministic | 167 | theorem | FROZEN (trivially true conclusion) | propext, Quot.sound | `Unit 47` — Auxiliary (`A`, [`NoOutside.md`](audit/modules/NoOutside.md)) |
| panel_equiv | 177 | theorem | FROZEN | none | `Unit 47` — Substantive (`S`) |
| certNeg_iff_panelEquiv | 190 | theorem | FROZEN | propext, Quot.sound | `Unit 47` — Substantive (`S`) |
| certC_ceiling | 266 | theorem | VERIFIED_FINITE / REFUTED (refutes certification = correspondence in the integrated kernel) | propext, Quot.sound | `Unit 47` — Substantive (`S`) |
| `transports;` | (grouped in [`NoOutside.md`](audit/modules/NoOutside.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 47` — Auxiliary (`A`, [`NoOutside.md`](audit/modules/NoOutside.md)) |

### 5.48 `NoOutsideFidelity` (`lean4/Derivation/NoOutsideFidelity.lean`) — Root-imported — `Unit 72`

- **Audit appendix:** [`textbook/audit/modules/NoOutsideFidelity.md`](audit/modules/NoOutsideFidelity.md)
- **Auxiliary / omission justification:** Recommend omitting: `no_support_inverse_faithfully_erases_index` (identical content to the `∀` form).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `supportTranslationPair backward` | 48 | def | ADMITTED (`backward` is a universally quantified parameter) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `supportTotalization backward` | 53 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `support_fiber_contains_distinct_notes` | 30 | theorem | VERIFIED_FINITE (concrete witness; `decide` on `[] ≠ [0]`) | propext | `Unit 72` — Substantive (`S`) |
| `support_projection_not_injective` | 40 | theorem | FROZEN (follows from the finite witness; the statement is about the whole function) | propext | `Unit 72` — Substantive (`S`) |
| `support_translation_never_round_trip_coherent` | 62 | theorem | FROZEN (universal over `backward`; uses only the `left` triangle) | propext | `Unit 72` — Substantive (`S`) |
| `support_translation_never_faithfully_erases_index` | 75 | theorem | FROZEN | propext | `Unit 72` — Substantive (`S`) |
| `no_support_inverse_faithfully_erases_index` | 83 | theorem | FROZEN (restatement) | propext | `Unit 72` — Auxiliary (`A`, [`NoOutsideFidelity.md`](audit/modules/NoOutsideFidelity.md)) |
| `notes_fiber_has_no_operational_authority` | 92 | theorem | FROZEN (alias of `PresentationRelativity.notes_update_kernel_results_agree`, itself an instance of `NoOutside.effectual_outside_dichotomy`) | propext, Quot.sound | `Unit 72` — Substantive (`S`) |

### 5.49 `ObsDescent` (`lean4/Derivation/ObsDescent.lean`) — Root-imported — `Unit 67`

- **Audit appendix:** [`textbook/audit/modules/ObsDescent.md`](audit/modules/ObsDescent.md)
- **Auxiliary / omission justification:** Omit: the five `int_*` arithmetic lemmas and `int_shift_cancel` (they exist to subsume an external tail and teach nothing about Genesis); `tag_view_zeroRel` (an `Iff.rfl`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| ClassConstant | 104 | def | ADMITTED | n/a (definition) | `Unit 67` (Definition / Structure) |
| descend | 108 | def | ADMITTED | n/a (definition) | `Unit 67` (Definition / Structure) |
| DeltaConstant | 151 | def | ADMITTED | n/a (definition) | `Unit 67` (Definition / Structure) |
| deltaDescend | 156 | def | ADMITTED | n/a (definition) | `Unit 67` (Definition / Structure) |
| coarsenMap | 261 | def | ADMITTED | n/a (definition) | `Unit 67` (Definition / Structure) |
| pairSetoid | 318 | def | ADMITTED | n/a (definition) | `Unit 67` (Definition / Structure) |
| intDiffObs | 359 | def (DiffObs Int Int) | ADMITTED instance; laws PROVED by arithmetic, not by `kernelObs` — **not a kernel observer** | n/a (definition) | `Unit 67` (Definition / Structure) |
| collapseAllObs | 437 | def (DiffObs Bool Bool) | ADMITTED instance (countermodel); laws trivially PROVED — **not a kernel observer** | n/a (definition) | `Unit 67` (Definition / Structure) |
| obsQuotient_exact | 83 | theorem | FROZEN | propext | `Unit 67` — Substantive (`S`) |
| obsQuotient_mk_eq_iff | 88 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Substantive (`S`) |
| obsQuotient_mk_surjective | 96 | theorem | FROZEN | none | `Unit 67` — Substantive (`S`) |
| descend_mk | 113 | theorem | FROZEN | none | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| descend_exists_iff | 119 | theorem | FROZEN | Quot.sound | `Unit 67` — Substantive (`S`) |
| descend_unique | 134 | theorem | FROZEN | Quot.sound | `Unit 67` — Substantive (`S`) |
| descend_blocked_of_witness | 142 | theorem | REFUTED (of descent, given a witness) | Quot.sound | `Unit 67` — Substantive (`S`) |
| deltaDescend_mk | 161 | theorem | FROZEN | none | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| deltaDescend_exists_iff | 169 | theorem | FROZEN | Quot.sound | `Unit 67` — Substantive (`S`) |
| deltaDescend_unique | 188 | theorem | FROZEN | Quot.sound | `Unit 67` — Substantive (`S`) |
| deltaDescend_blocked_of_witness | 200 | theorem | REFUTED (of descent, given witnesses) | Quot.sound | `Unit 67` — Substantive (`S`) |
| classConstant_pair_iff | 212 | theorem | FROZEN | none | `Unit 67` — Substantive (`S`) |
| pair_descend_exists_iff | 225 | theorem | FROZEN | Quot.sound | `Unit 67` — Substantive (`S`) |
| view_descends_pair_blocked | 248 | theorem | CONDITIONAL: ClassConstant O f, ZeroRel O x y, g x ≠ g y | Quot.sound | `Unit 67` — Substantive (`S`) |
| coarsenMap_mk | 267 | theorem | FROZEN | Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| classConstant_comp_mk_iff | 276 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Substantive (`S`) |
| descendMod_exists_iff | 284 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| deltaDescendMod_exists_iff | 293 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| pairSetoid_mk_eq_iff | 327 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| descendMod_exists_of_coarsen | 334 | theorem | FROZEN | Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| tag_view_zeroRel | 350 | theorem | FROZEN (definitional) | none | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| intDiffObs_zeroRel | 374 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| int_sub_ne_zero_iff | 385 | theorem | FROZEN (integer arithmetic) | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| int_sub_ne_zero_of_gt | 393 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| int_shift_cancel | 398 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| int_two_mul_eq_zero_iff | 403 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| int_add_sub_cancel | 411 | theorem | FROZEN | propext, Quot.sound | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| value_orientation_survives | 417 | theorem | VERIFIED_FINITE (two integers) | propext, Quot.sound | `Unit 67` — Substantive (`S`) |
| collapseAllObs_all_zero | 445 | theorem | FROZEN (trivially true by definition of `Zero`) | none | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| collapseAllObs_not_deltaConstant | 452 | theorem | REFUTED | none | `Unit 67` — Substantive (`S`) |
| collapseAllObs_no_delta_descend | 458 | theorem | REFUTED | Quot.sound | `Unit 67` — Substantive (`S`) |
| collapseAllObs_id_not_classConstant | 469 | theorem | REFUTED | none | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |
| collapseAllObs_no_view_descend | 476 | theorem | REFUTED | Quot.sound | `Unit 67` — Substantive (`S`) |
| classConstant_iff_fiberConstant_all | 494 | theorem | FROZEN | none | `Unit 67` — Substantive (`S`) |
| descend_iff_factorsOn_all | 507 | theorem | FROZEN | Quot.sound | `Unit 67` — Substantive (`S`) |
| fiberConstant_fixed_D_not_classConstant | 523 | theorem | REFUTED (of removing `∀ D`) | none | `Unit 67` — Substantive (`S`) |
| sigEq_append_iff | 532 | theorem | FROZEN | propext | `Unit 67` — Auxiliary (`A`, [`ObsDescent.md`](audit/modules/ObsDescent.md)) |

### 5.50 `ObserverInventory` (`lean4/Derivation/ObserverInventory.lean`) — Root-imported — `Unit 37`

- **Audit appendix:** [`textbook/audit/modules/ObserverInventory.md`](audit/modules/ObserverInventory.md)
- **Auxiliary / omission justification:** Recommend omitting: `Slot`/`slotList`/`slot_count`/`slots_nodup` as theorems (they only pin a list of names; mention the nine names in prose and the author's refusal note), and `closure_empty_family_is_identity` (a one-line specialisation of `PrimDiff.clos_empty_id`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Slot` | 43 | inductive | ADMITTED (declared classification) | n/a (definition) | `Unit 37` (Definition / Structure) |
| `slotList` | 48 | def | ADMITTED | n/a (definition) | `Unit 37` (Definition / Structure) |
| `EmptyRel` | 58 | def | ADMITTED | n/a (definition) | `Unit 37` (Definition / Structure) |
| (instance) | 60 | instance | ADMITTED (auxiliary) | n/a (definition) | `Unit 37` (Definition / Structure) |
| `zeroW` | 115 | def | ADMITTED | n/a (definition) | `Unit 37` (Definition / Structure) |
| `oneW` | 117 | def | ADMITTED | n/a (definition) | `Unit 37` (Definition / Structure) |
| `pushNot` | 151 | def | ADMITTED | n/a (definition) | `Unit 37` (Definition / Structure) |
| `edgeCount` | 204 | def | ADMITTED | n/a (definition) | `Unit 37` (Definition / Structure) |
| `isSymBit` | 208 | def | ADMITTED | n/a (definition) | `Unit 37` (Definition / Structure) |
| `slot_count` | 52 | theorem | VERIFIED_FINITE (`rfl`) | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `slots_nodup` | 54 | theorem | VERIFIED_FINITE (`decide`) | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `empty_irrefl` | 63 | theorem | VERIFIED_FINITE | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `empty_ne_D2` | 66 | theorem | VERIFIED_FINITE | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `bool_irrefl_full_classification` | 74 | theorem | CONDITIONAL:`[∀ x y, Decidable (r x y)]`, `Irrefl r` | propext, Quot.sound | `Unit 37` — Substantive (`S`) |
| `witnesses_are_data` | 124 | theorem | VERIFIED_FINITE | propext | `Unit 37` — Substantive (`S`) |
| `collision_is_not_obstruction` | 145 | theorem | REFUTED (countermodel to fusing the two defect readings) | none | `Unit 37` — Substantive (`S`) |
| `transpose_involutive` | 154 | theorem | FROZEN (`rfl`) | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `transpose_D2_eq_D2rev` | 157 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `transpose_D2rev_eq_D2` | 166 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `pushNot_D2_eq_D2rev` | 175 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `transpose_eq_pushNot_on_D2` | 180 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 37` — Substantive (`S`) |
| `transpose_ne_pushNot` | 185 | theorem | REFUTED (countermodel to "the two reversal maps are one operation") | none | `Unit 37` — Substantive (`S`) |
| `closure_empty_family_is_identity` | 198 | theorem | VERIFIED_FINITE (specialisation of a FROZEN lemma) | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `residuals_not_unique` | 212 | theorem | VERIFIED_FINITE (`decide`) | none | `Unit 37` — Substantive (`S`) |
| `swap_not_auto_of_D2` | 220 | theorem | VERIFIED_FINITE | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |
| `swap_not_auto_of_D2rev` | 227 | theorem | VERIFIED_FINITE (`decide`) | none | `Unit 37` — Auxiliary (`A`, [`ObserverInventory.md`](audit/modules/ObserverInventory.md)) |

### 5.51 `Pigeonhole` (`lean4/Derivation/Pigeonhole.lean`) — Root-imported — `Unit 42`

- **Audit appendix:** [`textbook/audit/modules/Pigeonhole.md`](audit/modules/Pigeonhole.md)
- **Auxiliary / omission justification:** Recommend omitting: everything but the two substantive statements and a one-paragraph note on the `ReflBEq Nat` trap; the module is apparatus.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `upto` | 173 | def | ADMITTED | n/a (definition) | `Unit 42` (Definition / Structure) |
| `nodup_head` | 51 | theorem | FROZEN | not in artifact | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `nodup_tail` | 56 | theorem | FROZEN | not in artifact | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `length_filter_split` | 63 | theorem | FROZEN | propext, Quot.sound | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `filter_eq_nil_of_none` | 81 | theorem | FROZEN | not in artifact | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `filter_nodup` | 92 | theorem | FROZEN | propext | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `nodup_filter_eq_le_one` | 113 | theorem | FROZEN | propext | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `nodup_length_le` | 141 | theorem | FROZEN | propext, Quot.sound | `Unit 42` — Substantive (`S`) |
| `upto_length` | 177 | theorem | FROZEN | none | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `upto_mem` | 183 | theorem | FROZEN | propext, Quot.sound | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `map_nodup_of_inj` | 193 | theorem | FROZEN | propext, Quot.sound | `Unit 42` — Auxiliary (`A`, [`Pigeonhole.md`](audit/modules/Pigeonhole.md)) |
| `pigeonhole` | 215 | theorem | FROZEN | propext, Quot.sound | `Unit 42` — Substantive (`S`) |

### 5.52 `PresentationDescent` (`lean4/Derivation/PresentationDescent.lean`) — Root-imported — `Unit 72`

- **Audit appendix:** [`textbook/audit/modules/PresentationDescent.md`](audit/modules/PresentationDescent.md)
- **Auxiliary / omission justification:** Recommend omitting: `CoincidentImages` as a taught notion (it is a derived property retained only to block the "coproduct is a descent" misreading; one sentence suffices).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `TranslationAttempt P Q` | 39 | structure | ADMITTED (supplied arrows) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `Totalization t` | 46 | structure | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `TranslationGap t` | 54 | inductive | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `RoundTripCoherent u` | 80 | structure (Prop) | ADMITTED (the declared coherence 2-cell) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `CoherenceResidual u` | 87 | inductive (Type) | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `coherent_to_bij h` | 104 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `CoincidentImages left right` | 117 | def | ADMITTED | n/a (definition) | `Unit 72` (Definition / Structure) |
| `FaithfulCommonDescent u` | 126 | structure (Type 1) | ADMITTED (the declared notion of "faithful descent"; its `Carrier : Type` field is metatheoretic existential output — see §4) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `coherent_to_faithful_descent h` | 156 | def | ADMITTED (one witness; docstring disclaims preference) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `translation_gap_refuses_totalization` | 60 | theorem | FROZEN | propext | `Unit 72` — Substantive (`S`) |
| `coherence_residual_refutes_round_trip` | 93 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`PresentationDescent.md`](audit/modules/PresentationDescent.md)) |
| `faithful_common_descent_has_coincident_images` | 138 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`PresentationDescent.md`](audit/modules/PresentationDescent.md)) |
| `faithful_descent_to_coherent` | 176 | theorem | FROZEN | none | `Unit 72` — Substantive (`S`) |
| `faithful_descent_iff_round_trip_coherent` | 196 | theorem | FROZEN | none | `Unit 72` — Substantive (`S`) |
| `incoherence_forces_index_retention` | 212 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`PresentationDescent.md`](audit/modules/PresentationDescent.md)) |
| `residual_forces_index_retention` | 221 | theorem | FROZEN | none | `Unit 72` — Substantive (`S`) |

### 5.53 `PresentationNaturality` (`lean4/Derivation/PresentationNaturality.lean`) — Root-imported — `Unit 70`

- **Audit appendix:** [`textbook/audit/modules/PresentationNaturality.md`](audit/modules/PresentationNaturality.md)
- **Auxiliary / omission justification:** Recommend omitting: `Viable` (unused); `Family` (the flat version, retained in Lean for historical reasons but superseded for teaching by `HFamily`, with a note that `hAuto_iff_auto` only bridges one object); `twoFamilyPos_has_section` and `card4_has_natural_section` as separate items (restatements).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Bij A B` | 82 | structure | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Bij.rfl'` | 88 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Bij.symm` | 94 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Bij.trans` | 100 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `PresIso O O'` | 118 | structure | ADMITTED (the notion of "presentation isomorphism" is declared here, not derived) | n/a (definition) | `Unit 70` (Definition / Structure) |
| `PresIso.refl` | 140 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `PresIso.symm` | 146 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `PresIso.trans` | 162 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Viable X R` | 196 | structure | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `PresIso.mapPair` | 204 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Family X R` | 222 | structure | ADMITTED (declared family) | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Sec D` | 232 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `IsNatural D s` | 236 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `autoFamily O F` | 242 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `notBij` | 293 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `negIso` | 301 | def | ADMITTED (fixture) | n/a (definition) | `Unit 70` (Definition / Structure) |
| `boolEqPair` | 325 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `boolEqRawSection` | 328 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Card4` | 349 | inductive | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `tw` | 354 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twBij` | 363 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `card4Obs` | 371 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twPairBij` | 373 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twIso` | 388 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `card4Pair` | 399 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `card4Section` | 402 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `HFamily` | 497 | structure | ADMITTED (declared family) | n/a (definition) | `Unit 70` (Definition / Structure) |
| `HSec D` | 505 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `HIsNatural D s` | 507 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `hAutoFamily O F` | 525 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Two` | 556 | inductive | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twoCar`, `twoRes`, `twoObs` | 560, 564, 568 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twoHom` | 573 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twoIsoNeg` | 579 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twoFamilyNeg` | 585 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twoIsoPos` | 601 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twoFamilyPos` | 607 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `twoSectionPos` | 615 | def | ADMITTED | n/a (definition) | `Unit 70` (Definition / Structure) |
| `Bij.fwd_injective` | 108 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `zeroRel_transport` | 128 | theorem | FROZEN | none | `Unit 70` — Substantive (`S`) |
| `refl_car` | 174 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `trans_car` | 177 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `symm_car_left` | 181 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `symm_car_right` | 185 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `symm_symm_car` | 189 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `viable_transport` | 211 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `no_natural_section_of_fixed_point_free` | 272 | theorem | FROZEN (near-definitional: see §11) | none | `Unit 70` — Substantive (`S`) |
| `fixed_pair_of_natural_section` | 282 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `negIso_fixed_point_free` | 309 | theorem | VERIFIED_FINITE (`decide` on `Bool`) | none | `Unit 70` — Substantive (`S`) |
| `no_natural_section_boolEq` | 318 | theorem | VERIFIED_FINITE (instance of the general theorem at a concrete observer) | none | `Unit 70` — Substantive (`S`) |
| `selection_is_possible_naturality_is_not` | 335 | theorem | VERIFIED_FINITE | none | `Unit 70` — Substantive (`S`) |
| `tw_involutive` | 360 | theorem | VERIFIED_FINITE | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `card4_natural_section` | 409 | theorem | VERIFIED_FINITE | none | `Unit 70` — Substantive (`S`) |
| `card4_has_natural_section` | 417 | theorem | VERIFIED_FINITE | none | `Unit 70` — Substantive (`S`) |
| `naturality_separates_presentations` | 427 | theorem | VERIFIED_FINITE | none | `Unit 70` — Substantive (`S`) |
| `bool_obstruction_and_sealed_selector` | 446 | theorem | VERIFIED_FINITE (co-statement) | Quot.sound (inherited from `swapObs_boolEqObs`'s `funext`) | `Unit 70` — Substantive (`S`) |
| `mapPair_refl` | 462 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `mapPair_trans` | 467 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `mapPair_symm_left` | 474 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `mapPair_symm_right` | 481 | theorem | FROZEN | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `no_natural_section_of_endo` | 517 | theorem | FROZEN | none | `Unit 70` — Substantive (`S`) |
| `hAuto_iff_auto` | 538 | theorem | FROZEN (one-object only, by construction of both sides) | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `twIso_fixes_card4Pair` | 619 | theorem | VERIFIED_FINITE | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `twoFamilyNeg_no_section` | 597 | theorem | VERIFIED_FINITE | none | `Unit 70` — Substantive (`S`) |
| `twoFamilyPos_natural` | 627 | theorem | VERIFIED_FINITE | none | `Unit 70` — Substantive (`S`) |
| `twoFamilyPos_has_section` | 635 | theorem | VERIFIED_FINITE | none | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |
| `heterogeneous_naturality_separates` | 643 | theorem | VERIFIED_FINITE | none | `Unit 70` — Substantive (`S`) |
| `stands` | (grouped in [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 70` — Auxiliary (`A`, [`PresentationNaturality.md`](audit/modules/PresentationNaturality.md)) |

### 5.54 `PresentationRelativity` (`lean4/Derivation/PresentationRelativity.lean`) — Root-imported — `Unit 71`

- **Audit appendix:** [`textbook/audit/modules/PresentationRelativity.md`](audit/modules/PresentationRelativity.md)
- **Auxiliary / omission justification:** Recommend omitting from the textbook: `encodeDepthOneProfile_injective` (a 64-case coding lemma); `world_eq_iff_support_eq_and_notes_eq` (schema extensionality, better stated in prose); `declared_generator_profiles_disagree_at_pair` (a restatement of two Generator theorems).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `FiberIdentityOn D p q` | 62 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `PresentationIdentityOn D p q` | 68 | def | ADMITTED (declared notion of relative identity) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `DirectionalResidual D p q` | 91 | structure | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `ResidualEmptyOn D p q` | 113 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `IdentityRelativeToQuestions D Q p` | 179 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `DirectionalResidualAt D p q x` | 200 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `jointPresentation D p q` | 327 | def | ADMITTED (a declared construction; docstring disclaims naturality) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `ViewIdentifies view x y` | 382 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `ViewSeparates view x y` | 385 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `Metatheory.AllViewsIdentify x y` | 394 | def | ADMITTED (fenced diagnostic) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `supportNotesView w` | 427 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `coarsePanel` | 522 | def | ADMITTED (fixture) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `separatingEvaluator` | 524 | def | ADMITTED (fixture) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `sourcePanelWorld w` | 526 | def | ADMITTED (fixture) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `extendedPanelWorld w` | 529 | def | ADMITTED (fixture) | n/a (definition) | `Unit 71` (Definition / Structure) |
| `boolBit` | 547 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `encodeDepthOneProfile` | 553 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `depthOnePresentation s i` | 565 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `generatorDomain n` | 574 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `presentationIdentity_iff_fiberIdentity` | 71 | theorem | FROZEN | Quot.sound | `Unit 71` — Substantive (`S`) |
| `directionalResidual_refutes_identity` | 100 | theorem | FROZEN | Quot.sound | `Unit 71` — Substantive (`S`) |
| `presentationIdentity_iff_residualEmpty` | 117 | theorem | FROZEN | Quot.sound | `Unit 71` — Substantive (`S`) |
| `presentationIdentity_equivalence` | 146 | theorem | FROZEN | Quot.sound | `Unit 71` — Substantive (`S`) |
| `self_comparison_has_empty_residual` | 169 | theorem | FROZEN | Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `identityRelativeToQuestions_iff` | 183 | theorem | FROZEN | Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `splitsAt_iff_directionalResidualAt` | 207 | theorem | FROZEN | Quot.sound | `Unit 71` — Substantive (`S`) |
| `family_enlargement_refines` | 225 | theorem | CONDITIONAL: `hsub : ∀ q ∈ Q, q ∈ Q'` | Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `family_split_refuses_relative_identity` | 239 | theorem | CONDITIONAL: a witnessed split | Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `family_enlargement_split_is_strict` | 251 | theorem | CONDITIONAL: `hsub`, `hs` | Quot.sound | `Unit 71` — Substantive (`S`) |
| `classCount_lt_of_refinement_split` | 265 | theorem | CONDITIONAL: `FactorsOn D r p` and a split pair | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `forced_split_of_factorization_failure` | 290 | theorem | CONDITIONAL: `¬ FactorsOn D p q` (the comparison `q` is supplied) | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `jointPresentation_factors_left` | 332 | theorem | FROZEN | propext, Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `jointPresentation_factors_right` | 342 | theorem | FROZEN | propext, Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `jointPresentation_strict_of_factorization_failure` | 356 | theorem | CONDITIONAL: `¬ FactorsOn D p q` | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `directionalResidual_of_factorization_failure` | 372 | theorem | CONDITIONAL: `¬ FactorsOn D p q` | propext, Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `Metatheory.attempted_absolute_identification_collapses_to_equality` | 399 | theorem | FROZEN (metatheoretic diagnostic; see §4) | none | `Unit 71` — Substantive (`S`) |
| `Metatheory.attempted_absolute_polarities_are_refuted` | 413 | theorem | CONDITIONAL: `x ≠ y` (metatheoretic diagnostic) | none | `Unit 71` — Substantive (`S`) |
| `world_eq_iff_support_eq_and_notes_eq` | 433 | theorem | FROZEN (schema-relative) | propext | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `supportNotesView_injective` | 446 | theorem | FROZEN | propext | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `support_identifies_while_supportNotes_separates` | 455 | theorem | CONDITIONAL: the two hypotheses (immediate) | none | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `notes_update_kernel_results_agree` | 466 | theorem | FROZEN (instance of `effectual_outside_dichotomy`) | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `panelEquiv_antitone` | 484 | theorem | CONDITIONAL: `hsub` | none | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `panel_members_preserved_by_extension` | 493 | theorem | FROZEN | propext, Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `panel_extension_refines_equivalence` | 503 | theorem | FROZEN | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `certNeg_extension_implies_source` | 512 | theorem | CONDITIONAL: `cw.panel ≠ []` | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `panel_extension_changes_verdict_not_world` | 536 | theorem | VERIFIED_FINITE (fixed panel, `simp` evaluation; universally quantified over `w` but `w` is inert) | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `encodeDepthOneProfile_injective` | 556 | theorem | VERIFIED_FINITE | propext | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `depthOnePresentation_eq_iff` | 568 | theorem | FROZEN | propext, Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `declared_generator_index_comparison_does_not_factor` | 582 | theorem | CONDITIONAL: `3 ≤ n` | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `declared_generator_index_comparison_forces_refinement` | 607 | theorem | CONDITIONAL: `3 ≤ n`; `id` is the supplied comparison | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `declared_generator_profiles_disagree_at_pair` | 630 | theorem | CONDITIONAL: `3 ≤ n` | propext, Quot.sound | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `constructs` | (grouped in [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |
| `selects` | (grouped in [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 71` — Auxiliary (`A`, [`PresentationRelativity.md`](audit/modules/PresentationRelativity.md)) |

### 5.55 `PrimDiff` (`lean4/Derivation/PrimDiff.lean`) — Root-imported — `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25`

- **Audit appendix:** [`textbook/audit/modules/PrimDiff.md`](audit/modules/PrimDiff.md)
- **Auxiliary / omission justification:** Recommend omitting: `one_point_hosts_bare_witness` and `collapse_unobstructed_without_fidelity` (verbatim aliases of `selfdiff_consistent`; teach the one countermodel under one name), `const_presentation_unfaithful` (its statement is the hypothesis `Irrefl r'` at `v`; teach the idea in prose), `repetition_*` (generic list facts), `sym_D2_eq_S2` (`rfl`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Irrefl` | 28 | def | ADMITTED (the one object-level law compared against none and symmetry) | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `Sym` | 31 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `Transpose` | 35 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `D2` | 89 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `D2rev` | 92 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `S2` | 95 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| (instances) | 97, 100, 103 | instance | ADMITTED (auxiliary) | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `Push` | 165 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `CollapseCollision` | 174 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `FidelityObstruction` | 181 | def | ADMITTED (declared policy: obstruction is *relative to a chosen `P`*) | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `Clos` | 491 | inductive | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `Irred` | 498 | def | ADMITTED | n/a (definition) | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` (Definition / Structure) |
| `irrefl_witness_ne` | 42 | theorem | CONDITIONAL:`Irrefl r` | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `selfdiff_consistent` | 48 | theorem | REFUTED (countermodel to A1 → A3, A1 → A1i) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `symm_selfdiff_consistent` | 55 | theorem | REFUTED (countermodel to "symmetry restores soundness") | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `meta_diff_without_assertion` | 63 | theorem | REFUTED (countermodel to A3 → A1) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `factors_through_point_iff` | 72 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `no_witness_on_subsingleton` | 84 | theorem | CONDITIONAL:`Irrefl r`, `[Subsingleton α]` | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `D2_irrefl` | 106 | theorem | VERIFIED_FINITE (concrete, case split on `Bool`) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `S2_irrefl` | 112 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `D2_witness` | 118 | theorem | VERIFIED_FINITE (`decide`) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `D2_initial_pointed` | 123 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `one_point_hosts_bare_witness` | 143 | theorem | REFUTED (alias) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `witnessed_irrefl_on_every_larger_carrier` | 149 | theorem | FROZEN (∀ n in the metatheory) | propext, Quot.sound | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `push_witness` | 188 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `collision_of_identifying_witness` | 194 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `collision_not_irrefl` | 199 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `bare_collapse_admissible` | 209 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `collapse_unobstructed_without_fidelity` | 217 | theorem | REFUTED (alias; see §11) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `obstruction_under_irrefl` | 223 | theorem | FROZEN (conditional only on a witnessed pair and its collision) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `collision_transpose_invariant` | 232 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `orientation_data_invisible_to_collapse` | 245 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `bool_irrefl_witness_classification` | 265 | theorem | CONDITIONAL:`[∀ x y, Decidable (r x y)]`, `Irrefl r`, `r false true` | propext, Quot.sound | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `D2_not_pointed_iso_S2` | 288 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `D2_S2_collapse_equiv` | 299 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `symmetric_no_equivariant_classifier` | 315 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `swap_is_S2_automorphism` | 322 | theorem | VERIFIED_FINITE (`decide`) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `oriented_rigid` | 328 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `oriented_classifier_exists` | 338 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `swap_carries_D2_to_D2rev` | 353 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `swap_twice_restores_D2` | 357 | theorem | VERIFIED_FINITE | propext | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `swap_twice_restores_D2rev` | 363 | theorem | VERIFIED_FINITE | propext | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `sym_D2_eq_S2` | 370 | theorem | VERIFIED_FINITE (definitional) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `sym_D2rev_eq_S2` | 373 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `swap_auto_of_S2_not_of_D2` | 379 | theorem | VERIFIED_FINITE | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `bool_irrefl_nonempty_classification` | 392 | theorem | CONDITIONAL:`[∀ x y, Decidable (r x y)]`, `Irrefl r`, `∃ x y, r x y` | propext, Quot.sound | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `single_oriented_witness_consistent` | 433 | theorem | REFUTED (countermodel to "two witnesses are forced") | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `multiplicity_invisible_to_presence` | 441 | theorem | REFUTED (countermodel to "multiplicity adds carrier-pair distinctions") | propext, Quot.sound | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `repetition_no_new_content` | 453 | theorem | FROZEN (list lemma) | propext | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `repetition_new_occurrence` | 472 | theorem | FROZEN (list lemma) | propext | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `const_presentation_unfaithful` | 481 | theorem | CONDITIONAL:`Irrefl r'` | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `id_presentation_faithful` | 485 | theorem | FROZEN (trivial) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `clos_empty_id` | 502 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Auxiliary (`A`, [`PrimDiff.md`](audit/modules/PrimDiff.md)) |
| `irred_empty_iff_ne` | 515 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `irred_antitone` | 527 | theorem | FROZEN | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |
| `merger_erases` | 541 | theorem | CONDITIONAL:`F (fun _ => v)` (a constant map, not merely a merge of the pair) | none | `Unit 14`, `Unit 15`, `Unit 23`, `Unit 24`, `Unit 25` — Substantive (`S`) |

### 5.56 `PrimitiveCats` (`lean4/Derivation/PrimitiveCats.lean`) — Root-imported — `Unit 52`

- **Audit appendix:** [`textbook/audit/modules/PrimitiveCats.md`](audit/modules/PrimitiveCats.md)
- **Auxiliary / omission justification:** Omit: `catsFindings` (label list); `d2Swap_initial` can be taught as "the same proof with roles exchanged" rather than as a separate theorem.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `PtdRel` | 36 | structure | ADMITTED (the object notion) | n/a (definition) | `Unit 52` (Definition / Structure) |
| `Hom` | 45 | structure | ADMITTED (morphism notion) | n/a (definition) | `Unit 52` (Definition / Structure) |
| `idH` | 65 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `comp` | 69 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `IrreflObj` | 87 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `SymObj` | 91 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `d2Obj` | 97 | def | ADMITTED (concrete object) | n/a (definition) | `Unit 52` (Definition / Structure) |
| `s2Obj` | 102 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `d2SwapObj` | 109 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `Initial` | 132 | def | ADMITTED (standard notion, defined natively) | n/a (definition) | `Unit 52` (Definition / Structure) |
| `WeaklyInitial` | 136 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `wideObj` | 302 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `bigObj` | 320 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `bigHomA` | 327 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `bigHomB` | 335 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `BoolBijective` | 373 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `IsRelAuto` | 378 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `bigObj3` | 439 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `Pres` | 446 | structure | ADMITTED (the "faithful presentation" = observer-cut notion) | n/a (definition) | `Unit 52` (Definition / Structure) |
| `PHom` | 453 | structure | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `pid`, `pcomp` | 467, 470 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `idPres3` | 485 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `mergeA` | 502 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `mergeB` | 506 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `Pres2` | 579 | structure | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `PHom2` | 585 | structure | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `idPres2` | 600 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `swapPres2` | 603 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `Epi2` | 608 | def | ADMITTED (named "epi" but defined as surjectivity, not the categorical cancellation property) | n/a (definition) | `Unit 52` (Definition / Structure) |
| `freePres2` | 666 | def | ADMITTED | n/a (definition) | `Unit 52` (Definition / Structure) |
| `catsFindings` | 709 | def | ADMITTED (declared label list) | n/a (definition) | `Unit 52` (Definition / Structure) |
| `hom_ext` | 54 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `comp_id` | 75 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `id_comp` | 78 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `comp_assoc` | 81 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `d2Obj_irrefl` | 112 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `s2Obj_irrefl` | 114 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `s2Obj_sym` | 116 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `d2_not_obj_sym` | 124 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `weaklyInitial_of_initial` | 139 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `d2_initial` | 156 | theorem | FROZEN | Quot.sound | `Unit 52` — Substantive (`S`) |
| `d2_initial_irrefl` | 174 | theorem | FROZEN (the hypothesis is discarded; it is `d2_initial P`) | Quot.sound | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `d2_map_injective` | 185 | theorem | CONDITIONAL:`IrreflObj P` | none | `Unit 52` — Substantive (`S`) |
| `d2_map_not_injective_without_irrefl` | 198 | theorem | REFUTED (injectivity without irreflexivity) | none | `Unit 52` — Substantive (`S`) |
| `s2_initial_sym` | 209 | theorem | CONDITIONAL:`SymObj T` | Quot.sound | `Unit 52` — Substantive (`S`) |
| `s2_no_hom_to_d2` | 234 | theorem | VERIFIED_FINITE / REFUTED (existence of such a morphism) | none | `Unit 52` — Substantive (`S`) |
| `s2_not_weakly_initial` | 245 | theorem | REFUTED | none | `Unit 52` — Substantive (`S`) |
| `s2_not_initial` | 248 | theorem | REFUTED | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `d2Swap_initial` | 256 | theorem | FROZEN | Quot.sound | `Unit 52` — Substantive (`S`) |
| `two_initials_not_identical` | 275 | theorem | VERIFIED_FINITE | none | `Unit 52` — Substantive (`S`) |
| `initials_iso` | 286 | theorem | FROZEN | none | `Unit 52` — Substantive (`S`) |
| `wideObj_irrefl` | 307 | theorem | FROZEN (over metatheoretic `n : Nat`) | propext, Quot.sound | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `ptd_on_every_larger_carrier` | 314 | theorem | FROZEN (over `n : Nat`) | propext, Quot.sound | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `bigHomA_ne_bigHomB` | 341 | theorem | FROZEN (over `n`) | propext, Quot.sound | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `larger_not_initial` | 353 | theorem | REFUTED (initiality of this family) | propext, Quot.sound | `Unit 52` — Substantive (`S`) |
| `d2_autos` | 384 | theorem | FROZEN (over `f : Bool → Bool`) | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `s2_swap_auto` | 391 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `s2_id_auto` | 396 | theorem | VERIFIED_FINITE (Iff.rfl) | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `not_bijective` | 400 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `s2_swap_isRelAuto` | 410 | theorem | VERIFIED_FINITE | none | `Unit 52` — Substantive (`S`) |
| `not_not_d2_auto` | 414 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `d2_swap_not_isRelAuto` | 419 | theorem | VERIFIED_FINITE | none | `Unit 52` — Substantive (`S`) |
| `pointed_rigid` | 426 | theorem | FROZEN (immediate from `ha`,`hb`) | none | `Unit 52` — Substantive (`S`) |
| `phom_ext` | 457 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `pcomp_pid`, `pid_pcomp`, `pcomp_assoc` | 474–480 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `pres_initial` | 490 | theorem | FROZEN | propext, Quot.sound | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `no_phom_mergeA_mergeB` | 511 | theorem | VERIFIED_FINITE / REFUTED | propext | `Unit 52` — Substantive (`S`) |
| `no_phom_mergeB_mergeA` | 522 | theorem | VERIFIED_FINITE / REFUTED | propext | `Unit 52` — Substantive (`S`) |
| `no_terminal_pres` | 548 | theorem | REFUTED (weak terminality) | propext | `Unit 52` — Substantive (`S`) |
| `phom2_ext` | 589 | theorem | FROZEN | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `idPres2_epi` | 610 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `swapPres2_epi` | 612 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `phom2_unique_of_epi` | 619 | theorem | CONDITIONAL:`Epi2 P` | Quot.sound | `Unit 52` — Substantive (`S`) |
| `phom2_exists_from_id` | 627 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `phom2_exists_from_swap` | 632 | theorem | VERIFIED_FINITE | none | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `phom2_unique_exists_id` | 636 | theorem | VERIFIED_FINITE | Quot.sound | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `phom2_unique_exists_swap` | 644 | theorem | VERIFIED_FINITE | Quot.sound | `Unit 52` — Auxiliary (`A`, [`PrimitiveCats.md`](audit/modules/PrimitiveCats.md)) |
| `no_terminal_pres2` | 677 | theorem | REFUTED (terminality in `Pres2`) | propext, Quot.sound | `Unit 52` — Substantive (`S`) |

### 5.57 `PrimitiveContact` (`lean4/Derivation/PrimitiveContact.lean`) — Root-imported — `Unit 53`

- **Audit appendix:** [`textbook/audit/modules/PrimitiveContact.md`](audit/modules/PrimitiveContact.md)
- **Auxiliary / omission justification:** Recommend omitting: `contactStatus`, `contactStatusHistory`, `contactStatusCurrent`, `contactVerdictPrimary`, `contact_status_count` (protocol bookkeeping, not mathematics; mention in a provenance footnote).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `contactStatus` | 80 | def | ADMITTED (declared policy; historical) | n/a (definition) | `Unit 53` (Definition / Structure) |
| `NativeKernel` | 84 | def (`Type 1`) | ADMITTED (the declared interface) | n/a (definition) | `Unit 53` (Definition / Structure) |
| `nativeKernelWitness` | 89 | def | ADMITTED (inhabitant) | n/a (definition) | `Unit 53` (Definition / Structure) |
| `contactStatusHistory` | 116 | def | ADMITTED (DECLARED_POLICY) | n/a (definition) | `Unit 53` (Definition / Structure) |
| `contactStatusCurrent` | 122 | def | ADMITTED (DECLARED_POLICY; must match the Python constant) | n/a (definition) | `Unit 53` (Definition / Structure) |
| `contactVerdictPrimary` | 126 | def | ADMITTED (DECLARED_POLICY) | n/a (definition) | `Unit 53` (Definition / Structure) |
| `native_kernel_initial` | 99 | theorem | FROZEN (proved in `PrimitiveCats`; not re-audited here) | Quot.sound | `Unit 53` — Substantive (`S`) |
| `contact_status_count` | 131 | theorem | VERIFIED_FINITE (of a declared datum) | none | `Unit 53` — Auxiliary (`A`, [`PrimitiveContact.md`](audit/modules/PrimitiveContact.md)) |
| `native_interface_not_representable` | 137 | theorem | REFUTED (proved in `ContactBridge`; not re-audited here) | none | `Unit 53` — Substantive (`S`) |
| `corpus` | (grouped in [`PrimitiveContact.md`](audit/modules/PrimitiveContact.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 53` — Auxiliary (`A`, [`PrimitiveContact.md`](audit/modules/PrimitiveContact.md)) |

### 5.58 `PrimitiveCore` (`lean4/Derivation/PrimitiveCore.lean`) — Root-imported — `Unit 51`

- **Audit appendix:** [`textbook/audit/modules/PrimitiveCore.md`](audit/modules/PrimitiveCore.md)
- **Auxiliary / omission justification:** Omit: the `open_cell_*` strings (teach the OPEN scope in prose instead); the per-row routine cells can be summarised as a matrix figure rather than taught one by one.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Setting` | 36 | structure | ADMITTED (the declared common signature; `X : Type` and `Ops` are metatheoretic) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `Cotrans` | 49 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `Located` | 55 | def | ADMITTED (metatheoretic existential over a function type; declared "admitted as separate data") | n/a (definition) | `Unit 51` (Definition / Structure) |
| `W` | 73 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `A` | 76 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `Bs` | 79 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `Bc` | 82 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `Bl` | 85 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `C` | 89 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `D` | 93 | def | ADMITTED (shown equal to `a ≠ b` by `D_iff_ne`) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `E` | 99 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `F` | 103 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `unitBare` | 159 | def | ADMITTED (concrete model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `unitFull` | 171 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `d2Bare` | 181 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `d2Merged` | 192 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `d2Protected` | 202 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `d2ProtectedMerged` | 213 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `s2Bare` | 223 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `s2Merged` | 233 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `triR` | 243 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| (instance) | 245 | instance | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `triSymR` | 249 | def | ADMITTED | n/a (definition) | `Unit 51` (Definition / Structure) |
| `tri` | 253 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `triProtected` | 264 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `triSym` | 275 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `boolEmpty` | 287 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `boolEmptyMerged` | 298 | def | ADMITTED (model) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `open_cell_a_bl` | 545 | def (String) | ADMITTED (declared label, not a proposition) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `open_cell_bs_bl` | 578 | def (String) | ADMITTED (label) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `open_cell_bc_bl` | 605 | def (String) | ADMITTED (label) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `open_cell_f_bl` | 770 | def (String) | ADMITTED (label) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `matrixCells` | 841 | def | ADMITTED (declared label table; nothing in Lean ties a row to its theorem) | n/a (definition) | `Unit 51` (Definition / Structure) |
| `located_of_decidable` | 64 | theorem | CONDITIONAL:`[∀ x y, Decidable (r x y)]` | none | `Unit 51` — Substantive (`S`) |
| `D_iff_ne` | 107 | theorem | FROZEN | none | `Unit 51` — Substantive (`S`) |
| `cotrans_auto_on_two` | 121 | theorem | CONDITIONAL:`Irrefl r`, carrier fixed to `Bool` | none | `Unit 51` — Substantive (`S`) |
| `not_bs_of_not_a` | 137 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `not_bc_of_not_a` | 140 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `not_bl_of_not_a` | 143 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `not_f_of_not_a` | 146 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitBare_w` | 309 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitBare_not_a` | 311 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitBare_not_c` | 313 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitBare_not_d` | 315 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitBare_not_e` | 318 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitFull_c` | 321 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitFull_not_a` | 323 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitFull_not_d` | 325 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `unitFull_not_e` | 328 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Bare_a` | 331 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Merged_a` | 333 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Protected_f` | 336 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2ProtectedMerged_f` | 339 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2_not_symm` | 344 | theorem | VERIFIED_FINITE (`decide`) | n/a (probe: none) | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Bare_not_bs` | 347 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Protected_not_bs` | 349 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Bare_bc` | 351 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Merged_bc` | 354 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Bare_bl` | 357 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Merged_bl` | 360 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Bare_not_c` | 363 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Bare_not_f` | 365 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2Merged_not_e` | 367 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `d2ProtectedMerged_not_e` | 371 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `s2Bare_bs` | 375 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `s2Merged_bs` | 379 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `s2Bare_not_c` | 383 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `s2Bare_not_f` | 385 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `s2Merged_not_e` | 387 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triR_edge` | 391 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triR_irrefl` | 393 | theorem | VERIFIED_FINITE (`decide`) | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `tri_a` | 398 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `tri_bl` | 400 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `tri_not_bc` | 404 | theorem | VERIFIED_FINITE | n/a (probe: propext) | `Unit 51` — Substantive (`S`) |
| `triProtected_f` | 416 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triProtected_not_bc` | 419 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triSymR_edge` | 431 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triSymR_irrefl` | 433 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triSymR_symm` | 439 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triSym_bs` | 444 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `triSym_not_bc` | 450 | theorem | VERIFIED_FINITE | n/a (probe: propext) | `Unit 51` — Substantive (`S`) |
| `boolEmpty_not_w` | 474 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `boolEmpty_not_a` | 476 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `boolEmpty_not_c` | 478 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `boolEmpty_d` | 480 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `boolEmpty_e` | 483 | theorem | VERIFIED_FINITE | n/a (probe: none) | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `boolEmptyMerged_d` | 487 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `boolEmptyMerged_not_e` | 490 | theorem | VERIFIED_FINITE | n/a | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_w_a` … `nimp_w_f` (8) | 500–526 | theorem | REFUTED (W→Q) | none | `Unit 51` — Substantive (`S`) |
| `imp_a_w` | 530 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_a_bs` | 534 | theorem | REFUTED | none | `Unit 51` — Substantive (`S`) |
| `nimp_a_bc` | 541 | theorem | REFUTED | propext | `Unit 51` — Substantive (`S`) |
| `nimp_a_c` | 548 | theorem | REFUTED | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `imp_a_d` | 553 | theorem | FROZEN | none | `Unit 51` — Substantive (`S`) |
| `nimp_a_e` | 559 | theorem | REFUTED | none | `Unit 51` — Substantive (`S`) |
| `nimp_a_f` | 562 | theorem | REFUTED | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `imp_bs_w`, `imp_bs_a`, `imp_bs_d` | 567–584 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_bs_bc` | 574 | theorem | REFUTED | propext | `Unit 51` — Substantive (`S`) |
| `nimp_bs_c`, `nimp_bs_e`, `nimp_bs_f` | 581–590 | theorem | REFUTED | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `imp_bc_w`, `imp_bc_a`, `imp_bc_d` | 595–611 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_bc_bs` | 601 | theorem | REFUTED | none | `Unit 51` — Substantive (`S`) |
| `nimp_bc_c`, `nimp_bc_e`, `nimp_bc_f` | 608–617 | theorem | REFUTED | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `imp_bl_w`, `imp_bl_a`, `imp_bl_d` | 625–641 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_bl_bs`, `nimp_bl_bc`, `nimp_bl_c`, `nimp_bl_e`, `nimp_bl_f` | 630–647 | theorem | REFUTED | none (bc: propext) | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `imp_c_w` | 656 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_c_a`, `nimp_c_d` | 660, 676 | theorem | REFUTED | none | `Unit 51` — Substantive (`S`) |
| `nimp_c_bs`, `nimp_c_bc`, `nimp_c_bl`, `nimp_c_e`, `nimp_c_f` | 663–683 | theorem | REFUTED | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_d_w` … `nimp_d_f` (8) | 692–718 | theorem | REFUTED | none | `Unit 51` — Substantive (`S`) |
| `nimp_e_w`, `nimp_e_a`, `nimp_e_bs`, `nimp_e_bc`, `nimp_e_bl`, `nimp_e_c`, `nimp_e_f` | 726–751 | theorem | REFUTED | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `imp_e_d` | 748 | theorem | FROZEN | none | `Unit 51` — Substantive (`S`) |
| `imp_f_w`, `imp_f_a`, `imp_f_c`, `imp_f_d` | 756–776 | theorem | FROZEN | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_f_bs` | 761 | theorem | REFUTED | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_f_bc` | 766 | theorem | REFUTED | propext | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_f_e` | 781 | theorem | REFUTED | none | `Unit 51` — Substantive (`S`) |
| `e_empty_iff_d` | 792 | theorem | CONDITIONAL:`S.Ops` empty | none | `Unit 51` — Substantive (`S`) |
| `prot_not_from_witness` | 804 | theorem | REFUTED (A → prot) | none | `Unit 51` — Substantive (`S`) |
| `ret_not_from_witness` | 809 | theorem | REFUTED (A → ret) | none | `Unit 51` — Substantive (`S`) |
| `f_ops_irrelevant` | 818 | theorem | FROZEN (definitional) | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `bool_class` | 827 | theorem | CONDITIONAL:`[∀ x y, Decidable (r x y)]` | propext, Quot.sound | `Unit 51` — Substantive (`S`) |
| `matrixCells_length` | 916 | theorem | VERIFIED_FINITE | none | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_w_bs` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_w_bc` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_w_bl` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_w_c` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_w_d` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_w_e` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_d_a` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_d_bs` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_d_bc` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_d_bl` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_d_c` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |
| `nimp_d_e` | (grouped in [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 51` — Auxiliary (`A`, [`PrimitiveCore.md`](audit/modules/PrimitiveCore.md)) |

### 5.59 `PrimitivePassage` (`lean4/Derivation/PrimitivePassage.lean`) — Root-imported — `Unit 54`

- **Audit appendix:** [`textbook/audit/modules/PrimitivePassage.md`](audit/modules/PrimitivePassage.md)
- **Auxiliary / omission justification:** Omit: `obst_diverges_when_undeclared` (retained only as a historical witness, per the ledger); `no_outside_operational` and `replay_deterministic` as separate results (they are congruences; teach determinism as "`step` is a function").

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `PState` | 77 | structure | ADMITTED (the passage state; nine declared separate fields) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `genesisP` | 89 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `PEvent` | 93 | inductive | ADMITTED (declared event alphabet) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `sepCol` | 110 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `sepP` | 115 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `zeroP` | 121 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `obstP` | 147 | def | ADMITTED; the `none ⇒ false` branch is a DECLARED POLICY (docstring, ledger CL-PD2-PACKET-05P) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `retainedP` | 168 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `protectedP` | 172 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `declaredP` | 176 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `zeroDeclP` | 184 | def | ADMITTED; DECLARED CONVENTION (vacuous truth) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `zeroStrictP` | 195 | def | ADMITTED (named only for `strict_gate_entails_declared`) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `obstEmptyObs` | 382 | def | ADMITTED (named rival policy) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `preRetainedObstructed` | 397 | def | ADMITTED (witness) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `gateWitnessNoZero` | 425 | def | ADMITTED (witness) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `gateWitnessNoDeclaration` | 433 | def | ADMITTED (witness) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `gateWitnessNoProtection` | 441 | def | ADMITTED (witness) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `gateWitnessNoRetention` | 449 | def | ADMITTED (witness) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `gateWitnessAll` | 456 | def | ADMITTED (witness) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `wfPair` | 592 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `refineOk` | 599 | def | ADMITTED (declared policy) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `colOk` | 614 | def | ADMITTED (declared policy) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `step` | 622 | def | ADMITTED (the declared kernel) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `replayP` | 678 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `inducedSetting` | 755 | def | ADMITTED (note `X := Nat`, see §4) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `preRetained` | 848 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `responseMenu` | 961 | def | ADMITTED (declared response universe) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `repairFamily` | 970 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `extensionProposals` | 997 | def | ADMITTED (declared extension universe) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `obstructedPairs` | 1224 | def | ADMITTED | n/a (definition) | `Unit 54` (Definition / Structure) |
| `nextFamilyP` | 1227 | def | ADMITTED (declared interpreter; `setBudget 1` is a declared self-funding policy) | n/a (definition) | `Unit 54` (Definition / Structure) |
| `zeroP_cons` | 124 | theorem | FROZEN | propext, Quot.sound | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `obstP_strict_factors` | 202 | theorem | FROZEN (definitional) | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `obstP_factors` | 218 | theorem | FROZEN (near-definitional, as its docstring says) | p,Q | `Unit 54` — Substantive (`S`) |
| `obst_of_gates` | 227 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `gates_of_obst` | 237 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `obstP_reads_three_stores` | 253 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `undeclared_gates` | 264 | theorem | CONDITIONAL:`s.obs = none` | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `obs_gates_not_both_false` | 281 | theorem |  | zeroDeclP s i j = true` always | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `strict_gate_entails_declared` | 292 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `wit_independent_of_obs` | 309 | theorem | FROZEN (definitional) | none | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `obst_requires_observation` | 326 | theorem | CONDITIONAL:`s.obs = none`; unfolds a DECLARED POLICY | p,Q | `Unit 54` — Substantive (`S`) |
| `obst_agrees_when_declared` | 338 | theorem | CONDITIONAL:`s.obs = some cols` | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `obst_diverges_when_undeclared` | 361 | theorem | VERIFIED_FINITE (first conjunct is a closed truth not about the state — module and ledger say so) | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `obst_policies_agree_when_declared` | 390 | theorem | CONDITIONAL:`s.obs = some cols` | p,Q | `Unit 54` — Substantive (`S`) |
| `obst_policies_differ` | 408 | theorem | VERIFIED_FINITE (`decide`) | p,Q | `Unit 54` — Substantive (`S`) |
| `obst_conditions_independent` | 476 | theorem | VERIFIED_FINITE (`decide`) | p,Q | `Unit 54` — Substantive (`S`) |
| `gate_zero_independent` | 521 | theorem | REFUTED (entailment), witness `gateWitnessNoZero` | p,Q | `Unit 54` — Substantive (`S`) |
| `gate_declared_independent` | 539 | theorem | REFUTED | p,Q | `Unit 54` — Substantive (`S`) |
| `gate_protection_independent` | 555 | theorem | REFUTED | p,Q | `Unit 54` — Substantive (`S`) |
| `gate_retention_independent` | 571 | theorem | REFUTED | p,Q | `Unit 54` — Substantive (`S`) |
| `assertion_not_retained` | 692 | theorem | VERIFIED_FINITE | p,Q | `Unit 54` — Substantive (`S`) |
| `retention_not_free` | 702 | theorem | VERIFIED_FINITE | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `retention_requires_assertion` | 711 | theorem | CONDITIONAL:`halted = false`, `(i,j) ∉ asserted` | p,Q | `Unit 54` — Substantive (`S`) |
| `retention_persists` | 725 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `assertion_persists` | 734 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `asserted_offdiag_step` | 766 | theorem | FROZEN | not in artifact (probe: p,Q) | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `asserted_offdiag` | 787 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `retained_sub_asserted_step` | 800 | theorem | FROZEN | not in artifact (probe: p,Q) | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `retained_sub_asserted` | 821 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `assert_transport` | 838 | theorem | CONDITIONAL:`(a,b) ∈ (replayP h genesisP).asserted` | p,Q | `Unit 54` — Substantive (`S`) |
| `kernel_enters_preretained` | 855 | theorem | VERIFIED_FINITE (via `assert_transport` + `decide`) | p,Q | `Unit 54` — Substantive (`S`) |
| `retention_completes` | 864 | theorem | VERIFIED_FINITE | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `witness_no_protection` | 870 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `no_protection_no_obstruction` | 878 | theorem | VERIFIED_FINITE | p,Q | `Unit 54` — Substantive (`S`) |
| `quotient_no_recovery` | 897 | theorem | FROZEN (trivial by rewriting; see §11) | none | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `sepCol_irrefl` | 907 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `sepCol_symm` | 912 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `sepCol_trans` | 917 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `zero_refl` | 925 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `zero_symm` | 934 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `zero_trans` | 944 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `menu_complete` | 982 | theorem | CONDITIONAL:`s.obs = some cols` | p,Q | `Unit 54` — Substantive (`S`) |
| `extension_always_available` | 1006 | theorem | CONDITIONAL:`obstP`, `i ≠ j`, in-bounds, protected (`hprot` is derivable from `hobst`; probe) | p,Q | `Unit 54` — Substantive (`S`) |
| `two_rule` | 1082 | theorem | CONDITIONAL: as above | p,Q | `Unit 54` — Substantive (`S`) |
| `proposal_not_execution` | 1098 | theorem | CONDITIONAL:`licensed = false`, `halted = false` | p,Q | `Unit 54` — Substantive (`S`) |
| `budget_gates_execution` | 1112 | theorem | CONDITIONAL:`budget = 0`, `halted = false` | p,Q | `Unit 54` — Substantive (`S`) |
| `refusal_object_inert` | 1130 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `refusal_not_terminal` | 1141 | theorem | FROZEN | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `step_halted` | 1148 | theorem | CONDITIONAL:`halted = true` | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `terminal_absorbing` | 1156 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `no_outside_operational` | 1166 | theorem | FROZEN (trivial congruence; see §11) | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `replay_deterministic` | 1171 | theorem | FROZEN (trivial congruence; see §11) | p,Q | `Unit 54` — Auxiliary (`A`, [`PrimitivePassage.md`](audit/modules/PrimitivePassage.md)) |
| `replay_append` | 1175 | theorem | FROZEN | p,Q | `Unit 54` — Substantive (`S`) |
| `extension_resolves` | 1185 | theorem | CONDITIONAL: six named hypotheses | p,Q | `Unit 54` — Substantive (`S`) |
| `nextFamilyP_stop` | 1236 | theorem | CONDITIONAL:`∀ r ∈ prot, obstP = false` | p,Q | `Unit 54` — Substantive (`S`) |
| `nextFamilyP_nonempty` | 1255 | theorem | CONDITIONAL: as `two_rule` | p,Q | `Unit 54` — Substantive (`S`) |
| `nextFamilyP_complete_repair` | 1273 | theorem | CONDITIONAL:`obstP`, protected, `m ∈ repairFamily` | p,Q | `Unit 54` — Substantive (`S`) |
| `nextFamilyP_complete_ext` | 1286 | theorem | CONDITIONAL:`obstP`, protected, `c ∈ extensionProposals` | p,Q | `Unit 54` — Substantive (`S`) |

### 5.60 `Progress` (`lean4/Derivation/Progress.lean`) — Root-imported — `Unit 35`

- **Audit appendix:** [`textbook/audit/modules/Progress.md`](audit/modules/Progress.md)
- **Auxiliary / omission justification:** Omit: `old_inst_form_lt`, `getD_*` helpers.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `old_inst_form_lt` | 22 | theorem | CONDITIONAL: `r.wf` | not in artifact | `Unit 35` — Auxiliary (`A`, [`Progress.md`](audit/modules/Progress.md)) |
| `getD_concat_self` | 27 | theorem | FROZEN | not in artifact | `Unit 35` — Auxiliary (`A`, [`Progress.md`](audit/modules/Progress.md)) |
| `getD_append_lt` | 34 | theorem | FROZEN | not in artifact (the artifact's `Attachment.getD_append_lt` is a different module's lemma) | `Unit 35` — Auxiliary (`A`, [`Progress.md`](audit/modules/Progress.md)) |
| `derivable_extend` | 45 | theorem | CONDITIONAL: `r.wf`, `x.1 ≠ r.forms.length` | not in artifact | `Unit 35` — Auxiliary (`A`, [`Progress.md`](audit/modules/Progress.md)) |
| `mark_progress` | 75 | theorem | CONDITIONAL: `r.wf`, `i < data`, `j < data`, `i ≠ j`, `∀ q ∈ r.reqs, separable r q.1 q.2` | propext, Quot.sound | `Unit 35` — Substantive (`S`) |
| `separable_of_subrules` | 202 | theorem | CONDITIONAL: `hsub` (subset) | propext | `Unit 35` — Substantive (`S`) |

### 5.61 `Quot` (`lean4/Derivation/Quot.lean`) — Root-imported — `Unit 27`

- **Audit appendix:** [`textbook/audit/modules/Quot.md`](audit/modules/Quot.md)
- **Auxiliary / omission justification:** Omit: `quotient_barrier` (duplicate of `quot_barrier`); teach the point that the theorem is a general fact about quotients and that the Genesis content is entirely in `R2L_collapsed`.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `collapseRel` | 31 | def | ADMITTED (no `Setoid` instance is built; `Quot` is used, so no equivalence proof is needed) | n/a (definition) | `Unit 27` (Definition / Structure) |
| `quotient_barrier` | 17 | theorem | FROZEN (a general Lean fact: `congrArg f (Quotient.sound h)`) | Quot.sound | `Unit 27` — Substantive (`S`) |
| `quot_barrier` | 23 | theorem | FROZEN | Quot.sound | `Unit 27` — Substantive (`S`) |
| `barrier_R2L` | 33 | theorem | FROZEN (instance at a concrete regime, via `R2L_collapsed`) | propext, Quot.sound | `Unit 27` — Substantive (`S`) |

### 5.62 `QuotientRetention` (`lean4/Derivation/QuotientRetention.lean`) — Root-imported — `Unit 72`

- **Audit appendix:** [`textbook/audit/modules/QuotientRetention.md`](audit/modules/QuotientRetention.md)
- **Auxiliary / omission justification:** Recommend omitting: `symmetry_failure_retains_multiplicity` (a renaming of `y` as `sigma x`; its docstring "The user's symmetry form" is a provenance note, not mathematics).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `RelationRefinement fine coarse` | 29 | structure (Prop) | ADMITTED (the hypothesis every theorem carries) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `collapseMap h` | 44 | def | ADMITTED (canonical construction via the quotient universal property) | n/a (definition) | `Unit 72` (Definition / Structure) |
| `RelationRefinement.refl` | 32 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`QuotientRetention.md`](audit/modules/QuotientRetention.md)) |
| `RelationRefinement.trans` | 36 | theorem | FROZEN | none | `Unit 72` — Auxiliary (`A`, [`QuotientRetention.md`](audit/modules/QuotientRetention.md)) |
| `collapseMap_mk` | 51 | theorem | FROZEN | Quot.sound | `Unit 72` — Auxiliary (`A`, [`QuotientRetention.md`](audit/modules/QuotientRetention.md)) |
| `collapseMap_surjective` | 58 | theorem | FROZEN | Quot.sound | `Unit 72` — Substantive (`S`) |
| `failed_identification_retains_two_classes` | 67 | theorem | CONDITIONAL: `coarse.r x y`, `¬ fine.r x y` | propext, Quot.sound | `Unit 72` — Substantive (`S`) |
| `failed_identification_makes_collapse_noninjective` | 82 | theorem | CONDITIONAL: same | propext, Quot.sound | `Unit 72` — Substantive (`S`) |
| `collapseMap_injective_iff_reverse_refinement` | 98 | theorem | FROZEN | propext, Quot.sound | `Unit 72` — Substantive (`S`) |
| `symmetry_failure_retains_multiplicity` | 118 | theorem | CONDITIONAL: `hbefore`, `hafter` (instance of the previous with `y := sigma x`) | propext, Quot.sound | `Unit 72` — Auxiliary (`A`, [`QuotientRetention.md`](audit/modules/QuotientRetention.md)) |
| `collapseMap_compose` | 134 | theorem | FROZEN | Quot.sound | `Unit 72` — Auxiliary (`A`, [`QuotientRetention.md`](audit/modules/QuotientRetention.md)) |

### 5.63 `Refusal` (`lean4/Derivation/Refusal.lean`) — Root-imported — `Unit 38`

- **Audit appendix:** [`textbook/audit/modules/Refusal.md`](audit/modules/Refusal.md)
- **Auxiliary / omission justification:** Recommend omitting: the two `_from` helpers (inline the induction); `marker_state_invisible` (`rfl`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `REvent` | 43 | inductive | ADMITTED (reduced signature) | n/a (definition) | `Unit 38` (Definition / Structure) |
| `RState` | 51 | structure | ADMITTED | n/a (definition) | `Unit 38` (Definition / Structure) |
| `emptyR` | 57 | def | ADMITTED | n/a (definition) | `Unit 38` (Definition / Structure) |
| `Mode` | 59 | inductive | ADMITTED (five declared disciplines) | n/a (definition) | `Unit 38` (Definition / Structure) |
| `stepR` | 65 | def | ADMITTED (declared policy) | n/a (definition) | `Unit 38` (Definition / Structure) |
| `stepOcc` | 82 | def | ADMITTED (declared policy, the bridge's) | n/a (definition) | `Unit 38` (Definition / Structure) |
| `replayR` | 87 | def | ADMITTED | n/a (definition) | `Unit 38` (Definition / Structure) |
| `replayOcc` | 90 | def | ADMITTED | n/a (definition) | `Unit 38` (Definition / Structure) |
| `isMarker` | 107 | def | ADMITTED | n/a (definition) | `Unit 38` (Definition / Structure) |
| `AtMostTokR` | 139 | def | ADMITTED (invariant) | n/a (definition) | `Unit 38` (Definition / Structure) |
| `swapIdx` | 234 | def | ADMITTED | n/a (definition) | `Unit 38` (Definition / Structure) |
| `swapState` | 236 | def | ADMITTED (see §6) | n/a (definition) | `Unit 38` (Definition / Structure) |
| `taggedTranslation` | 273 | def | ADMITTED | n/a (definition) | `Unit 38` (Definition / Structure) |
| `silent_eq_meta` | 98 | theorem | FROZEN (all states/events of the reduced signature) | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `marker_state_invisible` | 103 | theorem | FROZEN | propext, Quot.sound | `Unit 38` — Auxiliary (`A`, [`Refusal.md`](audit/modules/Refusal.md)) |
| `markers_invisible_from` | 111 | theorem | FROZEN | not in artifact | `Unit 38` — Auxiliary (`A`, [`Refusal.md`](audit/modules/Refusal.md)) |
| `markers_invisible` | 131 | theorem | FROZEN | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `nonreify_carrier_bound` | 142 | theorem | CONDITIONAL:`m = silent ∨ metaMarker ∨ fact`, `AtMostTokR t0 s`, single-token event | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `fact_state_changes` | 173 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `silent_state_fixed` | 178 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `reifyUntagged_eq_occurrence` | 186 | theorem | FROZEN | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `reify_occ_from` | 197 | theorem | FROZEN | not in artifact | `Unit 38` — Auxiliary (`A`, [`Refusal.md`](audit/modules/Refusal.md)) |
| `reifyUntagged_replay_eq_occurrence` | 207 | theorem | FROZEN | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `reifyUntagged_two_admissions` | 214 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `reifyTagged_two_admissions` | 220 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `tag_separates` | 227 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `occurrence_state_swap_invariant` | 243 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `tagged_state_not_swap_invariant` | 252 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `canonical_designation` | 262 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `tagged_translation_separable` | 278 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 38` — Substantive (`S`) |
| `untagged_translation_collapsed` | 285 | theorem | VERIFIED_FINITE (instance of a FROZEN Inertia lemma) | propext | `Unit 38` — Substantive (`S`) |

### 5.64 `RefusalFrontier` (`lean4/Derivation/RefusalFrontier.lean`) — Root-imported — `Unit 39`

- **Audit appendix:** [`textbook/audit/modules/RefusalFrontier.md`](audit/modules/RefusalFrontier.md)
- **Auxiliary / omission justification:** Recommend omitting: `distinction_needs_two_constructors` and `singleton_algebra_monochrome` (restatements of their hypotheses; the FR4 content lives in the Python normal-form checks), `mono_code_swap_invariant` (`rfl`).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `AdmResult` | 56 | inductive | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `stepTraced` | 60 | def | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `storeSwap` | 94 | def | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `JState` | 124 | structure | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `stepJ` | 129 | def | ADMITTED (declared protocol R2) | n/a (definition) | `Unit 39` (Definition / Structure) |
| `PState` | 179 | structure | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `stepP` | 185 | def | ADMITTED (declared "sufficient, non-minimum" protocol) | n/a (definition) | `Unit 39` (Definition / Structure) |
| `bridgeState` | 192 | def | ADMITTED (concrete) | n/a (definition) | `Unit 39` (Definition / Structure) |
| `swapP` | 203 | def | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `MItem` | 223 | inductive | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `MState` | 228 | structure | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `stepM` | 236 | def | ADMITTED (declared minimum protocol) | n/a (definition) | `Unit 39` (Definition / Structure) |
| `minState` | 242 | def | ADMITTED (concrete) | n/a (definition) | `Unit 39` (Definition / Structure) |
| `stepU` | 292 | def | ADMITTED | n/a (definition) | `Unit 39` (Definition / Structure) |
| `stepRefl` | 304 | def | ADMITTED (declared reflective semantics; ignores any token) | n/a (definition) | `Unit 39` (Definition / Structure) |
| `reflState` | 309 | def | ADMITTED (a metatheoretic `Nat`-indexed family) | n/a (definition) | `Unit 39` (Definition / Structure) |
| `silent_repetition_inert` | 29 | theorem | CONDITIONAL:every admission of `h` is of a present token | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `trace_erasure` | 69 | theorem | FROZEN | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `histories_collapse` | 82 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `mono_code_swap_invariant` | 96 | theorem | FROZEN (`rfl`) | none | `Unit 39` — Auxiliary (`A`, [`RefusalFrontier.md`](audit/modules/RefusalFrontier.md)) |
| `distinct_code_not_swap_invariant` | 99 | theorem | FROZEN | none | `Unit 39` — Auxiliary (`A`, [`RefusalFrontier.md`](audit/modules/RefusalFrontier.md)) |
| `singleton_algebra_monochrome` | 105 | theorem | FROZEN (trivial) | propext | `Unit 39` — Auxiliary (`A`, [`RefusalFrontier.md`](audit/modules/RefusalFrontier.md)) |
| `distinction_needs_two_constructors` | 113 | theorem | FROZEN (trivial restatement; see §11) | none | `Unit 39` — Auxiliary (`A`, [`RefusalFrontier.md`](audit/modules/RefusalFrontier.md)) |
| `judgment_variant_second_judgment_not_datum` | 133 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `judgment_carrier_bound` | 138 | theorem | CONDITIONAL:`∀ tok ∈ h, tok = 0`, start singleton-or-empty | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `priced_bridge_closes` | 194 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `priced_bridge_oriented` | 210 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `min_witnessed_route_closes` | 249 | theorem | VERIFIED_FINITE (one concrete two-step state) | propext | `Unit 39` — Substantive (`S`) |
| `bridge_facts_not_law` | 261 | theorem | REFUTED (countermodel to "the bridge's facts entail the law"); the witness does not depend on `bridgeState` | propext, Quot.sound | `Unit 39` — Substantive (`S`) |
| `equivariant_output_invariant` | 276 | theorem | FROZEN (generic over `Type`s) | none | `Unit 39` — Substantive (`S`) |
| `untyped_reflect_fixpoint` | 294 | theorem | VERIFIED_FINITE | none | `Unit 39` — Auxiliary (`A`, [`RefusalFrontier.md`](audit/modules/RefusalFrontier.md)) |
| `toggle_two_cycle` | 298 | theorem | VERIFIED_FINITE | none | `Unit 39` — Auxiliary (`A`, [`RefusalFrontier.md`](audit/modules/RefusalFrontier.md)) |
| `reflective_chain_growth` | 316 | theorem | FROZEN (∀ n, metatheoretic) | propext | `Unit 39` — Substantive (`S`) |
| `reflective_chain_is_initial_segment` | 333 | theorem | FROZEN | propext | `Unit 39` — Substantive (`S`) |
| `reflective_chain_successor_relation` | 347 | theorem | FROZEN | propext | `Unit 39` — Substantive (`S`) |
| `reflective_chain_irreflexive_facts` | 363 | theorem | FROZEN (follows from the successor shape; `omega`) | propext, Quot.sound | `Unit 39` — Substantive (`S`) |

### 5.65 `RenamingStructure` (`lean4/Derivation/RenamingStructure.lean`) — Root-imported — `Unit 59`

- **Audit appendix:** [`textbook/audit/modules/RenamingStructure.md`](audit/modules/RenamingStructure.md)
- **Auxiliary / omission justification:** Recommend omitting: `equal_size_supplies_no_law` and `equal_cost_supplies_no_law` (duplicates of Attachment theorems); `upFamily_transport_id` (trivial).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `idRen n` | 57 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `invRen σ` | 67 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `compRen σ τ` | 76 | def | ADMITTED | n/a (definition) | `Unit 59` (Definition / Structure) |
| `collapseMap` | 371 | def | ADMITTED (countermodel datum) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `rawRenamePairs f l` | 389 | def | ADMITTED (countermodel apparatus) | n/a (definition) | `Unit 59` (Definition / Structure) |
| `Renaming.ext` | 48 | theorem | FROZEN | none | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `comp_id` | 90 | theorem | FROZEN | none | `Unit 59` — Substantive (`S`) |
| `id_comp` | 94 | theorem | FROZEN | none | `Unit 59` — Substantive (`S`) |
| `comp_assoc` | 98 | theorem | FROZEN | none | `Unit 59` — Substantive (`S`) |
| `inv_comp` | 102 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `comp_inv` | 107 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `inv_inv` | 112 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `map_getD_range` | 118 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `act_id` | 129 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `act_comp` | 168 | theorem | CONDITIONAL: `n ≤ len` | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `act_inv` | 233 | theorem | CONDITIONAL: `n ≤ len` | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `upBlock_id` | 239 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `upBlock_comp` | 244 | theorem | CONDITIONAL: `n ≤ len` | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `upFamily_id` | 251 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `upFamily_comp` | 255 | theorem | CONDITIONAL: `n ≤ len` | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `upFamily_transport_comp` | 262 | theorem | CONDITIONAL: `n = len` | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `upFamily_transport_id` | 270 | theorem | FROZEN | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `wf_act` | 280 | theorem | CONDITIONAL: `n = len`, WFStores | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `act_up_comm_comp` | 312 | theorem | CONDITIONAL: four hypotheses | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `act_up_comm_twostep` | 323 | theorem | CONDITIONAL: four hypotheses | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `upFamily_orbit_closed` | 342 | theorem | CONDITIONAL: `n = len`, membership | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `star_orbit_both_present` | 353 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `upFamily_length` | 362 | theorem | FROZEN | propext | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `collapse_not_a_renaming` | 379 | theorem | REFUTED (collapse is not a renaming) | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `collapse_pushforward_ill_formed` | 397 | theorem | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | `Unit 59` — Substantive (`S`) |
| `equal_size_supplies_no_law` | 411 | theorem | REFUTED | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `equal_cost_supplies_no_law` | 420 | theorem | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | `Unit 59` — Auxiliary (`A`, [`RenamingStructure.md`](audit/modules/RenamingStructure.md)) |
| `equivariance_summary` | 461 | theorem | CONDITIONAL: four hypotheses | propext, Quot.sound | `Unit 59` — Substantive (`S`) |

### 5.66 `Represented` (`lean4/Derivation/Represented.lean`) — Root-imported — `Unit 45`

- **Audit appendix:** [`textbook/audit/modules/Represented.md`](audit/modules/Represented.md)
- **Auxiliary / omission justification:** Omit from the textbook: `schedWorld` (dead), `replay_deterministic` as a theorem (present it as a remark on the type of `step`); treat `histUpTo` as a worked example, not as an internal object.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| View | 70 | abbrev | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| Req | 73 | abbrev | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| World | 80 | structure | ADMITTED (budget and license are declared policy fields) | n/a (definition) | `Unit 45` (Definition / Structure) |
| genesis | 90 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| sepB | 94 | def | ADMITTED (declared separation law; constitution) | n/a (definition) | `Unit 45` (Definition / Structure) |
| satB | 97 | def | ADMITTED (constitution) | n/a (definition) | `Unit 45` (Definition / Structure) |
| violB | 100 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| quiescentB | 103 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| markApply | 108 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| preservesB | 111 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| dischargesSomeB | 114 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| markOkB | 117 | def | ADMITTED (constitution) | n/a (definition) | `Unit 45` (Definition / Structure) |
| augApply | 125 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| increaseB | 128 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| augOkB | 133 | def | ADMITTED (constitution) | n/a (definition) | `Unit 45` (Definition / Structure) |
| responseMenu | 144 | def | ADMITTED (declared policy; map row says "the menu is constitution") | n/a (definition) | `Unit 45` (Definition / Structure) |
| repairsB | 148 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| repairFamily | 151 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| obstructedB | 154 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| Event | 164 | inductive | ADMITTED (constitution: the event grammar) | n/a (definition) | `Unit 45` (Definition / Structure) |
| reqOkB | 175 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| step | 179 | def | ADMITTED (constitution) | n/a (definition) | `Unit 45` (Definition / Structure) |
| replay | 200 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| Supp | 219 | structure | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| supp | 228 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| SameElems | 329 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| WEquiv | 332 | def | ADMITTED (declared replay-equivalence) | n/a (definition) | `Unit 45` (Definition / Structure) |
| WF | 689 | def | ADMITTED (invariant, proved to hold on replays) | n/a (definition) | `Unit 45` (Definition / Structure) |
| blockEvents | 1013 | def | ADMITTED (supplied stream) | n/a (definition) | `Unit 45` (Definition / Structure) |
| histUpTo | 1016 | def | ADMITTED (metatheoretic history producer, declared as such) | n/a (definition) | `Unit 45` (Definition / Structure) |
| worldAt | 1020 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| witValid | 1090 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 45` (Definition / Structure) |
| prefixList | 1102 | def | ADMITTED (countermodel; g is metatheory) | n/a (definition) | `Unit 45` (Definition / Structure) |
| Evaluator | 1130 | abbrev | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| verdictB | 1132 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| certPosB | 1137 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| certNegB | 1140 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| stepSched | 1194 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 45` (Definition / Structure) |
| schedWorld | 1199 | def | ADMITTED (dead definition) | n/a (definition) | `Unit 45` (Definition / Structure) |
| schedWorld2 | 1206 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| stepGensym | 1214 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| stepOracle | 1223 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| oracleWorld | 1234 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| obstructedTruncB | 1245 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 45` (Definition / Structure) |
| truncWorld | 1248 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| overwriteFirst | 1262 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 45` (Definition / Structure) |
| owWorld | 1265 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| stepHead | 1292 | def | ADMITTED (countermodel) | n/a (definition) | `Unit 45` (Definition / Structure) |
| headWorldA / headWorldB | 1301 / 1305 | def | ADMITTED | n/a (definition) | `Unit 45` (Definition / Structure) |
| bool_eq_of_iff | 58 | theorem | FROZEN | propext | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| or_not_eq_true | 62 | theorem | \ | b) = true ↔ (a → b)` | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| replay_deterministic | 208 | theorem | FROZEN (conclusion trivially true; docstring says definitional) | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| replay_nil | 211 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| replay_append | 213 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| support_determines | 234 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| internal_support | 292 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| notes_inert | 298 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| repairFamily_sound | 305 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| repairFamily_complete | 310 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| repairFamily_retains_ties | 317 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| sameElems_refl | 337 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| sameElems_append | 340 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| sameElems_map | 353 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| any_congr | 364 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| all_congr | 374 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| satB_congr | 384 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| violB_congr | 388 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| sameElems_flatMap_menu | 397 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| markApply_equiv | 409 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| preservesB_congr | 415 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| dischargesSomeB_congr | 433 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| markOkB_congr | 451 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| increaseB_congr | 463 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| augOkB_congr | 479 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| repairsB_congr | 489 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| obstructedB_congr | 494 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| reqOkB_congr | 512 | theorem | FROZEN | not in artifact | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| equiv_step | 525 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| equiv_replay | 571 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| equiv_repairFamily | 579 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| mark_discharges | 594 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| mark_preserves | 606 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| step_mark_sound | 620 | theorem | CONDITIONAL: markOkB, 0 < budget (both explicit) | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| satB_aug | 652 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| aug_preserves_satisfied | 658 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| aug_increases | 665 | theorem | CONDITIONAL: augOkB | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| wf_genesis | 693 | theorem | FROZEN | none | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| wf_step | 697 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| wf_replay | 762 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| represented_progress | 778 | theorem | CONDITIONAL: WF (an invariant on replays) | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| progress_needs_budget | 868 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| progress_needs_license | 880 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| violation_only_from_require | 895 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| quiescent_stable | 966 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| admit_data_fresh | 1022 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| histUpTo_prefix | 1029 | theorem | FROZEN (about the supplied stream) | none | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| worldAt_data | 1035 | theorem | FROZEN (about the supplied stream) | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| worldAt_growth | 1067 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| productive_run | 1074 | theorem | FROZEN (about the supplied stream) | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| worldAt_three_quiescent | 1084 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Auxiliary (`A`, [`Represented.md`](audit/modules/Represented.md)) |
| wit_all_lengths | 1093 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| wit_no_infinite | 1107 | theorem | FROZEN (g is metatheory) | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| cert_scope | 1146 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| cert_not_correspondence | 1176 | theorem | REFUTED (refutes "certification = correspondence"), VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| cert_panel_relative | 1182 | theorem | REFUTED (refutes monotonicity), VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| scheduler_hidden | 1210 | theorem | REFUTED / VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| gensym_hidden | 1219 | theorem | REFUTED / VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| oracle_hidden | 1238 | theorem | REFUTED / VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| incomplete_search_false_alarm | 1255 | theorem | REFUTED / VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| augmentation_destroys_old_replay | 1273 | theorem | REFUTED / VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| repetition_not_progress | 1283 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| order_sensitivity_splits_equivalents | 1315 | theorem | REFUTED / VERIFIED_FINITE | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| refusal_needs_certificate | 1338 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |
| refusals_are_represented | 1351 | theorem | FROZEN | propext, Quot.sound | `Unit 45` — Substantive (`S`) |

### 5.67 `ResidualClosure` (`lean4/Derivation/ResidualClosure.lean`) — Root-imported — `Unit 71`

- **Audit appendix:** [`textbook/audit/modules/ResidualClosure.md`](audit/modules/ResidualClosure.md)
- **Auxiliary / omission justification:** Recommend omitting: `current_internal_symmetry_break_is_empty` and `current_directional_residual_is_empty` as separate items (immediate from ClosureSymmetry).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `InvariantUnderOn D f sigma` | 29 | def | ADMITTED | n/a (definition) | `Unit 71` (Definition / Structure) |
| `factorization_preserves_invariance` | 35 | theorem | CONDITIONAL: `FactorsOn D r q`, `hsigma` | Quot.sound | `Unit 71` — Auxiliary (`A`, [`ResidualClosure.md`](audit/modules/ResidualClosure.md)) |
| `carrying_right_face_loses_generating_invariance` | 46 | theorem | CONDITIONAL: `b`, `FactorsOn D r q` | Quot.sound | `Unit 71` — Substantive (`S`) |
| `carrying_right_face_splits_generating_pair` | 57 | theorem | CONDITIONAL: `b`, `FactorsOn D r q` | Quot.sound | `Unit 71` — Auxiliary (`A`, [`ResidualClosure.md`](audit/modules/ResidualClosure.md)) |
| `common_refinement_strictly_splits_left_face` | 72 | theorem | CONDITIONAL: `b`, `FactorsOn D r p`, `FactorsOn D r q` | propext, Quot.sound | `Unit 71` — Substantive (`S`) |
| `current_directional_residual_is_empty` | 86 | theorem | CONDITIONAL: `FactorsOn D r q` | Quot.sound | `Unit 71` — Auxiliary (`A`, [`ResidualClosure.md`](audit/modules/ResidualClosure.md)) |
| `current_internal_symmetry_break_is_empty` | 95 | theorem | CONDITIONAL: `FactorsOn D r q` | propext, Quot.sound | `Unit 71` — Auxiliary (`A`, [`ResidualClosure.md`](audit/modules/ResidualClosure.md)) |
| `common_refinement_closes_current_obstruction` | 106 | theorem | CONDITIONAL: same | propext, Quot.sound | `Unit 71` — Substantive (`S`) |

### 5.68 `Rounds` (`lean4/Derivation/Rounds.lean`) — Root-imported — `Unit 34`

- **Audit appendix:** [`textbook/audit/modules/Rounds.md`](audit/modules/Rounds.md)
- **Auxiliary / omission justification:** Omit: the choice-free list toolkit (`filter_*`, `nodup_*`, `range_nodup'`) from the main text; keep as an appendix note on the axiom boundary.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Round` | 283 | structure | ADMITTED (declared round shape) | n/a (definition) | `Unit 34` (Definition / Structure) |
| `ClosedRun r rds t` | 291 | inductive Prop | ADMITTED (declared policy: freshness and datum fixity are hypotheses of the shape, mirroring engine invariants) | n/a (definition) | `Unit 34` (Definition / Structure) |
| `filter_length_split` | 55 | theorem | FROZEN | propext, Quot.sound | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `nodup_head'` | 78 | theorem | FROZEN | not in artifact | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `nodup_tail'` | 83 | theorem | FROZEN | not in artifact | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `filter_none_of_all_false` | 88 | theorem | FROZEN | none | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `filter_nodup'` | 99 | theorem | FROZEN | not in artifact | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `nodup_filter_self_length` | 116 | theorem | FROZEN | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `nodup_subset_length` | 145 | theorem | FROZEN | propext, Quot.sound | `Unit 34` — Substantive (`S`) |
| `nodup_append_singleton` | 169 | theorem | FROZEN | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `allPairs_mem_bound` | 190 | theorem | FROZEN | propext, Quot.sound | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `mem_allPairs` | 205 | theorem | FROZEN | propext, Quot.sound | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `nodup_map_of_inj` | 222 | theorem | FROZEN | propext, Quot.sound | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `range_nodup'` | 240 | theorem | FROZEN | not in artifact | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `nodup_append_disjoint` | 249 | theorem | FROZEN | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `allPairs_nodup` | 264 | theorem | FROZEN | propext, Quot.sound | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `applyItem_data_eq` | 301 | theorem | CONDITIONAL: `it ≠ newDatum` | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `applyDelta_data_eq` | 328 | theorem | CONDITIONAL: `newDatum ∉ δ` | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `respond_anatomy` | 355 | theorem | FROZEN | propext | `Unit 34` — Substantive (`S`) |
| `round_reqs_succ` | 380 | theorem | CONDITIONAL: freshness `(i,j) ∉ r.reqs` | propext | `Unit 34` — Substantive (`S`) |
| `round_data_eq` | 389 | theorem | CONDITIONAL: `newDatum ∉ δ` | propext | `Unit 34` — Substantive (`S`) |
| `closedRun_data_eq` | 398 | theorem | FROZEN (over `ClosedRun`) | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `closedRun_reqs_length` | 405 | theorem | FROZEN (over `ClosedRun`) | propext, Quot.sound | `Unit 34` — Substantive (`S`) |
| `closedRun_reqs_nodup` | 415 | theorem | CONDITIONAL: `r.reqs.Nodup` | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `closedRun_reqs_wf` | 425 | theorem | CONDITIONAL: `hwf` | propext | `Unit 34` — Auxiliary (`A`, [`Rounds.md`](audit/modules/Rounds.md)) |
| `closedRun_round_bound` | 452 | theorem | CONDITIONAL: `r.reqs.Nodup`, `hwf` | propext, Quot.sound | `Unit 34` — Substantive (`S`) |
| `closedRun_round_bound_from_empty` | 472 | theorem | CONDITIONAL: `r.reqs = []` (and the `ClosedRun` shape) | propext, Quot.sound | `Unit 34` — Substantive (`S`) |

### 5.69 `RuleBridge` (`lean4/Derivation/RuleBridge.lean`) — Root-imported — `Unit 33`

- **Audit appendix:** [`textbook/audit/modules/RuleBridge.md`](audit/modules/RuleBridge.md)
- **Auxiliary / omission justification:** Omit: nothing; the auxiliary lemmas are one line each.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `dropRules` | 40 | def | ADMITTED | n/a (definition) | `Unit 33` (Definition / Structure) |
| `applyItem_rules_mono` | 46 | theorem | FROZEN | propext | `Unit 33` — Auxiliary (`A`, [`RuleBridge.md`](audit/modules/RuleBridge.md)) |
| `applyDelta_rules_mono` | 75 | theorem | FROZEN | propext | `Unit 33` — Auxiliary (`A`, [`RuleBridge.md`](audit/modules/RuleBridge.md)) |
| `applyDelta_dropRules` | 100 | theorem | FROZEN | propext | `Unit 33` — Substantive (`S`) |
| `dropRules_length_le` | 183 | theorem | FROZEN | propext | `Unit 33` — Auxiliary (`A`, [`RuleBridge.md`](audit/modules/RuleBridge.md)) |
| `dropRules_length_lt` | 195 | theorem | CONDITIONAL: `newRuleAll f ∈ δ` | propext | `Unit 33` — Auxiliary (`A`, [`RuleBridge.md`](audit/modules/RuleBridge.md)) |
| `aritySum_dropRules` | 225 | theorem | FROZEN | propext | `Unit 33` — Auxiliary (`A`, [`RuleBridge.md`](audit/modules/RuleBridge.md)) |
| `validResponse_dropRules` | 245 | theorem | FROZEN | propext | `Unit 33` — Substantive (`S`) |
| `rule_item_never_minimal` | 259 | theorem | CONDITIONAL: `newRuleAll f ∈ δ` (the premise is the claim's scope) | propext | `Unit 33` — Substantive (`S`) |

### 5.70 `SeparationCapacity` (`lean4/Derivation/SeparationCapacity.lean`) — Root-imported — `Unit 41`

- **Audit appendix:** [`textbook/audit/modules/SeparationCapacity.md`](audit/modules/SeparationCapacity.md)
- **Auxiliary / omission justification:** Recommend omitting: the three `filter_range_*` lemmas and `profile2_interior`/`profileD_radius_one` as separate items (fold into one sentence: "on an interior point the depth-2 record is exactly the three neighbouring depth-1 profiles").

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `ball` | 84 | def | ADMITTED (declared observation window; on the deep interior no clipping occurs) | n/a (definition) | `Unit 41` (Definition / Structure) |
| `profileD` | 93 | def | ADMITTED (declared regime) | n/a (definition) | `Unit 41` (Definition / Structure) |
| `filter_range_decide_eq` | 42 | theorem | FROZEN | propext, Quot.sound | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `filter_range_succ_eq` | 62 | theorem | CONDITIONAL:`0 < i`, `i ≤ n` | propext, Quot.sound | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `filter_range_eq` | 76 | theorem | CONDITIONAL:`i < n` | propext, Quot.sound | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `ball_length` | 87 | theorem | FROZEN | propext | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `profileD_deep` | 99 | theorem | CONDITIONAL:`d < i`, `i + d < n` | propext, Quot.sound | `Unit 41` — Substantive (`S`) |
| `depth_d_outrun` | 119 | theorem | CONDITIONAL:deepness of both points | propext, Quot.sound | `Unit 41` — Substantive (`S`) |
| `depth_d_obstruction` | 127 | theorem | CONDITIONAL:`2d + 3 ≤ n` | propext, Quot.sound | `Unit 41` — Substantive (`S`) |
| `incoming_edges_interior` | 143 | theorem | CONDITIONAL:`0 < i`, `i ≤ n` | propext, Quot.sound | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `outgoing_edges_interior` | 151 | theorem | CONDITIONAL:`i < n` | propext, Quot.sound | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `profile2_interior` | 159 | theorem | CONDITIONAL:`0 < i < n` | propext, Quot.sound | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `profileD_radius_one` | 169 | theorem | CONDITIONAL:`0 < i` | propext, Quot.sound | `Unit 41` — Auxiliary (`A`, [`SeparationCapacity.md`](audit/modules/SeparationCapacity.md)) |
| `radius_one_agrees_with_sealed_depth2` | 181 | theorem | CONDITIONAL:both interior | propext, Quot.sound | `Unit 41` — Substantive (`S`) |
| `radius_one_agrees_with_sealed_depth2_n5` | 201 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 41` — Substantive (`S`) |
| `radius_one_agrees_with_sealed_depth2_n4` | 224 | theorem | VERIFIED_FINITE (third conjunct: `omega`) | propext, Quot.sound | `Unit 41` — Substantive (`S`) |

### 5.71 `StableContent` (`lean4/Derivation/StableContent.lean`) — Root-imported — `Unit 62`

- **Audit appendix:** [`textbook/audit/modules/StableContent.md`](audit/modules/StableContent.md)
- **Auxiliary / omission justification:** Recommend omitting or demoting: the restricted fragment (`IsTraceExcludedEvent`, `RestrictedStableSep`, `sUnfunded`) to a remark — the source itself says it is "not a second countermodel to full trace stability" and the fragment is a syntactic choice with no ownership meaning; if kept, use a reachable witness (the probe's history, with the final `halt` dropped and the budget spent to 0 by `addCol [1]`) rather than `sUnfunded`.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `protSep` | 63 | def (Bool) | ADMITTED | n/a (definition) | `Unit 62` (Definition / Structure) |
| `SepHere` | 70 | def (Prop) | ADMITTED | n/a (definition) | `Unit 62` (Definition / Structure) |
| `TraceStableSep` | 76 | def (Prop) | ADMITTED (metatheoretic universal over all event lists) | n/a (definition) | `Unit 62` (Definition / Structure) |
| `IsTraceExcludedEvent` | 83 | def (Bool) | ADMITTED (declared syntactic fragment, "no ownership claim") | n/a (definition) | `Unit 62` (Definition / Structure) |
| `RestrictedTrace` | 91 | def (Prop) | ADMITTED | n/a (definition) | `Unit 62` (Definition / Structure) |
| `RestrictedStableSep` | 97 | def (Prop) | ADMITTED | n/a (definition) | `Unit 62` (Definition / Structure) |
| `sHalt` | 273 | def | ADMITTED (countermodel state) | n/a (definition) | `Unit 62` (Definition / Structure) |
| `sUnfunded` | 410 | def | ADMITTED (countermodel state) | n/a (definition) | `Unit 62` (Definition / Structure) |
| `sUnprot` | 465 | def | ADMITTED (witness state) | n/a (definition) | `Unit 62` (Definition / Structure) |
| `openExactStabilityCharacterization` | 495 | def (Prop) | ADMITTED (named OPEN proposition; never proved) | n/a (definition) | `Unit 62` (Definition / Structure) |
| `quiescentP` | 502 | def (Prop) | ADMITTED (universal over all `Nat` pairs; `obstP` is false off `wit` so the content is finite) | n/a (definition) | `Unit 62` (Definition / Structure) |
| `sepP_append` | 103 | theorem | CONDITIONAL:Sep | propext, Quot.sound | `Unit 62` — Auxiliary (`A`, [`StableContent.md`](audit/modules/StableContent.md)) |
| `sepP_refine` | 112 | theorem | CONDITIONAL:Dec, `refineOk`, Prot, Sep | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `prot_mono` | 130 | theorem | CONDITIONAL:Prot | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `sep_preserved` | 138 | theorem | CONDITIONAL:Dec, Prot, Sep | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `protSep_persists` | 245 | theorem | CONDITIONAL:`protSep` | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `protSep_replays` | 264 | theorem | CONDITIONAL:`protSep` | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `protSep_trace_stable` | 281 | theorem | CONDITIONAL:`protSep` | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `trace_stable_restricted_stable` | 300 | theorem | CONDITIONAL:`TraceStableSep` | propext, Quot.sound | `Unit 62` — Auxiliary (`A`, [`StableContent.md`](audit/modules/StableContent.md)) |
| `replay_halted` | 308 | theorem | CONDITIONAL:`s.halted = true` | propext, Quot.sound | `Unit 62` — Auxiliary (`A`, [`StableContent.md`](audit/modules/StableContent.md)) |
| `halted_stable_not_protected` | 283 | theorem | REFUTED (converse of sufficiency, over all `PState`) | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `restricted_step_inert_unfunded` | 299 | theorem | CONDITIONAL:`IsTraceExcludedEvent e = false`, Dec, `budget = 0` | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `restricted_replay_inert_unfunded` | 390 | theorem | CONDITIONAL:`RestrictedTrace`, Dec, `budget = 0` | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `unfunded_restricted_stable_not_protected` | 422 | theorem | VERIFIED_FINITE + CONDITIONAL theorem instance (restricted-fragment example; not a countermodel to the full converse, as the source says) | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `separation_breakable` | 438 | theorem | CONDITIONAL:the five named witness hypotheses | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `unprotected_separation_unstable` | 470 | theorem | VERIFIED_FINITE (`decide`) | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `quiescent_iff_protected_separated` | 507 | theorem | CONDITIONAL:Dec | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `quiescence_is_protected_separation` | 541 | theorem | CONDITIONAL:Dec | propext, Quot.sound | `Unit 62` — Substantive (`S`) |
| `quiescent_retained_protected_trace_stable` | 565 | theorem | CONDITIONAL:Dec, `quiescentP` | propext, Quot.sound | `Unit 62` — Substantive (`S`) |

### 5.72 `TraceAlgebra` (`lean4/Derivation/TraceAlgebra.lean`) — Root-imported — `Unit 66`

- **Audit appendix:** [`textbook/audit/modules/TraceAlgebra.md`](audit/modules/TraceAlgebra.md)
- **Auxiliary / omission justification:** Recommend omitting: `TRecord`/`WFRecord`/`LegalTrace` beyond a remark — no theorem uses the typed fields, and `replay_erases` is a statement about `Aligned` alone; `internal_blocks_cannot_supply_or_license` (teach the general `TransitionAlphabet` forms instead); `RepresentsZero` as a named definition (inline the example).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `postOf` | 86 | def | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `TRecord` | 285 | structure | ADMITTED (typed record) | n/a (definition) | `Unit 66` (Definition / Structure) |
| `WFRecord` | 297 | def (Prop) | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `Aligned` | 306 | def (Prop) | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `endState` | 311 | def | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `eraseTrace` | 315 | def | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `LegalTrace` | 317 | def (Prop) | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `licenseInsensitive` | 425 | def | ADMITTED (declared frame family) | n/a (definition) | `Unit 66` (Definition / Structure) |
| `budgetInsensitive` | 431 | def | ADMITTED (declared) | n/a (definition) | `Unit 66` (Definition / Structure) |
| `occInsensitive` | 438 | def | ADMITTED (declared) | n/a (definition) | `Unit 66` (Definition / Structure) |
| `wOneOcc` | 614 | def | ADMITTED (finite witness) | n/a (definition) | `Unit 66` (Definition / Structure) |
| `ReplayEqvOn` | 712 | def (Prop) | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `RepresentsZero` | 717 | def (Prop) | ADMITTED (declared scope) | n/a (definition) | `Unit 66` (Definition / Structure) |
| `Rw` | 749 | inductive (Prop) | ADMITTED (declared rewrite system) | n/a (definition) | `Unit 66` (Definition / Structure) |
| `RwStar` | 754 | inductive (Prop) | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `consNF` | 790 | def | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `nf` | 794 | def | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `noRedex` | 798 | def | ADMITTED | n/a (definition) | `Unit 66` (Definition / Structure) |
| `hfalse` | 80 | theorem | FROZEN (private) | not in artifact | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `live_of_accepted` | 104 | theorem | CONDITIONAL:Acc | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `live_of_guardHolds` | 110 | theorem | CONDITIONAL:`guardHolds s e = true` | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `step_eq_ite` | 116 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `inert_iff_guard_fails` | 183 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `terminal_absorbs` | 194 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `replayP_halted` | 197 | theorem | CONDITIONAL:`s.halted = true` | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `trace_absorbs` | 207 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `mem_append_singleton` | 219 | theorem | FROZEN (metatheory) | none | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `v_not_mem_map` | 225 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `colOk_false_of_mem` | 237 | theorem | CONDITIONAL:`t.obs = some cols`, `c ∈ cols` | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `refineOk_false_of_not_mem` | 245 | theorem | CONDITIONAL:`t.obs = some cols`, `v ∉ cols` | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `guardHolds_post_false` | 252 | theorem | CONDITIONAL:Acc | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `step_idem` | 328 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `retention_idem`, `terminal_idem` | 337, 341 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `replayP_cons` | 319 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `replay_erases` | 326 | theorem | CONDITIONAL:`Aligned s tr` | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `legal_trace_replays` | 338 | theorem | CONDITIONAL:`LegalTrace s tr` | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `ne_halt_of_licenseInsensitive` / `budget` / `occ` | 448–458 | theorem | CONDITIONAL:LI/BI/OI | propext | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `postOf_halted` | 460 | theorem | CONDITIONAL:`e ≠ halt` | propext | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `halted_frame` | 467 | theorem | CONDITIONAL:`e ≠ halt` | propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `postOf_occ`, `occ_unchanged` | 474, 481 | theorem | CONDITIONAL:OI | propext / propext, Quot.sound | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `guardHolds_licS`, `postOf_licS`, `frame_licS` | 490, 498, 507 | theorem | CONDITIONAL:LI | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `comm_setLicense` | 514 | theorem | CONDITIONAL:LI | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `guardHolds_budS`, `postOf_budS`, `frame_budS` | 528, 536, 544 | theorem | CONDITIONAL:BI | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `comm_setBudget` | 551 | theorem | CONDITIONAL:BI | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `comm_setBudget_setLicense` | 564 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `guardHolds_occS`, `postOf_occS`, `frame_occS` | 571, 579, 587 | theorem | CONDITIONAL:OI | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `comm_admitOcc` | 595 | theorem | CONDITIONAL:OI | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `noncomm_license_extension` | 620 | theorem | REFUTED (`decide`) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `noncomm_budget_extension` | 626 | theorem | REFUTED (`decide`) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `noncomm_terminal` | 632 | theorem | REFUTED (`decide`) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `noncomm_supply_retention` | 640 | theorem | REFUTED (`decide`) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `noncomm_same_store` | 647 | theorem | REFUTED (`decide`) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `same_store_observationally_equal` | 656 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `internal_trace_preserves_occ` / `_license` | 670, 679 | theorem | CONDITIONAL:all events non-env | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `internal_blocks_cannot_supply_or_license` | 691 | theorem | FROZEN (over all `s`, `b`) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `refusal_persists_step` / `_replay` | 705, 713 | theorem | CONDITIONAL:`(i,j) ∈ s.refusals` | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `refusal_not_erasable` | 724 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `replay_eqv_scoped` | 719 | theorem | FROZEN (over the declared class) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `replay_eqv_not_unscoped` | 729 | theorem | REFUTED (`decide`) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `rw_sound` | 762 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `rwStar_sound` | 776 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `rw_length` | 783 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `nf_halt`, `nf_cons_ne` | 807, 812 | theorem | FROZEN | none | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `consNF_idem`, `nf_idem_cons`, `nf_cons_congr` | 818, 837, 843 | theorem | FROZEN | none | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `rw_preserves_nf`, `rwStar_preserves_nf` | 850, 856 | theorem | FROZEN | none | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `noRedex_consNF`, `nf_noRedex` | 862, 881 | theorem | FROZEN | none / none | `Unit 66` — Substantive (`S`) |
| `noRedex_nf_eq` | 890 | theorem | CONDITIONAL:`noRedex l = true` | propext | `Unit 66` — Substantive (`S`) |
| `rwStar_cons`, `rwStar_to_nf` | 908, 915 | theorem | FROZEN | none | `Unit 66` — Substantive (`S`) |
| `rw_confluent` | 947 | theorem | FROZEN | none | `Unit 66` — Substantive (`S`) |
| `nf_unique` | 956 | theorem | CONDITIONAL:`noRedex a`, `noRedex b` | propext | `Unit 66` — Substantive (`S`) |
| `nf_sound` | 965 | theorem | FROZEN | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `rewrite_not_complete` | 975 | theorem | REFUTED (completeness of the two-rule system) | propext, Quot.sound | `Unit 66` — Substantive (`S`) |
| `ne_halt_of_budgetInsensitive` | (grouped in [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `ne_halt_of_occInsensitive` | (grouped in [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `internal_trace_preserves_license` | (grouped in [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |
| `refusal_persists_replay` | (grouped in [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 66` — Auxiliary (`A`, [`TraceAlgebra.md`](audit/modules/TraceAlgebra.md)) |

### 5.73 `TransitionAlphabet` (`lean4/Derivation/TransitionAlphabet.lean`) — Root-imported — `Unit 65`

- **Audit appendix:** [`textbook/audit/modules/TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)
- **Auxiliary / omission justification:** Recommend omitting: `sizeP` and `class_witness_sizes` (a reporting metric; minimality lives in Python); `dedup` (replace by the statement "13 distinct values"); the `Origin` naming history (teach `isEnvOwned` as a declared label and the refutation, not the legacy name).

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Accepted` | 78 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `occS`, `assS`, `witS`, `protS`, `obsS`, `refineS`, `colS`, `refuseS`, `budS`, `licS`, `haltS` | 104–127 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `guardHolds` | 170 | def | ADMITTED (declared; its agreement with `Accepted` is a theorem) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `ObstEffect` | 580 | inductive | ADMITTED (declared classifier; ordered: `removed` wins) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `ObstMove` | 589 | inductive | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `coarse` | 595 | def | ADMITTED (declared projection) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `gainedPairs`, `lostPairs` | 601, 604 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `obstEffect` | 607 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `FieldDelta` | 906 | structure | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `fieldDelta` | 918 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `fdOcc` … `fdHalted` | 929–948 | def (10) | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `GuardKind` | 1028 | inductive | ADMITTED (declared label) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `guardOf` | 1042 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `BudgetDelta` | 1055 | inductive | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `budgetDeltaOf` | 1061 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `Continuity` | 1066 | inductive | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `continuityOf` | 1071 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `Origin` | 1092 | inductive | ADMITTED (declared **policy label**, explicitly not provenance) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `originOf`, `isEnvOwned` | 1097, 1104 | def | ADMITTED (declared policy) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `Profile` | 1117 | structure | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `profileOf` | 1127 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `ClassSig` | 1142 | structure | ADMITTED (declared projection) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `sigOf` | 1150 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `EffectSig` | 1159 | structure | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `eraseGuard`, `effectSigOf` | 1166, 1169 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `WFClass` | 1180 | structure (Prop) | ADMITTED (declared class; shown replay-invariant) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `wfB` | 1184 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `wAssert`, `wRetain`, `wProtectQuiet`, `wProtectObstructing`, `wDeclareObstructing`, `wObstructed`, `wFunded`, `wRefine`, `wFundedUnlicensed`, `wRefineUnlicensed` | 1239–1287 | def (10) | ADMITTED (finite witnesses) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `outsideClass` | 1293 | def | ADMITTED (countermodel state) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `EffectClass` | 1308 | inductive | ADMITTED (declared table) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `classSig` | 1324 | def | ADMITTED (declared) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `classOf` | 1352 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `dedup` | 1592 | def | ADMITTED (metatheory helper) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `allClasses` | 1596 | def | ADMITTED | n/a (definition) | `Unit 65` (Definition / Structure) |
| `sizeP` | 1822 | def | ADMITTED (declared metric, used only to report witness sizes) | n/a (definition) | `Unit 65` (Definition / Structure) |
| `accepted_true_iff` | 80 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `accepted_false_iff` | 84 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `halted_accepts_nothing` | 91 | theorem | CONDITIONAL:`s.halted = true` | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `halt_inert_on_halted` | 97 | theorem | CONDITIONAL:`s.halted = true` | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `append_ne` | 129 | theorem | FROZEN (metatheory) | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `occS_ne`, `assS_ne`, `witS_ne`, `protS_ne`, `refuseS_ne` | 135–147 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obsS_ne` | 149 | theorem | CONDITIONAL:`s.obs = none` | propext | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `budS_ne` | 155 | theorem | CONDITIONAL:`n ≠ s.budget` | none | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `licS_ne` | 158 | theorem | CONDITIONAL:`b ≠ s.licensed` | none | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `haltS_ne` | 161 | theorem | CONDITIONAL:L | none | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `refineS_ne`, `colS_ne` | 167, 175 | theorem | CONDITIONAL:`0 < s.budget` | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `refineOk_declared`, `colOk_declared` | 196, 202 | theorem | CONDITIONAL:guard true | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `hfalse`, `hlive` | 208, 210 | theorem | FROZEN (private) | not in artifact | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_admitOcc_acc` / `_inert` | 213, 219 | theorem | CONDITIONAL:L + guard | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_assertWit_acc` / `_inert` | 224, 231 | theorem | CONDITIONAL:L + guard | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_admitWit_acc` / `_inert` | 239, 247 | theorem | CONDITIONAL:L + guard | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_protect_acc` / `_inert` | 255, 262 | theorem | CONDITIONAL:L + guard | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_declareObs_acc` / `_inert` | 269, 275 | theorem | CONDITIONAL:L + obs case | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_refineCol_acc` / `_inert` | 281, 290 | theorem | CONDITIONAL:L + guard | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_addCol_acc` / `_inert` | 297, 306 | theorem | CONDITIONAL:L + guard | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_refuse_acc` / `_inert` | 313, 320 | theorem | CONDITIONAL:L + guard | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_setBudget_live`, `step_setLicense_live` | 327, 332 | theorem | CONDITIONAL:L | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_halt_eq` | 338 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `accepted_eq_guardHolds` | 344 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `filter_notmem_eq_nil`, `filter_congr_mem`, `filter_all_true`, `filter_all_false`, `list_ne_nil_of_mem`, `isEmpty_not_of_ne` | 524–566 | theorem | FROZEN | propext / none | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_sub`, `obst_of_mem_obstructedPairs`, `mem_obstructedPairs` | 613–623 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `lost_nil_of_eq`, `gained_nil_of_eq`, `obstMove_inert_of_eq` | 626–643 | theorem | CONDITIONAL:`obstructedPairs t = obstructedPairs s` | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstEffect_split_of_inert` | 653 | theorem | CONDITIONAL:equal lists | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `obstructedPairs_eq_of_stores` | 670 | theorem | CONDITIONAL:three store equalities | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_occS/assS/refuseS/budS/licS/haltS` | 682–717 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_witS` | 723 | theorem | CONDITIONAL:PSW | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `obstructedPairs_protS` | 738 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `obstructedPairs_obsS` | 758 | theorem | CONDITIONAL:`obs = none`, PSW | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `sepP_append`, `zeroP_append_mono` | 781, 787 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_colS_sub`, `colS_lost_ne_nil`, `obstEffect_colS` | 796, 813, 841 | theorem | CONDITIONAL:`s.obs = some cols`, `colOk s c = true` | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `mem_map_refine`, `obstructedPairs_refineS_sub`, `refineS_lost_ne_nil`, `obstEffect_refineS` | 848–898 | theorem | CONDITIONAL:`s.obs = some cols`, `refineOk s v p = true` | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `bne_true_of_ne`, `map_replace_ne` | 950, 955 | theorem | FROZEN / CONDITIONAL:`v ∈ cols` | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_occS … fieldDelta_colS` | 970–1024 | theorem | CONDITIONAL:per-case (e.g. `n ≠ s.budget`, `0 < s.budget`, `v ∈ cols`) | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `continuityOf_live`, `continuityOf_halted` | 1074, 1078 | theorem | CONDITIONAL:halted value | none | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `isEnvOwned_iff_origin` | 1111 | theorem | FROZEN | propext | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `wf_of_wfB` | 1187 | theorem | CONDITIONAL:`wfB s = true` | propext, Quot.sound | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `protSubWit_step` | 1193 | theorem | CONDITIONAL:PSW | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `protSubWit_replay` | 1213 | theorem | FROZEN (over all event lists) | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `wf_of_replay` | 1228 | theorem | CONDITIONAL:replayed state live | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `sig_eq_classSig` | 1375 | theorem | CONDITIONAL:WF, Acc | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `classSig_inj` | 1580 | theorem | VERIFIED_FINITE (`decide` over 13×13) | none | `Unit 65` — Substantive (`S`) |
| `classSig_pairwise_distinct` | 1584 | theorem | VERIFIED_FINITE | none | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `exists_unique_class` | 1589 | theorem | CONDITIONAL:WF, Acc | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `allClasses_complete` | 1603 | theorem | VERIFIED_FINITE | propext | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `declared_codebook_size` | 1607 | theorem | VERIFIED_FINITE | propext | `Unit 65` — Substantive (`S`) |
| `guard_erased_codebook_size` | 1614 | theorem | VERIFIED_FINITE | propext | `Unit 65` — Substantive (`S`) |
| `classSig_not_right_congruent_occurrence` | 1622 | theorem | REFUTED (countermodel, `decide`) | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `classSig_not_right_congruent_budget` | 1634 | theorem | REFUTED (countermodel, `decide`) | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `refine_addCol_effect_merge` | 1647 | theorem | CONDITIONAL:WF×2, Acc×2 | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `refine_addCol_domain_countermodel` | 1660 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `preserved_untouched_not_invariant` | 1669 | theorem | REFUTED (the split is not a transition invariant) | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `budgetDelta_not_invariant` | 1679 | theorem | REFUTED (budget delta not an invariant of the constructor) | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `budgetDelta_of_funded_guard` | 1686 | theorem | CONDITIONAL:WF, Acc, guard kind | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `refuse_preserves` | 1729 | theorem | CONDITIONAL:WF, Acc | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `retention_creates_outside_class` | 1750 | theorem | VERIFIED_FINITE (countermodel to dropping PSW) | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `nextFamily_block_shape` | 1758 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `internal_family_no_occurrence_supply`, `_no_license_write`, `_no_terminal` | 1769–1781 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `internal_family_emits_budget_write` | 1789 | theorem | VERIFIED_FINITE (refutation witness) | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `env_ownership_claim_refuted` | 1793 | theorem | REFUTED | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `internal_family_env_only_unit_funding` | 1803 | theorem | FROZEN | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `nonEnv_preserves_occ_licensed` | 1818 | theorem | CONDITIONAL:`isEnvOwned e = false` | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `class_witnesses` | 1829 | theorem | VERIFIED_FINITE | propext, Quot.sound | `Unit 65` — Substantive (`S`) |
| `class_witness_sizes` | 1865 | theorem | VERIFIED_FINITE | none | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_admitOcc_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_assertWit_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_admitWit_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_protect_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_declareObs_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_refineCol_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_addCol_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `step_refuse_inert` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_assS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_refuseS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_budS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_licS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `obstructedPairs_haltS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_assS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_witS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_protS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_refuseS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_obsS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_budS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_licS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_haltS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `fieldDelta_refineS` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `internal_family_no_license_write` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |
| `internal_family_no_terminal` | (grouped in [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) | theorem | FROZEN | within {propext, Quot.sound} | `Unit 65` — Auxiliary (`A`, [`TransitionAlphabet.md`](audit/modules/TransitionAlphabet.md)) |

### 5.74 `TransitionTransport` (`lean4/Derivation/TransitionTransport.lean`) — Root-imported — `Unit 31`

- **Audit appendix:** [`textbook/audit/modules/TransitionTransport.md`](audit/modules/TransitionTransport.md)
- **Auxiliary / omission justification:** Omit: the forty auxiliary commutation lemmas from the main text; keep one worked case (`newInst`) of `applyItem_rename` to show where `padF_bound` enters.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `padF n f` | 53 | def | ADMITTED | n/a (definition) | `Unit 31` (Definition / Structure) |
| `DRen.pad σ m hm` | 97 | def | ADMITTED | n/a (definition) | `Unit 31` (Definition / Structure) |
| `mapReq f q` | 109 | def | ADMITTED (renormalising action on requirements) | n/a (definition) | `Unit 31` (Definition / Structure) |
| `renameRegimeR f r` | 117 | def | ADMITTED (the transition action; docstring: "the extension is forced" by `validResponse` reading `reqs`) | n/a (definition) | `Unit 31` (Definition / Structure) |
| `mapItem f` | 272 | def | ADMITTED (scope: datum bijections, identity on forms) | n/a (definition) | `Unit 31` (Definition / Structure) |
| `respond r i j δ` | 677 | def | ADMITTED (the Lean transition object) | n/a (definition) | `Unit 31` (Definition / Structure) |
| `TransStep r i j δ s` | 820 | def (Prop) | ADMITTED (declared relation, no selection) | n/a (definition) | `Unit 31` (Definition / Structure) |
| `formAritySum` | 910 | def | ADMITTED | n/a (definition) | `Unit 31` (Definition / Structure) |
| `regRegime` | 972 | def | ADMITTED | n/a (definition) | `Unit 31` (Definition / Structure) |
| `regSwapFun` | 975 | def | ADMITTED | n/a (definition) | `Unit 31` (Definition / Structure) |
| `regSwap` | 1000 | def | ADMITTED | n/a (definition) | `Unit 31` (Definition / Structure) |
| `padF_lt`, `padF_ge` | 56, 60 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `padF_fg`, `padF_gf` | 65, 72 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `padF_inj` | 79 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `padF_bound` | 86 | theorem | CONDITIONAL: `n ≤ m` | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `mapReq_cases` | 121 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `mapReq_ordered` | 128 | theorem | CONDITIONAL: `f` injective | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `mapReq_inj_ordered` | 139 | theorem | CONDITIONAL: injective `f`, both pairs ordered | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `mapReq_g_f` | 165 | theorem | CONDITIONAL: `i < j` | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `renameR_reqs_wf` | 185 | theorem | CONDITIONAL: `hn`, `hreq` | propext, Quot.sound | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `collapsed_reqs_irrel`, `separable_reqs_irrel` | 205, 209 | theorem | FROZEN (definitional) | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `collapsed_renameR` | 214 | theorem | CONDITIONAL: `hn` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `collapsed_symm`, `separable_symm` | 221, 261 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `separable_rename` | 228 | theorem | CONDITIONAL: `hn` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `separable_renameR` | 254 | theorem | CONDITIONAL: `hn` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `mapItem_pad_f_g` | 278 | theorem | FROZEN | propext, Quot.sound | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `insertNew_map_on` | 295 | theorem | CONDITIONAL: pointwise `hinj` | propext, Quot.sound | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `applyItem_data_mono`, `applyDelta_data_mono` | 310, 376 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `applyItem_reqs`, `applyDelta_reqs` | 341, 393 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `applyDelta_nil`, `applyDelta_cons` | 370, 372 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `applyItem_rename` | 415 | theorem | CONDITIONAL: `n ≤ r.data` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `applyDelta_rename` | 495 | theorem | CONDITIONAL: `n ≤ r.data` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `map_congr_mem` | 516 | theorem | FROZEN | none | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `DRen.inv_f`, `DRen.inv_g` | 526, 527 | theorem | FROZEN | in artifact (root 1417–1418), propext per artifact — not re-checked | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `mapReq_inv_pair` | 531 | theorem | CONDITIONAL: `hfg`, `i < j` | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `renameRegimeR_inv_pair` | 552 | theorem | CONDITIONAL: `hfg`, `hreq` (ordered) | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `renameRegimeR_g_f`, `renameRegimeR_pad_f_g` | 581, 586 | theorem | CONDITIONAL: ordered reqs | propext, Quot.sound | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `renameRegimeR_padF_agree` | 593 | theorem | CONDITIONAL: WF-data | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `rename_insts_bound` | 622 | theorem | CONDITIONAL: `hn`, `hinst` | propext, Quot.sound | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `stepE_impose_rename` | 635 | theorem | CONDITIONAL: `hn`, `hreq`, `i < j`, `j < r.data` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `respond_reqs_ordered` | 682 | theorem | CONDITIONAL: `hr` (ordered before) | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `respond_rename` | 711 | theorem | CONDITIONAL: WF-data, `i < j`, `j < r.data` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `validResponse_symm` | 744 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `validResponse_rename` | 751 | theorem | CONDITIONAL: WF-data, `i < r.data`, `j < r.data` | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `transStep_rename_fwd` | 828 | theorem | CONDITIONAL: WF-data | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `transStep_image_total` | 866 | theorem | CONDITIONAL: WF-data | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `mapItem_length` | 905 | theorem | FROZEN | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `formAritySum_map` | 918 | theorem | FROZEN | none | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `validCount_rename` | 937 | theorem | CONDITIONAL: WF-data, bounds, `hp`, `hq` (caller-supplied deciders) | propext, Quot.sound | `Unit 31` — Substantive (`S`) |
| `regSwapFun_invol`, `regSwapFun_bound` | 982, 991 | theorem | VERIFIED_FINITE (case split/`decide`) | none | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `one_unary_form_ctx_char` | 1010 | theorem | CONDITIONAL: `r.forms = [1]` | propext | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `reg_collapsed_01`, `reg_renamed_collapsed_01` | 1045, 1051 | theorem | VERIFIED_FINITE (via the context characterisation then `decide`) | propext, Quot.sound | `Unit 31` — Auxiliary (`A`, [`TransitionTransport.md`](audit/modules/TransitionTransport.md)) |
| `least_pair_selection_not_congruent` | 1064 | theorem | REFUTED (refutes congruence of index-least selection; VERIFIED_FINITE components) | propext, Quot.sound | `Unit 31` — Substantive (`S`) |

### 5.75 `WeightProfile` (`lean4/Derivation/WeightProfile.lean`) — Root-imported — `Unit 64`

- **Audit appendix:** [`textbook/audit/modules/WeightProfile.md`](audit/modules/WeightProfile.md)
- **Auxiliary / omission justification:** Recommend omitting: `decoratedCarrierShape_exists` (its only content is that an earlier proposal was vacuous; mention in one sentence); `ClaimedReadOutUniqueness` as a definition (state the refutation directly); the import of `Compression` (unused). If the textbook keeps a "where this sits" note, it must say the module is arithmetic on admitted decorations with no bridge to regimes, contexts or observers.

| Declaration | Line | Kind | Status Mark | Axioms | Coverage Role |
|---|---|---|---|---|---|
| `Weights` | 58 | abbrev | ADMITTED (an unbounded function treated as a datum; every theorem reads it only on a finite list `l`) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `CarrierList` | 63 | def (Prop) | ADMITTED (declared policy) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `total` | 69 | def | ADMITTED | n/a (definition) | `Unit 64` (Definition / Structure) |
| `SameProfile` | 125 | def (Prop) | ADMITTED | n/a (definition) | `Unit 64` (Definition / Structure) |
| `Presents` | 273 | def (Prop) | ADMITTED (declared presentation) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `sq` | 312 | def | ADMITTED (declared modulus) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `sqInt` | 341 | def | ADMITTED (declared fixture) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `SignedSquarePresents` | 344 | def (Prop) | ADMITTED | n/a (definition) | `Unit 64` (Definition / Structure) |
| `mixSum` | 350 | def | ADMITTED ("nothing forces this read-out; it is part of the fixture") | n/a (definition) | `Unit 64` (Definition / Structure) |
| `signedPlus`, `signedSplit`, `unitIntWeights` | 352–356 | def | ADMITTED (finite witnesses) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `readOut` | 395 | def | ADMITTED (declared linear read-out) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `ModulusBlind` | 398 | def (Prop) | ADMITTED | n/a (definition) | `Unit 64` (Definition / Structure) |
| `ClaimedReadOutUniqueness` | 480 | def (Prop) | ADMITTED (candidate claim) | n/a (definition) | `Unit 64` (Definition / Structure) |
| `duplicate_list_not_carrier` | 65 | theorem | VERIFIED_FINITE | propext | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `foldl_add_acc` | 72 | theorem | FROZEN (metatheory) | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `total_cons` | 82 | theorem | FROZEN | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `total_append` | 95 | theorem | FROZEN | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `total_scale` | 101 | theorem | FROZEN | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `total_ray` | 109 | theorem | CONDITIONAL:pointwise ray on `l` | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `profile_refl` | 128 | theorem | FROZEN | none | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `profile_symm` | 131 | theorem | FROZEN | none | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `profile_trans` | 136 | theorem | CONDITIONAL:Pv | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `profile_scale_raw` | 159 | theorem | FROZEN | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `profile_scale_positive` | 168 | theorem | CONDITIONAL:`0 < a`, Pw | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `profile_equivalence_positive` | 177 | theorem | CONDITIONAL:positive totals (only Pv used in the transitivity leg) | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `zero_scale_boundary` | 191 | theorem | FROZEN (the named hypothesis is not consumed) | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `profile_iff_ray` | 206 | theorem | CONDITIONAL:Pw, Pv | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `profile_support` | 236 | theorem | CONDITIONAL:Pw, Pv, SameProfile | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `profile_order` | 256 | theorem | CONDITIONAL:Pw, Pv, SameProfile | none | `Unit 64` — Substantive (`S`) |
| `profile_forgets_total` | 286 | theorem | VERIFIED_FINITE (witness) | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `total_congr` | 277 | theorem | CONDITIONAL:pointwise equality | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `presentation_profile_redundant` | 289 | theorem | CONDITIONAL:`Presents` (only its second conjunct is used) | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `presentations_agree_on_profile` | 298 | theorem | CONDITIONAL:two `Presents`, Pw | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `sq_mono` | 316 | theorem | CONDITIONAL:`c < d` | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `sq_injective` | 326 | theorem | FROZEN | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `unsigned_decoration_determined` | 334 | theorem | CONDITIONAL:two `Presents l sq _ w` (Nodup not used) | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `signed_square_presentations_split` | 361 | theorem | VERIFIED_FINITE (two-label witness) | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `presentation_scope` | 383 | theorem | CONDITIONAL:two `Presents l sq _ w` | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `sq_mul` | 402 | theorem | FROZEN (metatheory) | propext | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `sq_add_sub` | 408 | theorem | FROZEN (metatheory) | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |
| `descent_iff_subsingleton_support` | 423 | theorem | FROZEN (over all `a b : Int`) | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `decoratedCarrierShape_exists` | 465 | theorem | FROZEN (trivial witness; a `Type` existential in metatheory) | none | `Unit 64` — Substantive (`S`) |
| `claimedReadOutUniqueness_false` | 489 | theorem | REFUTED | propext, Quot.sound | `Unit 64` — Substantive (`S`) |
| `finite_scope_summary` | 503 | theorem | CONDITIONAL:Pw, Pv, `0 < a` | propext, Quot.sound | `Unit 64` — Auxiliary (`A`, [`WeightProfile.md`](audit/modules/WeightProfile.md)) |

