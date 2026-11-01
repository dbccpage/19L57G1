# Textbook handoff: delivered edition and remaining boundaries

Updated: 2026-11-01. AuthorityEffect: None.

## Current status

The requested editorial and publication work is complete. The final
status-page verification is recorded below. The book retains all 75 derivation
Units, eighteen Institution Units, ten beginner routes and twenty selected
research introductions. It starts from concrete examples without assuming
philosophy or formal mathematics study. No new lesson batch is waiting.

Use [the release audit](textbook/audit/RELEASE_AUDIT_2026-11-01.md) for the
requirement-by-requirement decision and [the issue register](TEXTBOOK_REMAINING_ISSUES.md)
for closed work and conditional future items. Do not restart chapter review,
repeat unchanged proofs or add another laboratory merely to keep working.

The author reported reading the material and finding it acceptable. Do not
ask again for a willing beginner or impose a new participant requirement.
That acceptance is not a measured reading-speed, other-reader mastery or
retention result. The book includes changed-example practice and separate
answers; software checks do not measure a reader's intuition.

## Verified source and publication state

| Item | State |
|---|---|
| Repository / branch | dbccpage/19L57G1 / codex/native-path-reading |
| Checked teaching source | d0386aee976e9dc46eec6cb6548ca8376faee0d3 |
| Canonical local textbook job | Five of five selected steps; 108 Python checks; 81 book-Lean drivers |
| Interpreter and receipt custody | Python 3.14.7; pinned dependencies; clean source; identical start/end HEAD |
| Published teaching Wiki before final status edits | a14e9cc12a8a52faf862e18e19610977bdc9b66b |
| main at release review | 14d23a98830a4e6916b0e50810f0bc6ca17a05cf |
| PR | #296; OPEN, DRAFT, directly against main; unmerged |
| Source workspace | `C:\Users\a343o\.codex\worktrees\institutions-reading-review\19L57G1` |
| Wiki checkout | `C:\Users\a343o\.codex\worktrees\5ce4\19L57G1\artifacts2\wiki-review\wiki` |

Final status-page publication has its own receipt under
`artifacts2/release-audit-2026-11-01/`. The final documentation checkpoint may
advance the source branch; it does not change the checked mathematics,
examples, videos or the scope of the d0386aee teaching receipt. Refresh remote
heads before any later write. There is no pending render or build to resume.

