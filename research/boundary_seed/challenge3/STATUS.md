# Challenge 3 — status

`AuthorityEffect: None`.  Session of 2026-09-05, branch
`research/boundary-run`, opened with Challenge 2 in its exact-head review
state (`70dd9258`: 165 tests, line and branch 100%, 84 Lean reports).  One
rung closed: the caller requires `<a|>` and `<|a>` to be internally
separable in a precisely declared sense.

## Order of the work, as committed

1. `a4f2a688` `challenge3/PREDICTIONS.md` frozen, sha256
   `27057895c47e5bd718b0ea8e51689f3325cef78102c912c6feea8e913a7e7755`,
   committed alone before any Challenge 3 code or proof.  The existing
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
loads the repository contract file **whole**, operating manual included, and
that is wider than the five sections the seed's isolation clause names; an
earlier wording of this paragraph said "the contract sections the harness
loads" and is withdrawn as understating it.  The session is in any case an
instrument of the same kind as the one that declared prior exposure.  The paper's section 0 now also discloses
the per-rung adversarial review channel, which supplied the design of two
gates and more than twenty actioned repairs across the run; that disclosure
is this rung's, and it is prose, checked by nothing.

## Results

Receipt `receipts/challenge3.json` (219789 bytes after the review repair,
219403 as the rung closed); full tables in `paper.md` sections 5.9 to 5.12.

| | reading U | reading O |
|---|---|---|
| the current regime meets the declared requirement | **no**: the composite of the side exchange with the mark exchange is a permitted automorphism carrying mark 0 to mark 1 (COMPUTED; PROVED that the composite fixes the regime and carries 0 to 1) | **yes**: the only permitted automorphism is the identity (COMPUTED) |
| the declared sense against its second reading | agree at all 48 points (DEFINITION, by unfolding; COMPUTED that the agreement holds at each) | same |
| the declared sense against Challenge 2's notion | the same at the current regime (COMPUTED) | same |
| what meets the requirement under O | not applicable | the withdrawal of the side exchange, carried by the O reading and paid at genesis; the two names are **not** used (COMPUTED on the exchange coordinate; DEFINITION on the names coordinate, definition 16) |
| the four-cell counterfactual | met exactly where the side exchange is not permitted, whatever the names | identical |
| adding judgment forms, whatever the forms | cannot meet it while the composite is permitted (PROVED for an arbitrary mark property; the concrete `admit_names` point COMPUTED to fail) | not applicable: the composite is not permitted |
| the two mark forms under the composite | neither is invariant, which is why both separate the marks as raw data and neither does so internally (PROVED, a countermodel) | not applicable |
| the declared candidate space | 48 points; one step exactly when the capability count is one (DEFINITION) | same |
| one-step points | six (DEFINITION) | same |
| one-step points meeting the requirement | four, in **three** classes (COMPUTED) | not applicable: the null point meets it at count zero |
| the minimum capability count | **1** (COMPUTED) | **0** (COMPUTED) |
| the minimum is unique | **no**, refuted by three retained classes (COMPUTED, scoped to the declared space) | yes, the null augmentation alone (COMPUTED) |
| the second measure, the collateral count | 1 at each of the three minima; the same three classes selected (COMPUTED) | 0 at the null point |
| the two measures are the same function | no: they differ at points of the space (COMPUTED) | same |
| bundles refused | 41 of 48 (COMPUTED from the declared count) | same |
| adopting reading O under U | count 2, refused as bundling although it meets the requirement (COMPUTED) | not applicable |
| the first minimum: withdraw the side exchange | both side properties become invariant and separating; the index properties do not (COMPUTED census) | not applicable |
| the second minimum: withdraw the mark permutations | both index properties become invariant and separating; **the requirement is met by unfolding**, no permitted renaming moving an index at all (DEFINITION-level, and reported as such) | not applicable |
| the third minimum: one further mark, either side | none of the five declared mark properties is both invariant and separating; the witness is the orbit property alone; the two sides then carry different numbers of marks (COMPUTED; PROVED unboundedly, over every permutation) | not applicable |
| the shared label | invariant under every candidate's renamings and separating nothing; the candidate that keeps the labels meets nothing (COMPUTED) | same |
| the further mark needs a new supply | no: the caller already supplied the token; a token never presented is refused by name (COMPUTED) | same |
| the two retained marks after the further mark | both judgments survive (DEFINITION, an instantiation of the Challenge 1 induction) | same |
| initial datum, reading, event-follows relation | unchanged, and empty on every event of all three declared kinds, five probes in all (DEFINITION for one event; PROVED for histories, by instantiation) | same |
| new event kind or judgment form | none added by the rung | none |

