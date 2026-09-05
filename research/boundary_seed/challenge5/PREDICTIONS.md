# Challenge 5 — predictions, written and hashed before any code or proof

`AuthorityEffect: None`.  Each prediction carries a falsifier and a
FORCED / NOT FORCED label: FORCED means the writer expects it to follow
from the definitions the run has not yet written, and a hit on a FORCED
prediction is evidence of the order of the work and not of insight.  A
missed prediction is recorded next to its value in `STATUS.md` and never
edited here.  The sha256 of this file as frozen is recorded in
`STATUS.md` and pinned by `verify_pins.py` and the tests.

The challenge: the caller supplies and retains

    <<a|>|>

a whole within a side.  The run must determine whether the object language
can see a boundary within a side; whether a whole on a side is a datum, a
side, or something requiring a new definition; what "within" means at depth
two under each reading; whether depth is an internally available count; and
what admission, if any, is needed to treat the inner whole as the outer whole
was treated.  Nesting is assumed neither admissible nor inadmissible.  The
state inherited is the Challenge 4 retention — four marks, placement
`(0, 1, 0, 1)`, labels `("a", "b", "b", "a")` — with nothing admitted at
Challenge 3 or Challenge 4 and none of their minima taken.

- C5-1 (the readers, and the third widening).  Both readers the run already
  has refuse `<<a|>|>` by name: the Challenge 1 reader, whose declared bound
  is at most one mark in a whole, and the Challenge 4 reader, whose declared
  bound is at most one mark on each side of the bar.  Neither reads an item
  that is itself a whole.  So the bound must be widened a third time, to a
  reader in which an item on a side is a mark or a whole, down to a declared
  finite depth beyond which it refuses by name; that widening is a new
  declaration of the run, priced like the Challenge 4 widening and paid by
  the run, and both narrower readers are left refusing so that what forced
  each widening stays visible.  FORCED.  Falsifier: either earlier reader
  accepting the inscription; the widened reader accepting an inscription
  deeper than its declared bound; or the widening not being priced as a
  declaration of the run.
- C5-2 (the declared policy space, and its prices).  What an admission does
  with an item that is itself a whole is not decided by the admitted
  boundary, so the run declares a finite space of policies and prices each in
  capabilities.  The space will have four members: refuse the nested item
  entirely; admit the inner whole as ONE opaque mark on the outer side,
  discarding its interior; discard the inner boundary and admit the inner
  whole's own items on the outer side; and admit the inner whole's items
  while recording, for each admitted mark, the finite sequence of sides
  crossed to reach it.  Their capability counts will be `0`, `1`, `1`, and
  `2`: three capabilities are declared, reaching inside a nested whole,
  admitting a whole as a mark, and recording the crossing, and the last
  policy uses two of them.  A policy is one step exactly when its capability
  count is one, so the recording policy is refused as a bundle exactly as the
  grouping-with-names was at Challenge 4.  NOT FORCED: the space is declared
  and a different space is available.  Falsifier: a policy count other than
  `0`, `1`, `1`, `2`; one step not coinciding with capability count one; or
  the recording policy having capability count one.
- C5-3 (at every one-step policy the nesting is invisible).  Under both
  one-step policies and under both readings, the regime the caller's history
  retains from `<<a|>|>` carries exactly one admitted mark, on the side the
  declared convention gives the inner whole, and is isomorphic to the regime
  the Challenge 1 inscription `<a|>` retains under the same reading.  So the
  object language cannot see a boundary within a side at any one-step policy:
  the nested inscription and the flat one are internally indistinguishable
  there, under both readings.  FORCED.  Falsifier: either one-step policy
  retaining a regime with a mark count other than one; either retaining a
  regime not isomorphic to the one `<a|>` retains under either reading; or
  the two inscriptions being internally distinguishable at a one-step policy.
- C5-4 (the two one-step policies are nevertheless two, and both are
  retained).  They are not the same policy: on the declared finite domain of
  inscriptions the enumeration will name at least one inscription at which
  the regimes they retain are not isomorphic.  So among the policies that
  admit the caller's inscription at all the minimum capability count is one,
  exactly two non-isomorphic classes attain it, both are retained, and
  uniqueness is refuted at this rung — where at Challenge 4 it was not
  refuted under U.  The class key will be the policy's behaviour over the
  whole declared domain and not its behaviour at the caller's one
  inscription, at which the two agree up to isomorphism and a one-inscription
  key would report a single class.  FORCED.  Falsifier: the two one-step
  policies agreeing up to isomorphism at every inscription of the declared
  domain; a class count other than two at the minimum; a minimum capability
  count other than one; or the two policies differing at the caller's own
  inscription.
