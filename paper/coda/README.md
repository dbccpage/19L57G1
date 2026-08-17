# Coda

**[declared metatheory]** This tree is a clean-slate recreation. Each
layer names one external paper as a read-only frame of reference and
keeps only a plain-language skeleton of the subject. The external
paper, its formalization, its code, its change log, and its claim list
are not imported.

**[declared metatheory]** The seed-prompt derivation (`paper/paper.md`
and `lean4/Derivation/`) stays a separate object.

Each layer folder holds three markdown files next to each other: the
paper `{acr}.md`, `{acr}_change_log.md`, and `{acr}_claims_ledger.md`.

A Lean claim file is created if and only if a ledger row has surface
`lean`. Its name is exactly the row id: `{acr}_claim_<uuid>.lean`, with
the same 32 lowercase hex digits and no hyphens. Prose-only rows and
rows mechanized in code do not get a Lean file.

| folder | external file (not imported) | skeleton |
|---|---|---|
| `foc` | `000_coda_foc.md` | two-stage leftover on a finite packet |
| `fda` | `001_coda_fda.md` | standing needs a finite record and a stop |
| `mur` | `002_coda_mur.md` | rewriting does not keep standing for free |
| `or` | `003_coda_or.md` | combining views does not raise standing |
| `cs` | `004_coda_cs.md` | continuum talk factors through finite samples |
| `q` | `008_coda_q.md` | holding rule for questions too large to claim |
| `b_cs_q` | `005_coda_cs_q_bridge.md` | gate from samples to those questions |
| `gtla` | `007_gtla.md` | moving evidence does not create standing |
| `gtoc` | `010_gtoc.md` | every extra structure is a paid import |

A folder is not an admission. Receipts are generated as work proceeds.
The layer sequence is a reserved plan, not a proved necessity.
