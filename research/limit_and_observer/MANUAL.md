# research/limit_and_observer — manual

How to run everything, and the injection record.

AuthorityEffect: None.

## The battery, from the repository root

    python research/limit_and_observer/verify_pins.py
    cd research/limit_and_observer
    python -m unittest discover -s tests -p "test_*.py"
    python -m mypy
    python -m coverage erase
    python -m coverage run -m unittest discover -s tests -p "test_*.py"
    python -m coverage json -q
    python check_coverage.py
    python run_price.py
    python verify_prose.py
    cd ../..
    git diff --exit-code -- research/limit_and_observer/receipts
    python ci/check_prose_watchlist.py
    python -m pytest tests/test_primitive_contact.py -q -p no:cacheprovider
    git status --short

The Lean package is separate, and **manual**:

    cd research/limit_and_observer
    python verify_lean.py                # compare against the committed receipt
    python verify_lean.py --write        # regenerate it, deliberately

This package's `verify_lean.py` is run by **no gate**. Read a pass as
"a person ran it", never as "a gate enforced it". This statement makes no
claim about the other research packages.

It does three things a reader should not conflate. It scans every `.lean` file
as text for the forbidden tokens; it requires every module of the package to
lie inside the census root's import closure, which is the half Lean cannot see
because a module nothing imports is absent from the compiled environment; and
it compares the axiom census, emitted from that environment rather than from a
hand-written list, byte for byte against `receipts/lean_axioms.txt`.

## Notes that will save time

* **`coverage.json` is untracked and dated.** `check_coverage.py` refuses a
  report it cannot date and fails if any measured source is newer than the
  report. Touching a source without changing it fails until you regenerate,
  which is the safe direction.
* **The receipt must regenerate byte-identically.** `run_price.py` writes
  sorted keys, LF endings, no timestamp and no environment value.
  `run_price.py --check` regenerates in memory and compares exact bytes without
  writing the receipt; `git diff --exit-code -- receipts` checks tracked drift.
* **`receipts/**` and the two frozen texts are `-text`.** Never let an editor
  or a CRLF conversion rewrite them: it breaks the pins and the byte
  comparison at once. `verify_pins.py` checks the attribute and refuses CR
  bytes in a receipt.
* **Pins are canonical Git blob sha256**, `git show HEAD:<path> | sha256sum`,
  never the worktree file's digest. The two differ for every file under
  `code/` and `lean4/` in a CRLF checkout and agree only for `artifacts/**`.
* **The full suite takes a few minutes.** The population is rebuilt per test
  module; the pure functions are memoised inside a process, not across them.
* **`verify_prose.py` runs after `run_price.py`, never before.** It binds the
  numbers `FINDINGS.md`, `STATUS.md` and `CLAIM_LEDGER.md` publish to the
  receipt they claim to report, and a stale receipt would make it compare
  prose against yesterday's run. It has **no** regeneration switch on purpose:
  a pin regenerated under a live divergence adopts the divergence as the
  baseline, so a binding is moved by a deliberate edit or not at all.

## The injection record

A gate is not proved by being green. It is proved by failing on the exact
defect it exists to catch, with the failure naming the injected object, and by
recovering when the injection is reversed. Green before and after, with
nothing in between, shows only that the gate is quiet.

Receipts are **never** regenerated while an injection is live: regenerating
`receipts/price.json` or `receipts/lean_axioms.txt` under an injection adopts
the defect as the new baseline and destroys the test.