- C5-5 (what the inner whole is, under each policy).  Under no policy is the
  inner whole a second initial datum: the regime carries exactly one and
  validation refuses any other, so no admission event can make a second one.
  Under no policy is it a side: sides are two per boundary, come with the
  boundary, and are never admitted.  It is a MARK under the opaque policy,
  NOTHING AT ALL under the discarding policy — which admits only its
  contents — and a SECOND BOUNDARY under the recording policy, which is a new
  definition.  Treating the inner whole as the outer whole was treated means
  exactly that its own two sides are places at which a further mark may be
  admitted, and that holds under the recording policy alone, which is not a
  minimum.  NOT FORCED: the classification is the run's.  Falsifier: a
  retained regime carrying a second initial datum; a policy admitting the
  inner whole as a side; or the inner whole's two sides being places at which
  a further mark may be admitted under a policy of capability count one.
- C5-6 (depth, in two senses that are kept apart).  Under the two one-step
  policies no component of the state records depth, every admitted mark is
  reached by crossing one boundary, and depth is therefore constant and
  separates nothing.  Under the recording policy the depth of a mark — the
  length of the sequence of sides crossed to reach it — is invariant under
  every permitted renaming and is determined by the key, so it is internally
  available in the sense the run declared at Challenge 3 and generalized at
  Challenge 4.  It is nevertheless not expressible: no judgment form of the
  closed observation grammar reads it, the grammar having no counting form,
  and this rung adds none.  So "is depth an internally available count" has
  two answers that the rung keeps apart, and neither is unconditional.
  FORCED.  Falsifier: a permitted renaming that changes a mark's depth; two
  configurations of the declared domain with equal keys and different depths;
  a judgment form of the closed grammar whose value depends on depth; or a
  mark of depth other than one under a one-step policy.
- C5-7 (at depth two each reading splits, and only one of the two splits
  collapses).  Whether the reading's naming of the two sides reaches the
  inner boundary is a further declaration that the seed's one admitted
  exception does not decide, and the run will carry it as a coordinate.
  Under U it collapses: U names nothing at any level, so both values of the
  coordinate declare the same permitted renamings and the same key, and the
  implemented quotient identifies them — as the naming of the wholes without
  the grouping collapsed at Challenge 4.  Under O it does not collapse.  With
  the naming reaching the inner boundary, no side exchange is permitted at
  either level and the mark's whole address is determined; without it, the
  exchange of the inner boundary's two sides is a renaming the object
  language cannot see, so which side of the inner boundary the mark lies on
  is NOT internally available under O either.  Under U the mark's address
  orbit will have four members, under O with the naming reaching inward one,
  and under O without it two.  FORCED.  Falsifier: the coordinate not
  collapsing under U; the inner side being internally available under O
  without the further declaration; or an address orbit size other than four,
  one, and two respectively.
- C5-8 (inertia, and the outside).  Nothing at this rung changes the initial
  datum, the reading, or the event-follows relation, which stays empty on
  every event of every declared kind at every retained configuration; the
  caller's history under each admitting policy is certified and replays from
  genesis; and no event kind of an earlier rung is withdrawn.  The run
  declares no address value denoting the outside of the outermost boundary:
  an address is a sequence of sides crossed inward, so the outside is not
  formulable in the declared alphabet and stays OPEN, named rather than
  answered.  FORCED.  Falsifier: a non-empty event-follows relation at any
  retained configuration; a retained configuration that does not replay from
  genesis; an address value denoting the outside; or an earlier event kind
  withdrawn.
- C5-X (the extrapolation, scored by the next stage).  The next stage is the
  autonomous continuation, in which the run declares, for a surviving branch,
  the weakest deterministic finite procedure it can justify for generating
  the next challenge from that branch alone.  The first challenge such a
  generator justifies from a surviving Challenge 5 branch will be a further
  MARK and not a deeper nesting: a further mark costs one capability at every
  rung that has priced it, deeper nesting costs two here, and the generator
  is required to be the weakest justified.  The stage will not reach fifteen
  accepted augmentation rounds on any branch in one session; it will declare
  a smaller resource bound, export the exact frontier, and state what is
  complete within that bound and nothing wider.  NOT FORCED.  Falsifier: the
  generator's first challenge from a surviving branch being a deeper nesting;
  the generator importing object-language structure the run has not declared;
  fifteen accepted rounds being reached on any branch; or the stage exporting
  no frontier under a declared bound.
