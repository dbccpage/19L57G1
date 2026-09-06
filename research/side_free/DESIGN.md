# The side-free control: design

Frozen before any code of this tree existed.  This file and `PREDICTIONS.md`
are committed alone, ahead of the build, and are never edited afterwards.
Their sha256 values are pinned in `verify_pins.py` in the build commit, so a
later edit fails the tree's own verifier rather than passing quietly.

Nothing in this file is an object-language input.  Every notion introduced
here carries a source classification in section 1, and the words *forced*,
*minimal*, *free*, *canonical*, *equivalent*, *universal* and *complete* are
used only inside a stated scope.

## 0. What this tree is a control for, and what it is not

A prior derivation on an unmerged branch admits one primitive: a whole with
two sides.  A regime there is a reading, the admitted marks, and a placement
assigning each mark to a side; the placement is the only structure the
carrier has, and its isomorphism key keeps the reading and the placement and
nothing else.  At its fourth rung that derivation imposes a requirement —
that two retained marks be internally separable — and reports what meeting it
costs.  Its own claims about which of its results depend on the admitted
primitive are a hand-written dictionary in one of its runner modules, which
its own ledger files as a limitation computed by nothing and read by no test.

That is the hole this tree fills.  It builds a carrier identical to that one
in every respect except that it has no placement, no sides, and no admitted
whole with two of them, and it prices the same requirement there.  The
difference between the two prices, if any, is what the admitted primitive
bought.  If the difference is zero, it bought nothing in price.

**Two things this tree is not.**  It is not a claim that the prior derivation
is wrong; it is the measurement that derivation could not take from inside
itself.  And it is not one rung wider than one rung: it says nothing about
what the admitted primitive bought at earlier rungs, and nothing about
whether the requirement was the right one to impose.

**How the prior tree is named here.**  It is not named.  Its path appears in
exactly three files of this tree — `SOURCE_MANIFEST.json`,
`pinned/BOUNDARY_PIN.json`, and `pinned/QUOTATIONS.md` — and this tree's own
source-isolation scan bars it everywhere else, along with the name of every
other sibling tree.  Everywhere else, including this file, it is *the pinned
receipt*, *the pinned carrier*, or *the pinned tree*.  The single carve is
declared in section 10 and enforced by a test.

**One rename against the judged design, recorded.**  The judged design named
the runner `run_control.py` and its output `receipts/control.json`.  The
caller's battery names `run_side_free.py`; this tree uses `run_side_free.py`
and `receipts/side_free.json` throughout, and the judged names appear nowhere.
Nothing else about the runner changes.

**One correction to the judged design's arithmetic, recorded.**  The judged
design says the control's requirement text is the pinned text "with the four
bytes ` under a reading` deleted".  That phrase is sixteen bytes, not four.
The deletion is the phrase, and the gate asserts the phrase; the byte count in
the judged prose was wrong and is not carried forward.

## 1. Classification ledger

Every notion this tree introduces carries exactly one of the twelve labels.

**Metatheory apparatus.**  The deletion rule and its closure; the reader of a
presented whole and the presented position; the generic enumerator; every
census; every gate; the pin; the endowment ledger; the deletion register; the
route table; the injection record.

**Supplied datum.**  The one opaque whole and the refusal that fixes it; the
two inscriptions the caller presents.

**Imposed challenge.**  The requirement and its second reading, inherited from
the pinned receipt by a declared textual deletion and by nothing else.

**Admitted primitive.**  NONE.  This tree admits nothing.  That is the whole
point of it, and it is what makes the comparison a control rather than a
second derivation.

**Derived definition.**  The side-free carrier and its events; the three
declared coordinates; `mu1`; `mu2`; `mu2_restricted`; the class key; the
`Admitted` judgment form; the forgetting map.

**Proved theorem.**  The forgetful lemma and its corollary, in Lean, over the
two declared carriers without a finite bound; the inertness of the
presentation event; that state changes only by an admission event; that
replay is deterministic.  The Python census is the bounded cross-check of the
lemma, not its proof.

**Deterministic computation.**  Every row value, every minimum, every class
count, every census fraction, every endowment row, and every field of the
decided object.

