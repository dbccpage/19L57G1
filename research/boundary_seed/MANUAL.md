# MANUAL: operating the boundary derivation

`AuthorityEffect: None`.  Apparatus only.

## Declared readings, recorded before the first challenge

0. **Prior exposure is material.**  The instrument that opened this run
   drafted the seed in the same session after reviewing the sealed
   derivation and research trees, and remembers their vocabulary and
   results.  The Challenge 0 status records where remembered structure was
   used.  The tree may establish source isolation after the seed, but it is
   not a blind, clean-room, convergence, or independent-discovery receipt.
   The scan enforces only checked byte populations and patterns.
1. **The seed's author and the first session coincide.**  Later challenges
   are intended to open in fresh sessions with nothing beyond the five
   named contract sections and the seed, but this does not erase the
   inherited prior-exposure ceiling.
2. **Two-ness is not assumed of the sides.**  Reading U and reading O are
   carried as separate towers; a result that holds under one and not the
   other is stated under its reading in the same sentence.

## Commands

From the repository root, for a challenge `<k>`:

```text
python research/boundary_seed/verify_pins.py
python research/boundary_seed/run_challenge<k>.py
cd research/boundary_seed && python -m unittest discover -s tests -p "test_*.py" && python -m mypy && cd ../..
cd research/boundary_seed && python -m coverage erase && python -m coverage run -m unittest discover -s tests -p "test_*.py" && python -m coverage json -q && python check_coverage.py && cd ../..
python research/boundary_seed/verify_lean.py
python ci/check_prose_watchlist.py
python -m pytest tests/test_primitive_contact.py -q -p no:cacheprovider
```

`verify_lean.py` first requires a successful clean, builds the tree's Lean
package, scans every
`.lean` file for the forbidden tokens as text, requires every axiom
report to lie within `{propext, Quot.sound}`, and compares the reports
with `lean/axioms.txt`; `--regen` rewrites that log deliberately and
never under a live injection.  The research job runs the pins, the tests
under coverage with the receipt regeneration and the blindness scan, and
strict typing; the Lean package is a manual receipt.

`verify_pins.py` compares working, index, HEAD, and committed-history bytes
for the seed and frozen predictions.  The source-isolation test likewise
checks working, index, and history bytes and fails on undecodable content.
A working or staged `FREEZE.md` does not retire the scan.  The current rule
retires it at a reachable committed marker; that rule does not validate the
marker as a complete hash manifest, so comparison remains blocked until a
parent-tree or explicit-exclusion protocol is defined and verified.

## Session protocol

Read the handoff, the seed, `PLAN.md`, this file, and the latest
challenge's `STATUS.md`; close at most one challenge or continuation
stage; write the handoff; never merge.

## Injection record

A gate is proved by failing on the exact defect it exists to catch, with
the failure naming the injected object, and by recovering when the
injection is reversed.  Receipts are never regenerated while an
injection is live.

| challenge | gate | injection | observed failure |
|---|---|---|---|
| 0 | blindness scan (`tests/test_blind.py`) | stray `zzz_probe.md` in the write root carrying an assembled citation into the sealed paper | `FAIL: test_write_root_is_blind_before_the_freeze` naming `research\boundary_seed\zzz_probe.md:1: citation into the sealed paper`, exit 1; 10 tests OK after deletion |
| 0 | receipt byte-identity (`test_committed_receipt_matches_the_renderer`) | `authority_effect` changed from `None` to `Some` in the committed receipt | the test failed showing the differing bytes, exit 1; OK after the original bytes were restored |
| 0 | frozen-prediction pin (`verify_pins.py`) | one byte appended to `challenge0/PREDICTIONS.md` | `FAIL: working copy of challenge0/PREDICTIONS.md: 1e15d854… wanted a03ee812…`, exit 1; `pins ok` after restore |
| 0 | axiom log (`verify_lean.py`) | the `supply_no_op` report dropped from `lean/axioms.txt` | `FAIL: axiom reports differ between the fresh build and lean/axioms.txt`, exit 1; `lean ok: 13 axiom reports` after restore |
| 0 | coverage gate (`check_coverage.py`) | `coverage.json` removed | `FAIL: coverage.json missing; run coverage from inside the tree first`, exit 1; the old recovery output mislabeled combined 98.09% as line coverage and is withdrawn below |
| 0 | forbidden-token scan (found live, not injected) | the Lean event constructor was first named with the forbidden admission word | `FAIL: lean\BoundarySeed\Basic.lean:34: forbidden token …` on four lines, exit 1; the constructor became `place` and the scan passed |
| 0 | census test (found live, not injected) | the reflection census compared regimes with their tokens | `test_census_rows`: `False is not true` on `fixed_iff_equal_counts`; the comparison now forgets tokens and the law holds to four marks |
| 0 review repair | frozen-file portability (found live) | clean Windows checkout converted the un-attributed prediction blob to CRLF | working sha256 `02f6ea78…` differed from pinned `a03ee812…`; `-text` attributes restore byte identity |
| 0 review repair | independent coverage arithmetic | synthetic totals report 94/100 lines and 100/100 branches while `percent_covered` says 97 | `test_combined_percent_cannot_rescue_low_line_coverage` returns line 94.00%, branch 100.00%; the repaired full suite is 53 passed at line 100.00%, branch 100.00% |
| 0 review repair | source-isolation parser probes | nested and Windows paths, lowercase Lean names, nested seed, non-UTF-8 bytes, and staged/history populations | 14 focused source-isolation/coverage-gate probes pass; malformed bytes and protected references fail closed by name |

The first five injected rows record the original Challenge 0 run and retain
their then-current counts.  The review-repair rows record the later
adversaries; current whole-tree counts are reported in `challenge0/STATUS.md`.
