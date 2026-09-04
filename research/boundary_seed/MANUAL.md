# MANUAL: operating the boundary derivation

`AuthorityEffect: None`.  Apparatus only.

## Declared readings, recorded before the first challenge

0. **Blindness is by rule, not by ignorance.**  The instrument that
   opened this run drafted the seed in the same session, after reviewing
   the sealed derivation and its research trees in detail, and remembers
   their vocabulary and results.  Every result below is derived from the
   seed and the tree's own code and proofs; where the run notices itself
   reaching for a remembered result instead of deriving one, it says so
   in the challenge's `STATUS.md` next to the result.  Nothing under
   `paper/`, `artifacts/`, `lean4/Derivation/`, `code/derivation/`, or
   another research tree is opened by this run before `FREEZE.md` exists,
   and `test_blind.py` enforces the part of that which a test can see.
1. **The seed's author and the first session coincide**, as they did for
   the second derivation.  Later challenges are to be opened in fresh
   sessions with nothing beyond `CLAUDE.md`'s five named sections and the
   seed.
2. **Two-ness is not assumed of the sides.**  Reading U and reading O are
   carried as separate towers; a result that holds under one and not the
   other is stated under its reading in the same sentence.

## Commands

From the repository root, for a challenge `<k>`:

```text
python research/boundary_seed/verify_pins.py
python research/boundary_seed/run_challenge<k>.py
cd research/boundary_seed && python -m unittest discover -s tests -p "test_*.py" && python -m mypy && python check_coverage.py && cd ../..
python ci/check_prose_watchlist.py
python -m pytest tests/test_primitive_contact.py -q -k firewall -p no:cacheprovider
```

## Session protocol

Read the handoff, the seed, `PLAN.md`, this file, and the latest
challenge's `STATUS.md`; close at most one challenge or continuation
stage; write the handoff; never merge.

## Injection record

| challenge | gate | injection | observed failure |
|---|---|---|---|
