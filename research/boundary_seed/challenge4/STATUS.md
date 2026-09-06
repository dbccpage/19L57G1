# Challenge 4 — status

`AuthorityEffect: None`.  Session of 2026-09-05, branch
`research/boundary-run`, opened with Challenge 3 in its second exact-head
review-repair state (`5c43c5ee`: 228 tests, line and branch 100%, 105 Lean
reports).  One rung closed: the caller supplies and retains `<a|b>` and
`<b|a>` and requires their internal separability in the declared sense.

## Order of the work, as committed

1. `f07a20c4` `challenge4/PREDICTIONS.md` frozen, sha256
   `42371f458e23ce89885a76c542863c112482c0ca6b4f1d9ff6a058b3c21f2041`,
   committed alone before any Challenge 4 code or proof.  The existing
   `challenge*/PREDICTIONS.md -text` attribute already covered it
   (`git check-attr` reports `text: unset`), so no attributes change was
   needed.
2. The rung commit: kernel, Lean, receipt, tests, prose, registration, and
   the injections below.

This history proves “committed before” only.  It cannot prove when any
untracked or off-tree code or proof was written, and it is not evidence of
insight.

## Provenance ceiling

Inherited unchanged: `SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE`.  This
session read nothing outside the write root and the seed, but the harness
loads the repository contract file **whole**, operating manual included, which
is wider than the five sections the seed's isolation clause names; and the
session is an instrument of the same kind as the one that declared prior
exposure.  The per-rung adversarial review channel, disclosed in the paper's
section 0 at the previous rung, supplied this rung's advisory list; it supplied
no definition, candidate, or result.

## Results

Receipt `receipts/challenge4.json` (795960 bytes, after the review repair
below regenerated it from 795554); full tables in `paper.md` sections 5.13 to
5.16.

| | reading U | reading O |
|---|---|---|
| the Challenge 1 reader on the caller's inscriptions | refuses both by name (COMPUTED; the bound is that rung's DEFINITION) | same |
| the widened reader, and the within-whole order | two declarations of this rung, paid by the run (DEFINITION) | same |
| the retained configuration | four marks, placement `(0, 1, 0, 1)`, labels `("a", "b", "b", "a")`, groups `(0, 0, 1, 1)`; certified, replayed from genesis, matching the placement the declarations predict (DEFINITION for the history; COMPUTED for the replay and the placement check) | same |
| the other within-whole order | isomorphic: not internally available (COMPUTED) | same |
| the grouping of marks into wholes | metatheory: the regime carries no such component (a fact about the declared type, not computed) | same |
| **the requirement at the current configuration** | **not met** (COMPUTED; PROVED that the whole exchange carries the regime onto itself) | **not met** — the first rung at which O does not already meet it (COMPUTED; PROVED) |
| what carries one whole onto the other | the exchange of the two wholes, permutation `[2, 3, 0, 1]`, **using no side exchange** (COMPUTED; PROVED) | the same map, and under O it is the only kind there is |
| permitted automorphisms of the retained configuration | eight, over 48 images (COMPUTED) | four, over 24 (COMPUTED) |
| pairs of distinct marks that are separable | none of the six (COMPUTED) | four of the six: exactly the pairs on different sides (COMPUTED; PROVED for the two that are not) |
| the two sides carry | two marks each, so the Challenge 3 counting argument says nothing (COMPUTED; PROVED) | same |
| adding judgment forms, whatever the forms | cannot meet it while the whole exchange is permitted (PROVED for an arbitrary property of a pair of marks, with a countermodel) | same |
| any continuation whatever | never removes the obstruction (PROVED over every history, which is stronger than the enumeration) | same |
| the declared candidate space | 192 points; one step exactly when the capability count is one (DEFINITION) | same |
| one-step points | eight (DEFINITION) | same |
| one-step points meeting the requirement | **one**: withdraw the mark permutations (COMPUTED) | **two**: withdraw the mark permutations, or keep the presentation labels (COMPUTED) |
| the minimum capability count | **1** (COMPUTED) | **1** (COMPUTED) |
| the minimum is unique | **yes**, one class — the first rung at which uniqueness is not refuted, and inside the declared space only (COMPUTED, scoped) | **no**, two tied classes, both retained (COMPUTED) |
| the second measure at the minima | 2 (COMPUTED) | 3 at each (COMPUTED) |
| the two measures | not the same function; they select the same minima under both readings (COMPUTED) | same |
| bundles refused | 183 of 192 (COMPUTED from the declared count) | same |
| admitting the whole grouping alone | does not meet it: the tag exchange is then a renaming the object language cannot see (COMPUTED) | same |
| naming the wholes without the grouping | a no-op collapsing into the null point (COMPUTED quotient) | same |
| the grouping WITH the names | meets it, at count 2, refused as a bundle (COMPUTED) | same |
| keeping the presentation labels | does **not** meet it: the two wholes are each other's reflection (COMPUTED) | **meets** it: a label with a side is what the witness reads (COMPUTED) |
| the witness at each satisfying one-step point | the index property (COMPUTED census) | the index property; the label-and-side property (COMPUTED census) |
| the matching of a visible mark across the boundary | not internally available (COMPUTED) | same |
| the pointwise sense against the requirement | implies it at every point; the converse fails at 18 points (COMPUTED) | implies it at every point; the converse fails at 16 (COMPUTED) |
| at the Challenge 3 configuration | the two senses agree (COMPUTED) | same |
| initial datum, reading, event-follows relation | unchanged, empty on every event of all three declared kinds (DEFINITION for one event; PROVED for histories) | same |
| new event kind or judgment form | none added by the rung | none |

