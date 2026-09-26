# STATUS: continuation one -- the engine

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-25.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this
attempt ran is recorded in `research/second/MANUAL.md` with its observed
failure.

## The question, and where it came from

The seed's challenge three: declare precisely what an engine is,
enumerate every minimal engine in a declared class formed from the
surviving stakes of challenge two, the two continuation rules already
known and the validity rules of challenge one, count every capability
each engine declares, refuse any engine called one declaration that
bundles several, and retain all tied minima; with the seed's required
questions four and ten, whether a minimal engine exists, is unique up to
isomorphism, and is initial in its class.

It is rung three's leftover X-5, quoted in `CLAIM_LEDGER.md` from two
pinned spans.  Rung ten found the seed's next-rung rule selected nothing
and recorded X-5 for the author.  The author's ruling of 2026-09-25,
recorded verbatim in `research/second/MANUAL.md` and in `CLAUDE.md` and
pinned here as a span, makes X-5 eligible as a named prerequisite of the
census and authorizes at most two further research attempts: first
challenge three, then challenge four.  **This tree is the first.**  It is
a protocol intervention by the author, not a result of the seed's rule;
`SEED.md` is unchanged.  It closes before the second opens.

`research/second/PLAN.md` item four assigns "the engine as a declared
class" to rung three.  As in rungs three to ten, the plan is not edited:
a plan committed before substantive work is not rewritten to match what
happened.

## The readings applied, recorded before the predictions

Every one is written in `PROMPT.md`, frozen at `03b67607` before
anything else in the tree, and binds no later attempt.

- *The class.*  The generators are rung two's nine rules, which its
  receipt lists as the survivors of challenge two; its five controls are
  not members of its rule class and are not stakes here (leftover G-8).
- *HALT.*  The continuation of a member is a subset of the two known
  rules, and the empty subset is a member, named HALT.  Every question is
  answered on the class with HALT and on the seed-literal subclass
  without it.
- *Switch.*  The identification tree's switch is read as a flip of the
  generator's labels, apart and same exchanged and free kept, at a
  demand-free state; no requirement is retracted because an engine
  imposes none.
- *Member two.*  Rung one declared it for an index commitment; for a
  rule reading the state its clause reads the labels of the pairs a
  response introduces after the response, in the same mode.
- *Capabilities.*  Three skeleton capabilities, the observables of the
  rule as rung two counts them, the measure, the validity clauses, the
  continuation rules.  Growth is one capability; a second declared
  reading counts it as two, and every minimum is computed under both.
- *Morphisms.*  Inclusions of declarations, and nothing else.
- *The probe.*  To level two, at the sealed bounds, at both sealed
  genesis readings.  No engine is run forward: that is challenge four.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note per file, as rungs three to ten did.
`Kernel.lean` and `IsoKernel.lean` were produced from rung ten's copies
by changing only the outer namespace, and `test_reconstruction.py`
compares them declaration by declaration with the SEALED blobs at the
snapshot: 41 shared declarations, all identical after comments and
namespace lines are stripped and whitespace is normalized.

RESTATED, credited: `Carry.lean` is rung nine's module of that name,
unedited but for the namespace and its module comment.  The Python
consumes the sealed kernel, candidate space, measures, genesis readings
and key procedure, rung two's rules, observables, dynamic validity and
minimum responses, rung one's no-op filter and delta order, and the
two-sided tree's honour relation, through their public functions, and
copies no source of any of them.  The verifiers, the coverage gate and
three test files are hand copies of rung ten's, each saying so in its
first lines.

## What is proved, what is computed, what is open

**Proved in Lean** (67 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
sixteen with none, thirty-two with `propext` alone, nineteen with both --
and no `Classical.choice` anywhere):

- an engine, as a definition: a generator, a responder, a continuation
  and a replay rule; every history of every run is named by the
  declaration, a step from a state with a demand is a response, and with
  no continuation a demand-free state has no step -- all at the level of
  a definition, and recorded so;
- equal profiles, one orbit and requirement membership are each carried
  by every inhabitant of the sealed isomorphism between any two regimes,
  forward and back, with only the admission of the two data assumed; the
  orbit statement conjugates through `isoTrans`, the composite of two
  inhabitants -- the construction the sealed estate already has as
  `Iso.trans` in `lean4/Derivation/IsoCanon.lean`, written again here
  because that module is not reconstructed, and credited, not claimed;
- so the labels and demands of E-one, E-three, E-four and E-eight, in
  both modes, are invariant under renaming for every regime; rung two
  left E-three and E-four OPEN at transport replay, and in the Lean
  mirror they are now proved invariant;
- E-one never demands in plain mode and its flip demands every pair;
  E-three and E-four are one another's flip; E-eight is quiet on every
  regime without a requirement; an E-one engine with HALT has no step;
