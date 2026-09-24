# native_bridge

AuthorityEffect: None.  This tree reads research traces back as sequences of
native events, and records a counterexample wherever a reading fails.  It
imports the sealed Lean package and the sealed Python dynamics read-only,
and the G013 tree's `Trace` module as a Lake dependency.  It writes nothing
outside this directory.

## What it establishes

A **path** here is indexed by actual steps.  Each constructor's target is
the state that the sealed step function computes, so no intermediate state
is free data.  For every deterministic step function:

- paths from `s` to `t` correspond exactly to event lists whose replay from
  `s` ends at `t`;
- paths compose, with identities and associativity;
- the event encoding sends composition to concatenation.

This construction is instantiated three times:

- **The passage dynamics** (`PrimitivePassage.step`).  Native paths and the
  sealed typed traces correspond both ways, and the sealed erasure theorem
  is re-derived from the path square.  Refusals persist along paths.
  Every step keeps every field except budget and license, or strictly
  grows a size.  So **a cycle can move only the budget and the license**,
  and both do carry cycles.
- **The admission kernel** (`Derivation.stepE`).  Its step returns
  `none` on an ill-formed admission, so paths carry the successful step
  equations.  Every successful step keeps or
  grows the regime, so the kernel has no cycle through two distinct
  regimes.  Token-aware paths map to admission paths whose events are the
  sealed `eraseHistory`.
- **G013 traces over passage states.**  A supplied label decoder reads a
  G013 trace back as a native path exactly when every step is realized by
  the sealed step.  A one-step G013 trace whose endpoints *are* natively
  joined is still refused, because its own step is not native.  G013 steps
  are unconstrained, so a G013 trace is not by itself a native trace.

A **commuting translation** gives one replay square per source step.  It
lifts source paths to native paths and preserves composition.  Two
consequences:

- **Squares are cheap.**  Every system with an injective numbering commutes
  with the passage through budget writes alone, with an injective encoding
  (`budgetSim`).  So a commuting square with an injective encoding does not
  show that the passage reproduces the source's structure.
- **The squares do constrain where cycles live.**  The encodings of all
  states on a source cycle share every field except budget and license.
- **Observation excludes the budget register** (2026-09-24).  The
  passage's own observation (zero relation, obstruction, refusal) reads
  only the core.  So a translation that also preserves an observation
  sees one native observation on every source cycle, and a budget register
  preserves only a constant one.  The toggle, observed by its own state,
  has no faithful observation-preserving translation.

The claim ledger is `CLAIMS.md`.  Its open rows are:

- event selection;
- the read-back of the X310 and G012 carriers.

## Checks

```text
python verify.py --check   # pins, tests, strict typing, Lean build, named axiom reports
python run.py --check      # the finite receipt regenerates byte-identically
```

`verify.py` is the canonical new-tree verifier, unchanged.  `input.json`
declares the finite bounds and is pinned in `SOURCE_MANIFEST.json`.
`SEALED_PINS.json` records the Git blobs of every consumed sealed or
sibling source at the snapshot this tree was derived against.  The custody
test fails if a blob does not match at that snapshot, and reports drift at
HEAD without failing.  The Lean report scope is the exact declaration list
in `TREE_CONTRACT.json`.
