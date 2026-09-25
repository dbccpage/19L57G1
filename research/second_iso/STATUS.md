# STATUS: rung four -- the first-demand index up to the implemented isomorphism

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-24.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this rung
ran is recorded in `research/second/MANUAL.md` with its observed failure.

## The question, and where it came from

Rung three's leftover X-3, quoted verbatim in `CLAIM_LEDGER.md` from a
pinned span: the index up to the implemented isomorphism.  Rung three's
own application of the seed's next-rung rule, pinned as a second span,
selects it, because it extends the census of challenge five -- a second
reading of the row for succession, bearing on the row for symmetry -- and
because no leftover reduces the count of declared inputs.

`research/second/PLAN.md` item five assigns "run forward" and the census
to rungs four and five.  As in rung three, this rung follows the seed's
rule, which the plan's item six defers to, and not the list; the plan is
not edited.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note per file, as `PROMPT.md` declared before
any Lean was built.  Four reconstruction modules reproduce seven pinned
sources verbatim: the sealed kernel slice (`Kernel.lean`, from `Basic.lean`
and `Inertia.lean`), the sealed isomorphism structure and the transport of
collapse across it (`IsoKernel.lean`, from `Minimality.lean` and the parked
`IsoCollapse.lean`), the track-one sibling's stake and demand slice
(`Inherited.lean`), and rung three's prefix reading and first count
(`IndexSlice.lean`).  `test_reconstruction.py` compares them declaration by
declaration with the pinned blobs AT THE SNAPSHOT: 73 shared declarations,
all identical after comments, namespace and `open` lines are stripped and
whitespace is normalized; the omitted declarations are pinned by name.

`Kernel.lean` was produced from rung three's `Kernel.lean` by changing
only the outer namespace; that file is itself the verbatim sealed slice,
and the comparison above is against the SEALED blobs, not rung three's
copy.  The Python consumes the sealed kernel, the sealed isomorphism
procedure, the track-one sibling and rung three through their public
functions and copies no source of any of them.  The verifiers, the
coverage gate and three test files are hand copies of rung three's with
this rung's paths, each saying so in its first lines.

## What is proved, what is computed, what is open

**Proved in Lean** (84 theorems in the package, 35 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
four with none, thirty-four with `propext` alone, forty-six with both --
and no `Classical.choice` anywhere):

- separability transports across the sealed isomorphism in both
  directions, by carrying the witnessing context, with no decision of
  collapse;
- a demand is carried to a demand across any isomorphism that preserves
  the stake's labels; under a UNIFORM stake carrying a demand is invariant
  under the isomorphism, at every pair of regimes it relates;
- under a uniform stake, class-matched histories from any two bases have
  the same first counts;
- renaming the token every supply carries moves no first count;
- three countermodels for the stakes that are not uniform, closed by
  kernel computation through Boolean checks proved SOUND, with no
  converse proved: two isomorphic regimes, one carrying a demand and one none,
  under `parity` and `chain` at three data and under `residueThree` at
  four; two class-matched histories of eight events with first counts
  eight and none, under `parity` and `chain` alike; and two of eleven
  events with first counts eleven and none, under `residueThree`.

**Computed** over rung three's rectangle -- three bases, seven stakes,
18798 sequences, 2316 distinct regimes in 402 classes:

- the sealed key procedure and the brute-force minimum give one
  partition; the sealed automorphism list and a brute-force count agree at
  every regime, with sizes from one to two hundred and forty;
- under the four uniform-labelled stakes no class is split, reached or
  over 6128 presentations; under `parity`, `chain` and `residue_three`,
  47, 61 and 13 classes are split, the same counts both ways;
- 4368 trajectory classes, 3042 with more than one member: the first
  count is constant on every one, under every stake -- inside a bound of
  four events, which the Lean countermodels at eight and eleven exceed;
- quotiented by the class of the final regime, the first count varies on
  19 classes under each of five stakes, 226 under `total_same`, none
  under the free stake;
