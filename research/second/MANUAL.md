# MANUAL: operating the second derivation

`AuthorityEffect: None`.  Apparatus only: how to drive the run, what has
been injected, and what each session must do first and last.  Nothing
here is object-language content.

## Declared readings, recorded before the first rung

1. **The seed's author and the run's first session are the same
   session.**  The seed was drafted, hashed, and committed in the session
   that then opened rung 0.  Rung 0's content is replay and a census of
   declared inputs, which no prediction can steer; later rungs are to be
   opened in fresh sessions with no instruction beyond `CLAUDE.md` and
   the seed.  This is recorded because a run that is not blind to its
   author's expectation must say so, as `fresh_characters` did.
2. **Two of the three trees the seed names are not on `main` at rung
   0's snapshot** (`standing_commitment`, pull request 127;
   `two_sided_commitment`, pull request 128).  Rung 0 pins what is on
   `main`, records those two as absent, and leaves their replay OPEN for
   the first rung whose snapshot contains them.  Nothing is pinned from a
   commit that is not an ancestor of HEAD.

   After pull requests 127 and 128 merged in the declared order, rung 0 was
   repaired on exact base `dd2aba24`.  The absence claim above remains true
   of its original snapshot.  A separate manifest section now pins both
   landed engines, runners, and receipts at the later base, and the repaired
   receipt replays them.  This closes present custody without revising a
   frozen prediction or granting authority to either receipt.

## Commands

From the repository root, for a rung `<r>`:

```text
python research/second_<r>/verify_pins.py
python research/second_<r>/run_<r>.py
cd research/second_<r>
python -m unittest discover -s . -p "test_*.py"
python -m mypy
cd ../..
python ci/check_prose_watchlist.py
python -m pytest tests/test_primitive_contact.py -q -k firewall -p no:cacheprovider
```

Rung one CI does not run its generator over tracked receipts before replay.
Its non-mutating test and coverage form, from `research/second_stream`, is:

```text
python -m coverage erase
python -m coverage run -m unittest discover -s . -p "test_*.py"
python -m coverage json -q
python check_coverage.py
python -m mypy
```

Gate time per rung is recorded in the rung's `STATUS.md` and must stay
under fifteen minutes of wall time.

## Session protocol

At the start of a session: read the handoff, read `PLAN.md`, read the
`STATUS.md` of the last rung, take the next rung by the seed's rule.  At
the end: write the handoff, leave the working tree clean, never merge.

## Injection record

