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
| 2 (track 1) | Lean module census, derived not hand-listed | `theorem zzz_probe_unlisted` added to `Stake.lean` without regenerating the report | `FAIL: SecondNoFirst.Stake.zzz_probe_unlisted is declared in Stake.lean but not listed in AxiomReport.lean`, exit 1, then 0. The census enumerates modules from the filesystem and namespaces from each module's own `namespace` lines, so a hand list cannot go stale |
| 2 (track 1) | coverage floor (`second_nofirst/check_coverage.py`) | the floor raised from ninety-five to ninety-nine point nine | `FAIL: line coverage 98.66% is below 100%; branch coverage 95.28% is below 100%`, exit 1, then 0 |
| 2 (track 1) | coverage measured-set drift | `verify_pins.py` removed from the declared measured set | `FAIL: verify_pins.py is in the report but is neither declared measured nor declared excluded`, exit 1, then 0. The gate fails in both directions, so the set cannot shrink silently to flatter the number |
| 2 (track 1) | coverage staleness | `nofirst.py` touched after the report was written | `FAIL: nofirst.py was modified after the report was written (2026-09-04T11:37:03.162241); regenerate coverage.json`, exit 1, then 0 after regenerating |
| 2 (track 1) | FW-DEF census totality (`second_nofirst/test_census.py`) | the `fresh_profile` row deleted from `FWDEF_CENSUS.json` | `test_the_census_is_total_in_both_directions` failed with the two lists differing by that name, exit 1, then 0 |
| 2 (track 1) | FW-DEF census classification | `wf_step_inert` refiled from CONTENT to DEFINITION | `AssertionError: Lists differ: ['grammar_carries_no_stake (22 lines)', 'wf_step_inert (27 lines)'] != []`, exit 1, then 0. This probe also found a real defect in the gate as first written and changed the tree; see `research/second_nofirst/STATUS.md` |
| 2 (track 1) | prose census over the write root | one line carrying a watched noun appended to the rung's `STATUS.md` | `AssertionError: Lists differ: ['research/second_nofirst/STATUS.md:333: <term>'] != []`, exit 1, then 0, with `<term>` the watched noun, redacted here because writing it would put it into a tracked file and fail the root gate. The rung runs the repository's own scanner over its own tree, so a watched term fails there rather than waiting for the root gate; the census pin was NOT regenerated |
| 2 (track 1) | FW-OB1 discharge scan | a sentence appended to the rung's `STATUS.md` asserting the sealed obstruction had been discharged, redacted here | the scan named `research/second_nofirst/STATUS.md:333` and the matching pattern, exit 1, then 0. The scan has no carve-out for negation; the one line of the tree that states the refusal is excepted by DIGEST of its exact bytes |
| 2 (track 1) | reconstruction faithfulness, binder (`second_nofirst/test_reconstruction.py`) | `collapsed`'s second binder renamed from `d'` to `dd` in the reconstructed `Kernel.lean` | the normalized bodies differ and the assertion prints both, exit 1, then 0 after reversal.  A pin proves a source did not move; this gate proves the reconstruction says the same thing, which no pin can |
| 2 (track 1) | reconstruction faithfulness, hypothesis | `collapsed_of_no_insts`'s hypothesis weakened from `r.insts = []` to `r.insts = r.insts` | `AssertionError: Lists differ: ['lean4/Derivation/Inertia.lean -> Kernel.lean: collapsed_of_no_insts'] != []`, exit 1, then 0.  The sources are read by git blob AT THE SNAPSHOT, so the comparison is against the pinned revision and not against a working tree that may have moved |

<!-- markdownlint-enable MD013 -->
