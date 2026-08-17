# Identity schemes (plan)

Primary key stays the **structured bit key**. This page records
why UUID v7 and friends are not that key. Source: external
`planning_doc_000.md`.

## Requirements

- Fits in one SQLite BLOB
- Carries repo, visibility, track, program, paper, claim
- Sequential allocation inside a program node
- Stable if a human prefix is renamed
- Offline, private, no clock politics
- EKNF-friendly: one irreducible semantic identity

## Verdicts

- **Structured 128-bit `bit_key`** — keep as primary.
- **SQLite INTEGER** — internal row id only (`paper_id`).
- **Mnemonic prefix** (`CL-…`) — human layer; repairable.
- **UUID v8** — allowed **wire form** of the same bits if a
  tool will only take a UUID.
- **UUID v7 / ULID** — optional opaque public tokens. Never
  the research identity. They answer "when minted? unique?"
  not "which paper and claim forever?"
- **UUID v4** — avoid as PK.
- **Snowflake 64-bit** — too narrow.
- **TypeID** — API label, not PK.
- **KSUID** — skip.

v7 is time-sortable and standard. It carries **zero**
provenance and depends on a clock. That is the wrong
question for this library.