**Countermodel.**  The mirror carrier.  It is this tree's own re-declaration
of a side-typed carrier, used only as the domain over which the forgetful
lemma and the censuses are stated.  It is never claimed to be the pinned
carrier; it is pinned against the pinned receipt's published vector, and a
divergence voids the run rather than adjusting it.

**Optional realization.**  None.

**Conjecture.**  None.

**Open obstruction.**  (a) Whether the admission order is itself a container.
(b) The price of re-purchasing a per-mark two-valued datum, which lies
outside the pinned candidate space and is therefore priced in neither world.

**Refuted claim.**  The pinned clause asserting that *every* separation result
of that rung requires the admitted primitive — refuted within the scope of
this declared carrier, this three-coordinate space, and this eight-point
enumeration, and nowhere wider.

**DEFINITION-level, never counted as content.**  That withdrawing the mark
permutations satisfies the requirement.  With no permitted renaming that moves
an index, no renaming carries one mark to another, so the requirement holds by
unfolding.  This tree computes the fact rather than asserting it, reports it
as definition-level in the same object as the headline, and freezes both the
primary answer that counts it and the secondary answer that excludes it.

## 2. The pin

`pinned/boundary_challenge3.json` is the vendored blob of the pinned receipt
at commit `5c43c5ee`.  Four values fix it, each recomputable from the bytes
alone:

* sha256 `e4904075aaa07dd05a2f9d0cba313e77b6eb965a44efecb5cff51864f70a64ab`
* git blob id `dbb4cce3cdd49d15d0784c2a73bf7afeab9de7a0`
* length 220518 bytes
* no CR byte anywhere, and committed `-text`

`pinned/BOUNDARY_PIN.json` carries those four values, the provenance command
that produced the blob, the collapse map `{extra_mark_0 -> extra_mark,
extra_mark_1 -> extra_mark}`, and every number this tree extracts from the
receipt together with the JSON path it was read from.  `SOURCE_MANIFEST.json`
records every file of the pinned tree this design was matched against, by path
and by the sha256 of its blob at `5c43c5ee`.

A third check is conditional and must never be silent: `verify_pins.py`
compares the vendored bytes against `5c43c5ee` through `git show` and reports
either PASS or SKIPPED with the reason.  `5c43c5ee` is on an unmerged branch
and is not an ancestor of `main`; the manifest says so, and says that the pin
is to be re-taken when that work merges.  **Residual, recorded and not
closed:** the link from the vendored bytes to that commit is only as strong as
that branch's reachability in the clone doing the checking.

**Never read the pinned tree from this worktree.**  The branch is unmerged and
the path in this worktree holds an older state.  Every read is
`git show 5c43c5ee:<path>`.

## 3. The carrier

`code/sidefree/model.py`.

```
@dataclass(frozen=True)
class OpaqueDatum:      internal_id: int
INITIAL_DATUM = OpaqueDatum(0)

@dataclass(frozen=True)
class Regime:           marks: tuple[str, ...]
                        initial_datum: OpaqueDatum = INITIAL_DATUM
```

`__post_init__` keeps exactly one refusal from the pinned carrier: the initial
datum is fixed.  `n_marks()` is `len(marks)`.  `genesis()` is `Regime(())`.

One variable field.  A mark's internal identity is its index in `marks`, which
is the order in which it was admitted; the entry beside it is the presentation
**label**, which may repeat.  This is the pinned carrier's own Challenge 2
declaration with the placement's index space replaced by the marks' own, which
is legitimate because the pinned validator forced the two tuples to have equal
length at every valid regime, so the index space is the same set.

**Events**, the pinned grammar with the side argument removed:

* `Supply(token)` — external presentation.  `step` returns the regime
  unchanged.  It is not an admission.
* `AdmitMark(token)` — label-keyed admission.  A no-op when the label already
  names exactly one mark; refused **by name**, verbatim from the pinned text
  with the side clause removed, when the label names more than one.
* `AdmitOccurrence(token)` — admits one presented occurrence as a fresh mark
  whatever labels are present.  This is the pinned declared policy.

`replay(history, base)` refuses an admission whose token was not supplied
first, by name.  `certify(history, base, claimed)` is `replay(...) == claimed`.
`event_follows(r, e)` is `False`: no event is entailed by admitted state.