Boundary dependence: the declared sense, its second reading, the pointwise
sense, the identity of the candidate space, the capability counts, the one-step
rule, the refusal of bundles, the two grouping coordinates, the tag and index
properties, and the withdrawal of the mark permutations do not require the
admitted boundary.  The side exchange, its withdrawal, the two side-reading
whole properties, the label-and-side property, the grouping square's cells, the
further-mark coordinate, and every separation result of the rung except the
index withdrawal require it and are not formulated after removing it.

**The seed's questions, answered.**  What does the boundary contribute here
that it did not contribute at Challenge 3?  Nothing new in kind: it contributes
the side each mark lies on, exactly as there.  What is new is the
configuration, not the contribution — each side now carries one mark of each
whole, so that contribution sorts the four marks into two classes of two and no
finer and separates no whole from the other, under either reading.  Its one
sharper effect is indirect: under O a label together with a side is what makes
the label-keeping candidate a minimum, and without the boundary the labels
alone would separate nothing.  What can it not contribute?  Which mark within a
side is which; the grouping of marks into wholes, which the state does not
carry at all; and the matching of a visible mark across the boundary, the
configuration with the second whole's `a` replaced by an unpresented token
being reached by a permitted renaming under both readings.

## Predictions scored

| id | label | status | note |
|---|---|---|---|
| C3-X | NOT FORCED | **PARTIAL** | six clauses hit: the reader bound had to be widened and is paid by the run; the retained placement is `(0, 1, 0, 1)`; the two sides carry equally many marks and a side-exchanging automorphism exists under U; the requirement fails under U at a minimum count of one; the boundary contributes the side each mark lies on; and the cross-boundary matching stays internally unavailable under both readings.  **MISSED**, recorded next to its value: “and hold again under O with no new declaration”.  Under O the requirement FAILS, the exchange of the two wholes needing no side exchange, and the clause's own falsifier — “the O requirement needing a new declaration” — fired.  With it the clause that the boundary contributes here **exactly** what it contributed at Challenge 3 is MISSED, that contribution having met the requirement under O there and not here.  The frozen file is untouched |
| C4-1 the reader bound, and what the retention makes | FORCED | HIT, DEFINITION-level | the refusal is the Challenge 1 bound replayed and the configuration follows from four declarations; not counted as content |
| C4-2 the requirement fails under both readings | FORCED | HIT | content: automorphism and pair searches at each reading's own renamings |
| C4-3 what the boundary contributes, and what it cannot | NOT FORCED | **PARTIAL** | three clauses hit: neither side-reading whole property separates the two wholes; the cross-boundary matching is unavailable; keeping the labels parts the two readings.  **MISSED**, recorded next to its value: “both declared side-reading whole properties are invariant under both readings”.  Under U they are not, the side exchange being a permitted renaming that moves a mark's side — which is the same fact that made the Challenge 2 mark forms non-invariant under U, established two rungs earlier and not carried forward when the prediction was written.  The receipt reports the value per reading |
| C4-4 the declared candidate space | NOT FORCED | HIT, DEFINITION-level | the coordinates, values, and capability names are this rung's declarations; not counted as content |
| C4-5 the minimum under U, and its uniqueness | FORCED | HIT | content: a search at each candidate's own renamings and the implemented quotient; that the minimum meets the requirement by unfolding is DEFINITION-level and reported separately |
| C4-6 the minima under O | FORCED | HIT | content: the same search and quotient under the other reading |
| C4-7 the grouping is a bundle | FORCED | HIT | content: each cell of the grouping square is a search with both values attained |
| C4-8 the two senses part | FORCED | HIT | content: a census over the 192 points, with the reduction computed |
| C4-X | NOT FORCED | PENDING | scored by Challenge 5 |

