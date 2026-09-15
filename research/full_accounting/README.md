# Full accounting of this repository

`AuthorityEffect: None.` A chronological ledger of every commit at a
fixed walk snapshot, written so it can be compared with an independent
accounting. It amends nothing sealed. It is not a gate.

Companion walk of the *post-seal* trees (container, orientation, second
seed) is `research/post_seal_walk/`. This folder covers the **whole**
history, including the sealed derivation.

## Pin

| object | SHA |
|---|---|
| Roots | `5a5990d8` seed: uninterpreted repository; `6fb1f66d` Initial commit (GitHub baseline); `--all` also has `8fe842ba` |
| First derivation commit | `5a5990d8bcfafae639e6efe474e8b5f73c9f2e50` 2026-08-11 |
| Paper suite freeze | change-log entry 8, 2026-08-12 |
| Seal re-run merge | `052e65739ddfd8c23c657562a51288cb083a2464` 2026-08-17 |
| Walk snapshot | `0e7814089db5ed387489acd9553a9105b0b69462` 2026-09-13 |
| Origin snapshot at walk time | `dfe649445403d7d0326594c918430ae5456b1f6b` (4 commits ahead) |

Walk snapshot: **766** commits, **30** days (2026-08-11 … 2026-09-13).
Origin snapshot: **770**. The extra four are `research/sign_tower` plus
two merge commits; notes in `origin_extra.md`.

Every SHA at the walk snapshot is in `commits_shas.tsv` (hash and date only).
Commit *subjects* are not tracked here: reprinting them reintroduces
watched terms into new files. Regenerate a local subject index with
`_group.py` if you need one. Era narrative is in `era_*.md`.

## How to compare with another accounting

Match these objects, not prose tone:

1. Commit count on a named SHA (766 at `0e781408`; 770 at `dfe64944`).
2. Two-root topology on 2026-08-11.
3. Sealed terminal clauses (a)–(h) of `paper/paper.md` §11.
4. Native map: 19 PROVED / 2 DECLARED / 8 FALSE / 1 OPEN.
5. Post-seal container result: boundary admitted not derived;
   `NOTHING_IN_COST`; order ≠ container; (B) empty.
6. Second seed: stake + stream still the floor; C3–C5 unstarted.
7. Module census at seal vs walk snapshot: 55 → 75 `Derivation/` modules;
   axiom reports 1314 → 1530.
8. Research trees: 13 wired to gate 11; live directory much larger.

Disagreements that matter: a missing era, a terminal clause restated
without its tag, a cohort tree counted as a continuation of `<>`.

## Files

| file | contents |
|---|---|
| `census.md` | numbers another accounting can match |
| `commits_shas.tsv` | every SHA and date; no subjects |
| `commits_origin_main_shas.tsv` | origin/main SHA+date at walk time |
| `era_A_sealed.md` | 2026-08-11 … 16: the derivation |
| `era_B_seal.md` | 2026-08-17 isolate + stopping re-run |
| `era_C_to_F.md` | 2026-08-18 … 09-13, pointing at `post_seal_walk/` |
| `first_appearance.md` | when sealed modules were born |
| `origin_extra.md` | four unpulled commits |
| `path_forward.md` | complete system vs foundation; new seed vs cleanup |
| `prs.md` | merge-commit census (no subject dump) |
| `_group.py` | regenerates the indexes |
| `verify.py` | checks both ledgers and the census against fixed Git objects |

Post-seal tree STATUS reads remain in `research/post_seal_walk/`.
Do not duplicate them here.

## Verification boundary

- Commit lists: read-only comparison against the two pinned Git objects.
  Merge commits in generated subject indexes often show 0 files without `-m`.
- Sealed-era substance: `paper/paper_change_log.md` (authority for
  what the derivation *did*), plus first-appearance of modules, plus
  §11 of the paper.
- Post-seal substance: `research/post_seal_walk/` tree STATUS/SEED reads.
- Not run: twelve gates, Lake builds, receipt regeneration.
- Not claimed: line-read of every blob in 766 commits.

Verify the tracked ledgers and census without changing files:

```text
python research/full_accounting/verify.py
```

Regenerate the ignored subject indexes and tracked touch census from the
fixed walk snapshot with `python research/full_accounting/_group.py`.
