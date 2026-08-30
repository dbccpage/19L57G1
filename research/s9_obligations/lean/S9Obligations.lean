import Derivation.PrimDiff
import S9Obligations.AxiomLattice
import S9Obligations.MorphismClasses
import S9Obligations.WitnessTypes

/-!
# S9 obligations: research Lake package root

This package requires the sealed package under `lean4/` as a read-only
dependency (`require derivation from "../../../lean4"`).  It adds no
module under `lean4/Derivation/` and amends nothing sealed; every
declaration it will carry lives under `research/s9_obligations/lean/`.

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
