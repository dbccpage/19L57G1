import Derivation.PrimDiff
import Limits
import DiagonalIdentity.Covering
import DiagonalIdentity.Combinator
import DiagonalIdentity.Collapse
import DiagonalIdentity.Split

/-!
# Typed split of covering-miss and identifying-push

This package stages pinned copies of `Derivation.PrimDiff` and `Limits`
under `lean/sealed/` (gitignored).  It adds no module under
`lean4/Derivation/`, writes nothing under `lean4/`, and does not
path-require `research/unboundedness/lean`.

Terminal recorded here: the covering-miss theorems and the identifying-push
theorems both hold, and they do not share binders.  Identity of
`PrimDiff.obstruction_under_irrefl` with `Covering.seq_uncountable` is not
proved.

AuthorityEffect: None.
-/
