# second_nofirst: rung two, track one -- no first demand

`AuthorityEffect: None`.  This rung records and proves; it certifies
nothing beyond what its own verifiers, receipts, and Lean build show.
Every count below is dated 2026-09-04.

Challenge: read the sealed estate's first standing obstruction the other
way.  The question is `PROMPT.md`, frozen by hash before anything else in
this rung was written; the predictions are `PREDICTIONS.md`, frozen before
the first computation and before the first Lean build; the computed values
are `receipts/nofirst.json`, which regenerates byte-identically; the
proofs are in `lean/`, with the axiom log committed at
`receipts/lean_axioms.txt` and checked against a fresh build.

## Snapshot and the parallel track

- Pinned at `3f44571240a0830a2fa8de639281670f4e50a511`, which was `main` at
  launch.  Pull request 133 had NOT merged, so `research/second_stream/` is
  recorded ABSENT at this snapshot in `SOURCE_MANIFEST.json` and its
  `STATUS.md` was not read.  Only one commit is therefore in play, not two.
- The seed's next-rung rule had a tie between this rung and Challenge 2 of
  the seed.  The author resolved the tie by running both in parallel.  This
  track is the one named in its own prompt: no first demand.  **The
  parallel track, write root `research/second_stake/`, owns Challenge 2**,
  and nothing here answers it, weakens it, or strengthens it.
- FW-COUNT: this rung makes no claim about the count of declared inputs in
  either direction.  `receipts/nofirst.json` records
  `input_count_claim: none`.
- Rung one's pending extrapolation on the four-item bound belongs to
  neither track.  Four items are not computed here.
- FW-LEAD: not applicable, no bet supplied.  The `[OUTSIDE BET]` slot of
  the operator packet read `none` at launch, so this run scores only its
  own frozen predictions.

## Declared readings

1. **The source policy is RECONSTRUCTION, declared before the first
   compile.**  The sealed kernel slice and the pinned one-sided stake are
   reproduced verbatim in `lean/SecondNoFirst/Kernel.lean` and
   `lean/SecondNoFirst/Inherited.lean`, each with a pin note, and nothing
   sealed and no sibling package is imported.  The alternative the prompt
   allowed -- declaring an interface and discharging it -- was not taken.
2. **A disagreement between this prompt and the seed, recorded.**  The
   seed's section eight says each rung's Lean package consumes "the sealed
   package as a pinned dependency, as the sibling research trees do", while
   this rung's prompt forbids importing sealed modules.  The two are
   reconciled by the seed's own qualifier: the sibling trees do NOT depend
   on the sealed Lake package, they reconstruct their slice under a pin, as
   `research/standing_commitment/` does.  The seed wins, and what the seed
   points at is reconstruction.  The literal words differ, so the tension
   is recorded rather than smoothed over.
3. **A second disagreement, recorded.**  The seed's `PLAN.md` numbers
   Challenge 2 as rung two.  This track is also called rung two by its own
   prompt.  Both are rung two; they are two tracks of it, run in parallel
   by the author's decision, with disjoint write roots.
4. **The obstruction is cited by pin in `PROMPT.md`, not reproduced
   there.**  The sealed sentence contains a bracketed section reference
   bearing digits, and `PROMPT.md` spells every number out; reproducing it
   there would have edited a sentence that is never edited.  The verbatim
   quotation lives in `CLAIM_LEDGER.md`, where no such rule applies, and
   `test_forbidden.py` checks it against the pinned span byte for byte.
5. **Three carriers are kept apart** (FW-SCOPE): the sealed regime, on
   which `Demand` is a proposition; the represented state of the pinned
   one-sided tree, on which `demandsW` is a list; and the pinned one-sided
   `demands`.  `reconstruction_matches` bridges the second to the third and
   bridges NEITHER to the first.  That missing bridge is leftover L-1.
6. **`grammar_carries_no_stake` is named wider than it is stated.**  It
   proves case completeness, boundedness of the kind code, and injectivity
   of that code.  It does NOT prove that no constructor carries a field of
   stake type: that is a fact about the SIGNATURE of the reconstructed
   `Event` type and of `stepE`, which reads `Regime -> Event -> Option
   Regime`.  A signature fact is checked by the compiler accepting the
   declaration, not by a proposition, and it is recorded in the ledger as
   metatheory read off the type.

## Terminals, each with its scope

