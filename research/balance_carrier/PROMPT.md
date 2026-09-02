# 19L57G1 research run -- the balance carrier

Run this as one autonomous construction run on the snapshot of `main`
pinned in `SOURCE_MANIFEST.json`.  Chain step 3, after sign_slice and
convention_price.  A parallel run with write root `research/role_census/`
is live in the same repository; the coordination protocol is reproduced
verbatim under PARALLEL below.

AuthorityEffect: None.

## Charter

- mode: long-horizon construction run; strict structured output in
  `STATUS.md`, `CLAIM_LEDGER.md`, and `receipts/`
- autonomy: no questions; every ambiguity becomes a declared reading in
  `STATUS.md`
- write root: `research/balance_carrier/` only
- sealed: `prompt/`, `paper/`, `code/`, `lean4/Derivation/`, `artifacts/`,
  `CLAUDE.md`, `ci/`, `.github/`, root `tests/`, `pyproject.toml`,
  `requirements.txt`, every sibling research tree (receipts included), and
  the census pin `ci/prose_watchlist.json`
- no claim about model internals; producer prose is testimony; a positive
  terminal is licensed only by this tree's own verifiers and receipts,
  replayed from the write root

## The carrier

The receiver and its layers, as pinned from `research/natural_sections/`
(Lean sources are the truth; Python receipts are the evidence):

- `NaturalSections.Receiver.QOne` -- the value group built from every
  layer; `layer k c` the `k`-th layer's embedding (part count `k + 1`);
  `receiver_is_union`
- `NaturalSections.Balance.FreshAt k c` -- fresh membership;
  `fresh_rep_exists`, `fresh_rep_unique`
- `balance n` -- the signed correction; `balance_one`,
  `balance_divisor_sum`, `balance_unique`
- `freshCount n`, `runningBalance n`, `divisors n`,
  `runningBalance_checkpoints`
- the receipt `receipts/layer_balance.json`: running balance at 10, 30,
  100, 1000, 10000, 100000, 1000000 = -1, -3, 1, 2, -23, -48, 212; "max
  squared ratio 4/5 at part count 5, stays below the square root: True"
  -- a computed record under bound, never a bound claim
- `NaturalSections.SignRepair.certificate_iff_dominated` and its
  constructive converses -- the certificate criterion, cited as
  CONDITIONAL_THEOREM and reconstructed as computation

Part counts range over `1..N` with `N` declared per stage.  No cycle or
rewrite calculus is used anywhere in this run.

## Supply

Three named leftovers are consumed, each from its own tree and from
nowhere else (FW-CHAIN: terminals and receipts, never prose hopes).  Two
of the three spans are quoted BY PIN -- path, line range, and the SHA-256
of the exact span as stored in the pinned blob (the lines joined with LF,
trailing LF included) -- because one span carries a word the census
watches and the other is a receipt, not prose.  `verify_pins.py`
recomputes every span hash at the snapshot and at HEAD.

1. natural_sections, layer-balance rung, registration -- the growth OPEN
   and the named NEXT question: `research/natural_sections/STATUS.md`
   lines 1627-1633, span SHA-256
   `6fb56d34d13ef2f3307d07cdb1283b477b00a05ca58fb3ca0197c8ff3e5a7869`.
   The span names how fast the running balance grows as OPEN, records it
   under declared bounds, claims no bound and refutes none, and names as
   the natural NEXT question an internal observer that grades the layers
   -- so that it cannot later be smuggled in as if derived.  One word of
   that span is not this run's own word and is quoted by pin only.
2. convention_price, CHANNELS terminal: `research/convention_price/STATUS.md`
   lines 138-141, span SHA-256
   `65ec33079d4a8372306d36d7861d76c5ef2aa9cbcab5c0165b190a402e600a6b`, which reads
   (this span carries no watched word and is reproduced): "The channels
   are not claimed to be one repair; they read disjoint ingredients, and a
   census with magnitude diversity is the priced leftover (LP4)."
