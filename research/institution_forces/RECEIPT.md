# Verification receipt

AuthorityEffect: None. One local run, recorded as it happened. A receipt is
not a proof of the mathematics; it says which commands ran, with which tools,
and how they exited. Where a number below came from a tool's output, the
output is quoted or counted from it; nothing here is estimated.

## Where and when

- Repository `dbccpage/19L57G1`, branch `claude/project-thread-u83wvs`, made
  from `main` at `1c9ad34b834671d0d71a26c7d3ce539d29fa551a`.
- Commit the run was made at: `335871fbbfc558671b0e3e3bae8317342fdfa2a0`
  (`research: add institution_forces ...`), with a clean working tree.
- Date: 2026-11-06, run started 03:09 UTC. Linux container; a cloud session,
  not the author's machine. No hosted CI exists for this repository; this is
  the local run `CLAUDE.md` means by "green".

## Tools

```
Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit d8b18978322de05a8f3dba51ef03cf5461676c17, Release)
Lake version 5.0.0-src+d8b1897 (Lean version 4.33.0)
Python 3.13.18
pytest 9.1.1
mypy 2.4.1 (compiled: yes)
```

Lean 4.33.0 is the official `lean-4.33.0-linux.zip` release from the
`leanprover/lean4` GitHub releases, unpacked outside the repository and put on
the `PATH` (`elan` is not installed in the container). `lean/lean-toolchain`
says `leanprover/lean4:v4.33.0`. pytest and mypy were installed into a
virtual environment outside the repository. No Mathlib: the tree requires
only the sealed `derivation` package, `research/two_theorems/lean` and
`research/actor_institution/lean`, all present in the checkout.

## The tree's own verifier

The tree's `lean/.lake` was deleted first, so its four modules were compiled
from source; the required packages reused their own build directories.
Command, from `research/institution_forces/`:

```
python verify.py --check            # exit 0, wall time 26 s
```

| step | result |
|---|---|
| `pins` | `pins: 1 local input files` |
| `tests` | `11 passed in 22.64s` |
| `typing` | `mypy --strict --python-version 3.14`: `Success: no issues found in 3 source files` |
| forbidden tokens | none in any `.lean` file of the tree |
| `Lean sources` | `lake build` of `ResearchInstitutionForces.Joint`, `.Robust`, `.Staleness`, `.Ballot` and the root: `Build completed successfully (31 jobs).` |
| `Lean named reports` | `lake env lean ResearchInstitutionForces/AxiomReport.lean`: 59 `#print axioms` reports, matching `TREE_CONTRACT.json` by multiset |
| closing line | `local verification complete; AuthorityEffect: None` |

Axiom report, counted from the run's output (59 reports):

| axioms | reports |
|---|---|
| `[propext, Quot.sound]` | 34 |
| `[propext]` | 8 |
| none | 17 |
| any other axiom (`Classical.choice` included) | 0 |

Per theorem (namespace `ResearchInstitutionForces` omitted):

