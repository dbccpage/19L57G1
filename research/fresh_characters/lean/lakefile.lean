import Lake
open Lake DSL

package fresh_characters

/-
Self-contained: core Lean only.  This package imports no sealed module and
declares no dependency.  The pinned receiver, balance, and step definitions
are reconstructed verbatim in `FreshCharacters/Receiver.lean`,
`FreshCharacters/Balance.lean`, and `FreshCharacters/Steps.lean`, each with a
pin note; every theorem originating here is in `Characters.lean` and
`FreshPart.lean`.
-/
@[default_target]
lean_lib FreshCharacters where
  roots := #[`FreshCharacters, `FreshCharacters.AxiomReport]