3. natural_sections, layer-balance receipt and the kernel-decided
   checkpoints: `research/natural_sections/receipts/layer_balance.json`
   (pinned whole) and `runningBalance_checkpoints` in
   `research/natural_sections/lean/NaturalSections/LayerBalance.lean`
   (pinned whole) -- consumed as terminals and receipts, never as prose
   hopes.

Native translation, the ONLY form used anywhere in this tree:

- the named NEXT question (a carrier that grades the layers) becomes
  **LayerObserver** and **WalkCarrier**: (a) an observer on the receiver
  whose value at an element is the part count of its fresh
  representation, proved well defined and layer-separating; (b) a finite
  family over part counts `1..N`, built from the divisor relation and the
  balance alone, together with a DECLARED signed count on it, such that
  the running balance at `N` equals that count -- found within a declared
  class or refused within it.
- LP4, magnitude diversity, becomes **SignedFamilyTable**: the signed
  families the carrier produces at each `N`, their magnitude multisets,
  and the certificate criterion applied; a magnitude-1 family records
  LP4's persistence, never a result.
- the growth OPEN becomes **GROWTH_OPEN_UNCHANGED**: recompute the running
  balance through the carrier to a declared bound, cross-check against
  the pinned checkpoints, record ratios at checkpoints, claim no growth
  bound in either direction.

Forbidden in the write root: every term the census watches (probe
first); the working denylist; every outside theory name; and the outside
names for the receiver, the balance, the running balance, the fresh
count, and the growth question -- describe, never name.

## Vocabulary

Admissible: receiver, layer, part count, fresh, balance, running balance,
divisor, carrier, family, arrow, transport, weight, closed walk, walk,
section, observer, grade, grading, table, signed expansion, signed
family, magnitude, certificate, per-magnitude domination, census,
register, bound, checkpoint, ratio, menu, class, price, leftover; the
twelve evidence classes of the seed (metatheory apparatus; supplied
datum; imposed challenge; admitted primitive; derived definition; proved
theorem; deterministic computation; countermodel; optional realization;
conjecture; open obstruction; refuted claim) and the tree classes used by
the siblings (DEFINITION, DECLARED_POLICY, PROVED_THEOREM,
CONDITIONAL_THEOREM, FINITE_COMPUTATION, COUNTERMODEL, CONJECTURE, OPEN,
REFUSED, METATHEORY, PREDICTION).

Not admissible as this run's own words: the one word of span 1 that
names the closed-walk carrier action, and any name for the stage-2 count
other than the declared count it is.

## Laws

The sign_slice hard rules, then the seed's word discipline: no sealed
path is written; no supplied challenge vocabulary and no outside theory
name appears in any committed file; the working denylist stays out; the
three protected opens (OB-1, S6 item 6, S9 last bullet) stay open; ties
are retained; a table is not a computation; a green test discharges
nothing by itself; the complete classification is not a legal terminal.

Every substantive line carries exactly one evidence class.  Every
theorem-level sentence is a Lean theorem in this tree's own package or a
citation into a pinned sibling packet, or is downgraded.  Every
computational claim has deterministic, fully typed Python evidence with
byte-replayable receipts.  Predictions are written and hashed before the
first computation of their stage; a missed prediction is recorded next to
its value, never edited.  The words "forced", "minimal", "free",
"canonical", "equivalent", "universal", "complete" appear only with a
proof or a precise conditional scope.  Absence of a test is never
equality.  A receipt is never proof of an unverified payload.

## Refusals

- FW-SEAL: no path outside the write root is written; see PARALLEL for
  the frozen list.
- FW-NAME: no outside name; `python ci/check_prose_watchlist.py --probe
  WORD` before any new prose word; identifiers with `_` or digits are
  exempt by construction, prose is not.
- FW-SET: no "for all N" without a Lean proof; no completed classification
  of carriers.
