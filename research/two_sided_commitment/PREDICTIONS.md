# Predictions, written and hashed before the first run

`AuthorityEffect: None`.  Each prediction carries its falsifier.  A missed
prediction is recorded next to its value in `STATUS.md` and never edited
here.  The sha256 of this file as frozen is recorded in `STATUS.md` and
pinned by `test_two_sided.py`.

- Q1 (both kinds, no flip).  Under parity and under residue_three, some
  run contains accepted responses to a same demand and to an apart
  demand, and the tree has no event that flips a demand kind, because
  none exists.  Falsifier: a run under either commitment in which only
  one demand kind is ever answered.
- Q2 (one response, several demands).  Some accepted response honours
  more than one open demand at once.  Falsifier: every accepted response
  leaves every other open demand open.
- Q3 (growth generates).  Under every commitment except total_same and
  chain-at-the-bound, every growth step from a demand-free state produces
  at least one demand; under total_same no growth step ever produces a
  demand, so the total_same tree is a single chain of growth steps.
  Falsifier: a growth step under parity, residue_three, or total_apart
  that produces no demand; or any demand under total_same.
- Q4 (supply is not a response).  No accepted minimum in any run admits a
  fresh datum.  Falsifier: an accepted minimum containing a fresh datum.
- Q5 (refusals exist).  Under parity or residue_three, at four or more
  admitted data, some demand has no valid response within two items,
  because every response that would honour it regresses a committed pair
  that was honoured.  Falsifier: no terminal_no_response node in those
  runs.
- Q6 (total_apart reproduces the seal).  Under total_apart, before the
  first growth step, the tree from each sealed genesis is the sealed
  closed baseline for that reading and measure, node for node.
  Falsifier: a difference in node count or leaf status before growth.
- Q7 (discharge within the count).  Under total_apart, after a growth
  step on n data, the demands are exactly n and are all honoured within n
  accepted rounds on every branch that does not refuse.  Falsifier: a
  branch needing more than n rounds.
- Q8 (measure sensitivity).  Under total_apart the mu1 and mu2 trees
  differ in node count from the same genesis, because separation minima
  admit forms and the arity term decides; under total_same they are
  identical.  Falsifier: equal counts under total_apart, or unequal under
  total_same.
