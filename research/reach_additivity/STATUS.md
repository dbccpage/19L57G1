# reach_additivity: additivity holds, and it buys the opposite of what was wanted

`AuthorityEffect: None.`

The preceding rung left as its second open whether a base-relative cost is
additive along composition, on the stated ground that additivity would give
the estate a price for a sequence of moves rather than a re-measurement.

It is additive. It is additive for a whole class of costs and not just the
one that was asked about, and the reason it is additive is the reason it is
useless for the thing the question was reaching toward.

> A cost of the form `P(apply(base, delta)) − P(base)` **telescopes**. Its
> total along a sequence of moves is the functional's value at the end minus
> its value at the start, so it cannot tell one route from another, and its
> total around any closed walk is **zero**. It therefore cannot witness a
> nonzero route discrepancy or circulation. This rung does not define or
> classify every possible obstruction.

And the counterweight, which is what actually settles the question: **the
sealed item count is additive along composition too.** So additivity does
not distinguish a base-relative cost from a base-free one, and was never the
property worth asking for.

## Frozen inputs

Native `PROMPT.md` sha256 `49b428e993546dbf4923dfc8ece0a72f8d22870f22635b985e0cfc654ab4710f`.
`PREDICTIONS.md` sha256 `c8d0d05297e5c88992058a8d6b1fffa327dfc8d4f2dd53044547a6a9f0370dfb`, frozen as one whole-file digest before any
module of this tree existed. The chronology section of `PREDICTIONS.md` records against
itself that the sealed implementation had been **read** before the
predictions were written, and names which three predictions are weaker for
it.

Sources pinned at snapshot `7fcd72f618e676a88df65efed4926ac3c11eacbe` of
`main`: five blobs and **three spans**. The spans are the load-bearing text:
the clause where datum admission absorbs a repeat, the clause where form
admission appends unconditionally, and the item-to-event translation. The
self-loop classification below turns entirely on those three, so they are
pinned rather than paraphrased.

**No reconstructions, and the preceding rung was not pinned at this run's
snapshot.** At `7fcd72f6`, `research/reach_measure` sat in an open pull
request, so it was not pinnable at any ancestor of this branch's original
head; stacking on it was prohibited. This tree consumed no file of it and
restated the shared two-line functional, as declared in
`SOURCE_MANIFEST.json`. Later integration does not retroactively change
that source boundary.

## Declared readings

1. **Composition is declared, not discovered.** The sealed candidate grammar
   declares no composition on responses. This tree declares one —
   concatenation of item sequences — and `FW-DECLARE` forbids calling it
   canonical or forced. A declaration that renumbered the second response's
   indices against the intermediate state is a *different* operation and
   would need its own run.
2. **The question is asked of a class, not of a cost.** A result about one
   hand-picked cost would be a result about the hand. Everything below is
   stated for an arbitrary state functional, and three are carried through
   the computation — total profile size, form count, datum count — so no
   finding can be an accident of the first one.
3. **The rectangle is depth two, and the depth is a finding.** At depth one
   the rectangle carries no standing instance and no standing rule, because
   the sealed genesis states declare no form and the one-item enumerator
   offers an instance only over a form that already exists. A depth-one
   rectangle therefore answers the closed-walk question **vacuously**, and
   `FW-VACUOUS` refuses a vacuous answer as a finding. Depth two: 44 bases.
   `test_depth_one_answers_the_question_vacuously` pins the reason.
4. **Absorbing and offered are different questions.** A repeat is absorbed
   at the *event* level; whether the *item* level ever presents one is
   separate, and the two come apart in both directions. Every count below
   says which level it is about.

## Terminals, each with its scope

- **SEQUENTIAL_ACTION_HOLDS** (PROVED_THEOREM and COMPUTATION).
  `actList_append`: applying a composite is applying the parts in order, for
  an arbitrary state, item type and one-item action. Over the rectangle,
  **66376 triples, 66376 agreeing** — and by the stronger equality: the
  composite's *event tuple* is literally the concatenation of the parts'
  event tuples in all 66376. That is why the two sides also agree on
  ill-formedness rather than merely on results, and it is checked directly
  rather than inferred.
- **Composition is not total, and that is what makes it substantive**
  (COMPUTATION). In **16514 of the 66376 triples** the second response is
  ill-formed at the original base — it references a form or a datum the
  first response introduced. So the agreement above is not a statement about
  independent responses that happened to be written next to each other.
