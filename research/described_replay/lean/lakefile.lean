import Lake

open Lake DSL

package described_replay

@[default_target]
lean_lib DescribedReplay where
  roots := #[`DescribedReplay, `DescribedReplay.AxiomReport]
