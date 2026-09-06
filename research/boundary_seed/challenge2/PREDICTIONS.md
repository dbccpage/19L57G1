# Challenge 2 — predictions, written and hashed before any code or proof

`AuthorityEffect: None`.  Each prediction carries a falsifier and a
FORCED / NOT FORCED label: FORCED means the writer expects it to follow
from the definitions the run has not yet written, and a hit on a FORCED
prediction is evidence of the order of the work and not of insight.  A
missed prediction is recorded next to its value in `STATUS.md` and never
edited here.  The sha256 of this file as frozen is recorded in
`STATUS.md` and pinned by `verify_pins.py` and the tests.

The challenge: the caller supplies **and retains** both opaque wholes

    <a|>
    <|a>

the same visible mark, the other side.  The run must say what changed
merely by admission, what remains internally unavailable, and whether
the two wholes are internally distinguishable by the admitted boundary
alone; and if so, what that cost and who paid it.  Challenge 1 admitted
nothing, so nothing is inherited as current state.

- C2-1 (what "retains" licenses).  The run will read the caller's
  "retains" as the admission of both wholes, so that after Challenge 2
  the current state under each reading is the replay of a caller history
  containing, for each whole, a supply and an admission, and that state
  holds two admitted marks, one on each side under the declared
  convention.  No new state-changing capability beyond admission is
  needed for that reading, and the caller's two supplies are the same
  event value twice, separated only by their position in the history.
  NOT FORCED: this is the run's decision about a word of the seed, and
  the run could instead refuse and record OPEN.  Falsifier: a current
  state after Challenge 2 with fewer than two admitted marks, a state
  change with no admission event in the caller's history, or two marks
  on the same side under the declared convention.
- C2-2 (the shared visible mark refuses the Challenge 1 admission, by
  name).  The caller's Challenge 2 history, formed with the Challenge 1
  admission event under either convention, is refused by certifying
  replay under both readings, and the refusal is the moving-admission
  refusal by name: the Challenge 1 event keys the admitted mark by its
  presentation token, so the second whole names the first mark and asks
  for it on the other side.  FORCED, from the kernel as Challenge 1
  leaves it.  Falsifier: that history certifying a two-mark regime, or
  being refused for any other reason, or the refusal depending on the
  reading or on the convention.
- C2-3 (the identity policy is one declaration, and it is not free).
  Exactly two identity policies lie in the declared space — the second
  admission names a mark already admitted, or a fresh one — and only the
  second lets the caller retain both wholes; every policy of the space
  is one of the two, because the second admission's target either is or
  is not already admitted.  The run declares the second at the price of
  one new admission event and the withdrawal of the token-uniqueness
  rule, so that internal identity is the admission index and the
  presentation token is a label a regime may carry twice.  That price is
  paid by the run, not by the boundary and not by the caller, and it is
  the same under both readings.  NOT FORCED: the run could refuse the
  challenge and record it OPEN.  Falsifier: a third policy inside the
  declared space; the caller's retention expressible with no new
  declaration; the price differing between the readings; or the boundary
  rather than the run paying it.
- C2-4 (what admission adds: two judgments, and nothing else).  Under
  each reading the two admissions add exactly two holding judgments,
  `OnSide(0, s)` and `OnSide(1, s')` with `s` and `s'` the two sides, and
  change no name judgment, no initial datum, and no reading; the count of
  holding judgments goes 0 to 2 under U and 2 to 4 under O; each mark's
  profile is its own side and nothing else; and no new judgment form is
  needed.  Each admitted mark's judgment survives every later event of
  the Lean grammar.  FORCED.  Falsifier: a third new holding judgment, a
  changed name judgment, a changed datum or reading, or a Challenge 2
  fact that needs a new judgment form.
- C2-5 (under U the two marks are exchanged by a permitted
  automorphism).  Under U the retained regime is carried to itself by the
  reflection followed by the exchange of the two marks; its permitted
  automorphism group has exactly two elements, the identity and that
  composite, while under O it has exactly one.  The composite exchanges
  the two marks, so no mark property invariant under permitted renamings
  separates them, and neither of the two mark-naming judgment forms is
  invariant under U.  FORCED, from the equal-count law of the Challenge 0
  census at two marks.  Falsifier: a different automorphism count under
  either reading; no automorphism exchanging the marks under U; or a
  permitted-renaming-invariant mark form that holds of one U mark and not
  the other.
- C2-6 (under O the two marks are separated, and by the names).  Under O
  the only permitted automorphism of the retained regime is the identity,
  the two admitted names hold as at genesis, and the two marks are
  separated: both mark-naming judgment forms are invariant under the
  permitted renamings of O and both separate the marks, one mark lying on
  `near` and the other on `far`.  The separation costs the boundary read
  as O, paid at genesis, and the Challenge 2 identity policy, paid at
  this rung; the presentation convention decides which presented whole is
  which mark and not that they are separated, so the regime under the
  other convention lies in the same isomorphism class as the declared
  one, under both readings.  FORCED.  Falsifier: a permitted automorphism
  of the O regime exchanging the marks; equal mark side-profiles under O;
  a separation that survives removing the names; or the other
  convention's regime lying in a different class.
- C2-7 (what the boundary alone buys, under both readings).  Under both
  readings it is an internal fact that the two marks do not share a side:
  the property "no two admitted marks lie on the same side" is invariant
  under every permitted renaming of both readings, checked over every
  regime of at most three marks, and it holds of the retained regime.
  Under U the boundary alone buys that and nothing further about the two
  wholes; under O it buys, in addition, which of them lies on which named
  side.  FORCED.  Falsifier: a permitted renaming after which two marks
  share a side; the property failing at the retained regime; or a further
  invariant U fact separating the two wholes.
- C2-8 (the two sides become interchangeable again under U).  Under U the
  two sides, which one admitted mark made unequal at Challenge 1, are
  exchanged by a permitted automorphism once both wholes are retained, so
  they are not internally separated at Challenge 2; the profile
  comparison `sides_collapsed` is false there and is therefore not the
  internal fact, because it reads internal identities that a permitted
  renaming permutes.  Under O no permitted renaming exchanges the sides
  and they stay separated by their names.  Neither the admission order of
  the two wholes nor the visible mark they share is internally available
  under either reading.  NOT FORCED: the run has not declared an
  exchangeability notion, and Challenge 0 declared only the profile
  comparison.  Falsifier: no permitted automorphism exchanging the U
  sides at the retained regime; `sides_collapsed` true there; an
  exchanging automorphism under O; or an internal fact that reads the
  admission order or the visible mark.
- C2-X (the extrapolation, scored by Challenge 3).  When Challenge 3
  requires `<a|>` and `<|a>` to be internally separable in a declared
  sense, the run will declare that sense to be the one Challenge 2
  computes — no permitted automorphism carries one mark to the other —
  and will find the requirement already satisfied under O by the
  declaration of the reading, with no augmentation, and unsatisfied under
  U.  Under U no augmentation that only adds a judgment to the closed
  grammar can satisfy it, because the automorphism transports every
  judgment; so every minimum one-step augmentation will either name a
  side, paying under U what reading O paid at genesis, or admit a further
  datum that the automorphism cannot carry, and there will be at least
  two tied non-isomorphic minima, so uniqueness will not be provable.
  NOT FORCED.  Falsifier: Challenge 3 declaring a different sense and
  finding the O requirement unmet; a U augmentation that separates the
  marks by adding a judgment alone; a single minimum proved unique; or a
  minimum that pays neither a side name nor a further datum.
