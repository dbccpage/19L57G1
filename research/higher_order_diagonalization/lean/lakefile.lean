import Lake
open Lake DSL

package higher_order_diagonalization

@[default_target]
lean_lib HigherOrderDiagonalization where
  roots := #[
    `ObserverHierarchy,
    `SeparationCapacity,
    `Diagonalization,
    `Inventory
  ]
