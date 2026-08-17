# Project Anomalon — Codename Woland (plan)

**AuthorityEffect:** None. No remotes are cut here.

We plan the whole project together: research vault, core engine,
operating system, swarms, and a research community. Claude is
reviewing this same planning tree in a separate worktree. Grok
lands planning only under `coda_meta/planning/`. Neither worktree
implements the vault until you say go.

## Four first remotes, one project

How they are cut is `repo_split.md`. Short form:

- Research — claims, Lean, private library. Prefix OER
  (`19L57G1`). Cites. Does not ship the engine.
- Engine — mathematics. Prefix OEC. Publishes crates and/or
  a release binary. Consumers pin a tag or SHA.
- Swarm base — OEAS. A library to inherit. Not a binary.
- Governance — OEAG. Versioned policy packs.

OS, research-swarm, and Techne (OEOS, OEAR, OETC) stay
directories until they earn a remote. They instantiate OEAS;
they do not start as remotes of their own.

Estate papers in anomalonpy stay **frames** (OEE). They are not
renumbered as OER papers. The Omega Engine archive and the
Anomalon archive are hashed history, not frames and not
products; see `archives.md`.

The earlier "three communities" grouping (research / core /
swarms-as-one-bucket) is withdrawn as the first-cut map. The
swarm **law** below is not withdrawn.

## Source-of-record split (from the external note)

- anomalonpy (and later OEC) is source of record for **code and
  product**.
- `19L57G1` is source of record for **research claims and
  research Lean**.
- Copy library and selected research one way. Do not live-link
  both ways. Dual sources of truth already hurt once.

## Secrecy

This research repo stays **private**. Visibility bit `1`
(public Substack, LinkedIn, explainers) lives in a detached
surface repo. Public content must not carry Lean or claim
ledgers from this vault.

## Swarm law (repeat)

OEAS is the base class. Techne (OETC), governance (OEAG), and
research swarm (OEAR) instantiate it. They call OEC. They cite
OER. They do not promote OER papers.

## How we review together

1. Planning PRs land only under `coda_meta/planning/`.
2. Claude's worktree comments on those files, or adds a
   sibling page in the same folder via his own PR.
3. Conflicts with the seal stay in `open_conflicts.md`.
4. Implementation is a later, named go.

Internal track codes stay `X` / `N` / `Q`. External speech can
say frontier / spine / quarantine so the names do not age as
memes.