| theorem | axioms |
|---|---|
| `Joint.knows_family_iff_joint`, `Joint.knows_joint_idem`, `Joint.knows_iff_redundancy`, `Joint.duplicate_knows_inert` | propext, Quot.sound |
| `Joint.redundancy_pos_iff_not_sigEq`, `Joint.redundancy_zero_iff_sigEq` | propext |
| `Joint.sepCount_le_one`, `Joint.sepCount_eq_zero`, `Joint.sepCount_eq_one`, `Joint.redundancy_nil`, `Joint.redundancy_cons`, `Joint.redundancy_append`, `Joint.redundancy_le_length`, `Joint.redundancy_symm`, `Joint.redundancy_pos_iff`, `Joint.duplicate_counts_twice` | none |
| `Robust.repl_mono`, `Robust.redundancy_le_repl`, `Robust.robust_iff`, `Robust.del_mono`, `Robust.redundancy_le_del`, `Robust.deletion_robust_iff`, `Robust.robustB_iff` | propext, Quot.sound |
| `Robust.sigEq_blunt`, `Robust.repl_zero_aux`, `Robust.repl_zero`, `Robust.sigEq_agreeing` | propext |
| `Robust.repl_refl`, `Robust.repl_length`, `Robust.repl_blunt`, `Robust.del_agreeing`, `Robust.robust_parity_half` | none |
| `Staleness.knows_congr_mem`, `Staleness.add_preserves`, `Staleness.removal_iff`, `Staleness.seat_corruption_iff`, `Staleness.relabel_of_kept`, `Staleness.removal_count_not_necessary`, `Staleness.relabel_can_be_harmless`, `Staleness.relabel_can_break`, `Staleness.extension_iff`, `Staleness.extension_breaks`, `Staleness.target_member_preserves`, `Staleness.decision_holds_target_fails` | propext, Quot.sound |
| `Staleness.sigEq_append_consts` | propext |
| `Staleness.sigEq_symm` | none |
| `Ballot.knows_of_known_members`, `Ballot.ballot_known`, `Ballot.ballot_compression`, `Ballot.uniform_ballot_compression`, `Ballot.tally_known`, `Ballot.tally_compression`, `Ballot.settledAt_eq`, `Ballot.sincere_known`, `Ballot.sincere_compression`, `Ballot.ballot_loses_exceeding`, `Ballot.injective_ballot_keeps` | propext, Quot.sound |
| `Ballot.mem_ballots` | propext |
| `Ballot.settledAt_congr` | none |

## Root gates that see the tree

Commands from the repository root at the same commit, after the index
regeneration that the commit contains (`python ci/research_index.py --write`
wrote `research/README.md`, one row `institution_forces`, local receipt only;
`python ci/lookup_indexes.py --write` wrote `docs/index/pins.md`, two rows;
`python ci/lean_build_order.py --write` wrote `docs/lean_build_order.md`, 102
build entries, require group 3 now `two_theorems -> actor_institution ->
institution_forces`):

| command | result |
|---|---|
| `python -m pytest -q -p no:cacheprovider tests/test_research_module_names.py tests/test_toolchain_pins.py tests/test_research_index.py tests/test_lookup_indexes.py tests/test_lean_build_order.py tests/test_primitive_contact.py tests/test_new_research_tree_contract.py tests/test_research_drift.py` | exit 0; 154 progress marks, one of them a skip (an earlier non-quiet run of the same files on the same content printed `153 passed, 1 skipped in 174.63s`) |
| `python ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, 141 files with pinned hits, 1898 hits, census matches its pin`, exit 0 |
| `python ci/check_new_research_trees.py` | `new research-tree contract clean; ...`, exit 0 |
| `python research/_scaffold/check_scaffold.py` | `scaffold clean of correctness drift; ...`, exit 0 |
| `python ci/research_index.py --check`, `python ci/lookup_indexes.py --check`, `python ci/lean_build_order.py --check` | exit 0 each |

`check_new_research_trees.py` first failed in this clone, before the commit,
with `fatal: not a tree object` for the grandfathered baseline commit
`7c07a764…`: the clone is shallow. That one commit was fetched
(`git fetch origin 7c07a764b497daffc9db73627f2ba28fbb5d89ab`) and the check
passed. No file changed.

After the run, `CLAIMS.md` gained a paragraph recording a cross-check
reported by the coordinating session (no row changed), and this file was
added; `check_new_research_trees.py` and `check_prose_watchlist.py` were run
again on that text, exit 0 each.

## What this receipt does not cover

- The sealed derivation's gates (`python ci/run_gates.py`): not run; the tree
  changes nothing under the seal.
- The full root `pytest`: not run.
- The other research trees' verifiers, `two_theorems` and
  `actor_institution` included: not run. Their Lean was compiled as
  dependencies of this tree (`lake build` above), which is not their own
  `verify.py --check`. The `two_theorems` change is a dated note in its
  `CLAIMS.md`, which its pins do not cover.
- The mathematics. `CLAIMS.md` says what is proved, computed, refuted and
  open; `AUDIT.md` says what each result depends on and what it admits.