A gate is proved by failing on the exact defect it exists to catch, with
the failure naming the injected object, and by recovering when the
injection is reversed.  Receipts are never regenerated while an injection
is live.

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
| --- | --- | --- | --- |
| 0 | frozen-text pin (`second_inheritance/verify_pins.py`) | one line appended to `PROMPT.md` in a throwaway commit `08cb4808` on top of `f2d40f59`, 2026-09-03 | `FAIL: frozen text moved: research/second_inheritance/PROMPT.md: expected aa804ee3..., got 9b2498ce...`, exit 1; after `git reset --hard HEAD~1` the verifier passed with exit 0 and the tree was clean. The verifier reads blobs at HEAD, so an uncommitted edit is invisible to it by design; the injection therefore had to be committed to be seen, and was discarded, not reverted, so no receipt was regenerated under it |
| 1 | operator-vocabulary digest scan (`second_stream/test_forbidden.py`) | a probe file in the write root carrying one watched word, 2026-09-04 | `AssertionError: Lists differ: ['zz_review_probe.md:1: topology'] != []`, exit 1; exit 0 after deleting the probe.  The scan stores the terms only as sha256 digests, never as text, so the committed file does not carry what it watches for |
| 1 | the same scan, multi-word terms | a probe carrying a two-word, a three-word and a second two-word term | the failure named all three, so the phrase passes are live and not decoration; exit 1, exit 0 after deletion.  The three tokens are elided here rather than quoted, because this record is itself scanned - the same trap the root census caught in a sibling tree, met again and recorded again |
| 1 | root census scan (`CensusScan`) | a probe carrying a word confirmed watched at the root by `ci/check_prose_watchlist.py --probe` | the scan named the file, the line and the token, exit 1; exit 0 after deletion.  The token is elided here because this file is itself scanned |
| 1 | identifier firewall (`DenylistScan`) | a probe carrying two working-denylist identifiers, plus a suffixed and a prefixed form as negative controls | the failure named exactly the two whole identifiers and NOT the two substring forms, which is the repair the author made to a sibling tree, confirmed live here rather than inherited on trust; exit 1, then 0 |
| 1 | outside-write-root scan | a file created at `research/zz_review_probe_outside.txt`, outside the write root and under no sealed prefix | `AssertionError: ... ['?? research/zz_review_probe_outside.txt'] != [] : a path outside the write set is touched`, exit 1; exit 0 after deletion |
| 1 | source pin at the snapshot (`second_stream/verify_pins.py`) | one hex digit changed in the pinned `code/derivation/model.py` digest | `FAIL: snapshot hash mismatch for code/derivation/model.py: expected 7A7FD2BA..., got 6A7FD2BA...`, exit 1; exit 0 after byte-exact restore |
| 1 | source pin at HEAD - the half that only a second check can see | in a throwaway clone at `cdefee90`, a committed change to `code/derivation/model.py` with the snapshot copy left intact | `FAIL: source moved at HEAD for code/derivation/model.py`, exit 1.  Pinning at the snapshot alone would have passed; this is why the verifier checks twice |
| 1 | frozen-text pin | in the same clone, one line appended to `PROMPT.md` and committed | `FAIL: frozen text moved: research/second_stream/PROMPT.md: expected efca5d96..., got 9e96bcf8...`, exit 1 |
| 1 | frozen-text pin, the recorded blind spot and its repaired cover | exact-head review found that an unstaged edit was invisible to `verify_pins.py` and that the runner performed no on-disk check; the prior claim that the runner refused was false and is withdrawn. The repair test points the runner at a changed temporary frozen file and pre-existing sentinel outputs | `run_stream.py` returned 1 with `FAIL: frozen text moved on disk`; both sentinel outputs remained byte-identical. The production anchors are independent constants checked before construction or output |
| 1 | two-point frozen-text drift detection | a mocked build changes a prechecked temporary frozen file before returning, with both output paths preloaded with sentinels | the second check returned 1 with `FAIL: frozen text moved on disk`; both outputs remained byte-identical, and the receipt builder receives only the digests captured by the first check. This detects a mismatch present at either check; it does not establish atomic time-of-check/time-of-use closure or uninterrupted disk history |
| 1 | exact manifest populations | a source row and then a frozen row removed from temporary manifest objects | each failed with `source population differs` or `frozen text population differs`; the committed manifest was never rewritten |
| 1 | committed write scope | synthetic NUL-delimited snapshot-to-`HEAD` paths containing a sealed path, plus rename-disabled command inspection | the verifier named the sealed committed path and refused; the test also requires `--no-renames`, while the separate status check covers unignored working-tree and index paths |
| 1 | the four declared budgets | each constant lowered until it fired, with bounded-consumption generators for the response cap | each recorded its own named terminal; the response cap consumed exactly bound plus one candidates and attached nothing |
| 1 | attachment atomicity | the second prospective child key raised after the first preflight succeeded | `terminal_iso_budget` named `attach`, recorded `attached: 0`, and the terminal parent retained zero outgoing edges |
| 1 | coverage module census and thresholds | synthetic missing, stale, malformed, file-set-mismatched, line-low, and branch-low reports; production-module discovery is compared to both the checker set and `pyproject.toml` | each defect failed by name; the workflow now generates the report in the same test process and immediately executes the checker |
| 1 | the prediction scorer | a synthetic receipt fragment built to score MISSED | the scorer emitted MISSED rather than HIT, so a scoreboard of hits is not a rubber stamp; an empty population separately emitted VACUOUS and was never rounded up |
| 2 (track 1, no first demand) | pin verifier, source blob (`second_nofirst/verify_pins.py`) | first hex digit of the pinned `lean4/Derivation/Inertia.lean` hash changed in `SOURCE_MANIFEST.json`, 2026-09-04 | `FAIL: hash mismatch at the snapshot for lean4/Derivation/Inertia.lean: expected 062615CB…, got C62615CB…`, exit 1; exit 0 after restoring the manifest |
| 2 (track 1) | pin verifier, span | first hex digit of the `paper/paper.md` 488-494 span hash changed | `FAIL: span mismatch at the snapshot for paper/paper.md:488-494: expected 0fb9e4e0…, got bfb9e4e0…`, exit 1, then 0. A blob pin and a span pin are different guarantees and this rung records both |
| 2 (track 1) | pin verifier, frozen text | first hex digit of the `PROMPT.md` hash changed | `FAIL: frozen text moved: research/second_nofirst/PROMPT.md: expected 013f38a2…, got e13f38a2…`, exit 1, then 0 |
| 2 (track 1) | Lean axiom whitelist (`second_nofirst/verify_lean.py`) | a `Classical.em` theorem added to `SecondNoFirst/Stake.lean` with its report line added | `FAIL: SecondNoFirst.Stake.zzz_probe_choice depends on disallowed axioms ['Classical.choice']`, exit 1; then `lean audit clean: 10 sources, 75 axiom reports` and exit 0 |
| 2 (track 1) | Lean committed axiom log | the `fresh_profile` line deleted from `receipts/lean_axioms.txt` | `FAIL: fresh build has a report the committed log does not: SecondNoFirst.Propagate.fresh_profile :: Quot.sound propext`, exit 1, then 0. This is the check the sibling trees lack: their axiom audit needs a live build, and this rung's committed log makes the result reviewable without one |
| 2 (track 1) | Lean module census, derived not hand-listed | `theorem zzz_probe_unlisted` added to `Stake.lean` without regenerating the report | `FAIL: SecondNoFirst.Stake.zzz_probe_unlisted is declared in Stake.lean but not listed in AxiomReport.lean`, exit 1, then 0. The repaired verifier recursively enumerates module paths and compares compiler-reported declarations and module origins exactly with fresh reports, FW-DEF rows, and the committed receipt |
| 2 (track 1) | coverage floor (`second_nofirst/check_coverage.py`) | the floor raised from ninety-five to ninety-nine point nine | `FAIL: line coverage 98.66% is below 100%; branch coverage 95.28% is below 100%`, exit 1, then 0 |
| 2 (track 1) | coverage measured-set drift | `verify_pins.py` removed from the declared measured set | `FAIL: verify_pins.py is in the report but is neither declared measured nor declared excluded`, exit 1, then 0. The gate fails in both directions, so the set cannot shrink silently to flatter the number |
| 2 (track 1) | coverage staleness | `nofirst.py` touched after the report was written | `FAIL: nofirst.py was modified after the report was written (2026-09-04T11:37:03.162241); regenerate coverage.json`, exit 1, then 0 after regenerating |
| 2 (track 1) | FW-DEF census totality (`second_nofirst/test_census.py`) | the `fresh_profile` row deleted from `FWDEF_CENSUS.json` | `test_the_census_is_total_in_both_directions` failed with the two lists differing by that name, exit 1, then 0 |
| 2 (track 1) | FW-DEF census classification | `wf_step_inert` refiled from CONTENT to DEFINITION | `AssertionError: Lists differ: ['grammar_carries_no_stake (22 lines)', 'wf_step_inert (27 lines)'] != []`, exit 1, then 0. This probe also found a real defect in the gate as first written and changed the tree; see `research/second_nofirst/STATUS.md` |
| 2 (track 1) | prose census over the write root | one line carrying a watched noun appended to the rung's `STATUS.md` | `AssertionError: Lists differ: ['research/second_nofirst/STATUS.md:333: <term>'] != []`, exit 1, then 0, with `<term>` the watched noun, redacted here because writing it would put it into a tracked file and fail the root gate. The rung runs the repository's own scanner over its own tree, so a watched term fails there rather than waiting for the root gate; the census pin was NOT regenerated |
| 2 (track 1) | FW-OB1 discharge scan | a sentence appended to the rung's `STATUS.md` asserting the sealed obstruction had been discharged, redacted here | the scan named `research/second_nofirst/STATUS.md:333` and the matching pattern, exit 1, then 0. The scan has no carve-out for negation; the one line of the tree that states the refusal is excepted by DIGEST of its exact bytes |
| 2 (track 1) | reconstruction faithfulness, binder (`second_nofirst/test_reconstruction.py`) | `collapsed`'s second binder renamed from `d'` to `dd` in the reconstructed `Kernel.lean` | the normalized bodies differ and the assertion prints both, exit 1, then 0 after reversal.  A pin proves a source did not move; this gate proves the reconstruction says the same thing, which no pin can |
| 2 (track 1) | reconstruction faithfulness, hypothesis | `collapsed_of_no_insts`'s hypothesis weakened from `r.insts = []` to `r.insts = r.insts` | `AssertionError: Lists differ: ['lean4/Derivation/Inertia.lean -> Kernel.lean: collapsed_of_no_insts'] != []`, exit 1, then 0.  The sources are read by git blob AT THE SNAPSHOT, so the comparison is against the pinned revision and not against a working tree that may have moved |
| 2 (track 1 repair) | first-demand claim scope | two datum admissions from the empty history under the all-apart stake | the executable witness records first demand at index 2 with kind `AdmitDatum`; the prior sentence assigning the first occurrence one source is withdrawn, while the label-source assembly retains its frozen Lean name |
| 2 (track 1 repair) | reconstruction declaration population | found live: the old parser missed attributed declarations and anonymous instances | the adversarial parser covers both syntactic shapes; the gate compares exactly 49 shared declarations, including three anonymous instances, and pins the exact omitted population, which contains the attributed `insertNew_nil` declaration |
| 2 (track 1 repair) | coverage source, schema, arithmetic, and freshness gate | synthetic unlisted and nested modules, unknown `test_`-prefixed module, impossible counters, absent branch metadata, zero populations, inconsistent detail arrays and totals, future timestamp, and a supplied false percentage | `test_coverage_gate.py` raises by name; the test population is pinned, detailed arrays are reconciled, future-dated evidence is rejected, and true line and branch coverage and aggregate totals are recomputed |
| 2 (track 1 repair) | file and scope scanners fail closed | unreadable, non-UTF-8, NUL, non-UTF-8 path, failed git commands, missing comparison base, and an untracked working file | `ScannerFailureTests` names each unavailable input and verifies the census covers index plus untracked files and the scope diff includes the current worktree |
| 2 (track 1 repair) | Lean clean build and compiler census | root, report, nested, quoted, Unicode, private, attributed, and colliding declaration shapes plus failed `lake clean` | `LeanVerifierTests` compares the compiler's environment census with fresh reports and the receipt, includes nested modules, applies the whitelist before regeneration, and stops before build on a failed clean |
| 2 (track 1 repair) | CI registration | each required rung command or execution condition removed or changed in an in-memory workflow copy | the negative tests require one ordered replay step with the exact discovered-test count, coverage check, receipt comparison, strict typing, pins, and Lean verifier; the real workflow keeps the repository's per-module elaboration step last |

<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 2-stake | source-span pin (`second_stake/verify_pins.py`) | changed the first hexadecimal character of the frozen `challenge_two` span digest, 2026-09-04 | `FAIL: span moved at 3f44571240a0830a2fa8de639281670f4e50a511: challenge_two`, exit 1; restoring the manifest made the verifier exit 0 |
| 2-stake | frozen-text disk pin (`second_stake/verify_pins.py`) | appended `pin-probe` to the frozen prompt without committing it, 2026-09-04 | `FAIL: frozen text moved on disk: research/second_stake/PROMPT.md`, exit 1; removing the probe restored the pinned sha256 and exit 0 |
| 2-stake | deterministic receipt (`second_stake/run_stake.py --check`) | changed `authority_effect` in the summary receipt without regenerating, 2026-09-04 | `FAIL: receipt differs: receipts\stake.json`, exit 1; restoring the byte gave `second-stake receipts regenerate byte-identically`, exit 0 |
| 2-stake | census scan (`second_stake/test_forbidden.py`) | added `watchlist_probe.md` with the watched surface whose digest is `02195b8e989603e4dfb45352b902e8dc34bff40bb228f3c26e56a6ddebdb85ad`, 2026-09-04 | `watchlist_probe.md:1` was the sole named hit and the test exited 1; deleting it restored exit 0 without changing the census pin |
| 2-stake | working identifier firewall (`second_stake/test_forbidden.py`) | added `denylist_probe.md` with identifier digest `85e656601fc8a931ea14273b5c5377eedd183428601c91f91a563cc9f4f12835`, 2026-09-04 | `denylist_probe.md contains denied identifier`, exit 1; deleting it restored exit 0 |
| 2-stake | outside-name digest scan (`second_stake/test_forbidden.py`) | added `outside_name_probe.md` with a name whose digest is `874b4eedb60aa5724731fc8fff49c280d5f743565035f30b8e99cf2a81465468`, 2026-09-04 | `outside name in outside_name_probe.md`, exit 1; deleting it restored exit 0 |
| 2-stake | protected-open sentence (`second_stake/test_forbidden.py`) | added `forbidden_probe.md` carrying the barred closure sentence, 2026-09-04 | `forbidden_probe.md changes the protected open`, exit 1; deleting it restored exit 0 |
| 2-stake | line and branch threshold (`second_stake/check_coverage.py`) | supplied a synthetic report with 50/100 lines and 20/100 branches, 2026-09-04 | `FAIL: line coverage 50.00% is below 95.00%` and `FAIL: branch coverage 20.00% is below 95.00%`, exit 1; a 100/100 recovery report passed both checks and was deleted |
| 2-stake | outside-write-root predicate (`second_stake/test_forbidden.py`) | supplied `research/outside_probe` beside one allowed synthetic path, 2026-09-04 | `AssertionError: path outside declared writes: ['research/outside_probe']`, exit 1; the write root and both named shared paths recovered with exit 0 |
| 2-stake | shared append-only predicate (`second_stake/test_forbidden.py`) | put changed bytes before the synthetic base prefix, 2026-09-04 | `AssertionError: shared file is not append-only: synthetic`, exit 1; base bytes followed by appended bytes recovered with exit 0 |
| 2-stake | receipt temporal-field refusal (`second_stake/test_forbidden.py`) | inserted a `timestamp` key in the summary receipt, 2026-09-04 | `AssertionError: 'timestamp' unexpectedly found`, exit 1; removing it restored exit 0 and the receipt bytes |
| 2-stake | strict typing (`mypy --strict`) | assigned a text literal to an integer probe in `second_stake/rules.py`, 2026-09-04 | `rules.py:46: error: Incompatible types in assignment (expression has type "str", variable has type "int") [assignment]`, exit 1; removing the probe gave `Success: no issues found in 6 source files`, exit 0 |
| 2-stake repair | multi-demand completeness (`test_one_refusal_does_not_suppress_an_answerable_demand`) | supplied two open demands with the first unanswerable and the second carrying one minimum response, 2026-09-04 | the repaired traversal recorded the first refusal as nonterminal and called the edge attachment once; the pre-repair first-refusal break would have marked the node terminal and failed the regression |
| 2-stake repair | quotient-edge replay (`test_edge_certificate_refuses_round_and_transport_mutations`) | incremented a stored child response round, then replaced its datum transport by a non-bijection, 2026-09-04 | the certificate named `edge response-round mismatch` and `edge datum transport is not a bijection`; restoring both values returned no failure |
| 2-stake repair | immutable freeze (`test_freeze_commit_hash_and_population_injections_are_refused`) | changed a frozen-text manifest digest and matching disk bytes while leaving the original freeze-commit blob different, 2026-09-04 | verification named `frozen manifest hash differs from freeze commit`; the original PROMPT and PREDICTIONS bytes and commit-derived digests pass |
| 2-stake repair | runtime source custody (`test_runtime_origin_source_and_extra_module_injections_are_refused`) | substituted the same-named `observer_visibility/dual.py`, changed the pinned dual digest, and loaded one undeclared repository module, 2026-09-04 | the three probes respectively named `runtime module origin differs: dual`, `runtime source bytes differ from the pin: dual`, and `runtime module population differs from the closed census`; the fourteen declared origins pass |
| 2-stake repair | O4 claim downgrade (`test_small_invariance_paths_cover_refutation_and_refuse_unreplayed_orbits`) | presented an O4 rule on a source regime without executable target-regime transport replay, 2026-09-04 | the disposition is `OPEN_AT_TRANSPORT_REPLAY`, not CHECKED; only future target replay or proof can recover a CHECKED claim |
| 2-stake repair | compressed receipt semantic scan (`test_compressed_receipt_semantic_probe_is_named`) | placed an `environment` key inside a synthetic gzip receipt node, 2026-09-04 | the recursive scan named `nodes[0].environment`; both committed JSON and JSON-gzip receipts recover with no forbidden keys |
| 2-stake repair | growth-kind scoring (`test_growth_kind_scoring_does_not_substitute_response_targets`) | made E1's synthetic growth-kind union differ from its accepted-response target-kind union in both directions, 2026-09-04 | P-G1 followed the growth population: growth apart/response empty was MISS, while growth empty/response apart was HIT; the committed receipt exports both populations separately |
| 2-stake repair | control-target and input-count classification (`test_control_target_and_p_i4_require_both_constants_unrefuted`, `test_summary_records_exact_finite_terminal`) | refuted one synthetic constant and separately inspected the hard-coded input-count branch, 2026-09-04 | the P-I4 predicates require both constants unrefuted, the blanket proposition is REFUTED by the two invariant constants in the committed run, and P-C1 is `UNSCORED_DECLARED_POLICY` because no frozen-falsifier check exists |
| 2-stake repair | closed runtime-module population (`test_runtime_origin_source_and_extra_module_injections_are_refused`) | loaded an undeclared repository-local module named `test_extra_probe`, 2026-09-04 | the production census retained the module despite its `test_` prefix and origin verification named a population difference; only the unit harness explicitly excludes its two already-loaded caller modules |
| 2-stake repair | fail-closed text/binary census (`test_scan_population_fails_closed_on_binary_and_decode_defects`) | supplied NUL-bearing text, invalid UTF-8, an undeclared binary suffix, and a read failure, 2026-09-04 | each defect raised by name; the sole declared binary path is the full gzip receipt, whose decompressed UTF-8 JSON enters the same vocabulary scans |
| 2-stake repair | rename-safe path census (`test_changed_path_census_disables_renames_and_parses_nul`) | supplied synthetic NUL-delimited old and new paths and malformed path streams, 2026-09-04 | the regression requires `--no-renames --name-only -z`, retains both path names, and rejects unterminated or invalid-UTF-8 output; the comparison base remains separately rebound at ordered integration |
| 2-stake repair | declared metadata-key aliases (`test_compressed_receipt_semantic_probe_is_named`) | placed exact and conventional alias keys including `created_at`, `datetime`, `hostName`, `platform`, `cwd`, and `env` inside synthetic compressed JSON, 2026-09-04 | the recursive predicate named every injected location; this gate covers its declared spellings and aliases rather than every possible synonym |
| 2-stake repair | tracked cache-directory refusal (`test_scan_population_fails_closed_on_binary_and_decode_defects`) | supplied a synthetic force-tracked `.venv/test_evil.py` member while ordinary untracked cache output remained excluded, 2026-09-04 | the tree census named `tracked file in excluded generated directory`; a committed byte cannot hide behind a cache-directory name |
| 2-stake repair | coverage report integrity (`CoverageGateTests`) | supplied false and missing branch metadata, zero branch populations, a wrong-path basename duplicate, traversal, negative and inconsistent counters, aggregate drift, and a stale timestamp, 2026-09-04 | every malformed report failed by its named defect; the retained fresh pre-integration report still reads 97.20% line and 95.27% branch coverage |
| 2-stake repair | independent coverage-source census (`test_new_production_source_enters_the_independent_census`) | added synthetic top-level production file `helper.py` beside the gate and a test file, 2026-09-04 | the derived population included `helper.py`, excluded only the gate and `test_*.py`, and rejected a report that omitted the new source |
| 2-stake correction | frozen response-kind scoring (`test_frozen_response_scoring_and_growth_metric_do_not_substitute`) | diverged growth-origin kinds from accepted-response target kinds in both directions, 2026-09-04 | P-G1 and P-G10 followed response targets exactly as frozen in PREDICTIONS, while the Challenge 2 terminal helper followed growth origins; the earlier repair row saying the scorer followed growth is WITHDRAWN |
| 2-stake repair | tracked coverage-artifact refusal (`test_scan_population_fails_closed_on_binary_and_decode_defects`) | supplied synthetic force-tracked `.coverage` and `coverage.json` members, 2026-09-04 | each member failed by name as a `tracked volatile coverage artifact`; ordinary ignored runtime reports remain outside the committed-source census |

<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 1 (attribution repair) | rung-attributable scope, ordinary commit (`second_stream/verify_pins.py`) | one commit writing `research/second_stream/zz_probe_inside.md` and `research/zz_probe_outside.md` together, 2026-09-04 | `FAIL: rung-attributable committed diff changed outside the write root research/second_stream/ and the declared exceptions: research/zz_probe_outside.md`, exit 1; exit 0 after `git reset --hard` to the recorded base |
| 1 (attribution repair) | the same scope, MERGE commit | a merge whose author wrote `research/second_stream/zz_merge_inside.md` and `research/zz_merge_outside.md` inside the merge itself, over a side branch that had added a third file | the merge contributed exactly the two files its author wrote and NOT the inherited side-branch file, and `FAIL: ... research/zz_merge_outside.md`, exit 1; exit 0 after reversal. This is the probe the repair had to keep passing: narrowing a merge to its combined diff must not stop the gate seeing what a merger writes |
| 1 (attribution repair) | the same scope, unrelated tree | one commit writing only `research/boundary_seed/zz_probe_unrelated.md` | exit 0, and the committed-scope line unchanged at four attributable commits: an unrelated tree's commit is not this rung's. The counterfactual matters as much as the failure -- a scope check that fails on everything is not a scope check |
| 1 (attribution repair) | the same scope, REAL CASE (found live, not injected) | none -- `main` at `7d2e6e86` | `FAIL: ... and the declared exceptions:` naming sixty-five files across `research/boundary_seed/`, `research/second_nofirst/` and `research/second_stake/`, none of which this rung has ever touched. Three integration merges were attributed to rung one because the rule diffed every commit against its FIRST PARENT, and the first-parent diff of a merge is everything the other branch brought with it. Reading a commit's own contribution instead -- the combined diff for a merge -- returns exit 0 with three attributable commits, which are the rung's own three. A red `main` that no rung had caused |

<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 2-stake (scope repair) | boundary scan, this rung writing outside its root | one commit adding `research/second_stake/zz_in.md` and `research/zz_stake_outside.md`, 2026-09-04 | `AssertionError: Items in the first set but not the second:` naming the outside path, exit 1; exit 0 after `git reset --hard` to the recorded base |
| 2-stake (scope repair) | shared-file append claim | one commit of this rung PREPENDING a line to `research/second/MANUAL.md` | `AssertionError: False is not true : shared file is not append-only: research/second/MANUAL.md`, exit 1, then 0.  Measured against the comparison base now, so the claim is the one this rung can own -- this branch only appended -- rather than a rule about every future rung's edits to a shared file |
| 2-stake (scope repair) | sealed-path claim, deliberately NOT scoped | one commit touching `paper/paper.md` on a branch that otherwise touches only another rung's tree | `AssertionError: Lists differ: ['paper/paper.md'] != []`, exit 1, then 0.  This half stays repository-wide: no rung may write a sealed path, so it is checked on whatever branch is under test rather than skipped when the branch belongs to someone else |
| 2-stake (scope repair) | REAL CASE (found live, not injected) | none -- the branch of pull request 138, which touches only `research/second_nofirst/` | `FAIL: test_only_write_root_and_two_shared_appends_are_changed`, exit 1: the scan diffed the working tree against the FIXED `8dea98da`, so it read every rung merged since as this rung writing outside its root.  It passed on `main` only because this rung merged last, and the next rung to touch anything else broke it.  The repaired scan SKIPS that shape, named; that half is proved hermetically in `BoundaryScopeSituationTests` rather than replayed, because reproducing it for real needs the repair itself on `main` first -- copying the repaired file into a foreign checkout puts a path under this write root into the diff and makes the branch look like this rung's own.  Recorded as the residual it is |

<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 1 (scanner repin, 2026-09-18) | frozen-text pin on the shared scanner (`second_stream/verify_pins.py`), after `ci/check_prose_watchlist.py` moved from the sources to the HEAD-only frozen texts | one throwaway commit appending a comment line to `ci/check_prose_watchlist.py` on top of `2687d948` | `FAIL: frozen text moved: ci/check_prose_watchlist.py: expected cf5cbb17…, got 54697c52…`, exit 1; after `git reset --keep HEAD~1`, `second_stream pins verified: 19 sources at snapshot and HEAD, 5 frozen texts at HEAD`, exit 0 |

<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 2-stake (sealed-path scope, 2026-09-18) | sealed-path claim BEFORE the change, `test_no_branch_writes_a_sealed_path` at `9386c81e` | one throwaway commit adding only `ci/zz_probe.txt` on a branch touching nothing of this rung | `AssertionError: Lists differ: ['ci/zz_probe.txt'] != []`, exit 1.  An author branch changing `ci/` failed this rung's step; this is the behaviour withdrawn |
| 2-stake (sealed-path scope, 2026-09-18) | a rung commit writing `ci/` still fails, `test_no_rung_commit_writes_a_sealed_path` at `0b818337` | one throwaway commit adding `research/second_stake/zz_probe.md` and `ci/zz_probe.txt` together | `AssertionError: Lists differ: ['ci/zz_probe.txt'] != []`, exit 1 |
| 2-stake (sealed-path scope, 2026-09-18) | an unrelated commit writing `ci/` is outside this rung's scope, same test at `0b818337` | one throwaway commit adding only `ci/zz_probe.txt` on top of `0b818337` | `ok`, exit 0 for this test: the `ci/` commit touches nothing of this rung.  The branch-level write-scope test, unchanged, still refuses that branch, because the branch also carries a commit of this rung.  A branch with no commit of this rung at all skips both; that is proved in `BoundaryScopeSituationTests`, since staging it for real needs this change on `main` first |
| 2-stake (sealed-path scope, 2026-09-18) | ownership judged on everything a commit wrote, `test_no_rung_commit_writes_a_sealed_path` at `6038cead` | two throwaway commits: one adding `research/second_stake/zz_probe.md` and `ci/zz_probe.txt`, then one removing only `zz_probe.md` | `AssertionError: Lists differ: ['ci/zz_probe.txt'] != []`, exit 1.  The same two commits on `0b818337`, which judged ownership after dropping the reverted path, gave `ok`, exit 0: the review finding this row proves repaired |

<!-- markdownlint-enable MD013 -->

## Session handoff, rung three (2026-09-23)

**Read at the start of a session; written at the end of one.**  The
seed's section eleven asks for a handoff, and the run had none as a file:
until now the next rung was carried only in the last rung's `STATUS.md`.
It still is, and this section says where to look rather than duplicating
it, because two copies of a handoff drift.

- The rungs on `main` are rung zero (`second_inheritance`), rung one
  (`second_stream`), rung two track two (`second_stake`) and rung two
  track one (`second_nofirst`).  Rung three (`second_index`) is this
  session's, and is not merged by an agent.
- The next rung is named at the end of the LAST rung's `STATUS.md`, under
  the heading "The next rung, named so it cannot be smuggled in later",
  with the seed's rule applied to that rung's own leftover list.  Rung
  three's says X-3, the index up to the implemented isomorphism.
- One rung per session at most.  Never merge a rung; the author merges.
- Before writing anything in a new rung: freeze `PROMPT.md` by hash and
  commit it, then freeze `PREDICTIONS.md` by hash and commit it, then
  compute.  The commits are the evidence of the order.

## Injection record, rung three (2026-09-23)

Eight injections, each minimal and reversible, none live while any
receipt was regenerated.  Every one names the object it was given.

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 3 | frozen-text pin (`second_index/verify_pins.py`) | one line appended to `PROMPT.md` in a throwaway commit `bb479a90` on top of `321cfd29` | `FAIL: frozen text moved: research/second_index/PROMPT.md: expected 8487d72e..., got 3452f3e8...`, exit 1; after `git reset --hard HEAD~1` the verifier passed with exit 0 and the tree was clean.  The verifier reads blobs at HEAD, so an uncommitted edit is invisible to it by design; the injection had to be committed to be seen, and was discarded rather than reverted, so no receipt was regenerated under it |
| 3 | span pin (same verifier) | one span's `last_line` moved by one in `SOURCE_MANIFEST.json`, uncommitted | `FAIL: span mismatch at the snapshot for lean4/Derivation/Basic.lean:20-168: expected 3b9f40cb..., got 0c646ee8...`, exit 1; exit 0 after restoring the manifest.  A blob pin and a span pin are different guarantees, and this is the span one firing on its own |
| 3 | receipt comparison (`run_index.py --check`) | one node count in `receipts/index.json` changed from 577 to 578 | `FAIL: ...receipts\index.json differs from a fresh run`, exit 1; exit 0 after restoring the file.  The check writes nothing, so the generator could not bless the drift by overwriting it |
| 3 | Lean audit (`second_index/verify_lean.py`) | one `#print axioms` line deleted from `AxiomReport.lean` | `FAIL: compiler declaration SecondIndex.Index.first_demand_unique has no fresh #print axioms report`, exit 1; exit 0 after restoring the line.  The compiled-environment census and the report population are compared both ways, so dropping a print drops only one side |
| 3 | FW-DEF census totality (`test_census.py`) | one row deleted from `FWDEF_CENSUS.json` and its count decremented | `AssertionError: Lists differ: ['first_demand_follows_a_changing_event'] != []`, exit 1; exit 0 after restoring the row |
| 3 | reconstruction comparison (`test_reconstruction.py`) | one binder renamed in the reconstructed sealed `collapsed`, from `d d'` to `d dd` | the assertion printed both normalized declarations with the differing character marked, exit 1; exit 0 after restoring the binder.  The comparison reads the source blob AT THE SNAPSHOT, so it is a comparison with the pinned revision and not with the working tree |
| 3 | prose census over the write root (`test_forbidden.py`) | a probe file `zz_probe.md` in the write root carrying one watched term | `AssertionError: Lists differ: ['research/second_index/zz_probe.md:1: <term elided>'] != []`, with the watched term named in place of the elision, exit 1; exit 0 after deleting the probe.  RECORDED BESIDE IT: the first probe used the term the rung-one row of this record names, and it did NOT fire -- that term is not in the current watched population.  The term that DID fire is elided above for the same reason the rung-one rows elide theirs: this record is itself scanned.  A probe must be drawn from the list as it stands, not from a record of what it once held.  Why the population moved is not established here, and this rung regenerated no pin |
| 3 | write-root scope scan (`test_forbidden.py`) | an untracked `zz_outside_probe.md` at the repository root | `AssertionError: Lists differ: ['zz_outside_probe.md'] != []`, exit 1; exit 0 after deleting it.  The scan reads uncommitted writes as well as committed ones, so a file outside the root is seen before it is added to Git |
| 3 | coverage census (`second_index/check_coverage.py`) | a new production module `zz_helper.py` in the tree, declared nowhere | `FAIL: production module census differs: missing from declarations=['zz_helper.py'], declared but absent=[]`, exit 1; exit 0 after deleting it.  The census fails in both directions, so a measured file cannot disappear silently either |

