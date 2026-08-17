# Axiom — derived query surface (plan)

**AuthorityEffect:** None. Plan only. This page does not
create datasets, ingest events, store a token, or mint
identity.

**Org (currently free):** `ooutwire-c95u`
**Console:** https://app.axiom.co/ooutwire-c95u/datasets

Axiom is a **derived** surface, same class as the planned
`index/` SQLite: blow it away and rebuild from fossils,
censuses, figure rows, and gate receipts. It is not a
ledger. It is not a lock table. It does not award jewels.
A green dashboard is not promotion.

Tokens stay in the operator environment (`~/.axiom.toml` or
the host secret store). Nothing under this vault commits an
API key.

## Why it is on the plan

The org is already paid-for-by-being-free. Use it for
questions that APL is good at: counts over holds, gate
history, op-read candidates, “what changed in `programs/`.”
Do not use it to replace FTS, embeddings, or the spine/lock
layer in `oes.md`. Those stay in operations (later its own
remote). Axiom *queries* what those tools emit.

Free-tier quotas are a residual. Ingest that would blow the
quota is refused, not “we will see.” When the free org
stops being enough, that is an earn-a-remote / earn-a-bill
decision, not a silent upgrade.

## What may be ingested (later, from operations)

Event-shaped, rebuildable, no secrets. Two families.

**Vault manifests** (this repo, when a go exists):

| Dataset (proposed names) | Source | Question |
| --- | --- | --- |
| `oer-census` | `programs/000_obstruction/census.json` and later slot censuses | how many fossils, by kind, by slot |
| `oer-lib` | encyclopedia *manifest* only (path, bytes, sha256) | size and churn; not the markdown bodies |
| `oer-gates` | CI / local gate receipts (name, pass/fail, sha of input) | which gate failed, on which pin |
| `oer-opread` | op-read *candidates* only | locks nearly filled; never jewel status |
| `nsa000-runs` | illustration tests and notebook runs | did the public object still run |

**Swarm streams** (anomalonpy / later OEAS; ship, do not archive locally):

Product record is
`omega_engine_operations/controllers/woland_bout_controller.py`
and
`omega_engine_operations/use_cases/woland_bout/`.
This vault cites. It does not grow an `_intelligence/` tree.

| Dataset (proposed names) | Source on disk today | Question |
| --- | --- | --- |
| `oeas-uts` | `_intelligence/unified_oe_trace.jsonl` (UTS in code; spoken UTC) | what ran, Φ₁ / γ₂, verdict, antibodies |
| `oeas-uns` | `_intelligence/_woland/*_uns_*.md` and scene `*_trace_*.md` | the human/LLM narrative of a bout |
| `oeas-packets` | `_intelligence/unified_oe_packets.jsonl` | Symbol Game packet steps |
| `oeas-woland` | `_intelligence/_woland/*_receipt_*.json` | scene receipts, licensing verdict |
| `oeas-skills` | Seal-and-Mine positive proposals; skill-inbox rows | what was *proposed* |
| `oeas-antiskills` | `_intelligence/_antibodies/` and anti-skill inbox | what was *refused* |

No dataset for live claim IDs as a source of truth. If a
claim unit is mentioned, it is `prefix:track:local-id` as a
*field*, copied from the census, not allocated by Axiom.
Shipping a skill or anti-skill event does not promote it.
Mined objects stay `PROPOSED` with `AuthorityEffect: None`.

## What Axiom must not do

- Originate bit keys, ledger rows, or lock lifecycle.
- Store jewel promotions. Those stay with the declaring
  prefix (`multi_repo.md`).
- Ingest `__pycache__`, tokens, or the abandoned-mine tree.
- Ingest encyclopedia markdown bodies or keep a growing
  `_intelligence/` tree in this vault.
- Promote a skill or anti-skill by ingesting it.
- Treat “latest dashboard” as an import. Pin dataset names
  and query text in a versioned file when a dashboard
  becomes apparatus. Floating APL in a chat is a query, not
  a receipt.
