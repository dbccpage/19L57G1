# PROMPT: the identification demand on the sealed fixpoints

`AuthorityEffect: None`.  This file is the challenge.  It states no
expected value; every number in it is a bound or an index, spelled out,
so that a solver agreeing with this file is not evidence of anything.

## 0. Isolation

Use only this repository.  The sealed kernel is consumed read-only
through its public functions in `code/derivation/` (`model`, `observe`,
`candidates`, `iso`, `engine`), pinned by blob hash in
`SOURCE_MANIFEST.json`.  Nothing under the seal is modified.  No outside
theory is named or targeted; the demand below is stated in the kernel's
own vocabulary and nowhere else.

## 1. Genesis

The starting states are the all-pairs-separated fixpoints of the sealed
closed-system baselines (external continuation disabled), for both
admission readings and both sealed cost measures, quotiented by the
sealed isomorphism relation.  Each carries its replayable history from
the sealed genesis.  No starting state is constructed by hand.

## 2. The demand

The caller requires, of two admitted data that are internally separable
in the sealed declared sense, that they become internally
indistinguishable in that same sense: equal profiles.  Call the
requirement RequireSame(i, j).  It is an externally imposed requirement,
persistent like the sealed separation requirement, and it is recorded in
the history as a declared event.

## 3. Readings of persistence (both carried)

- Reading P: the sealed separation requirements standing at genesis
  remain in force.
- Reading R: a declared retraction event discards them at genesis.  The
  retraction is a declared metatheoretic act, priced as one event; it is
  not an object-language transition and nothing derives it.

## 4. Candidate space and measures

The sealed candidate grammar and bounds (at most two items per response;
form arity at most two), enumerated WITHOUT the sealed pruning lemmas,
which were proved for separation demands and are not assumed here.  The
sealed measures mu1 and mu2, unchanged.  A response is valid when the
augmented state collapses the target pair, keeps every earlier
RequireSame collapsed, and keeps every standing separation requirement
separated.

## 5. Procedure

For each genesis state, reading, and measure: enumerate every valid
response within bounds; take the minima; quotient by the isomorphism
relation extended to both requirement stores; retain every tied class;
replay every node from the sealed genesis before certifying it; continue
under the declared closure policy, one RequireSame per automorphism orbit
of separated pairs, to the fixpoint where no separated pair remains, or
to the declared bounds (fifteen rounds; a pre-expansion node guard of two
hundred and fifty).

## 6. The switch (declared)

Under a further declared policy, at a fixpoint the process retracts every
standing requirement, flips the demand kind (RequireSame to Separate, or
back), and continues under the same bounds.  The separate direction is
enumerated without the sealed pruning as well.  This switch is the only
new event kind in the tree.

## 7. Required answers, by computation, countermodel, or explicit OPEN

- the minimum cost of the first identification, per genesis state and
  reading;
- whether that minimum is unique up to isomorphism, per measure;
- which item kinds the minima use;
- whether an accepted response changes the profile of any datum outside
  the target pair;
- whether every demand has a response in reading R, and which demands
  have none in reading P;
- the number of rounds to the fixpoint on every maximal branch, against
  the number of admitted data;
- the cost and shape of re-separating a collapsed pair at a fixpoint;
- under the switch, what accumulates and what is admitted, within bounds.

## 8. Discipline

Every claim is classified.  The words minimal, unique, and complete are
used only within the declared bounds.  No receipt is a proof.
Predictions are frozen in `PREDICTIONS.md` before the first run, hashed,
scored, and never edited.