Boundary dependence: the declared sense and its second reading, the identity
of the candidate space, the capability counts, the one-step rule, the refusal
of bundles, the two index mark properties, and the withdrawal of the mark
permutations do not require the admitted boundary.  The side exchange, its
withdrawal, the two side mark properties, the counterfactual square, the
further-mark minimum, and every separation result of the rung require it and
are not formulated after removing it.

**The seed's questions, answered.**  Define the chosen meaning: definitions
38 and 39.  Does the current regime satisfy it under each reading: yes under
O, no under U.  Which declaration made it so under O, and its price in
capabilities: the withdrawal of the side exchange carried by the O reading of
the one admitted primitive, paid at genesis by the declared reading — one
capability, and **not** the two names, which the counterfactual square shows
to be idle.  Under U, every non-isomorphic minimum one-step augmentation over
the declared space, with every undeclared capability counted: three, each at
one capability, all retained; every candidate of count two or more refused as
bundling, including the one that adopts reading O.  Uniqueness: **refuted**
inside the declared space, not proved.  And the seed's warning is earned: the
boundary does not make the requirement trivial, and one of the three minima
meets it while leaving the boundary idle entirely.

## Predictions scored

| id | label | status | note |
|---|---|---|---|
| C2-X | NOT FORCED | **PARTIAL** | five clauses hit: the declared sense is the Challenge 2 notion; under O the requirement holds with no augmentation, at minimum count zero; under U it fails; no candidate that changes only the judgment grammar meets it, which this rung PROVED rather than argued; and at least two tied non-isomorphic minima survive, three in fact.  **MISSED**, recorded next to its value: “every minimum one-step augmentation will either name a side, paying under U what reading O paid at genesis, or admit a further datum that the automorphism cannot carry”.  Two retained minima pay neither — the withdrawal of the side exchange admits no name, and the withdrawal of the mark permutations is neither — and the clause's own falsifier, “a minimum that pays neither a side name nor a further datum”, fired.  A weaker reading counting the withdrawal as paying what reading O paid still misses, on the second of the two (`scores.C2-X.same_clause_on_the_weaker_reading_status`).  The frozen file is untouched |
| C3-1 the declared sense, and a second reading of it | NOT FORCED | HIT, DEFINITION-level | the sense is the run's declaration and the agreement of its two readings is by unfolding; not counted as content |
| C3-2 the current regime, and what does the work under O | FORCED | HIT | content on the side-exchange coordinate, whose cells are searches with both values attained; DEFINITION-level on the names coordinate |
| C3-3 no addition of judgment forms can meet it under U | FORCED | HIT | content: the Lean statement quantifies over an arbitrary property, and its countermodel shows the hypothesis is a real restriction |
| C3-4 the declared candidate space, and the refusal of bundles | NOT FORCED | HIT, DEFINITION-level | the coordinates, values, and capability names are this rung's declarations; not counted as content |
| C3-5 the minimum under U is one, and it is not unique | FORCED | HIT | content: a search at each candidate's own renamings, and the implemented quotient |
| C3-6 the two measures agree on the minimum and are not the same measure | FORCED | HIT | content: witness searches, and a census over the 48 points |
| C3-7 three mechanisms, one of them by unfolding | FORCED | HIT | content on the first and third; the second is DEFINITION-level and the receipt says so separately |
| C3-8 what the reading changes, and what the boundary is charged | NOT FORCED | HIT | content on the two minimum counts and the two class counts; the boundary-dependence map is the run's classification and is not computed |
| C3-X | NOT FORCED | PENDING | scored by Challenge 4 |

