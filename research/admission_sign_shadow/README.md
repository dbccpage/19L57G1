# Admission-to-sign-shadow import audit

`AuthorityEffect: None`.

This is post-seal research. It does not amend, rebuild, or renew the sealed
derivation, and it places no frozen source in the tracked research package.
Compatibility builds materialize the exact frozen tree only in a temporary
directory that is removed on exit. The only write surface is
`research/admission_sign_shadow/`. `SOURCE_MANIFEST.json` separately pins the
exact post-seal source base, current publication base, frozen object, source
blobs, trees, and toolchain declaration used for this audit.

## Claim ceiling

The initial stage proved three local results.

1. A reconstructed two-history exchange is a free two-point action. Its
   characters are exactly the trivial character and the sign character. The
   character laws alone do not choose between them. If operational
   nontriviality is supplied, exchange maps uniquely to negative polarity;
   fixing a basepoint removes the remaining global-label convention.
2. Canonical ordered deduplication does not determine occurrence count. In a
   separately declared occurrence presentation, count has zero, append, and
   reordering laws. An integer count encoding becomes unique only after the
   zero, additive, and unit calibration laws are supplied.
3. Given an imported same-erasure exchange pair, imported operational
   nontriviality, a declared polarity-to-integer calibration, and a declared
   mixer, the induced integer pairs have equal coordinate squares and
   different mixed readouts. Collapsed pairs, unequal endpoints, the trivial
   character, a flat mixer, and a three-point mutation block the corresponding
   stronger claims.

The bridge tournament then compiled three lanes against the exact frozen
interfaces:

1. The two frozen histories and token-aware endpoints differ, while their
   erased endpoints agree. A chosen post-seal equivalence to the local pair is
   proved, but no frozen exchange authorization or unique orientation follows.
2. A retained exact `List TEvent` produces deterministic occurrence records,
   count, and canonical forgetting. Duplicate admission proves that no
   endpoint-only recovery exists. Zero and additivity do not select an integer
   unit.
3. A kernel with `query`, report-fibre `pairOf`, and exact `mapPair`
   commutation produces the actual frozen `Sec`/`IsNatural` types. A
   fixed-point-free actual family proves that bare report-section data cannot
   produce that kernel.

These results produce exact bridge types and close several stronger claims
negatively. They do not close the zero-import end-to-end connector.

## Typed boundary

The local `ReportSection X Q report` is a right inverse of one report map. The
local `NaturalChoice F` is an observer-indexed family that commutes with every
declared transport. They are different types. `AdapterKernel` states the extra
query, conversion, and commuting data needed to obtain the latter from the
former. A countermodel proves that a report section need not provide such a
kernel; a converse countermodel proves that a natural choice need not provide
a report section.

`ActualSectionAdapter.Kernel` repeats that boundary on the exact frozen
`PresentationNaturality.Family`, `Sec`, and `IsNatural` types. Its report fibre
makes the right-inverse proof operational rather than decorative.

## Imports and declarations

| Item | Classification | Reason |
|---|---|---|
| frozen observed pair facts | proved | exact frozen distinctness and erased equality compile |
| chosen pair equivalence | proved post-seal choice | existence is proved; source authorization and uniqueness are not |
| operational nontriviality | imported for sign; refuted as forced | the trivial character satisfies every character law |
| occurrence history from retained trace | proved | exact `TEvent` projection; not recoverable from endpoint |
| retained-trace connector integration | open | current downstream connector does not carry `List TEvent` |
| count-to-integer unit calibration | imported; refuted as forced | every integer scale satisfies zero and additivity |
| polarity-to-integer calibration | declared input | the local connector consumes it explicitly |
| mixing map | declared input | coordinate squares alone do not determine it |
| actual section adapter type | conditional theorem | exact kernel compiles when its fields are supplied |
| actual adapter fields | open | report right inverse does not determine query, pair, or commutation |

## Nonclaims

- The local `HistoryClass` is not definitionally the frozen history type.
- A chosen bijection is not source authorization, canonical orientation, or
  an object-language event.
- A pinned source blob is not a compiled cross-package theorem; the exact
  compatibility receipt is the build evidence.
- Occurrence multiplicity is not recovered from canonical admission.
- Character laws do not derive operational nontriviality.
- The two-history theorem does not extend automatically to larger carriers.
- No wider semantic interpretation, completion, scalar action, or uniqueness
  result is claimed.
- No post-seal construction changes the sealed object or its receipts.

## Replay

Run from this directory with the Python environment used by the machine
receipt:

```powershell
python source_manifest.py --check
python -m unittest discover -s . -p "test_*.py"
python run_connector.py --check
python verify_lean.py --check
python verify_frozen_compatibility.py --check
python -m unittest discover -s tournament/lanes/occurrence -p "test_*.py"
python -m mypy --config-file pyproject.toml
python build_receipt.py --check
```

`source_manifest.py --check` is the permanent source-identity replay. During
branch review, run `source_manifest.py --check-scope` as the separate
publication-base path-confinement audit. Keeping that audit explicit prevents
later unrelated commits on `main` from invalidating this package's source
receipt.

The deterministic outputs live in `receipts/`. The proof-tournament signature
lock and sparse packet ledger live in `tournament/`. The exact results and
remaining imports are enumerated in `CLAIM_LEDGER.md`; `STATUS.md` records the
terminal verdict.

`receipts/connector.json` is the byte-stable stage-one local-connector
subreceipt and therefore retains its original
`IMPORT_ISOLATED_BUT_NOT_REMOVED` terminal. The current package terminal is
the one in `receipts/machine_receipt.json`.
