# iso_sound: status and injection record

AuthorityEffect: None.

Baseline: `cea346d7f3603fd8da374947e76c9b3cd426d122`.
Outcome: no falsifier in the declared bound.  General soundness: **OPEN**.

## Injections

| Gate | Injection | Observed failure | Reversed |
|---|---|---|---|
| G1 | `first_split` grouping with two brute labels | returns `(0, 1)` | constant labels return None |
| G2 | hunt record with `general_soundness: PROVED` | `SOUNDNESS_GUARD` | OPEN restores |
| G3 | agreement true with `falsifier_count: 1` | `AGREEMENT_GUARD` | 0 restores |
| G4 | coverage 94% statements / 100% branches | `COVERAGE_STATEMENT` | 95/95 restores |
| G5 | coverage population `{unrelated.py}` | `COVERAGE_POPULATION` | required four files restore |
| G6 | `assume-unchanged` then edit `Example.lean` | `SOURCE_CHANGED`; `git diff` silent | no failure |
| G7 | `sorry` / `mathlib` in a scanned string | forbidden-token / mathlib regex | — |

The hunt itself is not regenerated under a live injection.
