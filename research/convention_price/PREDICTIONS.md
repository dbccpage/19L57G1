# Predictions, written and hashed before each phase's first computation

A missed prediction is recorded next to its value and never edited.
Freeze hashes are recorded in `SOURCE_MANIFEST.json`
(`predictions_freezes`, in freeze order) and in `STATUS.md`.

## Phase 1: ParityLaws (written before the Lean package was compiled)

- PL1: `slot_toggles_parity` is provable in core Lean: a hop's
  relabelled transport parity differs from its original parity iff
  exactly one of the two slot parities consumed at its ends is the
  exchange.
- PL2: `cycle_parity_sum` is provable in core Lean: a walk's
  relabelled holonomy parity is the original parity plus (as parity
  sum) the sum of the slot parities its traversals consume, by list
  induction and nothing else.
- PL3: `pointwise_parity_blind` is provable in core Lean: on a closed
  vertex chain, a pointwise assignment's consumed slot parities
  telescope to zero, so cycle parities are unchanged -- the pinned
  packet's invariance, at parity level, proved here abstractly on this
  tree's own model rather than cited (FW-T1 respected: the citation is
  not used as the proof).
- PL4: all three carry axiom reports within `{propext, Quot.sound}`;
  any target that resists is recorded OPEN_AT_NAMED_TARGET next to its
  name, never prose-proved.

## Phase 2: Promotion (written before any phase-2 computation ran)

- PM1: `slot_group_sections` is provable in core Lean: for every
  hop-parity family there exists a slot assignment within the
  {identity, exchange} bound -- constructively, source slot identity
  and target slot the hop's own parity -- after which every walk over
  the relabelled hops has holonomy parity zero, in either traversal
  direction.
- PM2: the seven obstructed two-label census members (reconstructed
  under pin: `square_2x2_occ2`, `star_K13_occ2`, `triangle_C3_occ2`,
  `square_plus_edge_occ2`, `pan_C3_tail_occ2`, `signed_square_pos`,
  `signed_square_neg`) all have slot counts within the declared
  exhaustion bound of 20 slots, so each price floor is decided by full
  exhaustion with the pinned predicate as the only verdict source.
- PM3: the reconstructed square's price equals the pinned 2 from
  sign_slice, and its flip census reproduces the pinned 8192 of 65536
  with all 64 pointwise assignments unmoved.
- PM4: the other members' prices are recorded, not predicted; ties
  among cheapest flips are retained as counts, never collapsed.
- PM5: the general closed-form price is not proved this run: it is
  recorded as CONJECTURE with its supporting agreement data, or OPEN,
  next to the computed floors.
- PM6: `signed_square_pos` and `signed_square_neg` share every
  transport with `square_2x2_occ2`, and the predicate reads
  transports only, so their exhaustions agree with the square's; the
  agreement is checked, not assumed.

## Phase 3: SixLabel (written before the exhaustion ran)

- PS1: the space is 4^8 = 65536 assignments over eight slots (four
  choices per slot: identity and the three rank-exchange label
  actions), exhausted, not sampled; verdicts come from the pinned
  predicate only.
- PS2: BOTH branches pre-agreed, neither favoured: if some assignment
  sections the member, the terminal is SIXLABEL_MOVES, the first
  witness in the deterministic order is named with its slot distance
  from the pointwise-shaped family, and the two-label scope note is
  corrected only in the direction of MORE cure, never generalized; if
  none does, the terminal is SIXLABEL_INVARIANT_BOUNDED, stated with
  the bound in the same sentence, and the enlarged-bound question is a
  named leftover -- absence of a search is not invariance.
- PS3: the four-map relabel written for this phase agrees with the
  pinned binary relabel on every binary sub-assignment for each single
  exchange (3 x 256 cross-checks, 0 misses expected).
- PS4: the base member is obstructed as pinned; its census row is
  reproduced before the exhaustion runs.

## Phase 4: ChannelTable (written before the table was computed)

- PT1: rows are the two signed census members plus the nine obstructed
  members' signed variants (declared: amp -1 on parity-odd hops, +1
  elsewhere); no row is discarded and no walk is discarded -- the full
  closed-walk list at the declared length bound of 6 (the pinned
  register's bound, reused) is the weight list, trivial walk included.
- PT2: channel (a) is decided only within the phase-2/3 bounds; a
  member outside them is recorded NOT_COVERED_BY_BOUND, which is not
  a "no".
- PT3: channel (b) is decided by per-magnitude domination, the pinned
  characterization (SR1/SR2 of the sign-repair rung) cited as
  CONDITIONAL_THEOREM and reconstructed as computation; the dominated
  side is recorded per row.
- PT4: no cell is forced by this prompt: the separation is exhibited
  if some decided row is (a)-without-(b) or (b)-without-(a), and
  otherwise refused with the table as the record; if every weight list
  has all magnitudes equal, that degeneracy is named next to the
  refusal rather than smoothed over.
- PT5: signed_square_pos coincides with square_2x2_occ2's declared
  signed variant; the coincidence is checked and recorded, and both
  rows are kept (FW-TIES).

## Phase 5: Register (written before the register was built)

- PR1: one row per obstructed census member; no sectioned member
  appears in the register.
- PR2: every row names its leftover, priced, executed nowhere.
- PR3: the register closes none of the three protected opens, and
  SS-09's disposition is stated only in the exact partial form: the
  two-label half closes with slot_group_sections; the larger-fibre
  half stays OPEN.
- PR4: ties are retained: cheapest-flip counts are recorded, never
  collapsed to a chosen representative except as "first in the
  deterministic order", named as such.