**A refusal is removed and recorded, not absorbed.**  The pinned carrier
refuses an admission that would move an already-admitted mark to the other
side.  That refusal has no side-free statement at all: with no sides there is
nowhere to move a mark to.  It is entered in `DELETED.md` as a *removed
refusal*, and its computed consequence is reported in section 9 rather than
left as prose.

**Keys.**  `serialize(r) = (r.n_marks(),)`.  `serialize_keeping_labels(r) =
(r.marks,)`.  Labels are forgotten unless a candidate withdraws the
forgetting.  `rename_marks(r, pi)` is the pinned function with its placement
line removed.

**The flagged family.**  `permitted_images_under(r, mark_permutations)` and,
built on it, `automorphisms_under`, `mark_automorphism_to_under`,
`marks_separable_under`, `is_isomorphic_under`, `canonical_under` and
`mark_orbit_under`.  Two flags where the pinned carrier has three; the
serializer is handed in as a declared flag and is never chosen by judgment;
every enumeration is unpruned.

## 4. The presentation layer, kept

`code/sidefree/presentation.py`.

The presentation layer is **kept**, and the deletion falls on the convention
instead.  The pinned tree declares the presented position to be a fact of the
presentation and the map from it to an admitted side to be a convention
declared in the metatheory and not derived from the inscription.  The
convention's codomain is gone, so the convention goes; the presented position
is metatheory in the pinned world too, so keeping it costs the control nothing
and gives it nothing, while preserving the caller's two inscriptions as two
distinct facts of presentation.  Deleting the reader as well would have
collapsed the caller's two inscriptions into one identical history, which is a
loss with no compensating gain.

`Whole(token, presented_position)` with positions `before` and `after`.
`read_whole` keeps the one-bar, at-most-one-mark bound and every refusal by
name.  `supply_event` and `admission_event` build events and apply nothing.
No function of this module reaches the carrier's state.

## 5. Observation grammar

One positive judgment form, `Admitted(mark)`, holding exactly when
`0 <= mark < n_marks()`.

This is the honest residue rather than an empty grammar, and the pinned source
is what makes it honest: the pinned `observation_holds` for the side judgment
is literally the conjunction of `mark < n_marks()` and
`placement[mark] == side`, so the disjunction of the two side judgments is
already derivable there and holds exactly when the mark is admitted.
`Admitted` is that conjunct with the side clause removed — not less, and not
more.  Its extension is empty at genesis.

Because it is a residue and not a gift, it can be **proved inert**: a test
requires that `Admitted` separates the two retained marks at no cell of the
control's census.  An empty grammar could only have been absent.

Judgment counts holding at genesis are reported for all three carrier
columns: control 0, unnamed reading 0, named reading 2.  The named reading's
two are **unmatchable** and are reported as such.  A container exists before
its contents; an order does not.

## 6. The requirement, shown rather than promised

`code/sidefree/requirement.py`.

The control's requirement is the pinned `requirement.declared` with the phrase
` under a reading` deleted — the pinned world has two readings and indexes the
requirement by them, and the control has one carrier and does not.  The
control's second reading is the pinned `requirement.second_reading` with the
phrase ` of the reading` deleted.  **Both deletions are asserted byte for byte
against the vendored receipt** by gate G2, which also runs a whole-word scan
proving that neither control string contains any of *side*, *sides*,
*boundary*, *placement*, *reflection*, *near*, *far*.

`RETAINED_MARKS = (0, 1)`.

**One shared verdict function**, used by both carriers and by the replay
against the pin:

```
def separates(automorphism_permutations, i, j) -> bool:
    return not any(pi[i] == j for pi in automorphism_permutations)
```

`marks_separable_under` in each carrier is *defined* as this function applied
to that carrier's own automorphism set — never a parallel implementation — and
a test pins that.

## 7. The candidate space

`code/sidefree/candidates.py`.

