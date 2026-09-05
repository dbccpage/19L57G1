# Challenge 4 — predictions, written and hashed before any code or proof

`AuthorityEffect: None`.  Each prediction carries a falsifier and a
FORCED / NOT FORCED label: FORCED means the writer expects it to follow
from the definitions the run has not yet written, and a hit on a FORCED
prediction is evidence of the order of the work and not of insight.  A
missed prediction is recorded next to its value in `STATUS.md` and never
edited here.  The sha256 of this file as frozen is recorded in
`STATUS.md` and pinned by `verify_pins.py` and the tests.

The challenge: the caller supplies and retains

    <a|b>
    <b|a>

and requires their internal separability in the declared sense.  The object
language has no licensed access to glyph identity, order, or matching
beyond what it has already derived and admitted.  The run must determine
what the admitted boundary contributes here that it did not contribute at
Challenge 3, and what it cannot contribute.  The state inherited is the
Challenge 2 retention — two marks, placement `(0, 1)`, labels `("a", "a")` —
with nothing admitted at Challenge 3 and none of its three minima taken.

- C4-1 (the reader bound, and what the retention makes).  The Challenge 1
  reader refuses both inscriptions by name, its declared bound being at
  most one mark in a whole, so the bound must be widened deliberately to
  at most one mark on each side of the bar; that widening is a new
  declaration of the run, priced like Challenge 2's occurrence identity
  and paid by the run, and the Challenge 1 reader is left refusing.  Under
  the Challenge 2 reading of "retains" and the declared occurrence
  identity, the caller's history is then a supply and an admission for
  each of the four marks, eight events, and the current state under each
  reading is its replay: four admitted marks, placement `(0, 1, 0, 1)`
  under the declared convention and a declared within-whole admission
  order, labels `("a", "b", "b", "a")`, certified and replayed from
  genesis.  The other within-whole order gives an isomorphic regime under
  both readings, so that order is not internally available.  FORCED.
  Falsifier: the Challenge 1 reader accepting either inscription; a
  retained placement other than `(0, 1, 0, 1)`; a history that is not one
  supply and one admission per mark; or the other within-whole order
  giving a non-isomorphic regime.
- C4-2 (the requirement fails under BOTH readings, and what carries one
  whole onto the other).  For the first time in the run the current regime
  fails the requirement under reading O as well as under reading U.  The
  obstruction is the exchange of the two wholes — the mark permutation
  carrying mark 0 to mark 2 and mark 1 to mark 3 — which carries the
  retained regime onto itself with no side exchange at all, so the
  withdrawal that reading O carries does not touch it.  Of the six pairs
  of distinct admitted marks, under O exactly the four pairs lying on
  different sides are separable and the two pairs sharing a side are not;
  under U no pair is separable.  FORCED.  Falsifier: the O regime meeting
  the requirement; a permitted automorphism that carries neither whole
  onto the other; the whole exchange needing the side exchange; or any
  pair status differing from the four-and-two split under O.
- C4-3 (what the boundary contributes, and what it cannot).  The admitted
  boundary contributes here what it contributed at Challenge 3 — the side
  each mark lies on — but that now sorts the four marks into two classes
  of two and no finer, so it no longer meets the requirement under either
  reading: both declared side-reading whole properties are invariant under
  both readings and separate neither whole from the other.  What it cannot
  contribute is which mark within a side is which, the grouping of marks
  into wholes, and the matching of a visible mark across the boundary: the
  configuration in which the second whole's `a` is a token the caller
  never presented is isomorphic to the retained one under both readings.
  What is new relative to Challenge 3 is that under O the pair of a
  label and a side becomes a complete invariant of the four marks, so
  keeping the presentation labels meets the requirement under O and does
  not meet it under U — the two wholes being each other's reflection,
  which is exactly what reading U cannot see.  NOT FORCED: the
  classification of a contribution is the run's.  Falsifier: a
  side-reading whole property that separates the two wholes; the
  cross-boundary matching being internally available at the retained
  regime under either reading; or the label-keeping candidate meeting the
  requirement under U, or failing to meet it under O.
