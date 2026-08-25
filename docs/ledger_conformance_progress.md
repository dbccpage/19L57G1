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

## Iterations 2–3 — not in this PR

A draft backfill edited `paper/paper_claim_ledger.md` and was dropped
from the branch. The reason recorded here previously — "CLAUDE.md seals
`paper/` so ledger edits are unauthorized" — was false. CLAUDE.md's
`paper/` paragraph bars creating `paper/coda/`; it does not bar ledger
edits, and `main` already contains many commits that edit
`paper/paper_claim_ledger.md`. This PR still does not backfill: it
lands the checker first. Gap sets stay at the merge-base snapshot
because no backfill is in the commit, not because the ledger is
uneditable.

The operator log previously stored under a filename that named an
external project was renamed to this path.

## Iteration 4 — review repair (no ledger edits)

- **Batch**: checker only.
- **Claim IDs**: none.
- **What changed**:
  - frozen `KNOWN_CLAIM_IDS` census of all 127 headings; population is
    CommonMark ATX h3 (`#{3}` plus space or tab), not the ID classifier;
  - qualified Lean tokens no longer fall back to last-segment match;
  - Lean/Evidence field text concatenates every matching field in
    source order (hash-seed independent);
  - this log renamed off the barred project name.
- **Could not do**: mixed-class rows remain in
  `KNOWN_CLASS_OUTSIDE_VOCAB` until a backfill commit edits them.
- **Open obligations added**: 0.
- **Escalations added**: 0.

## Iteration 5 — presence-only holes (no ledger edits)

Mutation review of `47752ac`: empty fields, a lie that kept every key,
and a tab heading all stayed green. Fixes:

- ATX population accepts tab after `###`; a tab heading is classified
  and then fails the census.
- Required fields without a letter are missing. Lean/Axioms `--` remains
  the none-sentinel.
- Per-claim SHA-256 body pin in `tests/claim_ledger_body_pin.txt`.
- Declaration index is theorem/lemma/def/constructor heads after
  comment stripping; match-arms and `/ - -/` prose words are not names.
- `Derivation.*` does not resolve. Module wildcards still do.
- Injection tests reproduce the mutations. CLAUDE.md injection table
  gained the corresponding rows.