- **INHERITANCE_RECONSTRUCTED** (RECONSTRUCTION).  Seventeen theorems are
  reproduced verbatim under a blob pin, six of them additionally under span
  pins: seven from the sealed kernel, ten from the pinned one-sided stake.
  Scope: the reconstruction is faithful only as far as a reader checks; the
  pins prove that the sources did not move and nothing more.
- **NO_FIRST_DEMAND_PROVED** (PROVED_THEOREM, as an assembly).  In the
  sealed grammar reconstructed here, extended by a declared two-sided
  stake, and in no other grammar: a demand is at a pair the stake labels;
  it depends on the stake only through that pair's label; every event is
  one of the six recorded kinds; a supply changes no demand; and the free
  stake carries none anywhere.  **Scope, stated plainly: all five conjuncts
  are at the level of a definition.**  See the FW-DEF census below.  The
  theorem is true and its scope discipline is clean, and what it shows is
  that the definitions were chosen well -- which is a design claim, not a
  mathematical result.
- **DEMANDS_PROPAGATE_PROVED** (PROVED_THEOREM).  With a stake declared,
  growth generates, in both label directions, over the sealed regime; the
  apart form is also proved with its collapse hypothesis discharged rather
  than assumed.  Scope: one growth step, this grammar, these definitions.
- **AT_MOST_ONE_PROVED** (PROVED_THEOREM).  Under the stake labelling every
  distinct pair apart, from a well-formed regime carrying no demand, at
  most one held datum has the empty profile, and one growth step leaves the
  grown regime carrying at most one demand ALTOGETHER.  Scope: the sealed
  regime.  The sibling two-sided tree records the corresponding statement
  over ITS OWN carrier as a conjecture with no Lean; this is not a proof of
  that row, and that row stands as the sibling wrote it.
- **THREE_KINDS_DEMAND_INERT** (PROVED_THEOREM, unpredicted).  Three of the
  six sealed event kinds leave every demand of every stake unchanged: the
  supply, the imposition, and the admission of a judgment form, the last at
  a well-formed regime.  Scope: this grammar.  The other three kinds are
  not claimed inert.
- **INERT_RUN_CARRIES_NO_FIRST_DEMAND** (PROVED_THEOREM, unpredicted).
  From a well-formed base carrying no demand, no regime reached by a RUN of
  inert events carries one.  Scope: runs whose every event is inert.  A
  general first-demand index over arbitrary runs is leftover L-2.
- **CROSSCHECK_WRITTEN** (FINITE_COMPUTATION).  The declared rectangle,
  unpruned, from both sealed genesis readings.  Reading L: 3928 sequences
  reaching 523 distinct regimes, 1540 of them demand-free under the
  all-apart stake.  Reading F: 14293 sequences reaching 1718 distinct
  regimes, 4368 demand-free.  Across both readings 4000 growth steps
  generate exactly one demand, so the at-most-one bound is not vacuous.
  Scope: sequences of at most four events over the declared alphabet.
- **REGISTER_WRITTEN**, **OB1_UNCHANGED**.  The sealed sentence is quoted
  verbatim in `CLAIM_LEDGER.md` against its pinned span, and
  `test_forbidden.py` scans this whole write root for any sentence
  reporting it as discharged, narrowed, or superseded, finding none.

## The FW-DEF census, total

`FWDEF_CENSUS.json` classifies **every one of the 75 theorems** of the
package, and `test_census.py` checks that it is total in both directions,
that the two reconstruction modules are classed as such and no other module
is, and that nothing classed definitional has a long proof.

| class | count | what it means |
|---|---|---|
| RECONSTRUCTION | 17 | not this rung's work; reproduced verbatim under a pin |
| DEFINITION | 24 | true by unfolding, by `rfl`, by a projection, by one rewrite, or by pure case exhaustion; never counted as content |
| THIN | 8 | one genuine step, or a direct corollary of a neighbour |
| CONTENT | 26 | everything else |

Of this rung's own 58 theorems, **24 are at the level of a definition and
8 are one-step**, leaving 26 that carry content.  The headline
conjunction `no_first_demand` is among the 24.

**Why this census is total and the frozen one was not.**  `PREDICTIONS.md`
named seventeen targets.  An adversarial reading of the package before it
was committed, run as five independent lenses with a refutation pass, found
that the package carries far more theorems than that and that the
omissions were disproportionately the trivia -- so the frozen census
flattered the run.  The frozen census is not edited; this total one is
added beside it, and the misses are scored against the frozen text below.

### Census misses, scored against the frozen text

