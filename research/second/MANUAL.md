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
cd research/second_<r> && python -m unittest discover -s . -p "test_*.py" && python -m mypy && cd ../..
python ci/check_prose_watchlist.py
python -m pytest tests/test_primitive_contact.py -q -k firewall -p no:cacheprovider
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

| rung | gate | injection | observed failure |
|---|---|---|---|
| 0 | frozen-text pin (`second_inheritance/verify_pins.py`) | one line appended to `PROMPT.md` in a throwaway commit `08cb4808` on top of `f2d40f59`, 2026-09-03 | `FAIL: frozen text moved: research/second_inheritance/PROMPT.md: expected aa804ee3…, got 9b2498ce…`, exit 1; after `git reset --hard HEAD~1` the verifier passed with exit 0 and the tree was clean. The verifier reads blobs at HEAD, so an uncommitted edit is invisible to it by design; the injection therefore had to be committed to be seen, and was discarded, not reverted, so no receipt was regenerated under it |
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
