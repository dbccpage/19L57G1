# fresh_characters — the native run charter

Frozen. This file is hashed in `SOURCE_MANIFEST.json` and is not edited after
the first computation of any stage. It is the native statement of the run;
the operator's copy lives outside this repository and is not reproduced here.

`AuthorityEffect: None.`

## Write root and seal

Write root: `research/fresh_characters/` only. Sealed and frozen for this
run: `prompt/`, `paper/`, `code/`, `lean4/Derivation/`, `artifacts/`,
`CLAUDE.md`, `ci/`, `.github/`, root `tests/`, `pyproject.toml`,
`requirements.txt`, every sibling research tree including its receipts, and
the census pin `ci/prose_watchlist.json`.

Snapshot: `f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`. A parallel
run with write root `research/described_replay/` may be live; this tree pins
`main`, never that branch, reads sibling trees and never writes them.

## Carrier

The receiver, its layers, their fresh members, the balance, and the layer's
own step action, all pinned at the snapshot above and reconstructed verbatim
in `lean/FreshCharacters/{Receiver,Balance,Steps}.lean` with a pin note per
file:

- `Receiver.QOne`, `mk`, `layer`, `layer_mul_compat`, `receiver_is_union`
- `Balance.FreshAt`, `fresh_rep_exists`, `fresh_rep_unique`, `balance`,
  `balance_one`, `balance_divisor_sum`, `balance_unique`, `freshCount`,
  `runningBalance`, `divisors`, `divisorsBelow`, `sumI`,
  `runningBalance_checkpoints`
- `Steps.repAdd`, `repAdd_val`, `repAdd_rot_zero` — the step action, whose
  value at a member is the member multiplied by the step, taken in the part
  count
- `SignRepair.certificate_iff_dominated`, cited as CONDITIONAL_THEOREM and
  reconstructed as computation in `magnitude_census.py`
- the receipts `research/natural_sections/receipts/layer_balance.json` and
  `research/balance_carrier/receipts/balance_carrier.json`

Part counts range over `1..N` with `N` declared per stage.

## The three consumed leftovers, quoted by pin

Every span hash below is recomputed by `verify_pins.py` at the snapshot and
at `HEAD` before anything else runs.

1. `research/balance_carrier/STATUS.md` lines 352-358, span
   `d3d8d6ff61fcc2c022851e4f6eccefca30cf6f48a0dea2d9561d41ba62715bcc` — the
   rung this run executes, named there and not started there.
2. `research/balance_carrier/STATUS.md` lines 349-351, span
   `42b2010fc09d52ed589deabcd93801b608cd4e17978d079f566dfcd36471d52e` — LP4,
   magnitude diversity, OPEN.
3. `research/convention_price/STATUS.md` lines 139-141, span
   `3d1f91d4276037dd7e9404116379dce68a9950b73bcae6b7c29042b85dd55c7d` — the
   CHANNELS terminal, which prices a census with magnitude diversity.

The spans are quoted by pin and their words are not adopted as this tree's
own.

## Native translation

- **LayerCharacters.** The layer of part count `n` has members `0..n-1` and
  the step action above. A *character* of that layer, into a declared value
  carrier, is a map from the members that turns each step into the carrier's
  operation; it is determined by where it sends the unit member, and its
  carrier-free record is the exponent word `c ↦ a·c mod n`. The value
  carrier is chosen from a menu frozen in `PREDICTIONS.md` before any
  computation of the stage that reads it.
- **FreshTotal.** `total(n, a)` is the sum, over the fresh members of the
  layer of part count `n`, of the value there of the character indexed by
  step `a`. Well-definedness rides on `fresh_rep_unique`.
- **TotalIdentity.** Is there a menu member and a step rule making
  `total(n, step)` the balance at every part count within a declared bound?
- **DivisorRecursion.** What the sum of `total(d, a)` over the divisors `d`
  of `n` equals, proved or bounded.
- **MagnitudeCensus.** The magnitude multisets of the totals over a declared
  rectangle, and the cancellation-certificate criterion applied to each
  family. Whether diversity appears is not stated here.

## Refusals, in force for every file of this tree

`FW-SEAL` no path outside the write root is written.
`FW-NAME` no outside theory, programme, or person name, in prose or in an
identifier; every new prose word is probed against the census before it is
written.
`FW-SET` no statement for every part count without a Lean proof; no
completed classification of characters, carriers, or totals.
`FW-TIES` a menu member that meets a stage is retained through every later
stage, and none is called the carrier.
`FW-TABLE` a table is not a computation; a receipt is not a proof.
`FW-BILL` a green test discharges nothing by itself.
`FW-SCOPE` every identity carries its bound in the same sentence unless
proved in Lean for every part count; every ratio is a checkpoint value,
never a rate.
`FW-CHAIN` sibling terminals, theorems, and receipts are consumed via pins;
sibling prose is not.
`FW-GROWTH` the growth of the running balance is a protected open of this
run. No sentence in this tree claims a bound on it in either direction and
none refutes one. `test_forbidden.py` fails the run on a growth sentence.
`FW-CARRIER` a value carrier is used only inside the stage that declared it;
a theorem proved over one menu member is not restated over another.
`FW-PIN` the census pin is not regenerated by this run; the write root
carries no watched prose word, and `test_forbidden.py` scans it.
`FW-SHARE` no file outside the write root is edited.
`FW-LEAD` the author's expectation is sealed under a commitment hash
recorded in `SOURCE_MANIFEST.json` as `outside_bet_sha256`; the run does not
open it. **This refusal is recorded as BREACHED for this run; see the
declared readings in `STATUS.md`.**

## Stages and their pre-agreed terminals

1. `LAYER_CHARACTERS` — [`CHARACTERS_DEFINED`, `OPEN_AT_NAMED_TARGET`]
2. `TOTAL_IDENTITY` — [`TOTAL_IDENTITY_PROVED`, `TOTAL_IDENTITY_BOUNDED`,
   `NO_TOTAL_IN_CLASS`]
3. `DIVISOR_RECURSION` — [`RECURSION_PROVED`, `RECURSION_BOUNDED`,
   `OPEN_AT_NAMED_TARGET`]
4. `MAGNITUDE_CENSUS` — [`DEGENERACY_PERSISTS`, `DIVERSITY_EXHIBITED`,
   `CERTIFICATE_REFUSED`]
5. `REGISTER_AND_LEFTOVER` — [`REGISTER_WRITTEN`, `GROWTH_OPEN_UNCHANGED`]

Both branches of stages 2 and 4 are agreed before either runs. Predictions
are frozen and hashed per freeze; a missed prediction is recorded next to
its value and never edited.

## Evidence classes

Exactly one per substantive line: DEFINITION, DECLARED_POLICY,
PROVED_THEOREM, CONDITIONAL_THEOREM, FINITE_COMPUTATION, COUNTERMODEL,
CONJECTURE, OPEN, REFUSED, METATHEORY, PREDICTION.
