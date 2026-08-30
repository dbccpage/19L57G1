import Derivation.PrimDiff
import S9Obligations.AxiomLattice
import S9Obligations.MorphismClasses
import S9Obligations.WitnessTypes

/-!
# S9 obligations: research Lake package root

This package reads the sealed module `Derivation.PrimDiff` as a
byte-pinned staged copy: `verify_lean.py` writes the snapshot blob of
`lean4/Derivation/PrimDiff.lean`, checked against `SOURCE_MANIFEST.json`,
to `sealed/Derivation/PrimDiff.lean` (gitignored), and the `Derivation`
library of `lakefile.lean` compiles it here.  A Lake path dependency on
`../../../lean4` would build in `lean4/.lake/`, outside this tree's write
root, which a reviewer of pull request 96 demonstrated on a clean
checkout.  The package adds no module under `lean4/Derivation/`, writes
nothing under `lean4/`, and amends nothing sealed; every declaration it
carries lives under `research/s9_obligations/lean/`.

The root imports `Derivation.PrimDiff` and the part modules landed so
far: `S9Obligations.AxiomLattice` (P1, step 13),
`S9Obligations.MorphismClasses` (P2, step 19), and
`S9Obligations.WitnessTypes` (P3, step 26).  The parts P1, P2, and
P3 of `research/s9_obligations/PROMPT.md` add their own modules under
`S9Obligations/` and import them from here; each exported theorem then
receives its own report line in `S9Obligations/AxiomReport.lean`, and
`verify_lean.py` requires every such report to lie within
`{propext, Quot.sound}`.

AuthorityEffect: None.  This package proposes; it discharges nothing on
its own, and a green build is a build receipt, not a discharged
obligation.
-/