**The deletion criterion is mechanical.**  A pinned coordinate transfers
exactly when its pinned capability sentence contains no whole word *side* or
*sides*.  Applied to the pinned five this partitions with no borderline case:
`withdraw_reflection` and `admit_names` name sides and are dropped;
`withdraw_mark_permutations`, `keep_labels` and `extra_mark` do not and
transfer.  A test asserts that the mechanical partition equals the implemented
one, so the coordinate list cannot drift away from the criterion that produced
it.

The three surviving coordinates carry their pinned capability sentences
**byte-identical**, pinned by gate G3 against
`candidate_space.capability_of` in the vendored receipt.  Their names are
string-identical to the pinned names, so the cross-world join is by equality:
a rename fails the join **by name** rather than silently dropping a route.

```
COORDINATES = ("withdraw_mark_permutations", "keep_labels", "extra_mark")
extra_mark in (False, True)
```

Eight points: one base, three one-step, four bundles refused at `mu1 >= 2`.

**The one value-set change of the whole deletion**, flagged in the receipt
because it is the single place a second deletion could hide: `extra_mark`
collapses from `(None, 0, 1)` to `(False, True)`.  This is *read from the pin,
not asserted*: the receipt shows `extra_mark_0` and `extra_mark_1` carrying
the same class key and standing as the two members of one retained class, so
one control point against one pinned class is like for like.

`extra_mark` admits one further occurrence of the token the caller already
supplied, so it needs no new supply and costs exactly the one pinned
capability.  A never-supplied token is refused by name, and the refusal is
reported.

`changed_coordinates` tests each coordinate against its **own** inherited
value, keeping the pinned per-coordinate form even though `extra_mark` is now
boolean.  Dropping a repaired guard because the repair happens not to bite is
how the defect comes back.

**Scope, in the pinned world's own form.**  The enumeration is exhaustive over
these three declared coordinates and their declared values and nothing wider.
It does not enumerate an augmentation that changes the event grammar again,
that admits more than one further mark in one step, that supplies a datum the
caller never presented, that derives the permitted renamings instead of
declaring them, or that admits a new per-mark datum.  Every minimality
statement in this tree is scoped accordingly.

**The rejected coordinate, recorded because it is the first thing a critic
proposes.**  "Admit a per-mark two-valued datum" is rejected on three grounds.
It is an addition where the whole instrument is a deletion.  It lies outside
the pinned space, so allowing it would price a route the pinned world was
never charged for either.  And it answers a different question — the *price*
of rebuilding the admitted primitive rather than the *worth* of having it
free.  It is carried as open obstruction (b).

## 8. Cost measures

**`mu1`, inherited whole, and the deciding measure.**  "Capability count: the
number of undeclared capabilities the candidate uses", one per moved
coordinate.  It is comparable across the two worlds because the three
surviving coordinates carry the pinned capability sentences byte-identical and
the one-step and bundling rules are unchanged.  Deleting coordinates can only
*raise* the control's minimum, never lower it.

**`mu2`, per carrier, never differenced.**  Of the pinned five collateral
facts, two transfer verbatim — `order_internally_available` and
`label_internally_available` — and three have no side-free subject.  A raw
cross-world `mu2` difference would charge the pinned world one unit for
re-reporting the answer, because the pinned receipt itself computes that its
first collateral fact takes the requirement's value at every point of its
space.  **A test asserts that the receipt of this tree carries no cross-world
`mu2` difference field anywhere.**

**`mu2_restricted`, derived and comparable.**  Both worlds' second measure
recomputed over the two transferring facts only.  The pinned side is obtained
by a data join from the receipt's per-point `collateral_facts`, never by
importing pinned code.  It is labelled derived and is reported beside `mu1`,
never overriding it.

**The endowment ledger** is a computed report and not a fairness proof.  Six
rows across three carrier columns — the control, the unnamed reading, the
named reading — every row computed by the same code in each column:

1. declarations at genesis;
2. coordinates the genesis declaration fixes away from the carrier's inherited
   defaults;
3. judgment forms, with the count holding at genesis;
4. automorphism order at the retained regime, with the number of renaming
   generators;
5. mark properties that are both invariant and separating at base;
6. the collateral facts both worlds can state.

Rows that do not match are **named and priced, not smoothed**.  Two are known
in advance: the control has one renaming generator fewer, and the named
reading holds two judgments at genesis that the control cannot hold.

## 9. What else is computed and reported