- the declared token renaming changes 7849 presentations and moves no
  count and no class.

**Open, named and priced** (Y-1 to Y-4 below, and rung three's X-1, X-2,
X-4, X-5 and X-6 carried unchanged, less the symmetry row this rung
decides).

## The frozen predictions, scored

Nine computational rows, scored mechanically by `run_iso_index.py` and
recorded in `receipts/iso_index.json`:

| row | value | verdict |
|---|---|---|
| J-10 | 577, 3928, 14293 sequences; 0 replay mismatches | HIT |
| J-11 | 0 key disagreements; 402 classes of 2316 regimes | HIT |
| J-12 | 0 automorphism disagreements; smallest 1, largest **240** (predicted 24) | **MISSED** |
| J-13 | uniform-labelled stakes: 0 split classes, reached and over presentations | HIT |
| J-14 | parity 47, chain 61, residue_three 13, both ways | HIT |
| J-15 | 0 varying trajectory classes under all seven stakes; 3042 with two members | HIT |
| J-16 | 19, 19, 19, 19, 19, 226 varying final classes; free 0 | HIT |
| J-17 | 0 moved counts, 0 moved classes, 7849 changed presentations | HIT |
| J-18 | the exhibited pairs in one class at every prefix; counts 8, 8, 11 and none | HIT |

**The miss, J-12, recorded next to its value and not edited.**  The
prediction said the largest automorphism group in the rectangle has
twenty-four elements.  It has two hundred and forty, at two regimes: five
data none of which any instance separates, with two forms of one arity.
The prediction was made reasoning from the Lean reading regimes, which
carry an imposed requirement between two data and so break the symmetry
of the data; the sealed Python readings consumed here carry none, and
rung three's receipt said so (`reqs: 0` at both readings) before this
rung froze anything.  A reading of a supplied receipt was available and
not made.

Thirteen rows are scored where their evidence lives and are marked so in
the receipt rather than omitted: J-1, J-2 and J-6 by `verify_lean.py`
and the statement-shape tests of `test_census.py`; J-3, J-4, J-5, J-7,
J-8, J-9 and J-21 by `test_census.py`; J-19 by `run_iso_index.py
--check` and `test_iso_index.py`; J-20 by `verify_lean.py` and the
committed axiom log; J-22 by the measured time below.  Each is met.

### The census prediction, and its seven misses

`PREDICTIONS.md` named 38 Lean targets and a class for each, frozen
before the compile.  All 38 exist.  Scored mechanically by
`test_census.py`: **31 hits, 7 misses**, and **11 further native
declarations** were written that the frozen list did not name.

Every one of the seven misses is a DEMOTION:

| target | predicted | recorded | why |
|---|---|---|---|
| `first_demand_matched_of_uniform` | CONTENT | THIN | the argument moved into the unpredicted `first_demand_transport`; the headline pairs two applications of it |
| `honourCheck_sound` | CONTENT | THIN | a case split dispatching to the two check soundness lemmas |
| `noDemandCheck_sound` | CONTENT | THIN | two list rewrites and one application of `honourCheck_sound` |
| `demandCheck_sound` | CONTENT | THIN | the same shape, with the label read off the check |
| `matched_P` | CONTENT | THIN | a case exhaustion closed by kernel computation, plus one step reducing long counts to the full length |
| `matched_Q` | CONTENT | THIN | the same |
| `separable_of_unary_witness` | THIN | DEFINITION | a given witness whose four side conditions close by unfolding |

**What the misses say.**  The content of this rung sits in four
theorems: `demand_transport`, `first_demand_transport`, `unary_ctx_slots`
and `collapsed_of_unary`.  The rest are transports of sealed lemmas,
corollaries, and countermodels that the soundness lemmas turn into kernel
computation.  The prediction expected the Boolean checks and the matching
proofs to carry content; once the checks were proved sound, they did not.

## Found live, before any injection

