# Predictions, written and hashed before each stage's first computation

A missed prediction is recorded next to its value and never edited.
Freeze hashes are recorded in `SOURCE_MANIFEST.json`
(`predictions_freezes`, in freeze order) and in `STATUS.md`.  Stages 1
and 2 are frozen together (the stage-2 menu belongs to the first freeze);
stages 3, 4 and 5 are frozen together after stage 2's results exist and
before any stage-3 computation runs.

## Stage 1: LayerObserver (written before the Lean package was compiled)

Source policy, declared here and in `STATUS.md` before the first
compile: the pinned definitions are RECONSTRUCTED VERBATIM into this
tree's own package, each with a pin note naming the pinned file and its
blob id; nothing is imported from a sibling package and no sealed module
is imported.  Theorems whose proof text is reproduced from a pinned file
are classified CONDITIONAL_THEOREM (a citation into the pinned packet,
compiled here); theorems originating in this tree are PROVED_THEOREM.

The observer, declared: on a raw pair `(n, k)` (the `n`-th part of
`k + 1`) the value is `(k + 1) / gcd(n, k + 1)`; the observer on the
receiver is this raw function lifted through the quotient, which is what
`layer_observer_wf` has to license.

- L1: `layer_observer_wf` is provable in core Lean: two raw pairs naming
  the same receiver element have the same raw value.  Route: every raw
  pair equals a fresh representative whose part count is the raw value
  (an explicit reduction with cross difference zero, the pinned
  `reduce_below` shape), and the pinned `fresh_rep_unique` identifies the
  part counts of two fresh representatives of one element.
- L2: `layer_observer_constant` is provable in core Lean: for `c` fresh at
  layer `k`, the observer's value at `layer k c` is `k + 1`.
- L3: `layer_observer_separates` is provable in core Lean: for `c` fresh at
  layer `k` and `c'` fresh at layer `k'`, equal observer values force
  `k = k'`; the contrapositive form is stated alongside.
- L4: `layer_observer_grades` is RECORDED, not predicted.  The declared
  arrow and step: the divisor arrow `d -> m` with `m = q * d`, `q >= 2`,
  carries a part `c` fresh at part count `d` to the part `q * c` of part
  count `m`; the declared statement is that the observer's value at that
  image is `d` -- the value along the arrow stays at the arrow's source
  while the layer index is multiplied by `q`.  If this form is not
  provable in the run, OPEN_AT_NAMED_TARGET with the exact obstruction.
- L5: every report in `AxiomReport.lean` lies within `{propext,
  Quot.sound}`; a target that resists is recorded OPEN_AT_NAMED_TARGET
  next to its name, never prose-proved.
- L6 (Python): the raw observer agrees with a brute-force fresh
  representation search on every raw pair `(n, k)` with `n <= k <= 40`,
  `0` misses; the observer's values on the fresh members of part counts
  `1..12` are constant per part count and equal the part count.

## Stage 2: WalkCarrier (written before any stage-2 computation ran)

The class is the one declared in `PROMPT.md`: objects `1..N`, arrows
`d -> m` exactly when `d` divides `m` and `d < m`, the quotient
`q = m / d >= 2`.

### The weight menu (frozen)

| index | weight on the arrow `d -> m` |
|---|---|
| W0 | `0` |
| W1 | `1` |
| W2 | `-1` |
| W3 | `balance(q)` |
| W4 | `-balance(q)` |

Each item is built only from `balance`, the divisor quotient, and the
constants `0`, `1`, `-1`.  Weights reading the balance of an endpoint
rather than of the quotient are OUTSIDE this menu by the letter of the
class and are named as the enlarged-menu leftover if they matter.

### The count menu (frozen)

- S1, walk sums from `1` to `N`: the sum over strict divisor chains
  `1 = c_0 < c_1 < ... < c_r = N`, each dividing the next, of the product
  of the arrow weights along the chain; at `N = 1` the empty chain
  contributes `1`.  Five candidates, one per weight.