* **Both identity policies replayed.**  Under the pinned *shared* policy the
  pinned world refuses the caller's second admission by name.  Side-free,
  `AdmitMark("a")` twice is admit-then-no-op and yields ONE mark, so the
  requirement has no subject and the retained-mark check raises by name.  This
  is reported as a **refusal of the subject** — never as a false, and never as
  a satisfied requirement.  Occurrence identity is therefore inherited already
  paid, exactly as the pinned world pays it one rung earlier, and the
  inheritance is visible rather than assumed.
* **The two caller histories** under the surviving presentation layer, and the
  computed value of `order_internally_available` **with its reason**: the two
  supplies carry the same token, so reversing them is not a change to notice.
  That is **not** "the order is unavailable".  The admission order still
  exists, it is the mark's internal identity, and it is what the whole result
  turns on.  Stating it wrongly would be the easiest overclaim in this tree.
* **The censuses.**  Two instruments, both declared here.
  * The *withdrawal census*: over a two-mark domain — for the mirror, the two
    declared labels in each of two positions, each reading, each `keep_labels`
    value, and each placement, giving 64 cells; for the control, the two
    labels in each of two positions and each `keep_labels` value, giving 8
    cells — the fraction of cells at which the two marks separate, taken once
    with the mark permutations kept and once with them withdrawn.
  * The *route census*: for each candidate, over that world's own two-mark
    configuration domain at that candidate's own flags, with the candidate's
    further mark appended when it declares one, the fraction of configurations
    at which the two retained marks separate.  This is the instrument the
    declared secondary computation uses.
* **The deletion register**, `DELETED.md`: a closure over the pinned source's
  own names, each entry with its reason — direct, or via which name — and a
  **test asserting totality**: no deleted name survives anywhere under
  `code/sidefree/`.

## 10. Gates, isolation, and CI

Registered by steps **appended** to the research job of
`.github/workflows/verify.yml`, after the existing steps, touching nothing
else, in the shape that job already uses: the pin verifier; then from inside
the tree, coverage erase, unittest discover, coverage json, the tree's own
dual 95% gate, the runner, and `git diff --exit-code -- receipts`; then strict
typing.

`lean/` stays a **manual receipt** and is recorded as a live residual, exactly
as the pinned tree records its own.  `verify_lean.py` builds the package from
clean, text-scans every `.lean` file for the forbidden tokens, requires every
module to lie in the root's import closure, requires every declared theorem to
carry a `#print axioms` line, requires every report to lie within
`{propext, Quot.sound}`, and compares the reports with the committed
`lean/axioms.txt`.  No CI job runs it.

**Source isolation, with exactly one carve.**  The tree carries its own scan:
no citation into a sealed path, no sealed claim identifier, no sealed Lean
name, no import of the sealed kernel, and no name of another research tree —
accumulated from history the way the pinned tree's own scan accumulates them,
so a sibling name that appeared between commits cannot evade it.  The one
carve is that the pinned tree's own name may appear in exactly three declared
paths: `SOURCE_MANIFEST.json`, `pinned/BOUNDARY_PIN.json`, and
`pinned/QUOTATIONS.md`.  Every other tree name stays barred everywhere,
including in those three.

**Gate 12 of the repository** — the prose watchlist — is run after every file
is added and its pin is **never** regenerated.  Its pins are per file, so even
the pinned tree's own vocabulary would produce a new hit in a new file.  Every
candidate noun is probed before adoption and reworded on any hit.

**Every gate this tree adds is proved by injection**, one row each in
`MANUAL.md`, with the mutation, the command, the diagnostic, the exit status
read **directly** and never after a pipe, and the recovery.  No receipt, axiom
log or pin is regenerated while an injection is live.

## 11. The decisive computation

One function, `sidefree.control.decide()`, returning one deterministic record
written to `receipts/side_free.json` by `run_side_free.py`.  If any gate fails
the record carries `VOID` and **no difference is reported**.

**Inputs.**  `P` the vendored pin; `E` the generic enumerator, which imports
neither carrier module by name; `Cf` the side-free carrier; `Cm` the mirror
side-typed carrier under readings `U` and `O`; `sep` the one shared verdict
function.

