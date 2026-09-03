import Lake
open Lake DSL

package closed_family

/-
Self-contained: core Lean only.  This package imports no sealed module and
declares no dependency.  The pinned presentation machinery is reconstructed
verbatim in `ClosedFamily/Base.lean` with a pin note and per-block manifest
records; every theorem originating here is in `ClosedFamily/Closure.lean`.
-/
@[default_target]
lean_lib ClosedFamily where
  roots := #[`ClosedFamily, `ClosedFamily.AxiomReport]
