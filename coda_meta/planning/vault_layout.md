# Vault layout (plan)

**Do not create `0X/`, `0N/`, `0Q/`, `lean/`, `code/`,
`art/`, or `index/` yet.** Name-clash residuals in
`open_conflicts.md` are still open. Creating those folders
while the residuals are open is a defect.

A 2026-08-17 multi-color pass (Grok lead, Harper, Benjamin,
Lucas) treated the tracks, the paper triad, and the admission
rules as the future human-readable surface of the residual
monoid, OES, multi-repo prefixes, and OEAG limits. Red named
the hinges. Green closed them without creating folders. Blue
made the triad a projection, not a second ledger.

**Bring-over now (encyclopedia markdown only).**
Processing tools stay in
`anomalonpy/omega_engine_operations` and are not copied.
The markdown hold is `lib/`. It is one-way, not a
track, not a paper triad, and not an identity source.
Off-repo is parked until (if) the system goes online
for money (`axiom.md`, `open_conflicts.md` §10).
Promotion into `0X`/`0N`/`0Q` is refused until the
conversion-quality gate (~80 % parse / label
retention) is a CI artifact and the name-clash
residuals are discharged. `lib/` contents are not
claims.

## Planned tree (not created except `lib/` hold)

```text
0X/     frontier          — not created
0N/     ordered spine     — not created
0Q/     quarantine        — not created
lib/    encyclopedia markdown hold (one-way; this phase)
programs/  research-program fossils (plan: `programs_hold.md`)
lean/   mirrors           — not created (name clash)
code/   paper twins       — not created (name clash)
art/    residual receipts — not created
index/  derived SQLite    — not created
        Axiom (ooutwire-c95u) is the same class of
        derived query surface — see `axiom.md`
```

Tracks `0X` / `0N` / `0Q` are **local to this vault’s
prefix** (normally `0000` OER). They are not a second global
hierarchy. Cross-prefix rules and OEAG limits on
`multi_repo.md` apply unchanged.

## Paper triad (when papers exist)

Every research unit under a track has exactly three core
files:

```text
paper.md
claim_ledger.md
change_log.md
```

plus one sealed exception: `aux/` (or paper-local
`artifacts/`) for residual certificates, toy spines,
diagrams, conversion reports, test witnesses. Contents of
`aux/` are not claims. They cannot become ledger rows
without a change-log admit that promotes them.

Human folders stay readable (`0N/01-primdiff`). Identity is
the bit index, not the folder name. The bit-index ↔ folder
map is a sealed ConfigGauge; agents must not hard-code
paths as identity.

## Single source of truth

Residual monoid + mechanical lock table + typed claim-unit
spine are authoritative for cost, provenance, and jewel
status.

`paper.md` is the source text OES extracts.

`claim_ledger.md` is a **human-readable projection only** of
admitted claim units (stable IDs `prefix:track:local-id`),
observational edges, residual status, optional lock
attachments, and visibility. Divergence emits `ledger-drift`.
Automated ledger writes are produced from residual/OES
objects, never the reverse.

`change_log.md` is the human-visible side of residual
admissions, discharges, track moves, and secrecy-boundary
freezes. Each admission carries a residual reference or is
itself residual-trackable. Soft free-text admits are a
defect.

`art/` receipts, when they exist, are the human-readable
projection of ResidualCertificates and lock-fill witnesses.
They are not a third evidence system.

`index/` SQLite, when it exists, is a **derived cache only**.
It may be blown away and rebuilt from the triad + residual
certificates. It never originates identity or admission.
The free Axiom org `ooutwire-c95u` is the same class
(`axiom.md`): events and APL over manifests and receipts,
not a lock table and not a jewel panel.

## Rules

- No claim in `paper.md` without a matching ledger row.
- No ledger row without a change-log event that admitted it.
- Every ledger ID and every claim-unit stable ID from this
  vault is prefix-qualified (`prefix:track:local-id` or
  `prefix:bit-index`). Local section prefixes are
  subordinate. See `prefix_table.md` and `oes.md`.
- Every ledger row carries an explicit `visibility` field.
  Extract, spine build, or export that lacks markers, or
  that would place `visibility=1` content into this private
  vault, emits `secrecy-boundary-violation` and is refused.
  The freeze itself is a sealed event.
- Track moves (`0X`/`0N`/`0Q`, including quarantine
  entry/exit) require a change-log event that carries a
  residual: reason and discharge condition for the previous
  track. `0Q` is not a junk drawer. Promotion uses the same
  residual-gated pattern as “earns a remote”
  (`multi_repo.md`): explicit residual, discharge condition,
  no taste-based moves.
- New tracks may only observationally cite the sealed
  derivation (`references_by_name`, `shares_identifier`,
  `cites_by_prefix`). No automatic twinning or re-ownership
  until a residual-gated migration plan exists.
- `lib/` import is one-way. It stays blocked from the
  ordered spine by the conversion-quality gate. Premature
  ledger rows on hold files are refused.

## Name clashes

`lean/` and `code/` collide with sealed `lean4/Derivation/`
and `code/`. Residual gate: do not create those track
mirrors until `open_conflicts.md` §1 is residual-discharged
(explicit supersession, rename, or permanent “do not
create”). Ad-hoc overwrite, shadow, or fork is refused.

## What already exists (do not move)

- Sealed derivation: `prompt/`, `paper/`, `code/`,
  `lean4/Derivation/`, `artifacts/`
- Canon binds: `coda/000_no_self_authorization`, `coda/foc`,
  `coda/fda`
- Local unmerged drafts: `coda/mur` and other working-tree
  leftovers — not this layout

`AuthorityEffect: None.`