Public entry points: [Wiki](https://github.com/dbccpage/19L57G1/wiki),
[reading path](https://github.com/dbccpage/19L57G1/wiki/textbook_learning_path),
[completion status](https://github.com/dbccpage/19L57G1/wiki/textbook_completion_status),
[PR #296](https://github.com/dbccpage/19L57G1/pull/296).

## What has been done

| Area | Delivered scope | Evidence guide |
|---|---|---|
| Complete curriculum | All 93 formal Units have First pass openings; all have reusable dated selected semantic/readability reviews | [Review register](TEXTBOOK_REMAINING_ISSUES.md), [audit index](textbook/audit/README.md) |
| Core entrance | First steps → Reasoning 00–07 → Search → Change → formal guide → Unit 00; 29 numbered lessons and 45 reconciled tasks | [Core-route review](textbook/audit/CORE_ROUTE_READING_REVIEW_2026-11-01.md) |
| Reasoning and tools | Worked labels/tests/profiles, witnesses, conditionals, hypotheses, recovery, demands/repair, arithmetic/fractions, maps, paths, growth and selected research applications | [Reading path](textbook/learning_path.md), route source guides and separate answers |
| Early formal Units | Units 00–22 now separate representation, state/history, contexts, admissions, all-request validity, cost order and renaming; changed practice and source-grounded corrections are retained | Core/state/context/admission/repair reviews in the audit index |
| Later Units and Institutions | Dated reviews/corrections cover all later Unit ranges and all eighteen Institution Units; source hypotheses and separate models remain explicit | The register assigns each Unit exactly once to its reusable review |
| Research placement | All 123 trees classified: twenty selected introductions, 88 references, eight open-question roles and seven standalone omissions | [Placement decisions](textbook/audit/RESEARCH_PLACEMENT_2026-11-01.md), companion JSON |
| EXT-01 | Reasoning 62–64: supports, conflict/retraction choices, cascades and consistency versus truth; ten changed questions and separate answers | [Revision review](textbook/audit/REVISION_READING_REVIEW_2026-11-01.md) |
| EXT-02 | Reasoning 65–67: FIFO memory, projection/envelope/license stages, refusal and no-change success; ten changed questions and separate answers | [Agency review](textbook/audit/AGENCY_READING_REVIEW_2026-11-01.md) |
| Source placement | All 75 sealed modules mapped; 2,564 source heads reconciled with compiled locations under the recorded scanner scope | [Coverage matrix](textbook/derivation_coverage.md), [declaration review](textbook/audit/DECLARATION_REVIEW_2026-10-28.md) |
| Videos | Twelve corrected Manim MP4/GIF pairs; wrapping, reserved regions and transition cleanup; 90 settled states and sampled frames reviewed | [Video review](textbook/media/REVIEW_2026-10-28.md) |
| Publication/custody | All 93 complete Unit bodies tied to their own source pins; all 601 original quoted blocks retained; author pages and existing media preserved | Current publication and release receipts below |
| Rendered review | Both new branches, six predictions, two ten-question/answer packets, route returns and the formal entrance work; three named phone tables fit | release-audit hosted_qa.json and screenshots |

Twenty introductions do not mean twenty fully taught research trees. The
other 103 trees are not 103 automatically missing chapters. Reference,
open-question and omission roles have explicit reasons and source identities.

## What remains

There is no retained P1 textbook task after final publication verification.
The following boundaries are explicit:

- **Author-controlled merge:** PR #296 remains draft and unmerged. The full
  twelve-family local contract has not run. Run it before asking for a merge;
  do not infer merge clearance from textbook receipts. No hosted CI is used.
- **Conditional exhaustive coverage:** no claim is made to teach every
  auxiliary source declaration. A future exhaustive claim would require the
  additional reconciliation described by COV-02.
- **Optional learner evidence:** independent timing, retention and broader
  reader trials could support stronger claims; none is invented or required
  again from the author. See LEARN-01.
- **Open research:** named mathematical questions remain open. The textbook
  release does not prove them or supply new physical observations.

## Checks and portable evidence

The canonical receipt at d0386aee is under
`artifacts2/agency-reading-2026-11-01/textbook_gates.json` and its log.
It includes the new X302/X303 wrappers. Additional checks include:

- X302: 3,456 finite notebooks; 3,771 returned candidate replays; eighteen
  exact native theorem reports (seventeen empty, one propext).
- X303: 36 FIFO cases; 2,304 controller cases (672 successes, 1,632 refusals);
  sixteen exact separate-model reports (propext, Quot.sound).
- 123 Reasoning authoring tests and fourteen Wiki authoring/custody tests.
- Both vocabulary firewall checks; unchanged prose census of 49 terms,
  141 files and 1,898 hits. No vocabulary population changed.
- Complete Unit/source-pin checks and original-quotation comparisons.
  The raw Wiki verifier's seventeen known SVG checkout line-ending differences
  are qualified separately; all 28 published SVGs match source Git blobs.
- Live keyboard navigation, named phone samples and restored 1280-pixel
  viewport. These are samples, not a full accessibility audit.

`artifacts2/` is ignored and does not travel with a fresh clone. Keep the small
`artifacts2/textbook-handoff-2026-11-01.zip` when handing off to another machine.
It contains the current handoff/register, dated release audit, source guides,
selected controls, canonical/publication receipts and small screenshots.
It excludes toolchain caches and scratch builds. Tracked dated reviews remain
available directly from the branch. Receipt scopes and source pins stay literal.

## Rules for later maintenance

Read [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md). The author merges; do
not merge or create a stacked PR. Preserve unrelated dirty work and refresh
source/PR/Wiki heads before writes. Never treat absent hosted Actions as a defect.

Do not edit sealed paths, CLAUDE.md, native research sources/results/receipts,
frozen pins or original quoted blocks without explicit author authorization.
Preserve Wiki Home.md, textbook_first_steps.md and the author-edited Reasoning
Lesson 01. Generate into scratch and copy only reviewed pages.

For a substantive later teaching/check change, use the canonical local job:

```powershell
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/textbook-next.json
```

On Windows, use PYTHONIOENCODING=utf-8 and writable TEMP/TMP directories.
Reuse existing receipts for unchanged sources; rerun only checks justified by
a change, failure or specific unresolved concern. Do not rerender unchanged
videos or start a new research campaign as routine maintenance.
