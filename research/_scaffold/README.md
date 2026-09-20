# research/_scaffold — canonical copy-source for research trees

AuthorityEffect: None. Outside the seal; copy sources and the new-tree contract.

2026-09-20: the earlier "consumes nothing; pins nothing" description is withdrawn
for the new additions. The generator copies the root toolchain declaration, and
the contract fixes an existing-directory list at its recorded baseline.

Every `research/<tree>/` is deliberately **self-contained**: it keeps its own
`check_coverage.py`, `run.py`, `verify_sources.py`, `verify_lean.py`,
`verify.py`, `evidence/`, `tests/`, and prose, so it can be verified and its
custody reasoned about in isolation. Nothing here is imported by a tree — a
shared import would make the trees depend on this directory and break that
isolation. New trees use the generator in the new-tree contract section below. The two
earlier copy sources remain available when a tree needs their coverage or
record runners.

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

When a tree needs these earlier coverage or record runners:

- Copy [`check_coverage.py`](check_coverage.py) verbatim; edit only
  `REQUIRED_FILES`.
- Copy [`run.py`](run.py) verbatim; edit only `RECORD`, the `compute()` body,
  and the messages. Keep the single `verify_sources()` call.

Do **not** copy an older tree's `check_coverage.py` / `run.py` — that is how the
bugs spread.

Register the tree in `research/README.md`: stage its files (`git add`), run
`python ci/research_index.py --write`, which reads the git index, and commit
the result. `tests/test_research_index.py`, part of the root suite, fails
until the tree has a row, and again when it is registered in or out of the
workflow's research job. The row is inserted in name order, so it is not an
append. A tree whose boundary checks look at each of its own commits can take
the row in a separate commit on the same branch; a tree whose boundary test
checks the whole branch diff must list `research/README.md` as a declared
shared path that it does not require to be append-only.

## Keep the family in sync

`python research/_scaffold/check_scaffold.py` scans every `research/<tree>/` and:

- **fails (exit 1)** if the substring `COVERAGE_LEAK` form (`OMIT_PARTS` without
  `_directories`) reappears anywhere — a correctness bug that must never ship;
- **fails (exit 1)** on a quote-excluding name capture in an axiom-report
  pattern — `'([^']+)' does not depend on any axioms` and its relatives — in
  any `.py` file under `research/` (added 2026-09-18). A primed theorem name
  ends in a quote character, so that capture stops short and the report is
  dropped without a word; the fixed form is `'(.+?)'`, with its comment, in
  `research/balance_carrier/verify_lean.py`. The check reads string literals,
  which `research/house_diff.py` blanks and so cannot see;
- **warns (exit 0)** on any `run.py` that calls `verify_sources()` twice.

The capture check has two pinned lists, keyed by path and pinned to the
SHA-256 of the file's committed bytes, and it prints both on every run:

- `FROZEN_EXCEPTIONS` holds one file, `research/boundary_seed/verify_lean.py`,
  which `research/boundary_seed/verify_freeze.py` freezes. It is the one
  permanent exception.
- `REPAIR_PENDING` holds the remaining files from the eight that carried the
  capture on 2026-09-18, printed as `DEFECT, repair pending`. Narrowed
  2026-09-19: five entries have been repaired and removed; the earlier
  present-tense count of eight is withdrawn. Three files remain in two
  trees whose frozen source checks already fail on the current main.
  It only shrinks:
  `tests/test_research_drift.py` fails if it names a path it did not name on
  that day. An entry excuses its pinned bytes and nothing else, so once a file
  is edited the entry fails the check until the capture is repaired and the
  entry deleted. Repair a tree in the tree's own commit, then delete its entry
  here in a separate commit.

Neither list makes the capture an accepted form. The two error checks also run
over the live tree in the root suite, through `tests/test_research_drift.py`.

Until 2026-09-18 the double-scan warning counted the text `verify_sources()`,
so a comment naming the call read as a second scan: `diagonal_identity`, which
copied the canonical `run.py` and its comment, was warned on with one call. It
now counts calls in the syntax tree.

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

## Do not reuse a standard-library module name

`research/limit_and_observer/code/` is a regular package: it has an
`__init__.py`, and the tree imports it as `code.calibration`,
`code.census` and so on. So whenever `research/limit_and_observer/` comes
first on `sys.path`, as it does for `python -m ...` or `python -c ...`
started in that directory and for a script in it run directly,
`import code` finds the tree's package and not Python's built-in `code`
module. Measured on 2026-09-18 with Python 3.14.2:

