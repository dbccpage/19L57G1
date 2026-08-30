import Lake
open Lake DSL

package natural_sections

/-
The sealed modules this package reads: the import closure of
`Derivation.PresentationNaturality`, twelve modules.  They are NOT a Lake
dependency on `../../../lean4` -- a path dependency is built in the
dependency's own directory and would write `lean4/.lake/`, outside this
tree's write root.  `verify_lean.py` stages the snapshot blob of each
module, byte-checked against `SOURCE_MANIFEST.json`, into `sealed/`
(gitignored), and this library compiles those copies here, so every build
product stays under `research/natural_sections/lean/.lake/`.
-/
lean_lib Derivation where
  srcDir := "sealed"
  roots := #[
    `Derivation.Apartness,
    `Derivation.Compression,
    `Derivation.ContactBridge,
    `Derivation.ContactKernel,
    `Derivation.DiffInterface,
    `Derivation.ObsDescent,
    `Derivation.PresentationNaturality,
    `Derivation.PrimDiff,
    `Derivation.PrimitiveCats,
    `Derivation.PrimitiveContact,
    `Derivation.PrimitiveCore,
    `Derivation.PrimitivePassage
  ]

@[default_target]
lean_lib NaturalSections where
  roots := #[`NaturalSections, `NaturalSections.AxiomReport]
