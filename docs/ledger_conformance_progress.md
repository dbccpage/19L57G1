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
from the branch. The seal preserves the derivational boundary: it neither
authorizes arbitrary edits nor categorically forbids ordinary claim-hygiene
edits to `paper/`. This PR deliberately lands the checker without a backfill.
The proposed T1–T8 fields do not cover the global debt, and some affected rows
need scope correction rather than mechanical field insertion; a separately
reviewed claim-hygiene change is therefore required before any backfill lands.

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

## Iteration 6 — relocate T1–T8 field draft (no ledger edits)

Follow-up to #86. An earlier #87 attempt wrote T1–T8 fields into
`paper/paper_claim_ledger.md` (`665e38c`, `d4cfcfa`) and `--repin`'d
the tower snapshot onto those commits. That is not on this branch:
paper-modifying commits were dropped from history rather than reverted
and re-pinned, because `verify_manifest.py` walks
`snapshot..HEAD` with `--full-history` and a later revert still
counts as a protected touch.

- **Batch**: operator draft plus the two tests named as T5/T6
  evidence. No claims in `paper/` touched.
- **Claim IDs**: CL-FR6-T1-INERTIA through CL-FR6-T8-DYNAMICS (draft
  only).
- **What changed**:
  - `docs/ledger_fr6_t1_t8_field_draft.md` holds the proposed
    Deps/Assumptions/Python/Axioms/Falsifier fields, written from the
    cited Lean. `Assumptions` is the FR6 carriers, not the header's
    `shared` package (`CL-TOKEN-ERASURE` does not cover
    `RState`/`JState`/`PState`/`MState`/`Bool` or Python
    `Proto`/`FState`). T4 is scoped to the judgment variant. T3 names
    `refusal_frontier.json:normal_form.witnessed_without_relation_rule`.
  - `tests/test_refusal_frontier.py`: `test_refusal_links_are_born_irreflexive_in_class`
    and `test_witnessed_minimum_unique_under_both_orders` now run at
    the declared 6-event horizon (they previously used 5).
  - Research snapshot stays at `477a60ff24346ea87b601dd0fffb75b437e46a31`.
    `--repin` was not used.
- **Did not do**: land the fields in `paper/paper_claim_ledger.md`. This
  iteration is the checker and operator draft, not a separately reviewed
  claim-hygiene change, and the draft is not a ledger row.
- **Open obligations added**: the eight rows remain in the ledger
  `KNOWN_*` gap sets until a separately reviewed change resolves their
  scopes and fields in the ledger.
- **Escalations added**: 0.

## Iteration 7 — exact legacy-debt terminal (no ledger edits)

`STATUS: LEGACY_LEDGER_GAPS_REMAIN`

`AuthorityEffect: None`

The conformance checker is a drift ratchet, not a completion certificate. At
the current 135-heading ledger population its exact frozen debts are:

| Gap | Count |
|---|---:|
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

The gap sets overlap: these rows are separate projections of the frozen debt,
not additive counts of distinct claims.

The snapshot is bound by SHA-256 over the LF tracked Git-blob payload bytes:

```text
paper/paper_claim_ledger.md            B32FD411BC7297974826377D41FDB46E1098375722D842C1E7A2F21B206B3F16
tests/test_claim_ledger_conformance.py  1040199FD5D7B6E08CEDFFDC169D65D1BF470A98A38688F82C78E419135838C5
tests/claim_ledger_body_pin.txt         0C9B39840C72CF9575F7DF3A6DC346DBFADEE57F0C8D6C79434E9358B6A14D8D
```

The live test requires exact equality with every `KNOWN_*` set and the body
pin. Therefore green means the listed gaps neither grew nor silently vanished;
it does not mean the claims acquired the missing fields or semantics.

```text
LEDGER_BACKFILL_NOT_PERFORMED
RATCHET_GREEN_MEANS_NO_NEW_OR_STALE_GAPS_NOT_COMPLETION
LEDGER_BACKFILL_REQUIRES_SEPARATE_SCOPE_REVIEW
KNOWN_UNRESOLVED_LEAN=0
```

Backfill remains unperformed. The T1–T8 draft is only a proposal and must not
be copied mechanically into `paper/paper_claim_ledger.md`: it does not cover
the global debt, and some rows need scope correction rather than field
insertion.
