# Predictions, frozen per freeze

A missed prediction is recorded next to its value in `STATUS.md` and is
never edited here. Freeze hashes are recorded in `SOURCE_MANIFEST.json`.

`AuthorityEffect: None.`

## Chronology, stated exactly

**Freeze 1 is RETROSPECTIVE for the Lean half of stages 1 to 3 and
PROSPECTIVE for everything else.** The Lean package
(`lean/FreshCharacters/`) was written and built before this file existed, so
its decided instances were known when freeze 1 was written. Those values are
recorded below under "already obtained" and are NOT counted as predictions.
Every line under "predicted" concerns a computation that had not run when
this freeze was hashed: the whole Python side, the exhaustive search to the
declared bounds, and stages 4 and 5.

**Freeze 2 is prospective without exception**: it was written and hashed
before `magnitude_census.py` was written and before any census value
existed.

This is a defect of the run's order, not of its results, and it is recorded
here and in `STATUS.md` rather than smoothed. A reader who wants a purely
prospective record has it for freeze 2 only.

## The value-carrier menu, frozen (stage 1)

Six members. Each is a value carrier together with the operation a character
turns steps into, and the operation totals are taken in.

- **V1** the receiver itself: values in `QOne`, characters ADDITIVE, totals
  added in the receiver.
- **V2** the integers with every character value the unit: totals added in
  the integers.
- **V3** the free abelian group on the layer's members: a character sends a
  member to a member, the step permutes them, totals are formal integer
  combinations.
- **V4** V3 modulo the single relation that the sum of all members is zero.
- **V5** the two-element sign carrier, defined only when the part count is
  even.
- **V6** V3 modulo the layer's FRESH PART, where the fresh part is defined
  by the same divisor recursion the pinned `balance` uses: the layer's own
  difference divided by the fresh parts of every proper divisor layer.

V6 was added to the operator's five at freeze time, and the reason is
recorded: V4 quotients by the total of ALL members, and this tree's own
vocabulary already distinguishes all members from FRESH members, so the
sibling quotient is the obvious sixth and refusing to write it would be a
gap in the menu, not a discipline.

## The step rules, frozen (stage 2)

Exactly four: the zero step; the unit step; the step one below the part
count; and the step given by the part count itself taken in the part count
(which is the zero step for every part count, kept in the list so the search
is over the declared four and not over three plus a judgement).

## Freeze 1 — stages 1 to 3

### Already obtained before this freeze (Lean; values, not predictions)

- All four stage-1 targets are proved in core Lean for every part count,
  carrier-free on the exponent word: `characters_are_steps`,
  `character_total_wf` (`freshExp_wf`), `character_trivial_total`
  (`freshExp_zero`), `character_restricts` (`exponent_embed`). The counting
  law `freshExp_length` is proved too.
- The V1 obstruction is proved: an additive carrier's step-zero total is the
  carrier's zero and not the fresh count
  (`additive_trivial_total_ne_freshCount`).
- Under V6, every total reduces to a plain integer for `n ≤ 20`; the
  unit-step total is the pinned balance for `n ≤ 20`; the zero-step total is
  the pinned fresh count for `n ≤ 20`; the divisor sum of the totals is the
  part count at the zero step and vanishes otherwise for `n ≤ 16`; and the
  totals depend on the step only through the largest divisor it shares with
  the part count, for `n ≤ 20`. All kernel-decided, 18 axiom reports within
  `{propext, Quot.sound}`.

### Predicted (Python; not yet run at freeze time)

- **P1.1** The Python recomputation of the four stage-1 targets agrees with
  the Lean statements at every part count `n ≤ 60`, with `0` misses.
- **P1.2** V1 fails `character_trivial_total` at every `n ≥ 1`; V5 is
  defined only at even part counts and satisfies the targets there; V2, V3,
  V4, V6 satisfy every target where it is defined. Any member failing a
  target is recorded with its obstruction and kept.
- **P2.1** The exhaustive search over the six menu members times the four
  step rules at `n ≤ 60` finds exactly one pair whose total equals the
  balance at every `n ≤ 60`: V6 at the unit step. If a second pair also
  matches, both are retained and neither is called the carrier.
