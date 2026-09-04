# PLAN: the second derivation

`AuthorityEffect: None`.  This file contains only the execution plan, the
write-root boundary, the assumption discipline, the proof gates, the test
gates, and the stopping conditions, as `SEED.md` section 0 requires.
Operating instructions live in `MANUAL.md`.

## Write-root boundary

The seed is `research/second/SEED.md`, sha256
`52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e`,
read-only.  `CLAUDE.md` governs and is not amended.  Nothing under
`prompt/`, `paper/`, `code/`, `lean4/Derivation/`, or `artifacts/` is
written, and no earlier research tree is written.  This run writes only
`research/second/` (this plan, the manual, the paper, the change log, the
claim ledger) and `research/second_<rung>/` for each rung, plus the
registration of each rung in the research job of the workflow.

Every consumed source is pinned as a canonical Git blob at a snapshot
commit that is an ancestor of HEAD.  A supplied tree that is not on
`main` at a rung's snapshot is recorded as absent at that snapshot, its
replay is OPEN, and the rung that first finds it on `main` replays it.

## Execution plan

1. Rung 0, `research/second_inheritance/`: replay every supplied receipt
   this run will cite; list the declared inputs of the supplied process
   by name and by introducing event; show inertia at the second level.
2. Rung 1: the stream as a response at a three-item bound (Challenge 1).
3. Rung 2: the stake read off the state (Challenge 2).
4. Rung 3: the engine as a declared class (Challenge 3).
5. Rungs 4 and 5: run forward; the census of definability.
6. Further rungs by the seed's next-rung rule, to twelve at most.
7. Freeze; then the comparison, in the companion repository only.

Each rung: freeze its question and predictions by hash before any
computation and before any Lean; compute; score mechanically; keep misses
as findings; name leftovers; pin sources; register its checks; one pull
request against `main`, never stacked.

## Assumption discipline

The seed's section 6, without addition.  Every notion carries exactly one
class.  The guarded words, including "engine", appear only with a proof
or a precise conditional scope.  A demand read off the state is kept
distinct from a demand emitted by an act.  A receipt is not a payload; a
pin proves only that a source did not move; a gate is proved by injection
and never by being green.

## Proof gates

Every theorem-level claim used by `research/second/paper.md` has a Lean
proof in some rung's committed package, with its `#print axioms` report
in that rung's committed axiom log checked against a fresh build, or is
downgraded to computation, conjecture, countermodel, or OPEN.  No
`sorry`, `admit`, user-declared `axiom`, `unsafe`, or `partial`, in code
or in comments.  Library-axiom reliance is recorded in the claim ledger.

## Test gates

Each rung's tests pass under strict typing, with line and branch coverage
each at 95% measured from inside the rung; every receipt regenerates
identically; every result replays from the sealed genesis; the root
identifier firewall and the prose watchlist stay clean with no pin
regenerated.  Every rung's verifier, tests, and typing are registered in
the research job.

## Stopping conditions

The seed's section 12, without addition.  In particular: the count of
declared inputs is reduced below two or proved at its floor within stated
bounds; every engine in the declared class is run to bounds, refuted, or
OPEN; every census row is decided at every stage reached; every gate the
run adds is proved by injection; the comparison is written after the
freeze, in the companion repository only, and causes no revision here.
