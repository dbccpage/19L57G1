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
the declared routes I0–I5.  Review-pass scoping: the two headline
results are an extensional incompleteness theorem and a
declared-model theorem; the identification of the boundary with a
Primitive Difference is retained as a FRONTIER CONJECTURE with its
missing theorem stated exactly.

## I0 — fixed external interpreter (sealed status, restated)

Quotation (inert data), executable description (`interpStep d`), and
verified self-description (`interp_describe`) remain three separated
levels.  Nothing here was rewritten.

## I1 — finite code families are extensionally incomplete (THEOREM)

`tower_persists`: for ANY finite code list `cs : List C` and ANY
evaluation map `ev : C → World → Event → World`, there exists a
function of the same type differing from every coded member.  The
construction is a finite diagonal: at the world whose carrier length
indexes code `c`, the diagonal extends the notes of `ev c`'s output
by one element, so it disagrees with `ev c` there.  The theorem is
uniform in the level, and recoding the missed function yields a new
finite family to which it applies again.

Exact scope (review pass): the diagonal differs only at the
operationally inert notes field.  This proves
**FINITE_CODE_FAMILY_NOT_EXTENSIONALLY_COMPLETE** — a finite family
does not enumerate the function type — and nothing more.  It does
NOT prove that no self-interpreter exists, NOT that the evaluator
cannot be coded, NOT that every interpreter hierarchy has a new
*semantic* top, and NOT that self-evaluation is impossible: a finite
family may well contain a code for its own evaluator without
containing every function of the evaluator's output type.  By the
repository's own operational standard, a difference affecting no
accessible operational verdict carries no operational authority.

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

## I5 — a declared boundary model satisfies A and F (THEOREM);
the identification is a FRONTIER CONJECTURE

The novel possibility, formalized at the model level:

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
- `i5_difference_grounded`: reuses `family_missed` (extensional
  incompleteness).  Review-pass scope: the reused witness differs
  only at the inert notes field, so this grounds the
  non-identification EXTENSIONALLY, not operationally — see the
  frontier conjecture below for what operational grounding would
  require.

Terminal: **DECLARED_BOUNDARY_MODEL_SATISFIES_A_AND_F**.  Exact
scope: `boundarySetting`'s relation, retention, and protection are
inserted BY DEFINITION; no theorem identifies the uncoded occurrence
`none` with the diagonal's missed function, interprets `none` as
that function, or derives the boundary relation from interpretation
behavior.  What `i5_difference_grounded` reuses is
`family_missed` — extensional incompleteness — whose witness
differs only at the inert notes field.

**FRONTIER CONJECTURE (retained):
INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE.**  The reading — the
description/interpretation distinction as the next retained
non-identification, its resolution options exactly the passage's
(create a new top, refuse via the typed partial top, or terminalize)
— is coherent and potentially important, and it is NOT proved by
the notes-diagonal.  The missing theorem is a denotational bridge
connecting: code, interpretation, lawful interpreter behavior, the
uncoded evaluator role, and an OPERATIONALLY EFFECTIVE
non-identification (one whose collapse changes an accessible
operational verdict).  Until that bridge exists, the conjecture
stays in this section.  Absolute no-outside is NOT claimed either
way.

## Computation record

64 family members pairwise behaviorally distinct on the declared
six-probe basis; the diagonal verified to miss all 64 members at
their indexed worlds; a fake diagonal that copies a member is caught
by the negative test.  All in `primitive_interpreter.json`, byte
deterministic.
