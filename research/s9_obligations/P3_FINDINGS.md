# P3 -- S9.3, proof-relevant witness types below function spaces

PROMPT.md steps 21-25, with step 26's statements proposed for the Lean
stage.  AuthorityEffect: None.  This part proposes; it amends nothing
sealed, and nothing below is a discharged obligation.

Receipt: `receipts/witness_types.json`, written by
`run_witness_types.py` (`--out DIR`, default `receipts`) through
`common.write_receipt` after `common.assert_inside_tree`.  Every number
in this document sits next to the receipt key that holds it, and a test
resolves every key, test name, function name, and file this document
cites (`test_findings_cite_only_resolvable_names`).  Governing prompt
blob `1642e3f6ac746002678e4997f738e0fabd1248c9`, snapshot commit
`db1d2b225b577d5212780ff02700efd693c8e446` (receipt keys
`prompt_blob_id`, `snapshot_commit`).  S9.1-S9.3 numbering is the
prompt's, not the paper's (`numbering_note`).

House rule, applied: a table is not a computation, so the numbers here
are outputs of `witness_types.py` over a declared finite space, not
tallies of expected cases; an absent separation is not an equality, so
"invisible" below never means "equal"; the answer to S9.3 is a boundary.

## Round-2 repairs, recorded

This is the third version of this part.  Three adversarial reviews of
the second version found defects; what changed is recorded here and
under the receipt key `revision.round_2`, so a reader comparing versions
sees the rewordings rather than a quietly different sentence.  Nothing
withdrawn in round 1 is restored, and no pair count, first pair, or Lean
target changed (`revision.round_2.unchanged_by_the_repair`).

1. **A phrase reached past the bound.**  The sharing-multiplicity
   residue (kind 3 of step 24) was stated as holding at every T from 3
   up -- the words "from T = 3" followed by "on" -- in the step-25
   sentence, in the S9_3_WITNESS_INVISIBLE scope, and in four places in
   this document; but the only T = 3 cell enumerated is (2, 3), since
   cell (3, 3) is refused under the per-cell bound and T = 4 is refused
   by name.  Every occurrence now names the cell
   (`revision.round_2.reworded[0]`), and the step-37 scanner lists that
   wording and its relatives (`test_scanners_fire_on_injected_claims`
   shows it firing on the withdrawn wording and on a "T >=" form; the
   scanner is strict, and this record therefore spells the wording in
   two pieces rather than exempting quotations).  The phrase
   "depends on T >= 2" in the when-half is withdrawn the same way: T = 1
   is not a declared cell and nothing is said about it
   (`revision.round_2.reworded[2]`).
2. **Step 25 named half of step 21's admission.**  Step 21 admits
   TOKEN_DOMAIN and TOKEN_EQ; the sentence said "exactly when TOKEN_EQ is
   admitted".  V0 and V1 already presuppose TOKEN_DOMAIN (stores are
   subsets of T), so the sentence now reads "exactly when TOKEN_EQ is
   admitted on top of TOKEN_DOMAIN (together, the admission named in
   step 21)" (`revision.round_2.reworded[1]`; the S9_3_WITNESS_OBSERVABLE
   scope says the same).
3. **The kind-3 characterization had no receipt key.**  "Every
   count-equal non-isomorphic invisible pair differs in how many tokens
   two pairs share" was read off the first such pair.  The count-equal
   non-isomorphic pairs are now split by the invariant they differ in
   (`cells.<cell>.spaces.<space>.invisible.<V>.non_isomorphic_count_equal_pairs_by_differing_invariant`,
   with the comparison
   `cells.<cell>.spaces.<space>.invisible.<V>.every_non_isomorphic_count_equal_pair_differs_in_intersection_profile`;
   `revision.round_2.added_keys`), re-derived independently in every
   enumerated space by grouping and a direct loop inside each group
   (`test_count_equal_pairs_by_differing_invariant_in_every_space`) and
   by the full pair loop on the small spaces; the numbers are in step 24.
4. **One receipt declared two units for the assignment bound.**
   `declared_bounds.cell_assignment_space` reads the bound against the
   witnessed space; `step21_admission.why_sets` read it against the full
   space (262144).  The latter now names the witnessed count (196608) and
   what multisets would have cost (`revision.round_2.reworded[3]`).
5. **Two tautologies were labelled findings.**  The token-bijection
   invariance of V2_ANON, and the refinements `V1 refines V0`,
   `V2_ANON refines V0`, and V2_NAMED refining every other vocabulary,
   could not have come out otherwise under the declared definitions and
   are now labelled so in the same sentence; the computed content of
   those blocks is the pair of non-refinements.  No receipt value
   changed.
6. **The kind-2 paragraph read as a prose proof.**  It is now a computed
   pair with a remark on the encoding, in the form the V2_NAMED paragraph
   already had.
7. **The step-36 scanner stripped a denial to the end of its sentence**,
   so a sentence denying one verb and asserting another -- "OB-1 is not
   closed here, but this part narrows it anyway", with the protected name
   repeated after the verb -- was invisible to it.  It now strips the denial phrase only, and that
   sentence is an injection it is shown to catch.
8. **The step-35 probe handed the writer a sealed path.**  On the defect
   it exists to catch -- a guard that lets a path through -- the old test
   would have written into `artifacts/`.  It now exercises the resolver
   alone on that path and the writer on an empty directory under the OS
   temporary root, outside the repository, checked empty afterwards.

Not changed, and why: step 26's proofs remain the Lean stage's (the
reviewers recorded this without re-raising it; see "Step 26" below), and
the tree-wide test failure the reviewers saw was in another part's file.

## Round-1 repairs, recorded

This is what the second version of this part changed.  Three adversarial
reviews of the first version found defects; what changed is recorded
here and under the receipt key `revision.round_1`, so a reader comparing
versions sees the withdrawals rather than a quietly different table.

1. **Two `first_*` values were not the least pair.**  The receipt
   declares that every "first pair" is the lexicographically least
   (A, B) with A < B.  The old code took, for the count-equal and the
   joint-invariant groups, the pair of the first bucket visited; bucket
   order is by each bucket's least member, which need not belong to a
   qualifying pair, so a later bucket could hold a smaller pair.  It did,
   in two spaces.  Withdrawn (`revision.round_1.withdrawn_values`): the value
   (0,3,0,3)/(0,3,0,5) for
   `cells.N2_T3.spaces.witnessed.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair`,
   now (0,1,3,3)/(0,1,3,5); and the whole (3, 3) irreflexive block, for
   the reason in item 2.  The repair (`least_pair` in `invisible_pairs`)
   takes the minimum over every group, and two new tests re-derive every
   `first_*` key without buckets: an independent scan in enumeration
   order over every enumerated space
   (`test_every_first_pair_is_the_least_by_independent_scan`) and a full
   pair loop over every space of at most 200 assignments
   (`test_counts_and_first_pairs_by_full_pair_loop_on_small_spaces`).
   Unchanged by the repair (`revision.round_1.unchanged_by_the_repair`): every
   pair count, the step-23 pair W1/W2, the step-24 pair W3/W4 (already
   the least in its space), and every `first_pair` and
   `first_non_isomorphic_pair` value.
2. **The assignment bound was applied per space; PREFLIGHT states it per
   cell.**  The old module comment said the bounds were "copied, not
   re-declared" while its rule text had been reworded from PREFLIGHT's
   per-cell rule to a per-space one, under which the (3, 3)
   witnessed_irreflexive sub-space (229376 assignments) was enumerated
   although the cell's declared assignment space (117440512) exceeds the
   bound.  That was a departure from the declared bound rule that nothing
   recorded.  Now the rule is applied per cell as PREFLIGHT states it,
   cell (3, 3) is not enumerated in any space, the code refuses every
   space of that cell by name, and the departure is recorded
   (`declared_bounds.withdrawn_application`).  A per-space rule would be
   an amendment of `PREFLIGHT.md`, which this part does not own; it is
   proposed, not made (`declared_bounds.proposed_amendment_not_made`).
   Every (3, 3) number of the first version is withdrawn and none is
   cited here.
3. **Step 25's "only when" half was presented as a computed finding.**
   It is definitional within the declared vocabularies, and now says so
   in the same sentence (`step25_answer.only_when_half`).
4. **A receipt string cited a key that did not exist**
   (`step21_admission.TOKEN_NAMES.price`); it now names the key that
   exists.
5. **"Checked on whole cells" overstated the fast-key test's reach**; the
   sentence now names the spaces it covers, and the test covers one more.
6. **The V2_NAMED "hides nothing" paragraph read as a prose proof**; it is
   now a computed number with a remark, not a reason.
7. **No negative test scanned this part's prose for steps 36, 37, 40**;
   `test_witness_types.py` now carries scanners for protected-open
   claims, carrier-general phrasing, external-name markers, and the
   restricted words, each shown to fire on an injected sentence
   (`test_scanners_fire_on_injected_claims`).
8. The function that computes the least transport of an assignment was
   named with a word the house rule restricts; it is `least_transport`.