- S1b, totalled walk sums: the sum of S1 over every endpoint `m` in
  `1..N`.  Five candidates.  (Added to the "at least three" of the
  prompt; a walk sum to every object of the family, totalled, is a signed
  count on the same family.)
- S2, the signed expansion of a square table `T` indexed by `1..N`:
  `T(i, j) = w(i -> j)` when `i` divides `j` and `i < j`; `T(i, j) = 0`
  when `i` does not divide `j` and `i` is not `j`; the diagonal
  `T(i, i) = delta` with `delta` in `{0, 1, -1}`; the first column
  `T(i, 1) = f(i)` for `i >= 2` with `f` in `{0, 1, -1, balance(i),
  -balance(i)}`; `T(1, 1) = delta`.  Rows are sources, columns are
  targets.  The count is the alternating sum over bijections `s` of
  `{1..N}`: the sum of `sign(s) * prod_i T(i, s(i))`, the sign being
  `(-1)` to the inversion count of `s`.  `5 * 3 * 5 = 75` candidates,
  indexed `(W, delta, f)`.
- S3, signed section counts: a section assigns to every object `m` in
  `2..N` one arrow into `m` (one proper divisor `d(m)`); the count is the
  sum over sections of the product over `m` of `w(d(m) -> m)`; at `N = 1`
  the empty section contributes `1`.  Five candidates.

Ninety candidates in all.  Each is compared with the running balance at
every `N` in `1..12`; a candidate meets stage 2 exactly when it agrees at
all twelve.

### Routes for the counts (declared)

- S1, S1b, S3: direct recursion over proper divisors, exact integers.
- S2, the declared count itself: the literal alternating sum over all
  `N!` bijections for `N <= 9` (the "literal route").  For `N` from 10 to
  12 and for the extension cross-checks, two exact elimination routes,
  both METATHEORY (elementary facts about the alternating sum over
  bijections, not proved in this tree): fraction-free row elimination,
  and -- when the diagonal is `1` or `-1` -- the reduction of the first
  column by the other columns to a triangular table whose alternating sum
  is its diagonal product ("the column route").  Where two routes overlap
  they are compared and the comparison recorded; a disagreement is a
  defect of this tree.

### Predictions

- P2.1: S1 with weight W2 (`-1`) equals the BALANCE at every `N <= 12`,
  not the running balance; in Lean, `walkSum_neg_one_eq_balance` is
  provable for every part count `>= 1` from the pinned `balance_unique`
  (the walk sum with weight `-1` has value `1` at part count `1` and
  vanishing divisor sums).
- P2.2: S1b with weight W2 therefore matches the running balance at every
  `N <= 12`, and the Lean theorem `totalWalkSum_neg_one_eq_runningBalance`
  is provable for every `N` from P2.1 and the pinned definition of the
  running balance -- so this pair would reach CARRIER_IDENTITY_PROVED.  If
  the Lean proof does not compile in the run, the pair stays
  CARRIER_IDENTITY_BOUNDED at `N <= 12` and the general form is OPEN.
- P2.3: no S1 candidate matches the running balance at every `N <= 12`.
- P2.4: in S2, at least one table matches at every `N <= 12`.  The run
  expects two: `(W1, 1, 1)` -- unit weights, unit diagonal, unit first
  column -- and `(W3, 1, balance(i))`.  The stated reason is METATHEORY
  and not a result: a unit first column collects, in the alternating sum,
  one signed term per divisor chain from `1` to each object, so the
  expansion totals the S1 walk sums with weight `-1`.  The exact hit set
  is recorded; any further hit and any miss are recorded next to this
  line.
- P2.5: no S3 candidate matches at every `N <= 12`.
- P2.6: every S2 hit is cross-checked against the running balance
  recomputed directly (the pinned divisor recursion) at every `N <= 10000`
  and against the pinned checkpoints at 10, 30, 100, 1000, 10000; at
  100000 and 1000000 the column route is used and compared with the
  pinned receipt values `-48` and `212`; the literal route and the
  fraction-free route agree with the column route wherever two run.
  Zero misses expected; any miss is a defect of this tree.
