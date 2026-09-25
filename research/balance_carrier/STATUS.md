# balance_carrier: the balance carrier

Three named leftovers were consumed, pinned in `PROMPT.md` from their own
trees: the natural_sections layer-balance registration (the growth OPEN
and the named NEXT question, quoted by pin because its span carries a
word the census watches), the convention_price CHANNELS terminal (LP4,
magnitude diversity), and the layer-balance receipt with its
kernel-decided checkpoints.  This tree builds the observer that grades
the layers and proves it in core Lean; declares a finite class of signed
counts on the divisor family and searches it exhaustively for the running
balance; prices LP4 on the carriers' own signed families; recomputes the
running balance three ways at the pinned checkpoints; and registers the
leftovers, the next rung among them, executed nowhere.

The growth question is a protected open of this run.  No sentence here is
about how the running balance behaves past the last computed checkpoint.

## Frozen inputs

Native `PROMPT.md` sha256
`ef50dbe708942458876d21a3219b1afa740da6de68edff9cc77021b81f1813fb`;
predictions frozen at
`83e7ab7cfd3c929613b580c230c39a199383d77050a478dfdd91deace37b3828`
(stages 1-2, before any stage computation and before the first compile)
and
`626936375324eead6d3444959d442e32eca2f86d27e6742de57db4926f0d5f6e`
(stages 3-5, after stage 2 closed and before any stage-3 computation).
`verify_pins.py` reconstructs and hashes both content states from the final
append-only file.  It does not provide an external timestamp, so the stated
before/after chronology remains an operator report rather than a receipt.
Sources are pinned in `SOURCE_MANIFEST.json` at snapshot
`be7476868e496e06d5dec6599fa4346394c512bd` of `main`; `verify_pins.py`
checks the eight blobs and the two spans at the snapshot, and reports any
that have moved at HEAD without failing (see the dated note at the end of
this file).
The parallel track (`research/role_census/`) was live on its own branch
when this run started; this tree pins `main`, never that branch, and read
nothing from it.  One prediction missed (P3.5); it is recorded below next
to its value and was not edited.

## Declared readings (recorded, not silently chosen)

1. **Source policy for stage 1** (recorded here and in the frozen
   `PREDICTIONS.md` before the first compile): the pinned definitions
   are RECONSTRUCTED VERBATIM into this tree's own package
   (`lean/BalanceCarrier/Receiver.lean`, `lean/BalanceCarrier/Balance.lean`),
   each file carrying a pin note with the pinned path and blob id; the
   one change is the outer namespace.  No sibling package and no sealed
   module is imported.  Theorems whose proof text is reproduced are
   CONDITIONAL_THEOREM; theorems originating here are PROVED_THEOREM.
2. **The observer's formula.**  The charter names the observer by what
   it reads (the part count of the fresh representation) and not by a
   formula.  Reading: on a raw pair `(n, k)` the value is
   `(k + 1) / gcd(n, k + 1)`, lifted through the quotient once
   `layer_observer_wf` licenses the lift.
3. **The declared arrow and step for `layer_observer_grades`.**  The
   divisor arrow `d -> m` with `m = q * d` carries a part `c` fresh at
   part count `d` to the part `q * c` of part count `m`; the declared
   statement is that the observer's value at the image is `d`.
4. **Orientation of the stage-2 table.**  Rows are sources, columns are
   targets; `T(1, 1)` is the diagonal value; the declared first column
   applies to rows `2..N`.
5. **Sections in S3.**  A section assigns to every object `2..N` one
   arrow into it; the signed count is the sum over sections of the
   product of the chosen arrows' weights, enumerated, not factored.
6. **A fourth count, S1b.**  The prompt asks for "at least these three"
   counts; the totalled walk sum (S1 summed over every endpoint `1..N`)
   was added to the menu before any computation, in the frozen
   `PREDICTIONS.md`.
7. **The fastest exact route.**  For a table whose diagonal is `1` or
   `-1`, the first column is reduced by the other columns to a
   triangular table whose alternating sum is its diagonal product.  Two
   elementary facts about the alternating sum over bijections are used
   (column operations preserve it; a triangular table's is its diagonal
   product); both are METATHEORY here, not proved in this tree, and the
   route is cross-checked against the literal alternating sum where that
   is affordable and against fraction-free elimination beyond it.
