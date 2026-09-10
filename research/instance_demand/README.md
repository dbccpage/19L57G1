# Instance demand: Stage 1 checkpoint

AuthorityEffect: None. OB-1 remains **OPEN**. This is a staged construction
attempt with supplied targets and prior exposure, outside the sealed derivation.

Stage 1 supplies instance-provenance theorems and tests the original I1 encoding.
It does not claim Outcome A or impossibility of every represented generator.

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

`lean/InstanceDemand.lean` has 14 authored theorems. The compiled environment
census includes nine generated theorems, for 23 reports, all within
`{propext, Quot.sound}`. `lean/Inventory.lean` obtains that population from the
compiled environment independently of the printed reports. No private theorem
is permitted in the namespace.

`probe.py` sweeps 1,062 reachable states on one binary form, sizes 0..3, every
instance subset and each rule subset, with empty initial requirements. It checks
17,762 successful single-event extensions and 2,337 derivable-but-unstored
instance cases. This bounded computation is a separate control for the general
Lean results. Python token handling and Lean's token-erased histories are not
proved equivalent by this stage.

From this directory, with Python, coverage, mypy, and Lean 4.33.0 installed:

```text
python verify.py --lake PATH_TO_LAKE
```

The verifier checks sources at the pinned base and HEAD and from disk; checks
the runtime origin of the consumed Python modules; runs tests, strict typing,
and compilation; compares the complete namespace census to the axiom reports;
and compares fresh evidence bytes. Coverage measures `probe.py` and requires
95% statements and branches independently. Verification apparatus is outside
that coverage claim. `--write` deliberately regenerates the receipts. Inputs
are hashed with text line endings normalized; evidence files are byte-bound.

This stage is a local checkpoint, not a registration in the twelve gate
families. Full repository integration and a merge decision are later work.

## Remaining stages

1. **Stage 1:** native provenance and singleton/control witnesses (this tree).
2. **Stage 2:** attempt uniform-closure materialization; distinguish stored
   instances from derivable tuples and state any additional admission law.
3. **Stage 3:** attempt an emitter controlled by admitted program instances,
   with a fixed interpreter retaining every alternative or refusing ambiguity.
   Prove the semantic bridge; replayability alone is insufficient.
4. **Stage 4:** assess E1, literal E2, owed-separation E2, E3, E4, and the dynamics
   claim separately. The event-origin theorem does not close this stage.
5. **Stage 5:** reconcile claims and artifacts, run required local integration
   checks, and prepare publication when authorized.
