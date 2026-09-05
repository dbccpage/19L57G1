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
  `STATUS.md` was not read.  Only one commit was therefore in play at
  launch, not two.
- **Pull request 133 merged while this rung was being built**, at
  `9b9bea87f0ed3b3bd5be8145b837f91cbaeb3d4d`.  No pinned source moved: it added
  `research/second_stream/` and appended to the two shared files, and every
  blob and span this rung pins still hashes to its recorded value at the
  snapshot AND at HEAD.  So there is no repin, and the snapshot stays where
  it was; a repin is a logged act and there was nothing to repin.  What it
  did produce is the trivial conflict the packet anticipated on the two
  append-only files, resolved by KEEPING BOTH, rung one's block first
  because it landed first.  `main` was merged into this branch to resolve
  it; this branch was NOT rebased onto anything, and its base is `main`.
- One consequence is recorded because it changed a gate.  The write-root
  scan originally measured this branch against the PIN SNAPSHOT, which was
  correct until `main` moved: from the snapshot, rung one's whole tree now
  reads as though this branch had written it.  The scan now measures
  against the tip of `main` this branch has merged.  The snapshot remains
  the base for the PINS, where it belongs; it was never the right base for
  "what did this branch write".
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
  reproduced verbatim under a blob pin -- seven from the sealed kernel, ten
  from the pinned one-sided stake -- and FOUR of those seventeen carry a
  span pin as well.  Six spans are recorded on the sibling's
  `Commitment.lean`, but two of them pin a `structure` and a `def` rather
  than theorems, so the count of SPAN-PINNED THEOREMS is four, not six.  An
  earlier draft said "six of them", taking "seventeen theorems" as the
  antecedent; that was wrong and is WITHDRAWN.
  Scope: the pins prove that the sources did not move.
  `test_reconstruction.py` mechanically compares 49 normalized declarations
  shared with those sources.  Safety of the exact pinned omitted population
  remains reader-checked.
- **LABEL_SOURCE_ASSEMBLY_PROVED** (DEFINITION assembly, under
  the frozen target name `no_first_demand`).  In the
  sealed grammar reconstructed here, extended by a declared two-sided
  stake, and in no other grammar: a demand is at a pair the stake labels;
  it depends on the stake only through that pair's label; every event is
  one of the six recorded kinds; a supply changes no demand; and the free
  stake carries none anywhere.  **Scope, stated plainly: all five conjuncts
  are at the level of a definition.**  See the FW-DEF census below.  The
  theorem is true and its scope discipline is clean, and what it shows is
  that the definitions were chosen well -- which is a design claim, not a
  mathematical result.  It proves no statement about a first occurrence in
  an arbitrary run: non-inert events can make a demand appear, and that
  index remains leftover L-2.
- **DEMANDS_PROPAGATE_PROVED** (PROVED_THEOREM).  With a stake declared,
  growth generates, in both label directions, over the sealed regime; the
  apart form is also proved with its collapse hypothesis discharged rather
  than assumed.  Scope: one growth step, this grammar, these definitions.
- **AT_MOST_ONE_PROVED** (PROVED_THEOREM).  Under the stake labelling every
  distinct pair apart, from a regime carrying no demand, at most one held
  datum has the empty profile, and one growth step leaves the grown regime
  carrying at most one demand ALTOGETHER.  NO well-formedness is required
  and none is taken; an earlier version of this terminal said "well-formed
  regime", naming a hypothesis none of the four at-most-one theorems
  carries, and that wording is WITHDRAWN.  The route that avoids the
  sibling's false lemma also avoids needing well-formedness.  Scope: the sealed
  regime.  The sibling two-sided tree records the corresponding statement
  over ITS OWN carrier as a conjecture with no Lean; this is not a proof of
  that row, and that row stands as the sibling wrote it.
- **THREE_KINDS_DEMAND_INERT** (DEFINITION assembly, unpredicted).  Three of the
  six sealed event kinds leave every demand of every stake unchanged: the
  supply, the imposition, and the admission of a judgment form, the last at
  a well-formed regime.  Scope: this grammar.  The other three kinds are
  not claimed inert.  The unpredicted content is NF-22, classed THIN; this
  three-kind assembly adds nothing beyond its inputs.