- **ADDITIVITY_HOLDS** (PROVED_THEOREM and COMPUTATION). `diff_additive`:
  every difference cost is additive along composition, for an arbitrary
  functional, using no property of it — sequential action and one
  cancellation. Over the rectangle: 66376 checked, 0 non-additive, for each
  of the three functionals **and** for the sealed item count.
- **PATH_INDEPENDENT** (PROVED_THEOREM). `pathTotal_eq` telescopes the
  step-by-step total to the endpoints; `path_independent` follows;
  `circulation_zero` is the closed-walk case. The Python side computes the
  total step by step and never from the endpoints, so the telescoping is
  checked and not assumed.
- **CIRCULATION_WITNESS_FOUND** (COMPUTATION, scope: the rectangle).
  **18 of 44 bases carry an enumerated self-loop**, all of them instance
  repeats. Constructed probes find rule repeats at 4 bases as well. So the
  closed walk exists, `FW-VACUOUS` does not fire, and the circulation
  statement has subjects.
- **COUNT_IS_NOT_A_DIFFERENCE_COST** (PROVED_THEOREM).
  `Loop.count_is_not_a_difference`: no state functional has the item count
  as its difference, because the count is nonzero around a closed walk and
  every difference is zero there. A refutation, not a failure to find. The
  computed witness: at base `L0.1.3`, the paths `[datum]` and
  `[inst repeat, datum]` have the same endpoints; all three difference costs
  agree on them, the item count is 1 against 2.
- **The unsigned form is where the sign earns its keep** (PROVED_THEOREM
  and COUNTERMODEL). `natDiff_not_additive` exhibits a rise then a fall
  totalling one step by step and zero as a composite, because truncated
  subtraction eats the fall. `natDiff_additive_of_monotone` recovers
  additivity under an explicit monotonicity hypothesis. Over the rectangle
  no step cost of any of the three functionals is negative, so the two forms
  agree there — recorded, and not offered as a reason to drop the sign.
- **Axioms**: 14 `#print axioms` reports, 5 axiom-free, the rest within
  `{propext, Quot.sound}`.
- **OPEN_AT_NAMED_TARGET**: the leftovers below, each priced.
- **OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED**:
  this rung touches none of the protected opens. A cost algebra is not a
  demand generator, proves nothing about the two paper items, and says
  nothing about the growth question of the arithmetic chain.
- **MANUAL_RECEIPT_DECLARED**: no CI gate reads this tree's pins, its Lean
  audit, or its scans.

## The prediction record

| # | prediction | disposition |
|---|---|---|
| A1 | sequential action holds, by literal equality of event tuples, so the two sides agree on ill-formedness | **CONFIRMED** — 66376/66376 on both counts |
| A2 | additivity for every difference cost, over signed coefficients; the unsigned form needs monotonicity | **CONFIRMED** — `diff_additive`, `natDiff_not_additive`, `natDiff_additive_of_monotone` |
| A3 | path-independence by telescoping | **CONFIRMED** — `pathTotal_eq`, `path_independent`, and computed step by step |
| A4 | the item count is additive too, so additivity does not separate the costs; **the preceding rung's summary of this open is wrong** | **CONFIRMED, and the contradiction lands** — see below |
| A5 | four item kinds can self-loop: instance, rule, datum, requirement; form never | **PARTLY MISSED** — see below |
| A6 | the item count is not a difference cost | **CONFIRMED, and proved rather than exhibited** |
| A7 | a difference cost has zero circulation on every closed walk, so it cannot carry an obstruction | **PARTLY CONFIRMED, SCOPE NARROWED** — `circulation_zero` proves zero circulation; the broad obstruction classification was not defined or proved |
| A8 | no negative step cost over the rectangle | **CONFIRMED** — least step cost 0 for all three functionals |

### A4, and the correction it forces, by name

`FW-PRIOR` requires this to be recorded against the source rather than
quietly superseded. `research/reach_measure`'s `STATUS.md` says of this open:

> *If `reach(base, d ; e) = reach(base, d) + reach(apply(base, d), e)`, the
> measure is an action along a path of moves and a composite has a price
> rather than a re-measurement.*

