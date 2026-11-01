# Declaration coverage, batch 1: consistent choices across presentations

2026-11-01. AuthorityEffect: None.

## Result

The one-symmetry idea is already taught. The next useful addition is a short,
worked continuation showing when choices at several presentations agree.
This batch identifies five explanation or scope gaps in that cluster. It
does not establish five mathematical defects or five missing chapters.

The highest-priority scope issue is Unit 70's unqualified statement that
naturality across connecting arrows remains OPEN. That describes what the
sealed fixtures do not exercise; it is not the current state of the related
post-seal research. The latter supplies a criterion with explicit inputs.

This is the first bounded batch requested by the author, estimated at one
hour. It delivers an inventory and teaching plan, not new lessons, a Wiki
publication, a new proof audit, or an exhaustive coverage claim.

## Exact population and evidence boundary

Source snapshot: `1c9ad34b834671d0d71a26c7d3ce539d29fa551a` (merged PR 296).
The companion [JSON crosswalk](declaration_coverage_batch_01.json) records
source locations, Git blob identities, raw file hashes, individual decisions
and a dependency graph for the next batches.

- **Sealed:** all twelve source declaration heads beginning at lines 222–290
  and 497–550 of [PresentationNaturality.lean](../../lean4/Derivation/PresentationNaturality.lean).
  Those are the two family/section/obstruction interfaces, not the entire
  module. Dependency definitions and fixtures elsewhere in the module were
  consulted; they are not silently added to the counted population.
- **Research:** all 41 source declaration heads in
  [NaturalSections.lean](../../research/natural_sections/lean/NaturalSections.lean):
  24 theorem heads and seventeen other heads. This is one file of one research
  tree, not its later layer, repair, sign, or physical-model developments.
- **Total:** 53 source heads. The existing comment-aware scanner enumerates
  them independently of the manual disposition groups. Constructors, fields,
  generated constants and every declaration in the repository are different
  populations. No new compiled-name/axiom census was run for this audit.

Teaching evidence was read in [Unit 70](../units/70_can_a_pair_be_chosen_in_a_way_every_relabelling_respects.md),
its two book drivers, [Unit 72](../units/72_round_trip_coherence_quotient_retention_and_the_fidelity_closure.md),
the Map and Path routes, the [earlier selected review](DESCENT_READING_REVIEW_2026-10-31.md),
and the owner's [status](../../research/natural_sections/STATUS.md), especially
its first three sections and many-object criterion. Source reading supports
the classifications below; name matches alone do not establish explanation.
Absence findings concern this cluster and these teaching locations, rather
than a certified semantic search of every paragraph of the book.

The 137-step merge receipt for the unchanged snapshot is reusable background
evidence. It is not a proof that every research file is verified by that
contract, nor a check of a later teaching change. This batch changes no sealed
source, native research result, receipt, original quotation or video.

## Gaps worth teaching

| ID / priority | Existing coverage and actual gap | Beginner-sized addition and acceptance check |
|---|---|---|
| DC-01 / P2, dense existing coverage | Unit 70's opening correctly distinguishes a chosen ordered pair from a symmetry-respecting one. Its later explanation and 24-permutation summary already require two fixed, distinguished endpoints. The research's one-fixed-point and blind-observer counterexamples are not presented together as a worked beginner checklist. | Show three separate questions: does the observer distinguish this pair; are both endpoints unchanged; does this same pair work for every required comparison? Use a four-card cycle with one fixed card, a blind observer with identity, and the existing positive two-fixed-card case. A changed prediction must distinguish an unavailable pair from an available pair moved by a symmetry. This expands an existing idea; it is not a new discovery. |
| DC-02 / P2, worked continuation missing | Unit 70 lists `HFamily`, `HSec` and `HIsNatural`, but its two-object fixtures have no cross-object arrows. Map teaches translation and Unit 72 teaches a different network-descent target. Neither supplies the research criterion's connected pair-selection example. | Use two desks with two cards each. One comparison preserves order, another swaps it. Tabulate the pair selected at both desks and test both comparisons. First use only the preserving arrow as a positive control, then add the swapping arrow. Explain that a listed arrow constrains the choices; it is not an instruction to change the supplied family. |
| DC-03 / P2, common-choice constraint missing as a worked example | The fixed-pair test for one symmetry is covered. A beginner still needs to see why separate successful tests can choose incompatible pairs when several comparisons must hold together. | On four distinct cards, one comparison swaps 0/1 and fixes 2/3; the other swaps 2/3 and fixes 0/1. Each fixes two admissible ordered pairs; their fixed-pair sets have empty intersection. The same choice must satisfy both. This shows failure of checking each named comparison separately, not a counterexample claiming every possible closed walk individually has a fixed pair. |
| DC-04 / P2, research criterion lacks a beginner route | Path introduces walks and closed walks; Unit 72 already shows a loop obstruction to faithful carrier descent. The selected research file adds a constructive base-and-route criterion for choosing admissible pairs, including a sufficiency direction not supplied by those examples. | Use a three-desk loop. Supply a base desk and routes, carry one ordered pair out along them, then check each remaining arrow. Change one arrow to a swap and predict the conflict. Only afterward name `Forest`, `spread`, generator and closed-loop transport. State the shared-base hypothesis for the closed-loop form and keep the base/path data explicit. Include a successful all-identity case. |
| DC-05 / P1, research handoff needs clearer scope | Unit 70, “What has not been proved,” says connecting-arrow naturality “remains OPEN.” The sealed negative/positive fixtures indeed omit cross arrows. Research proves `natural_section_iff_generators` and, with `hroot`, `natural_section_iff_holonomy` for a supplied `HFamily`. | Narrow the old OPEN wording to the sealed fixtures and link the post-seal criterion. Explicitly retain the unproved general flat `Family` to `HFamily` embedding and the separate selector-reduction question. Do not say the research solves Unit 72's `AllLoopsTrivial` to `FaithfulNetworkDescent` converse: that has another target type. |