<!-- markdownlint-enable MD013 -->

**What these injections do not prove.**  That the populations they pin
are the right mathematical objects.  A perfect pin of the wrong set is
still the wrong set.  Each shows only that the named gate is live and
recovers.

## Session handoff, rung four (2026-09-24)

**Read at the start of a session; written at the end of one.**  As rung
three's handoff says, the next rung is carried in the LAST rung's
`STATUS.md`, and this section says where to look rather than copying it.

- The rungs on `main` at this session's start (`bdbe5832`) are rung zero
  (`second_inheritance`), rung one (`second_stream`), rung two track two
  (`second_stake`), rung two track one (`second_nofirst`) and rung three
  (`second_index`).  Rung four (`second_iso`) is this session's, and is
  not merged by an agent.
- The next rung is named at the end of `research/second_iso/STATUS.md`,
  under "The next rung, named so it cannot be smuggled in later": Y-3,
  symmetry along a history.
- **A registration gap, met twice.**  `tests/test_gates_skill_matches_workflow.py`
  requires `.claude/skills/gates/SKILL.md` to name every gate script the
  workflow runs.  A rung registers its scripts in the workflow and may
  hand-edit nothing else outside its write root, so the rung's own pull
  request cannot keep that test green.  Rung three's registration left it
  red on `main` until `db434a28`.  This session opened the skill edit as
  its own pull request against `main`, not stacked, on branch
  `fix/gates-skill-rung-four`; the test is green once both have landed,
  in either order.  The residual, recorded and not repaired here: the
  rung contract and this test disagree, and each future rung will meet it.
  Whether the skill joins the generated views a rung may write is the
  author's call.