Not changed, and why: step 26's proofs are the Lean stage's by this
part's brief, and the Lean files are not this part's to write; see
"Step 26" below for what happens if no Lean stage runs.

## Bounded, first

**Bounded:** every result of this part is finite computation bounded by
carrier N = 3, reached at T = 2 (`bounds_reached.carrier_reached`,
`bounds_reached.carrier_reached_at`), and token domain T = 3, reached at
N = 2 (`bounds_reached.token_domain_reached`,
`bounds_reached.token_domain_reached_at`); N = 4 and T = 4 were refused
by name (`bounds_reached.refused_by_name`); nothing here is
carrier-general or token-domain-general, and no Lean theorem names a
general case.

**Bounded:** cells (2, 2), (2, 3), (3, 2) were enumerated whole in both
declared spaces (`bounds_reached.cells_enumerated`; `cells.<cell>.bounded`
is false and `cells.<cell>.enumerated` is true for each); cell (3, 3)
was not enumerated in any space (`bounds_reached.cells_not_enumerated`,
`cells.N3_T3.enumerated = false`, `cells.N3_T3.bounded = true`) because
the assignment-count bound is applied **per cell**, as PREFLIGHT.md step
4 states it (`declared_bounds.rule_when_hit`, quoted verbatim;
`declared_bounds.rule_unit`): the declared assignment space of a cell is
A2's object over it, the `witnessed` space, of which the irreflexive
space is a sub-space (`declared_bounds.cell_assignment_space`), and for
(3, 3) that space has 117440512 assignments
(`cells.N3_T3.declared_cell_assignment_count`), over the bound 2^20 =
1048576 (`declared_bounds.assignments_enumerated_per_cell_at_most`).  Its
irreflexive sub-space, 229376 assignments
(`cells.N3_T3.declared_assignment_counts.witnessed_irreflexive`), is
inside the number and outside the rule, and is not enumerated
(`bounds_reached.refused_by_name[2]`, `cells.N3_T3.bound_reached`); the
first version of this part enumerated it under a per-space reading of
the rule, which departed from PREFLIGHT and is withdrawn
(`declared_bounds.withdrawn_application`, `declared_bounds.application`).
`enumerate_space` refuses every space of that cell by name (test
`test_bounds_are_refused_by_name`), and the per-cell rule itself is
tested (`test_bound_rule_is_per_cell`).

## Step 21 -- the witness-type layer against A2's bill

A2 (S1 of `paper/primitive_difference.md`): as A1, plus witness
multiplicity; object `(X, W : X -> X -> Nat, a, b)` with `0 < W a b`
(`step21_admission.a2_bill`).

The layer (`step21_admission.layer`): a finite token domain
`T = {t0, ..., t(k-1)}` with identity across pairs, and a witness
assignment `S : (X x X) -> finite subsets of T` with `S(a, b)` nonempty.
The store per ordered pair is a **set**, not a multiset
(`step21_admission.store`), for three declared reasons
(`step21_admission.why_sets`): the layer *replaces* A2's count, which is
recovered as the derived cardinality `|S(x, y)|` and is not admitted a
second time; with TOKEN_EQ the only admitted judgement on tokens, two
occurrences of one token at one pair would be inseparable by every
expressible question, so a within-pair multiplicity would be A2's count
re-entering under a new name; and it keeps the (3, 2) cell inside the
2^20 bound read, as the per-cell rule reads it, against the cell's
declared assignment space, the witnessed space: 196608 assignments, of a
full space of 262144 (`cells.N3_T2.declared_cell_assignment_count`,
`cells.N3_T2.full_space_count`), whereas with multisets of multiplicity
at most 2 the full space alone would be 3^18 = 387420489.  The brief's
performance note assumed multisets with multiplicity at most 2; this
part chose sets and says so.

Admitted beyond A2, in one line (`step21_admission.admitted_beyond_a2`):

    TOKEN_DOMAIN (a second finite sort T, distinct from the carrier) and
    TOKEN_EQ (a decidable equality judgement on T, admitted as a
    primitive, not derived); V2_NAMED admits in addition TOKEN_NAMES
    (one object-language constant per element of T).

Price of TOKEN_EQ (`step21_admission.TOKEN_EQ`): it is **outside A1's
bill** -- A1 admits no identity relation of the object language, and
TOKEN_EQ is one, on the token sort.  It is **not contained in A3's
bill, which it does not contain either** -- A3 imports the metatheory's
identity on the *carrier* through function types, composition, and the
one-point carrier; TOKEN_EQ is an identity on T only, says nothing about
carrier points, and uses no function type, no composition, and no
one-point carrier; the two bills are incomparable under inclusion of
their listed items, and no ranking between them is claimed.  (This
paragraph was narrowed by the synthesis pass's repair round 1; the
receipt string `step21_admission.TOKEN_EQ.price_vs_A3` and the
S9_3_ADMISSION_NAMED scope, which had read "strictly less than A3's
bill", a ranking that no declared order on bills supports, say the same
since the repair after full-run audit 1, `revision.round_3.reworded[0]`.)
TOKEN_NAMES
(`step21_admission.TOKEN_NAMES`) is priced separately: a question may
then address a token by its metatheoretic name, and the computation
shows what that buys and what it costs (step 24; the price text names
the key `cells.<cell>.spaces.<space>.invariant_under_token_bijections`,
whose `V2_NAMED` entry is false in every enumerated space, test
`test_token_names_price_cites_an_existing_key`).  Not admitted
(`step21_admission.not_admitted`): identity on the carrier, function
types, composition, quotients, any order on T, any axiom on the presence
relation.

Terminal: **S9_3_ADMISSION_NAMED** -- scope: the admission is
TOKEN_DOMAIN plus TOKEN_EQ, with TOKEN_NAMES as a further, separately
labelled admission for the named vocabulary only; it is a declaration
priced against S1's bills, not a theorem, and it is what every result
below is relative to.

## Step 22 -- the vocabularies, as explicit finite question lists

Designated pair (0, 1); ordered pairs row-major
(`step22_vocabularies.pair_order`).  The questions
(`step22_vocabularies.questions`), none taking a map as an argument
(test `test_no_question_argument_is_a_map_and_kinds_are_declared`):

| question | reads | vocabulary | admission used |
|---|---|---|---|
| `presence(p)` | is the store at p nonempty | V0 | none beyond A2 |
| `count_eq(p, q)`, p < q | `|S(p)| = |S(q)|` | V1 | A2's count, recovered |
| `count_lt(p, q)`, p != q | `|S(p)| < |S(q)|` | V1 | A2's count, recovered |
| `share(p, q)`, p < q | do S(p) and S(q) hold a common token | V2_ANON | TOKEN_EQ |
| `token_at(t, p)` | does the named token t occur at p | V2_NAMED | TOKEN_EQ + TOKEN_NAMES |

V0 = presence; V1 = V0 + count comparisons; V2_ANON = V0 + share;
V2_NAMED = V0 + token_at; V1_V2_ANON and V1_V2_NAMED are the joins with
V1 (`step22_vocabularies.vocabularies`).  Named versus anonymous: the
prompt's V2 is computed **both** ways and labelled separately, because
step 24's answer depends on the choice
(`step22_vocabularies.named_versus_anonymous`).

Sizes (`step22_vocabularies.sizes_by_cell`, formulas in
`step22_vocabularies.size_formulas`, test
`test_sizes_match_the_declared_formulas_in_every_cell`); the (3, 3) row
is a question count only, since that cell is not enumerated:

| cell | V0 | V1 | V2_ANON | V2_NAMED | V1_V2_ANON | V1_V2_NAMED |
|---|---|---|---|---|---|---|
| N2_T2 | 4 | 22 | 10 | 12 | 28 | 30 |
| N2_T3 | 4 | 22 | 10 | 16 | 28 | 34 |
| N3_T2 | 9 | 117 | 45 | 27 | 153 | 135 |
| N3_T3 (not enumerated) | 9 | 117 | 45 | 36 | 153 | 144 |

**What "below function spaces" forbids**
(`step22_vocabularies.below_function_spaces_forbids`): *maps as data* --
no question takes, returns, or ranges over a map of any type, so "is
there a bijection carrying A onto B" is not a question; *composition* --
no question forms a witness at (x, z) from witnesses at (x, y) and
(y, z), and no maps are composed; *quotients* -- no question is asked of
a quotient carrier (points identified by presence) or a quotient token
domain (tokens identified by sharing), and no assignment is formed by
quotienting.  Refused by name, in code and here
(`step22_vocabularies.refused_constructions`; functions
`refuse_map_as_datum`, `refuse_composition`, `refuse_quotient`, `refuse`,
each raising `BelowFunctionSpaces`; test `test_refusals_raise_by_name`):
`family_isomorphism_as_question` (needs maps as data),
`witness_composition` (needs composition),
`presence_quotient_of_carrier` and `sharing_quotient_of_tokens` (need
quotients).

