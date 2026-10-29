# Early formal chapters: reading and scope review

AuthorityEffect: None. Scope: first-pass explanations in Units 04–16
and the specific claims below. This changes teaching prose and book
checks only. Sealed sources, their comments, research sources, and
native receipts remain read-only.

## Reading order

Each of the thirteen chapters now starts with a short worked first pass
before the formal definitions. Classification and source metadata sit
in an optional disclosure. Existing unit IDs and source links remain
stable. The first passes separate one principal question, an example,
a prediction, and its limit. They do not set a reading-time target.

Examples include a caller choosing an existing event kind, copied
position indices selecting the wrong objects, a duplicate becoming a
supply during erasure, multiple holes receiving the same datum, an
already populated starting store, and a newcomer forming a new class.
The separate relation setting uses Bool only as two position labels;
`false` and `true` are not themselves asserted claims about those positions.

Generated hub and homepage copy still advertised study in fifteen-second
soundbites and every-definition coverage. The follow-up removes those
promises across the overview, institution, coverage, audit, video, and home
introductions. The duration bound remains a property of video previews.
Source placement does not establish complete teaching coverage. Snapshot
links carry the source revision without a hard-coded generation date.

## Selected semantic findings

| Units | Original problem | Repair and authoritative evidence |
|---|---|---|
| 04 | Closure of the event type was described together with absence of an event-producing policy | Six constructors bound event kinds; they do not prevent an external policy using those kinds. A supplied book policy admits a fixed token, then designates it on repetition. The no-event replay fact is not a law of elapsed physical time. |
| 05 | The prose twice said each reading's target was ill formed in the other reading | F's `(1,2)` is out of range in L; L's `(0,1)` is accepted in F but selects ⟨⟩/⟨A⟩. The new token-aware replay theorem and actual Python replay check the accepted wrong pair. Claims that every later theorem covers both readings are restricted to the named results. |
| 06–07 | Representation storage, observation, and theorem transport were blurred | TRegime stores token labels externally; the erased ledger lacks a character-inspection judgment. The theorem is an erasure simulation between two Lean models. It transports properties through that erasure, not arbitrary token-sensitive claims or a proof over Python source. |
| 08 | A raw context record was introduced as already admitted and well formed | A raw record has a form index and slots. The four guards decide whether it counts as a test. All holes receive the same tested datum. Absent positive derivability is not a negative measurement. |
| 09, 16 | The explanation claimed the displayed proofs established `¬ collapsed → separable` | They establish `collapsed ↔ ¬ separable`. The new book proof records its exact negation, `¬ collapsed ↔ ¬¬ separable`, without eliminating the double negation. The per-context decision in Unit 16 is distinguished from a decision over every context. Complete finite enumeration needs a separate completeness argument. No assertion is made that the stronger direction is false for the current finite grammar. |
| 10 | “Internally the same” could identify datum indices; existence of an instance could be read as sufficient for separation | Collapse means equal context answers, not equal indices. The redundant-instance check under an existing uniform rule leaves the pair collapsed. The absence-of-instances theorem gives a necessary condition, not sufficiency for any chosen instance. Lean R2L/R2F include the later demand, unlike Python's pre-demand base histories. |
| 11 | The opening omitted the initial AtMostTok condition; a seven-event search's None was glossed as never | The opening requires an empty or singleton matching store and successful replay. An empty history from `[5,7]` satisfies the history condition yet keeps two tokens and fails the initial invariant. Search None means not reached within its horizon; the independent induction theorem supplies the all-length result. Histories remain external records. |
| 12 | Avoiding one target was said to preserve its collapse with anything; fresh data were said to add contexts and no power | R3 requires avoiding both targets. Adding marked(1) avoids 0 but separates 0/1; marking only 2 preserves that pair. Unary context lists stay unchanged during growth; a binary list can grow from five to seven. With two old marked data, a fresh unmarked datum raises the class count from one to two while preserving the old pair. The title now states preservation of old comparisons. |
| 13–15 | A supplied token could be read as requiring a Supply event; point factoring and the empty relation used overly broad analogies | The second-token theorem requires a datum-admission event with another token, not an earlier Supply event. The one-point map has one fixed output; it is not a moving pointer. PrimDiff defines a relation, not a Regime event history. An empty relation still has a supplied carrier, while asserting no pairs. |

The formal `collapsed_append_unmentioning` statement supplies **both**
avoidance hypotheses. Its source introduction uses shorter wording
about one datum; the textbook now follows the formal hypotheses explicitly.
No sealed comment or theorem is edited.

The ordinary `by decide` used in the closed replay examples requires
a goal without free variables in its expected type. A rejected scratch
attempt confirmed that restriction; the published text retains it.
Decidability alone is not a proof of every requested assertion.

## New checked book evidence

There are nine additional named book theorems:

| Script | New report | Meaning |
|---|---|---|
| u05 | F_with_L_demand_accepted | Valid indices can select the wrong pair |
| u09 | not_collapsed_iff_not_not_separable | Exact negation of the existing equivalence |
| u11 | initial_guard_needed | History condition alone does not constrain an arbitrary base |
| u12 | unary_context_shape | One unary form has only its single-hole context |
| u12 | both_marked_collapsed | Both old marked data have equal profiles |
| u12 | fresh_adds_new_distinction | Old collapse survives while the newcomer is distinguished |
| u12 | avoidance_needs_both_targets | Avoiding one target is insufficient |
| u12 | avoiding_both_preserves | The actual two-target condition preserves the pair |
| u12 | separation_preserved_fresh | Reuse an existing positive witness directly after growth |

Seven new reports use `{propext, Quot.sound}`; the context-shape and direct-witness proofs
use only `propext`. The four affected scripts check 58 reports in total:
ten in u05, eight in u09, sixteen in u11, and 24 in u12. These are book
results, not additions to the sealed census or new research results.

The fixed axiom gate caught an unwanted dependency in an initial helper:
the simplifier selected `Nat.add_eq_right._simp_1`, which reaches
`Classical.choice`. Direct constructor reasoning removes it without
changing the allowed boundary. The final reports are checked exactly;
the expected dependency list was not widened to accept the draft.

Python checks call the actual sealed replay and observation APIs for the
new examples. Existing finite populations remain unchanged: the added
cases are separately stated, not silently counted into old enumerations.
No general Python-to-Lean refinement theorem is claimed.

## Limits and reproduction

Run the existing textbook job through `python ci/run_gates.py --job textbook`
in the pinned local environment. Focused book scripts are u05, u09, u11,
and u12; their exact report maps reject unexpected dependencies. The
full job also rechecks the unchanged native definitions and all other
book scripts. Publication and exact-head receipts are recorded with the PR.

This review does not certify every explanation, S/A classification,
prerequisite, or source declaration in the thirteen chapters. The optional
token-aware check in Unit 05 still refers forward to Unit 06; the first
pass needs only the displayed position table. The recorded prerequisite
graph remains a different, limited population.

Static Markdown and generated Wiki checks do not establish hosted
rendering, reading time, novice comprehension, unfamiliar transfer, or
retention. Existing positive reader feedback does not supply those
measurements. The broader teaching goal remains active.
