# Predictions, written and hashed before the first run

`AuthorityEffect: None`.  Each prediction carries its falsifier.  A missed
prediction is recorded next to its value in `STATUS.md` and never edited
here.  The sha256 of this file as frozen is recorded in `STATUS.md` and
pinned by `test_dual.py`.

- P1 (cost floor). In reading R, the minimum cost of an identification
  response over all genesis states and all separated pairs is one item.
  Falsifier: every valid response at some genesis costs two items.
- P2 (item kinds). In reading R under mu1, every accepted minimum of cost
  one is a single instance or a single uniform rule, and at least one
  accepted minimum is a rule alone.  Falsifier: an accepted cost-one
  minimum that is a fresh form or a fresh datum, or no rule-alone minimum
  anywhere.
- P3 (third-party effect). In reading R, at some genesis state with three
  admitted data, an accepted minimum response changes the profile of a
  datum outside the target pair.  Falsifier: every accepted response
  leaves every non-target profile unchanged.
- P4 (progress). In reading R, no node of any tree ends with a demand
  that has no valid response within bounds.  Falsifier: a
  terminal_no_response node in reading R.
- P5 (closure bound). In reading R, every maximal branch reaches the
  all-collapsed fixpoint in at most n minus one rounds, where n is the
  number of admitted data of its genesis state.  Falsifier: a branch
  needing n rounds or more, or a branch cut by the round bound.
- P6 (persistence conflict). In reading P, every genesis state has at
  least one demanded orbit with no valid response, so no reading-P tree
  reaches the all-collapsed fixpoint; and in the single-pair probe, a
  separated pair that is NOT among the standing separation requirements
  is identifiable within bounds while a pair that IS among them is not.
  Falsifier: a reading-P tree reaching the fixpoint, or a required pair
  with a valid identification, or a free pair without one.
- P7 (reversal). At every reading-R fixpoint, re-separating any collapsed
  pair costs exactly two items, and every minimum uses a fresh form,
  never a form carrying a uniform rule.  Falsifier: a cost-one
  re-separation, or a minimum that instantiates a ruled form.
- P8 (accumulation under the switch). In the alternating run, the number
  of forms carrying a uniform rule is non-decreasing along every branch
  and increases across every identify-to-separate cycle, and no fresh
  datum is ever admitted.  Falsifier: a branch where the ruled-form count
  falls, a cycle where it does not rise, or an admitted fresh datum.
- P9 (ties). In reading R under mu1, some demand has at least two tied
  minimum classes that are not isomorphic, and at least one such tie is
  between an instance-only response and a rule-only response.
  Falsifier: every demand has a unique minimum class, or no tie of that
  shape.
- P10 (measure insensitivity). In reading R, the mu1 and mu2 trees have
  identical node and edge counts at every genesis state, because no
  accepted identification minimum admits a new form.  Falsifier: any
  count differing, or an accepted minimum containing a fresh form.