Seven of eight scored predictions hit and one is PARTIAL: five as content
(C4-2, C4-5 to C4-8) and two by construction (C4-1, C4-4), by the criterion
Challenge 1 declared and this rung reuses unchanged.  The counts are the
receipt's `tally`, computed from the statuses and a declared list, and the
negative direction of every one is tested.

**This rung's sweep is not clean, and that is the useful part.**  C4-3's
invariance clause is false under U for a reason this run had established two
rungs earlier; that is a miss of attention rather than of computation, and it
is recorded next to its value rather than reworded.  The informative number
remains the previous rung's extrapolation, written before this rung existed:
PARTIAL, on the clause that mattered most, with its own falsifier naming the
miss.  As at every earlier rung, the predictions were written by an instrument
that had reasoned the rung through, so the hits are evidence of the order of
the work.

## Advisories carried from the review of Challenge 3

The rule, inherited: an advisory is **actioned** when the repair lies in a
living document of this rung or in apparatus; one that would require
regenerating a closed rung's receipt, or editing a previous rung's
`STATUS.md`, is **carried** with its reason.  Every advisory is listed;
`change_log.md` carries each repair with its reason.

Actioned:

1. `paper.md:1`, the title still scoping the paper to Challenges 0 to 2, then
   0 to 3.  It now says 0 to 4, and section 0's counts move with it.
2. `paper.md:1036` and its three duplicates, the paper counting four hitting
   C2-X clauses where the status and the receipt count five.  Section 5.10 now
   counts five and says which.
3. `paper.md:1012`, "the converse half".  Section 5.9 now says the converse is
   NOT proved and states what `retained_counts_equal` does record.
4. `paper.md:1380`, the countermodel said to show the theorem is not vacuous.
   Section 7.4 now says its HYPOTHESIS is a real restriction, which is what
   the same section says correctly four lines earlier.
5. `paper.md:1370`, the 7.4 row for `retained_U_requirement_fails`.  It now
   says the SIDE EXCHANGE is permitted and the composite fixes the regime.
6. `paper.md:423` and `paper.md:440`, `mu1` and `mu2` used with no
   remembered-vocabulary note.  Definition 41 now carries the disclosure that
   both identifiers are the sealed derivation's own names for the same role.
7. `paper.md:1020`, "internal designation" as a second sense of a reserved
   word.  Every use in the paper's prose now reads "internally available",
   definition 3's included.  The sweep did NOT reach code or Lean comments: it
   left the phrase in this rung's own `challenge4.py` capability text, in the
   `Challenge4.lean` doc comment, and in `challenge3.py`.  The first two are
   repaired in the review repair below; the third is carried, its repair
   regenerating a closed rung's receipt.  The narrowed claim is that the
   sweep covered the documents named here and not the whole tree.
8. `paper.md:1049` (carried `should_fix`), the label-keeping candidate written
   without a reading.  Section 5.9 now scopes it to U and says what happens
   under O.  The `challenge3/STATUS.md` half is carried.
9. `challenge3.py:996`, `points_satisfying_with_grammar_change_only` including
   the serialization coordinate.  The paper's row now says the key is empty
   under U by its own reading clause and that it admits the label-keeping
   coordinate; the key is carried.
10. `paper.md:1106` and `paper.md:1055` (carried `should_fix`), the
    boundary-dependence row reading "every separation result of the rung" with
    no exception.  Section 5.12 now names the exception; the receipt field is
    carried.
11. `claim_ledger.md:1098` (carried `should_fix`), B2-MARKS-O.  The narrowing
    is now written into that entry, the paper's C2-6 row carries the same
    note, and B3-O-ALREADY-MET's attribution sentence names the Challenge 2
    receipt's price field rather than the ledger entry.
12. `claim_ledger.md:1408` (carried `should_fix`), B3-THREE-MINIMA's merge
    attributed to the side exchange alone.  It now says the class key decides
    it, the side exchange composed with a mark renaming.