8. **Span pins.**  A consumed leftover is pinned as a line range of a
   pinned file; the hash is the SHA-256 of those lines joined with LF,
   trailing LF included, as stored in the pinned blob.
9. **Kernel-decided bound.**  The Lean instances of the table count
   reach whatever `N` the kernel decides within the run; the bound
   reached is written into each statement and nowhere extended.
10. **Certificate reconstruction.**  `certificate_iff_dominated` is
    reconstructed as the computation "for every magnitude present, the
    count of `-v` is at most the count of `v`, or the reverse holds for
    every magnitude present"; the pinned fixtures (the wedge without a
    certificate, the witness with one) are re-decided by it.
11. **The literal route, appended after stage 2 ran.**  The frozen
    predictions declared the unpruned alternating sum over all `N!`
    arrangements for `N <= 9` and elimination for `10..12`.  The
    unpruned loop cost 224 seconds over the menu; the same count with
    the arrangements that meet a zero entry pruned (they contribute `0`)
    runs in under a second at every `N <= 12`, so the search values are
    the pruned literal count at all twelve `N`, checked against
    elimination at all twelve and against the unpruned loop at `N <= 8`.
    A route change, not a value change: every value agreed.

## Terminals, each with its scope

- LAYER_OBSERVER_PROVED (PROVED_THEOREM): in core Lean, on the verbatim
  pinned receiver -- `layer_observer_wf` (two raw pairs naming one
  element have one raw value, via the explicit fresh representative
  `red_same` / `red_fresh` and the pinned `fresh_rep_unique`),
  `layer_observer_constant` (the value is `k + 1` on every fresh member
  of layer `k`), `layer_observer_separates` with `layer_observer_separates'`
  (equal values at fresh members force equal part counts), and the
  optional `layer_observer_grades` in the declared form (a fresh part
  carried along the divisor arrow reads its source part count at the
  image; `partCount_layer_image` puts it on the receiver through the
  pinned `layer_mul_compat`), plus `observer_value_divides` (the value
  divides the part count it is read in).  58 `#print axioms` reports in
  the package, all within `{propext, Quot.sound}`, 11 axiom-free; the
  observer's own theorems report `[propext, Quot.sound]`.  Computationally
  (L6): `0` misses against a brute-force fresh-representation search on
  every raw pair `n <= k <= 40` and on wrapped pairs to `k <= 24`;
  values on fresh members of part counts `1..12` are exactly the part
  count; the grading holds for quotients `1..6`.
- CARRIER_IDENTITY_PROVED (PROVED_THEOREM) for `S1b(W2)`: the totalled
  walk sum with weight `-1` on every arrow equals the running balance at
  every `N` -- `totalWalkSum_neg_one_eq_runningBalance`, from
  `walkSum_neg_one_eq_balance` (the walk sum has value `1` at part count
  `1` and vanishing divisor sums, so the pinned `balance_unique`
  identifies it with the balance at every part count `>= 1`).  The chains
  are explicit lists computed with fuel and proved fuel-stable
  (`chainsFuel_stable`), and the recursion `walkSum_succ_succ` is proved
  from the chain structure (`chains_succ_succ`, `chains_head`), not
  assumed.  Ties retained: this is one of three carriers meeting stage 2.
- CARRIER_IDENTITY_BOUNDED (FINITE_COMPUTATION) for `S2(W1,1,C1)` --
  unit arrow weights, unit diagonal, unit first column -- and for
  `S2(W3,1,Cbal)` -- balance-of-quotient arrow weights, unit diagonal,
  balance first column.  Both equal the running balance at every
  `N <= 12` (exhaustive menu search, the pruned literal count agreeing
  with fraction-free elimination at every `N <= 12`); kernel-decided in
  Lean for `N <= 7` (`unit_table_matches_to_7`,
  `balance_table_matches_to_7`, axiom-free reports); by the column route
  at every `N <= 1000`, at the stepped checkpoints `2000..10000`, and at
  the pinned checkpoints `100000` and `1000000`; the unpruned alternating
  sum agrees with the pruned one at `N <= 8` and the pruned one with
  elimination and the column route at `N <= 60`; `0` misses anywhere.
  The general identity is CONJECTURE (below), stated nowhere as a
  theorem.  Recorded, not claimed: a probe of the unit table at `N = 8`
  compiled outside the package with `maxRecDepth 1000000` and
  `decide +kernel` succeeded in 3 minutes 53 seconds; inside the package
  at `maxRecDepth 100000` the kernel refused `N = 8` by deep recursion,
  and the package keeps `N <= 7` (37-second build).  The probe is not in
  any axiom report and is not a theorem of this tree.