Metatheoretic apparatus that is in **no** vocabulary
(`step22_vocabularies.metatheoretic_apparatus_not_in_any_vocabulary`):
the isomorphism of witness families (`family_isomorphic_metatheory`,
`least_transport`) and the classifying invariants (`count_vector`,
`intersection_profile`, `token_degree_multiset`, `common_token_count`).
They are used only to say what an invisible pair differs by.

## The space, and why bucketing is the enumeration

Two spaces over each cell (`enumeration.spaces`): `witnessed` is A2's
object -- every map from ordered pairs to subsets of T whose store at
(0, 1) is nonempty, no other axiom; `witnessed_irreflexive` is S7's
object -- witnessed with every diagonal store empty.  Counts
(`cells.<cell>.declared_assignment_counts`, checked against the
enumeration in `analyze_space` and by test
`test_declared_counts_match_the_enumeration`):

| cell | full space | witnessed | witnessed_irreflexive |
|---|---|---|---|
| N2_T2 | 256 | 192 | 12 |
| N2_T3 | 4096 | 3584 | 56 |
| N3_T2 | 262144 | 196608 | 3072 |
| N3_T3 | 134217728 | 117440512 (over the per-cell bound) | 229376 (not enumerated: the cell is over the bound) |

Order (`enumeration.order`): a store is a bit mask over T, an assignment
is the tuple of masks in pair order, and the order is lexicographic on
that tuple; "first pair" always means the lexicographically least
(A, B) with A < B among the pairs the key describes, taken as the
minimum over every group holding such a pair, never the pair of the
first group visited (`enumeration.first_pair_rule`; round-1 repair,
item 1 above).  The order is deterministic and equals the sorted order
(test `test_order_is_lexicographic_and_deterministic`).  Every `first_*`
key of every enumerated space is re-derived by an independent scan in
enumeration order (`test_every_first_pair_is_the_least_by_independent_scan`),
and on the spaces of at most 200 assignments -- N2_T2 both spaces,
N2_T3 irreflexive -- every count and every first pair is re-derived by a
full pair loop with no bucketing at all
(`test_counts_and_first_pairs_by_full_pair_loop_on_small_spaces`).

Bucketing is the enumeration, not a shortcut past it
(`enumeration.bucketing_is_the_enumeration`): every assignment of a
space is generated and keyed by its full answer vector under each of the
six vocabularies; a separating pair is two members of one coarse bucket
in different fine buckets, an invisible pair is two distinct members of
one bucket, and the pair counts are exact sums over bucket sizes.  The
fast keys are checked equal to the generic question-by-question
evaluation on the whole cells (2, 2) and (2, 3) in both spaces and on
the (3, 2) witnessed_irreflexive space
(`test_fast_keys_equal_generic_answer_vectors`); the (3, 2) witnessed
space, 196608 assignments, is not compared generically, and its
reported pairs are re-checked by evaluating every question of the
relevant vocabularies on them
(`test_separating_pairs_rechecked_by_every_question`,
`test_invisible_pairs_rechecked_by_every_question`), as are the reported
pairs of every other enumerated space.

Computed in every enumerated space
(`cells.<cell>.spaces.<space>.invariant_under_token_bijections`, test
`test_refinement_order_is_computed_not_assumed`): V0, V1, V2_ANON, and
V1_V2_ANON give the same answers on an assignment and on every token
renaming of it; V2_NAMED and V1_V2_NAMED do not.  None of the four
affirmative entries could have come out otherwise: V0 and V1 read only
the count vector, and V2_ANON's `share` questions read only whether an
intersection of two stores is nonempty, which every token bijection
preserves, so all four are invariant by construction and the computation
confirms definitional facts rather than finding them (step 25 below).
The two negative entries are computed -- an assignment and a token
renaming of it with a differing `token_at(t, p)` answer exist in every
enumerated space -- and a reason is visible in the encoding (`token_at(t, p)`
names its token), but the computed value is the ground.  Also computed,
the refinement order between the vocabularies
(`cells.<cell>.spaces.<space>.refinement`), with the same labelling:
`V1 refines V0` and `V2_ANON refines V0` hold by inclusion of question
lists (each is built as V0 plus further questions), and V2_NAMED
refining every other vocabulary holds by the encoding (`token_at(t, p)` over
every token and pair reads off the masks, so its partition has as many
classes as the space has assignments:
`cells.<cell>.spaces.<space>.partition_class_counts.V2_NAMED` equals
`cells.<cell>.spaces.<space>.assignment_count`); those entries could not
have come out otherwise.  The computed content of the block is the pair
of non-refinements, **V1 does not refine V2_ANON and V2_ANON does not
refine V1**, each witnessed by a first pair (step 23).

## Step 23 -- the separating pair (V1 cannot, V2 can)

Headline counts (`summary.<cell>/<space>.V1_equal_V2_ANON_different` and
`summary.<cell>/<space>.V1_equal_V2_NAMED_different`; pairs with
identical answers to every V1 question and a differing answer to some V2
question):

| space | pairs V1-equal, V2_ANON-different | V1-equal, V2_NAMED-different |
|---|---|---|
| N2_T2/witnessed | 390 | 498 |
| N2_T2/witnessed_irreflexive | 6 | 15 |
| N2_T3/witnessed | 100140 | 122238 |
| N2_T3/witnessed_irreflexive | 150 | 402 |
| N3_T2/witnessed | 4015170 | 4113858 |
| N3_T2/witnessed_irreflexive | 16806 | 18390 |

The first pair in declared order, S7's object at (2, 2)
(`cells.N2_T2.spaces.witnessed_irreflexive.separating.V1_vs_V2_ANON.first_pair`,
test `test_step_23_first_pair_is_the_computed_one`):

    A: S(0,1) = {t0}, S(1,0) = {t0}        masks (0, 1, 1, 0)
    B: S(0,1) = {t0}, S(1,0) = {t1}        masks (0, 1, 2, 0)

All 22 V1 questions answer identically (`coarse_differing_question_count
= 0`); exactly one V2_ANON question differs
(`fine_differing_question_count = 1`): `share((0,1),(1,0))`, true for A
and false for B (`first_fine_differing_question`).  That question uses
TOKEN_EQ and nothing else.  In A2's object at (2, 2) the first pair is
`S(0,1) = {t0}, S(1,1) = {t0}` versus `S(0,1) = {t0}, S(1,1) = {t1}`,
separated by `share((0,1),(1,1))`
(`cells.N2_T2.spaces.witnessed.separating.V1_vs_V2_ANON.first_pair`): A2
imposes no irreflexivity, so a diagonal store is a legitimate member of
that space.  Both firsts are computed, not hand-picked, and both are
re-derived by the independent scan.

