# Natural sections at one object: the fixed-pair criterion is an iff

AuthorityEffect: None.  This tree proposes nothing for the sealed
derivation and amends nothing under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`.

| object | id |
|---|---|
| source snapshot | `a36d34948ffd2a24ee99ec717f903f57141095c7`, tree `603478526a6c06de116c843956da7e76d280c4b6` |
| semantic root | `Derivation.PresentationNaturality` (import closure: 12 sealed modules, all pinned in `SOURCE_MANIFEST.json`) |

## Question

`PresentationNaturality.no_natural_section_of_fixed_point_free` is a
sufficient condition for naturality to FAIL over the one-object family
`autoFamily O F`: if the automorphism fixes no admissible pair, no
natural section exists.  Its contrapositive
`fixed_pair_of_natural_section` is stated.  The sealed module never
states the equivalence, and its non-claims leave every many-object
question open.  Two questions:

1. Is the converse provable -- does a natural section exist whenever the
   automorphism fixes something?
2. What is the necessary and sufficient condition, and is it stated
   anywhere in the repository?

## Results (Lean, `lean/NaturalSections.lean`; 24 reports, every one
"does not depend on any axioms")

* **`natural_section_iff_fixed_pair`** -- over `autoFamily O F`, a natural
  section exists **iff** `F` fixes an admissible pair:
  `(∃ s, IsNatural (autoFamily O F) s) ↔ ∃ p : NonZeroPair O, F.mapPair p = p`.
  The forward half is the sealed `fixed_pair_of_natural_section`; the
  backward half is `natural_section_of_fixed_pair`, the constant section.
  `hnatural_section_iff_fixed_pair` is the same statement for the indexed
  `hAutoFamily`, through the sealed bridge `hAuto_iff_auto`.  Over one
  object the whole question is this; the sealed module's own docstring
  calls the negative direction near-definitional, and the equivalence is
  no deeper.  **Proved theorem**, on every carrier and residual type.
* **`fixed_pair_iff_two_fixed_points`** -- `F.mapPair p = p` iff `F`
  fixes both components of `p`.  Since `p` is admissible, the invariant
  is: two fixed carrier points that the observer distinguishes.
  **Proved theorem.**
* **The converse as "has a fixed point" is false**, by two countermodels:
  - `fixed_point_without_natural_section` -- `cycIso` on the sealed
    `card4Obs` fixes `e1` and cycles `e2 e3 e4`.  It has a fixed point;
    its only fixed pair is `(e1, e1)`, inadmissible because
    `DiffObs.zero_refl` is a field; so it fixes no admissible pair
    (`cycIso_fixed_pair_free`) and carries no natural section.
  - `identity_fixes_everything_no_section` -- the identity on the
    one-view observer `blindObs = kernelObs (fun _ => ())` fixes every
    carrier point, and there is no section of any kind because no pair
    is admissible (`blindObs_no_admissible_pair`).
  **Countermodels.**  So "every automorphism has a fixed point" is
  neither the condition nor sufficient; "fixes an admissible pair" is
  the condition at one object.

## The many-object criterion: walks, forests, and the iff (sections 4-5)

Over a declared `HFamily` -- arrows listed with no closure, `HIsNatural`
quantifying over exactly the listed arrows -- the necessary and
sufficient condition is now a theorem, in two forms.

Definitions.  `Step D a b`: a declared arrow traversed forward (`fwd h`)
or backward (`bwd h`); `Walk D a b`: a list of steps with chained
endpoints; `Step.transport` / `Walk.transport`: the composite of the
declared transports, `mapPair` forward and `.symm.mapPair` backward;
`Walk.append`, `Walk.reverse`.  `Forest D`: a base object `root a` for
every object and a walk `path a : Walk D (root a) a` -- DATA, declared,
so no choice principle is used anywhere.  `Forest.gen h` for a declared
arrow `h : a → b` is the walk `path a ; fwd h ; (path b).reverse` from
`root a` to `root b`; `Forest.spread p` is the section that transports
the base pair `p (root a)` out along `path a`.

* **`natural_section_iff_generators`** (generator form; NO condition on
  the forest) -- a natural section exists iff some choice of pairs `p`
  satisfies, for every declared arrow `h : a → b`,
  `(T.gen h).transport (p (root a)) = p (root b)`.  Necessity is
  `Walk.transport_of_natural`: a natural section is carried to itself
  along every walk, backward steps included (`Step.transport_of_natural`
  uses the sealed `mapPair_symm_left`).  Sufficiency is the spread: the
  generator equation, after cancelling `(path b).reverse` against
  `path b` (`Walk.transport_reverse_transport`), is exactly naturality at
  `h`.  **Proved theorem**, with no axioms.
* **`natural_section_iff_holonomy`** (holonomy form; bases constant
  along arrows, `hroot : Hom a b → root a = root b`, i.e. one base per
  connected component) -- a natural section exists iff some choice of
  pairs is fixed by every closed walk at its base.  Derived from the
  generator form through `walk_maps_of_closed_fixed`, which turns
  "fixed by every closed walk at `r`" into "carried along any walk from
  `r` to a base equal to `r`" by substituting the equality of bases.
  **Proved theorem**, with no axioms.
* **`one_object_recovered`** -- the general theorem, specialised to
  `hAutoFamily O F` with the trivial forest (`root _ = ()`,
  `path _ = nil`), is the one-object iff of section 1: the single
  generator is `F` itself.  A consistency check, not new content.
  **Proved theorem.**

What the proofs settled about the clauses assessed before they were
written.  (a) Backward traversal: built into `Step.bwd`; the two
cancellation lemmas `Walk.reverse_transport_transport` and
`Walk.transport_reverse_transport` rest on the sealed
`mapPair_symm_left/right` and nothing else.  (b) One base per
component: needed only for the holonomy form (`hroot`); the generator
form holds for ANY assignment of bases and walks, including one that is
not a forest at all.  That is stronger than the assessed statement.  (c)
The fixed pair is common per base: it is `p (root a)`, one value per
base.  (d) The generators suffice: the generator form IS the theorem;
the holonomy form is derived from it, not the other way round.  (e) The
section is determined by its base values: it is `Forest.spread p`, and
the choice of walks changes the construction, not existence.
Existential per-base pairs would need choice to assemble; the theorem
quantifies over a function `p : HSec D` instead, which is the
constructive statement and the one that says the same thing.

Relation to the sealed module.  `no_natural_section_of_endo` is the
length-one-loop case of `Walk.transport_of_natural`; the sealed
non-claims -- multi-object families, naturality under a generating set,
arrows crossing objects with different carriers -- are now covered by
these theorems as far as `HFamily` reaches, and `HFamily` already
allows carriers and residual types to vary with the object.  The
sealed module is not amended; it is imported.

Still open.  No fixture exercises the holonomy form on a family with a
genuinely nontrivial closed walk of length above one, and no finite
computation of holonomy classes exists yet; the parity case
(admissible pairs `{(a, b), (b, a)}`, every transport identity or
swap) is where the first such fixture belongs.  A general embedding of
the flat `Family` into `HFamily` is untouched and remains the sealed
module's OPEN item.

## Boundary and write root

Write root: `research/natural_sections/`.  The Lean package declares
NO Lake dependency: a path dependency on `../../../lean4` is built in
`lean4/.lake/`, outside the write root (a reviewer showed this on the
sibling S9-obligations tree).  Instead `verify_lean.py` stages the
snapshot blob of each of the 12 pinned modules, SHA-256-checked against
the manifest, into `lean/sealed/` (gitignored), and the `Derivation`
library of `lakefile.lean` compiles them inside `lean/.lake/`.  The
verifier diffs a repository-wide `git status --ignored` before and after
the build and fails by name on any new record outside the write root;
`test_clean_build_leaves_lean4_untouched_and_stays_inside_the_root`
rebuilds from nothing and asserts `lean4/.lake` is as present or absent
as before.  Verified on a checkout with no `lean4/.lake`: exit 0, and
none afterwards.

`SOURCE_MANIFEST.json` follows the primitive-difference tower's shape;
`verify_pins.py` resolves the snapshot, requires it to be an ancestor of
HEAD with the recorded tree, hashes every module at the snapshot and at
HEAD, requires the module list to equal the import closure of the root
in both directions, and refuses any modified, untracked, or
ignored-but-present file under a sealed prefix.

## Manual receipt

This tree's axiom reports are a manual receipt.  No CI gate reads them.
Nothing in `.github/workflows` runs `verify_lean.py` or `verify_pins.py`;
a pass is a receipt for the sources present when it ran and implies no
enforcement.  The registration diff that would add the Python checks to
the research job (not `verify_lean.py`, for the sibling trees' reason)
is the same shape as the sibling steps; it is not applied here.

## Non-claims

* No categorical structure is claimed for `Family`, `HFamily`, `Step`,
  `Walk`, or `Forest`; a walk is a list, "holonomy" names the transport
  along a closed walk, and no groupoid, fundamental group, or covering
  is asserted.
* A `Forest` is any assignment of bases and walks; nothing here proves
  that a spanning forest exists for a given family, and the theorems do
  not need one to.
* Nothing here derives `ContactKernel.no_equivariant_pair_valued_map`
  or touches the OPEN items the sealed module records.
* The countermodels separate the fixed-point reading from the
  fixed-pair reading; they say nothing about which automorphisms arise
  from any presentation theory.

## Commands (run from the repository root)

| command | exit | key line |
|---|---|---|
| `python research/natural_sections/verify_pins.py` | 0 | `import closure of ['Derivation.PresentationNaturality']: 12 module(s), all pinned`; `sealed prefixes clean` |
| `python research/natural_sections/verify_lean.py` | 0 | `Lean #print axioms declarations: 24 within ['Quot.sound', 'propext']`; every report `no axioms`; `write root respected` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | `Ran 23 tests`, `OK` (the clean rebuild included) |
| `cd research/natural_sections && python -m mypy` | 0 | strict, 3 source files |
