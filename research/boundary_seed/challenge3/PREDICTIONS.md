# Challenge 3 — predictions, written and hashed before any code or proof

`AuthorityEffect: None`.  Each prediction carries a falsifier and a
FORCED / NOT FORCED label: FORCED means the writer expects it to follow
from the definitions the run has not yet written, and a hit on a FORCED
prediction is evidence of the order of the work and not of insight.  A
missed prediction is recorded next to its value in `STATUS.md` and never
edited here.  The sha256 of this file as frozen is recorded in
`STATUS.md` and pinned by `verify_pins.py` and the tests.

The challenge: the caller now requires the process to make

    <a|>
    <|a>

internally separable in a precisely declared sense.  The run must
declare the sense, prove whether the current regime satisfies it under
each reading, price the declaration that satisfies it where it is
satisfied, and — where it is not — enumerate every non-isomorphic
minimum one-step augmentation over a declared finite candidate space
under declared cost measures, count every undeclared capability each
candidate uses, refuse any candidate called one-step that bundles
capabilities, and retain every tied minimum unless uniqueness is proved.
The state inherited from Challenge 2 is two admitted marks, placement
`(0, 1)`, labels `("a", "a")`, under the declared convention.

- C3-1 (the declared sense, and a second reading of it).  The run will
  declare the required separation to be the sense Challenge 2 computed:
  the two retained marks are separable under a reading exactly when no
  permitted automorphism of the regime carries one to the other.  It
  will also declare a second reading — some property of a mark that is
  invariant under every permitted renaming holds of one and not of the
  other — and will compute that the two readings agree at every point of
  the declared candidate space under both readings of the boundary, the
  witness for the second being an orbit property where no declared mark
  property is both invariant and separating.  NOT FORCED: the choice of
  sense is the run's, and it could declare a different one.  Falsifier:
  a different declared sense; or a point of the declared space at which
  the two readings of the requirement disagree.
- C3-2 (the current regime, and what does the work under O).  Under O
  the current regime already satisfies the requirement and under U it
  does not.  The declaration that satisfies it under O is the
  withdrawal of the side exchange from the permitted renamings, carried
  by the O reading of the one admitted primitive and paid at genesis by
  the declared reading, not by the run at this rung; the two admitted
  names are **not** used by the separation.  The run will show this by a
  four-cell counterfactual over the two coordinates (names admitted or
  not) by (the side exchange permitted or not): the requirement is met
  in exactly the two cells where the exchange is not permitted, whether
  or not the names are admitted.  FORCED.  Falsifier: the O regime
  failing the requirement; the U regime satisfying it; or any of the
  four cells coming out the other way.
- C3-3 (no addition of judgment forms can satisfy it under U).  While
  the composite of the side exchange with the exchange of the two marks
  remains a permitted automorphism, no addition of judgment forms
  satisfies the requirement, whatever the forms added: every property of
  a mark that is invariant under that composite takes the same value at
  the two retained marks.  This will be PROVED in Lean for an arbitrary
  property, and the one concrete addition in the declared space —
  admitting the two side names into the U tower — will be computed to
  fail.  The two mark forms of Challenge 2 will be shown, by a Lean
  countermodel, not to be invariant under the composite, which is why
  they separate the two marks as raw data and not internally.  FORCED.
  Falsifier: an addition of judgment forms that satisfies the
  requirement with the composite still permitted; the Lean statement not
  covering an arbitrary property; or either mark form turning out
  invariant under the composite.
- C3-4 (the declared candidate space, and the refusal of bundles).  The
  declared candidate space will have five coordinates — withdraw the
  side exchange; withdraw the mark permutations; admit the two side
  names; keep the presentation labels in the serialization; admit one
  further mark, on side 0 or on side 1 — giving 48 points under each
  reading.  A candidate is one-step exactly when it changes one
  coordinate, which is exactly when the count of undeclared capabilities
  it uses is one; every candidate whose count is two or more is refused
  as bundling; and the candidate that adopts reading O under U — the
  names together with the withdrawal — has count two and is refused,
  although its withdrawal half alone is a minimum.  NOT FORCED: the
  space is declared and a different space is available.  Falsifier: a
  point count other than 48; a one-step candidate whose capability count
  is not one; the reading-O candidate costing other than two; or a
  candidate of the space that the count and the one-step test classify
  differently.
