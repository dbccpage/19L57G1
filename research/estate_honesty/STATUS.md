# estate_honesty: status

AuthorityEffect: None.

- **Gate 11 Status**: Not in Gate 11.
- **Receipts**: Local receipts only.
- **Verification**: Verified via local Python test suite (`test_estate_honesty.py`).
- **Census scope**: The frozen `ESTATE_AUDIT_REPORT.md` and `audit_summary.json` cover the 48 trees present at audit time. The `audit_estate.py` script dynamically discovers trees from `research/README.md` on each run, so future runs will reflect the current tree count.

## 2026-09-18: the audit numbers are a dated record

- **The snapshot is historical.** `audit_summary.json` and `ESTATE_AUDIT_REPORT.md`
  are the 2026-09-10 audit: 48 trees, 523 root tests collected over 41 files
  against a root `README.md` row of 481, and 1530 kernel axiom reports. They do
  not describe the estate today, and `test_estate_honesty.py` tests them only
  as that record (`test_dated_snapshot_20260910`).
- **Live counts are no longer compared with frozen literals.** Four tests did
  that: 56 trees, 43 local receipts, 523 collected / 41 files / README 481, and
  1530 reports / 75 modules. At `827bf983` the first three failed (103 trees,
  90 local receipts, 598 collected) with nothing wrong in the estate. The live
  path is now tested for parser health (root collection succeeds, its per-file
  counts equal an independent nodeid read, the tree census equals the generated
  table in `research/README.md`, report counts are non-zero) and for drift
  arithmetic (drift = current - README), whatever the populations are.
- **No silent fallback.** `audit_estate.py` used to substitute 41 files / 481
  collected when it could not parse the Tests row of the root `README.md`; it
  now raises.
- **Withdrawn.** Section 3.1 of `ESTATE_AUDIT_REPORT.md` says the root
  `README.md` is "under blind seal". It is not: the seal contract in `CLAUDE.md`
  names `prompt/`, `paper/`, `code/`, `lean4/Derivation/` and `artifacts/`. The
  report is left as written because it is the dated record; the generator no
  longer says it.
- `audit_estate.py --write` overwrites the dated record, and
  `test_dated_snapshot_20260910` then fails by design.
