import Lake
open Lake DSL

package twin_pricing

@[default_target]
lean_lib TwinPricing where
  roots := #[
    `TwinRelation,
    `QuotientTopology,
    `ValuationPricing,
    `Inventory
  ]
