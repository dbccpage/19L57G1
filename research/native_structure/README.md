# native_structure

AuthorityEffect: None.  Plan D of the foundations roadmap: structure on
native transitions.  Every statement here is about one state space and one
step: the sealed passage state and step, and the native paths of
`research/native_bridge`.  This tree consumes both read-only and writes
nothing outside this directory.

## What it establishes

- **Cells.**  A swap exchanges two adjacent events only where, at the
  actual state the prefix reaches, both orders reach the same state.  Cells
  are the equivalence closure of swaps.  They relate parallel lists, are
  permutations, whisker on both sides, and compose horizontally.  The
  sealed frame commutations are swap generators.  Two parallel native
  loops at genesis, one in the budget and one in the license, are *not*
  related by any cell.  So cells are finer than parallelism.  `Cell` is a
  proposition, and a proof-relevant cell calculus is open.
- **Boundaries.**  Chains on native states, edges and two-step squares are
  read through integer cochains.  The boundary of a square's boundary
  vanishes for every 0-cochain exactly when the square commutes.
  Boundary cancellation *is* verified commutation.
- **Cost.**  Path cost is additive.  A cost with a potential telescopes
  and is closed on commuting squares.  A closed cost is invariant under
  cells, and a nonzero cycle excludes a potential.  The budget change has
  the budget as its potential; the count of state-changing steps has none.
  That count is nevertheless closed on every commuting square (proved
  2026-09-24; the declared battery had found no failure before), so it
  is a closed cost that is not exact.
- **Descent.**  The native core (every field but budget and license) is
  an observer through which every event except column refinement and
  column creation descends.  Those two read budget or license in their
  guards, and a proved witness shows each failing.
- **A declared symmetry.**  Renaming occurrence tokens is an action.  An
  injective renaming commutes with the step and with replay.  It is
  therefore a commuting self-translation in the sense of `native_bridge`,
  and it transports invariant costs.  A non-injective renaming does not
  commute.

The claim ledger is `CLAIMS.md`.

## Checks

```text
python verify.py --check   # pins, tests, strict typing, Lean build, named axiom reports
python run.py --check      # the finite receipt regenerates byte-identically
```

`input.json` declares the finite bounds.  `SEALED_PINS.json` records the
Git blobs of every consumed sealed or sibling source at this tree's
snapshot.  The custody test fails if a blob does not match at that
snapshot, and reports drift at HEAD without failing.
