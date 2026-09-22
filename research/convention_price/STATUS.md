# convention_price: the price of the slot convention

Two named leftovers were consumed, quoted in `PROMPT.md` from their
own trees: sign_slice `SS-09` (promotion of the occurrence-relabel
finding requires Lean that tree did not carry), and the sign-repair
rung's fenced route comparison (slot relabelling against pairing
certificates, named there as a future rung so it could not be smuggled
in as done).  This tree carries the Lean, executes the comparison, and
states both dispositions with their scopes.

Frozen inputs: native `PROMPT.md` sha256
`6ed89e9be7434fc3d78f03a608c9acf5625670938c749390191efc718f934e6c`;
predictions frozen at
`150044ee5a657a12c98516b761784433f56e25a71fc5c380d499e0b585b0ac3a`
(phases 1-2, before any phase computation) and
`8c6691c8973ea643b51a87120d38c944b72f6ef1b562f9808576886e6268fbed`
(phases 3-5, also before any phase computation ran).  Sources read are
pinned in `SOURCE_MANIFEST.json` at snapshot
`d54118ca6d8768e6f1ef31cc8e72192f7880f8be`; `verify_pins.py` checks
them at the snapshot and at HEAD.  Every prediction was disposed
CONFIRMED or held; no prediction missed this run (the dispositions are
in the receipt next to their values).

## Declared readings (recorded, not silently chosen)

The operator charter arrived with gaps; per its own rule, each became
a declared reading here rather than a question:

1. **Template blocks.**  The charter says "[LAWS] as template v2,
   verbatim" and the same for [DONE], but no template file exists in
   this repository.  Reading: the laws and done conditions are
   reconstructed from chain step 1's own rendering of the same
   template -- the sign_slice hard-rules and evidence-discipline
   paragraphs -- and appear so in `PROMPT.md`.
2. **A truncated refusal name.**  One refusal identifier between
   FW-BILL and FW-LEAD arrived cut off in transmission.  Reading:
   FW-T1, the consumed trees' standing refusal (never cite the pinned
   packet's pointwise-invariance proof as the answer to a slot
   question), is adopted by name; `pointwise_parity_blind` re-proves
   the parity-level fact abstractly instead of citing it.
3. **"Three adjacent rank-exchange label actions."**  A three-element
   rank set has two adjacency-neighbouring exchanges; the charter
   says three and prices the space as `4^8`.  Reading: the three
   exchanges of the rank set, each acting on labels by the pinned
   transport construction; the space is `4^8 = 65536` as priced.
4. **One snapshot for two predecessor trees.**  The frozen charter
   records the original construction reading in which the two consumed
   trees were combined on this branch.  That history is now superseded:
   the repaired sign-repair and repinned sign-slice trees were merged
   first, this tree was rebased onto their shared `main` descendant, and
   the snapshot above pins that exact merge result.  The nested
   sign-slice pin verifier is therefore clean at HEAD; no predecessor
   drift is accepted or hidden.  The frozen `PROMPT.md` and
   `PREDICTIONS.md` remain byte-identical historical inputs.
5. **Eleven evidence classes.**  The charter's admissible vocabulary
   names "the eleven evidence classes" without listing them.  Reading:
   the eleven listed in `PROMPT.md`, which extend sign_slice's seven
   with PROVED_THEOREM (this tree carries Lean), CONJECTURE,
   METATHEORY, and PREDICTION.

## Terminals, each with its scope

- PARITY_LAWS_PROVED (PROVED_THEOREM): on this tree's abstract
  two-label parity model, in core Lean with no sealed import --
  `slot_toggles_parity` (a hop's relabelled parity toggles iff exactly
  one end slot is the exchange), `cycle_parity_sum` (relabelled
  holonomy parity = original + consumed slot parities),
  `pointwise_parity_blind` with corollary `pointwise_cycle_invariant`
  (a pointwise assignment's consumed parities telescope to zero on
  closed chains, so cycle parities are unchanged -- the pinned
  packet's invariance at parity level, proved here abstractly, FW-T1
  respected).  18 `#print axioms` reports, all within
  `{propext, Quot.sound}`, 16 of them axiom-free.
