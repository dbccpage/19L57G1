# Research-program hold (plan)

**AuthorityEffect:** None. Advice for bringing
`anomalonpy/omega_research/programs/` into this vault. This
page does not copy files, mint bit keys, rewrite claim IDs,
or create `0X`/`0N`/`0Q`.

Parent: `vault_layout.md`. Index/search tools stay in
`omega_engine_operations` (or a later operations remote).
This vault cites that code. It does not own it.

## What this tree is

Not encyclopedia. `lib/` is third-party PDF→markdown.
`programs/` is *your* research: papers, ledgers, notebooks,
Python, Lean, figures, kits. Census excluding
`_ow_speculative`: about 7200 files (≈3100 md, 1000 py, 520
lean, 285 ipynb, plus yaml/png/sh). Big programs: `001_coda`
(1544), `003_quantum_foundations` (1360),
`004_projection_obstruction` (1138).

Existing YAML catalogs (`domain_index.yaml`,
`estate_root.yaml`, the published_* indexes) are **not**
imported as authority. They stamp every artifact
LOCAL_GREEN. That is a receipt, not a spine.

You said the papers are a **map of missing ideas**, not a
mandate to publish everything. The hold must optimize for
seeing gaps. It must not force a new paper into every hole.

**000–006 are one program.** Estate folders
`000_witnessed_difference` … `006_ai_evaluation` (no 005)
are one obstruction story on different carriers. In this
vault they live under `programs/000_obstruction/`: fossils
keep estate paths; `slots/` is the decided map, including
empty gaps `01_admission` and `06_authorization`. 007+
estate programs are not this program.

**Frontier** (`omega_engine_frontier_research`) is untied
Generation X work. It is `programs/frontier/`, not a slot,
until a human names an attachment.

## Two layers, never one

| Layer | What it is | What you may do |
| --- | --- | --- |
| **Fossil** | Byte-identical copy of selected program trees + sha256 manifest | Read. Cite. Do not edit claim IDs, ledgers, or Lean paths. |
| **Working** | Later, per slot, a new triad under a track | New `prefix:track:local-id`. New ledger. New Lean. Old IDs become aliases. |

Rewriting claim numbers *in the fossil* destroys the only
map from “what the estate said then” to “what we admit
now.” Do the rewrite only on the working copy, with an
explicit map:

`old_path + old_claim_id → 0000:<track>:<new-id>`

Old IDs remain citations of the fossil. They are not live
keys.

## What to copy, and what not

**Copy (fossil hold), when you say go:**

- Numbered programs `000`–`015`, `100`–`102`
- Their `README.md` files
- `principia_anomalonica` if you want it as fossil
- A generated **census** (below), not the old master YAML

**Do not copy now:**

- `_ow_speculative` (902 files; junk drawer, not a program)
- `_kits` search/index generators, `*.pyc`, `__pycache__`,
  lockfiles, zip balls
- `domain_index.yaml` / `estate_root.yaml` / published_*
  indexes as if they were SSOT
- Operations / OAS / FTS / embedding tools
- Root `edward_witten_*.pdf` as a named folder (see
  `open_conflicts.md` §7)
- Live `coda/foc`, `coda/fda`, `coda/mur` overlays — those
  already live here. The estate’s `001_coda/000_coda_foc`
  etc. stay fossils. Do not merge them into `coda/` as if
  they were the same object.

Destination (done as hold, not committed):

- `programs/000_obstruction/fossils/{000,001,002,003,004,006}_*`
- `programs/000_obstruction/slots/00_…07_…` (two empty)
- `programs/frontier/` (no `.olean` / `.ilean` / `.c` /
  `.trace`)

Sibling of `lib/`. Not `0N/`. Not `lean4/Coda/`.

Lean files come along as fossils. Broken Lake/imports are
expected. Do not “fix” them in the hold. When a slot is
promoted, new Lean is written under a discharged path and
points at the fossil by hash, not by the old relative
import.

## Index *before* enrichment

You need a program index **before** new triads and before
OES extract. That index is a census, not a claim ledger.

One machine file, derived, rebuildable, no identity minting:

```text
program_id     001_coda
slot_id        000_coda_foc
fossil_path    programs/001_coda/000_coda_foc/...
sha256         ...
kinds          {md, py, lean, ipynb, ...} counts
old_ledger     path or absent
old_claim_ids  listed as *strings found*, not as live IDs
lean_ok        false  (broken is the default)
gap            optional: human note, not a paper
```

Plus a **program spine**: the ordered list of *slots* (folder
names) in each program. That is the map you walk to see what
is missing. A missing slot is a **TODO / lock proposal**,
not an order to write a paper.

Do **not**:

- regenerate `claim_ledger.md` on import
- invent new CL-* numbers on import
- run OES extract on the fossil
- treat notebook outputs or `_estate_*.py` scripts as
  papers
- build SQLite as a source of truth (`vault_layout.md`)

When operations/OAS later lands from its own remote, it
reads this census and the fossils. It does not own them.
Axiom (`axiom.md`) may later ingest the same census as
events in `oer-census`. That is a query copy. It does
not replace this file.

## Claim-number rewrite (later, per slot)

1. Freeze the fossil (manifest pins sha256).
2. Choose the working slot under a track (after tracks
   exist).
3. Write a new triad. New IDs only.
4. `aux/id_map.md` (or equivalent) lists old → new. The map
   is not a claim.
5. FOC / other CODA layers may force a later rewrite of the
   *working* triad. The fossil does not move. Each rewrite
   is a change-log event that references a residual.

Republication is a promotion of a working triad, not a
sweep of the hold.

## Gaps as the point

A research program is allowed to stay gappy. The index
should make gaps *visible*:

- adjacent slots with no bridge note
- a program with no FOC/CODA bind
- a slot whose old ledger claims more than the fossil paper
  states
- Lean present and not elaborating

Each of those can become a pre-declared lock (OES) or stay
a TODO. Filling a gap is an author’s act. The hold must not
auto-spawn papers.

## Firewall and size

Same rule as `lib/`: do not `git add` the tree until a
vocabulary-firewall census is clean. `.pyc` and generated
indexes must not enter the commit. Prefer a manifest + the
source files, not 395 bytecode leftovers.

## Order

1. Census of the *source* tree (no copy required to start):
   programs, slots, kind counts, old ledger paths.
2. Copy the selected fossils into `programs/` when you say
   go. Write `programs/README.md` as hold rules (mirror
   `lib/README.md`).
3. Do not create tracks. Do not rewrite IDs.
4. Operations/OAS arrives later from its remote and indexes
   the census.
5. Promote one slot at a time, new triad, new IDs, map in
   `aux/`.

`AuthorityEffect: None.`