- FW-TIES: two carriers or two counts meeting stage 2 at the same price
  are both retained.
- FW-TABLE: a table is not a computation; a receipt is not a proof.
- FW-BILL: a green test discharges nothing by itself.
- FW-LEAD: this prompt states no result of stage 2; the operator does not
  know whether a carrier in the declared class exists; both terminals are
  pre-agreed; the operator's expectation is sealed under OUTSIDE BET and
  the run never sees it.
- FW-SCOPE: every identity is stated with its bound in the same sentence
  unless proved in Lean for every `N`; every ratio is a checkpoint value,
  never a rate.
- FW-CHAIN: consume sibling terminals and receipts only, via pins; never
  their prose hopes.
- FW-GROWTH: the growth question is a PROTECTED OPEN of this run; no
  growth bound is claimed, in either direction, by any sentence;
  `test_forbidden.py` fails the run on one.
- FW-PIN: the census pin is not regenerated by this run; the write root
  contains no watched prose word; `test_forbidden.py` runs the census
  scanner over the write root and fails on any hit.
- FW-SHARE: no file outside the write root is edited, including
  `CLAUDE.md`, `ci/`, `.github/`, root `tests/`, the pin, and every
  sibling tree.

## Stages

### Stage 1: LAYER_OBSERVER (Lean, own package under `lean/`)

Core Lean only, axioms within `{propext, Quot.sound}`, no sorry-class
escape, no user axiom, no unsafe or partial declaration.

Goal: the observer that grades the layers, proved.

Source policy, declared: EITHER reconstruct the pinned definitions
verbatim with a pin note per definition, OR declare the abstract
interface they satisfy and prove against it, discharging the instance by
the pinned theorems' exact statements; the choice is recorded in
`STATUS.md` before the first compile.

Targets, named now:

- `layer_observer_wf` -- the observer is well defined on the receiver:
  two fresh representations of one element have one part count (from the
  pinned uniqueness).
- `layer_observer_separates` -- distinct part counts give distinct values.
- `layer_observer_constant` -- the value is constant across a layer's
  fresh members.
- `layer_observer_grades` -- OPTIONAL TARGET, both outcomes pre-agreed:
  along a declared arrow between layers (divisor step), the value changes
  by the declared step; if not provable in the declared form,
  OPEN_AT_NAMED_TARGET with the exact obstruction.

Predictions: the first three provable in core Lean; the fourth recorded,
not predicted.  May not: import sealed modules; cite the packet where a
proof is required.  Terminals: LAYER_OBSERVER_PROVED,
OPEN_AT_NAMED_TARGET.

### Stage 2: WALK_CARRIER (Lean + computation, FW-LEAD)

Goal: is the running balance at `N` a declared signed count on a finite
family built from the divisor relation and the balance alone?

Class, declared before any computation:

- objects: part counts `1..N`
- arrows: `d -> m` exactly when `d` divides `m` and `d < m`
- weights: one function from a finite MENU declared in `PREDICTIONS.md`
  before running, each menu item built only from `balance`, the divisor
  quotient, and the constants `0`, `1`, `-1`
- counts: a finite menu of declared signed counts, at least these three:
  (S1) walk sums -- the sum over walks from `1` to `N` of the product of
  weights; (S2) the signed expansion of a square table indexed by `1..N`
  whose entries are drawn from the arrow weights and a declared first
  column -- the alternating sum over bijections, stated as such; (S3)
  signed section counts of the family with its declared observer.

Bound, declared: exhaustive menu search for `N <= 12` in Python; any
identity found is cross-checked against the pinned checkpoints to
`N <= 10000` by direct recomputation and against the pinned receipt at
100000 and 1000000 by the fastest exact route this tree can afford; Lean:
the identity for every `N` if provable within the run, else kernel-decided
instances with the bound in the sentence.

