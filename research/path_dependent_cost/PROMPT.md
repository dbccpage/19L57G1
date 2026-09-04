# path_dependent_cost — the native run charter

`AuthorityEffect: None.`

## The question

Direct author instruction, 2026-09-03: *now find the path-dependent
base-relative cost.*

The preceding rung proved that a cost of the form
`P(apply(base, delta)) − P(base)` telescopes: its total along a sequence of
moves is fixed by the endpoints, so it cannot tell one route from another
and its total around any closed walk is zero. A cost with that property
carries no obstruction, because obstruction is exactly what a coboundary
does not have. It also proved that the sealed item count is **not** of that
form — but the item count is base-free, and the rung named the target that
remains:

> a cost that is additive along composition, reads the base, and is **not**
> a difference of a state functional.

This tree looks for one, and refuses to accept a hand-tuned function as an
answer.

## Write root and seal

Write root: `research/path_dependent_cost/` only. Sealed and frozen:
`prompt/`, `paper/`, `code/`, `lean4/Derivation/`, `artifacts/`, `CLAUDE.md`,
`ci/`, `.github/`, root `tests/`, `pyproject.toml`, `requirements.txt`, every
sibling research tree, and the census pin. Snapshot
`7fcd72f618e676a88df65efed4926ac3c11eacbe` of `main`. Every pull request
targets `main` directly.

**Two preceding rungs are unmerged**, `research/reach_measure` and
`research/reach_additivity`, so neither is on `main` and neither is
pinnable; stacking on an open pull request is prohibited. This tree consumes
no file of either. It restates the same two-line state functional from the
sealed `profiles` and declares the restatement in `SOURCE_MANIFEST.json`.
Where it relies on a result of theirs it re-proves it here rather than
citing across an open branch, and says which results those are.

## What must be settled, in order

1. **What the search space is.** Additivity along composition is a
   constraint, not a wish. Before hunting for a cost, characterise every
   cost that satisfies it, so that the hunt is over a described set rather
   than over whatever occurs to the author.
2. **Where path-dependence can come from at all.** Admission only adds, so
   the reachable states are ordered by what stands in them. That may forbid
   whole classes of closed walk, and a search for path-dependence in a
   place where it is impossible would be wasted.
3. **Whether the estate's own move graph carries the structure needed.**
   Two distinct routes to the same state, or none. This is a fact about the
   sealed grammar and is computed, not assumed.
4. **A cost, exhibited.** Additive, reading the base, and provably not a
   difference of any state functional.
5. **Whether it is one cost or many**, and whether the different sources of
   path-dependence are the same phenomenon or different ones.

## Refusals

`FW-SEAL` no path outside the write root is written.
`FW-NAME` no outside theory, programme, or person name.
`FW-TUNED` a cost invented to have the property is not an answer to the
question. Every candidate priced here is declared before its circulation is
computed, with the reading that motivates it, and a candidate that turns out
to be exact is reported as exact rather than dropped.
`FW-DEGENERATE` a cost whose only path-dependence is that it charges for a
move that changes nothing is reported as that and not as the general
article. If waste is the only source found, the run says so.
`FW-SCOPE` every count carries the rectangle it was computed over.
`FW-VACUOUS` if the structure a statement quantifies over does not occur in
the rectangle, the statement is recorded as vacuous rather than as a
finding.
`FW-CLASS` a computed rank over a finite rectangle is a fact about that
rectangle. No sentence turns it into the rank of anything larger.
`FW-PRIOR` the two preceding rungs are unmerged claims of this session and
carry no authority. Any result of theirs used here is re-proved here, and if
a re-proof fails the failure is recorded against them by name.

## Terminals, pre-agreed

`SEARCH_SPACE_CHARACTERISED`, `TWO_ROUTES_EXIST`, `NO_TWO_ROUTES`,
`PATH_DEPENDENT_COST_EXHIBITED`, `NO_PATH_DEPENDENT_COST_FOUND`,
`ONLY_DEGENERATE_PATH_DEPENDENCE`, `RANK_COMPUTED`,
`DIRECTED_CLOSED_WALKS_ARE_STATIONARY`,
`DIRECTED_CLOSED_WALKS_ARE_NOT_STATIONARY`, `OPEN_AT_NAMED_TARGET`. Both
branches of every question above were written here before anything ran.
