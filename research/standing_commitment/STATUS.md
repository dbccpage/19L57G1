# standing_commitment: demands as a consequence of growth

`AuthorityEffect: None.`

The estate's first standing obstruction, pinned as a span in
`SOURCE_MANIFEST.json`, records that no object-language endogenous demand
generator was derived, and that the fixed-radius, fixed-finite-alphabet
local-strategy class was excluded outright. The machine has a dynamics and
no source of work.

A local strategy looks at a state and *emits* a next demand. A **standing
commitment** does not: it is a condition declared once, saying which pairs
must be kept apart whenever both are held, and it emits nothing. This rung
asks whether a state that GROWS under such a condition thereby acquires
demands that were not there before, with no act between the growth and the
demand.

**It does, and the amount is exact.** Under the commitment that keeps every
distinct pair apart, one growth step on a state of `n` data adds exactly `n`
demands. One declaration covers this stated family of growth steps. The
growth events themselves remain externally supplied.

**This does not close the obstruction, and no sentence here says it does.**
Positive generation results either take a commitment as an input or use the
explicitly declared `total`; nothing here produces a commitment. What changes
is the requirement accounting: separately imposed requirements are replaced
by one standing declaration. The growth events remain external.

## Frozen inputs

`PROMPT.md` sha256
`f5bd6aaba310a3cb…` (recorded in full in `SOURCE_MANIFEST.json`);
`PREDICTIONS.md` sha256
`8b52dcd9a8f041c41668ef051c9618a7ceb83854157ea62c1e1164665c43c48b`, hashed
before the race ran. Sources pinned at snapshot
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be`: four blobs, the OB-1 span, and
one exact source projection.

## Declared readings

1. **The Lean half preceded the freeze; the computational half did not.**
   The Lean package was written and built before `PREDICTIONS.md` existed,
   so its results are recorded there as *already obtained*, not predicted.
   The race had not run when the file was hashed: `run_standing.py` did not
   exist and no value in section 3 had been computed. Section 3 is
   prospective without exception.
2. **Discharge is a declared budget, not a derived repair.** Up to `rate`
   demands are removed per round, oldest first, and a discharged demand
   never returns. The sealed estate gates repair by a represented budget;
   this tree does not reconstruct the repair machinery and claims no repair
   exists.
3. **A fifth commitment was added after the freeze**, and is marked as such
   in the receipt and in `standing.py`. It exists to refute a regularity the
   four frozen commitments exhibit, and it is not scored against any
   prediction.
4. **Only the represented state and its observation semantics are
   reconstructed.** The repair, augmentation, and gate machinery is
   deliberately left out: this rung asks where demands come from, not how
   they are discharged.

## Terminals, each with its scope

- **GROWTH_GENERATES** (PROVED_THEOREM, core Lean, every part of the
  statement general):
  - `demands_grow` — after a growth step the demands are exactly the new
    datum's pairs followed by the demands already there;
  - `demands_persist_under_growth` — growth loses no demand;
  - `growth_generates` — a fresh datum the commitment keeps apart from
    something already held produces a demand the old state did not carry,
    and **no act occurs between the growth and the demand**;
  - `fixpoint_reopens` — **a discharged state is not a finished state**: one
    growth step under the same commitment reopens the process, so the
    fixpoint is not absorbing under growth;
  - `demand_count_grows` — under the total commitment on a viewless state,
    one growth step adds exactly as many demands as there were data;
  - `demands_congr` — demands read the data and the views and nothing else
    in the represented state: not the fuel, not the authorization, not the
    refusal store, not the inert field.
- **GROWTH_GENERATES_NOTHING** (PROVED_THEOREM), the matching negative:
  `empty_commitment_generates_nothing` — under the empty commitment no
  sequence of growth steps produces a demand. Generation is a property of
  the declaration, not of growth. Same shape as the sealed
  `no_guard_no_obstruction`: no stake, no obstruction.
- 14 `#print axioms` reports, all within `{propext, Quot.sound}`, and 14
  originating theorems all listed by the source census.
