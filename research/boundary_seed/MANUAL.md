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

`verify_lean.py` scans every `.lean` file for the forbidden tokens as
text, requires every module under `lean/BoundarySeed/` to lie in the
root's transitive import closure (an unreached module is never
elaborated), then requires a successful clean, builds the tree's Lean
package, requires every axiom report to lie within `{propext,
Quot.sound}`, and compares the reports with `lean/axioms.txt`; `--regen` rewrites that log deliberately and
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
| 1 | frozen-prediction pin (`verify_pins.py`) | one byte appended to `challenge1/PREDICTIONS.md` | `FAIL: working copy of challenge1/PREDICTIONS.md: 22b94644… wanted 7cf17e56…`, exit 1; `pins ok: seed ba30bcd600d8 and 2 frozen prediction file(s)` after restore |
| 1 | receipt byte-identity (`test_committed_receipt_matches_the_renderer`, Challenge 1) | `authority_effect` changed from `None` to `Some` in the committed `receipts/challenge1.json` | the test failed showing the differing bytes, exit 1; OK after the original bytes were restored |
| 1 | workflow test-count grep | the fresh suite log matched against the stale `^Ran 53 tests in ` | exit 1; `^Ran 97 tests in ` exit 0 on the same log |
| 1 | axiom log (`verify_lean.py`) | the `replay_preserves_onSide` report dropped from `lean/axioms.txt` (48 lines) | `FAIL: axiom reports differ between the fresh build and lean/axioms.txt`, exit 1; `lean ok: 49 axiom reports` after restore |
| 1 | Lean import-closure census (`verify_lean.py`) | `lean/BoundarySeed/ZzzProbe.lean` added, imported by nothing | `FAIL: BoundarySeed.ZzzProbe is outside the root's import closure and is never elaborated`, exit 1; `lean ok: 49 axiom reports` after deletion; `test_planted_unreached_module_is_named` fixes the negative direction |
| 1 | Lean import-closure hole (found live, not injected) | `Challenge1.lean` written but not imported by the root | `lake build` reported `Build completed successfully` with the 20 Challenge 0 reports and never elaborated the new file; the root import and the census above close it |
| 1 | generator census (found live, not injected) | the candidate enumerator written into `model.py` with return type `list[AdmitMark]` | `test_no_state_event_generator_in_the_kernel`: `['one_step_admissions'] != []`, and the Challenge 0 receipt's byte identity failed with it; the enumerator moved to `challenge1.py`, the Challenge 0 receipt is unchanged |
| 1 | no-timestamp scan (found live, not injected) | the receipt key `candidates` | `AssertionError: 'date' unexpectedly found` from a substring match; the scan now matches whole words and asserts the key is present |
| 1 review repair | no-timestamp scan, the narrowing above (found live by review) | keys `build_date`, `run_timestamp`, `python_version` planted in a copy of the receipt | the whole-word scan `\b…\b` returned no hit on all three, `_` being a word character; the repaired scan, which forbids a watched word glued to letters, names `date`, `python`, `timestamp` on the same plant and nothing on the real receipt; `test_environment_scan_catches_planted_snake_case_keys` fixes both directions, and `test_challenge0.py` now uses the same pattern |
| 1 review repair | moving-admission refusal (found live by review) | `AdmitMark(a, 1)` replayed after `a` admitted on side 0 | the pre-repair kernel returned the regime unchanged with placement `(0,)`, the requested side discarded, so “an event that moves the admitted mark” could not fire; the repaired kernel raises `AdmissionError: mark 'a' is admitted on side 0; an admission naming side 1 would move it and is refused`, `certify` returns false, the receipt records the refusal, and `test_moving_admission_is_refused_by_name` and `test_c1_2_misses_when_a_moving_admission_is_accepted` fix both directions |
| 1 review repair | prediction scorer, literal clauses (found live by review) | C1-4 “the only event in the history” scored against a two-event history; C1-5 “the designation is by convention” scored as current-state designation of an admitted candidate | the scorer now reports each disputed clause on both readings: C1-4 `only_event_clause_status: MISSED`, `only_state_changing_event_status: HIT`, PARTIAL; C1-5 `current_state_designation_status: MISSED`, `facts_status: HIT`, PARTIAL; `test_c1_4_only_event_clause_is_scored_literally` shows HIT only for a one-event history and MISSED for two admissions, and `test_c1_5_designation_clause_hits_only_if_an_admitted_candidate_were_current` shows HIT only when the receipt says an admitted candidate is current |
| 1 review repair | receipt byte-identity (`test_committed_receipt_matches_the_renderer`, Challenge 1) | the kernel and metatheory repairs, with the committed receipt left stale | the test failed showing the differing bytes (3 failures in the suite); `run_challenge1.py` regenerated the receipt deliberately with no injection live, `run_challenge0.py` reported `unchanged: receipts\challenge0.json (5553 bytes)`, and the suite passed 106 |
| 1 review repair | axiom log (`verify_lean.py`), deliberate regeneration | six theorems added (`reflect_replay` and companions) | `wrote lean\axioms.txt: 55 reports` under `--regen`, then `lean ok: 55 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; no injection live |
| 1 review repair | workflow test-count grep | the fresh suite log matched against the stale `^Ran 97 tests in ` | exit 1; `^Ran 106 tests in ` exit 0 on the same log |
| 1 second review repair | prediction scorer, C1-2 literal clause (found live by review) | the parenthetical's other-side half labelled from the overall pass, with no clause fact | the pre-repair receipt read `readmission_clause_status: SHARPENED` beside `status: HIT`; the repaired scorer reads `either_side_readmission_clause_status: MISSED` and `status: PARTIAL` on the real receipt, and HIT only when every candidate's `moving_admission_accepted_and_inert` is true; `test_c1_2_either_side_clause_hits_only_when_every_moving_admission_is_accepted_and_inert` fixes both directions, and `test_moving_admission_fact_reads_accepted_and_inert_only_when_the_kernel_absorbs` shows the fact true only under an absorbing `step` |
| 1 second review repair | current-state designation fact (found live by review) | a caller history admitting a token `z`, no Challenge 1 candidate current | the pre-repair proxy `marks > 0` read True; the membership fact reads False, and `test_current_state_designation_is_candidate_membership` fixes it |
| 1 second review repair | receipt byte-identity (`test_committed_receipt_matches_the_renderer`, Challenge 1) | the scorer and fact repairs with the committed receipt left stale | the test failed showing the differing bytes (1 failure in 109); `run_challenge1.py` regenerated the receipt deliberately with no injection live (24663 bytes), `run_challenge0.py` reported `unchanged: receipts\challenge0.json (5553 bytes)`, and the suite passed 109 |
| 1 second review repair | axiom log (`verify_lean.py`) | `bounded_invariant_judgment_does_not_separate` added with its `#print axioms` line, the log left stale | `FAIL: axiom reports differ between the fresh build and lean/axioms.txt`, exit 1; then `wrote lean\axioms.txt: 56 reports` under `--regen` and `lean ok: 56 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; no injection live |
| 1 second review repair | workflow test-count grep | the fresh suite log matched against the stale `^Ran 106 tests in ` | exit 1; `^Ran 109 tests in ` exit 0 on the same log |
| 1 third review repair | receipt byte-identity (`test_committed_receipt_matches_the_renderer`, Challenge 1) | the scorer's `result_basis` for C1-1, C1-3, and C1-6, the `tally` key, and the C1-5 evidence wording, with the committed receipt left stale | the test failed showing the differing bytes (1 failure in 111); `run_challenge1.py` regenerated the receipt deliberately with no injection live (24663 to 26687 bytes), `run_challenge0.py` reported `unchanged: receipts\challenge0.json (5553 bytes)`, and the suite passed 111 |
| 1 third review repair | workflow test-count grep | the fresh suite log matched against the stale `^Ran 109 tests in ` | exit 1; `^Ran 111 tests in ` exit 0 on the same log |

The first five injected rows record the original Challenge 0 run and retain
their then-current counts.  The review-repair rows record the later
adversaries.  The Challenge 1 rows record that rung and its three review
repairs; current whole-tree counts are reported in the latest
`challenge<k>/STATUS.md`.