| gate | injection | observed failure |
|---|---|---|
| Source pin | changed the first byte of the pinned `code/derivation/observe.py` digest | `FAIL: hash mismatch for code/derivation/observe.py`, printing wanted and snapshot; exit 1, then 0 after reversal |
| Frozen text pin | changed one character of `PREDICTIONS.md` | `FAIL: hash mismatch for research/limit_and_observer/PREDICTIONS.md`, naming the file; exit 1, then 0 after reversal |
| Snapshot reachability | replaced the snapshot commit with a 40-hex id no object matches | `FAIL: snapshot ... is not reachable in this repository`; exit 1, then 0 after reversal |
| Snapshot exactness | replaced the snapshot commit with `HEAD` | `FAIL: source snapshot commit must be an exact 40-digit lowercase hex id`; exit 1, then 0 after reversal |
| Receipt CR refusal | wrote a CR byte into `receipts/price.json` | `FAIL: price.json contains CR bytes`; exit 1, then 0 after reversal |
| Calibration gate | changed the transcribed sealed F/`mu1` class count from 5 to 3 | `test_transcribed_sealed_answer_matches_the_pinned_artifact` failed against the committed artifact, and `test_calibration_reproduces_the_sealed_answer` reported the differing row; exit 1, then 0 after reversal |
| Quotient coarseness (found live, not injected) | the first calibration run, before the demand carried its imposed pair | reproduced every sealed cost and delta count but gave **3** classes where reading F's `mu1` answer has **5**. The sealed `_quotient` imposes the target before keying; carrying the imposed pair as a field of the demand fixed it |
| Enumerator certification (found live, not injected) | the first set-equality run of `sealed_prefixes` against `superset_prefixes` | `AssertionError` at three items in reading L, naming `(NewForm(arity=1), NewRuleAll(form=0), NewRuleAll(form=0))` and the arity-2 sibling as present in the superset and absent from the breadth search. Repaired by restating the sealed offer condition exactly in `admissible_shape`, **not** by widening the space |
| Block-count monotonicity (found live, not injected) | the first run of `test_a_strict_split_raises_the_block_count` over the population | `AssertionError: 1 not greater than or equal to 2` — under the parity aggregation adding a context **lowers** the block count. The refinement proof was narrowed to the monotone aggregations, the countermodel was kept as a test, and the chain bound for the other two is now reported as a bounded computation |
| Monotonicity census count (found live, not injected) | the first run of `test_no_move_shrinks_the_context_set` | `AssertionError: 1067 != 243` — the pre-freeze figure counted moves only from the states expanded during the breadth rounds. The census expands all 85. Recorded as a P-1 miss rather than the prediction being edited |
| Frozen-text custody (found live by injection) | appended one byte to `PREDICTIONS.md` in the worktree | the pin check stayed **green**, because it compares git objects at the snapshot and at HEAD and never looks at the working tree. The hole was real; `verify_pins.py` now hashes the frozen texts on disk and refuses tracked worktree changes, and the same injection then reports `FAIL: frozen input research/limit_and_observer/PREDICTIONS.md has worktree changes`, exit 1, then 0 after reversal |
| Enumerator certification, re-injected | removed the `admissible_shape` filter from `superset_prefixes` | the same two doubled-rule deltas reappeared and `test_prefixes_equal_the_superset_construction` failed, naming them; exit 1, then 0 after reversal |
| Width bound | offered a fourth `AddContext` to one reader | `AdmissionRefused: selection exceeds width 3`; the guard test fails if the bound is removed |
| Reader bound | offered a third `NewReader` | `AdmissionRefused: at most 2 readers per stated state` |
| Candidate budget | set the budget to 1 and enumerated | `CandidateBudgetRefused`, refused rather than truncated |
| Bijection budget | set the budget to 1 and keyed a state | `BijectionBudgetRefused: 6 candidate bijections exceed the declared budget 1` |
| Harness partition invariant | built a `Minimum` whose classes cover only one of two raw minima | `GradeRefused: the response classes must partition the raw minima` |
| Harness duplicate invariant | built a `Minimum` with the same delta twice in `raw_minima` | `GradeRefused: raw minima hold no duplicate` |
| Stage-locality exhaustiveness | passed an item carrying a `stage` field | `reads_only_the_stage` returned `False`, which is what makes LIM-F's content a real property rather than an unfolding |
| Vacuous finding | called `refuse_if_vacuous` with a count of zero | `VacuousFindingRefused: ... has a supporting count of zero and is refused as vacuous` |
| Lean forbidden token | wrote a line-leading `axiom` into a `.lean` file | `FAIL: forbidden token 'axiom ' at lean/LimitObserver.lean:<line>`; exit 1, then 0 after reversal |
| Lean axiom whitelist | proved a theorem by `Classical.em` | `FAIL: disallowed axioms ['Classical.choice']`, naming the declaration; exit 1, then 0 after reversal |
| Lean report pin | deleted one line from `receipts/lean_axioms.txt` | `FAIL: axiom reports differ between the build and the committed receipt`, printing both blocks; exit 1, then 0 after reversal |
| Receipt determinism | re-ran `run_price.py` twice | `git diff --exit-code -- receipts` clean both times |
| CI registration, vacuity | replaced the test discovery root with a directory holding no tests | the asserted minimum test count failed the step, which is exactly the failure `thinghood`, `grammar_fit` and `priced_admissions` do **not** get |
| Coverage gate, missing report | moved `coverage.json` aside | `FAIL: coverage.json is missing; run coverage first`; exit 1, then 0 after restoring it |
| Coverage gate, file-set drift | added an unmeasured `code/zzz_probe.py` | `FAIL: the measured file set differs from code/**/*.py`, naming `only expected: ['code\zzz_probe.py']`; exit 1, then 0 after deletion |
| Coverage gate, undatable report | removed `meta.timestamp` from the report | `FAIL: coverage.json carries no timestamp; refusing to date it`; exit 1, then 0 after restoring it |
| Coverage gate, stale report | touched a measured source after generating the report | `FAIL: code\enumerate_space.py was modified after the report was written; regenerate coverage`; exit 1, then 0 after regenerating. It errs conservatively: touching a source without changing it fails, which is the safe direction |
| Coverage gate, threshold | added five unexercised branches to `code/price.py` and regenerated the report | **NOT PROVED — attempted twice and abandoned, and the reason is recorded rather than a number invented.** Both runs were invalidated: the tree was edited by another writer while `coverage run` was executing, so the report's line numbers no longer matched the sources it had measured and the gate failed on unrelated modules (`code\items.py` at 39.6%, `code\enumerate_space.py` at 70.1%) rather than on the probe. The probe was removed and the arithmetic that predicts the failure is recorded instead: the clean report has 417 of 432 branches covered, 96.53%, and five unexercised `if`s add 10 uncovered branches, giving 417/442 = 94.34%. **That prediction is arithmetic, not an observation, and this row is not a receipt until someone runs it on a quiet tree.** The other four coverage rows above WERE observed |
| Lean census, unimported module | added `lean/LimitObserver/ZzzProbe.lean`, imported by nothing | `FAIL: LimitObserver.ZzzProbe is outside LimitObserver.AxiomReport's import closure, so no axiom report is emitted for it`; exit 1, then 0 after deletion. This is the half Lean cannot see: a module nothing imports is absent from the compiled environment, so the in-Lean census has no name to miss |
| Lean census, unreported theorem | added `theorem zzz_probe_unreported` to `LimitObserver.lean` | the census emitted `LimitObserver.zzz_probe_unreported: []` and `FAIL: axiom reports differ between the build and the committed receipt`; exit 1, then 0 after reversal. Under the hand-written list this injection would have been **silent**, which is how `separatesAt_eq_readsAt` went unreported |
| Prose gate, the defect that shipped | restored `**8 / 7**` in the OBS-4 row of `FINDINGS.md` | `FAIL: FINDINGS.md:101: the OBS-4 row: the second miss of this tree: published ['8', '7'], receipt has ['7', '6']`; exit 1, then 0 after reversal |
| Prose gate, stale binding | deleted the bound census row from `FINDINGS.md` | `FAIL: FINDINGS.md: the binding for rival-admitting states matched 0 times, expected exactly 1`; exit 1, then 0 after reversal. Deleting the sentence is not a way to pass |
| Prose gate, mis-tabulated prediction | changed P-16's outcome cell in `STATUS.md` from MISS to HIT | `FAIL: STATUS.md:62: P-16 is tabulated '**HIT**' but the receipt scores it False`; exit 1, then 0 after reversal |
| Primed Lean report, isolated review control | added `theorem zzz_probe_report' : True := True.intro` to the main module | baseline 21 reports; verifier exit 1 names `LimitObserver.zzz_probe_report'` in the build/receipt diff; after removing the theorem, clean rebuild passes 21 reports. The receipt SHA256 remained `a986cf928fa9c56fa4828717e523cc81841f3414df793168723109f5dd212a76`; no receipt regeneration occurred during the injection |
| Independent coverage thresholds, in-memory input control | supplied the actual gate a dated one-source report with 94 of 100 lines and 100 of 100 branches, combined percentage 97 | gate exits 1 naming `line coverage 94.00%`; reversing to 100 lines and 94 branches exits 1 naming `branch coverage 94.00%`; both 100 passes. `test_line_and_branch_thresholds_are_independent` invokes `main` with mocked file/report input. This tests gate arithmetic, not coverage-tool instrumentation; it does not retroactively turn the abandoned source-injection row into a pass |
| Imported module outside the declared theorem domain, in-memory input control | supplied a source census whose root imports `LimitObserver.Probe` | exits 1 naming the probe as outside the declared theorem census even though import closure includes it; `test_importing_a_new_module_does_not_extend_the_theorem_census` carries the control. The audit still reports main-module theorems, not every declaration or metaprogram in the package |
| Interrupted minimum, actual small-budget enumeration | set `candidate_budget = 3`, `max_items = 2` at each genesis base | `test_actual_refusal_retains_only_completed_levels` records completed level 0, three yielded level-1 candidates and the refused ordinal 4. Three observed successful level-1 candidates are retained only as partial trace data, never as a minimum or tie census. Pending rows are OPEN, null-priced and not exhausted. The default API still raises `CandidateBudgetRefused` naming item count 1; reversing the budget to 10000 completes the control and certifies its minimum at 1 |

