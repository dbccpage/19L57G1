# UNFROZEN DRAFT -- the second derivation: report of the research stage

**UNFROZEN DRAFT, dated 2026-09-25.  The research stage is still running.**
Continuation attempt one (Challenge 3) was running when this draft was
written, and continuation attempt two (Challenge 4) had not begun.  This
paper is finalized only after both continuation attempts close and the
author approves the freeze.  Nothing here is a frozen result, and no
comparison has been written or may be written from it.

`AuthorityEffect: None`.  Companion files: `research/second/claim_ledger.md`
(one row per retained claim, cited below as `SD-...`) and
`research/second/change_log.md` (the dated history).

## 0. What this draft is

This is the report the seed's section nine asks for, written by the
closeout session the author designated on 2026-09-25 (`CLAUDE.md`, gate 11,
"Second-derivation continuation" and "Genesis closeout scope").  It
reports the original stage of the run: twelve research attempts under the
unchanged seed, carrying eleven ordinal labels, zero to ten, because rung
two ran as two separately scoped tracks.  Counted by attempts, as the
author's ruling of 2026-09-25 counts them, the original budget of twelve is
exhausted.

The draft runs no new research and proves nothing new.  It reads each rung
tree, verifies the Lean statements it cites by reading their source, and
re-runs each rung's registered checks (section 9).  Where a rung's text
and this draft differ, the rung's receipts and ledger are the record.
Reporting and replay consume no research attempt.

The draft keeps four things apart, as the ruling requires: results of the
original stage (sections 4 to 8), results of the continuation (none yet,
section 12), protocol deviations (section 12), and unresolved obstructions
(section 13).  Budget exhaustion is not reported as satisfying any clause
of the completion gate (section 14).

## 1. The experimental boundary

### 1.1 The seed and the write root

- The seed is `research/second/SEED.md`, committed once at `83fdabef` on
  2026-09-03, sha256
  `52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e`,
  Git blob `bc27dccdd4497197922e5f72723fcee9a38347e1`.  It is marked
  `-text` and has not changed.  Every one of the twelve rung manifests pins
  that sha256, and the pin verifiers re-ran green on 2026-09-25 (section 9).
- The supplied input is the repository itself at each rung's snapshot:
  the sealed kernel, proofs, artifacts, paper and claim ledger, and every
  earlier research tree, all read-only.  The seal contract of `CLAUDE.md`
  governs: nothing under `prompt/`, `paper/`, `code/`, `lean4/Derivation/`
  or `artifacts/` is written by the run.
- The run's write root is `research/second/` and `research/second_<rung>/`,
  plus the registrations `CLAUDE.md` allows a rung (the workflow step, the
  generated views, the gates skill lines, appends to `MANUAL.md`).

### 1.2 The supplied tree at each attempt

A snapshot is the commit at which a rung pins its consumed sources as Git
blobs; it is an ancestor of `ccd0ab06`, the commit this draft was written
on.  The tree hash is the Git tree of that commit.

<!-- markdownlint-disable MD013 -->

| attempt | label | tree | snapshot commit | tree hash | frozen `PROMPT.md` sha256 | frozen `PREDICTIONS.md` sha256 |
|---:|---|---|---|---|---|---|
| 1 | 0 | `second_inheritance` | `7dabce4e8f8b22c3841511b1414d879dff3d7a65`; landed replay at `dd2aba24aca2bcfba065a8af1ff4a928b24a7907` | `c37dd4c6`; `544e77ef` | `aa804ee3eaab8b35…` | `86767fe4d8b2ed73…` |
| 2 | 1 | `second_stream` | `3f44571240a0830a2fa8de639281670f4e50a511` | `1d32cef0` | `efca5d969189bc2d…` | `b688840362287aa3…` |
| 3 | 2, track one | `second_nofirst` | `16fcffd64fcc8c7299a5dda5bb8b7082dc181c11` (launched at `3f445712`; repinned 2026-09-10 and 2026-09-23 when the sealed paper moved) | `e652ca24` | `e13f38a2ed329900…` | `7a0d9ba8ef1ee6d7…` |
| 4 | 2, track two | `second_stake` | `3f44571240a0830a2fa8de639281670f4e50a511`; freeze commit `d4d5830e` | `1d32cef0` | `4bd0b507f322c952…` | `efd3893006b4b59e…` |
| 5 | 3 | `second_index` | `110fededbeb63efd839287d3a4eda7a62aee4d97` | `d2c2f2eb` | `8487d72e4f3840b8…` | `410c6ff9d17d449f…` |
| 6 | 4 | `second_iso` | `bdbe583289fd641e7399d46bf8769d8101efc3cc` | `947b9146` | `833fb3b369636d7d…` | `dffe41d4084b7e5d…` |
| 7 | 5 | `second_symmetry` | `630622da034a17113b7bce0c34f2d9d122ea25f1` | `6bae49ea` | `7b3f73c0af7b1e5e…` | `bcedea0030021838…` |
| 8 | 6 | `second_succession` | `144d9c2bcd356290cce070887f03811416bc87b1` | `6e0f87af` | `ac59280878c2e8f6…` | `bffdd720b9dc4f96…` |
| 9 | 7 | `second_duration` | `d6dca75058e2d65ad5be19d682fb2a6b93291ecc` | `2972368e` | `90ee1d2266f7d1a1…` | `338d1b115327e1b9…` |
| 10 | 8 | `second_class` | `35e680ec35dfffb8a108ac88783645880eaabaf9` | `0d1d1856` | `16b57c49057359fc…` | `75f0dfca01023bce…` |
| 11 | 9 | `second_profile` | `ff584d441caad8300d01cbfda8b316846a8b5fc4` | `c14f9db9` | `df68d1cc735c3bfc…` | `7fc9a68c6447a7df…` |
| 12 | 10 | `second_response` | `77ad2a7839aff8c9ec9b0204a5e9d6927fe8ae38` | `ac13e411` | `09e9df8c4349b1ef…` | `2fc139d7f455da1a…` |

<!-- markdownlint-enable MD013 -->