13. `paper.md:1544` (carried `should_fix`), section 9's restatement of the
    Challenge 3 second reading.  It now names the token-forgetting clause and
    says which direction is by unfolding and which is prose.
14. `challenge3.py:958`, `one_step_minima`'s docstring.  Corrected in place;
    no receipt carries a docstring and all five regenerate byte-identically.

Carried, with reasons:

15. `challenge3.py:953`, the `points_satisfying_with_grammar_change_only` key
    itself; `challenge3.py:1140` and `:1163`, the C3-3 scorer's
    judgment-vocabulary conjunct and its weaker Python proxy for
    non-invariance under the composite; and the Challenge 3 receipt's
    `boundary_dependence` text.  All four lie in `code/boundary/challenge3.py`
    and would regenerate a closed rung's receipt.  None can change that rung's
    recorded statuses, and the paper now carries the correction for each.
16. `challenge3/STATUS.md:64`, the "same" cell for the label-keeping candidate
    under O.  A previous rung's status is not edited; the paper carries the
    correction, and this row records what the receipt computes: under O that
    candidate meets the requirement because the base does not — it meets it
    because the candidate's own renamings, with labels kept and no side
    exchange, admit only the identity — and it makes the label and the
    cross-boundary matching available at a collateral count of 3.
17. The Challenge 1 and Challenge 2 items 13 to 15 of the Challenge 3 status
    survive unchanged: they lie in `challenge1.py`, `challenge2.py`, or a
    frozen `STATUS.md`.

A dedicated repair session for Challenges 1 to 3 would clear items 15 to 17 in
one deliberate regeneration.  That is not this rung's work.

## Where the run reached for a remembered result (declared reading 0)

- **The vocabulary is standard mathematics and is not derived here.**
  "Automorphism", "orbit", "invariant", "permutation", and the idea that a
  structure the state does not carry cannot be separated by anything the state
  determines are known to this instrument.  They are declared as definitions
  51 to 55 and used.
- **The shape of the whole-property census follows Challenge 3's**, which this
  session read: a declared list of properties, a bounded domain, invariance,
  separation, and a witness column.  What is NOT inherited is the second
  conjunct, key-determination; that was forced by a defect the census produced
  on its first run, and the run wrote the conjunct to answer it.
- **The Lean file's shape** — a concrete regime, an obstruction that is `rfl`,
  a general theorem over an arbitrary property, a countermodel — follows
  Challenges 1 to 3, which the session read.  The continuation induction
  (`replay_placement_append`) is elementary and remembered as a technique.
- **What was derived, and in this order.**  That the two wholes are each
  other's reflection and that this is why keeping the labels parts the two
  readings; that the exchange of the two wholes needs no side exchange and so
  defeats reading O for the first time; that the grouping alone leaves the tag
  exchange free and so is not a minimum, while the grouping with the names is a
  bundle; that the two senses of separability part exactly where the wholes
  separate and the marks do not; and that no continuation removes the
  obstruction.  All of those were worked out by hand before the predictions
  were frozen and then confirmed by the code, which is why the sweep is weak
  evidence — and one of them, the invariance of the side properties under U,
  was worked out wrong.
- **Nothing in the numbers was remembered.**  192, 183, 8 and 4 automorphisms,
  four separable pairs of six, 18 and 16 parting points, 768 domain
  configurations, 138 axiom reports (139 after the review repair below): all
  the code's.
- **The tag-level U/O echo is the run's own observation**, made while writing
  the grouping coordinates: that naming the two whole tags stands to the
  grouping as reading O stands to the boundary.  It is used to justify two
  coordinates rather than one, and it is a declaration, recorded as such in
  B4-CANDIDATE-SPACE because a run that declared one coordinate would report a
  second minimum under both readings.

## Leftovers, for Challenge 5 and later

- Score C4-X: whether Challenge 5's reader must be widened a second time,
  whether depth is an internally available count, whether the inner whole is a
  datum, and whether the decision takes the form of a declared finite policy
  space.
- **The uniqueness of the U minimum is uniqueness inside the declared space.**
  It is the run's first uniqueness statement and the easiest thing here to
  overstate.  A wider space — one that declared the grouping and its naming a
  single coordinate, or that grouped marks by something else — would report
  more minima, and nothing here rules such a space out.
- The requirement is about a structure the state does not carry, and so is its
  witness.  Whether the requirement should have been declared so as to be
  about the state alone is OPEN; the rung reports the narrowing rather than
  repairing it, because repairing it after seeing the enumeration would be
  fitting the declaration to the answer.
