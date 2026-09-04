# two_sided_commitment: one stake and a stream

`AuthorityEffect: None`.  This tree records; it does not certify.

The sealed derivation takes one demand kind from outside, one demand per
round.  The sibling `identification_dual` showed the machine can regenerate
its own work by flipping the demand kind at a fixpoint, under a declared
switch.  The sibling `standing_commitment` worktree, open when this rung's
inputs were frozen, showed by finite computation that one standing
declaration makes growth generate separation demands with no act in
between.  This rung joins the two: a **two-sided standing commitment**,
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

## Quotient repair

The first receipt used the sibling's current labelled-state canonical key
as the operational key and selected one demanded pair per current
automorphism orbit.  That quotient was unsound for these index-defined
commitments.  A chain reversal has the same current canonical key, but after
both states receive the same fresh-datum event their canonical keys differ:
the commitment attaches the new index to different old indices.  The
operational key now retains the exact indexed regime alongside the canonical
diagnostic component, and every indexed demand is retained.  The earlier
counts are withdrawn; all counts below are from the repaired replay.

## Terminals, each with its scope

- BOTH_KINDS_FROM_ONE_STAKE (FINITE_COMPUTATION).  Under parity and under
  residue_three, every one of the eight runs answers same demands and
  apart demands in the same tree, from the declaration and growth alone.
  The grammar carries no flip event, and the receipt records that as a
  count of zero.  The sibling's declared switch is not needed once the
  stake is two-sided.
- ONE_RESPONSE_SEVERAL_DEMANDS (FINITE_COMPUTATION).  215 accepted
  responses honour two or more open demands at once (34 under parity, 127
  under residue_three, 18 under chain, 36 under total_apart): a mark that
  separates a datum from its two neighbours, or a fill that identifies a
  datum with its class and separates it from the others in one item.
- SUPPLY_IS_NOT_A_RESPONSE (FINITE_COMPUTATION, within bounds).  No
  accepted minimum in any of the 20 trees admits a fresh datum, although
  the enumeration is unpruned and offers one at every state.  The proposed
  general no-regress explanation remains a conjecture (TS-15); this run
  establishes only the bounded absence.  Supply stays a stream within the
  declared candidate space.
- GROWTH_GENERATES_AT_MOST_ONE (FINITE_COMPUTATION, countermodel to the
  per-growth count).  Under total_apart, growth from a demand-free state
  produces at most one demand and sometimes none, never n.  The proposed
  general explanation -- that a demand-free total-apart state has at most
  one empty profile for the fresh datum to match -- remains conjectural
  (TS-14); the receipt establishes the bounded count.  The
  sibling's count of n demands per growth step is a theorem about the
  viewless state and does not carry to a state that has already answered.
  See Q3 and Q7 below.
- TOTAL_SAME_IS_A_CHAIN (FINITE_COMPUTATION).  Under total_same no state
  ever carries a demand and every tree is a single chain of growth steps
  to the data bound: a stake with nothing to keep apart generates
  nothing, however much the state grows.
- THE_SEALED_BASELINE_IS_NOT_REPRODUCED (FINITE_COMPUTATION, countermodel
  to the expectation that total_apart reproduces the seal).  Before the
  first growth step none of the total-apart trees matches the sealed closed
  baseline.  Reading L has 7 against 4 nodes under mu1 and 3 against 2 under
  mu2; reading F has 64 against 20 and 10 against 4.  The two constructions
  impose different demand and quotient policies, so the discrepancy is not
  evidence that either receipt is wrong.  See Q6 below.
- REFUSALS_AT_FOUR_DATA (FINITE_COMPUTATION).  Fifteen demanded targets
  have no valid response within two items: twelve under residue_three at
  four data, and three under parity at three or four data.  Fourteen are at
  four data.  Every refusal is
  a same demand: identifying two data of one residue class regresses an
  apart pair they share a form with, and no two-item response avoids it.
  This is the sibling's P6 finding, now arising from a single stake rather
  than from a retained separation store.
- MEASURE_SENSITIVITY (FINITE_COMPUTATION).  Under total_apart the mu1
  and mu2 trees differ at both readings (254 against 85 nodes from reading
  L, 251 against 112 from reading F): separation minima admit forms, the
  arity term decides, and mu1 retains every tied arity.  Under total_same
  they are identical (4 and 4; 3 and 3).  Six mu1 trees hit the node guard:
  both readings for total_apart, residue_three, and chain.
- THIRD_PARTY_EFFECT (FINITE_COMPUTATION).  274 accepted responses under
  total_apart, 230 under chain, 246 under residue_three, and 8 under parity
  change the profile of a datum outside the answered pair.

## Predictions scored (mechanically, in the receipt)

| id | prediction | verdict | what the receipt shows |
|---|---|---|---|
| Q1 | both kinds, no flip | HIT | all eight parity and residue_three runs answer both kinds; zero flip events |
| Q2 | one response, several demands | HIT | 215 such responses |
| Q3 | growth generates under total_apart, parity, residue_three; total_same silent | MISS | total_same silent and chain-shaped as predicted; but under all three generating stakes some growth step produces no demand |
| Q4 | supply is not a response | HIT | zero accepted minima with a fresh datum |
| Q5 | refusals at four or more data | HIT | 14 refusals at four data under parity and residue_three; one additional parity refusal occurs at three data |
| Q6 | total_apart reproduces the seal before growth | MISS | none match: L is 7 against 4 and 3 against 2; F is 64 against 20 and 10 against 4 |
| Q7 | growth on n data yields n demands, honoured within n rounds | MISS | at most one demand per growth step; the rounds clause holds trivially |
| Q8 | mu1 and mu2 differ under total_apart, agree under total_same | HIT | 254 against 85, 251 against 112; 4 and 4, 3 and 3 |

The three misses are the findings of the run.  Q3 and Q7 fall together:
a state that has already answered its demands keeps at most one viewless
datum, so the sibling's growth count is a statement about genesis and not
about the process in flight.  Q6 says only that the standing-stake and
sealed constructions, with their different demand and quotient policies,
do not have the same bounded pre-growth tree.

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
- Nothing past the node guard.  Both readings of total_apart,
  residue_three, and chain reach it under mu1.

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