Predictions, BOTH branches pre-agreed: if some (weights, count) pair
matches the running balance at every `N <= 12`, terminal
CARRIER_IDENTITY_BOUNDED, upgraded to CARRIER_IDENTITY_PROVED only by a
Lean theorem quantified over `N`; the pair is named, its menu index
recorded, ties retained.  If none does, terminal NO_IDENTITY_IN_CLASS,
stated with the menu and bound in the same sentence; the enlarged-menu
question is the leftover -- absence of a search is not absence of a
carrier.

May not: extend a bounded identity beyond its bound in any sentence; name
the count by anything but the declared count it is.  Terminals:
CARRIER_IDENTITY_PROVED, CARRIER_IDENTITY_BOUNDED, NO_IDENTITY_IN_CLASS.

### Stage 3: SIGNED_FAMILY_TABLE (FINITE_COMPUTATION)

Goal: LP4 on the carrier's own signed families.  For each (weights,
count) pair that met stage 2 -- or, if none did, for each menu pair at
`N = 12` -- the signed family of its terms at `N = 6`, `12`, and the
largest `N` the Lean instances reach: magnitude multiset, total, the
certificate decision by per-magnitude domination
(`certificate_iff_dominated` reconstructed as computation, cited as
CONDITIONAL_THEOREM), and the LP4 check.

Predictions, pre-agreed: if every magnitude is `1`, terminal
DEGENERACY_PERSISTS and LP4 is carried forward unchanged, said exactly
that way; otherwise CERTIFICATE_DECIDED per `N` with the table as the
record.  May not: treat a certificate decision as a statement about
growth (FW-GROWTH).  Terminals: CERTIFICATE_DECIDED, DEGENERACY_PERSISTS.

### Stage 4: GROWTH_CHECKPOINTS (FINITE_COMPUTATION, protected open)

Goal: the running balance recomputed through the stage-2 identity (if
any) and directly, agreeing at every pinned checkpoint; the ratio of the
absolute running balance to the square root of `N` recorded at 10, 30,
100, 1000, 10000, 100000, 1000000 and at the running maximum.

Predictions: agreement at every checkpoint (a MISS here is a defect of
this tree, not of the sibling); ratios recorded, not predicted.  May not:
write any sentence about how the ratio behaves beyond the last
checkpoint.  Terminal: GROWTH_OPEN_UNCHANGED -- mandatory; no other
terminal exists for this stage.

### Stage 5: REGISTER_AND_LEFTOVER

Goal: per-candidate rows (menu index, count, bound reached, Lean status,
certificate cell); the leftovers named and priced: the general identity if
bounded only; the grading target if OPEN; LP4 if degenerate again; and
the next rung named so it cannot be smuggled in later -- signed sums of
the receiver's layer characters over the fresh members of a layer (the
operator's own phrase for these is withheld; the native word is found
here) -- named, not started.  Terminal: REGISTER_WRITTEN.

## Adversarial

- A1 "an identity for the running balance says something about its
  growth" -- refute: FW-GROWTH; an identity re-expresses the same signed
  sum; growth stays OPEN.
- A2 "the carrier is a known outside object" -- the class is declared,
  the count is declared, the identity is stated in those terms; naming is
  refused (FW-NAME).
- A3 "agreement at the checkpoints to a million is a theorem" --
  FINITE_COMPUTATION within bound.
- A4 "a Lean proof of the identity for every N closes the growth OPEN" --
  it does not; say so.
- A5 "magnitude-1 degeneracy makes certificates useless" -- it means LP4
  persists on this family; say exactly that and price the
  diverse-magnitude census again.
- A6 "the observer grades walks" -- only if `layer_observer_grades` is
  proved; else OPEN.
- A7 "receipts prove the theorems" -- refute: Lean proves; receipts
  record.
- A8 "the sealed bet steers the run" -- refute: the run never sees the
  plaintext; only a hash is in this prompt; FW-LEAD is honored by
  construction.