- One rung per session at most.  Never merge a rung; the author merges.
- Before writing anything in a new rung: freeze `PROMPT.md` by hash and
  commit it, then freeze `PREDICTIONS.md` by hash and commit it, then
  compute.  The commits are the evidence of the order.  Read every
  supplied receipt a prediction leans on before freezing it: rung four's
  one computational miss (J-12) came from reasoning about the Lean reading
  regimes while the Python readings, whose receipt was already on `main`,
  differ from them.

## Injection record, rung four (2026-09-24 and 2026-09-25)

Eleven injections, each minimal and reversible, none live while any
receipt was regenerated.  All were run in a throwaway worktree detached at
`6c852dba`, the rung branch's head at the time, so that none could race
the root test suite running in the rung's own worktree, and that worktree
was removed afterwards.  Every one names the object it was given.

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 4 | frozen-text pin (`second_iso/verify_pins.py`) | one line appended to `PROMPT.md` in a throwaway commit `5e610375` on top of `6c852dba` | `FAIL: frozen text moved: research/second_iso/PROMPT.md: expected 833fb3b3..., got e25440c2...`, exit 1; after `git reset --hard HEAD~1`, exit 0 and a clean tree |
| 4 | span pin, the new sealed span (same verifier) | the `Minimality.lean` span's `last_line` moved from 224 to 225 in `SOURCE_MANIFEST.json`, uncommitted | `FAIL: span mismatch at the snapshot for lean4/Derivation/Minimality.lean:169-225: expected 4856138d..., got 7ea30d05...`, exit 1; exit 0 after restoring the manifest |
| 4 | receipt comparison (`run_iso_index.py --check`) | the first `"classes": 402` in `receipts/iso_index.json` changed to 403 | `FAIL: ...receipts\iso_index.json differs from a fresh run`, exit 1; exit 0 after `git checkout`.  The check writes nothing |
| 4 | Lean axiom whitelist (`second_iso/verify_lean.py`) | a theorem `zzz_probe_choice` proved by `Classical.em`, appended to `Countermodel.lean` with its report line | three failures naming it: no FW-DEF row; `depends on disallowed axioms ['Classical.choice']`; a fresh report the committed log lacks; exit 1, then `lean audit clean: 11 sources, 84 axiom reports`.  RECORDED BESIDE IT: the same gate had already fired on a real defect before any injection, naming nineteen theorems whose proofs reached `Classical.choice` through two `simp` calls; see `research/second_iso/STATUS.md` |
| 4 | Lean compiler census (same verifier) | the `#print axioms` line for `SecondIso.Transport.demand_transport` deleted from `AxiomReport.lean` | `FAIL: compiler declaration SecondIso.Transport.demand_transport has no fresh #print axioms report`, exit 1; exit 0 after restoring |
| 4 | FW-DEF census totality (`test_census.py`) | the `demand_transport` row deleted and the CONTENT count decremented | `AssertionError: Lists differ: ['demand_transport'] != []` from the totality test, plus the dated-count and prediction tests naming it; exit 1, then OK |
| 4 | reconstruction faithfulness (`test_reconstruction.py`) | the binder of the reconstructed sealed `collapsed_transport` renamed from `d d'` to `d dd` in `IsoKernel.lean` | `AssertionError: Lists differ: ['lean4/Derivation/IsoCollapse.lean -> IsoKernel.lean: collapsed_transport'] != []`, exit 1; OK after restoring.  The comparison reads the PARKED sealed module at the snapshot |
| 4 | prose census over the write root (`test_forbidden.py`) | a probe `zz_probe.md` in the write root carrying one term confirmed watched by `ci/check_prose_watchlist.py --probe` | `AssertionError: Lists differ: ['research/second_iso/zz_probe.md:1: <term elided>'] != []`, the term named in place of the elision; OK after deleting the probe.  The term is elided because this record is itself scanned |
| 4 | write-root scope scan (`test_forbidden.py`) | an untracked `zz_outside_probe.md` at the repository root | `AssertionError: Lists differ: ['zz_outside_probe.md'] != []`, exit 1; OK after deleting it |
| 4 | coverage module census (`second_iso/check_coverage.py`) | an undeclared production module `zz_helper.py` in the tree | `FAIL: production module census differs: missing from declarations=['zz_helper.py'], declared but absent=[]`, exit 1.  RECORDED BESIDE IT: the first recovery run failed for a different reason, `verify_pins.py is declared measured but is absent from the report`, because the report had been generated from one test module only; the gate refused a partial report by name.  With the full suite under coverage it passed, exit 0 |
| 4 | registration scan (`test_forbidden.py`) | the line `python run_iso_index.py --check` deleted from the rung's step in `.github/workflows/verify.yml` | `AssertionError: 'python run_iso_index.py --check' not found in` the rung's block, exit 1; OK after restoring |

