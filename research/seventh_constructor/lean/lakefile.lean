import Lake
open Lake DSL

package seventh_constructor

@[default_target]
lean_lib SeventhConstructor where
  roots := #[
    `ConservativeGrammar,
    `MovegraphTopology,
    `OperationalPricing,
    `Inventory
  ]
