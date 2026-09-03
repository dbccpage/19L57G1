# two_sided_commitment: one stake and a stream

`AuthorityEffect: None`.  This tree records; it does not certify.

The sealed derivation takes one demand kind from outside, one demand per
round.  The sibling `identification_dual` showed the machine can regenerate
its own work by flipping the demand kind at a fixpoint, under a declared
switch.  The open pull request `standing_commitment` proves that one
standing declaration makes growth generate separation demands with no act
in between.  This rung joins the two: a **two-sided standing commitment**,
declared once over every pair of datum indices present or future (apart,
same, or free), and **growth** as the only external event after the
declaration.  Both demand kinds are read off the state; no event flips a
demand kind, because the grammar has none.  The challenge is `PROMPT.md`;
the predictions were frozen before the first run in `PREDICTIONS.md`;
every result is in `receipts/two_sided_commitment.json`, which regenerates
byte-identically, with every node and edge in
`receipts/full/two_sided_commitment_full.json.gz`, whose uncompressed
content regenerates identically and whose sha256 the summary records.

## Frozen inputs

- `PROMPT.md` sha256
  `d96cab6efc4c89ee99dda4e7f911325e5e14b4b554444943834e0e1e914a028d`
- `PREDICTIONS.md` sha256
  `b9dea8cea62749321422da6b1ba01f76dc1af16624d9e8d5ea44e6338f46e333`,
  written and hashed before the first computation, scored mechanically by
  `run_two_sided.py`, never edited.
- Sealed sources and the sibling `research/identification_dual/dual.py`
  pinned as Git blobs at snapshot
  `7fcd72f618e676a88df65efed4926ac3c11eacbe` in `SOURCE_MANIFEST.json`;
  `verify_pins.py` checks them at HEAD and checks that the frozen texts
  have not moved.
- Declared bounds: the sealed grammar and measures; at most two items per
  response; form arity at most two; fifteen rounds; a pre-expansion node
  guard of two hundred and fifty; at most five admitted data.  Five
  commitments, declared in `PROMPT.md` by rule on indices.

## Terminals, each with its scope

- BOTH_KINDS_FROM_ONE_STAKE (FINITE_COMPUTATION).  Under parity and under
  residue_three, every one of the eight runs answers same demands and
  apart demands in the same tree, from the declaration and growth alone.
  The grammar carries no flip event, and the receipt records that as a
  count of zero.  The sibling's declared switch is not needed once the
  stake is two-sided.
- ONE_RESPONSE_SEVERAL_DEMANDS (FINITE_COMPUTATION).  94 accepted
  responses honour two or more open demands at once (16 under parity, 68
  under residue_three, 6 under chain, 4 under total_apart): a mark that
  separates a datum from its two neighbours, or a fill that identifies a
  datum with its class and separates it from the others in one item.
- SUPPLY_IS_NOT_A_RESPONSE (FINITE_COMPUTATION, within bounds).  No
  accepted minimum in any of the 20 trees admits a fresh datum, although
  the enumeration is unpruned and offers one at every state.  Under a
  no-regress validity a fresh datum never helps: a held pair is honoured
  or regressed by instances on held data, and a fresh datum only adds
  demands of its own.  Supply stays a stream.
- GROWTH_GENERATES_AT_MOST_ONE (FINITE_COMPUTATION, countermodel to the
  per-growth count).  Under total_apart, growth from a demand-free state
  produces at most one demand and sometimes none, never n.  The reason is
  exact: a demand-free state under total_apart separates every held pair,
  so at most one held datum has the empty profile, and the fresh datum,
  which has the empty profile, collapses with that datum alone.  The
  sibling's count of n demands per growth step is a theorem about the
  viewless state and does not carry to a state that has already answered.
  See Q3 and Q7 below.
- TOTAL_SAME_IS_A_CHAIN (FINITE_COMPUTATION).  Under total_same no state
  ever carries a demand and every tree is a single chain of growth steps
  to the data bound: a stake with nothing to keep apart generates
  nothing, however much the state grows.