<!-- markdownlint-enable MD013 -->

**What these injections do not prove.**  That the populations they pin
are the right mathematical objects, or that the Lean stake formulas are
the sibling Python rules: that last is checked by transcription on a
finite range, and a transcription is not the text it transcribes.

## Session handoff, rung five (2026-09-25)

**Read at the start of a session; written at the end of one.**  As the
earlier handoffs say, the next rung is carried in the LAST rung's
`STATUS.md`, and this section says where to look rather than copying it.

- The rungs on `main` at this session's start (`630622da`) are rung zero
  (`second_inheritance`), rung one (`second_stream`), rung two track two
  (`second_stake`), rung two track one (`second_nofirst`), rung three
  (`second_index`) and rung four (`second_iso`).  Rung five
  (`second_symmetry`) is this session's, and is not merged by an agent.
- The next rung is named at the end of `research/second_symmetry/STATUS.md`,
  under "The next rung, named so it cannot be smuggled in later": Z-4,
  succession through the element count.
- **The registration gap rung four met is closed by rule.**  The author's
  ruling of 2026-09-25 in `CLAUDE.md` lets a rung add its own gate scripts
  to `.claude/skills/gates/SKILL.md`.  This rung did so in its own pull
  request, and `tests/test_gates_skill_matches_workflow.py` passed on the
  rung branch before it was opened.  `test_forbidden.py` now lists the
  skill beside the workflow and this manual as a shared file a rung may
  append to, and checks that no line of it is removed.