- PROMOTION_PROVED (PROVED_THEOREM + FINITE_COMPUTATION), TWO-LABEL
  ONLY (FW-SCOPE): `slot_group_sections` -- every hop-parity family is
  cured by an explicit slot assignment within the {identity, exchange}
  bound (near slot identity, far slot the hop's own parity), after
  which every walk's holonomy parity vanishes in either traversal
  direction.  Computationally: the concretized witness sections all
  seven obstructed two-label census members (pinned predicate as the
  only verdict source), and the price floor -- least slot distance of
  a flipping assignment from the pointwise family -- was decided by
  full slot-space exhaustion at every one of them under the declared
  20-slot bound:

  | member | slots | flips | price | ties at price |
  |---|---|---|---|---|
  | square_2x2_occ2 | 16 | 8192 | 2 | 1024 |
  | star_K13_occ2 | 12 | 2048 | 1 | 384 |
  | triangle_C3_occ2 | 6 | 32 | 1 | 24 |
  | square_plus_edge_occ2 | 20 | 32768 | 2 | 448 |
  | pan_C3_tail_occ2 | 16 | 8192 | 1 | 192 |
  | signed_square_pos | 16 | 8192 | 2 | 1024 |
  | signed_square_neg | 16 | 8192 | 2 | 1024 |

  The square reproduces the pinned 8192 / price 2 / 64-of-64
  pointwise-unmoved exactly (PM3).  The pinned 2 is NOT universal:
  three members price at 1 (A4 disposed per member, no
  extrapolation).  Pointwise assignments moved nothing anywhere.
- PRICE_FORM_CONJECTURE (CONJECTURE): the closed form -- price equals
  the least per-hop disagreement between a flipping consumed-parity
  class and a pointwise consumed-parity class -- is supported by exact
  agreement of the slot-space and consumed-class routes on flip count
  and price at all seven members, and proved nowhere.  Support is not
  proof; the routes share the pinned predicate and differ in
  enumeration.
- SIXLABEL_MOVES (FINITE_COMPUTATION), within the bound of four maps
  per slot (identity and the three rank exchanges) on eight slots,
  `4^8 = 65536` exhausted, not sampled: the occupancy-3 square moves.
  10965 assignments section it; the first witness in the deterministic
  order is `[0, 0, 0, 0, 0, 0, 1, 3]`; none of the 256
  pointwise-shaped assignments moves it; the cheapest flip sits at
  slot distance 1 from the pointwise-shaped family, with 768 ties at
  that price.  Per the pre-agreed reading, the two-label scope note is
  corrected only in the direction of MORE cure: a six-label member
  also moves, at its own bound; no grammar-wide sentence follows
  (FW-LEAD was held -- the outcome was stated nowhere before the
  exhaustion ran, and both terminals were frozen in `PREDICTIONS.md`
  first).
- CHANNELS_AGREE_ON_DECIDED_ROWS + TABLE_WRITTEN
  (FINITE_COMPUTATION): 11
  rows -- the two signed census members plus the nine obstructed
  members' declared signed variants (amp -1 on parity-odd hops;
  `signed_square_pos` IS the square's variant, checked, both rows
  kept, FW-TIES).  Channel (a) reads transports only and is decided
  within the phase-2/3 bounds; channel (b) reads amps only and is the
  sign-repair rung's certificate criterion (per-magnitude domination,
  repaired exact iff `certificate_iff_dominated` and its two
  constructive converses cited as CONDITIONAL_THEOREM, reconstructed
  as computation) on the FULL closed-walk weight list from the declared
  least base object at bound 6 -- no enumerated walk discarded, the
  pinned discard countermodel binds.  Result: 10 decided rows are
  all cell `both`; 1 row (`square_plus_edge_occ3`'s variant) is
  NOT_COVERED_BY_BOUND on (a), which is not a "no".  No decided row
  separates the channels, so the separation is REFUSED with the table
  as the record -- and the reason is named, not smoothed: every walk
  magnitude on this census is 1, and at a single magnitude one side
  always dominates, so channel (b) cannot refuse anything here.  The
  channels are not claimed to be one repair; they read disjoint
  ingredients, and a census with magnitude diversity is the priced
  leftover (LP4).
- REGISTER_WRITTEN (FINITE_COMPUTATION): 9 rows, one per obstructed
  member, each with its cure data (phase-2 price, phase-3 terminal, or
  the named bound refusal), its channel cell, and its priced
  leftovers, executed nowhere.
- TIES_RETAINED: prices carry tie counts; witnesses are "first in the
  deterministic order", named as such, never "the" witness.
- PREDICTIONS_HASHED: the two freeze hashes above, both recorded in
  `SOURCE_MANIFEST.json` and checked by `verify_pins.py`.
- SS09_PARTIALLY_CLOSED: exactly A9's form -- the two-label half of
  SS-09 closes with `slot_group_sections`; the larger-fibre half stays
  OPEN (LP3).  Nothing stronger is claimed anywhere in this tree.
- MANUAL_RECEIPT_DECLARED: no CI gate reads this tree's receipts,
  scans, or Lean audit.  `verify_lean.py` is a manual receipt in the
  same sense as the other research trees'.
- OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED: the three protected
  opens are untouched; `test_forbidden.py` fails the run on any claim
  to the contrary.
- FW_SET_HELD: no completed-classification sentence appears in this
  tree; the census is the declared slice, consumed under pin.

## Evidence classes and the Lean scoping statement

Unlike sign_slice, this tree DOES originate theorem-level claims, and
carries its own self-contained Lake package (`lean/`, core Lean only,
no sealed import, no staging) to prove them: the four theorems above
plus their bookkeeping lemmas, 18 reports, whitelist
`{propext, Quot.sound}`.  Every theorem is TWO-LABEL (FW-SCOPE); the
six-label result is FINITE_COMPUTATION at its declared bound and is
not a theorem here; the price closed form is CONJECTURE; citations
into the pinned trees (the section criterion, the repaired exact
pairing iff and both constructive converses, the discard countermodel)
remain CONDITIONAL_THEOREM and were not re-proved,
except where re-proving abstractly was the point (FW-T1 and
`pointwise_parity_blind`).

## The injection record

Every verifier in this tree was proved by failing on the exact defect
it exists to catch, then recovering on reversal.  Receipts were never
regenerated while an injection was live.

| Gate | Injection | Observed failure |
|---|---|---|
| Pin integrity (original pre-rebase injection) | first digit of the `genpres.py` pin flipped | `FAIL: research/sign_slice/genpres.py blob at b57fb08... is a69a2a4c..., pinned 069a2a4c...` at snapshot AND at HEAD; exit 1, then 0 after reversal |
| Predictions freeze | one probe line appended to `PREDICTIONS.md` | `FAIL: PREDICTIONS.md hash f5cd1f46... differs from the last recorded freeze 8c6691c8...`; exit 1, then 0 after reversal |
| Lean forbidden tokens | a comment carrying the first forbidden token appended to `Promotion.lean` | `FAIL: Promotion.lean contains forbidden token` naming it; exit 1, then 0 after reversal |
| Receipt replay | `flip_count` 10965 changed to 10964 in the committed receipt | `test_sixlabel_exhaustion_replays_the_receipt`: `10965 != 10964 : flip_count`; exit 1, then 0 after reversal |
| Supplied-name scan | scratch file with a supplied token in the write root | `AssertionError: ... unexpectedly found ... zzz_probe.txt`; exit 1, then 0 after deletion |

Two defects were also caught LIVE during construction, before any
receipt existed, and repaired: the word "admits" in a Lean docstring
tripped the substring scan (reworded), and the primed theorem names
(`xor_self'` and kin) defeated a `'[^']*?'` report capture -- the
repository's recorded primed-names parser defect, reproduced
independently here and repaired with `'(.+?)'` at birth.  A third
defect crashed the first full run: this tree and the pinned sign_slice
tree both carry a `register` module, and the pinned one shadowed this
one on the import path -- the run crashed on arity rather than
computing anything wrong, and the path order is now this-tree-first
with the hazard named in both entry points.

## What this run does NOT claim

No sentence here answers the supplied challenge (A2: two labels,
declared bounds, a slice).  The six-label result does not extend by
analogy anywhere (A3).  Price 2 is not universal, and price 1 is not
either -- the map is per member (A4).  A green Lean build discharges
no computational claim and no receipt proves a theorem (A7, A10).
Unit-weight members needed no curing on the weight side all along --
their full walk lists are single-signed, recorded per member (A6).
The two repair channels are not one repair, and this census cannot
separate them; the refusal names its own degeneracy (A5).  The
completed classification is refused (A8).  The full adversarial
dispositions A1-A10 are in the receipt under `adversarial`.

## The registration diff this tree does NOT apply

Adding this tree to the research job would be the following step in
`.github/workflows/verify.yml`, recorded here as text and not applied
(registration is an author act):

    - name: convention_price pins and tests
      run: |
        python research/convention_price/verify_pins.py
        python -m unittest discover -s research/convention_price -p "test_*.py"

## Commands (run from this directory)

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 23 sources at snapshot and HEAD; native PROMPT.md frozen; 2 predictions freeze(s) recorded` |
| `python verify_lean.py` | 0 | `lean audit clean: 5 sources, 18 axiom reports, axioms within ['Quot.sound', 'propext']` |
| `PYTHONDONTWRITEBYTECODE=1 python run_convention_price.py --out receipts` | 0 | `sixlabel: SIXLABEL_MOVES, flips 10965, price 1`; `channels: CHANNELS_AGREE_ON_DECIDED_ROWS`; `register rows: 9` |
| `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | all tests pass, refusal scans included |
| `python -m mypy` | 0 | strict, all source files |

## Source pin semantics (2026-09-22)

By the author's ruling, `verify_pins.py` separates two claims it used to
merge. Provenance still fails: the 23 pinned blobs at the snapshot, the frozen
native `PROMPT.md`, and the last recorded predictions freeze. Currency is now
reported: a pinned source that differs between the snapshot and HEAD prints as
a `DRIFT:` line with a count, and no longer fails. `--require-current` restores
the old failure.

Why: the snapshot blob is fixed history, so once `CLAUDE.md`, the two
`natural_sections` documents and the two `sign_slice` files changed, no repin
could satisfy both sides, and this check was red for that reason alone. What
this tree claims is about its snapshot, and that is what the check enforces.
