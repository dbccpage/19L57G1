# Multi-repo prefixes (plan)

**AuthorityEffect:** None. Do not cut remotes in this phase.

Bits 0–3 of the bit index. Not paper numbers. The versioned
16-row mapping is `prefix_table.md`. How they are cut — four
first remotes, later instances, archives as history — is
`repo_split.md`. OES spines, locks, and op-reads compose
with this striping as written below. The two plans must not
drift apart.

A 2026-08-17 multi-color pass (Grok lead, Harper, Benjamin,
Lucas) treated the letter list as the striping layer under
OES. Red named the hinges. Green made them executable
without cutting a remote. Blue composed prefixes with spines
and residuals. This revision records all three.

The earlier closing line “assign the remaining 4-bit codes
before any second repo allocates” is **kept as a law** and
**withdrawn as a deferral**. The table is sealed: only
`0000` and `0001` are assigned; every other row is reserved
until an admit names the letter. Unused slots are never
allocated ad hoc.

## First remotes (directory until earned)

- `0000` OER — this vault. Citer. Not a product factory.
- OEC — Omega Engine. Mathematics. Publishes crates and/or a
  release binary. No bit code yet.
- OEAS — swarm base class. A library. Not a binary. No bit
  code yet.
- OEAG — governance. Versioned policy packs. Not a live
  checkout at runtime. No bit code yet.

## Later (directories until earned)

- OEOS, OEAR, OETC — instances. No bit codes yet.

## History

- OEE — estate / archive letter. Hashed history only. See
  `archives.md`. Not a product remote. No bit code yet.
- `0001` — unknown / other.

## Laws

**Law:** OEAS is the base class. OETC, OEAG, and OEAR
instantiate it. They depend on OEC. They cite OER. They do
not own OER papers. Letters do not enforce this. The
spine-level firewall below is what makes it checkable.

**Law:** a consumer pins a tag or SHA. “Latest build” is a
query, not an import. A floating branch or “latest” import
is a non-empty Residual. Only an explicit tag or SHA
discharges it.

**Law:** `C:\Users\a343o\source\repos\anomalon` is an
abandoned dual-language mine. Not a live prefix. Not either
archive. Quarantine is a sealed path + content-hash
denylist (ConfigGauge). Any spine extract or residual
certificate that touches a denylisted path emits a non-empty
Residual and is refused. Hashes are not invented here; the
object is required before any extract that could see that
tree.

The earlier reading of this list as eight equal first
remotes is withdrawn. The first cut is the four under
“First remotes”.

## Earns a remote (falsifiable)

Until every item is true, the entity remains a directory.
“Earned” is not urgency or taste.

1. `prefix_table.md` is already sealed (it is).
2. At least one independent consumer pins a tag or SHA, not
   `main` / “latest”.
3. The domain ontology document, if the remote will host
   claim units, exists and passes its conversion-quality
   gate (`oes.md`, `code_spine_kinds.md`).
4. Zero open residuals of severity `cross-ownership` or
   floating-pin.
5. An AuthorityEffect review record that the remote does not
   invert the dependency laws.

Ontology documents live in the owning remote once it exists.
Until then they may be planned here. OER cites them. It does
not own OEC/OEAS kinds.

Cutting a remote is an author’s act. This page does not do
it. The named first-remote list is not permission.

## Composition with OES

**Stable IDs** carry the prefix: `prefix:local-id`. See
`prefix_table.md`.

**Cross-repo edges**, script-licensed only:
`references_by_name`, `shares_identifier`, `cites_by_prefix`,
`tested_by_link` when the foreign unit is literally named,
`appears_in` (rare). Ownership, implements,
depends_for_correctness, owns_paper, is_authoritative_for,
fills_lock across prefixes: forbidden as auto-edges;
require sealed admit that itself carries residual cost.

**Residuals carry prefix provenance.** A Residual born under
P and absorbed under Q keeps an obligation
`cross-prefix:P→Q:…`. Silent absorption of a foreign
residual is refused. Discharge needs a local witness or an
explicit cross-prefix admit.

**Locks are scoped by prefix.** Canonical short form:

1. Ownership and provenance stay with the declaring prefix
   forever. The lock object never moves.
2. Foreign prefixes see locks only as candidate holes.
3. Every cross-prefix fill attempt or supersession proposal
   emits a residual (`cross-fill-attempt:P←Q:lock-id`,
   `cross-supersede-proposal:P←Q:lock-id`).
4. Only the declaring prefix (or a joint protocol it has
   already accepted) may promote to jewel or retire the
   lock.
5. Observational edges may cross prefixes; ownership edges
   may not.
6. Archive (OEE) locks are historical candidates only. Live
   fill requires residual-gated promotion back to a live
   prefix first.
7. Conflicting locks across prefixes remain distinct.
   Resolution is a new residual-gated decision, never
   automatic. High-severity conflicts may escalate to OEAG
   under the limits below.

Jewel promotion from a foreign fill is **citation +
residual**, never ownership. Witness: residual movement
whose provenance names both prefixes, a deterministic test
accepted by P, or a sealed admit under P. Channel match
alone is never a jewel.

Op-read may query many prefixes and return candidates only.
It never rewrites a foreign spine or lock table. Thin-spine
diffs are computed inside one prefix first. Cross-prefix
diff is an explicit, residual-aware view. Lock tables stay
per-prefix objects.

## OEAG residual limits (policy packs only)

OEAG owns *meta-residuals* and *limit policy packs*. It does
not own ordinary claim residuals. Packs are pinned versioned
objects under the OEAG prefix. “Latest pack” is a query, not
an import. A floating governance pin is a Residual.

Hard limits, sealed before any second remote allocates a
named row:

1. Depth ceiling **k = 2**. Depth 0 local, 1 cross-prefix, 2
   escalation. Depth ≥ 3 → refuse +
   `residual-depth-exceeded`.
2. Volume quota per (source-prefix, target-lock). Soft:
   meta-residual. Hard: refuse + `cross-fill-spam`,
   discharged only by the offender.
3. Only these severities may escalate: `cross-ownership`,
   `foreign-lock-mutation`, `authority-inversion`,
   `unbounded-cascade`. Severity is immutable. OEAG may not
   downgrade it.
4. A governance residual is terminal. OEAG may
   accept/reject/advise a limit with TTL. It may not rewrite
   provenance, move a lock, expand observational or ρ\*
   licenses, invent residual kinds only it can discharge, or
   discharge ordinary residuals.
5. Changing a limit emits `policy-pack-change:…` and is not
   active until the residual discharge condition (or
   multi-prefix admit) is met.

## Residuals that remain (unexecuted)

1. Content hashes for the abandoned-mine denylist.
2. The earn checklist as a machine-checkable object, not
   only this prose.
3. Running per-prefix lock tables and the residual shapes.
4. Bit-field overflow if more than fourteen further remotes
   are ever wanted. Not solved here. Do not widen bits 0–3
   in this folder.

`AuthorityEffect: None.`
