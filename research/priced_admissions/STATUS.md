# Priced admissions status

## Boundary

Write root: `research/priced_admissions/`.

The run records the sealed paths in the receipt and reports an empty mutation
list.  The existing thinghood prompt and receipt are read-only inputs.  The
local Python module reconstructs event names as metatheory; it imports no
sealed implementation.

Prompt SHA-256: `4914cd2a087437830ab5119c25338e4a82cca883a42c555aa32d63906cb6e1ef`.

## Built objects

1. `collision`: carrier `(0, 1)`, edge `(0, 1)`, asserted pair `(0, 1)`,
   identifying map `(0, 0)`, and an irreflexive law that fails after the map.
2. `equal_profiles`: two data, one unary form, no instances, one concrete
   hole-context, and two equal empty profiles.
3. `directional_residual`: one directed edge with presentations `p=(0,0)`
   and `q=(0,1)`; `p` identifies and `q` separates the residual pair.

These are concrete data records.  The receipt also records what each state
does not contain.

## Event search

The search constructs the local `Admit`, `Supply`, `Impose`, `Observe`, and
guarded passage constructors from the existing names.  `Impose` candidates
are recorded in a separate external-challenge column and never set the
object-level `next_event_found` field.  An object-level event is reported only
when its payload is a field of that object: the equal-profile context yields
one `Observe` event, and the two residual presentation maps yield `Observe("p")`
and `Observe("q")`.  The collision therefore has no object-derived next event;
its asserted pair and identifying map are explicitly recorded as fields
outside the reconstructed grammar state.

The guarded response family has no candidate in the current state because
retained witness, protection, and a declared observation/closure path are not
all present.  The no-payload `declareObs` constructor is shown separately as a
grammar offer, never counted as an object-derived event.

The resulting terminals are:

```text
THREE_OBJECTS_BUILT
NEXT_EVENT_FOUND          # object-derived Observe scope only
NEXT_EVENT_NOT_FOUND     # guarded response scope
REFUSED                   # genesis two_rule and table-as-computation
```

## Orientation and finite minimum

Orientation is included as its own one-atom bill line.  The canonical key
retains the ordered asserted pair.  In the named finite space (carrier at
most 3, at most 3 directed edges, six named laws), the un-oriented baseline
cost is 7 and the oriented minimum cost is 8.  The oriented minimum retains
two non-isomorphic law-bearing classes (`irreflexive` and `asymmetric`).
The law list is not enlarged; laws outside it remain `OPEN`.

Terminals:

```text
ORIENTATION_PRICED
TIES_RETAINED
CANDIDATE_SPACE_OPEN
```

## S9 bill

The six lines are `carrier`, `occurrences`, `relation`, `witness`,
`irreflexivity`, and `orientation`.  Replaying the inscription plus
`Supply("<>")` leaves the admitted data empty, so every line is unpaid.

Terminal:

```text
S9_BRIDGE_PRICED
```

## Protected opens

```text
OB1_UNCHANGED
S66_UNCHANGED
S9_LAST_UNCHANGED
```

No closure terminal is issued for any of these surfaces.  The leftover is the
unpriced comparison policy and every candidate outside the named finite
space.  This run stops there.