Eight of eight scored predictions hit: six as content (C3-2, C3-3, C3-5 to
C3-8) and two by construction (C3-1, C3-4), by the criterion Challenge 1
declared and this rung reuses unchanged.  The counts are the receipt's
`tally`, computed from the statuses and a declared list, and the negative
direction of every one is tested.

**A second clean sweep is weaker evidence than the first, not stronger**, and
two things make it weaker still, both recorded above and in `MANUAL.md`.
The predictions were written by an instrument that had read the whole tree and
reasoned the rung through before writing them.  And **two of the eight were
scored HIT only after the scorer was corrected**: C3-3 was first scored
against a clause the frozen file does not make (“no declared mark property is
invariant”, when the frozen text names the two mark forms of Challenge 2, and
the label property is invariant and separates nothing), and C3-5 was first
compared as an ordered list where the frozen text names four points and no
order.  Both corrections narrow the scorer to the frozen words, which is the
rule this run applies; but a reader should weigh a sweep in which the scorer
moved twice accordingly.  The informative number remains the previous rung's
extrapolation, written before this rung existed: PARTIAL, with its own
falsifier naming the miss.

## Advisories carried from the review of Challenge 2

The rule this rung applies, inherited from Challenge 2: an advisory is
**actioned** when the repair lies in a living document of this rung or in
apparatus; one that would require regenerating a closed rung's receipt, or
editing a previous rung's `STATUS.md`, is **carried** with its reason.

Actioned:

1. `challenge2.py:525`, the tautological receipt keys.  `certified` and
   `replays_from_genesis` compare a replay with itself and cannot be false.
   Actioned for this rung: every candidate row now also carries
   `placement_matches_the_declared_convention`, computed from the presented
   sides and the declared convention alone (B3-PLACEMENT-CHECK), and
   `test_every_candidate_history_replays_from_genesis` rebuilds the events
   from the rendered receipt and replays them rather than reading a boolean.
   The Challenge 2 keys themselves are carried; see below.
2. `challenge2.py:509` and the carried `should_fix` of the same line, the
   hardcoded C1-X price literal.  Actioned in substance for this rung: the
   Challenge 3 price fields are computed —
   `nothing_new_paid_at_challenge_3` is the minimum being zero and
   `new_at_challenge_3` is the capability list of the retained minima — with
   `test_the_price_is_read_off_the_enumeration` fixing both directions.  The
   Challenge 2 field is carried.
3. `claim_ledger.md:980`, B2-TWO-JUDGMENTS's uncovered clause.  The status
   line and the evidence fields now cover “no initial datum and no reading”,
   naming `step_reading`, `step_initialDatum`, `retained_reading`,
   `retained_initialDatum`, and the two receipt keys.
4. `claim_ledger.md:1108`, “under U it buys nothing further about them”.
   Narrowed to what the rung computes, with a pointer to how far Challenge 3
   goes and where that stops too.
5. `challenge1.py:186`, the probe set that omits the event kind Challenge 2
   introduced.  Actioned for this rung: `challenge3.probes` offers all three
   kinds, and `test_the_probe_set_offers_every_event_kind` holds it there.
   The Challenge 1 and Challenge 2 probe sets are carried.
6. `lean/BoundarySeed.lean:8`, the root doc comment (raised twice).  It now
   says Challenges 0 to 3 and states what `verify_lean.py` requires.
7. `paper.md:130`, the definition-locator sentence.  Corrected a second
   time: 27, 28, and 36 are Lean-only, and 37 to 46 are Challenge 3's.
