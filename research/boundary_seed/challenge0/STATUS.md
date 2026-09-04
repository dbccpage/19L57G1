# Challenge 0 — status

`AuthorityEffect: None`.  Session of 2026-09-04, branch
`research/boundary-seed`, opened from main at `9b9bea87`.

## Order of the work, as committed

1. `de6c2f9f` seed commit: `SEED.md` sha256 `ba30bcd6…` and `.gitattributes`.
2. `0fe87837` `PLAN.md` and `MANUAL.md`, before substantive work.
3. `61faafba` `challenge0/PREDICTIONS.md` frozen, sha256
   `a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395`,
   before any code or proof.
4. This commit: kernel, Lean, tests, receipt, paper, ledger, change log,
   registration, injections.

## Results

Inscription `<|>`, no object-language operation.  Receipt
`receipts/challenge0.json`; the full tables are in `paper.md` section 4.

| | reading U | reading O |
|---|---|---|
| sides collapsed at genesis | yes (PROVED) | no; the difference is the two admitted names only (DEFINITION) |
| supply changes state | never (PROVED) | never (PROVED) |
| an event follows from the state | no kernel function returns an event (COMPUTED census) | same |
| observation fires at genesis | none (PROVED) | none (PROVED) |
| the reflection | permitted renaming; involution; fixes genesis (PROVED) | not a permitted renaming (DEFINITION); moves any placed mark (PROVED) |
| classes for n = 0..4 marks | 1, 1, 2, 2, 3 | 1, 2, 3, 4, 5 |

## Predictions scored

| id | label | status |
|---|---|---|
| C0-1 | FORCED | HIT |
| C0-2 | FORCED, DEFINITION-level | HIT |
| C0-3 | FORCED | HIT |
| C0-4 | NOT FORCED, DEFINITION-level | HIT |
| C0-5 | FORCED for genesis | HIT; general clause SHARPENED (true and too narrow: the reflection fixes a placement up to mark renaming exactly when the counts on the two sides are equal, computed to four marks) |
| C0-X | NOT FORCED | PENDING, scored by Challenge 1 |

Five of five scored predictions hit, and every one was labelled FORCED
or DEFINITION-level in advance.  That is evidence that the order of the
work was kept, not that anything was learned; the one that could have
gone otherwise, C0-4, turned on a choice the seed had already made.

## Where the run reached for a remembered result (declared reading 0)

- The kernel's shape: a frozen regime, an inert supply event, replay and
  certification from genesis, a brute-force minimum over renamings as
  the isomorphism key with tokens forgotten.  The seed's section 7
  prescribes replay, an implemented isomorphism relation, and a bound on
  enumeration; the particular shape those took here is the shape the
  instrument remembers from the sealed derivation, and it was written
  from memory rather than re-derived.  Recorded, not repaired: the shape
  is apparatus, and the seed permits any implementation that meets its
  section 7.
- The convention that re-admission of an admitted token is a designation
  and not a duplication.  A remembered discipline (the repository
  contract lists designation among the things never conflated), applied
  here as a declared convention in the kernel's docstring.
- The prediction that no negative observation would be admitted (C0-4)
  is the instrument's memory of how such a state was handled before.
  It was written as NOT FORCED for exactly that reason.
- Nothing in the reflection census or the class counts was remembered;
  those were computed here first.

## Leftovers, for Challenge 1 and later

- Score C0-X under Challenge 1's admission grammar.
- The equal-count law and the class-count closed forms are computations
  to four marks.  A Lean statement for all placements is a candidate
  target, not yet attempted.
- Whether the O-names ever earn their keep: nothing at Challenge 0 gives
  the O-distinction content beyond the declaration.
- A mark has no observable of its own at Challenge 0 beyond its side.
  Challenge 1 must say what a mark's profile is, if anything.

## Repairs during the challenge

Recorded in `change_log.md`: the Lean constructor name that tripped the
forbidden-token scan (live gate failure, renamed to `place`); the census
comparison that kept tokens (caught by `test_census_rows`); the Lean
verifier's report parser.

## Gates run in this session

| gate | result |
|---|---|
| `verify_pins.py` | pins ok: seed and one frozen prediction file |
| `unittest discover -s tests` | 37 tests OK, blindness scan included |
| `mypy` (strict, tree pyproject) | no issues in 10 source files |
| `coverage` + `check_coverage.py` | line 98.09%, branch 95.83% over 3 files |
| `run_challenge0.py` | receipt byte-identical on rerun |
| `verify_lean.py` | 13 axiom reports within {propext, Quot.sound}, matching `lean/axioms.txt` |
| `ci/check_prose_watchlist.py` | clean, census matches its pin, no regeneration |
| `tests/test_primitive_contact.py` | firewall passes |
| injections | five gates, each failed by name and recovered (`MANUAL.md`) |

## Next session

Open Challenge 1 fresh: read the handoff, the seed, `PLAN.md`,
`MANUAL.md`, and this file; write and commit
`challenge1/PREDICTIONS.md` with its own extrapolation before any code;
declare the admission grammar for the supply of `<a|>`; score C0-X.
