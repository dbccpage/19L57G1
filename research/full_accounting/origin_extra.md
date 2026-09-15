# Four commits on origin/main not on local HEAD

`AuthorityEffect: None.` Pin: `origin/main` `dfe64944` vs HEAD
`0e781408`. Walked by `git log HEAD..origin/main --stat` only. Trees
not present in this worktree.

| SHA | date | subject |
|---|---|---|
| `3fa76db9` | 2026-09-13 13:23 | `research/sign_tower`: Prompt B Sign Tower investigation |
| `dd179b6b` | 2026-09-13 17:28 | `research/sign_tower`: cite ScaleDynamics for twins; drive canonical in obstruction test |
| `a5e196b5` | 2026-09-13 17:30 | Merge PR #182 address_pr_164_feedback |
| `dfe64944` | 2026-09-13 17:30 | Merge PR #183 research/diagonal-identity |

`3fa76db9` adds 21 files, +2094 lines: Lean `Carrier`, `History`,
`Movegraph`, `Obstruction`, `ScaleDynamics`, `Inventory`; matching
Python and tests; `FINDINGS.md`.

`dd179b6b` touches `FINDINGS.md` and `test_obstruction.py` (+23 / −7).

PR #183 merge likely includes the diagonal-identity work already on
this HEAD (`0e781408` and parents). PR #182 is review of PR #164
feedback. Exact file lists of the two merges were not expanded
(`--name-only` without `-m`).

For comparison: if the other accounting is on `dfe64944`, it will
contain `research/sign_tower/` and this one will not.
