# PLAN: the boundary derivation

`AuthorityEffect: None`.  Only the execution plan, the write-root
boundary, the assumption discipline, the proof gates, the test gates,
and the stopping conditions, as `SEED.md` section 0 requires.  Operating
instructions live in `MANUAL.md`.

## Write-root boundary

The seed is `research/boundary_seed/SEED.md`, sha256
`ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be`,
read-only.  This run writes only `research/boundary_seed/` and the
append-only registration of its checks in the research job of the
workflow.  Until `FREEZE.md` exists, this run reads nothing of the
repository beyond the seed, the five named sections of `CLAUDE.md`, and
its own tree; it imports nothing from `code/derivation`; and
`test_blind.py` fails any checked write-root version that cites a sealed path, a
claim identifier, a sealed Lean name, or another research tree.

## Execution plan

1. Challenge 0, `challenge0/`: the initial state `<|>` under readings U
   and O, with no object-language operation.
2. Challenge 1, `challenge1/`: the supply of `<a|>`.
3. Challenge 2, `challenge2/`: `<a|>` and `<|a>` retained.
4. Challenge 3, `challenge3/`: required separation of those two.
5. Challenge 4, `challenge4/`: `<a|b>` and `<b|a>`.
6. Challenge 5, `challenge5/`: `<<a|>|>`, a whole within a side.
7. Autonomous continuation to fifteen accepted rounds per branch under
   each reading, or to a declared bound with the frontier exported.
8. The freeze; then `comparison.md`, in native vocabulary, after it.

Each challenge: its `PREDICTIONS.md` frozen by hash before any
computation and before any Lean, with one extrapolation about the next
challenge; the kernel extended only as the challenge requires; results
classified; misses recorded next to their values; leftovers named.

## Assumption discipline

The seed's section 6, without addition.  The admitted boundary is an
admitted primitive and is listed first in every ledger.  It is never
called free.  Side, containment, and order are kept distinct from one
another and from identity.

## Proof gates

Every theorem-level claim used by `paper.md` has a Lean proof in
`lean/`, a package with no dependency on the sealed package, its axiom
log committed and checked against a fresh build, or is downgraded.  No
`sorry`, `admit`, user-declared `axiom`, `unsafe`, or `partial`, in code
or in comments.  A target true by unfolding a definition is labelled
DEFINITION-level and never counted as content.

## Test gates

The tree's own tests pass under strict typing with line and branch
coverage each at 95%, measured from inside the tree by
`check_coverage.py`; every receipt regenerates identically; every
certified state replays from genesis; the source-isolation scan passes on
every distinct committed write-root version before the freeze; the
repository's identifier firewall and prose
watchlist stay clean with no pin regenerated; every gate the tree adds is
proved by injection.

## Stopping conditions

The seed's section 11, without addition.