The other direction of the same comparison is also computed
(`summary.<cell>/<space>.V2_ANON_equal_V1_different`: 784, 16, 378930,
501, 3072512, 23056 in the table's row order): V2_ANON is blind to count
comparisons.  Its first pair at (2, 2), irreflexive, is `{t0},{t0}`
versus `{t0},{t0,t1}`, separated by `count_eq((0,1),(1,0))`
(`cells.N2_T2.spaces.witnessed_irreflexive.separating.V2_ANON_vs_V1.first_pair`).
So V1 and V2_ANON are incomparable as separation orders in every
enumerated space; neither contains the other.

Terminal: **S9_3_WITNESS_OBSERVABLE** -- scope: finite computation,
bounded by N = 3 (reached at T = 2) and T = 3 (reached at N = 2), cells
(2, 2), (2, 3), (3, 2) enumerated whole in both spaces and cell (3, 3)
not enumerated; in every enumerated space there are pairs of witness
assignments that every V1 question answers identically and some V2_ANON
question separates (counts above), the first such pair being `{t0},{t0}`
versus `{t0},{t1}` on the two-element irreflexive object, separated by
`share((0,1),(1,0))`; no carrier-general claim is made, and the Lean
statements for this pair are proposed below, not proved by this part.

## Step 24 -- what stays invisible even in V2

Pairs of assignments that differ as raw data yet answer every question
of a vocabulary identically (`cells.<cell>.spaces.<space>.invisible.<V>`,
headline keys in `summary`):

| space | invisible in V2_NAMED | invisible in V1_V2_ANON | of which renamings (isomorphic) | non-isomorphic | non-isomorphic with equal counts |
|---|---|---|---|---|---|
| N2_T2/witnessed | 0 | 108 | 92 | 16 | 0 |
| N2_T2/witnessed_irreflexive | 0 | 9 | 5 | 4 | 0 |
| N2_T3/witnessed | 0 | 22098 | 8112 | 13986 | 7650 |
| N2_T3/witnessed_irreflexive | 0 | 252 | 90 | 162 | 18 |
| N3_T2/witnessed | 0 | 98688 | 98176 | 512 | 0 |
| N3_T2/witnessed_irreflexive | 0 | 1584 | 1520 | 64 | 0 |

Keys, under `summary.<cell>/<space>`: `invisible_in_V2_NAMED`,
`invisible_in_V1_V2_ANON`, `invisible_in_V1_V2_ANON_non_isomorphic`,
`invisible_in_V1_V2_ANON_non_isomorphic_count_equal`; the renaming
column is
`cells.<cell>.spaces.<space>.invisible.V1_V2_ANON.isomorphic_pair_count`.
V2_ANON alone (without V1) hides more -- 892, 25, 401028, 753, 3171200,
24640 pairs in the same row order
(`summary.<cell>/<space>.invisible_in_V2_ANON`) -- almost all of it
count differences V1 sees.

Under the **named** vocabulary nothing is invisible: the computation
gives 0 pairs in every enumerated space
(`summary.<cell>/<space>.invisible_in_V2_NAMED`,
`summary.<cell>/<space>.invisible_in_V1_V2_NAMED`; test
`test_v2_named_hides_nothing_and_v1_v2_anon_hides_renamings`), and the
computed V2_NAMED partition has one class per assignment
(`cells.<cell>.spaces.<space>.partition_class_counts.V2_NAMED`).  A
reason is visible in the encoding -- the answers to `token_at(t, p)`
over every token t and pair p read off the masks -- but it is not proved
here and is not the ground of the claim; the number is.  The price the computation makes
visible: V2_NAMED also separates every one of the 92, 5, 8112, 90,
98176, 1520 pairs that are isomorphic as witness families
(`cells.<cell>.spaces.<space>.isomorphic_pair_count_total`), i.e. token
renamings, which are not witness-level structure.  V2_NAMED is not
invariant under token bijections
(`cells.<cell>.spaces.<space>.invariant_under_token_bijections`, entry
`V2_NAMED`, false everywhere).  This is the dependence step 22 was told
not to hide: with TOKEN_NAMES the answer to "what is invisible" is
"nothing", and with TOKEN_EQ alone it is the boundary below.

Under the **anonymous** vocabulary with counts, V1_V2_ANON, the
invisible pairs split, from the computation, into three kinds:

1. **Token renamings.**  The first invisible pair in every enumerated
   space is `S(0,1) = {t0}` versus `S(0,1) = {t1}` (masks (0, 1, 0, 0)
   and (0, 2, 0, 0) at N = 2;
   `cells.<cell>.spaces.<space>.invisible.V1_V2_ANON.first_pair`, and
   `cells.<cell>.spaces.<space>.invisible.V1_V2_ANON.first_pair_characterization`
   has `isomorphic_as_families = true`).  These are isomorphic witness
   families; an anonymous vocabulary cannot and should not see them.  In
   every enumerated T = 2 space they are the whole of the invisible set
   apart from kind 2 (non-isomorphic with equal counts = 0 in every
   enumerated T = 2 space).
2. **Count magnitude.**  The first non-isomorphic invisible pair in
   every enumerated space is `S(0,1) = {t0}` versus `S(0,1) = {t0,t1}`
   (masks (0, 1, 0, 0) and (0, 3, 0, 0);
   `cells.<cell>.spaces.<space>.invisible.V1_V2_ANON.first_non_isomorphic_pair`,
   whose
   `cells.<cell>.spaces.<space>.invisible.V1_V2_ANON.first_non_isomorphic_pair_characterization`
   lists `invariants_that_differ` as count_vector, token_degree_multiset,
   common_token_count).  That pair is computed in every enumerated space
   and re-checked question by question; what it differs by is A2-level
   data (a count), not token-level structure.  A reason is visible in
   the vocabulary definitions -- V1 has only comparisons between pairs
   and no "is the count 1", and `share` reads only nonemptiness -- but
   it is a remark on the encoding, not the ground of the claim; the
   computed pair is.
3. **Sharing multiplicity** -- the token-level residue.  At T = 3 --
   cell (2, 3), the only T = 3 cell enumerated -- non-isomorphic pairs
   with **equal** count vectors are invisible to V1_V2_ANON: 7650 in A2's
   object and 18 in S7's (`summary.N2_T3/witnessed.invisible_in_V1_V2_ANON_non_isomorphic_count_equal`,
   `summary.N2_T3/witnessed_irreflexive.invisible_in_V1_V2_ANON_non_isomorphic_count_equal`),
   and 0 in every enumerated T = 2 space.  Nothing is said about T = 3 at
   N = 3 or about any T beyond 3: those cells were not enumerated.
   The first, on S7's object at (2, 3)
   (`cells.N2_T3.spaces.witnessed_irreflexive.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair`,
   test `test_step_24_first_count_equal_invisible_pairs`):

       A: S(0,1) = {t0,t1}, S(1,0) = {t0,t1}     masks (0, 3, 3, 0)
       B: S(0,1) = {t0,t1}, S(1,0) = {t0,t2}     masks (0, 3, 5, 0)

   Both stores have two tokens in both assignments, both pairs share a
   token in both assignments, and every one of the 28 V1_V2_ANON
   questions answers identically; yet no token bijection carries A onto
   B (`isomorphic_as_families = false`).  What they differ by, from the
   computation
   (`cells.N2_T3.spaces.witnessed_irreflexive.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair_characterization`):
   the intersection profile (`|S(0,1) & S(1,0)|` is 2 in A and 1 in B),
   the token degree multiset ([0, 2, 2] against [1, 1, 2]), and the
   common-token count (2 against 1).  A *how many* tokens are shared is
   not a *whether* tokens are shared.  In A2's object at (2, 3) the
   least such pair
   (`cells.N2_T3.spaces.witnessed.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair`,
   the value repaired in round 1) is `{t0}, {t0,t1}, {t0,t1}` versus
   `{t0}, {t0,t1}, {t0,t2}` on the pairs (0,1), (1,0), (1,1) -- masks
   (0, 1, 3, 3) and (0, 1, 3, 5) -- differing only at (1,1)
   (`cells.N2_T3.spaces.witnessed.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair_characterization`:
   `differing_pairs = [[1, 1]]`), in the intersection profile and the
   token degree multiset, with the common-token count equal (1 in both:
   t0 lies in all three nonempty stores).

   That every such pair, not only the first, differs in how many tokens
   two pairs share is a receipt value, not a reading of one pair
   (`cells.<cell>.spaces.<space>.invisible.<V>.non_isomorphic_count_equal_pairs_by_differing_invariant`,
   the count-equal non-isomorphic invisible pairs split by the invariant
   they differ in; test
   `test_count_equal_pairs_by_differing_invariant_in_every_space`, an
   independent grouping with a direct loop inside each group, and the
   full pair loop on the small spaces).  In A2's object at (2, 3) the
   7650 pairs split as `intersection_profile` 7650,
   `token_degree_multiset` 5598, `common_token_count` 3330,
   `none_of_the_computed_invariants` 0; in S7's object the 18 split as
   18, 18, 18, 0.  So the intersection profile catches every one of them
   while the other two invariants do not, and
   `cells.<cell>.spaces.<space>.invisible.<V>.every_non_isomorphic_count_equal_pair_differs_in_intersection_profile`
   is true in every enumerated space and vocabulary -- with content at
   (2, 3), and vacuously where the count is 0.

In every enumerated space every non-isomorphic invisible pair differs in
at least one of the four computed invariants
(`cells.<cell>.spaces.<space>.invisible.V1_V2_ANON.non_isomorphic_pairs_by_differing_invariant.none_of_the_computed_invariants`
is 0), so within the declared space the three kinds above exhaust what
V1_V2_ANON hides.  Whether a vocabulary with sharing-*count* comparisons
would see kind 3, and whether it is below function spaces, is not
decided here: no such vocabulary was declared.

Terminal: **S9_3_WITNESS_INVISIBLE** -- scope: finite computation,
bounded by N = 3 (reached at T = 2) and T = 3 (reached at N = 2), cells
(2, 2), (2, 3), (3, 2) enumerated whole in both spaces and cell (3, 3)
not enumerated; in every enumerated space V1 with V2_ANON leaves
invisible pairs that are unequal as raw data (counts above): token
renamings in every space, count-magnitude differences in every space,
and, at T = 3 (cell (2, 3), the only T = 3 cell enumerated; none in any
enumerated T = 2 space), non-isomorphic families with equal count
vectors, every one of which differs in how many tokens two pairs share
(`cells.N2_T3.spaces.<space>.invisible.V1_V2_ANON.non_isomorphic_count_equal_pairs_by_differing_invariant`,
entry `intersection_profile`, equals
`cells.N2_T3.spaces.<space>.invisible.V1_V2_ANON.non_isomorphic_count_equal_pair_count`),
the first being `{t0,t1},{t0,t1}`
versus `{t0,t1},{t0,t2}`; under V2_NAMED no pair is invisible in any
enumerated space, at the cost of separating every token renaming; none
of this is an equality claim, and none of it is carrier-general.

## Step 25 -- S9.3 answered in one sentence, with scope

The sentence (`step25_answer.sentence`, scope `step25_answer.scope`):

