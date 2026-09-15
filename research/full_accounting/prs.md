# Pull-request census

`AuthorityEffect: None.` Two counts, because squash lands do not
create merge commits.

- `git log --merges` on HEAD: 199 merge commits; 159 subjects contain
  `pull request #N` (machine: `pr_merges.tsv`).
- Titles on `origin/main` including squash `(#N)`: **173 merged PRs**
  in `#1`–`#183`. Gaps with no merge of that number:
  `#20, #28, #29, #30, #61, #66, #74, #95, #116, #118`.
  `#20` landed as review-repair `#21`.

On `origin/main` only (not this HEAD): PR #182, #183
(`origin_extra.md`). HEAD’s last merged PR is **#181**.

Load-bearing merges for comparison (not the full 159):

| PR | merge SHA (approx) | payload |
|---|---|---|
| #1 | `c6bded55` | greenfield derivation |
| #2 | `221dec42` | r4 merge certificates, Ext |
| #4 | `45bf54db` | primitive difference |
| #5 | `91d2690a` | bridge provenance |
| #7 | `e5d18ba9` | refusal / frontier 006 |
| #8 | `9c47c2b8` | F5 generator |
| #9 | `f7e4f392` | DiffInterface |
| #10 | `2c605e28` | Represented |
| #11 | `ccd3a538` | ultra closure |
| #12 | `1f272ef2` | contact/passage/growth |
| #19 | `bd2e8c8d` | contact collision executed |
| #32 | `b4e7c95e` | Breaking/Composing parked |
| #51–#57 | … `052e657` | coda then seal re-run |
| #60 | `3100c4ed` | isolate coda out |
| #79+ | 2026-08-21 | gate 11 / research job |

Research PRs after #75 are mostly one tree per PR; see
`commits_grouped.md` and `research/post_seal_walk/`.