- **P2.2** V2 at every step rule totals the fresh count, so it matches the
  balance only at `n = 1`. V5 totals plus or minus the fresh count. V3 and
  V4 do not reduce to an integer at every part count, so they cannot match;
  their non-reduction is recorded per part count rather than asserted.
- **P2.3** The V6 unit-step identity is cross-checked against the pinned
  `balance_values` and against the pinned running-balance checkpoints at
  `10, 30, 100, 1000, 10000` by direct recomputation, and at `100000` and
  `1000000` by the balance recursion alone; `0` disagreements. A
  disagreement would be a defect of this tree.
- **P2.4** The terminal is `TOTAL_IDENTITY_BOUNDED` at `n ≤ 60` in Python and
  `n ≤ 20` in Lean; `TOTAL_IDENTITY_PROVED` is NOT expected, because no Lean
  theorem quantified over the part count is attempted in this run. The
  general identity is the priced leftover.
- **P3.1** The divisor sum of the totals equals the part count at the zero
  step and vanishes at every other step, at every `n ≤ 60`; at the unit step
  and `n ≥ 2` this reproduces the pinned `balance_divisor_sum`, checked.
- **P3.2** The totals depend on the step only through the largest divisor
  shared with the part count, at every `n ≤ 60`, `0` counterexamples; the
  general statement stays CONJECTURE with its bounded evidence.
- **P3.3** No closed form for the totals is claimed by this run.

## Freeze 2 — stages 4 and 5

Written and hashed before `magnitude_census.py` existed and before any
census value was computed.

### Declared readings for stage 4, fixed before running

- The certificate criterion reads a list of INTEGERS. Under V6 the terms of
  a single total are members of the value carrier and not integers, so the
  term list of one total is not a list the criterion can read. Two family
  kinds are therefore censused, both recorded, and each terminal says which
  kind it belongs to:
  - the **term family** of a total: the integer values of the character at
    the fresh members, defined for the menu members whose character values
    are integers (V2 and V5);
  - the **row family** at a part count: the list `[total(n, a) : a = 0..n-1]`
    for the menu members whose totals reduce to integers (V2, V5, V6).
- The rectangle: part counts `1..60`, steps `0..n-1`, both family kinds.
- The criterion is per-magnitude domination, reconstructed from the pinned
  `certificate_iff_dominated` and cross-checked against a brute-force search
  for a pairing into exact opposites plus a single-signed residual. Zero
  terms carry no magnitude.

### Predicted

- **P4.1** Every term family has all magnitudes equal to `1`, so at the term
  level `DEGENERACY_PERSISTS` and LP4 is carried forward unchanged for that
  family kind.
- **P4.2** Some row family carries two distinct nonzero magnitudes, so
  `DIVERSITY_EXHIBITED` holds for the row-family kind. The smallest witness
  is recorded, not predicted.
- **P4.3** Every row family totals to `0` at part counts above one — a
  consequence of P3.1 read at the level of a row — and this is checked, not
  assumed.
- **P4.4** At least one row family admits NO cancellation certificate, so
  `CERTIFICATE_REFUSED` fires with a named witness. This is a prediction and
  may miss; if every row family admits a certificate the terminal is
  `DIVERSITY_EXHIBITED` alone and the miss is recorded next to the value.
- **P4.5** The two brute-force cross-checks of the criterion agree with it on
  every family in the rectangle and on every list over `{-2..2}` of length
  `5`; `0` disagreements.
- **P5.1** One row per menu member, six rows.
- **P5.2** `GROWTH_OPEN_UNCHANGED` is a terminal, no growth sentence appears
  anywhere in the tree, and `test_forbidden.py` fails the run on one.
- **P5.3** The leftovers are named and priced and none is started: the
  general identity, the enlarged menu, LP4's disposition, the certificate
  channel on a diverse-magnitude census, and the next rung.
- **P5.4** No protected open is closed: `OB1_UNCHANGED`, `S66_UNCHANGED`,
  `S9_LAST_UNCHANGED`, `NS95_GROWTH_UNCHANGED`.