- **RACE_TABULATED** (FINITE_COMPUTATION): four frozen commitments times
  seven run lengths (8 to 48 rounds), one datum admitted per round, with the
  least declared discharge budget that clears the run.

  | commitment | generated at 24 rounds | peak per round | least clearing budget |
  |---|---|---|---|
  | `total` | 276 | 23 | 23 |
  | `shared_parity` | 132 | 11 | 11 |
  | `adjacent` | 23 | 1 | 1 |
  | `empty` | 0 | 0 | 0 |

- **The regularity, and its refutation.** On all four frozen commitments, at
  all seven run lengths — 28 cases — the least clearing budget equals the
  **peak** per-round generation, never the mean. Every one of those four has
  non-decreasing generation. The post-freeze commitment `bounded`, whose
  generation rises and then stops, refutes the general form: peak `3`,
  least clearing budget `1`, at every run length tested.
  **REGULARITY_REFUTED**, with the countermodel constructed here rather than
  cited.
- **The finite contrast left by the run** (FINITE_COMPUTATION, no Lean):
  under `total` at budget 1, the final backlog is 253 at 24 rounds and 1081
  at 48. Under the post-freeze `bounded` commitment it is 0 at 24, 48, and
  96 rounds. This does not classify arbitrary commitments or later
  horizons. In particular, the bounded countermodel shows that peak
  generation is not a general formula for the least end-of-run clearing
  budget.
- **OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED**:
  the protected opens are untouched. In particular this rung does not narrow
  OB-1; it reports against it, and `test_forbidden.py` fails the run on a
  claim to the contrary.
- **MANUAL_RECEIPT_DECLARED**: no CI gate reads this tree's pins, receipts,
  or Lean audit.

## Predictions, disposed

| id | verdict | value |
|---|---|---|
| Q1 | HIT | `total` generates 276 at 24 rounds; per-round `0, 1, …, 23` |
| Q2 | HIT | `adjacent` generates 23 |
| Q3 | HIT | `shared_parity` generates 132; per-round `0, 0, 1, 1, 2, 2, …` |
| Q4 | HIT | `empty` generates 0 at every rate |
| Q5 | HIT | least clearing budget 1 for `adjacent`, 23 for `total`, both at 24 rounds |
| Q6 | HIT | least clearing budget 11 for `shared_parity` |
| Q7 | HIT | `total` at budget 1 is monotone after round 2 and peaks at the last round |
| Q8 | HIT | `total` 253 → 1081 on doubling; `adjacent` 0 at every length |

Eight of eight. Recorded honestly: **these predictions were arithmetically
forced once the definitions were fixed**, so hitting them is evidence about
the ordering of the work and not about insight. The substantive result of
the computational half is the one that was *not* predicted — that the
clearing budget tracks the peak rather than the mean, and that a commitment
whose generation stops refutes it.

## The injection record

Every verifier was proved by failing on the exact defect it exists to catch,
then recovering. No receipt was regenerated while an injection was live.

| Gate | Injection | Observed |
|---|---|---|
| Pin integrity | first digit of the pinned `Represented.lean` blob flipped | `FAIL: lean4/Derivation/Represented.lean blob at f4b1dcd… is 4c395d6d…, pinned 0c395d6d…`; exit 1, then 0 |
| Span pin | the OB-1 span's first line moved to `85` | `FAIL: span research/genesis_continuation/continuation_plan.md:85-93 … hashes ec1184b0…`; exit 1, then 0 |
| Source projection | a trailing comment added inside the reconstructed block | `FAIL: research/standing_commitment/lean/StandingCommitment/Base.lean:28-57 is not the declared exact projection of pinned lean4/Derivation/Represented.lean`; exit 1, then 0 |
| Predictions freeze | one line appended to `PREDICTIONS.md` | `FAIL: PREDICTIONS.md hashes e114d99b…, recorded 8b52dcd9…`; exit 1, then 0 |
| Axiom source census | one `#print axioms` line removed | `FAIL: StandingCommitment.Standing.satB_grow is declared in Commitment.lean but not listed in AxiomReport.lean`; exit 1, then 0 |
| Receipt replay | a generated count changed from `276` to `277` | `test_committed_receipt_replays_byte_for_byte` fails; exit 1, then 0 |
| Census scan | a probe file carrying a watched noun placed in the write root | the scan names the file, its line, and the token; exit 1, then 0 |
| **Forbidden token — the injection that exposed a dead gate** | a comment carrying the first forbidden token appended to `Commitment.lean` | **exit 0, `lean audit clean`.** See below. After the repair: `FAIL: Commitment.lean contains forbidden token 'sorry'`, exit 1, then 0 |

