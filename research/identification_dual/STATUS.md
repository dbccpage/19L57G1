# identification_dual: the sealed machine run under the other demand

`AuthorityEffect: None`.  This tree records; it does not certify.

The sealed derivation answers one demand, Separate(i, j), from a genesis
where every admitted datum is observationally collapsed.  This tree runs
the same machine under the other demand, RequireSame(i, j), from the
states the sealed machine ends in: the all-pairs-separated fixpoints of
its closed-system baselines.  Nothing under the seal is modified, no
starting state is constructed by hand, and the sealed pruning lemmas are
not used, because they were proved for the separation demand only.  The
challenge is `PROMPT.md`; the predictions were frozen before the first
run in `PREDICTIONS.md`; every result is in
`receipts/identification_dual.json`, which regenerates byte-identically,
with every node, edge, and single-pair probe in
`receipts/full/identification_dual_full.json.gz`, whose uncompressed
content regenerates identically and whose sha256 the summary records.

## Frozen inputs

- `PROMPT.md` sha256
  `a194961da50e2422bfe93a8ec907ddb2c791a022369e309df5f1dcdd12318d02`
- `PREDICTIONS.md` sha256
  `b5e066fca1cc262dfbef84db142a647c36d055bd887c0bf2f48084d180424e97`,
  written and hashed before the first computation, scored mechanically
  by `run_dual.py`, never edited.
- Sealed sources pinned as Git blobs at snapshot
  `f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` in `SOURCE_MANIFEST.json`;
  `verify_pins.py` checks them at HEAD and checks that the frozen texts
  have not moved.
- Declared bounds, unchanged from the seal: at most two items per
  response, form arity at most two, fifteen rounds, a pre-expansion node
  guard of two hundred and fifty.

## Terminals, each with its scope

- IDENTIFICATION_COSTS_ONE (FINITE_COMPUTATION, both readings of the
  sealed genesis, reading R).  The minimum identification response over
  every genesis state and every separated pair is one item: a single
  instance that fills the one context the other datum lacks, or a single
  uniform rule that makes the form distinguish nobody.  The sealed cost
  floor of two for the first separation does not dualise.  Across the
  19 genesis states the accepted minima number 290 edges; 222 of them
  cost one item and 68 cost two.
- RULE_ITEMS_DOMINATE (FINITE_COMPUTATION).  Of the 290 accepted minima,
  220 contain a uniform rule (164 rule alone, 34 rule with an instance,
  22 two rules); 58 are a single instance and 12 are two instances.  The
  item the sealed derivation proved never minimal for separation is the
  most common minimum for identification.  Under both sealed measures
  the trees are identical at every genesis state: no accepted minimum
  admits a form, so the arity term of mu2 never decides.
- THIRD_PARTY_EFFECT (FINITE_COMPUTATION, countermodel to locality).
  208 of the 290 accepted minima change the profile of a datum outside
  the target pair.  With a binary form, filling in an instance on one
  datum gives the datum it is related to a new context; with a rule, every
  datum gains every context of that form.  Identification is not local.
- PROGRESS_AND_CLOSURE (FINITE_COMPUTATION within bounds).  In reading R
  no node of any tree ends without a response, no tree is cut by the
  round bound or the node guard, and every maximal branch reaches the
  all-collapsed fixpoint in at most n minus one identification rounds
  (one round at two data, at most two rounds at three data).  Collapse is
  an equivalence, so the class count falls by at least one per accepted
  round; the general bound is stated in `CLAIM_LEDGER.md` as a
  conjecture with that argument and no Lean.
- REVERSAL_COSTS_TWO (FINITE_COMPUTATION).  At every reading-R fixpoint,
  re-separating any collapsed-pair orbit costs exactly two items, every
  minimum admits a fresh form, and no minimum instantiates a form that
  carries a uniform rule.  548 orbits priced.  A flooded form is dead for
  separation, as the sealed `separable_of_subrules` says; the dual shows
  the same for a saturated one.
- PERSISTENCE_BLOCKS (FINITE_COMPUTATION, reading P).  With the sealed
  separation requirements standing, every one of the 38 reading-P trees
  is terminal without a response at its root: the closure policy demands
  identification of a required pair and no delta within bounds both
  collapses and separates it.  Every pair that carries a standing
  separation refuses identification.  The single-pair probe adds the
  finding the prediction missed: some pairs whose separation was never
  required ALSO refuse within two items, because every fill that would
  identify them changes a required pair through the binary form they
  share.  See P6 below.