- **Line endings in a throwaway worktree.**  This machine checks files
  out with CRLF, so an injection script that edits by exact text must
  convert its line endings first; the first run of this rung's did not,
  and refused its own edit before injecting anything.  And a new worktree
  has no `coverage.json`: the coverage census must be given a report of
  the full suite before an injection into it, or it fails on the missing
  report and not on the injected module.  Both are recorded beside the
  table below.
- One rung per session at most.  Never merge a rung; the author merges.
- Before writing anything in a new rung: freeze `PROMPT.md` by hash and
  commit it, then freeze `PREDICTIONS.md` by hash and commit it, then
  compute.  The commits are the evidence of the order.

## Injection record, rung five (2026-09-25)

Twelve injections, each minimal and reversible, none live while any
receipt was regenerated.  All were run in a throwaway worktree detached at
`c60a0065`, the rung branch's head at the time, so that none could race
the rung's own worktree, and that worktree was removed afterwards with a
clean status.  Every one names the object it was given.

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 5 | frozen-text pin (`second_symmetry/verify_pins.py`) | one line appended to `PROMPT.md` in a throwaway commit `27ad905e` on top of `c60a0065` | `FAIL: frozen text moved: research/second_symmetry/PROMPT.md: expected 7b3f73c0..., got 6acbd072...`, exit 1; after `git reset --hard HEAD~1`, exit 0 and a clean tree |
| 5 | span pin (same verifier) | the `Minimality.lean` span's `last_line` moved from 224 to 225 in `SOURCE_MANIFEST.json`, uncommitted | `FAIL: span mismatch at the snapshot for lean4/Derivation/Minimality.lean:169-225: expected 4856138d..., got 7ea30d05...`, exit 1; exit 0 after restoring the manifest |
| 5 | receipt comparison (`run_symmetry.py --check`) | `"largest": 240` in `receipts/symmetry.json` changed to 241 | `FAIL: ...receipts\symmetry.json differs from a fresh run`, exit 1; exit 0 after `git checkout`.  The check writes nothing |
| 5 | Lean axiom whitelist (`second_symmetry/verify_lean.py`) | a theorem `zzz_probe_choice` proved by `Classical.em`, appended to `Witness.lean` with its report line | three failures naming it: no FW-DEF row; `depends on disallowed axioms ['Classical.choice']`; a fresh report the committed log lacks; exit 1, then `lean audit clean: 9 sources, 64 axiom reports` |
| 5 | Lean compiler census (same verifier) | the `#print axioms` line for `SecondSymmetry.Aut.inst_descends_of_fixed` deleted from `AxiomReport.lean` | `FAIL: compiler declaration SecondSymmetry.Aut.inst_descends_of_fixed has no fresh #print axioms report`, exit 1; exit 0 after restoring |
| 5 | FW-DEF census totality (`test_census.py`) | the `datum_lift` row deleted and the CONTENT count decremented | `AssertionError: Lists differ: ['datum_lift'] != []` from the totality test and from the axiom-log coverage test; exit 1, then OK |
| 5 | reconstruction comparison (`test_reconstruction.py`) | the binder `hreqs` of the reconstructed sealed `isoRefl` renamed to `hreq` in `IsoKernel.lean` | `AssertionError: Lists differ: ['lean4/Derivation/Minimality.lean -> IsoKernel.lean: isoRefl'] != []`, exit 1; OK after restoring.  The comparison reads the sealed blob AT THE SNAPSHOT |
| 5 | prose census over the write root (`test_forbidden.py`) | a probe `zz_probe.md` in the write root carrying one term confirmed watched by `ci/check_prose_watchlist.py --probe` | `AssertionError: Lists differ: ['research/second_symmetry/zz_probe.md:1: <term elided>'] != []`, the term named in place of the elision; OK after deleting the probe.  The term is elided because this record is itself scanned |
| 5 | write-root scope scan (`test_forbidden.py`) | an untracked `zz_outside_probe.md` at the repository root | `AssertionError: Lists differ: ['zz_outside_probe.md'] != []`, exit 1; OK after deleting it |
| 5 | coverage module census (`second_symmetry/check_coverage.py`) | an undeclared production module `zz_helper.py` in the tree | `FAIL: production module census differs: missing from declarations=['zz_helper.py'], declared but absent=[]`, exit 1; exit 0 after deleting it.  RECORDED BESIDE IT: the first attempt ran in the fresh worktree before any coverage report existed, and the gate failed on `coverage.json is missing` -- the right refusal for the wrong reason, so it was not counted.  The report was generated from the full suite and the injection repeated |
| 5 | registration scan (`test_forbidden.py`) | the line `python run_symmetry.py --check` deleted from the rung's step in `.github/workflows/verify.yml` | `AssertionError: 'python run_symmetry.py --check' not found in` the rung's block, exit 1; OK after restoring |
| 5 | the datum law, through the receipt and the scoring (`run_symmetry.py --check`; `test_symmetry.py`) | `untouched_data` in `symmetry.py` made to count one datum too many whenever any datum is touched | `FAIL: ...receipts\symmetry.json differs from a fresh run`, exit 1; and the scored-verdict test `AssertionError: Lists differ: ['K-10', 'K-11', 'K-13', ...] != ['K-10', 'K-11', 'K-12', 'K-13', ...]`, naming K-12 as the row that fell; both recover after restoring the function |