- NO S1 AND NO S3 CANDIDATE meets stage 2: S1 with weight `-1` equals
  the BALANCE (P2.1, proved), not the running balance; the best S1
  agreement is at two of twelve `N`; the best S3 agreement (`S3(W3)`) is
  at four; the best non-meeting S2 candidates (`S2(W2,-1,C-1)`,
  `S2(W4,-1,C-bal)`) agree at the six even `N` only, where their sign
  matches.  87 of 90 candidates do not meet stage 2; the receipt lists
  every value.
- DEGENERACY_PERSISTS (FINITE_COMPUTATION): for each of the three
  carriers at `N` in `{6, 7, 12}`, every term magnitude is `1`; the
  family totals equal the running balance; the certificate criterion
  finds a certificate on every row (at one magnitude one side always
  dominates -- the non-positive-residual side, here, at every row), so it
  refuses nothing.  LP4 is carried forward unchanged: a census with
  magnitude diversity is the priced leftover, again.

  | carrier | N | terms | positive | negative | total |
  |---|---|---|---|---|---|
  | `S1b(W2)` | 6 | 9 | 4 | 5 | -1 |
  | `S1b(W2)` | 7 | 10 | 4 | 6 | -2 |
  | `S1b(W2)` | 12 | 28 | 13 | 15 | -2 |
  | `S2(W1,1,C1)` | 6 | 9 | 4 | 5 | -1 |
  | `S2(W1,1,C1)` | 7 | 10 | 4 | 6 | -2 |
  | `S2(W1,1,C1)` | 12 | 28 | 13 | 15 | -2 |
  | `S2(W3,1,Cbal)` | 6 | 7 | 3 | 4 | -1 |
  | `S2(W3,1,Cbal)` | 7 | 8 | 3 | 5 | -2 |
  | `S2(W3,1,Cbal)` | 12 | 12 | 5 | 7 | -2 |

  Recorded, not claimed: the `S1b(W2)` family and the unit table's
  family have the same size and the same sign counts at every `N` shown
  -- the supported arrangements of the unit table and the chains to the
  endpoints `1..N` number the same and sign the same here.  That is the
  content of the conjecture below, observed at three `N`, proved nowhere.
- GROWTH_OPEN_UNCHANGED (FINITE_COMPUTATION, mandatory): at every pinned
  checkpoint the running balance recomputed directly (the pinned divisor
  recursion), through `S1b(W2)` (the walk-sum recursion), and through the
  unit table's column route agree with each other and with the pinned
  values.  The ratio of the absolute running balance to the square root
  of `N`, a checkpoint value at each `N` and nothing more:

  | N | running balance | squared ratio (exact) | ratio (six places) |
  |---|---|---|---|
  | 10 | -1 | 1/10 | 0.316227 |
  | 30 | -3 | 3/10 | 0.547722 |
  | 100 | 1 | 1/100 | 0.100000 |
  | 1000 | 2 | 1/250 | 0.063245 |
  | 10000 | -23 | 529/10000 | 0.230000 |
  | 100000 | -48 | 72/3125 | 0.151789 |
  | 1000000 | 212 | 2809/62500 | 0.212000 |

  The running maximum of the squared ratio over `2..1000000` is `4/5` at
  part count `5` (ratio `0.894427`), as pinned, and the square of the
  running balance is below `N` at every part count of that window -- a
  value about the window, not a bound.  No growth bound is claimed in
  either direction, and none is refuted (NS95_GROWTH_UNCHANGED).
