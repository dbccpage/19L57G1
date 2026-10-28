# Source map and evidence scope

AuthorityEffect: None. This route teaches supplied mathematical language
outside the sealed derivation. It introduces no new primitive inside it.

## Definitions before applications

| Lesson | Teaching meaning | Native connection and limit |
|---|---|---|
| 00 | A record is a particular supplied entry; a rule specifies a permitted step; a definition fixes a meaning | `model.replay` and `observe.derivable` distinguish admitted records/rules and consequences. The table-reading rule here is a separate teaching admission. |
| 01 | A function assigns exactly one output to every input of its declared domain | `Compression.FactorsOn` supplies a function recovering q from p on D. Equal p-inputs cannot require unequal q-outputs. |
| 02–03 | An if-then comparison fails at P Yes / Q No; a two-way comparison checks both directions | The book's general `chain`, `both_directions`, and `no_automatic_reverse` proofs teach the surrounding logic, not a new passage event. |
| 04 | “Every” covers each declared member; “some” requires a member as witness | `Compression.SigEq`, `Adequate`, `FiberConstant`, `FactorsOn` quantify over declared families/domains. Empty-domain conventions do not imply existence. |
| 05 | A separating question may depend on a pair; a common question is chosen for every pair | `observe.separable` and `witness`, and `Basic.separable`, express pairwise separation. The book counterexample does not alter their definitions. |
| 06 | A result's hypotheses and domain accompany its conclusion | `Compression.factors_iff_fiberConstant` relates recoverability to constancy on merged inputs. The book proves its recovery-implies-agreement direction directly using the actual `FactorsOn` definition. |
| 07 | Definition, deduction, finite calculation, and measurement have different evidence requirements | This is a teaching discipline. No native theorem establishes the behavior of a physical sensor or a novice learner. |

Native paths are `code/derivation/model.py`, `observe.py`,
`lean4/Derivation/Basic.lean`, and `Compression.lean`. Existing longer
treatments include Units 03, 08–09 and 61, and Institutions 00–02.

## The declared table and encoding

The same A/B/C records come from `textbook/first_steps/cards.json`.
Blue answers Yes, Yes, No; round answers Yes, No, No; triangle answers
No, Yes, Yes. The round question is supplied consistently with those
recorded shapes. It is not a new physical measurement. “Not” complements
one of these complete supplied Boolean answers.

Selected domains are the eight subsets of the three positions; available
question lists are independently selected from the three named questions.
Different-card pairs are unordered off-diagonal pairs. On an empty pair
domain the each-pair condition is true. A common-question claim still
requires an available question; when both domains are empty it is false.

As in First steps, the executable correspondence admits three tokens and
one unary form per selected question, adds instances precisely at Yes
positions, and admits no uniform rules. It compares well-formed contexts,
positive derivability, profiles, separations, and witnesses through the
actual sealed Python kernel. A No encoding means absent derivability in
this rule-free ledger, not a separately proved physical negation.

## Checked finite populations

| Population | Size |
|---|---:|
| Recorded default-table conditional comparisons | 288 |
| Recorded default-table pair/question-family comparisons | 64 |
| Recorded default-table recovery domains | 8 |
| Arbitrary Boolean tables: three questions on three positions | 512 |
| Conditional comparisons across all those tables and domains | 147456 |
| Pair/question-family comparisons across those tables and domains | 32768 |
| Recovery tasks across those tables and domains | 36864 |
| Sealed unary-encoding replay histories | 4096 |

The population check compares row guards with independent set inclusion
or equality, pairwise signatures with distinct signature counts, and
common witnesses with injectivity of a single question. Recovery enumerates
all four Boolean lookup functions and compares existence with the absence
of blocking pairs. All 512 abstract tables are included even when their
answers would not describe the default colors and shapes; they are Boolean
tables, not 512 observed card collections.

The packet checks the loaded kernel module origins and pins consumed
card, encoding-check, and kernel source text by SHA-256 after
UTF-8/LF normalization. Its numbers are recomputed, not used as substitutes
for the actual population. These are finite checks, not a general
Python-to-Lean refinement or an unbounded semantic completeness result.

## Book proofs

`textbook/reasoning_lab/lean_cases.py` imports the actual
`Derivation.Compression` library and supplies twelve book declarations:
six general logic/recovery results and six concrete card results.
The general statements include chaining implications, both directions
of an equivalence, a failed automatic reverse, empty-domain quantifiers,
common-witness implication, and recovery preserving equal inputs.

Nine axiom reports are empty. `recover_on_smaller_domain` uses exactly
`{propext}`; `individual_without_common` and
`no_recovery_on_full_domain` use exactly `{propext, Quot.sound}`.
These are **derived (book Lean)** results, outside the sealed census.
Only the named cases are book-Lean instances; the 147456 Python comparisons
have not all been translated into Lean or proved to implement it generally.

No novice comprehension, unfamiliar-example transfer, reading-time result,
delayed retention, causal effect, or empirical correspondence is claimed.