- C3-5 (the minimum under U is one, and it is not unique).  Under U
  exactly four one-step points of the declared space satisfy the
  requirement — withdraw the side exchange; withdraw the mark
  permutations; admit one further mark on side 0; admit one further mark
  on side 1 — and under the implemented isomorphism relation they fall
  into exactly three classes, the two further-mark points being one
  class because the side exchange is still permitted there.  All three
  are retained and uniqueness is refuted.  FORCED.  Falsifier: a
  different set of satisfying one-step points; a different class count;
  or a proof that the minimum is unique.
- C3-6 (the two cost measures agree on the minimum and are not the same
  measure).  The second declared measure is the collateral count: how
  many of five declared facts about the retained configuration, none of
  them internally available under U at the close of Challenge 2, a
  candidate makes internally available besides the required separation
  itself.  It will be one at each of the three minima, so both measures
  select the same three classes; and the two measures will differ in
  value at some point of the declared space, so neither is the other.
  FORCED.  Falsifier: a minimum whose collateral count is not one; the
  two measures selecting different minimum sets; or the two measures
  agreeing at every point of the space.
- C3-7 (the three minima separate by three different mechanisms, and one
  of them satisfies the requirement by unfolding).  Against the declared
  list of mark properties — lies on side 0, lies on side 1, has index 0,
  has index 1, carries the label `a` — withdrawing the side exchange
  makes the two side properties invariant and separating and leaves the
  two index properties non-invariant; withdrawing the mark permutations
  makes the two index properties invariant and separating and leaves the
  two side properties non-invariant; and admitting one further mark
  makes none of the five both invariant and separating, its witness
  being an orbit property alone.  The second of the three satisfies the
  requirement by unfolding the declaration — with the mark permutations
  withdrawn no permitted renaming moves an index at all — so it is
  DEFINITION-level, and the run will say so rather than count it as
  content: the declared sense admits a candidate that internalizes the
  metatheoretic admission index, and the requirement as declared does
  not oblige the admitted boundary to do the work.  FORCED.  Falsifier:
  any of the three mechanism rows differing; a fifth property turning
  out invariant and separating somewhere; or the second minimum's
  satisfaction resting on a computation rather than on unfolding.
- C3-8 (what the reading changes, and what the boundary is charged).
  The difference between the two readings changes both the price and the
  count at this rung: under O the minimum capability count is zero and
  the unique minimum is the null augmentation, while under U it is one
  and three classes attain it.  Every result of this rung about sides,
  separation, and the candidates requires the admitted boundary and is
  not formulated after removing it; the identity of the candidate space,
  the capability counts, and the refusal of bundles do not.  NOT FORCED:
  the boundary-dependence classification is the run's.  Falsifier: a
  minimum count other than zero under O or other than one under U; more
  than one minimum class under O; or a separation result the run
  classifies as independent of the admitted boundary.
- C3-X (the extrapolation, scored by Challenge 4).  When Challenge 4
  supplies `<a|b>` and `<b|a>` and requires the same declared
  separation, the declared reader bound of at most one mark per whole
  will have to be widened to one mark on each side of the bar, and that
  widening will be a new declaration priced like this rung's, paid by
  the run.  The two wholes will become four admitted marks with
  placement `(0, 1, 0, 1)` under the declared convention, so the two
  sides will carry equally many marks and the composite of the side
  exchange with a mark renaming will again be a permitted automorphism
  under U; the requirement will therefore fail again under U, with the
  same minimum count of one, and hold again under O with no new
  declaration.  What the boundary contributes at Challenge 4 will be
  exactly what it contributed here — the side each mark lies on — and
  what it cannot contribute is the matching of a visible mark across the
  boundary: whether the `a` of the first whole and the `a` of the second
  are the same mark will remain internally unavailable under both
  readings.  NOT FORCED.  Falsifier: Challenge 4 needing no widened
  reader bound; a retained placement whose two sides carry different
  numbers of marks; the U requirement met with no augmentation; the O
  requirement needing a new declaration; or the matching of a visible
  mark across the boundary becoming internally available under either
  reading.
