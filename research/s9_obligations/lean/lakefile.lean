import Lake
open Lake DSL

package s9_obligations

/-
The sealed module this package reads.  It is NOT a Lake dependency on
`../../../lean4`: a path dependency is built in the dependency's own
package directory, so a clean run would write `lean4/.lake/`, outside this
tree's declared write root (PROMPT.md step 2; review finding on pull
request 96).  Instead `verify_lean.py` stages the pinned snapshot blob of
`lean4/Derivation/PrimDiff.lean`, byte-checked against `SOURCE_MANIFEST.json`,
into `sealed/Derivation/PrimDiff.lean` (gitignored), and this library
compiles that copy here, so every build product stays under
`research/s9_obligations/lean/.lake/`.  Nothing under `lean4/` is read by
Lake and nothing under `lean4/` is written.
-/
lean_lib Derivation where
  srcDir := "sealed"
  roots := #[`Derivation.PrimDiff]

@[default_target]
lean_lib S9Obligations where
  roots := #[`S9Obligations, `S9Obligations.AxiomReport]
