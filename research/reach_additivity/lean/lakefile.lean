import Lake
open Lake DSL

package reach_additivity

/-
Self-contained: core Lean only.  This package imports no sealed module and
reconstructs none.  The statements are about an ABSTRACT state, an abstract
one-item action, and an abstract state functional, so there is nothing to
reconstruct: what the sealed grammar supplies is one instance of the
hypothesis, and the run in `survey.py` checks that instance.
-/
@[default_target]
lean_lib ReachAdditivity where
  roots := #[`ReachAdditivity, `ReachAdditivity.AxiomReport]
