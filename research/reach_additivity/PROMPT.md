# reach_additivity — the native run charter

`AuthorityEffect: None.`

## The question

Direct author instruction, 2026-09-03: *do the reach additivity rung next.*

The preceding rung declared a base-relative cost — the number of pluggings a
response makes derivable — and left as its second open whether that cost is
additive along composition:

    cost(base, d ; e)  =?  cost(base, d) + cost(apply(base, d), e)

The stated reason for asking: if it holds, a sequence of moves has a price
rather than a re-measurement, and the estate has something an optimizer can
sum along a path.

**This charter widens the question before answering it**, because the narrow
form cannot be answered honestly. The sealed candidate grammar declares no
composition on responses at all, so the first act is to declare one, and a
declared operation can be declared to make the answer come out either way.
The defence against that is to prove the general statement: not *is this cost
additive*, but *which costs are additive, and what does additivity buy*.

## Write root and seal

Write root: `research/reach_additivity/` only. Sealed and frozen: `prompt/`,
`paper/`, `code/`, `lean4/Derivation/`, `artifacts/`, `CLAUDE.md`, `ci/`,
`.github/`, root `tests/`, `pyproject.toml`, `requirements.txt`, every
sibling research tree, and the census pin. Snapshot
`7fcd72f618e676a88df65efed4926ac3c11eacbe` of `main`. Every pull request
targets `main` directly.

**The preceding rung is unmerged.** `research/reach_measure` sits in an open
pull request and is therefore not on `main` and not pinnable. This tree
consumes no file of it. It restates the cost it studies from the sealed
`profiles` in two lines and says so in `SOURCE_MANIFEST.json`; the pin is
named as a follow-up and is not claimed here.

## The two operations, declared

**Composition of responses** is concatenation of item sequences:

    (d ; e) = d followed by e

**A difference cost** is any cost of the form

    diff_P(base, delta) = P(apply(base, delta)) - P(base)

for a state functional `P`. The preceding rung's cost is the instance at
`P = total profile size`. Nothing below is special to that instance, and the
generality is the point: a result about one hand-picked cost would be a
result about the hand.

## What must be settled, in order

1. **Whether the action is sequential**: `apply(base, d ; e)` equals
   `apply(apply(base, d), e)`, including agreement on ill-formedness. This
   is prior to every cost question and is a fact about the sealed grammar,
   not about any measure.
2. **Additivity**, for every difference cost, as a consequence or a
   countermodel.
3. **What additivity buys**, which is the part the instruction is really
   asking about. A cost that is additive along composition still has to be
   summed along a path, and the sum may or may not depend on the path.
4. **Whether the sealed item count is a difference cost**, decided rather
   than assumed.

## Refusals

`FW-SEAL` no path outside the write root is written.
`FW-NAME` no outside theory, programme, or person name.
`FW-DECLARE` the composition operation is declared, not discovered. No
sentence calls it canonical, forced, or the only one, and the charter says
plainly that a different declaration could give a different answer.
`FW-SCOPE` every count carries the rectangle it was computed over.
`FW-BUYS` additivity is not silently upgraded into path-independence, into
an action along a path, or into a capability. If the two come apart, the
gap is the result and is stated as one.
`FW-VACUOUS` a theorem that holds because its hypothesis is never met is
recorded as vacuous. If a closed walk of moves does not exist in this
grammar, no statement about closed walks is offered as a finding.
`FW-PRIOR` the preceding rung's own summary of this open — that additivity
would give the estate an action functional — is a claim of this session and
carries no authority. If the run contradicts it, the contradiction is
recorded against it by name.

## Terminals, pre-agreed

`SEQUENTIAL_ACTION_HOLDS`, `SEQUENTIAL_ACTION_FAILS`, `ADDITIVITY_HOLDS`,
`ADDITIVITY_FAILS`, `PATH_INDEPENDENT`, `PATH_DEPENDENT`,
`CIRCULATION_WITNESS_FOUND`, `NO_CIRCULATION_IN_RECTANGLE`,
`COUNT_IS_A_DIFFERENCE_COST`, `COUNT_IS_NOT_A_DIFFERENCE_COST`,
`OPEN_AT_NAMED_TARGET`. Both branches of every question above were written
here before anything ran.
