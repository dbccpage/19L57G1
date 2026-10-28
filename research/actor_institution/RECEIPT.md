# Verification receipt

AuthorityEffect: None. One local run, recorded as it happened. A receipt is
not a proof of the mathematics; it says which commands ran, with which tools,
and how they exited. Where a number below came from a tool's output, the
output is quoted; nothing here is estimated.

## Where and when

- Repository `dbccpage/19L57G1`, branch `claude/project-thread-22m35b`,
  made from `main` at `b8b3ab431a8f82b110fc5b42d8a6698d733953e6`
  (`tests: pin the Inventory collision inherited by research/uncollapse (#282)`).
- Date: 2026-10-28. Linux container; a cloud session, not the author's
  machine. No hosted CI exists for this repository; this is the local run
  `CLAUDE.md` means by "green".

## Tools

```
Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit d8b18978322de05a8f3dba51ef03cf5461676c17, Release)
Lake version 5.0.0-src+d8b1897 (Lean version 4.33.0)
Python 3.13.17
pytest 9.2.0
mypy 2.4.0 (compiled: yes)
```

Lean 4.33.0 came from the release tarball on the `PATH` (`elan` is not
reachable from the container). `lean/lean-toolchain` says
`leanprover/lean4:v4.33.0`, and the tree's own `verify.py` checks that pin.
No Mathlib: the tree requires only the sealed `derivation` package and
`research/two_theorems/lean`, both present in the checkout.

## The tree's own verifier

Command, from `research/actor_institution/`:

```
python3 verify.py --write-pins      # exit 0: "pins: 1 local input files"
python3 verify.py --check           # exit 0
```

Steps the `--check` run printed, in order, and their results:

| step | result |
|---|---|
| `pins` | `pins: 1 local input files` (`SOURCE_MANIFEST.json` matches `input.json`) |
| `tests` | `10 passed in 12.79s` |
| `typing` | `mypy --strict --python-version 3.14`: `Success: no issues found in 3 source files` |
| forbidden tokens | none in any `.lean` file of the tree (the scan is a whole-word match for the five shortcut tokens and a leading `axiom`) |
| `Lean sources` | `lake build` of `ResearchActorInstitution.Institution`, `.Chain`, `.Policy`, `.Acquisition` and the root: exit 0 |
| `Lean named reports` | `lake env lean ResearchActorInstitution/AxiomReport.lean`: 98 `#print axioms` reports, matching `TREE_CONTRACT.json` by multiset |
| closing line | `local verification complete; AuthorityEffect: None` |

Wall time of the `--check` run: 16.3 s. The `lake build` inside it was
incremental over an earlier build in the same checkout; a cold build of the
tree's four modules takes longer, and nothing below depends on the time.

Axiom report, counted from the run's output (98 reports):

| axioms | reports |
|---|---|
| `[propext, Quot.sound]` | 75 |
| `[propext]` | 12 |
| none | 11 |
| any other axiom (`Classical.choice` included) | 0 |

The 98 names are listed in `TREE_CONTRACT.json` and printed by the run as
"Lean reach: exactly 98 named declarations"; they are every `theorem` of the
four modules in file order, which `tests/test_model.py::test_axiom_report_covers_every_theorem_and_matches_contract`
checks against the sources.

One earlier `--check` run failed at the forbidden-token step: the variable
name `admit` (the admission rule of `Acquisition.lean`) matched the
whole-word scan for the proof shortcut of the same spelling. The variable
was renamed `rule`; no proof changed. That failure is why this receipt
exists for the second run, not the first.

## Root gates that see the tree

Commands from the repository root, after `git add research/actor_institution`
and the index regeneration:

| command | result |
|---|---|
| `python3 ci/research_index.py --write` | `wrote research/README.md` (one row added: `actor_institution`, local receipt only) |
| `python3 ci/lookup_indexes.py --write` | `docs/index/topics.md already current`; `wrote docs/index/pins.md` (two rows: `SOURCE_MANIFEST.json`, `input.json`) |
| `python3 ci/lean_build_order.py --write` | `wrote docs/lean_build_order.md` (100 build entries; new require group `two_theorems -> actor_institution`) |
| `python3 -m pytest -q tests/test_research_module_names.py tests/test_toolchain_pins.py tests/test_research_index.py tests/test_lookup_indexes.py tests/test_lean_build_order.py tests/test_primitive_contact.py` | exit 0 (88 passed, 1 skipped) |
| `python3 ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, 133 files with pinned hits, 1829 hits, census matches its pin`, exit 0 |
| `python3 ci/check_new_research_trees.py` | `new research-tree contract clean; existing baseline directories grandfathered; second-derivation rungs held to their seed`, exit 0 |

One earlier run of `check_new_research_trees.py` rejected the `AI-07c` row
of `CLAIMS.md`: its statement contained `|D|` inside backticks, which the
row parser read as two extra columns. The statement was reworded; its
content did not change.

## What this receipt does not cover

- The sealed derivation's own gates (`python ci/run_gates.py`): not run here;
  this tree changes nothing under the seal, and the identifier firewall test
  above is the gate that reads the whole tree.
- The other research trees' verifiers: not run; nothing here changes them.
- The mathematics. `CLAIMS.md` says what is proved, what is computed, what
  is refuted and what is open; `AUDIT.md` says what each result depends on.

## Addendum, 2026-10-28: the full root `pytest`

The pull request body promised this. Command, from the repository root on
this branch at `16634e3`, with the tools listed above:

```
python -m pytest -q
```

Exit status 1. Counted from the progress lines of the captured log (the
run's own summary line was not captured): 919 tests ran; 891 passed, 1
skipped, 19 failed, 8 errored at setup.

The same 27 outcomes occur on `origin/main`
(`b8b3ab431a8f82b110fc5b42d8a6698d733953e6`) in this environment. The three
files holding the 19 failures and the file holding the 8 setup errors were
run on a detached worktree of that commit
(`python -m pytest -q -p no:cacheprovider <files>`), and the sets of failing
and erroring test ids are identical (`diff` empty). None of the 27 touches a
path this branch changes. The observed causes:

| Tests | Count | Observed cause |
|---|---|---|
| `tests/test_pin_head_git_errors.py`: `test_present_head_source_git_error_fails[*]`, `test_absent_head_source_is_reported[*]`, `test_present_head_span_git_error_fails` | 17 | the clone here is shallow (`git rev-parse --is-shallow-repository` prints `true`), so each custody verifier reports `snapshot … is not an ancestor of HEAD` before reaching the injected git error under test |
| `tests/test_side_free_custody.py::HistoricalIsolationTests` (errors at `setUpClass`) | 8 | `git show c0c4ac505…:research/side_free/CLAIM_LEDGER.md` fails here with `path … exists on disk, but not in` that commit; the historical lookup is not reproduced in this clone |
| `tests/test_research_pin_consumption.py::test_template_tree_pins_exactly_the_python_it_loads[x310_vertical_integration]` | 1 | the test's child interpreter runs with that tree as its working directory, where the tree's `types.py` shadows the standard library's `types` on this Python 3.13 (`enum` imports `types`; circular import) |
| `tests/test_run_gates.py::test_a_failure_stops_its_own_job_and_not_the_others` | 1 | `coverage` is not installed here (`No module named coverage`), so a step fails for a reason unrelated to the job isolation under test |

What this addendum does not cover: it does not show that these 27 pass on
the author's machine, only that they fail identically on `origin/main` and
on this branch here, for causes outside this branch's diff.

## Correction, 2026-10-28

`README.md` (the vocabulary table's information row, the chain, link 2, and
the information paragraph) and `CLAIMS.md` row AI-22 said that a question
not yet known raises information "by exactly one class".
`information_lt_of_not_knows` proves a strict increase, by at least one
class; on `[0, 1, 2, 3]` the empty family has one class and the identity
question four. All three texts now say "strictly, by at least one class".
The vocabulary row was corrected one commit after the other two. No theorem
changed.
