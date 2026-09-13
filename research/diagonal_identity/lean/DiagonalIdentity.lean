import Derivation.PrimDiff
import Limits
import DiagonalIdentity.Covering
import DiagonalIdentity.Combinator
import DiagonalIdentity.Collapse
import DiagonalIdentity.Split
import DiagonalIdentity.Dual

/-!
# Typed split of covering-miss and identifying-push

This package stages pinned copies of `Derivation.PrimDiff` and `Limits`
under `lean/sealed/` (gitignored).  It adds no module under
`lean4/Derivation/`, writes nothing under `lean4/`, and does not
path-require `research/unboundedness/lean`.

Terminal recorded here: dual shapes on the declared carriers, not identity.
Pair-id is non-injectivity plus `Irrefl` failure; family-miss is
non-surjectivity of a `Nat`-indexed family.  They do not recode each other.
The square-then-flip combinator packages the covering side only.  Identity
of `PrimDiff.obstruction_under_irrefl` with `Covering.seq_uncountable` is
not proved.

AuthorityEffect: None.
-/
