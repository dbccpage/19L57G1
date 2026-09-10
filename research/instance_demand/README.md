# Instance demand: Stages 1 and 2 checkpoint

AuthorityEffect: None. OB-1 remains **OPEN**. This is a staged construction
attempt with supplied targets and prior exposure, outside the sealed derivation.

Stage 2 constructs a finite uniform-closure materializer and proves that it
stores fresh syntax without changing derivability or observational separation.
It supplies answerable, initially unmet pairs under a declared instance reading.
The procedure still needs a represented emitter and an obligation interpretation
to establish E1. Neither Outcome A nor full instance-channel impossibility is
claimed. Stage 1's provenance results and original I1 controls remain intact.

## Stage 2 construction and result

For each ruled form, enumerate all tuples of its declared arity over the current
data. Remove tuples already in the instance store. Apply one existing instance
admission per remaining entry. This procedure retains all consequences; its
index order serializes the list without selecting a demand pair. The explicit
additional operation is a **host procedure producing admission events**.
Admitting the native uniform rule itself still does not run that procedure.

`lean/ClosureMaterialization.lean` proves the enumeration's membership
characterization, finite list bound, replay through sealed admissions,
well-formedness preservation, unchanged data/forms/rules/requirements, and
unchanged derivability for every instance. Consequently every context's
separation behavior is preserved. After one pass the pending list is empty;
the materializer is idempotent. This is a fixed-point result for that procedure,
not a theorem about every possible dynamics or generator.

The new samples start with two or three data, one binary form, its uniform rule,
and no instances or requirements. Four or nine fresh instances are stored. A
declared reader of stored form 0 retains all pairs `x < y`, yielding one or
three pairs. They remain collapsed. In Lean, every such pair in this sample
family has a valid response: a fresh unary form and its instance at `x`.
The two concrete seed/materialization/response histories replay from genesis.
Python also replays a single combined response that separates every read pair
in each sample; that combined three-data response is a computation, whereas
Lean proves a response for each pair individually.

The reading of form 0 as an obligation is a declared convention. The initial
rule already makes those tuples derivable, and new storage alone does not make
them new semantic obligations. The reader still returns an answered pair
(`answered_pair_still_read`). E3 has conditional witnesses on these seeds, not
a general guarantee of fresh unmet demand after arbitrary responses.

| Clause | Stage 2 assessment |
|---|---|
| E1 | OPEN: prove the emitter and its reading are represented by admitted structure; deterministic host code and replay do not establish this. |
| Literal E2 | Not satisfied by this candidate: `reqs` is unchanged. The earlier `C_reqs` result is untouched. |
| Owed-separation E2 | Conditional witness under the declared reading; the obligation role and endogenous generation remain unproved. |
| E3 | New stored pair payloads are initially unmet in the reachable samples; an already answered pair is still readable. |
| E4 | Each pair in the sample family has a Lean-proved valid response; concrete whole histories replay in both implementations. |
| Dynamics | One pass reaches a fixed point. No continuing endogenous production follows. |

Observational conservativity does not rule out an instance reader observing
the added syntax. Conversely, observing new syntax does not itself establish
an endogenous obligation. Stage 3 must resolve that distinction.

## Stage 1 results retained

For every successful sealed history, a stored instance occurs exactly when its
instance admission event occurs in that history (or it was in the initial
state). This is an occurrence theorem: an encoded program could in principle
determine such an event. **The theorem does not identify its source as external.**
The corresponding faithful-reader theorem applies to every reader satisfying
its stated membership condition; that condition alone does not establish E1.

Admitting a uniform rule preserves the instance store. A derivable instance
absent from that store is covered by its form's uniform rule, so every tuple
of that form is derivable. The latter follows from the native definition even
for ill-formed tuples; consumers must separately enforce arity and bounds.
Neither statement turns logical derivability into an admission event.

The original I1 singleton instance `(0, [x,y])` with distinct endpoints already
separates them: the context `(0, [hole,y])` accepts `x` and rejects `y`.
The general Lean lemma requires `y` to be an admitted datum; the reachable
examples also have `x` admitted. Thus the original witness fails E3. Adding the
form's uniform rule makes the same pair collapsed while its instance remains
stored. This control prevents extending the singleton failure to all encodings.
It is still an explicitly admitted instance, not a demonstrated production rule.

The L and F controls have respectively two and three data, with the target at
`(0,1)` and `(1,2)`. Both histories contain no requirement event. They are
requirement-free analogues of those readings, not the Challenge-3 histories
with their imposed requirements removed from a claimed replay of those states.

## Evidence and reproduction

`lean/InstanceDemand.lean` has 14 authored theorems and nine generated reports.
`lean/ClosureMaterialization.lean` adds 28 authored theorems and 29 generated
reports. The combined census has 80 reports, all within
`{propext, Quot.sound}`. `lean/Inventory.lean` obtains that population from the
compiled environment independently of the printed reports. No private theorem
is permitted in the namespace.

`probe.py` sweeps 1,062 reachable states on one binary form, sizes 0..3, every
instance subset and each rule subset, with empty initial requirements. It checks
17,762 successful single-event extensions and 2,337 derivable-but-unstored
instance cases. This bounded computation is a separate control for the general
Lean results. Python token handling and Lean's token-erased histories are not
proved equivalent by these stages.

`materialize.py` reuses that 1,062-state rectangle and checks 2,337 new
admissions, preservation of every datum's complete finite context profile,
native replay, and 1,062 fixed points. Additional tests cover mixed unary,
binary, and ternary forms, an unruled form, an existing requirement, malformed
inputs, omitted or extra consequences, wrong admission traces, and corrupted
replay or observation results. The combined suite has 25 tests and passes
strict typing. Both measured modules have 100% statement and branch coverage.

From this directory, with Python, coverage, mypy, and Lean 4.33.0 installed:

```text
python verify.py --lake PATH_TO_LAKE
```

The verifier checks sources at the pinned base and HEAD and from disk; checks
the runtime origin of the consumed Python modules; runs tests, strict typing,
and compilation; compares the complete namespace census to the axiom reports;
and compares fresh evidence bytes. Coverage measures `probe.py` and
`materialize.py` and requires
95% statements and branches independently. Verification apparatus is outside
that coverage claim. `--write` deliberately regenerates the receipts. Inputs
are hashed with text line endings normalized; evidence files are byte-bound.

`evidence/computation.json` retains the Stage 1 record unchanged, including its
historical next-stage field. `evidence/materialization.json` records Stage 2;
`lean.json` and `verification.json` cover both stages.

This work is a local checkpoint, not a registration in the twelve gate
families. Full repository integration and a merge decision are later work.

## Remaining stages

1. **Stage 1 COMPLETE:** native provenance and singleton/control witnesses.
2. **Stage 2 COMPLETE:** uniform-closure materialization, conservative replay,
   fixed point, conditional unmet-pair witnesses, and existing responses.
3. **Stage 3:** attempt an emitter controlled by admitted program instances,
   with a fixed interpreter retaining every alternative or refusing ambiguity.
   Prove the semantic bridge; replayability alone is insufficient.
4. **Stage 4:** assess E1, literal E2, owed-separation E2, E3, E4, and the dynamics
   claim separately. The event-origin theorem does not close this stage.
5. **Stage 5:** reconcile claims and artifacts, run required local integration
   checks, and prepare publication when authorized.
