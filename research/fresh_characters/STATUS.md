# fresh_characters: the layer's characters and their fresh totals

Chain step 4, after sign_slice, convention_price, and balance_carrier. This
run executes the rung balance_carrier named and did not start: the signed
total, over the fresh members of a layer, of one of that layer's characters.

`AuthorityEffect: None.`

The growth of the running balance is a protected open of this run. No
sentence here is about how it behaves past the last computed checkpoint, in
either direction.

## Frozen inputs

Native `PROMPT.md` sha256
`d45ba3e4827806458f19d3ec7d7ce8b4b474aab51a1a11d50d5a8b8b03d78348`.
Predictions frozen at
`aeb3d7728e98c98e1d2a00cd22145d5f198d8af9b0df28b63b301bb03534699f`
(freeze 1, stages 1 to 3) and
`aa37d38170d20a3978331bab7e297a199c1e9c1c1d648ff2ef4c4a61d83a2abe`
(freeze 2, stages 4 and 5). Sources are pinned in `SOURCE_MANIFEST.json` at
snapshot `f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`;
`verify_pins.py` checks eleven blobs, three spans, and three exact source
projections at the snapshot and at `HEAD`.

## Declared readings, recorded and not silently chosen

1. **FW-LEAD is BREACHED for this run, and the breach is this session's.**
   The charter says the author's expectation is sealed and the run never sees
   it. The plaintext of that sealed file was **written by this same session,
   earlier the same day, when the operator packet was drafted**. So the
   blindness the outside-bet mechanism assumes did not hold here. What
   remains true and checkable: the commitment hash in
   `SOURCE_MANIFEST.json` matches the file the author holds, the file was not
   reopened during the run, and every branch of stages 2 and 4 was written
   into `PREDICTIONS.md` as a pre-agreed terminal. What is no longer true is
   that the run was blind to the expectation. **The author should score this
   run's bet as void, or score it knowing this.** Recorded here rather than
   left for a reader to infer from the session history.
2. **The freeze order was violated for the Lean half of stages 1 to 3.** The
   Lean package was written and built before `PREDICTIONS.md` existed. Freeze
   1 therefore records those decided values under "already obtained" and
   predicts only the Python side, which had not run. Freeze 2 is prospective
   without exception: it was hashed before `magnitude_census.py` existed and
   before any census value was computed. The defect is in the order, not in
   the values.
3. **A sixth menu member was added at freeze time.** The operator's menu named
   five carriers and said "at least these five". V4 quotients by the total of
   ALL members; this tree's own vocabulary distinguishes all members from
   FRESH members, so the sibling quotient — by the layer's fresh part,
   defined by the same divisor recursion the pinned balance uses — is the
   obvious sixth, and omitting it would have been a gap in the menu rather
   than a discipline. It is V6, and it is the member that met stage 2.
4. **Two family kinds are censused in stage 4, and the reason is structural.**
   The certificate criterion reads a list of integers. Under V6 the terms of
   one total are members of the value carrier, not integers, so the term list
   of a single total is not a list the criterion can read. The declared
   substitute, fixed in freeze 2 before any census ran, is the ROW family:
   the totals at every step of one layer. Both kinds are censused and every
   terminal says which kind it belongs to.
5. **The direct cross-check bound is 600, not the 10000 the operator asked
   for.** Reducing a total costs roughly the cube of the part count in this
   implementation: `400` takes about eight seconds and `1000` is out of
   reach. The totals are therefore recomputed directly to `600`; the pinned
   running-balance checkpoints to `1000000` are recomputed from the BALANCE
   recursion alone, which is the pinned object, and no sentence says the
   totals were recomputed there.
6. **Source policy: verbatim reconstruction.** `Receiver.lean` and
   `Balance.lean` are byte-identical to balance_carrier's reconstructions
   apart from the outer namespace, the snapshot id in the pin note, and the
   tree's name; both are verbatim from the same pinned blobs, and
   `verify_pins.py` checks the projection against the pinned source rather
   than against the sibling. `Steps.lean` is new here and reconstructs the
   pinned step action.