- **INERT_RUN_CARRIES_NO_FIRST_DEMAND** (THIN direct corollary, unpredicted).
  From a well-formed base carrying no demand, no regime reached by a RUN of
  inert events carries one.  The PROVED_THEOREM carrying the content is
  `demands_replay_inert` (NF-32a).  Scope: runs whose every event is inert.
  A general first-demand index over arbitrary runs is leftover L-2.
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
| N-12 | HIT | `apart_at_most_one_new_demand` proves the fresh-datum-pair bound; the separate NF-32e theorem proves the total bound |
| N-13 | HIT | 0 free-stake demands anywhere in the rectangle |
| N-14 | HIT | 0 demands at a free pair; 0 totality mismatches |
| N-15 | HIT | first demand and first dishonoured labelled pair coincide, all seven stakes, both readings |
| N-16 | **MISSED** | **three** inert kinds, not two: `AdmitForm`, `Impose`, `Supply` |
| N-17 | HIT | at most one empty profile; at most one new demand; at most one demand altogether after growth; 4000 growth steps generating exactly one |
| N-18 | HIT | the one-sided total commitment's stake and the all-apart stake agree at every regime |
| N-19 | HIT | receipt byte-identical; both enumerators reach the same 118 and 276 regimes |
| N-X | PENDING | scored by the operator packet's rung four, the removal grammar |

Nineteen predictions scored: eighteen HIT, one MISSED.  N-X is not among
them: it is PENDING by construction, scored by the operator packet's rung
four and by no earlier one.  Twenty rows, therefore, and nineteen scored.
Plus four census misses recorded above against the FW-DEF half of N-3,
N-5 and N-6.  An earlier draft of this paragraph read *"Nineteen scored:
seventeen HIT, one MISSED, one PENDING"*; it undercounted the hits by one
and counted a prediction this rung does not score.  WITHDRAWN, and quoted
here rather than deleted.

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
5. **The axiom census was hand-maintained.**  `verify_lean.py` now derives a
   recursive module-path population and asks the Lean compiler for declaration
   names, module origins, source ranges, and axiom sets.  It requires exact
   equality among that environment census, fresh reports, the FW-DEF census,
   and the committed receipt.
6. **The reconstructions are now checked, not only pinned.**  The reading
   observed that the pins prove only that the sources did not move.
   `test_reconstruction.py` closes the shared-declaration half: 49
   declarations across four sources, all identical at the snapshot.
7. **A finding worth recording on its own.**  The sibling two-sided tree's
   conjecture sketch routes through "a fresh datum has the empty profile".
   Over the SEALED carrier that is false whenever the rule set is
   non-empty: `fresh_profile` shows the fresh datum is derivable in exactly
   the contexts whose form carries a uniform rule.  This rung's proof does
   not use that route; it goes through collapse transitivity and the
   restriction from the grown regime.  The sibling's row is not edited.

## Gate injections and exact-head repair probes

