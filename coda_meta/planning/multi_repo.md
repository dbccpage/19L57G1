# Multi-repo prefixes (plan)

**AuthorityEffect:** None. Do not cut remotes in this phase.

These prefixes occupy **bits 0–3** of the bit index when a
second repo starts allocating keys. They are not paper numbers.

How they are cut — four first remotes, later instances,
archives as history — is `repo_split.md`. This page is the
letter list only.

## First remotes (when a remote is earned)

- `0000` OER — Omega Engine Research. Lives in `19L57G1`.
  Citer. Not a product factory.
- TBD OEC — Omega Engine. The mathematics. Publishes crates
  and/or a release binary. `anomalonpy/omega_engine` and
  `omega_engine_rs` are the current names, not a promise they
  stay one directory forever.
- TBD OEAS — Agentic Swarm base class. A library consumers
  inherit. Not a binary.
- TBD OEAG — Governance. Versioned policy packs. Not a live
  checkout at runtime.

## Later (directories until they earn a remote)

- TBD OEOS — Operating System.
  `omega_engine_operating_system`.
- TBD OEAR — Agentic Research Swarm instance.
  `omega_engine_agentic_research_swarm_host`.
- TBD OETC — Techne Coding Swarm instance (OEWAS). Skills
  plus `omega_engine_workflows_agents_skills`.

## History (not a product remote)

- TBD OEE — estate / archive letter. May later name hashed
  history objects. The two dumps on hand — Omega Engine
  archive and Anomalon archive — stay put; see `archives.md`.
- `0001` — unknown / other.

## Laws

**Law:** OEAS is the base class. OETC, OEAG, and OEAR instantiate
it. They depend on OEC. They cite OER. They do not own OER
papers.

**Law:** a consumer pins a tag or SHA. "Latest build" is a
query, not an import.

**Law:** `C:\Users\a343o\source\repos\anomalon` is an abandoned
dual-language mine. Not a live prefix. Not either archive.

The earlier reading of this list as eight equal first remotes
is withdrawn. The letters stay. The first cut is the four
under "First remotes".

Assign the remaining 4-bit codes before any second repo
allocates a bit key. 0000 is reserved for this vault.
