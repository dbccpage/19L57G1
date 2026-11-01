# Textbook handoff: completed work and remaining work

Updated: 2026-11-01. AuthorityEffect: None.

## Start here

The book is substantially written. Continue toward a correct, approachable
textbook for a determined teenager with no assumed philosophy or mathematics
background. Use concrete examples, explicit assumptions and clear boundaries
between model results and observations about reality.

**Review consolidation is now recorded in [the remaining-issues register](TEXTBOOK_REMAINING_ISSUES.md).
Research placement is now recorded there too. Next task: PATH-01, the core-route reading.
Do not start another small
chapter-polishing cycle or another laboratory.**
Reuse work already checked. Fix substantive errors and prerequisite gaps first;
batch ordinary grammar corrections with those fixes. Do not spend effort
repeatedly changing acceptable wording or rechecking unchanged material.

The author has already said that they read the material and found it acceptable.
Do not ask again for a willing beginner or make a new participant a condition
of finishing the text. That feedback is not an independently measured result
for other readers, a reading-speed guarantee or a delayed-retention study.

## Exact resumption state

These pins were verified immediately before this documentation-only handoff.
The handoff commit advances the source branch; it does not change the published
teaching edition or extend the earlier test receipts to a new commit.

| Item | Verified state |
|---|---|
| Repository | `dbccpage/19L57G1` |
| Working branch | `codex/native-path-reading` |
| Last validated/published teaching source | `26c06c086421776e31f2301f254c570dfb6ef472` |
| `main` | `14d23a98830a4e6916b0e50810f0bc6ca17a05cf` |
| Published Wiki commit | `71ff97f288f55775e9e2d36c2b185b539d6dd52b` |
| Working PR | #296, OPEN, DRAFT, unmerged, directly against `main` |
| Workspace | `C:\Users\a343o\.codex\worktrees\institutions-reading-review\19L57G1` |
| Existing Wiki checkout | `C:\Users\a343o\.codex\worktrees\5ce4\19L57G1\artifacts2\wiki-review\wiki` |
| Last teaching batch | Units 17–22, practice/answers, completion audit and phone-table fix |

The teaching batch finished; it leaves no pending render, build or publication
job to resume. Refresh Git/PR/Wiki state before the next write. Preserve unrelated
dirty work. The author merges; do not merge or open a stacked PR.

