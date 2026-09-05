# Operating manual: the side-free control

Everything here is metatheoretic apparatus — how to drive this tree and what
each of its gates is worth.  Nothing here is an object-language input.
Material changes, each with its reason, are recorded newest-last in
`change_log.md`; the two frozen files are never among them.

## Commands, from the repository root

```powershell
python research/side_free/verify_pins.py
cd research/side_free
python -m unittest discover -s tests -p "test_*.py"
python -m mypy
python -m coverage erase
python -m coverage run -m unittest discover -s tests -p "test_*.py"
python -m coverage json -q
python check_coverage.py
python run_side_free.py
python run_comparison.py
cd ../..
git diff --exit-code -- research/side_free/receipts research/side_free/COMPARISON.md
python ci/check_prose_watchlist.py
```

`run_comparison.py` writes both `receipts/comparison.json` and `COMPARISON.md`;
the document is RENDERED from the receipt, so it cannot carry a number the
receipt does not, and a test asserts the committed file is a fresh rendering.
`--check` compares both without writing.

`run_comparison.py --declare` re-snapshots the pinned values into
`pinned/BOUNDARY_PIN.json`.  It is a **deliberate** act, exactly as a pin
regeneration is elsewhere in this repository: running it while an injection is
live adopts the injected value as the baseline and destroys gate C1.

The Lean package is separate and is a **manual receipt**:

```powershell
cd research/side_free
python verify_lean.py            # builds from clean, then audits
python verify_lean.py --regen    # rewrites lean/axioms.txt, deliberately
```

`verify_pins.py` takes `--allow-unreachable-pin`, and only the CI step passes
it.  See "What the gates are worth" below for why.

**Adding or removing a test obliges a second edit.**  The registered CI step
asserts an EXACT test count, so that an enumeration finding nothing cannot pass
as a green suite; that literal lives in the workflow and does not move by
itself.  It DRIFTED once — written at 321, left there while two later commits
added two tests, so the step could not pass at all — which is why the
obligation is written here beside the other deliberate acts.  The count is now
held from this side as well: `tests/test_registration.py` parses it out of the
workflow and fails by name when it is not the count this suite discovers, in
either direction.

## What this tree adds, gate by gate

| gate | what it checks | where it lives |
|---|---|---|
| pin verifier | the two frozen files byte for byte in the working tree, the index, `HEAD` and every commit that touched them; the vendored pin's three digests and its CR refusal; the manifest's blob digests at the pinned commit; the `-text` attributes | `verify_pins.py` |
| G1 | the vendored pin's four values, plus the conditional check against the pinned commit reported PASS or SKIPPED-with-reason | `control.gate_pin_bytes` |
| G2 | the two requirement texts, as the pinned texts with one declared phrase deleted, byte for byte; plus a whole-word scan of the control strings | `control.gate_requirement_texts` |
| G3 | the three surviving capability sentences byte for byte, the cross-world join by name, and the mechanical side-word partition | `control.gate_capability_texts` |
| G4 | **the decisive one.**  This tree's own verdict function against the pinned world's own recorded automorphism sets, on the fourteen rows the minimum ranges over | `control.gate_verdict_replay` |
| G5 | **the smuggle tripwire.**  The forgetful lemma and its corollary over the full declared census of 1344 cells, plus two counts that are not each other: the cells where the corollary's antecedent holds, which is its non-vacuity, and the cells where the side-typed world separates and the forgotten one does not, which is the converse's failure | `control.gate_forgetful_lemma` |
| G6 | the mirror against the pinned vector on all 48 rows per reading, plus the minima and their classes | `control.gate_mirror_matches_the_pin` |
| deletion totality | no deleted name survives in the side-free modules; no narrowed name is absent; no identifier carries a deleted stem outside a declared allowlist | `tests/test_deletion.py` |
| source isolation | no citation into a sealed path, no sealed identifier, no other research tree name — with exactly one declared carve | `tests/test_isolation.py` |
| coverage | line AND branch, each at or above 95%, measured from inside the tree, with a stale-report refusal.  The measured set is `code/sidefree/**` plus the declared top-level modules, held to EXACT equality so it fails in both directions | `check_coverage.py` |
| Lean | build from clean, forbidden tokens as text, import closure, audit totality, the axiom whitelist, and the committed log | `verify_lean.py` |
| C0 | the four vendored pinned receipts by declared sha256, byte count and CR refusal; the blob at the pinned commit when it is reachable; and that each file is the receipt of the challenge it is filed under | `comparison.gate_bytes` |
| C1 | **the comparison's own gate.**  Every pinned value a row reads is declared in `pinned/BOUNDARY_PIN.json` at its `CHALLENGE:JSON-PATH`, agrees with the pinned bytes, and the declaration is TOTAL in both directions | `comparison.gate_declared_values` |
| C2 | the control's own headline numbers are the ones the rows carry, the two deltas recomputed from the two minima, and the base row is where the row that reads it by index says it is | `comparison.gate_receipt_agrees` |
| C3 | the two worlds' minima joined through the declared collapse map, and the routes only the pinned world reaches recomputed from the pin | `comparison.gate_minimum_join` |
| C4 | the row ids are distinct and the declared item taxonomy is total in both directions | `comparison.gate_taxonomy` |
| registered count | the test count pinned in this tree's own CI step equals the count this suite discovers, failing in both directions | `tests/test_registration.py` |

