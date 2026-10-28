# interpreter_verdict

AuthorityEffect: None. Outside the seal. Consumes the sealed `Derivation`
package read-only (`lean/lakefile.toml` requires `../../../lean4`) and
changes nothing in it. First built against `fc6349e`, core Lean 4.33.0.

Question: is the interpreter boundary of `Derivation/InterpreterBoundary.lean`
a primitive difference, or only declared to be one?

That module's `boundarySetting` puts the 64 codes and one uncoded occurrence
(`none`, the interpreter role) on one carrier and asserts the pair (kernel
code, interpreter role) by definition; `i5_boundary_is_A` holds because the
relation is inserted, and `openDenotationalBridge` records what is missing:
a meaning for `none` fixed by a law rather than chosen
(`arbitrary_uncoded_assignment` shows that any step function can be assigned
to `none` with every coded member unchanged, so a free choice proves nothing),
and a proof that identifying `none` with a coded member changes an accessible
operational verdict, not only an inert field. This tree closes both halves
for the quiescence verdict, with the exact scope below.

## The meaning of the uncoded role

A *reflective world* is a world together with the code it runs under
(`RWorld := ConstitutionDesc × World`; the code is carried as data, as the
sealed module already carries it). Two laws, both already named in the sealed
module's tags, are stated as predicates on reflective steps:

- interpretation (`Interprets g`): on a world carrying code `c`, the world
  part of `g` does what `c` means, `interpStep c`;
- quotation (`Quotes g`): the carried code is inert data.

Exactly one reflective step satisfies both (`lawful_unique`): `rstep`, "run
the code the world carries". That is the meaning given to `none`
(`meaning none = rstep`). A coded member `d` means the canonical lift of its
step, `liftStep (interpStep d)`, which quotes but does not interpret
(`liftStep_not_interprets`). Under this meaning the kernel's own code still
runs to the sealed step (`rstep_self_description`, which is
`Constitution.interp_describe` unchanged). The contrast with
`arbitrary_uncoded_assignment` is the type: at step-function type the uncoded
role is free; at reflective type the two laws fix it.

## The verdict that separates

At `genesis`, the event `require 0 0` asks that datum 0 be separated from
itself. The sealed kernel refuses it through `reqOkB`'s `i != j`; a code with
`guardRequire` off records it. So the quiescence verdict of the resulting
world is exactly the code's `guardRequire` bit (`quiescent_reads_guard`), and
the obstruction certificate for `(0, 0)` is its negation
(`obstructed_reads_guard`). One verdict at the beginning reads one bit of the
code.

Hence the interpreter is not a step function: for every
`s : World → Event → World` some code `c` makes `interpStep c` and `s`
disagree on quiescence there (`interp_not_step`; pick the code whose guard is
the opposite of the verdict `s` gives). Every coded member is such an `s`
(`coded_member_separated`, also for the obstruction certificate), and so is
the diagonal function of `tower_persists`. By `NoOutside.support_quiescent`
the verdict difference is a support difference (`verdict_entails_supp`); the
scratch result `tower_persists_operational` of 2026-10-27 gave the support
half, this is the verdict half.

## The derived relation

`VSep x y`: the meanings of `x` and `y` disagree on quiescence at some
reflective world and event. Irreflexivity, symmetry and cotransitivity are
theorems (`vsep_irrefl`, `vsep_symm`, `vsep_cotrans`); the uncoded role is
separated from every coded member (`vsep_uncoded`). The setting
`verdictBoundary` (carrier `Option ConstitutionDesc`, relation `VSep`,
endpoints kernel code and interpreter role) satisfies candidates A, Bs, Bc and
D of `Derivation/PrimitiveCore.lean` by proof (`boundary_A`, `boundary_Bs`,
`boundary_Bc`, `boundary_D`). The sealed declared relation is contained in the
derived one (`declared_le_derived`).

Collapse: identifying `none` with any coded member is obstructed relative to
`Irrefl` (`collapse_obstructed`; the sealed `i5_collapse_obstructed` covered
the kernel code only). Any reading of the carrier that keeps the coded
meanings and reads `none` as a coded member reports, at an accessible
reflective world, a quiescence verdict the lawful meaning does not
(`identification_changes_quiescence`); the same for reading `none` as the
lift of any step function at all (`identification_with_step_changes_quiescence`).

## Limits

- Not every presentational difference among codes is a verdict difference: a
  code and its `dedupAdmit` flip are never separated by one quiescence
  verdict (`coded_pair_not_vsep`). `VSep` is strictly coarser than `≠` on the
  carrier, so the boundary separation is a fact about behaviour, not about
  names. Locatedness of `VSep` (candidate `Bl`) is not claimed either way.
- Retention and protection (candidate F) hold only with the stores declared
  to be `VSep` (`boundary_F`); that is the same declared status as
  `i5_boundary_is_F`.
- At the `genesis` witness the closure family `nextFamily` under the `close`
  policy is empty either way (`nextFamily_blind_at_genesis`). The two-token
  world reached by two admissions (`twoWorld_reached`) separates it
  (`family_reads_guard`, `interp_not_step_family`).
- The witnesses are one-step. Nothing here is about evaluators of other
  types, about a 65th code (a code of evaluator type is not a code of this
  family), or about an absolute no-outside; `tower_persists` and
  `no_closed_self_interpreter` are untouched.
- Not verified by this tree: that `input.json`'s `source_revision` matches,
  or that the consumed modules are unchanged (no module digests are pinned;
  the tests check that the pinned modules are exactly the imports and that
  their files exist).

`python verify.py --check` runs the input pin, tests, strict typing, the Lean
build and the named axiom reports (all 35 within `{propext, Quot.sound}`).
`python verify.py --write-pins` regenerates the input digest.
