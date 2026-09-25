# STATUS: rung eight -- the element count across the isomorphism

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-25.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this rung
ran is recorded in `research/second/MANUAL.md` with its observed failure.

## The question, and where it came from

Rung five's leftover Z-1, quoted verbatim in `CLAIM_LEDGER.md` from a
pinned span: the element count across the isomorphism.  Rung seven's own
application of the seed's next-rung rule, pinned as a second span,
selects it, because it extends the census of challenge five -- the row
for recurrence, and irreversibility up to the isomorphism -- it is the
smaller of the two eligible leftovers, and no leftover reduces the count
of declared inputs.

`research/second/PLAN.md` item five assigns "run forward" and the census
to rungs four and five.  As in rungs three to seven, this rung follows the
seed's rule, which the plan's item six defers to, and not the list; the
plan is not edited.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note per file, as rungs three to seven did.
Two reconstruction modules reproduce three pinned sealed sources
verbatim: the sealed kernel slice (`Kernel.lean`, from `Basic.lean` and
`Inertia.lean`) and the sealed isomorphism structure (`IsoKernel.lean`,
from `Minimality.lean` lines 169-224).  `test_reconstruction.py` compares
them declaration by declaration with the pinned blobs AT THE SNAPSHOT: 41
shared declarations, all identical after comments and namespace lines
are stripped and whitespace is normalized; the omitted declarations are
pinned by name.

`Kernel.lean` was produced from rung seven's `Kernel.lean`, and
`IsoKernel.lean` from rung five's, by changing only the outer namespace;
the comparison above is against the SEALED blobs, not those copies.
Seven lemmas of this package repeat, as statements, lemmas of rungs five,
six and seven (named in `CLAIM_LEDGER.md` CLS-3 and CLS-9); they are
proved again here so that the package imports nothing, and the ledger and
the census note credit them.  The Python consumes the sealed kernel, the
sealed genesis readings, rung three's bases and rung four's population,
keys and partition comparison through their public functions and copies
no source of any of them.  The verifiers, the coverage gate and four test
files are hand copies of rung seven's (the reconstruction test of rung
five's) with this rung's paths, each saying so in its first lines.

## What is proved, what is computed, what is open

The FIVE COMPONENT COUNTS of a regime are its data, forms, instances,
uniform rules and requirements; the element count is their sum.  A
regime is CLEAN when it is well formed in the sealed sense and none of
its lists of instances, rules and requirements holds an entry twice.

**Proved in Lean** (58 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
three with none, eighteen with `propext` alone, thirty-seven with both --
and no `Classical.choice` anywhere):

- every inhabitant of the sealed isomorphism keeps the number of data
  and the number of forms, with no hypothesis on either regime;
- from a well-formed source, a list of instances, rules or requirements
  without a repeated entry is no longer than the target's; so two clean
  regimes the structure relates have all five counts equal, and one
  element count;
- every event the sealed step accepts keeps a regime clean, and the
  sealed empty regime and the two sealed reading regimes are clean;
- from a clean base: after a changing event no class left is reached
  again; a regime isomorphic to one reached earlier on the same history
  is that very regime, and the events between change nothing; two
  histories reaching isomorphic regimes have one CHANGING count, one
  number of growths and one number of rest rounds.

**Countermodels in Lean**, each by kernel computation:

- for each of the instances, the rules and the requirements, a pair of
  isomorphic regimes breaking duplicate-freedom alone, and a pair
  breaking well-formedness alone, with different lengths of that list;
- across two bases the count is carried by neither the class nor the
  regime: the empty history from the Lean reading regime `R2L`, and two
  data and the requirement between them from the empty regime, reach one
  regime with CHANGING counts zero and three.

**Computed** over rung three's rectangle -- three bases, 18798
sequences, 2316 distinct regimes, 402 classes:

- no class carries two values of any component count, within a base or
  over all three; the key and brute-force partitions agree everywhere;
- no sequence returns to a class; 339, 1597 and 4790 sequences recur at
  EMPTY, L and F, exactly those holding an event that changes nothing,
  and all 454, 1921 and 5583 recurrences are stutters, reached by
  supplies and by repeated instances, rules and requirements, never by a
  datum or a form;
- 86 classes are reached at more than one base, 5 at all three, and all
  86 carry two CHANGING counts.

