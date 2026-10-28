# Wiki review scope and findings: 2026-10-23

## Source and purpose

This Wiki was prepared against source commit [`85a83ae7ce64dc2123ff218568a4ecd37e566d33`](https://github.com/dbccpage/19L57G1/commit/85a83ae7ce64dc2123ff218568a4ecd37e566d33). The previous Wiki consisted of a one-sentence Home page at Wiki commit `1b253423324716c0c55ae4112385a5c6fe5611d6`.

The review inventories the entire tracked repository and provides detailed navigation and explanations. It is **not** a fresh independent proof audit of every mathematical claim or a full replay of all local gates. Source instructions, sealed bytes, research freeze, verifiers, scanner populations, and CI configuration were left unchanged.

## Complete structural population

| Population | Observed at the reviewed source SHA |
| --- | ---: |
| Tracked files, all areas | 3,147 |
| Canonically indexed research trees | 118 |
| Python files, parsed syntactically | 1,240 |
| Python syntax parse errors under the authoring interpreter | 0 |
| Lean source files, all areas | 526 |
| Modules under sealed `lean4/Derivation/` | 75 |
| Tracked Lean toolchain files | 97 |
| Distinct toolchain pins | 1: `leanprover/lean4:v4.33.0` |
| Root `code/` Python files | 60 |
| Root `tests/` Python files | 61 |
| Statically named root test definitions | 791 |

The last row counts syntax definitions, not collected/parametrized cases, executed tests, or passes. No current theorem count is inferred from regex or filename inventory. Research templates, notes, and the E2E harness are distinguished from the canonical indexed tree population.

The Wiki contains 165 content pages plus a shared sidebar and footer: 118 research-tree references, 14 complete area-file inventories, the research index and Python reference, and 31 curated guide pages including Home.

## Semantic reading performed

The review read the current contracts; main README and paper boundary; core model, observation, candidate, isomorphism, engine, and export interfaces; generated topic/research/build indexes; research orientations and implementation symbol inventories; closeout and Alpha handoff; second-derivation reporting and terminal scope; native/foundations documents; and dated claim-scope corrections. Dedicated reference pages attribute research source descriptions rather than presenting them as independent endorsements.

## Fresh checks for this documentation edition

- Existing research index, lookup indexes, and Lean build-order freshness checks.
- Existing local runner's `--list` mode, which enumerates commands and executes no gate steps.
- All three small [worked examples](worked_examples): inert supply and separation/replay; Challenge-3 class counts; committed closed-L export verification.
- Complete source-path inventory coverage, Wiki navigation target checks, pinned source-link checks, source-line target bounds, UTF-8 and fenced-block checks, and Markdown lint.

The examples and authoring checks ran on **Python 3.12**, not the root job's required Python 3.14. They are documentation smoke checks only. The sealed suite, strict mypy job, full coverage job, all Lean packages, all research verifiers, live injections, and estate custody census were **not** rerun for the Wiki. Historical results are always attributed to their recorded source/date.

## Important findings reflected in the Wiki

| Observation | How this edition handles it |
| --- | --- |
| Root README contains September 19 test counts | Labels them historical, never a fresh current pass |
| README's axiom-scope explanation lags the registered declaration audit | Follows the current detailed contract/workflow and states the exact module population |
| Frozen second-derivation headers still say “not frozen” | Gives precedence to the explicit September 28 freeze record and explains preserved bytes |
| Research registration table reads only the research job | Separately exposes Lean-job path mentions and warns that neither is execution evidence |
| Alpha readiness coexists with an unsatisfied original completion gate | Keeps the three closeout axes independent |
| Custody pin records a known failure | Preserves its red disposition; does not claim all estate verification passes |
| Several research headlines have explicit scope corrections | Carries those ceilings into the atlas, limitations, and per-topic guides |
| Companion repositories can have different Lean/axiom policies | Documents Genesis's actual pins and boundaries without migrating them |

This is a documentation review with explicit evidence ceilings. No new development gates, source repairs, mathematical bridges, publication deposits, or authority promotions were introduced.

## Readability and media review, 2026-10-28

This later pass checks the 267-page Wiki's Markdown structure and focuses
editorial and source-semantic review on the reader guides, textbook
introductions, generated summaries, and twelve Manim scenes. Earlier
snapshot counts and receipts above remain dated records.

Units 08 and 44–74 now separate a short introduction, reading steps,
detailed claims, and formal anchors. Institution 02 adds a small factoring
example, and Institution 17 separates its introduction from the detailed
statement. The glossary and core guides introduce terms before their
reference tables. Fifteen seconds describes an overview video's duration,
not a deadline for understanding a lesson.

Corrections include the source types and direction of factorization in
Unit 71; thirteen effect classes versus the separate 64-descriptor
interpreter family; tuple-valued mu2 cost; actor re-indexing versus output
relabeling; renamed lesson links; and the direct-import versus import-closure
census. Full explanations and validation scope are recorded in the source
file `textbook/media/REVIEW_2026-10-28.md` at this edition's source snapshot.

Fresh local checks passed: the 80-job Lean build, 95 textbook Python
checks, 71 book Lean checks, nine generator/source regression checks,
and text geometry at 90 settled states across all twelve animations.
All twelve MP4/GIF pairs were rendered and checked against the
fifteen-second limit. Geometry and sampled visual inspection do not
certify every interpolation frame or reading comprehension. The full
twelve-family gate contract was not rerun.