**`Classical.choice` twice, from `simp`.**  The first audit of the
package failed with nineteen theorems depending on `Classical.choice`.
Two sources, found by `#print axioms` on isolated probes: `simp` closing
a list-length contradiction in `unary_ctx_slots`, and `simp` proving the
diagonal condition of `chain`.  Both were replaced by choice-free steps
(`simp only [List.length_cons]` then `omega`; `if_neg` with
`Nat.succ_ne_self`), and the audit passed.  The whitelist gate of
`verify_lean.py` therefore fired on a real defect before it was injected,
naming each dependent theorem; the injection record also carries its
deliberate probe.

**A census measurement reads definitions as proof.**  `test_census.py`'s
length reader counts every non-blank line from one theorem to the next,
so a `def` block between them is charged to the theorem above it.  Two
DEFINITION rows first read long for that reason and for no other.  Every
definition of `Countermodel.lean` and `Check.lean` was moved ahead of the
theorems, and one proof was shortened by merging its case split.  No row
was reclassified to pass the bound, and the bound was not raised.

## Leftovers, named and priced, executed nowhere

- **Y-1, the shortest class-matched witnesses.**  Lengths five to seven
  for `parity` and `chain`, five to ten for `residue_three`, are not
  enumerated.  A search over PAIRS of histories whose prefixes stay in
  one class, pruned by nothing proved for another demand kind, would
  settle them.  Price: moderate; the unpruned sequence rectangle at seven
  events is too large to enumerate whole.
- **Y-2, necessity of uniformity.**  Whether a stake that is not uniform
  can make carrying a demand invariant.  The candidate is named in
  `CLAIM_LEDGER.md` row ISO-NECESSITY; its proof needs a decision of
  collapse, which is rung three's X-1.  Price: small once X-1 exists.
- **Y-3, symmetry along a history.**  This rung decides the symmetry
  row as definable at every regime reached.  Whether the size of the
  automorphism group is preserved or monotone along the events of a
  history, and at which event kinds it moves, is not measured.  Price:
  small; the rectangle and the automorphism counts are in place.
- **Y-4, the converse of the checks for regimes of arity one.**  The
  Boolean checks are proved sound, and no converse is proved: a check
  returning false proves nothing.  For regimes whose forms all have
  arity one, the converse is within reach of `unary_ctx_slots`, and would
  be a first piece of X-1.  Price: small.
- Carried from rung three, unchanged: X-1 (a decision for a demand at a
  regime), X-2 (the first count under a generated run), X-4 (the safety
  of rung three's omitted declarations), X-5 (the engine of the seed's
  challenge three), and X-6 less symmetry: two-ness, observational
  classes, duration, adjacency, reach, invariants, irreversibility,
  branching, exhaustion and recurrence.

## Gates and timing

Measured on this machine, 2026-09-24, serially, one run each:

| gate | command | measured |
|---|---|---|
| pins, spans, frozen texts | `python research/second_iso/verify_pins.py` | 1.7 s |
| tests under coverage (148 tests) | `python -m coverage run -m unittest discover -s . -p "test_*.py"` | 36.0 s |
| coverage gate | `python -m coverage json -q; python check_coverage.py` | 0.5 s |
| receipt comparison | `python run_iso_index.py --check` | 2.5 s |
| strict typing | `python -m mypy` | 0.3 s, warm cache |
| clean Lean build and axiom audit | `python verify_lean.py` | 11.2 s |

Grouped measured time **52.2 seconds**, inside the fifteen-minute
per-rung ceiling the seed sets.  The mypy row was measured with a warm
cache and a cold run is longer; the ceiling is what the number is for.
The Lean row is a CLEAN build: `lake clean`, a full rebuild, then the
compiled-environment census.  Coverage over the declared measured set
(`iso_index.py`, `run_iso_index.py`, `verify_pins.py`): **line 99.32%,
branch 97.52%**, both above the 95% floor.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps are run
here, each command directly from its working directory, in the order the
contract lists them.  `python ci/run_gates.py --list` enumerates the four
registered steps of this rung, three in the research job and one in the
lean job.

## Terminal scope