- REGISTER_WRITTEN (FINITE_COMPUTATION): three rows (menu index, count,
  bound reached, Lean status, certificate cells), a summary of the 87
  non-meeting candidates by kind with their best agreement, and four
  leftovers named and priced, executed nowhere.
- TIES_RETAINED: three carriers met stage 2 at the same bound and all
  three are carried through stages 3-5; none is called "the" carrier.
- PREDICTIONS_HASHED: the two content-state hashes above, recorded in
  `SOURCE_MANIFEST.json` and reconstructed by `verify_pins.py`; their
  reported chronology is not promoted to a machine-verified claim.
- RECONSTRUCTIONS_BOUND: the selected `Receiver.lean` and `Balance.lean`
  declaration ranges are checked byte-for-byte against their pinned source
  blobs after only the declared outer-namespace rename.
- MANUAL_RECEIPT_DECLARED: no CI gate reads this tree's receipts, scans,
  or Lean audit.  `verify_lean.py` is a manual receipt in the same sense
  as the other research trees'.
  2026-09-24: withdrawn for the Lean audit only.  The `lean` job of
  `.github/workflows/verify.yml` now runs `verify_lean.py`; the receipts,
  the scans and `verify_pins.py` are still read by no gate.
- OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED:
  the three protected opens of the chain and the growth open of this run
  are untouched; `test_forbidden.py` fails the run on any claim to the
  contrary and on any growth sentence.
- FW_SET_HELD, FW_NAME_HELD: no completed-classification sentence and no
  outside name appears in this tree; the count is called the alternating
  sum over bijections (the signed expansion of the table) and nothing
  else; the census scanner of `ci/` finds no watched word in the write
  root and the pin was not regenerated.

## The conjecture (CONJECTURE, proved nowhere)

For every `N`, the alternating sum over arrangements of the unit table
with unit first column equals the running balance -- CONJECTURE.  The
same for the balance-weighted table with balance first column --
CONJECTURE.  Support: exhaustive agreement at `N <= 12`, kernel-decided
agreement at `N <= 7`, column-route agreement at every `N <= 1000` and
at the checkpoints to `1000000`, and the coincidence of family sizes and
sign counts with the proved `S1b(W2)` carrier at `N` in `{6, 7, 12}`.
The mechanism the evidence points at -- that a supported arrangement is
the identity or one cycle through column `1` whose entries form a chain
to its top, so the expansion totals the walk sums with weight `-1` -- is
a METATHEORY reading and is not a theorem of this tree.  Its price: a Lean
development of the alternating sum over arrangements (the sign under
composition, the cycle decomposition of a supported arrangement) that
this tree does not carry.  A1 and A4 bind: the conjecture, and even its
proof, would re-express the same signed sum and say nothing about growth.

## Predictions, disposed

| prediction | disposition |
|---|---|
| L1-L3, L5 | CONFIRMED: all three targets and the axiom whitelist, first build |
| L4 | RECORDED: `layer_observer_grades` proved in the declared form; not OPEN |
| L6 | CONFIRMED: `0` misses at every declared bound |
| P2.1 | CONFIRMED: `walkSum_neg_one_eq_balance`; S1 with W2 is the balance at `1..12` and not the running balance |
| P2.2 | CONFIRMED: `totalWalkSum_neg_one_eq_runningBalance` compiled; CARRIER_IDENTITY_PROVED |
| P2.3 | CONFIRMED: no S1 candidate meets stage 2 |
| P2.4 | CONFIRMED: exactly the two expected tables meet stage 2, no others |
| P2.5 | CONFIRMED: no S3 candidate meets stage 2 |
| P2.6 | CONFIRMED: `0` misses on every cross-check, to `1000000` |
| P2.7 | CONFIRMED: kernel-decided to `N <= 7` (at least `6` was expected); the general S2 identity is CONJECTURE |
| P2.8 | CONFIRMED: three carriers carried into stage 3 |
| P3.1-P3.4 | CONFIRMED: every magnitude `1`, totals equal the running balance, a certificate on every row, the pinned fixtures re-decided |
| P3.5 | MISSED: the prediction said some supported arrangements of `S2(W3,1,Cbal)` have a zero product and would be excluded with their count recorded; the recorded count is `0` at every `N`.  The enumeration walks nonzero entries only, so an arrangement meeting a zero balance entry is never produced -- it is absent from the family rather than excluded from it, which is why the balance table's family is smaller than the unit table's (`7` against `9` at `N = 6`, `8` against `10` at `7`, `12` against `28` at `12`).  The value stands; the prediction was wrong about the enumeration, not about the terms |
| P4.1-P4.4 | CONFIRMED: three-way agreement at every checkpoint, `4/5` at `5`, ratios recorded, GROWTH_OPEN_UNCHANGED |
| P5.1-P5.3 | CONFIRMED: three rows, four leftovers, no protected open closed, the classification refused |