**Open, named and priced** (U-1 and U-2 below, and the leftovers carried
from rungs three to seven).  Recurrence and no-return from an UNCLEAN
base are not decided (U-1).

## Superseded, dated 2026-09-25, and left standing

No earlier receipt is revised.  Three OPEN statements of earlier rungs
are closed here for clean bases, which every base the run declares is.
Each is quoted and stands as written at its rung:

- rung five, SYM-14: "That two regimes the sealed isomorphism relates
  have one element count is NOT proved here; no theorem statement of this
  package mentions both an isomorphism and the element count."  Closed
  for clean regimes by `size_iso`, and refused for unclean ones by the
  six countermodels.
- rung six, CENSUS-succession: "Up to the implemented isomorphism: a
  finite computation on the rectangle (SUC-17) and OPEN beyond it, behind
  rung five's Z-1."  Closed for clean bases by `counts_of_class`.
- rung seven, CENSUS-duration: "Up to the implemented isomorphism: the
  envelope is not a class invariant on the rectangle (DUR-17), and
  whether the sum is is OPEN beyond it, behind rung five's Z-1."  The
  sum is closed for clean bases by `counts_of_class`; the envelope
  sentence stands.

## The frozen predictions, scored

Five computational rows, scored mechanically by `run_class.py` and
recorded in `receipts/class_count.json`:

| row | value | verdict |
|---|---|---|
| P-9 | 577, 3928, 14293 sequences; 75, 523, 1718 regimes; 0 replay mismatches; 54, 174, 265 classes within base; 402 over 2316 regimes; 0 key and brute-force disagreements | HIT |
| P-10 | 0 classes with two component tuples, within any base and over all three | HIT |
| P-11 | 0 returns and 0 mismatches at each base; stutters by supply, instance, rule and requirement at each base, never by a datum or a form | HIT |
| P-12 | 86 classes at more than one base, inside 46 to 91; 86 of them with two CHANGING counts | HIT |
| P-13 | the six hypothesis countermodels hold in the Python grammar; `counts_not_of_class` does NOT: its two sides lie in two classes | **MISSED** |

Eleven rows are scored where their evidence lives and are marked so in
the receipt rather than omitted: P-1 to P-7 by the statement-shape tests
of `test_census.py` and by `verify_lean.py`; P-8 by the committed axiom
log; P-14 and P-15 by `CLAIM_LEDGER.md` and `test_census.py`; P-16 by
`run_class.py --check`, `test_class.py` and the measured time below.
Each is met.

**The miss, P-13, recorded next to its value and not edited.**  The
prediction wrote the Lean countermodel of P-7 into the Python grammar
and said its two sides reach one class with CHANGING counts zero and
three.  The counts are zero and three; the classes are two.  The sealed
Lean reading regime `R2L` is the regime of challenge three, after the
requirement between the two data is imposed; the sealed Python genesis
history of L, which rung three takes as the base, stops before that
requirement.  The prediction reasoned from the Lean regime while the
Python base, whose receipt was on `main`, differs from it: the same
defect rung four's handoff recorded for its J-12, met again.  The rung
seven predictions had even written down that the Python reading regimes
carry no requirement.  Recorded beside the miss, and not scored: written
for the Python readings, the empty history from L and two data from the
empty regime reach one class with counts zero and two
(`python_reading_witness`).

**A hit whose stated reason was wrong.**  P-12 is a hit on its
falsifier.  Its text named the class of L as reached from EMPTY by three
events, which is the Lean reading; in the Python rectangle that class is
reached by two.  Recorded in `CLAIM_LEDGER.md` CLS-PREDICTIONS.

### The census prediction

`PREDICTIONS.md` named 40 Lean targets and a class for each, frozen
before the compile.  All 40 exist.  Scored mechanically by
`test_census.py`: **40 hits, 0 misses, one unpredicted native theorem**,
`range_nodup` (THIN), added when the first compile found that the
library's own statement of it reaches `Classical.choice`.  One DEFINITION
row, `sortPair_map`, is longer than the line bound; it is pure case
exhaustion and is listed in `long_but_definitional` with the reason.

## Found live, before any injection