**Step 1 — gates.**  All must pass; each names its offender.

* **G1 `pin_bytes_ok`** — the four pin values, then the conditional check
  against `5c43c5ee`, reported PASS or SKIPPED-with-reason.
* **G2 `requirement_texts_match`** — the two textual deletions, byte for byte,
  plus the whole-word scan of the control strings.
* **G3 `capability_texts_match`** — the three surviving capability sentences,
  byte for byte against the receipt.
* **G4 `verdict_replay_agrees`** — *the decisive gate*.  For each reading, for
  the base row and each of the six one-step rows — fourteen rows in all — the
  control's own verdict function, applied to the pinned world's own recorded
  automorphism sets, must reproduce the pinned world's own recorded
  `satisfies` values.  Any disagreement means the translation is wrong and the
  run is VOID.  This gate uses no re-declaration of anything.
* **G5 `forgetful_lemma`** — *the smuggle tripwire*.  Over the full declared
  lemma census — marks labelled from the two declared labels at each of
  n = 1, 2, 3 positions, every placement in `{0,1}^n`, both readings, and each
  of the three flags `withdraw_reflection`, `mark_permutations`, `keep_labels`
  — for every side-typed automorphism `(reflected, pi)` of the mirror regime,
  `pi` must be an automorphism of the forgotten regime under the transferred
  flags.  Then the corollary at every cell of two or more marks: side-free
  separation implies side-typed separation.  Then non-vacuity: the count of
  cells where the side-typed world separates and the side-free does not must
  be greater than zero.  A violation names the reading, the labels, the
  placement, the flags and the offending automorphism.

  This is what makes the instrument fair *against* the pinned world rather
  than by argument.  Any structure the side-free carrier keeps beyond
  forgetting shrinks its automorphism set below the image of the side-typed
  one, and the lemma fails by name at a named cell.  Its corollary fixes the
  sign of the answer in advance: the pinned minimum is at most the side-free
  minimum, so a negative difference is unreachable, and a tie is the strongest
  statement available against the admitted primitive.  That is what "bought
  nothing" means here.

  The census iteration order is declared, so "the first violating cell" is
  determined: reading, then mark count ascending, then labels in the order the
  two declared labels are taken, then placement in ascending tuple order, then
  `withdraw_reflection`, then `mark_permutations`, then `keep_labels`, each
  false before true.
* **G6 `mirror_matches_the_pin`** — the mirror, enumerated by the same generic
  enumerator, must reproduce the pinned vector on all 48 point rows per
  reading: `satisfies`, `mu1`, `mu2`, `class_key`, `automorphism_count`,
  `effective_structure`, the minima with their class counts and members, the
  space size 48 and the refused-bundle count 41.  Any divergence VOIDS the run
  rather than adjusting it.

**Step 2 — enumerate, one code path, two carriers.**  `Rf = E(Cf)` over 8
points; `Ru = E(Cm, U)` and `Ro = E(Cm, O)` over 48 points each.  Every regime
in every row is the replay of an explicit history from genesis, and a test
asserts it, so no row rests on a mutation.

**Step 3 — minima, ties retained.**  Over the candidates that satisfy and are
base-or-one-step, the least value of the measure; the members at that value
quotiented by the class key; every tied class retained; unique only at one
class.

**Step 4 — the decided object.**

```
delta_vs_unnamed      = side_free_minimum - unnamed_minimum
delta_vs_named        = side_free_minimum - named_minimum
plurality_vs_unnamed  = side_free_classes - unnamed_classes   (never summed with the above)
routes_the_boundary_bought = (unnamed minimum members through the collapse map)
                             minus (side-free minimum members)
side_free_minimum_is_definition_level = the withdrawal row's COMPUTED
                             no_permitted_renaming_moves_an_index
what_the_admitted_primitive_bought in {
    VOID                    if any gate failed
    NO_SATISFYING_CANDIDATE if the side-free eligible satisfying set is empty
    NOTHING_IN_COST         if delta_vs_unnamed == 0
    COST_DIFFERENCE_<n>     if delta_vs_unnamed == n > 0
}
```

