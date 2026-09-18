# research/_scaffold — canonical copy-source for research trees

AuthorityEffect: None. Outside the seal; consumes nothing; pins nothing.

Every `research/<tree>/` is deliberately **self-contained**: it keeps its own
`check_coverage.py`, `run.py`, `verify_sources.py`, `verify_lean.py`,
`verify.py`, `evidence/`, `tests/`, and prose, so it can be verified and its
custody reasoned about in isolation. Nothing here is imported by a tree — a
shared import would make the trees depend on this directory and break that
isolation. Instead, new trees **copy** the two files below.

The cost of copy-based reuse is that a bug pasted once gets pasted again. Two
defects recurred that way across the recent scaffold generation:

1. **`check_coverage.py` COVERAGE_LEAK by substring** (correctness). The gate
   matched omit directories with `part in path` — a substring test — so a
   measured module under a directory like `clean/` (contains `lean/`) or
   `subtests/` (contains `tests/`) was falsely flagged and failed the gate. It
   also computed the two percentages through two divergent numeric paths (one
   accepting `bool`). Fixed in PRs #153/#154/#155.
2. **`run.py` double custody scan** (efficiency). `receipt_bytes()` ran the
   expensive `verify_sources()` twice — before and after a record computation
   that writes no files — so the second scan is redundant.

## Use it

When you start a new `research/<tree>/`:

- Copy [`check_coverage.py`](check_coverage.py) verbatim; edit only
  `REQUIRED_FILES`.
- Copy [`run.py`](run.py) verbatim; edit only `RECORD`, the `compute()` body,
  and the messages. Keep the single `verify_sources()` call.

Do **not** copy an older tree's `check_coverage.py` / `run.py` — that is how the
bugs spread.

Register the tree in `research/README.md`: run
`python ci/research_index.py --write` and commit the result.
`tests/test_research_index.py`, part of the root suite, fails until the tree
has a row, and again when it is registered in or out of the workflow's
research job. A tree whose own boundary test or charter forbids writes
outside its root either lists `research/README.md` among its declared shared
paths, as it does `.github/workflows/verify.yml`, or has the row added in a
separate commit on the same branch by whoever opens the pull request; a
commit that touches only `research/README.md` is not one of the tree's own.

## Keep the family in sync

`python research/_scaffold/check_scaffold.py` scans every `research/<tree>/` and:

- **fails (exit 1)** if the substring `COVERAGE_LEAK` form (`OMIT_PARTS` without
  `_directories`) reappears anywhere — a correctness bug that must never ship;
- **warns (exit 0)** on any `run.py` with two `verify_sources()` calls.

The double-scan is only warned, not blocked, because it **cannot be retrofitted
freely**: several older trees pin each other's whole `.py` tree at a baseline
commit (e.g. `record_reading` pins `setting_translation`,
`represented_execution`, and `coherent_process_limits`), so editing one tree's
`run.py` breaks a consumer's custody and cascades repins. Drop the second scan
in a **new** tree at creation, before any consumer pins it; an existing pinned
tree is left until its family is deliberately repinned.

## Known warnings today

`check_scaffold.py` currently warns on the double scan in these already-pinned
trees (left as-is by design): `coherent_process_limits`, `ignition`,
`local_reuse`, `magnification`, `record_reading`, `represented_execution`,
`setting_translation`.
