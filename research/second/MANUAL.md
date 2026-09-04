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
| 1 | operator-vocabulary digest scan (`second_stream/test_forbidden.py`) | a probe file in the write root carrying one watched word, 2026-09-04 | `AssertionError: Lists differ: ['zz_review_probe.md:1: topology'] != []`, exit 1; exit 0 after deleting the probe.  The scan stores the terms only as sha256 digests, never as text, so the committed file does not carry what it watches for |
| 1 | the same scan, multi-word terms | a probe carrying a two-word, a three-word and a second two-word term | the failure named all three, so the phrase passes are live and not decoration; exit 1, exit 0 after deletion.  The three tokens are elided here rather than quoted, because this record is itself scanned — the same trap the root census caught in a sibling tree, met again and recorded again |
| 1 | root census scan (`CensusScan`) | a probe carrying a word confirmed watched at the root by `ci/check_prose_watchlist.py --probe` | the scan named the file, the line and the token, exit 1; exit 0 after deletion.  The token is elided here because this file is itself scanned |
| 1 | identifier firewall (`DenylistScan`) | a probe carrying two working-denylist identifiers, plus a suffixed and a prefixed form as negative controls | the failure named exactly the two whole identifiers and NOT the two substring forms, which is the repair the author made to a sibling tree, confirmed live here rather than inherited on trust; exit 1, then 0 |
| 1 | outside-write-root scan | a file created at `research/zz_review_probe_outside.txt`, outside the write root and under no sealed prefix | `AssertionError: … ['?? research/zz_review_probe_outside.txt'] != [] : a path outside the write set is touched`, exit 1; exit 0 after deletion |
| 1 | source pin at the snapshot (`second_stream/verify_pins.py`) | one hex digit changed in the pinned `code/derivation/model.py` digest | `FAIL: snapshot hash mismatch for code/derivation/model.py: expected 7A7FD2BA…, got 6A7FD2BA…`, exit 1; exit 0 after byte-exact restore |
| 1 | source pin at HEAD — the half that only a second check can see | in a throwaway clone at `cdefee90`, a committed change to `code/derivation/model.py` with the snapshot copy left intact | `FAIL: source moved at HEAD for code/derivation/model.py`, exit 1.  Pinning at the snapshot alone would have passed; this is why the verifier checks twice |
| 1 | frozen-text pin | in the same clone, one line appended to `PROMPT.md` and committed | `FAIL: frozen text moved: research/second_stream/PROMPT.md: expected efca5d96…, got 9e96bcf8…`, exit 1 |
| 1 | frozen-text pin, the recorded blind spot and its cover | an UNSTAGED on-disk edit to `PROMPT.md` | `verify_pins.py` reads blobs, so it passed at exit 0 — the blind spot is real and is documented rather than hidden.  The cover was then proved: with the same edit live, `run_stream.py` hashes from disk and refused, so the pair of checks closes what neither closes alone |
| 1 | the four declared budgets | each constant lowered until it fired | each recorded its own named terminal carrying the tree, the node, the demand kind, the target and the bound, and the truncated node attached nothing |
| 1 | the prediction scorer | a synthetic receipt fragment built to score MISSED | the scorer emitted MISSED rather than HIT, so a scoreboard of hits is not a rubber stamp; an empty population separately emitted VACUOUS and was never rounded up |
