# cost_cohomology: status

AuthorityEffect: None.

- **Gate 11 Status**: Not in Gate 11.
- **Receipts**: Local receipts only.  No receipt file is committed: the
  receipt and its writer were removed in `f3ea95fc`.
- **Verification**: `python research/cost_cohomology/test_cost_cohomology.py`
  (five unittest checks) and `python research/cost_cohomology/verify_sources.py`
  (source pins).

## Dated notes

- **2026-09-24, withdrawn**: this file said the tree was "verified via local
  Python test suite and programmatic verification script (`verify.py`)".
  No `verify.py` has ever existed in this tree; `git log --all` finds no
  such path.  The claim is withdrawn.  The verification is the test suite
  and the source-pin script named above.
- **2026-09-24, repaired**: from `2914032f` (2026-09-13) the suite failed
  on main.  `test_no_numpy_float_rank_module` pinned the tree's Python
  files to exactly `test_cost_cohomology.py`, and the custody ratchet added
  `verify_sources.py` without updating the pin.  The pin now names both
  files and still fails on any other module.  The check that no module
  imports numpy is now explicit.  No gate ran the suite, so the failure
  went unnoticed.  Tests: 3 of 4 passing before, 5 of 5 after.  The added
  check pins the |V| = 262, |E| = 638 and two-component counts the README
  states.
