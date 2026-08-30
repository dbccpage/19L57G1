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

## Results (Lean, `lean/NaturalSections.lean`; 12 reports, every one
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

## The many-object criterion: stated, assessed, NOT proved

Over a declared `Family` or `HFamily` -- arrows listed with no closure,
`IsNatural` quantifying over exactly the listed arrows -- the proposed
necessary and sufficient condition is:

> Relative to a declared spanning forest `T` of the undirected graph
> whose vertices are the objects and whose edges are the declared
> arrows, a natural section exists **iff** at each root of `T` some
> admissible pair is fixed by every holonomy at that root, where a
> holonomy is the transport around a closed walk that may traverse
> declared arrows forward (`mapPair`) or backward (`.symm.mapPair`).

Assessment, recorded here because it is the next target and the claim
must not be read as proved:

* The statement is right, with these clauses load-bearing.  (a) Backward
  traversal is legitimate and necessary: each `mapPair` is a bijection
  on admissible pairs (the sealed `mapPair_symm_left/right`), so the
  arrow equation `mapPair f (s a) = s b` is equivalent to
  `s a = f.symm.mapPair (s b)`, and a family with no closure still
  constrains both ways.  (b) A forest has exactly one root per connected
  component; an arrow-less object is its own component, and there the
  condition reduces to viability (some admissible pair exists).  (c) The
  fixed pair must be common to every holonomy at the same root; pairs at
  different roots are independent.  (d) It suffices to check the
  generators `T_b⁻¹ ∘ f ∘ T_a` for each declared arrow `f : a → b`,
  where `T_x` is the tree path from the root to `x`; every closed walk
  is a product of those, so a pair fixed by the generators is fixed by
  all holonomies.  With finitely many objects and arrows that is a
  finite check.  (e) On a component, a natural section is determined by
  its value at the root: `s b = T_b (s root)` for any walk, all agreeing
  exactly because the holonomies fix that value.  So the choice of `T`
  changes the *construction* of the section, not whether one exists.
* Sufficiency is constructive only because `T` is data: to build the
  section one transports the root pair along the tree path to each
  object, and choosing a walk per object without a declared forest would
  need a choice principle the repository forbids.  The theorem must
  therefore be stated relative to a declared forest, not to an
  existential one.
* The sealed `no_natural_section_of_endo` is the length-one-loop case of
  the necessary direction; the one-object iff above is the case where
  every holonomy is a power of one `F` (a pair fixed by `F` is fixed by
  all its powers).  The parity case -- admissible pairs at the root are
  `{(a, b), (b, a)}` and every transport is identity or swap -- is the
  case where the holonomy group is the two-element group and the
  condition reads "every cycle has even swap-parity"; `boolEqObs` with
  `negIso` is the nontrivial class on a one-cycle.
* **Not stated anywhere in the repository.**  `PresentationNaturality`
  §"Non-claims" and §14 list multi-object families, naturality under a
  generating set, and arrows crossing objects as OPEN; the claim ledger
  entry for `no_natural_section_of_endo` repeats that and lists "a
  heterogeneous family where the endo obstruction fails" as a falsifier.
  The research tower imports `IsNatural` only for the Boolean instance.
  No walk, holonomy, or section-from-fixed-pair construction exists
  anywhere in `lean4/` or `research/`.
* What would carry it: a `Walk` type over a declared family (a list of
  arrows with directions, endpoints checked), `transport` along a walk
  by folding `mapPair`/`.symm.mapPair`, a `Forest` structure supplying a
  root and a tree walk per object with the endpoint proofs as fields,
  and the iff with the section built by transport along the tree walks.
  Everything is finite data and needs no choice principle.  **Open;
  not attempted here.**

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

* Nothing here is about many-object families beyond the one-object
  bridge the sealed module already proves; the forest criterion above
  is an assessed target, not a result.
* No categorical structure is claimed for `Family`, `HFamily`, or the
  walks described; "holonomy" above names a composite of declared
  transports, nothing more.
* Nothing here derives `ContactKernel.no_equivariant_pair_valued_map`
  or touches the OPEN items the sealed module records.
* The countermodels separate the fixed-point reading from the
  fixed-pair reading; they say nothing about which automorphisms arise
  from any presentation theory.

## Commands (run from the repository root)

| command | exit | key line |
|---|---|---|
| `python research/natural_sections/verify_pins.py` | 0 | `import closure of ['Derivation.PresentationNaturality']: 12 module(s), all pinned`; `sealed prefixes clean` |
| `python research/natural_sections/verify_lean.py` | 0 | `Lean #print axioms declarations: 12 within ['Quot.sound', 'propext']`; every report `no axioms`; `write root respected` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | `Ran 23 tests`, `OK` (the clean rebuild included) |
| `cd research/natural_sections && python -m mypy` | 0 | strict, 3 source files |
