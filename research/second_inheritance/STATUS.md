# second_inheritance: rung zero, replay the inheritance

`AuthorityEffect: None`.  This rung records; it does not certify.

Challenge zero of `research/second/SEED.md`.  Before the second
derivation asks anything, it replays what it inherits, censuses the
declared inputs it starts from, and shows that the inheritance alone
does nothing.  The question is `PROMPT.md`; the predictions were frozen
before the first run in `PREDICTIONS.md`; every result is in
`receipts/inheritance.json`, which regenerates byte-identically.

## Frozen inputs

- Seed `research/second/SEED.md` sha256
  `52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e`.
- `PROMPT.md` sha256
  `aa804ee3eaab8b358ff347036fce8810f41f431fd68390c18d709775fd5a1447`.
- `PREDICTIONS.md` sha256
  `86767fe4d8b2ed73ec516855d6d78d3310c22ca6815c835ea4b46060c026ab3a`,
  written and hashed before the first computation, scored mechanically
  by `run_inheritance.py`, never edited.
- Sources pinned as Git blobs at snapshot
  `7dabce4e8f8b22c3841511b1414d879dff3d7a65` in `SOURCE_MANIFEST.json`:
  the sealed kernel and runner, the sibling dual's engine and runner, the
  three committed artifacts replayed here, and the sibling's committed
  summary.  `verify_pins.py` checks them at HEAD, checks the frozen texts,
  and checks the absent-at-snapshot record at the snapshot, not at HEAD.
- Declared bounds: the sealed grammar (two items, arity two); at most
  five admitted data and at most eight supplies for the inertia
  computation; the sealed closed baselines rebuilt under their own
  parameters (fifteen rounds, guard of twelve hundred, measure mu1).

## Declared readings

1. The seed's author and this rung's session coincide (recorded in
   `research/second/MANUAL.md`).  Rung zero is replay and census; no
   prediction here could be steered by knowing the answer, since every
   value is a regeneration of committed bytes or a count read off pinned
   source.
2. Two trees the seed names, `standing_commitment` (pull request 127)
   and `two_sided_commitment` (pull request 128), are absent from `main`
   at the snapshot.  Their replay is OPEN, and the stake and the growth
   policy they introduce carry OPEN custody here.  Nothing was pinned
   from a commit that is not an ancestor of HEAD.

## Terminals, each with its scope

- INHERITANCE_REPLAYS (FINITE_COMPUTATION).  The sealed challenge
  reports regenerate byte for byte from the sealed kernel
  (`artifacts/challenges.json`).  Both sealed closed baselines rebuild
  from the sealed engine and match their committed summaries on every
  field, including the sha256 of the full DAG export: reading L, 4 nodes
  with 3 terminal; reading F, 20 nodes with 16 terminal.  The sibling
  dual's summary receipt regenerates byte for byte from the sibling's
  own runner.
- INHERITANCE_PARTLY_ABSENT (OPEN).  The two named trees above are not
  at the snapshot; the rung that first has them on `main` replays them.
- DECLARED_INPUTS_CENSUSED (FINITE_COMPUTATION, by introspection).  The
  sealed event grammar has six kinds; exactly one, supply, never changes
  state; the other five are admissions or the external requirement.  The
  sealed engine declares two policies: pair-separation closure and the
  external continuation.  The sibling dual declares three events:
  RequireSame, Retract, Switch.  The seed names two remaining inputs, the
  stake and the stream; the stream's events are sealed and pinned, its
  growth policy and the stake's declaring event are OPEN custody until
  their trees are on `main`.
- INERTIA_AT_THE_SECOND_LEVEL (FINITE_COMPUTATION).  From both sealed
  genesis readings, up to eight supplies leave the regime unchanged.
  Under no declaration and under the all-free stake the demand set is
  empty by definition.  Growing to five data under the all-free stake
  admits no form, answers nothing, and leaves every state totally
  collapsed: reading L, 4 states and 3 growth edges; reading F, 3 states
  and 2 growth edges; a single chain each.  A stream without a stake is
  inert.  The sealed theorems `supply_no_op` and `genesis_underivable`
  are the Lean behind the supply half; the stake half cites the absent
  sibling's `empty_commitment_generates_nothing` as OPEN custody and is
  otherwise a finite computation here.

## Predictions scored (mechanically, in the receipt)

| id | prediction | verdict | what the receipt shows |
|---|---|---|---|
| R0-1 | replay | HIT | challenges byte-identical; both closed baselines match every field; dual summary byte-identical |
| R0-2 | grammar census | HIT | six kinds, one state-preserving; two policies; three dual events; both named trees absent |
| R0-3 | inertia | HIT | supplies inert in both readings; all-free growth is a collapsed chain with no form and no response |

Three of three.  Recorded honestly: these were arithmetically forced
once the definitions were fixed, as the sibling `standing_commitment`
says of its own; they evidence the ordering of the work, not insight.
The one thing this rung establishes that was not certain in advance is
that the inheritance replays exactly at this snapshot.

## What this rung does not claim

- Nothing about the stake or the stream beyond their custody status.
- No theorem of its own: the inertia results are finite computations
  citing sealed Lean for the supply half.
- Nothing about the two absent trees.

## Commands and gate time

From the repository root:

```text
python research/second_inheritance/verify_pins.py
python research/second_inheritance/run_inheritance.py     # about ninety seconds
```

From this directory:

```text
python -m unittest discover -s . -p "test_*.py"     # regenerates the receipt
python -m mypy
```

Gate time for this rung on 2026-09-03: under four minutes of wall time
for the run, the tests, typing, the pin verifier, the identifier
firewall, and the prose watchlist together.

## Leftovers, named and executed nowhere

- Replay `standing_commitment` and `two_sided_commitment` at the first
  snapshot that contains them, and close their custody.
- Challenge one: the stream as a response at a three-item bound.