- THE_SEALED_BASELINE_IS_ASYMMETRIC (FINITE_COMPUTATION, countermodel to
  the expectation that total_apart reproduces the seal).  Before the first
  growth step, the reading-L trees under total_apart are the sealed closed
  baselines node for node (4 nodes with 3 demand-free under mu1, 2 with 1
  under mu2).  The reading-F trees are not: 13 nodes with 10 demand-free
  under mu1 against the seal's 20 with 16, and 3 with 1 against 4 with 1
  under mu2.  The seal's store records which pair was demanded first, so a
  link to the never-demanded datum is a class of its own there; under a
  stake that names every pair apart the three data are symmetric and those
  classes merge.  The seal's 16 terminals for reading F are in part a
  consequence of the order in which demands arrived.  See Q6 below.
- REFUSALS_AT_FOUR_DATA (FINITE_COMPUTATION).  Under residue_three, 152
  demands have no valid response within two items, all at four or five
  data, and under parity two do, at three and four data.  Every refusal is
  a same demand: identifying two data of one residue class regresses an
  apart pair they share a form with, and no two-item response avoids it.
  This is the sibling's P6 finding, now arising from a single stake rather
  than from a retained separation store.
- MEASURE_SENSITIVITY (FINITE_COMPUTATION).  Under total_apart the mu1
  and mu2 trees differ at both readings (230 against 8 nodes from reading
  L, 227 against 7 from reading F): separation minima admit forms, the
  arity term decides, and mu1 retains every tied arity.  Under total_same
  they are identical (4 and 4; 3 and 3).  The chain runs under mu1 hit the
  node guard; under mu2 they are seven nodes.
- THIRD_PARTY_EFFECT (FINITE_COMPUTATION).  302 accepted responses under
  total_apart, 261 under chain, 226 under residue_three, and 3 under parity
  change the profile of a datum outside the answered pair.

## Predictions scored (mechanically, in the receipt)

| id | prediction | verdict | what the receipt shows |
|---|---|---|---|
| Q1 | both kinds, no flip | HIT | all eight parity and residue_three runs answer both kinds; zero flip events |
| Q2 | one response, several demands | HIT | 94 such responses |
| Q3 | growth generates under total_apart, parity, residue_three; total_same silent | MISS | total_same silent and chain-shaped as predicted; but under all three generating stakes some growth step produces no demand |
| Q4 | supply is not a response | HIT | zero accepted minima with a fresh datum |
| Q5 | refusals at four or more data | HIT | 153 refusals at four or five data under parity and residue_three |
| Q6 | total_apart reproduces the seal before growth | MISS | reading L matches node for node; reading F quotients 20 to 13 and 4 to 3 |
| Q7 | growth on n data yields n demands, honoured within n rounds | MISS | at most one demand per growth step; the rounds clause holds trivially |
| Q8 | mu1 and mu2 differ under total_apart, agree under total_same | HIT | 230 against 8, 227 against 7; 4 and 4, 3 and 3 |

The three misses are the findings of the run.  Q3 and Q7 fall together:
a state that has already answered its demands keeps at most one viewless
datum, so the sibling's growth count is a statement about genesis and not
about the process in flight.  Q6 says the sealed reading-F baseline owes
part of its branching to the order of arrival of its demands, which a
standing stake does not have.

## What this tree does not claim

- No theorem.  Every result above is a finite computation within the
  declared bounds or a countermodel; the general statements are
  conjectures in `CLAIM_LEDGER.md` with their arguments and no Lean.
- Nothing about growth as a response.  The bounds admit two items, so a
  fresh datum with one instance was in the candidate space at every state
  and was never minimal; a bound of three items was not run.
- No endogenous generator.  The stake is declared and growth is supplied.
  What the run shows is that with those two inputs no third is needed for
  either demand kind; it does not make either of the two derived.
- Nothing past the node guard, which the chain runs under mu1 reach.

## Commands

From the repository root:

```text
python research/two_sided_commitment/run_two_sided.py     # under a minute
python research/two_sided_commitment/verify_pins.py
```

From this directory:

```text
python -m unittest discover -s . -p "test_*.py"     # regenerates the receipts
python -m mypy
```

## Leftovers, named and executed nowhere

- The three-item bound, to see whether a fresh datum with two instances
  is ever minimal where every two-item response regresses.
- The reach-weighted measure from the sibling, unchanged.
- Lean for the at-most-one growth count under total_apart at a
  demand-free state, and for the no-regress refusal shape.
- A commitment declared over profiles rather than indices, so that the
  stake reads what the state can see and not the metatheory's numbering.
