# gtla claims ledger

No claims are admitted.

A later row uses id `gtla_claim_<uuid>`. The uuid is 32 lowercase
hex digits with no hyphens, so the string is a legal Lean module
component and matches the Lean filename exactly.

| surface | Lean file |
|---|---|
| prose | none |
| code | none |
| lean | `lean4/Coda/<Layer>/gtla_claim_<uuid>.lean` |

The Lean file is created if and only if the row's surface is lean.
Prose-only rows and rows mechanized in code do not get a Lean file.

| id | statement | classification | surface | evidence |
|---|---|---|---|---|