### The dead gate, in full

The forbidden-token scan inherited from the sibling trees tests
`token in text` — a SUBSTRING scan. The root gate `ci/check_lean_audit.py`
uses word boundaries. A substring scan flags the estate's own word for a
datum entering the state, which the sealed Lean uses throughout and the root
gate allows. This is the same defect class already recorded in the
closed-family rung for the working-denylist scan, now in a second scan.

The repair was to mirror the root gate's patterns. **That repair silently
did not apply**: the escape sequences were consumed in transit and the
patterns reached the file as literal control characters, so the scan matched
nothing at all and the gate was dead. The audit reported clean over a file
that contained a bare forbidden token. Only the injection found it. The
patterns were then rewritten and checked programmatically — the check asserts
that no pattern contains a control character, that the pattern does not
match the estate's ordinary word, and that it does match a bare occurrence —
and the one bare occurrence in this tree's own prose was reworded.

Recorded at length because it is the strongest evidence in this tree for the
estate's own rule: a gate is not proved by being green.

## What this rung does not claim

No endogenous generator. Positive generation results either take a
commitment as an input or use the explicitly declared `total`; nothing here
produces a commitment. OB-1 is untouched. No repair exists here: discharge
is a declared budget, and a discharged demand is recorded as discharged,
not repaired. The regularity of the frozen family is refuted in general and
is not stated without its family. The finite comparison does not classify
arbitrary commitments or later horizons. Every computed number carries its
run length.

## Leftovers, named and priced, executed nowhere

1. **A correctly quantified backlog theorem.** State sufficient hypotheses
   on an arrival sequence for a fixed budget to accumulate backlog or to
   clear it, rather than classifying commitments from finite examples.
   Price: a general arrival model and hypotheses this tree does not define.
2. **Discharge as repair.** Replace the declared budget with the
   reconstructed repair machinery of the sealed module and ask the same
   question. Price: reconstructing the guards and the gates, which this rung
   deliberately left out.
3. **Commitments over forms and rules**, not only over pairs of data. The
   estate's requirements are pairwise; a commitment over the other item
   kinds is a different object and is not built here.
4. **The next rung, named so it cannot be smuggled in later**: whether a
   commitment can be *discharged* rather than only satisfied — the dual
   tree's retraction event is the first discharge in the estate, and pairing
   it with a standing commitment is the obvious next question. Named, not
   started.

## A worktree hazard, recorded

Building a Lean package on one branch leaves untracked artifacts that the
next branch's pin verifier reads as changes outside its write root, because
the ignore rule lives in the other branch's tree. It happened twice in one
session. The fix is to remove the sibling directory before switching, and it
is recorded here because the failure looks like a seal breach and is not one.

## Commands

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 4 sources and 1 spans at snapshot and HEAD; … 1 source projections exact; native PROMPT.md frozen; 1 predictions freezes reconstructed` |
| `python verify_lean.py` | 0 | `lean audit clean: 5 sources, 14 axiom reports (1 axiom-free), axioms within ['Quot.sound', 'propext'], 14 originating theorems all listed` |
| `python run_standing.py --out receipts` | 0 | `peak==threshold counterexamples: 7 (all from the post-freeze commitment)` |
| `python -m unittest discover -s . -p "test_*.py"` | 0 | all tests pass, refusal scans included |
| `python -m mypy` | 0 | strict |
| `python ci/check_prose_watchlist.py` (root) | 0 | clean without a repin |
