import Lake
open Lake DSL

package sign_tower

@[default_target]
lean_lib SignTower where
  roots := #[
    `Carrier,
    `History,
    `Movegraph,
    `ScaleDynamics,
    `Obstruction,
    `Inventory
  ]