8. `claim_ledger.md:908`, B2-SHARED-MARK-REFUSED's attribution.  The refusal
   is now attributed to low-level `step`, surfaced by certifying `replay`,
   which is what the same rung recorded as a repair in the paper.
9. `paper.md:705`, C2-5's unrecorded reading of “permitted automorphism
   group”.  Section 5.6 now records it: the set of permitted automorphisms,
   scored by its size, with the entries reported beside the count, and no
   structure beyond the set read into the word.
10. `paper.md:315` (carried `should_fix`), definition 33's justifying
    sentence.  Definition 29 now says the invariance is over the
    token-forgetting quotient of definition 14; definition 33's second
    sentence is narrowed to mark properties that forget the presentation
    tokens, with the one line that closes it at the retained regime — both
    labels are `a`, so the image is equal and not merely equal after
    forgetting — and a pointer to Challenge 3's third coordinate, which
    withdraws the forgetting and is computed to separate nothing here.
11. `challenge2.py:864` (both carried `should_fix` variants), C2-8's
    `result_basis`.  The **paper** half is actioned: section 5.6 now scopes
    C2-8's content to its three search clauses and says that the absence of
    a side-exchanging automorphism under O follows from a declaration.  The
    receipt half is carried.
12. `paper.md:30` (carried `should_fix`), the undisclosed review channel.
    Section 0 now names it beside the surviving provenance claim, says its
    findings are actioned or carried with reasons in each challenge's
    status, names the two gates whose design came from outside the run, and
    says what the channel has not supplied.

Carried, with reasons:

13. The Challenge 2 receipt keys `retained.certified` and
    `retained.replays_from_genesis`, and the hardcoded C1-X price literal,
    and C2-8's `result_basis`, and C2-6's per-reading constant conjunct
    (`challenge2.py:500`).  All four repairs lie inside
    `code/boundary/challenge2.py` and would regenerate a closed rung's
    receipt.  None can change that rung's recorded statuses, and the paper
    now carries the correction for C2-8.
14. The Challenge 1 probe set (`challenge1.py:186`) and the four advisories
    Challenge 2 itself carried (its items 17 to 21).  Same reason: they lie
    in `code/boundary/challenge1.py` or in a frozen `STATUS.md`.
15. `challenge1History` and `admitted` keep their names, as Challenge 2
    decided; the axiom log, the ledger, and two frozen receipts cite the
    theorem names built on them.

A dedicated repair session for Challenges 1 and 2 would clear items 13 to
15 in one deliberate regeneration.  That is not this rung's work.

## Where the run reached for a remembered result (declared reading 0)

- **The shape of the answer was reasoned, not remembered, but the vocabulary
  was not.**  “Automorphism”, “orbit”, “invariant”, and the idea that
  withdrawing a generator of a renaming set separates what the generator
  identified are standard mathematics this instrument knows.  They are not
  derived here; they are declared as definitions 32, 33, 37, and 39 and used.
- **The two measure identifiers are remembered, not derived.**  `mu1` and
  `mu2` are the names the sealed derivation gives its own two declared cost
  measures over a candidate space of one-step augmentations — the same two
  names for the same role — and the repository contract file, which the
  harness loads whole, says so.  This rung introduced them without noticing
  that.  What the two measures ARE here is this rung's: the capability count
  and the collateral count, declared at definitions 41 and 44 and computed.
  The names are inheritance, and are recorded as such so that a later
  comparison cannot read the coincidence as convergence.  Found by review,
  not by the run.
- **What was derived, and in this order.**  That the counterfactual square
  turns on one coordinate only, so the O names are idle; that withdrawing the
  mark permutations meets the requirement by unfolding and leaves the boundary
  idle; that admitting a further mark meets it through unequal side counts and
  that no declared mark property witnesses it; that the two further-mark
  points are one class and the two withdrawals are two; and that the
  reading-O bundle costs two while its withdrawal half costs one.  All of
  those were worked out by hand before the predictions were frozen and then
  confirmed by the code — which is the honest description, and it is why the
  sweep is weak evidence.