- at the genesis of reading L, E-four has a demand and E-one none;
- over the declared class, as a finite object: 144 members, 108
  seed-literal; every count at least six, sixteen at six; every
  seed-literal count at least seven, thirty-two at seven, sixteen when
  growth counts two; no member of count one; E-three and E-four declare
  one capability list; no initial member, and none in any subclass
  holding both measures.

**Computed** over the probe -- 288 probes, 728 nodes, 608 edges:

- only E-four demands at a plain genesis root (one at L, three at F, all
  apart); in flipped mode E-one, E-two, E-three, E-five, E-six and E-nine
  demand every pair apart; every growth state is quiet;
- every demand of the probe is answered at two items, one form and one
  instance, with six and two tied minima under `mu1` and `mu2` at L and
  ten and two at F; members one and two agree there; none is refused;
- every state an E-four response reaches reads a same demand: E-four
  relabels the pair it has just separated;
- 64 members are LIVE and 16 TWO-KINDED, exactly as frozen;
- every node replays and every edge holds only its capability's events;
- the responder agrees with rung two's at the four distinct situations,
  the key partition with the brute-force one on 22 regimes, and the label
  isomorphism with the exhaustive search in 1232 comparisons, 420
  isomorphic and 812 not.

**The minima** (growth as one capability; as two in brackets): the class
sixteen, three probe classes; the seed-literal subclass thirty-two, six
classes [sixteen, five]; LIVE two, two classes, and fourteen, four
classes [twelve, four]; TWO-KINDED two and four, two classes each [two,
two].  A minimal member exists in each; none is unique up to
probe-isomorphism; none has an initial member under inclusions of
declarations.

**Open, named and priced** (G-1 to G-9 below, and the leftovers carried
from rungs three to ten).

## Superseded, dated 2026-09-25, and left standing

No earlier receipt is revised, and no earlier OPEN statement is closed
in its own tree.  Rung two's `OPEN_AT_NAMED_TARGET` for E-three and
E-four -- that their labels were not replayed on renamed regimes -- is
answered here in the Lean mirror by `e3_carried` and `e4_carried`, for
every regime; rung two's receipt and sentence stand as written at its
rung, and E-six stays OPEN.  Rung two's frozen extrapolation X, to five
data, belongs to challenge four and is not scored here.

## The frozen predictions, scored

Thirteen computational rows, scored mechanically by `run_engine.py` and
recorded in `receipts/engine.json`:

| row | value | verdict |
|---|---|---|
| C-8 | 144 and 108 members; counts six to ten; the class minima the sixteen HALT members, the seed-literal minima thirty-two [sixteen] | HIT |
| C-9 | inclusion-minimal equals count-minimal in both; 32 pairs sharing a capability set, E-two with E-seven and E-three with E-four, at 16 settings | HIT |
| C-10 | no member of count one; 144 of 144 refuse the label | HIT |
| C-11 | only E-four demands at a plain root, one at L and three at F; six rules demand every pair in flipped mode; growth states quiet | HIT |
| C-12 | every minimum is form and instance at two items; 6 and 2 at L, 10 and 2 at F; members agree; no refusal | HIT |
| C-13 | every E-four response state reads a same demand; at L exactly one | HIT |
| C-14 | 64 LIVE, 16 TWO-KINDED, the frozen sets | HIT |
| C-15 | LIVE minima 2 and 14 [2 and 12]; TWO-KINDED minima 2 and 4 [2] | HIT |
| C-16 | probe classes 3, 6 [5], 2, 4 [4], 2, 2 [2] | HIT |
| C-17 | no initial member in any minimum set or its pool; every set holds both measures | HIT |
| C-18 | zero replay mismatches, zero attribution violations | HIT |
| C-19 | four distinct situations; zero disagreements in the three cross-checks | HIT |
| C-22 | thirty-two LIVE members without the stream | HIT |

Ten rows are scored where their evidence lives and are marked so in the
receipt rather than omitted: C-1 to C-6 by the statement-shape tests of
`test_census.py` and by `verify_lean.py`; C-7 by the committed axiom
log; C-20 and C-21 by `CLAIM_LEDGER.md` and `test_census.py`; C-23 by
`run_engine.py --check`, `test_engine.py` and the measured time below.
Each is met.

**Thirteen of thirteen, and what that is worth.**  Three of the thirteen
were labelled FORCED (C-8, C-9, C-10; the fourth FORCED row, C-23, is
scored elsewhere), and a hit on them evidences the order of the work.
The ten others were reasoned by hand before the run from the sealed definitions and rung two's code, and the probe is
shallow enough that such reasoning reaches it: its genesis regimes hold
no form, every rule reads them symmetrically, and every response is the
first separation.  So the hits say the hand reasoning about level one
was right; they are weak evidence about anything deeper, and the probe
was declared shallow so that challenge four, not this attempt, would run
the engines.  That the scorer can say MISSED on every one of the thirteen
rows is shown by `test_the_scorer_can_say_missed`.