A gate is proved by failing on the exact defect it exists to catch, with
the failure naming the injected object, and by recovering when the
injection is reversed.  Fifteen were run against the original rung's gates.
The exact-head repair adds executable adversarial probes for the defects
found in review; both sets are recorded below and appended to the injection
table of `research/second/MANUAL.md`.

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
| reconstruction faithfulness, binder | `collapsed`'s second binder renamed from `d'` to `dd` in `Kernel.lean` | `AssertionError: "def collapsed (r : Regime) (d d' : Nat) ..." != 'def collapsed (r : Regime) (d dd : Nat) ...'`; exit 1, then 0 after reversal |
| reconstruction faithfulness, hypothesis | `collapsed_of_no_insts`'s hypothesis weakened from `r.insts = []` to `r.insts = r.insts` | `AssertionError: Lists differ: ['lean4/Derivation/Inertia.lean -> Kernel.lean: collapsed_of_no_insts'] != []`; exit 1, then 0 |
| FW-OB1 exemption pin | the exempted line reworded | `test_an_exempted_line_loses_its_exemption_when_reworded`: the appended-to line's digest is not in the pinned list, so the exemption lapses |
| first-demand claim scope | two datum admissions from the empty history under the all-apart stake | `test_two_datum_admissions_witness_a_later_first_demand` records `index = 2` and `kind = AdmitDatum`.  The declaration supplies the label; the second admission triggers its first demand.  This is a counterexample to the withdrawn causal-source sentence, not a new general theorem |
| reconstruction declaration population | found live: the former parser split at an attributed declaration but then rejected its header, and ignored anonymous instances | the parser regression sees both syntactic shapes; the 49 shared declarations include three anonymous instances, while the attributed `insertNew_nil` declaration belongs to the exact pinned omitted population |
| coverage source, schema, arithmetic, and freshness | synthetic unlisted and nested modules; an unknown `test_`-prefixed module; impossible counters; absent branch metadata; zero populations; detailed line/branch arrays inconsistent with summaries; inconsistent totals; a future timestamp; and a supplied 99 percent beside true 94 percent line coverage | `test_coverage_gate.py` raises by each injected defect; the gate pins the test-file population, reconciles detailed arrays and aggregate counters, rejects future-dated evidence, and computes line and branch ratios rather than trusting supplied percentages |
| fail-closed file and scope scans | unreadable, non-UTF-8, NUL, non-UTF-8 path, failed `git ls-files`, failed `git diff`, missing base, plus an untracked worktree path | `ScannerFailureTests` names every unavailable input and verifies the census reads index plus untracked files while the scope diff compares the base to the current worktree |
| Lean fresh-build and declaration census | private and attributed forbidden-declaration source shapes; quoted and Unicode theorem names; nested, root, and report modules; duplicate module basenames and declaration leaf keys; a disallowed compiler-reported axiom; and `lake clean` returning 7 | `LeanVerifierTests` exercises each fail-closed parser or compiler-census path, compares module origins and reports, applies the whitelist before regeneration, and records stage `clean` without attempting `lake build` |
| workflow registration | each required rung-two command, ordering constraint, scalar style, working directory, or unconditional-job condition changed in an in-memory copy | `WorkflowRegistrationTests` requires the exact grouped execution: pins, strict replay and discovered-test census, coverage check, receipt diff, strict typing, and the clean Lean verifier |
| vacuity guard of the write-root scan, REAL CASE (found live, not injected) | none -- `main` at `7d2e6e86` | `AssertionError: False is not true : the comparison base sees no change in research/second_nofirst`, exit 1. On `main` the comparison base IS HEAD, so the change set is empty because this rung had already landed, and the guard asserted through the one situation where an empty diff is the right answer. The same checkout with the repaired file: `skipped 'HEAD is the comparison base (7d2e6e86b809); no branch is under test'`, exit 0, and the whole suite OK. Both states observed on one tree minutes apart. A red gate reporting nothing wrong is the failure the register exists to prevent, and it was committed by the guard against it |

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

The original fifteen injections have exact commands, outputs, and recoveries
in the rung's session log.  The repair defects are covered by the named
executable adversarial tests above; this table does not claim a separate
manual mutation session for each of them.

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

The pre-repair record called the same suite both 109 tests and 115 tests.
Those two census claims contradicted each other and are WITHDRAWN; none of
their historical timings is reused as evidence for the repaired suite.  The
fresh repaired census is **180 tests**: the coverage replay completed them in
664.712 seconds and the replay, coverage gate, and receipt comparison together
took 675.120 seconds.  The separate pin verifier took 3.320 seconds, strict
typing 1.977 seconds, and the clean Lean/compiler/axiom audit 48.558 seconds.
Their grouped measured time was 728.975 seconds, inside the fifteen-minute
per-rung ceiling.

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
- **L-6, the faithfulness of the reconstructions.  NARROWED, not open.**
  An earlier draft of this list read: *"The pins prove the sources did not
  move.  Whether the reconstruction says the same thing is read by hand.
  Price: a mechanical declaration-by-declaration differ, which would be a
  gate rather than a rung."*  That gate was then written, so the sentence
  is WITHDRAWN and quoted here rather than deleted.
  `test_reconstruction.py` compares every declaration the reconstruction
  shares with its source, read by git blob AT THE SNAPSHOT, with comments
  and namespace lines stripped and whitespace normalized: 49 shared
  declarations across four sources, all identical, including three anonymous
  instances.  The parser has an adversarial attributed-syntax regression, but
  the attributed `insertNew_nil` declaration is in the exact omitted
  population.  Two injections show
  the comparison catches a renamed binder and a weakened hypothesis.
  What remains open is narrower and stays named: whether the declarations
  the reconstruction OMITS are safe to omit.  The gate pins the exact omitted
  names and checks that none of them is mentioned by the reconstruction;
  that they are not NEEDED is still read by hand.  Price: small.

## The next rung, named so it cannot be smuggled in later

By the seed's rule -- the smallest named leftover that either reduces the
count of declared inputs or extends the census of Challenge 5, and on a tie
the one named first -- after both tracks land the next rung is **L-2, the
first-demand index over an arbitrary run**, because it extends the census
row for succession and is named before L-3.  If the parallel track's result
reduces the declared-input count, its leftovers rank ahead of L-2 by the
same rule, and the choice is made when both tracks are on `main`.  Nothing
of either is started here.