## Evidence classes and the Lean scoping statement

This tree originates theorem-level claims and carries its own
self-contained Lake package (`lean/`, core Lean only, no sealed import,
no sibling import, no staging) to prove them.  The verbatim
reconstructions of the pinned receiver and balance are
CONDITIONAL_THEOREM (their proof text is the sibling's, compiled here so
the observer's theorems can be stated against the pinned definitions
themselves); the observer theorems and the walk-sum theorems are
PROVED_THEOREM; the table instances are kernel-decided FINITE_COMPUTATION
inside Lean with the bound in each statement; the general table identity
is CONJECTURE; the two elimination facts are METATHEORY; the certificate
criterion is CONDITIONAL_THEOREM, reconstructed as computation.  The
prompt's "at least N <= 30" for the Lean instances was not reached: the
kernel's depth limit stops the package at `7` in 37 seconds, and the
recorded probe reaches `8` in nearly four minutes; the bound is in every
sentence.

## The injection record

Every verifier in this tree was proved by failing on the exact defect it
exists to catch, then recovering on reversal.  Receipts were never
regenerated while an injection was live.

| Gate | Injection | Observed failure |
|---|---|---|
| Pin integrity | first digit of the `LayerBalance.lean` pin flipped in `SOURCE_MANIFEST.json` | `FAIL: research/natural_sections/lean/NaturalSections/LayerBalance.lean blob at be74768... is 493bdc27..., pinned 093bdc27...`; exit 1, then 0 after reversal |
| Span pin | leftover 1's line range moved to `1626-1633` | `FAIL: span research/natural_sections/STATUS.md:1626-1633 at be74768... hashes 883703bf..., pinned 6fb56d34...`; exit 1, then 0 after reversal |
| Predictions freezes | a probe byte changed in each reconstructed content state | the regression check changes the corresponding SHA-256 and the verifier rejects the recorded hash; both states match after reversal |
| Source reconstruction | a probe byte changed in an in-memory copy of each selected local projection | exact comparison differs from the pinned source projection; both committed projections match after reversal |
| Lean forbidden tokens | a comment carrying the first forbidden token appended to `WalkCarrier.lean` | `FAIL: WalkCarrier.lean contains forbidden token` naming it; exit 1, then 0 after reversal |
| Receipt replay | the checkpoint value `212` at a million changed to `213` in the committed receipt | `test_committed_receipts_replay_byte_for_byte` fails; exit 1, then 0 after reversal |
| Census scan (FW-PIN, FW-NAME) | a scratch file carrying a watched noun placed in the write root | `test_no_watched_prose_word_in_the_write_root` fails naming the file, line and token; exit 1, then 0 after deletion |
| Growth sentence (FW-GROWTH) | a sentence carrying a forbidden growth phrase appended to `CLAIM_LEDGER.md` | `test_no_growth_sentence` fails naming the file and the phrase; exit 1, then 0 after reversal |
| Outside-root check (FW-SHARE) | synthetic porcelain records only: a probe path under `research/` and a modified sealed artifact | `outside_write_root` returns both records and returns nothing for a path under the write root (`test_outside_write_root_check_is_a_pure_function_of_the_porcelain`).  Writing a real probe outside the root would itself breach FW-SHARE, so this gate's injection is synthetic by declaration |