Within the declared vocabularies V0, V1, V2_ANON, V2_NAMED and their
joins, and the declared finite space -- cells (2, 2), (2, 3), (3, 2)
enumerated whole in both spaces and cell (3, 3) not enumerated --
witness-level structure becomes observable below function spaces
exactly when TOKEN_EQ is admitted on top of TOKEN_DOMAIN (together, the
admission named in step 21): the vocabularies expressible over
TOKEN_DOMAIN without TOKEN_EQ, V0 and V1, leave `{t0},{t0}` versus
`{t0},{t1}` unseparated in every enumerated space, the one question that
separates that pair, `share((0,1),(1,0))`, uses TOKEN_EQ and nothing
else, and TOKEN_EQ does not make all witness-level structure observable
-- V1 with V2_ANON still hides token renamings, count magnitudes, and,
at T = 3 (cell (2, 3), the only T = 3 cell enumerated; 0 such pairs in
every enumerated T = 2 space), the number of tokens two pairs share --
while V2_NAMED hides nothing only because TOKEN_NAMES lets it address
tokens by metatheoretic name, which also makes it separate renamings
that are not witness-level structure.

The two halves of "exactly" are of different kinds, and the receipt
labels them (`step25_answer.when_half`, `step25_answer.only_when_half`).
The *when* half -- that admitting TOKEN_EQ makes some witness-level
structure observable -- is computed: separating pairs exist in every
enumerated space (each has T = 2 or T = 3; T = 1 is not a declared cell
and nothing is said about it).  The *only
when* half -- that V0 and V1 see none of it -- is definitional within
the declared vocabularies, not a finding: every V0 and V1 question reads
only the count vector, and the count vector is invariant under token
bijections by construction, so V0 and V1 could not separate an
assignment from a token renaming of it; the computed invariance of V0
and V1 confirms this and could not have come out otherwise.  The word
"exactly" is therefore scoped by "within the declared vocabularies": the
sentence says nothing about vocabularies that were not declared.

## Step 26 -- Lean targets (proposed only; the Lean stage proves)

Receipt key `lean_targets`, rendered from the computed pairs (test
`test_lean_targets_render_the_computed_pairs`).  Carrier `Bool` with
designated `(false, true)`; token domain `Fin k`; an assignment is
`W : Bool -> Bool -> Fin k -> Bool` with `W x y t = true` meaning token
`t` occurs at `(x, y)`.  The function type is the metatheory's encoding
of a finite table, not an object-language device; the object language
has no maps.

Separating pair (from `cells.N2_T2.spaces.witnessed_irreflexive`):

    def W1 : Bool -> Bool -> Fin 2 -> Bool := fun x y t =>
      match x, y, t.val with | false, true, 0 => true | true, false, 0 => true | _, _, _ => false
    def W2 : Bool -> Bool -> Fin 2 -> Bool := fun x y t =>
      match x, y, t.val with | false, true, 0 => true | true, false, 1 => true | _, _, _ => false

Definition of isomorphism of witness families, stated precisely:

    WitnessIso W W' := exists (s : Bool -> Bool) (r : Fin k -> Fin k),
      s false = false /\ s true = true /\ Function.Bijective s /\
      Function.Bijective r /\ forall x y t, W x y t = W' (s x) (s y) (r t)

-- a bijection on the carrier fixing the designated points plus a
bijection on tokens transporting the assignment.

Statements to prove:

1. `S9_3_sep_presence_equal`:
   `forall x y, (exists t, W1 x y t = true) <-> (exists t, W2 x y t = true)`
   -- by `decide`.
2. `S9_3_sep_count_equal`:
   `forall x y, card (W1 x y) = card (W2 x y)` with
   `card w := (if w 0 then 1 else 0) + (if w 1 then 1 else 0)` -- by
   `decide`.
3. `S9_3_sep_not_isomorphic`: `not (WitnessIso W1 W2)` -- not by
   `decide`, since the quantifiers range over function types; route:
   from a transport at `(false, true, 0)` and `(true, false, 0)` with
   `s` point-fixing obtain `W2 false true (r 0) = true` and
   `W2 true false (r 0) = true`, then case on `r 0 : Fin 2` and close by
   `decide`; constructive, no choice.
4. `S9_3_sep_V2_ANON_separates`:
   `(exists t, W1 false true t = true /\ W1 true false t = true) /\
   not (exists t, W2 false true t = true /\ W2 true false t = true)`
   -- by `decide`.
5. The negative half, `S9_3_sep_V1_indistinguishable`: **formalizable**
   under the encoding of V1 as an explicit finite list -- an inductive
   `Q` with the 4 presence, 6 count_eq, and 12 count_lt questions (22)
   and `evalV1 : Q -> (Bool -> Bool -> Fin 2 -> Bool) -> Bool`;
   `forall q in V1_list, evalV1 q W1 = evalV1 q W2` is then `decide`
   over the list.  The residual is the encoding, named: the list is
   written by hand in Lean, and that it equals the Python vocabulary V1
   at (2, 2) is checked by no gate.  It is a residual, not an obstacle
   to the proof.

Invisible pair (from `cells.N2_T3.spaces.witnessed_irreflexive`, the
first V1_V2_ANON-invisible non-isomorphic pair with equal counts, whose
value the independent scan confirms as the least):

    def W3 : Bool -> Bool -> Fin 3 -> Bool := fun x y t =>
      match x, y, t.val with | false, true, 0 => true | false, true, 1 => true
        | true, false, 0 => true | true, false, 1 => true | _, _, _ => false
    def W4 : Bool -> Bool -> Fin 3 -> Bool := fun x y t =>
      match x, y, t.val with | false, true, 0 => true | false, true, 1 => true
        | true, false, 0 => true | true, false, 2 => true | _, _, _ => false

6. `S9_3_inv_V1_V2_ANON_indistinguishable`: every one of the 28
   V1_V2_ANON questions (explicit list) answers identically on W3 and W4
   -- `decide` over the list; same residual as 5.
7. `S9_3_inv_count_equal`: `forall x y, card3 (W3 x y) = card3 (W4 x y)`
   -- `decide`.
8. `S9_3_inv_not_isomorphic`: `not (WitnessIso W3 W4)` over `Fin 3` --
   by an invariant transported by any `(s, r)`: the number of tokens
   `t` with `W false true t = true /\ W true false t = true` is 2 for W3
   and 1 for W4; not `decide`, for the same reason as 3.

The encoding obstacle, named: quantification over bijections of a
function type is not decidable in Lean core without a finite
enumeration of the function type, so the non-isomorphism statements go
through an invariant lemma rather than `decide`.

No LEAN terminal is emitted by this part: step 26's proofs are the Lean
stage's by this part's brief, and `lean/S9Obligations.lean` and
`lean/S9Obligations/AxiomReport.lean` are not this part's files.  If no
Lean stage runs (`lean_stage_note`), the synthesis pass must emit
**LEAN_NOT_CARRIED** for S9.3 with the obstacle "no Lean stage ran",
and S9.3 then ends narrowed with the residual -- the eight statements
above -- written, not discharged.  A reviewer asked for exactly this
sentence; it is the honest form of the definition of done for this
bullet until the proofs exist.

The Lean stage has since run.  Its outcome -- the eight statements
above proved under their proposed names, with the differences named --
is the section "Lean outcome (step 26), written by the Lean stage" at
the end of this document.  The sentences of this section and the
terminals below still describe this part's own files, which prove
nothing; the Lean stage's terminals are its own and are listed there.

## Terminals, with scopes

Receipt key `terminals` (each name checked against PROMPT.md's legal
list and against this section by test
`test_terminals_are_legal_scoped_and_bounded`).

* **S9_3_ADMISSION_NAMED** -- scope as in step 21: TOKEN_DOMAIN plus
  TOKEN_EQ, with TOKEN_NAMES a separately labelled further admission for
  V2_NAMED only; a priced declaration, not a theorem.
* **S9_3_WITNESS_OBSERVABLE** -- scope as in step 23: finite
  computation, bounded by N = 3 (reached at T = 2) and T = 3 (reached at
  N = 2), cells (2, 2), (2, 3), (3, 2) enumerated whole in both spaces
  and cell (3, 3) not enumerated; V1-equal, V2_ANON-different pairs
  exist in every enumerated space, the separating question using
  TOKEN_EQ on top of TOKEN_DOMAIN, the admission of step 21; not
  carrier-general; the Lean half for that pair is named by theorem in
  the scope string since the repair after full-run audit 1
  (`LEAN_STAGE_CITED`, each name checked against the audited inventory
  by `test_terminal_strings_cite_only_audited_lean_theorems`; the
  string had said "Lean statements proposed, not proved",
  `revision.round_3.reworded[1]`).
* **S9_3_WITNESS_INVISIBLE** -- scope as in step 24: finite computation,
  bounded by N = 3 (reached at T = 2) and T = 3 (reached at N = 2),
  cells (2, 2), (2, 3), (3, 2) enumerated whole in both spaces and cell
  (3, 3) not enumerated; V1 with V2_ANON hides renamings, count
  magnitudes, and, at T = 3 (cell (2, 3), the only T = 3 cell
  enumerated), sharing multiplicity; V2_NAMED hides nothing in any
  enumerated space at the cost of separating renamings; no equality is
  claimed.