## Proving a gate: the injection record

A gate is not proved by being green.  It is proved by failing on the exact
defect it exists to catch, with the failure naming the injected object, and by
recovering when the injection is reversed.

Every injection below was run.  Exit statuses were read **directly** from the
process, never after a pipe.  **No receipt, axiom log or pin was regenerated
while any injection was live**; the receipt runner was invoked with `--check`,
which compares and never writes.

| # | mutation | command | diagnostic | exit | recovery |
|---|---|---|---|---|---|
| I1 | one byte of `pinned/boundary_challenge3.json` changed | `python research/side_free/verify_pins.py` | `FAIL: pinned/boundary_challenge3.json: sha256 953efff352f1… wanted e4904075aaa0…` and the git blob line beside it | 1 | restored from the pinned commit; exit 0 |
| I2 | one newline appended to the frozen `PREDICTIONS.md` | `python research/side_free/verify_pins.py` | `FAIL: working copy of PREDICTIONS.md: aeaf3da9504b… wanted 24d6bdf5a6a7…` | 1 | reverted; exit 0 |
| I3 | the deleted phrase reinserted into the control requirement | `python run_side_free.py --check` | `FAIL: the record is VOID and NO difference is reported` then `FAIL: G2: the pinned declared with ' under a reading' deleted is not the control text byte for byte` | 1 | reverted; exit 0, receipt byte-identical |
| I4 | one character of a capability sentence altered | `python run_side_free.py --check` | `FAIL: G3: capability text for keep_labels is not byte-identical` | 1 | reverted; exit 0 |
| I5 | `keep_labels` renamed to `keep_label` throughout the control's own space | `python run_side_free.py --check` | `FAIL: G3: coordinate names absent from the pinned list: ['keep_label']` and the mechanical-partition line beside it — the cross-world join fails **by name** rather than dropping a route | 1 | reverted; exit 0 |
| I6 | the side re-admitted into the side-free key as a per-mark two-valued attribute | `python run_side_free.py --check` | `FAIL: G5: the forgetful lemma fails: {'reading': 'U', 'labels': ['a','a'], 'placement': [0,1], … 'automorphism': {'reflected': True, 'permutation': [1,0]}}`, the corollary line, and `FAIL: G5: forgetting loses no separation at any cell of the declared census: the converse fails nowhere` | 1 | reverted; exit 0, receipt byte-identical |
| I7 | a deleted identifier (`placement`) reintroduced into a side-free module | `python -m unittest discover -s tests -p "test_deletion.py"` | `test_no_deleted_name_survives_in_the_side_free_modules` … `Lists differ: ['placement'] != []`, and the stem scan names it too | 1 | reverted; exit 0 |
| I8 | one value of the committed receipt perturbed | `python run_side_free.py --check` | `FAIL: receipts/side_free.json differs from a fresh computation` | 1 | restored; exit 0 |
| I9 | a measured source touched without changing it, after the report was written | `python check_coverage.py` | `FAIL: coverage.json predates measured source files: code\sidefree\model.py` | 1 | regenerated; exit 0 |
| I10 | the side-word criterion widened so a deleted coordinate would transfer | `python -m unittest discover -s tests -p "test_space.py"` | `test_the_mechanical_partition_equals_the_implemented_one` … `Lists differ: ['admit_names', 'extra_mark', 'keep_labels', … 'withdraw_reflection'] != ['extra_mark', 'keep_labels', 'withdraw_mark_permutations']`, and `test_moving_a_coordinate_across_the_criterion_is_caught` beside it | 1 | reverted; exit 0 |
| I11 | a forbidden token added to a Lean doc line | `python verify_lean.py` | `FAIL: lean\SideFree\Basic.lean:126: forbidden token partial` | 1 | reverted; exit 0 |
| I12 | a Lean theorem added with no `#print axioms` line | `python verify_lean.py` | `FAIL: SideFree.zzz_probe_unaudited is declared under lean/SideFree/ but has no #print axioms line in SideFree.lean` | 1 | reverted; exit 0, 35 reports |
| I13 | a frozen expectation edited in code to fit a different answer | `python -m unittest discover -s tests -p "test_*.py"` | `test_all_predictions_hit` … `{'id': 'P1', 'status': 'MISS', 'failures': [{'path': 'decided.side_free_minimum', 'expected': 2, 'computed': 1}]}` | 1 | reverted; exit 0 |
| I14 | the pinned commit replaced by an unreachable one in a temporary manifest | `test_an_unreachable_pinned_commit_is_reported_as_skipped` | the conditional check returns `SKIPPED` with the reason and the residual, never a silent pass | — | permanent test |
| I15 | one boundary value changed in the pinned manifest: `declared_values["3:readings.U.minima_by_mu1.minimum"]` from `1` to `0` | `python run_comparison.py --check` | `FAIL: the comparison is VOID and NO difference is reported` then `FAIL: C1: declared value 3:readings.U.minima_by_mu1.minimum is 0, the pinned bytes say 1` | 1 | value restored; exit 0, both files byte-identical |
| I16 | the same one boundary value, against the pin verifier | `python research/side_free/verify_pins.py` | `FAIL: declared value 3:readings.U.minima_by_mu1.minimum is 0, the pinned receipt says 1` | 1 | value restored; exit 0 |
| I17 | one value of the vendored `pinned/boundary_challenge2.json` bytes altered | `python run_comparison.py --check`, then `python research/side_free/verify_pins.py` | `FAIL: C0: challenge 2: pinned/boundary_challenge2.json has sha256 b5f90e4b5295… , the manifest declares ca6a9f935951…`, and the verifier's own `FAIL: pinned/boundary_challenge2.json: sha256 … wanted …` | 1 and 1 | restored from the pinned commit; both exit 0 |
| I18 | the test count pinned in this tree's CI step changed from 325 to 324 | `python -m unittest tests.test_registration` | `AssertionError: 324 != 325 : .github/workflows/verify.yml pins Ran 324 tests and this suite discovers 325; bump the pin in the same commit that changes the suite size` | 1 | reverted; exit 0 |

