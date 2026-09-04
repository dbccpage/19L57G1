# Challenge 1 — predictions, written and hashed before any code or proof

`AuthorityEffect: None`.  Each prediction carries a falsifier and a
FORCED / NOT FORCED label: FORCED means the writer expects it to follow
from the definitions the run has not yet written, and a hit on a FORCED
prediction is evidence of the order of the work and not of insight.  A
missed prediction is recorded next to its value in `STATUS.md` and never
edited here.  The sha256 of this file as frozen is recorded in
`STATUS.md` and pinned by `verify_pins.py` and the tests.

The challenge: the caller supplies `<a|>`, another opaque whole, except
that the admitted boundary places its mark on a side.  Challenge 1
supplies; the word "retains" first appears at Challenge 2.  So the run
will carry, under each reading, the supplied-only history and the
admitted history as separate certified regimes, and say which facts hold
in which.

- C1-1 (supply is presentation only).  Under both readings the supply of
  `<a|>` is a new external presentation event and nothing else: the
  regime after `Supply(a)` equals genesis, and every judgment of the
  closed grammar holds after the supply exactly when it held before.
  FORCED, from the Challenge 0 inertia theorem.  Falsifier: a judgment
  whose holding changes across a supply, or a supply-only history that
  certifies a regime other than genesis.
- C1-2 (admission is a separate event, and the mark is retained).  The
  mark of `<a|>` enters the admitted state only through a separately
  defined admission event; certifying replay refuses that event without
  the prior supply and accepts it after.  Once admitted, the mark's
  judgment is unchanged by every later event of the Challenge 1 grammar
  (a further supply, or a re-admission of the same token on either side,
  which is designation and not duplication).  FORCED.  Falsifier: a
  supply-only history reaching a placed mark, or a later event of the
  grammar that removes or moves the admitted mark.
- C1-3 (exactly one new judgment; the mark's profile is its side).  After
  admission, under both readings, exactly one judgment holds that did not
  hold before: `OnSide(0, s)` for the placed side `s`; `OnSide(0, s')`
  for the other side does not hold; the side-name judgments hold after
  every event exactly as before, so under O they are unchanged and under
  U there are none.  The mark's own profile is therefore that one
  judgment and nothing else.  A supply alone adds no holding judgment, so
  a new external inscription does not by itself increase the set of
  holding judgments; only its admission does, by one.  FORCED.
  Falsifier: a second new holding judgment, a changed name judgment, or a
  holding judgment added by supply alone.
- C1-4 (the two sides under U).  Under U, after admission the two
  extensional side profiles differ, and the admission is the only event
  in the history.  The two candidate admitted regimes (mark on side 0,
  mark on side 1) are each the other's reflection, are unequal as raw
  data, and have the same canonical key.  So "the mark lies on exactly
  one side" is a U fact, while "which side" is not: no judgment of the
  closed grammar that is invariant under the permitted reflection names
  the side.  FORCED.  Falsifier: equal U profiles after one admitted
  mark, different U keys for the two candidates, or a reflection-invariant
  judgment that holds for one candidate and not the other.
- C1-5 (the two sides under O, and the convention).  Under O the
  inscription `<a|>` does not itself say which admitted name the left of
  the bar carries.  The run will have to declare a presentation-to-side
  convention (left is side 0, which O names `near`) as metatheory; the
  two candidate admitted regimes are unequal, have different canonical
  keys under O, and the regime under the other convention is exactly the
  reflection of the designated one.  Both candidates are carried; the
  designation is by convention and not by proof.  NOT FORCED: the run
  could instead carry the two O candidates as branches with no
  designation, and the prediction is about which of those it does and
  what the facts are.  Falsifier: a derivation of the O side of `a`
  from the inscription alone with no declared convention, equal O keys
  for the two candidates, or a designated regime whose reflection is not
  the other candidate.
- C1-6 (no transition follows).  No object-language transition follows
  from the supply or from the admitted one-mark regime under either
  reading: the declared event-follows relation stays empty on the new
  regimes, and Challenge 1 justifies no augmentation of the event or
  judgment grammar.  The initial datum and the reading are unchanged by
  every event.  FORCED.  Falsifier: an event in the relation on a
  Challenge 1 regime, or a Challenge 1 result that requires a new event
  kind or judgment form.
- C1-7 (one boundary, no second datum).  Every Challenge 1 result is
  stated with the mark placed on a side of the one admitted boundary; no
  result requires admitting the whole `<a|>` as a second opaque datum or
  a second boundary.  Whether a whole on a side is itself a datum is left
  OPEN for Challenge 5, where the seed asks it.  NOT FORCED: this is a
  modelling decision the run has not yet made, and the seed's phrase
  "the admitted boundary" is the reason for expecting it.  Falsifier: a
  Challenge 1 fact that cannot be stated without a second datum or a
  second boundary in the regime.
- C1-X (the extrapolation, scored by Challenge 2).  When Challenge 2
  supplies and retains `<a|>` and `<|a>` as two admitted marks on
  opposite sides of the one boundary: under U the admitted regime is
  fixed by the reflection up to mark renaming (the equal-count law of the
  Challenge 0 census at two marks), so the two marks are exchanged by a
  permitted automorphism and no judgment of the closed grammar that is
  invariant under permitted renaming separates them, which is what "not
  internally distinguishable by the admitted boundary alone" will mean;
  under O the two marks are separated by the side names (one lies on
  `near`, the other on `far`), the price is the O declaration paid at
  genesis, and nothing new is paid at Challenge 2.  NOT FORCED: it
  depends on Challenge 2 admitting two internal identities for the two
  wholes despite the shared glyph `a`, which the Challenge 0 token
  uniqueness rule does not do by itself.  Falsifier: under U a
  permitted-renaming-invariant judgment of the closed grammar that
  separates the two marks with no new declaration; under O a price
  beyond the names; or Challenge 2 admitting one mark twice so that only
  one mark exists.