Of the five targets `PREDICTIONS.md` predicted to be at the level of a
definition, five are.  Of the thirteen it predicted NOT to be, **four are**:

| target | predicted | recorded | why |
|---|---|---|---|
| `supply_preserves_demands` | not definitional | DEFINITION | two rewrites; the content is carried entirely by the reconstructed sealed `supply_no_op`, which is itself `rfl` |
| `demand_depends_only_on_the_label` | not definitional | DEFINITION | `unfold` then one rewrite.  The STATEMENT is load-bearing; the PROOF is an unfolding, and FW-DEF classes by proof |
| `grammar_carries_no_stake` | not definitional | DEFINITION | pure case exhaustion over six constructors plus a decidable injectivity check; no mathematical step |
| `no_first_demand` | not definitional | DEFINITION | an assembly of the four above and `free_stake_no_demand`, all definitional |

Four census misses out of thirteen.  Recorded next to their values and not
edited.

## Predictions scored

Scored mechanically by `run_nofirst.py` for the computational predictions,
and against `FWDEF_CENSUS.json` and the committed axiom log for the Lean
ones.

| id | verdict | value or note |
|---|---|---|
| N-1 | HIT | the three named are at the level of a definition and are labelled so |
| N-2 | HIT | `reconstruction_matches` PROVED, no side hypothesis |
| N-3 | HIT as to PROVED; **census MISS** as to the FW-DEF label | proved via the reconstructed sealed theorem |
| N-4 | HIT | `demand_needs_label` at the level of a definition |
| N-5 | HIT as to PROVED; **census MISS** as to the label | six kinds, matching the rung-zero census's six |
| N-6 | HIT as to PROVED; **census MISS** as to the label | one conjunction, five conjuncts, each proved separately |
| N-7 | HIT | both directions proved |
| N-8 | HIT | both label directions proved |
| N-9 | HIT | `growth_generates_apart_of_no_insts` discharges the hypothesis |
| N-10 | HIT | `fresh_profile` proved; the reviewer's counterexample confirms `r.wf` is needed |
| N-11 | HIT | `apart_at_most_one` proved over the sealed regime |
| N-12 | HIT | `apart_at_most_one_new_demand` proved, and strengthened to a total bound |
| N-13 | HIT | 0 free-stake demands anywhere in the rectangle |
| N-14 | HIT | 0 demands at a free pair; 0 totality mismatches |
| N-15 | HIT | first demand and first dishonoured labelled pair coincide, all seven stakes, both readings |
| N-16 | **MISSED** | **three** inert kinds, not two: `AdmitForm`, `Impose`, `Supply` |
| N-17 | HIT | at most one empty profile; at most one new demand; at most one demand altogether after growth; 4000 growth steps generating exactly one |
| N-18 | HIT | the one-sided total commitment's stake and the all-apart stake agree at every regime |
| N-19 | HIT | receipt byte-identical; both enumerators reach the same 118 and 276 regimes |
| N-X | PENDING | scored by the operator packet's rung four, the removal grammar |

Nineteen scored: seventeen HIT, one MISSED, one PENDING; plus four census
misses recorded above against the FW-DEF half of N-3, N-5 and N-6.

**What the miss produced.**  N-16 said two kinds are demand-inert; the
rectangle found three.  The third is the admission of a judgment form,
which is inert because a fresh form carries no instance and no uniform
rule, so no profile moves.  That is now the proved theorem
`admitForm_preserves_demands`, written after the miss and labelled
unpredicted throughout `lean/SecondNoFirst/Inert.lean`.  A miss is a
finding, not a defect, and this one is the most useful result of the stage.

## What the adversarial reading changed, before anything was committed

Five independent lenses read the package and a refutation pass ran over
every objection.  The reading is testimony, not evidence; what it produced
that IS evidence is listed here, and each item is in the committed tree.

1. **The FW-DEF census was made total** (24 of this rung's 58 theorems at
   the level of a definition, 8 one-step), with `test_census.py` checking
   totality.  The frozen partial census stands unedited beside it.
2. **`apart_at_most_one_new_demand`'s doc claimed a total bound its
   statement did not carry.**  The statement was STRENGTHENED to match the
   doc rather than the doc weakened to match the statement:
   `apart_at_most_one_demand_after_growth` now bounds the demands of the
   grown regime altogether, old pairs included, via `apart_no_old_demand`.
3. **Nothing in the package mentioned a run.**  Every theorem of stages two
   and three was about a single regime, so the word "first" in the headline
   was discharged only by the stage-four rectangle.
   `lean/SecondNoFirst/Run.lean` is the repair: the three inert kinds
   compose along a history, so under an inert run no demand is ever first.