- **Nothing in the numbers was remembered.**  48, 41, three classes, the
  177-image census inherited from Challenge 2, and the 85-regime property
  domain are the code's.
- **The Lean file's shape** — a concrete regime, a general theorem over an
  arbitrary property, a countermodel showing the hypothesis is not vacuous —
  follows the Challenge 1 and Challenge 2 files, which the session read.
- The **count argument** in Lean (a permutation preserves each side's count;
  the side exchange exchanges them) is elementary and remembered as a
  technique.  What is derived is that it applies exactly at the further-mark
  candidate and exactly does not apply at the retained regime, which is why
  `retained_counts_equal` is in the file.
- The **design of the placement check and of the disclosure in section 0**
  came from the review channel, not from the run; both are recorded above.

## Leftovers, for Challenge 4 and later

- Score C3-X: whether Challenge 4's reader bound must be widened, whether the
  retained placement is `(0, 1, 0, 1)`, whether the U requirement fails again
  at the same minimum count, and whether the matching of a visible mark
  across the boundary stays internally unavailable.
- **The declared space is five coordinates wide and no wider.**  A model in
  which the permitted renamings were derived from the judgment grammar rather
  than declared (definition 16) is a different space: there, admitting the
  side names would withdraw the side exchange in one move, and the
  enumeration would have to be redone.  It is OPEN and named in section 10.
- Whether the requirement should have been declared so as to exclude the
  index-withdrawal minimum is OPEN.  The rung reports that candidate rather
  than repairing the requirement, because repairing it after seeing the
  enumeration would be fitting the declaration to the answer.
- The three minima are tied under both declared measures.  A third measure
  could separate them; none is offered, and inventing one now would have the
  same defect.
- Lean does not close the enumeration, the capability counts, the class
  count, or the collateral facts.  A Lean statement that the permitted
  renamings of a two-mark regime are exactly those listed remains a candidate
  target, not attempted — it is the same leftover Challenge 2 recorded.
- The correspondence between the Lean `List.Perm` renaming and the Python
  `rename_marks` is prose, not a theorem.  B3-COUNT-ARGUMENT says so.
- The equal-count law of Challenge 0 is now half proved: at unequal counts no
  renaming undoes the side exchange.  The converse — that at equal counts one
  does — is not proved and is a candidate target.
- Every capability this rung enumerates is a candidate and none is admitted.
  A later rung that takes one of the three minima must say which, and pay it.
- Challenge 0 to Challenge 2 leftovers survive: no Lean statement of the
  class-count closed forms; no unbounded canonical-key theorem; the freeze
  manifest protocol remains OPEN.
- Items 13 to 15 above are open work for a dedicated Challenge 1 and 2 repair
  session, not for Challenge 4.

## Repairs and live failures during the rung

- `extra_mark = 0` was dropped from the enumeration because each coordinate
  was tested against a shared falsehood and `0` equals falsehood in this
  language; the point `extra_mark_0` vanished and the scorer raised looking
  for its row.  Each coordinate is now tested against its own inherited
  value.  Row in `MANUAL.md`; `test_side_zero_is_a_moved_coordinate` fixes it.
- The C3-3 and C3-5 clauses were first scored against words the frozen file
  does not contain, and both reported MISSED; both are now scored on the
  frozen words.  Rows in `MANUAL.md`, and the weakening of the sweep is
  recorded above.
- A Lean decision procedure refused a goal carrying the reading as a free
  variable — the same defect Challenge 2 met.  Two placement lemmas project
  the reading away first.
- Every gate this rung added or touched has an injection row in `MANUAL.md`,
  and no receipt, log, or pin was regenerated while any injection was live.
  That sentence was **false when the rung closed** and review found it: two
  checks the rung added, the placement check and the probe-set check, had no
  row and no negative-direction test, so each could only ever have read true.
  Both were injected in the repair session — the further mark's admission
  moved to the other side, and the occurrence admission dropped from the
  probe set — each named its object, each recovered, and each now has a row
  in `MANUAL.md` and a test of its negative direction.

