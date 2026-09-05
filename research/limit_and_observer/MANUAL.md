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
    cd ../..
    git diff --exit-code -- research/limit_and_observer/receipts
    python ci/check_prose_watchlist.py
    python -m pytest tests/test_primitive_contact.py -q -p no:cacheprovider
    git status --short

The Lean package is separate, and **manual**:

    cd research/limit_and_observer
    python verify_lean.py                # compare against the committed receipt
    python verify_lean.py --write        # regenerate it, deliberately

`verify_lean.py` is run by **no gate**, here or in any other research tree.
`CLAUDE.md` records that as the last live residual. Read a pass as "a person
ran it", never as "a gate enforced it".

## Notes that will save time

* **`coverage.json` is untracked and dated.** `check_coverage.py` refuses a
  report it cannot date and fails if any measured source is newer than the
  report. Touching a source without changing it fails until you regenerate,
  which is the safe direction.
* **The receipt must regenerate byte-identically.** `run_price.py` writes
  sorted keys, LF endings, no timestamp and no environment value.
  `git diff --exit-code -- receipts` is the check.
* **`receipts/**` and the two frozen texts are `-text`.** Never let an editor
  or a CRLF conversion rewrite them: it breaks the pins and the byte
  comparison at once. `verify_pins.py` checks the attribute and refuses CR
  bytes in a receipt.
* **Pins are canonical Git blob sha256**, `git show HEAD:<path> | sha256sum`,
  never the worktree file's digest. The two differ for every file under
  `code/` and `lean4/` in a CRLF checkout and agree only for `artifacts/**`.
* **The full suite takes a few minutes.** The population is rebuilt per test
  module; the pure functions are memoised inside a process, not across them.

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

### What injection does not prove

That the population is the right mathematical object. A perfect pin of the
wrong set is still the wrong set. Injection demonstrates that a residual is
live; it does not close one. In particular it says nothing about whether
depth 3 is deep enough, which is recorded OPEN on its own terms.

## Regenerating a receipt deliberately

    python run_price.py            # rewrites receipts/price.json
    python verify_lean.py --write  # rewrites receipts/lean_axioms.txt

Both overwrite a committed artifact, so run them deliberately and commit the
diff. Never run either while an injection is live.

## What this tree may write

Only `research/limit_and_observer/`, plus the research job of
`.github/workflows/verify.yml`, appended after the existing steps and touching
nothing else in that file. Not `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, `artifacts/`, `CLAUDE.md`, or any other tree.
