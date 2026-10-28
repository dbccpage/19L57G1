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

Both laws are admitted here as the reading of those tags; nothing derives
them, and everything below is relative to them. Exactly one reflective step
satisfies both: `rstep`, "run the code the world
carries". The content is pointwise (`lawful_unique_at`: at every reflective
world and event, any step that interprets and quotes gives `rstep`'s value);
`lawful_unique` packages it as one function equation by `funext` and is used
by nothing else. That is the meaning given to `none`
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
the verdict difference is a support difference (`verdict_entails_supp`), so
the support half, first shown by a scratch result of 2026-10-27
(`tower_persists_operational`, outside this repository and not an input
here), is re-proved from the verdict half.

The quantifier in `interp_not_step` is a fact of typing: a step function
takes no code, so the interpreter, which reads one, is matched against it at
every code. The content is the one-guard witness, not the quantifier. At a
reflective world carrying the code `d`, the coded member `d` and the
interpreter coincide; see the section on the aligned code below.

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

## The aligned code, the guards and well-formedness

Added after the review of 2026-10-28, which asked two questions. Does any
difference between a code and the interpreter survive when the reflective
world carries that very code? Does the separation survive when both
executions preserve the sealed well-formedness invariant?

**Alignment: no, by definition.** At a reflective world carrying `d`,
`meaning (some d) (d, w) e = meaning none (d, w) e` is `rfl`
(`aligned_coded_equals_uncoded`); no function of the outcome, of any type,
tells them apart (`aligned_no_verdict`); the two trajectories coincide along
every event sequence (`aligned_trajectory`). So `VSep (some d) none` is
witnessed exactly at a reflective world carrying a code other than `d`
(`vsep_uncoded_iff`). The interpreter is told from a coded member by nothing
but its reading of the other codes. A difference that survives alignment
does not exist at this type; the sentence "even when a code is the one being
interpreted, an irreducible difference remains" is refuted here, not left
open.

**Guards: every separation needs one.** `guardsPass w e` collects the
conditions the sealed step tests before acting. When they all pass, every
code performs the sealed step (`codes_agree_of_guardsPass`), so two codes
can disagree on quiescence only where a guard decides
(`codes_separated_needs_guard`), and so can the uncoded role and a coded
member (`vsep_uncoded_needs_guard`). The `require` instance is
`require_guard_irrelevant`: with `reqOkB w i j` true, the `guardRequire`
toggle changes nothing. This is the recurrence test the review asked for,
as a theorem: a separation certificate always names a deciding guard.

**Well-formedness: the separation survives it.** The `genesis` witness is a
rejected challenge: `reqOkB genesis 0 0 = false`, the kernel's outcome is
well formed, and a code with `guardRequire` off records the self-requirement
and breaks `Represented.WF` (`genesis_witness_rejected`,
`genesis_witness_kernel_wf`, `genesis_witness_unguarded_not_wf`). Every
other guard preserves well-formedness at every event (`wf_interpStep`). The
second witness uses one. `accWorld` (two tokens, the view `[0]`, the
requirement `(0, 1)`, one unit of budget) is reached from `genesis` by five
kernel steps and is well formed (`accWorld_reached`, `accWorld_wf`). The
event `mark [0] 1` is rejected by the kernel's acceptance guard because it
discharges nothing (`accWorld_kernel_rejects`); a code with `guardAccept`
off applies it, which puts `1` into the only view and breaks the one
requirement. Both outcomes are well formed and they disagree on quiescence
(`quiescent_reads_accept`, `accWorld_outputs_wf`). So the interpreter is
separated from every step function (`interp_not_step_wf`) and from every
coded member (`vsep_uncoded_wf`) at a well-formed, kernel-reachable world
with both outcomes well formed. The certificate of each witness is explicit:
whether the kernel's guard passes (`genesis_witness_guard_decides`,
`accWorld_guard_decides`), whether each outcome is well formed, and which
guard decides (`guardRequire` at `genesis`, `guardAccept` at `accWorld`).

**What Genesis is entitled to conclude.** The interpreter is a primitive
difference from every coded member in the sense proved: at some reflective
world carrying another code, at an event where a guard decides, the two
report different quiescence verdicts, and this survives the requirement that
both executions stay well formed. The difference is the admitted ability to
interpret alternative codes, exercised where a guard decides, and nothing
else.

## Metatheory and represented structure

The represented objects are the sealed module's: a world (finite lists), an
event, a code (six booleans, 64 in all) and the verdicts read off a world. A
reflective world pairs a world with the code it runs under, as the sealed
`Constitution.GWorld` pairs a world with its represented policy. The carrier
of `verdictBoundary` is the 65 occurrences of `Option ConstitutionDesc`,
never a function type. `rstep` is defined from `interpStep` and has
`interpStep`'s status: constitution, fixed metatheory, not represented state.

The statements quantified over every step function `s : World → Event →
World` (`interp_not_step`, `verdict_entails_supp`, `rstep_not_lift`,
`rstep_ne_lift`, `liftStep_not_interprets`, `interp_not_step_family`,
`identification_with_step_changes_quiescence`) and over every reading `I`
(`identification_changes_quiescence`) are schemata of the metatheory. Each
instance is about one `s` or one `I`; the witness code is computed from one
evaluation of `s` at `genesis` under `require 0 0`; no collection of step
functions, readings or worlds is formed or admitted anywhere. Every
existential is witnessed by a concrete finite object (`genesis` or
`twoWorld`, `require 0 0`, a code). Hypotheses about readings are stated
value by value, and the uniqueness of the lawful meaning is proved pointwise
(`lawful_unique_at`); the one function equation (`lawful_unique`) is a
`funext` packaging that nothing else uses. The tree admits no observer,
container, continuum or infinite family of presentations; the only infinite
type in play is the sealed `World`, which Genesis already has.

## Limits

- The separation of the uncoded role from a coded member is extensional
  across codes: witnessed at a reflective world carrying another code, never
  at an aligned one (`aligned_no_verdict`). Nothing here separates a code
  from the interpreter running that code.
- The `genesis` witness compares a guarded execution with one that records a
  rejected requirement and leaves well-formedness; `accWorld` is the witness
  to cite where both outcomes must be well formed. The family witness at
  `twoWorld` has the `genesis` character.
- The two laws that fix the meaning of `none` are admitted, not derived.
- The tree's Python checks custody (pins and imports) only; every claim about
  behaviour is a Lean theorem.

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
  family), or about an absolute no-outside; the sealed `tower_persists`,
  `family_missed` and `i5_family_not_extensionally_complete` are untouched.
- Not verified by this tree: that `input.json`'s `source_revision` matches,
  or that the consumed modules are unchanged (no module digests are pinned;
  the tests check that the pinned modules are exactly the imports and that
  their files exist).

`python verify.py --check` runs the input pin, tests, strict typing, the Lean
build and the named axiom reports (all 59 within `{propext, Quot.sound}`).
`python verify.py --write-pins` regenerates the input digest.
