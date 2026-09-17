# Mechanization — the (B)-is-empty lemma (discharges SF-OPEN-A)

**Evidence boundary (2026-09-16).** The later synthesis is a supplied
report, not locally authenticated independent-run evidence. Its shared-environment
flag, absent raw runs, distinct cost counters, and missing cross-model bridge
limit every reported HIT/MISS below; see `BLIND_RECONCILIATION.md`.
Zero observer cost does not mean a zero-admission oriented object.

`AuthorityEffect: None.` Object-language result. Touches nothing under the seal.
**Analytic, not blind** (see `CLOSURE.md`): author-reasoned, then reproduced by a
model run under disclosed premises at VERDICT T7. That run is **not**
independent confirmation — see `BLIND_RECONCILIATION.md`, dated 2026-09-16 —
and the frozen predictions in `AUTHOR_READING.md` are rescored there against a
reported blind run instead. This folder adds the mechanization the closure
planned; the caveats below on what it does and does not establish are
unchanged in kind, sharper in one place (see "What is NOT mechanized").

## What is mechanized, and at what grade

The load-bearing formal step — **route (B) is empty** — is mechanized twice:

- **Lean** (`lean/OrientedBoundary/Basic.lean`): on a two-element carrier a
  judgment is read on the tested ordered pair as `(d x y, d y x)`. `swapInAut js`
  is the swap σ=(x y) preserving every admitted judgment.
  - `b_is_empty` — `swapInAut js = true ↔ ∀ d ∈ js, distinguishes d = false`.
    σ ∈ Aut **iff** no admitted judgment distinguishes the pair.
  - `not_in_aut_needs_witness` — `swapInAut js = false → ∃ d ∈ js, distinguishes
    d = true`. σ ∉ Aut **forces** a mechanism-(A) witness; the witnessless route
    (B) cannot occur.
  - `s2u_swap_is_automorphism`, `s2o_swap_is_not_automorphism`,
    `s2o_breaks_at_one_witness` — the unoriented reading has σ ∈ Aut; the oriented
    reading breaks it at **exactly one** asymmetric witness (AP1/AP2).
  - Axioms: within `{propext, Quot.sound}`; no `sorry`/`admit`/`axiom`/mathlib/
    `Classical`. Reports emitted by `lean/OrientedBoundary.lean`.
- **Python** (`oriented_boundary.py`, `test_oriented_boundary.py`): the same lemma
  checked **exhaustively** over all 16 admitted sets on the four distinct
  judgments — `b_is_empty` holds on every set, `swap_in_aut` iff no (A) witness,
  and no admitted set realizes σ∉Aut without a witness (the "from-nowhere
  withdrawal" is unrepresentable). 7 tests pass.

## What is NOT mechanized (kept analytic, and graded so)

The **kind** conclusion — *an order is a paid symmetry-breaking witness, not a
container* — is the analytic step the lemma licenses, not itself a Lean theorem:
a container (boundary) exists **before** its contents; an order/relation exists
**only with** its contents (it needs a pair before it can hold). Different
existence-conditions ⇒ different kinds. This is reasoning about the seed's
existence conditions, recorded in `CLOSURE.md`, graded Representation. And
**time-as-succession never entered** the language; only static two-sidedness did.

Also NOT mechanized, as of 2026-09-16: the **toll direction**. `OB-ONE-CAPABILITY`
is a real Lean theorem about the stipulated two-judgment model in
`Basic.lean`, but that model does not itself establish that orientation is
the side of a separating response that costs. The supplied synthesis reports
a different item-price comparison in a different candidate space (`BLIND_RECONCILIATION.md`).
No corrected toll-direction theorem is mechanized here; the blind report's
own residuals (an unpayable polarity remainder, tied non-isomorphic minima, a
counter-level collapse) make a single clean replacement theorem premature,
not merely undone.

## Provenance and the remaining pins

The derivation is the author's (Jeremy Carroll). Grades: `OB-B-EMPTY`
Derivation (Lean, over a stipulated model — see its docstring and
`CLAIM_LEDGER.md`'s caveat), also reported as `OB-B-EMPTY-BLIND-JUDGEMENT`
(judgement, not mechanized; independence not certified); the exhaustive check
Representation (Python); `OB-KIND` Representation, narrowed to the kind
question only; `OB-ONE-CAPABILITY` Derivation over its stipulated model,
toll-direction claim superseded; the SF-OPEN-A discharge Representation,
downgraded — analytic plus a reported judgement on the kind
question, with independence not certified, **not** the "one independent clean-model confirmation" this file
previously claimed (`TIME_PROMPT_v2.md` discloses its own conclusion; see
`BLIND_RECONCILIATION.md`).

This tree lives at `research/oriented_boundary/` with a light `SOURCE_PIN.json`
(no sealed consume, so no gate-11 pin). `research/side_free/CLAIM_LEDGER.md`
records a "Correction, recorded" discharge under SF-OPEN-A (the verifier does
not read the ledger, so a note keeps it green), itself corrected alongside
this file. The supplied synthesis reports runs of `SEED.md`
(`BLIND_RUN_REPORT_20260916.md`); its claims and their limits are reconciled in
`BLIND_RECONCILIATION.md`.