**Library lemmas that reach `Classical.choice`.**  The first complete
build passed, and its axiom reports named `Classical.choice` for fifteen
theorems.  The root was one lemma of this package,
`length_le_of_nodup_sub`, which had used the library's lemmas on removing
one entry of a list and on the length after it; `data_le` and `forms_le`
reached it again through the library's statement that the admitted range
holds no index twice.  All three library lemmas report `Classical.choice`
under `#print axioms`.  The removal was redone by hand inside the proof,
and `range_nodup` proved natively; the library's own counting lemma,
which the obvious proof would call, opens a classical section and was
never used.  The frozen prediction P-8 had named that one lemma and not
the other three.

**A shell heredoc altered a generator script again.**  As rung seven
recorded, a script passed through a Bash heredoc lost its escapes; two
generator scripts of this rung were rewritten as files in the scratchpad
and run from there.  One of them had already patched only half of what
it was meant to, and its assertion refused the edit before anything was
injected.

## Leftovers, named and priced, executed nowhere

- **U-1, recurrence and no-return from an unclean base.**  Every base the
  run declares is clean, and cleanness is kept; whether a history from a
  base with a repeated entry or an ill-formed entry can return to a class
  it left is not decided, and the six countermodels show the element
  count is no guide there.  Price: small.  It refines the recurrence row
  this rung decides and extends no row of the census.
- **U-2, the recurrence equivalence in Lean.**  That a history from a
  clean base recurs exactly when it holds an unchanging event.  One
  direction is `recurrence_is_stutter` with a count; the other needs the
  identity inhabitant of the sealed structure on a clean regime.  Price:
  small.  It refines the recurrence row and extends no row of the census.
- Carried from rung seven, with V-3 narrowed: V-1, V-2, and V-3 less its
  sum part, which is now proved for clean bases -- the multiset of
  envelopes of a class stays open.
- Carried from rung six, unchanged: W-2 and W-3.
- Carried from rung five, unchanged: Z-2, Z-3 and Z-5.  Z-1 is this rung.
- Carried from rung four, unchanged: Y-1, Y-2, Y-4.
- Carried from rung three, unchanged: X-1, X-2, X-4, X-5, and X-6 less
  symmetry, invariants, irreversibility, succession, duration and
  recurrence: two-ness, observational classes, adjacency, reach,
  branching and exhaustion.

## Gates and timing

Measured on this machine, 2026-09-25, by `python ci/run_gates.py --step
"rung 8" --keep-going` at `7162abae`, which ran the four registered steps
of this rung in the workflow's order:

| gate | command | measured |
|---|---|---|
| clean Lean build and axiom audit | `python3 research/second_class/verify_lean.py` | 51.3 s |
| pins, spans, frozen texts | `python research/second_class/verify_pins.py` | 6.3 s |
| tests under coverage (147 tests), coverage gate, receipt comparison | the rung's replay, tests and coverage step | 172.7 s |
| strict typing | `python -m mypy` | 1.2 s |

Grouped measured time **231.5 seconds**, inside the fifteen-minute
per-rung ceiling the seed sets.  Most of the test step is the pin
battery, which re-reads twenty-three pinned blobs once per test.  The
Lean row is a CLEAN build: `lake clean`, a full rebuild, then the
compiled-environment census.  Coverage over the declared measured set
(`class_count.py`, `run_class.py`, `verify_pins.py`): **line 98.92%,
branch 95.68%**, both above the 95% floor.  The runner reported that the
interpreter's pytest (9.1.1) differs from the pin in `requirements.txt`
(9.0.3); this rung's tests run under `unittest` and do not import pytest.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps were run
here by the repository's own runner.  The estate custody census, run on
the clean worktree when its pin was rewritten, reports 105 verifiers,
104 green and one pinned red that this rung did not add.

## Terminal scope