### The census prediction, and its two misses

`PREDICTIONS.md` named 50 Lean targets and a class for each, frozen
before the compile.  All 50 exist.  Scored mechanically by
`test_census.py`: **48 hits, 2 misses, no unpredicted native theorem**.

| target | predicted | recorded | why |
|---|---|---|---|
| `oneOrbit_iso` | CONTENT | THIN | each direction exhibits the conjugate automorphism and closes by one rewrite; the work sits in the definition `isoTrans`, which is not a row of the census |
| `sortPair_swap` | DEFINITION | THIN | one case closes by the antisymmetry of the order, not by computation |

**What the misses say.**  The first is a demotion, the direction rungs
three, nine and ten recorded: the content of carrying an orbit sits in
no single statement.  The second is a promotion.  With both, **no theorem
of the package is CONTENT**: every native statement is at the level of a
definition or one step from its neighbours.  That is what a declaration
should look like, and it is recorded rather than dressed up.

## Found live

**A count cannot tell two rules apart.**  The capability count, taken
as rung two took it, is a count of observables; E-three and E-four read
one observable with opposite label maps, as do E-two and E-seven, and
their members declare identical capability lists.  So inclusion of
declarations identifies members that behave differently at the first
step (`same_caps_e3_e4`, and ENG-12).  Named as G-6.

**Engines without the stream answer demands.**  E-four with HALT answers
a demand at both genesis readings, and every state its responses reach
reads a new demand of the other kind.  Thirty-two LIVE members carry the
stake and not the stream.  Whether any carries the grammar forward
beyond level two is the sharpest question this attempt leaves, and it is
the second attempt's: G-2.

**`decide` refuses the class list.**  The elaborator's recursion depth
refuses `decide` on the one hundred and forty-four members; `decide
+kernel` leaves the check to the kernel and adds no axiom, as the fresh
axiom census confirms.

## Leftovers, named and priced, executed nowhere

- **G-1, run every member forward.**  Challenge four, the second
  authorized attempt: every member of the class, from both readings, to
  declared bounds, with the census rows' FORCED columns read off the
  runs.  The probe partitions the 144 members into ten classes, by label
  signature and by exact content alike; nothing says the partition holds
  deeper.  Price: the second attempt.
- **G-2, whether a member without the stream carries the grammar
  forward.**  The thirty-two of INPUT-COUNT; the question the seed's
  required question one turns on.  Price: inside G-1.
- **G-3, the other five rules in Lean.**  E-two, E-five, E-six, E-seven
  and E-nine read profile emptiness, profile size or the number of
  classes, which this package does not mirror; E-six's invariance stays
  OPEN.  Price: moderate; a finite cardinality in core Lean.
- **G-4, the responder in Lean.**  No statement here is about a minimum,
  a cost or a tie, as at rung ten's S-3.  Price: large.
- **G-5, another reading of morphism.**  A behavioural simulation of one
  engine by another, under which an initial member might exist.  Price:
  a declaration and its enumeration.
- **G-6, a finer count.**  A capability for the label map of a rule, so
  that rules reading one observable declare different lists.  Price:
  small; it changes the minima and is a declaration.
- **G-7, the probe beyond level two.**  Probe-isomorphism is decided to
  level two only.  Price: inside G-1.
- **G-8, the two constant controls as stakes.**  Rung two kept them out
  of its rule class; a class widened by them would have members of count
  five.  Price: small, and a declaration.
- **G-9, the Python and Lean orbits are read as one.**  The Python orbit
  reads the sealed serialization's automorphisms and the Lean orbit
  inhabitants of the sealed isomorphism structure; neither checks the
  other.  Price: small, a finite check of both on the probe's regimes.
- Carried from rung ten, unchanged: S-1 to S-5.
- Carried from rung nine, unchanged: T-1, T-2, T-3.
- Carried from rung eight, unchanged: U-1, U-2.
- Carried from rung seven: V-1, V-2, V-3.
- Carried from rung six, unchanged: W-2 and W-3.
- Carried from rung five, unchanged: Z-2, Z-3 and Z-5.
- Carried from rung four, unchanged: Y-1, Y-2, Y-4.
- Carried from rung three: X-1, X-2 and X-4, unchanged.  X-5 is taken
  here: the engine is declared, its class enumerated and counted, and
  the seed's questions four and ten are answered on it.  Running the
  engines is G-1.

## The attempt budget, counted and dated

The author's ruling counts the original budget by distinct research
attempts: twelve, spent.  It authorizes at most two more in an
explicitly identified continuation.  This is the first of the two; the
second is authorized for challenge four once this one closes, and no
further attempt is authorized automatically.

