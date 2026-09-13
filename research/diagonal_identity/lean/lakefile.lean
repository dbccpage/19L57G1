import Lake
open Lake DSL

package diagonal_identity

/-
The modules this package reads are NOT Lake path dependencies.  A path
dependency is built in the dependency's own directory and would write
`lean4/.lake/` or `research/coherent_process_limits/lean/.lake/`, outside
this tree's write root.  `verify_lean.py` stages the pinned snapshot blobs
of `lean4/Derivation/PrimDiff.lean` and
`research/coherent_process_limits/lean/Limits.lean`, byte-checked against
`SOURCE_MANIFEST.json`, into `sealed/` (gitignored), and these libraries
compile those copies here.
-/
lean_lib Derivation where
  srcDir := "sealed"
  roots := #[`Derivation.PrimDiff]

lean_lib Limits where
  srcDir := "sealed"
  roots := #[`Limits]

@[default_target]
lean_lib DiagonalIdentity where
  roots := #[`DiagonalIdentity, `DiagonalIdentity.AxiomReport]