- `import pdb` fails there with `AttributeError: module 'code' has no
  attribute 'InteractiveConsole'`, because the debugger subclasses that
  class when it is imported;
- `python -m pytest` started there stops with `INTERNALERROR` on the same
  error before it collects a test, because pytest imports the debugger.

The tree's registered test commands use `python -m unittest` and
`python -m coverage run -m unittest`, and `import unittest` does not import
the debugger, so those commands still run. Use them in that tree, or start
the tool from another directory. The package is not renamed here: the
tree's `run_price.py` and 11 of its test files import it by that name, and
its `mypy.ini` file list, `.coveragerc` and `check_coverage.py` name the
directory, so a rename is a deliberate change to that tree, not a scaffold
note.

Two other tracked research files share a name with a standard-library
module (census of 2026-09-18 against Python 3.14.2's list of 297 names):

- `research/g013_trace_calculus/trace.py`: `import trace` started in that
  directory gets the tree's file. The tree's 21 tests pass under
  `python -m pytest` there, and
  `research/e2e_tests/adversarial_challenge_cohort4.py` puts the directory
  first on `sys.path` on purpose so that this file wins.
- `research/x310_vertical_integration/types.py`: the interpreter has already
  loaded the built-in `types` before the directory is searched, and the tree
  imports its own file as `.types`; its 27 tests pass under
  `python -m pytest` there. mypy started in that directory refuses to check
  it, exit 2: `"types.py" shadows library module "types"`.

For a new tree, give each source file and package a name that no
standard-library module has; `sys.stdlib_module_names` lists them. A
directory without `__init__.py` is only a namespace package, and the
built-in module still wins over it. That is why the repository's own
top-level `code/`, which has no `__init__.py`, does not hide the built-in
module.

## New-tree contract (2026-09-20)

Existing research directories are grandfathered by the exact list and baseline
commit in `grandfathered.json`; their naming and verifier bytes are unchanged.
The new contract is checked by `python ci/check_new_research_trees.py` and by
the root test suite. The fixed list must equal the directories at its recorded
commit, so adding a new directory to that list silently does not exempt it.

Create a working seed with `python research/_scaffold/new_tree.py tree_name`.
This copies independent files from `new_tree_templates/`; it does not create
an import dependency on the scaffold. Replace the seed model, proofs, input,
tests and claims with the intended work. The seed proves only its stated
identity and checks one integer input. It grants no authority.

- Use exactly `CLAIMS.md`, with columns `Claim`, `Status`, `Statement`, `Evidence`.
  Status is one of `PROVED_THEOREM` (the stated theorem), `VERIFIED_FINITE`
  (the stated finite check), `CONDITIONAL` (stated assumptions), `OPEN`
  (no completed evidence), or `REFUTED` (a stated counterexample).
- Keep the canonical `verify.py` copy unchanged; `python verify.py --check`
  runs the tree's local input pins, tests, strict typing and Lean checks in
  order, failing if any step fails. `--write-pins` is a separate deliberate
  regeneration mode. Both read `TREE_CONTRACT.json`; pins cover actual local
  inputs selected there; manifest keys use repository-relative paths for the
  generated pin index. Run the complete verifier under the operator's serial
  lock when one is in use. A successful scaffold run is local evidence only.
- Use one Lake package, `lean/lakefile.toml`, with a unique `Research...` root.
  All Lean modules, including `Root.AxiomReport`, belong under that root.
  The report is compiled by file path, never imported as a census module.
  Commit its native, machine-independent Lake manifest after the first build.
- The seed chooses an explicit report scope: `axiom_declarations` must be
  nonempty and match every fresh report exactly, including primed names.
  The verifier states those names; it does not claim to enumerate every
  compiled constant. New evidence with broader reach needs an explicitly
  reviewed contract change, not an enlarged claim over this named list.

Stage the new files explicitly, then run `python ci/research_index.py --write`,
`python ci/lookup_indexes.py --write` and `python ci/lean_build_order.py --write`
to refresh the generated indexes and build recipe. Run the root contract check
and the tree's complete verifier before opening its PR.
CLAUDE.md can point here once its separate documentation-split item is resolved.
