# Workflow reference

## 1. Intake and source seal

Create a run manifest before dispatch:

- exact goal statement and claim scope;
- exact source revisions and allowed paths;
- permitted axioms and toolchains;
- known imports and declared inputs;
- success, negative-success, and stop conditions.

Encode that manifest as the unique level-zero `hypothesis` packet. It owns
the exact source revisions, write boundary, toolchain, allowed axioms, and
admissible-construction interface. Every candidate names it as an ancestor;
there is no out-of-band narrative manifest.

The source sentinel owns custody and scope only. It cannot judge a proof.

## 2. Sparse exploration

Explorers receive the smallest source slice capable of answering their route.
Each emits one or more symbol packets, not an essay. Candidate diversity must
come from different constructions, invariants, reductions, or countermodels;
renaming the same argument does not increase width.

Use an adaptive width:

- 4 candidates for one local theorem with several plausible lemmas;
- 8 candidates for a bridge with competing representations;
- larger pools only when an explicit diversity census shows uncovered
  strategy families.

The tournament shape is a scheduling device, never mathematical evidence.

## 3. Adversarial elimination

Every candidate gets an adversary before promotion. The adversary attempts:

- smallest carriers and degenerate cases;
- hypothesis deletion;
- type mismatch and domain/codomain mutation;
- symmetry/equivariance obstruction;
- forbidden source or axiom use;
- alternative models satisfying the same premises;
- mutation of every claimed machine witness.

An eliminated packet remains in the run ledger with the falsifier. A manager
may merge duplicate routes only after a typed equivalence theorem, or may
eliminate one by domination only after a typed implication into the stronger
route. Otherwise it must retain tied non-isomorphic survivors.

## 4. Signature lock

The surviving routes are converted into a dependency graph before code work.
Every leaf contains:

- an exact Lean statement or an exact countermodel statement;
- named hypotheses and imports;
- the source declarations it consumes;
- a Python finite-model or mutation specification when applicable;
- its downstream consumer.

If a bridge cannot be written as a typed function or theorem signature, it is
not ready for another managerial layer. Return it to exploration.

## 5. Leaf proof cells

Assign one cell per independent leaf. The cell is this complete triad:

- **constructor** writes the proof, computation, or countermodel;
- **adversary** attacks only that artifact and its hypotheses;
- **referee** reruns the evidence and decides `PROVED`, `CONDITIONAL`,
  `REFUTED`, or `OPEN`.

A theory specialist may advise several cells, but owns no verdict. Add an
intermediate manager only when multiple leaves share a real interface or
lemma library. Manager count should follow the dependency graph, not a fixed
organizational chart.

## 6. Integration

The integration manager checks composition, not local elegance:

- output types exactly match downstream input types;
- every theorem hypothesis has an upstream producer or stays imported;
- source revisions and toolchains agree;
- countermodels do not invalidate a promoted generalization;
- the axiom and receipt populations cover all promoted declarations.

An import is removed only when its packet is replaced by a proved producer
whose output inhabits the exact required type.

## 7. Independent victory audit

The victory auditor starts from the run manifest and committed artifacts. It
must independently:

- rebuild from clean state;
- enumerate promoted declarations and axiom dependencies;
- rerun Python tests and deterministic receipts;
- repeat at least one decisive falsifier or gate injection;
- verify path confinement and exact source identities;
- compare the terminal status with unresolved import packets.

Failure returns to the exact responsible leaf. Do not restart the full
tournament unless the winning strategy family itself is defeated.

## 8. Prose render

Only after the victory audit, render human prose from packet fields. The prose
may explain the result but cannot add a premise, theorem, number, or scope not
present in the verified ledger.