- The Challenge 3 whole-property census carried the invariance conjunct only.
  No result of that rung moves, but the two censuses are not the same test, and
  a reader comparing them should know it.  Whether the Challenge 3 census would
  report anything different under this rung's clause is not computed here.
- The correspondence between the Lean `exchangeWholes` index map and the Python
  renaming of a configuration is prose, as `List.Perm` against `rename_marks`
  was at Challenge 3.
- Lean does not close the enumeration, the automorphism counts, the class
  counts, the two measures, or the whole-property census.
- The closure premise under definition 54's "by construction" is inherited from
  Challenge 3 and is still checked by nothing.
- Challenge 0 to Challenge 3 leftovers survive: no Lean statement of the
  class-count closed forms; no unbounded canonical-key theorem; the freeze
  manifest protocol remains OPEN.

## Repairs and live failures during the rung

- **The whole-property census reported a witness where the requirement fails.**
  On its first run it carried invariance alone, and the property that reads the
  group tag — which no key carries unless the grouping is admitted — was
  reported as invariant, separating, and therefore a witness at the base of
  both readings.  The repair is definition 55's second conjunct, together with
  a domain that varies the grouping and a census over every two-element
  mark-set; without either the property is constant by construction.  Row in
  `MANUAL.md`, injected and reversed, and
  `test_the_key_determination_census_reads_both_ways` fixes both directions.
- **Two prediction clauses were first scored against words the frozen files do
  not contain**, C4-3's and C3-X's side-property clauses, and both reported
  MISSED.  Both are now scored on the two side-reading properties the frozen
  texts name.  Row in `MANUAL.md`; the same defect appeared twice at
  Challenge 3.
- **The receipt was too close to its bound and the build too slow.**  936733
  bytes with a 6% margin, and 9.9 seconds.  Restructured: one enumeration per
  candidate rather than fifteen, and the collateral facts that hold rather than
  eight booleans on each of the 384 point rows.  795554 bytes, 2.9 seconds.
- **A `git checkout` of the root Lean module during an injection reversal
  dropped the whole rung's audit lines**, and the audit-totality check named
  the module and all 33 theorems.  Recorded as a found-live row rather than
  quietly repaired: it is exactly what that check was added at Challenge 2 to
  catch, and the recovery was to rewrite the lines and re-verify at 138
  reports.
- Every gate this rung added or touched has an injection row in `MANUAL.md`,
  and no receipt, log, or pin was regenerated while any injection was live.

## Review repair of this rung

The review of Challenge 4 returned nine surviving findings, all `should_fix`
and two of them the same defect seen from two sides.  The frozen
`challenge4/PREDICTIONS.md` was not touched, no prediction changed status, and
no result of the rung moved.  Each repair is a line in `change_log.md` with its
reason.  Declined: nothing.

Actioned:

1. The paper said the boundary's failure to separate either same-side pair was
   proved, and cited one theorem, which covers marks 0 and 2 only.  The
   companion `crossRetained_other_marks_share_a_side` now proves it of marks 1
   and 3, so both pairs are proved and not one; the three prose sites and the
   two ledger entries cite both, and the axiom log was regenerated deliberately
   from 138 to 139 reports with no injection live.
2. "Which is proved rather than computed" is withdrawn from the same sentence:
   the receipt's `base.separable_mark_pairs` computes both exclusions, and the
   sentence now says the receipt computes it and Lean proves it.
3. The boundary's price table counted two of the five declared whole properties
   as needing the boundary where the receipt's own capability text and section
   5.16 count three; the third is the label-and-side property, whose body reads
   the placement.  The table now says three, naming which.
4. B4-WITNESS-CLAUSE stated an emptiness result "at every point that fails the
   requirement" while the census is computed only at the base and the eight
   one-step points; the entry is scoped to those nine rows per reading and says
   the 192 point rows carry no witness column.
5. This rung's own receipt repeated the boundary-dependence defect the rung
   said it corrected: its fifth key read "every separation result of the rung"
   with no exception, contradicting the key above it, which classifies the
   index withdrawal as independent of the boundary, and it omitted the grouping
   square's cells.  The key in `challenge4.py` now carries both, and
   `receipts/challenge4.json` was regenerated deliberately, 795554 to 795960
   bytes, with no injection live.  With that the ledger's B4-BOUNDARY-DEPENDENCE
   and the paper's section 5.16 row are what the receipt says.
