# Post-seal walk

`AuthorityEffect: None.` This folder is a reading of the repository after
the sealed derivation. It amends nothing under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`. It is not a gate. A summary here is
not a theorem.

## Pin

| object | SHA |
|---|---|
| Seal re-run merge | `052e65739ddfd8c23c657562a51288cb083a2464` (2026-08-17) |
| Walk snapshot | `0e7814089db5ed387489acd9553a9105b0b69462` (2026-09-13) |
| Origin snapshot at walk time | `dfe649445403d7d0326594c918430ae5456b1f6b` (4 commits ahead) |

The range `052e657..0e781408` has 561 commits. Every SHA and date is listed
in `commits_shas.tsv`. The expanded range `052e657..dfe64944` has 565;
its four additional, newest rows appear first in
`commits_origin_extra_shas.tsv`. Commit *subjects* are not tracked here:
reprinting them reintroduces watched terms into new files. The four
additional commits were inspected only through their path statistics,
not read as trees.

## What this folder is for

A prior review sampled research trees and scored many of them as costume.
It did not read `boundary_seed`, `side_free`, or `oriented_boundary`. Those
three trees are the post-seal derivation of the container question, the
no-container control, and the kind of an order. They are the reason this
folder exists.

This is a map, not a restart. It does not amend the seal.

## How to read

1. `from_scratch.md` — if the experiment were started from nothing again,
   the sequence that generates the system that is already here.
2. `thread_container.md` — `<|>`, sides, orientation, order ≠ container.
3. `thread_second.md` — stake, stream, standing commitment, second seed.
4. `thread_native.md` — difference, sections, demand no-gos, observers.
5. `thread_sealed_after.md` — what grew *inside* the sealed paths after
   2026-08-17.
6. `thread_other.md` — remaining research trees, indexed not dismissed.
7. `commits_shas.tsv` — all 561 SHAs and dates (no subjects).
8. `commits_origin_extra_shas.tsv` — the 565-row expanded origin snapshot.

## Verification boundary of the walk itself

- Commit ledgers: read-only comparison against the two pinned Git objects.
- Path buckets: machine-generated from `git log --name-only` at the walk
  snapshot.
- Tree terminals: read from each tree's `STATUS.md` / `SEED.md` /
  `CLOSURE.md` / `CLAIM_LEDGER.md` / paper, plus named Lean theorems.
- Not run: the twelve gate families, research Lake builds, regeneration
  of any receipt.
- Merge commits in `commits_grouped.md` often show `_0 files_`:
  `git log --name-only` without `-m` does not list the merge diff.
  The parent commits of those merges are listed and do carry files.
- Not claimed: that every one of ~2000 research files was line-read.
  Every *tree* was opened at its status/seed/ledger. Every *commit* is
  listed. File-level understanding is clustered by write-root.

Verify the tracked ledgers without changing files:

```text
python research/post_seal_walk/verify.py
```

Regenerate the ignored subject index and tracked touch census from the fixed
walk snapshot with `python research/post_seal_walk/_group_commits.py`.
