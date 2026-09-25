# Admit-leftover status

## Boundary

Write root: `research/admit_leftover/`.

Prompt SHA-256:
`1a432270017e81c5963d78072f84c349fa366a1c2de875cec97c52794cd4eb62`.
Grammar-fit receipt SHA-256:
`133f12896a0d8ae819d5ceb780eb82a16127c9b922446a124b34d3adcea7b61b`.
The grammar-fit packet is a read-only input.  No sealed path or sibling
receipt is written.

The local reconstruction is labelled `METATHEORY` and uses only the
constructors listed in the receipt.  `admitWit` requires an asserted pair;
`protect` requires a retained witness; `declareObs` has no object ingredient.
No no-op is treated as a passage constructor.

## Leftover admissions

The collision's asserted pair `(0, 1)` is admitted with the named
`assertWit` constructor.  The post-admission state contains the pair and the
bill charges one atom.  The identifying map remains outside state because no
map-admission constructor is declared.

The residual comparison policy is not admitted.  It is an explicit
`COMPARISON_EXCLUDED` policy line, so the comparison remains open rather than
silently free.

## Profile computation

The non-trivial profile case is replayed from grammar-fit's history.  It
contains a unary form and an instance on datum 0.  The local one-hole
algorithm computes the rows from that state: datum 0 has the context and datum
1 does not.  The receipt checks that these computed rows equal the read-only
input rows; no row is written by hand.

## Search after choices

Each post-choice state is searched in four separate columns:

```text
object-derived state change: none
object-derived no-op label: profile context; residual p and q
external challenge: Impose(0, 1), supplied input, not applied
guarded response: admitWit is CONDITIONAL after assertWit; not fired
```

All no-op labels replay without changing state.  The conditional retained-
witness response is not endogenous and has its own unpaid bill line until an
explicit extra admission is made.  `protect` remains conditional on that
retained witness, and `declareObs` is not an object-derived response.

## Cost, orientation, and S9

The sole measure is `mu_leftover_admission`: one atom per chosen extra
admission.  The chosen `assertWit` costs one; no minimum or completeness claim
is made.  Orientation is inherited as an explicit atom from grammar-fit, the
ordered-pair keys differ under reversal, and both tied classes remain retained.

Replaying `Supply("<>")` separately leaves admitted data empty.  Its six S9
lines (`carrier`, `occurrences`, `relation`, `witness`, `irreflexivity`, and
`orientation`) are all unpaid.  The assertion history is not substituted for
that supply history.

## Protected opens and stop

```text
LEFTOVER_ADMITTED
LEFTOVER_LEFT_OUTSIDE
STATE_CHANGE_NOT_FOUND
LABEL_ONLY
GUARDED_CONDITIONAL
COMPARISON_EXCLUDED
ORIENTATION_PRICED
S9_BRIDGE_PRICED
TIES_RETAINED
OB1_UNCHANGED
S66_UNCHANGED
S9_LAST_UNCHANGED
CANDIDATE_SPACE_OPEN
REFUSED
```

OB-1, S6.6, S9's last bullet, the identifying map, comparison policy, and the
guarded family remain open.  Genesis `two_rule` is not fired; no clock or
successor is added.  The leftover is an unseated map, an unpaid comparison,
and an unfired guarded family.  They are leftovers, not defects.

## Local verification boundary

The bundled Python runtime passes byte compilation, receipt generation, and
the dependency-free direct harness.  A repository pytest/CI witness is not
claimed for this research tree.

2026-09-24: the ten checks in `test_admit_leftover.py` were plain
functions.  The direct harness (`python test_admit_leftover.py`) called
them, but `python -m unittest` collected none of them and reported "NO
TESTS RAN".  They are now methods of one `unittest.TestCase`, still
dependency-free, and the direct harness is `unittest.main()`.  A
`load_tests` guard adds a failing check when the collected count is not
ten, or when assertions are disabled.  All ten pass under the direct
harness, `python -m unittest`, and pytest.  No check changed and no claim
moved.