6. B4-GROUPING-IS-METATHEORY was the only ledger entry with no **Axiom
   report** field, one of the nine the ledger's own header requires of every
   entry; it now reads "not applicable", as the other Lean-less entries do.
7. "Internal designation", a second sense of a word the run reserves for
   current-state designation, was reintroduced by this rung in
   `challenge4.py`'s capability text and in the `Challenge4.lean` doc comment,
   and reached the receipt three times.  Both now read "internally available"
   and the receipt carries the phrase nowhere.  The claim that every use in the
   run's own prose had been swept is narrowed above to the documents the sweep
   actually covered; `challenge3.py` keeps the phrase and is carried, its
   repair regenerating a closed rung's receipt.
8. The reduction of the whole sense to the Challenge 3 sense was presented as
   computed content and counted in C4-8's basis, but at singleton wholes the
   set test unfolds to the mark test over the same automorphism list, so the
   two senses cannot disagree there and the frozen falsifier naming that
   disagreement cannot fire.  Definition 52, the C4-8 basis in the paper and in
   the receipt, and the two ledger entries now label it DEFINITION-level and
   say that C4-8's content rests on the 192-point census and the parting
   points.  C4-8 remains HIT: the census and the parting points are unchanged.

Carried: `challenge3.py`'s capability text, alongside items 15 to 17 above,
for the same reason those are carried.

## Gates run in this session

| gate | result |
|---|---|
| `verify_pins.py` | `pins ok: seed ba30bcd600d8 and 5 frozen prediction file(s)` |
| `unittest discover -s tests` | `Ran 303 tests`, OK |
| `mypy` (strict, tree pyproject) | `Success: no issues found in 27 source files` |
| `coverage` + `check_coverage.py` | `line 100.00% branch 100.00% over 8 files` |
| `run_challenge0.py` … `run_challenge4.py` | `unchanged` for all five receipts: 5553, 28363, 35499, 220518, 795960 bytes |
| `git diff --exit-code -- receipts` | clean |
| `verify_lean.py` | `lean ok: 139 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; the log was regenerated deliberately twice, 105 to 138 in the rung and 138 to 139 in the review repair, with no injection live either time |
| `ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, 130 files with pinned hits, 1826 hits, census matches its pin`; no pin regenerated |
| `tests/test_primitive_contact.py` | firewall passes |
| `ci/check_paper_citations.py` | paper cross-references resolve |
| injections | twelve rows in `MANUAL.md` for this rung: six injected, four found live, and two from the review repair — the stale-receipt failure and the deliberate axiom-log regeneration |

## Next session

Open Challenge 5 fresh: read the handoff, the seed, `PLAN.md`, `MANUAL.md`,
and this file; write and commit `challenge5/PREDICTIONS.md` with its own
extrapolation before any code; score C4-X.

The state Challenge 5 inherits.  **Nothing was admitted at Challenge 4 beyond
the caller's own retention.**  Under each reading the current configuration is
the replay of the Challenge 4 caller history — four marks, placement
`(0, 1, 0, 1)`, labels `("a", "b", "b", "a")`, grouping `(0, 0, 1, 1)` read off
that history and carried by no regime.  The minima are candidates, priced and
retained, and none is taken: the permitted renamings, the judgment grammar, the
serialization, and the placement are exactly as Challenge 2 left them.  A rung
that wants one must say which and pay it.

What Challenge 4 adds to the inheritance: the widened reader and the
within-whole order, both paid; the configuration type that keeps a regime and a
grouping apart; the declared whole sense of separability with its orbit witness
and the pointwise sense beside it; the whole-property census with its
key-determination clause, which is the generalization of definition 29 and is
available for reuse; the declared seven-coordinate space; and the Lean
continuation theorem, which says that no later history removes an obstruction
that fixes a regime's placement prefix.

Challenge 5 supplies and retains `<<a|>|>` — a whole within a side.  This
rung's reader refuses it by name, which the receipt records and does not act
on, so the bound must be widened deliberately a second time and priced again.
The seed's own questions for that rung are whether the object language can see
a boundary within a side; whether a whole on a side is a datum, a side, or
something needing a new definition; what "within" means at depth two under each
reading; whether depth is an internally available count; and what admission, if
any, is needed to treat the inner whole as the outer whole was treated.  Do not
assume nesting is admissible; do not assume it is not.  Freeze the predictions
before looking.