### What injection does not prove

That the population is the right mathematical object. A perfect pin of the
wrong set is still the wrong set. Injection demonstrates that a residual is
live; it does not close one. In particular it says nothing about whether
depth 3 is deep enough, which is recorded OPEN on its own terms.

**And it does not prove that a theorem has any instance.** Every gate in this
table passed while `chain_bounded`'s hypotheses were jointly unsatisfiable and
its three theorems were vacuous. The axiom receipt reported them clean,
because an axiom report says which axioms a proof used and never whether its
hypotheses can be met; the forbidden-token scan read them as text; and no
Python evidence instantiated them. Only a reader caught it. The repair carries
`chain_bound_has_an_instance` so that the *next* reader has a witness to check
rather than a statement to re-derive, and that witness is the closest thing to
an injection this failure mode admits.

## Regenerating a receipt deliberately

    python run_price.py            # rewrites receipts/price.json
    python verify_lean.py --write  # rewrites receipts/lean_axioms.txt

Both overwrite a committed artifact, so run them deliberately and commit the
diff. Never run either while an injection is live.

The candidate budget belongs to each `iter_candidates(base, item_count)`
call: one reading and one item level, shared by all demands and both cost
measures. The existing sealed-prefix layer budget is a separate guard. Running
L and F in two processes changes neither domain nor bound. The explicit
retain-completed mode records a refusal and preserves only fully completed
successful levels; it does not truncate a level into a minimum certificate.
`searches` exports each reading's completed counts and, when interrupted, the
last yielded and first refused deltas, partial demand-hit counts, first
observed witnesses, declared ordering and replay inputs. This is a reproducible
observed prefix and boundary, not an enumeration of the unseen suffix.

## What this tree may write

Only `research/limit_and_observer/`, plus the research job of
`.github/workflows/verify.yml`, appended after the existing steps and touching
nothing else in that file. Not `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, `artifacts/`, `CLAUDE.md`, or any other tree.
