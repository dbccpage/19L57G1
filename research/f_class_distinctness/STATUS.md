# f_class_distinctness: status and injection record

AuthorityEffect: None.

Baseline: `cea346d7f3603fd8da374947e76c9b3cd426d122`.
Outcome: five named reading-F classes pairwise non-isomorphic.
Catalog completeness: **OPEN** as a Lean theorem.

## Injections

| Gate | Injection | Observed failure | Reversed |
|---|---|---|---|
| G1 | `pairwise_iso_hits` non-empty / `pairwise_noniso: false` | `ISO_HITS_GUARD` / `PAIRWISE_GUARD` | empty hits restore |
| G2 | `catalog_completeness: proved` | `CATALOG_GUARD` | engine-enumeration scope restores |
| G3 | F Lean cites `U0_not_iso_BL` | `test_lean_does_not_cite_l_distinctness_theorems` | names absent restore |
| G4 | coverage 94% statements / 100% branches | `COVERAGE_STATEMENT` | 95/95 restores |
| G5 | coverage population `{unrelated.py}` | `COVERAGE_POPULATION` | required two files restore |
| G6 | `assume-unchanged` then edit `Example.lean` | `SOURCE_CHANGED`; `git diff` silent | no failure |
| G7 | `sorry` / `mathlib` in a scanned string | forbidden-token / mathlib regex | — |

The Lean record and the class record are not regenerated under a live
injection.