**That inference does not hold, and this rung refutes it.** Additivity gives
a composite a price. It does not make the price informative, because the
sealed item count — the base-free measure that same rung proved blind — is
additive by the same token. What additivity actually implies, for a
difference cost, is telescoping, and telescoping is a *loss*: the price of a
route is fixed by its endpoints, so no route is ever worse than another.

The sentence in the preceding rung is left standing in its own tree, because
that tree is frozen and its wording is its own record. It is contradicted
here, by name, which is where the contradiction belongs.

### A5, the miss, with its value

Predicted: instance, rule, datum and requirement items can each self-loop.
Found:

| item kind | absorbs a repeat at the event level | is ever a self-loop at the item level | is ever enumerated as one |
|---|---|---|---|
| instance | yes | **yes** — 18 of 44 bases | **yes** |
| rule | yes | **yes** — 4 bases, by constructed probe | **no** — the enumerator subtracts standing rules |
| datum | yes | **no** | no |
| form | no | no | no |
| requirement | yes | **not an item at all** | no |

Two errors, each with a precise cause.

**The datum case.** Datum admission does absorb a repeat — the pinned span
shows the early return on a standing token. But the item level never
presents one: the item-to-event translation numbers a fresh datum from the
base's own datum count, so the token is new every time. **Absorption
downstream does not make a self-loop upstream**, and the prediction
conflated the two levels. `test_a_datum_item_is_never_a_self_loop` pins it.

**The requirement case.** A requirement is imposed by an event, not by a
candidate item; the item grammar has four constructors and none of them is a
requirement. The prediction named a thing that does not exist at the level
it was making a claim about.

The rule case is the interesting survivor: it self-loops and is never
offered. So a closed walk can exist in the state space and be unreachable
through the estate's own enumeration — which is why the table above reports
enumerated and constructed counts separately rather than merging them.

## What this rung settles, and what it does not

It settles that composition of responses is well behaved: the composite acts
as the parts in order, including on failure, and every difference cost is
additive along it. It settles that additivity is the wrong question —
necessary for a price along a path, satisfied by both costs on the table,
and therefore not evidence for either. It settles that the difference form
is a strong constraint with a cost: it forces path-independence and therefore
cannot witness a nonzero route discrepancy. It does not classify all
obstructions. And it settles, as a theorem, that the sealed item count is
not of that form.

It does **not** produce a cost that can carry an obstruction; it says what
such a cost cannot look like. It does not claim the declared composition is
the only one, and a renumbering composition is named below as untried. It
does not claim the rectangle is the states. It proves nothing about whether
any of these costs is a good cost, and no sentence here says one is.

## Inherited gates, adapted — recorded because adapting a gate is where a
gate goes to die

`verify_pins.py` and `verify_lean.py` came from a sibling tree, and three of
their checks encoded that tree's shape as a hard requirement. Each
adaptation is recorded with what it would have forced:

1. **`verify_lean.py` matched forbidden tokens as substrings.** Repaired to
   word boundaries, which is what the root gates use. This tree writes about
   *admission* on nearly every line, so the substring form would have been
   unusable here as well as wrong.
2. **`verify_lean.py` had no source census.** Added, with namespace
   tracking, so a theorem declared in `Additive.lean` and absent from
   `AxiomReport.lean` fails. The sibling's injection record shows that
   without it, deleting a report line is invisible — the line removes its
   own report.
3. **`verify_pins.py` required at least one source reconstruction.** Right
   for a tree that restates sealed material, wrong for one that restates
   none. Relaxed **only against a declared `reconstruction_policy`** of
   substantive length, so that a forgotten binding cannot pass as a
   deliberate absence.
4. **`verify_pins.py` required exactly two prediction freezes.** That tree
   froze in two stages; this one froze once, before anything ran. Requiring
   two would have forced a second stage that did not happen, which is the
   wrong direction to bend a receipt. Relaxed to one or more, with the
   single-freeze case checking the whole file.

## The injection record