P1 here means a scope statement worth clarifying first in this new
continuation. It does not reopen the completed editorial release wholesale.
P2 means a useful extension for the author's requested deeper coverage.

The research continuation must retain these hypotheses when it is written:

- The arrows carry `PresIso` data preserving the observer, not arbitrary
  maps supplied merely because they connect two drawings.
- Both iff statements quantify over one function `p : HSec D`. Do not replace
  that input with separate existence claims at each base and silently assemble
  a choice function. The chosen examples can list that function explicitly.
- `Forest` supplies roots and walks; its type does not require a graph-theoretic
  acyclic forest. The generator form needs no further root-compatibility
  hypothesis. The closed-loop form adds `hroot`, equal roots along every
  declared arrow.
- The loop criterion fixes the selected admissible pair, rather than every
  carrier point. It is not Unit 72's stronger `AllLoopsTrivial` condition.
  The theorem allows arbitrary carriers and arrow types; checking a finite
  list of generators is executable only for explicitly finite supplied data.

## Why these declarations do not become 53 new lessons

Each name has an individual row in the JSON. Dispositions mean:

- `reuse`: the selected concept is already explained. Reuse the existing
  Unit, exercise or book argument, while retaining any density gap above.
- `expand_existing`: retain the existing explanation and add the named
  worked connection. The declaration is not mathematically absent.
- `add_example`: a source result or construction needs the named beginner
  example if this research extension is taught.
- `auxiliary_reference`: keep the implementation/proof law in the source
  guide. Explain its role with the main example; it does not need a standalone
  lesson or a paragraph for every Lean helper.

The research fixed-pair equivalence is already proved independently in the
book's `Textbook.U70.natural_section_iff_fixed_pair`. Do not add a duplicate
chapter just because the research declaration has another namespace.
Inverse, concatenation and reverse-transport lemmas support the walk example;
their individual Lean proofs belong in the optional reference.

## Small examples checked in this audit

These supplied finite tables test the proposed explanations, not the Lean
theorems or a correspondence with reality. They are not yet textbook lessons.

| Example | Expected and checked result |
|---|---|
| Equality observer on four cards; fix 0 and cycle 1→2→3→1 | One fixed card; zero fixed admissible ordered pairs |
| Blind observer on two cards; identity transport | Two fixed cards; zero admissible pairs |
| Equality observer; swap 0/1 and fix 2/3 | Fixed admissible pairs exactly `(2,3)` and `(3,2)` |
| Two four-card comparisons, swapping disjoint pairs | Each comparison has two fixed admissible pairs; no common fixed admissible pair |
| Two two-card desks, one identity comparison | Two compatible pair assignments; adding a parallel swap leaves zero |
| Three two-card desks, identity arrows around the loop | Two compatible assignments; replacing the return arrow by a swap leaves zero |

These examples explain why output type, admissibility and simultaneous
agreement matter. They supply no physical law, preferred selector or theorem
that every observer must distinguish something.

## Next hour-sized batches

| Batch | Estimate | Depends on | Reviewable result / stopping point |
|---|---|---|---|
| B01 — this audit | About 60 minutes | None | 53-row crosswalk, five gaps, checked finite teaching tables, source boundaries and this plan |
| B02 — fixed-point checklist and scope handoff | 45–60 minutes | B01 | Short Unit 70 continuation for DC-01; repair DC-05's OPEN scope; changed prediction/answer; focused source/authoring checks |
| B03 — connected choices | 45–60 minutes | B02 | Two-desk worked example and disjoint-fixed-pair exercise for DC-02/03; positive and negative finite controls; retain ordered-pair output |
| B04 — base routes and loop consistency | 45–60 minutes | B03 | Three-desk example for DC-04; explicit supplied routes and common base choice; conditional research source guide; changed practice |
| B05 — next coverage audit | About 60 minutes | B01 | Inspect the complete eleven-head `QuotientRetention` module and its Unit 72 treatment; select a small related research slice only after checking existing coverage |

These are estimates, not a commitment that teaching, rendering, publication
and all merge gates fit one hour. Check at each boundary. Reuse unchanged
proof/media receipts. A substantive new teaching change needs its relevant
checks and the canonical textbook job before publication; if that does not
fit, retain the checkpoint instead of claiming completion. Full merge checks
remain separate. The author controls a future merge.

The remaining 2,552 sealed source heads and research declarations outside
the selected file have no new disposition from this batch. Existing reviews
and placement decisions still apply. Subsequent batches can find further
gaps; this report is deliberately not the global remaining-chapter count.

## Validation and handoff

The local audit receipt records an independent source-head/group comparison,
all source hashes and quoted teaching anchors, Markdown links, and the six
finite example families above. It is saved under
`artifacts2/declaration-coverage-batch01/`. The JSON crosswalk is tracked;
local build scripts and detailed receipts are also retained in a small
portable archive beside that directory. No full proof rebuild or video render
is necessary to identify these documentation gaps.
