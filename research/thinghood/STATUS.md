# Thinghood research packet -- status

A packet that supplies an agent prompt for one construction run.  It
does not itself answer the questions.  It records the boundary under
which an agent may begin building.

## Repository boundary

This tree is an explicitly non-sealed research surface.  It must not
modify or regenerate anything under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`.

It follows the precedent of the sibling trees
`research/primitive_difference_tower/`, `research/portable_interface/`,
`research/blind_restart/`, `research/partial_decide/`, and
`research/genesis_continuation/`.  Vocabulary is taken from
`research/genesis_continuation/native_terms.md` plus the native names
already fixed in `lean4/Derivation/PrimDiff.lean` and
`lean4/Derivation/PrimitivePassage.lean`.  The prompt introduces the
caller-supplied word **thing** as an externally imposed challenge, not
as a derived object.

Nothing external is named here.

## What is here

- `PROMPT.md` -- the whole of what a solver is given.  Demands,
  refusals, and a reply format.  No winning candidate is tabulated.
- `STATUS.md` -- this boundary note and the result of the run below
- `CLAIM_LEDGER.md` -- stable claims, evidence classes, and falsifiers
- `thing.py` -- the finite candidate grammar, cost, predicates, and reports
- `test_thing.py` -- positive and adversarial negative tests
- `run_thing.py` -- deterministic receipt writer
- `receipts/thing.json` -- the regenerated, timestamp-free receipt

## Registration note

This tree is **not** named by `.github/workflows/verify.yml`'s research
job.  Its receipt is therefore a local research record and can go stale
silently until an author separately registers the surface.  No registration
or sealed-path change is part of this run.

## How to run

Paste `PROMPT.md` into a solver that can write this repository.  The
solver works only under `research/thinghood/`.  It does not amend
`CLAUDE.md`, does not touch sealed prompt bytes, and does not close
`OB-1`.

## Nonclaims

- Supplying the prompt is not a derivation of a thing.
- Restating `FidelityObstruction` is not an answer to "what is a thing?".
- `two_rule` is not a dynamical law of the inscription.  The prompt
  forbids treating it as one.  That prohibition is a run rule, not a
  new theorem.
- `OB-1` remains open.  This packet does not change it.

## Result of the 2026-08-27 run

The prompt was executed with `PROMPT.md` byte hash
`ad70e80ec1eb9fd884671cad00881405b4ea4301d1f756472c35e105ebaf8bfc`.
All writes are under this directory.  The sealed paths named above were not
edited or regenerated.

### Q1 -- thinghood

The declared finite space has carrier sizes 1--3, relations with at most
three edges, the six law choices listed in `thing.py`, all eight subsets of
the independently priced stores `retained`, `protected`, and `observed`, the
A3-style metatheoretic inequality flag, and independent budget/license
resource flags.  It contains 120,640 valid candidates.  The cost is one
additive atom per carrier point, relation edge, asserted admission, law atom,
metatheoretic inequality, store admission, budget admission, and license
admission.

`collapse_fails_law` requires an admitted ordered pair, a law satisfied before
the map, and an endomap identifying that pair whose pushforward violates the
same law.  A collision with no law is not a failure of a law.

The exhaustive receipt reports minimum cost 5, four raw minima, and two
non-isomorphic minimum classes.  Their representatives are a two-point
asserted irreflexive edge and the same edge governed by the asymmetric law.
The finite law-order check records asymmetry as strictly richer than
irreflexivity (and retains the two-cycle countermodel to the converse).
There are no below-minimum survivors.  Thus the run issues
`THINGHOOD_CHARACTERIZED`, records `THING_COINCIDES_WITH_A1I` for one minimum
class, and records the tied `THING_STRICTLY_RICHER_THAN_A1I` class.  It does
not select a unique delta: the non-uniqueness is the result.  Unlisted laws,
stores, or cost measures remain `CANDIDATE_SPACE_OPEN`.

The implication lattice keeps `datum`, the local A1i `difference` predicate,
and `thing` distinct.  The bare-pair countermodel falsifies `datum -> thing`,
while the tied asymmetric minimum falsifies `thing -> difference`.  The local
A1i representative is not renamed in the sealed papers (`REFUSED`).

### Q2 -- dynamics

The five conditional claims in `CLAIM_LEDGER.md` and the receipt issue
`NO_FORCED_DYNAMICAL_LAW` with this scope only: the inscription supplies no
successor; a collapsed pair is not an active obstruction; `obstP` has four
independent gates; `two_rule` requires an active, in-bounds protected
obstruction; and `two_rule` is a response menu at that obstruction, not a law
of the inscription.  Their `machine_check` field is `false` and the receipt
records `machine_check_status=NOT_RUN`: this tree does not elaborate or
resolve the sealed theorem names, so `CONDITIONAL_THEOREM` is a downgrade,
not a dual-witness theorem.

The result is split by source.  Under declared `stepRefl` plus
pair-separation closure, `generation_never_dries` supplies a live demand from
`n >= 3`; that is demand persistence relative to a declared composite, not a
successor or repair forced by the inscription.  The bounded `tick_analysis`
probe then checks collision, equal profiles, and directional residual with no
store, observer, closure policy, or demand source: all three have zero
resource-free endogenous survivors.  Their declared fallback classifications
are `VOID_CYCLE`, `CHALLENGE_0`, and `VOID_CYCLE`, respectively.  This is a
finite accounting result only; S6.6, S9's last bullet, and OB-1 remain open to
a wider tick grammar.  The same-level repair/create-structure ceiling is
kept; no object-language generator and no cosmology is written.

The three required opens remain explicit:

- `OB1_UNCHANGED` -- no object-language endogenous demand generator.
- `S66_UNCHANGED` -- the static difference object does not derive a next
  challenge.
- `S9_LAST_UNCHANGED` -- the companion inscription is not silently elaborated
  into a witnessed irreflexive datum.  Carrier, two occurrences, relation,
  witness, irreflexivity, and orientation remain admissions if that bridge is
  ever attempted.

The previously established limit statements remain scoped to
`LocalStrategy` plus `FiniteDeclaration`; this run does not turn a finite
local alphabet into an infinite extension sequence.  Withdrawals remain
withdrawals, and the receipt carries `AuthorityEffect: None`.