- ACCUMULATION_UNDER_THE_SWITCH (FINITE_COMPUTATION, guard-cut).  In
  every alternating run no fresh datum is ever admitted, the count of
  forms carrying a uniform rule never falls along an edge, and the
  largest form count reached exceeds the genesis form count in every run
  (from two forms at genesis to three, four, or five at the deepest
  nodes).  What the prediction got wrong is the fossil counter: a form
  exhausted by identification is as often saturated by instances as
  flooded by a rule, so the ruled-form count fails to rise across some
  cycle in 18 of the 38 runs (every mu2 run at a reading-F genesis, and
  all six reading-L runs).  See P8 below.  All 38 alternating trees are
  cut by the node guard or the round bound; nothing is claimed past the
  cut.
- NO_UNIQUENESS (FINITE_COMPUTATION).  184 of the 290 accepted edges sit
  in a tie of at least two non-isomorphic minimum classes, and ties
  between a single instance and a single rule occur.  Under the plain
  count, "adjust the two" and "abolish the distinction for everyone"
  are tied wherever both cost one.

## Predictions scored (mechanically, in the receipt)

| id | prediction | verdict | what the receipt shows |
|---|---|---|---|
| P1 | cost floor one | HIT | minimum one item at every genesis in reading R |
| P2 | cost-one minima are inst or rule; rule-alone exists | HIT | 164 rule-alone, 58 inst-alone under mu1 |
| P3 | third-party change at a three-datum genesis | HIT | 208 edges with a non-target profile change |
| P4 | progress in reading R | HIT | no terminal_no_response node |
| P5 | fixpoint within n minus one rounds | HIT | max two rounds at three data; no cut branch |
| P6 | persistence conflict, three clauses | MISS | clauses one and two hold; clause three fails: the never-required pair at seven binary-form fixpoints (g05, g07, g09, g11, g12, g14, g15) refuses within two items under both measures |
| P7 | reversal costs two with a fresh form | HIT | 548 orbits, all cost two, all fresh form, none on a ruled form |
| P8 | ruled forms rise every cycle; no fresh datum | MISS | monotone and datum-free everywhere; the rise fails where a form is saturated rather than flooded |
| P9 | ties, including inst versus rule | HIT | 184 tied edges; inst/rule ties present |
| P10 | mu1 and mu2 trees identical; no fresh form in a minimum | HIT | equal counts at all 19 genesis states |

The two misses are the substantive findings of the run, and they are
kept as misses.  P6 says identification under standing separations is
blocked beyond the required pairs: a never-required pair can be
unidentifiable within bounds because its only cheap fills disturb a
required pair through a shared binary form.  P8 says the right invariant
is exhaustion, not rule membership: the machine retires a distinction by
filling it in as readily as by making it universal.

## What this tree does not claim

- No theorem.  Every result above is a finite computation within the
  declared bounds or a countermodel; the general statements (cost floor
  one whenever one context differs; fixpoint within n minus one rounds;
  reversal needs a fresh form) are conjectures in the ledger with their
  arguments stated and no Lean.
- No endogenous generator.  The switch is a declared event, exactly as
  the sealed continuation policy is; the alternating runs show what a
  declared alternation produces within bounds and nothing about what it
  would produce past them.
- No reading of RequireSame beyond equal profiles.  Internal identity
  (same index) is not reachable by any admission event in the sealed
  grammar; a merge event would be a new primitive with its own price and
  is not proposed here.
- No claim about the sealed derivation.  Its results are consumed, not
  revised.

## Commands

From the repository root:

```text
python research/identification_dual/run_dual.py     # about five minutes
python research/identification_dual/verify_pins.py
```

From this directory:

```text
python -m unittest discover -s . -p "test_*.py"     # regenerates the receipt
python -m mypy
```

## Leftovers, named and executed nowhere

- A reach-weighted measure that prices a rule by the number of contexts
  it grants, so that "adjust the two" can be minimal where "abolish for
  everyone" is not.  Declared, not derived; not run.
- The general bound of n minus one rounds and the cost-one lemma, as
  Lean statements over the sealed `Basic` definitions.
- A merge event on the carrier, with its replay consequences.
