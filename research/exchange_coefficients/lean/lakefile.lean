import Lake
open Lake DSL
package exchange_coefficients

lean_lib Derivation where
  srcDir := "pinned"
  roots := #[`Derivation.Apartness, `Derivation.BoundaryCancellation, `Derivation.Compression, `Derivation.ContactBridge, `Derivation.ContactKernel, `Derivation.DiffInterface, `Derivation.HigherStructure, `Derivation.LadderGeneral, `Derivation.ObsDescent, `Derivation.PresentationNaturality, `Derivation.PrimDiff, `Derivation.PrimitiveCats, `Derivation.PrimitiveContact, `Derivation.PrimitiveCore, `Derivation.PrimitivePassage]

lean_lib NaturalSections where
  srcDir := "pinned"
  roots := #[`NaturalSections, `NaturalSections.HopFixture, `NaturalSections.PhaseReceiver, `NaturalSections.SlotExchange, `NaturalSections.WeightedLayer]

@[default_target]
lean_lib ExamplesAudit where
  roots := #[`ExchangeCoefficients, `ClaimExample, `ExamplesAudit]