- Become a second AuthorityEffect. A panel that cannot
  compute the asked quantity is a Note, not a substitute
  number (Axiom dashboard discipline).

## Hot local window, then ship

Woland, other OEAS instances, UNS, UTS/UTC, Symbol Game,
and skill / anti-skill traffic are **research streams**.
They are not a second vault.

Keep **about one day** of local files under
`_intelligence/` (or the later operations equivalent).
After a successful ingest, delete or rotate anything
older. Do not commit the growing JSONL or UNS tree into
`19L57G1`. Do not let `_intelligence/` become a hold.

Ship to Axiom for research queries: counts, Φ₁ / γ₂
trends, refusal classes, antibody harvest, “which scene
verdict last failed.” Replay of a *claim* still uses
fossils and the triad, not the dashboard.

If free-tier quota cannot take full UNS markdown, ship
the UTS line plus `evidence_sha256` and a short excerpt;
keep the full narrative only inside the one-day window.
Quota blow-up is refused (`open_conflicts.md` §9), not
“we will see.”

## Library markdown (off-repo is later)

`lib/markdown` stays a hold in this phase. Moving the
bodies off this repo is a later discussion. It starts to
matter if the system is put **online for money**, not
now. Until then: Axiom still sees a manifest only, not
the text.

## Scale residual: the system eats its own output

Woland / Symbol Game / Seal-and-Mine can farm antibodies
and proposed skills from a bout, then feed those into
the next bout. Volume is not linear in “number of
users.” It is the run eating yesterday’s run. Terabytes
of UTS, UNS, packets, and receipts can appear quickly
once that loop is live.

The free org is a **probe**, not that store.

When (if) this is online for money:

- Earn-a-bill / a paid events store is decided **before**
  the loop is left running, not after the first terabyte.
- Local “about one day” is a research-machine window.
  A paid loop needs an explicit retention pack (hot /
  warm / drop) owned by operations, not by this vault.
- Default ship is the UTS line (and skill / anti-skill
  *proposals*). Full UNS and packet bodies are sampled
  or hashed. Shipping every narrative is an earn, not
  the default.
- Axiom still does not store “the intelligence.” Grown
  artifacts that are meant to persist are fossils,
  proposed skills, or claim units — each on its own
  path, with `AuthorityEffect: None` until admitted.
- Eating own output does not authorize that output.
  A log of a proposed skill is not a live skill. A
  terabyte of UNS is not a library.

This residual is open. Naming a vendor or a cold-store
layout is refused until a go. See `open_conflicts.md`
§11.

## Relation to OES and the holds

`lib/` and `programs/` are holds. Axiom sees **manifests**
of those holds, not the markdown bodies. Spine extract and
lock tables stay on disk / in operations. Op-read may *emit*
a candidate event to `oer-opread` after it has already
written the candidate locally. Swarm streams above are
operations telemetry, not an OES layer.

## First use, when someone says go

1. Confirm the org is still free and list datasets from the
   console (no token in git).
2. Create `oer-census` only. Ingest the existing
   `programs/000_obstruction/census.json` as one event (or
   one event per slot).
3. One dashboard: slot file counts. No jewel panel.
4. Stop. Conversion-quality gate and firewall census still
   block promoting holds. Swarm ship (`oeas-*`) is a later
   named go. Off-repo library and a paid/TB store wait
   until the system is actually going online for money.
   Do not start the one-day rotator from this page.

Implementation lives in operations when that remote exists.
This vault cites the org. It does not own the ingest job.

Operator apparatus already on this machine (skills, not
authority): Axiom dashboard / APL / cost / SRE plugins
talk to `~/.axiom.toml`. Those are how a later go is
executed. They do not create datasets from this page.
Dashboards follow compute-or-defer: a panel that cannot
answer the asked quantity is a Note, not a substitute
count. Version the dashboard JSON beside the APL if it
becomes apparatus.

`AuthorityEffect: None.`