Defects caught LIVE during construction, before any receipt was
committed, and repaired: (1) the certificate criterion's first version
iterated over the positive VALUES present and never checked a magnitude
that appeared only negatively -- it certified the pinned wedge; the
fixture test and the brute-force comparison test both failed, and the
repair iterates over every magnitude present.  (2) The pruned
enumeration of supported arrangements, written row by row, explored
exponentially many dead ends on the sparse divisor pattern at `N = 60`
and ran past ten minutes; the repair keeps the same generic search and
adds fewest-options row ordering with forward checking on rows and
columns; every value agreed after the repair.  (3) The unpruned `N!`
loop over the whole menu cost 224 seconds (reading 11).  (4) The
stage-3 module's Lean-instance constant said `8` while the package
decides to `7`; the first receipt carried rows at `N = 8` and was
regenerated at `7` before commit -- the frozen predictions name `7`.
(5) A two-word fragment in the refusal scan's own outside-name list was
reassembled by the census scanner's bigram matcher into a watched
phrase; the fragment was removed (the scanner covers the phrase).

## What this run does NOT claim

No sentence here answers the growth question in either direction (A1,
A4, FW-GROWTH).  The carriers are not named by any outside name; the
class and the count are declared and the identities are stated in those
terms (A2).  Agreement at the checkpoints to a million is
FINITE_COMPUTATION within bound (A3).  Magnitude-1 degeneracy means LP4
persists on these families, and the diverse-magnitude census is priced
again (A5).  The observer grades the layers along divisor arrows by a
proved theorem; no theorem here grades walks (A6).  Lean proves; the
receipts record (A7).  The run saw only the commitment hash of the
outside bet (A8).  Nothing outside `research/balance_carrier/` was
written (A9).  The menu is declared and finite; it is not a
classification of carriers, and none is claimed (A10).  The full
adversarial dispositions are in the receipt under `adversarial`.

Declared reading 12, appended when the refusal scans first ran: the
sentence-level scans (protected opens, growth, quantifiers, totality)
read this tree's own claims and skip the two frozen, hash-pinned inputs
`PROMPT.md` and `PREDICTIONS.md` -- the charter's adversarial section
quotes the very claims it refutes, and a substring scan cannot tell a
quoted claim from an asserted one.  The census scan and the outside-name
scan skip nothing.

## Leftovers, named and priced, executed nowhere

1. The general table identity -- CONJECTURE, bounded evidence only; price
   above.
2. The enlarged menu -- OPEN: weights reading an endpoint's balance, and
   counts beyond the four declared, are unsearched; absence of a search
   is not absence of a carrier.
3. LP4, magnitude diversity -- OPEN: every family here has one
   magnitude; a carrier with two is the first thing the enlarged menu
   would be asked for, and nothing about it is claimed.
4. The next rung, named so it cannot be smuggled in later: **fresh
   character totals** -- the signed total, over the fresh members of a
   layer, of one of that layer's characters, a signed count indexed by a
   part count and a step, and its relation to the balance and the
   divisor relation.  Named, not started; its price is a definition of
   the layer's characters in the receiver's own terms, a Lean statement
   of the total, and a frozen prediction before any value is computed.

## The registration diff this tree does NOT apply

Adding this tree to the research job would be the following step in
`.github/workflows/verify.yml`, recorded here as text and not applied
(registration is an author act; the shared files are frozen for both
parallel tracks):

    - name: balance_carrier pins and tests
      run: |
        python research/balance_carrier/verify_pins.py
        python -m unittest discover -s research/balance_carrier -p "test_*.py"

## Commands (run from this directory unless noted)

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 8 sources and 2 spans at snapshot and HEAD; sealed prefixes unchanged; nothing outside the write root; 2 source projections exact; native PROMPT.md frozen; 2 predictions freezes reconstructed` |
| `python verify_lean.py` | 0 | `lean audit clean: 7 sources, 58 axiom reports (11 axiom-free), axioms within ['Quot.sound', 'propext']` |
| `PYTHONDONTWRITEBYTECODE=1 python run_balance_carrier.py --out receipts` | 0 | `stage 2: menu 90, hits ['S1b(W2)', 'S2(W1,1,C1)', 'S2(W3,1,Cbal)']`; `stage 3: DEGENERACY_PERSISTS`; `stage 4: GROWTH_OPEN_UNCHANGED, checkpoint misses []` |
| `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | all tests pass, refusal scans included |
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
