# Repo split — products, not a cut-up app

**AuthorityEffect:** None. Plan only. Do not cut remotes in
this phase. Prefix letters stay as in `multi_repo.md`; no new
bit codes are assigned here.

## The idea

One application does not live across remotes. Products publish
artifacts. Other trees **pull** a pin.

That is the whole split. You can design the interface across
remotes (crate surface, CLI, policy-pack schema, "this binary
answers that question"). You cannot design the implementation
of one program across remotes. A composition checkout that is
secretly the application is the thing this page refuses.

## First remotes (four)

Cut these when a remote is earned, not before. Until then they
may remain directories.

| Product | Prefix | What it is | What a consumer pulls |
| --- | --- | --- | --- |
| Research vault | OER | This repository. Claims and research Lean. Citer, not a product factory. | A citation. Not code. |
| Omega Engine | OEC | The mathematics. Source of the other **crates**, not of the other **remotes**. | A library and/or a release binary, at a tag or SHA. |
| Swarm base | OEAS | The agentic-swarm base class. | A library (package or crate). Not a binary. |
| Governance | OEAG | Who may change the rules, and which pack is in force. | A versioned policy pack. Not a live checkout at runtime. |

**Law (unchanged):** OEAS is the base class. Later swarm
instances instantiate it. They depend on OEC. They cite OER.
They do not own OER papers.

**Law:** this vault stays a citer. Engine work does not land
under sealed `code/` or as a runner this repository would then
have to regenerate.

## Pins, not latest

"What's the latest build?" is a **query**. A dependency is a
tag or a SHA.

Unpinned `main` as an import is how replay dies. The same rule
applies to governance: versioned packs, not whatever the
governance remote says this morning.

## Crates versus remotes

OEC may be a workspace that **publishes** several crates
(`omega-engine` and friends). That is one remote, several
artifacts. Normal. Do that first.

"The math creates the other crates" means published output
from OEC. It does not mean OEC owns the git history of OEAS,
OEAG, or a swarm instance. Generated artifacts, not generated
remotes.

A base class is not a binary. Inherit OEAS. Run OEC.

## Not first remotes

These prefixes remain vocabulary. They stay directories (or
unbuilt) until they have a different cadence, access list, or
secrecy boundary:

- OEOS — operating system
- OEAR — research swarm instance
- OETC — Techne / coding swarm instance

Operations, library, frontier, university, dashboards, and
similar names in the estate are **directories inside a
product**, not a 1:1 remote map. The 4-bit repo field fits
eight planned prefixes with spare slots. It does not fit a
per-component cut of today's tree. Freeze the field before
anyone allocates a second key. See `bit_index.md`.

Do not split to save CI. Private minutes are one account pool.
Eight Lean installs copy the slowest job. Split for access
control and blast radius.

## Archives are history, not products

The Omega Engine archive and the Anomalon archive are the best
history on hand. They are **not** first remotes and they are
**not** on the build path. They stay put. They get hashed.
If a good idea was forgotten, that is where it will be found.

Cleanup of those trees is an operator pass outside this
repository. It does not block the four products. It is not a
gate. Details: `archives.md`.

## What this page withdraws

An earlier draft treated the eight prefixes as an equal first
cut (core, base swarm, governance, research swarm, coding
swarm, OS, this vault, estate). The **letters** stay. The
**first remotes** are the four in the table. The rest wait.

A sibling page in another worktree argued the same CI-cost
point and recommended submodules as the composition story.
Composition-by-pin is still allowed for an **operator**
checkout. It is not how applications are built. Consumers
pull the artifact.

`AuthorityEffect: None.`