I18's defect is not hypothetical: the pin stood at 321 against a suite of 323
when this guard was written, so the registered step could not pass, and the
first run of the guard reported that pair before anything was injected.

Several further probes live as permanent tests rather than as one-off
injections, because they mutate a temporary copy and can therefore run every
time: a mutated pinned verdict against G4, a drifting mirror against G6, a
malformed pin against every reader, a disagreeing key choice, an empty
satisfying set, and a scorer forced to report a MISS.  Each is written so it
FAILS if the guard is removed.

**Source isolation** is proved that way too, and is named here because it is a
row of the table above and was reachable by no census before this line.  Its
probes run the scan over assembled examples and require it to name each one:
a citation into the sealed paper, into the sealed artifacts, into the sealed
Lean and into the sealed kernel, each by its own label; a sealed claim
identifier; a sealed Lean name; an import of the sealed kernel, with this
tree's own import admitted beside it; a bare directory name that is not a
citation, admitted; the carved tree's name barred outside the three declared
files and admitted inside them, and another tree's name barred inside those
same three; and non-UTF-8 bytes reported as unscannable rather than passed
over.  Each example is assembled from pieces so this file carries no citation
of its own.

The remaining three published comparison gates are proved the same way, and
are named here because a census of what has been proved must reach every gate
the table above publishes.  **C2**: a record stating a delta it does not have
fails naming `delta_vs_unnamed`; a row disagreeing with the record fails
naming `R31`; a first control row that is not the base row fails on `not the
base row`.  **C3**: a record stating the wrong collapse fails on `the collapse
of the pinned minima`, and one stating the wrong route set fails on `routes
the pinned world reaches`.  **C4**: a duplicate row id fails on `duplicate row
ids`.  Each runs over a deep copy, so none of them writes anything.

