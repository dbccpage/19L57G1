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
