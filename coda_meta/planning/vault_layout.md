# Vault layout (plan)

**Do not create these folders yet.** Seal conflicts are in
`open_conflicts.md`.

## Tracks

```text
0X/     frontier
0N/     ordered spine
0Q/     quarantine
lib/    encyclopedia + PDF markdown (later, one-way)
lean/   mirrors 0X / 0N / 0Q   (name clash — see conflicts)
code/   paper twins            (name clash — see conflicts)
art/    receipts
index/  private SQLite
```

## Paper triad

Every research unit is a paper under a track. Inside the paper
folder, exactly three files:

```text
paper.md
claim_ledger.md
change_log.md
```

Human folders stay readable (`0N/01-primdiff`). The bit index is
the primary key.

## Rules

- No claim in `paper.md` without a matching ledger row.
- No ledger row without a change-log event that admitted it.
- Prefixes on paper sections and ledger IDs.
- Public (`visibility=1`) content does not live in this private
  vault, or lives only as a pointer. Freeze the secrecy
  boundary before any export.
- `lib/` import from anomalonpy is one-way and later.

## What already exists (do not move in this PR)

- Sealed derivation: `prompt/`, `paper/`, `code/`,
  `lean4/Derivation/`, `artifacts/`
- Canon binds: `coda/000_no_self_authorization`, `coda/foc`,
  `coda/fda`
- Local unmerged drafts (not this PR): `coda/mur` and other
  working-tree leftovers