4. **`grammar_carries_no_stake` was named wider than it was stated.**  The
   doc comment was narrowed to say exactly what is proved and what is a
   signature fact; see declared reading six.
5. **The axiom census was hand-maintained.**  `verify_lean.py` now derives
   the module list from the filesystem and each module's namespace from its
   own `namespace` lines, so a new module cannot be forgotten.
6. **A finding worth recording on its own.**  The sibling two-sided tree's
   conjecture sketch routes through "a fresh datum has the empty profile".
   Over the SEALED carrier that is false whenever the rule set is
   non-empty: `fresh_profile` shows the fresh datum is derivable in exactly
   the contexts whose form carries a uniform rule.  This rung's proof does
   not use that route; it goes through collapse transitivity and the
   restriction from the grown regime.  The sibling's row is not edited.

## Injections: every gate this rung adds, proved by failing

A gate is proved by failing on the exact defect it exists to catch, with
the failure naming the injected object, and by recovering when the
injection is reversed.  These rows are appended to the injection table of
`research/second/MANUAL.md`.

| gate | injection | observed failure, verbatim |
|---|---|---|
| pin verifier, source blob | first hex digit of the pinned `lean4/Derivation/Inertia.lean` hash changed | `FAIL: hash mismatch at the snapshot for lean4/Derivation/Inertia.lean: expected 062615CB..., got C62615CB...`; exit 1, then 0 after reversal |
| pin verifier, span | first hex digit of the `paper/paper.md` span hash changed | `FAIL: span mismatch at the snapshot for paper/paper.md:488-494: expected 0fb9e4e0..., got bfb9e4e0...`; exit 1, then 0 |
| pin verifier, frozen text | first hex digit of the `PROMPT.md` hash changed | `FAIL: frozen text moved: research/second_nofirst/PROMPT.md: expected 013f38a2..., got e13f38a2...`; exit 1, then 0 |
| Lean axiom whitelist | `theorem zzz_probe_choice (P : Prop) : P or not P := Classical.em P` added to `Stake.lean`, and its report line added to `AxiomReport.lean` | `FAIL: SecondNoFirst.Stake.zzz_probe_choice depends on disallowed axioms ['Classical.choice']`; exit 1, then `lean audit clean: 10 sources, 75 axiom reports` and exit 0 |
| Lean committed log | the `fresh_profile` line deleted from `receipts/lean_axioms.txt` | `FAIL: fresh build has a report the committed log does not: SecondNoFirst.Propagate.fresh_profile :: Quot.sound propext`; exit 1, then 0 |
| Lean census derivation | `theorem zzz_probe_unlisted` added to `Stake.lean` with the report NOT regenerated | `FAIL: SecondNoFirst.Stake.zzz_probe_unlisted is declared in Stake.lean but not listed in AxiomReport.lean`; exit 1, then 0 |
| coverage gate, floor | the floor raised from ninety-five to ninety-nine point nine | `FAIL: line coverage 98.66% is below 100%; branch coverage 95.28% is below 100%`; exit 1, then 0 |
| coverage gate, set drift | `verify_pins.py` removed from the declared measured set | `FAIL: verify_pins.py is in the report but is neither declared measured nor declared excluded`; exit 1, then 0 |
| coverage gate, staleness | `nofirst.py` touched after the report was written | `FAIL: nofirst.py was modified after the report was written (2026-09-04T11:37:03.162241); regenerate coverage.json`; exit 1, then 0 after regenerating |
| census totality | the `fresh_profile` row deleted from `FWDEF_CENSUS.json` | `test_the_census_is_total_in_both_directions` failed, the lists differing by that name; exit 1, then 0 |
| census classification | `wf_step_inert` refiled from CONTENT to DEFINITION | `AssertionError: Lists differ: ['grammar_carries_no_stake (22 lines)', 'wf_step_inert (27 lines)'] != []`; exit 1, then 0 |
| prose census over the write root | one line carrying a watched noun appended to `STATUS.md` | `AssertionError: Lists differ: ['research/second_nofirst/STATUS.md:333: <term>'] != []`, where `<term>` was the watched noun itself; exit 1, then 0.  The noun is REDACTED here: writing the failure text verbatim would put the watched term into this tree and fail the same gate, which is the defect the root repository records against its own gate's test file |
| FW-OB1 scan | a sentence appended to `STATUS.md` asserting that this rung had discharged the sealed obstruction, worded so as to match the first barred shape.  The sentence is REDACTED here for the same reason as the watched noun above | the scan named `research/second_nofirst/STATUS.md:333` and the pattern `(?:clos\|answer\|supersed\|narrow)...obstruction`; exit 1, then 0 |
| FW-OB1 exemption pin | the exempted line reworded | `test_an_exempted_line_loses_its_exemption_when_reworded`: the appended-to line's digest is not in the pinned list, so the exemption lapses |

