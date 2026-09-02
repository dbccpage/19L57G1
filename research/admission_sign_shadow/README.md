# Admission-to-sign-shadow import audit

`AuthorityEffect: None`.

This is post-seal research. It does not amend, copy, rebuild, or renew the
sealed derivation. The only write surface is
`research/admission_sign_shadow/`. `SOURCE_MANIFEST.json` pins the exact base,
frozen object, source blobs, trees, and toolchain declaration used for this
audit.

## Claim ceiling

The package proves three local results.

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

These results isolate the cheapest imports. They do not remove them.

## Typed boundary

The local `ReportSection X Q report` is a right inverse of one report map. The
local `NaturalChoice F` is an observer-indexed family that commutes with every
declared transport. They are different types. `AdapterKernel` states the extra
query, conversion, and commuting data needed to obtain the latter from the
former. A countermodel proves that a report section need not provide such a
kernel; a converse countermodel proves that a natural choice need not provide
a report section.

## Imports and declarations

| Item | Classification | Reason |
|---|---|---|
| frozen pair to local two-history correspondence | imported | exact source identity does not prove semantic correspondence |
| operational nontriviality | imported | the trivial character satisfies every character law |
| occurrence history | declared model | canonical admission deduplicates tokens |
| count-to-integer unit calibration | imported | count laws do not choose an integer encoding |
| polarity-to-integer calibration | declared input | the local connector consumes it explicitly |
| mixing map | declared input | coordinate squares alone do not determine it |
| report-section to natural-choice adapter | open | the available types do not determine one |

## Nonclaims

- The local `HistoryClass` is not asserted to be the frozen history type.
- A pinned source blob is not a compiled cross-package theorem.
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
python -m mypy --config-file pyproject.toml
python build_receipt.py --check
```

The deterministic outputs live in `receipts/`. The exact local results and
remaining imports are enumerated in `CLAIM_LEDGER.md`; `STATUS.md` records the
terminal verdict.