| Gate | Injection | Observed failure |
|---|---|---|
| Pin integrity | first digit of the pinned `code/derivation/model.py` blob flipped | `FAIL: code/derivation/model.py blob at 7fcd72f6... is b6f95a67..., pinned c6f95a67...`, at the snapshot and at `HEAD`; exit 1, then 0 after reversal |
| Span pin, the absorbing clause | the datum-absorption span moved by one line | `FAIL: span code/derivation/model.py:112-114 at 7fcd72f6... hashes af7eaa77..., pinned e01802fd...`, at the snapshot and at `HEAD`; exit 1, then 0 after reversal |
| Prediction freeze | one word changed in `PREDICTIONS.md` (*below* to *above*) | `FAIL: PREDICTIONS.md hashes c4247043..., recorded c8d0d052...`; exit 1, then 0 after reversal |
| Lean forbidden token, word-boundary form | a comment carrying the first forbidden token appended to `Additive.lean` | `FAIL: Additive.lean contains forbidden token 'sorry'`; exit 1, then 0 after reversal |
| Axiom-report source census | the `circulation_zero` `#print axioms` line removed | `FAIL: ReachAdditivity.circulation_zero is declared in Additive.lean but not listed in AxiomReport.lean`; exit 1, then 0 after reversal. Without the census the injection is invisible, because the removed line removes its own report |
| Reconstruction policy gate | `reconstruction_policy` deleted from the manifest | `FAIL: no source reconstruction bindings recorded and no reconstruction_policy declared to say why`; exit 1, then 0 after reversal |
| Census scan (FW-PIN, FW-NAME) | a probe file carrying a watched noun placed in the write root | `Lists differ: ['probe_watched.md:1: <the watched noun>'] != []`; exit 1, then 0 after deletion. The token is elided here rather than quoted: the scan reads every file of the write root and cannot tell a quoted hit from a real one, so quoting the observed message verbatim failed this very gate on the next run |
| Receipt replay | the triple count changed from 66376 to 66377 in the committed receipt | `test_the_committed_receipt_replays_byte_for_byte` fails on the differing byte range; exit 1, then 0 after reversal |
| Self-loop classification | the datum self-loop test inverted to assert a datum item IS a self-loop | fails at the first base, naming the two regimes and the token `'w2'` the response added; exit 1, then 0 after reversal. The recorded miss is pinned and cannot quietly become true |

## Leftovers, named and priced, executed nowhere

1. **A cost that can carry a nonzero route discrepancy** — OPEN, and the rung
   this one points at. It must be additive along composition and **not** a
   difference of a state functional. The item count is the first example of
   a non-difference cost in this estate, and it is base-free, so it does not
   answer the declared target. Price: a base-relative, path-dependent price
   whose path total is not determined solely by its endpoints.
2. **The renumbering composition** — OPEN. Concatenation reads the second
   response's indices as written. A composition that renumbered them against
   the intermediate state is a different operation, and whether sequential
   action survives it is not known here. Price: a declared renumbering and
   the same survey.
3. **Relations among composites** — OPEN. Concatenation is free: no two
   distinct item sequences are ever the same move. Imposing relations needs
   a declared relation set and a proved congruence.
4. **Reachability of the rule self-loop** — OPEN. A rule repeat is a closed
   walk that the sealed enumerator never offers. Whether any closed walk the
   estate *does* offer has length greater than one is not decided here; only
   length-one instance repeats were found.
5. **Depth beyond two** — OPEN. The rectangle is reachability-bounded at
   two. Nothing here says a deeper rectangle behaves the same, and the
   sequential-action theorem is the only statement above that does not need
   it to.

## The registration diff this tree does NOT apply

    - name: reach_additivity pins, Lean audit and scans
      run: |
        python research/reach_additivity/verify_pins.py
        python research/reach_additivity/verify_lean.py
        python -m unittest discover -s research/reach_additivity -p "test_*.py"

## Commands (run from this directory unless noted)

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 5 sources and 3 spans at snapshot and HEAD; ... 0 source projections exact; native PROMPT.md frozen; 1 predictions freezes reconstructed` |
| `python verify_lean.py` | 0 | `lean audit clean: 4 sources, 14 axiom reports (5 axiom-free), axioms within ['Quot.sound', 'propext'], 14 originating theorems all listed` |
| `python run_additivity.py` | 0 | `sequential: 66376/66376 triples agree, 66376 event tuples identical` |
| `python -m unittest discover -s . -p "test_*.py"` | 0 | 26 tests, refusal scans and unit tests pass |
| `python -m mypy` | 0 | strict, no issues |
| `python ci/check_prose_watchlist.py` (repository root) | 0 | clean without a repin |