## What the gates are worth, stated exactly

* **G4 is the load-bearing tie** between this tree and the pinned world.  It
  uses no re-declaration of anything: it applies this tree's own verdict
  function to the pinned world's own recorded automorphism sets and requires
  the pinned world's own recorded answers back.  Its scope is the fourteen
  rows the minimum ranges over — total over what the minimum is computed
  FROM, and not over all 48 points per reading.  A defect in a bundle row's
  recorded verdict is invisible to it.
* **G5 is the fairness guard that runs AGAINST the pinned world.**  It is a
  test, not an argument.  It was proved by injection before being relied on,
  and the injection's first violating cell is the retained configuration
  itself.
* **G6 keeps the mirror honest**, but the mirror is a countermodel-domain
  object and never the pinned carrier.  A divergence VOIDS the run.
* **The pinned-commit check can be unavailable.**  `5c43c5ee` is on an
  unmerged branch that a fresh clone of the remote does not carry.  By default
  `verify_pins.py` FAILS when it is unreachable; the CI step passes
  `--allow-unreachable-pin`, which downgrades that to a reported SKIP with the
  reason and the residual named.  **Residual, recorded and not closed:** in
  CI the link from the vendored bytes to that commit is not checked at all,
  and only the three digests — which need no git — hold.  Re-take the pin when
  that branch merges.  The suite asserts the SPLIT and not this machine's side
  of it: where the commit is reachable the verifier must exit 0 with no flag,
  and where it is not it must exit 1 naming the commit and then exit 0 under
  the flag.  An earlier version of that test asserted exit 0 with no flag
  unconditionally, which is a red job in exactly the clone the flag exists
  for; it was undisclosed by any document here, which is why it is written
  down now.
* **The Lean package is a manual receipt.**  No CI job builds it, so its axiom
  report is unchecked by any gate.  Recorded as a live residual, not closed.
* **Coverage is measured from inside the tree** and its report is untracked;
  the gate refuses a report older than any measured source.
* **C1 is the comparison's load-bearing gate**, and it is worth exactly its
  totality.  It does not check that the comparison compares the RIGHT items:
  a perfect pin of the wrong row set is still the wrong row set.  What it
  checks is that no boundary number in this tree was typed by hand and that
  none has drifted from the pinned bytes.
* **The comparison record carries no environment value.**  Whether the pinned
  commit is reachable is printed by `run_comparison.py` and never written into
  `receipts/comparison.json`, so the record is the same file in a clone that
  cannot reach that commit.  A test proves it by making every `git show` fail
  and requiring the rendering back byte for byte.  The sibling record
  `receipts/side_free.json` is built the other way and does NOT have this
  property; that is recorded as an open item and is not repaired here, because
  the frozen design declares the conditional check to be part of that record.
* **That sibling record's CI step takes the same split.**  It regenerates the
  record and then compares bytes — hard where the pinned commit is reachable,
  and where it is not the regenerated diff is PRINTED under a named SKIP.  It
  previously required no diff unconditionally, which the record itself cannot
  satisfy in a clone that cannot reach that commit, and the step was registered
  in that form anyway.  **Residual, recorded and not closed (SF-OPEN-E):** in
  that clone drift in this one record is visible in the job log and is gated by
  nothing.  Make the comparison hard again when that branch merges — the same
  act that drops `--allow-unreachable-pin` above.

## What injection does NOT prove

That the population is the right mathematical object.  A perfect pin of the
wrong set is still the wrong set.  In particular: the deletion register's
population is enumerated from the pinned source independently of the
classifier, but whether the declared word stems are the right stems is a
judgement, not a computation.