<!-- markdownlint-enable MD013 -->

**What these injections do not prove.**  That the populations they pin
are the right mathematical objects, or that a size law checked on the
rectangle holds beyond it: the Lean of this rung proves which
automorphisms survive, never how many there are, and a law about sizes
is a finite computation until it is proved.

## Session handoff, rung six (2026-09-25)

**Read at the start of a session; written at the end of one.**  As the
earlier handoffs say, the next rung is carried in the LAST rung's
`STATUS.md`, and this section says where to look rather than copying it.

- The rungs on `main` at this session's start (`144d9c2b`) are rung zero
  (`second_inheritance`), rung one (`second_stream`), rung two track two
  (`second_stake`), rung two track one (`second_nofirst`), rung three
  (`second_index`), rung four (`second_iso`) and rung five
  (`second_symmetry`).  Rung six (`second_succession`) is this session's,
  and is not merged by an agent.
- The next rung is named at the end of
  `research/second_succession/STATUS.md`, under "The next rung, named so
  it cannot be smuggled in later": W-1, duration under the CHANGING
  reading.
- **A leftover that refines a decided row is not eligible.**  This rung
  named W-2, the full set of counts a base and a regime admit, and
  recorded it as extending no row of the census, because the succession
  row it refines is decided here.  The seed's rule reads "extends the
  census"; a refinement of a decided row is recorded, priced, and left.
