# Audit of the frozen Genesis derivation

**AuthorityEffect: None.** This folder records an audit; it changes nothing
in the sealed derivation and authorizes nothing. Every verdict below is a
reading of `lean4/Derivation/` as it stands, checked against the artifact,
the paper and the ledger, and reproducible from the files named.

## Scope and method

- **Population.** The 75 tracked modules under `lean4/Derivation/` plus the
  root `lean4/Derivation.lean`. The root directly imports 62 modules; its import closure contains 63. The remaining 12 are
  parked (imported by `lean4/ParkedAudit.lean`, the second default target,
  so they build and report axioms under plain `lake build`). All 75 have a
  record in [`modules/`](modules/); none is omitted.
- **Snapshot.** Records were written against commit
  `33100245bb687b8242262279758bcc101ff2b5af` and carry the file's line count
  and the first 16 hex digits of its SHA-256. At the branch head
  `461e6d47ee53cf89b7fac57f6e1b653f3ec6eadf` (based on `main` at
  `7631e25`), `git diff --stat 33100245 HEAD -- lean4/Derivation
  lean4/Derivation.lean artifacts/lean_axioms.txt` is empty: the audited
  bytes are the current bytes.
- **Inventory.** [`inventory.py`](inventory.py) (a read-only script) produced
  [`inventory.json`](inventory.json): per module the imports, namespaces,
  declaration counts and theorem names; 1 685 theorems over 30 978 lines.
- **Record shape.** Each record has a header table (path, commit, hash,
  lines, root import, imports, declarations, axiom reports, forbidden-token
  scan) and eleven sections: 1 mathematical purpose; 2 definitions and
  structures, each marked FROZEN / POST_FREEZE_PROVED / CONDITIONAL /
  VERIFIED_FINITE / REFUTED / ADMITTED / OPEN; 3 theorems with informal
  statement, mark, axioms, and whether substantive (S) or auxiliary (A);
  4 external and admitted assumptions, with the eight-point smuggling
  checklist (unearned identity, unrestricted external universe, unbounded
  function, silent observer, unspecified presentation correspondence, cost
  function, admitted condition described as forced, finite computation
  presented as universal); 5 derived consequences (consumers, ledger,
  paper); 6 counterexamples and limitations; 7 axiom dependencies; 8
  verification status; 9 related Python; 10 textbook placement proposal;
  11 interpretation findings, each classified PROOF DEFECT, INTERPRETATION
  DEFECT, note, or no defect. These are the brief's fourteen fields with
  "dependencies" split between the header and section 5.
- **Probes.** Where a reading could not be settled from the text, a small
  Lean file was compiled against the built library. The eighteen probes are
  in [`probes/`](probes/), grouped by batch (A–F2). They are book Lean: not
  part of Genesis's build, inventory or gates, and they add no theorem to
  the frozen derivation.

## Verification receipt