The full digests are in each tree's `STATUS.md` and `SOURCE_MANIFEST.json`;
the verifiers compare them with the committed bytes.  The continuation's
starting commit is `01876f3a43490c3518e5c2c03c975ea9d21f49c0` (tree
`28ac749d`).

## 2. Metatheory and object language

**Object language.**  The sealed grammar, as the sealed kernel declares it:
regimes and their well-formedness, contexts, plugging, derivability,
collapse and separability, the six event kinds, the one-step admission and
replay.  To it the run adds two DECLARED inputs, never derived here: a
two-sided stake and a stream (growth by one fresh datum at a demand-free
state).  A demand is read off a regime and a declared stake; nothing in
the object language emits one.

**Metatheory.**  Everything else: the rung protocol and the next-rung
rule; the declared bounds and rectangles; the enumerations, receipts and
pins; the Lean packages and their verifiers; the census columns
DEFINABLE, USEFUL REALIZATION and FORCED; the candidate space at three
items (a declaration of rung one); the stake menu (a declaration of rung
two track two); the three readings of an accepted round (a declaration of
rung six); the choice of the sealed responder as "the response" of the
census rows (a declaration of rung ten); the author's rulings; the
operator's acts.  None of these is an object-language conclusion.

**Carriers, kept apart.**  In the terms of `docs/GENESIS_CLOSEOUT.md`
section one, this run is the carrier "second derivation"; it is not part
of the Alpha slice, and no bridge from it to the Alpha harness or to the
passage system is claimed.  Inside the run, three carriers matter:

- the sealed Python kernel under `code/derivation/`, consumed read-only
  through its public functions, whose regimes keep sets;
- each rung's Lean package, a verbatim reconstruction of the sealed kernel
  slice (lists, which may hold a repeated entry) with the rung's own
  definitions, importing nothing sealed;