## Gates run in this session

| gate | result |
|---|---|
| `verify_pins.py` | `pins ok: seed ba30bcd600d8 and 4 frozen prediction file(s)` |
| `unittest discover -s tests` | `Ran 222 tests`, OK |
| `mypy` (strict, tree pyproject) | `Success: no issues found in 24 source files` |
| `coverage` + `check_coverage.py` | `line 100.00% branch 100.00% over 7 files` |
| `run_challenge0.py` … `run_challenge3.py` | `unchanged: receipts\challenge0.json (5553 bytes)`; `unchanged: receipts\challenge1.json (28363 bytes)`; `unchanged: receipts\challenge2.json (35499 bytes)`; `unchanged: receipts\challenge3.json (219403 bytes)` |
| `git diff --exit-code -- receipts` | clean |
| `verify_lean.py` | `lean ok: 105 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; the log was regenerated deliberately once, 84 to 105, with no injection live |
| `ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, 130 files with pinned hits, 1826 hits, census matches its pin`; no pin regenerated |
| `tests/test_primitive_contact.py` | firewall passes |
| `ci/check_paper_citations.py` | `paper cross-references resolve: 62 citation(s) across 29 document(s)` |
| injections | nine rows in `MANUAL.md`, six injected and three found live |

The exact-head review repair re-ran the same battery on the same branch and
moved four of those readings: `Ran 227 tests`, OK, with the workflow grep
moved from 222 to 227; `Success: no issues found in 24 source files`;
`line 100.00% branch 100.00% over 7 files`; and
`unchanged: receipts\challenge3.json (219789 bytes)` after one deliberate
regeneration with no injection live.  The pins, the Lean audit at 105
reports, the watchlist at 1826 hits with no pin regenerated, the firewall,
and the paper cross-references are unchanged.  Four rows were added to the
injection record: the placement check, the probe-set check, that receipt
regeneration, and the test-count grep.

## Next session

Open Challenge 4 fresh: read the handoff, the seed, `PLAN.md`, `MANUAL.md`,
and this file; write and commit `challenge4/PREDICTIONS.md` with its own
extrapolation before any code; score C3-X.

The state Challenge 4 inherits.  **Nothing was admitted at Challenge 3.**
Under each reading the current regime is still the replay of the Challenge 2
caller history
`[Supply(a), AdmitOccurrence(a, 0), Supply(a), AdmitOccurrence(a, 1)]`: two
marks, placement `(0, 1)`, labels `("a", "a")`.  The three minima are
candidates, priced and retained, and none of them is taken: the permitted
renamings, the judgment grammar, the serialization, and the placement are all
exactly as Challenge 2 left them.  A rung that wants one of the three must
say which and pay it.

What Challenge 3 adds to the inheritance: the declared sense of internal
separability and its second reading (definitions 38, 39); the flagged
renaming enumerations in the kernel (definition 37), which reduce to the
reading's own at the reading's flags; the declared candidate space and the
one-step rule (definitions 40, 41), available for reuse if Challenge 4 wants
them; the theorem that no addition of judgment forms can separate two marks a
permitted automorphism exchanges; and the count argument, which says that a
placement whose two sides carry different numbers of marks admits no renaming
undoing the side exchange.

Challenge 4 supplies and retains `<a|b>` and `<b|a>` — two marks in one
whole, one on each side of the bar — and requires their internal separability
in the declared sense.  The reader of `presentation.py` refuses more than one
mark per whole by name, so the bound must be widened deliberately and priced;
the run's own extrapolation C3-X says the retained placement will be
`(0, 1, 0, 1)`, that the two sides will carry equally many marks, and that
the requirement will therefore fail again under U and hold under O.  Freeze
the predictions before looking.  The seed's own question for that rung is
what the boundary contributes there that it did not contribute here, and what
it cannot contribute; the honest candidate for the second half, on this
rung's evidence, is the matching of a visible mark across the boundary.
