# PREDICTIONS: rung eight -- the element count across the isomorphism

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_class.py` for the computational rows and by `test_census.py` for
the census rows.  A missed prediction is recorded next to its value and
never edited.  A miss is a finding, not a defect.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this rung, so a hit evidences the ordering of the
work and not insight.  NOT FORCED means the run could have come out the
other way.  An argument written by this rung's own session before the
run is not a receipt: a row that leans on one is NOT FORCED.

Receipts and sources read before freezing, because a prediction below
leans on them: rung four's `receipts/iso_index.json` (577, 3928 and
14293 sequences; 75, 523 and 1718 distinct regimes at EMPTY, L and F;
2316 distinct regimes in all, in 402 classes of the sealed key
procedure, with zero disagreements against the sealed brute-force
minimum); rung seven's `CLAIM_LEDGER.md` row DUR-17 (54, 174 and 265
classes within EMPTY, L and F); rung six's `receipts/succession.json`
(zero classes reached with two CHANGING counts within a base); rung
five's `STATUS.md` (no sequence of the rectangle returns, by a changing
event, to a class an earlier prefix reached); the declared alphabet of
the rectangle in `research/second_nofirst/nofirst.py` (one supply token;
five fresh datum tokens, taken in order; every instance, rule and
requirement the regime allows is offered, whether held or not; arities
one and two; at most five data, two forms and four events); the sealed
Python step in `code/derivation/model.py` (sets, so re-admitting a held
instance, rule or requirement returns the regime unchanged); and the
Lean of rungs five, six and seven named in `PROMPT.md`.

## Declared before the compile: the FW-DEF census this rung commits to

Four classes, as the sibling rungs use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this rung's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion); THIN (one
genuine step, or a direct corollary of a neighbour); CONTENT (everything
else).

Predicted DEFINITION:

- `replayE_cons`
- `replayE_split`
- `sortPair_of_le`
- `sortPair_map`
- `genesis_clean`
- `R2L_clean`
- `R2F_clean`
- `insts_need_nodup`
- `insts_need_wf`
- `rules_need_nodup`
- `rules_need_wf`
- `reqs_need_nodup`
- `reqs_need_wf`
- `counts_not_of_class`

Predicted THIN:

- `insertNew_grows`
- `step_parts`
- `still_of_no_changes`
- `nodup_map_of_inv`
- `count_le_of_inv`
- `data_le`
- `forms_le`
- `iso_data`
- `iso_forms`
- `insts_le`
- `rules_le`
- `reqs_le`
- `components_iso`
- `size_iso`
- `nodup_insertNew`
- `getD_append_lt`
- `clean_replay`
- `no_return_class`
- `recurrence_is_stutter`
- `counts_of_class`
- `counts_of_class_genesis`

Predicted CONTENT:

- `changes_counted`
- `growths_counted`
- `rest_counted`
- `length_le_of_nodup_sub`
- `clean_step`

The names above are the ones this rung commits to before Lean has run.  A
name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census and
is recorded in `STATUS.md` as unpredicted work.  Six of them repeat, as
statements, lemmas earlier rungs proved: `replayE_cons` and
`insertNew_grows` (rungs six and seven), `changes_counted` (rung six;
rung five's `size_counts_changes`), `step_parts`, `growths_counted` and
`rest_counted` (rung seven), and `getD_append_lt` (rung five).  They are
proved again here so that the package imports nothing, and the ledger
credits each statement to its rung.

The Lean objects, declared here so the rows below can name them: `size`,
rung five's element count; `changes`, rung six's CHANGING count;
`growths` and `rest`, rung seven's; `isoSymm`, the sealed isomorphism
with its maps exchanged, a definition; `Dupfree r`, that the lists of
instances, rules and requirements of `r` are each without a repeated
entry; `Clean r`, that `r` is well formed in the sealed sense and
duplicate-free.

## Stage one -- the counts across the isomorphism, in Lean

- **P-1** (NOT FORCED).  `iso_data` and `iso_forms` are PROVED for every
  pair of regimes and every inhabitant of the sealed isomorphism between
  them, with NO hypothesis on either regime: the numbers of data are
  equal, and the numbers of forms are equal.
  Falsifier: either OPEN, or needing well-formedness or
  duplicate-freedom.
- **P-2** (NOT FORCED).  `insts_le`, `rules_le` and `reqs_le` are PROVED
  with hypotheses on the SOURCE regime only -- well formed, and its one
  list concerned without a repeated entry -- giving that the source list
  is no longer than the target list.  `components_iso` and `size_iso`
  follow for two clean regimes: all five component counts are equal, and
  so is the element count.
  Falsifier: any of the five OPEN, or needing a hypothesis on the target.
- **P-3** (NOT FORCED).  Each of the six countermodels computes: for
  each of the instances, the rules and the requirements, there are two
  isomorphic regimes, both well formed, one of them duplicate-free, with
  different lengths of that list (`*_need_nodup`); and two isomorphic
  regimes, both duplicate-free, one of them well formed, with different
  lengths of that list (`*_need_wf`).  So neither hypothesis can be
  dropped for any of the three.
  Falsifier: any of the six failing to compute, or needing a pair in
  which both regimes break a hypothesis.
- **P-4** (NOT FORCED).  `clean_step` is PROVED for every clean regime
  and every event of the six kinds: the regime after a well-formed event
  is clean.  `clean_replay` follows for every history.  The sealed empty
  regime and the two sealed reading regimes are clean.
  Falsifier: any OPEN, or `clean_step` needing a hypothesis beyond
  cleanness.
- **P-5** (NOT FORCED).  From a clean base, for every history that
  replays: `no_return_class` -- if the first event changes the regime, no
  regime the rest of the history reaches is isomorphic to the base; and
  `recurrence_is_stutter` -- if the history is split in two, and the
  regime reached after both parts is isomorphic to the regime reached
  after the first, the two regimes are EQUAL and the second part has
  CHANGING count zero.
  Falsifier: either OPEN, or needing a hypothesis beyond a clean base.
- **P-6** (NOT FORCED).  `counts_of_class`: from one clean base, two
  histories that reach isomorphic regimes have one CHANGING count, one
  number of growths and one number of rest rounds.
  `counts_of_class_genesis`: in particular from the sealed empty regime.
  Falsifier: either OPEN, or needing a hypothesis beyond a clean base.
- **P-7** (FORCED).  `counts_not_of_class`: across two bases the answer
  changes -- the empty history from the sealed reading regime L, and a
  datum, a datum and the requirement between them from the sealed empty
  regime, reach one regime with CHANGING counts zero and three.  Kernel
  computation.
  Falsifier: the countermodel failing to compute.
- **P-8** (NOT FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.  The
  library's own counting lemma for lists without repeated entries opens
  a classical section, so it is not used; a native one is proved
  instead.
  Falsifier: the committed axiom log naming any other axiom.

## Stage two -- the finite cross-check

The bases, the bound and the alphabet are rung three's and are not
chosen after seeing a count.

- **Declared rectangle.**  Rung three's, consumed through rung four's
  public population: three bases (EMPTY, L, F), every sequence of at
  most four declared events.  For a sequence and its prefixes, numbered
  from zero (the empty prefix) to its length, the sequence RECURS at
  position `k` when the regime after prefix `k` has the class of the
  regime after some prefix `j` less than `k`; the recurrence is a
  STUTTER when the two regimes are equal and a RETURN otherwise; the
  KIND of the recurrence is the kind of the event at position `k`.  A
  sequence RECURS when it recurs at some position.
- **P-9** (FORCED).  577, 3928 and 14293 sequences; 75, 523 and 1718
  distinct regimes; zero replay mismatches; 54, 174 and 265 classes
  within EMPTY, L and F; 402 classes over the 2316 distinct regimes of
  all three; zero disagreements between the key partition and the
  brute-force partition.
  Falsifier: any other value.
- **P-10** (NOT FORCED).  Zero classes, within any base and over all
  three together, carry two values of any of the five component counts.
  Falsifier: any such class.
- **P-11** (NOT FORCED).  At every base: zero returns; a sequence recurs
  exactly when it holds an event that leaves the regime unchanged (zero
  mismatches); and stutters are reached by each of the four kinds
  supply, instance, uniform rule and requirement, and by neither a datum
  nor a form.
  Falsifier: a return; a mismatch; a base at which one of the four kinds
  reaches no stutter; a stutter reached by a datum or a form.
- **P-12** (FORCED, by arithmetic on receipts and by one exhibited
  history).  The number of classes reached at more than one base lies
  between forty-six and ninety-one inclusive, since the within-base
  class counts sum to four hundred and ninety-three, ninety-one more than
  the four hundred and two classes of the union; and at least one class
  is reached at two bases with two CHANGING counts, the class of the
  sealed reading regime L, reached from L by the empty sequence and from
  EMPTY by three events.
  Falsifier: any count outside that range, or no class with two counts.
- **P-13** (FORCED).  The Lean countermodels, written in the sealed
  Python grammar: the two regimes of each `*_need_nodup` are one Python
  regime, because the Python regime keeps sets; the event that would
  admit the ill-formed element of each `*_need_wf` is refused by the
  sealed Python step; and the two sides of `counts_not_of_class` replay
  to regimes of one class with CHANGING counts zero and three.
  Falsifier: two Python regimes, an event accepted, or any other value.

## Stage three -- the census rows and the input count

- **P-14** (NOT FORCED).  The ledger decides the challenge-five census
  row for recurrence: over histories of the sealed step from a clean
  base -- the sealed empty regime and the two sealed reading regimes
  among them -- an isomorphic state is revisited only as the same
  regime, through events that leave it unchanged, and never after a
  changing event (PROVED); on the rectangle, stutters by four kinds and
  no return (FINITE_COMPUTATION).  It adds to the irreversibility row
  that no history from a clean base returns to a CLASS it left, and to
  the succession and duration rows that the CHANGING count, the growths
  and the rest rounds are carried by the class within a clean base and
  from the empty regime, and not across bases (PROVED and COUNTERMODEL).
  FORCED in the seed's sense is conditional on an engine whose rounds
  are the changing events of the sealed step, and no such engine exists
  yet; each row says so.
  Falsifier: the ledger recording a row without that condition, or
  recording any class-level statement without its clean-base scope.
- **P-15** (FORCED).  This rung neither reduces the count of declared
  inputs nor proves it at a floor; the value stays two.
  Falsifier: any claim otherwise.
- **P-16** (FORCED).  The receipt regenerates byte-identically, every
  node replays from its base, and the grouped gate time stays under
  fifteen minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.
