# CODA-META

Apparatus about CODA, not content of it.

## What belongs here

- Claim typing, ledgers, and the vocabulary that types them.
- Gate design, injection records, and what a green run does and does not
  certify.
- Review procedure and the standing anti-patterns.
- Anything whose subject is *how a claim is established* rather than *what
  is claimed*.

## What does not

- Object-level results. Those go in `coda/`.
- Anything that would let apparatus confer standing on a claim. A ledger
  row, a receipt, a passing gate, and a review disposition are all evidence
  about a procedure. None is authority, and the separation is the subject
  matter here, so violating it here is worse than violating it elsewhere.

## Rules

Same as `coda/`: external citation permitted, the vocabulary firewall
applies, claim typing follows `CLAUDE.md` (single source — do not restate
it), withdrawal in place.

**And the same warning.** None of the eight gate families reads
`coda_meta/` either. The firewall walks the tree; nothing else here is
gate-protected. Given that this directory's subject *is* what a gate
certifies, saying otherwise would be the failure it exists to describe.

One addition. **Apparatus drifts and nothing checks it.** The `gates` skill
documented six gate families for as long as there were eight, including one
written the same day it went unrecorded. No gate compares a procedure
document with `.github/workflows/verify.yml`. Anything written here that
cites a gate count, a file path, or a command name is a claim about the
machine and should be checked against the machine before it is trusted.

## Horizon runner (2026-08-16)

- `LONG_HORIZON_PROMPT.md` — copy to Opus / Fable / Grok. One paper
  per sitting.
- `session_notes_20260816.md` — what this bind sitting already
  decided.
- `bringover_log.md` — what was classified and what was bound.
- `inter_repo_horizon_workflow.md` — lookup table and forbidden list.

Object binds live in `coda/foc/` and `coda/fda/`. Next default paper is
MUR.

## Institute library (plan only)

Wide-team review lives under [`planning/`](planning/README.md).
No vault folders, no SQLite, no paper moves in that tree.

`AuthorityEffect: None.`
