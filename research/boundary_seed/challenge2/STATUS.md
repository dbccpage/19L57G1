# Challenge 2 — status

`AuthorityEffect: None`.  Session of 2026-09-05, branch
`research/boundary-run`, opened with Challenge 1 in its fifth-repair state
(`a330da4f`: 114 tests, line and branch 100%, 56 Lean reports).  One rung
closed: the caller supplies and retains `<a|>` and `<|a>`.

## Order of the work, as committed

1. `22d9ea4b` `challenge2/PREDICTIONS.md` frozen, sha256
   `95f9371b030b8df64b4842a5df7be695d9e7f1b2311a300e78d915a701c16474`,
   committed alone before any Challenge 2 code or proof.  The existing
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
session read nothing outside the write root, the seed, and the contract
sections the harness loads, but it is an instrument of the same kind as the
one that declared prior exposure.

## Results

Inscriptions `<a|>` and `<|a>`, supplied and retained after the close of
Challenge 1.  Receipt `receipts/challenge2.json`; full tables in `paper.md`
section 5.5.

| | reading U | reading O |
|---|---|---|
| what the caller's “retains” licenses | the admission of both wholes: the caller's history is a supply and an admission per whole, and the current state is its replay, two marks, placement `(0, 1)` under the declared convention (DEFINITION, the run's reading of the word; COMPUTED, the certified history replayed from genesis) | same |
| the caller's history under the Challenge 1 admission event | refused by name, under both conventions, by the moving-admission refusal (DEFINITION: the Challenge 1 declaration replayed) | same |
| policies of the declared two-member space that retain both wholes | exactly one, the declared occurrence identity (COMPUTED over the four policy-and-convention histories; the space and its exhaustiveness are DEFINITION, scoped to that space) | same |
| the price of retaining both wholes | one new admission event and the withdrawal of the repeated-label rule, paid by the run, not by the boundary and not by the caller (DEFINITION) | same, and identical to U's |
| what the two admissions add | exactly two holding judgments, `OnSide(0, 0)` and `OnSide(1, 1)`; 0 to 2 (PROVED which judgments hold; COMPUTED the counts) | the same two; 2 to 4, the name judgments unchanged (PROVED, DEFINITION for the instantiation) |
| retention of both marks | both judgments survive every later history of the Lean grammar (DEFINITION as an instantiation of the Challenge 1 induction, which is PROVED); probed by a further supply and a further admission (COMPUTED) | same |
| the Challenge 1 admission event on the retained regime | refused by name: the label names two marks (DEFINITION, new at this rung) | same |
| permitted automorphisms of the retained regime | exactly two: the identity, and the reflection with the mark exchange (COMPUTED over the unpruned search; the composite itself is DEFINITION, `rfl`, and its permission DEFINITION) | exactly one: the identity (COMPUTED) |
| the two retained wholes, internally separable (definition 33) | **no**: the non-identity automorphism carries mark 0 to mark 1, and no invariant mark form separates them (COMPUTED; what the composite carries is PROVED) | **yes**: no permitted automorphism carries one to the other, and both invariant mark forms separate them (COMPUTED; the raw separation PROVED) |
| mark forms invariant on the bounded domain | neither (COMPUTED census) | both (COMPUTED census) |
| which named side each mark lies on | not formulable: U admits no name | mark 0 on `near`, mark 1 on `far` (COMPUTED) |
| the two sides, internally separable | **no**: the same automorphism exchanges them (COMPUTED) | **yes**: none does (COMPUTED) |
| `sides_collapsed`, the Challenge 0 profile comparison | false, and not the internal fact: it reads internal identities a permitted renaming permutes (COMPUTED; definition 29) | false, and the names alone would make it so |
| the two marks on different sides (definition 35) | an internal fact: invariant over all 177 permitted images of the census to three marks, and it holds (COMPUTED; PROVED for the concrete regime) | same |
| the admission order of the two wholes | not internally available: the other order is isomorphic (COMPUTED; PROVED that the two raw regimes differ) | same |
| the shared visible mark | not internally available: a relabelled regime is unequal and isomorphic (COMPUTED) | same |
| the presentation convention | invisible up to a permitted renaming, as at Challenge 1 | now also invisible up to one: one class, reached by the mark exchange (COMPUTED) |
| initial datum, reading, and the event-follows relation | unchanged, and empty (DEFINITION for one event; PROVED for histories, by instantiation) | same |
| new judgment form needed | none | none |

Boundary dependence: the identity policy space, the refusal of the shared
policy, the price, supply inertia, the current-state rule, the invariance of
the datum and reading, and the empty event-follows relation do not require
the admitted boundary.  The two new judgments, the sides the marks are
retained on, the automorphisms, the separation, and the different-sides fact
require it and are not formulated after removing it.

What the challenge exercises, by the seed's list: supply (one `Supply` per
retained whole, the two equal as values); mention (the shared visible mark
is named by every event and is not an identity); admission (the caller's, at
last: one per whole, under the declared identity policy); current-state
designation (the replay of the caller's history, now holding two marks);
retention (the placement tuple carries both, and both judgments survive the
growth probe); observation (two new `OnSide` judgments); side (the presented
side of each whole, mapped by the declared convention); equality (structural
equality compares the labels, the isomorphism relation and the canonical key
forget them, and the difference is live at this rung).

**The seed's question, answered.**  Are the two wholes internally
distinguishable by the admitted boundary alone?  Under U, no; under O, yes,
by the two admitted names.  What that cost: the admitted boundary, paid at
the seed; its O reading, paid at genesis; and, under both readings, the
occurrence identity, paid by the run at this rung, without which the two
wholes are not two marks at all.  Who paid the new part: the run.  What the
boundary alone buys, under both readings: that the two marks do not share a
side.

## Predictions scored

| id | label | status | note |
|---|---|---|---|
| C1-X | NOT FORCED | **PARTIAL** | U half HIT.  O half PARTIAL: the names clause hits; the clause “the price is the O declaration paid at genesis, and nothing new is paid at Challenge 2” is **MISSED**, recorded next to its value here — its own falsifier, “under O a price beyond the names”, fired, the occurrence identity being a new declaration paid at this rung under both readings (`scores.C1-X.O_nothing_new_paid_clause_status`).  The frozen condition, two internal identities for the two wholes despite the shared visible mark, was met (`condition_status`).  The frozen file is untouched |
| C2-1 what “retains” licenses | NOT FORCED | HIT, DEFINITION-level | every clause is fixed by the run's reading of the word and by the declared convention and policy; not counted as content |
| C2-2 the shared mark refuses the Challenge 1 admission | FORCED | HIT, DEFINITION-level | four histories refused by name; the Challenge 1 declaration replayed, so by construction, although that declaration predates the question |
| C2-3 the identity policy is one declaration, and not free | NOT FORCED | HIT, DEFINITION-level | two policies, one retains both wholes, price one event plus one withdrawn rule, paid by the run, equal under both readings; declared by this rung, so by construction |
| C2-4 two judgments, and nothing else | FORCED | HIT | content: rests on `retained_onSide_true_iff` and its three companions, none by unfolding |
| C2-5 under U the marks are exchanged by a permitted automorphism | FORCED | HIT | content: automorphism counts 2 and 1 and the exchanging witness over the unpruned search; the invariance census |
| C2-6 under O the marks are separated, and by the names | FORCED | HIT | content: the single O automorphism, both invariant separating forms, the one-class convention computation |
| C2-7 what the boundary alone buys | FORCED | HIT | content: 177 images of the census, and the property holds at the retained regime |
| C2-8 the sides become interchangeable again under U | NOT FORCED | HIT | content: the side-exchanging automorphism and the order and label witnesses |
| C2-X | NOT FORCED | PENDING | scored by Challenge 3 |

Eight of eight scored predictions hit: five as content (C2-4 to C2-8) and
three by construction, DEFINITION-level and not counted (C2-1 to C2-3), by
the criterion Challenge 1 declared and this rung reuses unchanged.  The
counts are the receipt's `tally`, computed from the statuses and a declared
list, and the negative direction of every one is tested.

**A clean sweep is weak evidence, and is reported as such.**  The
predictions were written by an instrument that had already read the whole
tree — the seed, the plan, the manual, the paper, the ledger, both earlier
predictions files, both earlier statuses, the kernel, the Lean, and the
tests — and had reasoned the rung through before writing them.  The commit
order shows that they were frozen before the code, and nothing more.  The
informative number is the previous rung's extrapolation, C1-X, written
before this rung existed: it is PARTIAL, and its own falsifier named the
miss.

## Advisories carried from the review of Challenge 1

The rule this rung applied: an advisory is **actioned** when the repair lies
in a living document of this rung or in apparatus; an advisory that would
require regenerating the frozen Challenge 1 receipt, or editing the previous
rung's `STATUS.md`, is **carried** with its reason, because this session
closes one rung and does not reopen a closed one.

Actioned:

1. The definition-locator sentence placed definitions 20 to 27 in the Python
   modules while 27 and 28 were marked Lean.  Rewritten, naming the Lean-only
   pair and the Challenge 2 additions.
2. B1-ONE-JUDGMENT's clause “a supply adds no holding judgment” carried no
   status and no theorem.  It now carries DEFINITION with
   `supply_preserves_holds`, which is `rfl`.
3. Section 9's continuation-reflection sentence was not scoped to the Lean
   grammar.  It is now, with the Python kernel's tested bound beside it and
   the Python-only events named as outside both.
4. `admitted_candidates_unequal` and `side_names_distinct` are both
   constructor distinctness after unfolding, and the paper did not say what
   line it drew between them.  Section 7.1 now states the line — a closed
   statement closed by `decide` against a parametrised one needing a rewrite
   and a case split — says plainly that it is a labelling convention and not
   a difference in depth, and records that the stricter reading would move
   `admitted_candidates_unequal` without moving C1-5.  Not relabelled: that
   would regenerate the Challenge 1 receipt for a label, and the paper
   records the alternative instead.
5. “Internal fact” was identified with “permitted-renaming-invariant
   separating judgment” by an evidence column, and under U that made the
   “no” tautological.  It is now definition 29, and the Challenge 1 table row
   says outright that the U “no” follows at once from the definition and that
   the content is the antecedent — that the two candidates are related by a
   permitted renaming — not the implication.
6. “Carried without a second tower” under O now says that the transported
   facts are the side-exchanged facts of the first class, because under O the
   reflection moves placements and not names.
7. The `oneMarkRelated` docstring asserted adequacy flatly; it now says the
   adequacy is prose and not a theorem of the file.
8. The Challenge 1 candidate-space cross-check was named for an unpruned
   enumeration it does not perform; renamed, with a comment saying what it
   does and that no minimality claim rests on it.
9. The `Regime` definition never disclosed that a mark's internal identity is
   its position in the admission order.  Definition 3 now states it,
   classifies the assignment, ties it to definition 13's permitted mark
   permutations, and points at this rung's computed result that the retention
   order is carried away by a permitted renaming; definition 1 separates the
   datum's identity number from the mark index, which share a numeral and
   nothing else.
10. Two relations were both called structural equality.  Section 1 now
    declares that Python `Regime` equality compares the labels and the Lean
    one has none to compare, that the Lean regime is the Python regime with
    tokens forgotten, and that the difference is live at this rung; the
    receipt reports it (`readings.*.label`).
11. Section 1 and the receipt attributed the moving-admission refusal to
    certifying `replay`.  Section 1 now says it is raised by low-level `step`
    and surfaced by `replay`.  The Challenge 1 receipt's clause fact keeps
    the older phrase; see the carried list.
12. The prediction tally had negative tests and no injection row.  The
    injection was performed at this rung and is a row in `MANUAL.md`.
13. “Fifty-six theorems, every one with a `#print axioms` report” was a
    totality claim with no check behind it.  `verify_lean.py` now enumerates
    the declared theorems and requires a report line for each; proved by
    injection, with the counterfactual observed on the same tree.
14. The injection record presented a retired test name as code, and the
    citation gate could not see it.  Both are repaired: the population now
    reads every `test_*` token anywhere inside a backtick span, and the three
    rows it then named give those names in plain text.  **The suggested
    widening was adapted**: taken literally it also fires on the tree's
    citations of its own test *files*, several of which are in documents this
    rung must not edit, so a token followed by `.py` is skipped as a file
    name, with a test fixing that direction.
15. The Lean names `challenge1History` and `admitted` carried the withdrawn
    framing.  Their docstrings are repaired and now say plainly that these
    are the candidate history and the candidate regime and that Challenge 1
    admits nothing.  **The names themselves are carried**; see below.

Carried, with reasons:

16. `challenge1History` and `admitted` keep their names.  Renaming them would
    leave fifteen theorem names built on the old framing (`admitted_eq`,
    `admitted_onSide_true_iff`, and the rest) either inconsistent with the
    definition or renamed too, and those names are cited by the committed
    axiom log, the claim ledger, and a frozen receipt.  The docstrings and
    the paper carry the correction instead.  A rename is a candidate for a
    dedicated repair session.
17. `c1_2_facts` requires `mark_judgment_retained_after_growth`, a probe the
    frozen C1-2 text does not name, so a future failure of that probe would
    score C1-2 MISSED on a clause outside the frozen words.  Not actioned:
    the repair is in the Challenge 1 scorer and would regenerate that rung's
    receipt.  It cannot change the current status, which the reviewer also
    observed.
18. `designation_clause_status` is decided partly by `selection_is_by`, a
    string the receipt builder writes, so that conjunct cannot fail on a real
    run.  Same reason, same file.
19. C0-X's O clause is scored on its falsifier's wording rather than on the
    clause as written, with no second reading recorded — the treatment the
    rung refuses for C1-2 and C1-4.  Same reason, same file.
20. `challenge1/STATUS.md` line 68 still labels “the other convention's
    candidate is the reflection of the convention's candidate” PROVED, where
    the fifth repair relabelled it DEFINITION everywhere else.  Not actioned:
    the previous rung's status is frozen for this session.  The label is
    correct in B1-CONVENTION-O, in the paper's 5.1 and 7.2, and in this
    rung's own prose, so no live claim rests on the stale one.
21. `challenge1/STATUS.md` line 60 uses “distinct” for profile difference
    while the seed uses it for the two-ness of the sides.  Not actioned, same
    reason.  This rung's prose says “the profiles differ” and reserves
    “distinct” for the seed's sense; the paper's section 5.5 row for
    `sides_collapsed` says outright that the profile comparison is not the
    internal fact.

## Where the run reached for a remembered result (declared reading 0)

- **The identity move itself was remembered in shape.**  That the second
  whole with the same visible mark needs its own internal identity, and that
  the fix is to stop keying admitted marks by their presentation token, is
  the shape this instrument would reach for from habit.  What was derived
  here: that the Challenge 1 kernel refuses the caller's history *by name*
  rather than absorbing it; that the declared policy space has exactly two
  members and why; and the price, in one new event and one withdrawn rule.
  The refusal was observed by running it, not assumed.
- **The automorphism notion of separability** — two things are separated
  when no symmetry of the state carries one to the other — is standard
  mathematics the instrument knows, and it is not derived here.  It is
  declared as definition 33 and used; what is derived is that the retained
  regime has exactly two permitted automorphisms under U and one under O,
  and which mark forms are invariant.
- **Nothing in the results was remembered.**  That the U side-symmetry
  returns at two marks, that the one non-identity U automorphism performs
  both exchanges at once, and that the O convention stops changing the
  isomorphism class at two marks were all computed first and then written
  down; the last two surprised the session.
- The Lean file's shape — a concrete regime, evaluations at it, a transport
  theorem — follows the Challenge 1 file's, which the session read.
- The audit-totality gate is apparatus, and its shape (enumerate the
  population independently, require each member to resolve, fail in both
  directions) is the repository contract's and the previous rung's, not this
  run's derivation; the reviewer proposed it and the run adopted it.  Its
  comment-stripping and the counterfactual are this rung's.

## Leftovers, for Challenge 3 and later

- Score C2-X: whether Challenge 3 declares definition 33's sense, whether it
  finds the O requirement already met, and whether more than one tied
  minimum survives under U.
- Challenge 3 requires `<a|>` and `<|a>` to be internally separable in a
  precisely declared sense.  The current regime already satisfies definition
  33's sense under O and fails it under U.  Challenge 3 must declare its own
  sense before looking, price the declaration that already satisfies it under
  O, and — under U — enumerate every non-isomorphic minimum one-step
  augmentation over a declared candidate space with declared cost measures,
  count every undeclared capability each uses, and retain all tied minima.
- Under U no augmentation that only adds a judgment to the closed grammar can
  separate the two marks, because the permitted automorphism transports every
  judgment.  That is an argument, not yet a theorem, and Challenge 3 should
  either prove it or refuse to lean on it.
- The occurrence identity and the withdrawn repeated-label rule are inherited
  by every later rung.  The token-keyed `AdmitMark` survives with its
  Challenge 1 meaning and now refuses a repeated label by name; a later rung
  that wants it back on such a regime must say what it means there.
- The reader is still bounded to one bar and at most one mark per whole.
  Challenge 4 supplies `<a|b>` and `<b|a>`, two marks in one whole, and must
  extend that bound deliberately; Challenge 5 supplies a nested whole and must
  revisit it again.
- Lean does not close the automorphism counts, only the composite and the two
  non-fixings.  A Lean statement that the permitted renamings of a two-mark
  regime are exactly those listed is a candidate target, not attempted.
- Challenge 0 and Challenge 1 leftovers survive: no Lean statement of the
  equal-count law or the class-count closed forms; no unbounded canonical-key
  theorem; the freeze manifest protocol remains OPEN.
- The four carried advisories above (17 to 21) are open work for a dedicated
  Challenge 1 repair session, not for Challenge 3.

## Repairs and live failures during the rung

- The Challenge 1 negative test asserting that a repeated admitted label is
  refused failed, as intended, the moment the rule was withdrawn: the case
  moved to a positive test of the new rule.  Row in `MANUAL.md`.
- `verify_lean.py` crashed with a `UnicodeEncodeError` instead of reporting a
  real `lake build` failure, because its failure printer wrote Lake's
  non-ASCII progress marks to a console that could not encode them.  Repaired
  and recorded.
- The first Lean draft did not compile: `decide` was offered a goal with a
  free variable, and four Challenge 1 lemmas were unreachable because the new
  module imported only `Basic`.  Both fixed before any log was regenerated.
- The widened citation population named three unresolved names on its first
  run, all in `MANUAL.md`; all three rows now give the names in plain text.
- Every gate this rung added or touched has an injection row in `MANUAL.md`,
  and no receipt or log was regenerated while any injection was live.

## Gates run in this session

| gate | result |
|---|---|
| `verify_pins.py` | `pins ok: seed ba30bcd600d8 and 3 frozen prediction file(s)` |
| `unittest discover -s tests` | `Ran 165 tests`, OK |
| `mypy` (strict, tree pyproject) | `Success: no issues found in 21 source files` |
| `coverage` + `check_coverage.py` | `line 100.00% branch 100.00% over 6 files` |
| `run_challenge0.py`, `run_challenge1.py`, `run_challenge2.py` | `unchanged: receipts\challenge0.json (5553 bytes)`; `unchanged: receipts\challenge1.json (28363 bytes)`; `unchanged: receipts\challenge2.json (35499 bytes)` |
| `verify_lean.py` | `lean ok: 84 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; the log was regenerated deliberately once, 56 to 84, with no injection live |
| `ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, 130 files with pinned hits, 1826 hits, census matches its pin`; no pin regenerated |
| `tests/test_primitive_contact.py` | firewall passes |
| `ci/check_paper_citations.py` | `paper cross-references resolve: 62 citation(s) across 29 document(s)` |
| injections | nine rows in `MANUAL.md`, including the audit-totality gate with its counterfactual |

## Next session

Open Challenge 3 fresh: read the handoff, the seed, `PLAN.md`, `MANUAL.md`,
and this file; write and commit `challenge3/PREDICTIONS.md` with its own
extrapolation before any code; score C2-X.

The state Challenge 3 inherits.  Under each reading the current regime is
the replay of the caller's history
`[Supply(a), AdmitOccurrence(a, 0), Supply(a), AdmitOccurrence(a, 1)]`: two
marks, placement `(0, 1)`, labels `("a", "a")`, one on each side of the one
admitted boundary under the declared convention `left is side 0`.  A mark's
internal identity is its admission index; the label beside it is
presentation and need not be unique.  Two holding judgments under U, four
under O.  Under U the regime has two permitted automorphisms and the
non-identity one exchanges both the marks and the sides; under O only the
identity, and the two marks are separated by the names, mark 0 on `near`.
The order of the two retentions, the shared visible mark, and the choice of
convention are all carried away by a permitted renaming.

Challenge 3 requires those two wholes to be internally separable in a
precisely declared sense.  Declare the sense first and in the predictions;
prove whether the current regime satisfies it under each reading; if it
does, name the declaration that made it so and price that declaration in
capabilities; if it does not, enumerate every non-isomorphic minimum
one-step augmentation over a declared finite candidate space with declared
cost measures, count every undeclared capability each candidate uses, refuse
any candidate called one-step that bundles capabilities, and retain every
tied minimum unless uniqueness is proved.  Do not assume one augmentation is
forced, and do not assume the boundary makes the requirement trivial: under
O it is already met and the price was paid at genesis, which is itself a
result to state rather than a reason to skip the enumeration under U.