* **PYTHON_ONLY_SCOPE_DECLARED** -- scope: the exhaustiveness of this
  part's enumeration lives in Python only, bounded by N = 3 and T = 3
  with cell (3, 3) not enumerated; the Lean stage's theorems concern the
  two computed pairs and the carrier-size-2 lists, and none reads the
  enumeration or its counts (the string had said "no Lean theorem of
  this part exists" and step 26's statements were proposals until the
  repair after full-run audit 1, `revision.round_3.reworded[2]`).
* **REFUSED** -- scope: N = 4 and T = 4 refused by name; cell (3, 3)
  refused under the per-cell assignment bound 2^20 -- its declared
  assignment space has 117440512 assignments, and its irreflexive
  sub-space is not enumerated either (`bounds_reached.refused_by_name`);
  the constructions `family_isomorphism_as_question`,
  `witness_composition`, `presence_quotient_of_carrier`,
  `sharing_quotient_of_tokens` refused by name
  (`step22_vocabularies.refused_constructions`).
* **OB1_UNCHANGED** -- scope: this part makes no claim about OB-1; it is
  not closed, narrowed, or priced here.
* **S66_UNCHANGED** -- scope: this part makes no claim about S6.6; it is
  not closed, narrowed, or priced here.
* **S9_LAST_UNCHANGED** -- scope: this part makes no claim about the
  inscription bridge, the S9 last bullet; it is not closed, narrowed, or
  priced here.

What this part does not do: it does not cite
`multiplicity_invisible_to_presence` for any claim about tokens (that
theorem of `lean4/Derivation/PrimDiff.lean` is about counts after
truncation to presence); it proves no Lean theorem; it declares no
vocabulary beyond the six above; and it does not say what happens at
N = 4, T = 4, or anywhere in cell (3, 3).

## Negative tests (steps 34-40) carried by this part

`test_witness_types.py`, all in-process, each named here so a reader
can find the one that guards a rule:

* step 35, the write root: `test_write_root_guard_refuses_a_directory_outside_the_tree`
  (the resolver refuses `artifacts/` by raising, and the writer refuses
  an empty directory under the OS temporary root, checked empty
  afterwards; the writer is never handed a sealed path, so a broken guard
  cannot make this test write one -- round-2 repair).
* step 36, the protected opens: `test_findings_and_receipt_make_no_protected_open_claim`
  scans this document and every string of the receipt for a sentence
  attaching "closed", "narrowed", or "priced" to OB-1, S6.6, or the
  inscription bridge, after removing each explicit denial phrase -- the
  phrase only, so a claim later in the same sentence still counts
  (round-2 repair); it fires on injected sentences
  (`test_scanners_fire_on_injected_claims`).
* step 37, no promotion to a carrier-general claim:
  `test_findings_and_receipt_carry_no_carrier_general_phrase` (a listed
  set of general phrasings, including from round 2 the phrases that
  project one cell onto every larger one, and the phrase
  "carrier-general" unless negated in the same sentence) and
  `test_result_terminals_say_bounded_in_the_same_bullet` (the two result
  terminals name the bound in their own bullet, and this document has a
  "Bounded, first" section naming the per-cell rule).
* step 39, the vocabulary firewall: `test_no_working_denylist_identifier_in_p3_files`
  over the five files of this part (102 identifiers, 0 leaks; also
  ASCII and LF).
* step 40, no external name: `test_no_external_name_marker_in_p3_files`
  over the five files (URLs, citation markers, appeals to what is known).
* the house rule on restricted words:
  `test_restricted_words_are_absent_or_scoped_in_findings`.
* the house rule that every cited key exists:
  `test_findings_cite_only_resolvable_names`, and the digest and size
  stated below: `test_findings_sha_and_size_match_the_committed_receipt`.

These scanners are pattern tests; they catch the phrasings they list and
no others, and a green run is a receipt that those phrasings are absent,
not that the prose is right.

## Round-2 injections, each reversed

Each round-2 repair that is a gate was made to fail on the defect it
exists to catch, with the failure naming the injected object, and shown
to recover when the injection was reversed.  No receipt was regenerated
while an injection was live, and the sealed prefixes were checked clean
afterwards.

| injection | observed |
|---|---|
| the denial-then-claim sentence of item 7 appended to this document | `test_findings_and_receipt_make_no_protected_open_claim` fails, naming the claim (the verb followed by the protected name); exit 1, then 0 after reversal.  The round-1 scanner returned an empty list on the same sentence, probed in-process before the repair |
| the withdrawn wording of item 1 appended to this document | `test_findings_and_receipt_carry_no_carrier_general_phrase` fails, naming the phrase; exit 1, then 0 after reversal.  The round-1 scanner returned an empty list on it |
| `invisible_pairs` made to add 0 to the count-equal split | `test_count_equal_pairs_by_differing_invariant_in_every_space` fails with the zeroed split against 7650 / 5598 / 3330, and the byte pin `test_committed_receipt_equals_a_fresh_build_byte_for_byte` fails with it; exit 1, then 0 after reversal |
| the writer made to bypass the guard and write its argument directly | `test_write_root_guard_refuses_a_directory_outside_the_tree` fails: the probe directory under the OS temporary root is no longer empty; the sealed-prefix status printed nothing afterwards, which is the point of the repair; exit 1, then 0 after reversal |

## Receipts of this part

    cd research/s9_obligations
    PYTHONPATH=../../code PYTHONUTF8=1 python run_witness_types.py --out receipts
    PYTHONPATH=../../code PYTHONUTF8=1 python run_witness_types.py --out tmp_replay_a
    PYTHONPATH=../../code PYTHONUTF8=1 python run_witness_types.py --out tmp_replay_b
    cmp tmp_replay_a/witness_types.json tmp_replay_b/witness_types.json
    cmp tmp_replay_a/witness_types.json receipts/witness_types.json

Step 33: the three runs produced byte-identical files, SHA-256
`71c77fb32cd83d3a8bf42d90c42977b0b1ee729f4351dadd9e7200fb8c476e67`,
342087 bytes, LF only, at that round; after the repair after full-run
audit 1 (the last section of this document) the receipt is
`25a31fb5fe1c82271c8e46ccfe6e93156581acc3ac7964a42c34eca3c2a0b880`,
345705 bytes, again produced twice into two directories and compared
byte for byte; the temporary directories were deleted
afterwards.  The unit tests (`test_witness_types.py`) rebuild the
receipt in-process and compare it byte for byte with the committed file
(`test_committed_receipt_equals_a_fresh_build_byte_for_byte`), write it
into two temporary directories inside the tree and compare
(`test_receipt_replays_byte_identically_into_two_directories`), and scan
this part's five files against the 102-identifier working denylist
(`test_no_working_denylist_identifier_in_p3_files`).

## Lean outcome (step 26), written by the Lean stage

