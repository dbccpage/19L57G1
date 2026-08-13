# The interpreter boundary

Run: PR #12, Phase VIII.  Sources:
`lean4/Derivation/InterpreterBoundary.lean`,
`code/derivation/interpreter_boundary.py`,
`artifacts/primitive_interpreter.json`.  Grounding: the sealed
constitution machinery (`ConstitutionDesc`, `interpStep`,
`kernelDesc`, `allDescs`, `interp_describe`, `allDescs_complete`).

The prior run left one OPEN bridge: the family interpreter is not a
member of its own described family; the outermost interpretation
relation is metatheoretic.  This phase attacks that boundary along
the declared routes I0–I5 and returns two theorems, not a wish.

## I0 — fixed external interpreter (sealed status, restated)

Quotation (inert data), executable description (`interpStep d`), and
verified self-description (`interp_describe`) remain three separated
levels.  Nothing here was rewritten.

## I1 — every finite closure has a new top (THEOREM)

`tower_persists`: for ANY finite code list `cs : List C` and ANY
evaluation map `ev : C → World → Event → World`, there exists an
interpreter-grade function differing from every coded member.  The
construction is a finite diagonal: at the world whose carrier length
indexes code `c`, the diagonal extends the notes of `ev c`'s output
by one element, so it disagrees with `ev c` there.  No appeal to
infinity beyond the world type itself; the theorem is uniform in the
level, so *stacking towers does not help* — each finite closure
mints its next top.  Terminal: **INTERPRETER_TOWER_PERSISTS**.

## I2 — universal code and evaluator, in the declared class

`i2_universal_in_class`: `ConstitutionDesc` with `interpStep` covers
the declared 64-member family exactly (`allDescs_complete` +
`interp_describe`).  "Universal" is scoped to that class and no
further — I1 is precisely the reason no unscoped reading survives.

## I3 — partiality closes what totality cannot (THEOREM)

`evalOpt : Option ConstitutionDesc → World → Event → Option World`
adjoins one uncoded top that *refuses*: `evalOpt none = fun _ _ =>
none` (`i3_partial_top_refuses`) while covering the family on the
coded side (`i3_partial_covers`).  A total same-type top is
impossible (I1); a typed-refusal top is a two-line construction.
The boundary closes only by admitting refusal/partiality — refusal
again carrying the structural load, as everywhere in this
derivation.

## I4 — self-description without self-justification

`kernelDesc` is a description-level fixed point
(`interp_describe`).  `family_missed` (= `tower_persists` at
`allDescs`, `interpStep`) shows the family provably misses an
interpreter-grade function: there is no evaluation-level fixed point
in the family.  Recursion delivers self-description; it does not
deliver a self-justifying evaluator.

## I5 — the boundary IS a Primitive Difference (THEOREM)

The novel possibility, formalized and proved rather than narrated:

- `boundarySetting`: carrier `Option ConstitutionDesc` — the 64
  coded occurrences plus ONE uncoded occurrence (`none`, the
  interpreter role); the witnessed difference is the pair
  (kernel description, interpreter role), retained and protected as
  declared stores.
- `i5_boundary_is_A`, `i5_boundary_is_F`: the boundary satisfies the
  native kernel candidates A (pointed witnessed irreflexive
  relation) and F (protected retained PD).
- `i5_collapse_obstructed`: any presentation identifying the two
  endpoints loses irreflexivity in the pushforward — the collapse is
  obstructed under the protected law, exactly the passage's
  obstruction shape.
- `i5_difference_grounded`: the non-identification is *behaviorally
  grounded*, not notational — the diagonal (`family_missed`) shows
  no total same-type recoding absorbs the interpreter role into the
  coded occurrences.

Terminal: **INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE**.  The
residue at the boundary is not a defect to erase; it is the next
retained non-identification — the same object this whole derivation
began from, one level up.  The ladder invariant reaches the
metatheory: the description/interpretation distinction is the
dimension-raising difference of the interpreter tower, and its
"resolution" options are exactly the passage's: create structure (a
new top — I1 says this never terminates), or refuse (I3's typed
partial top), or terminalize (stop the tower).  Absolute no-outside
is NOT claimed; the operational scope is exactly the theorems above.

## Computation record

64 family members pairwise behaviorally distinct on the declared
six-probe basis; the diagonal verified to miss all 64 members at
their indexed worlds; a fake diagonal that copies a member is caught
by the negative test.  All in `primitive_interpreter.json`, byte
deterministic.