- **A statement proved again is credited, not counted.**  The package is
  self-contained, so two of rung five's statements are proved again in it.
  The ledger and the census note say so, and `test_census.py` checks that
  the module and the note carry the credit.
- One rung per session at most.  Never merge a rung; the author merges.
- Before writing anything in a new rung: freeze `PROMPT.md` by hash and
  commit it, then freeze `PREDICTIONS.md` by hash and commit it, then
  compute.  The commits are the evidence of the order.

## Injection record, rung six (2026-09-25)

Twelve injections, each minimal and reversible, none live while any
receipt was regenerated.  All were run in a throwaway worktree detached at
`75d5ee72`, the rung branch's head at the time, by one script that edited
with line endings preserved and checked each recovery; the worktree was
clean after the last reversal and was then removed.  Every one names the
object it was given.

<!-- markdownlint-disable MD013 -->

| rung | gate | injection | observed failure |
|---|---|---|---|
| 6 | frozen-text pin (`second_succession/verify_pins.py`) | one line appended to `PROMPT.md` in a throwaway commit `40d770c9` on top of `75d5ee72` | `FAIL: frozen text moved: research/second_succession/PROMPT.md: expected ac592808..., got b5750061...`, exit 1; after `git reset --hard HEAD~1`, exit 0 |
| 6 | span pin (same verifier) | the Z-4 span's `last_line` moved from 198 to 199 in `SOURCE_MANIFEST.json`, uncommitted | `FAIL: span mismatch at the snapshot for research/second_symmetry/STATUS.md:194-199: expected 6b3f4b34..., got 122dbe59...`, exit 1; exit 0 after restoring the manifest |
| 6 | receipt comparison (`run_succession.py --check`) | the first `"split_regimes": 33` in `receipts/succession.json` changed to 34 | `FAIL: ...receipts\succession.json differs from a fresh run`, exit 1; exit 0 after restoring the bytes.  The check writes nothing |
| 6 | Lean axiom whitelist (`second_succession/verify_lean.py`) | a theorem `zzz_probe_choice` proved by `Classical.em`, appended to `Readings.lean` with its report line | three failures naming it: no FW-DEF row; `depends on disallowed axioms ['Classical.choice']`; a fresh report the committed log lacks; exit 1, then `lean audit clean: 6 sources, 34 axiom reports` |
| 6 | Lean compiler census (same verifier) | the `#print axioms` line for `SecondSuccession.Count.changes_counted` deleted from `AxiomReport.lean` | `FAIL: compiler declaration SecondSuccession.Count.changes_counted has no fresh #print axioms report`, exit 1; exit 0 after restoring |
| 6 | FW-DEF census totality (`test_census.py`) | the `changes_counted` row deleted and the CONTENT count decremented | `AssertionError: Lists differ: ['changes_counted'] != []` from the totality and axiom-log tests, and the dated-count and prediction tests naming it; exit 1, then OK |
| 6 | reconstruction comparison (`test_reconstruction.py`) | the binder of the reconstructed sealed `collapsed` renamed from `d d'` to `d dd` in `Kernel.lean` | `AssertionError: Lists differ: ['lean4/Derivation/Basic.lean -> Kernel.lean: collapsed'] != []`, exit 1; OK after restoring.  The comparison reads the sealed blob AT THE SNAPSHOT |
| 6 | prose census over the write root (`test_forbidden.py`) | a probe `zz_probe.md` in the write root carrying the one term whose watchlist digest begins `4cbe0959`, confirmed watched by `ci/check_prose_watchlist.py --probe` | `AssertionError: Lists differ: ['research/second_succession/zz_probe.md:1: <term elided>'] != []`, the term named in place of the elision; OK after deleting the probe.  The term is elided because this record is itself scanned |
| 6 | write-root scope scan (`test_forbidden.py`) | an untracked `zz_outside_probe.md` at the repository root | `AssertionError: Lists differ: ['zz_outside_probe.md'] != []`, exit 1; OK after deleting it |
| 6 | coverage module census (`second_succession/check_coverage.py`) | an undeclared production module `zz_helper.py` in the tree, after a report of the full suite had been generated and had passed | `FAIL: production module census differs: missing from declarations=['zz_helper.py'], declared but absent=[]`, exit 1; exit 0 after deleting it |
| 6 | registration scan (`test_forbidden.py`) | the line `python run_succession.py --check` deleted from the rung's step in `.github/workflows/verify.yml` | `AssertionError: 'python run_succession.py --check' not found in` the rung's block, exit 1; OK after restoring |
| 6 | the CHANGING law, through the receipt and the scoring (`run_succession.py --check`; `test_succession.py`) | `element_count` in `succession.py` made to leave out the uniform rules | `FAIL: ...receipts\succession.json differs from a fresh run`, exit 1; and the scored-verdict test `AssertionError: Lists differ: ['M-10', 'M-11', 'M-12', 'M-13', 'M-8'] != [..., 'M-9']`, naming M-9 as the row that fell; both recover after restoring the function |

<!-- markdownlint-enable MD013 -->

**What these injections do not prove.**  That the populations they pin
are the right mathematical objects, or that the count up to the
isomorphism behaves beyond the rectangle as it does inside it: the Lean of
this rung never mentions the isomorphism, and the class-level answer is a
finite computation until Z-1 is proved.
