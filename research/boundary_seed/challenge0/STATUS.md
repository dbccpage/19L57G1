# Challenge 0 — repaired status

`AuthorityEffect: None`.  Session of 2026-09-04, branch
`research/boundary-seed`, opened from main at `9b9bea87`.

## Order of the work, as committed

1. `de6c2f9f` seed commit: `SEED.md` sha256 `ba30bcd6…` and `.gitattributes`.
2. `0fe87837` `PLAN.md` and `MANUAL.md`, before substantive work.
3. `61faafba` `challenge0/PREDICTIONS.md` frozen, sha256
   `a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395`,
   before the branch's first code-or-proof commit.
4. `2d1353bd`: initial kernel, Lean, tests, receipt, paper, ledger, change
   log, registration, and injections.
5. Exact-head review repair: model/claim/gate corrections listed below.

This history proves “committed before” only.  It cannot prove when any
untracked or off-tree code or proof was written.

## Provenance ceiling

The instrument had reviewed the sealed derivation and research trees before
drafting the seed and declared that remembered structure influenced this
run.  The surviving status is
`SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE`.  It is not a blind,
clean-room, convergence, or independent-discovery receipt.

## Results

Inscription `<|>`, no object-language operation.  Receipt
`receipts/challenge0.json`; the full tables are in `paper.md` section 4.

| | reading U | reading O |
|---|---|---|
| initial opaque datum | present (PROVED) | present (PROVED) |
| sides collapsed at genesis | yes (PROVED) | no; the difference is the two admitted names only (DEFINITION) |
| supply changes state | never (PROVED) | never (PROVED) |
| an event follows from the state | none in the declared empty relation (PROVED) | same |
| mark-on-side judgment at genesis | none (PROVED) | none (PROVED) |
| side-name judgment at genesis | none (PROVED) | `near` and `far` (PROVED from the declaration) |
| the reflection | permitted operation; automorphism at genesis; involution | fixes genesis as raw data but is not permitted; moves any placed mark |
| classes for n = 0..4 marks | 1, 1, 2, 2, 3 | 1, 2, 3, 4, 5 |

Boundary dependence: the supplied opaque datum, supply inertia, and the
empty event-follows relation do not require the admitted boundary.  Every
side, placement, name, profile, reflection, collapse, and class-count result
does require it and is not formulated after removing it.  This is a
dependency classification, not a silently added third reading.

## Predictions scored

| id | label | status |
|---|---|---|
| C0-1 | FORCED | HIT |
| C0-2 | FORCED, DEFINITION-level | HIT |
| C0-3 | FORCED | HIT |
| C0-4 | NOT FORCED | PARTIAL; emptiness target supported, but “no observation fires” is false under O |
| C0-5 | FORCED for genesis | HIT; within n = 0..4 the general U clause is SHARPENED by the equal-count computation |
| C0-X | NOT FORCED | PENDING, scored by Challenge 1 |

Four of five scored predictions hit.  C0-4 was explicitly NOT FORCED and is
PARTIAL: the closed grammar has no emptiness judgment, but its frozen
“no observation fires” rationale is false because O has two name judgments.
The four HIT predictions were labelled FORCED in advance.  The commit topology
shows only that the frozen file was committed before the branch committed
code or proofs.  It is not evidence of insight or blind independence.

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
- The canonical key has no unbounded completeness or injectivity theorem.
- Whether the O-names ever earn their keep: nothing at Challenge 0 gives
  the O-distinction content beyond the declaration.
- A mark has no observable of its own at Challenge 0 beyond its side.
  Challenge 1 must say what a mark's profile is, if anything.
- The future freeze instruction is self-referential if `FREEZE.md` must hash
  itself.  A working or staged marker does not retire the scan, while the
  current committed-marker rule does not validate the manifest's semantics.
  A parent-tree or explicit-exclusion protocol remains OPEN before comparison.

## Repairs during the challenge

Recorded in `change_log.md`: the original three author repairs and the
exact-head review repair.  Review restored the supplied opaque datum,
closed the observation and event-follows grammars, corrected O-reflection
automorphism semantics and bounded scoring, validated regime and supply
invariants, hardened byte/history/source-isolation gates, and corrected the
coverage arithmetic and provenance claims.

## Gates run in this session

| gate | result |
|---|---|
| `verify_pins.py` | commit-aware gate; rechecked at the repair commit |
| `unittest discover -s tests` | 53 passed |
| `mypy` (strict, tree pyproject) | no issues in 11 source files |
| `coverage` + `check_coverage.py` | line 100.00%, branch 100.00%, 3 measured files |
| `run_challenge0.py` | receipt byte-identical on rerun |
| `verify_lean.py` | 20 axiom reports within {propext, Quot.sound}, matching `lean/axioms.txt` |
| `ci/check_prose_watchlist.py` | clean, census matches its pin, no regeneration |
| `tests/test_primitive_contact.py` | firewall passes |
| adversaries and injections | original injections plus review-repair probes (`MANUAL.md`) |

## Next session

Open Challenge 1 fresh: read the handoff, the seed, `PLAN.md`,
`MANUAL.md`, and this file; write and commit
`challenge1/PREDICTIONS.md` with its own extrapolation before any code;
declare the admission grammar for the supply of `<a|>`; score C0-X.
