# Coda change log

Material changes only, newest last.

## 1. 2026-08-16 — Reserved the tree

Folders reserved under `paper/coda/`, `lean4/Coda/`, `code/coda/`, and
`artifacts/coda/` for `foc`, `fda`, `mur`, `or`, `cs`, `q`, `b_cs_q`,
`gtla`, `gtoc`. Lean library `Coda` added next to `Derivation`. No
definitions, theorems, computations, or receipts admitted.

## 2. 2026-08-16 — External papers named; skeletons only

Each layer now points at one external paper and keeps a plain-language
skeleton of the subject. Formalization, code, change logs, and claim
lists were not imported. The claim ledger is still empty.

## 3. 2026-08-16 — Per-paper companions and Lean claim names

Each layer paper is `{acr}.md`, with `{acr}_change_log.md` and
`{acr}_claims_ledger.md` beside it. A Lean file
`{acr}_claim_<uuid>.lean` is created if and only if a ledger row has
surface `lean`, using the same uuid. No such rows exist yet.
