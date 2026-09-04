# PROMPT: one stake and a stream

`AuthorityEffect: None`.  This file is the challenge.  It states no
expected value; every number in it is a bound or an index, spelled out.

## 0. Isolation

Use only this repository.  The sealed kernel is consumed read-only
through its public functions in `code/derivation/`, and the sibling
research tree `research/identification_dual/` is consumed read-only for
its state, validity, and isomorphism apparatus; all are pinned by blob
hash in `SOURCE_MANIFEST.json`.  Nothing under the seal and nothing in
a sibling tree is modified.  No outside theory is named or targeted.

## 1. The stake

A two-sided standing commitment is a condition declared once over every
pair of datum indices, present or future, assigning each pair exactly
one of: apart, same, or free.  It emits nothing and reads no state.  The
demands of a state are the committed pairs among the data it holds that
the state does not yet honour: an apart pair whose profiles are equal,
or a same pair whose profiles differ.  Demands are read off the state;
nothing emits them.  The commitment is the only declaration of the
process besides the bounds.

Five commitments are declared, by name and by rule on indices:

- total_apart: every pair apart;
- total_same: every pair same;
- parity: pairs of equal index parity same, pairs of unequal parity
  apart;
- residue_three: pairs with equal index residue modulo three same, all
  other pairs apart;
- chain: consecutive indices apart, every other pair free.

## 2. The stream

Growth is the admission of one fresh opaque datum, supplied from outside.
It is the only external event after the declaration.  Growth happens
exactly when the state carries no demand, and only while the number of
admitted data is below the declared data bound.

## 3. Responses

The sealed candidate grammar and bounds (at most two items; form arity
at most two), enumerated without the sealed pruning lemmas, under the
sealed measures mu1 and mu2.  A response to a demand is valid when the
augmented state honours the demanded pair and honours every committed
pair among the previously held data that the state honoured before the
response.  Nothing else is required of it; other open demands stay open.

## 4. Procedure

From each sealed genesis (both admission readings), for each commitment
and each measure: read the demands; take one representative per
automorphism orbit of the demanded pairs, automorphisms being those of
the regime that preserve the commitment's labels on the held data;
enumerate every valid response within bounds; take the minima; quotient
by the isomorphism of regime and held-pair labels; retain every tied
class; replay every node from the sealed genesis; at a state with no
demand, grow; stop at the declared bounds (fifteen rounds, a
pre-expansion node guard of two hundred and fifty, at most five admitted
data) or when a demand has no valid response.

## 5. Required answers, by computation, countermodel, or explicit OPEN

- whether demands of both kinds arise in one run from the stake and the
  stream alone, with no event that flips a demand kind;
- whether one response can honour several demands at once;
- whether growth ever fails to produce a demand under a non-empty stake;
- whether any accepted minimum admits a fresh datum, that is, whether
  supply is ever a response rather than a stream;
- which demands, if any, have no valid response within bounds, and why;
- how the two sealed measures differ, if they differ.

## 6. Discipline

Every claim is classified.  The words minimal, unique, and complete are
used only within the declared bounds.  No receipt is a proof.
Predictions are frozen in `PREDICTIONS.md` before the first run, hashed,
scored, and never edited.