- C4-4 (the declared candidate space).  The declared space will have seven
  coordinates: the five of Challenge 3 — withdraw the side exchange;
  withdraw the mark permutations; admit the two side names; keep the
  presentation labels; admit one further mark, on side 0 or on side 1 —
  together with two this rung declares: admit the whole grouping, so that
  each admitted mark carries which presented whole admitted it; and name
  the two wholes, so that the exchange of the two whole tags is not a
  renaming.  That is 192 points under each reading.  A candidate is one
  step exactly when it moves one coordinate, which is exactly when the
  count of undeclared capabilities it uses is one; every candidate of
  count two or more is refused as bundling; and naming the wholes without
  admitting the grouping changes nothing and collapses into the null point
  under the implemented quotient, under both readings.  NOT FORCED: the
  space is declared and a different space is available.  Falsifier: a
  point count other than 192; a one-step candidate whose capability count
  is not one; or the name-wholes point not collapsing into the null point.
- C4-5 (the minimum under U, and its uniqueness).  Under U exactly one
  one-step point of the declared space meets the requirement: withdrawing
  the mark permutations.  The minimum capability count is one, exactly one
  class attains it, and uniqueness is therefore NOT refuted inside the
  declared space — the first rung at which it is not.  That unique
  minimum is the DEFINITION-level one: with the mark permutations
  withdrawn no permitted renaming moves an index at all, so it meets the
  requirement by unfolding and leaves the admitted boundary idle
  entirely.  In particular the withdrawal of the side exchange, which was
  a minimum at Challenge 3, does not meet the requirement here, and
  neither does a further mark on either side.  FORCED.  Falsifier: a
  second satisfying one-step point under U; a class count other than one;
  a minimum capability count other than one; or the side-exchange
  withdrawal or a further mark meeting the requirement under U.
- C4-6 (the minima under O).  Under O exactly two one-step points meet the
  requirement: withdrawing the mark permutations, and keeping the
  presentation labels.  They fall into two classes, tied at capability
  count one, both retained, and uniqueness is refuted under O.  So the two
  readings differ in their minima at this rung in both directions: O has a
  minimum that U does not, and neither reading meets the requirement
  without an augmentation.  FORCED.  Falsifier: a different set of
  satisfying one-step points under O; a different class count; or a
  minimum capability count other than one.
- C4-7 (the grouping is what the caller asked for, and it is a bundle).
  Admitting the whole grouping alone does not meet the requirement: with
  the two whole tags admitted but not named, the exchange of the two tags
  is a renaming the object language cannot see, and composed with the mark
  permutation that exchanges the two wholes it carries the regime onto
  itself and one whole onto the other.  Naming the two wholes without
  admitting the grouping is a no-op.  The two together do meet the
  requirement, under both readings, at a capability count of two — so the
  augmentation that gives the caller internal wholes, which is what the
  requirement is about, is refused as a bundle, and neither half of it is
  a minimum.  FORCED.  Falsifier: the grouping alone meeting the
  requirement; the grouping with the names costing other than two; or the
  pair failing to meet the requirement under either reading.
- C4-8 (the two senses of separability part, and how).  The rung declares
  the requirement as a statement about the two retained wholes — no
  permitted automorphism carries the mark-set of one onto the mark-set of
  the other — and beside it the Challenge 3 sense taken pointwise, that
  every pair of distinct admitted marks is separable.  The whole sense
  reduces to the Challenge 3 sense at the Challenge 3 configuration, where
  each whole is one mark, which the receipt computes under both readings.
  Over the declared space the pointwise sense implies the whole sense at
  every point, and the converse fails at some point: where the grouping is
  admitted and the wholes are named under U, the two wholes are separable
  while the two marks of one whole are not.  FORCED.  Falsifier: a point
  at which the pointwise sense holds and the whole sense fails; the two
  senses agreeing at every point of the space; or the two senses
  disagreeing at the Challenge 3 configuration.
- C4-X (the extrapolation, scored by Challenge 5).  When Challenge 5
  supplies `<<a|>|>`, the widened reader of this rung will refuse it by
  name as well, its declared bound reading marks and not wholes, so the
  bound will have to be widened a second time and priced a second time,
  paid by the run.  The regime records one side per admitted mark and no
  depth, so depth will not be an internally available count at the
  retained regime under either reading, and the boundary within a side
  will not be visible without a new declaration.  The rung will have to
  decide what the inner whole is — a datum, a side, or something needing a
  new definition — and that decision will take the shape Challenge 2's
  did: a declared finite space of policies with exactly one member letting
  the caller retain the inscription, priced and paid by the run.  NOT
  FORCED.  Falsifier: this rung's reader accepting the nested whole; depth
  being an internally available count with no new declaration; the inner
  whole being a datum with no declaration; or the decision not taking the
  form of a declared finite policy space.