AuthorityEffect: None.  This section is the Lean stage's, not P3's; it
proposes, and nothing in the receipt was changed by it: the receipt's
`lean_stage_note` and the PYTHON_ONLY_SCOPE_DECLARED bullet above
described this part's own files, which prove nothing, until the repair
after full-run audit 1 made them name this stage's theorems (the last
section of this document), and the terminals at the end of this section
are the Lean stage's own.  Module:
`lean/S9Obligations/WitnessTypes.lean`, namespace
S9Obligations.WitnessTypes (written here without backticks, because this
document's resolver reads a dotted token as a receipt path), imported by
`lean/S9Obligations.lean`; 30 theorems by this stage, 32 after the
repair after full-run audit 1 added `v1ListNodup` and `v2AnonListNodup`,
each with a `#print axioms` line
in `lean/S9Obligations/AxiomReport.lean` and the same name, in the same
order, in `AXIOM_REPORT_DECLARATIONS` of `verify_lean.py`.  Nothing
under `lean4/Derivation/` was touched.  The sealed names reused, never
restated: `S2` and `Irrefl` as objects, `S2_irrefl` as a theorem; the
sealed `multiplicity_invisible_to_presence` is not cited, as this part
said it would not be.

**Declared before proving.**  The encoding is the one P3 declared in
`lean_targets`: carrier `Bool` with designated `(false, true)`; token
domain `Fin 2` for the separating pair and `Fin 3` for the invisible
pair; an assignment is a function from two carrier points and a token to
`Bool`, abbreviated `Assignment k`, with `W x y t = true` meaning that
token `t` occurs at `(x, y)`; the function type is the metatheory's
encoding of a finite table, and no question takes, returns, or ranges
over a map.  `W1`, `W2`, `W3`, `W4` are the receipt's four definitions
verbatim.  A2's count is the cardinality `card`, defined by structural
recursion on the token domain so that it reduces inside `decide`; its
`Fin 2` instance is the receipt's `card` by definitional unfolding
(`cardTwo`, proved by reflexivity).  The questions are one inductive
`Q` with the four kinds `presence`, `countEq`, `countLt`, `share`, every
argument a carrier point, and `eval` mirrors `evaluate` question by
question: presence is "some token occurs", the count kinds compare
`card`, and `share` is "some token occurs at both pairs" -- `TOKEN_EQ`
enters only there, through the token variable occurring twice.  The
lists `presenceList` (4), `countList` (6 + 12), and `shareList` (6) were
transcribed from `vocabulary` at (2, 2) in the Python order by a one-off
rendering script, and `v1List` (22), `v2AnonList` (10), and
`v1V2AnonList` (28) are their joins, built as `vocabulary` builds them;
the lengths are proved (`v1ListLength`, `v2AnonListLength`,
`v1V2AnonListLength`, against
`step22_vocabularies.sizes_by_cell.N2_T2.V1`,
`step22_vocabularies.sizes_by_cell.N2_T2.V2_ANON`,
`step22_vocabularies.sizes_by_cell.N2_T2.V1_V2_ANON`) and no list has a
repeated entry (`v1V2AnonListNodup` by this stage; `v1ListNodup` and
`v2AnonListNodup` added by the repair after full-run audit 1), but that
the entries equal the Python list is checked by no gate: the residual P3 named
(`lean_targets[3].residual`) is narrowed to a mechanical transcription,
not closed.  `WitnessIso` is P3's definition
(`lean_targets[5].definition_of_isomorphism`) verbatim, except that the
sealed package carries the core injectivity and surjectivity predicates
and no bijectivity predicate, so the receipt's bijectivity is spelled as
their conjunction (`Bijective`); the content is the same.  Every finite
claim goes through `decide` with core instances (`Bool`, `Fin k`,
`Nat`, list membership) and with explicit `Decidable` instances for
`Shared`, `SomeShared`, `TwoShared`, and `presence` obtained by unfolding,
as the sealed module does for `S2`; no classical choice, and
`verify_lean.py` checks it.  Names: the eight proposed statements keep
the receipt's names; every other declaration is in lowerCamelCase, so
that this document can cite it without colliding with the resolver of
`test_witness_types.py`, which reads an underscored token as a receipt
citation.

**The eight proposed statements, all proved.**  Each row names the
theorem as written and what differs from the proposal, if anything.
Statements are given in ASCII; `forall`, `exists`, `<->`, `/\`, and
`not` stand for the Lean symbols.

| receipt name | statement as written | proof | difference from the proposal |
|---|---|---|---|
| `S9_3_sep_presence_equal` | forall x y : Bool, (exists t : Fin 2, W1 x y t = true) <-> (exists t : Fin 2, W2 x y t = true) | `decide` | none |
| `S9_3_sep_count_equal` | forall x y : Bool, card (W1 x y) = card (W2 x y) | `decide` | `card` is the structural recursion, whose `Fin 2` instance is the receipt's `card` (`cardTwo`) |
| `S9_3_sep_V1_indistinguishable` | forall q in v1List, eval q W1 = eval q W2 | `decide` over the 22-entry list | one inductive `Q` carries all four kinds, so a single `eval`, generic in the token domain, serves both lists; the list and evaluator the receipt names in `lean_targets[3].statement` are `v1List` and `eval` here |
| `S9_3_sep_V2_ANON_separates` | (exists t : Fin 2, W1 false true t = true /\ W1 true false t = true) /\ not (exists t : Fin 2, W2 false true t = true /\ W2 true false t = true) | `decide` | none |
| `S9_3_sep_not_isomorphic` | not (WitnessIso W1 W2) | `someSharedTransport` applied to the two halves of `S9_3_sep_V2_ANON_separates` | bijectivity spelled as the conjunction; the route is not the proposed case split on the image of token 0 but the transport of `SomeShared` -- the separating `V2_ANON` question is itself the invariant; the statement is unchanged |
| `S9_3_inv_V1_V2_ANON_indistinguishable` | forall q in v1V2AnonList, eval q W3 = eval q W4 | `decide` over the 28-entry list | as for the `V1` list |
| `S9_3_inv_count_equal` | forall x y : Bool, card (W3 x y) = card (W4 x y) | `decide` | none |
| `S9_3_inv_not_isomorphic` | not (WitnessIso W3 W4) | `twoSharedTransport` applied to the two halves of `invTwoShared` | the proposed invariant, transported by every witness isomorphism, in the form "two distinct tokens are shared by (0, 1) and (1, 0)" (`TwoShared`), which uses only the injectivity of the token map; its count form is `invSharedCounts` |

The two definition entries of `lean_targets` (`S9_3_sep_W1_W2_definitions`,
`S9_3_inv_W3_W4_definitions`) are the four `def`s, verbatim, with the
abbreviation `Assignment k` for the function type.

**Twenty-two further theorems** by this stage, twenty-four after the
repair after full-run audit 1.  On the lists: `v1ListLength`,
`v2AnonListLength`, `v1V2AnonListLength`, `v1V2AnonListNodup`,
`v1ListNodup` and `v2AnonListNodup` (the last two by that repair, both by
`decide`, both with no axioms), and
`v1ListReadsCountsOnly` (every `V1` question is of a kind other than
`share`).  On `card`: `cardTwo`, and `cardPosIff` (a store has positive
cardinality exactly when some token occurs in it; presence is the count
being nonzero), both for a token domain `Fin k` with `k` a variable.
Transport: `sharedTransport` (the transport equation of a point-fixing
carrier map carries a shared token `t` to the shared token `r t`),
`someSharedTransport` (uses neither bijectivity), and
`twoSharedTransport` (uses the injectivity of the token map), all with
`k` a variable.  On the separating pair: `sepExactlyOneV2AnonQuestionDiffers`
-- the filter of `v2AnonList` by "answers differently on W1 and W2" is
the one-element list holding `share((0,1),(1,0))`, which is the
receipt's
`cells.N2_T2.spaces.witnessed_irreflexive.separating.V1_vs_V2_ANON.fine_differing_question_count`
= 1 and
`cells.N2_T2.spaces.witnessed_irreflexive.separating.V1_vs_V2_ANON.first_fine_differing_question`
read off the list; `sepRawDataDiffer` (`W1` and `W2` are unequal as
functions); `sepPresenceS2` (both induce the sealed `S2` as their
presence relation, so the pair lives on S7's object, as the
`witnessed_irreflexive` space requires); `sepPresenceIrrefl` (both
induced relations satisfy the sealed `Irrefl`, by the sealed
`S2_irrefl`).  On the invisible pair: `invSharedCounts` (the shared-token
count is 2 for `W3` and 1 for `W4`, the receipt's
`cells.N2_T3.spaces.witnessed_irreflexive.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair_characterization.left_invariants.common_token_count`
and
`cells.N2_T3.spaces.witnessed_irreflexive.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair_characterization.right_invariants.common_token_count`);
`invTwoShared`; `invRawDataDiffer`; `invPresenceS2`; `invPresenceIrrefl`.
Beyond the proposal: `evalReadsCounts` (a question of a kind other than
`share` answers identically on two assignments with equal count
vectors), `v1ListReadsCounts` (two assignments with equal count vectors
answer every question of `v1List` identically), and
`sepV1IndistinguishableViaCounts` (target 3 re-derived from target 2
through `v1ListReadsCounts`, in agreement with its `decide` proof).  The
last three are stated for a token domain `Fin k` with `k` a variable and
for the lists of carrier size 2; they are the "only when" half of step
25 (`step25_answer.only_when_half`), which this part labelled
definitional, made a theorem for that list: no `V1` question separates
any count-equal pair, whatever the token domain size, so what
`share((0,1),(1,0))` sees of `W1` against `W2` is not expressible in
`V0` or `V1`.  A carrier-general claim is not made: the lists are those
of carrier size 2, and no theorem here quantifies over the carrier.

**What stays finite computation, bounded as P3 declared it.**  The
enumeration: that W1/W2 is the first separating pair in declared order,
that W3/W4 is the first count-equal invisible non-isomorphic pair, every
pair count of steps 23 and 24, the invisible split by invariant, and the
isomorphism-class counts live in Python only, bounded by N = 3 (reached
at T = 2) and T = 3 (reached at N = 2) with cell (3, 3) not enumerated,
and no Lean statement reads the receipt or the enumeration
(PYTHON_ONLY_SCOPE_DECLARED stands as this part emitted it).  The
transcription of the two lists, as above.  Not proposed and not
attempted: the token-bijection invariance of `V0`, `V1`, `V2_ANON`,
`V1_V2_ANON` and the non-invariance of `V2_NAMED`
(`cells.<cell>.spaces.<space>.invariant_under_token_bijections`), the
`V2_NAMED` vocabulary in any form, the (3, 2) cell, and the refinement
order; only the one-direction transports of two share properties were
stated.  Nothing was enumerated by this stage; N = 4, T = 4, and cell
(3, 3) stay refused by name.

**Terminals of the Lean stage, each with its scope.**  These are not in
the receipt (`terminals` holds P3's own, by the receipt's own rule in
`lean_stage_note`).

* **LEAN_CARRIED** -- the eight statements of `lean_targets` (seven
  entries: two definition entries and eight statements), every one
  proved under its proposed name in `lean/S9Obligations/WitnessTypes.lean`;
  no statement weakened and nothing dropped; the differences are the
  general `card` with `cardTwo`, bijectivity as the conjunction, and the
  non-isomorphism route through transported share properties in place
  of the proposed case split, which is a route and not a change of
  statement.  The negative half P3 marked "formalizable with the
  encoding as residual" (`lean_targets[3].residual`) is proved for the
  transcribed list; the residual is the transcription and is not
  closed.
* **LEAN_CARRIED** -- the twenty-two further theorems named above,
  including `v1ListReadsCounts`, the "only when" half of step 25 for
  the carrier-size-2 list with `k` a variable; a carrier-general claim
  is not made.
* **LEAN_CARRIED** -- the Lean half of S9_3_WITNESS_OBSERVABLE, for the
  pair this part computed: `S9_3_sep_V1_indistinguishable`,
  `S9_3_sep_V2_ANON_separates`, `sepExactlyOneV2AnonQuestionDiffers`,
  `S9_3_sep_not_isomorphic`, `sepPresenceS2`, `sepPresenceIrrefl`; the
  pair counts (6, 150, 16806 and the rest) and the claim "in every
  enumerated space" stay finite computation bounded by N = 3 and T = 3
  with cell (3, 3) not enumerated, as the bullet above says.
* **LEAN_CARRIED** -- the Lean half of S9_3_WITNESS_INVISIBLE, for the
  pair this part computed: `S9_3_inv_V1_V2_ANON_indistinguishable`,
  `S9_3_inv_count_equal`, `S9_3_inv_not_isomorphic`, `invSharedCounts`,
  `invTwoShared`, `invPresenceS2`, `invPresenceIrrefl`; the counts 7650
  and 18, the split by invariant, and every "every such pair" sentence
  stay finite computation bounded by N = 3 and T = 3 with cell (3, 3)
  not enumerated, as the bullet above says; no equality is claimed, and
  `invRawDataDiffer` says the pair is unequal.
* **LEAN_NOT_CARRIED** -- the enumeration and its counts: no Lean
  statement reads the receipt, the enumeration order, the first-pair
  rule, or any pair count; that scope is Python's, bounded by N = 3
  (reached at T = 2) and T = 3 (reached at N = 2) with cell (3, 3) not
  enumerated, and PYTHON_ONLY_SCOPE_DECLARED names it.
* **LEAN_NOT_CARRIED** -- that `v1List` and `v1V2AnonList` are the
  Python `vocabulary` at (2, 2): no Lean statement reads the Python
  lists and no gate compares the two; the lengths and the absence of
  repeats are proved, the entries were transcribed mechanically, and
  the residual is recorded, not closed.  Not attempted, and not
  proposed: the token-bijection invariance entries and `V2_NAMED`.
* **MANUAL_RECEIPT_DECLARED** -- the 83 `#print axioms` reports of this
  tree (23 of P1, 28 of P2, 32 of this module: 30 of this stage and the
  two `Nodup` lemmas of the repair after full-run audit 1) are read by
  no CI gate;
  `verify_lean.py` is run by hand, and a committed report implies no
  enforcement.
* **REFUSED** -- unchanged from P3: N = 4 and T = 4 refused by name,
  cell (3, 3) refused under the per-cell assignment bound, the four
  constructions refused by name; this stage enumerated nothing, and its
  theorems with `k` a variable concern only the two computed pairs and
  the carrier-size-2 lists.

The three protected opens of step 36 are untouched by this stage, which
says nothing about them.  It names no external theory and writes no
prose proof: every argument is inside the Lean file.

**Receipts of this stage.**  Run from the repository root:

    cd research/s9_obligations/lean && lake build
    python research/s9_obligations/verify_lean.py

The build exited 0 with last line `Build completed successfully (9 jobs)`.
The verifier exited 0 with counts line
`Lean #print axioms declarations: 81 within ['Quot.sound', 'propext']`
and 6 sources scanned for forbidden tokens; re-run after the repair
after full-run audit 1, exit 0, counts line
`Lean #print axioms declarations: 83 within ['Quot.sound', 'propext']`,
6 sources.  The 32 report lines, verbatim from the build log (the two
`Nodup` lines of the repair from the re-run's `lake env lean` output):

    'S9Obligations.WitnessTypes.cardTwo' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.cardPosIff' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.v1ListLength' does not depend on any axioms
    'S9Obligations.WitnessTypes.v2AnonListLength' does not depend on any axioms
    'S9Obligations.WitnessTypes.v1V2AnonListLength' does not depend on any axioms
    'S9Obligations.WitnessTypes.v1V2AnonListNodup' does not depend on any axioms
    'S9Obligations.WitnessTypes.v1ListNodup' does not depend on any axioms
    'S9Obligations.WitnessTypes.v2AnonListNodup' does not depend on any axioms
    'S9Obligations.WitnessTypes.v1ListReadsCountsOnly' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.sharedTransport' does not depend on any axioms
    'S9Obligations.WitnessTypes.someSharedTransport' does not depend on any axioms
    'S9Obligations.WitnessTypes.twoSharedTransport' does not depend on any axioms
    'S9Obligations.WitnessTypes.S9_3_sep_presence_equal' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.S9_3_sep_count_equal' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.S9_3_sep_V1_indistinguishable' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.S9_3_sep_V2_ANON_separates' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.sepExactlyOneV2AnonQuestionDiffers' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.S9_3_sep_not_isomorphic' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.sepRawDataDiffer' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.sepPresenceS2' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.sepPresenceIrrefl' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.S9_3_inv_V1_V2_ANON_indistinguishable' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.S9_3_inv_count_equal' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.invSharedCounts' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.invTwoShared' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.S9_3_inv_not_isomorphic' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.invRawDataDiffer' depends on axioms: [propext]
    'S9Obligations.WitnessTypes.invPresenceS2' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.invPresenceIrrefl' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.evalReadsCounts' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.v1ListReadsCounts' depends on axioms: [propext, Quot.sound]
    'S9Obligations.WitnessTypes.sepV1IndistinguishableViaCounts' depends on axioms: [propext, Quot.sound]

Files of this stage: the module, the root import line, the 30 report
lines, the 30 inventory entries (32 each after the repair after full-run
audit 1), and this section together with the
pointer paragraph at the end of step 26.  Nothing else in this tree,
and nothing sealed, was written by this stage; the receipt,
`witness_types.py`, `run_witness_types.py`, and `test_witness_types.py`
were not edited by it, and this part's tests (including the denylist
scan over its five files and the resolver over this document) pass with
this section in place.

## Repair after full-run audit 1

Written by the repair pass that followed the first full-run audit of the
tree (`STATUS.md`, "Repair round 3"), which owned every file of the tree
and changed these of P3's:

* `witness_types.py`: `step21_admission.TOKEN_EQ.price_vs_A3` and the
  S9_3_ADMISSION_NAMED scope say "not contained in A3's bill, which it
  does not contain either" in place of "strictly less than A3's bill"
  (no order on metatheory bills is declared in this tree; under
  inclusion of the listed items the two bills are incomparable); the
  S9_3_WITNESS_OBSERVABLE scope names the Lean half of the separating
  pair by theorem in place of "Lean statements proposed, not proved";
  the PYTHON_ONLY_SCOPE_DECLARED scope carries the bound and says what
  the Lean theorems concern in place of "no Lean theorem of this part
  exists"; `lean_stage_note` records that the Lean stage ran and what
  stays LEAN_NOT_CARRIED.  The names cited are the declared tuple
  `LEAN_STAGE_CITED` under `LEAN_STAGE_MODULE`.  The receipt's
  `revision.round_3` records each change with the wording withdrawn and
  the reason; no count, no first pair, and no Lean target changed
  (`revision.round_3.unchanged_by_the_repair`).
* `test_witness_types.py`: `test_terminal_strings_cite_only_audited_lean_theorems`
  requires every name in `LEAN_STAGE_CITED`, and every `S9_3_`-prefixed
  name the three strings cite, to be listed under the module in
  `AXIOM_REPORT_DECLARATIONS` and declared with `theorem` in the module
  source, and requires the withdrawn phrases to be absent;
  `test_terminals_are_legal_scoped_and_bounded` reads
  `revision.rounds_completed` = 3 and the reworded strings.
* `lean/S9Obligations/WitnessTypes.lean`: `v1ListNodup` and
  `v2AnonListNodup`, both `by decide`, inserted after
  `v1V2AnonListNodup` in file order, with their report lines in
  `lean/S9Obligations/AxiomReport.lean` and their inventory entries in
  `verify_lean.py` at
  the same position; `verify_lean.py` re-run, 83 reports within
  {propext, Quot.sound}, the two new ones with no axioms.  The residual
  of `lean_targets[3].residual` is narrowed again and not closed: every
  length and the absence of repeats in every list are proved, and that
  the entries are the Python questions is still checked by no gate.
* `receipts/witness_types.json`: regenerated twice into two directories
  and compared byte for byte, then installed; SHA-256 and size above.
* This document: the price paragraph of step 21, the terminal bullets
  S9_3_WITNESS_OBSERVABLE and PYTHON_ONLY_SCOPE_DECLARED, the step-33
  paragraph, the Lean section's counts, list, and report lines, and this
  section.

Nothing about S9.3's mathematics changed: every pair count, first pair,
vocabulary size and Lean target is as it was.