- the sibling research trees consumed read-only (the two-sided commitment
  tree, the one-sided tree's represented state).

No refinement proof joins the Python computations to the Lean statements.
They are compared by transcribing exhibited witnesses into the other
grammar and replaying them.  One difference between the carriers is
material: the sealed Lean reading regimes `R2L` and `R2F` hold the
requirement imposed at the sealed Challenge 3, while the sealed Python
genesis readings L and F, which rungs three to ten take as bases, stop
before it.  Two frozen predictions missed on that difference (J-12, P-13;
`SD-RUN-6`).

## 3. Definitions, in dependency order

Each definition is the sealed one unless a rung is named.

1. **Regime.**  A number of data, a list of forms (each an arity), a list
   of judgment instances (a form index and a tuple of datum indices), a
   list of ruled forms, and a list of requirements (ordered pairs of data).
   **Well-formed**: instances respect arity and datum bounds, rules name
   admitted forms, requirements are ordered pairs of admitted data, every
   arity is at least one.
2. **Context.**  A form with a slot tuple, at least one slot a hole.
   **Plugging** a datum fills every hole with it.  **Derivable**: an
   instance is admitted, or its form carries a uniform rule.
3. **Collapse** of two data: every well-formed context derives the two
   pluggings alike.  **Separable**: some well-formed context tells them
   apart.  The **profile** of a datum is the set of contexts deriving its
   plugging (Python); two data are separable exactly when their profiles
   differ.
4. **Events.**  Six kinds: supply (a token), admit a datum, admit a form,
   admit an instance, admit a uniform rule, impose a requirement.  One
   **step** admits one event or refuses it; a supply changes nothing.
   **Replay** folds a history over a base, all or nothing.
5. **Genesis.**  The empty regime.  The **reading regimes**: in Lean,
   `R2L` (two data, requirement (0, 1)) and `R2F` (three data, requirement
   (1, 2)); in Python, the sealed genesis histories of readings L and F,
   which stop before the requirement.
6. **Isomorphism.**  The sealed structure: a datum map and a form map with
   inverses on the admitted ranges, carrying arities, instances, rules and
   requirements both ways.  An **automorphism** is one from a regime to
   itself.  The Python **key procedure** assigns each regime a key; its
   classes are cross-checked against a brute-force minimum over bijections.
7. **Stake** (the declared input).  A label apart, same or `free` on
   every ordered pair of datum indices, `free` on the diagonal, declared
   once.  A pair is **honoured** when apart pairs are separable and same
   pairs collapsed; a **demand** is a held labelled pair not honoured.
   **Uniform** (rung four): one label on every distinct pair.
8. **Stream** (the declared input).  Growth: the supply and admission of
   one fresh datum at a demand-free state.
9. **Demand-inert kinds** (rung two track one): supply, imposition, and
   form admission at a well-formed regime.
10. **Prefix and first count** (rung three).  The regime a prefix of
    length `k` reaches; a **first count** is a prefix length at which a
    demand stands with no shorter prefix carrying one.  **Class-matched**
    histories (rung four): prefixes isomorphic at every length.
11. **Element count** (rung five): data plus the lengths of the four lists.
    **Clean** (rung eight): well-formed with no list holding an entry
    twice.
12. **Readings of an accepted round** (rung six): EVERY event; every
    ADMITTING event (not a supply); every CHANGING event (the regime
    differs after it).  **Growth** and **rest round** (rung seven): a
    CHANGING round that adds a datum, and one that does not.  The
    **duration vector** counts rest rounds between successive growths.
13. **Holds two** (rung nine): some two admitted data are separable.  A
    **representative list**: admitted data pairwise separable, every
    admitted datum collapsed with an entry.
14. **Exhausted** form (rung ten): every well-formed context on it reads
    every two admitted data alike; otherwise it **distinguishes**.  A pair
    is **moved** by a history when it is separable on one side and
    collapsed on the other.
15. **The sealed responder** (supplied; chosen as the census's response by
    rung ten): the sealed demand is a collapsed pair; a response is a
    minimum of the sealed candidate space of at most two items and arity
    at most two, under one of the two sealed cost measures `mu1`, `mu2`.
    It refuses to run on a regime holding a uniform rule.  **Adjacency**,
    **reach** and **branching** are rung ten's readings of the census rows
    through it.
16. **Census columns** (the seed): DEFINABLE (a function of the state's
    own observables exists), USEFUL REALIZATION (exists under an
    additional named and priced declaration), FORCED (proved to hold in
    every surviving engine of the seed's sense), or none of these.

## 4. Challenges 0 to 5, and their dispositions

<!-- markdownlint-disable MD013 -->

| challenge | original stage | continuation |
|---|---|---|
| 0, replay the inheritance | **Answered at stated scope.**  Replays exact; six event kinds, one state-preserving; two remaining inputs named; inertia a finite computation to eight supplies and five data (rung zero); in Lean, supplies preserve the regime and the `free` stake carries no demand at any regime, the latter at the level of a definition (rung two track one).  `SD-00-1` to `SD-00-5`, `SD-02a-2`, `SD-02a-3` | none |
| 1, the stream as a response | **OPEN.**  Scoped finite results only: no retained V1 minimum of 1680 carries a datum; 32 of them were selected at three items; all fourteen recorded refusal situations are answered at exactly three items; two new first refusals appear.  1039 nodes stopped at the guard and targets after a first refusal were not searched.  Four items not computed (R1-X PENDING).  `SD-01-1` to `SD-01-10` | not authorized |
| 2, the stake from the state | **Answered within a declared menu and rectangle, by finite computation only.**  Nine rules on six observables; six CHECKED invariant over 1,345,706 cases; three OPEN at transport replay; three index-reading controls refuted; E4 alone generates both demand kinds, and its invariance is OPEN; no member is both; all nine retained.  No Lean.  `SD-02b-1` to `SD-02b-7` | not authorized |
| 3, the engine | **Unrun.**  Named as leftover X-5 at rung three; the next-rung rule, as rungs three to ten read it, never selected it.  `SD-RUN-2` | attempt one **RUNNING**, launched from `01876f3a`; no result |
| 4, run forward | **Unrun.**  The rectangle of rungs three to ten enumerates histories supplied from outside; no run is generated.  `SD-RUN-3` | attempt two **not begun**; opens only after attempt one closes |
| 5, the census | **DEFINABLE and USEFUL REALIZATION columns decided for all twelve rows**, over histories of the sealed step: in Lean for every history where cited, and by finite computation on rung three's rectangle.  **FORCED column undecided for all twelve rows.**  Stages are rectangle stages, not stages of an engine's run.  Section 7 | the FORCED evaluations belong to attempt two |

<!-- markdownlint-enable MD013 -->

## 5. The rung protocol and the attempts

### 5.1 The protocol as run

Each rung is one branch and one pull request against `main`, never
stacked, merged by the author.  Before anything else the rung freezes its
question (`PROMPT.md`) and then its predictions (`PREDICTIONS.md`) by
sha256, each in its own commit, before any computation and before any
Lean build.  It then computes, scores its predictions mechanically in its
receipt, keeps every miss beside its value, classifies every result,
names every leftover with a price, pins every consumed source as a Git
blob at a snapshot, registers its checks in the workflow's research job
(and its Lean audit in the lean job), and records its gate injections in
`research/second/MANUAL.md`.  Every rung with a Lean package (two track
one, and three to ten) also carries a total FW-DEF census of its Lean
theorems (CONTENT, THIN, DEFINITION, RECONSTRUCTION) checked in both
directions, and a declaration-by-declaration comparison of its
reconstructions with the pinned blobs at the snapshot.

The next rung is chosen by the seed's rule: the smallest named leftover
that reduces the count of declared inputs or extends the census of
Challenge 5, and on a tie the one named first.  Two readings were added
during the run: a leftover that refines a decided row does not extend the
census (rung six, applied to every carried row at rung seven), and "named
first" means first in the applying rung's list (author, 2026-09-25).  No
leftover ever reduced the count of declared inputs.

### 5.2 The twelve attempts

<!-- markdownlint-disable MD013 -->

| attempt | label | tree | pull request | merged | question | answer |
|---:|---|---|---|---|---|---|
| 1 | 0 | `second_inheritance` | 130 | 2026-09-03 | Challenge 0 | receipts replay; the declared inputs are censused; nothing follows from the inheritance within the bound |
| 2 | 1 | `second_stream` | 133 | 2026-09-04 | Challenge 1 at three items | OPEN; no selected V1 minimum carries a datum in the measured tree |
| 3 | 2, track one | `second_nofirst` | 136 | 2026-09-04 | in the grammar extended by a declared stake, where can a demand come from | from a declared label only, at the level of a definition; growth generates; inert runs carry no first demand |
| 4 | 2, track two | `second_stake` | 135 | 2026-09-04 | Challenge 2 | no menu member both checked invariant and generating both kinds; three members OPEN |
| 5 | 3 | `second_index` | 239 | 2026-09-23 | L-2, the first-demand index over an arbitrary run | unique; not a function of the regime; can cease; existence conditional on a decision |
| 6 | 4 | `second_iso` | 255 | 2026-09-25 | X-3, the index up to the isomorphism | invariant under uniform stakes; escapes under the three index readers |
| 7 | 5 | `second_symmetry` | 258 | 2026-09-25 | Y-3, symmetry along a history | which automorphisms survive is proved per kind; the size moves both ways; no return to a regime |
| 8 | 6 | `second_succession` | 259 | 2026-09-25 | Z-4, succession through the element count | CHANGING count definable from base and regime; EVERY and ADMITTING not |
| 9 | 7 | `second_duration` | 260 | 2026-09-25 | W-1, duration under CHANGING | segments and sum definable; each duration between growths not |
| 10 | 8 | `second_class` | 262 | 2026-09-25 | Z-1, the element count across the isomorphism | kept between clean regimes; no return to a class; recurrence only as stutter |
| 11 | 9 | `second_profile` | 264 | 2026-09-25 | X-6, two-ness and observational classes | both definable; first stage four and two events; the class count as a number OPEN in Lean |
| 12 | 10 | `second_response` | 265 | 2026-09-25 | X-6, adjacency, reach, branching, exhaustion | three useful realizations at two declared capabilities; exhaustion definable |

<!-- markdownlint-enable MD013 -->

Rung four's counts are dated 2026-09-24; its pull request merged at 00:19
on 2026-09-25.  Maintenance pull requests to the early rungs (137, 138,
139, 140, 146, 159, 164, 200, 203, 223, 231, 241, 243) are in the change
log; none revised a frozen prediction or a scored value.

### 5.3 How the rule ended the original stage

At rung ten the rule, read as rungs three to nine read it, selected no
leftover: none reduces the count of declared inputs, and with X-6 closed
none extends the census.  The engine (X-5), which every FORCED column
waits on, was never eligible under that reading.  Rung ten recorded both
facts for the author and acted on neither.  The author then ruled
(2026-09-25) that resolving a FORCED classification extends the census,
that X-5 is eligible as a named prerequisite, that the twelve attempts
exhaust the original budget, and that at most two continuation attempts
are authorized.  The ruling is recorded verbatim in `CLAUDE.md` and
`research/second/MANUAL.md`; it is paraphrased here.

## 6. Results by attempt: bounds, frontiers, proofs and countermodels

**Rung zero** (`SD-00-*`).  The sealed challenge reports and both sealed
closed baselines (reading L, 4 nodes, 3 terminal; reading F, 20 nodes, 16
terminal) regenerate exactly; the sibling dual summary regenerates byte
for byte.  The grammar has six event kinds, one of them state-preserving;
the sealed process declares two policies; the dual tree three events.  The
stake and the stream are the two remaining inputs; their introducing
trees, absent at the original snapshot, replay at `dd2aba24`.  Inertia to
eight supplies and five data is a finite computation; the only Lean
evidence cited is the sealed `supply_no_op`.

**Rung one** (`SD-01-*`).  Rectangle: both readings, five stakes, two
measures, at most three items, arity two, fifteen rounds, a pre-expansion
guard of 250 nodes.  The three-item space is the rung's declaration,
checked against the sealed enumeration below three items and an
independent construction on an eight-base family.  Frontier: 1974 nodes;
1039 stopped at the guard in six runs; no declared budget fired.  No
retained V1 minimum carries a datum; at the twenty three-item situations
no valid response of at most three items carries one.  All fourteen
recorded two-item refusals are answered at three items; two new first
refusals appear.  A fresh datum is valid but priced out in 219 rows, 58
of them for a same demand, which refutes the mechanism offered for R1-5.
No Lean.

**Rung two, track one** (`SD-02a-*`).  In the reconstructed grammar
extended by a declared two-sided stake: the label-source assembly holds at
the level of a definition; supplies preserve the regime (proved); three
kinds are demand-inert, found after a missed prediction; inert runs from a
well-formed base carry exactly the base's demands; growth generates apart
demands (discharged from "no admitted instance") and same demands (under a
separability hypothesis not discharged); the fresh datum's profile is
exactly the ruled forms' contexts; under the all-apart stake, from a
demand-free regime, one growth step leaves at most one demand altogether.
Rectangle: every sequence of at most four sealed events from each
reading; of 5908 growth steps from demand-free regimes under the
all-apart stake, 4000 generate exactly one demand and none generates
more, so the bound is attained and not vacuous.  A sentence giving the
first demand of any run one source was withdrawn against a two-admission
counterexample.

**Rung two, track two** (`SD-02b-*`).  Rectangle: both readings, both
measures, two items, arity two, four held data, fifteen rounds, guard 250;
847 reached regimes.  Six menu members CHECKED invariant; E3, E4, E6 OPEN
at transport replay; E4 the only member generating both kinds; no member
both.  The declared-input count is stated as two with no proof.  No Lean.

**Rung three** (`SD-03-*`).  Proved: the first count is unique, with no
decidability hypothesis; every event preserves well-formedness; from a
well-formed base, a successor first count never consumes an inert event
last; no first count
below two from the empty base; the `free` stake has none.  Existence is
proved only given a decision for a demand at a regime (OPEN, X-1).
Countermodels: the first count is not a function of the reached regime; a
demand can cease.  Rectangle: 577, 3928, 14293 sequences; two independent
procedures agree; demands cease only at instance and rule admissions.

**Rung four** (`SD-04-*`).  Proved: separability and honour transport
across the sealed isomorphism; a label-preserving isomorphism carries a
demand; under a uniform stake, carrying a demand is class-invariant and
class-matched histories have one first count; supply tokens move nothing.
Countermodels under `parity`, `chain` (three data; eight-event histories)
and `residueThree` (four data; eleven-event histories), closed through
Boolean checks proved sound (no converse).  Rectangle: 2316 regimes in 402
classes; automorphism counts one to 240; inside four events the first
count is constant on every trajectory class, which the Lean witnesses
show is the bound's doing.  OPEN: necessity of uniformity; the shortest
witnesses.

**Rung five** (`SD-05-*`).  Proved: a supply keeps every automorphism;
at a well-formed regime, datum and form admissions lose none; at every
regime, an instance, rule or requirement admission keeps exactly the
automorphisms fixing the added element, and, at a well-formed regime,
those common to both sides are exactly its fixers after as well.
Countermodels: each adding kind loses and gains automorphisms.  Proved:
every event keeps the regime or raises the element count by one, so no
history returns to a regime it left.  Rectangle: the size moves both ways
at the three adding kinds and only up at datum and form; multiplication
and fixer laws hold on every edge; largest fall 24.  No theorem counts an
automorphism set.

**Rung six** (`SD-06-*`).  Proved: under CHANGING the count is the element
count of the regime less the base's, so it is a function of base and
regime, and, counted from the empty regime, a function of the regime
alone; the three counts are ordered.  Countermodels: EVERY and ADMITTING are not functions of base
and regime; CHANGING is not a function of the regime alone across bases.

**Rung seven** (`SD-07-*`).  Proved: growths and rest rounds are
functions of base and regime; lower bounds on later segments through the
data that instances and requirements name; the tail is fixed when every
new element names late.  Countermodels: no single segment and no duration
between the first two growths is a function of the regime.  Rectangle: the
vectors reached are exactly the envelope at every regime (OPEN beyond,
V-1); the envelope is not a class invariant.

**Rung eight** (`SD-08-*`).  Proved: the isomorphism keeps data and form
counts with no hypothesis, and all five component counts between clean
regimes; every event keeps cleanness and the three sealed bases are clean;
from a clean base no class left is reached again, a class revisited is the
very regime reached by unchanging events, and the counts of a history are
functions of the class of the regime it reaches.  Countermodels: each
hypothesis needed (six pairs); across bases the class does not carry the
count.  This closes, for clean regimes and bases, three OPEN statements of
rungs five, six and seven, which stand as written (section 13).

**Rung nine** (`SD-09-*`).  Proved: separability, collapse, holding two
and representative lists are carried by the isomorphism with no hypothesis
(forward statements, the reverse through the exchanged structure);
collapse is reflexive, symmetric and transitive; holding two needs two
data, a form and an instance; four and two events are the least lengths
from the empty and the Lean reading regimes; four kinds keep separable
pairs.  Countermodels: an instance or a rule admission can end holding
two.  OPEN in Lean: the class count as a number.

**Rung ten** (`SD-10-*`).  Proved: exhaustion is carried by the
isomorphism with no hypothesis; per-kind keeping of exhaustion and of
distinguishing; for a well-formed base and every history, a moved pair is
mentioned by an instance admission of the history, or the history holds a
rule.  Countermodels: the four other changes of exhaustion; one instance
moves two pairs apart, or one apart and another together.  Rectangle with
the sealed responder: 426 regimes outside its domain; 3110 demands, none
refused within two items; reach at most three; distance at most two; the
measure changes the adjacency graph and the tie counts.  No Lean statement
is about a minimum, a cost or a tie.

## 7. The census of definability

"Stage" is the length of a history in rung three's rectangle, or every
history where a Lean statement is cited.  No row is evaluated at the
stages of a run generated by an engine, because none was run.

<!-- markdownlint-disable MD013 -->

| row | DEFINABLE | USEFUL REALIZATION | FORCED | first stage | evidence |
|---|---|---|---|---|---|
| two-ness | yes, as holding two | none needed | undecided | four events from the empty regime; two from each Lean reading regime | `SD-C-1` |
| count of observational classes | the classes, as a relation and as representative lists | none needed | undecided | as two-ness | `SD-C-2`; the number is a finite computation, OPEN in Lean |
| succession of accepted rounds | under CHANGING: from base and regime; from the regime when counted from the empty regime; from the class within a clean base.  Not under EVERY or ADMITTING; the first-demand index not from the regime | none | undecided | every stage | `SD-C-3` |
| duration, as rounds between growths | the number of segments and their sum; lower bounds; not each duration between growths | none | undecided | every stage | `SD-C-4` |
| adjacency | not established | yes: the sealed responder under one measure, two declared capabilities | undecided | three events from EMPTY, one from L, zero from F | `SD-C-5` |
| reach | not established | yes: same declaration and price | undecided | as adjacency | `SD-C-6` |
| an invariant | the element count (monotone, +1 per change); the fixer set of an added element | none | undecided | every stage | `SD-C-7` |
| irreversibility | no return to a regime; from a clean base, to a class | none | undecided | every stage | `SD-C-8` |
| symmetry | the automorphism count at every regime reached; which automorphisms survive each kind | none | undecided | every stage | `SD-C-9` |
| branching | not established | yes: same declaration and price; finite computation only | undecided | two events from EMPTY under `mu1`, three under `mu2` | `SD-C-10` |
| exhaustion | yes | none needed | undecided | one event | `SD-C-11` |
| recurrence | from a clean base: only as a stutter | none | undecided | every stage | `SD-C-12` |

<!-- markdownlint-enable MD013 -->

"Undecided" in the FORCED column is an OPEN obligation, not a decision.
By the author's ruling of 2026-09-25, recording OPEN is not an evidential
resolution.  No notion was added to the census by a logged declaration.

## 8. Predictions, and every miss

Predictions were frozen before computation and before Lean at every rung,
and scored mechanically.  A hit on a prediction labelled FORCED evidences
the order of the work, not insight; several rungs say so of their own
clean sheets.

<!-- markdownlint-disable MD013 -->

| rung | computational rows | FW-DEF census rows | misses, with the value found | pending |
|---|---|---|---|---|
| 0 | 3 hit of 3 | none | none | none |
| 1 | 10 hit, 1 missed | none | R1-9: 58 of 219 priced-out rows answer a same demand; predicted none | R1-X |
| 2, track one | 18 hit, 1 missed | 4 misses | N-16: three demand-inert kinds, predicted two; four definitional classes predicted as not | N-X |
| 2, track two | 6 hit, 9 missed, 1 unscored | none | P-I1, P-I4, P-G2, P-G3, P-G5, P-G6, P-G7, P-G9, P-G10 (values in its `STATUS.md`) | X |
| 3 | 10 hit of 10 | 17 of 25, 8 demotions | the eight class demotions | I-X |
| 4 | 8 hit, 1 missed | 31 of 38, 7 demotions | J-12: largest automorphism group 240, predicted 24 | none |
| 5 | 8 hit, 1 missed | 27 of 35, 8 demotions | K-14: largest fall 24, predicted 20 | none |
| 6 | 6 hit of 6 | 17 of 17 | none | none |
| 7 | 7 hit of 7 | 13 of 16 | two promotions, one demotion | none |
| 8 | 4 hit, 1 missed | 40 of 40 | P-13: the Lean countermodel's two sides lie in two classes in the Python grammar | none |
| 9 | 7 hit of 7 | 29 of 33, 4 demotions | the four class demotions | none |
| 10 | 11 hit, 1 missed | 37 of 39, 2 demotions | R-11: no demand refused within two items, predicted a refusal at L and F | none |

<!-- markdownlint-enable MD013 -->

Two misses (J-12, P-13) came from reasoning about the Lean reading regimes
while computing on the Python readings, whose receipt already showed the
difference.  Four extrapolations remain PENDING (`SD-RUN-8`).

## 9. Python and Lean receipts

### 9.1 The receipts as each rung recorded them

<!-- markdownlint-disable MD013 -->

| rung | tests | line / branch coverage | receipts | Lean reports (reconstructions) | recorded gate time |
|---|---:|---|---|---|---|
| 0 | 15 | not measured | `receipts/inheritance.json` | none | under four minutes |
| 1 | 145 at the rung; registered floor 150 | 97.89% / 95.02% | `receipts/stream.json`, split full export | none | 309 s for replay and tests |
| 2, track one | 180 | 98.67% / 95.33% | `receipts/nofirst.json` | 75 (17) | 729 s grouped |
| 2, track two | 54 | 97.21% / 95.27% | `receipts/stake.json`, split full export | none | 346 s |
| 3 | 133 | 98.98% / 95.79% | `receipts/index.json` | 87 (44) | 221 s |
| 4 | 148 | 99.32% / 97.52% | `receipts/iso_index.json` | 84 (35) | 52 s |
| 5 | 137 | 99.29% / 97.22% | `receipts/symmetry.json` | 64 (17) | 100 s |
| 6 | 139 | 98.87% / 95.93% | `receipts/succession.json` | 34 (17) | 92 s |
| 7 | 150 | 98.96% / 96.15% | `receipts/duration.json` | 33 (17) | 81 s |
| 8 | 147 | 98.92% / 95.68% | `receipts/class_count.json` | 58 (17) | 232 s |
| 9 | 141 | 99.07% / 95.95% | `receipts/profile.json` | 50 (17) | 231 s |
| 10 | 150 | 99.41% / 97.73% | `receipts/response.json` | 56 (17) | 177 s |

<!-- markdownlint-enable MD013 -->

Every Lean report lies within `{propext, Quot.sound}`; no `sorry`,
`admit`, user-declared axiom, `unsafe` or `partial` appears.  The exact
reliance per theorem is in the claim ledger.  The coverage figures are the
rungs' own local observations on their dates; each rung's coverage gate
requires 95% line and branch from a fresh report.

### 9.2 The replay this closeout ran

On 2026-09-25, at `ccd0ab06` on a clean worktree, before these three
files existed, this closeout ran every registered step of the run with the
repository's own runner:

```text
python ci/run_gates.py --job research --job lean --step "Second derivation" --keep-going
```

Result: **48 of 48 selected steps passed** (nine clean Lean audits in the
lean job; pins, replay with tests and coverage, and strict typing for all
twelve trees in the research job), from 20:24 to 20:56 local time.  The
runner reported one environment difference: the interpreter's pytest is
9.1.1 where `requirements.txt` pins 9.0.3; the rung tests run under
`unittest`.  The working tree was clean after the run, so no receipt was
rewritten.

<!-- markdownlint-disable MD013 -->

| rung | pins, spans, frozen texts | tests (skipped; registered floor) | line / branch coverage | receipt comparison | Lean audit (clean build) |
|---|---|---|---|---|---|
| 0 | pass | 15 (0; none) | not measured by any registered step | tests regenerate it; tree unchanged | none |
| 1 | pass: 19 sources, 5 frozen texts | 150 (0; 150) | 97.96% / 95.25% | `git diff` clean | none |
| 2, track one | pass | 185 (4; 180) | 98.90% / 95.91% | `git diff` clean | 75 reports, 8 axiom-free, 9 modules |
| 2, track two | pass | 72 (3; none) | 97.61% / 96.45% | regenerated byte-identically | none |
| 3 | pass | 138 (2; 120) | 99.21% / 96.43% | matches a fresh run | 87 reports, 3 axiom-free, 6 modules |
| 4 | pass | 148 (2; 140) | 99.32% / 97.52% | matches | 84 reports, 4 axiom-free, 10 modules |
| 5 | pass | 137 (2; 110) | 99.29% / 97.22% | matches | 64 reports, 5 axiom-free, 8 modules |
| 6 | pass | 139 (2; 130) | 98.87% / 95.93% | matches | 34 reports, 3 axiom-free, 5 modules |
| 7 | pass | 150 (2; 130) | 98.96% / 96.15% | matches | 33 reports, 2 axiom-free, 5 modules |
| 8 | pass | 147 (2; 130) | 98.92% / 95.68% | matches | 58 reports, 3 axiom-free, 9 modules |
| 9 | pass | 141 (2; 135) | 99.07% / 95.95% | matches | 50 reports, 3 axiom-free, 8 modules |
| 10 | pass | 150 (2; 140) | 99.41% / 97.73% | matches | 56 reports, 3 axiom-free, 8 modules |

<!-- markdownlint-enable MD013 -->

Every Lean audit printed "axioms within ['Quot.sound', 'propext']",
"fresh reports and FW-DEF rows exact" and "committed log matches the fresh
build".  The skipped tests are the rungs' branch-scope tests, which skip
by name when the branch under test carries no commit of theirs; they
were not exercised by this replay.  The printed `FAIL:` lines in the test
output are the rungs' negative tests exercising their own verifiers, not
failures.  A green step is a local receipt: it shows the gate did not
fire, not that the mathematics is right, and none of these gates was
re-injected here.

## 10. The seed's required questions

1. **Is two the floor of declared inputs within the declared bounds?**
   Not established.  The count stays two; no rung reduced it and no rung
   proved a floor (`SD-RUN-1`).  OPEN.
2. **Can the stream be a response, and at which bound?**  In the measured
   V1 tree at three items no selected minimum carries a datum, and a fresh
   datum is valid but priced out in 219 two-item rows.  Whether it is ever
   part of a minimum response is OPEN at three items (guard and
   short-circuit) and uncomputed at four (`SD-01-*`).
3. **Can the stake be read off the state, by which rules, and are they
   invariant under renaming?**  Within the declared menu: six rules are
   invariant on the rectangle by finite computation, three are OPEN, and
   the only rule generating both demand kinds is among the OPEN three.  In
   Lean, a uniform stake makes carrying a demand class-invariant and the
   three index readers do not (`SD-02b-*`, `SD-04-2`, `SD-04-5`).
4. **Does a minimal engine exist in the declared class of Challenge 3; is
   it unique up to isomorphism; is it initial?**  Refused in the original
   stage: no class was declared.  Pending continuation attempt one.
5. **Is a quantity preserved or monotone across every accepted round?**
   Over every history of the sealed step: the element count rises by
   exactly one at each changing event, and the fixer set of an added
   element is the same before and after (`SD-05-3`, `SD-05-5`).  These hold
   for every history, not only within a bound; whether they are invariants
   of an engine is OPEN.
6. **Can a state count its own rounds?**  Under CHANGING, yes, from the
   base and the regime through the element count, and from the regime
   alone when counted from the empty regime; within a clean base also from
   the class.  Under EVERY and ADMITTING, no.  Durations between growths,
   no; their number and sum, yes (`SD-C-3`, `SD-C-4`).
7. **Is adjacency definable, and is its distance definable?**  Adjacency
   is a useful realization under a declaration priced at two capabilities;
   the distance is derived from it with no further declaration and, on the
   rectangle, never exceeds two (`SD-C-5`).
8. **Does the process have an arrow?**  No history of the sealed step
   returns to a regime it left by a changing event, and from a clean base
   none returns to a class; a class is revisited only as a stutter
   (`SD-C-8`, `SD-C-12`).  Whether a run of an engine has more is OPEN.
9. **What recurs across engines?**  Not answerable: no engine was run.
   Across rungs, recorded and not interpreted: every FORCED column waits
   on the engine; a decision procedure over contexts (X-1) blocks several
   Lean statements; the Lean and Python reading regimes differ; the FW-DEF
   census misses are almost all demotions.
10. **Is the surviving engine minimal or initial among engines meeting the
    same challenges?**  Refused: no engine was declared.
11. Answered only in the sealed comparison, after the freeze, in the
    companion repository, and nowhere here.

## 11. The strongest defensible terminal statement

> In the sealed grammar extended by a declared two-sided stake and a
> declared stream, and over histories of the sealed step -- in Lean for
> every history where a theorem is cited, and by finite computation on
> rung three's rectangle of every sequence of at most four declared events
> from the empty regime and the two sealed Python readings -- the original
> stage of the second derivation established: nothing follows from the
> inheritance alone (supplies change no regime; under the `free` stake no
> regime carries a demand, at the level of a definition); within the
> measured three-item tree no selected minimum response contains a fresh
> datum, while whether one ever does remains OPEN; no member of a declared
> nine-rule stake menu is both checked invariant on its rectangle and
> observed to generate both demand kinds; and every one of the twelve
> census rows is decided in its DEFINABLE or USEFUL REALIZATION column,
> none in its FORCED column.  The count of declared inputs remains two; it
> was neither reduced below two nor proved to be the floor.  No engine in
> the seed's sense was declared or run: Challenges 3 and 4 are unrun in the
> original stage and pending in an authorized continuation.  The original
> stage ended because its twelve-attempt budget was exhausted and its
> next-rung rule selected no leftover, not because the completion gate was
> met.

This is a statement of what was derived and of how the stage terminated.
It is not a floor theorem, not a reduction, and not a result about any
engine.

## 12. Original stage, continuation, deviations, obstructions

**Original-stage results.**  Sections 4 to 8 and every `SD-00` to `SD-10`
and `SD-C` row of the claim ledger.

**Continuation results.**  None.  Attempt one (Challenge 3) was launched
headless from `01876f3a` on branch `research/second-engine-continuation`;
when this draft was written that branch carried two freeze commits
(`03b67607`, question; `596e2c6e`, predictions) and no result, and nothing
of it is read or reported here.  Attempt two (Challenge 4 with its
engine-dependent census evaluations) had not begun and opens only after
attempt one closes.  No further attempt is authorized.

**Protocol deviations and interventions, each disclosed where it happened:**

- The seed's author and the run's first session were the same session
  (`MANUAL.md`, declared reading one); rung zero is not blind to its
  author's expectation.
- Rungs one and two were launched with an operator packet held outside the
  repository; the rung files name it.  The seed's section eleven asks for
  no user input after Challenge 0.
- The author resolved rung two's tie by running both candidates as two
  separately scoped tracks (`research/second_stake/STATUS.md`).
- From rung three on, the rungs followed the seed's next-rung rule and not
  `PLAN.md`'s execution list, which placed the engine at rung three and
  "run forward" at rungs four and five; the plan was not edited.
- Rung two track one's prompt forbade importing the sealed package where
  the seed's section eight says rungs consume it "as a pinned
  dependency"; the rung reconciled the two by the seed's qualifier ("as
  the sibling research trees do", which reconstruct) and recorded the
  tension.  Every later Lean rung reconstructs.
- Author rulings of 2026-09-23 (a rung regenerates its generated views)
  and 2026-09-25 (a rung adds its gate scripts to the gates skill;
  "named first" means first in the list; the continuation ruling).
- Rung nine and rung ten each applied their own reading of a leftover
  carrying several rows, recorded before their predictions.
- Operator acts stated in the closeout order and not found in any
  committed file or pull-request text read for this draft: headless
  launches with a fixed one-line prompt; rung ten's session paused at
  13:38 and resumed with a bare "continue" (its predictions froze at 13:32
  and its next commit is at 18:55); during rung four, a process listing
  exposed another repository's name, with no content.

**Unresolved obstructions.**  Section 13.

## 13. Limitations and open obstructions

- **The engine and the run forward** (Challenges 3 and 4): unrun; the
  continuation's.  Every FORCED column waits on them.
- **The declared-input floor**: neither a reduction nor a floor proof.
- **The stream as a response** (rung one): 1039 guard-stopped nodes, the
  first-refusal short-circuit, the four-item bound, V2 beyond nineteen
  situations, and the narrow-versus-wide comparison are OPEN.
- **Stake invariance** for E3, E4, E6: OPEN at target-regime transport
  replay.  No Lean statement concerns any menu rule.
- **A decision procedure over contexts** (X-1): not built.  Existence of a
  first count, necessity of uniformity (Y-2), the class count as a number
  (T-1), and deciding holding two or exhaustion at a regime in Lean wait
  on it.
- **The carrier bridges**: rung two track one's represented state is not
  bridged to the sealed regime (L-1, which needs an amendment of the seal
  that is the author's act); no refinement proof joins any Python
  computation to any Lean statement; the reading regimes differ.
- **Responses in Lean** (S-3): no statement about a minimum, cost or tie;
  the sealed responder's domain excludes ruled regimes (S-1); the other
  demand kind is not read (S-2); the distance bound of two is not known to
  be the grammar's (S-4).
- **Lean refinements of decided rows**: the numeric fixer and
  multiplication laws (Z-2, Z-3), attainment of the envelope (V-1), the
  multiset of envelopes of a class (V-3), recurrence from an unclean base
  (U-1), the Lean form of "a history recurs exactly when it holds an
  unchanging event" (U-2), the change of the class count by
  one event (T-2), the full set of counts (W-2), the shortest witnesses
  (Y-1), the converse of the checks at arity one (Y-4).
- **Reconstruction omissions**: each Lean rung pins the declarations it
  omits from the sealed sources; that they are safe to omit is read by
  hand (X-4 and its analogues).
- **The bound**: every rectangle result stops at four events (rungs three
  to ten), three items (rung one) or four held data (rung two track two).
  Rung four shows the bound can hide a phenomenon: inside four events
  the first count is constant on every trajectory class under every
  stake, while its Lean witnesses of eight and eleven events show it is
  not constant under the three stakes that are not uniform.
- **Supersessions within the run, dated 2026-09-25 and left standing**:
  rung five's SYM-14, rung six's class-level OPEN and the sum part of rung
  seven's class-level OPEN are closed for clean regimes and bases by rung
  eight (`SD-05-7`, `SD-06-6`, `SD-07-6`).  No sealed sentence is
  superseded by this run; the sealed first standing obstruction stands as
  the sealed paper records it (`SD-RUN-7`).

## 14. Completion-gate audit

One line per clause of the seed's section twelve.  MET means the evidence
named establishes the clause at the scope stated; UNMET means the record
shows the clause is not satisfied; NOT_ESTABLISHED means neither is shown.
Budget exhaustion satisfies no clause.

<!-- markdownlint-disable MD013 -->

| clause | status | evidence |
|---|---|---|
| every introduced notion has a source classification | NOT_ESTABLISHED | each rung ledger classifies its rows and each Lean rung's FW-DEF census is total and checked both ways; no run-level census of notions is checked by any gate, and this draft's ledger is unfrozen and judged by reading |
| every state change has a replayable admission history | MET at the computed scope | rungs three to ten record zero replay mismatches over the rectangle, with the counter shown able to fire at rung three; rung two track two replays every stored node and every edge certificate; rungs zero, one and two track one build every state by replaying its history through the sealed or sibling replay; state changes only through sealed events |
| the count of declared inputs is reduced below two or proved at its floor, with the bounds stated | UNMET | the count stays two; no reduction and no floor proof (`SD-RUN-1`) |
| every engine in the declared class is run to bounds, refuted, or recorded OPEN | UNMET | no engine class was declared in the original stage; continuation attempt one is running (`SD-RUN-2`) |
| every row of the definability census is proved, countermodelled, or OPEN at every stage reached | NOT_ESTABLISHED | DEFINABLE and USEFUL REALIZATION columns decided for all twelve rows over histories of the sealed step; the FORCED column is only recorded OPEN, which the author's ruling does not count as resolution; no engine-run stages exist (section 7) |
| every theorem-level claim used by the paper has Lean evidence or is downgraded | MET for this draft | every theorem-level claim cited names a Lean theorem whose statement was read at `ccd0ab06` and whose axiom report the registered audit re-checked on a clean build (section 9.2); every other claim is marked finite computation, countermodel, OPEN or prediction |
| every computational claim has deterministic Python evidence | MET at the computed scope | every rung's receipts regenerate byte-identically under its registered comparison, re-run green on 2026-09-25 (section 9.2); every computational claim of the ledger names a receipt field or test |
| all tied minimum branches are retained unless eliminated by proof | NOT_ESTABLISHED | the computed trees of rungs one and two track two retain ties under the implemented quotient, and rung ten counts every tie; but rung one does not search targets after a node's first refusal, and the minima of the engine class of Challenge 3 were never enumerated |
| Python line and branch coverage each meet 95% | NOT_ESTABLISHED | rungs one to ten each gate 95% line and branch from a fresh report; rung zero has no coverage gate and its coverage was never measured by a registered step |
| Lean builds without forbidden proof gaps and every module is audited | MET | the nine Lean packages each pass their registered clean-build audit: compiler census of every module, whitelist `{propext, Quot.sound}`, committed log equal to the fresh build (section 9.2) |
| every gate is proved by injection | UNMET | the manual records no injection for rung zero's tests and typing, nor for strict typing in rungs one, two track one, and three to ten; only rung two track two injected its typing gate |
| all intentional files committed, working tree clean, `SEED.md` byte-identical to its pinned hash, every sealed path untouched | NOT_ESTABLISHED | `SEED.md` hashes to `52439e5f…` and every rung pin verifier passes (section 9.2); none of the 94 non-merge commits up to `ccd0ab06` that touch `research/second/` or a rung tree touches a sealed path (checked with `git diff-tree` for this draft; the rungs' own sealed-path tests are branch-scoped and skipped on this replay); this draft's worktree is clean at its commit; but continuation attempt one's files are in progress on another branch, so the run's intentional files are not all committed |
| the comparison is written after the freeze, in the companion repository only, and has caused no revision here | UNMET | the freeze has not happened and no comparison exists |
| the paper states what was actually derived, including termination or failure, without targeting a predetermined conclusion | NOT_ESTABLISHED | this draft attempts it (sections 11 and 12); it is unfrozen, and the judgement is the author's at the freeze |

<!-- markdownlint-enable MD013 -->

## 15. What this draft does not do

It does not freeze anything, merge, tag or publish.  It does not write the
comparison, name any known theory, or answer the seed's eleventh question.
It does not edit the seed, the plan, the manual, any rung tree or any
sealed path.  It does not read the continuation's work in progress.  It
does not treat a receipt, a pin or a green gate as proof of a mathematical
payload.