**Step 5 — reported beside, never deciding.**  The route table; the unmatched
pinned routes with their removal arguments; the endowment ledger; both
censuses; the deletion register; `mu2` per carrier with its non-comparability
declared **in the same object as the numbers**; `mu2_restricted` on both
sides; and the declared secondary computation, which repeats steps 3 and 4
with every candidate that satisfies at every route-census point excluded.  The
secondary is frozen in `PREDICTIONS.md` in advance, reported, and never
deciding — and both numbers are frozen precisely because the answer flips
between them.

## 12. Fairness hazards and their guards

| hazard | direction | guard |
|---|---|---|
| a substitute for the side handed to the control under another name | rigs against the pinned world | G5, run as a test over the full declared census, and proved by injecting the side back as a per-mark two-valued attribute |
| order or index quietly made free content | rigs against the pinned world | order is not free content: making the admission index internally available costs one capability, exactly as it does in the pinned world.  The base key is the arity alone, the poorest defensible key; both worlds get arity free, because the pinned key keeps a tuple whose length is the arity.  Backed by a key-choice invariance test that recomputes every reported value under `(n_marks,)` and under `()` and requires agreement.  **This choice errs against the control and is recorded as doing so.** |
| a re-purchase coordinate that lets the control buy the primitive back | rigs against the pinned world | refused by the inherited exhaustiveness scope; carried as open obstruction (b) |
| the control unable to STATE the requirement | rigs for the pinned world | G2 byte-for-byte plus the whole-word scan; then G4, which replays the control's verdict function against the pinned world's own recorded answers |
| the control crippled by starting with less | rigs for the pinned world | the endowment ledger with every mismatching row named; the observation grammar kept at its honest residue and proved inert; the presentation layer retained; occurrence identity inherited already paid; and `extra_mark` retained as a coordinate and allowed to FAIL, so its failure is computed rather than produced by deletion |
| prices drifting between the worlds | rigs for the pinned world | G3 byte-for-byte; names string-identical so the join is by equality; a rename fails by name |
| the vacuous route decides | either | the primary decision counts it, because excluding it in the control while it stands in the pinned world would itself be the rigging; the definition-level flag is COMPUTED and reported so the headline cannot be read as content; the route census is computed in both worlds by the same code; and a declared secondary excluding every everywhere-satisfying candidate is frozen in advance and reported beside |
| plurality misread as price | either | routes and price are separate columns, never summed; a test asserts no field combines them |
| `mu2` misread as a cross-world cost | either | a test asserts no cross-world `mu2` difference field exists anywhere in the receipt; only `mu2_restricted` appears in a cross-carrier difference |
| the pin itself | either | four values recomputable with no git at all, plus the conditional commit check reporting SKIPPED-with-reason rather than passing quietly |
| the mirror | either | labelled a countermodel-domain object, pinned against the whole published vector by G6, with a divergence voiding the run.  The load-bearing tie remains G4, which uses no re-declaration at all |

**Scope hazards, stated rather than guarded, because they cannot be closed
here.**  G4 covers the fourteen rows the minimum ranges over and is total over
what the minimum is computed *from*, but not over all 48 points per reading,
so a defect in a bundle row's `satisfies` is invisible to it.  The control is
one rung wide.  The pinned premise that a candidate's permitted renamings are
closed under composition and inverse is inherited as OPEN, and is not treated
as discharged by the renaming set having shrunk.  And whether the admission
order is itself a container is open obstruction (a).

## 13. The terminal sentence this tree may write, and its scope

Within the three declared coordinates, at the pinned requirement and prices,
at the retained two-mark configuration, under `mu1`: the admitted primitive
reduced the price of the required internal separation by ZERO under the
unnamed reading and by ONE under the named reading.  What it bought under the
unnamed reading is two additional routes at the same price, both mediated by
the sides.

The tie holds only because a route that satisfies the requirement without
reading anything is counted — a route the pinned tree itself retains and
itself records as OPEN.

**The residue, which this tree ends on rather than on the headline:** what
pays for separation in a world with no container is the ADMISSION ORDER, and
whether an order is itself a container is a further question this control does
not answer.  The tree may write "the admitted primitive bought no price that
the admission order could not buy at the same price".  It may not write "the
admitted primitive bought nothing".