- `DEMAND_INVARIANT_UNDER_UNIFORM_STAKES` -- PROVED_THEOREM, every pair of isomorphic regimes.
- `INDEX_INVARIANT_ALONG_MATCHED_HISTORIES` -- PROVED_THEOREM, uniform stakes, any bases.
- `NON_UNIFORM_STAKES_ESCAPE_BOTH` -- COUNTERMODEL, `parity`, `chain`, `residueThree`.
- `SUPPLY_TOKENS_IRRELEVANT` -- THIN, every stake.
- `UNIFORMITY_NECESSARY` -- OPEN, candidate named.
- `SHORTEST_WITNESS` -- OPEN, lengths five to seven and five to ten.
- `RECTANGLE_MEASURED` -- FINITE_COMPUTATION, the frozen rectangle only.
- `CENSUS_SUCCESSION_READ_AGAIN` -- PROVED_THEOREM with COUNTERMODEL, one row.
- `CENSUS_SYMMETRY_DECIDED` -- FINITE_COMPUTATION, DEFINABLE at every regime reached.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Reconstruct, Transport, Match, Countermodels, Rectangle, Census, Register]
write_root: research/second_iso/
snapshot: bdbe583289fd641e7399d46bf8769d8101efc3cc
sealed_paths_touched: []
shared_files_touched:
  - .github/workflows/verify.yml (append only)
  - research/second/MANUAL.md (append only)
  - research/README.md (generated view)
  - docs/index/pins.md (generated view)
  - docs/lean_build_order.md (generated view)
  - ci/tree_custody_pin.json (generated view)
census_pin_regenerated: false
prompt_sha256: 833fb3b369636d7d166595442520032e2ce8540a6e1ff416968c6fc9e87802ab
predictions_sha256: dffe41d4084b7e5d56b2b5bcc8d34439a53969e5d10f8cb0f7c3225b6d7f2817
bases: [EMPTY, L, F]
stakes: [free, total_apart, total_same, parity, residue_three, chain, one_sided_total]
sequences: {EMPTY: 577, L: 3928, F: 14293}
regimes: {distinct: 2316, classes: 402}
lean_theorems: {total: 84, reconstruction: 35, content: 4, thin: 30, definition: 15}
predictions_scored: {hit: 8, missed: 1, elsewhere: 13}
census_prediction_scored: {named: 38, hit: 31, missed: 7, unpredicted_native: 11}
input_count: {value: 2, proof: none, sentence: "This rung neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: [succession, symmetry]
gate_time_seconds: 52.2
authority_effect: None
final_state: true
```

## The next rung, named so it cannot be smuggled in later

The seed's rule takes the smallest named leftover that EITHER reduces the
count of declared inputs OR extends the census of challenge five, and on
a tie the one named first.  Applied to this rung's leftovers and the ones
carried:

| leftover | reduces the input count | extends the census | price | eligible |
|---|---|---|---|---|
| Y-1 shortest witnesses | no | yes, succession | moderate | yes |
| Y-2 necessity of uniformity | no | no | small, after X-1 | no |
| Y-3 symmetry along a history | no | yes, symmetry, invariants, irreversibility | small | yes |
| Y-4 converse of the checks at arity one | no | no | small | no |
| X-1 decision procedure | no | no | moderate | no |
| X-2 count under a generated run | no | not until X-5 exists | a rung | no |
| X-4 safety of the omissions | no | no | small | no |
| X-5 the engine | no | no | not priced | no |
| X-6 the ten undecided rows | no | yes | large | yes |

Three are eligible and Y-3 is the smallest, so there is no tie to break:
the next rung is **Y-3, symmetry along a history** -- whether the size of
the automorphism group is preserved or monotone along the events of a
history, and at which kinds it moves, which bears on the rows for
invariants and irreversibility as well as symmetry.

As rung three recorded, X-1 is the leftover the others keep waiting on;
it is not eligible on the plain reading of the rule, and it is recorded
here again rather than taken.  Nothing of any leftover is started here.
