# Instance demand: Stages 1 through 3 checkpoint

AuthorityEffect: None. OB-1 remains **OPEN**. This is a staged construction
attempt with supplied targets and prior exposure, outside the sealed derivation.

Stage 3 constructs an emitter controlled by stored instructions and proves its
calculation agrees with the existing graph execution on functional operands.
It also refutes identifying the added composition rule with sealed derivability.
The output-admission operation and obligation meaning remain host conventions,
so E1 and OB-1 remain OPEN. Neither Outcome A nor full instance-channel
impossibility is claimed. Stages 1 and 2 remain intact as scoped inputs.

## Stage 3 construction and result

The declared layout stores instruction `(k,l,o)` as `(0,[k,l,o])`; operation
index `k` refers to binary form `3+k`, following the existing execution layout.
From that instruction and stored edges `(3+k,[x,z])`, `(3+l,[z,y])`, the
interpreter emits `(3+o,[x,y])` when `x < y`. This is a fixed syntactic reading:
no requirement store or observational profile selects the output. All matching
paths are retained. Distinct paths may give the same tuple and therefore
repeat an admission event; storage itself deduplicates it.

`lean/RepresentedEmitter.lean` proves exact instruction/edge decoding and output
membership. On functional operand graphs, the resulting endpoint equals the
existing `Execution.run` result for the two-operation word. Every successful
two-step execution output with `x < y` is retained by the emitter even when
other paths exist. The first direction's functionality assumption matters:
`Execution.lookup` takes the first matching edge, while this emitter retains
all paths. Python's separate unique lookup refuses ambiguity. These claims
concern `Execution` on stored graphs, not the entire finite-setting encoding.

The admission wrapper keeps only well-formed, initially unstored output tuples
and feeds their instance events through sealed replay. General Lean theorems
prove exact final membership, replay, unchanged other fields, and preserved
well-formedness. `represented_run_keeps_graph` separately proves that the
existing execution operation itself does not perform this write.

The stronger native inference claim is false: `native_closure_counterexample`
gives a reachable well-formed regime with the instruction and both premises,
but the unruled output is not derivable. `no_native_join_rule` refutes the
universal inference from this stored pattern to native derivability. It does
not quantify over all conceivable instance generators or interpreters.

Two output controls identify the remaining demand problem:

| Output form | Before output admission | After output admission | Assessment |
|---|---|---|---|
| Unruled | The pair is collapsed; the output is not derivable. | The singleton output separates its own endpoints. | The proposed stored demand fails E3 at the post-emission state. |
| Uniformly ruled | The pair is collapsed; the output is already derivable but unstored. | The stored output leaves the pair collapsed. | Conditional unmet-pair witness; native production and obligation meaning remain unproved. |

The L and F samples add one auxiliary datum to the two- and three-data reading
analogues: respectively 3 and 4 data, targets `(0,1)` and `(1,2)`, and
intermediates 2 and 3. The admitted instruction is `[0,1,2]`; all six forms are
explicitly admitted, including the layout's two unused unary forms. No claim
of a minimum encoding is made. For covered outputs a fresh unary form 6 and
its instance at the first endpoint answer the pair. Lean proves valid responses
and whole histories from genesis; both generating histories contain no impose.
They are not the sealed Challenge-3 states. Removing the instruction disables
the emitter; the finite samples retain the same observational profiles.

E1 is still the missing admission/interpretation bridge. Literal E2 fails
because `reqs` stays unchanged. Under owed-separation E2 the covered samples
provide conditional payload and response witnesses, not a proved endogenous
obligation. Stage 3 covers one emission pass. It does not transfer Stage 2's
fixed-point theorem to this different procedure or claim sustained dynamics.

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
an endogenous obligation. Stage 3 resolves the computation bridge for its
declared composition program and leaves the admission/obligation bridge OPEN.

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
reports. `lean/RepresentedEmitter.lean` adds 36 authored theorems and 30 generated
reports. The combined census has 146 reports, all within
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
replay or observation results.

`emitter.py` checks 5,140 reachable configurations: 1,044 from every pair of
binary-relation subsets on 0..2 active data, crossed with instruction presence
and output coverage; plus 4,096 pairs of partial functional graphs on three
active data, with the instruction present and the output covered. Each census
state has three additional admitted data outside the active graph carrier,
the six-form layout, and empty requirements. This padding makes the instruction
codes valid; it is not claimed necessary. The run records 2,560 admission events,
2,528 distinct new instances, 2,340 functional execution paths, and 522 states
without an instruction. Separate tests cover multiple instructions, differing
output forms, ambiguity, repeated outputs, and invalid output forms/arities.

The combined suite has 39 tests and passes strict typing. All three measured
modules have 100% statement and branch coverage. The original ten input pins
remain unchanged; `STAGE3_SOURCE_MANIFEST.json` adds 25 baseline-pinned files
covering the newly imported execution dependencies and package configurations.

From this directory, with Python, coverage, mypy, and Lean 4.33.0 installed:

```text
python verify.py --lake PATH_TO_LAKE
```

The verifier checks sources at the pinned base and HEAD and from disk; checks
the runtime origin of the consumed Python modules; runs tests, strict typing,
and compilation; compares the complete namespace census to the axiom reports;
and compares fresh evidence bytes. Coverage measures `probe.py`,
`materialize.py`, and `emitter.py` and requires
95% statements and branches independently. Verification apparatus is outside
that coverage claim. `--write` deliberately regenerates the receipts. Inputs
are hashed with text line endings normalized; evidence files are byte-bound.

`evidence/computation.json` retains the Stage 1 record unchanged, including its
historical next-stage field. `evidence/materialization.json` retains Stage 2
unchanged, including its historical next-stage field. `evidence/emitter.json`
records Stage 3; `lean.json` and `verification.json` cover all three stages.

This work is a local checkpoint, not a registration in the twelve gate
families. Full repository integration and a merge decision are later work.

## Remaining stages

1. **Stage 1 COMPLETE:** native provenance and singleton/control witnesses.
2. **Stage 2 COMPLETE:** uniform-closure materialization, conservative replay,
   fixed point, conditional unmet-pair witnesses, and existing responses.
3. **Stage 3 COMPLETE:** stored composition instructions, graph-execution bridge,
   admission replay, native-inference counterexample, and two output controls.
   This completes the candidate attempt; E1 itself remains OPEN.
4. **Stage 4:** assess E1, literal E2, owed-separation E2, E3, E4, and the dynamics
   claim separately. The event-origin theorem does not close this stage.
5. **Stage 5:** reconcile claims and artifacts, run required local integration
   checks, and prepare publication when authorized.