Public entry points: [Wiki](https://github.com/dbccpage/19L57G1/wiki),
[completion status](https://github.com/dbccpage/19L57G1/wiki/textbook_completion_status),
[reading path](https://github.com/dbccpage/19L57G1/wiki/textbook_learning_path),
[PR #296](https://github.com/dbccpage/19L57G1/pull/296).

## What has been done

“Done” below names the actual delivered scope. It does not certify exhaustive
semantic coverage of every source declaration or measured novice learning.

| Delivered area | Completed scope | Durable source/evidence guide |
|---|---|---|
| Curriculum and entrance | 75 derivation Units, 18 institution Units; all 93 have First pass openings; a core reading path and ten beginner routes exist | [Reading path](textbook/learning_path.md), [textbook hub](textbook/README.md) |
| Foundations and examples | Cards, tests, profiles, witnesses, rules, hypotheses, counterexamples, recovery, demands and repairs have worked introductions and changed practice | `textbook/first_steps/`, `reasoning_lab/`, `search_lab/`, `change_lab/` |
| Mathematical/application tools | Map, Path, Number, Growth, Boundary and Same-record routes; selected protocol, calibration, clock, composite, valuation, process and interpretation lessons | [Audit index](textbook/audit/README.md); route source guides and answer pages |
| Institutions | All eighteen Units have dated scoped reviews, including signatures/recovery, alignment, policy, acquisition and grounded verdicts | `textbook/audit/INSTITUTION*_REVIEW_*.md`; reuse these reviews rather than restart them |
| Source placement | All 75 sealed modules mapped to Units; a restricted census reconciles 2,564 source declaration heads with compiled locations | [Coverage matrix](textbook/derivation_coverage.md), [declaration review](textbook/audit/DECLARATION_REVIEW_2026-10-28.md) |
| Early formal Units | Recent passes cover Units 00–22 with smaller examples, explicit hypotheses, optional formal walkthroughs and separate changed practice | [Audit index](textbook/audit/README.md); core, state/history, context, admission and repair reviews dated 2026-11-01 |
| Later formal Units | Dated selected reviews/corrections already exist across the later topics; do not label everything after Unit 22 untouched | The remaining dated review files in [the audit index](textbook/audit/README.md) |
| Context search | Book proofs supply sound/complete finite search for the native context grammar and witness extraction; an instance alone need not separate under a uniform rule | [Context review](textbook/audit/CONTEXT_READING_REVIEW_2026-11-01.md) |
| Units 11–16 | Initial-store/successful-replay conditions, fresh-data comparisons, witness scope, separate relation models and request-only invariance clarified; twelve practice questions added | [Admission review](textbook/audit/ADMISSION_READING_REVIEW_2026-11-01.md) |
| Units 17–22 | Guard versus self-separation, replay versus all-request validity, cost order and renaming clarified; reading F correctly retains three data; twelve practice questions added | [Repair review](textbook/audit/REPAIR_READING_REVIEW_2026-11-01.md), [practice](textbook/repair_practice.md), [answers](textbook/repair_answers.md) |
| New repair proofs | Multi-request example proves target-only repair can be invalid; general zero-new-instance and zero-new-form-arity results support cost floors | `textbook/checks/u17_lean.py`, `u19_lean.py`, `u22_lean.py`; no sealed source changed |
| Videos | Twelve corrected Manim MP4/GIF pairs published; wrapping, reserved regions and transition cleanup address overlap; 90 settled states and sampled frames reviewed | [Video review](textbook/media/REVIEW_2026-10-28.md); not a claim about every interpolation frame |
| Wiki | Complete lesson before optional video; all 93 Unit bodies tied to their own source pins; original 601 quoted code blocks preserved; selected desktop/phone navigation checked | `textbook/media/build_wiki_textbook.py`, `unit_page_custody.py`; latest receipts below |
| Research inventory | 123 canonical trees inventoried; 18 have selected dedicated introductions; 105 have no dedicated treatment established by that inventory | [Research inventory](textbook/audit/research_inventory.md) |
| Completion audit | Existing content, remaining requirements and an ordered closure plan are now public | [Completion status](textbook/completion_status.md) |

Eighteen introductions are not eighteen fully taught research trees. The other
105 trees are **not automatically 105 missing chapters**: tooling, historical
experiments, duplicate developments and open questions may belong in references
or receive justified omissions.

## Remaining work, with dependencies and stopping conditions

| ID | Status | Depends on | Concrete next deliverable | Finished when |
|---|---|---|---|---|
| H0 | DONE | — | Preserve this handoff and published state | Document is available from the working branch; pins and receipt scope are explicit |
| R1 | DONE, selected-review scope | H0 | [Remaining-issues register](TEXTBOOK_REMAINING_ISSUES.md), covering all 93 Units with reusable review evidence and a prioritized gap list | No whole-book semantic certification is implied; use the register's explicit next actions |
| R2 | TODO | R1 | Repair the identified wrong claims, broken examples and prerequisite jumps; include ordinary grammar corrections in those batches | Each issue has a source-grounded resolution and appropriate example/proof/check; no unresolved blocker is hidden by prose |
| R3 | DONE, editorial scope | R1 | [123-tree placement](textbook/audit/RESEARCH_PLACEMENT_2026-11-01.md), with source identities and a bounded two-introduction gap list | Existing 18 introductions retained; 88 references, eight open-question roles and seven standalone omissions; EXT-01/EXT-02 remain to be written |
| R4 | TODO | R2, R3 | End-to-end reading of the chosen core route and its changed-example practice | Required terms are explained before use; examples and answers agree; optional branches stay optional; model/observation boundaries remain explicit |
| P1 | TODO | R4 | Final source/Wiki publication verification and concise release status | Changed pages/assets are published from verified sources; links, source pins and relevant layouts work; remaining mathematical questions are labelled open |
| M1 | AUTHOR CONTROLLED | Separate merge decision | Full local merge contract, then author review/merge | Twelve gate families actually run locally before asking for merge; no absent hosted check is treated as a defect |

R2 and R3 can be organized independently after R1; they do not require new
infrastructure. A compact Markdown issue table is enough: ID, lesson/topic,
source/review pointer, actual defect, priority, resolution and status. Do not
replace R1 with another generic roadmap or repeat the completed early batches.

## Verification already available

The following receipts apply to teaching source
`26c06c086421776e31f2301f254c570dfb6ef472`, **not automatically to later edits**:

- Canonical local textbook job: 5/5 selected steps passed, including 106 Python
  checks and 79 book-Lean drivers, with isolated Python 3.14.7/pinned requirements.
- Unit 17–22 selection: 97 distinct exact axiom reports: three empty, 40 exactly
  `propext`, 54 exactly `propext, Quot.sound`; 21 calculation guards and three
  rejected false witness claims. Initial failures are separate from successful runs.
- Wiki authoring/custody: 13 tests passed. Vocabulary/identifier selection: two
  tests passed, 17 deselected. Prose census unchanged: 49 terms / 141 files / 1,898 hits.
- Generated Wiki: 3,105 internal links; published mixed-edition Wiki: 3,102.
  All 93 complete Unit/source-pin checks passed.
- Raw Wiki verification has 17 known SVG checkout line-ending differences;
  all 28 published SVGs match source Git blobs. Do not describe that raw run as
  an unqualified pass or needlessly rewrite the preserved figures.
- Latest publication preserved 585 unselected files, both author-edited beginner
  pages, twelve MP4/GIF pairs, fourteen Reasoning assets and 601 source code blocks.
- Six Unit predictions and lesson links, three four-question groups and answers,
  optional details, the completion-page link and named Unit 19/22 phone tables
  were checked. Those tables fit 390-pixel viewports; the viewport was reset.
- The full twelve-family merge contract was **not** run. No hosted CI is used
  or expected. Software checks establish no physical measurements or reader mastery.

### Local receipt portability

Latest evidence is under `artifacts2/repair-reading-2026-11-01/`, especially:
`textbook_gates.json`, `textbook_gates.log`, `lean_controls.json`,
`source_preservation.json`, `publication_preservation.json`, `hosted_qa.json`,
`wiki_tests.log`, `wiki_verify.log`, `wiki_actual.log`, `firewall.log`,
`prose_watchlist.log`, `pr_final.json` and `complete_evidence.py`.

`artifacts2/` is ignored and does not travel with a fresh clone. A small local
handoff archive is delivered with this document. Preserve it if moving machines;
otherwise retain the exact source pins and rerun needed checks. Do not copy all
scratch builds or caches. Earlier dated source reviews remain tracked and portable.

## Repository and publication rules

- Read [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md). They remain authoritative.
- Do not edit `prompt/`, `paper/`, `code/`, `lean4/Derivation/`,
  `lean4/Derivation.lean`, `artifacts/` or `CLAUDE.md` without explicit author
  authorization. This textbook work also leaves native `research/` sources,
  results, receipts and pins unchanged.
- Do not introduce external citations, change vocabulary populations or modify
  original quoted source blocks. No new research claim becomes a sealed derivation.
- Preserve the author's Wiki `Home.md`, `textbook_first_steps.md` and
  `textbook_reasoning_lab_01_one_answer_per_input.md` unless explicitly asked.
  Generate into scratch and copy only reviewed pages; do not overwrite the Wiki wholesale.
- Reuse the current direct-to-main PR. The author merges. No hosted Actions
  investigation, restoration proposal or CI approval loop.
- Scope checks to the change. Use existing receipts for unchanged content;
  rerun a named check when a change, failure or unresolved concern warrants it.
  Do not rerender unchanged videos or run expensive whole-tree research checks
  merely to improve a status report.

For substantive textbook changes, the established local command is:

```powershell
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/textbook-next.json
```

On this Windows machine, set `PYTHONIOENCODING=utf-8` and use a normal writable
`TEMP`/`TMP` directory before Python/Lean tests; sandbox temp ACL failures are
not evidence that lesson code is wrong. Use the existing installed UV/Python
tools. Do not install or rebuild a toolchain without an actual need.

## Suggested resumption prompt

> Read TEXTBOOK_HANDOFF.md and the repository contract. Verify the current branch,
> PR and Wiki heads. Read TEXTBOOK_REMAINING_ISSUES.md and continue PATH-01:
> follow the selected core route end to end, then address EXT-01 and EXT-02.
> Reuse completed work; focus on substantive errors and prerequisites. Do not start
> another polishing cycle, new laboratory or expensive unchanged-content test run.
> Keep the original beginner-textbook goal intact, publish authorized corrections,
> and leave merging to the author.
