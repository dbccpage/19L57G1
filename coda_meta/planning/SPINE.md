# Spine freeze (plan)

**AuthorityEffect:** None. This page freezes letters and rules
for review. It does not create `0N/` on disk.

## Tracks

| Code | Folder (planned) | Meaning |
| --- | --- | --- |
| N | `0N/` | Ordered spine. Only you promote onto it. |
| X | `0X/` | Frontier / Gen X. Candidates. |
| Q | `0Q/` | Quarantine / speculative. |

## Promotion

- Agents may draft under `0X` or `0Q` **after** a go that
  creates those trees. They may not promote.
- Only the human author moves `0Q` → `0N` or `0X` → `0N`.
- A green test, a hash, a ledger row, and this file are not
  promotion.

## First program nodes (L1 draft — you edit)

Proposed codes. Not allocated.

- `coda`
- `meta-theory`
- `mathematics`
- `physics`
- reserved

Agents do not invent L1 codes.

## First spine slots (migration map, not a move)

| Planned slot | Existing object | Note |
| --- | --- | --- |
| `0N/00-null` | sealed derivation | pointer only; do not copy |
| `0N/01-primdiff` | sealed / paper primdiff | after triad exists |
| `0N/02-apartness` | sealed apartness | after triad exists |
| later coda binds | `coda/foc`, `coda/fda` | stay until rename PR |

## Paper triad (when papers exist)

Exactly `paper.md`, `claim_ledger.md`, `change_log.md`.

No claim in the paper without a ledger row. No ledger row
without a change-log admit event.