7. **The fresh-part module is named for the fresh part.** An earlier draft
   named it after the outside object it computes; that name was a fragment of
   an outside word and was replaced before anything was committed. The module
   is `FreshPart.lean` and the name describes what the divisor recursion
   produces.
8. **Two balance routes.** The pinned recursion is implemented literally in
   `balance_table_reference` and forward-accumulated in `balance_table`; the
   two are cross-checked to part count `300` by test, and only the fast route
   can reach `1000000`.

## Terminals, each with its scope

- **CHARACTERS_DEFINED** (PROVED_THEOREM): all four stage-1 targets proved in
  core Lean, for EVERY part count, carrier-free on the exponent word —
  `characters_are_steps` (every step below a positive part count supplies a
  character, distinct steps give distinct words, every character agrees on
  the layer members with one step's word, and the count is the part count),
  `freshExp_wf` (the total is a function of the receiver element, resting on
  the pinned `fresh_rep_unique`), `freshExp_zero` (the step-zero total is the
  fresh count many copies of the carrier's unit), and `exponent_embed` (the
  restriction along a divisor arrow). The counting law `freshExp_length` is
  proved too, and so is the V1 obstruction:
  `additive_trivial_total_ne_freshCount`. 19 axiom reports in the package,
  all within `{propext, Quot.sound}`, 2 axiom-free. Python recomputation of
  the carrier-free targets: `0` misses at every part count to `60`.
- **TOTAL_IDENTITY_BOUNDED** (FINITE_COMPUTATION), with **TIES_RETAINED**:
  exactly two of the twenty-four declared pairs make the fresh total the
  balance at every part count `1..60` — the fresh-part carrier at the unit
  step, and the same carrier at the step one below the part count. Both are
  carried through every later stage and neither is called the carrier. Direct
  recomputation to `600`: `0` misses. Kernel-decided in Lean to `20`. The
  general identity is CONJECTURE and is stated as one.
- **NO OTHER CARRIER MEETS THE STAGE.** The additive receiver never produces
  an integer total. The unit-value carrier totals the fresh count at every
  step, so it matches only at part count `1`. The sign carrier is defined
  only at even part counts. The free carrier and the all-members quotient
  fail to reduce to an integer: the all-members quotient first fails at part
  count `4`, and its best agreement is `17` of `60`.
- **RECURSION_BOUNDED** (FINITE_COMPUTATION): for the fresh-part carrier, the
  divisor sum of the totals is the part count at the zero step and vanishes
  at every other step, over the whole rectangle to `60` with `0` misses, and
  kernel-decided in Lean to `16`. At the unit step and a part count above one
  this reproduces the pinned `balance_divisor_sum`, checked rather than
  assumed. The unit-value carrier fails the recursion (1770 misses) and the
  sign carrier is undefined on 1830 cells; both are recorded, not dropped.
  The determination question — whether a total depends on the step only
  through the largest divisor shared with the part count — holds with `0`
  counterexamples for all three integer-valued carriers over the rectangle,
  and is kernel-decided to `20`. Its general form stays CONJECTURE.
- **DIVERSITY_EXHIBITED** and **CERTIFICATE_REFUSED** (FINITE_COMPUTATION),
  the LP4 rung, each with its family kind named:
  - *Term families*: 2760 in the rectangle, every one carrying exactly one
    magnitude, no diversity and no refusal. At this level LP4 is carried
    forward unchanged, and it is said exactly that way.
  - *Row families*: 150 in the rectangle, 54 of them carrying two or more
    magnitudes, 25 distinct magnitudes seen, the smallest diverse family at
    part count `3`. **LP4 has moved at this level.**
  - *Refusals*: 29 row families admit no cancellation certificate. The
    smallest is at part count `3` with terms `[2, -1, -1]`, total `0`. It
    cancels exactly, and no pairing into exact opposites plus a single-signed
    residual exists: at magnitude `1` there are two negatives and no
    positive, at magnitude `2` one positive and no negative, so neither side
    dominates. This is the first family in this chain on which the pinned
    criterion says no.
  - Recorded as an observation of the rectangle and nothing more: every
    refusing row sits at an odd part count, `3` through `59`, and no even
    part count refuses. Absence of a refusal outside the rectangle is not
    absence of a refusal (FW-SET).
  - The criterion against the brute-force search: `0` disagreements on the
    whole rectangle and on every list over `{-2..2}` of length `5`.
- **REGISTER_WRITTEN** and **GROWTH_OPEN_UNCHANGED** (FINITE_COMPUTATION,
  mandatory): six menu rows, five leftovers named and priced, and the pinned
  running-balance checkpoints reproduced exactly at
  `10, 30, 100, 1000, 10000, 100000, 1000000` — `-1, -3, 1, 2, -23, -48,
  212` — with no sentence anywhere in this tree about the behaviour past the
  last checkpoint.
- **OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED**:
  the protected opens are untouched, and `test_forbidden.py` fails the run on
  a claim to the contrary.
- **FW_SET_HELD, FW_NAME_HELD**: no completed-classification sentence and no
  outside name appears in this tree; the census scanner of `ci/` finds no
  watched word in the write root and the pin was not regenerated.
- **MANUAL_RECEIPT_DECLARED**: no CI gate reads this tree's receipts, scans,
  pins, or Lean audit. `verify_lean.py` and `verify_pins.py` are manual
  receipts in the same sense as the other research trees'.

## The two conjectures, stated as conjectures

For every part count, the fresh total under the fresh-part carrier at the
unit step equals the balance — CONJECTURE. The same at the step one below the
part count — CONJECTURE. Support: exhaustive agreement over the declared
menu at `n ≤ 60`, direct agreement at `n ≤ 600`, kernel-decided agreement at
`n ≤ 20`, and the divisor recursion of the totals decided at `n ≤ 16`. The
mechanism the evidence points at — that the divisor recursion of the fresh
parts mirrors the divisor recursion the pinned `balance_unique` characterises,
so the totals and the balance satisfy the same recursion with the same value
at part count one — is a METATHEORY reading and is not a theorem of this
tree. Its price: a Lean proof that the fresh parts multiply back to the
layer's difference for every part count, which this tree carries only as
decided instances, followed by the pinned uniqueness applied to the totals.

## Predictions, disposed

| prediction | disposition |
|---|---|
| P1.1 | CONFIRMED: `0` misses at every part count to `60` |
| P1.2 | CONFIRMED: V1 fails the trivial total at every part count; V5 is defined only at even part counts; V2, V3, V4, V6 satisfy every target where defined; no member dropped |
| P2.1 | **MISSED in part**: the prediction said exactly one pair would match. **Two** did — the fresh-part carrier at the unit step AND at the step one below the part count. The frozen text's own tie clause fires and both are retained. The value stands; the count was wrong |
| P2.2 | CONFIRMED: the unit-value carrier matches only at part count `1`; the sign carrier totals plus or minus the fresh count; the free carrier and the all-members quotient fail to reduce, the latter first at part count `4` |
| P2.3 | **MISSED as stated**: the prediction named a direct recomputation to `10000`. The reduction is roughly cubic and `10000` is out of reach; the direct bound is `600` and the checkpoints beyond it are recomputed from the balance recursion alone. `0` disagreements at either bound. The declared reading is recorded above |
| P2.4 | CONFIRMED: `TOTAL_IDENTITY_BOUNDED`, Lean bound `20` (better than the `at least 6` the sibling rung managed), no general theorem attempted |
| P3.1 | **MISSED as stated**: the prediction did not name a carrier, and the divisor sum holds only for the fresh-part carrier. The unit-value carrier misses it 1770 times and the sign carrier is undefined on 1830 cells. For the fresh-part carrier: `0` misses over the rectangle |
| P3.2 | CONFIRMED: `0` counterexamples over the rectangle for all three integer-valued carriers |
| P3.3 | CONFIRMED: no closed form is claimed |
| P4.1 | CONFIRMED: every one of 2760 term families carries one magnitude |
| P4.2 | CONFIRMED: 54 diverse row families; smallest witness at part count `3` |
| P4.3 | **MISSED as stated**: the prediction said every row family totals to zero above part count one. The unit-value carrier's rows do not (59 misses); the sign carrier's and the fresh-part carrier's rows do. The value stands; the quantifier was wrong |
| P4.4 | CONFIRMED, and it is the sharpest result of the run: 29 refusals, the smallest at part count `3` |
| P4.5 | CONFIRMED: `0` disagreements between the criterion and the brute-force search |
| P5.1 | CONFIRMED: six rows |
| P5.2 | CONFIRMED: `GROWTH_OPEN_UNCHANGED`, no growth sentence, and the scan fails the run on one |
| P5.3 | CONFIRMED: five leftovers, none started |
| P5.4 | CONFIRMED: no protected open closed |

Four predictions missed. None was edited; each is recorded next to its value.

## The injection record

Every verifier was proved by failing on the exact defect it exists to catch,
then recovering on reversal. No receipt was regenerated while an injection
was live.

| Gate | Injection | Observed failure |
|---|---|---|
| Pin integrity | first digit of the pinned `LayerBalance.lean` blob flipped in `SOURCE_MANIFEST.json` | `FAIL: research/natural_sections/lean/NaturalSections/LayerBalance.lean blob at f4b1dcd... is 493bdc27..., pinned 093bdc27...`; exit 1, then 0 after reversal |
| Span pin | leftover 1's line range moved to `351-358` | `FAIL: span research/balance_carrier/STATUS.md:351-358 at f4b1dcd... hashes e9595854..., pinned d3d8d6ff...`; exit 1, then 0 after reversal |
| Predictions freeze | one probe line appended to `PREDICTIONS.md` | `FAIL: reconstructed predictions freeze 2 hashes 6c0a6432..., recorded aa37d381...`; exit 1, then 0 after reversal |
| Lean forbidden token | a comment carrying the first forbidden token appended to `Steps.lean` | `FAIL: Steps.lean contains forbidden token sorry`; exit 1, then 0 after reversal |
| Receipt replay | the committed refusal count changed from `29` to `30` in `receipts/fresh_characters.json` | `test_committed_receipts_replay_byte_for_byte` fails; exit 1, then 0 after reversal |
| Census scan (FW-PIN, FW-NAME) | a probe file carrying a watched noun placed in the write root | `AssertionError: Lists differ:` a one-element list naming the probe file, its line, and the watched token, against the empty list; exit 1, then 0 after deletion. The token is described and not reproduced, because this file is itself scanned |
| Growth sentence (FW-GROWTH) | a sentence appended to `CLAIM_LEDGER.md` asserting a constant bound on the running balance, using one of the scanned phrases | `CLAIM_LEDGER.md carries a growth sentence:` followed by that phrase; exit 1, then 0 after reversal. The phrase itself is described and not reproduced here, because the scan cannot tell a quoted phrase from an asserted one and this file is scanned |
| Outside-root check (FW-SHARE) | synthetic porcelain records only, as in the sibling tree: writing a real probe outside the write root would itself breach FW-SHARE | `outside_write_root` returns the outside records and nothing for a path inside; `test_outside_write_root_check_is_a_pure_function_of_the_porcelain` |

Defects caught LIVE during construction, before anything was committed, and
repaired:

1. **The census caught a Lean hypothesis name.** `additive_step_zero_total`
   took a hypothesis whose name was a bare three-letter identifier with no
   underscore, so it read as prose — and that token is watched. The
   scan named the file and both lines on its first run over the write root.
   The hypothesis was renamed to one carrying an underscore, which is exempt
   by construction. The pin was NOT regenerated.
2. **A module was named after the outside object it computes.** Caught by
   reading, not by a gate — the name was a fragment of an outside word, so no
   scan fired. Renamed to `FreshPart` before commit, and recorded as declared
   reading 7 because a reader should know a gate did not catch it.
3. **The axiom-report list and the report text disagreed.** The report names
   are fully qualified and the list was written under an `open`, so every one
   of the eighteen failed in both directions at once. The list is now written
   fully qualified, which is the form the audit diffs.
4. **Three Lean tactics were not in core.** `conv_lhs`/`conv_rhs` and one
   library lemma name; replaced by explicit rewrites. Recorded because the
   package must build on core Lean with no library beyond it.

## What this run does NOT claim

No sentence answers the growth question in either direction (FW-GROWTH). The
characters, the carriers, and the totals are named by the descriptions they
are, and no outside name appears (FW-NAME). Agreement to a bound is
FINITE_COMPUTATION within that bound and every sentence carries it
(FW-SCOPE). The menu is declared and finite; it is not a classification of
value carriers and none is claimed (FW-SET). A refusal is a decision of the
pinned criterion on one named family, and says nothing about a family outside
the rectangle. The criterion itself is CONDITIONAL_THEOREM, cited by pin and
reconstructed as computation. Lean proves; the receipts record. Nothing
outside `research/fresh_characters/` was written. And the sealed bet was not
blind to this run — see declared reading 1.

## Leftovers, named and priced, executed nowhere

1. **The general total identity** — CONJECTURE, bounded evidence only; price
   stated above.
2. **The enlarged menu** — OPEN: value carriers beyond the six and step rules
   beyond the four are unsearched. Absence of a search is not absence of a
   total.
3. **LP4 at the term level** — OPEN: the diversity found here is at the row
   level; at the term level every family in the rectangle still carries one
   magnitude, and nothing here moves that question. Its price is a carrier
   whose character values are integers of more than one magnitude.
4. **The certificate channel on the refusing rows** — OPEN, and this is the
   leftover the channel comparison priced. The refusals are decisions of one
   criterion on named families; what another declared repair channel does
   with them, and whether a refusing row admits a repair of some other
   declared kind, is not asked here. This run is the first with material to
   pay that price and it does not pay it.
5. **The next rung, named so it cannot be smuggled in later**: how the totals
   of two characters of the same layer combine against each other, and
   whether a function on a layer is recovered from the totals of all its
   steps. Named, not started. Its price is a declared product on the value
   carrier, a Lean statement of the combined total, and a frozen prediction
   before any value is computed.

## The registration diff this tree does NOT apply

Adding this tree to the research job would be the following step in
`.github/workflows/verify.yml`, recorded here as text and not applied;
registration is an author act and the shared files are frozen for both
parallel tracks:

    - name: fresh_characters pins and tests
      run: |
        python research/fresh_characters/verify_pins.py
        python -m unittest discover -s research/fresh_characters -p "test_*.py"

## Parallel-track note

A run with write root `research/described_replay/` may be live on its own
branch. This tree pins `main` at one exact snapshot, never that branch, and
wrote nothing outside its own write root. Every pull request targets `main`
directly, as `CLAUDE.md` requires.

## Commands (run from this directory unless noted)

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 11 sources and 3 spans at snapshot and HEAD; sealed prefixes unchanged; nothing outside the write root; 3 source projections exact; native PROMPT.md frozen; 2 predictions freezes reconstructed` |
| `python verify_lean.py` | 0 | `lean audit clean: 8 sources, 19 axiom reports (2 axiom-free), axioms within ['Quot.sound', 'propext']` |
| `python run_fresh_characters.py --out receipts` | 0 | `stage 2: TOTAL_IDENTITY_BOUNDED, hits ['V6/R1', 'V6/Rlast']`; `stage 4: ['DIVERSITY_EXHIBITED', 'CERTIFICATE_REFUSED']` |
| `python -m unittest discover -s . -p "test_*.py"` | 0 | all tests pass, refusal scans included |
| `python -m mypy` | 0 | strict, all source files |
| `python ci/check_prose_watchlist.py` (repository root) | 0 | clean without a repin |

## Source pin semantics (2026-09-22)

By the author's ruling, `verify_pins.py` separates two claims that it used to
merge.

- **Provenance, which still fails.** The pinned blobs and spans at the
  snapshot, the exact source projections, the frozen native `PROMPT.md`, the
  recorded prediction freezes where this tree has them, and the rule that the
  worktree carries nothing outside the write root.
- **Currency, which is now reported.** That nothing pinned has moved between
  the snapshot and HEAD is printed as `DRIFT:` lines, followed by a
  `drift since the snapshot:` count. It no longer fails. Pass
  `--require-current` to restore the old failure.

Why the change: the snapshot blob is fixed history, so once the author edited
a sealed or contract file, no repin could satisfy both sides, and this check
had been red for weeks for that reason alone. What this tree claims is about
its snapshot, and that is what the check now enforces.

The `python verify_pins.py` row in the commands table above records a run made
under the earlier wording, and is kept as the dated record of that run.
