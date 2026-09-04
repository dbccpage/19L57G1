# PREDICTIONS — SECOND STAKE

`AuthorityEffect: None`.

Frozen on 2026-09-04 before any rung computation and before any rung Lean
build.  Every row is PREDICTION evidence unless explicitly marked as a
DEFINITION or DECLARED_POLICY.  A miss is retained beside the computed value.

## First freeze: observables

The following six observables are DECLARED_POLICY for this finite rule class.
They are functions of a sealed `Regime` and are required to commute with datum
and form renaming before a rule using them can be called invariant.

| id | observable | value |
|---|---|---|
| O1 | profile equality | whether the two held data have equal profiles |
| O2 | profile emptiness | whether each held datum has an empty profile |
| O3 | profile size | the cardinality of each held datum's profile |
| O4 | pair-orbit membership | whether one regime automorphism sends one member of the unordered pair to the other |
| O5 | class count | the number of distinct profiles in the regime |
| O6 | requirement pattern | whether the unordered pair is in the admitted requirement store |

## First freeze: declared menu and capability counts

The nine-member menu below is DECLARED_POLICY.  Its size and capability
counts are dated 2026-09-04.  A capability count is the number of distinct
observables read.  Every member is total from a regime and a held unordered
pair to `apart`, `same`, or `free`.

| member | rule | observables | capability count |
|---|---|---|---:|
| E1 | `same` exactly when profiles are equal; otherwise `apart` | O1 | 1 |
| E2 | `same` exactly when both profiles are empty; otherwise `apart` | O2 | 1 |
| E3 | `same` exactly when the pair is in one orbit; otherwise `apart` | O4 | 1 |
| E4 | `apart` exactly when the pair is in one orbit; otherwise `same` | O4 | 1 |
| E5 | `apart` exactly when profile sizes differ; otherwise `same` | O3 | 1 |
| E6 | `same` exactly when the pair is in one orbit and profile sizes are equal; otherwise `free` | O3, O4 | 2 |
| E7 | `apart` exactly when one and only one profile is empty; otherwise `free` | O2 | 1 |
| E8 | `apart` exactly when the pair occurs in the requirement pattern; otherwise `free` | O6 | 1 |
| E9 | `same` exactly when the class count is one; otherwise `apart` | O5 | 1 |

The five sibling rules `total_apart`, `total_same`, `parity`,
`residue_three`, and `chain` are DECLARED_POLICY controls run through the
same finite machine.  The first two are constant functions and therefore do
not read their index arguments extensionally.  The last three read index
values.  This distinction follows from the pinned definitions and overrides
the supplied packet's description of all five as index-reading, because the
seed's rule definition is extensional.

## First freeze: rectangle

The rectangle is DECLARED_POLICY, dated 2026-09-04:

- both sealed genesis readings, `L` and `F`;
- both sealed measures, `mu1` and `mu2`;
- unpruned deltas of at most two items and forms of arity at most two;
- no-regress response validity, recomputed against every previously honoured
  labelled pair;
- growth to at most four held data;
- at most fifteen accepted response rounds;
- a pre-expansion node guard of two hundred fifty per tree;
- exact canonical regime keys cross-checked against brute force on every
  reached regime within the permutation budget.

Any count at the guard is reported as guarded rather than complete.  Every
statement containing `never` is scoped to this rectangle.

## First freeze: invariance predictions

| id | subject | prediction | status label | falsifier |
|---|---|---|---|---|
| P-I1 | E1–E9 | every member commutes with every datum and form renaming in the rectangle | NOT FORCED; CHECKED expected | one reached regime, pair, and bijection whose label changes after transport |
| P-I2 | `total_apart`, `total_same` | both commute with every renaming because they are constant | FORCED by definition | any pair and renaming with unequal labels |
| P-I3 | `parity`, `residue_three`, `chain` | each is REFUTED by a datum renaming in the rectangle | NOT FORCED | exhaustive search finds no refuting bijection for one control |
| P-I4 | `controls_refuted` | OPEN because the two constant controls cannot be refuted by renaming | FORCED by definition | a valid refuting renaming for either constant control |

## First freeze: generation predictions

Kinds mean kinds of demands answered by accepted response edges.  Each value
is scoped to the declared rectangle.

| id | member | predicted kinds | re-labelling prediction | status label | falsifier |
|---|---|---|---|---|---|
| P-G1 | E1 | none | none | FORCED: the rule labels each pair by its current honour condition | any demand or any old-pair label change |
| P-G2 | E2 | apart only | none | NOT FORCED | no apart response, any same response, or any old-pair label change |
| P-G3 | E3 | both | at least one | NOT FORCED | either kind absent or no old-pair label change |
| P-G4 | E4 | both | at least one | NOT FORCED | either kind absent or no old-pair label change |
| P-G5 | E5 | same only | at least one | NOT FORCED | no same response, any apart response, or no old-pair label change |
| P-G6 | E6 | same only | at least one | NOT FORCED | no same response, any apart response, or no old-pair label change |
| P-G7 | E7 | none | at least one | FORCED for no demands; NOT FORCED for re-labelling | any demand, or no old-pair label change for the second clause |
| P-G8 | E8 | none | none | FORCED under the pinned no-regress validity | any requirement-labelled collapsed pair or any old-pair label change |
| P-G9 | E9 | apart only | at least one | NOT FORCED | no apart response, any same response, or no old-pair label change |

P-G10 is NOT FORCED: at least one invariant menu member generates both kinds
within the rectangle.  It is falsified when no member both passes the
renaming check and has accepted responses of both kinds.

P-G11 is NOT FORCED: at least one pair of distinct menu members produces
isomorphic trees for every reading and measure in the rectangle.  It is
falsified when every member has a distinct four-tree signature.

## First freeze: input-count branch

P-C1 is NOT FORCED: the declared-input count remains two.  A rule class is a
declaration; a surviving member does not lower the count.  This prediction is
falsified only by a theorem forcing one member from the grammar or by a proof
that exactly one member survives up to the declared tree isomorphism.

Both terminal branches are pre-agreed as DECLARED_POLICY.  If a checked
invariant member generates both kinds, record `STAKE_READ_OFF_STATE`; if none
does, record `NO_ENDOGENOUS_STAKE_IN_MENU`.  In either branch record
`INPUT_COUNT_STATED` with the value and its proof status.

## First freeze: extrapolation X

X is PREDICTION evidence and is NOT FORCED: every member surviving at the
four-data rectangle survives when the data bound is raised to five while all
other bounds remain fixed.  A member fails X if its five-data run is refuted
by renaming or loses its four-data generation disposition.  Challenge three
scores X before using any survivor.  This rung does not compute the five-data
rectangle.  The choice of five resolves the packet's internal conflict:
stage one requires the first rectangle to reach at least four data, while X
must concern the next data count not computed before this freeze.