**One injection changed the tree rather than only proving a gate.**  The
census classification probe was run BEFORE the census exception list
existed, and it exposed a conflict inside this rung's own apparatus:
`grammar_carries_no_stake` is classed at the level of a definition but its
proof is twenty-two lines, over the declared bound.  Length is the wrong
instrument for a proof whose length counts constructors.  The response was
to except that one theorem BY NAME in `FWDEF_CENSUS.json`, with its reason,
and to require the exception list to stay at or below two entries -- not to
raise the bound, which would have excused everything silently.  Recorded
here because the probe found a real defect in the gate as first written,
and a reader comparing revisions would otherwise see only the exception.

The exact commands, outputs and recoveries are in the run log of this
rung's session; each was observed before this tree was committed.

## Commands and gate time

From the repository root:

```text
python research/second_nofirst/verify_pins.py
python research/second_nofirst/run_nofirst.py       # about forty seconds
python research/second_nofirst/verify_lean.py       # needs elan
```

From this directory:

```text
python -m unittest discover -s . -p "test_*.py"
python -m mypy
python -m coverage run -m unittest discover -s . -p "test_*.py"
python -m coverage json -q -o coverage.json
python check_coverage.py
```

Coverage on 2026-09-04, measured from inside the rung over the declared
measured set: line 98.67% (519 of 526) and branch 95.33% (204 of 214),
both above the floor of 95%.
`check_coverage.py` excludes itself and `verify_lean.py`, each with its
reason recorded in that file.

Gate time on 2026-09-04: 491 seconds of wall time, measured end to end,
for the pin verifier, the run, the Lean build and audit, the 109 tests,
strict typing, the coverage measurement and its gate, the repository's
prose census and the identifier firewall together -- inside the fifteen
minutes the seed allows.  The tests are the bulk of it, at about 150
seconds; the Lean build is about 30.

## Leftovers, named and priced, executed nowhere

- **L-1, the carrier bridge.**  `reconstruction_matches` joins the
  represented state to the pinned one-sided demands and joins neither to
  the sealed regime.  A Lean statement of the two-sided demands over the
  sealed regime BY IMPORT rather than by reconstruction would need the
  estate to permit importing the sealed package, which it does not.  Price:
  one rung, and an amendment to the seal that is the author's act, not an
  agent's.
- **L-2, the first-demand index over an arbitrary run.**  `Run.lean` proves
  no demand is ever first under a run of INERT events.  The other three
  kinds do change demand sets, so locating the first demand of a general
  run needs an index over histories.  Price: a moderate rung; the
  definitions are in place and the induction shape is the one `Run.lean`
  already uses.
- **L-3, a discharged variant of `growth_generates_same`.**  The apart form
  has one, from "no admitted instance".  The same form still carries its
  separability hypothesis, and no regime inhabiting it is exhibited in
  Lean.  Price: small.
- **L-4, the removal grammar and X's scoring.**  The operator packet's rung
  four declares it; `PREDICTIONS.md` N-X is frozen for it with its scoring
  rule and its falsifier.  Not started here.
- **L-5, Challenge 2, the stake read off the state.**  The parallel track's
  question, named here so it cannot be smuggled in later.  Not answered
  here in any direction.
- **L-6, the faithfulness of the reconstructions.**  The pins prove the
  sources did not move.  Whether the reconstruction says the same thing is
  read by hand.  Price: a mechanical declaration-by-declaration differ,
  which would be a gate rather than a rung.

## The next rung, named so it cannot be smuggled in later

By the seed's rule -- the smallest named leftover that either reduces the
count of declared inputs or extends the census of Challenge 5, and on a tie
the one named first -- after both tracks land the next rung is **L-2, the
first-demand index over an arbitrary run**, because it extends the census
row for succession and is named before L-3.  If the parallel track's result
reduces the declared-input count, its leftovers rank ahead of L-2 by the
same rule, and the choice is made when both tracks are on `main`.  Nothing
of either is started here.
