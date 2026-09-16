# Reconciliation — the blind run against the analytic discharge

`AuthorityEffect: None.` Records what changed in this tree on 2026-09-16 and
why, after a genuinely blind run surfaced two things the analytic discharge
(`CLOSURE.md`, `AUTHOR_READING.md`, dated 2026-09-10/11) had wrong.

## Provenance

- Blind prompt: `SEED.md` in this tree, SHA-256
  `4e24fab42a3fbc8884b4f880a51e5d061c7a9b3cdf93aba1a2d77de7ad561ff3`. `SEED.md`
  self-declares blind (line 3: "to be run blind by an agent that has not seen
  this discussion... do not target a predetermined conclusion") and carries
  none of `AUTHOR_READING.md`'s frozen predictions or `TIME_PROMPT_v2.md`'s
  disclosed premises.
- Five independent runs against that seed were synthesized into
  `BLIND_RUN_REPORT_20260916.md`, vendored here as a content-identical
  transcription of the synthesis produced outside this repository. SHA-256 of
  the file as committed here: `1c316003a130a60eeaa958b2a3b7c810bdfde7fc566d8a18dcee46f94d150d18`.
  The source copy carries CRLF line endings and this repository's own text
  files do not (`.gitattributes` reserves `-text` protection for `prompt/**`
  and `artifacts/**` only); the transcription is therefore line-ending
  normalized, not byte-identical to the external source, and this note says so
  rather than claiming a byte match that would not survive inspection.

## What TIME_PROMPT_v2.md actually is, checked directly

`CLOSURE.md` and `AUTHOR_READING.md` both described a run of `TIME_PROMPT_v2.md`
as independent confirmation ("a clean model run... proved the (B)-empty lemma
independently"). Read directly, `TIME_PROMPT_v2.md` line 4 self-declares:
"This is an ANALYTIC PROOF-PROMPT, not a blind discovery." Its Settled fact 5
(lines 48-50) hands the model the exact premise the analytic conclusion turns
on: "A one-way edge is an extra admission." A run that is handed the
conclusion it is later credited with reaching independently is not
independent confirmation of that conclusion, regardless of which model ran
it or how "clean" that model's own session was. This was a real error in the
discharge's own evidentiary claim, not a matter of interpretation, and it is
corrected in `CLOSURE.md`, `AUTHOR_READING.md`, `MECHANIZATION.md`, and
`CLAIM_LEDGER.md` alongside this file.

## What the blind run actually found

Quoting `BLIND_RUN_REPORT_20260916.md` directly rather than re-paraphrasing:

- **(B)-empty: reconfirmed, but as a judgement, not a proof.** "CONFIRMED_BLIND
  with a stated reservation... Call it confirmed as a judgement, unconfirmed
  as a proof" (`HONEST_VERDICT`, paragraph 3). One of the two runs that
  exhibited an argument "says no Lean statement of it exists." This tree's own
  `lean/OrientedBoundary/Basic.lean::b_is_empty` is a real, mechanically
  checked theorem, but — see its own updated docstring — it is a theorem about
  a freely stipulated two-Boolean model, not a derivation from the sealed
  derivation's own primitives; it does not supply the missing independent
  mechanization. As of this reconciliation, (B)-empty stands as: one analytic
  Lean proof of a stipulated model (`OB-B-EMPTY`, unchanged grade, caveat
  added), plus a five-run blind judgement that agrees with it (not itself
  mechanized, graded as a judgement — see `CLAIM_LEDGER.md`'s new
  `OB-B-EMPTY-BLIND-JUDGEMENT` row).

- **The toll runs backwards.** "Direction is free or cheaper; symmetry is
  what is charged" (`DIVERGENCES [1]`, 5/5 agreement). The frozen prediction
  AP2 ("exactly one admitted capability") and AP4 ("[the arrow is] priced-
  and-internal... only after the toll is paid") are both contradicted:
  "the oriented reading's event history is a strict prefix of the symmetric
  one, the witnessing observer costs zero admissions... the analytic run that
  previously scored HIT was handed the (A)/(B) distinction and the statement
  that a one-way edge is an extra admission — it was told the conclusion
  these runs reached the opposite sign on" (`HONEST_VERDICT`, paragraph 2).
  Concretely (`DIVERGENCES [1]`): the cheapest swap-preserving separating
  response costs 2, every cost-1 response is already rigid (breaks the swap
  symmetry), and one run states it as a trilemma — of {the boundary instance
  is derivable, the swap is an automorphism, the two data are separable} at
  most two hold at once, never all three.

## What survives

The report is explicit that the reversal is economic, not structural
(`HONEST_VERDICT`, paragraph 1): "real confirmation of AP3 and of the first
clauses of AP1, AP2 and AP4" — the *unoriented reading is an automorphism*,
the *oriented reading is not*, and the two are *different kinds*, all hold
blind. So `OB-KIND`'s qualitative conclusion — an order is a kind of admitted
relation, not a container, because the two have different existence
conditions — is not contradicted by the blind run; only the specific
quantitative claim ("priced... exactly one capability", in the direction
`CLOSURE.md` originally stated it) is. `OB-KIND` and `OB-SF-OPEN-A` are
corrected in `CLAIM_LEDGER.md` to state the kind conclusion without the
now-unsupported toll direction, pointing here for the full account, rather
than being withdrawn outright — see there for the exact wording.

## What this file does not do

It does not re-derive a corrected toll direction as a new theorem. The blind
report itself records real remaining complexity the frozen predictions never
contemplated — an unpayable polarity remainder (`DIVERGENCES [5]`), a
counter-level where oriented and unoriented collapse (`DIVERGENCES [4]`), two
non-isomorphic tied minima (`DIVERGENCES [3]`, `[9]`), two tolls of opposite
sign that no declared measure sums (`DIVERGENCES [6]`) — and asserting a
single clean "symmetry costs 2" theorem here would repeat exactly the mistake
being corrected: reaching for a tidy conclusion the evidence does not yet
license as a proof. What changes here is narrower and load-bearing anyway:
the discharge's citation of independent confirmation was wrong, and the
specific toll-direction claim it rested on does not survive blind testing.
Both are now recorded, not smoothed over.
