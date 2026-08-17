# Open conflicts (plan)

Resolve in review. Do not "fix" by creating folders.

## 1. Sealed names

`CLAUDE.md` seals all of `prompt/`, `paper/`, `code/`,
`artifacts/`, and `lean4/Derivation/`.

The vault wants `code/`, `art/`, and `lean/` at repo root.

Until a carve is written, do not create those names. Options
for later:

- vault lives under `vault/` (not a sealed name)
- vault `lean/` ≠ `lean4/Derivation/`
- vault `code/` ≠ sealed `code/`

## 2. Null spine vs sealed derivation

`0N/00-null` is a **pointer** to the existing sealed
derivation. Do not copy or amend `paper/`, `code/derivation/`,
or `lean4/Derivation/`.

## 3. Existing coda binds

`coda/foc` and `coda/fda` stay until a migration PR names bit
keys and `0N/0k-slug`. This planning PR does not rename them.

## 4. Public visibility

`visibility=public` content must not sit in this private vault
without a secrecy-boundary note. Plan export before any public
file.

## 5. Repo bits

Only `0000` = 19L57G1 is assigned. Other prefixes wait on the
wide-team letter list.

## 6. Claim class lists

`catalog_schema.md` uses a short class enum. `CLAUDE.md`
assumption discipline is the single source for object-language
types. Reconcile the two lists before any live ledger uses the
SQL enum.