- `FIVE_COUNTS_ACROSS_THE_ISOMORPHISM` -- PROVED_THEOREM for data and forms with no hypothesis, and for all five between clean regimes.
- `HYPOTHESES_NECESSARY` -- COUNTERMODEL, six pairs, one hypothesis broken in each.
- `CLEAN_IS_KEPT` -- PROVED_THEOREM, every event of the sealed step; the three sealed bases are clean.
- `NO_RETURN_TO_A_CLASS` -- PROVED_THEOREM, every history from a clean base.
- `RECURRENCE_IS_STUTTER` -- PROVED_THEOREM, every history from a clean base; the equivalence with an unchanging event a FINITE_COMPUTATION in the rectangle (U-2).
- `COUNTS_OF_THE_CLASS` -- PROVED_THEOREM within one clean base; COUNTERMODEL across bases.
- `UNCLEAN_BASES` -- OPEN (U-1).
- `CENSUS_RECURRENCE` -- one row decided, conditional on an engine for FORCED; irreversibility, succession and duration extended to the class.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Reconstruct, Count, Clean, Recur, Counter, Rectangle, Census, Register]
write_root: research/second_class/
snapshot: 35e680ec35dfffb8a108ac88783645880eaabaf9
sealed_paths_touched: []
shared_files_touched:
  - .github/workflows/verify.yml (append only)
  - .claude/skills/gates/SKILL.md (append only, by the author's ruling of 2026-09-25)
  - research/second/MANUAL.md (append only)
  - research/README.md (generated view)
  - docs/index/pins.md (generated view)
  - docs/lean_build_order.md (generated view)
  - ci/tree_custody_pin.json (generated view)
census_pin_regenerated: false
prompt_sha256: 16b57c49057359fc931e35f4ec75441b9d51ece50c76d8a27500f5ec559709c6
predictions_sha256: 75f0dfca01023bcec3bd6da747035966812358eda24b126007aa71095be9ccef
bases: [EMPTY, L, F]
sequences: {EMPTY: 577, L: 3928, F: 14293}
regimes: {EMPTY: 75, L: 523, F: 1718}
classes: {EMPTY: 54, L: 174, F: 265, all: 402}
lean_theorems: {total: 58, reconstruction: 17, content: 5, thin: 22, definition: 14}
predictions_scored: {hit: 4, missed: 1, elsewhere: 11}
census_prediction_scored: {named: 40, hit: 40, missed: 0, unpredicted_native: 1}
input_count: {value: 2, proof: none, sentence: "This rung neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: [recurrence]
census_rows_extended: [irreversibility, succession, duration]
authority_effect: None
final_state: true
```

## The next rung, named so it cannot be smuggled in later

The seed's rule takes the smallest named leftover that EITHER reduces the
count of declared inputs OR extends the census of challenge five, and on
a tie the one named first -- first in the list below, by the author's
ruling of 2026-09-25.  A leftover refining a decided row is not eligible,
as rungs six and seven read it.

| leftover | reduces the input count | extends the census | price | eligible |
|---|---|---|---|---|
| U-1 recurrence from an unclean base | no | no, the recurrence row is decided | small | no |
| U-2 the recurrence equivalence in Lean | no | no, the recurrence row is decided | small | no |
| V-1 attainment of the envelope | no | no, the duration row is decided | moderate | no |
| V-2 duration under an engine | no | not until X-5 exists | a rung | no |
| V-3 the multiset of envelopes of a class | no | no, the duration row is decided | moderate | no |
| W-2 the full set of counts | no | no, the succession row is decided | small | no |
| W-3 succession under an engine | no | not until X-5 exists | a rung | no |
| Z-2 numeric fixer law in Lean | no | no | large | no |
| Z-3 multiplication laws in Lean | no | no | large | no |
| Z-5 automorphisms along a generated run | no | not until X-5 exists | a rung | no |
| Y-1 shortest witnesses | no | no, the succession row is decided | moderate | no |
| Y-2 necessity of uniformity | no | no | small, after X-1 | no |
| Y-4 converse of the checks at arity one | no | no | small | no |
| X-1 decision procedure | no | no | moderate | no |
| X-2 count under a generated run | no | not until X-5 exists | a rung | no |
| X-4 safety of the omissions | no | no | small | no |
| X-5 the engine | no | no | not priced | no |
| X-6 the undecided rows | no | yes | large | yes |

One leftover is eligible, so the next rung is **X-6, the undecided rows
of the census** -- two-ness, observational classes, adjacency, reach,
branching and exhaustion, in the order rung three named them.

**A reading left for the author, recorded rather than made.**  X-6 is
one named leftover carrying six rows.  The seed's rule selects the
leftover; it does not say whether a rung taking it must decide all six
rows, or may decide some and name the rest as leftovers, nor which row
comes first.  Rungs four to seven each decided one to three rows of
their own leftover's reach.  This rung does not choose; the rung that
takes X-6 records the reading it applies, before its predictions are
frozen.

As rungs three to seven recorded, X-1 is the leftover the others keep
waiting on; it is not eligible on the plain reading of the rule, and it
is recorded here again rather than taken.  Nothing of any leftover is
started here.
