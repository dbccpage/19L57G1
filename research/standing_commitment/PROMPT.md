# standing_commitment — the native run charter

`AuthorityEffect: None.`

## The question

Direct author instruction, 2026-09-03: *build the standing-commitment rung —
demands as a consequence of growth.*

The estate's first standing obstruction, pinned as a span in
`SOURCE_MANIFEST.json`, records that no object-language endogenous demand
generator was derived, and that the fixed-radius, fixed-finite-alphabet
local-strategy class was later excluded outright. So the machine has a
dynamics and no source of work.

This rung asks a narrower question the exclusion does not cover. A local
strategy looks at a state and *emits* a next demand. A **standing
commitment** does not: it is a condition declared once, saying which pairs
must be kept apart whenever both are held, and it emits nothing. The
question is whether a state that GROWS under such a condition thereby
acquires demands that were not there before, with no act between the growth
and the demand.

## Write root and seal

Write root: `research/standing_commitment/` only. Sealed and frozen:
`prompt/`, `paper/`, `code/`, `lean4/Derivation/`, `artifacts/`,
`CLAUDE.md`, `ci/`, `.github/`, root `tests/`, `pyproject.toml`,
`requirements.txt`, every sibling research tree, and the census pin
`ci/prose_watchlist.json`. Snapshot
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`; every pull request
targets `main` directly.

## Carrier

The represented state and its decidable observation semantics,
reconstructed verbatim in `lean/StandingCommitment/Base.lean` from
`lean4/Derivation/Represented.lean` and checked against the pinned source by
`verify_pins.py`. The repair, augmentation, and gate machinery is
deliberately NOT reconstructed: this rung asks where demands come from, not
how they are discharged.

## Refusals in force

`FW-SEAL` no path outside the write root is written.
`FW-NAME` no outside theory, programme, or person name.
`FW-OB1` **this rung does not close the standing obstruction.** The
commitment is a parameter of every theorem; nothing here produces one. Any
sentence claiming otherwise fails the run.
`FW-SCOPE` every computed number carries its run length; a budget that
clears a short run is not claimed to clear a longer one.
`FW-SET` the declared family of commitments is four members plus one
post-freeze addition, and is not the set of commitments.
`FW-BILL` a green test discharges nothing by itself.
`FW-PIN` the census pin is not regenerated.

## Terminals, pre-agreed

`GROWTH_GENERATES`, `GROWTH_GENERATES_NOTHING`, `OPEN_AT_NAMED_TARGET` for
the Lean half; `RACE_TABULATED` and `REGULARITY_REFUTED` or
`REGULARITY_UNREFUTED` for the computational half. Both branches of each
pair were written here before the corresponding work ran.

## Evidence classes

Exactly one per substantive line: DEFINITION, DECLARED_POLICY,
PROVED_THEOREM, CONDITIONAL_THEOREM, FINITE_COMPUTATION, COUNTERMODEL,
CONJECTURE, OPEN, REFUSED, METATHEORY, PREDICTION.
