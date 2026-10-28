# Source map and evidence scope

AuthorityEffect: None. The lab consumes the sealed sources read-only.
All carriers, histories, guards, and observations used here are supplied.

## Definitions and results

| Lesson | Primary source anchors | Meaning used here |
|---|---|---|
| 00 | `PrimitivePassage.PState`, `PEvent`, `step`; `assertion_not_retained`, `retention_requires_assertion`, `retained_sub_asserted` | Assertion, retention, and protection have different stores and event guards |
| 01 | `obstP`, `zeroP`, `obstP_factors` together with the four `gate_*_independent` results; `obst_policies_differ` | Active obstruction has the stated gates; the undeclared-observation policy is chosen |
| 02 | `responseMenu`, `refineOk`, `repairFamily`, `menu_complete`, `two_rule` | Existing repair menu and activity are different predicates |
| 03 | `step` cases `refineCol` and `addCol`; `proposal_not_execution`, `budget_gates_execution` | Budget gates both changes; permission gates only column creation |
| 04 | `extensionProposals`, `extension_always_available`, `nextFamilyP`, `nextFamilyP_complete_ext` | The proposal universe consists of singleton columns; generated blocks retain event guards |
| 05 | `refusal_object_inert`, `refusal_not_terminal`, `terminal_absorbing` | Refusal records an active pair; halt absorbs subsequent events |
| 06 | `retention_persists`, `retained_sub_asserted`; new book invariant `Textbook.PassageLab.protected_sub_retained` | Protected pairs in histories from genesis are retained, and retained pairs are asserted |
| 07 | The definitions separated in `MODEL_MAP.md`; finite world comparison | A shared word supplies no general model transport or empirical correspondence |

Unqualified passage names above belong to
`lean4/Derivation/PrimitivePassage.lean`. The executable mirror is
`code/derivation/primitive_passage.py`. The comparison uses
`code/derivation/represented.py` and its own `obstructed`, `repair_family`,
and refusal guard; the formal owner is `lean4/Derivation/Represented.lean`.
The longer existing treatments are Units 44–48 and 54–55.

## Three positions throughout the operational comparison

The teaching history admits tokens 10, 20, 30 at positions 0, 1, 2,
then asserts and retains all three unordered off-diagonal pairs. It
protects A/B and B/C, declares an empty observation, supplies budget two,
and appends the A column. This spends one budget unit. Protecting A/C
is one further legal event; every other field stays fixed.

The desk sorts members when displaying a column, so a membership pattern
such as `[A,C]` is easy to read. The packet and Lean comparisons retain
the source's literal list order: refinement prepends C and produces
`[C,A]`. Sorting the display does not replace the recorded list.

| Compared state | Existing menu entries | Structural repairs of B/C | Singleton proposals | Valid canonical new-column patterns |
|---|---:|---:|---:|---:|
| A/B and B/C protected | 3 | 1 | 2 | 4 |
| All three pairs protected | 3 | 0 | 2 | 4 |

The lab compares two protection states, three budgets (0, 1, 2), two
permission settings, and two halt settings: 24 operational states and
48 guarded event applications. Those variations are built with legal
events on the three-position carrier. They do not exhaust all passage
states, all budgets, all columns, or all histories.

Eight sorted duplicate-free subsets enumerate the Boolean membership
patterns on this carrier. Four qualify as new columns in the worked
case; the source's singleton proposal family contains two. This is not
an enumeration of every literal natural-number list with arbitrary
ordering or duplication.

## Record comparisons and reachability

Sixteen raw records vary retention, protection, and four observation
values (undeclared; declared empty; A column; A and B columns). Four
violate protection-within-retention and cannot be reached from genesis
by the passage events. The remaining twelve passing that necessary
invariant are not thereby proved reachable.

The source's **total** `zeroDeclP` gate is true before declaration by
convention. The learner display instead says that no comparison has been
declared; it does not pretend there is an undeclared blind observer.
The source's joint (declared, total-zero) gate values are (False, True),
(True, False), and (True, True). They cannot both be false. Individual
gate independence over raw records is not a proof that all sixteen
four-bit gate valuations occur, nor a claim about every reachable state.

## Python and Lean evidence

The Python check independently recomputes the finite guard conditions
and compares the outcomes with the actual passage functions. It pins
the consumed Python source text using SHA-256 after explicit UTF-8/LF
normalization and checks loaded module origins.

The book-Lean check proves 118 concrete equalities for the gate records,
guarded events, response families, columns, and history traces. It also
proves the general protection-within-retention step and replay invariants.
All 120 axiom reports use exactly `{propext, Quot.sound}`. These are
Lean (book) results, outside the sealed derivation and its census; the
general invariant is marked **derived (book Lean)**. Concrete equalities
are finite instances. None is a general Python-to-Lean refinement proof.

The teaching wrapper restricts tokens, endpoints, column members, and
budget to the declared natural-number encoding. The raw Python passage
functions use `int` and do not reject every negative value that Lean's
`Nat` type excludes. We do not claim agreement outside this encoding,
silently repair sealed code, or expose arbitrary integers as learner inputs.

## Refusal and generated blocks

The passage refusal guard checks activity, not repair-menu exhaustion.
Its stored certificate concerns the state when it was recorded; later
repair can leave the historical record present while activity disappears.

The proposal generator does not gate on permission or halt. Its extension
blocks explicitly set budget one and attempt `addCol`. With permission
off, the budget can change without adding the column. With halt on,
the whole block is inert. Existence of a block is not successful execution.