| item | value |
|---|---|
| Command | `lake build` in `lean4/` (both default targets, `Derivation` and `ParkedAudit`) |
| Toolchain | Lean 4.33.0 (`d8b18978322de05a8f3dba51ef03cf5461676c17`), Lake from the same release tarball, Linux x86_64 |
| Tree | `461e6d47ee53cf89b7fac57f6e1b653f3ec6eadf`; sealed paths byte-identical to `33100245` |
| Exit code | 0 (last line of [`lake_build_receipt.log`](lake_build_receipt.log)) |
| Build | 80 jobs, replayed from this session's earlier full build of the same sources; one pre-existing linter warning (`Progress.lean:31`, `simpa`) |
| Axiom reports | 1 530 `#print axioms` lines in the log |
| `python ci/check_lean_audit.py textbook/audit/lake_build_receipt.log` | exit 0: "77 sources, 1530 axiom reports, axioms within ['Quot.sound', 'propext']" |
| `python ci/check_axiom_report.py textbook/audit/lake_build_receipt.log` | exit 0: "axiom reports match (1530 theorems; name-blind count agrees at 1530)" |
| Forbidden tokens | every record's header scan found none; the gate's own pattern is `^\s*axiom\s` plus `sorry`, `admit`, `unsafe`, `partial` over whole files |
| Not run | hosted CI (none exists, by the author's ruling); `python -m pytest` for the whole repository is reported with the textbook gates, not here |

This receipt is a local run on Linux. The repository's primary platform is
Windows; the same commands run there unchanged (`lake build` from `lean4\`,
then the two `ci\check_*.py` scripts on the log).

## Index

Columns: root import; lines; theorems; axiom census of the module's theorems
as matched by name to `artifacts/lean_axioms.txt` by the index script
(1517 of 1 685 matched; the unmatched are theorems inside nested
namespaces or sections that the simple name join misses, and each record's
header field is the authoritative count); whether the record classifies a
PROOF DEFECT; how many INTERPRETATION DEFECT classifications it carries.

| module | root | lines | thms | axioms (none / propext / Quot.sound / both) | proof defect | interp. defects |
|---|---|---|---|---|---|---|
| [Apartness](modules/Apartness.md) | yes | 338 | 28 | 22 none / 3 propext / 3 Quot.sound / 0 both | - | - |
| [Attachment](modules/Attachment.md) | yes | 1173 | 54 | 4 none / 7 propext / 0 Quot.sound / 43 both | - | 1 |
| [Basic](modules/Basic.md) | yes | 218 | 7 | 0 none / 1 propext / 0 Quot.sound / 0 both / 6 not in artifact | - | 1 |
| [BoundaryCancellation](modules/BoundaryCancellation.md) | yes | 662 | 37 | 3 none / 4 propext / 0 Quot.sound / 30 both | - | - |
| [Breaking](modules/Breaking.md) | yes | 446 | 15 | 7 none / 0 propext / 0 Quot.sound / 0 both / 8 not in artifact | - | 1 |
| [Bridge](modules/Bridge.md) | yes | 317 | 12 | 4 none / 0 propext / 0 Quot.sound / 7 both / 1 not in artifact | - | 2 |
| [CapacityBound](modules/CapacityBound.md) | yes | 255 | 10 | 1 none / 1 propext / 0 Quot.sound / 6 both / 2 not in artifact | - | 2 |
| [ClosureSymmetry](modules/ClosureSymmetry.md) | yes | 167 | 7 | 0 none / 5 propext / 1 Quot.sound / 1 both | - | 1 |
| [Completion](modules/Completion.md) | yes | 530 | 22 | 2 none / 1 propext / 0 Quot.sound / 19 both | - | 1 |
| [Composing](modules/Composing.md) | no (parked) | 229 | 7 | 7 none / 0 propext / 0 Quot.sound / 0 both | - | 1 |
| [Compression](modules/Compression.md) | yes | 788 | 38 | 12 none / 2 propext / 4 Quot.sound / 4 both / 16 not in artifact | - | 2 |
| [Constitution](modules/Constitution.md) | yes | 394 | 16 | 2 none / 1 propext / 0 Quot.sound / 13 both | - | 2 |
| [ContactBridge](modules/ContactBridge.md) | yes | 711 | 35 | 29 none / 1 propext / 1 Quot.sound / 4 both | - | 3 |
| [ContactKernel](modules/ContactKernel.md) | yes | 1026 | 53 | 41 none / 4 propext / 5 Quot.sound / 3 both | - | 3 |
| [ControllerCategory](modules/ControllerCategory.md) | yes | 775 | 63 | 16 none / 1 propext / 0 Quot.sound / 46 both | - | 3 |
| [CountTransport](modules/CountTransport.md) | yes | 307 | 13 | 0 none / 0 propext / 0 Quot.sound / 8 both / 5 not in artifact | - | 1 |
| [Counting](modules/Counting.md) | yes | 87 | 4 | 0 none / 0 propext / 0 Quot.sound / 4 both | - | - |
| [DiffAnchor](modules/DiffAnchor.md) | no (parked) | 74 | 3 | 0 none / 0 propext / 0 Quot.sound / 3 both | - | 2 |
| [DiffAnchorCompat](modules/DiffAnchorCompat.md) | no (parked) | 18 | 0 | 0 none / 0 propext / 0 Quot.sound / 0 both | - | - |
| [DiffInterface](modules/DiffInterface.md) | yes | 762 | 35 | 17 none / 1 propext / 1 Quot.sound / 16 both | - | 3 |
| [EndogenousFidelityGenerator](modules/EndogenousFidelityGenerator.md) | yes | 110 | 6 | 3 none / 0 propext / 1 Quot.sound / 2 both | - | 1 |
| [Erasure](modules/Erasure.md) | yes | 162 | 4 | 0 none / 0 propext / 0 Quot.sound / 2 both / 2 not in artifact | - | - |
| [Ext](modules/Ext.md) | yes | 180 | 12 | 1 none / 6 propext / 0 Quot.sound / 0 both / 5 not in artifact | - | - |
| [FidelityClosure](modules/FidelityClosure.md) | yes | 235 | 11 | 6 none / 0 propext / 3 Quot.sound / 2 both | - | - |
| [FormRenaming](modules/FormRenaming.md) | no (parked) | 148 | 9 | 1 none / 4 propext / 0 Quot.sound / 3 both / 1 not in artifact | - | 1 |
| [FormTransport](modules/FormTransport.md) | no (parked) | 197 | 11 | 1 none / 6 propext / 0 Quot.sound / 4 both | - | 2 |
| [FormTransportCompat](modules/FormTransportCompat.md) | no (parked) | 24 | 0 | 0 none / 0 propext / 0 Quot.sound / 0 both | - | - |
| [G1Class](modules/G1Class.md) | yes | 46 | 3 | 0 none / 0 propext / 0 Quot.sound / 3 both | - | 1 |
| [Generator](modules/Generator.md) | yes | 297 | 16 | 0 none / 1 propext / 0 Quot.sound / 15 both | - | 1 |
| [GraphGenesis](modules/GraphGenesis.md) | yes | 721 | 28 | 2 none / 0 propext / 0 Quot.sound / 26 both | - | 1 |
| [HigherStructure](modules/HigherStructure.md) | yes | 817 | 40 | 1 none / 1 propext / 0 Quot.sound / 35 both / 3 not in artifact | - | 3 |
| [Horizon](modules/Horizon.md) | yes | 425 | 27 | 0 none / 0 propext / 0 Quot.sound / 10 both / 17 not in artifact | - | 1 |
| [Inertia](modules/Inertia.md) | yes | 95 | 10 | 2 none / 7 propext / 0 Quot.sound / 1 both | - | 2 |
| [Initiality](modules/Initiality.md) | yes | 172 | 11 | 1 none / 0 propext / 0 Quot.sound / 10 both | - | 2 |
| [InterpreterBoundary](modules/InterpreterBoundary.md) | yes | 395 | 15 | 4 none / 2 propext / 0 Quot.sound / 7 both / 2 not in artifact | - | 3 |
| [IsoBridge](modules/IsoBridge.md) | no (parked) | 76 | 0 | 0 none / 0 propext / 0 Quot.sound / 0 both | - | - |
| [IsoBridgeCompat](modules/IsoBridgeCompat.md) | no (parked) | 18 | 0 | 0 none / 0 propext / 0 Quot.sound / 0 both | - | - |
| [IsoCanon](modules/IsoCanon.md) | no (parked) | 233 | 10 | 0 none / 10 propext / 0 Quot.sound / 0 both | - | 1 |
| [IsoCanonCompat](modules/IsoCanonCompat.md) | no (parked) | 18 | 0 | 0 none / 0 propext / 0 Quot.sound / 0 both | - | - |
| [IsoCollapse](modules/IsoCollapse.md) | no (parked) | 178 | 8 | 0 none / 1 propext / 0 Quot.sound / 1 both / 6 not in artifact | - | 1 |
| [IsoCollapseCompat](modules/IsoCollapseCompat.md) | no (parked) | 18 | 0 | 0 none / 0 propext / 0 Quot.sound / 0 both | - | - |
| [LadderGeneral](modules/LadderGeneral.md) | yes | 330 | 13 | 2 none / 0 propext / 0 Quot.sound / 11 both | PROOF | - |
| [LocalStrategy](modules/LocalStrategy.md) | no (parked) | 263 | 23 | 1 none / 5 propext / 0 Quot.sound / 17 both | - | 3 |
| [Mention](modules/Mention.md) | yes | 200 | 7 | 1 none / 3 propext / 0 Quot.sound / 3 both | - | 2 |
| [Minimality](modules/Minimality.md) | yes | 488 | 26 | 1 none / 4 propext / 0 Quot.sound / 17 both / 4 not in artifact | - | 2 |
| [MinimalityF](modules/MinimalityF.md) | yes | 198 | 2 | 0 none / 0 propext / 0 Quot.sound / 2 both | - | - |
| [NoOutside](modules/NoOutside.md) | yes | 271 | 13 | 2 none / 0 propext / 0 Quot.sound / 10 both / 1 not in artifact | - | 2 |
| [NoOutsideFidelity](modules/NoOutsideFidelity.md) | yes | 106 | 6 | 0 none / 5 propext / 0 Quot.sound / 1 both | - | 1 |
| [ObsDescent](modules/ObsDescent.md) | yes | 540 | 37 | 10 none / 2 propext / 13 Quot.sound / 12 both | - | - |
| [ObserverInventory](modules/ObserverInventory.md) | yes | 232 | 17 | 11 none / 1 propext / 0 Quot.sound / 5 both | - | 1 |
| [Pigeonhole](modules/Pigeonhole.md) | yes | 233 | 11 | 1 none / 2 propext / 0 Quot.sound / 5 both / 4 not in artifact | - | - |
| [PresentationDescent](modules/PresentationDescent.md) | yes | 226 | 7 | 6 none / 1 propext / 0 Quot.sound / 0 both | - | 1 |
| [PresentationNaturality](modules/PresentationNaturality.md) | yes | 666 | 30 | 28 none / 0 propext / 1 Quot.sound / 0 both / 1 not in artifact | - | 2 |
| [PresentationRelativity](modules/PresentationRelativity.md) | yes | 638 | 34 | 2 none / 3 propext / 10 Quot.sound / 15 both / 4 not in artifact | - | - |
| [PrimDiff](modules/PrimDiff.md) | yes | 546 | 44 | 35 none / 4 propext / 0 Quot.sound / 5 both | - | 5 |
| [PrimitiveCats](modules/PrimitiveCats.md) | yes | 722 | 49 | 33 none / 3 propext / 7 Quot.sound / 6 both | - | 1 |
| [PrimitiveContact](modules/PrimitiveContact.md) | yes | 143 | 4 | 2 none / 0 propext / 1 Quot.sound / 0 both / 1 not in artifact | - | - |
| [PrimitiveCore](modules/PrimitiveCore.md) | yes | 919 | 129 | 76 none / 4 propext / 0 Quot.sound / 1 both / 48 not in artifact | - | 2 |
| [PrimitivePassage](modules/PrimitivePassage.md) | yes | 1299 | 58 | 2 none / 0 propext / 0 Quot.sound / 54 both / 3 not in artifact | - | 3 |
| [Progress](modules/Progress.md) | yes | 238 | 6 | 0 none / 1 propext / 0 Quot.sound / 1 both / 4 not in artifact | - | 1 |
| [Quot](modules/Quot.md) | yes | 38 | 3 | 0 none / 0 propext / 2 Quot.sound / 1 both | - | 1 |
| [QuotientRetention](modules/QuotientRetention.md) | yes | 144 | 9 | 2 none / 0 propext / 3 Quot.sound / 4 both | - | 1 |
| [Refusal](modules/Refusal.md) | yes | 290 | 18 | 0 none / 1 propext / 0 Quot.sound / 15 both / 2 not in artifact | - | 2 |
| [RefusalFrontier](modules/RefusalFrontier.md) | yes | 372 | 20 | 6 none / 5 propext / 0 Quot.sound / 9 both | - | 3 |
| [RenamingStructure](modules/RenamingStructure.md) | yes | 483 | 28 | 4 none / 1 propext / 0 Quot.sound / 23 both | - | - |
| [Represented](modules/Represented.md) | yes | 1364 | 65 | 2 none / 2 propext / 0 Quot.sound / 44 both / 17 not in artifact | - | 2 |
| [ResidualClosure](modules/ResidualClosure.md) | yes | 123 | 7 | 0 none / 0 propext / 4 Quot.sound / 3 both | - | - |
| [Rounds](modules/Rounds.md) | yes | 483 | 25 | 1 none / 11 propext / 0 Quot.sound / 9 both / 4 not in artifact | - | - |
| [RuleBridge](modules/RuleBridge.md) | yes | 269 | 8 | 0 none / 8 propext / 0 Quot.sound / 0 both | - | 1 |
| [SeparationCapacity](modules/SeparationCapacity.md) | yes | 239 | 14 | 0 none / 1 propext / 0 Quot.sound / 13 both | - | - |
| [StableContent](modules/StableContent.md) | yes | 583 | 18 | 0 none / 0 propext / 0 Quot.sound / 18 both | - | 1 |
| [TraceAlgebra](modules/TraceAlgebra.md) | yes | 1002 | 72 | 13 none / 10 propext / 0 Quot.sound / 48 both / 1 not in artifact | - | 3 |
| [TransitionAlphabet](modules/TransitionAlphabet.md) | yes | 1894 | 118 | 10 none / 9 propext / 0 Quot.sound / 97 both / 2 not in artifact | - | 3 |
| [TransitionTransport](modules/TransitionTransport.md) | yes | 1071 | 53 | 6 none / 26 propext / 0 Quot.sound / 21 both | - | 1 |
| [WeightProfile](modules/WeightProfile.md) | yes | 523 | 31 | 4 none / 2 propext / 0 Quot.sound / 25 both | - | 1 |

Totals over the matched theorems: 450 with no axioms, 184 `propext`
only, 60 `Quot.sound` only, 823 both. No theorem anywhere
depends on `Classical.choice` or any other axiom; the two gates above
confirm it over the full 1 530.

### The thirteen parked modules

`Composing`, `DiffAnchor`, `DiffAnchorCompat`, `FormRenaming`,
`FormTransport`, `FormTransportCompat`, `IsoBridge`, `IsoBridgeCompat`,
`IsoCanon`, `IsoCanonCompat`, `IsoCollapse`, `IsoCollapseCompat`,
`RenamingStructure`. Each record's header says which line of
`ParkedAudit.lean` imports it. The four `*Compat` modules begin with
`import Derivation` and therefore cannot be root-imported without a cycle;
that is why they are parked. The brief's note that `Composing` is imported
by neither root nor `ParkedAudit` is incorrect at this commit: it is
`ParkedAudit`'s first import, and its seven theorems are in the artifact
(record, header).

## Defect list

### PROOF DEFECT (one)

| module | theorem | finding | smallest counterexample | consequence |
|---|---|---|---|---|
| [LadderGeneral](modules/LadderGeneral.md) §11.1 | `d2_zero_dims_2_3_4` | Conjuncts 1 and 2 are vacuously true: `coeffN e (pushN (bdN t))` filters on `p.2 == e`, and `e` ranges over cells one dimension away from the chain's support, so the coefficient is `0` for every chain. Only conjunct 3 tests the right dimension. | Replace `bdN` by any map at all in conjunct 1; the conjunct still decides to `true` (probe `probes/E/lg_vacuity.lean`). | The theorem is a correct Lean statement whose first two conjuncts carry no information. The general theorem `BoundaryCancellation.d2_zero_unrestricted` covers what the docstring claims. No downstream theorem depends on the vacuous conjuncts. The ledger entry `CL-PD2-LADDER-GENERAL` should describe conjunct 3 only. Not altered in the frozen derivation; recorded here and in the record. |

Two further records write "PROOF DEFECT: none found" explicitly
(`ContactBridge` §11.6, `ContactKernel` §11.11); every other record's §11
ends with a vacuity check and names no proof defect.

### INTERPRETATION DEFECT (53 records carry at least one)

An interpretation defect is prose (docstring, header, paper, ledger or change
log) that claims more, less or other than the Lean statement proves, while
the Lean itself is sound. The frozen theorem is never the thing to change.
Grouped by kind; the record section gives the quoted prose, the Lean
statement and the smallest reading of the gap.

**Vacuity-adjacent or by-construction theorems presented as content.**
Completion §11.3 (`early_collapse_transports`); DiffInterface §11.1 (`cm_*`
countermodels hold because `guarded := fun _ _ => False`); Generator §11.3
(`valued_marks_collapse_generation`, distinct by `congrArg Prod.snd`);
ContactBridge §11.2 (`kernel_stage_no_obstruction` reads back
`retained := False`); ContactKernel §11.8 (policy read-backs); NoOutside
§11.2 (a general tautology presented as a lift); Represented §11.5
(`replay_deterministic`, flagged not a defect); PrimitiveCats §11.2,
PrimitiveContact §11.1 (renamings of `d2_initial`); DiffInterface §11.3
(two names, one theorem); FidelityClosure §11.3 (unused hypothesis by
design); WeightProfile §11.2 (unused hypothesis); PrimitiveCats §11.2
(unused `IrreflObj`).

**Scope words stronger than the statement** ("every", "never", "settled",
"universal", "strict hierarchy", "unique minimum", "rigid", "complete").
Bridge §11.1, §11.4; CapacityBound §11.1 (no `reflState` in the statement);
Constitution §11.1 (moderate: "represented as data" overreads
`interp_describe`), §11.2; ContactKernel §11.2 (categorical vocabulary);
HigherStructure §11.1, §11.2, §11.4; Initiality §11.1, §11.3;
InterpreterBoundary §11.1–§11.3; LocalStrategy §11.1 (minor-to-moderate:
"cycle", "member fires" for `¬ Clears S`), §11.2, §11.3; NoOutside §11.1;
NoOutsideFidelity §11.1; PresentationNaturality §11.1, §11.3; PrimDiff §11.3
(`const_presentation_unfaithful` has no presentation in it), §11.4;
PrimitiveCats §11.1; PrimitiveCore §11.1 (minimum-carrier claims);
PrimitivePassage §11.1–§11.3; Refusal §11.1–§11.4; RefusalFrontier §11.1
(`[theorem]` tag on a `[finite computation]` sentence), §11.2–§11.4;
SeparationCapacity §11.1 ("derived, not assumed" for a declared bound);
StableContent §11.1 ("only when"); TraceAlgebra §11.1–§11.4;
TransitionAlphabet §11.1 ("minimum", self-corrected in the source), §11.2;
WeightProfile §11.1; ObserverInventory §11.1; QuotientRetention §11.1
("exchange" never assumed); G1Class §11.1; Generator §11.2; Breaking §11.1
(the root prints seven, not all, of its theorems).

**Counts and cross-references that do not match.** TransitionAlphabet §11.3
(`CL-PD2-TRANSITION-CODEBOOK` says twelve for a theorem that proves 13 and
one that proves 12); CapacityBound §11.2 (header denies `LocalStrategy`
exists; it does and consumes `capacity_bound`); ContactBridge §11.1 and
ContactKernel §11.1 (header claims already corrected in the dependency map
or ledger but not in the module); DiffAnchor §11.2 (docstring says axioms
are verified by hand; the parked audit now reports them); PrimitiveCore
§11.2 (`matrixCells` rows are strings, so the row–theorem correspondence is
textual; Lean proves only the length); ContactKernel §11.7 (same for
`contactCells`); PresentationDescent §11.1 (`native_derivation_completion.md`
misdescribes `FaithfulCommonDescent`); ClosureSymmetry §11.2; Compression
§11.1, §11.2, §11.4 ("cost" is `List.length`, declared); Quot §11
(paper 10.5's "[theorem]" is exact; noted for the textbook's wording);
Minimality §11 (`mu1_minimum_not_unique` scope: reading L only; the paper's
prose lemma on `(2, 0)` deltas is not in Lean, now proved as book Lean in
`textbook/checks/u22_lean.py`).

**Finitude.** Horizon §11.2 ("at every horizon" is quantification over
Lean's `Nat`); InterpreterBoundary §11.4; HigherStructure §11.3
(`graph_growth`, "without bound"); Represented §11.1 (`wit_no_infinite`
quantifies over `Nat → Nat`), §11.3 (`setBudget` is unbounded supply);
PrimitivePassage §11.4 (`X := Nat` carrier); LadderGeneral §11.3. Each is a
place where the metatheory's `Nat`, function types or `Type` parameters
are used as if internal to the system; none is a proof defect, and 62 of
the 75 records carry a finitude flag or an explicit finitude check in §4.

## Assumption map

What the frozen derivation admits, by kind, with where it is admitted. The
records' §4 give the per-module detail; this is the cross-module view.

| kind | admitted where | how it is marked | notes |
|---|---|---|---|
| The grammar | `Basic.Item`, `Regime`, `stepE`, the guards (`i < j ∧ j < r.data`, the instance guard) | ADMITTED in `Basic` | every "exhaustive" case analysis is over this declared grammar |
| The two readings L and F | `Basic.R2L`, `R2F` | ADMITTED | theorems are stated per reading; `MinimalityF` repeats `mu2_unique` for F with the mention lemma |
| Cost measures | `mu1` (length), `mu2` (length, arity sum), `Compression`'s family length, `Represented`'s budget | ADMITTED (declared measures) | uniqueness and minimality results are measure-relative; records flag "cost" wherever the prose suggests it is derived |
| Sameness | `Minimality.Iso`, `IsoCanon`/`IsoCollapse` canonical forms, `Erasure`, the presentation-descent families | ADMITTED (definition 8 and its refinements) | tokens are forgotten by declaration; the parked `Iso*` modules study variants |
| Protected laws | `PrimDiff.Irrefl`, `Apartness.IsApart` (three laws), the guards in `Initiality`, `prot` in the passage | ADMITTED, with REFUTED derivations alongside (`irrefl_law_not_entailed`, the apartness countermodels) | the pattern throughout: a law is declared, what it buys is proved, and that it cannot be derived is proved |
| Finite carriers of record | `Unit`, `Bool`, `Fin 3`, `Fin n` for small `n`, concrete regimes | VERIFIED_FINITE | the records distinguish a theorem on `Bool` from a theorem on every carrier wherever prose blurs it |
| Metatheory types used as parameters | `X : Type`, `Nat` indices and horizons, `Nat → Nat` streams, arbitrary `f : α → β` | metatheory | the finitude flags above; the system never holds these objects |
| Library axioms | `propext` (from `decide` on `Prop`-valued data and `simp`), `Quot.sound` (from `funext` and list lemmas) | within the declared boundary | 1 530 of 1 530 reports inside `{propext, Quot.sound}`; `Classical.choice` nowhere |
| Observer | `kernelObs`, views, `ObserverInventory`'s two defect readings | ADMITTED where present; several modules are pre-observational by declaration | the records check "silently assumed observer" and find none; `NoOutside` proves the panel is data |
| Interpreter boundary | `InterpreterBoundary`, `Constitution` | OPEN as a boundary; the I-route theorems are about a declared class | the records keep the absolute boundary OPEN; the textbook does the same |

## What this audit does not do

- It does not alter the sealed derivation. The one PROOF DEFECT is recorded,
  not repaired; the repair, if the author wants one, is a ledger edit
  narrowing `CL-PD2-LADDER-GENERAL` to conjunct 3, or a post-freeze theorem
  outside the seal.
- It does not re-derive the paper. Section 5 of each record names the
  paper and ledger rows that cite the module; where a row was read and
  compared, §11 says so; where only a grep located it, the record says
  "not checked beyond the grep".
- It does not assess research trees. The audit population is the frozen
  derivation; `research/` is the textbook's Part V.

## How the records feed the textbook

Section 10 of every record proposes a lesson: prerequisites, the
substantive theorems, a title and the question answered, and the theorems
to omit as immediate corollaries. `textbook/derivation_coverage.md` will
map every module to its lesson or to a reason for omission, and the lesson
dependency graph is built from the §10 prerequisites.