- A9 "this run overlaps the parallel run" -- refute: disjoint write
  roots, frozen shared files, pins to `main`; a moved pinned source is a
  recorded repin, not a rewrite.
- A10 "the menu is the set of all carriers" -- FW-SET; the menu is
  declared and finite.

## PARALLEL (verbatim in both tracks' prompts)

1. Disjoint write roots: this run `research/balance_carrier/` only; the
   other run `research/role_census/` only.
2. Frozen for both: `CLAUDE.md`, `ci/`, `.github/`, root `tests/`,
   `pyproject.toml`, `requirements.txt`, every sibling research tree, the
   census pin `ci/prose_watchlist.json`.  A needed change is named in
   `STATUS.md` as an unapplied registration diff.
3. The census pin is not regenerated by a run; probe words before writing
   them; quote a sibling's leftover by pin when its span contains a
   watched word.
4. Pin to `main` at one exact 40-digit snapshot, never to the other
   track's branch; a moved pinned source after the other track merges is
   a recorded repin of that source only.
5. One branch, one PR, one rung; the author merges; the red X on every PR
   means nothing (Actions are billing-dead by author decision); the local
   battery is the verifier.
6. Work in an isolated checkout (worktree or second clone).
7. Read the other tree, never write it; its receipts are evidence, its
   prose is not.

## Outside bet

- hash algorithm: SHA-256 over the file bytes, LF line endings
- plaintext location: outside this repository, held by the author until
  the run ends
- commitment:
  `6b0219f1c397abf357e9aea36307cc5855b52f882699b83294a105c86da2ecbe`
- mismatch terminal: BET_MISSED, recorded by the author outside this
  repository; never in-repo

## Deliverables

`research/balance_carrier/`: `PROMPT.md` (this file, frozen, hashed;
leftovers quoted by pin); `PREDICTIONS.md` (hashed per stage, the
stage-2 menu included in the first freeze); `SOURCE_MANIFEST.json` +
`verify_pins.py` (pinning the three Lean modules, the natural_sections
`STATUS.md`, the two receipts, and the convention_price `STATUS.md` at one
exact 40-digit snapshot of `main`, plus the span hashes); `lean/` (own
package, `AxiomReport` with `#print axioms` per theorem, `verify_lean.py`);
`layer_observer.py`, `walk_carrier.py`, `signed_table.py`,
`growth_checkpoints.py`, `register.py`, `run_balance_carrier.py`,
`test_balance_carrier.py`, `test_forbidden.py` (runs the census scanner
over the write root, the working denylist, the sealed-path scan, the three
protected opens plus FW-GROWTH sentences); `pyproject.toml` (tree-local
mypy strict); `receipts/`; `STATUS.md` (terminals with scopes, the
manual-receipt sentence, the unapplied registration diff, the
parallel-track snapshot note); `CLAIM_LEDGER.md`.

## Done

Every stage carries its terminal with scope; the Lean package builds clean
with axiom reports inside the whitelist; `python
ci/check_prose_watchlist.py` is clean from the repository root WITHOUT a
repin; every sibling pin is untouched; GROWTH_OPEN_UNCHANGED is the
stage-4 terminal; the leftover register names the next rung without
starting it.

## TAU

The `[TAU]` export is written to `receipts/tau.yaml` at the end of the run
with: steps completed, write root, sealed paths touched (must be empty),
shared files touched (must be empty), census pin regenerated (must be
false), the native prompt hash, the predictions freeze hashes, the
terminals with scopes, the layer observer's proved and open targets, the
walk carrier's terminal, menu size, bounds, and identity, the signed
family table's terminal and magnitudes at 12, the growth terminal with
checkpoint agreement and ratios, the LP4 disposition, the leftover, the
four opens unchanged (OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED,
NS95_GROWTH_UNCHANGED), the outside bet hash, `authority_effect: None`,
and the final state.