## Gates and timing

Measured on this machine, 2026-09-25, by `python ci/run_gates.py --step
"continuation 1" --keep-going` at `c8655ef7`, which ran the four
registered steps of this tree in the workflow's order:

| gate | command | measured |
|---|---|---|
| clean Lean build and axiom audit | `python3 research/second_engine/verify_lean.py` | 16.2 s |
| pins, spans, frozen texts | `python research/second_engine/verify_pins.py` | 2.8 s |
| tests under coverage (152 tests), coverage gate, receipt comparison | the tree's replay, tests and coverage step | 60.6 s |
| strict typing | `python -m mypy` | 0.4 s |

Grouped measured time **80.0 seconds**, inside the fifteen-minute
ceiling the seed sets.  The registered test floor is 145.  Most of the
test step is the pin battery; the receipt builds in under a second.
Coverage over the declared measured set (`engine_decl.py`,
`engine_probe.py`, `run_engine.py`, `verify_pins.py`): **line 99.48%,
branch 97.92%**, both above the 95% floor.  The runner reported that the
interpreter's pytest (9.1.1) differs from the pin in `requirements.txt`
(9.0.3); this tree's tests run under `unittest` and do not import pytest.
An earlier run of the same command reported its HEAD moving mid-run --
this session committed while it ran -- refused to mix the two, and did
not run the typing step; it was run again with HEAD still, as above.

Fifteen injections proved the gates this tree adds, each failing by name
on its defect and recovering; they are recorded in
`research/second/MANUAL.md`.  The estate custody census, run on the
clean worktree when its pin was rewritten, reports 108 verifiers, 107
green and one pinned red that this attempt did not add.  The root prose
watchlist is clean and matches its pin; the root identifier firewall and
the gates-skill test pass; the generated views are current.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps were run
here by the repository's own runner.

## Terminal scope

- `ENGINE_DECLARED` -- DEFINITION, a generator, a responder, a continuation and a replay rule; every run's history named by the declaration.
- `CLASS_DECLARED` -- DECLARED_POLICY and DEFINITION, 144 members, 108 seed-literal.
- `CAPABILITIES_COUNTED` -- DEFINITION, every count six to ten; no member one declaration.
- `STAKES_CARRIED` -- PROVED_THEOREM, E-one, E-three, E-four and E-eight in both modes, every regime, every inhabitant of the sealed isomorphism.
- `PROBE_MEASURED` -- FINITE_COMPUTATION, level two, the sealed bounds, both readings.
- `MINIMA_RETAINED` -- FINITE_COMPUTATION with DEFINITION, every tie retained, in every subclass and under both readings of growth.
- `MINIMAL_EXISTS` -- DEFINITION.
- `MINIMAL_NOT_UNIQUE` -- COUNTERMODEL, the probe, and `minima_differ_at_genL` in Lean.
- `NO_INITIAL_UNDER_INCLUSION` -- PROVED_THEOREM, scoped to inclusions of declarations.
- `CENSUS_UNDECIDED_HERE` -- RECORDED, no census row decided in any column.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction; thirty-two streamless LIVE members within the probe.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Declare, Reconstruct, Restate, Orbit, Stake, Genesis, Engine, Census, Probe, Minima, Crosscheck, Register]
write_root: research/second_engine/
snapshot: 01876f3a43490c3518e5c2c03c975ea9d21f49c0
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
prompt_sha256: 7a2768078d63dd222398c9d3f1b3b953ee753ac094a8a01228e3adc7dbfba919
predictions_sha256: a225c07593edaea9c0cffbb5ae4e12625191cd9935f83ace066b9d3806fabee9
attempt: continuation one of two, under the author's ruling of 2026-09-25
class: {members: 144, literal: 108, least_count: 6, greatest_count: 10}
probe: {probes: 288, nodes: 728, edges: 608, live: 64, two_kinded: 16}
minima: {class: 16, literal: 32, live_class: 2, live_literal: 14, two_kinded_class: 2, two_kinded_literal: 4}
lean_theorems: {total: 67, reconstruction: 17, content: 0, thin: 28, definition: 22}
predictions_scored: {hit: 13, missed: 0, elsewhere: 10}
census_prediction_scored: {named: 50, hit: 48, missed: 2, unpredicted_native: 0}
input_count: {value: 2, proof: none, sentence: "This attempt neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: []
injections: 15
gate_time_seconds: 80.0
authority_effect: None
final_state: true
```

## The next attempt, named so it cannot be smuggled in later

The seed's next-rung rule does not choose it: the author's ruling does.
The second authorized attempt is challenge four with its
engine-dependent census evaluations -- G-1, with G-2 and G-7 inside it --
opened only after this attempt closes, keeping its declared bounds and
free to terminate OPEN.  No attempt after it is authorized.  Nothing of
it is started here.
