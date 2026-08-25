# Ledger conformance progress

AuthorityEffect: None. Operator log for `chore/ledger-conformance`.
Not a gate, not a ledger row, not a claim registration.

## Iteration 1 — checker and ratchet (no ledger edits)

- **Batch**: P1 checker only. No claims touched.
- **Claim IDs**: none.
- **What changed**: added `tests/test_claim_ledger_conformance.py`. It
  enumerates `### ` headings independently of the CL- ID classifier,
  then checks required fields, closed Class vocabulary, falsifier
  presence, Python-evidence presence, unique IDs, a frozen claim-ID
  census, and that every backticked Lean name in a Lean/Evidence field
  exists as a declaration in `lean4/`. HEAD gaps are frozen as `KNOWN_*`
  equality ratchets: a new gap fails; an entry that no longer fails
  must leave the set.
- **Measured at this freeze** (127 claims):

  | Gap | Count |
  |---|---|
  | Missing Statement | 1 |
  | Missing Class | 6 |
  | Missing Deps | 84 |
  | Missing Assumptions | 92 |
  | Missing Lean/Evidence | 14 |
  | Missing Axioms | 79 |
  | Missing Falsifier | 69 |
  | Missing/vacuous Python | 52 |
  | Class outside closed vocabulary | 84 |
  | Unresolved Lean names | 0 |

- **Lean names**: every backticked name in a Lean/Evidence field
  resolves. Qualified tokens require an exact elaborated or axiom-report
  name. `KNOWN_UNRESOLVED_LEAN` is empty. No theorem was invented.
- **Could not do**: none in this increment. The ledger was not edited.
- **Checker**: recorded after the review-repair tests.
- **lake build**: succeeded (77 jobs) at `e6168a9`.
- **sorry / admit / axiom counts**: 0 / 0 / 0.

## Iterations 2–3 — WITHDRAWN

Paper edits to `paper/paper_claim_ledger.md` (Class/Scope splits and
FR6 falsifier backfill) were reverted. The tracked CLAUDE.md seals
`paper/`; mechanical checks cannot authorize a mutation of the sealed
ledger. Mixed Class rows (theorem for one reading, finite computation
for another) are therefore left as they were: the checker still reports
them as Class-outside, and this tree does not split or reclassify them.

The operator log previously stored under a filename that named an
external project was renamed to this path.

## Iteration 4 — review repair (no ledger edits)

- **Batch**: checker only.
- **Claim IDs**: none.
- **What changed**:
  - frozen `KNOWN_CLAIM_IDS` census of all 127 headings; population is
    `### ` lines, not the ID classifier;
  - qualified Lean tokens no longer fall back to last-segment match;
  - Lean/Evidence field text concatenates every matching field in
    source order (hash-seed independent);
  - this log renamed off the barred project name.
- **Could not do**: ledger backfill remains unauthorized. Mixed-class
  rows remain in `KNOWN_CLASS_OUTSIDE_VOCAB`.
- **Open obligations added**: 0.
- **Escalations added**: 0.