- P2.7: Lean decides instances of every S2 hit against `runningBalance`
  by kernel evaluation of the literal alternating sum; the bound reached
  is recorded in the sentence (at least `N <= 6` expected); the general
  S2 identity is NOT proved this run and is recorded CONJECTURE with its
  computed support, never as a theorem.
- P2.8: ties are retained: every pair meeting stage 2 is carried into
  stage 3 with its menu index.

## Stages 3-5 (written after stage 2's search and Lean results existed,
## before any stage-3 computation ran)

Recorded, not smoothed: the stage-2 smoke run printed, next to each S2
hit's values, the number of supported arrangements of its table at each
`N <= 12`.  Those counts are therefore NOT predicted below; the stage-3
rows record them.  Stage 2 closed with three hits -- `S1b(W2)`,
`S2(W1,1,C1)`, `S2(W3,1,Cbal)` -- and the Lean instances of the two S2
hits are kernel-decided to `N <= 7` (the kernel refused `N = 8` inside
the package by deep recursion; a separate probe is recorded in
`STATUS.md`).  The largest Lean instance `N` for stage 3 is therefore `7`.

### Stage 3: SignedFamilyTable

- P3.1: for each of the three hits and each `N` in `{6, 7, 12}`, every
  term magnitude is `1` -- the S2 tables have entries in `{0, 1, -1}` and
  the chain weights of `S1b(W2)` are `+1` or `-1` -- so the terminal is
  DEGENERACY_PERSISTS and LP4 is carried forward unchanged, said exactly
  that way.
- P3.2: every family's total equals the running balance at its `N`
  (the total of the nonzero terms IS the count), `0` misses.
- P3.3: the certificate decision by per-magnitude domination finds a
  certificate on every row (at a single magnitude one side always
  dominates), with the dominated side recorded per row; no certificate
  decision is read as a statement about growth.
- P3.4: the reconstruction re-decides the pinned fixtures: the wedge
  `[-2, -2, -1, 2, 2, 2]` has no certificate, the witness
  `[1, 2, -1, -2, 1, 1]` has one.
- P3.5: for `S2(W3,1,Cbal)` some supported arrangements have a zero
  product (a balance value `0` on a chain or in the first column); they
  are excluded from the family and their count is recorded.

### Stage 4: GrowthCheckpoints

- P4.1: at every pinned checkpoint `10, 30, 100, 1000, 10000, 100000,
  1000000` the three recomputations -- direct (pinned recursion), through
  `S1b(W2)` (the walk-sum recursion), through `S2(W1,1,C1)` (the column
  route) -- agree with each other and with the pinned values
  `-1, -3, 1, 2, -23, -48, 212`; a miss is a defect of this tree.
- P4.2: the running maximum of the squared ratio over `2..1000000` is
  `4/5` at part count `5`, as pinned, and the square stays below `N`
  throughout that window -- a value about the window, not a bound.
- P4.3: the ratios at the checkpoints are recorded, not predicted.
- P4.4: the terminal is GROWTH_OPEN_UNCHANGED and nothing else; no
  sentence about the ratio beyond the last checkpoint is written anywhere
  in this tree, and `test_forbidden.py` fails the run on one.

### Stage 5: RegisterAndLeftover

- P5.1: one row per candidate that met stage 2 (three rows), each with
  menu index, count, bound reached, Lean status, and certificate cell;
  the 87 candidates that did not meet stage 2 are summarised by kind with
  their best agreement.
- P5.2: the leftovers are named and priced, executed nowhere: the general
  S2 identity for every `N` (CONJECTURE, bounded evidence only); the
  enlarged-menu question (weights reading an endpoint's balance; counts
  beyond the four declared); LP4, persisting on these families; and the
  next rung -- signed totals of a layer's characters over its fresh
  members -- named in this tree's own words and not started.
- P5.3: the register closes none of the four protected opens
  (OB-1, S6 item 6, S9 last bullet, the growth question), and the
  completed classification of carriers is refused (FW-SET).
